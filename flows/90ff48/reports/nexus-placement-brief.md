# Held nexus placement decision brief

Artifact /git/github.com/LiGoldragon/nexus c495f2acbfff57e017092b9cc1fbf9f73ca2badf→da2e10fe694d5f2094da8ed92e7508cd4fee89e8, feature/frame-limit-70a111. Field read-only packet, no fresh builds.

ARCHITECTURE:3-5: This crate owns universal Nexus types and trait-borne behavior. Domain nouns remain in each component authored Signal and Sema contracts. Transport, listener, actor, and runner mechanics remain in runtime libraries. Lines36-39 require second implementation and identical behavior for every instance. Blame placement e67735e; second rule1fedfb6d. Repository design text; explicit living approval unestablished, not reviewed psyche.

Candidate six files Cargo.toml/lock, lib.rs, entry.rs, entry_process.rs, lifecycle.rs. Entry constructs actor handles, binds Unix socket, serves serially, runs tasks/watch cancellation/joins for signals/completion/failure. Traits RunningTask, Signaling, Remembering, Operating<M>, Nexus, Entering. Types LifecycleState/Failure, Cancellation, NoTask, SupervisedTask, Changed, Admission, MemoryActor/Handle, OperationActor/Handle, SignalActor, FrameLength/Limit/Error, Door, MainActor. New Kameo/rustix process/Tokio runtime-net-io-signal dependencies. Present scoped consumers fixture entry_process (Remembering/Operating/Signaling/Nexus/enter) and lifecycle (task/cancellation/state/failure); rest compose entry. External consumers unverified.

Recommendation sent Core for explicit judgment: move cohesive new entry surface/bodies/tests/deps to runtime library→nexus ontology, no reverse dependency. Keep sole-implementation declarations with mechanics until second implementation justifies promotion. Destination library unestablished, must select before implementation. Local migration same six-file source boundary plus destination manifest/exports/fixture imports, no intended rewrite; external migration cost unknown. No relocation authority.

Known limitations unbounded cooperative joins, slow serial client blocks accepts, SIGTERM process ordinary exit/socket removal only, replacement guard historical unit-only, ignored process fixture invoked by owning test. Historical42/0/1+fmt/clippy not rerun. Enter documentation correction unresolved. Historical branch70a111 not running-owner proof.0.6.0 unallocated; no landing/tag/release.

## Core decision and next step

Core explicitly adopts ontology/runtime separation on supplied evidence (not psyche provenance claim). Cohesive new entry/runtime-specific surface/deps/tests remains runtime→nexus until real independent implementations establish abstraction. Read-only next step delegated Field core: existing runtime libraries + actual external consumer inventory, supported owner, single destination recommendation with repo/package and minimal public boundary/migration list for Core approval before edits. Immutableda2e10f reference; later migration correct enter docs and rerun relocated tests. Former0.6.0 suspended; no edits/landing/tag/release.

## External inventory update

Field finds Chronos and inbound-frame-limit checkout pinned ec097e3 consuming earlier entry traits/open/Door/enter. Not fixture-only migration. No candidate-only lifecycle/FrameLimit external hits in bounded symbol search, not exhaustive absence proof. triad-runtime owns listener/framing/process/worker mechanics and uses Tokio/Kameo/rustix, not this entry contract; cycle/legacy status and exact Chronos files pending before destination recommendation. Implementation owner unverified. Relayed Core.

## Destination recommendation delivered Core

triad-runtime4cc0a100841d2400f354c008c9faa73b2cedf50e owns async daemon runner/process/listener/frame/exit (ARCHITECTURE5-7,19-21,169-190,307-315), no legacy designation or evidenced dependency cycle. Recommend whole cohesive entry module/tests/deps there→nexus, no reverse reexport/old-daemon adaptation. BUT own second-component admission gate unresolved: Chronos only witnessed product, duplicate checkout not second implementation; destination approval alone insufficient. Core must judge admission before edits. Supported owner still unknown.

