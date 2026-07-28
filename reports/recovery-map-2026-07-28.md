# Recovery map — 2026-07-28

## Purpose and evidence boundary

This is an execution map, not an assertion that any repair has been made. It
synthesizes the read-only estate inventory, core-operations audit, and
Schema-to-Ethos audit dated 2026-07-28, plus the current primary beads
`primary-akw` and `primary-m8w`. No command in preparing this map mutated a
repository, service, store, bead, remote, or worktree.

The evidence establishes three things:

1. Orchestrate's live claim/observe boundary works; its worktree lifecycle has
   historical failures and a dirty/stale registry.
2. Messenger starts but its observed submission path forwards to a deliberately
   absent router socket. Mind is not deployed. **Logics** has no established
   referent and remains an unresolved term; Logos and Lojix are distinct
   candidates, not aliases.
3. Mind, Orchestrate, Messenger, Router, and Spirit still compile their
   contracts through `schema` / `schema-rust`. Ethos/Nomos/Logos is valuable
   prototype work but has no component-compatible generator or demonstrated
   three-daemon, per-store witness.

The map deliberately separates observations from proposals. A named target is
an exact planned edit or state boundary, not evidence of ownership.

## The first decision the psyche must make

Choose the migration posture:

- **Recommended: allow a bounded temporary Schema compatibility compiler.**
  Mind, Orchestrate, Messenger, Router, Spirit, and their signal crates retain
  the existing `schema` / `schema-rust` generation seam while Ethos progresses
  in an isolated, temporary-store vertical witness. The compatibility boundary
  ends only when one component-facing Ethos-generated contract has equivalent
  checked-in-artifact, freshness, metadata, frame, and daemon-runtime behavior.
- **Alternative: require final Ethos shape immediately.** No new or revised
  component deployment may rely on the Schema compiler. The replacement
  generator, translator/authority, per-daemon persistence topology, inventory
  naming, and first component port become prerequisites for the Mind/Messenger
  recovery work that currently depends on Schema.

This is psyche approval because it determines whether a ruled target is staged
through an adapter boundary or imposed as the immediate system shape. It is not
safe to infer from implementation names. The rest of this map is explicitly
branched on that answer.

## Ordered recovery sequence

1. Preserve ambiguous working state and establish an owner/disposition record.
   Do not delete, refresh, reconcile, or push it.
2. Select the canonical local Messenger contract, then repair and prove delivery
   on a non-production witness. This is the P0 coordination blocker.
3. Add and prove a declarative Mind deployment only on the selected compatibility
   branch; leave Orchestrate's working claim/observe path in service meanwhile.
4. Resolve the exact referent of **Logics**. If it is Lojix, continue the
   already-recorded durable v1-to-v2 migration; if it is Logos or another
   component, create a separate, named deployment/witness lane.
5. Run one authorized disposable Orchestrate worktree lifecycle witness; only
   then classify registry records and cleanup candidates.
6. Continue Ethos using the selected branch below. Do not let an incomplete
   language migration silently change the live component compiler.

