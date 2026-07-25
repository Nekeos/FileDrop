import sys
import asyncio
import os
import json
import webbrowser

from PySide6.QtCore import Qt, QObject, Signal, QSize

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog,
    QProgressBar, QListWidget, QMessageBox, QFrame
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

SAVE_DIR = os.path.join(APP_DIR, "received_files")
ICONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

# Links (replace with real ones later)
RUSTORE_URL = "https://www.rustore.ru/catalog/developer/ch7shq"
GITHUB_URL = "https://github.com/Nekeos/FileDrop"
TELEGRAM_URL = "https://t.me/Axkuon"

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
        self.setWindowTitle("FileDrop Desktop")
        self.setMinimumSize(800, 550)
        self.setStyleSheet("""
            QMainWindow { background-color: #fafafa; }
            QTabWidget::pane { border: 1px solid #ddd; border-radius: 8px; background: white; }
            QTabBar::tab { padding: 10px 20px; font-size: 13px; }
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #4CAF50; }
        """)

        self.port = 45000
        self.save_dir = SAVE_DIR
        os.makedirs(self.save_dir, exist_ok=True)

        self.server = FileTransferServer(save_dir=self.save_dir, port=self.port)
        self.server_signals = ServerSignals()
        self.server_signals.status_update.connect(self.on_server_status)
        self.server_signals.file_received.connect(self.on_file_received)

        self.client_signals = ClientSignals()
        self.client_signals.progress_update.connect(self.on_progress_update)
        self.client_signals.status_update.connect(self.on_client_status)
        self.client_signals.transfer_complete.connect(self.on_transfer_complete)

        self.init_ui()
        self.received_files = []

        asyncio.ensure_future(self.start_server())

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Left panel
        left_panel = QVBoxLayout()
        left_panel.setSpacing(10)

        # Status
        self.status_label = QLabel("Starting server...")
        self.status_label.setFont(QFont("Arial", 11))
        left_panel.addWidget(self.status_label)

        # Tabs
        self.tabs = QTabWidget()

        # Send tab
        send_tab = QWidget()
        send_layout = QVBoxLayout(send_tab)
        send_layout.setSpacing(12)

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("Device IP:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("For example: 192.168.1.5")
        self.ip_input.setMinimumHeight(32)
        ip_layout.addWidget(self.ip_input)
        send_layout.addLayout(ip_layout)

        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setStyleSheet("color: #888; border: 1px dashed #ccc; padding: 8px; border-radius: 4px;")
        file_layout.addWidget(self.file_path_label)

        browse_btn = QPushButton("Browse")
        browse_btn.setStyleSheet(self._btn_style("#FF9800", "#F57C00"))
        browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_btn)
        send_layout.addLayout(file_layout)

        self.send_btn = QPushButton("Send")
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
        self.tabs.addTab(send_tab, "Send")

        # Receive tab
        recv_tab = QWidget()
        recv_layout = QVBoxLayout(recv_tab)
        recv_layout.setSpacing(12)

        recv_title = QLabel("Received files")
        recv_title.setFont(QFont("Arial", 13, QFont.Bold))
        recv_layout.addWidget(recv_title)

        self.received_list = QListWidget()
        self.received_list.setStyleSheet("font-size: 13px;")
        recv_layout.addWidget(self.received_list)

        open_folder_btn = QPushButton("Open folder")
        open_folder_btn.setStyleSheet(self._btn_style("#607D8B", "#455A64"))
        open_folder_btn.clicked.connect(self.open_received_folder)
        recv_layout.addWidget(open_folder_btn)

        self.tabs.addTab(recv_tab, "Receive")

        left_panel.addWidget(self.tabs)

        # Footer
        footer = QLabel("FileDrop Desktop v1.0 | TCP port: 45000")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #aaa; font-size: 10px;")
        left_panel.addWidget(footer)

        # Social links with icons
        links_layout = QHBoxLayout()
        links_layout.setSpacing(8)

        rustore_btn = QPushButton()
        rustore_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "rustore.png")))
        rustore_btn.setIconSize(QSize(64, 64))
        rustore_btn.setToolTip("RuStore")
        rustore_btn.setStyleSheet(self._icon_btn_style())
        rustore_btn.clicked.connect(lambda: webbrowser.open(RUSTORE_URL))
        links_layout.addWidget(rustore_btn)

        github_btn = QPushButton()
        github_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "github.png")))
        github_btn.setIconSize(QSize(64, 64))
        github_btn.setToolTip("GitHub")
        github_btn.setStyleSheet(self._icon_btn_style())
        github_btn.clicked.connect(lambda: webbrowser.open(GITHUB_URL))
        links_layout.addWidget(github_btn)

        telegram_btn = QPushButton()
        telegram_btn.setIcon(QIcon(os.path.join(ICONS_DIR, "telegram.png")))
        telegram_btn.setIconSize(QSize(64, 64))
        telegram_btn.setToolTip("Telegram")
        telegram_btn.setStyleSheet(self._icon_btn_style())
        telegram_btn.clicked.connect(lambda: webbrowser.open(TELEGRAM_URL))
        links_layout.addWidget(telegram_btn)

        links_layout.addStretch()
        left_panel.addLayout(links_layout)

        main_layout.addLayout(left_panel, stretch=3)

        # Right panel - QR code
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: white; border-radius: 12px; padding: 15px;")
        right_panel.setMinimumWidth(280)
        right_panel.setMaximumWidth(300)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(12)

        qr_title = QLabel("Scan QR-code")
        qr_title.setAlignment(Qt.AlignCenter)
        qr_title.setFont(QFont("Arial", 14, QFont.Bold))
        right_layout.addWidget(qr_title)

        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setMinimumSize(260, 260)
        self.qr_label.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 10px; padding: 5px;")
        right_layout.addWidget(self.qr_label)

        self.qr_ip_label = QLabel("IP: --")
        self.qr_ip_label.setFont(QFont("Consolas", 11))
        self.qr_ip_label.setAlignment(Qt.AlignCenter)
        self.qr_ip_label.setStyleSheet("color: #555;")
        right_layout.addWidget(self.qr_ip_label)

        self.qr_port_label = QLabel("Port: --")
        self.qr_port_label.setFont(QFont("Consolas", 11))
        self.qr_port_label.setAlignment(Qt.AlignCenter)
        self.qr_port_label.setStyleSheet("color: #555;")
        right_layout.addWidget(self.qr_port_label)

        hint = QLabel("1. Open app on Android\n2. Press Scan QR\n3. Point camera at code")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #aaa; font-size: 11px;")
        right_layout.addWidget(hint)

        right_layout.addStretch()

        refresh_qr_btn = QPushButton("Refresh QR")
        refresh_qr_btn.setStyleSheet(self._btn_style("#2196F3", "#1976D2"))
        refresh_qr_btn.clicked.connect(self.refresh_qr)
        right_layout.addWidget(refresh_qr_btn)

        main_layout.addWidget(right_panel)

        self.refresh_qr()

    def _btn_style(self, bg, hover_bg):
        return f"""
            QPushButton {{
                background-color: {bg}; color: white; padding: 10px 18px;
                border-radius: 6px; font-size: 13px; font-weight: bold; border: none;
            }}
            QPushButton:hover {{ background-color: {hover_bg}; }}
            QPushButton:pressed {{ background-color: {bg}; }}
        """

    def _icon_btn_style(self):
        return """
            QPushButton {
                background-color: #e8e8e8; padding: 8px;
                border-radius: 6px; border: none;
                min-width: 40px; min-height: 40px;
            }
            QPushButton:hover { background-color: #ddd; }
        """

    def refresh_qr(self):
        data = QRCodeManager.generate_connection_data(self.port)
        pixmap = QRCodeManager.generate_qr_pixmap(data, 240)
        self.qr_label.setPixmap(pixmap)

        info = json.loads(data)
        self.qr_ip_label.setText(f"IP: {info['ip']}")
        self.qr_port_label.setText(f"Port: {info['port']}")

    async def start_server(self):
        await self.server.start()
        self.server_signals.status_update.emit("Server running (port 45000)")

    def on_server_status(self, text):
        self.status_label.setText(text)
        self.status_label.setStyleSheet("color: green; font-weight: bold;")

    def on_file_received(self, filename):
        self.received_files.append(filename)
        self.received_list.addItem(f"File: {filename}")

    def browse_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select file")
        if filepath:
            self.selected_file = filepath
            self.file_path_label.setText(os.path.basename(filepath))
            self.file_path_label.setStyleSheet("color: #333; border: 1px solid #4CAF50; padding: 8px; border-radius: 4px;")

    def send_file(self):
        if not hasattr(self, 'selected_file'):
            QMessageBox.warning(self, "No file", "Please select a file to send.")
            return

        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "No IP", "Enter device IP address.")
            return

        self.send_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.send_status.setText("Connecting...")

        asyncio.ensure_future(self._do_send_file(ip))

    async def _do_send_file(self, ip):
        client = FileTransferClient(ip, self.port)
        try:
            self.client_signals.status_update.emit("Checking connection...")

            if not await client.ping():
                self.client_signals.transfer_complete.emit(False, "Device unreachable.")
                return

            self.client_signals.status_update.emit("Sending file...")

            await client.send_file(
                self.selected_file,
                progress_callback=lambda sent, total: self.client_signals.progress_update.emit(sent, total)
            )

            self.client_signals.transfer_complete.emit(True, "File sent successfully!")

        except Exception as e:
            self.client_signals.transfer_complete.emit(False, f"Error: {str(e)}")

    def on_progress_update(self, sent, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(sent)
        percent = (sent / total) * 100
        self.send_status.setText(f"Sent: {sent // 1024} / {total // 1024} KB ({percent:.1f}%)")

    def on_client_status(self, text):
        self.send_status.setText(text)

    def on_transfer_complete(self, success, message):
        self.send_btn.setEnabled(True)
        if success:
            self.progress_bar.setValue(self.progress_bar.maximum())
            self.send_status.setStyleSheet("color: green; font-weight: bold;")
            QMessageBox.information(self, "Success", message)
        else:
            self.send_status.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.critical(self, "Error", message)
        self.send_status.setText(message)

    def open_received_folder(self):
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