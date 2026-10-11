# Flow audit 2026-10-10

Sources: `hm-list` (state), `herdr agent list` / `herdr pane list` (live panes), `harness UsageSnapshotQuery` (context tokens, last-request source), `flows/index.md` (topic, predecessors), `flows/<id>/log.md` (last line). Context tokens are the snapshot's observed value; the harness labelled each row Proxy or Superseded (meaning not established here). Codex shows used/window.

| flow | aspect / layer / topic | harness, model | ctx tokens | state | successor / superseded | dir, log last line |
|---|---|---|---|---|---|---|
| 42265e | Field Sol; local Ouranos host audit, cleanup executor | Codex gpt-6.1-sol | 155845/354350 | done | successor of an earlier Field Sol; none after | yes; 10-03 Opus authorized fresh Start on Astra's unwrapped-readback/session-binding build |
| 41fa34 | Mind Sol; operation-skill and Astra Flow review | Codex gpt-6.1-sol | 160319/354350 | working | registered successor of 5104af | yes; 10-04 Typesafe CEO interview report requested |
| 8f0f57 | Psyche Tertiary Sonnet | Claude sonnet-5-5 | 139815 | done | none found | no dir |
| 918df4 | Mind Tertiary Luna | Codex gpt-6-luna | 100220/258400 | done | none found | empty dir, no log |
| 02dda6 | Psyche Quaternary Sonnet | Claude sonnet-5-5 | 123548 | done | none found | dir (notion, vision), no log |
| 4ddfe1 | Mind (quaternary) Luna | Codex gpt-6-luna | 47834/258400 | done | none found | no dir |
| 4371ed | Field Tertiary | Codex gpt-6-luna | 73793/258400 | done | none found | empty dir, no log |
| 6aa08d | Field Quaternary (Mind six-seat controller) | Codex gpt-6-luna | 61670/258400 | done | none found | yes; 10-09 retained as controller only, no Mind seat started |
| 44cda5 | Field Primary | Codex gpt-6-astra | 81640/258400 | done | none found | empty dir, no log |
| f5a6e9 | Psyche Primary Fable; Flow Nexus, context modules | Claude fable-5-1 | 718742 | working | successor of b27767; lineage 5ed94b>bad807>8475a9>e5a0bc>b27767>f5a6e9 | yes; published e1e8d1 "order of checks at Deliver", wake-module fold next |
| 0c85a3 | Mind Primary Astra; Curriculum separation, Nexus registry | Codex gpt-6-astra | 204395/258400 | done | successor of f768df | yes; 41fa34 found first anatomy book lacked distillation section; second edition delegated |
| ebbe30 | Psyche Primary Fable; Spirit seat, basic vision distillation | Claude fable-5-1 | 322452 | idle | peer of f5a6e9, last request ~14.7 h ago; looks superseded in practice | yes; "Field 42265e repaired tree and index... committing lane with plain git" |
| 9fcf81 | Psyche Quaternary | Claude haiku-5-5 | 66846 | done | none found | no dir |
| bc914f | Psyche Quaternary | Claude haiku-5-5 | 63961 | done | duplicate of 9fcf81 (same layer, model, start time) | no dir |
| 445410 | Psyche Secondary (this flow) | Claude opus-5-5 | 419612 | working | none | yes; 10-10 timer removed, refresh order relayed, audit dispatched |
| 73ada7 | Psyche Nexus Secondary; message design | Claude opus-5-5 | 577027 | working | none | yes; 10-10 Message design d9703b landed, Unknown.Key removed |
| d5df1d | Psyche Ethos Primary | Claude fable-5-1 | 315781 | done (hm-list); Herdr says working | none | yes; 10-10 records published to main as e81260 |
| 1d0733 | Psyche Ethos Secondary; ethos | Claude opus-5-5 | 375605 | working | successor of dcd651; peer of d5df1d | yes; living ordered refresh of all Claude flows, handovers for 1d0733 and d5df1d requested |
| 9fed42 | Psyche Flow Secondary | Claude opus-5-5 | 429178 | working | none | yes; 73ada7 removed Unknown.Key, fold pending at f5a6e9 |
| 8475a9 | Psyche Fable designer (salience of standing books) | Claude fable (no snapshot row) | none | STALE | succeeded by e5a0bc per index | yes; handover.md, summary.md; log 10-06, last: book replacement stack not Fable's concern |
| bad807 | Psyche Primary Fable (context modules) | Claude fable (no snapshot row) | none | STALE | succeeded by 8475a9 | yes; log 10-04, last: Chronos test failed to compile at daemon.rs:69,74 |

## Claude flows to refresh

Rule: no further work at 200000 observed tokens or more. Claude windows are not in the snapshot, so only the 200k rule is applied.
Over the line: f5a6e9 (718k), 73ada7 (577k), 9fed42 (429k), 445410 (420k), 1d0733 (376k), ebbe30 (322k, idle), d5df1d (316k).
Under it: 8f0f57, 02dda6, 9fcf81, bc914f (all done, Sonnet/Haiku, 64k to 140k).
Codex over 200k or 30% of window (not asked, noted): 0c85a3 (204k, 79%), 41fa34 (45%), 42265e (44%), 918df4 (39%), 44cda5 (32%).

## Retire candidates

- bc914f: same layer, model and start time as 9fcf81, both done, no flow dir, no log. Duplicate.
- 9fcf81, 8f0f57, 02dda6, 4ddfe1: done, no log and no directory (02dda6 has empty notion/vision); no work recorded. Abandoned unless the living holds a role for them.
- 918df4, 4371ed, 44cda5: done, empty flow directory, no log; no recorded work.
- ebbe30: idle for ~14.7 h at 322k tokens; f5a6e9 is the active Psyche Primary and its log still addresses ebbe30 as the Spirit seat, so confirm its role before retiring.
- 6aa08d: kept as controller per its own log; not a candidate.

## STALE entries

- 8475a9 and bad807: hm-list shows STALE. Neither appears in `herdr agent list` or `herdr pane list` (no pane, no agent name), and neither has a row in the usage snapshot. Both have flow directories; both are succeeded (bad807 by 8475a9, 8475a9 by e5a0bc). Their logs end 10-04 (bad807) and 10-06 (8475a9). The panes are gone; the registry entries remain. This is the observed state; why the route stayed registered is not established.
- Run `hm-retire` for each only on the living's word (this audit did not).
