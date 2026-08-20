# Repository Test Inventory — 2026-08-20

Survey of tests across /git/github.com/LiGoldragon/ repositories.
Covers the most recently active repos that contain tests, plus all
priority repos (Curriculum, signal-*, sema/sema-engine, ethos-related,
mentci-related, datom-related).

## Categories

| Key | Meaning |
|-----|---------|
| (a) | Runs compiled machinery and asserts on its behavior/output |
| (b) | Round-trips or compares generated output against authored source |
| (c) | Reads/searches source or authored text and asserts on its content |
| (d) | Computes expected value with the same code path it is testing |
| (f) | No assertion, or cannot fail |
| (g) | Sleeps/depends on timing, order, network, or shared mutable state |

Categories (e) (asserts only that mocks/stubs were called) and (h) (other)
were not observed in any surveyed repo.

## Summary Table

| Repo | Total | (a) | (b) | (c) | (d) | (f) | (g) | Notes |
|------|-------|-----|-----|-----|-----|-----|-----|-------|
| Curriculum | 42 | 36 | 5 | 1 | 0 | 0 | 0 | |
| chroma | 121 | 72 | 27 | 15 | 0 | 1 | 4 | 4 async timing tests overlap with (a) |
| lojix | ~130 | ~123 | 4 | 3 | 0 | 1 | 1 | 1 `#[ignore]` network test |
| ethos-monolith | 13 | 9 | 1 | 2 | 0 | 1 | 0 | |
| datom | 7 | 3 | 4 | 0 | 0 | 0 | 0 | |
| protos | 25 | 21 | 4 | 0 | 0 | 0 | 0 | |
| signal-system | 35 | 1 | ~32 | 2 | 0 | 0 | 0 | |
| signal-psyche | 1 | 0 | 0 | 1 | 0 | 0 | 0 | Shell script only |
| signal-mirror | 12 | 1 | 6 | 7 | 0 | 0 | 0 | |
| signal-agent | 4 | 0 | 2 | 2 | 0 | 0 | 0 | |
| signal-router | 45 | 0 | 44 | 1 | 0 | 0 | 0 | |
| signal-mentci | 4 | 0 | 2 | 2 | 0 | 0 | 0 | |
| signal-lojix | 9 | 0 | 3 | 6 | 0 | 0 | 0 | |
| sema-engine | 34 | 34 | 0 | 0 | 0 | 0 | 0 | Richest behavioral suite |
| sema | 22 | 17 | 1 | 3 | 0 | 1 | 0 | 1 test has no assertion |
| mentci | 81 | 63 | 4 | 3 | 0 | 0 | 11 | 7 timing-dep in criome_bridge |
| mentci-lib | 12 | 12 | 0 | 0 | 0 | 0 | 0 | |
| mentci-egui | 13 | 9 | 2 | 0 | 0 | 0 | 2 | |
| synchronizer | ~44 | ~32 | ~11 | 1 | 0 | 0 | 1 | 1 ignored network test |
| ethos-engine | 5 | 5 | 0 | 0 | 0 | 0 | 0 | |
| spirit-judge | 10 | 8 | 0 | 0 | 0 | 0 | 2 | Duplicate test body |
| whisrs | 113 | 88 | 7 | 0 | 3 | 0 | 2 | env::remove_var race |
| structural-codec | 22 | 22 | 0 | 0 | 0 | 0 | 0 | |
| persona | ~31 | 22 | 2 | 7 | 0 | 0 | 2 | Daemon socket poll loops |
| persona-spirit | ~47 | 40 | 1 | 5 | 0 | 0 | 2 | Daemon socket poll loops |
| mirror | 9 | 6 | 1 | 2 | 0 | 0 | 0 | Obfuscated field names |
| cloud | ~27 | 25 | 1 | 0 | 0 | 0 | 1 | `#[ignore]` live API test |
| agent | 4 | 4 | 0 | 0 | 0 | 0 | 0 | |
| schema | ~30 | 22 | 6 | 0 | 0 | 0 | 0 | |
| schema-language | ~30 | 20 | 9 | 1 | 0 | 0 | 0 | |
| schema-rust | 11 | 11 | 0 | 0 | 0 | 0 | 0 | |
| nomos-engine | 2 | 1 | 1 | 0 | 0 | 0 | 0 | Very thin coverage |
| logos-engine | 3 | 2 | 0 | 1 | 0 | 0 | 0 | Very thin coverage |
| horizon-rs | 29 | 29 | 0 | 0 | 0 | 0 | 0 | |
| version-projection | 7 | 4 | 2 | 1 | 0 | 0 | 0 | |
| triad-runtime | ~30 | 25 | 3 | 2 | 0 | 0 | 0 | |
| content-identity | 11 | 4 | 5 | 0 | 1 | 0 | 0 | |
| tree-sitter-ethos | 1 | 0 | 1 | 0 | 0 | 0 | 0 | Requires `tree-sitter test` |
| tree-sitter-dotos | 1 | 0 | 1 | 0 | 0 | 0 | 0 | Requires `tree-sitter test` |
| mind-tests | 1 | 1 | 0 | 0 | 0 | 0 | 0 | Floating branch dep |
| CriomOS | 10 | 10 | 0 | 0 | 0 | 0 | 0 | NixOS VM tests only; require KVM |

