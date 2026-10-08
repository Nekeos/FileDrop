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

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar,
    QListWidget, QListWidgetItem, QFrame, QStackedWidget, QScrollArea,
    QGraphicsDropShadowEffect, QMenu, QComboBox
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
from .version import APP_VERSION, BUILD_DATE
from .themes import ALL_THEMES, THEME_NAMES
from .easter_eggs import check_easter_egg, get_unlocked_themes, get_progress, EASTER_EGGS

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PORT = 45000
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")

GITHUB_API = "https://api.github.com/repos/Nekeos/FileDrop/releases/latest"

RUSTORE_URL = "https://www.rustore.ru/catalog/developer/ch7shq"
GITHUB_URL = "https://github.com/Nekeos/FileDrop/releases"
TELEGRAM_URL = "https://t.me/Axkuon"
SITE_URL = "https://www.Axkuon.ru"
VK_URL = "https://vk.ru/axkuon"
MAX_URL = "https://max.ru/channel_axkuon"


def load_translations():
    candidates = []
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(sys._MEIPASS, "translations.json"))
        candidates.append(os.path.join(APP_DIR, "translations.json"))
    else:
        candidates.append(os.path.join(APP_DIR, "translations.json"))
        candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations.json"))

    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except:
            continue
    return {"en": {}, "ru": {}}


LANGUAGES = load_translations()


def get_default_save_dir():
    path = os.path.join(os.path.expanduser("~"), "Downloads", "FileDrop_Download")
    os.makedirs(path, exist_ok=True)
    return path


def load_settings():
    defaults = {
        "save_dir": get_default_save_dir(),
        "language": "system",
        "theme": "light",
        "unlocked_themes": [],
        "saved_ips": [],
        "last_ip": "",
        "ask_save_ip": True,
        "skip_update_notifications": False
    }
    try:
        with open(SETTINGS_FILE, 'r', encoding="utf-8-sig") as f:
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
        json.dump(s, f, indent=2, ensure_ascii=False)


def get_system_language():
    try:
        lang = locale.getlocale()[0] or ""
        if lang.startswith("ru"):
            return "ru"
    except:
        pass
    for var in ("LANG", "LC_ALL", "LC_MESSAGES"):
        val = os.environ.get(var, "")
        if val.startswith("ru"):
            return "ru"
    return "en"


