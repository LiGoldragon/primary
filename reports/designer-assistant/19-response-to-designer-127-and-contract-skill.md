# 19 - Response to designer 127 and contract skill update

*Designer-assistant report. Date: 2026-05-11. Scope: read of the
designer edits around these files:*

- `reports/designer/125-channel-choreography-and-trust-model.md`
- `reports/designer/126-implementation-tracks-operator-handoff.md`
- `reports/designer/127-decisions-resolved-2026-05-11.md`
- `reports/designer/116-123` component plans
- `reports/designer/124-synthesis-drift-audit-plus-development-plans.md`
- `skills/contract-repo.md`

*This report is a response, not an edit to designer-owned files.*

---

## 0 - Short Read

`reports/designer/127-decisions-resolved-2026-05-11.md` is the right
new center of gravity. It correctly moves injection safety into the
terminal input gate, pauses persona-system for the current wave, keeps
plain text messages valid, broadens contract repos into component wire
surfaces, closes `HarnessKind`, keeps raw transcripts out of normal
router/mind fanout, and now explicitly protects terminal-cell's raw
data plane while moving the control plane to `signal-persona-terminal`.

The problem is propagation. The older plans were not edited deeply
enough. An operator reading these files directly can still implement
the old world:

- `reports/designer/118-persona-router-development-plan.md`
- `reports/designer/119-persona-system-development-plan.md`
- `reports/designer/121-persona-terminal-development-plan.md`
- `reports/designer/123-terminal-cell-development-plan.md`

The stale concepts still present include class gates at every
component, system-owned prompt observations, `OwnerApprovalInbox` in
router, `EngineRoute`, `OtherPersona`, per-component auth proof checks,
and the old terminal-cell bespoke control protocol that 127 now
replaces with `signal-persona-terminal` on the control plane.

My recommendation: treat 127 as canonical, but add explicit
supersession banners or rewrite the stale sections before handing these
plans to operators. `reports/designer/126-implementation-tracks-
operator-handoff.md` should become the only active operator handoff
after it is made internally consistent.

## 1 - What 127 Settles Well

### 1.1 Terminal input gate is the safety primitive

D1 is now clearer than the earlier focus/input-buffer design.
`persona-terminal` owns the injection transaction; `terminal-cell` owns
the low-level byte gate; `persona-harness` supplies adapter-specific
prompt semantics when needed. `persona-system` focus is deferred and
advisory for this wave.

This matches the working terminal-cell lesson: human keystrokes must
not travel through an actor mailbox or heavyweight relay. The byte path
stays direct; the gate is a narrow writer-side arbitration primitive.

### 1.2 Text bodies are allowed

D2 corrects an overreaction. `MessageBody(String)` is not automatically
wrong. A human message can be text. The rule should be: do not hide
modeled semantics in the body once they have earned named variants.

That means `MessageKind` and future data-carrying variants carry the
semantic growth. `MessageBody` can remain the text portion, as long as
plans do not make it the dumping ground for every future structured
concept.

### 1.3 Contract repos are shared boundary vocabularies

The `skills/contract-repo.md` edit is directionally right. A contract
repo is a shared type crate. The discipline is not "never a shared type
bucket"; the discipline is "shared boundary vocabulary, not anonymous
utility drawer."

The new component-owned shape is workable:

- one crate may cover one component's wire surface;
- each relation inside it must be named in `ARCHITECTURE.md`;
- source modules should split the relations when the component has
  multiple surfaces;
- cross-component vocabulary belongs in a smaller kernel contract only
  when it is genuinely shared kernel language.

### 1.4 Transcript privacy posture is better

D4 is right: raw transcript bytes should not be pushed by default to
router or mind. Typed observations plus sequence pointers should be the
normal fanout. A future transcript-inspection role can request raw
ranges explicitly from terminal-owned storage and then produce
summaries or audit records.

### 1.5 `Other` is dead

D6 is settled. `HarnessKind::Other { name: String }` should not be a
production contract variant. `Fixture` is the named test/integration
case; production harnesses become explicit schema variants.

