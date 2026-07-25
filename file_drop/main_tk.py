import sys
import asyncio
import os
import json
import webbrowser
import threading
import locale
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .server import FileTransferServer
from .client import FileTransferClient
from .qr_manager import QRCodeManager

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PORT = 45000
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")

RUSTORE_URL = "#"
GITHUB_URL = "#"
TELEGRAM_URL = "#"

LANGUAGES = {
    "en": {
        "title": "FileDrop Desktop",
        "server_starting": "Starting server...",
        "server_running": "Server running (port 45000)",
        "send": "Send",
        "receive": "Receive",
        "settings": "Settings",
        "device_ip": "Device IP:",
        "no_file": "No file selected",
        "browse": "Browse",
        "send_btn": "Send",
        "qr_code": "QR-code",
        "scan_qr": "Scan QR-code",
        "received_files": "Received files",
        "open_folder": "Open folder",
        "save_to": "Save to:",
        "change": "Change",
        "language": "Language:",
        "qr_position": "QR position:",
        "qr_bottom": "Bottom",
        "qr_right": "Right",
        "qr_tab": "Tab",
        "refresh_qr": "Refresh QR",
        "connecting": "Connecting...",
        "checking": "Checking connection...",
        "sending": "Sending file...",
        "sent": "Sent:",
        "kb": "KB",
        "success_sent": "File sent successfully!",
        "device_unreachable": "Device unreachable.",
        "no_file_warn": "No file",
        "no_file_msg": "Please select a file to send.",
        "no_ip_warn": "No IP",
        "no_ip_msg": "Enter device IP address.",
        "select_file": "Select file",
        "select_folder": "Select save folder",
        "folder_changed": "Folder changed",
        "folder_changed_msg": "Files will be saved to:",
        "error": "Error",
        "success": "Success",
        "ip_example": "For example: 192.168.1.5",
        "footer": "FileDrop Desktop v1.0 | TCP port: 45000",
        "qr_hint": "1. Open app on Android\n2. Press Scan QR\n3. Point camera at code",
        "restart_msg": "Restart app to apply language",
    },
    "ru": {
        "title": "FileDrop Desktop",
        "server_starting": "Запуск сервера...",
        "server_running": "Сервер запущен (порт 45000)",
        "send": "Отправить",
        "receive": "Получить",
        "settings": "Настройки",
        "device_ip": "IP устройства:",
        "no_file": "Файл не выбран",
        "browse": "Обзор",
        "send_btn": "Отправить",
        "qr_code": "QR-код",
        "scan_qr": "Сканируйте QR-код",
        "received_files": "Полученные файлы",
        "open_folder": "Открыть папку",
        "save_to": "Сохранять в:",
        "change": "Сменить",
        "language": "Язык:",
        "qr_position": "Положение QR:",
        "qr_bottom": "Снизу",
        "qr_right": "Справа",
        "qr_tab": "Вкладка",
        "refresh_qr": "Обновить QR",
        "connecting": "Подключение...",
        "checking": "Проверка соединения...",
        "sending": "Отправка файла...",
        "sent": "Отправлено:",
        "kb": "КБ",
        "success_sent": "Файл успешно отправлен!",
        "device_unreachable": "Устройство недоступно.",
        "no_file_warn": "Нет файла",
        "no_file_msg": "Пожалуйста, выберите файл для отправки.",
        "no_ip_warn": "Нет IP",
        "no_ip_msg": "Введите IP-адрес устройства.",
        "select_file": "Выбрать файл",
        "select_folder": "Выбрать папку сохранения",
        "folder_changed": "Папка изменена",
        "folder_changed_msg": "Файлы будут сохраняться в:",
        "error": "Ошибка",
        "success": "Успех",
        "ip_example": "Например: 192.168.1.5",
        "footer": "FileDrop Desktop v1.0 | TCP порт: 45000",
        "qr_hint": "1. Откройте приложение на Android\n2. Нажмите Сканировать QR\n3. Наведите камеру на код",
        "restart_msg": "Перезапустите приложение для смены языка",
    }
}

