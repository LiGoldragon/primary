# 117 - Review of operator/134 terminal + orchestrate porting decisions

Date: 2026-05-17  
Role: designer-assistant  
Status: review, critique, and user decisions. Superseded in part by
operator/135 on 2026-05-17.

## Supersession note, 2026-05-18

The owner-signal placement recommended here has now landed. See
`reports/operator/135-owner-terminal-signal-surface-2026-05-17.md`.
`CreateSession` and `RetireSession` no longer live in the ordinary
`signal-persona-terminal` contract; they live in the new
`owner-signal-persona-terminal` contract. The remaining useful content in this
report is the authority reasoning, the owner-chain decision, and the warning
that non-owner sockets lose privileged request variants, not the `Mutate` verb
itself.

## 0. Verdict

`reports/operator/134-terminal-orchestrate-porting-decisions-2026-05-17.md`
is directionally right and is useful as an operator checkpoint, but its
closing sentence is too strong: there are still design questions that
affect the implementation shape.

The largest resolved correction is **where session-creation authority
lives**. At the time of this review, `CreateSession` had recently appeared
in the ordinary `signal-persona-terminal` contract and was mapped to
`Mutate`. That placement has since been corrected: production
`CreateSession` / `RetireSession` now live on the separate
`owner-signal-persona-terminal` surface.

Second, the report's phrase "a non-owner socket does not know `Mutate`"
needs correction. Permission-scoped sockets do not remove the verb
`Mutate` globally; they remove privileged **request variants** from the
non-owner vocabulary. A non-owner surface can still contain ordinary
`Mutate` variants if those operations are intentionally allowed there.

Third, the report was overtaken by implementation: `ListSessions` and
`ResolveSession` are already implemented and tested in
`persona-terminal` main. The remaining work is `CreateSession` /
`RetireSession`, consolidation into one daemon, CLI collapse, and
owner-socket placement.

## 0.5 User decisions after this review

The user accepted the recommendations from the first draft of this
report. Carry these as settled for operator work:

| Topic | Decision |
|---|---|
| Terminal session creation authority | Production `CreateSession` and `RetireSession` are owner-only terminal operations. |
| Contract placement | Create `owner-signal-persona-terminal`; do not keep privileged session lifecycle hidden in the ordinary terminal contract except as explicit prototype debt. |
| Owner chain for terminal sessions | First prototype shape: `persona-orchestrate` orders `persona-harness`; `persona-harness` owns/orders `persona-terminal` for terminal session lifecycle. |
| Socket and witness discipline | Even while same-UID prototype execution skips strong Unix permission enforcement, keep distinct owner/ordinary sockets and metadata/wrong-socket witnesses. |
| Wording correction | A non-owner socket does not know owner-only request variants. It is wrong to say it does not know `Mutate`; ordinary surfaces may still contain ordinary `Mutate` variants. |

This decision also fed back into `skills/component-triad.md`: OwnerSignal
surfaces are part of the triad component shape when privileged authority
exists, and daemon state is required to go through sema-engine so the
state model lines up with `signal-core` verbs.

## 1. Sources checked

- `reports/operator/134-terminal-orchestrate-porting-decisions-2026-05-17.md`
- `reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md`
- `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md`
- `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md`
- `skills/component-triad.md`
- `skills/testing.md`
- `/git/github.com/LiGoldragon/signal-persona-terminal/src/lib.rs`
- `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-terminal/src/supervisor.rs`
- `/git/github.com/LiGoldragon/persona-terminal/tests/terminal_supervisor.rs`
- `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md`

Original implementation snapshot checked:

- `signal-persona-terminal` `1709735`:
  `signal-persona-terminal: add session registry requests`
- `persona-terminal` `8153a0c`:
  `persona-terminal: answer session registry requests`
- `terminal-cell` `9a67965`:
  `terminal-cell: mark daemon as persona test harness`

## 2. What operator/134 gets right

### 2.1 Clean-slate restart first is the right first cut

The report records the user-approved decision that the first
consolidated terminal daemon does not need `pidfd` re-adoption. That
matches designer/211: a session is owned by the daemon, so daemon
failure can retire the session and record an archive cause. Re-adoption
can come later without changing the `signal-persona-terminal` contract.

### 2.2 `CreateSession` as `Mutate` is coherent

Under the authority-direction framing in `skills/component-triad.md`,
`Mutate` means "change component state at a stable identity." Creating
a named terminal session is not merely reporting a fact; it orders the
terminal daemon to install a named runtime object in its registry and
start the child process. So the mapping:

```rust
Mutate CreateSession(CreateSession)
```

