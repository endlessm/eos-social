find . -type f \( -name "*.py" -o -name "*.glade" \)| xargs xgettext --sort-output --keyword=translatable -o po/endless_template.pot --from-code=utf-8
