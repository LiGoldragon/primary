# Route manifest for the Messenger sender-identity cutover — 38de5b, 2026-09-25

Built read-only against branch m1-sender-aspect-model-38de5b@f592ede; nothing registered or sent. Mind 00f95a's gate: re-register the 12 live routes before cutover; stale rows stay roleless.

**Sources.** Registrations come from `hm-list` and `hm-heartbeat-state`: 43 routes, 11 retirements. Live agents come from `herdr --session messaging-build agent list`; the `default` session has none. The register syntax comes from branch `origin/m1-sender-aspect-model-38de5b` at `f592ede`, cloned to `/tmp/claude-1001/-home-li-primary/38de5bbb-be48-4bae-883e-2d622fb79c9e/scratchpad/routemanifest-1790370203/messenger-clj`. The model evidence is each pane's launch command line, plus the model recorded in its Codex rollout or Claude transcript.

**What the branch requires.** Registration is `hm-register FLOW NAME --session S --native-thread T` plus either `--aspect` with `--model`, or `--launch-receipt`. The receipt must have `canonicalRole.aspect` and a top-level `model`, and must name the same Flow. `--model` accepts a family name or a full model id, but only the family is stored. If Herdr doesn't report the pane as interactive-ready, `register!` refuses unless given `--readiness-probe HM_READY_… --rollout PATH`. That probe types a prompt into the target pane, so it is a mutation for the cutover operator to authorise.

### Live routed rows (12)
All are in session `messaging-build`. "Witnessed" means a launcher receipt or launch profile, or the harness itself, shows the value. "Inferred" means only the log header, title or agent name shows it. The `* ready?` column holds Herdr's interactive-ready flag; `–` means it is missing.

| flow | pane | terminal | state (ready?) | aspect (source, conf) | model (source, conf) |
|---|---|---|---|---|---|
| 00f95a | wM:pB | term_65c3ff8204dc373 | working (–) | mind (log header "Mind Sol 00f95a" + title; no role receipt) **inferred** | sol, gpt-6-sol (rollout; log) witnessed |
| 26c50c | wM:pC | term_65c41e8c721447a | done (–) | mind (receipt `5f38bc/mind-astra-native/receipts/mind-astra.json`, Mind High, threadId matches route) witnessed | astra, gpt-6-astra (receipt + rollout) witnessed |
| f5a74e | wM:pD | term_65c52095db80f82 | idle (ready) | mind (receipt `5f38bc/mind-astra-staged-for-review/receipt.json`; its Herdr pane and terminal match) witnessed | astra, gpt-6-astra (receipt + rollout) witnessed |
| a676b3 | wM:pF | term_65c5414e9aa9884 | done (ready) | mind (receipt `00f95a/launches/field-clj-receipt.json`, Mind Medium; pane and terminal match) witnessed | sol, gpt-6-sol (receipt + rollout) witnessed |
| 5f38bc | wQ:pN | term_65c3ff14cafb070 | done (–) | field (log restates a user-supplied launcher receipt; title "Field Astra 5f38bc"; no receipt JSON found) **inferred** | astra, gpt-6-astra (rollout) witnessed |
| b7da5d | wQ:pT | term_65c41aac961f978 | done (–) | field (receipt `5f38bc/field-sol-native/receipts/field-sol.json`, Field Medium) witnessed | sol, gpt-6-sol (receipt + rollout) witnessed |
| e71dab | wQ:pV | term_65c41cd7bd31479 | idle (–) | field (receipt `5f38bc/field-luna-native/receipts/field-luna.json`, Field Low) witnessed | luna, gpt-6-luna (receipt + rollout) witnessed |
| 98eb43 | wQ:pW | term_65c5100e5cf517e | idle (ready) | field (receipt `5f38bc/field-monitor-launch/receipt.json`, Field Low) witnessed | luna, gpt-6-luna at low effort (receipt + rollout) witnessed |
| 504461 | wQ:pX | term_65c543d588df185 | done (ready) | field (receipt `00f95a/launches/field-astra-receipt.json`, Field High; pane and terminal match) witnessed | astra, gpt-6-astra (receipt, rollout, launch command) witnessed |
| d8df70 | wD:pD | term_65c2be0c1adcd62 | idle (ready) | psyche (log header "Psyche Medium"; title) **inferred** | opus witnessed; exact id **conflicts** (launch command says claude-opus-5, latest transcript turns say claude-opus-5-5) |
| e51411 | wD:pF | term_65c3d2d430e6265 | working (ready) | psyche (log header "Psyche Medium"; title) **inferred** | opus, claude-opus-5-5 (launch command, transcript, status line "Opus 5.5") witnessed |
| 38de5b | wD:pR | term_65c500aa730757c | working (ready) | psyche (launch profile `5f38bc/psyche-fable-refresh/profile.json`, role "Psyche High"; log) witnessed | fable, claude-fable-5-1 (launch command, transcript, profile) witnessed |

