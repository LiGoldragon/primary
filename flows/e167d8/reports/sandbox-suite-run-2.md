# Flow/Message sandbox suite: run 2 (0.17)

Subflow of e167d8, 2026-09-26. The suite at `tools/flow-message-sandbox/`,
pinned to Flow 0.17.0 `908135684f27` and Message 0.17.0 `481b579fcf72`
(built on the Prometheus remote builder). Seats: Claude Haiku 4.5 and Codex
Luna (`gpt-5.6-luna`, low effort). Run 1 (0.16) is `sandbox-suite-run-1.md`.

## Results

Full run fms-9a3e2b, all 13 scenarios. Scenarios 4, 7 and 13 were run again
alone as fms-1bce62. Both teardowns came back clean on every check.

| # | Scenario | fms-9a3e2b | fms-1bce62 | Run 1 (0.16) |
|---|---|---|---|---|
| 1 | Soft to idle Haiku | pass | | pass |
| 2 | Soft to working Luna parks, lands on rest | pass | | pass |
| 3 | MiddleAbrupt to working Codex and Claude | pass | | pass |
| 4 | HardAbrupt interrupt, Codex and Claude | Codex pass, Claude **fail** | pass | Claude fail |
| 5 | Refused bodies (/compact, !, ESC, CR) | pass | | pass |
| 6 | Two senders, one pane | pass | | pass |
| 7 | Acknowledge by MessageId: Read | **fail** (cascade) | pass | pass |
| 8 | Withdraw before delivery | pass | | pass |
| 9 | Message restart with a parked letter | pass | | pass |
| 10 | Recipient pane closed: Exited, refusal names it | pass | | pass |
| 11 | Flow Start of Claude Haiku continues into its brief | **pass** | | fail |
| 12 | Flow Start of Codex | expected-fail (BindingRefused) | | expected-fail |
| 13 | 64 KiB body and psyche letter | 64 KiB pass; psyche letter **fail** (cascade) | pass | pass |

The 0.17 fixes are witnessed: Start of a Claude seat now answers Started and
continues into its brief (11). A HardAbrupt interrupted a Claude seat running a
foreground `sleep 90` in the isolated rerun (4).

## The failure in the full run

In fms-9a3e2b, scenario 4 began with the Soft setup letter
`m-18d8ebf6d76a13da009` to Haiku ("sleep 90 in the foreground"). Send graded
it `Presented`, yet the pane evidence (`evidence/s4-haiku-pane.txt`) shows the
letter still sitting in Claude's composer, typed but not submitted. The status
line was `Haiku 4.5·?`. The suite's Working check passed at that moment, so the
seat was read as working. The HardAbrupt that followed was `Parked` with
`NotRequested`, not interrupted. After that, every later letter to Haiku was
`Parked` and never landed. This covers scenario 7 (`m-18d8ec15a991e5bf011`) and
the psyche letter of 13 (`m-18d8ec888da0aff1001`). Those two failures are the
same stuck pane, not separate defects. Codex was unaffected.

This is the typed-but-not-submitted symptom that run 1 saw once in Flow's
brief continuation. It now appears on an ordinary Soft delivery, graded
`Presented`. It was seen once in two runs, so it is intermittent. The open
defect is that Flow grades Presented without witnessing the submit, and it
then leases the pane forever to a composer that never became a turn.

## Sources

- `~/.cache/flow-message-sandbox/fms-9a3e2b/` and `fms-1bce62/`
  (`results.{md,json}`, `evidence/`, `logs/`).
