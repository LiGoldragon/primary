---
title: 1 — schema implementation intent alignment audit
role: schemaWorkAudit
variant: Audit
date: 2026-06-24
topics:
  - schema
  - schema-rust
  - nota
  - intent-alignment
description: |
  Audit of nota-next, schema-next, schema-rust-next, and downstream binary
  boundary canaries against current psyche intent for the schema stack.
---

# 1 — schema implementation intent alignment audit

## Intent Anchors

This audit treats the following psyche-derived intent as the measuring surface:

- [Structural macro constructs are schema values, not a frozen compiler table; files are typed trees, grammar is type, and NOTA's own grammar must be schema-expressible.]
- [NOTA structural extension is type-directed matching over raw parser nodes; structural macro nodes are NOTA enums decoded by shape, not runtime string registries.]
- [Everything above the raw parser that reads NOTA-shaped structure goes through typed structural macro nodes; surviving hand-parsing sites are violations to retire or explicitly justify.]
- [Authored `.schema` sugar decodes into a fully specified, rkyv-serializable schema-in-Rust value whose public Rust name is `SpecifiedSchema`; Rust code, help, instance schemas, hashes, diagnostics, and editor projections are projections from that value.]
- [Separate Asschema IR is removed; its old resolution work lives as methods on schema-in-Rust types during the lower step.]
- [Schema-to-Rust lowering is token-based through `quote`, `proc_macro2`, `TokenStream`, and `ToTokens`, not a hand-rolled string emitter.]
- [Hand-written Rust is engine logic only; structural pieces such as NOTA/rkyv forms, data definitions, enum variants, and field accessors emit from schema.]
- [Daemons accept binary startup and binary meta-signal configuration; NOTA/text is a CLI or build-time edge, never daemon runtime configuration.]

## Verdict

The implementation is materially moving in the intended direction, but it is not yet fully aligned with the current psyche endpoint. The strongest alignment is in `nota-next` and the `schema-rust-next` emitter core: typed structural macro nodes exist, `SpecifiedSchema` is the internal Rust emission substrate, Asschema is absent from active artifacts, and downstream binary-only canaries keep NOTA out of daemon runtime dependency trees.

The remaining gap is canonicality. `schema-next` now has the `SpecifiedSchema` value, binary round-trip methods, and tests, but its central lower/build paths still construct old `Schema` first and then convert to `SpecifiedSchema`. That is a good migration step, not the final psyche-intended shape where the fully specified value is the first-class artifact every projection consumes.

## Aligned Evidence

| Area | Evidence | Assessment |
|---|---|---|
| Structural macro node shape | `nota-next/derive/src/lib.rs:668` accepts enum input and rejects structs/unions; `:759` rejects named variant fields. | Aligns with current typed structural macro node discipline: enum values decoded by shape. It contradicts one stale workspace map entry that says struct derive is already present. |
| `SpecifiedSchema` exists as a value | `schema-next/src/specified.rs:10` defines `SpecifiedSchema` as the fully specified schema value; `:130` and `:135` provide rkyv binary decode/encode methods. | Strong capability alignment. The value is real, cloneable, comparable, NOTA-decodable/encodable, and rkyv-serializable. |
| Asschema removal | Active tests and generated fixtures refer to `SchemaSourceArtifact`, `Schema`, and `SpecifiedSchema`, not `.asschema` artifacts. | Aligns with the decision that Asschema is no longer a separate IR. |
| Rust emission substrate | `schema-rust-next/src/lib.rs:136` implements `RustSchemaLowering for Schema` by converting to `SpecifiedSchema`; `:150` starts the direct `SpecifiedSchema` implementation; `:5526` shows later scans operating over `&SpecifiedSchema`. | The emitter's semantic work is now driven by `SpecifiedSchema`, with the old `Schema` API acting as an adapter. |
| Token-based Rust item emission | `schema-rust-next/src/lib.rs:6064` parses `TokenStream` into `syn::File` and renders Rust items from tokens. | Main source emission is not the old god-string-writer shape. `String` remains as the final text buffer and for headers/descriptive text, which is acceptable if kept out of semantic Rust generation. |
| Binary-only daemon boundary | `spirit` and `signal-spirit` no-default normal dependency trees do not include `nota`; their dependency boundary tests passed. | Aligns with the daemon NOTA-free runtime boundary: text remains an opt-in/client/build surface. |

## Gaps

| Gap | Evidence | Why It Matters |
|---|---|---|
| `SpecifiedSchema` is not yet the canonical package/build artifact | `schema-next/src/engine.rs:346` lowers source to `Schema`; `:355` lowers specified source by mapping through `SpecifiedSchema::from(&schema)`. `schema-rust-next/src/build.rs:522` loads `SchemaSource`, validates `SchemaSourceArtifact`, then `:531` lowers daemon modules to `Schema`. | Psyche intent says projections come from `SpecifiedSchema`. Current code can produce it, and the Rust emitter mostly consumes it, but the build pipeline still treats old `Schema` and source artifacts as the spine. |
| Hand readers remain above the raw parser | `schema-next/src/source.rs:418` manually reads import maps with `NotaBody` and `chunks_exact(2)`; many other `from_block` readers remain. Structural macro nodes also appear, for example `SourceVariantSignature` at `:2730`. | The code is mixed: some shapes use typed structural macro nodes, while other NOTA-shaped structures are still hand decoded. Intent says those sites are violations unless a narrow meaning-boundary exception is written down. |
| Verification guards are stale in places | `schema-rust-next/flake.nix:181` searches for the exact derive string `derive(nota::NotaDecode, nota::NotaEncode`, but generated fixtures now include `nota::NotaDecodeTraced` between them. | The guard fails despite the generated fixtures clearly deriving NOTA decode/encode. The check should prove the invariant structurally enough to survive trace-derive insertion. |
| Workspace map drift | `protocols/active-repositories.md` says `nota-next` already derives structural macro nodes for structs and enums; code and `skills/structural-forms.md` say enum-only. It also calls part of the `schema-rust-next` migration transitional while that repo's `INTENT.md` and `ARCHITECTURE.md` frame it as complete. | Agents reading the map can misjudge what is done and what remains. This is an auditability problem, not just stale prose. |
| Repo instruction surface is incomplete | `schema-next` and `nota-next` do not have repo-local `skills.md`; both have `INTENT.md`, `AGENTS.md`, and `ARCHITECTURE.md`. | The primary contract names `skills.md` as required repo context. Missing files create recurring session ambiguity. |
| Naming hygiene remains outstanding | Current active repos are still `nota-next`, `schema-next`, and `schema-rust-next`. | Spirit says `-next` repos won and the suffix should eventually drop. This is not an implementation blocker, but it remains unresolved intent drift. |

## Verification

| Surface | Command | Result |
|---|---|---|
| `nota-next` Rust tests | `cargo test --all-targets --all-features` | Passed. |
| `nota-next` Nix checks | `nix flake check --builders '' -L` | Passed. |
| `schema-next` Rust tests | `cargo test --all-targets --all-features` | Passed, including `specified_schema` and operator closed-claim witnesses. |
| `schema-next` Nix checks | `nix flake check --builders '' -L` | Failed in clippy: `schema-next/src/source.rs:2275` uses `ok_or_else` where Rust 1.96 clippy requires `ok_or`. This is a hygiene/check failure, not the main intent-alignment defect. |
| `schema-rust-next` Rust tests | `cargo test --all-targets --all-features` | Passed, including the canonical-entrypoint test for Rust lowering through `SpecifiedSchema`. |
| `schema-rust-next` Nix checks | `nix flake check --builders '' -L` | Failed in `generated-no-legacy-helper-surface`; the check's required derive grep is too exact for generated `derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode)`. |
| `spirit` binary dependency boundary | `cargo tree --edges normal --no-default-features`; `cargo test --no-default-features --test dependency_surface` | Passed. The binary-only surface has no NOTA runtime dependency. |
| `signal-spirit` binary dependency boundary | `cargo tree --edges normal --no-default-features`; `cargo test --test dependency_boundary --all-features` | Passed. The default runtime tree keeps text projection opt-in. |

## Follow-Up Work

The existing open queue already has broad structural-form and positional-schema items, including the structural-forms epic, universal-positional migration, and schema generics/reaction-frame integration. I did not duplicate those.

New bead-shaped follow-ups from this audit:

- Make `SpecifiedSchema` the package/build canonical artifact in `schema-next` and `schema-rust-next`: the build driver should validate a durable `SpecifiedSchema` artifact, and old `Schema` should be demoted to adapter/projection or retired.
- Repair the `schema-rust-next` generated legacy-helper Nix witness so it checks for NOTA decode/encode derives without depending on exact derive ordering or adjacency.

Recommended but not separately filed here:

- Refresh `protocols/active-repositories.md` for `nota-next`, `schema-next`, and `schema-rust-next` after the implementation owners confirm which surfaces are intended current truth.
- Add or intentionally waive repo-local `skills.md` in `schema-next` and `nota-next`.
- Treat the `-next` repo rename as a later cutover hygiene item, not as a blocker for current schema implementation work.

## Closing Assessment

The implementation is not a betrayal of psyche intent; it is a partial landing. The stack has crossed several important thresholds: typed structural macro nodes, real `SpecifiedSchema`, removal of Asschema as a separate active artifact, token-based Rust emission, and binary-only downstream runtime surfaces. The part that still does not match the stated endpoint is the artifact spine: the system can produce `SpecifiedSchema`, but it has not yet made it the thing the whole build and projection pipeline stands on.
