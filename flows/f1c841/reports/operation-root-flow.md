# The Operation root in the Flow Nexus

Subflow of f1c841. flow 0.20.0 on main at `f7230f81` (parent `4f3670ef`, flow
0.19.0). The Operation root compiles in a running Nexus for the first time:
flow-nexus carries `ethos/operation.ethos`, its build script generates it with
ethos-zero 16.0.0 and fails when the committed module is stale, and every
effect of the Nexus's launch, stop, retire and record paths is one generated
`Operation`. `RunningNexus` performs them through the `Performs` trait, and
one generated `Outcome` answers each. Wire unchanged (signal-flow 8.0.0,
meta-signal-flow 12.0.0), storage unchanged, nothing deployed.

## The ethos file, verbatim

`crates/flow-nexus/ethos/operation.ethos`. It is named `operation` after the
root's head, which is what the living calls the root.

```
; Flow Nexus Operation: what the Nexus does. Every effect its launch and
; record paths perform is one operation, and each is answered by one
; Outcome. An effect changes something: Herdr's panes, a harness, the
; launch bundle copies, or the store. A read of the world (a pane's
; presence, a transcript receipt, a skill catalog) is not an operation.
;
; Compose writes the per-launch bundle copy and composes the first prompt.
; Reserve opens the launch attempt in the journal. Record writes one
; journal or lifecycle entry. Register binds a flow's row and role.
; Confirm makes a Pending launch Active and answers Started. Open makes
; the launch pane; Spawn starts the native harness in it; Bind claims the
; flow's identity from the harness's integration report; Title names the
; claimed flow; Submit types the first prompt once; Continue types the
; brief continuation; Close closes a flow's pane; Prune removes a launch's
; bundle copy.
;
; LaunchOutcome and Replacement are the store's own types, imported from
; the Nexus crate until the Memory root is compiled.

Operation
[ signal_flow:[ FlowId LaunchRequestId FlowNode Caller LaunchProfile ComposedLaunch OriginClue LaunchAttemptReservation HerdrPaneBinding NativeLaunchIntent NativeLaunchBinding RegistrationAcknowledgement PromptDeliveryIntent PromptDeliveryResult Started ]
  flow_nexus:[ LaunchOutcome Replacement ] ]
[ Compose.LaunchProfile
  Reserve.{ ComposedLaunch OriginClue }
  Record.[ Intent.NativeLaunchIntent
           Binding.NativeLaunchBinding
           Acknowledgement.RegistrationAcknowledgement
           Delivery.PromptDeliveryIntent
           Delivered.PromptDeliveryResult
           Active.FlowId
           Stopped.FlowId
           Retired.FlowId
           Exited.FlowId
           Replacing.Replacement
           Withdrawn.LaunchRequestId
           Settled.{ LaunchRequestId LaunchOutcome } ]
  Register.{ FlowNode Caller }
  Confirm.FlowId
  Open.ComposedLaunch
  Spawn.PaneLaunch
  Bind.PaneLaunch
  Title.{ ComposedLaunch NativeLaunchBinding }
  Submit.{ ComposedLaunch PromptDeliveryIntent }
  Continue.FlowId
  Close.FlowNode
  Prune.LaunchRequestId ]
[ Composed.ComposedLaunch
  Reserved.LaunchAttemptReservation
  Recorded
  Registered.FlowNode
  Started.Started
  Opened.HerdrPaneBinding
  Spawned
  Bound.NativeLaunchBinding
  Titled
  Submitted.PromptDeliveryResult
  Continued
  Closed
  Pruned
  Failed.[ CompositionRefused
           StoreRefused
           ConflictingBinding
           Unstarted
           HerdrRefused
           CodexRefused
           BundleRefused ] ]
[ PaneLaunch.{ ComposedLaunch HerdrPaneBinding } ]
```

It follows the shape of the vision-ethos example: imports, operations,
outcomes, types; payloads inline; `PaneLaunch` is named once because Spawn
and Bind both use it. The sketch's `Failed.String` became an inline enum of
named refusals, because vision-nexus says errors are vocabulary, not strings.
The flat import list stays on one line, because none of its elements has a
next layer.

