# Source boundaries

Method: code read /git/github.com/LiGoldragon/chroma/src/theme.rs

Chroma's Emacs concern constructs a one-shot `emacsclient --eval` expression,
redirects output, waits with a bounded timeout, and does not expose a durable
consumer acknowledgement or postcondition. Chroma owns semantic light/dark
selection; this adapter is only its Emacs projection.

Method: code read /git/github.com/LiGoldragon/chroma/src/daemon.rs

Chroma serves its command API over a framed Unix socket. Its D-Bus use is as a
client of other services; it does not currently own a public D-Bus service,
theme revision, or per-consumer projection-status interface.

Method: code read /home/li/primary/CriomOS-home/modules/home/profiles/med/emacs.nix

`criomos-home` currently owns the Emacs package, service, generated init,
native compilation, and the startup-only Darkman theme-state read.

Method: code read /home/li/primary/CriomOS-home/modules/home/base.nix

`criomos-home` generates and installs `ignis-dark-theme.el` and
`ignis-light-theme.el`; the approved plugin does not take ownership of those
theme assets.

Method: code read /home/li/primary/CriomOS-home/modules/home/profiles/min/chroma.nix

Home configures Chroma's current direct Emacs concern and supplies
`emacsclient`. The approved integration replaces that imperative projection
with the resident plugin and D-Bus protocol.

Method: code read /home/li/primary/CriomOS-emacs/README.md

The existing `CriomOS-emacs` repository describes a whole Emacs distribution,
not the focused Chroma projection plugin. It remains an unfinished scaffold
and is not the repository selected by the psyche.

Method: code read /home/li/primary/CriomOS-emacs/flake.nix

The scaffold declares its distribution inputs and Blueprint outputs but does
not yet expose the approved plugin package.
