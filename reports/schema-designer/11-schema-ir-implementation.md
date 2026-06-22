# Schema IR as the single representation — Help collapsed onto the resolved IR

*schema-designer · report 10 · the working demonstration of "schema IR is the
single representation": Help is now a thin projection of schema-next's resolved
`SourceReference` IR, the same object instance-schema and Rust lowering read.
The duplicate Help AST is deleted; Help and instance-schema converge on
`(Vector Domain)`, proven by a real `cargo test`. All on the new designer branch
`schema-ir` across four repos; `main`, `help-codec`, and `instance-schema`
untouched.*

## The pipeline, now with one IR and three projections

```text
schema text (.schema)
  -> SourceDeclaration / SourceReference   (parse)
  -> resolution                            (the canonical resolved IR)
       -> schema-rust-next Rust lowering
       -> Help view              (NEW: projection, was a duplicate AST)
       -> per-instance schema reference rendering
```

Help was the odd one out: it carried `HelpBody` / `HelpTypeExpression` — a local
mirror of `SourceDeclarationValue` / `SourceReference` — built so that
`(Vec Domain)` survived as an opaque `Application` in Help while instance-schema
(reading the resolved type) already emitted canonical `(Vector Domain)`. The
collapse removes that fork.

## (a) The Vec -> Vector fix: migrate the contract source

Chosen fix: **migrate the contract `.schema` source to canonical `(Vector T)`**
in `signal-spirit/schema/signal.schema` (15 sites) and `schema/domain.schema`
(2 sites). This is schema-next's own canonical spelling (all its schemas already
use `(Vector ...)`) and the durable phase-out of the dropped alias.

Rejected the alternative leg — re-accepting `Vec` at the decode boundary as
`Vector`. On `main` `(Vec T)` no longer special-cases; it falls to the generic
`Application { head: Vec }` fallback in **three** parse paths
(`SourceReference::from_record`, `ExpandedObject::type_reference`,
`TypeReference::from_nota_block`). Re-accepting `Vec` would resurrect a
deliberately-dropped alias across all three — the wrong direction. Canonical at
source removes the legacy spelling from the one place it still lived.

## (b) The duplicate deleted; how Help now projects the resolved IR

Deleted from `signal-spirit/src/help.rs`: `HelpBody`, `HelpTypeExpression`,
`HelpTypeExpressionKind`, `HelpFieldTypes`, `HelpVariantTypes`,
`HelpTypeExpressions`. `HelpRoot` / `HelpNode` / `HelpEntry` now hold
`Option<SourceDeclarationValue>` — the resolved IR verbatim. Text codec is
schema-next end to end:

- encode: `HelpEntry::to_schema_text` re-heads the body as
  `SourceDeclaration::new(name, body)` and calls `.to_schema_text()`.
- decode: `HelpResponse::from_schema_text` is
  `SourceDeclarations::from_schema_text`, each declaration becoming a
  `HelpEntry { name, body: declaration.value().cloned() }`.

No hand `format!` printer, no parallel decoder. The one new schema-next method is
`SourceReference::plain_name(&self) -> Option<&Name>` (a method on the
data-bearing enum) for Help's one-level name resolution.

The collapse surfaced a real semantic gain: the old duplicate was **lossy** (it
collapsed declared field/variant types to bare names). The resolved IR is
faithful, so three goldens updated to the schema codec's own canonical forms —
`VerbatimQuote` now shows `(OptionalAntecedent (Optional Antecedent))`,
`DomainMatch` keeps `[Any (Partial) (Full)]`, `Domain` expands each variant's
nested leaf enum. These are exactly what the schema codec round-trips; Help and
the codec now agree by construction.

## (c) Real cargo test — convergence proven

`tests/help_instance_schema_convergence.rs` (feature `nota-text`), all green:

```text
test help_domains_renders_the_canonical_vector_reference ... ok   ;; (Help Domains) -> (Domains (Vector Domain))
test help_and_instance_schema_render_the_same_domains_reference ... ok   ;; Help SourceReference == instance-schema SourceReference; both render (Vector Domain)
test help_domains_reference_matches_instance_schema_expansion ... ok   ;; Help decl == instance-schema expanded view
test result: ok. 3 passed; 0 failed
```

Full `signal-spirit` `--features nota-text` suite: lib 0, daemon_configuration 2,
dependency_boundary 2, generated_contract 16, help_instance_schema_convergence 3,
instance_schema 10, validation 3 — all ok. Upstreams green: nota-next 8
instance-schema + suite; schema-next 20 result lines incl. 6 instance render +
help source_codec; schema-rust-next full suite.

## (d) Daemon-default build clean

`cargo build` / `cargo test` with no features: clean, no warnings. The
`dependency_boundary` gate (`cargo tree --edges normal --no-default-features`)
passes — the runtime tree excludes `nota-next` / `schema-next`; Help and the
schema-next runtime dep enter only via `nota-text`.

## (e) Pushed branch tips (schema-ir)

| repo | tip | base |
|---|---|---|
| nota-next | `4642807e` | instance-schema (unchanged) |
| schema-next | `1bfeb9c7` | merge(help-codec, instance-schema) + plain_name |
| schema-rust-next | `b744e1d9` | instance-schema + repin |
| signal-spirit | `39b1506e` | merge(help-codec, instance-schema) + collapse |

Base choice: no single existing branch had both Help and instance-schema, so
`schema-ir` is a clean **merge** of `help-codec` and `instance-schema` in the two
repos that carried Help work (schema-next, signal-spirit); the leaf deps adopt
`instance-schema` and repin. signal-spirit keeps the report-9 local `[patch]`
path redirects (now pointing at the `schema-ir` worktrees) so one IR version
flows end to end; an operator merging to main drops those patches.
