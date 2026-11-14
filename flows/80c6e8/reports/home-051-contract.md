# Home / actual Flow 0.51 contract — read-only report

Observed 2026-11-05 03:03 UTC. No implementation, activation, store change, seat migration, restart, unit removal, commit or push performed. The latest Core/Psyche ruling retires 0.44 and supersedes the predecessor legacy-evolution brief.

## Custody

Current seat is Mind criomosHome Secondary, flow 80c6e8. Field independently observed its native session and location, with Binding Unbound; location does not establish adoption. No edit custody acquired. Primary Home main is dirty at bacf040e4946f4e7a96635024bd339a11b09fc11. Predecessor reconciliation worktree /home/li/worktrees/criomos-home-merge-c3dba3 is held by lock 25318 under c3dba3, and its HEAD is 83784113ff9bf7689c8fe4b621d3d75449c0fb36 with staged changes. Neither is an immutable final candidate.

## Actual runtime and exact schema

`flow-nexus-051.service` is active, MainPID 4177139. `/proc/4177139/exe` and unit ExecStart agree:

- Runtime: /nix/store/5w5sqfmcndg8cr1dm72yr8iy591kmxsa-flow-configured-0.51.0
- Derivation: /nix/store/g76g8zqlimm79fxdjibrxd774bxwk71l-flow-configured-0.51.0.drv
- Its selected source: /nix/store/dz5dwigzydw2khv6wpgq3556hw83j4x7-source
- Cargo.lock SHA256: e92dd915d6ccb2398d01c8c3009916a80d423265539c42ef602c03d8e77e87fb
- meta-signal-flow 54.0.0: 281f5aa1b88cd43609c127cdf6f3c12645faf58b
- signal-flow 42.0.0: ce083f2ba9cc0bd928735ba4cc09e59965982e30

The exact meta schema has **nine wire positions**, preserving the eight earlier meanings plus an explicit optional workspace root:

```ethos
ConfigureMetaflow.{ Address Option<Root> SystemModules UserModules FlowKind ToolSet Continuity Purpose Records }
```

Root is String; None takes the Nexus source root. Actual source's flow-meta roundtrip test constructs root_option: None. Therefore “preserve all eight meanings” and “unchanged eight-position text” are different claims: the latter is incompatible with this schema. Adding a declared Root at the producer boundary needs explicit scope approval, not a field-dropping projection or runtime evolution.

The exact running meta-client successfully answered Configuration using the Invocation form `{ /run/user/1001/flow-051/flow-meta.sock Configuration }`. This witnesses read access to this actual runtime, not fresh-store initialization or equality of all declarations.

## Selected initializer and competing producers

The running unit's ExecStartPre selects /nix/store/b9czi957cxmhmmz197l9hgyddr5qb5vb-configure-flow-051/bin/configure-flow-051. Inspection shows both its --configure-only daemon and its flow-meta are the exact running package above. The client takes an explicit socket Invocation. Its Metaflows argument is /home/li/.local/state/flow-declarations/metaflows.datom, not the predecessor generated corpus. That current file has nine-position rows, explicit None roots, SHA256 1bbe91cf882260892b9ca9069596a4544b72021f27163ab1ea33cccea46a1142. It is mutable external state, not a durable immutable Home declaration.

The predecessor generator packages/flow-deployment/metaflows.clj is blob 383cdcff35e3e2470052f4370c0162084bfc6ce9 (authored Home 88ee5de4073b826060b865e03ff143971aca0c1a). It emits eight-position rows. Its old fresh-store failure against five-position 0.44 remains historical evidence, not a target 0.51 test.

The reserved Home worktree has another path: flow-051.nix imports flow-nexus-version.nix; that calls inputs.flow-051.lib.<system>.mkFlowPackage and consumes flow-nexus-config/metaflows.datom. This corpus SHA256 is 2035c4c21b7c3fb39c80de4219c13e97f18521a6ab4361e671ea0141b4134314, different from the running unit's corpus. The module explicitly redeclares Metaflows at every start; its comment says all rows OnDemand because that whole-family replacement resets Continuity. This is a semantic reconciliation item, not proof it preserves live declarations.

