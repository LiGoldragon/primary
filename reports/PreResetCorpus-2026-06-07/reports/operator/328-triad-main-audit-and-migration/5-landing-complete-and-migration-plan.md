---
title: 328 — triad_main landed + verified; component migration plan
role: operator
variant: Psyche
date: 2026-06-06
topics: [triad-main, landing-complete, component-migration, migration-plan, readiness]
description: |
  triad_main (the emitted daemon module) is landed across triad-runtime,
  schema-rust-next, spirit — audited, the string-emitter flaw fixed (token
  rewrite), all audit fixes + an E0284 regression fixed, verified green
  end-to-end. This file records the landing and the component-migration plan:
  readiness survey, the per-component recipe (the spirit template), and the
  order.
---

# 328 — Landing Complete + Migration Plan

## Landing complete (verified by me, pushed)

| Repo | main | What landed | Verified |
|---|---|---|---|
| triad-runtime | `1bd383bf` | `DaemonConfiguration` + `ExitReport::from_result` | 44 tests, clippy -D |
| schema-rust-next | `b75c7f50` | token daemon emitter (4np2 fix) + audit fixes (M3 dead code, m1/m2/m4, n1/n2) + E0284 disambiguation | 61 tests incl 6 daemon goldens, clippy -D |
| spirit | `d406d198` | pilot regenerated against the token emitter | `--all-features` 77 pass / 9 nix-ignored; **process_boundary 8/8** over a real socket; freshness guard clean |

`daemon_emit.rs`: `self.line` 404→0, `quote!` 0→30, `ToTokens` 0→11, `RustWriter` 0.
The audit's headline `4np2` violation is closed. One real regression caught that
the schema-rust-next goldens missed but spirit's actual compile surfaced: the m2
fix made `SubscriptionWriters<Daemon>` generic-but-impl'd-for-HashMap →
unconstrained type param → E0284; fixed by emitting a disambiguated
`SubscriptionWriters::<Daemon>::deliver(...)` call.

## The migration recipe (the spirit template)

A component on the triad runtime carries:
1. **Three plane schemas** — `schema/signal.schema` (daemon-local signal runtime),
   `schema/nexus.schema` (the internal-feature catalog, z6qu — every internal
   feature a declared Nexus verb+object), `schema/sema.schema` (durable
   single-writer state); plus the wire contract(s) `signal-<c>` (+ `meta-signal-<c>`
   when there's an owner tier).
2. **build.rs** — `GenerationPlan…with_module(signal_runtime_module)…nexus_runtime()…sema_runtime()…wire_contract(meta-signal)…daemon_module("signal", daemon_shape())` + a `daemon_shape() -> NexusDaemonShape` (process name, working tier, optional meta tier + mode).
3. **`impl ComponentDaemon for <C>Daemon`** — the only hand-written daemon code: the 1488 escape hatches (`Configuration`/`Engine`/`Error`/`PROCESS_NAME` + `build_runtime` + `handle_working_input`). The bin is a one-liner `<C>Daemon::run_to_exit_code()`.
4. **deps** — `triad-runtime` (runtime) + `schema-rust-next` (build-dep, the emitter).

## Readiness survey + order

| Component | Plane schemas | triad-dep | daemon bin | `signal-` | `meta-signal-` | Tier |
|---|---|---|---|---|---|---|
| spirit | ✓ (done) | ✓ | ✓ | ✓ | (single-repo pilot) | done |
| **message** | concept only | ✓ | ✓ | ✓ | — | single |
| persona | concept only | — | ✓ | ✓ | — | single |
| mind | concept only | — | — | ✓ | — | single |
| router | concept only | — | — | ✓ | ✓ | two-tier |
| orchestrate | concept only | — | — | ✓ | ✓ | two-tier |
| terminal-control | **no repo** | — | — | (`signal-terminal-control` forming) | (forming) | — |

**Order (most-ready first):**
1. **message** — has the triad dep + daemon bin + `signal-message`; the cleanest
   pattern-setter (single tier).
2. **persona**, **mind** — single-tier; persona has a daemon bin.
3. **router**, **orchestrate** — two-tier (working + owner-only meta listener);
   exercise the meta-signal path.
4. **terminal-control** — blocked: the repo does not exist (only `terminal` /
   `terminal-cell` + a forming `signal-terminal-control`). Needs the triad repo
   created (or the psyche means `terminal`). FLAGGED for the psyche.

Each migration is a real design+implement step (designing the three plane
schemas from the component's concept + wire contract, then wiring + verifying),
not a mechanical edit — so the migration proceeds component-by-component,
verified green per repo, starting with message.