Chronos679fa1865a3d85a28524d406d387627cf3b58896 Cargo.toml36 pins ec097e3; daemon.rs5 Admission/Changed/MemoryHandle/Nexus/Operating/Remembering/Signaling imports+impl174-220,237-254,257+; bin/chronos_daemon.rs4 Entering/29 enter(); tests/entry.rs5 open/Door::serve tests. Move owners/dependency/lock, retain ontology only if used. Candidate explicit FrameLimit requires approved configuration, not invented. inbound-frame-limit-54420d no-git copy same product; coordinate. External inventory bounded, unknowns remain.

Concrete doc correction recovered entry.rs651-657 until Ctrl-C omits SIGTERM handled686-699; correct during authorized migration, preserve other limits. Cost local six-file relocation+Chronos listed changes+configuration decision; no estimates.0.6.0 suspended, no edits/release. Full brief sent Core.

## Core narrows next step to product-local ownership

triad-runtime eventual shared owner; admission unmet (one Chronos+copy one implementation). Next read-only proposal product-private Chronos entry using existing library boundary; show binary/integration access, minimal public exposure, current-runtime collisions. Existing runtime facilities only if same behavior without new design. Need supported CURRENT Chronos owner and approved FrameLimit configuration source before migration brief. No manufactured second consumer/shared repo. Genuine second implementation evidence may change admission. Field assigned bounded investigation, no edits/publication, immutableda2e10f preserved.

## Product-local boundary interim

Chronos existing lib exports daemon, binary/tests use chronos::daemon::Chronos, local entry boundary feasible; minimal signatures pending Field. wire.rs MAX_FRAME_BYTES=1024*1024 only code constant, not approved typed FrameLimit config. No current owner binding; historical Psyche Chronos Secondary984e88 insufficient. Core asked current owner/address routing or supported assignment+approved config. Migration brief held; bounded boundary evidence continues, no edits.

## Supported custody inspection requested

Core lacks owner pointer; asks Psyche core for owner/config judgment (1048576 explicit typed default only a question, not approval). Field ordered read-only supported Flow inspection from historical Chronos address and orchestrate current repo lock snapshot; actual binding/absence, no pane inference/speculative launch/assignment. Minimal boundary brief continues, no edits.

## Minimal local API brief sent Core

Private Chronos library entry module; daemon crate::entry imports. Binary/tests use existing lib, direct names Entering/FrameLimit but reachable contract includes Nexus+Sized, MainActor/Door/OperationHandle, FrameError/FrameLength, enter_with/RunningTask. Preserve signatures, no wrappers/deletions to make export count small; exact accessible exports future authorized compile. open(PathBuf,FrameLimit)→Option<(MainActor<Self>,Door<Self>)>; enter/enter_with→ExitCode; Door knock and serve→Result<(),FrameError>.

Daemon5+impl174-275 imports become crate-local; binary4/29 and tests/entry5,13-20 change imports/FrameLimit argument. Move lifecycle/process fixtures preserving invocation, runtime deps/lock; retain ontology as used. wire framing path separate, no dedup/triad refactor. Owner/config gaps remain; no edits/compilation/publication.

## Migration authorized, chain briefed

Core/Psyche current owner Mind chronos Secondary54420d (must verify current binding before effects). Product-local boundary accepted; typed FrameCapacity.ByteLimit default1048576 configurable meta one value at a time per vision:herdr-nexus-v1, wire constant becomes default. Missing meta abstraction concrete design step goes Core before invention. Former Nexus0.6/shared proposal superseded; derive actual Chronos impact.

Full packet sent owner: implementation/custody+pre-edit plan→immutable independent diff review→owner fresh composed checks durable logs→Field core independent dependency/consumer/readback→main combined Core landing review. Beats each stage; no publication yet. First malformed nested-guillemet CLI dispatch failed before delivery, replaced by plain self-contained valid packet. Chronos owner independently received Core authority and asks packet; workspace chronos-inbound-frame-limit-54420d cleanbase679fa1865a3d85a28524d406d387627cf3b58896/no lock; configuration anatomy next read-only. Prior startup plan superseded. Field confirms wait immutable artifact, no duplicate implementation/checks; obsolete owner search stopped.

Supported flow-meta0.51 Inspect confirms Mind chronos Secondary Awake54420d/session01a1a90b-3a2f-73d2-8603-05a54420d9a4/location Available default/wMT:p1/term_65f7c53daca975e; binding Unbound+Active, live holder not adoption proof. Historical Psyche chronos/Chronos UnknownAddress. Forwarded owner to match actual environment, no process effects. Independent reviewer audit_test_diff rebriefed to await immutable artifact. Chain reported Core.

