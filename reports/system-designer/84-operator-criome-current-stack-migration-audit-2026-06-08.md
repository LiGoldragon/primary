---
title: 84 — audit — operator's criome current-stack migration (in flight)
role: system-designer
variant: Audit
date: 2026-06-08
topics: [criome, sema-engine, signal-frame, triad-main, daemon-binary-startup, two-contract, migration-audit, operator-review]
description: |
  Read-only audit of the main operator lane's in-flight criome port (bead
  primary-ffew, "current-stack sema-engine migration audit and unblocked
  port"). Four commits move criome off sema/signal-core/nota-codec onto
  sema-engine/signal-frame/nota-next + triad-runtime, split a binary-only
  rkyv-config daemon, and drop clap. The migration is disciplined and
  well-tested; the audit surfaces one architectural divergence (hand-written
  daemon, not triad_main emission), one dropped guarantee to confirm (verb
  mismatch rejection), a misnamed "meta socket" test (no meta plane wired),
  and two minor dead-code / placement nits. Operator is still working; I did
  not build (active detached-HEAD working copy).
---

# 84 — audit of the operator's criome current-stack migration

## What the operator is implementing

Lane: main `operator` (Codex). Claim (`orchestrate/operator.lock`, bead
`primary-ffew` — the criome current-stack port): `/git/.../criome #
current-stack sema-engine migration audit and unblocked port`. The repo is in
detached HEAD with a clean working copy — between steps, still in flight. No
operator report filed for this slice yet (337 covered harness; criome is
unreported).

Criome here is the **trust / attestation / authorization daemon** (its own
component: deps on `signal-criome`), distinct from `domain-criome`.

Four commits, `baffbc3..9dfaf84` (705 +/522 −, 16 files):

| Commit | What |
|---|---|
| `76bcfcd` | move daemon wire to `signal-frame` (off `signal-core`) |
| `24c83b9` | refresh schema-free `signal-frame` lock |
| `a3bc590` | route text and storage through the current stack |
| `9dfaf84` | split daemon into an rkyv-config single-argument binary |

Dependency cutover (`Cargo.toml`): `nota-codec`→`nota-next`, `sema`→`sema-engine`,
`signal-core`→`signal-frame`, `+triad-runtime`, `−clap`. New `criome-daemon`
binary.

## Conformance — what's right

This is a clean, on-discipline migration. Verified by reading source + tests:

| Discipline | Status | Evidence |
|---|---|---|
| Daemon binary-only startup (`pjvv`/`ur16`) | ✓ | `CriomeDaemonCommand::configuration()` takes `command.signal_file_argument()`, decodes rkyv via `CriomeDaemonConfigurationFile`; rejects `InlineNota`/`NotaFile` with `ArgumentError::ExpectedSignalFile`. Test `criome_daemon_configuration_rejects_nota_arguments`. |
| One argument, no flags | ✓ | clap removed; CLI client rejects `--`-prefixed args with `Error::FlagArgument`. Test `criome_cli_request_argument_rejects_flag_shape`. |
| sema → sema-engine (`fosp`) | ✓ | `Sema::open_with_schema` + `Table::ensure` per-txn → `Engine::open` + `register_table(TableDescriptor)` holding typed `TableReference<T>` handles. Store ext `.redb`→`.sema`. |
| signal-core → signal-frame | ✓ | frame primitives now from `signal_frame`; contract types stay in `signal_criome`. |
| Typed per-crate `Error` | ✓ | new `ConfigurationArchive{Decode,Encode}`, `Configuration{Read,Write}{path,source}`, `ExpectedNotaRequest`, `FlagArgument`, `Argument(#[from] triad_runtime::ArgumentError)` — all typed, `#[from]` chains. |
| rkyv binary config | ✓ | `CriomeDaemonConfiguration` is `Archive/Serialize/Deserialize`; file path in via `SignalFile::into_path`. |
| Test coverage | ✓ | binary-config accept + nota reject, CLI inline/file accept + flag reject, reply-on-request-path reject, socket 0o600, kameo actor-tree + authorization/replay/expiry suite retained. |

## Findings

### 1. Hand-written daemon, not triad_main emission (architectural divergence — flag)

Criome hand-writes the whole daemon spine in `src/daemon.rs` —
`CriomeDaemon` / `BoundCriomeDaemon` / `CriomeConnection`, `bind` /
`serve_one` / `serve_forever`. This is exactly the spine the **cloud pilot
(reports 80/81/542)** proved should be *emitted* into `src/schema/daemon.rs`
by `triad_main`, with the component hand-writing only `impl ComponentDaemon`
escape hatches.

