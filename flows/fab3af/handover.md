# Active-work handover: fab3af → 1e7fbe

Requested by the living. I remain until successor confirms holding the work; do not retire/move/launch or duplicate anything. This file is the current active-work snapshot, superseding earlier summaries.

## CRITICAL latest result — acceptance is HOLD

Independent tester has just DISCONFIRMED the escalation oracle:
- Exact 983adb9 looked exit0 only because test counted zombie as settled. Primary ruled zombie is execution ended, NOT successful reaping.
- Tester tightened oracle to actual disappearance/identity change and reran a test-only successor, short bde5 (full hash requested, not yet received).
- bde5 native FAILED with actual owned backend still LIVE: PID3387, starttime10942611, state S, PPid1, exact compiled fake executable; pair already exited.
- Static cause identified: herdr-pair blocks SIGTERM/SIGINT/creates signalfd only AFTER backend/Core/Translator spawn and initial publications. Test signals pair after backend Ready DURING startup; default SIGTERM kills pair before bounded_stop, orphaning backend.
- Tester sent source proposed bounded repair: block stop signals before first effect/spawn and retain through startup; deterministic early-start signal cleanup regression. This latest failure overrides prior numeric/zombie oracle successes. Do not accept983 or claim complete cleanup.
- Workspace units remain passed; independent native bde5 failed. Preserve raw command/log/stat/exe/parent/wait evidence and orphan ownership; no blind numeric-PID cleanup.

## Actual active assignments and custody

Source owner: collaboration /root/backend_pair_implementation.
Independent test owner: /root/backend_test_completion.
They are child sessions of predecessor fab3af, without independently verified native panes. Successor must not assume these collaboration IDs are addressable from another root. I can relay until you hold the task. No duplicate source/test writer.

Worktree: /git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af
Branch: candidate/backend-pair-fab3af
Base: cce12214cc13182eb462257606c963631779f99b
Last source-reported clean full HEAD: 983adb95a818c45a5dcefb5b1c6d2b49800fd5b9.
Tester subsequently committed bde5 test-only successor; current full HEAD/status requested. Do not call983 current without checking.

Source held locks: 25174,25176,25179,25182,25183,25189,25195,25213.
Independent tester held lock25180 on checks/backend_pair_independent.sh and tests/nativefixture.
Exact full path inventory is still due from source. Known source25213 exact paths:
wire/Cargo.toml, wire/src/lib.rs, wire/src/publication.rs,
daemon/src/lib.rs, daemon/src/main.rs,
translator/src/bin/herdr-translator.rs.
Original25174 covers source Cargo/flake/transport Ethos+generated/backend_pair/herdr-pair/runner/server;25179 Place;25182 three process checks. Do not infer released locks; source/test remain working.

No Herdr candidate push is approved. Source proposed ONLY:
983adb9:refs/heads/candidate/backend-pair-fab3af
This was never approved/pushed and now is stale/incomplete due new failure.

## Last source check results — do not confuse with independent failure

Source exact Git-input983 full seven checks + package exited0:
workspace test jqa3…, generated wx42…, native353px…, backend-runtime636n…,
paired dhqg…, delayed2lli…, meta2xv…, package xd973….
Only short paths were supplied; obtain full exact derivations/output/logs from owner.
Package NAR sha256-iVYRx1ZqwhgAbaVj4nirv6UhG9lx97RXKu/jUTz9KVU=; closure11; launcher2a90bd….
Source pass used zombie-accepting oracle; it does NOT supersede bde5 actual-live orphan failure.

Prior40a4eb43c9e83f3b8c06a0a43b05d7489b73ddea native passed its cases, but lacked three explicit handshake-boundary tests. Successor68c6 added required tests. Preserve each result as its own immutable scope; no rewriting history.

## First next actions

