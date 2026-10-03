Presentation.{ «Code craft» }

Code craft is how a piece of code comes to be and is shaped: a map of what is being made first, beautiful code as the goal, every method in a trait, and Ethos as what is written while Rust becomes the assembly nobody reads in full.

**1. The map comes first**
Module: vision, new name code-craft. Action: create.
Text: "Write code from a map of what is being made: its objects, its capabilities, how they fit. Old code may inspire the map, never decide it."
Rests on: 20 and 22 Aug.

**2. Design from the wanted result**
Module: vision, code-craft. Action: edit.
Text: "Name the wanted result first and ask what it is made from: demand-driven design. Write conversions from, never into."
Rests on: 21 Aug. The name is proposed.

**3. The anatomy of a machine**
Module: vision, code-craft. Action: edit.
Text: "Every machine has three parts: gather types, make one coherent type, convert it to the output. At small scale they may be plain variables. Main is a few lines, starting from the typed input arriving as datom."
Rests on: 21 and 22 Aug.

**4. Every method belongs to a trait**
Module: vision, code-craft. Action: edit.
Text: "Every method is part of a trait. Free functions, inline lambdas and freestanding implementations are signs of bad design. Trait names are qualifiers. Many one-method traits on one type are really one trait."
Rests on: 11, 13, 17 and 31 Aug.

**5. Rust in layers**
Module: vision, code-craft. Action: edit.
Text: "The top layer reads like baby code; the logic lives in separate implementation files. Rust generated from Ethos is laid out the same way."
Rests on: 14 Sep; the second sentence is the later question.

**6. Ethos writes, Rust is assembly**
Module: vision, code-craft. Action: edit.
Text: "Rust is the new assembly; Ethos is what is written. Generated Rust is explicit before it is pretty. Ethos generates everything, implementations as well as types."
Rests on: 11 Aug, 31 Aug, 8 Sep.

**7. Prototype first, or map first**
Module: vision, code-craft. Action: edit.
Text 1: "For a new component, write a Clojure prototype first, then rewrite it in Ethos and Rust."
Text 2: "For a new component, write the Ethos map first."
Rests on: 25 Sep, 21 Aug. Name 1 or 2.

**8. The actor library**
Module: vision, code-craft. Action: edit.
Text 1: "A Nexus engine is built from actors; anything that must lock is an actor. We keep our fork of Kameo while the standards of use are designed."
Text 2: Same, but the fork is distrusted and replaced.
Rests on: 22 Aug, 13 Sep. Name 1 or 2.

**9. Never done**
Module: vision, code-craft. Action: edit.
Text: "Backward compatibility is never weighed; what does not fit is rewritten. No checker is written for a single repository: the methods-outside-traits check is built once for all, not by text search."
Rests on: 19 Aug, 18 Aug.

**10. The repository checklist**
Module: operation, repository-lifecycle. Action: edit.
Text 1: "Any repository touched is checked against the checklist and brought up to date. The checklist lives in this skill."
Text 2: Same, but the Nexus that classifies repositories runs the checklist.
Rests on: 16 Sep. Name 1 or 2.

**11. Beauty and correctness**
Module: spirit, spirit. Action: edit.
Text: "Beauty is the symptom of good engineering. More correctness pays for its machinery. Simple is worth more than counted. The target is the best design, not a good-enough one."
Rests on: 4 Sep, 28 Sep.

**12. Code is language**
Module: knowledge, vocabulary. Action: edit.
Text: "Vocabulary drives code design and implemented code drives vocabulary. A name must be true when it names: Rust you still write is assembled, not generated."
Rests on: 13 Aug, 21 Aug.
