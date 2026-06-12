---
role: cloud-designer
session: 41-lojix-production-refresh
report: 11-synthesis
topic: Consolidated state-of-the-world + staged execution plan to finalize lojix for production
date: 2026-06-12
inputs: reports 0-10 (this directory), plus direct source confirmation of the spirit two-CLI/bootstrap precedent and the production lojix-cli parity baseline
---

# 41 · Lojix production refresh — synthesis and staged plan

The recon fan-out (files 1-10) is done. This file is the canonical
synthesis: where the daemon stack stands, what the psyche's goalpost
actually requires, and a STAGED execution plan ordered so that training +
schema-modernization + the two CLIs land before parity work, and parity
work lands before the live VM cutover test.

## 1. The goalpost, restated

From `0-frame-and-method.md` (psyche directive, 2026-06-12). Finalize the
new lojix logics component for production so the cluster runs on the
daemon stack. Five concrete asks:

1. **Two CLIs** — one on the meta socket, one on the regular (ordinary) socket.
2. **Modern schema syntax** — rewrite the `.schema` files, bump deps.
3. **Feature parity with production `lojix-cli`** — full-OS deploy,
   survives SSH disconnect, every operation described in schema types.
4. **End-to-end deploy testing** against a VM / test cluster on another
   host with a reachable IP.
5. **Train first**, work on `main`, then a full report.

The psyche's framing: *"I am pretty sure you can achieve this goalpost."*

## 2. Current state of the world — end to end

### 2.1 The lojix daemon crate (report 1)

`/git/github.com/LiGoldragon/lojix` on `main`, flattened to repo root.
`cargo build --offline` PASSES (24.6s); `cargo test --no-run` compiles
clean (heavy nix tests `#[ignore]`). One crate, two bins today:
`lojix-daemon` and `lojix`.

What WORKS end to end:

- Two authority-tiered Unix sockets via `triad-runtime`
  `AsyncMultiListenerDaemon`: **Ordinary** (peer read/observe) and
  **Owner/meta** (owner-only Deploy/Pin/Unpin/Retire). Owner socket is
  hardened: mode guard refuses `0o007` other-access; per-connection
  SO_PEERCRED uid/gid match, fail-closed.
- One-request/one-reply per connection, 64-permit cap per listener,
  8 MiB frame cap, 10s read timeout. Async engine, `tokio::process` for
  child nix, no blocking-pool bridge.
- The deploy pipeline's READ/BUILD half is real: `ResolveFlakeAuth`
  (`nix flake metadata`), `MaterializeHorizon` (loads cluster proposal,
  projects via `horizon-rs`, writes override-input flakes, SRI-hashes),
  `NixEval`, `NixBuild` (with remote builders + substituters).
- Pin/unpin/retire are real in-memory gc-root mutations (owner socket).

What is STUBBED or MISSING (the gaps to production):

- **Activating deploys are all REJECTED.** `unsupported_deploy_reason`
  accepts only System Eval/Build and Home Build; every Switch/Boot/Test/
  BootOnce/Home-Profile/Activate is rejected with `UnsupportedDeployAction`
  (test `activating_deploy_is_rejected_until_activate_lands`).
  `CopyClosure`/`ActivateGeneration` reference an unset `$CLOSURE` shell
  var — activation is not target-safe. **No real deploy mutates the live
  set end to end.**
- **All state is in-memory** (`Mutex<StoreState>`), NOT sema-engine/redb.
  No persistence, no crash-restart resume.
- **No virgin-daemon meta-signal config path / no SEMA self-resume** — the
  daemon hard-requires an rkyv startup file every launch.
- **Subscription push entirely missing** — Watch mints a token and replies
  once; no `SubscriptionSink`, no event emission, no delivery lane.
- **Container/dbus mirror missing** — write path exists, no event source.
- **Wire tier-ambiguity** (client.rs R7) — meta `Deploy` and ordinary
  `Query` share short-header ordinal 0x0; disambiguation rides rkyv layout,
  not a structural tier bit (fix is upstream in signal-frame).
- **No nix flake check surface** — only the cargo suite.

### 2.2 The two contracts (report 2)

The contract is already SPLIT cleanly along authority:

