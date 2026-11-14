# Lojix onto ethos-zero 28: steps 1 to 3 of the brief

The first Lojix steps onto ethos-zero 28 (`970459d`) are done. Each is one commit on a branch named `ethos28-be2651`, pushed and gated green on prometheus. Nothing is merged, released or deployed. Lojix itself is not repinned: that is step 5.

The brief's steps 1, 2 and 3 are the survey's steps 1, 3 and 4. The survey's step 2, ingress, is not part of this task.

Each claim is marked **Observed** (seen in a run or in source) or **Inference**.

## Heads

| repository | was (origin/main) | now (ethos28-be2651) | version |
|---|---|---|---|
| lojix | da0ad8a | 316422f | unchanged |
| horizon-rs (horizon-lib) | e723ce1 | 825a7f0 | 0.17.1 → 0.18.0 |
| signal-lojix | bd5d250 | 8a77619 | 0.11.0 → 0.12.0 |
| meta-signal-lojix | 1b0aaeb | 034e177 | 0.12.0 → 0.13.0 |

Versions follow the rule each repository's UPGRADES states: in 0.x, a change to a stored or archived layout bumps the second number. That is the semver major for a 0.x crate.

## One addition the brief did not name: datom-codec 0.32.3

**Observed.** Under datom-codec 0.32.2 (`4dff16b`), the derive writes a one-field tuple struct as a struct. So the newtypes ethos-zero 28 generates change the Datom text: `OpenCodeTesting.li` became `OpenCodeTesting.{ li }`, and a `Capabilities` list became `{ [ … ] }`. Four horizon contract tests failed on exactly this.

datom-codec 0.32.3 (`eb79226`) is the fix. Its only crate change since 0.32.2 is `eb10157`, "Project tuple newtypes transparently through their inner Datom form". It keeps the same protos, 0.32.2 (`15b41da`).

All three contract crates now pin it. A Lojix graph must hold one datom-codec revision, so the signal crates also pin horizon-lib by its branch commit `825a7f0`. **Inference:** this is the smallest change that keeps every Datom text, including CriomOS's. Orchestrate got the same behaviour from 0.33.

## Step 1: lojix 316422f

The commit deletes the 13 unused types the survey names, and nothing else:
- the nine table newtypes in `src/runtime_model.rs`;
- runtime_model's `Input` and `Output`;
- runtime_flow's `Input` and `Output`.

That is 27 lines removed.

## Step 2: horizon-rs 825a7f0 (horizon-lib 0.18.0)

**What changed.**
- **Pins.** ethos-zero moves to 970459d and datom-codec to 0.32.3.
- **Generated code.** `lib/src/generated/horizon.rs` is regenerated. The Ethos file is unchanged. All 37 aliases are now newtypes: 27 strings, 4 decimals and 6 vectors.
- **Projection code.** It reads each newtype through `.0`, and the tests wrap values where they build them. The public view types (`Horizon`, `Node` and the rest) and `Error` keep their `String`s.
- **build.rs.** It now names the stale file: "src/generated/horizon.rs is stale; regenerate it from ethos/horizon.ethos".
- **flake.** The crane source filter admits `/tests/fixtures/`.
- **UPGRADES.** It has a 0.17.1 to 0.18.0 entry.

**Byte-equality proof (Observed).**
- **Fixtures.** `lib/tests/representation.rs` reads two fixtures, written by origin/main e723ce1 (0.17.1) from one definition:
  - `lib/tests/fixtures/definition-0.17.1.rkyv` (3620 bytes);
  - `lib/tests/fixtures/definition-0.17.1.datom` (3375 bytes).

  The definition carries all 24 node capabilities, both virtual-machine hosts, a fixed location and all three user capabilities.
- **The three tests** all pass in the gate:
  - the 0.17.1 archive reads, and archives back to the same bytes;
  - the 0.17.1 text reads to a value that archives to those bytes;
  - the archive writes the 0.17.1 text again.
- **The real cluster (not committed).** I decoded `goldragon/cluster-definition.datom` (6490c11) as a `ClusterDefinition` with 0.17.1 and with 0.18.0 on the builder:
  - rkyv: 7788 bytes, sha256 `b3093fd1…` for both;
  - compact Datom: sha256 `bb494437…` for both.

  I then deleted the copy from the builder.
- **Inference.** A `HorizonDefinition` that Lojix's Memory holds inside a deploy job reads unchanged under 0.18.0.

## Step 3: signal-lojix 8a77619 (0.12.0)