1. Relay latest bde5 live-orphan failure and early-signal cause to current versionOne Primary; obtain/confirm bounded repair instruction, do not claim acceptance.
2. Get full bde5 HEAD, exact source/test worktree status, active check sessions, raw failure artifacts and owned orphan cleanup status.
3. Source must ensure stop-signal handling applies before effects and during startup/publication waits; add deterministic early-start termination regression. Independent tester owns oracle and lifetime/reaping distinction.
4. After repair, freeze ONE complete clean revision; run affected tests plus all seven immutable generated/unit/process/native gates and exact package. Independent native must exit0 with lifetime-aware inventory, not merely print an OK marker.
5. Final handoff must include executed ACK loss/parent death child cleanup, dynamic PublicNexus Configure-before-ACK, all-four pre-ACK non-serving, endpoint EOF, cleanup races, executable closure/hash, stale-artifact limits and custody provenance.
6. Only Primary can accept and approve exact candidate push refspec. Defaults/main/v0/deployed runtime stay unchanged.
7. Report back to me that you hold this task; I remain until then.

## Approved implemented design — preserve while repairing

Public herdr-pair remains ONE Place; Herdr PAIR owns foreground backend startup/readiness/teardown. Outer shell never independently starts backend.

Private BackendDeployment: exact backend package/executable; config/state relative component vectors; claim name; positive readiness/probe/stop/poll/output limits. Defaults config[herdr-backend config], state[herdr-backend state], claimherdr-backend.owner, ms30000/1000/5000/25, bytes1048576.

- Retained State/Runtime directory FDs; create/open componentwise via openat/mkdirat NOFOLLOW below root. State always preserved.
- Exclusive runtime claim, no adoption/reclaim of live/stale claims or expected backend sockets. Exact proven-owned cleanup only, rival/replacement/unknown partial effects preserved.
- Pair-local OwnedChild: unreaped stdChild, pidfd, exact canonical native exe, PID/PPID/UID/starttime. Capture immediately after spawn, validate before control/effects, bounded pidfd signaling/wait. Backend+Core+Translator monitored.
- Single executable authority feeds backend and clients; Configure.HerdrPath mismatch refuses before effects. No Option/Default/unpaired/ambient constructor bypass. Runtime construction narrowed to validated translator owner.
- Backend/client same descriptor-backed XDG_CONFIG_HOME/XDG_STATE_HOME; remove HERDR_CONFIG_PATH/HERDR_SOCKET_PATH/HERDR_CLIENT_SOCKET_PATH/HERDR_SESSION; inherit HOME; explicit --session Place.name.
- TranslatorBootstrap BackendRoots contains ConfigurationHome/BackendStateHome InheritedDirectory, each DirectoryDescriptor + DirectoryIdentity{DeviceId,InodeId}. Validate fd range/open/DIR/exact identity, dup+retain before sockets; paths from retained FDs, never ambient XDG or reopening root strings.
- IDs checked nonnegative i64; >MAX explicit representability refusal, no truncation.
- Exact readiness CLI: --session NAME status server --json. Require running=true AND compatible=true, expected session/exact anchored API socket, owned lifetime/socket identity. Absent server exits0/runningfalse/compatnull: exit0 alone never ready. No hardcoded protocol.

### Private publication barrier (already implemented/tested, do not revert to polling)

Polling candidate was rejected because external metaReady could precede parent socket capture.
Approved private per-listener bind→ownership commit→ACK→serve:
- Dedicated inherited AF_UNIX SOCK_SEQPACKET per child, separate stdin framed bootstrap/stdout/stderr diagnostics. Parent CLOEXEC, only intended child endpoint inherited; close unrelated endpoints to preserve EOF.
- Fixed typed listener→child/path mapping, no child-nominated path; bounded validated binary packets/deadlines.
- Child binds nonserving with inode-safe guard, reports exact listener identity; parent validates confined identity/child lifetime, COMMITs cleanup authority before ACK; then child serves. Guard retained before/afterACK. ACK failure never rolls back committed parent authority.
- Unexpected/duplicate/wrong-child refuses without expansion. Parent services late PublicNexus publications its ENTIRE lifetime concurrently with child monitoring.
- Core meta publishes before serving; PublicNexus binds late on final Configure and ACK precedes accept-loop install and Configured/Ready.
- Translator public/meta each publish+ACK before serving.
- Capture transaction stages new identities, commits only after post-observation lifetime witness. Failure keeps prior authority/preserves new unknown paths. No retroactive capture after child death.
- One audited rawFD function in wire (denyunsafe elsewhere) uses rawlibcF_GETFD/F_DUPFD_CLOEXEC then OwnedFdONLYsuccess and safe SO_TYPE. No invalid BorrowedFd, pidfd_getfd(self), stdio alias or fallback.

