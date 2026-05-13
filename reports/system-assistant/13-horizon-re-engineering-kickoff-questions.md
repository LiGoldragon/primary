# 13 — Horizon re-engineering: kickoff plan and open questions

Date: 2026-05-14
Role: system-assistant
Frames: user direction this session — start the refactor on a branch so production stays stable; integrate horizon schema work + cluster-policy extraction + new daemon work; new daemon and new CLI in a `lojix` repo (not `lojix-cli`); CriomOS / CriomOS-home use parallel branches; create beads; focus first work on horizon; surface anything unclear before starting.
Reads (this session): `lojix-cli/ARCHITECTURE.md`, `lojix-daemon/ARCHITECTURE.md`, `signal-lojix/ARCHITECTURE.md`, `forge` repo via `gh api` (its ARCHITECTURE.md, README.md, Cargo.toml), `~/primary/reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md`, `~/primary/skills/beads.md`, current open beads under `role:system-specialist`, `bd show primary-sff/primary-q3y/primary-a61/primary-da7`.
Pairs with: `~/primary/reports/system-assistant/12-horizon-re-engineering-combined-audit.md`.

---

## Frame

Three workstreams I'd been treating separately are one effort:

1. **Horizon re-engineering** (report 12) — `proposal::*` / `view::*` boundary split + 19 schema changes.
2. **Cluster-policy extraction from CriomOS / CriomOS-home Nix** (report 119, plan 04) — typed records replacing literal Wi-Fi / DNS / LAN / VPN / AI / containment policies.
3. **New lojix daemon** — long-lived deploy orchestrator (per plan 04 §P5, current skeleton repos).

The user's specific directives:
- Work happens on branches; production main stays stable.
- New schema is consumed by the **new daemon**, not by current `lojix-cli`. lojix-cli stays at the old schema until cutover; retires after CriomOS migrates.
- Daemon and new CLI live in **one repo**, named `lojix`.
- CriomOS / CriomOS-home use parallel branches that consume the new daemon's projection.
- File beads for the work.
- Focus initial work on horizon.

Several substantive ambiguities surfaced during research. This report names them, proposes resolutions, and asks for confirmation before any branch or bead lands.

---

## What I found

### The lojix repo space — five repos, three differ from each other

| Repo | Purpose | Status |
|---|---|---|
| `lojix-cli` | Current monolithic deploy CLI (project + build + copy + activate). Production. | Active, transitional. |
| `lojix-archive` | First-generation archive. | Frozen. |
| `lojix-daemon` | New deploy daemon — long-lived orchestrator per plan 04 §P5. | **Skeleton only** (created earlier this conversation). No code. |
| `signal-lojix` | New wire contract crate. | **Skeleton only** (created earlier this conversation). No code. |
| `forge` (formerly named `LiGoldragon/lojix`) | **A different daemon entirely** — the criome-stack executor: receives effect-bearing signal verbs from criome, links prism (records → Rust source), spawns nix, writes outputs into arca. Not part of deploy. | Has 38 KB of code; last pushed 2026-05-11; uses `ractor` + `signal-forge` (older naming). |

**Confusion alert:** GitHub redirects `LiGoldragon/lojix` → `LiGoldragon/forge` because `forge` was previously named `lojix`. Anyone who navigates to "the lojix repo" via `github.com/LiGoldragon/lojix` lands at `forge`, which is a criome-stack executor, not the deploy daemon you're asking about.

### Existing bead `primary-sff` proposes a different daemon shape

Bead `primary-sff` (open, P2, was blocked by `primary-q3y` which closed today) names this layout:

> Crate layout:
> - `lojix-cli/` becomes a **workspace** with `core/`, `cli/`, `daemon/`.
> - `lojix-core/`: existing deploy.rs/build.rs/copy.rs/activate.rs/etc. moved whole-file.
> - `lojix-cli/` (renamed from current monolith): thin main.rs only.
> - `lojix-daemon/`: long-lived state, GC roots, event log, container lifecycle observer.
> - `signal-lojix/`: NEW REPO with wire records.

Three competing shapes for "where the daemon lives":

- **(α) Cargo workspace inside the existing `lojix-cli` repo** with `core/`, `cli/`, `daemon/` member crates. Bead `primary-sff`'s plan.
- **(β) Three separate repos** — `lojix-cli` (thin client), `lojix-daemon` (daemon), `signal-lojix` (wire). Current skeletons; matches `protocols/active-repositories.md`.
- **(γ) Two repos** — `lojix` (one crate, `[[bin]] name = "lojix-daemon"` + `[[bin]] name = "lojix"`) + `signal-lojix` (wire). Matches your direction this session ("one repo for daemon and CLI") and `~/primary/AGENTS.md` §"Binary naming — `-daemon` suffix".

