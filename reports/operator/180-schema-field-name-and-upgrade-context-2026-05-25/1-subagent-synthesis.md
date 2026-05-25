# 180.1 - Subagent synthesis

## Bohr

Bohr framed the current schema pipeline as:

1. A `.schema` source file declares component shape.
2. NOTA parses it into token/tree form.
3. Built-in macro variants lower schema node positions.
4. The fixed-point output is an assembled schema.
5. Codegen emits signal types, ShortHeader tables, storage shape, and
   upgrade/projection pieces.
6. Component tests prove the generated pieces are the production path.

Bohr's strongest recommendation was to keep upgrade handover logic
separate from schema assembly, but make the handover consume
schema-derived projection and header artifacts. That preserves the clean
division:

- schema derives what a version can read, write, route, and project.
- handover decides when two versions coordinate and who is authoritative.

## Hegel

Hegel audited the actual Spirit/code path and found that schema-derived
pieces are already used in these production or constraint paths:

- `signal-persona-spirit/src/lib.rs` uses
  `signal_channel!([schema])`.
- `signal-persona-spirit/spirit.schema` is the schema source.
- `signal-frame/macros/src/schema_reader.rs` consumes the schema crate.
- `persona-spirit/src/daemon.rs` validates schema-derived ShortHeaders
  before ordinary ingress dispatch.
- `upgrade/src/migrations/persona_spirit/...` consumes the
  contract-owned version projection shape.

Hegel also found the still-missing pieces:

- Rust data records are still handwritten in the contract crate.
- `VersionProjection` is not generated from schema diffs.
- owner-signal schema integration is not yet parallel to ordinary signal.
- storage descriptors are not yet schema-derived.

The smallest non-speculative implementation target was the field-name
surface: make the schema reader preserve explicit schema field names and
make the macro emitter use those names before falling back to type-name
inference.
