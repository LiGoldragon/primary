# Ground-truth: criome origin/main

Sub-report 1 of the 705 criome-cluster reassessment. Descriptive map of
criome `origin/main` (`245f0441`) as the code actually is, with file:line
evidence. Read read-only via `git -C <repo> show origin/main:<path>`; no
working copy mutated. Companion repos: signal-criome `ff9ac192`,
meta-signal-criome `4940e4b1`.

This is ground-truth, not critique. A few "wired vs dormant" facts are
flagged plainly because the mission asks for them; they are observations,
not recommendations.

## (a) AuthorizationMode and where the three modes branch

`AuthorizationMode` is a copy enum in signal-criome with exactly three
variants:

- `signal-criome/src/schema/lib.rs:247-251` — `enum AuthorizationMode { Quorum, AutoApprove, ClientApproval }`.

The mode lives on `CriomeRoot` (`criome/src/actors/root.rs:35`,
`authorization_mode: AuthorizationMode`), defaulting to `Quorum`
(`Arguments::new`, root.rs near the `Arguments` impl; daemon default
`AuthorizationMode::Quorum` at `criome/src/daemon.rs:43`). It is set at
boot from the rkyv config (`CriomeDaemon::from_configuration`,
daemon.rs:47-60) and re-set at runtime by `Configure`
(`root.rs` `configure`, sets `self.authorization_mode = *configuration.authorization_mode()`).

The **only** place the three modes branch is `CriomeRoot::evaluate_authorization`
(root.rs, the `evaluate_authorization` method). Branch order:

1. Digest-consistency guard: if `evaluation.object.digest != evaluation.evidence.operation.object_digest()` -> `rejection(MalformedRequest)`.
2. `if self.authorization_mode == AuthorizationMode::AutoApprove` -> `record_evaluation_decision(evaluation, EvaluationDecision::Authorized)` immediately (no quorum, no parking).
3. `if self.authorization_mode == AuthorizationMode::ClientApproval` -> `park_authorization(evaluation)`.
4. Fallthrough (= `Quorum`): load `key_registry()` + `contract_store()`, run `store.evaluate(&contract, &evidence, &registry)`; `Ok(decision)` -> `record_evaluation_decision`; `Err(MissingContract(d))` -> `ContractMissing`.

Key observation: the mode is branched **only in `EvaluateAuthorization`**.
The legacy `AuthorizeSignalCall` path (authorization.rs
`authorize_signal_call`) is mode-blind — it always creates a `Signing`-status
state and returns `AuthorizationPending` regardless of mode. So "the
submit/evaluate flow" that honors the mode is the `EvaluateAuthorization`
request handled directly on root, not the coordinator's `AuthorizeSignalCall`.

`root.rs::submit` dispatch map (the working-signal request router):
- `EvaluateAuthorization(evaluation)` -> `self.evaluate_authorization(...)` (root-local; the mode-aware path).
- `AuthorizeSignalCall` / `ObserveAuthorization` / `VerifyAuthorization` / `RouteSignatureRequest` / `SubmitSignature` / `RejectAuthorization` / `AuthorizationObservationRetraction` -> forwarded to `AuthorizationCoordinator` via `ask_authorization`.
- `ObserveParkedAuthorizations(request)` -> `self.parked_authorization_snapshot(request)` (root-local).
- Sign / Attest* -> signer; Register/Revoke/Lookup identity -> registry; contracts -> store; subscriptions -> subscription.

## (b) ClientApproval park flow, end to end

### What is parked

`park_authorization` (root.rs) calls
`create_authorization_state(store::CreateAuthorizationState::parked(evaluation))`.
`CreateAuthorizationState::parked` (store.rs, the `parked` builder near
store.rs:218) sets `status = AuthorizationStatus::Parked`,
`request_digest = evaluation.object.digest`, `parked_evaluation = Some(evaluation)`,
and crucially `replay_identity = None` (parked submissions carry no
requester/nonce replay key, unlike `signing`/`expired`).

