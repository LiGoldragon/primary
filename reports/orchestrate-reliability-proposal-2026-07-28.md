# Orchestrate reliability proposal — 2026-07-28

## Decision boundary

This is a read-only design proposal. It makes no claim, registration,
worktree, message, deployment, restart, or cleanup change.

The desired outcome is reliable, legible agent coordination: one truthful
attempt tells a caller whether the deployed control plane accepted its request;
the registry records a lifecycle without silently forgetting it; and an
inspection operation cannot change the state it reports.

### Ruled matter to preserve

The previous Orchestrate handover records the psyche's decisions that
Orchestrate is a typed message board, keeps a worktree registry from agent
messages, and does no filesystem access or subprocess work. It also records
that the psyche authorized warnings for potentially stale entries, not deletion
or abandonment. These are treated as existing rulings, not proposals.

The same handover says the agent must push through a broken coordination
boundary rather than stop useful underlying work. That supports a single
bounded preflight and a visible fallback receipt. It does not by itself
authorize changing the current primary-wide requirement to claim before every
shared edit; that policy change needs psyche approval.

## Ground truth

### Live, on 2026-07-28 CEST

`orchestrate-daemon.service` is active/running since 12:29:47 and executes
`orchestrate-0.16.0`. The profile CLI, ordinary socket, meta socket, and upgrade
socket exist. The current-boot journal has no warning-level entry. This proves
the service/sockets are live; it does not prove every historical worktree
lifecycle completed.

No live request was sent for this proposal. That is intentional: the source
shows that some current observation paths reconcile state, so they are not a
safe read-only probe.

### Proven divergences

| Surface | Status | Evidence and consequence |
| --- | --- | --- |
| CLI success meaning | Wired but misleading | `src/bin/orchestrate.rs` and `src/bin/meta_orchestrate.rs` return success whenever transport/decoding succeeds. `tests/daemon_cli.rs` explicitly expects success for `PartialApplied` and typed refusals. A shell cannot distinguish acceptance from a semantic refusal. |
| Documentation/active skill | Stale deployment drift | Canonical `LiGoldragon/skills/skills/edit-coordination.md` has the exact command sequence and warns that refusals exit 0. The generated active `.agents/skills/edit-coordination/SKILL.md` lacks the commands and semantic-exit warning. The role generator currently includes only `general-instructions` and `tenets` universally, with no permission-scoped role-module mechanism. |
| Current `Observe` | Not read-only | `src/lane.rs` calls `reconcile()` from lane observations; terminal lane rows can be deleted after one hour. `src/execution.rs` reconciles bounded state at every ordinary write. The reclaimer re-enters via `Observe Lanes`. A read operation must not be relied upon as a non-mutating audit lens. |
| Stale worktree handling | Conflicts with ruling | `src/table_reclamation.rs` checks a registered path and deletes its worktree row when absent. This is daemon filesystem access and automatic forgetting of registry knowledge. |
| Request/conclude worktree | Wired, but conflicts with ruling | `src/worktree.rs` creates/checks checkouts and calls `jj`/`git`; conclusion also performs teardown and best-effort push/bookmark actions. The deployed Nix unit adds `jj`, `git`, and `gnupg` expressly for this behavior. Historic journal failures named precisely these runtime dependencies and malformed/missing worktrees. |
| Lifecycle proof | Partial and ephemeral | Tables hold snapshots (lanes, claims, worktrees) and some separate bounded triage records, but no single operation receipt joins request, semantic disposition, lane, claim, worktree registration, and conclusion. Terminal lane/worktree rows are reaped. A later observer therefore cannot distinguish never requested, refused, completed, or forgotten. |
| Historical active-lane reaper | Repaired in current source/deploy | Current `src/lane.rs` retains active/suspect lanes regardless of age; only explicitly terminal rows are eligible. The prior 24-hour active-lane reaper is historical deployed behavior, not an observed failure in the current service. |

The source and the historical handover are therefore consistent on one key
point: the 0.16 live claim/observe boundary works, while lifecycle observation,
worktree ownership, generated instructions, and semantic CLI exit behavior are
still not a coherent reliability contract.

## Smallest repair lane

Deliver one vertical slice, in this order. It changes no user worktree behind
the agent's back and introduces no second file mirror.

### 1. A truthful command outcome

Keep the typed NOTA reply on stdout. After printing it, both CLIs return:

| Result | Exit status |
| --- | --- |
| Accepted/success reply | 0 |
| Delivered semantic negative or partial result | 2 |
| Local parse, configuration, socket, or transport failure | 1 |

