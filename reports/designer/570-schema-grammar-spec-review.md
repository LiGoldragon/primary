# 570 — schema-next grammar spec: grounded review + build plan

designer, 2026-06-09. A four-lens grounded review (workflow `w0mqhlnwn`:
grammar-fit, emitter/codec, migration/blast-radius, completeness) of the schema
grammar improvements captured this session — `52ro` (compact variant forms),
`yp29` (`Bytes` primitive), `qz6j` (bare `Name Type` → newtype), `lm84`
(hash-identifier type). Every file:line was re-grounded against the live
`schema-next` / `schema-rust-next` code; where reviewers disagreed the
synthesizer re-ran the check and reports the resolved number. The review
corrected three of its own overstatements (below), which is the behaviour the
last review (567's six-lens pass) lacked.

## Verdict

**The four-part spec is sound, coherent, and implementable — a real improvement
on real warts, not a speculative redesign.** Its strength is internal coherence:
`qz6j` (bare-form newtype) is the keystone that gives `yp29` (Bytes) and `lm84`
(hash-id) a noun to attach a width and a codec to. Three of the four are additive
and low-risk. The one real danger is `qz6j` **as literally worded** ("flip the
bare form to newtype"): a blunt flip silently rewrites ~1068 alias declarations,
of which only ~306 are the intended typed-value wins — the other ~762 are
request-tag re-exports (`State Statement`, `RecordAccepted SemaReceipt`) that
genuinely want to stay transparent, and wrapping them breaks value-flow across
the fleet at once. Fix two grounding errors — the dead `syntax.rs` anchor and the
unscoped flip — and it ships.

## Per-decision

- **`52ro` (compact variant forms) — SOUND, smallest blast radius, ship FIRST.**
  All three forms add without inventing grammar. `(Tag)` → `(Tag Tag)` is a new
  `Exact(1)` parenthesised case, unambiguous (nothing else uses arity-1 in variant
  position). `(Name {…})` / `(Name […])` collide in *arity* with the existing
  2-element `(Tag Type)` variant — they disambiguate by the second element's
  delimiter, exactly as `declarative.rs:1745` already does at field position.
  Correction the records must absorb: this is **three coordinated edit sites**
  (`source.rs:1002` derive, `declarative.rs:1848`, `macros.rs:432`), not the one
  `macros.rs` line the record names; and the existing conflict guard
  (`silently_shadows`) does NOT catch a mis-ordered same-arity delimiter overlap,
  so it needs an explicit ordering test. **Zero forced regen** — purely additive.
- **`yp29` (`Bytes`) — SOUND for the scalar; fixed-size array is a real second
  feature, correctly secondary.** Bare `Bytes` is a clean fifth scalar leaf
  (~8-site exhaustive-match fan-out across both crates). **Load-bearing catch:**
  `Bytes` must NOT be a transparent `type Bytes = Vec<u8>` — the blanket `Vec`
  NOTA codec renders `Vec<u8>` as `[1 2 3 …]`, reproducing the exact wart the
  record exists to kill, and the orphan rule blocks a custom codec on an alias.
  It must be a newtype-scalar carrying its own codec. Fixed-size `[u8; N]` (BLS
  48/96, digests 32) needs the grammar's first numeric type-arg → a special-cased
  `(Bytes N)` head, not general const-generics.
- **`qz6j` (bare → newtype) — SOUND IN INTENT; dangerous spelling, dead anchor.**
  The cited `syntax.rs:80` is **dead code** (only `tests/` + a re-export consume
  it). The live Alias construction is `engine.rs:652` (a method literally named
  `lower_newtype` that today returns `TypeDeclaration::Alias`) and `source.rs:503`.
  A blunt flip hits ~1068 declarations, ~762 collateral (Issue 1). The **only
  fleet-forcing change** of the four.
- **`lm84` (hash-id) — SOUND; generalization of proven code, downstream of `qz6j`
  + `yp29`-fixed-size.** `RecordIdentifier` (`signal-spirit/src/lib.rs:210`) is
  `struct([u8;12])` + a separate base36 code + NotaString projection — exactly the
  template. **Correction:** base36-shortest-unique-prefix is *display truncation*,
  not a roundtrippable storage codec; it cannot be the canonical encoding for
  arbitrary-width hashes. Default to **lowercase hex** (case- and width-fixed, so
  dedup/equality is on the bytes).

## The load-bearing issues (ranked)

1. **`qz6j` collateral — scope the conversion to alias-over-scalar only.** Of
   ~1068 bare aliases, ~306 are alias-over-primitive (the wins: `Recipient
   String`, `CommitSequence Integer`) and ~762 are alias-over-declared-type (the
   re-tag pattern `State Statement`) that must stay transparent — wrapping them
   adds a useless layer and breaks every `Statement`-where-`State`-expected site.
   So `qz6j` converts to newtype **only when the reference resolves to a reserved
   scalar** (String/Integer/Boolean/Path/Bytes); alias-over-declared-type stays
   transparent. (Refinement: most hit-lines are in unused `*.concept.schema`
   stubs, so the *building* collateral is smaller — but the scalar-only rule is
   required regardless, the live `.schema` files carry the re-tag pattern too.)
2. **`Bytes` and the hash-id are ONE codec mechanism — decide the byte→text codec
   once.** Both are a bytes domain value that archives natively in rkyv but needs
   a dedicated NOTA projection to a single bracket-string code (NOTA has no quoted
   strings, so bytes-without-projection breaks `expect_fresh` the instant a field
   is retyped). Pick lowercase-hex once; `lm84` is a fixed-width parameterization
   of the same codec.
3. **Newtype emitter emits a PUBLIC wrapped field — must-fix riding with `qz6j`.**
   `schema-rust-next/src/lib.rs:3113` emits `struct #name(#visibility #reference)`,
   so every public newtype gets a public `.0` — violates wrapped-field-is-private.
   `qz6j` mass-produces newtypes, so landing it on this bug fleet-wides a
   discipline *regression*. Fix to a private field (the emitted `new`/`payload`
   accessors are the access path) before/with `qz6j`.
4. **Spec anchors point at the dead `syntax.rs` path.** Editing `syntax.rs:80` (as
   `qz6j` literally says) compiles and changes nothing. Implementers target the
   live triad: `engine.rs:652`, `source.rs:502/503`, `declarative.rs`,
   `source.rs:1002`.

## Not a real problem (debunked, so they don't resurface)

- **"29 schema-driven repos regenerate at once"** — overstated; ~15 actually
  invoke `schema-rust-next` via `build.rs`.
- **"The agent triad needs a contract rewrite"** — `signal-agent`/`meta-signal-agent`
  are hand-written `signal_channel!` with no `schema-rust-next` dep; no grammar
  change regenerates them. (Only the `agent` *daemon* repo builds from schema.)
  Migrating the agent triad onto schema-next is a separate, out-of-scope decision.
- **"criome uses `Vec<Integer>` for bytes"** — false; criome's binary fields are
  `{ value String }` newtypes. Only 4 live `(Vec Integer)`-as-bytes sites exist
  (meta-signal-upgrade, signal-terminal). `yp29` fixes criome by String→Bytes
  retype, not auto-migration.
- **"`(X)` arity-1 collides with the unit schema-node meaning"** — position-scoped
  (variant position vs type-reference position); a conscious decision, not a blocker.

## Open decisions (the psyche's)

1. **Canonical byte→text codec** — recommend lowercase hex (exact roundtrip);
   base36-shortest-prefix stays Spirit's display nicety, not a storage codec.
2. **Fixed-size bytes** — in-grammar `(Bytes N)` head (recommend; mirrors how `Map`
   is special-cased) vs an un-enforced newtype convention.
3. **Hash-id: new primitive vs marker-on-newtype** — reviewers converged on
   marker-on-newtype (a primitive is a closed parameterless scalar; it can't carry
   width + codec). Makes `lm84` downstream of `qz6j`. Confirm.
4. **Fate of aliases** — not a global drop: scalar→newtype, declared-type→stays
   transparent (or an explicit `(Alias X)` marked head if you want it nameable).
5. **Confirm the newtype pub-field fix lands with `qz6j`** (changes `.0` → `payload()`
   for every generated newtype).

## Implementation plan (blast-radius-aware)

1. **`52ro` alone** — additive, zero forced regen. Three coordinated sites + an
   ordering test. Immediately collapses criome's ~15 self-tagged variants and lets
   new authors use the compact forms.
2. **Newtype pub-field fix (`lib.rs:3113`) alone** — private field + existing
   accessors. Forces a regen of the ~15 building contracts (`.0`→`payload()`); do
   it as its own clean sweep *before* `qz6j` multiplies newtypes.
3. **`yp29` bare `Bytes` + the hex codec together** — `Bytes` as a newtype-scalar
   with its own codec (never a transparent `Vec<u8>`). Additive. Then migrate the
   4 `(Vec Integer)` sites + criome's ~5 `value String` binary fields, each a
   scoped single-contract wire change. Defer `(Bytes N)` unless a pilot needs it.
4. **`lm84` hash-id** — fixed-width parameterization of the Step-3 codec; pilot in
   ONE contract (criome `ObjectDigest`/`PublicKeyFingerprint`, or a schema-emitted
   `RecordIdentifier`) before fleet adoption. (Migrating Spirit's hand-written
   `RecordIdentifier` is its own contract migration — not a freebie.)
5. **`qz6j` LAST, scoped** — target `engine.rs:652` + `source.rs:503` (NOT
   `syntax.rs`). Convert to newtype only for alias-over-reserved-scalar; leave the
   ~762 declared-type re-tags transparent. Decide alias's fate here. Then regen the
   ~15 building contracts + patch value-flow in one coordinated sweep (checked-in
   `src/schema/*.rs` + `write_or_check` means a half-landed `qz6j` red-lights every
   gated build at once). Update the pinning test `tests/lowering.rs:73`.

Residual uncertainty (flagged by the synthesizer): the `~15 building repos` count
is from a `*/build.rs` glob; the exact `#[shape]` attribute syntax for an
`Exact(1)`/delimiter-discriminated variant is inferred from existing attributes,
not verified against the derive parser body; the test suites were not run
end-to-end.
