# 141 — Landed: router fan-out surface (G) + scoped attested-moment majority guard (H)

*Results of build workflow `wgpa80oej` (the 139 build). H is merge-clean. G's
substance is sound and faithful; one precise merge-blocker is being closed now.
Both on feature branches for operator. The build also surfaced a real integration
hazard that confirms the designer's Woe-4 as the critical path.*

## Track H — `:578` attested-moment majority guard: SOUND, merge

Branch `attested-moment-majority-guard-139` on `criome`, commit `ed2f3b5d`,
pushed. Reviewer verdict **sound, no defects**, build reproduced.

- The guard `|| required <= (authorities.len() as u16) / 2` is added **only** to
  `AttestedMoment::rejection_reason` (`language.rs:592`); `Threshold::validate_shape`
  (`:407-429`) is verified **unchanged** — the general m-of-n evaluator is not
  regressed. This is exactly the two-sites reconciliation from 139.
- Six boundary tests assert exactly: `n=1/r=1` accepted (the `9s52` single-machine
  self-quorum), `n=2/r=1` rejected, `n=2/r=2` accepted, `n=3/r=2` accepted,
  `n=4/r=2` rejected, `n=4/r=3` accepted. Mutation-check: removing the clause fails
  precisely at `n=2/r=1` and nowhere else.
- The code comment documents the fork-safety rationale (`ay3y`/`m0p2`) **and** that
  `:414` deliberately stays caller-declared and must not get the guard — so a
  future reader can't re-introduce the regression.

## Track G — router `Attend`/`Withdraw` fan-out: substance SOUND, one fix in flight

Branches `attendance-fanout-139` across `signal-standard`, `signal-router`, and
`router` (commits `signal-standard 8befd44e`, `signal-router 1a9b02e9`, `router
23312d96`), all pushed; no code-repo main moved.

All five design checks **pass**, reviewer-verified (incl. a matcher mutation):

- **Router-sole & light:** the attendance table is a router-local SEMA family
  (`attendance` / `router-attendance`) on the existing `RouterStore`; `criome` and
  `signal-criome` are **untouched** — no governed criome contract for attendance.
  Faithful to `m0p2`.
- **Reference, not payload:** `ObjectAvailable` carries only the
  `AuthorizedObjectReference` (component + digest + kind); the push encodes that
  reference over the existing `ComponentSocket` delivery, never the body.
- **Match is real (mutation-verified):** matching `(component, kind)` against a
  registered `AuthorizedObjectInterest` pushes to the attender; a non-match pushes
  to no one; `Withdraw` stops further pushes; the table survives restart (SEMA
  replay). The 4-rung `matches_reference` predicate was lifted into
  `signal-standard` (the type's home) so router and criome share one definition —
  closing the report-135 drift risk.
- **Imports from `signal-standard`** (not re-declared, not from `signal-criome`),
  wired via `GenerationPlan::wire_contract().with_dependency_schema(...)` (the
  proven meta-signal-message pattern); the schema freshness gate passes.
- **NOTA/Rust discipline:** positional records, `Withdraw` (not the SEMA word
  `Retract`), no quotes; methods on data-bearing types, schema-derived decode.

The one merge-blocker (P2, being fixed): on the non-compat `signal-router` branch
the new attendance tests in `tests/round_trip.rs` weren't feature-gated, so
`cargo clippy --all-targets` fails under **default** features (the "clippy clean"
claim was produced only with `--features nota-text`). The fix (gate them behind
`#[cfg(feature = "nota-text")]`, matching the compat branch) + an optional
strengthening of the `withdraw` test is in flight (agent `ad6e5b1a`). After it,
the reviewer's own words: "ready to integrate."

The match-and-push step is complete, durable, and tested via a `FanOutAdmittedObject`
runtime entry point; the **criome-event-stream client** that drives it per admitted
object is the documented milestone-3 seam in `daemon.rs` (it needs the criome
client, gated on the same work as the attestation path).

## The integration hazard the build surfaced (confirms Woe-4 is the critical path)

The build could not consume `signal-router/main` directly from `router`:
`router/main` (`430f1de5`) has **not** integrated `signal-router/main`'s
field-label removal (`3e4bb074`), and building `router/main` against current
`signal-router/main` throws **69 errors** (in `router.rs`,
`forward_attestation.rs`, `observation.rs`, `peer_delivery.rs`, `config.rs`) — the
retired dot-field/label syntax. This **is** the designer's Woe-4 (the
positional/field-label migration) biting at the router↔signal-router boundary.

To keep Track G self-contained and green, the build introduced a
`signal-router/attendance-fanout-139-compat` branch (the older `e36e773` that
`router/main` pins, plus *only* the additive Attend/Withdraw surface); `router`
depends on that. The canonical additions live on `attendance-fanout-139` (based on
`signal-router/main`).

**Operator integration sequence:** (i) port `router/main` onto the current
`signal-router` contract (the field-label migration); (ii) rebase the router
attendance commit onto that; (iii) flip the `router` `Cargo.toml` `signal-router`
dep from `attendance-fanout-139-compat` to `main` and `signal-standard` to `main`;
(iv) delete the compat branch. Also: once `signal-standard` lands on main, point
`criome`'s `AuthorizedObjectInterest::matches_update` at the lifted
`matches_reference` to retire the drift risk for good.

## State of the branch fleet (all for operator to merge)

| Branch | Repo(s) | What | Status |
|---|---|---|---|
| `transport-p1-fixes-138` | router | P1 fixes + verifier fence | sound |
| `transport-two-kernel-e2e-138` | router | L1 nixosTest + `message-router.nix` | sound (KVM-green) |
| `signal-standard-bootstrap` | signal-standard | shared vocabulary crate | sound (now has local `main`) |
| `attended-moment-majority-guard-139` | criome | `:578` majority guard | **sound, merge** |
| `attendance-fanout-139` (+`-compat`) | signal-standard/router/signal-router | Attend/Withdraw fan-out | sound; gating fix in flight |
| `cluster-root-admission-ceremony` | criome | offline admission minting | sound (earlier) |
