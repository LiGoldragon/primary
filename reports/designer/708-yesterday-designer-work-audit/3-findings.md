# 708-3 — Findings (adversarially verified)

55 raw findings → **37 confirmed** after adversarial verification (each
non-low finding handed to a skeptic who read the real code and defaulted to
*refuted*); 6 refuted, 12 low-severity nits excluded. Corrected severity
distribution: **15 high, 22 medium**.

The narrative below curates the highest-signal findings with full harm + fix.
A **complete index of all 37** follows at the end so nothing confirmed is
dropped — it includes several high-severity items the narrative omits (the
egui dead meta-socket wing, the meta-signal-orchestrate hand-rolled codec,
the orchestrate live-store hard-fail, the signal-orchestrate codegen-mirror
field-name disagreement, and the zero-coverage peer/worktree contract deltas).

## High

- **[gap] gc0n approval card / answer-a-question ability still does not exist on main — egui remains strictly view-only** — `mentci-egui src/app.rs:64-84, 164-169` — Report 707-1/707-4 named the approval card (the gc0n EscalateToPsyche surface made real) the highest-value deliverable and the whole reason for re-founding mentci-lib. The shared model now fully supports answering — `UserEvent` has `SelectQuestion`/`AnswerQuestion`/`ProposeEditedAnswer`, `ApprovalModel` exposes `answer()`/`select()`/`verdict_for_selected()`, and `ApprovalView` carries `current: Option<ApprovalQuestion>` with the real pending question text — but egui consumes none of it: the only `UserEvent` it emits is `Observe`, and the header paints only the pending/answered integers. The keystone deliverable is unbuilt at the one surface the psyche actually touches. — *fix:* render the `current` question and wire a control that emits `AnswerQuestion`/`ProposeEditedAnswer`, replacing the two-count summary with the live approval card the shared model already backs.

## Medium

- **[gap] The criome verdict-by-slot path (the headline t00s deliverable) is unwired and unwireable as built** — `mentci-lib src/observation.rs:165-173, src/cmd.rs:32-34, src/decision.rs:33-38` — `CriomeVerdict::from_decision` and `Cmd::SubmitCriomeVerdict` both exist, but `Cmd::SubmitCriomeVerdict` is constructed nowhere and `CriomeVerdict` is never produced in the model; `on_user_event(AnswerQuestion)` routes every verdict to the Mentci socket with no criome branch. It cannot even be wired with current data: signal-mentci's `ApprovalSource::CriomeEscalation` carries no `AuthorizationRequestSlot`, so an answered question has no slot to build a `CriomeVerdict` from. The keystone's central control deliverable is two dead building blocks with no plumbing between them, and nothing flags the gap. — *fix:* either close the signal-mentci `ApprovalSource` cross-import so `CriomeEscalation` carries the slot and have `AnswerQuestion` emit `Cmd::SubmitCriomeVerdict { CriomeVerdict::from_decision(slot, decision) }` for criome-sourced questions, or, if the daemon's `criome_bridge` keeps owning the slot lookup, delete `Cmd::SubmitCriomeVerdict` here and document `CriomeVerdict` as a pure mapping the daemon imports. Pick one; do not ship both half-built.

```rust
UserEvent::AnswerQuestion { verdict } => {
    let socket = ComponentSocketKind::Mentci;
    let outcome = self.approval.answer(verdict.clone());
    if outcome.verdict().is_some() {
        vec![Cmd::send(socket, MentciRequest::AnswerQuestion(verdict))]  // always Mentci, never criome
```

