# 052 step 1 — bare place, configured Memory, operation readiness

Owner4f3cb8 through Core coordinator74026a. Step1 began2026-11-06 00:25UTC; coordinator Task60 received00:26UTC. Code/test step2 begins after step1 completion, then240min; capsule step4 after step2,120min. Existing sole worker/native and artifacts are preserved. No rollout is authorized by this design.

## Controlling living ruling

Nexus starts with its place alone. No startup configuration or Rust defaults. Every value, defaults included, is set one declaration at a time by Configure atomically into Memory; Memory is its only source. An unset required value makes the operation that needs it refuse, naming the value (Readiness.Awaiting); bare startup does not fail for missing configuration. Idle close requires a configured Continuity value authorizing it; absence causes no action and the flow continues. A Configure file replayed after start is an external shell convenience. This replaces startup-present override/absent-preserve and startup seeding/overlay, not merely their precedence.

## Removed from the previous design

Remove Start's ConfigurationChange vector, startup policy resolution/seeding, duplicate startup setting logic, startup-to-Memory overrides and whole-configuration startup readiness requirement. No automatic Configure replay inside the Nexus. Nix must not generate a runtime Rust defaults source or inject behavioral policy as Start data. Existing Memory remains authoritative, not overwritten at restart. No default continuity inferred from Address or an old profile for new runtime operations.

Keep the already accepted safe same-handle Memory admission, frozen predecessor decoding, explicit version allocation, store-private mutation ownership, configured codec values and exact native observations. Their mechanisms remain needed where the revised operations use them; no speculative opening transaction is retained merely to apply now-removed startup rows.

## Proposed type/operation structure

The Start domain remains the existing place facts: ordinary socket, meta socket, store path, explicit and startup-only. These are routing/placement, not behavioral Memory values. Live attempts to move/rebind still refuse by named setting; no live resource transition is added.

Configure keeps ONE shared typed per-setting vocabulary and atomic store-owned change path. One declaration/address operation changes only that declaration; snapshot collections remain observations. Other already approved explicit per-value operations retain their typed domains. There is no parallel startup setting vocabulary.

An unset value is represented as actual absence, not zero, empty string or a default-filled resolved policy. Each operation resolves only the settings it needs from one consistent Memory snapshot. Proposed readiness result identifies missing typed Setting keys, including Address for declaration absence and model/key for threshold/effort lookups. It is checked before that operation's effects. Present values undergo intrinsic validation at Configure; cross-setting constraints are checked against present peers and again on the fully required operation snapshot. Do not reject the first of two necessary independent declarations just because its peer has not yet been configured.

The prior all-required RuntimePolicy record cannot represent a bare unconfigured store. Proposed smallest adaptation is a single sparse configured-policy family (same owned vocabulary), with one keyed row per policy leaf rather than a seeded singleton resolved struct. Consumer-owned resolved groups remain ephemeral typed operation snapshots. This changes the previously allocated singleton key `policy`; exact table/schema/key revision requires Core allocation judgment BEFORE edits. An alternative all-Option stored struct could retain one row but changes every setter's omission semantics; do not choose it silently. This is a concrete new storage decision, not permission to rewrite unrelated families.

No aggregate readiness failure blocks Start. Physical store/open/socket failures remain truthful operational failures; “start never refused” for unset configuration does not mean manufacturing success after an I/O failure. Existing stores requiring missing policy values for an upgrade must not receive invented seeds: classify that upgrade as structural and preserve absence, or expose a typed operation readiness requirement. Exact migration transaction consequences require the affected family review.

## Continuity and lifecycle

Absent continuity authorizes NO idle close/retire action. Resolve member/default only when an operation actually needs a continuity decision; missing declaration versus existing declaration with absent member/default remains distinct named readiness evidence. Preserve current seat and queues while awaiting values. The earlier both-unset Define acceptance remains natural under Configure; no launch-producing operation invents OnDemand or inherited profile policy.

Resume keeps the same flow/session/transcript and explicit admission/uncertainty lifecycle already designed, subject to its named required configuration being present. No Fable gate. Continues is named in the new chain but its exact authoritative shape and relation to the earlier version1-only field is requested; do not manufacture a provenance field before that answer.

## Warning and refresh

Configure owns warning rational share/message, threshold and native transport policy. Missing warning settings produces named readiness for that warning attempt, never a fabricated message/share and never an idle-close decision. Only new validated actual context is eligible. Below threshold and at/above configured share, attempt same-session warning under the agreed latch/native limits. At/above threshold skip warning and let configured refresh proceed. A missing refresh threshold cannot trigger refresh. No cached-row startup replay, Memory handover or Fable authority.

