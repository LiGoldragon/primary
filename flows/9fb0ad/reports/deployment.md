# Deployment: orchestrate 0.37, flow 0.23, message 0.19 as the regular Home units

Subflow of 9fb0ad (successor of f1c841), 2026-10-03, on ouranos. Ruling: the
living, STT about 06:40 local, "Everything can get deployed … I want all this
deployed, made as the regular version in [CriomOS] in our home." The `claude`
wrapper's bypass is not in scope and was not touched. The plan is
`flows/f1c841/reports/deployment.md` «Next commands, for the successor»,
steps 1–4. Timestamps are `date -u`. Replies are copied from the terminal.

## Lock and preconditions (12:59–13:00 UTC), observed live

- `orchestrate 'Observe.Locks'` (12:59:34):
  `Observed.Locks.[ { 11778 PrimaryPublish 9fb0ad [ /home/li/primary/.PrimaryPublish.lock ] «Publish flow 9fb0ad lane» } ]`.
  The only Lock is this flow's own (FlowId 9fb0ad).
- `orchestrate 'Lock.{ HomeRegular 9fb0ad [ /home/li/wt/github.com/LiGoldragon/CriomOS-home/regular-f1c841 ] «…» }'` (12:59:45) →
  `Locked.{ 11779 HomeRegular 9fb0ad [ /home/li/wt/github.com/LiGoldragon/CriomOS-home/regular-f1c841 ] «Activate orchestrate 0.37, flow 0.23, message 0.19 as regular Home units and land CriomOS-home main» }`.
  `Observe.Locks` then lists 11779 and 11778, both FlowId 9fb0ad.
- Generations present: `qda5pkid…`, `2hnqcg3q…`, `1rj6l1ln…`, `xp12f872…` (`ls -d`).
- Rollback target: `readlink ~/.local/state/nix/profiles/home-manager` → `home-manager-1039-link` → `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation`; also rooted by `~/.local/state/f1c841/gcroots/hm-rollback`.
- Legacy meta socket: `ls /run/user/1001/orchestrate-nexus/` → `meta-orchestrate.sock`, `meta-orchestrate.sock.claim`, `orchestrate.sock`, `orchestrate.sock.claim` (since Sep 26 16:19).
- Running (`/proc/<MainPID>/exe`): orchestrate-nexus `0grjjmjc…-orchestrate-nexus-0.35.0`; flow-nexus `c044v5pa…-flow-0.12.2`; flow-nexus-next `7z15aqi4…-flow-0.17.4`; message-daemon `i66j8l0v…-message-0.14.0`; message-nexus-next `3v8qs8h4…-message-0.17.0`. Clients `orchestrate{,-meta}` → `v42cxgyd…-orchestrate-0.35.0-profile`.
- Flow/Message: drop-in `flow-nexus.service.d/override.conf` sets ExecStart to `c044v5pa…-flow-0.12.2`; `nix profile list` holds `flow` → `c044v5pa…`; `~/.local/bin/message-next{,-meta}` exec `nwrvnmk7…-message-0.17.0` (gone from the store, per f1c841). Stores: `~/.local/state/flow/flow.sema` (0.12.2), `~/.local/state/flow-next/.local/state/flow/{flow.sema,launch-bundles}`, `~/.local/state/message/messenger.sema` (+ `.preopen` copies), `~/.local/state/message-next/.local/state/message/message.sema`. `ss -xp`: no peer connected under `/run/user/1001/{flow,message}/`.
- Backups before step 1: only `~/.local/state/orchestrate-nexus/orchestrate-nexus.sema.pre-v2-20260908….bak` (Sep 8) exists; the reports prescribe no orchestrate snapshot, so this flow takes a closed copy in step 1. The next-slot `.predeploy` copies are taken in step 2 as prescribed.
- Seat survival: Herdr (`herdr server`, pid 4957) and the three Claude seats 9fb0ad (pid 2823995), 5578cc (2825212), 6e782c (2826200) run in `app-ghostty-surface-transient-4736.scope`; every Nexus unit's cgroup holds only its own Nexus process (`cgroup.procs`). `diff -rq` of the unit directories of `xp12f872…` against `qda5pkid…`, `2hnqcg3q…` and `1rj6l1ln…` shows only Nexus units (orchestrate-nexus, flow-*, message-*) changing; Ghostty, Herdr and codex-remote-control units are identical. No planned restart kills a pane.
- messenger-clj (`src/messenger_clj/core.clj` `reserve!`/`release!`) calls the `orchestrate` on PATH and matches `Locked\.\{\s+(\d+)` and a `Released.` prefix; 0.37.0's one-line replies keep both forms (orchestrate-rollback-witness).
- Baseline `FLOW_ID=9fb0ad hm-list` (13:00:02), exit 0: 7de94a done, 42265e done, 41fa34 done, dea0ba working, 9fb0ad working, 5578cc done, 6e782c done.

