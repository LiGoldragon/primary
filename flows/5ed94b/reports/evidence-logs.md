# Mechanical work flows do by hand: evidence from logs and reports

Survey for Psyche Fable 5ed94b. **W** = witnessed (I read it in the named log, report or live state); **S** = supposed (my inference). Quotes are from `flows/<id>/log.md` unless named otherwise; a quote shows what that flow recorded, not a re-check of the event.

Coverage. Read nearly in full (lines cut at ~330 characters): logs of 28d847, 5578cc, 6e782c, 01e496, d86ec0, 7de94a, 844491, edf227, 9fb0ad, 91ea9f, f1c841. Grepped only: 42265e, 41fa34, dea0ba, 3ec648; the other ~345 logs for counts and a few instances. Reports read: three (see Sources). Skipped: the other ~1130 reports and every summary.md. Counts over all 360 logs (W, grep): "conflict" in 72 flows, "Transported" 444 lines in 39 flows, "regenerat" in 91 flows, "lost|wiped|dropped|disappear" in 81 flows.

## 1. Publishing to Primary (lock, commit own paths, copy onto main, push, release)

- **What flows do (W):** compensation-primary-commit as a hand sequence: Orchestrate `Lock` PrimaryPublish on the sentinel, `jj commit` own paths, `jj duplicate` onto main@origin, `jj resolve --list -r <COPY>`, set main, `jj git push`, `Release`, then message whoever was waiting. Most flows send this to a subflow.
- **Instances (W):**
  - 01e496: "interim Primary publication rule sent to all seats — PrimaryPublish Orchestrate lock around commit of own paths, rebase on main@origin, push, release".
  - 9fb0ad: "Lane published: copy 9c2e3a on main … lock 11778 released; dea0ba told" (about 8 such entries in one day).
  - 3ec648: "the rebase of this flow's commit onto origin main produced a conflict … Push rejected; local main bookmark sits on the conflicted commit".
  - f1c841: "Log publication conflicted … a subflow reconciles", then "The 'conflict' was a misread by the haiku publication subflow".
- **Cost (W):**
  - 5578cc: "My lane's records (26 files) had been deleted at 12:00 by edf227's publisher (an unscoped jj commit then abandon in the shared working copy)".
  - 5578cc: Astra's rebase "had rewritten six files on disk (my log with conflict markers, flows/index.md, …)".
  - 91ea9f: "a transport-only subflow, briefed 'run no jj command', executed the publish sequence … and pushed … while Mind Sol held PrimaryPublish".
  - 42265e: "A command-sequencing mistake nevertheless created scoped own batch commit df8a0df1 after rejection, without a held publication lock".
  - Primary was frozen across several quiet windows on 10-02 (91ea9f, 41fa34, d86ec0), until "Tell Opus to just figure it out and just make it work" (the living, 91ea9f).
  - 28d847: "The working copy lost an unpublished file of mine during a publish."
- **Tool or design (W):**
  - The living ordered "one command: fetch, commit the named lane paths, put onto main, check conflicts, push, release; flows never type jj in Primary" (5578cc).
  - `tools/primary-publish.mjs` and its test exist, but git status shows them Added and uncommitted.
  - 28d847: the single publisher design is "designed only; no review verdict, build or holder on record".

## 2. Waiting on a lock and asking who holds it

- **What flows do (W):** a refused Lock names the holder. The flow messages the holder, asks for a release notice, and retries by hand when the notice comes.
- **Instances (W):**
  - 9fb0ad: "Publish attempt 2 rejected: PrimaryPublish 11771 now held by f1c841". Also: "publish subflow told to notify dea0ba on release".
  - 9fb0ad: "42265e: believes 9fb0ad holds PrimaryPublish 11776 … Both 11776 and 11778 are released".
  - 42265e: "Requested that the index lock owner add the successor entry or release the lock", then "Field Astra confirms lock 10676 is released".
  - 41fa34: "Own-path publication acquisition stopped on Field lock 12278 … one Messenger release-event request transported".