## Immediate operational repair

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **O1. Adjudicate the local Messenger contract.** Targets: `/git/github.com/LiGoldragon/message/AGENTS.md`, `/git/github.com/LiGoldragon/message/src/{daemon.rs,engine.rs,router.rs,config.rs,schema/{signal,nexus,sema,daemon}.rs}`, `/git/github.com/LiGoldragon/message/tests/{forward_to_router.rs,process_boundary.rs}`, `/git/github.com/LiGoldragon/signal-message`, and `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/message.nix`. Choose one coherent contract: Messenger owns durable local identity/delivery and uses Router only host-to-host, or Messenger forwards every submission to Router. | Design decision first; then source, generated-contract, test, and Home Manager service configuration edits. | A mixed result can strand messages, weaken owner boundaries, make the service configuration lie about persistence, or make local delivery depend on the absent `%t/router/router.sock`. | A reviewed contract record agrees across source, test, service module, architecture, and generated signal surfaces. The implementation gate is O2, not socket presence alone. | First migration-posture decision does not determine this; it does determine which compiler may regenerate touched contracts. | **Yes.** The present source, deployment module, and messenger-first design conflict; no implementation can choose among them by inference. |
| **O2. Repair Messenger and prove a local delivery witness.** Same O1 targets plus the exact selected `CriomOS-home/flake.nix` input pin and any created check under `/git/github.com/LiGoldragon/CriomOS-home/checks/message-*/`. | Source/config/test changes; build; user-profile activation; controlled runtime message/store writes. | Bad schema regeneration, un-routable frames, stale sockets, unreadable durable state, or a test that proves only forwarding failure. | In a disposable non-production user profile: bind two identities; submit; durable inbox/read or delivery acknowledgement; recipient wake/ack; daemon restart survival; typed failure after intentionally killing the recipient. Also show local delivery while Router is absent, if that is the selected contract. Run the exact owning source and Nix gates before activation. | O1; selected Ethos branch; verified authoritative user/system manager context; release/pin procedure. | **Yes for activation and runtime witness.** Code work follows O1; service activation and deliberate store writes affect a live user environment. |
| **O3. Deploy Mind declaratively, not ad hoc.** Create `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/mind.nix`; import it from `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix`; add a narrow `/git/github.com/LiGoldragon/CriomOS-home/checks/mind-*/default.nix`; pin Mind in `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`; rely on `/git/github.com/LiGoldragon/mind/{Cargo.toml,build.rs,src/bin/mind_write_configuration.rs,tests/{configuration.rs,cli.rs,memory.rs,daemon_wire.rs,orchestrate_caller.rs}}`. | New Home Manager module, source pin, evaluation/test, profile activation, and durable Mind-state writes. | A second configuration dialect, wrong socket permissions, a state path that cannot survive restart, or an apparently installed but unreachable daemon. | Evaluate the Home Manager module; run Mind's documented CLI/daemon configuration, open/query, owner-meta reachability, and restart-survival tests against the installed daemon; then observe the exact configured socket and state path. | O2's delivery contract for coordination behavior; selected migration branch; confirmation that the inspected systemd/user manager is authoritative. | **Yes.** The audit cannot tell whether Mind was intentionally absent; deployment creates a durable live service. |
| **O4. Keep Orchestrate's current core usable and test lifecycle once.** Targets: `/git/github.com/LiGoldragon/orchestrate/{src/{claim.rs,worktree.rs,table_reclamation.rs,execution.rs,repository.rs},tests/{worktree.rs,daemon_cli.rs,store_migration_fixtures.rs},ARCHITECTURE.md}` and live Orchestrate registry/state only through its owner protocol. | Controlled non-production worktree/lane creation, claim/release/conclude operations; possibly source fixes after diagnosis. | A faulty conclude may auto-land, push a discard branch, delete a worktree, or remove a record that was still live. | After Messenger is demonstrated usable, execute one explicitly authorized disposable RequestWorktree → Claim → Submit → Release → ConcludeWorktree **Rejected** witness. Capture expected reply heads and verify no unreviewed landing; then compare live registry state with the witness. | O2; a disposable repository and unique lane; authoritative manager context. | **Yes.** The audit specifically withheld this state-changing witness; it creates and tears down a worktree and may publish a discard branch. |
| **O5. Resolve the term `Logics` before assigning its repair.** Targets are a psyche decision record and then exactly one named candidate: `/git/github.com/LiGoldragon/lojix` plus `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix`, or `/git/github.com/LiGoldragon/{core-logos,logos-runtime,logos-engine}`, or the separately named system supplied by the psyche. | Decision; only thereafter code/deployment work. | Treating Logos as Lojix can corrupt the scope: Lojix has a live v1-to-v2 store mismatch; Logos has no host deployment. | The target name appears verbatim in the approved task/bead; the follow-up witness matches that target (served Lojix request after migration, or a narrow Logos witness). | Psyche naming; if Lojix, `primary-akw`. | **Yes.** Exact-name evidence is absent; the boot contract forbids silently equating terms. |
| **O6. Continue the Lojix recovery only if O5 names Lojix.** Targets: `/git/github.com/LiGoldragon/lojix/{src/lib.rs,src/schema_runtime.rs,src/bin/lojix-inspect-store.rs,tests/{store_startup_gate.rs,store_inspection.rs,durable_resume.rs}}`, `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix`, and the existing live `/var/lib/lojix/lojix.sema` only through a tested migration. | Durable store migration, tests, system activation, live service restart/deploy. | Loss or unreadability of deployment history, a partial migration, or a restart loop. | A v1 fixture/store migrates deterministically, retains readable history, and reopens under schema v2; latest Lojix serves a request after declarative activation. These are already the acceptance criteria in `primary-akw`. | O5 = Lojix; `primary-akw`; no-backport direction recorded there. | **No new design approval if `primary-akw` remains current; yes for any change outside its durable-migration/deploy scope.** |

