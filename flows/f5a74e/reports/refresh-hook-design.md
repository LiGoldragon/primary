# Refresh hook: bounded Mind design

## Scope and evidence

This is a design contribution, not an implementation or a claim that a hook exists. The living's request is recorded verbatim at flows/f5a74e/vision/refresh-hooks.md lines 2-10. Its preface says the lost V2 receipt and unready successor are a relay claim, not independently witnessed fact (line 4). This design therefore preserves a handoff independently of the checkout but does not treat that incident as measured runtime state.

Repository revision inspected: 133c9d53aa1d83e72ae9ca1d4bd2d363fad978be. The working tree already contained two unrelated untracked launch files under flows/00f95a; this report does not use or alter them.

Measured present mechanisms:

- The installed flow and message CLIs exist, but their --help inputs reject as malformed typed queries; no message was sent or route inspected live. This is availability evidence only, not delivery or queue evidence.
- tools/main-flow-mode/reminder-hook.py lines 2-9 and 40-73 is a per-session, locked counter on UserPromptSubmit; every twentieth event adds prompt context. It has no context-window measurement, lifecycle state, message interception, handoff capture, or successor selection.
- tools/flow-cli-poc/README.md lines 1-16 and flow.py lines 8-13 and 60-75 describe a SQLite fixture POC. It accepts a keyed restart, waits for a pipe handshake, retires the prior process only after readiness, and makes duplicate request keys idempotent. The README expressly excludes production Nexus, Sema, Signal, authentication, provisioning, and durable supervision.
- The native launcher has the useful receipt-first boundary. It snapshots manifest source bytes and hashes (tools/native-seat-launch.mjs lines 159-175), writes a receipt before starting the first turn (444-452), verifies exact turn/context/skill/source hashes (231-242), and records ready only after title finalization (494-518). Its plan says provenance does not retire or deregister the predecessor (165), and its launch result says no registration or predecessor retirement occurred (456-457). A title change has an explicit restoration attempt on failure (509-513).
- The Claude equivalent rejects resending an ambiguous first prompt (tools/claude-native-seat-refresh.py lines 795-805) and labels the verified bootstrap receipt title-pending while recording no predecessor retirement or registration (876-885).
- Messaging's intended semantics distinguish hard, middle, and soft delivery and distinguish interrupt, submission, and recipient consumption (Vision/messaging.md lines 3-25). No checked-in source inspected provides a delivery-time refresh gate or successor reroute.

The raw vision permits pending subagents to finish while explicitly deferring direct subflow rerouting (flows/f5a74e/vision/refresh-hooks.md lines 6-8). That boundary controls the proposal below.

## Proposed hook contract

Introduce one future Refresh Coordinator as the owner of durable lifecycle state. It is not a hook that guesses from prompt count. A harness-specific observer supplies a measured, timestamped context observation; policy decides whether that observation crosses a configured threshold. The coordinator owns one refresh record keyed by (flow-id, predecessor-generation, refresh-epoch).

The epoch is minted once on acceptance. A repeated threshold event with the same flow/generation returns the existing record; it must never create another successor or duplicate a handoff. A later generation needs a new epoch.

Each accepted state change appends an immutable receipt and atomically advances the record revision. The coordinator compares the expected revision at every transition. A competing final-response event, threshold observer, or launch completion therefore either wins once or reads the already-won receipt. It does not infer success from a process, prompt submission, file path, or predecessor silence.

    Normal
      -- measured threshold plus accepted policy --> RefreshRequested
      -- predecessor captures final handoff --> HandoffCaptured; inbound delivery gated
      -- launch receipt written --> SuccessorPending
      -- exact native context and title receipt verified --> SuccessorReady
      -- failed or expired launch before ready --> RollbackOpen

    RollbackOpen -- predecessor still attributable --> Normal
    SuccessorReady -- explicit later routing decision --> Routed

HandoffCaptured is a durable capture of the predecessor's completed final response, its content hash, the relevant flow/generation, and capture sequence. It is not SuccessorReady. SuccessorPending is only a launch/receipt fact. SuccessorReady requires the native evidence already enforced by the launchers: exact target turn, model/effort, expanded skills, source manifest, canonical title, and successor flow identity. The launcher data above supports this readiness shape but is not a coordinator or route switch.

The observer record should keep raw measured fields separate from policy: observed context capacity/usage and source, timestamp, session/generation binding, and measurement quality. Threshold, predicted burn rate, desired handoff deadline, and refresh decision belong to coordinator policy. This prevents an estimate or stale receipt from becoming a claimed live context fact.

## Safe gate while readiness is pending

