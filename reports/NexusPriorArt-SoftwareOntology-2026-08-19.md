# Prior Art: Software Ontology via Traits, Types, and Specification-First Design

**Date:** 2026-08-19  
**Scope:** Research into prior art relevant to designing coherent trait/typeclass ontologies in software, the anti-patterns that arise from mindless trait proliferation, knowledge-ontology methodologies, and specification-first workflows.

---

## 1. Ontology in Code via Type Classes, Traits, and Protocols

### 1.1 Haskell: Typeclasses and the Typeclassopedia

The **Typeclassopedia** (Brent Yorgey, *The Monad.Reader* issue 13, 2009) is the canonical community document on Haskell's typeclass hierarchy.  
Canonical URL: https://wiki.haskell.org/Typeclassopedia  
PDF: https://wiki.haskell.org/wikiupload/e/e9/Typeclassopedia.pdf

Criteria stated or implied for a *good* typeclass hierarchy in Haskell:

- **Laws are mandatory.** Every typeclass must come with formal equational laws. `Functor` requires Identity (`fmap id = id`) and Composition. `Monad` has its own set. Code that typechecks but violates the laws is invalid, not merely bad style.
- **Canonical uniqueness.** A given type has at most one valid `Functor` instance, provable via free theorems. Ambiguous instances are a design smell.
- **Category-theoretic grounding.** The hierarchy tracks mathematical structures, not implementation convenience. `Functor` maps to categorical functor; `Applicative` lies between functor and monad — mirroring the true mathematical containment.
- **Structural hierarchy.** As of GHC 7.10, `Applicative` is a superclass of `Monad` and `Functor` is a superclass of `Applicative`, encoding the real mathematical relationship in the type system.

The **numeric tower** (`Num`, `Real`, `Integral`, `Fractional`, `Floating`) is widely cited as a *bad* hierarchy: no laws are attached to `Num`; the hierarchy does not mirror genuine algebraic structure; `Integral` and `Fractional` ought to be disjoint but the language cannot enforce it. See: "The numeric tower fiasco" https://mmapped.blog/posts/23-numeric-tower-fiasco  
The `numeric-prelude` package proposes a replacement built on real algebraic structures (`Additive`, `Ring`, `Field`): https://hackage.haskell.org/package/numeric-prelude

**Inference:** The community contrast between the praised Functor/Monad tower and the condemned numeric tower reveals the criterion: good hierarchies have mathematical laws; bad ones do not.

John A. De Goes states the criteria directly: typeclasses should be (1) principled — have laws; (2) minimal — few methods; (3) denotational — methods have clear meaning, not just use-case-driven.  
Source: https://degoes.net/articles/principled-typeclasses

### 1.2 Rust: Trait Design and the API Guidelines

Rust API Guidelines: https://rust-lang.github.io/api-guidelines/

The guidelines are almost entirely about *implementing* existing traits (C-COMMON-TRAITS: `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Debug`, `Display`, `Default`) and notably say little about when to introduce a *new* custom trait. The implicit answer: introduce a trait only when multiple unrelated types need a common contract that consumers write against generically.

**`Iterator`** is the model Rust trait: it requires one method only — `fn next(&mut self) -> Option<Self::Item>` — and all other methods (`map`, `filter`, `fold`, `zip`) are default implementations. This is the canonical Rust pattern: **minimal required surface; maximum derived behavior from blanket defaults**.  
Docs: https://doc.rust-lang.org/std/iter/index.html

**`From`/`Into`** are linked by a blanket impl: implementing `From` gives `Into` for free. Pattern: implement the fundamental direction; blanket impls derive the rest.

**Extension traits** (RFC 0445) are a recognized pattern when adding methods to a foreign type without orphan violations. Convention: name them `FooExt`.  
RFC: https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html

### 1.3 Scala: Cats Typeclass Hierarchy

