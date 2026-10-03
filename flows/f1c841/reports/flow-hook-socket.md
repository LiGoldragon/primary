# flow-hook reports to its launching Nexus

Verdict: **landed and green; nothing deployed.** flow 0.23.0 exports the
launching Nexus's ordinary socket into every Claude launch pane as
`FLOW_SOCKET`; flow-test's `flow-claude-hook` now runs its Nexus in the next
slot's layout and the launched flow's events land in that Nexus's Memory.

## Versions

| repo | before | after |
|---|---|---|
| flow | 0.22.0 `2fa51db8` | 0.23.0 `636214e5` (main) |
| flow-test | `36c8d2ca` (input flow `2fa51db8`) | `b18ce4ea` (main; `flake.nix` URL and lock pin flow `636214e5`) |

No wire, store or contract change: signal-flow 10.0.0 and meta-signal-flow
14.0.0 are untouched. UPGRADES.md has a `# Flow 0.23.0` entry.

## How the socket reaches the hook

1. `RunningNexus::open` reads `ordinary_socket_path` from its store's
   configuration (the socket it is about to serve; a meta `Configure` of the
   sockets still takes effect only on restart) and hands it to `HerdrCli`
   (`with_ordinary_socket`, new field `ordinary_socket`).
2. Spawn's pane preparation line (`claude_environment_preparation`) now reads:

       unset CLAUDE_CODE_CHILD_SESSION CLAUDE_JOB_DIR CLAUDE_CODE_SESSION_ID CLAUDE_CODE_SESSION_KIND FLOW_ID && export FLOW_SOCKET='<socket>' && export FLOW_ID=<id> && printf 'FLOW_CLAUDE_ENV_READY_%s\n' <marker>

   The path is single-quoted for the shell (new `QuotesForShell`). It is
   exported for every Claude launch, reserved or not.
3. The harness starts at that prompt and inherits it; Claude runs `flow-hook`
   with its environment; `flow-hook` runs the `flow` beside it, which already
   read `FLOW_SOCKET` before its default (`crates/flow/src/main.rs`). No
   change was needed in `flow-hook` or `flow`.
4. A harness started by hand has no `FLOW_SOCKET` and reaches
   `$XDG_RUNTIME_DIR/flow/flow.sock` as before (the existing
   `default_socket.rs` test still holds).

Why the pane environment and not `--settings`: the value is the launching
Nexus's, like `FLOW_ID`, and rides the same channel; it is harness-neutral;
and a seat's own `flow` calls then reach the same Nexus as its hook.

## Tests

flow (`cargo test --workspace`, clippy `-D warnings`, fmt, `nix flake check
path:.` and `nix flake check github:LiGoldragon/flow/636214e5`: all green).
Three new tests, each a Nix exact check:

- `flow-launch-exports-its-nexus-socket`: the preparation line, run by `sh`
  with a foreign inherited `FLOW_SOCKET`, gives a child the path
  `/run/user/1001/flow-next/it's a $HOME/flow.sock` exactly.
- `flow-launch-socket-from-the-store`: `RunningNexus::open` under a
  `run/flow-next` runtime directory carries `run/flow-next/flow/flow.sock`;
  after the store is configured to another path and reopened, it carries that
  one.
- `flow-hook-reports-to-its-launching-nexus`: the `flow-hook` binary with
  `FLOW_SOCKET` naming a fixture Nexus under `run/flow-next/flow/` and no
  socket under its `XDG_RUNTIME_DIR` delivers `Report.{ 5a4d0b Stopped }` there
  and logs `Stop\tReport.{ «5a4d0b» Stopped }\t0\tReported`.

Seen failing once: with `with_ordinary_socket` a no-op and the quoting
removed, four tests failed (the first assertion showed
`left: "/run/user/1001/flow/flow.sock"`); with `flow` reading another
variable name, the hook test failed with `the hook reached the launching
Nexus: Empty`. The two existing launch tests now also assert the export.

flow-test: `flow` and `flow-populated-store` (checks) and the lint are green
locally and on `github:LiGoldragon/flow-test/b18ce4ea`; `flow-claude-hook`
was red once on flow 0.22.0, green with `--override-input` on the local
0.23.0 tree, and green from the pushed rev.

## The scenario

`packages/flow-claude-hook.nix`: the Nexus starts with
`XDG_RUNTIME_DIR=$root/run/flow-next` and so serves
`$root/run/flow-next/flow/`; the script then goes back to
`XDG_RUNTIME_DIR=$root/run`. The fixture Herdr
(`lib/components/herdr-fixture.nix`) gives the pane's shell
`FIXTURE_HERDR_RUNTIME_DIR` (`$root/run`, the Herdr server's) and removes any
`FLOW_SOCKET`. Steps 1-6 name the Nexus to their clients and the hand-run
harness explicitly. Step 7 adds three checks: the harness's runtime directory
is the pane's, `$root/run/flow/flow.sock` does not exist, and the harness's
`FLOW_SOCKET` is the launching Nexus's socket; the existing check that
`ReadEvents` holds Started, ToolUsed.Bash, Stopped for the launched FlowId is
the witness.

Red, on flow 0.22.0 (`witnesses/flow-claude-hook-socket.red.run.txt`): this
is the morning plan's inferred consequence, now seen in the sandbox (not on
the live host):

    harness: FLOW_SOCKET , XDG_RUNTIME_DIR /tmp/fh-MN6DLyy0/run
    green: the default stable socket /tmp/fh-MN6DLyy0/run/flow/flow.sock does not exist
    red: the harness's FLOW_SOCKET is the socket of the Nexus that launched it (/tmp/fh-MN6DLyy0/run/flow-next/flow/flow.sock)
    ReadEvents.aa4ca6 after the launched run: EventsRead.{ aa4ca6 [] }
    red: the Nexus holds Started first, ToolUsed.Bash, Stopped last for the launched aa4ca6
    flow-claude-hook: red

