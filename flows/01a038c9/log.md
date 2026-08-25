# Flow 01a038c9

## About

Realization work mapping repository congregations, deleting understood
build-artifact directories, and designing a space-freeing protocol from
observed environment behavior.

## Scope

- The root realization scope is the repository-congregation map, removal of
  build-artifact directories whose identity and retention are understood, and
  an environment-derived space-freeing protocol.
- The full session UUID is
  `01a038c9-5052-7531-9f0e-a3e5d280451e`; this flow uses its first eight hex
  characters, `01a038c9`.

## Settled

- The child cleanup receipt records 37 understood derived-artifact deletions:
  35 Cargo `target/` directories and two Python `__pycache__` directories.
- Independent closeout verification found all 37 selected paths absent, no
  selected ordinary candidate remaining, a clean primary working copy, and a
  final `df -P /` reading of 423,949,544 available 1-KiB blocks (54%). This
  is a current filesystem observation, not a causal attribution of all free
  space to cleanup.
- The cumulative directory-measured cleanup receipt is 51,103,723,328 bytes:
  37,930,817,068 bytes in the first round plus 13,172,906,260 bytes in the
  follow-up. The child witnesses observed separate filesystem deltas of
  38,011,604,992 bytes and 13,277,585,408 bytes; these are not treated as
  pure deletion attributions.
- There were zero failures or skips among understood selected artifacts.
  Dirty source/beads work, virtual-environment `site-packages` caches, and
  uncertain source-like paths were preserved outside the authorized class.
- The evidence-backed local storage map and design-oriented space-freeing
  protocol are recorded in `reports/localRepositoryStorageMap.md`.

## Open

- Reconcile the authoritative `protocols/repos-manifest.dotos` membership
  with every physical root before any broader repository action.
- Reconcile Lojix's 12 generated-input shape roots and modeled retention
  states with the live Nix/Lojix root tree; the intended
  `/nix/var/nix/gcroots/criomos` tree was not observed.
- Nix-store, profile, generated-input, and rollback retention remain outside
  this ordinary-artifact cleanup.
