# 052 step1 controlling design

Owner4f3cb8 through coordinator74026a; Task60 receipt00:26UTC, deadline01:26UTC. This document controls over the older startup-overlay/memberContinuity proposals. It preserves their unchanged implementation/verification work, not their superseded policy.

## 1. Start and ownership

Start contains Place ONLY: explicit store, ordinary socket and meta socket identities. New place has new Memory. NO051 Memory import, seed, upgrade-to-policy, copy, startup settings vector or automatic replay. External shell replay is ONE Configure datom PER FILE. Each replayed declaration is one atomic operation; partial replay is visibly partial.

The executable's outer typed translator receives its independent, explicit Nix-produced TranslatorConfiguration before reading Place/Configure text. That configuration owns five parser limits, framing byte limits and actual translator transport/native timeouts. The configured wrapper supplies the artifact and passes the user's Place argument unchanged. The translator decodes Place and calls core typed Start; the core does not receive those policies as Start fields or insert them into Memory. Core and translator may be separate modules in the same executable/library composition; no new IPC protocol is required.

The outer adapter owns length-prefix checks, bounded allocation and binary archive decoding before delivering typed requests. It accepts typed Configure without requiring unset general-operation values. General domain operations resolve THEIR needed policies from Memory. Codecs used at the wire edge and codecs used by domain composition have different owners; share types, not fictitious shared live values. No hidden65536/1024/1MiB/5s/defaultChain remains at the observed parser/socket sites.

Store-opening resource policy likewise belongs to the externally configured storage adapter, not fabricated bare Memory. Schema/layout identifiers and arithmetic checks remain correctness invariants. Actual redb/Engine resource-control parameters and native failure boundaries must be traced and explicitly supplied where chosen; absence of an EngineOpen parameter is not proof that lower defaults are intrinsic. This is a concrete implementation/test obligation, not authorization to reintroduce Nexus startup configuration.

Malformed Place, malformed translator inputs and native I/O failure remain truthful failures. Lack of a behavioral Memory value never refuses bare startup. Core control/readiness/configuration stay available so values can be supplied.

## 2. One configured declaration, one authority

Generate the setting-key and value projection once from the typed Configure vocabulary. Every applicable key includes its complete Address; topic is not discarded. A stored value is a typed sum variant whose key is derived from that variant, so callers cannot pair an unrelated key/value. Use existing configured-setting types where meanings match. No string dispatch, synthesized scalar default or duplicated active family.

Sparse RuntimePolicy authority: table `flow_nexus_runtime_policy`, family `flow-nexus-runtime-policy`, MemoryVersion1/schema `flow-nexus-runtime-policy-v1`, one generated Setting-keyed configured leaf per row. Core explicitly replaces the unreleased singleton `policy` layout with this layout. Ephemeral operation snapshots group typed values after consistent reads; they are not seeded or persisted a second time. Current candidate bytes must be witnessed absent for the superseded singleton before writing the new layout.

Configure validates the one present value's domain, uses the store-private writer guard, reads a consistent view, checks applicable present-peer constraints, and commits one atomic change. Missing peers are absence, not a reason to block configuration itself. An operation validates all its required values and cross-field constraints before effects. No startup batch is needed. Existing unrelated family policies remain only if their values genuinely form one declared setting; a vector of independent Address declarations is not one setting.

Per-address declarations use approved `Metaflow.ConfigureMetaflow` upsert and `RemoveMetaflow.Address`; outcomes Replaced/Unchanged are idempotent. Snapshot collections remain observations. Omitted Addresses preserve Memory. A remove does not end a live seat or rewrite composed work. Current declaration payload excludes obsolete Continuity, and Core retains the allocated meta-metaflow-configurationV6 coordinate for that fresh-place shape.

Model is `Configure.Model.{ Address Native.String }`, keyed by full Address, replacing the old Layer+Aspect model-family selector. No topic-blind fallback. Actual bound native model/session remains an observed identity, distinct from configured policy for a future launch/refresh.

## 3. Named readiness before effects

Use a typed missing-setting identity, generated from the same Configure vocabulary, including Address/model/key where needed. `Readiness.Awaiting` identifies the actual missing keys; it is not a generic NotConfigured string. Resolve only the values needed by the requested operation from one consistent Memory snapshot. Missing or invalid required configuration prevents that operation's dependent effects, preserves existing seat/queue and is surfaced truthfully.

Do not add a shared persisted Refusal variant just for naming symmetry. Each affected existing direct operation boundary must expose the named readiness through its typed result; local Wake outcome needs a local declaration/readiness carrier because current Failed_Data cannot express it. Actual wire/archive reachability is checked before enum edits. Current signal44/meta60 allocations are retained; any newly exposed persisted family change is reported, not silently extended.

Existing accepted queued delivery remains accepted/queued when a configuration-dependent wake awaits values. Do not fabricate terminal failure, consume its queue, create a successor, close its held seat or label readiness as a Herdr failure. Later normal explicit activity can retry once configured; no new hidden timer is implied.

## 4. Continuity, exactly as ruled

```ethos
Continuity.[ Continues Ends.IdleMinutes ]
IdleMinutes.Integer ; positive and checked for the actual duration conversion
Configure.Continuity.{ Address Continuity }
```

