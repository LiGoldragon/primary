# Transcript evidence: six recent main flows, 2026-10-02/03

Scope: 28d847, 5578cc, edf227, 6e782c (Claude), 41fa34, 42265e (Codex). 5ed94b (this flow) excluded. Times UTC. Counts are from parsing the transcripts' JSON records; kind labels are regex on the command text (heredoc bodies and quoted strings stripped), so each kind is WITNESSED as "command matching", not as intent. Mixed commands take one label by priority: publish, hm-send, flow-id, vision, book/report, log. The 28d847, 41fa34 and 42265e transcripts were still growing while read (42265e went 294 to 297 commands during the read); counts are a snapshot, +/- 3.

Provenance receipt: unavailable (no PROVENANCE handoff received). Codex rollout paths below have the native thread id redacted; the file is `rollout-2026-10-02T12-07-29-*` (41fa34) and `rollout-2026-10-02T12-07-00-*` (42265e) under `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/02/`. Claude transcripts: `/home/li/.claude/projects/-home-li-primary/<alias>*.jsonl` where the session id begins with the flow alias (28d847ee-, 5578cce2-, edf22711-, 6e782cf5-). Located per the transcript-search skill (read as evidence); the `transcript` CLI is not installed here, so I parsed the files directly. Line numbers are jsonl lines; Claude subagent results are quoted from their `queue-operation` records.

Not created: Beads, lane, index entry, log.

## 1. Totals

| flow | harness | lines | first to last | span | active (gaps <=30 min) | main-flow shell cmds | subflows / messages |
|---|---|---|---|---|---|---|---|
| 28d847 | Claude Opus | 471 | 10-03 20:20 - 20:35 | 0.25 h | 0.25 h | 21 | 8 Agent, 3 SendMessage |
| 5578cc | Claude Opus | 3560 | 10-03 12:46 - 20:22 | 7.60 h | 6.86 h | 146 | 75 Agent, 12 SendMessage |
| edf227 | Claude Fable | 2267 | 10-03 17:16 - 20:35 | 3.32 h | 3.32 h | 102 | 37 Agent, 4 SendMessage |
| 6e782c | Claude Sonnet | 718 | 10-03 12:46 - 20:31 | 7.74 h | 1.87 h | 20 | 17 Agent, 4 SendMessage |
| 41fa34 | Codex Sol | 7050 | 10-02 18:07 - 10-03 20:35 | 26.5 h | 10.7 h | 77 | 11 spawn_agent, 280 followup_task, 92 send_message |
| 42265e | Codex Sol | 9685 | 10-02 18:07 - 10-03 20:35 | 26.5 h | 12.4 h | 297 | 13 spawn, 261 followup_task, 175 send_message, 30 wait_agent, 3 interrupt_agent, 3 sleep |

All WITNESSED. The Codex span is wall clock including overnight idle: 41fa34 has 15.8 h and 42265e 14.1 h in gaps over 30 minutes (largest 6.8 h and 6.6 h, 06:14 - 13:00 on 10-03). 6e782c has 5.9 h of idle gaps (2.3 h 12:55 - 15:12 is the largest).

## 2. (a) Shell commands the main flow itself ran, by kind

Exclusive label per command, WITNESSED.

| kind | 28d847 | 5578cc | edf227 | 6e782c | 41fa34 | 42265e |
|---|---|---|---|---|---|---|
| hm-send | 8 | 75 | 45 | 5 | 0 (uses send_message/followup_task tools) | 32 |
| log.md append | 6 | 46 | 15 | 13 | 67 | 75 |
| vision file write | 4 | 11 | 7 | 1 | 3 | 3 |
| book/report/index write | 1 | 7 | 17 | 0 | 0 | 1 (+2 file-write) |
| flow-id | 1 | 4 | 1 | 1 | 1 | 3 |
| publish compound (orchestrate Lock + jj commit + duplicate + resolve + push + Release in one command) | 0 | 0 | 13 | 0 | 0 | 30 |
| other jj/git (status/log/diff/rebase/resolve/fetch) | 0 | 0 | 1 | 0 | 0 | 57 |
| file read cat/sed/head/tail | 1 | 1 | 2 | 0 | 1 | 46 |
| ls/grep/find/date status | 0 | 0 | 1 | 0 | 0 | 11 |
| beads (bd) | 0 | 2 | 0 | 0 | 0 | 0 |
| other (tool probes, clock, build/run) | 0 | 0 | 0 | 0 | 5 | 37 |
| total | 21 | 146 | 102 | 20 | 77 | 297 |

