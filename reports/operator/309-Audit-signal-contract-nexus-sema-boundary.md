# Audit: Signal Contract Nexus/SEMA Boundary

## Scope And Method

This audit checks whether contract repositories are wrongly carrying internal
Nexus/SEMA runtime surfaces instead of only public Signal messaging vocabulary.
I treated the supplied psyche/operator analysis as a hypothesis and verified it
with direct repository evidence.

Method:

- Read the workspace and role instructions requested in the prompt:
  `AGENTS.md`, `ESSENCE.md`, relevant `INTENT.md`, `skills/contract-repo.md`,
  `skills/component-triad.md`, and the Rust discipline files needed for source
  inspection.
- Used `rg` first across contract and component checkouts under
  `/git/github.com/LiGoldragon` and the `/home/li/primary/repos` symlink index.
  Searches excluded build products, lock files, and `/nix/store`.
- Focused on smoking terms:
  `NexusWork`, `NexusAction`, `CommandSemaRead`, `CommandSemaWrite`,
  `SemaWriteInput`, `SemaReadInput`, `SignalEngine`, `NexusEngine`,
  `SemaEngine`, and Sema-class public verbs.
- Did not modify any source repository. This report is the only file created.

## Ideal Boundary

The contract repo model is wire-only:

- A `signal-<component>` or `meta-signal-<component>` contract owns the public
  messages crossing its boundary: operation/input roots, output/reply roots,
  payload records, route/header vocabulary, frame encode/decode, rkyv/NOTA codec
  surfaces, handshake/version surfaces where present, and round-trip tests.
- A contract does not own daemon runtime behavior: reducers, authorization,
  routing decisions, transaction boundaries, SEMA table execution, Nexus runner
  loops, engine implementations, or generated traits whose methods turn Signal
  messages into Nexus/SEMA objects.
- A client sends and receives Signal messages only. The client does not send a
  `NexusAction`, `NexusWork`, `SemaWriteInput`, `SemaReadInput`, or any
  `CommandSemaRead`/`CommandSemaWrite` action.

This is consistent with `skills/contract-repo.md:92`, which says the contract
owns frame, handshake, request/reply, and payload records, and
`skills/contract-repo.md:119`, which begins the "does not own" list. It is also
consistent with `skills/contract-repo.md:267` through `skills/contract-repo.md:315`:
public contracts use contract-local operation verbs, while Sema is payloadless
classification, not a public executable database DSL. Lowering from public
operation to SEMA plan belongs in the runtime component, not the contract crate
(`skills/contract-repo.md:377` through `skills/contract-repo.md:392`).

The runtime triad is still real; it just belongs inside the component daemon.
`skills/component-triad.md:710` through `skills/component-triad.md:829` places
Signal, Nexus, and SEMA as daemon planes. `skills/component-triad.md:860`
through `skills/component-triad.md:877` describes the generated engine traits as
runtime interfaces. `skills/component-triad.md:980` through
`skills/component-triad.md:1042` defines `NexusWork`, `NexusAction`,
`CommandSemaRead`, and `CommandSemaWrite` as the Nexus mechanism substrate.

## Top Findings

1. `signal-upgrade` and `meta-signal-upgrade` clearly violate the contract
   boundary. They check in public contract schemas, generated Rust, and tests
   that expose Nexus and SEMA roots plus engine traits.
2. `schema-rust-next` is currently a cause and amplifier of this problem. It
   emits runtime engine traits and cross-plane projection solely by type-name
   presence, with no contract-vs-runtime emission profile.
3. The supplied refinement is correct: generated `SignalEngine` is not merely a
   contract-side codec trait. In generated code it converts
   `signal::Signal<Input>` to `nexus::Nexus<Work>` and converts
   `nexus::Nexus<Action>` back to `signal::Signal<Output>`, so it is daemon-side
   triage/reply behavior.
4. Component/runtime repos such as `spirit`, `cloud`, and `upgrade` are allowed
   to carry all-plane schemas. The violation is copying that all-in-one shape
   into `signal-*` or `meta/owner-signal-*` contract repos.
5. Several older hand-written contract repos do not carry generated engine
   traits, but still expose Sema-class verbs (`Assert`, `Match`, `Subscribe`,
   `Retract`, `Mutate`, `Validate`) as public wire operations. That is a
   separate legacy three-layer migration issue.

## Clear Violations

### `signal-upgrade`

