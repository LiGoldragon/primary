# Recovery map — 2026-07-28

## Purpose and evidence boundary

This is an execution map, not an assertion that any repair has been made. It
synthesizes the read-only estate inventory, core-operations audit, and
Schema-to-Ethos audit dated 2026-07-28, plus the current primary beads
`primary-akw` and `primary-m8w`. No command in preparing this map mutated a
repository, service, store, bead, remote, or worktree.

The evidence establishes three things:

1. Orchestrate's live claim/transport boundary works, but its current
   observations reconcile state and its worktree lifecycle has historical
   failures and a dirty/stale registry; neither is a safe read-only or
   state-only cleanup boundary.
2. The deployed Messenger package is byte-identical to `message` `main` at
   `1c47a20e` and implements durable, direct, Router-free local delivery.
   Router is absent, but is not the local-delivery blocker. Mind is not
   deployed. **Logics** has no established referent and remains an unresolved
   term; Logos and Lojix are distinct candidates, not aliases.
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
2. Run an isolated witness of the exact deployed Messenger package and correct
   only its stale documentation/Nix-check guidance; do not repair Router or
   choose a new Messenger contract.
3. Obtain a psyche-selected first Mind workflow and observable success
   criterion before designing or deploying Mind on the selected compatibility
   branch.
4. Resolve the exact referent of **Logics**. If it is Lojix, continue the
   already-recorded durable v1-to-v2 migration; if it is Logos or another
   component, create a separate, named deployment/witness lane.
5. Repair Orchestrate to provide pure reads, state-only worktree transitions,
   and durable lifecycle receipts. Only then may a separately authorized
   disposable state-only witness be considered; do not exercise the current
   worktree conclusion or use it for cleanup.
6. Continue Ethos using the selected branch below. Do not let an incomplete
   language migration silently change the live component compiler.

