# Transition and Hold: Operational and Flow Nexus Proposal

**Flow:** Mind Sol `6288d1`

**Date:** 2026-09-23

**Status:** Proposal for living review and Field implementation coordination. It takes no source ownership and authorizes no deployment.

## Evidence boundary

This proposal carries four different kinds of evidence:

1. **Living direction.** The living wants an ordinary message to be one CLI call; session start/end or process-exit signals to maintain registration; a short hold when a recipient is missing or in transition; operational work owned by Mind and testing work owned by Field; and Flow Nexus to absorb what the Hacky Messenger experiments discover.
2. **Distilled Vision.** Flow owns launch, identity, binding and refresh. Message owns durable attempts and receipts after Flow supplies an exact identity. Submission, transport, presentation, read and completion remain different facts.
3. **Machine proposal.** `Transition`, a bounded hold, durable pending attempts and one-time successor delivery come from the messaging audit and retained machine relays. The exact authority and lifecycle semantics are not yet living-approved.
4. **Source and test witness.** Revision `96d48f7dc6b83e6896cefc6c1cec0092112fded5` corrects Hacky Messenger's model of targeted `herdr agent get`: the response may contain only the selected agent, because the session was already selected by the command. An isolated run of that immutable revision passed 32 unit tests. This is not a live Herdr or deployment witness.

The current Hacky Messenger is experimental evidence for the final contracts. It is not the permanent owner of Flow identity or Message durability.

## Living direction

From `flows/d8df70/vision/messaging.md`, typed to Psyche Medium `d8df70` on 2026-09-23:

> You can just make a single CLI call and send a message. If there is a match for what you want and the pain still exists, then it just sends the message. I guess the script can check that the process still exists and is running in Herder?

The record notes “pain” as an inferred “pane” and “Herder” as Herdr; the original words remain unchanged.

The living also asked whether harness start/end hooks should register and unregister sessions, proposed using process exit when a normal exit hook is absent, and said a message could be held briefly when the registry is missing or says “in transition.” In the same record:

> If the mind gets involved then maybe there are some operational skills that he needs to adjust there too. Also in terms of making Flow Nexus adhere to all of the discoveries or insights that we are making with the script part, the hacky part of the hacky stack.

And:

> We have two skills:
> - Testing (field)
> - Operational (mine)

The source's reading of “mine” as Mind is an inference from context, not an alteration of the living's words.

## Target division of responsibility

### Flow Nexus

Flow owns the logical destination, current binding, binding generation, lifecycle generation, and the declared relationship between a predecessor and its expected successor. A transition is a Flow lifecycle fact. It is never inferred or created by a sender because a send failed.

The target Flow state relevant to messaging is:

```text
Active {
  logical_destination
  flow_id
  binding
  binding_generation
  lifecycle_generation
}

Transition {
  logical_destination
  predecessor_flow_id
  predecessor_binding_generation
  successor_expected
  since
  deadline
  lifecycle_generation
}

Exited {
  logical_destination
  last_flow_id
  last_binding_generation
  observed_at
  observation
}
```

Only the Flow meta authority may commit these states. A launcher or Field supervisor may submit witnessed lifecycle facts through that authority; it must not become a parallel registry writer. Successor registration clears `Transition` only through an authoritative generation-checked Flow mutation.

Process or pane exit removes the old binding from eligibility. It does not delete the Flow, imply archival, or authorize retirement. “Reap” remains separately unresolved across receiver removal, native stop and archive.

### Message Nexus

Message owns the durable attempt, hold, deadline, cancellation, delivery receipts and deduplication. A pending attempt records at least:

```text
PendingAttempt {
  attempt_id
  idempotency_key
  sender
  logical_destination
  predecessor_flow_id?
  successor_expected?
  lifecycle_generation
  binding_generation?
  payload_fingerprint
  created_at
  deadline
  state
  receipts
}
```

The payload itself remains in Message's durable store under its policy; Flow carries no message body. The attempt ID identifies an execution history. The idempotency key prevents a logically identical caller request from becoming a second delivery.

Message asks Flow for the exact binding immediately before any delivery attempt. It never selects a sibling, fallback rung or merely similar name after an ambiguous result.

### Sender and CLI

