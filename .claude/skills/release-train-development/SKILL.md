---
name: release-train-development
description: 'How to author, resolve, materialize, verify, and hand off immutable multi-repository epic release trains without conflating Cargo, Nix, or cache authority.'
---

# feature development

## Rules

Use feature branches or separate worktrees for code-repo feature work, experiments, rewrites, and prototypes that may ship. Do not do feature work directly on a shared integration line unless the repo instructions explicitly say so.

The parent or task owner names the branch and scope before work starts. A worker edits only that branch or worktree and returns the exact validation evidence.

Base feature work off `main`. If the shared checkout is claimed or already being edited, request an isolated workspace with `RequestWorktree`; the orchestrator scaffolds it from `main` with a feature bookmark at the canonical root `~/wt/github.com/LiGoldragon/<repo>/<branch>`. Claim that path with Orchestrate before editing.

Keep radical experiments in the existing repository. A branch may replace the whole tree for a prototype; that still does not justify a new repository.

Different worktrees of the same repository are separate claim scopes; the same worktree is a conflict.

At merge or abandonment, conclude the worktree with `ConcludeWorktree` (Merged or Rejected) so the orchestrator removes the workspace and later agents do not mistake stale checkouts for live work.

Subagents that edit code or produce ship-ready prototypes use their assigned feature branch or worktree. Research-only workers that write only their assigned output need no worktree.

## version control

### Use Jujutsu, not raw git

Use `jj` for version control. Raw `git` is only an escape hatch named in this skill. Every description-taking command uses an inline message or equivalent headless flag; never let a command open an editor.

### Target the repository explicitly

When scripting jj against any repository other than the lane's own verified working directory — especially throwaway, demo, or freshly cloned repos — pass an explicit `-R <path>`/`--repository <path>` on every command, or guard the `cd` so its failure hard-stops the script (`cd <path> || exit`). Agent bash resets cwd to the primary workspace each call, so a silently failed `cd` lets cwd fallback aim a mutating command at primary. Never let cwd fallback decide which repository a mutating command hits.

### Primary workspace stays on main

In primary, work directly on `main`. Do not create branches. Commit the complete working copy, then move `main` to the committed parent and push.

```sh
jj status --no-pager
jj commit -m 'short imperative message'
jj bookmark set main -r @-
jj git push --bookmark main
```

If unrelated dirty files exist, name them and avoid staging concepts; jj commits the working copy as a whole unless a repo-specific instruction explicitly permits path-scoped surgery.

### Code repos use logical commits

Outside primary, keep one logical change per commit. Inspect status before and after edits. Use concise imperative commit messages that name the behavior changed.

```sh
jj status --no-pager
jj diff --stat
jj commit -m 'component: change behavior'
jj bookmark set main -r @-
jj git push --bookmark main
```

Push each completed logical commit. Do not accumulate a local stack that is ready but unpushed.

### Integration facts

Branch and dependency staleness is closeout evidence. Surface unmerged branches, stale dependency pins, and dependencies that have unmerged branches when they affect integration, deployment, repurpose, or closeout; do not silently push past them.

### Descriptions are explicit

Do not run `jj describe @` as a finalization step. Do not leave a real commit descriptionless. If a command would open an editor, cancel and rerun with `-m`, `--message`, or the command's headless equivalent.

### Routine checks

Before committing, run the narrow validation that proves the change. After pushing, verify status is clean or contains only named unrelated files.

Useful reads:

```sh
jj status --no-pager
jj log -r 'main..@' --no-pager
jj diff --stat
jj show --stat --no-pager
```

### Fix uninitialized repos

If a repository lacks jj metadata, initialize colocated jj and track the existing default bookmark before editing.

```sh
jj git init --colocate
jj bookmark track main@origin
jj status --no-pager
```

### Raw-git escape hatches

If a remote URL blocks push mechanics, use raw git only to inspect or change the remote configuration, then return to jj.

