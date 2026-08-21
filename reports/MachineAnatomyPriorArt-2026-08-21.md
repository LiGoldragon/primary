# Machine Anatomy: Prior Art Survey

Survey date: 2026-08-21. The anatomy surveyed is from `psyche/Vision/machineAnatomy.md` (session 2b34fafa, dictated 2026-08-21). The software-design skill draft is at `reports/SkillDrafts/softwareDesign/draft.md`.

## The Anatomy Under Survey

For reference throughout. The four parts as stated in the psyche log:

> "There's sort of always at least four parts. One is input, receiving, then structuring these inputs... these are the inputs, and then we have the assembled inputs, the assembled source, and then what we want, which is the generated Rust, right, which has to have a type... first you have to put it all together into something that is coherent... assembled into a coherent whole... in order to have an output, we need a coherent type from which that output is a simple operation or at least an operation that can be reviewed all in one place, where all the logic is found in one place or under one trait."

The four parts in compact form:

- **Part 1 — Inputs/receiving**: raw, heterogeneous inputs from the external world
- **Part 2 — Coherent input**: assembled/standardized into a single unified named type from raw inputs; everything the core needs, in one place
- **Part 3 — Coherent output**: assembled into a coherent whole in memory before any emission; a named type representing what will be written
- **Part 4 — Output**: from the coherent output type, a simple operation reviewable in one place, under one trait; never logic sprawled everywhere

Additional principles woven into the anatomy:
- Design works **backwards** from the wanted output (demand-driven: "we know what's going to come out of it")
- Names describe what a value IS at the moment it exists, not what will happen to it
- The spine is conversions (`From`/`TryFrom`), not services

This survey covers six bodies of prior art, then synthesizes where the prior art converges, where it falls short, and what the skill can take from it.

## 1. Functional Core / Imperative Shell (Gary Bernhardt, 2012)

### Source

"Boundaries" talk, SCNA 2012: https://www.destroyallsoftware.com/talks/boundaries

Companion screencast: https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell

The talk video is paywalled. The quotes below are from Bernhardt's own published descriptions of both the talk and screencast, and from the most accurate secondary transcript record (the kbilsted GitHub collection: https://github.com/kbilsted/Functional-core-imperative-shell). All attributed to the original source.

### Bernhardt's Formulation

