# Criome policy triad schema branches

Operator implementation report for the main-based feature branches:

- `signal-criome` branch `operator/criome-policy-triad-schema`, commit `947f2719` — `signal-criome: add policy contract wire surface`
- `criome` branch `operator/criome-policy-triad-schema`, commit `03d2b32b` — `criome: evaluate schema-emitted policy contracts`

## Reasoned placement

The public criome policy-language surface belongs in the triad contract schema, not in a daemon-local handwritten language module.

`signal-criome` now owns the wire nouns and verbs:

- `Contract`, `Rule`, `PolicyMember`, `Threshold`, `TimedRule`, `TimeSwitch`
- `AgreementRule`, `AgreementFact`, `Evidence`, `SignatureEnvelope`
- `ContractDigest`, `OperationDigest`, `EvaluationDecision`
- request roots: `AdmitContract`, `LookupContract`, `EvaluateAuthorization`
- reply roots: `ContractAdmitted`, `ContractFound`, `ContractMissing`, `ContractAdmissionRejected`, `AuthorizationEvaluated`

`criome` owns the Nexus body over those generated nouns:

- content-addressed admission
- dangling-reference rejection
- duplicate quorum member rejection
- real BLS verification through the existing `MasterKey` / `VerifyBls` path
- quorum, time-window, object-member, agreement, and `EscalateToPsyche` evaluation

`meta-signal-criome` was not changed in this slice. The implemented verbs are ordinary working policy-contract operations, not owner/admin mutation yet. A future `AmendContract` / governance-control surface would belong in the meta contract.

## What changed

### `signal-criome`

`schema/lib.schema` now defines contracts as content-addressed graph nodes. Recursive composition uses `ContractDigest` references instead of inline recursive rules:

```nota
Rule [
  (SignedBy Identity)
  (All (Vector ContractDigest))
  (Any (Vector ContractDigest))
  (Threshold Threshold)
  (ActiveAfter TimedRule)
  (ActiveUntil TimedRule)
  (TimeSwitch TimeSwitch)
  (Agreement AgreementRule)
  EscalateToPsyche
]

PolicyMember [
  (KeyMember Identity)
  (ObjectMember ContractDigest)
]
```

This directly addresses the earlier designer/prototype split: the public shape is schema-emitted and digest-composable, not an inline Rust-only tree.

The generated Rust was refreshed in `src/schema/lib.rs`, with hand-written escape-hatch methods in `src/lib.rs` for:

- `ObjectDigest::from_bytes`
- `ContractDigest::from_contract`, `from_bytes`, `object_digest`
- `OperationDigest::from_bytes`, `object_digest`
- `Contract::digest`

Canonical NOTA examples and round-trip tests were extended for the new request/reply roots.

### `criome`

`src/language.rs` now evaluates `signal_criome::{Contract, Rule, Evidence, EvaluationDecision}` directly. The previous local handwritten policy types are gone from the public evaluator surface.

`src/actors/root.rs` now handles the new request roots explicitly:

- `CriomeRequest::AdmitContract`
- `CriomeRequest::LookupContract`
- `CriomeRequest::EvaluateAuthorization`

The root actor builds a `KeyRegistry` from the existing identity registry and evaluates against admitted contracts. The root request-path test proves a real registered BLS key can authorize a schema-emitted contract through the daemon actor, not only through unit tests.

`schema/criome.language.schema` is now only a placement note. It no longer sketches a drifting second copy of the public language; it points to `signal-criome` as the schema owner.

## Tests run

Local `signal-criome`:

- `SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text`
- `cargo test --features nota-text`
- `cargo fmt --check`
- `cargo clippy --all-targets --features nota-text -- -D warnings`

Local `criome`:

- `cargo test`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --features nota-text`
- `cargo clippy --all-targets --features nota-text -- -D warnings`

Remote Nix, using remote refs only:

```sh
nix build --builders '' --log-format bar-with-logs --print-out-paths --no-link \
  'git+https://github.com/LiGoldragon/signal-criome.git?ref=operator/criome-policy-triad-schema#checks.x86_64-linux.test-nota-text'

nix build --builders '' --log-format bar-with-logs --print-out-paths --no-link \
  'github:LiGoldragon/criome?ref=operator/criome-policy-triad-schema#checks.x86_64-linux.test-nota-text'
```

Results:

- `signal-criome` Nix `test-nota-text`: green, 17 tests
- `criome` Nix `test-nota-text`: green, 49 tests

No `path:` overrides were used.

## Proof coverage

The new `criome` language tests cover:

- enough distinct admitted authorities authorize
- duplicate signatures from the same identity do not satisfy a quorum
- duplicate quorum members are rejected at admission
- dangling object references are rejected at admission
- object members reference previously admitted contracts by digest
- active-after and time-switch rules
- signed agreement verdicts using real BLS
- explicit `EscalateToPsyche`
- `All` and `Any` composition over content-addressed children
- missing contracts are evaluation errors, not authorization denial
- contract digests are stable and distinguish content

The new root actor test covers:

- register a real BLS public key
- admit a `SignedBy` contract through `CriomeRequest::AdmitContract`
- sign an `OperationStatement`
- evaluate through `CriomeRequest::EvaluateAuthorization`
- receive `AuthorizationEvaluated { decision: Authorized }`

## Remaining hardening

The contract store is intentionally in-memory in this operator slice. That is enough to prove the triad schema placement, generated public surface, actor request path, and BLS-backed evaluator. It is not the final durable engine shape.

The next hardening slice is SEMA persistence:

- add contract storage tables keyed by `ContractDigest`
- persist admitted contract DAG nodes
- restore policy contracts across daemon restart
- make `LookupContract` / `EvaluateAuthorization` read from durable SEMA state

After that, the meta-policy surface can decide whether `DefineContract` / `AmendContract` belongs in `meta-signal-criome`.
