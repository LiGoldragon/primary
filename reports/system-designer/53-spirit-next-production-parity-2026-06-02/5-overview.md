# Overview — spirit-next production-parity audit synthesis — 2026-06-02

*Orchestrator synthesis of the four sub-agent reports. Surfaces what
each found, the cross-cutting picture, and a prioritised path-to-ship.*

## The picture, in one paragraph

The deployment INFRASTRUCTURE for a side-by-side spirit-next slot
already exists in CriomOS-home (per-slot CLI wrapper, per-slot systemd
user service, per-slot state directory + sockets, cutover machinery as
a one-line `currentDefault` change, end-to-end home-manager check).
The SCHEMA-DERIVED PILOT at `/git/github.com/LiGoldragon/spirit-next/`
builds locally, passes 41 tests, and serves every operation it declares
end-to-end via daemon + CLI round-trip — sub-agent 2 verified this with
a real daemon spawn against a `/tmp` state directory. BUT (1) the
deployment is currently pointed at the wrong target — `persona-spirit-
next.url` in CriomOS-home tracks `persona-spirit?ref=main`, so today
TWO copies of persona-spirit v0.3.0 run side-by-side, and the schema-
derived pilot is unreferenced by the deploy layer; (2) the pilot's wire
shape is structurally disjoint from production's (only operation root
names overlap; payloads, replies, selector enums, codec library all
differ); (3) the pilot's persisted record shape is byte-incompatible
with production's on three axes (missing `Magnitude::Zero`, missing
date/time stamping on `Entry`, redb major-version difference); and
(4) the pushed remote build is one-input-bump-blocked by stale
`flake.lock` for `schema-rust-next-source`. The path-to-ship is
*short* for incubation (one flake-lock bump + one CriomOS-home
flake-input redirect + one home-manager config-materialisation snippet)
and *longer* for parity (~9 schema additions to spirit-next, decided in
order, designer-shape work in worktrees) and *unspecified* for
historical-record migration (zero tooling exists; designer 447's
upgrade-as-SEMA is the eventual mechanism but hasn't started).

## Sub-agent findings

### SA1 — Wire-shape parity (verdict: DISJOINT)

Production deployed wire contract: `signal-persona-spirit @ 4c7b51ff`
(= main HEAD, no drift); production daemon `persona-spirit @ df09280a`
(= tag v0.3.0); `Magnitude::Zero` lives at `signal-sema
ee61fef:src/magnitude.rs:1-15` with explicit Spirit-1249 stability
comment.

Spirit-next at main `7c350679` carries an in-repo schema (`schema/lib.schema`,
`src/schema/lib.rs`) and references NONE of the production signal crates.
The codec is `nota-next` (vs production's `nota-codec`). The operation
vocabulary is disjoint — 7 of 8 production roots are missing
(`State`, `Watch`, `Unwatch`, `Tap`, `Untap`, `ChangeCertainty`,
plus the wrapped-`Observe` form). Spirit-next adds `Lookup`, `Count`,
`Error`, `Rejected`, plus a `DatabaseMarker` provenance envelope on
every reply.

Daily-use cutover requires nine specific schema additions to spirit-
next: `Zero`, `State`, `RecordedTime` + `Date`/`Time` stamping,
`RecordIdentifier` on observed entries, `RecordedTimeSelection`,
`TopicMatch::Any`, `CertaintySelection`, `ObservationMode`,
`ChangeCertainty`. Subscription/Tap surface deferrable.

### SA2 — Build + test + run (verdict: ALMOST USABLE)

Spirit-next builds locally and serves every wire operation it declares
end-to-end today. 41/0/9 tests pass on `nota-text` feature; 45/0/9
with `testing-trace`. All tests substantive (real daemon spawn, real
socket round-trip, real redb durability — no placeholder bodies).
Sub-agent 2 spawned a daemon against `/tmp`, round-tripped all five
declared input operations (`Record / Observe / Lookup / Count /
Remove`), saw `EmptyTopic` validation rejection work, saw durability
across daemon restart, saw multi-topic queries work. Local-built and
Nix-built binaries behave identically. Production daemon untouched
throughout; test artifacts cleaned.

**Remote build BLOCKED on stale `flake.lock`**. Build from
`github:LiGoldragon/spirit-next/7c350679` fails at `build.rs:88` with
*"checked-in generated schema source is stale"* — `flake.lock` pins
`schema-rust-next-source @ d3ec9f91` while `Cargo.lock` pins
`schema-rust-next @ a8c0f012` (newer). The Nix sandbox vendors the
older emitter, regenerates source that differs from the checked-in
generated code, freshness check panics. Fix is a one-input
`nix flake update schema-rust-next-source` + commit + push.

Reply-shape divergence: every spirit-next reply bundles a
`DatabaseMarker` (commit-sequence digest) after the payload. A
consumer expecting `(RecordAccepted N)` would mis-parse
`(RecordAccepted (N (1 ...)))`. This is design intent (Spirit 1389
slim-Nexus-output / provenance envelope), not a defect — but it makes
clients written against v0.3.0 incompatible.

Daemon configuration is binary rkyv only per Spirit 1373 (no NOTA
between components). Home-manager deploy needs an activation snippet
to emit the rkyv config from a typed Nix expression.

### SA3 — Deployment configuration (verdict: SLOT INFRASTRUCTURE READY)

The CriomOS-home deploy chain already implements:

- Per-slot CLI wrapper: `~/.nix-profile/bin/spirit-next` is a wrapper
  with `PERSONA_SPIRIT_NEXT_SOCKET` env vars routing to
  `~/.local/state/persona-spirit/next/` sockets + redb.
- Per-slot systemd user service:
  `persona-spirit-daemon-next.service` is active and running.
- Per-slot daemon NOTA-shaped configuration (cf. SA2 finding — actually
  binary rkyv per Spirit 1373).
- Cutover machinery: `currentDefault = "next"` is a one-line change at
  `modules/home/profiles/min/spirit.nix:175-179`.
- End-to-end home-manager check at
  `checks/persona-spirit-versioned-deployment/default.nix`.

The two gaps:

1. **Wrong target**: `persona-spirit-next.url =
   "github:LiGoldragon/persona-spirit?ref=main"` currently resolves to
   the same commit `df09280` as v0.3.0 — both daemons run identical
   binaries against separate state. To deploy the actual schema-
   derived pilot, this input must repoint at the spirit-next REPO.
2. **Data-staleness**: spirit-next's pilot redb (if SA4's findings about
   the seeded pilot db apply) stops at record ~708 (May 25 seeding);
   production has reached 1375+. Stale by ~667 records.

Side-by-side safety is fully verified through code + check coverage.

### SA4 — Data + storage compatibility (verdict: BYTE-INCOMPATIBLE)

Spirit-next's pilot redb is byte-incompatible with production v0.3.0
on three independent axes:

1. **Magnitude variant set** (active Spirit 1249 mismatch). Production
   has 8 variants with `Zero=7` appended last per Spirit 1249 stability
   rule. Pilot schema source omits Zero entirely (7 variants).
   Discriminants 0..6 happen to align — Minimum through Maximum decode
   bytewise correctly — but any production record with `certainty =
   Zero` would bytecheck-fail. The removal-candidate workflow does
   mint Zero, so this is live.
2. **Entry shape diverges**: production's `StampedEntry { entry, date,
   time }` wraps Entry with daemon-stamped provenance. Pilot's
   `Entry { topics, kind, description, magnitude }` has no date/time
   field at all.
3. **Redb major-version + infrastructure tables**: production uses
   sema-engine on redb 4 with `__sema_meta` / `__sema_headers`
   infrastructure tables and a hard-fail schema-version guard, plus
   decimal-string identifier keys. Pilot opens redb 2.6.3 directly with
   `u64` integer keys and no schema-version guard.

Zero migration tooling exists. The `migrate_v020_to_next` in
persona-spirit refers to a DIFFERENT "next" — production v0.3.0, NOT
the schema-derived pilot.

Empty-database side-by-side incubation is the only viable starting
state today.

The eventual cutover should follow the historical-shape reader
pattern documented in `skills/spirit-cli.md` §"Substrate migration
discipline" — `mod historical / mod current_shape` two-submodule
pattern reading the on-disk bytes through legacy types and re-emitting
into the new shape via a one-shot tool.

## Cross-cutting picture

### The deployment-infrastructure surprise

The most surprising finding is SA3's: the slot infrastructure for a
side-by-side spirit-next is fully implemented and running today, but
it's pointed at the wrong target. This means the cost of "spirit-next
in production, side-by-side" is much smaller than expected — the home-
manager mechanics are done. What's missing is a flake-input redirect
+ a config-materialisation snippet.

### The naming overload

`spirit-next` means three different things in different layers:

- **Deployment layer (CriomOS-home)**: `spirit-next` is a wrapper
  binary in `~/.nix-profile/bin/` pointing at a daemon-with-separate-
  state. Today the binary is persona-spirit v0.3.0.
- **Workspace tagline**: `spirit-next` is the *project* — the canonical
  engine-trait worked example in the schema-derived stack.
- **Repo**: `/git/github.com/LiGoldragon/spirit-next/` is the actual
  pilot's source code.

This conflation makes audit reading harder than necessary. Worth
naming the wedge in the deployment vocabulary.

### What "production parity" actually means

The Spirit Next pilot is not a refinement of persona-spirit v0.3.0 —
it's a *different system* sharing the same problem domain. The
operation vocabulary diverges (`Lookup` + `Count` are new design
direction per Spirit 1389; the `DatabaseMarker` envelope is provenance
discipline per the engine-trait pattern). Wire-level identical replay
is not a goal of the pilot.

"Production parity" in the user's sense reads as: spirit-next can
serve a working agent's daily intent capture + observation needs
WITHOUT requiring users to learn a new vocabulary. That target is
achievable through the 9 schema additions identified by SA1 — none
contentious, mostly mechanical (append Zero, add date/time stamping,
add State + ChangeCertainty operation roots, add the missing
selector variants).

### What's blocking each phase

| Phase | Goal | Blocker | Cost |
|---|---|---|---|
| 1 | Pushed remote build works | Single stale flake input | 5 minutes |
| 2 | Deploy actual pilot to next slot | CriomOS-home flake input + config-materialisation snippet | hours |
| 3 | Wire-shape parity for daily use | 9 schema additions | days (designer-shape) |
| 4 | Historical record availability | Migration tool from production redb | weeks (designer 447) |
| 5 | Cutover (next → production) | All of 1-4 + a `currentDefault` flip | one-line change |

## Path-to-ship — prioritised

### Now (immediately actionable)

**Phase 1 — `flake.lock` bump.** One commit on a spirit-next worktree.
Bump `schema-rust-next-source`, push. Pushed remote builds again.
Operator-shape work; designer-worktree discipline; ~5 minutes wall
time.

### Soon (this week if user wants the slot live)

**Phase 2 — point the spirit-next slot at the actual pilot.** Two
sub-tasks:

- CriomOS-home: change `persona-spirit-next.url` from
  `github:LiGoldragon/persona-spirit?ref=main` to
  `github:LiGoldragon/spirit-next?ref=main`. Add a home-manager
  activation snippet that materialises the rkyv binary config from a
  Nix expression (the daemon takes a single rkyv config argument per
  Spirit 1373). Update the home-manager check to exercise the new
  daemon's wire vocabulary.
- Spirit-next: confirm the daemon's config schema is stable enough to
  drive from Nix without flag-soup.

System-operator + designer collaboration; ~half-day to a day of work.

After Phase 2, the slot would serve the pilot's wire vocabulary (not
v0.3.0's), starting empty. Daily intent capture would still happen
against production v0.3.0 (`spirit -> spirit-v0.3.0`); spirit-next
becomes an experimental harness an agent can opt into.

### Iterative (designer-shape worktrees, one capability at a time per Spirit 1355)

**Phase 3 — schema additions for daily-use parity.** Order suggested
by SA1 (Maximum-leverage first):

1. `Magnitude::Zero` appended (Spirit 1249 discipline; closes the
   removal-candidate workflow gap).
2. `Entry → StampedEntry` with daemon-stamped date/time (closes the
   `RecordedTime` and FormatSelection `WithProvenance` gap).
3. `RecordIdentifier` carried on every observed row (so observed
   records can be referenced for follow-up `Lookup`/`Remove` from the
   reply alone).
4. `RecordedTimeSelection` variants (Any / Between / Since / Until /
   Shallow / Recent / Deep / VeryDeep).
5. `TopicMatch::Any` variant (alongside existing Partial/Full).
6. `CertaintySelection` selector enum (Any / Exact / AtMost / AtLeast).
7. `ChangeCertainty` operation root.
8. `State` operation root.
9. Defer `Watch / Unwatch / Tap / Untap` — production's CLI doesn't
   use them; agent code uses a typed client library which can be
   built on top later.

Each landing is a worktree + a pushed branch + an operator pull onto
main. Each is independently testable (extend the existing test suite).

### Eventually (gated on designer 447)

**Phase 4 — historical record migration.** Production has ~1375+
records. When the pilot reaches feature parity AND psyche directs
cutover, build a one-shot tool that reads production's redb through
historical-shape decoders and re-emits as spirit-next records via the
Record operation. Designer 447's upgrade-as-SEMA is the eventual
mechanism. Until designer 447 starts, this phase stays in spec.

### Cutover

**Phase 5 — `currentDefault = "next"`.** Single line. Trivial once
phases 1-4 are complete. Per `modules/home/profiles/min/spirit.nix:175-179`.

## Open questions for psyche

1. **Phase 2 timing.** Should we deploy the actual pilot into the
   `next` slot now (Phase 2) and let it accumulate days of feedback,
   or wait for some Phase 3 schema additions first?
2. **DatabaseMarker reply envelope.** Spirit-next bundles a provenance
   envelope on every reply — design intent per Spirit 1389 slim-Nexus-
   output. Is this the right shape for daily-use CLI? It makes replies
   harder to read at a glance ("`(RecordAccepted (N (1 ...)))`" vs
   `(RecordAccepted N)`). Possibly a CLI-side projection drops the
   envelope for terminal display while preserving it on the wire.
3. **Migration eventually-required vs eventually-discardable.** Are
   today's 1375+ production records worth migrating to the pilot's
   shape, or are they "previous-era" intent we treat as historical
   reference (read-only, accessed only when needed)?
4. **Lookup + Count divergence.** Spirit-next adds `Lookup` (by
   identifier) + `Count` (aggregate). Production has neither. These
   are useful additions; they shouldn't go away. Confirm direction.

## Recommendations

### Immediate (orchestrator-shape this turn)

- **Phase 1 — flake.lock bump.** Open worktree at
  `~/wt/github.com/LiGoldragon/spirit-next/flake-lock-bump-2026-06-02/`,
  run `nix flake update schema-rust-next-source`, commit, push.
  Verifies the pushed remote builds. Tiny, mechanical, gates Phase 2.

### Surfaced for psyche

- Phase 2 (deploy actual pilot to next slot): half-day to a day; ready
  to begin once Phase 1 lands and psyche directs.
- Phase 3 (schema additions, one capability at a time per Spirit
  1355): designer-shape worktree work; proceed one at a time on user
  authorisation.
- Phase 4 (historical migration): gated on designer 447 starting.

### Tracked

- Naming clarification in deployment layer (`spirit-next` slot name vs
  spirit-next pilot binary) — small skill or repo INTENT addition
  could disambiguate.
- Spirit-next's reply-envelope shape (`DatabaseMarker` per Spirit
  1389) needs CLI-projection thinking when daily-use deployment lands.

## See also

- `0-frame-and-method.md` — orchestrator frame
- `1-wire-shape-parity-audit.md` — SA1 wire shapes
- `2-build-test-run-audit.md` — SA2 empirical build + smoke test
- `3-deployment-configuration-audit.md` — SA3 deployment chain
- `4-data-and-storage-compatibility.md` — SA4 storage compatibility
- Predecessor (retired): no direct predecessor — first system-designer
  audit explicitly on the spirit-next path-to-ship
- Related: `reports/system-designer/51-recent-work-audit-2026-06-02/`
  §"F4 persona-spirit is the deployment gap" surfaced the same picture
  from the workspace-wide audit angle
- `skills/spirit-cli.md` §"Deployment slots" — the side-by-side model
- `skills/spirit-cli.md` §"Substrate migration discipline" — the
  historical-shape-reader pattern for Phase 4
- Anchoring Spirit records: 1242 (deployment-slot model), 1249
  (discriminant stability), 1322 (build-time compilation), 1327
  (engine-trait Principle), 1357 (engine-trait LIVE in spirit-next),
  1373 (no NOTA between components), 1389 (slim-Nexus-output)
