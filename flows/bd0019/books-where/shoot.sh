#!/usr/bin/env bash
# Renders each page of «Where books go…» at phone size (390x844), light and dark, with headless
# Chrome, that page alone shown (the others hidden in the test wrapper only); also dumps the DOM to check for sideways overflow and controls.
set -e
D=$(cd "$(dirname "$0")" && pwd); O="$D/shots"; mkdir -p "$O"
for scheme in light dark; do
  { echo '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    [ $scheme = dark ] && echo '<script>document.documentElement.setAttribute("data-theme","dark")</script>'
    echo '</head><body>'; cat "$D/book.html"
    echo '<script>addEventListener("load",function(){var n=+(location.hash.slice(2)||1);var ps=document.querySelectorAll(".page");ps.forEach(function(p,i){if(i!==n-1)p.style.display="none";});
var w=document.documentElement.scrollWidth;var bad=[].filter.call(document.querySelectorAll("body *"),function(e){var r=e.getBoundingClientRect();return r.right>innerWidth+0.5&&!e.closest("pre")&&!e.closest("svg");}).length;
document.title="SW="+w+" IW="+innerWidth+" OVER="+bad+" BTN="+document.querySelectorAll("button,a,input,select,[onclick],[role=button],[tabindex]").length;});</script>'
    echo '</body></html>'; } > "$O/wrap-$scheme.html"
  for n in $(seq 1 10); do
    google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=390,844 --virtual-time-budget=4000 \
      --screenshot="$O/$scheme-$n.png" "file://$O/wrap-$scheme.html#p$n" >/dev/null 2>&1
  done
done
google-chrome --headless=new --disable-gpu --window-size=390,844 --virtual-time-budget=4000 --dump-dom "file://$O/wrap-light.html#p1" 2>/dev/null | grep -o '<title>SW=[^<]*</title>'
ls "$O"
