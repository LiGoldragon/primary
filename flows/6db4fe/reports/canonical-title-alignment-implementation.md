# Canonical seat titles and aspect workspaces — implementation checkpoint

Observed 2026-09-21 19:11–19:15 UTC in Herdr session `messaging-build`.

## Result

The exact current Codex seats now have persisted native titles, Herdr agent names, pane labels, singleton tab labels, and HM names of the form `<Aspect> <Power> <own six-character Flow ID>` and `flow-<id>`. The four current Mind tiers are ordered High, Medium, Low, Ultra Low in workspace `wM`, labeled `Mind · Current`. The four current Field tiers are in that order in `wQ`, labeled `Field · Current`. The three identified Psyche seats are ordered High, Medium, Low in `wD`, labeled `Psyche · Current`. These three workspaces contain only the identified current tiers. Historical/retained seats and their routes remain in place outside them. No route was retired, no native process restarted, and no paid status probe was sent for these moves.

| Aspect/workspace | Current canonical tabs, in order | Remaining gap |
| --- | --- | --- |
| Mind `wM` | High `4b0f60`; Medium `2c61af`; Low `e798f3`; Ultra Low `23d977` | None in workspace. |
| Field `wQ` | High `03e825`; Medium `753e69`; Low `0347d0`; Ultra Low `c88918` | None in workspace. |
| Psyche `wD` | High `1b8ac0`; Medium `b80e55`; Low `0625c3` | No uniquely accepted Ultra Low seat. |

`1b8ac0` is the live Fable process bound to the current High route; the owner's recollection of `f38926` refers to historical evidence and is not a current HM target. `b80e55` is the accepted Medium. The `0625c3` owner subsequently confirmed the direct living instruction assigning it Psyche Low in its native transcript and accepted same-native-session continuity; this corrects the earlier provisional Low grade without implying its title/job isolation is complete. These distinctions come from the live Herdr/HM inventory, `flows/6db4fe/reports/twelve-flow-health.md`, and the Low owner's explicit checkpoint; no missing seat was fabricated.

The old Field Astra coordinator `6db4fe` and retained Mind crossover `9e7ea5` were moved, with their exact live processes, into workspace `wK`, labeled `Retained / Coordination`, alongside existing retained `98ac2e`. Exact HM terminal IDs, native UUIDs, and process PIDs matched after transfer. The coordinator's Codex native title already read `Field High 6db4fe`; its Herdr agent/HM name is now `flow-6db4fe`, pane label `Field High 6db4fe`, and tab label `Coordination Field High 6db4fe`. Retained tabs/panes show their own Flow IDs. Other historical routes outside the three current aspect workspaces were not moved or retired. A stale HM record or closed pane was never used as a move target.

## Guarded pane transfer

`tools/hm-move` and `tools/hacky-messenger/hm.py` now transfer one exact Flow pane under the same Orchestrate registry reservation as HM delivery. The caller supplies the registered old route, native UUID, and witnessed foreground PID. The helper checks exact Herdr agent, terminal, native process and collision state, writes a route hold, moves the pane, verifies the same process and terminal at the returned pane, and atomically updates the HM pane ID before releasing the reservation. If a move fails after Herdr acts, it makes a compensating move and binds the *returned* pane ID. A cross-workspace reverse does not restore the old pane ID. An uncertain move leaves delivery held for manual repair instead of sending to stale routing.

A disposable non-agent shell demonstrated `wM:p7 → wQ:pB → wM:p8` with one unchanged terminal/PID; its test pane was closed. The live cross-workspace transfers were `1b8ac0` and `0625c3` into `wD`, and `0347d0` and `c88918` into `wQ`. Same-workspace new-tab moves ordered the eligible canonical tiers. The working Field High seat was not moved: it already precedes the other current Field tiers. Post-move readback for each transferred route matched HM terminal ID, Herdr workspace and foreground process, with no route hold. The existing native UUID remained in each HM record.

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/hacky-messenger -q` passed 25 tests, including stale UUID/PID refusal, collision refusal, move, same-workspace ordering, compensation to a new pane ID, and uncertain-result delivery hold. Source commits `0bb0b5d2` and `611f7f9c` were pushed and read back on `main@origin`.

## Native title limit

The Codex native titles were corrected through the supported app-server title path and revalidated by exact native thread. Claude native title changes remain frozen. One targeted `herdr agent prompt wQ:p4 '/rename Psyche High 1b8ac0'` updated the native/terminal title in three separate Claude sessions (`1b8ac0`, `b80e55`, `0625c3`). Herdr addressed one pane; installed Claude 2.1.263 shares one `CLAUDE_JOB_DIR` across those processes. Its `/rename` writes the shared job state and sibling title watchers adopt the same title. Distinct PIDs, PTYs, native session IDs, and per-session custom-title events confirmed this was title-state fan-out, not a Herdr prompt broadcast. The incorrect Claude native titles for Medium and Low are retained as observed; their Herdr tab/pane labels and HM routes remain individually correct. A launcher source isolation fix and same-native-session refresh are separately owned. Do not invoke `/rename`, native UDS rename, or manually edit transcripts on these shared-job processes.

`tools/canonical-title-alignment.mjs` remains guarded: the Claude native adapter is disabled for live apply; its route-only mode aligns Herdr/HM without claiming native title repair. The exact title source and tests are in `tools/canonical-title-alignment.mjs` and `.test.mjs` (commits `842c9e79`, `681f514c`).

## Open ownership

The Psyche owner/Luna coordinator must identify and accept a distinct Ultra Low native seat. The Claude launcher owner must isolate per-session job state before independently repairing native titles, preserving the same UUID/context and verifying each title no longer propagates. The Field Astra successor owns continued lifecycle/title integration and must retain the old Field routes until its separate handoff gates are met. Existing process/route continuity and current workspace grouping are proved here; a complete twelve-seat readiness claim is not.

## Later same-session title repair and Ultra workspace correction

The preceding native-title limit describes the earlier shared-job processes. Subsequently, the launcher source isolation fix passed its full remote native-seat fixture suite. Each of the three existing Psyche sessions was gracefully exited and resumed with `--resume` of its **same native UUID** in its **same Herdr pane and HM route**, with the original model, effort and remote-control arguments. Each now has a distinct `CLAUDE_JOB_DIR`, no inherited Claude session-ID variables, and the same transcript inode and sampled tail. Medium `b80e55` and Low `0625c3` received their correct titles through the isolated native `/rename` command; High `1b8ac0` already had the correct title. Sibling native titles remained unchanged after each action. Machine receipts: `flows/6db4fe/claude-isolation/b80e55-runtime.json`, `0625c3-runtime.json`, and `1b8ac0-runtime.json` (remote commits `15236be9`, `96b01e41`, `bd5a3c5e`). This did not create a new Flow or pay for a model status turn. The live Claude adapter in the generic title script remains disabled; it has not been proved safe for arbitrary shared-job seats.

The first Psyche Ultra launch attempt used historical workspace `wS`, which no longer exists after the Low pane was moved into current Psyche workspace `wD`. It failed **before a pane or native session was created**; its failed state was preserved in `flows/03e825/reports/psyche-ultra-launch-attempt.md`. The successor launch owner was given the exact current target `wD` for a bounded manifest-only correction and retry. At this checkpoint, `wD` contains only the three witnessed Psyche High, Medium and Low seats; Ultra is not counted until its own native and route receipts exist. The Mind `wM`, Field `wQ`, and retained `wK` groupings remain as recorded above.
