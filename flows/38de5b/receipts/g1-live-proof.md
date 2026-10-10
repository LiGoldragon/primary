# G1 live proof: Fallback-Presented to a disposable Haiku agent

Done by an Opus subflow of 38de5b on 2026-09-25, for the messenger-clj branch `m1-sender-aspect-model-38de5b` at 5171131d465c0ee80806cb485bcb81300ff6766c.

## Method

- The branch was freshly cloned into `scratchpad/messenger-clj-g1live-proof-opus3` and run from the clone through its own `bin/hm-send`. The installed package was not touched.
- State root: `HM_REGISTRY=scratchpad/g1-live-registry-opus3`. This is a copy of the earlier G1 temporary registry, which holds the sender route for 38de5b (pane wD:pR, terminal term_65c500aa730757c). The live ledger was not written.
- Recipient: in Herdr session messaging-build, `herdr tab create --workspace wD --label g1live-disposable-haiku-opus3 --no-focus` created tab `wD:tJ` with root pane `wD:pV` and terminal `term_65c55316a42d287`. The pane ran in a scratch directory.
- Start: `herdr agent start g1live-haiku-opus3 --kind claude --pane wD:pV --timeout 120000 -- --model claude-haiku-4-5-20251001 --dangerously-skip-permissions`. It answered `agent_started` with `interactive_ready: true` and `agent_status: idle`, agent session c5a32a43-f0fe-4c6a-803b-6952ad53db63. The footer read `Haiku 4.5`. The terminal title showed `Psyche Opus b87854`; the source of that title was not investigated.
- The disposable agent was not registered.

## Sends and receipts

Marker: `G1LIVE9bcf3c48`

1. At 21:14:07Z, pre-send status idle, the command was `FLOW_ID=38de5b hm-send g1live --pane wD:pV '<body>' --wait-presented`.
   Receipt: `Held.{ g1live NotRegistered attempt-58bf3051-1df }` (exit 1).
   Nothing was typed: before the second send, the pane held no marker text. The cause is that `--pane` takes `<session>:<pane>`. `parse-pane` splits on the first colon, so `wD:pV` was read as session `wD`, pane `pV`. No live agent matched, the fallback failed, and with no stored route the Held reason was NotRegistered. That reason misleads, because the actual fault is a pane that did not resolve.
2. At 21:14:29Z, pre-send status idle, the command was `FLOW_ID=38de5b hm-send g1live --pane messaging-build:wD:pV 'G1LIVE9bcf3c48 disposable delivery test: reply with the single word ACK and do nothing else.' --wait-presented`.
   Receipt: `Fallback-Presented.{ g1live idle }` (exit 0, returned 21:14:40Z).

There was no Uncertain result and no retry.

## Observed pane text (`herdr agent read wD:pV`, after send 2)

```
❯ #msg ["38de5b" "G1LIVE9bcf3c48 disposable delivery test: reply with the single word ACK and do nothing else."]
● ACK
✻ Worked for 1s · done 3:14 PM
```

After the send, `herdr agent get wD:pV` showed `agent_status: done` and `state_change_seq: 4786`, up from 4784 at start. The envelope was typed exactly as HM builds it, and the agent reacted by answering ACK.

## Herdr 0.8.2 reply shape for a waited prompt

Two direct waited prompts were sent to the same disposable agent. Neither was sent through HM, and neither bypassed an HM refusal.

- At 21:14:52Z, the same arguments HM uses (`--wait --until working --until idle --until done --until blocked --timeout 10000`):
  ```
  {"id":"cli:agent:prompt","result":{"agent":{"agent":"claude","agent_session":{"agent":"claude","kind":"id","source":"herdr:claude","value":"c5a32a43-f0fe-4c6a-803b-6952ad53db63"},"agent_status":"working","cwd":"…/g1live-haiku-cwd-opus3","focused":false,"foreground_cwd":"…/g1live-haiku-cwd-opus3","interactive_ready":true,"name":"g1live-haiku-opus3","pane_id":"wD:pV","revision":4,"state_change_seq":4787,"tab_id":"wD:tJ","terminal_id":"term_65c55316a42d287","terminal_title":"◑ Psyche Opus b87854","terminal_title_stripped":"Psyche Opus b87854","workspace_id":"wD"},"type":"agent_prompted"}}
  ```
- At 21:15:00Z, the old HM form (`--wait --timeout 5000`):
  ```
  {"id":"cli:agent:prompt","result":{"agent":{… "agent_status":"done", … "state_change_seq":4790, … "pane_id":"wD:pV", …},"type":"agent_prompted"}}
  ```
  This returned in about 3 s, because Haiku settled quickly.

Findings:

- A waited prompt answers `result.type = "agent_prompted"`. Its `result.agent` is the pane's AgentInfo, with the first matching post-prompt `agent_status` and a raised `state_change_seq`.
- Neither reply has a `presented` field. This confirms the G1 finding against live Herdr: the pre-c72fc9d check could never succeed.
- The old `--wait --timeout 5000` form does not always fail. It succeeds when the agent settles within 5 s. The f5a74e Unknown therefore fits a target that stayed working past 5 s, together with the missing `presented` field. The second cause is certain; the first is inferred.
- HM's printed state after send 2 was `idle`, while the direct HM-argument call returned `working`. Both are first-matching states and both are valid. The difference was not investigated.

## Cleanup

- `herdr tab close wD:tJ` answered `{"type":"ok"}`.
- `herdr pane get wD:pV` answered `pane_not_found`, and `herdr tab get wD:tJ` answered `tab_not_found`.
- `herdr agent list` shows no g1live agent, and no process remains for session c5a32a43.
- No live flow pane was touched. The real HM registry was neither read for routing nor written.
