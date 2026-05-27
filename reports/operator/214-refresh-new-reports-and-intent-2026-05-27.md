# 214 — Refresh: new reports and intent after schema-source emission

## Scope

Refresh pass over the newest Spirit records and reports after the
`spirit-next` checked-in generated-source landing.

Read surfaces:

- Spirit records 874-919, with emphasis on 909-919.
- `reports/designer/385-nota-schema-next-stack-design-via-nix-tests-2026-05-27.md`
- `reports/designer-assistant/383-next-version-schema-design-study-and-implement-2026-05-27.md`
- `reports/designer-assistant/384-emit-to-src-schema-2026-05-27.md`
- `reports/operator/213-nota-schema-next-stack-focused-test-design-2026-05-27.md`
- `reports/system-designer/35-schema-deep-new-logics/3-overview.md`
- `reports/system-operator/163-critique-of-162-after-schema-next-refresh-2026-05-27.md`
- `reports/system-designer/36-criomos-reconciliation-audit.md`
- `reports/cloud-operator/8-cloud-component-design-recap-2026-05-26/4-overview.md`
- `reports/cloud-designer/2-cloud-component-design-recap-2026-05-27/4-overview.md`

## Intent Refresh

Records 909-912 settle the schema/reporting correction:

- `src/schema/lib.rs` and `src/schema/<module>.rs` are the current target for
  schema-derived Rust visibility. `OUT_DIR/schema` is corrected away.
- The current schema-stack version must materialize generated Rust under that
  source-tree path.
- Nota/schema design reports use short focused Mermaid graphs, each tied to
  code and Nix-test witnesses.

Records 913-919 open a parallel cloud/system arc:

- CriomOS production-to-lean reconciliation should be audited against the
  refreshed schema-next context.
- Cloud component production work uses the existing old NOTA and old signal
  macro stack for the first production slice, not the new schema stack.
- Cloudflare DNS read/set is the first useful cloud path; redirects are a
  follow-up if the Cloudflare surface supports it cleanly.
- Cloud-designer and cloud-operator are working in parallel: designer prototype
  branch plus operator working tool.

## Current Situation

The schema-next stack is now split into two documented layers:

- `designer/385` explains `schema-next` itself by five Nix-test scenarios:
  key/value brace namespaces, two-layer macro registry, `schema/lib.schema`
  package loading, colon-qualified names, and method-only Rust discipline.
- `operator/213` explains the full consumer path through `spirit-next`: NOTA
  CLI input, schema-generated `Input`/`Output`, binary short-header+rkyv signal
  frames, executor lowering into generated `SemaCommand`, and process-boundary
  tests.

`spirit-next` is current on main at commit `0296be2d6b9c`
(`materialize generated schema source`). It has checked-in generated source at
`src/schema/lib.rs`; `build.rs` regenerates into memory and fails if the file is
missing or stale; `nix flake check` passed.

One implementation-definition seam remains: `schema-rust-next/main` commit
`5ca1c964` still emits `GeneratedFile.path == "schema/lib.rs"` and
`"schema/signal/public.rs"`. `spirit-next` materializes that under
`crate_root/src/`. Designer-assistant report 384 has a branch where
`schema-rust-next` itself emits `src/schema/...`. The intent wording supports
the latter more literally. This is the next small operator decision point.

## System Arc

The schema-deep Lojix pilot in `reports/system-designer/35...` is strong:
green `nix flake check`, 28 schema-emitted nouns, 9 actor planes, process tests,
and no production free functions. It did not fork `schema-next`; it navigated
the four-root limitation by keeping internal command/reply types as namespace
types rather than signal-frame roots.

The CriomOS reconciliation reports say the existing `horizon-leaner-shape` work
is useful but no longer the whole "next stack" story. The new question is
whether production fixes should be ported only into the old lean stack, or also
mapped into the schema-deep future as schema nouns, actor messages, and SEMA
records. The most important unresolved system questions are builder capability
for aarch64, repository source distribution, and whether Horizon should keep
walking legacy NOTA migrations or move to `nota-next`/`schema-next`.

## Cloud Arc

Cloud is now framed as a production-first component using the old NOTA/signal
macro stack. That is explicit, not drift: the new schema stack remains the
future path, but Cloudflare DNS is allowed to ship on the existing stack first.

Current real shape:

- `cloud`, `signal-cloud`, and `owner-signal-cloud` exist.
- Ordinary cloud can observe/validate Cloudflare DNS state.
- Owner cloud owns account registration, policy, plan preparation, approval,
  and apply ceremony.
- Live mutation is intentionally still blocked by typed rejection until the
  Cloudflare mutation actor/path is real.

Most important next cloud items: implement Cloudflare DNS set path, decide
Mutate/Query channel split timing, clarify schema-engine cutover timing for
cloud, and keep credentials out of ordinary signals/logs/source.

## Operator-Relevant Questions

1. Should I integrate the designer-assistant `schema-rust-next` branch so
   `RustEmitter::emit_file()` itself returns `src/schema/<module>.rs`, or keep
   the current split where `schema-rust-next` returns `schema/<module>.rs` and
   consumers choose `src/` as the materialization root?
2. Should the next schema-stack operator slice be the regeneration command for
   `src/schema/lib.rs`, since `spirit-next` now only detects staleness and does
   not rewrite generated source?
3. For system work, is the next operator priority lean cutover repair
   (`horizon-leaner-shape`) or schema-deep Lojix amalgamation?
4. For cloud work, should operator take the Cloudflare DNS set path now under
   the old signal macro stack, or wait for the cloud-designer prototype/audit
   to settle the remaining open positions?
