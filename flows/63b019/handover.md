# Handover — Mind versionOne Primary 63b019

Working state for the next flow; not vision. Updated 2026-11-03.

## Roles and order
- I am Mind versionOne Primary: judge design. Mind versionOne Secondary `af8fe8` builds.
- Psyche codexManager Secondary receives completed parts, blockers, and departures from vision; not routine progress.
- Living order (raw source: `/home/li/primary/flows/a53796/vision-raw/living-words-04df39.md`, 2026-11-03 18:12): fresh v1; everything configurable and atomically reconfigurable; no v0 reuse; same login, independent environment; `herdr → Belief → Flow → meta-v1`; per-part Opus audit.

## Repositories and completed Herdr slice
Repos: `/git/github.com/LiGoldragon/{translator,herdr-nexus,signal-herdr-nexus,meta-signal-herdr-nexus}`; later `belief-nexus/meta-v1`; flow-nexus version 1 from scratch. Emission has a separately marked Signal root; ethos-zero unchanged.

Herdr implementation is at code `8046d952` (proof/clean final `054b12b0`): actual remote Nix checks/packages passed. Owned CLI and live subscription behavior are proved (Configure/Create/StartCodex/Prompt/nonce-pane read/ListLabelIdle/Close/emptyList; Subscribe ack→Busy→Idle); cleanup complete; `PROOF.md` carries evidence. However, independent final review found missing `Changed.Dead` on disappearance and possible per-subscriber duplicate polling. Repair/tests are dispatched: missing IDs after a complete snapshot yield one Dead, repeated absence yields no duplicate, failed snapshot yields no Dead, and one shared poll hub is verified. Component completion/audit closure is pending this bounded repair; manager informed. Live Start/Prompt/BusyIdle evidence remains valid. Memory is explicitly process-lifetime.

Shared Outcome supports success payloads, refusal, Unknown, Uncertain, StoreRefused with phase/effect evidence. Command carries AgentName, AgentKind, Executable (Configured|ExplicitProgram), argv; generic shell launch is excluded. Translator default binary is fixed-endian, rkyv-validated; optional datom text and generated Place registry. Immutable direct datom pins: `e26d90f`, `0cad1d1`.

Meta runtime configuration only; immutable Place at startup. Launcher reads explicit typed registry/name and sends bounded binary Place on stdin. Daemon closes bootstrap fd, binds meta then public only after successful initial Configure. Public bind failure is typed Unavailable; unknown socket is never unlinked. Herdr uses one external codec and bounded process-group runner (deadlines/output cap/child reap), strict source-tagged schemas, complete owned-snapshot reconciliation, direct bounded subscription delivery/no queue.

Repo history: published target artifacts in `2617a3c`, removed latest tree `aad6572`; no force rewrite authorized. Earlier `nix develop cargo test` evidence was local and is corrected; current remote ssh-ng/max-jobs=0 derivations are witnessed.

## Belief acceptance work
Belief is now authorized to implement first files: mock Register/Resolve/Furnish. New PoC YAML placement is `SystemPrompt` or singular `Skill`; missing/malformed placement refuses; no kind inference. Translator parses files and writes; core remains typed only. Full generation bundle plus skills stages in owned workspace, then atomically swaps current pointer. Deployment-configured stable discovery links `.agents/skills` (Codex) and `.claude/skills` (Claude), only when absent/already-owned, never overwriting unrelated paths. Codex `model_instructions_file` config is verified in docs; actual marker and skill-discovery proof is still owed. Claude system-prompt-file docs are untested. Live repo watch/refurnish/permanent refresh is explicitly deferred/mock for first acceptance; manager informed.

Module resolution uses canonical roots, safe relative paths, no traversal; duplicate/ambiguous sources refuse; missing modules follow explicit Flow policy. Bundle bodies follow request order and preserve appropriate skill frontmatter. One datom/file definition persists via translator atomic rename.

