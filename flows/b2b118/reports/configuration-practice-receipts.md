# Configuration practice row receipts

- Initial live read: `2026-10-29T17:04:09-06:00`, `/tmp/practice-before.datom`.
- Exact fresh rechecks preceded both replacements.
- First whole-vector reply: `Configured.Replaced`.
- Amendment whole-vector reply: `Configured.Replaced`.
- Final live read: `2026-10-29T17:04:55-06:00`, `configuration-practice-after.datom`.
- Final exact-byte SHA-256 (including one trailing LF): `3d4ad16219a29f1d0f4b9beea4b3031a1e60a8c97cc780a8cac732cb6d8f81e9`.
- Authored source: CriomOS-home `c97ff0ff161bfce080c0ada6dcc941e192a2905a`.

## `Field core Primary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Field core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Field core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

## `Field core Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Field core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Field core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

## `Field core Tertiary`

- Changes: system +`intent:energy`; system -`vision:book`; user +`knowledge:flow`; user +`knowledge:beads`.

**Before**

```datom
{ { Field core Tertiary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Field core Tertiary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

## `Field flow Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Field flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Field flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads vision:account ] Regular Default OnDemand «» [] }
```

## `Field publisher Quaternary`

- Changes: system +`intent:energy`.

**Before**

```datom
{ { Field publisher Quaternary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Field publisher Quaternary } [ intent:context vision:book spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default OnDemand «» [] }
```

## `Mind core Primary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Mind core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind core Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

## `Mind core Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Mind core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

## `Mind core Tertiary`

- Changes: system +`intent:energy`; system -`vision:book`; system -`compensation:book-crystallization`; user +`knowledge:flow`; user +`knowledge:beads`.

**Before**

```datom
{ { Mind core Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind core Tertiary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

## `Mind flow Primary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Mind flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Mind flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads vision:account ] Regular Default OnDemand «» [] }
```

## `Mind flow Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Mind flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Mind flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:flow vision:subflows knowledge:flow knowledge:beads vision:account ] Regular Default OnDemand «» [] }
```

## `Mind obsidian Primary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Mind obsidian Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind obsidian Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts vision:account ] Regular Default Maintained «» [] }
```

## `Mind obsidian Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Mind obsidian Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Mind obsidian Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads vision:proposal vision:book knowledge:obsidian-sync knowledge:obsidian-comments knowledge:obsidian-self-hosted-sync knowledge:obsidian-app knowledge:obsidian-hosts vision:account ] Regular Default Maintained «» [] }
```

## `Psyche book Tertiary`

- Changes: system +`intent:energy`; system -`vision:ethos`; system -`vision:datom`; user -`compensation:behavior`; user -`compensation:correction`; user -`knowledge:orchestrate`; user -`knowledge:protos`; user -`knowledge:datom`.

**Before**

```datom
{ { Psyche book Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:book-publishing-procedure vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche book Tertiary } [ intent:context vision:book compensation:book-crystallization spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:book-publishing-procedure intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization vision:aspects vision:model-roles vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

## `Psyche core Primary`

- Changes: system +`intent:fable`; user +`vision:account`.

**Before**

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration vision:aspects vision:messaging knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:belief-modules intent:fable ] [ vision:remembering vision:model-roles vision:crystallization vision:proposal vision:psyche vision:belief-modules vision:collaboration vision:aspects vision:messaging knowledge:flow knowledge:beads knowledge:psyche vision:account ] Regular Default Maintained «» [] }
```

## `Psyche core Quaternary`

- Changes: system +`intent:energy`; system -`vision:ethos`; system -`vision:datom`; user -`compensation:behavior`; user -`compensation:correction`; user -`knowledge:orchestrate`; user -`knowledge:protos`; user -`knowledge:datom`.

**Before**

```datom
{ { Psyche core Quaternary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Quaternary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization vision:aspects vision:model-roles vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

## `Psyche core Secondary`

- Changes: system -`vision:criomos`; system -`vision:ethos`; system -`vision:datom`; user +`vision:account`; user -`compensation:behavior`; user -`compensation:correction`; user -`knowledge:orchestrate`; user -`knowledge:protos`; user -`knowledge:datom`.

**Before**

```datom
{ { Psyche core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom vision:proposal intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:proposal intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization vision:aspects vision:model-roles vision:messaging knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

## `Psyche core Tertiary`

- Changes: system +`intent:energy`; system -`vision:ethos`; system -`vision:datom`; user -`compensation:behavior`; user -`compensation:correction`; user -`knowledge:orchestrate`; user -`knowledge:protos`; user -`knowledge:datom`.

**Before**

```datom
{ { Psyche core Tertiary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche core Tertiary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models role:psyche-core-tertiary intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization vision:aspects vision:model-roles vision:messaging knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

## `Psyche flow Primary`

- Changes: system +`intent:energy`; system +`intent:fable`; user +`vision:account`.

**Before**

```datom
{ { Psyche flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche flow Primary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom intent:energy intent:fable ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads vision:account ] Regular Default OnDemand «» [] }
```

## `Psyche flow Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Psyche flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche flow Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:flow vision:nexus vision:signal vision:ethos vision:datom intent:energy ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging vision:remembering knowledge:flow knowledge:beads vision:account ] Regular Default OnDemand «» [] }
```

## `Psyche test Quaternary`

- Changes: system +`intent:energy`; user +`knowledge:flow`; user +`knowledge:beads`.

**Before**

```datom
{ { Psyche test Quaternary } [ spirit:core spirit:ghost intent:models vision:ethos vision:datom ] [] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche test Quaternary } [ spirit:core spirit:ghost intent:models vision:ethos vision:datom intent:energy ] [ knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

## `Psyche records Secondary`

- Changes: system +`intent:energy`; system -`vision:criomos`; system -`vision:ethos`; system -`vision:datom`; user +`vision:account`; user -`compensation:behavior`; user -`compensation:correction`; user -`knowledge:orchestrate`; user -`knowledge:protos`; user -`knowledge:datom`.

**Before**

```datom
{ { Psyche records Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models vision:criomos vision:ethos vision:datom ] [ compensation:behavior compensation:correction knowledge:vocabulary knowledge:psyche vision:crystallization knowledge:orchestrate vision:aspects vision:model-roles knowledge:protos knowledge:datom vision:messaging knowledge:flow knowledge:beads ] Regular Default OnDemand «» [] }
```

**After**

```datom
{ { Psyche records Secondary } [ intent:context spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:design intent:models intent:energy ] [ knowledge:vocabulary knowledge:psyche vision:crystallization vision:aspects vision:model-roles vision:messaging knowledge:flow knowledge:beads vision:account ] Regular Default OnDemand «» [] }
```

## `Psyche obsidian Primary`

- Changes: system +`intent:fable`; user +`vision:account`.

**Before**

```datom
{ { Psyche obsidian Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche obsidian Primary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy intent:fable ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche vision:account ] Regular Default Maintained «» [] }
```

## `Psyche obsidian Secondary`

- Changes: user +`vision:account`.

**Before**

```datom
{ { Psyche obsidian Secondary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche obsidian Secondary } [ spirit:core spirit:ghost intent:context intent:design intent:main-flow intent:models intent:psyche intent:living-interaction intent:energy ] [ vision:proposal vision:book vision:psyche vision:collaboration vision:crystallization knowledge:flow knowledge:beads knowledge:psyche vision:account ] Regular Default Maintained «» [] }
```

## `Psyche research Primary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Psyche research Primary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:fable intent:belief-modules vision:psyche-aspect compensation:messaging ] [ compensation:correction knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche research Primary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:fable intent:belief-modules vision:psyche-aspect compensation:messaging intent:energy ] [ compensation:correction knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

## `Psyche research Secondary`

- Changes: system +`intent:energy`; user +`vision:account`.

**Before**

```datom
{ { Psyche research Secondary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:belief-modules vision:psyche-aspect compensation:messaging ] [ compensation:correction knowledge:flow knowledge:beads ] Regular Default Maintained «» [] }
```

**After**

```datom
{ { Psyche research Secondary } [ spirit:core spirit:ghost intent:main-flow intent:living-interaction intent:psyche intent:belief-modules vision:psyche-aspect compensation:messaging intent:energy ] [ compensation:correction knowledge:flow knowledge:beads vision:account ] Regular Default Maintained «» [] }
```

