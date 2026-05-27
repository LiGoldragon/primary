# Cloud Component Design Recap — Repos and Architecture

Date: 2026-05-27

## Question 1: Does Cloud Code Exist Yet?

**Yes, partial.** The full triad repos exist with skeleton daemon runtime. The three repositories (`cloud`, `signal-cloud`, `owner-signal-cloud`) are created and building. The daemon binds ordinary and owner Unix sockets, decodes `signal-frame` frames, and implements a read-only Cloudflare DNS observation path. Live provider mutation and full sema-engine persistence are intentionally deferred.

Repository status per `/home/li/primary/protocols/active-repositories.md` (lines 86–88):

- `/git/github.com/LiGoldragon/cloud` — runtime repo; Cargo.toml with two binaries, ARCHITECTURE.md, schema directory, and multi-module daemon code (`client.rs`, `cloudflare.rs`, `daemon.rs`, `lib.rs`).
- `/git/github.com/LiGoldragon/signal-cloud` — ordinary contract repo; Cargo.toml, ARCHITECTURE.md, standard contract structure.
- `/git/github.com/LiGoldragon/owner-signal-cloud` — owner contract repo; Cargo.toml, ARCHITECTURE.md, standard contract structure.

## Question 2: Triad-Shape Design Discipline

The cloud component inherits the five invariants and the single-argument rule from `~/primary/skills/component-triad.md`:

### The Five Invariants

1. **CLI has exactly one Signal peer — its daemon.** The `cloud` CLI binary is a thin NOTA-to-Signal adapter. It opens no database, no peer sockets, no other component connections. It exists as a temporary human/agent text bridge; once peer daemons speak Signal directly (which they already do in persona-introspect), the CLI is obsolete machinery. All runtime state lives exclusively in the daemon.

2. **Daemon's external surface is exclusively `signal-frame` frames.** No JSON, no NOTA on the wire between `cloud-daemon` and peer components. NOTA appears at three named projection edges: CLI argv/stdin, optional daemon↔harness terminal, and audit/debug dumps. Cloud daemon will speak Signal over its sockets to any peer daemon (future `domain-criome`, other infrastructure components).

3. **Verbs come in three layers.** (a) **Contract Operation** — the domain action: `State(CloudState)`, `PlanPreparation(DesiredState)`, `PlanApply(ApprovedPlan)`. (b) **Component Command** — daemon-internal: `CloudCommand::PrepareCloudflareZones`, `CloudCommand::ApplyPlan`. (c) **Sema Operation** — payloadless classification: `Assert`, `Mutate`, `Match`, `Subscribe`. The contract crate names Layer-1; daemon owns Layer-2; `signal-sema` supplies Layer-3 payloadless classification for cross-component observation.

4. **Two authority tiers — both in the triad.** `signal-cloud` is the ordinary peer-callable contract. `owner-signal-cloud` is owner-only authority (who owns cloud? future: `domain-criome` or infrastructure authority). Both contracts ship together. A daemon with only the ordinary surface is not yet triad-shaped.

5. **Policy state and working state — both in one sema-engine DB.** The daemon owns `cloud.redb` opened through `sema-engine`. Policy state (account credentials, capability zones, rate-limit policies) is seeded once from `bootstrap-policy.nota` on first start; thereafter, it changes only through owner-signal `Mutate` variants. Working state (prepared plans, applied-operation records, rate-limit tracking) is populated from operation alone. One database, two table categories, two authority boundaries.

### Single-Argument Rule

Every binary — `cloud` (CLI) and `cloud-daemon` (daemon) — takes exactly one argument:

- **CLI:** one NOTA argument matching a request variant from `signal-cloud` or `owner-signal-cloud`. Example: `cloud "(State Main)"` or `cloud ./state-query.nota`.
- **Daemon:** one NOTA config argument (identity, socket paths, redb path, bootstrap-policy path). Schema lives in `signal-cloud` or a small `cloud-config` crate.

**No flags.** No `--verbose`, no `--config=path`. Additional configuration becomes a field of the NOTA payload. The contract's NOTA schema is the only source of truth for what arguments mean.

