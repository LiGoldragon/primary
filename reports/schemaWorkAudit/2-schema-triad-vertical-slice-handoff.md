---
title: 2 - schema triad vertical slice handoff
role: schemaWorkAudit
variant: Handoff
date: 2026-06-24
topics:
  - schema
  - schema-daemon
  - specified-schema
  - vertical-slice
description: |
  Alignment-interview handoff after the psyche clarified the schema endpoint:
  full schema component triad, manifest-loaded schema environment, typed source
  maps, canonical schema re-encode, Rust regeneration, and fast feedback.
---

# 2 - schema triad vertical slice handoff

## Intent Anchors

- [Schema is the textual representation of the psyche's idea language: it is not merely a code generation input, but the text form where the idea language is expressed, inspected, and authored.] Spirit accepted this during the interview as the schema-as-idea-language record.
- [The schema component is a full component triad. Its daemon loads a schema environment from a manifest that selects the versions of modules used by the import system; resolves schemas, namespaces, core definitions, and macro libraries from that environment; parses source files with source-map awareness of where each block begins and ends and what type each block has; and serves as the extensible schema language-server surface for inspection, editing, code generation, upgrade, and future schema-aware features.] Spirit clarified the existing schema-daemon record with this endpoint.
- [Authored `.schema` sugar decodes into `SpecifiedSchema`, the first-class, typed, rkyv-serializable semantic schema value; Rust code, help, instance-schema, hashes, language-service features, and text/debug projections are projections from `SpecifiedSchema`, while source locations and shorthand origins live in a `SourceMap` companion.]

## Alignment Standard

The audit now uses two judgments:

| Question | Standard |
|---|---|
| Endpoint match | Does the implementation already realize the psyche's intended end shape? |
| Trajectory | Is the implementation moving in a direction that can reach that end shape without preserving the wrong spine? |

Under that standard, the current implementation is not endpoint-aligned yet. It is on trajectory where it has real `SpecifiedSchema`, structural macro nodes, and Rust emission over `SpecifiedSchema`, but it has not landed the full schema daemon triad, manifest-loaded schema environment, typed source-map service, canonical schema re-encode, or daemon/language-server query surface.

## Decisions Made

| Topic | Decision |
|---|---|
| What `SpecifiedSchema` is | `SpecifiedSchema` is the finished semantic snapshot after authored source, imports, macro expansion, shorthand, and resolution have been interpreted. |
| What `SpecifiedSchema` is not | It is not the full editing/source layer. Exact source spans, aliases, shorthand choices, and block provenance belong in a companion typed source/source-map layer. |
| Re-encoding | `SpecifiedSchema` must re-encode to canonical `.schema` text. Exact original authoring text can wait for the source-map/editing layer. |
| First slice scope | The first slice should be comprehensive enough to prove the spine: manifest, environment, parse, import resolution, typed source maps, `SpecifiedSchema`, canonical `.schema` re-encode, Rust regeneration, and tests. |
| Feedback pressure | The slice should be quick and feedback-oriented; avoid spending the first pass on broad platform completeness before the schema-environment behavior is visible. |
| Canary sequence | Start with a small real multi-module `schema-rust-next` fixture, then use `spirit` and `signal-spirit` as higher-value canaries. |

## First Vertical Slice

Build this as the first concrete feedback slice:

1. Load a schema environment manifest.
2. Select the schema module versions named by that manifest.
3. Parse multiple `.schema` modules under that environment.
4. Resolve at least one versioned import across modules.
5. Produce typed source maps that identify file ranges, block boundaries, and schema node types.
6. Lower the environment result into `SpecifiedSchema`.
7. Re-encode `SpecifiedSchema` into canonical `.schema` text.
8. Regenerate Rust from the same `SpecifiedSchema`.
9. Prove the generated Rust still works.
10. Expose one feedback query through a daemon-shaped API surface.

Recommended first surface, still open until implementation starts: use a CLI command backed by daemon-shaped library code. That gets feedback faster while keeping the handler shape portable to the eventual schema daemon request.

## Acceptance Checks

| Check | Pass Condition |
|---|---|
| Manifest load | The command reports the manifest, selected module versions, and module paths used for the environment. |
| Import resolution | A real import resolves through the manifest-selected environment, not through ad hoc path lookup. |
| Typed source map | The output can name at least one source file range, its block boundary, and its schema node type. |
| Canonical schema text | `SpecifiedSchema` re-encodes to canonical `.schema` text and can be parsed/lowered again. |
| Rust regeneration | If regenerated Rust is byte-identical to the checked-in fixture, pass immediately. If it differs only because canonical schema text normalized the input, compile and run existing fixture tests. Behavioral differences fail the slice. |
| Canary path | The small multi-module fixture passes first; then `spirit` and `signal-spirit` are run as larger canaries. |

## Tracking

Filed a new follow-up bead for the slice: the schema triad vertical-slice work, `primary-lwc6`.

Existing related follow-ups remain relevant:

- Make `SpecifiedSchema` the package/build canonical artifact in `schema-next` and `schema-rust-next`, `primary-ing7`.
- Repair the `schema-rust-next` generated legacy-helper Nix witness, `primary-yeom`.

## Intent Surface

Do not manifest this interview by editing repo `INTENT.md` files. Spirit is the
current intent source; static intent files are deprecated. Future agents should
query Spirit for the schema endpoint and keep implementation-facing surfaces
current through reports, beads, architecture notes, and code changes.

For this slice, the implementation-facing summary is:

- `schema-next` owns the schema environment manifest model, typed source/source-map layer, canonical `.schema` projection from `SpecifiedSchema`, and the eventual schema daemon/library/macro substrate.
- `schema-rust-next` consumes `SpecifiedSchema` from the environment/build spine and participates in the vertical slice by regenerating Rust from the same semantic snapshot that re-encodes canonical schema text.

## Audit Update

The previous audit's main conclusion still stands, but the endpoint is sharper now. The current implementation is a partial landing, not a match for the intended endpoint. The next useful work is not merely to swap old `Schema` for `SpecifiedSchema`; it is to prove the whole language spine quickly: manifest environment to typed source map to `SpecifiedSchema` to canonical schema text to regenerated Rust.
