# Meta-Signal Rename Pass

*Kind: implementation report · Topics: meta-signal, component-triad, upgrade, signal-upgrade, rename-boundary · 2026-06-03 · operator lane*

[The workspace-wide policy-contract rename is active work: `owner-signal-*` retires in favor of `meta-signal-*`, and new/current guidance must state `meta-signal` as the positive rule rather than a tentative proposal.]

[Component triad means daemon + working signal + policy signal; the policy signal is the `meta-signal-<component>` contract.]

[Reports are historical unless a current guidance rule demands editing them; do not mass-edit old reports just to rewrite history.]

## Audit

The local fleet still contains many legacy `owner-signal-*` repositories. The safe slice for this pass was the upgrade triad plus canonical workspace guidance, because the upgrade policy contract was already the live contradiction: `owner-signal-upgrade` existed as a newly touched active contract after the fleet rename decision.

The audited active targets were:

- `/git/github.com/LiGoldragon/owner-signal-upgrade`, now renamed to `/git/github.com/LiGoldragon/meta-signal-upgrade`.
- `/git/github.com/LiGoldragon/upgrade`, which depended on the policy contract.
- `/git/github.com/LiGoldragon/signal-upgrade`, whose architecture text pointed at the policy contract.
- `/home/li/primary/AGENTS.md`, `INTENT.md`, `skills/component-triad.md`, `skills/double-implementation-strategy.md`, `skills/major-break-via-new-repo.md`, and `protocols/active-repositories.md`.

The broad `owner-signal` search also found historical reports, stale generated lock references in unrelated repos, and still-unrenamed fleet repositories. Those were not blindly rewritten. The rule for this pass was coherence over text replacement: active guidance and the upgrade triad are current; historical reports remain historical; the remaining fleet is an explicit gap.

## Boundary

Remote rename was safe for the upgrade policy contract. GitHub CLI was authenticated with repo/admin scope, and `gh repo view LiGoldragon/meta-signal-upgrade` failed before the rename while `gh repo view LiGoldragon/owner-signal-upgrade` succeeded. I renamed the remote through GitHub's repository API and then aligned local directory, remote URL, crate names, schema identity, and primary symlink.

I did not rename the whole fleet in this pass. The remaining owner-signal repositories are separate contract lines with their own dependencies and likely remote rename ordering. Renaming all of them at once would mix this proven upgrade-triad change with a broad fleet cascade.

## Implementation

`meta-signal-upgrade` commit `fe465fa045cd` (`meta-signal-upgrade: rename upgrade policy contract`) does the direct contract rename:

- Remote repository renamed from `LiGoldragon/owner-signal-upgrade` to `LiGoldragon/meta-signal-upgrade`.
- Local checkout moved to `/git/github.com/LiGoldragon/meta-signal-upgrade`.
- Git remote updated to `git@github.com:LiGoldragon/meta-signal-upgrade.git`.
- Cargo package/lib/build names changed to `meta-signal-upgrade` / `meta_signal_upgrade`.
- Schema identity changed to `(meta-signal-upgrade:lib [0.1.0])`.
- Concept schema file renamed to `schema/meta-signal-upgrade.concept.schema`.
- README, architecture, skills, tests, and generated references updated to the new name.

`upgrade` commit `640be3f25258` (`upgrade: depend on meta-signal-upgrade`) retargets the runtime upgrader:

- Cargo dependency now points at `https://github.com/LiGoldragon/meta-signal-upgrade.git`.
- Rust imports now use `meta_signal_upgrade`.
- Runtime event, handover, placeholder, crate docs, architecture, and skills point at the renamed policy contract.
- `Cargo.lock` was narrowed to the renamed dependency commit `fe465fa045cd`.

`signal-upgrade` commit `e1fbcf8ba3f8` (`signal-upgrade: point architecture at meta policy contract`) updates the contract architecture text to reference `meta-signal-upgrade`.

Primary guidance now states the positive current rule:

- `AGENTS.md` says the policy contract leg is `meta-signal-<component>`.
- `skills/component-triad.md` removes the stale tentative/self-rename paragraph and states `meta-signal` as canonical.
- `INTENT.md`, `skills/double-implementation-strategy.md`, `skills/major-break-via-new-repo.md`, and `protocols/active-repositories.md` point the active upgrade policy contract at `meta-signal-upgrade`.
- `/home/li/primary/repos/meta-signal-upgrade` points to `/git/github.com/LiGoldragon/meta-signal-upgrade`; the old `repos/owner-signal-upgrade` symlink is gone.

## Verification

`meta-signal-upgrade` passed:

- `META_SIGNAL_UPGRADE_UPDATE_SCHEMA_ARTIFACTS=1 cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `cargo fmt --check`
- `cargo test --features nota-text`
- `nix flake check`

`upgrade` passed:

- `cargo fmt --check`
- `cargo test`
- `cargo test --locked`
- `cargo clippy --all-targets --locked -- -D warnings`
- `cargo test --features nota-text`
- `nix flake check`

`signal-upgrade` passed:

- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check`

The primary guidance search for `owner-signal-upgrade`, `owner_signal_upgrade`, `OWNER_SIGNAL_UPGRADE`, stale `core-signal` active forms, and malformed `meta-signal -> meta-signal` wording is clean across the touched guidance files, except for the intentional sentence naming `core-signal-*` as a legacy migration leftover.

## Remaining Gaps

Fleet rename still remains for these local repositories:

- `owner-signal-agent`
- `owner-signal-cloud`
- `owner-signal-domain-criome`
- `owner-signal-mind`
- `owner-signal-orchestrate`
- `owner-signal-persona`
- `owner-signal-persona-spirit`
- `owner-signal-repository-ledger`
- `owner-signal-router`
- `owner-signal-sema-upgrade`
- `owner-signal-terminal`
- `owner-signal-version-handover`

`core-signal-spirit` is also still a legacy predecessor name and should move to `meta-signal-spirit` in its own coordinated slice.

`protocols/active-repositories.md` still lists unrenamed owner-signal repositories where those repos actually exist today. That is intentional: the live repo map should stay accurate until each repo is renamed.

Historical reports still contain `owner-signal` references. Those are not active guidance and were intentionally left alone.

One implementation note: a broad `cargo update` in `upgrade` pulled unrelated git dependency heads and exposed a transitive schema parsing failure in `signal-persona-spirit`. I restored that broad lock movement and narrowed `Cargo.lock` to only the renamed `meta-signal-upgrade` dependency. The successful `cargo test --locked` and `nix flake check` prove the lock is coherent after the narrow change.
