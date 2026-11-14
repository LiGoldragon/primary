# Lojix onto its Ethos: ethos-zero 29, the ingress, and the repin

This report covers steps 1 to 3 of the brief. Each step that landed is one commit on a branch named `ethos28-be2651`. Each was pushed and gated green on prometheus. Nothing is merged, released or deployed.

Step 1 is only partly done. horizon-lib and signal-lojix need a design ruling first (see "Needs a ruling").

Each claim is marked **Observed** (seen in a run or in source) or **Inference**.

Scratch directory: `/tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad`, written `$S` below.

## Heads

| repository | was | now | commits |
|---|---|---|---|
| meta-signal-lojix | 034e177 | 4e42269 | step 1 |
| lojix | 316422f | 26caf36 | 4b2c50f (step 3), then 26caf36 (step 2) |
| horizon-rs (horizon-lib) | 825a7f0 | 825a7f0 | none; blocked |
| signal-lojix | 8a77619 | 8a77619 | none; blocked |

Lojix's own version moves from 0.10.6 to 0.10.7. Its UPGRADES rule is that only a store-format change moves the second number, and the store format is unchanged.

**Order.** Step 2 landed after step 3, for this reason:
- The ingress's new newtypes keep their tool text only under datom-codec 0.32.3, which writes a newtype as the value it wraps.
- A Lojix graph holds one datom-codec, so that version arrives only with the step-3 repin.
- Under 0.32.2, every scalar in the tool texts would have gained braces.

## Step 1: ethos-zero 29.0.0 (f23eacf)

**meta-signal-lojix 4e42269 (Observed).**
- The build-dependency is repinned from 970459d to f23eacf, and the lock was resolved on the builder.
- The 29 binary regenerates `src/generated/signal.rs` byte-identical to the committed file.
- The UPGRADES line now names 29.0.0.

**horizon-lib and signal-lojix are refused by 29 (Observed).**
- `horizon.ethos` is refused at `{ 67 15 } TooFewVariants.MotherBoard`.
- signal-lojix's `signal.ethos` is refused at `{ 137 11 } TooFewVariants.Refusal`.
- I gave each one-variant enum a probe second variant in a scratch copy. With that, 29 generates Rust identical to the committed files except for the probe lines: 5 in horizon and 1 in signal.
- So the only change 29 forces is the enums. I left both repositories untouched (see "Needs a ruling").

## Step 3: lojix 4b2c50f, the repin

**Pins, on every edge.**

| dependency | was | now |
|---|---|---|
| signal-lojix | 0.11.0 (bd5d250) | 0.12.0 (8a77619) |
| meta-signal-lojix | 0.12.0 (1b0aaeb) | 0.13.0 (4e42269) |
| horizon-lib | 0.17.1 (e723ce1) | 0.18.0 (825a7f0), and the flake input `horizon` |
| datom-codec | 0.32.2 (4dff16b) | 0.32.3 (eb79226) |
| nexus | 0.1.1 (a84bfa9) | 0.5.0 (64a735d) |

Between nexus 0.1.1 and 0.5.0, `ConfigurationState` gains only `Hash`, so its archive is unchanged (Observed in the diff).

**Mechanical changes.**
- **Roots.** `Query` and `Response` become `Input` and `Output`.
- **Newtypes.** They are built by their constructors and read through `.0`. That covers the configuration defaults and the legacy conversion in lib.rs, the TestDefaults in schema_runtime, the daemon's sockets, and the meta client's proposal path.
- **adapters.rs is kept.**
  - `text_value!` and `integer_value!` now convert between a wire newtype and its runtime twin.
  - The wire's one `DeploymentPhase` is raised from the runtime `DeploymentLifecycle`.
  - The three markers are raised as structs that hold the DatabaseMarker.
  - `RequestedGenerationArtifact` is gone.
- **Selection.** It lowers ByNode, ByGeneration and ByDeployment. The new inputs `QueryDeploymentEvents` and `QueryTestRuns` lower to the engine's own `ByEventLog` and `ByTestRun` selections, so the engine is unchanged.
- **WatchCacheRetention leaves**, with its runtime twin `CacheRetentionWatch`.
- **Watching.** The runtime `Watching` is raised as `DeploymentsWatched`.
- **Refused.Store.**
  - Where a store read or write failed under a query, pin, unpin or retire, the engine used to panic and the connection closed with no reply. Nine sites are affected: six reads and three writes.
  - Each now answers `StoreRefused(<what failed>)`, which is raised as `Output::Refused(Refusal::Store(..))` on either socket.
  - The panics that answer no request stay as they were: the test-run record and the container transition.