The stored record is `AuthorizationStateRecord`
(signal-criome/src/schema/lib.rs:1012-1020): `request_slot`,
`request_digest`, `status`, `state_missing_authorities`, `grant`, `denial`,
`parked_evaluation: ParkedEvaluation(Option<AuthorizationEvaluation>)`
(crate-private wrapper, lib.rs:1007).

### The slot model

`AuthorizationRequestSlot(String)` (signal-criome/src/schema/lib.rs:79).
There is **no separate `ParkedAuthorizationId` type** — parked records are
keyed by the same `AuthorizationRequestSlot` as every other authorization
state. The slot is a monotonic u64 counter rendered as a decimal string:

- `criome/src/tables.rs` `AuthorizationSlot::request_slot` -> `AuthorizationRequestSlot::new(self.value.to_string())` (tables.rs:620-621).
- Counter persisted in table `authorization_next_slot` (tables.rs:35, key bump in `put_new_authorization_state` tables.rs ~431).
- `next_authorization_slot` reads the counter or falls back to `after_records` (= max existing numeric slot + 1) (tables.rs:497-503, 605-614).

So a parked authorization's identity = the decimal slot string the daemon
assigned at park time, returned in the `AuthorizationPending` reply.

### Park reply

`park_authorization` returns
`CriomeReply::AuthorizationPending(AuthorizationPending::new(slot, request_digest, Vec::new(), AuthorizationObservationToken::new(slot)))`.
`AuthorizationPending` (signal-criome/src/schema/lib.rs:958-963):
`request_slot`, `request_digest`, crate-private `pending_missing_authorities`
(empty for parked), `observation_token`. The client learns its slot from
this reply and observes by slot afterward.

### List-parked

Two read paths, both backed by `store::ReadAuthorizationSnapshot`:

- Working socket: `CriomeRequest::ObserveParkedAuthorizations` -> `root.parked_authorization_snapshot` -> `read_parked_authorization_snapshot` -> `CriomeReply::ParkedAuthorizationSnapshot`.
- Meta socket: `Input::ObserveParkedAuthorizations` -> `read_parked_authorization_snapshot` -> `Output::ParkedAuthorizationSnapshot`.

`read_parked_authorization_snapshot` (root.rs, last method in the
~500-516 block) asks `store::ReadAuthorizationSnapshot`, then
`filter_map`s: keep only `status == AuthorizationStatus::Parked`, and only
those whose `parked_evaluation()` is `Some`, mapping each to
`ParkedAuthorization { request_slot, evaluation }`
(signal-criome/src/schema/lib.rs:1035-1038). Result wrapped via
`ParkedAuthorizationSnapshot::from_parked`. The request payload
`ParkedAuthorizationObservation {}` is empty (lib.rs:1043) and is ignored
(`_request`); there is no per-slot or per-component filtering — every
parked record is returned. Sorted by slot string in
`store.rs::authorization_snapshot` (store.rs:448-456).

### Approve / reject / defer by slot

The only approve/reject/defer entry point is the **meta socket**
`Input::SubmitAuthorizationApproval(AuthorizationApproval)` ->
`root.record_authorization_approval`.

`AuthorizationApproval` (meta-signal-criome/src/schema/lib.rs:79-82):
`request_slot: AuthorizationRequestSlot`, `decision: AuthorizationApprovalDecision`.
`AuthorizationApprovalDecision { Approve, Reject, Defer }`
(meta-signal-criome/src/schema/lib.rs:70-75).

`record_authorization_approval` flow:
1. `lookup_authorization_state(request_slot)` -> `Option<AuthorizationStateRecord>`.
2. `None` -> records `recorded_decision = Reject` (unknown slot treated as reject; nothing stored).
3. `Some(state)` -> `apply_authorization_approval(state, decision)`, records the caller's decision.
4. Returns `Output::AuthorizationApprovalRecorded { request_slot, decision }`.