Later owner custody report: actual CODEX_SESSION_ID guarded Adopt returned Adopted54420d successfully; root+sole chronos_loop worker active read-only. Earlier Unbound observation superseded by later adoption event, not retroactively false. No edits/publication; config anatomy pending, concrete gap before implementation.

## Concrete missing abstraction escalated before edits

Owner54420d adopted, sole worker read-only, workspace empty417914f1 over679fa1 clean/no lock; nexusda2e10f unchanged, preexisting untracked ethos untouched. Chronos only ordinary Place socket, one signal/operation/listener, location-only redb Memory. No config/meta schema/socket/client/authority. Dependency ConfigurationState unused/restart snapshot. enter_with discards main, RunningTask only Cancellation, cannot access actor Memory/OperationHandle. Core asked design for per-value typed wire/refusals, path/client/authority, storage/default seed/immediate-vs-restart effect, additive actor-access capability. Also asked whether cohesive transplant may proceed separately or all edits held. Directed read-only until ruling; no invention. Field waits artifact.

## Separate interim transplant authorized

Core permits isolated behavior-preserving mechanical transplant after lock despite missing config abstraction: preserve whole contract/tests/explicit FrameLimit, startup approved1048576 default, stop docs, wire path separate. No Configure/socket/authority/persistence/channel invention; no publish/deploy-as-ruling-complete. Independent review/check/readback chain remains before Core landing review. Owner/Field/reviewer briefed.

Core owns missing coherent config/meta design. Owner asked exact existing authored-vs-generated Ethos/types/contact points only: Place/socket construction, signal→operation→Memory, Memory startup/upgrade, actor handle/lifetime, dependency peer/client identification. No schema invention. Mutable persistence/activation judged separately.

Pre-edit beat owner54420d lock25515 ChronosEntryTransplant reserves ONLY /git/github.com/LiGoldragon/chronos-inbound-frame-limit-54420d, clean empty417914f19712 over679fa186. Canonical clean detached Chronos excluded; foreign Nexus ethos untouched. Mechanical transplant now begins, no meta invention/publication/deploy. Contact-point extraction follows.

## Exact existing contact points returned Core

Authored .ethos/data/chronos.ethos Types1-18 Place4-7/Request8-10/Response11-16 only; generated datomic_library.rs Place3-43 Request44+ SetLocation170 Subscribe205 unused runtime. Handwritten src/place18-63 Place ordinary_socket runtime/chronos.sock,86-145 codec/install; daemon257-275 State/socket; client18-25 fixed main. daemon41-82 signal→operation,222-255 operation→MemoryHandle,84-220 redb location. Startup89-158 migration/open,174-182 State,184-220 data/revalidation; no schema upgrade kind/version. Local entry traits163-212,Memory215-262,Operation266-305,Signal308+,MainActor.operation451-458,lifecycle22-142,Door/frame326-448,socket461-575,Entering577+,stop586-636. No peer Caller on streams; euid/parent+inode guard only. Full packet sent Core, observation not design.

Mechanical implementation done, preliminary remote doctest crate-path issue repaired preserving private-field proof; owner freezing next. Requested immutable revision/base/log/diff/dependency impact; final fresh gate required, prelim not acceptance. Independent reviewers wait.

## Core exact-code design request dispatched separately

Owner asked exact declarations/code Remembering/Operating/Signaling/Nexus/Entering/MemoryHandle/OperationHandle/MainActor/RunningTask, Memory read/change messages and Memory-open/actor-graph startup; relevant methods only. Field separately asked current dependency actual metadata/config store and peer-identified meta transport contracts or none found, revisions/authored status. This read-only design extraction must NOT expand/delay isolated transplant freeze/gates. No new design or implementation scope.

## Immutable interim artifact and review

Chronos66f22a20e104d5110acb6af3b2f2ca1585b50356 base679fa1865a3d85a28524d406d387627cf3b58896, clean empty childcdb0eace775e lock25515. Patch /tmp/chronos-entry-transplant-679fa18-66f22a2.patch SHA25609ea917c0871af37ae4c3233b44fd279eaeb7d997c092c1c9a3811c689ff26f3. Independent audit_test_diff exact diff and Field dependency/consumer readback active. Owner final gate AFTER reviews: nix build six checks build/test/doc/fmt/clippy/ethos-source remote with pipefail+revision assertion, /tmp/chronos-entry-transplant-66f22a2-final-composed.log. Preliminary green not final acceptance. No push/deploy.

