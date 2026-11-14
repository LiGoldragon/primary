# zeus: the Flow MemoryMax stub unit removed

The unguarded `MemoryMax=3G` / `MemorySwapMax=0` fragment is now part of the Nexus unit's own declaration, so a Home without the unit no longer generates the stub. CriomOS-home main is 39c86609, CriomOS main is 949c4508, and zeus runs it as Lojix deployment 576. ouranos needed no switch. Work files are in `/home/li/primary/flows/565bc8/zeus-stub/`; paths below are relative to it. This flow had no Skill tool, so knowledge:lojix and knowledge:criomos-deploy were not loaded.

## The change

- `modules/home/profiles/min/flow-nexus-place.nix` gains the option `memoryLimit` (null, or `{ maximum swapMaximum }`). The unit's Service merges `MemoryMax` and `MemorySwapMax` from it, inside the module's single `config = lib.mkIf (sizeAtLeast "Min" && cfg.enable)` block. The condition is written once.
- `modules/home/profiles/min/flow-0550.nix` drops its `systemd.user.services.${unit}.Service` fragment and sets `memoryLimit = { maximum = "3G"; swapMaximum = "0"; }`. The values are unchanged.
- Commit 39c86609 on branch `zeus-flow-stub-565bc8` (worktree `/git/worktrees/CriomOS-home-zeus-stub-565bc8`), branched from 20d46eda and pushed to main as a fast-forward.
- CriomOS: `nix flake update criomos-home` moved exactly the criomos-home node (3 lines), commit 949c4508 (worktree `/git/worktrees/CriomOS-zeus-stub-565bc8`), pushed to main as a fast-forward from 63e95f1.

## Builds (on prometheus, `build-*.log`)

| host | live Home | new Home, Home override on CriomOS 63e95f1 | pushed CriomOS 949c450, no override |
|---|---|---|---|
| ouranos | rpvdvc5s | rpvdvc5s | rpvdvc5s |
| zeus | 24459mp9 | jlyfa1mj | jlyfa1mj |

- **ouranos is byte-identical:** the new build is the same store path as the live generation, so the flow-nexus-0550 unit keeps its 3 GiB and zero swap. Nothing was switched on ouranos.
- **zeus differs only by the stub:** `nix store diff-closures` reads `flow-nexus: 0550.service → ∅`. `diff -rq` of the two generations shows the removed `home-files/.config/systemd/user/flow-nexus-0550.service` (content: the two memory lines only) plus the three files that name the home-files path (activate, bin/home-manager-generation, putter.json). See `zeus-diff.txt`.

## zeus switch (`zeus/`)

- Requests are release-0562's with only the CriomOS rev changed to 949c450.
- Realize 575 Succeeded, ActivateNow 576 Succeeded (`zeus/realize-*`, `zeus/activate-*`). Lojix Current is jlyfa1mj at CriomOS 949c450.
- Rollback: `zeus/rollback-request-0562.datom`, the ActivateNow at CriomOS 63e95f1 (the previous live Home 24459mp9).

## Verification on zeus (`zeus/before.txt`, `zeus/after.txt`, `zeus/after-reload.txt`)

- **Before:** flow-nexus-0550.service LoadState=bad-setting, inactive (`before-zeus-stub-state.txt`, read before the switch).
- **After:** the home-manager profile is jlyfa1mj; LoadState=not-found; no flow-nexus-0550.service file in `~/.config/systemd/user`; no flow-nexus unit listed; `systemctl --user --failed` is empty; the user manager is `running`; `flow-nexus --version` answers 0.56.2.
- **Reload error:** the activation's own reload (06:01:37) and three explicit `daemon-reload`s (06:01:46, 06:01:51, 06:01:53) all finished with no "Refusing" line. The two earlier "Service has no ExecStart ... Refusing" journal lines (05:55:37 and 05:56:46) are from user-manager instances started before the activation.

## Not done

- ouranos's other modules and Orchestrate's pre-versioned memory file on zeus (the other triage finding) are untouched.
- The CriomOS-home main checkout `/git/github.com/LiGoldragon/CriomOS-home` is dirty with another flow's work and was not touched; the work was done in the worktrees above, both equal to their mains.
