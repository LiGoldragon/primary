# Wave 4 migration audit

Wave 4 independently sought disconfirming evidence. It reproduced the
Vision matching from a fresh parse, rejected whole-file shortcuts, checked
earliest authorship and destination collisions, and challenged the earlier
zero-candidate result for bulk legacy stores.

## Approved session-flow work

Ten legacy session logs have exact transcript creation witnesses and may be
realized as terse current-protocol `log.md` files:

`e4be1c4a`, `358f143a`, `7c3f0c1d`, `bc05da32`, `01a01149`, `01a0145c`,
`01a0193f`, `01a01998`, `01a01a93`, and `01a020ff`.

The audit also approved:

- `reports/RustCodeAnalysisTools-2026-08-16.md` and
  `reports/HarnessRungMechanics-2026-08-16.md` for
  `flows/e4be1c4a/reports/`, with protocol-compliant `## Sources` endings;
- exact transcript-backed Vision fragments for the ten flows, as governed
  by the record-level Vision manifest;
- correction of the `01a020ff` external addendum now embedded in
  `flows/01a01b52/log.md`: the detailed external-edit material belongs in
  `flows/01a01b52/annotations.md`, headed by `01a020ff`, while the log keeps
  only a terse pointer.

The legacy session file is source material for reconstructing the terse
flow log; it is not copied wholesale when that would preserve the obsolete
protocol shape.

## Deferred or rejected session-associated work

- `759fc98a` remains unresolved because its recorded alternate transcript
  identifies itself as `d076fe3a`; the `01a0145c` predecessor addendum is
  blocked on the same identity mismatch.
- `72939228`, `4a959c64`, `6bec1f7a`, `b5b1f5fe`, and `91254d53` remain
  because no actual transcript was recovered.
- Mixed awareness files are not migrated wholesale.
- `bc05da32` materially edited the two `SkillDrafts/softwareDesign`
  reports, but did not originate them. Their whole-file migration to that
  flow is rejected; the true origin remains to be established.
- Five `7c3f0c1d` ledger reports live only on an unmerged side branch. The
  parent transcript witnesses landing, not nested-subflow authorship. They
  remain deferred until their actual transcript provenance and branch
  integration are established.
- `verified/` claims without direct write witnesses remain evidence claims,
  not migrated artifacts.

## Approved Vision work

A fresh parse inspected 376 Vision heading boundaries and 6,599 human user
records from actual Claude and Codex transcripts. It independently
reproduced the proposed 312 exact units:

- 286 session-marked exact heading records;
- 16 session-marked exact file-level units;
- 10 unmarked headings with one unique exact transcript origin.

The initial audit incorrectly rejected eight as already migrated under
`flows/fd301d9a/vision/`. Reinspection of that flow's annotation disproved
the classification: those files explicitly reproduce earlier quotations,
no ruling occurred in `fd301d9a`, and authoritative provenance remains with
the earlier flows. The eight therefore migrate to their actual origins:

- five records to `flows/15b67974/vision/`;
- one to `flows/55d18f4f/vision/rustComponentArchitecture.md`;
- two to `flows/e06e4c07/vision/nexus.md`.

The contextual `fd301d9a` copies remain annotated and are neither canonical
destinations nor grounds for retiring the raw origin records.

Final Vision disposition:

| Disposition | Units |
|---|---:|
| Approved for true-origin migration | 308 |
| Deferred for suggestion/queue provenance or unsafe split boundary | 4 |
| Drift, ambiguous, weak, no-match, Intent, Spirit, archive, or otherwise protected | All remaining units |

The four deferred units are `colonConfusion.md`,
`observerFixtureBlessed.md`, `streamSection.md`, and
`workingSpiritNewEthosSyntax.md`. Some of their content entered through
`suggestion_accepted` or queue operations rather than a canonical typed
user record. Superseded historical Vision remains historical Vision; it is
not discarded.

Destination files preserve exact psyche wording, source chronology, and
record boundaries. Mixed raw topic files must be split record-by-record;
they are never assigned wholesale to the last flow that edited them.

## Bulk-store challenge

The audit machine-searched main and nested Codex transcripts for exact
writes, edits, and commits involving `reports/`, `handoffs/`,
`awareness/sessions/`, `agent-outputs/`, and `verified/`. Hundreds of
transcripts mention those trees, but the mentions resolve to later reads,
searches, copied prompts, handoffs, or repository/evidence infrastructure.

No additional safely originated migration candidate was established. The
ungrounded files remain unknown and unmoved. The five already completed
migrations have no live duplicate source in these trees.

## Realization boundary

Wave 5 may create the approved canonical destinations and retire only the
corresponding legacy source material after exact comparison. Jujutsu keeps
that retirement recoverable. Deferred and unknown material stays byte-for-
byte in place. Destination collisions, mixed files, or failed comparison
stop the affected item without stopping independent approved migrations.

## Sources

- Wave 4 audit returns from the `origin_rule_history`, `migration_scope`,
  and `ruling_provenance` subflows of flow 01a02a06.
- Actual Claude and Codex transcripts enumerated in
  `reports/wave3OriginTrace.md`.
- `.agents/skills/flows/SKILL.md` as generated evidence of the current
  protocol; authored skill sources remain outside generated trees.
- `flows/fd301d9a/annotations.md` and its contextual Vision files.
- `flows/01a01b52/log.md`.
- Legacy files under `sessions/`, `reports/`, and `psyche-raw/Vision/`.
- Temporary Wave 4 manifest witnesses
  `/tmp/w4-exact-manifest-v3.tsv`, `/tmp/w4-filelevel-manifest-v2.tsv`, and
  `/tmp/w4-unmarked-manifest.tsv`; their checksums were returned by the
  audit subflow and must be rechecked by the implementation subflow.
- Flow 01a02a06 reports `wave1MigrationRulings.md`, `wave2Inventory.md`,
  and `wave3OriginTrace.md`.
