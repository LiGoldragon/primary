# Disconnect-survival job model for lojix S4 (up9q)

Read-only recon grounding the up9q work: make a deploy survive an SSH
disconnect across BOTH disconnect surfaces. Every claim below cites a
file read or command run. Nothing was mutated; no live deploy was run.

## Spirit availability — BLOCKER (not mine to fix)

The four requested lookups (`up9q`, `1lex`, `xv9v`, `kx32`) could not be
read. The `spirit` user daemon is down:
`systemctl --user status spirit-daemon.service` reports
`failed (Result: start-limit-hit)`; its `ExecStartPre`
(`/nix/store/6xdmjza2dpz2fgkn6i95hmmrnljh1vb0-spirit-startup-state`,
which runs `spirit-upgrade-store`) exits 1, so the socket
`/home/li/.local/state/spirit/spirit.sock` is never created and every
`spirit "(Lookup …)"` returns `transport IO error: No such file or
directory`. Restarting the unit (`reset-failed` + `start`) reproduces
the `ExecStartPre … status=1/FAILURE` immediately. This is a store-upgrade
failure on the Spirit daemon side, outside a read-only recon's scope —
flag for the operator / system-maintainer lane.

The up9q *design intent* is, however, fully recoverable from code: lojix
`INTENT.md:82-86` paraphrases it verbatim, and the `lojix-cli`
`systemd-run --collect` reference it ports is in-tree. The findings below
are grounded entirely in code, not memory.

## Up9q intent as captured in lojix INTENT.md

`/git/github.com/LiGoldragon/lojix/INTENT.md:82-86`:

> **Survives SSH disconnect.** A durable deploy is owned by a job actor
> that owns the external process and persists job state; process lifetime
> is decoupled from the request stream, so a dropped client does not
> abort the deploy. Per Spirit `up9q` (and the `lojix-cli` `systemd-run
> --collect` transient-unit reference it ports).

Two distinct properties are bundled there: (a) decouple the deploy from
the request stream (the client→daemon surface) via a job actor that owns
the process and persists job state; (b) port the `lojix-cli` `systemd-run
--collect` transient unit (the daemon→target surface).

## The two disconnect surfaces

1. **client → daemon** — the CLI/owner client holds the owner-socket
   connection open for the whole deploy and reads the single reply frame
   at the end. If that socket drops mid-deploy, today there is no actor
   that owns the deploy independently and no way to redeliver the reply.

2. **daemon → target** — the daemon activates the target by spawning a
   local `ssh <node> …` child process (see below). If the daemon's own
   SSH to the target drops mid-activation, the remote command — `nix-env
   --set` and (intended) `switch-to-configuration` — dies with the SSH
   channel, leaving the target half-activated.

## Is today's deploy connection-coupled? YES — fully inline in the request future

The whole deploy pipeline runs synchronously inside the single
owner-request future, and the reply is written only after the pipeline
finishes:

- `daemon.rs:275-290` `serve_owner` — reads ONE request frame
  (`read_body`), calls `execute_request(…)` which awaits the entire
  Nexus runner, then writes ONE reply frame back. One request → one reply,
  no intermediate reads, no separate job handle.
- `daemon.rs:321-338` `execute_with_store` builds a per-request
  `SchemaRuntime` and drives `engine.execute(work).await` — the runner's
  full continuation chain (submit → flake-auth → eval → build → copy →
  activate → record-activation, `schema_runtime.rs:129-130`) resolves
  inside that single `.await`. The reply (`ReplyToSignal`) is the runner's
  terminal action; there is no detached spawn around the deploy.
- `daemon.rs:223-235` `handle_connection` / `triad_runtime`
  `async_runtime.rs:961-972` `spawn_connection` — each connection is a
  `tokio::spawn`ed task, and the deploy lives ENTIRELY inside that
  connection task. The 64-permit cap (`daemon.rs:101,133`
  `MAXIMUM_CONCURRENT_REQUESTS`) gates concurrent connection tasks; a long
  deploy holds its permit for the whole run.

Consequence: the deploy is coupled to the connection task. Tokio doesn't
poll the read half mid-deploy, so a quiet client disconnect isn't
*detected* until the final write fails — but the deploy is still
strictly coupled: it holds a permit, has no persisted job identity, the
reply cannot be redelivered to a reconnecting client, and a daemon
restart mid-deploy loses the in-flight pipeline entirely (the durable
`Store` records only committed phase transitions, `lib.rs:359-432`, not a
resumable in-flight job). So while a passive drop won't *cancel* it,
nothing makes the deploy *survivable* in the up9q sense.

## Today's copy + activate are stubbed/unsafe AND non-survivable

