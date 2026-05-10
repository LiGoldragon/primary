# Abduco Agent Session Survivability

Written 2026-05-10 by system-specialist.

## Short Answer

Abduco is a good fit for the human part of the problem: one command, one
terminal-sized application, detachable and reattachable, without panes, tabs, or
tmux's extra interaction model.

It is not enough as Persona's terminal truth. Persona needs durable PTY
ownership, programmatic input, transcript capture, resize/lifecycle events, and
eventual typed terminal observations. Abduco exposes a small attach/detach byte
relay. That makes it useful as a human session wrapper or compatibility adapter,
but too thin to be the central substrate for Persona-controlled agents.

## What Abduco Gives Us

Officially, abduco is a "terminal session manager." It starts a command in its
own pseudo-terminal, represents the session as a Unix domain socket, lets clients
attach to that socket, and lets the command keep running after the client
detaches.

Useful properties:

- Minimal model: no panes, no windows, no tab semantics.
- Normal-feeling terminal attachment for a single application.
- Detach and reattach with `Ctrl+\` by default, configurable with `-e`.
- `abduco -A name command ...` attaches if the session exists, otherwise creates
  and attaches immediately.
- `abduco -r -a name` attaches read-only, useful for passive observation.
- `printf ... | abduco -p name` can pass input bytes into an existing session.
- Sessions use owner-only socket directories by default.
- Socket recreation is possible with `SIGUSR1` if the socket file is deleted.

Local state:

- `abduco` is already installed at `/home/li/.nix-profile/bin/abduco`.
- Local version reports `abduco-0.6`.
- `CriomOS-home` already includes it in the minimal profile at
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`,
  alongside `dvtm`.

## What It Does Not Give Us

Abduco does not preserve terminal state by itself. Its man page says it operates
on the raw I/O byte stream and does not interpret terminal escape sequences. If
the application needs preserved/redrawn terminal state, upstream recommends
running another utility such as `dvtm` inside abduco.

That has direct consequences for agent work:

- It is not a transcript database.
- It is not a typed terminal event stream.
- It is not a render-completion or readiness protocol.
- Its `-p` path is good for sending bytes, but not for capturing output.
- Read-only attach is a convenience, not a security boundary.
- Programmatic observation requires attaching a client and consuming raw terminal
  bytes, or adding a wrapper that records/parses output.

There is also an important detached-output caveat. Abduco keeps the process
alive after the terminal view disappears, but it is not a lossless scrollback
buffer. A chatty process can still become awkward while detached if no component
is draining and recording the PTY. For quiet interactive agents waiting on input,
that may be acceptable; for long tool output, Persona should own the PTY and
scrollback directly.

## Local Probe

A disposable local probe confirmed the important behavior:

- Starting an interactive shell through `abduco -c name /bin/sh -i`, then
  terminating the client, left the abduco session listed and reattachable.
- Passing input with `abduco -p name` returned immediately and kept the session
  alive.
- Creating an interactive shell with `abduco -n name /bin/sh -i` is not the same
  thing; an interactive shell created detached may exit because there was never
  an attached terminal client.

So the right human launcher shape is attach-or-create, not detached-create:

```sh
abduco -A codex-main codex
```

Reattach:

```sh
abduco -a codex-main
```

Send bytes:

```sh
printf 'status\n' | abduco -p codex-main
```

Observe without input:

```sh
abduco -r -a codex-main
```

## Persona Fit

`/git/github.com/LiGoldragon/persona-wezterm` already contains the more correct
core for Persona: a durable PTY daemon with disposable viewers, raw input
senders, capture, resize propagation, and a planned typed
`signal-persona-terminal` boundary.

That architecture is essentially the "terminal GUI is just a view" principle we
wanted from WezTerm mux, but with Persona owning the PTY instead of a terminal
emulator or abduco owning it.

Current local Persona surfaces:

- `persona-wezterm-daemon`: starts a child behind a durable PTY and exposes a
  Unix socket.
- `persona-wezterm-view`: attaches a disposable terminal viewer.
- `persona-wezterm-send`: sends prompt text plus Enter.
- `persona-wezterm-type`: sends raw bytes.
- `persona-wezterm-capture`: captures raw scrollback or visible screen text.

That is a better programmatic substrate than abduco because it can grow into
pushed terminal events and transcript ownership. The name is misleading now:
the durable core is not inherently WezTerm. It should become or be treated as a
general Persona terminal transport, with WezTerm, Ghostty, browser, abduco, or
other tools as viewers/adapters.

## Why Not Just Embed Abduco Under WezTerm Mux Or Tmux?

It can be done, but it is mostly layering without a clearer owner.

If abduco owns the process, WezTerm/Ghostty/tmux should be only a view that runs
`abduco -a name`. Adding WezTerm mux under or over abduco does not make Persona
control better; it only adds another lifecycle boundary to debug.

The clean split is:

- Human manual sessions: abduco is reasonable.
- Programmatic Persona sessions: Persona terminal daemon owns the PTY.
- GUI terminals: disposable viewers only.

## Recommendation

Use abduco for a small manual-agent launcher, not as Persona's core terminal
backend.

Proposed next shape:

1. Keep Ghostty as the default terminal.
2. Add a tiny `agent-session` launcher that defaults to:

   ```sh
   abduco -A <stable-name> <command> ...
   ```

3. Add explicit subcommands for list, attach, send, and read-only observe.
4. Test the invariant that killing the terminal window leaves the abduco session
   alive and reattachable.
5. Continue the Persona terminal path by generalizing `persona-wezterm` into a
   terminal transport whose durable PTY daemon owns critical agents directly.

This gives us the immediate practical safety the user wants, without confusing
abduco's minimal detach/reattach job with Persona's larger terminal-control job.

## Sources

- Official abduco project page:
  <https://www.brain-dump.org/projects/abduco/>
- abduco GitHub repository:
  <https://github.com/martanne/abduco>
- abduco man page:
  <https://www.mankier.com/1/abduco>
- Raw upstream man page:
  <https://raw.githubusercontent.com/martanne/abduco/master/abduco.1>
- Persona terminal backend survey:
  `/git/github.com/LiGoldragon/persona-wezterm/reports/1-terminal-backend-survey.md`
- Persona WezTerm architecture:
  `/git/github.com/LiGoldragon/persona-wezterm/ARCHITECTURE.md`
- WezTerm mux survivability report:
  `/home/li/primary/reports/system-specialist/102-wezterm-mux-survivability.md`
