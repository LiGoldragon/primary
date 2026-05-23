# Deploy-Stack Consumers Bracket-String Subreport

## Scope

Owned repositories audited and edited:

- `/git/github.com/LiGoldragon/horizon-rs`
- `/git/github.com/LiGoldragon/lojix-cli`
- `/git/github.com/LiGoldragon/lojix`

I did not edit historical reports and did not enter the locked Persona/signal repositories. The second-operator Persona/signal lock became relevant because one verification blocker is in `signal-core`.

## Horizon-rs

### Branches and commits

Two horizon changes were needed because the consumers track different horizon branches:

- Commit `7a3072c7` (`horizon-rs: migrate NOTA fixtures to bracket strings`) on `horizon-leaner-shape`, used by `lojix`.
- Commit `ae8754d3` (`horizon-rs: refresh main NOTA codec consumers`) on `main`, used by `lojix-cli`.

Both bookmarks were pushed with `jj git push --bookmark ...`.

### Changed files

Lean branch `horizon-leaner-shape`:

- `Cargo.lock`
- `lib/src/disk.rs`
- `lib/src/name.rs`
- `lib/src/proposal/placement.rs`
- `lib/src/proposal/secret.rs`
- `lib/src/proposal/services.rs`
- `lib/src/proposal/vpn.rs`
- `lib/tests/ai.rs`
- `lib/tests/network.rs`
- `lib/tests/placement.rs`
- `lib/tests/proposal.rs`
- `lib/tests/secret.rs`
- `lib/tests/tailnet.rs`
- `lib/tests/vpn.rs`

Main branch:

- `Cargo.lock`
- `lib/src/io.rs`
- `lib/src/name.rs`
- `lib/src/proposal.rs`
- `lib/tests/proposal.rs`

### Changes

- Refreshed direct `nota-codec` locks to merged main commit `538555e8` (`nota-codec` merged main for bracket strings).
- Added `NotaMapKey` derives where map keys are horizon newtypes, including node/user/domain-like names and mount paths.
- Replaced removed `NotaSum` usage with merged-codec-compatible implementations.
- Kept record-shaped empty variants such as `(Metal)` and `(TailnetClient)` by adding manual `NotaEncode` / `NotaDecode` for the affected enum shapes instead of changing the authored wire form.
- Migrated clear authored NOTA test fixtures to positional records, bracket strings, explicit `(Some ...)`, map braces, and `True` / `False`.
- Added the witness `public_certificate_with_apostrophe_must_not_require_quote_delimiters` in `lib/tests/tailnet.rs`; it decodes a bracket-string certificate containing an apostrophe.

### Verification

- `nix build .#checks.x86_64-linux.default` passed on `horizon-leaner-shape`.
- `nix build .#checks.x86_64-linux.default` passed on `main`.

## Lojix-cli

### Changed files

- `Cargo.lock`
- `README.md`
- `tests/builder_validation.rs`
- `tests/eval.rs`
- `tests/request.rs`

### Changes

- Refreshed direct `nota-codec` lock to `538555e8`.
- Refreshed `horizon-lib` lock to horizon main commit `ae8754d3` (`horizon-rs: refresh main NOTA codec consumers`) so it builds against the same codec contract.
- Changed active README NOTA examples from quote strings to bracket strings.
- Changed CLI test request arguments and generated request strings to bracket strings.
- Added the constraint-style witness `source_path_with_apostrophe_must_not_require_quote_delimiters`, decoding `(CheckHostKeyMaterial goldragon tiger [/tmp/operator's datom.nota])`.

### Verification

`nix build .#checks.x86_64-linux.default` is blocked before `lojix-cli` tests run.

Exact blocker: dependency `clavifaber` at commit `4e666c8a` still imports `nota_codec::NotaSum`, which no longer exists in merged `nota-codec`; consequently `ClaviFaberRequest` and `ClaviFaberResponse` do not implement `NotaDecode` / `NotaEncode`.

This dependency is outside my owned scope.

## Lojix

### Changed files

- `Cargo.lock`
- `tests/build_pipeline.rs`
- `tests/daemon-cli-integration.sh`
- `tests/real-build-smoke.sh`

