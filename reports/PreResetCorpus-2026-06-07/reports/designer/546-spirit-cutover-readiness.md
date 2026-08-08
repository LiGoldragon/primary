---
title: 546 — Spirit cutover readiness: new schema-derived spirit vs persona-spirit production
role: designer
variant: Audit
date: 2026-06-06
topics: [spirit, persona-spirit, cutover, production-readiness, migration, sema-engine, signal-frame, nota-next, schema-rust-next, triad-runtime, privacy, identity, archive, audit]
description: |
  Cutover-readiness audit (19 agents: dual feature-surface survey + real
  build/run/exercise of the new daemon + core-crate-usage/design audit →
  gap-synthesis → per-claim adversarial verification). Verdict: NOT READY —
  but the blocker is deliberate wire-shape divergence, not bugs. New spirit
  builds clean, 90/90 tests pass, clippy clean, ran live through all 12 working
  ops. Cutover is a MIGRATION not a swap: 4-field Record shorthand breaks, the
  Observe vocabulary diverges, privacy lost its typed access tier, recorded-time
  provenance/recency is absent, identity is u64-counter vs base36/random, and
  there is no deployment/migration/handover stack. Design audit: all five core
  crates used at their proper seams (no bypass; the 541 meta-frame risk resolved
  into emission); the worth-fixing design flaws are store-error swallowing (a
  failed sweep reported as empty success) and a single-variant meta root.
---

# 546 — Spirit cutover readiness: new schema-derived spirit vs persona-spirit production

## Verdict

NOT READY to replace production — but the blocker is wire-shape divergence, not bugs. The new schema-derived spirit (`spirit` repo, HEAD commit `bd04eac` — "thread ConnectionContext through handle_working_input", 0.1.0 pilot) is in excellent internal health and I ran the daemon for real: it builds clean, 90/90 tests pass, clippy is clean, and every working operation drove end-to-end over a live socket. The single biggest blocker to cutover is that the new NOTA surface is deliberately not compatible with deployed Spirit (persona-spirit 0.5.0, the rev pinned in `CriomOS-home/flake.lock`): a drop-in swap breaks documented callers at the highest-traffic op (Record) plus the whole Observe vocabulary, and there is no migration binary, no deployment module, and no identity bridge. Per the repo's own `INTENT.md` this is explicitly "not production Spirit; the public pilot repo." Adoption is a migration project, not a swap. A great deal actually ran: a real `spirit-daemon` was spawned on a temp socket + temp `.sema` + owner-only meta socket and exercised through all 12 working ops plus owner Configure.

## What was tested (build + run)

Build/test/lint/freshness were all run against `spirit` HEAD `bd04eac` (the pilot tip on `main`):

- **Build:** PASS. `cargo build --all-features` succeeds cold and incremental against git deps sema-engine, signal-frame, nota-next, schema-rust-next (build-dep), triad-runtime v0.2.1, schema-next (dev-dep). Both bins build (`spirit` 24 MB, `spirit-daemon` 27 MB).
- **Tests:** PASS — 90 tests, 0 failures across 15 binaries + 1 doc-test. Notable suites: `process_boundary` 8/8 (real daemon spawn over rkyv socket, including durable restart + candidate handover), `runtime_triad` 26/26, `generated_signal_plane` 13/13, `meta_configure` 4/4, `observer_tap` 3/3, `collect_removal_candidates` 2/2. The 9 `nix_integration` tests are gated (ignored without nix).
- **Clippy:** CLEAN. `cargo clippy --all-features -- -D warnings` exits 0.
- **Freshness guard:** PASS. `build.rs` runs `GenerationDriver::generate().write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")`; with the env var unset it runs in check mode and a plain build leaves a clean tree, so checked-in `src/schema/*.rs` is fresh against `schema/*.schema`. The deeper `scripts/check-local-schema-stack` (nix flake check over local dep overrides) was NOT exercised — it needs the full local schema-stack checkout set.

### Per-operation run outcomes

A real daemon was spawned and driven through the CLI over a live socket. "Production op" rows are deployed 0.5.x shapes tested against the new daemon to probe compatibility.