**What changed in `ethos/signal.ethos`.**
- **Inputs.** Configure, WatchDeployments, Query.Selection, QueryDeploymentEvents.EventLogRange, QueryTestRuns.TestRunLookup, Unwatch. WatchCacheRetention and CacheRetentionWatch are removed.
- **Outputs**, where the n-th output answers the n-th input:
  - Configured, DeploymentsWatched (was Watching), Queried, DeploymentEventsQueried, TestRunsQueried, Unwatched;
  - then ConfigurationRejected, WatchRejected, QueryRejected, UnwatchRejected;
  - then the reaction DeploymentPhaseObserved;
  - then `Refused.Refusal`, with `Refusal.[ Store.String ]`.
- **Selection** keeps ByNode, ByGeneration and ByDeployment.
- **Generation artifacts.** RequestedGenerationArtifact is folded into GenerationArtifact, so `NodeSelector` holds `Option<GenerationArtifact>`.
- **One phase type.** DeploymentLifecycle and DeploymentPhase are now one type, named `DeploymentPhase`; it is the name the event and its output already use. `DeploymentRecord` holds it, and its Rust field is now `deployment_phase`.
- **Markers.** The three markers are written `X.{ DatabaseMarker }`. Each archives to its DatabaseMarker's bytes, but its Datom text gains braces: `Some.{ { 9 17 } }` where it was `Some.{ 9 17 }` (Observed).
- **Enumeration order.** Every enumeration takes the variant order in lojix `src/runtime_model.rs` at da0ad8a. A script checked the 27 enumerations that have a twin there. 26 match. Selection differs only because ByEventLog and ByTestRun left; its three remaining variants are in runtime_model's order.
- **Header comments** describe the pairing, the stream and `Refused.Store`.

**Other files.**
- `build.rs` names the stale file.
- The tests read `Input` and `Output`.
- README and ARCHITECTURE are updated.
- UPGRADES has the 0.11.0 to 0.12.0 entry with the moved-tag table.

**New tests.**
- `each_input_is_answered_by_its_own_output`: a fake Answering Nexus, through `input.answer`.
- `a_store_refusal_is_an_output_of_the_contract`, with its Datom name `Refused.Store.«…»`.
- `the_query_texts_criomos_sends_read_and_write_unchanged`: `Query.ByNode.{ fixture-cluster fixture-node None }` and `Query.ByDeployment.{ 1 }` read, and write back byte-identical.
- In `tests/representation.rs`:
  - every variant tag of the 21 enumerations in Lojix's stored closure;
  - each marker archiving as its DatabaseMarker.

**Moved tags (signal-lojix):**

