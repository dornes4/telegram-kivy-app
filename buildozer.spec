[app]

# (str) Title of your application
title = TelegramParser

# (str) Package name
package.name = telegramparser

# (str) Package domain (unique identifier)
package.domain = org.dornes4

# (str) Source code where main.py is located
source.dir = .

# (str) Main .py file
source.main = main.py

# (list) List of inclusions using pattern matching
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Supported orientation (one of: landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (str) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android build tools version to use
android.build_tools_version = 33.0.2

# (str) Minimum API your APK will support
android.minapi = 21

# (str) Target API your APK will support
android.api = 33

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (list) Application requirements
requirements = python3,kivy

# (str) Entry point for your app
entrypoint = main.py

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (bool) Presplash screen
presplash.filename = %(source.dir)s/presplash.png

# (str) Supported architectures
android.archs = armeabi-v7a, arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = 1

# (bool) Use legacy android support libraries
android.use_android_support = 0

# (str) Custom Java package path (if needed)
# android.add_src = ./src

# (list) Additional Java .jar files to add to the libs
# android.add_jars = libs/*.jar

# (list) Additional .aar libraries to add
# android.add_aars = libs/*.aar

# (str) Custom Java classpath (if needed)
# android.add_classes = com/example/MyClass

# (str) Path to keystore for signing (optional for debug)
# android.release_key.alias = mykey
# android.release_key.storepass = password
# android.release_key.keypass = password
# android.release_key.keystore = mykeystore.keystore

# (bool) Enable logcat output
log_enable = 1

# (str) Custom package data
# include_patterns = assets/*,images/*.png

# (str) Path to custom build directory
# build_dir = ./build

# (str) Path to .spec file
# specfile = buildozer.spec
