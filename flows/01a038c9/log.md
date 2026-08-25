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

- The child cleanup receipt records 32 understood derived-artifact deletions:
  31 Cargo `target/` directories and one Python `__pycache__`.
- Independent closeout verification found all 32 selected paths absent,
  preserved candidates present at their recorded sizes, a clean primary
  working copy, and current root free space of 411,107,460 1-KiB blocks.
- The directory-measured cleanup receipt is 37,930,817,068 bytes; the child
  witness observed a 38,011,604,992-byte `df` delta. The difference is not
  treated as a pure deletion attribution.
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
