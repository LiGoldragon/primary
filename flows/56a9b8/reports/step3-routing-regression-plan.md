# STEP3 — hook and CLI routing regression plan

Owner: Mind flowNexus Secondary 56a9b8, successor of375c69.
Receipt2026-11-06T00:42:18Z; deadline02:42:18Z.
Status: plan only. No implementation, tests, builds or production effects.

## Authority and custody

Core owns the chain; versionZero Secondary febc51 owns052 composition.
The sole existing body worker is native01a1adee-75af-7043-a7cc-1ffa6eedf393,
/root/implement_052, original parent01a1adda-fc98-7f13-bc6a-1692aed8d121.
Locks25623–25626 remain2aed8d. No control/lock transfer is inferred.
Selected Flow root: /git/worktrees/flow-config-d05351-independent,
base916b54574ae0024b893a9f4252f2e97704db48c1; later changes require a fresh
owner-supplied immutable candidate pin. Other selected roots and observation
hashes: flows/febc51/reports/current-index.md. Frozen historical gate:
flows/2aed8d/reports/final-gate-packet.md; superseded startup parts carry no
current authority. Current design: flows/4f3cb8/reports/052-bare-start-memory-config-delta.md.

Native worker ACTIVE was observed23:40:08, not now. Delivery11548 was reported
queued; native acceptance and worker acknowledgment remain unconfirmed. This
plan has reached composition-owner coordination, not proved worker consumption.

## Accepted target

Trace the actual generated hook command through packaged Flow CLI invocation
and its explicit ordinary socket to the Nexus holding Address declarations.
Use one explicit place-derived route through the configured Nix wrapper.
An absent or wrong target must fail truthfully, not report to another place.
Bare startup takes place alone; behavioral values enter Memory through explicit
Configure operations. Shell replay stays outside the Nexus.

## Bounded fixture and procedure

1. A separately appointed fixture custodian supplies an immutable coherent052
   build and test-only root. Record all artifact pins, rendered wrapper and hook
   command, sockets, Memory roots and isolation witness before execution.
2. Start exactly two isolated test Nexus places A and B, each with private
   sockets/Memory and test process identities. Start bare; explicitly Configure
   only the values needed by the tested operations. The test Address declaration
   exists only at B. Fixture configuration is test data, never runtime defaults.
3. Through the actual selected launch renderer/package wrapper, generate the
   Claude event commands bound to B. Inspect all five event commands for the
   selected hook executable and explicit B route. Execute the rendered Stop
   command through its real shell/argv boundary, not a reconstructed snippet.
4. Supply synthetic native Stop JSON with registered same-session identity and
   test transcript path. Where the actual recorder reads context from transcript,
   supply a minimal supported test transcript with an independently known token
   total. Do not add invented context fields to Stop. Capture hook exit/result,
   CLI destination, B report event, native correlation, stored measurement and
   settlement separately. Observe A before/after: no new matching report, context,
   settlement or queue change. Compare fixture-owned state, not production data.
5. Repeat with an inherited decoy legacy FLOW_SOCKET pointing to A and hostile
   PATH decoys. Explicit selected executable/B socket must still win. Exercise
   real argv quoting using spaces, apostrophes and shell metacharacters in fixture
   paths; a sentinel verifies that content never executes as another command.
6. Negative fixtures: absent B listener; wrong target A lacking the declaration;
   native-session mismatch; transcript mismatch. Assert the actual typed/error
   result and absence of false success/correlated settlement. A wrong-target report
   may be journaled by its actual admission rules; it must not masquerade as a
   correlated B success. Record that distinction rather than assume zero traffic.
7. For fresh and supported refresh launch paths, verify generated hooks retain
   selected executable and B socket under the decoy parent environment. Identity
   adoption alone is not hook migration. No real harness/model launch is needed
   for the renderer/fixture test; any broader lifecycle test needs its own custody.

## Oracle and evidence

Use the actual candidate renderer, wrapper, CLI, hook and report handling path.
An independent expected fixture identity/token total and A/B state delta are the
oracle; command-text inspection alone is insufficient. Report emission, native
acceptance, correlation, Memory write and settlement as distinct observations.
Codex token-usage reporting is a separate existing source; this Claude regression
makes no parity claim. No warning/Continuity behavior is added in STEP3.

