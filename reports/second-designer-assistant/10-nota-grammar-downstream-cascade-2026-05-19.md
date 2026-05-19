# 10 — NOTA grammar changes: downstream-rewrite cascade for consumers

**Lane:** second-designer-assistant
**Date:** 2026-05-19
**Audience:** any agent picking up the consumer-crate sweep (the psyche removed role-labels-on-beads on 2026-05-19 21:45, so this isn't operator-specific)
**Status:** four grammar changes are settled in `nota-codec` main; this report is the recipe for cascading them through the forty consumer crates that depend on the codec

## What changed in the codec

Four NOTA grammar changes settled in `nota-codec` over 2026-05-18 and 2026-05-19. The first three were landed in commit `503f4754` (Bool, Option, PascalCase-at-String); the fourth — the headless-struct change for `NotaRecord` and the matching new encoder / decoder methods (`start_record_untagged` / `expect_record_start`) — landed in commits `88852e6897c1` and `57747a3a4c48` on the same `LiGoldragon/nota-codec` main branch after my report 8 deferred it. The codec test suite (112 tests) is green on all four. Every consumer of `nota-codec` will see at least one wire-form change. The changes are:

The **Bool change**: lowercase `true` / `false` keyword tokens are gone. The lexer no longer dispatches on them. A `Bool` value encodes as the PascalCase ident `True` or `False` — a normal two-variant enum, case 3 of the PascalCase rule (a bare PascalCase ident is a non-data-carrying unit variant). Any wire fixture containing bare `true` or `false` at a `Bool` field position needs `True` / `False`. Strings whose content happens to be `"true"` / `"false"` were previously rejected at encode time and quoted at decode time; they now encode and decode as ordinary camelCase strings (the reserved-literal list is reduced to just `None`).

The **Option change**: a present `Option<T>` now wraps as `(Some inner)` — the standard data-carrying variant shape (case 1 of the rule). The Some-less carve-out is gone. Absent stays bare `None` (case 3). Any wire fixture where a present `Option<u64>` was written as `5` is now `(Some 5)`; where a present `Option<String>` was written bare as `label` is now `(Some label)`. The blanket impl in `nota-codec/src/traits.rs` does the wrapping; consumers don't write the wrap themselves, but their test fixtures and persisted data carry the old form.

The **PascalCase-at-String change**: a bare PascalCase token at any `String` schema position returns `Error::PascalCaseAtStringPosition` at decode time. PascalCase is variant territory only. The bare-camelCase and bare-kebab-case carve-outs are unchanged. Wire fixtures like `(Container Foo)` for a `Container { label: String }` shape are now decode errors; rewrite to `(Container "Foo")` (quoted) or `(Container foo)` (lowercased) or `(Container foo-bar)` (kebab). The encoder side already quoted PascalCase content; the new error catches the decoder side.

The **headless-struct change**: a struct (`NotaRecord`-derived type) emits no PascalCase head. Its wire is `(field1 field2 …)` with no leading type name. The schema position determines the type. NotaSum's data-carrying enum variants still wrap with the variant name (`(VariantName field1 …)`). Newtype-wrapped types that use explicit start-record naming — `(Some inner)`, `(Entry key value)` for `BTreeMap`/`HashMap`, `(Tuple a b)` for tuples — keep their tag because their wrapping name is a variant tag, not a struct head. The cascade is biggest here: every `(StructName field1 field2 …)` form that's not a variant tag becomes `(field1 field2 …)`.

## The cascade scope — forty consumer crates

Forty crates depend on `nota-codec` per `Cargo.toml` (counted by `grep -l nota-codec Cargo.toml` across `/git/github.com/LiGoldragon/`). The set spans the persona stack (`persona`, `persona-mind`, `persona-router`, `persona-message`, `persona-terminal`, `persona-system`, `persona-introspect`, `persona-harness`, `persona-spirit`), the signal contract crates (`signal-core`, `signal-criome`, `signal-persona`, `signal-persona-auth`, `signal-persona-mind`, `signal-persona-message`, `signal-persona-router`, `signal-persona-spirit`, `signal-persona-terminal`, `signal-forge`, etc.), the owner-signal contracts (`owner-signal-persona-orchestrate`, `owner-signal-persona-spirit`, `owner-signal-persona-terminal`, `owner-signal-repository-ledger`), and the application crates (`chroma`, `chronos`, `clavifaber`, `criome`, `horizon-rs`, `lojix-archive`, `lojix-cli`, `nexus`, `nota-config`, `repository-ledger`, `prism`, `forge`, `mentci-egui`, `mentci-lib`, `mentci-tools`). Some are signal-contract crates that only define types and tests; some are daemons with persisted Sema/redb data that may carry old wire forms; some are CLIs that don't persist anything.

Each consumer falls into one of three sweep classes.

The **signal-contract and library crates** (the `signal-*`, `owner-signal-*`, and `nota-*` crates) carry types + tests + ARCHITECTURE.md examples. Sweep needed: rebuild tests; update any wire-form examples in `ARCHITECTURE.md` and per-repo `skills.md` and `INTENT.md` if they exist; rerun `nix flake check`. No persisted data.

The **daemon and CLI crates** (the `persona-*` daemons, `criome`, `repository-ledger`, `clavifaber`, etc.) carry tests + ARCHITECTURE + may persist Sema/redb data with old wire forms. Sweep needed: rebuild tests; data migration if any persisted state lives across the codec bump (`persona-mind`'s memory graph, `signal-criome`'s authorisation state, the repository-ledger's spool, etc. are candidate migration targets); regenerate any fixture files; rerun the integration witnesses. The persisted-data piece is the load-bearing one — a daemon that boots with old-format records will fail to decode them.

The **application and UI crates** (`mentci-*`, `prism`, `forge`, `chroma`, `chronos`, `horizon-rs`) mostly consume the codec for config or wire. Sweep needed: rebuild tests; update any committed fixture files; possibly migrate `*.nota` config in production (e.g., `criomos-*` config files if they pin certain wire shapes).

## The sweep recipe per crate

For each consumer, the discipline is the same. Open the crate; run `cargo build` against the current `nota-codec` main (the four changes are already there). Compile errors will surface every place where `Token::Bool(_)` was pattern-matched (now gone) or where some other API moved. Then run `cargo test`. The test failures are the inventory of wire-form fixtures that need updating. For each failing test:

If the test contains a wire fixture string like `(SomeStruct field1 field2)` and `SomeStruct` is a `NotaRecord`-derived struct, drop the head: `(field1 field2)`. If it's a `NotaSum`-derived enum variant, keep the tag: `(Variant field1 field2)`. If it contains a bare `true` or `false` at a `Bool` field position, replace with `True` / `False`. If it contains a present `Option<T>` written as a bare inner value, wrap it: `(Some inner)`. If it contains bare PascalCase at a String position, quote or lowercase: `(Container Foo)` becomes `(Container "Foo")` or `(Container foo)`.

For daemons with persisted state, the cleanest move per `ESSENCE.md` §"Backward compatibility is not a constraint" is to wipe and re-create the state with the new codec — for development data, this is right; for any data that needs preserving, a one-time migration script reads old form, writes new form, and the daemon never sees the old form at boot. The persisted-state surfaces are listed per crate in their `ARCHITECTURE.md` Code-map sections; the most load-bearing ones are `persona-mind`'s mind graph (the typed-thought records), `signal-criome`'s authorisation state, `repository-ledger`'s spool, and `signal-forge`'s build-record store.

The `ARCHITECTURE.md` files in many of these repos contain illustrative wire forms in §"Wire shape" or §"Examples" sections. Those examples are documentation and need refreshing alongside the test fixtures. The pattern is the same: look for `(TypeName fieldX fieldY)` examples; the `TypeName` head goes away if `TypeName` is a struct; stays if `TypeName` is an enum variant.

## What the codec API looks like for the headless change

The new encoder methods, per `nota-codec/src/encoder.rs:160-194`: `start_record(name: &str)` writes `(Name` and is used by NotaSum's variant arms plus the blanket impls that wrap their payload in an explicit variant tag (`Some`, `Tuple`, `Entry`). `start_record_untagged()` writes just `(` and is used by the NotaRecord derive. `end_record()` writes `)` for either. The new decoder methods, per `nota-codec/src/decoder.rs:201,220,228`: `expect_record_head(expected: &'static str)` reads `(Name` and matches `expected`. `expect_record_start()` reads just `(`. `expect_record_end()` reads `)`. Consumer code that called the old `start_record(name)` API for a `NotaRecord`-derived type's encoding will keep compiling (the method still exists for variants) but will produce wrong wire output unless the derive was regenerated. Re-running `cargo build` in each consumer is what surfaces the staleness; the `NotaRecord` proc-macro picks up the new codec automatically.

## Open coordination — the Some / Entry / Tuple wrapper-with-tag question

A subtle point worth surfacing: the codec still uses `(Entry key value)` for map entries, `(Some inner)` for present options, and `(Tuple a b)` for tuples. These look like NotaRecord-derived structs but they retain a PascalCase tag, which under the strict three-case rule would say they're variants of some enum. Reading the blanket impls in `nota-codec/src/traits.rs`, the rationale is that `Entry`, `Some`, and `Tuple` are conceptually variant tags of the surrounding container type — `BTreeMap` is a sequence of `Entry` variants, `Option` is `Some` or `None`, a tuple is a `Tuple` variant carrying its positional values. Whether to formalise these as actual enum types or leave them as wrapper conventions is a designer-shaped question; for the cascade, treat them as variant tags that stay in the wire.

## Skills sweep status

I checked the workspace skills for stale NOTA wire-form references. The main NOTA-design skill `skills/nota-design.md` has been heavily updated by designer to teach the three-case PascalCase rule explicitly (§"Grammar facts that catch the recurring mistakes" names the three cases by number and references bead `primary-hj63`; §"Before you sketch any NOTA record" makes the variant-test the entry point). It also names the timestamp two-field shape inline (line 226-227). One stale line remains: line 181 says *"Tail-omission is decode-only compatibility, not canonical output"* — that's the old Option behaviour; with `(Some inner)` wrapping in place, there's no tail omission at all. Worth a tiny edit in a follow-up.

`skills/nota-schema-docs.md` is current — it teaches pseudo-NOTA documentation conventions (angle-bracket placeholders, `?` for optional, `|` for enum variants) and doesn't show real wire forms. No edit needed.

`skills/language-design.md` contains `(Foo a b c)` as a generic example in the discussion of newlines being insignificant. That example is benign — it doesn't claim `Foo` is a struct or a variant; it just illustrates token-based parsing. No edit needed.

`skills/contract-repo.md` shows signal-contract record-style examples. I didn't read it in detail this pass; recommend a follow-up sweep to verify it doesn't teach the old "(TypeName fields)" struct shape.

`skills/component-triad.md` and `skills/architecture-editor.md` may contain wire-form examples in their discussions of signal verbs and ARCH sections; these need a sweep too.

## See also

- `reports/second-designer-assistant/8-nota-three-case-pascal-implementation-2026-05-19.md` — the original implementation report (Bool / Option / PascalCase-at-String) with codec commit references.
- `reports/second-designer-assistant/9-intent-manifestation-audit-nota-2026-05-19.md` — the intent-manifestation audit that surfaced this report's gap.
- `skills/nota-design.md` — current canonical NOTA design discipline; teaches the three-case rule.
- `repos/nota/README.md` and `repos/nota/INTENT.md` — the spec and per-repo intent files (`LiGoldragon/nota` commits `0b0af8bb` and `ad14c35d`).
- `repos/nota-codec` main — the four codec changes (`503f4754` for the first three; `88852e6897c1` and `57747a3a4c48` for the headless-struct change).
