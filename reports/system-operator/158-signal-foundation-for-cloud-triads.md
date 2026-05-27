# 158 - signal foundation for cloud triads

*Kind: Audit / handoff · Topic: current signal foundation for a new
`cloud` component triad · Date: 2026-05-23 · Lane:
system-specialist assistant*

## Frame

The assigned lane was read-only except for this report:

- Write only
  `/home/li/primary/reports/system-specialist/158-signal-foundation-for-cloud-triads.md`.
- Do not edit code.
- Do not create repositories.
- Use local source, repo docs, and recent reports; do not use web.

Intent capture was recorded through Spirit before writing:
`(RecordAccepted ((301 signal Constraint "Cloud signal foundation report lane is read-only" Maximum)))`.

Correction: that record was an agent assignment, not psyche intent. It should
not be treated as architectural truth. The cleanup is tracked by bead
`primary-4f08`.

## Executive answer

For a new triad component today, the canonical signal foundation is:

- `signal-frame` for wire frames, `Request` / `Reply`, rkyv transport
  shape, `signal_channel!`, `signal_cli!`, stream witnesses, operation
  heads, and working-vs-owner CLI route tables.
- `signal-sema` for universal payloadless classification:
  `SemaOperation`, `SemaOutcome`, `SemaObservation`, and projection
  traits.
- `signal-executor` for the daemon request path: lower public
  contract operations into local commands, execute an atomic command
  batch, emit operation/effect observations, and map effects back to
  typed contract replies.
- `sema-engine` only inside daemon/runtime repos that need typed local
  state. It is not the public signal contract layer.
- `nota-codec` as the text projection. NOTA is the only argument
  language.

The current name for new signal foundation work is `signal-frame`, not
`signal-core`. `signal-core` still exists and still appears in parts of
the dependency graph, but its own architecture file marks it
deprecated and superseded by `signal-frame + signal-sema`.

For the `cloud` triad, the current repository names should remain:

- `cloud` - daemon/runtime repo with bundled thin CLI.
- `signal-cloud` - ordinary working contract.
- `owner-signal-cloud` - owner/policy contract.

Do not start new work under `meta-signal-cloud` until the tentative
`owner-signal` to `meta-signal` rename is explicitly decided and
propagated through skills, repo names, crate names, and docs.

## Source and status clues

Foundation repos:

- `/git/github.com/LiGoldragon/signal-frame`
  - Clean working copy.
  - Parent: `75837dce` - `signal-frame: rename persona origin reference`.
  - `/git/github.com/LiGoldragon/signal-frame/ARCHITECTURE.md`
    says this is the renamed successor to former `signal-core`.
  - `/git/github.com/LiGoldragon/signal-frame/src/lib.rs`
    re-exports `signal_channel!` and owns the frame / command-line
    surface.
  - `/git/github.com/LiGoldragon/signal-frame/src/command_line.rs`
    implements the single-argument CLI, request-head routing, caller
    injection, socket send, and NOTA reply printing.
  - `/git/github.com/LiGoldragon/signal-frame/macros/README.md`
    documents the current `operation Verb(Payload)` grammar.

- `/git/github.com/LiGoldragon/signal-sema`
  - Clean working copy.
  - Parent: `1604cceb` - `signal-sema: ARCH SemaObservation as
    Tier-2-shaped type with verb-namespace shape`.
  - `/git/github.com/LiGoldragon/signal-sema/src/operation.rs`
    contains `SemaOperation` and `ToSemaOperation`.
  - `/git/github.com/LiGoldragon/signal-sema/src/outcome.rs`
    contains `SemaOutcome`, `ToSemaOutcome`, and `SemaObservation`.
  - `/git/github.com/LiGoldragon/signal-sema/ARCHITECTURE.md`
    explicitly says public contract operations, component commands,
    and Sema classification are three separate layers.

