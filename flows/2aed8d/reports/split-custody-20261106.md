# Actual disjoint internal source custody — 2026-11-06 split

Core ordered split; original Orchestrate owner remains2aed8d. No lock release/transfer or reparent. Old implementation worker native01a1adee-75af-7043-a7cc-1ffa6eedf393 ACTUALLY acknowledged handoff/quiescence/write-abstention at2026-11-06T05:43:22Z. No Datom/Protos running effects reported. Do not confuse followup dispatch with that actual ACK.

Exact absolute-path→SOLE permitted writer map under retained locks:

- `/git/worktrees/meta-signal-flow-config-d05351-independent` (25624): existing worker `/root/implement_052`, native01a1adee-75af-7043-a7cc-1ffa6eedf393 ONLY. Meta accepted05:43:22Z/deadline06:43:22Z/nextbeat05:53:22Z.
- `/git/worktrees/datom-codec-config-d05351-independent` (25626): new write-ordinary Luna publication/materialization appointment PENDING; NO writer until actual child appointment/acceptance is recorded. Old worker explicitly relinquished ALL writing here. No source redesign authorized by new task.
- `/git/worktrees/protos-config-d05351-independent` (25626): READONLY, NO active writer. Old worker relinquished all writing. No new Datom appointment authorizes edits here.
- `/git/worktrees/flow-config-d05351-independent` (25623): PAUSED/preserved under original owner, NO active writer. Separate explicit Flow handback required after BOTH immutable dependencies land.
- `/git/worktrees/sema-config-d05351-independent`, `/git/worktrees/sema-engine-config-d05351-independent`, `/git/worktrees/signal-flow-config-d05351-independent` (25624) and `/git/worktrees/redb-config-d05351-independent` (25625): HELD/preserved, NO active writer under this split.

Meta alone may generate/review/publish its admitted bd1 work. Datom appointment only publication/materialization of exact immutable dc9987d and dependency-route reconciliation within explicit scope; no Meta/Flow/Protos changes. Same existing nonauthor reviewer is used for immutable gates, never another writer. No source edit by parent. Whole04:50:31MISS retained; no240reset/STEP4.

Actual snapshot from handoff: Datom clean dc9987d38c9aa01ebf246f98ec9f5b78a12cc4eb/treee246c2047bacfae3792cb283512024dd8fbffe6d; Protosclean2c76ccf1ed7ba646a62962131bd60f8886daac54/treeb6551eb8afb2d4089c84e93c0bb411e3534d1b0a; Meta cleanb7fcb04c5ffec830fa62dcabaac0be6c434d5c1f/tree331fca45c237b013075937b100e3502b0c694d55. Actual held Datom remote ref e1a275b2e782defc38c9826453e9d538a069353c. dc immutable independent review NOT yet done.

Recovered full outputs: generated-kinds /nix/store/2qv3yxhyg5y8w5jbh9j179pxwab79dkc-datom-codec-generated-kinds; tests /nix/store/ak3dii71bwfdd1v7w6q7fqqsxzbj0qqf-datom-codec-test-0.33.0. Commands `nix build --no-link --print-out-paths .#checks.x86_64-linux.generated-kinds` and analogous test selector were DIRTY-WORKTREE before dc commit, retained thread only/no durable full log. These are qualified historical evidence, NOT immutable candidate proof.

## Actual appointment result — BLOCKED role/model mismatch

After actual oldwriter05:43:22handoff, parent spawned EXACTLYONE candidate `/root/datom_materialize` using `agent_type=write-ordinary`, `fork_turns=none`, no modeloverride and no second candidate. Tool admitted task. Child FINAL refused acceptance BEFOREeffects: it reports actualsession Mind/Secondary/Sol (`gpt-6.1-sol`) ratherthanrequiredwrite-ordinaryLuna, nativebindingnotexposed/pending. It cannotacceptpublication/materialization. Read-onlycandidatecleanfactdc9987dreported05:45:37; no publication/materializationeffect. ParentdoesNOToverridecapability/modelorlaunchsubstitute.

Therefore DatomappointmenthasNOactualacceptanceUTC/60mdeadline/nativequalifiedwriter; NOcurrentDatomwriter. Protosreadonly. OldnativeDatom/ProtosrelinquishmentSTANDS (notreinstated). ExactMetaoldnativecontinuesONLYMetawithacceptance05:43:22/deadline06:43:22/beat05:53:22; FlowPAUSEDpendingbothdeps+explicitFlowhandback. ExistingOrchestratelocksremainoriginalowner2aed8d/no fictionaltransfer. Requirednextdecision: supportedNON-Solqualifiedwrite-ordinaryLuna launch route, notpermissiontoinferrolefromtoolargument. No independentdcimmutablepublicationgatewasclaimedclosed; remoteexpectedOLDe1andimmutablebuildproofstillowed. NoSTEP4/reset/rollout.

