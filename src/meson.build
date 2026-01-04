# Install Python source files to /usr/share/askilit/

askilit_sources = [
    '__init__.py',
    'main.py',
    'application.py',
    'window.py',
    'utils.py',
    'network.py',
    'qrcode_generator.py',
    'touch_handler.py',
    'dialogs.py',
    'autolock.py',
    'network_restart.py',
    'constants.py',
    'i18n.py',
]

install_data(
    askilit_sources,
    install_dir: libdir
)

# Install UI files
install_subdir('ui', install_dir: libdir)
