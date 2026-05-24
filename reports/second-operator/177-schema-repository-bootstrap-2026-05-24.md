*Kind: Implementation Report · Topic: schema repository bootstrap · Date: 2026-05-24 · Lane: second-operator*

# 177 — schema repository bootstrap

## Situation

The `schema` repository did not exist remotely, locally, or under
`repos/schema`. I created `github.com:LiGoldragon/schema`, cloned it to
`/git/github.com/LiGoldragon/schema`, added `repos/schema` as the local
workspace symlink, and pushed the first `main` commit:

`d9b9150e9d26` — `schema: bootstrap typed schema model`

I also registered `schema` in `protocols/active-repositories.md` as part
of the active core stack.

## What landed

The new repo is a Rust library crate named `schema`. It deliberately starts
as a library, not a daemon triad. Current code owns:

- `Document`, `Declaration`, `Variant`, `Payload`, `TypeExpression`,
  `Primitive`, `Container`, `Engine`, and `Reference`.
- Validation for duplicate declarations, duplicate variants, invalid
  names, and unknown named type references.
- Root-versus-box layout planning for data-carrying variants.
- A conservative cross-schema reference model: reference declarations
  validate, but layout treats them as variable until the referenced schema
  is resolved.

Repo discipline files also landed: `AGENTS.md`, `CLAUDE.md`,
`ARCHITECTURE.md`, `INTENT.md`, `skills.md`, `README.md`, `Cargo.toml`,
`flake.nix`, `flake.lock`, and `.gitignore`.

## Design choice made

I treated the psyche's fresh repository intent as superseding the older
location ambiguity in `/324 §10.3` and `/325`: the schema substrate now has
its own repo. I did not move or duplicate the current operator's locked
`primary-l6pc` / `nota-codec` box-form implementation. Instead, this repo
starts one layer above that: typed schema metadata and layout planning that
macro code can consume.

This means `schema` can later either:

- depend on a `nota-box`/`nota-codec` wire container, or
- grow the `nota-box` surface itself,

without invalidating the schema document model.

## Verification

Ran in `/git/github.com/LiGoldragon/schema`:

- `cargo fmt`
- `cargo test` — 6 tests passed
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --option max-jobs 0` — passed on the remote builder

## Questions needing intent

1. Should `schema` own the eventual box-form wire crate, or should
   `nota-codec` keep `BoxedNotaEncoder` / `BoxedNotaDecoder` and `schema`
   only own metadata and layout?
2. Is the schema daemon triad still post-MVP, or did creating the repo mean
   we should now plan `schema` + `signal-schema` + `owner-signal-schema`?
3. Should the NOTA schema parser live in `schema` and feed typed documents
   to `signal-frame-macros`, or should the parser stay macro-local?
4. For cross-schema references, do we want repository/path references as the
   canonical authoring form, Cargo symbolic references, or both from day one?
