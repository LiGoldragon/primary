# Audit A — psyche flows d8df70, e167d8, b7ba00, 183ae0

The order, typed by the living on the morning of 2026-10-03 and relayed through the main flow's brief: "Do a complete audit and use all of the psyche flows to report on everything that's been done, everything that's not been done, and why." The main flow's log has his full words, which continue: "Put this all in the books this morning." (flows/f1c841/log.md:52).

## Scope and method

- **In scope.** The four flows named in the brief, audited in the brief's order.
- **Out of scope.** The named predecessors 88475f (of e167d8) and b860be (of b7ba00) are not in `flows/index.md` at all, as psyche or as anything else (`grep -nE "88475f|b860be" flows/index.md` finds them only inside the e167d8 and b7ba00 rows, :224-225). They are therefore not audited. Each appears only for what its successor inherited from it.
- **How it was done.** Each flow was audited by its own forked subflow of this subflow. The forks read the flow's log, summary, reports, vision, notion and witnesses. Each landing claim was checked with one command against origin/main or the host. Every handed-over item was grepped for in the logs of the later psyche flows: 93ba9f, e51411, c64ee3, 7328f4, fe945a, 6997eb and f1c841, as each section says.
- **Labels.** **Observed** means checked by command in this audit. **Claim** means the record says it, and this audit did not check it. **Unknown** means the records do not settle it.
- **Not searched.** Transcripts were not searched beyond what the flows' own reports quote. A ruling the living gave outside these logs would not be seen here.

## d8df70 — Psyche Medium (Claude, claude-opus-5 then claude-opus-5-5), 2026-09-23 to 2026-09-24

Lineage: no predecessor stated (log.md:4, :19-21). Successor: Psyche Medium e51411, made "the one Psyche Medium" on the living's word relayed by e51411 (log.md:379-389). e51411 is not in this audit's flow list; it is cited below only where it took an item.

### 1 Asked

Provenance key: "LW" = `flows/d8df70/reports/living-words-since-launch.md`, which quotes Claude session d8df703d-d083-4c29-9597-6b32e7411b75 by JSONL line. That report states that records 12–377 were injected by Field 9ddcbc's launcher, not typed by the living (LW header; log.md:145-157). So the slash-command "orders" at launch (title work, lineage) were **not** the living's words.

