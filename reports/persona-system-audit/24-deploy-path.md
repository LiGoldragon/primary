# Deploy Path

I have enough grounded evidence across all five investigation areas. Both `horizon-leaner-shape` and `live-deploy-test-chain` are stale/divergent from `main` (merge-base is the May skeleton); ouranos runs a legacy-style nixos-system closure (22 generations, not in lojix's live set). Here is the analysis.

Per the harness directive, findings are returned inline (no report file written). Every claim is tagged FACT (direct evidence) or INFERENCE (reasoned from evidence), with paths/commands.

# CriomOS / lojix Deploy-Path Situational Map — 2026-07-01

## 0. One-paragraph orientation

FACT — This workstation is node **ouranos** (`hostname` → `ouranos`), the production `goldragon` cluster's `PersonaDevelopment` operator host. The **lojix daemon** (the daemon rewrite, not a monolith) is the live deploy orchestrator: `lojix-daemon` PID 542758 has been running since Jun 20 from `…-lojix-0.3.10/bin/lojix-daemon` (`/proc/542758/exe`), bound to `/run/lojix/{ordinary,owner}.sock`. A read-only `lojix "(Query (ByNode (goldragon prometheus None)))"` returned one live generation: `goldragon prometheus FullOs BootOnce Current` → a `nixos-system-prometheus-26.05` closure. So real host deploys through the daemon have happened; full cutover has not.

## 1. How a node is built + deployed today (build → deploy → activate → verify)

FACT — The build target is a single NixOS system in `CriomOS/flake.nix` (`/git/github.com/LiGoldragon/CriomOS/flake.nix:198`): `nixosConfigurations.target = nixosSystem { … modules = [ readOnlyPkgs (home-manager if includeHome) self.nixosModules.criomos ]; }`. Four axes enter as **stub path-inputs that lojix overrides per deploy** (`flake.nix:94-115`): `system` (`stubs/no-system`), `pkgs` (`github:LiGoldragon/CriomOS-pkgs`), `horizon` (`stubs/no-horizon`), `deployment` (`stubs/default-deployment`), plus `secrets` (`stubs/no-secrets`). `deployment.includeHome`/`includeAllFirmware` select full-OS vs OS-only.

FACT — The concrete pipeline the running daemon uses (evidence: `lojix/ARCHITECTURE.md:8-33`, `lojix/src/schema_runtime.rs:8` "resolve flake auth, eval, build, copy, activate", and the on-disk artifacts under `/var/lib/lojix/`):
1. **Author** cluster facts: `goldragon/datom.nota` (production proposal) + `criomos-horizon-config/horizon.nota` (pan-horizon identity/LAN).
2. **Submit** `meta-lojix "(Deploy (Host (…)))"` to the owner socket (per `operating-system-operations` skill).
3. **Project + materialize**: daemon reads the proposal via `horizon-lib` (horizon-rs, in-process Rust dep — `lojix/Cargo.toml` `horizon-lib = …horizon-rs…branch=main`) and writes content-addressed flake inputs. FACT — these exist on disk: `/var/lib/lojix/generated-inputs/goldragon/{ouranos,zeus,prometheus}/{full-os,os-only,home}/{horizon,system,deployment,secrets}/` (e.g. `…/prometheus/full-os/horizon/horizon.json` contains `cluster.name=goldragon`, `node.name=prometheus`, `node.services=[TailnetClient, NixBuilder{6}, NixCache, VmHost]`).
4. **Build**: `nix eval`/`nix build` of `CriomOS#nixosConfigurations.target` with `--override-input` for each axis. FACT — for a target ≠ daemon host, realization happens **on the target node's own store** over `ssh-ng://root@<node>.<cluster>.criome` (build-on-target, `lojix/ARCHITECTURE.md:18-33`); an active `ssh nix-ssh@prometheus.goldragon.criome … nix-daemon --stdio` remote-build connection was observed in `ps`.
5. **Activate**: copy is a no-op for build-on-target; activation runs the deterministic transient unit `lojix-boot-once-deploy-<id>` (BootOnce) or Switch/SetBootProfile/TestActivation. FACT — `schema_runtime.rs` maps `HostDeployAction::{SetBootProfile→BootProfile, ScheduleBootOnce→BootOnceProfile, Switch/ActivateNow→LiveActivation, TestActivation}` (`schema_runtime.rs:1127-1148`).
6. **Verify**: `lojix "(Query (ByNode …))"` against the live-generation set persisted in `sema-engine` (`/var/lib/lojix/lojix.sema`, 270 KB, mtime today 15:27).

FACT — Supporting repos' roles: **CriomOS-lib** = "Shared constants, helpers, and data files" (`CriomOS-lib/README.md`); **CriomOS-pkgs** = nixpkgs wrapper flake, system-keyed so CriomOS source edits don't invalidate the pkgs eval cache (`CriomOS/flake.nix:97-103`); **CriomOS-home** = standalone home-manager flake, `homeConfigurations` per `horizon.users`, gated by `deployment.includeHome` (`CriomOS-home/flake.nix:392`).

FACT — **forge is NOT in any deploy path.** `forge/ARCHITECTURE.md:1-27` states it plainly: "Today's stack still builds with nix directly; forge is **not** in any current production path… Not related to the Lojix deploy work." All bodies are `todo!()` skeleton (`forge/ARCHITECTURE.md:127`).

## 2. Stack A (monolith) vs Stack B (daemon): which is live

INFERENCE (high confidence) — **The A/B dichotomy in the brief has resolved: the daemon is both landed and live; no separate monolith is running or present in `lojix` main.** Evidence:
- FACT — `lojix` main history is 51 commits: earliest real code is `5c0ee76 2026-06-05 "import schema-derived triad-port daemon crate (new-stack rewrite, M1 build+evaluate)"`; before that (May) it was a docs-only skeleton. So today's `lojix` main **is** the daemon rewrite.
- FACT — Top of main is `4cc65fd 2026-07-01 "lojix: land nonlegacy deploy runtime"` (today), bumping `Cargo.toml` to **v0.4.0**, rewriting `src/schema_runtime.rs` (+1111/−… lines). "Nonlegacy" ≙ the legacy path removed.
- FACT — `git ls-files | rg 'monolith|lojix-cli'` → nothing. No monolith crate in the tree.
- FACT — The branch the brief calls "Stack B" (`horizon-leaner-shape`) is **stale and divergent**: `git merge-base --is-ancestor horizon-leaner-shape main` → NO; merge-base is the May-14 skeleton `eca194f`; its tip is `7466723 2026-06-13`. `live-deploy-test-chain` is likewise divergent (tip `2026-06-19`, "runNixOSTest proof GREEN under KVM"). Both are earlier/experimental lineages; the live daemon lineage is on **main**.

FACT — **What is actually live:** the daemon binaries are installed (`/home/li/.nix-profile/bin/{lojix,meta-lojix,lojix-daemon}` all → `…lojix-0.3.10`), the daemon runs, and it has completed **one recorded production host deploy** (`goldragon/prometheus FullOs BootOnce Current`, gen/deploy id `1 1`, event-log `488`).

FACT — **Cutover is incomplete:**
- Running/installed daemon is **0.3.10**; today's **0.4.0** is landed in source but not built into the profile (both `/proc/542758/exe` and `/home/li/.nix-profile/bin/lojix-daemon` → `lojix-0.3.10`).
- The live-generation set holds **only prometheus** (the Query returned a single row). ouranos and zeus were eval/materialized (generated-inputs exist) but are **not** recorded as lojix-`Current`.
- FACT — ouranos's own OS is a legacy-shaped closure: `/run/current-system` → `nixos-system-ouranos-26.05…` with **22 system generations** (newest `system-134`, 2026-06-29), none reflected in lojix's live set. INFERENCE — ouranos is still maintained outside the recorded lojix path (legacy `nixos-rebuild`), i.e. the operator host itself is pre-cutover.
- FACT — No `/nix/var/nix/gcroots/criomos/` tree exists on ouranos, though `lojix/ARCHITECTURE.md:88-97` specifies that GC-roots layout — so the durable gcroots surface is not yet populated here.

## 3. Is the Persona federation deployable onto a CriomOS host today?

FACT — **Partially, and only piecemeal.** CriomOS ships NixOS service modules (aggregated in `CriomOS/modules/nixos/criomos.nix:16-41`) for exactly five federation-adjacent daemons:

| Daemon | CriomOS module | systemd unit | Gated by (horizon) |
|---|---|---|---|
| router-daemon | `modules/nixos/persona-router.nix` | `persona-router` | `PersonaRouter` node service |
| mirror | `modules/nixos/mirror.nix` | `mirror` | `TailnetClient` + `PersonaDevelopment` |
| repository-ledger | `modules/nixos/repository-receive.nix` | `repository-ledger` | `PersonaDevelopment` w/ `GitoliteServer` |
| criome | `modules/nixos/criome.nix` | `criome` | `services.criome.enable` option (not horizon-gated) |
| lojix-daemon | `modules/nixos/lojix.nix` | `lojix-daemon` | `PersonaDevelopment` node service |

FACT — **The core federation daemons have no NixOS service module at all**: persona, mind, mentci(-lib/-egui), nexus, listener, orchestrate, spirit, sema. None of their repos export a `nixosModules` flake output (checked across all 14). They exist only as crates/binaries. INFERENCE — you cannot declaratively bring the persona/mind/mentci/nexus/spirit federation up on a host today; only the router/mirror/ledger/criome/lojix perimeter is packaged.

FACT — **No composite "run the whole federation" node role exists** — each module is independently gated; there is no parent role.

FACT — Live corroboration on ouranos: `repository-ledger.service` = active (running, since Jun 20); `mirror.service` = **crash-looping** (`activating (auto-restart)`, `ExecStart=…mirror-0.1.2/bin/mirror-daemon … status=1/FAILURE`); stale `persona-spirit-daemon-v0.x` **user** units are all `not-found/dead`; `criome-daemon` and `mentci-daemon` run only as ad-hoc debug/demo processes under `/tmp/*sandbox` and tmux, not as deployed services.

## 4. CriomOS-test-cluster's role

FACT — It is a **regression-test fixture, not a deploy target for real nodes** (`CriomOS-test-cluster/README.md`: "Independent fixture cluster… intentionally not `goldragon`… prove CriomOS consumes projected Horizon data without production names/secrets leaking"). Contents: `flake.nix` (test harness) + `clusters/fieldlab.nota` (7 synthetic nodes: atlas, beacon, cedar, dune, mercury, edge-desktop, base-home) + two deliberately-invalid fixtures.

FACT — Its flake exposes: `nix flake check` pure checks (horizon projection, module rendering, source-constraint audits); auto-generated per-node **`vm-<node>` runNixOSTest** checks; a "deployer node deploys the TARGET's projected config" runNixOSTest under KVM; and apps that run on the **real prometheus** node: `run-on-prometheus`, `build-dune-on-prometheus`, `nspawn-dune-on-prometheus`, `nspawn-spirit-upgrade-on-prometheus`, plus a `spirit-nspawn-toplevel` package (threads in `persona-spirit` v010/v011 + `upgrade`).

INFERENCE — So the test-cluster **can host a "full-system" deploy only as a contained test**: runNixOSTest microVMs and nspawn toplevels (including a spirit-daemon nspawn) built/run on prometheus. This is exactly the `lojix/ARCHITECTURE.md:231-239` "testing and deployment are one function; ordinary contained vs meta production" split. It is the natural pre-production gate — not a place where the federation runs persistently.

## 5. Ranked blocker list (to "the whole federation running together")

1. **No system packaging for the core federation daemons** (persona, mind, mentci, nexus, listener, orchestrate, spirit, sema). FACT. Biggest gap: most of the federation cannot be declaratively deployed at all. Needs NixOS modules + units + horizon gating.
2. **No composite federation node role.** FACT. Even the packaged five are gated piecemeal; nothing composes them.
3. **lojix cutover incomplete.** FACT. Only prometheus is `Current`; ouranos/others unrecorded; 0.4.0 landed but 0.3.10 runs; no `gcroots/criomos` tree here.
4. **LiveActivation (Switch) unproven on real production nodes.** INFERENCE. Only BootOnce is evidenced (`prometheus … BootOnce`); large-AI guidance (`CriomOS/ARCHITECTURE.md:78-88`) mandates BootOnce over Switch for prometheus, so Switch remains unexercised on metal.
5. **lojix production-cutover bar not met** (`lojix/ARCHITECTURE.md:45`, `:201-206`): SSH-survivable job actor decoupling, durable self-resume with the acknowledged **torn-write reconciliation gap**, and end-to-end validation against a full routed microVM with its own Criome domain (Spirit `se72`).
6. **A deployed federation daemon is currently failing:** `mirror.service` crash-loops on ouranos. FACT.
7. **criome not horizon-driven / credential custody future.** FACT/INFERENCE. `criome.nix` is option-gated, not role-gated; criome runs only as demo processes; production credential custody through criome (Spirit `h03z`) and GitHub-auth flake resolution (Spirit `2qhw`) are still open in `lojix/ARCHITECTURE.md:255-270`.
8. **forge absent.** FACT. Build authorization stays on raw nix + the operator's SSH/GPG agent (`lojix.nix:56` `SSH_AUTH_SOCK=…gpg-agent.ssh`); the Criome-authorized build future is not here.

## 6. Recommended staged deploy path (RECOMMENDATION / INFERENCE)

Aligned to lojix/horizon conventions (meta-lojix Deploy → build-on-target → BootOnce → Query verify; contained test in test-cluster before metal):

- **Stage 0 — refresh the operator daemon.** Build+deploy lojix **0.4.0** to ouranos, restart `lojix-daemon`, re-run the read-only Query to confirm state survived (sema-engine resume). Removes the 0.3.10/0.4.0 skew before anything else.
- **Stage 1 — one packaged daemon on one host.** Use a daemon that already has a module. First fix `mirror.service` (it's failing) or start with `persona-router` (self-contained). Deploy via `meta-lojix Deploy … BootOnce` to a safe node; verify the unit + `lojix Query`.
- **Stage 2 — prove activation depth in containment.** Exercise `DeployIntoTestVm`/runNixOSTest in `CriomOS-test-cluster` (the `vm-<node>` checks) to prove Switch/LiveActivation and full-closure activation without risking metal; then a single real edge node (`zeus`, `NodeService::[]`/Edge — low blast radius) for a live Switch.
- **Stage 3 — package the missing core daemons (the critical path).** Add CriomOS NixOS modules for persona, mind, mentci, nexus, listener, orchestrate, spirit — following the existing `criome.nix` / `persona-router.nix` pattern (package from the crate's flake, define the systemd unit, gate on a horizon `NodeService`). This is the largest and highest-value work item.
- **Stage 4 — compose a federation role.** Introduce one horizon `NodeService` (e.g. a `PersonaFederation` variant in horizon-rs) that turns on the daemon set together; validate the whole set in a test-cluster runNixOSTest VM end-to-end before any metal.
- **Stage 5 — complete cutover.** Migrate all `goldragon` nodes into the lojix live set, close the durable self-resume torn-write gap, land criome credential custody + GitHub-auth, then deploy the federation role to a production node.

## 7. Unknowns / not checked

- **Module vs live-daemon config mismatch (flagged UNKNOWN).** `CriomOS/modules/nixos/lojix.nix:27` hardcodes the daemon config as `(goldragon prometheus Hermetic github:LiGoldragon/CriomOS-test-cluster …)` — naming **prometheus** as a config field and the **test-cluster** as proposal source — yet the live daemon on ouranos operates on **goldragon** production data (generated-inputs + Query). I did not decode the running `/run/lojix/startup.rkyv` (binary), so whether the checked-in module reflects the live config, is a test default, or the running daemon predates the current module text is unresolved.
- I did **not** run any `meta-lojix` mutation, deploy, activate, or build (per brief). Only one read-only `lojix Query` (ByNode goldragon/prometheus) was executed; I did not enumerate other nodes/kinds or the event log.
- I did **not** verify remote node live state (only prometheus's remote-builder SSH was observed passively); no `ssh root@<node>` was run.
- Whether ouranos's 22 generations were built by legacy `nixos-rebuild` vs unrecorded lojix runs is INFERENCE from the empty gcroots tree + single-row live set, not proven.
- `lojix/src/{daemon.rs,schema_runtime.rs}` were read at grep depth, not line-by-line; the exact set of `HostDeployAction` variants the 0.4.0 runtime accepts on the wire was not exhaustively enumerated.
- `CriomOS-pkgs/README.md` is empty; its overlay contents were not audited.
- Two read-only `Explore` sub-agents were used for the persona-packaging and cluster-data sweeps (their conclusions are folded in and independently corroborated above by `criomos.nix`, the Query, and the generated-inputs tree). Note: these launched in background mode by the harness despite the "no background sub-agents" intent — flagging for transparency.