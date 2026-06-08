# Active Repositories

This file is the current attention map. It is deliberately smaller
than `RECENT-REPOSITORIES.md`.

`RECENT-REPOSITORIES.md` is a checkout index. This file answers a
different question: which repositories are active enough that agents
should read their current `ARCHITECTURE.md`, `AGENTS.md`, and
`skills.md` before reshaping the Persona stack.

Update this file when the work focus changes. Do not use it as a
historical archive.

## Current Core Stack

These repos are the active Persona / Sema / Signal / Nexus / NOTA
stack.

| Repository | Path | Current role |
|---|---|---|
| `primary` | `/home/li/primary` | Workspace coordination, skills, protocols, reports. |
| `lore` | `/git/github.com/LiGoldragon/lore` | Cross-workspace agent discipline and language/coding lore. |
| `persona` | `/git/github.com/LiGoldragon/persona` | Persona meta-repo; wires the stack through Nix and apex architecture. |
| `mind` | `/git/github.com/LiGoldragon/mind` | Central Persona state component; replaces lock-file orchestration over time. |
| `router` | `/git/github.com/LiGoldragon/router` | Message routing and delivery coordination. Binds one socket: `router.sock` (0600, internal traffic only). External engine-owner ingress arrives via `message-daemon`. |
| `message` | `/git/github.com/LiGoldragon/message` | Engine message ingress: the `message` CLI **and** the `message-daemon` supervised first-stack daemon. Daemon binds `message.sock` (mode 0660, engine-owner group) and forwards typed Signal frames to `router` with SO_PEERCRED-minted origin tags. |
| `introspect` | `/git/github.com/LiGoldragon/introspect` | Supervised prototype inspection-plane component. Talks to live component daemons over Signal, fans in typed observation records, and projects NOTA only at the human/agent edge. It is not in the delivery path and does not directly open any peer component's redb. |
| `signal-introspect` | `/git/github.com/LiGoldragon/signal-introspect` | Central introspection envelope contract: introspection query/reply selectors, correlation, projection wrappers, and prototype witness records. It asks and wraps; component-specific observations stay in the owning component contracts. |
| `system` | `/git/github.com/LiGoldragon/system` | Deferred system observation component for OS/window facts such as focus. Prompt-state checking is terminal-owned in the current wave. |
| `harness` | `/git/github.com/LiGoldragon/harness` | Harness process/session control boundary. |
| `terminal` | `/git/github.com/LiGoldragon/terminal` | Persona-facing terminal owner: named terminal sessions, Signal adapter, viewer-adapter policy, and component Sema metadata around `terminal-cell`. Terminal-brand mux helpers are retired. |
| `terminal-cell` | `/git/github.com/LiGoldragon/terminal-cell` | Low-level daemon-owned PTY/transcript cell primitive consumed by `terminal`. |
| `sema` | `/git/github.com/LiGoldragon/sema` | **Today's** typed storage kernel (redb + rkyv + schema guard). Not a daemon, not shared storage, and not the full database engine. Distinct from the **eventual** `Sema` — the universal medium for meaning (self-hosting computational substrate, fully-typed human-language representation, universal interlingua). Per `ESSENCE.md` §"Today and eventually". |
| `signal-sema` | `/git/github.com/LiGoldragon/signal-sema` | Sema operation vocabulary: `Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`, and `Validate`. Public component contracts lower into this layer; they do not expose these words as universal request roots. |
| `sema-engine` | `/git/github.com/LiGoldragon/sema-engine` | Full database engine library over `sema`, `signal-sema`, and a small transitional `signal-core` utility seam: registered record families, Sema operation execution, operation log/snapshot identity/subscription surface as it lands. Not a daemon, not Kameo, not NOTA, and not Persona-specific. First real consumer is `mind`; Criome follows. |
| `schema` | `/git/github.com/LiGoldragon/schema` | Typed schema-language substrate: resolved schema document model, validation, and root-versus-box layout metadata for schema-driven signal/sema macro work. Library-shaped now; future runtime schema triad authority remains unsettled. |
| `schema-next` | `/git/github.com/LiGoldragon/schema-next` | Replacement schema engine for the schema-derived stack. Schema is a specialized NOTA dialect (a `.schema` file IS full NOTA), not a separate language. Authored `.schema` deserializes via the structural-macro-node codec into schema-in-Rust — the typed, rkyv-serializable canonical round-trip image. There is NO separate assemble/`Asschema` step (Asschema removed per record `vez8`); the resolution it once did (inline-declaration hoisting, visibility, ordering, symbol paths) now lives as methods on the schema-in-Rust source types. Operator-owned `main`; designers branch from that baseline in `~/wt`. |
| `schema-rust-next` | `/git/github.com/LiGoldragon/schema-rust-next` | Replacement Rust emission layer. LOWERS schema-in-Rust into Rust interface code using Rust's real macro infrastructure — `quote!` / `proc-macro2` `TokenStream` / `ToTokens` — NOT a hand-rolled string code generator (records `4np2`, `e6v5`). Each schema type/subobject renders itself as tokens via `LowerToRust`; the old 52-method `RustWriter` string emitter is mid-migration out and the remaining `format!`/string surface is transitional. Whether tokens land in checked-in `src/schema/*.rs` (build-time `quote!` + `prettyplease`) or expand inline is a separate visibility choice; generation is token-based either way. Operator-owned `main`. |
| `triad-runtime` | `/git/github.com/LiGoldragon/triad-runtime` | Shared runtime support for schema-derived Signal/Nexus/SEMA daemons. Current live surface is generic trace logging, rkyv frame transport, and Unix trace socket listening; component crates keep generated nouns and actor hooks. |
| `persona-spirit` | `/git/github.com/LiGoldragon/persona-spirit` | Production Spirit source until schema-derived cutover. Provides the deployed `spirit` / `spirit-v0.3.0` CLI and `persona-spirit-daemon`, including the current profile's side-by-side `spirit-next` deployment slot. |
| `spirit` | `/git/github.com/LiGoldragon/spirit` | Public runnable pilot for the schema-derived stack. `schema/spirit.schema` is lowered by `schema-next`, emitted by `schema-rust-next`, then used by a real NOTA CLI and rkyv Unix-socket daemon boundary. This is the active implementation formerly carried under the temporary `spirit-next` repository name; the stale concept-track `spirit` repository is retired. |
| `signal-spirit` | `/git/github.com/LiGoldragon/signal-spirit` | Active ordinary Spirit wire contract, renamed from `signal-persona-spirit`. Default builds are binary/rkyv-only; `nota-text` enables CLI/debug/audit projection. |
| `meta-signal-spirit` | `/git/github.com/LiGoldragon/meta-signal-spirit` | Active Spirit meta policy wire contract, renamed from `owner-signal-persona-spirit`. It carries privileged lifecycle/configuration operations; the default graph is binary/rkyv-only and `nota-text` is an explicit edge projection feature. |
| `version-projection` | `/git/github.com/LiGoldragon/version-projection` | Shared projection and compatibility-policy library for adjacent component versions. Pure library; no daemon, no socket, no component-specific migration logic. |
| `signal-version-handover` | `/git/github.com/LiGoldragon/signal-version-handover` | Private daemon-to-daemon signal contract for version handover marker, readiness, completion, mirror, divergence, and recovery messages. |
| `owner-signal-version-handover` | `/git/github.com/LiGoldragon/owner-signal-version-handover` | Owner-only administrative signal contract for version handover authority: force selector flip, rollback, and quarantine. |
| `upgrade` | `/git/github.com/LiGoldragon/upgrade` | Upgrade triad runtime scaffold. Target home for schema/version migration orchestration, handover driver code, and the thin `upgrade` CLI plus `upgrade-daemon`. |
| `signal-upgrade` | `/git/github.com/LiGoldragon/signal-upgrade` | Ordinary upgrade contract scaffold. Target merger home for sema-upgrade inspection/planning/migration and version-handover working traffic. |
| `meta-signal-upgrade` | `/git/github.com/LiGoldragon/meta-signal-upgrade` | Owner-only upgrade meta-signal contract scaffold. Target merger home for upgrade administration, selector control, rollback, and quarantine. |
| `signal-core` | `/git/github.com/LiGoldragon/signal-core` | Signal wire kernel: typed frames, envelopes, channel macro. It is being redirected away from universal request verbs; public contracts own contract-local operation roots. |
| `signal` | `/git/github.com/LiGoldragon/signal` | Sema-ecosystem record vocabulary atop `signal-core`. |
| `owner-signal-persona` | `/git/github.com/LiGoldragon/owner-signal-persona` | Owner-only Persona engine-manager contract: launch, retire, start, stop, and status query. |
| `signal-engine-management` | `/git/github.com/LiGoldragon/signal-engine-management` | Ordinary Persona manager-to-supervised-component lifecycle contract: announce, readiness, health, stop, and spawn envelope. |
| `signal-persona` | `/git/github.com/LiGoldragon/signal-persona` | Retired compatibility shim for the former combined Persona signal surface; new code depends on `owner-signal-persona` or `signal-engine-management` directly. |
| `signal-persona-origin` | `/git/github.com/LiGoldragon/signal-persona-origin` | Persona origin-context vocabulary: engine/route/channel ids, component names, connection classes, message origins, and ingress context. Not an authentication library. |
| `signal-agent` | `/git/github.com/LiGoldragon/signal-agent` | Ordinary agent front-door signal contract for pre-configured API agent calls. |
| `owner-signal-agent` | `/git/github.com/LiGoldragon/owner-signal-agent` | Owner-only agent policy signal contract for backend/provider configuration and lifecycle control. |
| `signal-message` | `/git/github.com/LiGoldragon/signal-message` | Message CLI to router channel contract. |
| `signal-router` | `/git/github.com/LiGoldragon/signal-router` | Router-owned observation contract for accepted messages, route decisions, channel state, delivery status, and adjudication status. Used by `introspect` without turning `signal-introspect` into a shared schema bucket. |
| `meta-signal-router` | `/git/github.com/LiGoldragon/meta-signal-router` | Meta-signal router policy contract. |
| `signal-system` | `/git/github.com/LiGoldragon/signal-system` | System observation to router channel contract. |
| `signal-harness` | `/git/github.com/LiGoldragon/signal-harness` | Router to harness delivery/observation channel contract. |
| `signal-terminal` | `/git/github.com/LiGoldragon/signal-terminal` | Terminal transport control contract: prompt patterns, input gates, write injection acknowledgements, and terminal-worker lifecycle records. |
| `owner-signal-terminal` | `/git/github.com/LiGoldragon/owner-signal-terminal` | Owner-only terminal session lifecycle mutation contract for `CreateSession` and `RetireSession`; ordinary terminal traffic stays in `signal-terminal`. |
| `signal-mind` | `/git/github.com/LiGoldragon/signal-mind` | Mind/orchestration contract vocabulary. |
| `owner-signal-mind` | `/git/github.com/LiGoldragon/owner-signal-mind` | Owner-only mind policy contract. |
| `orchestrate` | `/git/github.com/LiGoldragon/orchestrate` | Orchestration component runtime. |
| `signal-orchestrate` | `/git/github.com/LiGoldragon/signal-orchestrate` | Ordinary orchestration contract vocabulary. |
| `meta-signal-orchestrate` | `/git/github.com/LiGoldragon/meta-signal-orchestrate` | Meta-signal orchestration policy contract. |
| `signal-criome` | `/git/github.com/LiGoldragon/signal-criome` | Criome trust and attestation contract vocabulary: BLS signature envelopes, identity records, delegation grants, component releases, and out-of-band attestations. Pure contract crate; no daemon, no storage, no Persona policy ownership. |
| `repository-ledger` | `/git/github.com/LiGoldragon/repository-ledger` | Triad runtime component for recording pushed repository changes from the local Gitolite server into a sema-engine database. |
| `signal-repository-ledger` | `/git/github.com/LiGoldragon/signal-repository-ledger` | Ordinary repository-ledger contract: receive-hook event assertions and repository/event read queries. |
| `meta-signal-repository-ledger` | `/git/github.com/LiGoldragon/meta-signal-repository-ledger` | Meta-signal repository-ledger contract: repository registration, spool policy, and future mirror policy mutation. |
| `nexus` | `/git/github.com/LiGoldragon/nexus` | Typed semantic text vocabulary written in NOTA syntax. |
| `nexus-cli` | `/git/github.com/LiGoldragon/nexus-cli` | CLI surface for Nexus-shaped NOTA records. |
| `nota` | `/git/github.com/LiGoldragon/nota` | NOTA language home. |
| `nota-next` | `/git/github.com/LiGoldragon/nota-next` | Replacement NOTA implementation for the schema-derived stack. Owns raw structural block parsing, source spans, `qualifies_as_*` methods, and the **structural macro node** codec — `#[derive(StructuralMacroNode)]`, a NOTA enum decoded by SHAPE (type-directed, structural match per variant in declaration order, first match wins, recursive) with bidirectional encode back to a matching NOTA block (records `xai7`, `z544`). Schema semantics still live in `schema-next`. Operator-owned `main`. |
| `nota-codec` | `/git/github.com/LiGoldragon/nota-codec` | NOTA parser/encoder/decoder; no Nexus semantics. |
| `nota-derive` | `/git/github.com/LiGoldragon/nota-derive` | NOTA derive support. |
| `nota-config` | `/git/github.com/LiGoldragon/nota-config` | Strict one-argument typed configuration input over NOTA, `.nota`, or `.rkyv`. |