Green, from the pushed rev `b18ce4ea`
(`witnesses/flow-claude-hook-socket.green-pushed.run.txt`; the local run is
`…green-local.run.txt`):

    flow-nexus serves /tmp/fh-l6hZFqq3/run/flow-next/flow/flow.sock; the pane's runtime directory is /tmp/fh-l6hZFqq3/run
    unset CLAUDE_CODE_CHILD_SESSION CLAUDE_JOB_DIR CLAUDE_CODE_SESSION_ID CLAUDE_CODE_SESSION_KIND FLOW_ID && export FLOW_SOCKET='/tmp/fh-l6hZFqq3/run/flow-next/flow/flow.sock' && export FLOW_ID=aa4ca6 && printf 'FLOW_CLAUDE_ENV_READY_%s\n' 5583b297…
    harness: FLOW_SOCKET /tmp/fh-l6hZFqq3/run/flow-next/flow/flow.sock, XDG_RUNTIME_DIR /tmp/fh-l6hZFqq3/run
    green: the default stable socket /tmp/fh-l6hZFqq3/run/flow/flow.sock does not exist
    green: the harness's FLOW_SOCKET is the socket of the Nexus that launched it (/tmp/fh-l6hZFqq3/run/flow-next/flow/flow.sock)
    ReadEvents.aa4ca6 after the launched run: EventsRead.{ aa4ca6 [ Started ToolUsed.Bash Stopped ] }
    green: the Nexus holds Started first, ToolUsed.Bash, Stopped last for the launched aa4ca6
    flow-claude-hook: green

## Red, and open

- **Not deployed.** The live next slot is still flow 0.17.4. For the morning
  plan, 0.23.0 should replace 0.22.0 as the `flow-next` pin. Then a seat that
  the next Nexus launches reports to that Nexus even after the stable one is
  retired. Flows launched before the restart keep their old environment.
- **A seat's own `flow` calls move too.** A Claude seat launched by the next
  Nexus that runs plain `flow` now reaches the next Nexus, where before it
  reached `$XDG_RUNTIME_DIR/flow/flow.sock`. This is intended, but it is a
  behaviour change. A wrapper that sets its own socket still overrides it.
- **Codex panes get no `FLOW_SOCKET`.** Codex runs no `flow-hook`, and its
  launch path has no pane preparation line.
- **The launch is the stand-in's.** As before, the fixture Herdr stops the
  Start at Title (`StartRejected.BindingRefused`). The pane is a shell the
  fixture runs, not a Herdr pane.
- The same session id `aa4ca62b…` came up in both runs. This is the known
  open issue: the session is a pure function of the launch request id.

## Vision conflicts seen

- **vision-nexus says a CLI takes one inline datom and no flags.** The Nexus
  is chosen through the environment (`FLOW_SOCKET`), which is not a flag,
  and the CLI still speaks to exactly one Nexus. But the environment is a
  channel the vision does not name.
- **vision-nexus says a Nexus knows its caller by the process, never by a
  claim.** The hook's Report still carries `FLOW_ID` from the environment,
  which is a claim. This is unchanged from 0.21.0.
- **vision-flow says Flow chooses a flow's system prompt, entry files and
  first prompt.** The socket rides in neither the entry files nor
  `--settings`. It rides in the pane environment, as `FLOW_ID` does.
- **vision-flow says Flow knows each flow's state through hooks without
  polling.** This now holds for flows launched by either slot. `ReadEvents`
  is still a point read, not a subscription.

## Sources

- `/git/github.com/LiGoldragon/flow` at `2fa51db8` and `636214e5`:
  `crates/flow-nexus/src/{herdr.rs, herdr/launch.rs, lib.rs,
  tests/launching_nexus.rs}`, `crates/flow/{src/main.rs, src/hook.rs,
  tests/hook_socket.rs}`, `UPGRADES.md`, `DESIGN.md`, `README.md`,
  `flake.nix`
- `/git/github.com/LiGoldragon/flow-test` at `36c8d2ca` and `b18ce4ea`:
  `packages/flow-claude-hook.nix`, `lib/components/herdr-fixture.nix`,
  `lib/components/flow.nix`
- `/home/li/primary/flows/f1c841/witnesses/flow-claude-hook-socket.{red,green-local,green-pushed}.run.txt`
- `/home/li/primary/flows/f1c841/reports/{flow-report-memory,morning-deploy-final}.md`
- Skills: vision-flow, vision-nexus, knowledge-flow, knowledge-nexus,
  claude-harness, compensation-nix, testing, versioning
