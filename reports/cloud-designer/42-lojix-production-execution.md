# 42 · Lojix production execution — running log

Execution against the staged plan in `reports/cloud-designer/41-lojix-production-refresh/11-synthesis.md`
(S0…S6), toward the psyche goalpost: the daemon-based logics running the
cluster, at feature parity with production `lojix-cli` (full-OS deploy,
survives SSH disconnect, every operation schema-typed), with two CLIs
(meta socket + regular socket). This file logs what actually landed, stage
by stage. Working straight on `main` in the triad repos (Spirit `o5rz`;
psyche re-authorized 2026-06-12).

Durable intent captured this arc: [the lojix component ships two CLIs — a
meta-socket CLI for the policy/owner contract and a regular-socket CLI for
the peer contract] (Spirit `ssk2`, Decision High).

## S1 · Schema modernization + dependency bump — DONE (2026-06-12)

**Reframe confirmed.** The psyche's "schema syntax changed; expect a
rewrite" was half-right: the `.schema` *grammar* changed (2026-06-09→06-11)
but lojix's `schema/nexus.schema` + `schema/sema.schema` were already on the
modern compact surface. The real work was a dependency refresh + artifact
regeneration, not a grammar rewrite (see report 41 file 4).

**The cascade.** `schema-rust-next` `cedb2e06` ("stop emitting nota bridge
methods") removes the inherent `from_nota_block`/`to_nota` convenience
methods from every generated artifact (the `NotaDecode`/`NotaEncode` trait
impls stay). Because the contract crates check in their generated `.rs`, the
removal made *their* artifacts stale — `signal-lojix`'s `build.rs`
freshness gate (`write_or_check("SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS")`)
panicked before lojix could even regenerate its own. So a one-repo bump is
really a **triad-wide regen in dependency order**:
`signal-lojix → meta-signal-lojix → lojix`, each pushed to origin `main`
before the next consumer's `cargo update` could fetch it.

**What landed (each: bump codegen deps to current main, regen with the
crate's `*_UPDATE_SCHEMA_ARTIFACTS=1`, build green, push main):**

| repo | main before | main after | artifact change |
|---|---|---|---|
| signal-lojix | `b31cd980` | `c33e2be4` | `src/schema/lib.rs` −695 lines (0 bridge methods left) |
| meta-signal-lojix | `317b7fab` | `defade02` | `src/schema/lib.rs` −398 (picks up signal-lojix `c33e2be4`) |
| lojix | `13192bce` | `b3041914` | `nexus.rs` −353, `sema.rs` −331 (0 bridge methods left) |

Crate revs now current across the stack: `schema-rust-next cedb2e06`,
`schema-next 2397d5b2`, `nota-next 065fa2ad`, `signal-frame 166bda84`,
`triad-runtime 6ea83162`, `horizon-lib 9fae4a36` (the last two were already
current — the `DaemonConfiguration → BindingSurface` rename does not touch
any symbol lojix imports, so no code break).

**Verification.** No hand-written code called the removed inherent methods
(lojix uses the traits/derives only), so the break was artifacts-only.
lojix builds clean; the non-ignored suite is green on both gates —
default features 20 passed, `--features nota-text` 22 passed, 7 ignored
real-nix/live-daemon tests in each. No `.schema` grammar edits were needed
(the only candidate touch-ups — collapsing `(OrdinaryInput OrdinaryInput)`
self-pairs to `(OrdinaryInput)` — are cosmetic and were left alone).

## S0 · Doc honesty — partial (2026-06-12)

`lojix/INTENT.md` re-manifested: the superseded "thin CLI is the daemon's
first client" framing is replaced with the two-CLI charter (`ssk2`) and a
production-cutover-charter section (`tvbn`/`up9q`/`oh9l`/`se72`). Pushed at
lojix `146594b2`. Remaining: refresh the stale `signal-lojix` /
`meta-signal-lojix` contract docs (still describe the pre-split single
contract with a non-existent `signal_channel!` macro and live streams).

## S2 · Two CLIs — split landed (2026-06-12)

The unified `Client` (which trial-decoded both contracts, carrying the
audit-R7 short-header ambiguity) is split into two tier clients in
`src/client.rs` — `OrdinaryClient` (peer `signal-lojix`) and `MetaClient`
(owner `meta-signal-lojix`) over a shared `SocketExchange` — driving two
binaries: `lojix` (ordinary socket) and the new `meta-lojix` (owner/meta
socket), mirroring `spirit` / `meta-spirit`. The R7 ambiguity is gone
**structurally**: each CLI parses only its own contract, so there is no
cross-tier decode. The daemon needed no change (it already binds both
sockets). Green on both feature gates (default 5, `nota-text` 6 client
tests; full suite green, 7 ignored real-nix). Pushed at lojix `1375bd95`.

## Test target — resolved (2026-06-12)

Per psyche clarification (Spirit `7let`): the e2e is **deploy a full OS into
a throwaway KVM VM on Prometheus** — harmless because a broken deploy kills
only the VM, host untouched; NOT the host-reconfiguring `vm-testing` module
(report 43 corrected). Prometheus verified live: bare-metal, AMD-V,
`/dev/kvm`, 32 cores, 124 GiB free. qemu run transiently via `nix`. No
`5hir5bnz` exposure.

## S2 finish · bootstrap tool — landed (2026-06-12)

`lojix-write-configuration` (mirrors `spirit-write-configuration`): a typed
NOTA config request → the daemon's rkyv startup file, round-trip tested.
Pushed at lojix `e51d71de`. (The meta `Configure` runtime-reconfig op +
virgin-daemon-wait remain a follow-on — not blocking; the daemon configures
from its binary startup file today.)

## S3 · Durable state — landed (2026-06-13)

Replaced the in-memory `Mutex<StoreState>` with a durable `sema-engine`-backed
`Store` persisting to `<state-dir>/lojix.sema`, copying the shipped spirit
`Store`-on-`Engine` precedent verbatim. `StoreState`, the Mutex/lock API, the
four RAM counters, and the ten in-RAM mutators are deleted. One keyed
`TableReference` per family (live-set, gc-roots, event-log, container) — one
row per element; `EngineRecord` impls live in `lib.rs`, the generated
`schema/sema.rs` stays byte-for-byte. **`Engine::open` IS the self-resume.**
The reset-to-zero id bug is fixed: `next_generation/deployment_identifier`
derive from max-persisted+1; `next_event_log_position` from the row count;
the subscription token stays an ephemeral atomic (subscriptions don't
persist). Built via an implement→adversarial-review workflow; the reviewer
independently re-ran both gates (default 24 / nota-text 25 passed, 7 ignored)
and confirmed resume is *proven* (genuine drop+reopen test), keying is
collision-free (`assert` errors on duplicate, never clobbers), ids are
restart-safe, and cloud-operator's TCP-peer owner-auth is intact. Two notes
addressed before push: the "idempotent on retry" wording corrected to
*fail-safe / no-clobber* (a duplicate-key `assert` errors, it is not an
idempotent no-op), and `rust-version` bumped to 1.89 (redb 4.1 MSRV). Pushed
at lojix `196ab501`. INTENT.md + ARCHITECTURE.md refreshed to the durable
shape on the same commit.

**Tracked durability gap (follow-on):** `record_activation` writes the
live-set then gc-root rows as two sequential keyed asserts — `CommitRequest`
is single-table, so a crash between them leaves a torn write (a live row
without its gc-root) with no reopen reconciliation. Honestly documented;
acceptable pre-production baseline (Spirit `oh9l`), but must be closed before
the real cutover — either a sema-engine multi-table commit (the right layer,
Spirit `fosp`) or an interim reopen-reconciliation that rebuilds missing
gc-roots from the live set on open.

## S4a · Real activation — landed (2026-06-13)

Split S4 into S4a (command construction, unit-testable) and S4b (the
disconnect-survival job-actor). S4a is done: the daemon now constructs correct
target-side **copy + activate** commands and the reject-guard is open for every
activating action (System Boot/Switch/Test/BootOnce + Home Profile/Activate).
The `$CLOSURE` bug is fixed — the built closure path was already on the cursor;
`ActivateGenerationCommand` now carries it mandatorily (no empty fallback).
Faithful port of `lojix-cli`: `SshTarget` `root@<node>.<cluster>.criome`
(derived from the cursor's cluster+node via `CriomeDomainName::for_node` — no
new field), `--substitute-on-destination` copy with the three from/to/skip
cases, per-action System activation with EFI reconcile, and the
`systemd-run --collect --wait --service-type=oneshot` PID-1 transient-unit
BootOnce + the byte-exact OLD/NEW EFI staging script (the daemon→target
disconnect-survival surface). 20 new unit/argv/snapshot tests; build + both
gates + clippy green. Adversarially reviewed **pass** — the BootOnce/EFI
scripts verified byte-for-byte against `lojix-cli` and pinned by a snapshot
test; on-node behavior proves at S5 (a throwaway VM, so any error is caught
harmlessly). Pushed at lojix `cbe3c06b`. (Two extra schema fields were needed
for a faithful port: `CopyClosureCommand.source`, `ActivateGenerationCommand.profile`.)

## S4b · Disconnect-survival job-actor — landed (2026-06-13)

A meta `Deploy` now records the submission synchronously, replies the
`AcceptedDeploy` handle immediately, and runs the full effect pipeline on a
**daemon-owned `DeployJobs` kameo actor** whose `ActorRef` lives on
`LojixRuntime` — the pipeline is a detached runtime task, so dropping the
client connection cannot cancel it (client→daemon survival, Spirit `up9q`).
Only `Deploy` decouples; Pin/Unpin/Retire stay synchronous. A deploy-job cap
(8) refuses overflow with the typed `DeploymentInFlight`. A fifth durable
`DeployJob` sema family is written per phase + read-on-start with a typed
per-phase resumption decision (persist + read-back + reconcile-decision; live
restart continuation is S5-proven). Reviewed **pass-with-notes**: the reviewer's
ownership trace confirmed the decoupling is real by construction; I then
strengthened the headline survival test to a **mechanical witness** (the submit
runs on a separate task that is joined and dropped while the pipeline is parked,
then the deploy provably reaches terminal — proving it outlives its submitting
task). build + both gates (48/49) + clippy green. Pushed at lojix `bbb8030c`.

## Daemon code feature-complete against the parity bar (2026-06-13)

| Parity requirement | Status |
|---|---|
| Deploy a full OS (System + Home, copy + activate) | S4a — daemon constructs real `nix copy` + per-action activate + EFI reconcile |
| Survive SSH disconnect | S4a (daemon→target: `systemd-run --collect` PID-1 transient unit) + S4b (client→daemon: detached job actor) |
| Every operation described in schema types | both contracts type the full surface; the daemon is schema-derived |
| Durable-first state | S3 — `sema-engine` store + self-resume |

The remaining work is the **live proof** (S5) and the tracked follow-ons — the
*code* paths exist, are unit/argv/snapshot-tested, and are reviewed.

## Next

- **S5 · Live e2e** (the cutover validation; a live-host step — coordinate with
  the psyche first). Stand up a throwaway qemu/KVM VM on Prometheus (run via
  `nix`, host config untouched — verified bare-metal, AMD-V, `/dev/kvm`, 32c /
  124 GiB), then drive lojix end-to-end: deploy a full OS into the VM, prove the
  copy + BootOnce activation land, and prove the deploy survives an SSH
  disconnect. Spirit `se72`/`7let`. On-node behaviors deferred from S3/S4 prove
  here (EFI staging boots NEW then rolls back to OLD; the transient unit
  survives a real ssh drop; the live resumption continuation).

### Tracked follow-ons (non-blocking for S5's happy path, close before cutover)

- **Cross-table torn-write** (S3): an activation's live-set + gc-root are two
  sequential asserts; needs a sema-engine multi-table commit or an interim
  reopen-reconciliation.
- **Untracked deploy-job spawn** (S4b): the detached pipeline task's panic
  before `DeployCompleted` would leak a cap slot — promote to a supervised
  child actor (or a completion guard).
- **Terminal `DeployJob` rows** (S4b): Failed/rejected rows are cleaned only at
  next-restart reconcile — durable hygiene, retract on terminal.
- **Wire variant** (S4b): the immediate reply reuses `Deployed(AcceptedDeploy)`;
  a distinct Accepted-vs-Completed variant would be cleaner.
- **Meta `Configure` op + virgin-daemon-wait**; the **owner→meta socket rename**
  (`3chp`); the stale `signal-lojix`/`meta-signal-lojix` contract docs (S0).
- **Environment:** the **Spirit intent daemon is down** (`spirit-daemon`
  start-limit-hit, `spirit-upgrade-store` exits 1) — system-maintainer scope,
  blocks new intent capture.
