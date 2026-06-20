# 9 — Synthesis: what to build for a working mentci↔criome approval UI

## Top gaps (priority)

| Severity | Gap | Why |
|---|---|---|
| blocker | criome never parks an escalation — EscalateToPsyche drops the AuthorizationEvaluation (object+evidence) and stores nothing | The goal's core mechanic does not exist on the criome side. record_evaluation_decision publishes only on Authorized (root.rs:336); EscalateToPsyche returns AuthorizationEvaluated{contract,decision} and forgets the submission. There is no parked record for mentci to list and nothing for a later verdict to reference. Without a held, addressable evaluation the park-then-authorize loop cannot run over two sockets. |
| blocker | Nothing maps a criome escalation into a mentci question or carries the evaluation back — the only working loop is a single-process test sharing one Rust variable | CriomeApprovalBridge exposes only configure()+submit_verdict() and is never called from any binary; submit_verdict REQUIRES the caller to already hold the AuthorizationEvaluation. mentci state never stores one; ApprovalQuestion/QuestionProposal/ApprovalVerdict carry no criome reference. The test (criome_bridge.rs:316-371) closes the loop only because one process holds `evaluation` twice. In two live daemons no code knows which mentci verdict answers which criome escalation. |
| blocker | The mentci CLI is not a UI — one-shot client, single hand-authored NOTA argument, raw binary output, no verbs | client.rs:49-58 connects, writes one frame, reads one binary reply, exits. The single argument is parsed straight into a full MentciRequest (client.rs:80-86) and output is a raw length-prefixed frame (client.rs:55-56). A human cannot see parked questions, cannot learn the daemon-minted QuestionIdentifier, and cannot approve without hand-authoring the exact AnswerQuestion(ApprovalVerdict(...)) record. This is the single largest barrier between today's code and a working approval UI. |
| blocker | criome has no client-approval/park mode and no discovery surface for parked submissions | AuthorizationMode is the closed enum [Quorum AutoApprove] (signal-criome lib.rs:247-250); no variant parks every submission. EvaluateAuthorization is request/reply with no Parked{id} reply, no list-all, no observe over escalations; authorization_snapshot() exists but no CriomeRequest routes to it. The goal's 'client approval mode' and the human's 'show parked submissions' both map to nothing on the wire. |
| blocker | Meta-approval is content-replay, not answer-by-id; the answerer must re-supply the full evaluation criome already evaluated | AuthorizationApproval{evaluation, decision} carries the entire AuthorizationEvaluation by value (meta-signal-criome lib.schema:46-49); record_authorization_approval re-checks the digest locally and never looks up a parked slot (root.rs:351-383). Over two real sockets mentci has no source for the Evidence/AttestedMoment/AuthorizedObjectReference, so genuine cross-process approve-by-id is impossible on this contract. A working answer-by-slot pattern already exists on the signing flow (authorization.rs:104-158) and should be reused. |

## The shape of the gap

The psyche wants a loop that runs end-to-end over two live Unix sockets: a human types `mentci approve <id>` on a CLI, the verdict reaches `mentci-daemon`, the daemon forwards it to a running `criome` that had **parked** a submission, and criome then authorizes. Today that loop runs in exactly one place — `mentci/tests/criome_bridge.rs`, a single `#[test]` that starts both daemons inside one process and hand-carries an `AuthorizationEvaluation` Rust variable across every hop. Erase that test's shared local variable and the loop has no spine.

The 38 confirmed findings collapse into one structural truth that recurs at every layer: **the `AuthorizationEvaluation` — the typed object criome must re-authorize — is never persisted, never put on the wire, and never threaded through any contract.** criome forgets it the instant it escalates; the signal-mentci question type has no field to hold it; mentci's daemon state has no slot for it; and criome's meta-approval contract forces the answerer to re-supply the entire evaluation by value. The test "works" only because one process owns the object twice. So the build is not a wiring task on top of a working substrate — the substrate (a parked, addressable-by-id evaluation) does not exist on either side.

