# Skills repo becomes training

> "we should rename skills repo to training"

— psyche, 2026-08-11, steward session

Context: the repo holds skills, role agent definitions, and will hold
all material that trains agents. The rename covers everything — repo
name, directory, binary, all references.

---

> "yes, thats the concept. soon the training will be injected in the
> harness system prompt, which has higher authority in the LLM context"

— psyche, 2026-08-11, steward session

Context: training material in the system prompt outranks inherited
patterns in the LLM context. Connects to the gradients of authority
vision.

---

> "we want to make it a regular daemon+signal component (regular rust
> component)"

— psyche, 2026-08-11, steward session

Context: the generator should become a standard component following
the component architecture — a daemon that speaks signal.

---

> And I'd also like to better train the agents on being able to
> discern intent from vision. And there's so many things I'm going
> to do all at once, and I'm trying to be reasonable here, because
> if I overwhelm all the agents with all of my ideas at once, it's
> just going to be a mess, and that's been kind of my main problem,
> which is why I want to do this meta-harness.

— psyche, 2026-08-13, Designer session 6863ef19, dictated

Context: intent-from-vision discernment becomes training material;
the overwhelm problem is the stated motivation for the meta harness
(the deferred flow system, bead primary-auo).

---

> we should rename to training because now skills is like, I can't
> say skills and then you know what repo I'm talking about. But if
> it's called training, then yeah, it would be less ambiguous. I
> would see intent as a skill, which would be a hack, right? Or
> yeah, not really. I mean, intent really is durable and
> authoritative instruction, which is, it's more like we're exposing
> the fact that the word skills is not really appropriate to put all
> of these concepts. It's not the appropriate umbrella to contain
> all of these concepts, which we're not trying to fit into it. But
> I would see intent as per domain, even though right now our intent
> inventory is thin.

> we can start if there's not a lot of intent, but I mean, it should
> be per topic because otherwise everybody's going to load it and it
> might have nothing to do with what they're doing.

— psyche, 2026-08-13T18:34+02:00 (Designer session 6863ef19),
dictated

Context: the training rename reaffirmed with its reason (the
ambiguity of "skills"). Intent-as-skill ruled in concept — not a
hack: intent is durable and authoritative instruction, and the need
exposes "skills" as the improper umbrella name. Intent skills are
per domain/topic, starting thin.

## 2026-08-17 — Athena is deployment specific; the successor is a Rust daemon holding variables, regenerating through a terse datom interface

Design session `358f143a`, typed (captured 2026-08-17T19:20+02:00):

> We also have another problem; Athena is deployment specific.
> Curriculum should become a proper rust component (a daemon) which
> is configured for such variables, which it can keep in its database
> so regeneration can be done with a very terse datom interface. I
> should start another flow with this. We can put all the
> brainstorming of deep curriculum changes into a non-technical
> goal-oriented short prompt to start another design flow dedicated
> to this.

Context (agent-authored, separate from the psyche's words): "such
variables" are the setup-specific named variables (see entryFiles);
"Athena" naming inside role skills ties them to one deployment. The
successor repo is named `training` (see skillsRepository, same
message).
