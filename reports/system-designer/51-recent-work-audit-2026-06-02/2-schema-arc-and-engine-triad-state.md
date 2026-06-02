# Schema arc + engine-triad repo state — 2026-06-02

*Sub-agent 2 of the system-designer recent-work audit. Read-only audit of
the schema-derived stack and the engine-triad consumer repos: where each
sits, what landed recently, where migration gaps to per-repo
`ARCHITECTURE.md` and skills remain.*

## Frame

Repos in scope:

- **Schema arc** (the type-emission stack) — `nota-next`, `schema-next`,
  `schema-rust-next`, `schema-core`.
- **Engine-triad consumers** (each a daemon owning Signal/Nexus/SEMA
  internally) — `spirit-next` (canonical worked example),
  `persona-spirit` (deployed today), `sema`, `sema-engine`, `nexus`,
  `upgrade`.

For each repo: recent jj log, ARCHITECTURE.md/INTENT.md state, code state
for engine-trait pattern, migration gaps. The two through-lines:

1. **Engine-trait pattern** — the Spirit 1327 Principle that Signal /
   Nexus / SEMA planes are emitted as trait surfaces; Signal=triage+reply
   (2 methods), Nexus=execute (1 method), SEMA=apply+observe (2
   methods).
2. **Designer 447 F6 manifestation** — upgrade-as-SEMA + self-editing
   schema-daemon design authored at Maximum certainty (Spirit 1308-1314);
   has it reached `/git/github.com/LiGoldragon/upgrade/` or anywhere?

## Per-repo state

### `nota-next` — raw NOTA structural floor

**Recent activity:**

```text
pswlszqw 2026-06-01 designer: constraint tests for operator-271 closed claims 2 and 3
mtqruwxs 2026-06-01 nota: make FieldEncode data-bearing
tomkmzsq 2026-05-27 INTENT: name recurring patterns E, F realised in nota-next (record 988)
uxyoqzmt 2026-05-27 INTENT: NOTA below the three execution centers (record 970)
mpzwlkvz 2026-05-27 INTENT + ARCHITECTURE: manifest brace key-value, no-\n inline NOTA, ...
```

**ARCH/INTENT state:** Both files exist, recent, substantive (~111 +
~80 lines). They reflect 2026-05-27 manifestation work for records 712,
882, 894, 902, 922, 927, 964, 965, 970, 988. The recent
`make FieldEncode data-bearing` commit (`mtqruwxs`) confirms the
no-ZST-namespace rule actively applied — that's the workspace-level
rule from Spirit 712/882 still landing in this repo.

INTENT (lines 56-58) names body-stream semantics: "after NOTA structural
parsing matches a file body or a delimited object, the next semantic
parsing step should receive the matched body's inner object stream
rather than the outer delimiter wrapper" — that's Spirit 1287/1290
landed.

**Code state:** No engine-trait — out of scope for this repo (NOTA is
below the three execution centers per record 970). The codec layer
(`NotaDecode`/`NotaEncode`) is the schema-emission contract; the macros
substrate is the structural-matching contract. Both are concerns
upstream of the engine-trait pattern.

**Gaps:** None for engine-trait. The repo's own next slice is the
macro-node substrate convergence with schema-next (move structural cases
fully into nota-next).

### `schema-next` — schema authoring (input)

**Recent activity:**

```text
mlmzuupx 2026-06-01 designer/452: audit rkyv enum-wrapping presumption on MacroPatternObject pilot
wwpspulk 2026-06-01 designer: constraint tests for operator-271 closed claims 1, 4, 5
rowlrytn 2026-06-01 schema: collapse macro library data mirrors
pzmvslmo 2026-05-28 schema-next: lower collections and types-only modules
tyxqyytv 2026-05-28 sigil grammar: @-prefix macro invocations + *-suffix same-name variants
```

**ARCH/INTENT state:** Both files exist, very substantive (~373 +
~280 lines). The INTENT names: schema substantive shape (strict
brace key-value, brackets-as-NOTA-vectors per record 1259), macro nodes
as first-class structural expectations, declarative macro expansion
keeping NOTA structure as data, scalar pass-throughs in asschema (not
just in Rust emission), and the cross-crate `ImportResolver`
architecture that ratifies schema-core (lines 89-93 of INTENT).

The ARCH ends with the SchemaPackage layer (lines 234-247) — the
cross-crate import resolution floor for schema-core.

