# 103 - Reorientation after router witness

Role: `operator-assistant`

Purpose: reorient after closing `primary-o3m`, check open beads, compare recent
operator work against my lane, and name the decisions I need before the next
implementation pass.

## Short read

My lane is idle and cleanly reoriented.

- `primary-o3m` is done. `persona-router` commit `1186a2c3dd05` added the
  commit-before-delivery actor trace witness and closed the bead.
- `primary-m8x` is already closed. `persona-mind` commit `cacd8eb5` deleted
  `MindRuntime` and exposed the direct `ActorRef<MindRoot>` surface.
- The remaining assigned beads are `primary-46j`, `primary-aww`, and
  `primary-3ro`.
- `primary-2w6` is still the open P1 around `persona-message` migrating away
  from text files and polling, but it is not assigned to my role.

Current locks matter: operator holds `/git/github.com/LiGoldragon/persona` and
`/git/github.com/LiGoldragon/persona-mind`, so I should not edit either until
operator releases or explicitly coordinates.

## Recent operator work

Operator has moved `persona-mind` beyond the state described in older reports:

| Repo | Recent commits | Current effect |
|---|---|---|
| `persona-mind` | `8d3ecaaa`, `8e92072e`, `6133511e`, `e3954ff3`, `f8849a75` | socket Signal transport, Signal auth-derived actor identity, role claims through actor store, daemon-backed role CLI, packaged CLI binary check |
| `persona` | `d0e90cc7`, `0460def4`, `9c119908`, `0e6e6042` | removed shared Sema composition, added persona-trust/durable-agent positioning, advanced mind pins |

The important correction: the `mind` binary is no longer just a scaffold for
role-claim work. It has a daemon-backed role CLI for `RoleClaim`,
`RoleRelease`, and `RoleObservation`, plus a Nix `cli-binary` check that runs
the packaged binary against a daemon socket.

The limit is just as important: `persona-mind` has a durable claim table through
component-local Sema (`MindTables` / `ClaimLedger`), but memory/work graph state
is still in-memory and `RoleHandoff` / activity requests are still unsupported.
The process-restart witness exists as a Rust test; it is not yet the full
chained Nix artifact witness described in `skills/testing.md`.

## Bead status

### `primary-46j` - Niri push witness

This is still the cleanest next implementation target outside operator's lock.
`persona-system` is free, and the repo still has `NiriFocus` wrapping
`FocusTracker` while tests already assert the mailbox path.

The thing I almost missed: `primary-3ro` also wants `NiriFocus` collapsed into
`FocusTracker`. If I implement `primary-46j` exactly as written first, I may add
a witness to a wrapper that the next bead removes. Better shape: take the
`persona-system` slice of `primary-3ro` together with `primary-46j`, put the
mailbox on `FocusTracker`, then make the push witness target the final actor
shape.

### `primary-aww` - signal kernel extraction

Still valid and ready, but broad. It touches `signal`, `signal-core`, and
consumer imports. I would not interleave it with `primary-3ro`; both are
cross-cutting type-surface changes.

### `primary-3ro` - data type shadowing sweep

This bead needs splitting before implementation.

- `persona-system`: still valid, and probably should pair with `primary-46j`.
- `persona-message`: `Ledger` still wraps `MessageStore` and is still a valid
  collapse candidate.
- `persona-mind`: the old premise is stale. `StoreSupervisor` now wraps both
  `MemoryState` and `ClaimLedger`, and it owns real role-claim persistence. It
  may still be too dense, but the old "single data object wrapper" diagnosis is
  no longer exact. Also operator currently owns the repo.
- `persona-mind` `Config`: still looks deletable, but operator owns the repo.
- `persona-wezterm` `TerminalDelivery`: still exists, but designer/109 told me
  to stay out of the terminal-cell lane while the split decision is active. I
  should defer this piece unless you explicitly want it carved out.

### `primary-2w6` - persona-message off text/polling

This is the most important unassigned work item near my lane. It may supersede
the narrow `Ledger -> MessageStore` collapse because `MessageStore::tail` still
polls a text log and the store still writes `*.nota.log` files. Taking
`primary-2w6` means a larger design/implementation pass, not just a witness
patch.

## What I think I should do next

My preferred next move is:

1. Claim `primary-46j` plus the `persona-system` slice of `primary-3ro`.
2. Collapse `NiriFocus` into `FocusTracker` if the code still supports that
   cleanly.
3. Add `niri_subscription_cannot_poll_focus_snapshots` against the final actor
   shape and keep it under `nix flake check`.
4. Leave `persona-mind` and `persona-wezterm` portions of `primary-3ro`
   deferred with a bead comment, because both are currently coordination-risky.

Second choice: take `primary-aww` as a focused signal/signal-core session.

Third choice: take `primary-2w6`, but I would treat it as a larger migration
session rather than a quick bead.

## Questions

1. For `persona-system`, do you want me to combine `primary-46j` with the
   `primary-3ro` `NiriFocus -> FocusTracker` collapse so the push witness lands
   on the final actor shape?

2. Should I update `primary-3ro` with a split note now: mind portion stale and
   blocked by operator ownership, terminal portion deferred until the terminal
   split settles, system/message portions still ready?

3. Do you want me to keep following the assigned-bead order, or should I
   elevate the unassigned P1 `primary-2w6` after the Niri witness?