The classifier is protocol-owned and exhaustive over the generated ordinary and
meta output types, not a string match in a shell wrapper. `PartialApplied` is
status 2 even when it contains useful detail; the stdout record remains the
authoritative receipt. `LaneAlreadyRegistered` is status 2 for `FreshConflict`
and 0 for `RecoveryInherited` only if that is the contract's explicit accepted
recovery result. The implementation must enumerate any other conditional reply
variant rather than silently defaulting it to success.

This intentionally changes the CLI process contract. It does not change wire
frames, daemon availability, or the information printed to callers.

### 2. One non-mutating control-plane preflight

Add a read-only ordinary request, named provisionally `Observe ControlPlane`,
whose response contains only stable operational facts:

- component public version and build revision supplied by Nix at build time;
- ordinary/meta protocol revision and supported request families;
- whether this endpoint is declared non-reconciling;
- a fixed response schema/version.

It must read no `/proc`, worktree path, or store row and must not call any
reconciler, touch timestamp, arm a worker, or write a record. `Observe Lanes`,
`Observe Worktrees`, and lifecycle history must take the same pure read route.
Reconciliation, if retained for explicitly terminal temporary data, runs only
from a dedicated scheduled maintenance command/event, never from a read.

The write-capable coordination instruction becomes one exact attempt:

1. Run `orchestrate "(Observe ControlPlane)"` once and retain its request,
   executable/version, reply, and exit status.
2. If it returns 0 and advertises the required operation, make the one intended
   request and inspect both reply and status.
3. On 1, 2, malformed reply, missing capability, or stale build, record that
   compact receipt and take the task's independently safe fallback. Do not
   guess command names or retry the preflight.

The fallback needs an explicit policy decision for shared edits: either the
existing claim gate remains fail-closed, or the psyche authorizes a documented
fail-open exception after this receipt. The latter better matches the stated
aim of pushing through broken machinery, but it is not implied authority to
change the former.

### 3. One canonical lifecycle witness

Add append-only `LifecycleReceipt` records inside the Orchestrate SEMA store,
written atomically with the corresponding state transition. This is an event
history, not a filesystem projection or a mirrored registry.

Every receipt has an opaque operation id, operation kind, accepted/refused/
partial disposition, lane/session, optional claim scopes, optional worktree
identity, timestamp, and a typed reason code. It excludes free-form prompts,
file contents, credentials, and external command output.

The initial covered operations are: lane registration/recovery/retirement,
claim/release/handoff, worktree request/reservation, worktree registration, and
worktree conclusion. Refusals receive a receipt too. `Observe Lifecycle
(<filter> <cursor> <limit>)` returns chronological receipts with a hard limit
(for example 100) and a continuation cursor; it is read-only. This gives a
read-only work lens bounded output without pretending the current registry
snapshot is history.

### 4. Restore the ruled worktree boundary and preserve stale knowledge

Replace daemon worktree side effects with messages/state transitions:

- `RequestWorktree` reserves and records the intended repository, branch,
  lane, purpose, and deterministic destination. It does not inspect the
  checkout or invoke `jj`/`git`.
- The agent creates or reuses the worktree with `jj`, then sends a typed
  registration/activation message containing the actual absolute path and
  evidence it chooses to report. The daemon records it without scanning it.
- `ConcludeWorktree` records the named disposition and any supplied immutable
  landing reference; it never pushes, deletes a bookmark, removes a checkout,
  or infers a merge from the filesystem.
- A potentially stale worktree remains a registry record. A human/agent can
  submit an explicit `MarkWorktreeSuspect`/conclusion message with a typed
  reason. Nothing automatically abandons or deletes it from a missing path or
  elapsed time.

The old request/conclude commands may receive a one-release compatibility
period only if their replies clearly state `LegacyFilesystemActionDisabled` and
perform no external action. Do not silently retain their former `jj`/`git`
behavior. Remove the worktree scan/refresh operations as part of this slice;
they contradict the ruled source of truth.

## Exact mutation set

The following is the smallest coherent set. Exact generated paths may differ
after schema generation; source changes belong in the named repositories.

