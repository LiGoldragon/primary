# 193 - Schema object pass and Spirit v0.3 skill correction

## Scope

This slice responds to two direct corrections:

- Spirit skills were stale and still taught agents to call `spirit-v0.2.0`
  or use the v0.2 single-topic `Record` shape.
- The schema parser path from `/349` and the `/350` retraction still did not
  match the psyche's delimiter-first, pass-driven parsing intent.

Intent records captured during the slice:

- 715-721: schema parsing should be pass-driven toward `AssembledSchema`,
  bootstrapped through explicit assembled/builtin schema specifications, using
  NOTA delimiter/object shape and per-file namespace prefixes.
- 722 + 727: Spirit skills should document current production Spirit and teach
  agents to use the unsuffixed `spirit` CLI for normal capture.
- 723-726: schema parsing should identify parentheses, square brackets, and
  curly braces as first-pass schema object roles; schema files contribute a
  prefix; ordinary/owner socket split remains current.

## Spirit Skill Update

Updated:

- `skills/spirit-cli.md`
- `skills/intent-log.md`

Changes:

- Documented Spirit `0.3.0` as the live production shape.
- Replaced single-topic record examples with the topic-vector shape:

```sh
spirit "(Record ([workspace] Decision [summary] Maximum))"
```

- Reframed versioned wrappers (`spirit-v0.2.0`, `spirit-v0.3.0`, etc.) as
  diagnostic/testing surfaces only.
- Stated the normal agent command explicitly: use unsuffixed `spirit`.

Committed on primary:

```text
a619f18c skills: document Spirit v0.3 production CLI
```

## Spirit Database State

The unsuffixed production `spirit` resolves to v0.3.0:

```text
/nix/store/a7ym03j4h63grjkr6jkqk1y7v8rwxi22-spirit-v0.3.0/bin/spirit-v0.3.0
```

Record-count check by observation:

```text
spirit       -> 743 records
spirit-v0.3.0 -> 743 records
spirit-v0.2.0 -> 723 records
```

Interpretation: production has cut over to v0.3.0, and v0.3.0 is now the
authoritative substrate. It is not being mirrored back to v0.2.0. The v0.2.0
database is retained as an older side-by-side database and is now behind
because new records have been written to v0.3.0 after cutover.

## Schema Implementation

Updated branch:

```text
repo: schema
branch: operator-full-schema-spirit-2026-05-26
commit: 2498e5b3 schema: add delimiter-first object pass
```

New files:

- `src/object_pass.rs`
- `tests/object_pass.rs`

Edited:

- `src/lib.rs`
- `src/multi_pass.rs`
- `ARCHITECTURE.md`

The new `SchemaObjectPass` is the first-pass reader that the prompt was
asking for. It:

- parses any schema file into ordered top-level NOTA values;
- derives the schema namespace prefix from the file stem;
- classifies every root by delimiter:
  - parentheses = record / enum / variant / macro-record object;
  - square brackets = sequence object;
  - curly braces = name-value namespace map;
  - atom = identifier/string/scalar;
- preserves curly-map entry order;
- exposes identifier vectors before semantic lowering;
- records recursive object paths so later passes can dispatch by position.

The existing `multi_pass` path now starts by constructing a
`SchemaObjectPass`, then adapts into the current six-position compatibility
reader. This makes the object pass part of the active parser path instead of a
standalone toy test.

## Constraint Tests

New constraints in `tests/object_pass.rs`:

- root delimiters are preserved;
- file namespace prefix is derived from the `.schema` path;
- curly-map namespace entries preserve order;
- namespace values expose their delimiter shape;
- square-bracket identifier vectors are observable before semantic lowering;
- recursive paths locate nested header/variant objects.

Verification run:

```sh
cargo test
nix flake check --option max-jobs 0 --print-build-logs
```

The Nix check passed through the remote builder and included build, test,
upgrade-rule exact test, docs, fmt, and clippy.

## What This Corrects

This moves the branch away from treating the fixed six-position schema shape
as the actual first principle. The first principle is now a NOTA object pass:
read delimiters and positions, keep ordered namespace maps, derive file
prefixes, then let macro/lowering passes decide meaning.

This also makes `/350` easier to act on. The drifted `Feature` surface still
exists in this branch for compatibility, but the parser now has a cleaner
lower layer where future work can remove authored feature sections without
also rewriting the raw object reader.

## Remaining Gap

The authored `Feature` variants are still present in code:

- `Feature::EffectTable`
- `Feature::FanOutTargets`
- `Feature::StorageDescriptor`

They are now isolated above the object pass, not baked into the first reader.
The next cleanup is to replace the old six-position `features` slot with a
schema-file-type or channel-specific root-object model, then remove authored
feature parsing while keeping hidden composer/runtime machinery where it
belongs.

