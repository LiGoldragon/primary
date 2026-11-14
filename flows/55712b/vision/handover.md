# Mind beliefNexus Primary — migration handover

Predecessor flow: 55712b. Successor: Custom.[55712b]. Read this whole before acting.

## Current instruction and state

All Belief implementation, tests, audits and bridge removal are STOPPED for migration. Latest core instruction permits preparation/checkpoint only. Do not resume until explicitly authorized. No self-retirement or successor launch. Mind core Secondary coordinates the move with Psyche core Secondary; it requires the whole first prompt, first answer and native proof before predecessor retirement. No runtime Memory migration.

I am the design Primary. Mind beliefNexus Secondary owns implementation and delegates it. Main flows read no files/command outputs themselves; brief subflows for evidence. Write only own records/proposals and send own messages. Supplied skills remain the governing context; do not reload them unnecessarily.

## Proven result

Belief v1 is public at github.com/LiGoldragon/belief-nexus, with sibling signal/meta repositories. Authoritative checkout: /git/github.com/LiGoldragon/belief-nexus.

Final executable revision: 39b422e28fd7ae09413cd62e789afa2128a3cc46.
Ordinary: ccfa452bf1b807c9f180a4cae70318e66afb9a11.
Meta: 257d34641381a3743d58df2c9437db672a92af91.
Shared translator: 751c326f11c874b527a69ce6377ce9e196aeca37.
Installed package: /nix/store/3v2wkqf3wj3miw1kq66v72fv5136wlwb-belief-nexus-v1.
Build: `nix build github:LiGoldragon/belief-nexus/39b422e28fd7ae09413cd62e789afa2128a3cc46#default --print-out-paths --no-link`.

Independent subflow replay from clean detached /tmp/belief-final-39 verified HEAD and clean status, bash syntax, then proof/run.sh exit 0. Both real Codex and Claude returned `BUNDLE_DEFAULT_TOKEN BUNDLE_OVERRIDE_TOKEN SKILL_DEFAULT_TOKEN`. It observed public named CLI registration/configuration, both Furnish paths, configured Kind defaults and front-matter placement override. This is independent execution of supplied proof, not an independently authored oracle. Separate implementation tests prove configured binary Peer Register→Furnish and unconfigured refusal. No general multi-owner isolation proof.

VersionOne Primary subsequently reported the first actual Flow→Belief→Herdr→Codex nonce receipt PASSED against this Belief revision: Launched.1, assistant nonce absent whole from input, owned pane cleaned. That is versionOne's evidence. It used fresh proof State and a TEMPORARY same-Peer Flow Register bridge. Preserve that bridge during migration.

## Latest access ruling and stopped next work

Core ruling supersedes earlier proposed owner-isolated sources: login owner registers repositories through Belief CLI; ANY configured peer may Furnish registered repositories. Flow Register is not intended final design. The temporary bridge is allowed for first launch and must later be removed in a coordinated versionOne change once Login Register→configured Peer Furnish is proven.

I authorized a focused probe after first launch, then migration STOP superseded it. Secondary safely halted BEFORE execution. No owner-path run completed; no blocker/no-blocker conclusion exists. No source/bead edits or locks acquired. Owned Nix processes 2232967/2233069 were stopped; no worker temporary pair remains; unrelated processes untouched. Repository was reported clean. Resume requires explicit authorization.

When resumed, first test a fully Ready fixture on existing revision before changing code: login CLI Register, separate configured Flow Peer binary Furnish, actual paths/content, unconfigured refusal. Change only demonstrated blockers. Preserve same-login different-PID ownership. Resolve/subscription policy is unresolved and outside this focused change. Preserve Peer Register compatibility until coordinated bridge deletion. Send a self-contained immutable package/recipe to versionOne, then replay launch without bridge.

## Current public boundaries

