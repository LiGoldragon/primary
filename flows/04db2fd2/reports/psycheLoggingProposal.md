# Proposal: excerpt protocol for psyche logging (redraft)

## Problem

When the living speaks in a long monologue (especially speech-to-text), multiple vision entries are created across different topics. Each entry tends to reproduce the entire monologue text, duplicating it across every vision file touched. The original lives in the transcript; there is no preservation need served by repeating it everywhere.

## Where the recording protocol lives

The recording protocol belongs in **psyche-interraction.md**. It is the skill loaded when an agent directly converses with the psyche, and it already owns the "Logging" section and the "Preserving the psyche's words" section. That makes it the natural and only home for rules about how entries are formed, what they carry, and what they omit.

Other skills that mention recording do so in passing:

- **flows.md** (line 25-26): "A psyche record goes in `vision/<topic>.md`, the psyche's words verbatim." This is a placement rule (where records go), not a recording-format rule. It needs one clause added to defer to psyche-interraction for format.
- **psyche.md** (line 20): "Preserve the psyche's raw words." This is a principle about drift, not a format rule. No change needed.
- **psyche-acquisition.md** (line 15): "Use verbatim quotes." This governs how acquisition reports back to the caller, not how vision entries are recorded. No change needed.
- **psyche-distillation.md** (line 35-36): "A record's id is its originating session's short id and that session's own count." This is about record identity for distillation, not about entry format. No change needed.

## What a record carries

Per the psyche's rulings:
- No timestamps. The flow directory implies the session.
- No session id. The flow directory implies it.
- The provenance line carries only the input mode: `-- psyche, STT.` or `-- psyche, typed.`
- STT corrections are noted inline as `[STT: <corrected word>]`.

This matches how records are already written in flows/04db2fd2/vision/.

## Proposed changes

### 1. `Curriculum skills/psyche-interraction.md`

#### 1a. Remove timestamp and provenance-reconstruction rules

**Before** (lines 13-14):

```
Log rulings as they land. Each entry carries a timestamp.
Order each topic log oldest first, with the most recent entry last.
```

**After**:

```
Log rulings as they land.
Order each topic log oldest first, with the most recent entry last.
```

What this removes: "Each entry carries a timestamp." The psyche ruled no timestamps; the flow directory implies the session.

What this preserves: the log-as-they-land and ordering rules.

**Before** (line 19):

```
When reconstructing an entry, recover its exact words, source-event timestamp, and provenance from the originating transcript.
```

**After**:

```
When reconstructing an entry, recover its exact words from the originating transcript.
```

What this removes: "source-event timestamp, and provenance" from the reconstruction rule. There is no timestamp or provenance to recover.

What this preserves: the duty to recover exact words from the transcript.

#### 1b. Add excerpt rule and provenance line

**Before** (lines 30-34):

```
### Preserving the psyche's words

Use verbatim quotes for the psyche's words. Agent context — what
prompted the ruling, what it answers — is kept brief and clearly
separate from the quoted words.
```

**After**:

```
### Preserving the psyche's words

Use verbatim quotes for the psyche's words. Agent context — what
prompted the ruling, what it answers — is kept brief and clearly
separate from the quoted words.

When one message yields entries across several topics, each entry
quotes only the words relevant to it. Omitted stretches within a
quote are marked ` ... `.

Each entry ends with a provenance line: `-- psyche, STT.` or
`-- psyche, typed.`
```

What this preserves: the existing "verbatim quotes" rule. The psyche's words are never paraphrased. "Verbatim" means the quoted fragments are exact, not that the entire message is reproduced.

What this adds: the excerpt rule (quote only the relevant parts), the ellipsis convention (` ... ` for omissions), and the provenance-line format (input mode only, no timestamp or session id).

### 2. `Curriculum skills/flows.md`, lines 25-26

**Before**:

```
A psyche record goes in `vision/<topic>.md`, the psyche's words
verbatim.
```

**After**:

```
A psyche record goes in `vision/<topic>.md`, per the recording
protocol in the psyche-interraction skill.
```

What this preserves: the placement rule (where records go).

What this changes: replaces "the psyche's words verbatim" -- which could be read as requiring whole-message reproduction -- with a pointer to the single home of the recording protocol. The verbatim rule, excerpt rule, and provenance format all live in psyche-interraction.

### 3. No change to `Curriculum skills/psyche.md`

Lines 20-21: "Preserve the psyche's raw words. Do not paraphrase without the psyche reviewing the result." This is a drift-prevention principle, not a format rule. Excerpting with ellipsis is not paraphrase. No change needed.

### 4. No change to `Curriculum skills/psyche-acquisition.md`

Line 15: "Use verbatim quotes." This governs how acquisition reports to the caller, not how vision entries are recorded. No change needed.

### 5. No change to `Curriculum skills/psyche-distillation.md`

Lines 35-36: "A record's id is its originating session's short id and that session's own count." This is about record identity for distillation. The removal of timestamps from entries does not affect record ids. No change needed.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-interraction.md` (lines 8-45, the logging and preserving-words protocol)
- `/git/github.com/LiGoldragon/Curriculum/skills/flows.md` (lines 25-26, psyche record placement)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche.md` (lines 20-21, raw-words principle; line 55, topic/heading definition)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-acquisition.md` (line 15, verbatim quotes in reports)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-distillation.md` (lines 20-21, archived originals; lines 35-36, record ids)
- `/home/li/primary/flows/04db2fd2/vision/psycheLogging.md` (psyche rulings: excerpt rule, no timestamps, no session id, single-skill home)
- `/home/li/primary/flows/04db2fd2/vision/anatomy.md` (example of current entry format with `-- psyche, STT.`)
- `/home/li/primary/flows/04db2fd2/vision/datomMaps.md` (example of current entry format)
- `/home/li/primary/flows/01a03d6e/vision/flows.md` (example of old verbose provenance format, now superseded)
