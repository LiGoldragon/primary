# The CriomOS / Lojix / Horizon stack: vision, current state, and end-shape

Flow 674a4dab, 2026-08-28. Every current-state claim below was verified at
`origin/main` of each repository (the /git working copies were found behind
main — see "Cause 5"). Psyche quotes are verbatim; the per-plane acquisition
reports in this directory carry their transcript lines.

## 1. The stack the psyche described

Read from the transcripts (2026-05 → 2026-08-28), the psyche's own words draw
seven planes, each with one job and one source:

```
  authored by the psyche                 ┌──────────────────────────────┐
  ──────────────────────                 │ manifests/<node>.datom        │
  goldragon/cluster.datom                │ deploy selection per node     │
   "a bunch of dials to turn shit        └──────────────┬───────────────┘
    on and off" — variants, no booleans                 │
  criomos-horizon-config/horizon.datom                  │
   pan-horizon constants (domains, LAN)                 │
   "there shouldnt be criome and                        │
    criome.net in cluster data"                         │
          │                                             │
          ▼                                             ▼
  ┌─────────────────────┐        ┌────────────────────────────────────┐
  │ Horizon (horizon-rs)│        │ Lojix (OS-only daemon + lojix CLI  │
  │ "mostly just the    │──────▶ │  + meta-lojix CLI, signal messages)│
  │  reducer"           │        │ "CLIs cannot accept any other type │
  │ WHAT, never HOW     │        │  of argument than the typed input" │
  └─────────────────────┘        └───────────────┬────────────────────┘
                                                 │ Horizon → Nix, at deploy
                                                 ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ criomos-core  (supersedes CriomOS-lib; "indirection is bad design")  │
  │  • interprets Horizon for Nix (isEdge, builderConfig, cacheUrls …)   │
  │  • derivations "declared once, used everywhere" (codex, claude …)    │
  │  • the one nixpkgs pin every consumer follows                        │
  └───────────────┬───────────────────────────────────┬──────────────────┘
                  ▼                                   ▼
  ┌───────────────────────────┐        ┌──────────────────────────────────┐
  │ CriomOS (OS modules)      │ embeds │ CriomOS-home (Home modules)      │
  │ network-neutral, no host  │──────▶ │ "no difference between the       │
  │ names in control flow     │ thin   │  embedded and independent home"  │
  └───────────────────────────┘        └──────────────────────────────────┘
```

The daemon/CLI/meta-CLI/signal shape is the psyche's own ("Everything is in
the daemon. So this is my vision from the very beginning", 2026-08-08). The
reducer, the dials, the single shared source, the minimal flake, and the
identical Home are all the psyche's words (reports `psycheHorizon.md`,
`psycheOsHomeGoldragon.md`, `psychePackagesSources.md`, `psycheLojix.md`).

## 2. The stack as it is (origin/main, 2026-08-28)

```
  goldragon/datom.dotos ──(Dotos syntax, 8 nodes, 2 users)──┐
  criomos-horizon-config/horizon.dotos ── NO CONSUMER        │
  CriomOS-lib constants (LAN, ports, paths) ──────────┐      │
                                                      │      ▼
  horizon-rs 6.5k lines: ClusterProposal ──▶ Node ≈54 fields (35 derived
     booleans/policies), species 11 + services 7, hardcoded domain suffixes
                                                      │      │
  lojix 21k lines: 2 sockets, redb store (10 tables), │      │
     5-stage pipeline, writes 4 content-addressed     │      │
     flakes, overrides CriomOS stub inputs ───────────┼──────┘
     no durable Deploy.Host request → agent composes it │
                                                      ▼
  CriomOS 9.2k lines Nix ── pkgs := (head criomos-home.homeConfigurations).pkgs
     │ 9 follows into Home; passes constants (dead) + horizon to embedded Home
     ▼
  CriomOS-home 15k lines Nix, 73 inputs, 4 nixpkgs revisions, 61 checks,
     owned-agents/ + criomos.corePackages option, prometheus + /home/li hardcoded
  CriomOS-pkgs: 4 overlays on the LiGoldragon nixpkgs fork
```

