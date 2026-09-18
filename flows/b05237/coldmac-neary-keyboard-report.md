# Cold Mac and Neary keyboard investigation

Date: 2026-09-18
Flow: b05237

## Result

There is no `Neary` repository, no `coldmac` file, and no literal Cold Mac
implementation in the checked repositories. The current keyboard
virtualization layer is CriomOS's per-device `keyd` configuration. It maps
only the laptop's AT Translated Set 2 keyboard to Colemak, swaps the left
Alt/Meta roles through layers, and leaves compositor/XKB globally US. This is
the strongest repository-backed explanation of the Cold Mac setup; the name
and any additional live sequence programming are not present in these trees.

## Repository survey

- `/git/github.com/LiGoldragon/` contains `CriomOS`, `CriomOS-home`, and
  `CriomOS-emacs`, but no repository named Neary/neary, Cold Mac, or keyboard.
- `CriomOS-home` has keyboard policy, Niri/Sway/Hyprland input, Colemak
  support, and Emacs configuration. It has no `keyd` service definition.
- `CriomOS` owns the system-side `keyd` service and its laptop check.
- Searches for `coldmac`, `cold-mac`, `neary`, `zfly`, `keyd`, `xkb`, and
  `keyboard` found no Neary or Cold Mac source/configuration.

## What the virtualization layer does

Current source: `CriomOS/modules/nixos/edge/default.nix:238-253`.

1. Enables `keyd` for edge hosts.
2. Targets only device ID `0001:0001`, the laptop's AT Translated Set 2
   keyboard. External/QMK Colemak boards are not remapped by this stanza.
3. Inlines keyd's shipped `layouts/colemak` into the generated config and
   selects it with `default_layout = colemak`.
4. Defines `leftalt = layer(meta)` and `leftmeta = layer(alt)`. Thus the
   physical laptop's modifier roles are normalized before applications see
   the resulting virtual key events.

The compositor is intentionally not another remapping layer. Niri uses
`layout = "us"` with `ctrl:nocaps,altwin:swap_ralt_rwin` in
`CriomOS-home/modules/home/profiles/min/niri.nix:204-209`; the Home policy
check rejects a global Colemak variant and rejects duplicate Colemak in the
Sway and Hyprland fallbacks. CriomOS's laptop check likewise requires plain
US XKB defaults and an empty X11 variant. This avoids double translation and
keeps device-specific behavior at the physical-key boundary.

The checked-in layer contains no Cold Mac-specific sequence map, navigation
cluster, or programmable-keyboard emulation. `layer(...)` proves layer-based
modifier virtualization; it does not prove that a live deployment has any
additional macros or sequences.

## Git history

The relevant design was introduced and then deliberately moved between
layers:

- CriomOS `d7f3e9d` / `ebedba3` (2026-07-02): move laptop Colemak into keyd,
  add the laptop check, preserve the Alt/Meta swap, and clear global XKB
  Colemak.
- CriomOS `2c5a317`: temporarily restored global Colemak and removed the
  keyd implementation.
- CriomOS `d7f3e9d` is the surviving keyd direction in the checked tree.
- CriomOS-home `329c93ec` / `fd0626e0`: remove compositor Colemak and add a
  policy check so keyd is the sole laptop layout owner.
- CriomOS-home `e42ca632` briefly restored compositor Colemak; `594559c3`
  and the later `329c93ec` direction returned ownership to keyd.
- CriomOS `9818e6f` (2026-08-30): admits the exact keyd virtual keyboard to
  Wispr's controlled input boundary, showing that the logical virtual device
  is an intentional system surface, not an accidental duplicate keyboard.

## Neary status

No Neary source or binding map was found, so the reported problem — that
Neary's up/down and related movement bindings are incomplete — cannot be
validated against implementation here. The flow vision records it as the
living user's observation. Treat the following as a proposal, not a claim
about current Neary code.

There is a useful local precedent: Home's Emacs profile installs
`xah-fly-keys`, selects the Colemak layout, and organizes commands into a
leader plus named prefix maps (`.../emacs.nix:347-472`). Home's Colemak
configs also use a spatial movement cluster (`h n e i` for left/down/up/right)
in tmux and ranger, though these are application-local rather than Neary
bindings.

## Frequency-first Emacs-like revamp proposal

1. Establish one canonical logical vocabulary: left/down/up/right,
   beginning/end, page movement, focus, workspace, open, close, and command
   search. Make the four movement actions the smallest, easiest cluster.
2. Use a stable spatial cluster, chosen to match the user's established
   Colemak/Zfly muscle memory. Do not guess the exact letters: derive them
   from the existing Zfly/Neary config once that source is located. The
   current application precedent is `h n e i` (left/down/up/right).
3. Put the highest-frequency actions on single keys or one held layer;
   reserve two-key sequences for less frequent actions and related families.
   Example families: movement, pane/workspace, file, and command/search.
4. Make every sequence composable and discoverable: a leader opens a
   transient map, and a help overlay displays the next valid keys. Avoid
   making common movement depend on a leader sequence.
5. Keep text insertion and application shortcuts safe. The system layer
   should own only device normalization and explicitly universal actions;
   Neary should own desktop semantics. This preserves the current no-double-
   translation boundary.
6. Add a compatibility test matrix before deployment: physical laptop,
   external QMK Colemak board, plain keyboard, Niri, terminal, Emacs, and
   Neary. Test held modifiers, repeat, up/down, focus changes, and sequence
   cancellation.
7. Instrument real use for a short period, then promote actions by observed
   frequency. The ordering should be frequency first, spatial ease second,
   mnemonic sequences third — not a large guessed keymap.

The first implementation task is therefore to locate Neary's actual source
or generated config, inventory its existing bindings and Git history, and
only then encode the shared movement vocabulary. Until then, the safe
repository-backed Cold Mac story is: keyd virtualizes the laptop's Colemak
and modifier behavior; the desktop remains plain US; application layers add
their own Emacs-like sequences.

## Sources

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/edge/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/checks/laptop-keyboard-keyd/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/keyboard-layout-policy/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/home/li/primary/flows/b05237/vision/operational-herderUserExperience.md`
- Git history inspected with `git log` and `git show` in both CriomOS repos.
