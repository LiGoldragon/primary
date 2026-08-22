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

## 2026-08-17 — the training design flow asks the psyche how it is designed; it does not bring an anatomy

Design session `358f143a`, typed (captured 2026-08-17T20:20+02:00),
on the Designer's draft prompt for that flow ("Bring me the anatomy
and the forks: what the daemon owns versus what a workspace owns; how
a deployment declares itself; …"):

> Thats backwards. The model doesnt know what I want, he has to *ask
> me* how it is designed, so he can formulate it coherently and
> simply, without bluffing

The flow had not been started at that time:

> I didnt yet.

## 2026-08-18 — superseded: the daemon is flow, not training

Design session `358f143a`, typed (captured 2026-08-18T15:23+02:00):

> the new daemon I want to make isnt training anymore (abandonned).
> Its flow

See flowDaemon for the full statement.