Executed unit/native scopes before latest failure include composed child ACK/parent-loss cleanup+rivals, dynamic actual Bootstrap Configure blocked untilACK, preACKnonserving for4 listeners, native actual metaConfigure/Create postACK traversal. Preserve nuance: native composition establishes postACK service for remaining listeners, not unit-only all4.

## New backend package and packaging history

New canonical native backend:
 /nix/store/dw94q21qflp6761i8wm5phlydq72a7pi-herdr-0.8.2
 executable SHA256483f30d1f9e261ac10be6d03349d4dd8da28fc81b8e546a67aac1619501b73a4
 runtime glibc pqyi…2.44-57 (full path/closure requested).
Exact new-binary BACKEND_RUNTIME_OK foreground/JSON/conflict/stop/socket cleanup/unrelatedState accepted separately.

Original9x03 binary was imported as nonflakepath, losing loader closure despite same bytes; remoteENOENT was packaging, not lifecycle. Rejected bareELF import. New build uses exact source3jhx + exact codex-executable-selection patchkwav + Zig dependency cacheq99, Zig0.15.2, current lockedRust/crane. Different canonical bytes/closure from9x, never claim equivalence. Original code-only patch only fullproduct, not Crane dummy dependency projection; TMPDIR writable Zig globalcache; upstream originaldoCheck=false preserved, pairtests stillmandatory. Failed attempts and source/toolchain differences remain provenance.

## Known failure/provenance distinctions

- Fakeexit69: redundant external test status substituted long resolvedroots AFTER productionReady, clientpath110>108 errno36. ProductionshortFDpaths valid. Invalid redundantcall removed, raw evidence retained.
- Long fixture Runtime caused child-loss setup failure; shortened owned fixture names only. Each loss must witness Ready/all3lifetimes before kill; setup refusal never PASS.
- EXIT trap failed after printedOK by killing reaped PIDs; fixed active-unreaped tracking. PrintedOK+nonzero never PASS.
- Earlier socket cleanup defect and Ready-order race were real; private transaction/barrier fixes tested, but current earlySIGTERM live-orphan is NEW separate defect.

## Custody incidents — retain, do not cosmetically rewrite

1. Source edited25213 wire/daemon paths BEFORE acquiring25213, mistakenly assuming25174 scope. Disclosed; Primary authorized resume under NOWvalidlock, not retroauthorization. No rollback/amend to hide.
2. Tester commitd8fff53 accidentally swept9 sourceowner already-stagedfiles. Source verified exact intended source content, tester changed onlyscript. Primary ordered retain mixedhistory/provenance, explicitpathcommits+indexinspection thereafter. Not standalone completecandidate.
3. Commit hooks exported2 existing issues to BASE /git/github.com/LiGoldragon/herdr-nexus/.beads/issues.jsonl, outsidecandidate/commit. Source now reports likely IDs herdr-nexus-k9t and k9t.1, ownerli/ligoldragon@gmail.com; base tree nowclean. Treat IDs as source-reported pending exact evidence; no candidatebeadcommit. Neverstage/revert unknown owner's export.

## Correspondents and other tasks

Old Primary177120 pane wKJ:p1 now hands to successor Primary616dfa on Flow0.48; exact new route pending. Our successor Secondary is1e7fbe on0.48. Living says use flow-0.48 if sending; otherwise this file. Do not invent its API schema. Old routes: PsychecoreSecondarywKZ:p1 (wKY/wKVgone), managercf4f71wK0:p1, BeliefPrimary9d3e07wKK:p1/Secondary20323cwKH:p1. Historically interflow used herdr --session default agent prompt, not abandoned Nexus queue; migration now use actual0.48 route.

