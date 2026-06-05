---
title: 539 — Audit of the operator's engine-trait Plane follow-up
role: designer
variant: Audit
date: 2026-06-05
topics: [audit, schema-rust-next, spirit, plane-type, engine-traits, short-header, signal-frame, verification]
description: |
  Adversarial four-dimension audit of operator report 325 (schema-rust-next
  3ebeeda + spirit 46daf37), closing audit 538's engine-trait follow-up.
  Verdict: functionally SOUND and independently verified (byte-identical,
  three-tier clean, the cross-plane gotcha handled, builds/tests reproduced),
  but a PARTIAL migration of the designer's verified scope, plus two real
  ARCHITECTURE.md doc defects and a tracked zero-byte residue.
---

# 539 — Audit of the engine-trait Plane follow-up

## Verdict: sound and verified, but partial

The operator (report 325) carried the engine-trait family onto `Plane`, gated
`short_header`, documented the three-tier rule, and regenerated Spirit.
Audited adversarially across four dimensions with independent build/test
re-runs. **The work is functionally correct and honestly verified** — but it
is a *partial* migration of the scope the designer branch proved, and it
introduced two `ARCHITECTURE.md` statements that the code contradicts.

## What checks out (clean)

- **Build/test reality.** Both repos at the exact claimed commits. Re-ran:
  `schema-rust-next` `cargo test` → 54 passed, `clippy -D` clean;
  `spirit` `cargo check --no-default-features` (forced real recompile),
  `cargo test --all-features` → 68 passed / 9 nix-ignored, `clippy -D` clean.
  No failure, no unreproducible claim. (Nix builds not re-run — flagged.)
- **The cross-plane gotcha is handled correctly.** Inside the engine-trait
  token bodies, cross-plane payload paths (`nexus::Nexus<nexus::Work>` inside
  the `SignalEngine` body, etc.) stay **literal** — only the trait *name*,
  trace enum, and trace-activation method are `Plane`-derived. No trait body
  wrongly derives a cross-plane payload from `self.plane`. This was the main
  correctness risk; he got it right.
- **Three-tier purity.** `impl Plane` is the sole block; the three new methods
  are pure `&self` constants — grep for `emits_`/`RustEmissionTarget`/
  `declarations`/`root_enums`/`nexus_runner_shape` inside it returns zero. The
  `SignalRuntime` concreteness special-case stays on `RustWriter`/the target.
- **Byte-identical output.** Commit `3ebeeda` touches only `ARCHITECTURE.md`,
  `src/lib.rs`, and `tests/emission.rs (+2)` — **zero** golden fixtures. The
  parametrized tokens render to the same bytes (engine-trait emission test
  passes).
- **538 finding #2 properly closed.** Rather than just dropping the orphaned
  `short_header`, he added `RustWriter::emits_short_headers()` =
  `matches!(target, WireContract) || emits_signal()`, gating it at the source;
  Spirit regen removed the dead `pub mod short_header` from `nexus.rs` (−12)
  and `sema.rs` (−7), `signal.rs` unchanged, **no dangling references**
  (consumers in `subscription.rs`/`engine.rs` bind only to the signal plane).

## Findings

1. **(Central — completeness) Partial migration.** He migrated the three
   *engine-trait* nouns (`SignalEngineTraitTokens`/`NexusEngineTraitTokens`/
   `SemaEngineTraitTokens`) to consult `Plane`, **but not** the trace
   object-name path that the designer branch (`77affc0b`) also migrated:
   - `TraceObjectNameEnumTokens` still carries caller-supplied
     `enum_name`/`rendered_prefix` *string* fields (lib.rs:2149-2173); call
     sites hardcode `("SignalObjectName","Signal")` etc. (lib.rs:3517-3537).
   - `TraceSupportTokens` (the cross-plane dispatcher) still emits the six
     plane references as raw literal tokens (lib.rs:2254-2307).
   The designer branch routes both through `Plane` (`trace_prefix` +
   `object_name_variant(plane)`). **Different decomposition, not strictly
   lesser:** he added `trace_activation_method_name` — a net-new migration the
   designer branch did *not* do (it hardcoded `trace_signal_activation`). So
   each carried a slice the other didn't. **Functionally correct** — the
   hardcoded literals equal what `Plane` would produce, output is unchanged —
   the gap is DRY / single-source-of-truth, not behavior.

2. **(Real doc defect) `ARCHITECTURE.md` falsely says `WireContract` emits
   signal-frame.** ARCHITECTURE.md:112-114 states `WireContract` emits "…short
   headers, **and signal-frame encode/decode**." The "and signal-frame
   encode/decode" clause is **false**: `emits_signal()` is `false` for
   `WireContract`, so it emits no `encode_signal_frame`/`decode_signal_frame`,
   and `tests/emission.rs` *explicitly asserts their absence*. The doc
   contradicts the code and the tests.

3. **(Doc overclaim) `ARCHITECTURE.md` says "Plane owns … trace enum names"**
   (lines 39-44) — but per finding #1, `TraceObjectNameEnumTokens` and the
   dispatcher still hardcode those trace enum names. The doc claims more
   single-sourcing than the code delivers.

4. **(Minor) `WireContract` `short_header` is orphaned-but-deliberate.** The
   gate keeps `short_header` for `WireContract`, but a dumped wire emission
   shows it has **zero** consumers there (wire has no signal-frame after
   `gb95` either). So `short_header` is dead in wire just as it was in
   nexus/sema — kept by the explicit `matches!(…, WireContract)` arm. Either
   it's intended as part of the external wire vocabulary, or it's the same
   orphan one plane over; worth an explicit decision.

5. **(Hygiene risk) The zero-byte `spirit/src/main.rs` is *tracked*, not
   "untracked".** Report 325 calls it untracked; `jj status` shows `A
   src/main.rs` (a tracked add in the shared jj working copy, 0 bytes, not in
   `HEAD`). Build-harmless, but under the **whole-working-copy commit**
   discipline the *next* `jj commit` by any lane will sweep this empty file
   into history. It should be removed before then, not left.

6. **(My audit hygiene — noted, resolved)** A scratch diagnostic test from a
   *prior* designer-audit agent was found uncommitted in the `schema-rust-next`
   working tree; this audit restored the file byte-identical to `HEAD` and the
   tree is now clean. Lesson for my side: audit agents that dump emission into
   the live operator repos must clean up (or run in a worktree).

## Recommendations

- **To genuinely make ARCHITECTURE.md true, finish the trace path:** give
  `TraceObjectNameEnumTokens` a `plane: Plane` field (drop the two string
  fields) and route the cross-plane `TraceSupportTokens` dispatcher through
  `Plane` — the designer branch `77affc0b` has the verified version
  (`trace_prefix` + `object_name_variant`). Small, byte-identical change.
- **Fix the two doc defects:** delete the `WireContract` "signal-frame
  encode/decode" clause (it's false); and either complete the trace migration
  or soften the "Plane owns trace enum names" claim.
- **Remove the tracked zero-byte `spirit/src/main.rs`** before the next commit.
- Decide explicitly whether `WireContract` `short_header` is wire vocabulary
  (keep) or an orphan (gate it out too).

The three production blockers from 324/325 (no `meta-signal-spirit`
contract/listener; no Nix subscription-streaming witness; no `persona-spirit`
cutover) remain the right next targets.

Per psyche 2026-06-05 ("run your audit").