- **[gap] The criome approval loop is half-open: answering a criome-sourced question in the daemon never routes the verdict back to criome** — `mentci src/state.rs:155-178 vs src/daemon.rs:162-176` — The daemon folds parked criome `ClientApproval` requests into its own pending-question queue via `absorb_criome_parked_authorizations`, but when a client answers one, `State::answer` only removes the question and stores the verdict locally — it never calls `criome_bridge.submit_decision`/`submit_verdict` (State has no bridge handle, and `StateOwner::handle` ignores it after answering). A psyche who approves a criome escalation through the daemon's own answer path gets `VerdictAccepted` while criome is never told and the parked request stays parked forever; the advertised park → question → verdict → grant chain is closed only by the separate `criome:approve:<slot>` CLI atom. — *fix:* store the `AuthorizationRequestSlot` on the question/state (not just in `into_question_proposal`'s context body) and, when a removed question has `ApprovalSource::CriomeEscalation`, have the actor call `criome_bridge.submit_verdict` by slot. Add an integration test that answers the minted criome question via `AnswerQuestion` and asserts criome records the grant.

- **[gap] `submit_verdict` — the entire subject of the capstone "use shared criome verdict mapping" commit — is dead in the daemon runtime** — `mentci src/criome_bridge.rs:35-45` — The capstone deleted `map_decision` and adopted `mentci_lib::CriomeVerdict::from_decision` inside `submit_verdict`, framed as hardening the shared-model integration, but `submit_verdict` has exactly one caller in the whole workspace: the integration test. No daemon path and no CLI path invokes it (the CLI calls `submit_decision` directly with an already-typed decision), so the `ApprovalDecision → AuthorizationApprovalDecision` projection — the only consumer of `from_decision` in this repo — runs only under `cargo test`. The commit's headline value is not realized on main. — *fix:* make `submit_verdict` the real answer-path sink (per the half-open-loop finding) so `from_decision` runs in production, or delete `submit_verdict` and build the `CriomeVerdict` directly in the answer path.

- **[gap] RetractObservation emits the Cmd but never clears the local slot, so the model keeps a token it just retracted** — `mentci-lib src/observation.rs:153-158` — After retract, `slot.token`/`slot.latest`/`slot.liveness` are untouched, so `socket(kind).token()` still returns the retracted token and liveness stays `Connected`. A later `InterfaceStateChanged` push for that token still passes the `on_engine_event` token-equality guard and is folded as live state — exactly the "fold foreign state" case that guard exists to prevent, defeated by stale local state. Because `Observe` sets liveness locally but close does not, the open/close asymmetry is also surprising. — *fix:* on `RetractObservation` clear the matching slot (`token=None`, `liveness=Disconnected`), gating on whether the supplied token matches the held one (the swallowed `UnknownSubscription` path). Add a test: retract then push-on-old-token must be ignored.

- **[gap] The focus delta's six reader methods have zero test coverage** — `signal-mentci tests/round_trip.rs (all 5 tests); methods at src/lib.rs:109-164` — The entire purpose of commit `58dd5a2` was to add public readers piercing `pub(crate)` wrappers so mentci-lib can project state it did not build, yet none of `pending_questions()`/`notification()`/`panes()`/`questions()`/`suggested_answer()`/`context()` is called by any test. `pending_questions()` holds the only real logic in the hand-written surface — a 4-arm match — and the `FullProjection`-vs-`PendingQuestionsProjection` equivalence (both must yield the same slice for a given question set) plus the double-indirection in `PendingQuestionsView::questions` are exactly what silently regresses. The 5 existing tests assert only frame/NOTA round-trips, never that a reader returns what was put in. — *fix:* add a test constructing a `FullProjection` and a `PendingQuestionsProjection` over the same `approval_question()` and assert `pending_questions()` returns a 1-element slice in both cases and empty for Status/Notification; likewise assert the other readers echo their constructor inputs.