The worktree flow-051 input lock is 3a202a439f55d13b34c12c0255d232aeb8cba87f. That source's flake advertises 0.50.0 and keeps packages.default pointing to unconfigured-flow d3ab87ee18b1dd30947d5f0089f5abb4bafa80d5. No equality between that input and the actual running 0.51 source is established. Selecting inputs.flow-051.packages.default merely by name would not establish the target runtime.

## Selection plan requiring owner/Core approval

1. Reconcile custody of the occupied Home worktree before editing.
2. Obtain the deployment owner's reproducible source/configuration identity for the exact running package, not a version label. Pin/select that explicit configured package path coherently for daemon, initializer, validator and clients.
3. Choose one authored semantic corpus and explicitly include the supported Root option at its configuration edge; preserve Continuity, Purpose and Records. Resolve the competing restart-time replacement policy against durable live declarations before effects.
4. Prove the generated declaration parses and is accepted by the exact selected target in an isolated fresh store, then separately witness preserved-store behavior. No current full-green or fresh-install proof is claimed.
5. Remove 0.44 units only after the runtime owner supplies supported seat inventory and the last seat is off. No migration or kill is inferred.

## Seats / removal gate

`flow-nexus.service` (canonical 0.44) was inactive, MainPID 0. A distinct `flow-nexus-harnessflags.service` remained active, MainPID 2351217, executing /nix/store/r1k4wad7zdic9mg24fkqpqjx8xf58f0q-flow-configured-0.44.0 against flow-harnessflags state. Neither observation proves seat emptiness.

One read-only legacy `List` query attempt was refused by client parsing before connection; it yielded no inventory. No further 0.44 query is undertaken under Core's latest no-scan/no-live boundary. Mind versionZero Primary explicitly does not own inventory: its own adoption on 0.51 proves only its address, not descendants. Core Secondary is asking Psyche core Secondary/deployment owner for the supported inventory route. Remaining 0.44 seat set is UNKNOWN; removal is held.

Wants-only dependency changes remain separately reviewed and certify neither declaration compatibility nor runtime adoption.

## Subsequent scope ruling

Core approved the explicit nine-position shape with None immediately after Address and the other eight meanings preserved. Core Secondary then held implementation READ-ONLY pending reproducible configured-package identity, corpus/restart Continuity policy rulings, and verified edit custody. Field core Primary was asked to establish custody and an implementer, then immediately sent the superseding hold: owner/custody identification only, no implementation. The sequence after approval is custody receipt, coherent producer/selection correction, isolated fresh initialization and semantic roundtrip plus separate preserved-store witness, immutable diff/check report, then Core landing judgment. No publication authority is inferred.

Core's next read-only request is a semantic per-address delta between the authored Home corpus and the deployed mutable file: added/removed addresses and roots/modules/kind/tools/continuity/purpose/records, with reviewed authority or unknown for every difference. Forwarded to Field core Primary through its existing custody chain, with exact earlier file hashes and drift checks requested. Authored reviewed Home is eventual authority; deployed state is evidence, not an automatically chosen source. Restart replay needs proof of intended per-seat configuration/state preservation; existing ExecStartPre does not grant that policy. No deployment/initialization effects authorized. None insertion is approved only in isolation, separately from unresolved package/corpus decisions.

## Sole corpus audit returned by Field core Secondary 2885c5

The one bounded reader compared exact A/B paths and SHA256 identities above. Before/after/after-parse hashes matched; no drift witnessed. Snapshots parsed in memory; no source edits, effects or lock changes. Schema witness is this report's exact-runtime evidence, not an independent source-tree scan.

Both corpora are already nine positions in exact declared order, with explicit Root=None on EVERY row. The approved None insertion applies to the separate historical eight-position generator; these corpora need no such insertion.

A (authored) has 34 addresses; B (deployed) has 67. Zero A-only addresses. Authored order remains a subsequence. Twenty-seven common rows are identical in every field. Seven common rows differ only in UserModules, replacing vision:metaflow-v1 with vision:complex-v1:

- Mind beliefNexus Primary
- Mind beliefNexus Secondary
- Mind versionOne Primary
- Mind versionOne Secondary
- Psyche codexManager Secondary
- Psyche core Primary
- Psyche core Secondary