From the talk page description (Bernhardt's words):

> "This talk is about using simple values (as opposed to complex objects) not just for holding data, but also as the boundaries between components and subsystems."

From the screencast description (Bernhardt's words):

> "This screencast reviews a Twitter client whose core is functional, managing tweets and syncing timelines, surrounded by a shell of imperative code that manipulates stdin, stdout, the database, and the network. This design naturally allows isolated testing with no test doubles."

From the kbilsted README, transcribing the talk:

> "Imperative shell that wraps and uses your functional core. The result of this is that the shell has fewer paths, but more dependencies. The core contains no dependencies, but encapsulates the different logic paths. So we're encapsulating dependencies on one side, and business logic on the other side. Or put another way, the way to figure out the separation is by doing as much as you can without mutation, and then encapsulating the mutation separately."

From handwritten talk notes (delbetu gist: https://gist.github.com/delbetu/55b21056f9fcf7b33f0187484cd28061):

> "Every function has Value IN - Value Out"
> "These functions do not have dependencies"

### What Bernhardt Requires

Bernhardt's two constraints for the functional core: (1) purity — no mutation, no side effects; (2) no external dependencies — no I/O, no network, no database. The shell carries all mutation and all I/O. The boundary is defined by "simple values (as opposed to complex objects)."

### Mapping onto the Four Parts

**Part 1 (raw inputs):** Exact match. The imperative shell, by definition, lives at the boundary with the world. It handles stdin, stdout, the database, the network — all external input sources.

**Part 2 (coherent input, single named type):** Loose match. Bernhardt says "simple values" cross from shell into core, and that every function has "Value IN." But he never requires that these values be assembled into a single named type. Multiple values may be passed as separate arguments. The constraint is purity (values, not objects-with-behavior; no mutable state) — not any particular type topology. The "single unified type" half of Part 2 is absent from his definition.

**Part 3 (coherent output, single named type in memory before emission):** Loose match. The core returns "values out" — pure return values. No demand for a single named output type. The constraint is that the return is referentially transparent. Whether that return is a single named record or multiple tupled values is not specified.

**Part 4 (output, simple, reviewable, one place):** Exact match in intent. All mutation and I/O lives in the shell. The shell IS the output layer. Whether it is reviewable "under one trait" is a further structural claim Bernhardt does not make.

### Sharpest Gap

Parts 2 and 3. Bernhardt's pattern is defined by the purity property and the value-passing property. It says nothing about whether the values must be assembled into a single unified named type before entering the core (Part 2) or before exiting (Part 3). The anatomy adds a type-topology constraint that is absent from the functional core / imperative shell pattern.

### What the Skill Can Take

The pattern provides good language for Part 1 / Part 4 separation: "encapsulating dependencies on one side, and business logic on the other." The screencast's Twitter client is a concrete example of the shell/core split. However, the skill should not represent FCIS as equivalent to the four-part anatomy — FCIS is a purity/dependency constraint, not a type-topology requirement. The "simple values at the boundary" language is usable as a stepping stone, but the anatomy is more specific.

## 2. Impureim Sandwich (Mark Seemann, 2020)

### Sources

All from blog.ploeh.dk (Seemann's blog):

- Defining post: https://blog.ploeh.dk/2020/03/02/impureim-sandwich/
- Functional architecture definition: https://blog.ploeh.dk/2018/11/19/functional-architecture-a-definition/
- Refactoring registration flow: https://blog.ploeh.dk/2019/12/02/refactoring-registration-flow-to-functional-architecture/
- A conditional sandwich example: https://blog.ploeh.dk/2022/02/14/a-conditional-sandwich-example/
- What's a sandwich?: https://blog.ploeh.dk/2023/10/09/whats-a-sandwich/
- Recawr Sandwich: https://blog.ploeh.dk/2025/01/13/recawr-sandwich/
- Song recommendations (F#): https://blog.ploeh.dk/2025/05/19/song-recommendations-as-an-f-impureim-sandwich/

### Seemann's Formulation

From the defining 2020 post:

> "At every entry point (Main method, message handler, Controller action, etcetera) you first perform all impure actions necessary to collect input data for a pure function, then you call that pure function, and finally you perform one or more impure actions based on the function's return value."

The three-layer statement from the same post:

> "Top layer (impure): Gather data from impure sources. Middle layer (pure): Call a pure function with that data. Bottom layer (impure): Change state based on the return value."

From the 2018 foundational post:

> "A pure function can't invoke an impure activity."

From the 2022 post on limits:

> "The short answer is that it doesn't [generalize to arbitrary complexity]. Given sufficient complexity, you may not be able to 1. gather all data with impure queries, 2. call a pure function, and 3. apply the return value via impure actions."

From the 2023 "What's a sandwich?" post (relaxing the three-layer constraint):

> "the adjusted definition of the Impureim sandwich seems to be that it may have at most two impure phases, but from one to three pure slices."

From the 2025 Recawr Sandwich post (sharpest statement on the output side):

> "Once you start writing data to the network, to disk, to a database, or to the user interface, you shouldn't go back to reading in more data."

From the registration flow refactoring post, showing how intermediate values are named:

> "Instead of `p`, I decided to call the first value `validityOfProof`. This is the result of the first impure action in the sandwich (the upper slice of bread)."

Then: `let decision = completeRegistrationWorkflow r validityOfProof`

From the Song Recommendations F# post, showing multi-argument passing (not a single assembled type):

The pure function receives: `let getRecommendations topScrobbles topListeners userName = ...` — two dictionaries and a username, passed as separate parameters.

### What Seemann Requires

The ordering constraint: all impure reading before the pure core; all impure writing after. The Recawr formulation sharpens the output side: once writing begins, no more reading. Purity of the middle layer is mandatory.

### What Seemann Does Not Require

A single named/typed coherent input before the pure layer — he passes multiple parameters (two dictionaries in Song Recommendations, named intermediate values in Registration Flow). The assembly happens, but the form — single named record vs. multiple parameters — is not prescribed. Similarly for the output: the pure function's return type varies (`Result<T>`, `Either<L, R>`, `IReadOnlyCollection<_>`, etc.). No single named output type is required.

### Mapping onto the Four Parts

**Part 1 (raw inputs):** Exact match. The first impure phase gathers from the external world (DB, network, clock, file system). This is precisely what the "top bread" does.

**Part 2 (coherent input, single named type):** Loose match. Seemann's phrase is "collect all the data you need" — and the data must arrive before the pure function is called. The ordering is strict; the type topology is not. He passes multiple separate parameters in his clearest examples.

**Part 3 (coherent output, single named type in memory):** Loose match. The pure function returns a strongly-typed result, and Seemann consistently uses typed returns. In the registration flow he assigns `let decision = completeRegistrationWorkflow ...` — a single named value. But this is not a universal demand across his examples.

**Part 4 (output, simple, reviewable, one place):** Exact match in intent. The "bottom bread" acts on the pure function's return value. The Recawr formulation adds directionality: once output begins, no more input. However, whether the final impure phase is "under one trait/interface" is not specified; it can be multiple sequential impure actions.

### Sharpest Gap

Same as FCIS, but stated more precisely: Seemann's core claim is the ordering property. He does not require that the gathered data be assembled into a single named/typed coherent input before being handed to the pure function. The "single unified type" half of Part 2 is absent. The anatomy's Part 2 is a stronger prescription than either FCIS or the impureim sandwich contains.

### What the Skill Can Take

The Recawr formulation is the most useful single piece of language this tradition offers:

> "Once you start writing data to the network, to disk, to a database, or to the user interface, you shouldn't go back to reading in more data."

This is the Part 3 → Part 4 ordering constraint stated crisply. It can be cited as a named supporting principle. The name "Recawr Sandwich" (read-compute-act-write-react) is too clever to borrow, but the constraint it names is real and can be cited. The impureim sandwich is also a useful demonstration that the four-part anatomy is not eccentric — it has a clear relationship with an established, named pattern — while being more specific about type topology.

## 3. Ports and Adapters / Hexagonal Architecture (Alistair Cockburn, 2005)

### Sources

Primary: https://alistair.cockburn.us/hexagonal-architecture (2005-09-04, HaT Technical Report 2005.02)

Secondary: arc42 reproduction (https://patterns.arc42.org/patterns/hexagonal/), Cockburn interview (https://jmgarridopaz.github.io/content/interviewalistair.html), Wikipedia (https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)), 2024 book "Hexagonal Architecture Explained" (co-authored with Juan Manuel Garrido de Paz, ISBN 979-8-9985862-0-0).

### Cockburn's Formulation

The intent statement:

> "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases."

The core mechanism (the most precise single quote in the original):

> "As events arrive from the outside world at a port, a technology-specific adapter converts it into a usable procedure call or message and passes it to the application. The application is blissfully ignorant of the nature of the input device. When the application has something to send out, it sends it out through a port to an adapter, which creates the appropriate signals needed by the receiving technology (human or automated). The application has a semantically sound interaction with the adapters on all sides of it, without actually knowing the nature of the things on the other side of the adapters."

The adapter definition:

> "For each external device there is an adapter that converts the API definition to the signals needed by that device and vice versa."

The hexagon rule:

> "The rule to obey is that code pertaining to the inside part should not leak into the outside part."

### What Cockburn's Architecture Prescribes

Ports define protocol interfaces. Adapters convert between external technology and the port interface. The application core is isolated from all external technology and can be tested against any adapter — including a test harness. The driving/driven distinction separates adapters that initiate calls to the application from adapters the application calls out to.

### Where Cockburn's Architecture Falls Short of the Anatomy

The phrase "a usable procedure call or message" is the crux. Cockburn uses the disjunction deliberately. "Procedure call" permits passing multiple arguments without any assembled type. "Message" is consistent with a single named object. He does not mandate that the adapter must assemble a single coherent named type before calling the core.

From Cockburn's original, confirmed verbatim:

> "As events arrive from the outside world at a port, a technology-specific adapter converts it into a usable procedure call or message..."

The adapter converts — but the form of what is converted to is left open. The architecture is defined by the symmetry of ports (interfaces) and by the inside-must-not-leak-to-outside rule. It does not prescribe typed coherent assembly at either input or output.

### Robert C. Martin's Clean Architecture Elaboration (2012/2017)

**Sources:** Blog: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html. Book notes: https://github.com/serodriguez68/clean-architecture/blob/master/part-5-2-architecture.md

Martin acknowledges Cockburn's hexagonal architecture explicitly, then elaborates the boundary data discipline:

> "Typically the data that crosses the boundaries is simple data structures. You can use basic structs or simple Data Transfer objects if you like. Or the data can simply be arguments in function calls. Or you can pack it into a hashmap, or construct it into an object. The important thing is that isolated, simple, data structures are passed across the boundaries."

> "when we pass data across a boundary, it is always in the form that is most convenient for the inner circle."

Martin's book introduces named boundary types — the InputBoundary/OutputBoundary pattern (from book notes, claimed not witnessed):

> "The Controller packages that data into a plain old Java object and passes this object through the InputBoundary to the UseCaseInteractor."

> "Upon completion, the UseCaseInteractor gathers data from the Entities and constructs the OutputData as another plain old Java object. The OutputData is then passed through the OutputBoundary interface to the Presenter."

### Mapping onto the Four Parts

**Part 1 (raw inputs):** Exact match. "Events arrive from the outside world at a port" — raw, technology-specific events.

**Part 2 (coherent input, single named type):** Loose match in Cockburn; closer in Martin. Martin's "Controller packages that data into a plain old Java object" is the closest the tradition comes to requiring a single assembled input type. But Martin explicitly says "or the data can simply be arguments in function calls" — multiple forms are acceptable. The anatomy's requirement for a single named domain type is stronger than either source.

**Part 3 (coherent output, single named type in memory):** Loose match in Cockburn; closer in Martin. Martin's "UseCaseInteractor gathers data from the Entities and constructs the OutputData" approaches the anatomy's Part 3. But "plain old Java object" / "OutputData" is a generic DTO framing — the anatomy asks for a domain-meaningful named type (AssembledRust, not "OutputData"), assembled by a conversion, not constructed by a use case interactor.

**Part 4 (output, simple, reviewable, one place):** Cockburn: the driven adapter "creates the appropriate signals needed by the receiving technology." Martin: the Presenter receives OutputData through OutputBoundary. This maps structurally, but the Presenter is an adapter, not a simple emission operation from a named type.

### Sharpest Gap

Services-at-boundary vs. typed-coherent-conversion. Cockburn's and Martin's architectures define boundaries by port interfaces (services), not by named domain types. An adapter converts external signals into port calls; the boundary is the interface, not the type. The four-part anatomy's boundaries are defined by named types (the coherent input type and the coherent output type). No service exists at the boundary — the boundary IS the type. The adapter (in hexagonal) becomes unnecessary: if the coherent input type is defined correctly, TryFrom from raw inputs to the coherent input type IS the adapter. This is not a refinement of hexagonal; it is a different framing of what a boundary is.

The term "semantically sound interaction" in Cockburn is also noteworthy — the application has "a semantically sound interaction with the adapters." The anatomy achieves semantic soundness through type names, not through port protocols.

### What the Skill Can Take

Martin's InputData/OutputData pattern can be cited as prior art approaching Part 2 and Part 3 — evidence that the typed-boundary idea has appeared in adjacent literature, even if not made into a hard requirement. The hexagonal literature is most useful as a contrast: "hexagonal architecture defines boundaries by port interfaces (services); the anatomy defines boundaries by named conversion types." The contrast sharpens what is original in the anatomy.

## 4. Compiler Architecture

### Sources

- LLVM architecture (Lattner): https://aosabook.org/en/v1/llvm.html ("Architecture of Open Source Applications," vol. 1)
- GHC architecture (Marlow and Peyton Jones): https://aosabook.org/en/v2/ghc.html ("Architecture of Open Source Applications," vol. 2)
- rustc dev guide overview: https://rustc-dev-guide.rust-lang.org/overview.html
- rustc MIR: https://rustc-dev-guide.rust-lang.org/mir/index.html
- "Introducing MIR" (Rust blog): https://blog.rust-lang.org/2016/04/19/MIR/
- Nanopass framework: https://nanopass.org/ ; SIGPLAN blog: https://blog.sigplan.org/2019/07/09/my-first-fifteen-compilers/
- LLVM deeper analysis: https://www.thesoftwarefrontier.com/p/how-llvm-works-the-ir-that-took-over

### 4a. LLVM (Lattner)

Lattner's AOSA article is the clearest statement in the literature of why a coherent intermediate representation is the architectural invariant. From the article:

The three-phase shape:

> "The most popular design for a traditional static compiler (like most C compilers) is the three phase design whose major components are the front end, the optimizer and the back end. The front end parses source code, checking it for errors, and builds a language-specific Abstract Syntax Tree (AST) to represent the input code."

The IR as the sole interface — the sharpest formulation:

> "LLVM IR is both well specified and the *only interface to the optimizer*. This property means that all you need to know to write a front end for LLVM is what LLVM IR is, how it works, and the invariants it expects."

The IR as self-contained — stated by naming the failure case (GCC without it):

> "its GIMPLE mid-level representation is not a self-contained representation. As a simple example, when the GCC code generator goes to emit DWARF debug information, it reaches back and walks the source level 'tree' form."

This is the anatomy's negative case stated explicitly: absence of a coherent output type forces the emitter to "reach back" into earlier stages. This is what "logic sprawled over everywhere" looks like in a real system.

The IR's three isomorphic forms (from the Software Frontier analysis):

> "the IR exists in three isomorphic forms: a human-readable textual assembly, a dense binary serialization called bitcode, and an in-memory form the compiler manipulates directly. They are interconvertible without loss, which is exactly what lets the IR be shipped and compiled later rather than only used in-process."

On backend emission:

> "Optimized IR is still target-independent. Turning it into machine code is the backend's job."

### 4b. GHC (Marlow and Peyton Jones)

GHC's AOSA chapter states the four-part anatomy most cleanly of any documented compiler, because the intermediate representation (Core) is explicitly described as the complete, fully-assembled form into which all of Haskell is translated before any optimization or code generation occurs.

On desugaring producing Part 2:

> "The process of desugaring therefore removes all the syntactic sugar, translating the full Haskell syntax into a much smaller language that we call Core."

> "In contrast Core is a tiny, principled, lambda calculus. It has extremely few syntactic forms, yet we can translate all of Haskell into Core."

Core as the invariant through the optimization pipeline:

> "All of GHC's analysis and optimisation passes work on Core. This is great: because Core is such a tiny language an optimisation has only a few cases to deal with."

> "Each of the optimisation passes takes Core and produces Core."

The pipeline from Core to emission (Parts 3 and 4):

> "The code generator first converts the Core into a language called STG, which is essentially just Core annotated with more information required by the code generator. Then, STG is translated to Cmm, a low-level imperative language with an explicit stack."

After Cmm: three backend routes (native code generator, LLVM, C). Emission is last, downstream of a complete Cmm representation.

The full pipeline: Source → Parse → Rename → Type-check → Desugar → **Core** → Optimise (Core → Core) → STG → Cmm → emit. Core is the boundary between coherent input and coherent output phases. Nothing is emitted until Core is complete.

### 4c. rustc

rustc names every intermediate form explicitly and states the "lowering" operation at each step.

The pipeline (Parts 1 and 2):

> "The raw Rust source text is analyzed by a low-level lexer... The parser translates the token stream from the lexer into an Abstract Syntax Tree (AST)."

> "Next the AST is converted into High-Level Intermediate Representation (HIR), a more compiler-friendly representation of the AST... This process is called 'lowering' and involves a lot of desugaring."

> "The HIR is further lowered to MIR (used for borrow checking) by constructing the THIR (an even more desugared HIR used for pattern and exhaustiveness checking) to convert into MIR."

MIR as the assembled coherent form (Part 2 → Part 3 boundary):

> "MIR stands for mid-level IR, because the MIR comes between the existing HIR ('high-level IR', roughly an abstract syntax tree) and LLVM (the 'low-level' IR)."

> "Previously, the 'translation' phase in the compiler would convert from full-blown Rust into machine-code-like LLVM in one rather large step. But now, it will do its work in two phases, with a vastly simplified version of Rust — MIR — standing in the middle."

> "With MIR, all of that logic is centralized in MIR construction, and the later passes can just rely on that."

The last quote — "all of that logic is centralized in MIR construction" — is the anatomy's "under one trait, in one place" stated for a real system.

Codegen as emission (Part 4):

> "Since rustc uses LLVM for code generation, the first step is to convert the MIR to LLVM-IR. This is where the MIR is actually monomorphized. The LLVM-IR is passed to LLVM, which does a lot more optimizations on it, emitting machine code."

### 4d. Dragon Book (Aho, Lam, Sethi, Ullman)

The Dragon Book's canonical contribution is the analysis-synthesis model (from secondary summaries; direct text not fetched):

> "In the analysis-synthesis model of a compiler, the front-end analyzes a source program and creates an intermediate representation, from which the back-end generates target code."

The book divides compilation into the analysis part (lexical, syntactic, semantic analysis — producing an IR) and the synthesis part (code generation — consuming that IR to produce output). This maps directly to Parts 1–2 as analysis and Parts 3–4 as synthesis. The m+n vs. m×n argument: with a complete IR separating frontend and backend, m source languages and n target architectures require m+n components, not m×n. This only holds when the IR fully separates the two sides — no reaching back.

### 4e. Nanopass Framework

From the SIGPLAN blog:

> "a compiler should be structured as a large number of small passes, each performing a single specific task"

> "a series of many small passes, each with a well-defined input and output language"

Nanopass makes the four-part anatomy mandatory at the micro level: each pass consumes a complete, well-defined IR and produces a complete, well-defined IR, never reaching backward. The framework provides a DSL for specifying these IRs explicitly, so the type of each stage is a first-class design artifact.

### Mapping onto the Four Parts

| Part | Compiler | Mapping |
|------|----------|---------|
| Part 1 (raw inputs) | Source text, token stream | Exact. Source text / lexer tokens are the raw, unstructured external input. |
| Part 2 (coherent input, single named type) | AST → (HIR/THIR) → Core/MIR | Exact. The AST and further-lowered forms are the assembled, structured representation of all source material, consumed by the optimizer. GHC's Core is the sharpest example: one tiny language into which all of Haskell translates. |
| Part 3 (coherent output, single named type) | Cmm/LLVM IR (target IR) | Exact. The target IR is assembled in memory before any machine code is written. LLVM IR's three isomorphic forms show that the coherent output exists as a complete in-memory object. |
| Part 4 (output, simple, reviewable, one place) | Code emission / AsmPrinter | Exact in structure. The emitter consumes the target IR and writes machine code. LLVM's AsmPrinter is a named class for this stage. |

### Sharpest Insight

The compiler tradition is the most exact match for the anatomy — the only prior art body that maps all four parts precisely. The additional insight from the LLVM article is the negative case: GCC's failure to have a self-contained IR forces the emitter to "reach back and walk the source-level tree form." This is the anatomy's "logic sprawled over everywhere" stated as an architectural defect in real production code. The nanopass framework turns the four-part shape into a formal requirement enforced by a DSL. The anatomy generalizes this compiler pattern to all machines.

### What the Skill Can Take

The LLVM/GHC/rustc examples are the strongest concrete exemplars available. The skill can use:
- "LLVM IR is the only interface to the optimizer" as the model for Part 2 (coherent input type is the only interface to the core)
- The GCC failure case ("reaches back and walks the source level tree") as the named failure mode of an absent or incomplete Part 3
- rustc's "all of that logic is centralized in MIR construction, and the later passes can just rely on that" as the anatomy's "under one trait, in one place" stated for a real system
- GHC's Core as the clearest example of a coherent assembled input: "tiny, principled, lambda calculus... we can translate all of Haskell into Core"

## 5. Backwards Design

### 5a. Denotational Design (Conal Elliott)

**Sources:**
- "Denotational design with type class morphisms" (ICFP 2009 paper): http://conal.net/papers/type-class-morphisms/
- Talk: BayHac 2014: https://github.com/conal/talk-2014-bayhac-denotational-design
- "Tangible Functional Programming" (ICFP 2007): http://conal.net/papers/Eros/eros.pdf
- Commentary by Eric Normand: https://ericnormand.me/podcast/why-do-i-like-denotational-design
- Sandy Maguire's summary: https://reasonablypolymorphic.com/blog/follow-the-denotation/

Elliott's method, from primary sources and secondary summaries:

> Give a (preferably simple) mathematical meaning (model) for the types provided by a library, and then define each operation as if it worked on meanings rather than on representations.

His key principle:

> The instance's meaning is the meaning's instance.

On not starting from representation (paraphrase from secondary sources reflecting his talks):

> "We don't want to jump in and say, 'An image is an array of pixels.' That's too soon... we're bringing a lot of implementation baggage into our design before we've even thought about what we wanted to do."

The design order: (1) choose the type, (2) give it a denotation — a mathematical meaning as simple as possible (e.g., `Behavior a = Time -> a`, `Image = Point -> Color`), (3) define operations on the meaning, (4) derive correct implementations from the requirement that implementation must conform to the denotation. The implementation is constrained to be correct with respect to the meaning; the meaning is not constrained to be achievable.

**Mapping.** Elliott's denotation corresponds to Part 3 — he first declares what the output type IS (as a mathematical object), before asking what produces it. He then asks what operations on that meaning are required (what must inputs look like). Implementation (Part 4) is last. The direction: desired meaning → required operations → implementation. Not: here is what I can build, now what does it mean?

**What the skill can take.** The demand to name what a type IS before asking how to produce values of that type. Elliott's `Behavior a = Time -> a` is the model: the output type has a declared essence, and implementation correctness is defined as conformance to that essence. This is the "coherent output type" step stated as a design requirement: you must know what the type IS before you can implement what produces it. The specific wording "denotational design" is not the skill's language, but the principle — declare the output type's meaning before asking how to build it — is.

### 5b. Wishful Thinking (SICP, Abelson and Sussman)

**Source:** "Structure and Interpretation of Computer Programs," 2nd edition, Section 2.1.1 ("Example: Arithmetic Operations for Rational Numbers"): https://sicp.sourceacademy.org/chapters/2.1.1.html

The verbatim quote:

> "We are using here a powerful strategy of synthesis: wishful thinking."

The context: Abelson and Sussman write `add-rat`, `mul-rat`, and other arithmetic operations using constructors and selectors (`make-rat`, `numer`, `denom`) before specifying how rational numbers are represented:

> "We haven't yet said how a rational number is represented, or how the procedures `numer`, `denom`, and `make-rat` should be implemented. Even so, if we did have these three procedures, we could then add, subtract, multiply, divide, and test equality..."

The strategy: write the core transformation (given coherent inputs, produce the result) as if coherent inputs already exist. Then separately ask how to produce those coherent inputs. This is strict top-down decomposition: write the high-level operation first (assuming its inputs are in the right form), then ask what produces those coherent inputs.

**Mapping.** Exact match for the anatomy's design direction. SICP writes them in the order: Part 2→3 first (the transformation, assuming coherent input), Part 1→2 second (what creates the coherent input). This is the anatomy's backwards design stated as a programming strategy, with "wishful thinking" as the name for the permission to write the central logic before the input pipeline exists.

**What the skill can take.** "Wishful thinking" is the permission slip to write the central logic (Part 2 → Part 3) before the input pipeline (Part 1 → Part 2) exists. The anatomy's design order — start from the coherent output type, ask what creates it, ask what creates that — is SICP wishful thinking applied recursively to type design rather than to function implementation.

### 5c. TDD Assert-First (Kent Beck)

**Sources:**
- "Test-Driven Development: By Example" (Beck, 2002, Addison-Wesley): Assert First pattern, pp. 128–129
- "Canon TDD" (Kent Beck's newsletter): https://newsletter.kentbeck.com/p/canon-tdd

The sharpest quote — Beck attributing the original inspiration:

> "The original description of TDD was in an ancient book about programming. It said that you take the input tape, manually type in the output tape you expect, then program until the actual output tape matches the expected output."

From Canon TDD, on the assert-first protip:

> "Try working backwards from the assertions some time."

**Mapping.** The "output tape" formulation is backwards design in one sentence. The expected output is prior; programming is the activity of closing the gap between "what I want" and "what I have." Mapping to the anatomy: the assertion IS the declaration of Part 4 (what the output should be); test setup constructs the coherent input (Part 2); the implementation closes the gap. TDD's red bar is demand without supply — the demand exists (Part 4), supply does not yet exist (Parts 1–3). The design direction is from desired output backwards.

**What the skill can take.** Beck's "output tape" formulation is the shortest, most accessible expression of backwards design: write the expected output first, then derive what must produce it. This can be cited as the TDD formulation of the anatomy's design direction.

### 5d. Demand-Driven / Pull-Based / Lazy Evaluation

**Sources:**
- Haskell lazy evaluation: https://wiki.haskell.org/Lazy_evaluation
- Haskell Wikibook on Laziness: https://en.wikibooks.org/wiki/Haskell/Laziness
- Conal Elliott, "Push-Pull Functional Reactive Programming" (Haskell Symposium 2009): http://conal.net/papers/push-pull-frp/

From the HaskellWiki:

> "Lazy evaluation is driven by demand: the evaluation of a term depends on how much of its result will be needed."

> "Expressions are not computed when bound to variables but only when their values are required."

From secondary analysis of Elliott's push-pull FRP paper:

> "[In the pull model] evaluation starts at the output event and follows the arrows in reverse direction to calculate its occurrences."

**Mapping.** In a pull-based system, the consumer's demand is the primary cause; everything upstream exists to satisfy it. The pull model is the computational substrate of backwards design: the output query (Part 4) drives what the coherent output type must provide (Part 3), which drives what the coherent input must contain (Part 2), which drives what the raw inputs must supply (Part 1). Lazy evaluation makes this explicit at the language level: thunks are forced only when demanded, propagating the demand backwards through the computation graph.

**What the skill can take.** The pull model is confirmation that the demand-driven design direction has a computational basis, not merely a methodological preference. The anatomy's "we know what's going to come out of it" is the pull model stated as a design discipline.

### 5e. Outside-In TDD (London School / Freeman and Pryce)

**Sources:**
- "Growing Object-Oriented Software, Guided by Tests" (Freeman and Pryce, 2009): https://growing-object-oriented-software.com/
- Outside-In TDD slideshare: https://www.slideshare.net/pkofler/outsidein-test-driven-development-the-london-school-of-tdd

From the London School presentation:

> "Start with top level interaction (from UI)"

> "Discover/design needed collaborators" [by mocking them into existence]

The outside-in / London school discipline: write an acceptance test (outermost layer — what the user or system sees). That test is red. Run to see the first failure point — which collaborator is missing. Write a unit test for that collaborator, implement it, move to the next. The acceptance test drives the entire inner design.

**Mapping.** Outside-in TDD applies backwards design recursively: the acceptance test is the desired user output (Part 4). Mocked collaborators are the declared coherent output contracts at each layer boundary (Part 3, layer by layer). Unit tests that implement those collaborators construct what the coherent inputs need to look like (Part 2). Raw data sources are last (Part 1). Each layer's acceptance test becomes the outer frame from which the next layer's design is derived.

**What the skill can take.** Outside-in TDD demonstrates that backwards design applies recursively — at every layer boundary, the consumer's need defines the producer's contract. This maps to the anatomy's recursive "what do we need to get what we need to get what we want."

## 6. Coherent Whole Before Writing

### 6a. Haskell IO Monad (Sharpest Formal Statement)

**Sources:**
- UPenn CIS 194 Spring 2013, Lecture 8 (Brent Yorgey): https://www.engineering.upenn.edu/~cis194/spring13/lectures/08-IO.html
- "A Gentle Introduction to Haskell" (Hudak, Peterson, Fasel, 1999): https://www.haskell.org/tutorial/io.html
- Haskell Wiki — IO for Imperative Programmers: https://wiki.haskell.org/Haskell_IO_for_Imperative_Programmers

The sharpest formulation (Yorgey CIS194):

> "Values of type `IO a` are *descriptions of* effectful computations, which, if executed would (possibly) perform some effectful I/O operations and (eventually) produce a value of type `a`."

> "A value of type `IO a`, *in and of itself*, is just an inert, perfectly safe thing with no effects. It is just a *description* of an effectful computation."

> "a value of type `IO a` is just a 'recipe' for producing a value of type `a` (and possibly having some effects along the way). Like any other value, it can be passed as an argument, returned as the output of a function, stored in a data structure"

> "The Haskell compiler looks for a special value `main :: IO ()` which will actually get handed to the runtime system and executed."

From "A Gentle Introduction to Haskell":

> "Actions are defined rather than invoked within the expression language of Haskell. Evaluating the definition of an action doesn't actually cause the action to happen."

From the Haskell Wiki:

> "The secret to success is to start thinking about I/O as a result that you achieve rather than something that you do."

**Mapping.** Haskell's IO monad is the most precise formal statement of the build-whole-then-emit principle: the pure computation produces a value (an `IO` description — the coherent output type); the runtime then executes it. The program and its effects are separated. Parts 1–3 are pure computation; Part 4 (execution of IO actions) is handed to the runtime. The anatomy's Part 3 "assembled into a coherent whole in memory before emission" is what `main :: IO ()` is: a complete description of all effects, computed first, emitted by the runtime after.

**What the skill can take.** "A value of type `IO a`, in and of itself, is just an inert, perfectly safe thing with no effects. It is just a description of an effectful computation." This is the anatomy's Part 3 stated with maximum clarity. The coherent output type is an inert description. Emission (Part 4) is the runtime acting on that description. The skill can borrow this framing: a machine's Part 3 is a description of what should be emitted, not an act of emitting.

### 6b. Linker Algorithm (Ian Lance Taylor)

**Source:** Ian Lance Taylor, "Linkers Part 2," airs.com, 2007: https://www.airs.com/blog/archives/39

The full basic linker algorithm, verbatim:

> "At this point we already know enough to understand the basic steps used by every linker.
>
> * Read the input object files. Determine the length and type of the contents. Read the symbols.
> * Build a symbol table containing all the symbols, linking undefined symbols to their definitions.
> * Decide where all the contents should go in the output executable file, which means deciding where they should go in memory when the program runs.
> * Read the contents data and the relocations. Apply the relocations to the contents. Write the result to the output file.
> * Optionally write out the complete symbol table with the final values of the symbols."

**Mapping.** The linker algorithm is a clean example of all reading before any writing. Writing (Part 4) is the last step. All symbol resolution, layout decisions, and relocation application (Parts 2 and 3) are complete before the output file is opened for writing. The "write the result to the output file" step receives a complete, resolved, relocated, laid-out representation — the coherent output type — and writes it.

**What the skill can take.** The linker is the cleanest systems-programming example of Parts 3 and 4 in sequence: build the complete in-memory layout (Part 3), then write it (Part 4). The algorithm structure enforces the anatomy's requirement that emission be a simple operation from a complete representation.

### 6c. Browser Rendering Pipeline

**Source:** "How Browsers Work" (Tali Garsiel and Paul Irish, 2011): https://web.dev/articles/howbrowserswork

The within-stage pipeline:

> "While the DOM tree is being constructed, the browser constructs another tree, the render tree. This tree is of visual elements in the order in which they will be displayed."

> "After the construction of the render tree it goes through a 'layout' process... The next stage is painting — the render tree will be traversed and each node will be painted using the UI backend layer."

Counterpoint from the same article:

> "It won't wait until all HTML is parsed before starting to build and layout the render tree. Parts of the content will be parsed and displayed, while the process continues with the rest of the contents that keeps coming from the network."

**Assessment.** The within-stage ordering (render tree precedes paint, layout precedes paint) maps to the anatomy. But browsers use progressive rendering — they do not wait for the complete tree before beginning to paint. This is partial prior art: the stage ordering is correct, the "whole before any output" reading is refuted by the same source. The render tree pattern is a real example of a coherent intermediate type (render tree) being assembled before a downstream stage (painting), but the practical system does not enforce whole-before-emit at the document level.

### 6d. Transactional Atomicity (Jim Gray, 1981)

**Source:** Jim Gray, "The Transaction Concept: Virtues and Limitations," Tandem TR 81.3, June 1981: https://jimgray.azurewebsites.net/papers/theTransactionConcept.pdf

Verbatim from the paper:

> "A transaction is a transformation of state which has the properties of atomicity (all or nothing), durability (effects survive failures) and consistency (a correct transformation)."

> "Transactions must be atomic and durable: either all actions are done and the transaction is said to commit, or none of the effects of the transaction survive and the transaction is said to abort."

> "none of the effects of protected and real actions of an aborted transaction are ever visible to other transactions."

**Mapping.** The transactional model is the database formulation of whole-before-emit: a complete transformation is assembled, and then committed atomically — no partial state is ever visible. This maps to the anatomy's Part 3 → Part 4 transition: the coherent output type is the "prepared transaction," and emission (commit) is atomic. However, Gray's concern is correctness under failure (all-or-nothing for reliability), not the architecture of how output logic is structured in a program. The motivation differs from the anatomy's motivation (reviewability and non-sprawl of output logic).

### 6e. GoF Builder Pattern (Partial)

**Source:** Design Patterns (Gamma, Helm, Johnson, Vlissides, 1994), intent (via Wikipedia: https://en.wikipedia.org/wiki/Builder_pattern):

> "The intent of the builder design pattern is to separate the construction of a complex object from its representation. By doing so, the same construction process can create different representations."

From Refactoring.guru (https://refactoring.guru/design-patterns/builder):

> "Builder is a creational design pattern that lets you construct complex objects step by step. The pattern allows you to produce different types and representations of an object using the same construction code."

**Mapping.** The Builder pattern separates construction from representation — the built product is assembled step by step and then retrieved. This has structural resemblance to Part 3 (assemble the coherent output, then emit). However, the GoF's emphasis is on configurability of construction (one process, multiple product forms), not on the discipline of having a complete type before emission. The pattern does not prohibit side-effectful emission during construction; the GoF does not make that constraint explicit. The anatomy's Part 3 is stronger: it is not about configurability but about the principle that emission must come from a complete type, not be interleaved with assembly.

## 7. Single-Point-of-Emission / Output Logic in One Place

### 7a. Rust's Display Trait (Strongest Type-System Enforcement)

**Source:** Rust standard library documentation, `std::fmt::trait.Display`: https://doc.rust-lang.org/std/fmt/trait.Display.html

Verbatim:

> "Because a type can only have one `Display` implementation, it is often preferable to only implement `Display` when there is a single most 'obvious' way that values can be formatted as text."

> "`fmt::Display` implementations assert that the type can be faithfully represented as a UTF-8 string at all times."

**Mapping.** The Rust type system enforces single-point-of-emission at the per-type level: one canonical `impl Display for T` per type, enforced by the compiler. This does not prevent scattered emission across modules — it prevents multiple competing Display implementations for one type. Within the anatomy: Part 4 (output from the coherent output type) corresponds to implementing Display (or Serialize, or whatever emission trait is appropriate) once, on the coherent output type. The type system then makes that the single place all output logic for that type must live.

### 7b. Serde (Serialize trait)

**Source:** https://serde.rs/

> "A data structure that knows how to serialize and deserialize itself is one that implements Serde's `Serialize` and `Deserialize` traits (or uses Serde's derive attribute to automatically generate implementations at compile time)."

**Mapping.** Serde's Serialize is the anatomy's Part 4 expressed as a trait: the coherent output type (Part 3) implements Serialize once, and all serialization logic lives in that one implementation. Multiple output formats (JSON, TOML, bincode) are handled by swapping the serializer, not by scattering output logic. This is the anatomy's "under one trait" pattern instantiated in a widely-used Rust library.

### 7c. Single Responsibility Principle (Robert C. Martin)

**Source:** https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html

Verbatim:

> "The Single Responsibility Principle (SRP) states that each software module should have one and only one reason to change."

On not generating output in computation modules:

> "This is the reason we do not put SQL in JSPs. This is the reason we do not generate HTML in the modules that compute results."

On the organizing principle:

> "Gather together the things that change for the same reasons. Separate those things that change for different reasons."

**Mapping.** SRP is the closest named principle to "output logic in one place." The statement "we do not generate HTML in the modules that compute results" directly articulates the separation. SRP is a necessary but not sufficient condition for the anatomy's Part 4: it says output and computation must not be co-located; it does not say output must be under one trait or reviewable in one place. The anatomy's claim is stronger.

### 7d. GoF Visitor Pattern

**Source:** Wikipedia citing GoF (https://en.wikipedia.org/wiki/Visitor_pattern):

GoF intent:

> "Represent an operation to be performed on elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates."

GoF motivation (verbatim, attributed):

> "distributing all these operations across the various node classes leads to a system that's hard to understand, maintain, and change."

**Mapping.** The Visitor centralizes one operation (e.g., serialization) into one class. The GoF motivation explicitly states the problem Visitor solves: distributing operations across node classes makes a system hard to understand. This is the anatomy's "sprawled over everywhere" named as an architectural defect. Visitor is partial prior art for the single-point-of-emission idea, but it centralizes per-operation (one visitor class per operation), not per-output-type. Multiple visitors can coexist; the single canonical output trait under the anatomy is stronger than one-visitor-per-operation.

### 7e. What Was Not Found

No named principle was found in the literature for "single point of emission" in the sense the anatomy uses. The Single Writer Principle (Martin Thompson, 2011, https://mechanical-sympathy.blogspot.com/2011/09/single-writer-principle.html) applies to concurrency — one execution context owns mutations to any item of data — not to the architecture of output logic:

> "The Single Writer Principle is that for any item of data, or resource, that item of data should be owned by a single execution context for all mutations."

This is orthogonal. The anatomy's "under one trait, in one place" for output logic appears to be a gap in the named literature. The closest enforcement is the Rust type system's one-impl-per-trait-per-type rule, which makes the property structural rather than named. No single statement in the surveyed literature names and argues for the principle as the anatomy states it.

## 8. Rust and Haskell Examples

### 8a. Parse, Don't Validate (Alexis King, 2019)

**Source:** https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

This is the most precise existing statement of the anatomy's Part 2 in the programming community. Key verbatim quotes:

> "the difference between validation and parsing lies almost entirely in how information is preserved."

> "a parser is just a function that consumes less-structured input and produces more-structured output."

> "a value of type `NonEmpty a` [is] like a value of type `[a]`, plus a proof that the list is non-empty."

> "write functions on the data representation you *wish* you had, not the data representation you are given."

This last quote is the anatomy's wishful-thinking principle stated directly in King's post.

On what the approach provides:

> "The error can only occur in one place, rather than potentially throughout the entire codebase."

**Mapping.** This is the anatomy's Part 2 stated precisely: the raw input (Part 1) is parsed into a coherent named type (Part 2) that makes invalid states unrepresentable. Every downstream consumer of that type can trust its invariants. King does not address Part 3 in this post — she is writing about input parsing, not output assembly. The post stops at Part 2.

**What the skill can take.** King's "parse, don't validate" is the closest existing named principle for Part 2. Her formulation "a parser is just a function that consumes less-structured input and produces more-structured output" maps directly to Part 1 → Part 2. The anatomy can extend this: what King does for input (parse into a coherent named type), the anatomy also demands for output (assemble into a coherent named type before emission). The extension is symmetric but not yet named anywhere in the literature.

### 8b. The `prettyprinter` / Doc Type (Wadler-Lindig / Haskell)

**Sources:**
- Wadler, "A Prettier Printer" (1998): https://homepages.inf.ed.ac.uk/wadler/papers/prettier/prettier.pdf
- `prettyprinter` Hackage: https://hackage.haskell.org/package/prettyprinter-1.7.1/docs/Prettyprinter.html

The Hackage documentation states the phase separation explicitly:

> "The workflow proceeds through distinct phases: (1) Construction — users build documents using primitives like `vsep`, `pretty`, `<+>`, `nest`, and `align`; (2) Layout — layout algorithms (such as `layoutPretty`) convert the rich `Doc` into a `SimpleDocStream`; (3) Rendering — renderers transform the simple stream into terminal output, plain text, HTML, or other formats."

On why `Doc` must be a first-class assembled type (from the Hackage documentation):

> "Making `Doc` a first-class type assembled before layout allows the `group` function to work: it 'tries laying out x into a single line by removing the contained line breaks; if this does not fit the page... x is laid out without any changes.' The system can explore alternative arrangements because the complete document structure exists as a value ready for inspection and manipulation."

The `Doc` type is "a non-empty set of possible layouts of a document." This makes `Doc` the anatomy's Part 3 with precision: it is not a description of a single output, but of all possible formatted outputs, allowing the layout algorithm to select among them. The selection must happen before rendering, which requires having the complete `Doc` assembled first.

This is the anatomy's Parts 3 and 4 in a widely-used library: `Doc` is the coherent output type (Part 3), and `layoutPretty` followed by the renderer is the simple emission operation (Part 4). The Hackage documentation is, outside of compiler literature, the clearest explicit statement of "build the coherent output type completely, then emit" as a design rationale.

**What the skill can take.** The `prettyprinter` documentation is the strongest non-compiler prior art for Parts 3 and 4. It names the phases, explains why the coherent output type must exist before emission (the `group` function needs to inspect the whole), and demonstrates the pattern in a widely-used production library. The `Doc`/`SimpleDocStream`/rendered-string pipeline is the anatomy's Part 3 → Part 4 transition made concrete.

### 8c. matklad on rust-analyzer Architecture

Alex Kladov (matklad) writes about rust-analyzer's architecture at https://matklad.github.io/. Rust-analyzer uses a series of lowering passes (text → green tree → red tree → HIR → type inference artifacts → MIR for specific analyses), mirroring rustc's staged lowering. The architecture is demand-driven: Salsa (the incremental computation framework) evaluates queries lazily, pulling results through the graph only when demanded. This is the anatomy's pull model and staged coherent types instantiated in a major real-world Rust project.

## 9. Synthesis

### The Closest Prior Art

The compiler tradition (LLVM, GHC, rustc, the Dragon Book, nanopass) is the closest and most complete prior art for the four-part anatomy. It maps all four parts precisely, names each stage, and provides both positive examples (LLVM IR as sole interface) and negative examples (GCC reaching back into source-level trees during emission). The nanopass framework turns the four-part shape into a formal requirement enforced by a DSL. GHC's Core is the clearest real-world example of a "coherent assembled input type": a complete, minimal language into which all of Haskell is translated before any optimization runs.

Among the software-design traditions, the closest is a combination of:
- Alexis King's "parse, don't validate" (Part 2 precisely named)
- Haskell IO monad (Part 3 precisely named and formally modeled)
- SICP wishful thinking (the design direction — write core before input pipeline exists)
- Seemann's Recawr formulation ("once you start writing, don't go back to reading")

### The Sharpest Gap Between Prior Art and the Anatomy

**The gap is in Parts 2 and 3 as type-topology requirements, not just ordering/purity constraints.**

Every prior-art body places some constraint on the input→core→output pipeline. The functional core / imperative shell and impureim sandwich constrain it by purity (no side effects in the core). Hexagonal architecture constrains it by dependency direction (inside must not depend on outside). The compiler tradition constrains it by the IR's completeness (the IR is the only interface). All of these are property constraints on what the boundary must exclude.

The anatomy adds a type-topology constraint: the boundary must be a single named type that assembles everything the core needs (Part 2) or everything that will be emitted (Part 3). This is not a purity constraint, a dependency constraint, or a completeness constraint — it is a structural claim about the form of the boundary. A program can satisfy FCIS, impureim sandwich, hexagonal architecture, and even LLVM-style IR separation while passing multiple parameters (not a single named type) across each boundary. The anatomy's prescription — assemble into a single coherent named type — is not equivalent to any of the prior-art property constraints.

No prior-art body names this as a pattern. The closest individual examples are:
- Haskell IO (`IO a` is a single named type representing the complete output description)
- GHC Core (a single named intermediate language representing the complete input to optimization)
- Martin's InputData/OutputData DTOs (named types at use-case boundaries, but not prescribed as the general principle)
- King's "parse, don't validate" (single named input type, but not extended to output)

The anatomy unifies these into a single principle and applies it to all machines, not just compilers or Haskell programs.

**The second gap is in Part 4's "under one trait" requirement.**

Prior-art bodies say output must be separated from computation (SRP), or that all mutation lives in the shell (FCIS), or that the emitter is a named stage (AsmPrinter in LLVM). None state that emission must be placed under one trait, reviewable in one place. The Rust type system enforces one impl per trait per type, which makes Display and Serialize the closest examples. But the principle itself — that the entirety of output logic for a given coherent output type must live under one trait — is not named anywhere in the surveyed literature.

### What the Skill Can Take

The following direct quotations and formulations are available for use:

1. For the backwards-design principle:
   - Beck: "You take the input tape, manually type in the output tape you expect, then program until the actual output tape matches the expected output." (TDD origin of backwards design)
   - SICP: "We are using here a powerful strategy of synthesis: wishful thinking." (permission to write the core before the input pipeline)

2. For Part 2 (coherent input type):
   - King: "A parser is just a function that consumes less-structured input and produces more-structured output." / "Use a data type that makes illegal states unrepresentable."
   - LLVM: "LLVM IR is the only interface to the optimizer." (the IR as the coherent assembled input)
   - GHC: "yet we can translate all of Haskell into Core." (everything collapses into one named intermediate type)

3. For Part 3 (coherent output type, assembled before emission):
   - Yorgey: "A value of type `IO a`, in and of itself, is just an inert, perfectly safe thing with no effects. It is just a description of an effectful computation." (the coherent output type as an inert description)
   - Taylor: "Read the input object files... Build a symbol table... Decide where all the contents should go... Write the result." (all assembly before writing)

4. For the failure mode of absent Part 3:
   - Lattner on GCC: "when the GCC code generator goes to emit DWARF debug information, it reaches back and walks the source level 'tree' form." (this is what output logic sprawled everywhere looks like in production code)

5. For the ordering constraint (Seemann's sharpest contribution):
   - Seemann: "Once you start writing data to the network, to disk, to a database, or to the user interface, you shouldn't go back to reading in more data."

6. For Part 4 under one trait:
   - Martin: "This is the reason we do not put SQL in JSPs. This is the reason we do not generate HTML in the modules that compute results."
   - Rust Display: "Because a type can only have one `Display` implementation..." (type-system enforcement of the principle)

7. For concrete project examples:
   - GHC Core (Haskell) — the single coherent input type, as real as it gets
   - rustc MIR: "all of that logic is centralized in MIR construction, and the later passes can just rely on that"
   - rust-analyzer (Kladov) — Salsa demand-driven evaluation with staged named types
   - Haskell `prettyprinter` — `Doc` as a coherent output type, rendering as emission

### A Note on Terminology Overlap

Several traditions use "functional" or "pure" as their central term, while the anatomy uses "coherent." These terms are not synonyms. A function can be pure (no side effects) without its input or output being a single named assembled type. A type can be coherent (assembled from parts into a whole) without the transformation being pure. The anatomy's primary claim is about type topology, not about computational properties. When the skill cites prior art from the functional programming tradition, it should be clear that the anatomy uses these traditions as examples of the type-topology principle, not as arguments that the core must be a pure function in the FP sense.

## Appendix: Source Status Summary

Witnesses are quotes extracted directly from the named URL. Claims are attributed but not directly verified by page fetch.

| Source | Key Claim | Status |
|--------|-----------|--------|
| Bernhardt, DAS talk description | "simple values... not just for holding data, but also as the boundaries" | Witnessed |
| Bernhardt, DAS screencast description | Twitter client with functional core, imperative shell | Witnessed |
| Seemann, 2020 blog | "first perform all impure actions... then call that pure function... finally perform impure actions" | Witnessed |
| Seemann, 2025 Recawr | "Once you start writing... you shouldn't go back to reading" | Witnessed |
| Cockburn, 2005 original | "converts it into a usable procedure call or message" | Witnessed (multiple independent reproductions) |
| Martin, 2012 blog | "data can simply be arguments in function calls" | Witnessed |
| Martin, 2017 book InputBoundary | "Controller packages that data into a plain old Java object" | Claimed (book notes, not direct read) |
| Lattner, AOSA vol. 1 | "LLVM IR is... the only interface to the optimizer" | Witnessed |
| Lattner, AOSA vol. 1 | GCC "reaches back and walks the source level tree form" | Witnessed |
| Marlow/Peyton Jones, AOSA vol. 2 | "translate all of Haskell into Core" | Witnessed |
| rustc dev guide | "all of that logic is centralized in MIR construction" | Witnessed |
| Abelson/Sussman, SICP 2.1.1 | "We are using here a powerful strategy of synthesis: wishful thinking" | Witnessed |
| Beck, Canon TDD | "manually type in the output tape you expect, then program until..." | Witnessed |
| Gray, 1981 transaction paper | "either all actions are done... or none of the effects... survive" | Witnessed |
| Taylor, linkers blog | Read all, build symbol table, decide layout, then write | Witnessed |
| Yorgey, CIS194 | "just an inert, perfectly safe thing with no effects... just a description" | Witnessed |
| King, lexi-lambda blog | "parse, don't validate" / "makes illegal states unrepresentable" | Witnessed |
| Rust std docs, Display | "a type can only have one Display implementation" | Witnessed |
| Martin, SRP blog | "we do not generate HTML in the modules that compute results" | Witnessed |
| GoF Builder intent | "separate the construction of a complex object from its representation" | Witnessed (Wikipedia attribution) |
| GoF Visitor motivation | "distributing all these operations across the various node classes leads to a system that's hard to understand" | Witnessed (Wikipedia attribution) |
| Dragon Book, analysis-synthesis model | Front-end produces IR; back-end consumes IR to produce target code | Claimed (secondary summaries; text not directly fetched) |
| Nanopass framework | "each with a well-defined input and output language" | Witnessed (SIGPLAN blog) |
| Haskell HaskellWiki, lazy evaluation | "driven by demand: the evaluation of a term depends on how much of its result will be needed" | Witnessed |