- `/git/github.com/LiGoldragon/signal-executor`
  - Clean working copy.
  - Parent: `63d3732f` - `signal-executor: document atomic and reply
    mapping contracts`.
  - `/git/github.com/LiGoldragon/signal-executor/src/lowering.rs`
    defines `Lowering`, `OperationPlan`, and `BatchPlan`.
  - `/git/github.com/LiGoldragon/signal-executor/src/executor.rs`
    executes a `signal-frame::Request<Operation>` through lowering,
    atomic command execution, observations, and reply mapping.
  - `/git/github.com/LiGoldragon/signal-executor/ARCHITECTURE.md`
    says `signal-executor` depends on `signal-frame` and
    `signal-sema`, not `sema-engine`.

- `/git/github.com/LiGoldragon/sema-engine`
  - Dirty working copy: `M ARCHITECTURE.md`.
  - Working copy is described as `e36c47b8 main* | ARCHITECTURE:
    handover raw-payload container discipline (intent 274)`.
  - Parent: `67ac34a9 main@origin | sema-engine: use canonical
    signal-core source`.
  - `/git/github.com/LiGoldragon/sema-engine/Cargo.toml` still has
    `signal-core = { git = "https://github.com/LiGoldragon/signal-core.git" }`.
  - `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md` still
    labels `signal-core` as a `NonEmpty` utility. This is a live
    transitional dependency, not the foundation name for new contract
    work.

- `/git/github.com/LiGoldragon/signal-core`
  - Dirty working copy: `M AGENTS.md`.
  - Parent: `c59bcb95` - `signal-core: rename persona origin reference`.
  - `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` starts
    with a deprecation banner: superseded by `signal-frame +
    signal-sema` on 2026-05-19.
  - The rest of that file still contains old universal-verb
    architecture prose. Treat the banner as the authority; the lower
    body is historical/stale for new component design.

Current or nearly-current contract examples:

- `/git/github.com/LiGoldragon/signal-persona-spirit`
  - Depends on `signal-frame` and `signal-sema`.
  - `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`
    is the best ordinary contract example with operations, replies,
    events, stream declarations, and an `observable` block.
  - It currently emits `EffectEmitted(SemaObservation)` in an ordinary
    contract. Per `reports/second-designer/154-...`, that is now
    transitional for component-local domain contracts; new
    component-local contracts should prefer a typed local `Effect`
    unless they are authority-tier.

- `/git/github.com/LiGoldragon/owner-signal-persona-mind`
  - Depends on `signal-frame`.
  - `/git/github.com/LiGoldragon/owner-signal-persona-mind/src/lib.rs`
    is a compact owner contract example with policy operations and
    typed rejections.

- `/git/github.com/LiGoldragon/signal-repository-ledger`
  - Depends on `signal-frame`.
  - `/git/github.com/LiGoldragon/signal-repository-ledger/ARCHITECTURE.md`
    explicitly describes migration away from old `signal-core` Sema
    verbs.

- `/git/github.com/LiGoldragon/owner-signal-repository-ledger`
  - Depends on `signal-frame`.
  - Useful owner-contract example, but its shape still carries some
    older policy-style configuration habits and should not be copied
    blindly for a new cloud schema.

Recent report sources:

- `/home/li/primary/reports/operator/150-triad-signal-sema-migration-current-state.md`
  is the most useful consolidated operator handoff for triad
  migration state.
- `/home/li/primary/reports/second-designer/154-effect-emitted-and-public-routing-designs-2026-05-22.md`
  records the ratified tier default: authority-tier contracts default
  to `SemaObservation`; component-local domain contracts default to a
  typed local `Effect`.
- `/home/li/primary/reports/second-designer/157-audit-engine-stack-state-before-constraint-and-integration-beads-2026-05-23.md`
  says the foundation stack is moving and that three-tier signal
  sizing plus routing work is partly architectural / beaded rather
  than fully implemented.
