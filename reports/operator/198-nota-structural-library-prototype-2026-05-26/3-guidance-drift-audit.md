# 3 — Guidance drift audit

Subagent 3 report for `reports/operator/198-nota-structural-library-prototype-2026-05-26/`.

## Scope

Read:

- `skills/nota-design.md`
- `repos/nota/INTENT.md`
- `repos/nota-codec/INTENT.md`
- `repos/schema/INTENT.md`
- `repos/nota/ARCHITECTURE.md`
- `repos/nota-codec/ARCHITECTURE.md`
- `repos/schema/ARCHITECTURE.md`
- nearby schema guidance: `repos/schema/AGENTS.md`, `repos/schema/README.md`
- prototype schema files: `repos/schema/prototype/schemas/nota.schema`, `repos/schema/prototype/schemas/coordinate.schema`
- recent intent records for `nota`, `schema`, `core`, and `naming`
- nearby reports `operator/195`, `operator/197`, `designer/350`, and `designer/353`

No code edits were made.

## Current Intent Anchor

The latest direction is records `783-807` plus the earlier records they refine:

- NOTA is a thin structural library for delimiter/object inspection, object counts, recursive shape, spans, and symbol qualification.
- NOTA methods should say `qualifies_as_*`, not `is_*`, where final type context is needed.
- Schema macros are custom parsers over NOTA block structure; they consume shape methods and re-emit resolved schema objects.
- The endpoint is `AssembledSchema` / `Asschema`: pure, macro-free, fully resolved enum and struct definitions.
- `.schema` root is an implied `Schema` struct supplied by `.schema` context and the schema-schema.
- The current schema root direction is positional structs around imports/exports and input/output; field ordering is still explicitly carried as uncertain in record `806`.
- `owner-signal-*` should move to `core-signal-*`; Spirit-facing names should drop unnecessary `persona` ancestry.

## Drift Items

### 1. Quote-string legacy guidance contradicts current codec behavior

`skills/nota-design.md:196-205` still says `nota-codec` accepts legacy `"..."` strings through `read_legacy_quote_string`. `repos/nota-codec/INTENT.md:27-41` says the same. `repos/nota/README.md:74-76` also says legacy double-quoted strings are accepted as migration input. `AGENTS.md:174-180` repeats the same high-authority guidance.

The current codec rejects quote strings at the lexer boundary: `repos/nota-codec/src/lexer.rs:162` returns `QuoteStringDelimiter`, and tests such as `repos/nota-codec/tests/horizon_rs_feedback_fixes.rs:169-212` assert rejection for quoted and triple-quoted strings. `repos/nota-codec/ARCHITECTURE.md:151` correctly says double-quoted string forms are rejected.

Impact: agents reading guidance can still assume a migration-acceptance mode exists. The code and tests have already crossed into hard bracket-only behavior.

Correction path: patch `skills/nota-design.md`, `repos/nota-codec/INTENT.md`, `repos/nota/README.md`, and the `AGENTS.md` hard override so they say quoted strings are rejected by current codec behavior. Historical legacy acceptance should live only in reports/history.

### 2. PascalCase guidance still treats typed semantics as raw NOTA semantics

`skills/nota-design.md:141-167` and `repos/nota/README.md:112-128` teach the older rule as if raw NOTA can always decide PascalCase: data-carrying variant, struct, or unit variant. `skills/nota-design.md:183-189` and `repos/nota/README.md:122-128` also state that PascalCase at ordinary `String` positions is rejected.

That remains true for the existing typed codec path, but it is not the whole new model. Records `786`, `789`, and `799-803` say raw NOTA should expose qualified-symbol candidates and leave final casing/type legality to the schema or macro context. The latest wording wants `qualifies_as_symbol`, not `is_symbol`; demotion from qualified symbol to string is easy, while later promotion is hard.

Impact: the docs collapse two layers into one: raw structural NOTA and typed schema decoding. That will bias agents toward putting PascalCase legality in the structural library, which is exactly what the new design removes from raw NOTA.

Correction path: split the guidance into two explicit layers. Raw NOTA exposes atoms, delimiter blocks, and qualified-symbol candidates. Typed schema decoding may reject PascalCase at a `String` field when that is the selected final type.

### 3. Schema repo still teaches six-position schema and authored Features

`repos/schema/INTENT.md:9-18` names six fixed top-level fields, including `features`. `repos/schema/ARCHITECTURE.md:5-24` does the same and names an `owner signal header`. `repos/schema/AGENTS.md:7-11` and `repos/schema/README.md:5-11` repeat the six-position authored shape.

