# Quotas

## 2026-09-14 — Balance Claude and Codex usage at about 14 percent a day so both meet at the end of the week; priority to core and primary; an accounting system

Context: "Sol" is Codex's high model as transcribed earlier this month.

> I want you to start working on a protocol for managing the quotas for the usage of both Claude and Codex, so that they are balanced and meet up at the end of the week if we use them at about 14% per day. We try to keep that rhythm.
>
> This would also drive the frequency of update of certain parts, with priority to the core and primary. It's better to agree on ideas and proof of concepts and things that we want to land directly from primary, which can then go to secondary to be implemented into production and at scale.
>
> We're going to have some kind of accounting system for these quotas. If Codex has not much usage, then Claude can start driving the proof of concept more with some Opus jobs, which are really good to manage, like an Opus main flow sub-job. If you want to make a big job out of it with a custom prompt, that makes it really good at knowing what it wants to do and doing a really good job. Opus 5 can do that really well. Also, it was kind of made as a response to Sol or whatever.
>
> Even small jobs can be driven by Sonnet on the Cloud side, and trivial jobs can go to Haiku or Sonnet. Sonnet is really good also and quite cheap.

-- psyche, STT.

## 2026-09-14 — Log context and tokens from the harness records, programmatically, without asking the agents

> Keep things flowing and try and figure out how you're going to log how much context and how many tokens of input and output are used by all the models, maybe if that's possible and if it's recorded in the harness. If we don't have to ask the agents to try and tell us, which I think is kind of wasteful, we could ballpark estimate from what we send and what some programmatic tool measuring thing (maybe one that already exists or that we can copy the patterns of)

-- psyche, STT.
