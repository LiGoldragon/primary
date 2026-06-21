# Schema Help Branch Set Research

Role: schema-operator
Date: 2026-06-21

## Branch Set

I created and pushed `schema-help` branches under `~/wt` for the pilot stack:

| Repository | Worktree | Branch base |
|---|---|---|
| schema-next | `/home/li/wt/github.com/LiGoldragon/schema-next/schema-help` | `schema-next: one lowering engine + macro-registry pre-expansion pass` |
| schema-rust-next | `/home/li/wt/github.com/LiGoldragon/schema-rust-next/schema-help` | `schema-rust-next: consume the {| |} impl catalog + typed malformed-name errors` |
| signal-spirit | `/home/li/wt/github.com/LiGoldragon/signal-spirit/schema-help` | `signal-spirit: bump to 0.8.0 for referent validation` |
| meta-signal-spirit | `/home/li/wt/github.com/LiGoldragon/meta-signal-spirit/schema-help` | `meta-signal-spirit: regenerate src/schema/meta_signal.rs against schema-rust-next 90d853c3; repin signal-spirit to fresh main` |
| spirit | `/home/li/wt/github.com/LiGoldragon/spirit/schema-help` | `spirit: bump to 0.16.0 for referent enforcement` |

All five worktrees are clean and have remote `schema-help` bookmarks. The schema-operator lane currently holds the five feature-worktree paths, not the canonical `/git` checkouts.

Current branch tips:

| Repository | `schema-help` tip |
|---|---|
| schema-next | `ece5c380` — exposes source shapes for help projection |
| schema-rust-next | `cb38435e` — pins client-side schema Help intent |
| signal-spirit | `974d4a13` — types schema Help responses |
| meta-signal-spirit | `13c53dfa` — refreshes typed Help signal lock |
| spirit | `fe7fa603` — refreshes mutable refs in Nix integration builds |

## Existing Contract Surface

Spirit's working signal currently has no help root. Its top-level roots are in `signal-spirit/schema/signal.schema`:

| Surface | Relevant current shape |
|---|---|
| input roots | `[State Record Propose Clarify Supersede Retire ResolveClarification Observe PublicTextSearch PublicRecords PrivateRecords Lookup Count Remove ChangeCertainty BumpImportance ChangeRecord RegisterReferent LookupStash CollectRemovalCandidates Tap Untap (SubscribeIntent SubscribeIntent opens IntentEventStream) Version Marker]` |
| output roots | `[RecordAccepted Proposed Clarified Superseded Retired ClarificationResolved GuardianRejected ReferentGuardianRejected RecordsObserved RecordsStashed RecordFound RecordsCounted RecordRemoved CertaintyChanged ImportanceBumped RecordChanged ReferentRegistered RemovalCandidatesCollected ObservationTapped ObservationUntapped SubscriptionStarted VersionReported MarkerReported (Event IntentEvent) Error Rejected]` |
| example one-way command | `Version` input to `VersionReported VersionReport` |
| example payload output | `RecordAccepted RecordIdentifier` |
| example structural record | `Record { Entry Justification }` |

The generated Rust already exposes the important surfaces for a pilot:

| Repository | Existing hook |
|---|---|
| schema-next | `Root`, `RootApplication`, `Schema::input`, `Schema::output`, `Schema::root_variant_path`, `Schema::symbol_path_position`, and `SymbolPath` already describe schema locations as typed values. |
| schema-rust-next | `RustEmissionOptions::feature_gated_nota("nota-text")`, `RustRenderContext::nota_feature_gate`, `NotaRootEnumStringSupportTokens`, `RustEnumTokens::root`, route enums, and `SignalFrameImplTokens` centralize generated root behavior. |
| signal-spirit | `Version`, `VersionReported`, `Record`, `RecordAccepted`, and generated route/header support provide a small known-good model for adding a text-client command. |
| spirit | `Input::Version` is handled in `src/nexus.rs`, accepted by the daemon boundary in `src/daemon.rs`, parsed from CLI NOTA, and verified through generated NOTA round-trip/process tests. |

## Implemented POC

This pass uses the schema-designer runtime-projection recommendation rather than generating a pre-baked table in `schema-rust-next`. The psyche clarified the one disputed boundary after the designer comparison: none of this is in the daemon; Help is CLI/client logic with an actual typed Rust help data tree.

Implemented shape:

1. `schema-next` exposes read-only source-AST accessors needed by downstream projection: root variant payload source, source declaration text, source field value text, and source reference text.
2. `signal-spirit` adds a `nota-text`-gated `help` module. It parses `SIGNAL_SCHEMA_SOURCE` with `schema_next::SchemaSource::from_schema_text`, builds a rkyv-serializable `HelpModel`, recognizes `Help` / `(Help)` / `(Help Name)`, and resolves each request to a typed `HelpResponse { HelpEntries [HelpEntry { origin name body }] }` tree before display.
3. `meta-signal-spirit` is repinned to the same `signal-spirit/schema-help` branch so Spirit resolves one `signal-spirit` package.
4. `spirit` repins the branch set and intercepts Help in `src/bin/spirit.rs` before parsing generated `Input` or connecting to the daemon socket.
5. Help is therefore a CLI/text-client surface for this POC. It never becomes a daemon request, does not add `Input::Help` / `Output::HelpReported` roots, and does not touch SEMA.

Real rendered examples from the tests:

| Request | Render |
|---|---|
| `(Help Record)` | `(Record { Entry Justification })` |
| `(Help Entry)` | `(Entry { Domains Kind Description Certainty Importance Privacy Referents })` |
| `(Help Domains)` | `(Domains (Vec Domain))` |
| `(Help Description)` | `(Description String)` |
| `(Help VerbatimQuote)` | `(VerbatimQuote { QuoteText OptionalAntecedent })` |

The container spelling intentionally echoes the pinned source text: Spirit currently writes `(Vec Domain)`, and the renderer preserves that use-site source form rather than normalizing it to another spelling.

## Implementation Direction

The feature should be generated, not hand-maintained in Spirit.

1. Keep the first production path on `nota-text`; binary-only daemon builds omit the Help module and still carry no `nota-next` dependency.
2. Treat Help recursion as navigation: each `(Help X)` renders one structural level and names child types. The renderer does not transitive-dump nested definitions.
3. Preserve schema-emitted nouns and newtyped domain values. Parent shapes do not erase ordinary fields to primitive scalars.
4. Scalar backing primitives appear only at scalar-backed leaf boundaries, such as `(Description String)` or `(CommitSequence Integer)`.
5. Represent container forms explicitly at the use site, for example `(Domains (Vec Domain))`; the element type remains a named reference.
6. Keep both `HelpModel` and `HelpResponse` rkyv-serializable even when the model is built at CLI runtime from embedded schema source.
7. Generalize the runtime-projection accessor from `signal-spirit` into generator-emitted contract support once the Spirit pilot is accepted.

The lowest-friction first proof is:

| Input | Expected structural output intent |
|---|---|
| `(Help)` | top-level input and output possibilities, structurally grouped |
| `(Help Record)` | `Record { Entry Justification }` |
| `(Help RecordAccepted)` | `RecordAccepted RecordIdentifier` |
| `(Help Version)` | `Version` or `Version -> VersionReported VersionReport`, depending on whether command/reply pairing is part of help |

## Test Plan

| Layer | Test |
|---|---|
| schema-rust-next unit tests | Generator emits help/spec data only behind the configured feature gate; binary-only emission has no NOTA/help text dependency. |
| signal-spirit generated tests | `Help` roots, payload constructors, route enums, short headers, rkyv frame encode/decode, `FromStr`, and `Display` round-trip. |
| spirit generated_signal_plane | `(Help)`, `(Help Record)`, and `(Help RecordAccepted)` parse into generated `Input` and display generated `Output`. |
| spirit process_boundary | The CLI renders Help without a daemon socket, proving Help is client-side and never crosses transport. |
| spirit production-copy handover | Not applicable to Help itself after the client-side decision: Help does not open the daemon socket or database. Existing production-copy SEMA tests still cover daemon/database behavior for real signal operations. |
| spirit nix_integration | Added and passed a Nix-built CLI Help test against pushed `schema-help` refs with a deliberately missing daemon socket. |

The current Spirit test suite already has a production-copy pattern in `tests/process_boundary.rs` and ignored Nix integration tests in `tests/nix_integration.rs`; the new tests should extend those rather than inventing a parallel harness.

Tests run in this pass:

| Repository | Command |
|---|---|
| schema-next | `cargo test schema_source_exposes_one_level_help_projection_inputs -- --nocapture` |
| signal-spirit | `cargo test --features nota-text generated_help -- --nocapture` |
| signal-spirit | `cargo test --no-default-features default_dependency_tree_does_not_pull_text_or_legacy_signal_crates -- --nocapture` |
| meta-signal-spirit | `cargo test --features nota-text` |
| spirit | `cargo test --features nota-text --test process_boundary cli_renders_help_without_daemon_transport -- --nocapture` |
| spirit | `cargo test --features nota-text --no-run` |
| spirit | `cargo test --no-default-features --test dependency_surface binary_only_surface_has_no_nota_next_runtime_dependency -- --nocapture` |
| spirit | `SPIRIT_STACK_REF=main SPIRIT_TARGET_REF=schema-help SIGNAL_SPIRIT_REF=schema-help META_SIGNAL_SPIRIT_REF=schema-help SCHEMA_NEXT_REF=schema-help SCHEMA_RUST_NEXT_REF=schema-help cargo test --features nota-text --test nix_integration nix_built_spirit_cli_renders_help_without_daemon_transport -- --ignored --nocapture` |

## Clarifications Still Needed

1. Should the next pass lift the hand-written `signal-spirit::help` module into generated contract support from `schema-rust-next`, or is the runtime-projection POC acceptable as the first branch artifact?
2. Should `(Help Version)` describe only the input form (`Version`) or the command/reply relation (`Version -> VersionReported VersionReport`)?
3. Should Help query names stay as a single local type/root name for the pilot, or move immediately to `SymbolPath`?
4. Should `nota-next` join the epic branch set now, or stay out until a parser/codec change is actually needed?

## Current Recommendation

Use `nota-text` as the first gate; keep Help client-side for the pilot; carry the response as typed rkyv-serializable data; render structural NOTA-like help only at CLI/text edges; and lift the contract-local `signal-spirit` module into generated contract support after the Spirit pilot is reviewed.

Do not force a production database copy into the Help proof. The clarified client-side boundary makes database state irrelevant to Help; the stronger proof is the one now in `nix_integration`: the Nix-built CLI returns `(Help Entry)` successfully while pointed at a missing socket.