`apply_authorization_approval`:
- `Defer` -> early return; state stays `Parked`, nothing changes (no re-park, no timer).
- requires `state.parked_evaluation()` `Some`; else early return.
- `Approve` -> `publish_authorized_object_update(...)` with `EvaluationDecision::Authorized` (this is what wakes any authorized-object subscribers), then store a new state with `status = Granted`.
- `Reject` -> store state with `status = Denied` and `denial = Some(AuthorizationDenial { source: Policy, reason: PolicyRefused })`.
- The rebuilt `AuthorizationStateRecord` is written with empty missing-authorities and `None` grant but **re-attaches** the parked evaluation via `.with_parked_evaluation(evaluation)` — so a Granted/Denied record still carries its evaluation. (Consequence: it remains attached, but the snapshot filter only surfaces `Parked`, so it drops off the parked list once decided.)

Important asymmetry: **approve/reject/defer is meta-socket only.** There is
no working-socket request variant for client approval; the working socket
can park and observe but cannot decide. `RejectAuthorization` on the
working socket is the *signer* rejection path (source `Signers`), a
different mechanism from client `Reject` (source `Policy`).

## (c) Meta socket: Input variants and submit_meta dispatch

`meta_signal_criome::Input` has exactly three variants
(meta-signal-criome/src/schema/lib.rs:138-142):
- `Configure(CriomeDaemonConfiguration)`
- `ObserveParkedAuthorizations(ParkedAuthorizationObservation)`
- `SubmitAuthorizationApproval(AuthorizationApproval)`

`Output` has five (lib.rs:147-153, including two never emitted by the
daemon): `Configured`, `ParkedAuthorizationSnapshot`,
`AuthorizationApprovalRecorded`, `ConfigurationRejected`,
`RequestUnimplemented`.

`root.rs::submit_meta` dispatch:
- `Configure(configuration)` -> `self.configure(configuration)`.
- `ObserveParkedAuthorizations(request)` -> `Output::ParkedAuthorizationSnapshot(self.read_parked_authorization_snapshot(request))`.
- `SubmitAuthorizationApproval(approval)` -> `self.record_authorization_approval(approval)`.

`configure` (root.rs): sets `authorization_mode`, derives `cluster_root`
(`configuration.cluster_root().cloned().map(ClusterRoot::new)`), fire-and-forgets
`registry::ConfigureClusterRoot`, bumps `configuration_generation`, returns
`Output::configured(ConfigurationGeneration::new(self.configuration_generation))`.
Note: `configuration_generation` starts at 0 (root.rs:174 region) and is
bumped per `Configure`; the boot-time config (from the rkyv startup file)
does **not** go through `configure`/the meta socket — it is applied directly
in `from_configuration` + `CriomeRoot` args, so the first runtime `Configure`
returns generation 1.

`ConfigurationRejected` and `RequestUnimplemented` exist in the Output
schema but `submit_meta` never produces them — there is no reject/unimplemented
branch in the daemon's meta dispatch on this main.

## (d) src/transport.rs — UnixStream-only, codecs, frame shape

**Confirmed UnixStream-only.** The only network primitives in the whole
crate are `UnixStream::connect` at transport.rs:233 and :254 (the two
clients). No `TcpListener`/`TcpStream`/`SocketAddr` anywhere in `src/`
(grep clean). The daemon side (daemon.rs) binds `UnixListener` for both
sockets. There is no cross-host transport on this main — **E1 is unbuilt**.

Two codecs, structurally identical, differing only in payload type:
- `CriomeFrameCodec` (working): `read_request/write_request: CriomeRequest`, `read_reply/write_reply: CriomeReply`.
- `CriomeMetaFrameCodec` (meta): same shape over `meta_signal_criome::Input` / `Output`.

Both default to `maximum_frame_bytes = 1024 * 1024` (1 MiB), const-constructed.

**Frame shape:** length-prefixed. `read_frame`: read 4-byte big-endian u32
length prefix (`u32::from_be_bytes`), reject if `length > maximum_frame_bytes`,
then read `length` bytes; reconstructs the full buffer (prefix + body) and
calls `CriomeFrame::decode_length_prefixed(&bytes)` (the signal-frame
codec). `write_frame`: `frame.encode_length_prefixed()` then `write_all` +
`flush`. So the wire is `[4-byte BE length][rkyv-encoded signal-frame]`.

