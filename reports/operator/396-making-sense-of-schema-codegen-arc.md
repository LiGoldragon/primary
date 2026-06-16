# 396 — Making sense of the schema codegen arc

This is the operator translation of Designer's report `665`: what the idea is, what the
real code proves, what is still prototype-grade, and what decisions remain.

## The shortest explanation

Designer is talking about two related mechanisms that are easy to blur:

1. **Standard generated impls**: the schema declares a shape, and the Rust emitter stamps
   obvious trait impls whose bodies are forced by that shape. No method-body language is
   needed. This is the operator branch `operator/standard-newtype-impls` in
   `schema-rust-next`.
2. **Shape-checked body composition**: the schema authors a method body as data, and the
   compiler checks each call against the receiver's schema shape before emitting Rust. This is
   Designer's resolver/composition line.

The first one is mergeable and narrow. The second one is the deeper vision and has good
prototype evidence, but it still needs hardening before main.

## Real example 1 — standard generated newtype impls

This schema is real, from
`/git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/standard-newtype-impls.schema`
on the operator branch:

```nota
[(Record NameText)]
[(Accepted NameText)]
{
  NameText String
  FilePath Path
  Count Integer
  Enabled Boolean
  WrappedName NameText
}
```

The important part is `NameText String`. That says: `NameText` is a newtype over the scalar
`String`. From that alone, the emitter can produce `Display`, `AsRef<str>`, and
`PartialEq<&str>` without asking the schema author to write a method body.

Generated Rust from
`/git/github.com/LiGoldragon/schema-rust-next/tests/fixtures/standard_newtype_impls_generated.rs`:

```rust
pub struct NameText(String);

impl NameText {
    pub fn new(payload: impl Into<String>) -> Self {
        Self(payload.into())
    }
    pub fn payload(&self) -> &String {
        &self.0
    }
    pub fn into_payload(self) -> String {
        self.0
    }
}

impl From<String> for NameText {
    fn from(payload: String) -> Self {
        Self::new(payload)
    }
}

impl std::fmt::Display for NameText {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.payload().fmt(formatter)
    }
}

impl AsRef<str> for NameText {
    fn as_ref(&self) -> &str {
        self.payload().as_str()
    }
}

impl PartialEq<&str> for NameText {
    fn eq(&self, other: &&str) -> bool {
        self.payload() == other
    }
}
```

That is not magic and not broad Rust-in-schema. It is just: "this type wraps a string, so all
the standard delegation bodies are known."

The same fixture proves integer and boolean cases:

```rust
impl std::fmt::Display for Count {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.payload().fmt(formatter)
    }
}

impl PartialEq<u64> for Count {
    fn eq(&self, other: &u64) -> bool {
        self.payload() == other
    }
}

impl PartialOrd<u64> for Count {
    fn partial_cmp(&self, other: &u64) -> Option<std::cmp::Ordering> {
        self.payload().partial_cmp(other)
    }
}

impl PartialEq<bool> for Enabled {
    fn eq(&self, other: &bool) -> bool {
        self.payload() == other
    }
}
```

And the same generated file shows the safety boundary:

```rust
pub struct WrappedName(NameText);

impl WrappedName {
    pub fn new(payload: NameText) -> Self {
        Self(payload)
    }
    pub fn payload(&self) -> &NameText {
        &self.0
    }
    pub fn into_payload(self) -> NameText {
        self.0
    }
}

impl From<NameText> for WrappedName {
    fn from(payload: NameText) -> Self {
        Self::new(payload)
    }
}
```

`WrappedName NameText` does **not** get `Display` or `AsRef<str>` from this branch. The
operator branch only looks one layer deep, at scalar payloads. That restraint is deliberate.

The runtime test is also real:

```rust
let name = generated::NameText::new("schema");
assert_eq!(name.to_string(), "schema");
assert_eq!(name.as_ref(), "schema");
assert_eq!(name, "schema");

let count = generated::Count::new(42);
assert_eq!(count.to_string(), "42");
assert_eq!(count, 42);
assert!(count > 10);

let enabled = generated::Enabled::new(true);
assert_eq!(enabled.to_string(), "true");
assert_eq!(enabled, true);
```

