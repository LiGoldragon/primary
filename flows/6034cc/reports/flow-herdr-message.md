# Flow ↔ Herdr ↔ Message: feasibility and implementation boundary

Flow: 6034cc, messaging-builder-1. Requested by primary Psyche opus 108ab0,
2026-09-17. This is a feasibility witness and proposed implementation contract;
no Flow or Message code has been changed or deployed.

## Finding

The triangle is feasible with the installed Herdr 0.8.2, protocol 20,
schema version 1. Herdr already owns terminal input, pane placement, harness
recognition, and state observation. Flow owns recipient identity and position;
Message asks Flow for a position and submits the datom through Herdr.

The running session is `messaging-build`. Plain `herdr agent list` failed
with `server_not_running` for the default socket, while
`herdr --session messaging-build agent list` found this Codex agent by its
name, pane, terminal identity, and working state. `HERDR_ENV=1` alone does
not supply the session selection in this environment.

## Observed primitives

Commands run against the installed executable:

- `herdr agent prompt --help`: takes TARGET and TEXT; optional wait is a
  state observation, explicitly not per-turn tracking. Blocked agents reject
  submission before input. The timeout must be bounded by our caller.
- `herdr agent send-keys --help`: takes TARGET and KEY values; canonical
  Escape spelling is `esc`.
- `herdr api schema` and `herdr api schema --json`: prompt accepts a text
  string, start accepts name/kind/pane/args, send_keys accepts key strings.
- `herdr agent start --help`: starts a supported harness in an existing
  interactive shell pane and returns after recognition/readiness. Codex and
  Claude are supported. Startup timeout is bounded.
- `herdr pane split --help`: accepts an explicit pane, cwd, environment, and
  no-focus placement. `pane list` returns pane and terminal identity.
- `herdr session list`: default stopped, messaging-build running.
- `herdr --session messaging-build agent wait messaging-builder-1
  --until working --timeout 1000`: returned this working agent.
- `herdr --session messaging-build agent send-keys messaging-builder-1
  'Probe.{ no-input }'`: returned `invalid_key`, unsupported key. No Escape
  or valid input was included in this probe.
- Prompting an absent target returned `agent_not_found`.

The available source checkout at `/git/github.com/herdrdev/herdr` supports
these observations: `src/app/api/agents.rs` submits prompt text and schedules
Enter; `src/app/api_helpers.rs` uses bracketed paste when supported. Its
send-keys implementation validates all keys before writing. This source was
inspected, not rebuilt or proved identical to the installed binary.

## Smallest component slice

Extend the public producer contracts, not a parallel script or component-local
command vocabulary. The existing Message AGENTS.md requires producer-owned
Types and datom-codec at the text boundary.

1. Flow `RegisterFlow`: flow ID plus a Herdr position. Store session, pane,
   terminal ID, agent name, and harness kind. Validate against Herdr's live
   agent list before registering. Identical registration may succeed again;
   conflicting reassignment must be explicit, never a silent overwrite.
2. Flow `ResolvePosition`: flow ID to the stored position, with a typed
   unknown/stale/unavailable refusal. Compare terminal identity and harness
   against the live list before delivery so a reused pane does not receive a
   former occupant's message. A registry cannot manufacture a live harness.
3. Message `Send`: recipient, priority, body. Priority has HardAbrupt,
   MiddleAbrupt, and Soft variants. The body must remain a datom value, not
   JSON and not an opaque quoted copy of a datom in the recipient prompt.
   Settle the precise priority-headed Datom type in signal-message; do not
   hand-write a second parser. Validate the full body before any Escape.
4. Message resolves through Flow's ordinary typed socket. It passes datom
   text as one process argument to Herdr, without a shell. Herdr's JSON
   replies are an external substrate protocol, never the recipient's prompt.
5. For Codex HardAbrupt: `herdr --session SESSION agent send-keys TARGET esc`,
   followed by `herdr --session SESSION agent prompt TARGET DATOM`. Prompt
   supplies text and Enter; a second explicit Enter would double-submit.
6. For MiddleAbrupt and Soft: `herdr --session SESSION agent prompt TARGET
   DATOM`. These have the same transport in this slice, per the assignment.
   Preserve priority in the delivered datom; promise no distinct scheduling.
7. Fail closed for unsupported hard-abrupt harness behavior. Claude's exact
   interrupt semantics need a dedicated observation before claiming parity.
8. A successful receipt means submitted to Herdr. It does not mean read,
   comprehended, or finished. A failure after Escape is a partial side effect;
   distinguish it from a refusal that sent nothing. Do not retry uncertain
   submission automatically.

Follow-on launch integration belongs to Flow: allocate a flow ID, split/place
with Herdr, start the configured harness, record the returned terminal identity,
and submit the launch brief. Persist a pending launch before starting so an
uncertain start does not cause an automatic duplicate. Registration and sending
existing live flows is the first implementation boundary; the complete launcher
still needs this integration and a live witness.

## Gaps and required tests

Herdr has no atomic compare-terminal-and-submit operation in the inspected
surface. Revalidation narrows but cannot eliminate the replacement race.
Hard Escape plus prompt is also not one atomic operation. Serialize sends per
recipient within Message; external keyboard input remains outside that lock.

Herdr wait is state-based, not a read receipt. No three-tier scheduling or
exactly-once delivery is established. A terminal accepting bytes does not
prove where a harness inserts them in model context.

Meaningful tests must witness: registry persistence and conflicting registration;
unknown flow; stale terminal identity; unavailable server; literal Unicode datom
payload; invalid datom rejected before side effects; exact Escape/prompt order;
soft and middle prompt-only delivery; failed Escape preventing prompt; failed
prompt after Escape reporting partial delivery; and real disposable Codex
recipient acknowledgement. Expose durable automated tests through Nix checks.
No live recipient interruption or comprehension test has yet been run.

## Repository and coordination findings

`/git/github.com/LiGoldragon/flow` is clean on main and still owns workspace-local
signal-flow Types plus a Codex app-server launcher. The separate signal-flow
repository already declares a different ResolveRecipient contract. Converge the
producer boundary rather than adding a third contract.

`/git/github.com/LiGoldragon/message` is clean on `flow-delivery-poc`, not main.
Its interim FlowMarkerIndex only proves a marker exists, and FlowDeliver parks
an envelope; neither resolves a Herdr terminal nor injects a prompt. Its main
bookmark points elsewhere. Do not accidentally publish this branch as main.

Orchestrate Observe.Locks reports fac697 holding:

- 1836: flow, signal-flow, meta-signal-flow repositories.
- 1837: message repository.
- 1839: signal-message and meta-signal-message repositories.

The local non-management instructions require an isolated workspace for claimed
repos. A RequestWorktree request was rejected with
`Unreadable.Error.{ Composition [] Variant.{ Query RequestWorktree } }`.
Ownership transfer or an available workspace provisioner is needed before edits.
The same instructions require a named Rust doctrine before Rust editing; that
was requested from the primary alongside ownership coordination.

Progress and blockers were queued to the primary Codex forwarding thread and
sent via intercom addressed to primary Psyche opus at claude-primary-3080436.
Delivery into either model's context has not been observed.

The schema-3 → 5 decoder and generated skill trees were untouched.
