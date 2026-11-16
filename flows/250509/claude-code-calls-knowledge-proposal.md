# Calling Claude from code

Proposed new module: `knowledge:claude-code-calls:0` in Mind belief.
Status: proposal, not landed. Measurements below are preliminary; the comparison
suite and Fable's rulings remain pending.

## Proposed module

Description: Claude model calls from code: the typed boundary, supported trial
models, measured call costs and observed failure cases.

A model call is a typed Emission. Its operation supplies the question and its
evidence; the translator calls the provider; its observation is decoded into a
declared answer type before the operation uses it.

The reviewed trial processor supports `claude-haiku-5-5` and
`claude-sonnet-5-5`. Opus support is not established by the completed trial.
Supported models and rates belong to the reviewed processor's configuration.

The processor currently makes one Messages request per invocation, with an
output ceiling of 4096 tokens and no tools, caching, redirects or retries.
Those are this processor's limits, not general limits of the Messages API.

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

That call decoded as a repeat with a real line identifier, but the identified
line concerned a different proposition. Historical evidence says the submitted
line landed. The semantic judgment therefore needs review independently of
the successful typed integration.

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
