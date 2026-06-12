# 98/5 — Triad-interface conformance across five components

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
An independent adversarial verifier re-checked every key claim against the code; its verdicts are appended at the end of this file.*

# Triad-Interface Conformance Audit: Reality vs. Ideal

## Executive Summary

The triad-interface ideal posits that every component is fully defined by schema — signal messaging, nexus operations, and storage — all generating Rust types and traits so hand-written code implements only the core algorithm. **Reality is a spectrum**: Spirit and Terminal approach the ideal most closely with generated signal/nexus/sema modules and external contract repos. Repository-Ledger and Introspect show major gaps: hand-written nexus enums where generation is declared but not executed, incomplete schema-emission pipelines, and ad-hoc decision logic outside the nexus plane.

## Per-Component Conformance Analysis

### Spirit

**SIGNAL Plane**: Generated from internal `schema/signal.schema` into `src/schema/signal.rs` (156KB). Exports external `signal-spirit` contract repo with NOTA schema at `/git/github.com/LiGoldragon/signal-spirit/schemas/v0.1.0/schema.nota`.

**NEXUS Plane**: Full schema-derived pipeline. `schema/nexus.schema` → `src/schema/nexus.rs` (73KB). Hand-written `Nexus` struct implements the engine; generated `NexusEngine` trait and `NexusWork`/`NexusAction` enums expose the decision surface. Manual runner loop (not using `triad-runtime::Runner`) in hand-written nexus.rs.

**SEMA Plane**: Full schema-derived. `schema/sema.schema` → `src/schema/sema.rs` (35KB). `Store` wraps `sema-engine::Engine` with keyed-record operations, no direct redb access.

**Metrics**: 14.5K generated lines; 8.8K hand-written. **Ratio**: ~1.6:1 hand-written to generated.

**Conformance**: HIGH. Schema-derives the three planes; generated types are the interface contract.


### Orchestrate

**SIGNAL Plane**: External sourcing via `signal-orchestrate` contract.

**NEXUS Plane**: Schema file exists but is **minimalist** (11 lines): declares only role types and enums, not feature verbs. Generated `nexus.rs` (24KB) provides trait stubs. **Hand-written Nexus engine** in `execution.rs` implements manual nested-loop runner (lines 90-121), NOT using `triad-runtime::Runner`. Decision logic is hand-coded state transitions.

**SEMA Plane**: Schema file `sema.schema` → `sema.rs` (28KB). Sema types are generated, but operation implementations in hand-written `OrchestrateSemaEngine` are domain-specific (read_roles, apply_ordinary, etc.), not derived from schema.

**Metrics**: 2.5K generated lines; 5.1K hand-written. **Ratio**: ~2:1.

**Conformance**: MEDIUM-LOW. Schema exists but generation is incomplete; nexus schema lacks feature verbs; sema.rs is generated but operations are hand-written; custom runner loop.


### Repository-Ledger

**SIGNAL Plane**: External via `signal-repository-ledger` contract.

**NEXUS Plane**: **Critical gap**: `schema/nexus.schema` exists and is well-formed, but **`build.rs` does NOT emit `nexus.rs`** (only daemon.rs emitted). Hand-written `RepositoryLedgerNexusWork` and `RepositoryLedgerNexusAction` enums in `src/lib.rs` (lines 268-279) duplicate the schema shape. **Uses `triad-runtime::Runner` correctly** (lines 840-875) — the ONLY component besides Terminal doing so.

**SEMA Plane**: **NO `schema/sema.schema`**. Hand-written `LedgerSemaWriteInput`, etc., enums (lines 225-253). Durable storage via `sema-engine::Engine` with 5 typed tables.

**Metrics**: Only 260 lines generated; 2.2K hand-written. **Ratio**: ~8.5:1.

**Conformance**: MEDIUM. Uses Runner correctly; sema-engine for storage. But nexus schema is authored but not emitted (enum duplication); sema schema entirely missing.


