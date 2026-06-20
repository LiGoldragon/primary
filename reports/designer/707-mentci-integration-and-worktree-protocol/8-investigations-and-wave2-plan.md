# 707-8 — Investigations resolved; wave-2 plan

Three forensic investigations (sub-reports 5-7) grounded the three pending
decisions. All resolved with evidence; one wave-1 framing corrected.

## Grounded decisions

1. **mentci-lib → RE-FOUND on the live contracts** (sub-report 5). mentci-lib is
   the *original* Mentci design (`2026-04-29`), predating the daemon +
   signal-mentci (`2026-06-18`) by ~50 days — overtaken, not abandoned. Its
   transport (signal-crate Handshake) has no live responder (the daemon speaks
   signal-frame `StreamingFrame`); it redefines the approval vocabulary that
   signal-mentci already owns; its sole consumer (egui) left it (`293a228`); the
   dual-daemon `nexus` it targets was never built. Keep the MVU shape,
   edits-as-proposals model, and approval state machine; discard the signal-crate
   transport, graph model, nexus connection, and duplicate types.
2. **Registry → BUILD IN THE `/git/orchestrate` TRIAD** (sub-report 6). Corrects
   wave-1's "tools/orchestrate IS the component." Reality: two artifacts, one
   architecture, no duplication. The workspace switched to the dedicated triad;
   primary `orchestrate-cli` is a thin *client* (no redb, no `tables.rs`) that
   spawns + talks to `orchestrate-daemon` (PID 653243), which owns the redb store
   and *projects* the `.lock` files (legacy bash locks imported once; store is now
   the source of truth). The daemon already owns a `StoredRepository` registry
   (scans `/git`); it has **no worktree concept** — so `eh5a` is a natural
   extension: `StoredWorktree` beside `StoredRepository`, a `worktrees` table
   (schema-version bump), a `WorktreeRegistry` scanner of `~/wt`, Register/Refresh
   in meta-signal-orchestrate, `Observe(Worktrees)` in signal-orchestrate, and a
   thin `orchestrate worktree …` argv adapter in orchestrate-cli. The GC manifest
   is the daemon's `worktrees.nota` projection (one artifact, as B+C agreed).
3. **schema-rust-next** (sub-report 7): `reaction-expand` (`8b147fac` +
   `a1582dfd`, ~4d old) is **unique-at-risk** — a parked competing design
   (`CapabilityResolver` route; main chose impl-catalog) whose consumer side is
   local-only; its schema-next half is already pushed (`next/schema-capability-
   resolution`). **Preserve** by pushing the consumer to a matching `next/`
   bookmark; route the catalog-vs-resolver design choice to the schema-toolchain
   owner (nota-designer / system-designer); the `Cargo.toml` `[patch]` local-path
   pin needs repointing to the pushed branch before it builds elsewhere.
   `structural-forms-integration` is **safe to archive** — superseded on main
   (the must-not-lose flag was a false positive from the twin divergence).

## Wave 2 (executing in parallel)

- **Registry build** — the `/git/orchestrate` triad + orchestrate-cli adapter, on
  designer branches; seeds from the wave-1 audit; generates `worktrees.nota`.
  Prototype-on-branch (operator/system integrates); do not disturb the live tool.
- **mentci re-found** — rebuild mentci-lib on signal-mentci + signal-frame off
  operator's latest (operator just landed typed endpoint config:
  meta-signal-mentci `42222f30`, mentci `f5e17af0`, mentci-egui `075cbff4`), keep
  the proposal/approval MVU, make daemon + egui consume it; then the CLI
  read+answer roster and the criome+mentci `runNixOSTest` on Prometheus (recycle
  `criome-nixos-module-142`).
- **Worktree upkeep** — preserve `reaction-expand` (surface to owner with the push
  command), mark `structural-forms-integration` + the merged/archive set for the
  gated GC pass (which the registry's manifest will drive); remove the empty
  `nota-next/` + `upgrade/` parent dirs in that pass.
