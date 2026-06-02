# Private repositories and intent privacy — 2026-06-02

## What changed

Two private GitHub repositories now exist for personal-affairs reports:

- `LiGoldragon/assistant-reports` — private assistant report repository.
- `LiGoldragon/counselor-reports` — private counselor report repository.

Both are checked out under the primary workspace's gitignored `private-repos/` directory and exposed through gitignored convenience symlinks under `repos/`:

- `private-repos/assistant-reports/` and `repos/assistant-reports`.
- `private-repos/counselor-reports/` and `repos/counselor-reports`.

The primary workspace now has `skills/privacy.md`, and assistant/counselor role skills route personal-affairs report substance into these private repositories instead of primary's public report tree.

## Current privacy rule

Public primary files may carry the mechanism: the existence of the private repos, routing rules, privacy-safe status, and skill guidance. They do not carry personal details, counselor analysis, or assistant working notes.

Ordinary Spirit may record privacy-safe meta-intent, such as the decision that private reports belong in private repositories. It should not receive private personal substance.

Until a private Spirit substrate exists, private intent points go in a private report section titled `Private intent` inside the matching private repository.

## Private intent design options

### Option A — separate private Spirit database

A separate Spirit database/socket pair handles private personal-affairs intent. This keeps the five existing kinds intact and isolates storage/access. The challenge is agent routing: every agent must know when to use private Spirit vs ordinary Spirit.

### Option B — privacy-marked variants of every intent kind

Add variants like `PrivateDecision`, `PrivatePrinciple`, `PrivateCorrection`, `PrivateClarification`, and `PrivateConstraint`. This makes privacy visible at the type level but still risks one database containing both public and private material unless storage/access is also separated.

### Option C — privacy field on intent entries

Keep the five kinds and add a privacy classification field. This is schema-efficient and queryable, but the storage plane still needs private access control; a field alone does not prevent leakage.

### Option D — private intent as private reports until substrate lands

Use the private repos as the interim substrate. This is safest immediately because it avoids ordinary Spirit leakage, but it loses Spirit's query ergonomics until a private daemon/database exists.

## Recommendation to discuss

The conservative next shape is D now, then A when implemented: private reports carry private intent temporarily; a separate private Spirit database becomes the real private intent substrate. B or C can still be used inside that private database if the psyche wants type-level privacy markers, but they should not be treated as sufficient by themselves.

## Verification

- GitHub reports both new repositories as `PRIVATE`.
- Both repositories have bootstrap commits on `main`.
- `private-repos/` is gitignored in primary.
- `repos/assistant-reports` and `repos/counselor-reports` symlink to the local private checkouts.
