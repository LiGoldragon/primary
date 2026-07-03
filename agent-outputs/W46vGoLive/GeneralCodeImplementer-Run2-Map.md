# w46v bounded completion push (run 2) — terminal: RED, complete blocker map

Session W46vGoLive. Tool at synchronizer `main 8eec5a46` (coordinator's
transitive-fallback fix). Report: `SyncNotaReport2.nota`.

## Applied

- **B — persona flake inputs normalized to github: form.** persona/flake.nix
  `persona-router` and `persona-message` changed from
  `git+ssh://git@github.com/LiGoldragon/<repo>.git?ref=main` to
  `github:LiGoldragon/<repo>`; flake.lock re-locked (github-type nodes, same
  revs). LANDED to persona main `ac629103`.
- **C — router + message added to `goldragon/synchronizer.nota`** (now 7
  components; validate → "ok: 7 components configured"). Committed+pushed to
  goldragon main `e8b658fa`. Note in-file revised.

B is PROVEN effective by the report: persona's `router` FlakeLock repointed
`14f8557 → 2f2e2224` (router synchronizer tip), `message` FlakeLock → `2ebd32f0`,
`introspect` FlakeLock → `087d0cf9`. The tool now discovers and cascades the
persona→router / persona→message flake edges. The git+ssh builder-fetch blocker
from run 1 is GONE.

## Re-run NOTA summary

| repo | bumped to signal-frame 0.3.0 + producer synctips | staging tip | verify |
|---|---|---|---|
| signal-frame | leaf, AlreadyAligned | — | NotAttempted |
| message | signal-frame→0027ea3c | 2ebd32f0 | **GREEN (WireChecks)** |
| signal-harness | signal-frame→0027ea3c | 746b5347 | **GREEN (DefaultPackage)** |
| signal-router | signal-frame→0027ea3c | df94b8bf | **GREEN (DefaultPackage)** |
| router | signal-frame→0027ea3c, signal-harness→746b5347, signal-router→df94b8bf | 2f2e2224 | **GREEN (WireChecks)** |
| introspect | signal-router main→sync, signal-frame, signal-router→df94b8bf | 087d0cf9 | **FAILED** |
| persona | message/harness/router main→sync, signal-frame→0.3.0, message→2ebd32f0, harness→746b5347, router→df94b8bf(flake), introspect→087d0cf9(flake) | ac07cdcb | **FAILED** |

Key positive: **router verified GREEN with WireChecks at signal-frame 0.3.0** —
the router-daemon builds and its wire checks pass on the bumped contracts. The
signal-frame `Caller.identity` skew concern is resolved for the launched daemon
once persona is unblocked. All mains verified UNTOUCHED (persona ac629103 = B;
signal-router 30be9b0f, signal-harness 52cd2ed, message d7dfb005, router
14f8557, introspect 7b53b37e, signal-frame 0027ea3c). Staging branches left
unmerged.

## Gate result: RED

The persona whole-engine gate (all persona-daemon-launches-nix-built-*-topology,
persona-router-daemon-*, wire-* checks — enumerated in the report) VerifyFailed —
but no longer at fetch and not on a wire skew. It fails because persona's own
Cargo.lock is invalid: `cargo check --locked` errors on `message@2ebd32f0`'s
`schema-rust` dep because persona's lock was left broken by the nota-next
transitive-lock failure. introspect fails identically on `signal-router@df94b8bf`.

## Complete remaining-blocker map (current state → GREEN gate)

GREEN already, on prometheus at signal-frame 0.3.0: signal-frame, signal-router,
signal-harness, message, **router**. B+C effective. **The entire remaining
surface is ONE issue in TWO repos:**

### nota-next → nota crate-rename staleness — introspect and persona

- **What:** nota-next.git renamed its crate `nota-next` → `nota` at `96e64bc`
  (ancestor of main; nota-next.git@main crate = `nota`, v0.6+). introspect
  (Cargo.toml:30) and persona (Cargo.toml:32) still declare
  `nota-next = { git = ".../nota-next.git", branch = "main" }` → dependency on a
  package literally named `nota-next`, and their locks pin a pre-rename rev
  (`f94b5462`, crate nota-next v0.5.1). Every other consumer (signal-*, message,
  router) already declares `nota = { package = "nota", ... }`.
- **Why it blocks:** bumping introspect/persona to signal-router `df94b8bf`
  (which pulls package `nota` from nota-next.git@main) forces nota-next.git@main
  to a post-rename rev (crate `nota`), which cannot also satisfy their own
  `nota-next` package dep at the same branch=main resolution →
  `no matching package named nota-next` → invalid lock → verify fails.
- **Classification: MECHANICAL (manifest + lock; NO source edits).**
  Fix per repo: `nota-next = { package = "nota", git = ".../nota-next.git", branch = "main" }`.
  Keeping the dependency KEY `nota-next` means the extern crate name stays
  `nota_next`, so all `use nota_next::` references compile unchanged.
- **Source-reference scope (coordinator's question):** `use nota_next::` refs DO
  exist — introspect: surface.rs, error.rs, meta.rs, command.rs; persona:
  error.rs, engine_event.rs, request.rs, engine.rs, launch/command.rs,
  schema/reports.rs, bin/persona_write_configuration.rs (9+). They do NOT need
  editing: the `package = "nota"` rename preserves the `nota_next` extern name.
  So the migration is manifest-key-attribute + lock, not source.
- **One operational caveat:** the landed introspect/persona main must be
  self-consistent (manifest+lock), so the nota-next lock entry must be
  regenerated to a `nota` entry at nota-next main. The tool's transitive
  fallback (now fixed) should produce this during the signal-router bump once the
  manifest agrees, but the lock regen should be checked to not cascade other
  branch=main deps.

### Residual unknown (not a found blocker, flagged)

persona's whole-engine topology checks have never actually BUILT+RUN (run 1 died
at git+ssh fetch; run 2 at the broken lock). So a latent persona-source
incompatibility with signal-frame 0.3.0 is unproven — but router (a comparable
signal-frame/router/harness consumer) passed its WireChecks at 0.3.0, so
confidence is high that persona builds once the nota-next lock is fixed.

## Disposition

STOP (gate not green): landed to NO component main; six `synchronizer` staging
branches left unmerged (message 2ebd32f0, signal-harness 746b5347, signal-router
df94b8bf, router 2f2e2224, introspect 087d0cf9, persona ac07cdcb). primary-w46v
left OPEN. B (persona main) and C (goldragon main) are independently-correct and
kept.