## Custody needed before tests

Name one fixture runner, its new test-only root/reservation, exact candidate pins
and the supported capsule/bootstrap invocation. Prove production sockets, stores,
Herdr, homes and credentials are unreachable; block external network. Supply only
synthetic session/transcript data. Explicit grant must cover the two processes,
Configure fixture operations, rendered command execution and readback. Define
cleanup of those exact processes/sockets/files and retain the evidence first.
No current regression build root, test lock or execution grant exists in this lane.

The existing body worker remains the only implementation writer. Core must
reconcile the once-authorized controller attempt and receipt before claiming
handoff consumed. A test runner receives no authority to steer, resume, reparent,
refresh, adopt, deploy, publish or change production configuration.

## Subsequent rulings and actual custody checkpoint

VersionZero Primary accepted this bounded test design. Core authorized fixture
PREPARATION ONLY through febc51's one completed facade checker, conditional on
actual availability, write capability, a new isolated root, fresh path lock and
scope acknowledgment. That assignment has been sent to febc51; no checker ACK,
root or lock has yet been returned. No build/process/native effects or baseline916
run are authorized. Neither a coherent052 pin nor acceptance proof exists yet.
Latest bootstrap ruling:052 uses a NEW bare place; NO051 Memory migration.
Explicit external Configure replay is ONE PER FILE, continuity per Address included.

## Added STEP3 scope: Codex Awake queue stall

Psyche Secondary ordered diagnosis, fix and queued-message delivery regression.
Witnesses: flows/262263/reports/flownexus-secondary-refresh.md and
mind-core-primary-refresh.md. Nine entries at375c69 and fourteen atb138f5 remained
queued despite Awake; both showed Codex Unbound Active and remoteUnavailable.
One supported Refresh each replaced the native seat and emptied the queue.
The successor56a9b8 acknowledged its work at00:42:18. These observations establish
stall/recovery, not cause. Successors also show remoteUnavailable, so that field
alone is insufficient explanation.

Bounded installed051 source observations, not incident attribution:

- waking.rs:1928–1933 withholds queued delivery at past threshold unless the
  refresh-refusal latch holds; sending.rs:1281–1292 similarly gates direct lease.
- Automatic Codex settlement waking.rs:3104–3111 needs tracked Resting.
- codex_turns.rs:181–195 ignores StatusIdle while named Running or Delivered;
  ResumedIdle clears Running but retains Delivered, preserving ordering safety.
- send_tool.rs:595–650 does retry subscription, so a missing reconnection loop
  is not an established defect.

Requested from Core: bounded read-only diagnostic custody/pointer for retained
old flow context+threshold, tracked turn/event and delivery disposition. The
witness records contain none of these causal discriminators. No production
query or controller attempt was made by this successor. No patch is chosen.

Regression requirement after causal/design judgment: an Awake Codex seat with
an admitted queued message must reach documented native acceptance and exact
logical receipt, then recipient acknowledgment; preserve message identity/order
and prove no duplicate submission across reconnect/uncertain outcome. Include
Soft/Middle/Hard priority behavior and rest/reconnect/threshold boundary cases
only according to the approved cause-specific contract. Queue removal alone
cannot prove consumption. Fixture preparation may reserve this test interface;
it must not invent native protocol behavior or a cause-specific oracle.

## Retained-only diagnostic result (receipt00:49:01Z)

Core authorized this flow alone to read retained evidence for375c69/b138f5, no
runtime probes. Psyche Secondary confirms it holds no retained context/threshold,
turn/events or lease/delivery transitions. Bounded roots:375c69 top-level report
is only the handoff packet; b138f5 directory has no report. No broader search or
live store open was performed. None of the cited conditional branches is proved
reached. Requested a precise existing pointer from Core, otherwise this is the
causal evidence gap; it does not stop independent fixture preparation.