## Flow/meta pending
Flow judgment is ahead of build and has been sent to the Secondary: validate whole Complex (unique members, valid speaker/internal routes/tool policy), atomically replace by name, capture a snapshot per operation. Running processes retain launch config; future launches/routes use latest. Demonstrate replacing one complex while a second is unchanged; invalid candidate preserves old; changed configured launch value is observed without Nexus restart.

Flow/Belief/meta shell is not yet built. Next: receive Herdr audit; supervise Belief implementation and proof; then Flow and meta-v1 final acceptance: Mind Secondary starts harness through Flow→Herdr, Prompt arrives, and one complex is redefined without restart.

## Latest Herdr status and superseding rulings

Herdr `5a883469` / code `8a116f41` fixed one shared poll per session and one Dead on disappearance. Remote tests, real two-subscriber external-close proof, and independent source review pass. It is nevertheless release-blocked by the full Opus audit at `/home/li/primary/flows/a53796/audits/herdr-nexus-v1.md`.

Repair priority is: **1** ownership before emission; **3** translator in front (`CLI datom → translator socket → Call.{Caller Input} signal → Nexus → translator → CLI`); **2** failed meta request must not kill the listener; **6** one bounded uncertain record per pane, not per poll. Then address audit items 13/14/15/9/16/17; reader is pending. No global lock may span external I/O. Belief may proceed beside repairs, but shared helper extraction waits until the front-translator architecture settles.

Latest Psyche rulings supersede earlier Primary choices: translator owns `HerdrPath`; Nexus has no executable path and emission carries no full Configuration. Known is Label plus one State Library. A hand-written Memory trait returns Answer; nondurable remains approved. Emission has no duplicateSession, PaneClose, or PaneList; Start Timeout comes from config; codecs use per-type `Arguable` traits rather than monolithic invocation. Meta Configure is one field via a Set enum, not whole config; running subscriptions follow configuration updates.

Belief’s latest manager order cancels placement frontmatter: Kind comes from folder; Spirit/Intent are bundled; other kinds are skills, with no duplicate metadata. Belief public scaffold `003d5385` has four crates only. Primary dispatched all repairs and an `opus_audit_read` subflow is reading the full audit. Preserve earlier history above, but these status and rulings govern current work.

## Current Herdr front-repair state

Front repair checkpoints `543889` then `751efc` pass 24 remote-prometheus tests. Integrated: generated `Call` kernel caller, flat per-field `Set`/`CoreSet`, partial owner initialization/readiness, configuration-free emission, text-only frontend CLI and forwarding. Work remains: short-lock reservations, bounded uncertainty, shared reconciliation, `streamingSubscribe`, and Operation-drift enforcement (worker exclusive). Bad-meta-then-valid-Set regression passes; invalid `HerdrPath` preserves the prior value. Reviewer flagged bootstrap deadlines/coreSet not gated on translator readiness and accepted-peer UID checks; repairs are dispatched.

Approved Outcome is only `Unavailable.TransportRefusal{SocketPath, Message}` when submission is definitely absent; loss after submission is `Uncertain`.

Manager privilege ruling: separate META FRONT. Current topology has four named typed lanes: `herdr.sock` core-binary public; `herdr-meta.sock` core-binary meta; `herdr-translator.sock` `PublicText+EmissionSignal`; `herdr-meta-translator.sock` `MetaText` only. Wrong lanes reject. Frames are 4-byte big-endian length, then lane/kind bytes; original datom text is UTF-8, binary is validated by explicit lane. Public CLI has no domain schema or datom decode; installed wrapper embeds registry path, so user syntax is NAME DATOM. Translator kernel caller is uid/gid/pid; core trusts same-login UID, not an adversary boundary.

