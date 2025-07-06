[app]
title = Telegram Parser
package.name = telegramparser
package.domain = org.telegram.parser

source.dir = .
source.include_exts = py,kv,json,gif
source.include_patterns = background.gif,credentials.json

version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.archs = armeabi-v7a, arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b

android.entrypoint = org.kivy.android.PythonActivity
android.theme = @android:style/Theme.NoTitleBar
android.copy_libs = 1

log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
