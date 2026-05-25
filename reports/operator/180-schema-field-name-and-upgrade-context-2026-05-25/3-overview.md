# 180.3 - Overview

## What moved

The schema macro stack moved one step closer to the intended shape:
schema field names now survive from `.schema` into the generated
ShortHeader and NOTA box-form logic. This is not the full schema engine,
but it removes a concrete Spirit-only hack from the shared macro library.

## What this accomplishes

Contract authors can now spell the field name at the schema declaration
site when type-name lowering would produce the wrong Rust field. The
macro consumes the schema's explicit name instead of carrying a hardcoded
table of component-specific exceptions.

This is the right direction for the larger schema vision because the
schema becomes the source of truth for:

- route/header names,
- data field names,
- box-form field access,
- migration projection inputs,
- future generated storage descriptors.

## What remains

`reports/designer/333-v2-upgrade-mechanism-corrections-from-real-world-test.md`
adds a P0 blocker that this slice did not try to solve: the deployed
v0.1.0.1 retrofit and current v0.1.1 Spirit do not share a wire format
because v0.1.0.1 was built before ShortHeader landed. The next cutover
cannot be trusted until the retrofit is rebuilt against current
`signal-frame`.

Open implementation/design gaps still standing:

- `primary-602y`: rebuild persona-spirit v0.1.0.1 retrofit against
  current post-ShortHeader `signal-frame`.
- Mirror ordering: current Spirit accepts Mirror only after
  `HandoverCompleted`, while the design needs Mirror during handover.
- Divergence semantics: the wire exists, but abort/recovery policy is
  not yet enforced.
- Recovery semantics: mostly wire-only, with no real recovery executor.
- Schema diffs do not yet generate `VersionProjection`.
- Storage schema descriptors are not yet schema-derived.
- Owner signal schema coverage remains behind ordinary signal coverage.

## Recommendation

The next operator slice should take `primary-602y` before production
cutover work. It is the direct consequence of the real-world test in
`/333-v2`: without the v0.1.0.1 retrofit rebuild, the handover daemons
cannot parse each other's frames.