Flat public Configure.Set routes translator-owned `HerdrPath`, `CallTimeout`, `OutputLimit`, `TextBudget`; core owns `StartTimeout`, `Polling`, `FrameCapacity`, `TransportTimeout`. Start.Timeout is in emission; translator has no duplicate StartTimeout. Configure acknowledges owner plus `Readiness` (`Awaiting` with missing fields or `Ready`), with no policy defaults. Initialization is partial: public bind occurs only at coreReady, translator public readiness only at ownReady, while metadata remains bootstrap-bounded. `CoreTransportTimeout > StartTimeout`.

Belief remains scaffolding only pending critical Opus repairs; metadata follows folder Kind, not frontmatter. Primary latest sends: `7551` / `7556`.

## Resumed work — current second audit and repair order

CodexManager authorized resumption after the weekly reset. Baseline `3ded62c8` and the whole second Opus audit (`/home/li/primary/flows/a53796/audits/herdr-nexus-v1-second.md`) are read. Priority repairs are N1 quiet-subscribe timeout, N2 same-UID bypass/forged caller, and N3/N5 NexusClose notification, then remaining findings. Secondary is the exclusive worker; no new immutable repaired result exists yet. Belief remains held at scaffold until Herdr closes.

Current decisions (Primary sends `7785`–`7813`): launcher spawns both children blocked on bootstrap, gets actual PIDs, supplies `PeerIdentity{UID, PID}` to both; core public/meta accepts exact translator, translator emission accepts exact Nexus, text login is accepted then caller is kernel-derived. Pair lifetime is immutable; launcher tears down the survivor when either exits and starts a new pair on restart. N1 is request+ACK bounded, then infinite idle until first byte; after first byte frame progress and downstream writes are bounded; EOF ends.

Changed remains Pane+State and Attempt appears in List. Create uncertainty does not invent a Pane record; remove unused `sessionPollFailure` storage. Close publishes one Dead to current subscribers before ownership removal; unsuccessful Close publishes none; a late subscriber receives no historical removed Dead. Translator deployment admission bounds its decoding; NexusFrameCapacity remains a separate owner.

PaneList and AgentList split into two emissions joined by Listing (one emission per external call). Distinct observationalEmissionResult remains pending Psyche clarification; public shared Outcome carries KnownLabel unavailable to translator. Arguable is per type in Ethos. Exact empty stdout is a permitted pinned-contract success; nonempty is invalid; refusal IDs are checked. All generated files get aggregate drift checking.

N4 supersedes serialized writes: short hub lock, one writer plus bounded FIFO per subscriber, configurable `newcoreSubscriberCapacity`; overflow disconnects only the slow peer. Capacities apply to existing subscribers, with a current deadline per frame and no unbounded channels/tasks. NAME DATOM wrappers bind one registry path from deployment data (no home/env fallback; internal engine registry argument is allowed); prove two names through wrappers. Remove obsolete root `PROOF.md` in favor of `proof/PROOF.md` and rerun the harness. Keep generated Operation alignment for Listing/Subscribing/Start.Label; manager has been asked to align modules.

This resumption supersedes the stopping-state pause for current work; historical pause records remain unchanged.

## Latest Herdr implementation and remaining gate

Psyche core approved a raw observational Emission result separate from shared Operation/PublicOutcome; `earnedEthos` remains pending manager landing. Herdr implementation is `a9ea94e`; bead-only clean HEAD `6671a63`. Remote full check and all nine contract-drift checks pass. Installed package `/nix/store/wcy4bxjac730jq6ncckp4z5a7bwsqaly-herdr-nexus-v1` and `proof/live-herdr.sh` report `LIVE_HERDR_PROOF_OK`, all resources cleaned, lock `25050` released.

Repairs now present include: Known.Attempt without orphan stores; Configure echo; positive subscriber capacity; idle-first-byte with bounded frame progress; exact UID+PID paired gates; FIFO writer isolation and capacity shrink; Close one Dead before ownership removal; missing-pane Memory AnswerFailed; separate PaneList/AgentList one call each with conservative join; exact Keys/refusal IDs; quiet disconnect write cleanup and stale-poll Close-publication guard; paired launcher blocked bootstrap/survivor teardown; explicit BootstrapMeta/Ready types. Direct N2 impostor-zero-effect and core forged-peer rejection tests pass.