- `signal-lojix` (ordinary) = peer-callable read/observe/subscribe:
  `Query`, `WatchDeployments`, `WatchCacheRetention`, `Unwatch`,
  `CheckHostKeyMaterial`.
- `meta-signal-lojix` (meta) = owner-only mutation: `Deploy`, `Pin`,
  `Unpin`, `Retire`. `DeployRequest` is `[(System ...) (Home ...)]`; one
  verb covers FullOs/OsOnly/HomeOnly via the `DeploymentKind` discriminant.

Both crates are clean and committed. `meta-signal-lojix` cross-imports 12
shared nouns one-way from `signal-lojix` (`signal-lojix:lib:Type`). Watch
is a request→token handshake, not a live stream (schema-next can't emit
event frames yet; Spirit `2tfa`). **Stale-doc hazard:** both contracts'
`INTENT.md`/`ARCHITECTURE.md` still describe the pre-split single contract
with a non-existent `signal_channel!` macro and live streams — the schema
files and `src/lib.rs` doc-comments are the current truth.

### 2.3 Dependencies (reports 3, 4)

lojix's `Cargo.lock` pins every upstream codegen/contract crate BEHIND
current `main@origin`:

| crate | pinned | current main | nature of the gap |
|---|---|---|---|
| schema-rust-next | `b252e81e` | `cedb2e06` | **breaking-on-regen**: drops inherent `from_nota_block`/`to_nota` bridges (~124 defs) from generated files |
| schema-next | `ccdf5487` | `2397d5b2` | additive (scoped enum refs); moves with codegen |
| nota-next | `af6a2080` | `065fa2ad` | additive (byte-scalar codec) |
| signal-lojix | `8f6c498a` | `b31cd980` | flatten/split commits; moves in lockstep with codegen |
| meta-signal-lojix | `2e69371b` | `317b7fab` | flatten commit; lockstep |

Non-events: signal-frame (pin already current), triad-runtime (pin already
current; the `DaemonConfiguration`→`BindingSurface` rename touches no symbol
lojix imports), horizon-lib (pin current). `sema-engine`/`signal-sema` are
**not in lojix's tree at all** — lojix talks SEMA through `triad-runtime`'s
`NextStep::SemaRead/SemaWrite`, not the engine library.

The "modern schema syntax" codegen is owned by **schema-rust-next v0.5.3**
(Rust emitter) over **schema-next v0.2.0** (the `.schema` language engine).

### 2.4 The modern schema syntax (report 4)

The psyche's "schema syntax has changed; expect a full rewrite" is **half
right**. The syntax DID change materially (2026-06-09..06-11), but lojix's
two daemon schemas (`schema/nexus.schema`, `schema/sema.schema`) are
**already on the modern compact surface** — no stale grammar. They need at
most cosmetic touch-ups (collapsing `(OrdinaryInput OrdinaryInput)` self-
pairs to `(OrdinaryInput)`), NOT a rewrite. The real, concrete work is the
**dependency refresh + artifact regeneration**: bump the five pins above,
set `LOJIX_UPDATE_SCHEMA_ARTIFACTS=1`, rebuild so `nexus.rs`/`sema.rs` shed
the nota bridge methods and re-pass `build.rs`'s `write_or_check` freshness
gate. No hand-written lojix code calls those bridge methods (only the
traits/derives), so the break is regeneration-of-artifacts only.

Modern-syntax rules to honor when touching any `.schema`: braces are
key/value maps only (no enum sugar, no `(Name Body)` wrappers, no doubled-
name pairs); bare `Name Type` is always a distinct newtype (aliases were
dropped); `*` derives the field name from the type; `(Vec/Optional/Map ...)`
for composites; scalar leaves `String Integer Boolean Path Bytes`; single-
colon qualified names for cross-module refs; broad bare NOTA strings, no
quotation marks.

### 2.5 Coding + intent discipline (reports 6, 7, 8)

