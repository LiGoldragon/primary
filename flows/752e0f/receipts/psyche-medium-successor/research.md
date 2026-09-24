# Research: Psyche Medium successor to d8df70 — STOPPED, duplicate found

Passive research subflow of Psyche High 752e0f. Draft first prompt was NOT written: the
coordinator (752e0f) interrupted mid-task after step 4 with a stop instruction, because
a successor already exists and is HM-registered and working. This file records only what
was read before the stop.

## 1. Duplicate check (passive)

`hm-list` output (flow / agent / session / state), relevant rows:

```
d8df70	psyche-opus-5	messaging-build	done
752e0f	psyche-fable-of-836818	messaging-build	working
e51411	psyche-opus-of-d8df70-r2	messaging-build	working
9ddcbc	field-medium-9ddcbc	messaging-build	working
```

`herdr --session messaging-build agent list` output, relevant entries:

- `wD:pD`, name `psyche-opus-5`, terminal title `Psyche Medium d8df70`, agent_status `done`.
- `wD:pF`, name `psyche-opus-of-d8df70-r2`, terminal title `Psyche Opus 5.5 e51411`,
  agent_status `working`, agent_session (herdr:claude id)
  `e5141130-9a4a-4b8f-b405-67d941a7b320`.
- `wD:pE`, name `psyche-fable-of-836818`, terminal title `Psyche Fable 752e0f` (this
  subflow's own pane), agent_status `working`, agent_session
  `752e0f7e-49ec-4110-b27b-6107e0eb6520`.

**Finding: a Psyche Medium successor already exists.** Pane `wD:pF` is titled
`Psyche Opus 5.5 e51411`, flow id `e51411`, and is `working`. Its native session id
(`e5141130-9a4a-4b8f-b405-67d941a7b320`) is byte-identical to the content of
`flows/9ddcbc/psyche-medium-successor-20260924/receipts/native-id.txt`, proving Field
Medium 9ddcbc already launched and HM-registered this exact successor before this
subflow started. The task's premise (that only a Field Medium *preparation* exists, and
Psyche High must draft the first prompt) is stale. No further launch preparation is
warranted; e51411 should be reviewed as an existing seat, not drafted for.

## 2. flows/d8df70/refresh-inject.md (1653 bytes)

Seat spec: Psyche Medium, Claude, model `claude-opus-5-5`, effort medium, title
`Psyche Medium <new FLOW_ID>` (note: the successor that was actually launched used
title `Psyche Opus 5.5 <id>` instead — the aspect+model form, per testing-flow-titles).
Predecessor d8df70 remembered at depth one via its own transcript's latest
"# Flow handover — Psyche Medium d8df70" text.

17 skills listed: spirit, psyche, main-flow, psyche-interraction, flow-aspect, behavior,
messaging, testing-message-route, testing-datom-messaging, testing-session-registry,
testing-flashbook, testing-flashbook-illustration, flow-evidence, file-editing,
testing-commit-scope, operational-layer-communication, herdr.

11 inline files: flows/d8df70/log.md; flows/d8df70/vision/messaging.md;
flows/d8df70/vision/flashbooks.md; flows/d8df70/vision/flowLifecycle.md;
flows/d8df70/vision/flowTool.md; flows/d8df70/vision/building.md;
flows/d8df70/vision/deployment.md; flows/d8df70/reports/living-words-since-launch.md;
flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md;
flows/d8df70/flashbooks/dawn/source.md (once the render lands);
flows/05c604/vision/launch.md.

4 pointer-only files: flows/d8df70/reports/messaging-audit.md;
flows/d8df70/reports/what-waits-dossier.md;
flows/9ddcbc/reports/context-meta-harness-survey-2026-09-24.md; flows/836818/log.md.

Predecessor rule: d8df70 stays crossover-only until the successor is ready; not to be
killed or silenced as a side effect.

## 3. flows/9ddcbc/psyche-medium-successor-20260924/ (Field Medium's prepared+executed guidance)

- `first-prompt.txt` — 2840 bytes. Read in full. It is titled implicitly (no heading) and
  addresses "You are Psyche Medium, running Claude Opus 5.5 at medium effort... successor
  of d8df70... Behavioral power remains Medium; your native title uses aspect and exact
  model." It gives a first-turn contract: claim Flow ID, set/read back title
  `Psyche Opus 5.5 <Flow ID>`, register the pane in HM; load the same 17-skill block from
  refresh-inject.md in one turn; acquire pointer sources (handover record,
  refresh-inject.md, log.md, the same vision files, living-words, prometheus witness, plus
  messaging-audit.md and what-waits-dossier.md and flows/836818/log.md — i.e. the pointer
  files from refresh-inject.md are pulled in as sources here too, not left as
  pointer-only); carries forward 6 duties (living's-words preservation, flashbook/Dawn
  work, messaging decisions, plain messages, coordinate with 752e0f and peers, keep d8df70
  crossover-only); required return line `PSYCHE_MEDIUM_READY <Flow ID>` plus Title/Model/
  HM/Skills/Sources/Current-work fields.