Findings (WITNESSED):
- 5578cc ran zero jj or git commands itself. Every commit and push went through a subagent: 34 write-trivial plus 15 write-ordinary dispatches, descriptions such as "Commit flow log" (L220, L303, L396, L723, L844, L990, L1097) and "Retry commit of records" (L1676, L1726).
- edf227 ran its own publish as one compound command, 13 times (first L259, last L2204). Each contains lock, fetch, commit, duplicate, resolve, push, release.
- 41fa34 ran 0 git, 0 lock, 0 hm-send in its own shell; its 67 log appends are `apply_patch` or python heredocs. Its coordination is 372 collaboration messages to subflows, bodies encrypted, so not classifiable.
- 42265e (Field executor) runs jj itself; 18 Lock requests (11 Locked, 7 LockRejected), 6 Release commands.
- Re-reads: own log.md read 2 times by 42265e (L325, L562) and once by 41fa34 (L443). Re-reading to find one thing shows as 18 reads of `/tmp/field-flow-main-fix-42265e.path` (L7951 - L8065), 12 of `/tmp/flow-current-private-42265e.path` (L8122 - L8214) and 7 views of `flow-nexus/src/herdr/launch.rs` (L7376 - L7783).

## 3. (b) Stalls and failures, each with its line

### 28d847
- Message resent. L123 `hm-send 5578cc ...` then result L124: "messenger-clj: Set FLOW_ID to your own flow ID before sending". Resent identically with `FLOW_ID=28d847` at L126. 1 resend.
- Wait on another flow. L138 (subagent result): "Retire 5578cc: not done, held as the coordinator ordered until `flows/5578cc/` is on main." Main then told 42265e about lock 13054 (L147, L153) and 13066 (L184).

### 5578cc
- Lock refused, subflow stopped, work parked: 6 times.
  - L569: "The commit is blocked: another flow holds the PrimaryPublish lock, so I skipped the commit and push"
  - L1102: "`LockRejected.DuplicateName.{ 12093 PrimaryPublish holder41fa34 ... }`"
  - L1646 and L1685: "`LockRejected.DuplicateName.{ 12230 PrimaryPublish 9fb0ad ...`" then 12242 held by 9fb0ad again three minutes later
  - L2662: "`LockRejected.DuplicateName.{ 12569 PrimaryPublish 6e782c ...`"
  - L3521: "Blocked: the PrimaryPublish lock (id 13049) is held by flow 42265e, so I published nothing."
- Subflow re-dispatched: L1641 "Commit records and log", then L1676 "Retry commit of records" (refused, L1685), then L1726 "Retry commit of records" (landed, L1737 `c5a4117a`). 3 dispatches, 1 landing. Also L395-L638: book commit skipped at L569, re-dispatched L638 ("Commit book source and log").
- Conflict reconciled by hand: L226 "The duplicate of my commit onto `main@origin` conflicted in `flows/index.md` (a 2-sided conflict)... abandoned the copy", re-dispatched L255-L268 "I resolved the conflict as you ruled. `flows/index.md` keeps all of `main@origin`'s lines". 1 conflict, 2 dispatches.
- Data loss and recovery (cross-flow): L2618 "All 28 files of flows/5578cc/ are back on disk... Psyche Fable edf227 caused it at 11:59 to 12:00, while publishing its own records." Dispatches L2401 "Recover shared working copy", L2589 "Restore my lane's missing files", L2644 and L2688 re-publish; main also sent a 4-recipient urgent notice (L2622).

### edf227
- Subflow re-dispatched after "no block": L777 "I did not publish anything. The transcript has no presentation block titled exactly «Flow»" (dispatch L730, re-dispatch "Book: Flow (content in brief)" L788); again L1022 "The transcript has no block titled «A flow and its role»" (re-dispatch L1026). 2 re-dispatches. Main logged the cause at L1039.
- Lock waited and copy redone: L1086 "the lock was held by another flow at first, so I waited for it. My first copy was based on an older main, so I duplicated again".
- Lock released too early: L1761 and L1999 "I released the lock once before the push had gone through, then took it again" (2 books).
- Data loss from the 5578cc incident: L532 `ls flows/edf227/vision` "No such file or directory"; `vision/incorrectness.md` written at L526 and again at L560 (same file, 2 writes); recovery dispatch L555, result L586 "I restored 22 paths from 64cf1b2e"; "One message did not reach its flow: f1c841 is retired".
- Fix flagged by main itself, L2235 (hm-send to 42265e): "`jj resolve --list` prints 'No conflicts found at this revision' as an error with a nonzero exit". WITNESSED in all 13 publish compounds: each result begins "Error: No conflicts found at this revision" (L837, L929, L1208, L1278, L1691, L1775, L2044, L2213 ...). That is 13 of 13 clean publishes printing a false Error.
- Irreversible action by a subflow: L1891 "I saw 'forget and delete nothing' only after the deletions finished... all 51 work trees are gone."

