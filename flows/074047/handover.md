# Harness release 3kyf — successor of074047

**Open:**3kyf (Done only with committed/gated candidate), daxc (SessionId consumer rename). Original1p59 answered2ac0: Psyche gcyd defers Identifiable/identify; keep ClaimIdentity, add no hash/Identifier. Read predecessor92d3be and de6298 handovers/audit for original obligations; longer continuation detail survives in this file at git commitfc467f4dd.

## Custody and source

Actual locks owner074047:420 core/tests mend worktrees;432 three isolated library/contracts below;429 this handover. Preserve canonical refs/WIP anchors. All workers stopped after source commits; no background writer remains. No heavy grant, compilation/tests, publication, registry edit, dependency regeneration or deployment occurred. Source rustfmt/diff checks and limited pinned Ethos generation are not a gate.

| Worktree under `/git/worktrees/` | Branch | HEAD |
|---|---|---|
|codex-harness-nexus-mend-de6298|mend-de6298|`ecbfc11d421f4f98104b54ebe62751661f1dd8ba`|
|codex-harness-nexus-tests-mend-de6298|mend-de6298|`dfbeb08c6769ab5af055a1aadf5b247c4802b541`|
|harness-nexus-library-074047|harness-sessionid-lock432|`bf8613a0ea18ec34976b07ddb02e8ee60d53b88c`|
|signal-codex-harness-nexus-074047|signal-refusal-lock432|`b80a1035f3ea190381afcd974d1cee44ed68fac8`|
|meta-signal-codex-harness-nexus-074047|meta-refusal-lock432|`d95a8580c7f6839f07ac10f63218b7bab142d909`|

All clean at worker terminal receipt. Contracts were created from exact approved library8e987849, signal64471468 and meta4a12f25 anchors (canonical→anchor ancestry checked). Proposed versions library0.2/ordinary0.5/meta0.5 are source proposals, not registry/publication acceptance. Core querywwlx proposes core/daemon/translator/tests0.2; unanswered.

## What the source now does — and does not

**Core HEAD is explicitly SOURCE-WIP, not compiling release evidence.** `nexus.rs` now has `CoreActor<Translator,Opening>` owning Store, translator, publishers, SessionsWatch and Opened. Local native-handle `HarnessNexus { actor:ActorRef<CoreActor<...>> }` uses Kameo blocking_send. Generated `NexusPort` is the sync facade; mutable `NexusRuntime` handles report/configure/perform/watch/initialize/open/subscriptions. Listener stage+publish+Opened is one actor transition through generic PublicOpening; daemon native PublicListener shares Arc<Listeners> with acceptors. `watching.rs` classifies configured directories vs explicit rollout files, converts notify at callback to owned generated vocabulary, supports outside-dir paths. FoldRefusal is imported from ordinary signal, not duplicated; signal-owned native From projection is inb80a103. StoreOpening/Familial are generated static capabilities on actual data/native Store, no empty behavior markers.

**Next required code:** daemon still uses OLD locked API/OnceLock and must be replaced with wrapper/runtime-before-bind/PublicOpening integration; startup/test constructors are not finalized. Update generation-check file list for translator_settings/new daemon schemas after reading ordinary rust-nix-example. No free functions except main, inherent helpers, own state locks, orphan foreign/foreign impls or empty behavior namespaces. Remaining handwritten daemon/watch capability traits must be generated. Preserve F1 stale-reading guard and audit mends.

Translator sourcec86b1d8 integrates separate settings actor (no RwLock), typed TranslatorUnavailable, SessionId, checked budgets, preserves unrelated meta replies; generated settings actor owns/joins runtime at synchronous OS-thread boundary. `Ready=ValidTextBudget` now REQUIRES the shared native TextBudgeting impl below. `ready()` Option-only failure projection remains an explicit gap. Tests cover SessionId, F1/F3/F6/F7/F10, outside path/symlink, pair restart/live append, typed startup UnwatchableDirectories; no tests executed. In-process ctor and actor-unavailability tests await new core API.

## Latest rulings and next sequence

1. **nm6g approved:** add ordinary `ReportedUnwatched.RolloutWatchFailure`, `RolloutWatchFailure.{FilePath Diagnostic}`; hook stays committed/pending when path watch placement fails. Not added yet. Wire into core projection, never Memory/Unreadable/ReportRefused.
2. **j0uc approved:** implement `TextBudgeting for ValidTextBudget` once in owning shared translator-serving, its own commit; Ready stays native, no local wrapper. Shared source custody/reference NOT acquired. Ask Core to coordinate exact isolated path/ref with subscription owner; every other translator-serving consumer must be built. Core notifiedt6zo (Uncertain; do not resend blindly). `ValidTextBudget` lacks archive traits; `TextLimits` does have them.
3. Finish whole core/daemon/translator/tests consumer integration, SessionId/session_id everywhere scalar id, retain SessionRecord/SessionStart names. Tentative notifications absent from actual code; invent none. ActorUnavailable.Diagnostic ordinary/meta and TranslatorUnavailable.Diagnostic meta approveda6ju and in contract sources; obsolete Poisoned/HeldLock removed, so old consumers are incompatible until whole actor release.
4. Submit exact committed write-set/dependency/resource PLAN to Core before metadata generation. Accepted base7fca4d583adfd2354903c59cbc7f5e928e1baa76 registers Kameo0.22.2/macros0.21.1; use minimal Cargo features, not registry closure strings as flags. No f2wj accepted release received: subscription76b588 owns it; old129206c/be5c3f9/8405b0a are WIP, not adoption pins. No inherited heavy slot; priority Flow gate precedes this. Canonical build-base has unrelated history; inherited registry worktree is build-base-msc030.
5. Gate complete checks on builder against committed published revisions, then send packet to Psyche core Opus for independent second audit **by another flow**. Mind harnessNexus Opus is held; do not wake it. No merge/deploy before audit. Field core Sol deploys accepted candidate. Keep3kyf open.

Pinned ethos executable `/nix/store/dfz5drcy3c2afy5558ccr03iz3998zzr-rust_ethos-zero-30.1.0-bin/bin/ethos-zero` matches415c370 proof in92d3be handover; use Check/Generate, no local cargo/Nix evaluation. Native Kameo0.22.2 cache confirms blocking_send; public serving is spawn_blocking, meta/translator sync OS threads. Generic runtime adapters are not arbitrary async-context safe.
