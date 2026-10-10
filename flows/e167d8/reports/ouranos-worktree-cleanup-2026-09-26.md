# Ouranos worktree / build-dir / primary cleanup — 2026-09-26

Flow e167d8 subflow, on ouranos. Order (living, ~08:00 STT): remove all old
profiles, GC the Nix store, delete all build directories everywhere, get rid of
abandoned worktrees, keep only one primary Git. Continues
`ouranos-cleanup-2026-09-26.md` (models + first GC).

## Space

Root filesystem `/dev/nvme0n1p2` carries `/`, `/nix` and `/home` (one filesystem).

| Point | Size | Used | Avail | Use% |
| --- | --- | --- | --- | --- |
| Before this pass (after prior model purge + GC) | 916G | 726G | **144G** | 84% |
| After cargo `target/` sweep | 916G | 500G | 369G | 58% |
| After abandoned-worktree sweep | 916G | 480G | 389G | 56% |
| After primary-copy sweep | 916G | 472G | 398G | 55% |
| After stale scratch/`result` sweep | 916G | 455G | 415G | 53% |
| After final `nix-collect-garbage -d` | 916G | **451G** | **419G** | 52% |

Net reclaimed this pass: **275G**. Combined with the prior pass, `/nix` + `/home`
went from 16G free to 419G free.

## 1. Old profiles

Nothing to delete — the prior pass's `nix-collect-garbage -d` had already
reclaimed every superseded generation. Verified:

- `/nix/var/nix/profiles/`: only `system -> system-188-link` (= `/run/current-system`), plus `default -> per-user/root/profile`. No `system-N` besides 188.
- `/nix/var/nix/profiles/per-user/root/`: empty.
- `/home/li/.local/state/nix/profiles/`: only `home-manager-1032-link` and `profile-1996-link`, both current.
- `nix-env --list-generations`: one generation, `19 (current)`.
- The `/home/bird/...` and `/home/maikro/...` profile links referenced from `gcroots/auto` are dangling (those home directories no longer exist); GC cleaned them.

Kept: the booted and current system, and the two Lojix audit roots
`/var/lib/lojix/audits/bird-zeus-8e9fd484` and `bird-zeus-9ef4d609` (~29 GiB
each) — untouched, separate ruling still owed.

## 2. Build directories

**Cargo `target/`**: 234 directories removed (every `target/` under `/home/li/wt`,
`/git`, `/home/li/primary`, `/tmp` and `/var/tmp` carrying `debug/`, `release/`
or `CACHEDIR.TAG`), **226 GiB**. Orchestrate lock 7167.

Skipped as locked by other flows: `/git/github.com/LiGoldragon/agent/target`
(5f38bc, lock 5477) and
`/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588/target`
(lock 441).

Activity check before deleting: no `cargo`/`rustc` process running, `lsof +D` on
the largest trees empty, and no process `cwd` inside any `target/`. The only long
run on the box was flow 31147a's `nix build` of the CriomOS toplevel (pid 919656,
`max-jobs 0`, remote builders) and Field Luna e71dab's read-only `du` — neither
touches a cargo target dir.

**Stale scratch and `result` roots** (lock 7213, 429 paths, ~16.5 GiB):

- `target-*` build dirs in session 38de5bbb's scratchpad (~9.3 GiB) — the session process is still resident but no build was running and nothing held the dirs open; the rest of that scratchpad was left alone.
- `/tmp/cf7879-process-boundary-target`, `/tmp/goldragon-synchronizer-validate-target`, `/tmp/field753-flow-nexus-target.o8TN9T`, `/var/tmp/mentci-cargo-XroOL2/target`, `/tmp/ethos-zero-astra-EfNPnY/consumer-target`, `/tmp/lojix-test-store`, `/tmp/herdr-codex-executable.pbE7to`.
- Scratchpads of Claude sessions with no live process.
- 77 `result` / `result-*` Nix out-links (GC roots) outside live flows' trees.

Kept: `/tmp/lojix-a67-target-00f95a` (2.4 GiB) and every `result` link under a
00f95a, 31147a or e167d8 path — those flows are live or building.

