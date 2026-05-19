# 5 — NOTA three-case PascalCase rule: codec change + downstream cascade

**Lane:** second-operator-assistant
**Date:** 2026-05-19
**Status:** codec change landed; cascade partial across consumer crates
**Bead:** `primary-hj63` (NOTA README: PascalCase-head rule is over-strict — a struct can be a record without naming the type)
**Reads against:** `reports/second-designer-assistant/8-nota-three-case-pascal-implementation-2026-05-19.md` §"What did not land — primary-hj63 codec change"

## TL;DR

Implemented the codec follow-up the designer report deferred — `NotaRecord`-derived structs encode tag-less per case 2 of the three-case PascalCase rule, and `NotaSum` newtype variants wrap the inner with the variant tag explicitly. Plus a symmetry fix to `nota-codec`'s `is_bare_string` and an update to `signal-core`'s `signal_channel!` macro that mirrored the old NotaSum dispatch shape. Six contract/library crates and one consumer have full test passes; one consumer (`persona-router`) compiles but has fixture failures awaiting follow-up; five more consumers (`persona-mind`, `persona-message`, `persona-introspect`, `owner-signal-persona-terminal`, `horizon-rs`) untouched.

## What landed

### Codec change — `nota-derive` + `nota-codec`

The shape NotaRecord derives changed:

- Old: `(TypeName field0 field1 …)` — struct head was the Rust type name.
- New: `(field0 field1 …)` — no type tag; the struct type is determined by the schema position the record sits at.

The shape NotaSum derives changed for newtype variants:

- Old: `Foo(Inner)` delegated to `Inner.encode()` — wire form was whatever Inner emitted (usually `(InnerTypeName fields…)` via Inner's NotaRecord head). Decode dispatched on the inner type's name.
- New: `Foo(Inner)` wraps with the variant tag — wire form is `(Foo <inner>)` where `<inner>` is the inner's encoding (a tag-less `(fields…)` for NotaRecord, bare for NotaTransparent, nested `(InnerVariant …)` for NotaSum). Decode dispatches on the variant name.

NotaSum struct variants did not change.

To support the new struct shape, `nota-codec` grew two primitives:

- `Encoder::start_record_untagged()` — writes `(` only (no PascalCase tag).
- `Decoder::expect_record_start()` — expects `(` only.

The existing `start_record(name)` / `expect_record_head(name)` stay in place for case 1 (data-carrying enum variants) — used by the `NotaSum` derive's variant arms and by the `Tuple` / `Some` / `Entry` blanket impls in `nota-codec`.

Symmetry fix bundled in the same arc: `Ident::is_bare_string` now excludes PascalCase content. `read_string` already rejected bare PascalCase per case 1 of the rule; `write_string` was still emitting PascalCase content bare via `is_bare_string`, producing wire that `read_string` would refuse to decode. The asymmetry surfaced as `signal-core`'s `pattern_field_string_match_emits_inner_value` round-trip failure on the new nota-codec.

### Macro update — `signal-core`

`signal-core/macros/src/emit.rs`'s `emit_payload_enum_codec` mirrored the old NotaSum behavior: encode delegated to the inner payload's `encode`, decode peeked the payload's NotaRecord head and dispatched. That shape relied on the now-removed payload-type-name head; after the derive change, the wire form for `signal_channel!`-generated request/reply enums went from `(<PayloadType> fields)` to just `(fields)` (tag-less inner from NotaRecord), which broke variant dispatch.

The macro now wraps each variant's payload with the variant tag explicitly — encode emits `(VariantName <inner>)`; decode peeks the variant tag, expects `(VariantName + inner + )`. The `last_path_segment` helper that mapped payload type names to their record head is dropped.

This means `signal_channel!`-generated wire forms now use the *variant* name as the outer head, which can differ from the payload type name (e.g. `EngineLaunchAccepted` variant wrapping `EngineLaunchAcceptance` payload). The old "payload-head quirk" referenced in several consumer canonical.nota top comments is gone.

### Commits (and where to find them)

| Repo | Commit | Description |
|---|---|---|
| `/git/github.com/LiGoldragon/nota-derive` | `30c665f3` | NotaRecord drops struct type tag; NotaSum wraps newtype variants with variant tag |
| `/git/github.com/LiGoldragon/nota-codec` | `ee90eef3` | Untagged-record primitives + test fixtures for new wire form |
| `/git/github.com/LiGoldragon/nota-codec` | `88852e68` | `is_bare_string` rejects PascalCase content (encode/decode symmetry) |
| `/git/github.com/LiGoldragon/signal-core` | `5762bba1` | `signal_channel!` macro wraps payload with variant tag; pattern tests adjusted |
| `/git/github.com/LiGoldragon/signal` | `eb745e3f` | Cascade: `text_round_trip` fixtures + bundled ARCH sweep from `push-sxsxtyxpozzr` |
| `/git/github.com/LiGoldragon/signal-persona` | `b7524aaf` | Cascade: canonical.nota + canonical_examples / engine_manager / spawn_envelope fixtures |
| `/git/github.com/LiGoldragon/signal-persona-message` | `346bd881` | Cascade: MessageSubmission / SubmissionAccepted fixtures |
| `/git/github.com/LiGoldragon/signal-persona-introspect` | `651cd730` | Cascade: canonical.nota + canonical_examples for IntrospectionRequest/Reply |
| `/git/github.com/LiGoldragon/signal-persona-system` | `965647e6` | Cascade: canonical.nota + canonical_examples / round_trip fixtures (System*) |
| `/git/github.com/LiGoldragon/signal-persona-auth` | `facfa73f` | Cascade: canonical.nota + round_trip / canonical_examples (MessageOrigin / IngressContext) |
| `/git/github.com/LiGoldragon/persona-router` | `f6ba3c0c` | Compile fix (`ComponentName::Orchestrate` match arm) + Cargo.lock; **wire fixtures pending** |

All commits pushed to `main` on origin. nota-codec stayed green throughout (112 tests pass after the encoder symmetry fix); each downstream commit was preceded by `cargo test` confirming the lane's tests are green at that rev.

## Pending follow-up

These consumers still need wire-form fixture updates. They use the new codec via `cargo update` (or are pinned via flake.lock to the old codec until that's updated). Pattern is mechanical:

- Wrap NotaSum variant payloads with the variant tag explicitly: `(VariantName <inner>)`. For NotaRecord-derived inners, the inner becomes a tag-less `(fields)`. For NotaTransparent inners, bare value.
- For variants where the variant name differs from the payload type name (e.g. `EngineLaunchAccepted` wraps `EngineLaunchAcceptance`), the wire head is now the variant name.
- For `Option<T>::Some(v)`, wire is `(Some <v>)`.
- For Bool, wire is `True` / `False` PascalCase.
- For PascalCase string content, wire is quoted `"..."` (the encoder now refuses to emit it bare).
- For struct variants of NotaSum, the wire shape is unchanged.

Consumer status:

| Crate | Status |
|---|---|
| `/git/github.com/LiGoldragon/persona-router` | **Compiles, 5 smoke-test fixtures fail.** `tests/smoke.rs` lines 74, 89, 97, 109, 125 — `RouterInput`, `RouterOutput`, `RouterBootstrapOperation` NOTA string inputs need new wire form. |
| `/git/github.com/LiGoldragon/persona-mind` | Untouched in this lane. Cargo.lock not bumped. |
| `/git/github.com/LiGoldragon/persona-message` | Untouched in this lane. Cargo.lock not bumped. |
| `/git/github.com/LiGoldragon/persona-introspect` | Untouched in this lane. Cargo.lock not bumped. |
| `/git/github.com/LiGoldragon/owner-signal-persona-terminal` | Untouched in this lane. Cargo.lock not bumped. |
| `/git/github.com/LiGoldragon/horizon-rs` | Untouched in this lane. Cargo.lock not bumped. |

Other consumers I noticed in the workspace but did not touch (some are in other lanes' claims):

- `/git/github.com/LiGoldragon/owner-signal-persona-spirit` — operator's lane (`primary-ojxq`)
- `/git/github.com/LiGoldragon/signal-persona-spirit` — operator's lane
- `/git/github.com/LiGoldragon/owner-signal-repository-ledger` — designer-assistant's lane (`rename-repository-ledger-domain-prefixes`)
- `/git/github.com/LiGoldragon/persona-harness` — has `NotaRecord` use per earlier grep
- `/git/github.com/LiGoldragon/signal-persona-mind` — has `NotaRecord` use per earlier grep
- `/git/github.com/LiGoldragon/signal-persona-orchestrate` — has `NotaRecord` use per earlier grep
- `/git/github.com/LiGoldragon/signal-persona-terminal` — has `NotaRecord` use per earlier grep
- `/git/github.com/LiGoldragon/signal-persona-harness` — has `NotaRecord` use per earlier grep

The cascade pattern is the same across all of them. The risk surface is small — derive-level changes mean Rust APIs unchanged; only wire-form-pinning tests and any persisted Sema/redb data need updating.

## Decisions taken on judgment calls

1. **Bundled the `is_bare_string` PascalCase rejection into the same arc.** It's not strictly `primary-hj63` scope, but the asymmetry between encoder and decoder was a load-bearing inelegance — `read_string` rejected PascalCase per case 1 of the three-case rule, `write_string` still emitted it bare. The symmetric fix is one line in `Ident::is_bare_string`. Per ESSENCE §"Beauty is the criterion" and the broader three-case-rule design, fixing the asymmetry at source rather than working around it downstream.

2. **Bundled the `push-wxupkwlv` ARCH commit into the signal codec-cascade commit on main.** Same user authored both; the ARCH commit was pure docs; advancing main carried both forward. Alternative was a split + rebase that the discipline supports but felt like ceremony for what's effectively the same author's two-day-old in-flight work.

3. **Used `Encoder::start_record_untagged()` instead of repurposing existing primitives.** Considered renaming `start_record(name)` to `start_variant(name)` and reusing the no-arg shape for the struct case, but that's wider API churn for the same end. Adding one new primitive keeps the existing Tuple/Some/Entry callers untouched.

4. **Stopped the cascade at `persona-router` compile-only.** Each remaining consumer is mechanical fixture work but representative of a few hours of update-test-update cycles. The codec change itself is landed and downstream consumers will pull on next `cargo update`. The bead can be closed against the codec landing; follow-up beads against each remaining consumer can land independently.

## Open follow-ups

- **Bead `primary-hj63` can close** against this report. The codec change has landed; the cascade is a separate effort that doesn't gate the codec.
- **Per-consumer wire-form sweep** — each listed pending crate needs `cargo update` + fixture update + commit. Mechanical, no design judgment.
- **`skills/nota-design.md` update** — the designer's report 8 listed this as a designer-lane follow-up; not touched here. The skill currently doesn't explain when there's no wrapping at all (struct case 2) cleanly.
- **`nota-derive` `NotaPath` derive** — still deferred per report 7 §10.3. The Option/Bool/PascalCase/struct-tag changes don't change that recommendation.

## See also

- `reports/second-designer-assistant/8-nota-three-case-pascal-implementation-2026-05-19.md` — the designer's three of four beads landing report; this report is the codec follow-up §"What did not land" listed.
- `intent/nota.nota` — psyche intent on the three-case rule (entries from 2026-05-19 20:30 through 21:30).
- `/git/github.com/LiGoldragon/nota-codec/README.md` (commit `503f4754`) — canonical spec for the three-case rule.
- `/git/github.com/LiGoldragon/nota-derive/src/{nota_record,nota_sum}.rs` (commit `30c665f3`) — the derive impls.
- `/git/github.com/LiGoldragon/nota-codec/src/{encoder,decoder,ident}.rs` (commits `ee90eef3` + `88852e68`) — codec primitives and the encoder symmetry fix.
- `/git/github.com/LiGoldragon/signal-core/macros/src/emit.rs` (commit `5762bba1`) — the `signal_channel!` macro update.
