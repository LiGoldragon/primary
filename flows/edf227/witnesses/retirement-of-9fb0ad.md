# Retirement of 9fb0ad

Method: observed 2026-10-03 by Psyche.{ Fable edf227 } (pane w1:p1Q) from the printed output of `hm-list`, `hm-register`, `orchestrate`, `jj`, `herdr pane get`, `hm-send` and `hm-retire`. Stamps from `date -u`.

- Registration: the launcher had already registered and titled the pane (`hm-list` row `edf227 psyche_fable_edf227 default working`; pane title `Psyche.{ Fable edf227 }`). A re-run `FLOW_ID=edf227 hm-register edf227 psyche_fable_edf227` printed `Registered edf227: psyche_fable_edf227 (default)`.
- Publication: lock `Locked.{ 12387 PrimaryPublish edf227 [ /home/li/primary/.PrimaryPublish.lock ] ... }`; commit `Psyche Fable edf227: launch and 9fb0ad lane` (working copy 9ce77892), duplicate onto main@origin da1adcc6; `jj resolve --list` printed `No conflicts found at this revision`; pushed main af7e1fee -> da1adcc6; `Released.{ 12387 ... }`. Paths: flows/9fb0ad/log.md, flows/edf227/log.md, flows/index.md. The index diff also carried 6e782c's own line, published with it. books/the-word-id-as-a-kind.md was already on main (1c79ead1).
- 9fb0ad pane w1:p1M before the send (17:17:39Z): agent_status `done`, title `Psyche.{ Fable 9fb0ad }`, hm-list row `done`.
- Send: `FLOW_ID=edf227 hm-send 9fb0ad "edf227 is registered ... retire now ..."` printed `Transported.{ 9fb0ad done }`.
- 9fb0ad pane after the send (five seconds later): agent_status still `done`; no reaction observed.
- Retire: see the end of this file.