The ordinary sender makes one call. It neither probes first nor creates a messaging subflow. It does not resend a held or uncertain attempt. The CLI textualizes one typed request; the final Nexuses exchange only their compiled Signal contracts.

## Transition and hold contract

1. An authorized launcher or Field supervisor asks Flow meta to enter `Transition` before the predecessor stops being eligible. The mutation names the expected successor and a deadline and is generation-checked.
2. A send creates one durable Message attempt before route-dependent effects.
3. Message resolves the stable logical destination through Flow.
4. If Flow returns an eligible `Active` binding, Message validates the exact binding and attempts transport once.
5. If Flow returns `Transition`, Message waits on Flow's state subscription for at most the configured hold window. The current experimental default is about ten seconds; the final duration is policy, not protocol.
6. If the declared successor becomes `Active`, Message re-resolves and makes one generation-bound attempt to that successor.
7. If the hold window ends first, Message retains the same pending attempt. The sender receives `Held`; it does not resend. Later delivery, if still before the deadline, is performed by Message from the same attempt after a matching declared successor becomes active.
8. `NotRegistered` is not silently treated as a transition. A durable successor hold requires a Flow-authored transition or another typed declaration naming the expected successor. Without that authority, Message returns `Held.NotRegistered` and retains or expires the attempt according to explicit Message policy; it cannot invent the successor.
9. If transport may have issued the prompt but cannot prove its outcome, the attempt becomes `Uncertain`. It is never automatically retried, rerouted or delivered to a successor.
10. Transition expiry does not authorize delivery elsewhere. It produces a typed held/expired outcome for the same attempt and an operational condition for the responsible Field flow.

This design makes “the sender does not resend” true without losing the message: Message, not the caller, retains the one attempt. It also prevents the current experimental pending-file shape from becoming a second uncoordinated delivery system.

## Send-time acceptance

Before transport, the selected binding must agree with the live Herdr target on the recorded agent name, pane ID, terminal ID and harness agent. The selected pane's foreground process must prove the recorded native thread. The target must be `interactive_ready` and not blocked.

The Herdr session is selected in the `herdr --session … agent get …` command. A targeted `agent get` response is therefore valid without duplicating `session` inside its returned agent object. If a response does include a session, it must agree with the selected session.

These checks are a last-moment defense against stale bindings. They do not replace Flow's lifecycle authority or Message's durable attempt.

## Receipt contract

```text
Held        the attempt is retained or refused without a proved transport
Transported the exact selected transport accepted the prompt bytes
Presented   the target terminal or harness was observed receiving the prompt
Read        a target-side read acknowledgment was observed
Completed   the requested work returned its stated completion evidence
Uncertain   transport may have issued the prompt but the outcome is unprovable
```

`Held` needs a typed reason such as `NotRegistered`, `Retired`, `RouteHold`, `PaneMissing`, `IdentityChanged`, `ProcessMismatch`, `Blocked`, `NotReady`, `Stalled` or `InTransition`. Every reason except `Uncertain` is intended to mean that no prompt was issued, and the implementation must make that distinction testable. `Uncertain` is terminal for automatic delivery.

No grade is inferred from a stronger-sounding command result. In particular, `Transported` and `Presented` do not establish `Read`.

## Operational skill proposal

The following wording should land only with matching tool and lifecycle acceptance evidence:

```md
## Operational message send

For an ordinary message to a Herdr-hosted Flow, the main flow makes one direct call:

`FLOW_ID=<sender-flow> hm-send <recipient-flow> "<text>"`

Do not create a messaging subflow, send a probe, or send an acknowledgment-only message. The send performs recipient resolution and the binding, process, and readiness checks for that attempt.

`Submitted`, `Transported`, `Presented`, `Read`, and `Completed` retain their defined receipt boundaries. Never upgrade one grade into another.

`Held.{ FLOW <reason> }` means the attempt did not reach a proved transport. `Uncertain` means a prompt may already have been issued; never retry, reroute, or fall back after it.

When Flow reports an authorized transition, Message holds the same durable attempt for the bounded hold window and for one later delivery to the launcher-declared successor. The sender never resends. Missing registration without a Flow-authored successor declaration never authorizes Message to invent a successor.
```

