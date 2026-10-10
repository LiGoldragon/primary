# MiniDox Bootloader Entry Evidence

Task and scope: implement the approved `/git/github.com/LiGoldragon/kibord` MiniDox first-firmware safety changes without flashing or resetting hardware. Scope included restoring a deliberate `leader r e s e t` bootloader-entry path, adding a tucked-away `QK_BOOT` fallback on `ADJUST`, documenting build and pre-flash safety, and including the requested number-output ordering behavior without broader layout redesign.

Files and commands consulted:

- `/home/li/primary/AGENTS.md` from the prompt.
- `/home/li/primary/.agents/skills/code-implementation/SKILL.md`.
- `/home/li/primary/.agents/skills/edit-coordination/SKILL.md`.
- `/home/li/primary/.agents/skills/version-control/SKILL.md`.
- `/home/li/primary/.agents/skills/repository-closeout/SKILL.md`.
- `/git/github.com/LiGoldragon/kibord/README.md`.
- `/git/github.com/LiGoldragon/kibord/flake.nix`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/{keymap.c,config.h,rules.mk}`.
- QMK docs pages for Leader Key, Quantum Keycodes, and Flashing.
- QMK 0.33.8 upstream MiniDox default keymap source.
- `jj status --no-pager`, `jj diff --stat --no-pager`, `jj show -r main --stat --no-pager`.

Observed facts:

- The repo had no local `AGENTS.md`.
- Initial `jj status --no-pager` in `kibord` was clean.
- Orchestrate and meta-orchestrate claim attempts could not acquire a lane claim because the local Orchestrate service refused normal reads or rejected the meta observe shape.
- The MiniDox keymap target is `maple_computing/minidox/rev1` with keymap directory `maple_computing/minidox/LiGoldragon`.
- The existing MiniDox `RAISE` row already used `KC_1` through `KC_0` in conventional left-to-right source order. The implementation preserved those physical positions and documented that as the intended first-flash number behavior.

Changed files:

- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/rules.mk`: enabled QMK Leader with `LEADER_ENABLE = yes`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/config.h`: added leader timeout and per-key timing for a five-key reset sequence.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`: added `QK_LEAD` on `ADJUST` left home-row pinky, added `QK_BOOT` on `ADJUST` left bottom-row pinky, and implemented `leader r e s e t` with `reset_keyboard()`.
- `/git/github.com/LiGoldragon/kibord/README.md`: documented `nix build .#minidox`, the number-row ordering, the leader reset sequence, the direct `QK_BOOT` fallback, the no-flash status, and the unverified Pro Micro/Caterina physical reset fallback.

Verification:

- `nix build .#minidox`: passed. This built the MiniDox firmware derivation and produced the expected build output without flashing or resetting hardware.
- `jj status --no-pager` after closeout: clean working copy in `/git/github.com/LiGoldragon/kibord`.
- `jj git push --bookmark main --dry-run` after push: `main@origin` already matched `main`; nothing changed.

Commit and push:

- Commit: `c71c7787338f0ed76dc5d16547f6c9e971ba767c`.
- Bookmark: `main`.
- Remote state: `main@origin` matched `main` after push.

Remaining warnings:

- No hardware was flashed or reset.
- The physical MiniDox controller, bootloader, half selection, and actual reset procedure remain unverified.
- The Pro Micro/Caterina physical reset fallback is documented as inferred from QMK guidance, not as a verified procedure for this specific keyboard.
