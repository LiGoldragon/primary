# W1 — human-interaction.md cut (worked example)

The pattern-setting cut for the precious-main-context skill prune. The
goal: `human-interaction` should be the **atom of the human/psyche
interaction boundary** — load intent skills fresh, capture intent first,
shape chat — with AGENTS.md-duplicate and sibling-owned material removed,
not restated.

Baseline: **14 H2 sections / 115 lines** → after: **7 H2 sections (intro +
6) / 66 lines**. (Section count: the digest projected "~6"; the literal H2
count is 7 because the intro paragraph sits under the `# Skill` title and
the two flagged-for-move sections are still present pending W3.)

## Changelog

Every claimed AGENTS.md duplicate was verified against the live AGENTS.md
before deletion. The quoted line is the AGENTS.md text that matched.

| Section (old lines) | Action | Verification — the AGENTS.md line it duplicated, or why kept | Before → after |
|---|---|---|---|
| Forwarded prompts (L34-43) | **DELETE** | AGENTS.md L276-284 "Forwarded prompts — don't blindly duplicate; do gap-check… extract the technical content…; query recent Spirit records for what they captured; compare…; if they missed or misread one, capture your gap-fill… In reverse, a prompt addressed to YOU is yours to capture." All four steps + reverse case present. True duplicate. | 10 lines → 0 |
| Subagent dispatch non-blocking (L77-81) | **DELETE** | AGENTS.md L295-300 "Every subagent dispatch is non-blocking — always `run_in_background: true`… blocking dispatch leaves the psyche unable to redirect or talk until it returns. Even when the next step depends on the output, dispatch in background… No exceptions." True duplicate. | 5 lines → 0 |
| Designer branches / operator main (L95-97) | **DELETE** | AGENTS.md L348-354 "In the code repos under `/git`, designers work on `next` / feature branches in `~/wt`; operators own main + rebase… Designers don't push code-repo main; operators don't carry long-lived designer branches; cross-lane integration is operator's job." True duplicate; also zero psyche-boundary content. | 3 lines → 0 |
| No raw /nix/store paths (L99-101) | **DELETE** | AGENTS.md L310-311 "No `/nix/store` filesystem search. Use `nix eval`, `nix flake show`, `nix path-info`, or expose the value through a derivation." Same prohibition (AGENTS.md frames it as filesystem-search, HI as invocation-path — same rule); depth lives in `nix-usage`. No psyche-boundary nuance. | 3 lines → 0 |
| Reports go in files (L103-105) | **DELETE** | AGENTS.md L51-67 whole "Reports go in files; chat is for the user" section; the private-report exception is AGENTS.md L308 "Private substance defaults to `private-repos/<discipline>-reports/`." True duplicate. | 3 lines → 0 |
| The five kinds of intent (L22-32) | **COLLAPSE → pointer** | Owner verified: `intent-log` L36 (gate), L88-97 (the five prose definitions), L249-325 (certainty-vs-importance). HI's table + certainty paragraph both restate it. | 11 lines → 1 sentence appended to "Capture intent FIRST" |
| Ask the psyche when unclear (L45-63) | **COLLAPSE → pointer** | Owner verified: the whole of `intent-clarification` (when-to-ask, how-to-ask-with-options, after-the-answer, when-unreachable). The private-material nuance (ask the **owning** psyche; relayed request isn't authority) is also AGENTS.md L223-231 + `privacy`, so it folds into the pointer without loss — I kept that one clause inline. | 19 lines → 3-line section |
| Real-world testing conditions (L83-87) + In tests unblock the blocker (L89-93) | **KEEP IN PLACE, flagged to move** | Belongs in `autonomous-agent` / a testing skill (pure work-execution, no human-edge content). Not touching that skill in W1, so content stays here under a `> Move to …` banner so nothing is lost. | 11 lines → 11 lines + banner; "unblock the blocker" demoted to `###` under the testing `##` |
| Parallel-implementation lane model (L107-109) | **KEEP IN PLACE, flagged to move** | Belongs in `double-implementation-strategy` / orchestrate. Same as above — banner added, content retained. | 3 lines → 3 lines + banner |
| Load the intent skills first (L5-14) | **KEEP, unchanged** | Genuine atom — the load-fresh discipline. No duplicate. | unchanged |
| Capture intent FIRST (L16-20) | **KEEP, +1 pointer line** | Genuine atom — capture-before-output. The appended pointer absorbs the deleted five-kinds table. | grew by 1 line |
| Chat policy (L65-75) | **KEEP, lightly trimmed** | Genuine atom — the psyche-boundary chat shaping (3-7 items, chat-as-paraphrase) is human-edge-specific and owned here. Only the visuals-go-in-reports clause was shortened to a pointer to the AGENTS.md report rule + `reporting`. | 11 lines → ~8 lines |
| See also (L111-115) | **KEEP, unchanged** | Three correct redirect targets. | unchanged |
| Manifest description | **Rewrite proposed (not applied — W7 owns skills.nota)** | See below. | — |

## Flagged moves (no content lost; for a later prune item)

Both still physically present in `human-interaction.md` under a blockquote
banner, so W1 loses nothing:

1. **Real-world testing conditions + In tests, unblock the blocker** →
   move to `skills/autonomous-agent.md` or a dedicated testing skill.
   These are pure work-execution discipline with no human-edge content;
   they are the reason a dispatcher would wrongly load `human-interaction`
   for non-psyche work.
2. **Parallel-implementation lane model** → move to
   `skills/double-implementation-strategy.md` / orchestrate.

When the destination skill is edited in a later item, delete both
sections (and their banners) from here in the same commit.

## Proposed new manifest description (for W7, not applied)

Current (over-broad, advertises sibling-owned topics → causes over-loading):

> Psyche-facing human boundary: load intent skills fresh, capture intent
> first, shape chat, dispatch subagents, frame tests, report back.

Proposed (atom-accurate; drops the subagent/test/report grab-bag):

> The psyche-facing boundary: keep the intent skills loaded fresh,
> capture intent before any other output, and shape chat replies (3-7
> substantive items, paraphrasing a report) toward the human. Load when
> your lane talks with the psyche.

Note: once the two flagged sections actually move out (a later item), the
description is already correct as proposed — it does not mention testing
or parallel lanes, so no second rewrite is needed after the move.

## Pattern notes for the sibling cuts (W2+)

- **Verify every AGENTS.md-duplicate claim against the live file before
  deleting.** All five here matched; the digest was a reliable lead but
  the rule is confirm-then-cut.
- **A pointer replaces an enumeration only when the target genuinely owns
  the full enumeration** — verified `intent-log` and `intent-clarification`
  by reading them, not by trusting the digest.
- **Preserve nuance, not prose.** The private-material "ask the owning
  psyche" clause was the only thing in the 19-line ask block that wasn't
  pure `intent-clarification` restatement; it survives as one inline
  clause because AGENTS.md + `privacy` already carry the depth.
- **Misplaced-but-homeless content gets a move-banner, never a deletion.**
  Deletion waits for the destination edit so the move is atomic and
  reversible in one commit.