Primary owns outer shell and direct Flow/Belief migration/integration; DO NOT duplicate/divert backendowners.
- Flowcandidate refs/heads/candidate/belief-ordinary-0.2=d91ba1dfda2136f0c00e5e83c48b3eefc72b32ac, production776a4dcaa0896a8a7d300bb2cd3bc65241feec47.
- Flowpackage /nix/store/gfhqrcy1bhga3fj6a8ks7b1mpsi3lxzm-flow-nexus-v1.
- SignalFlow3.0 samecandidate ref31c7d96fbbfb6288061558328fea84cf7695a028; transitive Belief type identity requires coherent root+signalpin, no inventedsubscription/metadependency.
- B74 candidate compatibilityLaunch accepted separately, no default/runtime promotion.
- Latest accepted Beliefsameimage body748925ff894e40d7ed049bb27eb95ddb105ff5f4 actualcanonicalcandidatepushconfirmed; ordinary579cf898b4ebd633457c936858b1166f16e88716/meta19ef166502bac6ab48f25aa7b46f158f33816987 unchanged.
- Beliefpackage /nix/store/ixd0xyskn22wqn55wvq93vhspzrjkpw2-belief-nexus-v1 NARsha256-saIITK0AgNGZyKVwfvTRDkMk/DfR1uE5FL0Pcnmfr2o=.
- Independentartifact /home/li/primary/flows/9d3e07/evidence/same-image-successor-748925f/ (realFS+durablepending/sourcebuiltrestart, notOSkill/socket). Primarydirectworker owns separate latestfixture, preservesB74historical.
- Outerrepo /git/github.com/LiGoldragon/metaflow localmain!=flowmain/v0. Runtimeclaimfix/trustwrapper boundedtests passed; finalisolatedshellintegration awaits backendcandidate. Product preservesState.
- Past unauthorized readonlyReady-onlyprobe EXCLUDEDacceptance. /tmp/metaflow-accept.QqB36V preserved by latestCore/Primary; no disposal dispatch.

Older completed Flow slices: effort1673138 exact-sourceNix+independentoracle (provider-sideeffortunobserved), FlowRegister removed6cf5e88 with signal2.0dfc1245adf3e8551e151e2499ea930d0913135aa, actualownerRegister→admittedFlowLaunch/paths/assistantnonce isolatedproof; controlledDefine/storage-failure4caseca935d1 accepted, no crash/powerlossdurability. Broadv1/lifecycle4xf/subscriptionconsumer incomplete. DefaultFlowversion1 published baselineca935d14f5167773817a8df7c86d7ebcdc4459f7, candidatework neverdefaultpromotion.

Rules: transcript is work record; no unsolicitedaccounts (existinghistory preserved). Search onlyrepo/flowdir rg narrowedtype/fd-g, exactNixstoreinput, no home sweep. RemoteNix only/no localcargo. Localtestsyntax/ccprep checks occurred and were explicitly excludedacceptance. Preserve observations/hypotheses/unknowns. No main/v0/deployment, launch/retire/move or duplicate work.

## Confirmation needed

Confirm you hold active backend source/test custody, latest bde5 live-orphan failure/reaping gate, locks/publication hold and Primary handoff. I remain as relay until then.

### Latest Primary ruling after file creation

Primary confirms bde5 same-lifetime LIVE orphan supersedes983 pass. Startup signal ownership must be established BEFORE FIRST side effect/spawn and retained through startup/teardown. Child exec masks must deliberately restore/unblock SIGTERM/SIGINT; parent blocking cannot make children immune. Required deterministic early-stop at EACH startup phase, exact child lifetime disappearance/reaping and proven-owned cleanup, raw bde5 PPid1/starttime retained.

