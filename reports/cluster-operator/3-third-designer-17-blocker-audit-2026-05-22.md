# Third-designer 17 blocker audit

## Scope

Audited `reports/third-designer/17-situation-and-questions-2026-05-22.md`
against the current workspace and implemented the narrow helper breakage that
was safe to fix in this lane.

## Implementation landed locally

`tools/orchestrate status` was broken exactly as reported: the runtime
`orchestrate/roles.list` contained `second-operator`, `second-designer`, and
`third-designer`, while `orchestrate-cli` still carried a closed Rust `Lane`
enum from the earlier assistant-lane shape.

The local fix changes `orchestrate-cli` so `Lane` is a validated dynamic token,
not a closed enum. `LaneRegistry` now accepts both `assistant-of:<role>` and
`parallel-of:<role>` markers, preserving registry order for status rendering.
`orchestrate-cli/Cargo.lock` was refreshed to current
`signal-persona-orchestrate`, where `RoleName` is the dynamic
`RoleIdentifier`.

Verification:

```sh
cargo test --manifest-path orchestrate-cli/Cargo.toml
cargo build --manifest-path orchestrate-cli/Cargo.toml --release --bin orchestrate
tools/orchestrate status
```

`tools/orchestrate status` now renders the registry lanes including
`second-operator`, `second-designer`, and `third-designer`.

## Active blockers: current truth

### B1 — Spirit v0.1.1 cutover

Third-designer's branch blocker is stale. Current local evidence:

- `persona-spirit` has `main` and tag `v0.1.1` at `e137f5de` (package version
  bump).
- `signal-persona-spirit` has `main` and tag `v0.1.1` at `5f7d4f42` (package
  version bump).
- `sema-upgrade/Cargo.toml` depends on
  `signal-persona-spirit.git` with `branch = "main"`.
- `sema-upgrade/Cargo.lock` pins `signal-persona-spirit` to `5f7d4f42`.
- `CriomOS-home/flake.lock` has `persona-spirit-v0-1-0` and
  `persona-spirit-v0-1-1` inputs pinned by tags.
- Both `persona-spirit-daemon-v0.1.0.service` and
  `persona-spirit-daemon-v0.1.1.service` are active.

The real blocker is write drift after staging:

- `spirit` resolves to `spirit-v0.1.0`.
- `spirit-v0.1.1` exists and answers queries.
- Querying workspace records shows v0.1.0 contains recent records such as 147
  and 150, while v0.1.1 stops earlier for the same query. That means the staged
  v0.1.1 database is no longer current.

So the current cutover problem is not "merge branch before tag." It is:
re-stage/replay the v0.1.0 tail, then either dual-write during the migration
window or flip unsuffixed `spirit` to v0.1.1 and stop writing v0.1.0.

Existing beads already cover this:

- `primary-x3ci` (cut over Spirit daemon to v0.1.1) says to rerun migration or
  replay records after the high-water mark.
- `primary-chpq` (Spirit default wrapper dual-writes) says unsuffixed `spirit`
  must stop writing only v0.1.0 during the migration window.

### B2 — `tools/orchestrate` broken

Fixed locally by the dynamic-lane patch described above. The helper is still a
transitional lock-file writer, but it no longer breaks the moment
`orchestrate/roles.list` grows a valid dynamic lane.

Remaining design gap: this only fixes the helper. The durable destination is
still persona-orchestrate as the source of truth for lane registry, occupancy,
and activity.

### B3 — Engine-manager Axis 2

The substance is still open, but "not on a bead" is only partly true. The bead
`primary-k2mh` now has a 2026-05-21 comment naming the omitted gap:

- `src/supervisor.rs` still carries supervisor/supervision vocabulary.
- `src/supervision_readiness.rs` still names the engine-management probe actor
  as supervision readiness.
- `supervision_socket_*` identifiers and `.supervision.sock` filenames remain.
- `ARCHITECTURE.md` still has supervision prose where it means
  engine-management.

The code audit confirms the gap remains. Examples still present in
`/git/github.com/LiGoldragon/persona` include `supervision_socket_path`,
`supervision_socket_mode`, `ComponentSupervisionReadiness`,
`mind.supervision.sock`, `router.supervision.sock`, and architecture text
describing typed supervision frames.

This is an ABI/config break because the socket filenames and environment
names appear in scripts, tests, fixtures, Nix checks, and spawn envelopes. It
should land as one coordinated slice or remain explicitly deferred.

## Questions still needing psyche attention

### Q1 — sema-upgrade self-upgrade

Still open. I agree with third-designer's lean: use a hand-written
bottom-of-stack path until the inspect/plan/migrate protocol and schema DSL
are stable enough to dogfood.

### Q2 — Health/Readiness and ItemPriority on Magnitude

Partly answered by implementation: `ItemPriority` already collapsed to
`signal_sema::Magnitude` in `signal-persona-mind` and `persona-mind`, per the
`primary-k2mh` bead comment. Health/readiness collapse still needs an explicit
decision before touching the system/harness surfaces.

### Q3 — commit-sequence scope and migration 1

Still open. The Spirit v0.1.1 situation makes this concrete: without a
commit-sequence high-water mark, we only know there is drift by comparing
observed records. My recommendation remains per-database commit sequence, with
stop-old-start-new accepted for the first Spirit migration only if the final
staging run starts from the newest v0.1.0 database immediately before the
default flip.

### Q4 — Engine-manager Axis 2 timing

Still open. My recommendation: do not mix it into Spirit cutover. Keep it on
`primary-k2mh` as a persona-engine slice because it touches socket filenames,
spawn envelopes, tests, scripts, Nix checks, and architecture text.

### Q5 — cutover branch ratification

Mostly resolved by current state: the branch is no longer the concrete blocker
for the repos I checked. The lesson should still be retained as enforcement of
intent record 109: no long-lived branch by default; if a branch happens, merge
to `main` and tag the stable interface promptly.

### Q6 — multi-version verification

Still open. The deployed state strongly favors side-by-side
verify-then-flip: both daemons already run, and the versioned CLI wrappers
exist. The missing piece is making the v0.1.1 database current at flip time.

### Q7 — sema-upgrade RejectionReason fanout

Still open for daemon promotion. The five variants named by third-designer
are correct for implementation: source database missing, target database
exists, component identifier mismatch, version identifier mismatch, and
engine-internal error.

### Q8 — ItemPriority collapse

Already implemented for mind according to the bead comment:
`signal-persona-mind fc93f02c` and `persona-mind d08881b5` collapse
`ItemPriority` into `signal_sema::Magnitude`.

### Q9 — designer protocol coverage for parallel-main lanes

The current `skills/role-lanes.md` says `designer`, `second-designer`, and
`third-designer` are structural-authority windows on the same Designer agent.
However, intent record 57 still phrases the subagent-dispatch carve-out as
"prime designer" only. So structural design authority is resolved; automatic
parallel-subagent authority for `second-designer` / `third-designer` remains
ambiguous unless the psyche explicitly extends record 57.

### Q10 — push

Third-designer's push question belongs to that lane. I did not push their
commits. The primary working copy currently has many unrelated uncommitted
report and skill changes from other lanes; any push needs path-isolated commits.

## Extra issue surfaced

This session is operating as `cluster-operator`, but `cluster-operator` is not
registered in `orchestrate/roles.list`. Reports can exist under
`reports/cluster-operator/`, but source-code claims cannot be represented by
the helper under that lane yet. Because `orchestrate-cli` now supports dynamic
lanes, registering a new lane is mechanically easy; the unresolved part is the
main-role relation for `cluster-operator`.
