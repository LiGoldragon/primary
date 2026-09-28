# Primary workspaces, 2026-09-28

Observed and acted on 2026-09-28 10:00-10:20 (-06:00) by a subflow of 8904b1.

## Result

- Primary jj workspaces that existed: 44 (jj workspace list), of which 42 had a
  directory, 1 is the original (`default`, directory not recorded by jj) and 1
  (`mind-sol-summary-correction-review`) had no directory anywhere.
- Removed: 35 workspaces (forgotten and directory deleted) plus 1 forgotten
  without a directory = 36.
- Remaining: 8 (`default`, `56ae53`, and 6 others, below).
- Disk: `df -B1 /` available 414,343,802,880 bytes before, 424,738,349,056
  after; 10,394,546,176 bytes (about 9.7 GiB) freed.

## Where the original workspace is

`/home/li/primary` is the `default` workspace and holds the repository store
(`/home/li/primary/.jj/repo` is a directory; every other workspace's
`.jj/repo` is a file pointing at it). `jj workspace root` there answers
`/home/li/primary`; its `@` is `tuykplpx` (empty). At the first reading 44
processes had it as cwd, and Herdr panes of Codex seats Luna 19ff9f and
Astra 6fe957 and several unnamed Codex panes sat there. Not touched.

## Remaining workspaces and why

| workspace | path | why kept |
|---|---|---|
| default | `/home/li/primary` | the original; live seats |
| 56ae53 | `/home/li/wt/primary/56ae53` | main flow 8904b1 (Psyche Fable) runs here; excluded by the brief. Note: its `@` sat on a chain of 14 commits that are on no bookmark; `main` carries rewritten copies with the same descriptions, so these are probably superseded predecessors, not verified |
| opus-sonnet-56ae53 | `/home/li/wt/primary/opus-sonnet-56ae53` | live: Herdr panes of Psyche Opus dc53b4 and (at first reading) Psyche Sonnet 38f337, 8 then 3 processes; `@` has an uncommitted `.count` file and one commit `nkyzkmkw` ("Psyche Sonnet 38f337 records ... secured before the seat was ended") on no bookmark |
| mind-sol-successor-56ae53-target | `/home/li/wt/primary/mind-sol-successor-56ae53-target` | live: Herdr session `recovery-56ae53` pane of Mind Sol c56100 at first reading, 8 then 2 processes; `@` adds `.native-seat-receipts/mind-sol-of-56ae53-recovery.json` uncommitted |
| field-packet-56ae53 | `/home/li/wt/primary/field-packet-56ae53` | live at first reading (17 processes; Codex panes incl. Field Luna 184bd8). By 10:19 no process and `@` empty, but two unpublished commits: `kwtzzvmu` (Field Sol 9ac67c records) and `qurnnxwq` (Field Luna 184bd8 records), "secured before the seat was ended" by someone working concurrently |
| e71dab | `/home/li/wt/primary/e71dab` | no process; uncommitted work in `@`: adds `flows/e71dab/vision/{flowEffort,flowRefresh,launchGovernance,paneLifecycle}.md`, modifies `flowGarbageCollection.md` |
| home-flow-0173-receipt-56ae53 | `/home/li/wt/primary/home-flow-0173-receipt-56ae53` | no process; `@` in conflict, adds `flows/56ae53/receipts/home-flow-0173-stage-validation.md`; 7 ancestor commits on no bookmark (`qwunxlwk`, `nwnllllo`, `krmupwqt`, `ulzyurkk`, `utsnwprl`, `wpqtvqyn`, `kwnzkwrs`) |
| mind-sol-56ae53-log | `/home/li/wt/github.com/LiGoldragon/primary/mind-sol-56ae53-log` | no process; sparse (only `flows/`); `@` adds `flows/56ae53/log.md` uncommitted |

