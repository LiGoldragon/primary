# 573 — schema-grammar implementation: progress + corrections to 571

designer, 2026-06-09. Implementation of the four schema-grammar decisions
(`52ro`/`yp29`/`qz6j`/`lm84`) from handover `571`. This records what landed, the
places reality corrected `571`'s assumptions, the binding cross-repo constraint
that reshapes the rest, and the decisions now in front of the psyche. Companion
to `571` (the plan) and `570` (the review).

## What landed (all on feature branches; neither repo's `main` touched)

| Step | Record | Where | Commit | State |
|---|---|---|---|---|
| dead-code | — | schema-next `schema-grammar-spec` | `f301636a` | dead `syntax.rs` removed |
| 1 | `52ro` | schema-next `schema-grammar-spec` | `376b847a` | `(X)` self-tag form, both paths, test |
| 2 | newtype priv-field | schema-rust-next `schema-grammar-emitter` | `44e472bf` | schema newtypes get a private field |
| 3a | `yp29` | schema-next `schema-grammar-spec` | `3e76cf9c` | `Bytes` reserved scalar (grammar half) |

Each step is its own commit; each was verified green (`cargo build` + `cargo
test` + `cargo clippy`). schema-next: 106 tests pass. schema-rust-next: 66 pass.

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

## Decisions in front of the psyche

1. **`qz6j` alias fate.** Scalar bare-refs → newtype (the wins). For the ~5
   declared-type bare-refs (`State Statement` re-tags): keep them as **implicit
   `Alias`** (recommended — simplest, nothing else changes), OR require an explicit
   `(Alias X)` reserved head so aliasing is opt-in and the bare form is
   *always* a newtype. This changes the lowering shape, so it gates authoring.
2. **Runtime identity newtypes** (`MessageIdentifier`/`OriginRoute`): privatize to
   match the discipline (needs accessor emission + fixing every runtime
   construction/`.0` site), or leave them as `pub` Copy conveniences (a conscious
   exception for runtime-minted integer identities).
3. **Integration sequencing.** The grammar branch (schema-next) must land on main
   before the emitter halves (Bytes/hash-id) can be built — operator integration,
   and `qz6j`'s main-landing IS the fleet sweep the handover gates. Confirm the
   go-ahead to author `qz6j` lowering on the branch now (verifiable in isolation),
   held for that gated integration.

## Pointers

- Plan: `571`. Review: `570`. The four records: `52ro` `yp29` `qz6j` `lm84`.
- Branches: schema-next `schema-grammar-spec` (`3e76cf9c`); schema-rust-next
  `schema-grammar-emitter` (`44e472bf`). Neither repo's `main` advanced.
- The other active thread to resume after the grammar (per the psyche): the
  gated-Spirit guardian + agent component — handover `572`.