| enumeration | variant | was | now |
|---|---|---|---|
| Input | WatchCacheRetention | 3 | removed |
| Input | Unwatch | 4 | 5 |
| Input | QueryDeploymentEvents | (new) | 3 |
| Input | QueryTestRuns | (new) | 4 |
| Output | ConfigurationRejected | 1 | 6 |
| Output | TestRunsQueried | 2 | 4 |
| Output | UnwatchRejected | 3 | 9 |
| Output | QueryRejected | 4 | 8 |
| Output | Watching → DeploymentsWatched | 5 | 1 |
| Output | Queried | 6 | 2 |
| Output | DeploymentEventsQueried | 7 | 3 |
| Output | Unwatched | 8 | 5 |
| Output | WatchRejected | 9 | 7 |
| Output | Refused | (new) | 11 |
| UserEnvironmentAction | ActivateNow | 0 | 2 |
| UserEnvironmentAction | Realize | 1 | 0 |
| UserEnvironmentAction | SetProfile | 2 | 1 |
| CacheRetentionTransition | Demoted | 0 | 3 |
| CacheRetentionTransition | Retired | 1 | 4 |
| CacheRetentionTransition | Pinned | 2 | 0 |
| CacheRetentionTransition | Promoted | 3 | 2 |
| CacheRetentionTransition | Unpinned | 4 | 1 |
| FailureStage | HermeticCheck | 0 | 4 |
| FailureStage | BringUp | 1 | 0 |
| FailureStage | Deploy | 3 | 1 |
| FailureStage | TearDown | 4 | 3 |
| HostDeployAction | TestActivation | 0 | 4 |
| HostDeployAction | ScheduleBootOnce | 1 | 5 |
| HostDeployAction | Realize | 2 | 1 |
| HostDeployAction | SetBootProfile | 3 | 2 |
| HostDeployAction | Evaluate | 4 | 0 |
| HostDeployAction | ActivateNow | 5 | 3 |
| GenerationSlot | Pinned | 0 | 3 |
| GenerationSlot | Recent | 1 | 4 |
| GenerationSlot | BootPending | 3 | 1 |
| GenerationSlot | Current | 4 | 0 |
| DeploymentPhase | Built | 0 | 2 |
| DeploymentPhase | Completed | 1 | 6 |
| DeploymentPhase | Failed | 2 | 8 |
| DeploymentPhase | Rejected | 4 | 7 |
| DeploymentPhase | Submitted | 6 | 0 |
| DeploymentPhase | Building | 7 | 1 |
| DeploymentPhase | Activating | 8 | 4 |
| DeploymentInputMode | Horizon | 0 | 1 |
| DeploymentInputMode | Direct | 1 | 0 |
| TestRunPhase | TearingDown | 2 | 4 |
| TestRunPhase | Completed | 3 | 5 |
| TestRunPhase | Deploying | 4 | 2 |
| TestRunPhase | Asserting | 5 | 3 |
| WatchRejectionReason | MalformedWatch | 0 | 1 |
| WatchRejectionReason | SubscriptionLimitReached | 1 | 0 |
| ActivationBackend | HomeManagerNixProfileV1 | 0 | 1 |
| ActivationBackend | NixosSystemdBootV1 | 1 | 0 |
| GenerationArtifact | BaseHost | 0 | 1 |
| GenerationArtifact | CompleteHost | 1 | 0 |
| DeploymentLifecycle → DeploymentPhase | Failed | 0 | 8 |
| DeploymentLifecycle → DeploymentPhase | Rejected | 1 | 7 |
| DeploymentLifecycle → DeploymentPhase | Completed | 2 | 6 |
| DeploymentLifecycle → DeploymentPhase | Building | 3 | 1 |
| DeploymentLifecycle → DeploymentPhase | Submitted | 5 | 0 |
| DeploymentLifecycle → DeploymentPhase | Copying | 6 | 3 |
| DeploymentLifecycle → DeploymentPhase | Activated | 7 | 5 |
| DeploymentLifecycle → DeploymentPhase | Built | 8 | 2 |
| ActivationEffect | ProfileOnly | 0 | 4 |
| ActivationEffect | BootOnceProfile | 1 | 3 |
| ActivationEffect | LiveActivation | 3 | 0 |
| ActivationEffect | BootProfile | 4 | 1 |
| QueryRejectionReason | MalformedSelector | 0 | 3 |
| QueryRejectionReason | EventLogPositionOutOfRange | 1 | 2 |
| QueryRejectionReason | GenerationUnknown | 2 | 0 |
| QueryRejectionReason | NodeUnknown | 3 | 1 |
| DeploymentTerminal | Failed | 1 | 2 |
| DeploymentTerminal | Rejected | 2 | 1 |
| SourceRevisionPolicy | ResolveAndRecord | 0 | 1 |
| SourceRevisionPolicy | RequireImmutable | 1 | 0 |
| DeploymentFailureStage | Build | 0 | 4 |
| DeploymentFailureStage | Eval | 1 | 3 |
| DeploymentFailureStage | Daemon | 3 | 7 |
| DeploymentFailureStage | Activate | 4 | 6 |
| DeploymentFailureStage | Admission | 6 | 0 |
| DeploymentFailureStage | FlakeAuth | 7 | 1 |
| DeploymentTerminalReason | NodeUnknown | 0 | 1 |
| DeploymentTerminalReason | FlakeReferenceMalformed | 1 | 3 |
| DeploymentTerminalReason | DeploymentInFlight | 3 | 7 |
| DeploymentTerminalReason | UnsupportedDeployAction | 5 | 8 |
| DeploymentTerminalReason | InternalError | 6 | 9 |
| DeploymentTerminalReason | ClusterUnknown | 7 | 0 |
| DeploymentTerminalReason | ActivationFailed | 8 | 10 |
| DeploymentTerminalReason | BuilderUnreachable | 9 | 5 |
| DeploymentTerminalReason | SubstituterUnreachable | 10 | 6 |
| Selection | ByTestRun | 1 | removed |
| Selection | ByGeneration | 3 | 1 |
| Selection | ByEventLog | 4 | removed |
| RequestedGenerationArtifact → GenerationArtifact | UserEnvironment | 0 | 2 |
| RequestedGenerationArtifact → GenerationArtifact | CompleteHost | 1 | 0 |
| RequestedGenerationArtifact → GenerationArtifact | BaseHost | 2 | 1 |
| Refusal | Store | (new) | 0 |

