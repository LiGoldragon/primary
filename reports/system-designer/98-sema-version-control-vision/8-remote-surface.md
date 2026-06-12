# 98/8 — The server side — hosts, deploy surface, repository-ledger exemplar, mirror shape

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
This chapter reads reports/logs rather than code and was not adversarially verified.*

# Remote Mirror Server Architecture: Same Component or Specialized?

## Context: The Versioned-State Vision

The workspace is designing server-backed version control for component Sema databases, with a pilot on Spirit. The psyche's core requirement: protect component state against laptop data loss via append-only remote backup. Report 97 (system-designer) defines a staged implementation; report 214 (system-operator) sets non-negotiable constraints.

## 1. Current Host Topology — What is Reachable

**ouranos** is the designated remote host, established across multiple reports:

- **Primary purpose**: Gitolite server + tailnet node, running CriomOS ([system-maintainer/4](file:///home/li/primary/reports/system-maintainer/4-ouranos-disk-cleanup-inventory-2026-06-11.md:1-10))
- **Network**: tailnet-trusted (Tailscale VPN), single-psyche trusted boundary
- **Availability**: Always-on system-operator infrastructure (implicit from hosting Gitolite)
- **Current state**: Operational, with recent disk management completed ([system-maintainer/4](file:///home/li/primary/reports/system-maintainer/4-ouranos-disk-cleanup-inventory-2026-06-11.md:1-50))

**zeus** (Bird's host) is the second active node:

- Reachable via root SSH, but not via direct user SSH (Bird cannot SSH to Zeus directly) ([system-maintainer/2](file:///home/li/primary/reports/system-maintainer/2-Handover-bird-zeus-home-profile-redeploy.md:16))
- CriomOS deployment confirmed with Home Manager profiles ([CriomOS-home/modules/home/profiles/min/spirit.nix](file:///git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:1-30))

**Transport layer is Unix-socket-only today**: `triad-runtime` provides `AsyncSingleListenerDaemon` and `AsyncMultiListenerDaemon` for binding Unix listeners ([triad-runtime/ARCHITECTURE.md](file:///git/github.com/LiGoldragon/triad-runtime/ARCHITECTURE.md:52-82)). No TCP/network socket infrastructure exists in the current component daemon scaffold.

## 2. Deploy Surface: How Daemons Ship Today

Spirit-daemon deploys via **systemd user service**, integrated through Nix Home Manager:

- **Module**: `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix` ([lines 154-207](file:///git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:154-207))
- **Service definition**: `spirit-daemon` unit takes typed rkyv configuration (`spirit.config.rkyv`) as single argument
- **State directory**: `~/.local/state/spirit/` with Unix socket at `spirit.sock` ([lines 31-34](file:///git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:31-34))
- **Startup**: Single-argument binary consuming rkyv-encoded configuration ([ComponentCommand pattern](file:///git/github.com/LiGoldragon/triad-runtime/ARCHITECTURE.md:84-100))

**Deploying another daemon to ouranos would require**:
- New systemd service definition on ouranos
- New CriomOS or CriomOS-home module (or direct system.nix module)
- Nix package pin for the daemon binary
- Separate configuration generation and rkyv encoding

The burden is identical whether the daemon is the same component binary in a mirror role or a dedicated new component.

## 3. Repository-Ledger: The Exemplar for Remote Append-Ingest

Repository-ledger proves the triad pattern for server-side append machinery:

- **Intent**: Records pushed repository changes from local Gitolite into a sema-engine database ([repository-ledger/INTENT.md](file:///git/github.com/LiGoldragon/repository-ledger/INTENT.md:7-13))
- **Shape**: Full triad (daemon + signal-repository-ledger + meta-signal-repository-ledger) ([component-triad.md](file:///home/li/primary/skills/component-triad.md:65-86))
- **Daemon responsibilities**: 
  - Ordinary socket listener for queries ([Query variants](file:///git/github.com/LiGoldragon/repository-ledger/ARCHITECTURE.md:156-175))
  - Meta socket listener for policy (registration, spool, **mirror policy mutation**) ([INTENT.md line 42](file:///git/github.com/LiGoldragon/repository-ledger/INTENT.md:42))
  - sema-engine database for typed storage
  - Store and spool actor concerns, separate from socket listeners ([ARCHITECTURE.md lines 46-66](file:///git/github.com/LiGoldragon/repository-ledger/ARCHITECTURE.md:46-66))

**Load-bearing finding**: Repository-ledger's meta-signal explicitly includes **"mirror policy state"** ([INTENT.md line 42](file:///git/github.com/LiGoldragon/repository-ledger/INTENT.md:42)) — the infrastructure already contemplates the mirror as a policy concern of the owning component, not as a separate system.

## 4. Signal-Version-Handover: Mirror Already in the Wire Contracts

The daemon-to-daemon upgrade handover contract **already includes mirror messages**:

- **Operations** include `Mirror` (next forwards a write back to current) and `Divergence` (next records an entry reverse-projection cannot represent) ([signal-version-handover/INTENT.md](file:///git/github.com/LiGoldragon/signal-version-handover/INTENT.md:38-40))
- **Mirror discipline**: Raw unspecified payload + RecordKind discriminant sent to **separate container outside the receiver's typed database** ([lines 50-61](file:///git/github.com/LiGoldragon/signal-version-handover/INTENT.md:50-61))
- **Pattern precedent**: Version upgrade uses mirror for writes during handover; the container discipline is already proven

The mirror is treated as a durable log of untyped payloads, not as a full component instance.

## 5. The Versioned-State Mirror Design (Report 97)

Report 97 explicitly frames the remote as an **"append-ingest daemon"** on ouranos, not as a component instance:

- **Role**: Dumb append-only server, validates sequence continuity + expected-head digest, idempotent dedup, fsyncs, acks ([97 §5](file:///home/li/primary/reports/system-designer/97-versioned-state-implementation-handoff.md:165-195))
- **Capabilities**: No decryption, no signing, no guardian in this cut; tailnet-trusted ([97 lines 49-52, 192](file:///home/li/primary/reports/system-designer/97-versioned-state-implementation-handoff.md:49-52))
- **Storage**: Per-store append-only files (repository-ledger atomic-spool pattern precedent) ([97 line 188](file:///home/li/primary/reports/system-designer/97-versioned-state-implementation-handoff.md:188))
- **Durability**: Payload log suffix + previous-entry digest validation; no typed Sema state in the mirror ([97 lines 114-118](file:///home/li/primary/reports/system-designer/97-versioned-state-implementation-handoff.md:114-118))

**Explicitly NOT component replication**: The mirror is not asked to run guardian policy, not asked to rebuild views, not asked to project queries.

## 6. Operator Position on Mirror as Separate or Same Component

System-operator report 214 clarifies the four-layer target architecture:

1. Component daemon (owns semantic families and policy)
2. `sema-engine` (owns reusable versioning mechanism: log, DAG, frontiers, checkpoints, **mirror outbox**)
3. `sema` kernel (owns redb/rkyv bytes)
4. **Remote mirror/server** (owns append-only durable copy, expected-head checks, idempotent dedup, fsync ack, **retention policy**, signed-head storage) ([214 lines 189-201](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:189-201))

**Critical statement**: "The split matters. The engine should not become a network daemon. The server should not become a component guardian unless it is explicitly running as a semantic peer. The kernel should not learn branch semantics." ([214 lines 203-205](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:203-205))

**Remote retention is a policy axis**: "Never GC" is not a default; Spirit-class or private stores need explicit authority, privacy class, retention, pruning, deletion semantics ([214 lines 183-185](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:183-185)).

The **"server role must be explicit"** so "remote ingest" does not become accidental guardian bypass ([214 lines 177-179](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:177-179)).

## 7. Triad Pattern Favors Dedicated Mirror Component

The workspace pattern strongly favors creating a new **component triad** for the mirror:

### Evidence for dedicated `<mirror>` triad

1. **Policy authority boundary**: The mirror owns **retention policy, privacy policy, signed-head authority** — these are not Spirit's or Mind's concerns. Operators expect policy-owning state to live in a dedicated component ([component-triad.md lines 105-114](file:///home/li/primary/skills/component-triad.md:105-114) — security-sensitive visibility + policy authority boundaries are repo boundaries)

2. **Wire contract separation**: Repository-ledger shows the pattern: **meta-signal contract carries policy** ([repository-ledger/INTENT.md line 42](file:///git/github.com/LiGoldragon/repository-ledger/INTENT.md:42)). A dedicated mirror component would own `meta-signal-mirror` for:
   - Per-store retention policy
   - Privacy class mapping
   - Signed checkpoint authority thresholds
   - Per-component pruning/deletion overrides

3. **Role clarity**: Operators need to see at the **filesystem boundary** whether code is local component logic (Spirit's guardian, Mind's queries) or remote server policy (ouranos's durability, retention, attestation). Mixed code hides the split.

4. **Reusable across components**: Every component opts into versioning independently. The mirror server should be **one shared daemon on ouranos**, not replicated for each component. A dedicated `mirror` component with generalized per-store policy is cleaner than configuring each component daemon with "if you are spirit, run the mirror; if you are mind, also run the mirror."

5. **Schema-centric pattern**: The workspace principle is "center design around schema types" ([97 §4](file:///home/li/primary/reports/system-designer/97-versioned-state-implementation-handoff.md:131-156)). The mirror schema is different from Spirit's or Mind's — it owns `CheckpointMetadata`, `MirrorOutboxRow`, `PrivacyClass`, `RetentionPolicy`, signed proof structures. These should be schema-defined in the mirror's own `schema/sema.schema`, not grafted into Spirit's schema.

### Evidence against same-component-in-mirror-mode

1. **No precedent in current workspace**: Component scaffolds have no config-selected role switching. Spirit is not "Spirit in guardian mode" vs "Spirit in learner mode"; it is Spirit. Upgrade is upgrade, not "upgrade in migration mode."

2. **Entangles local and remote concerns**: Spirit's daemon would need to:
   - Open Unix socket for local CLI
   - Run guardian policy locally
   - AND open Unix socket for ouranos's append messages
   - AND manage retention policy for its own state on the remote
   - The guardian is for local admissions; the retention policy is for remote durability. They are separate policy axes.

3. **Violates the "server should not become a component guardian" rule** ([214 line 204](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:204)). If Spirit-daemon runs on both laptop and ouranos, confusion is baked in: which instance is the authoritative guardian?

4. **Deployment friction**: Both spirit-daemon and mirror-daemon would be packaged in the same binary, but deployed to different hosts with different configurations. Operators updating CriomOS-home would need to know "spirit.nix updates the CLI and local daemon, AND also must sync the mirror daemon config on ouranos." That is a deployment-time contract spanning two repos (spirit + CriomOS-home), making breakage likely.

## 8. Recommended Architecture: Dedicated Mirror Triad

**Create a new component triad: `<mirror>`, `signal-mirror`, `meta-signal-mirror`**

### Mirror daemon responsibilities

- **Storage**: Per-store append-only payload log (as designed in 97 §3)
- **Validation**: Expected-head digest check, idempotent dedup by entry-digest
- **Durability**: fsync before ack (no encryption in this cut; criome deferred)
- **Policy observation**: Query operations to observe retention status, privacy classes, recent appends
- **Meta authority**: `meta-signal-mirror` gates retention-policy overrides, privacy-class assignment, checkpoint signing thresholds, pruning/deletion directives

### Binaries

- `mirror` (CLI, thin Signal client, NOTA edge for debugging)
- `mirror-daemon` (ouranos long-lived process, bound to Unix socket)

### Wire contracts

- **`signal-mirror`**: Ordinary ingest (`AppendEntry` + validation reply), checkpoint polling, state observation queries
- **`meta-signal-mirror`**: Retention policy mutation, privacy class assignment, garbage-collection/pruning authority

### Per-store configuration

Each component (Spirit, Mind, etc.) configures its mirror behavior in its own `IntakePolicy`:
- Which privacy class (public / ordinary-private / existence-private)
- Which retention window (keep-all / pruning-window / ttl)
- Server-committed durability requirement (local-only / queued / server-committed)

The mirror daemon reads per-store retention policy as a durable `RetentionPolicy` record in its sema-engine database, not as ad-hoc config.

### Deployment

- Add mirror-daemon to CriomOS system-level modules (not CriomOS-home user-level)
- Package in flake.lock pin to `mirror` binary
- Single service definition on ouranos
- All components (spirit-daemon, mind-daemon, etc.) on all hosts connect to the single ouranos mirror-daemon

This design:
- Keeps the server "dumb but policy-aware" ([214 line 204](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:204))
- Makes retention/privacy policy **schema-visible and operator-transparent** (ownership is explicit in repos)
- Scales: one mirror daemon, many component daemons, per-store policies compose cleanly
- Aligns with triad-pattern discipline: filesystem boundaries = policy boundaries

## Grounding in Existing Patterns

The decision rests on three established patterns:

1. **Repository-ledger shows mirror as policy concern** ([INTENT.md line 42](file:///git/github.com/LiGoldragon/repository-ledger/INTENT.md:42)): Meta-signal already owns mirror policy mutation
2. **Triad pattern isolates policy authority** ([component-triad.md lines 105-114](file:///home/li/primary/skills/component-triad.md:105-114)): Policy-sensitive code belongs in dedicated repos
3. **Operator architecture explicitly separates concerns** ([214 lines 203-205](file:///home/li/primary/reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md:203-205)): Engine ≠ server, server ≠ guardian

The mirror is **not another instance of the same component**. It is a **specialized mirror component**, a peer daemon on the trusted remote, with its own schema, policy authority, and retention/privacy semantics.


## keyClaims
- CLAIM: ouranos is the designated remote host for the mirror, established as always-on Gitolite + tailnet infrastructure
  EVIDENCE: system-maintainer/4, system-designer/97 §5, system-operator/214 §1
- CLAIM: The current workspace has no cross-host network transport (TCP, Tailscale sockets); all daemon communication uses Unix sockets bound locally
  EVIDENCE: triad-runtime/ARCHITECTURE.md (AsyncSingleListenerDaemon, AsyncMultiListenerDaemon bind Tokio Unix listeners), no TCP infrastructure in /git/github.com/LiGoldragon/*
- CLAIM: Daemons deploy via systemd user/system services configured through Nix, taking exactly one rkyv-encoded configuration file as argument
  EVIDENCE: CriomOS-home/modules/home/profiles/min/spirit.nix lines 154–207, triad-runtime/ARCHITECTURE.md lines 84–100 (ComponentCommand pattern)
- CLAIM: Repository-ledger's meta-signal contract explicitly owns 'mirror policy state', establishing the pattern that mirrors are policy concerns of owning components
  EVIDENCE: repository-ledger/INTENT.md line 42: 'meta-signal registration, spool policy, and future mirror policy mutation'
- CLAIM: Report 97 frames the remote as a dumb 'append-ingest daemon', not a component instance, with no guardian, no decryption, no signing in this cut
  EVIDENCE: system-designer/97 §5 lines 49–52, 165–195: 'new minimal append-ingest daemon', 'tailnet-trusted, no per-suffix authentication'
- CLAIM: System-operator report 214 establishes a four-layer target architecture where the server's role is explicitly distinct from component logic, explicitly NOT a guardian unless running as a semantic peer
  EVIDENCE: system-operator/214 lines 189–205: 'The split matters. The engine should not become a network daemon. The server should not become a component guardian unless it is explicitly running as a semantic peer.'
- CLAIM: The triad pattern isolates policy authority at the repository boundary, so policy-owning state (retention, privacy, signed attestation) belongs in a separate component
  EVIDENCE: component-triad.md lines 105–114: 'security-sensitive visibility: owner-only operations live in a distinct meta-signal repo', '3. meta-signal is optional...authority boundary is a repo boundary'
- CLAIM: Workspace principle 'center design around schema types' requires the mirror's distinct schema (CheckpointMetadata, MirrorOutboxRow, PrivacyClass, RetentionPolicy) to live in the mirror component's own schema files, not grafted into Spirit or Mind
  EVIDENCE: system-designer/97 §4 lines 131–156 (schema-centric principle), signal-version-handover/INTENT.md lines 50–61 (mirror payload schema discipline)
- CLAIM: No precedent exists in the current workspace for config-selected role switching (Spirit-in-mirror-mode, etc.); all components are single-role daemons
  EVIDENCE: component-triad.md (all example components: persona, spirit, harness, orchestra, chroma, chronos are single-role), upgrade triad is upgrade-only (not upgrade-plus-mirror)
- CLAIM: Retention and privacy policy must be explicit, durable, and per-store; 'never GC' is not a default for all component stores
  EVIDENCE: system-operator/214 lines 183–185: 'Never GC on ouranos' is the strongest backup story, but private or high-churn stores may need classed retention and cryptographic erasure semantics'
- CLAIM: The recommended architecture is a dedicated mirror triad: mirror daemon (ouranos), signal-mirror (wire contract), meta-signal-mirror (policy authority), with per-store retention/privacy policy as durable sema-engine schema
  EVIDENCE: Synthesis of 97, 214, component-triad.md, repository-ledger pattern; no contradicting precedent in workspace

## openQuestions
- Should the mirror daemon open per-store directories (one per component store) or use a single append log with record headers for store routing? (Report 97 suggests per-store files; operator practice from repository-ledger suggests same pattern)
- What is the initial retention-policy default for Spirit-class state: keep-all, pruning-window, or ttl? Should it differ from low-value stores like cache/telemetry?
- Should the mirror-daemon listening socket be on the local ouranos filesystem (accessed via Tailscale forwarding) or bound to localhost:port with explicit Tailscale socket exposure? (Current triad pattern uses Unix sockets; no cross-host socket transport has been built)
- Which component owns the checkpoint-signing authority in this cut: the component daemon (Spirit) generating the checkpoint, or the mirror daemon? (Report 97 defers BLS; unclear whether checkpoint generation or server storage holds authority)
- Should the mirror implement Schema::PrivacyClass as a closed sum enum generated from its schema, or as per-store configuration? (Schema-centric principle suggests closed enum; operator flexibility suggests policy file)
- If the mirror scales to multiple ouranos instances in the future, should each component explicitly choose which remote it trusts, or should there be a quorum/replication pattern? (Out of scope for this cut per report 97, but affects meta-signal design now)

