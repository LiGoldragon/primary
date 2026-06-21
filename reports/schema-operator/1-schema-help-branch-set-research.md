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

## Likely Implementation

The feature should be generated, not hand-maintained in Spirit.

1. Add generated help/spec nouns in `schema-rust-next`, gated by the existing `nota-text` feature unless a separate gate is chosen.
2. Emit a `Help` input variant into root input enums and a generated help response variant into output roots.
3. Generate help recursively from schema structure until scalar leaves are reached. Scalar leaves terminate as structural terminal forms such as `(X String)` or `(Y Int)`.
4. Represent container forms explicitly: `(Z (Vec SomeThing))` keeps the container constructor and element type at the use site, while `SomeThing` remains recursively discoverable through `(Help SomeThing)`.
5. Represent the help response as typed data that can be serialized by `rkyv`; the CLI/text surface should render the structural form from that data.
6. Use Spirit as the pilot: regenerate `signal-spirit`, handle `Input::Help` in Spirit without touching SEMA, and add generated-contract, process-boundary, and Nix integration tests.
7. Keep `meta-signal-spirit` in the branch set so it can be regenerated or repinned if the generator changes public surfaces used by meta signals.

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
| spirit process_boundary | The CLI talks to a real daemon and returns generated help output parseable by `Output::FromStr`. |
| spirit production-copy handover | Extend the existing copied-SEMA handover style so Help works against a production database copy and proves the original database is untouched. |
| spirit nix_integration | Build from the pushed `schema-help` remotes in a Nix sandbox and run CLI/daemon help checks against an isolated state directory. |

The current Spirit test suite already has a production-copy pattern in `tests/process_boundary.rs` and ignored Nix integration tests in `tests/nix_integration.rs`; the new tests should extend those rather than inventing a parallel harness.

## Clarifications Needed

1. Should the feature gate reuse `nota-text`, or should this be a new gate such as `schema-help` layered on top of `nota-text`?
2. What is the exact query datatype: an optional typed `SymbolPath`, a custom `HelpQuery`, or a generated enum/path specific to each root?
3. What should the output root be named in Spirit: `Helped`, `HelpReported`, `HelpShown`, `SchemaHelpReported`, or another noun?
4. Should `(Help Version)` describe only the input form (`Version`) or the command/reply pairing (`Version -> VersionReported VersionReport`)?
5. For the top-level production-copy test, do you authorize copying the live `~/.local/state/spirit/spirit.sema` into the sandbox input, or should I use the existing production-like seeded database pattern only?
6. Should `nota-next` be in the epic branch set, or is the intended implementation limited to schema-next, schema-rust-next, the Spirit signal repos, and Spirit?
7. For container payloads such as `(Z (Vec SomeThing))`, should top-level help preserve `SomeThing` as a reference with recursive help available on demand, or should it inline-expand `SomeThing` in the first response until scalar leaves?

## Current Recommendation

Use `nota-text` as the first gate; make Help a generated root feature; carry the response as typed rkyv-serializable data; render structural NOTA-like help only at CLI/text edges; and pilot the shape in Spirit before broadening to mentci.

The one point I would not decide without psyche confirmation is whether production-copy testing may read the live Spirit database file. The existing copied-SEMA harness can prove the behavior without touching the live file, but the request sounds like it may want a real live-database copy as the top-level proof.