Groups: live seat inside 3 (56ae53, opus-sonnet, mind-sol-successor; plus
default); uncommitted work 2 (e71dab, mind-sol-56ae53-log) besides the live
ones; unpublished commits 2 (home-flow-0173-receipt, field-packet); uncertain 0.

## Full inventory at first reading

Columns: size in MiB (`du -sm`), last snapshot (mtime of
`.jj/working_copy/tree_state`), newest file outside `.jj` (mtime). Maker is
taken from the flow ID in the name; no record states who made any of them.

| workspace | path | MiB | snapshot | newest file | outcome |
|---|---|---|---|---|---|
| messenger-plural-projection-00f95a | `/home/li/wt/github.com/LiGoldragon/primary/messenger-plural-projection-00f95a` | 291 | 09-26 09:04 | 09-26 09:04 | removed |
| mind-sol-56ae53-log | `/home/li/wt/github.com/LiGoldragon/primary/mind-sol-56ae53-log` | 1 | 09-26 20:35 | 09-26 20:35 | kept |
| mind-sol-56ae53-log-main | `/home/li/wt/github.com/LiGoldragon/primary/mind-sol-56ae53-log-main` | 295 | 09-27 04:11 | 09-27 04:11 | removed |
| mind-sol-managed-successor-56ae53 | `/home/li/wt/github.com/LiGoldragon/primary/mind-sol-managed-successor-56ae53` | 293 | 09-26 20:59 | 09-26 20:59 | removed |
| sonnet-successor-handoff-139366 | `/home/li/wt/github.com/LiGoldragon/primary/sonnet-successor-handoff-139366` | 295 | 09-27 03:49 | 09-27 03:49 | removed |
| 139366-roster-receipt-audit | `/home/li/wt/primary/139366-roster-receipt-audit` | 294 | 09-27 01:53 | 09-27 01:53 | removed |
| 31147a-primitive-message-prep | `/home/li/wt/primary/31147a-primitive-message-prep` | 293 | 09-26 15:35 | 09-26 15:35 | removed |
| 56ae53 | `/home/li/wt/primary/56ae53` | 294 | 09-28 10:09 | 09-28 10:11 | kept |
| 56ae53-summary | `/home/li/wt/primary/56ae53-summary` | 293 | 09-26 19:08 | 09-26 19:08 | removed |
| 93ba9f | `/home/li/wt/primary/93ba9f` | 293 | 09-26 15:35 | 09-26 15:35 | removed |
| 93ba9f-gate | `/home/li/wt/primary/93ba9f-gate` | 292 | 09-26 12:56 | 09-26 12:56 | removed |
| b7ba00 | `/home/li/wt/primary/b7ba00` | 293 | 09-26 15:35 | 09-26 15:35 | removed |
| b7da5d | `/home/li/wt/primary/b7da5d` | 293 | 09-26 15:54 | 09-26 15:54 | removed |
| bind-c56100-bcc | `/home/li/wt/primary/bind-c56100-bcc` | 293 | 09-26 20:28 | 09-26 20:28 | removed |
| c56100-send-receipt-9ac67c | `/home/li/wt/primary/c56100-send-receipt-9ac67c` | 294 | 09-27 01:09 | 09-27 01:09 | removed |
| e167d8 | `/home/li/wt/primary/e167d8` | 292 | 09-26 12:04 | 09-26 12:04 | removed |
| e167d8-cleanup | `/home/li/wt/primary/e167d8-cleanup` | 292 | 09-26 10:16 | 09-26 10:16 | removed |
| e71dab | `/home/li/wt/primary/e71dab` | 292 | 09-28 09:57 | 09-26 12:14 | kept |
| field-decision-amendment-a68GhE | `/home/li/wt/primary/field-decision-amendment-a68GhE` | 295 | 09-27 03:08 | 09-27 03:08 | removed |
| field-launcher-56ae53 | `/home/li/wt/primary/field-launcher-56ae53` | 293 | 09-26 18:02 | 09-26 18:02 | removed |
| field-luna-claim-184bd8 | `/home/li/wt/primary/field-luna-claim-184bd8` | 293 | 09-26 18:04 | 09-26 17:57 | removed |
| field-packet-56ae53 | `/home/li/wt/primary/field-packet-56ae53` | 295 | 09-28 09:57 | 09-27 07:36 | kept |
| field-recovery-56ae53 | `/home/li/wt/primary/field-recovery-56ae53` | 293 | 09-26 17:13 | 09-26 17:13 | removed |
| herdr-recovery-audit-56ae53 | `/home/li/wt/primary/herdr-recovery-audit-56ae53` | 293 | 09-26 20:06 | 09-26 20:06 | removed |
| home-check-triage-56ae53 | `/home/li/wt/primary/home-check-triage-56ae53` | 294 | 09-27 00:22 | 09-27 00:22 | removed |
| home-flow-0173-receipt-56ae53 | `/home/li/wt/primary/home-flow-0173-receipt-56ae53` | 292 | 09-26 21:19 | 09-26 21:19 | kept |
| home-flow-0173-receipt-clean-56ae53 | `/home/li/wt/primary/home-flow-0173-receipt-clean-56ae53` | 293 | 09-26 21:20 | 09-26 21:20 | removed |
| land-mind-sol-profile-56ae53 | `/home/li/wt/primary/land-mind-sol-profile-56ae53` | 1 | 09-26 19:38 | (no files, only `.jj`) | removed |
| launcher-resume-argv-fix | `/home/li/wt/primary/launcher-resume-argv-fix` | 293 | 09-26 20:23 | 09-26 20:22 | removed |
| mind-sol-56ae53-profile | `/home/li/wt/primary/mind-sol-56ae53-profile` | 293 | 09-26 19:36 | 09-26 19:35 | removed |
| mind-sol-successor-56ae53-target | `/home/li/wt/primary/mind-sol-successor-56ae53-target` | 295 | 09-27 17:36 | 09-27 17:36 | kept |
| mind-vision-00f95a | `/home/li/wt/primary/mind-vision-00f95a` | 278 | 09-24 16:14 | 09-24 16:14 | removed |
| mind-vision-main-00f95a | `/home/li/wt/primary/mind-vision-main-00f95a` | 278 | 09-24 18:25 | 09-24 16:17 | removed |
| native-seat-herdr-56ae53 | `/home/li/wt/primary/native-seat-herdr-56ae53` | 293 | 09-26 16:54 | 09-26 16:54 | removed |
| opus-records-dc53b4 | `/home/li/wt/primary/opus-records-dc53b4` | 295 | 09-27 04:35 | 09-27 04:35 | removed |
| opus-sonnet-56ae53 | `/home/li/wt/primary/opus-sonnet-56ae53` | 295 | 09-27 12:44 | 09-27 12:44 | kept |
| remote-access-56ae53 | `/home/li/wt/primary/remote-access-56ae53` | 293 | 09-26 18:18 | 09-26 18:17 | removed |
| roster-receipt-56ae53 | `/home/li/wt/primary/roster-receipt-56ae53` | 293 | 09-26 19:55 | 09-26 19:55 | removed |
| roster-repair-medium-c56100 | `/home/li/wt/primary/roster-repair-medium-c56100` | 293 | 09-26 21:34 | 09-26 21:34 | removed |
| roster-title-readback-56ae53 | `/home/li/wt/primary/roster-title-readback-56ae53` | 293 | 09-26 20:00 | 09-26 20:00 | removed |
| summary-prep-56ae53 | `/home/li/wt/primary/summary-prep-56ae53` | 293 | 09-26 19:34 | 09-26 19:34 | removed |
| stable-store-copy-witness-56ae53 | `/home/li/wt/stable-store-copy-witness-56ae53` | 294 | 09-27 01:19 | 09-27 01:19 | removed |
| mind-sol-summary-correction-review | (none found) | - | - | - | forgotten |
| default | `/home/li/primary` | - | 09-27 12:47 | - | kept |

