# Nexus-for-lojix completeness audit

The lens: intent record `z6qu` (VeryHigh, psyche 2026-06-05) makes the Nexus
schema the engine's INTERNAL FEATURE INTERFACE whose MAIN reason for existing
is VISIBILITY — *"Every engine feature — any computation, any filtering or
condition on results, any conditional write, any internal logic-feature — MUST
be defined as a Nexus interface verb + object in the schema ... Internal
features must not live as inline hand-written logic hidden from the schema."*
The nexus schema is the readable catalog of everything the engine can do
internally.

This audit reads `schema/nexus.schema` against what `src/schema_runtime.rs`
actually routes, and against the functionality inventory drawn from the two
wire contracts (`signal-lojix`, `meta-signal-lojix`), `lojix/ARCHITECTURE.md`,
and the legacy Stack-A reference (`lojix-cli/src/*.rs`). The discrepancy
between declared-in-schema and routed-inline-in-Rust is the key finding.

## What the nexus schema declares today

The catalog at `schema/nexus.schema:48-76`:

- `SignalInput` / `SignalOutput` — the two-leg ingress/egress unions
  (Ordinary + Meta).
- `EffectCommand` — six variants: `ResolveFlakeAuth`, `NixEval`, `NixBuild`,
  `CopyClosure`, `ActivateGeneration`, `PathInfoGc`.
- `EffectResult` — seven variants: `FlakeResolved`, `ClosureEvaluated`,
  `ClosureBuilt`, `ClosureCopied`, `GenerationActivated`, `PathsCollected`,
  `EffectFailed`.
- `EffectStage` — `FlakeAuth Eval Build CopyClosure Activate Gc`.
- `NexusWork` — `SignalArrived`, `SemaReadCompleted`, `SemaWriteCompleted`,
  `EffectCompleted`.
- `NexusAction` — `CommandSemaRead`, `CommandSemaWrite`, `CommandEffect`,
  `ReplyToSignal`, `Continue`.

The deploy pipeline IS the `EffectCommand` catalog, and the re-entry protocol
(`SignalArrived -> Command* -> Continue`) IS the `NexusWork`/`NexusAction`
pair. That much is correctly schema-declared. The gaps are about features the
engine *performs* that have no verb/object, and stages that are *collapsed*
inside Rust instead of expressed as distinct NexusActions.

## (1) External operations: are all contract Input roots reachable?

Mostly yes. The mapping (verified against `decide_signal_arrival` /
`decide_ordinary_input` / `decide_meta_input`, `schema_runtime.rs:247-317`):

| Contract Input root | Reaches NexusAction | Status |
|---|---|---|
| ordinary `Query` | `CommandSemaRead(QueryGenerations)` | reachable |
| ordinary `CheckHostKeyMaterial` | `CommandSemaRead(CheckKeyMaterial)` | reachable but stubbed (see Gap E) |
| ordinary `WatchDeployments` / `WatchCacheRetention` | inline `open_subscription` -> `ReplyToSignal` | NOT schema-declared (Gap A) |
| ordinary `Unwatch` | inline `close_subscription` -> `ReplyToSignal` | NOT schema-declared (Gap A) |
| meta `Deploy` | `CommandSemaWrite(RecordDeploySubmitted)` then effect chain | reachable |
| meta `Pin` / `Unpin` / `Retire` | `CommandSemaWrite(Pin/Unpin/Retire Generation)` | reachable |

Two contract operations have no internal Nexus expression at all.

### Gap A — subscription handshake is an inline engine feature, not a Nexus verb

`open_subscription` (`schema_runtime.rs:269-284`) and `close_subscription`
(`286-290`) are real engine logic: they mint a subscription token from
`StoreState::next_subscription_token`, read `commit_sequence`, branch on a
poisoned-lock error to emit `StreamUnavailable`, and build the
`SubscriptionOpened` / `SubscriptionClosed` reply. Per `z6qu` this is
"computation" plus a "condition on results" plus a token mint — it MUST be a
declared Nexus verb+object, but it is hand-written and invisible to the
schema. The engine reaches `ReplyToSignal` directly without any
`NexusWork`/`NexusAction` token-state object.

