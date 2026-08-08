# The operation-root payload fix — authoring rule for the post-5311f9a engine

2026-06-05. During the lojix daemon build, the generated `NexusEngine` came out
**degenerate** — only `decide()`, with `run_effect` / `apply_sema_write` /
`observe_sema_read` / `budget_exhausted_reply` / `continuation_limit`, the
`NexusRunnerAdapter`, and the `RunnerEngines` impl all missing, and the
`NexusWork`/`NexusAction`/`SemaReadInput`/`SemaWriteInput` enums emitted as bare
payloadless variants. The daemon could not be implemented against that surface.

## Root cause — a deliberate in-flux change, not stale breakage

It traces to the psyche's own commit from today: schema-next
`5311f9a "keep same-name payload recovery out of namespace enums"`
(`schema-next/src/source.rs`). That change makes enums declared in a schema's
**namespace body** use `SourceVariantPayloadResolution::explicit_only()` — a
bare variant name no longer auto-recovers a same-named type as its payload. Its
companion test (`namespace_enum_bare_variants_do_not_resolve_to_same_named_payloads`)
locks this in for plain enums like `Kind [Decision Correction]`. The
still-passing `root_header_bare_names_resolve_to_exported_namespace_payloads`
test shows bare names in the **header `[...]` position still resolve**.

The cloud/lojix daemon schemas declared their operation roots the *body* way —
`NexusWork [SignalArrived SemaReadCompleted …]` inside `{}`, with separate
same-name alias lines (`SignalArrived SignalInput`). Post-`5311f9a` those body
variants stay bare, so the emitter's `nexus_runner_shape`
(`schema-rust-next/src/lib.rs:3443-3446`) finds no `Plain` payload on
`ReplyToSignal` and returns `None`, which gates out the entire runner/effect
trait surface. cloud only escapes this because its `Cargo.lock` pins
schema-rust-next **0.1.12** (pre-`5311f9a`); the lojix stack regenerated on
**0.1.13** and hit the new rule.

This is purely a toolchain-era difference, proven: the same schema yields the
full surface on 0.1.12 and the degenerate one on 0.1.13.

## The fix — schema-side, no generator surgery, no version pin

Declare the operation-root enums with **explicit `(Variant Payload)` variants**
instead of bare names + same-name aliases. `explicit_only()` keeps explicit
payloads; it only drops bare-name recovery. So the post-`5311f9a` authoring rule
is:

> **Operation-root enums in a daemon plane schema's namespace body
> (`NexusWork`, `NexusAction`, `SemaReadInput`, `SemaWriteInput`) must declare
> explicit `(Variant Payload)` variants. The bare-name + same-name-alias form no
> longer carries payloads outside the header position.**

Applied to lojix (`drafts/lojix.nexus.schema:75-76`,
`drafts/lojix.sema.schema:48,53`):

```
NexusWork [(SignalArrived SignalInput) (SemaReadCompleted SemaReadOutput) (SemaWriteCompleted SemaWriteOutput) (EffectCompleted EffectResult)]
NexusAction [(CommandSemaRead SemaReadInput) (CommandSemaWrite SemaWriteInput) (CommandEffect EffectCommand) (ReplyToSignal SignalOutput) (Continue NexusWork)]
SemaReadInput [(QueryGenerations Selection) (ReadEventLog EventLogRange) (CheckKeyMaterial KeyMaterialQuery)]
SemaWriteInput [(RecordDeploySubmitted DeploySubmission) … (RecordContainerTransition ContainerTransition)]
```

The now-redundant same-name alias lines were dropped. The `*Output` roots
already used the explicit form, which is why only the `*Input`/`Work`/`Action`
roots needed conversion.

**Verified:** regenerating the lojix daemon artifacts restores the full surface
— `NexusEngine` carries `run_effect`/`apply_sema_write`/`observe_sema_read`/
`budget_exhausted_reply`/`continuation_limit` (nexus.rs:1249-1256),
`NexusRunnerAdapter` + `RunnerEngines` are present (nexus.rs:1297-1317), and
`NexusWork`/`NexusAction` are payload-bearing (`SignalArrived(SignalInput)`,
`CommandEffect(EffectCommand)`, `ReplyToSignal(SignalOutput)`).

## Implication for cloud (and every future triad daemon)

cloud's `schema/nexus.schema` + `schema/sema.schema` still use the old bare form
and build only because cloud is pinned to schema-rust-next 0.1.12. **When cloud
(or any component) moves to 0.1.13+, its operation-root enums need the same
explicit-payload migration**, or its generated runner surface collapses the same
way. This is a one-time, mechanical per-schema edit. Whether 0.1.13's
namespace-body `explicit_only` rule is the settled direction (in which case this
authoring rule belongs in `skills/component-triad.md` and cloud should migrate)
or an interim state of the in-flux lowering rewrite is the psyche's call — the
lojix fix works under either, since explicit payloads are valid in both eras.
