import sys
import asyncio
import os
import json
import webbrowser
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .server import FileTransferServer
from .client import FileTransferClient
from .qr_manager import QRCodeManager

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAVE_DIR = os.path.join(APP_DIR, "received_files")
PORT = 45000

RUSTORE_URL = "#"
GITHUB_URL = "#"
TELEGRAM_URL = "#"

class FileDropApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FileDrop Desktop")
        self.root.geometry("700x500")
        self.root.configure(bg="#fafafa")
        self.root.minsize(650, 450)

        self.selected_file = None
        self.server = None
        self.server_thread = None

        os.makedirs(SAVE_DIR, exist_ok=True)

        self.init_ui()

        self.start_server()

    def start_server(self):
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.server = FileTransferServer(save_dir=SAVE_DIR, port=PORT)
            try:
                loop.run_until_complete(self.server.start())
                self.root.after(0, lambda: self.status_label.config(text="Server running (port 45000)", fg="green"))
                loop.run_forever()
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f"Server error: {e}", fg="red"))

        self.server_thread = threading.Thread(target=run, daemon=True)
        self.server_thread.start()

    def init_ui(self):
        top_frame = tk.Frame(self.root, bg="#fafafa")
        top_frame.pack(fill="x", padx=15, pady=(15, 5))

        self.status_label = tk.Label(top_frame, text="Starting server...", font=("Arial", 11), bg="#fafafa", fg="gray")
        self.status_label.pack(side="left")

        qr_btn = tk.Button(top_frame, text="QR-code", font=("Arial", 10), bg="#2196F3", fg="white",
                           relief="flat", padx=12, pady=4, command=self.show_qr)
        qr_btn.pack(side="right")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=5)

        # Send tab
        send_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(send_frame, text="Send")

        ip_frame = tk.Frame(send_frame, bg="white")
        ip_frame.pack(fill="x", padx=15, pady=(15, 10))
        tk.Label(ip_frame, text="Device IP:", font=("Arial", 11), bg="white").pack(side="left")
        self.ip_entry = tk.Entry(ip_frame, font=("Arial", 11), width=20)
        self.ip_entry.pack(side="left", padx=(10, 0))
        self.ip_entry.insert(0, "192.168.43.1")

        file_frame = tk.Frame(send_frame, bg="white")
        file_frame.pack(fill="x", padx=15, pady=5)
        self.file_label = tk.Label(file_frame, text="No file selected", font=("Arial", 10),
                                   bg="#f5f5f5", fg="gray", anchor="w", relief="solid", bd=1, padx=8, pady=6)
        self.file_label.pack(fill="x", side="left", expand=True)
        tk.Button(file_frame, text="Browse", font=("Arial", 10), bg="#FF9800", fg="white",
                  relief="flat", padx=14, pady=4, command=self.browse_file).pack(side="left", padx=(10, 0))

        tk.Button(send_frame, text="Send", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                  relief="flat", padx=20, pady=8, command=self.send_file).pack(pady=15)

        self.progress = ttk.Progressbar(send_frame, mode="determinate", length=400)
        self.progress.pack(pady=5)

        self.send_status = tk.Label(send_frame, text="", font=("Arial", 10), bg="white", fg="gray")
        self.send_status.pack()

        # Receive tab
        recv_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(recv_frame, text="Receive")

        tk.Label(recv_frame, text="Received files", font=("Arial", 13, "bold"), bg="white").pack(pady=(15, 10))

        self.received_list = tk.Listbox(recv_frame, font=("Arial", 11), height=12, relief="solid", bd=1)
        self.received_list.pack(fill="both", expand=True, padx=15, pady=5)

        tk.Button(recv_frame, text="Open folder", font=("Arial", 10), bg="#607D8B", fg="white",
                  relief="flat", padx=14, pady=4, command=self.open_folder).pack(pady=(5, 15))

        # Bottom
        bottom_frame = tk.Frame(self.root, bg="#fafafa")
        bottom_frame.pack(fill="x", padx=15, pady=(0, 10))

        tk.Label(bottom_frame, text="FileDrop Desktop v1.0 | TCP port: 45000",
                font=("Arial", 9), bg="#fafafa", fg="#aaa").pack(side="left")

        for text, url, color in [("RuStore", RUSTORE_URL, "#005FF9"),
                                  ("GitHub", GITHUB_URL, "#24292e"),
                                  ("TG", TELEGRAM_URL, "#0088cc")]:
            tk.Button(bottom_frame, text=text, font=("Arial", 9, "bold"), bg=color, fg="white",
                     relief="flat", padx=10, pady=2, command=lambda u=url: webbrowser.open(u)).pack(side="right", padx=3)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.selected_file = path
            self.file_label.config(text=os.path.basename(path), fg="#333")

    def send_file(self):
        if not self.selected_file:
            messagebox.showwarning("No file", "Please select a file to send.")
            return

        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showwarning("No IP", "Enter device IP address.")
            return

        self.send_status.config(text="Connecting...", fg="gray")
        self.progress["value"] = 0

        threading.Thread(target=self._do_send, args=(ip,), daemon=True).start()

    def _do_send(self, ip):
        async def run():
            client = FileTransferClient(ip, PORT)
            try:
                if not await client.ping():
                    self.root.after(0, lambda: self._done(False, "Device unreachable."))
                    return

                self.root.after(0, lambda: self.send_status.config(text="Sending..."))

                def progress(sent, total):
                    self.root.after(0, lambda: self._update_progress(sent, total))

                await client.send_file(self.selected_file, progress_callback=progress)
                self.root.after(0, lambda: self._done(True, "File sent successfully!"))

            except Exception as e:
                self.root.after(0, lambda: self._done(False, f"Error: {e}"))

        asyncio.run(run())

    def _update_progress(self, sent, total):
        self.progress["maximum"] = total
        self.progress["value"] = sent
        pct = (sent / total) * 100
        self.send_status.config(text=f"Sent: {sent//1024} / {total//1024} KB ({pct:.1f}%)")

    def _done(self, success, msg):
        if success:
            self.progress["value"] = self.progress["maximum"]
            self.send_status.config(text=msg, fg="green")
            messagebox.showinfo("Success", msg)
        else:
            self.send_status.config(text=msg, fg="red")
            messagebox.showerror("Error", msg)

    def open_folder(self):
        path = os.path.abspath(SAVE_DIR)
        os.system(f'xdg-open "{path}"')

    def show_qr(self):
        try:
            data = QRCodeManager.generate_connection_data(PORT)
            img = QRCodeManager.generate_qr_image(data, 250)
            from PIL import ImageTk
            tk_img = ImageTk.PhotoImage(img)

            qr_win = tk.Toplevel(self.root)
            qr_win.title("QR-code")
            qr_win.geometry("350x450")
            qr_win.configure(bg="white")

            tk.Label(qr_win, text="Scan QR-code", font=("Arial", 14, "bold"), bg="white").pack(pady=15)
            lbl = tk.Label(qr_win, image=tk_img, bg="white")
            lbl.image = tk_img
            lbl.pack()

            info = json.loads(data)
            tk.Label(qr_win, text=f"IP: {info['ip']}\nPort: {info['port']}",
                    font=("Consolas", 11), bg="#f5f5f5", fg="#333").pack(pady=10)

            tk.Label(qr_win, text="1. Open app on Android\n2. Press Scan QR\n3. Point camera at code",
                    font=("Arial", 10), bg="white", fg="#888").pack()

            tk.Button(qr_win, text="Close", font=("Arial", 11), bg="#4CAF50", fg="white",
                     relief="flat", padx=20, pady=6, command=qr_win.destroy).pack(pady=15)
        except Exception as e:
            messagebox.showerror("QR Error", str(e))

    def run(self):
        self.root.mainloop()

def main():
    app = FileDropApp()
    app.run()

if __name__ == "__main__":
    main()