A second truth: **the `mentci` CLI is not a UI at all.** It is a one-shot `connect → write one frame → read one binary reply → exit` client (`mentci/src/client.rs:49-58`) whose single argument must be a complete, hand-authored NOTA `MentciRequest` (`client.rs:60-65, 80-86`), and whose output is a raw length-prefixed binary frame dumped to stdout (`client.rs:55-56`). There is no verb, no rendering, no list, no watch. A human cannot read what is parked, cannot learn the daemon-minted `QuestionIdentifier`, and cannot approve without hand-writing the exact `AnswerQuestion(ApprovalVerdict(...))` record. These two truths — the missing parked-evaluation substrate and the missing CLI surface — are the whole job.

### 1. End-to-end loop blockers (the parked-evaluation spine)

This is the dimension that decides whether the loop can run at all. Five findings describe one missing mechanism from five angles; they must be built as one coherent change.

| Layer | What's missing | Evidence |
|---|---|---|
| criome parks nothing | `record_evaluation_decision` only publishes when `decision == Authorized`; on `EscalateToPsyche` it stores nothing and returns `AuthorizationEvaluated{contract, decision}`, dropping `object` + `evidence` | `criome/src/actors/root.rs:336, 345-348` |
| no parked wire type | `AuthorizationEvaluated` carries only `{contract, decision}`; `AuthorizedObjectUpdateStream` only ever carries `Authorized` items, so a parked item is invisible over the wire | `signal-criome/schema/lib.schema:260-263`; `root.rs:336-343` |
| no discovery path | `EvaluateAuthorization` is synchronous request/reply with no `Parked{id}` reply; there is no list-all/observe over escalations. `StoreKernel.authorization_snapshot()` exists (`criome/src/actors/store.rs:431,618`) but **no `CriomeRequest` routes to it** — it is unreachable over the socket | `criome/src/actors/root.rs:172-271` (no list-all arm); `signal-criome/schema/lib.schema:23-24,82` |
| meta-approval is content-replay, not answer-by-id | `AuthorizationApproval{evaluation, decision}` carries the **full** evaluation by value; `record_authorization_approval` re-checks the digest locally and republishes from the supplied object — never a store lookup | `meta-signal-criome/schema/lib.schema:46-49`; `criome/src/actors/root.rs:351-383` |
| mentci can't supply it | `CriomeApprovalBridge::submit_verdict(evaluation, verdict)` **requires** the caller to already hold the `AuthorizationEvaluation`; mentci state never stores one; the bridge is **never called from any binary** (only the test) | `mentci/src/criome_bridge.rs:31-44`; `mentci/src/state.rs:13-26,132-155`; `mentci/src/daemon.rs` (zero bridge references) |

The decisive proof that this is a single-process illusion: the test builds one `evaluation` at `mentci/tests/criome_bridge.rs:316-320`, passes it to `EvaluateAuthorization` (line 325), and re-passes the same clone to `submit_verdict` (line 371). The mentci question presented in between (`question_proposal()`, lines 158-169) is a **hardcoded fixture** with no link to the escalation. No assertion ties the mentci `QuestionIdentifier` to the criome evaluation. The escalation→question hop — the literal core of "criome parks → mentci sees it" — is not coverage at all; it is fabricated by the harness.

There is a working answer-by-id pattern already in the codebase, on the **wrong** flow: the BLS signature-quorum path (`AuthorizeSignalCall → AuthorizationPending{request_slot} → ObserveAuthorization`, `criome/src/actors/authorization.rs:104-158`, store-backed `LookupAuthorizationState`) does exactly the park-and-resolve-by-slot the goal needs — but it is wired to the signing flow, not to `EvaluateAuthorization`. The cheapest correct path is to fold contract escalations into that existing slot/observation-token machinery rather than invent a parallel model.

Also folded here: there is no resident process that owns the lifecycle. mentci ships exactly two executables — `mentci-daemon` (request/reply UI-state) and `mentci` (one-shot client) — and criome is symmetric request/reply with no outbound client to mentci. Nothing subscribes to criome and drives mentci, and nothing watches mentci verdicts and pushes them to criome, **except the `#[test]`**. Either the mentci-daemon itself grows a long-running criome client, or a third resident bridge binary is added; today neither exists (`mentci/src/lib.rs:7-14` has no bridge-daemon module).

