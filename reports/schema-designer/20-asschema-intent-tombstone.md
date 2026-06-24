# 20 — Asschema-era intent-log cleanup: tombstone + execution log

*schema-designer · report 20 · the tombstone appendix and execution record for the
Asschema-era Spirit cleanup recommended in report 19 and authorized by the psyche
("Full cleanup"). Captures each record's full pre-edit text before any mutation
(`skills/intent-maintenance.md` — capture before you remove), then logs the
operation applied and the daemon receipt.*

## Spirit gate

The psyche explicitly authorized this cleanup, selecting **Full cleanup** when
asked how far to bring the Asschema-era records into the SpecifiedSchema era. That
selection is the supersession authority (only the psyche supersedes prior psyche
intent); the underlying design authority is `6cfr` / `6grf` / `ng1x`. No *new*
intent is recorded — this is maintenance: `Retire`, `Clarify`, `ChangeRecord`.

## Refinement of report 19's A/B split (more preservation, not less)

On reading each record's full text, two records first slotted for retirement carry
surviving rules worth keeping, so they move to `Clarify`; one record's description
is already current, so it needs only a referent fix:

- **`hc0t` → Clarify** (was: retire). Its codec-floor constraint — *all schema NOTA
  output comes from the typed codec; a printed type label is a real decodable
  shape, never hand-rolled* — survives; only the `.asschema` artifact framing is
  dead.
- **`h053` → Clarify** (was: retire/fold). Its principle — *one typed noun per
  semantic object across the schema/NOTA stack* — is the conceptual root of `6grf`
  and worth keeping in its own words.
- **`mcuk` → ChangeRecord** (referent-only). Its description (header-first `.schema`,
  positional input/output) is current and correct; only the stale `asschema`
  referent is dropped.

Final disposition: **Retire 4** (`n9ta`, `av1q`, `sfwv`, `yuku`), **Clarify 8**
(`hc0t`, `h053`, `bkcd`, `b2jg`, `t5wx`, `oxgh`, `xbu8`, `py4h`), **ChangeRecord 1**
(`mcuk`).

## Tombstone — full pre-edit text (verbatim from `spirit "(Lookup …)"`)

**Retired (4):**

- `n9ta` (Decision High/High, `[asschema nota rkyv schema-emitter]`) — [|The
  assembled schema is a live serializable artifact — NotaDecode, NotaEncode, and
  rkyv on Asschema and all substructure — with the in-memory typed Rust value as
  bootstrap only; the Rust emitter consumes the serialized assembled form (checked-in
  or build-time-emitted .asschema NOTA files), not the in-memory value directly.|]
- `av1q` (Decision High/Medium, `[asschema assembled-schema nota schema-macro]`) —
  [|Define assembled schema (.asschema) before sugar: it is macro-free final data —
  Vec, Optional, Enum, Struct, Newtype, Plain, Carries are final assembled-schema
  variants, not macro invocations. Sugar belongs only in authored schema before
  lowering. Schema macros re-emit schema structure toward AssembledSchema
  (conceptually re-emitting NOTA, intermediate may stay binary) and must expand into
  a fully one-to-one assembled tree describing all generated types, endpoint variant
  names, and carried input structs before Rust is emitted. Application is iterative
  to a fixed point: each pass applies lowerers at macro positions, macros may
  introduce new macros, until the namespace is pure typed enums, structs, newtypes.|]
- `sfwv` (Clarification Medium/Minimum, `[asschema nota schema]`) — [|The resolved
  assembled-schema artifact is the Asschema (.asschema) file: pure NOTA holding fully
  resolved enum and struct definitions with no remaining macros, read against the
  known Asschema root struct positionally with no outer wrapper. Human-readable debug
  output is not .asschema and must be named as a witness.|]
- `yuku` (Principle Medium/Minimum, `[asschema nota rkyv sema]`) — [When reconciling
  the asschema roundtrip design, prefer simple canonical NOTA syntax and separated
  typed-object responsibilities: Asschema owns assembled schema data, AsschemaArtifact
  owns NOTA and rkyv artifact projection, a SEMA store owns durable rkyv persistence,
  and Rust emission consumes the typed Asschema object rather than parsing side syntax.]

**Clarified (8) — pre-edit text:**