CODING discipline is settled (no drift since the 2026-06-07 corpus
rewrite). Hard fails to respect: method-only (no free functions, no ZST
namespaces), typed domain newtypes, typed per-crate `Error` via
`thiserror`, no hand-rolled parsers, redb+rkyv storage/wire, no blocking in
actor handlers, schema-emitted nouns own the methods, full-English names,
kameo-0.20 lifecycle (`Self` is the actor, restart reconstructs from
`Args`, durable state in sema/redb). Toolchain authority is
`CriomOS-home`; kameo is the `kameo-push-only-lifecycle` fork.

The Spirit topic sweep (report 8, 80+ records) confirms the directive is
**heavily pre-decided** by durable intent — this is execution against a
settled charter, not open design. Load-bearing records:

- `tvbn` (VeryHigh imp) — the Horizon+lojix rewrite charter: reach parity,
  cut over per-node, **retire the dual deploy stacks**.
- `8bwo` (VeryHigh cert) — two thin CLI clients per component: working
  named after the component, meta prefixed `meta-`. So **`lojix` +
  `meta-lojix`** (the spirit/meta-spirit pattern).
- `7sx6` (Maximum cert) — exactly two contracts, no more.
- `vudl`, `9v7h`, `3chp` — the lojix two-contract authority split; meta
  socket is the policy/control socket; SO_PEERCRED fail-closed.
- `ur16` (Maximum imp) — daemon bootstrap: single startup arg is a
  pre-generated rkyv `Configure` message (NOT NOTA); virgin→apply as first
  config, populated→self-resume; same `Configure` accepted live on the
  meta socket.
- `t803`, `q3q7`, `cgd8` — baseline meta op of every meta contract is
  `Configure`; the config TYPE lives in the ordinary contract, imported for
  binary startup decode; the meta `Configure` wraps it.
- `oh9l` (High) — **durable-first**: build the sema-engine durable backing
  NOW as baseline, not a first cutover on in-memory state.
- `up9q` (High) — a deploy **survives client disconnect**: owned by a job
  actor that owns the external process and persists job state; durable
  deploys survive disconnect by default; no blanket kill-on-drop.
- `2alg`, `k6w1` — daemon serves multiple connections concurrently, never
  blocks during a nix build; per-request deploy state; brief sema locks.
- `fosp` (VeryHigh), `e440`, `3d5z` (VeryHigh) — sema-engine is the
  exclusive DB interface; SEMA single-writer actor, parallel reads; strict
  triad-engine separation.
- `v5d4` (Constraint) — passing sandbox testing is a **precondition** for
  the lean-stack cutover.
- `xv9v`, `kx32`, `1lex`/`gnfx` — BootOnce/boot-mode for router nodes;
  disruptive switches run as durable systemd transient units so they
  survive SSH/Wi-Fi drop.
- `6x2k` (VeryHigh) — never build/deploy from a local path checkout; use
  the github remote url, commit-and-push first.
- `o5rz` — the rewrite repos (lojix, signal-lojix, meta-signal-lojix) push
  **directly to main**, no next/feature-branch ceremony (production code is
  lojix-cli + the current stack, which keep the designer-next/operator-main
  split).

### 2.6 Test cluster + VM (report 10)

There IS a working independent fixture
(`github:LiGoldragon/CriomOS-test-cluster`, synthetic nodes
`atlas beacon cedar dune`) and a reachable authenticated peer host
**Prometheus** (`ssh prometheus.goldragon.criome` verified from ouranos via
Yggdrasil; `criomos-nspawn` deployed there). The live proven E2E path is an
**nspawn machine on Prometheus**, driven by
`nix run .#nspawn-dune-on-prometheus` (push main → `nix build
#dune-nspawn-toplevel` on Prometheus → `criomos-nspawn create/start dune`).

A routed, human-viewable **microVM** with its own Criome domain
(`vm-testing.<cluster>.criome`) is designed and CI-tested but lives only on
CriomOS `next` and is **NOT deployed** to any node (Prometheus runs `main`;
no `microvm`/`qemu` binaries present). It is gated on Prometheus networking
non-breakage (Spirit `5hir5bnz`).

## 3. The two-CLI model — concrete shape (precedent confirmed)

The spirit crate is the canonical, already-shipped precedent for the
two-CLI + bootstrap pattern lojix must adopt. Confirmed in
`/git/github.com/LiGoldragon/spirit`:

| binary | role | socket | startup |
|---|---|---|---|
| `spirit` | working CLI (thin, `nota-text`) | ordinary | one NOTA arg |
| `meta-spirit` | meta CLI (owner-only, `nota-text`) | meta/owner (`SPIRIT_META_SOCKET`) | one NOTA arg, typed on `MetaInput` |
| `spirit-daemon` | daemon | binds both | one rkyv `Configure` file |
| `spirit-write-configuration` | bootstrap tool | — | reads NOTA, encodes typed config → rkyv startup file |

`meta-spirit.rs` mirrors `spirit.rs` but is typed on the meta contract's
`Input` (`Configure`, `Import`) and connects to the owner socket.
`spirit-write-configuration` decodes a NOTA `ConfigurationWriteRequest`
into the typed `SpiritDaemonConfiguration` and writes the rkyv startup
file the daemon consumes — this is exactly the deploy/bootstrap tool the
hard-override "daemons accept only binary startup" rule mandates (the tool
encodes typed NOTA into binary before it reaches the daemon).

**Lojix's shape, by parity:**

- `lojix` (working CLI) → ordinary socket, `signal-lojix` Input/Output
  (Query/Watch/Unwatch/CheckHostKeyMaterial). Already exists as
  `src/bin/lojix.rs` but currently routes both tiers and carries the R7
  tier-ambiguity bug.
- `meta-lojix` (new) → meta socket, `meta-signal-lojix` Input/Output
  (Deploy/Pin/Unpin/Retire/Configure). Does not exist yet.
- `lojix-daemon` → binds both sockets, takes one rkyv `Configure`. Exists;
  needs the virgin/self-resume path and the `Configure` meta op.