### 6e782c
- Message refused, then outage: L581 (result of L580) "messenger-clj: Reservation refused: Unreachable.{ /run/user/1001/orchestrate-nexus/orchestrate.sock «Signal archive validation failed» }". Diagnosis dispatched L588; result L606 "Every `hm-send` is failing because the new `orchestrate` 0.37.0 client is now on PATH, but the Nexus behind the socket is still 0.35.0."
- Messages sent to a retired seat: L474 "None of the comments reached Fable 9fb0ad. Every send was refused with `messenger-clj: Retired: 9fb0ad`... I sent nine of the 15 comments, all with rc=1". Relay re-dispatched to the right seat at L640 (result L645 "all four returned `Transported`").
- Relay dispatched 4 times for one comment batch: L469, L582, L640, L656 ("Relay ... to Fable", "to Opus properly", "to Fable edf227", "to Opus").

### 42265e (Codex)
- LockRejected, 7 of 18 Lock requests (own transcript, WITNESSED): L7550 `PathOverlap ... 12728 Dea0baFlowReportCorrections dea0ba`; L8037 `12798 Dea0baHome82Report`; L8611 `12867 Dea0baHome82Outcome`; L9093 `DuplicateName 12940 PrimaryPublish edf227`; L9425 `13024 PrimaryPublisherCorrection41fa34`; L9516 `13054 PrimaryPublish 28d847`; L9548 `13066 PrimaryPublish 28d847`. Three of the seven fall in 20:17 - 20:22, other seats' publishes colliding with Field's.
- Waits: 30 wait_agent calls, 3 sleep calls, 3 interrupt_agent calls (first at L36, 18:07, "interrupted and replaced" per log line 19: a subflow launched with the wrong inheritance, re-dispatched).
- 22 non-zero exits of 297 commands (7.4%). Examples: L9501 `set -e ... jj resolve --list` exit 2 stopped a publish sequence while the lock was still held (then L9516 `Released.{ 13049 ...}`); L8490 "flow-id claim helper refused the native identity: ... No such file or directory"; L8751 exit 130 then L8757 exit 127.
- Log-attested only, 10-02 (bodies encrypted; `flows/42265e/log.md` lines): own-log conflict resolved by hand (157-163); rebase incident and publication freeze (199-207); its own lock 10813 blocked every publisher (251-257); "command-sequencing mistake nevertheless created scoped own batch commit df8a0df1 after rejection" (340).

### 41fa34 (Codex)
- No non-zero exit and no LockRejected in its own shell (0 of 77), because it publishes through subflows.
- Subflow reuse: 90 `followup_task` to `verify_and_coordinate`, 95 to `review_landed_batch`; 11 spawns, none re-spawned under one name. Re-dispatch of failed work not determinable (bodies encrypted): not claimed.
- Log-attested (`flows/41fa34/log.md`): line 174 "Own-path publication acquisition stopped on Field lock 12278... no retry"; line 71 "Opus froze Primary publication pending reconciliation".

## 4. (c) Elapsed time and mechanical fraction

Elapsed: see section 1. Active hours: 28d847 0.25, 5578cc 6.86, edf227 3.32, 6e782c 1.87, 41fa34 10.7, 42265e 12.4 (WITNESSED, 30-minute gap threshold). Total tool calls by main: 5578cc 255, edf227 166, 6e782c 47, 28d847 38; Codex 41fa34 467, 42265e 791.

Mechanical fraction (ESTIMATED; "mechanical" = log append, publish, flow-id, index and open-list bookkeeping, plus subflow dispatches whose description is commit, publish, tell, relay, register, fetch or book publish; judgment = reading, research, ruling, vision capture, message content):

| flow | bookkeeping shell cmds / all main tool calls | mechanical Agent dispatches (by description) | combined mechanical share of main tool calls |
|---|---|---|---|
| 28d847 | 8 / 38 | 5 of 8 | about 34% |
| 5578cc | 57 / 255 | 44 of 75 | about 40% |
| edf227 | 46 / 166 | 26 of 37 (20 are book publishes) | about 43% |
| 6e782c | 14 / 47 | 7 of 17 | about 45% |
| 41fa34 | 68 / 467 | not classifiable (bodies encrypted) | about 15% pure bookkeeping; the other 372 calls are messages to subflows |
| 42265e | 109 / 791 | not classifiable | about 14% pure bookkeeping; 436 are messages, 57 jj, 46 reads |

Reading (ESTIMATED): about 35-45% of a Psyche seat's tool calls are judgment-free bookkeeping. The 75 hm-send in 5578cc (29% of its calls) mostly forward the living's words; counting them mechanical would lift 5578cc to about 70%, not checked per message. The Codex seats' own bookkeeping is 14-15% of calls; the rest is delegation traffic, and 42265e is the one that holds locks and sits through refusals.
