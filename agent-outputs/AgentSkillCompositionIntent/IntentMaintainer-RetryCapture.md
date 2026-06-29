# Intent Maintainer Retry Capture

## Task and scope

Retry Spirit capture for the latest psyche utterances about agent/skill composition, early context, output quality, and work quality. The prior attempt was rejected because testimony used third-person paraphrases. This pass used only verbatim psyche wording in Spirit testimony.

## Files, doctrine, and commands consulted

- `AGENTS.md` workspace boot contract, via supplied project context.
- `INTENT.md` current workspace intent surface.
- `.agents/skills/spirit-cli/SKILL.md` for deployed Spirit CLI rules.
- `.agents/skills/intent-log/SKILL.md` for conservative capture and testimony discipline.
- `.agents/skills/intent-maintenance/SKILL.md` for duplicate/maintenance classification.
- `/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema` for the current deployed `Testimony` shape: a vector of `VerbatimQuote { QuoteText OptionalAntecedent }` plus `Reasoning`.
- Existing neighborhood queried with `PublicTextSearch` for `early context`, `agent skills`, `quality output`, `trained agents`, `role packets self-contained training`, `quality`, and `bad work redo efficiency`.

## Classification

- Utterance 1 is durable universal agent-system direction: compose with specifically trained one-task agents rather than agents loading skills on the fly.
- Utterance 2 is durable universal work principle: bad quality forces redo and destroys efficiency.
- Utterance 3 is durable universal agent-workflow principle: maximize early context and scenario-specific skill/agents for output quality because long contexts degrade agents.
- Utterance 4 explicitly authorizes Spirit capture for the early-context / quality-output intent.

No private personal substance was recorded. The phrase `my vision` was treated as public project/design testimony, not personal-private content.

## Existing intent neighborhood

Relevant existing records included:

- `69fa`: early high-fidelity context window is precious; lead relies on fresh-context subagents and later work continues through fresh-context subagents.
- `f5jr`: generated worker role packets carry bundled curated doctrine and are self-contained for normal role work.
- `ka4l`: runtime `skills.nota` removed; skill discovery moves into generated role packets.
- `3pw2`, `30cu`, `3ey7`, `hu84`: subagent workflow, context preservation, and cross-audit quality records.
- `k4i3`: tight skills/reports because bloat consumes agent context.

The new records are not duplicates: `n9fl` captures the broader end-state of composing with specialized agents and maximizing early context for quality; `346n` captures the general work-quality/redo/efficiency principle.

## Spirit records accepted

### `n9fl`

Spirit reply: `(RecordAccepted n9fl)`

Captured entry:

```text
(RecordFound (n9fl ([(Technology (Software (Intelligence AgentSystems))) (Work Teamwork)] Principle [Agent systems should maximize best-quality output by maximizing early context and using extremely specific agents/skills for extremely specific scenarios. The end direction is composing with agents trained for one task rather than agents loading skills on the fly.] High High Zero [agents skills role-packets agent-workflow subagent])))
```

Verbatim testimony used:

```text
my in my vision, my end, my end goal is agents are specifically trained. For like one task, and they do it really well, and then we compose with agents instead of composing with skills that agents load. On the fly.

agents with long contexts become quickly become stupid and make mistakes. So we have to maximize for early contexts with extremely specific skill for extremely specific scenarios to maximize the quality of the output, which is why I'm doing what I'm doing.

Actually, some of this probably should go in spirit as durable intent, because maximizing early context for best quality output is actually valid intent.
```

### `346n`

Spirit reply: `(RecordAccepted 346n)`

Captured entry:

```text
(RecordFound (346n ([(Work Productivity) (Work Teamwork)] Principle [Quality is primary for agent work: bad-quality work must be redone, so sacrificing quality destroys efficiency rather than improving it.] High High Zero [agent-workflow agents])))
```

Verbatim testimony used:

```text
The quality of the work is extremely important. And when quality is bad, then the work has to be redone. And efficiency just goes right down the drain.
```

## Guardian and retry notes

- First local `n9fl` attempt failed before guardian because I initially used the old testimony shape. Exact CLI rejection: `spirit: invalid NOTA input: expected VerbatimQuote to be a parenthesis block`. I corrected the request to the current `Testimony (Vector VerbatimQuote)` shape from `signal.schema`.
- First `346n` attempt used referents `[agent-workflow quality efficiency]` and was rejected by the referent guardian because `quality` was abstract. Exact meaningful rejection: `(ReferentGuardianRejected ... [quality is an abstract concept, not a nameable particular])`. I retried with concrete registered referents `[agent-workflow agents]`, and Spirit accepted the record.

No accepted record used third-person paraphrase as testimony.

## Changed files

- `agent-outputs/AgentSkillCompositionIntent/IntentMaintainer-RetryCapture.md`

## Checks run

- `spirit Version` → passed, `(VersionReported 0.18.1)`.
- `spirit '(PublicTextSearch [early context])'` → passed; found `69fa` and related subagent/context records.
- `spirit '(PublicTextSearch [agent skills])'` → passed; found `ka4l`, `f5jr`, `k4i3`, and related records.
- `spirit '(PublicTextSearch [quality output])'` → passed; found capture and agent workflow records.
- `spirit '(PublicTextSearch [trained agents])'` → passed; found agent/role-packet neighborhood.
- `spirit '(PublicTextSearch [role packets self-contained training])'` → passed; found `ka4l`, `f5jr`, and related records.
- `spirit '(PublicTextSearch quality)'` → passed; found quality/design and testing records.
- `spirit '(PublicTextSearch [bad work redo efficiency])'` → passed; found workflow/quality adjacent records.
- `spirit /tmp/spirit-agent-composition.nota` → accepted after syntax correction: `(RecordAccepted n9fl)`.
- `spirit /tmp/spirit-quality-efficiency.nota` → accepted after referent correction: `(RecordAccepted 346n)`.
- `spirit '(Lookup n9fl)'` → passed; returned the accepted captured entry.
- `spirit '(Lookup 346n)'` → passed; returned the accepted captured entry.

## Residual risks and follow-up

- Static guidance manifestation was not edited in this retry-capture pass. `n9fl` likely has a future manifestation target in role-packet / skill-generation doctrine or workspace agent-workflow guidance; `346n` may inform quality/cross-audit workflow guidance.
- The record descriptions are agent-clarified prose, per Spirit doctrine. The Spirit testimony and reasoning strings used verbatim psyche wording only.