## Preservation and ownership decisions

No preservation item below is a cleanup candidate. The inventory's state is
point-in-time only and did not establish authorship, retention periods, or
supersession.

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **P1. Assign an owner and disposition to dirty canonical work.** Targets: `/git/github.com/LiGoldragon/{CriomOS-test-cluster,TheBookOfSol,meta-signal-mind,meta-signal-persona,schema}`; preserved items include `CriomOS-test-cluster/lib/{nestedReachability.nix,nestedSpike.nix}`, `meta-signal-mind/src/schema/lib.rs`, `meta-signal-persona/src/schema/lib.rs`, and `schema/schemas/#spirit-min.schema#`. | No content mutation until ownership is recorded; later recover, commit, discard, or archive is a separate mutation. | Tests/fixtures, personal/editorial content, generated contracts, or an active editor backup can be lost. | Named owner acknowledges the exact working copy and chooses retain/land/recover/discard; for the backup, identify the editor/session before any removal. Record current `jj status` and a content-safe disposition proof before mutation. | Owner discovery; worktree claim by the eventual editor. | **Yes.** Inventory explicitly reserves these decisions; ownership cannot be inferred. |
| **P2. Decide repair versus retirement for stale Lojix checkouts.** Targets: `/git/github.com/LiGoldragon/{meta-signal-lojix,signal-lojix}` with stale Jujutsu operations `4e1291c8d92b` and `6fa1f26bd8f8`. | Potential Jujutsu working-copy update followed by inspection; later recovery/retirement. | Updating can materialize hidden changes or overwrite the understanding of a stale working copy; retirement could lose unincorporated work. | Before an update, capture metadata and owner decision. After an authorized refresh, inspect status/diff and show either an incorporated successor or a reviewable preservation/export. | P1-style owner assignment; O5 if the work relates to selected Lojix work. | **Yes.** The only disambiguating inspection mutates state. |
| **P3. Preserve the three dirty dotted-syntax pilots as independent until compared.** Targets: `/git/github.com/LiGoldragon/{meta-signal-spirit-schema-dotted-syntax-pilot,signal-spirit-schema-dotted-syntax-pilot,spirit-schema-dotted-syntax-pilot}/ARCHITECTURE.md`, all on bookmark `schema-vision-redesign-arch-docs`. | Read-only content comparison first; later merge/land/discard only after review. | Deduplicating by name can drop materially distinct documentation corrections. | A side-by-side diff identifies identical versus distinct edits, a named owner accepts the chosen canonical wording, and each workspace's disposition is recorded. | P1 owner record; current migration-posture decision informs terminology but does not replace content review. | **Yes for disposition.** Cleanliness/name similarity is not authority to discard. |
| **P4. Resolve the orphan-like primary-linked worktree before touching its metadata.** Target: `/home/li/primary/synchronizer-release-train-p0-p2` and its linked metadata `/home/li/primary/.git/worktrees/synchronizer-release-train-p0-p2`. | Forensic inspection; possible worktree repair, archival, or removal later. | It contains retained `.agents`, `.beads`, reports, and `agent-outputs`; deleting or pruning metadata could strand the only copy. | Identify its originating lane/repository and owner; inventory retained material; create an explicit keep/archive/retire decision; only then use the owning VCS lifecycle. | P1 owner/disposition; no broad cleanup. | **Yes.** It is the highest-risk cleanup surface and lacks Jujutsu identity. |
| **P5. Defer bookmark/remote reconciliation.** Targets: the twelve non-converged `main@*` repository states listed in `estate-inventory-2026-07-28.md`, plus deleted bookmark markers in `CriomOS-home`, `core-ethos`, `core-logos`, `core-nomos`, `signal-domain`, `signal-message`, `signal-orchestrate`, `signal-sema-storage`, `signal-spirit-judge`, `structural-codec`, `textual-rust`, and `version-projection`. | Fetch/review then possible bookmark changes and push. | Pushing a deleted bookmark may permanently delete remote history; a stale local tracking view can cause the wrong reconciliation. | Per repository: fresh authorized remote state, chosen source-of-truth bookmark, review of deletion impact, and explicit push result. | P1–P4 dispositions; network/VCS authority. | **Yes.** This changes shared history/remotes and the inventory explicitly defers it. |

