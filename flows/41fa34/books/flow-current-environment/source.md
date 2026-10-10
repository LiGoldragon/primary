# Flow: the current environment

## Current registry and memory

**FILE:** `skills/knowledge-flow.md`, current-environment
section. **ADD:**

The Oct 7 `hm-list` read used the deployed wrapper
`/home/li/.local/bin/hm-list` and typed messenger package
`messenger-clj 0.3.0`. It showed these readable rows:

FieldSol working; MindSol working; Psyche Opus `d4ae97` done;
Psyche Tertiary Sonnet `8f0f57` done; Mind Tertiary Luna `918df4`
done; Psyche Quaternary Sonnet `02dda6` done; Mind Quaternary Luna
`4ddfe1` done; Field Tertiary `4371ed` done; Field Quaternary
`6aa08d` done; Field Primary `44cda5` done; Psyche Primary Fable
`f5a6e9` working; Mind Primary Astra `0c85a3` blocked; another
Psyche Primary Fable `ebbe30` done. Old Psyche Fable `8475a9` and
`bad807` are stale or absent. Done means completed, not retired.

The Herdr read corroborated 13 matched panes and titles; an earlier
14-pane claim is withdrawn. `flows/index.md:260-284` is a historical
handoff index, and Oct 3 `roster.json` is not a live registry. The
ordinary Flow list was NUL-corrupted; its cause is unknown. Flow CLI
0.23 and installed Nexus 0.12.2 are distinct; the live process's
current binary version is unknown.

**INSERTION:** This replaces any authored line claiming that no current
registry response exists. These observations are retained runtime
witnesses, not proof that every listed row has a Flow route.

## Routing and ordinary versus meta paths

**FILE:** `skills/knowledge-flow.md`, routing section. **ADD:**

The deployed messenger source documents the ordinary route in
`messenger-clj/src/messenger_clj/core.clj:191-258, 901-948, 977-985`.
`hm-send` resolves the exact short Flow alias, uses the session Unix
route and `agent.prompt`, rechecks the target, then reports
`Transported`, `Presented`, `Uncertain`, or refusal. `hm-send-abrupt`
uses the same target guards and adds the documented interrupt keys
(`core.clj:834-887`); it does not bypass a blocked target. A wait for
Presented may observe working, idle, done, or blocked, but subsequent
verification still rejects blocked (`core.clj:208-224, 259-265`).

The authored Flow source separately stores FlowNodes and harness events:
`flow-nexus/src/store.rs:1605-1613, 2177-2201` and
`flow-nexus/src/reporting.rs:1-57`. No complete current Flow or meta-Flow
inventory was established. A meta socket is not automatically a
meta-Flow registry, and the source's meta list composition is refused:
`meta-signal-flow/src/generated/signal.rs:400-410` has no List variant.

**INSERTION:** Keep messenger routing, Flow memory, and meta event reads
as separate layers. The `hm-list` read itself never wakes a Flow.

## Wake and non-wake behavior

**FILE:** `skills/knowledge-flow.md`, wake section. **ADD:**

The retained messenger source qualifies route semantics, not a live wake
result. `hm-send` targets an exact alias, accepts idle, working, or done
when the route verifies, and refuses a blocked target; abrupt delivery
keeps the same guards. No send or wake probe was performed in this
review. Reading `hm-list` only reads the ledger and does not prompt a
seat.

The Oct 3 artifact-comment record is optional retained evidence. Its
harness contract distinguishes `@Claude` or “Send to Claude” from a
plain comment and names the continuous main loop as watch owner, but it
is not a current real Claude.ai idle-wake witness.

No current evidence supports waking every Flow or polling every seat.
The documented route is targeted: an explicitly named source, the
verified messenger target, then its Flow or main loop.

**INSERTION:** Preserve the distinction between documented routing,
retained harness claims, and a witnessed idle wake.

## Breakdowns and evidence limits

**FILE:** `skills/knowledge-flow.md`, breakdowns section. **ADD:**

Flow source records explicit refusals for unknown, stopped, retired,
exited, blocked, unavailable, occupied, and persistence failures
(`flow-nexus/src/reporting.rs:31-40`; `delivery.rs:32-52`). The messenger
source adds `Transported`, `Presented`, `Uncertain`, and refusal outcomes
(`messenger-clj/src/messenger_clj/core.clj:901-948`). These statuses do
not prove that a model read a message.

The current source checkout, deployed wrapper, Flow CLI, Nexus binary,
Herdr pane listing, ordinary Flow list, meta socket, native binding,
first turn, and artifact watch are different evidence layers. The
ordinary list's corruption has unknown cause; it is not evidence of a
protocol mismatch or dead store. Generated schemas, historical indexes,
and stale roster files do not replace a current binding witness.

**INSERTION:** Keep these facts and unknowns in this section; do not
infer deployment, wake success, retirement, or liveness from labels,
absence, or an old registry file.
