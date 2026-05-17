# Terminal / Orchestrate Porting Decisions

Operator record of the questions raised before porting the latest terminal,
orchestrate, and permission-scoped Signal architecture into repository
architecture files and code.

Sources read for this decision point:

- `reports/designer/211-persona-terminal-consolidation-one-daemon-2026-05-17.md`
- `reports/designer-assistant/115-orchestrate-integration-architecture-2026-05-17.md`
- `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md`

## User-Approved Answers

| Question | Approved answer | Implementation consequence |
|---|---|---|
| Should the first consolidated terminal implementation re-adopt existing terminal-cell processes by `pidfd`, or restart sessions cleanly? | Clean-slate restart first. Re-adoption is later. | Session registry records model the desired terminal surface now, but first implementation does not need a re-adoption protocol. |
| What Signal verb owns `CreateSession`? | `CreateSession` is `Mutate`. | `signal-persona-terminal` session creation enters the contract as an owner-side state-changing request. |
| Are "control" and "supervision" distinct socket categories? | "Control" is too close to supervision. Use **communication socket** for the component's main Signal socket and **supervision socket** for engine lifecycle/readiness. | Architecture docs should stop contrasting "control socket" with "supervision socket" at the component boundary. Existing old code names may remain until touched, but new prose should say communication/supervision. |
| Who owns durable orchestration policy truth? | `persona-mind` owns durable policy truth; `persona-orchestrate` sequences execution of accepted orders. | Orchestrate is a real component, not a compatibility wrapper, but policy state is mind's authority. |
| Can orchestrate issue downstream router grants? | Yes. The owner-socket `Mutate` accepted by orchestrate can translate into downstream `Mutate` orders. The incoming socket determines which actor handles the message; a non-owner socket does not know `Mutate` and returns an error. | Owner-scoped contracts and sockets must make unauthorized `Mutate` structurally unreachable or typed-rejected. Router grant tests should hit both owner and non-owner sockets. |
| Does the prototype need real Unix permission enforcement? | No. The prototype can run same-UID and skip file-permission enforcement. | The architecture still targets per-component users/groups later, but the current sandbox work should focus on typed socket separation and error behavior. |

The user also confirmed that the other answers were good, so these are closed
for the current porting pass.

## Additional Operating Decisions

- `terminal-cell-daemon` remains a standalone development/test harness. The
  production Persona path consumes `terminal-cell` as a library inside the
  consolidated `persona-terminal` daemon.
- `persona-terminal-validate-capture` is a test/check witness, not production
  runtime surface.
- `tools/orchestrate` remains transitional workspace tooling. It does not
  become `persona-orchestrate`.
- `persona-orchestrate` is a real triad component: daemon, CLI, Signal
  contract, and component-owned Sema database.
- Owner-scoped contract repository names use the `owner-signal-*` shape.

## Current Porting Status

`signal-persona-terminal` now carries the first session-registry contract
surface:

- `CreateSession` / `RetireSession`
- `ListSessions` / `ResolveSession`
- `SessionCreated` / `SessionRetired`
- `SessionList` / `SessionResolved`

The request/reply variants were appended to the existing enums so archived
variant order remains stable for existing variants.

`persona-terminal` has started consuming the new contract. The old supervisor
runtime can now type-check against the extended request/reply enums. The next
implementation step is to add tests proving the supervisor can answer
`ListSessions` and `ResolveSession` from its component Sema registry, then
update the architecture files to reflect the consolidated one-daemon target.

## No Open User Questions For This Slice

The remaining work is implementation:

1. add session-registry supervisor tests;
2. update `persona-terminal` architecture/status around communication vs
   supervision and the consolidated daemon target;
3. update `terminal-cell` architecture/status to mark the standalone daemon
   as development/test harness for Persona;
4. run Nix checks;
5. commit, push, and update the relevant BEADS items.