## Safe cleanup candidates

**There are no directories safe to delete now.** “Clean”, “at main”, a July 15
mtime, or a migration-shaped name is insufficient evidence of supersession.
The only safe work now is a *non-destructive classification pass*; it must not
invoke `jj workspace update`, prune a worktree, delete a directory, or push a
bookmark.

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **C1. Classify clean migration/cargo-repair workspaces.** Targets: `/git/github.com/LiGoldragon/{mentci-lib-cargo-migration,mentci-lib-mentci-signal-family-migration,meta-signal-criome-cargo-source-repair,meta-signal-criome-mentci-contract-migration,meta-signal-mentci-cargo-source-repair,meta-signal-mentci-client-cargo-source-repair,meta-signal-mentci-client-mentci-signal-family-migration,meta-signal-mentci-mentci-signal-family-migration,signal-criome-cargo-source-repair,signal-criome-mentci-contract-migration,signal-mentci-cargo-source-repair,signal-mentci-mentci-signal-family-migration,signal-message-cargo-source-repair,signal-persona-cargo-source-repair,signal-router-cargo-source-repair,signal-terminal-dependency-cascade,terminal-cell-dependency-cascade,schema-structural-pipe-retirement}`. | Read-only parent/change/owner classification; eventual recoverable worktree conclusion or deletion. | Ancillary files or a named migration may be the only retained evidence despite a parent at `main`. | For every path, record parent change, current clean status, owner, successor/landing evidence, retention need, and proposed disposition. A path becomes cleanup-eligible only if all five are affirmative and P1–P5 show no shared-history conflict. | P1–P5; owner availability. | **Yes for deletion or conclusion; no for the read-only classification.** |
| **C2. Classify remaining clean operational/pilot workspaces.** Targets: `/git/github.com/LiGoldragon/{CriomOS-listener-criome-recovery,CriomOS-spirit-domain-all,CriomOS-spirit-judge-deploy,CriomOS-home-laptop-colemak-merge,CriomOS-home-listener-criome-recovery,CriomOS-home-listener-zddv4,CriomOS-home-spirit-domain-all,CriomOS-test-cluster-spirit-domain-all,lojix-inspect-store,meta-signal-mind-mind-judge-diagnostic,meta-signal-orchestrate-session-lane-clear,mind-domain-all-repin,orchestrate-session-lane-storage,orchestrate-writer-ordering,signal-domain-schema-dotted-syntax-pilot,spirit-judge-hardening,pi-subagents-nested-roles-preference-training,pi-subagents-nicobailon-closeout,pi-subagents-nicobailon-optional-list-consistency}`. | Same classification; no cleanup during this pass. | Deployment/recovery evidence, a Lojix inspection aid, or an active diagnostic may be destroyed. | Same five-part evidence as C1, plus explicit confirmation that deployment/recovery evidence has a durable successor. | C1 method; O4 may reveal still-live Orchestrate records. | **Yes for deletion or conclusion; no for read-only classification.** |
| **C3. Reclaim only after a controlled Orchestrate witness.** Targets: the live Orchestrate Worktree registry and only the individually classified C1/C2 paths, using the owning lane's release/conclude mechanism. | Registry/worktree mutation, potentially a discard-branch push, then recoverable filesystem teardown. | A stale-looking record can still belong to a live lane; teardown can delete local changes or land unexpectedly. | O4 has passed; exact registry record maps to a classified path; owner disposition is recorded; conclusion is `Rejected` unless an approved reviewed landing exists; afterward the registry no longer shows the recycled record. | O4, P1–P5, C1/C2. | **Yes.** This is destructive/shared lifecycle work. |

## Ethos compatibility lane — branch A: temporary Schema compatibility allowed

