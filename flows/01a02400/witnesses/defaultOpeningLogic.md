# Default opening logic witnesses

## Published source and immutable pin

Method: probe `gh api repos/LiGoldragon/CriomOS-home/commits/3aad4cad674926f0e921590079d285d8fcaef028`.

GitHub returned the published CriomOS-home commit `3aad4cad674926f0e921590079d285d8fcaef028` (`Make handlr-regex the Chrome default opener`).

Method: probe `gh api repos/LiGoldragon/CriomOS/commits/90da2a6f82ecd73a40850303abaa4e911a20c51f`.

GitHub returned the published CriomOS commit `90da2a6f82ecd73a40850303abaa4e911a20c51f` (`Pin CriomOS-home default opener revision`).

Method: probe `gh api 'repos/LiGoldragon/CriomOS/contents/flake.lock?ref=90da2a6f82ecd73a40850303abaa4e911a20c51f'`.

At that CriomOS revision, the `criomos-home` lock node has `rev` `3aad4cad674926f0e921590079d285d8fcaef028` and `narHash` `sha256-l2b68bgqXEj14Gxc2kCcIp4AUaAWhYvdDZyYR7qtjAI=`.

## Current opener resolution and desktop defaults

Method: probe `command -v xdg-open xdg-mime xdg-settings handlr; type -a xdg-open handlr; printf '%s\n' "$PATH"`.

`xdg-open`, `xdg-mime`, and `xdg-settings` resolve to `/run/current-system/sw/bin`; `handlr` resolves to `/home/li/.nix-profile/bin/handlr`. `type -a xdg-open` reports `/run/current-system/sw/bin/xdg-open` before `/home/li/.nix-profile/bin/xdg-open`. The relevant live PATH order is system `xdg-open` before the user profile; `/home/li/.local/bin` is absent.

Method: probe `for mime in x-scheme-handler/http x-scheme-handler/https text/html text/plain application/pdf inode/directory; do xdg-mime query default "$mime"; done`.

`xdg-mime` reports `google-chrome.desktop` for `x-scheme-handler/http`, `x-scheme-handler/https`, and `text/html`; `emacsclient.desktop` for `text/plain`; `org.pwmt.zathura-pdf-mupdf.desktop` for `application/pdf`; and `org.gnome.Nautilus.desktop` for `inode/directory`.

Method: probe `xdg-settings get default-web-browser`.

`xdg-settings` reports `google-chrome.desktop` as the default web browser.

Method: probe `for mime in x-scheme-handler/http x-scheme-handler/https text/html text/plain application/pdf inode/directory; do handlr get "$mime"; done`.

`handlr get` reports `google-chrome.desktop` for HTTP, HTTPS, and HTML; `emacsclient.desktop` for plain text; `org.pwmt.zathura-pdf-mupdf.desktop` for PDF; and `codium.desktop` for directories.

## Durable-check store path

Method: probe `test -x /nix/store/5vjjj770afapvwvp4mfgqcc2syzm9xdg-default-opener`.

The path was carried from implementation transcript `rollout-2026-08-21T20-29-06-01a02595-71c1-7471-91f5-57b3008e5419.jsonl`, JSONL record 1159 (ordinal 1158, `2026-08-21T22:28:34.655Z`): its completed exit-0 remote-only check command reported copying this output from Prometheus. It is not a fresh derivation by this migration. It is not currently executable (and was not run), so the historical green-check result remains a claim rather than a current witness.

## Lojix deployment 23

Method: probe `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'`.

The reply includes deployment `23`: `UserEnvironment.li`, `UserEnvironment.ActivateNow`, `LiveActivation`, immutable revision `90da2a6f82ecd73a40850303abaa4e911a20c51f`, admission marker `(522 522)`, terminal state `Completed`, terminal marker `(555 555)`, and `Some.Succeeded`.

## Feature-bead state

Method: probe `bd show home-nhb --json` in `/git/github.com/LiGoldragon/CriomOS-home`.

`home-nhb` is `blocked`. Its recorded remaining acceptance gap is a safe fresh graphical login and a post-login current-session wrapper witness; its notes state that no GUI/session refresh, reboot, or emergency mutation was performed.
