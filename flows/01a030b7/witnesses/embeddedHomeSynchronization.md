# Embedded Home synchronization

Method: code read exact CriomOS revision `35fc6e9896d012bf6f54a9916bd8e725af3fcea0`; probe Zeus NixOS Home Manager units, user GC roots, actual executable paths, and retained standalone profiles.

## Observations

- The deployed CriomOS revision pins CriomOS-home `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`.
- Its target NixOS configuration maps embedded `home-manager.users` to Home activation packages; Zeus cluster projection includes both `li` and `bird`.
- `home-manager-li.service` and `home-manager-bird.service` are enabled, active-exited NixOS units with successful results. Their user `current-home` GC roots resolve to their respective embedded generations.
- Both embedded Home activations completed during host activation, and each updated the actual `~/.nix-profile`.
- Both users resolve Codex to version `0.148.0` and Claude Code to version `2.1.235`, matching the immutable CriomOS-home target.
- Retained standalone Home Manager profile links point at older generations and are not the active NixOS-embedded generations.

## Hypotheses

The retained standalone profiles are historical migration residue, not an active competing owner. This is supported by active embedded units, their GC roots, and live executable resolution.

## Unknowns

Whether an operator later invokes standalone `home-manager switch` was not established. Two Kvantum files are content-identical to current Home outputs but are regular files rather than symlinks; changing them is outside this read-only closeout.