## 3. Findings, by plane

Severity: **blocks** a design the psyche stated · **duplicates** a source ·
**unasked** machinery · **cosmetic**. Origin: who put it there.

### Cluster data and pan-horizon constants

| What it is | What is wrong | Sev. | Origin |
|---|---|---|---|
| `criomos-horizon-config` (HorizonProposal: domain suffixes, LAN, DHCP) | Nothing reads it — not horizon-rs, lojix, CriomOS, or CriomOS-home. Its facts live again in `horizon-rs/lib/src/domain.rs:108,121` (hardcoded defaults), `goldragon/datom.dotos:276`, and `CriomOS-lib/lib/default.nix:88-91`. | blocks · duplicates | agent extraction 2026-05-17, never wired |
| `goldragon/datom.dotos` | Named datom, written in Dotos; the psyche: "There should be no Dotos files anymore" (2026-08-26). Positional bare booleans at data positions; every trust entry is Max. | blocks | Dotos rename 2026-07-31 (agent) |
| `goldragon/synchronizer.dotos` | References `datom.nota`, a file that no longer exists. | cosmetic | stale rename |

### Horizon

| What it is | What is wrong | Sev. | Origin |
|---|---|---|---|
| `Node` output (~54 fields) | BehavesAs (11 bools), is_*/has_* (16), ComputerIs (5), LidSwitchAction (3), builder_configs, cache_urls, admin_ssh_pub_keys are all derivable in Nix from authored facts. "Horizon should mostly be just the reducer … We're just inflating the Rust code." | blocks | living's 2026-04-23 scaffold; grown by agents |
| `NodeSpecies` (11) + `NodeService` (7) | Two axes for one thing; the 2026-05-21 intent to merge into one `roles` vector was never implemented and never re-confirmed. TestVm/CloudNode species added by agents. | blocks | agents, May–Jul |
| `*Proposal` in-types vs `Node/User` out-types | Parallel type families the psyche asked not to have ("should not repeat themselves across inputs and outputs"). | unasked | scaffold |
| Test fixtures | Repeat production node names (5 files) and `lojix/tests/deploy_transport_integration.rs`. | cosmetic | agents |

Resolved on main: AgentIntercomLocal/Graphical removed from the schema.

### Lojix

Aligned with the psyche: OS-only (a check enforces it); CLIs reject flags;
no host names in code; three-repo shape (lojix, signal-lojix,
meta-signal-lojix); Lojix is the only deployment interface.

| What it is | What is wrong | Sev. | Origin |
|---|---|---|---|
| The `Deploy.Host` request | Exists nowhere durable: each deployment's 13-field typed input is composed by an agent in the moment. Flow 01a048a6's "no authoritative `manifests/*.dotos`" block was a conflation — that CLAUDE.md line is about Curriculum skill deployment (`manifests/active-outputs.dotos`, deleted 2026-08-25); Lojix has no manifest concept. | blocks | conflation, 01a048a6 |
| `Query.ByDeployment` | `schema_runtime.rs:4187` hard-codes `false` in the live-generation filter → always empty generations; no test covers it. | blocks | agent, untested |
| `CheckHostKeyMaterial` | `schema_runtime.rs:4276-4283` returns `Vec::new()`; nothing anywhere consumes it. A contract on the wire that does nothing. | unasked | agent |
| `runtime_flow.rs` / `runtime_model.rs` | 11 identical type pairs (NixStoreUri, SshDestination, DeploymentTransport, DeploymentInputMode, FlakeAttribute, DeploymentOutputSelector, ActivationBackend, NixBuilderSpec, NixSystem, ExtraSubstituter, TestExecutionProfile) plus DeploymentPhase/DeploymentLifecycle; converted by scattered inline code. | duplicates | agent, 2026-08-06, session with zero psyche messages |
| Deploy request (13 positional fields) | `DeploymentInputMode::Direct` (a path that bypasses Horizon), per-request builder, substituters, output selector: no psyche ask. Transport, activation backend, action, source policy trace to the psyche. | unasked | agent, 2026-08-04 |
| Sema store (10 tables), Watch contracts | `container-lifecycle` is written and never queried; `WatchDeployments`/`WatchCacheRetention`, outbox and transition-intent have no consumer outside lojix. 21,255 lines for an eight-node cluster; the whole internal architecture was built in June sessions with no psyche transcript. | unasked (partly) | agents, June 2026 |
| 13 untracked `.beads/` files | Agent tooling residue in the checkout. | cosmetic | beads |

