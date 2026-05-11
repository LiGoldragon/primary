# 14 - Terminal Cell Architecture Review

Role: designer-assistant.

Date: May 11, 2026.

## Verdict

`terminal-cell` first existed as a narrow prototype: code written to prove the
risky attach-path idea before treating it as the durable shape. The next pass
started converting that prototype into a production-candidate low-level
terminal cell by replacing source-only witnesses with behavioral witnesses and
enforcing single active viewer authority.

It is not done as the production terminal component. The production shape still
belongs in `persona-terminal`: a long-lived supervisor daemon, Sema-owned
session registry, typed contracts, and an explicit policy for active viewers and
programmatic injection.

The component now proves the important local claim: a terminal session can be
daemon-owned, visible through Ghostty, reattachable, injectable, transcriptable,
and responsive when the live path is an abduco-like byte pump instead of a
transcript-rendered actor relay.

## Tour

The current runtime shape is:

```text
Ghostty PTY
  <-> terminal-cell-view
  <-> one attached Unix stream
  <-> terminal-cell-daemon
  <-> child PTY
```

The live human path is not the Kameo actor path.

Input:

```text
terminal-cell-view stdin
  -> attach_stream.write_all(...)
  -> TerminalCellConnection::attach_viewer
  -> TerminalInputPort::accept(TerminalInput { source: Viewer })
  -> TerminalInputWriter
  -> TerminalInputGate
  -> child PTY writer
```

Programmatic input:

```text
terminal-cell-send
  -> SocketRequest::Input(TerminalInput { source: Programmatic })
  -> TerminalCellConnection::write_input
  -> TerminalInputPort
  -> TerminalInputWriter
  -> TerminalInputGate
  -> child PTY writer
```

Output:

```text
child PTY reader
  -> TerminalOutputPort
  -> TerminalOutputFanout
      -> attached viewer sockets first
      -> TerminalCell actor transcript append after that
```

Control:

```text
capture / wait / resize / exit
  -> socket request
  -> TerminalCell actor or side-channel port
```

So the answer to "does input pass through an actor?" is:

- Live attached keyboard input: **no**. It enters through the attached stream
  and `TerminalInputPort`, then reaches the dedicated `TerminalInputWriter`.
- Programmatic socket input: **also no** in the daemon path. It uses the same
  `TerminalInputPort`.
- The `TerminalCell` Kameo actor still owns lifecycle, transcript, resize,
  waiters, and exit state. It no longer exposes `Message<TerminalInput>`.

That last point matters. Before this pass, the code still had an in-process
`impl Message<TerminalInput> for TerminalCell` that forwarded to
`TerminalInputPort`. It was not the live Ghostty path, but it kept a misleading
actor-mailbox input route alive. I removed it and moved the witnesses to the
port.

## Why This Input Shape

The failed design routed visible terminal behavior through a higher-level relay:

```text
child PTY -> actor/transcript/subscription -> view stdout
view stdin -> socket request path -> child PTY
```

That made typing feel broken under real Pi TUI use. The fix was not "optimize
the relay"; the fix was to stop making the relay semantic.

The current path preserves the useful middle:

- daemon-owned child lifetime;
- durable transcript;
- programmatic input;
- input gate for non-interleaved injection;
- resize and exit observation;
- detachable/reattachable viewer.

But the middle does not interpret the live terminal. It moves bytes. Transcript,
screen projection, waiters, and actors observe around the hot path instead of
becoming the hot path.

The input gate belongs at the PTY writer because that is the one place shared by
all writers. When Persona injects a prompt, it can close human input, write a
contiguous byte sequence, then reopen human input and flush held human bytes.
Putting that gate in a viewer would leave other viewers or programmatic clients
outside the same rule.

## Changes Made In This Pass

Repository changes in `/git/github.com/LiGoldragon/terminal-cell`:

- Removed the actor-mailbox input route:
  `impl Message<TerminalInput> for TerminalCell` is gone.
- Added `TerminalInputWriter`, a data-bearing owner for the blocking PTY writer
  and `TerminalInputGate`.
- Updated session and agent terminal witnesses to inject through
  `TerminalInputPort` instead of `TerminalCell.ask(TerminalInput)`.
- Added `tests/production_witnesses.rs`, which spawns the real daemon and uses
  the real socket/client path to prove detach/reattach, single active viewer
  rejection, and slow-subscriber behavior.
