# 573 — schema-grammar implementation: progress + corrections to 571

designer, 2026-06-09. Implementation of the four schema-grammar decisions
(`52ro`/`yp29`/`qz6j`/`lm84`) from handover `571`. This records what landed, the
places reality corrected `571`'s assumptions, the binding cross-repo constraint
that reshapes the rest, and the decisions now in front of the psyche. Companion
to `571` (the plan) and `570` (the review).

## What landed — now on `main` (psyche: "main is where this work belongs")

schema-next `main` = **`cf4cfb9f`** (grammar complete) and schema-rust-next `main`
= **`44e472bf`** (Step 2), both pushed. The earlier feature-branch isolation was
dropped — the "can't build the emitter until grammar reaches main" framing was an
artifact of that isolation, not a real blocker; main is the home.

| Step | Record | Commit (on `main`) | State |
|---|---|---|---|
| dead-code | — | `f301636a` | dead `syntax.rs` removed |
| 1 | `52ro` | `376b847a` | `(X)` self-tag form, both paths, test |
| 3a | `yp29` | `3e76cf9c` | `Bytes` reserved scalar (grammar half) |
| 5 | `qz6j` | `cf4cfb9f` | aliases dropped entirely; bare form is always a distinct newtype |
| 2 | newtype priv-field | `44e472bf` (schema-rust-next) | schema newtypes get a private field |

Each step is its own commit; each verified green (`build` + `test` + `clippy`).
schema-next: 107 tests pass. schema-rust-next at Step 2: 66 pass. The
**schema-next grammar side is complete and on main.** One remaining pass — the
**schema-rust-next emitter integration** against the new schema-next — is below;
it has a real semantic subtlety (`From`-impl emission) so it gets a careful pass
rather than a rushed one.

## `qz6j` resolved harder than scoped — the psyche dropped aliases entirely

The handover proposed scoping `qz6j` to scalar-refs only (declared-type re-tags
stay transparent aliases). The psyche overrode: **"we don't use alias — they're
useless and offer no correctness."** So `TypeDeclaration::Alias` + `AliasDeclaration`
are **removed**, and *every* bare `Name Type` (scalar, declared-type, collection)
lowers to a distinct `NewtypeDeclaration`. `Recipient String` → newtype (the win);
`State Statement` → distinct `State(Statement)`, no longer interchangeable with
`Statement` (the intended correctness, at the cost of the ~5 live re-tag sites,
which break at integration — fine pre-production). Reinforces Spirit record
`qz6j`.

## `52ro` — what was actually needed (557's fear was overstated)

The handover warned the `Data` variant captures payload with `PatternElement::any`
and would shadow `(X {…})`. **False.** `Data` is `#[shape(pascal_head, arity=2)]`
→ `pascal_headed_parenthesis(Exact(2), …)`; arities discriminate by parenthesis
root-object count (`(X)`=1, `(X Y)`=2, `(X Y kw Z)`=4), mutually exclusive. And
the inline-body forms `(X {…})` / `(X […])` **already lowered** via the existing
`Data` + `SourceVariantPayload::Declaration` + hoisting path. So the only new
form was the arity-1 `(X)` self-tag:

- schema-next live path: new `SourceVariantSignature::SelfTagged` variant
  (`#[shape(pascal_head, arity=1)]`), lowering to a variant whose payload is
  `TypeReference::from_name(name)` **unconditionally** (`source.rs to_enum_variant`).
- registry path: `MacroExpansionVariant::lower_parenthesis` arity-1 case, so the
  two lowerings agree on the new form.

**`primary-vllc` correction.** I earlier said `52ro` closes the dual-lowering
bare-header bug. It does **not**. `vllc` is about *bare* `X` (no parens), whose
payload is context-sensitive on the SchemaSource path (`resolves_variant_payload`)
but dropped to `None` on the registry path. That is a separate resolver-semantics
unification (records 1572/1578, operator-owned). `52ro` only guarantees the two
paths agree on the **new `(X)`** form. I did not fold `vllc` in — it needs the
"unify on SchemaSource" decision, not a variant addition.

## Step 2 — the handover conflated two newtype categories

