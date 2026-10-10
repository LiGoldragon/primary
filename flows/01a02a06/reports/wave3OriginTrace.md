# Wave 3 origin trace

Wave 3 traced candidate artifacts to actual transcript records. Every item
here remains a candidate until Wave 4 independently challenges identity,
earliest authorship, record boundaries, destination collisions, and source
retirement.

## Remaining legacy session records

Sixteen timestamped session records remain. Ten have a matching actual
transcript that directly witnesses creation of their legacy session log:

| Origin | Directly witnessed flow artifacts |
|---|---|
| `e4be1c4a` | Legacy log; `RustCodeAnalysisTools` and `HarnessRungMechanics` reports; several raw-Vision topics; mixed legacy awareness material. |
| `358f143a` | Legacy log and raw-Vision records across multiple topics. |
| `7c3f0c1d` | Legacy log and raw-Vision records; five ledger reports have parent landing witnesses but their content was authored in nested subflows. |
| `bc05da32` | Legacy log; material edits to two `SkillDrafts/softwareDesign` reports and three raw-Vision topics. Earliest report authorship is not yet established. |
| `01a01149` | Legacy log only. |
| `01a0145c` | Legacy log, a prior-session addendum, and one raw-Vision edit. |
| `01a0193f` | Legacy log only; its repository implementation outputs are excluded. |
| `01a01998` | Legacy log and raw Vision for `minimalFlake` and `mentci-egui`. |
| `01a01a93` | Legacy log and raw-Vision edits to `host-environment-recovery` and `skillDesigning`. |
| `01a020ff` | Legacy log and an addendum to predecessor `01a01b52`. |

`759fc98a` records an alternate Claude transcript whose actual UUID is
`d076fe3a`. That transcript witnesses awareness and Vision edits, but the
identity mismatch means neither the legacy log nor those artifacts may yet
be assigned to `flows/759fc98a/`.

No actual transcript was recovered for `72939228`, `4a959c64`, `6bec1f7a`,
`b5b1f5fe`, or `91254d53`. Their legacy logs and claimed artifacts remain
immovable.

## Raw Vision record trace

After excluding Intent, Spirit, archive material, and existing flow Vision,
Wave 3 classified the raw corpus at record level:

| Classification | Record units | Disposition entering Wave 4 |
|---|---:|---|
| Marked and exact transcript-verbatim | 286 | Candidate for origin-flow Vision. |
| Marked but partial/drifted | 13 | Remain. |
| Marked with no complete canonical match | 36 | Remain. |
| Weak `01a01450` provenance | 1 | Remain. |
| Unmarked but uniquely exact in one transcript | 10 | Candidate for that origin-flow Vision. |
| Marked file-level unit, uniquely exact | 16 | Candidate for origin-flow Vision. |
| Unmarked file-level unit without unique origin | 7 | Remain. |

The provisional exact candidate total is therefore 312 record units. The
ten newly traced unmarked headings are:

- `draftIdeasForImprovement.md:25-34` → `98fbfa47`;
- `entryFiles.md:7-11`, `:12-24`, and `:25-32` → `358f143a`;
- `everyConceptShouldHaveItsRepo.md:18-23` → `98fbfa47`;
- `falseConfidence.md:6-19`, `:20-33`, and `:34-49` → `358f143a`;
- `noctalia.md:1-6` → `01a01046`;
- `setupIndependentInterfaces.md:31-36` → `01a01046`.

The sixteen exact marked file-level units belong to `5abf3be8`,
`d63804f2`, `98fbfa47`, and `55d18f4f`. Wave 4 must reproduce all matches
from the transcripts, because Wave 3's complete line ledger was generated
as temporary analysis state rather than a durable artifact.

All drift, ambiguous, weak, attachment-derived, no-match, and unmarked
records remain. In particular, repeated wording is not a unique origin;
`019ff178`, `019ffbd3`, `72939228`, attachment UUID `37b689c9`, and the
`01a01450` history-versus-rollout mismatch are not resolved.

## Other legacy stores

A first exact-path trace across `reports/`, `handoffs/`,
`awareness/sessions/`, `agent-outputs/`, and `verified/` established no new
migration candidate. It positively classified 18 files as transcript
recovery, research, handoff, or evidence infrastructure. The remaining
bulk is ungrounded, not excluded by proof.

This zero-candidate result is deliberately not accepted yet: Wave 4 is
searching main and nested subagent transcript writes/edits/commits and will
challenge whether the first trace searched the correct side of the
artifact-to-transcript relationship.

## Sources

- Wave 3 transcript-trace returns from the `origin_rule_history`,
  `migration_scope`, and `ruling_provenance` subflows of flow 01a02a06.
- The 16 timestamped files under `sessions/` and their recorded transcript
  paths.
- Claude transcripts for `e4be1c4a`, `358f143a`, `7c3f0c1d`, `bc05da32`,
  and alternate `d076fe3a` under
  `/home/li/.claude/projects/-home-li-primary/`.
- Codex transcripts for `01a01149`, `01a0145c`, both `01a0193f` lanes,
  `01a01998`, `01a01a93`, and `01a020ff` under
  `/home/li/.codex/sessions/2026/08/`.
- `psyche-raw/Vision/`, matched against actual user-message records in the
  Claude and Codex transcript corpora.
- Flow 01a02a06 reports `wave1MigrationRulings.md` and
  `wave2Inventory.md`.