## Required coherent producer/consumer tests

- Start a fresh place with zero behavioral values; listener/control readiness exists, no policy seed or automatic lifecycle effect.
- Configure a single value/declaration atomically; read back exactly it; restart preserves Memory. Other values remain absent, not defaults.
- Operations with missing values name their exact keys and have no dependent effects. Configure needed peers in either order; the operation becomes ready only with a valid consistent set.
- Per-address upsert/remove preserves unrelated declarations and active seats; missing future declaration/continuity uses named readiness before successor/close/drain. Existing queued sends stay queued.
- Idle with no continuity takes no close action; configured close behavior acts only according to its explicit value. No address-derived runtime fallback.
- Warning share/message and refresh threshold configured through operations; actual context receipt/late jump/dedup tests remain. Stop hook/CLI routing regression is parallel FlowNexus step3, not asserted complete here.
- Nix/shell producers launch place alone then explicitly replay per-declaration Configure as external operations. Partial replay is visibly partial; no pretend atomic startup batch. No shell eval of Query text.
- Frozen predecessor bytes/unchanged families, new sparse-policy key/type decision and same-handle/fault proof remain independent acceptance gates.

## Exact step1 decisions still required

1. Authoritative Continues shape/semantics for052 (requested Psyche).
2. Sparse policy storage key/shape allocation versus optional singleton, and exact Readiness.Awaiting public/internal carrier reachability.
3. Bootstrap decoding/transport on a bare unconfigured Nexus: previous required five-budget Startup envelope is superseded, yet the parser cannot consume its configured Memory limits before finding/opening the place. Need the smallest explicitly intrinsic place decoder/control bootstrap boundary, or an approved external translator capability, with no hidden behavioral defaults. Existing adapter parser policies outside the Nexus must be distinguished from forbidden Nexus startup configuration.
4. Opening upgrade plan now excludes startup policy rows; identify which approved prepared structural conversions remain necessary and which APIs can shrink.

These are bounded consequences of the new ruling. Unchanged implementation and isolated accepted tests continue under the exact worker authority; affected code follows the resolved design and independent checks, not the superseded startup packet.

## Authoritative Continues ruling — resolves decision 1

Psyche core Primary supplied the exact domain during step1:

```ethos
Continuity.[ Continues Ends.IdleMinutes ]
IdleMinutes.Integer ; strictly positive
Set.[ Continuity.{ Address Continuity } ... ]
```

```datom
Configure.Continuity.{ { Psyche core Primary } Continues }
```

Continues keeps the flow hot: idle closes nothing; threshold refresh, Stop or Retire may end it. Ends.IdleMinutes closes the flow after that idle interval, preserving permaflow and queue. Absent continuity causes no closing action; it is lack of an action, not a manufactured Continues value. Model is likewise a per-address declaration alongside other one-declaration settings. Step2 waits on no further Psyche domain answer.

### Explicit reconciliation with the old accepted contract

The previous member Option<Maintained|OnDemand>/DefaultContinuity resolution and both-unset LaunchNotConfigured design is SUPERSEDED for this continuity domain. Do not keep it as a second active authority. Configure.Continuity is keyed by Address, separate from the other declaration settings. Readiness distinguishes an absent setting, but idle closing simply has no action when Continuity is absent. Do not classify absent continuity as a reason to close or silently install a default.

Exact old wire/persisted Continuity types and existing declaration V5 bytes must remain frozen for predecessor decoding. Neither Maintained nor OnDemand supplies an IdleMinutes value; especially OnDemand MUST NOT map to Ends with invented minutes. Proposed migration preserves frozen historical evidence and leaves the new separate continuity setting absent until explicitly configured; that means no idle close. Whether old Maintained may be explicitly converted to Continues requires Core's compatibility judgment, not a guessed equivalence. The final new declaration schema/storage layout must be revised coherently with the separately keyed continuity operation; the previously allocated unreleased V6 shape is not final under this supersession.

Read consumers needing review: successor.rs170–177; context/refresh and waking lifecycle uses of Maintained/OnDemand; retirement/idle scheduling; meta ConfigureMetaflow payload and its frozen history; snapshot and rendered Configure producers. Preserve the actual hot seat, permaflow and queue through conversion/replay. No blanket lifecycle rewrite outside those affected decisions.

Tests: explicit Continues remains hot across idle; absent emits no close and remains absent in readback; Ends positive interval closes only the flow after its measured idle deadline, retains Address/queue, and rejects zero/negative/overflow interval; configuration edits govern future idle timers without rewriting accepted deadlines unless explicitly ruled; threshold refresh/Stop/Retire still work. Test predecessor Maintained/OnDemand bytes with no fabricated minute value and new per-address explicit replay.