## Step 1: orchestrate 0.37.0 (`qda5pkid…`): failed, rolled back

Plan followed: `flows/f1c841/reports/deployment.md` «Next commands» step 1, with a closed store copy added by this flow.

- 13:00:29 `systemctl --user stop orchestrate-nexus`; `cp --reflink=auto -p ~/.local/state/orchestrate-nexus/orchestrate-nexus.sema ~/.local/state/orchestrate-nexus/orchestrate-nexus.sema.orchestrate-0.35.0.pre037-9fb0ad` (4841472 bytes, both files; the store written only by 0.35.0).
- 13:00:29 `/nix/store/qda5pkid3fa8aj1s32wqk8xcmd029dwm-home-manager-generation/activate`, exit 1:

  ```
  Starting Home Manager activation
  Activating adoptHerdrConfig
  Activating checkFilesChanged
  Activating checkLinkTargets
  Activating writeBoundary
  Creating new profile generation
  Activating createGpgHomedir
  Activating retireProvenLegacyMessengerBindings
  refusing to replace non-legacy messenger binding: /home/li/.local/bin/messenger-clj
  ```

  The profile became `home-manager-1040-link` → `qda5pkid…`. `linkGeneration`, `installPackages` and sd-switch never ran: unit links still point into `ddp041ij…-home-manager-files` (the 1039 files), `nix profile list` `home-manager-path` is still `acj63i96…`, `orchestrate` still resolves to `v42cxgyd…-orchestrate-0.35.0-profile`. `adoptHerdrConfig` was a no-op: `~/.config/herdr/config.toml` still links to `ddp041ij…`, resolving to `grj6d8ly…-herdr-config.toml`, the generation's own.
- 13:00:36 `systemctl --user start orchestrate-nexus` (the unchanged 0.35.0 unit) → active, pid 2853468, `6ynfv0hy…-orchestrate-0.35.0/bin/orchestrate-nexus`, journal `orchestrate-nexus ready` 07:00:37 local; sockets `orchestrate.sock`, `meta-orchestrate.sock` rebound. A first `Observe.Locks` at 13:00:36, before the socket was bound, answered `Unreachable.{ /run/user/1001/orchestrate-nexus/orchestrate.sock «Unix socket I/O failed: No such file or directory (os error 2)» }`; at 13:00:40 `Observed.Locks.[ { 11779 HomeRegular 9fb0ad … } ]` (11778 PrimaryPublish had been released by its owner meanwhile). orchestrate was unavailable from 13:00:29 to about 13:00:37.

### Cause

`retireProvenLegacyMessengerBindings` (CriomOS-home `modules/home/profiles/min/messenger-clj.nix`, last changed by main `0025894f` «Home: admit witnessed Messenger predecessor») lets a present `~/.local/bin/<command>` through only if it links to `predecessorManagedFiles = /nix/store/9ajs6aji25akz3dfrzpffj7j4kpqjjzv-home-manager-files` or to the 0.2.5 legacy root. Since generation 1039 (`xp12f872…`, built from `0025894f`) was activated on Sep 30, `~/.local/bin/messenger-clj` and every `hm-*` link into `ddp041ij…-home-manager-files`, the 1039 generation's own files. So the guard refuses **every** activation built from main or from these branches: `qda5pkid…`, `2hnqcg3q…`, `1rj6l1ln…`, and the rollback target `xp12f872…` itself (all four carry the identical step; read from each `activate`). The guard was written as a one-migration admission and was never re-admitted for its own successor. f1c841's reports did not foresee it: no candidate was activated, and the sandbox witnesses ran Nexus binaries, not `activate`. This is this flow's reading of the script and the links; the refusal itself is witnessed above.

