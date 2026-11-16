# Calling Claude from code

Proposed new module: `knowledge:claude-code-calls:0` in Mind belief.
Status: proposal, not landed. Measurements below are preliminary; the comparison
final three-model table formatting and Fable's rulings remain pending. The eight-prompt Opus extension has completed; final-summary.json holds all 180 results.

## Proposed module

Description: Claude model calls from code: the typed boundary, supported trial
models, measured call costs and observed failure cases.

A model call is a typed Emission. Its operation supplies the question and its
evidence; the translator calls the provider; its observation is decoded into a
declared answer type before the operation uses it.

The reviewed trial processor has completed calls on `claude-haiku-5-5`,
`claude-sonnet-5-5` and `claude-opus-5-5`.
Supported models and rates belong to the reviewed processor's configuration.

The processor makes one Messages request per invocation, without tools, caching,
redirects or retries. The measured Haiku and Sonnet profiles cap output at 4096
and use disabled thinking and low-effort between-tools thinking respectively.
The initial Opus profile uses medium-effort adaptive thinking with its display
omitted and caps total generated output, thinking included, at 1024. These are
reviewed processor profiles, not general limits of the Messages API.

The caller supplies the whole question and evidence; this processor gives the
model no facility to open a referenced file. An absolute path in a prompt is
text rather than file contents.

The credential producer pipes directly to the provider client's supported
header-stdin interface. The Rust caller receives the processor's result, never
the API key. Failed or uncertain calls are preserved for owner review rather
than automatically repeated.

The output passes two checks: decoding the declared answer type, then validating
references and nonempty fields against the supplied evidence. Unknown fields,
duplicate fields, trailing values, missing referenced lines and wrong-task
answers are unsuccessful outcomes. A valid existing reference can still be
semantically wrong: decoding establishes shape, not judgment truth.

Provider failure, malformed answer, explicit model refusal and incomplete
generation are distinct outcomes. A successful accounting settlement alone
does not establish generation completion: inspect the native `stop_reason` and
require the completion state the task accepts.

One completed Haiku admission call took 1.957 seconds for the processor boundary,
used 2249 input and 50 output tokens, and had a raw usage estimate of
0.0002499 USD. Its conservative retained ledger charge was 0.001530625 USD.
These are different accounting quantities. Neither is an invoice or proof of
account balance. One call does not establish a typical price or latency.

The completed Haiku/Sonnet comparison has thirty belief and thirty queue cases
per model, with 120 unique paid receipts including that first call. Total raw
usage estimate is 0.5795420 USD and total retained commitment 0.720953125 USD.
Mean raw estimated cost per belief call is 0.00075201 USD for Haiku and
0.01515913 USD for Sonnet; median boundary time is 2.148 and 3.329 seconds.
Per queue call the means are 0.00017373 and 0.00323320 USD; medians are 2.940
and 4.270 seconds. The one Haiku queue outlier took 142.382 seconds; its cause
was not established.

On these thirty belief cases, Haiku produced 29 declared-shape answers, eight
of which failed a reference/nonempty check. Sonnet produced 28 declared-shape
answers: twenty judgments and eight evidence-insufficiency refusals. On the
queue cases, Haiku produced thirty declared-shape answers including seven
refusals; Sonnet produced twenty-nine and one malformed refusal. An explicit
refusal in the wrong nesting position is a shape failure rather than an
accepted answer. No failed answer was repaired or automatically repeated.

The initial Opus stage completed 52 paid responses, all ending with `end_turn`,
for 0.807456 USD estimated and retained. Eight long belief questions were refused
locally without calling the provider. Opus used a conservative admission bound
of prompt UTF-8 bytes plus system UTF-8 bytes plus a configured framing allowance;
that bound is not a token estimate. A prompt can fit an observed token count
from another model while failing this processor's local byte-bound contract.

On the actually shared twenty-two belief cases, valid judgments numbered fifteen
for Haiku, fifteen for Sonnet and twenty-two for Opus. Historical construction
class agreement was ten, twelve and twenty; adding exact-reference agreement
made it nine, eleven and eighteen. Those are small, correlated-case construction
comparisons, not accuracy estimates: Fable has not ruled on the labels, and the
operation's add/replace intent and comparison retrieval were incomplete.

That call decoded as a repeat with a real line identifier, but the identified
line concerned a different proposition. Historical evidence says the submitted
line landed. The semantic judgment therefore needs review independently of
the successful typed integration. The original change operation and its
authorization belong in the question: a landed replacement can still collide
when presented as an additional line against the old snapshot.

## Evidence, outside the proposed module

- Trial report: `flows/250509/typed-call-report.md`.
- Rust source and case data: `flows/250509/trial/`, revision `f387b046c`.
- Builder default gate: `/tmp/typed-call-250509-gate-final.log`; 22 dry tests pass,
  plus Cargo.nix, crate-version and crate-feature checks. Tests are authored by
  the implementer, not an independent test flow.
- Call receipt: `/tmp/typed-call-250509-calibration-observation.json`.
- Paid job: `raw-general-082e0f-5dcdc8f6abe8492b9da002df17ca77dd`, retained by
  Research under its authoritative paid-jobs directory and ledger.
- The domain-core trial has not implemented full Nexus socket serving,
  binary Signal transport, generated Ethos contracts or a production store.
  This proposal records what the code-call experiment proves, not deployment.