### Shared ground (criomos-core / CriomOS-lib / CriomOS-pkgs)

| What it is | What is wrong | Sev. | Origin |
|---|---|---|---|
| `criomos-core` | Does not exist. The psyche ruled it supersedes CriomOS-lib (2026-08-25) and placed the Codex/Claude derivations in it (2026-08-27); it was deferred "right now" for a Home option, which now exists (`criomos.corePackages.{codex,claude}`). CriomOS-lib still carries constants (LAN, ports, paths) that belong to Horizon or core. | blocks | psyche-deferred |
| `CriomOS/flake.nix:160` `pkgs = (head (attrValues criomos-home.homeConfigurations)).pkgs` | The OS takes its package set from the first Home configuration of the Home repo — the exact indirection the psyche named the next day ("indirection is bad design"). | blocks | agent, 2026-08-23 |
| `CriomOS-pkgs` | A separate repository for four overlays and the nixpkgs pin; the psyche accepted it in April ("fine, just create another repo then") but core is now the ruled home of shared ground. | duplicates | agent extraction, psyche-accepted |
| `normalize.nix:174` `nixpkgs.overlays = mkOverride 0 []` | Overlays forced off at priority 0 ("Overlays are bad") while CriomOS-pkgs and CriomOS-home both apply overlays elsewhere — two overlay mechanisms. | unasked | archive legacy |

### Packages and sources

| What it is | What is wrong | Sev. | Origin |
|---|---|---|---|
| Four nixpkgs revisions in one deploy closure | The LiGoldragon fork plus herdr's, orca-ide's and stylix's own nixpkgs, none following. Measured: three distinct glibc store paths (~38 MB each) and the same multiplication across every transitive dependency. One `follows` line per input removes two of them. | blocks · duplicates | agents (herdr/orca added 2026-08-23 without follows) |
| `github:LiGoldragon/nixpkgs?ref=main` | The fork has zero commits of its own; every patch lives in CriomOS-pkgs overlays. The fork is a moving `ref=main` indirection in front of a plain upstream revision. | unasked | never discussed with the psyche |
| `nix-vscode-extensions` overlay | Applied in CriomOS-pkgs and again in CriomOS-home `packageOverlays`. | duplicates | agents |
| Rust toolchains | rust-build (spirit, orchestrate, dotos, datom) versus direct crane+fenix (lojix, agent, aggregator, message, listener): two providers of one thing across the repos the OS consumes. | duplicates | historical |
| Claude Code VSIX / CLI versions | Pinned in two places (VSIX URL 2.1.250; `hashes.json` 2.1.250) with no coupling; the binary is forced to `corePackages.claude`, so the skew is cosmetic — but "we should have a way that ensures the tui and desktop versions line up". | cosmetic | agents |

