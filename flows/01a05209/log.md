# Wispr Flow client packaging on NixOS

Remembered: 01a04e75 — depth 1. The prior flow designed Listener's provider boundary around Wispr-first transcription with OpenAI fallback, then implemented a mocked vertical slice; real Wispr interoperability, credentials, downstream NixOS activation, and main integration remained open.

Working interpretation: “Nixon's” means NixOS and points to the existing unofficial `wispr-flow-linux` Electron repackaging repository, independent from Listener; no literal local “Nixon” referent was found. The repository already exports bare and FHS Nix packages plus desktop and udev artifacts, but the default Nix build is currently broken by a fake, stale helper pin; its Nix path applies only part of the required patch set and deliberately omits Linux replacements for Windows native modules. The proprietary Windows installer remains a user-supplied impure input.

Likely realization boundary: repair and prove the package in `wispr-flow-linux`, then consume it as an opt-in CriomOS/Home package while keeping Listener's provider architecture and bindings separate. NixOS owns the udev/uinput capability; Home owns the desktop package. Do not infer autostart or overlapping hotkeys.

Correction: the living wants personal use of the Wispr client they pay for. The earlier flow incorrectly turned an unknown about redistribution authority into a gate on local realization. The technical boundary is a local, user-supplied-installer build; nothing is hosted or redistributed.

Ruled work: repair and prove the existing `wispr-flow-linux` Nix package, integrate it as an opt-in local desktop package with declaratively owned input capabilities, keep it independent from Listener, and activate it for personal use.

Package realized: public fork `LiGoldragon/wispr-flow-linux`, bookmark `fix/nix-runtime`, commit `5a73a4be482d4cb6686352bb963801845c001db9`. The source-only repair pins helper v0.1.2 and ABI-146 Linux SQLite modules, applies the complete Linux patch set, removes `crypt32.node`, and preserves the Electron FHS runtime. Flake evaluation and the x86_64 runtime check passed; the complete FHS package built successfully on the configured remote builder from Wispr's official v1.6.7 full Squirrel installer. No proprietary bytes were committed or pushed.

Integration boundary settled: Home owns the explicit personal desktop package for `li`; CriomOS owns only required udev/uinput capability; Listener, autostart, and its hotkeys remain unchanged. The exact producer revision must be pinned. The proprietary installer needs a declarative user-supplied transport compatible with remote realization; environment-only `WISPR_FLOW_EXE` is not sufficient for immutable Lojix deployment.

Home/System realized: `CriomOS-home` commit `ac54e3af28d7ca3d01c58395594148040f2718a5` installs the exact Wispr package for `li`; `CriomOS` commit `9338e54c998e5a07c5ca5e66d4523201d3681645` pins that Home revision. Existing `/dev/uinput` ownership and `li`'s `uinput` membership were sufficient, so no broader `input` group or functional system-capability change was added.

Deployed without reboot through Lojix: deployment 89 Evaluate succeeded, 90 Realize succeeded, and 91 CompleteHost ActivateNow succeeded and is Current/LiveActivation on Ouranos. Live `wispr-flow` resolves from `li`'s profile; Listener remains active and unchanged.

Graphical handoff: transient user unit `wispr-flow-first-run.service` is active with bwrap/Electron and no journal error. Niri shows Wispr Flow Hub and Status windows plus the focused Chrome `Login | Wispr Flow` window. No credentials were accessed.

Runtime evidence from the living: onboarding reaches shortcut setup, but modifier shortcut capture does not register although focused Escape does; the expected purple key feedback never appears and shortcut editing cannot complete. A separate opaque pink/purple `Status` window appears as a large normal Niri window, overlaps the Hub when hovered, and tiles beside it when the Hub is fullscreen. This disproves graphical usability despite successful launch.

Current task: diagnose and repair global input capture and Linux/Wayland window behavior, then redeploy and repeat the shortcut/onboarding witness. Likely but unproved boundaries are missing read access to `/dev/input/event*` versus renderer/global-shortcut translation, and transparent always-on-top Status-window classification versus Electron/Wayland compositor behavior.

Diagnosed input: the live helper reports no readable keyboard under `/dev/input`; `li` has working `/dev/uinput` access but no readable physical keyboard event descriptor. Focused Escape uses a separate path. The narrow system repair is active-seat `uaccess` for keyboard-class event nodes, not membership in the broad `input` group.

Diagnosed window: the pink surface is Wispr's separate transparent/frameless always-on-top `Status` BrowserWindow. Wispr can expand it to the work area; Electron/Wayland loses its transparent popup behavior and Niri then treats the opaque magenta surface as a normal/tiled window. Primary repair belongs in the client Status-window state/alpha handling; a Niri floating rule is only defensive containment.

Credential witness: `/home/li/.config/Wispr Flow/session.json` exists inside a mode-0700 user-data directory; its secret value was not read or output. Wispr logs show device-code authentication, session setting, `SIGNED_IN`, device registration, and a reusable authenticated session despite incomplete onboarding.

Current task: implement, prove, pin, and deploy the keyboard ACL and Status-window repairs; preserve the authenticated session and repeat the living's onboarding test.

Repairs landed: producer `9e991e50b1b281abbeaf7e2f29550bab50e4f828` adds and verifies the Status BrowserWindow transparent background and passes Bats, Prometheus checks, flake evaluation, and the official-v1.6.7 remote FHS build. Home `6201c493e80a8618d8cefd26227e21f80b80c2a6` pins it. CriomOS combined commit `e3c9d71441434f13995f8720ff81ce774db2c2e7` adds keyboard-class-only active-seat uaccess and pins Home. The rendered contract excludes generic event access and `GROUP=input`; the full immutable Ouranos target realized successfully. The aggregate check remains blocked before its Wispr body by the preexisting MS2130 kernel assertion.

Deployment blocker: Lojix 92/93 were rejected before effect because active Lojix 0.19.2 uses Horizon `c70915…`, whose legacy ClusterProposal parser intentionally rejects removed `AgentIntercomLocal`/`AgentIntercomGraphical` variants in the stale `goldragon/datom.dotos`. Canonical goldragon authority has migrated to `proposal.datomic`, but deployed Lojix accepts only legacy `.dotos`. No existing valid Ouranos proposal source exists. A generated legacy duplicate would be a backward-compatibility path; the terminal repair is to migrate Lojix to consume canonical `proposal.datomic`, which is broader than the Wispr round and needs the living's ruling.
