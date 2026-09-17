# Primary next: inventory decisions and preservation checks

Design POC, 2026-09-17. Flow `b399c1`. Read alongside
[the pre-v1 skeleton specification](PRIMARY-SKELETON.md), being authored by
flow `f60a1e` in the same shared workspace. That file was already present and
locked when this flow arrived. This companion owns no runtime configuration:
it records concrete disposition decisions, independent evidence, and the
conditions a later implementation must meet.

Nothing is deleted, relocated, rebased, or activated by this document.
`pre-v1` names the proposed repository generation; this documentation change
does not release version 1 or bump a package version.

## 1. The boundary being specified

The specification's tracked allowlist is nine files: `.gitignore`, `README.md`,
`ARCHITECTURE.md`, `SKILL_VARIABLES.md`, `AGENTS.md`, `CLAUDE.md`,
`bootstrap/manifest.dotos`, and the two generated bundled snapshots
`bootstrap/skills/workspace-primary/SKILL.md` and
`bootstrap/skills/provisioning-primary/SKILL.md`. The two skill names are design
choices, not existing authored skills. Their eventual sources belong under
`Curriculum skills`; primary contains generated release snapshots only.

`bootstrap/` is the only tracked subdirectory. Generated harness projections
and per-launch selections are local provisioning output. `.primary/` can hold
an ignored content cache and immutable launch receipts; it contains no second
checkout. The old generated `.agents/`, `.claude/`, `.codex/`, and `.pi/` trees
do not survive as tracked trees. A provisioner can recreate narrowly selected
projections there when a harness needs them. Hidden files remain outside every
discovery root, including roots contributed by parents, plugins, and user
configuration.

