Independent Field startup witness — completed

Identity and scope:

- Parent Field successor native thread: `01a0f603-8dc3-7fb0-bde5-6ace2a70a4eb`.
- This delegated fork-none subflow native thread: `01a0f603-c973-7012-88f8-e6236f9cabca`, observed in the parent transcript’s `SubAgentActivity` start event. It is a witness subflow, not the Field seat.
- Flow identity: `e2a70a`; flow directory: `/home/li/primary/flows/e2a70a`.
- This report uses only evidence already read during the completed witness. No new host, source, readiness, socket, registration, or predecessor checks were made for this request.

Startup assessment: **PASS, scoped to independent Field-seat startup and acceptance.**

Direct parent-native evidence from:

`/home/li/.codex-next-8mkkxq293hk2/sessions/2026/09/30/rollout-2026-09-30T23-50-23-01a0f603-8dc3-7fb0-bde5-6ace2a70a4eb.jsonl`

- `session_meta` identifies the native thread above and cwd `/home/li/primary`.
- `turn_context` records `gpt-6-astra`, effort `medium`, approval policy `never`, sandbox `danger-full-access`.
- Completed command `flow-id codex --flows-root /home/li/primary/flows` exited `0` and returned `e2a70a`.
- Connected `codex_tui.set_thread_title` succeeded with `Field.{ Astra e2a70a }`.

Actual candidate-launch and connection evidence was read from Mind Sol `5104af`’s bounded native transcript:

`/home/li/.codex-next-8mkkxq293hk2/sessions/2026/09/30/rollout-2026-09-30T19-37-12-01a0f51b-c14f-7300-9778-3365104afba2.jsonl`

- Command event ordinal `362`, completed, captured Herdr pane `w1:p16` foreground argv for a live candidate client:
  `codex-next-candidate-0.161.0-alpha.2`, `-m gpt-6-astra`,
  `-c model_reasoning_effort="medium"`, `-s danger-full-access`,
  `-a never`, and
  `--remote unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock`.
- Ordinal `369`, completed, reported:
  `FIRST_PROMPT_VERIFIED 9 14291 c9022bd684f1a86c3fc414cabf849bad44b10efd332b29f1935d30eef7cef419`
  and `EXACT_PROMPT_MATCH True`.
- That same completed command observed candidate client PID `2745175` and its Unix peer candidate server PID `1965146`.
- Ordinal `397` had overall exit `1` from a later wait, but its successful rename response reports `w1:p16` with native session UUID `01a0f603-8dc3-7fb0-bde5-6ace2a70a4eb`, name `field_astra_e2a70a`, and terminal title `Field.{ Astra e2a70a }`.
- Ordinal `404`, completed, executed:
  `hm-register e2a70a field_astra_e2a70a --session default --native-thread 01a0f603-8dc3-7fb0-bde5-6ace2a70a4eb`
  and returned:
  `Registered e2a70a: field_astra_e2a70a (default)`.

Earlier bounded local metadata evidence:

- Candidate server process PID `1965146` was observed with:
  `codex app-server --remote-control --listen unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock`.
- The candidate socket existed, mode `0600`, owner `li:users`; its mtime matched the observed candidate server start.
- An earlier `ss -xlpn` listing did not display that pathname. Later peer evidence and the live server process mean that omission is not evidence of a broken service; no repair conclusion was made.
- The prepared Field launcher was read only as corroborating launch metadata. It is not the actual-launch witness; the actual witness is the Mind Sol pane/process record above.

Flow artifacts read:

- [`flows/e2a70a/index.md`](/home/li/primary/flows/e2a70a/index.md) identifies the same UUID, lane, canonical flow-id result, and candidate endpoint.
- [`flows/e2a70a/log.md`](/home/li/primary/flows/e2a70a/log.md) contains the substantive Field reconciliation:
  - accepts coordination of both living tasks;
  - preserves Mind Sol `5104af` as sole migration executor;
  - preserves Field Sol `1bc255` as sole AP host diagnosis/repair executor;
  - preserves old d5 and requests no lifecycle action;
  - retains the held source-pointer obligation;
  - keeps the phone test pending;
  - makes no Bubblewrap repair or qualification claim.
- [`flows/index.md`](/home/li/primary/flows/index.md) line 236 records `field, e2a70a` with Mind Sol migration coordination and Field Sol as sole AP executor.
- Published startup revisions observed:
  - `f1517cd4e879c580ffc47f7a74d4211e13b9118c` — establish Field lane/index.
  - `e4d60985bf1209cccc51eaf3896c85c01b0b4fc8` — record Field native and coordination evidence.

Remaining facts and limits:

- The new Field-held source send was observed as `Held.{ 1bc255 Blocked attempt-2655b5d1-6b3 }`; nothing was typed. Delivery remains pending.
- Phone-path evidence remains pending. Field Sol’s AP work remains active; no AP repair or host mutation is witnessed here.
- Bubblewrap remains technically unqualified. The optional earlier Field pilot `f69847` is a separate existing pilot and its Bubblewrap failure was inconclusive; it is not evidence about this fresh fork-none Field Astra successor.
- No predecessor d5 state, retirement, closure, server retirement, or Bubblewrap remedy is witnessed or authorized by this report.
- The pass result concerns only startup identity, candidate launch/binding, lane/index, registration, and acceptance scope.