- `receipts/native-id.txt` — single line, `e5141130-9a4a-4b8f-b405-67d941a7b320`. This is
  the native session id of the pane now titled `Psyche Opus 5.5 e51411` — i.e. Field
  Medium's prepared prompt was already submitted and accepted, and the successor is live,
  not merely drafted.

**What it did not do / not present in this directory:** no launch.json / tab-create.json
/ extraction.json / readiness receipt comparable to the High-successor directory's set —
i.e. no equivalent step-by-step submission-route evidence (no record here of which
submission call was used, whether it timed out, or a prompt sha256/byte-count receipt).
Only the final prompt text and the resulting native id are captured.

## 4. flows/9ddcbc/psyche-high-successor-20260924/ (how the 752e0f pane itself was created/prompted)

- `launch.json`: input naming the target — nativeThread
  `752e0f7e-49ec-4110-b27b-6107e0eb6520`, pane `wD:pE`, terminal `term_65c3cc0d883a764`,
  agent `psyche-fable-of-836818`, model `claude-fable-5-1`, effort `medium`.
- `tab-create.json`: result of `cli:tab:create` — created pane `wD:pE` on tab `wD:tD`
  ("Psyche High successor", tab number 13), workspace `wD`. This is how the pane was
  created (a herdr tab-create call), not a manual UI action.
- `extraction.json`: found source records ("Refresh Payload — Psyche High 836818",
  "Refresh Payload Addendum — Psyche High 836818"), nothing missing, and a 30-skill list
  used for that extraction pass (broader than the 17-skill Medium block).
- `first-prompt.txt` (root, not attempt-2) — 312,872 bytes. This is the superseded first
  attempt: the prompt manifest (below) calls it "the prior 313 KB assembled packet",
  explicitly omitted from the final send. Too large to inline-read (over the 256KB read
  cap); not needed further since it was superseded.
- `attempt-2/prompt-manifest.md`: explains the second, lean prompt (~5KB) replaced the
  313KB packet — kept only living intent, role duties, predecessor-at-depth-one note,
  summary-level state, the claim/register/title/readiness contract, no-noise rule, and a
  bounded skill list; omitted full transcripts, raw logs, digests, UUIDs, inode/pane
  evidence, and historic material as "operational noise for this role."
- `attempt-2/first-prompt.txt` — the actual accepted prompt, "# Psyche High continuation",
  with the first-turn contract (load skills in one turn without pasting them; claim Flow
  ID; create flow dir + log; register via HM and set title `Psyche High <id>`; read
  current living words/records with 836818 at depth one; return exactly
  `PSYCHE_HIGH_READY flow=<short-id> title="Psyche High <short-id>"`), Living intent,
  Current state to inherit, and Psyche High duties sections — this is the structural
  template step 6 of the original task was to mirror.
- `receipts/attempt-2-preprompt-pane.txt`: a captured pane screen before send, showing
  Claude Code v2.1.280, "Fable 5.1 with medium effort", `/remote-control` active with a
  claude.ai/code session URL, confirming the pane was live and idle before the prompt
  write.
- `receipts/attempt-2-prompt-submit.json`: `"grade":"refused","ok":false`,
  `prompt_bytes:4981`, `request_bytes:5219`,
  `"response":{"error":{"code":"timeout","message":"timed out waiting for agent status"}}`,
  over socket `/home/li/.config/herdr/sessions/messaging-build/herdr.sock`. **This is the
  submission route that timed out**: a file-backed `agent.prompt` call that writes the
  prompt then waits on agent-status confirmation — the status-wait leg timed out.
- `receipts/attempt-2-readiness.json`: records `"submission": "one file-backed
  agent.prompt; transport wait timed out after write; native transcript proves one
  accepted user prompt; no resend"`, and `"nativeWrapper": "Claude recorded the prompt in
  one pasted_content wrapper"`. **This is what worked**: the write itself landed (the
  prompt reached the pane and Claude ingested it as a single pasted_content block); proof
  came from reading back the native transcript directly, not from a second submission
  call. No resend was performed after the timeout. Gates in this receipt: remoteControl
  visually witnessed active; flowClaim verified; hmRegistration verified; titleReadback
  verified; mainFlowSkill native `/main-flow` receipt verified; authoritativeSources
  verified in `flows/752e0f/receipts/authoritative-reacquisition.md`. Predecessor 836818
  preserved at depth one, not relaunched.

`flows/9ddcbc/log.md` does not exist at that path (checked; no top-level log.md under
flows/9ddcbc — only subdirectories of reports/witnesses/etc. under flows/9ddcbc), so no
tail was available there; the directory-listing of flows/9ddcbc top-level files was
captured instead (reports/*, retirements/836818-living-order-2026-09-24.md,
stack-recovery-20260923/*, vision/modelNamedSeatsAndAdaptiveRouting.md,
flow-message-acceptance/README.md, mind-sol-flow-psyche-20260923/mission.md).

## 5–7. Not performed

Steps 5 (claude-native-seat-refresh.py / native-seat-launch.mjs usage and manifest
requirements) and 6 (draft first prompt) were not carried out: the coordinator (Psyche
High 752e0f) interrupted this subflow after step 4 with an explicit stop instruction,
stating the successor already exists (e51411, HM-registered, working) and that no draft
first prompt should be written. Only this research.md was completed, from material
already read in steps 1–4 above.