- **[unmerged-idea] Local StandardSocket/ComponentKind kept (and a third local enum added) although signal-standard now exists and 707 §3.5 said to collapse to imports** — `meta-signal-mentci schema/lib.schema:34-47,93-145; src/schema/lib.rs:39,53-95` — The schema's stated reason for the local stand-ins — "signal-standard is not yet a crate" — is now false: signal-standard exists on main with both `ComponentKind` and `StandardSocket`, and router already consumes it. The most recent delta was authored after signal-standard landed and after the design that directs collapsing to imports, yet kept all local declarations and added a new local `ComponentSocketKind`. The shapes have already diverged — this crate's `StandardSocket(SocketPath)` newtype versus signal-standard's two-variant enum — so the hand-written `StandardSocket::unix(path)` constructor will not survive the import, and consumer code written now is wrong on arrival. — *fix:* collapse the local `StandardSocket` + `ComponentKind` into signal-standard imports now, re-express `ComponentSocket`'s socket field as the imported enum, and rewrite `StandardSocket::unix` as a `UnixSocket`-variant constructor. If the import genuinely cannot land this cycle, correct the schema comment to state the real blocker, not the false one.

- **[gap] INTENT.md and ARCHITECTURE.md not updated for the focal socket-shape change; INTENT still describes the retired two-socket model** — `meta-signal-mentci INTENT.md:6-9; ARCHITECTURE.md:11-13` — The delta replaced the two positional fields `socket_path`/`home_criome_socket` with a single typed `Vec<ComponentSocket>`, but touched only schema + generated + tests. INTENT.md still describes exactly the retired shape ("where to listen, which home criome socket") — documenting a contract the code no longer has, the most misleading kind of stale doc — and ARCHITECTURE.md's owned-types list omits the delta's headline `ComponentSocket`/`ComponentSocketKind` entirely, giving no account of the multi-component generalization that is the whole point of the change. AGENTS.md requires updating INTENT.md on the same branch as work affecting landed intent. — *fix:* rewrite the INTENT.md sentence to describe typed `component_sockets` (N self-describing component/channel endpoints) and add `ComponentSocket`/`ComponentSocketKind` to ARCHITECTURE.md's owned list.

- **[gap] Observe-time criome poll swallows all bridge errors into an empty result** — `mentci src/daemon.rs:130-141` — `parked_authorizations().map(...).unwrap_or_default()` means that if criome's meta socket is down, misconfigured, or returns `UnexpectedCriomeMetaReply`, the daemon silently returns zero parked authorizations and projects interface state as if criome had nothing pending. A psyche sees an empty queue indistinguishable from "criome is up and idle" — a security-relevant approval surface failing open and silent. `Error::UnexpectedCriomeMetaReply`/`Error::Criome` are constructed only to be discarded here. — *fix:* surface the bridge failure — at minimum log it; better, fold a degraded/notification state into the projection so absence of questions is never confused with criome being unreachable.

```rust
self.criome_bridge.parked_authorizations()
    .map(|s| s.into_parked())
    .unwrap_or_default()   // criome down == criome idle, silently
```

## Low

- **[dead-code] The entire error.rs module is never produced** — `mentci-lib src/error.rs:1-66, src/lib.rs:42` — No method in the crate returns `Result` or constructs any `Error::` variant; every model method returns `Vec<Cmd>`, `Option`, or `bool`. The five variants name exactly the failures the model instead swallows silently, and `dead_code` does not fire because the items are `pub`. INTENT.md/ARCHITECTURE.md advertise a "typed per-crate Error" as a discipline win, but it is decorative — a module that satisfies a checklist rather than being used. — *fix:* convert the silent-swallow paths to return `Result`/`Error`, or delete error.rs if the model is genuinely infallible; a `pub` error enum the crate never returns misleads consumers into thinking there is a typed failure surface.

- **[gap] Error paths are swallowed: answering/pushing/retracting an unknown id returns empty Vec with no signal** — `mentci-lib src/observation.rs:159-164,197-210; src/approval.rs:241-248,262-272` — Three failures are indistinguishable from success-with-no-effect: `answer` on an unknown question returns an all-`None` outcome mapped to empty `Vec<Cmd>`; `select` on a non-pending id returns empty; `InterfaceStateChanged` for an unheld token returns empty. The `error.rs` variants `UnknownQuestion`/`UnknownSubscription` were written for these paths but never wired. A control surface that drops a psyche's verdict because the queue moved, with zero signal, is a correctness hazard. — *fix:* return the typed `Error` for the unknown-question/unknown-token cases or surface a typed rejection the caller can branch on; add a test asserting answer-of-unknown is observably distinct from answer-accepted.

