# Configure and install launcher scripts to /usr/bin

bindir = get_option('prefix') / 'bin'

# Main application launcher
configure_file(
    input: 'askilit.in',
    output: 'askilit',
    configuration: conf,
    install: true,
    install_dir: bindir,
    install_mode: 'rwxr-xr-x'
)

# Autolock launcher
configure_file(
    input: 'askilit-autolock.in',
    output: 'askilit-autolock',
    configuration: conf,
    install: true,
    install_dir: bindir,
    install_mode: 'rwxr-xr-x'
)

# Network restart launcher
configure_file(
    input: 'askilit-restart.in',
    output: 'askilit-restart',
    configuration: conf,
    install: true,
    install_dir: bindir,
    install_mode: 'rwxr-xr-x'
)
