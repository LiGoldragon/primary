# Track A (ClientApproval park substrate) — adversarial review

Mission 2 of the 705 criome-cluster reassessment. Read-only review of the
three landing commits at origin/main:

- criome `245f0441` — park client approval authorizations
- signal-criome `ff9ac192` — add parked authorization surface
- meta-signal-criome `4940e4b1` — add parked authorization approval surface

Verdict: the landing is mostly clean. The contract shape is sound, the
custody docs now match p43g, NOTA is positional and quote-free, generated
code obeys the method-only rule. The real defects are about
authorization *gating* (who is allowed to decide a parked request) and
*unwired contract surface* (advertised rejection replies the daemon can
never emit), plus a string-sorted slot ordering bug. None block the
ClientApproval skeleton; several should be closed before it is presented
as a security boundary.

## (a) Workspace-rule audit — clean for Track A

- **No new free functions.** The only free function outside test/main in
  the touched files is the pre-existing, dead `pub fn active_status`
  (`criome:src/actors/store.rs:712`), introduced in `66276fe` (the
  original skeleton), not Track A. It is unused
  (`git grep active_status` finds only the definition) and violates the
  method-only rule, but it is not this landing's defect. Worth a cleanup
  bead.
- **No ZST-namespace methods.** New logic lives on real data-bearing
  types: `CriomeRoot` (root.rs), `StoreKernel` / `CreateAuthorizationState`
  (store.rs), `CriomeTables` / `AuthorizationSlot` (tables.rs),
  `AuthorizationStateRecord` / `ParkedAuthorizationSnapshot`
  (signal-criome lib.rs).
- **No hand-rolled parsers.** Wire decode stays in the schema-emitted
  codec; the daemon never parses NOTA.
- **No blocking in actor handlers.** Every new `Message::handle`
  (`CreateAuthorizationState`, `ReadAuthorizationSnapshot`,
  `SubmitMetaRequest`) is a sync table op or a delegated `.ask(...).await`;
  no `std::fs` blocking beyond the sema-engine calls the kernel already
  made, no thread sleeps, no sync mutex.
- **Identifiers are full words.** `request_slot`, `parked_evaluation`,
  `configuration_generation`, `authorization_mode` — no abbreviations
  introduced.
- **NOTA is positional and quote-free.** Both canonical example files are
  type-head-first with no `(key value)` pairs and no `"`:
  `signal-criome:examples/canonical.nota` (`ObserveParkedAuthorizations ()`,
  `ParkedAuthorizationSnapshot [...]`) and
  `meta-signal-criome:examples/canonical.nota`
  (`SubmitAuthorizationApproval (authorization-request-1 Approve)`).
- **Generated code obeys method-only.** All emitted items in
  `signal-criome:src/schema/lib.rs` and
  `meta-signal-criome:src/schema/lib.rs` are `impl`-block methods or
  `impl From<X> for Y`, e.g. `From<ParkedAuthorizations>` /
  `From<ParkedAuthorizationSnapshot>` at lib.rs:2270/2289.

## (b) Contract shape — `AuthorizationRequestSlot` is sound; one sort bug

- **The slot is a monotonic, never-reused counter — not a fragile
  index.** `AuthorizationSlot` is a `u64` persisted in the
  `criome-authorization-slot` family
  (`criome:src/tables.rs:602-626`, `next_authorization_slot` at :497).
  Every mint reads the stored next value, formats it as a decimal string,
  and stores `value+1`; the cold-start fallback is `max(existing)+1`
  (`after_records` at :611). No reuse, no recycling. The list→approve
  race the mission asked about does not exist: a stale slot from a prior
  `ObserveParkedAuthorizations` can only refer to the same logical
  request forever, so a late `SubmitAuthorizationApproval(slot, …)`
  targets exactly the request the client saw. Worst case is a no-op /
  Reject (see the next finding), never a wrong-target approval.

- **MEDIUM — parked snapshot ordering is lexicographic over decimal
  strings.** `StoreKernel::authorization_snapshot` sorts by
  `request_slot.as_str().cmp(...)` (`criome:src/actors/store.rs` —
  `authorization_snapshot`), so slot `"10"` sorts before `"2"`. The
  parked list is therefore returned in string order, not mint order.
  A client paging or "approve oldest first" will mis-order once ≥10
  parked requests exist. The slot is an integer that was deliberately
  stringified for the wire; the store should sort by the parsed `u64`
  (same `parse::<u64>()` already used in `after_records`).

