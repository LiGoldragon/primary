# Harness continuation 074047 — task 3kyf remains open

## Custody and instructions

Mind harnessNexus Sol 074047 succeeds 92d3be. Continue from `flows/92d3be/handover.md`, then `flows/de6298/handover.md` and its named failed audit. The original notions/crystallization were read in this continuation. The later Psyche rulings in 92d3be's handover supersede Locking and native WatchWord.

Core actually released Lock418 and acquired Lock420 `harnessMends074047`, owner074047, over exactly:
- `/git/worktrees/codex-harness-nexus-mend-de6298`
- `/git/worktrees/codex-harness-nexus-tests-mend-de6298`

Both remain on branch `mend-de6298`; do not edit the canonical daemon checkout. Release420 only after terminal handoff. Lock429 owns this flow's handover directory. Primary commits only its own report files; source workers commit only their own files.

Psyche 6rzg corrects the release chain: **Mind harnessNexus Opus is held and must stay asleep.** Send the committed complete gate packet to Psyche core Opus, who arranges an independent second audit by another flow. No merge or deployment before that audit. Field core Sol remains the deployer. No heavy grant exists. Core says source lanes run in parallel, subscription ahead of Harness on collisions, bounded gates interleave only after explicit packet admission. No local cargo/Nix evaluation or compilation has run.

## Source checkpoints

Core inherited `c35fa34c68d3f2d92ca0a020c107dc07eb17ebef` and tests inherited `cae20b24b35ab0b187d01c37dd240d6c0941def6`.

Core source checkpoints now:
- `ea0f7ee0f80e7ec3afb2d8ff5eab5397b9e1d9da`: `actor.ethos` and generated owned WatchWord/Event/Failure/Consequence, callback conversion from notify, checked signed watch generation, folder-create/rename-from semantics, generated ListenerFailure, daemon consequence consumption. Also includes minimal workspace/core/daemon Kameo manifest edges and generation-check file list, **without lock/Cargo.nix regeneration**.
- `94c1540d2d2a27ba7694442fe77aeb1a73b4b23f`: corrects helper placement from the preceding intermediate checkpoint. Placement/coverage capabilities are generated traits; notify conversions are native From interactions; no inherent SessionsWatch constructor.

These have pinned Ethos Check/Generate, formatting and diff-check evidence only. No Rust type-check, tests, or complete gate. Core locks and readiness migration remain unfinished. Generated traits must replace handwritten behavior; free functions and inherent methods are not a way around F2.

Tests HEAD `5770d573f6675a57b21bf545713ecdef2f5fcdd0` contains:
- `9fd96cb`: outside-configured-directory hook path, canonical/symlink path, and real pair restart/live append regressions;
- `4fd9ed3`: moves started_with to existing Pairing trait;
- `5770d57`: removes stale socket files only after the old pair's children are confirmed reaped. Pinned serving only unlinks in OwnedListener Drop; direct SIGTERM cannot be assumed to run Drop.

Exact restart test scope: rows persist through restart, then completion rows are appended **after** restart. It does not yet append rows while daemon is down. Tests were formatted/diff-checked, not executed. F9 startup typed readiness and F8 additional typed caller refusals are deferred until the contract cohort is adopted.

## Active workers at this snapshot

Two Luna/xhigh workers, bounded source-only, no heavy/SSH/gates:
- `/root/actor_bodies`: core + daemon + root minimal Kameo manifest edge. Owns actor ownership migration, remaining F2 capabilities and generated vocabulary; no translator/tests worktree edits.
- `/root/actor_tests`: completed tests above, now owns **only** `crates/codex-harness-translator/**` in core worktree. Separate settings actor, generated TranslatorSettings/limits/errors and remaining translator F2 capabilities. May add kameo.workspace and tokio.workspace member edges; versions/features stay existing workspace/base values.

There is a withdrawn initial worker `/root/actor_migration`; it was interrupted immediately and told to do no work because its full fork could not guarantee the non-Sol model constraint. It holds no source custody. A later attempted translator worker spawn failed at lifetime thread limit, so actor_tests was reused. Before refreshing, obtain final worker checkpoints and stop/close active work rather than leaving writers unbriefed.

## Actor boundary question li9u

Core sync Answering APIs run on shared spawn_blocking paths; translator dispatch is on OS threads, per inherited pinned-source evidence. A single core actor owns Store/publishers/watch mutable state and Opened; a separate translator settings actor avoids synchronous emission re-entry.

Readiness requires stage_public + publish_public inside the same serialized actor transition, setting Opened only after success. A boolean actor operation followed by outside listener staging has a race/failure window and was refused in review.

