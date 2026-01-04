#!/bin/bash
# Update translation files for ASKilit

if ! command -v xgettext &> /dev/null; then
    echo "xgettext could not be found."
    echo "Install with: apt install gettext"
    exit 1
fi

echo "Updating pot file..."
xgettext -o po/askilit.pot --from-code="utf-8" \
    $(find src -type f -iname "*.py") \
    $(find src -type f -iname "*.ui")

for lang in $(cat po/LINGUAS); do
    if [[ -f po/$lang.po ]]; then
        echo "Updating $lang.po"
        msgmerge -o po/$lang.po po/$lang.po po/askilit.pot
    else
        echo "Creating $lang.po"
        cp po/askilit.pot po/$lang.po
    fi
done

echo "Done!"