- **Cost (W):**
  - A flow forgets its own lock and blocks everyone. 91ea9f: "lock 10813 SkillBatch42265e … held under your own id and blocks every PrimaryPublish, mine included, and you report it blocks you."
  - Books sat uncommitted waiting on locks (9fb0ad: "source uncommitted (PrimaryPublish held by 42265e)", 4 instances).
  - edf227: "Lock release answered UnknownLockId though the lock was gone".
  - Older: 098f27 got DuplicateName on index.md against a lock held by d32329. 6fe957 needed a stale-lock takeover of 7359.
- **Tool or design:** the stale-lock skill exists (W). I found no release subscription in Orchestrate in these records (S). trial-no-polling forbids polling for it (W, skill list).

## 3. Lock requests written by hand in datom

- **What flows do (W):** compose `orchestrate 'Lock.{ Name id [ paths ] reason }'` by hand.
- **Instances (W):**
  - 3ec648: "Twice today the lock client rejected a reason in guillemets or curly quotes with an arity error".
  - 5578cc: "Field Sol's Curriculum lock failed with a frame I/O error; its request quoted paths in ASCII quotes".
  - 7de94a and 42265e: "cleanup lock stdout Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 13 } } with exit 0".
- **Cost (W):** cleanup was held on 10-02. A diagnosis loop ran between Field and Mind (42265e: "provide the exact lock-error command and typed Unreadable Arity output"). checks-inventory #11: the refusal arrives as a fake "Unreachable".
- **Tool:** only the raw client (S).

## 4. Claiming the flow id and passing FLOW_ID down

- **What flows do (W):** the first log line is a hand claim ("FLOW_ID edf227 claimed", "Flow id 9fb0ad claimed", 7de94a: "Canonical identity obtained with flow-id codex --flows-root /home/li/primary/flows"). Briefs carried `$subflow`, FLOW_ID and FLOW_DIRECTORY by hand.
- **Instances (W):**
  - 5578cc: "the Claude main-flow skill itself says 'Put `$subflow`, `FLOW_ID`, and `FLOW_DIRECTORY` in every subflo[w brief]'"; the living saw Codex notation in a Claude brief.
  - 91ea9f: "failed in its subflow on a FLOW_ID validation error no other send hit today".
  - 1b8ac0: "on a flow-id collision, created an empty lane 836818c before stopping".
  - In this session (W, live): `FLOW_ID` and `FLOW_DIRECTORY` are both empty, and git status shows root markers `.5578cc.flow-id` and `.5578cc.flow-id.lock` staged as added files.
