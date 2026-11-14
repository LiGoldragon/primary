# Orchestrate 0.39 and Curriculum 8881cc1, released on ouranos and zeus

Both hosts run orchestrate 0.39.0 (`ag9lqzvk…-orchestrate-0.39.0`, which serves as the Nexus and both clients) and Curriculum 8881cc1. Every Lojix deployment completed Succeeded, and nothing needed rolling back. The evidence is in `/home/li/primary/flows/2e404d/release-orchestrate/`, and the paths below are relative to it.

**Skills were not loaded.** This flow has no Skill tool, so knowledge:lojix and knowledge:criomos-deploy could not be loaded. I reused the last release's Lojix requests and scripts, changing only the revisions.

## Heads

| repo | before | after |
|---|---|---|
| CriomOS-home main | d140957 | **8e4ce433af7ef3f549098e57dacb090090defa35** (fast-forward) |
| CriomOS main | 032f84e | **64f55aef9f8592742f62c1a5e92b51a49623fe25** (fast-forward) |

- The other mains were already where the brief said and were not pushed (`mains-after-promotion.txt`).
- **CriomOS-home:** `nix flake update orchestrate curriculum-source` moved two lock nodes, and both originals stay bare URLs:
  - orchestrate, 0f99614 → ef4fe80;
  - curriculum-source, 1b6c454 → 8881cc1.
  - orchestrate's own flake inputs, rust-build and flake-utils, are unchanged.
- **CriomOS moved three nodes, not only criomos-home.** These were criomos-home, curriculum-source beneath it, and **CriomOS's own `orchestrate` input**.
  - CriomOS declares `criomos-home.inputs.orchestrate.follows = "orchestrate"`. With criomos-home moved alone, the Home still builds 0.38.0. The first build showed this: it gave fy9dq6dbg, which is the Curriculum-only generation (`before/home-build-ouranos-032f84e-8e4ce43-orchestrate-0.38-superseded.log`).
  - CriomOS's `checks/lojix-ownership` also asserts that the two orchestrate revisions are equal. Both are now ef4fe80.
- **Gates.**
  - I did not run CriomOS-home's nix-fast-build checks; they are known red on main from the codex-next.nix evaluation fault.
  - CriomOS's `lojix-ownership` check fails the same way, at `codex-next.nix:16` (`attribute 'criomos' missing`), on both 032f84e and 64f55ae (`before/check-lojix-ownership-*.log`).
  - **The Home builds were the gate.**

## Home builds (prometheus, `scripts/home-build-host.sh`; logs in `before/`)

| host | live generation reproduced | new Home (64f55ae) |
|---|---|---|
| ouranos | pkxvlf56 (032f84e) | **c7hjhgav5715gpcb426px0idg61npz08** |
| zeus | 9qgs7g1i (c521835, inputs `/tmp/offload/rmmd-zeus-home-inputs`) | **baaa2p5fng987fb0yck8svik7sfgmvm0** |

- **Overrides first, then the pushed lock.** I first built with overrides (criomos-home 8e4ce43, orchestrate ef4fe80). The pushed CriomOS 64f55ae, with no orchestrate override, rebuilt the same two paths.
- **ouranos delta** (`before/closure-diffs.txt`, `before/closure-path-diffs.txt`): only Orchestrate and Curriculum.
  - orchestrate, orchestrate-clients and orchestrate-nexus go from 0.38.0 to 0.39.0, and orchestrate-nexus.service changes.
  - Curriculum changes: rust_curriculum, its source, the curriculum unit and its runtime configuration, and the resolver check.
  - The rest are Home Manager's own wrapper derivations.
- **zeus delta:** the same, plus flow-0550's clients and flow-configured.
  - That is the previous release (flow 967f2f5), which zeus had not yet received.
  - Measured against zeus at d140957, only Orchestrate and Curriculum move.
- **One build.** In both generations, the unit's ExecStart and the `orchestrate` and `orchestrate-meta` wrappers all point into the one `ag9lqzvk…-orchestrate-0.39.0` (`before/one-build.txt`).

## ouranos

- **Rollback kept:**
  - Lojix Current was 562 (pkxvlf56, CriomOS 032f84e). The rollback request is `rollback/lojix-ouranos-rollback-request.datom`.
  - orchestrate-nexus was stopped at 03:43:28. The whole state directory was copied to `rollback/stopped-orchestrate-nexus/`, and its checksums equal the source's at the stop and after the copy (`rollback/stop-state.txt`, `*.sha256`).
  - Flow was not stopped.
- **Switch:**
  - Realize, **deployment 563**: Succeeded. It ran before the stop.
  - ActivateNow, **deployment 564**: Succeeded. Each wait read Lojix's events up to the Completed event.
  - Lojix now lists 564 as Current: c7hjhgav, CriomOS 64f55ae.
  - Orchestrate was down from 03:43:28 to 03:44:44.
- **Checks** (`after/`):

