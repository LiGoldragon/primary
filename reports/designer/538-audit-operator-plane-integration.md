---
title: 538 — Audit of the operator's Plane integration + Spirit regeneration
role: designer
variant: Audit
date: 2026-06-05
topics: [audit, schema-rust-next, spirit, plane-type, signal-frame, operator-integration, verification]
description: |
  Adversarial four-dimension audit of operator report 324 (schema-rust-next
  7f59b395 + spirit 41d96e70). Verdict: SOUND. Every reproducible claim was
  independently reproduced; the signal-frame gating effect on generated output
  is correct with no over-removal; three-tier design and rust-discipline are
  preserved; the report is honestly hedged. Four minor findings, one a
  mitigated completeness concern (the engine-trait family was not carried and
  its deferral is unstated).
---

# 538 — Audit of the operator's Plane integration

## Verdict: SOUND

The operator (report 324) integrated the designer's **namespaces** Plane
family onto `schema-rust-next` main (`7f59b395`) and regenerated Spirit
(`41d96e70`) against the gated emitter. Audited adversarially across four
dimensions by independent agents that re-ran the build/test claims and
verified the diffs against source. **No fabrication; every reproducible claim
reproduced; the gating is correct; discipline holds.** Four minor findings
below; none blocking.

## What was verified

**Build/test reality (PASS, clean).** Both repos confirmed at the exact
claimed commits with clean trees. Re-ran independently:
- `schema-rust-next`: `cargo test` → 54 passed / 0 failed; `cargo clippy
  --all-targets --all-features -D warnings` → clean.
- `spirit`: `cargo check --no-default-features` (forced a real rebuild by
  clearing the fingerprint — genuinely compiles) → clean; `cargo test`
  (`generated_signal_plane` 10, `runtime_triad` 25, `daemon_command` 3) → all
  pass; `clippy --all-features -D warnings` → clean.
- The diff-anchored claims check out: `git show 41d96e7` shows `nexus.rs` −159
  / `sema.rs` −139 (exactly as reported), `signal.rs` untouched (retains 66
  signal-frame references).
- *Not* independently re-run (operator's claim stands, neither confirmed nor
  refuted): the Nix builds, `check-local-schema-stack`, and the 9-test
  `run-nix-integration-tests`.

**Integration fidelity (PASS).** Three-tier design (537/h3cy) preserved — the
`impl Plane` block owns only plane-intrinsic naming (grep-verified zero
`emits_`/`runtime_planes`/`RustEmissionTarget`/`declarations`/`root_enums`);
target-set logic stays on `RuntimePlaneSet`/`RustEmissionTarget`. Namespace
output **byte-identical** on his base (no golden fixture changed; 32 emission
tests pass). The `gb95` gate is byte-identical to the designer branch. The
operator's `PlaneWrapperPath` **"tightening" is a genuine improvement** —
it renders `nexus::Nexus`/`sema::Sema` as tokens directly (`quote!{ #module::#wrapper }`)
instead of the designer's `format!`-string-then-`syn::parse_str`-reparse, and
was proven output-equivalent (the path token streams are identical; the names
aren't keywords so no raw-ident divergence). It is a real data-bearing noun,
not a ZST.

**Spirit output/regeneration (PASS).** `signal.rs` still owns signal-frame
(`SignalFrameError`, `InputRoute`, `encode/decode_signal_frame`); `nexus.rs`
and `sema.rs` no longer do. The removed blocks are **genuinely signal-frame
transport and nothing more** — each block ends immediately before the
retained `NexusWorkRoute`/`WriteInputRoute` plane enums (no over-removal). The
only non-generated consumer, `src/transport.rs`, imports frame types
*exclusively* from `crate::schema::signal` — no dangling reference to a gutted
nexus/sema symbol exists. `cargo check/test/clippy --all-features` clean after
force-touching the regenerated files.

## Findings (all minor)

1. **(Completeness — the one real concern) The engine-trait family was not
   carried, and its deferral is unstated.** The designer branch (`77affc0b`)
   migrated **two** families; the operator integrated only the first
   (namespaces). On his main `fn engine_trait_name`/`trace_enum_name`/
   `trace_prefix` = 0 and `SignalEngineTraitTokens` still hardcodes plane
   names. Report 324 says "namespace family" but never notes the verified
   engine-trait family exists and is deferred. **Mitigated to minor:** it is a
   clean no-output-regression debt — the engine-trait emission still works
   (its tests pass; generated Spirit traits are correct), it just hasn't
   adopted `Plane` yet. No functional gap, only an unstated one.
2. **(Output hygiene) Orphaned `short_header` constants.** The `pub mod
   short_header { pub const … }` block remains in `nexus.rs`/`sema.rs` but is
   now referenced 0 times there (the removed frame methods were its only
   consumers; `signal.rs` still uses it). Dead-but-`pub`, so it survives
   `clippy -D warnings` — harmless, but it should be gated out of nexus/sema
   generation or explicitly retained.
3. **(Report accuracy) Feature/test-target conflation in 324.** Report 324
   lists spirit verification "across features `dependency_surface`,
   `generated_signal_plane`, `runtime_triad`, `daemon_command`,
   `process_boundary`, `--all-features`." Spirit's actual `[features]` are only
   `default`/`nota-text`/`testing-trace`; those names are `[[test]]` *targets*,
   not features. The tests exist and pass — this is a wording slip, not a false
   claim.
4. **(Discipline) Dropped doc-comments.** Integration dropped much of the
   designer's explanatory commentary (`///` count 66 vs 123 on the branch).
   Most of the delta is the deferred engine-traits family, but it also dropped
   the 7-line **three-tier rationale** on the `Plane` enum — load-bearing
   context for why target-set logic must stay off `Plane`. Worth restoring so
   the next family-migrator doesn't relearn it.

## Recommendations

- **Carry the engine-trait family to main.** It is verified byte-identical on
  `designer-plane-type-2026-06-05` (77affc0b); the change is small (grow
  `Plane` with `engine_trait_name`/`trace_enum_name`/`trace_prefix`, make the
  existing engine-trait nouns consult it). Either operator picks it up or I can.
- Drop or explicitly retain the orphaned `short_header` block in nexus/sema.
- Fix the 324 verification wording (test targets ≠ features); restore the
  `Plane` three-tier doc rationale.
- The stated production gaps (no `meta-signal-spirit` contract/listener path,
  no Nix subscription-streaming witness, no `persona-spirit` cutover) are
  **accurate and complete** — they are the right next production-readiness
  blockers.

Per psyche 2026-06-05 ("audit the operator's work").
