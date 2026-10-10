# Trait Vision Misread Research

Date: 2026-08-20
Design session: 2b34fafa
Research directed by: psyche

## Psyche Statements (verbatim)

Design session 2b34fafa, typed, 2026-08-20:

> "You misunderstood the trait based approach. your trait methods are just regular functions pretending to be traits. if the type needs a 'name' to resove the import, then it's not resolvable. So we found one of the cornerstone of models not understand my vision. Do a research in this"

Design session e06e4c07, dictated, 2026-08-19:

> "when we introduced the mandatory traits... the first implementation just simply created placeholder traits for every function, and just sort of mindlessly created traits that don't create a sensible ontology. And there's going to have to be a lot to be done in terms of creating training for this to be understood better by agents, and also creating a workflow for this, for any ontology to be designed properly before it's implemented."

traitsAsCapabilities.md, 2026-08-18:

> "realize isnt implemented by the same type as textualize. if you cant find two different types, the implementation is wrong. You dont textualize the text, and you dont realize the realized data."

rustComponentArchitecture.md, 2026-08-18:

> "Using mechanical tests isnt going to create good ontology; trait/types design is ontology in code."

traitsAsCapabilities.md, 2026-08-13:

> "we need to think very carefully of what the types are. First, really, because the traits are something that the types implement. We don't look for traits and then think of types for that."


## Question 1 — What the Misunderstanding Is Made Of

### The distinction

A capability trait: `self` IS the thing that has the capability. The trait is an ontological statement — this type is resolvable, displayable, iterable. The method signature is `fn verb(&self) -> Result`. The implementing type has an intrinsic relationship to the operation; laws can be stated about it.

A function-shaped trait (the misread): `self` is a service holder or configuration bag. The real subject of the capability is passed as a parameter: `fn resolve(&self, name: &str) -> Import`. The struct is a dispatch namespace. No law relates the implementing type to the operation. It is a regular function with an extra `self` for DI or namespacing.

The import resolution case is a clean illustration. The psyche's statement — "if the type needs a 'name' to resolve the import, then it's not resolvable" — identifies the symptom precisely: the real subject (the import reference, the thing that needs resolving) is not the receiver; it is the parameter. The type that carries the name IS what is resolvable. A correct capability trait would be implemented on the import reference: `fn resolve(&self) -> ResolvedImport` where `self` IS what needs resolving.

The Realize/Textualize ruling (2026-08-18) is the same principle applied to type assignment: "You dont textualize the text, and you dont realize the realized data." The textual type carries Realize (it realizes into real form); the real type carries Textualize (it textualizes into textual form). When the same type implements both, it holds capabilities for which it is not the subject on at least one side.

### Sharpest existing formulations

**Tell Don't Ask — Martin Fowler**
URL: https://martinfowler.com/bliki/TellDontAsk.html

"Tell-Don't-Ask is a principle that helps people remember that object-orientation is about bundling data with the functions that operate on that data. It reminds us that rather than asking an object for data and acting on that data, we should instead tell an object what to do."

A service trait extracts data from the object (or passes data to the service) and acts on it from outside. A capability trait tells the object what to do; the object acts on itself. The difference is whether `self` is the subject or a bystander.

**Anemic Domain Model — Martin Fowler (2003)**
URL: https://martinfowler.com/bliki/AnemicDomainModel.html

"The fundamental horror of this anti-pattern is that it's so contrary to the basic idea of object-oriented design; which is to combine data and process together."

"The more behavior you find in the services, the more likely you are to be robbing yourself of the benefits of a domain model."

When a `Resolver` service's `resolve(name)` method holds all the logic, the import reference type becomes anemic — it holds data but no behavior. The behavior has been relocated to a service, which is precisely the misread.

**Alan Kay on messaging**
HN discussion: https://news.ycombinator.com/item?id=21852444

Kay: "The objects are the computers, and the messages are the instructions to those computers!" The receiver of a message IS the entity performing the computation. If you send `resolve` to an import reference, it resolves itself. Sending `resolve(import_ref)` to a Resolver routes the message to the wrong receiver.

**Standard library as the clearest Rust example**
URL: https://doc.rust-lang.org/book/ch10-02-traits.html

The Rust Book frames traits as "functionality a particular type has." Every standard trait follows the pattern: `Display` (the type displays itself), `Iterator` (the type yields its own items), `Clone` (the type clones itself), `Read`/`Write` (the type reads/writes itself), `FromStr` (the type parses itself). In no case is `self` a namespace; in every case `self` IS the subject. The stdlib is the available counter-example to the service trait pattern in idiomatic Rust.

**Principled type classes — John De Goes**
URL: https://degoes.net/articles/principled-typeclasses