- `/home/li/primary/reports/nota-designer/5-bracket-string-migration-2026-05-23/2-deploy-stack-consumers.md`
  reports that `lojix` was blocked by a stale `signal-core`
  dependency. This is another clue that `signal-core` is not gone
  from the graph, even though it is not the new design target.

## Current canonical signal foundation

The canonical layer split is:

1. Public contract crate: `signal-<component>` or
   `owner-signal-<component>`.
2. Frame layer: `signal-frame`.
3. Classification layer: `signal-sema`.
4. Execution layer used by the daemon: `signal-executor`.
5. Optional daemon-local state engine: `sema-engine`.

The contract crate declares domain operations. It does not declare
universal `Assert`, `Mutate`, `Retract`, or `Match` operations as
public request roots. Those are Sema classifications projected from
component-local commands after the public operation has been lowered.

Correct public-contract direction:

```rust
signal_channel! {
    channel Cloud {
        operation Query(Query),
        operation Plan(ChangeSet),
        operation Apply(ChangeSet),
        operation Watch(Subscription) opens DomainStream,
        operation Unwatch(SubscriptionToken),
    }

    reply Reply {
        Queried(QueryResult),
        Planned(PlanResult),
        Applied(ApplicationReceipt),
        Rejected(Rejection),
        RequestUnimplemented(RequestUnimplemented),
    }

    event Event {
        OperationReceived(OperationReceived) belongs DomainStream,
        EffectEmitted(EffectEmitted) belongs DomainStream,
    }

    stream DomainStream {
        token SubscriptionToken;
        opened SubscriptionOpened;
        event OperationReceived;
        event EffectEmitted;
        close Unwatch;
    }

    observable {
        filter default;
        operation_event OperationReceived;
        effect_event EffectEmitted;
    }
}
```

The names above are illustrative skeleton style, not a final Cloud API
schema. The important constraints are:

- Contract-local verbs in the public operation roots.
- Domain payloads as typed records and variants.
- Provider capability and provider-specific requests represented as
  variants, not loose booleans or stringly flags.
- Typed unsupported-capability replies when a daemon was built
  without a provider or capability.
- The CLI remains generated / thin and speaks only to the daemon.
- The daemon lowers `Operation` into local `Command` and projects
  local command/effect to `SemaOperation` / `SemaOutcome`.

## `signal-core` vs `signal-frame`

Current answer:

- New code should say and depend on `signal-frame`.
- New contract crates should import `signal_frame::signal_channel`
  and use `signal-frame` in `Cargo.toml`.
- New daemon CLI code should use `signal_frame::signal_cli!` or the
  underlying command-line helper types from `signal-frame`.
- New runtime/executor work should use `signal-executor` for the
  request path and `signal-sema` for classification.

Mixed-state answer:

- `signal-core` still exists as a repo and still compiles as a crate.
- `signal-core/ARCHITECTURE.md` and `signal-core/skills.md` mark it
  deprecated at the top.
- `signal-core/ARCHITECTURE.md` still contains old prose below the
  banner; do not copy that shape.
- `sema-engine` still depends on `signal-core` for `NonEmpty` today.
- At least one recent deploy-stack report says stale `signal-core`
  dependencies still block some consumers.

Practical conclusion:

`signal-core` is a migration residue and live dependency hazard. It is
not the naming target for `cloud`, `signal-cloud`,
`owner-signal-cloud`, or new reports. New work should avoid adding any
new `signal-core` dependency. Existing `signal-core` edges should be
tracked as migration debt and removed deliberately.

## Contract skeleton for `signal-cloud`

`signal-cloud` should be the ordinary working contract. It should
model cloud-provider work as typed domain requests, not as generic
Sema verbs.

Recommended skeleton categories:

- `Query` for reading provider state:
  - zone state;
  - DNS records;
  - redirect / ruleset state;
  - provider capability surface.
- `Plan` for dry-run / validation of intended changes.
- `Apply` for mutating external provider state.
- `Watch` / `Unwatch` if cloud state or daemon activity needs a
  subscription surface.

