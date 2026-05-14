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
| `persona-mind` | `/git/github.com/LiGoldragon/persona-mind` | Central Persona state component; replaces lock-file orchestration over time. |
| `persona-router` | `/git/github.com/LiGoldragon/persona-router` | Message routing and delivery coordination. Binds one socket: `router.sock` (0600, internal traffic only). External engine-owner ingress arrives via `persona-message-daemon`. |
| `persona-message` | `/git/github.com/LiGoldragon/persona-message` | Engine message ingress: the `message` CLI **and** the `persona-message-daemon` supervised first-stack daemon. Daemon binds `message.sock` (mode 0660, engine-owner group) and forwards typed Signal frames to `persona-router` with SO_PEERCRED-minted origin tags. |
| `persona-introspect` | `/git/github.com/LiGoldragon/persona-introspect` | Supervised prototype inspection-plane component. Talks to live component daemons over Signal, fans in typed observation records, and projects NOTA only at the human/agent edge. It is not in the delivery path and does not directly open any peer component's redb. |
| `signal-persona-introspect` | `/git/github.com/LiGoldragon/signal-persona-introspect` | Central introspection envelope contract: introspection query/reply selectors, correlation, projection wrappers, and prototype witness records. It asks and wraps; component-specific observations stay in the owning component contracts. |
| `persona-system` | `/git/github.com/LiGoldragon/persona-system` | Deferred system observation component for OS/window facts such as focus. Prompt-state checking is terminal-owned in the current wave. |
| `persona-harness` | `/git/github.com/LiGoldragon/persona-harness` | Harness process/session control boundary. |
| `persona-terminal` | `/git/github.com/LiGoldragon/persona-terminal` | Persona-facing terminal owner: named terminal sessions, Signal adapter, viewer-adapter policy, and component Sema metadata around `terminal-cell`. Terminal-brand mux helpers are retired. |
| `terminal-cell` | `/git/github.com/LiGoldragon/terminal-cell` | Low-level daemon-owned PTY/transcript cell primitive consumed by `persona-terminal`. |
| `sema` | `/git/github.com/LiGoldragon/sema` | **Today's** typed storage kernel (redb + rkyv + schema guard). Not a daemon, not shared storage, and not the full database engine. Distinct from the **eventual** `Sema` — the universal medium for meaning (self-hosting computational substrate, fully-typed human-language representation, universal interlingua). Per `ESSENCE.md` §"Today and eventually". |
| `sema-engine` | `/git/github.com/LiGoldragon/sema-engine` | Full database engine library over `sema` and `signal-core`: registered record families, Signal-verb execution, operation log/snapshot identity/subscription surface as it lands. Not a daemon, not Kameo, not NOTA, and not Persona-specific. First real consumer is `persona-mind`; Criome follows. |
| `signal-core` | `/git/github.com/LiGoldragon/signal-core` | Signal wire kernel: typed frames, envelopes, channel macro. |
| `signal` | `/git/github.com/LiGoldragon/signal` | Sema-ecosystem record vocabulary atop `signal-core`. |
| `signal-persona` | `/git/github.com/LiGoldragon/signal-persona` | Persona-wide Signal vocabulary. |
| `signal-persona-auth` | `/git/github.com/LiGoldragon/signal-persona-auth` | Persona origin-context vocabulary: engine/route/channel ids, component names, connection classes, message origins, and ingress context. Not an authentication library. |
| `signal-persona-message` | `/git/github.com/LiGoldragon/signal-persona-message` | Message CLI to router channel contract. |
| `signal-persona-router` | `/git/github.com/LiGoldragon/signal-persona-router` | Router-owned observation contract for accepted messages, route decisions, channel state, delivery status, and adjudication status. Used by `persona-introspect` without turning `signal-persona-introspect` into a shared schema bucket. |
| `signal-persona-system` | `/git/github.com/LiGoldragon/signal-persona-system` | System observation to router channel contract. |
| `signal-persona-harness` | `/git/github.com/LiGoldragon/signal-persona-harness` | Router to harness delivery/observation channel contract. |
| `signal-persona-terminal` | `/git/github.com/LiGoldragon/signal-persona-terminal` | Terminal transport control contract: prompt patterns, input gates, write injection acknowledgements, and terminal-worker lifecycle records. |
| `signal-persona-mind` | `/git/github.com/LiGoldragon/signal-persona-mind` | Mind/orchestration contract vocabulary. |
| `signal-criome` | `/git/github.com/LiGoldragon/signal-criome` | Criome trust and attestation contract vocabulary: BLS signature envelopes, identity records, delegation grants, component releases, and out-of-band attestations. Pure contract crate; no daemon, no storage, no Persona policy ownership. |
| `nexus` | `/git/github.com/LiGoldragon/nexus` | Typed semantic text vocabulary written in NOTA syntax. |
| `nexus-cli` | `/git/github.com/LiGoldragon/nexus-cli` | CLI surface for Nexus-shaped NOTA records. |
| `nota` | `/git/github.com/LiGoldragon/nota` | NOTA language home. |
| `nota-codec` | `/git/github.com/LiGoldragon/nota-codec` | NOTA parser/encoder/decoder; no Nexus semantics. |
| `nota-derive` | `/git/github.com/LiGoldragon/nota-derive` | NOTA derive support. |