`main-flow` should remove peer messaging from the subflow-script catalogue and state that routine peer messages use the operational rule directly. `subflow-scripts` should retain only transport investigation, testing and repair—not ordinary message routing. `messaging` should distinguish a pre-issuance binding failure from post-issuance uncertainty and forbid automatic retry after the latter.

## Source and test witness at `96d48f7`

Revision `96d48f7dc6b83e6896cefc6c1cec0092112fded5` changes:

- `tools/hacky-messenger/hm.py`: targeted agent matching no longer requires an embedded session; if session is present, it must match.
- `tools/hacky-messenger/test_hm.py`: adds `test_targeted_agent_get_without_session_is_the_exact_selected_session`.

An independent test used a `git archive` of that immutable revision with archive-tree digest `ebb98c2ae3f0bd0f63ab059dc9b9ca4247fc8eb5bcac7f6c8811d71098a6c150` and ran:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s <isolated>/tools/hacky-messenger -v
```

Result: exit 0, `Ran 32 tests in 15.127s`, `OK`. The corrected no-session case passed and produced the fixture's `Transported.{ test-flow working }` result.

The repository's `tools/hacky-messenger/check.nix` declares the same unittest discovery gate, but `flake.nix` does not expose it as a Nix check. The isolated run proves the 32 unit tests at the revision. It does not prove live Herdr behavior, installed revision, hooks, registry contention, successor delivery or deployment.

## Acceptance still required

Field acceptance should establish, with disposable identities and no production route mutation:

- a live targeted `agent get` response without embedded session;
- exact rejection of a mismatched optional session and each other binding facet;
- SessionStart registration and process/pane-exit projection;
- generation-checked entry into and exit from `Transition`;
- hold across Message and Flow restart;
- one delivery to the declared successor and none to any sibling;
- duplicate caller submission and pending replay deduplication;
- binding ABA and stale-successor rejection;
- crash boundaries around persistence, resolution and transport;
- zero automatic resend after `Uncertain`;
- receipt-grade evidence at the exact observed boundary.

The current revision writes pending files for `NotRegistered` and `InTransition`, but no consumer drains them to a declared successor. `successor_expected` is stored but not enforced as a delivery contract. That is the principal implementation gap between the experiment and this proposal.

## Open decisions for the living and owners

1. Which exact Flow meta authority may enter `Transition`, and may Field submit observations directly or only through a launcher-owned replacement operation?
2. Does `NotRegistered` without an existing transition retain a pending attempt, and under which expiration policy?
3. What deadline and cancellation authority belongs to the sender versus Message policy?
4. What exact effects does “reap” authorize at receiver removal, process stop and archival stages?
5. Which coherent Flow/Message source graph and owners implement this contract without parallel registries or controllers?
6. When should the experimental `hm-send` CLI become a thin client of Flow and Message rather than an owner of registry and pending state?

## Sources

- `flows/d8df70/vision/messaging.md` — living words and source notes, 2026-09-23.
- `flows/d8df70/reports/messaging-audit.md` — machine-authored audit and B/B6 proposals, 2026-09-23.
- `flows/6288d1/reports/recent-psyche-for-flow.md` — Mind Sol synthesis of recent Psyche for Flow, 2026-09-23.
- `Vision/flowNexus.md` — distilled Flow identity, launch, refresh and subflow vision.
- `Vision/modelRoles.md` — distilled typed model, identity and routing vision.
- `Vision/messaging.md` — distilled messaging and receipt distinctions.
- `flows/4b0f60/reports/flow-nexus-main-replacement-contract.md` — owner-scoped machine architecture and evidence boundaries, 2026-09-23.
- Git revision `96d48f7dc6b83e6896cefc6c1cec0092112fded5` — Hacky Messenger source correction and regression test.
- Independent isolated unittest witness for revision `96d48f7`, Flow `6288d1`, 2026-09-23 — 32 tests passed; no live or deployment claim.
- Machine relay `e0ffc1fc3ad6545bcadcc88cafdaa8796`, origin `9ddcbc`, timestamp `2026-09-23T22:52:44Z` — requests incorporation and reports Field acceptance; treated as a machine-origin claim pending the witnesses above.