There are **two** newtype-emission paths in schema-rust-next:

1. **`RustNewtypeTokens` (lib.rs:3105)** — schema-declared newtypes (e.g.
   `Summary`). Emits `new`/`payload`/`into_payload`/`From`. **This** is what
   `qz6j` mass-produces, and what `571` Issue B targeted. Fixed: private field.
   Zero in-repo construction sites broke (these are built via `::new`/`From`).
2. **`RuntimeCopyNewtypeTokens` (lib.rs:2534)** — runtime mail-surface identity
   wrappers (`MessageIdentifier`, `OriginRoute`). Emits `pub struct N(pub Integer)`
   with **no accessors**; constructed pervasively as `OriginRoute(900)` and read
   via `.0` in the generated runtime + tests. **Left untouched** — privatizing
   these is a distinct change (needs accessor emission + runtime-template +
   consumer fixes) and is not what `qz6j` produces.

So the "fleet-forcing, 17 sites break" worry was a category confusion: those 17
sites are runtime newtypes (still `pub`, unaffected). The schema-newtype
privatization is **low-risk**. **Open flag:** the runtime identity newtypes also
violate the private-field discipline; whether to privatize them is its own
decision (see below).

## The binding constraint: schema-rust-next depends on schema-next via `git, branch="main"`

`schema-rust-next/Cargo.toml:19` →
`schema-next = { git = …, branch = "main" }`. So **schema-next branch changes are
invisible to the emitter until they reach schema-next `main`** (operator
integration). Consequences:

- The **emitter halves** of `yp29` (Bytes hex-codec newtype) and `lm84` (hash-id)
  cannot compile or be tested until the grammar halves land on schema-next main —
  their code references `TypeReference::Bytes`, which main doesn't have yet.
- So Steps 3b/4 are **integration-gated by construction**, not by choice. This is
  the natural cross-repo ordering: grammar → main → emitter.
- What I *can* author + verify in isolation is the schema-next **grammar** side
  (Bytes grammar ✓; `qz6j` lowering — pending the decision below) and the
  emitter-internal Step 2 (✓, no schema-next dependency).

## `qz6j` census correction — far smaller than `570`/`571` claimed

The review's ~1068 aliases / ~306 scalar / ~762 declared-type split counted
`.concept.schema` stubs that **do not exist** in live contracts. Live building
contracts hold **~55 bare `Name Type` declarations, ~50 reserved-scalar (the
wins), ~5 declared-type (stay transparent)**. The scoping check is a clean
`reference.scalar_name().is_some()` at lowering. So `qz6j`'s live blast radius is
~50 newtype conversions, not ~1000.

## Step 3b — Bytes emitter codec (spec for integration)

When schema-next's Bytes reaches main, schema-rust-next emits `Bytes` as a
**newtype-scalar with its own hex codec**, NOT `type Bytes = Vec<u8>` (the blanket
`Vec` codec renders `[1 2 3 …]` — the exact wart). Template:
`signal-version-handover/src/lib.rs:149` `RawPayload(Vec<u8>)` with hand-written
`NotaDecode`/`NotaEncode` (orphan-safe — emitted in the generated module).
Surface form: lowercase-hex inside a bracket string (`[deadbeef]`), per the
bracket-form NOTA discipline; exact-roundtrip, case/width fixed so dedup/equality
stay on the bytes. Sites: `default_aliases` must special-case Bytes (not a plain
alias); `to_tokens`, `references_private_type`, `collect_map_keys`, `rust_type`
gain Bytes arms. Then migrate the 4 `(Vec Integer)`-as-bytes sites
(`meta-signal-upgrade`, `signal-terminal` ×3) and criome's `{ value String }`
binary fields (`BlsPublicKey`/`BlsSignature`/`ObjectDigest`/`PublicKeyFingerprint`).

## Decisions — resolved + still open

- **RESOLVED — `qz6j` alias fate:** drop aliases entirely (psyche). Done on the
  branch (`cf4cfb9f`).