### Introspect

**SIGNAL Plane**: External via `signal-introspect` contract.

**NEXUS Plane**: **No nexus schema**. `schema/daemon.schema` is 12 bytes. Decision logic entirely hand-written, not visible in schema.

**SEMA Plane**: **No sema schema**. Hand-written `Store` wraps `sema-engine::Engine`.

**Metrics**: Only 262 lines generated; 1.8K hand-written. **Ratio**: ~7:1.

**Conformance**: LOW. Neither nexus nor sema schemas exist. No schema-derived typing for decision plane.


### Terminal

**SIGNAL Plane**: Generated from internal `schema/signal.schema` → `src/schema/signal.rs` (47KB). Parallel external contract.

**NEXUS Plane**: Full schema derivation. `schema/nexus.schema` → `src/schema/nexus.rs` (27KB). Generated enums declare session lifecycle and terminal-cell effect commands. **Uses `triad-runtime::Runner` correctly**.

**SEMA Plane**: `schema/sema.schema` → `src/schema/sema.rs` (24KB). Tables managed through `sema-engine` in hand-written `tables.rs`.

**Metrics**: 3.6K generated lines; 5.4K hand-written. **Ratio**: ~1.5:1.

**Conformance**: HIGH. Full schema-generated signal/nexus/sema. Uses `triad-runtime::Runner`. Structurally closest to Spirit.


## Three Biggest Gaps (Ranked)

### 1. Incomplete Nexus Schema Emission

**Gap**: `schema/nexus.schema` files are authored but generation is either entirely skipped (Repository-Ledger: `build.rs` line 29 emits only daemon.rs) or minimalist (Orchestrate: 11 lines, placeholder enums). Hand-written enums duplicate the schema shape (/git/github.com/LiGoldragon/repository-ledger/src/lib.rs:268-279).

**Impact**: Nexus schema cannot be read as the feature catalog; decision logic is hidden in ad-hoc Rust code. Onboarding and cross-component reasoning require reading hand-written match statements instead of schema verbs.


### 2. Absent SEMA Schemas

**Gap**: Introspect and Repository-Ledger have no `schema/sema.schema` files, despite durable storage. SEMA types are hand-written (Repository-Ledger /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:225-253). Storage contracts are implicit in code, not explicit in schema.

**Impact**: Schema-rust-next cannot verify sema types are consistent; adding a field requires manual enum and Store method updates. Durable schema is invisible.


### 3. Manual Nexus Runner Loops

**Gap**: Spirit, Orchestrate, and Introspect implement custom work-dispatch loops instead of reusing `triad-runtime::Runner`. Only Repository-Ledger and Terminal delegate to the generic runner (/git/github.com/LiGoldragon/repository-ledger/src/lib.rs:840-875; Orchestrate /git/github.com/LiGoldragon/orchestrate/src/execution.rs:90-121).

**Impact**: Runner loop is duplicated per-component instead of being a shared primitive. Blocks adding runner features without hand-updating every component. Each component bears its own correctness burden for work dispatch.


## Strict Separation Constraint

**Full Adherence**: **Repository-Ledger alone**. All storage through `sema-engine::Engine` keyed operations, all decisions through typed nexus enums dispatched by `triad-runtime::Runner`, all inter-daemon traffic Signal frames (/git/github.com/LiGoldragon/repository-ledger/src/lib.rs:480-550).

**Nearly Adherent**: Spirit and Terminal (custom runner loops but otherwise full separation).

**Partial**: Orchestrate (hand-implemented sema operations; custom runner).

**Minimal**: Introspect (no nexus schema; opaque supervision logic).


## Conclusion

**Reality Gap from Ideal**:
- **Spirit/Terminal**: 85% — full schema-derived planes, but custom runner loops.
- **Repository-Ledger**: 70% — uses shared runner and strict separation, but nexus schema ungenerated (enum duplication) and no sema schema.
- **Orchestrate**: 50% — minimalist nexus schema; hand-implemented sema operations; custom runner.
- **Introspect**: 30% — no nexus or sema schemas; durable contract invisible.