Retained timeline:
- 375c69 Inspect00:41:56Z: nine queued. Refresh00:42:09;56a9b8 empty00:42:10;
  actual successor acknowledgment00:42:18.
- b138f5 Inspect00:44:46Z: fourteen queued. Refresh00:44:59;6ac27b empty00:44:59.
- Earlier375c69 queue at00:0x and b138f5 sends~00:28 are reported recollections,
  not the missing causal state snapshots.

Bounded file comparison found waking.rs, sending.rs, codex_turns.rs and
send_tool.rs byte-equal between installed051 and selected916 at this observation.
This makes the cited pointers applicable to those files, not proof of execution.

Actual prep custody has since ACKed: same checker native
01a1ae1e-ddca-7d43-ae1d-a4445901c867 accepts exact root
flows/febc51/reviews/step3-hook-routing-only, lock25651/febc51, prep-only scope.
Anchored checkpoint00:57:21Z. No run/build/process/source-edit authority.

## Added STEP3 scope: exact Done/Task matching

Psyche Secondary ordered regression: byte-identical Task matches Done both before
and after the Task sender refreshes. Correction: the30minute Task senderfe53f9
has NOT refreshed; refresh cannot explain that incident. Task6225 also returned
Unresolved on two reported exact attempts. No root cause established.

Source fact: installed051 store/logical_delivery.rs:1228–1266 filters by reminder
sender/recipient Address, matching retained exact Task and DeliveryState.Delivered.
It does not match by sending FlowId. Missing reminder, retained request or required
delivery state all produce Unresolved. Task admission creates reminder1481ff;
Done admission retracts it1499ff. Address matching disconfirms a simple claim that
this resolver uses the old sending FlowId; it does not prove all relevant paths.

Psyche's retained lead: original Task6225 send21:26:46Z returned
SendAccepted.{ 6225 Uncertain }; transcript87314557-8c42-594f-8b8a-73f2d2d6c4d0.
If Uncertain persisted, the Delivered gate could explain refusal. The initial
receipt proves no later state: reconciliation may have changed it. The30minute
Task's delivery state is unknown. Requested precise retained original request,
address pair, reminder and later logical receipt evidence; no new runtime query.

Fixture composition received the discriminator: Uncertain, actual native proof,
Delivered, exact Done; repeat with sender refresh. Do not turn Done into native
proof or silently accept an uncertain native delivery. Capture logical identity,
ambiguity and reminder cancellation independently. Domain/design judgment and
candidate API remain separate from fixture input preparation.

### Exact Done fixture matrix requested by versionZero Primary

Use the actual30minute Task text in flows/74026a/records/step3-recovery-task.txt,
removing its file-terminating LF only as the reported failing caller did. Keep
Minutes30, Task text and both Address values explicit fixture positions.

- One matching open Task with actual Delivered evidence: exact Done matches.
- Refresh only the Task sender while retaining its Address: exact Done still
  matches. Receiver refresh is a distinct additional case, not the same event.
- No Task; wrong minutes; changed body; wrong sender/recipient Address: distinct
  missing-match typed cases; do not collapse them into an incident explanation.
- Multiple eligible identical open Tasks: Ambiguous, not arbitrary selection.
- Queued, Attempting, Uncertain and Delivered: separate logical-state fixtures.
  Current resolver accepts only Delivered. This is characterization, not approval
  to weaken native proof or an assertion that the incidents remained Uncertain.
- Proven native acceptance reconciles the same logical identity to Delivered;
  exact Done resolves the one open Task and cancels only its reminder. A second
  Done cannot silently close another Task. Preserve unrelated reminders/queues.

Missing/nonDelivered case expectations beyond the current resolver remain a
cause-specific design judgment, not a fixture author's patch decision. No runs.

Step1 controlling design supplied complete00:50:31Z:
flows/4f3cb8/reports/052-step1-controlling-design.md,
SHA25689f56154d752c7db2fd8c410026e72ab453e3a048b523ab908a03feb9d6dd993.
Step2 deadline04:50:31 is separate from this STEP3 deadline02:42:18.
Primary reports another Step1 Done Unresolved; no matching retained receipt facts
establish that it shares either earlier incident's cause.