| Operation | Outcome |
|---|---|
| Record (single-topic, 5-field) | works |
| Record (multi-topic + non-Zero privacy) | works |
| Record (4-field shorthand, no privacy) | errors — "expected Entry to hold 5 root objects, found 4" |
| Observe (new flat Query → Stash slim reply) | works |
| Observe (production `(Records ...)` / `(RecordIdentifiers ...)` wrappers) | errors — "expected Query to hold 3 root objects, found 2" |
| LookupStash (resolve Observe handle) | works |
| Lookup (by identifier) | works |
| Count | works |
| ChangeCertainty (identifier-stable) | works |
| State (classify-and-write) | works |
| Remove (+ gone-after / nonexistent / empty-topic reject) | works |
| CollectRemovalCandidates (new bare-RecordQuery shape) | works |
| CollectRemovalCandidates (production `(ArchiveDatabase ...)` / `(Print ...)` shape) | errors — "expected Query to hold 3 root objects, found 2" |
| Configure (owner meta socket, set archive target) | works (required a library MetaSignalTransport client; the CLI cannot reach it) |
| Tap / Untap (observer log replay) | works |
| SubscribeIntent (live streaming push) | works — separate subscriber received pushed `(Event (IntentRecorded ...))` |
| RecordIdentifiers / Topics observation (production ops) | unimplemented — no such variant in the new schema |
| Daemon durability + restart + candidate handover | works (8/8 `process_boundary`) |

Concrete reference files: `/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs` (CLI, signal::Input only), `/git/github.com/LiGoldragon/spirit/src/schema/signal.rs` (Input enum, 12 working ops), `/git/github.com/LiGoldragon/spirit/src/schema/meta_signal.rs` (ArchiveDatabaseTarget), `/git/github.com/LiGoldragon/spirit/src/config.rs` (rkyv daemon Configuration), `/git/github.com/LiGoldragon/spirit/build.rs:48` (freshness guard), `/git/github.com/LiGoldragon/spirit/tests/process_boundary.rs` (real-spawn pattern).

## What is missing for production parity

Each gap below survived independent verification (`standsUp=true`). Ordered blocker → major → minor. The single State-classifier gap was REFUTED and is moved to the last section.

### Major

**Record 4-field shorthand backward compatibility.** Production: `Entry::decode` reads privacy only if not at record-end, `Entry::open` defaults privacy=Zero, so `(Record ([workspace] Decision [summary] Maximum))` is valid (confirmed live against deployed `spirit` v0.5.2 → `(RecordAccepted [1mhv])`). New spirit: `Entry` requires all 5 fields; the nota-next derive is exact-count and rejects the 4-field form with "expected Entry to hold 5 root objects, found 4". This is a hard incompatibility on the single highest-traffic op — every existing caller and the documented capture idiom (`skills/spirit-cli.md:102,178-179,185`) uses the 4-field form. Easy to re-add (optional-trailing privacy in the decoder); currently a clean break. Why it matters for cutover: a drop-in swap breaks record capture for every client on day one. Evidence: `src/schema/signal.rs:361-367`; nota-next derive exact-count check.

**Privacy two-tier ACCESS-CONTROL split (PrivateRecords / PrivateRecordIdentifiers).** Production enforces privacy BY TYPE: `PublicRecordQuery` carries no privacy field, `into_record_query()` always injects `Exact(Zero)`, and `decode` actively rejects an elevated privacy selection ("public record queries cannot carry elevated privacy", lib.rs:904-913). Reading non-Zero-privacy records REQUIRES the distinct `PrivateRecords`/`PrivateRecordIdentifiers` variants. New spirit: a single `Observe` op whose `Query` carries an explicit `privacy_selection` for ALL callers; default is `Exact(Zero)` but any caller can pass `(AtLeast High)` on the ordinary working socket. Privacy is a filter predicate, not an access-control tier; no decode-time rejection, no private-read op split. The SO_PEERCRED `ConnectionContext` is now threaded through `handle_working_input` but currently ignored — the hook exists, unwired. Why it matters: the workspace privacy discipline ("private information is closed by default") is load-bearing; losing the typed gate is a real capability regression, not cosmetic. Evidence: `schema/signal.schema:16,105,78`; `src/store.rs:517-530`; `src/daemon.rs:118-124`.

