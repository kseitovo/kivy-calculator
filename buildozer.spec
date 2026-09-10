[app]
title = Calculator
package.name = calculator
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,jpeg,atlas
version = 0.1
requirements = python3==3.10.14,kivy==2.3.0
orientation = portrait
fullscreen = 1

# Android configuration
android.api = 33
android.minapi = 21
android.ndk = 26b
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True
android.archs = arm64-v8a

# ТИЙ НАЙКРИТИЧНІШИЙ ФІКС ДЛЯ HARFBUZZ:
android.ext_cflags = -Wno-error=format-security