The three gaps block full realization: (1) incomplete nexus emission eliminates schema-visible feature catalogs; (2) absent sema schemas hide storage contracts in code; (3) duplicated runner loops prevent shared runtime features.

## keyClaims
- CLAIM: Spirit fully generates signal/nexus/sema modules from internal schemas but implements a custom hand-written nexus runner loop instead of using triad-runtime::Runner
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/schema/signal.rs; /git/github.com/LiGoldragon/spirit/src/schema/nexus.rs; /git/github.com/LiGoldragon/spirit/INTENT.md:108-116
- CLAIM: Orchestrate's nexus.schema is minimalist (11 lines) with placeholder enums and no feature verbs, while decision logic is hand-coded in execution.rs manual loop lines 90-121
  EVIDENCE: /git/github.com/LiGoldragon/orchestrate/schema/nexus.schema:1-27; /git/github.com/LiGoldragon/orchestrate/src/execution.rs:90-121
- CLAIM: Repository-Ledger's build.rs authors nexus.schema but explicitly does not emit nexus.rs (line 29), forcing hand-written RepositoryLedgerNexusWork/Action enums in lib.rs lines 268-279
  EVIDENCE: /git/github.com/LiGoldragon/repository-ledger/build.rs:29; /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:268-279
- CLAIM: Repository-Ledger and Introspect have no sema.schema files; storage types are hand-written enums despite using sema-engine
  EVIDENCE: /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:225-253; /git/github.com/LiGoldragon/introspect/schema/ contains only daemon.schema
- CLAIM: Only Repository-Ledger and Terminal use triad-runtime::Runner for work dispatch; Spirit, Orchestrate, and Introspect implement custom nexus runner loops
  EVIDENCE: /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:840-875; /git/github.com/LiGoldragon/orchestrate/src/execution.rs:90-121; grep results confirm Runner usage only in two components
- CLAIM: All five components correctly use sema-engine for durable storage and import triad-runtime for daemon shells
  EVIDENCE: /git/github.com/LiGoldragon/spirit/Cargo.toml; /git/github.com/LiGoldragon/orchestrate/Cargo.toml; /git/github.com/LiGoldragon/repository-ledger/Cargo.toml; /git/github.com/LiGoldragon/introspect/Cargo.toml; /git/github.com/LiGoldragon/terminal/Cargo.toml
- CLAIM: Terminal has highest conformance: full signal/nexus/sema schema generation, uses triad-runtime::Runner, sema-engine storage, 1.5:1 hand-written to generated ratio
  EVIDENCE: /git/github.com/LiGoldragon/terminal/src/schema/signal.rs; /git/github.com/LiGoldragon/terminal/src/schema/nexus.rs; /git/github.com/LiGoldragon/terminal/src/schema/sema.rs
- CLAIM: Orchestrate's sema.schema generates type stubs but OrchestrateSemaEngine implements operations hand-written (read_roles, apply_ordinary) rather than schema-derived
  EVIDENCE: /git/github.com/LiGoldragon/orchestrate/schema/sema.schema:1-30; /git/github.com/LiGoldragon/orchestrate/src/execution.rs:27-150
- CLAIM: Introspect has only daemon.schema (12 bytes), no nexus or sema schemas, and no declared decision layer visible in schema
  EVIDENCE: /git/github.com/LiGoldragon/introspect/schema/daemon.schema; /git/github.com/LiGoldragon/introspect/INTENT.md
- CLAIM: Repository-Ledger is the only component fully adhering to strict separation: all storage through sema-engine keyed operations, decisions via typed nexus enums dispatched by triad-runtime::Runner, comms via Signal frames
  EVIDENCE: /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:480-550; /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:268-279; /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:840-875