### Changes

- Refreshed both direct `nota-codec` lock entries to `538555e8`.
- Refreshed `horizon-lib` lock to horizon lean commit `7a3072c7` (`horizon-rs: migrate NOTA fixtures to bracket strings`).
- Changed daemon and CLI configuration fixtures to bracket strings.
- Added a Nix-owned shell witness for apostrophes by using apostrophe-bearing daemon socket/state paths in `tests/daemon-cli-integration.sh`.
- Changed real-build smoke request/configuration strings to bracket strings.
- Changed the build-pipeline `HorizonProposal` fixture to positional records with bracket strings, including the nested DHCP pool record.

### Verification

There is no `.#checks.x86_64-linux.default` check in `lojix`; I used the named witnesses:

- `nix build .#checks.x86_64-linux.daemon-cli-integration .#checks.x86_64-linux.test-build-pipeline`

The named witnesses are blocked before `lojix` tests run.

Exact blocker: dependency `signal-core` at commit `f17efc1c` still expects `nota_codec::Error::UnknownKindForVerb`, which no longer exists in merged `nota-codec`.

`signal-core` is outside my owned scope and is part of the active signal work area, so I did not edit it.

## Remaining Quote Exceptions

- Rust string literals that are not authored NOTA remain, including normal assertion strings, process arguments, Nix flake text, shell quoting, and test data constructors.
- `lojix-cli/tests/network_neutrality.rs` intentionally scans for quoted historical Nix/JSON-like source literals; those are not authored NOTA examples.
- No deliberate quote-delimited NOTA fixture remains in files I changed, except where the quoted content is non-NOTA prose or generated language text.

## Blockers

- `lojix-cli` cannot complete its Nix default check until `clavifaber` is migrated off `NotaSum` for merged `nota-codec`.
- `lojix` cannot complete its named Nix witnesses until `signal-core` is migrated off `Error::UnknownKindForVerb` for merged `nota-codec`.
- Because both consumer checks are blocked in out-of-scope dependencies, I left `lojix-cli` and `lojix` changes uncommitted for the next agent after those dependency migrations land.

## Next Actions

1. Migrate `clavifaber` to merged `nota-codec` enum derives/manual codecs, then rerun `lojix-cli`'s default Nix check.
2. Let the active signal owner migrate `signal-core` to merged `nota-codec` errors, then rerun the `lojix` named Nix witnesses.
3. After those checks pass, commit the `lojix-cli` and `lojix` consumer changes with `jj` and push the relevant bookmarks.

## Coordinator follow-up

After this subreport landed, the coordinator cleared the `lojix-cli`
blocker by migrating `clavifaber` and refreshing `lojix-cli` to that
pushed dependency.

Additional landed deploy-stack commits:

- `clavifaber` `eec30b0b`
  (`clavifaber: migrate NOTA request surface to bracket strings`);
  `nix flake check --print-build-logs` passed.
- `signal-lojix` `a007e8b6` on `horizon-leaner-shape`
  (`signal-lojix: migrate NOTA sum records to bracket strings`);
  `cargo test` and `nix flake check --print-build-logs` passed.
- `lojix-cli` `bf73b9d3`
  (`lojix-cli: migrate NOTA request examples to bracket strings`);
  `nix flake check --print-build-logs` passed.

The `lojix-cli` blocker named above is therefore resolved.

The remaining `lojix` blocker changed shape after `signal-lojix`
advanced: the failing surface is now a daemon/client API migration to
current `signal-lojix` and `signal-frame`, not a `nota-codec`
`NotaSum` cleanup. `lojix` still references retired `wire::LojixFrame`,
`wire::LojixFrameBody`, `wire::LojixChannelReply`,
`wire::LojixChannelRequest`, `wire::DeploymentSubmission`,
`wire::DeploymentObservationSubscription`, and the old request variant
names. The current contract emits `Frame`, `Operation`, `Reply`,
`LojixReply`, `LojixEvent`, and `StreamKind`.

Tracker: bead `primary-36iq.6.1` covers the `lojix` port required
before this migration slice can close.
