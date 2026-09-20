# Ghost-flow reap audit — no safe target

The living requested reaping with Luna. Existing Field Reap Luna 21a218 was asked to execute only exact safe candidates. A separate Luna read-only audit checked HM registrations, Herdr panes/processes, locks, native/transcript evidence, and retirement markers. Both concluded that **zero candidates pass the reap gates**. No flow was reaped, deregistered, or retired.

| HM Flow ID | Observation | Disposition |
| --- | --- | --- |
| 53067b, 8565e8 | Both stale rows bind the same live Codex pane `wH:p1`, PID 825621, native `01a0bb1c-5142-7763-9ea6-6638565e8508`. | Hold; live process. |
| 1cb440 | Live `wJ:p1`, PID 1057539, native `01a0bb1c-5082-7593-8f81-71e1cb4409ef`. | Hold; live process. |
| 2fe3f1 | Live `wZ:p2`, PID 1684149, native `01a0c019-fedc-7ad3-abfe-c3f2fe3f13f5`. | Hold; live process. |
| 0625c3 | Live Claude `wS:p1`, PID 1647093 with server child 1647214; native session `0625c31b-798d-44f7-a116-44a7966fe618`. | Hold; live process. |
| b81560 | Registered pane `wD:p1` still exists, now foreground zsh PID 4105305. Living explicitly closed its native session and required transcript/Flow preservation; registration cleanup was not proven. | Hold; closure alone is insufficient. Never resume its native session. |
| cf3553, c3e42e, 9a79dc | Registered panes `w6:p1`, `w8:p1`, `wE:p1` are absent; prior judgment explicitly protects these records. | Hold; absent pane is insufficient. |
| effa1b | Registered `wC:p2` is absent; registration lacks a native thread, retained transcript binding, and retirement evidence. | Hold; exact identity and closure proof unavailable. |

No candidate matched an observed lock in `orchestrate Observe.Locks`, but absence of a lock does not prove no job. The available local `flow` CLI does not expose a no-job observation, and none of these HM records has a valid retirement marker. An exact no-job and retained-evidence gate therefore remains open. In particular, the Mind ownership transfer to 4b0f60 does not turn 9e7ea5, 98ac2e, or 0ab019 into ghosts; their crossover routes and retained writers remain protected.

Read-only checks used `hm-list`, exact `herdr pane get` and `pane process-info`, `orchestrate Observe.Locks`, HM registration files under `~/.local/state/hacky-messenger/`, and available Flow records. `tools/hacky-messenger/hm.py` requires exact native identity and hashed retirement evidence; stale registration is not itself an ended-Flow witness.
