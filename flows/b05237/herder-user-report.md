# Herdr user report

**Checked 2026-09-18 against Herdr 0.8.2.** Herdr is a persistent terminal
workspace manager: start/attach with `herdr`; sessions survive terminal
detachments. The live config is `~/.config/herdr/config.toml`.

## Start here

```sh
herdr                         # launch or attach to the default session
herdr --session writing       # create/attach a named persistent session
herdr session list            # find sessions
herdr session attach writing  # attach one explicitly
herdr --remote host           # attach to a server through SSH
```

Use `prefix` below as **Ctrl-b** unless the configuration changes it. Press
and release the prefix, then the next key. `herdr --no-session` is the
single-process escape hatch; normally use the persistent server model.

## Every default keybinding

The current `config.toml` contains only `[ui.toast] delivery = "terminal"`;
it overrides **no keys**. These are the built-in defaults printed by
`herdr --default-config`.

| What | Key |
|---|---|
| Help / settings / detach | `prefix ?` / `prefix s` / `prefix q` |
| Reload config / open notification target | `prefix Shift-r` / `prefix o` |
| Workspace picker / go-to | `prefix w` / `prefix g` |
| New / rename / close workspace | `prefix Shift-n` / `prefix Shift-w` / `prefix Shift-d` |
| New / rename / previous / next / close tab | `prefix c` / `prefix Shift-t` / `prefix p` / `prefix n` / `prefix Shift-x` |
| Switch to tab 1–9 | `prefix 1` … `prefix 9` |
| Rename pane / edit scrollback | `prefix Shift-p` / `prefix e` |
| Focus pane left/down/up/right | `prefix h` / `prefix j` / `prefix k` / `prefix l` |
| Cycle panes next / previous | `prefix Tab` / `prefix Shift-Tab` |
| Split right / split down | `prefix v` / `prefix -` |
| Close pane / zoom pane / resize mode | `prefix x` / `prefix z` / `prefix r` |
| Toggle sidebar | `prefix b` |
| Remote image paste only | `Ctrl-v` with `herdr --remote` |

In **navigate mode**, local movement is `↑`, `↓`, `h`, `j`, `k`, `l`; the
left/right arrows always focus the adjacent pane. This mode deliberately
does not use prefix, Escape, Enter, Tab, or 1–9.

No defaults exist for previous/next workspace, previous/next agent, direct
agent/workspace index selection, moving tabs, direct resizing, opening or
removing worktrees, or last-pane toggle. They are configurable but unset.

## Everyday operations

**Organize work.** Use `prefix Shift-n` for a workspace, `prefix c` for a
tab, and `prefix v` / `prefix -` for side-by-side or stacked panes. Navigate
with `prefix hjkl`; `prefix z` temporarily makes one pane full-screen.
Rename rather than relying on generated labels.

**CLI equivalents.** Use `herdr workspace list|create|focus|rename|close`,
`herdr tab list|create|focus|rename|close`, and `herdr pane list|current|get|
layout|focus|resize|zoom|rename|split|swap|move|close`. `pane split` accepts
`--direction right|down`, `--ratio`, `--cwd`, environment entries, and focus
control. `pane focus` / `resize` use `--direction left|right|up|down`.

**Read or drive a terminal pane.** `herdr pane read PANE_ID` reads output;
`pane send-text PANE_ID TEXT` types text; `pane run PANE_ID COMMAND` types it
and Enter; and `pane send-keys PANE_ID esc …` sends named keys. Other pane
tools are `process-info`, `neighbor`, `edges`, `input`, `wait-output`, and
the `report-*` / `release-agent` lifecycle and metadata interfaces.

**Work with an AI agent.** `herdr agent list|get|read|rename|focus|attach|
wait|explain` inspects or reaches a detected agent. Start one only in a pane
at an interactive shell prompt:

```sh
herdr agent start research --kind codex --pane PANE_ID
herdr agent prompt research "Inspect the test failure" --wait
herdr agent send-keys research esc
```

`agent prompt` rejects a blocked agent before sending input. `--wait` can
wait for `idle`, `working`, `blocked`, `done`, or `unknown`; use `--timeout`
for a bound. `agent attach TARGET --takeover` opens its terminal directly.

