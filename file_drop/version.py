"""Загрузка версии приложения из version.json."""

import json
import os
import sys


def _find_version_file():
    """Ищет version.json в нескольких местах."""
    candidates = []

    # 1. Frozen EXE — внутри PyInstaller bundle
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(sys._MEIPASS, "version.json"))

    # 2. Рядом с exe
    if getattr(sys, 'frozen', False):
        candidates.append(os.path.join(os.path.dirname(sys.executable), "version.json"))

    # 3. В корне проекта (исходники)
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)
    candidates.append(os.path.join(project_root, "version.json"))

    # 4. Рядом с этим файлом
    candidates.append(os.path.join(here, "version.json"))

    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def load_version():
    """Возвращает (version, build_date)."""
    path = _find_version_file()
    if not path:
        return "0.0.0", ""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data.get("version", "0.0.0"), data.get("build_date", "")
    except Exception as e:
        print(f"[Version] Ошибка загрузки: {e}")
        return "0.0.0", ""


VERSION, BUILD_DATE = load_version()
APP_VERSION = VERSION