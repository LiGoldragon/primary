# 1 - Nota designer protocol adoption and lane gap

## Load-bearing state

The active role for this thread is now `nota-designer`.
Operationally, this is a designer-specialist lane focused on NOTA
notation, grammar, human authoring ergonomics, codec contracts, and
the reports that make operator implementation unambiguous.

The `nota-designer` discipline is therefore the designing protocol:
intent first, durable design substance in reports, operator-facing
implementation work through explicit handoff, and no direct
implementation while acting in this role.

## NOTA quoting correction

Spirit records 66 and 67 captured the new NOTA string correction:
normal square-bracket string examples should avoid double quotes
inside the string. The example is:

```nota
[he said 'yes']
```

not:

```nota
[he said "yes"]
```

The reason is now load-bearing. The square-bracket string redesign is
not only a prettier string delimiter; it lets authored inline NOTA
fit naturally inside shell double quotes. Normal NOTA examples should
discourage `"` so the outer command can use `"` without fighting the
message's own string syntax.

The current bracket-string design premise I am carrying forward:

- Plain `[ ... ]` is the candidate ordinary string form.
- `[| ... |]` is the candidate indented multiline block-string form.
- The block form strips common indentation after parsing.
- Authored prose inside ordinary bracket strings should prefer
  apostrophes where natural, as in `[he said 'yes']`.

## Protocol changes adopted

The recent role-protocol changes I read and am adopting:

- `reports/designer/264-designing-protocol-and-role-spaces.md`:
  the role label drives protocol. A designer-labeled conversation is a
  shaping conversation, not an implementation conversation.
- `reports/designer/264-designing-protocol-and-role-spaces.md`:
  the designer is the bridge from psyche prompt to intent, report, and
  operator handoff. The operator remains on the implementation side.
- `AGENTS.md`: the current workspace contract now names the designer
  protocol as special. Inside this harness, there is one active
  limitation: the external Codex tool contract still forbids spawning
  subagents unless the psyche explicitly asks for subagents, so this
  `nota-designer` instance will not dispatch subagents by default.
- `orchestrate/ARCHITECTURE.md`: current lane files are transitional;
  the destination is typed role state in the future orchestration
  component, with runtime role or lane registration.
- `skills/role-lanes.md`: a lane shares its main role's discipline and
  skill file; only the lock filename, report subdirectory, and claim
  string are lane-specific.

## Current lane gap

`nota-designer` is not yet a first-class orchestration lane.

The current helper is not fully dynamic. `tools/orchestrate` is a shim
to the Rust `orchestrate-cli`; that CLI reads `orchestrate/roles.list`,
but it then validates every lane token against a closed Rust `Lane`
enum and projects each lane onto `signal-persona-orchestrate::RoleName`.

Consequence: adding only this line to `orchestrate/roles.list` would
not be enough:

```text
nota-designer                  assistant-of:designer
```

The helper would fail with the built-in "lane appears in registry but
is missing from the closed Lane enum" error until the Rust enum and
signal contract are updated, or until the helper is changed to a truly
runtime registry.

## Provisional operating rule

Until the lane is registered in the tooling, I will operate as
`nota-designer` in substance:

- write NOTA design reports under `reports/nota-designer/`;
- treat NOTA grammar, notation, examples, and codec-contract shape as
  the active design surface;
- use designer discipline for shared guidance and protocol questions;
- avoid claiming `nota-designer` through `tools/orchestrate`, because
  the helper cannot accept that lane today.

For shared guidance edits that need a lock, the existing practical
claim lane is still `designer`. A true first-class `nota-designer`
lane requires an operator-facing implementation task to either expand
the closed lane enum and signal projection or complete the dynamic
lane-registry direction already sketched in the orchestration
architecture.
