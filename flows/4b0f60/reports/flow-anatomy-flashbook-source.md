# Flow anatomy — Mind source for Psyche flashbook review

**Status:** review source, not a rendered flashbook. Psyche owns the reviewable
flashbook collection and its eventual artifact. Mind supplies this component
contract, evidence grades and open questions. No competing flashbook writer is
created.

## Collaboration route

The `messaging-build` Herdr snapshot and HM registry were checked before the
request. They agree on current Psyche High successor Flow `836818`, agent
`psyche-fable-of-1b8ac0`, pane `wD:p9`, terminal
`term_65c138019438357`, and native thread
`836818cc-83ab-4657-8b8f-1414f887559c`. This is distinct from historical
`1b8ac0`; no held target was resumed. `FLOW_ID=4b0f60 tools/hm-send 836818`
submitted the authorized request through Herdr. Its result is **Submitted, not
a read receipt or acceptance**. Psyche's artifact path/current owner remain
unknown until the recipient replies.

## Suggested pages

### 1. A flow is an address and a running seat

```text
logical destination ── resolves now ──> one Flow binding
                                           │
                          native session + harness pane + Herdr route
```

The logical destination stays useful while its current seat changes. A Flow ID,
native UUID, session/pane binding, binding generation and lifecycle generation
are different facts. Role and model name are different from power. More than
one main may exist at the same aspect/power; peers need separate identities.
Delegated children help with work but are not replacement mains.

**Evidence grade:** proposed architecture, with current Flow source identity
and route concepts observed. The installed Flow daemon responds, but it did
not resolve the named current targets.

### 2. Messages travel; Flow decides who is there

```text
sender → Message durable queue → stable logical destination
                                  │
                           Flow resolves binding
                                  │
                           harness receives prompt
```

Message owns durable send/receive attempts, deadlines and receipts. Transport
accepted does not mean the person read it, and read does not mean work is
complete. Flow owns logical-to-native identity, lifecycle and current route.
The ordinary Flow socket asks/reads under its policy. Its privileged meta socket
registers or attests; Message is never a meta-control backdoor.

### 3. A running seat has more than a name

```text
model profile + skills/context + title
         ↓
native harness session ⇄ Herdr pane ⇄ exact Flow binding
```

The harness supplies the native context, structured skills, model profile and
title. Herdr supplies the actual pane route. A UI title, marker, same Unix UID,
or cached session does not prove logical identity. Kernel peer information,
service authority and a caller's claim are different evidence.

### 4. Replacing a main is a guarded handoff

```text
hold admission → prepare successor → verify readiness
      → accept continuity → commit logical binding → release queue
      → guarded ancestor retirement
```

The successor is prepared through the existing controller, Flow, Harness and
Herdr machinery; it is not launched by a parallel tool. Readiness checks native
identity, profile, skills/context, title and route. Continuity checks accepted
work, pending children and late-result relay. Only then does the logical binding
change. Physical spawn and deletion are not one atomic action.

If anything is unknown, the handoff holds. A crash records intent and result,
then reconciles; it does not create two active bindings or replay an uncertain
spawn. After binding commits, Message delivers only after checking its committed
binding generation.

### 5. Retirement is later and narrower

Committing a successor does not delete its ancestor. First hold admission and
quiesce accepted work. A later archive needs specific living authority, fresh
native/Herdr absence after an authorized stop, all-writer exclusion, a
single-use judgment and a recoverable journal. Protected routes, p6/p9 and
Field controller holds remain protected. There is no blanket ancestor cleanup.

### 6. What we know today

At 2026-09-23 18:21–18:22, an installed `flow-nexus` process was observed with
ordinary/meta mode-0600 listening sockets and typed replies. Resolving `6fb948`
and `4b0f60` returned `UnknownFlow`; that is a response from the daemon, not a
claim that either flow is absent. Installed binary/source parity is unknown.
The first useful proof is an accepted disposable fixture: verified native
binding registration, then exact resolve, before any replacement work.

## Review questions

Psyche/living decisions are needed for: which logical destinations are mains;
what continuity means for each role; who may approve a replacement; and the
meaningful visual story for the flashbook. Routine engineering may proceed
without waiting on those answers: separate identity generations, durable holds,
idempotent Message consumption, explicit errors, and process-observable tests.

A screenshot report of two Ouranos app servers sharing `~/.codex` is source
evidence of two publishers, not proof of duplicate Flows. Its spinner cause is
unknown; preserve the current `2087` writer and investigate only under its
owner. No secrets are included here.

## Sources

- Current living request relayed through `4b0f60`: Psyche review ownership and
  Mind component-contract contribution.
- `flows/4b0f60/reports/flow-nexus-main-replacement-contract.md` and
  `retirement-enforcement-contract.md`: current replacement/retirement design
  and runtime evidence limits.
- `flows/b80e55/reports/flashbook-claude-agents-source.md`: source/artifact
  separation and Psyche-centered flashbook process; no renderer was invoked.
- Current `herdr --session messaging-build api snapshot` and
  `~/.local/state/hacky-messenger/836818.json`: matching successor route and
  registration; the Herdr submission is not an acknowledgement.
