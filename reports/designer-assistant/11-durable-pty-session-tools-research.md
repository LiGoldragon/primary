# Durable PTY Session Tools Research

Role: designer-assistant research sidecar.

Question: which existing tools or libraries provide durable PTY session ownership, transcript or scrollback capture, and attach/detach, with preference for minimal non-tmux abstractions?

Conclusion: no surveyed existing tool cleanly satisfies all four requirements while staying a minimal non-multiplexer abstraction:

1. child survives viewer death,
2. programmatic input,
3. programmatic output transcript including detached periods,
4. minimal abstraction, not a full terminal multiplexer.

The closest fit depends on which requirement is allowed to move:

- If minimal detach is primary: `abduco` or `dtach` are the right shape, but they deliberately do not own transcript or scrollback.
- If native scrollback plus simple persistence is primary: `shpool` is the closest user-facing tool, but it does not expose a durable append-only transcript API.
- If programmatic control and output capture are primary: Zellij now has the strongest off-the-shelf surface, but it is a full terminal workspace/multiplexer.
- If building a small purpose-specific component is acceptable: a Rust daemon using `portable-pty` plus an append-only output log is the cleanest way to satisfy all four.

## Requirement Matrix

| Candidate | Child survives viewer death | Programmatic input | Output transcript including detached periods | Minimal non-mux |
|---|---:|---:|---:|---:|
| `abduco` | Yes | Partial through attach/socket, not a stable API | No | Yes |
| `dtach` | Yes | Partial through attach/socket, not a stable API | No | Yes |
| `shpool` | Yes | Mostly interactive CLI, single attached client | Partial current rendered state, not durable transcript | Yes-ish |
| `script` / `ttyrec` / `asciinema` | No, recorder owns child lifecycle | Yes while recording | Yes while recorder lives | Yes |
| `tmate` | Yes | Yes through tmux semantics | tmux-style screen state, not minimal transcript | No |
| Zellij | Yes | Yes | Snapshot/stream and scrollback buffer; durable session serialization optional | No |
| `ttyd` / WeTTY | Browser transport, not durable ownership | Yes through websocket/browser | No durable detached transcript by default | Yes-ish transport, not session layer |
| Rust `portable-pty` | Only if wrapped in daemon | Yes | Only if implemented | Yes as library |
| Rust `expectrl` / `rexpect` | No durable ownership by itself | Yes | Buffered live output, not detached ownership | Yes as automation library |

## Findings

### `abduco`

Primary source: `abduco` README, https://raw.githubusercontent.com/martanne/abduco/master/README.md

`abduco` is a minimal session attach/detach tool. Its README says it lets programs run independently from the controlling terminal, detach into the background, and later reattach. It explicitly positions itself as a simpler alternative to tmux/screen when paired with `dvtm`, and as similar to `dtach`.

Important evidence:

- create and attach: `abduco -c session-name your-application`
- detach: `CTRL-\`
- reattach: `abduco -a demo`
- list sessions with client/terminated state
- read-only attach mode ignores keyboard input

Assessment:

- Satisfies child survivability and minimal abstraction.
- Does not satisfy transcript/scrollback. The design is relay-like; it does not provide a durable output log or scrollback API.
- Programmatic input is possible only indirectly by writing through an attached client/socket path. That is not a stable, documented control protocol.

### `dtach`

Primary source: project page, https://dtach.sourceforge.net/

`dtach` is the strongest example of the minimal detach-only shape. Its project page says it emulates screen's detach feature, protects a program from its controlling terminal, and allows later attach. It also states the key limitation: it does not track screen contents, so it works best with programs that can redraw themselves.

Assessment:

- Satisfies child survivability and minimal abstraction.
- Does not satisfy transcript/scrollback by design.
- Programmatic input is not a first-class API. It can relay bytes through an attached client, but there is no documented command/control surface for structured input and output capture.

### `shpool`

Primary source: `shpool` README, https://raw.githubusercontent.com/shell-pool/shpool/master/README.md

`shpool` is the most relevant user-facing non-tmux tool. It is a daemon that owns named shell sessions so they survive dropped connections. It explicitly says it is lighter than tmux/screen, only provides persistent sessions, and preserves native terminal scrollback/copy-paste because output is sent directly to the local terminal.

Important evidence:

- `shpool attach main` creates or reattaches to a named shell session.
- `shpool detach main` detaches without stopping the session.
- The daemon owns subshells in a table.
- Unlike `dtach`/`abduco`, it maintains an in-memory terminal render and redraws on reattach, including output generated after the connection dropped.
- It allows only one connected client per session.

Assessment:

- Satisfies child survivability.
- Mostly satisfies minimal abstraction; it is a persistence daemon, not a window/pane multiplexer.
- Does not satisfy durable transcript. It preserves native local scrollback while attached and keeps an in-memory render for reattach, but the README does not expose an append-only transcript or programmatic output stream that includes all detached output.
- Programmatic input is not the target surface. It is designed around interactive attach, not a documented automation API.

### `script`, `ttyrec`, `asciinema`

Primary sources:

- util-linux `script` help: https://www.kali.org/tools/util-linux/
- `ttyrec` compatible implementation README: https://github.com/ovh/ovh-ttyrec
- asciinema docs: https://docs.asciinema.org/manual/cli/usage/ and https://docs.asciinema.org/how-it-works/

These tools solve recording, not durable ownership. `script` can log stdin, stdout, combined I/O, and timing. `ttyrec` records a terminal session with timing for playback. `asciinema` records raw terminal output in asciicast format and can optionally capture input.

Assessment:

- Satisfy transcript capture while the recorder process is alive.
- Do not satisfy child survival after viewer/recorder death. The recorder is the PTY master. When it dies, the recording/control process dies and the child normally loses its PTY master.
- They are useful as subcomponents or wrappers around a durable owner, but not a complete answer.

### `tmate`

Primary source: project page, https://tmate.io/

`tmate` is a fork of tmux for instant terminal sharing. It supports shared and read-only terminal access and uses tmux configuration syntax.

Assessment:

- Satisfies child survivability and programmatic/shared input through tmux-like semantics.
- Does not satisfy the minimal non-mux criterion. It inherits tmux's terminal server/multiplexer model.
- It is optimized for sharing and NAT traversal, not local minimal durable PTY ownership with transcript.

### Zellij

Primary sources:

- Programmatic control: https://zellij.dev/documentation/programmatic-control.html
- Options: https://zellij.dev/documentation/options
- Session resurrection: https://zellij.dev/documentation/session-resurrection.html

Zellij has the richest programmatic surface of the surveyed tools. Its programmatic-control docs include:

- headless session creation with `zellij attach --create-background`,
- input actions such as `write-chars`, `write`, `paste`, and `send-keys`,
- output observation with `subscribe` as real-time raw text or NDJSON rendered viewport content,
- `dump-screen --full` for point-in-time viewport/scrollback snapshots.

Its options include default detach on force close and a configurable scrollback buffer. Its resurrection docs describe serialized session layout, command resurrection, and optional viewport/scrollback serialization.

Assessment:

- Satisfies child survivability under normal detach/close settings.
- Satisfies programmatic input.
- Partially satisfies programmatic output. It can stream rendered pane content and dump scrollback snapshots, but this is viewport/rendered terminal state, not necessarily an append-only byte transcript. It can serialize scrollback for resurrection, but that is not the same as a durable transcript API.
- Fails the minimal non-mux criterion. Zellij is a terminal workspace/multiplexer with panes, tabs, plugins, layouts, and UI semantics.

### `ttyd` and WeTTY

Primary sources:

- `ttyd` README: https://raw.githubusercontent.com/tsl0922/ttyd/main/README.md
- WeTTY README: https://github.com/butlerx/wetty

Both are web terminal transports. `ttyd` shares a command over the web and supports browser terminal features. WeTTY provides terminal access in a browser over HTTP/HTTPS, normally launching login or SSH.

Assessment:

- They are access layers, not durable PTY ownership layers.
- They can carry programmatic input/output over websocket, but do not by themselves define detached session survival with transcript capture across disconnected periods.
- They could front a durable owner, but they are not the owner.

### Rust Libraries

Primary sources:

- `portable-pty`: https://docs.rs/portable-pty/latest/portable_pty/
- `portable-pty` `MasterPty`: https://docs.rs/portable-pty/latest/portable_pty/trait.MasterPty.html
- `expectrl`: https://github.com/zhiburt/expectrl
- `rexpect`: https://docs.rs/rexpect/latest/rexpect/

`portable-pty` provides a cross-platform PTY interface. Its `MasterPty` exposes a cloneable reader for slave output and a writer for input to the slave. This is enough to build the desired durable owner: a daemon owns the PTY master and child, appends every byte read from the PTY to a log, accepts input over a local socket, and allows attach/detach viewers to subscribe to live output plus replay log ranges.

`expectrl` and `rexpect` are automation libraries. They spawn and control interactive processes in a PTY and provide expect-style matching/sending. They are good for a single controlling program, but they do not provide durable detached ownership by themselves.

Assessment:

- `portable-pty` is a good primitive, not a finished session manager.
- `expectrl`/`rexpect` are useful for automation, not durable attach/detach ownership.

## Design Implication

The four requirements describe a small daemon, not a terminal recorder and not a terminal multiplexer:

- one long-lived owner per session,
- one child process group attached to a PTY slave,
- one PTY master reader that never stops while the child lives,
- append-only transcript storage from the master reader,
- a local command socket for input, resize, attach, detach, and transcript read,
- optional live subscribers fed from the same byte stream.

Existing minimal detach tools intentionally avoid owning scrollback/transcript. Existing recorder tools own the PTY but are not durable detached session managers. Existing programmatic tools with enough observability become multiplexers. Therefore the clean answer is to build the small owner directly, most likely in Rust on `portable-pty`, borrowing user-facing ideas from `abduco`/`dtach` and persistence ergonomics from `shpool`.