- **[unmerged-idea] ARCHITECTURE.md still describes a `[patch]` scaffold and unmerged signal-mentci readers that have already landed** — `mentci-lib ARCHITECTURE.md:126-135, Cargo.toml:10-18` — Cargo.toml has no `[patch]` section and the crate builds clean against `branch = main` git deps (verified `cargo build --offline` succeeds, `pending_questions()` resolves from signal-mentci main). The "Scaffold note (designer prototype)" section is stale post-integration documentation: it tells a future reader to look for a `[patch]` that isn't there and implies the crate doesn't build standalone, which is false. — *fix:* delete the scaffold-note section; while there, reconcile the "Adoption" section's future-tense `CriomeVerdict`-adoption claims with the slot gap above.

- **[unmerged-idea] `ApprovalModel::receive` (single-question push) is implemented and public but no event ever drives it** — `mentci-lib src/approval.rs:230-238, src/observation.rs:211-218` — `receive()` exists for "when a single question push arrives rather than a whole projection" and emits a `QuestionReceived` delivery, but `on_engine_event` handles `QuestionPresented` by doing nothing and waiting for the next full `InterfaceStateChanged` to re-fold. The single-push fan-out is built and tested only in isolation; the model never calls it, and `ApprovalUpdate::QuestionReceived` originates only from this dead caller. — *fix:* wire `on_engine_event(QuestionPresented)` to call `approval.receive`, or remove `receive()` + `ApprovalUpdate::QuestionReceived` if the model is snapshot-only by design.

- **[dead-code] ComponentLabel newtype is dead — declared, accessor-decorated, referenced by nothing** — `signal-mentci schema/lib.schema:98; src/schema/lib.rs:69,749,761; src/lib.rs:51` — `ComponentLabel` has existed since genesis and is used by no struct, enum variant, operation root, or reply anywhere in the schema; its only occurrences are the declaration plus generated boilerplate. Worse, it propagated into the hand-written surface — it sits in the `string_accessor!` list, so a human deliberately wrote an `as_str()` reader for a type no message can carry, leftover masquerading as live API. Component labeling lives in meta-signal-mentci, not here. — *fix:* delete the `ComponentLabel` line from the schema, regenerate, and drop it from the `string_accessor!` list; reintroduce attached to a field only if a component label genuinely belongs on the working contract later.

- **[gap] Schema doc comment still names the deleted InterfaceStateSnapshot type** — `signal-mentci schema/lib.schema:276` — Commit `d0fea7b` replaced `Output::InterfaceStateSnapshot(ProjectedInterfaceState)` with `InterfaceObservationOpened { token, state }`, so `InterfaceStateSnapshot` no longer exists anywhere except this comment, which still documents `ProjectedInterfaceState` as "the InterfaceStateSnapshot reply payload." For a contract repo whose schema source is the authoritative human-readable spec, a future reader finds nothing — or reintroduces the removed type. — *fix:* edit the comment to say the projected state is carried by the `InterfaceObservationOpened` reply (token + first snapshot) and re-emitted in `MentciEvent::InterfaceStateChanged`; a contract reshape must update the schema prose, not just the lowered struct.

- **[gap] `component_socket(kind)` silently returns the first match; nothing enforces or documents one-socket-per-kind** — `meta-signal-mentci src/lib.rs:67-71` — The configuration models sockets as `Vec<ComponentSocket>`, so two entries with `kind == Mentci` are representable and round-trip cleanly, and the only consumer resolves by `find`, silently taking the first. For a daemon that indexes sockets by lane to decide who it trusts and dials, a duplicate-kind config is an error that should be caught, not silently resolved; the contract advertises a by-kind lookup as if `kind` were a key while the type gives no uniqueness guarantee. — *fix:* make `kind` a real key (a map-shaped newtype, or distinct optional fields per lane), or keep the Vec but have daemon-config validation reject duplicate kinds with `ConfigurationRejectionReason::MalformedConfiguration` and document the invariant; at minimum a doc comment stating first-wins behavior.

