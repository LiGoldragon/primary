# Designer handoff — Mentci deploy/theme/prototype

## Current state

- `mentci-egui` exists and is already reframed as a **thin egui client** of the Mentci daemon.
- `mentci-lib` owns the client-side MVU observation/control model (`ObservationModel`, `EngineEvent`, `UserEvent`, `Cmd`, `ObservationView`) and NOTA fallback rendering.
- `mentci-egui` `ARCHITECTURE.md` says the app sends `ObserveInterfaceState` on first frame and renders replies in a transcript; meta mode is currently a visible placeholder until the daemon meta surface lands.
- `mentci-lib` `INTENT.md` already says thin clients must not open Criome directly; answers route back through the Mentci daemon.

## Design translation of the psyche request

- Treat this as the **start of usable Mentci**, not just a sandbox demo.
- Writing mode = meta mode. Ordinary mode is observation/light operations.
- Make the app available from the OS profile and ensure it follows system light/dark theme.
- Keep designer work on a prototype branch/worktree; do not turn `mentci-egui` into the state owner.

## Likely files/repos

- `/git/github.com/LiGoldragon/mentci-egui/src/main.rs`
- `/git/github.com/LiGoldragon/mentci-egui/src/app.rs`
- `/git/github.com/LiGoldragon/mentci-egui/src/daemon_client.rs`
- `/git/github.com/LiGoldragon/mentci-lib/src/`
- CriomOS-home profile/module that installs desktop apps and GUI defaults.

## Work items

1. Add a real light/dark theme path in `mentci-egui`, preferably reading OS/portal/desktop color-scheme when available.
2. Add explicit mode labels: observation/light operations vs meta/write mode.
3. Package/install the current `mentci-egui` as an available test surface on the local profile.
4. Keep all approval, Criome bridge, and durable state in daemon/lib surfaces, not egui.
5. Add a visible “connected component/channel” header: Mentci, MetaMentci, future Criome, MetaCriome.

## Validation

- `cargo test` in `mentci-egui` and `mentci-lib`.
- Launch the app with both light and dark settings; screenshot/visual witness preferred.
- Verify no direct `signal-criome` socket access was added to `mentci-egui`.

## Compact implementation prompt

Implement a prototype branch making `mentci-egui` deployable and theme-aware. Keep it a thin client of `mentci-lib`; add ordinary observation/light-operation vs meta/write mode labels; make it follow the system light/dark preference or an app-level fallback; package it through the relevant local profile. Validate with cargo tests and a live launch witness.