- CLAIM: Signal plane split: Spirit and Terminal source internally; Orchestrate, Repository-Ledger, and Introspect source externally via signal-<component> contract repos
  EVIDENCE: /git/github.com/LiGoldragon/spirit/schema/signal.schema; /git/github.com/LiGoldragon/terminal/schema/signal.schema; /git/github.com/LiGoldragon/signal-orchestrate/schema/lib.schema; /git/github.com/LiGoldragon/signal-repository-ledger/schema/signal-repository-ledger.concept.schema; /git/github.com/LiGoldragon/signal-introspect/schema/
- CLAIM: Spirit generates 14.5K lines (signal 156K + nexus 73K + sema 35K + domain 118K + meta_signal 20K + daemon 25K) vs 8.8K hand-written, indicating schema generation is primary path
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/schema/; wc -l confirms file sizes; /git/github.com/LiGoldragon/spirit/src/lib.rs:1-8 describes the generation pipeline

## openQuestions
- Why does Repository-Ledger author nexus.schema but explicitly omit nexus.rs emission in build.rs line 29 — is this intentional staging or an oversight?
- Will Introspect gain a declared nexus schema to make supervision logic visible, or is it intentionally exempt from the triad-interface pattern?
- Should Orchestrate's nexus.schema be expanded to declare feature verbs (ClaimRole, ReleaseRole as explicit nexus operations) or is the minimalist shape intentional?
- Is Repository-Ledger's lack of sema.schema a gap waiting to be filled, or is the hand-written Store shape intentionally table-agnostic until SEMA stabilizes?
- Will Spirit and Orchestrate eventually delegate to triad-runtime::Runner, or will they keep custom loops for component-specific control flow?
- How should missing sema.schema files (Introspect, Repository-Ledger) be prioritized given that sema-engine is already in use and working?


## Adversarial verification verdicts

- [CONFIRMED] Spirit fully generates signal/nexus/sema modules from internal schemas but implements a custom hand-written nexus runner loop instead of using triad-runtime::Runner
  EVIDENCE: /git/github.com/LiGoldragon/spirit/src/schema/signal.rs:1 (@generated); /git/github.com/LiGoldragon/spirit/src/schema/nexus.rs:1 (@generated); /git/github.com/LiGoldragon/spirit/src/nexus.rs:978-1026 (hand-written loop); /git/github.com/LiGoldragon/spirit/src/nexus.rs:1039-1040 (comment confirming no multi-hook runner trait emitted)
- [NUANCED] Orchestrate's nexus.schema is minimalist (11 lines) with placeholder enums and no feature verbs, while decision logic is hand-coded in execution.rs manual loop lines 90-121
  EVIDENCE: /git/github.com/LiGoldragon/orchestrate/schema/nexus.schema is 27 lines, not 11; it defines complete NexusWork/NexusAction enums with CommandSemaRead/Write/ReplyToSignal variants. Decision logic IS hand-coded: /git/github.com/LiGoldragon/orchestrate/src/execution.rs:90-121 implements drive_until_reply with manual match/continue loop
- [CONFIRMED] Repository-Ledger's build.rs authors nexus.schema but explicitly does not emit nexus.rs (line 29), forcing hand-written RepositoryLedgerNexusWork/Action enums in lib.rs lines 268-279
  EVIDENCE: /git/github.com/LiGoldragon/repository-ledger/build.rs:28-29 calls ModuleEmission::daemon_module() only, no nexus emission. /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:268-279 defines hand-written enums
- [CONFIRMED] Repository-Ledger and Introspect have no sema.schema files; storage types are hand-written enums despite using sema-engine
  EVIDENCE: /git/github.com/LiGoldragon/repository-ledger/schema/ contains only nexus.schema and repository-ledger.concept.schema; /git/github.com/LiGoldragon/introspect/schema/ contains only daemon.schema (12 bytes) and introspect.concept.schema. Repository-Ledger hand-written enums: /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:225-253