## Adjacent Active Work

These repos have recent commits or platform relevance, but they are not
the main Persona architecture reset unless the user names them.

| Repository | Path | Why adjacent |
|---|---|---|
| `criome` | `/git/github.com/LiGoldragon/criome` | Current target is a minimal Spartan BLS12-381 authentication and attestation daemon. It verifies signatures, maintains identity/revocation state, signs attestations, and reports verification facts. Persona decides policy. Distinct from the **eventual** `Criome` — the universal computing paradigm in Sema (replaces Git, editor, SSH, web; encompasses broader auth/security via quorum-signature multi-sig). Per `ESSENCE.md` §"Today and eventually". |
| `cloud` | `/git/github.com/LiGoldragon/cloud` | New runtime repo for provider API management. Documentation-only at birth; real daemon work is tracked by bead `primary-kbmi` (cloud/domain-criome runtime daemons). |
| `signal-cloud` | `/git/github.com/LiGoldragon/signal-cloud` | Ordinary `cloud` contract: provider/capability observation, desired-state validation, and plan preparation. |
| `meta-signal-cloud` | `/git/github.com/LiGoldragon/meta-signal-cloud` | Meta policy `cloud` contract: credential handles, provider account policy, plan approval, and plan application. |
| `domain-criome` | `/git/github.com/LiGoldragon/domain-criome` | New runtime repo for Criome-domain registry, intelligent resolution, and provider-neutral projection. Documentation-only at birth; real daemon work is tracked by bead `primary-kbmi`. |
| `signal-domain-criome` | `/git/github.com/LiGoldragon/signal-domain-criome` | Ordinary `domain-criome` contract: domain observation, intelligent resolution, and provider-neutral projection. |
| `meta-signal-domain-criome` | `/git/github.com/LiGoldragon/meta-signal-domain-criome` | Meta policy `domain-criome` contract: domain registration, delegation, retirement, and projection policy. |
| `chroma` | `/git/github.com/LiGoldragon/chroma` | Active system-operator visual/scheduler work. |
| `CriomOS` | `/git/github.com/LiGoldragon/CriomOS` | Operating-system layer for the broader project. |
| `CriomOS-home` | `/git/github.com/LiGoldragon/CriomOS-home` | User/home-manager surface for the OS layer. |
| `mentci-lib` | `/git/github.com/LiGoldragon/mentci-lib` | Future shell-state consumer of Sema patterns. |
| `horizon-rs` | `/git/github.com/LiGoldragon/horizon-rs` | Active Rust codebase with NOTA/Rust discipline overlap. |
| `lojix-cli` | `/git/github.com/LiGoldragon/lojix-cli` | Active CLI/Nix discipline reference. |
| `goldragon` | `/git/github.com/LiGoldragon/goldragon` | Active workspace-adjacent tooling. |
| `chronos` | `/git/github.com/LiGoldragon/chronos` | Active enough to keep visible, not Persona-core. |
| `TheBookOfSol` | `/git/github.com/LiGoldragon/TheBookOfSol` | Poet/prose surface, not Persona-core. |

