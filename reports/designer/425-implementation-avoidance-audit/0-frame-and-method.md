# 425 — Implementation-avoidance audit (frame + method)

*Kind: Meta-report (sub-agent session) · frame · Topics: schema, nota-extension, audit, implementation-avoidance · 2026-05-29 · designer lane*

## Frame

The operator is bootstrapping the schema (NOTA-extension) stack — nota-next →
schema-next → schema-rust-next → spirit-next. Bootstrapping is exactly when
**design-implementation avoidance** creeps in (record 1185): making the system
*look* done without genuinely implementing the design. This audit hunts for it,
checking the live code against the design intent
([[424-schema-nota-extension-full-correctness-design-intent]] + [[421-nota]] /
[[422-schema]] / [[423-signal-nexus-sema]] + the locked records).

## Method

One dispatched sub-agent (designer lane, background, read-only) reads the actual
code and fixtures and judges, per avoidance pattern, GENUINE / AVOIDED / PARTIAL
with file:line evidence. The patterns are those named in
[[424-schema-nota-extension-full-correctness-design-intent]] §5:

- circular golden tests (esp. the `.witness.txt` goldens — dump-and-reread?);
- stubs / `todo!` / `unimplemented!` / placeholder returns dressed as done;
- the per-file emitted reader standing in for the shared codec (step 2);
- a text-round-trip macro black-box standing in for macros-as-data (step 4);
- claimed-but-absent features (roots model step 5; `Path`; inline-declare);
- the emitted runtime — genuine parse/dispatch, or a stubbed skeleton.

The audit distinguishes **honest in-progress** (the operator openly flagged the
codec slice as not done — that is not avoidance) from **disguised
incompleteness**.

## Layout

- `0-frame-and-method.md` — this frame.
- `1-findings.md` — the sub-agent's audit.
- `2-overview.md` — synthesis (written after the sub-agent returns).
