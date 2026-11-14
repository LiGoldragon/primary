# What Nix decides by node or user name (audit finding 3), for a later ruling

Read at CriomOS c9a0240 and CriomOS-home 9e2d259c (branches criomos-audit-fixes-b2e257). Nothing here was changed.

## CriomOS, modules/nixos/userHomes.nix

| Line | Decision | Name read |
|---|---|---|
| 14-33 | recorded Zeus Home adoption: literal home-files, herdr-config and Kvantum store paths per user | zeus, per user |
| 51 | criomosHome.herdr takes that adoption | node zeus |
| 54 | criomosHome.curriculum.enable | node ouranos and user li |
| 56 | criomosHome.codexNextCandidate.enable off | node zeus |
| 75 | home-manager-<user> TimeoutStartSec 20min | node zeus |
| 78 | which users that timeout covers | users bird, li |

The landing deploy request (old line 59-65, node ouranos, user li, a full Deploy.UserEnvironment with goldragon, a store path and a secrets path) is removed on the branch with the 0.39 unit it served.

## CriomOS-home

| File:line | Decision | Name read |
|---|---|---|
| modules/home/profiles/min/flow.nix:19 | criomosHome.flow.enable default | username li |
| modules/home/profiles/min/flow-nexus-version.nix:244 | each Flow Nexus version's enable default | username li |
| modules/home/profiles/min/codex-next.nix:11-12 | birdTarget and occupied | user bird, /home/bird; user li, /home/li |
| modules/home/profiles/min/codex-remote-control.nix:20-21 | the same two | the same |

Each becomes a Horizon role or capability field once ruled.