## Repos with zero tests

| Repo | Notes |
|------|-------|
| signal-domain-criome | Empty repo (AGENTS.md only) |
| domain-criome | Empty repo (AGENTS.md only) |
| transcript | 407-line Python CLI; no tests of any kind |

---

## Per-Repo Sections

### Curriculum (42 tests)

All tests in `tests/generation.rs`. A `Fixture` helper creates temp dirs,
writes source files, runs the generator, and asserts on output.

Representative examples:
- `generation.rs:43` — `assert!(matches!(operation, Operation::Generate(_)));` **(a)**
- `generation.rs:107` — `assert_eq!(generated, "---\nname: example\ndescription: ...")` **(b)** output matches authored expectation
- `generation.rs:343` — `assert!(include_str!("../manifests/universal-role-modules.dotos").contains("[general-instructions]"))` **(c)** reads authored manifest
- `generation.rs:428` — `assert!(matches!(error, Error::ModuleDependencyCycle { .. }))` **(a)**

### chroma (121 tests)

Tests across 9 files. `hard_constraints.rs` (15 tests) is an architecture-enforcement
suite that `include_str!`s production source and asserts on presence/absence of named
constructs — all **(c)**.

- `theme.rs:96` — `assert_eq!(round_trip_dotos(&ThemeMode::Dark), ThemeMode::Dark);` **(b)**
- `theme.rs:115` — `assert_eq!(received, ("dark\n".to_string(), "dark\n".to_string()));` **(a)/(g)** async timeout
- `theme.rs:185` — no explicit assert; passes if `apply_theme` completes **(f)**
- `request.rs:6–68` — all 15 tests round-trip Request variants through DOTOS+rkyv **(b)**
- `hard_constraints.rs:5` — `assert!(source.contains("impl Actor for ChromaRoot"))` **(c)**
- `geoclue.rs:116` — tokio test with `timeout(Duration::from_secs(1), ...)` **(g)**

### lojix (~130 tests)

39 integration tests, ~91 inline. Largest suite is `src/schema_runtime.rs` (~63 tests)
covering activation, flake locator policy, boot scripts, systemd profiles, secrets,
self-switch recovery, nix eval command shapes — all **(a)**.

