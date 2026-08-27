# Flow 01a0439f — listener context

Read-only context recovery for parent flow 01a0439e.

Remembered: 04db2fd2, f426777b, 01a0193f, 019fe121, 012fbf07, 13cfc23f,
c6b71b4c — depth 1. The immediately prior design flow handled a long
speech-to-text monologue by splitting it into topic records; the standing
listener requirement is to keep recording available during one or more
transcriptions and never lose a transcript. Historical records show recurring
technical-name STT errors and explicit correction by the psyche.

Settled for this handoff: prior records establish expectations and failure
modes, not the cause of the current event. Cause remains with the parent
event/runtime investigations.

Open: whether the latest odd result was recognition, prompt/customization,
artifact selection, delivery, or transcript-display behavior.

Focused follow-up settled the local stage boundary: the known two-header
region is not at the three-request chunk join, whose delimiter is one space.
Its observed internal bytes are `\n\n    `. Prompt/customization, parser,
history, recall, and clipboard insertion paths have no matching source or
transformation; the earliest remaining candidate, if not spoken, is the
upstream response/model output. Per-request responses and audio semantics
remain unavailable.
