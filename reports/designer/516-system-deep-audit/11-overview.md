---
title: 516 — Overview — synthesis of the system deep audit
role: designer
variant: Psyche
date: 2026-06-04
session: meta-report directory (sub-agent session) — orchestrator synthesis
topics: [audit, schema, nota, engine, wire-contract, runtime-triad, intent, design-constraints, code-bulk, bad-patterns, verification]
description: |
  Synthesis of the 516 deep audit: the verification ledger (5 reports
  real, 1 partial then corrected), the most important design constraints
  isolated system-wide toward repo INTENT.md, the code-bulk / repetition
  / bad-pattern catalogue, and the INTENT.md state-of-the-union (core
  present-but-over-captured; 64 wider repos missing). All report-only.
---

# 516 — Overview — synthesis of the system deep audit

This is the synthesis of a ten-report meta-session that ran real code
across the schema-derived stack. Everything below is grounded in
commands the sub-agents actually executed; each mechanism report carries
an independent verification verdict. Read this first; the numbered
reports are the evidence.

## Verification ledger — was it real?

The "no guesswork" rule was enforced by a second, adversarial agent per
mechanism report that re-ran the load-bearing commands and compared
output.

| Report | Verdict | What the re-run found |
|---|---|---|
| `1` NOTA the language | **partial → corrected** | One fabricated grep-hit line in §4.2; re-run returns zero output. Every other command (174-test tally, the live 19-byte rkyv round-trip, lexer/encoder greps) matched verbatim. The invented line is now removed and annotated. |
| `2` schema ↔ NOTA | **real** | `.schema`/`.asschema` sha256 byte-identical; schema-next 116-test tally exact; `emit_artifacts` byte-identical to checked-in. |
| `3` schema stack pipeline | **real** | All three suite totals (36/116/51) exact; the stale-artifact panic (`build.rs:39:14`, exit 101) reproduced verbatim; four md5 checksums identical. |
| `4` schema emits an engine | **real** | Trait line numbers, the `RustEmissionTarget` enum, `emits_signal_engine_support`, and all three `impl … Engine` sites matched verbatim. |
| `5` schema emits wire-only | **real** | signal-spirit generated output 232 lines, `grep -c Engine == 0` reproduced; spirit's `SignalEngine` trait + impl matched verbatim. |
| `6` runtime triad in spirit | **real** | The verifier rebuilt the daemon from a throwaway config and reproduced the **entire live CLI↔daemon round-trip** — six typed NOTA replies, the deterministic digest marker, the exact 561152-byte durable `.sema`. |

The one fabrication was a single invented grep result whose own
conclusion was correct; the adversarial pass caught it, located it to
the line, and it is fixed. Five of six reports reproduced with zero
material drift. **The reports can be trusted as run-real evidence.**

## The most important design constraints, isolated

This is the heart of what you asked for: the few constraints that, if
violated, break the system's purpose — the ones that belong in repo
`INTENT.md` files. They recurred across every mechanism report and
intent review. Twelve, grouped by layer:

### NOTA (the language floor)
1. **The encoder structurally cannot emit a quotation mark.** `write_string`
   has exactly three branches (bare ident / `[|…|]` block / `[…]` inline);
   there is no fourth quote branch. This is what makes every NOTA value
   embedding-safe inside any double-quote host (JSON, Rust, shell, …).
   *(nota-codec; verified: `write_bracket_string` body, and a live
   `([he said 'yes'])` round-trip with "contains a double-quote char?
   false".)*
2. **Records are positional, never `(key value)`.** Type first, then
   fields in declared order. The Lisp/JSON shape is not NOTA. *(nota)*
3. **Three-case PascalCase rule.** `(Variant fields…)` data variant,
   `(fields…)` struct, bare `Variant` unit; a bare PascalCase at a
   `String` position is a typed error. `Bool` is `True`/`False`, `Option`
   is `None`/`(Some inner)`. *(nota)*

### Schema (the type layer)
4. **The schema IS NOTA, and lowering is deterministic.** A `.schema`
   file is authored NOTA; schema-next lowers it to ordered, macro-free
   `Asschema`. Re-lowering an unchanged schema is byte-identical
   (sha256-verified). *(schema-next)*
5. **The layering firewall.** NOTA owns *structure* (delimiters, spans);
   schema owns *type-names* (`[]` is raw vector structure, `(Vec T)` is a
   schema type-reference); emission owns *Rust*; runtime owns
   *mechanics*. Each boundary is load-bearing and the newer repos hold
   it cleanly.
6. **Emission is data-before-text.** `Asschema` → typed `RustModule` →
   rendered `RustCode`. The same "parse to typed model, then render"
   shape repeats at every stage; nothing hand-builds output strings
   from raw text (except, see gap #4 below, a few generated panic arms).

### Emission targets and the plane split
7. **Five emission targets gate the plane split.** `WireContract` (zero
   engines — public contracts), `SignalRuntime`/`NexusRuntime`/`SemaRuntime`
   (one engine each — daemon-local planes), `ComponentRuntime` (legacy
   all-in-one). A daemon's three plane schemas emit three engine traits,
   each implemented by one actor. *(schema-rust-next; this is the
   SignalRuntime resolution, now carried by report 527.)*
8. **"Signal schema" means two different files.** Public
   `signal-<component>` contract = `WireContract` (engine-free); daemon-local
   `<component>/schema/signal.schema` = `SignalRuntime` (emits `SignalEngine`).
   *(now in `skills/component-triad.md`.)*
9. **Source-visible emission.** Generated Rust lands under `src/schema/`,
   not hidden in `OUT_DIR` — generated interfaces are reviewable.
   *(schema-rust-next.)*

### Methods, runtime, and the edge
10. **Methods on data-bearing nouns, never free functions.** The audit
    confirms this is *achieved* in every new crate (schema-next,
    schema-rust-next, sema, sema-engine, spirit, signal-spirit: **zero**
    free functions); the debt is confined to the older foundational
    layer. *(workspace records 712/882.)*
11. **The triad-engine readability principle.** *Types name the work,
    schema names the interface, generated Rust names the objects and
    traits, and handwritten code is mostly the real algorithm — match
    typed input, decide, call the next typed interface, return typed
    output.* The intent reviewer flagged this (buried at
    `triad-runtime/INTENT.md:7`) as **the thesis of the entire
    schema-derived stack.** Strong candidate for promotion to `ESSENCE.md`.
12. **The single-argument NOTA edge.** Every binary takes one argument: a
    NOTA string/file, or (for a daemon) a binary rkyv `Configuration`.
    Binary rkyv is universal between machines; NOTA *text* is
    feature-gated at the human/CLI edge — the daemon must not depend on
    nota-next, enforced by a `cargo tree` test, not a comment. *(spirit,
    triad-runtime.)*

## Where the code actually lives (report 7)

- **23,698 committed src LOC** across the seven core repos; only **11.6%
  is committed-generated**, all in `spirit/src/schema/`. The other six
  core repos commit zero generated `src/`.
- **The mass is the generator, not the output.** schema-next (8,147) +
  schema-rust-next (4,575) = **61% of hand-written core src**. The
  biggest hand-written file is `schema-rust-next/src/lib.rs` at 3,462
  LOC — the Rust emitter itself, structurally healthy (24 structs, 24
  impls, zero free functions).
- **Amplification:** signal-spirit's 11 declaration lines emit a 232-line
  Rust file (~21×).

## Repetition and bad patterns (reports 7 + 8)

The stack is **healthy and the debt is cleanly stratified by age.**
Verified-clean: no `anyhow`/`eyre`/`Box<dyn Error>` anywhere; no
`clap`/flag-soup in production; the deployed CLI replies bracket-only
(zero quotes, live-confirmed); single-colon schema paths; sema/sema-engine
carry zero `unwrap`/`expect`/`panic` *and* zero free functions; TODO/FIXME
density near zero. Real findings, report-only:

| Finding | Where | Kind | Severity |
|---|---|---|---|
| 260-line `build.rs` verbatim copy-paste (4 lines differ) | signal-upgrade vs meta-signal-upgrade | repetition | high |
| Generator's own public API unstable — 4 distinct `build.rs` styles co-exist | signal-{spirit,cloud,domain-criome,upgrade} | bad-pattern | high |
| `WireCodec` ZST namespace holder — the only one in the stack, in the flagship contract, likely to be copied | signal-spirit/src/lib.rs:34 | bad-pattern | high |
| ~18 `round_trip.rs` share one skeleton; rkyv feature string copy-pasted in 68 `Cargo.toml` | signal-* | repetition | medium |
| Daemon is actor-named in prose but `Mutex`-implemented (no kameo; 17× `.lock().expect`) | spirit/src/engine.rs | bad-pattern | medium |
| Generated code emits `panic!` arms into consumer-facing methods via string-concat codegen | schema-rust-next/src/lib.rs:2551+ | bad-pattern | medium |
| nota-box re-implements NOTA structure scanning beside nota-codec's canonical lexer | nota/nota-box/src/decode.rs | repetition | medium |
| Deployed spirit-v0.5.1 read-side `Observation` enum diverged from committed schema (write verified live, read path behind) | deployed binary vs spirit/schema | gap | medium |
| Free-function debt confined to the older layer: nota(27), signal-core(26), nota-codec(18) | foundational crates | bad-pattern | medium |
| `temporal.rs` is a pure calendar free-function bag (missing noun) | nota-codec/src/temporal.rs | bad-pattern | low |

## INTENT.md — state of the union (reports 9 + 10)

Your principle (record `nqsb`): every repo needs an INTENT.md holding
the most important *and only* the most important intent.

- **Core stack: all nine repos have an INTENT.md — no missing gap.** The
  problem is the **opposite of missing — over-capture.** schema-next
  (331 lines), schema-rust-next (286), and spirit (263) have grown into
  near-exhaustive design logs where durable intent is buried under
  implementation status that belongs in `ARCHITECTURE.md`. **triad-runtime
  (51 lines) and signal-spirit (87) are the curated models to imitate.**
  Per-repo distillation proposals are in report 9.
- **nota and schema are the legacy/predecessor track** — they need a
  one-line supersession banner naming nota-next/schema-next/schema-rust-next
  as the live stack. `schema/INTENT.md` is the most drifted (still posing
  open questions the replacements answered structurally).
- **Wider stack: 14 of 78 active repos have an INTENT.md; 64 do not.**
  The single largest coherent gap: **every `signal-*`/`owner-signal-*`/
  `meta-signal-*` contract repo lacks one, without exception.** Highest-value
  missing daemon is **mind**. (Your own `primary/INTENT.md` exists, 44 KB —
  the workspace is covered.) Full presence table in report 10.

## Recommendations awaiting your decision

All report-only; nothing was changed. In rough priority:

1. **Distill the three over-long core INTENT.md files** (schema-next,
   schema-rust-next, spirit) down to the triad-runtime model — keep the
   constraint clusters, move status/mechanism to `ARCHITECTURE.md`.
   Proposals drafted in report 9.
2. **Promote the triad-engine readability principle to `ESSENCE.md`** (or
   workspace `INTENT.md`) — it is the stack's thesis and currently lives
   in one repo's line 7. Needs your blessing since ESSENCE is psyche-intent.
3. **Fill the missing INTENT.md files**, starting with the daemons (mind,
   router, message) and then the contract families — directly serving the
   universality principle you just stated.
4. **Mechanical de-dup**, low-risk: collapse the 260-line build.rs
   copy-paste and the 4 build.rs styles onto the shared `GenerationDriver`
   helper; share the `round_trip.rs` skeleton.
5. **WireCodec ZST** (signal-spirit) — move the four codec methods onto
   the schema-emitted `Input`/`Output` nouns before the pattern is copied
   into other contracts.
6. **Confirm two loose ends:** the deployed-vs-source `Observation` read
   path (spirit-v0.5.1), and whether `signal-frame` is still active or
   folded into signal-core/triad-runtime.

Beads were deliberately **not** filed (you said "report them and then we
can see what we want to do"). I can file beads for any subset on your
word, or start applying the INTENT.md distillations — on primary I edit
directly; on the code repos that means designer `next` branches for the
operator to integrate.