Two anomalies:
- **d8df70:** Herdr reports the pane's Claude session as `97d78b53-…`. That id belongs to an SDK test-harness transcript from `/tmp/claude-1001/test-harness`, not to the route's native thread `d8df703d-…`. Pass `--native-thread` explicitly.
- **f5a74e and 98eb43:** Herdr shows the terminal title as only "primary".

### Register lines the branch would need
```
FLOW_ID=00f95a hm-register 00f95a mind-sol-00f95a --session messaging-build --native-thread 01a0d4ec-9746-7340-b60c-84300f95aa7c --aspect mind --model gpt-6-sol --readiness-probe HM_READY_00f95a_<fresh> --rollout /home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T13-37-50-01a0d4ec-9746-7340-b60c-84300f95aa7c.jsonl
FLOW_ID=26c50c hm-register 26c50c mind-astra-26c50c --session messaging-build --native-thread 01a0d579-f7e3-72e3-8444-65826c50c59f --launch-receipt /home/li/primary/flows/5f38bc/mind-astra-native/receipts/mind-astra.json --readiness-probe HM_READY_26c50c_<fresh> --rollout /home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T16-12-15-01a0d579-f7e3-72e3-8444-65826c50c59f.jsonl
FLOW_ID=f5a74e hm-register f5a74e mind-astra-f5a74e --session messaging-build --native-thread 01a0d997-a21c-7903-b997-b34f5a74e208 --launch-receipt /home/li/primary/flows/5f38bc/mind-astra-staged-for-review/receipt.json
FLOW_ID=a676b3 hm-register a676b3 mind-sol-a676b3 --session messaging-build --native-thread 01a0da22-1cab-7aa1-89d7-9b4a676b3fc7 --launch-receipt /home/li/primary/flows/00f95a/launches/field-clj-receipt.json
FLOW_ID=5f38bc hm-register 5f38bc field-astra-5f38bc --session messaging-build --native-thread 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 --aspect field --model gpt-6-astra --readiness-probe HM_READY_5f38bc_<fresh> --rollout /home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T13-48-34-01a0d4f6-6bc6-7530-94d6-1515f38bcb84.jsonl
FLOW_ID=b7da5d hm-register b7da5d field-sol-b7da5d --session messaging-build --native-thread 01a0d54c-9013-73f3-8ab2-c55b7da5da58 --launch-receipt /home/li/primary/flows/5f38bc/field-sol-native/receipts/field-sol.json --readiness-probe HM_READY_b7da5d_<fresh> --rollout /home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T15-22-39-01a0d54c-9013-73f3-8ab2-c55b7da5da58.jsonl
FLOW_ID=e71dab hm-register e71dab field-luna-e71dab --session messaging-build --native-thread 01a0d572-6ba1-7b20-bdcf-f29e71dabb46 --launch-receipt /home/li/primary/flows/5f38bc/field-luna-native/receipts/field-luna.json --readiness-probe HM_READY_e71dab_<fresh> --rollout /home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T16-04-00-01a0d572-6ba1-7b20-bdcf-f29e71dabb46.jsonl
FLOW_ID=98eb43 hm-register 98eb43 field-monitor-01a0d9 --session messaging-build --native-thread 01a0d956-86a5-7600-9283-c8f98eb43815 --launch-receipt /home/li/primary/flows/5f38bc/field-monitor-launch/receipt.json
FLOW_ID=504461 hm-register 504461 field-astra-504461 --session messaging-build --native-thread 01a0da2a-fdbb-7262-a93b-226504461843 --launch-receipt /home/li/primary/flows/00f95a/launches/field-astra-receipt.json
FLOW_ID=d8df70 hm-register d8df70 psyche-opus-5 --session messaging-build --native-thread d8df703d-d083-4c29-9597-6b32e7411b75 --aspect psyche --model opus
FLOW_ID=e51411 hm-register e51411 psyche-opus-of-d8df70-r2 --session messaging-build --native-thread e5141130-9a4a-4b8f-b405-67d941a7b320 --aspect psyche --model claude-opus-5-5
FLOW_ID=38de5b hm-register 38de5b psyche-fable-refresh-5f38bc --session messaging-build --native-thread 38de5bbb-be48-4bae-883e-2d622fb79c9e --aspect psyche --model claude-fable-5-1
```
- **00f95a and 5f38bc** use explicit `--aspect` and `--model` because no receipt names them.
- **38de5b** can't use `--launch-receipt`: its profile has `role` but no `canonicalRole`.
- **The 5 panes without ready** (00f95a, 26c50c, 5f38bc, b7da5d, e71dab) need a probe at cutover; without one, registration is refused with "Agent is not interactively ready".