## Replacement Stack

These repos replace parts of the current stack. Built in parallel
with the existing surface; the current stack keeps working until
cutover.

| Repository | Path | Replaces | Status |
|---|---|---|---|
| `signal-lojix` | `github:LiGoldragon/signal-lojix` | wire surface implicit in `lojix-cli` (none today) | Skeleton + ARCHITECTURE.md. Implementation lands on the `horizon-leaner-shape` feature branch alongside `lojix` daemon work. |
| `lojix` | `github:LiGoldragon/lojix` | implementation surface of `lojix-cli` (legacy stays at current schema; retires after CriomOS migrates) | Renamed from `lojix-daemon` (2026-05-14). One crate, two binaries: `lojix-daemon` (long-lived orchestrator) + `lojix` (thin CLI client) per `~/primary/AGENTS.md` §"Binary naming". Implementation lands on the `horizon-leaner-shape` feature branch. Storage via `sema-engine`; wire via `signal-core` carrying `signal-lojix` records. |
| `criomos-horizon-config` | `github:LiGoldragon/criomos-horizon-config` | pan-horizon constants previously inlined in `goldragon/datom.nota` (operator/suffixes/LAN pool/reserved labels) | Pan-horizon constants repo introduced on `horizon-leaner-shape`. Consumed by `horizon-rs` to derive cluster domains, router SSID, LAN CIDR/DHCP pool, resolver listen addresses, and tailnet base from cluster facts. |

