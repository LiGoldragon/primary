# Flow 0.17.4 disposable starts: Phase 1 gate (STOPPED)

Method: read-only Bash probes from the harness-native child (Sonnet 5), 2026-09-26. Phase 2 not run; nothing started, no state created.

- (a) HERDR_ENV: WITNESSED. HERDR_ENV=1, HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock (srw------- socket exists), pane w1:pF, tab w1:tD, workspace w1. Liveness of the session not queried.
- (b) FLOW_ID/FLOW_DIRECTORY in env: ABSENT. `env | grep ^FLOW` empty. Values exist only in the brief text (38f337, flows/38f337).
- (c) TTY: ABSENT. `tty` = "not a tty"; stdin not a tty; `: </dev/tty` fails "no such device or address".
- (d) Scratch FLOW_SOCKET: NOT PROVED. No FLOW_SOCKET in env. Production runtime dirs exist under $XDG_RUNTIME_DIR (flow, flow-next). Scratch socket not attempted because the CLI below is not 0.17.4.
- (e) Budget: NOT SET. Proposed: claude-sonnet-5, medium, 3 Starts, but per-Start turn/token cap and wall-clock timeout are not stated in the brief and Flow's flags for them are unknown.
- CLI: `flow` on PATH is /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow, `flow --version` = 0.12.2, NOT 0.17.4. It takes a single typed query argument (`--help` is rejected as an invalid Query), so typed Stop/List syntax is undiscovered.

Needed: a Flow 0.17.4 binary path; FLOW_ID/FLOW_DIRECTORY exported (or authorization to pass explicitly); a pty for the Start (a pane-attached shell or `script`/pty wrapper authorized); the scratch socket flag/env of 0.17.4; explicit per-Start turn/token cap and timeout.