- `hc0t` (Constraint VeryHigh/Medium, `[asschema nota rkyv assembled-schema typed-codec]`) —
  [|The assembled schema (.asschema) is canonical NOTA-and-rkyv only, round-tripped
  through AsschemaNotaWriter/Reader. All NOTA output comes from the typed codec — a
  printed type label is a real decodable shape, never hand-rolled witness/line formats
  or ad hoc field joins; a known-root file is its root body encoded through an
  object/body abstraction over ordered fields.|]
- `h053` (Decision High/Medium, `[asschema schema-macro nota rkyv sema schema-source]`) —
  [|One typed noun per semantic object across the schema/NOTA stack: source text and
  checked-in/serialized artifact share the same datatype unless there's a real
  semantic projection. Assembled schema is one typed Asschema object projected to
  rkyv bytes (SEMA db), binary archive, and .asschema NOTA text via the same
  Nota-derived types; a SchemaMacro source entry fits one serializable enum variant,
  not split source/data enums. Schema source itself is a typed value with a dedicated
  in/out codec reading strict NOTA source into source-node data and writing it back
  canonically, distinct from raw NOTA parsing and from assembled serialization.|]
- `bkcd` (Decision High/VeryHigh, `[rkyv nota notadecode notaencode asschema schema-rust-next daemon cli]`) —
  [|rkyv is the universal wire base for the schema-derived stack; the NOTA codec
  (NotaDecode/NotaEncode + derive) is opt-in per consumer. DOUBLE clients (text+binary,
  e.g. CLI) carry the NOTA derive; binary-only clients (daemon) omit it for leanness
  and to structurally reject NOTA text at the wire. Same data types across consumers —
  only the derive set differs; byte-compatibility comes from the identical shared rkyv
  layout. Schema-emitted types derive both NOTA and rkyv from one .asschema, with
  extra communication traits on roots that cross component boundaries, reusing the same
  NOTA typed interfaces as direct Rust rather than a parallel mini-codec.|]
- `b2jg` (Constraint High/High, `[nota-next schema sema spirit-next asschema]`) — [Tests
  across the nota/schema/sema stack load real separate .nota/.schema/.sema files via a
  small shared read-fixture helper, never inline source strings. Every .schema fixture
  is NOTA-legal, parsable by nota-next before lowering, and uses local relative imports.
  Real file-based tests prove each step: structural parse, the shared nota-next codec,
  schema-of-schemas read, macro assembly into macro-free Asschema data, the roots model,
  Rust datatype/derive emission over the shared codec, and the actor system running full
  constraints on spirit-next.]
- `t5wx` (Decision High/Medium, `[schema-next schema-rust-next nota-next spirit signal-spirit meta-signal-spirit triad-runtime rkyv]`) —
  [|schema-codegen capability set is closed (…). Next phase is integration/migration …
  Pipeline: each plane defined in schema, **assembled into Asschema**, emitted as Rust
  datatypes plus basic trait impls … the schema/NOTA compiler (nota-next, schema-next,
  schema-rust-next) is build-time-only, never linked into runtime, and the NOTA text
  codec is an optional edge feature absent from the daemon.|] (full text in git / Lookup)
- `oxgh` (Decision High/Medium, `[assembled-schema struct type-declaration field-name rust]`) —
  [|**In the assembled schema** a struct is a key-value brace map: field name is the key,
  type reference is the value … a field's identity IS its type name … Type declarations
  are visibility-tagged Public(name,value) or Private(name,value) … An inline PascalCase
  type in a field is sugar …|] (full text in git / Lookup)
- `xbu8` (Decision Medium/Medium, `[schema-daemon asschema schema-component macro nota]`) —
  [|The schema component is self-editing: the schema daemon IS the editor of **its
  Asschema** … three faces from one NOTA source: runtime daemon …, library crate …,
  macro substrate …|] (full text in git / Lookup)
- `py4h` (Decision Medium/Medium, `[sema asschema upgrade-operations schema-diff typed-operations]`) —
  [|Upgrade mechanisms are live typed SEMA operations **on the Asschema**: a protocol or
  database-format change is a typed operation/message … Diff operations have three
  families: Add, Remove, Modify (Modify subdivides into ContainerEmbed, EnumWrap, Reorder,
  KeyChange).|]

**ChangeRecord (1) — referent fix only:**

- `mcuk` (Correction Medium/Low) — description unchanged (header-first `.schema`,
  positional input/output, both current); referents `[schema nota asschema input output]`
  → `[schema nota input output]`.

## Execution log

Receipts appended after each operation runs.
