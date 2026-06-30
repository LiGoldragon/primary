# Naming Discovery for primary-ascl.1

Task: discover whether prior approved replacement names exist for bad skill/module names `jj`, `beads`, `beauty`, and `component-triad`, without editing source files.

Scope used: local project instructions, tracker descriptions, public/open agent-output history, the `repos/skills-primary-ascl-doctrine` source worktree as read-only evidence, and read-only Spirit public text searches. I did not intentionally inspect private repositories; one overbroad exploratory `rg` command included `private-repos` and its output was discarded for this report. No private content is quoted or used below.

## Commands and files consulted

- `sed -n '1,220p' AGENTS.md`
- `bd show primary-ascl primary-ascl.1 primary-ascl.2 --long`
- `rg --no-ignore ...` over `agent-outputs/`, `reports/`, `repos/skills`, `repos/skills-primary-ascl-doctrine`, `.pi`, `.codex`, `.claude`, excluding private scopes except the discarded overbroad command noted above
- `spirit "(PublicTextSearch jj)"`, `spirit "(PublicTextSearch beads)"`, `spirit "(PublicTextSearch beauty)"`, `spirit "(PublicTextSearch component-triad)"`, plus broader public searches for `skill`, `naming`, `names`, `role-packets`, and `agents`
- `agent-outputs/orchestration-weave/naming-orchestration-spirit-bundle-retry.md`
- `agent-outputs/SkillDoctrineV2/SkillEditor-CorpusTriage.md`
- `agent-outputs/RoleSkillReview/SkillEditor-CorpusTrimProposal.md`
- `repos/skills-primary-ascl-doctrine/agent-outputs/V2RoleDoctrineBundles/SkillEditor-Handoff.md`
- `repos/skills-primary-ascl-doctrine/manifests/active-outputs.nota`
- `repos/skills-primary-ascl-doctrine/modules/code-implementation-core/full.md`
- `repos/skills-primary-ascl-doctrine/modules/rust-core/full.md`
- `repos/skills-primary-ascl-doctrine/modules/repo-operation-core/full.md`

## Observed facts

- Tracker authority says `primary-ascl.1` must find prior approved replacement proposals for `jj`, `beads`, `beauty`, and `component-triad`, and if any are missing, pause renaming for psyche approval. Evidence: `bd show primary-ascl.1 --long`; same wording appears in `agent-outputs/orchestration-weave/naming-orchestration-spirit-bundle-retry.md:23-29`.
- `primary-ascl.2` is explicitly blocked until approved replacements are found or psyche approves missing choices. Evidence: `bd show primary-ascl.2 --long`; same blocker is in `agent-outputs/orchestration-weave/naming-orchestration-spirit-bundle-retry.md:76-81`.
- Public Spirit text searches for the four exact bad names returned no matching record, so I found no direct Spirit approval for exact replacements. Evidence: each of `spirit "(PublicTextSearch jj)"`, `spirit "(PublicTextSearch beads)"`, `spirit "(PublicTextSearch beauty)"`, and `spirit "(PublicTextSearch component-triad)"` returned `(Error [no matching record])`.
- `agent-outputs/SkillDoctrineV2/SkillEditor-CorpusTriage.md:59-62` says `beauty` and `jj` are to be kept/preserved as load-bearing doctrine, not renamed: `beauty` is listed among compact core craft doctrine; `jj` is listed as necessary safety/verification/mechanics doctrine.
- `agent-outputs/SkillDoctrineV2/SkillEditor-CorpusTriage.md:74` proposes `beads` plus `bead-weaver` merge to `work-tracking` or a lead-only bundle, but the target is an either/or proposal, not an exact approval.
- `agent-outputs/SkillDoctrineV2/SkillEditor-CorpusTriage.md:84` says `component-triad` should keep unique doctrine but split or compress several subtopics. Lines `122`, `151`, and `167-168` offer multiple shapes: `component-core` plus optional `runtime-triad` detail; `contract-component`; or separate component packaging, runtime triad, and signal-contract packets.
- `agent-outputs/RoleSkillReview/SkillEditor-CorpusTrimProposal.md:219-225` says `component-triad` is a candidate to split into `component-triad` plus `runtime-triad`, and explicitly says to raise the split to the psyche before acting. Lines `401-419` again mark the `component-triad` split as requiring a psyche decision if taken.
- `repos/skills-primary-ascl-doctrine/agent-outputs/V2RoleDoctrineBundles/SkillEditor-Handoff.md:26-35` records implemented role-composition modules including `code-implementation-core`, `rust-core`, and `repo-operation-core`; line `35` calls `repo-operation-core` concise `jj`/repo-operation doctrine.
- `repos/skills-primary-ascl-doctrine/modules/repo-operation-core/full.md:15-20` carries the `jj` version-control rule inside a broader repo operation module; lines `49-62` carry bead closeout/work-tracking rules inside the same broader module.
- `repos/skills-primary-ascl-doctrine/modules/code-implementation-core/full.md:22-24` carries the `beauty` rule as a correctness gate inside implementation core.
- `repos/skills-primary-ascl-doctrine/modules/rust-core/full.md:27-29` carries a compressed component-triad rule: daemon, thin CLI, and signal-* contract stay distinct.
- Despite those composite modules, `repos/skills-primary-ascl-doctrine/manifests/active-outputs.nota:44` and `:47` still emit first-class skills named `jj` and `beads`; line `21` still emits `beauty`; line `8` still emits `component-triad`. This means the composite modules are role-packet condensation evidence, not completed/approved active-skill renames.