Notes on removed ones: `93ba9f` and `e167d8` held only ignored
`__pycache__/*.pyc` files beyond the tree; `field-luna-claim-184bd8` held only
the ignored `flows/.184bd8.flow-id`, byte-identical to
`/home/li/primary/flows/.184bd8.flow-id`. `mind-vision-00f95a` was stale: its
`@` had been rewritten onto a parent adding two files after its last snapshot,
so the disk lacked them; nothing on disk was absent from the repository.

## Method

- Workspaces: `jj workspace list` (jj 0.44.0) from 56ae53; plus a search of
  `/home/li` (depth 7), `/tmp`, `/git`, `/run/user/1001`, `/home` (depth 14)
  for `.jj/repo` files resolving to `/home/li/primary/.jj/repo`. The checkout
  file of each workspace named the same workspace as its directory.
- Live processes: `readlink /proc/*/cwd`, `/proc/*/fd/*`, and at removal
  also `/proc/*/maps`, matched against each workspace path; Herdr panes by
  `herdr pane list` and `herdr --session recovery-56ae53 pane list`
  (read-only; no seat woken or prompted).
- Uncommitted changes: without snapshotting anyone's working copy
  (`--ignore-working-copy` throughout): `@` emptiness from jj; files outside
  `.jj` newer than `.jj/working_copy/tree_state` (none except 56ae53); the
  file list of `<name>@` compared with the files on disk, with every extra
  file checked against `.gitignore`.