The living asks for new messages to stop going to the predecessor immediately after handoff capture. The existing receipt-first launch discipline instead keeps the predecessor attributable until successor readiness. These can fit together without silently withdrawing its route:

1. On HandoffCaptured, install a delivery gate for the exact predecessor flow-id, generation, and refresh epoch. The public route remains resolvable; the gate refuses delivery to that generation and durably appends each incoming message to the refresh inbox with its original message id, intended recipient, priority, sender, body hash/body reference, and sequence. Inbox acceptance is a receipt, not a recipient-consumption receipt.
2. A message addressed to the proposed successor before SuccessorReady is held in a target-readiness inbox. A sender gets queued-awaiting-readiness, never invented delivery success.
3. On verified readiness, the coordinator exposes held records to a routing decision. It may release them once, in original sequence per recipient/priority lane, to the verified successor only if the release rule is authorized. Original message id is the deduplication key, so retry after timeout cannot double deliver.
4. If launch verification fails or expires, atomically remove the delivery gate and retain queued records. They become deliverable to the still attributable predecessor; release is recorded once. Do not discard them or call a failed successor a target.

This is a queue/gate proposal, not authorization to reroute. It blocks new delivery as requested while retaining the existing route and a rollback path. The ruling still needed is whether the coordinator may automatically release held messages to a verified successor, or must expose them for an explicit Flow/Message routing decision. The latter is safer under present evidence because the launcher explicitly does not register or retire either seat.

## Durable receipts and checkout changes

The coordinator's append-only record, handoff body/blob, launch receipt, gate receipts, and message envelopes need an owned durable store outside the shared checkout. Store content-addressed immutable payloads, then reference their hashes from the lifecycle log; atomically fsync/commit the payload before the transition that names it. A report or checkout file is a readable projection only. Replacing, pulling, or cleaning a checkout cannot erase the only launch or handoff evidence. On restart, reconstruct current state from the log and retain every accepted receipt; do not reconstruct it from directory presence or a process list.

The gate must use the same durable transaction boundary as the state advance: either final-response capture and gate receipt both exist, or neither does. A message racing that advance is committed either before capture sequence (old delivery semantics, with normal delivery receipt) or after it (queued under the gate). There is no unrecorded middle interval.

## Pending subflows and handoff returns

At RefreshRequested, snapshot parent-owned pending-subflow identities, their request/return correlation ids, and expected parent flow/generation into the refresh record. Do not cancel them. When one returns after HandoffCaptured, append its actual return payload/hash as a SubflowReturned receipt and put a compact notification in the durable refresh inbox. The notification is available to the verified successor after readiness; its payload may refer to the complete stored return. A result is not acknowledged as consumed merely because it was captured or queued.

This deliberately does not change a child's recipient, cause a child to message a successor, or issue it new instructions. Those are the deferred advanced rerouting behavior named in the raw vision. If the predecessor later becomes able to receive after rollback, normal parent correlation remains valid. If a successor is ready, release requires the same future routing decision.

## Ownership and non-actions

| Concern | Future owner | Evidence-bound rule |
| --- | --- | --- |
| Context observation | harness adapter | emits measurements; does not choose a route |
| Threshold and state CAS | Refresh Coordinator | one epoch; immutable receipts; no delivery claim |
| Final-response capture | predecessor hook plus coordinator | capture differs from successor readiness |
| Launch/readiness evidence | existing native launcher plus coordinator | launcher verifies native receipt; coordinator records it |
| Message holding/release | Message delivery gate | accepts/queues durably; release only with a rule |
| Subflow returns | subflow runtime plus coordinator inbox | capture/correlate only; no direct rerouting |

No automatic predecessor retirement, session reaping, route withdrawal, registration, or advanced direct-subflow rerouting is proposed. Those actions need separate authority and an observed successor route.

## Open decisions before implementation

1. Which harness APIs can provide trustworthy context measurement and atomic final-response event rather than approximate prompt-count hook?
2. What authority releases the held inbox to SuccessorReady? The raw request settles immediate blocking after handoff, but not automatic forwarding before a route is bound.
3. What priority rule applies to hard-abrupt living messages while the gate is closed: durable hold, a separate human-visible escalation path, or another explicitly authorized behavior?
4. Which durable component owns receipt log and message bodies, and what retention/compaction policy preserves auditability without reusing checkout storage?
5. What identifies a subflow return across harnesses, and what receipt proves its eventual successor consumption?

## Verification limits

This report was produced from static source inspection only. I did not launch, refresh, stop, message, or register a session; run a build/test; inspect a live message route; or verify the reported lost-receipt incident. The only executed coordination mutation was an Orchestrate lock on this report path, required to publish this unique artifact.