The repo describes itself as a peer-callable contract: `signal-upgrade`
`ARCHITECTURE.md:5` through `ARCHITECTURE.md:15` says it owns the upgrade
wire vocabulary and typed Signal records, not storage or runtime.

The checked-in schema contradicts that boundary:

- `/git/github.com/LiGoldragon/signal-upgrade/schema/lib.schema:59` declares
  `NexusWork`.
- `/git/github.com/LiGoldragon/signal-upgrade/schema/lib.schema:60` declares
  `NexusAction` with `CommandSemaWrite` and `CommandSemaRead`.
- `/git/github.com/LiGoldragon/signal-upgrade/schema/lib.schema:63` through
  `/git/github.com/LiGoldragon/signal-upgrade/schema/lib.schema:66` declares
  `SemaWriteInput`, `SemaReadInput`, `SemaWriteOutput`, and `SemaReadOutput`.

The generated Rust makes the leak behavioral, not just nominal:

- `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2347` through
  `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2382` lowers
  `NexusWork::SignalArrived(Input)` into `NexusAction::from(SemaWriteInput::*)`
  or `NexusAction::from(SemaReadInput::*)`.
- `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2385` through
  `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2408` projects
  `NexusAction::CommandSemaWrite` and `NexusAction::CommandSemaRead` into SEMA
  inputs, or `ReplyToSignal` into Signal output.
- `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2459` through
  `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2553` exports
  `SignalEngine`, `NexusEngine`, and `SemaEngine`.
- `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2481` through
  `/git/github.com/LiGoldragon/signal-upgrade/src/schema/lib.rs:2490` proves
  `SignalEngine` is daemon-side triage/reply: it takes Signal input and returns
  Nexus work, then takes Nexus action and returns Signal output.

The tests also assert the leak as intended generated behavior:

- `/git/github.com/LiGoldragon/signal-upgrade/tests/generated_schema.rs:1`
  through `/git/github.com/LiGoldragon/signal-upgrade/tests/generated_schema.rs:4`
  import `NexusAction`, `NexusWork`, and SEMA roots from the contract crate.
- `/git/github.com/LiGoldragon/signal-upgrade/tests/generated_schema.rs:47`
  through `/git/github.com/LiGoldragon/signal-upgrade/tests/generated_schema.rs:67`
  assert that a public upgrade input routes to `CommandSemaWrite`.
- `/git/github.com/LiGoldragon/signal-upgrade/tests/generated_schema.rs:70`
  through `/git/github.com/LiGoldragon/signal-upgrade/tests/generated_schema.rs:75`
  assert that SEMA completion projects back through Nexus into Signal output.

Conclusion: this is a direct contract/runtime boundary violation.
`CommandSemaRead` and `CommandSemaWrite` are `NexusAction` variants. They are
not wire operations and should not appear in this contract repo.

### `meta-signal-upgrade`

The owner/meta upgrade contract has the same defect.

The schema exports internal roots:

- `/git/github.com/LiGoldragon/meta-signal-upgrade/schema/lib.schema:49`
  declares `NexusWork`.
- `/git/github.com/LiGoldragon/meta-signal-upgrade/schema/lib.schema:50`
  declares `NexusAction` with `CommandSemaWrite` and `CommandSemaRead`.
- `/git/github.com/LiGoldragon/meta-signal-upgrade/schema/lib.schema:53`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/schema/lib.schema:56`
  declares SEMA write/read roots.

The generated Rust repeats the runtime behavior:

- `/git/github.com/LiGoldragon/meta-signal-upgrade/src/schema/lib.rs:2104`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/src/schema/lib.rs:2135`
  lowers public meta inputs into SEMA write/read actions.
- `/git/github.com/LiGoldragon/meta-signal-upgrade/src/schema/lib.rs:2139`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/src/schema/lib.rs:2162`
  projects `CommandSemaWrite`, `CommandSemaRead`, and `ReplyToSignal`.
- `/git/github.com/LiGoldragon/meta-signal-upgrade/src/schema/lib.rs:2213`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/src/schema/lib.rs:2307`
  exports `SignalEngine`, `NexusEngine`, and `SemaEngine`.

The generated tests import and exercise those runtime surfaces:

- `/git/github.com/LiGoldragon/meta-signal-upgrade/tests/generated_schema.rs:1`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/tests/generated_schema.rs:5`
  import `NexusAction`, `NexusWork`, and SEMA types from the contract crate.
- `/git/github.com/LiGoldragon/meta-signal-upgrade/tests/generated_schema.rs:63`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/tests/generated_schema.rs:80`
  assert public `ForceFlip` becomes `CommandSemaWrite`.
