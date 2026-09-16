# Predefined subflow templates and main-flow token savings

Order: `flows/efa157/vision/tokenEfficiency.md`. Sources: this flow's transcript (efa15708, 2324 records, 2026-09-16 08:06–15:02Z), the predecessor's (840e42bb, 2026-09-15 21:34 – 2026-09-16 08:24Z), `.claude/agents/*.md`, Curriculum `roles.datom`, `origin/flow/cf7879:flows/cf7879/log.md`. Numbers are marked **[W] witnessed** (counted from those files) or **[E] estimate**.

## a. The measured pattern

**[W] Volume.** efa157: 35 Agent calls, 67,758 prompt bytes, 319,728 assistant output tokens. 840e42: 71 Agent calls, 142,146 prompt bytes, 670,295 output tokens. Combined: 106 dispatches, 209,904 prompt bytes (~52,500 tokens at 4 B/token) = **5.3% of output tokens, in each session independently**, over 17.8 wall hours — **[E] ~143 dispatches and ~70,000 prompt tokens per day**.

**[W] Kinds by depth (efa157 / 840e42).** read-ordinary 25/13, read-trivial 4/4, read-demanding 4/8, write-trivial 1/43, write-ordinary 1/2, write-demanding 0/1. Model overrides: `haiku` on 13 checkups (efa157), `fable` on 4 audits and `opus` on 2 (840e42); the rest take the definition's model.

