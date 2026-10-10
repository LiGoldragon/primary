# Field Low roster and closure ledger — 2026-09-20

## Authority and boundary

Field Low `2fe3f1` owns one-at-a-time Field lifecycle coordination. The current
native is `01a0c019-fedc-7ad3-abfe-c3f2fe3f13f5`, bound to Herdr
`messaging-build/wZ:p2/term_65bee70e7730341` as `field-terra`. The binding was
repaired in place; it is not a new Flow. No cluster network mutation occurred.

## Current Field refresh queue

| Order | Flow | Seat | Native / pane | Profile | Context | State |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `2fe3f1` | Field Low coordinator | `01a0c019-fedc-7ad3-abfe-c3f2fe3f13f5` / `wZ:p2` | Terra / medium | 61% | Refresh next; predecessor stays crossover until successor acceptance. The present approved Terra profile is fresh-only and cannot safely express this successor. |
| 2 | `c88918` | Field Ultra Low | `01a0c00e-605e-7f23-91db-814c8891898f` / `wY:p1` | Luna / medium | 70% | Refresh candidate. |
| 3 | `9ddcbc` | Field Medium | `01a0c051-d38e-7d92-a79e-c609ddcbc64b` / `w0:p2` | Sol / medium | 68% | Refresh candidate. |
| 4 | `1cb440` | Field High | `01a0bb1c-5082-7593-8f81-71e1cb4409ef` / `wJ:p1` | Astra / medium | 45% | Refresh candidate. |
| 5 | `0625c3` | Psyche Low renderer | `0625c31b-798d-44f7-a116-44a7966fe618` / `wS:p1` | Sonnet / medium | 60% | Refresh candidate; HM rebind remains required. |

The queue is ordered by the living: Field Low first, then Field Ultra Low,
Field Medium, Field High, then Psyche Low. Starts, takes, refreshes, and reaps
are sequential; no batch controller is authorized.

## Proven pane-only closures

| Pane | Evidence | Disposition |
| --- | --- | --- |
| `wD:p1` | `zsh` PID `4105305` only; closed `b81560` native had no active job; no matching lock; active Psyche Medium `b80e55` continued at `wD:p5`. | Closed. `b81560` Flow directory, HM record, transcript, and no-resume boundary retained. |
| `wD:p2` | `zsh` PID `817153` only; native `1b851735-82cd-41ed-ab5b-28bd23dc19ed` exited; two resume attempts were refused; no HM row; retained continuity `c8d79f -> f38926 -> 1b8ac0`. | Closed; all Flow directories and transcripts retained. |
| `wP:p1` | `zsh` PID `1583174` only; interrupted remote session `01a0bf97-8e37-73d1-8733-e5af5d5d9b97`; no HM Flow claim or matching lock; retained active Field-Sol successor `395aed` at `wQ:p1`. | Closed; no Flow or HM record removed. |

## Roster blockers

- Mind Medium is absent. Its Sol model/profile must be validated through the
  current typed profile authority, not a validator bypass.
- Psyche Ultra has no evidenced Haiku profile, native identity, or acceptance.
- Mind Low `e798f3` and Mind Ultra `23d977` retain valid launch receipts and
  acceptance. Their exact liveness replies arrived at about 22:32 UTC after
  roughly 303 seconds to first token: `MIND_TERRA_LIVE_9DDCBC` and
  `MIND_LUNA_LIVE_9DDCBC`. They are responsive with substantial queue latency;
  do not relaunch them.
- Closed `b81560` must never be resumed.
- Psyche Medium corrected the prior helper profile. Psyche Ultra Low is a fourth
  Psyche **main** seat: `claude-haiku-4-5-20251001` at medium effort, Herdr
  name `psyche-haiku-of-b80e55`, with native `main-flow`, `refresh`, messaging,
  Herdr, file-editing, testing, and Orchestrate skills. It claims its own Flow
  ID and remembers `b80e55` at depth one. No native identity or acceptance
  exists yet. Its launch is sequenced after the Field Low refresh gate.
  Haiku's Claude-side delegation ceiling remains unruled; do not infer the
  Codex Luna analogy as authorization.
- The approved `field-terra.json` is explicitly fresh (`predecessor: null`,
  `ancestor: null`, `fresh: true`). The typed launcher requires a successor
  profile to name exact predecessor and ancestor IDs, so it cannot be used for
  a receipt-first successor of `2fe3f1` without a new typed profile authority.