Cats library: https://typelevel.org/cats/  
The hierarchy tracks Haskell's: `Functor` → `Apply` → `Applicative` → `FlatMap` → `Monad`; `Foldable` → `Traverse`.

Governing rule per RockTheJVM: **one fundamental capability per typeclass**.  
Source: https://rockthejvm.com/articles/cats-essential-type-class-hierarchy

The distinction between `Applicative` and `Monad` is canonical: Applicative embodies independent/concurrent computations; Monad embodies dependent/sequential ones. This distinction warrants the separate typeclass.

The Typelevel blog "Subtype type classes don't work" (2016) identifies a structural flaw in using Scala's subtyping to encode the hierarchy: it creates implicit ambiguity when multiple conversions have the same priority. The post quantifies the trade-off between ergonomics (keeping hierarchy) and correctness (breaking it to eliminate ambiguity).  
Source: https://typelevel.org/blog/2016/09/30/subtype-typeclasses.html

`cats-mtl` takes a different approach: use the weakest typeclass constraint that suffices, weakening down to `Functor` or `Applicative` wherever possible.  
Source: https://typelevel.org/cats-mtl/design.html

### 1.4 Swift: Protocol-Oriented Programming

Dave Abrahams, "Protocol-Oriented Programming in Swift," WWDC 2015 session 408.  
Apple developer page: https://developer.apple.com/videos/play/wwdc2015/408/  
WWDC Notes: https://wwdcnotes.com/documentation/wwdc15-408-protocoloriented-programming-in-swift/

Central claim: "Don't start with a class, start with a protocol." Criteria stated for good protocol design:

- **Value types first.** Protocols + structs avoid reference-sharing bugs.
- **Retroactive modeling.** A type can conform to a protocol defined after the type itself was written (impossible with class inheritance).
- **Protocol extensions.** Default implementations mean conforming types get behavior for free without inheritance.
- **Composition over inheritance.** A struct can conform to multiple protocols; a class can only inherit from one superclass.

