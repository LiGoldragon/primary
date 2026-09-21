# Canonical seat titles and aspect workspaces — implementation checkpoint

Observed 2026-09-21 19:11–19:15 UTC in Herdr session `messaging-build`.

## Result

The exact current Codex seats now have persisted native titles, Herdr agent names, pane labels, singleton tab labels, and HM names of the form `<Aspect> <Power> <own six-character Flow ID>` and `flow-<id>`. The four current Mind tiers are ordered High, Medium, Low, Ultra Low in workspace `wM`, labeled `Mind · Current`. The four current Field tiers are in that order in `wQ`, labeled `Field · Current`. The three identified Psyche seats are ordered High, Medium, Low in `wD`, labeled `Psyche · Current`. These three workspaces contain only the identified current tiers. Historical/retained seats and their routes remain in place outside them. No route was retired, no native process restarted, and no paid status probe was sent for these moves.

| Aspect/workspace | Current canonical tabs, in order | Remaining gap |
| --- | --- | --- |
| Mind `wM` | High `4b0f60`; Medium `2c61af`; Low `e798f3`; Ultra Low `23d977` | None in workspace. |
| Field `wQ` | High `03e825`; Medium `753e69`; Low `0347d0`; Ultra Low `c88918` | None in workspace. |
| Psyche `wD` | High `1b8ac0`; Medium `b80e55`; Low candidate `0625c3` | No uniquely accepted Ultra Low seat; Low acceptance/readiness not proven. |

`1b8ac0` is the live Fable process bound to the current High route; the owner's recollection of `f38926` refers to historical evidence and is not a current HM target. `b80e55` is the accepted Medium. The current Low route exists but its tier acceptance is still open. These distinctions come from the live Herdr/HM inventory and `flows/6db4fe/reports/twelve-flow-health.md`; no missing seat was fabricated.

The old Field Astra coordinator `6db4fe` and retained Mind crossover `9e7ea5` were moved, with their exact live processes, into workspace `wK`, labeled `Retained / Coordination`, alongside existing retained `98ac2e`. Exact HM terminal IDs, native UUIDs, and process PIDs matched after transfer. The coordinator's Codex native title already read `Field High 6db4fe`; its Herdr agent/HM name is now `flow-6db4fe`, pane label `Field High 6db4fe`, and tab label `Coordination Field High 6db4fe`. Retained tabs/panes show their own Flow IDs. Other historical routes outside the three current aspect workspaces were not moved or retired. A stale HM record or closed pane was never used as a move target.

## Guarded pane transfer

`tools/hm-move` and `tools/hacky-messenger/hm.py` now transfer one exact Flow pane under the same Orchestrate registry reservation as HM delivery. The caller supplies the registered old route, native UUID, and witnessed foreground PID. The helper checks exact Herdr agent, terminal, native process and collision state, writes a route hold, moves the pane, verifies the same process and terminal at the returned pane, and atomically updates the HM pane ID before releasing the reservation. If a move fails after Herdr acts, it makes a compensating move and binds the *returned* pane ID. A cross-workspace reverse does not restore the old pane ID. An uncertain move leaves delivery held for manual repair instead of sending to stale routing.

A disposable non-agent shell demonstrated `wM:p7 → wQ:pB → wM:p8` with one unchanged terminal/PID; its test pane was closed. The live cross-workspace transfers were `1b8ac0` and `0625c3` into `wD`, and `0347d0` and `c88918` into `wQ`. Same-workspace new-tab moves ordered the eligible canonical tiers. The working Field High seat was not moved: it already precedes the other current Field tiers. Post-move readback for each transferred route matched HM terminal ID, Herdr workspace and foreground process, with no route hold. The existing native UUID remained in each HM record.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/hacky-messenger -q` passed 25 tests, including stale UUID/PID refusal, collision refusal, move, same-workspace ordering, compensation to a new pane ID, and uncertain-result delivery hold. Source commits `0bb0b5d2` and `611f7f9c` were pushed and read back on `main@origin`.

## Native title limit

The Codex native titles were corrected through the supported app-server title path and revalidated by exact native thread. Claude native title changes remain frozen. One targeted `herdr agent prompt wQ:p4 '/rename Psyche High 1b8ac0'` updated the native/terminal title in three separate Claude sessions (`1b8ac0`, `b80e55`, `0625c3`). Herdr addressed one pane; installed Claude 2.1.263 shares one `CLAUDE_JOB_DIR` across those processes. Its `/rename` writes the shared job state and sibling title watchers adopt the same title. Distinct PIDs, PTYs, native session IDs, and per-session custom-title events confirmed this was title-state fan-out, not a Herdr prompt broadcast. The incorrect Claude native titles for Medium and Low are retained as observed; their Herdr tab/pane labels and HM routes remain individually correct. A launcher source isolation fix and same-native-session refresh are separately owned. Do not invoke `/rename`, native UDS rename, or manually edit transcripts on these shared-job processes.

`tools/canonical-title-alignment.mjs` remains guarded: the Claude native adapter is disabled for live apply; its route-only mode aligns Herdr/HM without claiming native title repair. The exact title source and tests are in `tools/canonical-title-alignment.mjs` and `.test.mjs` (commits `842c9e79`, `681f514c`).

## Open ownership

The Psyche owner/Luna coordinator must identify and accept a distinct Ultra Low native seat and resolve the Low acceptance gate. The Claude launcher owner must isolate per-session job state before independently repairing native titles, preserving the same UUID/context and verifying each title no longer propagates. The Field Astra successor owns continued lifecycle/title integration and must retain the old Field routes until its separate handoff gates are met. Existing process/route continuity and current workspace grouping are proved here; a complete twelve-seat readiness claim is not.
