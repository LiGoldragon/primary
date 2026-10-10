# Types book tests

Repository: LiGoldragon/orchestrate-test. No datom-codec test repository
exists; orchestrate-test was chosen because Orchestrate derives its
contracts through datom-codec and owns the FlowId, LockName and LockPath
nouns the claims use.

Branch: `types`, not merged. Pushed commit: `e24da9`.

Host: prometheus (ssh to the NixBuilder; `hostname` printed `prometheus`).

Nix command, run on prometheus:

    nix build --keep-going --no-link --print-build-logs \
      github:LiGoldragon/orchestrate-test/e24da9e…#checks.x86_64-linux.rustc \
      github:LiGoldragon/orchestrate-test/e24da9e…#checks.x86_64-linux.datom-codec \
      github:LiGoldragon/orchestrate-test/e24da9e…#checks.x86_64-linux.lint

All three built. Compiler: rustc 1.98.0-nightly (bc2112ed5 2026-06-18),
from the rust-build pinned by datom-codec 0.32.2 (`4dff16`). The full
`nix flake check` of the repository, which also builds the Orchestrate
scenarios, was not run.

## Method

`checks/rustc.nix` compiles each file in `fixtures/rustc/` as a binary
with `--edition 2024`, extracts the distinct `error[E…]` codes from
stderr, and fails the check unless the outcome equals the expectation
written in the check. `checks/datom-codec.nix` builds the crate in
`fixtures/datom-codec/` with crane against a copy of the datom-codec
flake input (path dependency) and compares its whole stdout.

## Verdicts

| claim | fixture | observed | verdict |
| --- | --- | --- | --- |
| 1 alias LockName into FlowId | alias-crossing | compiled | pass |
| 2 newtype LockName into FlowId | newtype-crossing | E0308 | pass |
| 3 Display on alias of String | alias-display | E0117 | pass |
| 3 Display on `struct FlowId(String)` | newtype-display | compiled | pass |
| 4 size_of FlowId, String | newtype-size | ran, printed `24 24` | pass |
| 5 alias through derive | datom-codec | `abc123` | pass |
| 5 `struct FlowId(pub String)` through derive | datom-codec | `{ abc123 }` | pass |
| 6 `paths.push(path)` on `Paths(Vec<LockPath>)` | newtype-push | E0599 | pass |
| 7 `paths.0.push` inside defining module | field-push-inside | compiled | pass |
| 7 `paths.0.push` outside, private field | field-push-outside-private | E0616 (field `0` of struct `Paths` is private) | pass |
| 7 `paths.0.push` outside, `pub` field | field-push-outside-public | compiled | reported |

Claim 7 named no expected code; the observed code is E0616. With the
field `pub`, the outside push compiles.

## Sources

- Branch `types` of github.com/LiGoldragon/orchestrate-test at `e24da9`:
  `checks/rustc.nix`, `checks/datom-codec.nix`, `fixtures/rustc/`,
  `fixtures/datom-codec/`, `lib/components/rust.nix`,
  `lib/components/datom-codec.nix`.
- Build outputs on prometheus: `/nix/store/6pwi5w…-rustc/observed`,
  `/nix/store/v74n6g…-datom-codec/observed`.
- Provenance receipt: unavailable; no PROVENANCE handoff was given.
