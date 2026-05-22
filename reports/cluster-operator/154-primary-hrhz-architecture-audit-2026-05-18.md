# primary-hrhz architecture audit - 2026-05-18

## Scope

Audit of the `primary-hrhz` carveout after moving ordinary
role/activity orchestration out of `persona-mind` /
`signal-persona-mind` and into the new `persona-orchestrate` /
`signal-persona-orchestrate` component pair.

The architectural yardsticks were:

- `skills/component-triad.md`: stateful component equals daemon + thin
  CLI + Signal contract, with authority surfaces split by contract.
- `primary-699g`: `persona-orchestrate` is a full triad daemon with
  sema-engine state; ordinary `signal-persona-orchestrate` handles
  peer/CLI role and activity records; owner-signal repos handle
  privileged lane registry and downstream orders.
- `persona/ARCHITECTURE.md`: `persona-mind` owns central mind state;
  `persona-orchestrate` owns ordinary role claims, handoffs, activity,
  and future execution orchestration under mind authority.

## Verdict

The boundary cut is directionally correct. Ordinary role claims,
handoffs, observations, and activity no longer live in the mind
runtime/contract. The new ordinary contract crate has no runtime, and
`persona-orchestrate` owns a sema-engine-backed store for the carved
state. The apex `persona` lock now points at the audited commits.

The slice is still not the full intended `persona-orchestrate` triad.
The daemon and thin CLI are still scaffolds, owner-signal surfaces are
not created, lane registry is not implemented, and `tools/orchestrate`
still writes compatibility lock files directly.

## Gaps filled in this audit

1. Current workspace lane coverage.

   `signal-persona-orchestrate::RoleName` and
   `signal-persona-mind::RoleName` now include:

   - `second-operator-assistant`
   - `second-designer-assistant`
   - `second-system-assistant`

   This closes the immediate mismatch between the closed contract role
   enums and `orchestrate/AGENTS.md` / `skills/role-lanes.md`.

2. Transitional CLI projection.

   `/home/li/primary/orchestrate-cli` now maps second-assistant lanes to
   the matching `signal-persona-orchestrate::RoleName` variants instead
   of collapsing them onto first-assistant roles.

3. Ledger edge fixes.

   `persona-orchestrate` now:

   - serializes `OrchestrateService::handle` calls with a process-local
     sequence lock until the daemon actor becomes the real sequencer;
   - treats path-prefix activity filters as path-boundary matches, so
     `/git/.../persona` does not match `/git/.../persona-orchestrate`;
   - has witness tests for full lane snapshots and prefix-boundary
     filtering;
   - refreshes README, skills, and architecture wording around
     `sema-engine`, `persona-orchestrate.redb`, and mind/orchestrate
     ownership.

4. Locks and apex wiring.

   Consumer locks now point at the audited commits:

   - `signal-persona-orchestrate`: `0251c888`
   - `signal-persona-mind`: `115eb908`
   - `persona-orchestrate`: `be5dfa2a`
   - `persona-mind`: `168d2296`
   - `persona`: `92fa1d2`

## Remaining architectural gaps

1. The `persona-orchestrate` triad is not complete.

   The runtime repo has a library and a `persona-orchestrate-daemon`
   scaffold, but not a long-lived daemon that accepts
   `OrchestrateFrame` over a socket. There is no thin `persona-orchestrate`
   CLI that accepts one NOTA request and prints one NOTA reply through
   exactly one Signal peer. The component-triad witness tests for CLI
   peer count, Signal-only daemon traffic, and non-bypass are therefore
   not yet present.

2. OwnerSignal is still absent.

   `primary-699g` calls for `owner-signal-persona-orchestrate`,
   `owner-signal-persona-router`, and `owner-signal-persona-harness`.
   None exist yet. That means privileged lane registry mutation,
   downstream router orders, and harness executor-management orders are
   still future architecture rather than implemented surfaces.

3. Lane registry is not implemented.

   The audit patched the closed role enums to include today's lanes, but
   that is an interim repair. The intended architecture dissolves role
   churn by moving lane definitions into `persona-orchestrate` state,
   mutated through owner-signal and observed/subscribed through the
   ordinary surface.

