# b7c test verification — stopped on first failure

Target commit: `c537aec8eaf6a4bea34ef022744d1df89283db97`
Target tree: `a55b4e35641e88e0bb8e1c2f58d42f0f02b97249`
Temporary isolated clone: `/tmp/belief-nexus-b7c-test-verification-owned-567be7`
Ownership: FlowId `567be7`; excluded from publication; retained for failure evidence.

The production repository was read only. The isolated clone was clean at the target before the attempted patch. The proposed test-only patch adds an `InspectPublication` assertion for the invalid `../invalid` publication identity and uses `PublicationOperation::StagingGeneration`, matching `resolve_publication` lines 780–785: address/path validation failures are staging failures, while candidate manifest inspection failures are `InspectingManifest`.

The first patch command, `git apply --check`, exited 128 with `error: corrupt patch ...:30`. Per the stop-on-first-failure instruction, the patch was not corrected or retried. `git apply` itself did not run. No source change was applied. The one authorized Nix flake check was not invoked, so there are no Nix store outputs or test result.

Raw command/output/exit evidence:

- `preparation.log`: lock snapshot, clone, exact checkout, commit/tree identities, clean statuses, source search.
- `inspection.log`: exact production/test semantics inspected in the immutable checkout.
- `patch.log`: failed `git apply --check`, including cwd, exact command, raw error, exit 128.
- `focused-inspect-assertion.patch`: retained malformed proposed patch.
- `source-identity.txt`, `clone-ownership.txt`: immutable source and custody.

Foreign activity observed during the earlier preflight was not treated as this seat's slot after clarification. No build was started by this seat.
