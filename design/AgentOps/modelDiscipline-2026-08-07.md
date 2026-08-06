# Model Discipline — 2026-08-07

Rulings from the psyche during the Protos vision-reacquisition session,
after a Fable subagent was spawned by mistake and stopped.

## Ruling: Claude subagents are 4.6-generation only; Fable never

Psyche: Fable must never run as a subagent ("I really cannot afford for
you to use Fable for sub-agents"), and the guard must be harness-
enforced. Revision: a hard deny "will create a failure, which will
poison context and waste tokens and money" — the mechanism must SET a
default model instead of refusing.

Psyche on tiers: "We always use 4.6. Sonnet would default to 5, which
is not what we want. Sonnet 5 and Opus 5 are bad models. Claude
degenerated their models after 4.6, other than Fable, which is a
different class" (possibly different pre-training).

Consequences: the PreToolUse guard on the Agent tool rewrites
Fable-bound and unpinned calls to the 4.6 ordinary tier; the eight role
agents (read/write × trivial/ordinary/demanding/critical) remain the
preferred spawning surface, pinning claude-haiku-4-5 /
claude-sonnet-4-6 / claude-opus-4-6[1m]. Sonnet 5 and Opus 5 are not
used.

## Ruling: Codex subagent defaults for the fresh session

Psyche: Codex's startup prompt must tell him "to never use GPT 5.6 Sol
for subagents and to default to Luna extra high thinking or to use the
built-in roles that we have made."

Note: NON_IDEAL_AGENTS.md (2026-08-06) says gpt-5.6-terra xhigh for
every non-trivial subagent, luna only for trivial mechanical ones. The
luna-xhigh default stated today overlaps that line; recency favors
luna-xhigh as the default, with the role built-ins as the alternative.
Flagged to the psyche for explicit confirmation before
NON_IDEAL_AGENTS.md itself is edited.