## Step 3: meta-signal-lojix 034e177 (0.13.0)

**What changed.**
- **Inputs.** Unchanged.
- **Outputs**, where the n-th output answers the n-th input:
  - Configured, ConfigurationReversed, Retired, Pinned, DeployAccepted, Tested, Unpinned;
  - then ConfigurationRejected, RetireRejected, PinRejected, DeployRejected, DeployRefused, TestRejected, UnpinRejected;
  - then DeployTerminal;
  - then `Refused.Refusal`, with `Refusal` imported from signal-lojix.
- **Enumeration order.** Every enumeration takes runtime_model's order. All 8 that have a twin there match.
- **DeploySubmission** is `[ Host UserEnvironment ]`. That is the stored order, and a test checks it.
- **ClientQuery** is unchanged.
- **Pins.** signal-lojix 8a77619, horizon-lib 825a7f0, datom-codec 0.32.3, ethos-zero 970459d.
- **Other files.** build.rs names the stale file, the tests use Input and Output, the README is updated, and UPGRADES carries the moved tags.

**New tests.**
- The pairing test, with all 7 inputs.
- The store-refusal test, as bytes and as text.
- The CriomOS harness-update deploy text, with its variables filled in. It reads as `ClientQuery::Deploy(UserEnvironment)` and writes back byte-identical.
- The DeploySubmission tag test.

**Moved tags (meta-signal-lojix):**

| enumeration | variant | was | now |
|---|---|---|---|
| Output | ConfigurationRejected | 1 | 7 |
| Output | ConfigurationReversed | 2 | 1 |
| Output | PinRejected | 3 | 9 |
| Output | DeployRejected | 4 | 10 |
| Output | DeployRefused | 5 | 11 |
| Output | DeployAccepted | 6 | 4 |
| Output | TestRejected | 7 | 12 |
| Output | Unpinned | 8 | 6 |
| Output | Tested | 9 | 5 |
| Output | UnpinRejected | 10 | 13 |
| Output | DeployTerminal | 11 | 14 |
| Output | Pinned | 12 | 3 |
| Output | RetireRejected | 13 | 8 |
| Output | Retired | 14 | 2 |
| Output | Refused | (new) | 15 |
| PinRejectionReason | PinSlotExhausted | 0 | 3 |
| PinRejectionReason | InternalError | 1 | 4 |
| PinRejectionReason | NodeUnknown | 2 | 1 |
| PinRejectionReason | PinLabelInUse | 3 | 2 |
| PinRejectionReason | GenerationUnknown | 4 | 0 |
| NodeSelection | All | 0 | 1 |
| NodeSelection | Nodes | 1 | 0 |
| RetireRejectionReason | NodeUnknown | 0 | 1 |
| RetireRejectionReason | GenerationUnknown | 1 | 0 |
| RetireRejectionReason | GenerationPinned | 2 | 3 |
| RetireRejectionReason | InternalError | 3 | 4 |
| RetireRejectionReason | GenerationActive | 4 | 2 |
| UnpinRejectionReason | GenerationNotPinned | 0 | 2 |
| UnpinRejectionReason | PinLabelUnknown | 1 | 0 |
| UnpinRejectionReason | InternalError | 2 | 3 |
| UnpinRejectionReason | NodeUnknown | 3 | 1 |
| DeploySubmission | UserEnvironment | 0 | 1 |
| DeploySubmission | Host | 1 | 0 |
| TestRejectionReason | SubstrateUnavailable | 0 | 6 |
| TestRejectionReason | NoTestDefaults | 1 | 4 |
| TestRejectionReason | ClusterUnknown | 2 | 0 |
| TestRejectionReason | LiveNotYetEnabled | 4 | 5 |
| TestRejectionReason | NodeUnknown | 5 | 1 |
| TestRejectionReason | VmHostNotDeclaredForNode | 6 | 2 |

## Further byte proof for the signal crates

- **Observed, scratch, not committed.** A `DeploymentPhaseEvent` built from the new newtypes archives to the same 131 bytes as a mirror built from `i64`, `String` and a plain two-level marker struct.

  This is the record Lojix's event log stores. Together with the tag tests, it covers the integer newtypes, the string newtypes and the marker structs.
- **Inference.** Lojix's Memory keeps its bytes when step 5 repins.

## Gates

All four were run in the foreground on prometheus with `nix-fast-build --remote prometheus.goldragon.criome --no-nom --no-download --eval-workers 1`, against the pushed branch head.