Worker inspected pinned `nexus-serving::Listeners`: no Clone, but stage/publish/accept all take &self; native Arc sharing is plausible. Preferred proposed shape, sent to Psyche in li9u/stwz, awaits ruling:
- generated PublicOpening capability returning Result<Opened, ListenerFailure>;
- daemon native runtime wrapper owns Arc<Listeners<CodexHarness>> and implements capability;
- generic core actor owns wrapper plus Opened/core state, stages and publishes synchronously;
- acceptors clone only native Arc.

Use a daemon-local wrapper, not an orphan impl of core trait directly for external Arc<Listeners<_>>. Worker continues unrelated actor/F2 source while readiness body waits for ruling.

## Translator boundary question byb4

Pinned MetaTranslating.settle returns Settling<Output, Forwarded> and has no error case. A local settings actor ask/send can fail; current meta ConfigurationRefusal has no faithful cause. Psyche byb4 asks permission for ConfigurationRefusal.TranslatorUnavailable carrying typed actor failure, returned as an answered refusal. Do not label actor failure InvalidTextBudget. Generated settings/actor work may proceed; hold only missing failure projection.

For bootstrap errors currently &'static str: generate TranslatorBootstrapFailure variants for actual existing refusal causes, not a string-wrapper substitute. Worker must send exact variants for review. Generated i64 limits need checked native conversion. Runtime lifecycle must own/stop actor work, not silently detach it.

## Dependency and rename work still open

Core requests yvv7 (custody, answered), r6w6 (harness-library/consumer rename custody), 8qmr (accepted Kameo registry packet) were sent. Existing inherited registry worktree `/git/worktrees/build-base-msc030` contains registry kameo0.22.2 and kameo_macros0.21.1, Kameo default/macros/tracing; canonical build-base has unrelated history and is not the source to modify. Source manifest edges are allowed against that exact existing set; lock/Cargo.nix generation still needs a bounded builder packet and explicit grant. No f2wj WIP revision is adopted. Subscription owner76b588's 129206c/be5c3f9/8405b0a were WIP, not accepted landed releases. Request jgp2 to Mind subscription Opus asks immutable release packet; unanswered at this snapshot.

Orders daxc and 1p59 remain unclosed: rename harness long-id type to SessionId, fields session_id, and capability Identifiable.identify yielding FlowId; no universal Identifier. Actual library3613d63 has Session but **no Identifiable declaration/body**. Existing daemon identity comes through configured ClaimIdentity emission. Psyche question gcyd asks exact hash/identity behavior rather than inventing an algorithm from the notion's hash().first_characters(6) example. Wait for ruling/custody, then replace the whole affected library+signal/emission/notification consumer cohort coherently; no compatibility alias.

Pending inherited contract sources can be read with git show:
- signal-codex-harness-nexus 6447146: ReportedUnread, FoldRefused, UnknownFlow, Unreadable.RolloutFailure, MemoryFault, publisher failure, etc.; not adopted/gated in this continuation;
- meta-signal-codex-harness-nexus 4a12f25: WIP ConfigurationReadout includes UnwatchableDirectories; changes include it too. Not adopted. Old Poisoned/HeldLock variants reflect superseded lock design and do not justify retaining own locks.

## Next steps and reporting

Finish/commit actor source checkpoints and F2 coverage, obtain rulings li9u/byb4/gcyd and rename cohort custody, adopt immutable accepted shared revisions, complete typed F8/F9 mends/tests, and prepare exact dependency/version/resource packet. Ask Core for a fresh slot, regenerate dependencies and gate complete checks on builder against committed revisions. Then send gate packet to Psyche for independent second audit. 3kyf Done only with committed/gated candidate and required audit chain complete. No gate/audit/deployment success has been claimed here.

## Update after the clean checkpoints and received rulings

Current clean source checkpoint before actor body resumption is `b3ddfad` (core), which follows `dda787e` PublicOpening/watch capability preparation and `d260ce4` store preparation. Source review corrected d260ce4: removed empty StoreOpener/StoreFamilies behavior namespaces, generated static StoreOpening on native Store and static Familial.descriptor on each data-bearing record, fixed a wrong Self return and temporary path borrow. Generator byte-match/rustfmt/diff checks only. No CoreActor body exists at b3ddfad; production locks/OnceLock remain explicitly unfinished.

Translator preparation is `721ba07`, followed by `3b39057`: removes an orphan foreign-trait implementation and adds required local accessor bodies. `settings_actor` is a separate public preparatory module, not wired into production. It owns Runtime/ActorRef/task, uses native Kameo blocking_send and stops/joins at synchronous OS-thread Drop. Production RwLock remains until approved contract integration; no arbitrary async-context safety or runtime test claim.