## Immediate operational repair

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **O1. Witness the deployed Router-free Messenger and correct stale guidance.** Targets: the verified deployed `message` `main` source at `1c47a20e`, `/git/github.com/LiGoldragon/message/{AGENTS.md,ARCHITECTURE.md,flake.nix}`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/message.nix`, and the owning isolated test/Nix-check surface. The direct durable delivery path is established: `Submit` persists ledger/inbox state, then `DeliveryRunner` delivers to a bound endpoint or retains a durable outbox entry. The Router field is dormant. | Isolated temporary-root test stores/sockets plus documentation and Nix-check hygiene; no Router deployment, Router configuration repair, Messenger routing change, pin change, or live submission. | A fixture can accidentally use live state, or guidance can continue to name deleted Router-forward tests and misstate the dormant field as a delivery dependency. | Against the exact deployed package/source in an isolated temporary root: bind identities, submit, verify direct delivery or durable outbox/retry, restart survival, and a typed recipient-failure result while Router is absent. Documentation and the Nix check must describe the Router field as dormant and the current direct path; no result may be presented as a live delivery witness. | Exact package/source selection and an isolated harness. No migration-posture or Router decision is required because no contract is changed. | **No for isolated testing and documentation/check hygiene. Yes for any live synthetic submission, activation, or persistent-store write.** |
| **O2. Select Mind's first workflow and success criterion before deployment.** Targets are a direct psyche answer, then only the Mind/CriomOS-home deployment targets justified by that answer, including any proposed `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/mind.nix`, its import/check/pin surfaces, and `/git/github.com/LiGoldragon/mind` configuration and test surfaces. The required selection is one first human workflow—durable work memory, accepted-knowledge admission, or queryable source-backed architecture knowledge—and the observable result that makes it useful. | Psyche product decision first; only then a narrow deployment design, source/configuration changes, evaluation, and any approved activation. | A fixture-backed daemon or incomplete policy surface can be deployed as a product without an intended use, acceptance criterion, or authority boundary. | The psyche names one workflow and a measurable successful outcome. A subsequent design must show that its deployment boundary, judge/configuration, data scope, and tests serve that outcome before any service activation or durable Mind-state write. | First-workflow/success answer; selected migration posture if the chosen design changes generated contracts; authoritative manager context. Messenger delivery is not a general prerequisite. | **Yes.** The inspected record contains no direct selection of the first deployed workflow or success criterion. |
| **O3. Repair Orchestrate before any lifecycle witness or cleanup conclusion.** Targets: `/git/github.com/LiGoldragon/{signal-orchestrate,meta-signal-orchestrate,orchestrate}`, `/git/github.com/LiGoldragon/CriomOS-home`, and the canonical skills source that generates the write-role instructions. Replace reconciling observations and filesystem-based request/conclude/reaping behavior with pure reads, state-only worktree reservation/activation/suspect/conclusion transitions, and append-only lifecycle receipts. | Protocol, CLI, daemon/store, deployment, test, and generated-instruction changes; a later separately authorized disposable fixture witness only after the repair is deployed. | Current `Observe` can reconcile state; current `ConcludeWorktree Rejected` can create/push a discard bookmark, forget/remove a workspace, and delete local bookmarks. A mixed repair can still mutate a read or let the daemon inspect the filesystem. | Every observation leaves byte-identical fixture state; receipts persist every accepted/refused transition; daemon PATH and tests prove no `jj`/`git` filesystem action; request/activation/conclusion are typed state-only transitions. Only after those gates and explicit authorization may a disposable reserve → claim → activate → conclude witness run, with no checkout, bookmark, remote, or directory effect. | Selected migration posture for any protocol generation; explicit psyche approval of the public CLI/protocol/deployment repair and claim-gate fallback. The current Messenger witness is not a dependency. | **Yes.** This materially changes deployed coordination and removes unsafe lifecycle side effects. |
| **O4. Resolve the term `Logics` before assigning its repair.** Targets are a psyche decision record and then exactly one named candidate: `/git/github.com/LiGoldragon/lojix` plus `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix`, or `/git/github.com/LiGoldragon/{core-logos,logos-runtime,logos-engine}`, or the separately named system supplied by the psyche. | Decision; only thereafter code/deployment work. | Treating Logos as Lojix can corrupt the scope: Lojix has a live v1-to-v2 store mismatch; Logos has no host deployment. | The target name appears verbatim in the approved task/bead; the follow-up witness matches that target (served Lojix request after migration, or a narrow Logos witness). | Psyche naming; if Lojix, `primary-akw`. | **Yes.** Exact-name evidence is absent; the boot contract forbids silently equating terms. |
| **O5. Complete Lojix live gates only if O4 names Lojix.** Targets: the existing live `/var/lib/lojix/lojix.sema` through its owner protocol and `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix` at immutable CriomOS `475bf5c27efa843f97ad58cc99e611d519d0f40f`. The static migration suite and the exact immutable activation closure already pass; they are not work still to repeat. | Authorized read-only live-store precondition witness; then declarative activation, pre-start migration, service restart, and live query/history observations. | A non-schema-1 or unreadable live store, partial migration, restart loop, or lost/unreadable deployment history. | Before activation, establish the live schema/canonical-store precondition without exposing payloads. Then activate the validated generation and witness pre-start result, daemon sockets, an ordinary query, and readable deployment history. | O4 = Lojix; `primary-akw`; explicit live-store and activation authority. | **Yes.** The remaining gates access or change live Lojix state; a passing static migration and closure do not authorize them. |

## Preservation and ownership decisions

No preservation item below is a cleanup candidate. The inventory's state is
point-in-time only and did not establish authorship, retention periods, or
supersession.

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **P1. Assign an owner and disposition to dirty canonical work.** Targets: `/git/github.com/LiGoldragon/{CriomOS-test-cluster,TheBookOfSol,meta-signal-mind,meta-signal-persona,schema}`; preserved items include `CriomOS-test-cluster/lib/{nestedReachability.nix,nestedSpike.nix}`, `meta-signal-mind/src/schema/lib.rs`, `meta-signal-persona/src/schema/lib.rs`, and `schema/schemas/#spirit-min.schema#`. | No content mutation until ownership is recorded; later recover, commit, discard, or archive is a separate mutation. | Tests/fixtures, personal/editorial content, generated contracts, or an active editor backup can be lost. | Named owner acknowledges the exact working copy and chooses retain/land/recover/discard; for the backup, identify the editor/session before any removal. Record current `jj status` and a content-safe disposition proof before mutation. | Owner discovery; worktree claim by the eventual editor. | **Yes.** Inventory explicitly reserves these decisions; ownership cannot be inferred. |
| **P2. Decide repair versus retirement for stale Lojix checkouts.** Targets: `/git/github.com/LiGoldragon/{meta-signal-lojix,signal-lojix}` with stale Jujutsu operations `4e1291c8d92b` and `6fa1f26bd8f8`. | Potential Jujutsu working-copy update followed by inspection; later recovery/retirement. | Updating can materialize hidden changes or overwrite the understanding of a stale working copy; retirement could lose unincorporated work. | Before an update, capture metadata and owner decision. After an authorized refresh, inspect status/diff and show either an incorporated successor or a reviewable preservation/export. | P1-style owner assignment; O4 if the work relates to selected Lojix work. | **Yes.** The only disambiguating inspection mutates state. |
| **P3. Preserve the three dirty dotted-syntax pilots as independent until compared.** Targets: `/git/github.com/LiGoldragon/{meta-signal-spirit-schema-dotted-syntax-pilot,signal-spirit-schema-dotted-syntax-pilot,spirit-schema-dotted-syntax-pilot}/ARCHITECTURE.md`, all on bookmark `schema-vision-redesign-arch-docs`. | Read-only content comparison first; later merge/land/discard only after review. | Deduplicating by name can drop materially distinct documentation corrections. | A side-by-side diff identifies identical versus distinct edits, a named owner accepts the chosen canonical wording, and each workspace's disposition is recorded. | P1 owner record; current migration-posture decision informs terminology but does not replace content review. | **Yes for disposition.** Cleanliness/name similarity is not authority to discard. |
| **P4. ~~Resolve the orphan-like primary-linked worktree.~~ Resolved.** The worktree was at `/git/github.com/LiGoldragon/synchronizer-release-train-p0-p2` (not the earlier-reported `/home/li/primary/synchronizer-release-train-p0-p2`). It carried branch `release-train-p0-p2`, which is fully merged into `main` (142 commits behind). The worktree has been removed via `git worktree remove`. | Completed. | N/A | Verified: all commits are ancestors of `main`; `git worktree list` confirms removal. | None remaining. | **Done.** |
| **P5. Defer bookmark/remote reconciliation.** Targets: the twelve non-converged `main@*` repository states listed in `estate-inventory-2026-07-28.md`, plus deleted bookmark markers in `CriomOS-home`, `core-ethos`, `core-logos`, `core-nomos`, `signal-domain`, `signal-message`, `signal-orchestrate`, `signal-sema-storage`, `signal-spirit-judge`, `structural-codec`, `textual-rust`, and `version-projection`. | Fetch/review then possible bookmark changes and push. | Pushing a deleted bookmark may permanently delete remote history; a stale local tracking view can cause the wrong reconciliation. | Per repository: fresh authorized remote state, chosen source-of-truth bookmark, review of deletion impact, and explicit push result. | P1–P4 dispositions; network/VCS authority. | **Yes.** This changes shared history/remotes and the inventory explicitly defers it. |

