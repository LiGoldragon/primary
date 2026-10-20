# Ethos and Nexus: what Chronos must conform to

Flow 504f11, 2026-10-16, read-only extraction. Line numbers refer to the files as they stood at 13:01 CST.

## 0. Sources used

- **Ethos book: 2nd edition** — `/home/li/primary/flows/65f93a/books/02-ethos-vision-2.md` (published https://claude.ai/artifact/BTKBnDFt5CYJYMM4t9UmcR). The 1st edition (`01-ethos-vision.md`, Ms23Gj) has the same 19 proposals. Only the presentation changed (per 65f93a log 12:55: "one sentence per marker line, no headings or Rust, neutral datom value"). The one content change is P3's datom value: `081064` became `000000`.
- **Nexus book** — `/home/li/primary/flows/a275c0/books/01-nexus-vision.md` (published https://claude.ai/artifact/1yzVoViZQxoPuyRaqco4Yn). It has one edition.
- **Landed skills** — skills live in `/home/li/primary/.agents/skills/<name>/SKILL.md`, mirrored in `.pi/`, `.claude/` and `.opencode/`. The `.opencode` copy differs only by a `name:` frontmatter line. They are generated from psyche-context at `/git/github.com/LiGoldragon/psyche-context` (main `c301353`):
  - `vision-ethos` ← `vision/ethos.md`. It is byte-identical to `.agents/skills/vision-ethos/SKILL.md`. Last change: `97874fb 2026-10-10 vision-ethos: the inline import (D1, approved 2026-10-10)`.
  - `vision-nexus` ← `skills/vision-nexus.md`. It is byte-identical to `.agents/skills/vision-nexus/SKILL.md`.
  - Branch `v2-type-folders` (cdd49b, unmerged) moves these to `vision/ethos.md` and `vision/nexus.md` with the same content. *Inference:* the Nexus book's target path changes when that branch merges.
  - **`vision-flow-ethos` is not landed anywhere.** No such skill exists in any skills tree. `.agents/skills/knowledge-context-source-contracts/SKILL.md:35` says: "There is no vision-flow-ethos module in the inspected current psyche-context, mind-context or field-context trees, including Psyche's legacy vision directory, and no matching generated skill in current Primary. Psyche's `vision/ethos.md` still refers to that module, so the reference is not evidence that the module currently exists or is generated." vision-ethos SKILL.md:8 and :28 still point to it. The d68c82 Open books index lists «The Flow Nexus, whole: long term, then short term», 2nd edition, whose proposals include "a new flow-ethos file". That book is unruled.

## Ruling evidence (applies to every proposal below)

- **Comments:** none. `ArtifactComments read` returns "No comment threads on this artifact yet" for BTKBnD (Ethos 2nd), Ms23Gj (Ethos 1st) and 1yzVoV (Nexus).
- **Rulings:** none. Both books still end every proposal with "Ruling: land, amend, or reject." The d68c82 log ends at 12:59:52 with no ruling. Its relevant lines:
  - 12:53:18 "Ethos 65f93a published «The Ethos vision» Ms23Gj, 19 proposals in vision/ethos.md; supersedes book 38 Ethos P1-10, P22, P25"
  - 12:53:49 "Nexus a275c0 published «The Nexus: the vision» 1yzVoV, 14 proposals; supersedes book 38 Nexus P12-18, P21, P23, P24; collides with Flow Nexus/ethos/design 2nd P9-13 and Flow Nexus whole 2nd P9."
  - 12:59:52 "Open books v169: Ethos 2nd edition first, markers render."
- `flows/d68c82/books/index.html` (Open books) lists both books as open: "The Ethos vision, 2nd edition … Nineteen proposals, into the Ethos vision. Replaces the first edition." and "The Nexus: the vision, flow a275c0".
- **Landed check:** each source file is byte-identical to its landed skill, and every "-" line the books remove is still in the skill. So nothing is landed.

**Result: all 19 Ethos and 14 Nexus proposals are open.** None is landed, approved-not-landed, amended or rejected.

## 1. Proposals, verbatim

Each block is copied from the book source, lines prefixed `+` (add), `-` (remove) or blank (context). Lines inside `ethos` fences are verbatim too.

### 1a. «The Ethos vision, 2nd edition» (65f93a)

#### E1. Proposal 1: The golden example, a new section after Flow, a current best example · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:30-35`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: no "golden example" sentence in vision-ethos SKILL.md (line 8 still reads only "Flow is one of the best current examples of ethos…").

````text
+ Ethos, the Nexus and the Chronos example project together are the golden example.
+ Flow is implemented properly from the golden example, then the other nexuses.
````

#### E2. Proposal 2: How Ethos is shown, added to What Ethos is · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:37-43`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: vision-ethos SKILL.md still shows Rust beside every Ethos example (e.g. lines 130-135, 211-218).

````text
+ Where types are shown, the Ethos is shown, never the Rust it generates, unless the work is on how Ethos generates Rust.
+ Ethos is never shown out of context: each declaration names the kind of object it is and says what its types are for.
+ A datom is never shown without its Ethos specification.
````

#### E3. Proposal 3: The type ethos, a new section after Declaration: File · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:45-65`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: no `type` root or "type ethos" in SKILL.md.

````text
+ A type ethos opens with `type` and defines a single type.
+ Every type it needs is declared inline, where it is used; a type from a source comes in by the inline import.
+ A type ethos may carry one or more examples of its datom.

```ethos
+ type
+ CommitMessage.[              ; one variant
+    VisionDistillation.Vector< ;  per kind
+       Reference.{            ; a topic and
+          Topic.String        ;   a flow id
+          FlowId.String } > ]
```

```ethos
+ ; datom, expecting CommitMessage
+ VisionDistillation.[ { ethos 000000 } ]
```
````

#### E4. Proposal 4: Whole programs in Ethos, added to Horizon · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:67-72`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: Horizon section (lines 80-84) unchanged.

````text
+ The next step toward that horizon is the whole program written in Ethos: its function syntax, its implementations under traits, and a manifest for compiling and finding dependencies.
+ It stays pure description of a program, compact by having no repetition and no noise, never by shortening words.
````

#### E5. Proposal 5: The cost of the datom payload, added to What Ethos is · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:74-79`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ Ethos is designed with its datom payload in mind: machines write the datom, so what the datom costs to output weighs on every design.
+ System 1 models speak a subset of Ethos, so they can talk to an Ethos contract.
````

#### E6. Proposal 6: Memory, the stored root, in Roots and Associations · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:81-94`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: the removed lines are still present (SKILL.md line 57-60, wrapped; line 443-444 "In the Signal and Sema roots"). Removed lines 83-84 match exactly; 85, 86, 91 match after line-wrap normalisation.

````text
- Library, Signal, Operation, Memory.
- No version in a file.
- Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided.
- Signal gives a Nexus its main types and Sema its database types.
+ No version in a file.
+ Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided.
+ Signal gives a Nexus its main types and Memory its database types.
+ Every Nexus has all three: Signal, Operation and Memory.
- In the Signal and Sema roots the associations of the query, response and record types are implied and never written.
+ In the Signal and Memory roots the associations of the query, response and record types are implied and never written.
````

#### E7. Proposal 7: The Ethos Nexus, a new section after Generation · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:96-127`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: no Ethos Nexus section after Generation (SKILL.md ends at line 494).

````text
```
 +--------------+    +--------------+
 | repository A |    | repository B |
 +--------------+    +--------------+
        | carries           | carries
        v                   v
 +--------------+    +--------------+
 | datom file   |    | datom file   |
 +--------------+    +--------------+
        | loaded together, atomically
        v
 +----------------------------------+
 | Ethos Nexus                      |
 |  Memory: the registry            |
 +----------------------------------+
        | resolves
        v
 +----------------------------------+
 | a lowercase source name          |
 +----------------------------------+
```


+ The Ethos Nexus has three parts, Signal, Memory and Operation, each written in Ethos.
+ It keeps the registry of Ethos sources.
+ Each repository carries datom files naming the sources it holds, kept by whoever keeps that repository.
+ They are loaded together, atomically, into one full registry.
+ The registry changes whenever an Ethos source is added, edited or renamed.
````

#### E8. Proposal 8: Lowercase sources, capital built-ins, added to Imports · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:129-144`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ A lowercase source names an entry of the registry.
+ A name with no source and a capital first letter is a core built-in, declared in the core library; the intrinsic names are among them.

```ethos
+ Library
+ []                     ; imports
+ [ Count.Integer        ; types: a core
+                        ;   built-in
+   Topic.custom:Name ]  ;   a registry source
+ []                     ; traits
+ []                     ; associations
```
````

#### E9. Proposal 9: Types taken from Rust, added to Imports · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:146-152`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ The types Ethos takes directly from Rust are listed in one vector, specified and kept by hand.
+ The Ethos-to-Rust compiler reads that vector to know what each type links to.
+ In time, programmatic feedback on the code says where each type comes from, as it does for a built-in.
````

#### E10. Proposal 10: The special representation, a new section after Every declared type bears both traits · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:154-184`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
```
 +--------------+
 | runtime type |
 +--------------+
        | bears
        v
 +------------------------+
 | special representation |
 +------------------------+
     | encodes        ^
     | into           | decodes from
     v                |
 +------------------------+
 | representation type    |
 +------------------------+
        | is written as
        v
 +------------+
 | datom text |
 +------------+
```


+ A type whose datom form differs from its runtime form bears the special representation trait: its own datom encoding and decoding.
+ Ethos describes the real type and its representation type, which fixes the trait's input and output; Rust does the implementation.
+ A hash is held in memory as bytes and written in datom in an alphanumeric encoding.
+ A flow id is written in datom as three camelCase words.
````

#### E11. Proposal 11: New types, never aliases, in Every declared type bears both traits · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:186-200`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md lines 303-305 and 336-337 still state the alias rule; examples still emit `pub type` (lines 212-213, 239-240, 267-268, 292, 308-309, 356-358). Defect: the removed example line `[ FilePath.String   ; types: an alias` does not occur in the skill; the nearest is line 259 `[ FilePath.String                          ; types: FilePath is an alias of String`.

````text
- An alias bears them through the type it names: an alias is not a new type and cannot carry a derive.
+ A type of one position is a new type, never a type alias, and bears both traits like every declared type.
+ A struct of one field is never written: `FlowId.String` declares the new type.
+ A new type never wraps another new type: if a job is a flow id, it is written flow id.
- Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, an alias in the types section.
+ Head then symbol is a variant of `Query` or `Response` in a Signal's first two sections, a new type in the types section.

```ethos
- [ FilePath.String   ; types: an alias
+ [ FilePath.String   ; types: a new type
```
````

#### E12. Proposal 12: The flow id, a string for now, in Shapes and placement · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:202-212`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md line 349 still `  FlowId.String` with no comment. (Book shows 3-space indent; skill has 2.)

````text
```ethos
-   FlowId.String
+   FlowId.String           ; very unideal: a
+                           ;   real id from the
+                           ;   flow's hash is
+                           ;   needed
```
````

#### E13. Proposal 13: Inline is mandatory, in Inline types · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:214-220`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md line 249 still has the removed sentence verbatim.

````text
- A type used once is declared inline where it is used; a type used in more than one place is declared once and named.
+ A type used once must be declared inline where it is used, unless it is so deep that it needs too much recursion; an algorithm decides which.
+ A type used in more than one place is declared once and named.
````

#### E14. Proposal 14: Seniority, and structs over chains, added to Shapes and placement · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:222-234`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ Variants are ordered by seniority: the first is the most senior.
+ A struct is preferred over a chain of variants.

```ethos
+ Level.[ Spirit       ; most senior
+         Intent
+         Vision
+         Notion ]     ; least senior
```
````

#### E15. Proposal 15: Names made of words, added to Naming · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:236-249`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ A defined object, a type or a trait, and a variant are named in PascalCase.
+ Every other name is an uncapitalized camelCase identifier made of words, checked whenever one is created; its lowercase first letter tells it from a variant.
+ Such an identifier is a variant made on demand, with no recompiling.
+ Its check lives in a library shared across dialects: a cheap check that its parts are words, falling back to a System 1 judgment held to a certainty threshold.

```ethos
+ ; datom, a Metaflow: an aspect, a topic,
+ ; a layer; the topic is made of words
+ { Mind sourceNexus Tertiary }
```
````

#### E16. Proposal 16: How a trait is named, in Naming · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:251-256`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md lines 98-99 still "Traits are qualifier-named: Runnable, Textualizable, Structural, Embodied."

````text
- Traits are qualifier-named: Runnable, Textualizable, Structural, Embodied.
+ A trait is named for the capability it gives its type of object, by a qualifier or by a name: Runnable, Textualizable, Structural, Embodied, ClaudeHost.
````

#### E17. Proposal 17: Every trait in Ethos, added to Trait · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:258-265`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ Every feature is a capability, borne by a trait.
+ A trait carries weight: a trait with one function is suspicious, and one borne by a single type is doubly so.
+ Long term, every trait in a program is declared in Ethos, every implementation sits under one of them, and a mechanical check finds no trait outside the code Ethos generates.
+ Short term, hand-written traits are allowed.
````

#### E18. Proposal 18: Vertical layout, in Spacing · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:267-284`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md line 478 has the removed line verbatim.

````text
- Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line.
+ Ethos expands vertically, not horizontally: where a structure would run far to the right, its first element opens on a new line, indented, and each element with a next layer takes its own line.
+ The closing delimiter ends the last element's line; it never takes a line of its own.
+ Ethos indents by three spaces.
+ A comment sits above or beside what it comments on, never below, lined up with that object's indentation.
+ A vector may hold several items on a line; past a width it wraps, lined up with its first item.

```ethos
+ Metaflow.{                   ; who a flow is
+    Aspect.[ Psyche Mind Field ]
+    Topic                     ; core by default
+    Layer.[ Primary Secondary
+            Tertiary Quaternary ] }
```
````

#### E19. Proposal 19: White square brackets for a vector, added to Shapes and placement · psyche-context › vision/ethos.md  
Source: `flows/65f93a/books/02-ethos-vision-2.md:286-295`  
Target: psyche-context `vision/ethos.md` (/git/github.com/LiGoldragon/psyche-context/vision/ethos.md, byte-identical to landed /home/li/primary/.agents/skills/vision-ethos/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
+ The white square brackets are sugar for a vector, read at their own layer of interpretation and turned into the vector before the ethos reader sees the text.

```ethos
+ Names.⟦ String ⟧      ; sugar
+ Names.Vector<String>  ; what the reader sees
```
````


### 1b. «The Nexus: the vision» (a275c0)

#### N1. Proposal 1: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:69-85`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md lines 22, 35, 91 contain the removed lines verbatim.

````text
  The basic ontology of an actor and dataflow system is designed before
- implementation; signal and sema are designed against it as if new, the
+ implementation; Signal, Operation and Memory are designed against it as if new, the
  old code at most inspiration.

- The nexus and sema documents are undesigned; when they are designed
+ The Operation and Memory documents are undesigned; when they are designed
  they live in the Nexus's main repository.

  Its executable holds a default configuration as a constant. On start
- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database
  that exists holds the configuration; a database created new is
````

#### N2. Proposal 2: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:87-97`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md lines 124-127 unchanged (`## Actors`, Kameo).

````text
- ## Actors
+ ## The engine

- The engine inside a Nexus is driven by Kameo actors. The standards
- of their use are still to be designed. Arc-Mutex is permitted.
+ Whether the engine inside a Nexus is built of actors, or of something better named, is settled once it has been tried in practice.
+ Arc-Mutex is permitted.
````

#### N3. Proposal 3: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:99-107`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ The three parts, and how each of them divides, are most of the machine's anatomy.
+ 
+ A standard entry point, like a Rust macro, enforces the three parts and their one path, so nothing bypasses them; the bodies are written by hand.
````

#### N4. Proposal 4: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:109-115`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ An effect may be an algorithm over data or a wrapped command, such as a Nix build; its operation is the interface around it.
````

#### N5. Proposal 5: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:117-123`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill (but cf. vision-ethos SKILL.md line 62, landed: "A memory trait carries … for each version, the upgrade from the previous format").

````text
  Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ A Memory record type that changes form carries the operation that upgrades each record from its old form into its new one.
````

#### N6. Proposal 6: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:125-132`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  seeded with the defaults. The meta socket carries a Configure
  interface, and changed values are accepted through it.
+ 
+ For now, a Nexus's configuration may live in separate files in different repositories, each a datom payload for that Nexus. Its CLI sends them one after another on the meta socket, and the Nexus loads them atomically, even at different layers. This is how a Nexus is started until one datom can draw in another by its path.
````

#### N7. Proposal 7: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:134-140`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ 
+ A Nexus's payloads, its configuration among them, are written in datom. A Nexus that needs a value from a datom file gets it through its CLI, never by reading the text itself.
````

#### N8. Proposal 8: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:142-148`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ 
+ The code that identifies a CLI's caller lives in one library that every Nexus's CLI shares, so no CLI writes it again and it reads plainly. It is never user-facing and never configurable.
````

#### N9. Proposal 9: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:150-156`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.
+ 
+ Signal defines the forms a message can take: a simple form, without the flow id, for common queries and replies; and an extended form for the technical side, for debugging and for other components.
````

#### N10. Proposal 10: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:158-165`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md line 44 still "opens more sockets".

````text
  every Nexus has one, since without it nothing could configure the
- Nexus. A Nexus that needs more levels of access opens more sockets.
+ Nexus. A Nexus that needs more levels of access may open more sockets.
+ In the long term a Nexus knows who called each socket and checks each caller's access itself, and needs no more sockets for it.
````

#### N11. Proposal 11: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:167-173`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
+ 
+ Functionality may be put into one Nexus and moved into another once its best anatomy and the home of its data are known; it is offloaded while it still runs on the first. A Nexus may also reuse another Nexus's function, or take it in.
````

#### N12. Proposal 12: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:175-185`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill.

````text
  Everything built from now on is a Nexus, and what was built in
  another shape is rewritten as one. The consistency creates
  reliability, quality, and clarity.
+ 
+ ## Nexuses and prototypes
+ 
+ Nexuses are the long term. For now a component may run as a Clojure prototype derived from the same Ethos, carrying EDN payloads where a Nexus carries datom. A prototype is described in its own terms and never in a Nexus's: the meta socket is a Nexus's.
````

#### N13. Proposal 13: psyche-context › skills/vision-nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:187-242`  
Target: psyche-context `skills/vision-nexus.md` (/git/github.com/LiGoldragon/psyche-context/skills/vision-nexus.md, byte-identical to landed /home/li/primary/.agents/skills/vision-nexus/SKILL.md)  
Status: **open** (no ruling). Not in the skill: SKILL.md lines 154-196 still use `Voice`. Also collides: d68c82 log 12:35:55 "Conflict: Flow Nexus 2nd P9 removes the Flow example that Ethos/Nexus/Chronos P13-15 edit"; d68c82 log 12:53:49 "collides with Flow Nexus/ethos/design 2nd P9-13 and Flow Nexus whole 2nd P9"; Open books index: "Proposal 9 held: «The Nexus: the vision» covers the same file." (the hold is on the other book's P9, not on this one).

````text
```
  [ FlowId.Integer                         ; types
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
+   Metaflow.{ Aspect Topic Layer }
+                           ; who a flow is
    Aspect.[ Psyche Mind Field ]
+   Topic.String            ; core is the default
    Layer.[ Primary Secondary Tertiary Quaternary ]

  Signal                                   ; what Flow says, on its ordinary socket
- [ flow:[ FlowId Voice Event ] ]          ; imports from the Library
- [ Launch.{ Voice                         ; queries
+ [ flow:[ FlowId Metaflow Event ] ]
+                           ; imports from the Library
+ [ Launch.{ Metaflow       ; queries
             Brief.String }
    Report.{ FlowId Event } ]
  [ Launched.FlowId                        ; responses
    Refused.[ NoCapsule
-             VoiceBusy.Voice ]
+             MetaflowBusy.Metaflow ]

  Operation                                ; what Flow does: one operation for every effect
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Start.{ Voice Capsule }                ; operations
+ [ flow:[ FlowId Metaflow Event ] ]
+                           ; imports
+ [ Start.{ Metaflow Capsule }
+                           ; operations

  Memory                                   ; what Flow remembers
- [ flow:[ FlowId Voice Event ] ]          ; imports
+ [ flow:[ FlowId Metaflow Event ] ]
+                           ; imports
  [ Flow.{ FlowId                          ; record types
-          Voice
+          Metaflow
           State.[ Running Ended ]

- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
+ ; 1 Query, typed at the CLI, sent as signal
+ Launch.{ { Psyche core Primary }
+          «Draft the Nexus book» }
+ ; 2 Operation, from Signal's intend
+ Start.{ { Psyche core Primary }
+         { /home/li/primary [] } }
+ ; 3 the Change Operation hands Memory
+ Flow.{ 7 { Psyche core Primary }
+        Running [ Started ] }
```
````

#### N14. Proposal 14: primary › flows/445410/vision/nexus.md  
Source: `flows/a275c0/books/01-nexus-vision.md:244-248`  
Target: primary `flows/445410/vision/nexus.md` (a Destroy, not a skill edit)  
Status: **open** (no ruling). Not done: flows/445410/vision/nexus.md line 5 still ends "…Get this ratified, and then [Mind]. Let's get [Mind] making this on Astra on its own, even Astra and Sol topic flow."

````text
**Destroy** The working order that closes the configuration record of 2026-10-09, to ratify it and to have Mind build it, is cut out of the record. The vision in the record stays, and is archived with the landing of Proposal 6.
````


## 2. Where the books differ from the landed skills

Every `-` line in section 1 is a landed line the books would change. The pairs below set the landed skill line against the book line. They also include tensions the books create without a `-` line. Pairs marked *(inference)* are my reading.

| # | Landed skill line | Book line |
|---|---|---|
| 1 | vision-ethos:57 "Library, Signal, Operation, Memory. No version in a file. Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types." | Ethos P6 "+ Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided." / "+ Signal gives a Nexus its main types and Memory its database types." / "+ Every Nexus has all three: Signal, Operation and Memory." |
| 2 | vision-ethos:443-444 "In the Signal and Sema roots the associations of the query, response and record types are implied and never written." | Ethos P6 "+ In the Signal and Memory roots the associations …" |
| 3 | vision-ethos:303-305 "An alias bears them through the type it names: an alias is not a new type and cannot carry a derive." | Ethos P11 "+ A type of one position is a new type, never a type alias, and bears both traits like every declared type." |
| 4 | vision-ethos:336-337 "…an alias in the types section." | Ethos P11 "+ … a new type in the types section." |
| 5 | vision-ethos:212 `pub type LockId = Integer;` (and every `pub type` example) | Ethos P11 "+ A struct of one field is never written: `FlowId.String` declares the new type." *(inference: Rust output becomes a newtype, not an alias; the book shows no Rust, per P2)* |
| 6 | vision-ethos:259 `[ FilePath.String                          ; types: FilePath is an alias of String` | Ethos P11 `- [ FilePath.String   ; types: an alias` / `+ [ FilePath.String   ; types: a new type` (the removed line is not verbatim in the skill) |
| 7 | vision-ethos:349 `  FlowId.String` | Ethos P12 `+   FlowId.String           ; very unideal: a` … `;   needed` |
| 8 | vision-nexus:153 `[ FlowId.Integer                         ; types` | Ethos P12 keeps `FlowId.String`. Nexus P13 keeps `FlowId.Integer` as context. *(inference: the two skills already disagree on FlowId's type, and neither book reconciles it)* |
| 9 | vision-ethos:249 "A type used once is declared inline where it is used; a type used in more than one place is declared once and named." | Ethos P13 "+ A type used once must be declared inline where it is used, unless it is so deep that it needs too much recursion; an algorithm decides which." |
| 10 | vision-ethos:98-99 "Traits are qualifier-named: Runnable, Textualizable, Structural, Embodied." | Ethos P16 "+ A trait is named for the capability it gives its type of object, by a qualifier or by a name: Runnable, Textualizable, Structural, Embodied, ClaudeHost." |
| 11 | vision-ethos:478 "Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line." | Ethos P18 "+ Ethos expands vertically, not horizontally: where a structure would run far to the right, its first element opens on a new line, indented, and each element with a next layer takes its own line." / "+ Ethos indents by three spaces." |
| 12 | vision-ethos:164-169 canonical form indented by two spaces (`Library.{` / `  [ protos:String ]`) | Ethos P18 "+ Ethos indents by three spaces." *(inference: no `-` line touches it, so it stays in conflict)* |
| 13 | vision-ethos:174-177 "Intrinsic names known without import: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self." | Ethos P8 "+ A name with no source and a capital first letter is a core built-in, declared in the core library; the intrinsic names are among them." (adds to the rule, does not contradict it) |
| 14 | vision-ethos:130-135 etc. Rust shown beside every Ethos example | Ethos P2 "+ Where types are shown, the Ethos is shown, never the Rust it generates, unless the work is on how Ethos generates Rust." *(inference: the skill is itself about how Ethos generates Rust, so it may fall under the exception)* |
| 15 | vision-ethos:8 "Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code." | Ethos P1 "+ Ethos, the Nexus and the Chronos example project together are the golden example." / "+ Flow is implemented properly from the golden example, then the other nexuses." (P1 adds and removes nothing at line 8) |
| 16 | vision-nexus:22 "implementation; signal and sema are designed against it as if new, the" | Nexus P1 "+ implementation; Signal, Operation and Memory are designed against it as if new, the" |
| 17 | vision-nexus:35 "The nexus and sema documents are undesigned; when they are designed" | Nexus P1 "+ The Operation and Memory documents are undesigned; when they are designed" |
| 18 | vision-nexus:91 "it looks for its Sema database at the default location: a database" | Nexus P1 "+ it looks for its Memory database at the default location: a database" |
| 19 | vision-nexus:124-127 "## Actors" / "The engine inside a Nexus is driven by Kameo actors. The standards of their use are still to be designed. Arc-Mutex is permitted." | Nexus P2 "+ ## The engine" / "+ Whether the engine inside a Nexus is built of actors, or of something better named, is settled once it has been tried in practice." / "+ Arc-Mutex is permitted." |
| 20 | vision-nexus:44 "Nexus. A Nexus that needs more levels of access opens more sockets." | Nexus P10 "+ Nexus. A Nexus that needs more levels of access may open more sockets." / "+ In the long term a Nexus knows who called each socket and checks each caller's access itself, and needs no more sockets for it." |
| 21 | vision-nexus:154 `  Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer` | Nexus P13 `+   Metaflow.{ Aspect Topic Layer }` / `+                           ; who a flow is` / `+   Topic.String            ; core is the default` |
| 22 | vision-nexus:191 `Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal` | Nexus P13 `+ ; 1 Query, typed at the CLI, sent as signal` / `+ Launch.{ { Psyche core Primary }` / `+          «Draft the Nexus book» }` |
| 23 | vision-nexus:158 `[]                                       ; kinds` (Library's third section) | vision-ethos:151 "A Library's sections, in order, are imports, types, traits and associations." *(skill against skill; neither book fixes it. inference: "kinds" is the pre-rename word, per d68c82 log 12:54:05 "ethos-zero emits traits at Flow's pin c2653dd (called kinds); 07714b renames to trait")* |
| 24 | vision-ethos:62 "Four roots: Library, Signal, Operation, Memory." | Ethos P6 "+ Every Nexus has all three: Signal, Operation and Memory." and Ethos P3 "+ A type ethos opens with `type` and defines a single type." *(inference: P3 adds a fifth head, `type`, that no Roots line lists)* |
| 25 | (style rule) Ethos P18 "+ A comment sits above or beside what it comments on, never below, lined up with that object's indentation." | Nexus P13 places a comment below its object: `+   Metaflow.{ Aspect Topic Layer }` / `+                           ; who a flow is`. *(inference: book against book)* |
| 26 | vision-nexus:116 "A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies…" | Ethos P6 "+ No version in a file." and vision-ethos:148 "An ethos file carries no version" *(inference: a "protocol version" inside the wire vocabulary is in tension with this unless it lives in a manifest, which vision-nexus:68 suggests: "The wire vocabulary's version is its contract crate's semver.")* |

## 3. The current ethos form of a Nexus

**L** = landed (skill line). **P** = proposed, open (book proposal).

### 3.1 File and roots

1. One file is one Rust module, and a file has no namespace inside it. A file is written in the sweet form: the root's head, then its sections as siblings. It is converted mechanically to the canonical braced form `Root.{ … }` before it is read. — L, vision-ethos:139-146.
2. A file carries no version. Versions live in a manifest. — L, vision-ethos:148-149; P, Ethos P6 (restates it).
3. The roots are Library, Signal, Operation and Memory. Signal is what a Nexus says, Operation what it does (one operation type for every effect), Memory what it remembers, and Library what they share. — L, vision-ethos:62; vision-nexus:148.
4. Every Nexus has all three of Signal, Operation and Memory. — P, Ethos P6.
5. Each of the three is its own ethos specification. — L, vision-nexus:148.
6. Every root's first section is its imports. — L, vision-ethos:152-153.
7. A `type` head starts a single-type file, with every type inline and optional datom examples. — P, Ethos P3.

### 3.2 Sections of each root, in order

| Root | Sections | Source |
|---|---|---|
| Library | imports, types, traits, associations | L vision-ethos:151-152. vision-nexus:158 still comments the third section `kinds` |
| Signal | imports, queries, responses, types | L vision-ethos:342-351 (example, "a Signal's first two sections" are queries and responses after imports, :336-337); vision-nexus:161-170 |
| Operation | imports, operations, outcomes, types | L vision-nexus:172-180 (example only; no prose rule) |
| Memory | imports, record types ("the rest to be decided") | L vision-nexus:182-187 (example); vision-ethos:57 says "Sema's are record types". P Ethos P6 renames the rule to "Memory's are record types, the rest to be decided." |

- In Signal and Memory (landed text: "Signal and Sema"), the associations of query, response and record types are implied and never written. — L vision-ethos:443-445; P Ethos P6 (Sema→Memory).
- Ethos may generate default implementations for Query and Response, which is why Signal is its own root. — L vision-ethos:338-340.
- Placement carries meaning. Head-then-symbol is a `Query`/`Response` variant in Signal's first two sections and an alias in the types section. — L vision-ethos:335-337. P Ethos P11 makes it "a new type".
- A Nexus's own Library is imported by a lowercase source: `[ flow:[ FlowId Voice Event ] ]`. — L vision-nexus:162 (example). *Inference:* Chronos's equivalent is `chronos:[ … ]`.
- Wire repositories: `signal-<nexus>` and `meta-signal-<nexus>`, the latter never optional. A wire type repository "is written in ethos and declares vocabulary only … a closed enum of operations with their paired replies … no catch-all". Operations are verbs (`Submit`), replies are past tense (`Submitted`), and rejections name themselves. Storage vocabulary never appears on the public wire. — L vision-nexus:114-116.

### 3.3 Types and enums

- `Name.Type` declares a one-position type. Landed it is an alias (vision-ethos:204-213, 303-305). Proposed it is a new type, never an alias; a struct of one field is never written, and a new type never wraps another new type (P Ethos P11).
- `Name.{ A B … }` is a struct. Fields are named after their type in snake case; a constructed type is named type-first (`string_vector`, `lock_option`); a repeated type gets `first_`/`second_`. — L vision-ethos:195-218.
- `Name.[ A B … ]` in a types section is an enum, never a vector. — L vision-ethos:337-338.
- A variant named like a defined type carries that type. A variant may declare its payload inline (`Variant.{ … }`, `Variant.[ … ]`, `Variant.Vector<…>`), and the inline type takes a derived `_Data` name. — L vision-ethos:220-297.
- Everything is a type; there is no key-value. A type used once is declared inline, and a type used in more places is declared once and named. Nesting goes about three deep. — L vision-ethos:249. P Ethos P13: inline is mandatory unless too deep, and "an algorithm decides which".
- Variants are ordered by seniority, first most senior. A struct is preferred over a chain of variants. — P Ethos P14.
- Constructed types: `Vector<T>`, `Option<T>`, `Result<T E>`. — L vision-ethos:176-177, 397. P Ethos P19: `⟦ T ⟧` is sugar for `Vector<T>`.
- Imports: `src:Name` or `src:[ A B ]`. The inline import `Topic.custom:Name` declares a type from a source without an import entry. The source is recognised by its lowercase first letter followed by a colon. Generated code fully qualifies every name, with no `use`. — L vision-ethos:172-191. P Ethos P8: a lowercase source is a registry entry; a capitalised name without a source is a core built-in. P Ethos P9: Rust-taken types are listed in one hand-kept vector.
- Intrinsics: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self. — L vision-ethos:176-177.
- Every declared struct and enum bears `Datomizable` and `Compositional`. In a signal library they are compiled in only under the `datom` feature, which the Nexus does not enable. — L vision-ethos:299-331.
- A type whose datom form differs from its runtime form bears the special-representation trait. — P Ethos P10.
- Naming: types, traits and variants are PascalCase. Other names are camelCase identifiers made of words, "a variant made on demand". — P Ethos P15.
- No tuples except at contact points that need them. — L vision-ethos:469-470.

### 3.4 Traits

- There are no generics, only traits. A trait's identity is its name plus its constraints: `Processable<[Clonable Sendable] Serializable>`. — L vision-ethos:88-118.
- Simple trait: `Name.[ capabilities ]`. Complex trait: `Name.{ [supertraits] [AssocType<Constraint>] [CONST.Type] [capabilities] }`. — L vision-ethos:385-435.
- Capability receiver: `.` takes self, `!` takes mutable self, `:` takes no self. A bare capability is `cap.[ Yield ]`; with inputs it is `cap!{ [ Inputs ] [ Yield ] }`. A yield bracket holds one type. — L vision-ethos:387-399.
- A capability speaks in Self, the trait's own parameters and other traits. — L vision-ethos:94.
- Traits are qualifier-named (Runnable). — L vision-ethos:98. P Ethos P16 adds name-style (ClaudeHost).
- Every feature is a capability borne by a trait. A trait with one function is suspicious. Long term every trait is in Ethos. — P Ethos P17.
- Every method lives in a trait. Traits live on data-bearing types, and `fn main()` is the only free function. — L vision-nexus:25.

### 3.5 Associations

- `Type.[ TraitA TraitB ]` in the Library's fourth section asserts that the type bears those traits. It generates a compile-time assertion, and the bodies are hand-written. — L vision-ethos:361-383, 440-464.
- Interactions (trait implementations) use the type itself. — L vision-ethos:466-467.

### 3.6 Layout

- One space inside every non-empty bracket or brace. — L vision-ethos:474-476.
- Vertical layout. Landed: elements hang beneath the first, aligned. — L vision-ethos:478. Proposed: three-space indent, the first element on a new line when the structure is wide, the closer never on its own line, comments above or beside and never below, vectors wrapping. — P Ethos P18.
- A comment on every section and on every line that has a next layer, from `;` to the end of the line. — L vision-ethos:480.

### 3.7 The Signal → Operation → Memory path

- "A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path." — L vision-nexus:148.
- Worked trace (L vision-nexus:190-197): `1 Query` (Launch) → `2 Operation, from Signal's intend` (Start) → `3 the Change Operation hands Memory` (record `Flow.{ … }`) → `4 Memory's answer to Operation` (`Succeeded`) → `5 Outcome` (`Started.7`) → `6 Response, from Signal's answer` (`Launched.7`).
- "A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs." — L vision-ethos:62.
- A standard entry point, like a Rust macro, enforces the three parts and the one path. — P Nexus P3.
- An effect may be an algorithm or a wrapped command. — P Nexus P4.
- A Memory record type that changes form carries its upgrade operation. — P Nexus P5.
- Errors are vocabulary, never strings. Every reply is typed. — L vision-nexus:68.
- The Memory is reached only through the memory engine, with no central store. Policy changes only over the meta socket. — L vision-nexus:66.
- Configuration: no arguments. A default config constant seeds a new database. Configure goes on the meta socket, or on the ordinary socket until first configuration. — L vision-nexus:87-105. P Nexus P6: atomic load of several datom payloads via the CLI.
- Observation is by subscription (state on open, then each change), and polling is forbidden. — L vision-nexus:136-144. *Inference:* a Chronos that reports time must push changes to subscribers, not be polled.

## 4. Chronos, time, angles, watches — verbatim mentions

In the named sources (books, their references, landed skills):

- Ethos book 2nd ed., figure (02-ethos-vision-2.md:15): `|  | Nexus |<--------------| Chronos | |` with the edge label "is built as" (line 14) and the frame title "the golden example" (line 7).
- Ethos P1 (02-ethos-vision-2.md:32-33): "+ Ethos, the Nexus and the Chronos example project together are the golden example." / "+ Flow is implemented properly from the golden example, then the other nexuses."
- Ethos 1st ed. P1 (01-ethos-vision.md:36): "+ Ethos, the Nexus and the Chronos example project together are the golden example: Flow is implemented properly from it, then the other nexuses."
- Ethos references (65f93a/books/references/01-ethos-vision.md:14): "9 Rust types — pkg §7: d68c82/vision/ethos.md:67 (984e88/vision/ethos.md:3-7); d68c82/notion/ethos.md:3. Book 38 P8; «Chronos» 2nd ed P3; 3rd ed P6."
- Nexus references (a275c0/books/references/01-nexus-vision.md:20): "Left out of this book: Source nexus (own book); Ethos Nexus and kinds/traits and FlowId type (Ethos sibling 65f93a); Chronos and the held angle/apogee/watch defaults (later Chronos design); work-order records (one good nexus first, Chronos as test) as working instructions."
- Time, in a non-domain sense only: vision-ethos:84 / Ethos 1st ed.:80 "enables — generator emission among it — comes in its time."; Ethos P9 "+ In time, programmatic feedback on the code says where each type comes from, as it does for a built-in."; vision-nexus:134 "toward zero-downtime self-update".
- "Angle" occurs only as the delimiter: vision-ethos:116-117 "Angle brackets hold the constraints; they are a protos delimiter, recycled from Rust as Result and Self are."
- **No** landed skill (vision-ethos, vision-nexus) names Chronos, clocks or watches.

Adjacent, outside the named sources. These are logs, not books or skills, and are given only as pointers:

- a275c0 log 12:38: "exact-fraction angle/apogee/watch defaults held."
- d68c82 log 12:35:55: "It sent Chronos design defaults (Rational angle, apogee names, no open watches, contextualizer) as decided; told Field to hold them for the Chronos design metaflow. Conflict: Flow Nexus 2nd P9 removes the Flow example that Ethos/Nexus/Chronos P13-15 edit; vision-chronos path differs."
- Open books index: "Chronos, 3rd edition, flow d68c82 (Psyche core), 2026-10-16. The choices still open, each written at its default: how a derivation is reached, the solar and lunar formats, true nodes, where the location comes from, and the ephemeris; six proposals, in a new chronos file and vision-ethos. Replaces the 2nd edition."
- Chronos vision records exist at `flows/984e88/vision/chronos.md` and `flows/d68c82/vision/chronos.md`. They are not read here.
