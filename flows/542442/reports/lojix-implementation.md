# Lojix implementation report

## Final contract

Lojix 0.21.0 consumes one absolute, regular public
`horizon-definition.datom` file and resolves/projects its selected Horizon
node. It receives no generic catalogue, cluster file, sibling directory, or
secret path by discovery. Every deploy has an explicit `SecretsInput`:
`NoSecrets` or a caller-owned absolute non-symlink `SecretsDirectory`.

Ordinary `lojix` and owner `meta-lojix` requests use generated current Datom
`Request`/`Response` roots inside length-bounded, route/binding/revision checked
binary Signal frames. String reconstruction is restricted to runtime string
fields; structural request identity remains typed. The former Dotos CLI ingress
has been replaced by generated Datom roots for inspection, reconstruction,
bootstrap, and configuration writing.

`lojix-bootstrap` accepts exactly one inline request. The no-activation form is:

```text
BootstrapRun.{ <request-id> BuildOnly.{ Horizon.{ <horizon-definition.datom> <cluster> <node> <CompleteHost-or-BaseHost> <NoSecrets-or-SecretsDirectory.{<directory>}> <immutable-criomos-ref> <nix-system> <output-selector> } <NoBuilder-or-NixBuilder.{...}> <private-journal-parent> <new-gc-root> <new-terminal-evidence> } }
```

It creates the four explicit flake inputs `system`, `horizon`, `deployment`,
and `secrets`; `BuildOnly` has no transport or activation representation.

## Durable state and upgrade boundary

A source comparison with Lojix main `46585a2c` found a real stored-layout
change: durable `DeployJob.optional_deploy_submission` now contains
`HostDeployment`/`UserEnvironmentDeployment` with the new `SecretsInput`.
Lojix therefore advances the sema store from v4 to **v5**. It refuses v4 before
row decode or restart reconstruction; it does not map old authority to
`NoSecrets`, migrate old jobs, or resume them under changed semantics.

`UPGRADES.md` documents the non-destructive cutover: stop the daemon, retain
the existing v4 primary path unchanged for `lojix-inspect-store`, and generate
the next daemon archive with a distinct new absolute v5 `store_path`. The
explicit stopped-daemon `lojix-reset-store` operation remains separately
opt-in and destructive; it recreates a recognized v2/v3/v4 store as empty v5
and discards its history/jobs.

The red-green regression is
`v5_refuses_the_v4_deploy_submission_layout_until_explicit_reset`; startup,
reset, and inspection tests prove the guard and reset behavior.

## Released producers and gates

- Horizon main: `05879e7c1e5f637f78fbe26234b95213c77c59bc` (0.6.0).
- signal-lojix main: `5ce3f11feac22a0ddbed028dec2a60385f77fa55`.
- meta-signal-lojix main: `55c1df20ddfa6ae99e0f4bca57b803bf366b781f`.
- Behaviour-complete Lojix consumer: `d4404aad0d9418e29ebbbc8042c1684276bb3dcd` (0.21.0).
- Final Lojix main: `59293764e02e0fb0ec9251f382e627787420f30d`.

The Lojix feature passed `cargo test --all-targets` (96 library tests and all
active integration tests; one existing network/Nix smoke remains ignored),
`cargo clippy --all-targets -- -D warnings`, and `cargo fmt --check`. Its remote
Nix default package passed. A previous combined BuildOnly candidate pinned
`9832f80…` and failed at the remote package test because
`tests/store_inspection.rs` still expected schema v4; the frozen revision fixes
that assertion and was remote-package green. Direct materialized evaluation of
the combined CriomOS candidate succeeded before that package-test-only failure.
`59293764` is a documentation-only child of that behaviour-complete revision:
`cargo fmt --check` passed, it contains no Rust, lockfile, contract, or flake
change, and corrects the retained-v4 inspector instructions below.

## Retained v4 inspection and main transition

The v5 inspector can read the catalog read-only, but its table reader decodes
v5 Rust records. It is therefore not evidence that a v4 job/history layout is
inspectable. The compatible reader is Lojix 0.20.3 at old main
`46585a2c8303bffe885b1722bfebd97d5353ca17`, whose CLI accepts the legacy
single inline request:

```text
lojix-inspect-store '(InspectStore <absolute-v4-store-path>)'
```

