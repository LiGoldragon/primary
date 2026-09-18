# Herdr 0.8.2 — practical guide and window-management policy

Checked on 2026-09-18 against the **installed Herdr 0.8.2**. This is the
local guide for the tool the living calls “Herder”; its executable name is
`herdr`. It is deliberately not a guide to current `main`, a release after
0.8.2, or a community configuration. Those can contain useful ideas, but are
not evidence that a feature exists on this machine.

The practical rule is simple: keep the current work full-screen (zoomed),
keep no more than two panes visible by default, and put overflow in named tabs
or workspaces. Herdr 0.8.2 has no `max_panes`, `max_splits`, or automatic
zoom setting. The limit is therefore an operating convention, not something
the program presently enforces.

## What the names mean

Herdr is the persistent terminal-workspace manager. A **session** is its
long-lived server-backed container; a **workspace** is a named group inside a
session; a **tab** is a page in a workspace; a **pane** is one terminal cell
in the tab. The nesting is:

```
Herdr session
  └─ workspace
       └─ tab
            └─ pane (one terminal / one harness process)
```

An individual **harness** is the program in a pane, such as Codex or Claude
Code. The **Persona meta-harness** is the larger proposed thinking-machine
system that coordinates identities, prompts, tools, and policies across
harnesses. It is not another name for Herdr. Use “Herdr” for the terminal
manager, “harness” for the individual coding environment, and “Persona
meta-harness” for the cross-harness design.

This terminology follows the psyche’s request for the mental model and
keyboard setup, its later full-screen-per-layer preference, and its named
Persona distinction. See [terminal vision](../flows/6cc91b/vision/terminal.md),
[operational user-experience request](../flows/b05237/vision/operational-herderUserExperience.md),
[Herdr learning request](../flows/01a030aa/vision/herdr.md),
[Persona meta-harness vision](../flows/1a6ca4/vision/personaMetaHarness.md),
and [harness vocabulary note](../flows/38dec9/vision/harnessVocabulary.md).

## The layout policy

### Default: work + companion

Use at most two panes in the current tab: the active harness plus one
companion (test/watch/log/reference). Split only when both must be watched or
acted on together. Make the active one full-screen with `prefix z`; toggle it
off only to consult the companion. Name panes and tabs rather than relying on
their position.

### Deliberate exception: 2×2 monitoring grid

Four panes are allowed only for a temporary monitoring grid: for example,
three long-running observations plus a control pane. Make it a 2×2 grid,
give every pane a clear name, and dissolve it when the observation ends. Do
not grow a five- or six-way nested split: legibility and targeting collapse
before the extra terminal is useful.

### Overflow: tabs and workspaces

Put a different task, repository, or layer in a labeled tab; put a larger
area of work in a labeled workspace. A reasonable starting organization is:

| Need | Put it in | Example label |
| --- | --- | --- |
| Current task and its one companion | one tab, one or two panes | `guide + verify` |
| A separate bounded task | another tab | `messaging research` |
| A different layer or long-lived role | another workspace | `field`, `psyche`, `build` |
| A temporary dashboard | one 2×2 tab | `monitoring` |

Two useful alternatives are:

- **Coordinator triad:** three named tabs/workspaces—`inbox`, `active`, and
  `observe`—with only `active` routinely split. This keeps coordination,
  work, and passive observation from becoming one noisy desktop.
- **Layer desktops:** one full-screen Herdr workspace/session per layer, as
  the psyche suggested: e.g. Field, Psyche, Build, Review, and Personal.
  Within each, use tabs for tasks and zoom for active attention. This gives
  the “five full-screen Herders” feel without mistaking each terminal for a
  new harness.

## Quick start

```sh
herdr                           # launch/attach the default persistent session
herdr --session field           # create or attach a named persistent session
herdr session list              # see named sessions and state
herdr session attach field      # attach explicitly
```

Use `prefix` as **Ctrl-b** unless the local configuration changes it. Press
and release the prefix, then the next key.