| repository | head | result | log |
|---|---|---|---|
| lojix | 316422f | 18 of 18 green, including the four NixOS VM checks | /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-lojix-step1.log |
| horizon-rs | 825a7f0 | 3 of 3 green; the representation test ran, 3 passed | /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-horizon-rs.log |
| signal-lojix | 8a77619 | 10 of 10 green (build, clippy, fmt, doc, four test checks, two shape checks) | /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-signal-lojix.log |
| meta-signal-lojix | 034e177 | 10 of 10 green | /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/gate-meta-signal-lojix.log |

Lock files were resolved on the builder through each repository's devShell cargo, `nix develop -c cargo`, because the plain `cargo` wrapper refuses there too.

## What lojix must change to repin (step 5)

**Pins, in one step.** Lojix needs one datom-codec and one revision of each contract in its graph.
- Every `4dff16b` datom-codec edge moves to `eb792265a67b2c6865f9b8c9ed9d2e5ae5a7174c`. The edges are in Cargo.toml, nexus, tools, and clients/meta and clients/ordinary.
- horizon-lib `e723ce1` moves to `825a7f09242380a7b3d2609b26e20647db46a8ce` in Cargo.toml, nexus, tools and clients/meta. The flake input `horizon` (flake.nix line 17) moves too.
- signal-lojix `bd5d250` moves to `8a776198db368c7f5d39e1615c3d3d319fc2cf5d`, the revision meta pins.
- meta-signal-lojix `1b0aaeb` moves to `034e17788316516e0be4417962d9bbde216c6f9b`.

**Code (Observed, by grep of da0ad8a):**
- **Horizon newtypes.** `horizon_lib` is used on 31 lines across 10 files. Wherever lojix builds or reads a Horizon name or list, it wraps or reads through `.0`.
- **Roots.** `Query` and `Response` become `Input` and `Output`: 132 lines across 8 files, the daemon, adapters, both clients and their tests.
- **Signal newtypes.** Every scalar that adapters.rs lowers from a bare `String` or `i64` is now a newtype, so its `text_value!` and `integer_value!` arms change. The same goes for the configuration defaults, TestDefaults and the configuration writer.
- **Selection.** `Selection::ByEventLog` and `ByTestRun` (20 lines in adapters, daemon, runtime_model, lib, schema_runtime) become the inputs `QueryDeploymentEvents` and `QueryTestRuns`.
- **Watching.** `Watching` becomes `DeploymentsWatched` (22 lines). That includes the reply-line test, the deployment-watch test and the flake.nix comment at line 208.
- **WatchCacheRetention.** Its handling goes (6 lines in adapters, runtime_model, schema_runtime).
- **One phase type.** Where the wire is lowered, `DeploymentLifecycle` and `deployment_lifecycle` become `DeploymentPhase` and `deployment_phase` (67 lines, most of them tests). runtime_model's two hand enums may stay until step 6.
- **Generation artifacts.** `RequestedGenerationArtifact` and `requested_generation_artifact` become `GenerationArtifact` (10 lines).
- **Markers.** They are structs: `AdmissionMarker { database_marker }` in place of a bare DatabaseMarker.
- **Store refusal.** Matches over `Output` gain `Refused`. The daemon may answer a store failure with `Output::Refused(Refusal::Store(..))`, where today it ends the connection.
- **Exhaustive matches.** Matches over meta `Output` pick up the reorder only by name; no code depends on tags.

**Texts.**
- CriomOS's `Query.ByNode.{ … }`, `Query.ByDeployment.{ … }`, `Deploy.UserEnvironment.{ … }` and the `DeployAccepted.{ N` grep are unchanged. Tests show this.
- Any text or grep that reads `Watching.`, `Query.ByEventLog` or `Query.ByTestRun`, or a marker's `{ seq digest }`, changes.

**Memory (Inference).** With these pins, every stored contract twin keeps its tag order and archive, and lojix's three store fixtures should open unchanged. Step 5 proves it.

## Notes

- **One-variant enums.** `Refusal.[ Store.String ]` is an enum of one variant, following Orchestrate's precedent. Item 11's generator fix in ethos-zero 29 would refuse it, together with horizon's `CompositionCommand`, so that ruling reaches both repositories.
- **Pins on branch commits.** signal-lojix and meta-signal-lojix pin horizon-lib, and meta pins signal-lojix, by branch commits that are not merged. When those branches merge, the merge commits must keep these revisions reachable, or the pins move with them.
- **Worktrees.** The worktrees used are under `/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/wt/`, and the builder copies are under `/tmp/offload/{horizon-rs,signal-lojix,meta-signal-lojix}`.
