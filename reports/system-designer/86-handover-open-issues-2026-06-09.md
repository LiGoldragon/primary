---
title: 86 — handover — open issues not addressed this session
role: system-designer
variant: Handover
date: 2026-06-09
topics: [handover, open-issues, nota-free, schema-emission, two-contract, migration-debt, criome, schema-rust-next]
description: |
  Running list of everything left open after the 2026-06-09 workspace survey +
  cleanup + criome NOTA-free / schema-emission arc (reports 82–85). Organised by
  area with priority. Includes a correction: criome's CONTRACT is now schema-
  emitted, but criome's DAEMON is still hand-written — it remains the last
  concept-stage component daemon.
---

# 86 — handover: open issues

Priority key: **P1** load-bearing / blocks the stated direction · **P2** real
debt, schedule it · **P3** minor / cosmetic.

## A. NOTA-free + schema-emission migration (the main arc)

1. **(P1) criome's DAEMON is still hand-written — not `triad_main`-emitted.**
   This session converted the *contract* `signal-criome` to schema emission and
   made criome's hand-written code NOTA-free. But `criome/` itself has no
   `build.rs` / `src/schema/` — its daemon spine is hand-written. criome is
   therefore still the **last concept-stage component daemon** (15/16 component
   daemons are emitted). *Correction to in-flight wording:* "16/16 components
   emitted" referred to the contract; the criome daemon still needs the
   `triad_main` daemon-emission conversion the other 15 had.

2. **(P1) Five hand-written contracts still need schema emission:**
   `signal-system`, `signal-introspect`, `signal-spirit`, `signal-mind`,
   `signal-harness`. Each is the same conversion `signal-criome` just went
   through (author `schema/lib.schema`, wire `build.rs`, drop hand-written
   `lib.rs`, migrate consumers to the normalized emitted API). `signal-cloud`
   is already emitted.

3. **(P1) Four of the five meta-signal contracts created this session carry the
   deprecated unconditional-NOTA pattern.** `meta-signal-{harness,system,message,
   introspect}` have `default = ["nota-text"]` and ungated derives (0 `cfg_attr`
   gates). Only `meta-signal-criome` is NOTA-free-by-default. They cannot be made
   NOTA-free until their ordinary contracts (#2) migrate. The broader
   `meta-signal-*` family (incl. the `meta-signal-mind` exemplar that was copied)
   is unmigrated too.

4. **(P1) Contract `default`-feature knob is inconsistent.** Even emitted
   contracts (`signal-message`, `signal-cloud`) still set `default = ["nota-text"]`,
   so a daemon depending on them with default features pulls NOTA anyway. The
   fleet needs one rule — contracts default `[]`, or components depend with
   `default-features = false` (criome does the latter). Until then, "daemons
   compile no NOTA" is **not** guaranteed fleet-wide.

5. **(P2) Only criome-daemon was verified NOTA-free.** The other 15 component
   daemons are emitted (so their codecs are gated) but their linked NOTA-freeness
   is unverified given #4. Worth a fleet `cargo tree -e normal -i nota-next` sweep.

## B. Migration debt (pre-existing)

6. **(P2) `orchestrate` → `triad_main` cutover unfinished.** It has *both* a
   hand-written `src/daemon.rs` and an emitted `src/schema/daemon.rs`; retire the
   hand-written one and prune legacy deps (`signal-version-handover`). (Bead
   `ocu7`.)

7. **(P3) `sema` → `sema-engine` is effectively done** — only `persona-spirit`
   (production Stack A, expected) and `sema-engine` itself (by design) still
   depend on `sema`. No action unless retiring `sema`.

## C. Contract / naming / docs hygiene

8. **(P2) `signal-sema` is misnamed** (it's the cross-component SEMA-operation
   observer vocabulary, not a daemon contract — there is no `sema` daemon).
   Rename candidate; also decide whether the observer layer is wired end-to-end
   or is half-built coupling (report 83 flag).

9. **(P2) INTENT.md coverage gap.** Many keeper repos (contracts, CriomeOS
   satellites, creative/web repos) still lack the per-repo `INTENT.md` the
   repo-intent discipline requires. Archiving the dead reduced the surface; the
   keepers still need them.

## D. The five meta-signal contracts — runtime wiring

10. **(P2) The 5 meta contracts exist but no daemon binds a meta socket against
    them.** `message`, `harness`, `system`, `introspect`, `criome` each have
    `signal-` + `meta-signal-` now, but the components don't yet serve the meta
    `Configure` channel at runtime. The "missing-meta" gap moved from
    "contract absent" to "contract present, runtime unwired."

## E. criome residuals (report 84 + this session)

11. **(P1) criome daemon emission** — same as #1.

12. **(P3) `RequiredSignatureThreshold` widened u16 → u64.** The schema emitter
    has no `u16`; the emitted newtype is `Integer` (u64) with a hand-added
    `into_u16()` cast. If the 16-bit bound is semantically meaningful, that's a
    latent narrowing gap to revisit.

13. **(P3) criome test `.to_string()` wraps are now redundant** — the emitter
    now takes `impl Into<String>` (#H/17). They still compile; clean on the next
    criome test pass / regen.

14. **(P3) Test `criome_daemon_meta_socket_is_user_private` is misnamed**
    (report 84) — criome binds one ordinary socket; there is no meta socket.
    Rename or wire the meta plane.

15. **(P3) Verb-mismatch rejection guard dropped** (report 84 finding 2) —
    almost certainly structural (signal-frame removed verbs from the frame
    model) but never formally confirmed.

16. **(P3) Pre-existing rust-discipline nits in criome** — e.g.
    `criome/src/actors/mod.rs::rejection` is a free function (no-free-functions
    rule). Not introduced this session; flag for the operator's cleanup.

## F. Persona contract cleanup (carried from prior context, Spirit `n0ss`)

17. **(P2) Confirm the persona-contract cleanup is complete.**
    `meta-signal-persona` exists and `owner-signal-persona` is archived, but the
    `signal-engine-management` fold-into-`signal-persona` step was never verified
    this session. Confirm no off-pattern `signal-engine-management` / owner-signal
    references remain.

## G. schema-rust-next (emitter) follow-ups

18. **(P2) Emit `Copy` for integer-backed newtypes.** This session had to
    hand-add `impl Copy for TimestampNanos {}` / `RequiredSignatureThreshold` in
    `signal-criome` because the emitter derives only `Clone`, which broke
    move-semantics in consumers. The emitter should derive `Copy` for
    integer/scalar newtypes — same one-place, fleet-wide fix as the
    `new(impl Into<String>)` change landed this session.

## Done this session (for context — not open)

Survey + lean-set cleanup (40 repos archived → `~/git-archive`, indexes
regenerated); 5 `meta-signal-*` contracts created; criome triad migrated to
NOTA-free; criome *contract* converted to schema emission (daemon binary verified
NOTA-free, tests green); `schema-rust-next` emits `new(impl Into<String>)` for
string newtypes. Detail in reports 82–85 and Spirit records `bds6`, `op4b`,
`hnpo`, `n0ss`, `t803`, `q3q7`, `5fdr`, `t4gd`.
