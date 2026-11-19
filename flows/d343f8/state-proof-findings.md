# Claude called from code: system-state proof

**The process boundary worked on Haiku, Sonnet and Opus: three calls, three
complete typed answers, no retry. All three answered `Unknown` for both overall
flow load and overall energy use.** The facts lacked a desired flow count and a
policy for combining the providers' different pace standings. This proves the
call and decoding path, not a correct automatic decision about the system.

## What the program did

`flows/d343f8/state-proof/proof.py` gathered one timestamped snapshot, normalized
its observations, emitted three typed `Emission` values through the unchanged
API adapter, and checked the returned JSON against the declared answer shape.
The same frozen facts and question went to each model. It changed no flow,
queue, host configuration or belief. This is a Python process-boundary proof,
not a fully served Nexus with generated Ethos, actors and persistent Memory.

At **19 November 2026, 06:28:47 UTC**, the snapshot contained:

| Source | Observed fact |
| --- | --- |
| Herdr | 26 flow rows: 4 UI-working, 22 UI-done; UI state is not task health |
| Flow queues | 46 pending messages across 20 queue addresses; message text withheld |
| Claude Energy | Week 66% used versus 73% expected; FableWeek 34% versus 73%; both Under pace |
| Codex Energy | Week 5% used versus 3% expected; Over pace |
| Builder | 32 logical CPUs; 1/5/15-minute load averages 0.05/0.02/0.00; one runnable task |

Builder load averages measure runnable-work pressure, not CPU utilization.
Claude's observation was current at capture; Codex's cached weekly observation
was 1,121 seconds old. The proof declared a 3,600-second Energy evidence-age
limit and a separate 900-second snapshot-age limit. Those are configurable
acceptance bounds, not a claim that cached readings are live measurements.
Unknown or unavailable sources have explicit representations.

The typed result is either an answer with `flow_load`, `energy_use` and a reason,
or a task refusal with a reason. Flow load chooses TooMany, Appropriate, TooFew
or Unknown; energy use chooses TooHigh, Appropriate, TooLow or Unknown.
Malformed JSON, duplicate/unknown fields, invalid enum values, native refusal,
truncation and transport/accounting uncertainty have separate outcomes.

## What happened and what it cost

Research admitted exactly three once-only slots under a $10 ceiling. The full
worst-case reservations totaled $2.904192. The run completed at 06:32:11 UTC.

| Model profile | Input / output tokens | Boundary seconds | Usage-priced estimate USD | Retained commitment USD |
| --- | ---: | ---: | ---: | ---: |
| Haiku 5.5, thinking disabled | 6,307 / 332 | 6 | 0.0007967 | 0.004771875 |
| Sonnet 5.5, low-effort thinking | 6,307 / 336 | 8 | 0.015974 | 0.015974 |
| Opus 5.5, medium adaptive thinking | 6,308 / 775 | 11 | 0.040732 | 0.040732 |
| **Total** | **18,922 / 1,443** | **25** | **0.0575027** | **0.061477875** |

Output counts include charged thinking where applicable. Boundary time includes
adapter and accounting work, not inference alone. Estimates are calculated from
reported usage; retained commitments are the ledger's conservative quantities.
Neither is an invoice or proof of which credit grant paid a request. Funding
was admitted on the relayed monthly-credit basis, not an independently read
Console balance.

All three native stop reasons were `end_turn`; all three receipts settled.
Declared-shape decoding was **3/3**. Each answer's two judgments were Unknown,
with evidence-based explanations. There were no paid malformed answers,
refusals or uncertain outcomes in this proof. Thirty-two unpaid fixtures cover
those branches, drift, freshness, budget refusal, durable intent and no replay;
they do not measure real provider failure rates. Three correlated calls establish
neither model accuracy nor variance.

## What the key handling took

The proof passes only model ID, a one-call cap and a prompt-file path to the
configured adapter. It does not request or receive the API key.

The adapter starts the configured GoPass producer in its bounded helper sandbox,
checks bounded stdout, builds the authentication header in private process
memory, and feeds curl's supported header-stdin interface. Curl runs with its
configuration file disabled and an empty environment. Credential bytes travel
through that private producer/adapter/transport path; they are absent from model
context, prompt files, arguments, recorded observations and the calling flow.
Transient process memory necessarily carries them during authentication.

No new credential installation or persistent key copy was needed. The existing
adapter was reused unchanged. The proof pinned its complete execution/accounting
closure, including imported worker code, static policy/evidence, interpreter,
external executable identities and CA bundle. The worker reserved before the
helper ran; the controller durably recorded run and slot intent before each
invocation. Uncertain execution would stop with the full bound held, rather
than create another job to retry it.

## What to keep and what to improve

- Typed facts and a strict answer contract work across the three measured
  profiles. Valid decoding is separate from semantic usefulness.
- Keep Unknown as an explicit judgment. Provide the desired concurrency/workload
  baseline and separate per-provider pace policy before asking for actionable
  high/low decisions. One combined energy label hid opposing provider standings.
- Keep source age, units and missing evidence in the packet. A resting UI row is
  not a failed task, an absent UI row is not proof of an invalid queue, and load
  average is not CPU percentage.
- This snapshot cost about 6,300 input tokens per call. A next, separately
  authorized experiment could compare a compact aggregate packet with this
  detailed packet and measure whether judgments retain their evidence.
- Treat the monthly allowance as capacity for useful, reviewed experiments,
  rather than a target requiring calls when no question needs answering.

An **illustrative $200 monthly allocation**, not spending authority:

| Code-call experiment | Illustrative envelope |
| --- | ---: |
| State judgments after meaningful events, with explicit operating targets | $50 |
| Belief duplicate/collision advice against human-reviewed historical outcomes | $50 |
| Test-failure and build-diagnostic classification into typed next-step proposals | $40 |
| Queue recommendations with recipient state and work context, without automatic launches | $30 |
| Missing-evidence, malformed-answer, truncation and independent-review comparisons | $30 |

Each would need its own frozen question, call count, admission and outcome
criteria. Deterministic parsing, arithmetic and established policy checks remain
ordinary code. Model calls are most useful where interpreting supplied evidence
requires judgment and the proposed decision can be checked before an effect.

## Accounting closure

Research independently reconciled exactly three reservations, admissions,
outcomes and settlements, then closed this single-run admission in commit
`c0cdc44a5`. Its read-only report is
`flows/85ab00/system-state-reconciliation.json`. The proof's retained commitment
is 0.061477875 USD; the earlier interrupted variance job remains separately
held at its full 0.10048 USD bound. No launcher remained active. This proof's
admission is consumed; it authorizes no further execution.

## Evidence

- Source, configuration, snapshot, prompts and fixture report:
  `flows/d343f8/state-proof/` (source commit `a17b2c8c8`).
- Frozen manifest SHA256:
  `0fc2bed0944deb0089d860ba5124d9e3b6f4f601b108d3a44662fce8ae7e4242`.
- Research admission `9h9b`, separate from the revoked variance campaign.
- Run report and per-slot intents/observations:
  `flows/d343f8/state-proof/results/7447ce3c-b18e-492e-b783-fe8216a37832/report.json`.
- Raw worker receipts are at each observation's `artifact_directory`, under
  `flows/082e0f/claude-api-evidence/paid-jobs/`.
- Existing worker guidance: `flows/082e0f/knowledge-claude-api-draft.md`.
  The original 180-job learning remains in
  `flows/250509/claude-code-calls-knowledge-proposal.md`; its figures exclude
  this three-call proof and the stopped variance campaign.