- **[ugly-pattern] Stringly-typed criome slot set and subscription map discard existing newtypes** — `mentci src/state.rs:19,28; slot_key at src/state.rs:289-291` — Both `AuthorizationRequestSlot` and `SubscriptionToken` are real typed-domain values, yet the dedup set stores raw `String` slot payloads (`BTreeSet<String>`) and the subscription map keys on `token.as_str().to_owned()`. This violates the typed-domain-values rule, loses the type at the exact boundary where slot identity matters for dedup, and forces `slot_key` to unwrap the newtype back to a `String`. — *fix:* make `criome_request_slots` a `BTreeSet<AuthorizationRequestSlot>` and key `subscriptions` by `SubscriptionToken` (derive `Ord` on the newtypes); `slot_key` returns the typed slot.

- **[unmerged-idea] Daemon adopted only mentci-lib's verdict mapping; the shared NOTA renderer was dropped, leaving Debug-format `{:?}` in question context** — `mentci src/state.rs:293-320` — 707-1 §3.1 specified mentci-lib owning one NOTA-fallback renderer (`RenderNota`) so the daemon's `format!("{:?}", ...)` and the GUI's ad-hoc `to_nota` collapse into it, and mentci-lib was re-founded with exactly that. The integration picked up only `CriomeVerdict` and left the criome-question context rendered via Rust `Debug` — a non-NOTA, non-stable, unreadable projection of contract/component/kind/digest into a human-facing approval card, with byte-array Debug noise on `ObjectDigest`. This is the readability payoff the whole 707 effort targeted, dropped in integration. — *fix:* depend on mentci-lib's `RenderNota` and render the parked evaluation's contract/object through it; flag that the daemon consumes mentci-lib for one type only while the renderer leg is still unmerged.

- **[gap] Defer accepts a verdict for a question that does not exist** — `mentci src/state.rs:155-162` — The `Defer` branch returns `VerdictAccepted` before the pending-question existence check that approve/reject perform, so `AnswerQuestion(Defer)` for a fabricated or already-answered id is accepted while the same id under Approve/Reject is correctly rejected with `UnknownQuestion`. A client gets `VerdictAccepted` for nothing, and the criome relay (once wired) would have no slot to act on. — *fix:* do the pending-question lookup first for all decisions, then branch on Defer (keep open) vs Approve/Reject (remove + record); add a test that Defer on an unknown question rejects.

- **[rust-discipline] Synchronous blocking criome network round-trip on the connection thread, ahead of the actor** — `mentci src/daemon.rs:104-141` — Every `ObserveInterfaceState` does a blocking synchronous send to criome's meta socket on the accept loop's connection thread before the actor message is even built. Since `serve_forever` handles connections one at a time, a slow or hung criome meta socket stalls the entire daemon's accept loop; the actor boundary exists precisely to keep I/O off the state owner, but the criome I/O is hoisted in front of it onto the single-threaded serial server — the no-blocking-in-the-hot-path discipline inverted. — *fix:* move the criome poll into an async task (the runtime is already present) so it does not serialize the accept loop, or run the bridge poll concurrently and merge; longer term the §3.4 continuous-subscription loop replaces this per-observe poll entirely.

Verification note: 6 findings were refuted during adversarial verification and removed; 12 additional low-severity nits were not verified and are excluded from this report.

## By category (all 37 confirmed)

| category | count |
|---|---|
| gap | 19 |
| unmerged-idea | 5 |
| dead-code | 4 |
| ugly-pattern | 4 |
| repetition | 4 |
| rust-discipline | 1 |

## Complete confirmed-findings index (all 37)

