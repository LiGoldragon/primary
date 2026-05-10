# 13 - Terminal Cell Relay Architecture Failure

Role: designer-assistant.

Date: May 11, 2026.

## Verdict

The current `terminal-cell-view` architecture should be rejected for live human
agent harness use.

It is not merely under-optimized. It puts an application-level relay between
the user's terminal and the agent TUI, then tries to recover terminal behavior
through socket framing, actor messages, transcript replay, and subscription
delivery. That is the same class of mistake the workspace wanted to avoid in
tmux-style systems: a middle layer starts acting like a terminal policy engine
instead of staying a byte path.

The prototype still has useful pieces:

- daemon-owned child PTY lifecycle;
- real Pi launch under Ghostty;
- transcript capture;
- programmatic input injection;
- child-exit observation;
- resize plumbing.

But the live viewer architecture is wrong.

## Evidence

Manual Pi tests on May 10-11, 2026:

- The full Pi TUI rendered in Ghostty.
- Typing was extremely slow, initially around multi-second delay.
- Switching viewer input from one socket request per stdin read to one
  persistent input stream improved the symptom only slightly.
- Most keypresses still did not appear.
- After a short period, input effectively stopped appearing.

That symptom pattern means the live terminal path is not trustworthy. It does
not matter that deterministic witnesses pass; they test the harness adapter and
socket control paths, not human TUI quality under real terminal behavior.

## Root Mistake

The failed path is:

```text
keyboard
  -> Ghostty PTY
  -> terminal-cell-view stdin
  -> terminal-cell socket protocol
  -> daemon connection handler
  -> terminal input queue
  -> child PTY

child PTY
  -> daemon PTY reader
  -> actor/transcript/subscriber path
  -> daemon socket protocol
  -> terminal-cell-view stdout
  -> Ghostty render
```

Even after making input persistent, output still flows through the transcript
subscription model. That means the echo for human typing depends on the
transcript delivery path. When a TUI emits many small writes, the hot path is
competing with actor scheduling, subscriber delivery, replay concerns, and
control-plane requests.

This is the wrong abstraction boundary.

## Do We Need Anything In The Middle?

For a normal terminal, no:

```text
keyboard -> terminal emulator PTY -> application
application -> terminal emulator PTY -> display
```

That is the ideal live path.

Persona needs something in the middle only because it wants properties a plain
GUI terminal does not provide:

- the child survives the GUI terminal closing;
- transcript exists while detached;
- Persona can inject bytes programmatically;
- Persona can observe output/usage;
- a later viewer can attach.

So the middle exists for durability and observability, not for live terminal
policy.

The middle must therefore be an abduco-like byte broker, not a terminal UI
relay.

## Replacement Architecture

The next shape should be:

```text
Ghostty tty <-> attach pump <-> daemon byte pump <-> child PTY
                                  |
                                  +-> transcript recorder
                                  +-> actor/control plane
                                  +-> programmatic input port
```

Hot path rules:

- Human keyboard bytes go to the child PTY as raw bytes.
- Child PTY output goes to the active viewer as raw bytes.
- The hot path does not call actor handlers.
- The hot path does not interpret terminal semantics, replay transcripts as
  display state, or make terminal bytes wait on a semantic protocol.
- Minimal framing for content, attach, detach, resize, exit, and lifecycle
  messages is allowed.
- The hot path does not wait for transcript append, screen projection, waiters,
  or Persona decisions.
- Transcript capture observes the PTY output stream as a side effect.
- Programmatic input writes to the same child PTY input path but does not
  replace human input semantics.

The actor remains valuable, but not as the live byte path. It owns lifecycle,
metadata, health, resize, child-exit observation, waiters, and control-plane
decisions.

## What Abduco Does Right

I cloned and read `/git/github.com/martanne/abduco` after the manual
`terminal-cell-view` failure.

The important files are:

- `/git/github.com/martanne/abduco/client.c`
- `/git/github.com/martanne/abduco/server.c`
- `/git/github.com/martanne/abduco/abduco.c`
- `/git/github.com/martanne/abduco/abduco.1`

Abduco does have a small protocol. It is not literally the terminal connected
directly to the application. But for live content, the protocol is intentionally
thin:

```c
enum PacketType {
    MSG_CONTENT = 0,
    MSG_ATTACH  = 1,
    MSG_DETACH  = 2,
    MSG_RESIZE  = 3,
    MSG_EXIT    = 4,
    MSG_PID     = 5,
};
```

`client.c` puts the attaching terminal into raw mode, then uses `pselect` over
only two descriptors:

- `STDIN_FILENO`;
- the Unix socket connected to the abduco server.

When stdin is readable, it reads raw bytes into a packet and sends
`MSG_CONTENT` to the server. The only live-input policy is:

- detach key;
- redraw key;
- read-only client mode.

When the server socket is readable, it receives `MSG_CONTENT` and writes the
bytes directly to stdout.

`server.c` similarly uses `select` over:

- the listening socket;
- the child PTY;
- connected client sockets.

When the PTY is readable, the server reads bytes from the PTY and sends the
same `MSG_CONTENT` packet to attached clients. When a client socket sends
`MSG_CONTENT`, the server writes the bytes directly to the PTY.

That is the whole live path:

```text
client stdin -> MSG_CONTENT -> server socket -> child PTY
child PTY -> MSG_CONTENT -> client socket -> client stdout
```

No actor.

No transcript replay as live display.

No screen projection.

No terminal escape interpretation.

No per-key request/reply.

No "wait until transcript accepted this byte".

Abduco's man page is explicit about the boundary: it operates on the raw I/O
byte stream and does not interpret terminal escape sequences. It also says
terminal state is not preserved across sessions; if state preservation is
needed, another utility such as `dvtm` should provide it.

This is the design lesson for Persona: the hot path is allowed to have a
minimal packet wrapper, but not a semantic terminal layer.

## Where Persona Extends Abduco

Persona wants more than abduco:

- transcript capture while detached;
- programmatic input;
- usage/availability probes;
- typed actor supervision;
- health and recovery;
- possibly multiple supported attach frontends.

Those extensions should attach beside the abduco-like pump, not inside the
human byte path.

A better daemon split:

```text
                         +-> transcript append
child PTY read pump -----+-> active attach client socket(s)
                         +-> observer parser / prompt-state recognizer

human attach client -----> child PTY write pump
Persona injection -------> child PTY write pump
actor/control plane -----> resize, lifecycle, health, session metadata
```

The transcript writer must not block attached live display. The observer parser
must not block attached live display. Actor mailboxes must not block attached
live display.

If a transcript sink is slow, live display continues and the transcript sink
either catches up from an internal queue or records an explicit loss/error
event. It must never make human input feel broken.

## Terminal / Multiplexer Frontends

We do not have to support only one frontend.

Candidate frontends:

- a tiny abduco-like attach client run inside Ghostty;
- direct abduco interop for manual containment sessions;
- a terminal emulator with an explicit programmatic control API, if one is
  good enough;
- a browser/GUI terminal frontend later, if it can preserve raw byte behavior.

The invariant is not "no frontend layer." The invariant is:

> The live frontend layer must be a raw byte transport with only detach,
> resize, attach, and lifecycle framing. It must not become the terminal
> semantics engine.

If a terminal emulator provides clean programmatic input/output APIs, it can be
supported as one frontend. If it forces Persona to route human keyboard input
through an application-level relay, it is the wrong frontend for live harness
work.

## Next Experiment

The next Terminal Cell experiment should be named around the thing it proves:
an abduco-shaped attach path.

Minimum useful shape:

```text
terminal-cell-attach
  stdin  -> Content packet -> daemon socket -> child PTY
  stdout <- Content packet <- daemon socket <- child PTY

terminal-cell-daemon
  child PTY read pump -> attached clients
                      -> non-blocking transcript queue
                      -> observer queue
  attached clients and Persona injection -> input gate -> child PTY write pump
```

The input gate is the right place for the multiple-writer problem. Before
Persona injects a prompt or slash command, it can close the gate to attached
human input, write its bytes contiguously to the child PTY, then reopen the
gate. The gate is not a parser and not a harness-state engine. It only
arbitrates writers to the one PTY input stream.

Two policies are viable:

- buffer blocked human bytes and release them after the injection;
- reject blocked human bytes with an explicit "input gate closed" event so the
  frontend can avoid pretending input was accepted.

The choice belongs to the UX layer, but the gate itself belongs at the PTY
writer, not in the viewer. Putting it at the writer means every frontend and
every programmatic injector shares the same serialization rule.

Required witnesses:

- A manual Pi TUI session in Ghostty accepts human typing immediately and
  losslessly.
- The same session still accepts Persona programmatic input.
- A gated Persona injection cannot interleave with simultaneous human typing.
- A high-volume output fixture does not make keyboard input lag.
- A deliberately slow transcript sink does not affect the attached viewer.
- The live byte path can be inspected in code without finding an actor mailbox,
  screen projection, transcript replay, or wait condition between stdin and the
  child PTY.

The current `terminal-cell-view` tests are still useful as negative history and
for harness launch details. They are not sufficient acceptance tests for the
next architecture.

## Attach Model

The GUI terminal still needs a tiny command because Ghostty starts a process
inside its own PTY. That command should be closer to `abduco -a` than to
`terminal-cell-view`.

Its job:

```text
local tty raw mode <-> daemon attach socket
```

It should not:

- replay transcript by itself;
- subscribe to transcript deltas as its live display source;
- parse terminal escape sequences;
- know about actors;
- know about waits, captures, or Persona messages.

If scrollback replay is needed on attach, the daemon can write replay bytes to
the attach socket before switching that socket into live pumping. That replay
must be part of the daemon's byte pump protocol, not a separate display client
that renders transcript subscriptions.

## What To Retire

Do not continue improving these as the live Pi attach path:

- `terminal-cell-view` as a transcript subscriber;
- per-request or framed viewer input for keyboard bytes;
- actor mailbox delivery of every PTY output chunk;
- live display sourced from `TranscriptSubscription`;
- witnesses that prove a prompt can be injected but do not prove manual typing
  is responsive and lossless.

Those can remain as diagnostic tools only until the next architecture replaces
them.

## Decision

Stop extending the current viewer/subscriber design for live human use.

Keep the useful constraints:

- daemon-owned PTY;
- durable child process;
- transcript capture;
- programmatic input;
- resize;
- child-exit observation.

Replace the live attach path with an abduco-like byte pump. Actors and typed
messages remain the correct shape for lifecycle and Persona control, but the
human terminal path must be a direct raw-content transport with only minimal
session framing around it.

## Next Prototype Test

The next prototype should be judged by a harsh interactive witness:

1. Launch real Pi under the daemon-owned PTY.
2. Attach Ghostty through the byte-pump attach command.
3. Use compositor-injected keyboard input or a real manual test.
4. Send a long mixed string quickly.
5. Assert that every byte appears in the Pi draft promptly.
6. While the user types, make Pi or a fixture emit high-volume output.
7. Assert input remains lossless and visible.

If this test is not good, the design is still wrong.

## Correction To Earlier Report

`reports/designer-assistant/12-terminal-cell-owner-spike.md` was too optimistic.
It correctly identified that `abduco` is closer to the desired shape than tmux,
but it allowed `terminal-cell-view` to become an application-level relay. That
was the wrong conclusion.

The durable lesson is narrower:

> Own the PTY and transcript, but keep the live terminal path as close to raw
> bytes as possible.