This is the recommended branch. It continues Ethos without pretending the
prototype is already a component compiler.

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **E1A. Freeze the compatibility boundary.** Targets: `/git/github.com/LiGoldragon/{mind,orchestrate,message,router,spirit}/Cargo.toml` and `build.rs` where present; `/git/github.com/LiGoldragon/{signal-message,signal-orchestrate}` build scripts; compatibility repositories `/git/github.com/LiGoldragon/{schema,schema-rust,schema-language}`; and the policy/inventory targets in primary `protocols/repos-manifest.nota`. | Pin/documentation/inventory edits only; no broad package rename. | A broad source rewrite can fork generated artifacts, Cargo metadata, signal frames, or daemon runtime output while live recovery is in progress. | Exact known-good pins plus current generated-artifact freshness checks pass for Mind, Orchestrate, Messenger, Router, and Spirit. The primary manifest represents Ethos names and present Schema compatibility explicitly rather than naming absent repos. | First psyche decision; ownership/claim of each repository. | **No additional approval after the branch decision, except the manifest's formal membership ruling is itself a psyche-level naming decision.** |
| **E2A. Build the isolated Ethos→Nomos→Logos witness.** Targets: `/git/github.com/LiGoldragon/{protos,core-ethos,core-nomos,core-logos,ethos-engine,nomos-engine,logos-engine,protos-engine}`; prioritize `ethos-engine/tests/equivalence.rs`, engine `src/lib.rs` files, and a new isolated process witness in the owning test surface. | Library/daemon/test code and temporary local stores/sockets; build/test state only, no production service or shared Sema store. | The current engines use `signal-sema-storage`, ordinary Ethos ingress uses legacy parse-order names, and Nomos chooses a fixed fixture. A superficial test would validate the old topology rather than the ruled family. | At exact pins, run owning Nix gates and prove one fixture end-to-end: authority-bound identity; a selected typed Nomos package; persisted Logos; Rust projection; compilation/behavior; separate temporary local state per daemon; and a real translator authority. The test must fail if it falls back to the shared storage socket or the fixed package. | E1A; an explicit fixture and translator-boundary design; no production deployment. | **No additional approval for bounded prototype work after branch selection; yes before promoting the witness to a component or creating a permanent translator protocol.** |
| **E3A. Define the first component hand-off, then port one leaf only.** Targets: a new component-facing generator contract in the Ethos/Protos family; one selected leaf among `/git/github.com/LiGoldragon/{signal-message,signal-orchestrate}`; its consumer's generated-artifact and test surfaces. | New generator contract and one leaf migration, guarded by fallback compatibility. | A non-equivalent hand-off can change checked-in artifact freshness, Cargo schema-directory metadata, frame wire shape, or daemon runtime behavior. | The Ethos-generated leaf has equivalent behavior to the Schema-generated leaf, passes the consumer's full gates, and retains a declared Schema fallback for every other component. No global rename or wholesale dependency rewrite. | E2A; exact leaf selection; manifest ruling. | **Yes for selecting the first production-facing leaf and promotion; no for prototype-only contract exploration.** |

## Ethos strict lane — branch B: final Ethos shape required immediately

This branch is viable only as a deliberate program; it makes the current
Schema-dependent Mind/Messenger deployment changes contingent on a much larger
set of proofs. It must not be described as a quick migration.

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **E1B. Decide final terminology and authority before coding.** Targets: `protocols/repos-manifest.nota`; `/git/github.com/LiGoldragon/{core-ethos,ethos-engine,signal-ethos,tree-sitter-ethos,protos,protos-engine}`; and the named future translator repository/protocol. Decide schema's enduring role, manifest naming/alias rule, translator name/wire/storage/mint-bind/stale-entry policy, and the exact meaning of **Logics** separately. | Psyche design and inventory decisions; then documentation/manifest edits. | Premature rename/release automation can select absent repositories or hard-code a translator/identity policy later rejected by the psyche. | A single approved naming/authority record resolves the manifest-versus-checkout contradiction and names no unproven aliases; every selected repository exists at its declared path. | First psyche decision = strict branch; explicit Logics decision. | **Yes.** These are unresolved design/identity rules, not mechanical implementation details. |
| **E2B. Implement final compiler and daemon topology before component recovery.** Targets: `/git/github.com/LiGoldragon/{protos,core-ethos,core-nomos,core-logos,ethos-engine,nomos-engine,logos-engine,protos-engine}` and any newly approved translator target; then `/git/github.com/LiGoldragon/{schema,schema-rust,schema-language}` only through a reviewed replacement plan. | Cross-repository language/compiler/daemon/storage changes; migration tests. | Component artifact and wire incompatibility, incorrect name allocation, central-store leakage, or a migration that cannot restart/durably recover. | Replaces all required Schema generator surfaces: checked-in artifact/freshness workflow, Cargo schema-directory metadata, signal frames, and daemon/runtime Rust emission; ordinary Ethos ingress is authority-bound; each daemon has embedded local state; translator is real; Nomos selects/authors a durable package; full three-daemon witness passes. | E1B; per-repo worktree/claims; exact pins and Nix gates. | **Yes.** This is the final language architecture becoming operational. |
| **E3B. Migrate and deploy one complete component only after equivalence.** Targets: first approved component and signals (likely one of `/git/github.com/LiGoldragon/{mind,orchestrate,message,signal-message,signal-orchestrate}`), its CriomOS/CriomOS-home deployment module, and exact service/store migration fixture. | Component port, state migration, declarative activation, runtime writes. | Any loss of Mind/Messenger availability, incompatible peer frame, bad store migration, or unrecoverable rollback. | Full component acceptance under final Ethos generation, including service restart/durability; no compatibility compiler/adapters remain for that component; isolated copied-store launch and rollback rehearsal pass before production. | E2B; selected first component; Messenger contract if Messenger; Mind deployment plan if Mind. | **Yes.** It changes live component contracts and may migrate state. |