## Controlling bootstrap/storage rulings — decisions resolved

Psyche Primary: NOTHING is migrated from0.51 Memory. The new052 place starts bare, then external replay supplies Configure datoms, ONE PER FILE, including each Address's Continuity. Absent Continuity means no closing action. Remove old-store migration from this rollout's critical path; do not copy051 Memory or derive new continuity from old rows. Preserving frozen predecessor source/bytes is not authority to migrate the running store.

Mind Core Primary's exact design judgment:

1. ONE sparse RuntimePolicy family, keyed by typed Setting identity with Address in applicable keys, one typed configured leaf per row. Resolved operation snapshots are ephemeral and never seeded. This replaces the unreleased singleton allocation. Numeric coordinates must be explicitly confirmed, not inferred.
2. External typed translator boundary. Place text decoding and Configure text decoding are OUTSIDE the Nexus, with explicit translator-owned configuration/accounting available independently of Nexus Memory. Bare Nexus Start takes typed Place and opens Memory/control. Configure stores one typed value without needing general query policy. General operations resolve their five codec values from Memory. No five startup budgets, hidden parser caps or startup policies are smuggled into the Nexus. Concrete predecode/binary admission/opening limits must have named owners and actual sources.
3. Per-Address Continuity is a separate setting in the same keyed authority. Neither old Maintained nor OnDemand becomes a new continuity setting. In the new place it is absent until Configure. Absence authorizes no idle close and DOES NOT itself block launch. This overrides the earlier “both unset LaunchNotConfigured” member/default contract and all stale paragraphs in older artifacts. Continues/Ends positive minutes are the only new domain.

### Exact sparse authority proposed

Keep current one-declaration command types as the input vocabulary. Generate a typed `Setting` key and its corresponding typed `ConfiguredValue` once from those declarations; no string-key dispatcher or duplicate source-of-truth enum. Keys include the full Address for Continuity and per-Address model values; non-address leaf keys remain their distinct setting identity. A value can be stored only with its matching generated key. Configure rejects malformed/invalid values before one atomic mutation; removal yields actual absence. Snapshot/readiness decode typed values from one consistent read, no zero/empty/default fabrication.

Proposed unreleased coordinate replacement to request explicitly: table flow_nexus_runtime_policy, family flow-nexus-runtime-policy, MemoryVersion1/schema flow-nexus-runtime-policy-v1, NEW typed-setting-key encoding rather than singleton key policy. No released bytes exist for the old proposed singleton; confirm reservation replacement before source schema edits. Other reserved current coordinates are resume-headv1, resume-attemptv1 and meta-metaflow-configurationv6; the latter was allocated for an Option<oldContinuity> payload now superseded. Its final fresh-place payload/key layout must be reconciled rather than silently retaining that field or inferring a new number. Wire allocations currently signal44.0.0/meta60.0.0/commonFlow0.52.0 remain subject to this exact changed contract, with no publication claim.

### Translator and core split, concrete target

Nix/packages own explicit translator configuration as data separate from Nexus Start: the existing five typed codec limits and any transport admission byte limits. Package wrappers supply them to the actual text adapter before its first general parse. Configure files are individual external inputs; a shell replay invokes the configured adapter once per file, receives each typed result, and stops/reports at the first failure. No shell eval, no Nexus replay service and no implied all-files transaction.

The adapter decodes Place or a single Configure command using its own supplied limits, then submits the existing typed/binary contract to the core. The core distinguishes bootstrap control operations (Start/Configure/readiness/readback required for configuration) from general policy-dependent operations. It does not require its not-yet-set codec limits merely to accept an already typed Configure value. Binary frame admission still occurs before a typed value exists; actual framing/decoder limits must therefore be owned by the external translator/control transport, not assumed present in Memory. This precise producer/consumer path remains the bounded source verification to complete step1; do not call it implemented from this design sketch.

No old051 migration, all-family upgrade-plus-startup transaction, or startup overlay is part of new-place bootstrap. Reuse necessary safe store creation/opening and ordinary atomic Configure mechanisms; preserve prepared ownership/fault improvements where needed, but remove speculative migration prerequisites from delivery of this scope.

## Exact model authority reconciliation

Immutable meta281f defines ConfigureModel.{ Layer Aspect Native.String }, and Flow916 StoredMetaModelConfigurationV2 keys only Layer+Aspect (store.rs1010–1031/7760–7766). NamesConfiguredModel::configured_model(Address) ignores Topic when deriving that key (1340–1353). This cannot implement the living's model PER ADDRESS by merely retaining the old selector.

