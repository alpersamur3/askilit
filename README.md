# ASKilit - Screen Lock Application for Interactive Boards

<p align="center">
  <img src="data/icons/com.asoftware.askilit.svg" alt="ASKilit Logo" width="128" height="128">
</p>

<p align="center">
  <strong>Etkileşimli eğitim tahtaları için ekran kilidi uygulaması</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#building">Building</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

---

## 🎯 About / Hakkında

ASKilit, etkileşimli eğitim tahtaları için tasarlanmış bir ekran kilidi uygulamasıdır. Öğrencilerin öğretmen izni olmadan tahtayı kullanmasını engeller.

ASKilit is a screen lock application designed for interactive educational boards. It prevents students from using the board without teacher authorization.

## ✨ Features / Özellikler

| Feature | Description |
|---------|-------------|
| 🔐 **EBA QR Login** | Teachers can unlock using EBA QR code login |
| 📱 **Offline QR** | Fallback QR code when internet is not available |
| ⏱️ **Auto-lock** | Automatic screen lock after 25 minutes of inactivity |
| 👆 **Touch Detection** | Monitors touch screen for activity |
| 🌍 **Multi-language** | Turkish and English support with gettext |
| 🔄 **Auto-restart** | Restarts when network becomes available |

## 📁 Project Structure / Proje Yapısı

```
askilit/
├── meson.build              # Main build configuration
├── src/                     # Source code
│   ├── application.py       # GTK Application class
│   ├── window.py            # Main lock window
│   ├── utils.py             # Utility functions
│   ├── network.py           # Network checking
│   ├── qrcode_generator.py  # QR code generation
│   ├── touch_handler.py     # Touch screen handling
│   ├── dialogs.py           # Dialog windows
│   ├── autolock.py          # Auto-lock module
│   ├── constants.py         # Configuration constants
│   └── i18n.py              # Internationalization
├── bin/                     # Launcher scripts
├── data/                    # Desktop files, icons, images
├── po/                      # Translations (tr, en)
└── debian/                  # Debian packaging
```

## 📦 Installation / Kurulum

### From .deb Package / Paketten Kurulum

```bash
# Download the latest release
sudo dpkg -i askilit_4.0-1_all.deb

# Install missing dependencies if any
sudo apt-get install -f
```

### Dependencies / Bağımlılıklar

```bash
sudo apt install python3 python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 gir1.2-webkit2-4.1 \
    python3-qrcode python3-evdev python3-requests xinput
```

## 🔧 Building / Derleme

### Prerequisites / Gereksinimler

```bash
# Debian/Ubuntu/Pardus
sudo apt install meson ninja-build python3 python3-gi \
    python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.1 \
    python3-qrcode python3-evdev python3-requests xinput gettext
```

### Build from Source / Kaynaktan Derleme

```bash
# Clone the repository
git clone https://github.com/alpersamur3/askilit.git
cd askilit

# Configure
meson setup build --prefix=/usr

# Build
ninja -C build

# Install (requires root)
sudo ninja -C build install
```

### Build Debian Package / Debian Paketi Oluşturma

```bash
# Install build dependencies
sudo apt install debhelper dh-python meson ninja-build

# Build the package
dpkg-buildpackage -us -uc -b

# The .deb file will be in the parent directory
```

## 🚀 Usage / Kullanım

The application starts automatically on login via the autostart desktop file.

### Manual Start / Manuel Başlatma

```bash
askilit        # Normal start
askilit st     # Autostart mode (with loading countdown)
```

### Touch Permission Setup / Dokunmatik Ekran İzin Ayarı

For the 25-minute inactivity timer to work properly:

```bash
# Find your touch device
xinput list | grep -i touch

# Enable read permission (replace X with your device number)
sudo chmod a+r /dev/input/eventX
```

Without this setup, the device will lock every 45 minutes instead of 25 minutes of inactivity.

## ⚙️ Configuration / Yapılandırma

All timing and configuration values can be customized by editing:

**`/usr/share/askilit/constants.py`** (after installation)

or

**`src/constants.py`** (before building)

### Available Settings / Mevcut Ayarlar

| Setting | Default | Description |
|---------|---------|-------------|
| `AUTOLOCK_TIMEOUT` | 25 min | Lock after inactivity (with touch device) |
| `AUTOLOCK_FALLBACK_TIMEOUT` | 45 min | Lock after inactivity (without touch device) |
| `AUTO_POWEROFF_TIMEOUT` | 20 min | Auto shutdown if lock screen not unlocked |
| `NETWORK_CHECK_INTERVAL` | 60 sec | How often to check network status |
| `STARTUP_NETWORK_CHECK_INTERVAL` | 20 sec | Network check interval at startup |

### Example / Örnek

```python
# Change autolock to 30 minutes
AUTOLOCK_TIMEOUT = 30 * 60  # 30 minutes in seconds

# Disable auto poweroff (set very high)
AUTO_POWEROFF_TIMEOUT = 24 * 60 * 60  # 24 hours
```

## 🔓 Unlocking / Kilidi Açma

### With Internet / İnternet Varken
1. EBA QR code appears on screen
2. Teacher scans with EBA mobile app
3. Login with teacher account (roles: 2, 300, 301)
4. Screen unlocks automatically

### Without Internet / İnternet Yokken
1. Random QR code with 6-digit number appears
2. Scan QR code with any QR reader
3. Enter the 6-digit code using numpad
4. Screen unlocks

## 🌐 Translations / Çeviriler

To update translations:

```bash
./update-translations.sh
```

To add a new language:
1. Add language code to `po/LINGUAS`
2. Run `./update-translations.sh`
3. Edit the new `.po` file

## 📋 Changelog

### v4.3 (2026-01-05)
- Fix loading screen disappearing during countdown
- Add udev rules for automatic touch permission
- Fix postinst script for debian package

### v4.2 (2026-01-05)
- Fix QR codes showing together on desktop startup
- Add loading screen for normal startup mode
- Fix UI blocking during network check
- Add udev rules for automatic touch permission
- Add Configuration section to README

### v4.0 (2026-01-05)
- Major refactoring with Meson build system
- Complete code restructuring with proper hierarchy
- All code converted to English with gettext i18n
- Fixed gi.require_version for GTK/WebKit
- Added WebKit2 4.0/4.1 compatibility
- Replaced os.system with subprocess.run

### v3.4
- Initial public release

## 📄 License / Lisans

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

## 👤 Author / Yazar

**Alper Samur**
- 📧 Email: alpersamur0705@gmail.com
- 🐙 GitHub: [@alpersamur3](https://github.com/alpersamur3)

## 🙏 Acknowledgments / Teşekkürler

- Bayram Karahan öğretmenime, bu projeye ilham verdiği için teşekkürler.

---

<p align="center">
  Made with ❤️ for Turkish Education
</p>
