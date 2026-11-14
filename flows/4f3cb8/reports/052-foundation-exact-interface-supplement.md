# 052 foundation exact interface supplement

This supplies missing authored interfaces in 89f561/7b35, not a new scope. Original backend selection and partial-configuration semantics control. No runtime permission is granted by this proposal.

## Configure vocabulary and generated projections

The current authored ConfigurationChange variants are the SINGLE source for stored configured-value/key projections. Set variants carry one complete existing typed declaration; removals carry only its typed identity. Add these exact operations alongside Metaflow/RemoveMetaflow:

```ethos
ConfigureModel.{ Address Native.String }
ConfigureContinuity.{ Address Continuity }
ConfigurationChange.[ Model.ConfigureModel RemoveModel.Address
                      Continuity.ConfigureContinuity RemoveContinuity.Address
                      ... ]
```

The ellipsis means all already approved other setting variants, unchanged, not a generated variant. Each concrete runtime-policy leaf is a separate set variant using its approved leaf type; do not persist an entire RuntimePolicy product or a string key. Keep the existing explicit leaf inventory as the input declaration, not a second hand-maintained enum.

Generate `ConfiguredValue` from SET variants only, with identical variant name and payload. Generate `Setting` from their typed identity projection: `Model.Address`, `Continuity.Address`; keyed declarations retain their existing native typed key; genuinely singleton leaf variants are nullary. `ConfiguredValue::setting(&self) -> Setting` is total, exhaustive generated matching, cloning only its typed key. Generate the corresponding removal-to-Setting projection. No arbitrary key accompanies a value in the mutation API. Generated output is committed and compared against generation in tests. Existing metaflow declaration storage remains its separately allocated V6 family; its Setting identity is still available for readiness/removal, without also storing the value in RuntimePolicy. Every setting has exactly one selected family.

`RemoveModel.Address` and `RemoveContinuity.Address` retract that key only, returning existing Replaced/Unchanged outcomes; absence is idempotent. No seat, queue, native model, or composed work is altered by a setter/removal. No new Memory version is proposed beyond the already allocated sparse RuntimePolicy V1 and declaration V6. Expose actual additional persisted reachability before changing any result type.

## Readiness and construction boundary

Shared vocabulary, owned below both contracts:

```ethos
Readiness.[ Ready Awaiting.Vector<Setting> ]
```

Awaiting is nonempty, deterministic first-use order with duplicate keys removed; Ready represents no missing required setting. The wire may observe this type; avoid adding it to existing persisted shared Refusal. Each affected operation adds its own typed readiness result as already approved, and its actual archived reachability must be checked. Internal resolution returns either an ephemeral fully typed operation snapshot or Awaiting; it never inserts placeholders.

Bare RunningNexus construction holds ONLY Place, opened original Engine/FlowStore, and intrinsic synchronization/control state. Remove the requirement to construct Herdr/Codex/runtime adapters during this constructor. At the dependent operation boundary resolve its exact settings from one consistent view, then construct that operation's adapter from the successful snapshot. No Option-filled fake adapter, global default, or cached policy copy is needed. Configure/Observe readiness are core control capabilities callable before those adapters exist. A missing required setting returns before dependent effects; existing queue/seat remains intact.

## External translator fields, order, units

Reuse the approved BootstrapTextBudget five-field order and FrameBytes type. Add distinct typed positive millisecond counts, checked into the actual Duration/deadline:

```ethos
ConnectTimeoutMilliseconds.Integer
ReadTimeoutMilliseconds.Integer
WriteTimeoutMilliseconds.Integer
TranslatorConfiguration.{ BootstrapTextBudget FrameBytes
                          ConnectTimeoutMilliseconds
                          ReadTimeoutMilliseconds
                          WriteTimeoutMilliseconds }
```

Order is exactly as shown. FrameBytes applies independently to each inbound/outbound frame at this translator; arithmetic/protocol u32 representability is checked. Connect bounds client socket connection, Read bounds each complete frame read, Write bounds each complete frame write. An accepted server connection has no connect phase. Each bound is one absolute deadline across that operation, not reset per partial read/write; interruption retries preserve it. No native harness timeout is introduced here: those remain separately configured domain settings at their actual consumers. No timeout/default value is supplied in Rust or inferred from another field.

The configured external wrapper supplies this explicit translator value before decoding Place/Configure. Core typed Start receives Place only. The outer translator performs parsing, framing, validation and I/O accounting, then invokes typed core control. General domain codec settings remain Memory-owned and separate from outer parsing. Test actual wrapper arguments and predecode path, not only constructed Rust values.

## Required bounded checks

Generated equality and exhaustive key/value/removal projections; model full-Address/topic isolation; idempotent removal and untouched seats/queues; exact timeout order and positive/width/deadline checks; partial I/O cannot extend a deadline; bare control works with zero policy rows; resolve only needed keys and no adapter construction on Awaiting; original own-052 store fresh/reopen/atomicity/corruption tests. Existing source conversions are implementation work, not absent design authority.

Publication remains separate: Meta candidate needs an actual witnessed owned remote and exact reserved ref, independent candidate review, protected publication and exact consumer pins. This supplement allocates no ref or wire/Memory number.
