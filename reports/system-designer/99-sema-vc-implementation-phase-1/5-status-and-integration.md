# 99/5 — Phase-1 status: what landed, the NOTA answer, residue, integration order

**TL;DR.** Phase 1 of the version-control build is on pushed, reviewed,
green feature branches. The macro library is now fully typed (zero
hand-parsing on the read path — Spirit `v0n6` realized in schema-next, with
one general-purpose derive extension landed in nota-next); schema values now
carry blake3 content identity (whole-schema + per-family closures); the
workspace has its first cross-host transport (TCP listener with a typed
`Unix | Tcp` peer-identity sum); and the engine's versioned log dispatches
on typed `FamilyIdentity` with a *derived* store hash, `storage_kernel()`
reduced to a read-only handoff, mind's out-of-band writes eliminated, and
`replay_versioned` folding state back from the log — `iir4` realized at the
engine layer. 372 tests green across six crates, every suite re-run
independently by the reviewers.

## The NOTA answer (the psyche asked to be told)

**No fundamental gap.** All three violation sites dissolved into typed
structural macro nodes. The derive needed one genuinely missing,
general-purpose capability, which was built rather than worked around:
`#[shape(head = "...", body)]` for variable-arity headed forms like
`(Fields item*)`, plus `StructuralMacroNode for Vec<Item>` — nota-next
branch `structural-shape-extension`, four new tests.

One precise boundary remains, by design rather than failure: the
pattern/template payload trees (`MacroPatternObject` / `MacroTemplateObject`)
are universal mirrors of arbitrary NOTA — any delimiter, any nesting, with
`$name` / `$*name` capture atoms. They decode through hand-written **impls
of the StructuralMacroNode trait** (the sanctioned leaf pattern, same as
`SourceVariantName`), not through the derive, because (a) the derive has no
`#[shape(...)]` vocabulary for sigil-prefixed atoms, any-atom fallbacks, or
any-delimiter variants, and (b) the pattern engine captures blocks and
bodies but cannot capture *which delimiter* matched — which a tree-mirror
must store to re-encode. The matcher substrate can express sigiled atoms
(`AtomShape::with_sigil`) and any-delimiter shapes (`DelimitedShape::any`),
so this is a derive-vocabulary plus delimiter-capture limitation, not a hole
in the macro-node design. If the psyche wants even tree-mirror types
derive-expressed, the extension is: a delimiter capture kind in the pattern
engine plus sigil/any-delimiter shape forms in the derive. Optional;
nothing currently violates `v0n6`.

## What each branch establishes for the next phase

- **`schema-next@schema-content-identity`** — `Schema::content_hash()` and
  `Schema::family_closure(name).content_hash()`: the hashes phase 2's
  emission pins as per-family consts. Known coverage boundaries are now
  documented in the module doc and ARCHITECTURE: relation declarations move
  only the whole-schema hash; the whole-schema address includes
  `SchemaIdentity`, so family hashes are the pure-structure addresses. A
  cross-crate fact phase 2 must own: an importing family's hash does **not**
  move when the imported type changes inside the dependency (the closure
  carries the import's stable identity only) — cross-crate change detection
  composes family hashes with the dependency schema's own hashes.
- **`sema-engine@versioned-family-identity`** — `FamilyIdentity { family,
  schema_hash, table }` in every versioned operation; `StoreSchemaHash`
  derived from the sorted family inventory (structurally impossible to
  hand-supply); storage layout guard v2 hard-fails pre-family stores;
  `Engine::replay_versioned` + `ReplayReceipt`; `StorageReader` with no
  write affordance plus an architectural truth test. Per-family hashes are
  still typed *stand-ins* (`SchemaHash::for_label`) until phase-2 emission
  supplies real content hashes — drift now hard-fails instead of silently
  corrupting.
- **`mind@memory-graph-family`** — all durable mind state through logged
  engine families; the only versioned consumer no longer bypasses its own
  log. Honest cost: existing `mind.sema` stores hard-fail (typed
  `StorageLayoutMismatch` + mind schema v7→v8) and must be re-seeded —
  accepted pre-production. Known follow-up: each memory mutation currently
  logs a full `MemoryGraph` snapshot payload; decomposing the graph into
  row-level families is future mind work.
- **`triad-runtime@tailnet-listener`** — `TcpListenerDaemon` /
  `BoundTcpListenerDaemon` + `PeerIdentity::{Unix, Tcp}`. Intentional
  pre-production breaks at integration: `lojix/src/daemon.rs:176-182` and
  `message/src/router.rs:260-261` read credential accessors and must decide
  explicitly what a TCP peer means (likely reject); the emitted
  `handle_working_input` doc comment needs refresh at the next
  schema-rust-next regeneration.

## Stage-0 residue (named, pinned, not broken)

Components still writing through the kernel handoff, all pinning
sema-engine `main` so they build untouched until the operator rebases:
**orchestrate** (`src/tables.rs`, ~10 write sites — the whole component-local
table layer), **persona** (`src/manager_store.rs:267/:293/:388/:424`, plus
`tests/manager_store.rs:884-928`, a source-scan truth test that requires the
removed `storage_kernel().write(` text and must be rewritten with its
migration), **router** (`src/tables.rs:66/:106`). Each needs the mind-style
family migration when sema-engine main advances.

## Integration order (operator lane)

1. nota-next `structural-shape-extension` → main; then schema-next
   `typed-macro-library` (flip its nota-next dep back to `branch = "main"`,
   `cargo update -p nota-next`). Independent of everything else; ready now
   (bead filed).
2. schema-next `schema-content-identity` → main (independent of 1 in
   content; same repo, trivial ordering either way).
3. sema-engine `versioned-family-identity` + mind `memory-graph-family`
   land **together** (mind's Cargo points at the sema-engine branch; flip to
   main at integration). Gate: the orchestrate/persona/router residue
   migrations ride the same integration or stay pinned. Mind version-number
   collision to reconcile: this branch bumps 0.2.0→0.3.0 while the canonical
   checkout carries an uncommitted operator 0.3.0.
4. triad-runtime `tailnet-listener` → main once lojix/message peer-identity
   arms land (or in the same integration pass).
5. Phase-2 branches build on 2 and 3's branches and rebase trivially once
   those reach main.

## Spirit records this phase realizes

`v0n6` (structural macro nodes everywhere), `x0ja` (blake3 content
addressing), `wrjl` (hash-is-identity direction), `iir4` (log authoritative
— engine layer), `fosp` (engine-exclusive storage boundary), `rj9y` (tailnet
TCP + typed peer identity), `0yx5` / `t0tu` set up phases 2–3. Per-repo
INTENT.md files on every branch carry the bracket-quoted records.

## Next: phase 2 (running)

- **Storage families in schema + RecordFamily emission** — sema.schema
  grows a family declaration (stream-declaration precedent); schema-rust-next
  emits per-family content-hash consts (computed at generation from the
  closure), engine descriptors, the closed `RecordFamily` enum + decoder
  (unknown identity = typed hard error), and the component's
  `VersioningPolicy` — replacing the engine branch's label stand-ins.
- **The fold** — checkpoint payload + engine-owned import + rebuild-from-log
  + the mirror outbox in the same transaction, with operator 214's
  witnesses (checkpoint-restore, payload-replay, same-transaction, crash),
  plus the review's engine fixes (no stamping before catalog validation;
  tombstone replay gets its own error variant).

Phase 3 after that: spirit opt-in + v8→v9 fold-migration pilot (`t0tu`),
the mirror triad repos (`0yx5`), deploy bead for system-operator.