Exact design packet /tmp/chronos-54420d-config-extraction.md read and forwarded Core; RunningTask absent despite claim, requested supplement. No current dependency usable standard config store/identified meta transport found; Flow separate examples explicitly not dependency. Core asks product distinction (location-only entry experiment vs actual deployed/full-service path) now sent owner, authored vision:herdr-nexus-v1 pointer asked Field. No service scope expansion.

RunningTask supplement filled from frozen66f22a2 entry22-58, report SHA256c513246a29e9b03f5c246881d61cd2424191e9b7999a160e0e926005e3db4cde. run(self,Cancellation)→Future<Result<(),LifecycleFailure>>; cancellation watch receiver only, no actor handle. Exact declaration sent Core; full addendum also lifecycle/failure/cancellation. Initial shell quoting failed before dispatch, corrected safe quoting.

Authored vision pointer returned Core: /home/li/primary/.codex/skills/vision-herdr-nexus-v1/SKILL.md Meta35-37,Set63-73,FrameCapacity.ByteLimit69. Lookup only, module not reloaded/copied. Field base-only nexusec097e3 ConfigurationState/Configurable+SocketAuthority not standard config store/identified transport, candidate removes dependency. Exact declarations requested; no translator in graph.

Serving distinction owner packet /tmp/chronos-54420d-serving-scope.md SHA2564fa50553afb49d2eda7030fb8e8dd51d664468cd215db9bcee888185a340b241. Real repo daemon entry is location-only Phase1 experiment, intended time/schedule/subscriptions only declared. No alternate full-service binary/deployment refs in bounded search, actual deployment UNKNOWN. Source behavior preserved only; no full-service/replacement claim. Returned Core.

## Immutable reviews PASS, final gate started next

Exact diff reviewer accepts66f22a20: ten files+1240/-25, hash/reverse-apply/diff-check match. entry bodies/signatures/tests equalda2e10f normalized except SIGTERM doc; integration process/lifecycle namespace/format only. Full23 exports retained. Generic frame boundary/truncation/u32max, lifecycle/socket/SIGTERM proofs preserved; no daemon-default-specific assertion (inspection1MiB, generic tests), nonblocking. Field independent dependency/consumer PASS: only nexus lock block removed, resolved kameo/rustix/Tokio unchanged, local imports/calls consistent, wire unchanged. Owner told run final exact-revision six-check composed gate now with pipefail/log; any source fix new revision/review. No publication.

Core given actual removed BASE ConfigurationState/Configurable lifecycle and SocketAuthority/Permissive contracts, not usable store/credential transport and not restoration authority.

Core config design direction ONLY: two independently served typed signal surfaces share SAME OperationHandle+Memory; background RunningTask remains lifecycle-only, no arbitrary handle access. Meta signal→operation→Memory, per-value config and Memory sole durable owner; do not restore removed whole-config API. Core specifies abstraction before behavior, no edits authorized. Owner notified; frozen gate independent.

## Final composed gate and combined recommendation

Owner final six-check nix PASS exact66f22a20, pre/post workspace assertions clean. build/doc/fmt/clippy/ethos-source remotely executed; test cache from SAME source preliminary run incl lifecycle/SIGTERM/privacy. First successful pipeline recorder zsh readonly status failed shell after Nix, corrected identical gate_exit retry FINAL_EXIT0 cached. No second test replay claimed.

Logs /tmp/chronos-entry-transplant-66f22a2-final-composed.log SHA2569f8706c8dfcf3f716854cf751b06e02ca4392c5be44d016d9e47a23fb1997898; retry SHA256579d8cca6c71925fddc6c8988dba80071b6f3ffbbcc700428f70fc01044e6b23; actual preliminary-test SHA25690749a668e17a694be214b96caf1f87c1ab8c5269542e9ec0eaea53634befe17. clean childcdb0eace/bookmark679fa18, canonical/Nexus unchanged,25515 held. Combined diff+consumer+gate sent Core recommending isolated transplant acceptance only, landing decision pending. Phase1/location experiment not full-service/deploy/mutable config; limits retained.

