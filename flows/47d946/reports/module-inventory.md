 # Context module inventory
 
 Observed read-only on 2026-10-14 from the authored repositories named in `SKILL_VARIABLES.md`.
 
 ## Result
 
There are 136 authored Markdown modules: Psyche 41, Mind 45, Field 50. Psyche has one current loader input outside `skills/`: `vision/ethos.md`.
 
 The evidence does not define a numeric ideal size. It does establish an ideal-size requirement and a density requirement. Therefore this report marks measured outliers for review; it does not decree splits.
 
 Largest measured modules:
 
 | Repository | Module | Bytes | Lines | Words |
 | --- | --- | ---: | ---: | ---: |
 | psyche-context | vision-datom.md | 15541 | 318 | 2565 |
 | mind-context | operation-lojix.md | 10997 | 383 | 1462 |
 | psyche-context | vision-nexus.md | 10122 | 197 | 1590 |
 | psyche-context | vision-flow.md | 6594 | 86 | 1142 |
 | field-context | compensation-psyche-interraction.md | 6951 | 100 | 1153 |
 | mind-context | operation-psyche-interraction.md | 6838 | 100 | 1134 |
 | psyche-context | vision-protos.md | 6801 | 153 | 1098 |
 | mind-context | knowledge-datom.md | 6495 | 106 | 1019 |
 
 Modules above 200 lines or 1,000 `wc -w` words are the eight rows above. They are split candidates only if their statements have more than one coherent owner; the current records forbid repetition and require a statement to have one home. The largest modules are concentrated in technical/reference topics, so size alone does not prove a split.
 
 ## Distribution
 
 | Repository | Kind counts | Bytes sum / mean / median / min / max | Lines sum / mean / median / min / max | Words sum / mean / median / min / max |
 | --- | --- | --- | --- | --- |
| psyche-context | intent 14; spirit 1; vision 26 | 94593 / 2307.1 / 729.0 / 177 / 20262 | 2045 / 49.9 / 18.0 / 6 / 494 | 14960 / 364.9 / 123.0 / 20 / 2799 |
 | mind-context | knowledge 13; operation 32 | 100542 / 2234.3 / 1339.0 / 197 / 10997 | 1805 / 40.1 / 23.0 / 6 / 383 | 15106 / 335.7 / 195.0 / 28 / 1462 |
 | field-context | compensation 50 | 61715 / 1234.3 / 794.0 / 149 / 6951 | 933 / 18.7 / 14.0 / 6 / 100 | 9650 / 193.0 / 115.0 / 21 / 1153 |
 
 Kind totals:
 
 | Repository | Kind | Modules | Bytes | Lines | Words |
 | --- | --- | ---: | ---: | ---: | ---: |
 | psyche-context | intent | 14 | 9646 | 182 | 1666 |
 | psyche-context | spirit | 1 | 1806 | 33 | 280 |
| psyche-context | vision | 26 | 83141 | 1830 | 13014 |
 | mind-context | knowledge | 13 | 41690 | 673 | 6147 |
 | mind-context | operation | 32 | 58852 | 1132 | 8959 |
| field-context | compensation | 50 | 61715 | 933 | 9650 |

Word-count percentiles (nearest-rank p90, index `ceil(0.90*n)`): Psyche n=41, min 20, median 123, p90 1098, max 2799; Mind n=45, min 28, median 195, p90 853, max 1462; Field n=50, min 21, median 115, p90 426, max 1153.
 
 ## Counting method and limits
 
