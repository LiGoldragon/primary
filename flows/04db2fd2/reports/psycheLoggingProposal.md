# Proposal: excerpt protocol for psyche logging

## Problem

When the living speaks in a long monologue (especially speech-to-text), multiple vision entries are created across different topics. Currently, each entry tends to reproduce the entire monologue text. This duplicates the full text across every vision file touched, making logs unwieldy, noisy on recovery, and hard to read.

The original monologue lives in the transcript. There is no preservation need served by repeating it in every entry.

## Proposed changes

### 1. `Curriculum skills/psyche-interraction.md`, section "Preserving the psyche's words"

This is the primary logging protocol. The change adds the excerpt rule below the existing verbatim-quotes line.

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
quote are marked ` ... `. The entry's provenance line names the
transcript (session short id and source-event timestamp) so the
full original is always reachable.
```

What this preserves: the existing "verbatim quotes" rule stands. The psyche's words are never paraphrased. The word "verbatim" continues to mean the quoted fragments are the psyche's exact words, not that the entire message is reproduced.

What this adds: the excerpt rule (quote only the relevant parts), the ellipsis convention (` ... ` for omissions), and the provenance requirement (transcript pointer so the original is always reachable).

What this removes: the implicit practice of copying an entire monologue into every topic entry that comes from it.

### 2. `Curriculum skills/flows.md`, line 25-26

This line currently says "the psyche's words verbatim" without qualification. It could be read as requiring the whole message. It needs the same narrowing.

**Before** (lines 25-26):

```
A psyche record goes in `vision/<topic>.md`, the psyche's words
verbatim.
```

**After**:

```
A psyche record goes in `vision/<topic>.md`, the psyche's words
verbatim, excerpted to the parts relevant to that entry when the
source message covers more than one topic.
```

What this preserves: "the psyche's words verbatim" still means the quoted text is exact.

What this changes: makes explicit that "verbatim" means the quoted fragments are exact, not that the whole message is copied.

### 3. No change to `Curriculum skills/psyche.md`

Lines 20-21 say: "Every rephrasing compounds the drift. Preserve the psyche's raw words. Do not paraphrase without the psyche reviewing the result."

This does not conflict. It forbids paraphrase; excerpting with ellipsis is not paraphrase. The words that appear are still the psyche's raw words. No change needed.

### 4. No change to `Curriculum skills/psyche-acquisition.md`

Line 14 says: "Use verbatim quotes." This is about how acquisition reports back to the caller, not about how vision entries are recorded. The excerpt protocol applies to logging (psyche-interraction), not acquisition reporting. No change needed.

## Conflict analysis

The phrase "the psyche's words verbatim" in `flows.md` is the only text that could be read as requiring whole-message reproduction. The proposed edit resolves this by making the excerpt intent explicit while keeping the verbatim guarantee for the words that do appear.

The psyche-distillation skill says "The archived originals keep every original word." This refers to archived raw records, not to the initial logging of entries. No conflict.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-interraction.md` (lines 30-45, the logging protocol)
- `/git/github.com/LiGoldragon/Curriculum/skills/flows.md` (lines 25-26, psyche record placement)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche.md` (lines 20-21, raw-words principle)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-acquisition.md` (line 14, verbatim quotes in reports)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-distillation.md` (line 21, archived originals)
- `/home/li/primary/flows/06196cc7/vision/psycheLogStructure.md` (prior psyche rulings on record structure)
- `/home/li/primary/flows/b675f3d9/vision/distillation.md` (placement ruling)
- `/home/li/primary/flows/01a04336/vision/remoteFlag.md` (example of current entry format)
- `/home/li/primary/flows/01a03d6e/vision/flows.md` (example of current provenance format)