- `test_op.rs:7` — `let _runtime = SchemaRuntime::new();` no assertion **(f)**
- `build_smoke.rs:59` — `assert_eq!(decoded, input);` **(b)**
- `daemon_configuration.rs:66` — `assert!(... .contains("PinRejected"))` **(a)/(g)** socket wait
- `horizon_materialization_contract.rs:7` — `assert!(flow.contains("pub struct HorizonMaterializationCommand"));` **(c)**
- 1 `#[ignore]` test: `fixture_eval_reserves_a_durable_deployment_before_effects` — hits network

### ethos-monolith (13 tests)

- `interface_fixture.rs:15` — no assert; proves generated types construct without panic **(f)**
- `interface_fixture.rs:244` — `interface.rust_artifact(path)...assert_matches_existing()` **(b)**
- `architecture_guards.rs:2163` — parses all `src/` files with `syn`, asserts no structural violations **(c)**

### datom (7 tests)

All in `tests/substrate.rs`. Mix of behavioral and round-trip tests on the datom substrate.

- `substrate.rs:38` — `assert_eq!(again.textualize().expect(...), canonical);` **(b)**
- `substrate.rs:288` — `assert_eq!(invalid_group_key.textualize(), Err(... AmbiguousMapPair))` **(a)**

### protos (25 tests)

20 in `tests/substrate.rs`, 5 architecture guard tests.

- `substrate.rs:235` — `assert_eq!(report.textualize(), source);` **(b)**
- `substrate.rs:307` — `assert_eq!(remark.string_carrier, Some(StringCarrier::Parenthesized(...)));` **(a)**
- `guards.rs:17` — `assert!(status.success(), "guard {name} failed with {status}");` **(a)**

### signal-system (35 tests)

All in `tests/round_trip.rs`. Predominantly frame/dotos/rkyv encode-decode round-trips.

- `round_trip.rs:110` — `assert_eq!(decoded, request)` **(b)** frame round-trip
- `round_trip.rs:198` — `assert_eq!(request.operation_kind(), operation)` **(a)** behavioral dispatch
- `round_trip.rs:440` — `assert!(violations.is_empty(), ...)` **(c)** reads `src/lib.rs` for forbidden tokens

### signal-psyche (1 test)

Single shell test `tests/dependency-boundary.sh` asserting the crate has no public
symbols or dependencies — **(c)**.

### signal-mirror (12 tests)

- `interface_contract.rs:7` — `assert!(source.starts_with("Interface.{1 0 0}\n[signal_standard:lib.["))` **(c)**
- `canonical_examples.rs:4` — `assert_eq!(value.to_dotos(), *text)` **(b)** authored fixture
- `round_trip.rs:174` — `assert_eq!(decoded, expected)` **(b)** frame round-trip

### signal-router (45 tests)

40 in `tests/round_trip.rs` (all **(b)** frame encode/decode), 4 canonical examples **(b)**,
1 ethos reader test **(c)**.

### signal-agent, signal-mentci, signal-lojix (4, 4, 9 tests)

Uniform pattern: `round_trip.rs` tests **(b)**, `dependency_boundary.rs` tests **(c)**.

### sema-engine (34 tests)

All **(a)**. Richest behavioral test suite — exercises write/compact/restart/import/replay
cycles against a redb-backed engine. Each test uses `TempDir` for isolation.

- `compaction.rs:90` — `assert_eq!(compacted.compacted_entries(), 2)` + restart rebuild
- `import.rs:187` — `assert_eq!(rebuilt.records(), &[...])` import into fresh engine
- `family_identity.rs:130` — `assert_eq!(receipt.applied(), 4)` cross-engine replay

### sema (22 tests)

- `kernel.rs:67` — no assertion, just `unwrap()` without checking value **(f)**
- `kernel.rs:78` — `assert_eq!(header, DatabaseHeader::current())` **(a)**
- `kernel.rs:230` — `assert_eq!(read_back, original)` **(b)** redb round-trip
- `no_legacy_surface.rs:14` — `assert!(!source.contains("pub struct Slot"))` **(c)**

### mentci (81 tests)