| check | result |
|---|---|
| orchestrate-nexus on 0.39.0 | **pass.** Active, ExecStart `ag9lqzvk…-0.39.0`, journal shows `ready`, and no upgrade line (the store was already in the memory format) |
| Observe.Locks equals the snapshot taken just before the stop | **pass.** Byte-identical (md5 4387f5b9…), 12 Locks, again after all the checks |
| Lock and Release round trip with the new client | **pass.** `Locked.{ 173 … }`, then `Released.{ 173 … }`, continuing the old numbering |
| meta client answers | **pass.** `orchestrate-meta Configure` with two equal socket paths answers `ConfigurationRejected.{ InvalidConfiguration }`. I chose this input because it changes no state |
| bad path | **pass.** `LockRejected.RelativePath.relative/path`, and an empty path list answers `LockRejected.NoPath` |
| curriculum-nexus answers a Resolve as before | **pass.** ResolveSkills and ResolveSources over Psyche core Fable's 27 modules are byte-identical to before. The CLI is now `wksqh2p3…-curriculum` |
| Flow seats untouched | **pass.** flow-nexus-0550 and flow-configure-0550 keep their invocation IDs and PIDs. herdr shows the same 8 panes, titles and sessions; only my own pane's spinner glyph differs |
| journals clean | **pass.** No user unit has failed. The only matches are gpg-agent's card noise (799 lines in the 43 minutes before) and systemd's "io pressure threshold" line, which has appeared 236 times since Nov 1 |

## zeus

- **Rollback copy, taken as root before any li login.**
  - At 03:35, li was not logged in and had no lingering. I copied the store as root.
  - The copy is `orchestrate-nexus.memory`, sha256 115a6b62…, inode 28879478. It matches the source before and after the copy.
  - It is kept on zeus at `/root/orchestrate-rollback-2e404d/` and here at `rollback/zeus-orchestrate-nexus/` (`rollback/zeus-copy.txt`).
  - The rollback request at c521835 (Current 560) is `rollback/lojix-zeus-rollback-request.datom`.
- **Pre-check on today's bytes.** 0.39.0's `orchestrate-upgrade-preflight` ran on a scratch copy on prometheus:
  - the first run printed the upgrade line and `active legacy PathLock rows: 0`;
  - the second printed the count alone (`before/zeus-bytes-preflight.txt`).
- **Switch:**
  - Realize, **deployment 565**: Succeeded.
  - ActivateNow, **deployment 566**: Succeeded.
  - Lojix now lists 566 as Current: baaa2p5f, CriomOS 64f55ae.
- **Checks** (`zeus/after-activate.txt`, `zeus/checks.txt`):

| check | result |
|---|---|
| orchestrate-nexus starts and prints the upgrade line | **pass.** At 03:55:26: `orchestrate-nexus upgraded /home/li/.local/state/orchestrate-nexus/orchestrate-nexus.memory from the sema format to the memory format`, then `ready`. The inode is still 28879478 |
| Observe.Locks | **pass.** `Observed.Locks.[]`, which is 0 Locks |
| second start upgrades nothing | **pass.** After `systemctl --user restart` the journal shows `ready` only |
| extra checks | Lock 1 and Release 1 round trip. Bad path answers `LockRejected.RelativePath`. The meta client answers `ConfigurationRejected`. The final Observe is `[]`. No failed units, and nothing in li's journal matches error, fail, panic, refus or mismatch |

## Anything off

1. **The CriomOS relock moved `orchestrate` as well as `criomos-home`** (see Heads). Without that, the Home would have stayed on 0.38.0.
2. **Lojix's zeus transport is li, so the old unit ran before the switch.**
   - The deploy requests use `ssh-ng://li@zeus`, as every zeus deployment has. Realize's li sessions at 03:48:08 therefore started li's user manager, and the old 0.38.0 unit failed until it hit its start limit.
   - The store's bytes moved: 115a6b62… → 9176e3d5… → 79d112db…. Those failed opens commit nothing, which I take from the earlier zeus report's reading of the code. The rollback copy predates all of them.
3. **I started li's zeus user manager as root, then stopped it.**
   - The new unit allows 5 starts in 60 s. The old unit uses up those 5 starts within about 10 s of each li session. An activation landing inside that window could have had its start of the new unit refused.
   - So after Realize I ran `systemctl start user@1001.service` as root. The old unit settled in start-limit-hit at 03:48:47, and the ActivateNow began at 03:49:18. The activation's sd-switch at 03:55:26, well past the window, started 0.39.0 with no restarts.
   - After the checks I stopped user@1001 as root (`zeus/settle.txt`, `zeus/cleanup.txt`). This is how zeus normally rests: no lingering, and no user services outside a login.
4. **zeus's activation spent about 5 minutes in `nix profile install`** of home-manager-path (03:50:24–03:55:26). nix-daemon was CPU-bound with no TCP connection. Cause unknown.
5. **orchestrate-nexus is a simple unit, so "started" is not "ready".** An `Observe.Locks` sent straight after the zeus restart got `Unreachable … No such file or directory` on the socket. The next call answered.
6. **A closing li session is left on zeus.** Session 354 (service `login`, opened at 03:55:27 during the activation) holds a `gnome-keyring-daemon --daemonize --login`. I left it alone; it is not under user@1001.
7. **My Orchestrate Lock 172**, on this release's worktrees and evidence, was held through the ouranos switch and was served by 0.39.0 afterwards. I released it after writing this report.
8. **Worktrees left:** `/git/worktrees/CriomOS-home-orchestrate-release-2e404d` and `/git/worktrees/CriomOS-orchestrate-release-2e404d`, each equal to its new main. Branches `orchestrate-release-2e404d` are pushed in both repositories.