### Naming Discipline

- **Repository:** `cloud` (unprefixed, top-level component; not `persona-cloud` or `signal-cloud-daemon`).
- **CLI binary:** `cloud` (short role-name, human types this often).
- **Daemon binary:** `cloud-daemon` (long-lived process, explicit `-daemon` suffix).
- **Signal contracts:** `signal-cloud` (ordinary) and `owner-signal-cloud` (owner-only).
- **Sockets:** daemon owns two Unix domain sockets — ordinary (mode 0600 or 0660) and owner-only (mode 0600). Paths and modes are set via daemon config.

### Signal Tree Layout

Future `cloud.schema` file (when schema-engine lands) will declare both working and policy splits:

- **Working contract** (`signal-cloud`): `State(…)` for observation, `PlanPreparation(…)` for planning, `Subscribe` for change events.
- **Policy contract** (`owner-signal-cloud`): `Mutate(AccountPolicy)` for credential/zone setup, `Mutate(CapabilityPolicy)` for authorization, `PlanApply(…)` for order-to-apply.

Per `/git/github.com/LiGoldragon/cloud/ARCHITECTURE.md` (lines 18–24), cloud owns provider execution; `domain-criome` owns domain meaning and provider-neutral projection. Cloud does not decide which Criome domains exist; it applies plans from authorized sources.

## Question 3: Adjacent Triads as Templates

The workspace has three mature triads that serve as design templates for cloud:

### 1. `persona-spirit` (Most Mature Triad)

**Location:** `/git/github.com/LiGoldragon/persona-spirit/`

Directory structure mirrors cloud's shape:
- `src/lib.rs`, `src/bin/spirit-daemon.rs`, `src/bin/spirit.rs`
- `schema/` directory for future schema work
- `bootstrap-policy.nota` (one-shot policy seed)
- `Cargo.toml` with three crates: `persona-spirit` (runtime), `signal-persona-spirit` (ordinary), `owner-signal-persona-spirit` (owner)

Key details:
- 35K character ARCHITECTURE.md with deep actor topology (Kameo actors: SpiritRoot, OwnerPlane, PolicyPlane, IngressPhase, NotaDecoder, ClassifierPlane, ClockPlane, DispatchPhase, SignalExecutor, SemaObserver, StatePlane, SubscriptionPlane, RecordStore, ReplyShaper, ReplyTextEncoder, SemaWriter, SemaReader).
- Two authority contracts: `signal-persona-spirit` (psyche statements, intent queries) and `owner-signal-persona-spirit` (lifecycle, identity, bootstrap-reload).
- Owns `persona-spirit.redb` sema-engine database with policy tables seeded from bootstrap and working tables from operation.
- Explicitly cites the component-triad skill and follows all five invariants.

Cloud should mirror persona-spirit's directory organization and socket/database naming patterns.

### 2. `domain-criome` (Parallel Triad, Active)

**Location:** `/git/github.com/LiGoldragon/domain-criome/`

Peer to cloud in the Criome ecosystem. Owns domain meaning; cloud owns provider execution. Both follow the triad:
- `domain-criome` (runtime) + `signal-domain-criome` (ordinary) + `owner-signal-domain-criome` (owner).
- ARCHITECTURE.md describes content-addressed per-domain authority.
- Example of triad applied to a registry/projection daemon with multiple provider backends (future: multiple resolution strategies).

Cloud's relationship to domain-criome is provider-side only; cloud consumes domain-criome's projections and applies them to provider APIs.

### 3. `signal-version-handover` and `upgrade` (Cross-Cutting Triad)

**Location:** `/git/github.com/LiGoldragon/signal-version-handover/`, `/git/github.com/LiGoldragon/upgrade/`

Specialized triad for version migration and daemon upgrade orchestration. Not a primary template (domain-specific), but demonstrates the triad applied to infrastructure concerns.
- `signal-version-handover` (ordinary wire contract)
- `owner-signal-version-handover` (owner authority)
- `upgrade` (runtime daemon + CLI)