Frame body wrapping (working): a request becomes
`CriomeFrame::new(FrameBody::Request { exchange: synthetic_exchange(), request: request.into_request() })`;
a reply becomes `FrameBody::Reply { exchange, reply: Reply::committed(NonEmpty::single(SubReply::Ok(reply))) }`.
`synthetic_exchange()` is a fixed `ExchangeIdentifier::new(SessionEpoch::new(0), ExchangeLane::Connector, LaneSequence::first())`
— the same constant exchange on every frame (no session/sequence tracking).
Reading a reply unwraps `Reply::Accepted { per_operation }` -> first
`SubReply::Ok(payload)`; `Reply::Rejected { reason }` -> `Error::UnexpectedSignalFrame`.

Clients: `CriomeClient` (working) and `CriomeMetaClient` (meta), each
holding a socket path + codec. `send`: existence-check the socket path
(`Error::MissingSocket` if absent), `UnixStream::connect`, `BufReader`,
write request, read reply — one request/reply per connection, synchronous,
blocking. `CriomeClient::from_environment` reads `CRIOME_SOCKET` (default
`/tmp/criome.sock`). `CriomeMetaClient` has no `from_environment`.

**Not in transport (and relevant to p43g):** there is no `SO_PEERCRED`
read anywhere in the crate (grep for `peercred|SO_PEERCRED|ucred|getsockopt`
returns nothing). The connecting peer's Unix credential is never inspected;
the only access control on either socket is the 0600 file mode set in
`daemon.rs::bind_private_socket` (`Permissions::from_mode(0o600)`). The
"authenticated by SO_PEERCRED" half of governing decision p43g is **not
yet implemented** — see open questions.

## (e) Actor topology and the peer-signature actor flow

### Topology

`src/actors/mod.rs` modules: `authorization`, `registry`, `root`, `signer`,
`store`, `subscription`, `verifier`. `CriomeRoot` (root.rs:30-39) holds
`ActorRef`s to `registry`, `signer`, `verifier`, `authorization`,
`subscription`, `store` plus `authorization_mode` and
`configuration_generation`.

Spawn graph in `CriomeRoot::on_start` (root.rs), all supervised by root:
1. `StoreKernel` (`store`) — opened on the store location; the only
   persistence actor.
2. `IdentityRegistry` (`registry`) — `Arguments { store, cluster_root }`.
3. master-key reconciliation: load/generate `MasterKey` from
   `<store>.masterkey`; resolve criome's own `Identity::host("criome")`;
   if registered, the stored public key MUST match the master key or
   startup fails (`Error::Startup`, "mismatched key"); if absent, register
   criome's identity directly to the store (bypassing the cluster-root
   gate), `KeyPurpose::CriomeRoot`.
4. `AttestationSigner` (`signer`) — `{ registry, store, master_key, criome_identity }`.
5. `AttestationVerifier` (`verifier`) — `{ registry }`.
6. `AuthorizationCoordinator` (`authorization`) — `{ store }` (holds an
   `AuthorizationClock::system()` over `UNIX_EPOCH`).
7. `SubscriptionRegistry` (`subscription`) — `{ registry }`.

`CriomeRoot::Error = Error` (startup can fail typed); the other actors use
`Error = Infallible` (e.g. `AuthorizationCoordinator`, authorization.rs).
`ReadTopology` always reports `CriomeTopology::complete()` (all five legs
true) — it is a liveness ack, not a real probe.

### Peer-signature actor flow: RouteSignatureRequest / SubmitSignature

Both are working-socket requests routed root -> coordinator:

- `CriomeRequest::RouteSignatureRequest(SignatureSolicitationRoute)` -> `ask_authorization(authorization::RouteSignatureRequest::new(route))` (root.rs:231-233).
- `CriomeRequest::SubmitSignature(SignatureSubmission)` -> `ask_authorization(authorization::SubmitSignature::new(submission))`.

`AuthorizationCoordinator::route_signature_request` (authorization.rs):
takes `route.solicitation.request_slot` + `route.routed_to`, calls
`store_signature_solicitation(route)`; on success returns
`CriomeReply::SignatureRouteReceipt { request_slot, routed_to }`, on store
error `rejection(MalformedRequest)`. `SignatureSolicitationRoute`
(signal-criome/src/schema/lib.rs:895-898): `{ solicitation: SignatureSolicitation, routed_to: Identity }`.

