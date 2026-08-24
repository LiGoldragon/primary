## 2026-08-11 — schema-next is a relic; schema should be called schema-old

> thats so old! schema *is* schema-next, so it should be called
> schema-old now. the old-old-schema doesnt exist anymore. those
> terms are relics and should be rooted out too

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
answering the workspace manifest's schema-next / schema-rust-next
ghost entries: the current schema repo is what schema-next named; the
old-old schema no longer exists; the -next terms leave the living
documents.

## 2026-08-11 — no core-* split; three repos per component

> I dont know if we need a core-* repo. I dont see much point. so
> ethos can have all the code, minus the two signal repos, and so on
> (3 repos per component). other than reusable libraries of course,
> which we want to encourage for shared traits especially.

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed,
ruling the placement fork of the shortcut round: generated Nexus and
Sema types live in the component repository itself — no
core-<component> split, no central generated-types repository.
Component anatomy: the component repo plus its two signal repos,
three repos per component. Reusable shared libraries — shared traits
especially — are encouraged.

## 2026-08-11 — a new component named psyche; spirit-ethos should not have existed

> I have a better approach now, for a new component which will
> include spirit, named psyche, which will hold spirit, intent and
> vision, and be used to feed the hijacked llm calls (we need a name
> for that... you know what im talking about?)

> I dont even know why we made that repo. the ethos code can live
> with the component. like all components (component + 2 signal
> repos)

— psyche, 2026-08-11T00:39+02:00 (Designer session 012fbf07), typed.
The first quote redirects the first-fixture fork: a new component
named **psyche** will include Spirit and hold Spirit, Intent, and
Vision, feeding the hijacked LLM calls. The second answers the
spirit-ethos repository: a component's ethos code lives in the
component repository; the anatomy is component plus two signal
repos. The psyche component's anatomy is not yet fleshed out.

## 2026-08-11 — datom confirmed; psyche is the fixture; the top-level layer enum

> 1 yes. 2 psyche is the fixture. we re-use much of spirit, and
> introduce a top-level enum; Spirit, Intent, Vision, which
> differentiates which layer records belong to. 3 yes

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
ruling the remaining shortcut-round forks: (1) the Datom repo is
plain `datom`, no -incorrect variant; (2) the psyche component is the
first ethos-rust fixture, reusing much of Spirit, with a top-level
enum — Spirit, Intent, Vision — marking which layer a record belongs
to; (3) the two signal repos per component are the ordinary-socket
and metasocket ones (agent framing confirmed by the psyche).

## 2026-08-11 — the router sorts signals; a universal signal repo wraps them

> the signal ID must be how agents interpreted my vision for an
> ability for the router to differentiate between signal types for
> sorting them out. router is for signals to go across the network.
> it should be an enum in a universal signal repo that all components
> depend on, which wrap the objects. that universal-signal repo could
> also serve other functions that all signals need to deal with
> (handshake payload basically)

— psyche, 2026-08-11T12:04+02:00 (Designer session 012fbf07), typed,
on the agent-coined numeric "Signal contract ID" scheme: the real
vision is the router — which carries signals across the network —
differentiating signal types to sort them. The mechanism is an enum
in a universal signal repo all components depend on, wrapping the
signal objects; that repo may also carry what every signal must deal
with, essentially the handshake payload. The numeric ID/registry
scheme is superseded. The repo's name is not yet ruled.