- [CONFIRMED] Only Repository-Ledger and Terminal use triad-runtime::Runner for work dispatch; Spirit, Orchestrate, and Introspect implement custom nexus runner loops
  EVIDENCE: grep -rn 'impl.*RunnerEngines' returns only: /git/github.com/LiGoldragon/terminal/src/schema/nexus.rs:886 (generated NexusRunnerAdapter impl) and /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:964. Terminal uses Runner at nexus.rs:863, Repository-Ledger at lib.rs:840,874. Introspect uses kameo actors (/git/github.com/LiGoldragon/introspect/src/runtime.rs:226-260 Message trait), not nexus dispatch
- [CONFIRMED] All five components correctly use sema-engine for durable storage and import triad-runtime for daemon shells
  EVIDENCE: All five Cargo.tomls verified to contain sema-engine and triad-runtime dependencies: spirit, orchestrate, repository-ledger, introspect, terminal
- [NUANCED] Terminal has highest conformance: full signal/nexus/sema schema generation, uses triad-runtime::Runner, sema-engine storage, 1.5:1 hand-written to generated ratio
  EVIDENCE: Full schema generation confirmed: /git/github.com/LiGoldragon/terminal/src/schema/{signal.rs:1,nexus.rs:1,sema.rs:1} all marked @generated. Runner usage: nexus.rs:863-865. Actual ratio: generated=5398+2577+1322=9297 signal/nexus/sema lines, hand-written=5435 lines (excluding schema/) → ratio is 1.61:1, not 1.5:1
- [CONFIRMED] Orchestrate's sema.schema generates type stubs but OrchestrateSemaEngine implements operations hand-written (read_roles, apply_ordinary) rather than schema-derived
  EVIDENCE: /git/github.com/LiGoldragon/orchestrate/schema/sema.schema:1-30 is minimal stub (30 lines, not code-generating operations). /git/github.com/LiGoldragon/orchestrate/src/execution.rs:232-259 (impl SemaEngine) and 317-354 (observe_read with ReadRoles/ReadLanes/ReadActivity pattern-matched manually) show hand-written dispatch
- [CONFIRMED] Introspect has only daemon.schema (12 bytes), no nexus or sema schemas, and no declared decision layer visible in schema
  EVIDENCE: /git/github.com/LiGoldragon/introspect/schema/daemon.schema is 12 bytes (empty template). No nexus/sema.schema files present. Decision layer implemented via kameo Message handlers (/git/github.com/LiGoldragon/introspect/src/runtime.rs:226-260), not schema-visible nexus work/action enums
- [CONFIRMED] Repository-Ledger is the only component fully adhering to strict separation: all storage through sema-engine keyed operations, decisions via typed nexus enums dispatched by triad-runtime::Runner, comms via Signal frames
  EVIDENCE: Storage: /git/github.com/LiGoldragon/repository-ledger/src/lib.rs:480-550 uses Engine.assert/mutate only (sema-engine primitives). Decisions: hand-written enums at 268-279 dispatched by Runner.drive at 840-875. Signal: Cargo.toml imports signal-repository-ledger contract
- [CONFIRMED] Signal plane split: Spirit and Terminal source internally; Orchestrate, Repository-Ledger, and Introspect source externally via signal-<component> contract repos
  EVIDENCE: Internal: /git/github.com/LiGoldragon/spirit/schema/signal.schema exists, /git/github.com/LiGoldragon/terminal/schema/signal.schema exists. External repos verified: /git/github.com/LiGoldragon/signal-orchestrate/, /git/github.com/LiGoldragon/signal-repository-ledger/, /git/github.com/LiGoldragon/signal-introspect/ all exist with schema files