Critical reaction: Rob Napier, "Protocols I: Start With a Protocol, He Said" (https://robnapier.net/start-with-a-protocol) warns that "start with a protocol" is often taken too far — protocols with associated types become difficult to use as types (only as constraints), and concrete types should be preferred when there is only one plausible implementation. **This is the Swift community's named criticism of premature protocol extraction — directly parallel to the designer's anti-pattern.**

### 1.5 Go: Interfaces

Rob Pike, "Go Proverbs," Gopherfest SV, November 18, 2015.  
Official proverbs list: https://go-proverbs.github.io/  
YouTube: https://www.youtube.com/watch?v=PAAkCSZUG1c

Key proverb: "The bigger the interface, the weaker the abstraction."  
Also: "interface{} says nothing" — the empty interface, satisfiable by everything, carries zero information.

Go's structural typing enforces discovery over design: an interface can be defined after the fact, once two types are observed to share a method. The standard library's `io.Reader` has one method: `Read(p []byte) (n int, err error)`. A type satisfies it without importing `"io"`. Interfaces are defined by consumers (callers), not producers (implementors).

Thoughtworks on Go interface mistakes: "In Go, you don't define what something *is* but what it *provides* — behavior, not things."  
Source: https://www.thoughtworks.com/insights/blog/programming-languages/mistakes-to-avoid-when-coming-from-an-object-oriented-language

Note: "Accept interfaces, return structs" does not appear on the official Go proverbs page; it is a widely attributed idiom, not a canonical proverb.  
Confirmation: https://github.com/go-proverbs/go-proverbs.github.io/issues/37

### 1.6 Clojure: Protocols

Official reference: https://clojure.org/reference/protocols  
Design rationale: https://clojure.org/about/runtime_polymorphism

Key distinction from Java interfaces: a Clojure protocol can be extended to any existing type — including final Java classes — from any namespace, without touching the type's source. This solves the Expression Problem (adding new types to old operations AND new operations to old types without modifying existing code). Java interfaces solve only one half.

Protocol dispatch is single — always on the type of the first argument. Faster than multimethods, more constrained.

### 1.7 Smalltalk: Protocols

In Smalltalk, "protocol" is a documentation and organizational convention for grouping related messages within a class — not a type-system construct. Common protocol names: `accessing`, `initialization`, `printing`, `testing`, `private`.

Research paper noting the gap: "Interfaces and Specifications for the Smalltalk-80 Collection Classes" observed that "message protocols have not been formalized... it is currently only a matter of style for protocols to be consistent from one class to another."  
Source: https://www.researchgate.net/publication/2409926_Interfaces_and_Specifications_for_the_Smalltalk-80_Collection_Classes

**Significance:** Smalltalk introduced the idea that an object's public interface — the set of messages it responds to — is a meaningful abstraction separate from the class hierarchy. It never elevated protocols to first-class type-system constructs; that step was taken by Java, Haskell, and Swift.

### 1.8 Cross-cutting criteria (inferred from the above, not stated by any single source)

Criteria that recur across communities:

1. **Laws** — a good abstraction comes with equational laws (Haskell, Cats).
2. **Minimal required surface** — the mandatory interface is as small as possible; defaults fill the rest (Rust `Iterator`, Go `io.Reader`, Swift protocol extensions).
3. **One capability per unit** — each trait captures exactly one composable idea (Cats' Applicative vs. Monad split; Go's single-method interfaces).
4. **Open extension without source modification** — good polymorphism lets you extend types you don't own (Clojure protocols, Go structural typing).
5. **Structural grounding** — the hierarchy mirrors mathematical or semantic structure, not implementation convenience.
6. **Consumer-side definition** — interfaces should be defined where they are used, not where types are implemented.

---

## 2. The Anti-Pattern: One Trait per Function / Interface for Everything

### 2.1 Speculative Generality

Martin Fowler, *Refactoring: Improving the Design of Existing Code* (1st ed. 1999; 2nd ed. 2018).  
Summary: https://xp123.com/speculative-generality/

Defined as: adding "all sorts of hooks and special cases to handle things that aren't required," justified by "we might need this someday." The interface-specific form: using "interface + abstract class + concrete class" for every type on the grounds of hypothetical future extension. Classified as a *Dispensable* smell — code that adds no current value.

Most diagnostic sign: the only caller of an abstraction is a test case. Remedy: delete both.

### 2.2 Header Interfaces

Martin Fowler, *HeaderInterface* bliki: https://martinfowler.com/bliki/HeaderInterface.html  
Martin Fowler, *RoleInterface* bliki: https://martinfowler.com/bliki/RoleInterface.html

**Header interface:** An interface that mimics the implicit public interface of a class — extracted mechanically by listing all public methods. Fowler's criticism: "force you to implement every method, even if you're not going to need them"; "don't communicate actual collaboration patterns." Contrast with **role interface**: defined by the needs of a consumer, not the capabilities of a provider.

Mark Seemann, "Interfaces are not abstractions" (2010): https://blog.ploeh.dk/2010/12/02/Interfacesarenotabstractions/

Seemann states: "Having only one implementation of a given interface is a code smell." He names this the **Reused Abstractions Principle (RAP)**: "If the only class that ever implements the Customer interface is CustomerImpl, you don't really have polymorphism and substitutability because there is nothing in practice to substitute."

### 2.3 Java's IFoo / FooImpl Pattern

Stephen Colebourne (author of `java.time`): https://blog.joda.org/2011/08/implementations-of-interfaces-prefixes.html

The `I`-prefix (IFoo, IService) is not idiomatic Java — it is a COM/C# convention. Idiomatic Java: the interface holds the clean name (`List`); the implementation gets the descriptive suffix (`ArrayList`, `LinkedList`). The `FooImpl` suffix signals premature abstraction: "Stop Naming Everything Impl" (https://softwareascraft.com/posts/stop-naming-everything-impl/) argues it duplicates the class definition without separating what from how, and the `Impl` class typically evolves into a god class.

### 2.4 Go Proverbs (see §1.5 above)

"The bigger the interface, the weaker the abstraction." — Rob Pike.  
https://go-proverbs.github.io/

### 2.5 Interface Segregation Principle — What It Actually Says and Its Misuse

Robert Martin, ISP (1996 paper; *Agile Software Development* 2002):  
Source: https://blog.ndepend.com/solid-design-the-interface-segregation-principle-isp/

**What ISP says:** "A client should not be forced to depend on methods it does not use." It targets fat interfaces that couple many clients to methods they never call.

**The misuse:** ISP is often read as a mandate to make every interface have one method, applied uniformly without identifying a concrete fat-interface problem. This produces interface proliferation — dozens of single-method interfaces that fragment a coherent abstraction without reducing coupling.

Seemann's resolution: when ISP is applied rigorously, you naturally arrive at single-method interfaces — but only after identifying what each consumer actually needs, not by mechanical splitting.  
Source: https://blog.ploeh.dk/2014/03/10/solid-the-next-step-is-functional/

### 2.6 Named Criteria for When an Abstraction Deserves to Exist

**Rule of Three** (Don Roberts, via Fowler's *Refactoring*):  
https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)  
Abstract only after the third occurrence of a pattern. Two data points cannot determine a true pattern versus coincidental similarity.

**"The Wrong Abstraction"** (Sandi Metz, 2016):  
https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction  
Criterion of degradation: "If you find yourself passing parameters and adding conditional paths through shared code, the abstraction is incorrect." Diagnostic pattern: a clean abstraction gets stretched by new requirements via parameters and conditionals until it becomes a "condition-laden procedure which interleaves a number of vaguely associated ideas." Remedy: inline back to duplication; let cleaner abstractions emerge.

**Fowler's negative criterion:** An abstraction does not deserve to exist when its only users are test cases (*Speculative Generality*).

### 2.7 Summary of Named Terms

| Term | Source | What it names |
|---|---|---|
| Speculative Generality | Fowler, *Refactoring* | Abstraction added for hypothetical future use |
| Header Interface | Fowler bliki; Seemann | Interface mechanically mirroring all public methods of one class |
| Role Interface | Fowler bliki | Interface defined by a consumer's actual needs |
| Reused Abstractions Principle (RAP) | Seemann | If only one class implements an interface, it is not a real abstraction |
| Rule of Three | Don Roberts via Fowler | Abstract only after the third occurrence |
| Wrong Abstraction | Sandi Metz (2016) | Abstraction stretched past its natural scope via parameters and conditionals |

---

## 3. Knowledge-Ontology Methodologies and Their Transfer to Code

### 3.1 OntoClean (Guarino and Welty, 2002–2004)

Key papers:
- Guarino, N. and Welty, C. (2002). "Evaluating ontological decisions with OntoClean." *Communications of the ACM* 45(2): 61-65.  
  PDF: https://www.loa.istc.cnr.it/old/Papers/GuarinoWeltyOntoCleanv3.pdf  
  ResearchGate: https://www.researchgate.net/publication/297428382_Evaluating_ontological_decisions_with_ontoclean
- Wikipedia overview: https://en.wikipedia.org/wiki/OntoClean

OntoClean assigns four meta-properties to every class before accepting it into an ontology:

- **Rigidity (+R / -R / ~R):** A property is rigid if all instances hold it necessarily — they cannot lose it without ceasing to exist. *Person* is rigid (+R); *Student* is anti-rigid (-R) because someone can stop being a student while remaining a person.
- **Identity (+I / -I):** Does the class supply an identity criterion — a principled answer to "when are two instances the same individual"? *Person* carries identity (+I). Properties like *Red* or *Tall* do not (-I).
- **Unity (+U / -U):** Does every instance constitute a unified whole under a common unity criterion?
- **Dependence (+D / -D):** Is each instance's existence ontologically dependent on something external?

The ontological punchline: a class that is anti-rigid (-R, like *Role*, *Student*, *Employee*) cannot subsume a rigid class (+R, like *Person*). **Roles cannot be supertypes of types.** This is the formal grounding for "a role is not a real noun." Four canonical categories result:

| Category | Rigidity | Identity | Example |
|---|---|---|---|
| Type (Sortal) | +R | +I | Person |
| Role | -R | +I | Student, Employee |
| Mixin | -R | -I | PhysicalObject cutting across unrelated types |
| Category | +R | -I | (rare; rigid but no identity criterion) |

Identity criteria: the answer to "If a and b are Ks, what are the necessary and sufficient conditions for a = b?" Without an identity criterion, a class is ontologically suspect as a first-class entity.

Tutorial for applying OntoClean in OWL: https://people.cs.uct.ac.za/~mkeet/OEbook/ontocleantutorialOE19.pdf

### 3.2 Methontology

Overview: https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0186-10422019000500015

Methontology defines these sequential activities before implementation:

1. **Specification** — document purpose, scope, competency questions.
2. **Conceptualization** — build a glossary of terms; build concept taxonomies; build binary relation diagrams; produce a concept dictionary with attributes and relations described in detail. This is pre-formal — done in natural language and semi-formal tables before any code.
3. **Formalization** — convert the conceptual model into a formal or semi-computable model.
4. **Integration** — reuse existing ontologies.
5. **Implementation** — encode in an implementation language (e.g., OWL).
6. **Maintenance**.

The conceptualization step is the workflow for designing concepts before implementing them: it forces enumeration of every concept, every binary relation, and every attribute before touching code.

### 3.3 NeOn Methodology

Homepage: https://oeg.fi.upm.es/index.php/en/methodologies/59-neon-methodology/index.html  
Suárez-Figueroa et al. (2015): https://journals.sagepub.com/doi/abs/10.3233/AO-150145

Rather than a single rigid workflow, NeOn proposes nine scenarios covering different starting situations (from scratch, reusing existing ontologies, reusing ontology design patterns, aligning multiple ontologies, re-engineering non-ontological resources). Its primary target is *ontology networks* rather than single ontologies. It is scenario-driven rather than phase-driven.

### 3.4 BFO and DOLCE: Roles vs. Types

DOLCE key paper: Gangemi et al., "Sweetening Ontologies with DOLCE" (2002).  
ResearchGate: https://www.researchgate.net/publication/221630979_Sweetening_ontologies_with_DOLCE  
DOLCE journal paper (2022): https://arxiv.org/pdf/2308.01597

BFO: Arp and Smith, "Realizable Entities in Basic Formal Ontology."  
PDF: http://ontology.buffalo.edu/smith/articles/realizables.pdf

In **DOLCE**, roles are anti-rigid: an entity may play a role for a limited time without changing its identity. Roles are also *founded* — they have a relational nature and depend on other entities and contexts. The class *Doctor* is a role; *Person* is a type. The same individual is a Person permanently (type/sortal) but is Doctor only relationally and contingently (role). If something can cease to be a member of class C without ceasing to exist, C is a role, not a type.

In **BFO**, the corresponding distinction is between *Continuants* (things that persist through time) and *Realizable entities* (dispositions, functions, roles). A role in BFO *inheres in* its bearer but is not essential to it.

Both BFO and DOLCE agree: **roles are not types**. Types define what a thing essentially is; roles define what a thing happens to be in a context. Encoding a role as a class that subsumes a type class is a structural error both frameworks diagnose and prohibit.

### 3.5 Description Logics

Standard DLs (the logics underlying OWL) have no built-in mechanism to express identity criteria. A DL class is simply a set of individuals satisfying a description. This is precisely the gap that OntoClean fills on top of DL-based systems — it adds meta-properties that DL cannot express natively.

OWL DL enforces a strict type separation (a class cannot also be an individual or property) but does not address whether a given class node represents a genuine kind with identity criteria versus a role or attribute cluster.

The Keet tutorial shows how to operationalize OntoClean's meta-properties using OWL annotations and a DL reasoner to catch structural errors OntoClean identifies conceptually.  
Source: https://people.cs.uct.ac.za/~mkeet/OEbook/ontocleantutorialOE19.pdf

### 3.6 Domain-Driven Design (Eric Evans)

Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software.* Addison-Wesley. ("The Blue Book.")  
Free reference: https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf

DDD's central claim: types in software should emerge from language negotiated with domain experts, not from technical convenience. Key concepts:

- **Ubiquitous Language:** Every class name, method name, and module name must come from a shared language agreed with domain experts. A change in the language is a change to the model.
- **Bounded Context:** Language is only precise within a boundary. The same word may mean different things in different bounded contexts (billing vs. support vs. shipping). Crossing boundaries requires explicit translation maps.
- **Entities vs. Value Objects:** Objects with identity that persists through state change (Entities) vs. objects defined purely by attributes (Value Objects). This parallels the OntoClean distinction between types with identity criteria and those without.
- **Aggregates:** Clusters of objects treated as a single unit for consistency. The aggregate root is the only externally addressable entity — encoding ontological commitment about what constitutes an independent identifiable thing.

### 3.7 "Make Illegal States Unrepresentable"

Origin: Yaron Minsky, "Effective ML" talk at Harvard CS51 (2010).  
Video: https://vimeo.com/14313378  
Minsky confirming origin: https://x.com/yminsky/status/1852756565729612137  
Jane Street blog: https://blog.janestreet.com/effective-ml-revisited/

Scott Wlaschin's elaboration in F#: https://fsharpforfunandprofit.com/posts/designing-with-types-making-illegal-states-unrepresentable/  
Wlaschin's book: *Domain Modeling Made Functional* (Pragmatic Programmers, 2018): https://pragprog.com/titles/swdddf/domain-modeling-made-functional/

Minsky's point: the type system should make certain states inexpressible, not merely guarded by runtime assertions. Canonical example: replace `{verified: bool; verified_at: date option}` (where `verified=false, verified_at=Some(...)` is legal but invalid) with a sum type `Unverified | Verified of date` so the invalid combination cannot be constructed. **Type design as ontology:** the type system should reflect real-world constraints about which combinations of properties can coherently coexist.

### 3.8 Type-Driven Development (Edwin Brady, Idris)

Brady, E. (2017). *Type-Driven Development with Idris.* Manning Publications.  
Manning page: https://www.manning.com/books/type-driven-development-with-idris  
CoRecursive podcast interview: https://corecursive.com/006-type-driven-development-and-idris-with-edwin-brady/

Brady's method: write the types of functions first, leaving holes that the compiler fills by providing types. The types are the specification from which the implementation is derived. Idris has dependent types, so a type like `Vect n a` (a vector of exactly `n` elements of type `a`) encodes a cardinality constraint verified statically.

The workflow:
1. Define types (the what and the contract).
2. Use the type-checker's hole-filling mechanism interactively to discover what implementation terms are needed.
3. Types act as specification; compiler inference acts as verification.

**This is the closest prior art for a formal "types and traits first" design workflow.**

### 3.9 Algebraic Data Types as Ontology / Domain Modeling

Thoughtworks two-part series: https://www.thoughtworks.com/en-us/insights/blog/microservices/domain-modeling-algebraic-data-types-pt1  

The central claim: sum types (OR types, `Shape = Circle | Rectangle | Triangle`) model mutually exclusive cases in the domain; product types (AND types, `Point = { x: Float; y: Float }`) model things that must always coexist. Properties:

- **Exhaustiveness:** A sum type enumerates all valid states; the compiler enforces that every state is handled.
- **No null:** Absence is modeled as a type variant (`Option<T>`), not a sentinel value.
- **No illegal combinations:** Structure prevents invalid compositions.

Sum types correspond to disjoint union in OWL (`owl:disjointUnionOf`); product types correspond to intersection/conjunction (`owl:intersectionOf`). The connection to formal ontology is structural.

Wlaschin's *Domain Modeling Made Functional* is the most complete book-length treatment, walking through F# domain modeling with ADTs following DDD principles.  
Source: https://pragprog.com/titles/swdddf/domain-modeling-made-functional/

---

## 4. Design the Types and Traits First, Then Implement

### 4.1 Haskell: "Write the Types First"

Gabriella Gonzalez, "Haskell for all" blog: https://www.haskellforall.com  
Her posts "The category design pattern" (2012) and "Scalable program architectures" (2014) argue that types and their algebraic laws precede and constrain implementation.

Sandy Maguire, *Algebra-Driven Design* (Leanpub, 2020): "it is possible to understand everything about a library before even a single line of code is written to implement it." The method defines algebraic laws first, then a reference implementation, then the real implementation.  
Source: https://leanpub.com/algebra-driven-design  
Companion Hackage library: https://hackage.haskell.org/package/algebra-driven-design

Maguire, *Thinking with Types: Type-Level Programming in Haskell* (2018): frames type design as the primary intellectual act.  
Source: https://leanpub.com/thinking-with-types

### 4.2 Idris: Type-Driven Development (see §3.8 above)

The hole-based workflow is the formal procedural expression of "design with types first."

### 4.3 Liskov and Zilles (1974) — "Programming with Abstract Data Types"

Liskov, B. and Zilles, S. "Programming with Abstract Data Types." *Proceedings ACM SIGPLAN Symposium on Very High Level Languages*, March 1974. DOI: 10.1145/800233.807045.  
Full text PDF: https://dl.acm.org/doi/pdf/10.1145/800233.807045  
Morning paper summary: https://blog.acolyer.org/2016/10/20/programming-with-abstract-data-types/

Key sentence: "In the case of programming, the use which may be made of an abstraction is relevant; the way in which the abstraction is implemented is irrelevant." This is the definitional statement of specification-implementation separation for data types — what an ADT *does* can be specified entirely without specifying *how* it is realized in memory.

### 4.4 Parnas (1972) — Module Decomposition and Information Hiding

Parnas, D.L. "On the Criteria To Be Used in Decomposing Systems into Modules." *CACM* 15(12), December 1972, pp. 1053–1058.  
Full text PDF: https://wstomv.win.tue.nl/edu/2ip30/references/criteria_for_modularization.pdf

Core argument for interface-first design: each module should be defined by what it *hides* from all other modules — a "design decision which is likely to change." The module interface must "reveal as little as possible about its inner workings." The interface is the design artifact; the implementation is a private detail replaceable independently.

Parnas explicitly proposes beginning with a list of design decisions to hide, designing interfaces around that list, and only then implementing module bodies.

### 4.5 Meyer — Design by Contract

Meyer, B. "Applying 'Design by Contract.'" *IEEE Computer* 25(10), October 1992, pp. 40–51.  
ACM/IEEE DL: https://dl.acm.org/doi/10.1109/2.161279  
*Object-Oriented Software Construction* (2nd ed.): https://bertrandmeyer.com/wp-content/upLoads/OOSC2.pdf

Every routine has a contract — preconditions (what the caller must guarantee), postconditions (what the routine guarantees on return), and class invariants. Writing contracts before implementation is the method: commit to observable behavior first, then write the body. Meyer's language Eiffel makes contracts first-class syntax.

### 4.6 CLU — Cluster Specifications and Bodies

Liskov, B. "A History of CLU." MIT LCS TR-561, April 1992.  
PDF: https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-561.pdf  
ACM HOPL-II: https://dl.acm.org/doi/10.1145/234286.1057826

In CLU, every abstract data type is a *cluster* with a cluster header (type name and operation signatures — the specification) and a cluster body (representation type and implementation). The representation (`rep`) type is entirely hidden. Liskov frames program development as a sequence of well-specified abstractions that can each be reasoned about independently of their implementations. **CLU is the first language to formally separate ADT specification from body in this way.**

### 4.7 Standard ML — Signatures and Functors

Milner, Tofte, Harper, MacQueen. *The Definition of Standard ML (Revised).* MIT Press, 1997.  
1990 edition PDF: https://smlfamily.github.io/sml90-defn.pdf  
Tofte tutorial: https://www.cs.tufts.edu/comp/105-2017f/readings/tofte-tips.pdf

In SML, a *signature* is a specification of a module — it declares type names, value names, and their types, without any implementation. A *structure* is an implementation of a signature. *Functors* are functions from structures to structures, parameterized by signatures. Code can be written that depends only on a signature long before any structure (implementation) exists. This is the SML module system as a specification-first workflow.

### 4.8 OCaml — .mli Files as Interface Specifications

*Real World OCaml* — Files, Modules, Programs: https://dev.realworldocaml.org/files-modules-and-programs.html  
Official OCaml modules docs: https://ocaml.org/docs/modules

A `.mli` file defines the type of module `Foo`; `foo.ml` is the implementation. *Real World OCaml*: "When designing an mli file, you can choose whether to expose the concrete definition of your types or leave them abstract. Most of the time, abstraction is the right choice." The `.mli` file is recommended as the first artifact to write when designing a module — it is the specification.

### 4.9 Ada — Package Specifications and Bodies

Ada modular programming: https://learn.adacore.com/courses/intro-to-ada/chapters/modular_programming.html  
ARM section 7.2: https://ada-lang.io/docs/arm/AA-7/AA-7.2/

A package specification (`.ads`) declares all public names, types, and subprogram signatures. A package body (`.adb`) provides the implementations. The specification is compiled independently of and prior to the body. Ada makes interface-before-implementation not merely possible but structurally enforced: you cannot write a body until its specification is accepted by the compiler.

### 4.10 "Parse, Don't Validate" (Alexis King, 2019)

King, A. "Parse, don't validate." November 5, 2019.  
https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

A *validator* checks a condition and returns a boolean, discarding evidence. A *parser* checks the same condition but encodes the evidence in a more precise type — the result type makes the constraint structural and permanent. The design principle: before implementing behavior, design types so that the type system itself enforces invariants. This is specification-first in the sense that the type design *is* the specification.

---

## Summary: The Lineage

| Source | Year | What they separate and how |
|---|---|---|
| Parnas | 1972 | Module interface (what is hidden) designed before body |
| Liskov/Zilles, CLU | 1974–75 | ADT specification (use) separated from representation (implementation) |
| Hoare logic / Meyer | 1969 / 1988 | Pre/postconditions/invariants committed before writing body |
| SML signatures | 1984–90 | Module signatures as formal compiler-checked specifications preceding structures |
| Ada package specs | 1983 | Spec compiled before body; language-enforced separation |
| OCaml .mli | 1996 | Module interface file recommended as first artifact |
| Haskell culture | 2000s– | Write type signatures first; typeclass laws as pre-implementation constraints |
| Brady/Idris | 2013–17 | Holes as a formal workflow tool for top-down type-first construction |
| Gonzalez, Maguire | 2012–20 | Algebraic laws first; everything about a library knowable before implementation |
| King | 2019 | Type design is the specification |

---

*Researched 2026-08-19. Every claim carries its source. Observations and inferences are kept distinct. No design proposals for the subject system are made here.*