- `/git/github.com/LiGoldragon/meta-signal-upgrade/tests/generated_schema.rs:83`
  through `/git/github.com/LiGoldragon/meta-signal-upgrade/tests/generated_schema.rs:100`
  assert SEMA reply projects back to Signal output.

Conclusion: same direct violation as `signal-upgrade`.

## Generator Diagnosis: `schema-rust-next`

`schema-rust-next` currently has no profile separating contract emission from
runtime/component emission.

Evidence:

- `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:206` through
  `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:221` documents and
  defines `RustEmissionOptions`; its only public knob is `nota_surface`.
- `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:2365` through
  `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:2379` decides engine
  trait emission by checking for root/type names. `SignalEngine` emits when
  `Input`, `Output`, `NexusWork`, and `NexusAction` exist; `NexusEngine` emits
  when `NexusWork` and `NexusAction` exist; `SemaEngine` emits only when all four
  SEMA roots exist.
- `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:2385` through
  `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:2489` emits the
  engine traits directly once those name gates pass.
- `/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md:63` through
  `/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md:68` still says
  root declarations emit Signal, Nexus, and SEMA traits.
- `/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md:91` through
  `/git/github.com/LiGoldragon/schema-rust-next/ARCHITECTURE.md:139` describes
  generated Signal/Nexus/SEMA envelopes, engine traits, and runtime runner
  direction as one undifferentiated emission target.

This confirms the supplied analysis. The generator treats a public contract
schema and a runtime component schema as the same kind of input. That encourages
copying Spirit's all-plane component schema shape into contract repos.

The read-only SEMA refinement is also real. `SemaEngine` emission is all-or-
nothing: it requires `SemaWriteInput`, `SemaWriteOutput`, `SemaReadInput`, and
`SemaReadOutput` together. An internal runtime schema with only read roots would
get some SEMA names and constructors but no `observe` trait. The fix should
emit read/write SEMA halves independently when an internal schema declares them.

## Counterexamples And Clean Repos

### Clean For This Audit

These repos are clean or aligned with the intended boundary for the specific
Nexus/SEMA engine leak audited here:

- `signal-persona-spirit`: its architecture declares the three-layer model
  explicitly. Public contract operations are wire vocabulary; daemon commands
  and SEMA classification are separate (`signal-persona-spirit/ARCHITECTURE.md:16`
  through `signal-persona-spirit/ARCHITECTURE.md:79`).
- `owner-signal-persona-spirit`: current source uses contract-local operations
  such as `Start`, `Drain`, `Reload`, `Register`, and `Retire`, with no generated
  Nexus/SEMA engine roots found by the smoking-term search.
- `signal-agent`: current source uses contract-local operations
  `Send`, `Cancel`, `SubscribeTranscript`, `TranscriptRetraction`, and `Observe`
  (`signal-agent/src/lib.rs:289` through `signal-agent/src/lib.rs:296`).
- `signal-cloud`: current architecture states that public operations are
  `Observe` and `Validate`, and that Sema classification is daemon-local after
  lowering (`signal-cloud/ARCHITECTURE.md:17` through
  `signal-cloud/ARCHITECTURE.md:26`). No generated Nexus/SEMA roots are checked
  into current main.
- `owner-signal-cloud`: current architecture lists owner-only public operations
  such as `RegisterAccount`, `RotateCredential`, `SetPolicy`, `PreparePlan`,
  `ApprovePlan`, and `ApplyPlan` (`owner-signal-cloud/ARCHITECTURE.md:17`
  through `owner-signal-cloud/ARCHITECTURE.md:31`). No generated engine roots
  were found on current main.
- `signal-sema`: allowed carve-out. It is explicitly the payloadless Sema
  classification vocabulary crate, not a component contract carrying executable
  payloads. `signal-sema/ARCHITECTURE.md:3` through
  `signal-sema/ARCHITECTURE.md:25` says it owns Layer 3 classification; lines
  `38` through `55` forbid daemon/runtime/component payload records.

### Runtime Repos Allowed To Carry All Planes

The following are not violations when they carry Signal/Nexus/SEMA together:

- `spirit`: this is a component/runtime repo. Its all-plane schema and
  generated/runtime engine code are expected because the daemon owns Signal
  triage, Nexus execution, and SEMA state.
