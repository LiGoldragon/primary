# Orchestrate skill proposal -- curly-quoted reasons

The `orchestrate` skill (authored in `.claude/skills/orchestrate/SKILL.md`,
rendered into `.claude/skills/orchestrate/`) shows Lock request examples
without curly quotes around the reason. A reason with spaces must now be
curly-quoted.

## Current lines (verbatim)

```
    orchestrate 'Lock.{<name> <flow> [<absolute-path> ...] <reason>}'
```

```
Release by the returned integer ID using the Orchestrate release request skill variable, substituting the integer for <lock-id>. Read the typed reply.
```

## Proposed replacement lines

```
    orchestrate 'Lock.{ <name> <flow> [ <absolute-path> ... ] <reason> }'
```

(Spaced delimiters inside braces and brackets.)

Add after the Lock example:

```
A reason containing spaces or delimiter characters must be curly-quoted:
\u{201C}reason text\u{201D}. A single word is bare.
```

The Release line and the Observe line are correct as-is: `Release.<lock-id>`
and `Observe.Locks` have no reason field and no enclosures needing spacing.

## Also update the Orchestrate release request skill variable

Current value in `SKILL_VARIABLES.md`:

```
Orchestrate release request: Release.<lock-id>
```

This is correct and needs no change. `Release.442` is canonical bare datom.

## Sources

- `.claude/skills/orchestrate/SKILL.md` (current authored skill)
- `SKILL_VARIABLES.md` (current variable)
- Flow 6329f1 final witness (spaced-delimiter canonical output)
