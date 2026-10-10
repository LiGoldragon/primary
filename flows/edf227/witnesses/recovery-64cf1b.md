# Recovery from abandoned commit 64cf1b2edb4f

Stamp: 2026-10-03T18:05:50Z

## Method
Read-only: `jj --ignore-working-copy diff --from 64cf1b2edb4f --to @ --summary` listed 53 candidate paths. Each was compared with the file on disk (the jj working-copy snapshot was stale, so disk is the truth). Missing or older/smaller-than-abandoned paths were written from `jj --ignore-working-copy file show -r 64cf1b2edb4f <path>` under the lock; identical paths untouched; paths whose disk copy was newer (after the abandoned commit's 11:59:15 -0600) and larger were skipped. No jj commit/abandon/restore/new/edit was run for recovery.

## Restored (22)

### 5578cc
- .5578cc.flow-id
- .5578cc.flow-id.lock

### 42265e
- flows/42265e/log.md
- flows/42265e/reports/claude-mcp-capability-fixture-2026-10-03.md
- flows/42265e/reports/home-deployment-2026-10-03.md
- flows/42265e/reports/home-deployment-79-evidence.md
- flows/42265e/reports/retirement-result.md
- flows/42265e/vision/finding-out.md

### dea0ba
- flows/dea0ba/reports/knowledge-codex-candidate.md
- flows/dea0ba/vision/deterministicWork.md
- flows/dea0ba/vision/ethosLibrary.md
- flows/dea0ba/vision/hashes.md
- flows/dea0ba/vision/identifiers.md
- flows/dea0ba/vision/quotaTracking.md
- flows/dea0ba/vision/speakingToTheLiving.md
- flows/dea0ba/vision/systemPrompt.md
- flows/dea0ba/vision/titles.md

### edf227
- flows/edf227/reports/open-books.md
- flows/edf227/vision/bookTitles.md
- flows/edf227/vision/readingTheLiving.md

### f1c841
- flows/f1c841/log.md
- flows/f1c841/witnesses/succession.md

## Skipped: disk newer and larger (a flow already advanced it)
- flows/5578cc/log.md newer+larger disk=25594 abandoned=24712
- flows/5578cc/vision/behavior.md newer+larger disk=2327 abandoned=1435
- flows/6e782c/log.md newer+larger disk=3033 abandoned=2701
- flows/dea0ba/reports/deployment-investigation.md newer+larger disk=9723 abandoned=6612
- flows/edf227/log.md newer+larger disk=3361 abandoned=2627

## Skipped: disk identical to abandoned (26)
- flows/5578cc/books/answers-flow-ids.md
- flows/5578cc/books/answers-layers.md
- flows/5578cc/books/answers-on-flow-launch.md
- flows/5578cc/books/answers-three-questions.md
- flows/5578cc/books/find-out-and-keep-knowledge.md
- flows/5578cc/books/flow-ids-in-words.md
- flows/5578cc/books/how-flow-builds-a-prompt.md
- flows/5578cc/books/layers-not-models.md
- flows/5578cc/books/may-field-speak-to-psyche.md
- flows/5578cc/books/messages-to-fable-skill-line.md
- flows/5578cc/books/messages-to-fable-vision-flow.md
- flows/5578cc/notion/nexus.md
- flows/5578cc/notion/permissions.md
- flows/5578cc/notion/skills.md
- flows/5578cc/reports/decisions-2026-10-03.md
- flows/5578cc/vision/flashbook.md
- flows/5578cc/vision/flow.md
- flows/5578cc/vision/identifiers.md
- flows/5578cc/vision/knowledge.md
- flows/5578cc/vision/layers.md
- flows/5578cc/vision/locking.md
- flows/5578cc/vision/permissions.md
- flows/5578cc/vision/skills.md
- flows/5578cc/vision/vocabulary.md
- flows/5578cc/vision/writing.md
- flows/6e782c/vision/bookRendering.md

## Not restored
Nothing failed. Paths present only on disk (untracked in 64cf1b2edb4f) were not touched.
