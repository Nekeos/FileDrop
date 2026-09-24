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
import random
import urllib.request

GITHUB_API = "https://api.github.com/repos/Nekeos/FileDrop/releases/latest"

async def check_updates(current_version):
    try:
        req = urllib.request.Request(
            GITHUB_API,
            headers={'User-Agent': 'FileDrop'}
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        latest = data.get('tag_name', '').lstrip('v')
        html_url = data.get('html_url', '')
        if latest and latest != current_version.lstrip('v'):
            return {'available': True, 'version': latest, 'url': html_url}
    except Exception as e:
        print(f"[Update] Ошибка проверки: {e}")
    return {'available': False}

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar,
    QListWidget, QFrame, QStackedWidget, QScrollArea,
    QGraphicsDropShadowEffect, QMenu
)
from PySide6.QtCore import (
    Qt, QObject, Signal, QEvent, QPoint, QTimer,
    QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import (
    QFont, QPixmap, QIcon, QColor, QAction, QPainter,
    QBrush, QLinearGradient, QPen, QImage, QPainterPath,
    QRadialGradient
)

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
APP_VERSION = "v2.3.0"

RUSTORE_URL = "https://www.rustore.ru/catalog/app/com.myname.socketflow"
GITHUB_URL = "https://github.com/Nekeos/FileDrop/releases"
TELEGRAM_URL = "https://t.me/Axkuon"
SITE_URL = "https://www.Axkuon.ru"
VK_URL = "https://vk.ru/axkuon"
MAX_URL = "https://max.ru/channel_axkuon"


def load_translations():
    # 1. Frozen EXE — PyInstaller unpack dir
    if getattr(sys, 'frozen', False):
        candidates = [
            os.path.join(sys._MEIPASS, "translations.json"),
            os.path.join(APP_DIR, "translations.json"),
        ]
    else:
        # 2. Обычный запуск из исходников
        candidates = [
            os.path.join(APP_DIR, "translations.json"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations.json"),
        ]

    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except:
            continue

    # Fallback — все языки пустые
    return {lang: {} for lang in ["en", "ru", "de", "es", "jp", "ch", "kz"]}


LANGUAGES = load_translations()


# ============ STYLES ============

LIGHT_STYLE = """
QMainWindow { background-color: #FAFAFA; }
QStackedWidget { background-color: #FAFAFA; }

QLabel { color: #000000; background: transparent; }

#sidebar { background-color: #FFFFFF; border-right: 1px solid #E5E5EA; }
#logo { font-size: 18px; font-weight: bold; color: #000000; padding: 20px; background: transparent; }
#version { font-size: 11px; color: #8E8E93; padding: 15px; background: transparent; }

#sidebar QPushButton {
    background-color: transparent; color: #3A3A3C; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 8px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #F2F2F7; }
#sidebar QPushButton:checked { background-color: #E8EFFF; color: #2563EB; font-weight: bold; }

#card { background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E5E5EA; }
#card QLabel { color: #000000; background: transparent; }

#page_title { font-size: 22px; font-weight: bold; color: #000000; background: transparent; }
#subtitle { font-size: 13px; color: #8E8E93; background: transparent; }

QLineEdit {
    background-color: #FFFFFF; color: #000000; border: 1px solid #E5E5EA;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #2563EB; }

#primary_btn {
    background-color: #2563EB; color: white; padding: 12px 20px;
    border-radius: 8px; font-size: 14px; font-weight: bold; border: none;
}
#primary_btn:hover { background-color: #1D4ED8; }
#primary_btn:disabled { background-color: #C7C7CC; color: white; }

#secondary_btn {
    background-color: #F2F2F7; color: #000000; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; border: none;
}
#secondary_btn:hover { background-color: #E5E5EA; }

#selector_btn {
    background-color: #F2F2F7; color: #000000; padding: 8px 16px;
    border-radius: 8px; font-size: 13px; border: none; text-align: left;
    min-width: 120px;
}
#selector_btn:hover { background-color: #E5E5EA; }

#dropzone {
    background-color: #FFFFFF; border: 2px dashed #C7C7CC;
    border-radius: 12px; color: #8E8E93; font-size: 14px;
}
#dropzone_active {
    background-color: #E8EFFF; border: 2px dashed #2563EB;
    border-radius: 12px; color: #2563EB; font-size: 14px;
}

QProgressBar {
    background-color: #E5E5EA; border: none; border-radius: 6px;
    height: 8px; text-align: center; color: #000000;
}
QProgressBar::chunk { background-color: #2563EB; border-radius: 6px; }

QListWidget {
    background-color: transparent; border: none; color: #000000; font-size: 13px;
}
QListWidget::item { padding: 10px; border-radius: 6px; color: #000000; }
QListWidget::item:hover { background-color: #F2F2F7; }
QListWidget::item:selected { background-color: #E8EFFF; color: #2563EB; }

QMenu {
    background-color: #FFFFFF; color: #000000;
    border: 1px solid #E5E5EA; border-radius: 8px; padding: 6px;
}
QMenu::item { padding: 8px 20px; border-radius: 6px; color: #000000; }
QMenu::item:selected { background-color: #2563EB; color: #FFFFFF; }

#status_ok { color: #10B981; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #8E8E93; font-size: 12px; background: transparent; }

#community_btn {
    background-color: #F2F2F7; color: #2563EB; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; font-weight: bold; border: none; margin: 10px;
}
#community_btn:hover { background-color: #E8EFFF; }

#community_title { color: #000000; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #8E8E93; font-size: 12px; background: transparent; }

QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical { background: #C7C7CC; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #8E8E93; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
"""

DARK_STYLE = """
QMainWindow { background-color: #0F0F0F; }
QStackedWidget { background-color: #0F0F0F; }

QLabel { color: #FFFFFF; background: transparent; }

#sidebar { background-color: #1C1C1E; border-right: 1px solid #2C2C2E; }
#logo { font-size: 18px; font-weight: bold; color: #FFFFFF; padding: 20px; background: transparent; }
#version { font-size: 11px; color: #8E8E93; padding: 15px; background: transparent; }

#sidebar QPushButton {
    background-color: transparent; color: #C7C7CC; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 8px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #2C2C2E; }
#sidebar QPushButton:checked { background-color: #1E293B; color: #3B82F6; font-weight: bold; }

#card { background-color: #1C1C1E; border-radius: 12px; border: 1px solid #2C2C2E; }
#card QLabel { color: #FFFFFF; background: transparent; }

#page_title { font-size: 22px; font-weight: bold; color: #FFFFFF; background: transparent; }
#subtitle { font-size: 13px; color: #8E8E93; background: transparent; }

QLineEdit {
    background-color: #2C2C2E; color: #FFFFFF; border: 1px solid #3A3A3C;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #3B82F6; }

#primary_btn {
    background-color: #2563EB; color: white; padding: 12px 20px;
    border-radius: 8px; font-size: 14px; font-weight: bold; border: none;
}
#primary_btn:hover { background-color: #3B82F6; }
#primary_btn:disabled { background-color: #3A3A3C; color: #8E8E93; }

#secondary_btn {
    background-color: #2C2C2E; color: #FFFFFF; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; border: none;
}
#secondary_btn:hover { background-color: #3A3A3C; }

#selector_btn {
    background-color: #2C2C2E; color: #FFFFFF; padding: 8px 16px;
    border-radius: 8px; font-size: 13px; border: none; text-align: left;
    min-width: 120px;
}
#selector_btn:hover { background-color: #3A3A3C; }

#dropzone {
    background-color: #1C1C1E; border: 2px dashed #3A3A3C;
    border-radius: 12px; color: #8E8E93; font-size: 14px;
}
#dropzone_active {
    background-color: #1E293B; border: 2px dashed #3B82F6;
    border-radius: 12px; color: #3B82F6; font-size: 14px;
}

QProgressBar {
    background-color: #2C2C2E; border: none; border-radius: 6px;
    height: 8px; text-align: center; color: #FFFFFF;
}
QProgressBar::chunk { background-color: #2563EB; border-radius: 6px; }

QListWidget {
    background-color: transparent; border: none; color: #FFFFFF; font-size: 13px;
}
QListWidget::item { padding: 10px; border-radius: 6px; color: #FFFFFF; }
QListWidget::item:hover { background-color: #2C2C2E; }
QListWidget::item:selected { background-color: #1E293B; color: #3B82F6; }

QMenu {
    background-color: #2C2C2E; color: #FFFFFF;
    border: 1px solid #3A3A3C; border-radius: 8px; padding: 6px;
}
QMenu::item { padding: 8px 20px; border-radius: 6px; color: #FFFFFF; }
QMenu::item:selected { background-color: #2563EB; color: #FFFFFF; }

#status_ok { color: #10B981; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #8E8E93; font-size: 12px; background: transparent; }

#community_btn {
    background-color: #2C2C2E; color: #3B82F6; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; font-weight: bold; border: none; margin: 10px;
}
#community_btn:hover { background-color: #1E293B; }

#community_title { color: #FFFFFF; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #8E8E93; font-size: 12px; background: transparent; }

QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical { background: #3A3A3C; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #8E8E93; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
"""


def get_default_save_dir():
    path = os.path.join(os.path.expanduser("~"), "Downloads", "FileDrop_Download")
    os.makedirs(path, exist_ok=True)
    return path


def load_settings():
    defaults = {
        "save_dir": get_default_save_dir(),
        "language": "system",
        "theme": "light"
    }
    try:
        with open(SETTINGS_FILE, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for k, v in defaults.items():
                if k not in data:
                    data[k] = v
            try:
                os.makedirs(data["save_dir"], exist_ok=True)
            except:
                data["save_dir"] = defaults["save_dir"]
            return data
    except:
        return defaults


def save_settings(s):
    with open(SETTINGS_FILE, 'w', encoding="utf-8") as f:
        json.dump(s, f, indent=2)


def get_system_language():
    try:
        if locale.getdefaultlocale()[0].startswith("ru"):
            return "ru"
    except:
        pass
    return "en"


# ============ TOAST ============

class Toast(QFrame):
    def __init__(self, parent, text, kind="info", duration=2500):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        colors = {
            "info": ("#2563EB", "ℹ"),
            "success": ("#10B981", "✓"),
            "error": ("#EF4444", "✕"),
        }
        accent, icon = colors.get(kind, colors["info"])

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(12)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"color: {accent}; font-size: 16px; font-weight: bold; background: transparent;")
        layout.addWidget(icon_lbl)

        text_lbl = QLabel(text)
        text_lbl.setStyleSheet("color: #FFFFFF; font-size: 13px; background: transparent;")
        layout.addWidget(text_lbl)

        self.setStyleSheet(f"""
            Toast {{
                background-color: rgba(28, 28, 30, 245);
                border-radius: 10px;
                border-left: 3px solid {accent};
            }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        self.adjustSize()
        px = (parent.width() - self.width()) // 2
        py = parent.height() - self.height() - 30
        self.move(px, py)

        QTimer.singleShot(duration, self.fade_out)

    def fade_out(self):
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(300)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.finished.connect(self.deleteLater)
        anim.start()
        self._anim = anim


# ============ SELECTOR BUTTON ============

class SelectorButton(QPushButton):
    def __init__(self, options, current_value, on_change, parent=None):
        super().__init__(parent)
        self.setObjectName("selector_btn")
        self.options = options
        self.current_value = current_value
        self.on_change = on_change
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.show_menu)
        self.update_label()

    def update_label(self):
        for label, value in self.options:
            if value == self.current_value:
                self.setText(f"{label}   ▾")
                return
        self.setText("—   ▾")

    def show_menu(self):
        menu = QMenu(self)
        for label, value in self.options:
            action = QAction(label, menu)
            action.setCheckable(True)
            action.setChecked(value == self.current_value)
            action.triggered.connect(lambda checked, v=value: self.select(v))
            menu.addAction(action)
        pos = self.mapToGlobal(QPoint(0, self.height() + 4))
        menu.exec(pos)

    def select(self, value):
        if value != self.current_value:
            self.current_value = value
            self.update_label()
            self.on_change(value)


# ============ DROP ZONE ============

class DropZone(QLabel):
    file_dropped = Signal(str)

    def __init__(self, tr, parent=None):
        super().__init__(parent)
        self.tr = tr
        self.setObjectName("dropzone")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(160)
        self.setText(self.tr.get("dropzone_text", "Drop file here\nor click to browse"))
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setObjectName("dropzone_active")
            self.style().unpolish(self); self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setObjectName("dropzone")
        self.style().unpolish(self); self.style().polish(self)

    def dropEvent(self, event):
        self.setObjectName("dropzone")
        self.style().unpolish(self); self.style().polish(self)
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isfile(path):
                self.file_dropped.emit(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            path, _ = QFileDialog.getOpenFileName(self, self.tr.get("select_file", "Select file"))
            if path:
                self.file_dropped.emit(path)


# ============ GLASS CARD ============

def enhance_contrast(pixmap, factor=1.35):
    """Sharpen the blurred backdrop by boosting contrast — pseudo-sharpening."""
    img = pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
    w, h = img.width(), img.height()
    for y in range(h):
        for x in range(w):
            c = img.pixelColor(x, y)
            r = max(0, min(255, int((c.red() - 128) * factor + 128)))
            g = max(0, min(255, int((c.green() - 128) * factor + 128)))
            b = max(0, min(255, int((c.blue() - 128) * factor + 128)))
            img.setPixelColor(x, y, QColor(r, g, b, c.alpha()))
    return QPixmap.fromImage(img)


class GlassCard(QFrame):
    """Premium frosted glass — real blur + sharpened backdrop + rounded look."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = True
        self._blurred_bg = None
        self._grain = None
        self._cached_size = (0, 0)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def set_dark(self, is_dark):
        self._is_dark = is_dark
        self._blurred_bg = None
        self._grain = None
        self.update()

    def update_background(self, screenshot):
        if screenshot is None or screenshot.isNull():
            return
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return

        # Stage 1: strong downscale (blur)
        stage1 = screenshot.scaled(
            max(1, w // 10), max(1, h // 10),
            Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        # Stage 2: more blur
        stage2 = stage1.scaled(
            max(1, w // 30), max(1, h // 30),
            Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        # Upscale back
        self._blurred_bg = stage2.scaled(
            w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        self._cached_size = (w, h)
        self.update()

    def _ensure_grain(self):
        w, h = self.width(), self.height()
        if self._grain is not None and self._cached_size == (w, h):
            return
        image = QImage(w, h, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        density = (w * h) // 30
        for _ in range(density):
            x = random.randint(0, w - 1)
            y = random.randint(0, h - 1)
            alpha = random.randint(2, 7)
            c = QColor(255, 255, 255, alpha) if self._is_dark else QColor(0, 0, 0, alpha)
            image.setPixelColor(x, y, c)
        self._grain = QPixmap.fromImage(image)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        rect = self.rect().adjusted(1, 1, -1, -1)
        radius = 28

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        # 1. Blurred background
        if self._blurred_bg is not None and not self._blurred_bg.isNull():
            painter.drawPixmap(0, 0, self._blurred_bg)
        else:
            fallback = QColor(22, 22, 26) if self._is_dark else QColor(248, 248, 252)
            painter.fillRect(rect, fallback)

        # 2. Tint — differs for light/dark
        if self._is_dark:
            tint = QColor(18, 18, 24, 175)
        else:
            # Light theme: soft white veil so text stays readable
            tint = QColor(255, 255, 255, 200)
        painter.fillRect(rect, tint)

        # 3. Diagonal sheen — softer in light
        diag = QLinearGradient(rect.topLeft(), rect.bottomRight())
        if self._is_dark:
            diag.setColorAt(0.0, QColor(120, 150, 255, 35))
            diag.setColorAt(0.35, QColor(180, 180, 255, 12))
            diag.setColorAt(0.65, QColor(255, 200, 220, 10))
            diag.setColorAt(1.0, QColor(180, 140, 255, 30))
        else:
            diag.setColorAt(0.0, QColor(210, 225, 255, 60))
            diag.setColorAt(0.5, QColor(255, 255, 255, 20))
            diag.setColorAt(1.0, QColor(240, 220, 255, 50))
        painter.fillRect(rect, diag)

        # 4. Radial soft light
        radial = QRadialGradient(
            rect.left() + rect.width() * 0.3,
            rect.top() + rect.height() * 0.05,
            rect.width() * 0.8
        )
        if self._is_dark:
            radial.setColorAt(0.0, QColor(255, 255, 255, 22))
            radial.setColorAt(1.0, QColor(255, 255, 255, 0))
        else:
            radial.setColorAt(0.0, QColor(255, 255, 255, 160))
            radial.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(rect, radial)

        # 5. Grain
        self._ensure_grain()
        if self._grain:
            painter.drawPixmap(0, 0, self._grain)

        # 6. Top bloom
        bloom = QLinearGradient(0, rect.top(), 0, rect.top() + 80)
        if self._is_dark:
            bloom.setColorAt(0, QColor(255, 255, 255, 90))
            bloom.setColorAt(0.4, QColor(255, 255, 255, 25))
            bloom.setColorAt(1, QColor(255, 255, 255, 0))
        else:
            bloom.setColorAt(0, QColor(255, 255, 255, 255))
            bloom.setColorAt(0.4, QColor(255, 255, 255, 180))
            bloom.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillRect(rect.left(), rect.top(), rect.width(), 80, bloom)

        # 7. Bottom shadow
        bot = QLinearGradient(0, rect.bottom() - 90, 0, rect.bottom())
        bot.setColorAt(0, QColor(0, 0, 0, 0))
        bot.setColorAt(1, QColor(0, 0, 0, 80 if self._is_dark else 30))
        painter.fillRect(rect.left(), rect.bottom() - 90, rect.width(), 90, bot)

        painter.end()

        # 8. Border
        painter2 = QPainter(self)
        painter2.setRenderHint(QPainter.Antialiasing)
        painter2.setBrush(Qt.NoBrush)

        if self._is_dark:
            border = QColor(255, 255, 255, 60)
        else:
            border = QColor(0, 0, 0, 35)
        pen = QPen(border)
        pen.setWidth(1)
        painter2.setPen(pen)
        painter2.drawRoundedRect(rect, radius, radius)

        painter2.end()


# ============ COMMUNITY SHEET ============

class CommunitySheet(QFrame):
    def __init__(self, tr, parent=None):
        super().__init__(parent)
        self.tr = tr
        self.setObjectName("community_sheet")
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedHeight(560)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(0)

        self.glass = GlassCard(self)

        shadow = QGraphicsDropShadowEffect(self.glass)
        shadow.setBlurRadius(80)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, -14)
        self.glass.setGraphicsEffect(shadow)

        outer.addWidget(self.glass)

        # Content
        layout = QVBoxLayout(self.glass)
        layout.setContentsMargins(28, 16, 28, 24)
        layout.setSpacing(10)

        # Clickable handle (closes sheet)
        handle_wrap = QHBoxLayout()
        handle_wrap.setContentsMargins(0, 0, 0, 0)
        handle_wrap.addStretch()
        self.handle = QPushButton()
        self.handle.setFixedSize(52, 16)
        self.handle.setCursor(Qt.PointingHandCursor)
        self.handle.setToolTip(self.tr.get("close", "Close"))
        self.handle.setStyleSheet("""
            QPushButton { background: transparent; border: none; }
            QPushButton:hover QFrame { background-color: rgba(180, 180, 185, 230); }
        """)
        self.handle_bar = QFrame(self.handle)
        self.handle_bar.setGeometry(0, 5, 52, 5)
        self.handle_bar.setStyleSheet("background-color: rgba(142, 142, 147, 200); border-radius: 2px;")
        self.handle.clicked.connect(self.hide_with_animation)
        handle_wrap.addWidget(self.handle)
        handle_wrap.addStretch()
        layout.addLayout(handle_wrap)
        layout.addSpacing(4)

        # Title
        title_block = QVBoxLayout()
        title_block.setSpacing(2)
        title = QLabel(self.tr.get("community_title", "Axkuon Community"))
        title.setObjectName("community_title")
        title_block.addWidget(title)

        subtitle = QLabel(self.tr.get("community_subtitle", "Follow us on socials"))
        subtitle.setObjectName("community_subtitle")
        title_block.addWidget(subtitle)

        layout.addLayout(title_block)
        layout.addSpacing(10)

        # Links
        links = [
            ("🌐", self.tr.get("link_site", "Website"), SITE_URL, "#3B82F6"),
            ("✈️", "Telegram", TELEGRAM_URL, "#229ED9"),
            ("🐙", "GitHub", GITHUB_URL, "#A0A0A8"),
            ("🛍️", "RuStore", RUSTORE_URL, "#005FF9"),
            ("🅥", "VK", VK_URL, "#0077FF"),
            ("M", "MAX", MAX_URL, "#8B5CF6"),
        ]
        for icon, text, url, color in links:
            btn = QPushButton(f"  {icon}    {text}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(52)
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.06);
                    color: #FFFFFF;
                    text-align: left;
                    padding: 12px 20px;
                    border-radius: 14px;
                    font-size: 14px;
                    font-weight: 500;
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-left: 4px solid {color};
                }}
                QPushButton:hover {{
                    background-color: rgba({r}, {g}, {b}, 0.18);
                    border: 1px solid rgba({r}, {g}, {b}, 0.5);
                    border-left: 4px solid {color};
                }}
                QPushButton:pressed {{
                    background-color: rgba({r}, {g}, {b}, 0.28);
                }}
                QPushButton:disabled {{
                    color: rgba(255, 255, 255, 0.3);
                    border-left: 4px solid rgba(255, 255, 255, 0.1);
                }}
            """)
            if url != "#":
                btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
            else:
                btn.setEnabled(False)
                btn.setToolTip(self.tr.get("soon", "Soon"))
            layout.addWidget(btn)

        layout.addStretch()

        close_btn = QPushButton(self.tr.get("close", "Close"))
        close_btn.setObjectName("primary_btn")
        close_btn.setMinimumHeight(46)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.hide_with_animation)
        layout.addWidget(close_btn)

    def set_dark(self, is_dark):
        self.glass.set_dark(is_dark)
        # Switch link button text color for light theme
        for btn in self.glass.findChildren(QPushButton):
            if btn.objectName() == "" and btn.minimumHeight() == 52:
                if is_dark:
                    btn.setStyleSheet(btn.styleSheet().replace("color: #1C1C1E;", "color: #FFFFFF;"))
                else:
                    btn.setStyleSheet(btn.styleSheet().replace("color: #FFFFFF;", "color: #1C1C1E;"))

    def show_with_animation(self):
        parent = self.parent()
        target_y = parent.height() - self.height()

        self.move(self.x(), parent.height())
        self.show()
        self.raise_()
        QApplication.processEvents()

        pixmap = parent.grab()
        if not pixmap.isNull():
            sheet_rect = self.geometry()
            cropped = pixmap.copy(sheet_rect)
            self.glass.update_background(cropped)

        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(280)
        self.anim.setStartValue(QPoint(self.x(), parent.height()))
        self.anim.setEndValue(QPoint(self.x(), target_y))
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.glass and self.isVisible():
            pixmap = self.parent().grab()
            if not pixmap.isNull():
                sheet_rect = self.geometry()
                if sheet_rect.width() > 0 and sheet_rect.height() > 0:
                    cropped = pixmap.copy(sheet_rect)
                    self.glass.update_background(cropped)

    def hide_with_animation(self):
        parent = self.parent()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(220)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(QPoint(self.x(), parent.height()))
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.finished.connect(self.hide)
        self.anim.start()

    def showEvent(self, event):
        super().showEvent(event)


# ============ SIGNALS ============

class ServerSignals(QObject):
    file_received = Signal(str)


class ClientSignals(QObject):
    progress_update = Signal(int, int)
    transfer_complete = Signal(bool, str)


# ============ MAIN WINDOW ============

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.lang_code = self.settings["language"] if self.settings["language"] != "system" else get_system_language()
        self.tr = LANGUAGES.get(self.lang_code, LANGUAGES.get("en", {}))

        self.setWindowTitle("FileDrop")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icon.png")
        else:
            icon_path = os.path.join(APP_DIR, "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.save_dir = self.settings["save_dir"]
        os.makedirs(self.save_dir, exist_ok=True)

        self.server = FileTransferServer(save_dir=self.save_dir, port=PORT)
        self.server_signals = ServerSignals()
        self.server_signals.file_received.connect(self.on_file_received)
        self.server.on_file_received = lambda fn: self.server_signals.file_received.emit(fn)

        self.client_signals = ClientSignals()
        self.client_signals.progress_update.connect(self.on_progress)
        self.client_signals.transfer_complete.connect(self.on_transfer_done)

        self.selected_file = None
        self.received_files = []

        self.init_ui()
        self.apply_theme()
        asyncio.ensure_future(self.start_server())

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 0, 0, 0)
        sb.setSpacing(0)

        logo = QLabel("FileDrop")
        logo.setObjectName("logo")
        sb.addWidget(logo)
        sb.addSpacing(10)

        nav_items = [
            ("📤", self.tr.get("send", "Send"), 0),
            ("📥", self.tr.get("receive", "Receive"), 1),
            ("⚙️", self.tr.get("settings", "Settings"), 2),
        ]
        self.nav_buttons = []
        for icon, text, idx in nav_items:
            btn = QPushButton(f"{icon}   {text}")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.switch_page(i))
            sb.addWidget(btn)
            self.nav_buttons.append(btn)

        sb.addStretch()

        self.status_dot = QLabel("● " + self.tr.get("server_starting", "Starting..."))
        self.status_dot.setObjectName("status_bad")
        self.status_dot.setContentsMargins(20, 0, 20, 0)
        sb.addWidget(self.status_dot)

        version = QLabel(APP_VERSION)
        version.setObjectName("version")
        sb.addWidget(version)

        community_btn = QPushButton("✨   " + self.tr.get("community", "Community"))
        community_btn.setObjectName("community_btn")
        community_btn.setCursor(Qt.PointingHandCursor)
        community_btn.clicked.connect(self.show_community)
        sb.addWidget(community_btn)

        root.addWidget(sidebar)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._wrap_scroll(self.build_send_page()))
        self.stack.addWidget(self._wrap_scroll(self.build_receive_page()))
        self.stack.addWidget(self._wrap_scroll(self.build_settings_page()))
        root.addWidget(self.stack, stretch=1)

        self.community = CommunitySheet(self.tr, central)
        self.community.hide()

        self.nav_buttons[0].setChecked(True)

    def _wrap_scroll(self, page):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(page)
        scroll.setFrameShape(QFrame.NoFrame)
        return scroll

    def toast(self, text, kind="info", duration=2500):
        t = Toast(self.centralWidget(), text, kind, duration)
        t.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.community.isVisible():
            self._position_community()

    def _position_community(self):
        cw = self.centralWidget().width()
        ch = self.centralWidget().height()
        self.community.setFixedWidth(cw)
        self.community.move(0, ch - self.community.height())
        self.community.raise_()

    def show_community(self):
        cw = self.centralWidget().width()
        self.community.setFixedWidth(cw)
        self.community.set_dark(self.settings.get("theme") == "dark")
        self.community.show_with_animation()

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def build_send_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        title = QLabel(self.tr.get("send_file", "Send File"))
        title.setObjectName("page_title")
        layout.addWidget(title)

        sub = QLabel(self.tr.get("send_subtitle", "Drag & drop a file"))
        sub.setObjectName("subtitle")
        layout.addWidget(sub)
        layout.addSpacing(10)

        self.dropzone = DropZone(self.tr)
        self.dropzone.file_dropped.connect(self.on_file_dropped)
        layout.addWidget(self.dropzone)

        self.file_label = QLabel("")
        self.file_label.setObjectName("subtitle")
        layout.addWidget(self.file_label)

        ip_row = QHBoxLayout()
        ip_row.setSpacing(10)
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.5")
        self.ip_input.setMinimumHeight(44)
        ip_row.addWidget(self.ip_input, stretch=1)
        layout.addLayout(ip_row)

        self.send_btn = QPushButton(self.tr.get("send_btn", "Send"))
        self.send_btn.setObjectName("primary_btn")
        self.send_btn.setMinimumHeight(48)
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.send_file)
        layout.addWidget(self.send_btn)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMinimumHeight(8)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        self.progress_label = QLabel("")
        self.progress_label.setObjectName("subtitle")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)

        layout.addStretch()
        return page

    def on_file_dropped(self, path):
        self.selected_file = path
        name = os.path.basename(path)
        size = os.path.getsize(path) / 1024
        self.file_label.setText(f"📄  {name}  •  {size:.1f} {self.tr.get('kb', 'KB')}")
        self.dropzone.setText(f"📄\n\n{name}")
        self.send_btn.setEnabled(True)

    def build_receive_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        title = QLabel(self.tr.get("receive_file", "Receive File"))
        title.setObjectName("page_title")
        layout.addWidget(title)

        sub = QLabel(self.tr.get("receive_subtitle", "Server running"))
        sub.setObjectName("subtitle")
        layout.addWidget(sub)
        layout.addSpacing(10)

        status_card = QFrame()
        status_card.setObjectName("card")
        sc = QHBoxLayout(status_card)
        sc.setContentsMargins(20, 20, 20, 20)

        self.server_status = QLabel("🟢  " + self.tr.get("server_active", "Server active"))
        self.server_status.setObjectName("status_ok")
        sc.addWidget(self.server_status)
        sc.addStretch()

        self.ip_label = QLabel("")
        self.ip_label.setObjectName("subtitle")
        sc.addWidget(self.ip_label)
        layout.addWidget(status_card)

        qr_card = QFrame()
        qr_card.setObjectName("card")
        qc = QVBoxLayout(qr_card)
        qc.setContentsMargins(20, 20, 20, 20)

        qr_title = QLabel(self.tr.get("qr_for_connection", "QR-code for connection"))
        qr_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        qc.addWidget(qr_title)

        self.qr_display = QLabel()
        self.qr_display.setAlignment(Qt.AlignCenter)
        self.qr_display.setMinimumHeight(220)
        qc.addWidget(self.qr_display)

        self.qr_info = QLabel("")
        self.qr_info.setObjectName("subtitle")
        self.qr_info.setAlignment(Qt.AlignCenter)
        qc.addWidget(self.qr_info)
        layout.addWidget(qr_card)

        files_title = QLabel(self.tr.get("received_files", "Received files"))
        files_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(files_title)

        self.received_list = QListWidget()
        self.received_list.setMinimumHeight(150)
        layout.addWidget(self.received_list)

        open_btn = QPushButton("📂   " + self.tr.get("open_folder", "Open folder"))
        open_btn.setObjectName("secondary_btn")
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.clicked.connect(self.open_folder)
        layout.addWidget(open_btn)

        layout.addStretch()
        return page

    def build_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        title = QLabel(self.tr.get("settings", "Settings"))
        title.setObjectName("page_title")
        layout.addWidget(title)
        layout.addSpacing(10)

        theme_card = QFrame()
        theme_card.setObjectName("card")
        tc = QHBoxLayout(theme_card)
        tc.setContentsMargins(20, 15, 20, 15)
        lbl = QLabel("🎨   " + self.tr.get("theme", "Theme"))
        lbl.setStyleSheet("font-weight: bold;")
        tc.addWidget(lbl)
        tc.addStretch()

        theme_options = [
            (self.tr.get("theme_light", "Light"), "light"),
            (self.tr.get("theme_dark", "Dark"), "dark"),
        ]
        self.theme_selector = SelectorButton(theme_options, self.settings.get("theme", "light"), self.change_theme)
        tc.addWidget(self.theme_selector)
        layout.addWidget(theme_card)

        lang_card = QFrame()
        lang_card.setObjectName("card")
        lc = QHBoxLayout(lang_card)
        lc.setContentsMargins(20, 15, 20, 15)
        lbl = QLabel("🌐   " + self.tr.get("language", "Language"))
        lbl.setStyleSheet("font-weight: bold;")
        lc.addWidget(lbl)
        lc.addStretch()

        lang_options = [
            ("English", "en"),
            ("Русский", "ru"),
            ("Deutsch", "de"),
            ("Español", "es"),
            ("日本語", "jp"),
            ("中国人", "ch"),
            ("Қазақ", "kz"),
        ]
        self.lang_selector = SelectorButton(lang_options, self.lang_code, self.change_language)
        lc.addWidget(self.lang_selector)
        layout.addWidget(lang_card)

        folder_card = QFrame()
        folder_card.setObjectName("card")
        fc = QHBoxLayout(folder_card)
        fc.setContentsMargins(20, 15, 20, 15)
        lbl = QLabel("📁   " + self.tr.get("save_folder", "Save folder"))
        lbl.setStyleSheet("font-weight: bold;")
        fc.addWidget(lbl)
        fc.addStretch()
        self.folder_path = QLabel(os.path.basename(self.save_dir))
        self.folder_path.setObjectName("subtitle")
        self.folder_path.setToolTip(self.save_dir)
        self.folder_path.setMaximumWidth(300)
        fc.addWidget(self.folder_path)
        change_btn = QPushButton(self.tr.get("change", "Change"))
        change_btn.setObjectName("secondary_btn")
        change_btn.setCursor(Qt.PointingHandCursor)
        change_btn.clicked.connect(self.change_save_dir)
        fc.addWidget(change_btn)
        layout.addWidget(folder_card)

        about_title = QLabel(self.tr.get("about", "About"))
        about_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(about_title)

        about_card = QFrame()
        about_card.setObjectName("card")
        ac = QVBoxLayout(about_card)
        ac.setContentsMargins(20, 15, 20, 15)
        ac.addWidget(QLabel(f"FileDrop {APP_VERSION}"))
        ac.addWidget(QLabel("Axkuon.ru"))
        ac.addWidget(QLabel("Nekeos | Htoya227 & soxr.net"))
        layout.addWidget(about_card)
        layout.addStretch()
        return page

    def change_theme(self, value):
        self.settings["theme"] = value
        save_settings(self.settings)
        self.apply_theme()

    def apply_theme(self):
        if self.settings.get("theme", "light") == "dark":
            self.setStyleSheet(DARK_STYLE)
        else:
            self.setStyleSheet(LIGHT_STYLE)

    def change_language(self, value):
        self.settings["language"] = value
        save_settings(self.settings)
        self.toast(self.tr.get("restart_msg", "Restart app to apply language"), "info", 3000)

    def change_save_dir(self):
        p = QFileDialog.getExistingDirectory(self, self.tr.get("select_folder", "Select folder"))
        if p:
            self.save_dir = p
            self.folder_path.setText(os.path.basename(p))
            self.folder_path.setToolTip(p)
            self.settings["save_dir"] = p
            save_settings(self.settings)
            self.server.save_dir = p

    async def start_server(self):
        await self.server.start()
        self.status_dot.setText("● " + self.tr.get("server_running", "Server running"))
        self.status_dot.setObjectName("status_ok")
        self.status_dot.style().unpolish(self.status_dot)
        self.status_dot.style().polish(self.status_dot)

        data = QRCodeManager.generate_connection_data(PORT)
        info = json.loads(data)
        self.ip_label.setText(f"IP: {info['ip']}  •  Port: {PORT}")
        pixmap = QRCodeManager.generate_qr_pixmap(data, 220)
        self.qr_display.setPixmap(pixmap)
        self.qr_info.setText(f"{info['ip']}:{PORT}")

    def on_file_received(self, fn):
        self.received_files.append(fn)
        self.received_list.addItem(f"📄   {fn}")
        self.toast(f"📥 {fn}", "success", 3000)

    def send_file(self):
        if not self.selected_file:
            return
        ip = self.ip_input.text().strip()
        if not ip:
            self.toast(self.tr.get("enter_ip", "Enter IP address"), "error")
            return
        self.send_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.progress_label.setText(self.tr.get("connecting", "Connecting..."))
        asyncio.ensure_future(self._do_send(ip))

    async def _do_send(self, ip):
        cl = FileTransferClient(ip, PORT)
        try:
            if not await cl.ping():
                self.client_signals.transfer_complete.emit(False, self.tr.get("device_unreachable", "Device unreachable"))
                return
            await cl.send_file(
                self.selected_file,
                progress_callback=lambda s, t: self.client_signals.progress_update.emit(s, t)
            )
            self.client_signals.transfer_complete.emit(True, self.tr.get("success_sent", "File sent!"))
        except Exception as e:
            self.client_signals.transfer_complete.emit(False, str(e))

    def on_progress(self, s, t):
        self.progress.setMaximum(t)
        self.progress.setValue(s)
        pct = (s / t) * 100
        self.progress_label.setText(f"{s//1024} / {t//1024} {self.tr.get('kb', 'KB')}  •  {pct:.1f}%")

    def on_transfer_done(self, ok, msg):
        self.send_btn.setEnabled(True)
        if ok:
            self.progress.setValue(self.progress.maximum())
            self.toast(msg, "success", 3000)
        else:
            self.toast(msg, "error", 4000)
        self.progress_label.setText(msg)

    def open_folder(self):
        p = os.path.abspath(self.save_dir)
        if os.name == 'nt':
            os.startfile(p)
        else:
            subprocess.Popen(['xdg-open', p])

    def closeEvent(self, e):
        asyncio.ensure_future(self.server.stop())
        e.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    w = MainWindow()
    w.show()
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
