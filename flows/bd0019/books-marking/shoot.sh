#!/usr/bin/env bash
# Renders every page at phone size (390x844) in light and dark with headless Chrome.
set -e
D=$(cd "$(dirname "$0")" && pwd); mkdir -p "$D/shots"
for scheme in light dark; do
  { echo '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    if [ $scheme = dark ]; then echo '<script>document.documentElement.setAttribute("data-theme","dark")</script>'; fi
    echo '</head><body>'; cat "$D/book.html"; echo '</body></html>'; } > "$D/shots/wrap-$scheme.html"
  for n in $(seq 1 10); do
    google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=390,844 --virtual-time-budget=4000 \
      --screenshot="$D/shots/$scheme-$n.png" "file://$D/shots/wrap-$scheme.html#p$n" >/dev/null 2>&1
  done
done
ls "$D/shots"