This is the part I would land first.

## Real example 2 — generics and impls as schema syntax

Designer's prototype branch demonstrates the larger syntax, using actual schema files.

From
`/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand/tests/fixtures/pipe-demo/schema/reaction.schema`:

```nota
{}
[]
[]
{
  Work (| [Event WriteDone ReadDone EffectDone]
    [(SignalArrived Event) (SemaWriteCompleted WriteDone) (SemaReadCompleted ReadDone) (EffectCompleted EffectDone)] |)
  Action (| [Reply Write Read Effect Continuation]
    [(ReplyToSignal Reply) (CommandSemaWrite Write) (CommandSemaRead Read) (CommandEffect Effect) (Continue Continuation)] |)
}
```

Read that as: `Work` and `Action` are generic enum frames. They are authored once.

Then the component applies those frames in
`/home/li/wt/github.com/LiGoldragon/schema-rust-next/reaction-expand/tests/fixtures/pipe-demo/schema/ledger.schema`:

```nota
{
  Work reaction:reaction:Work
  Action reaction:reaction:Action
}
(Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)
(Action SignalOutput SemaWriteSet SemaReadInput EffectCommand (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome))
{
  SignalInput { payload String }
  SignalOutput { reply String }
  SemaReadInput { selector String }
  SemaReadOutput { records Integer }
  SemaWriteOutput { written Boolean }

  Statement { text String }
  LedgerEntry { statement Statement sequence Integer }
  EntryHandle Statement

  EntryHandleIsAuditable {| Auditable EntryHandle |}
  EntryHandleDeref {| Deref EntryHandle [ (deref (reference (field self payload))) ] |}
}
```

There are three important things here:

- `(Work SignalInput ...)` is a generic application. It expands to a concrete component
  `Input` enum, not a Rust generic alias.
- `{| Auditable EntryHandle |}` is a marker impl. It generates
  `impl Auditable for EntryHandle {}`.
- `{| Deref EntryHandle [ (deref (reference (field self payload))) ] |}` is method body as
  data. The body is an expression tree, and the prototype emits the Rust `&self.0`.

The test asserts the generated Rust shape:

```rust
assert!(code.contains("pub enum Input {"));
assert!(code.contains("SignalArrived(SignalInput)"));
assert!(code.contains("SemaWriteCompleted(SemaWriteOutput)"));

assert!(code.contains("impl Auditable for EntryHandle {}"));

let normalized: String = code.split_whitespace().collect();
assert!(normalized.contains("&self.0"));
```

Then it includes the generated Rust and exercises it at runtime:

```rust
let statement = Statement::new("recorded".to_owned());
let handle = EntryHandle::new(statement.clone());
let derefed: &Statement = &handle;
assert_eq!(derefed, &statement);
assert_eq!((*handle).payload(), statement.payload());
```

That is why Designer says "the vision is proven." The prototype really does generate and run
Rust from schema-authored generics and a small method-body expression.

## The capability-resolver idea

The next problem is: how does the compiler know that this body is legal?

```nota
(deref (reference (field self payload)))
```

The old shallow version could drift toward "if the method name is in an allowlist, accept it."
That is weak. A name like `payload` is only valid when the receiver has a payload.

The stronger version is the **shape-derived capability resolver**:

- If `self` is `EntryHandle`, and schema says `EntryHandle Statement`, then `self` is a
  newtype.
- A newtype has a generated `payload` capability.
- Therefore `field self payload` is legal and has type `Statement`.
- `reference (...)` is legal when the expression has an addressable borrowed result.
- Therefore the body emits `&self.0`.

If `self` were a normal struct with no newtype payload, `payload` must reject. That is the
meaning of "shape-derived": the call is not accepted because its name sounds familiar; it is
accepted because the receiver's schema shape proves it.

This is the clean conceptual boundary:

- **Generated/data body**: every call resolves against schema-implied capabilities.
- **Hand-written Rust**: the first call that does not resolve is business logic.

Examples of schema-implied capabilities:

- newtype payload access: `payload`, `into_payload`;
- scalar newtype standard traits: `Display`, `AsRef<str>`, `PartialEq<&str>`, scalar
  comparisons;
