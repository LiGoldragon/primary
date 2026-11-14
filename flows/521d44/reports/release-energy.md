# Energy Nexus 0.4.0 (contracts 0.6.0) released and switched on ouranos

Energy Nexus 0.4.0 is live on ouranos. Activation was Lojix deployment 578, between 2026-11-14T10:03:04-06:00 and 10:04:34-06:00. The Energy units were restarted at **2026-11-14T10:04:30-06:00**. Nothing needed rolling back.

**Niri, Noctalia and the screen locker did not restart.** Their PIDs are the same before and after (niri.service 2832, app-niri-noctalia-3122.scope 3122, criomos-lock-listener.service 5933), and no other service's MainPID or start time moved. Only energy-nexus.service and energy-translator.service did (`release-energy/after/service-mainpids.diff`).

Evidence is in `/home/li/primary/flows/521d44/release-energy/`; paths below are relative to it.

## Mains (all fast-forwards; each main was as prepared when checked)

| repository | before | main now |
|---|---|---|
| signal-energy-nexus (0.6.0) | 7ca10eb | **8c861ec2b52be29f13c616c3501557bc38708d22** |
| meta-signal-energy-nexus (0.6.0) | 3264d6f | **24958c7417d251525c7823c3c0ca91ff51401b9c** |
| energy-nexus (0.4.0) | 2623947 | **aafd0ebdfae570614b61f6b62c547739c2a8bedf** |
| CriomOS-home | 39c86609 | **018691de31637646fa007b1798bd7ac98f4510e7** (only the energy-nexus lock node) |
| CriomOS | 949c450 | **cee786aa2aab9d7cbba5e6400b9db513888454f4** "Release Energy 0.4.0 (521d44): energy-nexus aafd0eb on CriomOS-home 018691d" |

- Push log: `push-producers.log`. The CriomOS push was `949c450..cee786a`. Its `flake.lock` change is 6 lines: the `criomos-home` node and its `energy-nexus` node, nothing else. Worktree `/git/worktrees/CriomOS-energy-521d44` (branch `energy-release-521d44`).
- CriomOS-home main was moved from the existing worktree `/git/worktrees/CriomOS-home-energy-565bc8` (branch `energy-565bc8` is now equal to main).

## Home builds from the pushed CriomOS cee786a, no criomos-home override (`before/`)

Built on prometheus with each host's live deployment inputs (`scripts/home-build-nooverride.sh`).

- ouranos: **`/nix/store/czmfd0pmdr6zh9alw4wx26hv2y52ymaa-home-manager-generation`**, the expected path (`before/home-build-ouranos-cee786a....log`).
- zeus: `/nix/store/jlyfa1mjpzd7a7769ap5a20ymn6drp37-home-manager-generation`, **equal to zeus's live generation**: `readlink -f ~/.local/state/nix/profiles/home-manager` on zeus gives that path, and Lojix's Current on zeus is 576 at that path. No closure diff, **no zeus switch is needed**, and none was made (`before/home-build-zeus-cee786a....log`).

## Before the switch (`rollback/`, `before/`)

- Rollback request: `rollback/lojix-ouranos-rollback-request.datom`, an ActivateNow at CriomOS 949c4508a3765a8225a288b36bf4d1718573d64b (the live Home rpvdvc5s is in the store).
- Energy state, copied at 10:01 with `cp -p`; each copy's sha256 equals its source (`rollback/state-sha256.txt`):
  - `~/.local/state/nexus/main/energy.rkyv`, 617470 bytes, `925a9d3c...5ac`; envelope format version 2.
  - `~/.local/state/nexus/main/energy-translator.rkyv`, 142 bytes, `7c2385a7...5864` (the digest the store proof also gave).
- User units: 145 active units (`before/user-units-active.txt`); MainPIDs of the 51 active services in `before/service-mainpids.txt`. Niri 2832 (started Nov 11 18:13:40), criomos-lock-listener 5933, Noctalia scope 3122. ouranos has no separate idle unit: the locker is `criomos-lock-listener.service`, which forwards logind lock requests to Noctalia.
- One failed user unit already existed: `context-skills.service` (`before/failed-before.txt`). It is not Energy's.
- Lojix Current before: 572 (rpvdvc5s, CriomOS 63e95f1); home-manager profile link 1159.