is coherent if the caller has authority to order the terminal component.

### 2.3 Communication vs supervision is the right prose split

The component boundary should say:

- **communication socket**: component's main Signal socket;
- **supervision socket**: engine lifecycle/readiness socket.

"Control" remains meaningful inside the low-level `terminal-cell`
primitive (`control.sock` vs `data.sock`), but it should not be the
component-boundary contrast with supervision.

### 2.4 `persona-terminal` and `terminal-cell` were moving toward the target

The original implementation snapshot was not just prose:

- `signal-persona-terminal/src/lib.rs` contained `CreateSession`,
  `RetireSession`, `ListSessions`, and `ResolveSession`.
- The same contract mapped `CreateSession` to `Mutate`,
  `RetireSession` to `Retract`, and the two queries to `Match`.
- `persona-terminal/src/supervisor.rs` answers `ListSessions` and
  `ResolveSession` directly from the component Sema registry.
- `persona-terminal/tests/terminal_supervisor.rs` has functional tests
  proving list/resolve do not contact cells.
- `terminal-cell/ARCHITECTURE.md` now says production Persona consumes
  `terminal-cell` as a library and the standalone daemon is a
  development/stateful-test harness.

That is real progress.

## 3. Corrections before this becomes an implementation guide

### 3.1 "No open user questions" was false; the questions are now answered

Operator/134 says "No Open User Questions For This Slice." That is only
true if the slice is narrowly "append records and answer read-only
session queries." It is not true for the next consolidation step.

The questions that affected code placement are now answered:

- `CreateSession` and `RetireSession` are production owner-only
  terminal requests.
- `persona-harness` owns/orders `persona-terminal` for terminal
  session lifecycle in the first prototype; `persona-orchestrate`
  orders harness.
- The owner-signal terminal contract should be created now if these
  operations are being made real.

Those answers decide socket count, contract repo count, and who gets to
depend on which terminal contract.

### 3.2 "Non-owner socket does not know Mutate" is the wrong abstraction

Operator/134 says:

> The incoming socket determines which actor handles the message; a
> non-owner socket does not know `Mutate` and returns an error.

The permission-scoped model is narrower and cleaner:

> The non-owner socket does not know owner-only request variants.

The verb itself is not the permission boundary. The request vocabulary
is. Ordinary surfaces may still expose legitimate `Mutate` variants.
Example: `TerminalResize` is already `Mutate` in
`signal-persona-terminal`, and it does not automatically become an
owner-only operation just because the verb is `Mutate`.

Recommended rewrite:

> The incoming socket determines which typed contract actor handles the
> frame. A non-owner socket cannot decode owner-only variants because
> they live in `owner-signal-*`; if a caller sends the wrong frame family
> to that socket, it gets a typed protocol/contract error. Ordinary
> contracts may still include ordinary `Mutate` variants.

### 3.3 `CreateSession` now lives in the owner contract

This section is superseded by operator/135. Current code has the intended
shape:

- `owner-signal-persona-terminal::OwnerTerminalRequest` carries
  `Mutate CreateSession(CreateSession)` and
  `Retract RetireSession(RetireSession)`.
- Ordinary `signal-persona-terminal::TerminalRequest` has no
  `CreateSession` or `RetireSession` variants.
- `persona-terminal` has a Kameo owner request witness path that returns
  typed `OwnerTerminalRequestUnimplemented { reason: NotBuiltYet }`.

The remaining gap is runtime, not contract placement: `persona-terminal`
still needs a Unix owner socket listener and real create/retire execution.

### 3.4 The current pending-work list is stale

Operator/134 says the next implementation step is to add tests proving
`ListSessions` and `ResolveSession` from component Sema. Those tests
already exist in `persona-terminal/tests/terminal_supervisor.rs`, and
the implementation is in `persona-terminal/src/supervisor.rs`.

The updated remaining work should be:

1. Implement `CreateSession` / `RetireSession` in the consolidated
   daemon path, not just as rejected variants in the transitional
   supervisor.
2. Add the owner terminal Unix socket listener and wire it to the owner
   request path.
3. Collapse `persona-terminal-supervisor` into
   `persona-terminal-daemon`.
4. Retire or rename the transitional CLIs.
5. Make `persona-terminal-view` resolve data sockets through the daemon,
   not by reading Sema directly.
6. Add witness tests for one-daemon topology, create/retire lifecycle,
   data-socket availability after `SessionCreated`, and no stale data
   socket after `SessionRetired`.

### 3.5 Communication prose is not fully cleaned up

`persona-terminal/ARCHITECTURE.md` has adopted "communication socket" vs
"supervision socket." But new/active contract prose still says
"terminal transport control plane" in
`signal-persona-terminal/src/lib.rs`, and the README still says
"control records."

