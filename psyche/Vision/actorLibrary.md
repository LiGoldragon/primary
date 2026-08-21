# Actor library

## 2026-08-21 — re arc mutex ban: the approach disliked; review the actor library we use and whether the nexus skill documents it

Design session `15b67974`, typed (captured 2026-08-21T12:35+02:00),
answering the prior flow's finding that an agent-created test in
persona (`tests/actor_discipline_truth.rs`) greps production source
for `Arc<Mutex` — the "Arc<Mutex> ban":

> Re arc mutex ban: I dont like the approach anyway. I want to review
> the actor library we use, and if it is well documented in the nexus
> skill