Core ACCEPTS exact66f22a20 isolated transplant, accepts same-source test cache/no forced rerun. Publication NOT yet granted: owner asked intended exact branch/bookmark/remote, target/base relation, actual package/version consequence; experimental entry-point vs main/release unresolved. No deployment/main promotion. Logs/diff+recorder failure preserved.

Exact publication PROPOSAL: git@github.com:LiGoldragon/chronos.git origin, entry-point only. Local+lsremote refs679fa186, candidate66f22a20 sole child/one ahead. main+chronos-datom-542442 ata5cf51 excluded; package remains0.3.0/no release/tag/deploy. Core asked explicit strict FF artifact/readback/release authorization; no publication yet,25515 held.

Core publication GRANT strict FF exact66f22a20 experimentalrefs/heads/entry-point at stated origin only: current verified holder recheck25515/custody cleanartifact bothlocal+actualremote parent679fa18; divergence/claim stop/no merge-rebase-force-edit. Advance/push/readback both exactcandidate then release25515. Main/otherbranches/tags/version/release/deploy excluded. Relayed owner; result pending.

## Experimental publication completed

Owner54420d verified25515/local+actualremoteparent679fa186, jjbookmark/pushentry-point strictFF→66f22a20 exit0, local/tracked/actualremote readback exactcandidate. Only entry-point heads delta; main/chronos-datom remaina5cf51f4. Cleanworkspace/canonical,Nexus unchanged.25515released+absent. No tags/version/rebase/force/deploy. Account /tmp/chronos-entry-transplant-66f22a2-ACCOUNT.md SHA256df2b8cdbb02afb12ef704ca65a0a2e9c55b10f438b9894493589e21f2d098e52 and prefixed publication receipt files. Reported Core complete. Only Phase1/location experiment; mutableconfig/fullservice/release/deploy incomplete. Bounded authority ended.

Separate ChronosAudit24triage: nexus-ethos-part.md79-83items33/34/38/39 targetmainc95b07b,notlanded66f22a20. AuthoredoldTypes/import/layout/comments+ethoszerobcf728b;generateddatomicnotauthority. Coreaskedapprovedgeneratorcompatibilityslice/currentownerpacket,no schema/regenerationedit. Landedtransplantauthorityended.

Coreauthorizesread-onlyAudit24compatibilitypacket exactmainc95b07b/pinbcf728b: today-supportedauthoredsyntax,minimalsupportedmigration,exactgeneratorrev,generated/API/consumerimpact; distinguishsyntaxcleanupfromnewdomainroots. FieldaskedverifiedcurrentEthosZeroowner;logicalMindethosZeroSecondaryaskedconfirmbinding+packet. Noregeneration/pin/sourceedit/experimentalmerge.

EthosZeroowner6dad92confirmsAdopted.6dad92on051,worktreerepoethos-zero/branchkind-to-trait,lastcleanpushedf0c8bf2;read-onlycompatibilitypacket underway,no writer/migration.

EthosZeroauditdeviation:subflowGenerate/tmpcopydespitenoregenerationbrief;stopped,norepopin/source/build/merge. Coreinformed,outofscopeattemptNOTauthorizedcurrentrevvalidation;source-backedpacket+executableprovenancepending,no rerunrepair. PreliminaryTypes→Library+fourthsection,notrenamealone.

FinalAudit24source-backedpacket6dad92:exactmainc95b07b/bcf728b5.0→proposedf0c8bf24792f1c30626ea2571312dc10cf5d2d8c19.0.1(notearliestclaim). Types→Library+fourth[];superimports/requestresponseordinaryLibrary retained. Futuredevpinlockclosure/testregenerate API ethos_zeroActualizing/Generating/Potential.actualize replaces protosActualizable/Potential.actualize(()). Generatednamedfields/currentderiveonlytexttestnotruntimelib;c95bnot66experimental. Noauthorizedregen/edit/build. Scratchtarget/debugprovenanceunproved,NOTcurrentvalidation,/tmp/chronos-auditpreservationunverified. OwnercurrentpasscompleteWAIT. ReportedCoreonly,no newpass.