## What each operation maps to

The table shows what each `Performs::perform` arm (in
`crates/flow-nexus/src/performing.rs`) calls, and which call it replaced on
each path.

| Operation | Performs through | Outcome | Replaced call sites |
|---|---|---|---|
| Compose | `LaunchComposer::compose` (writes the Claude bundle copy) | Composed / Failed.CompositionRefused | `start` |
| Reserve | `store.reserve_launch_attempt` | Reserved / Failed.StoreRefused | `start` |
| Record.Intent | `store.record_native_launch_intent` | Recorded / Failed.StoreRefused | `start` |
| Record.Binding | `store.record_native_launch_binding` | same | `start` |
| Record.Acknowledgement | `store.record_registration_acknowledgement` | same | `start` |
| Record.Delivery | `store.record_prompt_delivery_intent` | same | `start` |
| Record.Delivered | `store.record_prompt_delivery_result` | same | `start` (three places), `promote_ambiguous` (two places) |
| Record.Active | `store.record_active` | same | brief continuation, delivery's Presented witness (`delivery.rs`) |
| Record.Stopped | `store.record_stopped` | same | ordinary `Stop`, `reap` |
| Record.Retired | `store.record_retired` | same | meta `Retire` |
| Record.Exited | `store.record_exited` | same | delivery's absent-pane witness (`delivery.rs`) |
| Record.Replacing | `store.record_replacement` | same | `replace` |
| Record.Withdrawn | `store.withdraw_replacement` | same | `settle` |
| Record.Settled | `store.record_launch_outcome` | same | `settle` (two places), `reap` (two places) |
| Register | `store.register_flow_in_role` | Registered / Failed.ConflictingBinding / Failed.StoreRefused | `start` |
| Confirm | `store.confirm_started` (Pending to Active, generation 1) | Started / Failed.Unstarted / Failed.StoreRefused | `start` (two places), `promote_ambiguous`, `resume_reaping` |
| Open | `HerdrCli::create_launch_pane` | Opened / Failed.HerdrRefused | `start` |
| Spawn | `HerdrCli::start_native_harness` | Spawned / Failed.HerdrRefused | `start` |
| Bind | `HerdrCli::observe_native_binding`, which runs the flow-id claim helper | Bound / Failed.HerdrRefused | `start` |
| Title | `HerdrCli::title_native_flow` (Claude session title, or Codex thread name) | Titled / Failed.HerdrRefused | `start` |
| Submit | Codex: `CodexAdapter::submit_bound_codex_first_turn`; Claude: `HerdrCli::submit_first_prompt_once` | Submitted / Failed.CodexRefused or HerdrRefused | `start` |
| Continue | types `BRIEF_CONTINUATION` under the pane lease, and performs Record.Active on a witnessed reaction | Continued / Failed.HerdrRefused | `settle`, `reap` |
| Close | `HerdrCli::close` | Closed / Failed.HerdrRefused | ordinary `Stop` (inside its pane lease), `reap` |
| Prune | `LaunchBundles::remove_for_request` | Pruned / Failed.BundleRefused | `settle`, `prune_launch_bundles_of` (Stop, Retire, reap) |

Every launch rejection the Nexus answers is the same one it answered before.
Each Outcome goes back to the `StartRejection`, `StopRejection`,
`ReplaceRejection` or `RetireRejection` that the call site mapped the old
`Err` or `false` to. Two small changes of order and placement:

- The Codex endpoint check stays before Reserve, so a model no endpoint
  serves is still refused before anything is reserved. Submit now resolves
  the adapter again instead of carrying it from that check. The
  configuration is fixed while the Nexus runs, so the adapter is the same
  one.
- The bundle-copy removal's log line moved into the Prune arm.

## What was replaced

- `launching::ContinuesIntoBrief` (trait and impl) is gone. Its body is the
  Continue arm, and its constant is `Performs::BRIEF_CONTINUATION`.