Each row is one authored loader-input `*.md` regular file: all regular Markdown directly under each repository's `skills/` directory, plus Psyche's current `vision/ethos.md`, selected by `find -maxdepth 1 -type f -name '*.md'` in those roots and sorted by path. The complete-tree check found no other current authored Markdown outside those roots except README files, which are repository documentation rather than loader modules. This includes tracked, modified, and untracked files present in the checked-out worktree; it excludes deleted files because they are no longer regular files on disk. YAML frontmatter is included because the whole file is counted. Generated `.agents/`, `.claude/`, `.codex/`, `.pi/`, and `.opencode/` trees are outside these roots and excluded. Bytes are GNU `wc -c` (the file's byte count). Lines are GNU `wc -l` (newline characters; a final unterminated line is not counted). Words are locale-fixed `LC_ALL=C wc -w`, which counts whitespace-delimited words under the system utility's definition. Word counts are not tokens. No tokenizer was available with a specified model vocabulary, so no token count or universal word-to-token conversion is asserted.
 
The inventory reads current worktrees. Psyche is clean at `bf03117b424413cea4c3df7cf76a279127c8567d` (short `bf03117`, 2026-10-14). The actual current Mind repository is `/git/github.com/LiGoldragon/mind-context` with remote `git@github.com:LiGoldragon/mind-context.git`; it is detached at `344f6c3669d3d882f96f63ed435022a3cfed2bf4` (short `344f6c3`, 2026-10-09) and has foreign/current modifications in `skills/operation-book.md`, `skills/operation-flashbook.md`, and `skills/operation-main-flow.md`. The actual current Field repository is `/git/github.com/LiGoldragon/field-context` with remote `git@github.com:LiGoldragon/field-context.git`; its last commit is `5070467dd8b596246c47e9cbcbf55415025483fc` (short `507046`, 2026-10-13), and its worktree contains the broad compensation rename/addition/deletion set shown by `git status` (including deletion of the remaining `trial-*` files). Counts include those current worktree states, so they are measurements of the checked-out files, not claims about the last commits.
 
 ## Current psyche records and rules bearing on size and placement
 
 The current authored Psyche module `/git/github.com/LiGoldragon/psyche-context/skills/vision-context-modules.md` says:
 
 > Knowledge modules are audited from time to time for truth and currency against practice; a variation found goes to the type that holds what is unclear.
 
 The raw record `vision-raw/skillsRepository.md` (2026-08-21, design session 15b67974) says the elaborate breakup into modules was a bad approach and that the manifest should be removed in favour of generating whatever skills are present. This is an exception against assuming that more modules is better; it gives no numeric size rule.
 
 The raw record `flows/d68c82/vision/context-modules.md` (2026-10-13) says: “a subject he reviews or asks about has a module to hold it; modules have an ideal size”; it also says a module should not have so much content that it can hold more. The same record says “dense modules is intent” and “context modules are super dense and precise; no statement in two modules.” These are qualitative current direction, not a measured threshold.
 
 The raw record `flows/5ed94b/vision/contextModules.md` (2026-10-03) says all work now concerns editing, creating, removing, splitting, and merging context modules. It leaves which modules qualify for the system prompt open.
 
 The raw record `flows/d4ae97/vision/contextModules.md` (2026-10-07) says context should be modularized, with a small brief and most flow context coming from modules; it gives a 100,000-token context example and 100:1 or 1,000:1 leverage target for caller output versus loaded context. It does not define a module size.
 
 The raw record `vision-raw/domainKnowledgePlacement.md` (2026-08-08/09) places domain-specific information in its domain repository and says documentation should live in the code it documents; this supports keeping Psyche, Mind, and Field material in their owning repositories.
 
 The raw record `flows/edf227/vision/contextModules.md` (2026-10-03) says modules are Markdown, with registry type/name/location metadata, and launches select module names rather than repeating content. The raw record `flows/f5a6e9/vision/contextModules.md` (2026-10-09) adds source hash and relative path to registry identity. These records concern registry identity, not split thresholds.
 
 The current Mind operation module `operation-file-editing.md` says: “A source file is written in pieces of a few hundred lines; a module that would exceed that is split.” This is the clearest operational split rule found. It points at `vision-datom.md` (318 lines) and `operation-lojix.md` (383 lines) as direct review candidates. It does not state whether “few” means a fixed number, so the threshold remains unknown.
 
 The current Field module `compensation-skill-designing.md` says: “Each piece of meaning has one home” and “A new line replaces the line it resembles, never stands alongside it.” This supports splitting only along coherent ownership boundaries and checking duplicate statements.
 
 ## Repository and eventual edit facts
 
 Authored sources are the `*.md` files under the three `skills/` directories above. The generated trees under Primary are read-only evidence. Repository AGENTS search found no `AGENTS.md` under any of the three context repositories. Primary's `NON_MANAGEMENT_AGENTS.md` says authored source files are those Markdown files, generated trees must not be edited, and Primary changes belong to the standing committer. The Mind repository currently violates a clean-worktree assumption; preserve those edits. The Field worktree also contains foreign/current uncommitted work; preserve it.
 
The eventual worker should edit only the owning authored repository, claim exact paths through Orchestrate before editing shared files, and follow the repository's own publication workflow. All three origins are SSH GitHub remotes with default branch `main`: `git@github.com:LiGoldragon/psyche-context.git`, `git@github.com:LiGoldragon/mind-context.git`, and `git@github.com:LiGoldragon/field-context.git`. The current Mind source instruction says normal non-Primary jj publication is `jj commit -m 'short imperative message'`, `jj bookmark set main -r @-`, then `jj git push --bookmark main`. In these shared checkouts, that route is blocked for a new worker until ownership of the existing dirty changes is established: committing would capture foreign work, and resetting, abandoning, restoring, or cleaning would destroy it. Use an independent clone/workspace for an owned change, or have the existing owner land the dirty work first. This research task made no edits to either context repository, commits, builds, or pushes.

New knowledge or inquiry material belongs in the owning Mind context repository. The current Psyche module `vision-context-modules.md` states that Mind has knowledge modules and a second type, inquiry, for what is unclear or what an audit finds varying from stated knowledge. No repository-level `AGENTS.md` exists under any of the three context repositories. The authored source files remain the `skills/*.md` files; generated evidence trees are not edit targets.
 
## Whole relevant records

The following are the complete relevant records as read, with provenance retained.

`flows/d68c82/vision/context-modules.md`, 2026-10-14, Psyche STT, relayed by the Psyche Core Tertiary:

> ## 2026-10-14 — context modules are super dense and precise; no statement in two modules
>
> I want to go hard on reprogramming the behavior for this in many layers: from the whole concept that the context is super important and the context modules must be super dense and precise (especially the system stuff like spirit and intent), and from the point of view of the book and how it's presented.
>
> If the spirit context is long I would refocus on honing in on the whole concept of how to handle the user interface, how to communicate better.
>
> This would be a repetition so no, we're not going to repeat the same thing in two skills. Let's not do that. Let's skill ourselves against that somewhere.
>
> ## 2026-10-14 — dense modules is intent
>
> This is great. Actually this is even intent. This is intent. This is system prompt vision, which is intent.
>
> ## 2026-10-14 — a subject he reviews or asks about has a module to hold it; modules have an ideal size
>
> In review, anything that's thought to be relevant for me to review, especially if I ask questions concerning a subject, means that there should be a skill on that topic or broader topic that will hold it (and doesn't have so much content that it can hold more), right? We have a sort of ideal context module size also.
>
> A knowledge review is not so much a proposal but I'm reviewing knowledge and it can be knowledge that already exists.

