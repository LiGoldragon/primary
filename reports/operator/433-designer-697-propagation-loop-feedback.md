# 433 — operator feedback on designer 697 propagation-loop blockers

## Scope

Reviewed `reports/designer/697-propagation-loop-state-blockers.md` against
current `spirit`, `router`, `criome`, `mirror`, and `signal-mirror` main
checkouts. This is feedback only; no code repos were edited.

## Verdict

Designer 697 is directionally right and usefully corrects the framing:
operator 431 closed the schema-chain split and proved a real offline
ship/router-notify/restore loop, but that green proof is not yet the
criome-gated typed authorized-head loop.

The most important addition from this audit: Q1 is answerable from current
mirror code. `signal-mirror::RestoreQuery` is just `StoreName`, and
`mirror::Store::load_restore` returns the latest checkpoint plus every later
entry. Mirror does not currently support restore-by-digest or restore-by-head.
So the immediate causal witness is necessarily "restore latest, then verify it
matches the delivered head"; true fetch-by-`D` needs a signal-mirror contract
change.

## Confirmed

### The current Spirit loop is transport-causal, not criome-causal

`spirit/tests/end_to_end_offline_full_chain.rs` says it plainly: no criome
daemon, router offline accept-fixed verifier, and one test-local seam:
`MirrorObjectNotice { store, sequence, digest }`. The notice is encoded into a
chat-shaped `signal-message::MessageBody` and forwarded by two router runtimes.

The test is still valuable. It proves:

- Spirit-shaped component history ships to a real mirror service.
- Router A forwards a message to Router B.
- Router B delivers to a local harness witness.
- Mirror B fetches from Mirror A and restores a fresh store whose records match.
- The restored store's current sequence equals the sequence carried in the
  delivered notice.

It does not prove:

- Spirit asked criome to authorize the head.
- A 2-of-3 root contract gated the propagation.
- Router carried a typed `AuthorizedObjectReference { Spirit, D, Head }`.
- Restore was requested by `D`; the restore request only names the store.

### Router authorized-object fanout is real but not yet a public wire path

`router/src/authorized_object.rs` has `AuthorizedObjectFanout` with
`AttendAuthorizedObjects`, `WithdrawAuthorizedObjects`, and
`PublishAuthorizedObjectReference`; `tests/authorized_object_fanout.rs` proves
reference-only delivery filtering, late snapshots, and projection from
`signal-criome::AuthorizedObjectReference` to `signal-standard`.

However, I found no `AuthorizedObject*` surface in `signal-router` or
router's generated signal schema. So this is a real in-process actor/API, not
yet a production component subscription operation through the router signal
contract.

### Criome still owns an operational matcher, but that should not be deleted blindly

`criome/src/actors/subscription.rs` still uses `AuthorizedObjectInterest` to
filter snapshots, count matching subscribers, and evaluate scheduled
time-check absence conditions. Designer is right that component fan-out should
move to router-sole. The nuance: criome still needs the same predicate for
stored observation/audit and contract-time checks. The cleanup is not "remove
matching from criome"; it is "remove criome as the component delivery matcher."

## Corrections / sharpened points

### Q1 is decided by current code

Designer asks whether mirror supports content-addressed restore by digest
today. It does not. Current `RestoreQuery(StoreName)` has no head/digest field,
and `load_restore` asks for the latest checkpoint plus suffix to the current
store end.

Recommended slice:

1. In the current Spirit offline test, replace "restore latest, assume it is D"
   with an explicit post-restore assertion that both sequence and digest equal
   the delivered notice. Sequence is already asserted; digest should be
   asserted against the restored imported head, not only against the source
   confirmed head.
2. Add the adversarial test: announce D1, advance mirror to D2, restore-latest
   must fail the delivered-D assertion.
3. Later, change `signal-mirror::RestoreQuery` to carry a target `HeadMark` or
   equivalent digest/sequence coordinate, and make mirror return the bundle for
   that head or a typed refusal.

### The real loop has four wirings, not three

Designer names three main wirings: criome authorize, typed reference, acquire
exactly D. I would split router fanout into two pieces:

1. `spirit` produces a candidate head object `D`.
2. `criome` evaluates/authorizes `D` under the 2-of-3 root contract.
3. `router` publishes the resulting `signal-standard::AuthorizedObjectReference`
   to matching subscribers.
4. subscriber-side `spirit` or mirror acquisition consumes that delivered
   reference and restores/verifies exactly the announced head.

Step 3 needs the router fanout actor connected to a real signal/wire path, not
only tested by direct actor messages.

### The criome-gate should precede mirror publication in the proof

The current loop ships to mirror first, then emits a notice about what mirror
accepted. The target loop says a head is authorized, then propagated. For a
clean proof, the test should make the authority order visible:

1. produce local head `D`;
2. ask criome to authorize `D`;
3. publish the authorized reference through router;
4. fetch/restore the data needed for `D`.

If mirror shipping remains physically before criome authorization because the
remote needs bytes to exist before subscribers can fetch them, the test should
still distinguish "bytes are available" from "head is authorized." The pulse
should be emitted only after criome authorization.

## Priority

I agree with Designer's priority: close the single-host fully causal loop next.
That gives one hard proof that the architecture is real before multi-machine
work adds transport noise.

The implementation order I would use:

1. Add the red adversarial Spirit test for D1/D2 restore-latest mismatch.
2. Replace `MirrorObjectNotice` in the happy path with a typed standard
   authorized-head reference as far as current crates allow.
3. Add a minimal criome authorization call in the test path for a 2-of-3
   Spirit `Head`.
4. Connect router authorized-object fanout to the test path.
5. Keep criome matching for audit/time-check semantics, but stop using it as
   the component delivery matcher.

That turns operator 431's strong transport witness into the first
LoopProvenGreen witness for the actual agreement-machine shape.
