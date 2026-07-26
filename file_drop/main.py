import sys
import asyncio
import os
import json
import webbrowser
import locale


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,
    QProgressBar, QListWidget, QMessageBox, QFrame, QComboBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QObject, Signal, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon

import qasync
from .server import FileTransferServer
from .client import FileTransferClient
from .qr_manager import QRCodeManager

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PORT = 45000
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")
ICONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

RUSTORE_URL = "https://www.rustore.ru/catalog/developer/ch7shq"
GITHUB_URL = "https://github.com/Nekeos/FileDrop/releases"
TELEGRAM_URL = "t.me/Axkuon"

# Загрузка переводов
def load_translations():
    # Пробуем найти в корне проекта
    translations_path = os.path.join(APP_DIR, "translations.json")
    
    # Если нет в корне - ищем рядом с текущим файлом
    if not os.path.exists(translations_path):
        translations_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations.json")
    
    try:
        with open(translations_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл переводов не найден: {translations_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка в JSON: {e}")
        return None

LANGUAGES = load_translations()



def load_settings():
    defaults = {
        "save_dir": os.path.join(os.path.expanduser("~"), "Downloads", "FileDrop"),
        "language": "system",
        "qr_position": "bottom"
    }
    try:
        with open(SETTINGS_FILE, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for k, v in defaults.items():
                if k not in data:
                    data[k] = v
            return data
    except:
        return defaults

def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

def get_system_language():
    try:
        lang = locale.getdefaultlocale()[0]
        if lang and lang.startswith("ru"):
            return "ru"
    except:
        pass
    return "en"

class ServerSignals(QObject):
    status_update = Signal(str)
    file_received = Signal(str)

class ClientSignals(QObject):
    progress_update = Signal(int, int)
    status_update = Signal(str)
    transfer_complete = Signal(bool, str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.lang_code = self.settings["language"] if self.settings["language"] != "system" else get_system_language()
        self.tr = LANGUAGES.get(self.lang_code, LANGUAGES.get("en", {}))

        self.setWindowTitle(self.t("title"))
        self.setMinimumSize(800, 550)
        self.setStyleSheet("""
            QMainWindow { background-color: #fafafa; }
            QTabWidget::pane { border: 1px solid #ddd; border-radius: 8px; background: white; }
            QTabBar::tab { padding: 10px 20px; font-size: 13px; }
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #4CAF50; }
        """)

        self.save_dir = self.settings["save_dir"]
        os.makedirs(self.save_dir, exist_ok=True)

        self.server = FileTransferServer(save_dir=self.save_dir, port=PORT)
        self.server.on_file_received = lambda fn: self.server_signals.file_received.emit(fn)
        self.server_signals = ServerSignals()
        self.server_signals.status_update.connect(self.on_server_status)
        self.server_signals.file_received.connect(self.on_file_received)

        self.client_signals = ClientSignals()
        self.client_signals.progress_update.connect(self.on_progress_update)
        self.client_signals.status_update.connect(self.on_client_status)
        self.client_signals.transfer_complete.connect(self.on_transfer_complete)

        self.qr_position = self.settings["qr_position"]

        self.init_ui()
        self.received_files = []
        asyncio.ensure_future(self.start_server())

    def t(self, key, default=None):
        """Безопасное получение перевода"""
        return self.tr.get(key, default if default is not None else key)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Status bar
        self.status_label = QLabel(self.t("server_starting"))
        self.status_label.setFont(QFont("Arial", 11))
        main_layout.addWidget(self.status_label)

        # Tabs
        self.tabs = QTabWidget()

        # Send tab
        self.send_tab = QWidget()
        send_layout = QVBoxLayout(self.send_tab)
        send_layout.setSpacing(12)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel(self.t("device_ip")))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(self.t("ip_example"))
        self.ip_input.setMinimumHeight(32)
        ip_layout.addWidget(self.ip_input)
        send_layout.addLayout(ip_layout)

        file_layout = QHBoxLayout()
        self.file_path_label = QLabel(self.t("no_file"))
        self.file_path_label.setStyleSheet("color: #888; border: 1px dashed #ccc; padding: 8px; border-radius: 4px;")
        file_layout.addWidget(self.file_path_label)

        browse_btn = QPushButton(self.t("browse"))
        browse_btn.setStyleSheet(self._btn_style("#FF9800", "#F57C00"))
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        send_layout.addLayout(file_layout)

        self.send_btn = QPushButton(self.t("send_btn"))
        self.send_btn.setStyleSheet(self._btn_style("#4CAF50", "#388E3C"))
        self.send_btn.clicked.connect(self.send_file)
        self.send_btn.setMinimumHeight(45)
        send_layout.addWidget(self.send_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setStyleSheet("""
            QProgressBar { border: 1px solid #ddd; border-radius: 12px; text-align: center; }
            QProgressBar::chunk { background-color: #4CAF50; border-radius: 12px; }
        """)
        send_layout.addWidget(self.progress_bar)

        self.send_status = QLabel("")
        self.send_status.setAlignment(Qt.AlignCenter)
        send_layout.addWidget(self.send_status)
        send_layout.addStretch()
        self.tabs.addTab(self.send_tab, self.t("send"))

        # Receive tab
        self.recv_tab = QWidget()
        recv_layout = QVBoxLayout(self.recv_tab)
        recv_layout.setSpacing(12)

        dir_frame = QHBoxLayout()
        dir_frame.addWidget(QLabel(self.t("save_to")))
        self.dir_label = QLabel(self.save_dir)
        self.dir_label.setStyleSheet("color: #333; border: 1px solid #ddd; padding: 6px; border-radius: 4px; background: #f9f9f9;")
        dir_frame.addWidget(self.dir_label, stretch=1)
        change_dir_btn = QPushButton(self.t("change"))
        change_dir_btn.setStyleSheet(self._btn_style("#2196F3", "#1976D2"))
        change_dir_btn.clicked.connect(self.change_save_dir)
        dir_frame.addWidget(change_dir_btn)
        recv_layout.addLayout(dir_frame)

        recv_title = QLabel(self.t("received_files"))
        recv_title.setFont(QFont("Arial", 13, QFont.Bold))
        recv_layout.addWidget(recv_title)

        self.received_list = QListWidget()
        self.received_list.setStyleSheet("font-size: 13px;")
        recv_layout.addWidget(self.received_list)

        open_folder_btn = QPushButton(self.t("open_folder"))
        open_folder_btn.setStyleSheet(self._btn_style("#607D8B", "#455A64"))
        open_folder_btn.clicked.connect(self.open_folder)
        recv_layout.addWidget(open_folder_btn)
        self.tabs.addTab(self.recv_tab, self.t("receive"))

        # QR tab (hidden by default)
        self.qr_tab = QWidget()
        qr_tab_layout = QVBoxLayout(self.qr_tab)
        qr_tab_layout.setSpacing(12)
        qr_title = QLabel(self.t("scan_qr"))
        qr_title.setAlignment(Qt.AlignCenter)
        qr_title.setFont(QFont("Arial", 14, QFont.Bold))
        qr_tab_layout.addWidget(qr_title)
        self.qr_label_tab = QLabel()
        self.qr_label_tab.setAlignment(Qt.AlignCenter)
        self.qr_label_tab.setMinimumSize(260, 260)
        self.qr_label_tab.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 10px; padding: 5px;")
        qr_tab_layout.addWidget(self.qr_label_tab)
        self.qr_info_label_tab = QLabel("")
        self.qr_info_label_tab.setAlignment(Qt.AlignCenter)
        self.qr_info_label_tab.setFont(QFont("Consolas", 11))
        qr_tab_layout.addWidget(self.qr_info_label_tab)
        qr_hint = QLabel(self.t("qr_hint"))
        qr_hint.setAlignment(Qt.AlignCenter)
        qr_hint.setStyleSheet("color: #aaa; font-size: 11px;")
        qr_tab_layout.addWidget(qr_hint)
        qr_tab_layout.addStretch()
        self.tabs.addTab(self.qr_tab, self.t("qr_code"))

        # Settings tab
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout(self.settings_tab)
        settings_layout.setSpacing(15)
        settings_title = QLabel(self.t("settings"))
        settings_title.setFont(QFont("Arial", 13, QFont.Bold))
        settings_layout.addWidget(settings_title)

        # Language
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(self.t("language")))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Русский", "ru")
        if self.lang_code == "ru":
            self.lang_combo.setCurrentIndex(1)
        else:
            self.lang_combo.setCurrentIndex(0)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        settings_layout.addLayout(lang_layout)

        # QR position
        qr_pos_layout = QHBoxLayout()
        qr_pos_layout.addWidget(QLabel(self.t("qr_position")))
        self.qr_group = QButtonGroup()
        self.qr_bottom_radio = QRadioButton(self.t("qr_bottom"))
        self.qr_tab_radio = QRadioButton(self.t("qr_tab"))
        self.qr_group.addButton(self.qr_bottom_radio, 1)
        self.qr_group.addButton(self.qr_tab_radio, 3)

        if self.qr_position == "tab":
            self.qr_tab_radio.setChecked(True)
        else:
            self.qr_bottom_radio.setChecked(True)

        self.qr_group.buttonClicked.connect(self.change_qr_position)
        qr_pos_layout.addWidget(self.qr_bottom_radio)
        qr_pos_layout.addWidget(self.qr_tab_radio)
        qr_pos_layout.addStretch()
        settings_layout.addLayout(qr_pos_layout)
        settings_layout.addStretch()
        self.tabs.addTab(self.settings_tab, self.t("settings"))

        main_layout.addWidget(self.tabs)

        # Footer
        footer = QLabel(self.t("footer"))
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #aaa; font-size: 10px;")
        main_layout.addWidget(footer)

        # Social links
        links_layout = QHBoxLayout()
        links_layout.setSpacing(8)

        for text, url, color in [("RuStore", RUSTORE_URL, "#005FF9"),
                                  ("GitHub", GITHUB_URL, "#24292e"),
                                  ("Telegram", TELEGRAM_URL, "#0088cc")]:
            btn = QPushButton(text)
            btn.setStyleSheet(f"background-color: {color}; color: white; padding: 6px 14px; border-radius: 4px; font-size: 11px; font-weight: bold; border: none;")
            btn.clicked.connect(lambda checked, u=url: webbrowser.open(u))
            links_layout.addWidget(btn)
        links_layout.addStretch()
        main_layout.addLayout(links_layout)

        # QR panel at bottom
        self.qr_panel = QFrame()
        self.qr_panel.setStyleSheet("background-color: white; border-radius: 12px; padding: 10px;")
        qr_panel_layout = QVBoxLayout(self.qr_panel)
        qr_panel_layout.setSpacing(5)

        self.qr_label_bottom = QLabel()
        self.qr_label_bottom.setAlignment(Qt.AlignCenter)
        self.qr_label_bottom.setMinimumSize(150, 150)
        self.qr_label_bottom.setMaximumSize(180, 180)
        self.qr_label_bottom.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 8px; padding: 3px;")
        qr_panel_layout.addWidget(self.qr_label_bottom, alignment=Qt.AlignCenter)

        self.qr_info_label_bottom = QLabel("")
        self.qr_info_label_bottom.setAlignment(Qt.AlignCenter)
        self.qr_info_label_bottom.setFont(QFont("Consolas", 9))
        self.qr_info_label_bottom.setStyleSheet("color: #555;")
        qr_panel_layout.addWidget(self.qr_info_label_bottom)

        self.qr_panel.setVisible(False)
        main_layout.addWidget(self.qr_panel)

        self.apply_qr_position()

    def _btn_style(self, bg, hover_bg):
        return f"""
            QPushButton {{
                background-color: {bg}; color: white; padding: 10px 18px;
                border-radius: 6px; font-size: 13px; font-weight: bold; border: none;
            }}
            QPushButton:hover {{ background-color: {hover_bg}; }}
            QPushButton:pressed {{ background-color: {bg}; }}
        """

    def apply_qr_position(self):
        pos = self.settings["qr_position"]
        self.qr_panel.setVisible(pos == "bottom")

        qr_tab_idx = -1
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) in ["QR-code", "QR-код"]:
                qr_tab_idx = i
                break

        if pos == "tab":
            if qr_tab_idx == -1:
                self.tabs.insertTab(2, self.qr_tab, self.t("qr_code"))
        else:
            if qr_tab_idx >= 0:
                self.tabs.removeTab(qr_tab_idx)

        self.refresh_qr()

    def refresh_qr(self):
        data = QRCodeManager.generate_connection_data(PORT)
        pixmap_small = QRCodeManager.generate_qr_pixmap(data, 150)
        pixmap_large = QRCodeManager.generate_qr_pixmap(data, 260)
        info = json.loads(data)
        info_text = f"IP: {info['ip']}  Port: {info['port']}"

        pos = self.settings["qr_position"]
        if pos == "bottom":
            self.qr_label_bottom.setPixmap(pixmap_small)
            self.qr_info_label_bottom.setText(info_text)
        elif pos == "tab":
            self.qr_label_tab.setPixmap(pixmap_large)
            self.qr_info_label_tab.setText(info_text)

    def change_language(self):
        new_lang = self.lang_combo.currentData()
        self.settings["language"] = new_lang
        save_settings(self.settings)
        QMessageBox.information(self, self.t("info"), self.t("restart_msg"))

    def change_qr_position(self, btn):
        pos_map = {1: "bottom", 3: "tab"}
        self.settings["qr_position"] = pos_map[self.qr_group.id(btn)]
        save_settings(self.settings)
        self.apply_qr_position()

    def change_save_dir(self):
        path = QFileDialog.getExistingDirectory(self, self.t("select_folder"))
        if path:
            self.save_dir = path
            self.dir_label.setText(path)
            self.settings["save_dir"] = path
            save_settings(self.settings)
            self.server.save_dir = path
            self.received_list.clear()
            QMessageBox.information(self, self.t("folder_changed"), f"{self.t('folder_changed_msg')}\n{path}")

    async def start_server(self):
        await self.server.start()
        self.server_signals.status_update.emit(self.t("server_running"))

    def on_server_status(self, text):
        self.status_label.setText(text)
        self.status_label.setStyleSheet("color: green; font-weight: bold;")

    def on_file_received(self, filename):
        self.received_files.append(filename)
        self.received_list.addItem(f"📄 {filename}")

    def browse_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, self.t("select_file"))
        if filepath:
            self.selected_file = filepath
            self.file_path_label.setText(os.path.basename(filepath))
            self.file_path_label.setStyleSheet("color: #333; border: 1px solid #4CAF50; padding: 8px; border-radius: 4px;")

    def send_file(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, self.t("no_file_warn"), self.t("no_file_msg"))
            return
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, self.t("no_ip_warn"), self.t("no_ip_msg"))
            return
        self.send_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.send_status.setText(self.t("connecting"))
        asyncio.ensure_future(self._do_send_file(ip))

    async def _do_send_file(self, ip):
        client = FileTransferClient(ip, PORT)
        try:
            self.client_signals.status_update.emit(self.t("checking"))
            if not await client.ping():
                self.client_signals.transfer_complete.emit(False, self.t("device_unreachable"))
                return
            self.client_signals.status_update.emit(self.t("sending"))
            await client.send_file(
                self.selected_file,
                progress_callback=lambda sent, total: self.client_signals.progress_update.emit(sent, total)
            )
            self.client_signals.transfer_complete.emit(True, self.t("success_sent"))
        except Exception as e:
            self.client_signals.transfer_complete.emit(False, f"{self.t('error')}: {e}")

    def on_progress_update(self, sent, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(sent)
        pct = (sent / total) * 100
        self.send_status.setText(f"{self.t('sent')} {sent//1024} / {total//1024} {self.t('kb')} ({pct:.1f}%)")

    def on_client_status(self, text):
        self.send_status.setText(text)

    def on_transfer_complete(self, success, message):
        self.send_btn.setEnabled(True)
        if success:
            self.progress_bar.setValue(self.progress_bar.maximum())
            self.send_status.setStyleSheet("color: green; font-weight: bold;")
            QMessageBox.information(self, self.t("success"), message)
        else:
            self.send_status.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.critical(self, self.t("error"), message)
        self.send_status.setText(message)

    def open_folder(self):
        path = os.path.abspath(self.save_dir)
        os.startfile(path) if os.name == 'nt' else os.system(f'xdg-open "{path}"')

    def closeEvent(self, event):
        asyncio.ensure_future(self.server.stop())
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main()
