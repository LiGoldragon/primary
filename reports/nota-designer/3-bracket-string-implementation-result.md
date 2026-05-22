# 3 - Bracket string implementation result

## Result

The bracket-string design landed on feature branch
`nota-bracket-strings` in two repos:

- `nota-codec`: commit `538555e8` (`nota-codec support bracket strings`)
- `nota`: commit `40d62711` (`nota document bracket strings`)

Both branches were pushed to origin.

## What changed in `nota-codec`

`nota-codec` now treats square brackets as schema-positioned:

- at `Vec<T>` / set positions, `[ ... ]` remains the sequence form;
- at `String`, `Path`, and map-key positions, `[ ... ]` is an
  inline string form;
- `[| ... |]` is a block string form, with the existing common-indent
  dedent behavior when content starts with a newline;
- legacy double-quoted strings still decode;
- canonical encoding no longer emits double-quoted strings for
  non-bare string-like values.

The implementation lives in the decoder protocol layer, not by turning
all `[` tokens into string tokens in the lexer. That keeps vectors
working and makes the ambiguity explicit at the schema-aware boundary.

New production witnesses landed in
`nota-codec/tests/bracket_string_round_trip.rs`:

- `String` position reads `[alpha beta]` as one string.
- `Vec<String>` position reads `[alpha beta]` as two elements.
- apostrophe strings encode as `[he said 'yes']`, with no `"` emitted.
- `]`, backslash, and control characters escape in inline bracket
  strings.
- block strings dedent human-layout content.
- `|]` collision falls back to inline bracket escapes.
- bracket map keys decode when they contain no whitespace.
- map keys containing whitespace remain rejected.
- unterminated bracket/block strings return typed errors.

Existing path, transparent-newtype, and horizon feedback tests were
updated so canonical output uses bracket strings while legacy quote
decode remains covered.

## What changed in `nota`

The spec now teaches the bracket-string grammar:

- `[ ]` is the compact sequence family: a collection at collection
  positions, a string at string-like positions.
- `[| |]` is the multiline block string form.
- double quotes are described as legacy accepted input in the Rust
  codec, not the canonical authored form.
- `example.nota` now uses bracket strings.
- the obsolete rule that `[ligoldragon]` always means
  `Vec<String>` was replaced by a schema-positioned explanation.

## Verification

`nota-codec`:

- `cargo test` passed.
- `nix flake check path:/tmp/materialized-nota-codec-source --option builders ''`
  passed after materializing the worktree source without `.jj` and
  `target`.

`nota`:

- `nix flake check path:/home/li/wt/github.com/LiGoldragon/nota/nota-bracket-strings --option builders ''`
  passed. The repo has no behavioral checks; this validates the flake
  surface.

## Tooling caveats

Two workspace tooling problems surfaced:

- `tools/orchestrate claim designer ...` failed before claiming
  because `orchestrate/roles.list` now contains `second-designer
  parallel-of:designer`, while the Rust `orchestrate-cli` still has a
  closed `Lane` enum that does not include `second-designer` or
  understand `parallel-of`.
- `nix flake check` directly inside the jj feature worktree failed
  while building the source derivation because the worktree `.jj`
  metadata points back through `/home/...`, which the Nix sandbox could
  not create. A materialized source copy without `.jj` and `target`
  passed the same flake check.

These are not NOTA implementation failures, but they are production
workflow gaps for feature worktrees.

## Remaining skepticism

The chosen design knowingly makes square brackets schema-positioned.
That is the only part that still deserves careful downstream review.
The implementation proves the codec can support it cleanly, but humans
reading isolated fragments now need the schema position to distinguish
`String` from `Vec<T>`.

That cost is acceptable only because the design premise is explicit:
`String` is the compact character-vector case. If that premise stops
feeling true in real NOTA files, the syntax should be revisited before
the double-quote form is removed entirely.
