[app]

title = TelegramParser
package.name = telegramparser
package.domain = org.dornes4
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# ✅ Указание стабильных версий SDK и Build Tools
android.sdk = 33
android.ndk = 25b
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2

android.archs = armeabi-v7a, arm64-v8a
android.enable_androidx = 1
android.use_android_support = 0
android.copy_libs = 1

requirements = python3,kivy

entrypoint = main.py
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

log_enable = 1