## FIXED scheduling update, actual delivery/ACK05:55:00Z

Core supersedesrelative60minwording: BOTHDatommaterialization andMetageneration/publication DUE06:45UTC. MetaactualupdateRECEIPT/CONSUMPTION+SCHEDULINGACK2026-11-06T05:55:00Z; NEW10minACKcutoff/nextconcretebeat06:05:00Z. Notnativefollowupadmission/prior05:43acceptanceclock. Old06:43:22supersededonlyscheduling, unchangedscope/handoffremainsvalid.

DatomhasNOacceptedqualifiedholderfollowingONLYappointmentrole/modelmismatch, so no Datomupdate-delivery/ACKcutoffcanbewitnessed; fixed06:45appliesfutureholderwithoutreset. NOreplacementauthorizedbyexpiryalone: requiresrevocation+actualquiescence/filecustodyexclusion+freshonequalifiednonSol/fullbrief. No duplicateappointmentunderthisupdate.

FreshreadonlyOrchestrate05:54:16 owner2aed8d locks25623–26/exactapprovedpaths, reasonsstillnameoldnative. Actualtoolreservationsdonotencodeper-childper-pathEXCLUSIONS:25624coversMeta+Sema/Engine/signal;25626coversDatom+Protos. ExplicitCoreINTERNALmapremainsabove; nofictionallocktransfer/changedexclusions claimed. Metaholderacknowledgesrepresentationalgap; noreset/transfer. CurrentoneactiveMetaallocationplusnoDatomwriteravoidsactualoverlap; futureappointmentmustsatisfycustodyrule.

LatestexplicitFlowhandback: oldnative01a1adee... soleoriginalFlowholder MAYcompile/testexistingFlowpathwhenpublishedcorrectedDatomandactualgraphpermit WITHOUTwaitingMetabyblanketrule; NOFlowSOURCEeditpermission/newwriter. Actualgraphcurrentlyblocks: FlowCargo.toml19 pinsMetae2d8c973; currentb7Metaunpublished/reviewheld→Datome1(notdc); b7→flow-ethosb92b9689190c62db4f4c66a2b39cafe356cec1e4→Datom4dff16unavailable. dcunpublished. No buildattempt/pathoverride/redundantknownfailedcompile. e2remoteavailabilitynotindependentlywitnessedbyparent—manifestpinisnotpublicationproof.

Whole04:50MISS/no240reset/noSTEP4 remains. Parentno sourceeffects. ExistingMetaONLYholdercontinuesreview/evidencewithactual05:55ACK, fixed06:45 andnext06:05beat. Source/archiveWIPpreserved.

## Explicit Terra replacement attempt — refused, NO accepted Datom holder

Freshoriginalregistry verified prior `/root/datom_materialize` DEFINITIVELYcompletedmodelrefusal/nochildrenbeforepublication/materialization. CorethenauthorizedEXACTLYONEreplacement. Parentcalledspawn_agent with task_name datom_materialize_terra, EXPLICITmodel `gpt-6.1-terra`, `fork_turns=none`, noagent_typeoverride/nominalwriteordinary. Supportedtoolaccepted `/root/datom_materialize_terra`; no retry/modelcycling/substitute.

ChildFINAL refusal: actualdeliveryobserved2026-11-06T06:05:22Z; ACKcutoff06:15:22Z; fixeddue06:45Z. Childreportsactualmodelgpt-6.1-sol/MindSecondarynotrequestedTerra; actualCODEX_THREAD_ID01a1af75-c09d-7431-93a6-e805d82b355f; nativebindingpending/unverified; technicalfilesystemwritecapabilityexistsbutqualifiedexclusivecustodyACKNOTgranted. Itreadonlyverifieddc9987d/treee246c204cleanandperformedNOsource/build/materialization/publication/ref/networkeffect. This isrefusalnotacceptedappointment. ParentdoesNOToverridechildreportedrole/modelorlaunchanother.

ThereforeNOacceptedDatomwriter/remainsunassigned; oldnative01a1adeeDatom/ProtosauthorityREVOKED05:43:22stillstands. No source/refcustodytransferorrelease. MetaexistingholderONLYMeta/native01a1adee... retainsactualscheduleACK05:55/fixeddue06:45/nextconcretebeat06:05. Protosreadonly/backendheld; Floworiginalholdercompile/testonlyconditional/currentgraphblocked, noFloweditor. Bothfixed06:45, whole04:50MISS/no240reset/noSTEP4. NeedexplicitlyreconciledactualTerra-role/nativebindinglaunchroute, notinferredfromacceptedmodelparameter; no duplicateappointmentunderthisgrant.