Remaining explicit gap: terminate → survivor exit → fresh-pair relaunch regression. Primary ordered fixture work; no model change needed. Secondary must perform final independent audit delta, followed by manager Opus gate; audit is not closed. Checked observational Outcome, Starting.Label, Listing/Subscribing, list emissions, and SubscriberCapacity are to be sent to manager with exact code. Belief remains scaffold. Primary sends `7910` / `7917`.

## Third audit and Flow authorization

Third audit (`/home/li/primary/flows/a53796/audits/herdr-nexus-v1-third.md`) judges Herdr fit for Flow once D1 is fixed and D3 ruled. D1 delayed-start E2E passes at `aec3f05` (`DELAYED_START_OK`): external 200ms, Call 50, Transport 50, Start 1000 completes; Start 40 yields Uncertain. Client quiet results wait indefinitely until first byte; connect/send/frame progress are bounded and the operation owns execution timeout. Translator CallTimeout is external non-Start only; Start has typed timeout; core TransportTimeout covers I/O progress only, with the `> StartTimeout` constraint removed. D3 is SIGNAL between Nexuses using typed configured peers.

Stable design: PeerId.String is separate from UID/PID; Set.Peer upserts/rebinds one peer; RemovePeer revokes it, not panes. `pidfd_open`/poll prevents PID reuse. Principal derives from login UID for own translator-forwarded kernel callers or PeerID for configured peers; no delegation or forged caller. Identity propagates through ownership/List/subscriptions; revocation closes old subscriptions after finite in-flight snapshot completion. Registry is at Nexus signal transport, not text translator; core meta applies it; translator gates only its own Nexus emission. Shared generated `identity.ethos` is approved; translator `2f1fd07b` and meta `8cfcf635` checked/pushed; runtime integration continues.

D4 approved pending creation: pre-emit `CreationId{InstanceId, Sequence}`, Principal, Workspace in memory; launcher uses fresh InstanceId and workspace-create emission marker. Later WorkspaceList plus PaneList finds an exact unique marker; one complete pane adopts and consumes it. Uncertainty keeps the active pending record; absence/ambiguity is not proof; no invented pane or orphan history. D5 uses `Known.Option<Label>` for unstarted-pane consistency. D6 pane-not-found closes locally (`1169c09` tests pass). D7 classifies accept failures as retry/recoverable/resource-pressure using deployment retry delay, with permanent fatal visible.

Remaining requirements: partly Argueable in Ethos; no free parallel Invocation/Decoder; one Subscribe/total matches/no unreachable; shared socket/budget/max; truthful design. Core Psyche approved one attempt may compose multiple emissions, each one external call; observational Emission result remains approved.

Belief is now a separate team: Primary `55712b`, Secondary `19c3e3`. Checked Furnish includes Workspace, HarnessCodex, and modules. Placement paths were restored in FurnishedWorkspace/state/updates; final pins pending. Flow must consume Placement, never reconstruct layout.

Flow reconnaissance: clean `flow-nexus` main `b5c9722` (no beads), safe orphan worktree sibling at `/git/github.com/LiGoldragon/flow-nexus-version-1`. Installed Codex 0.166 flags model, effort, `-C`, and `model_instructions_file`; generic tool filters are unverified. Primary `8407` authorizes F1 design plus checked Ethos proposal first: fresh orphan branch; Complex vocabulary Define/Undefine/Describe; validation, atomic per-name snapshots, persistence via translator one file; no launch yet and no copied server framework. Required tests: two definitions, valid one update, invalid/write failure preserves old, stable in-flight. Await schema judgment before implementation. Tools semantics question `8408` asks Psyche to choose HarnessDefault vs Restricted typed allow/deny; no ruling yet. No live v0 touch. Herdr worker continues D3–D7/partial work; final closure is not claimed.
