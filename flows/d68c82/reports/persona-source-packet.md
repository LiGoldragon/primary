# vision-persona source packet

Witnessed in a fresh clone of https://github.com/LiGoldragon/psyche-skills after `git fetch origin`.

## Hashes
- 7a6b13: 7a6b1304d16eae83352c58496d8bc77bd922a83f
- 82c92f: 82c92fad46018dfc79fb1c87ced757c4fdc8eeeb
- origin/main: 82c92fad46018dfc79fb1c87ced757c4fdc8eeeb (equals 82c92f)
- Both commits are ancestors of origin/main (merge-base --is-ancestor, both true).

## Parent chain
9fb0433dffe74a407fa879544290dbc7bde873f7 -> 7a6b1304d16eae83352c58496d8bc77bd922a83f -> 82c92fad46018dfc79fb1c87ced757c4fdc8eeeb

- 82c92f has parent 7a6b13; 7a6b13 has parent 9fb0433.
- `git merge-base --is-ancestor 9fb0433dffe74a407fa879544290dbc7bde873f7 82c92f` exits 0: 9fb0433 is an ancestor.
- `git log 9fb0433..82c92f` lists exactly those two commits.

## Authored path and blob
Path: skills/vision-persona.md (absent at 9fb0433)
- at 7a6b13: ee74e10fb9574e706c966e2b99ed7a1901c53262
- at 82c92f: 5240055e1abdcca5053581ea7d1de4d4e874ffa7

## Sources section
- At 82c92f: absent. The file is 12 lines, ending after "## What the root does"; no "Sources" appears anywhere in it.
- At 7a6b13: present, with lines `05c604 persona`, `6fb948 personaServiceAndNexusImagery-20260923`, `aa887c persona`.

## 82c92f commit message (verbatim)
```
vision-persona: the source references move to this message

05c604 persona
6fb948 personaServiceAndNexusImagery-20260923
aa887c persona

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01VdTYmnAT9CWXKJvmZqVSqt
```

7a6b13 message, for reference: subject `vision-persona: what the root does (approved 2026-10-10)`, then the same three reference lines and the same two trailers.

## Paths changed
- 7a6b13: A skills/vision-persona.md
- 82c92f: M skills/vision-persona.md (6 deletions: the blank line, the "## Sources" heading, a blank line, and the three reference lines)