`unsupported_deploy_reason` (`schema_runtime.rs:555-575`) is the
reject-guard: every activating System action (`Boot/Switch/Test/BootOnce`)
and every activating Home mode is rejected with
`UnsupportedDeployAction` — only `Eval`/`Build` pass. The comment states
copy/activate is "not yet target-safe."

The effect bodies exist but are unsafe:
- `run_copy_closure` (`schema_runtime.rs:1386-1398`) →
  `NixCommand::copy_closure` (`1886-1896`): `nix copy --to
  ssh-ng://<node> <closure>`. A plain local child; if the daemon's SSH
  drops, the copy aborts.
- `run_activate_generation` (`1400-1416`) →
  `NixCommand::activate_system` (`1898-1908`): `ssh <node> 'nix-env -p
  /nix/var/nix/profiles/system --set "$CLOSURE"'`. **Two bugs:** it
  references an unset `$CLOSURE` (the closure path is never passed), and
  it never runs `switch-to-configuration`, so it does not actually
  activate. And it is a bare `ssh`, not a transient unit — a dropped SSH
  kills the activation.
- `NixCommand::run` (`1917-1934`) is `tokio::process::Command…output().await`
  — a foreground child whose lifetime is bound to the request future.

## The triad-runtime job/actor primitive to use

`triad-runtime` re-exports the full kameo actor framework:
`/git/github.com/LiGoldragon/triad-runtime/src/lib.rs:22` `pub use kameo;`
(and `async_runtime.rs:15-18` uses `kameo::actor::{Actor, ActorRef,
Spawn}`, `kameo::message::{Context, Message}`, `kameo::reply`). The only
existing `impl Actor` is `RequestGate` (`async_runtime.rs:386`), used
solely for admission permits — there is no job/background-task actor today.
lojix spawns deploys **inline in the request future**, never detached.

So the up9q job primitive is a **kameo actor** (`spawn`/`spawn_link`,
mailbox, `ask`/`tell`) owned by the daemon's `LojixRuntime` (not by a
connection task), holding the deploy's `ActorRef`. It owns the external
process and a durable job row in the sema `Store`. `tokio::spawn` is the
lower-level fallback, but kameo is the in-house, already-exported,
supervised choice and matches the INTENT.md "job actor" wording.

## Concrete up9q-compliant design

**Surface (a) client → daemon — decouple the deploy from the request stream.**
On `Deploy`, the owner request should NOT run the pipeline inline. Instead
`LojixRuntime` spawns a long-lived **deploy job actor** (kameo `ActorRef`
held on the runtime, not the connection worker) that owns the pipeline and
persists job state to a new durable sema table (a `DeployJob` family
alongside the four in `lib.rs:44-61`: job id, phase cursor mirroring
`DeployStage` `schema_runtime.rs:131-142`, closure path, target). The
owner request returns *immediately* with a `DeployAccepted`-style reply
carrying the job id; the client then observes progress/result via the
existing subscription/`Watch` surface (or a `Lookup` by job id). A dropped
client kills only the short request task, never the job actor. On daemon
restart, the persisted job row makes the in-flight deploy resumable
(the same self-resume discipline as `oh9l`/`ur16`, `lib.rs:11-16`).
Kill-on-drop is thereby explicitly *off* for the job — that is the whole
point of the decoupling.

**Surface (b) daemon → target — run activation as a target-side transient unit.**
Port the `lojix-cli` pattern (`/git/github.com/LiGoldragon/lojix-cli/src/activate.rs:128-147`):
wrap the remote activation in `systemd-run --unit=<deploy-unit>
--collect --service-type=oneshot /bin/sh -c '<script>'` over SSH. PID 1 on
the target owns the unit, so a daemon→target SSH drop leaves it running to
completion; `--collect` reaps the finished transient unit. The activation
script must do what `activate.rs:92-126`/`62-63` do and the current stub
does NOT: pass the real closure path (fix the unset `$CLOSURE` bug,
`schema_runtime.rs:1898-1908`) and run `switch-to-configuration <action>`.
For live feedback keep `--wait` (ssh streams output and exits with the
unit's code, `activate.rs:128-134`); recovery after an SSH drop is
re-attaching via `ssh <target> journalctl -u <unit>.service`. The
deploy job actor records the unit name so a resumed job can poll the unit
rather than blindly re-running activation. (`nix copy`,
`schema_runtime.rs:1886-1896`, is idempotent and re-runnable, so it does
not itself need a transient unit — only the activation does.)

The two surfaces compose: (a) makes the deploy outlive the *client*
connection and the *daemon* process (job actor + persisted job state);
(b) makes the *remote activation* outlive the daemon→target SSH (target
transient unit). Both are required; neither alone satisfies up9q.
