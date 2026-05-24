*Kind: Synthesis · Topic: schema macro + upgrade integration audit · Date: 2026-05-24 · Lane: operator*

# 176.5 · Overview

## Headline

The schema-macro stack is partially real and partially aspirational.

The real part is important: Spirit's ordinary signal contract is generated from
`spirit.schema`, outbound frames get schema-derived `ShortHeader`s, the CLI is
generated with `signal_cli!`, and the daemon's ordinary path goes through
`signal-executor`.

The aspirational part is also important: receive-side header triage, schema
derived version projection, schema-derived storage descriptors, owner-signal
schema adoption, and most repo-wide component schemas are not on the production
path.

## Coverage Matrix

| Surface | Current status | Audit verdict |
|---|---|---|
| `schema` crate | Parses and lowers to `AssembledSchema`; tested as a library | Real substrate, not yet codegen authority |
| `signal-frame` schema adapter | Reads `.schema` into `ChannelSpec` | Real macro bridge |
| Spirit ordinary signal | `signal_channel!([schema])` consumes `spirit.schema` | Live schema-derived pilot |
| Spirit owner signal | Handwritten `signal_channel!` body | Not migrated |
| ShortHeader emission | Generated and written to frames | Live on outbound path |
| ShortHeader receive dispatch | Generated and tested | Not used by daemon ingress |
| OperationDispatch | Generated and tested | Not production-routed |
| Box-form NOTA | Generated and tested for `Entry` | Not wire path |
| `VersionProjection` | Trait exists; Spirit has handwritten impls | Not schema-derived |
| Upgrade database migration | Works in sandbox via handwritten conversion | Not schema-derived; not daemon-driven |
| Handover protocol | Spirit socket + mock upgrade driver tests exist | Not nspawn end-to-end yet |
| sema-engine commit sequence | Implemented and tested | Marker path uses it; replay not integrated |
| Concept schemas | 73 canonical markers | Mostly validation/documentation only |

## Confirmation Against Designer `/332`

Designer `/332-schema-macro-coverage-audit.md` independently reaches the same
shape:

- persona-spirit is the only live generated-code schema pilot.
- upgrade migration is handwritten.
- the schema repo is a library substrate, not a full proc-macro/codegen system.
- concept schemas are migration markers, not source-of-truth code inputs.

This operator audit adds path-level detail from the Spirit runtime, upgrade,
and nspawn surfaces.

## Highest-Value Next Work

### 1. Put ShortHeader receive dispatch on the daemon path

The generated receive-side dispatch must stop being test-only. The natural
place is a shared signal-frame server/ingress helper that peeks the short
header before body decode, classifies the root, and calls generated dispatch.

For Spirit, the concrete acceptance is: an ordinary socket request is triaged
from `ShortHeader` before the full `Operation` body is decoded.

### 2. Generate `VersionProjection` from schema diff

The next macro slice should turn the existing schema upgrade annotations into
generated `VersionProjection` impls. The current `V010ToV011` handwritten
Spirit projection is the reference output.

The first useful target is not a full universal migrator. It is a generator
that emits the identity projections plus the one changed conversion for
`Certainty -> Magnitude`, with a manual hook only where the schema marks an
ambiguous transformation.

### 3. Make `upgrade` consume the generated projection

The `upgrade` crate currently carries a separate handwritten historical/current
conversion. That duplicates the signal contract's migration knowledge.

After projection generation exists, the database migration should call the
contract-owned projection as the authority rather than re-declaring equivalent
conversion logic.

### 4. Extend the nspawn test from offline migration to socket handover

Designer `/330` landed an nspawn proof around the existing in-process migration
binary. The next operator proof is the real private-upgrade-socket handover:

- run v0.1.0 daemon
- copy/migrate to v0.1.1
- freeze public writes
- complete handover
- start or switch to v0.1.1
- verify records and in-transition behavior

This maps directly to beads `primary-dlut` and `primary-1jql`.

### 5. Promote one more small contract to schema-derived

Designer `/332` recommends `signal-version-handover`. That is a good second
pilot because it is small, directly relevant to the cutover protocol, and would
force the schema engine to handle a non-Spirit contract.

## Questions That Still Matter

1. Should receive-side `ShortHeader` triage be a mandatory `signal-frame`
   ingress primitive for every daemon, or may each daemon choose whether to use
   it? The architecture reads like mandatory, and this audit recommends making
   it shared.
2. Should schema-generated projection code live in the signal contract crate
   and be imported by `upgrade`, or should `upgrade` generate its own migration
   module from the two schema versions? This audit recommends contract-owned
   projection as authority.
3. Is the first production Spirit cutover allowed to be brief-outage
   stop/migrate/start, or must the next deploy prove private-socket handover
   first? Current code can support the former sooner; the stated long-term
   target is the latter.

## Verification Status

This audit was static/read-only with four subagents plus local grep/code-path
inspection. It did not rerun Nix checks. Recent referenced witnesses are:

- Designer `/330`: nspawn N=10 sandbox upgrade succeeded on Prometheus.
- Operator prior `/175`: 73 concept schema validation and in-process Spirit
  sandbox upgrade witnesses.
- Existing repo tests cover generated short headers, generated dispatch, box
  form, sema-engine commit replay, handover driver mocks, and Spirit upgrade
  socket behavior.

## Bottom Line

It is not accurate to say "the schema macro now drives all corresponding code."

It is accurate to say: "the first live slice exists in Spirit ordinary signal
generation and outbound header emission; the next required operator work is to
move receive dispatch and migration projection from tests/handwritten code onto
the schema-derived production path."