If push is rejected because the remote advanced, stop normal work. Fetch with jj, inspect divergence, and ask before rebasing or force-moving shared history unless the task explicitly authorizes that repair.

During an authorized landing, replaying your landing stack over a compatible commit that reached `main` mid-flight is in scope and expected; it produces new `main` commits and orphans the stack's feature branches, so clean up the orphaned branches afterward. Pause and ask only when the rebase would rewrite commits outside your landing stack or that you did not author.

### Restore carefully

`jj restore` discards working-copy content. Use it only when the exact path and loss are understood. Prefer reading diffs and making a forward edit.

### Forbidden shortcuts

- Do not use `jj git push -c @` for routine commits.
- Do not create anonymous descriptionless checkpoints to satisfy process.
- Do not path-scope commits in primary.
- Do not use raw git for ordinary add, commit, branch, merge, or push work.

## Nix discipline

### Model services as NixOS modules

Long-running services are NixOS modules with typed options, systemd units, users, files, and firewall policy. Do not smuggle service shape into ad-hoc shell scripts or container-only definitions when the host is NixOS.

### Choose flake inputs deliberately

Use registry or remote inputs for shared dependencies. Do not commit local file inputs. For temporary integration checks, override inputs at command time instead of changing the committed flake.

Keep lock-file updates intentional and reviewable. Pin through the lock file, not duplicate hashes in `flake.nix`.

### Build and deploy from reproducible inputs

Commands that prove a change should build from the committed flake state or an explicit temporary override. Do not rely on an untracked checkout to be present on the target host.

Compiled artifacts are build outputs. Do not compile at service start. Runtime scripts may select, configure, and launch artifacts; they do not build them.

Command resolution, Home Manager profiles, package profiles, and runtime outputs are owned by source plus activation. Change them through flake inputs, modules, packages, checks, and deployment, not by PATH shadowing, replacing managed symlinks, mutable profile edits, ad hoc dependency symlinks, or copied store/profile output.

### Cargo dependencies in crane flakes

For Rust git dependencies, keep the dependency identity in Cargo metadata and let the lock file carry the revision. Do not add manual output hashes to flake code as the normal fix.

### Do not bake store paths into source

Source and docs do not depend on raw store paths. Refer to packages, derivations, options, and outputs by name. Inspect store paths with Nix commands when needed; do not search the store filesystem.

### Use Nix to get tools

If a tool is missing, run it through Nix or add it to the dev shell. Do not install ad-hoc host packages to make a build pass.

### Checks are the gate

`nix flake check` is the default pre-commit proof for Nix changes. Add narrower package, module, or VM checks when they prove the edited surface better. Stateful deployment checks must name the host, target, and rollback plan.

### Keep evaluation separate from activation

Evaluation and build checks prove the derivation graph. Activation and deployment checks prove host behavior. Do not treat a successful build as evidence that a service migrated safely.

### Module shape

Keep options typed and documented. Put defaults near option definitions. Keep assertions close to the invariant. Prefer small modules with clear imports over one large conditional module.

### Prefer data over shell

Use Nix values, options, derivations, and systemd fields for structure. Shell belongs at the edge where a program must be invoked, and it stays small enough to audit.

## testing

### Tests prove the edited contract

Choose tests that witness the behavior or invariant changed. Prefer small deterministic checks near the contract over broad smoke tests that can pass while the edited rule is broken.

### Nix is the normal test gate

Expose durable project checks through the flake. Pure checks belong in flake checks. Test-only binaries use clear test names and do not become runtime services.

Run the narrow check that proves the edit, then the broader gate required by the repo before commit. Build that single check directly (`nix build .#checks.<system>.<check>`); reserve full `nix flake check` for pre-commit, and run whole-engine sweeps dry-run first with background builds and logs on disk. Record exact failures when a check cannot run.

Do not substitute an unrelated passing check for the one that proves the edited surface.

