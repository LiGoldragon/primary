# Existing Codex remote-control thread names

On 2026-09-21, all 11 named targets were exact HM/Herdr bindings to existing Codex native threads. Before mutation, the app server's read-only `thread/read` confirmed each exact native ID, canonical rollout path, model, current name, and status. Each change used only the supported `thread/name/set` method. A second `thread/read` immediately before each mutation guarded against concurrent name changes; a read afterward confirmed the target, and every change emitted `thread/name/updated` for the same native ID and target name. The exact IDs, models, timestamps, and per-thread receipts are in [machine evidence](remote-thread-names.receipts.json).

| Existing name | Verified new name |
| --- | --- |
| Refresh native main flow | Mind Astra |
| mind-astra-of-98ac2e | Mind Astra (crossover 1) |
| mind-astra-of-0ab019 | Mind Astra (crossover 2) |
| Refresh native main flow | Mind Terra |
| Refresh native main flow | Mind Luna |
| Refresh native main flow | Field Astra |
| 7091ea | Field Sol |
| Refresh native main flow | Field Sol (crossover 1) |
| Refresh native main flow | Field Terra |
| field ultra low | Field Luna |
| field medium | Field Sol (crossover 2) |

The HM route without a native ID was left unknown. The newly launching Mind Sol thread was outside this change. HM registrations, Herdr route keys, and native identities were not edited. A fresh `--overview --json` after the renames found all 11 target names on exact routes. That snapshot had 14 exact routes, 13 native context observations, and one exact route without a native thread ID; the 11 renamed Codex rows all had context proxies, not exact resident-context measurements. Account quota was available as a separate observation.
