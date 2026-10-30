# Flow Configuration changes witnessed today

**Report kind:** machine audit report; not a psyche record.

**Current snapshot:** `flow-meta Configuration` read at `2026-10-29T16:56:37-06:00`; raw receipt `/tmp/config-current-report.datom` (16,464 bytes). This report prints module declarations and other nonsecret metaflow fields. It intentionally omits the Nexus paths/socket configuration and send-server paths.

## Evidence boundary

The first retained live snapshot in this hand is `/tmp/flow-config-before.datom`, read at 2026-10-29 15:59:53 -0600. The history below is complete for live Configuration differences witnessed by this hand from that snapshot through the current read. It does **not** prove that no other live Configuration change happened earlier today or through another hand. Where a direct `Configured.*` response was not retained as an artifact, the report says so and relies only on the before/query/after reads actually retained.

Source commits prove authored source, not live mutation. A later Configuration read proves the live state by that later read, not the exact instant or actor of an intervening change.

## Live changes witnessed

### 15:59–16:00 — Psyche core Primary declaration

- Field: `Metaflows`.
- Before read: `/tmp/flow-config-before.datom` (15:59:53).
- Whole-vector request: `/tmp/configure-metaflows-query.datom` (16:00:06).
- After read: `/tmp/flow-config-after.datom` (16:00:10).
- Direct `Configured.*` response artifact: not retained.
- Authored source: CriomOS-home `c1a0b09816128a87e5f1e6c9af3c72c08bf53119`.

**Before**

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction vision:ethos vision:datom vision:remembering vision:model-roles vision:proposal intent:energy ] [] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

### 16:02–16:03 — settled module audit, row by row

- Field: `Metaflows`.
- Before reads: `/tmp/flow-config-audit-before.datom` (16:02:41) and unchanged recheck `/tmp/flow-config-audit-fresh.datom` (16:03:33).
- Whole-vector request: `/tmp/configure-all-settled.datom` (16:03:33).
- After read: `/tmp/flow-config-audit-after.datom` (16:03:38).
- Direct `Configured.*` response artifact: not retained.
- Authored source matching the after rows: CriomOS-home `93bceceb497070c4ba207f9041bce4df16d3ff68`.
- Fields other than system modules and user modules stayed byte-for-byte the same in each changed row. Publishing rows retained their book modules; settled nonpublishing rows lost book/presentation modules and gained `knowledge:flow` and `knowledge:beads`; Psyche flow also received its settled topic vision.

#### `Field core Primary`

**Before**

```datom
{ { Field core Primary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Field core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Field core Secondary`

**Before**

```datom
{ { Field core Secondary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Field core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Field flow Secondary`

**Before**

```datom
{ { Field flow Secondary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Field flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Mind core Primary`

**Before**

```datom
{ { Mind core Primary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Mind core Secondary`

**Before**

```datom
{ { Mind core Secondary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Mind flow Primary`

**Before**

```datom
{ { Mind flow Primary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Mind flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Mind flow Secondary`

**Before**

```datom
{ { Mind flow Secondary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Mind flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Psyche book Tertiary`

**Before**

```datom
{ { Psyche book Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:book-publishing-procedure vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche book Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:book-publishing-procedure vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Psyche core Quaternary`

**Before**

```datom
{ { Psyche core Quaternary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Quaternary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Psyche core Secondary`

**Before**

```datom
{ { Psyche core Secondary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom vision:proposal intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom vision:proposal intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Psyche core Tertiary`

**Before**

```datom
{ { Psyche core Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Tertiary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Psyche flow Primary`

**Before**

```datom
{ { Psyche flow Primary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:subflows vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Psyche flow Secondary`

**Before**

```datom
{ { Psyche flow Secondary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:subflows vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Psyche records Secondary`

**Before**