This may be acceptable if the intended distinction is:

- `signal-persona-terminal` is the terminal **control plane** in the
  low-level terminal sense;
- `persona-terminal` component boundary names its main endpoint
  **communication socket** when contrasted with supervision.

But if the user intended "control" to disappear from new prose at the
Persona component boundary entirely, `signal-persona-terminal` should
be cleaned in the same pass. The operator report should state the
scope explicitly so agents do not churn all low-level `control.sock`
language.

### 3.6 Test-only binary naming is only partly absorbed

Designer/211 and `skills/testing.md` now say test-only binaries should
use the `-test` suffix. Operator/134 says `terminal-cell-daemon`
remains a standalone development/test harness, but it does not mention
the suffix migration.

This is not a blocker for session-registry work, but it should not be
lost. If a binary is not production path, it should become
`terminal-cell-daemon-test` when the terminal-cell production/test split
is next touched, along with the test-only fixture binaries named in
`skills/testing.md`.

## 4. Settled answers that operator should use

### Q1. Who is allowed to create and retire terminal sessions in production?

The original snapshot put `CreateSession` and `RetireSession` in the
ordinary `signal-persona-terminal` request enum. That would have meant any
caller with the ordinary terminal contract and ordinary terminal socket could
express "start a child process" and "retire this session."

Decision: **owner-only in production**. Session lifecycle now lives in
`owner-signal-persona-terminal`. The ordinary terminal contract keeps
operations such as per-session input/gate/capture/query that are safe for
normal authorized peers.

### Q2. Which component owns `persona-terminal`?

The owner determines who can send owner-signal session lifecycle orders.
Possible owner edges:

- `persona-orchestrate -> persona-terminal`: orchestrate owns agent-run
  execution machinery and creates terminals as part of scheduling work.
- `persona-harness -> persona-terminal`: harness knows the harness
  adapter and session command, so it creates/retains terminals for its
  own executor sessions.
- `persona-orchestrate -> persona-harness -> persona-terminal`:
  orchestrate orders harness to run; harness orders terminal to create
  the terminal session.

Decision: **orchestrate orders harness; harness orders terminal**.
Harness is the component that knows provider adapter shape, prompt
patterns, and session command details. Orchestrate should schedule work
and capacity, not learn terminal launch details.

### Q3. Should the owner-signal terminal surface be created now?

If we wait, the consolidated daemon can move faster, but the ordinary
terminal contract will keep gaining privileged operations. If we create
`owner-signal-persona-terminal` now, the implementation is slower but
the security boundary is correct from the start.

Decision: **create the owner-signal terminal surface now** if
`CreateSession` / `RetireSession` are about to become real. It is much
cheaper to place these variants correctly before the one-daemon
consolidation wires them into code.

### Q4. Does "prototype skips Unix permission enforcement" still require
socket metadata witnesses?

The user approved same-UID prototype execution, but that should not mean
we stop testing socket shape. The prototype can skip per-component Unix
users/groups while still proving:

- there are distinct ordinary and owner socket paths when both surfaces
  exist;
- the daemon binds the expected sockets;
- wrong contract frames on the wrong socket are rejected;
- the spawn envelope records the intended modes/paths even if the OS
  identity model is deferred.

Decision: **yes, keep socket metadata witnesses**. Only the strong OS
denial test waits for per-component users/groups.

### Q5. Should `terminal-cell-daemon` be renamed now or deferred?

The new testing skill says test-only binaries use `-test`. The
terminal-cell standalone daemon is explicitly no longer production
Persona boundary. That points to `terminal-cell-daemon-test`.

My recommendation: defer the rename if it would disrupt the terminal
consolidation slice, but create a specific follow-up and do not let the
architecture say "test-only" while Cargo still presents the binary as
production forever.

## 5. Recommended update to operator/134

Operator/134 should be revised or followed by an operator handoff note:

1. Change "non-owner socket does not know `Mutate`" to "non-owner socket
   does not know owner-only variants."
2. Replace "No open user questions" with the settled session-authority
   decisions above.
3. Update current status: `ListSessions` / `ResolveSession` are already
   implemented and tested; `CreateSession` / `RetireSession` now live in
   `owner-signal-persona-terminal` and remain unimplemented at runtime.
4. Keep terminal-cell test-binary suffix migration visible.

With those fixes plus operator/135's owner-signal split, operator/134 is a
good implementation checkpoint. The remaining risk is no longer broad
ordinary-contract placement; it is whether the owner socket and real
create/retire execution land cleanly.