- **The snapshot model is sound but unbounded.**
  `read_parked_authorization_snapshot` (`criome:src/actors/root.rs`)
  pulls the *entire* authorization-state table via
  `ReadAuthorizationSnapshot`, then filters `status == Parked` in the
  root actor and clones the full `AuthorizationEvaluation` (all
  evidence + BLS envelopes) for each. Granted/Denied/Expired records are
  never pruned, so every parked-list call deserializes and rescans the
  whole history. Correct, but O(total-authorizations) per list and
  carrying full evidence payloads. LOW for a skeleton; a dedicated
  parked-only index (or a Parked secondary key) is the fix when this is
  load-bearing.

## (c) Custody docs vs p43g — VERIFIED, now consistent

The custody section was the previous model's worst stale spot; it is now
corrected across all three doc surfaces.

`criome:ARCHITECTURE.md` §6 (the diff replaces the old "personas hold
their own; criome does not custody private keypairs other than its own
master" bullet):

> Private keypair custody is daemon-managed. Requesters submit typed
> objects and evidence; they do not sign the final authorization
> decision. Criome owns the key store it uses to sign or record
> authorization outcomes.

Quorum = peer criome nodes signing is stated unchanged at
`ARCHITECTURE.md:131-132`:

> *Complex policy (quorum)* — needs criome's own signature plus
> signatures from named peer criome daemons. Cross-criome routing
> solicits the additional signatures.

`AGENTS.md` repo-role now reads "owning criome's local key store …
authorization state" and drops "hold any private keys other than its own
root." `skills.md` replaces "No private keypair custody other than
criome's root / Personas … custody their own private keys" with "Criome
owns daemon-managed keys and makes authorization decisions. Do not model
requesters as signing the authorization decision." A grep for the old
language (`hold their own`, `personas hold their own`, `criome does not`,
`only verif`) finds no surviving contradiction. The one remaining
"verify external signatures" bullet (`ARCHITECTURE.md:43`) is a distinct,
legitimate capability (verifying developer release signatures), not the
old custody model. **Docs pass.**

## (d) Error handling & typed Error — mostly good, two soft spots

- **Good:** the store actor models creation outcomes as a typed enum
  (`AuthorizationStateCreationOutcome` with `Created` / `ReplayAttempted`
  / `StoreUnavailable`, `criome:src/actors/store.rs:111`) and round-trips
  through the per-crate `crate::Error`. `from_result` / `into_result`
  preserve `AuthorizationReplayAttempted` distinctly.

- **MEDIUM — park failure is laundered into `MalformedRequest`.**
  `CriomeRoot::park_authorization` (`criome:src/actors/root.rs`) maps
  *any* `Err(_error)` from `create_authorization_state` to
  `rejection(RejectionReason::MalformedRequest)`. A store-unavailable
  failure (disk, sema-engine) is reported to the client as if the request
  were malformed. The typed distinction the store just built
  (`StoreUnavailable` vs `ReplayAttempted`) is discarded one layer up.
  This pattern repeats across the `ask_*` helpers, but park is the new
  path. There is no `Unavailable`-class working reply being produced even
  though `AuthorizationUnavailable` exists in the contract.

- **MEDIUM — approving an unknown slot silently records a Reject.**
  `CriomeRoot::record_authorization_approval` (`criome:src/actors/root.rs`):
  when `lookup_authorization_state(slot)` returns `None`, the code sets
  `recorded_decision = AuthorizationApprovalDecision::Reject` and replies
  `AuthorizationApprovalRecorded { slot, decision: Reject }` — *even
  when the client sent `Approve`*. So an approve against a typo'd /
  already-resolved slot comes back as "recorded: Reject," which is a
  confusing lie (nothing was recorded; the slot doesn't exist). The
  honest reply is the contract's own `RequestUnimplemented` or a
  not-found variant; instead the surface fabricates a Reject. This also
  means a deferred-then-resolved slot that a client re-approves reads
  back as Reject.

## Cross-cutting findings

- **HIGH (gating) — a working-socket peer can deny a ClientApproval
  parked request.** `AuthorizationCoordinator::reject_authorization`
  (`criome:src/actors/authorization.rs:197`) transitions *any* slot to
  `Denied` with `source: Signers`, with no authorization-mode check and
  no caller-identity check. In ClientApproval mode the meta authority is
  supposed to be the sole decider (the whole point of parking), but a
  client on the **working** socket can send `RejectAuthorization(slot,
  …)` and flip a parked request to Denied out from under the meta client.
  The two decision paths (working `RejectAuthorization` → `source=Signers`
  vs meta `SubmitAuthorizationApproval(Reject)` → `source=Policy`) are not
  mutually exclusive and the working path is not gated by mode. The park
  model's exclusivity rests entirely on the 0600 socket file
  permission, not on any in-daemon check.

- **HIGH (advertised-but-unbuildable replies) — `ConfigurationRejected`
  and `RequestUnimplemented` are dead contract surface.** Both reply
  variants are defined in `meta-signal-criome:schema/lib.schema` (with
  reasons `ManagerAuthorityRequired`, `MalformedConfiguration`,
  `StoreUnavailable`, etc.) and the constructors are emitted
  (`meta-signal-criome:src/schema/lib.rs:240` `configuration_rejected`,
  :243 `request_unimplemented`). criome never constructs either — a grep
  for `configuration_rejected` / `request_unimplemented` /
  `ManagerAuthorityRequired` over `criome/src/**` is empty.
  `CriomeRoot::configure` (`criome:src/actors/root.rs`) *always* returns
  `Configured`, even on a malformed config, and performs **no** manager-
  authority check despite `ManagerAuthorityRequired` existing for exactly
  that. The contract promises a rejection handshake the daemon cannot
  produce. Either wire the checks or this is a contract that lies about
  its failure modes.

- **MEDIUM (security model) — no `SO_PEERCRED` anywhere.** The project
  context names SO_PEERCRED as the authentication primitive and
  ARCHITECTURE.md §"Authorization model" says "Only that user can write
  to the daemon's meta socket." A grep for `SO_PEERCRED` / `peer_cred` /
  `getsockopt` over `criome/src/**` is empty. Access control is purely
  the 0600 bind in `Daemon::bind_private_socket`
  (`criome:src/daemon.rs:129-135`). For a single-Unix-user daemon 0600
  is defensible, but the meta-vs-working *authority distinction* that
  Track A's approval flow assumes (HIGH finding above) has no kernel-
  verified peer credential behind it. Pre-existing, not a Track A
  regression, but Track A is the first feature whose correctness depends
  on that distinction.

- **LOW (replay asymmetry, by design but undocumented in code) — parked
  requests carry no replay guard.** `CreateAuthorizationState::parked`
  sets `replay_identity: None` (`criome:src/actors/store.rs`), so
  `put_new_authorization_state` skips the replay-nonce write
  (`criome:src/tables.rs` — the `if let Some(replay_identity)` guards).
  Two identical client-approval evaluations therefore mint two distinct
  parked slots. ARCHITECTURE.md §"Current implementation status" does
  call this out ("parked client-approval authorization … does not consume
  requester/nonce replay state because it is keyed by the parked
  evaluation"), so it is an intentional decision — but the evaluation
  carries no nonce field at all, so there is no dedup key available even
  if wanted. Acceptable for the skeleton; flag for when ClientApproval
  faces untrusted submitters.

## Test coverage note

`criome:tests/daemon_skeleton.rs`
`meta_socket_approval_by_parked_id_records_authorized_head_update` is a
genuine in-process socket round-trip: Configure(ClientApproval) →
EvaluateAuthorization (asserts `AuthorizationPending`) → ObserveParked
(asserts 1 entry, slot + full evaluation match) → Defer (asserts still
parked) → Approve (asserts `AuthorizationApprovalRecorded { Approve }`)
→ ObserveAuthorizedObjects (asserts the head update published). Good
coverage of the happy path and defer-keeps-alive. **Untested:** meta
`Reject` path, approve-against-unknown-slot (the fabricated-Reject
finding), working-socket reject of a parked request (the gating
finding), and the absent `ConfigurationRejected` path. No VM proof of the
park flow yet (consistent with the stated current state).
