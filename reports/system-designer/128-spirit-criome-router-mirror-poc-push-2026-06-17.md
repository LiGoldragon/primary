# 128 - Spirit -> criome -> router -> mirror PoC push

## Frame

The psyche clarified the intended production path:

```text
Spirit accepts a new log object
-> Spirit asks local criome to authenticate the exact object/event
-> criome validates that this is a Spirit-shaped object Spirit is allowed to ask it to sign
-> criome signs/authenticates it under the local structural trust boundary
-> propagation goes through Router
-> the remote mirror receives the authenticated event and fetches/restores the announced head
```

Two constraints came through clearly:

- criome is auth/authorization logic, not transport;
- all cross-host propagation still goes through Router.

Threshold/majority/time-window acceptance is real direction, but belongs in later criome contract logic, not in the first Router/mirror PoC slice.

## Spirit intent maintenance

Existing intent records were checked first for `spirit`, `criome`, `router`, and `mirror`.

Updated/added:

- `d6he` (first e2e milestone) now explicitly carries the clarified order: Spirit accepts log object, asks local criome to authenticate the exact content-addressed object/event, criome trusts the local structural request boundary, validates the Spirit-shaped request, signs/authorizes it, and propagation goes through Router to remote criome/mirror participants.
- `5osd` was clarified by the mirror worker: mirror topology now carries the router-carried object/head notice and mirror-owned fetch/restore shape.
- `z9d6` was newly recorded: criome authorization contracts should be content-addressed composable objects, where one component's acceptance can depend on another accepted object/contract.

Attempted but rejected:

- A `w2g3` clarification was rejected because it tried to preserve the envelope as open while `2st7` already settles the Spirit criome-auth pilot envelope. Correct handling is to work under `2st7`, not reopen it.

## Subagent work

### Mirror worker result

Worker `Epicurus` implemented a bounded signal contract slice.

Branch:

```text
signal-mirror mirror-object-notice @ 24ee1949
```

Changed files:

- `signal-mirror/schema/lib.schema`
- `signal-mirror/src/schema/lib.rs`
- `signal-mirror/tests/round_trip.rs`
- `signal-mirror/ARCHITECTURE.md`

New contract shape:

```text
NotifyObject(ObjectNotice)
ObjectNoticeAccepted(ObjectNoticeReceipt)
ObjectNoticeRejected(ObjectNoticeRejection)
ObjectNotice { store, head, source }
```

Verification:

```text
cargo fmt --check
cargo test
```

`cargo test` passed 16 tests. `nix flake check` was not available because `signal-mirror` has no `flake.nix`.

The runtime auto-fetch path was intentionally not implemented yet. The semantic blocker is what `ObjectNoticeAccepted` means.

### Router worker

Still running at report time. Scope: Router m3, `ForwardAttestationVerifier`, `TailnetForwardIngress`, replay/freshness, refusal mapping.

### Criome worker

Still running at report time. Scope: typed Spirit log-object authentication request, current criome sign/verify/admission APIs, and smallest contract/runtime step toward the clarified path.

## Current architecture lean

### Notice acceptance should mean present/restored

For `ObjectNoticeAccepted`, the strongest semantic shape is:

```text
accepted = the announced head is already present or fetch/restore completed
```

We should avoid:

```text
accepted = notice decoded and queued
```

Reason: Router delivery already proves the notice arrived. Mirror acceptance should prove mirror state changed or was already sufficient. If the mirror only queues, the reply should say queued/deferred, not accepted.

### Router verifies first, mirror object attestation follows

First cut:

- Router-carried frame has criome attestation.
- Router verifies the sender before applying forwarded message.
- Mirror receives a typed object notice from Router.

Later defense-in-depth:

- the mirror notice or fetch payload also carries object-level criome attestation;
- mirror verifies the object-level attestation before restoring.

This matches existing `5osd`: router carries notification; mirror owns object/fetch.

### Criome propagation remains auth logic, not transport

The psyche phrased criome as potentially propagating authorization/authentication. The safer interpretation under existing `wckt` is:

- criome emits or signs an authenticated event;
- Router transports the event;
- remote criome/mirror participants consume it;
- criome contract logic can later require majority/threshold/time-window agreement before announcing acceptance.

Criome should not become the network transport.

## Open questions for psyche

1. Should `ObjectNoticeAccepted` mean the announced head is already present/restored?

My lean: yes. If mirror only queued the work, use a separate deferred/queued reply.

2. For the first live cut, should `ObjectNotice.source` stay a raw `MirrorAddress`, or become a structured `.criome` service endpoint now?

My lean: raw now, then structured service endpoint when Router m4 config lands.

3. Does the first PoC require object-level criome attestation inside the mirror notice, or is Router-frame attestation enough for the first cut?

My lean: Router-frame attestation first; object-level attestation follows.

4. Should criome threshold/majority/time-window policy be modeled now, or left as a later contract family?

My lean: later. The first contract should authenticate one Spirit object/event and leave the acceptance-policy vocabulary extensible.

5. Is the first typed criome request named around Spirit specifically, or generic enough for every component to use?

My lean: generic criome `AuthenticateObject` / `AuthorizeObject` shape with a typed purpose field, where Spirit supplies the first concrete purpose.

## Immediate next implementation order

1. Review the `signal-mirror` `mirror-object-notice` branch and decide the `ObjectNoticeAccepted` semantics.
2. Let Router worker finish m3 seam/replay assessment.
3. Let criome worker finish the typed authentication-request assessment.
4. If both line up, implement:
   - `signal-criome` typed authenticate/authorize object request if missing;
   - Router m3 criome verifier + replay window;
   - mirror runtime handling for `NotifyObject` with fetch/restore semantics.
5. Then wire the spirit harness away from harness-local `MirrorObjectNotice` toward the new `signal-mirror` notice.
