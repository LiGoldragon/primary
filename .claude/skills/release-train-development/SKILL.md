---
name: release-train-development
description: 'Release train development rules.'
---

# feature development

- Use the assigned branch or isolated worktree for feature work.
- Do not share a claimed checkout.
- Conclude the worktree when work lands or is rejected.

## version control

- Use `jj` for ordinary history and pushes.
- Use an explicit message for every authored commit.
- Preserve peer work and verify the pushed bookmark.

## Nix discipline

- Model services declaratively with typed options.
- Pin portable inputs in the lock file.
- Build and deploy reproducible source.
- Keep `flake.nix` readable as an index.
- Keep substantial check and build implementations and long shell programs out of `flake.nix`.
- Keep evaluation and activation evidence separate.

## testing

- Test the changed contract with the smallest meaningful witness.
- Use the repository's durable test gate.
- Keep stateful test requirements explicit.

## release train development

- Resolve every train member to a pushed immutable revision.
- Keep Cargo and Nix lock evidence separate.
- Verify the resolved closure before landing producers and consumers.