**Recorded-time provenance + qualitative recency selection.** Production: a daemon clock actor stamps date+time on every record (`StampedEntry`); WithProvenance returns `RecordProvenance=[RecordSummary Date Time]`; `RecordedTimeSelection` exposes Shallow=5 / Recent=15 / Deep=30 / VeryDeep=100 depths plus Since/Until/Between ranges. New spirit: NO recorded-time field anywhere — not on `Entry` (`src/schema/signal.rs:361`), not in the store, not in any reply; repo-wide grep for clock/SystemTime/chrono/StampedEntry returned zero hits. No clock stamping, no provenance mode, no recency selector. `DatabaseMarker.commit_sequence` is a monotonic ordering proxy but is not a query selector and not wall-clock. Why it matters: "query recent Spirit records" is a recurring workspace-discipline pattern; an entire production query class would return un-time-filtered results.

**Production identity machinery (base36 codes, friendly display, long-id decode, collision-rejecting random minting).** Production: `RecordIdentifier=[u8;12]` (96-bit), minted as collision-rejected random bytes, displayed as base36 (4-char minimum), `from_code` decodes any ≥4-char base36 string for long-id compat. New spirit: `RecordIdentifier=u64` allocated by sema-engine's monotonic counter (`assert_identified().identifier().value()`), rendered as a bare integer; no base36, no friendly display, no sidecar mapping, no long-id compat, no collision logic. Why it matters: 96-bit base36-keyed production records cannot be addressed by a u64 counter — carrying data forward needs a re-keying migration; sequential u64s also leak record count/ordering the random scheme deliberately hid. (Caveat: the claim's parenthetical that 0.5.2/main uses a shortest-prefix + sidecar scheme could not be confirmed in this checkout — that checkout's minting is random-within-length-range, not sidecar-prefix. The core gap — the whole base36/random identity model is absent in the u64-counter model — is fully verified.) Evidence: `src/schema/signal.rs:98,4`; `src/store.rs:333-338`.

**Upgrade socket + owner identity-lifecycle channel + engine-management supervision.** Production: ordinary + owner (Start/Drain/Reload/Register/Retire lifecycle, Mutate forwarding) + upgrade (version handover) + optional engine-management (ComponentHealth/ComponentReady/Identify/Stop). New spirit: working socket + one optional meta socket whose ONLY op is `Configure`; the `ListenerTier` enum has exactly Working and Meta — no Upgrade tier, no lifecycle vocabulary, no supervision channel. Authority rests purely on the 0o600 meta-socket file mode (no peer-cred check on the meta tier). Why it matters: version-handover + owner lifecycle is the machinery that makes side-by-side cutover work; without handover there is no graceful in-place upgrade story. This couples directly to the deployment gap. Evidence: `schema/meta-signal.schema:4`; `src/schema/daemon.rs` ListenerTier; `src/daemon.rs:130-137`.

**CollectRemovalCandidates safety constraints, Print output target, and skip taxonomy.** Production: the sweep is constrained to exact-Zero-certainty AND exact-Zero-privacy (`CollectionQueryGuard::validate` rejects broad queries — a data-safety rail); `OutputTarget` includes `(Print StandardOutput|StandardError)`; 4 skip reasons. New spirit: NO guard — it archives whatever the supplied Query matches (verified: a Maximum-magnitude record was archived+removed, which the production guard would reject); the new Query has no certainty selector at all, so the guard is structurally inexpressible; the archive target moved out of the request to meta `Configure` (Default|Path only); no `Print` variant; only `ArchiveFailed` + `RecordAlreadyRemoved` skip reasons are actually produced (`RecordChanged`/`NoLongerCandidate` declared but unreachable). Why it matters: losing the exact-Zero guard makes a broad CollectRemovalCandidates a near-data-loss footgun — kept at major (not blocker) only because records are archived to a `.sema` file first, so recoverable. Evidence: `src/store.rs:281-324`; `tests/collect_removal_candidates.rs:20-36`; `schema/meta_signal.rs:27-30`.

### Concern