### Plan 04 already designed substantial parts of this

`reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md` (landed 2026-05-12) has comprehensive design for material that report 12 doesn't cover:
- `ContainmentSubstrate` (`NixosContainer | MicroVm`) and `WorkloadSubstrate`
- `NodePlacement` variants (`Metal | Contained`) with `ContainedPlacement { host, substrate, resources, network, state, trust, user_namespace_policy }`
- `UserNamespacePolicy ::= PrivateUsersPick | HostRootMappingAllowed { reason, approved_by }` (data-driven, not trust-gated)
- `SecretReference { name: SecretName, purpose: SecretPurpose }` + `ClusterSecretBinding { name, backend }` + `SecretBackend ::= Sops | SystemdCredential | Agenix` on `Cluster`
- `BinaryCache`, `BinaryCacheEndpoint`, `PublicDomain ::= Criome(...) | External(...)` (mixed internal/external domains)
- `Horizon { node, ex_nodes, contained_nodes: BTreeMap<NodeName, ContainedNodeView>, users, cluster }` — one level of containment by type, not by policy
- `HostPublicEndpointRoute` derived projection for the reverse-proxy module
- `NodeSpecies::Publication` (new variant for Ghost, the publication node)
- `BuilderSelection ::= Local | DispatcherChooses | Named(NodeName)` replacing `Option<NodeName>`
- daemon shape: LiveSetActor, GcRootActor, EventLogActor, ContainerLifecycleActor

Report 12 didn't cite plan 04 (oversight). Plan 04 + report 12 integrate cleanly: plan 04 owns placement/containment/secrets/Ghost; report 12 adds the boundary principle, Wi-Fi/DNS/LAN/VPN/AI policy, and the language split. The migration order needs to fold both.

### Existing beads to leverage

| Bead | Title | Aligns with |
|---|---|---|
| `primary-a61` (open, P2) | CriomOS: move router Wi-Fi policy and SAE secret out of Nix modules | Migration step 5 |
| `primary-sff` (open, P2) | lojix: extract lojix-core, add lojix-daemon, create signal-lojix contract crate | Daemon work; needs revision per Q1 |
| `primary-1ha` (open, P2) | CriomOS-test-cluster: negative Horizon fixtures for role invariants | Step 15 |
| `primary-58l` (open, P2) | CriomOS-test-cluster: VM/nspawn smoke for DNS/tailnet roles | Step 4 |
| `primary-tpd` (open, P2) | Review headscale and Yggdrasil roles in CriomOS | Step 13 |
| `primary-da7` (open, P3) | lojix (or successor): query cluster DB for host registration mismatches | Future, post-cutover |

Reusing existing beads keeps the surface small and preserves prior context (acceptance criteria, comments, blockers).

---

## Open questions blocking start

### Q1 — The lojix repo

| Option | Shape | Pro | Con |
|---|---|---|---|
| **(α)** | `lojix-cli` repo restructures into Cargo workspace with `core/`, `cli/`, `daemon/` member crates. `signal-lojix` separate. | Matches existing bead `primary-sff`. Preserves git history. One place for all deploy code. | Doesn't match your wording ("different repository as opposed to lojix-cli"). Modular-monolith failure-mode risk per ESSENCE §"Micro-components". |
| **(β)** | Three repos: `lojix-cli` (thin client), `lojix-daemon` (daemon), `signal-lojix` (wire). | Matches current skeletons + `active-repositories.md`. Clean micro-components. | Doesn't match your "one repo for daemon and CLI" direction. The `-daemon` suffix on a repo holding both binaries reads oddly. |
| **(γ)** | Two repos: `lojix` (one crate; `[[bin]] name = "lojix-daemon"` + `[[bin]] name = "lojix"`) + `signal-lojix` (wire). | Matches your wording. Repo name = lib name = CLI binary name. Daemon binary follows `-daemon` suffix convention from `~/primary/AGENTS.md`. | Requires either renaming `lojix-daemon` → `lojix` (breaks GitHub redirect from `lojix` → `forge`) or creating fresh `lojix` repo. Existing skeleton's commit gets re-housed. |

