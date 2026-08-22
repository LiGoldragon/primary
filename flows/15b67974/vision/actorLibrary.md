## 2026-08-21 — there is no ban of arc mutex; the actor subject gets its own flow

Design session `15b67974`, typed, answering the review finding that
the only two production `Arc<Mutex>` uses are intra-actor and that
the ban exists only as an agent-created grep test:

> there is no ban of arc mutex. the whole actor subject deserves its
> own discussion in another flow

## 2026-08-22 — a dedicated flow for the actor question; distrust all prior actor work, including our fork

Design session `15b67974`, typed (captured 2026-08-22T13:39+02:00),
answering the supervision/lifecycle fork and the kameo fork
keep/rebase/return decision surface:

> I want to dedicate a flow to the actor question. Everything was
> done by previous flows that received little to no guidance on
> design in this respect. Distrust it all, including our fork.

## 2026-08-22 — we are definitely using kameo actors in nexus; the standards of use are undesigned

Design session `15b67974`, typed (captured 2026-08-22T15:19+02:00),
after the withdrawn kameo identity line for the nexus skill:

> re actors: we are definitely using kameo actors in nexus. I just
> havent designed the standards of use