### 1.6 The terminal-cell edit fixed the major ambiguity

The edited 127 now makes the crucial split I wanted:

- control plane: `signal-persona-terminal` frames for gate leases,
  prompt state, injection, resize, lifecycle, capture, wait, and worker
  lifecycle subscriptions;
- data plane: raw viewer bytes after attach, with no per-byte Signal
  encoding, no actor-mailbox hop, and no transcript-subscription detour.

It also resolves the repo question: terminal-cell stays its own repo
for now. That is the right call. The repo's direct byte-path witnesses
are valuable, and the control-plane contract gives persona-terminal a
clean integration seam without folding the low-level primitive into the
supervisor too early.

## 2 - Main Drift After The Edits

### 2.1 `reports/designer/126` is still internally inconsistent

`reports/designer/126-implementation-tracks-operator-handoff.md` has
the right top-level intent, but the body still contains old decisions.

Fixes I would make before operator handoff:

- T8 is marked deferred in the TL;DR, but the T8 section still reads
  like active persona-system implementation work. Replace that section
  with a short deferred note and remove it from active beads.
- T9 now means terminal-cell signal integration, but T3 still says
  engine-level upgrade lands in follow-up track T9. That should say
  "later engine-upgrade track"; T9 is already taken.
- The dependency graph, suggested parallelism, and bead table still
  lack T9 and still route work through active T8. They should be
  updated to `T1 -> T9 -> T6`, with T8 paused.
- §9 still says typed-Nexus body is deferred as an open decision and
  lists D1/D3/D5/D6/D7 as waiting. Those are now resolved by 127.
- T6 should explicitly include the gate-and-cache transaction:
  acquire input gate, hold human bytes, read prompt state while gate is
  held, inject only if clean, release and replay cached human bytes.

If 126 is the operator map, it must not contain resolved-decision
language that contradicts 127.

### 2.2 `reports/designer/118` still describes the old router

`reports/designer/118-persona-router-development-plan.md` remains the
largest stale plan.

Stale concepts still present:

- class-aware delivery as the router's central decision tree;
- `OwnerApprovalInbox` owned by router;
- `EngineRoute` / `OtherPersona` as active router concepts;
- router reading class from `AuthProof` and rejecting missing proof;
- router subscribing to persona-system focus and input-buffer
  observations;
- per-class garbage collection and witnesses around those gates.

The new router should instead be a channel choreographer:

- accepted socket origin is tagged for audit/provenance;
- router commits messages and delivery state;
- router holds authorized channel state: A can talk to B, A cannot talk
  to C, or A can talk to C only after mind grants a one-shot, temporary,
  or durable channel;
- ungranted user/external requests go to mind for adjudication;
- normal component-to-component messages on already-authorized channels
  do not all pass through mind;
- terminal injection readiness comes from persona-terminal, not
  persona-system focus/input-buffer state.

`OwnerApprovalInbox` belongs in mind if it exists. Router can hold a
pending-delivery table, but not an owner-approval policy inbox.

### 2.3 `reports/designer/121` still describes class-gated terminal

`reports/designer/121-persona-terminal-development-plan.md` still says
the terminal input gate is class-aware and fed by persona-system
prompt/focus observations. That conflicts with 127.

The active terminal plan should be rewritten around these records and
witnesses:

- `AcquireInputGate`;
- `ReadPromptState`;
- `WriteInjection`;
- `ReleaseInputGate`;
- `InputGateHeld`;
- `InputGateReleased`;
- `PromptStateChanged`;
- human bytes cached while the gate is held;
- cached bytes replayed contiguously after release;
- dirty or unknown prompt state defers injection without dropping human
  bytes.

Connection origin may still be recorded for audit, but it should not be
the terminal's runtime permission gate. The filesystem ACL and router's
authorized-channel state decide who can reach the supervisor; terminal
then performs the byte-safety transaction.

### 2.4 `reports/designer/123` is superseded by edited 127

This was the sharpest design conflict before 127 was edited.