"If you can't define laws for a type class, then it's not useful as an abstraction, and you should not try to define a type class."

A capability trait has natural laws: resolving a well-formed reference succeeds; the resolution is deterministic. A service trait like `trait Resolver` has no intrinsic laws — it is a bag of methods. The law test is a diagnostic.


## Question 2 — Where It Comes From in Models

### Finding: four reinforcing sources in training data

**1. Java/C# IService patterns imported into Rust**

The dominant enterprise architecture in Java and C# is: data types (DTOs, POJOs) holding no behavior, service types holding all behavior, interfaces extracted per service boundary for DI. This is the anemic domain model as architectural default. When a model trained on this corpus is told "every method lives under a trait," it applies the pattern it has seen most: extract a trait per service, put `self` as the service holder, pass the real subject as a parameter.

Julio Merino's "Rust traits and dependency injection" (https://jmmv.dev/2022/04/rust-traits-and-dependency-injection.html) explicitly maps Rust traits to "interfaces in other languages" and applies the DI pattern: "Use interfaces instead of concrete types as constructor parameters." This is a published, widely-read article that directly imports the IService habit into Rust.

**2. Mock-driven trait extraction**

The standard Rust testing workflow when using mockall or similar: write concrete code, extract a trait at the seam where a mock is needed, generate a mock implementation. The trait boundary is placed where the test requires a swap point, not where an ontological distinction exists. Traits produced by this workflow are inherently service-shaped — they cover a set of operations performed BY an object ON other things.