**Git worktrees.** `herdr worktree list`; `create` supports `--cwd`,
`--branch`, `--base`, `--path`, `--label`, `--workspace`, and focus options;
`open` opens an existing checkout; `remove` removes one. Use `create` for a
new branch/worktree and `open` for an already-created checkout.

**Sessions, notices, integrations, and API.** `session list [--json]`,
`attach NAME`, `stop NAME`, and `delete NAME` manage persistence. Send a
visible notice with `herdr notification show TITLE --body TEXT --position
bottom-right --sound done|request|none`. `integration install TARGET`,
`uninstall TARGET`, and `status [--outdated-only]` manage built-in harness
hooks. `herdr api snapshot` shows live state; `api schema --json --output
FILE` exports the socket contract. `herdr config check` validates config and
`config reset-keys` backs up then removes custom bindings.

## Command map (complete top-level survey)

| Area | Commands found |
|---|---|
| `pane` | list, current, get, layout, process-info, neighbor, edges, focus, resize, zoom, read, rename, input, split, swap, move, close, send-text, send-keys, wait-output, run, report-agent, report-agent-session, release-agent, report-metadata |
| `agent` | list, get, read, send-keys, prompt, rename, focus, wait, attach, start, explain |
| `workspace` | list, create, get, focus, rename, report-metadata, close |
| `tab` | list, create, get, focus, rename, close |
| `notification` | show |
| `integration` | install, uninstall, status |
| `session` | list, attach, stop, delete |
| `config` | check, reset-keys |
| `worktree` | list, create, open, remove |
| `api` | snapshot, schema |

## Proposed Emacs-style Zfly setup

The aim is frequency-first: direct chords for pane movement, a two-key leader
for frequent layout/workspace operations, and indexed sequences for recall.
Use **Ctrl-Space** as the leader if the laptop terminal reliably forwards it;
otherwise use **F12**. Test in the actual terminal and keyboard-virtualization
layer before adopting it: terminals can encode Ctrl-Space as NUL.

```toml
[keys]
prefix = "ctrl+space" # fallback: "f12"
help = "prefix+?"
detach = "prefix+q"
reload_config = "prefix+shift+r"
focus_pane_left = "ctrl+alt+h"
focus_pane_down = "ctrl+alt+j"
focus_pane_up = "ctrl+alt+k"
focus_pane_right = "ctrl+alt+l"
split_vertical = "prefix+v"
split_horizontal = "prefix+minus"
zoom = "prefix+z"
close_pane = "prefix+x"
new_tab = "prefix+c"
previous_tab = "prefix+p"
next_tab = "prefix+n"
workspace_picker = "prefix+w"
new_workspace = "prefix+shift+n"
switch_tab = "prefix+1..9"
switch_workspace = "prefix+shift+1..9"
resize_pane_left = "ctrl+shift+alt+h"
resize_pane_down = "ctrl+shift+alt+j"
resize_pane_up = "ctrl+shift+alt+k"
resize_pane_right = "ctrl+shift+alt+l"
```

This preserves the memorable Emacs/Zfly spatial cluster (`h j k l`) while
avoiding plain `Ctrl-h/j/k/l`, which terminal programs commonly need. The
leader sequences remain mnemonic: `C-Space w` workspace, `c` tab, `v` split
vertical, `-` split horizontal, `z` zoom, `x` close, and `1..9` select. Add
previous/next workspace or agent bindings only after real use identifies them
as frequent enough to deserve scarce easy chords.

## Neary check

I searched `/git/github.com/LiGoldragon/` for a repository named Neary and
for tracked text/file names mentioning `neary`, `zfly`, `cold mac`, or
`coldmac`. No Neary-related repository or keyboard configuration was present.
The only Neary references found were historical flow records under the
`primary` repository, including the stated concern that its up/down bindings
are incomplete. Therefore this report does not claim a Neary binding map; it
is a proposal for Herdr pending the Neary source/config location.

## Evidence and safety notes

This report was derived from `herdr --help`, every requested area’s `--help`,
`herdr config --help`, `herdr integration --help`, `herdr --default-config`,
and the live config. Before editing the config, copy it; then run `herdr
config check` and `herdr server reload-config`. `config reset-keys` is a
recovery action, not a way to preview changes.