- `state.rs:61` — `assert_eq!(reply, MentciReply::QuestionPresented(...))` **(a)**
- `frame_codec.rs:18` — `assert_eq!(recovered, frame)` **(b)**
- `preflight.rs:220` — `assert!(!source.contains(term), ...)` **(c)** source boundary check
- `criome_bridge.rs:265` — `assert!(listed_after_cancel.policies().is_empty())` **(g)** socket poll loop
- `harness_liveness.rs:125` — `assert_eq!(outcome.reason(), &StopReason::IdleTimeout)` **(g)** wall-clock

### mentci-lib (12 tests)

All **(a)** in `tests/model.rs`. Exercises observation model, approval cursor, verdicts.

### mentci-egui (13 tests)

- `control.rs:488` — `assert_eq!(recovered, input)` **(b)** DOTOS round-trip
- `control.rs:505` — `assert_eq!(request.input(), &expected)` **(g)** real socket exchange

### synchronizer (~44 tests)

14 integration test files covering topology, release trains, Cargo/Nix manifest
manipulation, cascade bumping.

- `flake_lock.rs:73` — `assert_eq!(rendered, LOCK_TEXT, ...)` **(b)** byte-identical reserialize
- `topology.rs:203` — `assert!(matches!(cyclic.ascent_levels(), Err(Error::DependencyCycle { .. })))` **(a)**
- `nix_resolution.rs:139` — `#[ignore]` network+SSH test **(g)**

### ethos-engine (5 tests)

All **(a)**. Tests legacy-vs-native ingestion equivalence and interface surface agreement.

- `equivalence.rs:121` — `assert_eq!(legacy_identity, native_identity, ...)` **(a)**

### spirit-judge (10 tests)

- `lib.rs:772` — `assert!(matches!(reply, SpiritJudgeReply::AdmissionJudged(... Accept ...)))` **(a)**
- `lib.rs:890` — `assert_eq!(reply, served_reply)` **(g)** tokio test with 25ms sleep
- Duplicate test body: `adapter_configuration_names_external_prompt_root` appears identically in `tests/scaffold.rs:5` and `src/lib.rs:752`.

### whisrs (113 tests)

Across 6 source files. Largest suite is `filler-remove` (25 tests) and
`xkb-type/keymap` (34 tests).

- `audio-silence-gate/lib.rs:251` — `assert!(detector.feed(&silence))` **(a)**
- `feedback.rs:193` — `assert_eq!(samples.len(), expected)` where expected uses same formula **(d)**
- `filler-remove/lib.rs:466` — `assert_eq!(filter.apply(case), remove_filler_words(case, &[]))` **(d)** same code path
- `lib.rs:835` — calls `std::env::remove_var(...)` **(g)** races with parallel tests
- `capture.rs:285` — `assert_eq!(read_samples, samples)` **(b)** WAV encode round-trip

### structural-codec (22 tests)

All **(a)** in `tests/downstream_authoring.rs` and `tests/normalization.rs`.

- `downstream_authoring.rs:1133` — `assert_eq!(evaluator.encode_text(...), "Result<Vector Error>")` **(a)**
- `downstream_authoring.rs:2220` — `assert_eq!(forward.identity(), reverse.identity())` **(a)** order independence

### persona (~31 tests)

- `engine.rs:168` — `assert!(TemporaryEngineRoot::contains(layout.state_dir(), "state/engine-alpha"))` **(a)**
- `daemon.rs:325` — runs binary, polls socket with sleep loop **(a)/(g)**
- `actor_discipline_truth.rs:41` — `assert!(violations.is_empty(), ...)` **(c)** scans src/ for `Arc<Mutex`
- `schema.rs:49` — `assert_eq!(recovered, report)` **(b)** NOTA round-trip

### persona-spirit (~47 tests)

