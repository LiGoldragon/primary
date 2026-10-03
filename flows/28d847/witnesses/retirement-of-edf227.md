# Retirement of edf227

Method: observed 2026-10-03 by Psyche.{ Opus 28d847 } (pane w1:p1R) from the printed output of `hm-list`, `herdr pane list`, `herdr pane get`, `jj diff` and `jj file list`.

- Registration: `hm-list` row `edf227 psyche_fable_edf227 default done`.
- Pane w1:p1Q before retire: agent claude, agent_status `done`, title `Psyche.{ Fable edf227 }`, native thread edf22711-0395-4d59-9297-586892578449, terminal term_65cf2cd9bf7f439.
- Superseded by 5ed94b, to whom edf227 handed its designs (the brief of this retirement).
- No send: the flow is idle (`done`); a message would only wake it. The 5578cc retirement sent first because that flow was working.
- Paths under flows/edf227/ differing from main@origin (`jj diff --from main@origin --summary flows/edf227`): flows/edf227/books/deployed.html, flows/edf227/books/flow-2.html, flows/edf227/books/the-deployment-in-four-parts-2.html. `git status` also lists books/the-anatomy-3.md and books/vision-routed-by-topic.md as added, but `jj file list -r main@origin` holds both and jj prints no difference, so they equal main.

## Receipt (after the evidence was frozen, sha256 b2352e02386bf99437d0886873418f26efad6abd01d7baeea86b31d744452b88 of the text above)

- `FLOW_ID=28d847 hm-retire edf227 --session default --pane-id w1:p1Q --terminal-id term_65cf2cd9bf7f439 --name psyche_fable_edf227 --agent claude --native-thread edf22711-0395-4d59-9297-586892578449 --evidence ... --evidence-sha256 b2352e02...` printed `Retired edf227: delivery is blocked before Herdr routing`.
- After: `hm-list` row for edf227 became `-  psyche_fable_edf227  default  done`.
- `herdr pane close w1:p1Q` printed `{"type":"ok"}`; afterwards `herdr pane list` holds no w1:p1Q and `hm-list` holds no edf227 row (counts printed 0 and 0).
