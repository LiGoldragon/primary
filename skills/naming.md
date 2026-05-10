# Skill — naming (full English words)

*Identifiers are read far more than they are written. Spell every
identifier as a full English word; let the right name happen.*

---

## What this skill is for

Apply this skill every time you name an identifier — a type, a
function, a field, a variable, a module, a parameter. The
default is the spelled-out English form; abbreviations require
one of six narrow exceptions. Skim the offender table when you
catch yourself reaching for `ctx`, `tok`, `op`, `de`, or any
two-to-three-letter shape; it's almost always the wrong move.

This skill pairs with the **verb-belongs-to-noun** discipline
(workspace `skills/abstractions.md`) — that rule forces a naming
step to happen at all; this one decides what the name should look
like once you're forced to choose.

---

## The default

**Spell every identifier as full English words.**

Identifiers are read far more than they are written. Cryptic
abbreviations optimize for the writer (a few keystrokes saved) at
the reader's expense (one mental lookup per occurrence).

Examples (bad → good):

| bad | good |
|---|---|
| `lex` | `lexer` |
| `tok` | `token` |
| `ident` | `identifier` |
| `op` | `operation` (or specific: `assert_op`) |
| `de` | `deserializer` |
| `pf` | `pattern_field` |
| `ctx` | `context` (or specific: `parse_context`) |
| `cfg` | `config` (or `configuration`) |
| `addr` | `address` |
| `buf` | `buffer` |
| `tmp` | `temporary` (or — better — name what it holds) |
| `arr` | `array` (or — better — what it contains) |
| `obj` | (name what it actually is) |
| `params` | `parameters` |
| `args` | `arguments` |
| `vars` | `variables` |
| `proc` | `procedure` or `process` |
| `calc` | `calculate` |
| `init` | `initialize` |
| `repr` | `representation` |
| `gen` | `generate` or `generator` |
| `ser` / `deser` | `serialize` / `deserialize` |

---

## Permitted exceptions — tight, named, no others

1. **Loop counters in tight scopes (<10 lines).** `for i in 0..n`
   is fine. Beyond ~10 lines or nested, use descriptive names.
2. **Mathematical contexts** where the math itself uses the symbol.
   `x`, `y`, `z`, `theta`, `phi`, `lambda`, `n` for sample size,
   `p` for probability — only when the surrounding code or comment
   establishes the math context.
3. **Generic type parameters.** `T`, `U`, `V`, `K`, `E`. Use a
   descriptive name when the parameter has non-trivial semantic
   content.
4. **Acronyms that have passed into general English.** `id`, `url`,
   `http`, `json`, `uuid`, `db`, `os`, `cpu`, `ram`, `io`, `ui`,
   `tcp`, `udp`, `dns`. Spell them when ambiguous in context.
5. **Names inherited from `std` or well-known libraries.** `Vec`,
   `HashMap`, `Arc`, `Rc`, `Box`, `Cell`, `RefCell`, `Mutex`,
   `mpsc`, `regex`. Do not rename these; do *not* extend the
   abbreviation pattern to your own types.
6. **Domain-standard short names already documented in an
   `ARCHITECTURE.md`.** `slot`, `node`, `edge`, `frame` are full
   words and need no exception. If a true short form is
   load-bearing in the schema, name it in `ARCHITECTURE.md` so the
   exception is explicit; otherwise spell it out.

---

## Rule of thumb

**Name length proportional to scope.** A 3-line loop counter can
be `i`. A module-level type that appears across the codebase must
spell itself out. A function parameter that lives for 50 lines
must read as English.

---

## What this rule is NOT

- Not "verbose names everywhere" —
  `calculate_the_total_amount_of_items` is worse than
  `total_items`. The goal is *clear*, not *long*.
- Not "no acronyms ever" — see exception 4.
- Not "rewrite std" — see exception 5.

---

## How to apply when generating code

When generating new code: **spell identifiers as full English
words by default.** When the surrounding code uses cryptic
identifiers, do not propagate them into new code. Either rename
(if rename is in scope) or use the full form for new identifiers
and flag the inconsistency as a follow-up. Pattern-matching the
local dialect is exactly the failure mode this rule exists to
break.

---

## The "feels too verbose" anti-pattern

When a spelled-out name (`AssertOperation`, `Deserializer`,
`PatternField`, `RelationKind`) "feels needlessly verbose" — that
feeling is **not** a signal to shorten the name. It is a signal
that the writer has been taught wrong by a culture inherited from
constraints that no longer apply.

