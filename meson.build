project(
    'askilit',
    version: '4.2',
    license: 'GPL-3.0',
    meson_version: '>= 0.59.0'
)

# Python module
python = import('python')
py_installation = python.find_installation('python3')

# i18n module
i18n = import('i18n')

# Project directories
prefix = get_option('prefix')
bindir = prefix / 'bin'
datadir = prefix / 'share'
libdir = prefix / 'share' / meson.project_name()
localedir = prefix / 'share' / 'locale'
icondir = prefix / 'share' / 'icons' / 'hicolor' / 'scalable' / 'apps'
desktopdir = prefix / 'share' / 'applications'
autostartdir = '/etc/xdg/autostart'

# Configuration data
conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('VERSION', meson.project_version())
conf.set('LOCALEDIR', localedir)
conf.set('PKGDATADIR', libdir)
conf.set('BINDIR', bindir)
conf.set('PROJECT_NAME', meson.project_name())

# Subdirectories
subdir('src')
subdir('data')
subdir('po')
subdir('bin')
