[app]
# Uygulamanın tablette görünecek adı
title = Ziraat Turkiye Kupasi Simulation

# Paket adı (Boşluksuz ve küçük harf)
package.name = ztk_simulation
package.domain = org.ztk

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0

# Gerekli kütüphanelerimiz
requirements = python3,kivy

# ⚠️ TABLET İÇİN ÖNEMLİ DEĞİŞİKLİK: 
# Tabletlerde uygulamanın hem yatay hem dikey dönebilmesi için 'all' yapıyoruz.
# Eğer sadece dikey kalmasını istiyorsan 'portrait' olarak bırakabilirsin.
orientation = all

fullscreen = 1

# ==========================================
# Android / Tablet Ayarları
# ==========================================
android.api = 33
android.minapi = 21
android.skip_update = False

# ⚠️ TABLET İÇİN ÖNEMLİ DEĞİŞİKLİK:
# Bazı eski Buildozer sürümleri varsayılan olarak tablet desteğini kapatabiliyor.
# Bu satır uygulamanın büyük ekranlarda (tabletlerde) düzgün ölçeklenmesini sağlar.
android.manifest.supports_screens = small, normal, large, xlarge

[buildozer]
log_level = 2
warn_on_root = 1
