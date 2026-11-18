# Proposal 2 credential source proof — selected raw Codex

Status: source-established save semantics; no native execution, credential read,
link creation, login, refresh request, or production mutation performed.

## Selected executable and provenance

Select `/nix/store/r0k59hi2q6di7xhmqxp11vygy4hclzyy-codex-next-candidate-0.161.0-alpha.2/bin/codex`,
not either production wrapper. Field's actual inventory is
`flows/4c325a/v6jr-ouranos-flow-contract-inventory.md`.
Its derivation is `5ck97j38j3sbxjzynkl8hn77bxh554dy-codex-next-candidate-0.161.0-alpha.2.drv`.
The install phase copies the upstream precompiled binary without a source patch.
The source fetch derivation `138p7pivxrhkl6363v12z9bw2rlj88zs-codex-x86_64-unknown-linux-musl.tar.gz.drv`
names the official release URL
`https://github.com/openai/codex/releases/download/rust-v0.161.0-alpha.2/codex-x86_64-unknown-linux-musl.tar.gz`
and SHA256 `Vfht8jbnRC2IwhWGfVMngXX85155T52yCpZ7ae5MqOk=`.
These were read with `nix derivation show`, not evaluated or rebuilt.

The locally present upstream repository `/git/github.com/openai/codex` has
release tag `rust-v0.161.0-alpha.2` resolving to
`870b79feef9d4ecdd578b9f76f621c54f744bc31`.
This binds the source reading to the exact release provenance, not a newer
checkout's implementation. It is release-source evidence, not a reproducible
proof that upstream's uploaded binary equals a build of that tree.

## File save and refresh

At that tag, `codex-rs/login/src/auth/storage.rs`:
- `get_auth_file`, lines164–166, chooses `CODEX_HOME/auth.json`.
- `FileAuthStorage::load` opens that file through `File::open`.
- `FileAuthStorage::save`, lines213–230, creates the parent, serializes the
  auth record, opens with truncate/write/create and mode0600, writes and flushes.
  There is no temporary-file rename, unlink, canonical-target replacement,
  `O_NOFOLLOW`, or sibling lock in this save body.
- `create_auth_storage_with_store`, lines509 onward, selects FileAuthStorage
  for `AuthCredentialsStoreMode::File`.

`codex-rs/login/src/auth/manager.rs:1149–1160` routes `save_auth` to the
selected backend. Its `persist_tokens` at1594–1622 loads the stored record,
updates refreshed token fields and last_refresh, then invokes the same
backend's `save`.

Thus, with `cli_auth_credentials_store = "file"`, an existing auth.json
symlink is followed for both load and save; refresh saves through the link to
the single production file. The link is not replaced by this body. This is
ordinary POSIX open behavior, not the stale capsule helper's asserted0.167
canonical-target/locking algorithm. No cross-process refresh lock is proved.
The shared credential can be updated by refresh, as the approved shared-file
ruling anticipates; all other homes/state remain private.

The packet must explicitly choose file storage and prohibit login/logout or
credential-mode changes during the test. Logout uses remove_file and would
unlink the private link; it is outside this test. The production target is
`/home/li/.codex-next-5ck97j38j3sb/auth.json`, corresponding to the selected
next native endpoint, and is named without reading it. Field verifies target
existence/ownership and the exact link metadata only before launching.

## Model and effort

A bounded parse of frozen ConfigurationSnapshot
`/tmp/s4s7-configuration-2219e4.4q4cGYOs/configuration.datom`, field
ConfiguredModels, finds `{ Luna gpt-6-luna }`. The configured next endpoint
lists gpt-6-luna. Candidate source `crates/flow-nexus/src/model.rs` assigns
Luna medium effort. No whole snapshot is replayed; synthetic Luna declarations
alone will be installed in fresh Memory. No native model-availability or
provider acceptance is claimed before execution.