**Observation wrapper vocabulary (Topics, RecordIdentifiers envelope), observation Mode, and CertaintySelection.** Verifier downgraded this from major to concern. Production: `Observe` dispatches a 7-variant Observation enum; `Topics` returns the topic vocabulary with per-topic counts; `Mode` (SummaryOnly/WithProvenance) selects reply shape; `CertaintySelection` filters by certainty; `TopicSelection` supports Any/Partial/Full. New spirit: `Observe` is a bare 3-field `Query` (TopicMatch Partial|Full only — no Any), no Topics op, no Mode/provenance, no certainty filter. Production-shaped wrappers all error live. Mitigation that lowers severity: single-identifier reads survive under the renamed `Lookup` op, so `RecordIdentifiers(Exact)` is name-mapped rather than absent. The genuinely missing pieces are the Topics-listing/counts capability, CertaintySelection, and the Any topic-match. Evidence: `schema/signal.schema:14,105`; `src/store.rs` Query::matches.

**Entire deployment + operational stack.** Verifier downgraded from major to concern because the absence is a deliberate, documented project boundary, not an oversight (the repo's own `INTENT.md` frames it as an iteration/pilot repo intentionally separate from the deployed substrate). Production: side-by-side alias-cutover with per-release `spirit-vX.Y.Z` wrappers + `spirit-next` slot, segregated per-version state dirs, shell wrappers setting `PERSONA_SPIRIT_SOCKET`/`PERSONA_SPIRIT_OWNER_SOCKET`, a CriomOS-home flake module authoring the DaemonConfiguration NOTA + systemd user service, and a versioned migration-binary chain. New spirit: a crane build producing build targets only; `nix/` is empty (confirmed); no versioned wrappers, no module, no migration binaries; CLI socket env is `SPIRIT_SOCKET` (default `/tmp/spirit.sock`), not the `PERSONA_SPIRIT_*` pair the deployed wrappers set. Why it still matters for cutover: the deployed CriomOS-home module cannot start or cut over to this daemon, and there is no migration binary to carry the pinned store forward — confirming adoption is a migration project. Evidence: empty `nix/`; `flake.nix:275-322,378-410`; `src/bin/spirit.rs:37-38`.

**Owner archive-target configuration unreachable from the deployed CLI.** Verifier downgraded from major to concern: the owner-configures-where / peer-does-the-archiving authority split is a documented, intentional design (`ARCHITECTURE.md:189-198`), so the wire shape is correct-by-intent. What is genuinely missing is an operator-facing surface — the shipped CLI (`src/bin/spirit.rs`, single SignalTransport on `SPIRIT_SOCKET`) speaks only `signal::Input` and has no path to the 0o600 meta socket; setting the archive target today requires a custom library `MetaSignalTransport` client. A real operability gap, not a correctness blocker.

### Minor

**Topic non-duplicate validation.** Production `Topics::validate` rejects both empty AND duplicate topic vectors. New spirit `Entry::validate` (`engine.rs:419-432`) checks only non-empty / non-blank — it does NOT reject duplicate topics. A record like `(Record ([[a] [a]] Decision [x] High Zero))` is admitted by new spirit but rejected by production. Low impact (duplicate topics are redundant, not corrupting) but a real validation weakening.

**State (presence) and Questions observation.** Production has `Observe State` → `PresenceView` (itself a hardcoded Absent/None placeholder in deployed 0.5.0) and `Observe Questions` → pending clarification questions. New spirit has neither. Classed minor because the deployed implementations are placeholder/rarely exercised; flagged so the omission is a conscious choice.

## Design audit — core-crate usage

No real bypass found. All five core crates are used at their proper seams; the previously-flagged meta-frame bypass risk (report 541) was resolved into emission rather than entrenched.

### sema-engine — used-properly

The exclusive durable boundary. `store.rs` opens a `sema_engine::Engine` via `EngineOpen::new(path, SchemaVersion)`, registers an identified `Entry` table, and performs every write/read through typed engine ops: `assert_identified` / `mutate_identified` / `retract_identified` / `match_identified` plus `current_commit_sequence()`. No hand-rolled redb/sled/file store and no raw redb handle — redb appears only transitively in `Cargo.lock`. The separate `ArchiveDatabase` for CollectRemovalCandidates is a second sema-engine handle over its own `.sema` file. `StoreError` is a typed thiserror enum with `#[from] sema_engine::Error`. Query predicate semantics (topic/privacy/kind filtering) correctly stay in spirit as domain logic. Evidence: `src/store.rs:6-10,187-201,333-339,367-376,387-391,449-454`.

### signal-frame — used-properly

The socket wire body is signal-frame throughout, reached via schema emission. Emitted `signal.rs` maps `Input`/`Output` onto signal-frame types and emits `encode_signal_frame`/`decode_signal_frame`; the emitted daemon transport and both client transports wrap that codec in `triad_runtime::LengthPrefixedCodec` (a triad-runtime export, not hand-rolled). No hand-rolled length-prefix arithmetic anywhere. CRITICAL update vs report 541: the previously hand-written `encode_meta_frame`/`decode_meta_frame` + route enums in `meta_transport.rs` are RETIRED and replaced by the schema-emitted codec identical to the working plane (its own docstring states this) — the entrenched-bypass risk did NOT materialize. Evidence: `src/meta_transport.rs:1-10,77,84`; `src/schema/signal.rs:1392-1438`; `src/transport.rs:8,86-97`.

### nota-next — used-properly

The sole NOTA path, correctly confined to the text boundary. Wire types get nota-next derives behind the `nota-text` feature; the daemon compiles without nota-next linked. The CLI parses argv via the emitted `parse::<Input>()`, and the LegacyStateInput fallback navigates nota-next's parsed `Document` (`as_delimited`, `NotaBlock::parse_string`) — structured navigation, not a hand-rolled parser. No `serde_json` on the wire (it appears in `Cargo.lock` only under the wit-component emission tooling). Evidence: `Cargo.toml:36,45`; `src/bin/spirit.rs:4,105-138`.

### schema-next / schema-rust-next — used-properly

All wire, plane-envelope, AND daemon types are schema-emitted, source-visible, and freshness-guarded. Five schema sources drive five `src/schema/*.rs` modules, each headed `// @generated by schema-rust-next`; `build.rs` runs the token-based `write_or_check` guard. The Nexus schema is genuinely feature-visible: every internal effect is a declared Nexus verb (Stash, ClassifyState, OpenIntentSubscription, CollectRemovalCandidates, OpenObserverTap, CloseObserverTap), so the engine's internal capability surface reads in one schema file. The daemon skeleton (DaemonCommand, decode→execute→encode spine, listener selection, subscription registry/publish) is now emitted (pilot landed, commit `ad122e3` — "pilot emitted daemon"). Nothing that should be emitted is hand-maintained. Evidence: `src/schema/*.rs:1`; `build.rs:39-49`; `src/schema/daemon.rs:106-431`.

### triad-runtime — used-properly

The daemon is built on triad-runtime's listener shells + the emitted daemon module, not a hand-rolled accept loop. The bin is a true one-liner: `fn main() -> ExitCode { SpiritDaemon::run_to_exit_code() }`. The emitted `GeneratedDaemonRuntime` implements `MultiListenerRuntime`, driven by `MultiListenerDaemon`. Subscriptions use `triad_runtime::{SubscriptionRegistry, SubscriptionEventPublisher, SubscriptionToken}` — the hand-written `SubscriptionHub` is deleted (`src/subscription.rs:1-9` keeps only the token newtype). The Nexus runner (consume→decide→act continuation loop with a budget) is the schema-emitted `NexusEngine::execute` backed by triad-runtime's Runner; spirit supplies only per-step hooks. Evidence: `src/bin/spirit-daemon.rs:3-5`; `src/schema/daemon.rs:7,149,171-179,372`; `src/nexus.rs:32,402-472`.

## Design audit — weird patterns

The findings below survived verification. Two were downgraded by the verifier (noted inline). One praise item stands. All are refinements, not blockers.

### Store-error swallowing in CollectRemovalCandidates and Untap (verified major)

`nexus.rs:389-397` `collect_removal_candidates` does `self.store.collect_removal_candidates(collection).unwrap_or_else(|_error| RemovalCandidatesCollection { archived: empty, removed: empty, skipped: empty, .. })` and the caller replies with a SUCCESS `Output::removal_candidates_collected` — so a genuine sema-engine error (archive DB unwritable, retract failure) is discarded and reported as a successful empty collection, indistinguishable from "nothing matched". Notably the inner store already converts per-record archive failures into typed `SkippedRemovalCandidate{ArchiveFailed}`, so the swallowed errors are precisely the harder store-level failures — masking a partially-failed sweep. Similarly `nexus.rs:370` `observer_tap_table.close(token).unwrap_or_default()` turns an unknown/closed token (whose `None` explicitly means "not registered") into an empty SUCCESS retraction. This is inconsistent, not forced: the contract already has typed failure paths used everywhere else (`Output::rejected(StashHandleNotFound)`, `Output::error(report)`, budget-exhaustion error), and there is a near-exact precedent in `StashHandleNotFound` for an unknown handle. The doc comment rationalizing the swallow conflates a typed-SUCCESS reply with a typed-FAILURE reply — which is exactly the flaw, not an exemption. Recommendation: surface the store error as `Output::error(ErrorReport{...})` (the pattern used in the sema-Missed arms); for Untap return a typed rejection when the token is unknown. Location: `src/nexus.rs:368-371,389-399`.

### meta-signal Input root is a single-variant enum `[Configure]` (verified, downgraded major→concern)

Spirit 1401 (`skills/component-triad.md` §"Interface roots are enums with more than one variant", Clarification High, 2026-06-02) states an interface root enum must have more than one variant; a single-variant root is a newtype wearing enum clothing. The meta-signal schema declares `[Configure]` as its sole Input op (Output `[Configured Rejected]` is fine at 2 variants). The compiler confirms the lack of discrimination: `src/daemon.rs:133` destructures it irrefutably (`let MetaInput::Configure(request) = input;`). There is no meta-signal exemption to the rule (the owner-only framing governs WHO may invoke, not whether the root may be single-variant). Verifier downgraded to concern because this is design-incompleteness, not a runtime bug — the meta surface is genuinely thin today (archive-target config only). Recommendation: develop the meta surface to ≥2 owner-only operations (e.g. add `Reset` or a policy `Mutate` beside `Configure`), or note explicitly in `ARCHITECTURE.md` that the meta plane is a deliberately-minimal pilot — don't let the one-variant root become the copyable exemplar for other components' meta contracts. Location: `schema/meta-signal.schema`; `src/daemon.rs:133`.

### Hand-written client transports duplicate the emitted daemon transport (verified, downgraded concern→minor)

`src/transport.rs:86-97` (`SignalTransport`) and `src/meta_transport.rs:91-102` (`MetaSignalTransport`) have byte-identical `write_frame`/`read_frame` bodies (modulo error-type name), matching the emitted `WorkingTransport` body at `src/schema/daemon.rs:189-198` — three copies straddling the generation boundary (one emitted, two hand-written). Verifier downgraded to minor and corrected the framing: the actual length-prefix envelope algorithm lives exactly ONCE in `triad_runtime::LengthPrefixedCodec` and all three sites delegate to it — what repeats is a ~3-line trivial adapter, not the envelope itself. The meta copy carries a documented temporary-bridge justification (its own docstring; reports 541/544): WireContract emits per-root short_header but not encode/decode_signal_frame yet, so the hand-written meta codec is the bridge until schema-rust-next emits frame codecs for socket-transported wire contracts. Also note `WorkingTransport` is the private server-side type while `SignalTransport` is the public client type — different sides of the wire. Recommendation: promote the length-prefix-around-signal-frame transport to one shared shape (a generic `triad_runtime` transport, or emit the client transport from schema as the daemon transport is). Location: `src/transport.rs:86-97`; `src/meta_transport.rs:91-102`; `src/schema/daemon.rs:188-200`.

### `error_message: String` carries domain errors as prose on the wire (nit)

The schema's `ErrorReport` payload is `{ error_message: String, database_marker }`, populated throughout via `error.to_string()` / `String::from("record not found")` / `format!("nexus continuation budget exhausted ...")`. This is the one place the otherwise strongly-typed contract degrades to a stringly error on the wire: a peer daemon can only display the text, not match on the failure class. Milder than a Rust `Box<dyn Error>` (it is a schema field, and `ValidationError` IS a typed enum used for rejections), but the SEMA/Nexus paths lose the typed-rejection discipline that meta-signal's `ConfigureRejectionReason [ArchiveTargetUnwritable InternalError]` shows the schema can express. Recommendation: promote the SEMA/Nexus error surface to a typed reason enum (e.g. `SemaFailure [RecordNotFound NoMatch ArchiveEncodeFailed ContinuationExhausted ...]`) so cross-component observation can classify failures without parsing prose. Location: `src/store.rs:91-94,103-106,139-146,160-163,171-175`; `src/nexus.rs:462-471`.

### Praise — clean Rust discipline and a single legitimate ZST

The crate is otherwise exemplary against the Rust discipline. The only `struct Name;` ZST in hand-written src is `pub struct SpiritDaemon;` (`daemon.rs:40`) — NOT a ZST-namespace violation: it is the `ComponentDaemon` type-level selector the emitted `DaemonCommand<SpiritDaemon>`/`DaemonEntry` dispatch on to pick spirit's associated types, the sanctioned framework-marker carve-out (its job does not vanish if you erase its name). The crate is free of free functions outside `fn main`, free of `Box<dyn>`, free of stringly errors (every error is a typed thiserror enum with `#[from]`), and every `.expect()` is a Mutex lock-poison or infallible-marked mail-ledger push. This is the shape other components should copy.

## Did not survive verification

- **"Missing real statement classifier."** REFUTED (`standsUp=false`, severity → invalid). The claim's facts about the new spirit are accurate — `ClassificationPolicy::classify` (`nexus.rs:224-234`) is a fixed fallback (every Statement → topics=[unclassified], kind=Clarification, magnitude=Minimum). But the comparative premise is false: production (`persona-spirit/src/actors/classifier.rs:51-66`) is byte-for-byte the SAME fixed fallback — same struct name, same fields, same constant output — and production's own ARCHITECTURE.md states "No LLM classifier or mind-forwarding behavior exists until its intent is clear." No capability was lost; the new spirit faithfully ports the identical deliberate placeholder (and additionally exposes ClassifyState/StateClassified as schema effects). This is not a gap.

Two findings survived but at lower severity than originally claimed (kept, not dropped): the deployment-stack gap (major→concern, deliberate documented pilot boundary), the Observation-wrapper gap (major→concern, partial Lookup survival), the owner-Configure-CLI gap (major→concern, intentional authority split), the single-variant meta root (major→concern, incompleteness not bug), and the duplicate-transport finding (concern→minor, trivial delegating adapter over an already-shared codec). All are reflected at corrected severity above.

## Recommendation

Do NOT cut over yet; this is a migration, not a swap. Proceed to build the missing layer in this order:

1. **Restore wire compatibility on the highest-traffic ops first** — make `Entry` privacy optional-trailing so the 4-field Record shorthand decodes (the day-one break), and decide the Observe vocabulary story (re-add Topics-listing/counts, CertaintySelection, the Any topic-match, and a compatibility envelope or an explicit migration of callers).
2. **Re-establish the privacy access-control tier** — wire the already-threaded SO_PEERCRED `ConnectionContext`, or re-add a typed public/private read split, so elevated-privacy reads are not exposed to every working-socket caller.
3. **Add recorded-time provenance + recency selection** — clock stamping on capture plus a `RecordedTimeSelection` counterpart; this whole production query class is currently impossible.
4. **Decide and build the identity migration** — either keep the u64-counter model and ship a re-keying migration binary for the existing base36-keyed store, or restore base36 identity; pick before any data is carried forward.
5. **Restore the CollectRemovalCandidates safety guard** (exact-Zero certainty/privacy, which needs a certainty selector on Query first) and fix the store-error swallowing (#1 design finding) so failed sweeps surface as typed errors.
6. **Build the deployment + operational stack** — versioned wrappers, per-version state dirs, the CriomOS-home module on the `PERSONA_SPIRIT_*` socket contract, the version-handover/owner-lifecycle channels, and an operator surface to reach meta `Configure`.

Before that work lands, the engine/daemon core is genuinely production-grade and the design is the intended copyable exemplar — keep iterating on the pilot, but keep the alias pointed at deployed persona-spirit 0.5.x. Cut over only after steps 1-4 close (the hard incompatibilities and the migration path) and step 6 makes the daemon deployable by the existing module.
