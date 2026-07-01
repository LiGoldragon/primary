# NOTA Strict-Positional Fix — Design and Plan

## Task and Scope

Establish durable design and tracking for the NOTA strict-positional fix lane.
This document is the pickup surface for the implementing worker and for
post-implementation audit. It records the problem statement, audit verdict,
accepted design, scope decision, and residual items.

Audit evidence: `agent-outputs/NotaSchemaAudit/Machinery.md`,
`agent-outputs/NotaSchemaAudit/Contracts.md`.

## Problem

NOTA is a strict positional format. A positional or variant-payload component
must never disappear from the text form: the position carries the type
identity.

The bug: `(Optional T)` used as a variant-payload type lets bare `Data` decode
to `Data(None)` and encode back to bare `Data`. This is a silent omission and
an atom demotion. Both violate strict-positional NOTA because the payload
position is present at decode time but absent at encode time.

Custom per-type codec logic is forbidden; only the canonical shared codec
(`#[derive(nota::…)]`) is allowed.

## Audit Verdict

The bug is isolated, not an epidemic.

The only hand-rolled NOTA implementation in the generator is the
`schema-rust-next` crate's `RustOptionalEnumNotaTokens` path
(`lib.rs` approximately lines 4822–5196). Everything else in the generated set
uses the canonical `#[derive(nota::…)]` path.

Manifested anti-patterns:

- Exactly 13 enum tuple-variant `Option<T>` payloads across exactly 2 crates.
- Crates affected: `signal-spirit` (12 variants), `signal-mentci` (1 variant).
- Backed by exactly 6 hand-written NOTA-body codecs in the 91-file generated set.

## Accepted Design (Option a)

Forbid `(Optional T)` as a positional or variant payload via a `schema-next`
lowering validation error.

Delete the `schema-rust-next` `RustOptionalEnumNotaTokens` codegen path.

Model the general case as an explicit member with a required payload. For
example: `(Data DataLeaf)` with `DataLeaf [All …]`, yielding
`(Technology (Software (Data All)))`. Named `(Optional T)` brace-record fields
remain legal. The `nota-next` codec crate is unchanged.

## Scope Decision (Psyche-Approved)

Machine-enforce globally. Migrate both affected crates. Migrate downstream
`spirit` and `mentci`/`mentci-lib` consumers.

## Boundary

This is not a Mind redesign. Do not copy Spirit's pattern into Mind.
`signal-mentci`'s case is a pre-existing peer bug.

## Residual and Parked Items

### Psyche-Gated Blocker

Wire/storage compatibility and `spirit` deployment decision. No work may
proceed on this front without psyche approval.

### Implementation Blocker Pending Verification

Scope-enum second inconsistency (item #1): to be verified during
implementation, not pre-decided.

### Low-Priority Parked

- Item #2: `ListenerTier` lowercase Display divergence.
- Item #3: query/selection newtype style.

## Bead Graph Location

Beads filed under this lane are tagged `nota-strict-positional` in the primary
workspace tracker.
