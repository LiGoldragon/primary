# Who archives a record

## Context

A record is heard by one flow and lives in that flow's directory.
When a distillation of it lands in a skill, the record is replaced
and moves into an `archive-` file beside it. The skill says that it
moves; it does not say who moves it.

By the time the distillation lands, the flow that heard the record
is often retired. A rule of 2026-09-05
(`flows/e996e8/vision/editCoordination.md`) says only the flow that
has an id writes in its directory. Read that way, nobody may move a
retired flow's record. Past moves were all made by the distilling flow writing into other flows' directories, twice, in August and September.

Today's case: the inline-import statement landed in psyche-skills
`vision/ethos.md`. Its raw record is in
`flows/d5df1d/vision/ethos.md`. Flow d5df1d is retired and 081064
is its successor. The record is not archived.

Both skills involved are in production. This is a gap in a rule,
not a development branch.

```
 flows/d5df1d/vision/ethos.md
   record, in the heard flow's directory
            |
            v
 distillation lands in a skill
   (psyche-skills vision/ethos.md)
            |
            v
 flows/d5df1d/vision/archive-ethos.md
   archive- file beside the record
            ^
            |
   who writes this arrow?  (unnamed)
```

## Distillation

Target file, authored source:
`/git/github.com/LiGoldragon/mind-skills/skills/operation-psyche-distillation.md`

Topic of the statement: how a replaced record is archived. Lines 33
to 37 as they stand, with the added line marked:

Above, as it stands:

an intent- skill only on the living's explicit word. The raw records a distillation replaces move into an `archive-` prefixed file beside their source file.

Added:

```
+ The distilling flow moves the replaced
+ record into its archive- file, in
+ whichever flow's directory the record lives.
```

Below, as it stands:

A record's id is its originating session's short id and that session's own count.

Removed lines: none.

Impurities discarded: none.

Ruling asked:

1. Land as written.
2. The successor of the retired flow moves it.
3. Amend by line.

## Sources

e996e8 editCoordination