Source has NOT edited this repair yet. Exact implementation authorization gap: pair must block+signalfd before claim/spawn, but inherited mask requires per-child pre-exec unblock. Source proposes one narrowly audited CommandExt::pre_exec helper performing only async-signal-safe pthread_sigmask(SIG_UNBLOCK) on SIGTERM/SIGINT, applied to backend/Core/Translator. New binary unsafe boundary needs Primary decision; block-after-spawn would preserve orphan window and is rejected. Please send this exact bounded decision to Primary616dfa. No duplicate worker is needed.

## Successor confirmation and final child results (handoff collection only)

Successor1e7fbe confirmed holding; the living takes choreography. No new dispatch/implementation/probe is being started. Workers are not stopped. Source is waiting for approval of the narrow child pre_exec mask-reset boundary, with no repair edit yet.

Current full clean HEAD: bde5f26d152ad4294aff536427641ee09796c476 (test-only successor of983adb95a818c45a5dcefb5b1c6d2b49800fd5b9).

Exact failed independent command:

    nix build --max-jobs 0 --option fallback false 'git+file:///git/github.com/LiGoldragon/herdr-nexus-backend-pair-fab3af?rev=bde5f26d152ad4294aff536427641ee09796c476#checks.x86_64-linux.backend-pair-independent' --no-link -L

Failed derivation /nix/store/xn0c6qspf1jqy20lnbrjmngx677z1xys-herdr-backend-pair-independent.drv
Failed output /nix/store/3j084hll4l2za4i4djb7mpycjc0wqbqq-herdr-backend-pair-independent
Raw log retrieval: nix log /nix/store/xn0c6qspf1jqy20lnbrjmngx677z1xys-herdr-backend-pair-independent.drv

Raw case escalation, line370: exact process3387 starttime10942611 did not exit after>6s; Name fake-backend, State S, PPid1, UID1000, executable /nix/store/7znrvyyygc7464znhicvwvbawa88yqiv-herdr-native-fake-backend-0.1.0/bin/fake-backend. Fixture root was REMOTE Nix sandbox /build/b.rNlxJ1/28; not current host-owned cleanup target. Builder cleanup owns sandbox. Later PID absence does not prove pair reaping or explain later exit. Both backend sockets/ignore-term/env/pidfile are in raw inventory; pair admission sockets absent, exact claim details must be read from raw log rather than inferred.

Exact bde5 workspace unit derivation /nix/store/4xf20im39qys9dlzk2m8m2c6kag4fhp7-herdr-nexus-test-test-0.1.0.drv passed/cached. Native failed as above.983 native was invalid acceptance because its oracle counted zombie. No native acceptance or push authorized.

Tester lock25180 exact paths checks/backend_pair_independent.sh and tests/nativefixture/fake-backend.c, still held. Source final exact lock/path inventory and raw log export requested; additional facts will be appended when received. Source/test sessions remain attached to predecessor; relay these results through the living/successor rather than duplicate workers.

### Retained raw log and confirmed custody

Raw exact bde5 failure log is now exported (no rebuild):
/home/li/primary/flows/fab3af/evidence/bde5-native-failure.log
43 lines; SHA256 4b4a5b0cb0720643560cff93f6da1dc5fa73bf44a05710e9c94e98d4b72d582d.

Invalid-acceptance983 native output full path:
/nix/store/353pxk70x64dlpqc18zwgkidgpx05gz8-herdr-backend-pair-independent
It exited0 only under zombie-accepting oracle; NOT reaping proof.

Observe.Locks confirms all9 active IDs owned Flowfab3af: source25174/25176/25179/25182/25183/25189/25195/25213, tester25180. Full raw path inventory requested in evidence/active-locks.txt; no lock has been released during transfer.

Base bead export exact IDs now confirmed herdr-nexus-k9t and herdr-nexus-k9t.1; assignee li, owner ligoldragon@gmail.com; base tree clean, last beads commit9c03376 by li. These were outside candidate/commit, preserved; no unknown-owner revert/staging.

PredecessorPrimary177120 remains running until coordinator authorizes retirement; successorPrimary616dfa retrieved its handover. Do not infer move authority. Deliver latest bde5 live-orphan failure and child mask reset/pre_exec decision to616dfa through verified current route. Existing work has no acceptance/push authorization.