Continuity is a separate per-Address setting in the same keyed authority. Continues keeps the flow hot: idle closes nothing; threshold refresh, explicit Stop or Retire can end it. Ends closes the flow after its configured idle minutes while retaining permaflow and queue. ABSENT causes NO closing action and DOES NOT itself block launch. That is absence of an action, not a Rust default value.

Old Maintained/OnDemand types stay frozen where historical source tools still need them, but neither is migrated to the new place. Remove old member Option/defaultContinuity fallback authority. No invented Ends interval. Explicit Configure replay supplies desired new Continuity for each Address.

Idle timers capture the configured interval and native/lifecycle identity; stale timer completion must not close a different generation or a seat now kept hot by a newer explicit policy. Exact rescheduling/cancellation mechanics are part of lifecycle implementation/tests, not an excuse for an implicit close while absent.

## 5. Resume, warning, threshold, Adopt

Resume preserves original FlowId/native session/transcript, exact address admission and staged durable uncertainty semantics from the accepted Resume design. It resolves only its needed configured settings before effects. No Fable gate, StartedBy or security substitute.

Warning share0<N<=D and nonempty literal message are Configure values, not startup values. Only newly validated actual context receipts can evaluate. Below threshold and at/above the share cutoff, same-session warning uses the approved transient crossing latch. At/above threshold, skip warning and continue configured refresh; share1 has no pre-threshold opportunity, no clamp. Missing threshold cannot trigger refresh. Native submission is enough, never claimed model read; stale composer placement/possible-effect timeout are uncertain. Contention skips warning without blocking settlement. One explicitly owned native deadline and kill/reap prevent detached later submission; inherited Engine waits are not advertised as a hard aggregate deadline. Exact lower runner/typed outcomes remain the warning implementation delta test obligation.

Adopt preserves actual identity/transcript/work; adopting a seat is NOT proof its existing hooks now route correctly. STEP3 separately proves generated/packaged hook and CLI reach the Nexus holding declarations and diagnoses the actual CodexAwake queue-stall witness. No guessed cause is coded as a fix.

## 6. Reused mechanisms and discarded work

Keep necessary safe same-handle backend ownership, private scoped decoded-value inspection, atomic configuration changes, exact native error/first-mutation evidence and existing reserved Resume families. Redb1bd's escaping owned-table facade is rejected: corrected borrowed facade must expose only scoped decoded values; independent signature fixtures pass, future repository-body/fault proof remains required. Do not retain migration/opening-plan complexity solely to batch removed startup policy or import051 Memory.

No new source writer: existing native01a1adee-75af-7043-a7cc-1ffa6eedf393 is preserved. Its current owner/control/ruling ACK and custody must be positively reconciled before new source instructions. Local independent test fixtures are not replacement implementation authority.

## 7. Required tests and implementation evidence

- Fresh bare Place starts with zero behavioral rows; control Configure/readiness works. No seed or automatic close/refresh. Restart preserves configured Memory only.
- Single-declaration set/readback/remove and idempotence; unrelated Address unchanged; model full-Address isolation. Configure peers in either order, named Awaiting until ready; invalid value refuses atomically.
- RuntimePolicy sparse key/value agreement, absent snapshots and no singleton materialization. Exact current wire/datoms/rkyv and current producers updated coherently; no051 import.
- Continuity absent/Continues idle no-close; Ends validated minute boundary, stale timer/generation/config change and retained queue/permaflow; threshold refresh/Stop/Retire unaffected.
- Resume exact native identity, staged crash/ambiguity and no repeat emission; truthful readiness without draining queued work.
- Warning actual receipt, exact arithmetic/share1/latejump, same-session/dedup, missing values, no stale lower rearm, subprocess deadline/cancellation and truthful uncertainty.
- Translator actual predecode/framing/Configure-before-Memory proof using explicit independently available configuration; every observed hidden cap replaced at its true owner. Store resource policy must be accounted, not assumed intrinsic.
- STEP3 two isolated places, actual rendered hooks/CLI/Stop transcript correlation and decoy routing; Codex stall cause and regression require witnessed diagnostics. Existing baseline tests are not052 candidate proof.
- Exact pinned source/consumer review, independent changed-body/fault tests, coherent dependency pins and native testing capsule follow before rollout. No publication, native process or deployment effect is inferred from this design.

## 8. Chain and concrete outstanding execution facts

STEP1: controlling design recorded here; outstanding source details are named implementation evidence, not requests to reapprove the living's scope. STEP2: code/tests240min from coordinator's recorded actual completion of this step. STEP3: 56a9b8 parallel, ACK00:42:18/deadline02:42:18. STEP4: testing capsule/native proof120min after step2. Coordinator owns5/6/7; no rollout now.

Execution facts to carry explicitly: latest exact worker ruling ACK is not yet witnessed; Protos one authorized remote attempt status remains unknown and must not be replayed; redb body escape needs corrected implementation/fault verification; dependent builds need authorized exact immutable materialization; no current coherent052 artifact exists. These facts do not erase completed independent fixture/test evidence or authorize duplicate writers.
