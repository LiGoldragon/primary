*Kind: Audit Slice · Topic: schema/header/macro layer · Date: 2026-05-24 · Lane: operator*

# 176.1 · Schema/header/macro layer

## Scope

Read-only audit of:

- `/git/github.com/LiGoldragon/schema`
- `/git/github.com/LiGoldragon/signal-frame`
- `/git/github.com/LiGoldragon/signal-frame/macros`
- `/git/github.com/LiGoldragon/nota`
- `/git/github.com/LiGoldragon/signal-persona-spirit`

## What Is Live On The Code Path

### Schema file input reaches the signal macro

`signal-frame/macros/src/lib.rs` switches to schema mode when
`signal_channel!` receives the `[schema]` marker. That path calls
`schema_reader::read_default_schema()` and feeds the resulting generated
`ChannelSpec` into the existing emitter.

`signal-persona-spirit/src/lib.rs` uses this path directly:

```rust
signal_channel!([schema]);
```

That means `signal-persona-spirit/spirit.schema` is not just a marker. It is
the actual input for the generated Spirit ordinary contract surface.

### ShortHeader emission is on the frame path

The macro emits `LogVariant` for generated operations. `signal-frame` then uses
that trait on ordinary frame construction:

- `Request::short_header()` reads the first payload's `log_variant()`.
- `ClientFrame::request_frame()` calls `request.short_header()`.
- `ExchangeFrame::with_short_header()` stores the generated header.
- frame encoding writes the 8-byte short header before the archived body.

So outbound Spirit request frames from the generated CLI path do carry the
schema-derived `ShortHeader`.

### The macro emits dispatch traits

The emitter also generates:

- `kind_from_short_header`
- operation handler traits
- `OperationDispatch`
- mismatch errors through `signal_frame::OperationDispatchError`

The contract tests in `signal-persona-spirit/tests/short_header.rs` prove that
the generated dispatch rejects header/body mismatch and unknown roots.

## What Is Generated But Not On The Production Path

### Receive-side ShortHeader triage is test-only

The daemon path decodes full frames and dispatches decoded `Operation` values.
The generated `OperationDispatch` / `kind_from_short_header` path is exercised
in tests, but the Spirit daemon does not use it to triage before body decode.

This is the main gap against the directive that "64-bit header emitting and
consumption for signal/receiving dispatch triage" should be direct logic, not
only a test witness.

### Box-form NOTA codecs are test-only

`signal-frame/macros/src/emit.rs` emits `nota_box::BoxedNotaEncode` and
`BoxedNotaDecode` implementations for boxed schema types. Spirit has
`signal-persona-spirit/tests/box_form.rs` proving this works for `Entry`.

Production frame round-trips still use rkyv length-prefixed frames. Ordinary
text round-trips still use `nota-codec`. The box-form path is not yet the CLI or
daemon wire path.

### Leaf types remain handwritten

The Spirit schema currently drives the operation/reply/event/header surface.
Most domain leaves are still declared by hand in Rust:

- `Entry`
- `StampedEntry`
- `Observation`
- `Subscription`
- `Topic`
- `Summary`
- `Quote`
- `Kind`

This is compatible with the current MVP, but it is not the full "schema emits
all corresponding signal types" vision.

## Missing Or Incomplete

### Owner Spirit is not schema-derived

`owner-signal-persona-spirit` still uses a handwritten `signal_channel! { ... }`
body. It has not moved to `.schema` input.

### Schema-derived VersionProjection is absent

`signal-persona-spirit/src/migration.rs` contains handwritten
`VersionProjection` implementations. The macro does not derive these from
`spirit.schema` or a schema diff.

### Storage descriptors are absent from macro output

The schema crate has an upgrade model and assembled routes/types/features, but
no observed macro output for storage descriptors used by `persona-spirit`'s
store.

## Verdict

Schema macro adoption is real in the Spirit ordinary contract, and short-header
emission is genuinely on the frame path. Receive-side header dispatch,
box-form wire use, version projection emission, owner-signal schema adoption,
and storage descriptor emission remain incomplete.