**Cutover discipline.** Each replacement repo has a documented
"replaces" target above. The cutover for that target is staged: build
the replacement to feature parity, run both in parallel, switch
producers/consumers one at a time, then retire the original (move it to
"Retired / Cleanup Targets"). Do not begin retiring the old until the
replacement covers every consumer of the surface being replaced.

**Active feature arc — horizon-leaner-shape** (sibling branch off the
earlier `horizon-re-engineering` work; supersedes it as of 2026-05-17).
Spans `horizon-rs`, `lojix`, `signal-lojix`, `CriomOS`, `CriomOS-home`,
`CriomOS-lib`, `goldragon`, and the new `criomos-horizon-config` repo.
All on the `horizon-leaner-shape` branch in worktrees per
`~/primary/skills/feature-development.md`. `lojix-cli` is untouched by
the arc — stays at the current schema and retires after CriomOS migrates
to the new daemon's projection. Smoke-built `zeus` end-to-end through
`prometheus` (see `reports/system-operator/134`); has **not** been cut
over to any node.

`horizon-re-engineering` worktrees still exist for several repos but are
**superseded**. Do not pick up that branch; new work belongs on
`horizon-leaner-shape`.

### Two deploy stacks coexist — production and the lean rewrite

Until cutover lands, agents must distinguish two parallel deploy stacks.

