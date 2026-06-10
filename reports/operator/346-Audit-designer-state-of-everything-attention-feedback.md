# Operator Feedback 346 — Designer 574 State of Everything

Target: `reports/designer/574-state-of-everything/`

This is an operator read of the designer state sweep, focused only on things that
clearly need attention. I spot-checked the highest-risk claims against the
current local repos after the report landed; this is not a full re-audit of all
75 crates.

## Headline

The report's core read is right: the fleet is not rotten, but the consumer side
is behind a fast-moving schema/NOTA foundation. The useful operator framing is
not "fix everything in the synthesis list"; it is "stabilize the wire/toolchain
surfaces first, then clean the local discipline debt."

One important freshness correction: the report measures against
`schema-rust-next` HEAD `eca4028`; the local `schema-rust-next` checkout is now
`cbe6f340`. Any dependency sweep should re-measure from today's HEAD before
landing. The report remains useful as a map, but not as an exact pin table.

## Clearly Needs Attention

### 1. Foundation pin sweep, but only as component-sized migrations

This is the top item. The qz6j no-alias change and private newtype fields mean
regeneration is expected to break consumers; treating this as a routine
`cargo update` would be wrong. The sweep should be staged one component triad at
a time: re-pin schema-next / schema-rust-next / nota-next, regenerate, absorb
newtype breaks, and land tests.

Current spot-checks confirm the report is already stale in the exact HEAD but
not stale in the risk: `spirit` still pins schema-rust-next `9f50920` while
linking nota-next `d8862b6`; `agent` still pins schema-rust-next `7282446` with
nota-next `d8862b6`; the Criome triad still pins nota-next `d8862b6` with older
schema-rust-next emitters.

### 2. Criome triad encoding split-brain

This is the sharpest concrete wire-risk I verified. `criome`, `signal-criome`,
and `meta-signal-criome` currently link nota-next `d8862b6`, while their
schema-rust-next pins are still `c0f76c2` / `261c779`. That matches the report's
warning: generated code and linked NOTA runtime sit on different encoding
points.

Action shape: either pull the triad back to the pre-bump nota-next point used by
the emitter, or advance the emitter/toolchain and regenerate all three together.
Do not leave one leg on the bumped NOTA runtime while another leg emits from the
old assumptions.

### 3. Spirit is not finished just because the `Version` operation landed

The newer operator work added `spirit Version`, moved daemon configuration into
`signal-spirit`, and bumped the crate to `0.4.0`. That does not close the
designer report's remaining Spirit blockers.

The current `spirit` repo still links nota-next `d8862b6` and pins
schema-rust-next `9f50920`. It also still owns the ordinary signal schema
locally (`schema/signal.schema`) even though the settled architecture says the
ordinary working Signal contract belongs in `signal-spirit` and the daemon
imports/wraps it. Treat Spirit as a high-priority migration target, not as
production-ready.

### 4. Lojix to CriomOS has a hard production blocker: durable storage

The report is correct and the current `lojix/triad-port` source confirms it:
state is still an in-memory `Mutex` store, with comments naming sema-engine/redb
as a future step. That violates the daemon self-resume rule and makes cutover
unsafe for an operator-owned deploy ledger.

Action shape: wire sema-engine/redb persistence and restart recovery before any
CriomOS service activation. The later CriomOS flake wiring and horizon shape
work are real, but durable storage is the first gate.

### 5. Hard NOTA quotation breaches are small and should be fixed immediately

The cloud bins still emit quoted fake-NOTA on error:
`cloud/src/bin/cloud-daemon.rs` prints `(DaemonRejected "{error}")`, and
`cloud/src/bin/cloud.rs` prints `(CliRejected "{error}")`. This violates the
workspace rule that NOTA strings come from bracket forms and never emit
quotation marks.

This is tiny, obvious, and high-signal. Fix it before larger schema sweeps so
the codebase stops teaching agents the wrong pattern.

### 6. Hand-assembled NOTA still exists in named sites

The designer report's worst fake-NOTA sites are still present in current source:
`signal-persona/src/origin.rs` hand-assembles several record variants with
`format!("(Tag {})")`; `persona-spirit/src/migration.rs` emits
`(MigrationCompleted ({}))`; `signal-system/src/lib.rs` emits
`(NiriWindow {})`.

These are concentrated enough to fix without a fleet migration. Prefer deriving
or routing through the real nota-next structural APIs; do not add more local
string assembly.

### 7. Meta-signal NOTA pin skew is low-effort cleanup

`meta-signal-introspect`, `meta-signal-system`, `meta-signal-harness`, and
`meta-signal-message` still pin nota-next `16493c8` while nearby siblings sit at
the pre-bump `ae5c25c` isolation point or older. This is lower severity than the
`d8862b6` split-brain because it is pre-bump, but it is exactly the kind of
small skew that makes later migrations harder to reason about.

Fold this into the next component-local re-pin rather than treating it as an
independent project.

## Defer or Down-Rank

The free-function count is useful as a discipline audit, but it should not drive
the next operator slice except where it intersects real runtime code. The
proc-macro helper count is especially low urgency. The recurring
`synthetic_exchange` / `io_error` / `encode_reply` patterns are worth fixing
when touching those crates for a real migration.

The stale `.concept.schema` cleanup is also real, but broad deletion across
~50 files is second-order unless paired with the component's actual re-pin /
regen. Deleting dead concept files is good hygiene; it is not the production
gate unless the stale file is actively misleading a current migration.

The skills-corpus trim belongs to designer, not operator. It is valuable, but it
should not compete with the schema/NOTA/deploy blockers above.

## Suggested Next Operator Order

1. Fix the tiny hard NOTA quotation breaches in `cloud`.
2. Pick one high-risk triad for a full foundation migration; Criome is the
   strongest candidate because the encoding split-brain is current and concrete.
3. Continue Spirit only as a migration target: update to current schema-rust-next,
   finish moving ordinary Signal ownership to `signal-spirit`, regenerate, and
   prove the daemon/CLI boundary.
4. For Lojix, do not wire CriomOS until sema-engine/redb persistence and restart
   recovery exist.
5. Fold dead concept-schema deletion and free-function cleanup into those
   component-sized migrations instead of opening a fleet-wide cleanup pass.

## Sources Read

- `reports/designer/574-state-of-everything/15-synthesis.md`
- `reports/designer/574-state-of-everything/3-spirit.md`
- `reports/designer/574-state-of-everything/6-terminal-harness.md`
- `reports/designer/574-state-of-everything/7-introspect-system.md`
- `reports/designer/574-state-of-everything/8-persona-agent.md`
- `reports/designer/574-state-of-everything/9-criome-ledger-upgrade.md`
- `reports/designer/574-state-of-everything/12-lojix-criomos-migration.md`
- Current spot-checks in `/git/github.com/LiGoldragon/{spirit,criome,signal-criome,meta-signal-criome,agent,cloud,signal-persona,persona-spirit,signal-system,lojix}`.