```datom
{ { Psyche records Secondary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche records Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

#### `Psyche research Primary`

**Before**

```datom
{ { Psyche research Primary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:fable intent:belief-modules vision:book vision:psyche-aspect compensation:book-making compensation:messaging ] [ compensation:correction ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche research Primary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:fable intent:belief-modules vision:psyche-aspect compensation:messaging ] [ compensation:correction knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

#### `Psyche research Secondary`

**Before**

```datom
{ { Psyche research Secondary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:belief-modules vision:book vision:psyche-aspect compensation:book-making compensation:messaging ] [ compensation:correction ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche research Secondary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:belief-modules vision:psyche-aspect compensation:messaging ] [ compensation:correction knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### 16:19 — Psyche Obsidian declarations

- Field: `Metaflows`; each address was absent in `/tmp/flow-config-final.datom` (16:04:56).
- Whole-vector request: `/tmp/obsidian-configure.datom` (16:19:25).
- A later live read `/tmp/config-before-obsidian.datom` (16:34:05) contains both rows.
- Direct `Configured.*` response artifact: not retained.
- Authored source: CriomOS-home `7c4bee33cab48a55802ca565a3d0b454a17acede`.

#### `Psyche obsidian Primary`

**Before:** absent.

**After**

```datom
{ { Psyche obsidian Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

#### `Psyche obsidian Secondary`

**Before:** absent.

**After**

```datom
{ { Psyche obsidian Secondary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

### 16:25 — Fable refresh threshold

- Field: `Thresholds`.
- Whole-vector request: `/tmp/threshold-configure.datom` (16:25:18).
- Direct `Configured.*` response artifact: not retained.
- Before is in `/tmp/flow-config-final.datom`; after is in `/tmp/config-before-obsidian.datom`.
- Authored source: CriomOS-home `b7a6788d8cc13fce3f3eb4a40d4d7e90f70b5d0c`.

**Before:** `{ claude-fable-5-1 200000 }`

**After:** `{ claude-fable-5-1 280000 }`

No refresh execution event is claimed; this is configuration state.

### 16:30–16:34 — Psyche core Primary routing vision

- Field: `Metaflows`, user modules.
- `vision:aspects` and `vision:messaging` were inserted after `vision:collaboration`; no other row field changed.
- There is no isolated meta request/reply artifact for this mutation. The retained earlier row is in `/tmp/flow-config-final.datom`; the retained later row is in `/tmp/config-before-obsidian.datom`.
- Authored source: CriomOS-home `636fe46e3566cd884319ce7a692302fccf22a45b`.

**Before**

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration vision:aspects vision:messaging knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

### 16:36 — Mind Obsidian declarations and Codex leave-outs

- Fields: `Metaflows` and `LeaveOuts`.
- Fresh before and unchanged recheck: `/tmp/config-fresh-obsidian.datom` (16:36:00) and `/tmp/config-recheck-obsidian.datom` (16:36:15).
- Requests: `/tmp/configure-mf-obsidian.datom` and `/tmp/configure-lo-obsidian.datom`.
- Direct replies witnessed in this hand: `Configured.Replaced` for `Metaflows`; `Configured.Replaced` for `LeaveOuts`.
- After read: `/tmp/config-after-obsidian.datom` (16:36:16).
- Authored source: CriomOS-home `c3b793249aed5783ba07ff9f5054bd0dd3babd9e`.

#### `Mind obsidian Primary` metaflow

**Before:** absent.

**After**

```datom
{ { Mind obsidian Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts ] Regular Default Maintained «» [] }
```

#### `Mind obsidian Primary` leave-out

**Before:** absent.

**After**

```datom
{ { Mind obsidian Primary } Codex [ CodexAgentsMd CodexSkillListing CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions ] }
```

#### `Mind obsidian Secondary` metaflow

**Before:** absent.

**After**

```datom
{ { Mind obsidian Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts ] Regular Default Maintained «» [] }
```

#### `Mind obsidian Secondary` leave-out

**Before:** absent.

**After**

```datom
{ { Mind obsidian Secondary } Codex [ CodexAgentsMd CodexSkillListing CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions ] }
```

## Source changes that are not live Configuration evidence

- CriomOS-home `c1a0b09816128a87e5f1e6c9af3c72c08bf53119` also removed `FLOW_CORE_PRESENTATION_PROMPT=/home/li/primary/flows/9ef2c5/prompts/presentation-maker.md` from `modules/home/profiles/min/flow.nix`. That is source evidence only. An earlier retained observation of the still-running transient `flow-nexus-040.service` found `FLOW_CORE_PRESENTATION_PROMPT=/home/li/primary/flows/e3c8c1/presentation-role.md`; no authorized restart or supported environment-clean operation occurred. Therefore this report does not claim the live environment variable absent.
- No Artifact tool mutation was made. The metaflow `ToolSet` values of existing rows remained unchanged; the newly declared rows copied `Default`. Adding the Mind Obsidian Codex leave-outs copied existing Codex prompt-section leave-outs and did not change tool availability.

## Exact current Psyche core Primary row

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration vision:aspects vision:messaging knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

## Current model mapping and thresholds

Model mapping is separate from each metaflow declaration.

```datom
{ Primary Field gpt-6-astra }
{ Primary Mind gpt-6-astra }
{ Primary Psyche claude-fable-5-1 }
{ Quaternary Field gpt-6-luna }
{ Quaternary Mind gpt-6-luna }
{ Quaternary Psyche claude-haiku-5-5 }
{ Secondary Field gpt-6.1-sol }
{ Secondary Mind gpt-6.1-sol }
{ Secondary Psyche claude-opus-5-5 }
{ Tertiary Field gpt-6-luna }
{ Tertiary Mind gpt-6-luna }
{ Tertiary Psyche claude-sonnet-5-5 }
```

```datom
{ claude-fable-5-1 280000 }
{ claude-haiku-5-5 200000 }
{ claude-opus-5-5 200000 }
{ claude-sonnet-5-5 200000 }
{ gpt-5.6-luna 150000 }
{ gpt-5.6-sol 150000 }
{ gpt-6-astra 150000 }
{ gpt-6-luna 150000 }
{ gpt-6-sol 150000 }
{ gpt-6.1-sol 150000 }
```

## Current served declaration of every metaflow

These are the complete metaflow rows from the 16:56:37 live Configuration read. Each row is `Address`, system-module vector, user-module vector, flow kind, tool set, continuity, purpose, records.

### `Field core Primary`

```datom
{ { Field core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Field core Secondary`

```datom
{ { Field core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Field core Tertiary`

```datom
{ { Field core Tertiary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

### `Field flow Secondary`

```datom
{ { Field flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Field publisher Quaternary`

```datom
{ { Field publisher Quaternary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

### `Mind core Primary`

```datom
{ { Mind core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Mind core Secondary`

```datom
{ { Mind core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Mind core Tertiary`

```datom
{ { Mind core Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

### `Mind flow Primary`

```datom
{ { Mind flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Mind flow Secondary`

```datom
{ { Mind flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Mind obsidian Primary`

```datom
{ { Mind obsidian Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts ] Regular Default Maintained «» [] }
```

### `Mind obsidian Secondary`

```datom
{ { Mind obsidian Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts ] Regular Default Maintained «» [] }
```

### `Psyche book Tertiary`

```datom
{ { Psyche book Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:book-publishing-procedure vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Psyche core Primary`

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration vision:aspects vision:messaging knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

### `Psyche core Quaternary`

```datom
{ { Psyche core Quaternary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Psyche core Secondary`

```datom
{ { Psyche core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom vision:proposal intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Psyche core Tertiary`

```datom
{ { Psyche core Tertiary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Psyche flow Primary`

```datom
{ { Psyche flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Psyche flow Secondary`

```datom
{ { Psyche flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Psyche test Quaternary`

```datom
{ { Psyche test Quaternary } [ spirit:core spirit:ghost intent:models vision:ethos vision:datom ] [] Regular Default OnDemand «» [] }
```

### `Psyche records Secondary`

```datom
{ { Psyche records Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

### `Psyche obsidian Primary`

```datom
{ { Psyche obsidian Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

### `Psyche obsidian Secondary`

```datom
{ { Psyche obsidian Secondary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

### `Psyche research Primary`

```datom
{ { Psyche research Primary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:fable intent:belief-modules vision:psyche-aspect compensation:messaging ] [ compensation:correction knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

### `Psyche research Secondary`

```datom
{ { Psyche research Secondary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:belief-modules vision:psyche-aspect compensation:messaging ] [ compensation:correction knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

## Completeness gaps

- No retained pre-15:59 live snapshot or complete meta-operation ledger was available to this hand, so earlier-today live changes are unrecovered rather than inferred.
- Direct `Configured.*` reply text was not retained for the 16:00, 16:03, 16:19, 16:25, or 16:30 operations. Their before/query/after and source evidence is identified above. The two 16:36 replies were witnessed exactly.
- The current read proves current declarations, model mapping, thresholds and leave-outs. It does not prove that already-running flows reloaded changed modules, that a threshold-triggered refresh occurred, or that a source-only environment edit reached the running service.
- Source commit dates and the retained file timestamps are today (2026-10-29). No claim is made about changes outside this evidence window.