Every adversarially-confirmed finding, grouped by repo. The narrative above
curates the highest-signal subset with fixes; this index guarantees nothing
confirmed is dropped. Severity is the verifier's corrected value where it differs.

### mentci (7)

| sev | category | finding | location |
|---|---|---|---|
| high | gap | The criome approval loop is half-open: answering a criome-sourced question in the daemon never routes the verdict back to criome | `src/state.rs:155-178 (answer) vs src/daemon.rs:162-176 (StateOwner::handle)` |
| high | gap | submit_verdict — the entire subject of the capstone 'use shared criome verdict mapping' commit — is dead in the daemon runtime | `src/criome_bridge.rs:35-45; only caller is tests/criome_bridge.rs:450` |
| medium | gap | Defer accepts a verdict for a question that does not exist | `src/state.rs:155-162 (answer, Defer branch)` |
| medium | gap | Observe-time criome poll swallows all bridge errors into an empty result | `src/daemon.rs:130-141 (parked_authorizations_for_request)` |
| medium | rust-discipline | Synchronous blocking criome network round-trip on the connection thread, ahead of the actor | `src/daemon.rs:104-141` |
| medium | ugly-pattern | Stringly-typed criome slot set and subscription map discard existing newtypes | `src/state.rs:19,28; slot_key at src/state.rs:289-291` |
| medium | unmerged-idea | Daemon adopted only mentci-lib's verdict mapping; the shared NOTA renderer was dropped, leaving Debug-format {:?} in question context | `src/state.rs:293-320 (into_question_proposal)` |

### mentci-egui (6)

| sev | category | finding | location |
|---|---|---|---|
| high | dead-code | Entire meta-socket + legacy NOTA-transcript wing is dead, hidden from the linter by pub export | `src/daemon_client.rs:55-65, 68-86, 108-116, 152-166, 207-215; DaemonTranscriptEntry 26-33` |
| high | gap | gc0n approval card / answer-a-question ability still does not exist on main — egui remains strictly view-only | `src/app.rs:64-84, 164-169` |
| high | ugly-pattern | Model's authoritative Cmd is dropped; the shell hand-rebuilds the request, defeating the MVU contract | `src/app.rs:72-83` |
| medium | gap | Live subscription absent — single one-shot Observe, no InterfaceStateChanged consumption, polling repaint | `src/app.rs:56-62, 197-224, 213` |
| medium | repetition | Crate-local SocketKind enum duplicates mentci_lib::ComponentSocketKind | `src/daemon_client.rs:35-39 + impl 218-225` |
| medium | ugly-pattern | ObservationEntry.operation is stringly-typed despite a closed contract enum being in hand | `src/app.rs:22-25, 110-113, 118-128` |

### mentci-lib (6)

| sev | category | finding | location |
|---|---|---|---|
| high | dead-code | The entire error.rs module (Error, Result, constructors) is never produced | `src/error.rs:1-66, src/lib.rs:42` |
| high | gap | The criome verdict-by-slot path (the headline t00s deliverable) is unwired and unwireable as built | `src/observation.rs:165-173, src/cmd.rs:32-34, src/decision.rs:33-38` |
| high | gap | Error paths are swallowed: answering/pushing/retracting an unknown id returns empty Vec with no signal | `src/observation.rs:159-164, 197-210; src/approval.rs:241-248, 262-272` |
| medium | gap | RetractObservation emits the Cmd but never clears the local slot, so the model keeps a token it just retracted | `src/observation.rs:153-158` |
| medium | unmerged-idea | ARCHITECTURE.md still describes a [patch] scaffold and unmerged signal-mentci readers that have already landed | `ARCHITECTURE.md:126-135, Cargo.toml:10-18` |
| medium | unmerged-idea | ApprovalModel::receive (single-question push) is implemented and public but no event ever drives it | `src/approval.rs:230-238, src/observation.rs:211-218` |

### meta-signal-mentci (3)

