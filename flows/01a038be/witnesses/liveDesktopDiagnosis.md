# Live Codex Desktop and Claude callback diagnosis

Method: strict BatchMode SSH as `li` to the established Ouranos endpoint,
reading only command links, installed package metadata, XDG handler metadata,
desktop caches, and process identities.  No URI callback, query data, auth
state, environment values, desktop action, or deployment was read or changed.

## Codex observations

The live login shell resolves `codex` from the active profile to the shared
`codex-0.149.0` package and reports `codex-cli 0.149.0`.  It resolves
`codex-desktop` to package
`codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059-codex-cli-path`.
There is no shell command named `chatgpt`.

The deployed `codex-desktop` wrapper remains present.  It defaults
`CODEX_CLI_PATH` to the shared Codex executable and execs the maintained
`codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059` frontend.
That frontend's own `codex-desktop.desktop` metadata states:

```text
Name=ChatGPT
Exec=…/bin/codex-desktop %u
MimeType=x-scheme-handler/codex;x-scheme-handler/codex-browser-sidebar;
StartupWMClass=codex-desktop
```

No Codex/ChatGPT desktop file or textual Codex/ChatGPT launcher override was
found in the inspected user, profile, system, Noctalia, or launcher-cache
locations.  Running current and older `codex` processes coexist; process
identity alone does not establish which one owns the screenshot window.

## Claude callback observations

The active Claude Desktop package is `claude-desktop-1.34493.1`.  Its package
desktop file declares:

```text
Name=Claude
Exec=claude-desktop %U
MimeType=x-scheme-handler/claude
StartupWMClass=claude-desktop
```

`xdg-mime` reports `claude-desktop.desktop` as the default for
`x-scheme-handler/claude`, but no `claude-desktop.desktop` file exists in the
active user, profile, or system XDG application directories and no active MIME
cache claims that handler.  The visible user-local desktop cache contains only
the unrelated `x-scheme-handler/claude-cli` Claude Code handler.  The package
desktop file exists only inside the installed package output, where application
discovery does not look on this live profile.

Chrome is the declared default browser for HTTPS and Chrome and Claude Desktop
processes are active.  No matching portal journal evidence was found, GNOME
Software has neither a live process nor a discoverable desktop entry, and no
stateful discovery action was observed.  The actual OAuth callback URI was not
captured, so its query data and even its observed-at-runtime scheme remain
unknown; the installed package supports `claude://` only.
