<!-- to-the-living:start -->
Presentation.{ «Clojure and data: the rectification» }

## 1. Crystallization: short-term code is Clojure

File: `psyche-skills/skills/vision-stack.md` (new)

Drawn from `flows/e51411/vision/stack.md` (2026-09-25), `flows/d4ae97/vision/tools.md` (2026-10-08), `flows/d68c82/vision/flow.md` (2026-10-13), `flows/da2038/vision/prototypes.md` (2026-10-13).

```text
+ ---
+ description: Short-term code (a prototype, a tool, a launcher, a hook) is written, proposed, or judged for its language.
+ dependencies: [intent-psyche]
+ ---
+
+ ## Short-term code is Clojure
+
+ Short-term code is written in Clojure: a prototype, a tool, a launcher, a hook. It runs with Babashka first; when it is deployed, Nix builds its image.
+
+ A short-term program in another language is proposed as its Clojure rewrite.
+
+ The long term is Ethos and Rust, rewritten from the Malli specs and pseudo-traits of the Clojure prototype.
```

Ruling: 1a land as written · 1b land with changes (comment).

## 2. Crystallization: no values in code

File: `psyche-skills/skills/intent-data.md`

Drawn from `flows/8904b1/vision/anatomy.md` (2026-09-28), `flows/d68c82/vision/design.md` (2026-10-12), `flows/da2038/vision/data.md` (2026-10-13).

```text
  ---
- description: Code, types, traits, configuration or interpreters are treated as standing apart from data.
+ description: Code, types, traits, configuration or interpreters are treated as standing apart from data, or a value (a prompt, a context module, a model id, a path, a flow id) is placed in code.
  dependencies: []
  ---

  Everything is data. Code is data: a type is declared with code, so a type is data; a trait is data; an impl is data. "Code", "type", "check", "configuration" are not kinds of being — they are roles data plays for an interpreter, and an interpreter is just another program, so it too is data. There is one plane; nothing stands above it. Protolanguages make this obvious by being a data notation before they are anything else.
+
+ ## No values in code
+
+ Code holds only the machine that takes the values and turns them into the system. Every value is fed in: a prompt, a context module, a model id, a path, a flow id lives in its data file or context repository, and the code reads it.
+
+ What defines a language's own structure stays in the language; a constant that is structure keeps its place.
```

Ruling: 2a land in `intent-data` as intent · 2b land as vision in `vision-design` instead · 2c land with changes (comment).

On 2026-08-23 (`flows/68512643/vision/negatives.md`) you said that when Ethos authors software logic, Ethos may carry inline data the way Rust does. Choose 2d: the structure exception covers it, no further line · or 2e: add the line below.

```text
+ Whether Ethos carries inline data is ruled when Ethos authors logic.
```

## 3. Crystallization: what a correction, a question and an explanation ask for

File: `psyche-skills/skills/intent-psyche.md`

Drawn from `flows/da2038/vision/correction.md` (2026-10-13).

```text
  ---
- description: A flow weighs the living's reviewed and approved words against a machine's inference, handles psyche data, or reads a vision as short-term or long-term, or decides whether a reviewed line is psyche and which level it sits at.
+ description: A flow weighs the living's reviewed and approved words against a machine's inference, handles psyche data, reads a vision as short-term or long-term, decides whether a reviewed line is psyche and which level it sits at, or is corrected, asked, or told what the living wants.
  dependencies: []
  ---
  ...
  ## What the living reviews is psyche

  Anything the living has reviewed is psyche: a line he approves is a vision statement at least, whatever module proposed it, and leaves the mind or field module it sat in. A line he has not reviewed is a machine line.

  What the living reviews line by line becomes psyche. He may also review a knowledge proposal: it holds only facts verified in code, and he skims it.
+
+ ## A correction asks for its fix
+
+ A correction from the living asks for a proposal that fixes it in the right place. Where he names no place, the machine chooses where and what kind of fix, preferring psyche.
+
+ ## What his words ask for
+
+ A question from the living asks for knowledge. An explanation of what he wants asks for vision, or intent when it is broad enough to guide many decisions.

  ## Spirit holds beyond this system
```

Ruling: 3a land as written · 3b land with changes (comment).

## 4. Crystallization: a relay is checked first

File: `psyche-skills/skills/intent-main-flow.md`

```text
  Never block on a subflow. When the living speaks, answer from what is already witnessed; a holding line while a subflow is out is a complete answer.

  A claim is relayed as a claim; a thing is verified only by a witness. Keep observations, hypotheses, and unknowns separate.
+
+ Before relaying a brief or a book, the flow checks its proposed code against the living's lines on the stack and on values in code; one that breaks them goes back to its author.
```

Ruling: 4a land as written · 4b land with changes (comment).
<!-- to-the-living:end -->