**[W] Kinds by task shape** (grouped by the flow's own descriptions; covers essentially all 106):

| shape | n | avg bytes |
|---|---|---|
| Codex queue send / relay | 44 | 2,192 |
| night/day checkup | 22 | 1,793 |
| cross-lane witness of one claim | 19 | ~1,800 |
| Fable audit of a proof branch | 11 | ~2,600 |
| report delta / verbatim file read | 8 | ~700 |
| transcript record verification | 3 | ~1,050 |

**[W] What every prompt repeats.**
- Identity prefix, byte-identical 175 B in all 35 efa157 prompts: `$subflow. FLOW_ID efa157. FLOW_DIRECTORY /home/…/flows/efa157.` (840e42 used a 150 B prose form). 6,125 B in efa157 alone.
- Sandbox paragraph: 33/35 say "Read-only"; 21 "send nothing"; 14 "edit nothing"; **20/35 carry the git rule** ("do not run git with -C or GIT_DIR against other repositories; cd in a subshell instead") at ~180 B each.
- Bounds: 27/35 name a `timeout`.
- Evidence rule: 27/35 carry "witnessed (with the command) or failed/claimed (with the error)".
- Output shape: 32/35 end with a "Return …" sentence ("compact report, facts only", "the verdict section in your reply", "under N lines").
- **[W] The whole first paragraph — identity, sandbox, bounds — is 12,917 B of 67,758 B: 19% of efa157's Agent-prompt spend, re-typed verbatim every dispatch.**
- **[W] The checkups repeat their seven numbered items too**: 13 efa157 checkups = ~25,100 B, differing only in a tip hash, a rollout filename and which units to poll.
- **[W] Codex sends repeat a wrapper around a fenced verbatim block**: 40 of 43 predecessor write-trivial prompts fence the payload; the wrapper outside the fence averages **931 B**, totalling **37,253 B** — pure protocol (which socket or CLI, which thread id, "report the turn id", "take no other action; edit, commit and push nothing").

**[W] What the agent definitions carry today.** `.claude/agents/*.md` are 193–316 B: front matter (name, description, model, effort) plus one or two sentences taken from `roles.datom` (`general-instructions`, and for read roles the `read` permission line). They encode **depth and model only**. Every task-shape rule above therefore lives in the prompt and is paid for on every dispatch.

## b. Proposed templates

Each is a new `.claude/agents/<name>.md` generated from Curriculum (authored role bodies; regenerate, never hand-edit the read-only trees). Front matter keeps the `model`/`effort` of the depth it wraps. The fixed body absorbs the `$subflow` identity contract, the read-only/send-nothing sandbox, the git -C rule, default timeouts, the witnessed-or-failed rule, and the return shape. The main flow then types one line.

| template | depth / model | one-line invocation |
|---|---|---|
| `checkup` | read-ordinary / haiku | `Checkup. Last cf7879 tip 776e20ea. Rollout 01a0a715. Extra: quota lines from events.ndjson.` |
| `lane-delta` | read-trivial / haiku | `Lane delta. Branch flow/cf7879, file reports/to-840e42.md, since 776e20ea.` |
| `proof-audit` | read-demanding / fable | `Proof audit. Item 48 on CriomOS proposal/prometheus-service-provider-poc. Claims: <3 lines>. Prior: reports/prometheusServicesAudit.md. Report item48Audit.md.` |
| `verbatim-read` | read-trivial / haiku | `Verbatim. origin/flow/cf7879:flows/cf7879/reports/to-efa157.md and to-secondary.md.` |
| `record-check` | read-ordinary / haiku | `Record check. Rollout 01a0a715: did turns 29ac8517 and 74b28dd4 land, and what answered?` |
| `codex-send` | write-trivial / haiku | `Codex send, thread 01a0a715: ---<note>---` |
| `witness` | read-ordinary / sonnet | `Witness: <one claim>. Sources: <repo/branch/commit>. Seek disconfirming evidence.` |

### Exact body for `checkup` (most repeated read shape, 22 dispatches)

```
---
name: checkup
description: 'A periodic read-only state sweep of the cluster. Report deltas.'
model: 'claude-haiku-4-5'
effort: medium
---
You are a checkup subflow. You carry the main flow's identity: its FLOW_ID and
FLOW_DIRECTORY are in your cwd's flows/ directory; find them, do not ask.
Do not edit files, commit, push, restart a unit, or send any message. Fetch is
allowed. In your own cwd plain git is allowed; never run git with -C or GIT_DIR
against another repository — cd into it in a subshell instead. Bound every
command: 60 s for a fetch, 20 s for ssh or `claude agents`, 120 s otherwise.
Run this sweep unless the brief replaces an item:
1. `git fetch origin <peer branch>` and `git log -3 --format='%h %ci %s'`; if the
   tip is newer than the one the brief names, print the added lines of the peer
   report whole and `git diff --stat` for its flow directory.
2. Hosts: `ssh -o BatchMode=yes -o ConnectTimeout=5 <host> uptime` for each host
   the brief names, else prometheus.goldragon.criome and zeus.goldragon.criome.
3. Units: `systemctl --user is-active` for the user units, plus the last Result,
   ExecMainStatus and next elapse of the checkup timer; `systemctl is-active lojix`.
4. Sessions: `timeout 20 claude agents --json` to a file, parsed; for each session
   prefix in the brief report name, status, state, waitingFor.
5. The peer harness's newest rollout file and the timestamp of its last record.
6. Quota: the newest `remaining` and `percent` lines, printed whole.
7. `df -h /home | tail -1`.
Mark every line witnessed (with the command that produced it) or failed (with the
error, verbatim). Report only what changed since the state the brief names, plus
anything failed; say "no change" for the rest. Facts only, no advice, under 25
lines. Then append your own dated line to the main flow's log.md under
"## Checkups" and say that you did.
```
**[W]** basis: 1,793 B average prompt today. **[E]** saving ~1,650 B per dispatch.

### Exact body for `codex-send` (most repeated write shape, 44 dispatches)

```
---
name: codex-send
description: 'Deliver one exact note to the paired Codex flow. One send, nothing else.'
model: 'claude-haiku-4-5'
effort: medium
---
You are a send subflow carrying the main flow's identity. Your whole task is to
put the brief's note into the paired Codex thread unchanged and report what the
route answered. The note is the text between the `---` fences in your brief.
Never rewrite, paraphrase, summarise, re-wrap or re-space it; if it does not
begin with `[PEER primary-claude <FLOW_ID>]`, prepend exactly that and no more.
Route, in order, stopping at the first that returns an id:
1. `timeout 60 codex queue --thread <thread> --message "<note>"`.
2. The app-server: initialize a client as `fable-<FLOW_ID>` against
   /home/li/.codex/app-server-control/app-server-control.sock and call turn/start
   with the note. Use the existing helper; write no new socket script.
3. prompt-relay to the peer, if the brief names it as a fallback.
Report: the route used, the turn or queue id, whether it opened a new turn, and
any error verbatim. A sender acceptance is not a recipient receipt — say which
you have. Take no other action: edit nothing, commit nothing, push nothing, read
no more than the send requires. Never run git with -C or GIT_DIR.
```
**[W]** absorbs the 931 B average wrapper; the main flow then types only the fenced note.

## c. Codex's delegated jobs

**[W]** From `origin/flow/cf7879:flows/cf7879/log.md`, Codex names long-lived, topic-owning workers rather than per-call prompts: `skill_receipt`, `relay_witness`, `jj_merge_agreement`, `jj_usage_audit`, `relay_parser_repair`, `relay_loop_fix`, `notify_consumer`, `core_checkup`. The log records ownership ("the parser worker owns the Message store migration…", "relay_loop_fix owns Message provenance loop-guard follow-ups, then transitive pin convergence"), so its per-job preamble re-establishes scope a worker already holds. **[W]** `roles.datom` gives Codex only three generic agents — `default` (write/ordinary), `explorer` (read/ordinary), `worker` (write/demanding) — plus the `codex-skill-loading` line.

Proposal, same shape: add named `CodexAgent` roles to `roles.datom` with fixed bodies — `witness` (read/ordinary: gather evidence for one claim, mark witnessed or claimed, touch nothing), `audit` (read/demanding: seek disconfirming evidence, verdict first, under N lines), `proof` (write/demanding: land a behavior test, publish the tested-source and publication commits, no change-detectors), `relay` (write/trivial: one exact delivery, report the id). Each carries once the workspace-isolation rule the log shows being restated per job (isolated Jujutsu workspace; never check out over another flow's working tree). The orchestrator then briefs by name and re-briefs by name, not by re-prompt.

## d. Other main-flow savings (per 24 h, extrapolated from witnessed rates)

1. **Log entries written by a subflow from a one-line brief.** **[W]** 64 Bash calls wrote or appended `flows/efa157/log.md`, totalling **72,448 command bytes in 6.9 h** — more than the entire Agent-prompt spend of that session. **[E]** ~250,000 B/day ≈ 62,700 tokens/day; a one-line brief to a `log-entry` write-trivial subflow that reads the report or transcript itself costs ~250 B: **saves ~37,000–48,000 tokens/day**.
2. **A persistent read-only checkup that reports only deltas.** **[W]** consecutive efa157 checkup prompts differ by a tip hash and a filename yet cost 1,799–2,347 B each. Keeping one `checkup` agent alive and re-briefing it ("again; last tip 776e20ea") costs ~60 B. **[E] ~12,000 tokens/day**, and it shortens the replies too.
3. **The checkup writes its own log line** (last clause of its body above). **[E]** removes one 400–1,100 B main-flow append per checkup at ~30/day: **~7,500 tokens/day**.
4. **A daily orders file replacing long queued messages.** **[W]** `reports/ordersToCodex-2026-09-16.md` (2,852 B) already exists, yet sends still restated item text: predecessor payloads averaged ~1,280 B inside the fences across 43 sends. **[E]** citing "orders file, item 51" instead: **~15,000 tokens/day**.
5. **ScheduleWakeup prompts.** **[W]** efa157: 14 wakeups, 21,775 B, avg 1,555 B, each restating the checkup instruction a template would own. **[E]** reduce to ~200 B: **~4,800 tokens/day**.
6. **Do not re-quote what a subflow returned.** **[W]** several efa157 log appends restate a reply already in context; cite `reports/<file>.md` and line numbers instead. **[E] ~5,000 tokens/day.**
7. **Fan out independent witnesses in one message.** **[W]** they were dispatched one per turn; batching removes the per-round re-orientation text. **[E] ~3,000 tokens/day.**

## e. Candidate lines for a token-efficiency skill in the primary system prompt

1. Every repeated instruction belongs in an agent definition, not in a prompt; if you have typed a sentence to two subflows, it is a template's body.
2. Brief a template by its difference from the default — the tip, the claim, the file — never by its procedure.
3. Re-brief a living subflow by message before dispatching a new one.
4. A subflow that gathers a fact writes the log line for it; the main flow does not re-type what it has already read.
5. Never restate in a peer message what the day's orders file already holds; cite it.
6. Ask for the delta, not the state: name the last witnessed value so the reply can be "no change".
7. Depth and model are chosen by the work, not by caution: trivial reads to haiku, audits to the demanding role.
8. Bound every delegated command and name the return shape once, in the template, not per dispatch.
