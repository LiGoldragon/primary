# 44 · Lojix durable state (S3) — grounding frame

## Goal

Per Spirit `oh9l` (durable-first): replace lojix's in-memory `StoreState`
(`Mutex<StoreState>`, no persistence, no crash-resume) with durable
sema-engine backing and **self-resume on restart**, *before* the activation
work (S4) commits live-set / GC-root / event-log mutations against it. The
recon (report 41) flagged this as one of the two stages with real
engineering.

## Why ground first

The durable-state architecture must be pinned to the actual code and the
shipped precedent, not assumed:

- Does `triad-runtime`'s `NextStep::SemaRead/SemaWrite` already route through
  a durable store, or does the daemon supply it?
- sema-engine library vs direct redb — Spirit `fosp` says sema-engine, the
  synthesis says "no direct redb calls"; confirm against how a shipped daemon
  (spirit) actually persists SEMA state.
- The self-resume-on-restart flow and the backup discipline (`oh9l`, `fosp`,
  `29pb`).

Getting this wrong means rebuilding the foundation, so this meta-report maps
it (read-only) and produces a concrete implementation plan I execute from.

## Method

Read-only reconnaissance fan-out, each dimension writing its numbered file,
then a synthesis implementation plan. No mutation.

Dimensions:

1. lojix's current SEMA flow — the `SemaEngine` impl, the runner loop, the
   `StoreState` read/write seam where durable backing plugs in
2. triad-runtime's SEMA layer — `NextStep::SemaRead/SemaWrite`, the Sema
   traits, what the daemon must supply
3. durable precedent — how spirit (and mind) persist SEMA state durably +
   self-resume
4. the sema-engine library API — open, register tables, typed read/write,
   resume from the persisted log
5. self-resume + backups — the restart-resume flow and backup discipline
6. synthesis — the concrete S3 implementation plan
