# WezTerm Palette RPC Test

This is a narrow probe for WezTerm's internal `SetPalette` RPC path.

It does not emit OSC, does not write to `/dev/pts`, and does not
discover or fan out to terminals. It requires an explicit WezTerm GUI
socket and pane id.

Run it only against a disposable pane. The default restore sends
`ColorPalette::default()` after 1200 ms; it does not remember the
pane's previous palette.

## Check

```sh
tools/wezterm-palette-rpc-test/run --help
```

## Suggested Manual Probe

Start a disposable WezTerm process:

```sh
wezterm start --always-new-process --class chroma-palette-rpc-test -- \
  zsh -lc 'for index in {1..2000}; do print "palette-test $index"; done; exec zsh'
```

Find its socket and pane id:

```sh
ls -t /run/user/$UID/wezterm/gui-sock-* | head
WEZTERM_UNIX_SOCKET=/run/user/$UID/wezterm/gui-sock-<pid> \
  wezterm cli --no-auto-start list --format json
```

Apply one palette change through the internal RPC path:

```sh
tools/wezterm-palette-rpc-test/run \
  --socket /run/user/$UID/wezterm/gui-sock-<pid> \
  --pane-id <pane-id> \
  --palette magenta
```

Use `--restore-after-ms never` only when you are comfortable closing
the disposable pane instead of relying on the default restore.