For the retained-store witness, a synthetic v4 store was created outside any
live state at `/tmp/lojix-v4-inspection.5ExX1n/retained-v4-0203.sema`. Building
that exact old binary and running
`lojix-inspect-store '(InspectStore /tmp/lojix-v4-inspection.5ExX1n/retained-v4-0203.sema)'`
reported `Database opened-read-only`, `Schema matches version=4`, a ten-table
catalog, and a readable `identifier-allocation` row. No live store was read or
changed. `README.md` and `UPGRADES.md` at final main now name this binary and
grammar; they also state that the v5 `InspectStore.{ <path> }` reader is not
the compatible v4 job/history reader.

The old main Git object was `46585a2c8303bffe885b1722bfebd97d5353ca17`. The
Jujutsu revision graph confirms that the migration's behavior commit
`d4404aad0d9418e29ebbbc8042c1684276bb3dcd` is not a descendant of that old
object: each has a distinct root. The main move was consequently a deliberate
sideways replacement after the feature's producer, consumer, and combined
checks, followed by the docs-only child `59293764e02e0fb0ec9251f382e627787420f30d`.
The exact comparison `jj diff --from 46585a2c8303bffe885b1722bfebd97d5353ca17
--to d4404aad0d9418e29ebbbc8042c1684276bb3dcd --summary` reports 34 changed
paths: dependency/version files, generated ingress, adapter/client/daemon and
bootstrap/runtime/state code, documentation, flake, and migrated tests. Before
the bookmark move, `jj status` reported no working-copy changes. The `main`
bookmark label itself is not proof of that conclusion; the clean status and
explicit object comparison are the evidence that no unseen local work was
advanced.

## Authored skill amendment for review

No authored skill source or generated skill evidence was edited. The current
generated `lojix` skill still says `## Dotos syntax`, gives parenthesized
product examples, requires a `proposal.datom` source, and says the daemon
accepts schema v4. The following is the exact review proposal for its authored
replacement blocks; it is grounded in the final Lojix contract and the
commands above.

````markdown
## Generated Datom ingress and Signal frames

Current Lojix clients accept exactly one inline generated current Datom root.
Reject files, flags, zero arguments, and extra arguments. Do not use Dotos
syntax or a legacy schema root. Ordinary and owner requests travel only in
length-bounded binary Signal frames; validate the frame binding, wire revision,
and route before recovering the typed request or response.

For a Horizon deployment, the source is exactly one existing absolute regular
non-symlink public file named `horizon-definition.datom`. Decode it as a
composed `HorizonDefinition`, resolve the requested `(cluster, node)`, and do
not load a generic catalogue, cluster source, sibling directory, or secrets by
discovery.

Each Horizon deployment carries `SecretsInput` explicitly: use `NoSecrets`, or
`SecretsDirectory.{ <existing-absolute-non-symlink-directory> }`. That
directory is caller-owned. Never serialize secret contents or secret paths into
the public Horizon artifact and never substitute a sibling secrets path.

`BuildOnly` is activation-free by its generated type. Its tested inline shape
is:

```text
BootstrapRun.{ <request-id> BuildOnly.{ Horizon.{ <horizon-definition.datom> <cluster> <node> <CompleteHost-or-BaseHost> <NoSecrets-or-SecretsDirectory.{<directory>}> <immutable-criomos-ref> <nix-system> <output-selector> } <NoBuilder-or-NixBuilder.{...}> <journal-parent> <new-gc-root> <new-terminal-evidence> } }
```

It materializes four explicit caller inputs: `system`, `horizon`, `deployment`,
and `secrets`. It has no transport or activation field.

## Retained v4 store inspection

Lojix 0.21 uses a v5 durable store because `SecretsInput` is persisted in an
in-flight submission. It refuses v4 before decoding or resuming a job. Retain a
v4 store at its existing path and create a separate v5 store path; do not copy
the database, map a historic secret authority to `NoSecrets`, or resume an old
job.

To inspect retained v4 history, use the compatible Lojix 0.20.3 binary at
`46585a2c8303bffe885b1722bfebd97d5353ca17` with exactly:

```sh
lojix-inspect-store '(InspectStore <absolute-v4-store-path>)'
```

The v5 `InspectStore.{ <path> }` ingress is not the compatible v4 job/history
reader. `lojix-reset-store` remains a separately opted-in destructive discard
operation for a stopped daemon.
````

The authored `file-editing` skill also needs this review-only integration
guard, supplied verbatim for approval: “For a change participating in an
integration, do not advance main until the assigned integration branch has all
affected producer and consumer revisions and their combined required checks
pass; follow main-feature-integration.”
