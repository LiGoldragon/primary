# Spirit Guardian Live Scenario Suite

Operator report for the guardian design/implementation/test pass completed on
2026-06-11.

## Summary

Implemented and pushed a real guardian scenario suite that exercises Spirit
through the actual agent component and DeepSeek Flash, with a sandbox Spirit
store and fictitious records.

Commits landed:

- agent `a8afaaba` — `agent: require one NOTA root for model output`
- spirit `a814a282` — `spirit: test live guardian through agent`

## Design

The test path is intentionally close to production:

- Spirit opens a temporary SEMA store.
- The test seeds realistic intent records into that store.
- The test starts an in-process Unix-socket agent server.
- That server uses the real `agent::AgentEngine`.
- Agent resolves the DeepSeek key through `SecretSource::gopass("platform.deepseek.com/api-key")`.
- Agent calls DeepSeek at `https://api.deepseek.com/v1` with model `deepseek-v4-flash`.
- Spirit sends normal signal-agent frames to that socket through `AgentGuardian`.
- DeepSeek returns a NOTA verdict.
- Spirit parses the verdict as generated schema type and applies the accept/reject result.

The live test is ignored by default because it spends live provider calls:

`cargo test --features agent-guardian --test guardian_live_scenarios -- --ignored --nocapture`

## Implementation

Agent now rejects NOTA output unless the completion parses as exactly one NOTA
root object. This fixed a real issue found during the first live guardian run:
`deepseek-v4-flash` could return empty final content while spending tokens in
reasoning content, and the previous generic NOTA parse accepted an empty
document.

Spirit now keeps the long guardian prompt text in `src/guardian_prompt.rs`
instead of bloating `src/guardian.rs`. The module owns:

- write-operation guardian prompt assembly
- referent-registration guardian prompt assembly
- retry prompt text
- operation-to-text rendering for guardian candidates
- temperature-zero and NOTA-output prompt options

Spirit’s guardian prompt now explicitly tells the model that `Justification` is
source evidence for admission, not a second intent arrow. That was necessary
after rebasing onto main’s current `RecordRequest` / `Proposal` shape: the live
model otherwise rejected a valid proposal as `Compound`.

## Scenario Coverage

The live DeepSeek scenario seeds these records:

- NOTA uses bracket forms; quotation marks are not valid NOTA string syntax.
- Spirit entries express one forward act, principle, constraint, or decision at
  a time.
- Agent provider secrets are resolved by the agent daemon from configured
  secret-source backends.
- Referents must be registered before records may attach them to entries.

It then checks:

- accept: clear guardian testing intent
- accept: clear agent provider test intent
- reject `Contradiction`: NOTA quotation-mark canonicalization conflict
- reject `Compound`: agent key-resolution plus Spirit deployment bundled into
  one entry
- reject `NonIntent`: uncertainty/status phrased as an intent entry

The live run passed with `deepseek-v4-flash` after increasing the guardian
completion budget to 1024 tokens and clarifying the justification semantics.

## Verification

Green checks run in Spirit:

- `cargo test --features agent-guardian`
- `cargo test referent -- --nocapture`
- `cargo clippy --features agent-guardian -- -D warnings`
- `cargo test --features agent-guardian --test guardian_live_scenarios -- --ignored --nocapture`

Green checks run in Agent:

- `cargo test`
- `cargo clippy --features live-provider -- -D warnings`

## Readiness

The tested path can accept and reject write proposals through the real agent and
DeepSeek Flash. On current main, the broader guardian architecture also covers
record, propose, clarify, supersede, retire/remove/change flows and referent
registration in the deterministic fake-agent tests.

This was not a deployment pass. The code is pushed and tested, but production
activation should still be done by the deployment lane with the current CriomOS
service configuration and startup archive path.
