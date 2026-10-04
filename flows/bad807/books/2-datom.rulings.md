# Datom: rulings

1. Datom everywhere, or only where a program needs it.
   (a) Datom everywhere: all the CLIs, the system prompt of every machine call. 2026-09-15 (692df8), 2026-09-19 (b81560).
   (b) Datom only where the program needs it; none forced on a messenger. 2026-09-27 (8904b1), 2026-09-28 (8904b1).
   Proposals 1 and 8 assume (b).
2. The flow id's type.
   (a) A hash, a number of its own type; text forms are serialization outside the Nexus. 2026-10-03 (edf227, his words).
   (b) A string: `FlowId.String` in `Vision/ethos.md` (2026-09-09) and in signal-flow 10.0.0 (2026-10-03).
   Proposals 6 and 7 assume (a).

## Summary

1. `Vision/datom.md`: new section "Where datom is spoken", datom at every text edge, none where a program reads no text.
2. `Vision/datom.md`: new section "Datom beside protos and signal", a Nexus never handles datom; the CLI does.
3. `Vision/signal.md`: new section "Formats", simple and extended forms as two variants of one type.
4. `Vision/ethos.md`: new section "Shown first as ethos", ethos spec first, example datom after.
5. `Vision/datom.md`: new section "Titles and presentations", titles are datom; presentations show ethos and datom.
6. `Vision/datom.md`: new section "Identifiers and their text forms", the flow id a number; renderings on the text side.
7. `signal-flow/ethos/signal.ethos` line 116: `FlowId.String` becomes `FlowId.{ Integer }`.
8. `Curriculum/skills/datom.md`: new section "Where datom is spoken", with the two formats.
9. `Curriculum/skills/main-flow.md` line 39: the presentation line gets its type, `Block.[ Presentation.{ Title } ]`.
