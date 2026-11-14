# Deployment 253: the Home base made coherent

Psyche criomos Secondary 44b777, owner of the Home deployment, 2026-11-06.

## Branch heads, published (origin equals local)

- CriomOS criomos-audit-fixes-b2e257: c9a0240c7afc2a9b30d6bbb26bbbfc804dd022c9; it pins CriomOS-home 9e2d259c13f391ba0701d595864a798f661f6473 in flake.lock
- CriomOS-home criomos-audit-fixes-b2e257: 9e2d259c13f391ba0701d595864a798f661f6473
- Neither branch is merged: origin/main is CriomOS 88dc887 and CriomOS-home 6f6eec61

## The failures before 253

- 251 failed at the Home Manager link check: hand-made zoekt-index.service, zoekt-index.timer and the timer's wants link were in the way. b2e257 removed them; copies are in flows/b2e257/removed.
- 252 failed at nix profile add: a nixpkgs zoekt installed by hand on 2026-11-05 (profile history version 15) collided with the declared home-manager-path. The 249 path had already been removed, so from about 11:43 to 11:45 ~/.nix-profile held only zoekt. I removed that hand package with nix profile remove zoekt.

## Raw terminals

```
Queried.{ [] [ { 251 251 { UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.c9a0240c7afc2a9b30d6bbb26bbbfc804dd022c9 } Some.{ 5582 5582 } Failed Some.{ 5606 5606 } Some.Failed.{ Activate ActivationFailed Some.{ Some.{ /nix/store/yfx9hw7baha19mr47z29fhlv0510p10b-home-manager-generation/activate [] Some.1 } «» False } } } ] { 5677 5677 } }
Queried.{ [] [ { 252 252 { UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.c9a0240c7afc2a9b30d6bbb26bbbfc804dd022c9 } Some.{ 5611 5611 } Failed Some.{ 5635 5635 } Some.Failed.{ Activate ActivationFailed Some.{ Some.{ /nix/store/yfx9hw7baha19mr47z29fhlv0510p10b-home-manager-generation/activate [] Some.1 } «nix profile remove /nix/store/rzvd4ai0q5zn14acq3c055bcl7l1xhl7-home-manager-path
removing 'home-manager-path'
removed 1 packages, kept 1 packages
warning: 'install' is a deprecated alias for 'add'
error: An existing package already provides the following file:

         "/nix/store/24xg4gclxhqzxpslhdj9n6w8zqysi6f7-home-manager-path/bin/zoekt-sourcegraph-indexserver"

       This is the conflicting file from the new package:

         "/nix/store/8394kig12g3vvbfx7r79hzsgic6d2w8c-zoekt-0-unstable-2026-03-25/bin/zoekt-sourcegraph-indexserver"

       To remove the existing package:

         nix profile remove home-manager-path

       The new package can also be added next to the existing one by assigning a different priority.
       The conflicting packages have a priority of 5.
       To prioritise the new package:

         nix profile add flake:nixpkgs#legacyPackages.x86_64-linux.zoekt --priority 4

       To prioritise the existing package:

         nix profile add flake:nixpkgs#legacyPackages.x86_64-linux.zoekt --priority 6» False } } } ] { 5677 5677 } }
Queried.{ [ { 253 253 goldragon ouranos UserEnvironment LiveActivation Current Some./nix/store/yfx9hw7baha19mr47z29fhlv0510p10b-home-manager-generation Some.c9a0240c7afc2a9b30d6bbb26bbbfc804dd022c9 } ] [ { 253 253 { UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.c9a0240c7afc2a9b30d6bbb26bbbfc804dd022c9 } Some.{ 5640 5640 } Completed Some.{ 5673 5673 } Some.Succeeded } ] { 5677 5677 } }
```

## Live proof after 253

```
home-manager profile: /nix/store/yfx9hw7baha19mr47z29fhlv0510p10b-home-manager-generation
gcroot current-home: /nix/store/yfx9hw7baha19mr47z29fhlv0510p10b-home-manager-generation
generation home-path: /nix/store/24xg4gclxhqzxpslhdj9n6w8zqysi6f7-home-manager-path
Store paths:        /nix/store/24xg4gclxhqzxpslhdj9n6w8zqysi6f7-home-manager-path
generation home-files: /nix/store/6syxdyk38h1mfykwvw27rq5kd0g5wbqv-home-manager-files
home-files entries linking outside that path: 0
failed user units: 0
MainPID=1069499
ExecMainStartTimestamp=Fri 2026-11-06 11:10:04 CST
flow-nexus-0511.service: byte-identical to the 249 home-files 2lfpkp4dh7vig7ig1nrwdfy8dn1j2hy2
DropInPaths=/home/li/.config/systemd/user/curriculum-nexus.service.d/50-declared-runtime.conf
MainPID=1280854
ExecMainStartTimestamp=Fri 2026-11-06 11:45:26 CST
Fri 2026-11-06 11:57:56 CST 10min Fri 2026-11-06 11:42:56 CST 4min 13s ago zoekt-index.timer zoekt-index.service
```

The four hand Curriculum drop-ins (70, 80, 85, 90) are removed, with copies in flows/44b777/removed. The effective unit is the same before and after the daemon-reload. The transcript is ~/.claude/projects/-home-li-primary/44b7778d-d651-5ba7-95ef-2c3b40d59aa2.jsonl, and the predecessor's is b2e257c1-2e49-5df0-971f-849f6642505b.jsonl in the same directory.