- `sema_projection.rs:85` — `assert_eq!(effect_event_for(request, reply), EffectEmitted { ... })` **(a)**
- `daemon.rs:241` — `assert_eq!(configuration, fixture.configuration())` **(b)** NOTA round-trip
- `actor_runtime.rs:819` — `assert!(!source.contains("SpiritActorRuntime"))` **(c)** reads source

### mirror (9 tests)

- `daemon_logic.rs:242` — `assert_eq!(rejection.field_0, ...)` **(a)** obfuscated field names
- `dependency_boundary.rs:3` — `assert!(manifest.contains(required), ...)` **(c)** reads Cargo.toml

### cloud (~27 tests)

- `hetzner.rs:119` — `assert_eq!(host, CloudHost { provider: Provider::Hetzner, ... })` **(a)** fixture mock API
- `runtime.rs:256` — `assert_eq!(decoded, configuration)` **(b)** config round-trip
- `digitalocean_live.rs:27` — `#[ignore]` live API poll with sleep **(g)**

### schema (~30 tests), schema-language (~30 tests), schema-rust (11 tests)

Schema repos are predominantly **(a)** (lowering, typing, editing, rejection paths)
with **(b)** round-trips through rkyv/DOTOS/canonical text.

- `content-identity` capsule_identity.rs:46 is the only **(d)** test: two API entry points
  for the same hash computation tested against each other rather than an oracle.

### nomos-engine (2 tests), logos-engine (3 tests)

Very thin coverage.

- `nomos-engine/tests/bootstrap.rs:177` — `assert_eq!(WholeLogos::from_archive_bytes(...), *outcome.logos())` **(b)**
- `logos-engine/src/lib.rs:428` — `assert!(status.success(), "projected Rust must compile")` **(a)**

### horizon-rs (29 tests)

All **(a)**. Error display, key parsing, machine/proposal decoding from DOTOS records.

### triad-runtime (~30 tests)

- `trace.rs:103` — `assert_eq!(decoded, event)` **(b)** trace frame socket round-trip
- `signal_frame_boundary.rs:1` — `assert!(manifest.contains(expected))` **(c)** reads Cargo.toml

### content-identity (11 tests)

- `integrity.rs:23` — `assert_eq!(digest.bytes(), &INTEGRITY_LOCK)` **(b)** stability lock
- `capsule_identity.rs:46` — `assert_eq!(ContentAddressedHash::derive(...), preimage.derive_...)` **(d)** same computation
- `mutation.rs:9` — `assert_ne!(derive(&[1,2,3]), derive(&[1,2,4]))` **(a)** mutation sensitivity

### tree-sitter-ethos, tree-sitter-dotos (1 test each)

Both **(b)**: tree-sitter corpus tests diff parse tree against authored S-expression.
Run via `tree-sitter test`, not `cargo test`.

### mind-tests (1 test)

- `scaffold.rs:3` — `assert!(DotoslArtifactPath::new(...).is_ok())` **(a)**

Note: floating `branch = "main"` git dep.

### CriomOS (10 tests via NixOS VM)

Two NixOS VM tests in `.nix` files. Require `/dev/kvm`. All **(a)**: boot VM, drive daemon,
assert on service state, socket modes, identity receipts.

## Cross-Cutting Observations

- No category (e) (mock-only assertions) found anywhere. Where mocks exist (lojix
  `SuppressedExecutor`, cloud fixture APIs), assertions target behavioral outcomes.
- Category (c) "architecture guard" tests appear in ~12 repos. The consistent pattern:
  `include_str!` or `fs::read_to_string` production source, then assert
  presence/absence of strings to enforce architectural invariants at test time.
- Category (f) tests (3 total across survey) prove compilation and non-panic but
  cannot catch logic errors.
- Category (d) tests (4 total: 3 in whisrs, 1 in content-identity) compute expected
  values through the same code path under test.
- `spirit-judge` has a duplicate test body across two files.
- `whisrs` `lib.rs:835` mutates shared process env with `std::env::remove_var`,
  which will race under `cargo test` parallelism.
