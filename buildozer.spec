[app]
title = Love App
package.name = loveapp
package.domain = org.example
version = 2.0

source.dir = .
source.include_exts = py,png,jpg,kv,webp,ttf
source.include_patterns = logos/*
source.exclude_dirs = tests, bin, venv

requirements = 
    python3,
    kivy==2.3.0,
    setuptools,
    openssl,
    pillow,
    android,
    pyjnius

orientation = portrait
fullscreen = 1
icon.filename = %(source.dir)s/logos/heart.png
presplash.filename = %(source.dir)s/logos/heart.png

[android]
archs = arm64-v8a,armeabi-v7a
api = 33
minapi = 21
ndk_api = 21

android.accept_sdk_license = True
android.enable_androidx = True
android.allow_backup = False

android.permissions = 
    WRITE_EXTERNAL_STORAGE,
    READ_EXTERNAL_STORAGE

android.meta_data = 
    android.app.background_running=false
    android.hardware_accelerated=true

android.manifest_activities = 
    org.kivy.android.PythonActivity:
        android:launchMode="singleTask"
        android:configChanges="orientation|screenSize|keyboardHidden"
        android:screenOrientation="portrait"
        android:windowSoftInputMode="adjustResize"

android.release_artifact = apk
android.debug_artifact = apk
android.strip = True

[buildozer]
log_level = 2
warn_on_root = 1