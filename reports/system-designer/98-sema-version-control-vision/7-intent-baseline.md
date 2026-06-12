# 98/7 — The Spirit intent log — binding set, adjacent intent, suspected-stale, gaps

*Sub-agent chapter of meta-report `reports/system-designer/98-sema-version-control-vision/`. Produced by a read-only exploration agent (workflow run `wf_a18d52f9-f89`, 2026-06-12), system-designer lane. 
This chapter reads reports/logs rather than code and was not adversarially verified.*

# Spirit Intent Log — Version Control + Backup Baseline

## Current Binding Set: Core VC + Backup Mandate

The following records establish the core version-control and backup system for component Sema databases:

### Foundational Constraints

**i4ak** (High/Maximum): The reusable component version-control system must support full distributed-version-control semantics over the typed database — branching, forking, rebasing, and merging — with per-component customizable intake/merge/rebase policy. Example: Spirit's guardian mediates rebase. Extends 29pb and j487.

**29pb** (High/High): Component Sema databases must be backed up to a server atomically; state loss is unacceptable. Pursue native version-controlled component databases rather than opaque binary blobs. Mechanism is Dolt-informed with strict-typed hard-migration-per-schema-change as core constraint.

**j487** (Medium/Medium): The version-controlled server-backed atomic durability mechanism must be built once as a reusable library of generic types and traits, not reimplemented per component. Every component has the option to version-control its state through this shared mechanism.

**x0ja** (High/High): One consistent cryptographic basis spans the entire VC and backup system: blake3 for all content addressing and criome BLS for signing and attesting history. No divergence across components.

### Database as Versioned Operation Log

**iir4** (High/High): The versioned operation log is the authoritative source of truth for component Sema state; the redb store becomes a rebuildable materialized view folded from the log. This kernel inversion is chosen for first VC implementation rather than deferred.

**qpv6** (High/High): For current SEMA VC implementation, keep the work in sema-engine now rather than creating new sema-vcs repository. Later extraction remains possible after engine nouns settle.

**2uhh** (High/High): The reusable VC design's IntakePolicy is a universal reusable admission interface with per-component implementations. Every path introducing entries to a branch routes through it unless superseded.

### Intake + Guardian Discipline

**kasm** (High/VeryHigh): The guardian decides an entry together with the new referents it introduces and the psyche statement justifying them as one atomic accept/reject. A referent is never admitted for a refused entry.

**zgi8** (High/VeryHigh): The Spirit guardian is the single locus of judgment; the model checks everything semantic — consistency, duplication, trample, non-intent — with only structural admission staying upstream.

**opbj** (High/High): Re-importing vetted records into a fresh Spirit database needs a privileged meta-signal Import operation that writes directly, preserving identifier/timestamp/fields, bypassing the guardian. Guardian-bypassing writes live only on meta-signal; working signal stays gated.

### Data Persistence + Storage

**fosp** (VeryHigh/Minimum): Sema-engine is the exclusive interface to the database. No component daemon may make direct redb calls. Components are dumb about storage and speak only sema-engine operations.

**e440** (High/Minimum): SEMA engine implements durable state as single-writer actor. Database upgrade operations flow through SEMA. Reads run in parallel (redb MVCC); single-writer invariant applies to writes only.

**ycwf** (High/Medium): Persistent typed-record store is the SEMA database. Adopt this vocabulary in all design conversations.

### Migration + Upgrade Discipline

**w1ss** (Medium/Minimum): Persona daemon schema migration uses in-process versioned reads. Every stored record carries schema-version tag; daemon dispatches read-side by tag, migrating older records on read into current shape. Zero downtime per schema bump. Per-record-version (not per-table).

**wrjl** (Medium/Minimum): Each persona contract carries explicit schema-layout schema in NOTA-based language, fully content-addressable — its hash is its identity. Version-checking pipeline detects schema-address mismatches and derives migration operations from diff.

**zf4v** (Medium/Minimum): Upgrade mechanism: (1) schema changes between versions; (2) schema-diff identifies moved/changed/dropped/renamed; (3) hand-written Rust bridge per version-boundary; (4) version number marks boundary; (5) new daemon recompiled with previous schema available; (6) auto-migration on database load.

**tmji** (Medium/Minimum): Sema-upgrade is a new persona-system component — universal stateful schema upgrade mechanism. First test case: legacy intent file log → spirit migration. Eventually schema-spec-language drives sema-upgrade transformations from declarative schema diffs.