- Unpublished commits: revset
  `(::<name>@ ~ ::(bookmarks() | remote_bookmarks())) ~ (empty() & description(exact:""))`.
- Maker: search of `flows/`, `Vision/`, `vision-raw/`, `witnesses/`,
  `reports/` for the workspace name; mentions exist for some (e.g. e167d8,
  b7ba00, e71dab, opus-sonnet-56ae53) but none records creating one.
- Last written: newest mtime of any file outside `.jj`, and tree_state mtime.
- Removal: for each of 35 named workspaces, rechecked immediately before
  (no process cwd/fd/map, no Herdr pane cwd, no path newer than tree_state,
  `@` empty), then `jj --ignore-working-copy workspace forget <name>` and
  `rm -rf -- <exact path>`. `mind-sol-summary-correction-review` forgotten
  only.

## Other repositories under /home/li/wt (listed, not touched)

Separate Primary clones with their own store:
`/home/li/wt/github.com/LiGoldragon/primary/mind-luna-recovery-56ae53`,
`...-clean`, `...-https`, `...-shallow`. Broken workspace whose store
(`.../primary/core-checkup-recovery-20260915-1902`) no longer exists:
`/home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery`.
Bare git evidence repos: `/home/li/wt/348e7b-home-evidence`,
`/home/li/wt/348e7b-message-probe-evidence`, `/home/li/wt/348e7b-os-evidence`.
Own-store checkouts: `/home/li/wt/flow-0174-independent-test-407811`.

Workspaces of other repositories under `/home/li/wt/github.com/LiGoldragon/`:
- CriomOS: bootstrap-b860be, field-clj-b7da5d-repin, flow-next-home-56ae53,
  ouranos-next-9ac67c, bootstrap-piperless-31147a, step2-piperless-31147a,
  tailnet-restart-trigger-56ae53
- CriomOS-home: field-clj-b7da5d-readonly, flow-0173-stage-56ae53,
  flow-0173-stage-56ae53-5ba2e1e, flow-0173-validation-56ae53,
  flow-0174-stage-56ae53, flow-home-check-6fe957, flow-next-enable-56ae53,
  flow-widget-check-6fe957, home-messenger-pin-6fe957,
  message-recovery-56ae53, ouranos-next-9ac67c, remove-piper-31147a,
  spirit-deployment-fixture-6fe957, widget-plugin-registration-56ae53
