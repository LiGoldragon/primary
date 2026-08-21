# flow — the daemon that sets up and starts a model flow

## 2026-08-18 — the daemon is not training (abandoned); it is flow

Design session `358f143a`, typed (captured 2026-08-18T15:23+02:00).
Supersedes the successor-repo naming in trainingRepo /
skillsRepository (2026-08-17: "a new repo called training"):

> On another note: the new daemon I want to make isnt training
> anymore (abandonned). Its flow, which will setup and start a model
> flow, with its own working directory, system prompt and training
> files, and its instruction prompt.

Context (agent-authored, separate from the psyche's words): the
component is named flow. What it does, in the psyche's words: set up
and start a model flow, with its own working directory, system
prompt, training files, and instruction prompt. Whether the
repository is also named flow, and what becomes of Curriculum's
generator role, is not yet said.

## 2026-08-19 — Curriculum is rewritten as a Nexus; the flow repo is the machinery; skills live in another repo; a few basic skills in flow replace the built-in harness prompt; the name stays flow; research requested

Design session `e06e4c07`, dictated (captured 2026-08-19T13:49+02:00).
Excerpts from one message; the Nexus vocabulary part is logged under
nexus. Trims between excerpts.

> So for example, the curriculum repository. Now essentially, not all
> of its content will go into the flow nexus, but because the skill
> contents themselves will have to live somewhere else because the
> flow nexus, the repository will be about the machinery of the flow
> nexus. And the actual skills that people want to use with their
> system will have to live in a different repository. Of course, there
> will probably be a few basic skills. No, there will be a few basic
> skills that are actually included in the flow repo, which are
> essentially the analogs of what the basic harness training prompt is
> currently that is built into the harnesses, which we will completely
> replace, is going to be about. Just basic stuff on how agents should
> behave in a harness, but with our own take on it. So do some
> research and anything that's vaguely or closely resembles or touches
> the topics that I've covered, whether it's in programming theory,
> software architecture, software ontology. Let's make you smart. I
> need a smart flow. I mean, this brings me to the fact that the word
> flow is kind of getting overloaded if we have a flow nexus. So we
> can also discuss maybe thinking of a different name for that
> repository, for that nexus. Maybe something that has to do like a
> tap or a source of the flow or something like that. Maybe flow.
> Yeah, flow is good. I like the idea that it's a flow.

Context (agent-authored, separate from the psyche's words): the flow
repo holds the machinery of the flow Nexus plus a few basic skills —
our own replacement for the harness's built-in training prompt (how
agents behave in a harness); the skills people use with their system
live in a different repository, not yet named. The name flow is kept
after a tap/source alternative was considered. Research into
programming theory, software architecture, and software ontology
touching these topics is requested before going deeper.

## 2026-08-21 — flow launches an existing harness for now; our own custom harness later, 100% typed datom messages

Design session `15b67974`, typed (captured 2026-08-21T17:21+02:00),
answering e06e4c07's Question 1 — does flow launch an existing
harness (Claude Code / Codex) with a composed system prompt, or run
its own model loop:

> yes for now. we will create our own custom harness in the future,
> which will be 100% typed datom messages going in and being
> expected out.
