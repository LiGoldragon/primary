# Calling Claude from code

Proposed new module: `knowledge:claude-code-calls:0` in Mind belief.
Status: proposal only; no belief landed. All 180 unique paid jobs are complete.
Task accuracy remains unestablished pending Fable's rulings.

## Proposed module

Description: Claude calls from Rust: typed Emission, measured trial profiles and
costs, strict answer decoding, and the limits of structural validation.

The Rust trial has two operations: belief admission into a disposable snapshot
and a queue recommendation that launches no flow. Each emits a typed ModelCall,
receives the processor observation, and decodes it into the task's declared
answer type before using it. The trial proves this domain-core/process boundary;
full Nexus socket serving, binary Signal transport, generated Ethos contracts,
actors and persistent Memory serving remain unimplemented.

The caller supplies the whole question and evidence. The trial gives the model
no facility to open referenced files: a path in a prompt is text, not contents.
The observed processor makes one Messages request per invocation without tools,
caching, redirects or retries. The Rust caller receives its result, never the
API key. Failed or uncertain calls remain evidence for owner review.

The measured profiles were `claude-haiku-5-5` with thinking disabled and a 4096
output-token cap; `claude-sonnet-5-5` with low-effort between-tools thinking and
the same cap; and `claude-opus-5-5` with medium-effort adaptive thinking, display
omitted and a 1024 total output-token cap including thinking. These are trial
configurations, not general Messages API limits. Compare profiles, not model
names alone. Supported models, rates and bounds belong to configuration.

Answer checking separates declared-shape decoding from evidence constraints.
Unknown or duplicate fields, trailing values, wrong-task answers, absent line
or module references and required empty wording are unsuccessful outcomes. A
real line identifier can still identify the wrong proposition: structural
validity and semantic correctness are distinct.

Provider failure, malformed answer, explicit model refusal and incomplete
generation are distinct outcomes. Accounting settlement alone does not establish
generation completion; the task must check the native stop reason. All 180 paid
responses in this trial ended with `end_turn`. Evidence-insufficiency refusals
were JSON task responses, not native provider or content-policy refusals.

Each profile completed thirty belief and thirty queue cases, with one paid call
per slot and no paid retry. The decoder results were:

| Profile/task | Schema decoded (refusals included) | Constraint failures | Judgments | Evidence refusals | Shape failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Haiku / belief | 29/30 | 8 | 21 | 0 | 1 |
| Haiku / queue | 30/30 | 0 | 23 | 7 | 0 |
| Sonnet / belief | 28/30 | 0 | 20 | 8 | 2 |
| Sonnet / queue | 29/30 | 0 | 29 | 0 | 1 |
| Opus / belief | 30/30 | 0 | 30 | 0 | 0 |
| Opus / queue | 30/30 | 0 | 27 | 3 | 0 |

A refusal in the wrong JSON nesting position is a shape failure. Eight Haiku
belief answers decoded to the declared shape but failed evidence constraints.
No failed answer was repaired or automatically repeated.

| Profile/task | Mean raw estimate USD/call | Mean retained USD/call | Median boundary seconds |
| --- | ---: | ---: | ---: |
| Haiku / belief | 0.00075201 | 0.00466331 | 2.1475 |
| Haiku / queue | 0.00017373 | 0.00097612 | 2.9400 |
| Sonnet / belief | 0.01515913 | 0.01515913 | 3.3285 |
| Sonnet / queue | 0.00323320 | 0.00323320 | 4.2700 |
| Opus / belief | 0.03434360 | 0.03434360 | 6.4745 |
| Opus / queue | 0.01260507 | 0.01260507 | 8.1935 |

Total raw usage estimate was 1.9880020 USD; conservative retained commitment was
2.129413125 USD. These are different accounting quantities, neither an invoice
nor proof of balance. Boundary time includes the processor, reservation and
settlement, not inference alone. One Haiku queue call took 142.382 seconds;
its cause is unknown. Opus output usage includes its thinking profile.

Opus initially completed 52 paid jobs. Eight long belief questions failed the
local conservative admission bound before any provider call. The bound summed
prompt UTF-8 bytes, system UTF-8 bytes and a framing allowance against 20000;
it was not an actual token count. A reviewed exact-prompt-hash one-shot extension
raised that bound to 60000 for those eight prompts, retaining the 1024 output
cap. All eight then completed once. The local no-call refusals remain separately
recorded; they are not paid retries or failed provider requests.

The belief construction was eight admitted, eight repeats, seven collides and
seven elsewhere, made from real historical paragraphs and snapshots. Repeated
and wrong-placement cases reuse admission paragraphs; collision cases share four
change families. The cases are correlated and their labels provisional. Adding
versus replacing a line, authorization, retrieval sufficiency and policy ordering
can change the right judgment. Historical class agreement was Haiku 12/30,
Sonnet 16/30 and Opus 28/30; class plus exact-reference agreement was 10/30,
13/30 and 24/30. These are construction comparisons, not established accuracy.
A different line in the same paragraph is not necessarily a semantic error.

The calibration returned a valid repeat referencing a real but unrelated line,
although the submitted paragraph historically landed. This directly demonstrates
why valid decoding and reference existence cannot alone authorize a live write.
Some Sonnet refusals identify missing comparison content: module names alone
provide no such content, particularly for empty new-module snapshots.

The thirty queue cases are real captured messages with unknown recipient live
state and no final labels. Sender and priority were retained in provenance but
not supplied as model-facing fields. Haiku returned 21 KeepQueued, 2 StartFresh
and 7 evidence refusals; Sonnet 28 KeepQueued, 1 StartFresh and 1 malformed
refusal; Opus 26 KeepQueued, 1 StartFresh and 3 evidence refusals. Agreement or
successful decoding on these cases establishes no queue-policy accuracy.

## Evidence and companion proposal, outside the proposed module

- Final report: `flows/250509/typed-call-report.md`; all sixty case rows include
  the three model outcomes, with provenance and limitations.
- Aggregation: `flows/250509/trial/results/final-summary.json`, including 180
  unique paid job references and eight prior local no-call refusals.
- Rust trial: `flows/250509/trial/`, Rust revision `f387b046c`; builder default
  gate passed with 22 dry Rust tests. Final driver has twelve synthetic tests.
  Tests are implementer-authored, not independent tester certification.
- Research owns the companion worker draft at
  `flows/082e0f/knowledge-claude-api-draft.md`, still due at this finalization.
  That draft is the home for verified secret/ledger/adapter invocation guidance;
  this proposal records Rust trial learning and adds no competing worker manual.
- Research retains the sole authoritative spend ledger and raw paid receipts.
  The final accepted scoped worker archive is
  `04731745b5875cd19ef52ce107883845df63cccfbbacd55b920c99b8492d9ea7`.
- Fable's post-run belief and queue rulings remain requested. No additional paid
  calls are required, and neither authored belief nor live queues were changed.