- `PrunesLaunchBundles::prune_launch_bundle` is gone; pruning one copy is
  `Operation::Prune`. `prune_launch_bundles_of` stays as the loop that reads
  which launches bound a flow and performs one Prune for each.
- `start`, `promote_ambiguous`, `settle`, `replace`, `reap`,
  `resume_reaping`, `Stop`, `Retire` and the two delivery lifecycle witnesses
  no longer call the store, Herdr, the composer or the Codex adapter to
  change anything. They decide, and `perform` acts. New helpers on the
  private `ResumesReplacement` trait: `settled_as`, which builds the
  Record.Settled operation, and `confirmed`, which maps Confirm's Outcome
  to the wire response.
- `store::LaunchOutcome` and `store::Replacement` now derive `Hash`, which
  every generated type requires of what it holds. They are re-exported at
  the crate root, and `extern crate self as flow_nexus;` lets the generated
  module name them `flow_nexus::LaunchOutcome`. Their archives are
  unchanged.
- Build: new `crates/flow-nexus/build.rs` and a build-dependency on
  ethos-zero `0edfc0c332e99e89263d3ec0f8538bca3fcfd44f` (16.0.0, the same
  rev signal-flow 8.0.0 builds with, so Cargo.lock gained one line). The
  generated module sits in `src/generated/`, under
  `#[allow(unexpected_cfgs, clippy::large_enum_variant)]`, because its datom
  derives sit behind a `datom` feature the Nexus does not declare. The
  flake's source filter now keeps `.ethos` files.
- Version: 0.19.0 to 0.20.0. There is no wire, storage or deployment
  change, but public items of the flow-nexus library were removed, which is
  a breaking change for a 0.x crate. The change is recorded in `UPGRADES.md`
  and in a paragraph of `DESIGN.md`.

## Tests

The worktree is `~/wt/github.com/LiGoldragon/flow/operation-f1c841`, with
`CARGO_TARGET_DIR` in the scratchpad.

- `cargo test --workspace`: all green. flow-nexus has 166 lib tests (165
  existing plus 1 new), and every other test binary passes.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`:
  clean. `cargo fmt --all --check`: clean.
- New test `tests::an_operation_is_answered_by_its_own_outcome`, also a
  flake check named `flow-operation-outcomes`. A record of an unknown flow
  answers Failed.StoreRefused. Confirm of an unbound flow answers
  Failed.Unstarted. Record.Exited of a live flow answers Recorded and the
  stored row reads Exited; a second Exited answers Failed.StoreRefused. Seen
  failing once: with the Exited arm wired to `record_stopped`, it failed
  with `left: Stopped right: Exited`; it passed once restored.
- Freshness, seen failing once: renaming `Exited.FlowId` to `Gone.FlowId`
  in the ethos file only made `cargo check -p flow-nexus` fail in the build
  script with `src/generated/operation.rs is stale; regenerate it from
  ethos/operation.ethos`. It built once restored.
- Generation: `ethos-zero 'Check.<abs>/operation.ethos'` answered
  `Checked.`, and `ethos-zero 'Generate.{ <abs>/operation.ethos
  <abs>/src/generated }'` wrote the committed module. The binary was a
  `cargo install` of the 0edfc0c3 rev into the scratchpad.
  `nix build github:LiGoldragon/ethos-zero/0edfc0c3` itself fails in its
  check phase; the later commit `c2653dd8` exists for that offline
  flow-contract test.
- `nix flake check path:<worktree> -L`: all 38 checks passed, exit 0, on
  x86_64-linux (aarch64-linux was omitted as incompatible). This covers
  default, fmt, clippy, no-free-functions, no-inherent-methods and every
  named exact test, including the new flow-operation-outcomes.

## Gaps and proposals

None of the Nexus's launch or record effects failed to fit the sketch, so
nothing was invented. These gaps are for the psyche seat.

