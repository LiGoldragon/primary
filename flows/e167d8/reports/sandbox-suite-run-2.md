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

Corrected by 93ba9f, 2026-09-26. The cause first written here — "Flow grades
Presented without witnessing the submit, and it then leases the pane forever
to a composer that never became a turn" — is wrong. The letter *was*
submitted. The interrupt put it back.

In fms-9a3e2b, scenario 4 began with the Soft setup letter
`m-18d8ebf6d76a13da009` to Haiku ("sleep 90 in the foreground"). Send graded
it `Presented`, and that grade was right: Claude took the letter as a turn and
started the sleep, which is why the Working check passed. The HardAbrupt that
followed pressed `esc esc`. Pressed before the turn's first response, that
cancels the turn and **restores its prompt — the letter — into Claude's
composer**. Flow then read the pane again, found the composer occupied, and
refused the HardAbrupt `ComposerOccupied`, recorded as `Parked` with
`NotRequested`. The restored letter was never taken out, so it held the pane
against every later letter: scenario 7 (`m-18d8ec15a991e5bf011`) and the
psyche letter of 13 (`m-18d8ec888da0aff1001`) are the same stuck pane, not
separate defects. Codex was unaffected.

The pane evidence `evidence/s4-haiku-pane.txt` is a snapshot taken at the end
of the scenario, after the interrupt. The letter it shows in the composer is
the restored one, not one that was never submitted; the snapshot cannot
distinguish the two, and it was read here as the latter.

93ba9f reproduced the restoration deliberately against a real Claude Haiku 4.5
seat (run fms-c42635): an `agent prompt` followed 1.2 s later by `esc esc` left
`❯ Soft.{ m-... }` in the composer, and one `ctrl+c` emptied it.

Flow 0.17.1 `ac216c89` takes a restored letter back and is proven in
`flows/93ba9f/reports/flow-0171-proof.md`.

## Sources

- `~/.cache/flow-message-sandbox/fms-9a3e2b/` and `fms-1bce62/`
  (`results.{md,json}`, `evidence/`, `logs/`).
