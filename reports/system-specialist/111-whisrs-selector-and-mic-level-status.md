# WHISRS Selector And Mic Level Status

Report date: 2026-05-11
Role: system-specialist

## Question

The immediate request had two parts:

- choose the right selection UI for recalling recent transcriptions;
- enable a visible microphone-level signal in the desktop status bar.

The architectural question is whether transcript recall belongs inside WHISRS
or should be a separate component over WHISRS' structured history.

## Selector Research

Walker is the best modern launcher-shaped candidate. It is active, Wayland
native, presents itself as a full launcher with service mode, providers, dmenu
compatibility, themes, and typed workflows. Its CLI supports `--dmenu`, stdin
entries, labels, icons, values, preselection, and a background service for fast
open. That makes it the better long-term system selector if we want one launcher
surface to grow into multiple desktop actions.

Fuzzel is the best small immediate picker. It is Wayland-native, fast, stable,
and deliberately supports dmenu mode: feed newline-delimited rows on stdin, get
the selected row on stdout. For "show the last transcriptions and copy the one I
choose", that is exactly enough.

Wofi is the practical installed fallback. It is GTK-ish and supports dmenu mode,
but it is older and less appealing as the durable path. It is fine for a quick
local script, but I would not make it the named architecture.

Vicinae is modern and interesting, but it is too large for this narrow job. It
is a Raycast-like command environment with extensions and clipboard/history
features. That is a product surface, not a simple transcript picker.

Sources:

- Walker CLI: https://walkerlauncher.com/docs/cli
- Walker providers: https://walkerlauncher.com/docs/providers
- Fuzzel man page: https://man.archlinux.org/man/fuzzel.1.en
- Wofi man page: https://man.archlinux.org/man/wofi.1.en
- Vicinae docs: https://docs.vicinae.com/

## Recommendation

Do not put a selector dependency in WHISRS core.

WHISRS should own capture, transcription, recovery, and structured history.
Selection should be a separate component, probably named around the noun it
serves: `transcript-recall` or `whisrs-recall`. That component should read the
structured history file at `~/.local/share/whisrs/history.jsonl`, present recent
items through a pluggable picker backend, and copy the selected exact transcript.

The important constraint is that the recall component must not parse
human-formatted `whisrs log` output. It should read JSONL directly, or WHISRS
should grow a stable `history --json`/`recall --json` command first. That keeps
the desktop picker replaceable: Fuzzel now, Walker later, maybe a Noctalia panel
eventually.

## Mic Level Status

I implemented this as a pushed status stream, not polling.

The WHISRS daemon now has a `general.status_bar` config flag. When enabled, it
publishes newline-delimited JSON events over:

```text
$XDG_RUNTIME_DIR/whisrs/level.sock
```

Each client receives the current state immediately and then receives updates
when either daemon state or microphone level changes:

```json
{"state":"recording","level":0.42}
```

This uses the existing audio capture RMS level path. The old level path only fed
the bottom-screen overlay; now the stream can be enabled independently of that
overlay. The bottom overlay remains disabled in the home profile.

Noctalia gets a small local bar plugin at:

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/manifest.json`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/noctalia-plugins/whisrs-level/BarWidget.qml`

The widget subscribes to the Unix socket with QuickShell's socket/parser support
and renders a compact five-bar meter in the existing Noctalia bar. It reconnects
only when disconnected; it does not poll WHISRS for state. The WHISRS stream
caps microphone-level events at about 30 Hz so the bar can animate without
turning every audio callback into a shell redraw.

Sources:

- Noctalia plugin overview: https://docs.noctalia.dev/plugins/overview/
- Noctalia bar widget guide: https://docs.noctalia.dev/v4/development/plugins/bar-widget/
- Noctalia manifest reference: https://docs.noctalia.dev/plugins/manifest/
- QuickShell Socket: https://quickshell.org/docs/types/Quickshell.Io/Socket/
- QuickShell SplitParser: https://quickshell.org/docs/types/Quickshell.Io/SplitParser

## Local Changes

CriomOS-home changes:

- `packages/whisrs/status-bar-level-stream.patch` adds the daemon status socket.
- `packages/whisrs/default.nix` enables WHISRS' overlay feature because the
  pinned package needs that feature for the existing audio-level capture path.
- `modules/home/profiles/min/dictation.nix` enables `status_bar = true`.
- `modules/home/profiles/min/sfwbar.nix` registers the local Noctalia plugin in
  the right side of the bar.

Validation:

- `nix build .#whisrs -L`
- `nix build .#checks.x86_64-linux.pkgs-whisrs -L`

The WHISRS package build ran the release test suite: 210 library tests and 16
daemon tests passed.