## Later visibility and tooling work

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **V1. Make the active operational truth observable from one authoritative context.** Targets: the selected CriomOS/CriomOS-home service module(s), their Nix checks, and a read-only status script/documentation surface; do not use the conflicting `systemctl` observations as a health verdict. | Configuration/check/documentation changes; later status reads. | A probe bound to the wrong manager/namespace can report false absence or false health and drive unsafe repair. | The probe identifies manager, user, host, unit, executable, socket, state path, and revision; it reports Mind, Orchestrate, Messenger, and the separately named Logics target consistently after activation. | O2/O3/O5 and authoritative-context decision. | **No for read-only tooling; yes if it changes deployment/service access boundaries.** |
| **V2. Add component-local work tracking only where it reduces real ambiguity.** Targets: `/git/github.com/LiGoldragon/{mind,orchestrate,message,logos-engine}` only if each owner accepts a local `.beads` database; otherwise retain primary bead links. Preserve `primary-akw` as the Lojix durable-migration authority and `primary-m8w` as the skills/subagent continuation context. | Tracker initialization/linking and documentation, not code behavior. | Duplicate or split issue truth can make recovery work disappear between trackers. | Each component has either a local tracker with a cross-reference to the primary parent or an explicit documented primary-only choice; no historical IDs are fabricated. | Owners from P1; tracking convention decision. | **No, unless the psyche chooses a broader tracker policy; do not mutate existing beads without the assigned owner.** |
| **V3. Establish a worktree retention/reclamation dashboard after O4.** Targets: `/git/github.com/LiGoldragon/orchestrate` registry query/presentation surfaces and primary's report/operating documentation; map physical path, repository, owner lane, parent change, status, disposition, and expiry/retention policy. | Observability code/docs; later controlled registry cleanup. | Treating a display as authority can hide a live claim or invite broad automated deletion. | Dashboard is read-only by default, derives path/owner from the live registry, flags unknown identity instead of auto-pruning, and links every cleanup action to C1/C2 evidence. | O4 and P1–P5. | **No for read-only visibility; yes for any automated reclamation policy.** |

## Stop conditions and non-goals

- Do not update stale Jujutsu working copies, delete a worktree, prune linked
  metadata, reconcile bookmarks, fetch/push, deploy, restart, or migrate a
  live store until the relevant row's gate and approval have been met.
- Do not equate **Logics** with Logos or Lojix.
- Do not claim that Messenger is reliable because its socket exists, that
  Orchestrate lifecycle is reliable because claim/observe works, or that Ethos
  replaces Schema because the prototype libraries compile.
- Do not make a broad package/repository rename a prerequisite for the bounded
  compatibility lane.

## First three actions after the psyche decision

1. Record the selected migration posture (recommended: bounded temporary
   Schema compatibility) and update the map's active branch only.
2. Obtain the canonical Messenger local-delivery ruling, then claim the exact
   Message/CriomOS-home paths for O1.
3. Name owners and disposition for P1–P4 while the Messenger contract work is
   prepared; no cleanup or stale-workspace refresh occurs in parallel.