New Psyche results supersede earlier questions:
- gcyd: only Session→SessionId this release; ClaimIdentity stays sole identity production; Identifiable/identify waits for supplied Identifier implementation. No hash. Result to original1p59 sent as2ac0; daxc remains open pending actual rename.
- byb4/a6ju: core `ReportFailure.ActorUnavailable.Diagnostic` and meta `ConfigurationRefusal.ActorUnavailable.Diagnostic`; meta `TranslatorUnavailable.Diagnostic` for settings actor. Remove Poisoned if no producer. The later a6ju payload spelling controls; no false Memory/InvalidBudget mapping.
- li9u first suggested direct core listener edge, but **m9oy supersedes it** and approves generic PublicOpening with daemon native wrapper/Arc, core actor owning wrapper+Opened, no core nexus-serving dependency.

Core8qmr verified accepted build-base `7fca4d583adfd2354903c59cbc7f5e928e1baa76`, Kameo0.22.2 crates.io, no git rev; existing central closure/default/macros/tracing and macros0.21.1. Closure strings are not Cargo manifest flags. No heavy grant. Core coordinates registrations.

Core r6w6 says074047 owns library and Harness Signal consumers too, but Lock420 does not cover them. Request7tg1 (exact-ref followup2td5) proposes source-only separate custody before creation/edits:
- `/git/worktrees/harness-nexus-library-074047` from `8e9878495790b49a8e1707e0018d11ad60caf0ad`;
- `/git/worktrees/signal-codex-harness-nexus-074047` from `64471468c4b8a3a042aff3b9e2c26d7ecba1e30f`;
- `/git/worktrees/meta-signal-codex-harness-nexus-074047` from `4a12f25b672f089151524ba86e8e33df524ba8d1`.
Proposed versions library0.2.0, signal0.5.0, meta0.5.0; source schema/generated/bodies/member version writes, later dependency regeneration only with explicit slot. No canonical repo writes. Core lock reply remains required. `actor_tests` prepares this cohort read-only, awaiting clearance. Its later work will integrate translator adapter/tests after exact contracts exist.

`actor_bodies` has been resumed with approved rulings to implement the whole core/daemon Kameo ownership replacement, not duplicate shadow state. It owns core+daemon/root manifest and flake generation list (must add translator_settings). Target approved new variants even while dependency/pin regeneration remains separate. Kameo0.22.2 local cache confirms `ask(...).blocking_send()` and tell equivalent. Pinned public Answering is spawn_blocking, meta serving is sync OS thread; construct/enter existing multithread runtime before daemon bind/spawn. In-process callers/tests need explicit blocking/runtime contract.

Field credential source review (requests1ed8/g3ar/jlxl) was separately answered, source-only, no credentials or runtime: local exact upstream tag870b79fe + existing derivations confirm selected r0k59hi2q6di7xhmqxp11vygy4hclzyy0.161alpha2 release asset provenance, File backend load/save follows symlink via ordinary open/truncate/write/create, refresh persists through same backend. No source-tree-to-binary reproducibility, cross-process locking, or atomic-save claim. Replies bfav/bhf5/5rhy sent. No credential contents/links touched, no execution/build/evaluation.

### Actual rename custody received

Core7tg1/gyvh/nzr1 confirms **actual Lock432**, owner074047, on the three exact proposed library/signal/meta worktree paths above. Source-only creation/edits are now allowed from the confirmed full refs, preserving canonical refs and WIP anchors; no dependency regeneration/publication/registry/heavy grant. Actor_tests has been cleared to create branches/worktrees after clean/ref/ancestry preflight. Signal/meta anchors are expected descendants of the older canonical HEADs, not their ancestors; verify canonical→anchor ancestry and do not move canonical HEAD. Proposed0.2/0.5/0.5 versions remain a source proposal requiring coherent metadata allocation. Actor_bodies owns core+daemon SessionId consumers, actor_tests owns translator and the three isolated contract/library repos; no overlap. Fieldh8xn exact Herdr0.8.2 launch containment question was returned as unknown (ggl0), no source/runtime containment claim made.

Active Flow consumer-impact inventory was corrected from legacy flow-nexus to active `/git/github.com/LiGoldragon/flow` HEAD53782fba5e1f5b761b87f09809c0b319bcc27ad: root manifest + tracked crates/flow-nexus, crates/flow and crates/flow-meta have no harness-library dependency or Session/ItemStarted/ItemCompleted/TurnFailed references. This is bounded canonical-checkout evidence, not all unmerged worktrees. Correction8bj0 sent to Core. Actual checked Harness sources also have no tentative notification types, so none is invented.