The full word reads as English. The abbreviation reads as ceremony
to be decoded. The cost of mis-naming is paid every time the name
is read; the benefit of saving three keystrokes is paid once.
There is no contest.

When you catch yourself thinking "this name feels too long" or
"this is unnecessarily ceremonial":

1. **Question the feeling.** It is almost certainly inherited
   prejudice, not informed judgment.
2. **Re-read the name as English.** Does `AssertOperation` read as
   English? (Yes.) Does `AssertOp` read as English? (No — it
   requires expansion.)
3. **Apply the rule.** The full English form wins unless the name
   falls in one of the six named exception classes above.

There is no exception class for "feels verbose." That feeling is
the bug, not the criterion.

---

## Field naming — `profileSize` vs `size` vs `profile::size`

When naming a field, method, or local that *could* be just a
short word (`size`, `id`, `name`, `body`), the question is:
**does the surrounding namespace already give the noun?**

- If the access path is `profile::size` (module path) or
  `profile.size` (struct field of a `Profile`-typed thing),
  then `size` reads as English at the call site —
  `profile.size` *is* the description.
- If the field stands alone, naked, with no enclosing
  namespace (a top-level binding, an unqualified function
  parameter, a record field that often appears outside its
  parent type's context), then `size` is too thin —
  `profileSize` carries the missing context.

```rust
// Right — namespace already qualifies; field name stays short
struct Profile {
    pub size: u64,        // accessed as profile.size
}

// Right — naked parameter with no enclosing namespace; name carries the context
impl MetricsRecorder {
    pub fn record(&self, profileSize: u64, requestCount: u32) { … }
}

// Wrong — descriptor's namespace already names "profile"; field name redundant
struct Profile {
    pub profileSize: u64,  // profile.profileSize reads as repetition
}

// Wrong — naked parameters claim a context that isn't there
impl MetricsRecorder {
    pub fn record(&self, size: u64, count: u32) { … }
    //                   ^^^^         ^^^^^ which size? which count?
}
```

The rule: **the name carries the context the namespace
doesn't.** Tests:

- *Will the reader see this name with or without its
  enclosing namespace?*
- *Does the namespace already name the thing the field
  describes?*

If both answers are "with namespace + namespace names it,"
the field name can be short. If either answer is "without
namespace" or "namespace doesn't name it," the field name
needs the descriptive prefix.

The discipline is logical-plane separation: naked names
*claim* a context they don't have. Naked names that survive
in code are silent failures of clarity that the type system
can't catch.

This refines the "full English words" rule: it isn't *more
words* that wins — it's *the words the namespace doesn't
already supply*. `messageId` when there's no `Message`
namespace; `id` when there is.

(Per Li 2026-05-09: "I prefer more indirection and logical
planes, more naming accuracy — `profileSize` is better than
`size`, unless it is `profile::size`.")

---

## Anti-pattern: prefixing type names with the crate name

**A type's name belongs to its module context, not to the
cross-crate global namespace.** The crate IS the namespace;
repeating it in the type name is redundant ceremony.

```rust
// Wrong — crate name redundant at every use site
pub struct ChromaRequest { … }
pub struct ChromaResponse { … }
pub struct ChromaConfig { … }
pub struct ChromaError { … }

// Right — call sites read chroma::Request, chroma::Error
pub struct Request { … }
pub struct Response { … }
pub struct Config { … }
pub struct Error { … }
```

The discriminator: **does the leading word *describe* the
type, or does it *name* its origin crate?** Descriptive
words stay; namespace prefixes go.

| Prefix is wrong | Prefix is fine |
|---|---|
| `ChromaRequest` (Chroma is the crate) | `VisualState` (Visual describes what kind of state) |
| `StylixOptions` (Stylix is the crate) | `ColorScheme` (descriptive) |
| `NotaCodecError` | `LexerError` |
| `PersonaMessageRouter` | `MessageRouter` |

**The standard library is the canonical reference.** `Vec`,
`HashMap`, `Arc`, `Cell`, `Mutex` — never `StdVec`,
`StdHashMap`, `StdArc`. The pattern propagates: well-shaped
crates name their types as if `use crate_name::*` were the
norm, even when it isn't.

**Why LLM agents are particularly prone to this:** the
prefix "feels safe" (avoids collisions, matches the file
name, looks self-documenting) and tokens are free. Same
procrastination pressure as in `skills/abstractions.md` —
the agent skips the harder thinking ("what does this type
actually represent?") in favour of the shallower
disambiguator ("which crate is it from?"). Both produce
the same drift: structural meaning hidden by ceremony.

The Rust enforcement (with std references) lives in
`skills/rust-discipline.md` §"No crate-name prefix on
types"; this section is the cross-language form.

---

## Anti-pattern: framework-category suffixes on type names

**A type's name should describe what it IS or what role it plays
— never the framework category it falls into.** A `Counter` that
implements the `Actor` trait IS an actor; calling it `CounterActor`
adds the category to the name without adding meaning.

```rust
// Wrong — framework-category suffix
pub struct CounterActor { count: i64 }
pub struct IncMessage { amount: i64 }
pub struct ClaimNormalizerActor { … }
pub struct SubmitMessage { … }

// Right — name says what the type IS / does
pub struct Counter { count: i64 }
pub struct Inc { amount: i64 }
pub struct ClaimNormalizer { … }
pub struct Submit { … }
```

The discriminator: **does the suffix describe the type's role, or
does it tag the framework category the type happens to fall into?**
Role-shaped suffixes stay; category-shaped suffixes go.

| Suffix is wrong (framework category) | Suffix is fine (descriptive role or relationship) |
|---|---|
| `*Actor` | `*Supervisor` (this type supervises children) |
| `*Message`, `*Msg` | `*Resolver` (this type resolves something) |
| `*Handler` | `*Decoder`, `*Encoder` (this type decodes/encodes) |
| `*Listener`, `*Subscriber` (as a generic trait-participation tag — `EventSubscriber` to mean "thing that implements `Subscribe`") | `*Tracker`, `*Cache`, `*Ledger` (this type holds that state); also `Subscriber` as the *role* of the long-lived actor on the receiving side of a publish/subscribe channel — that's role-naming, not category-tagging |
| `*Object`, `*Type`, `*Class` | `*Builder`, `*Factory` (when actually building things) |
| | `*Handle`, `*Client`, `*Ref` — relationship-naming (the value IS a held authority on the target; same shape as `JoinHandle`, `FileHandle`) |

**Note on `Handle`**: `Handle` is *not* a framework-category tag in the
same shape as `Actor` / `Message` / `Handler`. It names a relationship —
the value IS the caller's held authority to a live service or resource.
Same pattern as `tokio::task::JoinHandle` (a handle to join a task) or
`std::fs::File` / `std::process::Child` as held-resource types.
`*Handle` earns its place when the wrapper carries domain content
(lifecycle ownership, capability narrowing, error vocabulary mapping,
topology insulation, or send-policy enforcement). For the actor-specific
application of *when* a Handle is appropriate, see this workspace's
`skills/kameo.md` §"Public consumer surface — ActorRef<A> or domain
wrapper".

A bare `Handle` wrapper that just holds an `ActorRef<A>` and delegates
method-by-method without adding domain content is still the
runtime-laundering anti-pattern operator/103 retired — drop the wrapper
and expose `ActorRef<A>` directly.

The rule's deeper purpose: type names are read at every use site,
and a category tag forces the reader to mentally strip it ("oh,
`CounterActor` — that's a Counter that's an Actor — well it's
always going to be an Actor in this codebase, so just Counter").
That mental strip is paid every time. Drop the tag; let the type
name carry meaning.

**Why LLM agents are particularly prone to this:** category tags
"feel safe" (they document the framework participation visibly,
match common tutorial conventions, look self-explanatory). Same
procrastination pressure as crate-name prefixes — the agent reaches
for the shallower disambiguator instead of doing the harder work
of finding the right role-shaped name.

For the actor-specific application of this rule (with worked
examples and the historical context — ractor's behavior-marker
+ State split made the suffix briefly defensible; Kameo's
`Self`-IS-the-actor shape removed even that), see this workspace's
`skills/kameo.md` §"Naming actor types".

---

## Companion rule

Pairs with this workspace's `skills/beauty.md`: a name that
doesn't read as English is one of the diagnostic readings of
structural ugliness. The aesthetic discomfort is the signal that
the right structure (the right name, the right type) hasn't been
found.

---

## See also

- this workspace's `skills/beauty.md` — beauty as the criterion;
  bad names are a diagnostic reading.
- this workspace's `skills/abstractions.md` — verb-belongs-to-noun;
  this rule restores the naming step LLM agents tend to skip.
- this workspace's `skills/stt-interpreter.md` — the
  table-of-mappings shape, applied to speech-to-text mishearings
  rather than code abbreviations.
- this workspace's `skills/rust-discipline.md` — Rust-specific
  application (the cryptic-dialect example, the offender table
  again with Rust-flavor entries).
