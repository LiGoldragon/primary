# Schema Help Deploy Readiness

Role: schema-operator
Date: 2026-06-21

## Verdict

The `schema-help` branch set is ready for Spirit deployment from the schema-operator side on the tested platform.

The deploy gate now proves the client-side Help boundary directly:

- The binary-only daemon dependency surface excludes both `nota-next` and `schema-next`.
- Help is generated from decoded real schema data, not a hand-maintained list.
- The deployed Help model covers the decoded `signal.schema` roots and declarations plus imported `domain.schema` declarations.
- A live production database copy remains byte-identical after a batch of Help calls with no daemon running.
- The candidate daemon can still read the copied live database afterward.
- Refreshed Nix integration tests and the full refreshed flake check pass against pushed branch refs.

## Branch Tips

| Repository | `schema-help` tip | Note |
|---|---:|---|
| `schema-next` | `ece5c380` | source-AST accessors for runtime projection |
| `schema-rust-next` | `cb38435e` | client-side Help intent documentation |
| `signal-spirit` | `cbe60cf0` | deployed-schema Help coverage, domain schema merge, compact NOTA codec round-trip |
| `meta-signal-spirit` | `13c53dfa` | typed Help signal lock refresh |
| `spirit` | `9db5463c` | deploy-gate tests, refreshed Nix branch refs, repinned `signal-spirit` |

## Gaps Fixed

| Gap | Fix |
|---|---|
| Existing default dependency test only excluded `nota-next`. | `tests/dependency_surface.rs` now also rejects `schema-next` in the binary-only runtime tree. |
| Help coverage was a golden subset. | `signal-spirit` now decodes `SIGNAL_SCHEMA_SOURCE` and `DOMAIN_SCHEMA_SOURCE` with `schema_next::SchemaSource::from_schema_text`, derives all root/declaration targets, and requires each to render. |
| Imported domain names rendered as import references only. | `HelpModel::from_signal_schema_source()` now merges decoded `domain.schema` namespace declarations into the client-side model. |
| Inline enum payloads could dump nested schema text at the parent. | Inline enum payloads now render as named references, so `(Help Domain)` names `Health`, `Food`, etc.; `(Help Health)` is the next navigation step. |
| Production DB proof was not specific to client-side Help. | The ignored live-copy test now runs Help calls before any daemon exists, asserts the copied `.sema` bytes are unchanged, then starts the daemon and verifies `Lookup 6th4` and `Marker`. |
| Nix helper scripts could reuse stale mutable branch refs. | `scripts/check-local-schema-stack` and `scripts/run-nix-integration-tests` now pass `--refresh`. |
| Nix stack scripts did not override all pilot repos. | Both scripts now override `signal-spirit-source` and `meta-signal-spirit-source` as well as schema repos. |
| Help text was NOTA-shaped but not a decoding codec. | `HelpResponse` now implements custom compact `NotaEncode` / `NotaDecode` and `NotaDocumentEncode` / `NotaDocumentDecode`, so `(Record { Entry Justification })` decodes back into the typed help tree instead of being only a `Display` string. |
| A derived NOTA codec would leak internal variants. | The implementation deliberately uses the schema-declaration surface as the codec grammar: brace means struct, square bracket means enumeration, empty means unit, and atom/application means reference. It does not emit tagged internals such as `(Record (Struct [Entry Justification]))`. |

The Stream/Family typed-frame follow-up remains non-blocking. `IntentEventStream` is included in the decoded full-schema render gate and renders successfully; it still uses the existing text fallback internally.

## Dual Codec Closure

The Help value is now a true dual-codec contract value on the branch set:

- rkyv: `HelpModel`, `HelpResponse`, `HelpBody`, and `HelpTypeExpression` continue to archive and round-trip as typed Rust values.
- NOTA text: `HelpResponse` and `HelpEntry` encode through the compact help grammar and decode through the inverse delimiter-based grammar.
- Top-level `(Help)` is a multi-root document body and round-trips through `NotaDocumentEncode` / `NotaDocumentDecode`.
- Named `(Help X)` responses round-trip as a single `HelpResponse` block through `NotaEncode` / `NotaDecode`.
- Invisible provenance was removed from `HelpEntry`; the tree now contains only the value that the compact NOTA form actually carries.

The new codec test pins the exact compact syntax for `Entry` and `IntentEventStream`, and also round-trips top-level Help as a document body. That directly closes schema-designer's report 5 spec without changing the user-facing Help output.

## Tests Passed

| Scope | Command | Result |
|---|---|---|
| `signal-spirit` default daemon-side contract | `cargo test` | 13 tests passed; Help text codec remains feature-gated |
| `signal-spirit` full text-client contract | `cargo test --features nota-text -- --nocapture` | 23 tests passed, including `generated_help_response_round_trips_through_nota_codec` |
| `signal-spirit` text-client lint | `cargo clippy --features nota-text --all-targets -- -D warnings` | passed |
| Spirit text-client and regular integration suite | `cargo test --features nota-text -- --nocapture` | all non-ignored tests passed after repinning `signal-spirit` to `cbe60cf0` |
| Live production DB Help side-effect proof | `cargo test --features nota-text --test process_boundary help_leaves_live_production_database_copy_byte_identical_in_sandbox -- --ignored --nocapture` | passed against `~/.local/state/spirit/spirit.sema` |
| Refreshed Nix integration | `SPIRIT_STACK_REF=main SPIRIT_TARGET_REF=schema-help SIGNAL_SPIRIT_REF=schema-help META_SIGNAL_SPIRIT_REF=schema-help SCHEMA_NEXT_REF=schema-help SCHEMA_RUST_NEXT_REF=schema-help scripts/run-nix-integration-tests --nocapture` | 10/10 ignored Nix integration tests passed |
| Refreshed full flake check | `SPIRIT_STACK_REF=main SPIRIT_TARGET_REF=schema-help SIGNAL_SPIRIT_REF=schema-help META_SIGNAL_SPIRIT_REF=schema-help SCHEMA_NEXT_REF=schema-help SCHEMA_RUST_NEXT_REF=schema-help scripts/check-local-schema-stack` | all 23 x86_64-linux checks passed |

The Nix integration run explicitly unpacked pushed refs `spirit` `9db5463caf54` and `signal-spirit` `cbe60cf00e5e`, then used the Nix-built package at `/nix/store/pz05jk67cjjr8phz3c83vsiv7ms0kbbi-spirit`.

The flake check reported `all checks passed!` and noted only the normal omitted incompatible systems: `aarch64-darwin`, `aarch64-linux`, and `x86_64-darwin`.

## Deployment Readiness

This is deploy-ready for the Spirit x86_64-linux path tested here. The remaining integration work is branch-set landing/rebase into the owned main flow, not a feature correctness blocker.

The important operational property is now proven by tests: Help resolves locally in the CLI/text-client layer from typed decoded schema data, and the daemon/database boundary is untouched.
