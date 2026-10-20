# References: A module's kind shows in its name on old tech

## Proposal 1 (psyche-context vision/context-modules.md)

- flows/d68c82/vision/context-modules.md — A colon between a context module's kind and its name (latest entry): colon between kind and name, visually clear, taught in basic training
- flows/d68c82/vision/context-modules.md — 2026-10-14, a separator between type and name: colon separates type from a hyphenated name; models trained to read it
- the living's comment on the second edition (relayed 2026-10-18): the name is the one old tech uses (directory name, file name, however the harness picks up the name); old tech does not support spaces, so the name is adapted to show the module's kind
- psyche-context origin main b938651, vision/context-modules.md lines 66 and 68 are the context lines
- the second edition's "On disk the kind stays the folder" line is dropped: line 66 already says the folder gives the type
- witnessed 2026-10-18 (Field, /tmp/colon-skill-live-20261018-6uxf9dy6/report.json): Claude Code 2.1.294 loads .claude/skills/vision:book; Codex 0.158.0-alpha.9 loads it
- figure redrawn: the second edition's figure mapped kind to folder and name to file, the dropped line

## Proposal 2 (psyche-context spirit/core.md)

- the living's comment on "Every flow learns in its basic training to read a name as kind:name": make that vision, do it rather than announce it
- Curriculum origin main 2ec2862, roles.datom: spirit-core and intent-context are in every role; src/startup.rs lines 125-126 refuse a startup without a spirit- and an intent- SYSTEM module; spirit/core.md is the only spirit module in psyche-context b938651, so spirit-core is the module every flow composes at start
- psyche-context b938651, spirit/core.md lines 23 and 25 are the context lines

## Removed from the second edition

- the living's comment on the curriculum-deploy proposal: code does not belong in a vision book; the Curriculum, curriculum-deploy and vocabulary proposals are dropped; implementation follows approval through the implementation cycle