## Workspace cleanup status

Classification is complete for **47 physical extra workspace-like directories**:
**7 preserve**, **17 require an owner decision**, and **23 are conditionally
cleanup-eligible after approval**. The tally concerns physical extras, not the
166 canonical repository roots or a mixed registry inventory.

An earlier **"215 surfaces / 171 preserve"** figure mixed unlike units — 166
canonical repository roots, 42 detached Jujutsu workspaces, 6 registry
records, and 1 Git-linked orphan — and is withdrawn as a workspace or
physical-directory summary. It was self-corrected during the same Codex
session that produced this inventory; see the "Withdrawn mixed tally"
subsection of `workspace-cleanup-batch-plan-2026-07-28.md` for the retired
arithmetic.

**No cleanup is authorized.** The 23 conditional paths are not deletion or
conclusion targets today. Current `ConcludeWorktree Rejected` is unsafe: it can
push a discard bookmark, forget/remove the workspace, and delete local
bookmarks; current observations are not a pure historical lens.

Any future cleanup needs all of: O3's deployed pure-read/state-only repair and
durable receipts; a repeated path-specific material/ancestry and owner proof;
an explicit approval naming the exact path or batch; and a separately approved
recoverable executor action. The daemon must not perform filesystem, bookmark,
or remote effects.

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
| **E3B. Migrate and deploy one complete component only after equivalence.** Targets: first approved component and signals (likely one of `/git/github.com/LiGoldragon/{mind,orchestrate,message,signal-message,signal-orchestrate}`), its CriomOS/CriomOS-home deployment module, and exact service/store migration fixture. | Component port, state migration, declarative activation, runtime writes. | Any loss of Mind/Messenger availability, incompatible peer frame, bad store migration, or unrecoverable rollback. | Full component acceptance under final Ethos generation, including service restart/durability; no compatibility compiler/adapters remain for that component; isolated copied-store launch and rollback rehearsal pass before production. | E2B; selected first component; O1's exact deployed Messenger witness/guidance if Messenger; O2's workflow-selected Mind deployment plan if Mind. | **Yes.** It changes live component contracts and may migrate state. |