Retain all nine currently declared variable names, including **`Claude
transcript root`**: `Orchestrate release request`, `Curriculum skills`, `Claude
transcript root`, `NixBuilder`, `Reference skill collections`, `Repository
root`, `Standards`, `The system`, and `The user environment`. Values remain
setup-specific. The base specification's retention paragraph omitted `Claude
transcript root` when first inspected; the inventory decision here includes it.
New destination variables below receive real, verified endpoints during
implementation; this POC does not invent endpoint values or edit that file.

The `-primary` suffix identifies bundle origin. Visibility is separately
selected for each launch: agent-loadable, user-invoked, or hidden from the
skill interface. Reserve the suffix in Curriculum and reject collisions.
Hidden dependencies cannot silently become loadable through dependency
expansion. Every ordinary flow continues to start in the one shared primary
working directory; role selection must not overwrite another live flow's
catalog in a shared discovery directory.

## 2. Destination ownership

These names define destinations, not claims that their APIs are deployed.
Each named record collection has one shared owner. Adopt the specification's
proposed data repositories `primary-records` and `flow-data` as the first
migration destinations; Nexus service activation follows proven import and
retrieval contracts. These are new data destinations, not claims that the
existing `psyche` implementation accepts records. A data export lives outside primary and is shared by
flows; it is not copied into each launch or included in the new Git ancestry.

| Destination variable or owner | What it owns |
| --- | --- |
| `Psyche records` | `primary-records/psyche/`: the complete written-psyche corpus, including raw typed/dictated statements, distilled Vision and Intent, Notion, context, provenance, revisions, and transcript links. A future Psyche Nexus may serve it after its record contracts work. |
| `Flow records` | `flow-data/`: flow/thread identity, transcript locators, handoffs, session history, and new flow evidence. One shared data destination across layers; Flow's future record service consumes it. |
| `Workspace records` | `primary-records/workspace/`: repository inventory, historical reports/designs, and historical coordination records. Live work/release state ultimately belongs to the appropriate Nexus. |
| `Primary archive` | One preserved v0 history and the unique unpublished material collected from old checkouts. It is an archival data repository/export outside the new primary's refs and ancestry. It is searchable history, not live instructions. |
| Curriculum | Authored skill and role sources, manifests, skill selection, generated bundle releases, and the Nix-declared seed for the future Curriculum Nexus. |
| Component repositories / `Standards` | Executable tools and their tests belong to their shipping components; domain specifications belong to their existing standards owner. |
| Orchestrate | Live locks, registry, coordination database, and socket. Paths in primary can be projections only; this state is not a versioned repository payload. |

The v0 `ARCHITECTURE.md` calls the deployed Spirit store the raw-statement
authority; the current psyche skill describes files under `Vision/`,
`Intent/`, `flows/`, and `vision-raw/`. That disagreement is evidence of a
transition, not proof that either location contains everything. The migration
must reconcile both with the transcript and unpublished-worktree inventory.
The target variable `Psyche records` names the unified access surface without
asserting that today's Spirit deployment already fulfills it.

## 3. Keep / relocate / leave in v0

“Leave in v0” means excluded from the new working tree and its ancestry,
retained in `Primary archive` where appropriate. It never authorizes deletion
in this POC. Mixed directories have an explicit split below; embedded psyche
records follow the preservation rule in section 4 regardless of their path.

| Current path | Decision | Surviving content and destination |
| --- | --- | --- |
| `flows/` | Relocate | Raw `vision/` and `notion/` records to `Psyche records`; reports, witnesses, logs, summaries, and flow identity to `Flow records`. Flow-id claim files and live state move to Flow runtime storage. No per-flow directory is tracked in the skeleton. |
| `Vision/` | Relocate | Preserve every distilled statement, its review status, and links to raw sources in `Psyche records`. Do not turn an unreviewed summary into distilled vision during migration. |
| `vision-raw/` | Relocate | Preserve the legacy raw corpus verbatim in `Psyche records`, retaining its legacy paths as lookup aliases. Draining or distilling it does not erase source text. |
| `Intent/` | Relocate | Preserve explicit intent and its source/review metadata in `Psyche records`; retain the distinction from Vision and agent interpretation. |
| `psyche-archive/` | Relocate | Import preserved source records and archival provenance into `Psyche records`. Keep any original archive payload in `Primary archive` as recovery evidence. The directory name is not grounds to discard it. |
| `reports/` | Relocate | Preserve the historical corpus under `primary-records/workspace/reports/`. Accepted component decisions belong in their component architecture or standards; new flow evidence belongs to `Flow records`. Index embedded psyche quotations without presenting agent prose as psyche. |
| `agent-outputs/` | Leave in v0 after extraction | The complete original remains in `Primary archive`. Extract sole-copy psyche material to `Psyche records` and active deliveries to `Flow records`; generated diagnostics are not a bootstrap dependency. |
| `handoffs/` | Relocate | Flow succession, unresolved work, references, and unique records to `Flow records`; active work references enter `Workspace records`. Preserve original documents as source artifacts. |
| `sessions/` | Relocate | Session/transcript metadata and unique content to `Flow records`; local harness caches stay in harness runtime storage. No session clone is retained in primary. |
| `skills/` | Leave generated inventory in v0; relocate any unique input | Regenerate output inventories and deployment receipts from Curriculum. Any source without a Curriculum owner is imported into Curriculum before its old copy is retired. This is not a second skill-authoring root. |
| `tools/` | Relocate | Shipping implementations, tests, fixtures, and packaging to their component repositories. Operational usage belongs in Curriculum or the component README. Retired experiments remain in v0. No executable tool collection ships with the skeleton. |
| `orchestrate/` | Relocate | Runtime database/locks/socket to Orchestrate service storage; implementation and protocol docs to the Orchestrate repository; historical lock/coordination evidence to `Workspace records`. Retire stale file projections. |
| `awareness/` | Relocate | Current aspect/role behavior becomes Curriculum role-skill source after review. Historical prose remains in v0; psyche source material goes to `Psyche records`. Awareness is not indiscriminately injected from a shared parent entry file. |
| `protocols/` | Relocate | Repository manifest and attention map to `Workspace records`; standards to `Standards`; operational rules to Curriculum or their owning component. Retired-lane history goes to `Flow records`. Preserve source documents and identities when splitting. |
| `release-trains/` | Leave in v0 | Historical receipts remain in `Primary archive`. Any still-live release state is transferred to its release/work owner before retirement. No release-train directory ships in primary. |
| `verified/` | Leave in v0 | Preserve witnesses in `Primary archive` with scope, producer/version, and source artifact. A directory named “verified” does not make its claims current. |
| `.agents/` | Leave old generated tree in v0; regenerate selected output | Curriculum owns source and selection. Recreate only eligible local projections. No direct edits or retained full catalog. |
| `.claude/` | Leave old generated tree in v0; relocate unique local data | Regenerate eligible Claude skills/roles/configuration. Inventory worktrees and any unique records before retirement; those records follow their own destinations. Nested worktrees are absent from the skeleton. |
| `.codex/` | Leave old generated tree in v0; regenerate selected output | Curriculum/Flow owns selected Codex projections. Preserve any unique source or runtime record separately; generated agent/config trees are not the authoring home. |
| `.pi/` | Leave old generated tree in v0; regenerate only for an explicit Pi launch | Curriculum owns role output; local continuation/session data belongs to Flow/harness storage. Document Pi visibility without interpreting this POC as reversing its retirement direction. |

## 4. Preserve the psyche as one accessible corpus

The relevant September 17 source is outside this checkout:

`/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/visionAccessibleToAll.md`

It was read at that path before this disposition was written. The psyche's
typed words there include:

> This is why the vision, all of the primary, has to work together so that all the vision is accessible to everyone, so they can just wrap all the vision files and get the psyche. Astrak can load itself with all the vision raw, even if it can work on raw vision.

Keep the original bytes, including the recorded spelling, distinct from
editorial normalization. This design interprets the access requirement as
follows: every flow and layer can search, retrieve, and export the complete raw
corpus through `Psyche records`. Distillation, role selection, and skill
visibility do not gate that access. A host-wide read-only export can provide
file access if required by a harness, but belongs outside primary and is
shared, not cloned for each flow.

The preservation set is wider than current main. It includes `Vision/`,
`Intent/`, `vision-raw/`, `psyche-archive/`, every flow's raw vision/notion,
unique quotations in reports and handoffs, transcript-only typed/dictated
statements, and unpublished copies in all old checkouts. In particular,
`9993b5` is an explicit import source, not a presumed ancestor of main.
Report `flows/7b4d4c/reports/psyche-harnesses.md` demonstrates why transcripts
matter: its “Transcript-only” section cites statements that were never copied
into vision files. Preserve the transcript source and its message locator.

For each source artifact, the future import records its original repository,
revision when available, path, byte digest, flow/thread identity, message
locator, time, medium, and raw text. Unknown fields remain unknown. Separate
psyche words from agent-authored headings, context, classification, and
interpretation. Preserve revisions and explicit supersession links; a later
copy does not silently erase an earlier statement. Identical bytes can share
storage while retaining every source locator. Divergent versions remain
distinct until reconciled.

A migration is complete only after a source-to-destination manifest accounts
for every collected artifact, byte comparisons pass for verbatim payloads,
old locators resolve to new record IDs, and a fresh flow can query both raw
and distilled material without an originating flow's private workspace.
Queries must retrieve the `9993b5` source and a transcript-only example.
Take a restorable export and verify it independently of the live Nexus before
retiring an old copy. Primary can become small because record ownership moves;
records do not become disposable because primary v0 does.

## 5. Disk arithmetic and measured inventory

The inventory subflow inspected the shared filesystem without following
symlink targets. The first allocated-size sample and the subsequent tracked
regular-file sample are separate observations of a changing workspace.
The latter was taken at **2026-09-17 12:11:20 -06:00**, using `jj file list -r @`
and file metadata, at working revision
`fa9213480f328f2d95af5e7221a68e89773c8368`. It is not an immutable-tree or
compressed-object measurement. Counts exclude symlinks: the two report links
account for the difference between 708 regular files here and 710 tracked
entries in the specification's earlier inventory.

| Path | Tracked regular files / content bytes | Allocated bytes, including local contents |
| --- | ---: | ---: |
| `flows/` | 1,857 / 24,501,319 | 32,456,704 |
| `Vision/` | 25 / 53,688 | 147,456 |
| `vision-raw/` | 90 / 117,142 | 417,792 |
| `reports/` | 708 / 11,136,347 | 13,135,872 |
| `agent-outputs/` | 1,003 / 150,061,580 | 153,038,848 |
| `handoffs/` | 12 / 60,536 | 81,920 |
| `sessions/` | 8 / 54,386 | 90,112 |
| `skills/` | 3 / 1,977 | 16,384 |
| `tools/` | 25 / 125,274 | 176,128 before concurrent POC additions |
| `orchestrate/` | 4 / 42,621 | 53,248 |
| `Intent/` | 9 / 3,769 | 45,056 |
| `awareness/` | 13 / 24,648 | 65,536 |
| `protocols/` | 7 / 188,056 | 204,800 |
| `release-trains/` | 2 / 4,096 | 12,288 |
| `verified/` | 3 / 12,088 | 24,576 |
| `psyche-archive/` | 1 / 6,316 | 12,288 |
| `.agents/` | 49 / 101,810 | 450,560 |
| `.claude/` | 52 / 103,300 | 218,394,624 |
| `.codex/` | 9 / 3,472 | 45,056 |
| `.pi/` | 10 / 92,542 | 1,024,000 |

The later sample totals **3,992 tracked regular files / 203,745,354 bytes**,
including new work from other flows. A scoped allocated-size sum is
**2,282,078,208 bytes**, excluding external symlink targets and `private-repos/`.
The latter independently occupies 62,001,152 bytes, giving 2,344,079,360 bytes
when included (root directory metadata is excluded from these sums).

The first sample measured `.git/` at **542,199,808 allocated bytes**, `.jj/` at
**1,012,875,264**, and `.beads/` at **288,481,280**. `.claude/worktrees/flow-840e42`
accounts for about 218 MB of the Claude tree and contains untracked relay
artifacts; it must be separately accounted for before retirement. The Claude
projection excluding that worktree is only **462,848 allocated bytes**.
Large VCS state, diagnostic output, and a nested worktree dominate this
checkout; generated skill text does not.

The top-level follow-up also found the concurrent additions
`design/Flows/flowCliPoc.md`, `tools/flow-cli-poc/`, and this companion document.
They follow the existing decisions: design/evidence to records; tool code to
its component owner. The skeleton allowlist does not expand. The base
specification covers the other root items, including `index.js` (15,512,451
content bytes), `.beads/`, `CriomOS/`, `firstmate-bridge/`, and build remnants.
`spiritbackup.nota` must be examined as potential psyche evidence before it is
left behind. The `repos` symlink targets the separate repository collection;
its targets are not primary payload and are not copied during migration.

The same subflow observed `df -h /home`: **916G total, 548G used, 322G
available, 64% used**. The motivating **45 clones / approximately 11 GB** is
the historical figure supplied in the request, not a new census by this POC.
With decimal GB, `11,000 MB / 45 = 244.44 MB` per clone on average. If the
original figure meant GiB, `11 × 1,024 / 45 = 250.31 MiB` per clone. Neither
average describes this unusually large live checkout.

Adopt the specification's explicit size budgets: **128 KiB tracked content**,
**1 MiB allocated for a fresh unprovisioned clone including its VCS metadata**,
and **3 MiB allocated after the initial selected overlay**. Its nine-file
ceilings sum to 124 KiB, leaving 4 KiB inside the content budget. These are
acceptance limits, not measured candidate sizes: the nine files have not been
rendered and this POC creates no clone or worktree. A later implementation must
measure both Git and JJ forms on the deployment filesystem and report any
overrun rather than assert it met a hypothetical target.

| Budget scenario | Per clone | 45 copies, comparison only |
| --- | ---: | ---: |
| Tracked content ceiling | 128 KiB | 5.625 MiB |
| Skeleton plus fresh VCS | 1 MiB | 45 MiB |
| Initially provisioned skeleton | 3 MiB | 135 MiB |

Against 11 GiB, the provisioned comparison saves
`1 - 135 / 11,264 = 98.80%` of duplicated clone storage **if the budget is met**.
The operating target remains one shared checkout. Its cost is one skeleton,
one shared content cache, and the selected per-launch projections. Shared
records, preserved history, and service data remain separately charged disk
costs. A history-preserving commit deleting directories would not remove their
Git/JJ objects; a later new-root operation must also avoid carrying v0 refs or
objects into the fresh clone. This POC reclaimed no space.

## 6. Harness review and implementation acceptance

The harness review subflow inspected local Codex and Pi implementations and
primary upstream documentation. These are source/documentation witnesses,
not four live model-session tests. Preserve version boundaries when applying
them to the specification's separately inspected upstream revisions.

In particular, this review **could not reproduce** the specification's Codex
source witness at `3d3ae4965ab370217e871b3a7f0d15589557ee4b`: the cited
`core-skills/src/config_rules.rs` was unavailable through the checked upstream
routes, and the fetched app-server README did not establish the extra-roots
API. The local Pi witness also differs from the specification's cited
`781139411232411196de9fcc9f8823229c9ae084`. These are unresolved version checks,
not evidence that the draft's author fabricated its observations or that a
mechanism exists in every release. The exact deployed revision must be
established before implementing its adapter. Current official
[Codex local-skill documentation](https://learn.chatgpt.com/docs/build-skills)
documents `.agents/skills` discovery; the additional local mechanisms below
must not be presented as the documented current contract.

| Harness | Required visibility mechanism and explicit limit |
| --- | --- |
| Claude Code | Put hidden files outside all enabled skill roots. A per-launch `--plugin-dir` is additive; inspect inherited roots, installed plugins, and synced skills too. `disable-model-invocation: true` remains user-invoked; `user-invocable: false` alone remains model-loadable. Documented `skillOverrides: off` disables both invocation routes for covered skills, but does **not** cover plugin skills; disable/remove the plugin or omit that skill from its selected projection. |
| Codex | Omit hidden content from every discovery root. The inspected local source includes project `.codex/skills` as well as `.agents/skills`, user/system/admin/plugin roots, and app-server extra roots. Disabled skill rules come from user/session-flag configuration, not project `.codex/config.toml`; `allow_implicit_invocation: false` remains explicitly invocable. The local app-server has process-scoped `skills/extraRoots/set`, described below. No per-thread isolation follows merely from that API. |
| Pi | Use `--no-skills` and explicit `--skill` paths for the selected projection. Extensions can add skill paths: use an audited extension set or `--no-extensions`. `disable-model-invocation` leaves `/skill:name` usable. Parent context is a separate surface; the inspected distribution offers `--no-context-files` when those files must be excluded. Pi documentation here does not reactivate Pi as a default harness. |
| DeepSeek (`dsh`) | Register only selected skills in the intended preset/agent scope and keep hidden files out of global roots. Both invocation flags false still allows trusted `ctx.skills.get()` access. The ordinary model skill tool enforces its model-invocation flag, but a plugin exposing broad trusted lookup can undo the selection. Without an audited scoped adapter, a global `customSkillDirs` union cannot enforce per-flow isolation. |

Claude's limits are documented in its [skills reference](https://code.claude.com/docs/en/skills)
and [CLI reference](https://code.claude.com/docs/en/cli-reference). The DeepSeek
review used the unpinned upstream [skills subsystem documentation](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
as fetched on 2026-09-17; it is not an installed-runtime witness.

At the local Codex revision listed below, `skills/extraRoots/set` replaces the
additional standalone roots for the **whole app-server process**, loses them
on exit, and leaves the ordinary roots in force. A Flow adapter can provision
a dedicated process with the selected roots, then suppress unwanted inherited
skills through supported user/session rules. Multiple threads sharing that
process cannot obtain different extra-root lists through this API alone.
Use per-process isolation or implement and prove per-flow filtering if the
chosen build exposes that API. This is an adapter route at the witnessed local
revision, not a prescription for the unverified pinned or installed build.
Until an additive selection route is proved for that build, Codex uses a
common-only catalog or reports a role-specific launch as unsupported.

All four mechanisms govern skill registration and invocation. Ordinary
filesystem reads can still see the bytes; the design does not claim a secrecy
boundary. Conversely, hiding only a menu label is insufficient: the
implementation must also reject explicit hidden names through the skill
interface. An unsupported visibility requirement must be reported before
launch, not treated as enforced by prose.

The named Curriculum documentation sections in the base specification remain
the implementation work list. Add these particular details to **Skill
discovery and workspace overlays / Concurrent flow selections** in
`codex-harness.md`; the plugin exception to **Skill visibility** in
`claude-harness.md`; extension-added roots to **Skill discovery and explicit
paths** in `pi-harness.md`; and trusted registry access to **Skill visibility**
in `deepseek-harness.md`. No authored skills or generated harness trees were
edited by this flow.

Before the later history cut, the implementation must demonstrate:

1. The selected source inventory maps to the external data destinations and
   the `9993b5` and transcript-only records read back with original bytes and
   context. No unexplained unique source is retired.
2. Each supported harness lists/loads an ordinary skill, handles user-only
   skills as documented, and rejects hidden names while their files remain
   present. Include plugin, extension, parent-root, cache/reload, and subagent
   cases; source inspection alone does not establish live behavior.
3. Two concurrent flows in the same primary cwd retain different selected
   catalogs without swapping shared directories or shared process settings.
4. Fresh Git/JJ and initially provisioned storage are measured against the
   budgets separately from records, archive, caches, and live service state.

The POC validation is the documentary cross-check, arithmetic, source review,
and inventory witness. It does not claim those future runtime gates passed.

## Sources

- `CLAUDE.md`, `AGENTS.md`, `ARCHITECTURE.md`, `NON_MANAGEMENT_AGENTS.md`, and
  `SKILL_VARIABLES.md`, read in the shared primary workspace on 2026-09-17.
- `Vision/highLevelView.md`; `flows/1030529c/vision/workspace20.md`;
  `flows/7b4d4c/reports/psyche-harnesses.md`. The latter is an agent collection
  of source claims, not a witness of harness implementation.
- Flow `9993b5`'s `primarySkeleton.md`, `primaryNext.md`, `worktreeHygiene.md`,
  `workspaceProvisioning.md`, `curriculumNexus.md`, `sharedWorkspace.md`,
  `oneSharedPrimary.md`, `sprawlFix.md`, `transcriptOverFiles.md`,
  `visionAccessibleToAll.md`, `noMoreBranches.md`, `launchOnMain.md`, and
  `orchestrateCommitBinding.md`, read from the unpublished worktree path above.
- `PRIMARY-SKELETON.md`, flow `f60a1e`'s concurrent draft, initially inspected
  at 337 lines. Its nine-file skeleton and origin/visibility separation are
  adopted here as design choices; external harness claims are checked below.
- `flows/e996e8/vision/flows.md`, read for the dedicated flow-data direction;
  `/git/github.com/LiGoldragon/psyche/ARCHITECTURE.md`, read for its explicitly
  undefined record/runtime contracts. Data destinations are proposed, not
  deployment claims.
- Inventory subflow `/root/inventory`, 2026-09-17: `find -P`, `du -s -B1`,
  `du --apparent-size`, `df -h`, and the later `jj file list`/file-metadata
  sample. Directory recommendations above are this flow's design; measured
  counts and sizes are that subflow's direct observations.
- Harness subflow `/root/harness_visibility`: local
  `/git/github.com/openai/codex` revision
  `ff29a44391deccde0aba0f8390337d7f3c319ea4` (commit dated 2026-08-23),
  `codex-rs/ext/skills/src/host_roots.rs:28`,
  `codex-rs/config/src/skills_config.rs:90`,
  `codex-rs/skills/src/selection.rs:44`, and
  `codex-rs/app-server/README.md:1882`. This flow additionally read the
  app-server README's skill invocation and extra-roots section directly.
- The same harness subflow: local `/git/github.com/badlogic/pi-mono` revision
  `3da591ab74ab9ab407e72ed882600b2c851fae21` (commit dated 2026-07-17),
  `packages/coding-agent/src/core/resource-loader.ts:400`,
  `packages/coding-agent/src/core/skills.ts:327`, and
  `packages/coding-agent/docs/skills.md:24`.
