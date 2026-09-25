# ethos-zero dependency-ethos repin: receipt

Subflow of 38de5b (Opus), 2026-09-25. It fixes the defect found in `nix-witness-local.md` row 3.

## Landed

ethos-zero main `cf7dd12` (parent `2a39e50`). After the push, `git ls-remote origin main` returned `cf7dd128bcaead69e03ce1c2e6ac20c0c19a6823`.

- `flake.nix`: protos was pinned at `1febca7` (the lock held `2054086`) and is now `2f9c63c`, its current main. datom-codec moved from `09e2a9d` to `58474fd`, its current main, which is after fix 10's `8c05d5a` dropped `Meaning.String`. The locked nixpkgs, rust-build and flake-utils are unchanged. The lock shrank because protos `2f9c63c` no longer has its own ethos-zero input, so the nested nodes were removed.
- `checks/dependency-ethos.sh`: the tool is now run as `reply="$(… 2>&1)" || status=$?`. Unless the status is 0 and the reply is `Generated.*`, the check prints `<declaration> (exit N): <reply>` to stderr and exits 1. It no longer dies silently under `set -eu`.

## Version

No bump. The versioning skill asks for one when public behavior, wire, storage, package or deployment changes. This commit changes only a check's inputs and its script. The binary, its crate and its output are unchanged, so it stays at 13.0.0.

## Witness (local build on ouranos, `--option builders '' --option substituters https://cache.nixos.org --option max-jobs auto`, nix.conf untouched)

- `nix flake check -L` on the committed tree: `all checks passed!`, exit 0. The dependency-ethos log shows four `Generated.[ … ]` lines: protos.rs, protos-kinds.rs, datom-codec.rs and datom-codec-kinds.rs.
- Negative case: `nix build .#checks.x86_64-linux.dependency-ethos --override-input datom-codec …/09e2a9d` fails, and the log ends with
  `…/17y75hdv…-source/datom-codec.ethos (exit 1): Rejected.{ …/datom-codec.ethos { 11 3 } Conceptual.{ [ 1 1 3 0 ] Intrinsic.Meaning } }`.
  The refusal now reaches the log.

## Method

The work was a fresh clone in `…/scratchpad/ez-repin-38de5b-opusA/`. It ran under Orchestrate lock 6527, which has been released. Nothing was activated or installed.
