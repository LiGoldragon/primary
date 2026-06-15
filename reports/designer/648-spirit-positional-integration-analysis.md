# Spirit positional-syntax integration — analysis + scope

How to put the positional struct syntax (the structural-forms epic refinement)
into spirit's production schema stack, what it costs, and the blast radius.
Recon source: workflow `wpdo71d2c` (6 parallel mappers). Design context: `646`,
`647`.

## The two structural-forms lines

There are two parallel landings of the epic, and they have diverged:

| Line | Where | Has positional syntax? | Graph-coherent? |
|---|---|---|---|
| `structural-forms-integration` | every repo in spirit's graph (nota-next, schema-next, schema-rust-next, sema-engine, triad-runtime, signal-spirit, meta-signal-spirit, spirit) | **No** | **Yes** — builds green graph-wide (spirit `cargo check` passes in 6s) |
| `next/structural-forms` (+ `next/family-identity-newtype`) | nota-next, schema-next, schema-rust-next only | **Yes** | No — only the schema toolchain; no matching consumer branches |

The integration line already absorbed the *hard* part of the epic graph-wide
(structural macro shapes, TypeReference-as-derive, thiserror, families). It lacks
exactly **one** later refinement: the **positional struct-body syntax + retired
name-value reject** (schema-next commits `c7c6d8d` + `08ccfd0`). So the integration
line is the right vehicle; the work is to carry that one refinement into it.

### A skew to fix along the way

The git ref `refs/heads/next/structural-forms` (`c7c6d8d`) is **stale** — two
commits behind the real jj branch tip (`51289bc5`), which carries the reject
(`08ccfd0`) and the doc refresh. A recon agent reading the git ref wrongly
concluded "no reject exists"; the live parser test (8/8) confirmed the reject is
real at the jj tip. The jj bookmark must be synced to the git ref / origin.

## What "the new syntax" changes

The positional reader (`SourceStructBody`/`SourceField` in schema-next
`src/source.rs`, plus `Name::names_a_type`/`derived_field_name` in `src/schema.rs`,
`MacroExpansionField` in `src/declarative.rs`, and the `RetiredStructFieldSyntax`
error in `src/engine.rs`) replaces the old name-value `chunks_exact(2)` reader:

```
;; retired (rejected with SchemaError::RetiredStructFieldSyntax)
StoredRecord  { RecordIdentifier * Entry * }
StoredReferent { Referent * aliases Referents }

;; new positional
StoredRecord  { RecordIdentifier Entry }              ;; bare distinct types
StoredReferent { Referent aliases.Referents }         ;; dot-differentiated named slot
```

Spelling rules (empirically confirmed on the jj tip):
- A bare PascalCase/scoped atom is a type; its field name is the snake-cased type.
- A renamed plain-type slot uses `name.Type` (dot): `aliases.Referents`.
- A renamed composite slot uses `name (Composite)` (space): `byTopic (Map K V)`.
- A slot whose name already equals the derived snake-case stays bare.
- **Families are untouched** — `(Family { record … table … key … })` is read by a
  dedicated keyword reader, immune to the positional change. Spirit's three
  families stay exactly as written.

## The blast radius — why spirit alone is impossible

Spirit's `build.rs` lowers `schema/{sema,nexus}.schema`. To resolve imports like
`signal-spirit:signal:Input`, the `ImportResolver` is handed each dependency's
**`schema/` text directory** (`DependencySchema` → `DEP_*_SCHEMA_DIR` →
`crate_root/schema`) and **re-parses the dependency's `.schema` text**. Those
dependency schemas are saturated with retired name-value bodies:

- `signal-spirit/schema/signal.schema`: `Import { SourcePath * LocalPath * }`,
  `SemaReceipt { RecordIdentifier * DatabaseMarker * }`,
  `ReferentRegistration { Referent * aliases Referents Justification * }`, …
- `meta-signal-spirit/schema/meta-signal.schema`: `ConfigureReceipt { … }`,
  `ImportReceipt { RecordCount * DatabaseMarker * }`, …

So the moment spirit builds against the retire-enabled reader, it re-parses those
files and rejects them. **Migrating spirit requires migrating signal-spirit and
meta-signal-spirit too.** There is no spirit-only path, and a dual-mode reader
that keeps accepting name-value is ruled out by the no-backward-compatibility
override.

## The cascade (dependency order, build-verified each layer)