For each substitution independently, REVIEWED AUTHORITY UNKNOWN. Address, Root, SystemModules, FlowKind, ToolSet, Continuity, Purpose and Records remain identical.

### Thirty-three B-only addresses

Every addition has Root=None, FlowKind=Regular, ToolSet=Default, Continuity=OnDemand, Purpose empty, Records empty. REVIEWED AUTHORITY UNKNOWN for EACH addition independently. SystemModules and UserModules match the following groups exactly, preserving order.

G1 addresses (2): Field kinks Primary; Field kinks Secondary.

SystemModules:
```datom
[ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom intent:energy knowledge:flow-messaging knowledge:search ]
```
UserModules:
```datom
[ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles vision:account knowledge:context-strata ]
```

G2 addresses (21): Mind belief Secondary; Mind chronos Secondary; Mind criomosHome Secondary; Mind datomCodec Secondary; Mind energyNexus Secondary; Mind ethosZero Secondary; Mind flowNexus Secondary; Mind garbageTests Primary; Mind garbageTests Secondary; Mind herdrNexus Secondary; Mind lojix Secondary; Mind memoryEngine Secondary; Mind metaflow Secondary; Mind nixCriomos Secondary; Mind nixCriomosHome Secondary; Mind nixEthosTest Secondary; Mind nixFlowTest Secondary; Mind nixMessageTest Secondary; Mind orchestrate Secondary; Mind protos Secondary; Mind signalSema Secondary.

SystemModules:
```datom
[ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models intent:energy knowledge:flow-messaging knowledge:search ]
```
UserModules:
```datom
[ vision:ethos vision:datom knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles vision:flow-nexus vision:account knowledge:context-strata ]
```

G3 addresses (2): Psyche audit Primary; Psyche flowAudit Primary.

SystemModules:
```datom
[ spirit:core spirit:psyche spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules intent:fable intent:anatomy intent:conversion intent:protos-parsing intent:startup-prompt knowledge:flow-messaging knowledge:search ]
```
UserModules:
```datom
[ vision:nexus vision:flow-nexus vision:ethos vision:datom vision:signal vision:proposal vision:psyche vision:remembering vision:model-roles vision:belief-modules vision:collaboration vision:crystallization knowledge:vocabulary knowledge:psyche vision:nexus-v1 vision:herdr-nexus-v1 vision:flow-nexus-v1 vision:belief-nexus-v1 vision:complex-v1 ]
```

G4 addresses (5): Psyche audit Secondary; Psyche flowAudit Secondary; Psyche garbageTests Secondary; Psyche language Secondary; Psyche tools Secondary.

SystemModules:
```datom
[ spirit:core spirit:psyche spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules intent:anatomy intent:conversion intent:protos-parsing intent:startup-prompt knowledge:flow-messaging vision:proposal knowledge:search ]
```
UserModules:
```datom
[ vision:nexus vision:flow-nexus vision:ethos vision:datom vision:signal vision:psyche vision:remembering vision:model-roles vision:belief-modules vision:collaboration vision:crystallization knowledge:vocabulary knowledge:psyche vision:aspects vision:account knowledge:context-strata vision:nexus-v1 vision:herdr-nexus-v1 vision:flow-nexus-v1 vision:belief-nexus-v1 vision:complex-v1 ]
```

G5 addresses (3): Psyche hostClean Tertiary; Psyche search Tertiary; Psyche undone Tertiary.

SystemModules:
```datom
[ intent:context spirit:core spirit:ghost spirit:psyche intent:main-flow intent:living-interaction intent:psyche intent:design intent:models intent:energy knowledge:flow-messaging knowledge:search ]
```
UserModules:
```datom
[ knowledge:vocabulary knowledge:psyche vision:crystallization vision:aspects vision:model-roles vision:flow-nexus ]
```

These are observed declarations, not an approved merge. Staged authored placement and active initializer argument establish neither reviewed authority nor restart policy. The historical eight-position producer remains separate. No corpus selection, replay, Continuity reset, package selection, initialization or deployment is granted by this audit. Editing custody remains unresolved.
