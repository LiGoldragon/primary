# Harness skills

## A skill whose body is one Claude block is an empty skill for Codex, taking up context

Context: the proposal put the whole web-report body inside
`{% if claude %}`.

> that doesn't work because then you'll create an empty skill for Codex, which will just take up context, telling him there's a skill there when there isn't.

-- psyche, STT.