Why it's defensible *for now*: criome's schema is still `schema/criome.concept.schema`
(concept stage, 561 bytes) — there is **no `build.rs`, no emitted daemon
module**, so triad_main emission is not yet available to this component. Getting
criome onto signal-frame + sema-engine + binary startup *first*, daemon-emission
*later*, is a reasonable incremental order.

Why it's worth flagging: this hand-written daemon is **future rework** — when
criome's schema graduates from concept to a triad and triad_main emits its
daemon, most of `daemon.rs` is thrown away (the cloud port deleted exactly this
kind of hand code). The operator's scope string ("current-stack migration") does
not mention triad_main, so this looks intentional — but the psyche should
confirm whether criome should stop at current-stack or carry through to
triad_main while it's open.

### 2. Verb-mismatch rejection dropped — confirm it's structural, not lost (verify)

The pre-migration receive path validated the signal verb:
`request.into_checked()` → reject on mismatch (the guarantee a prior commit
`e43eafe` deliberately added, *"reject mismatched signal verbs on receive"*).
The new path is `request.payloads.into_head()` — **no verb check**, and
`SignalVerb` / `into_checked` no longer appear anywhere in `src`. Reply side
likewise: `SubReply::Ok { verb, payload }` → `SubReply::Ok(payload)`.

Most likely this is correct: `signal-frame` appears to have **removed verbs from
the frame model** (the `verb` field is gone from `SubReply::Ok`), so there is
nothing left to check and `e43eafe`'s guard is simply obsolete. But that turns a
once-explicit *runtime guarantee* into a *contract-level assumption*. Confirm:
does signal-frame enforce operation/verb correctness structurally at decode, or
did criome silently lose the mismatch rejection it intentionally added? If the
latter, the guard needs a new home.

### 3. "Meta socket" test is misnamed — no meta plane is wired (correctness of claim)

Test `criome_daemon_meta_socket_is_user_private` reads as two-contract evidence,
but it binds the **single ordinary socket** and asserts `0o600`. `daemon.rs`
binds exactly one `UnixListener` (`self.socket`); there is no second
(meta-signal) listener and no `meta-signal-criome` dependency. So criome has **no
meta-signal plane** — fine for a concept-stage component, but the test name
claims a meta socket that doesn't exist. Rename to
`criome_daemon_socket_is_user_private`, or wire the meta plane. (Ties to the
two-contract invariant, Spirit `n0ss`: every component eventually needs
`signal-criome` + `meta-signal-criome`.)

### 4. `CriomeDaemon::from_environment` looks dead (minor)

The daemon binary (`src/bin/criome-daemon.rs`) goes through
`CriomeDaemonCommand::from_environment().run()` → `from_configuration`. The
separate `CriomeDaemon::from_environment` (daemon.rs:47, reads `CRIOME_SOCKET`)
has no caller in src — leftover from the pre-binary-startup path. Remove it, or
confirm a test uses it. (Also: env-var socket discovery for a *daemon* sits
uneasily next to binary-only startup; the live path correctly avoids it, so this
is just dead-code hygiene.)

### 5. `handle_connection` is a static associated fn (minor — placement)

`CriomeDaemon::handle_connection(runtime, root, stream)` uses no `self`/`Self`
data — it operates entirely on `BoundCriomeDaemon`'s fields passed in. Per the
method-placement rule it's a free function in disguise; it belongs on
`BoundCriomeDaemon` (where `runtime`+`root` live) or `CriomeConnection`. Cosmetic.

## Not verified

I did **not** run `cargo build/test/clippy`: the operator's working copy is a
live detached HEAD and a concurrent cargo run contends on the build/working-copy
lock and could stall their session. Conformance above is from source + test
reading. Recommendation: the operator should land this slice with the same green
witness 337 used — `cargo test` + `cargo clippy --all-targets --all-features -D
warnings` pinned in the report — and add the verb-guarantee note (finding 2).

## Verdict

Sound, disciplined current-stack migration — binary-only startup, no flags,
typed errors, sema-engine and signal-frame cutover, and good rejection-test
coverage all land correctly. Two items to resolve before/at landing: **confirm
the verb-mismatch guarantee** (finding 2) and **decide triad_main vs
stop-at-current-stack** (finding 1). Three cosmetic cleanups (3–5). Nothing
blocking; nothing that violated a hard override.