1. **schema-next** — carry the positional reader + reject (port `c7c6d8d`+`08ccfd0`
   onto the integration line); migrate the integration line's own fixtures.
2. **nota-next** — likely unchanged (the reader is schema-next's own lowering
   code; integration nota-next already has PascalHeadBody). Port only if the
   compiler demands.
3. **schema-rust-next** — repin schema-next; rebuild. No code change expected.
4. **signal-spirit** — migrate `schema/{signal,domain}.schema`; regenerate
   `src/schema/*.rs` (`SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1`); build + test.
5. **meta-signal-spirit** — same.
6. **spirit** — migrate `schema/{sema,nexus}.schema`; regenerate `src/schema/*.rs`
   (`SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1`); build + test.

Each layer's `build.rs` *checks* checked-in artifacts are byte-fresh, so every
migration forces a regenerate-and-commit — which is the end-to-end proof the new
syntax round-trips through the real toolchain on real production schemas. The
family-identity `SchemaHash` newtype (`647`/`6eog`) is **orthogonal** and stays
out of this scope.

## Risks

- The two lines reimplemented TypeReference/thiserror as *different* commit sets;
  porting the positional reader onto integration is a semantic re-apply, not a
  clean cherry-pick (conflict-prone if done as raw history transplant).
- Migrating wire-contract schemas changes generated artifacts; consumer hashes
  move; everything downstream regenerates. This is normal pre-production but it is
  a real multi-repo commit.
- nix build needs pushed branches + a `flake.lock` refresh; cargo (offline, via
  local-path `[patch]`) is the fast verification path during development.
- Wire-contract repos (signal-spirit, meta-signal-spirit) are normally operator
  integration territory; doing the cascade on feature branches is the reversible,
  designer-scoped way, with operator landing to main afterward.

## Landed — the cascade is done and pushed

The full cascade was implemented, verified green per layer, and pushed to the
shared `structural-forms-integration` line of every repo:

| repo | `structural-forms-integration` | verification |
|---|---|---|
| schema-next | `0543341e` → `1abdcd22` | 173/173 tests, clippy clean, `identity.rs` hash-stable |
| schema-rust-next | `e6d13940` → `ab9d16b7` | 86/86 tests; generated fixtures byte-identical |
| signal-spirit | `cf9da984` → `e7a10e79` | tests green (default + `nota-text`); `src/schema/*.rs` byte-identical |
| meta-signal-spirit | `2c34eef1` → `c67ecd52` | tests green (default + `nota-text`); artifacts byte-identical |
| spirit | `dd98342f` → `9b3bb959` | builds green (lib + bins, default + `nota-text`); artifacts byte-identical |

**The decisive proof:** every regenerated artifact across all five repos is
**byte-identical** to the pre-migration output. The positional syntax lowers to
the same rkyv model, the same generated Rust, and the same SchemaHash constants —
so the migration is provably semantically lossless on the real production stack,
and every consumer's runtime behavior is unchanged. The retired-syntax reader was
the gate: spirit re-parses signal-spirit + meta-signal-spirit schema text at
build, so the cascade was mandatory, and each layer was rebuilt against the
*pushed* (not local-path) upstreams before its own push to prove standalone
coherence.

Designer prototype seams (local-path `[patch]`) were used only for offline
iteration and removed before each push; the committed branches carry only the
`.schema` migrations plus the dependency-pin advances.

### One pre-existing caveat (not caused by this work) — bead `primary-opzy`

Spirit's `cargo test` (not its build) cannot fully run: its `agent`
*dev*-dependency (branch=main) build-depends on `schema-rust-next` branch=main
`00763d67`, which calls the long-removed `schema_next::Root::lower_to_rust` and
doesn't handle `TypeReference::Application`. That stale pin fails against *current*
schema-next (both `main` and integration) regardless of this migration — a
pre-existing breakage in the agent ecosystem. Filed as `primary-opzy`: bump the
agent ecosystem's schema toolchain pins + regenerate. Spirit's build, and every
spirit-owned schema-derived type, is unaffected (artifacts byte-identical).

### Still operator's

The shared `structural-forms-integration` branches are now positional-coherent and
pushed. Landing them to `main` + the `nix flake check` gate remain operator's
(`primary-cxyf`); the family/stream universal-positional migration is `primary-hhp0`
(syntax pinned in report `649`); the agent-ecosystem pin-bump is `primary-opzy`.