The implementation is still wired to that shape: `repos/schema/src/multi_pass.rs:128-151` rejects anything except six top-level values, and `repos/schema/tests/multi_pass_pipeline.rs:173-181` asserts that non-six-position documents fail. The feature surface remains a first-class pass through `repos/schema/src/feature.rs:3-9`, `repos/schema/src/engine.rs:16-21`, `repos/schema/src/engine.rs:265-279`, and `repos/schema/src/node_shape.rs:5-12`.

This conflicts with records `730-732`, `751`, and `805`, and with `reports/designer/350-schema-feature-drift-retraction-2026-05-26.md:12-26` and `reports/designer/353-schema-derived-nota-design-2026-05-26.md:126-135`. Authored schema should not carry a Features section. Runtime/effect/composer machinery can survive only behind the schema surface.

Impact: repo-local intent and architecture are exactly what agents read before editing, so they will keep reimplementing the old surface even when reports are correct.

Correction path: rewrite `repos/schema/INTENT.md`, `repos/schema/ARCHITECTURE.md`, `repos/schema/AGENTS.md`, and `repos/schema/README.md` around the implied root `Schema` struct, imports/exports, input/output, namespace maps, macro lowerers, and `Asschema`. Fence the old six-position reader as compatibility if it must remain, then flip tests so authored Feature sections are rejected by the current path.

### 4. Prototype `.schema` files violate the no-comments schema intent

Intent record `419` says schema files should not carry comments; descriptions belong in code, not schema source. The prototype files are comment-heavy:

- `repos/schema/prototype/schemas/nota.schema:1-31` has a prose header and block layout commentary.
- `repos/schema/prototype/schemas/nota.schema:45-62` adds explanatory comments inside the namespace.
- `repos/schema/prototype/schemas/coordinate.schema:1-24` carries a prose domain description and section banners.

`repos/nota/README.md:87-92` is aligned at the general NOTA level: comments carry no load-bearing data. But `skills/nota-design.md:47-86` still allows schema preamble comments for NOTA files generally, which can be misread as applying to real `.schema` source.

Impact: these prototype files are useful teaching artifacts, but if they become canonical examples, they normalize comments in `.schema` files and undermine schema-as-data discipline.

Correction path: keep teaching versions in reports or README examples; strip comments from canonical `.schema` fixtures. If the no-comments rule is meant to be mechanical, add a schema fixture lint or parse-mode rejection for comments in authored `.schema` files.

### 5. Owner/core naming drift is now high-authority

Records `765-768` say Spirit-facing names should drop unnecessary `persona` ancestry and move `owner-signal-*` to `core-signal-*`. Record `768` is maximum certainty: owner-signal surfaces become core-signal surfaces; core owns the privileged control/library layer.

The workspace still teaches the old name in high-traffic places:

- `AGENTS.md:158-166` defines the component triad as `<component>`, `signal-<component>`, and `owner-signal-<component>`.
- `protocols/active-repositories.md:39-66` lists many `owner-signal-*` repos as current surfaces.
- `repos/schema/ARCHITECTURE.md:19-24` still names an `owner signal header`.
- `repos/schema/AGENTS.md:15-17` still describes a future daemon/working-signal/policy-signal triad instead of the emerging core-signal terminology.

Impact: this is not only naming polish. The old `owner` vocabulary keeps policy/control framed as ownership, while the new intent frames it as core control/library surface with safer ordinary signal interfaces above it.

Correction path: stage the terminology update in guidance first: `AGENTS.md` and `skills/component-triad.md` should name the current direction, probably with a migration note that existing repositories may still be named `owner-signal-*` until renamed. For Spirit-facing work, examples should use `spirit`, `signal-spirit`, and `core-signal-spirit`.

## Bottom Line

The most dangerous drift is not in the newest prototype report; it is in the guidance surfaces agents are required to read before touching the repos. The code already rejects quote strings, but guidance still teaches legacy acceptance. The schema design has moved away from six-position/features, but the schema repo still presents that shape as current truth. The raw NOTA structural-library idea is new enough that older PascalCase documentation now needs a layer split instead of another local exception.

The next cleanup should be a guidance-first patch before more implementation: update NOTA quote guidance, split raw NOTA from typed schema decoding, rewrite schema repo intent/architecture around `Asschema`, strip comments from canonical schema fixtures, and begin the `owner-signal` to `core-signal` terminology migration.