## Mapping discovery

| Old name | Proposed new name found | Evidence and status |
| --- | --- | --- |
| `jj` | No approved exact rename found. Candidate evidence only: `repo-operation-core` for role-packet doctrine; source description also spells out `Jujutsu version-control discipline`. | `SkillEditor-CorpusTriage.md:62` and `:93` say keep/preserve `jj` content. `V2RoleDoctrineBundles/SkillEditor-Handoff.md:35` says `repo-operation-core` is concise `jj`/repo-operation doctrine, and `repo-operation-core/full.md:15-20` carries the rule. This is ambiguous: it supports role composition, not an exact first-class skill/module rename. |
| `beads` | No approved exact rename found. Candidate evidence: `work-tracking` or lead-only bundle; current role composition uses `bead-weaver` and/or `repo-operation-core`. | `SkillEditor-CorpusTriage.md:74` proposes `work-tracking` or lead-only bundle; `:103` says keep temporarily until Persona/mind tracking is available; `:161-162` asks whether BEADS remains required or should be archived. The target is explicitly undecided. |
| `beauty` | No replacement proposal found. Candidate evidence only: content is folded into `code-implementation-core`. | `SkillEditor-CorpusTriage.md:59` says keep `beauty` as distinct compact craft doctrine. `code-implementation-core/full.md:22-24` embeds the beauty rule, but no source found proposes a new first-class name for `beauty`. |
| `component-triad` | No approved exact rename found. Candidate names/shapes include `runtime-triad`, `component-core`, `contract-component`, and separate component packaging/runtime triad/signal-contract packets. | `SkillEditor-CorpusTriage.md:122` names `component-core` plus optional `runtime-triad`; `:151` names `contract-component`; `:167-168` asks whether to split into component packaging, runtime triad, and signal-contract packets. `SkillEditor-CorpusTrimProposal.md:219-225` proposes split into `component-triad` plus `runtime-triad` but says to raise it to the psyche first; `:418-419` marks this as psyche-decision if taken. |

## Interpretation

The local history contains several useful proposals and an implemented role-composition direction, but I did not find exact approved replacement mappings for any of the four active first-class names. The strongest evidence is:

- `jj` and `beads` content can live under `repo-operation-core` in role packets, but that does not prove the active skill/module output should be renamed to `repo-operation-core`.
- `beads` has a plausible proposed replacement `work-tracking`, but the same sentence says `or lead-only bundle`, and other surfaces say the BEADS substrate decision itself remains open.
- `beauty` appears intentionally retained as a distinct doctrine in prior triage; only its rule is embedded in implementation-core role composition.
- `component-triad` has multiple competing decomposition proposals and explicit prior text saying psyche approval is required before a split.

## Missing or ambiguous names needing psyche approval

All four names need approval before implementation if `primary-ascl.2` is meant to rename active source/generated skill/module surfaces:

1. `jj`: approve exact target, for example `repo-operation-core`, `jujutsu`, or another full-name skill/module id.
2. `beads`: approve exact target, for example `work-tracking`, `repo-operation-core`, `bead-weaver`, or a Mind/memory/weave vocabulary name.
3. `beauty`: approve whether to keep `beauty` or rename to a new exact name; no prior replacement proposal was found.
4. `component-triad`: approve exact decomposition/name set, choosing among `component-core`, `runtime-triad`, `contract-component`, separate component packaging/runtime/signal-contract packets, or another exact mapping.

## Can `primary-ascl.2` be dispatched now?

No. Severity: blocker for `primary-ascl.2`. The implementation bead should not be dispatched for naming cleanup yet because the discovery requirement was not met: there is no exact approved mapping for the four requested names. Dispatching now would force the implementer to invent or choose names, which `primary-ascl.1` and `primary-ascl.2` explicitly forbid.

## Unknowns and not checked

- I did not inspect private repositories for approval evidence.
- I did not inspect full raw chat transcripts beyond targeted `.pi/.codex/.claude` local searches; no exact approval surfaced in those targeted searches.
- I did not run source generators or tests because this was discovery-only and read-only.
- I did not modify source files, tracker state, or generated runtime surfaces.

