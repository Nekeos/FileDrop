"""Пасхалки — открытие скрытых тем по имени или размеру файла."""

import json
import os
import re

KB = 1024
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB


EASTER_EGGS = {
    "halflife": {
        "sizes": [3, 3 * KB, 3 * MB, 3 * GB, 3 * TB],
        "message": "The right file in the wrong place can make all the difference...",
        "title": "Half-Life",
        "names": ["halflife", "halflife3", "hl3", "gordon", "freeman", "gordonfreeman", "lambda", "blackmesa"],
    },
    "cyberpunk": {
        "sizes": [2077 * KB, 2077 * MB],
        "message": "Wake up, samurai. We have files to burn.",
        "title": "Cyberpunk 2077",
        "names": ["cyberpunk", "cyberpunk2077", "nightcity", "samurai", "johnny", "silverhand"],
    },
    "fahrenheit": {
        "sizes": [451 * KB, 451 * MB],
        "message": "It was a pleasure to burn.",
        "title": "451°F",
        "names": ["fahrenheit", "fahrenheit451", "451", "montag", "bradbury"],
    },
    "orwell": {
        "sizes": [1984 * KB, 1984 * MB],
        "message": "Big Brother is watching you.",
        "title": "1984",
        "names": ["1984", "orwell", "bigbrother", "winston", "oceania"],
    },
}


def _normalize_name(name):
    """Приводит имя файла к нижнему регистру и убирает разделители."""
    base = os.path.splitext(os.path.basename(name))[0].lower()
    return re.sub(r"[\s\-_]+", "", base)


def _load_settings(settings_file):
    try:
        with open(settings_file, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except:
        return {}


def _save_settings(settings_file, settings):
    try:
        with open(settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[EasterEgg] Ошибка сохранения: {e}")


def _match_theme(file_name, file_size):
    """Ищет тему по имени и размеру. Приоритет — имя."""
    normalized = _normalize_name(file_name) if file_name else ""

    # 1. По имени
    if normalized:
        for theme_key, data in EASTER_EGGS.items():
            for alias in data.get("names", []):
                if _normalize_name(alias) == normalized:
                    return theme_key

    # 2. По размеру
    if file_size and file_size > 0:
        for theme_key, data in EASTER_EGGS.items():
            if file_size in data["sizes"]:
                return theme_key

    return None


def check_easter_egg(file_name, file_size, settings_file):
    """
    Проверяет имя и размер файла.
    Возвращает (egg_info, updated_settings) или (None, settings).
    egg_info: {theme, title, message}
    updated_settings: обновлённый объект настроек.
    """
    matched_theme = _match_theme(file_name, file_size)

    settings = _load_settings(settings_file)

    if not matched_theme:
        return None, settings

    unlocked = settings.get("unlocked_themes", [])

    if matched_theme in unlocked:
        return None, settings

    unlocked.append(matched_theme)
    settings["unlocked_themes"] = unlocked
    _save_settings(settings_file, settings)

    return {
        "theme": matched_theme,
        "title": EASTER_EGGS[matched_theme]["title"],
        "message": EASTER_EGGS[matched_theme]["message"],
    }, settings


def get_unlocked_themes(settings_file):
    settings = _load_settings(settings_file)
    return settings.get("unlocked_themes", [])


def get_progress(settings_file):
    unlocked = get_unlocked_themes(settings_file)
    return len(unlocked), len(EASTER_EGGS)