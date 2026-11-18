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