## Review findings

- blocker: `primary-ascl.2` — no exact approved old-name to new-name mapping was found for `jj`, `beads`, `beauty`, or `component-triad`; implementation must wait for psyche approval or a newly located approval source.
- medium: `component-triad` — prior proposals conflict between keeping/slimming, splitting to `runtime-triad`, using `component-core`, and using `contract-component`; prior text explicitly marks the split as a psyche decision.
- medium: `beads` — prior proposals conflict between `work-tracking`, lead-only bundle, temporary retention while BEADS remains live, and future Persona/mind tracking.
- low: `jj` and `beauty` — role-composition modules already absorb their content, but no evidence shows active first-class names should be renamed to those composite modules.

## Residual risks

- A prior approval may exist in unsearched private/local transcript material, but it was not found in scoped public project evidence, tracker, agent outputs, or public Spirit search.
- The `repos/skills-primary-ascl-doctrine` worktree demonstrates role-composition naming, but treating those names as approved active-skill replacements would overextend the evidence.
- If the psyche wants only wording cleanup inside generated packets rather than active module id renames, `primary-ascl.2` should be re-scoped before dispatch.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete blocker and ambiguity findings list paths and line references: agent-outputs/SkillDoctrineV2/SkillEditor-CorpusTriage.md:59-74,84,122,151,161-168; agent-outputs/RoleSkillReview/SkillEditor-CorpusTrimProposal.md:219-225,401-419; repos/skills-primary-ascl-doctrine/agent-outputs/V2RoleDoctrineBundles/SkillEditor-Handoff.md:26-35; repos/skills-primary-ascl-doctrine/modules/repo-operation-core/full.md:15-20,49-62; repos/skills-primary-ascl-doctrine/modules/code-implementation-core/full.md:22-24; repos/skills-primary-ascl-doctrine/modules/rust-core/full.md:27-29."
    }
  ],
  "changedFiles": [
    "/home/li/primary/agent-outputs/primary-ascl/naming-discovery.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "sed -n '1,220p' AGENTS.md",
      "result": "passed",
      "summary": "Read project instructions."
    },
    {
      "command": "bd show primary-ascl primary-ascl.1 primary-ascl.2 --long",
      "result": "passed",
      "summary": "Confirmed discovery scope and that implementation is blocked pending approved replacements."
    },
    {
      "command": "rg --no-ignore ... targeted searches for jj/beads/beauty/component-triad and replacement terms",
      "result": "passed",
      "summary": "Found proposals and role-composition evidence but no exact approved mapping."
    },
    {
      "command": "spirit PublicTextSearch for jj, beads, beauty, component-triad, skill/naming related terms",
      "result": "passed",
      "summary": "Exact bad-name searches returned no matching public Spirit records; broader searches found no exact replacement approval."
    },
    {
      "command": "nl -ba selected evidence files",
      "result": "passed",
      "summary": "Collected line-number evidence for cited findings."
    },
    {
      "command": "jj status --no-pager; wc -l /home/li/primary/agent-outputs/primary-ascl/naming-discovery.md; rg -n '```acceptance-report|blocker: primary-ascl\\.2|Can `primary-ascl\\.2`' /home/li/primary/agent-outputs/primary-ascl/naming-discovery.md",
      "result": "passed",
      "summary": "Confirmed the report exists, has the acceptance report marker, and jj shows only agent-output working-copy changes including this new report."
    }
  ],
  "validationOutput": [
    "Report written to /home/li/primary/agent-outputs/primary-ascl/naming-discovery.md.",
    "No source files, tracker state, or generated runtime surfaces were edited.",
    "jj status after writing showed this new report plus pre-existing/unrelated agent-output changes; no source paths were changed."
  ],
  "residualRisks": [
    "A prior approval may exist in unsearched private/local transcript material.",
    "Composite role modules may be mistaken for approved active-skill renames unless the psyche confirms that interpretation."
  ],
  "noStagedFiles": true,
  "diffSummary": "Discovery report only; no source or tracker mutations.",
  "reviewFindings": [
    "blocker: primary-ascl.2 - no exact approved replacement mapping was found for jj, beads, beauty, or component-triad; psyche approval is needed before implementation.",
    "medium: component-triad - prior proposals are mutually ambiguous and explicitly call for psyche approval if split.",
    "medium: beads - prior proposals are ambiguous between work-tracking, lead-only bundle, temporary retention, and future Mind/memory/weave vocabulary.",
    "low: jj and beauty - role-composition modules absorb their content but do not evidence approved active-name replacements."
  ],
  "manualNotes": "primary-ascl.2 should not be dispatched for naming cleanup now. Ask the psyche for exact old-name to new-name mappings or provide a newly located approval source."
}
```