**Stack A — production today** (running on every node). `main` branches
in the canonical `/git/github.com/LiGoldragon/...` checkouts of:
`horizon-rs`, `lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`,
`goldragon`. Old monolithic `lojix-cli` projects `horizon-rs/main` over
`goldragon/datom.nota` and writes the `horizon` / `system` /
`deployment` flake inputs into CriomOS at deploy time. No daemon, no
`lojix` repo, no `criomos-horizon-config`. CriomOS and CriomOS-home
flake locks pin `lojix-cli` at `4c66b8a6fa55`. **Production fixes go
here.**

**Stack B — lean rewrite, smoke-built, not yet deployed**.
`horizon-leaner-shape` branches in worktrees under
`~/wt/github.com/LiGoldragon/<repo>/horizon-leaner-shape/`, spanning the
same six repos plus two new ones: `lojix` (daemon + thin CLI client) and
`criomos-horizon-config` (pan-horizon constants). Lean horizon
proposal/view, pan-horizon config split into its own repo, new lojix
daemon-and-thin-client shape. **Rewrite edits go here.**

**Do not fold one stack into the other piecemeal.** Schemas have
diverged. Cutover happens as a coordinated multi-repo merge after the
rewrite reaches feature parity, per §"Cutover discipline" above. Until
then: production edits → `main` in the canonical checkout; rewrite edits
→ `horizon-leaner-shape` in the worktree.

Note: GitHub redirects `LiGoldragon/lojix` → `LiGoldragon/forge` are
stale (forge was previously named lojix and got renamed). The new
`lojix` repo at `github.com/LiGoldragon/lojix` is the deploy stack;
`forge` is unrelated (criome-stack executor; future replacement for
nix's build infrastructure).

## Current Truth Pins

- Actor runtime: direct `kameo` today. Actor density is required:
  runtime roots are actors, public actor nouns carry data, and
  topology/trace tests prove real mailbox paths. Direct `ractor`,
  `persona-actor`, and `workspace-actor` language is stale unless a
  current report explicitly reopens that decision.
- State: today's `sema` is the typed storage kernel; `sema-engine` is
  the full database engine library. Each component that needs durable
  state owns its own redb and its own engine/kernel handle. There is no
  shared sema daemon, no generic store component, and no Persona-wide
  storage architecture. The eventual `Sema` (universal medium
  for meaning — self-hosting computational substrate, fully-typed
  human-language representation, universal interlingua) is the
  long-term target, not a current implementation.
- Scope discipline: when a concept has both a today's form and an
  eventual encompassing form, the docs explicitly mark that boundary
  (`sema` storage kernel / `sema-engine` today vs eventual `Sema`;
  `criome` daemon today vs `Criome`). ARCH docs describe
  what's built today; eventual scope gets an explicit marker. Per
  ESSENCE §"Today and eventually — different things, different
  names". This is a scope discipline, not a quality one — "today's
  piece" is never a license to cut corners.
- Wire: Signal is the typed binary communication fabric. Component
  contracts live in dedicated `signal-*` repos and expose
  contract-local operation roots. The six database words
  (`Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`, `Validate`)
  belong to `signal-sema` / `sema-engine` execution, not to the
  public contract spine.
- Text: NOTA is the only text syntax. Nexus is typed semantic content
  written in NOTA syntax, not a second parser or alternate text
  format.
- Persona center: `mind` is the central state component for
  orchestration/work graph evolution. Lock files and BEADS are
  transitional compatibility surfaces.