Recommendation: declare a subscription plane in the nexus schema. Minimum:
- `NexusAction` gains `OpenSubscription SubscriptionOpenRequest` and
  `CloseSubscription SubscriptionCloseRequest`, OR
- a `SubscriptionRegistry` SEMA table (subscription tokens are durable
  registry state, not transient) with `SemaWriteInput::RegisterSubscription`
  / `RetireSubscription` and the matching read for an event-replay cursor.

The token mint is a `next_subscription_token()` counter on `StoreState` — it
is durable-ish state, so the SEMA-write framing is the more honest one and it
plugs into the same `NexusWork::SemaWriteCompleted` re-entry the deploy
pipeline already uses. Either way the verb must exist; today it does not.

### Gap B — `ReadEventLog` is a real SEMA read with no ordinary Input verb

`SemaReadInput::ReadEventLog` (`sema.schema:48`) and `read_event_log`
(`schema_runtime.rs:874-897`) are fully implemented — range filter, deployment
vs retention partition, container-event skip — but NO ordinary contract Input
root reaches it. `decide_ordinary_input` only routes `Query` and
`CheckHostKeyMaterial`; there is no `ReadEventLog` ordinary verb. Worse, when a
`ReadEventLog` completion arrives at `decide_read_completion`
(`schema_runtime.rs:329-331`) the engine treats `EventLogRead` as an ERROR and
replies `QueryRejected(MalformedSelector)`. So a declared, implemented SEMA
read is unreachable from the wire and is wired to fail if it ever fires.

This is the streaming-handshake follow-on (`signal-lojix.lib.schema:11-20`):
the contract carries the Watch/Unwatch handshake but no poll verb, yet the
SEMA layer already supports the poll. The port plan (§GAP, report 25/3:294-303)
says the daemon "can ANSWER a `ReadEventLog` poll" — but it structurally
cannot, because no ordinary Input variant carries an `EventLogRange` to a
`CommandSemaRead(ReadEventLog)`. Recommendation: add an ordinary `ReadEvents`
verb to `signal-lojix` (payload `EventLogRange`, reply the `EventLogPage`
shape) and route it; then `decide_read_completion` handles `EventLogRead` as a
success reply rather than a malformed-selector rejection.

## (2) Internal effects: is every pipeline stage a declared EffectCommand?

The six `EffectCommand` variants each have a matching `run_*` arm in
`run_effect` (`schema_runtime.rs:1167-1178`) and a matching `EffectResult`.
That 1:1 EffectCommand/EffectResult pairing is clean. But the legacy reference
shows the deploy pipeline has more *distinct* stages than six, and the rewrite
has COLLAPSED several real operations into the inside of single effect arms,
hiding them from the catalog.

### Gap C — remote input staging (rsync of generated flake inputs) is missing entirely

Legacy `stage.rs` (`RemoteInputStage`) is a whole pipeline stage: before a
remote build it `mkdir -p`s a remote input root and `rsync -a --delete`s the
materialized horizon/system/deployment/secrets directories to the builder, so
the build's `--override-input` flake refs resolve on the builder. Legacy
`deploy.rs:124-131` runs this stage whenever a builder target is set. The
nexus catalog has NO verb for it. `NixBuild` with `BuildTarget::Remote`
(`schema_runtime.rs:951-953`) just wraps `nix build` in `--builders
ssh-ng://<builder>` and never stages the override inputs — so a remote build of
a flake that depends on the locally-generated horizon/secrets inputs would fail
to resolve them. This is a missing feature, not just a missing verb.

Recommendation: declare `EffectCommand::StageRemoteInputs StageInputsCommand`
(payload: builder node, the generated-input directories + their nar-hashes)
with `EffectResult::RemoteInputsStaged` and an `EffectStage::StageInputs`.
Note this also implies the artifact-materialization step (Gap D) feeds it.

### Gap D — artifact materialization (the `nix flake` override-input generation) is missing entirely