4. Ordinary subscribe surface is missing.

   The ordinary contract has `Match`-style observations and activity
   queries, but no `Subscribe` variants for role state, activity, or lane
   registry observations. This is not aligned with the push-not-poll
   destination in `primary-699g`.

5. Storage transaction witnesses are weaker than the destination.

   `sema::Table` exposes typed `get`/`iter` over read transactions and
   typed `insert`/`remove` over write transactions. That prevented a
   clean read-decide-write transaction in `persona-orchestrate` without
   dropping below the typed table API. The audit added service-level
   sequencing, which is enough for a single daemon process, but the
   storage layer still lacks an architectural-truth witness that conflict
   detection and activity slot allocation happen in one typed write
   transaction.

6. Lock-file compatibility is still inverted.

   `tools/orchestrate` / `orchestrate-cli` still writes lock files as the
   live compatibility surface. The intended replacement path is
   `persona-orchestrate` owning durable records and projecting lock files
   only as temporary compatibility views.

7. Handoff semantics may be underspecified.

   Current handoff requires the source role to hold each handed-off scope
   exactly. If `operator` holds `/git/.../persona`, it cannot hand off
   `/git/.../persona/ARCHITECTURE.md` without first reshaping the claim.
   That may be correct, but it should be explicit before agents rely on
   sub-scope delegation.

8. Activity query shape may need a cursor.

   `ActivityAcknowledgment` returns a store slot, but `Activity` records
   returned by query do not include the slot. Without the slot, stable
   pagination, replay, and subscription catch-up are harder.

## Best questions

1. Should the next implementation pass finish the ordinary triad first,
   or jump straight to owner-signal?

   Ordinary-first means: real `persona-orchestrate-daemon`, thin
   `persona-orchestrate` CLI, Signal socket, lock-file projection, and
   triad witness tests. Owner-first means: build the privileged contract
   chain and lane registry before replacing the helper. Ordinary-first is
   smaller and makes the current carveout real; owner-first gets closer
   to the final authority model.

2. Is `RoleName` still allowed in `signal-persona-mind` once lane
   registry lands?

   Mind graph records still use role identity. If lane identity becomes
   dynamic orchestrate state, mind probably should store a typed
   `LaneIdentifier` or actor identity, not another closed `RoleName`
   enum. The compatibility bridge needs a clear boundary.

3. Should `sema` grow typed read-during-write/update helpers?

   The current table API made storage-transaction atomicity awkward for
   claim conflict detection and activity slot minting. A typed
   `Table::get_for_update`, `Table::iter_for_update`, or
   `Engine::update` helper would let components prove read-decide-write
   invariants without bypassing the typed table layer.

4. Are sub-scope handoffs valid?

   Exact-only handoff is simple and avoids implicit claim splitting.
   Sub-scope handoff is more ergonomic for large repo claims but requires
   explicit split semantics and tests.

5. Should activity query records expose the store slot?

   Keeping slot only in the acknowledgment is enough for append
   confirmation. Exposing it in query results would make pagination,
   replay, and subscription catch-up explicit.

6. What is the first owner-signal lane-registry migration shape?

   The likely path is: bootstrap from `orchestrate/roles.list`, store
   lane records in `persona-orchestrate.redb`, expose read-only ordinary
   observation/subscription, then stop compiling new lanes into the
   ordinary contract. The open decision is whether lock-file lanes remain
   a generated projection during that cutover or become a separate import
   command.

## Verification

- `signal-persona-orchestrate`: `cargo test`; `nix flake check -L`.
- `signal-persona-mind`: `cargo test`; `nix flake check -L`.
- `persona-orchestrate`: `cargo test`; `nix flake check -L`.
- `persona-mind`: `cargo test`; `nix flake check -L`.
- `/home/li/primary/orchestrate-cli`: `cargo test`.
- `persona`: `nix flake check -L`.

Known check noise:

- several flakes omit incompatible non-Linux systems;
- `persona` and component app outputs still warn about missing app
  `meta` attributes;
- `persona` check was run with a dirty tree because `flake.lock` had
  not yet been committed during the check.
