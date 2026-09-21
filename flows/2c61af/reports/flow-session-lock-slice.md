# Flow session-lock slice

**Status:** design and review input only. No component reservation, code edit, test run, build, delivery, or runtime claim accompanies this record.

## Observed baseline

The inspected Flow candidate is `/home/li/wt/github.com/LiGoldragon/flow/night-messaging-0ab019`, clean at `55bab983` with parent `e387576f`. Its `crates/flow-nexus/src/store.rs` persists a `FlowRecord` containing identity, native thread, lifecycle, and **lifecycle** `generation`. It separately persists Herdr routes. Registration atomically asserts a new flow plus route; changed session, harness, or route returns `ConflictingBinding`. Inline tests already cover reopen/restart, pending recovery, duplicate binding refusal, and legacy-row reopen.

There is no persisted delivery-binding generation, opaque binding nonce, session hold/open state, admission permit, or quiescence transition. `RestartAuthorization` is a read-time restart authorization and must remain distinct from a delivery-binding token.

## Selected holder-executed slice

Mind owner4b0f60 selected Option A: retained holder f72ab7 is the sole writer of this narrow slice under existing Lock 2836, **only after explicit bounded implementation authorization**. The write set is exactly `crates/flow-nexus/src/store.rs`, including its inline `#[cfg(test)]` module. Before editing, f72 confirms candidate base and clean state, confirms no concurrent writer, and obtains the required own Orchestrate reservation/authorization. This record grants none of those conditions.

The slice excludes `lib.rs`, adapters, Flow CLI, all Message and signal-message files, signal-flow vocabulary/generated source, migrations, deployment, and activation. Message owns durable attempts, queueing, receipts, sender waiting deadlines/cancellation, and bounded missing-recipient recovery. A sender deadline has no Flow API that can release a Flow hold.

## Proposed store contract

Persist a separate binding record keyed by Flow identity with: `flow_id`; opaque, unguessable `binding_nonce`; monotonically increasing `binding_generation`; the exact protected native/session binding; `state: Open | Held | Quiescent`; and lifecycle generation plus source binding evidence captured at creation. Binding generation is separate from the existing lifecycle generation.

Create `Open` only for a current registered Flow binding. Admission atomically verifies that binding and changes `Open` to `Held`, returning the nonce and binding generation. Entering `Quiescent`, reopening, or releasing requires the exact current Flow identity, binding, nonce, and generation. Reopen/release atomically returns to `Open` and advances binding generation before later admission. A native restart may advance lifecycle generation, but cannot silently recreate, release, or validate a delivery binding. A validated rebind creates a new binding generation; the old nonce is unusable.

This is only the Flow admission/quiescence boundary. It does not establish a Message delivery, acceptance, retry, cancellation, or completion.

## Failure semantics

Absent, duplicated, undecodable, corrupt, or schema-incompatible binding data fails closed: admission, admitted-recipient resolution, reopen, and release refuse. Counter overflow fails closed and never wraps. Unknown flow, session/harness/route mismatch, stale nonce, stale binding generation, lifecycle mismatch, competing admission, and a request during `Held` or `Quiescent` refuse without changing durable state. Restart/open with incomplete hold evidence refuses rather than inferring an unlocked state.

## Focused inline acceptance tests

- `binding_admission_persists_hold_across_reopen`: reopening retains the held binding and cannot issue a second admission.
- `stale_nonce_or_binding_generation_cannot_release_rebound_hold`: an old token/generation cannot alter a newer binding, covering ABA.
- `conflicting_binding_or_concurrent_admission_preserves_one_hold`: one valid binding/hold commits and the competitor is refused.
- `missing_or_corrupt_binding_record_fails_closed`: resolution, admission, reopen, and release refuse.
- `binding_generation_overflow_fails_closed`: no wrap and no new admission.
- `restart_does_not_release_or_revalidate_a_held_binding`: lifecycle restart and delivery binding generation stay distinct.
- `quiescent_binding_is_not_recipient_admissible`: recipient resolution remains unavailable while quiescent until a valid current reopen.
- `sender_deadline_has_no_flow_hold_release_path`: no deadline-driven Flow transition exists and a held record stays held.

These are acceptance requirements, not results. Ultra23d977's returned matrix identifies damaged-file fail-closed, ABA generation/token, and contention coverage as absent; it credits existing restart/open coverage. Low e798f3 is already acknowledged for a separate read-only audit. No test ran for this record.

## Coordination and blocker

Lock 2836, held by f72ab7, covers the entire candidate worktree. Lock 1834, held by553901, covers `/home/li/primary/flow` and its report. These are distinct checkouts, but Field's read-only comparison found the same upstream and differing `store.rs` hashes; checkout separation is not a source-ownership decision. The protected owner has no observed route, acknowledgement, completion, transfer, or successor authority. Original assigner da1e3f and recorded successor108ab0 do not establish transfer. Fac697's released 1836/1837/1839 locks were separate work and do not alter 1834.

Requests to f72 through retained crossover0ab019 and to protected-owner lookup through Field9ddcbc were submitted through Herdr and are **Submitted, not Read**. f72 now accepts Option A only prospectively, pending this concrete model, owner consent, and implementation authority. No owner reply grants an edit or reservation. The work is blocked until explicit agreement and the holder's exact Orchestrate reservation. No route is released, resumed, retired, or replaced.

## Sources

- Read-only `crates/flow-nexus/src/store.rs` inspection at clean `55bab983`, parent `e387576f`.
- `flows/4b0f60/reports/nexus-messaging-current-handoff.md` and the Field census/checkup and context-usage integration contracts.
- Live `orchestrate 'Observe.Locks'` receipt showing Locks 1834 and 2836.
- Current Flow coordination receipts and owner-status relays.
