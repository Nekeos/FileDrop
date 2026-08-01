# FileDrop

File transfer between PC and Android over Wi-Fi.
Передача файлов между ПК и Android по Wi-Fi.

## Authors / Авторы
- Nekeos — Desktop (Windows/Linux)
- soxr.net — Android

## Features / Возможности
- Send & receive files / Отправка и приём файлов
- QR-code connection / QR-код для подключения
- Custom save folder / Выбор папки сохранения
- English & Russian UI / Русский и английский язык
- Dark and Light themes / Тёмная и светлая темы
- Windows (PySide6) + Linux (Tkinter)

## Install / Установка

### Windows
Download FileDrop.exe from Releases and run.
Скачай FileDrop.exe из Releases и запусти.

### Linux
Download FileDrop from Releases:
Скачай FileDrop из Releases:
chmod +x FileDrop
./FileDrop

### From source / Из исходников
git clone https://github.com/Nekeos/FileDrop.git
cd FileDrop
pip install -r requirements.txt
python -m file_drop.main        # Windows
python -m file_drop.main_tk     # Linux

## Android app / Android-приложение
FileDrop for Android by soxr.net
FileDrop для Android от soxr.net

## Protocol / Протокол
TCP port 45000. Format: [4 bytes JSON length][JSON UTF-8][file bytes]
TCP порт 45000. Формат: [4 байта длина JSON][JSON UTF-8][файл]

## Links / Ссылки
- Website / Сайт: https://www.Axkuon.ru
- GitHub: https://github.com/Nekeos/FileDrop
- RuStore: https://www.rustore.ru/catalog/developer/ch7shq
- Telegram: https://t.me/Axkuon

## License / Лицензия
MIT
