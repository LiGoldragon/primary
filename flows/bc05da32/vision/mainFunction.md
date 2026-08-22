## 2026-08-22 — maybe all we want is a simple macro: datom-derived type in, input selection and conversion boilerplate out

Design session `bc05da32`, typed (captured 2026-08-22), refining the
same exchange after the derive-for-config idea was ruled out
(interfaceRootEnumerators.md 2026-08-22 — configuration comes from
the datom's shape):

> maybe all we want is a simple macro that takes a datom derived
> type as argument and creates all the input selection and
> conversion boilerplate.

Context (agent-authored, separate from the psyche's words): the
entry machinery shrinks to a thin macro — given the datom-derived
input type (the interface's root enum), it generates the
OS-boundary boilerplate: selecting where the datom arrives and
converting it into the typed input. No UI generation — the shape is
already the interface. Tentative ("maybe"); tracked as a bead. Open
there: macro versus emission by the same generator that writes the
interface types; the channel set the selection covers.

## 2026-08-22 — ethos will eventually replace everything; of course generator emission will happen, just not now

Design session `bc05da32`, typed (captured 2026-08-22), answering
the Designer's recommendation of a generic free function (option C)
over generator emission (option B) for the entry boilerplate:

> youre suggesting a free function. you're not realizing that ethos
> will eventually replace everything, so of course B will happen.
> just not now.

Context (agent-authored, separate from the psyche's words): the
fork closes — generator emission is the destination; it is not
built now because the machinery is not there yet. The free-function
recommendation weighed near-term simplicity against the end-shape,
which the spirit forbids (target the best end-shape, not the
practical compromise); an interim entry crate would be scaffolding
Ethos later kills. Bead primary-8vs updated: nothing to build now;
when the generator reaches it, the entry boilerplate is one more
thing it emits.