## 3. Abandoned worktrees

533 worktrees / workspaces were enumerated under `/home/li/wt` (plus
`/home/li/primary-worktrees` and `/home/li/primary-workspaces`, found in step 4).
Each was probed for content not on its remote:
`jj log -r 'remote_bookmarks()..@'` for jj workspaces, `git status --porcelain`
plus `git log --branches --not --remotes` for git worktrees and clones.

**Removed: 489 jj workspaces and git worktrees** (lock 7177). Each was
`jj workspace forget`-ed (or `git worktree prune`-d afterwards) before removal; a
follow-up sweep forgot 174 further stale registrations, and a re-scan of every
repo under `/git` and `/home/li/primary` now reports **no** workspace whose path
is missing.

**Rescued first — 76 bookmarks/branches pushed and verified on
`github.com` with `git ls-remote`** before their worktree was removed. Bookmark
name = worktree directory name; commits that had no description were given
`Rescued work from worktree <name> before cleanup (flow e167d8)`.

| Worktree | Bookmark on `github.com/LiGoldragon/<repo>` | Revision |
| --- | --- | --- |
| `/home/li/wt/348e7b-heartbeat-consumer` | `348e7b-heartbeat-consumer` | `5efad7a26898` |
| `/home/li/wt/348e7b-heartbeat-home` | `348e7b-heartbeat-home` | `33e0072d92ac` |
| `/home/li/wt/348e7b-prometheus-single-model` | `348e7b-prometheus-single-model` | `368297c92a28` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/field-medium-eb7bae-flow-message-deploy` | `field-medium-eb7bae-flow-message-deploy` | `90702b6e9aa3` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/field-wifi-wan-recovery-753e69` | `field-wifi-wan-recovery-753e69` | `114fcbd10294` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/flow07-b7da5d` | `flow07-b7da5d` | `58b4c6b98263` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/6852f4-default-effort-medium` | `6852f4-default-effort-medium` | `9758210279a8` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/core-checkup-cf7879-v2` | `core-checkup-cf7879-v2` | `b8ec0f10d43b` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-codex-next-9e735b` | `field-codex-next-9e735b` | `aa86cb50db24` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-medium-eb7bae-agent-intercom-cleanup` | `field-medium-eb7bae-agent-intercom-cleanup` | `ba5bcac8d04b` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/field-medium-eb7bae-flow-message-deploy` | `field-medium-eb7bae-flow-message-deploy` | `904185761771` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/flow07-b7da5d` | `flow07-b7da5d` | `e6f60a145baa` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-home/luna6-flow06-aba-active` | `luna6-flow06-aba-active` | `f1cc3d50019e` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/luna6-flow06-aba-active` | `luna6-flow06-aba-active` | `c0b02d8afe72` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/prometheus-usb-bus-property-5f38bc` | `prometheus-usb-bus-property-5f38bc` | `da85c4a9e755` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/prometheus-usb-downlink-5f38bc` | `prometheus-usb-downlink-5f38bc` | `de5ac1b797c1` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/fixlojixbootownership` | `fixlojixbootownership` | `185c3df15658` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/generic-nodes-fixtures-542442` | `generic-nodes-fixtures-542442` | `bc5eaef8d114` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/usb-downlink-non-router` | `usb-downlink-non-router` | `e0aef3da0511` |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/usb-downlink-source-fix` | `usb-downlink-source-fix` | `e92a336e2e69` |
| `/home/li/wt/github.com/LiGoldragon/Curriculum/fix-5f4fea-main-flow-execution-boundary` | `fix-5f4fea-main-flow-execution-boundary` | `bccac013493e` |
| `/home/li/wt/github.com/LiGoldragon/Curriculum/fix-5f4fea-main-subflow-execution-boundary` | `fix-5f4fea-main-subflow-execution-boundary` | `5f8b46f7b8ca` |
| `/home/li/wt/github.com/LiGoldragon/Curriculum/flow-aspect-7e8542` | `flow-aspect-7e8542` | `d63563f908d7` |
| `/home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-binding-542442` | `ethos-binding-542442` | `87a30492a4a2` |
| `/home/li/wt/github.com/LiGoldragon/ethos-zero/ethos-zero-keepgoing-6329f1` | `ethos-zero-keepgoing-6329f1` | `8bcb0b9402fb` |
| `/home/li/wt/github.com/LiGoldragon/flow/launch-profile-47764b` | `launch-profile-47764b` | `be898a478da8` |
| `/home/li/wt/github.com/LiGoldragon/flow/mind-medium-delivery-2c61af` | `mind-medium-delivery-2c61af` | `b83bfbddc2fd` |
| `/home/li/wt/github.com/LiGoldragon/flow/mind-sol-6288d1-bind-existing-v2` | `mind-sol-6288d1-bind-existing-v2` | `6ed7d1742995` |
| `/home/li/wt/github.com/LiGoldragon/flow/start-store-47764b` | `start-store-47764b` | `33b9f608cbac` |
| `/home/li/wt/github.com/LiGoldragon/flow/transcript-schema-repin-47764b` | `transcript-schema-repin-47764b` | `4c985b6725b4` |
| `/home/li/wt/github.com/LiGoldragon/goldragon/lojix-canonical-proposal` | `lojix-canonical-proposal` | `fd54f8cb4830` |
| `/home/li/wt/github.com/LiGoldragon/goldragon/post-terminus-horizon-data` | `post-terminus-horizon-data` | `a911515c69a7` |
| `/home/li/wt/github.com/LiGoldragon/goldragon/prometheus-usb-downlink-5f38bc` | `prometheus-usb-downlink-5f38bc` | `1781f079a1f1` |
| `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-primary-api-correction-753e69` | `horizon-primary-api-correction-753e69` | `b45d6ad48b5e` |
| `/home/li/wt/github.com/LiGoldragon/horizon-rs/post-terminus-horizon-data` | `post-terminus-horizon-data` | `37416e10c00c` |
| `/home/li/wt/github.com/LiGoldragon/horizon-rs/prometheus-usb-downlink-40d-5f38bc` | `prometheus-usb-downlink-40d-5f38bc` | `fed0a12a3763` |
| `/home/li/wt/github.com/LiGoldragon/horizon-rs/prometheus-usb-downlink-5f38bc` | `prometheus-usb-downlink-5f38bc` | `b45d6ad48b5e` |
| `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-sandbox` | `listener-wispr-sandbox` | `cd8d7e81f1f6` |
| `/home/li/wt/github.com/LiGoldragon/lojix/prometheus-usb-downlink-5f38bc` | `prometheus-usb-downlink-5f38bc` | `387c13b51276` |
| `/home/li/wt/github.com/LiGoldragon/mentci/main-transitives` | `main-transitives` | `b3df35b2d548` |
| `/home/li/wt/github.com/LiGoldragon/message/datom-cli-cf7879` | `datom-cli-cf7879` | `21768e590558` |
| `/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e` | `integrated-messenger-poc-34d94e` | `e6eae2538ca4` |
| `/home/li/wt/github.com/LiGoldragon/message-schema3-v5-cf7879` | `message-schema3-v5-cf7879` | `dd02153b4903` |
| `/home/li/wt/github.com/LiGoldragon/orchestrate/mcp-component-fixture-cf7879` | `mcp-component-fixture-cf7879` | `39b7a3dac142` |
| `/home/li/wt/github.com/LiGoldragon/orchestrate/orchestrate-keepgoing-6329f1` | `orchestrate-keepgoing-6329f1` | `1c0dd769c827` |
| `/home/li/wt/github.com/LiGoldragon/primary/cf7879-overnight-batch` | `cf7879-overnight-batch` | `fed52f82d875` |
| `/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj` | `claude-successor-efa157-jj` | `285320751612` |
| `/home/li/wt/github.com/LiGoldragon/primary/claude-successor-f55ec8-jj` | `claude-successor-f55ec8-jj` | `d045387519bb` |
| `/home/li/wt/github.com/LiGoldragon/primary/field-6db-report-20260921` | `field-6db-report-20260921` | `1b8d1d4cf2ed` |
| `/home/li/wt/github.com/LiGoldragon/primary/field-census-6db4fe` | `field-census-6db4fe` | `8c38d3b5341c` |
| `/home/li/wt/github.com/LiGoldragon/primary/field-world-6db4fe` | `field-world-6db4fe` | `b57a43de02c6` |
| `/home/li/wt/github.com/LiGoldragon/primary/overnight-queue-recovery-20260916` | `overnight-queue-recovery-20260916` | `a307ebbba455` |
| `/home/li/wt/github.com/LiGoldragon/primary/psyche-medium-jj` | `psyche-medium-jj` | `33c389f71495` |
| `/home/li/wt/github.com/LiGoldragon/signal-flow/night-messaging-0ab019` | `night-messaging-0ab019` | `13e96ce5ce08` |
| `/home/li/wt/github.com/LiGoldragon/wispr-flow-linux/wispr-desktop-observer-4647d2` | `wispr-desktop-observer-4647d2` | `1b91b98e3258` |
| `/home/li/wt/primary-5f4fea-disk-retention` | `primary-5f4fea-disk-retention` | `f6b6c47293ab` |
| `/home/li/wt/primary-5f4fea-flow-assembler-full-context` | `primary-5f4fea-flow-assembler-full-context` | `46c6bae43c5a` |
| `/home/li/wt/primary-5f4fea-g11g12` | `primary-5f4fea-g11g12` | `ef9cf86d9785` |
| `/home/li/wt/primary-5f4fea-item30` | `primary-5f4fea-item30` | `321050ff64b7` |
| `/home/li/wt/primary-5f4fea-main-flow-projection` | `primary-5f4fea-main-flow-projection` | `70b62c0032c6` |
| `/home/li/wt/primary-5f4fea-main-subflow-projection` | `primary-5f4fea-main-subflow-projection` | `42a2979d1e46` |
| `/home/li/wt/primary-5f4fea` | `primary-5f4fea` | `7178764c9e56` |
| `/home/li/wt/primary-cf7879` | `primary-cf7879` | `88a058623aa8` |
| `/home/li/wt/primary-eae736-closure` | `primary-eae736-closure` | `197997d0ef17` |
| `/home/li/wt/primary-fd0f97` | `primary-fd0f97` | `fb6e00b8295b` |
| `/home/li/wt/primary/field-census-9ddcbc` | `field-census-9ddcbc` | `fdb2c1c0f8e6` |
| `/home/li/wt/primary/field-checkup-shadow-9ddcbc` | `field-checkup-shadow-9ddcbc` | `244f338efc02` |
| `/home/li/wt/primary/field-high-main-merge-753e69` | `field-high-main-merge-753e69` | `9427c0cd895e` |
| `/home/li/wt/primary/field-high-refresh-753e69` | `field-high-refresh-753e69` | `a0fa9d5301fb` |
| `/home/li/wt/primary/field-merge-9ddcbc` | `field-merge-9ddcbc` | `1cb65aa2ce68` |
| `/home/li/wt/primary/field-network-main-753e69` | `field-network-main-753e69` | `c078012e2ad5` |
| `/home/li/wt/primary/field-rollout-plan-9ddcbc` | `field-rollout-plan-9ddcbc` | `5da0093c2604` |
| `/home/li/wt/primary/harness-visual-indicators-753e69` | `harness-visual-indicators-753e69` | `4435501401f5` |
| `/home/li/wt/primary/psyche-harness-vision-753e69` | `psyche-harness-vision-753e69` | `47ce0aa71df7` |
| `/home/li/wt/primary/psyche-harness-vision-main-753e69` | `psyche-harness-vision-main-753e69` | `706080d0ff95` |
| `/home/li/wt/primary/transitive-network-topology-753e69` | `transitive-network-topology-753e69` | `8433b21930c6` |

Verification grade for every row: the local revision equals
`git ls-remote git@github.com:LiGoldragon/<repo>.git refs/heads/<bookmark>`.
`/tmp/f55ec8-v7/primary` was pushed twice — once as `primary` (its directory
basename) and once as the clearer `f55ec8-v7-primary`.

`/home/li/wt/github.com/LiGoldragon/horizon-rs/usb-gateway-main-merge-753e69`
held a merge commit that became reachable from a remote bookmark once its sibling
horizon-rs rescues landed; nothing separate was owed.

### Kept, with reason

| Path | Reason |
| --- | --- |
| `/home/li/wt/github.com/LiGoldragon/claude-hijack-stock-263-cf7879` | locked path |
| `/home/li/wt/github.com/LiGoldragon/codex-hijack/context-modules-cf7879` | locked path |
| `/home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-b860be` | locked path |
| `/home/li/wt/github.com/LiGoldragon/Curriculum/hm-docs-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/Curriculum/hm-docs-fix-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/Curriculum/hm-skill-audit-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/claude-launch-rule-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/field-flow-retry-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/main-system-prompt-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/marker-pane-witness-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-bind-evidence` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-confirm` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-flow-basics` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/mind-sol-00f95a-recovery` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/flow/start-list-faults-e167d8` | flow e167d8 is the live main flow |
| `/home/li/wt/github.com/LiGoldragon/flow/system-prompt-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/HackingMessenger/hm-clojure-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/HackyMessenger/clojure-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/HackyMessenger/hm-docs-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/HackyMessenger/hm-docs-fix-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/harness/claude-launch-rule-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness` | locked path |
| `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588` | locked path |
| `/home/li/wt/github.com/LiGoldragon/message/mind-sol-00f95a-recipient-presentation` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/message/signal-flow-6-e167d8` | flow e167d8 is the live main flow |
| `/home/li/wt/github.com/LiGoldragon/messenger-clj/rename-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/messenger-clj/route-identity-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/meta-signal-flow/marker-pane-witness-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/meta-signal-flow/mind-sol-00f95a-basic-commands` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/meta-signal-flow/mind-sol-00f95a-confirm` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/meta-signal-flow/start-list-faults-e167d8` | flow e167d8 is the live main flow |
| `/home/li/wt/github.com/LiGoldragon/plannotator/capability-peer-auth-f7941a` | locked path |
| `/home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery` | locked path |
| `/home/li/wt/github.com/LiGoldragon/signal-flow/marker-pane-witness-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/signal-flow/mind-sol-00f95a-basic-commands` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/signal-flow/start-list-faults-e167d8` | flow e167d8 is the live main flow |
| `/home/li/wt/github.com/LiGoldragon/signal-message/mind-sol-00f95a-recipient-presentation` | flow 00f95a is working |
| `/home/li/wt/primary/mind-vision-00f95a` | flow 00f95a is working |
| `/home/li/wt/primary/mind-vision-main-00f95a` | flow 00f95a is working |
| `/home/li/wt/github.com/LiGoldragon/message` | container directory that is itself a git repo and holds live 00f95a and e167d8 worktrees |
| `/home/li/wt/github.com/LiGoldragon/datomic/datomic-ProtoformStack-6329f1` | orphan: its owning repo `/git/github.com/LiGoldragon/datomic` is gone, so nothing can be pushed (156K) |
| `/home/li/wt/github.com/LiGoldragon/datomic/datomic-situated-6329f1` | same orphan (160K) |
| `/home/li/wt/github.com/LiGoldragon/datomic/e2-default-bodies-01a04a30` | same orphan (136K) |
| `/home/li/wt/github.com/LiGoldragon/lojix/.concluded-workspaces/lojix-testactivation-01a05833` | orphan repo pointer, cannot push (1.1M) |

Protection rule used: a worktree stayed if it sits on a path in a currently held
Orchestrate lock, if its flow is `working` in `hm-list` (00f95a), if its flow has
a build in flight (31147a), or if it belongs to the live main flow e167d8 — except
e167d8's own `s1-e167d8`, `s2-e167d8` and `flow-message-016-e167d8`, which the
brief released. `/tmp/lojix-a67-target-00f95a` was likewise kept.

### One side effect, recorded

`/home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery` is a locked
path (lock 1805, flow cf7879, which no longer appears in `hm-list`) and was kept.
Its `.jj/repo` pointed at a *sibling* worktree,
`.../primary/core-checkup-recovery-20260915-1902`, which was in the removal set,
so that pointer is now dangling. No content was lost: both worktrees probed
`CLEAN` / empty-working-copy before removal, i.e. everything reachable was
already on a remote bookmark. The report-recovery files themselves are untouched
on disk; only local history access through that worktree is gone.

## 4. Primary

Kept exactly **`/home/li/primary`**. Copies were located by fingerprint
(`find / -xdev -name NON_MANAGEMENT_AGENTS.md`, excluding `/nix/store`) plus a
`primary*` directory sweep, giving 47 clones/copies. **41 removed** (lock 7206,
~8.8 GiB), after rescuing:

- 3 jj workspaces under `/home/li/primary-worktrees` pushed (`MindJudgePromptRewrite-NarrowThirdPass`, `MindJudgePromptRewrite-TargetedSecondPass`, `mind-judge-fixture-label-cleanup`).
- `/home/li/primary/.claude/worktrees/flow-840e42` → branch `flow-840e42`.
- `/tmp/f55ec8-v7/primary` → branches `primary` and `f55ec8-v7-primary`.
- The 23 copies with no `.jj`/`.git` at all had no history to push. Each was diffed against `/home/li/primary` (`diff -rq`); every "unique" file was a file *deleted* from primary since the copy was taken — the old `tools/hacky-messenger` + `hm-*` shims (superseded by messenger-clj), removed `.claude/agents/*-critical.md`, and `flows/0ab019/.../codex_history.rs`, which is present in primary's history (now `history.rs`). Nothing unrecorded was destroyed.

Also removed: `/git/github.com/LiGoldragon/primary` (only a container holding one
clean worktree, no repo of its own),
`/home/li/wt/github.com/LiGoldragon/primary/cf7879-core-artifact-restoration`
(8K of Nix out-link roots), `/home/li/primary-workspaces`,
`/home/li/primary-worktrees`, both `/home/li/.codex/worktrees/*/primary`, and
`/home/li/wt/348e7b-primary-evidence` (a 69M bare clone, no unpushed refs).

Kept: `/git/github.com/LiGoldragon/primary-next` — a **different** repository
(`origin git@github.com:LiGoldragon/primary-next.git`), not a copy of primary.

### Damage to `/home/li/primary`'s `default` workspace, and its repair

While removing `/home/li/primary/.claude/worktrees/flow-840e42` the removal loop
ran `jj workspace forget` with that directory as cwd. Because the harness
worktree is a *git* worktree with no `.jj` of its own, `jj` walked up to
`/home/li/primary/.jj` and forgot the **`default`** workspace instead. That was
this flow's mistake, not another flow's.

Recovery: the forgotten working-copy commit was `nwyvwuoy 675d0487`, and it is
**empty** (`jj log -r 675d0487` → `empty=yes`) — it held no uncommitted change,
so nothing on disk or in history was lost. `jj` recreated the workspace on the
next command. `/home/li/primary` now reports:

    default: upymluzs … (working copy present)
    mind-vision-00f95a: ../wt/primary/mind-vision-00f95a
    mind-vision-main-00f95a: ../wt/primary/mind-vision-main-00f95a

`jj status` works ("The working copy has no changes"), `@-` is `main`, and other
flows have committed and pushed `main` through this checkout since (b860be's
Zeus-first receipts), which is the direct proof the checkout is healthy. Both
`../wt/primary/mind-vision*` workspaces survived.

Rule taken forward: never run `jj workspace forget` with a repo's primary
checkout reachable above the cwd; forget by explicit workspace name from the
owning repo instead.

## 5. Final garbage collection

`nix-collect-garbage -d` (as `li`; the system-wide run needs a password that is
not available to an agent): **2,916 store paths deleted, 4.7 GiB freed**.
`note: hard linking is currently saving 64.2 GiB`. 86 of the 148
`/nix/var/nix/gcroots/auto` links were dangling before the run and are no longer
counted as roots.

Prometheus was not touched. All five Orchestrate locks taken for this work (7167,
7177, 7206, 7213) were released; `Observe.Locks` shows no lock held by e167d8.
TAIL
wc -l $R