# Harness release3kyf — successor of074047

**Open:**3kyf; daxc SessionId consumer rename. Original1p59 answered2ac0: gcyd defers Identifiable/identify; keep ClaimIdentity, no hash/Identifier. Original obligations/audit:92d3be/de6298 handovers. Detailed continuation history: this file at commitfc467f4dd.

**Custody:** actual420 core/tests;432 isolated library/contracts;429 handover, owner074047. All workers stopped, all trees clean. Preserve canonical refs/anchors. No heavy grant, compilation/tests, publication, dependency regeneration or deployment; generator/format checks are not a gate.

## Exact source

All paths below are under `/git/worktrees/`:

| Worktree | Branch | HEAD |
|---|---|---|
|codex-harness-nexus-mend-de6298|mend-de6298|`ecbfc11d421f4f98104b54ebe62751661f1dd8ba`|
|codex-harness-nexus-tests-mend-de6298|mend-de6298|`dfbeb08c6769ab5af055a1aadf5b247c4802b541`|
|harness-nexus-library-074047|harness-sessionid-lock432|`bf8613a0ea18ec34976b07ddb02e8ee60d53b88c`|
|signal-codex-harness-nexus-074047|signal-refusal-lock432|`b80a1035f3ea190381afcd974d1cee44ed68fac8`|
|meta-signal-codex-harness-nexus-074047|meta-refusal-lock432|`d95a8580c7f6839f07ac10f63218b7bab142d909`|

Core HEAD is **SOURCE-WIP, incomplete/non-compiling expected**. `nexus.rs`: CoreActor<Translator,Opening> owns Store/translator/publishers/SessionsWatch/Opened; local native-handle HarnessNexus wrapper uses Kameo blocking_send. Generated NexusPort is sync facade; mutable NexusRuntime performs operations. Generic PublicOpening stages+publishes+sets Opened in actor order (Psychem9oy). `watching.rs` owns callback-translated notify vocabulary and directory/explicit-rollout targets. FoldRefusal imports signal; native From projection lives in signalb80a103. StoreOpening/Familial are generated static capabilities on real types.

**Daemon still uses old locks/API/OnceLock.** Next replace it with runtime-before-bind/wrapper/PublicOpening integration, generate remaining daemon/watch traits, settle startup/test constructors. Preserve F1/audit mends. Update flake generation list for translator_settings/new schemas after reading ordinary rust-nix-example. No free/inherent helpers, own locks, empty behavior markers or orphan impls.

Translator sourcec86b1d8 integrates settings actor, SessionId, typed failures/checked budgets and preserves unrelated meta replies. Ready=ValidTextBudget depends on shared fix below; Option-only ready failure remains a gap. Tests cover stale reads, restart/appends, immediate/outside/symlink paths, malformed rows and typed startup UnwatchableDirectories, but were not run; actor-failure/constructor tests await core API.

## Next sequence

1. **nm6g approved, not implemented:** ordinary ReportedUnwatched.RolloutWatchFailure; RolloutWatchFailure.{FilePath Diagnostic}. Report remains committed/pending when watch placement fails.
2. **j0uc approved, no shared custody yet:** native TextBudgeting for ValidTextBudget in owning translator-serving, own commit. Ask Core for isolated exact path/ref coordinated with subscription owner; all other serving consumers must be gated. Core notifiedt6zo (Uncertain; do not blindly resend). No local Ready wrapper: native ValidTextBudget lacks archive traits; TextLimits has them.
3. Finish whole actor/SessionId consumer integration. ActorUnavailable.Diagnostic ordinary/meta and TranslatorUnavailable.Diagnostic meta are approved/in schemas; Poisoned/HeldLock removed, so whole-cohort compatibility needs audit. Keep SessionRecord/SessionStart names; tentative notification types do not exist. Versions library0.2/ordinary0.5/meta0.5 are proposals, not allocation/publication approval. Core querywwlx proposes core/daemon/translator/tests0.2; unanswered.
4. Submit committed write-set/dependency/resource PLAN before metadata generation. Accepted base7fca4d583adfd2354903c59cbc7f5e928e1baa76 registers Kameo0.22.2/macros0.21.1. No accepted f2wj packet received; subscription76b588 owns it; old WIP refs are not adoption pins. No inherited slot; priority Flow gate first. Canonical build-base history differs; inherited registry worktree build-base-msc030.
5. Complete builder gate on committed published revisions; packet to Psyche for independent audit by another flow. **Mind harnessNexus Opus held; do not wake.** No merge/deploy before audit; Field core Sol deploys. Keep3kyf open.

Generator: `/nix/store/dfz5drcy3c2afy5558ccr03iz3998zzr-rust_ethos-zero-30.1.0-bin/bin/ethos-zero`, pinned415c370 proof in92d3be. No local cargo/evaluation. Kameo cache verifies blocking_send; public serving uses spawn_blocking, meta/translator OS threads. In-process adapters require explicit runtime/blocking context.
