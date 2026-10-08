# ============ Easter Egg Themes ============

LIGHT_STYLE = """
QMainWindow { background-color: #FAFAFA; font-family: 'Inter', 'Segoe UI', sans-serif; }
QStackedWidget { background-color: #FAFAFA; font-family: 'Inter', 'Segoe UI', sans-serif; }
QLabel { color: #000000; background: transparent; }
#sidebar { background-color: #FFFFFF; border-right: 1px solid #E5E5EA; }
#logo { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 18px; font-weight: bold; color: #000000; padding: 20px; background: transparent; }
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
#page_title { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 22px; font-weight: bold; color: #000000; background: transparent; }
#subtitle { font-size: 13px; color: #8E8E93; background: transparent; }
QLineEdit {
    background-color: #FFFFFF; color: #000000; border: 1px solid #E5E5EA;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #2563EB; }
QComboBox {
    background-color: #FFFFFF; color: #000000; border: 1px solid #E5E5EA;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #2563EB; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #000000;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF; color: #000000;
    selection-background-color: #2563EB; selection-color: #FFFFFF;
    border: 1px solid #E5E5EA; padding: 4px;
}
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
    border-radius: 8px; font-size: 13px; border: none;
    text-align: left; min-width: 120px;
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
QListWidget { background-color: transparent; border: none; color: #000000; font-size: 13px; }
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
QMainWindow { background-color: #0F0F0F; font-family: 'Inter', 'Segoe UI', sans-serif; }
QStackedWidget { background-color: #0F0F0F; font-family: 'Inter', 'Segoe UI', sans-serif; }
QLabel { color: #FFFFFF; background: transparent; }
#sidebar { background-color: #1C1C1E; border-right: 1px solid #2C2C2E; }
#logo { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 18px; font-weight: bold; color: #FFFFFF; padding: 20px; background: transparent; }
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
#page_title { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 22px; font-weight: bold; color: #FFFFFF; background: transparent; }
#subtitle { font-size: 13px; color: #8E8E93; background: transparent; }
QLineEdit {
    background-color: #2C2C2E; color: #FFFFFF; border: 1px solid #3A3A3C;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #3B82F6; }
QComboBox {
    background-color: #2C2C2E; color: #FFFFFF; border: 1px solid #3A3A3C;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #3B82F6; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #FFFFFF;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #2C2C2E; color: #FFFFFF;
    selection-background-color: #2563EB; selection-color: #FFFFFF;
    border: 1px solid #3A3A3C; padding: 4px;
}
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
    border-radius: 8px; font-size: 13px; border: none;
    text-align: left; min-width: 120px;
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
QListWidget { background-color: transparent; border: none; color: #FFFFFF; font-size: 13px; }
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

HALFLIFE_STYLE = """
QMainWindow { background-color: #1a1a1a; font-family: 'Consolas', 'Courier New', monospace; }
QStackedWidget { background-color: #1a1a1a; font-family: 'Consolas', 'Courier New', monospace; }
QScrollArea { background-color: #1a1a1a; border: none; }
QScrollArea > QWidget > QWidget { background-color: #1a1a1a; }
QLabel { color: #e8e4dc; background: transparent; }
#sidebar { background-color: #252220; border-right: 1px solid #ff9900; }
#logo { font-family: 'Consolas', 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #ff9900; padding: 20px; background: transparent; letter-spacing: 2px; }
#version { font-size: 11px; color: #8a8478; padding: 15px; background: transparent; }
#sidebar QPushButton {
    background-color: transparent; color: #c4beb2; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 4px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #3a342e; color: #ff9900; }
#sidebar QPushButton:checked { background-color: #ff9900; color: #1a1a1a; font-weight: bold; }
#card { background-color: #252220; border-radius: 6px; border: 1px solid #4a4438; }
#card QLabel { color: #e8e4dc; background: transparent; }
#page_title { font-family: 'Consolas', 'Courier New', monospace; font-size: 22px; font-weight: bold; color: #ff9900; background: transparent; letter-spacing: 2px; }
#subtitle { font-size: 13px; color: #8a8478; background: transparent; }
QLineEdit {
    background-color: #1a1a1a; color: #ff9900; border: 1px solid #4a4438;
    padding: 10px 14px; border-radius: 4px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #ff9900; }
QComboBox {
    background-color: #1a1a1a; color: #ff9900; border: 1px solid #4a4438;
    padding: 10px 14px; border-radius: 4px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #ff9900; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #ff9900;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #1a1a1a; color: #e8e4dc;
    selection-background-color: #ff9900; selection-color: #1a1a1a;
    border: 1px solid #4a4438; padding: 4px;
}
#primary_btn {
    background-color: #ff9900; color: #1a1a1a; padding: 12px 20px;
    border-radius: 4px; font-size: 14px; font-weight: bold; border: none;
}
#primary_btn:hover { background-color: #ffaa22; }
#primary_btn:disabled { background-color: #4a4438; color: #8a8478; }
#secondary_btn {
    background-color: #252220; color: #ff9900; padding: 10px 18px;
    border-radius: 4px; font-size: 13px; border: 1px solid #4a4438;
}
#secondary_btn:hover { border-color: #ff9900; }
#selector_btn {
    background-color: #252220; color: #ff9900; padding: 8px 16px;
    border-radius: 4px; font-size: 13px; border: 1px solid #4a4438;
    text-align: left; min-width: 120px;
}
#selector_btn:hover { border-color: #ff9900; }
#dropzone {
    background-color: #1a1a1a; border: 2px dashed #4a4438;
    border-radius: 6px; color: #8a8478; font-size: 14px;
}
#dropzone_active {
    background-color: #252220; border: 2px dashed #ff9900;
    border-radius: 6px; color: #ff9900;
}
QProgressBar {
    background-color: #252220; border: 1px solid #4a4438;
    border-radius: 4px; height: 12px; text-align: center; color: #ff9900;
}
QProgressBar::chunk { background-color: #ff9900; border-radius: 4px; }
QListWidget { background-color: transparent; border: none; color: #e8e4dc; }
QListWidget::item { padding: 10px; border-radius: 4px; color: #e8e4dc; }
QListWidget::item:hover { background-color: #3a342e; }
QListWidget::item:selected { background-color: #ff9900; color: #1a1a1a; }
QMenu {
    background-color: #252220; color: #ff9900;
    border: 1px solid #4a4438; border-radius: 4px; padding: 6px;
}
QMenu::item { padding: 8px 20px; color: #ff9900; }
QMenu::item:selected { background-color: #ff9900; color: #1a1a1a; }
#status_ok { color: #ff9900; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #8a8478; font-size: 12px; background: transparent; }
#community_btn {
    background-color: #252220; color: #ff9900; padding: 10px 18px;
    border-radius: 4px; font-size: 13px; font-weight: bold;
    border: 1px solid #4a4438; margin: 10px;
}
#community_btn:hover { border-color: #ff9900; }
#community_title { color: #ff9900; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #8a8478; font-size: 12px; background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #4a4438; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #ff9900; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

CYBERPUNK_STYLE = """
QMainWindow { background-color: #0a0a12; font-family: 'Consolas', 'Courier New', monospace; }
QStackedWidget { background-color: #0a0a12; font-family: 'Consolas', 'Courier New', monospace; }
QScrollArea { background-color: #0a0a12; border: none; }
QScrollArea > QWidget > QWidget { background-color: #0a0a12; }
QLabel { color: #d0d0e0; background: transparent; }
#sidebar { background-color: #12101a; border-right: 1px solid #2a2838; }
#logo { font-family: 'Consolas', 'Courier New', monospace; font-size: 20px; font-weight: 900; color: #fcee0a; padding: 20px; background: transparent; letter-spacing: 4px; }
#version { font-size: 11px; color: #00f0ff; padding: 15px; background: transparent; }
#sidebar QPushButton {
    background-color: transparent; color: #b0b0c0; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 4px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #1a1825; color: #fcee0a; }
#sidebar QPushButton:checked {
    background-color: #1a1825; color: #fcee0a; font-weight: bold;
    border-left: 3px solid #fcee0a;
}
#card { background-color: #12101a; border-radius: 6px; border: 1px solid #2a2838; }
#card QLabel { color: #d0d0e0; background: transparent; }
#page_title { font-family: 'Consolas', 'Courier New', monospace; font-size: 24px; font-weight: 900; color: #fcee0a; background: transparent; letter-spacing: 2px; }
#subtitle { font-size: 12px; color: #00f0ff; background: transparent; }
QLineEdit {
    background-color: #0a0a12; color: #fcee0a; border: 1px solid #2a2838;
    padding: 10px 14px; border-radius: 4px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #fcee0a; }
QComboBox {
    background-color: #0a0a12; color: #fcee0a; border: 1px solid #2a2838;
    padding: 10px 14px; border-radius: 4px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #fcee0a; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #fcee0a;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #12101a; color: #d0d0e0;
    selection-background-color: #fcee0a; selection-color: #0a0a12;
    border: 1px solid #2a2838; padding: 4px;
}
#primary_btn {
    background-color: #fcee0a; color: #0a0a12; padding: 12px 20px;
    border-radius: 4px; font-size: 14px; font-weight: 900;
    border: none; letter-spacing: 1px;
}
#primary_btn:hover { background-color: #ffe93a; }
#primary_btn:disabled { background-color: #2a2838; color: #666; }
#secondary_btn {
    background-color: #12101a; color: #fcee0a; padding: 10px 18px;
    border-radius: 4px; font-size: 13px; border: 1px solid #2a2838;
}
#secondary_btn:hover { border-color: #fcee0a; }
#selector_btn {
    background-color: #12101a; color: #fcee0a; padding: 8px 16px;
    border-radius: 4px; font-size: 13px; border: 1px solid #2a2838;
    text-align: left; min-width: 120px;
}
#selector_btn:hover { border-color: #fcee0a; }
#dropzone {
    background-color: #0a0a12; border: 2px dashed #2a2838;
    border-radius: 4px; color: #666; font-size: 14px;
}
#dropzone_active {
    background-color: #12101a; border: 2px dashed #fcee0a;
    border-radius: 4px; color: #fcee0a;
}
QProgressBar {
    background-color: #12101a; border: 1px solid #2a2838;
    border-radius: 4px; height: 12px; text-align: center; color: #fcee0a;
}
QProgressBar::chunk {
    background-color: #fcee0a;
    border-radius: 4px;
}
QListWidget { background-color: transparent; border: none; color: #d0d0e0; }
QListWidget::item { padding: 10px; border-radius: 4px; color: #d0d0e0; }
QListWidget::item:hover { background-color: #1a1825; }
QListWidget::item:selected { background-color: #fcee0a; color: #0a0a12; }
QMenu {
    background-color: #12101a; color: #fcee0a;
    border: 1px solid #2a2838; border-radius: 4px; padding: 6px;
}
QMenu::item { padding: 8px 20px; color: #fcee0a; }
QMenu::item:selected { background-color: #fcee0a; color: #0a0a12; }
#status_ok { color: #00f0ff; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #666; font-size: 12px; background: transparent; }
#community_btn {
    background-color: #12101a; color: #fcee0a; padding: 12px 18px;
    border-radius: 4px; font-size: 13px; font-weight: 900;
    border: 1px solid #2a2838; margin: 10px; letter-spacing: 1px;
}
#community_btn:hover { border-color: #fcee0a; }
#community_title { color: #fcee0a; font-size: 18px; font-weight: 900; background: transparent; }
#community_subtitle { color: #00f0ff; font-size: 12px; background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #2a2838; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #fcee0a; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

FAHRENHEIT_STYLE = """
QMainWindow { background-color: #1a0d08; font-family: 'Georgia', 'Times New Roman', serif; }
QStackedWidget { background-color: #1a0d08; font-family: 'Georgia', 'Times New Roman', serif; }
QScrollArea { background-color: #1a0d08; border: none; }
QScrollArea > QWidget > QWidget { background-color: #1a0d08; }
QLabel { color: #e8c8b0; background: transparent; }
#sidebar { background-color: #241008; border-right: 1px solid #3a1c10; }
#logo { font-family: 'Georgia', 'Times New Roman', serif; font-size: 18px; font-weight: bold; color: #ff5500; padding: 20px; background: transparent; }
#version { font-size: 11px; color: #a07860; padding: 15px; background: transparent; }
#sidebar QPushButton {
    background-color: transparent; color: #c8a080; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 6px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #341810; color: #ff5500; }
#sidebar QPushButton:checked { background-color: #ff5500; color: #1a0d08; font-weight: bold; }
#card { background-color: #241008; border-radius: 8px; border: 1px solid #3a1c10; }
#card QLabel { color: #e8c8b0; background: transparent; }
#page_title { font-family: 'Georgia', 'Times New Roman', serif; font-size: 22px; font-weight: bold; color: #ff5500; background: transparent; }
#subtitle { font-size: 13px; color: #a07860; background: transparent; }
QLineEdit {
    background-color: #1a0d08; color: #e8c8b0; border: 1px solid #3a1c10;
    padding: 10px 14px; border-radius: 6px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #ff5500; }
QComboBox {
    background-color: #1a0d08; color: #e8c8b0; border: 1px solid #3a1c10;
    padding: 10px 14px; border-radius: 6px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #ff5500; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #ff5500;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #241008; color: #e8c8b0;
    selection-background-color: #ff5500; selection-color: #ffffff;
    border: 1px solid #3a1c10; padding: 4px;
}
#primary_btn {
    background-color: #ff5500; color: #ffffff; padding: 12px 20px;
    border-radius: 6px; font-size: 14px; font-weight: bold; border: none;
}
#primary_btn:hover { background-color: #ff7733; }
#primary_btn:disabled { background-color: #3a1c10; color: #a07860; }
#secondary_btn {
    background-color: #241008; color: #e8c8b0; padding: 10px 18px;
    border-radius: 6px; font-size: 13px; border: 1px solid #3a1c10;
}
#secondary_btn:hover { border-color: #ff5500; color: #ff5500; }
#selector_btn {
    background-color: #241008; color: #e8c8b0; padding: 8px 16px;
    border-radius: 6px; font-size: 13px; border: 1px solid #3a1c10;
    text-align: left; min-width: 120px;
}
#selector_btn:hover { border-color: #ff5500; }
#dropzone {
    background-color: #1a0d08; border: 2px dashed #3a1c10;
    border-radius: 8px; color: #a07860; font-size: 14px;
}
#dropzone_active {
    background-color: #241008; border: 2px dashed #ff5500;
    border-radius: 8px; color: #ff5500;
}
QProgressBar {
    background-color: #241008; border: 1px solid #3a1c10;
    border-radius: 6px; height: 10px; text-align: center; color: #e8c8b0;
}
QProgressBar::chunk {
    background-color: #ff5500;
    border-radius: 6px;
}
QListWidget { background-color: transparent; border: none; color: #e8c8b0; }
QListWidget::item { padding: 10px; border-radius: 6px; color: #e8c8b0; }
QListWidget::item:hover { background-color: #341810; }
QListWidget::item:selected { background-color: #ff5500; color: #ffffff; }
QMenu {
    background-color: #241008; color: #e8c8b0;
    border: 1px solid #3a1c10; border-radius: 6px; padding: 6px;
}
QMenu::item { padding: 8px 20px; color: #e8c8b0; }
QMenu::item:selected { background-color: #ff5500; color: #ffffff; }
#status_ok { color: #ff5500; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #a07860; font-size: 12px; background: transparent; }
#community_btn {
    background-color: #241008; color: #ff5500; padding: 10px 18px;
    border-radius: 6px; font-size: 13px; font-weight: bold;
    border: 1px solid #3a1c10; margin: 10px;
}
#community_btn:hover { border-color: #ff5500; }
#community_title { color: #ff5500; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #a07860; font-size: 12px; background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #3a1c10; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #ff5500; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

ORWELL_STYLE = """
QMainWindow { background-color: #0d0d0d; font-family: 'Courier New', monospace; }
QStackedWidget { background-color: #0d0d0d; font-family: 'Courier New', monospace; }
QScrollArea { background-color: #0d0d0d; border: none; }
QScrollArea > QWidget > QWidget { background-color: #0d0d0d; }
QLabel { color: #8a8a8a; background: transparent; }
#sidebar { background-color: #1a1a1a; border-right: 1px solid #333333; }
#logo { font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #cccccc; padding: 20px; background: transparent; }
#version { font-size: 11px; color: #666666; padding: 15px; background: transparent; }
#sidebar QPushButton {
    background-color: transparent; color: #999999; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 4px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #222222; color: #cccccc; }
#sidebar QPushButton:checked { background-color: #333333; color: #ffffff; font-weight: bold; }
#card { background-color: #1a1a1a; border-radius: 6px; border: 1px solid #333333; }
#card QLabel { color: #8a8a8a; background: transparent; }
#page_title { font-family: 'Courier New', monospace; font-size: 22px; font-weight: bold; color: #cccccc; background: transparent; }
#subtitle { font-size: 13px; color: #666666; background: transparent; }
QLineEdit {
    background-color: #0d0d0d; color: #cccccc; border: 1px solid #333333;
    padding: 10px 14px; border-radius: 4px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #cccccc; }
QComboBox {
    background-color: #0d0d0d; color: #cccccc; border: 1px solid #333333;
    padding: 10px 14px; border-radius: 4px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #cccccc; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #cccccc;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #1a1a1a; color: #cccccc;
    selection-background-color: #555555; selection-color: #ffffff;
    border: 1px solid #333333; padding: 4px;
}
#primary_btn {
    background-color: #333333; color: #ffffff; padding: 12px 20px;
    border-radius: 4px; font-size: 14px; font-weight: bold;
    border: 1px solid #555555;
}
#primary_btn:hover { background-color: #555555; }
#primary_btn:disabled { background-color: #1a1a1a; color: #444444; }
#secondary_btn {
    background-color: #1a1a1a; color: #999999; padding: 10px 18px;
    border-radius: 4px; font-size: 13px; border: 1px solid #333333;
}
#secondary_btn:hover { border-color: #cccccc; color: #cccccc; }
#selector_btn {
    background-color: #1a1a1a; color: #999999; padding: 8px 16px;
    border-radius: 4px; font-size: 13px; border: 1px solid #333333;
    text-align: left; min-width: 120px;
}
#selector_btn:hover { border-color: #cccccc; }
#dropzone {
    background-color: #0d0d0d; border: 2px dashed #333333;
    border-radius: 6px; color: #666666; font-size: 14px;
}
#dropzone_active {
    background-color: #1a1a1a; border: 2px solid #cccccc;
    border-radius: 6px; color: #cccccc;
}
QProgressBar {
    background-color: #1a1a1a; border: 1px solid #333333;
    border-radius: 4px; height: 10px; text-align: center; color: #cccccc;
}
QProgressBar::chunk { background-color: #555555; }
QListWidget { background-color: transparent; border: none; color: #8a8a8a; }
QListWidget::item { padding: 10px; border-radius: 4px; color: #8a8a8a; }
QListWidget::item:hover { background-color: #222222; }
QListWidget::item:selected { background-color: #555555; color: #ffffff; }
QMenu {
    background-color: #1a1a1a; color: #8a8a8a;
    border: 1px solid #333333; border-radius: 4px; padding: 6px;
}
QMenu::item { padding: 8px 20px; color: #8a8a8a; }
QMenu::item:selected { background-color: #555555; color: #ffffff; }
#status_ok { color: #999999; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #555555; font-size: 12px; background: transparent; }
#community_btn {
    background-color: #1a1a1a; color: #cccccc; padding: 10px 18px;
    border-radius: 4px; font-size: 13px; font-weight: bold;
    border: 1px solid #333333; margin: 10px;
}
#community_btn:hover { border-color: #cccccc; }
#community_title { color: #cccccc; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #666666; font-size: 12px; background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { background: transparent; width: 8px; }
QScrollBar::handle:vertical { background: #333333; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #555555; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

CONSOLE_STYLE = """
QMainWindow { background-color: #0a0e0a; font-family: 'Consolas', 'Courier New', monospace; }
QStackedWidget { background-color: #0a0e0a; font-family: 'Consolas', 'Courier New', monospace; }
QLabel { color: #33ff66; background: transparent; }
#sidebar { background-color: #0d120d; border-right: 1px solid #1a3a1a; }
#logo { font-family: 'Consolas', 'Courier New', monospace; font-size: 18px; font-weight: bold; color: #33ff66; padding: 20px; background: transparent; letter-spacing: 1px; }
#version { font-size: 11px; color: #2a8a4a; padding: 15px; background: transparent; }
#sidebar QPushButton {
    background-color: transparent; color: #33ff66; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 8px; margin: 2px 10px;
    font-family: 'Consolas', 'Courier New', monospace;
}
#sidebar QPushButton:hover { background-color: #152515; }
#sidebar QPushButton:checked { background-color: #1a3a1a; color: #55ff88; font-weight: bold; }
#card { background-color: #0d120d; border-radius: 12px; border: 1px solid #1a3a1a; }
#card QLabel { color: #33ff66; background: transparent; }
#page_title { font-family: 'Consolas', 'Courier New', monospace; font-size: 22px; font-weight: bold; color: #33ff66; background: transparent; letter-spacing: 1px; }
#subtitle { font-size: 13px; color: #2a8a4a; background: transparent; }
QLineEdit {
    background-color: #0d120d; color: #33ff66; border: 1px solid #1a3a1a;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
    font-family: 'Consolas', 'Courier New', monospace;
}
QLineEdit:focus { border: 1px solid #33ff66; }
QComboBox {
    background-color: #0d120d; color: #33ff66; border: 1px solid #1a3a1a;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
    font-family: 'Consolas', 'Courier New', monospace;
}
QComboBox:hover { border: 1px solid #33ff66; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #33ff66;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #0d120d; color: #33ff66;
    selection-background-color: #1a3a1a; selection-color: #55ff88;
    border: 1px solid #1a3a1a; padding: 4px;
}
#primary_btn {
    background-color: #33ff66; color: #0a0e0a; padding: 12px 20px;
    border-radius: 8px; font-size: 14px; font-weight: bold; border: none;
    font-family: 'Consolas', 'Courier New', monospace;
}
#primary_btn:hover { background-color: #55ff88; }
#primary_btn:disabled { background-color: #1a3a1a; color: #2a8a4a; }
#secondary_btn {
    background-color: #0d120d; color: #33ff66; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; border: 1px solid #1a3a1a;
    font-family: 'Consolas', 'Courier New', monospace;
}
#secondary_btn:hover { border-color: #33ff66; background-color: #152515; }
#selector_btn {
    background-color: #0d120d; color: #33ff66; padding: 8px 16px;
    border-radius: 8px; font-size: 13px; border: 1px solid #1a3a1a;
    text-align: left; min-width: 120px;
    font-family: 'Consolas', 'Courier New', monospace;
}
#selector_btn:hover { border-color: #33ff66; }
#dropzone {
    background-color: #0d120d; border: 2px dashed #1a3a1a;
    border-radius: 12px; color: #2a8a4a; font-size: 14px;
    font-family: 'Consolas', 'Courier New', monospace;
}
#dropzone_active {
    background-color: #1a3a1a; border: 2px dashed #33ff66;
    border-radius: 12px; color: #33ff66; font-size: 14px;
}
QProgressBar {
    background-color: #0d120d; border: 1px solid #1a3a1a; border-radius: 6px;
    height: 8px; text-align: center; color: #33ff66;
}
QProgressBar::chunk { background-color: #33ff66; border-radius: 6px; }
QListWidget { background-color: transparent; border: none; color: #33ff66; font-size: 13px; }
QListWidget::item { padding: 10px; border-radius: 6px; color: #33ff66; }
QListWidget::item:hover { background-color: #152515; }
QListWidget::item:selected { background-color: #1a3a1a; color: #55ff88; }
QMenu {
    background-color: #0d120d; color: #33ff66;
    border: 1px solid #1a3a1a; border-radius: 8px; padding: 6px;
    font-family: 'Consolas', 'Courier New', monospace;
}
QMenu::item { padding: 8px 20px; border-radius: 6px; color: #33ff66; }
QMenu::item:selected { background-color: #1a3a1a; color: #55ff88; }
#status_ok { color: #33ff66; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #2a8a4a; font-size: 12px; background: transparent; }
#community_btn {
    background-color: #0d120d; color: #33ff66; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; font-weight: bold;
    border: 1px solid #1a3a1a; margin: 10px;
}
#community_btn:hover { border-color: #33ff66; background-color: #152515; }
#community_title { color: #33ff66; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #2a8a4a; font-size: 12px; background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical { background: #1a3a1a; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #2a8a4a; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
"""

AXKUON_STYLE = """
QMainWindow { background-color: #0c0c0f; font-family: 'Inter', 'Segoe UI', sans-serif; }
QStackedWidget { background-color: #0c0c0f; font-family: 'Inter', 'Segoe UI', sans-serif; }
QLabel { color: #e0e0e0; background: transparent; }
#sidebar { background-color: #0c0c0f; border-right: 1px solid #1e1e24; }
#logo { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 18px; font-weight: bold; color: #a78bfa; padding: 20px; background: transparent; letter-spacing: 1px; }
#version { font-size: 11px; color: #7c7c8a; padding: 15px; background: transparent; }
#sidebar QPushButton {
    background-color: transparent; color: #c0c0d0; text-align: left;
    padding: 12px 18px; font-size: 14px; border: none;
    border-radius: 8px; margin: 2px 10px;
}
#sidebar QPushButton:hover { background-color: #16161a; color: #c4b5fd; }
#sidebar QPushButton:checked { background-color: rgba(167, 139, 250, 0.15); color: #c4b5fd; font-weight: bold; }
#card { background-color: #16161a; border-radius: 12px; border: 1px solid #22222a; }
#card QLabel { color: #e0e0e0; background: transparent; }
#page_title { font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 22px; font-weight: bold; color: #c4b5fd; background: transparent; }
#subtitle { font-size: 13px; color: #9090a0; background: transparent; }
QLineEdit {
    background-color: #16161a; color: #e0e0e0; border: 1px solid #22222a;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QLineEdit:focus { border: 1px solid #a78bfa; }
QComboBox {
    background-color: #16161a; color: #e0e0e0; border: 1px solid #22222a;
    padding: 10px 14px; border-radius: 8px; font-size: 14px;
}
QComboBox:hover { border: 1px solid #a78bfa; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #a78bfa;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #16161a; color: #e0e0e0;
    selection-background-color: rgba(167, 139, 250, 0.25); selection-color: #c4b5fd;
    border: 1px solid #22222a; padding: 4px;
}
#primary_btn {
    background-color: #a78bfa; color: #0c0c0f; padding: 12px 20px;
    border-radius: 8px; font-size: 14px; font-weight: bold; border: none;
}
#primary_btn:hover { background-color: #c4b5fd; }
#primary_btn:disabled { background-color: rgba(167, 139, 250, 0.2); color: #7c7c8a; }
#secondary_btn {
    background-color: #16161a; color: #c4b5fd; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; border: 1px solid #22222a;
}
#secondary_btn:hover { border-color: #a78bfa; background-color: rgba(167, 139, 250, 0.08); }
#selector_btn {
    background-color: #16161a; color: #e0e0e0; padding: 8px 16px;
    border-radius: 8px; font-size: 13px; border: 1px solid #22222a;
    text-align: left; min-width: 120px;
}
#selector_btn:hover { border-color: #a78bfa; }
#dropzone {
    background-color: #16161a; border: 2px dashed #2a2a35;
    border-radius: 12px; color: #9090a0; font-size: 14px;
}
#dropzone_active {
    background-color: rgba(167, 139, 250, 0.1); border: 2px dashed #a78bfa;
    border-radius: 12px; color: #c4b5fd; font-size: 14px;
}
QProgressBar {
    background-color: #16161a; border: 1px solid #22222a; border-radius: 6px;
    height: 8px; text-align: center; color: #e0e0e0;
}
QProgressBar::chunk { background-color: #a78bfa; border-radius: 6px; }
QListWidget { background-color: transparent; border: none; color: #e0e0e0; font-size: 13px; }
QListWidget::item { padding: 10px; border-radius: 6px; color: #e0e0e0; }
QListWidget::item:hover { background-color: #1c1c22; }
QListWidget::item:selected { background-color: rgba(167, 139, 250, 0.2); color: #c4b5fd; }
QMenu {
    background-color: #16161a; color: #e0e0e0;
    border: 1px solid #22222a; border-radius: 8px; padding: 6px;
}
QMenu::item { padding: 8px 20px; border-radius: 6px; color: #e0e0e0; }
QMenu::item:selected { background-color: #a78bfa; color: #0c0c0f; }
#status_ok { color: #a78bfa; font-size: 12px; font-weight: bold; background: transparent; }
#status_bad { color: #7c7c8a; font-size: 12px; background: transparent; }
#community_btn {
    background-color: #16161a; color: #c4b5fd; padding: 10px 18px;
    border-radius: 8px; font-size: 13px; font-weight: bold;
    border: 1px solid #22222a; margin: 10px;
}
#community_btn:hover { border-color: #a78bfa; background-color: rgba(167, 139, 250, 0.1); }
#community_title { color: #c4b5fd; font-size: 17px; font-weight: bold; background: transparent; }
#community_subtitle { color: #9090a0; font-size: 12px; background: transparent; }
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 0; }
QScrollBar::handle:vertical { background: #2a2a35; border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #a78bfa; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
"""

ALL_THEMES = {
    "light": LIGHT_STYLE,
    "dark": DARK_STYLE,
    "console": CONSOLE_STYLE,        
    "axkuon": AXKUON_STYLE,          
    "halflife": HALFLIFE_STYLE,
    "cyberpunk": CYBERPUNK_STYLE,
    "fahrenheit": FAHRENHEIT_STYLE,
    "orwell": ORWELL_STYLE,
}

THEME_NAMES = {
    "light": "Light",
    "dark": "Dark",
    "console": "Console",            
    "axkuon": "AxKuon",              
    "halflife": "Half-Life",
    "cyberpunk": "Cyberpunk 2077",
    "fahrenheit": "451°F",
    "orwell": "1984",
}