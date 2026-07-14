---
name: pi-extension-updates
description: 'Evidence-gated Pi extension updates that discover local forks and patches, reconcile every delta with upstream, and choose rebase, reimplementation, drop, or authority escalation.'
---

# pi internals

## Rules

Inspect installed Pi files, pinned Pi source, docs, and examples when Pi behavior matters and the active role permits direct inspection. In delegation-only roles, dispatch inspection instead of reading directly.

Treat installed Pi packages, generated runtime files, profile symlinks, `$HOME/.pi/agent/bin/pi`, `$HOME/.local/share/criomos/pi/package`, and runtime `dist` as read-only evidence. Do not replace managed symlinks, patch installed runtime output, add ad hoc dependency symlinks, shadow profile commands, or make copied installed source the effective Pi system.

Make durable Pi package, prompt, skill, extension, theme, settings, and harness changes through CriomOS-home/Nix patches or declarative package and configuration surfaces. Commit source, update portable inputs, build or check the owning Nix surface, and redeploy.

Read-only inspection, byte-for-byte backups for evidence preservation, and isolated repro copies are allowed when the active role permits them. They must not become effective runtime, profile, or system behavior, and they are not closeout fixes.

Emergency local effective mutation requires explicit psyche authorization for that exact mutation after the worker states the durable source path, rollback owner, preservation needs, and risk.

Preserve active role and action-space restrictions. Do not use Pi internals to bypass management delegation, read-only Spirit boundaries, or repository closeout.

Keep package inputs portable through flake inputs, committed patches, and lock files. Validate the narrow Nix surface that owns the change. Pi's wrapper can derive version and package behavior from `PI_PACKAGE_DIR`; give standalone derivation checks a representative package directory, and use the activated profile for deployment acceptance. Closeout is blocked when Pi behavior depends on uncommitted runtime edits, PATH shims, replaced managed symlinks, or copied installed source.

## Pi extension updates

### Update Rules

Start with one concrete update candidate. Record the canonical upstream package and source repository, the currently packaged version or revision and lock identity, the target version or revision, the package derivation and source input, and every activation path. Treat the update as fork reconciliation, not a version-string change.

### Discover Local Maintenance

Trace the effective package from Pi settings or Home Manager exposure through the derivation, flake input, and lock record. Inspect patches, fork revisions, vendored or copied source, overlays, overrides, substitutions, build and install transforms, environment-selected extension paths, and alternate package inputs. Repository names are hints, never proof.

Compare the unpacked packaged source with canonical upstream at its recorded base. Use commit ancestry and a base-to-tip diff for a VCS fork; use normalized tree diffs for tarballs, copied source, and generated package trees. Declare “no local fork” only after both the package-wiring scan and the source comparison find no delta.

Record immutable provenance: upstream repository, upstream base, local fork or patch revision, package lock identity, and update target. Keep the prior package and base identities as rollback pointers.

### Delta Ledger

Keep one durable ledger entry per independently removable local delta beside the owning package or fork maintenance documentation. Each entry names:

- behavior and purpose;
- rationale evidence such as a reproducer, issue, commit, test, or user-visible contract;
- local implementation paths and commits or patch hunks;
- upstream counterpart and one status: `fully absorbed`, `partially absorbed`, `still absent`, `deliberately divergent`, or `unknown`;
- a validation witness that can distinguish the desired behavior from regression.

Do not collapse several patches into one rationale. Do not infer rationale from the diff when history or a witness can establish it. Missing rationale or witness makes the delta `unknown` and blocks deletion.

### Classify and Decide

Compare the target against every ledger entry. Read upstream source, release notes, linked issues, tests, and commits; a matching feature name is not proof. When a registry or release artifact omits tests or history, use its recorded source revision, such as npm `gitHead`, to materialize the immutable upstream repository tree. Exercise the witness on the unmodified target when possible.

Choose per delta, so one package update may drop, rebase, and reimplement different deltas:

- **Rebase** when the behavior remains required, upstream still lacks or deliberately differs from it, the forward-only patch or fork commits apply cleanly to the target, the resulting diff contains only the intended delta, and its witness passes. Use patch tools in forward-only dry-run mode first. A reversed-patch warning is absorption evidence to inspect, not a successful rebase.
- **Reimplement** when the behavior remains required but upstream partially absorbs it, target APIs or structure make the old implementation misleading, or a clean application would preserve obsolete code. Define the smallest target-native remainder, remove superseded pieces, and make the witness cover the new boundary.
- **Drop** only when upstream fully owns the behavior and the unmodified target passes the delta witness plus package regression checks. Remove the patch, fork commit, override, and stale ledger claim together; patch non-application alone never proves redundancy.
- **Escalate** only when the remaining choice changes authorized behavior, user-visible values, accepted maintenance burden, or an acceptable security or privacy tradeoff. Routine source archaeology, patch repair, test design, and implementation uncertainty stay with the accountable worker.

`Unknown` is not a fifth implementation choice. Recover upstream artifacts and local history, reproduce the old failure, and strengthen the witness. If evidence remains unavailable, keep the current package or retained delta rather than deleting it by guess. Escalate only if proceeding now requires an authority or value choice.

### Apply and Verify

Work against an isolated target tree while the current package remains reproducible. Establish the rollback pointers before changing sources. Update a fork producer first, commit and push its immutable revision, then update the consumer lock and package metadata. Keep local patch changes and their consumer update in one coherent consumer change. Never point a consumer at an unpushed fork revision; follow the owning repository's required push-before-build or build-before-push order.

For each delta, retain comparison evidence from the unmodified target and the reconciled target. Run upstream tests that cover changed areas, each ledger witness, patch application checks, the package build, package-content checks, and the Pi harness or runtime flow that loads the extension. Verify the declared package version or revision and locked source. When Pi wrapper behavior depends on `PI_PACKAGE_DIR`, give standalone checks a representative package directory; use the activated profile only when deployment acceptance is actually requested.

Do not activate a failed candidate. Recover by restoring the prior consumer input and lock, the prior patch set or fork revision, and the last passing package result, then rerun the narrow load witness. Preserve the failed target and comparison notes long enough to explain the failure without making them effective runtime state.

### Escalation Packet

Return a compact packet with the decision that needs authority, viable options, evidence and unknowns, maintenance, security, privacy, and user-visible consequences, a recommendation, and the smallest reversible next step. Identify which delta entries are affected; leave independently settled deltas on their technical path.
