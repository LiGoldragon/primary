# 421 — Mentci component PoC feedback

## Scope

Reviewed Designer reports:

- `reports/designer/686-mentci-poc-furthering/3-poc.md`
- `reports/designer/687-mentci-full-component/3-component.md`

Reviewed PoC files under `/tmp/mentci-poc`:

- `signal-mentci/schema/lib.schema`
- `meta-signal-mentci/schema/lib.schema`
- `mentci/schema/nexus.schema`
- `mentci/schema/sema.schema`
- `crates/mentci-poc-lib/src/approval.rs`
- `crates/mentci-poc-lib/src/signer.rs`
- `crates/mentci-poc-lib/src/protocol.rs`
- `crates/mentci-cli/src/command.rs`

Verified:

- `cargo test --offline` in `/tmp/mentci-poc`: 12 tests passed. The daemon test target emits two pre-existing dead-code warnings for `connection_point`.
- `cargo run --quiet --offline --manifest-path /tmp/mentci-poc/schema-validate/Cargo.toml`: Nexus and SEMA schemas lower.
- `cargo run --quiet --offline --manifest-path /tmp/mentci-poc/meta-signal-mentci/validate/Cargo.toml`: meta-signal-mentci lowers and assertions pass.

## Direct Answer On Q2

The word **free-text** is the wrong frame for the real system.

In the PoC it means one specific Rust implementation detail: `ApprovalDecision::Answer(ApprovalAnswer)` holds an arbitrary `String`, the tab-delimited codec serializes it through `Line::free_text`, and the fake signer renders it into a string preimage:

```text
VERDICT/<question>/<decision-or-answer-text>
```

That is useful only as a pressure-test for the seam. It should not become the production verdict contract.

For the real Mentci/criome path, there are three different layers:

1. Human-editable surface: can be NOTA text in the CLI/TUI/editor.
2. Wire/storage object: must be a schema-defined typed object, emitted as rkyv and optionally projected as NOTA.
3. Signed preimage: must be canonical bytes or a digest of that typed object, not an arbitrary string.

So the better term is **authored typed answer object**, not free text. If the psyche edits an answer, Mentci should produce a typed `AnswerProposal` or revised typed request object. Then the verdict is still closed over that object:

```text
ApproveProposal | RejectProposal | Defer
```

My recommendation: do not promote `PendingAnswer` into `ApprovalDecision`. Delete the `Answer(PendingAnswer)` direction from the real contract. Let authoring/editing create a new typed proposal object; let the signed verdict approve or reject the proposal's content-addressed typed preimage.

## Review

The full component shape is right. `mentci` as daemon repo plus `signal-mentci` and `meta-signal-mentci` as the two contracts matches Spirit `7x5z`, `7sx6`, `26e7`, and `f8ds`. Nexus and SEMA schemas belong inside the daemon repo, not in the contracts. Designer's 687 framing is aligned with that.

The SEMA idea is the load-bearing win: Mentci's canonical UI state is SEMA state. A UI changes because SEMA changes; clients render the subscribed state. That cleanly implements the psyche's statement that the daemon owns state.

The PoC proves the right behavior at the right level: a client subscribes over a real Unix socket, an agent pushes a question, daemon state changes, subscriber receives the pushed update, and an answer updates subscribers. This is the correct push-not-poll shape.

## Issues To Fix Before Main

### 1. The `Answer` variant must not leak into production

`/tmp/mentci-poc/crates/mentci-poc-lib/src/approval.rs` still has:

```rust
ApprovalDecision::Answer(ApprovalAnswer)
```

That was acceptable as a PoC seam. In the production contract, the verdict should be closed. User-authored content belongs in a typed proposal/update object, not in the verdict enum.

Concrete production shape:

```nota
ApprovalDecision [
  ApproveSuggestedAnswer
  Reject
  Defer
]

;; if editing is needed:
AnswerProposal {
  question QuestionIdentifier
  body <typed NOTA/rkyv answer object>
}
```

Then criome signs the digest of the proposal plus the closed decision.

### 2. Question identifiers should be daemon-minted unless they are content-addressed origins

`signal-mentci` currently has `PresentQuestion ApprovalQuestion`, and `ApprovalQuestion` contains `identifier QuestionIdentifier`. That lets the pusher supply the identity of the daemon's pending-question record.

The safer production surface is:

```nota
PresentQuestion QuestionProposal
QuestionPresented { question QuestionIdentifier ... }
```

The daemon mints `QuestionIdentifier`, or derives it from a content-addressed origin object. External agents should not choose local SEMA row identity.

Open question: should a criome escalation use its content-addressed origin as the stable question identity, or should Mentci always mint a local question token and store the origin separately?

### 3. Subscription tokens should be daemon-minted tokens, not subscriber names

`InterfaceObservationToken { subscriber SubscriberName }` is weak if one client opens multiple subscriptions, reconnects, or changes interest. The production token should be a daemon-minted `SubscriptionToken`, with `SubscriberName` only metadata.

This matches the `mentci-lib` work already landed in report 420: subscriptions have identifiers separate from clients.

### 4. Full-state fan-out may be too broad for every client

`ObserveInterfaceState` currently implies a full `InterfaceState` stream. That is fine for a TUI/editor, but a status bar or popup may not be allowed to see full question context.

The production contract should probably add an `InterfaceInterest` or `InterfaceProjection`:

```nota
InterfaceStateObservation {
  subscriber SubscriberName
  interest InterfaceInterest
}

InterfaceInterest [
  FullInterfaceState
  StatusOnly
  Notifications
  PendingQuestions
]
```

This keeps the push model while avoiding unnecessary context exposure.

### 5. Timestamps need a clear role

`QuestionPresented { accepted_at TimestampNanos }` and `RevisionStamp { at TimestampNanos }` look like ordinary daemon time. If they are only local UI metadata, that is fine but should be named as local receipt time and not used for authorization. If they influence criome decisions, they need the attested-moment model.

Given Spirit `9s52`, this should stay local to the per-Unix-user Mentci daemon unless a cross-machine agreement object is being signed.

## Decisions Already Settled

Q1 is effectively answered by Spirit `9s52`: criome is per-Unix-user. A privileged system criome exists only for host-scoped system services under a service user; it is not a shared multi-user daemon with in-process user lanes.

Q3 should stay plain monotonic for Mentci's local UI revision. A local daemon's render revision is not a quorum-signed object. If the revision becomes cross-machine, signed, or agreement-bearing, then it graduates to an attested moment. Until then, a counter is the right object.

## Proposed Landing Order

1. Create or migrate `signal-standard` first enough to provide `ComponentKind` and `StandardSocket`.
2. Migrate `signal-criome` to current strict positional syntax so cross-imports stop being local duplicates.
3. Create `signal-mentci`, `meta-signal-mentci`, and `mentci` repos.
4. Land `signal-mentci` without the `Answer(PendingAnswer)` verdict path.
5. Change `PresentQuestion` to daemon-minted question identity.
6. Change subscription tokens to daemon-minted tokens and add an observation-interest shape if status/popup/email clients should not receive full state.
7. Build the daemon over `mentci-lib`'s state model, replacing the PoC tab codec with the real signal frame/rkyv path.

## Questions For The Psyche

1. Should Mentci always mint a local `QuestionIdentifier`, or should criome escalations use their content-addressed criome origin as the question identity?
2. Should status-bar, popup, and email clients receive the full `InterfaceState`, or should the contract include filtered interests from the start?
3. When the user edits a suggested answer, should that produce a new typed proposal object which is then approved/rejected, rather than putting authored content inside `ApprovalDecision`?
