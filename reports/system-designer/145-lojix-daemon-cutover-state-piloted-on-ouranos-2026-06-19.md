# 145 — State of the lojix daemon cutover: piloted on ouranos, legacy CLI still production

*The psyche asked, "what is the state of deprecating the old lojix CLI and moving
daemon-based in production?" — noting designer and operator are on it. This is the
grounded answer from a five-reader live-code survey (daemon, legacy CLI, wire
surfaces, production deploy, coordination), synthesized. It corrects my own
pre-survey framing on two points (the daemon host is ouranos not zeus; the active
lanes are cloud-designer / cloud-operator, not the default designer / operator).*

## BLUF

The lojix daemon stack is real and live, but the cutover is **piloted, not done**.
The daemon, its two per-socket CLIs, and both wire contracts (`signal-lojix` working
signal, `meta-signal-lojix` meta policy signal) are fully implemented, building, and
test-green on `main` — and the daemon is genuinely running in production on exactly
one host (ouranos), where it drove a real zeus FullOS Switch with behavior parity to
the legacy CLI. Everywhere else the legacy `lojix-cli` (plus the `lojix-run`
wrapper) remains the shipped, pinned user-facing deploy command on every
workstation, with no daemon, no deprecation marker, and no durable Spirit/INTENT
record mandating its retirement. What blocks full deprecation is not the contract or
the daemon code — it is end-to-end live-deploy validation beyond the single pilot,
routing operators onto `meta-lojix`, first-class daemon credentials, and repointing
CriomOS-home off the `lojix-cli` input.

One survey-level disagreement, surfaced up front: my orchestration framing said
"installed on zeus"; the grounded production survey shows the daemon live on
**ouranos**, with zeus as the deploy *target*. Ouranos is canonical throughout.

## Where each piece stands