**2ypu** (Medium/Minimum): Sema-upgrade-daemon starts FIRST on engine boot (before any persona daemon). First task: check whether database upgrade needed (compare stored schema-version-hash against current code's version-hash). Symmetric to spirit being LAST.

### Private/Encrypted State

**dun9** (Medium/High): Private component state organized as multiple key-gated stores on GoPass model. Each store encrypted to recipient keys; access is key possession. Per-store key is both access boundary and crypto-shred erasure unit. Explore rethinking Spirit as federation of key-scoped stores that multiple instances share as ciphertext, queries scoped to stores whose keys instance holds.

## Adjacent Design Intent: Storage, Schema, and Triad Foundations

### Schema as Source of Truth

**1aam** (High/Minimum): Schema is the macro-language source of truth for component data, wire, storage, and upgrade behavior.

**nm97** (High/Minimum): Components have TWO schema categories: EXTERNAL (wire contracts, database contracts) and INTERNAL (internal actor messages). Multiple schemas per component possible; each describes ONE channel. Internal schemas can change without breaking database or wire format.

**py4h** (High/Minimum): Upgrade mechanisms are live SEMA operations: protocol or database-format change is represented as typed operation/message, applied as database work, source for derived datatype and upgrade code.

**ngk0** (Medium/Minimum): Vocabulary discipline: authors always write from point of view of NEXT. MAIN = published baseline. PREVIOUS/LAST = prior iteration. Development model: if main == next at same revision, no upgrade path needed. If main != next, upgrade machinery generates From-chain.

### Serialization + Wire Protocol

**a9sq** (VeryHigh/High): rkyv binary form is SINGLE encoded representation living in BOTH database (sema body at rest) AND wire (signal movement). One byte layout, two homes. NOTA is text-readable projection emitted at CLI read time.

**bkcd** (High/VeryHigh): rkyv is universal wire base; NOTA codec is OPT-IN per consumer. Binary-only clients (daemon) must NOT have NotaDecode/NotaEncode compiled in — for leanness and contract clarity. Same data types across consumers; what differs is derive set, not wire shape.

**n5ch** (High/Minimum): NOTA mirrors binary self-describing root object plus relative-pointer box layout. Unsized fields become BOXES after root in declaration order. Coordinate notation supports access: (vector-N element-M).

**wv2a** (High/Minimum): Canonical name for 64-bit per-message prefix is "short header." Every message carries this; everything else is body. Structure is 8 enums total occupying 64 bits. Carries discriminator only; variant payload in Tier 3 body, NOT header.

### Component Triads + Architecture

**a71r** (VeryHigh/High): Every component engine in workspace triad defines and uses Signal/Nexus/SEMA interfaces in schema, conducts core logic through schema-emitted traits. Trait surface uniform across components; runtime is composition of schema-emitted trait implementations.

**fosp** (VeryHigh/Minimum): [Repeated for emphasis on sema-engine boundary]

## Suspected-Stale Records and Contradictions Requiring Psyche Resolution

### Major-Break-via-New-Repo Retirement (op4b vs vqtd)

**op4b** (VeryHigh/High, Correction 2026-06-07): Agents must NOT create new GitHub repos for architectural breaks/experiments/mockups. Work belongs on feature branches in worktrees. Skill major-break-via-new-repo is RETIRED. Default is feature-development branches/worktrees. New repositories only on explicit psyche authority.

**vqtd** (High/Medium, Principle): Methodology for major architectural breaks: create new repository with -next or -v2 suffix, signal prototype status, enable parallel development without disrupting production on old repo. After stabilization, rename to canonical short name.

**Status**: op4b is newer (2026-06-07) and bears Maximum/VeryHigh certainty labeling it a correction that supersedes vqtd's older principle. However, vqtd frames -next branches as acceptable alternative. Current state: major-break-via-new-repo is RETIRED; -next branches on existing repos (e.g., vpa5) or feature branches in worktrees are approved paths.

### Operator vs Designer Authority on New Concept Repos (nzf3)

**nzf3** (Medium/Minimum, Decision 2026-05-26): Operator may work directly on main of NEW concept-prototype repos without standard designer-feature-branch/operator-rebase ceremony. Exception applies only to fresh repos with no production history; production-track repos retain standard discipline.

**Current State**: This appears to be a greenfield-only exception. Requires clarification: is op4b's retirement of new-repo creation in tension with nzf3's allowance of operator-main work on fresh concept prototypes? The psyche's 2026-06-07 directive (op4b) appears stricter. Reconciliation: op4b says "new repositories created only on explicit psyche authority"; nzf3 authorizes operators to work directly on fresh concept-prototype repos that ARE created. These do not contradict if the psyche has pre-authorized operator creation of concept-prototype repos as a category.

### Design vs New-Stack Repo Branching (o5rz vs 6xzu)

**6xzu** (High/VeryHigh, Decision): Designer roles work on standard next branch by default; operators own main and integrate. Breaks happen on next.

**o5rz** (High/Minimum, Clarification): For new-stack rewrite repos (lojix, signal-lojix, meta-signal-lojix, etc.) — NOT production deploy logic — work is pushed directly to main with no next/feature-branch ceremony. Psyche does not want designer-next/operator-main split on greenfield non-production rewrite.

**Status**: CONSISTENT. 6xzu governs PRODUCTION code repos. o5rz explicitly carves out greenfield non-production new-stack repos as exception. No contradiction.

### Schema-Derived Spirit Pilot vs Sema-Engine Boundary (fosp)

**fosp** (VeryHigh/Minimum, Correction): Sema-engine is exclusive interface to database. Schema-derived spirit pilot bypassed sema-engine with raw redb — misunderstanding of sema-engine's role. Components are dumb about storage.

**Status**: This is a flagged correction pointing to pilot architecture error, not a stale design intent. The VC system MUST respect sema-engine boundary going forward.

### Guardian Admission vs Pre-Authorized Import (opbj vs general guardian discipline)

**opbj** (High/High, Decision): Re-importing vetted records needs privileged meta-signal Import that bypasses guardian.

**Status**: NOT contradictory. Guardian discipline applies to all NEW intent capture. opbj handles the special case of RESTORING/IMPORTING existing vetted records into fresh database — a data-restoration path, not ordinary capture. This is design-complete and non-contradictory.

### Archive Semantics (3pfh)

**3pfh** (Medium/Minimum, Decision): Spirit archive semantics are redirect-forward-only: setting archive target re-points future writes/reads to new target; records already in prior archive stay in place, NOT migrated forward.

**Status**: Clear decision. May seem stale vs later archival records (o70j, pn0n) but is consistent — those records discuss NEW archival mechanics, not contradiction of redirect-only semantics.

## Gaps: Questions the Log Does NOT Answer

### 1. Specific Intake Policy Mechanisms

The log defines IntakePolicy as "universal reusable admission interface" (2uhh) but does NOT specify:
- Per-component override semantics (what does customizable intake policy look like in code?)
- Rejection criteria beyond "guardian judges" (what specific rebase conflicts, data collisions, or policy violations trigger rejection?)
- merge/rebase policy specifics (3-way merge? rebase semantics for operation log? cherry-pick filtering?)

**Implementer question**: Do you need a designer prompt specifying detailed intake policy mechanics, or is that left to per-component design?

### 2. Operation Log Format + Content Addressing

**iir4** establishes operation log as authoritative source, but the log does NOT specify:
- What constitutes an "operation" in the log? (atomic transaction? single write? state diff?)
- Content addressing scheme for log entries (blake3 hash of what? full operation? operation+timestamp?)
- Log structure (append-only linear? DAG for branches?)
- Log replayability semantics (deterministic replay of all operations → current state?)

**Implementer question**: Is operation log a sequence of Sema mutations (one per write), or coarser-grained transactions? How do branches relate to log entries?

### 3. Federation + Distributed Semantics

**i4ak** says "distributed-version-control semantics" but the log does NOT detail:
- Multi-peer merging (if Spirit A and Spirit B diverge, how do they reconcile?)
- Conflict resolution protocol (who decides which entry wins in a fork?)
- Pull/push semantics (dun9 mentions "federation of key-scoped stores" but mechanism is exploratory/open)

**Implementer question**: Is the VC system primarily for per-instance version history (one Spirit backing up to a server), or full multi-peer distributed merge semantics?

### 4. Guardian + Psyche Interaction Protocol

The log DESCRIBES guardian judgment (zgi8, kasm) but does NOT specify:
- What constitutes a "psyche statement"? (exact format, quoting discipline, provenance chain?)
- How does guardian retrieve psyche statement? (where stored? who provides?)
- Guardian feedback loop on rejection (does psyche see guardian reasoning? how detailed?)
- Multi-step mediation (if guardian rejects, can submitting agent appeal or reword?)

**Implementer question**: Is there a detailed guardian protocol/spec document, or is that part of Spirit's next-generation schema work?

### 5. Key-Gated Store Mechanics (dun9)

**dun9** envisions "federation of key-scoped stores" but details are marked "explore rethinking." Unspecified:
- Key derivation/management (how are keys generated? stored? rotated?)
- Store isolation mechanics (can one Spirit instance hold keys for multiple stores? merge across keys?)
- Erasure receipt format (what constitutes cryptographic proof of shredding?)
- Query scoping (how does daemon know which stores a query can access?)

**Implementer question**: Is key-gated federation a Phase 2 design, or should VC Phase 1 assume simpler single-store encryption?

### 6. Server Backup Target

**29pb** requires "backup to a server atomically" but does NOT specify:
- Server protocol (HTTP? custom daemon? SSH?)
- Backup trigger (on every write? periodic? explicit?)
- Consistency guarantee (what makes backup "atomic"? transaction-level? database-level?)
- Server durability model (replicated? quorum?)

**Implementer question**: Should first VC implementation target a simple server endpoint, or is server design part of the same effort?

### 7. Integration with Criome Signing

**x0ja** mandates "criome BLS for signing and attesting history" but the log does NOT specify:
- What gets signed? (individual entries? log root hash? batches?)
- Signature verification protocol (who verifies? when?)
- Attestation format (what counts as "attesting history"?)
- Pre-Criome path (is BLS signing conditional on Criome availability, or mandatory from start?)

**Implementer question**: Does VC Phase 1 assume Criome is deployed, or should it degrade gracefully without it?

### 8. Schema Migration During VC Operations

The log covers schema migration in isolation (w1ss, wrjl, zf4v) but does NOT address:
- Can version-control branches exist at different schema versions? (branch A on v1, branch B on v2?)
- Merge semantics across schema versions (how do you merge v1 operation from branch A into v2 branch B?)
- Rebase with migration (does rebase trigger schema upgrade?)

**Implementer question**: Is the assumption that all branches stay synchronized on schema version, with upgrades coordinated separately?

### 9. Content Erasure + Retention Policies

**dun9** mentions "accountable content-erasure via crypto-shredding" but does NOT detail:
- Retention class definitions (how many classes? transient/normal/permanent?)
- Erasure trigger (explicit? time-based? garbage collection?)
- Erasure audit trail (who can query what was erased and when?)

**Implementer question**: Is this part of the data-lifecycle-ladder work (q4l0), or does VC Phase 1 assume simple delete semantics?

### 10. Triad Coordination + Cutover

**iir4, qpv6** place VC in sema-engine, but do NOT specify:
- How spirit-engine (the guardian, the intent logic) coordinates with sema-engine (versioning)?
- What happens to intent records during operation-log rebase?
- Does spirit run INSIDE sema-engine or alongside?

**Implementer question**: Is sema-engine the database kernel (low-level storage), with spirit-engine and VC logic above it, or does sema-engine include VC as internal machinery?

## Summary Observations

1. **Kernel Inversion is Decided** (iir4): Operation log → materialized view is the architecture. This is non-negotiable.

2. **Guardian as Gatekeeper is Decided** (zgi8, kasm): IntakePolicy must route through guardian. Design is firm.

3. **Cryptographic Consistency is Decided** (x0ja): blake3 + criome BLS, no divergence.

4. **Schema Migration is Decided but Evolving** (w1ss, wrjl, zf4v, ngk0): In-process per-record versioning with structured upgrade operations. Precise code shape is still being researched (wrjl notes "warrants deep testing").

5. **Federation is Exploratory** (dun9, i6ih): Last-known-acknowledgment pattern is described; full multi-peer merge semantics are under design.

6. **Guardian + Psyche Protocol is Incomplete**: The log describes WHAT the guardian does (judgment, gating), but the PROTOCOL (how it retrieves psyche statements, formats feedback) is not fully detailed in the observable records.

7. **Server Backup Target is Constrained but Unspecified**: Must exist, must be atomic, must support Dolt-informed mechanism; exact protocol/topology deferred.

8. **First Implementation Constraints are Clear**: Sema-engine boundary (fosp), single-writer SEMA actor (e440), per-record-version migration (w1ss), binary rkyv protocol (a9sq, bkcd). These set implementation boundaries.



## keyClaims
- CLAIM: The reusable component version-control system is foundational and must support full distributed-version-control semantics (branching, forking, rebasing, merging) over the typed database with per-component customizable intake, merge, and rebase policy.
  EVIDENCE: i4ak (High/Maximum)
- CLAIM: The versioned operation log is the authoritative source of truth for component Sema state; the redb store becomes a rebuildable materialized view folded from the log.
  EVIDENCE: iir4 (High/High)
- CLAIM: Component Sema databases must be backed up to a server atomically; state loss is unacceptable. Pursue native version-controlled component databases rather than opaque binary blobs with strict-typed hard-migration-per-schema-change as core constraint.
  EVIDENCE: 29pb (High/High)
- CLAIM: One consistent cryptographic basis spans the entire version-control and backup system: blake3 for all content addressing and criome BLS for signing and attesting history. No component diverges in hash function or crypto.
  EVIDENCE: x0ja (High/High)
- CLAIM: The version-controlled server-backed atomic durability mechanism must be built once as a reusable library of generic types and traits, not reimplemented per component.
  EVIDENCE: j487 (Medium/Medium)
- CLAIM: The reusable VC design's IntakePolicy is a universal reusable admission interface with per-component implementations. Every path introducing entries to a branch routes through it unless a later design explicitly supersedes.
  EVIDENCE: 2uhh (High/High)
- CLAIM: The Spirit guardian is the single locus of judgment; the model checks everything semantic (consistency, duplication, trample, non-intent) with only structural admission staying upstream.
  EVIDENCE: zgi8 (High/VeryHigh)
- CLAIM: Sema-engine is the exclusive interface to the database. No component daemon may make direct redb calls. Components are dumb about storage and speak only sema-engine operations.
  EVIDENCE: fosp (VeryHigh/Minimum)
- CLAIM: SEMA engine implements durable state as single-writer actor: queries, writes, mutations, additions. Database upgrade operations flow through SEMA. Reads run in parallel (redb MVCC); single-writer invariant applies to writes only.
  EVIDENCE: e440 (High/Minimum)
- CLAIM: Persona daemon schema migration uses in-process versioned reads. Every stored record carries schema-version tag; daemon dispatches read-side by tag, migrating older records on read into current shape. Zero downtime per schema bump. Per-record-version (not per-table).
  EVIDENCE: w1ss (Medium/Minimum)
- CLAIM: Sema-upgrade-daemon starts FIRST on engine boot before any persona daemon. First task: check whether database upgrade needed (compare stored schema-version-hash against current code's version-hash).
  EVIDENCE: 2ypu (Medium/Minimum)
- CLAIM: Private component state is organized as multiple key-gated stores on GoPass model with per-store key as both access boundary and crypto-shred erasure unit. Explore rethinking Spirit as federation of key-scoped stores that multiple instances share as ciphertext.
  EVIDENCE: dun9 (Medium/High)

## openQuestions
- What does per-component customizable intake policy look like in code? What are the rejection criteria beyond guardian judgment? Does 3-way merge apply, or operation-log-specific semantics?
- What constitutes an operation in the log? How are log entries content-addressed? Is the log append-only linear, a DAG for branches, or something else? What are replayability semantics?
- Is the VC system primarily for per-instance version history backing up to server, or full multi-peer distributed merge semantics? How do multiple Spirit instances reconcile divergence?
- What is the exact protocol between submitting agent, guardian, and psyche? How does guardian retrieve psyche statements? What format counts as valid testimony? Can agents appeal rejections?
- Is key-gated federation (dun9) a Phase 2 design, or should VC Phase 1 assume simpler single-store encryption? What is the key derivation, rotation, and store-isolation protocol?
- What server protocol, trigger, and consistency model are required for backup? Should first VC implementation target a simple server endpoint, or is server design part of the same effort?
- Is criome BLS signing mandatory from start, or conditional on Criome availability? What gets signed (individual entries, log root, batches)? What is the signature verification protocol?
- Can version-control branches exist at different schema versions? How do you merge across schema versions? Does rebase trigger schema upgrade, or must all branches stay synchronized on version?
- Is data-lifecycle-ladder classification (retain/archive/purge) part of VC Phase 1, or does it assume simple delete semantics?
- How does spirit-engine coordinate with sema-engine during VC operations? Does sema-engine include VC as internal machinery, or is VC a separate layer above sema-engine? What happens to intent records during operation-log rebase?

