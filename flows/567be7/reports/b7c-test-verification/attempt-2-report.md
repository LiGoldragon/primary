# b7c focused Inspect verification — attempt 2

Result: PASS for the bounded test-only verification.

## Sealed source and patch

- Immutable base commit: `c537aec8eaf6a4bea34ef022744d1df89283db97`
- Immutable base tree: `a55b4e35641e88e0bb8e1c2f58d42f0f02b97249`
- Patched tree: `d02f15e127dec972528d212d0674d3849a1a4440`
- Modified source blob: `d59c3fd1af5f191dfd83fd9d5c8076062e2bbf25`
- Modified source SHA-256: `f4cd5a565521c771cf51a5f45b64e2805e5982908cde4a80a286dce844c29f00`
- Valid patch: `attempt-2-valid.patch`, 1189 bytes
- Patch SHA-256: `46cf178d75428bf71a77ecbb700b6c0d516e40713a74be6b686a1d379aaef20b`
- Patch Git blob: `e76dd9919084d33a8318af0ba39d347b46c1e0f5`

The only source difference is a focused assertion in `requested_publication_candidate_failures_keep_the_inspection_stage_without_effects`: it constructs an `InspectionRequest` from the invalid `../invalid` publication and asserts that `Query::InspectPublication` refuses with `PublicationOperation::StagingGeneration`. This is the existing executable oracle: invalid identity path/address construction is mapped by `resolve_publication` to `StagingGeneration`; candidate manifest inspection remains separately mapped to `InspectingManifest`.

`git diff --check` passed. `git apply --check attempt-2-valid.patch` passed in a separate freshly cloned, clean checkout sealed to the same commit and tree.

## One remote check

Command, run exactly once by this seat from the patched isolated clone:

```text
nix flake check -L --builders @/etc/nix/machines --max-jobs 0
```

Exit: 0. The log ends `all checks passed!`. The emission suite reports 23 passed, 0 failed, including `requested_publication_candidate_failures_keep_the_inspection_stage_without_effects`.

Check derivations and outputs:

- `/nix/store/v8c0gh94n4mgsy12fjqc0vkfcif7bxyk-belief-nexus-test-test-0.1.0.drv`
  → `/nix/store/g40y9qdn8y24kbqiy3fiv8pvdglph67c-belief-nexus-test-test-0.1.0`
- `/nix/store/kdkc7iczly2r3lg9hya4fik2d0i7wwjx-belief-emission-generated.drv`
  → `/nix/store/d1i15xgzqi56m0gw50a2xp2qsmzw92wn-belief-emission-generated`

Full raw build log: `attempt-2-nix-flake-check.log`, SHA-256 `fcb36e2ceefeb4a7e46354300cd97c5e9a87a3260f47bc0478c6d3ea8d93bdc5`.

## Custody and limits

The isolated clone retains one uncommitted modification to `crates/emission/src/lib.rs`. The production repository remained clean and read only. No commit, push, bead mutation, acceptance, closure, deployment, or publication occurred. The check covered x86_64-linux; Nix reported aarch64-darwin, aarch64-linux, and x86_64-darwin as incompatible and omitted. Compiler and evaluation warnings are retained verbatim in the build log and did not fail the check.

The malformed first attempt patch and logs remain untouched beside this attempt.