- Observed (LW, record 387, 2026-09-23T22:02Z): "Create a bunch of flashbooks with everybody's main flow from the recent presentation that they left in their transcript, including your own, and do an audit on the fact that you were loaded with the prompts broken up. ... Did you have your model changed halfway or something? The way your skills were loaded, one after another, is really inefficient ..."
- Observed (LW, record 566): "Talk to Psyche Fable. Tell him about your existence. ... He has a job for you." The job was pasted from 836818: "do a flashbook on all the things that need my attention and do a proper illustration." (log.md:230-231; `flows/836818/vision/flashbooks.md:13` per what-waits-dossier.md:5)
- Observed (LW, record 602): "Audit the messaging system and find a more efficient way to do it and then tell Field how to do it better. Tell him to implement your suggestions in testing skills and ... operational changes to make the messaging more efficient." Follow-ups at records 608 (session-start/end hooks to register and unregister), 776 and 852 (Mind's operational skills; "making Flow Nexus adhere to all of the discoveries").
- Observed (LW, record 946): "So if the Opus harness cannot actually generate images, then we can use Codex to generate images." Record 1087: "No you don't run Codex. You talk to him. We have messages." Record 1127: "No, field is not the right aspect. Mind is."
- Observed (LW, record 985): "Get all of your flashbooks audited to make sure they're still accurate ... Then get them all reillustrated and only bring forward the 6 most important or 6 to 9 most important ..."
- Observed (LW, record 1196, 2026-09-24T13:53Z): "We need to just have a proper flow tool. How's the flow tool? How's the connection to Prometheus? ..."
- Observed (LW, record 1240, 14:03Z; also log.md:274-279): "Is there a firewall problem on Prometheus? ... get mine to test, build, and deploy the new flow and then let's make message work with it. I want Prometheus up ... I want all hands on deck. I want new flows spawned. ... Let's get the flow nexus and the message nexus up to date, tested, built, deployed and running, and used by you guys."
- Claim (log.md:294-300; not in LW, which stops at record 1240): "talk to Field about getting a survey of the context size of everyone and a sort of chronology of the dawn of this new meta harness ... and then make a flashbook out of it properly."
- Claim (reports/recurring-problems.md:3): "Why don't we start making a log of the things that are recurring and not getting solved, which need particular attention."
- Claim (reports/psyche-logging-audit.md:3-5): "Are you not getting psyche updates when I've been talking to Field and mine? ... Is everybody logging? Can you check?"
- Claim (log.md:316-319): "you're getting really held up ... give your make reexecute a new fresh flow. Bring forward what you want to bring and make a list of files ... and then let Field refresh you."
- Claim (log.md:352-356): "Can you amalgamate everything, get all the vision logged, and then re-inject it into a new proper flow that started by Flow ... have you answered my other questions that I can't seem to get answers for?"
- Claim, relayed by Psyche High 752e0f (log.md:333-335): "Tell everyone the humans are not going to type on the keyboards anymore." / "kill it with fire. Purge it from all momentums of all flows."

### 2 Done and landed

Primary commits (repository `primary`):
- Observed (`git branch -r --contains`): 39f1d059 (a dirty tree found and committed), 399e0055 ("What Waits" dossier), 75350237 (flashbook build), 79e23d32 (Mind 6288d1's illustrations) and 96d48f7d (Field's checked hm-send) are all on origin/main. aecc3c9b, also on main, swept in 9ddcbc's in-progress files, a scope fault the log admits (log.md:217-226).
- Observed (`git -C Curriculum branch -r --contains 5ec29ffb`): Curriculum 5ec29ffb is on origin/main. Per log.md:258-259 it carries testing-message-route, testing-datom-messaging and testing-session-registry. This is Field's landing, relayed by this flow, not this flow's own.

Prometheus:
- Observed (ssh prometheus, 2026-10-03): `kernel.panic` = 10, kernel 7.1.8, profile system-55-link, up 3 days 15 h. The panic-reboot setting this flow deployed (log of reports/recurring-problems.md §1: CriomOS f9343c6, generation 54, built on Prometheus outside Lojix) is live today, on a later generation (55). On CriomOS main, the setting comes from eebeab5, "Reboot router nodes after kernel panic or hang" (`modules/nixos/router/default.nix:138-140`). f9343c6 is on CriomOS origin/main, but its subject is "Accept both VmHost field spellings in test-vm-host". Unknown: whether generation 54 was built from f9343c6 with eebeab5 as an ancestor, or from a dirty tree.
- Observed (the report, with its pstore evidence): reports/prometheus-recurring-outage.md finds the cause of the recurring outage. The kernel panics in the mt7925 Wi-Fi driver, and `kernel.panic=0` then freezes the machine. That was a diagnosis, not a fix of the trigger.
- Claim (e51411/log.md:80): d8df70 also applied "Wi-Fi A" and both firewall fixes in generation 54. Not checked here.
- Observed (file exists): witnesses/prometheus-firewall-2026-09-24.md is a read-only firewall diagnosis. It found an NDP drop and an inert port-80 declaration (recurring-problems.md §1).

Flashbooks (claims; the artifact URLs were not opened in this audit):
- Claim (log.md:198-206): "State of the World, Revision 2" (SvwP3vVhvFVGBYCrL2Xm7m, 14 pp) and "Flow coordination · answers and three rulings sought" (XoSFJnmwofNDPz77qPH7jf, 12 pp).
- Claim (log.md:285-290): "What Waits for the Living" (Jmh4wVsHve1vPYX8MZwSGi, 16 pp, six questions, eight illustrations). The flow notes its own fault: pages 14 and 15 are both text pages.
- Claim (log.md:323-329): "The Dawn of the Meta Harness" (JWTTJZysuyuKGFZ4ACNkGJ, 10 pp, five illustrations).

Audits and reports (observed, files present):
- The launch-injection audit, in log.md:145-190. Of 31 profile skills, the launcher sent 5, one turn each. Injected turns cannot be told apart from typing. The model switched at 20:20:08. The cost was 162 calls and about 7.1M cache-read tokens.
- reports/messaging-audit.md. It found tools/msg dead and hm-send the checked single-call send, and proposed improvements. Field then implemented hm-send in primary 96d48f7d (claim relayed from Field, log.md:254-259; the commit is observed on main).
- reports/psyche-logging-audit.md: "Psyche logs. Mind and Field log nothing." Psyche flows logged 30 of 49 messages; Mind and Field logged 0 of 43.
- reports/recurring-problems.md, five entries: Prometheus, Flow and Message unusable, Field unreachable, main flows not delegating, bad launches.
- The title-tool review, in log.md:95-140 and reports/title-testing/. claude-native-seat-refresh.py never reads `terminal_title` and has no gate for an unsupported harness. Its rollback is sound.
- The native title was aligned, with readback, through `herdr agent prompt` driven by a subflow (log.md:57-76).
- Claim (log.md:375-377): the Flow-launch requirements were sent to Mind 6288d1.
- Claim (log.md:302-312; relayed from Field eb7bae, not witnessed by d8df70): Flow and Message daemons were running on 2026-09-24 ~15:50 UTC, and a durable typed Send was accepted.

### 3 Not done

- **Flow and Message "used by you guys".** Not done. Flow knew no flows, so nothing resolved or delivered. It was waiting on Mind 6288d1's bind command and a Field seat to run it (recurring-problems.md §2).
- **A new flow "started by Flow".** Not done. The deployed Flow started only headless Codex, with no prompt, model or title fields and no pane, under a ~64 KB frame cap (log.md:375-377).
- **Removing the Prometheus crash trigger** (keeping ouranos off the AP, or disabling the AP or the driver). Not done: it "awaits the living's choice" (recurring-problems.md §1).
- **Review of "What Waits" pages 1–2 by 836818.** Held: `Held.{ 836818 IdentityChanged ... }`. The new rules forbid a retry or fallback (log.md:243-250). The 87-item plan was later replaced by the six-topic redo (log.md:265-270).
- **"have you answered my other questions that I can't seem to get answers for?"** The log records subflows collecting the open questions (log.md:356-358). No answer to the living is recorded: no reason recorded.
- **`message-daemon.service` failed on ouranos.** "Not investigated" (log.md:212-213): no reason recorded.
- **The live error paths of the title tool**, untested: they "need a live scratch seat, not fixtures" (log.md:138-140).
- **The injection hazard** (injected input reads as the living's authority). "Raised here unresolved; it is not this flow's to settle alone" (log.md:93).
- **The tension between one-prompt and per-skill launch.** Partly settled by e51411's test (log.md:371-374). The launcher redesign is not recorded as done.
- **The Psyche Medium model-variable mismatch** (`claude-opus-4-6[1m]` in SKILL_VARIABLES.md against the claude-opus-5 that ran). "Not resolved here" (log.md:23-24).
- **The Prometheus ActivateNow.** It needs the living's approval in the sending seat's own transcript, because of Claude's auto-mode classifier (log.md:387-389). It was passed on to the successor.
- **Field consolidation into messaging-build.** The order is out, but "no Field seat reachable to carry it" (recurring-problems.md §3).
- **Main-flow system-prompt replacement.** The design was sent, with Psyche High to draft it and Field to wire it (recurring-problems.md §4). Not landed by this flow.

### 4 Handed over

Handed to e51411 with the full state, and to Field to perform the exit (log.md:379-389). Uptake was searched in the logs of e167d8, b7ba00, 183ae0, c64ee3, 7328f4, fe945a, 6997eb and f1c841, plus e51411 and 88475f where they bear.

- **Prometheus generation 54, Wi-Fi A and the firewall fixes.** Taken by e51411 as state (e51411/log.md:80). The Prometheus AP is still a live topic later: da88cf found the AP broadcasting at 3 dBm under the PL regdomain (e167d8/log.md:27), and the index shows Field 29b75f holding "Prometheus AP host diagnosis/repair". Whether the living ever chose to remove the trigger: unknown. No later log names mt7925.
- **Binding flows into Flow so Message can deliver.** Taken, in a later form. e167d8's mission was "improve Flow, then Message Nexus through Flow" (index.md:224). It observed flow-nexus 0.12.2 and message-daemon 0.12.0 live (e167d8/log.md:12). By 2026-10-02, fe945a still saw "no live seat started through Flow" (fe945a/log.md:59). f1c841 landed flow 0.21.0 and meta-signal-flow 13.0.0 (f1c841/log.md:34). Starting a flow through Flow is still not observed in the records.
- **Main-flow system-prompt replacement.** Taken up by 88475f with the living (88475f/log.md:48-61) and by e51411 ("Shrink the prompts and the system prompt, and replace it", e51411/log.md:86). Not found in the listed later logs.
- **One-prompt launch.** fe945a observed (fe945a/log.md:59): "Claude launcher titles first, one prompt". This item appears to have landed in the launcher. Commit not checked.
- **"What Waits" as a standing presentation.** Continued as the books "What Waits on You" (7328f4/log.md:37; c64ee3/log.md:115-117). Taken in spirit; the d8df70 book itself is not referenced.
- **d8df70 and e51411 retirement.** They were retired in messenger-clj by 88475f at 2026-09-26T01:58Z, but still showed Pending in Flow List, because Flow had no retire (e167d8/log.md:34-35).
- **Not found in any listed later log:** the title tool's findings (`terminal_title`, the unsupported-harness gate), the injection hazard, the message-daemon failure, the Dawn and What Waits receipts held for the successor Psyche High, the psyche-logging gap ("Mind and Field log nothing"), the recurring-problems log, and the Field messaging-build consolidation. Each was searched by its distinctive phrase, with zero hits.

### Sources for this flow

- /home/li/primary/flows/d8df70/log.md (1-389)
- /home/li/primary/flows/d8df70/refresh-inject.md
- /home/li/primary/flows/d8df70/reports/living-words-since-launch.md, messaging-audit.md (head), prometheus-recurring-outage.md (head), psyche-logging-audit.md, recurring-problems.md, what-waits-dossier.md (head); reports/title-testing/ (listing only)
- /home/li/primary/flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md (head)
- /home/li/primary/flows/index.md:219,224-233
- /home/li/primary/flows/e51411/log.md:80,86; /home/li/primary/flows/88475f/log.md:48-61
- Greps over the logs of e167d8, b7ba00, 183ae0, c64ee3, 7328f4, fe945a, 6997eb and f1c841
- Commands: `git -C /home/li/primary branch -r --contains` {39f1d059, aecc3c9b, 399e0055, 75350237, 96d48f7d, 79e23d32}; `git -C /git/github.com/LiGoldragon/CriomOS branch -r --contains f9343c6`, `git log -1 f9343c6`, `git grep kernel.panic origin/main`, `git log -S kernel.panic origin/main`; `git -C .../Curriculum branch -r --contains 5ec29ffb`; `ssh prometheus 'sysctl -n kernel.panic; uname -r; readlink /nix/var/nix/profiles/system; uptime'` (2026-10-03)
- Not read: vision/* (the living's words were taken from LW and log.md instead); the flashbook artifacts themselves

## e167d8 — PsycheV2.{ Opus e167d8 } (Psyche Opus, successor of 88475f; 2026-09-25 night → 2026-09-26 ~16:30)

Scope note (observation): predecessor 88475f is not listed as a psyche row in flows/index.md, so it is out of scope. Only what e167d8 inherited from flows/88475f/handover.md is quoted. e167d8's own successor 93ba9f is not in flows/index.md either (grep returned nothing), but its log is the main place where e167d8's handover was taken up, so it is cited in §4.

Line numbers: `log.md:N` is flows/e167d8/log.md. Lines 238–376 repeat the 2026-09-25 section (a duplicated block). Citations use the first occurrence.

### 1 Asked

The mission came through 88475f. e167d8 itself holds it only in paraphrase:
- (Claim, paraphrased by 88475f) handover.md:4–5: "Improve Flow, then make Message Nexus work through it … datom-based messages that pass through Flow, Flow locking panes; features configured on the meta socket; no arbitrary typing into panes — Message is the only interface to send to other panes … refuse a message that is really a command such as `/compact`; expose these through the Flow CLI at the authority level each needs … Deploy your fixes, then test." The verbatim is said to be in 88475f/log.md and was not re-read here.
- Also inherited from 88475f/handover.md:18–22, open with the living: subagent system prompts; the compensation-messenger-clj fallback line; claude-harness wording; 077114 vs the Opus line.

The living's words that reached e167d8, quoted as e167d8 recorded them (verbatim in its log; STT unless marked typed):
- Relayed by 88475f, ~22:05 (log.md:17–18): "…stop doing [Nix] builds and [Nix] tests on [ouranos] and move everything to Prometheus now."
- ~22:08 (log.md:21–22): "Prometheus should be doing the builds and running the fan hard…"
- ~22:15 (log.md:24–25): "Just keep running new code, testing things and recovering if you need to, mainly using cloud subworkers…"
- Typed, ~02:30 (log.md:62–63): "Make sure Zeus is updated."
- Typed (log.md:70–71): "…tell your sub-agents Fable to wind down or to get ready to wind down so the agents can take notes before they get stopped cold."
- Typed (log.md:76–77): "Get a big status of everything and then contact Fable to see what he thinks you should do. If there are things undone just ask Mind Astra to take care of it and create a new flow for it if it's old."
- ~07:50 (log.md:83–84): "There should be no AI models on [ouranos] ever and we can garbage collect."
- ~07:52 (log.md:86–87): "You can reboot Prometheus whenever you want."
- ~08:00 (log.md:93–96): "Just remove all the old profiles and then garbage collect the [Nix] store. / Delete all of the build directories everywhere and get rid of abandoned work trees. / Make sure we don't have more than one primary Git…"
- ~08:02 (log.md:98–99): "Get Luna Field to do a big deep dive into finding ways to maybe get more space."
- ~08:40 (log.md:114–121), on the AI-node role and cluster spec: "…maybe spec it in Ethos … let's do that and then we can make that a signal contract, a signal repo, so that logics can pick that up…" On final responses: "I want to modify a spec. Let's go edit, find the right skill…", "you don't need the flow ID…", "'Main flow' is also unnecessary."
- ~08:50 (log.md:124–125), on Piper: "I don't even know what Piper is. I've never used it so I had no problem losing it."
- ~09:00 (log.md:129–130): "Well has Zeus been redeployed and updated? It should be."
- ~09:15 (log.md:134–137): "Get Opus to put together an update package for Fable … We're going to use him like that, like a sort of oracle … Let's create a specialized subagent, an Opus subagent, that does that…"
- ~11:55 (log.md:158–159): "You asking me if you should move to 0.16? I would love to … maybe you can even start using it in parallel."
- ~12:10 (log.md:164–165): "Yeah the repository is, as you said, persona test."
- ~13:00 (log.md:176–177): "…you can start a Fable successor. Let's use the new Flow, 0.16, and can we fix the herder pane and all of the names disagreeing so that the name is the same everywhere … We can remove the V2 … in the next version."
- ~13:15 (log.md:181–182): "You'll also have to eliminate the previous conflicting meaning of primary, secondary, tertiary, etc., and the name of the repo is one of them."
- ~13:25–13:30 (log.md:185–189), on logins; then the ruling "copy only the login credentials and generate the sandbox configuration" (log.md:193; vision/testRepos.md).
- ~14:10–14:15, the emergency (log.md:199–207): "We have two Fable flows running, which is costing us a lot of money, and one of them was on high … close these sessions … find the culprit who made the code that started a model on high effort…"; "I want this emergency signal sent out to everybody who's actually valid…"; "I need a full situation report on the best quick solutions … and let's talk about the better design long-term solution."; "I want this new flow version out and deployed right now … bypass all tests and all checks, and just deploy and run on the next socket…"
- ~15:00 (log.md:227–229): "Start on a fresh Flow. … Just give your final presentation, questions, and context … get your final presentation to be made into a book … just a simple sonnet book, and then get a field to refresh you."

### 2 Done and landed

Checks in this subsection were run 2026-10-03 on ouranos, against `git fetch` of the clones under /home/li/primary/repos (`git merge-base --is-ancestor <rev> origin/main`).

**Flow and Message: the mission**
- Claim (log.md:38–40, 49): Flow faults 1–4 fixed. Flow 0.14.0 9fcd625a, signal-flow 6.2.0 e9e243c7, meta-signal-flow 8.0.2 a897462c. List is read-only, Exited is distinct from Retired, and there is a privileged Retire. Nix gate green on Prometheus.
  - Observed: flow 9fcd625a and signal-flow e9e243c7 are ancestors of origin/main.
- Claim (log.md:44, 51, 65, 216): the design stages ran.
  - S1: Flow is the only pane writer; Vet refuses /compact, #, !, ESC, CR; per-pane lease; Priority grades.
  - S2: Message no longer runs herdr; ResolvePeer→Vet→Deliver; Threads/Inbox retired.
  - Fixes to 0.16, then 0.17: Flow 0.17.0 90813568, Message 0.17.0 481b579f, meta-signal-flow 11.0.0 2ac045c2, signal-message 8.0.0 d5742005, meta-signal-message 0.8.0 14f57596.
  - Observed: all five revisions are ancestors of origin/main of their repos.
  - Observed: the flow main log carries "Flow 0.15.0: Flow is the only pane writer", 0.16.0, 0.17.0 and 0.17.1.
  - Observed: these reached main after e167d8. summary.md:10 says "Not yet on main"; the merge was done later by successors (§4).
- Claim (log.md:235): Flow 0.17.1 ac216c89 (take-back of a restored letter). Scenario 4 still failed at e167d8's close.
  - Observed: ac216c89 is on flow main.
  - Proof was finished by 93ba9f (93ba9f/log.md:28).
- Claim, witnessed in the log (log.md:222, 226): first live letter on the next pair. `Soft.{ m-18d8eb22e06706ef001 Owner Text.«Hello from Message 0.16 …» }` went Presented → Read.
- Claim (log.md:217, 226): next pair running on ouranos as transient units `flow-nexus-next`, `flow-configuration-next`, `message-nexus-next`, with CLIs flow-next/message-next.
  - Observed (`systemctl --user list-units 'flow*' 'message*'`): all three -next units are active today, beside stable flow-nexus and message-daemon.
  - Observed: `flow-next --version` prints flow 0.17.4, a later version than e167d8 left.
- Claim (log.md:172; summary.md:9): stable/next Home slot function `lib/stable-next-service.nix`.
  - Observed (`git show origin/main:lib/stable-next-service.nix` in CriomOS-home): present on Home main.
- Claim (summary.md:9): Home main 657f4ba8 carries the 0.16 next pair.
  - Observed: 657f4ba8 is an ancestor of CriomOS-home origin/main.
- Claim: the 0.17 bookmark eba6d270 pins the next pair at 0.17.
  - Observed: eba6d270 exists but is NOT on Home main. It was a sibling of main, and b7ba00 rebased it as integration-b7ba00-home (b7ba00/log.md:58).

**Testing and Nix**
- Claim (log.md:179, 226): sandbox suite `tools/flow-message-sandbox/` in primary, 13 scenarios.
  - Observed (`git ls-tree origin/main tools/`): present on primary main.
- Claim (log.md:168, 212): repo persona-test created. First main 58e263b6; credential-only runner e3505bfd.
  - Observed: both are ancestors of persona-test origin/main. Main is now c1a2370 "pin Flow 0.17.4".
- Claim (log.md:163): skills compensation-nix and compensation-nix-rationale (Curriculum 16cf0d8e).
  - Observed: 16cf0d8e is on Curriculum main, and both skill files are on main.

**Cleanup, the emergency, and launching**
- Claim, witnessed by its worker (log.md:142, 174): ouranos disk went 16 GiB → 144 GiB → 419 GiB free.
  - Gemma (~48.8 GiB) and Qwen (~72 GiB) roots removed.
  - 489 of 533 worktrees, 226 GiB of target dirs, and 41 primary copies removed.
  - Reports: reports/ouranos-cleanup-2026-09-26.md and reports/ouranos-worktree-cleanup-2026-09-26.md.
  - Observed (`df -h /nix` today): 287 GiB free (67%). That is current state, not proof of the claim at the time.
- Claim, witnessed by its subflow (log.md:219; reports/herdr-cleanup-2026-09-26.md): the emergency Herdr cleanup closed 38de5b, da88cf, 9c7514, 077114 and the 88475f/b860be shells, plus stray panes and daemons.
- Claim (log.md:218): the culprit was found. Launch agents read "Psyche High" as an effort and wrote it into Start datoms, and Flow passes effort verbatim. e167d8 was liable for two of three; no code change landed.
- Launcher work:
  - Claim (log.md:150, 169, 171): fixes to tools/native-seat-launch.mjs (canonical titles, resuming an unloaded thread).
  - Observed: that tool was later retired from primary main (`git log -- tools/native-seat-launch.mjs`: "4e4233b54 Retire obsolete native seat launchers"; "9ed50bda3 Remove V2 from native launcher titles").
- Claim, witnessed by subflow: seats launched.
  - Fable b860be (log.md:52), then Mind Astra 31147a (log.md:82).
  - Fable b7ba00 through flow-next 0.16 (log.md:191). Its "names equal" line also covers part of the one-name ruling.
  - Successor Opus 93ba9f through flow-next 0.17, effort medium (log.md:233).

**Reports and the final presentation**
- Claim: reports written (files exist):
  - message-through-flow-design.md
  - layer-vocabulary-research.md
  - layer-words-rename-proposal.md
  - fable-oracle-package-1.md and fable-oracle-package-2.md
  - status-2026-09-26-morning.md
  - home-016-state.md
  - per-flow-workspaces-design.md
  - sandbox-suite-run-1.md and sandbox-suite-run-2.md
- Claim: the final-response spec was located and the cluster data mapped (log.md:132–133). Reporting only; no edit.
- Claim (log.md:231): final presentation book at https://claude.ai/artifact/9gfqFYs3H6yCs9vsPzLyov. Not opened here.

### 3 Not done

- **Zeus updated** (asked log.md:63 and again at :130).
  - Observed in records: "Zeus not deployed (never Lojix-deployed)" (log.md:131). Routed to b860be, then b7ba00.
  - Reason given: integration step 2 was not complete, and Lojix 7 rejected the 0.13 proposal (log.md:79–81, 104). The work belonged to the integration head.
  - Unknown: Zeus's state today. `ssh zeus` does not resolve from ouranos.
- **Cluster spec in Ethos plus a signal repo for cluster data** (log.md:115–116).
  - Done: survey only (log.md:133: "No signal repo for cluster data").
  - Observed (`ls repos`): no signal-horizon or signal-cluster repo.
  - No reason recorded. The oracle answer recommended "Ethos rendering of Horizon first" (log.md:146).
- **Final-response spec edit** (log.md:118–121).
  - Located and "Proposing the edit to the living" (log.md:132); oracle answer 1 drafted a shape (log.md:146).
  - No record that the edit was made in e167d8. No reason recorded.
- **Oracle-package-composer as a standing Opus subagent** (log.md:137).
  - Packages 1 and 2 were sent by ad hoc subflows. The definition was "to be proposed for approval" (log.md:138), and it is still open in summary.md (Q8).
  - Observed: `.claude/agents/` has no oracle agent.
  - Reason: it awaited the living's approval.
- **Layer-word rename and README note** (log.md:180–184, 211). "Held until the emergency settles."
  - Five conflicts are left to the living (summary.md Q5).
- **Role templates in SKILL_VARIABLES.md** (summary.md Q2).
  - Observed: SKILL_VARIABLES.md on main has no "launch:" role lines, only the "Psyche medium Claude model/effort" lines.
  - Reason: awaiting the living's approval.
- **compensation-nix credential-only line** (summary.md Q3).
  - Observed (`git show origin/main:skills/compensation-nix.md`, line 27): it still reads "copies in at run time only the login files its components need". The proposed line is not landed.
  - Reason: awaiting approval.
- **Stable/next section in breaking-upgrades** (summary.md Q4).
  - Observed: not in breaking-upgrades.md on main.
  - A different skill, compensation-update ("Rotate stable and Next…", b7e1515, 2026-09-30), covers rotation in other words. That is an inference, not a recorded uptake.
- **Luna's deep dive for more space** (log.md:99).
  - Briefed (log.md:103: "Transported; working").
  - No result recorded in e167d8's log. No reason recorded.
- **Herdr pane / one name everywhere** (log.md:177).
  - Recorded as "Flow backlog"; b7ba00 was launched with equal names (log.md:191).
  - V2 removal deferred to the next Flow version, by the living's own words. Observed: commit 9ed50bda3 "Remove V2 from native launcher titles" on primary main.
- **Codex Flow Start BindingRefused.** Open throughout. Reason: Herdr 0.8.2 never fills agent_session (log.md:82, 169).
- **messenger-clj pane writes (S3) and caller gating (S4).**
  - Not started. "moving hm-send onto Deliver is the living's decision" (log.md:109).
- **Letter shape: id rendering, 'Owner', body variants** (log.md:229).
  - Deliberately left to the successor by the living's own words: "Anyway don't answer that here."
  - Observed: `Owner` is still in meta-signal-flow ethos/signal.ethos:126 on main.
- **Stale primary/flow submodule at 0.9.0** (log.md:49). No action recorded.

### 4 Handed over

Successor: Psyche Opus 93ba9f. It accepted "all its unfinished work" in seven items (93ba9f/log.md:20).

| Item | Taken? | Evidence |
|---|---|---|
| Flow 0.17.1 Soft-submit fix, scenario 4 | Taken, done | 93ba9f/log.md:28 (scenario 4 five of five); ac216c89 on flow main (observed) |
| Home bookmark eba6d270 (0.17) for b7ba00 to merge | Taken | b7ba00/log.md:57–58 (rebased as integration-b7ba00-home); 93ba9f/log.md:23 (merge duty to Field Sol b7da5d). Landing of that specific bookmark not checked; Home main has moved on (0025894f) |
| a676b3 safe #commit rebuild | Carried | 93ba9f/log.md:5, 20; b7ba00/log.md:31. Outcome not found in these logs (unknown) |
| Codex Start BindingRefused | Carried | 93ba9f/log.md:20 item (4). Outcome not found |
| persona-test suite move | Carried | 93ba9f/log.md:20 item (5). Observed: persona-test main pins Flow 0.17.4 |
| Q1 leftover seats 26c50c/98eb43/f5a74e | Carried, unresolved in these logs | 93ba9f/log.md:20 item (6) ("re-derive before asking"); b7ba00/log.md:34 still lists them live; no later close found |
| Q2 role templates | Carried; 93ba9f surveyed launch effort | 93ba9f/log.md:17, 25. Not landed (observed above) |
| Q3 compensation-nix line | Carried in the list only | No later mention found; not landed (observed) |
| Q4 stable/next skill section | Carried in the list only | No later mention found; see compensation-update (inference) |
| Q5 layer-word conflicts | Carried in the list only | No later ruling found in the grepped logs |
| Q6 letter shape | Taken | 93ba9f/log.md:27, 38; b7ba00/log.md:66, 71, 83 (books comparison, "Message Primitive" artifact, primitive-Message prototypes to Mind Astra 31147a) |
| Q7 Luna effort | Carried in the list only | No later mention found |
| Q8 oracle composer subagent | Carried in the list only | No agent definition exists (observed) |
| Inherited from 88475f: subagent prompts, messenger-clj line, claude-harness wording | Not carried by e167d8 | Absent from summary.md; grep of later logs finds no mention of subagent prompts or claude-harness. 93ba9f/log.md:10 notes the compensation-messenger-clj skill describes an undeployed version |
| 077114 vs Opus line | Resolved by closure | log.md:219 (077114 closed) |

The later logs grepped were 93ba9f, b7ba00, 183ae0, c64ee3, 7328f4, fe945a, 6997eb and f1c841. Beyond 93ba9f and b7ba00, none names any e167d8 item.

Unknowns:
- Whether a676b3's #commit rebuild landed.
- Whether 98eb43, 26c50c and f5a74e were closed.
- Zeus's current generation.
- Whether the living ever ruled Q2–Q5, Q7 or Q8 outside these logs. Transcripts were not searched.

### Sources for this flow

- flows/e167d8/log.md (all 376 lines; 238–376 duplicate 5–176)
- flows/e167d8/summary.md
- flows/88475f/handover.md
- flows/index.md:219–233
- flows/93ba9f/log.md:5–38
- flows/b7ba00/log.md:31, 34, 57–58, 66, 71, 83
- grep of flows/{93ba9f,b7ba00,183ae0,c64ee3,7328f4,fe945a,6997eb,f1c841}/log.md
- e167d8 reports/, notion/, vision/ (listing only). The vision files cited in the log all exist; contents were not re-read beyond the log's quotes.
- Commands run 2026-10-03 on ouranos:
  - `git fetch` + `git merge-base --is-ancestor` in /home/li/primary/repos/{flow,message,signal-flow,meta-signal-flow,signal-message,meta-signal-message,CriomOS-home,persona-test,Curriculum}
  - `git show origin/main:` for lib/stable-next-service.nix (CriomOS-home), skills/compensation-nix*.md, skills/breaking-upgrades.md and skills/compensation-update.md (Curriculum), ethos/signal.ethos (meta-signal-flow), SKILL_VARIABLES.md (primary)
  - `git ls-tree origin/main tools/` and `git log origin/main -- tools/native-seat-launch.mjs` (primary)
  - `systemctl --user list-units 'flow*' 'message*'`, `flow-next --version`, `df -h /nix`, `ssh zeus` (failed: host not resolvable)

## b7ba00 — PsycheV2.{ Fable b7ba00 } (Psyche Fable, successor of b860be; 2026-09-26)

Scope note: b860be is not listed in flows/index.md, so it is not audited here. b7ba00 took over from it through b860be's `reports/handoff.md`, which was written on the living's order relayed at about 02:00 on 2026-09-26 ("model usage at 99%"). That handoff carried the state of goldragon main ddf27e0c, field-clj a2c278d3, the CriomOS and CriomOS-home `integration-2-b860be` lines, eight rulings, and the Route A bootstrap order (flows/b860be/reports/handoff.md:1-12; b7ba00/log.md:14). The log has no closing entry. dc53b4/log.md:40 later lists b7ba00's route as one of the "Pre-crash routes … STALE".

### 1 Asked

The launch brief came from e167d8, not the living. b7ba00's log summarises it at log.md:10 as: take integration head back from 38de5b, route everything to e167d8, use jj only, and register seats through Flow. The living's own words reached this seat only as relays: 93ba9f relayed them by direct Herdr prompt, and e167d8 relayed one through a #psyche envelope. None of them was typed to this seat. They are recorded verbatim in b7ba00/vision/:
- Emergency (STT, relayed by e167d8, about 14:15 on 2026-09-26): "We have to take urgent action to stop bad model flows from being started or from continuing on when they should be…" (vision/modelFlows.md:7).
- The correction (STT, relayed by 93ba9f): "Yeah I never said freeze all launches. Everything that has a big context should be refreshed and everything that has been abandoned needs to be reaped … let's make sure the code makes sure it doesn't happen again." (vision/modelFlows.md:15). Also: "We should have a list of flows all programmed with their datom configuration." (vision/modelFlows.md:23).
- Role: "What do you mean merging something is Fable's job? Fable's job is to design and think not sweep the floor." (vision/fableRole.md:7).
- Design book: "So you can get Fable involved and you each do your own. You give him all the psyche material and then you all go each hunting for more psyche…" (vision/designBook.md:7).
- Word IDs: "the standard that we want to use to replace hashes with words, with a series of words … Let's come up with a name for this" (vision/wordIds.md:5-7).
- Meaning-language anatomy, typed as an artifact comment on 2026-09-26T20:54: "Let's make a book about the anatomy … This is a very early draft but this is the meaning language, which actually needs a name. I think we can send all of this to Fable." (vision/meaningLanguage.md:9-15).
- Sema, typed as an artifact comment: "Sema was supposed to be the language of meaning and so that is actually the right name … That means we rename all of the Sema aspect pertaining to the database." (vision/meaningLanguage.md:143). On the first version: "The first version of sema could be that it just has one or two layers of variants … payload at the end being a string." (meaningLanguage.md:157).
- Primitive Message (STT): "Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages … Let's figure out the name for the database part." (vision/messaging.md, "A primitive Message now" entry).
- Caller identity (STT): "It can get its origin without the user having to say, 'Hey I'm Psyche Fable.' It would just know." (vision/callerIdentity.md:7).
- Mind roles (STT): "Astra does the designing and the orchestrating and the big decisions and Sol does the implementation and the testing." (vision/mindRoles.md:7).
- Field tool (STT, designBook.md:13): "develop the field tool to extract transcript … version control, committing, getting transcripts from certain sessions".
- Unknown: the living's exact wording of the instruction that the book be an "independent analysis from the psyche alone". It reached this seat only as 93ba9f's paraphrase (log.md:71).

### 2 Done and landed

Integration work (morning, before the living took integration away from Fable):
- Observed (`git merge-base --is-ancestor 6d14ffb origin/main` in CriomOS: yes): CriomOS main was fast-forwarded from e6a83edc to 6d14ffb. That move completed 38de5b's tailnet merge-to-mains. The record behind it is b7ba00's ruling and a 28-derivation Prometheus check (log.md:43-45). The present main is 6485b64 (2026-09-30).
- Observed (`git merge-base --is-ancestor ddf27e0c origin/main` in goldragon: yes; 657f4ba8 is in Home main): goldragon main ddf27e0c and Home 657f4ba8 are on their mains. 38de5b made these landings, not b7ba00 (log.md:21).
- Observed (`git merge-base --is-ancestor b8b45e2f origin/main` in CriomOS-home: yes): Home branch `integration-b7ba00-home` b8b45e2f is now on Home main. It carries the Flow 0.17.0 and Message 0.17.0 next-pair pins rebased onto field-clj 3e5f450 (log.md:62). b7ba00 did not land it on main: it handed the branch to b7da5d (log.md:61, 63). Unknown: which seat fast-forwarded it.
- Observed (all four are ancestors of origin/main in Primary): b7ba00's records landed in Primary as bd987fca, f4f2ff8d, 07e8c30d and b39c41bd.
- Claim (log.md:30, 39-41; b7da5d's grade A witnesses): deployment 38 (ouranos TestActivation) was a bookkeeping orphan created when lojix 8.1.0 restarted the 7.0.0 Nexus. b7ba00 ruled that 38 had "met its purpose" and authorized a proposal regeneration plus an Evaluate-only probe. Not checked by this audit.
- Observed (`bd show`): three beads were opened and all are OPEN. primary-ql9 (P1) is the nix-ssh offload authentication from ouranos to Prometheus. primary-8sd (P1) is the Lojix self-deploy handoff that orphans the in-flight row. CriomOS-unm (P2) is criome-deps E0432.
- Claim (log.md:19, 22; e167d8/log.md:216): a jj op-log witness traced a working-copy loss to two causes. One is field-clj's refusal path running a whole-repo `jj op restore`. The other is an "import git head" by an unknown raw-git process. The finding became gap #6 of e167d8's field-clj landing spec. b7ba00 broadcast the "no field-clj #commit, land from own workspace" rule to nine live seats (log.md:26), graded Transported.

Design work (afternoon; every item is a private Claude Artifact plus a report in b7ba00/reports/; artifact URLs in receipts/relays.md):
- Observed (file exists): `reports/design-book-letters-roles-monikers.md` is the design book on letters, roles and word IDs (named "Monikers"), with a 4096-word list and measured token costs (log.md:68-69). Claim: the artifact was published (relays.md).
- Observed (file exists): `reports/books-comparison.md` compares this book with 93ba9f's, listing eight conflicts and ten tensions in the living's own records. It was published as "Two Books, One Ruling" (log.md:73-74).
- Observed (file exists): `reports/anatomy-of-the-meaning-language.md` is the anatomy book, under the name "Noema". It has a Noema.[One Many] root, five utterances and a Sanskrit table. Addendum v2 records that the head is the kind and priority goes to the database (log.md:79-83).
- Observed (file exists): `reports/sema-version-one.md` is "Sema, version one", a single scrolling page with four figures (log.md:84-85).
- Observed (file exists): `reports/message-primitive.md` is the "Message Primitive" prototype. It has nine kinds, Origin stamped through Flow ResolveCaller, a Bearing address, and Mnema as the database name (log.md:87).
- Observed (file exists): `reports/primitive-prototypes-comparison.md` compares this prototype with 93ba9f's. It was sent to 93ba9f and to Mind Astra 31147a (log.md:90).
- Claim (log.md:66-67): psyche hunts were sent to 93ba9f as #psyche envelopes. A word-ID token measurement found "two words 3.8 tokens vs six hex 3.5; three words 5.4 vs twelve hex 6.9".

### 3 Not done

- Observation: none of the design outputs reached code. The current mains of signal-message (b94d907), message (ce3eb6c) and meaning-language (e4319d1) contain no Noema, Bearing or Mnema (`git grep` on origin/main returned nothing). Repositories named sema, sema-engine and sema-storage still exist, so the living's ordered rename of the database (meaningLanguage.md:143) is not observed. The reasons in the records are these. 31147a, the Mind Astra that received the primitive-Message package, was not live, and "nothing reached a live Mind Astra … no owner for primitive-Message package since 31147a" (dc53b4/log.md:51, 72). The seat itself went stale in a crash (dc53b4/log.md:40).
- The eight conflicts for the living (books-comparison) and the six design questions, including Toward vs Bearing and Sent/SendRejected vs Delivered/Parked/Refused: no ruling found in the b7ba00 records. Per dc53b4/log.md:47 and 52, 93ba9f asked the living and 8904b1 kept the questions with dc53b4. Reason: no reason recorded.
- Field tool for transcripts, version control and committing (designBook.md:13): no b7ba00 action recorded. No reason recorded.
- The launch guard (no duplicate roles, no undeclared effort) was held by order of 93ba9f: "Psyche is drafting that design with the living — hold any launch-guard implementation" (log.md:60). b7ba00 flagged it as an item for e167d8 as Flow owner (log.md:59).
- The Home branch was not landed by b7ba00, and neither was the CriomOS repin to the new Home main or the second-deploy gate. Reason: the living's ruling at fableRole.md:7 ("Fable's job is to design and think not sweep the floor"), followed by 93ba9f's instruction to hand them to b7da5d (log.md:61). The Home branch is "pin-verified, not check-verified": the stub system input meant no override was supplied (log.md:62).
- Evaluate-only probe of the regenerated ouranos proposal: authorized (log.md:46). No result is recorded in b7ba00's log. Unknown whether it ran.
- The hypothesis that beads auto-export is the raw-git process behind the git-HEAD import: "to be checked when the emergency lifts" (log.md:34). It was never checked. No reason recorded.
- The independence of the design book is compromised: b7ba00 had already read 93ba9f's drafts before the living's correction arrived, and it disclosed this (log.md:71).
- Self-reported error (log.md:23): three messages were sent with `--stdin`, which messenger 0.2.5 lacks. They were resent.

### 4 Handed over, and whether a successor took it

- CriomOS-home `flow-message-next-e167d8` and `integration-b7ba00-home`, with the CriomOS repin and the second-deploy gate, went to Field b7da5d (log.md:61, 63). Observation: b8b45e2f is on Home main, so the branch was landed by someone. The later Psyche logs (e167d8, 183ae0, c64ee3, 7328f4, fe945a, 6997eb, f1c841) have no hit for `integration-b7ba00-home|b8b45e2f`. Taken: yes in substance; who landed it is unknown.
- primary-ql9 (nix-ssh offload) went to b7da5d (log.md:16, 47). Not taken to closure: the bead is OPEN, and no later Psyche log has a hit for `primary-ql9`.
- primary-8sd (Lojix orphaned row) went to b7da5d. Not taken: the bead is OPEN. dc53b4/log.md:72 records it as "owned by stale b7da5d".
- CriomOS-unm (criome-deps) had no owner named. It is OPEN. No later Psyche log mentions it.
- The primitive Message plus comparison went to 93ba9f and Mind Astra 31147a (log.md:90). Not taken by its addressee: dc53b4/log.md:51 says "nothing reached a live Mind Astra". The design state was recovered into dc53b4/reports/recovered-design-state.md. No hits for Bearing, Mnema or primitive Message in the later Psyche logs listed above. Observation: no Bearing, Mnema or Noema in the message or signal-message mains.
- The design books, the comparison and the Noema/Sema books were left with 93ba9f and the living. Partly taken: 93ba9f wrote flows/93ba9f/reports/books-compared.md, and dc53b4 recovered the state. No hit for Sema, Noema or design book in the e167d8, 183ae0, c64ee3, 7328f4, fe945a and 6997eb logs beyond unrelated "sema" store mentions (6997eb/log.md:98).
- The launch guard went to e167d8, then to Psyche (log.md:59-60). The later Psyche logs have no hit for `launch.guard|SeatOccupied|EffortUndeclared|same role|duplicate role`. Not taken, per these greps.
- The messenger route repair (93ba9f's sends to b7ba00 were Held RepairRequired four times; log.md:61, 71, 72) was addressed to "whoever owns messenger routes". Not taken: fe945a/log.md:58 records on 2026-10-02 that Held messages are never retried.
- The field-clj #commit rebuild (a676b3) was e167d8's matter, not handed over by b7ba00. dc53b4/log.md:72 says "(c) not fixed (field-clj still restores op log; a676b3 pre-crash)".

### Sources for this flow
- /home/li/primary/flows/b7ba00/log.md (lines 1-106; lines 92-106 are a re-merged duplicate of the opening block)
- /home/li/primary/flows/b7ba00/vision/{callerIdentity,designBook,fableRole,flowAnatomy,meaningLanguage,messaging,mindRoles,modelFlows,reachingTheLiving,types,wordIds}.md
- /home/li/primary/flows/b7ba00/receipts/relays.md (artifact URLs, send grades); reports/ listing
- /home/li/primary/flows/b860be/reports/handoff.md:1-12
- /home/li/primary/flows/dc53b4/log.md:40,47,51,52,72; dc53b4/summary.md:35
- /home/li/primary/flows/e167d8/log.md (grep hits 191-225); fe945a/log.md:58; 6997eb/log.md:98
- Commands: git merge-base checks in /git/github.com/LiGoldragon/{CriomOS,CriomOS-home,goldragon} and /home/li/primary; `bd show primary-ql9 primary-8sd CriomOS-unm`; `git grep Noema|Bearing|Mnema` on meaning-language, signal-message and message origin/main; greps of the later Psyche logs, as listed above.

## 183ae0 — Psyche Opus, second Psyche seat beside Psyche Fable 8904b1 (later c02c0d, then c64ee3)

Active 2026-09-28 to 2026-09-29. Successor: Psyche Opus 7328f4 (index.md:233). All quotes below are the living's typed words as logged by 183ae0; L = `flows/183ae0/log.md` line.

### 1 Asked

- Fable contact: "I don't know if talking to Fable is a good idea. That would cost tokens so wait till you have something to tell them and let's talk first." (L9)
- Context: "Get your subagent to populate your context with the middle stratum so that you have the right context to follow along with Fable." (L17)
- Probes and Fable's loaded context: "Why are you getting these probes? I thought we had decided not to use them. Could you help Fable to load its context and find relevant recent psyche for him to work on? First get a subagent to find out what its state is and what it was loaded with ..." (L31); "We'll find out where the probe came from then too, and what the deal is with it, and why we need it, and what we could do to get rid of it, and what would be the pros and cons." (L37)
- Codex page (relayed by Field Astra bea031; the living's own words found at bea031 rollout line 750, per L49): "When I say all the [Codex flows], I mean all the live [Codex flows] so there are only four of them." (L45, STT)
- The For You button: "Can you see the button I pushed on the For You page?" (L43); "The button I pushed was for taking out the intercom." (L53)
- Anatomy page from Fable: "... let's contact Fable about creating a page on the anatomy of the architecture and the anatomy of the different components that we were talking about today ..." (L69)
- Book: "There is some content in Fables transcript that needs to be made into a book. Very recent" (L105)
- Skill edit: "You can remove the part that tells everybody to contact Psyche for now and deploy that while I review the book." (L111)
- "Maybe this belongs on another line somewhere also." (L127)
- Fresh Fable: "Let's get Fable involved or could we just start a fresh Fable Flow? I think it would be better. Don't wake it up." (L143)
- Research and browser work: "I'd like you to do a little side research on anybody who's looked into the stratification of context in the LLMs ... Is there any code out there that started to programmatically change the system prompt of some harnesses? What about open source stacks? ... ask Astra Field, or maybe Sol Field, to restart Astra Field and focus on learning about and then injecting into its user prompt the psyche that relates to controlling the web browser ... log me into my OpenAI account through the web authentication ... Develop some skills for that." (L155–159)
- Registration: "I want you to send the registration problem to Mind Astra. We need to take out the requirement for the flow to not be busy to be able to register and we don't want it to require any kind of probe or testing message." (L163)
- Old seat: "You forgot: your sub-agent didn't close the old Fable ... we can register a new one and close the old one." (L175)
- Successor prompt: "Can you refer to your own transcript and tell him what you want passed in as a user prompt again? ... My new flows are not getting a nice fat user prompt for context." (L183)
- Vision and notion records (not orders, but asks embedded): skills out of the Curriculum, three skill repos plus log repos, typed skills via a nexus, "Let's do the anatomy of that" (vision/skills.md:13–43); single-writer nexus for main, a question (notion/commits.md:5); datom payload from multiple places (notion/datom.md); psyche injected with a message, "That's long term" (notion/psyche.md:5).

### 2 Done and landed

- Observed (`git log origin/main` in Curriculum, `git branch -r --contains 3593fa16` → origin/main): Curriculum 3593fa1, 2026-09-28, "Stop forwarding the living's words to Psyche in main-flow logging line". Observed (`git branch -r --contains b2caab82` in Primary → origin/main): Primary b2caab828 deploys it. Observed: the phrase "forwards the whole message to Psyche" is absent from `.claude/skills/main-flow/` and Curriculum `skills/` (grep, no hits). Claim (L119): the regeneration also carried AspectV2 → Aspect; check-skills matched.
- Observed (`git log origin/main -- flows/183ae0/reports/context-strata-research.md` → b5787ff77): the context-strata research report, 828 lines, on Primary main. Its Part 5 names open items (see 4).
- Observed (`git -C messenger-clj log origin/main | grep probe` → 4bce278, 2026-09-29 10:30, "Remove messenger readiness probes and gates"): the registration fix the living asked to send to Mind Astra landed in messenger-clj main. Executor per records: Mind Astra 6f51ad (source) and Field Sol caf622 (install) (caf622/log.md:307). Claim (L197, Field Sol): installed as messenger 0.2.8; Observed by 7328f4 (7328f4/log.md:9): it registered while working with no probe.
- Claim (L77): page "Codex live flows" https://claude.ai/artifact/TR6EhLfLtPK1xLJCxSvx9P over Mind Astra 6f51ad, Field Astra bea031, Mind Sol b666e7, Field Sol caf622. Not checked (artifact host).
- Claim (L97, L101): "Who Contacts Whom" aspect-contact book https://claude.ai/artifact/PW1i1qraz9ZjWcpxy7jzGV, version 2 after Fable's review; drafts in flows/183ae0/drafts/ (Observed: three files present, psyche-/mind-/field-aspect.md).
- Claim (L123): book from Fable c02c0d transcript lines 849–1094 (Mentci bridge), https://claude.ai/artifact/5PJiTz7AzuK1njSsDfNR2B. The living judged it "a bunch of gap-filling with a poor understanding of my approach" (L133).
- Claim (L73): the anatomy request forwarded to Fable c02c0d; Claim (L171): fresh Fable c64ee3 put the anatomy of skill deployment, nine questions, on the living's page Afo898DtrDNPf82Q5aLi3H.
- Claim (L151): fresh Psyche Fable c64ee3 launched (pane w1:pP, claude-fable-5-1); c02c0d not woken. Observed in index.md:232 (c64ee3 listed).
- Claim (L179): old Fable c02c0d deregistered, process ended, transcript kept; the subflow sent one test message to c02c0d against its brief.
- Claim (L189): shared working copy conflict resolved with nothing discarded; main moved forward 4ae14d59 → 314e4700; conflict markers in flows/caf622/log.md removed; cause named (`jj duplicate -d main@origin` side chains).
- Observed (file present): successor prompt flows/183ae0/launch/successor-prompt.md, with the living's words verbatim. Claim (7328f4/log.md:5–7): 7328f4 launched from it and remembered 183ae0 at depth one.
- Claim (caf622/log.md:247–249, L193): Field Astra restart for browser work relayed to Field Sol caf622; Field Astra d5b96b launched with its brief whole in the first prompt.
- Observed (git log of each repo): repositories psyche-skills 9cd7d98, mind-skills 6f2b400, field-skills f8ecb48, psyche-logs abc71db, each 2026-09-29, "Add README stating purpose and charge". Unknown: which flow created them (not in 183ae0's log; likely c64ee3, unverified).

### 3 Not done

- Probe: where it came from, why, pros and cons (L37). Observation: no log entry answers it; the probe was removed instead (4bce278). No reason recorded.
- "find relevant recent psyche for him [Fable]" (L31). Observation: L23 lists the 24 skills Fable loaded; no entry records gathering psyche for Fable. No reason recorded.
- For You button (intercom): stopped on the living's word "it doesn't work. You don't have to check again." (L61); vision/presentation.md:5 records his ruling for comments-only pages.
- Browser control / OpenAI web login skills (L155–159). Observation: no browser or OpenAI-login skill in Curriculum `skills/` (ls, no match); d5b96b's log records session recovery, migration and Prometheus work, no browser-login work (grep "openai|login" in d5b96b/log.md finds only the phone access route at :421). No reason recorded.
- Aspect contact skills (drafts): not deployed. Observation: no aspect skill in Curriculum `skills/`. Reason recorded: four points left open, Fable reviews before the living (L93–101); the living later approved only Proposal 2, the skill-designing line; Proposals 1 and 3 not approved (L139).
- Skill-designing "named spot in a named file" line: approved, held "until skills have their new home" (successor-prompt.md, State at hand-over).
- Phone-first page skill: "not approved" (7328f4/log.md:7); the living's proposal rule (vision/proposals.md) answered the ask for its target.
- Correction: the "rebuild the Rust executable" premise was 183ae0's own, repeated by the living; witnessed false by c64ee3 (vision/skills.md:47; L171).
- Single-writer nexus for main: a question, left open without owner (7328f4/log.md:7).

### 4 Handed over (successor-prompt.md "State at hand-over"; 7328f4/log.md:7)

- Skill deployment anatomy at c64ee3 (nine questions). Taken: c64ee3/log.md:5, :21. Later: fe945a/6997eb carry vision-is-skill "settled, deploy mechanism open" (6997eb/log.md:114).
- Aspect contact drafts / who-contacts-whom. Not taken as drafts (grep "Who Contacts|drafts/" in successor logs: no hits). The topic resurfaces as Codex aspect briefs in fe945a/log.md:62–66 and 6997eb/log.md:125 (different artifact).
- Held skill lines (skill-designing named spot; phone-first page skill; psyche-interraction target line). Carried as open by 7328f4/log.md:7; no later log takes them (grep "skill-designing|phone" beyond 7328f4:7: none). 6997eb/log.md:66 presents four skill proposals including psyche-interraction; whether it is the same line is Unknown.
- Register c64ee3 after the messenger fix. Taken and done: L197; witnessed by 7328f4/log.md:7.
- Field Astra restart for browser control / OpenAI web login. Restart taken (d5b96b, 7328f4/log.md:7); browser-login work not taken (no hit in any successor log for "browser|OpenAI|web login").
- End bea031 after crossover. Claim taken: 7328f4/log.md:7 "old bea031 to be ended after crossover"; completion not found in the grepped logs (Unknown).
- Single writer for main. Carried "without owner" by 7328f4/log.md:7; not taken later (no hit for "single writer").
- Context-strata report's open items (Codex responses-lite witness; three reconciliations owed to claude-harness, including OTEL raw-body readability). Not taken (no hit for "claude-harness|OTEL|strata" in successor logs).
- Fat first prompt. Taken as settled: fe945a/log.md:6 ("one fat startup prompt"), 6997eb/log.md:114.

### Sources for this flow

- /home/li/primary/flows/183ae0/log.md (all 201 lines)
- /home/li/primary/flows/183ae0/vision/{messaging,presentation,proposals,seats,skills}.md
- /home/li/primary/flows/183ae0/notion/{commits,datom,psyche}.md
- /home/li/primary/flows/183ae0/reports/context-strata-research.md (head, outline, Part 5, sources)
- /home/li/primary/flows/183ae0/launch/successor-prompt.md; drafts/*.md (heads)
- /home/li/primary/flows/index.md:229–233
- grep over /home/li/primary/flows/{c64ee3,7328f4,fe945a,6997eb,f1c841}/log.md; /home/li/primary/flows/{d5b96b,caf622}/log.md
- Commands: git in /home/li/primary (b2caab82, b5787ff77), /git/github.com/LiGoldragon/Curriculum (3593fa16; skills/ listing; grep), /git/github.com/LiGoldragon/messenger-clj (4bce278), /git/github.com/LiGoldragon/{psyche,mind,field}-skills and psyche-logs (git log -1)

## Across the four flows

### Asked by the living and never done by any flow in the records

Each item was searched in the later psyche logs named above. None has a later log entry that records it done.

1. **A flow started through Flow and used by the seats.**
   - Asked: "re-inject it into a new proper flow that started by Flow" and "used by you guys" (d8df70).
   - Observed in the records: fe945a/log.md:59 (2026-10-02) still reads "no live seat started through Flow".
   - Reasons given: Flow knew no flows, and it could start only headless Codex (d8df70). Codex Start BindingRefused, because Herdr 0.8.2 never fills agent_session (e167d8).
2. **Code that stops bad model flows from starting or continuing.**
   - Asked: the launch guard against duplicate roles and too-high effort (b7ba00, vision/modelFlows.md:7, :15), and "a list of flows all programmed with their datom configuration".
   - Reason given: held by 93ba9f's order. No later log mentions it.
3. **The field tool for transcripts, version control and committing** (b7ba00, vision/designBook.md:13). No reason recorded.
4. **Renaming the database away from "Sema"** (b7ba00, vision/meaningLanguage.md:143).
   - Observed: the database still carries the name sema.
   - Reason given: the primitive-Message package went to a Mind Astra (31147a) that was not live (dc53b4).
5. **Zeus deployed** (e167d8, log.md:63, :130).
   - Reasons given: integration step 2 was unfinished, and Lojix 7 rejected the proposal.
   - Unknown: Zeus's state today.
6. **Cluster spec in Ethos, with its own signal repository** (e167d8, log.md:115-116). It got a survey only.
   - Observed: no such repository exists.
   - No reason recorded.
7. **Browser-control and OpenAI web-login skills for Field Astra** (183ae0, L155-159). No reason recorded.
8. **The account of where the readiness probe came from, with pros and cons** (183ae0, L37).
   - The probe was removed instead (messenger-clj 4bce278).
   - No reason recorded.
9. **"have you answered my other questions that I can't seem to get answers for?"** (d8df70, log.md:352-356).
   - Questions were collected, but no answer to the living is recorded.
   - No reason recorded.
10. **Removing the Prometheus crash trigger.**
    - Observed: the panic-reboot mitigation is live (`kernel.panic`=10 on 2026-10-03). The mt7925 trigger itself remains.
    - Recorded as awaiting the living's choice (d8df70, recurring-problems.md §1).

### Proposals that wait on the living's approval and were never ruled in the records

- From e167d8 (Q2–Q5, Q7, Q8):
  - role templates in SKILL_VARIABLES.md
  - the compensation-nix credentials line
  - the stable/next section
  - the layer-word conflicts
  - Luna's effort
  - the oracle-composer subagent
- From 183ae0:
  - the aspect contact skills
  - the skill-designing named-spot line, which was approved but is held "until skills have their new home"
  - the phone-first page skill
  - the psyche-interraction target line
  - the single-writer-for-main question, which was left "without owner"

### Dropped in hand-over: items in no later log

- **From d8df70:**
  - the title-tool findings
  - the injection hazard (injected launcher turns read as the living's authority)
  - the failed message-daemon on ouranos
  - "Mind and Field log nothing"
- **From e167d8:** three items inherited from 88475f
  - subagent prompts
  - the compensation-messenger-clj fallback line
  - the claude-harness wording
- **From b7ba00:** three open beads
  - primary-ql9, nix-ssh offload
  - primary-8sd, the Lojix self-deploy orphan
  - CriomOS-unm, criome-deps
- **From 183ae0:** the open items in the context-strata report.

## Sources

- /home/li/primary/flows/index.md (:219-233)
- /home/li/primary/flows/f1c841/log.md:52-53
- The per-flow "Sources for this flow" lists above, which hold every file read and every command run by the four forked subflows.
- /home/li/primary/flows/{d8df70,e167d8,b7ba00,183ae0}/ (log.md, summary.md, reports/, vision/, notion/, witnesses/, receipts/, launch/, drafts/)
- /home/li/primary/flows/88475f/handover.md and /home/li/primary/flows/b860be/reports/handoff.md, read only for what was inherited
- Later logs grepped: /home/li/primary/flows/{93ba9f,e51411,c64ee3,7328f4,fe945a,6997eb,f1c841,dc53b4}/log.md