Cloud is unlikely to adopt this pattern directly, but the ownership and authority-chain semantics (Mutate as authority order, Subscribe for observation) apply.

## Implementation Slice and Deferral Status

Per `/git/github.com/LiGoldragon/cloud/ARCHITECTURE.md` (lines 43–66):

**Current slice (0.1.0):**
- Bind ordinary and owner sockets.
- Decode signal-cloud and owner-signal-cloud frames.
- Return typed unsupported replies when no provider account configured.
- Runtime in-memory store for account policy and prepared plans.
- Generate local plans from `owner-signal-cloud::PlanPreparation`.
- Require owner approval before apply.
- Read-only Cloudflare DNS observation via environment-variable credential handles.

**Intentionally deferred:**
- Cloudflare live mutation (provider actor exists; apply endpoint returns typed rejection until mutation actor is real).
- sema-engine persistence (deferred because current `sema-engine` still pulls deprecated `signal-core` dependency; swap in after removal).
- Redirect observation and mutation.
- Schema-engine integration (waiting for schema MVP via spirit-next cutover).

**Hard constraints:**
- No provider credentials in source, logs, or ordinary Signal records.
- Secret material crosses owner policy only by handle (e.g., `CLOUDFLARE_DNS_TOKEN` environment variable).
- No direct provider calls from CLI.
- No deprecated `signal-core` in new code.
- Cloudflare is a provider adapter, not the domain model.

## Comparison: Cloud vs Persona-Spirit vs Domain-Criome

| Aspect | Cloud | Persona-Spirit | Domain-Criome |
|---|---|---|---|
| **Role** | Provider API execution | Psyche cognition; apex authority | Domain meaning & projection |
| **Binaries** | `cloud`, `cloud-daemon` | `spirit`, `persona-spirit-daemon` | `domain-criome`, `domain-criome-daemon` |
| **Ordinary contract** | `signal-cloud` (State, Plan, Subscribe) | `signal-persona-spirit` (Psyche, Intent, Query) | `signal-domain-criome` (Observation, Projection, Query) |
| **Owner contract** | `owner-signal-cloud` (Account, Zone, Apply) | `owner-signal-persona-spirit` (Lifecycle, Identity) | `owner-signal-domain-criome` (Registry, Delegation, Retire) |
| **Database** | `cloud.redb` (in-memory, sema-engine pending) | `persona-spirit.redb` (sema-engine live) | `domain-criome.redb` (sema-engine live) |
| **Maturity** | Skeleton (actor topology TBD, mutation unimplemented) | Deep (actor topology defined, full operation path) | Partial (registry foundation, projection TBD) |
| **Schema status** | Hand-written `signal_channel!` macros; schema conversion pending | Hand-written `signal_channel!` macros; schema MVP via spirit-next | Hand-written `signal_channel!` macros; schema conversion pending |

## Architecture References

- `/home/li/primary/skills/component-triad.md` — the universal triad shape (lines 1–90 essential).
- `/home/li/primary/skills/nota-design.md` — NOTA discipline for bootstrap-policy and config records.
- `/git/github.com/LiGoldragon/cloud/ARCHITECTURE.md` — cloud-specific actor topology (future).
- `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md` — mature actor topology reference (35K characters, full Kameo shape).
- `/git/github.com/LiGoldragon/domain-criome/ARCHITECTURE.md` — parallel triad example.
- `/home/li/primary/protocols/active-repositories.md` — curated attention map (lines 86–88 for cloud triad status).

## Synthesis

The cloud component triad exists in skeleton form. All three repos (runtime + two contracts) are in place with bindings, frame decoding, and read-only provider integration. The design inherits the triad shape perfectly: one daemon per component, CLI with one peer, two authority surfaces, single-argument rule, future sema-engine backing. The closest template is `persona-spirit` (full actor topology, deep ARCHITECTURE), with `domain-criome` as a peer example in the Criome ecosystem. Schema-engine integration is deferred until the spirit MVP lands; provider mutation is architecturally complete but operationally stubbed until the provider-actor infrastructure is real.