- **DECIDED — runtime identity newtypes** (`MessageIdentifier`/`OriginRoute`):
  the psyche said **privatize**. So the emitter pass also emits `new`/`payload`
  accessors for the `RuntimeCopyNewtypeTokens` types (lib.rs:2534) with a private
  field, and rewrites every generated/test construction (`OriginRoute(900)` →
  `::new(900)`) and `.0` read (`→ payload()`). Not yet actioned (part of the
  emitter pass below).

## The emitter integration pass — DONE, on schema-rust-next main `a2591391`

Completed this session: schema-rust-next now builds against the no-alias
schema-next (`cf4cfb9f`), **66 tests pass, clippy clean**. The work was much
deeper than "remove aliases" — `qz6j` "drop ALL aliases" ripples widely:

- **Alias machinery removed** (RustAlias/RustAliasTokens/the lowering + map-key +
  nota-bridge arms).
- **`From`-impl emission simplified** — former-alias variant payloads are now
  distinct newtypes, so the alias-exclusion in
  `unique_non_alias_plain_payload_variants` is obsolete (`From<X>` is always
  unambiguous). Removed the `alias_names` threading.
- **Alias resolution removed** (`declaration_alias_target`,
  `type_name_matches_plain_or_alias`, the alias tail of
  `local_runtime_role_type_exists`): a newtype is its own canonical type.
- **`Bytes` recognized** in all 5 `TypeReference` match sites.
- **Triad runner schema convention migrated.** This was the big finding: the
  `(X X)` self-tag + `X Synonym` bare-ref pattern (e.g. `(Continue Continue)` +
  `Continue NexusWork`) relied on aliases being *transparent* — the runner detected
  "Continue carries NexusWork" through the alias. Post-qz6j those are distinct
  newtypes, breaking the runner shape detection AND the role-trait/adapter
  emission. Fix = the **direct form** (`(Continue NexusWork)`, `(CommandSemaWrite
  SemaWriteInput)`, …); `plane-triad` and `driver nexus` already used it. Migrated
  `runner-triad.schema`.
- **All test construction/access migrated** to the newtype API (`Topics::new`,
  `.payload()`, `RecordSet::new`, …) + fixtures regenerated.
- **nota-next pinned back to `ae5c25cd`** — the lock bump also moved nota-next to
  `d8862b61`, which changes string encoding (`[[x]]`→`[x]`, simple atoms bare).
  That's a *separate* migration; pinning keeps this change cleanly qz6j+Bytes.
  One-field tuple newtypes encode **transparently** (`to_nota(&self.0)`), so the
  wire is preserved — `qz6j` is type-distinct, wire-transparent.

### Follow-ups — DONE this session (schema-rust-next main)

1. **Privatize the runtime identity newtypes** — `7db6df1e`. `MessageIdentifier`/
   `OriginRoute` now emit a private field + `new`/`payload` accessors; every
   construction/`.0` site migrated. Every emitted newtype (schema + runtime) now
   has a private field.
2. **Bytes newtype-prelude + hex codec** — `f6f1f653`. When a schema references
   `Bytes` (`CollectionScan::references_bytes`, precomputed → no bloat otherwise),
   the renderer emits `struct Bytes(Vec<u8>)` + accessors + a feature-gated
   lowercase-hex codec that delegates the hex String to `String`'s
   `NotaEncode`/`NotaDecode` (a literal `[hex]` parses as a list — delegation
   avoids that). Verified by a `digest Bytes` round-trip.
3. **`lm84` hash-id** — `9f509205`. A hash-id is a **newtype over Bytes** (the
   marker-on-newtype form): `Digest Bytes` → `struct Digest(Bytes)`, transparently
   hex-encoded. Round-trip verified.

### Fixed-size `(Bytes N)` — DONE (cross-repo)

- schema-next `main` `c8ebb399`: `(Bytes N)` → `TypeReference::FixedBytes(N)` — the
  grammar's first numeric type-argument, parsed in all three reference paths.