**Recommendation: (γ).** It's the most literal reading of your wording and `~/primary/AGENTS.md` §"Binary naming." Concrete moves under (γ):
1. Decide what to do with `forge`'s GitHub redirect from `lojix` (see Q2).
2. Either rename `lojix-daemon` → `lojix` (preserves the skeleton's one commit) or create fresh `lojix` and copy in the docs from the skeleton.
3. Update `protocols/active-repositories.md` to remove `lojix-daemon`, add `lojix`, and clarify `forge` is the criome-stack executor (not deploy).
4. Update `primary-sff` description to match the new shape.
5. The new `lojix` repo holds: `Cargo.toml` (one crate), `src/lib.rs`, `src/bin/lojix.rs` (CLI), `src/bin/lojix-daemon.rs` (daemon), and the actor modules per plan 04 §P5.

**Need confirmation:** is (γ) what you want?

### Q2 — `forge` and the new lojix daemon

`forge` is the **criome-stack executor**: receives effect-bearing signal verbs from the criome daemon (sema records validator), links `prism` (records → Rust source), spawns nix builds, writes outputs into `arca`. It's part of the eventual sema-runtime stack.

The new lojix daemon is the **deploy orchestrator**: receives `signal-lojix` deploy requests from operators over UDS, projects horizon, runs build/copy/activate, owns live-set + GC-roots + container-lifecycle observability.

Three possibilities:

- **(a) They're genuinely different.** `forge` belongs to the eventual criome stack; `lojix` belongs to today's deploy. They coexist; eventually `forge` absorbs deploy too (Sema-on-Sema), but for now they're separate. Action: leave `forge` alone. (γ) needs to handle the GitHub redirect by either claiming `lojix` first or accepting that the redirect breaks.
- **(b) `forge` is an older attempt at what `lojix-daemon` is now**, due to be archived. Action: archive `forge` (or rename it descriptively); reclaim `lojix` as the deploy daemon.
- **(c) `forge` and the new lojix daemon should converge** — one daemon for criome-validator-driven builds AND operator-initiated deploys. Action: pause Q1 until the convergence shape is designed.

I have no evidence for (b) or (c) from `forge`'s docs or recent reports — its architecture is substantially different (different actors, different upstream daemon, different downstream sink). **(a) seems most likely**, but you have context I don't.

**Need confirmation:** which possibility holds?

### Q3 — Plan 04 ↔ Report 12 integration

Report 12 missed plan 04's container/placement/Publication design. Report 12 + plan 04 fold cleanly into one migration order. Below is the proposed order — 15 steps including the 12 from report 12 and three from plan 04 (placement / containment, Publication species, contained-node view in Horizon).

| # | Step | Source | Open decisions |
|---|---|---|---|
| 1 | `proposal::` / `view::` namespace split (every compound straddling type splits into two distinct types translated by the projection) | Report 12 row 19 | none |
| 2 | `SecretReference { name, purpose }` + `ClusterSecretBinding` + `SecretBackend ::= Sops \| SystemdCredential \| Agenix` | Plan 04 §P1.1 | none — plan 04 already detailed |
| 3 | `Cluster.identity { internal_zone, public_zone }` + rename `criomeDomainName` | Report 12 row 5 | §8 (granularity), §9 (rename now/later) |
| 4 | `Cluster.lan: LanNetwork` + `Cluster.resolver: ResolverPolicy` | Report 12 rows 7, 8 | §4 (br-lan policy or constant) |
| 5 | `Cluster.wifi_networks` + `RouterInterfaces.wlans` (plural) + `WifiAuthentication ::= Wpa3Sae \| EapTls` + cert records | Report 12 rows 4, 6 | §10 (WiFi password during transition); bead `primary-a61` |
| 6 | `NodePlacement ::= Metal { … } \| Contained { … }` + `ContainmentSubstrate` + `UserNamespacePolicy` + Pod migration | Plan 04 §P1.1, §P1.2 | does plan 04's containment shape still hold? |
| 7 | `NodeCapabilities { binary_cache, build_host, container_host, public_endpoint }` + `BinaryCacheEndpoint` + `PublicDomain` | Plan 04 §P1.1 + Report 12 rows 14, 15 | §5 (capabilities/pubkeys boundary) |
| 8 | `Horizon { contained_nodes: BTreeMap<NodeName, ContainedNodeView>, … }` + `ProjectedNodeView` (one level deep) + `HostPublicEndpointRoute` derived | Plan 04 §P1.4, §P1.5 | none — plan 04 detailed |
| 9 | `NodeSpecies::Publication` + Ghost as a Publication node | Plan 04 §P6, §P6.4 | Ghost workload (native NixOS service vs OCI container) per plan 04 §"Decisions still owed" |
| 10 | `Cluster.ai_providers` | Report 12 row 10 | none |
| 11 | `Cluster.vpn_profiles` + per-node `vpn_memberships` | Report 12 row 11 | §7 (cluster vs node ownership) |
| 12 | `Machine` data-bearing enum (`Metal { … } \| Pod { … }`) + `KnownModel` direct | Report 12 rows 1, 2 | §2 (KnownModel closed/open), §3 (Pod/Metal shared resource fields) |
| 13 | `TailnetRole` collapse + `Cluster.tailnet` factor-out | Report 12 rows 3, 9 | §6 (tailnet TLS in Horizon vs runtime) |
| 14 | Address grouping in `view::Node` (preserve `YggdrasilEntry`) + delete `hasSshPubKey` | Report 12 rows 16, 17 | none |
| 15 | Source-constraint tests over `CriomOS/modules` + `CriomOS-home/modules` forbidding production literals | Report 12 row 18 | none; beads `primary-1ha`, `primary-58l` |

**Need confirmation:** does the integrated 15-step order work? Did plan 04's containment shape survive intact (no revisions since 2026-05-12)?

### Q4 — Branch naming

Proposed: `push-horizon-re-engineering` across all affected repos.

Repos that get a branch:
- `horizon-rs` — schema work (steps 1-2, 6-9, 12-14)
- `lojix` (or whatever Q1 resolves to) — daemon implementation
- `signal-lojix` — wire contract evolution
- `CriomOS` — consumer rewrites (every step that changes the output)
- `CriomOS-home` — consumer rewrites
- `goldragon` — `datom.nota` updated to new schema (after horizon-rs lands the typed shapes)

Repos untouched: `lojix-cli` stays at current schema; retires after cutover.

**Need confirmation:** is the branch name OK? Other naming preference?

### Q5 — Bead structure

Two shapes:

- **(a) Just the 15 step beads.** Each is a `task` under `role:system-specialist` naming the migration step + acceptance criterion. No epic. Reuse `primary-a61` for step 5; reuse and update `primary-sff` for the daemon work; file 13 new beads for the rest.
- **(b) Epic + 15 sub-task beads.** A parent `feature` bead ("horizon re-engineering — meta") with `bd dep` blocking by each step bead. Closes when all sub-beads close.

Skill `~/primary/skills/beads.md` doesn't strongly recommend either. (a) is lighter; (b) gives a single referenceable handle for "the whole arc."

**Need preference.**

### Q6 — Open design decisions from report 12

Of report 12's 11 decisions, two are already implicitly resolved:
- §1 user tool secrets — DEFERRED ("focus on horizon")
- §11 lojix-cli bump strategy — MOOTED (new daemon path; lojix-cli stays at old schema)

The other nine still need answers — see "Open decisions" column in the table above. They can be answered in batch now, or as each step comes up. Step 1 (namespace split) needs none of them, so work can start there immediately once Q1, Q4, Q5 resolve.

---

## What I'm NOT doing yet, and why

You asked me to "create the beats for that and start working on what you think you can work on." I'm holding off on both because:

- Filing beads now commits to a structure (Q5) and a daemon shape (Q1) that are the questions above.
- Creating branches commits to a name (Q4) and a target repo for the daemon work (Q1).
- Starting work on horizon step 1 needs a branch to land it on.

The cost of resolving Q1, Q2, Q4, Q5 in your next message is a few minutes of your time; the cost of guessing wrong is unwinding branches and beads under attention.

**If you'd prefer I move on something low-risk while waiting:** step 1 (the `proposal::`/`view::` namespace split) is pure Rust refactoring inside `horizon-rs` with no schema-shape change and no consumer-side impact. I could land it on a branch named `push-horizon-namespace-split` (or your preferred name) without committing to anything else. Say the word.

---

## Sources

- Reports: `04-dedicated-cloud-host-plan-second-revision.md` (the substantive plan), `12-horizon-re-engineering-combined-audit.md` (this report's predecessor), `119-horizon-data-needed-to-purge-criomos-literals.md` (CriomOS literal leaks).
- Skeletons + ARCH docs: `lojix-cli`, `lojix-daemon`, `signal-lojix`, `forge`.
- Beads via `bd ready --label role:system-specialist`, `bd show primary-sff`, `bd show primary-q3y` (closed today), `bd show primary-a61`, `bd show primary-da7`.
- GitHub via `gh api repos/LiGoldragon/{lojix,forge}` + raw content of `forge`'s `ARCHITECTURE.md`, `README.md`, `Cargo.toml`.
- Skill: `~/primary/skills/beads.md` — bead lifecycle.
- Workspace docs: `~/primary/AGENTS.md` §"Binary naming — `-daemon` suffix"; `~/primary/protocols/active-repositories.md` — current repo map.
- User direction this session: refactor branches, integrate three workstreams, daemon + CLI in `lojix` repo, focus on horizon, surface unclear architecture before starting.