## Retired / Cleanup Targets

These repos may still exist in checkouts or flake history, but they are not
current architecture targets.

| Repository | Path | Status |
|---|---|---|
| `persona-sema` | `/git/github.com/LiGoldragon/persona-sema` | Retired abstraction. Sema layers are component-owned: mind Sema lives in `persona-mind`, router Sema lives in `persona-router`, etc. |

## Adjacent Active Work

These repos have recent commits or platform relevance, but they are not
the main Persona architecture reset unless the user names them.

| Repository | Path | Why adjacent |
|---|---|---|
| `criome` | `/git/github.com/LiGoldragon/criome` | Current target is a minimal Spartan BLS12-381 authentication and attestation daemon. It verifies signatures, maintains identity/revocation state, signs attestations, and reports verification facts. Persona decides policy. Distinct from the **eventual** `Criome` — the universal computing paradigm in Sema (replaces Git, editor, SSH, web; encompasses broader auth/security via quorum-signature multi-sig). Per `ESSENCE.md` §"Today and eventually". |
| `chroma` | `/git/github.com/LiGoldragon/chroma` | Active system-specialist visual/scheduler work. |
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
| `signal-lojix` | `github:LiGoldragon/signal-lojix` | wire surface implicit in `lojix-cli` (none today) | Skeleton + ARCHITECTURE.md. Implementation lands on the `horizon-re-engineering` feature branch alongside `lojix` daemon work. |
| `lojix` | `github:LiGoldragon/lojix` | implementation surface of `lojix-cli` (legacy stays at current schema; retires after CriomOS migrates) | Renamed from `lojix-daemon` (2026-05-14). One crate, two binaries: `lojix-daemon` (long-lived orchestrator) + `lojix` (thin CLI client) per `~/primary/AGENTS.md` §"Binary naming". Implementation lands on the `horizon-re-engineering` feature branch. Storage via `sema-engine`; wire via `signal-core` carrying `signal-lojix` records. |

**Cutover discipline.** Each replacement repo has a documented
"replaces" target above. The cutover for that target is staged: build
the replacement to feature parity, run both in parallel, switch
producers/consumers one at a time, then retire the original (move it to
"Retired / Cleanup Targets"). Do not begin retiring the old until the
replacement covers every consumer of the surface being replaced.

**Active feature arc — horizon re-engineering** (started 2026-05-14, bead
`primary-vhb6`). Spans `horizon-rs`, `lojix`, `signal-lojix`, `CriomOS`,
`CriomOS-home`, `goldragon`. All on the `horizon-re-engineering` branch
in worktrees per `~/primary/skills/feature-development.md`. `lojix-cli`
is untouched by the arc — stays at the current schema and retires after
CriomOS migrates to the new daemon's projection.

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
  shared sema daemon, no generic store component, and no shared
  `persona-sema` architecture. The eventual `Sema` (universal medium
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
  contracts live in dedicated `signal-*` repos.
- Text: NOTA is the only text syntax. Nexus is typed semantic content
  written in NOTA syntax, not a second parser or alternate text
  format.
- Persona center: `persona-mind` is the central state component for
  orchestration/work graph evolution. Lock files and BEADS are
  transitional compatibility surfaces.
