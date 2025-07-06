[app]

# Название приложения
title = TelegramParser

# Имя пакета и домен
package.name = telegramparser
package.domain = org.dornes4

# Основной файл и директория
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json

# Версия приложения
version = 1.0.0

# Ориентация и полноэкранный режим
orientation = portrait
fullscreen = 1

# Разрешения Android
android.permissions = INTERNET

# ✅ Актуальные параметры сборки
android.api = 33
android.ndk = 25b
android.minapi = 21
android.build_tools_version = 30.0.3

# Архитектуры
android.archs = armeabi-v7a, arm64-v8a

# AndroidX
android.enable_androidx = 1
android.use_android_support = 0

# Копировать библиотеки в APK
android.copy_libs = 1

# Зависимости Python
requirements = python3,kivy

# Точка входа
entrypoint = main.py

# Иконка и заставка (если есть)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# Включить логирование
log_enable = 1
