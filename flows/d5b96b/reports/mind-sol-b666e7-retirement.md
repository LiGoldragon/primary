# Mind Sol `b666e7` retirement evidence

Writer: Field `d5b96b`, delegated executor `rotation_finish`.

This evidence was authored after successor `5104af` acceptance and a fresh passive predecessor check. The predecessor was naturally done before any lifecycle action:

- old flow: `b666e7`
- old name: `mind_sol_b666e7`
- old native UUID: `01a0e9d1-d20f-7b43-98b0-15bb666e70e1`
- old pane: `w1:pJ`
- old terminal: `term_65c915b9906ad14`
- Herdr readback: `agent_status: done`
- Messenger readback: `b666e7 mind_sol_b666e7 default done`

The accepted independent successor is `5104af`, `mind_sol`, native UUID `01a0f51b-c14f-7300-9778-3365104afba2`, candidate model `gpt-6.1-sol` at medium effort. Its full acceptance evidence is `flows/d5b96b/reports/mind-sol-5104af-successor-acceptance.md` at immutable commit `809e84762021`.

Authorized lifecycle commands to be recorded after this prewritten evidence are `herdr pane close w1:pJ` and `hm-retire b666e7 --session default --pane-id w1:pJ --terminal-id term_65c915b9906ad14 --name mind_sol_b666e7 --agent codex --native-thread 01a0e9d1-d20f-7b43-98b0-15bb666e70e1 --evidence <this-file> --evidence-sha256 <this-file-sha256>`. They retire routing only; old native files and both server processes remain retained.

## Actual closure and retirement receipt

- `herdr pane close w1:pJ` returned `{"id":"cli:pane:close","result":{"type":"ok"}}`.
- `hm-retire` with the exact arguments listed above and the prepublication SHA-256 returned: `Retired b666e7: delivery is blocked before Herdr routing`.
- Post-action `hm-list` has no `b666e7` entry; `herdr agent get mind_sol_b666e7` returns `agent_not_found`.
- `herdr agent get mind_sol` still reads the idle accepted successor in `w1:p15` with title `Mind.{ Sol 5104af } | GPT-6.1-Sol`.
- The old candidate-independent native rollout file still exists, and server PIDs `1936`, `1960`, and `1965146` remained present at verification.

The Messenger result records that delivery was blocked before Herdr routing. It is not represented as a successful message delivery. The prepublication evidence hash remains the value supplied to `hm-retire`; this appended receipt records the resulting command output at the same stable evidence path.