The five keys to learn first:

| Result | Default key |
| --- | --- |
| Move focus left/down/up/right | `prefix h` / `j` / `k` / `l` |
| Split right / down | `prefix v` / `prefix -` |
| Zoom or restore the current pane | `prefix z` |
| New tab | `prefix c` |
| Workspace picker | `prefix w` |

Then add `prefix x` to close a pane, `prefix p` / `prefix n` for previous /
next tab, `prefix 1` through `prefix 9` for a tab, `prefix b` for the
sidebar, `prefix Shift-r` to reload configuration, and `prefix q` to detach.
Herdr also has a resize mode at `prefix r`, pane cycling at `prefix Tab` and
`prefix Shift-Tab`, and `prefix Shift-p` to rename a pane.

The practical sequence is: make a named workspace (`prefix Shift-n`), make a
named tab (`prefix c`, then `prefix Shift-t`), split only for the one
companion (`prefix v` or `prefix -`), then zoom the pane in which you are
actually working (`prefix z`).

### Mouse-first use

Click a workspace/tab/pane to focus it, use visible controls to create or
close items, and use the sidebar as a compact status rail. The keyboard does
not need to be learned all at once: the essential mouse-first habit is still
“one active pane, zoomed; only one companion visible when needed.”

### Keyboard-first use

Stay on the spatial cluster `prefix h j k l`; use `prefix z` as the ordinary
full-screen toggle; and use `prefix w` or numbered tabs instead of cycling
through a crowded split. This fits the psyche’s frequency-first wish: common
navigation is easy, while less frequent operations remain leader sequences.

## Persistence, attachment, and safe recovery

Normal `herdr` use is server/client based. Detaching (`prefix q`) closes the
attached terminal view while leaving the session server and terminal programs
running. Attach later with `herdr session attach NAME`. `herdr --no-session`
is the one-process escape hatch, not the normal persistent workflow.

`herdr session stop NAME` stops a session; `herdr session delete NAME` only
deletes a stopped session. Do not use either as a substitute for detaching.

Current read-only state at check time:

```text
installed version: 0.8.2
server status: running (protocol 20, compatible)
running session: messaging-build
default session: stopped
config: /home/li/.config/herdr/config.toml
```

## Current configuration snapshot

The authored local config currently contains only:

```toml
[ui.toast]
delivery = "terminal"
```

So it overrides no keybinding and uses 0.8.2 defaults, including `ctrl+b` as
prefix, visible sidebar, and a tab row that remains visible even with one tab.
The default configuration does offer `sidebar_start_collapsed`,
`sidebar_collapsed_mode = "hidden"`, and
`hide_tab_bar_when_single_tab = true`; these are candidates for a later,
separately approved config change, not changes made by this guide.

Safe configuration workflow:

```sh
cp ~/.config/herdr/config.toml ~/.config/herdr/config.toml.before-layout-change
# edit ~/.config/herdr/config.toml
herdr config check
herdr server reload-config
```

Run `herdr config check` before reload. If the change is unusable, restore the
copy and validate/reload again. `herdr config reset-keys` backs up and removes
custom bindings; it is a recovery operation, not a preview facility. A few UI
settings explicitly take effect only on the next launch, so read the generated
default config comment before expecting a reload to change them.

## Notifications and automation boundary

With `delivery = "terminal"`, Herdr asks the outer terminal to present toast
notifications. `herdr notification show TITLE --body TEXT --position
bottom-right --sound done|request|none` can create a visible notice. Its sound
choice is an attention hint, not a Messenger receipt, an identity proof, or a
durable delivery ledger.

Herdr can control panes, expose `api snapshot`, integrate with harnesses, and
report display metadata. It is therefore a good terminal transport substrate.
It is not the authority for cross-flow identity resolution, durable messaging
receipts, session ownership, or lifecycle reaping. Automation must not infer
that a pane has died merely because a visible attachment closed. A field
watcher may observe endpoints and report a stale or failed harness to the
messaging/lifecycle owner, but it should not silently close panes, stop
sessions, alter layouts, or rewrite an index. Treat failed harness cleanup as
an explicit lifecycle action with its own evidence and authority.

