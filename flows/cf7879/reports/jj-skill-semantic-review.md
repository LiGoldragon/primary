# Authored skill review for Jujutsu

A Luna subflow reports reviewing all 45 authored Markdown skill files at Curriculum proposal revision `08e051cf2830586fd78bff94d40b41074a75bbfc`. Root independently read the version-control and nix-input-upgrade bodies as source data and had already verified the immutable 45-file inventory. This is a semantic source audit, not skill loading, native body receipt, source implementation, adoption or a Nix-tested artifact.

## Smallest proposed edits

| Authored source | Finding | Proposed edit |
|---|---|---|
| skills/nix-input-upgrade.md:12 | Allows a fork to be fast-forwarded through GitHub API, bypassing the proposed JJ publication workflow | Require the configured JJ remote/bookmark workflow for mutations; API inspection can remain read-only |
| skills/main-flow.md:13 | Offers Git or JJ history searching while the proposed central law says repository operations use JJ | Say “searching repository history with jj,” retaining the warning that reads of a live colocated workspace may snapshot/import state |
| skills/main-feature-integration.md:2 | Description says branches while its body uses producer bookmarks | Optional terminology cleanup to “Several producer bookmarks must come together on main” |
| skills/nix-input-upgrade.md:22–24 | “Rebase” refers to adapting patch content across upstream versions; this can be confused with rewriting repository history | Optional clarification: refresh the patch against the new source and verify applicability; this wave still permits only forward commits |

The `git clone --shared` example in file-editing.md is a prohibition, not an instruction to use it. Removing that example is optional wording cleanup, not a discovered operational violation.

## Beads is a separate unresolved requirement

The reviewer found no inherent contradiction between Beads bookkeeping and JJ version control. That does **not** close the living's separate requirement to remove residual Beads language from the stronger main/subflow proposal before its approval/adoption. The relevant references remain in main-flow.md lines 36 and 49, subflow.md line 11, prompt-crafting.md line 7, and the Beads skill itself. The stronger text at proposal commit 5f8b46f is not main. This review neither adopts that text nor authorizes a vocabulary/tracking migration.

## Coverage by file

Repository/tracking-related files were reviewed individually: `version-control`, `feature-development`, `file-editing`, `repository-lifecycle`, `nix-input-upgrade`, `lojix`, `main-feature-integration`, `main-flow`, `beads`, `subflow`, and `prompt-crafting`.

The remaining 34 files require no identified VC-mechanics change in this bounded review (some mention commits or harness Git context descriptively): `agent-harness-packaging`, `behavior`, `breaking-upgrades`, `claude-harness`, `codex-harness`, `context-strata`, `correction`, `datom`, `deepseek-harness`, `design`, `disk-hygiene`, `documentation-placement`, `edit-coordination`, `ethos`, `flow-evidence`, `nexus-rationale`, `nexus`, `nix-workflow`, `operating-system`, `orchestrate`, `protos`, `psyche-acquisition`, `psyche-distillation`, `psyche-grasp`, `psyche-interraction`, `psyche`, `realization`, `secrets`, `skill-designing`, `spirit`, `testing`, `transcript-search`, `versioning`, and `vocabulary`.

The central proposed law covers isolated ownership, forward publication to assigned producer bookmarks, direct remote verification, explicit integrator authority and caution around shared state. Existing compatible publication-order/freshness clauses do not require cosmetic JJ commands added to unrelated instructions.

## Limits and next step

The user's request was to rewrite all skills for JJ. This report advances the full inventory/review part; it does not claim that every skill has been rewritten. No authored or generated skill tree changed during this audit. The next source step is a forward Curriculum proposal implementing the concrete corrections and separately resolving the Beads cleanup, then regenerating and validating projections after the applicable review. Main integration, the integrator assignment and adoption remain unresolved. Generated .agents/.claude/.codex/.pi trees remain read-only evidence.
