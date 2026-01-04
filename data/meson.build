# Data files installation

datadir = get_option('prefix') / 'share'
icondir = datadir / 'icons' / 'hicolor' / 'scalable' / 'apps'
desktopdir = datadir / 'applications'
autostartdir = '/etc/xdg/autostart'

# Install icons
install_data(
    'icons/com.asoftware.askilit.svg',
    install_dir: icondir
)

# Install application images
install_data(
    'images/asoftware.png',
    'images/ebaqr.png',
    install_dir: libdir
)

# Install desktop file
install_data(
    'com.asoftware.askilit.desktop',
    install_dir: desktopdir
)

# Install autostart file
install_data(
    'com.asoftware.askilit.autostart.desktop',
    install_dir: autostartdir
)
