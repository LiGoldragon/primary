# Hygiene findings — 2026-10-31

**Coffee account:** Flow has **75 worktrees, not the earlier 57**; 13 are dirty and several have explicit holds, so deleting them without disposition would discard protected work. The historical runaway Python was already terminated; current short sampling found no equivalent runaway. Seven identifiable old test IDs are absent from current panes/Flow, while two of the alleged nine remain unidentifiable. The wrong book credit was written into the source despite inventory metadata saying **Opus 5.5**. **Production code removed 0 / added 0; no cleanup deletion, signal, lifecycle change or cutover action performed.**

## Worktrees: inventory, creation mechanism, disposition barrier

Raw rulings: `flows/81ee4e/vision/working-copies.md`, `flows/6ce3f8/vision/repositories.md` (2026-10-20). The new sweep `flows/1add4b/reports/unfixed-complaints.md` explicitly defines unfixed as no recorded fix, not a fresh test.

Read-only scout used `git -C /git/github.com/LiGoldragon/flow worktree list --porcelain`, per-path status and Orchestrate `Observe.Locks`:

- 75 total entries including main; 74 linked-worktree administrative records.
- 13 dirty entries including main; none was touched.
- Zero Git `locked` markers; this does **not** imply freedom from Orchestrate reservations or retained-work obligations.
- One missing/prunable entry: `/home/li/primary/flows/e3c8c1/flow-938ec35-fix`; Git says its gitdir points to a nonexistent location.
- Held paths include `flow-b2-deploy-2c06c7`, `flow-curriculum-omissions-2c06c7`, `flow-d0-repair-4db1d3`, `flow-datom-red-851681`, `flow-primary-jvm-2c06c7`, `flow-main-integration-851681`, `flow-night2-codex-7f0b01`, `flow-refresh-c27520` and canonical Ruling73 source files.

The actual creation mechanism is repeated explicit `git worktree add` in retained tool history, including `/home/li/.claude/projects/-home-li-primary/28d847ee-f350-4a24-8cb0-0e88abf16cbe/tool-results/bh0lh56gd.txt:67,143`. The current Flow Rust code does not create Git worktrees; `crates/flow-nexus/src/lean.rs` merely lists the harness Enter/ExitWorktree capabilities. This establishes repeated per-task isolated creation, not a common cleanup registry or each survivor's owner.

No remaining clean/unlocked path was proven disposable: detached commits, intended retention, current ownership and rollback needs remain unknown. Even pruning the missing administrative entry can remove a useful reachability/ownership record; it was retained. The precise why-not is disposition evidence, not a claim that cleanup is impossible. Full closure requires approved retained refs/patches plus exact removed-path and post-removal inventory witnesses. No removal authorization is inferred from cleanliness alone.

## Runaway processes: original termination and present sample

Raw source: `flows/aad413/vision/tracker.md`, ~2026-10-29 22:40. Historical retained checkpoint:
`/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/29/rollout-2026-10-29T19-23-58-01a18a68-1049-7dc2-81d6-448a5d5f5d75.jsonl` ordinals1419–1427.

That checkpoint records PID2417092 `python -`, PPID1965146, owner thread `01a18a68-46bd-7940-b7f0-ab50abbe2f9a` / `startup_context`, flow a5d5f5, parsing a `flow-meta Configuration` snapshot. Its 98.6–99% CPU and 45-minute duration were reported; ordinal1427 records `kill -TERM 2417092` followed immediately by no `ps` row. This is the existing incident's stop witness, not a termination performed tonight.

The checkpoint attributes repetition to `start = s.rfind('{ {', 0, i)` selecting a wrong nested opening. It does not retain the full offending loop/progress update. Therefore failed progress versus advancing-but-overlapping parsing is still unknown; “infinite” and “quadratic” are unproved. The exact child transcript was not found by filename in the retained 2026-10-29 session directory. No new parser repair was fabricated.

Coordinator sampled `/proc` CPU ticks/RSS/parent IDs twice, interval2.010s, without exposing environment/argument contents. Shared app-server1965146 used25.9% CPU and1143900KiB RSS in that interval. Flow parent4090634 had many app-server children at roughly0–0.5%CPU. Long-lived python3.14 PID3281690 was idle; the only `python -` in the short sample was this bounded probe itself. No matching present runaway was demonstrated. Neither process existence nor one short sample proves a Codex thread leak or long-term health.

`/home/li/tracker/role.md:25` already requires a >50%CPU process on two beats to be reported, then identity/owner-checked at the next beat before termination. Field Secondary received a request for the existing tracker's actual latest beat receipt (delivery775 accepted Queued). The rule text alone does not prove enforcement. No blanket process kill or Flow thread-lifecycle rewrite is justified by this evidence.

## Test flows: identifiable old IDs absent, two identities unresolved

Raw source `flows/97bb3e/vision/flow.md` describes nine Haiku panes after Retire on2026-10-24 but supplies no IDs. Retained parent transcript `/home/li/.claude/projects/-home-li-primary/97bb3e5c-59ba-57bc-9059-63da0769451b.jsonl:400` exposes related IDs `ac0070`, `10b9bb`, `1f8081`, `f99f7e`, `18d009`, histories `9a83ec`, `857ff0`. The same transcript reports FlowRetired receipts for the first three. It does not identify all nine independent panes or establish why a Retire receipt left a pane.

Current supported `herdr --session default pane list` and `flow 'Metaflows'` contain none of those seven IDs. That is an absence witness for the identifiable set only; the old nine as a whole are not proved cleared. Current cutover-held `82eb82`, `84efdc`, `891871` are different tests and remain untouched. `agent_status=done` or Awake is not teardown authority. No Retire, Drop, Close, pane input or signal was sent.

## Wrong signature: source-authoring cause witnessed

Raw complaint: `flows/787230/vision/proposal.md:9`, `flows/2933ce/vision/belief-modules.md:36`.

Retained `/home/li/.claude/projects/-home-li-primary/78723097-355d-5b49-a209-b17f4ffca09a.jsonl:704`, timestamp2026-10-29T18:34:47.794Z, is a Write input for `/home/li/primary/flows/787230/placement-design.md`. Its content literally credits “Designed by Fable 5.1, inventory by Opus 4.1.” Thus the wrong value predates rendering/publication.

Inventory tool-use `toolu_011nwwczXun3fcYRVymCkEnV` at line577 links completion task `a38b1bf811b4aaa1d` at673. The linked `subagents/agent-a38b1bf811b4aaa1d.jsonl:9` records `message.model=claude-opus-5-5`, independently read by coordinator. Publisher subtranscript `agent-a02714fd82f61d34f.jsonl:3` records `claude-sonnet-5-5`; publisher was requested at main736. The provenance contradicts the authored inventory credit; this finding says nothing about whether a model name ever existed externally.

The original placement-design.md is absent in today's tree. Psyche Secondary received the exact source/model evidence and request to correct retained hosted attribution through its existing book route, or report the precise source/publication absence (delivery779 accepted Queued). No historical raw words were rewritten or old proposal republished. `primary-5rgp` now holds this cause witness but stays open because it also requires the separate Curriculum role-module review.

## Preservation and accounting

All four earlier account files were observed committed in `00b0448e6de63677bf9a899b2f0cde7af877b3b2`; its stat contains only those four report paths (+154 documentation lines), not production code. That local commit is witnessed; push, publication and who consumed the reports are not inferred. Existing Field primaryCommitting56b457 is present in current pane/metaflow observations; direct authority/acceptance is still required. This report is a later authored file, not part of that commit.
