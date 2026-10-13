---
description: The authored context-module kinds, template syntax or loading metadata are needed.
dependencies: []
---

A module's prefix names its kind: `spirit-`, `vision-`, `intent-`,
`knowledge-`, `inquiry-` or `compensation-`.
Psyche owns spirit, vision and intent; these change only on the living's word.
Mind owns knowledge of verified contracts and inquiry methods.
Field owns compensation for behavior the system does not yet provide;
its owners change it without the living's review.
The operation and trial kinds are retired.

Target-specific text in a flat source uses `{% if claude %}`, `{% if codex %}`, or `{% if pi %}`, with `{% else %}` and `{% endif %}` alone on their lines; every other character is literal skill content.

`user-only: true` — the skill enters only through the user prompt or a
launcher's first turn; the flow cannot load it. It deploys as
`disable-model-invocation: true` in Claude Code, and in Codex as a policy
sidecar beside the skill that withholds it from the skills catalog.

A role skill carries an aspect's identity and names its
dependencies. Mark role skills user-only.

A skill's reasoning and concepts live in a parallel <skill>-rationale skill, loaded by psyche-facing flows only.