**Code state:** No engine-trait pattern lives in schema-next code
itself — schema-next is an authoring/lowering layer; the engine trait
surfaces are emitted by schema-rust-next. But schema-next ratifies the
SignalEngine/NexusEngine/SemaEngine pattern by recognising the schema
shapes that trigger emission (`Input`/`Output`, `NexusInput`/`NexusOutput`,
`SemaWriteInput`/`SemaWriteOutput` + `SemaReadInput`/`SemaReadOutput`).

**Gaps:**

- No explicit reference to Spirit records 1308-1314 (designer 447's
  upgrade-as-SEMA + self-editing schema-daemon).
- `MigrationEmitter` (designer 447 §"What schema-next has today") is the
  named next slice; no trace in the repo yet.
- `SchemaSemaEngine` (designer 447's apply-edit-to-asschema engine) —
  no trace.
- Generally schema-next is bounded by the "library-only" boundary; the
  schema-daemon repo would be a new sibling per designer 447. The
  question of where it lives is open.

### `schema-rust-next` — Rust emitter (output)

**Recent activity:**

```text
mrszoqmw 2026-06-02 schema-rust: prefer exact plane routes over payload fallback
yntmltpr 2026-06-01 schema-rust-next: emit plane trace traits + actor super-traits behind runtime-trace
prskxpqu 2026-06-01 schema-rust: remove legacy single sema surface
ukwywlus 2026-05-30 schema-rust: default to feature-gated NOTA emission
```

**ARCH/INTENT state:** Both files exist, very substantive. **This is
the only repo in the entire stack whose ARCH+INTENT explicitly
mentions engine-trait emission**. ARCH lines 106-115 and INTENT
lines 66-86 are the canonical engine-trait specifications:

- `Input`/`Output` → `SignalEngine` (triage_inner + reply_inner)
- `NexusInput`/`NexusOutput` → `NexusEngine` (execute)
- `SemaWriteInput`/`SemaWriteOutput` + `SemaReadInput`/`SemaReadOutput`
  → `SemaEngine` (apply + observe)

ARCH lines 116-124 + INTENT lines 78-86 add the testing-trace hook
substrate (designer 464): `triage_inner`/`reply_inner`/`decide`/
`apply_inner`/`observe_inner` are inner methods; default wrappers
supply trace-event names like `SignalTriaged`/`NexusEntered`/
`SemaWriteApplied`.

The 2026-06-02 commit `mrszoqmw` adds plane-route exactness; the
2026-06-01 `yntmltpr` lands actor super-traits behind `runtime-trace`.

**Code state:** This repo is the emitter; the engine traits manifest in
its consumers. Schema-rust-next's job is to recognise the schema shapes
and emit the trait surfaces. Confirmed working: spirit-next consumes
those emissions in src/engine.rs:194 (SignalActor impl SignalEngine),
src/nexus.rs:62 (Nexus impl NexusEngine), src/store.rs:40 (Store impl
SemaEngine).

**Gaps:**

- `Plane::{Signal,Nexus,Sema}` cross-plane match-surface is referenced
  in ARCH lines 92-95 + INTENT lines 38-43; landed in spirit-next.
- Variant projection emitter (designer 444 §"Companion cut" + designer
  443 sub-agent 4 Finding 2): named but not yet in ARCH. The three
  identical `FromMail<Payload>` impls (~200 lines per component) are
  not emitted yet.
- Schema-core extraction (designer 444 §"The schema-core extraction
  horizon"): the envelope substrate (~600 lines) that should be lifted
  into schema-core is still emitted per-component. ARCH does not yet
  describe the "emit `use schema_core::Signal;` instead of inline"
  cutover.

### `schema-core` — cross-crate-import proof (KEY NEW)

**Recent activity:**

```text
plmsuyqw 2026-05-28
vttulquq 2026-05-28 schema-core: witness cross-crate schema imports
```

Only two commits, both 2026-05-28, no activity since.

**ARCH/INTENT state:** Both exist. ARCH is ~84 lines, tightly scoped
to "the running proof that a schema type declared in one crate can be
imported by another crate's schema and referenced — not re-declared —
in the importing crate's generated Rust." It documents:

- The two-member Cargo workspace (`core/` + `consumer/`).
- The cross-crate import flow through Cargo `links` + `DEP_*` env vars
  + `ImportResolver`.
- Why it works in Nix (crane respects `DEP_*` because Cargo sets it
  regardless of build system).
- Distinct from the `{ }` Imports brace records (path-mapping data
  types — orthogonal concern).
- Iteration-N concerns: shared-types crate carries trivial Input/Output
  signal-plane noise; version resolution is single-version happy-path;
  error bridge collapses cross-crate parse failures.

INTENT (~48 lines) sources the work to "Psyche directive 2026-05-28
(Spirit record 1009, High): research whether schema-next can reuse
Cargo's crate-build setup to find schema libraries by the single-colon
module naming (`crate:module:Type`), deterministically, working in
Nix." The constraint list is mechanically precise: `links =
"schema-core"`, `cargo::metadata=schema-dir=<crate-root>/schema`,
`DEP_SCHEMA_CORE_SCHEMA_DIR`, `ImportResolver`,
`pub use schema_core::schema::mail::DatabaseMarker as DatabaseMarker;`.

The only declared shared noun today is `DatabaseMarker` in
`core/schema/mail.schema` — `CommitSequence`, `StateDigest`, and the
2-field `DatabaseMarker` struct.

**Code state:** No engine-trait. By design; schema-core is shared
primitives ratification, not a daemon. Note: there is no `AGENTS.md`
in schema-core.

**Gaps:** The interesting ones (see §"schema-core directional question"
below).

### `spirit-next` — canonical engine-trait worked example

**Recent activity:**

```text
rvqonmyv 2026-06-02 spirit-next: name-only trace prototype (designer 467)
yprztwqr 2026-06-01 spirit-next: use generated engine trace hooks
wrlxxyps 2026-06-01 designer 464 — testing-trace trait emit + CLI translation + debug wrapper enum
uxxsqrmy 2026-06-01 spirit-next: name trace events by runtime phase
xwkoytrv 2026-06-01 spirit-next: prototype testing-build logging-socket witness
prxrlrkw 2026-06-01 spirit-next: keep only schema triad runtime path
zmoynusn 2026-05-30 workspace split: daemon zero-NOTA + state-aware startup + numerator (records 1236-1241)
kmvzuspo 2026-05-28 docs: manifest three trait-ordered engines + runtime origin route
yvunykuu 2026-05-28 three trait-ordered engines + runtime origin route
oqkqtktn 2026-05-28 spirit-next: real Nexus mail-keeper + durable redb SEMA store
```

**ARCH/INTENT state:** Both substantive. ARCH ~390 lines, INTENT ~195
lines. Both extensively reference engine-trait emission, plane
namespaces (`signal::Input`, `nexus::Input`, `sema::WriteInput`),
mail-event nouns, testing-trace surface, and origin-route flow.

ARCH §"Runtime triad" (lines 76-202) is the canonical flow:
- `SignalActor::admit` mints origin route + `MessageSent`, produces
  `SignalAccepted`.
- `SignalAccepted::process_with` runs Signal triage → Nexus execution →
  Signal reply, emitting `MessageSent`/`MessageProcessed` hooks.
- `Nexus` implements `NexusEngine`; its `execute(&mut self, ...)`
  mutable borrow is the single-flight guard.
- `Store` implements `SemaEngine`; `apply(&mut self, WriteInput)` +
  `observe(&self, ReadInput)` are split borrows.

INTENT cites Spirit 1339 (line 54): "the one working path is the
schema-plane trait path: Signal emits a generated Nexus envelope,
Nexus executes it, and SEMA is reached only through generated split
write/read roots." Old design-convenience APIs do not stay beside the
working interface. The 2026-06-01 `prxrlrkw` commit ("keep only schema
triad runtime path") implements this — parallel bypass paths removed.

**Code state:**

```text
src/engine.rs:194:impl SignalEngine for SignalActor {
src/engine.rs:200:    fn triage_inner(&self, input: signal_plane::Signal<Input>) -> nexus_plane::Nexus<NexusInput>
src/engine.rs:205:    fn reply_inner(&self, output: nexus_plane::Nexus<NexusOutput>) -> signal_plane::Signal<Output>
src/nexus.rs:62:impl NexusEngine for Nexus {
src/store.rs:40:impl SemaEngine for Store {
src/store.rs:46:    fn apply_inner(...)
src/store.rs:80:    fn observe_inner(...)
```

All three engine traits implemented with the correct inner-method shape
(designer 464's trace-hook substrate). The mutable borrow is at
`NexusEngine::execute` taking `&mut Nexus`.

**Gaps:** Minor. The `last-version` upgrade-test package needs a real
previous release input/tag (INTENT line 146-149). The schema diff/upgrade
designer 447 mechanism has not landed; only the `UpgradeFrom`/`AcceptPrevious`
trait surfaces exist with no implementations.

### `persona-spirit` — deployed Spirit 0.3.0 CLI

**Recent activity:**

```text
sykytlkq 2026-06-01 persona-spirit: add verbal recency depth queries
ruplsyyq 2026-05-25 persona-spirit: refresh retrofit lockfile
ptmpozty 2026-05-26 persona-spirit POC: refactor free functions to methods/From impls per psyche 2026-05-26 (intent 712)
xwskupur 2026-05-26 persona-spirit: serve record identifier queries
quwtprym 2026-05-26 persona-spirit: wire runtime to schema-derived turn table
```

**ARCH/INTENT state:** Both substantive. ARCH ~544 lines, INTENT ~313
lines. **Neither file references `SignalEngine`, `NexusEngine`, or
`SemaEngine` anywhere.** ARCH describes the deployed Kameo-actor
architecture: SpiritRoot → IngressPhase → DecodePlane → DispatchPhase →
ClassifierPlane / ClockPlane / SignalExecutor / SemaObserver /
StatePlane / SubscriptionPlane / RecordStore / ReplyShaper /
ReplyTextEncoder. ARCH §"Schema-driven actor architecture (next-substrate)"
(line 194) names a parallel substrate but on the
`designer-schema-full-stack-spirit-2026-05-25` branch, not main.

**Code state:** No `SignalEngine`/`NexusEngine`/`SemaEngine` anywhere
in src/. Kameo actor tree is the working architecture.

**Gaps (large):**

- Persona-spirit is the **deployed** Spirit but its architecture is the
  pre-engine-trait Kameo actor tree. The cutover gap from spirit-next
  (engine-trait worked example) to persona-spirit (deployed) is
  unmigrated.
- Spirit records 1308-1339 not cited.
- Engine-trait pattern not absorbed into ARCH/INTENT, even as a "next
  target" section. The "Schema-driven actor architecture (next-
  substrate)" stub at ARCH:194 is the closest, but it describes the old
  schema-driven actor substrate (records ~639-720), not the post-1327
  Principle.
- `persona-spirit` is the deployment target for the engine-trait
  pattern (eventually); the manifestation gap here is the largest
  structural absence in scope.

### `sema` — durable single-writer (storage kernel)

**Recent activity:**

```text
sknnruqy 2026-06-01
wroxwzrq 2026-06-01 ARCHITECTURE: schema evolution discriminant stability rule
wsnpvlrq 2026-05-29 ARCHITECTURE: redb copy-on-write deletion durability
tokpqtwy 2026-05-25
ktlotuxx 2026-05-25 docs: schema-rust composer + emit_schema! proc-macro rename per psyche records 639 + 641
wyvswosu 2026-05-24 schema: add v0.1 concept schema
```

**ARCH state:** Substantive (~268 lines). No INTENT.md — only
ARCHITECTURE.md, AGENTS.md, skills.md.

ARCH documents sema as the storage kernel: `Sema::open_with_schema`,
typed `Table<K,V>`, closure-scoped read/write transactions, schema
version + database-format guards. The §"Versioning — today and
eventually" (lines 222-254) names content-addressed versioning as future
work; today is manual `SchemaVersion`. §"Macro-pattern integration"
(line 256) references designer/326 — outdated; the post-444/447 design
is not absorbed.

§"Deletion durability — copy-on-write page reuse" (lines 134-169)
landed 2026-05-29 — confirms forensic non-recoverability of
removed records. This is fresh and properly named.

**Code state:** No `SemaEngine`/`SignalEngine`/`NexusEngine` — sema is
the kernel below the engine-trait pattern. Engine-trait lives in the
consumer daemon's `Store`, which speaks to sema. Today sema is direct
redb; sema-engine wraps it with verb execution.

**Gaps:**

- **No INTENT.md file.** Per spirit record 944, ARCH+INTENT are the
  canonical agent-context surface; sema has only ARCH.
- Engine-trait absent — defensible for the kernel, but the ARCH should
  at least name how component daemons reach it through the engine-trait
  Store pattern. The §"Boundary" diagram (lines 51-67) shows
  component-daemon → sema-engine → sema; engine-trait language doesn't
  appear in that boundary description.
- §"Macro-pattern integration" references designer/326 — that's the
  pre-444/447 vision. The post-1308-1314 schema-language vision
  (designer 447's content-addressed schema-hash with runtime
  multi-version) is named in §"Versioning eventually" but not connected
  to designer 447.

### `sema-engine` — typed database engine library

**Recent activity:**

```text
xwyvmwno 2026-05-29
uvovkrov 2026-05-29 ARCHITECTURE: Retract destructive once pages reclaimed
ulrqkkyn 2026-05-25
xopkqron 2026-05-25 docs: schema-rust composer + emit_schema! proc-macro rename per psyche records 639 + 641
zorvxlpq 2026-05-24 schema: add v0.1 concept schema
```

**ARCH state:** Substantive (~200+ lines per the read so far). No
INTENT.md.

ARCH documents sema-engine as a typed engine over sema: `Engine` opens
storage through `Sema::open_with_schema`, registers record families,
serves the six closed `SemaOperation` (Assert/Mutate/Retract/Match/
Subscribe/Validate). Notable load-bearing constraints (lines 38-43):
Retract is destructive at the storage layer (added 2026-05-29 per
operator findings).

**Code state:** No `SemaEngine` in src/ — sema-engine has its own
`Engine` type that implements the verb-driven semantics. This is
NOT the schema-emitted `SemaEngine` trait (apply/observe). They are
different `Engine` types: sema-engine's `Engine` is the verb executor;
schema-rust-next's emitted `SemaEngine` is the per-component trait the
daemon Store implements.

**Gaps:**

- **No INTENT.md.**
- Engine-trait pattern not absorbed. The ARCH ends with "consumers"
  (component daemons) implementing higher-level workflows over the
  sema-engine `Engine`, but does not describe the engine-trait
  `SemaEngine::apply`/`observe` surface that sits between component
  schema and sema-engine.
- spirit-next today uses redb directly (`Store::open(path)`) rather
  than going through sema-engine. The "production destination is
  sema-engine" promise (spirit-next ARCH:198-201) is not reflected in
  sema-engine's ARCH as "this is the home for engine-trait `SemaEngine`
  implementations once the multi-component cutover lands."

### `nexus` — text/Signal translator (NAME COLLISION)

**Recent activity:**

```text
srknltsl 2026-05-27
ttlnvotp 2026-05-24 nexus: align text grammar with bracket strings
```

Only two commits in scope window, last 2026-05-24.

**ARCH state:** ~255 lines. No INTENT.md, no skills.md.

**Key finding: `nexus` repo is NOT the engine-trait Nexus.** This repo
is "the workspace's typed semantic text vocabulary over NOTA syntax …
translator daemon. … It does not own a second parser or a second text
syntax." It speaks NOTA text to clients and Signal (rkyv) to
`criome` — pure translator. Its purpose has nothing to do with the
execution-plane Nexus that lives between Signal and SEMA in spirit-next
runtime triad.

The `nexus` repo and the schema-emitted `NexusEngine` share a name but
are different concepts. This is a real name-collision risk.

**Code state:** No engine-trait. Designed for a different purpose.

**Gaps:**

- **No INTENT.md.**
- Name collision with the engine-trait `NexusEngine` is unaddressed.
  The repo predates the engine-trait pattern; if the engine-trait
  pattern propagates further, downstream agents will conflate "Nexus
  the translator" with "Nexus the execution plane in the runtime
  triad." A renaming or a disambiguation note in the repo ARCH would
  reduce conflation.
- §"Scope" notes today's nexus is a realization step toward an
  eventual `Criome`; designer 444/447 do not address this repo at all.

### `upgrade` — runtime leg of the upgrade triad

**Recent activity:**

```text
ypozxllo 2026-05-30
kpkkquym 2026-05-25 upgrade: add orchestrate sandbox migration
yxqwmkzx 2026-05-25
uvvpppnv 2026-05-25 docs: schema-rust composer + emit_schema! proc-macro rename per psyche records 639 + 641
ynprnklk 2026-05-25 upgrade: roll forward ARCH for multi-pass schema reader + supervisor choreography + diff taxonomy
numwlkqs 2026-05-24 upgrade: use Spirit contract projection in migration
```

**ARCH state:** ~73 lines, "scaffold only" (line 51). No INTENT.md.

§"U1 Shape" (lines 22-28): "U1 is intentionally skeletal. The binaries
enforce the component single-argument rule and return typed
`RequestUnimplemented` NOTA output. No `sema-upgrade` migration
modules, no Persona `HandoverDriver`, and no durable database code are
present in U1."

§"Pending schema-engine upgrade" (lines 55-72): references
designer/326 (pre-444/447 vision) and designer/324 — describes the
schema-engine cutover as scheduled, but cites only the OLD vision.

**Code state:** No engine-trait. No `SchemaEdit`/`EditSchema`/
`schema-daemon`/self-edit machinery. The placeholder src/ structure
returns `RequestUnimplemented`.

**Gaps (the F6 gap):**

- **Designer 447's upgrade-as-SEMA + self-editing schema-daemon design
  (Maximum certainty, Spirit 1308-1314) has not manifested into this
  repo's ARCH or INTENT.** The ARCH still references designer/326 +
  designer/324 as the destination.
- The split between "schema-daemon as editor" and "upgrade-daemon as
  testing-pipeline orchestrator" (designer 447's load-bearing
  realization) is not present. Without that split named here, an
  operator picking up upgrade for their first slice would build the
  pre-447 hand-authored handover state instead of consuming the
  derived code from schema-daemon.
- No INTENT.md.
- The schema-daemon repo doesn't exist yet (designer 447 sketches it
  as a sibling of schema-next that ships a daemon binary). The
  upgrade repo can't progress to U2 cleanly without that resolved.

## Engine-trait propagation table

| Repo | ARCH-reflects? | INTENT-reflects? | Code-implements? |
|---|---|---|---|
| `nota-next` | n/a (below the planes) | n/a | n/a |
| `schema-next` | partial (recognises shapes) | partial (Input/Output triggers) | n/a (lowering, not emission) |
| `schema-rust-next` | YES (canonical spec) | YES (canonical spec) | n/a (emits the traits) |
| `schema-core` | no | no | n/a (shared types, not engine) |
| `spirit-next` | YES (full triad worked example) | YES | YES (3/3 traits) |
| `persona-spirit` | NO | NO | NO (kameo actor tree) |
| `sema` | no (kernel below planes) | n/a (no INTENT) | n/a (kernel) |
| `sema-engine` | no | n/a (no INTENT) | n/a (verb-engine, not plane-engine) |
| `nexus` | n/a (different concept) | n/a (no INTENT) | n/a (translator daemon) |
| `upgrade` | no | n/a (no INTENT) | NO (U1 scaffold) |

The pattern propagation is concentrated at the emission end
(schema-rust-next) and one worked-example consumer (spirit-next).
Persona-spirit is the deployment gap; sema/sema-engine/upgrade are
structural gaps; nexus is a name-collision risk.

## schema-core directional question

### Current shape

schema-core today is the **cross-crate import mechanism proof**. Its
sole declared shared noun is `DatabaseMarker` (with `CommitSequence`
and `StateDigest`). Two-member workspace; consumer crate pulls the
declaration via Cargo `links` + `DEP_*` env vars + `ImportResolver`.
Works in Nix because Cargo propagates `DEP_*` independently of build
system.

This proves the mechanism. It does NOT yet ratify a shared-primitives
library.

### Next-decided

Designer 444 (the schema arc stack vision) names the **schema-core
extraction horizon** as the biggest remaining architectural cut. The
target is to lift the ~600 lines of envelope substrate that today is
emitted into every per-component generated `lib.rs`:

- `Signal<Root>` / `Nexus<Root>` / `Sema<Root>` envelope triple
- `pub mod schema::Plane<S,N,M>` cross-plane wrapper
- `MessageIdentifier`, `OriginRoute`, `MessageRoot`, `MessageSent`,
  `NexusMail<Payload>`, `MessageProcessed<Reply>`, hook traits
- `signal` / `nexus` / `sema` plane module re-exports
- Frame primitives (`short_header` constants, `SignalFrameError`,
  `encode_signal_frame`/`decode_signal_frame`)
- `NexusEngine` / `SemaEngine` / `UpgradeFrom` / `AcceptPrevious` trait
  surfaces

Designer 444 §"Companion cut: schema-aware variant projection" adds the
~200-line variant projection (per designer 443 sub-agent 4 Finding 2).

Designer 447 §"What schema-next has today" depends on horizon 1
(schema-core extraction) as a precondition for self-editing —
"schema-core extraction lets the upgrade migration code itself be
shared substrate."

### Next-open

- **Which primitives land first?** Designer 444 names the envelope
  bundle (Signal/Nexus/Sema + mail nouns + frame primitives + engine
  traits). Designer 446 (porting research) likely refines order; not
  inspected here. The current mail.schema has only DatabaseMarker; what
  is the order of the next adds (String, Integer, Magnitude, Time,
  Identifier, envelope types)?
- **How does the emitter recognise "this is a schema-core import" vs
  "this is locally declared"?** Today the import is explicit:
  `schema-core:mail:DatabaseMarker`. When envelope types land in
  schema-core, every component schema will need to import them; the
  question is whether that import is implicit (automatic schema-core
  prelude) or explicit (every component schema names them).
- **schema-core as `links` target requires `Cargo.toml` discipline in
  every dependent.** The current schema-core ARCH §"Iteration-N
  concerns" admits this is unsolved at scale: version resolution is
  single-version happy-path; diamond/transitive conflicts unaddressed.
  A component triad importing from both schema-core and another
  primitives crate will hit this.
- **Designer 447 dependency.** The upgrade-as-SEMA + self-editing
  schema-daemon design lists horizon 1 (schema-core extraction) as a
  precondition. If schema-core extraction is gated on the envelope
  bundle landing, designer 447 cannot start. The question of whether
  to land schema-core extraction one piece at a time (start with
  `MessageIdentifier`/`OriginRoute`) vs. as a single ~600-line cut
  affects designer 447's start date.

The mechanism is proven; the contents are open. The directional
question is **which shared noun lands second** and on **what
sequencing rule**.

## Cross-cutting findings

### F1 — engine-trait pattern is documented in ONE PLACE and implemented in ONE PLACE

The pattern is fully specified in `schema-rust-next` ARCH+INTENT
(lines 106-115 / 66-86) and fully implemented in `spirit-next`
(src/engine.rs:194, src/nexus.rs:62, src/store.rs:40). Every other
consumer repo (persona-spirit, sema-engine, upgrade) is silent on
engine-trait.

This is the textbook "canonical worked example, no propagation" shape.
The Principle (Spirit 1327) is workspace-wide but its manifestation is
local to the proof crate.

### F2 — INTENT.md is missing in 4 of 10 scoped repos

`schema-core` has INTENT; `sema`, `sema-engine`, `nexus`, `upgrade` do
not. Per spirit record 944 (Maximum, 2026-05-27), per-repo
`INTENT.md` + `ARCHITECTURE.md` are the canonical agent-context
surfaces and must be UPDATED as relevant intent lands. The four-repo
gap is a structural compliance gap.

### F3 — Designer 447 (F6) has not manifested anywhere

Designer 447 (upgrade-as-SEMA + self-editing schema-daemon, Maximum
certainty, Spirit 1308-1314) lives entirely in the report
`reports/designer/447-upgrade-as-sema-design-2026-06-01.md`. No
manifestation in:

- `/git/github.com/LiGoldragon/upgrade/ARCHITECTURE.md` (still cites
  designer/326)
- `/git/github.com/LiGoldragon/schema-next/INTENT.md` (no `MigrationEmitter`,
  no `SchemaSemaEngine`)
- `/git/github.com/LiGoldragon/schema-core/` (no envelope substrate
  added)
- No `schema-daemon` repo created

Per the report's own §"the operator-bead-shaped first action," a first
operator slice was named. No trace of that slice in any repo's recent
log. F6 is fully report-only.

### F4 — persona-spirit is the deployment gap

persona-spirit is the deployed Spirit (0.3.0); spirit-next is the
canonical engine-trait worked example. Architecturally, the spirit-next
pattern needs to migrate INTO persona-spirit at some point —
the deployment will eventually pick up the engine-trait model. But
persona-spirit's ARCH/INTENT have zero references to engine-trait,
spirit records 1308-1339, or the §"Schema-driven actor architecture
(next-substrate)" remains pinned to the OLD designer/326 vision.

The cutover plan is not described.

### F5 — Repo naming risks: `nexus` repo vs. engine-trait Nexus

`nexus` repo is the text↔Signal translator daemon (text vocabulary →
criome). The engine-trait `NexusEngine` is the execution-IO plane
between Signal and SEMA in the runtime triad. They are different
concepts that share a name. If the engine-trait pattern propagates
into more daemons, this collision will produce confusion in cross-repo
discussion.

### F6 — schema-core's mechanism is proven but content is empty

schema-core ratifies the mechanism (cross-crate import via Cargo
`links` + `DEP_*` + `ImportResolver`) on a single trivial type
(`DatabaseMarker`). The content side — what types live there — is
empty. Designer 444 names the ~600-line envelope substrate as the
content destination; designer 447 names this as a precondition;
neither has produced a slice of work.

### F7 — Engine traits emitted but envelope substrate per-component

The engine traits (`SignalEngine`/`NexusEngine`/`SemaEngine`) and the
envelope substrate (`Signal<Root>`/`Nexus<Root>`/`Sema<Root>`,
`MessageIdentifier`, `OriginRoute`, mail nouns) are emitted today as
~600 lines into each component's generated `lib.rs`. The next
multi-component triad (e.g., a `persona-introspect`) would emit
identical envelope into itself. Per designer 444 §"What this unblocks"
this is the headline cost of the not-yet-completed schema-core
extraction.

### F8 — sema vs. sema-engine vs. schema-rust-next's emitted `SemaEngine`

Three things share the "engine" name and operate at different layers:

- `sema-engine` crate's `Engine` type — the verb executor for the six
  closed `SemaOperation`s (Assert/Mutate/Retract/Match/Subscribe/
  Validate). Database-level.
- `schema-rust-next` emitted `SemaEngine` trait — the per-component
  database trait (apply + observe). Schema-level.
- spirit-next's `Store` — the data-bearing object that implements
  schema-rust-next's `SemaEngine` trait. Component-level.

Today spirit-next's `Store` uses redb directly, not sema-engine's
`Engine`. The "production destination is sema-engine" promise from
spirit-next ARCH:198-201 means: spirit-next's `Store` will eventually
implement `SemaEngine` BY delegating to sema-engine's `Engine` instead
of speaking redb directly. This delegation is the unmade slice; not in
sema-engine's ARCH; not in spirit-next's worktrees.

## Recommendations

Small concrete next moves, named.

### R1 — Add INTENT.md to sema, sema-engine, upgrade, nexus

Per spirit record 944. The four-file gap is the simplest structural
fix. Each INTENT.md sources the repo's purpose from the relevant
designer reports / spirit records and lists load-bearing constraints.
~50-150 lines per file. Designer lane work; one designer subagent could
draft all four. Use spirit-next's INTENT.md as the template — it is
the most recently formed INTENT.md in the schema-arc stack.

### R2 — Update upgrade/ARCHITECTURE.md to reflect designer 447

Replace §"Pending schema-engine upgrade" (lines 55-72) — which cites
designer/326 — with the post-1308-1314 vision: upgrade-as-SEMA on
Asschema, schema-daemon as the editor (Spirit 1309), upgrade-daemon as
the testing-pipeline orchestrator, transitory-database pattern (Spirit
1310). Mark U2 as gated on schema-daemon existing (or U2 as the
schema-daemon implementation, depending on the sequencing decision).
~60-100 lines of edit. Designer 447 already has the exact text shape;
this is a direct port.

### R3 — Decide and document the schema-core sequencing rule

What lands next in schema-core, in what order? The directional
question §"Next-open" has three open sub-questions:

- envelope bundle as one cut vs. one noun at a time
- implicit prelude vs. explicit per-schema imports
- multi-version Cargo resolution policy

A short designer report (or a §"Sequencing" addition to schema-core
ARCH) answering these unblocks the F6 design start. Designer lane
work; ~3-5 days; one designer.

### R4 — Add §"Engine-trait pattern (next-substrate)" to persona-spirit ARCH

Even before code migration, persona-spirit's ARCH should name where it
will land. A short section (~30-50 lines) explaining:

- the current Kameo-actor tree is the live deployment
- the engine-trait pattern (cite Spirit 1327, 1339; cite
  spirit-next as canonical worked example) is the migration target
- the migration is gated on (X, Y, Z) — probably schema-core extraction
  + multi-component proof in a second component first
- the cutover sequence is (M, N, O)

Without this, persona-spirit looks like an architecturally-stable
deployment when in fact it is on the pre-engine-trait substrate. The
absence is the textbook "deployment lags vision" gap and should be
named in the repo itself.

### R5 — Disambiguate `nexus` repo vs. engine-trait `NexusEngine`

A short note in `/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md`
disambiguating the name collision. Or — bolder — propose renaming the
text-translator daemon (it predates the engine-trait pattern but the
pattern is more architecturally load-bearing). The §"Scope" already
notes today's nexus is a "realization step" toward Criome; that's the
natural place to add the disambiguation.

### R6 — Spell out the spirit-next → sema-engine cutover

spirit-next ARCH:198-201 promises the eventual destination is
sema-engine. sema-engine ARCH doesn't reflect this. One section in
sema-engine ARCH naming "schema-emitted `SemaEngine` trait
implementations delegate here" would close the loop. Then a designer
or operator can plan the spirit-next `Store` delegation slice with
both ends of the boundary documented.

### R7 — Pull schema-core envelope substrate slice

A small operator slice: move `MessageIdentifier` + `OriginRoute` from
spirit-next's per-component generated `lib.rs` to schema-core's
shared crate. This is the smallest meaningful step toward F6 — proves
the envelope-substrate extraction works without trying to land all
~600 lines at once. Designer 444 named this as horizon 1; designer
447 named it as precondition. Operator-claimable slice; a few
~300-500 line patches.

The seven recommendations are roughly orderable: R1 (cheap structural
compliance) → R3+R4 (design decisions) → R2 (port designer 447) → R7
(first operator slice on the design once decided) → R5+R6
(disambiguations and cross-repo edits).
