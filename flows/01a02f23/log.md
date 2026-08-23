# Realization flow

Remembering Orca design flow `01a02a72`; researching Herdr and Orca packaging and installation, then updating both Claude and Codex from authored sources.

## 2026-08-23

- Flow opened from the living's request to remember `01a02a72`, research how Herdr and Orca should be packaged or installed, and update both Claude and Codex.
- The current edit-coordination examples were corrected from the stale generated skill syntax using the existing `01a02a34` witness. Registration and claims reached transport, but the coordination socket was absent; work continues with disjoint subflow ownership.
- Remembered: 01a02a72 — depth 1.
- The light current-state check retained Orca's prior control-plane and mailbox/context boundary, found stable `v1.4.188`, confirmed that nixpkgs still has only GNOME Orca, and identified an evaluated but not build-smoked `orca-ide` AppImage wrapper candidate.
- Packaging research identified Herdr `v0.8.2` with an official flake and nixpkgs package, plus upstream Claude and Codex hook installers. The local bridge remains on pre-breaking-change `v0.7.4`; upgrading it requires a CLI migration.
- `reports/agentHarnessPackaging.md` records the combined package evidence and recommends declarative ownership in CriomOS-home: pinned Herdr separately from the bridge, and an `orca-ide` stable-AppImage package after behavioral smoke proof.