| sev | category | finding | location |
|---|---|---|---|
| high | unmerged-idea | Local StandardSocket/ComponentKind kept (and a third local enum added) although signal-standard now exists and 707 §3.5 said to collapse to imports | `schema/lib.schema:34-47,93-145; src/schema/lib.rs:39,53-95` |
| medium | gap | INTENT.md and ARCHITECTURE.md not updated for the focal socket-shape change; INTENT still describes the retired two-socket model | `INTENT.md:6-9; ARCHITECTURE.md:11-13` |
| medium | gap | component_socket(kind) silently returns the first match; nothing enforces or documents one-socket-per-kind | `src/lib.rs:67-71` |

### meta-signal-orchestrate (2)

| sev | category | finding | location |
|---|---|---|---|
| high | ugly-pattern | Hand-rolled NOTA codec on WorktreeIndexRefreshed is unnecessary AND disagrees with its own generated schema | `src/lib.rs:160-179 (and copied original at 126-148)` |
| medium | gap | The four new worktree types have zero round-trip test coverage | `tests/round_trip.rs:92-180` |

### orchestrate (4)

| sev | category | finding | location |
|---|---|---|---|
| high | gap | Schema-version 2->3 bump rebakes EVERY family hash, so opening the live store hard-fails (no migration in the daemon) | `src/tables.rs:44, 167-179, 41-43` |
| high | unmerged-idea | The entire eh5a worktree lifecycle (merge/archive/recycle) is unreachable — Merged/Archived/Recycled can never be set | `src/execution.rs:441-452; variants only in projection bridges 1189-1203` |
| medium | dead-code | Three unused worktree items: From<WirePath> for WorktreePathProbe, worktree_record, and derive_owning_lane is a constant-returning stub | `src/worktree.rs:282-286, 153-155; src/tables.rs:270-279` |
| medium | repetition | WorktreePathProbe re-shells jj instead of reusing orchestrate-cli's verify_jj — two divergent jj probers now exist | `src/worktree.rs:158-280 vs primary/orchestrate-cli/src/verify_jj.rs` |

### signal-criome (3)

| sev | category | finding | location |
|---|---|---|---|
| high | gap | Entire peer delta has ZERO test coverage in a crate whose only job is wire fidelity | `signal-criome-peers/tests/round_trip.rs (no peer refs); tests/canonical_examples.rs (none)` |
| medium | gap | Tests and negative guardrails are feature-gated, so default `cargo test` runs zero of them | `signal-criome-peers/Cargo.toml:14-22 ([[test]] required-features=[nota-text], default=[])` |
| medium | repetition | PeerNode::new and PeerEnvelope::new are pure-passthrough boilerplate that break the crate's own ::new convention | `signal-criome-peers/src/lib.rs:206-230` |

### signal-mentci (3)

| sev | category | finding | location |
|---|---|---|---|
| high | gap | The focus delta's six reader methods have zero test coverage | `tests/round_trip.rs (all 5 tests); methods at src/lib.rs:109-164` |
| medium | dead-code | ComponentLabel newtype is dead — declared, accessor-decorated, referenced by nothing | `schema/lib.schema:98; src/schema/lib.rs:69,749,761; src/lib.rs:51` |
| medium | gap | Schema doc comment still names the deleted InterfaceStateSnapshot type | `schema/lib.schema:276` |

### signal-orchestrate (3)

| sev | category | finding | location |
|---|---|---|---|
| high | gap | Generated mirror and canonical struct disagree on the Worktree status field name — `worktree_status` vs `status` | `src/schema/lib.rs:182 vs src/lib.rs:617; root cause schema/lib.schema:45` |
| medium | gap | Entire worktree vocabulary ships with zero test coverage in a crate whose only job is wire round-trip fidelity | `tests/round_trip.rs (32 tests, none worktree); tests/schema_contract.rs` |
| medium | repetition | LaneName and PurposeText are byte-for-byte copies of LaneIdentifier and ScopeReason validation — divergent copy, not faithful reuse | `src/lib.rs:461-509, 514-556 duplicating 283-341, 815-857` |