`vision-raw/skillsRepository.md`, 2026-08-21, design session `15b67974`, typed:

> re registration check: the problem is we should get rid of the manifest and generate whatever skills are present. curriculum went through a very elaborate phase that was abandonned. many of those things are now unwanted. like how some things were broken up into modules. new insights made me realize this was the bad approach.

This is the principal exception: it rejects module proliferation as an automatic goal, while the newer 2026-10-14 record establishes an ideal size. Neither record gives a numeric threshold.

`/git/github.com/LiGoldragon/mind-context/skills/operation-file-editing.md`, current authored Mind source:

> A source file is written in pieces of a few hundred lines; a module that would exceed that is split.

This is an operational rule for split review. “A few hundred” is not numerically defined, so it cannot produce a hard p90 or byte threshold by itself.

## Complete inventory
 
 Columns: repository, filename, bytes, newline-lines, `LC_ALL=C wc -w` words.
 
 | Repository | Module | Bytes | Lines | Words |
 | --- | --- | ---: | ---: | ---: |
 | psyche-context | intent-anatomy.md | 297 | 10 | 50 |
 | psyche-context | intent-context-modules.md | 256 | 8 | 43 |
 | psyche-context | intent-context.md | 288 | 9 | 53 |
 | psyche-context | intent-conversion.md | 372 | 11 | 69 |
 | psyche-context | intent-data.md | 559 | 12 | 95 |
 | psyche-context | intent-design.md | 311 | 6 | 55 |
 | psyche-context | intent-main-flow.md | 2245 | 23 | 388 |
 | psyche-context | intent-mandatory-traits.md | 767 | 18 | 123 |
 | psyche-context | intent-models.md | 748 | 18 | 134 |
 | psyche-context | intent-protos-parsing.md | 614 | 13 | 100 |
 | psyche-context | intent-psyche-interaction.md | 566 | 12 | 96 |
 | psyche-context | intent-psyche.md | 1514 | 22 | 260 |
 | psyche-context | intent-startup-prompt.md | 614 | 8 | 112 |
 | psyche-context | intent-testing.md | 495 | 12 | 88 |
 | psyche-context | spirit-core.md | 1806 | 33 | 280 |
 | psyche-context | vision-archive-ethos-monolith.md | 1998 | 53 | 320 |
 | psyche-context | vision-aspects.md | 694 | 12 | 117 |
 | psyche-context | vision-book.md | 1345 | 14 | 251 |
 | psyche-context | vision-committing.md | 431 | 12 | 77 |
 | psyche-context | vision-context-modules.md | 2170 | 57 | 231 |
 | psyche-context | vision-crystallization.md | 1534 | 44 | 244 |
 | psyche-context | vision-datom.md | 15541 | 318 | 2565 |
 | psyche-context | vision-deployment.md | 420 | 14 | 82 |
 | psyche-context | vision-design.md | 486 | 8 | 85 |
 | psyche-context | vision-flow.md | 6594 | 86 | 1142 |
 | psyche-context | vision-high-level-view.md | 312 | 13 | 54 |
 | psyche-context | vision-horizon.md | 666 | 18 | 115 |
 | psyche-context | vision-meaning.md | 3567 | 83 | 629 |
 | psyche-context | vision-messaging.md | 1474 | 33 | 241 |
 | psyche-context | vision-model-roles.md | 2952 | 69 | 489 |
 | psyche-context | vision-nexus.md | 10122 | 197 | 1590 |
 | psyche-context | vision-orchestrate.md | 441 | 15 | 65 |
 | psyche-context | vision-persona.md | 748 | 12 | 136 |
 | psyche-context | vision-protos.md | 6801 | 153 | 1098 |
 | psyche-context | vision-psyche.md | 1465 | 27 | 203 |
 | psyche-context | vision-remembering.md | 729 | 20 | 129 |
 | psyche-context | vision-sema.md | 654 | 18 | 90 |
 | psyche-context | vision-signal.md | 1253 | 46 | 189 |
 | psyche-context | vision-system-one.md | 305 | 8 | 53 |
 | psyche-context | vision-x11.md | 177 | 6 | 20 |
 | psyche-context | vision/ethos.md | 20262 | 494 | 2799 |
 | mind-context | knowledge-claude-harness.md | 3962 | 76 | 600 |
 | mind-context | knowledge-codex-harness.md | 3374 | 65 | 501 |
 | mind-context | knowledge-codex.md | 2319 | 37 | 292 |
 | mind-context | knowledge-context-strata.md | 1339 | 31 | 213 |
 | mind-context | knowledge-datom.md | 6495 | 106 | 1019 |
 | mind-context | knowledge-ethos.md | 4190 | 26 | 632 |
 | mind-context | knowledge-flow.md | 3586 | 68 | 378 |
 | mind-context | knowledge-layer-models.md | 3257 | 21 | 466 |
 | mind-context | knowledge-nexus.md | 1383 | 15 | 173 |
 | mind-context | knowledge-protos.md | 4836 | 86 | 788 |
 | mind-context | knowledge-psyche.md | 3944 | 78 | 630 |
 | mind-context | knowledge-vocabulary.md | 1795 | 41 | 295 |
 | mind-context | knowledge-yt-dlp.md | 1210 | 23 | 160 |
 | mind-context | operation-agent-harness-packaging.md | 1062 | 18 | 146 |
 | mind-context | operation-beads.md | 3188 | 54 | 460 |
 | mind-context | operation-book.md | 1420 | 24 | 215 |
 | mind-context | operation-clojure-development.md | 338 | 10 | 48 |
 | mind-context | operation-design.md | 791 | 16 | 118 |
 | mind-context | operation-disk-hygiene.md | 232 | 8 | 33 |
 | mind-context | operation-documentation-placement.md | 972 | 17 | 146 |
 | mind-context | operation-edit-coordination.md | 629 | 12 | 109 |
 | mind-context | operation-feature-development.md | 197 | 6 | 28 |
 | mind-context | operation-file-editing.md | 1228 | 26 | 195 |
 | mind-context | operation-flashbook-illustration.md | 1404 | 12 | 240 |
 | mind-context | operation-flashbook.md | 2639 | 36 | 421 |
 | mind-context | operation-flow-evidence.md | 713 | 11 | 103 |
 | mind-context | operation-lojix.md | 10997 | 383 | 1462 |
 | mind-context | operation-main-flow.md | 5354 | 51 | 854 |
 | mind-context | operation-nix-input-upgrade.md | 2392 | 29 | 349 |
 | mind-context | operation-nix-workflow.md | 1105 | 19 | 169 |
 | mind-context | operation-operating-system.md | 834 | 14 | 115 |
 | mind-context | operation-orchestrate.md | 1710 | 32 | 235 |
 | mind-context | operation-prompt-crafting.md | 657 | 10 | 106 |
 | mind-context | operation-psyche-acquisition.md | 520 | 15 | 78 |
 | mind-context | operation-psyche-distillation.md | 3204 | 49 | 511 |
 | mind-context | operation-psyche-grasp.md | 790 | 16 | 111 |
 | mind-context | operation-psyche-interraction.md | 6838 | 100 | 1134 |
 | mind-context | operation-realization.md | 370 | 10 | 50 |
 | mind-context | operation-relaying-the-living.md | 363 | 10 | 59 |
 | mind-context | operation-repository-lifecycle.md | 598 | 14 | 90 |
 | mind-context | operation-secrets.md | 842 | 15 | 115 |
 | mind-context | operation-skill-designing.md | 5032 | 73 | 853 |
 | mind-context | operation-stale-lock.md | 639 | 6 | 105 |
 | mind-context | operation-testing.md | 1111 | 24 | 190 |
 | mind-context | operation-transcript-search.md | 683 | 12 | 111 |
 | field-context | compensation-agent-harness-packaging.md | 1065 | 18 | 146 |
 | field-context | compensation-behavior.md | 1412 | 26 | 258 |
 | field-context | compensation-book-crystallization.md | 1854 | 18 | 323 |
 | field-context | compensation-book.md | 1403 | 24 | 211 |
 | field-context | compensation-breaking-upgrades.md | 324 | 8 | 40 |
 | field-context | compensation-clojure-development.md | 338 | 10 | 48 |
 | field-context | compensation-correction.md | 788 | 16 | 145 |
 | field-context | compensation-default-effort.md | 525 | 15 | 77 |
 | field-context | compensation-design.md | 1017 | 25 | 162 |
 | field-context | compensation-disk-hygiene.md | 232 | 8 | 33 |
 | field-context | compensation-documentation-placement.md | 972 | 17 | 146 |
 | field-context | compensation-edit-coordination.md | 629 | 12 | 109 |
 | field-context | compensation-feature-development.md | 197 | 6 | 28 |
 | field-context | compensation-file-editing.md | 525 | 14 | 83 |
 | field-context | compensation-flashbook-illustration.md | 1404 | 12 | 240 |
 | field-context | compensation-flashbook.md | 2637 | 36 | 419 |
 | field-context | compensation-flow-evidence.md | 547 | 10 | 78 |
 | field-context | compensation-independent-review.md | 207 | 6 | 33 |
 | field-context | compensation-launch.md | 2744 | 40 | 452 |
 | field-context | compensation-low-power.md | 155 | 6 | 25 |
 | field-context | compensation-main-flow.md | 5527 | 51 | 884 |
 | field-context | compensation-messenger-clj.md | 3698 | 20 | 555 |
 | field-context | compensation-nix-rationale.md | 2779 | 18 | 392 |
 | field-context | compensation-nix-workflow.md | 1105 | 19 | 169 |
 | field-context | compensation-nix.md | 3257 | 52 | 426 |
 | field-context | compensation-operating-system.md | 824 | 14 | 115 |
 | field-context | compensation-orders.md | 1023 | 20 | 178 |
 | field-context | compensation-presentation-book.md | 621 | 10 | 88 |
 | field-context | compensation-primary-commit.md | 1314 | 10 | 195 |
 | field-context | compensation-prompt-crafting.md | 468 | 9 | 75 |
 | field-context | compensation-prose.md | 820 | 19 | 136 |
 | field-context | compensation-psyche-design.md | 800 | 16 | 118 |
 | field-context | compensation-psyche-injection.md | 252 | 6 | 37 |
 | field-context | compensation-psyche-interraction.md | 6951 | 100 | 1153 |
 | field-context | compensation-questions-book.md | 175 | 6 | 21 |
 | field-context | compensation-realization.md | 379 | 10 | 50 |
 | field-context | compensation-reaping.md | 206 | 6 | 32 |
 | field-context | compensation-relaying-the-living.md | 569 | 12 | 95 |
 | field-context | compensation-repository-lifecycle.md | 615 | 14 | 92 |
 | field-context | compensation-secrets.md | 842 | 15 | 115 |
 | field-context | compensation-skill-designing.md | 3126 | 48 | 520 |
 | field-context | compensation-stale-lock.md | 816 | 6 | 134 |
 | field-context | compensation-subflow.md | 149 | 6 | 25 |
 | field-context | compensation-temporary.md | 476 | 10 | 78 |
 | field-context | compensation-testing.md | 1862 | 39 | 299 |
 | field-context | compensation-truth.md | 484 | 13 | 79 |
 | field-context | compensation-unblocking-commands.md | 618 | 9 | 98 |
 | field-context | compensation-understanding.md | 564 | 15 | 89 |
 | field-context | compensation-update.md | 2164 | 26 | 307 |
 | field-context | compensation-versioning.md | 256 | 7 | 39 |
 