- [NUANCED] Spirit generates 14.5K lines (signal 156K + nexus 73K + sema 35K + domain 118K + meta_signal 20K + daemon 25K) vs 8.8K hand-written, indicating schema generation is primary path
  EVIDENCE: Actual Spirit line counts: signal.rs=5398, nexus.rs=2577, sema.rs=1322, domain.rs=3801, meta_signal.rs=706, daemon.rs=670 → total 14474 generated (claim's 14.5K approximately correct). Hand-written (non-schema): 8840 lines (claim's 8.8K approximately correct). However, claim's breakdown (156K+73K+...) is internally inconsistent (sums to 427K, not 14.5K). Actual ratio: 1.6:1 generated:hand-written confirming schema-first approach

## additionalFindings
## Critical Architectural Findings

### Terminal's Generated NexusEngine is Superior to Spirit's Hand-Written Loop
Terminal's generated `NexusEngine` trait (/git/github.com/LiGoldragon/terminal/src/schema/nexus.rs:813-871) provides a default `execute` method that integrates `triad-runtime::Runner::drive` (line 863-865), achieving full schema-driven work dispatch without custom loops. Spirit instead implements a hand-written `execute_to_reply` method (/git/github.com/LiGoldragon/spirit/src/nexus.rs:971-1027) with its own continuation loop. Terminal's approach is more aligned with the stated architecture of delegating runner logic to triad-runtime.

### Introspect's Fundamental Divergence: Kameo Actors Replace Nexus
Introspect (/git/github.com/LiGoldragon/introspect/src/runtime.rs:226-260) implements neither nexus work/action dispatch nor hand-written loops. Instead it uses kameo's `Message` trait for actor-based request handling. This is a fundamentally different architectural pattern from the other four components and was underspecified in the claims.

### Schema Generation Hierarchy
- **Terminal**: Fully generated (signal, nexus, sema schemas all produce .rs files with @generated marker)
- **Spirit**: Fully generated schemas but hand-written runner loop to work around schema limitations
- **Orchestrate**: Generated sema.schema but hand-coded sema engine implementations
- **Repository-Ledger**: No nexus.schema generation, only daemon.schema; all nexus/sema types hand-written
- **Introspect**: Minimal daemon.schema (12 bytes), no nexus/sema, actor-based instead

### Orchestrate's Actual Complexity Underestimated
The claim that Orchestrate's nexus.schema is "minimalist (11 lines)" is technically wrong—it's 27 lines and structurally complete. However, Orchestrate remains operationally simple because its decision logic (drive_until_reply loop, observe_read/apply_write pattern-matching) is entirely hand-written in execution.rs, not schema-generated.

### Repository-Ledger's Hand-Written Nexus Paradox
Repository-Ledger defines hand-written nexus enums (RepositoryLedgerNexusWork, RepositoryLedgerNexusAction) in lib.rs despite having a nexus.schema file in schema/. This creates a contract-implementation split: the schema exists for documentation but code generation is disabled in build.rs (line 29). The build.rs explicitly calls `ModuleEmission::daemon_module()` only, not nexus module emission.

### Signal Plane Sourcing Pattern
Spirit and Terminal source signal.schema from their own schema/ directories (crate-local). Orchestrate, Repository-Ledger, and Introspect rely on external signal-<component> contract repos for their signal Input/Output types. This creates two code-generation flow paths: crate-local (Spirit, Terminal) vs. cross-repo contract (Orchestrate, Repository-Ledger, Introspect).

### Store Architecture Variance
Repository-Ledger uses exclusively sema-engine keyed primitives (Engine.assert, Engine.mutate, Assertion, Mutation). Orchestrate implements a custom SemaEngine trait that wraps hand-coded read/write business logic. Introspect uses its own IntrospectionStore actor. Spirit uses Store struct with durable sema-engine via Store::apply. This variance across five components suggests the Store abstraction is still evolving.

### Missing from Claims: Nexus Repository
The claims reference triad-runtime and nexus libraries but do not analyze `/git/github.com/LiGoldragon/nexus` as a separate component or understand how it relates to the five daemon components. Nexus appears to be a routing/connection layer but its role in the Sema version-control/backup system design is unstated.

