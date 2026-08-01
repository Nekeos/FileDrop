# Coded by Nekeos | Htoya227 for AxKuon.ru & t.me/Axkuon
# Personal links: https://github.com/Nekeos, https://t.me/Nekeos_DEV, https://x.com/Nekeos227 

# Кодил Nekeos | Htoya227 для AxKuon.ru и t.me/Axkuon
# Личные ссылки: https://github.com/Nekeos, https://t.me/Nekeos_DEV, https://x.com/Nekeos227
# Я уже устал, я хочу спать

import sys
import asyncio
import os
import json
import webbrowser
import locale
import subprocess

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,
    QProgressBar, QListWidget, QMessageBox, QFrame, QComboBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QObject, Signal
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

RUSTORE_URL = "https://www.rustore.ru/catalog/developer/ch7shq"
GITHUB_URL = "https://github.com/Nekeos/FileDrop/releases"
TELEGRAM_URL = "t.me/Axkuon"

def load_translations():
    path = os.path.join(APP_DIR, "translations.json")
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations.json")
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

LANGUAGES = load_translations()

LIGHT_STYLE = """
QMainWindow { background-color: #fafafa; }
QTabWidget::pane { border: 1px solid #ddd; border-radius: 8px; background: white; }
QTabBar::tab { padding: 10px 20px; font-size: 13px; background: #f0f0f0; }
QTabBar::tab:selected { background: white; border-bottom: 2px solid #4CAF50; }
QLabel { color: #333; }
QLineEdit { background: white; color: #333; border: 1px solid #ddd; padding: 6px; border-radius: 4px; }
QListWidget { background: white; color: #333; }
QComboBox { background: white; color: #333; }
QRadioButton { color: #333; }
QFrame { background: white; }
QProgressBar { background: #eee; border: 1px solid #ddd; border-radius: 6px; }
QProgressBar::chunk { background-color: #4CAF50; border-radius: 6px; }
"""

DARK_STYLE = """
QMainWindow { background-color: #1e1e1e; }
QTabWidget::pane { border: 1px solid #444; border-radius: 8px; background: #2d2d2d; }
QTabBar::tab { padding: 10px 20px; font-size: 13px; background: #333; color: #ccc; }
QTabBar::tab:selected { background: #2d2d2d; border-bottom: 2px solid #4CAF50; color: white; }
QLabel { color: #ccc; }
QLineEdit { background: #333; color: #ccc; border: 1px solid #555; padding: 6px; border-radius: 4px; }
QListWidget { background: #333; color: #ccc; }
QComboBox { background: #333; color: #ccc; }
QRadioButton { color: #ccc; }
QFrame { background: #2d2d2d; }
QProgressBar { background: #444; border: 1px solid #555; border-radius: 6px; }
QProgressBar::chunk { background-color: #4CAF50; border-radius: 6px; }
"""