Possible fixes (none made; a CriomOS-home source change and three rebuilds, for the living's word): admit a link whose target is `$oldGenPath/home-files/.local/bin/<command>` (the generation being replaced, which Home Manager names), or any `/nix/store/*-home-manager-files/.local/bin/<command>` that is the current profile's; then rebuild the three generations from the fixed stack. A hand change to `~/.local/bin` to satisfy the guard would bypass the owning declarative source and is not done.

### Rollback (13:01)

- 13:01:27 `/nix/store/xp12f872zfklxd9vs08935lvw6n5nri5-home-manager-generation/activate`, exit 1, the same refusal, after `No change so reusing latest profile generation` (Home Manager's `~/.local/state/home-manager/gcroots/current-home` still names `xp12f872…`, so it did not move the profile back).
- 13:01:34 `nix-env -p ~/.local/state/nix/profiles/home-manager --switch-generation 1039` → `switching profile from version 1040 to 1039`, exit 0. `readlink ~/.local/state/nix/profiles/home-manager` → `home-manager-1039-link` → `xp12f872…`. The orphan `home-manager-1040-link` → `qda5pkid…` remains (`qda5pkid…` is also rooted by `hm-candidate-orchestrate-0.37.0`); it was not deleted.
- 13:01:37 checks: orchestrate-nexus active → `0grjjmjc…-orchestrate-nexus-0.35.0`; flow-nexus → `c044v5pa…-flow-0.12.2`; flow-nexus-next → `7z15aqi4…-flow-0.17.4`; message-daemon → `i66j8l0v…-message-0.14.0`; message-nexus-next → `3v8qs8h4…-message-0.17.0`. `orchestrate`, `flow`, `message` resolve to the 0.35.0, 0.12.2, 0.14.0 clients. `orchestrate 'Observe.Locks'` → `Observed.Locks.[ { 11779 HomeRegular 9fb0ad … } ]`, exit 0. Sockets `meta-orchestrate.sock`, `orchestrate.sock` present.
- `FLOW_ID=9fb0ad hm-list`, exit 0: 7de94a done, 42265e working, 41fa34 working, dea0ba working, 9fb0ad working, 5578cc done, 6e782c done. Herdr server pid 4957 unchanged; seat processes 2823995, 2825212, 2826200 alive (elapsed 15:09, 14:51, 14:45). No pane was lost.

## Not done (stopped per the brief)

- Steps 2 (next Flow 0.23.0 / Message 0.19.0 and `.predeploy` copies), 3 (`sandbox-regular.sh`, store reconfigure and move, the regular-slot generation `1rj6l1ln…`) and 4 (landing CriomOS-home main) were not started. No Flow or Message unit, store, drop-in, profile element or wrapper was touched. CriomOS-home main is still `0025894f`; `f1c841-regular` (`9497e4fb`) is unmerged.
- The promotion tension (compensation-update keeps the Next state root; the brief moves the stores to the regular paths): the prescribed plan is deployment.md's «Next commands» step 3, which moves the stores, each first reconfigured through its running Nexus. It was not reached, so neither form was carried out.
- Left on the host by this flow: the closed copy `~/.local/state/orchestrate-nexus/orchestrate-nexus.sema.orchestrate-0.35.0.pre037-9fb0ad`; profile generation `home-manager-1040-link`; orchestrate-nexus restarted once (new pid 2853468, same 0.35.0, same store).

## Sources

- Read: `flows/f1c841/reports/deployment.md`, `morning-deploy-final.md` (live state, (a), order), `morning-deploy-orchestrate-037.md`, `morning-deploy-flow-message.md`, `orchestrate-rollback-witness.md` (first 120 lines); `~/.local/state/f1c841/regular-witness/sandbox-regular.sh`.
- Activation scripts of `qda5pkid…` and `xp12f872…` (`adoptHerdrConfig` through `linkGeneration`); `diff -rq` of `home-files/.config/systemd/user` across `xp12f872…`, `qda5pkid…`, `2hnqcg3q…`, `1rj6l1ln…`; `home-files/.local/bin` of three generations.
- CriomOS-home `regular-f1c841` worktree `modules/home/profiles/min/messenger-clj.nix`; `git show 0025894f`; `origin/main` = `0025894f` after fetch.
- messenger-clj `3bbb8e32` `src/messenger_clj/core.clj` (`reserve!`, `release!`); `~/.local/bin/hm-send`.
- Live: `orchestrate 'Observe.Locks'`, `systemctl --user show/status/is-active`, `/proc/<pid>/exe`, `/proc/<pid>/cgroup`, `cgroup.procs`, `ls`/`readlink` of runtime, state, profile and `~/.local/bin`, `nix profile list`, `ss -xp`, `hm-list`, `pgrep`.
