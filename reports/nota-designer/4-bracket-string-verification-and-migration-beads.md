# NOTA bracket-string verification and migration beads

## Result

The core bracket-string implementation is present and tested in
`nota-codec` on branch `nota-bracket-strings`, commit `538555e8`
(`nota-codec support bracket strings`).

The language-home documentation is present in `nota` on branch
`nota-bracket-strings`, commit `40d62711` (`nota document bracket
strings`).

This does not mean the whole Nota family has already absorbed the
change. The implementation and spec branches are ready to merge, but
downstream consumers still pin earlier `nota-codec` revisions from
`main`. The migration beads filed below are the cross-repo work needed
after the codec merge.

## Verification

`nota-codec` local inner-loop test:

```sh
cargo test
```

Passed. The run included:

- 13 bracket-string witnesses.
- 9 map-key witnesses, including custom key types and duplicate-key
  rejection.
- 8 mixed-enum witnesses.
- Path, primitive, option/vector/record, transparent-newtype, and
  compile-fail suites.

`nota-codec` Nix-backed test:

```sh
nix build --no-link --print-out-paths \
  path:/tmp/<materialized-nota-codec-source>#checks.x86_64-linux.default \
  --option builders ''
```

Passed. The resulting check output was
`/nix/store/bwkcmnrpy8ws8nzi6z61ccnmd0b896nh-nota-codec-test-0.1.0`.
Its targeted `nix log` shows the check phase ran
`cargo test --release --locked` and passed the same behavior and
compile-fail suites.

The source was materialized to a temporary directory excluding `.jj`
and `target` before running Nix. This avoids the known jj worktree
source-materialization problem; it is not a codec test failure.

`nota` spec/docs gate:

```sh
nix flake check path:/home/li/wt/github.com/LiGoldragon/nota/nota-bracket-strings --option builders ''
```

Passed. The `nota` flake currently exposes devShell evaluation only,
so behavior coverage lives in `nota-codec`.

## What Is Implemented

In `nota-codec`:

- `Decoder::read_string`, `read_path`, and `read_map_key` accept
  bracket strings at string-like schema positions.
- Sequence positions still read `[ ... ]` as vectors.
- `[|...|]` block strings decode, with common indentation stripped
  when the content starts with a newline.
- Canonical encoding emits bare identifiers where valid, bracket
  strings for ordinary non-bare string-like values, and block strings
  for safe multiline values.
- Canonical encoding does not emit ordinary quotation-mark string
  delimiters.
- Legacy quotation-mark strings still decode.
- Map keys remain scalar key text in `{key value ...}` maps; whitespace
  in keys is rejected, including through bracket form.
- Custom map key types are constrained through `NotaMapKey`.
- Mixed enums support both bare unit variants and record-shaped
  data-carrying variants in the same enum.

In `nota`:

- README examples teach bracket strings as the normal string form.
- `[|...|]` is documented as the pretty multiline block string form.
- Quotation-mark strings are described as legacy accepted Rust-codec
  input, not the normal authored form.

## Remaining Gap

Downstream migration has not happened yet. Active components and
contracts that pin `nota-codec` still need lock refreshes after the
codec branch merges to `main`; then their docs, fixtures, examples,
and CLI snippets should move away from ordinary quotation-mark string
syntax wherever practical.

`nota-derive` itself does not directly depend on `nota-codec`; it emits
code that calls the codec API. The current `nota-codec` Nix test already
builds `nota-derive` from `main` through trybuild, so this bracket-string
change does not currently require a separate derive code change.

## Filed Beads

- `primary-36iq` - epic: coordinate the NOTA bracket-string merge and
  consumer migration.
- `primary-36iq.1` - merge the `nota-codec` bracket-string
  implementation to `main`.
- `primary-36iq.2` - merge the `nota` grammar/docs branch to `main`.
- `primary-36iq.3` - update `nota-config` and Spirit CLI examples,
  including a Nix-owned shell-safety witness for apostrophe-containing
  prose inside bracket strings.
- `primary-36iq.4` - refresh Persona `signal-*` and `owner-signal-*`
  contracts onto the merged bracket-string codec and update canonical
  examples.
- `primary-36iq.5` - refresh Persona runtime components onto the merged
  codec and migrate CLI/docs/test projection examples.
- `primary-36iq.6` - refresh adjacent NOTA consumers and deploy-stack
  examples, including `horizon-rs`, `lojix-cli`, `lojix`, `chroma`,
  `chronos`, `criome`, `nexus`, and `nexus-cli`.
- `primary-36iq.7` - sweep authored NOTA examples away from ordinary
  quotation-mark string delimiters, with explicit exceptions only for
  legacy-decode tests, historical reports, or non-NOTA prose.