- Curriculum: hm-docs-00f95a, hm-docs-fix-00f95a, hm-skill-audit-00f95a
- datomic: datomic-ProtoformStack-6329f1, datomic-situated-6329f1,
  e2-default-bodies-01a04a30
- flow: 93ba9f, cap-safe-56ae53, claude-direct-observer-56ae53,
  claude-launch-cap-removal-00f95a, claude-launch-rule-00f95a,
  codex-session-binding-6fe957 (a live process has it as cwd),
  confirm-imported-56ae53, confirm-imported-56ae53-v2,
  field-flow-retry-00f95a, main-system-prompt-00f95a,
  marker-pane-witness-00f95a, mind-sol-00f95a-{bind-evidence,confirm,flow-basics,recovery},
  release-0173-56ae53, start-list-faults-e167d8, system-prompt-00f95a
- goldragon: field-clj-b7da5d-zeus-location
- HackingMessenger: hm-clojure-00f95a
- HackyMessenger: clojure-00f95a, hm-docs-00f95a, hm-docs-fix-00f95a
- harness: claude-launch-rule-00f95a
- listener: listener-wispr-auth-witness, listener-wispr-edge-proxy-01a05588
- lojix: .concluded-workspaces/lojix-testactivation-01a05833
- message: (the directory itself), mind-sol-00f95a-recipient-presentation,
  signal-flow-6-e167d8
- messenger-clj: plural-large-input-00f95a, release-026-56ae53,
  rename-00f95a, route-identity-00f95a
- meta-signal-flow: confirm-imported-56ae53, marker-pane-witness-00f95a,
  mind-sol-00f95a-basic-commands, mind-sol-00f95a-confirm,
  start-list-faults-e167d8
- persona-test: message-flow-8904b1
- plannotator: capability-peer-auth-f7941a
- signal-flow: confirm-imported-56ae53, marker-pane-witness-00f95a,
  mind-sol-00f95a-basic-commands, start-list-faults-e167d8
- signal-message: mind-sol-00f95a-recipient-presentation
- claude-hijack-stock-263-cf7879, codex-hijack/context-modules-cf7879

## Second pass

Done 10:10 to 10:28 by a subflow of 8904b1. Primary main is now `3dd03811`.
Read back from git@github.com:LiGoldragon/primary.git with `git ls-remote`.

### Two processes in mind-sol-successor-56ae53-target

These were pids 3583787 (`node_repl`) and 3583789 (agent-intercom
`codex-server.mjs`). Both were children of the codex-next app-server
service (1960) and were started at 10:00:36. They served Codex thread
`01a0e8bf-a615-79f1-8034-b11c7a9c5980` ("Herschel",
`/root/flow_0174_fixture/profile_correction`). That thread is a depth-2
worker spawned by `01a0e164-85f5…`, which in turn was spawned by Mind Sol
c56100's thread `01a0e0a1…`. The worker's task completed at 10:01:58, and
c56100's pane was closed at 10:17. No Codex client was left. They were
leftovers of an ended seat. A SIGTERM was sent to each by pid, and `kill -0`
then confirmed both were gone.

### The five named copies

Every copy's working copy was snapshotted with `jj st` before it was
forgotten. Ignored `flows/.*.flow-id` markers were compared with the
original: all were identical, and the one exception is noted below. After
that, each copy was forgotten with `jj workspace forget` and removed with
`rm -rf -- <exact path>`. Before removal, no process had a cwd, fd or map
inside any of them.

- **mind-sol-successor-56ae53-target**
  - Held: only the uncommitted file `.native-seat-receipts/mind-sol-of-56ae53-recovery.json`, which is outside `flows/`.
  - Now lives in `secured-0928/mind-sol-successor-56ae53-target.patch`. It is byte-identical to the existing `mind-sol-c56100.patch`.