`AuthorizationCoordinator::submit_signature` (authorization.rs): takes
`submission.request_slot` + `submission.signer`, calls
`store_signature_submission(submission)`; returns
`SignatureSubmissionReceipt { request_slot, signer }`.
`SignatureSubmission` (lib.rs:903-907): `{ request_slot, signer: Identity, signature: StampedSignatureEnvelope }`.

Persistence: `store_signature_solicitation` / `store_signature_submission`
in store.rs write to tables `signature_solicitations` and
`submitted_signatures` (tables.rs `put_signature_solicitation` /
`put_signature_submission`). Keys: solicitation `"<slot>:<Kind:name>"`
(`SignatureSolicitationKey`, tables.rs:708-721); submission
`"<slot>:<Kind:name>"` keyed by signer (`SignatureSubmissionKey`,
tables.rs:726-739).

**Wired vs dormant:** the ingress half is fully wired — a peer can route a
solicitation and submit a signature, both persist and ack. The **consuming
half is dormant**: nothing reads `submitted_signatures` back. Grep for
readers of the submission table shows only writers
(`put_signature_submission` / `store_signature_submission`) and reply
plumbing; there is no `read`/snapshot of submitted signatures, no quorum
tally, no aggregate-verify, and `evaluate_authorization`'s `Quorum` branch
calls `store.evaluate(&contract, &evidence, &registry)` using the evidence
signatures carried **in the request**, not any stored peer submissions. So
`RouteSignatureRequest`/`SubmitSignature` form a store-only inbox with no
path back into a verdict on this main. (E3 multi-machine quorum and E6
aggregate-verify are the missing consumers.)

`AuthorizationGrant` (lib.rs:931-943) is a fully-specified grant type
(carries `authorization_grant_signatures`, `policy_satisfaction`,
`signature_result`, `issued_by`, `issued_at`, expiry) but on this main no
code path **mints** a `Grant` into a state record — `apply_authorization_approval`
and `reject_authorization` both write `grant = None`. `verify_authorization`
returns `AuthorizationGranted(verification.authorization)` echoing a grant
the caller supplied; it does not produce one.

## Daemon binding and startup argument (supporting facts)

- Binds two `UnixListener`s: working `socket` and `meta_socket`, both 0600 (`daemon.rs::bind_private_socket`).
- Default meta socket path = `<socket>.meta` (`default_meta_socket_path`).
- `serve_forever`: both listeners set non-blocking; a 10ms-sleep poll loop alternately drains working then meta connections. One request/reply per accepted connection (`handle_connection` / `handle_meta_connection`), each `runtime.block_on`-ing a single `root.ask`.
- Startup argument: `CriomeDaemonCommand::configuration` requires `ComponentArgument::SignalFile` (rkyv) and **rejects** `InlineNota` / `NotaFile` (`triad_runtime::ArgumentError::ExpectedSignalFile`) — daemon never parses NOTA, consistent with the binary-only daemon rule. `CriomeDaemonConfigurationFile::configuration` decodes via `CriomeDaemonConfiguration::from_rkyv_bytes`.
- Config arrives by **two** routes: (1) boot, from the rkyv startup file -> `from_configuration` (applied directly, not via `configure`); (2) runtime, via meta `Configure` -> `configure` (bumps generation). The thin NOTA CLI (`CriomeCommandLine`, feature `nota-text`) is the daemon's first client over the working socket, separate from the daemon binary.

## Quick reference: where each mode is decided

| Mode | Branch site | Effect |
|---|---|---|
| `AutoApprove` | `root.rs evaluate_authorization` | immediate `Authorized`, publishes update |
| `ClientApproval` | `root.rs evaluate_authorization` -> `park_authorization` | store `Parked` + `AuthorizationPending`; decided later via meta `SubmitAuthorizationApproval` |
| `Quorum` (default) | `root.rs evaluate_authorization` fallthrough | `store.evaluate(contract, evidence-in-request, registry)`; in-request signatures only |