Legacy `artifact.rs` (`ArtifactMaterialization::materialize`) is the stage that
writes the horizon.json + flake.nix templates into `~/.cache/lojix/...`,
computes each directory's `nix hash path --sri` nar-hash, and produces the
`FlakeInputRef`s the build consumes via `--override-input`. The rewrite's
`NixEval` (`run_nix_eval`, `schema_runtime.rs:933-942`) just evals a bare
`flake#attribute.drvPath` with NO override inputs — there is no materialization
verb, no nar-hash computation, no override-input plumbing. The whole
horizon-projection-to-flake-input bridge (the core of how Stack A injects
cluster data into the build) is absent from both the schema AND the runtime.

This is the largest functionality hole. The legacy deploy is fundamentally
"project horizon -> materialize 2-4 flake-input dirs -> build with those as
`--override-input`s." The rewrite's `NixEvalCommand` carries `flake` +
`attribute` only (`nexus.schema:57`) — no input refs. Recommendation: declare
`EffectCommand::MaterializeArtifact MaterializeCommand` (payload: cluster,
node, proposal source, deployment shape) ->
`EffectResult::ArtifactMaterialized` carrying the typed input refs; thread
those refs into `NixEvalCommand` / `NixBuildCommand` as a
`(Vec OverrideInput)` field. Without this the rewrite cannot actually build a
CriomOS closure — it only models the shape of one. (This connects to the
raw/pretty horizon split `9p8v`/`avvh` and `a2t4` minimal-horizon: the
materialization stage is exactly where projected horizon data enters the
build, and it is the seam where pretty-horizon output becomes flake inputs.)

### Gap E — `CheckHostKeyMaterial` is a no-op stub, not the real publication diff

`check_key_material` (`schema_runtime.rs:899-906`) always returns
`mismatches: Vec::new()` — it never sshes to the host, never reads
`/etc/criomOS/complex/publication.nota`, never projects horizon, never diffs
ssh/yggdrasil keys. The legacy `check.rs` is ~250 lines of real diff logic
(`collect_publication`, `parse_publication`, `diff` against horizon's expected
ssh/ygg material). The rewrite declares the verb and routes it but the engine
feature behind it is empty. The real check is fundamentally an EFFECT (it sshes
to a host and parses a remote file) — yet it is routed as a SEMA READ
(`CommandSemaRead(CheckKeyMaterial)`), which is wrong: SEMA reads are durable
state observations, not remote IO. Per `z6qu` the diff computation must be a
declared internal feature. Recommendation: re-route as
`EffectCommand::CheckHostKeyMaterial` ->
`EffectResult::HostKeyMaterialChecked` (it does remote ssh + parse, like the
other effects), and declare an `EffectStage::KeyMaterialCheck`. Leaving it as a
SEMA read both mis-categorizes the operation and leaves the real feature
unbuilt.

### Gap F — GitHub-authenticated flake input resolution (intent `2qhw`) is absent

Intent `2qhw` (High) gives lojix-daemon explicit scope to handle
GitHub-authenticated Nix flake input resolution: *"an authenticated wrapper
around the relevant Nix invocation that fetches the user GitHub API key from
gopass and injects it into the Nix call (likely via NIX_CONFIG
access-tokens)."* `ResolveFlakeAuth` (`run_flake_auth`,
`schema_runtime.rs:918-931`) only runs `nix flake metadata --json` and reads
the resolved revision — it does NOT fetch a token or inject access-tokens. The
verb NAME suggests auth but the feature is just metadata resolution. Either the
`ResolveFlakeAuth` effect must actually fetch+inject the gopass GitHub token
(and the schema should carry that as an explicit field/sub-object so the
feature is visible), or a distinct `EffectCommand::InjectFlakeAuthToken` should
be declared. As-is, the catalog implies an auth feature that does not exist —
which is the inverse of the `z6qu` discipline (the verb is in the schema but the
feature is not in the engine).

### Gap G — `PathInfoGc` does not do path-info reachability or two-phase TTL deletion