Aligned on main: `criomos.corePackages.{codex,claude}` is consumed by every
Home path (CLI, remote control, VSCodium extension, Claude Desktop's patched
asar, ChatGPT Desktop's wrapper) — the interim shape the psyche asked for on
2026-08-27; no stateful installation was found; the ~48 non-flake inputs are
each the single source for their tool.

### OS and Home

| What it is | What is wrong | Sev. | Origin |
|---|---|---|---|
| Embedded Home inputs | `userHomes.nix:44` still passes `constants` from the OS (now dead: `CriomOS-home/flake.nix:765` mkForces constants from Home's own CriomOS-lib input). Both Homes now agree — but on CriomOS-lib, not Horizon. | blocks (partly) | agents |
| `home.stateVersion = "26.05"` | Three definitions: `CriomOS/userHomes.nix:16`, `CriomOS/normalize.nix:215`, `CriomOS-home/flake.nix:723`. | duplicates | two agents, two sessions |
| `serviceName` parser | `CriomOS/node-services.nix:13` and `CriomOS-home/.../spirit.nix:20` (was three; Home cannot import OS Nix). | duplicates | repo split |
| `prometheus` | Hardcoded SSH matchBlock `CriomOS-home/.../min/default.nix:520-521` and LLM endpoint `pi-models.nix:42`; `/home/li/...` paths `default.nix:87-99`; gopass path `browser-use.nix:71`. "nothing in this should hardwire bird or zeus anywhere". | blocks | agents |
| `mirror.nix:30` `mirrorEnabled = false && …` | A module kept alive by force-disabling it. | unasked | agent |
| `med/element.nix` | Orphan: a system-level service in Home, imported nowhere. | cosmetic | agent |
| compat / migration hooks | `pi-models.nix:81` compat, `spirit.nix:88` migrateObsolete, `spirit.nix:189-201` conflicts list, `default.nix:728` removeDeprecatedCodexCollab, nix-profile-compatibility check. Spirit: "Backward compatibility is never a design variable." | unasked | agents |
| 86 checks (25 OS + 61 Home) | Many grep the source text for a string ("change detectors") rather than prove behaviour; they cost eval time on every change and prove that a file still contains a line. | unasked | agents |
| CriomOS-home inputs | 73 inputs, ~48 non-flake (npm tarballs, VSIX); 4 nixpkgs revisions in one lock: the LiGoldragon fork, plus herdr's, orca-ide's and stylix's own — no `follows`. The psyche asked for VSIX as flake inputs; nobody asked for four nixpkgs. | duplicates | agents |
| `owned-agents/codex/desktop-gate.nix` | A `codex`-named shell wrapper that lets ChatGPT Desktop run only `--version`/`--help`, `app-server daemon version`, and `app-server` (proxied to the managed owner socket); everything else exits 126. Commit 799f8fd, 2026-08-28. You said "we just need the server running for codex and claude, and the desktop apps using it locally" — no gate, wrapper or restriction was asked for; agents built it to realize that line after an earlier packaged gate exited 126. | unasked | agent, 2026-08-28 |

Resolved on main: AgentIntercom follows Claude/Codex presence; desktop apps
gate on Edge + Medium + per-package `meta.platforms`; the blanket x86 gate is
gone; `criomos.corePackages` makes one derivation per tool for every consumer
inside Home.

### Rust estate around the stack

| What it is | What is wrong | Sev. |
|---|---|---|
| `core-schema` = byte-identical `core-ethos` | Frozen duplicate kept for an ethos-engine "compat" pin; name-table pinned at two revisions. | duplicates |
| Leaf crates (content-identity, name-table, signal-frame) | Pinned at different revisions by different consumers. | duplicates |

## 4. How it got this way (causes, kept apart from the findings)

1. **April 2026: an agent rewrite laid the foundations without a record.** The
   four-repo split, the stub-input/override mechanism, the follows web and the
   54-field Node all landed 2026-04-23/27. No transcript survives; the only
   psyche words are quoted inside commit messages. What the psyche later
   criticised (indirection, duplicated constants) is the shape of that week.
2. **June and August 2026: Lojix's internals were built in sessions without the
   psyche.** The two-socket daemon is the psyche's architecture; the store,
   event log, outbox, transition intents, the +11.5k-line durable-transitions
   rewrite (2026-08-04) and the flow/model split (2026-08-06) were autonomous
   agent decisions — the Aug 6 sessions contain zero psyche messages.
3. **Extractions accepted by silence, then never finished.** CriomOS-lib,
   CriomOS-pkgs and criomos-horizon-config were agent-proposed repositories.
   criomos-horizon-config was created and never wired, so its facts were
   re-stated in three other places.
4. **A tentative question captured as a ruling.** "home ostensibly, right?"
   became an implementation in Home until "no, they were moving into
   criomos-core - why did you change the design?"; "that could be a standalone
   repo" became "extended-horizon is a deterministic derivation layer" until
   "you mean that repo already existed?". Each cost hours and left a half-shape.
5. **Agents read stale checkouts.** The /git working copies are behind main
   (CriomOS 11 commits, CriomOS-home 9, 64 files). This flow's own first Nix
   audit reported the AgentIntercomGraphical gate as still present; it was
   gone on main. Any agent auditing or "fixing" from /git repeats work that
   landed, or misses what did.
6. **Local mechanical fixes in place of the structural direction.** pkgs taken
   from the Home flake to make package sets equal (the day before the psyche
   asked for a shared source repo); llm-agents' nixpkgs unfollowed for a pnpm
   attribute; `serviceName` reimplemented because Home cannot import OS Nix;
   a module force-disabled rather than deleted.
7. **Words invented by agents travel as facts.** "manifests/*.dotos" named a Curriculum skill list; a later flow read it as OS deployment selection and declared deployment blocked on a file that had never been meant to exist. This flow repeated it until the psyche asked what the word meant.
8. **Proof theatre.** Checks that grep source text, contracts that return empty
   vectors, queries that hard-code `false` — all pass, none prove.

## 5. The end-shape and how to get there

The diagram in §1 is the end-shape. Concretely:

- **goldragon/cluster.datom** — Datom syntax; per node a `roles` vector of
  self-describing variants (Edge, Center, Router, LargeAi, NixBuilder{…},
  NixCache{…}, PersonaDevelopment…), machine facts, disks, pubkeys; users;
  trust. No booleans at data positions, no derived fields, no domain suffixes.
- **criomos-horizon-config/horizon.datom** — domain suffixes, LAN, operator
  identity; read by horizon-rs as a second input, or, if the psyche prefers
  one authored file, folded into goldragon and the repository deleted.
- **horizon-rs** — the reducer: validate, resolve viewpoint, derive domain
  names and trust, emit ~15 fields per node. Delete BehavesAs, ComputerIs,
  is_*/has_*, LidSwitchAction, builder_configs, cache_urls,
  admin_ssh_pub_keys; delete the parallel in/out type families; read Datom.
- **lojix** — keep: daemon, two sockets, signal contracts, pipeline,
  live-set/gc-roots/event-log/deploy-job/deployment-record. Fix ByDeployment;
  delete CheckHostKeyMaterial, `Direct` input mode, container-lifecycle; fold
  builder/substituter/selector into manifest defaults; one type family. Author
  `manifests/<node>.datom` for Ouranos and Zeus (transport, activation backend,
  action, source policy) — the first slice that makes the cluster deployable.
- **criomos-core** (new; CriomOS-lib and CriomOS-pkgs deleted into it) — the
  nixpkgs pin and its overlays; `lib/horizon.nix` interpreting Horizon
  (isEdge, isNixBuilder, builderConfig, cacheUrls, lidSwitchPolicy,
  sshMatchBlocks from exNodes); the declared-once derivations (codex,
  claude-code, claude-desktop, chatgpt) that CriomOS and CriomOS-home both
  consume directly — the `criomos.corePackages` option moves here.
- **CriomOS** — `pkgs` from core; specialArgs = { horizon; core }; embedded
  Home = `home-manager.sharedModules = [ criomos-home.homeModules.default ]`
  and nothing else; delete mirror.nix, the dead constants, the third
  stateVersion, normalize's overlay clearing.
- **CriomOS-home** — consumes core directly; every input follows core's
  nixpkgs (herdr, orca-ide, stylix); delete prometheus/`/home/li` literals
  (derive from horizon.exNodes / horizon.user), element.nix, compat and
  migration hooks; replace change-detector checks with behavioural ones or
  delete them.

Vertical slices, each leaving the cluster deployable:

1. Write the Deploy.Host requests for Ouranos and Zeus where question 3 puts
   them; fix ByDeployment; deploy main as it stands (proves the deploy path).
2. Create criomos-core with the nixpkgs pin + overlays and `corePackages`;
   point CriomOS and CriomOS-home at it; delete CriomOS-pkgs and the
   pkgs-from-Home line; deploy.
3. Move CriomOS-lib constants: LAN/domains to horizon config, ports/paths to
   core; delete CriomOS-lib; deploy.
4. Horizon: roles merge, derived fields out (into core/lib/horizon.nix), Datom
   in; goldragon to Datom; wire or fold criomos-horizon-config; deploy.
5. Home hygiene: hardcoded hosts and paths, orphans, compat hooks, checks;
   herdr/orca/stylix follow core's nixpkgs; deploy.
6. Lojix trims: dead contract, dead tables, Direct mode, duplicate types.

Every slice deletes the old path in the same change; no compatibility path.

## 6. Distillation proposal (nothing enters Vision/ without approval)

Raw records on four subjects have accumulated across a dozen flows. Proposed
`Vision/` topics and statements, in the psyche's words: **horizon.md** —
"Horizon should mostly be just the reducer"; "the cluster data should be a
bunch of dials"; "there shouldnt be criome and criome.net in cluster data".
**criomosPlanes.md** — "indirection is bad design" / "core is more accurate
than lib"; "there should be no difference between the embedded and independent
home …"; "nothing in this should hardwire bird or zeus anywhere".
**packages.md** — "declared once, used everywhere"; "we dont allow installing
software statefully"; "keep the flake very minimal; an entry point".
**lojix.md** — "it should only be in OS"; "CLIs cannot accept any other type of
argument than the typed input object". Graduation question: "indirection is
bad design" and "declared once, used everywhere" read broader than a topic —
Intent?

## 7. The three questions

1. **What is criomos-core, exactly?** One repository holding (a) the nixpkgs
   pin and overlays, (b) the Nix interpretation of Horizon, and (c) the
   declared-once derivations — with CriomOS-lib, CriomOS-pkgs and the
   `corePackages` Home option all deleted into it? And is "extended-horizon"
   the same thing as (b), or a separate repository?
2. **Where is Horizon's line?** Do you confirm the roles merge (species +
   services → one `roles` vector) and a reducer that emits only authored facts
   plus domain names and trust, every other derivation moving to Nix — and
   does criomos-horizon-config live as Horizon's second input, or die into
   goldragon?
3. **How much Lojix, and where does a deployment request live?** The
   daemon/CLI/meta-CLI shape is yours; the durable store, watch contracts,
   outbox and transition machinery were built without you. Keep them, or cut
   Lojix to the pipeline plus live-set and gc-roots? And the per-node
   `Deploy.Host` typed input (13 fields; four trace to you): an authored,
   durable file — in goldragon, CriomOS, or primary — or composed at deploy
   time from Horizon and shown for approval; and which fields do you choose
   per deployment at all? ("Manifest" was agent vocabulary for this, conflated
   with the Curriculum skill manifest; Lojix has no such concept.)

## Sources

- Psyche acquisition: `psycheOsHomeGoldragon.md`, `psycheLojix.md`,
  `psycheHorizon.md`, `psychePackagesSources.md`, `psycheStackOrigins.md`
  (verbatim quotes with transcript file and line).
- Archaeology: `archaeologyNixSide.md`, `archaeologyRustSide.md`.
- Audits: `auditNixSide.md` (verified at origin/main by a second subflow —
  verdicts in `flows/674a4dab/log.md`), `auditLojix.md` (verified at
  origin/main), `auditHorizon.md` and `auditPackagesSources.md` (written at
  origin/main).
- Witnesses: `witnesses/nixSideMap.md`, `witnesses/rustSideMap.md`,
  `witnesses/workingCopyState.md`.
- Raw psyche records: `flows/01a02b4b/vision/homeEquivalence.md`,
  `flows/01a030a1/vision/commonGround.md`,
  `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`,
  `flows/01a0437d/vision/codexAndClaude.md`, `flows/01a048a6/vision/`,
  `flows/01a04881/vision/`, `flows/55d18f4f/vision/everythingIsInTheDaemon.md`,
  `psyche-raw/Vision/`.
- Flows remembered: 01a048a6, 01a04881 (depth 1); 01a0437d, 01a030e8,
  01a030a1, 01a02b4b, 01a02fe5, 019ffafe (depth 2, through the acquisition
  subflows' transcript reads).

## Appendix — the `Deploy.Host` payload as it is (2026-08-29)

Schema: `meta-signal-lojix/ethos/lib.ethos:7`
`HostDeployment.{ClusterName NodeName HostComposition ProposalSource FlakeReference DeploymentTransport DeploymentInputMode DeploymentOutputSelector ActivationBackend HostDeployAction SourceRevisionPolicy Option<NixBuilderSpec> Vector<ExtraSubstituter>}`;
`signal-lojix/ethos/lib.ethos:7`: `DeploymentTransport.{NixStoreUri SshDestination}`,
`DeploymentInputMode.[Horizon Direct]`, `DeploymentOutputSelector.{FlakeAttribute}`,
`ActivationBackend.[HomeManagerNixProfileV1 NixosSystemdBootV1]`,
`HostDeployAction.[TestActivation ScheduleBootOnce Realize SetBootProfile Evaluate ActivateNow]`,
`SourceRevisionPolicy.[ResolveAndRecord RequireImmutable]`, `HostComposition.[CompleteHost BaseHost]`,
`NixBuilderSpec.String`, `ProposalSource.String`, `FlakeReference.String`, `ExtraSubstituter.{String String}`.

Real invocation (Zeus, 2026-08-23, `flows/01a02b46/witnesses/zeusDeployment.md`):
`meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS?rev=d04f6daf… (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'`

Per deployment only node, flake rev, action, and sometimes transport and
builder vary; cluster, proposal source, composition, input mode, selector,
backend, source policy and substituters have been constant, and transport is a
fact Horizon already holds for the node. Variant names other than the transport,
backend, action and immutable-source ideas are agent-coined.

## Deploy request, redesigned without repetition (proposal, 2026-08-29)

Rule: a field exists in the request only if it is a choice made at that
moment; every fact already true somewhere is read from there, once.

| Field today | Read from, in the redesign |
|---|---|
| ClusterName, ProposalSource | the daemon's own configuration (OS-only daemon, one cluster) |
| HostComposition | `BaseHost` only sets `includeHome=false, includeAllFirmware=false` in the generated deployment flake (`lojix/src/bootstrap.rs:716-725`, `schema_runtime.rs:4917-4922`) — the first-install composition that `lojix-bootstrap` uses. It belongs to the bootstrap message, not to a deployment; dropped from Deploy.Host |
| FlakeReference + SourceRevisionPolicy | one optional `Revision`; absent = main resolved and recorded; the policy is the field's own form |
| DeploymentTransport | Horizon (node addresses, keys); the psyche's actual choice was a route — optional `Route` or a rule (question 2) |
| DeploymentInputMode | `Direct` only skips MaterializeHorizon and jumps to Building (`schema_runtime.rs:1598-1604, 3462-3479`); dropped, one mode |
| DeploymentOutputSelector | CriomOS's contract, known to the daemon |
| ActivationBackend | already said by the message variant (Host vs UserEnvironment) |
| HostDeployAction | kept; the variant set is the psyche's to name (question 1) |
| NixBuilderSpec, ExtraSubstituter | Horizon (builder_configs, cache_urls per node) |
| NodeName | kept |

```
Deploy.Host.{ NodeName  Action  Option<Revision>  Option<Route> }
Deploy.UserEnvironment.{ NodeName  UserName  Action  Option<Revision> }
```

The daemon configuration archive (today: two socket paths) gains cluster
name, proposal path and CriomOS flake source. The deployment record keeps the
fully resolved request (rev, route, builder, caches) so the query surface is
unchanged. A per-node durable file would hold only the node name; that half
of question 3 dissolves.

Open for the psyche: (1) the real set and names of actions; (2) route as a
per-deployment choice or a Lojix rule (LAN when reachable).
