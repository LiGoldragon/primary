# Vision and history

This is a carried account from `/root/vision_and_history`, transcript thread `01a07139-76f6-7370-9ec1-6563bbd3d6f4`, completed at ordinal 656. The historical claims were witnessed from source history and the current vision; motive and authorization claims remain unknown unless explicitly stated.

## Current written vision

`flows/0062e8/vision/live-installation-image.md:3-27` asks for a USB installer node with allowed SSH keys, possibly SOPS, an encrypted non-root login, TTY-only minimal tooling, a deterministic synthetic name, and an external additional input to Lojix. The related `flows/01a0338f/vision/mediumGraphicalNodes.md:9-12` records an earlier graphical-node role and asks for current gate review. No transcript evidence was found for the literal term “preOS”; the transcript CLI was unavailable to this witness.

## Historical predecessor

The archived `criomos-archive` history gives direct precedent for an implicit installer node. Commit `a222d3da5e15` (2022-10-07) added `implicitNodes.nix` with a deterministically named `liveIso-x86-64-small` node and changed proposal construction to merge `explicitNodes // implicitNodes`. The node was later normalized to `species = "hybrid"; size = 1; machine.species = "metal"; machine.arch = "x86-64"`.

The old `nix/mkCriomOS/default.nix` selected `liveIso.nix` when `behavesAs.iso`, emitted `isoImage`, and excluded edge, router, metal, and desktop modules on ISO. Its ISO package branch included `openssh`, `ntfs3g`, `fuse`, `btrfs-progs`, `dosfstools`, `parted`, `nmap`, `vim`, and `htop`. It still enabled zsh, and `liveIso.nix:16` set `root.initialPassword = "r"`. The historical module did not implement the requested encrypted non-root login or allowed-key provisioning.

## Removal and successor timeline

Commit `b6fc86d63ef8` (2026-03-22) changed the archived `implicitNodes.nix` to `{}`. The same commit added an “asklepios rescue ISO” and retained the ISO module. This pins when the populated implicit node disappeared; it does not establish motive, approval, or that the requested design was rejected.

CriomOS commit `eff6eea67de3` (2026-04-23) copied `liveiso.nix` into the canonical rewrite without copying a populated implicit node. Commit `d519611760a0` (2026-04-24) deleted `zones/` and `sphere/`, including the empty `zones/implicitNodes.nix`, while recording that the in-Nix Horizon layer was superseded by `horizon-rs`. Phase8 commits `febf8560e5ea` and `0ea97eab988a` explicitly record `disks/{liveiso,pod}` as skipped alternative-target modules. Current `CriomOS/modules/nixos/criomos.nix` imports `disks/preinstalled.nix` and does not import `liveiso.nix`.

## Current boundaries and tensions

Current Horizon derives `behaves_as.iso` from `!virtual_machine && io_disks_empty`. `ClusterProposal::project` requires the viewpoint node in `self.nodes` and projects only that set; no default-node merge exists. Lojix accepts a request-supplied `proposal_source`, reads and projects that proposal directly, and has no external synthetic-default input slot.

The old `Hybrid` ISO cannot be restored unchanged as the new design: current edge facilities are gated by `behavesAs.edge`, and the old Hybrid ISO would satisfy that gate unless an explicit ISO exclusion or non-edge synthetic species is added. Current deployment defaults retain `includeHome = true`, which conflicts with a GUI-free minimal image unless the image receives a distinct deployment shape.

**Inference:** the requested `preOS` shape is analogous to the historical `liveIso-x86-64-small` precedent, but the names are not proven equivalent. The current architecture should preserve the historical merge idea only after defining the new external Lojix boundary, explicit installer kind, credentials, and image output.

The principal agreement is that the requested synthetic installer shape has direct historical precedent and that Horizon-rs/Lojix are now the intended ownership boundary. The principal tension is that the populated historical node and merge mechanism are gone, the ISO module survives only as an unreachable alternative-target file, and current Lojix/Horizon provide no external-default merge path.

## Sources

- `/home/li/primary/flows/0062e8/vision/live-installation-image.md:3-27` — current written vision.
- `/home/li/primary/flows/01a0338f/vision/mediumGraphicalNodes.md:9-12` — related written vision.
- `/home/li/git-archive/github.com/LiGoldragon/criomos-archive`, commits `a222d3da5e15` and `b6fc86d63ef8` — implicit node, merge, removal, and rescue ISO history.
- Archive `nix/mkCriomOS/default.nix`, `nix/mkCriomOS/liveIso.nix`, and `nix/mkCriomOS/normalize.nix` — historical image selection, exclusions, credentials, and package branch.
- `/git/github.com/LiGoldragon/CriomOS`, commits `eff6eea67de3`, `d519611760a0`, `febf8560e5ea`, and `0ea97eab988a` — canonical rewrite and skipped alternative-target history.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/criomos.nix`, `normalize.nix`, and `edge/default.nix` — current imports and gates.
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs` and `lib/src/horizon.rs` — current ISO heuristic and viewpoint projection.
- `/git/github.com/LiGoldragon/lojix/src/runtime_flow.rs`, `src/bootstrap.rs`, and `README.md` — current proposal-source boundary.