`ARCHITECTURE.md:53-55` and the port plan (25/3:212-213) specify GC as
"`nix path-info -r` + two-phase GC respecting narinfo TTL." `run_path_info_gc`
(`schema_runtime.rs:999-1008`) just runs `ssh <node> nix-store --gc` and counts
output lines. No `path-info -r` closure introspection, no narinfo-TTL grace, no
two-phase deletion, no consultation of the `recent/<timestamp>` short-grace
slot. The verb name (`PathInfoGc`) advertises path-info introspection the
engine does not perform. Recommendation: either split into
`EffectCommand::IntrospectClosure` (path-info -r) +
`EffectCommand::CollectGarbage` (the actual gc respecting the gc-roots
retention slots), or carry the retention policy in the `PathInfoGcCommand`
payload so the feature is visible. The current `GcRoot.label`/`GenerationSlot`
SEMA model (`sema.schema:74-75`) exists but the GC effect never reads it — the
retention tree is declared but inert.

## (3) Functionality items missing from / only implied in the catalog

Inventory cross-check (legacy reference + ARCHITECTURE + contracts), beyond the
gaps above:

- **Container lifecycle observation (systemd dbus).** `ARCHITECTURE.md:60-62`
  and `INTENT` name systemd dbus subscriptions for `containers.<name>.service`
  transitions, mirrored into the event log. The SEMA layer is fully built:
  `RecordContainerTransition` write, `ContainerLifecycleTable`,
  `ContainerLifecycleRecord`, `ContainerState` enum
  (`sema.schema:53,56-58,81-82`; `record_container_transition`
  `schema_runtime.rs:777-804`). But there is NO Nexus verb and NO ingress that
  ever PRODUCES a container transition — no `EffectCommand` watches dbus, no
  `SignalInput` carries a container event. The write path exists with no
  caller. This is the inverse-of-`z6qu` again: durable state with no declared
  feature that drives it. The daemon cannot observe a container without a dbus
  effect; recommend `EffectCommand::ObserveContainerLifecycle` (or a
  push-source effect) feeding `RecordContainerTransition`, OR explicitly mark
  the container plane as a carried-not-built follow-on in the schema comment so
  it is not mistaken for complete.

- **Cache-retention transitions never emitted.** `LoggedEvent::CacheRetention`
  and `CacheRetentionTransitionEvent` are declared (`sema.schema:79`,
  `signal-lojix.lib.schema:101-111`) and `read_event_log` partitions them out
  (`schema_runtime.rs:888`), but NOTHING ever writes a `CacheRetention` log
  entry. Pin/Unpin/Retire mutate `gc_roots` slots
  (`schema_runtime.rs:685-775`) but emit NO retention event into the event log
  — so a `WatchCacheRetention` subscriber would see nothing even after the push
  follow-on lands. The pin/unpin/retire writes should also append a
  `CacheRetention` event (a conditional write per `z6qu`), and that
  log-append should be a visible part of the verb, not silently absent.

- **Home deployment activation modes (`HomeMode` Build/Profile/Activate).**
  The meta contract carries `HomeMode` (`meta-signal-lojix.lib.schema:74,95`)
  and `HomeDeployment`. But `DeployPipeline::from_submission`
  (`schema_runtime.rs:92-106`) hard-codes home deploys to
  `ActivationKind::Switch` and drops `HomeMode` entirely. Legacy `activate.rs`
  `HomeActivation` distinguishes Build (no-op) / Profile (set home-manager
  profile) / Activate (profile + run activate). The rewrite collapses all three
  into one Switch activation against the SYSTEM profile via
  `run_activate_generation` (`schema_runtime.rs:975-988`), which runs
  `nix-env -p /nix/var/nix/profiles/system` — i.e. it would activate a home
  closure as a SYSTEM generation. There is no home-vs-system branch in the
  activate effect and no `HomeMode` in the `ActivateGenerationCommand`
  (`nexus.schema:60`). Recommendation: carry the home/system distinction and
  `HomeMode` in `ActivateGenerationCommand` so the activate feature is
  visible, and add the home-profile activation arm.