`reports/designer/123-terminal-cell-development-plan.md` says
terminal-cell should keep its own bytes-and-frames socket and that
`signal-persona-terminal` terminates one layer up in persona-terminal.
Edited 127 now says terminal-cell's **control plane** should speak
`signal-persona-terminal` directly, while its **data plane** remains
raw.

So the resolution is no longer ambiguous:

- control plane: signal-shaped is fine for leases, prompt state,
  resize, worker lifecycle, capture, wait, and programmatic input
  commands;
- raw viewer byte plane: must remain a transparent attach stream after
  the typed accept/lease step, with the same latency and behavior as
  the abduco-shaped design.

Plan 123 should be rewritten or marked superseded on this point. Its
"keep the cell socket protocol bytes-shaped" recommendation is now
historical for the control plane, but its warning about protecting the
raw byte path remains load-bearing and is now absorbed by 127 §2.3.

`WorkerObservation` push also changes status. 123 leaves it optional;
127 makes it necessary if persona-terminal session health is real. That
should become initial-state-then-deltas, not polling.

### 2.5 `reports/designer/119` needs a deferred banner

`reports/designer/119-persona-system-development-plan.md` still reads
as an active track: focus tracking, privileged actions, `ForceFocus`,
`InputBufferTracker`, and class gates. 127 says persona-system takes a
back seat for this wave.

I would not delete the design. Persona will need system integration.
But the file should open with a clear status banner:

> Deferred after designer/127. Not part of the current operator wave.
> Injection safety is terminal-owned. Focus and system privileged
> actions return when a concrete OS-level Persona need appears.

Without that banner, operators will file and implement T8 work that the
user just paused.

### 2.6 `reports/designer/120` needs transcript and enum cleanup

`reports/designer/120-persona-harness-development-plan.md` mostly
survives, but it should absorb 127 explicitly.

Needed edits:

- remove `HarnessKind::Other { name }` from the planned contract shape;
- promote typed observations plus sequence pointers from "risk
  mitigation" to the main transcript default;
- clarify that router/mind do not receive broad raw transcript event
  streams;
- describe harness prompt semantics as adapter-specific assistance to
  persona-terminal, not a generic system-owned input buffer;
- replace class/auth-gate language with origin/audit/projection
  language where appropriate.

The harness can still produce provider observations, quota signals,
prompt-shape hints, lifecycle, and summaries. It should not become a
raw transcript broadcaster.

### 2.7 `reports/designer/124` is now historical unless rewritten

`reports/designer/124-synthesis-drift-audit-plus-development-plans.md`
has an update banner, but the body still says:

- typed-Nexus body migration is the unresolved central gap;
- router work is class-aware delivery with `OwnerApprovalInbox`;
- terminal work is class-aware input gate;
- apex work includes `AuthProof` signing and component-level hot-swap;
- the order of work still routes through the old wave graph.

That makes 124 unsafe as an implementation guide. Either rewrite it
against 125/127 or mark it as historical synthesis superseded by 125,
126, and 127.

## 3 - AuthProof Naming Risk

There are two different ideas currently sharing one dangerous word.

`signal-core::AuthProof` may already exist as the generic signal
envelope's auth carrier. That is not automatically wrong. The
persona-message proxy may still need to put local caller identity into
the base signal frame.

What should not land is a new Persona-specific runtime proof that
recreates the old in-band trust model.

The settled trust model is:

- filesystem ACL on Unix sockets is the local trust boundary;
- component sockets are owned by the privileged persona user and mode
  `0600`;
- the user-writable persona-message socket is the explicit untrusted
  ingress;
- `ConnectionClass`/origin is an audit/provenance tag, not a runtime
  proof every component verifies;
- router and mind use origin/channel state for policy, not
  per-component auth proof validation.

So in `signal-persona-auth`, I would avoid `AuthProof` as a record name
unless it is truly a future cross-host cryptographic proof. For the
local engine, better names are:

- `ConnectionOrigin`;
- `MessageOrigin`;
- `OriginContext`;
- `AcceptedPeer`;
- `ChannelGrant`;
- `RouteGrant`.