def check_github_update(current_version):
    try:
        req = urllib.request.Request(GITHUB_API, headers={'User-Agent': 'FileDrop'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
        tag = data.get('tag_name', '')
        # Снимаем РОВНО одну ведущую 'v'/'V', чтобы не получить 'vv2.3.0'
        latest = tag[1:] if tag[:1] in ('v', 'V') else tag
        url = data.get('html_url', '')
        current = current_version[1:] if current_version[:1] in ('v', 'V') else current_version
        if latest and latest != current:
            return latest, url
    except Exception as e:
        print(f"[Update] Ошибка проверки: {e}")
    return None, None


# ============================================
# Toast
# ============================================

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

        existing = [t for t in parent.findChildren(Toast) if t is not self]
        offset = sum(t.height() + 8 for t in existing)

        px = (parent.width() - self.width()) // 2
        py = parent.height() - self.height() - 30 - offset
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


# ============================================
# AutoGrowListWidget
# ============================================

class AutoGrowListWidget(QListWidget):
    """Список, который увеличивает высоту по мере добавления элементов."""

    def __init__(self, min_h=36, max_h=280, parent=None):
        super().__init__(parent)
        self._min_h = min_h
        self._max_h = max_h
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(min_h)
        self.model().rowsInserted.connect(self._update_height)
        self.model().rowsRemoved.connect(self._update_height)
        self.model().modelReset.connect(self._update_height)

    def _update_height(self, *args):
        count = self.count()
        if count == 0:
            self.setFixedHeight(self._min_h)
            return
        row_h = self.sizeHintForRow(0)
        if row_h <= 0:
            row_h = 26
        frame = 2 * self.frameWidth()
        target = row_h * count + frame + 6
        target = max(self._min_h, min(target, self._max_h))
        self.setFixedHeight(target)


# ============================================
# SelectorButton
# ============================================

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


# ============================================
# DropZone
# ============================================

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


# ============================================
# IP ComboBox
# ============================================

class IPComboBox(QComboBox):
    def __init__(self, saved_ips, parent=None):
        super().__init__(parent)
        self.setObjectName("ip_combo")
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setMinimumHeight(44)
        self.update_saved_ips(saved_ips)

    def update_saved_ips(self, saved_ips):
        current_text = self.currentText()
        self.clear()
        for ip in saved_ips:
            self.addItem(ip)
        self.setEditText(current_text)

    def get_ip(self):
        return self.currentText().strip()

    def set_ip(self, ip):
        self.setEditText(ip)





# ============================================
# Glass Community Sheet
# ============================================

class GlassCard(QFrame):
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
        stage1 = screenshot.scaled(max(1, w // 8), max(1, h // 8), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        stage2 = stage1.scaled(max(1, w // 20), max(1, h // 20), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self._blurred_bg = stage2.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
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

        if self._blurred_bg is not None and not self._blurred_bg.isNull():
            painter.drawPixmap(0, 0, self._blurred_bg)
        else:
            fallback = QColor(22, 22, 26) if self._is_dark else QColor(248, 248, 252)
            painter.fillRect(rect, fallback)

        if self._is_dark:
            tint = QColor(18, 18, 24, 155)
        else:
            tint = QColor(252, 252, 255, 165)
        painter.fillRect(rect, tint)

        diag = QLinearGradient(rect.topLeft(), rect.bottomRight())
        if self._is_dark:
            diag.setColorAt(0.0, QColor(120, 150, 255, 35))
            diag.setColorAt(0.35, QColor(180, 180, 255, 12))
            diag.setColorAt(0.65, QColor(255, 200, 220, 10))
            diag.setColorAt(1.0, QColor(180, 140, 255, 30))
        else:
            diag.setColorAt(0.0, QColor(220, 230, 255, 120))
            diag.setColorAt(0.5, QColor(255, 255, 255, 60))
            diag.setColorAt(1.0, QColor(255, 230, 240, 100))
        painter.fillRect(rect, diag)

        radial = QRadialGradient(
            rect.left() + rect.width() * 0.3,
            rect.top() + rect.height() * 0.05,
            rect.width() * 0.8
        )
        if self._is_dark:
            radial.setColorAt(0.0, QColor(255, 255, 255, 22))
            radial.setColorAt(1.0, QColor(255, 255, 255, 0))
        else:
            radial.setColorAt(0.0, QColor(255, 255, 255, 220))
            radial.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(rect, radial)

        self._ensure_grain()
        if self._grain:
            painter.drawPixmap(0, 0, self._grain)

        bloom = QLinearGradient(0, rect.top(), 0, rect.top() + 80)
        if self._is_dark:
            bloom.setColorAt(0, QColor(255, 255, 255, 90))
            bloom.setColorAt(0.4, QColor(255, 255, 255, 25))
            bloom.setColorAt(1, QColor(255, 255, 255, 0))
        else:
            bloom.setColorAt(0, QColor(255, 255, 255, 255))
            bloom.setColorAt(0.4, QColor(255, 255, 255, 160))
            bloom.setColorAt(1, QColor(255, 255, 255, 0))
        painter.fillRect(rect.left(), rect.top(), rect.width(), 80, bloom)

        bot = QLinearGradient(0, rect.bottom() - 90, 0, rect.bottom())
        bot.setColorAt(0, QColor(0, 0, 0, 0))
        bot.setColorAt(1, QColor(0, 0, 0, 80 if self._is_dark else 25))
        painter.fillRect(rect.left(), rect.bottom() - 90, rect.width(), 90, bot)

        painter.end()

        painter2 = QPainter(self)
        painter2.setRenderHint(QPainter.Antialiasing)
        painter2.setBrush(Qt.NoBrush)
        border = QColor(255, 255, 255, 60) if self._is_dark else QColor(0, 0, 0, 40)
        pen = QPen(border)
        pen.setWidth(1)
        painter2.setPen(pen)
        painter2.drawRoundedRect(rect, radius, radius)
        painter2.end()


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

        layout = QVBoxLayout(self.glass)
        layout.setContentsMargins(28, 16, 28, 24)
        layout.setSpacing(10)

        handle_wrap = QHBoxLayout()
        handle_wrap.setContentsMargins(0, 0, 0, 0)
        handle_wrap.addStretch()
        self.handle = QPushButton()
        self.handle.setFixedSize(52, 16)
        self.handle.setCursor(Qt.PointingHandCursor)
        self.handle.setStyleSheet("QPushButton { background: transparent; border: none; }")
        self.handle_bar = QFrame(self.handle)
        self.handle_bar.setGeometry(0, 5, 52, 5)
        self.handle_bar.setStyleSheet("background-color: rgba(142, 142, 147, 200); border-radius: 2px;")
        self.handle.clicked.connect(self.hide_with_animation)
        handle_wrap.addWidget(self.handle)
        handle_wrap.addStretch()
        layout.addLayout(handle_wrap)
        layout.addSpacing(4)

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
            """)
            if url != "#":
                btn.clicked.connect(lambda _, u=url: webbrowser.open(u))
            layout.addWidget(btn)

        layout.addSpacing(6)

        close_btn = QPushButton(self.tr.get("close", "Close"))
        close_btn.setObjectName("primary_btn")
        close_btn.setMinimumHeight(46)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.hide_with_animation)
        layout.addWidget(close_btn)

    def set_dark(self, is_dark):
        self.glass.set_dark(is_dark)

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


# ============================================
# OverlayCard — универсальное крупное уведомление
# ============================================

class OverlayCard(QFrame):
    """Крупное модальное уведомление поверх окна."""
    closed = Signal()
    action_clicked = Signal()
    dismiss_clicked = Signal()
    choice_made = Signal(str)   # <-- новое: "action" | "cancel" | "dismiss"

    def __init__(self, config, tr, parent=None):
        super().__init__(parent)
        self.tr = tr
        self.config = config
        self._action_callback = None
        self._dismiss_callback = None

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("OverlayCard { background-color: rgba(0, 0, 0, 180); }")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch()

        card = QFrame()
        card.setFixedSize(460, 440 if config.get('dismiss') else 400)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {config['bg']};
                border-radius: 20px;
                border: 2px solid {config['accent']};
            }}
            QFrame QLabel {{
                background: transparent;
            }}
        """)

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(config['accent']))
        shadow.setOffset(0, 0)
        card.setGraphicsEffect(shadow)

        cl = QVBoxLayout(card)
        cl.setContentsMargins(40, 35, 40, 30)
        cl.setSpacing(14)

        icon_lbl = QLabel(config.get('icon', '✨'))
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(
            f"color: {config['accent']}; font-size: 72px; font-weight: bold; background: transparent;"
        )
        cl.addWidget(icon_lbl)

        if config.get('label'):
            small = QLabel(config['label'].upper())
            small.setAlignment(Qt.AlignCenter)
            small.setStyleSheet(
                f"color: {config['accent']}; font-size: 11px; font-weight: bold; "
                f"letter-spacing: 4px; background: transparent;"
            )
            cl.addWidget(small)

        title = QLabel(config.get('title', ''))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            f"color: {config['accent']}; font-size: 28px; font-weight: 900; "
            f"letter-spacing: 2px; background: transparent;"
        )
        cl.addWidget(title)

        cl.addSpacing(10)

        if config.get('message'):
            quote = QLabel(f"«{config['message']}»")
            quote.setAlignment(Qt.AlignCenter)
            quote.setWordWrap(True)
            quote.setStyleSheet(
                f"color: {config['text']}; font-size: 13px; font-style: italic; background: transparent;"
            )
            cl.addWidget(quote)

        cl.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        if config.get('action'):
            apply_btn = QPushButton(config['action'])
            apply_btn.setMinimumHeight(46)
            apply_btn.setCursor(Qt.PointingHandCursor)
            apply_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config['accent']};
                    color: {config['bg']};
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 12px 20px;
                }}
            """)
            apply_btn.clicked.connect(self._on_action)
            btn_row.addWidget(apply_btn)

        if config.get('cancel'):
            later_btn = QPushButton(config['cancel'])
            later_btn.setMinimumHeight(46)
            later_btn.setCursor(Qt.PointingHandCursor)
            later_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {config['text']};
                    border: 1px solid {config['text']};
                    border-radius: 8px;
                    font-size: 14px;
                    padding: 12px 20px;
                }}
                QPushButton:hover {{
                    border-color: {config['accent']};
                    color: {config['accent']};
                }}
            """)
            later_btn.clicked.connect(self._on_cancel)
            btn_row.addWidget(later_btn)

        cl.addLayout(btn_row)

        if config.get('dismiss'):
            dismiss_btn = QPushButton(config['dismiss'])
            dismiss_btn.setMinimumHeight(38)
            dismiss_btn.setCursor(Qt.PointingHandCursor)
            dismiss_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {config['text']};
                    border: none;
                    font-size: 12px;
                    padding: 6px 12px;
                    text-decoration: underline;
                }}
                QPushButton:hover {{
                    color: {config['accent']};
                }}
            """)
            dismiss_btn.clicked.connect(self._on_dismiss)
            cl.addWidget(dismiss_btn)

        outer.addWidget(card, alignment=Qt.AlignCenter)
        outer.addStretch()

    def set_action_callback(self, cb):
        self._action_callback = cb

    def set_dismiss_callback(self, cb):
        self._dismiss_callback = cb

    def _on_action(self):
        self.choice_made.emit("action")
        self.action_clicked.emit()
        if self._action_callback:
            self._action_callback()
        self._close()

    def _on_dismiss(self):
        self.choice_made.emit("dismiss")
        self.dismiss_clicked.emit()
        if self._dismiss_callback:
            self._dismiss_callback()
        self._close()

    def _on_cancel(self):
        self.choice_made.emit("cancel")
        self._close()

    def _close(self):
        self.closed.emit()
        self.hide()
        self.deleteLater()


# ============================================
# Signals
# ============================================

class ServerSignals(QObject):
    file_received = Signal(str, int)


class ClientSignals(QObject):
    progress_update = Signal(int, int)
    transfer_complete = Signal(bool, str)


# ============================================
# MainWindow
# ============================================

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
        self.server.on_file_received = lambda fn, sz: self.server_signals.file_received.emit(fn, sz)

        self.client_signals = ClientSignals()
        self.client_signals.progress_update.connect(self.on_progress)
        self.client_signals.transfer_complete.connect(self.on_transfer_done)

        self.selected_file = None
        self.received_files = []
        self._pending_send_ip = None

        self.init_ui()
        self.apply_theme()
        asyncio.ensure_future(self.start_server())
        asyncio.ensure_future(self._check_update_async())

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
        theme = self.settings.get("theme", "light")
        self.community.set_dark(theme in ("dark", "halflife", "cyberpunk", "orwell", "console", "axkuon"))
        self.community.show_with_animation()

    def switch_page(self, index):
        if index == 2:
            old_page = self.stack.widget(2)
            self.stack.removeWidget(old_page)
            old_page.deleteLater()
            self.stack.insertWidget(2, self._wrap_scroll(self.build_settings_page()))

        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    # ============ SEND PAGE ============

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

        self.ip_input = IPComboBox(self.settings.get("saved_ips", []))
        self.ip_input.set_ip(self.settings.get("last_ip", ""))
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

    # ============ RECEIVE PAGE ============

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

        # Статус
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

        # QR
        qr_card = QFrame()
        qr_card.setObjectName("card")
        qc = QVBoxLayout(qr_card)
        qc.setContentsMargins(20, 20, 20, 20)
        qc.setSpacing(10)

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

        # Контейнер для полученных файлов — скрыт, пока файлов нет
        self.received_section = QWidget()
        rs_layout = QVBoxLayout(self.received_section)
        rs_layout.setContentsMargins(0, 0, 0, 0)
        rs_layout.setSpacing(10)

        files_header = QHBoxLayout()
        files_title = QLabel(self.tr.get("received_files", "Received files"))
        files_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        files_header.addWidget(files_title)
        files_header.addStretch()

        self.clear_files_btn = QPushButton("🗑  " + self.tr.get("clear", "Clear"))
        self.clear_files_btn.setObjectName("secondary_btn")
        self.clear_files_btn.setCursor(Qt.PointingHandCursor)
        self.clear_files_btn.clicked.connect(self.clear_received_files)
        files_header.addWidget(self.clear_files_btn)
        rs_layout.addLayout(files_header)

        self.received_list = AutoGrowListWidget(min_h=36, max_h=280)
        rs_layout.addWidget(self.received_list)

        layout.addWidget(self.received_section)
        self.received_section.setVisible(False)

        open_btn = QPushButton("📂   " + self.tr.get("open_folder", "Open folder"))
        open_btn.setObjectName("secondary_btn")
        open_btn.setCursor(Qt.PointingHandCursor)
        open_btn.setMinimumHeight(44)
        open_btn.clicked.connect(self.open_folder)
        layout.addWidget(open_btn)

        layout.addStretch()
        return page

    def clear_received_files(self):
        self.received_files.clear()
        self.received_list.clear()
        self.received_section.setVisible(False)
        self.toast(self.tr.get("cleared", "Cleared"), "success", 2000)

    # ============ SETTINGS PAGE ============

    def _build_theme_options(self):
        opts = [
            (self.tr.get("theme_light", "Light"), "light"),
            (self.tr.get("theme_dark", "Dark"), "dark"),
            (self.tr.get("theme_console", "Console"), "console"),
            (self.tr.get("theme_axkuon", "AxKuon"), "axkuon"),
        ]
        unlocked = get_unlocked_themes(SETTINGS_FILE)
        for key in ["halflife", "cyberpunk", "fahrenheit", "orwell"]:
            if key in unlocked:
                opts.append((THEME_NAMES[key], key))
        return opts

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

        theme_options = self._build_theme_options()
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

        self.build_saved_ips_card(layout)

        found, total = get_progress(SETTINGS_FILE)
        eggs_card = QFrame()
        eggs_card.setObjectName("card")
        ec = QVBoxLayout(eggs_card)
        ec.setContentsMargins(20, 15, 20, 15)

        eggs_label = QLabel(f"🏆 {self.tr.get('easter_eggs', 'Easter eggs')}: {found} / {total}")
        eggs_label.setStyleSheet("font-weight: bold;")
        ec.addWidget(eggs_label)

        if found > 0:
            unlocked = get_unlocked_themes(SETTINGS_FILE)
            names = ", ".join([THEME_NAMES.get(k, k) for k in unlocked])
            ec.addWidget(QLabel(f"{self.tr.get('unlocked', 'Unlocked')}: {names}"))
        else:
            hint = QLabel(self.tr.get("easter_eggs_hint", "Send a file with a special size or name to unlock a hidden theme"))
            hint.setObjectName("subtitle")
            hint.setWordWrap(True)
            ec.addWidget(hint)

        layout.addWidget(eggs_card)

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

    def build_saved_ips_card(self, parent_layout):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        header = QHBoxLayout()
        lbl = QLabel("🌐   " + self.tr.get("saved_ips", "Saved IPs"))
        lbl.setStyleSheet("font-weight: bold;")
        header.addWidget(lbl)
        header.addStretch()

        self.ask_ip_checkbox = QPushButton()
        self.ask_ip_checkbox.setCheckable(True)
        self.ask_ip_checkbox.setChecked(self.settings.get("ask_save_ip", True))
        self.ask_ip_checkbox.setCursor(Qt.PointingHandCursor)
        self._update_ask_ip_button()
        self.ask_ip_checkbox.clicked.connect(self.toggle_ask_save_ip)
        header.addWidget(self.ask_ip_checkbox)

        layout.addLayout(header)

        saved = self.settings.get("saved_ips", [])
        self.saved_ips_list = QListWidget()
        self.saved_ips_list.setMinimumHeight(80)
        self.saved_ips_list.setMaximumHeight(160)

        if not saved:
            item = QListWidgetItem(self.tr.get("no_saved_ips", "No saved IPs"))
            item.setFlags(Qt.NoItemFlags)
            self.saved_ips_list.addItem(item)
        else:
            for ip in saved:
                self.saved_ips_list.addItem(ip)

        layout.addWidget(self.saved_ips_list)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        delete_btn = QPushButton(self.tr.get("delete_selected", "Delete selected"))
        delete_btn.setObjectName("secondary_btn")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.clicked.connect(self.delete_selected_ip)
        btn_row.addWidget(delete_btn)

        clear_btn = QPushButton(self.tr.get("clear_all", "Clear all"))
        clear_btn.setObjectName("secondary_btn")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_all_ips)
        btn_row.addWidget(clear_btn)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        parent_layout.addWidget(card)

    def _update_ask_ip_button(self):
        if self.settings.get("ask_save_ip", True):
            self.ask_ip_checkbox.setText("✓ " + self.tr.get("ask_save_ip", "Ask on new IP"))
        else:
            self.ask_ip_checkbox.setText("✗ " + self.tr.get("ask_save_ip", "Ask on new IP"))

    def toggle_ask_save_ip(self):
        new_val = not self.settings.get("ask_save_ip", True)
        self.settings["ask_save_ip"] = new_val
        save_settings(self.settings)
        self._update_ask_ip_button()
        state = self.tr.get("enabled", "Enabled") if new_val else self.tr.get("disabled", "Disabled")
        self.toast(f"{self.tr.get('ask_save_ip', 'Ask on new IP')}: {state}", "info", 2000)

    def delete_selected_ip(self):
        item = self.saved_ips_list.currentItem()
        if not item or not (item.flags() & Qt.ItemIsSelectable):
            self.toast(self.tr.get("nothing_selected", "Nothing selected"), "error", 2000)
            return
        ip = item.text()
        saved = self.settings.get("saved_ips", [])
        if ip in saved:
            saved.remove(ip)
            self.settings["saved_ips"] = saved
            save_settings(self.settings)
            self.saved_ips_list.takeItem(self.saved_ips_list.row(item))
            self.ip_input.update_saved_ips(saved)
            self.toast(f"{self.tr.get('deleted', 'Deleted')}: {ip}", "success", 2000)

    def clear_all_ips(self):
        self.settings["saved_ips"] = []
        save_settings(self.settings)
        self.saved_ips_list.clear()
        item = QListWidgetItem(self.tr.get("no_saved_ips", "No saved IPs"))
        item.setFlags(Qt.NoItemFlags)
        self.saved_ips_list.addItem(item)
        self.ip_input.update_saved_ips([])
        self.toast(self.tr.get("cleared", "Cleared"), "success", 2000)

    # ============ ACTIONS ============

    def change_theme(self, value):
        self.settings["theme"] = value
        save_settings(self.settings)
        self.apply_theme()

    def apply_theme(self):
        theme = self.settings.get("theme", "light")
        style = ALL_THEMES.get(theme, ALL_THEMES["light"])
        self.setStyleSheet(style)

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

    async def _check_update_async(self):
        if self.settings.get("skip_update_notifications", False):
            return
        loop = asyncio.get_event_loop()
        latest, url = await loop.run_in_executor(None, check_github_update, APP_VERSION)
        if latest and url:
            self.show_update_notification(latest, url)

    def on_file_received(self, fn, size):
        self.received_files.append(fn)
        if not self.received_section.isVisible():
            self.received_section.setVisible(True)
        self.received_list.addItem(f"📄   {fn}")
        self.toast(f"📥 {fn}", "success", 3000)

        egg, updated_settings = check_easter_egg(fn, size, SETTINGS_FILE)
        if egg:
            self.settings = updated_settings
            self.show_easter_egg(egg)

    # ============ SEND ============

    def send_file(self):
        if not self.selected_file:
            return
        ip = self.ip_input.get_ip()
        if not ip:
            self.toast(self.tr.get("enter_ip", "Enter IP address"), "error")
            return

        if self.settings.get("ask_save_ip", True):
            saved = self.settings.get("saved_ips", [])
            if ip not in saved:
                self._pending_send_ip = ip
                self._show_save_ip_overlay(ip)
                return  # <-- ждём выбор пользователя
            else:
                self.settings["last_ip"] = ip
                save_settings(self.settings)
        else:
            self.settings["last_ip"] = ip
            save_settings(self.settings)

        self._start_send(ip)

    def _show_save_ip_overlay(self, ip):
        meta = self._theme_overlay_meta()
        config = {
            "icon":    "💾",
            "label":   self.tr.get("save_ip_label", "NEW IP"),
            "title":   self.tr.get("save_ip_title", "Save IP?"),
            "message": self.tr.get("save_ip_msg", "Save IP {ip} for quick access?").format(ip=ip),
            "accent":  meta["accent"],
            "bg":      meta["bg"],
            "text":    meta["text"],
            "action":  self.tr.get("save", "Save"),
            "cancel":  self.tr.get("dont_save", "Don't save"),
            "dismiss": self.tr.get("never_ask", "Don't ask again"),
        }

        overlay = OverlayCard(config, self.tr, self.centralWidget())
        overlay.setGeometry(self.centralWidget().rect())
        overlay.choice_made.connect(lambda choice: self._on_save_ip_choice(choice, ip))
        overlay.show()
        overlay.raise_()

    def _on_save_ip_choice(self, choice, ip):
        saved = self.settings.get("saved_ips", [])
        if choice == "action":  # Save
            if ip not in saved:
                saved.append(ip)
            self.settings["saved_ips"] = saved
            self.settings["last_ip"] = ip
            save_settings(self.settings)
            self.ip_input.update_saved_ips(saved)
            self.ip_input.set_ip(ip)
            self.toast(self.tr.get("ip_saved", "IP saved"), "success", 2000)
            self._start_send(ip)
        elif choice == "cancel":  # Don't save, but still send
            self.settings["last_ip"] = ip
            save_settings(self.settings)
            self._start_send(ip)
        elif choice == "dismiss":  # Never ask again + send
            self.settings["last_ip"] = ip
            self.settings["ask_save_ip"] = False
            save_settings(self.settings)
            self._update_ask_ip_button()
            self._start_send(ip)

    def _start_send(self, ip):
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

            file_name = os.path.basename(self.selected_file)
            file_size = os.path.getsize(self.selected_file)
            egg, updated_settings = check_easter_egg(file_name, file_size, SETTINGS_FILE)
            if egg:
                self.settings = updated_settings
                self.show_easter_egg(egg)

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

    # ============ OVERLAYS ============

    def _show_overlay(self, config, on_action=None, on_closed=None, on_dismiss=None):
        overlay = OverlayCard(config, self.tr, self.centralWidget())
        if on_action:
            overlay.set_action_callback(on_action)
        if on_closed:
            overlay.closed.connect(on_closed)
        if on_dismiss:
            overlay.set_dismiss_callback(on_dismiss)
        overlay.setGeometry(self.centralWidget().rect())
        overlay.show()
        overlay.raise_()
        return overlay

    def show_easter_egg(self, egg):
        theme_key = egg['theme']
        icons = {
            "halflife":   "λ",
            "cyberpunk":  "◢",
            "fahrenheit": "🔥",
            "orwell":     "👁",
        }
        # Палитра — та, что соответствует самой пасхалке (её же и открываем)
        palette = {
            "halflife":   {"accent": "#ff9900", "bg": "#1a1a1a", "text": "#e8e4dc"},
            "cyberpunk":  {"accent": "#fcee0a", "bg": "#0a0a12", "text": "#00f0ff"},
            "fahrenheit": {"accent": "#ff5500", "bg": "#1a0d08", "text": "#ffd9c0"},
            "orwell":     {"accent": "#cccccc", "bg": "#0d0d0d", "text": "#8a8a8a"},
        }.get(theme_key, {"accent": "#a78bfa", "bg": "#1a1a1a", "text": "#e0e0e0"})

        config = {
            "icon":    icons.get(theme_key, "🎉"),
            "label":   self.tr.get("theme_unlocked", "THEME UNLOCKED"),
            "title":   egg['title'],
            "message": egg['message'],
            "accent":  palette['accent'],
            "bg":      palette['bg'],
            "text":    palette['text'],
            "action":  self.tr.get("apply_theme", "Apply theme"),
            "cancel":  self.tr.get("later", "Later"),
        }

        self._show_overlay(
            config,
            on_action=lambda: self._apply_egg_theme(theme_key),
            on_closed=self._refresh_theme_options
        )

    def show_update_notification(self, latest, url):
        meta = self._theme_overlay_meta()
        config = {
            "icon":     "🚀",
            "label":    self.tr.get("update_available", "UPDATE AVAILABLE"),
            "title":    latest,
            "message":  self.tr.get("update_message", "Новая версия уже доступна. Открыть страницу релиза?"),
            "accent":   meta["accent"],
            "bg":       meta["bg"],
            "text":     meta["text"],
            "action":   self.tr.get("download", "Скачать"),
            "cancel":   self.tr.get("later", "Позже"),
            "dismiss":  self.tr.get("never_ask_update", "Больше не спрашивать"),
        }

        self._show_overlay(
            config,
            on_action=lambda: webbrowser.open(url),
            on_dismiss=self._disable_update_notifications,
        )

    def _theme_overlay_meta(self):
        """Возвращает accent/bg/text под текущую тему.
        Используется и в пасхалках, и в уведомлении об обновлении.
        """
        theme = self.settings.get("theme", "light")
        palette = {
            "light":      {"accent": "#6D4AFF", "bg": "#F5F6FA", "text": "#2A2A35"},
            "dark":       {"accent": "#7C8CFF", "bg": "#14161C", "text": "#D6D9E0"},
            "halflife":   {"accent": "#ff9900", "bg": "#1a1a1a", "text": "#e8e4dc"},
            "cyberpunk":  {"accent": "#fcee0a", "bg": "#0a0a12", "text": "#00f0ff"},
            "fahrenheit": {"accent": "#ff5500", "bg": "#1a0d08", "text": "#ffd9c0"},
            "orwell":     {"accent": "#cccccc", "bg": "#0d0d0d", "text": "#8a8a8a"},
            "console":    {"accent": "#33ff66", "bg": "#0a0e0a", "text": "#2a8a4a"},
            "axkuon":     {"accent": "#a78bfa", "bg": "#0c0c0f", "text": "#e0e0e0"},
        }
        return palette.get(theme, palette["light"])

    def _disable_update_notifications(self):
        self.settings["skip_update_notifications"] = True
        save_settings(self.settings)
        self.toast(self.tr.get("update_notifications_disabled", "Уведомления об обновлении отключены"), "info", 2500)

        self._show_overlay(config, on_action=lambda: webbrowser.open(url))

    def _refresh_theme_options(self):
        if hasattr(self, "theme_selector"):
            self.theme_selector.options = self._build_theme_options()
            self.theme_selector.update_label()

    def _apply_egg_theme(self, theme_key):
        self.settings["theme"] = theme_key
        save_settings(self.settings)
        self.apply_theme()
        self.theme_selector.current_value = theme_key
        self.theme_selector.update_label()
        self.toast(f"{self.tr.get('theme_applied', 'Theme applied')}: {THEME_NAMES.get(theme_key, theme_key)}", "success", 3000)

    # ============ UTILS ============

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