## Troubleshooting

| Symptom | Check first | Safe response |
| --- | --- | --- |
| “Everything is tiny/confusing” | Too many panes are visible | `prefix z` the active pane; move overflow to named tabs/workspaces; reduce to two panes. |
| “I lost the terminal” | It may only be detached | `herdr session list`, then `herdr session attach NAME`. |
| Key does nothing | Prefix/config/terminal interception | Confirm `Ctrl-b`, run `herdr config check`, and test in the actual terminal/keyboard layer before remapping. |
| UI config looks unchanged | Setting may require a new launch | Check the relevant default-config comment, then detach/reattach or restart only with session-owner authority. |
| Notification is absent | Outer terminal notification delivery | Confirm `ui.toast.delivery`; use a direct `herdr notification show` test only when a visible test notice is acceptable. |
| Copy mode expectation is Emacs-like | Not established in 0.8.2 evidence | Treat current copy/navigation behavior as Vim-like; do not claim Emacs copy mode without a local test or version-specific documentation. |

## Version-aware research and configuration ideas

The following links are useful reading, not instructions to apply unchanged.
They target later upstream versions, a different fork/site, or individual
community configurations. None proves support in installed 0.8.2.

- Upstream [0.9.1 release notes](https://github.com/herdrdev/herdr/releases/tag/v0.9.1),
  [changelog](https://github.com/herdrdev/herdr/blob/master/CHANGELOG.md), and
  the supplied [keyboard-guide path](https://github.com/herdrdev/herdr/blob/master/website/src/content/docs/keyboard.mdx): compare these against `herdr --version`,
  `herdr --default-config`, and `herdr <subcommand> --help` locally before
  copying a binding or feature claim. The supplied keyboard-guide path returned
  HTTP 404 on this check, so it was not used as feature evidence.
- Motionharvest’s [configuration](https://github.com/motionharvest/herdr/blob/main/website/src/content/docs/configuration.mdx)
  and [persistence/remote](https://github.com/motionharvest/herdr/blob/main/website/src/content/docs/persistence-remote.mdx)
  documents may describe a different distribution or revision.
- A community [Vim-style config](https://github.com/mkdir700/herdr-config/blob/main/config.toml),
  a [daily-driver config](https://github.com/rlch/dotfiles/blob/main/CLAUDE.md),
  the [Emacs discussion](https://github.com/herdrdev/herdr/discussions/2806),
  [fullscreen discussion](https://github.com/herdrdev/herdr/discussions/533),
  [split-pain issue](https://github.com/herdrdev/herdr/issues/330), and
  [cbds bounded-tabs project](https://github.com/zqkra/cbds) are examples of
  ideas or individual practice. They are not evidence of popularity, support,
  or compatibility. In particular, Emacs-style copy mode is **not confirmed**
  here; local observed copy/navigation conventions are Vim-like.

Before adopting any keyboard scheme, test it through the terminal emulator and
the keyboard-virtualization layer. `Ctrl-Space` can be encoded as NUL by some
terminals, so a proposed Emacs-like leader needs a real end-to-end test and a
fallback such as `F12`. Do not remap plain `Ctrl-h/j/k/l` casually: terminal
programs frequently consume them.

## Local evidence used

The installed executable returned `herdr 0.8.2`; `herdr config check` returned
`config: ok`; `herdr status server` returned running and compatible; and
`herdr --default-config`, `herdr pane zoom --help`, `herdr workspace --help`,
`herdr tab --help`, and `herdr notification show --help` established the
version-specific commands recorded above. The expanded operational inventory
and default binding transcript are preserved in
[the field report](../flows/b05237/herder-user-report.md).