Recommended variant direction:

```rust
pub enum Query {
    ProviderCapabilities(ProviderSelection),
    DomainRecords(DomainSelection),
    RedirectRules(DomainSelection),
    ZoneSettings(DomainSelection),
}

pub enum Change {
    DnsRecord(DnsRecordChange),
    RedirectRule(RedirectRuleChange),
    ZoneSetting(ZoneSettingChange),
}

pub enum ProviderSelection {
    Cloudflare(CloudflareScope),
    Google(GoogleScope),
    Hetzner(HetznerScope),
}
```

The exact names should be refined when the Cloudflare API surface is
designed, but this shape preserves the important architectural rule:
provider and feature choices are self-describing variants. A missing
provider should not be encoded as an absent field or a boolean. It
should become a typed unsupported-capability reply such as:

```rust
pub enum Rejection {
    UnsupportedCapability(UnsupportedCapability),
    ProviderUnavailable(ProviderUnavailable),
    ValidationFailed(ValidationFailure),
}
```

Observable effect payload:

- If `signal-cloud` is mostly a component-local domain contract, its
  `EffectEmitted` should carry a typed cloud `Effect`, per
  `reports/second-designer/154-...` Design D.
- If a specific event is intentionally authority-tier or generic
  cross-component state, it can carry `SemaObservation`, but that
  should be the exception and should be called out in the contract
  architecture.

## Contract skeleton for `owner-signal-cloud`

`owner-signal-cloud` should be the owner/policy contract. It should
not duplicate ordinary DNS/redirect operations. It should control
daemon policy, provider enablement, credential references, and
inspection.

Recommended skeleton categories:

- `Configure(Configuration)` for owner policy.
- `EnableProvider(ProviderEnablement)` / `DisableProvider(ProviderSelection)`
  if provider support is runtime-policy gated.
- `InstallCredentialReference(CredentialReference)` or a better
  credential-reference name once the secrets substrate is specified.
  The owner contract should carry references and policy, not raw
  secrets.
- `Inspect(Inspection)` for owner-visible policy and health state.
- `RotateCredential(CredentialRotation)` only if credential rotation
  belongs to `cloud`; otherwise leave that to the secrets component
  and have `cloud` observe the new reference.

Owner observable payload:

- If the owner contract has an observable block, default to
  `EffectEmitted(SemaObservation)` because it is authority-tier, per
  the ratified direction in `reports/second-designer/154-...`.
- If policy effects carry domain-critical details that cannot be
  recovered elsewhere, add a typed owner `Effect` only after deciding
  why this authority contract is an exception.

## Tests a new contract repo must include

Minimum contract-repo checks for `signal-cloud` and
`owner-signal-cloud`:

1. `nix flake check` must run the contract test suite. Cargo-only
   tests are not enough as the durable entry point.
2. NOTA round trips for every operation family, every reply family,
   and every event/stream record the contract exposes.
3. Canonical NOTA examples under `examples/`, included in tests with
   `include_str!`, so docs and parser witnesses cannot drift.
4. rkyv frame round trips for representative request, reply, and
   event frames.
5. `SignalOperationHeads::HEADS` or equivalent macro-emitted witness
   tests proving the public operation heads exist and are the ones the
   CLI route table will use.
6. A no-old-shape constraint test:
   - no `signal-core` dependency in `Cargo.toml`;
   - no public operation root shaped like old `Assert(Payload)` /
     `Mutate(Payload)` / `Match(Payload)`;
   - no hand-written `OperationKind` where the macro should emit it.
7. Observable-surface tests if `observable` is present:
   - `Tap` / `Untap` injection;
   - default or explicit observer filter round trip;
   - stream token/open/event/close witness;
   - `OperationReceived` and `EffectEmitted` frame round trips.
8. Typed unsupported-capability tests:
   - a provider compiled or configured out returns a typed
     unsupported-capability reply;
   - the request is not treated as a parser error or frame rejection.
