# nota-config and Spirit surface

## Scope

Owned implementation scope for this subagent:

- `/git/github.com/LiGoldragon/nota-config`
- this subreport file

Spirit CLI examples were not edited by this subagent because no
Spirit repository or workspace skill surface was inside the owned
implementation scope.

## Dependency refresh

`nota-config` already resolved `nota-codec` to the merged
bracket-string-capable main commit:

- `Cargo.lock`: `nota-codec` source at
  `538555e895529e2884b7d37d20c66aadc2a49c08`

No dependency file change was needed.

## Changed files

Committed and pushed in `nota-config` as `b38f4719`:
`Strengthen nota-config bracket string witness`.

- `tests/inline_nota.rs`
  - renamed the inline decode witness to
    `nota_argument_accepts_apostrophe_text_without_quote_delimiters`
  - added an assertion that the authored NOTA argument contains no
    double-quote string delimiter
  - kept the apostrophe-bearing prose payload as `[we're ready]`
- `README.md`
  - changed the inline argv example to a bracket-string prose value:
    `"([we're ready] 64)"`
- `AGENTS.md`
  - changed the repo-contract inline argv example to the same
    bracket-string prose shape
- `ARCHITECTURE.md`
  - changed the architecture inline argv example to
    `"([we're ready] High)"`

## Tests run

- `cargo fmt`
- `nix flake check`
  - passed for `x86_64-linux`
  - built `checks.x86_64-linux.default`
  - Nix warned that `aarch64-darwin`, `aarch64-linux`, and
    `x86_64-darwin` were omitted by the default check

`cargo test` was not used as final evidence; the final evidence is
the repo-owned Nix check.

## Remaining quotation-mark exceptions

- Documentation examples still show shell quotation around the single
  argv token, for example `"([we're ready] 64)"`. Those quotes are
  shell grouping syntax, not NOTA string delimiters. The authored NOTA
  prose value is the bracket string `[we're ready]`.
- Rust tests necessarily contain Rust string literals such as
  `"([we're ready] High)"` and expected decoded Rust strings such as
  `"we're ready"`. These are host-language syntax, not authored NOTA
  quotation-mark string syntax.
- Error messages in `src/error.rs` remain Rust string literals.
- No normal nota-config authored NOTA example remains in the
  quotation-mark string form for ordinary prose.

## Blockers

None for the owned `nota-config` scope.

## Next actions

- A separate owner for the Spirit CLI surface should migrate live
  Spirit examples and any workspace skill examples to bracket-string
  authored NOTA where practical.
- Other consumer repos should prefer constraint-style witnesses that
  prove the same shell-safety property through their Nix-owned test
  surfaces.