- **Tests.**
  - Clients and tests follow the same changes.
  - The reply-line and deployment-watch tests now expect `DeploymentsWatched.`.
  - New adapter tests cover the store refusal on both sockets and the two split query inputs.
- **Docs.** ARCHITECTURE and UPGRADES (0.10.6 to 0.10.7) are updated.

**lojix-test** pins Lojix by flake lock and holds none of the changed texts, so it needs no change (Observed, by grep at a4fc77b).

## Step 2: lojix 26caf36, the ingress on 29

**`ethos/ingress.ethos`.** Each one-variant enum is now the variant's type itself:
- `InspectionRequest` becomes `InspectStore.{ String }`.
- `ResetStoreRequest` becomes `ResetStore.{}`.
- `BootstrapRequest` becomes `BootstrapRun`.
- `ConfigurationWriterInput` becomes `ConfigurationWriteRequest`.
- `BootstrapStrictHostKeyMode` becomes `RequireKnownHost.{}`, carried by `BootstrapSshPolicy` in the same position.

**Assumed.** For the two unit variants, `ResetStore` and `RequireKnownHost`, I read "the variant's type" as an empty struct named by the variant. That is the unit ethos-zero 29 gives a bare emission. The alternative was to drop the policy field.

**Other changes.**
- `src/ingress.rs` is regenerated with the 29 binary.
- **Freshness.** The check moved from `tests/ingress_freshness.rs` into lojix's `build.rs`, with ethos-zero f23eacf as a build-dependency. A stale file fails the build with "src/ingress.rs is stale; regenerate it from ethos/ingress.ethos" (Observed on a deliberately stale copy). Its text test moved to `tests/ingress_text.rs`, together with a new test that the reset request is `{}` and nothing else.
- **Code.** `bootstrap.rs` reads the newtypes by destructuring them. The hand bootstrap model is unchanged, so the journal fingerprint is unchanged too. The configuration writer, the inspector and the reset command read their request as the struct.
- **Texts.** Tests, the VM check in flake.nix, README, ARCHITECTURE, skills.md, NON_IDEAL_AGENTS and UPGRADES carry the new texts.

## Tool text changes

| tool | was | now |
|---|---|---|
| lojix-inspect-store | `InspectStore.{ <path> }` | `{ <path> }` |
| lojix-reset-store | `ResetStore` | `{}` |
| lojix-bootstrap | `BootstrapRun.{ <id> <mode> }` | `{ <id> <mode> }` |
| lojix-bootstrap, the Remote policy | `{ <identity> <known-hosts> RequireKnownHost }` | `{ <identity> <known-hosts> {} }` |
| lojix-write-configuration | `ConfigurationWriteRequest.{ … }` | `{ … }` |
| lojix, opening a watch (reply) | `Watching.{ <token> <seq> }` | `DeploymentsWatched.{ <token> <seq> }` |
| lojix, event-log query | `Query.ByEventLog.{ a b }` | `QueryDeploymentEvents.{ a b }` |
| lojix, test-run query | `Query.ByTestRun.{ c n o }` | `QueryTestRuns.{ c n o }` |
| lojix | `WatchCacheRetention.{ … }` | removed |
| replies holding a deployment record or a phase event | marker `{ s d }` | `{ { s d } }` |
| a store failure | no reply | `Refused.Store.«…»` |

**CriomOS at origin/main (cee786a)**, found by grep; CriomOS-home (018691de) holds none of these:
- `modules/nixos/lojix.nix:45` and `checks/lojix-nexus-service/default.nix:54-55` send `ConfigurationWriteRequest.{…}`.
- `modules/nixos/lojix.nix:267` and `checks/lojix-nexus-service/default.nix:73` run `lojix-reset-store ResetStore`.
- `modules/nixos/harness-update.nix:106` matches `Watching.*` when a watch opens. It must read `DeploymentsWatched.*` when CriomOS pins this Lojix.
- README.md:33, docs/GUIDELINES.md:271-277 and ARCHITECTURE.md:235 describe `BootstrapRun.{…}`, `SshPolicy.{… RequireKnownHost}` and `(ResetStore)`.

These CriomOS texts are unchanged: `Query.ByNode.{ … }`, `Deploy.UserEnvironment.{ … }`, the `DeployAccepted.{ N` grep, and the `DeploymentPhaseObserved.{ $identifier …Some.Succeeded` globs.

## Gates

Each gate ran in the foreground with `nix-fast-build --remote li@prometheus.goldragon.criome --no-nom --no-download --eval-workers 1`.