9. Contract purity dependency test:
   - no tokio;
   - no kameo;
   - no redb;
   - no `sema-engine`;
   - no provider HTTP client in the contract crate.
10. Name-shape tests or source checks for current naming discipline:
    no avoidable ancestry prefixes such as `CloudCloudRequest`, no
    abbreviations such as `Cfg`, and no meaningless boolean feature
    series where variants would be self-describing.

Daemon/runtime tests that are outside the contract repo but should be
planned next:

- CLI one-argument rule through `signal_cli!`.
- Working operation routed to the working socket.
- Owner operation routed to the owner socket.
- Public `Operation` lowered to component-local `Command`.
- `Command` projects to `SemaOperation`.
- Component `Effect` projects to `SemaOutcome`.
- External provider tests use local fakes or recorded fixtures, never
  real Cloudflare credentials in normal tests.

## Open conflicts from `owner-signal` to `meta-signal`

The tentative rename is real as an intent direction, but it is not
implemented enough to use for new repository names.

Current concrete vocabulary still says `owner-signal`:

- `/home/li/primary/AGENTS.md` states the triad repositories are
  `<component>`, `signal-<component>`, and
  `owner-signal-<component>`.
- `/home/li/primary/skills/component-triad.md` carries the same
  triad rule.
- Existing owner repos use the current name:
  - `/git/github.com/LiGoldragon/owner-signal-persona-mind`
  - `/git/github.com/LiGoldragon/owner-signal-persona-orchestrate`
  - `/git/github.com/LiGoldragon/owner-signal-repository-ledger`
- `signal-frame::signal_cli!` currently models route selection as
  working vs owner socket.

Open conflicts if `meta-signal` is adopted:

- Repository names: `owner-signal-*` vs `meta-signal-*`.
- Crate names: `owner_signal_*` vs `meta_signal_*`.
- Module names and runtime exports: `owner::SignalClient` vs a
  future `meta::SignalClient`.
- Socket environment names and generated CLI route names.
- Skills and AGENTS wording.
- Existing reports and beads that use owner terminology.
- Semantics: `owner` means authority/policy by identity; `meta` may
  imply supervisory, reflective, or cross-cutting control. That is a
  semantic change, not just a string rename.

Recommendation:

- Create `owner-signal-cloud`, not `meta-signal-cloud`, until the
  psyche explicitly supersedes the triad rule.
- When the rename is approved, do it as one migration across skills,
  AGENTS, repo names, crate names, CLI route naming, and existing
  owner contract docs. Do not split the vocabulary by introducing
  `meta-signal` for only one new component.

## Best next questions

1. Should `signal-cloud` expose `Plan` as a first-class public
   operation, or should validation/dry-run be an owner-policy mode
   attached to `Apply`?
2. Is Cloudflare support a compile-time feature, a daemon runtime
   policy, or both? The contract can support either, but tests differ.
3. Which component owns credential material and rotation? My default
   assumption is that `cloud` receives credential references and does
   not carry raw secrets.
4. Should cloud provider capability discovery be a normal `Query`, or
   should it be part of owner `Inspect`? I lean normal `Query`, because
   callers need to know what the working daemon can do without owner
   authority.
5. Is the `owner-signal` to `meta-signal` rename merely vocabulary, or
   does it change the authority model? This should be answered before
   any repo is created under the new name.

## Bottom line

The safe foundation for `cloud` is `signal-frame` plus
`signal-sema`, executed in the daemon through `signal-executor` and
optionally backed by `sema-engine`. `signal-core` is deprecated but
still present as migration residue. The new contracts should follow
the modern `signal_channel!` style with contract-local verbs,
self-describing variants, typed unsupported-capability replies, and
Nix-owned NOTA/rkyv/constraint tests. The owner/meta naming question
is still unresolved, so the correct repo name today remains
`owner-signal-cloud`.