### 2. The CLI-as-UI gaps

Even with the spine built, the human surface is absent. Three blocker-class findings, all in `mentci/src/client.rs`, are one job: give `ClientCommand` a verb layer.

- **No approval verbs.** `input_argument` accepts exactly one argument or errors (`client.rs:60-65`); that argument is parsed straight into a full `MentciRequest` (`client.rs:80-86`). No `list`, `watch`, `approve`, `reject`, `defer`. `main.rs` just calls `ClientCommand::from_environment().run()`. The human must hand-author the daemon-minted `QuestionIdentifier` inside a nested NOTA record — impossible, since the id is minted server-side.
- **Output is raw binary.** `run` does `reply.encode_length_prefixed()? → stdout.write_all` (`client.rs:55-56`). The daemon **can** return the data — `state.rs:208-227` projects `PendingQuestionsView` and signal-mentci's `PendingQuestionsView`/`ApprovalQuestion` already implement `to_nota()` — but the CLI never invokes it. The fix is to decode the reply and emit `to_nota()` (or a numbered list), keeping binary behind `--raw`.
- **No watch/subscribe.** `observe()` mints a `SubscriptionToken` and stores `InterfaceInterest` (`state.rs:122-130`) but the map is only ever read by `retract()`; `bump_revision()` (`state.rs:237-240`) never fans out. `serve_forever` is strictly serial one-shot (`daemon.rs:81-114`). `MentciEvent` is declared (`signal-mentci/src/lib.rs:16`) but never constructed. **Severity-adjusted to high, not blocker:** snapshot-on-reconnect polling lets the minimum loop run; push/fan-out is required only for a reactive TUI/status-bar (which the meta-config's `NotificationClient::StatusBar` anticipates).

Folded low-severity sibling: with no verb layer, every action is a verbose hand-authored positional NOTA record including `answered_by` each time (`signal-mentci/src/lib.rs:14`, `state.rs:55-71`) — the exact tax the verb layer erases.

### 3. criome client-approval-mode / park design gaps

`AuthorizationMode` is the closed two-variant enum `[Quorum AutoApprove]` (`signal-criome/src/schema/lib.rs:247-250`). **There is no "client approval" / hold variant and no code path that parks every submission for an external approver.** `evaluate_authorization` branches only on `AutoApprove` (short-circuit to `Authorized`) vs the `Quorum` contract path (`root.rs:312`). The goal's phrase "criome runs in client approval mode" maps to nothing in the enum — and even the per-contract escape, `Rule::EscalateToPsyche`, **does not park** (it returns and is forgotten, per §1). This is the central intent ambiguity below.

Two distinct authorization mechanisms now coexist and only the wrong one holds durable pending state (the slot-based signing flow parks; the contract-evaluation flow the goal uses does not). The risk is two half-built approval models; the goal targets the one without parking.

Defer is broken on both sides and deserves a design decision, not just an implementation: in criome, Defer folds into terminal `EvaluationDecision::EscalateToPsyche` and stores nothing (`root.rs:375`); in mentci, `answer()` short-circuits Defer to `VerdictAccepted` **without checking or touching the pending list at all** (`mentci/src/state.rs:133-139`) — a deferred question is neither kept nor re-parked, it is a no-op acknowledgment. "Defer" currently means "forget" everywhere.

### 4. Durable state + key custody

- **mentci SEMA is non-durable.** `bind()` spawns `StateOwner::new(State::default())` per boot (`daemon.rs:59-60`); `on_start` is a passthrough with no load (`daemon.rs:127-133`); state is plain `Vec`/`BTreeMap` with counters reset to 1 (`state.rs:13-52`). The five `*Family` redb tables in `mentci/schema/sema.schema` (~239-296) with the explicit "self-resume on restart" comment are pure spec — no code reads or writes them; `Cargo.toml` has no sema/redb dep. **Severity-adjusted to medium for the goal:** one continuous run satisfies the demanded loop; restart-durability is the workspace's daemon-self-resume override, not a demo blocker. But note the interaction: once the parked evaluation lives in mentci state (§1), durability becomes load-bearing — a restart would lose the question↔evaluation link and strand criome's parked work.
- **criome master key is plaintext-at-rest.** `persist` writes `secret.to_bytes()` to a `create_new`+0600 file with fsync, no encryption/KDF/unlock (`criome/src/master_key.rs:87-102`); the module doc names this the transitional bootstrap (Spirit psc6), with the eventual model being an authenticated meta-signal-criome key config. **Loop-functional, low severity for the goal** — the key reloads to the same public key; encryption-at-rest is a named production-boundary step, not a demo blocker.

### 5. Ugly code / discipline

None of these block the loop; they are the discipline debt the workspace contract forbids accumulating. Severities below are goal-scoped (re-rated low/medium by the audit).

- **Blocking sema-engine disk IO inside async actor handlers** (`criome/src/actors/store.rs:515-693` → `tables.rs:502-529` → synchronous `sema-engine` `commit`/`mutate_keyed`, no `spawn_blocking`). Violates no-blocking-in-actor-handlers; latent under the single shared runtime (`daemon.rs:106`). Works today only because traffic is single-shot and serial — exactly the condition the live loop stops guaranteeing once a resident bridge adds concurrency. Highest-value cleanup of this group.
- **Stringly-typed actor/frame error boundary** (`Error::ActorCall(String)` and `UnexpectedSignalFrame{got: format!("{other:?}")}`, `criome/src/error.rs:8,41`, `transport.rs:54-160`, `mentci/src/error.rs`). kameo's `SendError` is a real enum; the cause distinction is destroyed at the boundary. Concrete consequence: `authorization.rs:293-298` funnels any non-replay error into `MalformedRequest`, so a mailbox-closed/panic is reported as a malformed request — conflating "criome rejected" vs "transport broke" exactly where the loop wants to tell them apart.
- **Five free functions violating the method-only override** (`criome/src/transport.rs:14`, `actors/mod.rs:26,30`, `authorization.rs:293`, `store.rs:695`). `active_status` (`store.rs:695`) is **dead** — zero callers — delete it; the rest move onto their owning nouns (`CriomeReply::reject`, `From<CriomeReply> for CriomeActorReply`, etc.).
- **Length-prefixed frame read duplicated verbatim three times** (`criome/src/transport.rs:95-109,178-192`; `mentci/src/frame_codec.rs:25-45`) — wants one `LengthPrefixedFrameReader` generic over the frame type; the manual re-prefix-then-`decode_length_prefixed` is doubly wasteful since `decode_length_prefixed` already strips the prefix.
- **`record_authorization_approval` duplicates `record_evaluation_decision`** (`root.rs:351-383` vs `307-349`): same digest guard, same `AuthorizedObjectUpdate` literal, inline verdict mapping that should be `impl From<AuthorizationApprovalDecision> for EvaluationDecision`.
- **`key_registry` N+1 await loop** on the Quorum hot path (`root.rs:498-525`): one `ResolveIdentity` ask per identity because `IdentitySnapshot` drops the public key (`registry.rs:152-165`); `snapshot_records()` already returns the full `StoredIdentity`.
- **Stale schema doc** in both mentci headers claiming "signal-criome won't lower" (`signal-mentci/schema/lib.schema:52-54`, `meta-signal-mentci/schema/lib.schema:39-41`) — false; signal-criome regenerated today and meta-signal-criome cross-imports it fine. Retiring this claim is the prerequisite to letting `CriomeEscalation` cross-import a real criome reference (§1) instead of being a payloadless nullary tag.

### 6. Unported / stub catalog

What is named in schema or doc but has no running implementation:

| Symbol / capability | Where declared | State |
|---|---|---|
| `PublishInterfaceState` / `InterfaceFanOut` / `InterfaceDelivery` | `mentci/schema/nexus.schema` | schema-only; grep of `src/` for publish/fan/deliver/broadcast = empty |
| `FrameEscalation` / `EscalationFramed` / `CriomeEscalationRequest` (escalation→QuestionProposal) | `mentci/schema/nexus.schema:235,415,426,443,456` | schema-only; zero Rust |
| `RouteVerdict` / `VerdictRouted` / `SignedVerdict` / `VerdictRouting` | `mentci/schema/nexus.schema:253-263,421-457` | schema-only; `answer()` terminates at an in-memory `Vec` |
| Five `*Family` redb SEMA tables + self-resume | `mentci/schema/sema.schema:~239-296` | spec only; no redb dep, no read/write |
| `CriomeApprovalBridge` (the whole bridge) | `mentci/src/criome_bridge.rs` | compiles; **dead in every binary** — referenced only by the test |
| `StoreKernel.authorization_snapshot()` (list-all parked) | `criome/src/actors/store.rs:431,618` | exists; **no `CriomeRequest` routes to it** — unreachable over socket |
| Subscriber push channel | `criome/src/actors/subscription.rs:17-22` (doc admits unbuilt) | `publish_authorized_object_update` pushes to an in-memory `Vec` never drained to subscribers |
| `CriomeEvent` escalation variant | `signal-criome/src/schema/lib.rs:1207-1211` | enum has only Identity/Authorization/AuthorizedObject — no escalation/pending event; daemon constructs no `CriomeEvent` at all |
| Encrypted-at-rest key + unlock | `criome/src/master_key.rs:10-13` (doc names it) | transitional plaintext bootstrap |

Structural theme across the catalog: **the nexus.schema already names the entire intended bridge** (`FrameEscalation`, `RouteVerdict`, `InterfaceFanOut`). The design is drawn; none of it is built. The operator's job is to implement the schema mentci already declares, plus give criome a parked-evaluation store and an observable surface for it.

## Build sequence to the working loop

Ordered path from today's state to the running two-daemon CLI approval loop. Each step names the repos touched and the observable outcome that proves it.

1. **Make criome PARK on escalation: add a pending-authorization store keyed by a criome-minted ParkedAuthorizationId (reuse the existing AuthorizationStateRecord/request_slot machinery from the signing flow). On EscalateToPsyche, evaluate_authorization persists the full AuthorizationEvaluation and replies Parked{id} instead of a terminal AuthorizationEvaluated.**
   - Repos: criome, signal-criome
   - Outcome: A submission that escalates leaves a durable parked row; the EvaluateAuthorization reply returns a stable id. Provable by a criome-only test: submit one escalating evaluation, then read the parked row back by id.

2. **Expose discovery on criome: add a signal-criome request (e.g. ObserveParkedAuthorizations / ListPendingEscalations) that routes to the existing-but-unreachable authorization_snapshot(), returning parked AuthorizationEvaluations with their ids. (Optionally a CriomeEvent escalation variant later for push.)**
   - Repos: criome, signal-criome
   - Outcome: A fresh client connecting to criome's ordinary socket can enumerate every parked submission by id. Provable: a second connection lists the item parked in step 1 without holding the original evaluation.

3. **Change meta-approval to answer-by-id: AuthorizationApproval carries ParkedAuthorizationId + decision (not the inline evaluation). record_authorization_approval loads the parked evaluation by id, applies the verdict, transitions/removes the parked row, and publishes on Approve; Defer re-parks (refresh) instead of emitting terminal EscalateToPsyche. Give the recorded reply its own honest decision vocabulary.**
   - Repos: criome, meta-signal-criome
   - Outcome: criome authorizes a parked item from an id alone. Provable: list a parked id, send Approve{id} over the meta socket, observe the AuthorizedObjectUpdate — with no caller-supplied evaluation.

4. **Add a ClientApproval/hold mode (or wire Rule::EscalateToPsyche to the new park path) so criome parks uniformly when configured. Confirm with the psyche which framing 'client approval mode' means (open question) before choosing daemon-wide vs per-contract.**
   - Repos: criome, signal-criome
   - Outcome: A criome booted in client-approval mode parks every submission. Provable: configure the mode via meta-signal-criome Configure, submit any evaluation, see it parked rather than auto-authorized.

5. **Thread the criome reference through signal-mentci: give ApprovalSource::CriomeEscalation a payload (a CriomeAuthorizationReference carrying the ParkedAuthorizationId, cross-imported from signal-criome), thread it through QuestionProposal/ApprovalQuestion/ApprovalVerdict, and retire the stale 'signal-criome won't lower' header comment that blocks the cross-import.**
   - Repos: signal-mentci, meta-signal-mentci
   - Outcome: A mentci question and its verdict carry a typed handle to the exact parked criome item. Provable: a presented question round-trips the id; the verdict echoes it.

6. **Wire the bridge into a resident process: teach mentci-daemon (or a new mentci-criome-bridge binary booted from a meta-signal config with both socket paths) to hold a criome connection, poll/observe parked escalations, FrameEscalation each into a PresentQuestion (impl From<parked-evaluation> for QuestionProposal), and store the ParkedAuthorizationId in mentci State alongside the question.**
   - Repos: mentci, signal-mentci
   - Outcome: Running both daemons, a submission parked at criome appears automatically as a mentci pending question. Provable: criome parks, then mentci's pending list shows it with no manual PresentQuestion.

7. **Close the return arc in the daemon: State::answer looks up the stored ParkedAuthorizationId and calls CriomeApprovalBridge.submit_verdict(id, decision) so an accepted/rejected/deferred mentci verdict reaches criome's meta socket; make Defer re-park rather than no-op (state.rs:133-139).**
   - Repos: mentci
   - Outcome: Answering a mentci question drives criome to Authorized/Rejected/re-parked. Provable: a multi-process test (no shared variable) where AnswerQuestion flips the criome parked row.

8. **Build the CLI verb layer: add `mentci list` (decode the reply and render PendingQuestionsView via to_nota()/a numbered list), `mentci approve|reject|defer <id>`, and `mentci observe`; ClientCommand constructs the signal-mentci request internally, supplying constant fields (decision variant, default answered_by from configured identity). Keep raw binary behind --raw.**
   - Repos: mentci
   - Outcome: A human runs `mentci list`, reads parked submissions, runs `mentci approve <id>`, and sees a one-line status. Provable: drive the entire loop from a shell against two live daemons, no NOTA hand-authoring.

9. **Persist mentci SEMA: back State with the declared *Family redb tables (or persist the Vecs/map + counters to an rkyv/redb file), rehydrate in on_start, so a restarted mentci-daemon resumes its parked questions and their ParkedAuthorizationId links.**
   - Repos: mentci
   - Outcome: Restart mentci-daemon mid-loop and `mentci list` still shows parked items linked to criome. Provable: park, restart, approve — criome still authorizes.

10. **Replace the false-confidence integration test and clear discipline debt on the touched paths: rewrite criome_bridge.rs to run three separate serve loops with no shared evaluation variable; move criome store IO off the actor runtime (spawn_blocking) since the resident bridge now adds concurrency; delete dead active_status, dedupe the frame-read codecs, give ActorCall/UnexpectedSignalFrame typed payloads, and fix the verdict-mapping duplication.**
   - Repos: mentci, criome
   - Outcome: The end-to-end test asserts the SAME parked evaluation surfaces as a mentci question and that answering it authorizes criome — over real sockets. Discipline overrides satisfied on the loop's hot path.

## Open questions for the psyche

- Does 'client approval mode' mean a daemon-wide AuthorizationMode variant that parks every submission, or per-contract escalation via Rule::EscalateToPsyche? Neither parks today; the build path differs by answer.
- Where should the parked AuthorizationEvaluation live as source of truth — held in criome's store keyed by a ParkedAuthorizationId (criome owns the queue, mentci lists it over the wire), or carried into mentci's pending store (mentci owns the parked evaluation and re-supplies it on approval)? The nexus.schema implies mentci frames/owns it; criome's existing slot machinery implies criome. This decides which repo holds the queue.
- Should the meta-approval contract be changed to answer-by-id (ParkedAuthorizationId + decision), or is re-supplying the full evaluation acceptable for now? Answer-by-id is required for genuine cross-process approval but is a breaking contract change to meta-signal-criome.
- What should Defer do — terminally drop the item (current behavior on both sides), or re-park it to keep the submission alive for a later decision? This is a semantics decision, not just a bug fix.
- Is a separate resident mentci-criome-bridge binary wanted, or should mentci-daemon itself grow the long-running criome client? Both satisfy the loop; the choice affects deploy topology and the meta-signal config shape.
- For the first milestone, is a single continuous two-daemon run sufficient (in-memory state, plaintext key, poll-based list), deferring durable SEMA / push fan-out / encrypted key custody to a later pass — or must restart-durability and the daemon-self-resume override be satisfied before the loop counts as 'working'?

## Chat items raised

- **(question)** What exactly should 'client approval mode' mean in criome? Two readings exist and the codebase supports neither today: (a) a daemon-wide AuthorizationMode variant that parks EVERY submission for the human, or (b) per-contract policy via Rule::EscalateToPsyche where 'client approval mode' just means 'use contracts that escalate'. Today AuthorizationMode is only [Quorum AutoApprove] and even EscalateToPsyche doesn't park. Which framing do you want? The build branches here.
- **(observation)** The whole cross-daemon loop currently exists in exactly one place: a single #[test] (mentci/tests/criome_bridge.rs) that starts both daemons in one process and hand-carries an AuthorizationEvaluation as a local Rust variable from the escalation reply straight into the verdict submission. The mentci question it presents in between is a hardcoded fixture with no link to the escalation. Reports 440/441 may read as 'happy path proven' — but the escalation-to-question hop, the actual core, is faked by the test, not implemented.
- **(observation)** The root structural cause behind ~12 of the findings is one missing thing: the AuthorizationEvaluation is never persisted, never put on the wire, and never threaded through any contract. criome forgets it on escalation; the mentci question type has no field for it; mentci daemon state has no slot for it; and criome's meta-approval forces the answerer to re-supply the entire evaluation by value. Fix that one substrate (a parked, addressable-by-id evaluation) and most blockers fall together.
- **(observation)** criome ALREADY has a working park-and-answer-by-id pattern — but on the wrong flow. The BLS signature-quorum path (AuthorizeSignalCall -> AuthorizationPending{request_slot} -> ObserveAuthorization, store-backed lookup) does exactly the park/observe/resolve-by-slot the goal needs. The contract-evaluation path the approval loop uses has no equivalent. Reusing that machinery is far cheaper than building a parallel model and avoids two half-built approval systems.
- **(recommendation)** Two independent tracks can proceed in parallel without colliding: (1) the criome park/discover/answer-by-id substrate (criome + signal-criome + meta-signal-criome), and (2) the mentci CLI verb layer + human-readable rendering (mentci only, no schema change — the daemon can already project PendingQuestionsView and the types already have to_nota()). The bridge wiring in the middle depends on both. Starting the CLI track immediately gives you a visible, usable surface even before the live criome wiring lands.
- **(recommendation)** Decide what 'Defer' means before building it — right now it's broken to mean 'forget' on both sides: criome folds Defer into terminal EscalateToPsyche and stores nothing (root.rs:375), and mentci's answer() short-circuits Defer to VerdictAccepted without even touching the pending list (state.rs:133-139), so a deferred question is a no-op. If Defer should keep an item alive for later, it must re-park on both sides; that's a design choice, not just an implementation detail.
- **(recommendation)** For the FIRST working demo, snapshot-polling is enough — you do not need server push/fan-out, durable SEMA, or encrypted key custody to make the loop RUN over two live sockets. `mentci list` re-reading on each invocation satisfies 'the human sees parked submissions'. Treat watch-mode fan-out (InterfaceFanOut), restart durability (the *Family redb tables), and encrypted-at-rest key custody as the second pass once the loop is proven end-to-end.
