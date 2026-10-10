# Main-flow refresh correction

The authored source is the isolated branch
`/tmp/curriculum-main-flow-refresh`, based on `6dadae3`. Its Flow-refresh
paragraph now uses the approved distinction: lowercase `flow` is the running
entity and capital `Flow` is a position in the triad.

The final corrections are exactly these replacements:

- `if a newer flow already holds its flow` → `if a newer flow already holds its Flow`
- `; If this flow is at sixty percent` → `; if this flow is at sixty percent`
- `takes its predecessor's flow in the triad; the other flows are untouched` → `takes its predecessor's Flow in the triad; the other Flows are untouched`
- `which flows hold which places in the triad` → `which flows hold which Flows`

The earlier lowercase spelling came from the root-supplied approved paragraph;
the later explicit user correction is authoritative over it.

The native deployment command was:

`nix run .#generate-skills -- 'Generate.{ «/tmp/curriculum-main-flow-refresh» «/home/li/primary» }'`

It returned `Generated.{ 44 21 }`. The generated content diff is limited to
`.agents/skills/main-flow/SKILL.md` and `.claude/skills/main-flow/SKILL.md`.
The corresponding check returned `Checked.{ 44 21 }`.
