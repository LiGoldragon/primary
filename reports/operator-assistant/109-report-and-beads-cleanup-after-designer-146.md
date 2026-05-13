# Operator-Assistant 109 - Report and BEADS Cleanup After Designer 146

Date: 2026-05-13  
Role: operator-assistant

## Scope

This is a small maintenance report after reading:

- `reports/designer/145-component-vs-binary-naming-correction.md`
  - `-daemon` is binary-file-level only; the component name stays
    `persona-message`.
- `reports/designer-assistant/37-signal-nexus-and-introspection-survey.md`
  - durable inspectable component state needs contract-owned typed record
    shapes, without moving database ownership out of the component.
- `reports/designer/146-introspection-component-and-contract-layer.md`
  - absorbs DA/37, adds planned `persona-introspect`, updates the relevant
    skills and active repo map, and adds terminal introspection as a
    forward-looking track on `primary-devn`.

I did not edit code or architecture docs in component repositories. Operator
currently holds the core Persona implementation repos. I only changed BEADS
state and wrote this report.

## Current Architecture Reading

`reports/designer/146-introspection-component-and-contract-layer.md` is now the
canonical reading of the introspection layer:

- `persona-introspect` is planned, high-privilege, live-first, and not part of
  the first six-component prototype.
- Live introspection asks the owning component daemon through Signal. It must
  not directly open another component's redb.
- Durable inspectable Sema records need contract-owned typed shapes:
  operational contracts when the record crosses a live boundary, introspection
  records when the record exists so the component can explain its own state.
- The first introspection implementation slice is terminal, inside
  `signal-persona-terminal` unless the record family grows enough to justify a
  sibling crate.

The skill absorption is present:

- `skills/rust/storage-and-wire.md` now states that Sema values are
  Signal-compatible rkyv archived records on disk, not text and not
  necessarily IPC frames.
- `skills/contract-repo.md` now has the carve-out for typed introspection
  record shapes while still forbidding contract crates from owning daemon code,
  redb access, reducers, actors, or projection policy.

The active repository map is also updated:

- `protocols/active-repositories.md` reserves planned
  `persona-introspect`.
- `protocols/active-repositories.md` reserves planned
  `signal-persona-introspect`.

## BEADS Cleanup Performed

### Closed stale composite bead

Closed:

- `primary-3ro` - `operator-assistant: apply data-type-shadowing rule across persona-* (5 actors - collapse 3, delete 2)`

Reason: the bead was no longer a live unit of work. Its five named slices had
drifted:

- `persona-system`'s NiriFocus wrapper has already been collapsed into
  `FocusTracker`.
- `persona-message/src/actors/ledger.rs` no longer exists.
- `persona-wezterm` is retired.
- `persona-mind/src/actors/store.rs` no longer exists at the cited path.
- The only still-live evidence I found is `persona-mind/src/actors/config.rs`,
  which remains a dead-looking actor around `StoreLocation`.

Replacement bead:

- `primary-nurz` - `persona-mind: remove dead Config actor or make store location state real`

That bead is narrow and current. It names the remaining live issue and has
`role:operator`, `repo:persona-mind`, `kameo`, and `cleanup` labels.

### Normalized old assistant-prefixed bead title

Updated:

- `primary-aww`

Old title:

```text
operator-assistant: complete signal vs signal-core kernel-extraction - remove duplicate kernel modules from signal
```

New title:

```text
signal: complete signal vs signal-core kernel extraction - remove duplicate kernel modules from signal
```

This keeps the work in the operator pool without the old assistant-role
prefix. I did not close it because the latest comment says it needs a
coordinated `signal-core` API expansion plus `signal` and consumer migration,
not a quick deletion pass.

## Beads I Left Open

I left `primary-devn` open. It is still the active umbrella for the prototype
source/test work from `reports/designer/142`, `reports/designer/143`, and
`reports/designer/144`. `reports/designer/146` added terminal introspection as
track 21, but explicitly says that track is not on the prototype-one critical
path.

I left `primary-2y5.4` open. `reports/designer/146` talks about
introspection and manager event-log placement, but it is not the full engine
manager catalog design report that `primary-2y5.4` asks for.

I left `primary-75t` and `primary-es9` open. Their dependency relation still
looks right: by-name terminal control and harness transcript-pointer work both
wait on the `persona-terminal` supervisor/gate-and-cache path.

## Residual Drift

There is still wording drift around the `-daemon` naming rule in docs outside
the specific repos already fixed by operator/designer commits.

Examples:

- `protocols/active-repositories.md` still says external ingress arrives via
  `persona-message-daemon`. That is acceptable when it means the binary, but
  the row could read more cleanly as "`persona-message` binds `message.sock`
  through its daemon binary `persona-message-daemon`."
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` still has a few
  file-level/component-level mixed phrases such as "stateless components
  (today: `persona-message-daemon`, `persona-system` in skeleton mode)".
  Per `reports/designer/145-component-vs-binary-naming-correction.md`, the
  component phrase should be `persona-message`; the binary remains
  `persona-message-daemon`.

I did not edit these because the affected surfaces are designer/protocol or
operator-locked component docs. They are small follow-up cleanup, not a reason
to block current implementation.

## Current Best Next Work

For operator-assistant, the clean next implementation candidate is
`primary-nurz` once `persona-mind` is not locked: remove the dead Config actor
or make it real with a Kameo message path and Nix-backed witness.

For operator, the current high-signal path remains `primary-devn`: land the
six-component prototype witnesses before starting the `persona-introspect`
daemon. Terminal introspection records can follow after the prototype is real.
