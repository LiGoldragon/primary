*Kind: Audit Slice · Topic: repo-wide schema consumption · Date: 2026-05-24 · Lane: operator*

# 176.4 · Repo-wide schema consumption

## Scope

Read-only audit of schema files across `/git/github.com/LiGoldragon`, with
special attention to whether `.schema` files are consumed by code or only mark
future migration intent.

## Counts And Categories

The workspace has 73 canonical `schema/*.concept.schema` files if mockup and
worktree duplicates are excluded. Including those duplicates, the recursive
count is 75.

These concept files are useful migration markers, but most are not active code
inputs.

## Active Schema Consumers

### `schema` crate

The `schema` crate is a real library. It parses, validates, resolves imports,
lowers documents into `AssembledSchema`, and contains tests for route lowering
and upgrade planning.

It is not yet a proc-macro crate and does not itself emit Rust code.

### `signal-frame` proc-macro adapter

`signal-frame/macros` depends on the `schema` crate and adapts
`AssembledSchema` into the existing `signal_channel!` emitter.

This is the current bridge from `.schema` to generated contract code.

### `signal-persona-spirit`

`signal-persona-spirit/spirit.schema` is the one live component schema consumed
by production contract code.

### Validation-only tests

Some repositories, especially orchestrate-related ones, validate schema files
in tests. That proves parseability, not production adoption.

## Marker-Only Areas

The `/327` designer marking sweep intentionally did not convert code. It added
architecture/intent markers saying components are scheduled for schema-engine
upgrade.

Examples where architecture now names a schema target while code remains
handwritten:

- `signal-orchestrate`
- `owner-signal-orchestrate`
- `forge`
- `signal-persona-origin`
- many other signal contracts with handwritten `signal_channel!` bodies

These are not violations by themselves. They become risky only if later agents
read the architecture markers as proof that code migration happened.

## False Positive Risks

Not every file named schema is part of the active schema macro path:

- `schema/tests/fixtures/schema-e2e/*.schema` are fixtures.
- `signal-sema/magnitude.schema.nota` is a vocabulary file, not a component
  signal tree.
- `signal-frame-mockup-*` and `signal-frame-worktrees/*` are mockup/worktree
  copies.
- JSON schema files in unrelated infrastructure are outside the Persona
  `.schema` lane.

## Verdict

Workspace schema adoption is real but thin. The active generated-code path is:

```text
schema crate -> signal-frame/macros schema adapter -> signal-persona-spirit/spirit.schema
```

The concept-schema sweep gives the workspace a map for future migration. It
does not yet make those components schema-derived.