### The lojix daemon — IN PROGRESS (built, test-green, piloted live)
One library plus **four** binaries (`lojix-daemon`, `lojix`, `meta-lojix`,
`lojix-write-configuration`), not the two the README claims (`Cargo.toml` lines
14-28; `INTENT.md` lines 10-37). Builds offline with zero warnings; ~69 tests green
across 20 lib unit tests and 11 integration files, with slow nix/network tests
correctly `#[ignore]`d. Binary-only startup discipline holds: the daemon decodes
exactly one rkyv startup file and rejects inline NOTA / `.nota` paths
(`src/bin/lojix-daemon.rs` lines 16-23). Storage is durable sema-engine self-resume
— `Engine::open` resumes catalog, commit-sequence, and identifier counters from
persisted rows, proven by the `durable_resume` test and
`test_run_table_survives_store_reopen`. The copy+activate reject-guard is now
**OPENED** (commit `cbe3c06`, the "daemon constructs real copy + activate" change)
with full System and Home activation profiles, `.drv` output selection via `^*`, and
Criome-gated activate effects — but `ARCHITECTURE.md` line 16 and `AGENTS.md` line 9
still say "Activating deploys still reject," which is stale. Deploy durability
survives client/SSH disconnect (handed to a daemon-owned job actor that persists a
`Submitted` row and replies `AcceptedDeploy` before the pipeline runs;
`tests/deploy_job_survival.rs`, 5 pass). Hermetic Test-op runs real `nix build`
end-to-end (commit `538fdeb`, the "REAL hermetic Test-op dispatch, proven
end-to-end" change); live runs are honestly rejected at submit, never faked.

### The thin CLIs — DONE (per the current contract)
Two CLIs, one per socket, each flag-free and typed only on its own contract: `lojix`
on `signal-lojix` (ordinary), `meta-lojix` on `meta-signal-lojix` (owner/meta)
(`src/bin/lojix.rs`, `src/bin/meta-lojix.rs`; `src/client.rs`). This structurally
resolves the audit short-header tier ambiguity (commit `1375bd9`, the per-socket CLI
split). Ordinary surface dispatches `Query`/`WatchDeployments`/`WatchCacheRetention`/
`Unwatch`; meta surface is `[Deploy Pin Unpin Retire Test]` with `Pin`/`Unpin`/
`Retire` going through real sema-engine writes, not stubs.

### signal-lojix / meta-signal-lojix wire — DONE (exchange ops + handshake; streaming deferred)
Both are fully implemented contract crates on `main`, not skeletons. `signal-lojix`:
171-line NOTA schema generating 2244 lines of Rust plus three test files (boundary +
frame round-trip pass green offline). `meta-signal-lojix`: 167-line schema generating
1392 lines, carrying the full `Deploy/Pin/Unpin/Retire/Test` surface and sharing 14
nouns from `signal-lojix:lib` rather than redefining them. The daemon consumes both
deeply across 6 source files, with `Cargo.lock` pinned to their exact `main` HEADs
(`signal-lojix` at `970da11…`, `meta-signal-lojix` at `26b617c…`) — no drift.
**Known deferral:** true daemon-pushed event/stream frames are not yet emittable (a
`schema-next`/`schema-rust-next` enhancement); today's contract carries the
subscription *handshake* form (`Watching`/`Unwatched` replies), sufficient for the
cutover. The contract is honest about daemon-side gaps via
`TestRejectionReason::LiveNotYetEnabled` and
`DeployRejectionReason::UnsupportedDeployAction`.

### Legacy lojix-cli — LIVE, frozen-by-intent, still production
The monolithic CriomOS deploy CLI: one NOTA argument, no flags, four request kinds
(`FullOs`, `OsOnly`, `HomeOnly`, `CheckHostKeyMaterial`) (`src/request.rs` lines
51-55). It is "frozen at current schema" by intent — meaning the *contract* is held,
not that the repo is dormant: the last 20 commits span May 12–June 17, 2026, the two
most recent being dependency refreshes. **Production pins it at `fc2ff02…`** (the
"migrate to nota-next" commit) across all three consuming `flake.lock`s (CriomOS,
CriomOS-home, CriomOS-test-cluster). Local `origin/main` is **one commit ahead** at
`ad28c8c` (a 2026-06-17 horizon/nota refresh) not yet pinned into CriomOS. The only
direct consumer that must migrate off is **CriomOS-home** (its `lojix-cli.url` input
+ `lojix-run` wrapper/check); CriomOS and CriomOS-test-cluster carry the pin only
transitively. `horizon-rs` is the dependency, not a consumer, and is **not** a
blocker.

### Production deploy — PILOTED on one host
The `lojix-daemon` is active on ouranos, started by the 2026-06-15 production FullOS
switch, running `lojix 0.3.4` from the system closure (`systemctl status
lojix-daemon.service`: "active (running) since Mon 2026-06-15"). It is functional,
not a zombie — an ordinary `(Query (ByNode (goldragon zeus None)))` returns zeus's
live generation, resolving the earlier empty-query bug. Sockets are installed with
hardened modes (ordinary `0660`, owner `0600`, `startup.rkyv 0600`). It runs on
**exactly one host** because the CriomOS module gates on the `PersonaDevelopment`
service, which only ouranos carries (`CriomOS/modules/nixos/lojix.nix` line 14;
`goldragon/datom.nota`). zeus/prometheus/tiger/balboa do not run the daemon.
Meanwhile `lojix-cli` and `lojix-run` ship in CriomOS-home `deploymentPackages` on
the `size.min` profile — live in `~/.nix-profile/bin` on every workstation.

## Piece-by-piece map

| Piece | State | Owner | What's left |
|---|---|---|---|
| lojix daemon | IN PROGRESS — built, test-green, piloted live on ouranos | cluster-operator / system-maintainer | Validate full routed-microVM activation outside the single pilot; cross-table atomic commit; refresh stale docs |
| Thin CLIs (`lojix`, `meta-lojix`, write-config) | DONE for current contract | cluster-operator | Split admission-vs-terminal reply in `meta-lojix`; widen `Query` selection (`All` rejected in 0.3.4) |
| `signal-lojix` / `meta-signal-lojix` wire | DONE (handshake); streaming DEFERRED | operator (code repos) | `schema-next` event-frame emission for live streaming Watch; refresh "skeleton" README |
| Legacy `lojix-cli` | LIVE, frozen-by-intent, pinned in production | cluster-operator + operator | Repoint CriomOS-home off it, then delete; reconcile stale `AGENTS.md` fork framing |
| Production deploy | PILOTED on ouranos only | system-operator + system-maintainer | Daemon on other hosts; route operators to `meta-lojix`; first-class daemon credentials; durable retirement intent |

## What actually blocks full deprecation

Ordered from "installed on ouranos" to "legacy `lojix-cli` deleted across
production":

1. **Capture durable retirement intent (NOT STARTED).** No Spirit/INTENT statement
   mandates the daemon as the sole deploy path or schedules `lojix-cli`'s removal —
   the cutover decision itself is undocumented as durable intent (the only
   governance lives in `protocols/active-repositories.md`, which is itself stale).
   This is the upstream gate and is psyche-owned; designer should run the Spirit
   gate to capture it once the psyche confirms the intent. *Owner: designer /
   cloud-designer, on psyche authority.*

2. **Land and run the live (non-hermetic) deploy-into-VM + assert chain (BLOCKED,
   psyche-gated).** Live Test-op is honestly rejected at submit via
   `TestRejectionReason::LiveNotYetEnabled` (commit `1dbecc0`); the first Prometheus
   live run and the daemon-to-node cutover are explicitly behind psyche
   authorization. The source notes the live chain and container bring-up/teardown
   bracket are "unimplemented" (`src/schema_runtime.rs` lines 1573, 1735). *Owner:
   cloud-operator (implementation), psyche (gate).*

3. **Prove full-OS deploy + survives-disconnect end-to-end beyond the single pilot
   (IN PROGRESS).** Real nix-build/copy/activate paths only run under `#[ignore]`d
   network tests today; the one captured parity run was a single zeus Switch from
   ouranos. Full routed-microVM activation is the `INTENT.md` cutover goalpost
   (Spirit record `se72`) and is not yet in the green suite. *Owner:
   cluster-operator / system-maintainer.*

4. **Land first-class daemon credentials (NOT STARTED).** The service currently
   depends on the operator's GPG SSH agent socket rather than daemon-owned keys, so
   it cannot run as a non-interactive system identity where no operator is logged
   in. This is bead `primary-srmq` (authenticated Nix flake resolution via a new
   `nix-auth` crate, per Spirit record 324), OPEN P1, unstarted since 2026-05-23.
   Without it the daemon cannot replace the CLI on unattended hosts. *Owner:
   operator lane, currently not on it.*

5. **Route operators onto `meta-lojix` as the default entry point (NOT STARTED).**
   The owner socket is local-only (li:users uid match), so remote operators have no
   daemon entry point today; the deploy mechanism must be reachable before the CLI
   can be removed. *Owner: system-operator.*

6. **Repoint CriomOS-home off `lojix-cli`, then drop the transitive pins (NOT
   STARTED).** CriomOS-home's `lojix-cli.url` input + `lojix-run` wrapper/check must
   point at the daemon stack; once it does, CriomOS and CriomOS-test-cluster
   transitive pins fall away. *Owner: operator (owns CriomOS / CriomOS-home main +
   pin bumps), with cluster-operator.*

7. **Delete `lojix-cli` deploymentPackages and the repo (NOT STARTED).** Final
   removal across `size.min` home profiles, only after 1–6. *Owner: system-operator
   + system-maintainer, joint.*

## Who's doing what now

The active lanes on the lojix daemon are **cloud-designer** (proposals) and
**cloud-operator** (implementation) via the Test-op / VM-testing arc — not the
default designer / operator lanes the psyche named. cloud-designer report 54
(`reports/cloud-designer/54-lojix-test-op/`, steering VM-testing into
`meta-signal-lojix` as a Test operation) and cloud-operator reports 388 (vm-testing
closeout) and 390 (LojixOS extraction proposal) are the live thread. cloud-operator
388 confirms **no live remediation, deploy, activation, router switch, or Prometheus
live operation has run** — only the safe hermetic surface landed.

The **default operator lane is currently on unrelated work** (its lock claims
persona kameo-lifecycle, router, and signal-standard), and the **default designer
lock is empty**. That leaves an **ownership gap**: the two daemon-prerequisite beads
— `primary-srmq` (the `nix-auth` daemon-credentials crate) and `primary-es8u`
("extract daemon listener/startup runner beyond the Nexus loop," generic
daemon-runtime work) — are both OPEN P1 and labeled operator territory, but no lane
is presently on them. **system-designer** owns the cross-component port plan that
uses lojix as the `MultiListenerDaemon` / `triad_main` template (reports 77 and 87)
and should reconcile the stale branch guidance.

## Cross-survey discrepancies and the stale-doc cluster

Surfaced rather than papered over:

- **"zeus" vs "ouranos" as daemon host.** The orchestration framing said "installed
  on zeus"; the grounded production survey shows the daemon live on **ouranos**, with
  zeus as a deploy target. Ouranos is canonical.
- **`horizon-leaner-shape` is dead weight.** All five surveys agree the daemon, both
  wire contracts, and the Test-op arc consolidated onto **`main`**, yet
  `protocols/active-repositories.md` still directs daemon-reshape edits to the
  `horizon-leaner-shape` feature branch in worktrees. That branch is stale (23
  commits behind `main`, last touched 2026-06-13) and its `signal-frame` /
  Criome-authorization work is largely superseded. Reconcile or retire it
  (designer / system-designer).
- **A wide stale-documentation front contradicts live code:** `lojix/README.md`
  ("one crate, two binaries" / "in development"), `lojix/ARCHITECTURE.md` §0 (omits
  two binaries; "activating deploys still reject"), `lojix/AGENTS.md` line 9 (same
  reject claim), `signal-lojix/README.md` ("Status: skeleton. Documentation only —
  no code yet"), and `lojix-cli/AGENTS.md` (still framing the repo as a "safe
  rewrite fork" of a live tool, contradicted by its own INTENT/ARCHITECTURE). These
  are doc-refresh items owed by the owning code-repo lanes (README / ARCHITECTURE)
  and the designer lane (the protocol map on primary).
- **Production lag (minor, not a blocker):** `lojix-cli` `origin/main` (`ad28c8c`)
  is one commit ahead of the production pin (`fc2ff02`); worth confirming whether the
  2026-06-17 refresh is intended to ship before any cutover work freezes the CLI.
