#!/usr/bin/env bash
# Render each page at phone size (390x844), light and dark, with headless Chrome.
D=/home/li/primary/flows/bd0019/books-questions
S=${1:-/tmp/shots}; mkdir -p "$S"
for theme in light dark; do
for i in $(seq 1 12); do
  f="$S/t-$theme-$i.html"
  { echo '<!doctype html><html data-theme="'$theme'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}</style></head><body>';
    cat $D/book.html;
    echo "<script>document.getElementById('p$i').scrollIntoView({block:'start'});</script></body></html>"; } > "$f"
  google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=390,844 --virtual-time-budget=4000 --screenshot="$S/$theme-$i.png" "file://$f" >/dev/null 2>&1
done; done
ls "$S"/*.png | wc -l
