# FileDrop

File transfer between PC and Android over Wi-Fi.
Передача файлов между ПК и Android по Wi-Fi.

## Authors
- **Nekeos** — Desktop (Windows/Linux)
- **soxr.net** — Android

## Features
- Send & receive files
- QR-code connection
- Custom save folder
- English & Russian UI
- Windows (PySide6) + Linux (Tkinter)

## Install

### Windows
Download FileDrop.exe from Releases and run.

### Linux
Download FileDrop from Releases:
chmod +x FileDrop
./FileDrop

### From source
git clone https://github.com/Nekeos/FileDrop.git
cd FileDrop
pip install -r requirements.txt
python -m file_drop.main        # Windows
python -m file_drop.main_tk     # Linux

## Android app
FileDrop for Android by soxr.net

## Protocol
TCP port 45000. Format: [4 bytes JSON length][JSON UTF-8][file bytes]

## Links
- RuStore: https://www.rustore.ru/catalog/developer/ch7shq
- Telegram: t.me/Axkuon

## License
MIT

# FileDrop

Передача файлов между ПК и Android по Wi-Fi.
File transfer between PC and Android over Wi-Fi.

## Авторы
- **Nekeos** — десктоп (Windows/Linux)
- **soxr.net** — Android

## Возможности
- 📤 Отправка и приём файлов
- 📱 QR-код для подключения
- 📂 Выбор папки сохранения
- 🌐 Русский и английский язык
- 🖥️ Windows (PySide6) + Linux (Tkinter)

## Установка

### Windows
Скачай `FileDrop.exe` из [Releases](https://github.com/Nekeos/FileDrop/releases) и запусти.

### Linux
Скачай `FileDrop` из [Releases](https://github.com/Nekeos/FileDrop/releases):
```bash
chmod +x FileDrop
./FileDrop

Из исходников

git clone https://github.com/Nekeos/FileDrop.git
cd FileDrop
pip install -r requirements.txt
python -m file_drop.main        # Windows
python -m file_drop.main_tk     # Linux

Android-приложение