def load_settings():
    defaults = {"save_dir": os.path.join(os.path.expanduser("~"), "Downloads", "FileDrop"), "language": "system", "qr_position": "bottom", "theme": "light"}
    try:
        with open(SETTINGS_FILE, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for k, v in defaults.items():
                if k not in data: data[k] = v
            return data
    except:
        return defaults

def save_settings(s):
    with open(SETTINGS_FILE, 'w', encoding="utf-8") as f: json.dump(s, f, indent=2)

def get_system_language():
    try:
        if locale.getdefaultlocale()[0].startswith("ru"): return "ru"
    except: pass
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
        self.tr = LANGUAGES.get(self.lang_code, LANGUAGES["en"])
        self.setWindowTitle(self.tr["title"])

        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icon.png")
        else:
            icon_path = os.path.join(APP_DIR, "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setMinimumSize(800, 550)
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
        self.init_ui()
        self.apply_theme()
        self.received_files = []
        asyncio.ensure_future(self.start_server())

    def apply_theme(self):
        if self.settings.get("theme", "light") == "dark":
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet(LIGHT_STYLE)

    def init_ui(self):
        c = QWidget(); self.setCentralWidget(c)
        ml = QVBoxLayout(c); ml.setSpacing(10); ml.setContentsMargins(15,15,15,15)
        self.status_label = QLabel(self.tr["server_starting"]); self.status_label.setFont(QFont("Arial",11)); ml.addWidget(self.status_label)
        self.tabs = QTabWidget()
        st = QWidget(); sl = QVBoxLayout(st); sl.setSpacing(12)
        ip_l = QHBoxLayout(); ip_l.addWidget(QLabel(self.tr["device_ip"]))
        self.ip_input = QLineEdit(); self.ip_input.setPlaceholderText(self.tr["ip_example"]); self.ip_input.setMinimumHeight(32); ip_l.addWidget(self.ip_input); sl.addLayout(ip_l)
        fl = QHBoxLayout()
        self.file_path_label = QLabel(self.tr["no_file"]); fl.addWidget(self.file_path_label)
        bb = QPushButton(self.tr["browse"]); bb.setStyleSheet(self._btn("#FF9800","#F57C00")); bb.clicked.connect(self.browse_file); fl.addWidget(bb); sl.addLayout(fl)
        self.send_btn = QPushButton(self.tr["send_btn"]); self.send_btn.setStyleSheet(self._btn("#4CAF50","#388E3C")); self.send_btn.clicked.connect(self.send_file); self.send_btn.setMinimumHeight(45); sl.addWidget(self.send_btn)
        self.progress_bar = QProgressBar(); self.progress_bar.setVisible(False); self.progress_bar.setMinimumHeight(25); sl.addWidget(self.progress_bar)
        self.send_status = QLabel(""); self.send_status.setAlignment(Qt.AlignCenter); sl.addWidget(self.send_status); sl.addStretch()
        self.tabs.addTab(st, self.tr["send"])
        rt = QWidget(); rl = QVBoxLayout(rt); rl.setSpacing(12)
        df = QHBoxLayout(); df.addWidget(QLabel(self.tr["save_to"]))
        self.dir_label = QLabel(self.save_dir); df.addWidget(self.dir_label, stretch=1)
        cb = QPushButton(self.tr["change"]); cb.setStyleSheet(self._btn("#2196F3","#1976D2")); cb.clicked.connect(self.change_save_dir); df.addWidget(cb); rl.addLayout(df)
        rl.addWidget(QLabel(self.tr["received_files"], font=QFont("Arial",13,QFont.Bold)))
        self.received_list = QListWidget(); rl.addWidget(self.received_list)
        ob = QPushButton(self.tr["open_folder"]); ob.setStyleSheet(self._btn("#607D8B","#455A64")); ob.clicked.connect(self.open_folder); rl.addWidget(ob)
        self.tabs.addTab(rt, self.tr["receive"])
        self.qr_tab = QWidget(); ql = QVBoxLayout(self.qr_tab); ql.setSpacing(12)
        ql.addWidget(QLabel(self.tr["scan_qr"], alignment=Qt.AlignCenter, font=QFont("Arial",14,QFont.Bold)))
        self.qr_label_tab = QLabel(alignment=Qt.AlignCenter); self.qr_label_tab.setMinimumSize(260,260); ql.addWidget(self.qr_label_tab)
        self.qr_info_label_tab = QLabel("", alignment=Qt.AlignCenter, font=QFont("Consolas",11)); ql.addWidget(self.qr_info_label_tab)
        ql.addWidget(QLabel(self.tr["qr_hint"], alignment=Qt.AlignCenter)); ql.addStretch()
        self.tabs.addTab(self.qr_tab, self.tr["qr_code"])
        set_t = QWidget(); set_l = QVBoxLayout(set_t); set_l.setSpacing(15)
        set_l.addWidget(QLabel(self.tr["settings"], font=QFont("Arial",13,QFont.Bold)))
        th_l = QHBoxLayout(); th_l.addWidget(QLabel(self.tr["theme"]))
        self.theme_combo = QComboBox(); self.theme_combo.addItem(self.tr["theme_light"], "light"); self.theme_combo.addItem(self.tr["theme_dark"], "dark")
        self.theme_combo.setCurrentIndex(0 if self.settings.get("theme","light")=="light" else 1); self.theme_combo.currentIndexChanged.connect(self.change_theme); th_l.addWidget(self.theme_combo); th_l.addStretch(); set_l.addLayout(th_l)
        lg_l = QHBoxLayout(); lg_l.addWidget(QLabel(self.tr["language"]))
        self.lang_combo = QComboBox(); self.lang_combo.addItem("English","en"); self.lang_combo.addItem("Русский","ru")
        self.lang_combo.setCurrentIndex(1 if self.lang_code=="ru" else 0); self.lang_combo.currentIndexChanged.connect(self.change_language); lg_l.addWidget(self.lang_combo); lg_l.addStretch(); set_l.addLayout(lg_l)
        qp_l = QHBoxLayout(); qp_l.addWidget(QLabel(self.tr["qr_position"]))
        self.qr_group = QButtonGroup(); self.qr_bottom_radio = QRadioButton(self.tr["qr_bottom"]); self.qr_tab_radio = QRadioButton(self.tr["qr_tab"])
        self.qr_group.addButton(self.qr_bottom_radio,1); self.qr_group.addButton(self.qr_tab_radio,3)
        (self.qr_tab_radio if self.settings["qr_position"]=="tab" else self.qr_bottom_radio).setChecked(True)
        self.qr_group.buttonClicked.connect(self.change_qr_position); qp_l.addWidget(self.qr_bottom_radio); qp_l.addWidget(self.qr_tab_radio); qp_l.addStretch(); set_l.addLayout(qp_l); set_l.addStretch()
        self.tabs.addTab(set_t, self.tr["settings"])
        ml.addWidget(self.tabs)
        ml.addWidget(QLabel(self.tr["footer"], alignment=Qt.AlignCenter))
        ll = QHBoxLayout(); ll.setSpacing(8)
        for txt,url,clr in [("RuStore",RUSTORE_URL,"#005FF9"),("GitHub",GITHUB_URL,"#24292e"),("Telegram",TELEGRAM_URL,"#0088cc")]:
            b = QPushButton(txt); b.setStyleSheet(f"background:{clr};color:white;padding:6px 14px;border-radius:4px;font-size:11px;font-weight:bold;border:none"); b.clicked.connect(lambda _,u=url: webbrowser.open(u)); ll.addWidget(b)
        ll.addStretch(); ml.addLayout(ll)
        self.qr_panel = QFrame()
        qp_l = QVBoxLayout(self.qr_panel); qp_l.setSpacing(5)
        self.qr_label_bottom = QLabel(alignment=Qt.AlignCenter); self.qr_label_bottom.setMinimumSize(150,150); self.qr_label_bottom.setMaximumSize(180,180); qp_l.addWidget(self.qr_label_bottom, alignment=Qt.AlignCenter)
        self.qr_info_label_bottom = QLabel("", alignment=Qt.AlignCenter, font=QFont("Consolas",9)); qp_l.addWidget(self.qr_info_label_bottom)
        self.qr_panel.setVisible(False); ml.addWidget(self.qr_panel)
        self.apply_qr_position()

    def _btn(self, bg, hb): return f"QPushButton{{background:{bg};color:white;padding:10px 18px;border-radius:6px;font-size:13px;font-weight:bold;border:none}} QPushButton:hover{{background:{hb}}}"

    def change_theme(self):
        self.settings["theme"] = self.theme_combo.currentData()
        save_settings(self.settings)
        self.apply_theme()

    def apply_qr_position(self):
        pos = self.settings["qr_position"]; self.qr_panel.setVisible(pos=="bottom")
        qi = -1
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) in ["QR-code","QR-код"]: qi = i; break
        if pos=="tab":
            if qi==-1: self.tabs.insertTab(2, self.qr_tab, self.tr["qr_code"])
        else:
            if qi>=0: self.tabs.removeTab(qi)
        self.refresh_qr()

    def refresh_qr(self):
        d = QRCodeManager.generate_connection_data(PORT); ps = QRCodeManager.generate_qr_pixmap(d,150); pl = QRCodeManager.generate_qr_pixmap(d,260)
        info = json.loads(d); txt = f"IP: {info['ip']}  Port: {info['port']}"
        if self.settings["qr_position"]=="bottom": self.qr_label_bottom.setPixmap(ps); self.qr_info_label_bottom.setText(txt)
        else: self.qr_label_tab.setPixmap(pl); self.qr_info_label_tab.setText(txt)

    def change_language(self):
        self.settings["language"] = self.lang_combo.currentData(); save_settings(self.settings)
        QMessageBox.information(self, self.tr["info"], self.tr["restart_msg"])

    def change_qr_position(self, btn):
        self.settings["qr_position"] = {1:"bottom",3:"tab"}[self.qr_group.id(btn)]; save_settings(self.settings); self.apply_qr_position()

    def change_save_dir(self):
        p = QFileDialog.getExistingDirectory(self, self.tr["select_folder"])
        if p: self.save_dir = p; self.dir_label.setText(p); self.settings["save_dir"] = p; save_settings(self.settings); self.server.save_dir = p; self.received_list.clear(); QMessageBox.information(self, self.tr["folder_changed"], f"{self.tr['folder_changed_msg']}\n{p}")

    async def start_server(self):
        await self.server.start(); self.server_signals.status_update.emit(self.tr["server_running"])

    def on_server_status(self, t): self.status_label.setText(t); self.status_label.setStyleSheet("color:green;font-weight:bold")

    def on_file_received(self, fn): self.received_files.append(fn); self.received_list.addItem(f"📄 {fn}")

    def browse_file(self):
        p, _ = QFileDialog.getOpenFileName(self, self.tr["select_file"])
        if p: self.selected_file = p; self.file_path_label.setText(os.path.basename(p))

    def send_file(self):
        if not hasattr(self,'selected_file'): QMessageBox.warning(self, self.tr["no_file_warn"], self.tr["no_file_msg"]); return
        ip = self.ip_input.text().strip()
        if not ip: QMessageBox.warning(self, self.tr["no_ip_warn"], self.tr["no_ip_msg"]); return
        self.send_btn.setEnabled(False); self.progress_bar.setVisible(True); self.progress_bar.setValue(0); self.send_status.setText(self.tr["connecting"]); asyncio.ensure_future(self._do_send(ip))

    async def _do_send(self, ip):
        cl = FileTransferClient(ip, PORT)
        try:
            self.client_signals.status_update.emit(self.tr["checking"])
            if not await cl.ping(): self.client_signals.transfer_complete.emit(False, self.tr["device_unreachable"]); return
            self.client_signals.status_update.emit(self.tr["sending"])
            await cl.send_file(self.selected_file, progress_callback=lambda s,t: self.client_signals.progress_update.emit(s,t))
            self.client_signals.transfer_complete.emit(True, self.tr["success_sent"])
        except Exception as e: self.client_signals.transfer_complete.emit(False, str(e))

    def on_progress_update(self, s, t):
        self.progress_bar.setMaximum(t); self.progress_bar.setValue(s)
        self.send_status.setText(f"{self.tr['sent']} {s//1024}/{t//1024} {self.tr['kb']} ({(s/t)*100:.1f}%)")

    def on_client_status(self, t): self.send_status.setText(t)

    def on_transfer_complete(self, ok, msg):
        self.send_btn.setEnabled(True)
        if ok: QMessageBox.information(self, self.tr["success"], msg)
        else: QMessageBox.critical(self, self.tr["error"], msg)
        self.send_status.setText(msg)

    def open_folder(self):
        p = os.path.abspath(self.save_dir)
        if os.name == 'nt':
            os.startfile(p)
        else:
            subprocess.Popen(['xdg-open', p])

    def closeEvent(self, e): asyncio.ensure_future(self.server.stop()); e.accept()

def main():
    app = QApplication(sys.argv); app.setStyle("Fusion")
    loop = qasync.QEventLoop(app); asyncio.set_event_loop(loop)
    w = MainWindow(); w.show()
    with loop: loop.run_forever()

if __name__=="__main__": main()