## The switch (`ouranos/`)

| step | deployment | result |
|---|---|---|
| Realize at cee786a | 577 | Succeeded (`ouranos/realize-*`) |
| ActivateNow at cee786a | **578** | Succeeded, phases Submitted, Building, Copying, Activated, Completed (`ouranos/activate-*`) |

Lojix Current now: generation 578 at czmfd0pm..., CriomOS cee786a (`after/lojix-current.txt`). The home-manager profile link moved from 1159 to 1160.

## Readback (`after/`)

- **Generation:** `~/.local/state/nix/profiles/home-manager` resolves to czmfd0pmdr6zh9alw4wx26hv2y52ymaa-home-manager-generation. `~/.nix-profile` holds the new home-path (`158whd0f...-home-manager-path`, which carries `energy-nexus-daemon`). All 200 entries of the generation's home-files resolve to the same file in `$HOME` (0 mismatches) (`after/home-readback.txt`).
- **Units:** energy-nexus.service (MainPID 1203237) and energy-translator.service (1203231) are active, started 10:04:30, running `/nix/store/vpzq0cxd...-cargo-package-0.0.1` (the old one was `jdap7bz9...`). The `energy-nexus` client resolves to the same package.
- **Store:** `energy.rkyv` is now envelope format version 3 (`ENXMEMRY` then `03 00 00 00`; the file before had `02 00 00 00`). The daemon's journal line at first start: `energy-nexus: /home/li/.local/state/nexus/main/energy.rkyv upgraded from format version 2` (`after/journal-energy.txt`). New size 620020 bytes, sha256 `c693bd74...0e30`. `energy-translator.rkyv` is byte-identical to before.
- **Readings:** `energy-nexus Read.Claude` and `Read.Codex` both answered a `Read.{ ... }` with a reading and its pace (`after/read-Claude.txt`, `after/read-Codex.txt`). Claude: Week 4 used, FableWeek 0, pace Over/Under 165 hours left. Codex: Week 41 used, pace Over 106 hours left, three reset credits Available.
- **Failed units:** none after the switch (`after/failed-after.txt` and `failed-final.txt` are empty); the earlier `context-skills.service` failure is gone from the list.

## Units the activation touched (`after/units-touched.txt`, from the user journal)

- Stopped and started again: `energy-nexus.service`, `energy-translator.service` (the daemon binds to the translator).
- `systemctl --user daemon-reload` by `sd-switch` (80 ms).
- Run once and finished (oneshots): `criomos-ui-priority.service` (10:04:30 to 10:04:33; it lists niri.service, Noctalia and Mako scopes, pipewire and others as protected and sets their resource priority; it restarts none of them) and `set-SSH_AUTH_SOCK.service`.
- Nothing else was stopped, restarted or started.

## Observed, not caused by this release

- Anthropic's usage endpoint answered `429` with `retry-after` 0 at 10:04:33 and 10:04:47. The new translator logged `energy-translator: Claude reading failed: { Refused Some.429 Some.0 }` and the daemon answered `Read` from the reading it held (`Claude reading failed; answering with the reading held, 3 seconds old`). That is the fault fix working as designed: before it, this answered `ProviderDown`. A retry-after of 0 withholds nothing, so the daemon asks again on the next read. The Claude reading in `Read.Claude` was taken at 10:04:30 (the first read at start); a later reading depends on that endpoint answering.

## Left as is

- Worktrees `/git/worktrees/CriomOS-energy-521d44` and the Energy ones from prep remain; branches `ethos-565bc8` (three repositories) and `energy-565bc8` are equal to main. Flow, Curriculum and every other unit are untouched.
- The rollback request is unused; the old Energy state copy is kept in `rollback/` (note it is format version 2, readable only by 0.3.x).