| Owner/repository | Change |
| --- | --- |
| `signal-orchestrate` | Extend the ordinary schema with pure `ControlPlane` and bounded `Lifecycle` observations; typed lifecycle receipt/disposition/reason structures; worktree reservation/activation/suspect transition shapes. Bump the wire/public behavior version. |
| `meta-signal-orchestrate` | Make meta lane lifecycle outcomes project into the same receipt model or expose the required receipt correlation id, then regenerate its schema. |
| `orchestrate` | Add exhaustive semantic-outcome classification to both CLIs; implement pure reads; add one store table and atomic receipt writes; replace filesystem-based worktree request/conclusion/refresh/reaping with message-board transitions; remove automatic terminal/missing-path deletion that destroys lifecycle evidence; add tests. Remove `worktree.rs` process/scan helpers only after their state-only successor is proven. Bump from 0.16.x for the changed CLI/protocol behavior. |
| `CriomOS-home` | Pin the compatible signal/meta/orchestrate revisions; pass a reproducible build revision into the control-plane response; remove `git`, `jj`, and `gnupg` from the daemon unit PATH and remove configuration inputs used only for daemon filesystem operations. Replace the grep-only PATH check with an evaluated service and integration witness. |
| `LiGoldragon/skills` | Update `edit-coordination` and `feature-development` to use the exact preflight, exit codes, receipt, safe fallback, agent-run worktree lifecycle, and no-retry rule. Add a permission-scoped write-role composition mechanism, then attach only this short operational module to `write-*` packets. Regenerate all target outputs; do not hand-edit `.agents`, `.claude`, `.codex`, or `.pi` artifacts. |
| Primary/canonical instructions | Update only after the psyche decides the fail-open/fail-closed fallback. Remove obsolete claims that RequestWorktree/ConcludeWorktree make or tear down a filesystem worktree. |

The current checked-out `orchestrate` main is `83e09a131634` and clean; the
deployed `CriomOS-home` input pins that same revision. This proposal does not
assume a newer local source is already deployed.

## What can break

- Shell callers and tests that equate successful transport with success will
  receive status 2 for refused/partial replies. This is deliberate and must be
  versioned/documented.
- Existing automation that expects Orchestrate to scaffold, push, bookmark, or
  remove worktrees will stop receiving those side effects. That is necessary to
  honor the ruled message-board boundary, but requires a migration notice and
  agent-side `jj` procedure.
- A one-release compatibility response can mask unfinished migration if it is
  not tested to be side-effect free.
- Removing automatic purges grows the store. Do not solve that by reviving
  deletion. Later retention needs an explicit archival/export decision and a
  witnessed recovery path.
- Schema changes require lockstep versions/pins for `signal-orchestrate`,
  `meta-signal-orchestrate`, Orchestrate, the generated clients, and the Nix
  deployment. Mixed versions should fail visibly in preflight, not at the first
  agent write.
- The existing task-level claim requirement may still block agents after a
  failed preflight unless the fallback policy is explicitly decided.

## Proof gates

1. Unit exhaustiveness: every ordinary/meta output variant is classified; each
   positive result exits 0 and each refusal/partial result prints valid NOTA and
   exits 2. Parse and transport failures exit 1.
2. Pure-read regression: run every `Observe` operation against a fixture with
   expired terminal lanes, terminal worktrees, and missing worktree paths;
   byte-for-byte store state and lifecycle count are unchanged before/after.
3. One-attempt integration: a fresh deployed CLI invokes `Observe
   ControlPlane` once, verifies its advertised versions/capabilities, performs
   one valid registration/claim (in an isolated fixture), and captures the
   exact receipts. A malformed/refused invocation produces exactly one receipt
   and no retry.
4. Lifecycle vertical witness: reserve/request, claim, register/activate,
   conclude, and retire a fixture worktree. A new daemon process reads the same
   bounded chronological receipt sequence with correlation ids and dispositions.
5. Side-effect prohibition: PATH omits `git`/`jj`; request, activation,
   conclusion, suspect marking, and all observations succeed/fail only by typed
   store behavior. A fixture asserts no checkout, ref, bookmark, or directory
   is created, removed, or inspected by the daemon.
6. Stale-record witness: a registered path is absent or becomes absent; pure
   observations preserve its record, and only an explicit suspect/conclusion
   request changes its status with a receipt.
7. Deployment witness: independently run Nix evaluation and build; activate
   only with approval; after activation, collect a fresh `Observe ControlPlane`
   response proving the pinned build revision, non-reconciling read capability,
   sockets, and expected exit behavior. Build/evaluation is not activation.
8. Generated-instruction audit: the write-role packet contains the one exact
   preflight/fallback instruction; read packets do not carry mutation-only
   commands; generated outputs match source and contain no retired command
   wording.

## Approval required

Psyche approval is required before implementation because this lane deliberately
changes public CLI exit semantics, removes daemon worktree side effects, changes
the deployed service, and may change the current claim-gate fallback. The
specific choice needed is:

> After one failed or refused, recorded control-plane preflight, may an agent
> make an otherwise-safe shared edit without an Orchestrate claim, or must it
> stop at the claim gate?

Recommended: authorize the narrow, receipt-backed fail-open exception for
otherwise-safe work, with no retries or speculative cleanup. It directly serves
the stated aim that broken orchestration must not intimidate agents into
abandoning useful work, while keeping the failure visible and bounded.