- **e71dab**
  - Held: uncommitted records of flow e71dab under `flows/e71dab/vision/`. Four were new: flowEffort, flowRefresh, launchGovernance and paneLifecycle. The fifth was an 8-line addition to flowGarbageCollection.
  - Committed in the copy as `cdc8a9f9`, then duplicated onto main as `3dd03811`. It applied cleanly because main's flowGarbageCollection had not changed since the copy's parent. Pushed, and main was read back.
- **home-flow-0173-receipt-56ae53**
  - Held: an uncommitted `flows/56ae53/receipts/home-flow-0173-stage-validation.md`, which is byte-identical to main's.
  - It also held 7 conflicted commits on no bookmark: `kwnzkwrs` through `qwunxlwk`, all under `flows/`. The conflict is in `flows/38de5b/log.md`, and main already contains the added lines.
  - A trial duplicate onto main conflicted on `flows/56ae53/mind-luna-recovery/` and was abandoned.
  - The bookmark `secured-0928-home-flow-0173-receipt-56ae53` was set on the tip `38672921`. jj refused to push it: "Won't push commit 386729214e1d since it has no description and has conflicts".
  - **The bookmark exists only in the local repo /home/li/primary. It is not on the remote.**
- **field-packet-56ae53**
  - Held: an empty `@` and commits `kwtzzvmu` and `qurnnxwq`, which hold `flows/9ac67c/log.md` and `flows/184bd8/log.md`.
  - Both files are byte-identical on main, so nothing needed landing.
- **mind-sol-56ae53-log**
  - Held: an uncommitted `flows/56ae53/log.md`. Main's `flows/56ae53/log.md` holds the same text plus one later entry, so nothing needed landing.

### Copies the inventory missed

The search checked `.jj/repo` links and `NON_MANAGEMENT_AGENTS.md` markers
under /home/li and /tmp, to depth 6 to 7. It found eight more copies. They
are separate clones or orphans, and none is a workspace of /home/li/primary.
None had a live process. Each was removed by its exact path.

- `/home/li/wt/github.com/LiGoldragon/primary/mind-luna-recovery-56ae53`, `-clean` and `-https`: failed clones with no files, no bookmarks and only the root commit.
- `/home/li/wt/github.com/LiGoldragon/primary/mind-luna-recovery-56ae53-shallow`:
  - Clean, with every file tracked.
  - Its bookmarks `main` and `mind-luna-launch-authority-56ae53` point at `60bd205f`, which is on the remote.
  - Its local `mind-luna-recovery-56ae53` bookmark points at `ccd847ef`. That commit has the same tree as the remote's `aac3dc2a` and is also held by the /home/li/primary repo.
- `/home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery`:
  - An orphan workspace. Its repo `core-checkup-recovery-20260915-1902` no longer exists, so jj could not forget it.
  - Of its files, 329 differ from the original. Every one of them is byte-identical to the remote bookmark `flow/cf7879` (`6764621a`).
  - The one exception was the marker `flows/.cf78795.flow-id`, now saved at `secured-0928/cf7879-report-recovery-flow-ids/`.
- `/tmp/primary-flow-139366.QFdP5y/primary`: jj clone, clean, at `18baad59`, which is on the remote. Its empty mktemp parent was removed with rmdir.
- `/tmp/verify-repo`: git-only clone. `main` equals `origin/main` (`5d38ed28`, on the remote), and there are no extra or newer files.
- `…/-home-li-wt-primary-opus-sonnet-56ae53/38f33758…/scratchpad/iso`: jj clone in the ended Psyche Sonnet's scratchpad, clean, at `97de8e4b`, which is on the remote.

### Left

- Workspaces `default` (/home/li/primary), `56ae53` and `opus-sonnet-56ae53`.
- The local-only bookmark `secured-0928-home-flow-0173-receipt-56ae53`. It needs a decision: either mend and push it, or accept that it stays local.

Aside: the op log shows a `jj new main` at 10:22:22 that this pass did not run. After it, `default`'s `@` is `kstrmyyz` where it was `tuykplpx`.