- **`SystemAction::Eval` (build-stops-at-derivation) has no terminal path.**
  Legacy `BuildPlan::nix_operation` returns `EvalDrvPath` for `Eval`, and
  `finish_deploy` returns `DeployOutcome::Evaluated` WITHOUT copy/activate. In
  the rewrite, `system_activation_kind` (`schema_runtime.rs:115-117`) maps
  `Eval` (and `Build`, and `Switch`) all to `ActivationKind::Switch`, so an
  `Eval`-only request would still run the full copy+activate chain. The
  "evaluate only, no closure realization" and "build only, no activation"
  early-exit branches from legacy `build.rs:26-35` (`produces_closure` /
  `activates`) are gone. The pipeline always runs all stages. Recommendation:
  the `DeployStage` cursor (or a `DeployMode` carried on the pipeline) must
  encode stop-after-eval and stop-after-build, and the early-terminal reply
  must be a declared outcome.

- **EFI bootloader reconcile + BootOnce transient-unit activation.** Legacy
  `activate.rs` `SystemActivation` has substantial logic: `requires_efi_reconcile`
  (set `LoaderEntryDefault`, clear oneshot for Boot/Switch),
  `boot_once_script` + `systemd_run_invocation` (the transient-unit BootOnce
  path that survives ssh drop). The rewrite's `run_activate_generation` runs a
  single `nix-env --set` ssh call regardless of `ActivationKind` —
  `activation_slot` (`schema_runtime.rs:990-997`) maps the kind only to a
  GenerationSlot, never changing the ssh invocation. BootOnce and Boot/Switch
  produce identical IO. Intent `xv9v` (Prometheus uses BootOnce until
  out-of-band access) makes BootOnce a load-bearing real feature, not a
  nicety. Recommendation: `ActivateGenerationCommand` must drive distinct
  activation IO per `ActivationKind`, and the BootOnce transient-unit + EFI
  reconcile are distinct internal features that should be visible (sub-steps of
  the activate effect, or their own effect variants).

## (4) Redundancies / verbs without real functionality

- `ResolveFlakeAuth` — the name claims auth; the implementation is metadata
  resolution only (Gap F). The verb is half-real.
- `PathInfoGc` — the name claims path-info introspection; the implementation
  is a bare `nix-store --gc` (Gap G). The verb is half-real.
- No purely-redundant verb (every EffectCommand has exactly one EffectResult
  and one run-arm). The problem is the opposite direction: verbs whose declared
  scope exceeds the engine's actual feature, plus engine features (Gaps A, the
  pin-retention-event append, container observation) with NO verb.

## (5) Does SignalArrived -> Command* -> Continue express the FULL pipeline?

Partially. The chain is real and the continuation re-entry works
(`decide_write_completion` / `advance_after_phase` / `decide_effect_completion`,
`schema_runtime.rs:355-526`). But two structural collapses hide stages:

- **The phase-transition write is used as a control-flow trampoline, not a
  declared stage sequence.** `advance_after_phase` (`schema_runtime.rs:388-421`)
  switches on a private `DeployStage` enum (`Submitted` / `BuildingRecorded` /
  `CopyingRecorded` / `ActivatedRecorded`) that lives ONLY in Rust
  (`schema_runtime.rs:56-67`), not in the schema. The actual stage machine — the
  ordering of effects, which phase each emits, when the chain ends — is
  invisible to the nexus catalog. Per `z6qu` the pipeline's stage sequencing is
  the engine's central internal logic-feature and should be a declared object
  (e.g. a `DeployStage` NexusWork/Action sub-object or a schema-declared
  `PipelineCursor`), not a hand-rolled private enum. A reader of
  `nexus.schema` cannot see that Build is recorded between Eval and Copy, or
  that Activated triggers the live-set commit — those orderings are pure Rust.

- **Stages are collapsed (per Gaps C/D/E):** materialize-artifact,
  stage-remote-inputs, and the real key-material check are absent, so the
  schema's pipeline is a 6-step abstraction of a legacy ~10-step pipeline. The
  re-entry protocol expresses the stages that ARE declared correctly; it just
  declares too few.

## Precise gap list (for the synthesis agent)

