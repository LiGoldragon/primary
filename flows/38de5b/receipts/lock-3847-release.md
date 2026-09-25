# Lock 3847 stale release

Under the living's 2026-09-25 15:21Z word, relayed by Psyche Medium
e51411: "break the locks. Nobody in particular owns Flow Source."
Psyche High 38de5b acts on it here for Mind Sol 00f95a, who was blocked
on lock 3847.

## Lock

```
3847 MindLowFlowLaunchAdapter e798f3
/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/crates/flow-nexus/src/codex.rs
/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/crates/flow-nexus/src/herdr.rs
/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/crates/flow-nexus/src/prompt_modules.rs
```

Reason on record: "Implement Flow Start system-prompt and harness adapter
behavior after preserved stale ownership."

## Staleness witnesses (three, gathered before touching anything)

1. `hm-list` — `e798f3  flow-e798f3  messaging-build  STALE`.
2. `herdr agent list` — no pane, tab, or agent entry for `flow-e798f3`
   or change `e798f3` anywhere in the live agent list (checked against
   the full JSON dump).
3. `FLOW_ID=38de5b hm-send e798f3 '<Machine.Relay stale-release notice>'`
   returned `Held.{ e798f3 PaneMissing attempt-184c23d18f1f }` (exit 1) —
   undeliverable, no live target.

All three agree: the holder is stale. No live-holder signal was found on
any of the three; nothing here was stopped.

## Finding: lock 3847 already released

`orchestrate 'Observe.Locks'` at the time this subflow ran showed no
lock 3847 in the current set. Mind Sol 00f95a's own witness,
`/home/li/primary/flows/00f95a/witnesses/e798f3-lock-stewardship-20260925.md`,
records that Mind Sol released lock 3847 itself, as delegated steward,
under Psyche High 38de5b's 2026-09-25T15:20:58Z message (recorded in
`flows/38de5b/receipts/mind-lock-3847.md`) — quoting the identical lock
3847 fields above. Mind Sol then took its own locks on the same three
paths: `5707 FlowStartClaudeAdapter00f95a`, `5706
FlowStartSystemPrompt00f95a`, and `5704 FlowStartStaleLockEvidence00f95a`
(the last covering its own witness file), all currently held by 00f95a
in `Observe.Locks`.

So the release this task was dispatched to perform had already
happened, by Mind Sol's own hand under the earlier delegation. This
subflow issued no `Release.<id>` call — there is no lock 3847 left to
release, and re-issuing one against a non-existent id would only
produce `ReleaseRejected`.

## Holder's worktree state

Checked directly at
`/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/` (a
`jj` colocated checkout, branch `flow/e798f3-launch-adapter`, remote
`origin` = `git@github.com:LiGoldragon/flow.git`).

`jj status` showed one working-copy difference: `M result`, a symlink
(not `.gitignore`d) whose target changed between two `/nix/store/...`
paths — a build-output symlink, not authored source. This matches Mind
Sol's witness exactly (same file, same kind of change, dated
2026-09-21T19:20:51Z).

Per this task's step 3, that state was committed as found, without
rewrite, rebase, or deletion:

- `jj commit -m "Commit e798f3's work found under lock 3847 before
  stale release\n\nCo-Authored-By: Claude Fable 5.1
  <noreply@anthropic.com>"` — finalized change `fd1dae690d4c`
  (`svqromwz`), child of `34ddd0dac359` (`Wire selected testing skills
  into native modules`).
- `jj bookmark set flow/e798f3-launch-adapter -r @-` — moved the
  branch onto the new commit.
- `jj git push --bookmark flow/e798f3-launch-adapter` — pushed
  `34ddd0dac359 → fd1dae690d4c` to `origin`.

No other files differed from the branch's prior tip. Nothing was
rewritten, rebased, or deleted.

## Lock action taken here

None. Lock 3847 is already gone; no `Release.<id>` call was made
against it. No lock was taken for 38de5b — this seat does not edit
those paths.

## Sent

Mind Sol 00f95a's binding was resolved immediately before send via
`herdr agent list`: live at pane `wM:pB`, `agent_status: working`,
terminal `Mind Sol 00f95a | primary`.

`FLOW_ID=38de5b hm-send 00f95a '<Machine.Relay body>'` reporting that
lock 3847 is released as stale on the living's word "break the locks,"
that e798f3's dirty work is committed on its branch, and that Mind may
take its own lock.

Result: `Transported.{ 00f95a working }` — **Transported** grade (the
transport accepted the bytes for the exact live binding). Not upgraded
to Presented or Read; no target-side observation was made here.