| repository | head | result | log |
|---|---|---|---|
| meta-signal-lojix | 4e42269 | 10 of 10 green | `$S/s5/gate-meta-4e42269.log` |
| lojix | 4b2c50f | 18 of 18 green, the four NixOS VM checks included | `$S/s5/gate-lojix-4b2c50f.log` |
| lojix | 26caf36 | 18 of 18 green | `$S/s5/gate-lojix-26caf36.log` |

**A failure outside the gate (Observed).** `cargo test --workspace` on the builder fails two tests in `tools/tests/nexus_configuration.rs` with `LegacyFileLacksSchema`. They fail identically at the base 316422f. The flake's `test` check builds only the root crate, so the gate does not run them. Every other test binary passes: `$S/s5/test4.log`.

## A/B proof

**The copy (Observed).**
- The live store is `/var/lib/lojix/lojix.memory`, used by `lojix.service` (0.10.6, `/nix/store/m8gfpy8i…-lojix-0.10.6`, running as li).
- As root, I hashed it, copied it and hashed both. The source before, the copy and the source after are all `553b8b9e…`.
- The service was not touched. Proof: `$S/ab/copy-proof.txt`.

**A repair both runs start from (Observed).**
- The copy was taken while the service held the file open, so redb marks it as needing repair. The read-only inspector refuses it ("repair aborted").
- I repaired it once with a scratch redb 4.1.0 probe on the builder. The result, R, is `814dff1d…`.
- The 0.10.6 and the branch inspectors read R identically: schema v5, 12 tables, deploy-job and test-run empty, 4 quarantined rows.
- Because no deploy job is in flight, nothing resumes.

**The runs.**
- Each daemon served its own copy of R, under bubblewrap.
- In that namespace `/run/lojix` and `/var/lib/lojix` were scratch directories. Both daemons announced `/run/lojix/ordinary.sock` and `/run/lojix/meta.sock` inside it, so the live sockets were never reachable.
- The same 26 inputs went to each. Only reads were sent: no deploy, no test, no Configure.
- Transcripts: `$S/ab/A/replies.txt` (0.10.6) and `$S/ab/B/replies.txt` (branch). Harness: `$S/ab/tools/session.sh`. Inputs: `$S/ab/inputs.txt`.

| input | 0.10.6 | branch |
|---|---|---|
| `Query.ByNode.{ goldragon ouranos None }`, sent first and last | Queried, `{ 13974 13974 }` | the same after marker braces (29 markers) |
| `Query.ByNode.{ goldragon ouranos Some.CompleteHost }` | Queried | the same after marker braces |
| `Query.ByNode.{ goldragon nosuchnode None }` | `Queried.{ [] [] { 13974 13974 } }` | byte-equal |
| `Query.ByNode.{ fixture-cluster fixture-node None }` | empty Queried | byte-equal |
| `Query.ByGeneration.{ 578 }` | Queried | the same after marker braces |
| `Query.ByGeneration.{ 999999 }` | empty | byte-equal |
| `Query.ByDeployment.{ 578 }` and `{ 1 }` | Queried | the same after marker braces |
| `Query.ByDeployment.{ 999999 }` | empty | byte-equal |
| `Query.ByEventLog.{ 1 4 }`, `{ 2015 2018 }`, `{ 5000 5001 }` | DeploymentEventsQueried | refused by the client: `Variant { expected: "Selection", found: "ByEventLog" }` |
| `QueryDeploymentEvents.{ … }`, the same three ranges | refused by the client: `expected: "Query"` | equal to 0.10.6's ByEventLog after marker braces; the empty range is byte-equal |
| `Query.ByTestRun.{ goldragon ouranos None }` | `TestRunsQueried.{ [] { 13974 13974 } }` | refused by the client |
| `QueryTestRuns.{ goldragon ouranos None }` | refused by the client | byte-equal to 0.10.6's ByTestRun |
| `WatchDeployments.{ None None None }`, then Unwatch | `Watching.{ 1 13974 }`, `Unwatched.{ 1 }` | `DeploymentsWatched.{ 1 13974 }`, `Unwatched.{ 1 }` |
| `WatchDeployments.{ None Some.goldragon Some.ouranos }`, then Unwatch | `Watching.{ 2 13974 }`, `Unwatched.{ 2 }` | `DeploymentsWatched.{ 2 13974 }`, `Unwatched.{ 2 }` |
| `WatchCacheRetention.{ None None }` | `Watching.{ 3 13974 }`; its Unwatch is `SubscriptionAlreadyClosed 3` | refused by the client: `expected: "Input"` |
| `Unwatch.{ 999 }` | `UnwatchRejected.{ SubscriptionTokenUnknown 999 }` | byte-equal |
| meta `Pin.{ goldragon ouranos 999999 abprobe }` | `PinRejected.{ GenerationUnknown { 13974 13974 } }` | byte-equal |
| meta `Unpin.{ goldragon ouranos abprobe }` | `UnpinRejected.{ PinLabelUnknown … }` | byte-equal |
| meta `Retire.{ goldragon ouranos 999999 }` and `{ goldragon nosuchnode 578 }` | `RetireRejected.{ GenerationUnknown … }` | byte-equal |

