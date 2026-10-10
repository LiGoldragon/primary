# Vision map

Method: code read `/home/li/primary/flows/01a02b4b/log.md`,
`/home/li/primary/flows/01a02b4b/reports/chromaCorrectiveProof.md`,
`/home/li/primary/flows/01a02b4c/reports/chromaEmacsReacquisition.md`,
`/home/li/primary/flows/01a0238b/vision/emacsPlugin.md`,
`/home/li/primary/flows/01a02b4b/vision/emacsPlugin.md`, and
`/home/li/primary/flows/01a02b4b/vision/homeEquivalence.md`.

Observed from the written psyche: the plugin is a standalone public repository
and a CriomOS-home input (`01a0238b/vision/emacsPlugin.md:3-9`); D-Bus and
Home-owned Ignis generation were selected (`:17-29`); the public repository,
feature/mode, revisioned desired snapshots, typed acknowledgements, consumer
statuses, bounded Lisp failure, overlay preservation, and Home end-to-end
witness were approved as an implementation shape (`:37-50`). Flow
`01a02b4b` records only superficial implementation approval for inspection
(`01a02b4b/vision/emacsPlugin.md:3-11`). The later Home ruling requires no
difference between embedded and independent Home, shared logic from Horizon or
Horizon-only machinery, and only a minimal embedding wrapper
(`01a02b4b/vision/homeEquivalence.md:3-20`).

Method: code read `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`,
`src/daemon.rs`, `src/state.rs`, and `src/theme.rs` at Chroma `main`
`6a8e4c6a` on 2026-08-23.

Observed: Chroma has one typed `ThemeMode`; `StoredThemeState` persists mode
and revision; `ChromaRoot` restores it, allocates a checked next revision,
persists before publishing, and owns `ThemeProjection`; the daemon starts the
session service before its UDS loop (`daemon.rs:60-68,123-193,231-246`). The
service constants and interface are centralized (`theme_dbus.rs:20-31`),
registration binds the unique sender and returns a snapshot
(`theme_dbus.rs:163-205,293-305`), reports validate bounded failure values and
current/stale revisions (`:95-142,208-226`), owner loss becomes `Unavailable`
(`:229-246`), and the public methods/signal are fixed (`:293-345`). Theme
fanout now has Terminal, Desktop, Ghostty, and Pi concerns only
(`theme.rs:487-602`); no Emacs concern remains.

Method: code read `/git/github.com/LiGoldragon/chroma-emacs` at `main`
`119a2313` on 2026-08-23.

Observed: the package advertises Home-supplied Light/Dark theme symbols and a
resident global mode (`README.md:1-18`); it documents the inspection D-Bus
surface and explicitly disclaims permanent wire finality (`README.md:20-32`).
The client subscribes before registering and reconnects after owner changes
(`lisp/chroma-theme.el:49-95,260-300`), rejects stale revisions before state
normalization/mutation, reapplies duplicates, verifies exact Chroma theme
membership/order, preserves unrelated overlays, and sends only bounded typed
failures (`:120-228,230-258`).

Method: code read `/git/github.com/LiGoldragon/CriomOS-home` at `main`
`a61b02d0` on 2026-08-23.

Observed: Home pins Chroma and `chroma-emacs` (`flake.nix:143-152`), uses one
Emacs package set for program and service and includes the plugin
(`modules/home/profiles/med/emacs.nix:14-20,109-117,794-803`), installs
Home-generated Ignis files (`modules/home/base.nix:97-106,143-156`), and
declares the symbols/load path plus global mode in Home init
(`modules/home/emacs/chroma-theme-init.el:1-11`,
`modules/home/profiles/med/emacs.nix:313-317`). Chroma's generated DOTOS
concerns exclude Emacs and contain no direct Emacs adapter
(`modules/home/profiles/min/chroma.nix:107-126`). The resident check starts a
real Chroma daemon and Emacs daemon under a private bus, checks generated theme
artifacts/native-init/package identity, and witnesses late startup, theme
transitions, Chroma restart, and Emacs restart (`checks/chroma-emacs-resident/run.sh:1-28,72-160`).

Method: code read `/git/github.com/LiGoldragon/CriomOS` clean parent revision
`93049a6e` and its current dirty working copy, plus
`/home/li/primary/flows/01a02b4f/reports/criomosPinAudit.md`.

Observed: Home standalone output extends the shared package set with Home
overlays before constructing `homeConfigurations`
(`CriomOS-home/flake.nix:447-455,576-603`). The clean CriomOS parent selects
raw `inputs.pkgs.pkgs` for the embedded target (`CriomOS/flake.nix:154-162`),
then exposes embedded Home activation packages and the independent Home output
surface (`:254-267`); `home-activation-equivalence.nix:11-43` compares their
store paths. Flow `01a02b4f` witnessed differing activation paths at the pinned
source and identified the overlay/package-set boundary as a likely, not proven,
cause. The current CriomOS working copy is dirty and contains an uncommitted
attempt to use the standalone Home package set (`flake.nix:155-160`) and pass
that exact `pkgs` to embedded Home (`modules/nixos/userHomes.nix:40-49`); this
is not treated as an accepted or pushed result.

Method: probe `rg -n -i
'EmacsThemeConcern|Emacsclient|emacsclient|darkman/current-mode|current-mode|CriomOS-emacs|criomos-emacs'`
over the four product repositories.

Observed: active Chroma source no longer contains the old Emacs concern; its
remaining old-name matches are negative/documentary guards. Home still has
stale ownership/planning references to `CriomOS-emacs` in `AGENTS.md:7-15`,
`ARCHITECTURE.md:6-15,34-39,139-158`, `docs/ROADMAP.md:30-34`, and
`flake.nix:442-444`. Generic `emacsclient` in Home remains for ordinary editor
and test control, not Chroma projection (`modules/home/profiles/med/emacs.nix:744-851`).

Method: code read `/home/li/primary/psyche-raw/Vision/noctalia.md`,
`setupIndependentInterfaces.md`, `everyConceptShouldHaveItsRepo.md`,
`domainKnowledgePlacement.md`, `machineAnatomy.md`,
`worldModelBeforeCode.md`, and `visuals.md`.

Observed: the broader written psyche says Chroma, not Noctalia, owns theme
authority (`noctalia.md:1-5`); general repositories use setup-independent
interfaces (`setupIndependentInterfaces.md:1-17`); each concept has its own
repository and domain knowledge lives with that domain
(`everyConceptShouldHaveItsRepo.md:1-16`, `domainKnowledgePlacement.md:1-22`);
the design artifact is an object/capability map before code
(`worldModelBeforeCode.md:3-24`); machine anatomy is inputs → coherent type →
output, with logic discoverable in one place (`machineAnatomy.md:20-48,80-110`);
visual artifacts should use Mermaid (`visuals.md:3-20`).
