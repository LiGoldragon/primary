# 272.3 — Implementation

## Actions taken

Created and pushed the frame/verification/decision reports first:

- `6892782b` — `operator: frame bead staleness implementation`
- `447898f4` — `operator: verify bead staleness audit`

Then claimed the operator task lock:

```sh
tools/orchestrate claim operator '[bead-staleness-audit-implementation-2026-06-01]' -- implement verified bead staleness cleanup from designer 449
```

## Beads closed

Closed 60 open beads. Open count moved from 269 to 209.

### Persona-spirit handover/cutover

Closed as superseded by upgrade-as-SEMA and the schema-daemon /
upgrade-daemon path from designer 447:

- `primary-602y` — rebuild persona-spirit v0.1.0.1 retrofit.
- `primary-0jjz` — v0.1.0 to v0.1.1 brief-outage cutover.
- `primary-1jql` — in-transition messages probe.
- `primary-ekxx` — signal-version-handover as schema-derived pilot.
- `primary-x3ci.1` — production pre-migration step.
- `primary-dlut` — nspawn handover socket protocol.
- `primary-tfdj` — quarantine gate sandbox.
- `primary-l9iz` — quarantine policy gate.
- `primary-x3ci` — v0.1.1 migrated-database cutover, retried after its
  stale blockers closed.

### Legacy signal_channel and Tap substrate

Closed as superseded by schema-emitted Signal/Nexus/SEMA through
`nota-next`, `schema-next`, and `schema-rust-next`:

- `primary-k8cn` — three-tier subscription delivery sandbox.
- `primary-2py5` — `signal-sema` LogVariant impl.
- `primary-b86d` — observable block in `signal_channel!`.
- `primary-9dce` — section-vs-socket validation listener.
- `primary-uq04` — component CLI `signal_cli!` sweep.
- `primary-3cl1` — `frame_micro()` projection emit.
- `primary-bg9l` — LogSummary trait.
- `primary-l02o` — LogVariant trait + derive macro.
- `primary-v5n2` — contract-section grammar.
- `primary-ezqx` — consolidated macro epic.
- `primary-ezqx.1` — MVP schema-language pilot in old macro path.
- `primary-ezqx.3` — recursive Help-on-every-enum macro emission.
- `primary-muu2` — persona triad contract-section pilot.
- `primary-bann` — persona-spirit Tap point.
- `primary-145a` — persona-introspect Tap subscriber.
- `primary-8avm` — DeliveryTraceKey/Tap correlation.
- `primary-g21y` — golden-ratio adoption sweep, closed after its
  stale blocker `primary-muu2` closed.

### Persona-prefix rename remnants

Closed as superseded by the spirit fold:

- `primary-0m1u.11` — R11 rename spirit triad.
- `primary-0m1u.12` — R12 persona meta and CriomOS-home repin.
- `primary-0m1u` — persona-prefix rename epic.

### Persona-stack migration backlog

Closed as superseded by designer 446's wave plan: stateful persona
runtimes port in wave 2 after schema-core extraction, not through the
old signal-executor v4 recipe:

- `primary-a5hu` — persona engine epic.
- `primary-4naq` — signal-executor v4 migration epic.
- `primary-c620` — persona-orchestrate triad.
- `primary-gu7t` — persona-harness triad.
- `primary-qjdp` — persona-terminal triad.
- `primary-21gn` — persona-system triad.
- `primary-krbi` — persona-message triad.
- `primary-li7a` — persona-introspect triad.
- `primary-aunn` — persona-router triad.
- `primary-e1pm` — persona-mind triad.
- `primary-gvgj` — persona-agent epic.
- `primary-gvgj.3` through `primary-gvgj.10` — persona-agent daemon,
  backend, router, and harness-retirement children.
- `primary-nobf` — persona supervision/lifecycle.
- `primary-q98d` — persona upgrade orchestration.
- `primary-wvdl` — Persona port plus upgrade orchestration.
- `primary-hj4` — persona-mind channel choreography.
- `primary-hj4.1` — persona-mind typed graph.
- `primary-devn` — MessageProxy/supervision reducer work.
- `primary-8n8` — persona-terminal supervisor socket.
- `primary-07ot` — persona-router 4-hop durability chain.
- `primary-ojxq` — persona-spirit new triad component.
- `primary-0bls` — old "current foundation" criome migration bead.
- `primary-9up1` — old "current foundation" lojix migration bead.

### Shipped bead

Closed `primary-duuv` — DatabaseMarker on every signal reply — as
shipped. Its own notes say acceptance was met, and designer 444 names
DatabaseMarker/SemaReceipt propagation as live. Follow-up durability and
content-addressing remain separate work.

## Beads updated

Kept these open and refreshed them:

- `primary-kbmi` — removed `role:system-specialist`, added
  `role:operator`, appended a note anchoring the work at designer 446
  Phase 1a cloud wave.
- `primary-kbmi.2` — same label update and Phase 1a domain-criome
  runtime note.
- `primary-a1px` — appended a note anchoring the OutputNexus dispatcher
  follow-up at designer 446 Phase 0 spirit fold.

## BEADS persistence

Ran:

```sh
bd dolt commit -m "operator: close stale bead arcs from audit 449"
bd dolt push
```

The Dolt commit command reported `Nothing to commit`, which means the
configured BEADS write mode had already committed the writes. `bd dolt
push` completed successfully.

## Verification

Sequential verification reads after cleanup:

```sh
bd --readonly count --status open
bd --readonly count --status open --by-priority
bd --readonly list --status open --priority P0 --limit 0 --flat --no-pager
bd --readonly list --status open --label persona-prefix-rename --limit 0 --flat --no-pager
bd --readonly list --status open --label signal-channel --limit 0 --flat --no-pager
bd --readonly list --status open --label signal-executor --limit 0 --flat --no-pager
bd --readonly list --status open --label persona-spirit --limit 0 --flat --no-pager
bd --readonly list --status open --title persona --priority P1 --limit 0 --flat --no-pager
```

Results:

- Open count: 209.
- Priority distribution: P1 15, P2 146, P3 48; no P0 beads remain.
- No open beads remain with labels `persona-prefix-rename`,
  `signal-channel`, `signal-executor`, or `persona-spirit`.
- No open P1 bead title contains `persona`.
- Remaining P1s are live or deliberately left for owner-context:
  `primary-a1px`, `primary-9hx0`, `primary-lrf8`, `primary-srmq`,
  `primary-54ti`, `primary-kbmi.2`, `primary-kbmi`,
  `primary-36iq.6.1`, `primary-36iq.3`, `primary-36iq`,
  `primary-c2da`, `primary-izze`, `primary-at7x`, `primary-ipjx`,
  and `primary-ffew`.

Released the operator task lock:

```sh
tools/orchestrate release operator
```

The operator lock is idle after release.