## Later visibility and tooling work

| Action and exact targets | Mutation class | What could break | Proof / acceptance gate | Dependencies | Psyche approval under the boot contract |
| --- | --- | --- | --- | --- | --- |
| **V1. Make the active operational truth observable from one authoritative context.** Targets: the selected CriomOS/CriomOS-home service module(s), their Nix checks, and a read-only status script/documentation surface; do not use the conflicting `systemctl` observations as a health verdict. | Configuration/check/documentation changes; later status reads. | A probe bound to the wrong manager/namespace can report false absence or false health and drive unsafe repair. | The probe identifies manager, user, host, unit, executable, socket, state path, and revision; it reports Mind, Orchestrate, Messenger, and the separately named Logics target consistently after activation. | O1; O2 after its workflow/success decision and any approved deployment; O4; authoritative-context decision. | **No for read-only tooling; yes if it changes deployment/service access boundaries.** |
| **V2. Add component-local work tracking only where it reduces real ambiguity.** Targets: `/git/github.com/LiGoldragon/{mind,orchestrate,message,logos-engine}` only if each owner accepts a local `.beads` database; otherwise retain primary bead links. Preserve `primary-akw` as the Lojix durable-migration authority and `primary-m8w` as the skills/subagent continuation context. | Tracker initialization/linking and documentation, not code behavior. | Duplicate or split issue truth can make recovery work disappear between trackers. | Each component has either a local tracker with a cross-reference to the primary parent or an explicit documented primary-only choice; no historical IDs are fabricated. | Owners from P1; tracking convention decision. | **No, unless the psyche chooses a broader tracker policy; do not mutate existing beads without the assigned owner.** |
| **V3. Establish a worktree retention/reclamation dashboard after O3.** Targets: `/git/github.com/LiGoldragon/orchestrate` registry query/presentation surfaces and primary's report/operating documentation; map physical path, repository, owner lane, parent change, status, disposition, and expiry/retention policy. | Observability code/docs; later controlled registry cleanup. | Treating a display as authority can hide a live claim or invite broad automated deletion. | Dashboard is read-only by default, derives path/owner from the live registry, flags unknown identity instead of auto-pruning, and links every future cleanup action to its completed classification, owner proof, and durable lifecycle receipt. | O3 and P1–P5. | **No for read-only visibility; yes for any automated reclamation policy.** |

## Stop conditions and non-goals

- Do not update stale Jujutsu working copies, delete a worktree, prune linked
  metadata, reconcile bookmarks, fetch/push, deploy, restart, or migrate a
  live store until the relevant row's gate and approval have been met.
- Do not use current `Observe` as a pure audit lens or run current
  `RequestWorktree`/`ConcludeWorktree` as a lifecycle or cleanup witness;
  those operations remain unsafe until O3's state-only/pure-read repair is
  deployed and proved.
- Do not equate **Logics** with Logos or Lojix.
- Do not claim that Messenger is reliable because its socket exists, that
  Orchestrate lifecycle is reliable because claim/observe works, or that Ethos
  replaces Schema because the prototype libraries compile.
- Do not make a broad package/repository rename a prerequisite for the bounded
  compatibility lane.

## First three actions after the psyche decision

1. Record the selected migration posture (recommended: bounded temporary
   Schema compatibility) and update the map's active branch only.
2. Obtain the first Mind workflow and observable success criterion; do not
   treat a deployment module or fixture judge as that decision.
3. Run O1's isolated exact-package Messenger witness and documentation/Nix-check
   hygiene. Do not run an Orchestrate lifecycle witness, conclusion, or cleanup.