- `lojix-write-configuration` (new) → the bootstrap tool that encodes the
  typed lojix daemon config (today's five-field `DaemonConfiguration`) into
  the rkyv startup file.

Auth boundary: ordinary socket is peer-callable (filesystem mode); meta
socket is owner-only by SO_PEERCRED fail-closed + mode guard (already
implemented in the daemon). The config type lives in the ordinary contract,
imported for binary startup decode; the meta `Configure` wraps it (`q3q7`/
`cgd8`/`t803`).

## 4. Parity bar vs production lojix-cli (the missing report 9)

Production `lojix-cli` is deployed (`/home/li/.nix-profile/bin/lojix-cli`,
repo `/git/github.com/LiGoldragon/lojix-cli`). Its README + source give the
parity line items, each tied to a mechanism the daemon stack must match:

| parity item | production lojix-cli mechanism | lojix daemon status |
|---|---|---|
| Full-OS deploy | `FullOs` request = system generation with Home Manager included; `OsOnly`/`HomeOnly` variants | `DeployRequest [(System) (Home)]` covers the kinds; **eval/build only, activation rejected** |
| Request-is-the-interface | one NOTA request, no flags/subcommands; inline NOTA, request file, or default config | matches the component-one-arg rule; daemon takes rkyv, CLIs take NOTA |
| Every operation in schema types | the NOTA record IS the operator intent | contracts already type every op; ✅ on the contract side |
| **Survives SSH disconnect** | `BootOnce` runs `systemd-run --wait --unit=<name> --collect /bin/sh -c '…'` — a **transient unit owned by PID 1**; killing the ssh leaves the unit running to completion on the target | **not ported**: daemon's ActivateGeneration is stubbed; Spirit `up9q` says the daemon goes further (a job actor owns the process + persists state), but the proven `systemd-run` transient-unit primitive must back the remote activation |
| Remote build/copy | `nix copy --to ssh-ng://<target>`, remote builders from projected horizon nodes | CopyClosure exists but references unset `$CLOSURE`; not target-safe |
| Boot-once safety for routers | `BootOnce` swaps the oneshot boot entry without moving the persistent default | maps to Spirit `xv9v`/`kx32`; must be in the daemon activation path |

The parity gap is concentrated in **one place**: the daemon's
copy+activate+live-set-mutation path. Everything upstream (request typing,
horizon materialization, eval, build) already works.

## 5. Test infrastructure + recommended E2E target

- **VM/cluster availability:** `CriomOS-test-cluster` fixture +
  Prometheus peer (reachable, authenticated, `criomos-nspawn` deployed).
- **Recommended E2E deploy target (fastest to working):** drive lojix
  against synthetic node **`dune` on Prometheus via the nspawn path**. It
  is the only target where the host is reachable+authenticated, a deploy
  primitive (`criomos-nspawn create/start/shell`) is already deployed and
  exercised by `nspawn-dune-on-prometheus`, and the fixture already
  produces a buildable container toplevel (`dune-nspawn-toplevel`).
  Activation becomes `criomos-nspawn create/update <name> <toplevel> &&
  start` rather than a host-level switch — far lower risk than a router
  node, and it matches the proven manual runner.
- **Routed microVM endpoint** (`vm-testing.<cluster>.criome`) is the
  ultimate human-viewable target but requires deploying the `next`
  vm-testing module to a node and is gated on Prometheus networking
  non-breakage — **defer until after the nspawn-path E2E passes.**

## 6. Consolidated gap list (today → goalpost)

1. **Activation path is stubbed/rejected** — the single biggest parity gap.
   CopyClosure/ActivateGeneration must carry the real closure path; the
   reject-guard must open for activating actions once safe.
2. **No durable storage** — all state in-memory; sema-engine/redb cutover +
   self-resume is the headline architectural gap (`oh9l`, `fosp`, `3d5z`).
3. **No virgin-daemon `Configure` path / no SEMA self-resume** — daemon
   hard-requires an rkyv file every launch (`ur16`).
4. **No `meta-lojix` CLI and no `lojix-write-configuration` bootstrap tool**
   — the two-CLI model is half-built (`8bwo`).
5. **Wire tier-ambiguity (R7)** — needs an upstream short-header tier bit in
   signal-frame; today disambiguation rides rkyv layout.
6. **Dep pins are all behind; artifacts stale** — bump + regenerate
   (sheds nota bridge methods, re-passes the freshness gate).
7. **SSH-disconnect survival not implemented in the daemon** — port the
   `systemd-run --wait --collect` transient-unit primitive (lojix-cli) under
   the job-actor model (`up9q`, `1lex`/`gnfx`).
8. **Subscription push missing** — token handshake only; full schema-derived
   streaming is the direction but **does NOT block cutover** (`2tfa`/`brgo`).
9. **Stale contract docs** — signal-lojix/meta-signal-lojix INTENT/ARCH
   still describe the pre-split single contract; refresh before they
   mislead a CLI author.
10. **No live deploy test exists** — the daemon can eval/build against the
    test cluster but cannot activate; no E2E deploy has run.

## 7. Staged execution plan

Ordered so training + schema-modernization + the two CLIs come first, then
parity (durable state, activation, SSH-survival), then the live VM cutover
test. Each stage is committed directly to `main` in the rewrite repos
(`o5rz`).

| stage | goal | work |
|---|---|---|
| **S0 · Train + refresh** | Be fluent in the modern style and current intent before authoring. | Re-read CODING discipline (report 6) and intent model (report 7); run the Spirit gate on the directive and Record the durable charter capture; refresh the stale `signal-lojix`/`meta-signal-lojix` INTENT/ARCH docs to the split reality; manifest the lojix charter into the repos' INTENT.md. No code. |
| **S1 · Schema modernization + dep bump** | Land on current codegen with clean regenerated artifacts. | Bump the five pins (schema-rust-next, schema-next, nota-next, signal-lojix, meta-signal-lojix) to current main; `LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo build` to regenerate `nexus.rs`/`sema.rs` (shed bridge methods) and re-pass `write_or_check`; collapse cosmetic self-pairs only; verify `cargo build`/`test --no-run` green. Watch the triad-runtime listener rename if its pin moves. |
| **S2 · Two CLIs + bootstrap** | Complete the `lojix` + `meta-lojix` two-client model and the binary-startup bootstrap tool. | Split `src/bin/lojix.rs` to ordinary-only (fixing R7 by tier-typing on `signal-lojix::Input`); add `src/bin/meta-lojix.rs` typed on `meta-signal-lojix::Input` connecting the meta socket (mirror `meta-spirit.rs`); add `lojix-write-configuration` (mirror `spirit-write-configuration`) encoding the typed daemon config → rkyv; add the meta `Configure` op + virgin-daemon apply + SEMA self-resume (`ur16`/`t803`). |
| **S3 · Durable state cutover** | Replace in-memory `StoreState` with sema-engine/redb durable backing + self-resume. | Move the four tables (LiveSet/GcRoots/EventLog/ContainerLifecycle) onto the daemon-owned Sema layer through `triad-runtime` NextStep::SemaRead/SemaWrite; SEMA single-writer actor, parallel reads (`e440`); self-resume on restart (`oh9l`, `fosp`, `29pb` backups). No direct redb. |
| **S4 · Activation + SSH-survival parity** | Reach functional parity with production lojix-cli's deploy. | Carry the real closure path into CopyClosure (`nix copy --to ssh-ng`) and ActivateGeneration; port the `systemd-run --wait --unit --collect` transient-unit BootOnce primitive from lojix-cli under the job-actor model so deploys survive SSH disconnect (`up9q`, `1lex`); add an nspawn-target activation (`criomos-nspawn create/update + start`) as the lowest-risk first activation; open the reject-guard for the now-safe actions; node-identity injection (M3). Materialize `secrets` where the target needs them. |
| **S5 · Live VM/cluster E2E** | Prove cutover-readiness against the test cluster (the `v5d4` precondition). | Drive lojix end to end against synthetic node `dune` on Prometheus over the nspawn path: materialize Horizon from `fieldlab.nota` → build closure → activate via `criomos-nspawn`; assert hostname/`is-system-running`; verify SSH-disconnect survival by killing the client mid-deploy and confirming completion + persisted job state. Commit-first, build-from-remote (`6x2k`). Defer the routed microVM endpoint until this passes. |
| **S6 · (follow-on, non-blocking)** | Streaming push + container/dbus mirror + per-node router cutover. | Schema-derived event-frame emission (teach schema-next/schema-rust-next + add push to triad-runtime); dbus container-transition source; then the per-node production cutover retiring the dual stacks (`tvbn`). Explicitly does NOT block the S5 cutover test (`2tfa`/`brgo`). |

## 8. Open questions for the psyche

1. **First-activation target:** confirm the nspawn-on-Prometheus path for
   `dune` as the E2E target (vs holding out for the routed microVM, which
   needs the `next` vm-testing module deployed + networking sign-off).
2. **R7 tier bit:** fixing the short-header tier ambiguity is upstream in
   signal-frame — is a signal-frame change in scope for this push, or do we
   keep the rkyv-layout disambiguation and ship the tier bit later?
3. **Substituter-in-daemon** (`lc28`, Low cert, "must be replaced") — adopt
   the provisional move-into-daemon for now, or keep substituters on the
   wire until a better design lands?
4. **GitHub-auth flake resolution** (`2qhw`, Medium) — is the gopass→
   NIX_CONFIG access-token library in scope for this push or deferred?
5. **Streaming:** confirm the handshake+poll bridge is acceptable through
   cutover (`2tfa`/`brgo` say it does not block) so S6 streaming stays a
   follow-on.

## 9. Readiness assessment

The goalpost is **achievable in one focused execution push**, and the
psyche's confidence is warranted. The work is heavily de-risked: the
contracts are already split correctly along the exact two-CLI axis; the
schemas are already modern (the "rewrite" is really a dep bump + artifact
regen); the daemon's hard parts (two hardened sockets, horizon
materialization, eval, build, concurrency model) already work; the two-CLI
+ bootstrap pattern has a complete, shipped precedent in spirit to copy;
and a reachable, authenticated, deploy-capable test target (dune-on-
Prometheus) exists today. The genuine engineering remaining is concentrated
and well-scoped: durable-state cutover (S3) and the activation + SSH-
survival path (S4), both backed by clear intent and a working lojix-cli
reference for the activation primitive. The principal risks are (a) the
sema-engine durable cutover being larger than the psyche's "small and
straightforward" estimate, and (b) the first live activation surfacing
target-environment surprises (`criomos-nspawn` accepting a lojix-built
store path unchanged is unverified). Both are contained by staging the
nspawn path before any router-node or routed-microVM work and by the
`v5d4` precondition that sandbox testing gates the real cutover.