- enum variant constructors and `From` legs;
- struct field accessors, if guarded against collisions;
- later, total variant rewrap/match helpers.

Examples that are not structurally guaranteed:

- `trim`, `to_lowercase`, arithmetic, IO, store access, guardian logic;
- arbitrary std methods unless explicitly admitted by a small policy allowlist;
- decision-plane behavior.

## Why `as_str` is a trap

`self.payload().as_str()` looks harmless, but `as_str` is a `String`/`str` method. It is not
derived from the schema object itself except by stepping into Rust's standard library.

That creates an arbitrary boundary: why allow `as_str` but not `trim`, `to_lowercase`, or
`parse`?

My recommendation matches Designer's latest lean: avoid a broad std-method allowlist. Emit
standard traits instead:

- `AsRef<str>` for string/path newtypes;
- `Display` for scalar newtypes;
- scalar comparisons where the payload type proves them.

Then callers use normal Rust trait surfaces, and the schema language does not need to become
a curated list of std methods.

## What is mergeable versus prototype-grade

Mergeable now:

- `schema-rust-next` branch `operator/standard-newtype-impls`
- commit `f265aad6`
- opt-in emission knob: `RustEmissionOptions::with_standard_newtype_impls()`
- tests green: targeted fixture test, full `cargo test`, and clippy
- behavior: scalar-backed newtypes emit standard payload-delegating trait impls

Prototype-grade:

- pipe-delimiter generics/impl demo;
- `Deref` body emitted from data;
- shape-derived capability resolver core;
- composed method bodies.

Known hardening before main:

- residual `panic!` / `assert!` paths in impl emission need typed errors or generated
  `compile_error!`;
- generic impl headers are out of scope in the prototype;
- struct-generated accessors need collision handling, because a field named `new` can collide
  with a generated constructor;
- type propagation past some variant constructor paths is incomplete;
- `VariantMatch` is not built yet, and that is the likely right primitive for the big
  enum-rewrap boilerplate class.

## My recommendations on Designer's four calls

1. **Deref default or marker**: marker / opt-in. The real codebase has many newtypes that
   deliberately do not deref. `Deref` changes how a type behaves in Rust, so schema should
   express that intent.
2. **Flip standard-newtype impls default-on**: not globally yet. First land the opt-in
   mechanism, then turn it on for one contract generation path and review the regenerated
   diff. After that, default-on may be reasonable.
3. **Nested-newtype transitive scalar**: keep depth-1 opaque for the first landing.
   `StatementText String` can get scalar impls; `Statement StatementText` should not
   silently inherit them until we have an explicit transitive policy.
4. **`as_str`**: no named std-leaf methods for now. Use generated `AsRef<str>` and `Display`.

## The mental model

Schema names nouns and shapes. From a noun's shape, the compiler can derive some verbs.

For `NameText String`, the schema proves these verbs:

- construct it from a string;
- inspect or consume its payload;
- display it by displaying the payload;
- treat it as `&str`;
- compare it to `&str`.

For `EntryHandle Statement`, the schema proves:

- construct it from a `Statement`;
- inspect or consume its payload;
- maybe deref to `Statement`, but only if the schema says this newtype has that role.

For `Input [(Record Entry) (Observe Query)]`, the schema proves:

- construct each variant;
- convert payload wrappers into the enum through `From`;
- later, rewrap variants across isomorphic enums if a total `VariantMatch` proves the mapping.

Everything beyond those shape-proven verbs is ordinary behavior and stays hand-written.

That is the useful core of Designer's explanation. The schema language is not trying to
become "all Rust in NOTA" in one jump. It is carving out the recurring Rust that is already
mechanically implied by schema shapes, generating it, and only expanding the data-language
when a body can be proven by the same shape rules.

## Bottom line

Designer's whole vision is sound as a direction, but it has two landing tracks:

- land **standard generated impls** first, because that is small, tested, and immediately
  deletes repetitive code;
- then land **shape-derived body composition** in narrow slices, with typed errors and no broad
  std-method allowlist.

The phrase to keep in your head is: **the schema shape proves the generated code**. If the
shape does not prove it, it is behavior, and behavior remains hand-written until a later,
explicit schema construct proves it.