New command is `Configure.Model.{ Address Native.String }`, a single Address-keyed setting in the approved sparse authority. Its generated key includes full Aspect/Topic/Layer. No fallback to the old Layer+Aspect table. Remove the current Models whole-family setter from current052 writes; current snapshot/readback exposes explicit per-Address configured values. Newplace replay names each exact Address/model, including every intended existing seat; omission is named readiness for operations needing a model, not inherited policy. Old record/type code may remain frozen for historical tooling but is not consulted by new052 runtime policy.

Update actual lookup consumers: sending.rs553 launch/admission,1084 binding native choice,1271 recipient preparation; launching.rs256/707; binding.rs162; waking.rs2668/2864; store/metaflow.rs24; store.rs6092. Existing bound native seats/session identities remain observational facts; a newly configured future model does not rewrite the actual model identity of an already-running native process or a composed operation snapshot. Context thresholds must use the actual selected/bound model according to the operation's purpose, not retcon current usage to a newly configured future model.

Test two Topics with identical Aspect/Layer but distinct models; set/remove one leaves the other unchanged. Missing exact Address never selects another topic's model. Bind/adopt readback distinguishes actual native model from future configured model; refresh/launch captures current explicit per-Address choice once.

## Concrete predecode/control path replacing the old executable bootstrap

Source evidence identifies the exact hidden policy to remove: main.rs43–64 Start parser uses65536/1024;90 constructs environment defaults before open. CLI parsers likewise embed budgets; Nexus CarriesSignalFrames lib.rs1388–1440 and client reply readers use1MiB; configure-only main.rs243–266 sets5s timeouts. Those are chosen translator/transport values, not intrinsic Rust protocol constraints and not values already present in a bare store.

Concrete replacement composition: the packaged text/socket TRANSLATOR owns explicit typed TranslatorConfiguration (five parser counters, request/reply frame byte bounds, read/write/native call timeouts it actually uses). Its Nix-generated configuration is a separately supplied artifact, available before place decoding. The user-facing launch takes only Place text. The configured wrapper invokes the translator with that artifact plus the one Place argument; no shell parsing/eval. These values belong to the external translator, not Start or Nexus RuntimePolicy; a changed translator artifact does not overwrite Memory.

The translator decodes Place with its own five limits and calls the core's typed `start(Place)` in-process through the existing library boundary. This is an ownership boundary, not an invented second wire protocol: the same packaged executable can contain the outer translator and core library, but only the translator receives TranslatorConfiguration. The core sees typed Place, opens its new Memory and exposes typed control capabilities. There is no configuration vector inside Place/Start.

The outer socket translator owns length-prefix validation, frame allocation bounds, rkyv decoding and transport timeouts before calling a core method. Remove those code-owned caps from core CarriesSignalFrames and supply them explicitly at the translator instance. Configure decodes and admits a typed single declaration using those independently available translator resources, then calls core configure atomically. It does not require missing general-operation policy to store that policy. Binary length-prefix width and integer overflow checks remain protocol/arithmetic correctness, not configurable caps.

General operations resolve their own required core settings, including any core text-processing five-limit values, from Memory. Outer wire decoding is NOT evidence that those values are configured; ownership differs. Text work performed solely by the translator uses translator settings, not a duplicated live core value. Each actual counter has one owner; the source ledger must distinguish a codec used at the wire edge from a codec invoked by domain composition.

The external Configure replay tool uses the packaged translator with explicit configuration and a selected Place/socket, one Configure datom per file. Each command receives an independent atomic result/readiness outcome. A partial replay remains visible and restart-safe through idempotent per-setting setters; no Nexus auto-replay and no all-files atomicity claim.

A missing/malformed TranslatorConfiguration is a translator launch failure naming its input, not a Nexus refusal because Memory lacks behavioral values. A malformed Place/native I/O failure also remains truthful. No predecode parser reads its own budget using an unbounded general parser: reuse the approved fixed-field borrowed lexical bootstrap for translator configuration, with checked arity/range/canonical integer semantics; it is NOT part of Nexus Start. Exact independently supplied transport fields join the translator's explicitly typed input, with actual owned admission before allocation.

### Memory opening boundary still source-qualified

Current ConfigurationOnlyStore/FlowStore opens call EngineOpen(path,SchemaVersion), with no supplied operational codec/transport budget. Newplace construction may use fixed schema/layout identity and arithmetic correctness, but any lower chosen allocation/cache/resource policy still needs an explicit external storage-adapter owner/source or configured operation semantics. No source evidence yet proves those lower defaults are only correctness invariants. The bounded lower-layer pointer check is outstanding; this is a concrete step2 implementation evidence issue, not authority to seed Nexus Memory at startup or resume old-store migration.