- Exposed production witnesses through Nix as a stateful runner:
  `nix run .#production-witnesses`. They are not a pure flake check because
  they open a real PTY and the Nix build sandbox does not provide the needed
  host PTY device.
- Updated `ARCHITECTURE.md` and `skills.md` to document why live input uses the
  writer port rather than an actor mailbox.
- Removed obvious ZST method-holder shapes in the daemon/view/test helper code.

## Fit Against Workspace Discipline

**Daemon-first CLI:** good for this low-level component. CLIs are socket
clients; the daemon owns the child PTY and actor.

**Actor topology:** acceptable for the low-level terminal transport, incomplete
for the full production stack. The `TerminalCell` actor is a real data-bearing
Kameo actor. The raw PTY reader, PTY writer, output fanout, and per-connection
loops are blocking thread planes, not actors. That is intentional for this
low-level byte pump, but `persona-terminal` needs either an explicit
actor-supervised worker topology or a documented terminal-transport carve-out
that names exactly which blocking planes are allowed.

**Push-not-pull:** mostly good. Resize uses `SIGWINCH`; exit is pushed through
the child wait thread into actor state; transcript subscribers receive replay
plus live deltas. Session listing is a snapshot query over runtime directories,
not a live system state mechanism.

**Behavior on data-bearing types:** improved. The PTY writer is now
`TerminalInputWriter` with a writer and a gate. The daemon socket path and
viewer path no longer rely on hollow helper types for routine behavior.

**No-ZST rule:** better, not perfect under the strictest possible reading. The
obvious ZST method holders are gone. Remaining empty Kameo request message types
such as `TranscriptSnapshotRequest`, `TerminalExitRequest`, and
`WaitForTerminalExit` are type-level messages with no payload. They fit the
current Rust/Kameo skill carve-out, but if the workspace adopts an absolute
"every type carries runtime data" rule, these need a separate decision.

**Nix-backed witnesses:** improved. The production witnesses are real daemon
tests exposed through a named Nix app. They stay out of pure flake checks
because they require host PTY support. The other stateful witnesses remain
named Nix apps.

## Remaining Gaps

1. **Production registry is not here.**
   Runtime-directory files (`cell.sock`, pid files, `session.name`,
   `session.env`) are convenience metadata. They are not Sema. This is fine for
   `terminal-cell`; it must not become the production registry.

2. **Multiple viewers now have a first production policy.**
   The transport admits one active attached viewer. Extra viewers are closed
   rather than becoming extra human input writers. Production `persona-terminal`
   still needs the policy represented as a typed contract, but the low-level
   cell no longer silently accepts multiple human writers.

3. **The blocking IO planes are not supervised actors.**
   The input writer, output reader, fanout, and connection loops are named
   threads. That was the right move to prove the raw byte shape quickly, but
   production needs restart/error policy around those planes.

4. **The hardest manual witness is still human-observed.**
   The user confirmed the fixed path works. We still do not have a durable
   high-volume, lossless manual typing witness that proves keyboard latency
   under load.

5. **Session list/rename are shell apps.**
   They are useful, but they should remain local prototype tooling. In
   production these become typed requests to `persona-terminal` over its daemon
   socket, backed by Sema state.

## Recommendation

Freeze `terminal-cell` as the low-level evidence repo unless a specific witness
is missing.

The next architectural work should move upward into `persona-terminal`:

- one supervisor daemon;
- one Sema-owned session registry;
- typed create/list/rename/attach/detach/input/resize/close contracts;
- explicit active-viewer and writer-authority policy;
- terminal cells as supervised low-level PTY owners.

If work continues inside `terminal-cell`, keep it witness-oriented:

- prove high-volume output does not lag input;
- add a runtime witness that reattach chooses only live daemon sessions, not
  merely the newest socket path.

## Verification

Run on May 11, 2026:

```text
nix run .#production-witnesses  -> 3 passed
nix run .#session-witnesses     -> 4 passed
nix run .#agent-terminal-witness -> 2 passed
nix run .#daemon-witness        -> 6 passed
nix flake check                 -> all checks passed
nix run .#list-ghostty-agent-sessions -> no terminal-cell sessions under /run/user/1001/terminal-cell
```
