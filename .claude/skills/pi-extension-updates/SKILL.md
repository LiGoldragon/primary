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

Treat a Pi extension update as maintained-fork reconciliation, not a version bump. Keep installed/profile/store outputs read-only evidence; change the fork and declarative Nix owner, never effective runtime files.

### Compact flow

1. Establish primary/live sources and recent upstream activity. Record upstream, deployed fork revision, base, target, consumer pin, and activation path.
2. Extract mechanisms and tests from upstream; do not copy its brands, role names, or prompt bulk. Compare each local delta for overlap and local compatibility.
3. Make a semantic Jujutsu patch stack in an isolated workspace. For every delta decide: upstream, drop, carry/reimplement, or escalate. An automated proposal may aid comparison but must never blind-merge.
4. Validate the pristine target and reconciled result with focused tests, full relevant tests, package build, generated surfaces, and a runtime load/smoke witness. Record a failing pristine gate separately rather than weakening the reconciled gate.
5. Push the producer revision before updating a consumer pin. Reconcile the Nix/Home Manager source, build it, and deploy only after checks pass. Confirm the activated package is the pinned revision.

### Decisions and retirement

Carry only a small local behavior with a rationale and witness. Drop it only when upstream owns the behavior and the unmodified target passes its witness. Escalate only an authority, privacy, safety, or user-visible tradeoff; ordinary archaeology and patch repair stay with the worker.

A fork retires when the upstream target passes every retained witness without local deltas and the consumer can pin upstream directly. Re-audit whenever upstream activity, a deployment failure, or a changed local requirement invalidates the prior comparison.

Use `repository-management`, `version-control`, `feature-development`, `management`, `helper-context-transfer`, and `design-quality` for their owning mechanics. Keep branch recipes and ledger detail out of ordinary dispatch prompts.