Do not pipe a test or check run through `tail` or `head` when judging pass/fail — the pipe substitutes the pager's exit code for the run's own and can truncate per-binary results into a false green. Capture full output to a file and read the run's real exit status (or `${PIPESTATUS[0]}` when a pipe is unavoidable); judge pass/fail from that exit status, not a piped tail.

### Keep state explicit

Stateful tests name their resources, host requirements, cleanup, and failure artifacts. They do not depend on hidden local state. If a test needs credentials or hardware, mark the requirement and provide a safe skip or manual gate. Place a daemon-sandbox unix socket under a short run root (e.g. `/tmp/<lane>/`) so its path stays under the SUN_LEN limit; never nest the socket under the deep session scratchpad path.

### Test architecture, not just regression

When the change protects architecture, write tests for forbidden dependencies, protocol compatibility, ownership boundaries, and invariant preservation. A compile-fail or metadata check can be the right test when runtime behavior is not the contract.

### Put tests in owned locations

Keep unit tests close to small pure logic. Put integration tests at crate or component boundaries. Keep generated-surface tests at the generator source, not by patching emitted output.

### Name tests by behavior

Test names state the behavior under proof. Avoid names that only repeat the function name or issue number.

### Failure output is part of the interface

Assertions should say what invariant failed and show the relevant values. Do not dump secrets or large unrelated state.

### Keep fixtures minimal

Fixtures carry only the state needed to prove the case. Prefer named builders or typed records over copied blobs. Internal test, eval, and diagnostic artifacts use typed Rust records with NOTA projection; non-NOTA text fixtures name the external consumer or protocol that requires that exact format. When a fixture encodes compatibility, state the compatibility boundary in the test name or nearby assertion.

### Do not weaken tests to pass

If a test fails because the contract changed, update the contract and test together. If it fails because the implementation is wrong, fix the implementation. Do not delete coverage without replacing the proof.

## release train development

### Purpose

Use this skill when one feature spans independently locked repositories. A
release train makes one integration closure reproducible without treating a
branch name, universal Cargo.lock, local path, or cache as authority.

### Author

Author one `release-trains/<name>.nota` intent per epic. It names component
selectors, exact expected bases, and only explicitly admitted immutable
external components. Keep operational Synchronizer configuration separate.

Intent constrains discovered manifests; it never declares or overrides Cargo
or flake topology. A discovered internal edge outside the train, a missing
member, an unadmitted external, an expected-base mismatch, or selector movement
fails loudly.

### Resolve and materialize

Resolve every selector to a pushed commit before creating evidence. Emit an
immutable typed closure with a domain-separated identity. Candidate branches
are scoped `train/<name>` and are integration artifacts only: never write
mainline, worker branches, deployment pins, or production state.

Materialize each consumer from its exact source tree. Generate that component's
valid `Cargo.toml`/`Cargo.lock` changes through Cargo-aware resolution and its
own `flake.lock` through pinned commit plus narHash evidence. Cargo and Nix
locks are distinct domains; do not merge them and do not expect flake overrides
to alter Cargo Git locks.

Generate canonical `release-train.lock.json` only as a Textual JSON projection
of the resolved closure. An integration flake reads it and fetches only exact
commit/narHash inputs. No local paths may remain at the portable gate.

### Verify and hand off

Verify pushed candidate commits with the integration closure, recording exact
commits, lock identities, narHashes, closure identity, and check outcomes. A
failed train is discarded through its dedicated candidate branches; it has no
merge authority.

Do not build a shared compiled-artifact cache speculatively. First measure
matching Nix derivation keys. A future crate-source index is immutable,
Cargo-validated source materialization keyed by registry checksum or Git
commit; it is never a mutable latest-dependency registry.

Bootstrap JSON may use a deterministic adapter. Replace it with TextualJson
only when the shared structural-form boundary is ready, preserving the typed
closure and byte-stable JSON fixtures.
