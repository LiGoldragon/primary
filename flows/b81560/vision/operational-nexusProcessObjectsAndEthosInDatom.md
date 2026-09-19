# Operational: Nexus process objects implement specs, ethos specs in datom payloads, structured error messages from parsing, and ethos-in-datom escaping

## The Nexus process objects process everything. The spec is ethos, called from signal through a process that gets implemented. Give a subflow the spec and examples, explain in prose, then switch to datom for the system prompt. It responds with the spec of its response types. If it misresponds, correct it by naming the violated spec part. Better error messages generated automatically from ethos structure. Ethos becomes a payload in datom — how do we escape it?

Context: spoken directly by the living to primary Psyche opus (Claude, medium,
flow b81560) on 2026-09-19. The living describes the full Nexus → Signal →
Datom → Ethos pipeline. Nexus process objects are the implementations that
handle what comes through signal. The main function is standard. Projects must
use ethos specs. A subflow gets the spec and examples, starts in prose/markdown,
then switches to datom for the system prompt. The model responds in the spec'd
response types; misresponses are corrected by naming the violated spec part.
Error messages are auto-generated from the parse/protos structure — structure
errors are specific because the parser knows what was expected. Ethos is the
spec language used for training, error messages, and discussing new object
types. Ethos becomes a payload carried inside datom — this requires specifying
how ethos is escaped inside datom. Logged by the main flow before acting.

> So, the Nexus: it's too bad I lost this whole thing. The Nexus process objects are the ones that process everything that goes, and the main function is standard. That's why we have to force certain things, and the project has to use the ethos specs. The spec for the objects is the Nexus, and you have to call a Nexus object from signal. It has to go through a process, and that process is the implementation that gets written. It could involve a subflow, calling a subflow that's trying to use this spec. It's given the spec and a few examples of what should happen in a spec datom type, root message. Eventually, that's the vision.
>
> We can just make it simple for now: give it the spec of what it's expected to say and a few examples, and explain in prose, in a markdown thing, and then tell it, "Okay, now we switch to this spec." Then it starts to program it in datom for the rest of the system prompt. It expects it to respond with the spec of the types of responses it's supposed to be giving back, right? If it misresponds, it tries to correct it and tell it which part of the spec it's violating.
>
> We need better error messages that can be generated automatically because of the way we've created ethos, the structure, and all of that. We can give the error message as, "This is not the right structure," because when we decode, we can decode the structure part. If we can't do that, then we get an error message: "This is the wrong structure." We can get very specific types of error messages just based on the way we parse and the way we generate the protos. Datom is what's going to be generated and decoded, mostly, but ethos is the spec. Ethos is used to explain the messages in error messages or in training, or to talk about ideas for different kinds of new objects. Basically, ethos becomes a payload in datom, where we talk about ethos in datom, so that also has to be specified. How do we do that? How do we escape it?

-- psyche, direct to primary Psyche opus b81560.