def load_settings():
    defaults = {
        "save_dir": os.path.join(os.path.expanduser("~"), "Downloads", "FileDrop"),
        "language": "system",
        "qr_position": "bottom"
    }
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            for k, v in defaults.items():
                if k not in data:
                    data[k] = v
            return data
    except:
        return defaults

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def get_system_language():
    try:
        lang = locale.getlocale()[0]
        if lang and lang.startswith("ru"):
            return "ru"
    except:
        pass
    return "en"

class FileDropApp:
    def __init__(self):
        self.settings = load_settings()
        self.lang_code = self.settings["language"] if self.settings["language"] != "system" else get_system_language()
        self.tr = LANGUAGES[self.lang_code]

        self.root = tk.Tk()
        self.root.title(self.tr["title"])
        self.root.geometry("750x580")
        self.root.configure(bg="#fafafa")
        self.root.minsize(650, 500)

        self.selected_file = None
        self.server = None
        self.server_thread = None
        self.save_dir = self.settings["save_dir"]
        os.makedirs(self.save_dir, exist_ok=True)

        self.init_ui()
        self.start_server()

    def start_server(self):
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.server = FileTransferServer(save_dir=self.save_dir, port=PORT)
            try:
                loop.run_until_complete(self.server.start())
                self.root.after(0, lambda: self.status_label.config(text=self.tr["server_running"], fg="green"))
                loop.run_forever()
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f"Error: {e}", fg="red"))
        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()

    def init_ui(self):
        self.status_label = tk.Label(self.root, text=self.tr["server_starting"], font=("Arial", 11), bg="#fafafa", fg="gray")
        self.status_label.pack(fill="x", padx=15, pady=(15, 0))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=5)

        # Send tab
        send_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(send_frame, text=self.tr["send"])

        ip_frame = tk.Frame(send_frame, bg="white")
        ip_frame.pack(fill="x", padx=15, pady=(15, 10))
        tk.Label(ip_frame, text=self.tr["device_ip"], font=("Arial", 11), bg="white").pack(side="left")
        self.ip_entry = tk.Entry(ip_frame, font=("Arial", 11), width=20)
        self.ip_entry.pack(side="left", padx=(10, 0))
        self.ip_entry.insert(0, "192.168.43.1")

        file_frame = tk.Frame(send_frame, bg="white")
        file_frame.pack(fill="x", padx=15, pady=5)
        self.file_label = tk.Label(file_frame, text=self.tr["no_file"], font=("Arial", 10),
                                   bg="#f5f5f5", fg="gray", anchor="w", relief="solid", bd=1, padx=8, pady=6)
        self.file_label.pack(fill="x", side="left", expand=True)
        tk.Button(file_frame, text=self.tr["browse"], font=("Arial", 10), bg="#FF9800", fg="white",
                  relief="flat", padx=14, pady=4, command=self.browse_file).pack(side="left", padx=(10, 0))

        tk.Button(send_frame, text=self.tr["send_btn"], font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  relief="flat", padx=20, pady=8, command=self.send_file).pack(pady=15)

        self.progress = ttk.Progressbar(send_frame, mode="determinate", length=400)
        self.progress.pack(pady=5)
        self.send_status = tk.Label(send_frame, text="", font=("Arial", 10), bg="white", fg="gray")
        self.send_status.pack()

        # Receive tab
        recv_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(recv_frame, text=self.tr["receive"])

        dir_frame = tk.Frame(recv_frame, bg="white")
        dir_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(dir_frame, text=self.tr["save_to"], font=("Arial", 11), bg="white").pack(side="left")
        self.dir_label = tk.Label(dir_frame, text=self.save_dir, font=("Arial", 9),
                                  bg="#f5f5f5", fg="#333", anchor="w", relief="solid", bd=1, padx=6, pady=4)
        self.dir_label.pack(side="left", fill="x", expand=True, padx=(5, 5))
        tk.Button(dir_frame, text=self.tr["change"], font=("Arial", 9), bg="#2196F3", fg="white",
                  relief="flat", padx=10, pady=2, command=self.change_save_dir).pack(side="right")

        tk.Label(recv_frame, text=self.tr["received_files"], font=("Arial", 13, "bold"), bg="white").pack(pady=(10, 5))
        self.received_list = tk.Listbox(recv_frame, font=("Arial", 11), height=8, relief="solid", bd=1)
        self.received_list.pack(fill="both", expand=True, padx=15, pady=5)
        tk.Button(recv_frame, text=self.tr["open_folder"], font=("Arial", 10), bg="#607D8B", fg="white",
                  relief="flat", padx=14, pady=4, command=self.open_folder).pack(pady=(5, 10))

        # Settings tab
        settings_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(settings_frame, text=self.tr["settings"])

        lang_frame = tk.Frame(settings_frame, bg="white")
        lang_frame.pack(fill="x", padx=15, pady=(15, 10))
        tk.Label(lang_frame, text=self.tr["language"], font=("Arial", 11), bg="white").pack(side="left")
        self.lang_var = tk.StringVar(value=self.lang_code)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["en", "ru"], state="readonly", width=5)
        lang_combo.pack(side="left", padx=(10, 0))
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        qr_frame = tk.Frame(settings_frame, bg="white")
        qr_frame.pack(fill="x", padx=15, pady=5)
        tk.Label(qr_frame, text=self.tr["qr_position"], font=("Arial", 11), bg="white").pack(side="left")
        self.qr_var = tk.StringVar(value=self.settings["qr_position"])
        for text, val in [(self.tr["qr_bottom"], "bottom"), (self.tr["qr_right"], "right"), (self.tr["qr_tab"], "tab")]:
            tk.Radiobutton(qr_frame, text=text, variable=self.qr_var, value=val,
                          bg="white", command=self.change_qr_position).pack(side="left", padx=5)

        # QR frames
        self.qr_frame_bottom = tk.Frame(self.root, bg="white", relief="solid", bd=1)
        self.qr_label_bottom = tk.Label(self.qr_frame_bottom, bg="white")
        self.qr_label_bottom.pack(pady=5)
        self.qr_info_bottom = tk.Label(self.qr_frame_bottom, text="", font=("Consolas", 9), bg="white", fg="#555")
        self.qr_info_bottom.pack()

        self.qr_frame_right = tk.Frame(self.root, bg="white", relief="solid", bd=1)
        self.qr_label_right = tk.Label(self.qr_frame_right, bg="white")
        self.qr_label_right.pack(pady=5)
        self.qr_info_right = tk.Label(self.qr_frame_right, text="", font=("Consolas", 9), bg="white", fg="#555")
        self.qr_info_right.pack()

        self.apply_qr_position()

        # Footer
        bottom_frame = tk.Frame(self.root, bg="#fafafa")
        bottom_frame.pack(fill="x", padx=15, pady=(5, 3))
        tk.Label(bottom_frame, text=self.tr["footer"], font=("Arial", 9), bg="#fafafa", fg="#aaa").pack(side="left")
        for text, url, color in [("RuStore", RUSTORE_URL, "#005FF9"),
                                  ("GitHub", GITHUB_URL, "#24292e"),
                                  ("TG", TELEGRAM_URL, "#0088cc")]:
            tk.Button(bottom_frame, text=text, font=("Arial", 9, "bold"), bg=color, fg="white",
                     relief="flat", padx=10, pady=2, command=lambda u=url: webbrowser.open(u)).pack(side="right", padx=3)

    def apply_qr_position(self):
        pos = self.settings["qr_position"]

        # Hide all QR frames
        self.qr_frame_bottom.pack_forget()
        self.qr_frame_right.pack_forget()

        # Remove QR tab if exists
        for i in range(self.notebook.index("end")):
            if self.notebook.tab(i, "text") == self.tr["qr_code"]:
                self.notebook.forget(i)
                break

        if pos == "bottom":
            self.qr_frame_bottom.pack(fill="x", padx=15, pady=(0, 10), after=self.notebook)
            self._update_qr(self.qr_label_bottom, self.qr_info_bottom, 140)

        elif pos == "right":
            self.qr_frame_right.pack(side="right", fill="y", padx=(10, 15), pady=(0, 10), after=self.notebook)
            self._update_qr(self.qr_label_right, self.qr_info_right, 180)

        elif pos == "tab":
            qr_tab = tk.Frame(self.notebook, bg="white")
            qr_label_tab = tk.Label(qr_tab, bg="white")
            qr_label_tab.pack(pady=15)
            qr_info_tab = tk.Label(qr_tab, text="", font=("Consolas", 11), bg="white", fg="#555")
            qr_info_tab.pack(pady=5)
            hint = tk.Label(qr_tab, text=self.tr["qr_hint"], font=("Arial", 10), bg="white", fg="#888")
            hint.pack(pady=10)
            self.notebook.add(qr_tab, text=self.tr["qr_code"])
            self._update_qr(qr_label_tab, qr_info_tab, 250)

    def _update_qr(self, label_widget, info_widget, size):
        try:
            data = QRCodeManager.generate_connection_data(PORT)
            img = QRCodeManager.generate_qr_image(data, size)
            from PIL import ImageTk
            tk_img = ImageTk.PhotoImage(img)
            label_widget.config(image=tk_img)
            label_widget.image = tk_img
            info = json.loads(data)
            info_widget.config(text=f"IP: {info['ip']}  Port: {info['port']}")
        except Exception as e:
            print(f"QR error: {e}")

    def change_language(self, event=None):
        self.settings["language"] = self.lang_var.get()
        save_settings(self.settings)
        messagebox.showinfo("Info", self.tr["restart_msg"])

    def change_qr_position(self):
        self.settings["qr_position"] = self.qr_var.get()
        save_settings(self.settings)
        self.apply_qr_position()

    def change_save_dir(self):
        path = filedialog.askdirectory(title=self.tr["select_folder"])
        if path:
            self.save_dir = path
            self.dir_label.config(text=path)
            self.settings["save_dir"] = path
            save_settings(self.settings)
            self.server.save_dir = path
            self.received_list.delete(0, tk.END)
            messagebox.showinfo(self.tr["folder_changed"], f"{self.tr['folder_changed_msg']}\n{path}")

    def browse_file(self):
        path = filedialog.askopenfilename(title=self.tr["select_file"])
        if path:
            self.selected_file = path
            self.file_label.config(text=os.path.basename(path), fg="#333")

    def send_file(self):
        if not self.selected_file:
            messagebox.showwarning(self.tr["no_file_warn"], self.tr["no_file_msg"])
            return
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning(self.tr["no_ip_warn"], self.tr["no_ip_msg"])
            return
        self.send_status.config(text=self.tr["connecting"], fg="gray")
        self.progress["value"] = 0
        threading.Thread(target=self._do_send, args=(ip,), daemon=True).start()

    def _do_send(self, ip):
        async def run():
            client = FileTransferClient(ip, PORT)
            try:
                if not await client.ping():
                    self.root.after(0, lambda: self._done(False, self.tr["device_unreachable"]))
                    return
                self.root.after(0, lambda: self.send_status.config(text=self.tr["sending"]))
                def progress(sent, total):
                    self.root.after(0, lambda: self._update_progress(sent, total))
                await client.send_file(self.selected_file, progress_callback=progress)
                self.root.after(0, lambda: self._done(True, self.tr["success_sent"]))
            except Exception as e:
                self.root.after(0, lambda: self._done(False, f"{self.tr['error']}: {e}"))
        asyncio.run(run())

    def _update_progress(self, sent, total):
        self.progress["maximum"] = total
        self.progress["value"] = sent
        pct = (sent / total) * 100
        self.send_status.config(text=f"{self.tr['sent']} {sent//1024} / {total//1024} {self.tr['kb']} ({pct:.1f}%)")

    def _done(self, success, msg):
        if success:
            self.progress["value"] = self.progress["maximum"]
            self.send_status.config(text=msg, fg="green")
            messagebox.showinfo(self.tr["success"], msg)
        else:
            self.send_status.config(text=msg, fg="red")
            messagebox.showerror(self.tr["error"], msg)

    def open_folder(self):
        os.system(f'xdg-open "{os.path.abspath(self.save_dir)}"')

    def run(self):
        self.root.mainloop()

def main():
    app = FileDropApp()
    app.run()

if __name__ == "__main__":
    main()