1. Every operation shares one Outcome enum. The sketch pairs nothing, so
   the types do not say that Spawn is answered by Spawned and never by
   Composed. Each call site matches its own outcome and treats anything else
   as refused. Signal's queries and responses have the same flat shape.
   Pairing would be written in the operation itself. Proposal only, not
   accepted by ethos-zero 16.0.0:

   ```
   Operation
   [ signal_flow:[ ComposedLaunch HerdrPaneBinding ] ]
   [ Open.{ ComposedLaunch
            Opened.HerdrPaneBinding } ]
   ```

2. Operation has no kind for performing. vision-nexus wants every effect
   dispatched through a trait, but the Operation root generates data only.
   `Performs` is hand-written, and an Operation file cannot declare it,
   because kinds live only in a Library. Its input would be the concrete
   `Operation`, which a capability refuses with `KindWanted`. Proposal,
   undecided, in the Library's kind form:

   ```
   Library
   [ flow_operation:[ Operation Outcome ] ]
   []
   [ Performing.[ perform.{ [ Operation ]
                            [ Outcome ] } ] ]
   []
   ```

3. The Memory root is not compiled. Record.Settled and Record.Replacing
   name the store's own `LaunchOutcome` and `Replacement`. They are imported
   by crate name (`flow_nexus:[ ... ]`) through `extern crate self`, not from
   a Memory module. Once flow's store is a Memory ethos, the import becomes
   that module.
4. Reads are not operations. Pane presence, the transcript receipt, the
   skill catalogs, `accept_registration` (which builds the delivery intent
   from reads) and `validate_registration` are still direct calls. Whether
   "one operation type for every effect" covers observing the world is not
   settled; this change says it does not.
5. Effects not yet expressed, outside tonight's launch and record scope.
   All of them fit the same shape:
   - meta `Deliver` and `Command`, which type into panes, with the delivery
     lease and delivery records in `store::delivery`
   - meta `Configure`, which is a store write
   - `RegisterFlow` and `MetaBindExisting`, which are `register_flow` and
     `register_existing_flow`
   - `ConsumeReset`, which spends a Codex reset credit
   - the Claude daemon's refresh

Proposals for the wire, which signal-flow 8.0.0 does not carry. They were
not changed tonight.

- The sketch's Library has `Voice.[ Psyche.Rank Mind.Rank Field.Rank ]`.
  The wire carries `FlowAspect.[ Psyche Mind Field ]` and
  `PowerLevel.[ High Medium Low UltraLow ]` as two fields: four levels where
  the vision has three ranks.
- The sketch's `FlowId.Integer` is `FlowId.String` on the wire.
- The sketch's `Event.[ Started ToolUsed.String Stopped ]` and
  `Report.{ FlowId Event }` have no wire counterpart. Hooks reach Flow only
  as `QueueTurnEnd`, which is refused. The Nexus records lifecycle states
  (Active, Stopped, Retired, Exited), not harness events. With a wire Event,
  Record would gain one variant.
- The sketch's `Start.{ Voice Capsule }`: the Nexus has no Capsule. The
  place a flow runs is a Herdr pane opened from a `ComposedLaunch`, and Open
  is the operation that stands where Capsule-making will stand. A wire
  Capsule is a proposal for when the semi-sandbox exists:

```
Signal
[]
[ Launch.{ Voice
           Capsule
           Brief.String } ]
[ Launched.FlowId
  Refused.[ NoCapsule
            VoiceBusy.Voice ] ]
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```

## Sources

- flow main `4f3670ef` (0.19.0), and `f7230f81` (0.20.0, this work):
  `crates/flow-nexus/src/{launching,lib,delivery,store,herdr/launch,composition,codex}.rs`.
- ethos-zero `0edfc0c3` (16.0.0) and `c2653dd8`:
  `fixtures/print/flow-operation.ethos`, `tests/generated/flow-operation.rs`,
  `tests/freshness.rs`, `tests/flow_contract.rs`, `ethos-zero.ethos`.
- signal-flow `c297d987` (8.0.0): `build.rs`, `ethos/signal.ethos`,
  `src/lib.rs`, the pattern for freshness at build.
- Skills: vision-ethos, knowledge-ethos, vision-nexus, vision-flow, versioning, testing,
  nix-workflow.