Public CLI: `belief-nexus <metaflow> '<datom>'`, meta `belief-nexus-meta <metaflow> '<datom>'`.
Packaged pair: `belief-pair '<Place>'`, exactly one inline datom. Example shape: `{ main «absolute-runtime» «absolute-state» }`.
Shared Place is `{ MetaflowName Runtime State }`. CLI resolves runtime under `$XDG_RUNTIME_DIR/metaflow/<name>/`, state default HOME/.local/state/metaflow/<name>. Explicit test State may be isolated. Earlier package-fixed registry proposal was superseded; do not resurrect it.
Pair uses Nix-generated typed deployment and internally rich paired bootstraps; that internal seed was expressly approved. It seeds transport, layouts, placement defaults and readiness. Public startup does not expose the rich bootstrap.
Sockets in Runtime: belief.sock, belief-meta.sock, belief-translator.sock, belief-meta-translator.sock. Memory: State/belief.memory.
Wait for named ordinary `Resolve.[]` to return Resolved, not just socket existence.
Meta Configure optional revision: None is authorized unconditional one-field mutation; Some retains compare-and-set. Do not guess the private bootstrap's revision count.

Shared Caller is kernel-derived PID then UID. Owner.Login.UserId is authority of text callers through authenticated paired translator; same-login different CLI PIDs retain ownership/meta permission. Owner.Peer is configured signal peer ownership. Keeper.[Nexus Translator] names configuration responsibility, not authority. Meta requires paired translator transport then authorized login UID; ordinary peers gain no meta permission. Same-UID hostile-process isolation is not claimed.

Every ordinary signal caller sends ONE declared Call.{Caller Input}; no bare Query or decoder fallback. External configured translator's claimed Caller must match kernel peer identity; paired translator may forward original CLI Caller via its authenticated trust path.
OrdinaryPeers is one atomically replaced typed list, not per-peer mutation. Actual meta shape: `Configure.{ None OrdinaryPeers.[ { flow { FLOW_UID FLOW_PID } } ] }`. Peer binding order UID then PID differs Caller PID then UID. Bind the process actually opening Belief socket.
Binary wire: four-byte big-endian length plus rkyv. Same configured process currently Register→Furnish for temporary bridge. Register Rust shape Query::Register(Repository(RepositoryPath(path))). Furnish uses FurnishRequest{workspace:Workspace(WorkspacePath(path)),harness:Harness::Codex,module_name_vector:[ModuleName{kind:Kind::Spirit,subject:Subject("core")}]}. Fixture is committed refs/heads/main with spirit/core.md. Consume returned furnished_paths.system_prompt_path and skills_path; missing module_name_vector must be checked.

## Design rulings to preserve

- Harness.[Claude Codex]; Furnish includes Workspace, Harness, names. Per-harness typed layout. Claude uses owned CLAUDE.md and .claude/skills stable links; Codex model_instructions_file absolute bundle path and .agents/skills. Real installed harness discovery was verified with existing auth, no credential copies.
- Placement.[SystemPrompt Skills] is routing. Front matter `placement: system-prompt` or `placement: skills`; absent override uses Kind meta setting Set.Placement.{Kind Placement}. Initial deployment data Spirit/Intent→SystemPrompt, Vision/Knowledge/Role→Skills, never Rust policy. Output path pair renamed FurnishedPaths to avoid collision.
- Atomic publication is immutable complete generation plus single current-pointer replacement. It is not a transactional multi-file reader snapshot. Validate ownership of current, settings key and links; preserve unrelated settings/refuse conflicts. Missing modules are explicit successful partial furnishing, not Belief launch policy.
- Committed main snapshot, not working tree; observed source revision distinct from successful workspace revision. Failures and retry notifications typed. Pending attempt must persist before pointer publication; recovery compares observed owned generation against exact pending identity/source/config/request. Inspection may be observation-only, checked by Nexus; avoid redundant wire provenance demands.
- Nexus owns durable configuration and revision. One translator process shares immutable snapshots and admission/update gate. Authenticated binary restore before ready; Configured only after apply. Emissions carry attempt revision/translator snapshot, preventing latest-config drift. Do not hold admission gate over a call waiting for emission.
- Subscribe initial state and registration share serialized transition, then framed typed events. Slow subscriber bounded closure, no idle timeout on quiet stream. Terminal overflow/write-timeout semantics do not claim delivery after failure.
- Retention KeepAll or KeepPrevious.PositiveInteger; default KeepAll. Protect current/pending. Nexus selects exact owned generation from history; per-generation Clean rechecks manifest/current. Cleanup failure distinct from publication success. No pinning guarantee in bounded mode. These features already exist; audit called scope overbuilt, so no expansion.

