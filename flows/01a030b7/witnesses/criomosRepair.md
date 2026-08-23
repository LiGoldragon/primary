# CriomOS ClaviFaber repair

Method: code read `/git/github.com/LiGoldragon/CriomOS/modules/nixos/complex.nix`, the pinned ClaviFaber request-surface test, and CriomOS history; probe the behavioral Nix check with the configured remote builder.

## Observations

- The failed old candidate emitted a parenthesized `PublicKeyPublicationWriting` request. ClaviFaber 0.2.0 had migrated to DOTOS and rejected that form.
- CriomOS declarative owner repair already existed in ancestor `3bcd9189`: the NixOS `complex-init` integration emits the canonical curly DOTOS request.
- The new immutable main revision is `35fc6e9896d012bf6f54a9916bd8e725af3fcea0` (`checks: execute complex ClaviFaber publication contract`). It changes the CriomOS behavioral check and root `UPGRADES.md`, not the already-repaired owner module.
- The legacy request was witnessed failing through the real ClaviFaber DOTOS parser; the canonical request then passed Nix parsing, independent evaluation, and remote builder execution.
- `UPGRADES.md` documents the breaking systemd-boot deployment procedure and the observed partial-TestActivation boundary without prescribing a hot fix.

## Hypotheses

None. The old activation journal error and parser behavior identify producer/consumer request-shape skew.

## Unknowns

The separate ClaviFaber repository still has stale examples and manual scripts using legacy forms; their correction is outside this CriomOS change.