### Stale rows (31, all Bound or NeedsBinding with no live pane; they stay roleless)
0347d0, 03e825, 0625c3, 0ab019 (NeedsBinding), 1b8ac0, 1cb440, 21a218 (default), 23d977, 2c61af, 2fe3f1, 395aed, 47764b, 4b0f60, 6288d1, 634c9e (default), 6db4fe, 6fb948, 7091ea, 98ac2e, 9a79dc (NeedsBinding), 9ddcbc, 9e7ea5, c3e42e (NeedsBinding), c88918, cf3553 (NeedsBinding), d2dca6, df09b6, e798f3, e88ca4 (default), eb7bae (default), effa1b (NeedsBinding).

### Live agents with no route (4)
- **psyche-opus-b87854** (wD:pQ, term_65c40f03ab16676, idle, not ready): Flow b87854, per `flows/b87854/log.md`. It is psyche (log header, and e51411's refresh profile `e51411/receipts/psyche-opus-refresh-profile.json`: Psyche Medium, the same session id). The model is claude-opus-5-5 (launch command and status line). Aspect is inferred and model witnessed. Its main transcript `.jsonl` is missing from disk; only a `subagents/` directory exists. The pane itself says messenger registration of a Claude seat is blocked. A candidate line: `FLOW_ID=b87854 hm-register b87854 psyche-opus-b87854 --session messaging-build --native-thread b8785453-ff53-4e5a-9a74-e21edb554467 --aspect psyche --model claude-opus-5-5`. It still needs a readiness probe, which has no transcript to witness it.
- **psyche-haiku-of-b80e55** (wD:p8, term_65c0377a0776b56, idle): claude-haiku-4-5-20251001 (launch command and status line). Its title is "Psyche Ultra Low (claim pending)". It has no Flow ID, and b80e55 is retired. The model is witnessed, but there is no Flow, so no line can be written.
- **codex-2d0e71a77a40543c10ac8ac1** (w13:p1, term_65c429f01d0607b, idle): gpt-6-luna at medium effort (launch command). It is a fresh Codex that was never prompted, with no Flow and no aspect evidence.
- **g1-disposable-g1mark5b70be51** (wD:pT, term_65c550a4d612386, agent kind g1shell): a test fixture from 38de5b's scratchpad, not a Flow. It is the `- -` row in `hm-list`.