- `cloud`: this is the daemon/runtime repo. `cloud/ARCHITECTURE.md:87` through
  `cloud/ARCHITECTURE.md:111` correctly distinguishes generated signal contract
  crates from the combined runtime shape in `cloud/schema/cloud.concept.schema`.
- `upgrade`: this is the component/runtime repo where the ordinary and meta
  upgrade contract inputs can be lowered into one daemon's internal Nexus/SEMA
  engine shape.

This supports the prototype-copy hypothesis: Spirit can contain all planes
because it is a component/runtime repo. That shape must not be copied wholesale
into `signal-<component>` or `meta-signal-<component>` repos.

## Suspicious Or Legacy Contract Repos

These repos did not show the generated `NexusWork`/`NexusAction`/engine-trait
surface in the smoking-term search, but they still expose Sema-class verbs as
public wire operations through older `signal_channel!` declarations:

| Repo | Evidence | Classification |
|---|---|---|
| `signal-message` | `signal-message/src/lib.rs:271` through `signal-message/src/lib.rs:277` exposes `Assert` and `Match` request roots. | Legacy Sema-class wire wrappers. |
| `signal-router` | `signal-router/src/lib.rs:287` through `signal-router/src/lib.rs:293` exposes `Match` roots. | Legacy Sema-class wire wrappers. |
| `signal-system` | `signal-system/src/lib.rs:303` through `signal-system/src/lib.rs:309` exposes `Subscribe`, `Retract`, and `Match`. | Legacy Sema-class wire wrappers. |
| `signal-terminal` | `signal-terminal/src/lib.rs:934` through `signal-terminal/src/lib.rs:951` exposes `Assert`, `Mutate`, `Retract`, `Match`, and `Subscribe`. | Legacy Sema-class wire wrappers. |
| `signal-criome` | `signal-criome/src/lib.rs:844` through `signal-criome/src/lib.rs:863` exposes `Assert`, `Validate`, `Retract`, `Match`, and `Subscribe`. | Legacy Sema-class wire wrappers. |
| `signal-harness` | `signal-harness/src/lib.rs:349` through `signal-harness/src/lib.rs:357` exposes `Assert`, `Retract`, `Match`, and `Subscribe`. | Legacy Sema-class wire wrappers. |
| `signal-mind` | `signal-mind/src/lib.rs:893` through `signal-mind/src/lib.rs:910` exposes `Assert`, `Match`, `Subscribe`, `Retract`, and `Mutate`. | Legacy Sema-class wire wrappers. |
| `owner-signal-terminal` | `owner-signal-terminal/src/lib.rs:148` through `owner-signal-terminal/src/lib.rs:150` exposes `Mutate` and `Retract`. | Legacy owner-policy wire wrappers. |

This is lower severity than the generated engine leak because these repos are
not exporting `NexusAction`, SEMA roots, or engine traits. But it still violates
the current three-layer direction unless the contract is explicitly Sema-facing.
Many of their `ARCHITECTURE.md` files already say the three-layer migration is
pending, so the fix is a known migration rather than a new design question.

One naming caution: `signal-cloud` uses `Validate` as a public operation while
its architecture also says there is no public `Validate` Sema root
(`signal-cloud/ARCHITECTURE.md:19` through `signal-cloud/ARCHITECTURE.md:26`).
That can be acceptable only if `Validate` is treated as a domain-local Cloud
operation, not the universal Sema class. It is a collision-prone name and should
be reviewed when the schema profile lands.

## Correct Fix Pattern

### Contract Emission Profile

Add an explicit `schema-rust-next` emission profile for contract repos. A
contract profile should emit only:

- public Signal roots and payload records;
- route/header objects and short-header projection;
- Signal frame encode/decode;
- rkyv archive/deserialize surfaces;
- NOTA codec surfaces according to the existing `nota_surface` option;
- trace/help/version identity that names public Signal routes only.

The contract profile must not emit:

- `NexusWork`, `NexusAction`, `CommandSemaRead`, `CommandSemaWrite`,
  `CommandEffect`, or `Continue`;
- `SemaWriteInput`, `SemaReadInput`, `SemaWriteOutput`, or `SemaReadOutput`;
- `SignalEngine`, `NexusEngine`, `SemaEngine`, component runners, or projection
  methods that convert public Signal input into Nexus/SEMA objects.

### Runtime/Component Emission Profile

Add a runtime/component profile for daemon repos. A runtime schema may:

- import one or more public Signal contract crates;
- declare internal `NexusWork`, `NexusAction`, SEMA read/write roots, and effect
  roots;
- emit `SignalEngine`, `NexusEngine`, SEMA engine traits, runner loops, and
  cross-plane projections;
- keep daemon-only lowering from public Signal operation to Nexus/SEMA command
  inside the component repo.

For components with multiple contracts, the component repo is the join point.
For example, `cloud` should import/use public `signal-cloud` and owner/meta
`owner-signal-cloud`/`meta-signal-cloud` contract messages, then lower both into
one internal Cloud Nexus/SEMA runtime schema. The public contract repos should
not each carry their own daemon-internal Nexus/SEMA roots.

For `upgrade`, move the all-plane generated shape to the runtime `upgrade`
repo. Keep `signal-upgrade` and `meta-signal-upgrade` as wire-only contract
crates generated from contract profiles, and have `upgrade` import both public
contract surfaces into its internal Nexus/SEMA schema.

### Independent SEMA Halves

The runtime profile should not require all four SEMA roots to emit useful engine
interfaces. It should emit independently from declared halves:

- write half present: emit/apply `SemaWriteInput -> SemaWriteOutput`;
- read half present: emit/observe `SemaReadInput -> SemaReadOutput`;
- both present: either compose those halves into `SemaEngine` or emit a combined
  trait plus the two smaller halves, depending on the final design decision.

This fixes the read-only SEMA root gap without leaking SEMA roots into public
contract crates.

## Immediate Operator Fixes

1. In `schema-rust-next`, add an explicit emission profile such as
   `RustEmissionProfile::{Contract, Runtime}` inside `RustEmissionOptions`.
   Preserve the existing `nota_surface` as an orthogonal option.
2. Gate all runtime-only output behind the runtime profile: Nexus/SEMA roots,
   `nexus::Nexus`, `sema::Sema`, `schema::Plane`, engine traits, runner support,
   and cross-plane projection methods.
3. Add contract-profile regression tests using the upgrade contracts: generated
   `signal-upgrade` and `meta-signal-upgrade` contract outputs must not contain
   `NexusAction`, `CommandSemaRead`, `CommandSemaWrite`, `SemaWriteInput`,
   `SemaReadInput`, `SignalEngine`, `NexusEngine`, or `SemaEngine`.
4. Add runtime-profile tests using a component schema fixture: runtime output
   should still emit Nexus/SEMA roots, engine traits, and projection support.
5. Split SEMA engine emission by read/write availability in runtime profile.
   Add a read-only fixture proving an internal schema with only
   `SemaReadInput`/`SemaReadOutput` emits observe support.
6. Regenerate or hand-trim `signal-upgrade` and `meta-signal-upgrade` after the
   profile exists. Their public schemas/tests should keep only Signal input,
   output, payload, frame, route, and codec behavior.
7. Schedule the older `signal_channel!` Sema-class wire wrappers as separate
   migrations. Do not mix that broader operation-rename work into the
   generator-profile fix unless a repo is already being cut over.

## Design Questions For Psyche

1. Should `SignalEngine` be runtime-only in all cases? I infer yes because the
   generated trait currently maps Signal to Nexus and Nexus back to Signal.
   Contract-side generation should keep frame/codec/route helpers, not
   triage/reply implementation traits.
2. For SEMA read/write split, should the public generated names be separate
   traits (`SemaReadEngine`, `SemaWriteEngine`) or one `SemaEngine` emitted with
   only the declared methods? The mechanics are clear; the naming/API shape
   needs a psyche/designer decision.
3. Should domain operations that share a word with a Sema class, especially
   `Validate`, be avoided in public contracts to reduce ambiguity, or is the
   layer boundary enough when architecture states it explicitly?

## Classification Summary

| Classification | Repos |
|---|---|
| Clear boundary violation | `signal-upgrade`, `meta-signal-upgrade` |
| Generator/design cause | `schema-rust-next` |
| Clean for this audit | `signal-persona-spirit`, `owner-signal-persona-spirit`, `signal-agent`, current `signal-cloud`, current `owner-signal-cloud`, `signal-sema` as the explicit Sema vocabulary crate |
| Allowed all-plane runtime repos | `spirit`, `cloud`, `upgrade` |
| Suspicious legacy Sema-class wire wrappers | `signal-message`, `signal-router`, `signal-system`, `signal-terminal`, `signal-criome`, `signal-harness`, `signal-mind`, `owner-signal-terminal` |