If cross-host Persona later needs signed assertions, introduce that as
a separate future type such as `RemotePersonaAssertion` or
`SignedRouteAssertion`. Do not make local socket ACL trust look like a
signature protocol.

## 4 - Contract Skill Follow-Up

`skills/contract-repo.md` is improved, but I see three small places
where the new philosophy should be tightened.

### 4.1 Root enum wording should become per-relation

The skill still says the root enum of a contract crate is the closed
set of vectors in that relation. Under the new component-owned model,
that should become:

> Each named relation has a closed root enum or closed request/reply
> family naming that relation's vectors.

A component contract can have multiple relation modules. It should not
imply one crate-wide enum must cover all relations.

### 4.2 Shared types are not the problem

The row currently says a repo described as "shared types" or "messages"
has an unnamed relation. After the user's correction, the issue is not
sharing types. The issue is failing to name the boundary.

Better fix:

> "The repo is described only as shared types/messages, with no named
> endpoints, direction, authority, lifecycle, or owning component."

### 4.3 Auth files should be conditional, not assumed

The generic layout names `auth.rs` and proof types as a normal contract
crate piece. After the Persona trust-model correction, that can
encourage agents to put proof machinery everywhere.

Better rule:

> Only add `auth.rs`, origin, or proof records when the boundary
> actually carries identity/origin/auth context. Do not create an auth
> proof type just because the template has a slot for one.

## 5 - Operator Reading Order

Until designer finishes propagation, operators should use this reading
order:

1. `reports/designer/127-decisions-resolved-2026-05-11.md` for the
   settled decisions.
2. `reports/designer/125-channel-choreography-and-trust-model.md` for
   trust/channel model and superseded concepts.
3. `reports/designer/126-implementation-tracks-operator-handoff.md`
   only after its internal inconsistencies are fixed.
4. Component plans `116-123` only for the parts not contradicted by
   125/127.

Do not implement these stale pieces from the component plans:

- `ConnectionAcceptor` as a central acceptor for every component
  socket;
- in-band Persona `AuthProof` verification at every component;
- router `OwnerApprovalInbox`;
- active `EngineRoute`/`OtherPersona` routing machinery for milestone
  one;
- persona-system `InputBufferTracker`;
- focus as required injection safety gate;
- terminal class-aware input gate;
- `HarnessKind::Other`;
- raw transcript fanout to router/mind;
- component-level hot-swap with same-redb concurrent writes.

## 6 - Remaining Questions / Checks

### 6.1 Make the 127 control/data split executable

127 now answers the conceptual question: Signal frames for control,
raw bytes for the accepted attach stream. The remaining work is making
that executable in 126/123 and in tests. The T9 witness list should
include:

- no data-plane call to `signal_core::Frame` encode/decode;
- no attached keystroke path through a Kameo mailbox;
- attached viewer latency under output pressure;
- attached viewer input not routed through transcript subscription.

### 6.2 What exact type replaces Persona-specific `AuthProof`?

I recommend killing Persona-local `AuthProof` and using origin/channel
names instead. Keep `signal-core::AuthProof` only where the base signal
envelope already requires it.

### 6.3 Where do prompt-pattern rules live?

127 says prompt recognition is terminal-owned with harness adapter
patterns. That sounds right, but the contract needs a named handoff:
harness supplies prompt-shape capability records; terminal owns the
gate transaction and prompt-state decision.

### 6.4 Preserve terminal-cell as its own repo in implementation

127 now closes this: terminal-cell stays its own repo for now. The
implementation should keep that decision unless the human reopens it.
If it ever folds into persona-terminal later, preserve the same
internal boundary: low-level cell primitive below terminal supervisor.

## 7 - My Net Position

Designer's new decisions are mostly right. The system is simpler after
three corrections:

- kernel filesystem ACLs are the local trust boundary;
- router choreographs authorized channels rather than every component
  doing security;
- terminal input gate, not focus, is the first injection safety
  primitive.

The work now is editorial but important: stale plans must either be
rewritten or clearly marked historical. Otherwise agents will implement
the hallucinated middle layer the user is trying to remove.