Every difference is one of the wire changes listed in the tool-text table. Normalizing `{ { s d } }` to `{ s d }` and `DeploymentsWatched.` to `Watching.` makes every paired reply byte-equal. No store failure occurred, so neither daemon answered `Refused`. Both daemon logs hold only the two `DeploymentWatchEnded` lines.

**The store after the runs (Observed).**
- **No commit.** The marker is `{ 13974 13974 }` at the first and at the last query in both runs.
- **The branch did exactly what 0.10.6 did to the file.** The final files of the two runs are byte-identical, `a9edc931…`. Neither equals R.
- **Why neither equals R.** redb rewrites bytes on every read-write open and close. The control: opening and closing R three times with the redb probe alone gave three different hashes, at the same size.
- **So byte identity with R holds for no read-write opener, 0.10.6 included.** The proof is instead the A=B equality above, together with the content check below.
- **Content check.** A repaired copy of the final file reads, in both inspectors, identically to R: schema v5 with no upgrade, the same 12 tables, the same row counts and the same 4 quarantined rows. Files: `$S/ab/inspect-R-old.txt` and `$S/ab/inspect-F-*.txt`.
- **Hashes:** `$S/ab/hashes.txt`. I deleted every store copy afterwards, here and on the builder.

**Crossed versions are not refused (Observed).**
- Transcripts: `$S/ab/XN/replies.txt` (old clients, branch daemon) and `$S/ab/XO/replies.txt` (branch clients, old daemon).
- **Old clients against the branch daemon.** The replies misdecode silently:
  - `Query.ByNode…` prints `TestRunsQueried.{ [] { 4294967287 13974 } }`;
  - meta `Pin.{…}` prints `Tested.{ 3577344 { 3577344 0 } }`;
  - `Unwatch.{ 999 }` prints nothing and exits 0.
- **Branch clients against the old daemon.** They get no reply: `structural wire conversion failed`, exit 2. `Unwatch` prints nothing and exits 0.
- signal 8.0.0 has no contract greeting, so the daemon and every client must move together. A host's own package does that. A client built separately would not.

## Needs a ruling

1. **horizon-lib under 29: five one-variant enums.**
   - `MotherBoard.[ Ondyfaind ]`, `DomainProvider.[ Cloudflare ]`, `SiteRenderer.[ MarkdownStatic ]` and `PersonaCapability.[ GitoliteServer ]` are domain enumerations with one member today. Reshaping any of them removes a word from the cluster-definition text and changes `HorizonDefinition`'s archive. Lojix stores that archive inside deploy jobs and configuration test defaults.
   - `CompositionCommand.[ Compose.CompositionRequest ]` becomes `CompositionRequest` by the rule, which changes horizon-compose's text (`Compose.{ … }` to `{ … }`). Lojix's flake fixture and CriomOS both use that text.
   - Should these become a second variant, the payload type, or something else?
2. **signal-lojix `Refusal.[ Store.String ]`.**
   - It could become `Refused.Refusal` with `Refusal.String` (text `Refused.«…»`), or a newtype with a store-naming name, or some other shape.
   - signal-orchestrate's `Refusal` and meta-signal-flow's `StoreRefusal` have the same shape, so one ruling serves all three.
   - meta-signal-lojix imports `Refusal`, so it moves with it.
3. **The unit reading in step 2.** `ResetStore.{}` and `RequireKnownHost.{}` were my assumption, stated above.

## Notes

- The lock still holds ethos-zero 16 (c2653dd) and datom-codec 0.32.2, only through the `signal` 8.0.0 frames crate.
- The meta-signal-lojix, signal-lojix and horizon-lib pins in lojix are branch commits. When those branches merge, the merge must keep these revisions reachable.
- Worktrees: `$S/wt/{lojix,meta-signal-lojix,…}`. Builder copies: `/tmp/offload/{lojix,meta-signal-lojix,redb-repair}`.