- **Cost (W):** the living intervened on `$subflow`, and 5578cc spent a full landing round on it. The living: "there's no reason for us to make the model check the flow ID" (checks-inventory #6).
- **Tool or design (W):** the flow-id helper exists. Flow 0.22+ exports FLOW_ID for Claude, never for Codex (f1c841). Mind Sol decided the launcher should export it with "missing value fails", but that is not built (checks-inventory #6).

## 5. Succession, registration, retirement and reaping

- **What flows do (W):** write handover.md, launch the successor through a launcher script, register with hm, then hm-retire the predecessor, close its pane, and witness that it is gone. They split reaping duties by message.
- **Instances (W):**
  - 9fb0ad: "Settled: 9fb0ad reaps f1c841, 91ea9f, 3ec648; 5578cc reaps d86ec0, 01e496", agreed across three #msg exchanges with 5578cc and 6e782c.
  - edf227: "registered … (launcher had done it; re-register printed Registered)"; "its pane and hm-list row still read done, pane not killed".
  - 9fb0ad: "Retired f1c841: delivery is blocked before Herdr routing … f1c841's session is still alive".
  - 28d847: "It was still working when closed; the retire request was not acknowledged beforehand."
- **Cost (W):**
  - Successor launches were refused by the launcher's VCS guard (91ea9f: "main is not an ancestor of @ … No seat started"; also 3ec648).
  - 844491 was "Aborted … Codex's hook-review dialog held the launch and the launcher timed out … Never registered".
  - Retired seats stayed alive (f1c841: "Audit D also reports the retired seats 91ea9f and 3ec648 still running").
  - A dying seat's subflow left work unpublished (d86ec0: "successor to check and publish").
- **Tool or design (W):** `tools/reaper`, `tools/reap-flow`, hm-retire and the launchers exist. Flow Start is meant to replace the launchers but was still refused in private runs (`BindingRefused`, 5578cc; edf227 20:09). The trial-succession and trial-reaping skills exist.

## 6. The flow index and lane bookkeeping

- **What flows do (W):** take a lock on `flows/index.md`, append their row, verify it once, release. Then log "Index entry and title landed".
- **Instances (W):**
  - 42265e: "Acquired shared-index lock 10696 … verified it occurs once at flows/index.md:260".
  - 7de94a: "Main appended its flow index entry under Orchestrate lock 10676".
  - 01a0539e: "initially appended its flows/index.md row before observing the remembered stale Lock 19".
  - 28d847: "Index entry and title landed".
- **Cost (W):** index.md was among the files a rebase rewrote (5578cc), and among likely conflict sites (3ec648). Lock waits are covered under gap 2.
- **Tool:** none found (S). Flow's store already holds flow rows (S, from f1c841 "26 flow rows").

## 7. Regenerating .agents/.claude/.codex/.pi

- **What flows do (W):** edit Curriculum, run the generator and Check ("Generate/Check 68/24"), then publish the projected paths in Primary through gap 1. Only Field does this, so other flows wait.
- **Instances (W):**
  - 3ec648: "Primary's generated trees still carry the old skills until Field regenerates".
  - 91ea9f: "the generated book agent definition is a stub (Haiku, no procedure) while its authored source names Opus".
  - 91ea9f: "The regeneration swept in vocabulary".
  - 3ec648: "The seat that ran rebase -r today … loaded the older projection."
- **Cost (W):** a bookmaker failure needing two retries (91ea9f); a stale skill behind a data-loss rebase (3ec648).
- **Tool or design (W):** the curriculum-deploy generator and Check exist, and trial-generated-projection makes the model run them. checks-inventory #18: "the regenerator's Check already does it". No trigger regenerates on a Curriculum push (S).

## 8. Own log overwritten, then restored from the transcript

- **What flows do (W):** append to log.md by hand while subflows copy or rewrite the same file.
- **Instances (W):**
  - edf227: "The write subflow for the anatomy also rewrote this log from a stale copy and dropped five entries".
  - 3ec648: "(re-logged; the line was lost when the repair subflow copied the resolved log over the disk while this flow appended)"; "The disk log had been a 20-line headless fragment".
  - 7de94a: "two earlier successful log append calls … found those … paragraphs absent; cause remains unknown".
  - 41fa34: "Expected earlier handoff-event lines were absent … Events restored from this flow's witnessed transcript".
- **Cost (W):** re-logging, and a lesson pushed into briefs (edf227: "name the one file to touch and say the log is not to be written").
- **Tool:** none (S). An append-only log writer would remove this whole class (S).

## 9. Timestamps guessed

- **Instances (W):**
  - 9fb0ad: "the stamps 12:54Z–13:08Z above were estimated and ran ahead of the clock".
  - f1c841, three times: "Entry times from 01:25 on were again estimated late".
  - edf227: "stamps from 17:45Z on had been guessed and ran up to an hour fast".
- **Cost (W):** rewritten logs; wrong times in commit messages (f1c841).
- **Tool:** nothing stamps entries (S).

## 10. Fetching and relaying the living's comments

- **What flows do (W):** list their books, fetch comments by hand, log them verbatim, then relay them to other seats in a message.
- **Instances (W):**
  - 5578cc: "Also found an unread 15:11 comment on «May Field speak to Psyche?»".
  - f1c841: "A missed comment of his on «Ethos as two skills» (2026-10-02T23:23Z) is now logged".
  - 5578cc: "a session holds at most 10 artifact watches; a watch started by request does not arm comment wake-ups".
  - 6e782c, relaying 18 comments: "You really fucked up. You sent them giant hashes."
- **Cost (W):**
  - The living had to say twice that he had commented ("And I did comment on something, so").
  - Duplicate books on one question (9fb0ad: "Duplicate of «Two meanings for Flow»").
  - A skill fix had to be made (skills-9tl, operation-relaying-the-living).
- **Tool (W):** the living asked: "Is there some kind of hook that could notify one of the voices … that a comment has been put into a Claude artifact?" (5578cc). `tools/book-fetch.mjs` exists (I did not check what it does).

## 11. Coordination traffic carried by message

- **What flows do (W):** every state change becomes an hm-send "told X", often through a subflow, logged with its "Transported" receipt (444 lines in 39 logs).
- **Instances (W):**
  - 9fb0ad 13:06–13:11: "Review and the three #psyches resent to 41fa34 … Review package copied to 7de94a".
  - 3ec648: "the held orchestrate diff was addressed to the registered name field_sol_42265e instead of the flow id".
  - 91ea9f: "a relay subflow read 'report the typed replies' … and set a two-second monitor on them".
  - Deployment timeline: "Psyche Opus 5578cc's 16:04 brief to Field Sol did not carry 9fb0ad's attempt, report or fix, so Field rediscovered the guard."
- **Cost (W):** the living, to 9fb0ad: "Why is everybody bothering you with things that you shouldn't be bothered with?" and "So you started a sub-agent just to answer a message. Is that cheaper than answering the message directly?" There was also about 2.5 h with no executor (deployment timeline).
- **Tool:** the messenger transports messages but holds no shared state that other flows can read (S).

## 12. Deployment state and retry by hand

- **What flows do (W):** build the Lojix request by hand, pin store paths by hand, and ask Field which versions are running.
- **Instances (W):**
  - Deployment timeline: "deployment 79's record keeps neither the Horizon artifact nor the transport tuple … a retry is not one command".
  - checks-inventory #13: "a model builds a 14-field request by hand".
  - 5578cc: "stable flow-nexus now runs 0.23.0 (the 0.12.2 reading was stale)".
  - edf227: "PATH flow client still 0.12.2 … Field told: clients must match servers".
- **Cost (W):** an order from 12:40 that was done after about 19:28 (edf227). Deployment 81 failed on a guard pinned by hand (5578cc). The living: "I feel like there's a problem with things actually happening as I ask them."
- **Tool:** none for running-set state or retries (W, checks-inventory #13).

## 13. Hashes and provenance receipts kept by hand

- **Instances (W):**
  - 41fa34: "Accepted review-only knowledge-Codex report SHA256 8530d143…"; "Delegated review of uncommitted authored knowledge-codex.md at SHA256 4baf8777…".
  - checks-inventory #17: "'Deterministic code retains and compares raw checksums'. No such code exists."
- **Cost (W):** review cycles keyed on hashes, and the living's "no hashes in a model's context".
- **Tool:** none (W).

## 14. Permission prompts that stall seats

- **Instances (W):**
  - blocked-commands.md: 6997eb's `rm -rf $S/$n` waited "11 h 20 m".
  - blocked-commands.md: 3ec648's rm waited 54 min until 01e496 declined it ("Opus declined it via Escape in its pane").
- **Tool:** none; only hand `${S:?}` rewrites (3ec648) (W).

## 15. Worktree inventory and cleanup

- **Instances (W):**
  - 91ea9f: "87 worktrees and workspaces, 28.9 GB".
  - edf227: "my subflow had already removed all 51 made today".
  - 3ec648: "its subflow deleted a standalone worktree … before the required remote-branch preservation"; the content was "reconstructed (not byte-exact)".
- **Tool (W):** `guarded_remove.py` exists. Whether flows use it is unchecked (checks-inventory #23).

## Sources

- Logs: `flows/{28d847,5578cc,6e782c,01e496,d86ec0,7de94a,844491,edf227,9fb0ad,91ea9f,f1c841}/log.md` (read), `flows/{42265e,41fa34,dea0ba,3ec648}/log.md` (grepped), and the other logs grepped for counts and instances (098f27, 01a0539e, 1b8ac0, 6fe957).
- Reports: `flows/28d847/reports/checks-inventory.md`, `flows/5578cc/reports/deployment-timeline-2026-10-03.md`, `flows/f1c841/reports/blocked-commands.md` (§1).
- Live: `git status` in /home/li/primary (tools/primary-publish.mjs Added, `.5578cc.flow-id` Added), `ls tools/`, and an `echo` of `FLOW_ID`/`FLOW_DIRECTORY` (both empty).
- Provenance receipt: unavailable (no receipt handoff; FLOW_ID empty in this subflow).