1. **Gap A — subscription handshake.** `open_subscription` /
   `close_subscription` are inline engine features (token mint + conditional
   reply). Declare them as Nexus/SEMA verbs (recommend a `SubscriptionRegistry`
   SEMA table with `RegisterSubscription` / `RetireSubscription` writes).
2. **Gap B — `ReadEventLog` unreachable + mis-handled.** SEMA read is built but
   no ordinary Input verb reaches it, and `decide_read_completion` treats its
   completion as a malformed-selector error. Add an ordinary `ReadEvents` verb
   (payload `EventLogRange`); handle `EventLogRead` as success.
3. **Gap C — remote input staging missing.** No verb for the rsync-override-
   inputs-to-builder stage. Declare `EffectCommand::StageRemoteInputs`.
4. **Gap D — artifact materialization missing (largest hole).** No verb for
   horizon-projection -> flake.nix/horizon.json templates -> nar-hash ->
   `--override-input` refs. Declare `EffectCommand::MaterializeArtifact` and
   thread `OverrideInput` refs into `NixEvalCommand`/`NixBuildCommand`. Without
   this the rewrite cannot build a real CriomOS closure.
5. **Gap E — `CheckHostKeyMaterial` is a no-op stub AND mis-categorized.** It is
   routed as a SEMA read but is real remote ssh+parse IO. Re-route as an
   `EffectCommand` and build the publication diff.
6. **Gap F — GitHub-auth flake resolution (intent `2qhw`) absent.**
   `ResolveFlakeAuth` does not fetch/inject the gopass GitHub token. Make the
   token-injection a visible declared feature.
7. **Gap G — `PathInfoGc` does no path-info / two-phase TTL / retention-slot
   reading.** The declared GC-roots retention tree (`GcRoot`/`GenerationSlot`)
   is inert. Make GC consume it; consider splitting introspect vs collect.
8. **Container lifecycle: write path with no producer.** SEMA fully built; no
   Nexus verb / ingress ever emits a transition. Declare a dbus-observe effect
   or mark explicitly as follow-on.
9. **Cache-retention events never emitted.** Pin/Unpin/Retire mutate slots but
   append no `CacheRetention` log entry; the conditional log-append should be
   part of those verbs.
10. **`HomeMode` Build/Profile/Activate collapsed to system Switch.** Home
    closures would activate against the system profile. Carry home/system +
    `HomeMode` in `ActivateGenerationCommand`.
11. **`SystemAction::Eval`/`Build` early-exit branches dropped.** Eval-only and
    build-only requests run the full copy+activate chain. Encode stop-after-eval
    / stop-after-build in the pipeline cursor as a declared outcome.
12. **BootOnce + EFI-reconcile activation collapsed.** All `ActivationKind`s
    produce identical activate IO. Intent `xv9v` makes BootOnce load-bearing.
    Drive distinct IO per kind; surface the transient-unit + EFI sub-steps.
13. **The deploy stage machine is a private Rust enum (`DeployStage`), invisible
    to the schema.** Per `z6qu` the pipeline sequencing — the engine's central
    logic-feature — must be schema-declared, not hand-rolled in
    `schema_runtime.rs:56-67`.

## Bottom line

The schema correctly declares the SHAPE of the pipeline (six effects, the
re-entry protocol, the four SEMA tables) and routes them faithfully. But
against `z6qu` it FAILS the visibility test on three counts: (a) real engine
features that have NO verb (subscription handshake, container observation,
cache-retention log-append, the deploy stage machine itself); (b) declared
verbs whose engine feature is empty or smaller than the name implies
(`CheckHostKeyMaterial` stub, `ResolveFlakeAuth` no-auth, `PathInfoGc`
no-path-info); and (c) entire legacy pipeline stages collapsed out
(materialize-artifact and remote-input-staging — the two stages that actually
inject cluster data into the build — plus HomeMode and the Eval/Build
early-exits). The materialization gap (D) is the one that makes the current
rewrite unable to build a real closure rather than merely incomplete in
catalog terms. The fix direction is uniform: every one of these is a
hand-written-or-absent feature that `z6qu` says must become a declared Nexus
verb+object visible in `schema/nexus.schema`.