The entrait crate (https://docs.rs/entrait/latest/entrait/) was built precisely because this workflow produces the anti-pattern at scale. Its author acknowledges: "Dependency Injection is a strictly object-oriented concept that will often look awkward in Rust." The crate converts free functions into trait-generated form specifically to avoid service-object accumulation. This confirms mock-driven extraction mechanically generates function-shaped traits.

**3. Tower's Service trait as ecosystem precedent**

Tower's `Service` trait (`fn call(&self, req: Request) -> Future<Response>`) is Rust's most prominent service-style trait: `self` is middleware/handler infrastructure, and the real subject is the `req` parameter. This is a legitimate composition seam for middleware, but it has become a template. Models that have seen Tower extensively will reproduce the pattern in domains where it does not apply.

**4. LLM local-plausibility bias**

Research from Sonar (https://www.sonarsource.com/resources/library/llm-code-generation/) finds 62% of AI-generated code contains design flaws. The mechanism: LLMs complete patterns locally — they produce the next token that is plausible given the preceding context, weighted by training frequency. When the training corpus is dominated by service-layer Java/C# code and DI-pattern Rust, the locally plausible response to "add a trait for this behavior" is a service trait. Ontology-level design requires stepping back from local plausibility and asking what the types ARE before asking what they do. This is a non-local operation that models do not perform by default.

No study was found that specifically documents LLMs producing service traits in response to "use traits for everything" instructions. This is an unknown — the mechanism is strongly suggested by the training-data composition and local-plausibility findings, but direct evidence is absent.

### Interpretation (kept separate from findings)

The four sources reinforce each other. The model is not making a random error; it is applying the dominant pattern from its training distribution. "Every method under a trait" is a rule the model has no difficulty following — but it satisfies the rule at the function level (each function becomes a trait method) rather than at the ontological level (traits describe what types ARE). The psyche named this precisely: "mindlessly created traits that don't create a sensible ontology."

The distinction requires a prior question — "what are the types?" — that the model never asks when given a rule about traits. The psyche's design method (types first, 2026-08-13) is exactly the step that prevents the misread: enumerate the types, understand what each IS, then determine what capabilities belong on which type.


## Question 3 — What Corrects It

### Prior art: behavior lives with its subject

**Tell Don't Ask (Fowler)**
URL: https://martinfowler.com/bliki/TellDontAsk.html

The behavioral formulation of the placement law: move behavior to the data it operates on. `import_ref.resolve()` rather than `resolver.resolve(import_ref)`. Simple to state; requires knowing which type is the subject before it can be applied.

**Anemic Domain Model critique (Fowler)**
URL: https://martinfowler.com/bliki/AnemicDomainModel.html

Corrective: A rich domain model places behavior and invariants on the entities and value objects that own the data. Services handle only behavior that genuinely has no natural home in any entity or value object. The corrective design review question: which entity or value object is the natural home for this behavior? If the answer is clear, it should not be on a service.

**Domain-Driven Design entity/value object behavior placement**
URL: https://dev.to/ielgohary/domain-driven-design-entities-value-objects-and-services-chapter-51-22cm

DDD: "Prefer to put the behavior on value objects rather than on entities." Services are the exception, not the default. The corrective: before creating a service, exhaust the question of whether the behavior belongs on an existing entity or value object.

### Prior art: type-first design

**Parse, don't validate — Alexis King (2019)**
URL: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

"Use a data structure that makes illegal states unrepresentable."

The import resolution application: instead of a Resolver service that takes raw strings and validates them, parse the string into an `ImportReference` type that carries proof of validity. Methods on `ImportReference` (its capability traits) then work on a self that IS the thing with the capability. Parsing relocates the proof from the service to the type, enabling true capability traits.

**Denotational design — Conal Elliott and exposition by Sandy Maguire**
URL: http://conal.net/papers/type-class-morphisms/ and https://reasonablypolymorphic.com/blog/follow-the-denotation/

Method: (1) Choose a denotation — what does this type MEAN? (2) Derive type class instances that are homomorphisms over that meaning. The implementation must preserve the denotation.

If you ask "what does `ImportReference` mean?" — a reference to an import that can be resolved. The trait follows: `impl Resolvable for ImportReference`. If you ask "what does `Resolver` mean?" the answer is murky — a bag of dependencies. No clear denotation means no principled trait. This is a design-first test that precedes implementation.

Maguire's formulation: "Names are helpful, but laws are invaluable." A trait that falls out of a clear denotation will have laws; a service trait will not.

**Principled type classes — John De Goes**
URL: https://degoes.net/articles/principled-typeclasses

"Type classes can't stand alone. To be useful writing generic code, they need to ship with laws that describe how they behave."

Before creating a trait: (a) state the laws; (b) confirm the implementing type has an intrinsic relationship to the operation; (c) ask whether a free function serves equally well. If no laws exist and the relationship is extrinsic, the abstraction is a function, not a trait.

**Smalltalk message-receiver tradition**
HN: https://news.ycombinator.com/item?id=21852444

Kay: "The big idea is messaging." Objects are autonomous entities that respond to messages. The receiver of the message IS the subject of the computation. This is the oldest and clearest formulation of the placement law.

### Prior art: ontology-first workflow

**Haskell typeclass vs Java interface — the laws distinction**
De Goes (above); also Tony Morris "Type-classes are nothing like interfaces" (widely cited, not fetched due to certificate issue at time of research).

Java interfaces are signature contracts. Haskell type classes (and Rust traits at best) are algebraic structures with laws. `Eq` has reflexivity, symmetry, transitivity. A service trait has no such laws. The key workflow implication: you cannot design a trait without first knowing its laws; you cannot know its laws without knowing what the type IS.

**The psyche's own stated method (2026-08-13)**
From traitsAsCapabilities.md: "we need to think very carefully of what the types are. First, really, because the traits are something that the types implement. We don't look for traits and then think of types for that. So, what are all the types?"

This is the design workflow: enumerate the types; understand what each IS and what it carries; then ask which capabilities belong on which type. Traits follow from a clear type ontology; they cannot precede it.

### A synthesized design checklist (from sources above)

Before creating a trait:

1. Subject test (Tell Don't Ask): Is `self` the subject of the capability, or is the real subject a parameter? If `self` is not the subject, this is a function, not a trait.
2. Law test (De Goes): Can algebraic laws be stated for this trait? If no, it is a bag of methods, not a type class.
3. Denotation test (Elliott): What does the implementing type MEAN? Does the trait follow from that meaning?
4. Parse test (King): Could the parameter be eliminated by parsing it into a type that carries the proof? If yes, the parameter should not exist, and the trait belongs on the parsed type.
5. Standard library test: Does this trait resemble `Display`/`Iterator`/`Clone` (self is subject), or does it resemble a Tower middleware seam (self is infrastructure, subject is parameter)?
6. Free function test (entrait): Would a free function serve equally well? If yes, the trait is not earning its keep.


## Unknowns (kept separate)

No study was found specifically documenting LLMs producing service-shaped traits in response to mandatory-trait instructions. The mechanism is inferred from training data composition and local-plausibility findings; direct evidence is absent.

Whether the law test (De Goes) transfers cleanly to Rust trait design (where not all traits have algebraic laws in the Haskell sense) is not fully examined. The standard library's `Read`/`Write`/`Display` have informal correctness expectations rather than formal equational laws. The test may need softening for Rust.

The entrait crate's alternative (trait-per-function generated from free functions) avoids service-object accumulation but may produce the same fragmentation problem the psyche identified (2026-08-17: "many of those traits should be one"). That question is unexamined here.

The workflow for designing ontology before implementation — who does it, what the artifact looks like, how it gates implementation — is identified as needed by the psyche ("creating a workflow for this, for any ontology to be designed properly before it's implemented") but is not resolved by the prior art found. The checklist above is a candidate starting point, not a validated workflow.