- schema-rust-next `main` `eca40280`: emits `(Bytes N)` → `FixedBytes<N>` plus a
  generic `pub struct FixedBytes<const WIDTH: usize>([u8; WIDTH])` prelude
  (conditional) with a feature-gated lowercase-hex codec + a WIDTH×2 length check.
  One generic type serves every width (the orphan rule blocks a codec on a bare
  `[u8; N]`). rkyv const-generics work. A named hash-id `Fingerprint (Bytes 4)` →
  `Fingerprint(FixedBytes<4>)` round-trips; verified by the collections test.

### Remaining

- **Fleet consumer migration** — the bulk. On lock-bump, every former-alias access
  across the ~23 consumer crates needs the newtype API, and any triad runner
  schema using the `(X X)`+synonym pattern needs the direct form. This is the
  qz6j fleet-forcing sweep, scoped one component at a time.

The pass, in order:

1. **`cargo update -p schema-next`** (bumps to `cf4cfb9f`).
2. **Remove the qz6j `Alias` machinery** (dead once the variant is gone):
   `AliasDeclaration` import; `RustTypeDeclaration::Alias` variant (lib.rs:779);
   `lower_to_rust` arm (788); `RustAlias` struct+impl+`LowerToRust` (804-827);
   `RustAliasTokens` (3053-3083) + its dispatch arm (3033); `map_key` arm (3329) +
   `collect_alias_map_keys` (3349); the two `RustTypeDeclaration::Alias` arms at
   3781 and 3934. **KEEP** `RustScalarAlias` (the `pub type Integer = u64` prelude)
   and `PlaneNamespaceAlias` (`pub use` re-exports) — different mechanisms.
   - **THE SUBTLETY — `From`-impl emission.** `emit_enum_payload_from_impls`
     (3758) calls `alias_names` (3774, the qz6j-alias collector) → passes it to
     `unique_non_alias_plain_payload_variants` to *skip* `From<Payload>` for
     variants whose payload was a transparent alias (avoided `From<u64>` conflicts).
     With aliases gone (now distinct newtypes), that skip is obsolete and the param
     is always empty — former-alias payloads *should* now get `From` impls
     (distinct types, unambiguous). Verify no two variants share a newtype payload
     (that would make `From<X>` ambiguous) before deleting the filter; this is the
     fleet-wide-correctness-sensitive part, hence the careful pass.
3. **`yp29` Bytes emission** — the 5 match arms emit `Bytes`; plus a prelude
   `pub struct Bytes(Vec<u8>)` + accessors + hand-written lowercase-hex
   `NotaEncode`/`NotaDecode` (bracket form `[deadbeef]`; template
   `signal-version-handover/src/lib.rs:149` `RawPayload`, but bracket not `#`).
   Inject after the scalar-alias loop (render@274). NOT a transparent
   `type Bytes = Vec<u8>`.
4. **Privatize runtime identity newtypes** (psyche-approved) — `new`/`payload` on
   `RuntimeCopyNewtypeTokens`, fix all construction/`.0` sites + fixtures.
5. **`lm84` hash-id** — marker-on-bytes-newtype (confirm marker-vs-primitive);
   pilot criome `ObjectDigest`/`PublicKeyFingerprint`.
6. Regenerate fixtures (`SCHEMA_RUST_NEXT_UPDATE_FIXTURES=1` etc.), `cargo test`,
   `clippy`, land on schema-rust-next main.

**Fleet consumer migrations** (after the emitter lands, as each consumer bumps its
lock): the ~5 declared-type re-tag consumers (`State`/`Statement`-style) need
explicit conversions; criome's `{ value String }` binary fields → `Bytes`; the 4
`(Vec Integer)`-as-bytes sites → `Bytes`; criome `(Authorization… Authorization…)`
→ `(Authorization…)`; `signal-agent` `(RequestUnimplemented RequestUnimplemented)`
→ `(…)` (manual, hand-written contract).

## Pointers

- Plan: `571`. Review: `570`. The four records: `52ro` `yp29` `qz6j` `lm84`.
- Branches: schema-next `schema-grammar-spec` (`3e76cf9c`); schema-rust-next
  `schema-grammar-emitter` (`44e472bf`). Neither repo's `main` advanced.
- The other active thread to resume after the grammar (per the psyche): the
  gated-Spirit guardian + agent component — handover `572`.