## Audit and held beads

Opus audit: /home/li/primary/flows/b862a0/audits/belief-nexus-v1-review.md. Earlier scope audit: /home/li/primary/flows/a53796/audits/v1-vision-review-1.md. Do not reread broadly without a task; delegate relevant evidence.

Five approved OPEN/unclaimed beads, discovered from original yaf, designs pending:
- belief-nexus-nmz: now titled Configured peers furnish shared registered belief repositories; latest access matrix above.
- belief-nexus-ukr: old-belief notification to Flow, contract with versionOne.
- belief-nexus-0g7: Changed/affected-workspace/retry coherence.
- belief-nexus-9rk: Library/Memory/Operation Ethos correspondence.
- belief-nexus-fnu: bounded assessment of remaining deployment/meta/poll/retention/type findings, not omnibus rewrite.
Bead-only commits 0888bb118909bd1693b6c85ca757cf8b56aabb65 and nmz ruling update e70d9ec6000488d4452423bbcd8b4b74a5193738 pushed clean; executable pin remains 39b422e. Locks 25108 and 25121 were released.

Evidence grades: static final39b422e Register at daemon/src/lib.rs1268-1276 and Resolve1040-1048 reject any repository-owner mismatch. Furnish dispatch1055→core/src/lib.rs562-590 resolves all snapshots. Executed isolated negative proved Login Register then Peer Register/Resolve NotAuthorized; Peer Furnish returned NotReady, so dynamic furnishing conclusion INCONCLUSIVE. Under newer core ruling shared source furnishing is authorized, not itself a leak. Static subscriptions admit owner then return global state and drain global events without owner filtering; subscription policy remains unresolved. No executed subscription leakage test.
Old-belief notification missing, unnecessary refurnishing on any main commit, publication event coherence, and incomplete Ethos remain audit findings; no postlaunch repairs started.
FurnishedPaths may legitimately expose stable published skills directory rather than harness discovery link; assess actual contract before declaring defect. HOME/.local/state default follows latest ruling, so absent XDG_STATE_HOME support is not automatically a deviation.

## Coordination and evidence hygiene

Main contacts: Mind beliefNexus Secondary; Mind versionOne Primary/Secondary (integration); Psyche codexManager Secondary (commissioner, Opus audit); Mind core Secondary (migration).
Initial implementation handoffs repeatedly arrived batched/late. Final full runnable handoff 9496/9500 and direct Primary relay9504/9505 resolved it; versionOne acknowledged installed39b422e and smoke passed. Send actual package/commands together, not merely “already sent”.
Our tester once claimed immutable evidence after mistakenly running shared mutable checkout; parse-error claim was RETRACTED. Verified clean9a6ead replay then found old fixture passing socket path to new named CLI (UnsafeName); final39b422e corrected and passed. Future immutable proof must report cwd, HEAD and clean status before execution. Prior2ff080d proof does not establish later boundaries.

## Migration readiness

This handover is a working record, not a new vision ruling, though the requested destination is vision/handover.md. All unfinished work above is held. Await migration coordinator instruction and successor whole-prompt/first-answer/native proof; predecessor does not retire itself.
