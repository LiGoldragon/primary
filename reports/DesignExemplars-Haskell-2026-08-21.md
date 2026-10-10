# Design Exemplars: Haskell and the Typed-FP Tradition

Commissioned 2026-08-21, per machineAnatomy.md 2026-08-21 ("look for example programs
... in Rust, obviously, or maybe Haskell. I don't know how correct that language actually
is."). Research beat: Haskell and the typed-FP tradition. Parallel beat: Rust exemplars
(DesignExemplars-Rust-2026-08-21.md). Web research authorized for this round.

The vision being matched against is the four-part machine anatomy (machineAnatomy.md
2026-08-21), the conversion spine (draft.md, mainFunction.md), and the types-first
ontology-before-code protocol (worldModelBeforeCode.md, draft.md). In brief:
- Main is a few lines tying the spec together via conversions (TryFrom / From).
- A machine has four parts: raw inputs, coherent input type, coherent output type,
  output as a single reviewable operation.
- Types are enumerated from identity and contents before capabilities.
- Conversions consume inputs by value; no downstream references into them.
- Capabilities sit on the type that contains their subject.
- No service types; steps are walks across types, not things on the map.

Findings and interpretation are kept in separate sections. Claims are sourced by linking
to source files, commits, or documented public artifacts where available.

## Part I: Findings

### Exemplar A: Elm Compiler

**Source:** https://github.com/elm/compiler — written in Haskell.

**Architecture:** The Elm compiler defines three distinct named ADTs for the three
compilation stages, each in its own module:

- `AST.Source.Module` — the parsed, unresolved surface syntax.
- `AST.Canonical.Module` — after name resolution and canonicalization. A structurally
  different type: union types replace surface-syntax union syntax, pattern-match
  exhaustiveness can be checked.
- `AST.Optimized.LocalGraph` — after type checking and optimization. Names replaced
  with integers, dead branches eliminated.

The central pipeline in `compiler/src/Compile.hs` (circa 2019–2024 revisions) is
approximately:

```haskell
compile :: Pkg.Name -> Interfaces -> Src.Module -> Either E.Error Artifacts
compile pkg ifaces modul =
  do  canonical   <- canonicalize pkg ifaces modul
      annotations <- typeCheck modul canonical
      ()          <- nitpick canonical
      objects     <- optimize modul annotations canonical
      return (Artifacts canonical annotations objects)
```

Each stage function carries a typed signature: `Src.Module -> Either E.Error Can.Module`,
`Can.Module -> Either E.Error Opt.LocalGraph`. The type system forbids passing a
`Src.Module` to `optimize`. The structural repetition between stage types is deliberate
and explicitly defended in the compiler's architecture: the three types are not shared
via a parameterized AST.

The `Artifacts` return type packages the coherent-output values together before any
code generation or file emission. File writing is a downstream step on the output
of `compile`, not interleaved with compilation.

Main at the program level delegates to a small command dispatcher (`src/Main.hs`), with
each command (make, repl, install) resolved to a typed operation. It is not a one-liner
but it is short and entirely compositional.

**What matches:** Parts 1–4 of the anatomy are visible and distinct. The coherent-input
type (`Can.Module`) is genuinely structurally different from the surface type — you
cannot confuse them. The coherent-output type (`Artifacts`) is assembled completely
before emission. Stage boundaries are enforced by the type system, not by convention.
No Resolver or Canonicalizer service type appears on the map; canonicalization is a
function from `Src.Module` to `Can.Module`.

**What diverges:** The conversion functions are standalone functions, not typeclass
instances. There is no `From`/`TryFrom` protocol; each conversion is named differently
(`canonicalize`, `typeCheck`, `optimize`). Haskell has no equivalent to Rust's
`From`/`TryFrom` as an ecosystem-wide protocol. The `do`-notation in `compile` is an
`Either` monad, which is a thin wrapper over chained error propagation — analogous to
`?` in Rust, but less syntactically transparent about the conversion spine. Inputs are
not consumed by value in the ownership/move sense; Haskell's GC manages memory.

**Vision match: Strong.**

### Exemplar B: Dhall

**Source:** https://github.com/dhall-lang/dhall-haskell — Haskell implementation of
the Dhall configuration language.

**Architecture:** Dhall's core expression type is parameterized: `Expr s a`, where `s`
is annotation (source position) and `a` is the import type. Before import resolution,
`a ~ Import` (a concrete import reference). After import resolution, `a ~ Void`
(the uninhabited type from `Data.Void`).

The type `Expr Src Void` structurally cannot contain an import. `Embed Void` would
require a value of `Void`, which cannot be constructed. The function `load` in
`Dhall.Import` has signature (approximately):

```haskell
load :: Expr Src Import -> IO (Expr Src Void)
```

After `load`, the return type is a compile-time proof that all imports are resolved.
Downstream stages — type checking, normalization — operate on `Expr Src Void` and
structurally cannot receive an unresolved expression.

This is the clearest Haskell-ecosystem example of "parse, don't validate" (Alexis King,
2019: https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) applied at
architectural scale: the coherent-input type encodes its own validity proof in its
type parameter.

The normalization stage produces a `Expr Void Void` — no source annotations, no imports.
That is the coherent-output type from which pretty-printing (emission) proceeds.

**What matches:** The Part 1 → Part 2 transition (raw import-containing expression to
import-free expression) is enforced structurally, not by runtime assertion. The type
encodes stage membership. Downstream misuse is a type error, not a runtime error.

**What diverges:** `StateT Status IO` appears in the import resolver — a monad stack
that is service-ish in character. The resolver carries a cache and a stack of in-flight
imports; this is necessary for cycle detection, but it makes the coherent-input type's
construction less legible as a clean "assembled from inputs" operation. The parameterized
type approach (`Expr s a`) also means the same structural type spans all stages; it is
a shared parameterized type, not three distinct named types.

**Vision match: Strong on the phase-enforcement property specifically; Partial overall.**

### Exemplar C: Pandoc

**Source:** https://github.com/jgm/pandoc

**Architecture:** The universal document type is defined in a separate library package:

```haskell
data Pandoc = Pandoc Meta [Block]
```

`Meta` is a `Map MetaKey MetaValue`; `Block` is a large sum type (Para, Header, Table,
CodeBlock, etc.). This type is the shared intermediate representation. Readers have type
`ReaderOptions -> Text -> PandocIO Pandoc`. Writers have type
`WriterOptions -> Pandoc -> PandocIO Text` (approximately).

The data flow `Input -> Pandoc -> Output` is genuine and is the advertised design. The
type is defined once and both readers and writers are implemented against it by third
parties.

The driver function in `src/Text/Pandoc/App.hs` is approximately 200 lines. The
conversion chain itself (read → transform → write) is buried within it, approximately
10 lines, surrounded by option handling, error wrapping, and output routing. The coherent
input and the coherent output are the same type (`Pandoc`), meaning there is no type-level
boundary between "input assembled" and "output ready." A reader that emits an invalid
`Pandoc` value is not caught at type-check time; the type only has structural validity.

All reader and writer functions are standalone functions in modules, not methods on the
`Pandoc` type. `Pandoc` has no capabilities (no typeclass instances for reading or
writing). This is an intentional separation: the universal type is a pure data container.

**What matches:** The universal intermediate type is a genuine types-first design.
Readers and writers are structured as conversions. The type is in its own package,
enforcing the separation between the representation and the operations.

**What diverges:** Parts 2 and 3 of the anatomy are collapsed into one type. There is
no phase boundary between "coherent input" and "coherent output type ready for emission."
A large format ecosystem (dozens of readers, dozens of writers) with a single shared
type erases the distinction. Main/driver is not a few lines. The `PandocIO` monad wraps
IO and error handling but also carries reader/writer state; it is somewhat service-like.

**Vision match: Partial.**

### Exemplar D: GHC

**Source:** https://gitlab.haskell.org/ghc/ghc — the Glasgow Haskell Compiler, written
in Haskell.

**Architecture:** GHC's pipeline: parsed (`HsExpr GhcPs`) → renamed (`HsExpr GhcRn`)
→ typechecked (`HsExpr GhcTc`) → desugared to Core (`CoreExpr`) → STG (`StgExpr`)
→ Cmm → assembly/LLVM. The first three stages share the parameterized AST type
`HsExpr p` via the "Trees That Grow" extension (Najd & Peyton Jones 2016):

```haskell
data HsExpr p
  = HsVar     (XVar p) (Located (IdP p))
  | HsLit     (XLit p) HsLit
  | HsApp     (XApp p) (LHsExpr p) (LHsExpr p)
  ...
```

The type parameter `p` is `GhcPs`, `GhcRn`, or `GhcTc` depending on the phase. Type
families indexed by `p` control what extra information each node carries at each phase.
The pipeline functions have signatures like `HsExpr GhcPs -> TcM (HsExpr GhcTc)`.

Core, STG, and Cmm are distinct named types (not parameterized). Core desugaring
(`compiler/GHC/HsToCore.hs`) takes `HsExpr GhcTc` and produces `CoreExpr`. STG
generation takes `CoreExpr` and produces `StgTopBinding`. These stages have sharp type
boundaries.

The driver (`compiler/GHC/Driver/Pipeline.hs`) is large and stateful. It uses a phase
index and a `DynFlags`/`HscEnv` service record that is threaded through essentially
everything. The pipeline is not a chain of value conversions; it is a series of stateful
operations on a shared environment.

**What matches:** The named intermediate representations (Core, STG, Cmm) are a genuine
examples of the coherent-input and coherent-output boundary: passing a `CoreExpr` to the
STG stage is the right type, not a `HsExpr`. The desugaring boundary (HsTc → Core) is
especially clean in the type signature.

**What diverges:** The Trees That Grow pattern for the parsed/renamed/typechecked stages
deliberately chooses shared parameterized types over distinct named types, trading phase
legibility for code reuse at GHC's scale. The `HscEnv`/`DynFlags` record is a large
service container — exactly what "no service types" forbids. The driver is nowhere near
a few clear lines. GHC is a 500k-line compiler; scale forces tradeoffs.

**Vision match: Partial.**

### Exemplar E: XMonad

**Source:** https://github.com/xmonad/xmonad — a tiling window manager, written in
Haskell.

**Architecture:** XMonad's main is:

```haskell
main :: IO ()
main = xmonad def
```

`xmonad :: XConfig l -> IO ()` takes a configuration record and runs the event loop.
`def` (the `Default` typeclass method) produces a default `XConfig`. Users customize by
building a modified `XConfig` value. `XConfig` carries all callbacks (manageHook,
handleEventHook, logHook, keys) as fields — functions stored as data. There is no
separate Manager or Dispatcher service type; the user constructs the configuration value
and hands it to `xmonad`.

The internal state type, `XState`, is a pure record: focused window, workspace layout,
keybinding map. The `X` monad is `ReaderT XConf (StateT XState IO)`, carrying a read-only
environment and mutable window state.

**What matches:** Main genuinely is one or two lines. The `XConfig` value carries
capabilities as fields (hooks are stored functions, not separate service types). The
user-facing design is purely about constructing a value, not registering handlers or
calling methods on a service. This is close to "the schema is the types."

**What diverges:** XMonad is a reactive event loop; the four-part anatomy (inputs →
coherent input → coherent output → emit) does not map directly to a reactive domain.
There is no "coherent output type assembled before emission" in a window manager — output
is continuous and interleaved with input. The `StateT XState IO` monad carries mutable
state that is threaded through the loop; this is a service-like property, though at the
boundary of what any event loop can avoid.

**Vision match: Partial (strong on properties 1, 2, 7; domain makes 3–6 inapplicable).**

### Exemplar F: "Parse, Don't Validate" as Doctrine

**Source:** Alexis King, "Parse, Don't Validate," 2019.
https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/

**Architecture:** The central argument: instead of a function that validates data and
returns a `Bool`, write a function that parses data and returns a richer type that
structurally cannot be invalid. The classic example replaces `isNonEmpty :: [a] -> Bool`
with `parseNonEmpty :: [a] -> Maybe (NonEmpty a)`. After parsing, callers hold a
`NonEmpty a` — they cannot accidentally call head on an empty list, because the type
forbids it.

The doctrine extends to system boundaries: parse at the edge (reading config, parsing a
request), produce a rich validated type, and let the rest of the program never check
validity again. This is exactly the Part 1 → Part 2 transition in the four-part anatomy:
raw input becomes a coherent input type that downstream stages structurally cannot misuse.

The Dhall example above (Exemplar B) is the strongest production application of this
doctrine at architectural scale. The Elm compiler (Exemplar A) applies it at stage
boundaries. Pandoc (Exemplar C) applies it partially — the reader output is a typed AST,
but all readers produce the same type, so stage-specific invariants are lost.

**Vision match:** The doctrine names and precisely describes the Part 1 → Part 2
transition. It is the most exact theoretical articulation of that boundary from any
language ecosystem.

### What Was Checked and Not Included

**Shake** (build system): `Global` is a textbook service container: thread pool, rule
database, cleanup function, diagnostic logger. These are process-names-as-types. Weak
match on the vision; not a useful exemplar.

**HLint**: imperative IO pipeline, no distinct named intermediate types between parsing
and reporting. Weak match.

**Agda** and **Idris**: compiler pipelines structurally similar to GHC (multiple named
IRs, driver is large and stateful). No distinct advantage over GHC for this study.

## Part II: Interpretation

### What the Exemplars Demonstrate

The Elm compiler is the strongest overall demonstration because it makes the four parts
visible and enforced simultaneously. The three ADTs are not parameterized; they are
structurally distinct at every field. A function that receives `Can.Module` cannot have
received a `Src.Module` — the type mismatch is a compile error. The `Artifacts` type
assembles the coherent output before any file is touched. Stage functions are conversions
(not service calls), and no Canonicalizer type appears on the map.

Dhall provides the most precise demonstration of a single property: encoding phase
membership in the type parameter (`Expr Src Import` vs `Expr Src Void`). This is a
stronger guarantee than the Elm compiler's named-ADT approach for the specific question
"is this expression fully resolved?" — the uninhabited-type trick makes an invalid state
structurally unrepresentable. The cost is that the single parameterized type spans all
phases rather than being a distinct named type per phase.

Pandoc demonstrates that the universal-intermediate-type design is viable at ecosystem
scale (dozens of readers, dozens of writers), but it collapses the phase boundary between
coherent-input and coherent-output into one type. For Pandoc's purpose — format
conversion with no structured output stage — this is reasonable. For a compiler or a
code-generation system, the collapse loses information that the vision explicitly wants
to preserve.

### The "Parse, Don't Validate" Connection

The doctrine (Alexis King 2019) is the theoretical name for the Part 1 → Part 2
transition. It originated in typed-FP, is widely taught in Haskell, and has a direct
Rust translation: `TryFrom<RawInput>` for the coherent-input type's constructor, making
the invalid raw state uncallable from downstream code that only sees the output type. The
doctrine travels cleanly across the language boundary.

### Haskell Language Fitness: Where It Matches

**Types-first culture.** Haskell's design practice genuinely places types before code.
The idiom "define the types, then write the functions" is documented in Haskell textbooks
(Bird, Hutton), taught in courses, and visible in exemplar codebases. "Make illegal
states unrepresentable" (Yaron Minsky, 2011) originated in OCaml/Jane Street but is
the canonical formulation of what Haskell's ADTs enable.

**ADTs as ontology.** A `data` declaration is identity (the type name), enumeration
(the constructors), and contents (the fields) — the exact three properties the types-first
protocol enumerates. The `data` keyword is structurally what the protocol is about.

**"Parse, don't validate."** This is an explicit Haskell doctrine with a named essay,
wide adoption in the community, and production examples (Dhall, Elm). It is the sharpest
theoretical articulation of the Part 1 → Part 2 boundary from any ecosystem.

**Exhaustive pattern matching.** Haskell warns on non-exhaustive patterns; the language
culture treats exhaustiveness as a correctness property. This enforces the "capabilities
on the type that contains their subject" discipline at the use site.

**Total functions as design discipline.** Haskell's culture distinguishes total functions
(defined for all inputs) from partial functions (undefined for some inputs) and treats
partiality as a design failure. This aligns with the vision's "conversion errors at
the first missing edge" — the walk errors, not silently returns wrong.

### Haskell Language Fitness: Where It Diverges

**No From/TryFrom protocol.** The vision's conversion spine depends on a single
ecosystem-wide protocol: `From<T>` for infallible conversions, `TryFrom<T>` for
fallible. Rust's standard library defines these traits and the entire ecosystem
implements them. Haskell has no equivalent. Every conversion in Haskell is a differently
named function: `canonicalize`, `load`, `desugar`, `toCore`. There is no shared
typeclass that names the conversion relationship. The conversion spine exists in Haskell
programs, but it is not recognizable at a glance the way `TryFrom` impls are.

**Laziness subverts stage boundaries.** The vision requires a coherent-input type that is
"assembled into a coherent whole" before the next stage begins. In Haskell, a value of
type `Can.Module` may not be fully evaluated when handed to the next function — it is a
thunk that will be forced on demand. The stage boundary that the type enforces in Elm is
not an evaluation boundary. In a GC'd lazy language, "the coherent input type is fully
materialized" is a property to prove (using `seq`, `deepseq`, or strict fields), not a
language guarantee. In Rust, moving a value into a function by value guarantees it was
fully constructed by the caller.

**GC prevents enforcing "consume by value."** The vision's "conversions consume their
inputs by value; the inputs can be properly dropped" (draft.md) has no analogue in
Haskell. Haskell is GC'd; there is no move semantics, no `Drop`, no guarantee that the
input is freed when the conversion is complete. The memory discipline is inexpressible.
Rust's ownership system enforces it structurally: `From::from(val)` consumes `val`; the
caller cannot use it afterward. Haskell's `LinearTypes` extension (GHC 9.0+) is the
community's acknowledgment that this is a real gap, but it is not idiomatic Haskell.

**Monad stacks obscure the spine.** Idiomatic Haskell uses monad transformer stacks
(`ReaderT`, `StateT`, `ExceptT`) to compose effects. In the Elm compiler's `compile`
function, the `do`-notation runs in the `Either E.Error` monad — this is a thin wrapper
analogous to `?` in Rust. But larger Haskell codebases use `StateT Config (ReaderT Env
(ExceptT Error IO))`, and the conversion functions become `m CanonicalModule` for some
monad stack `m`. The conversion spine — which in Rust reads as a sequence of
`TryFrom::try_from` calls — is hidden behind effect machinery. The shape of the program
becomes "what monad stack are we in" rather than "what conversion are we performing."

**Handle/service-record pattern is idiomatic Haskell.** A widely-cited Haskell
best-practices pattern (the "Handle pattern," Tom Sydney Kerckhove, 2018;
https://jaspervdj.be/posts/2018-03-08-handle-pattern.html) promotes creating a record
of functions (a "handle") that encapsulates a service: `data Handle = Handle { sendEmail
:: Address -> Body -> IO (), logMessage :: Text -> IO () }`. This is precisely the
service-type pattern the vision forbids. It is promoted as good Haskell architecture,
which means the Haskell community's architectural instincts include a major divergence
from the vision.

**Typeclass sprawl.** The Haskell ecosystem has a culture of abstraction generalization:
MTL typeclass hierarchies (`MonadReader`, `MonadWriter`, `MonadState`), lens libraries
(`lens`, `optics`), and type-level programming (`DataKinds`, `TypeFamilies`,
`PolyKinds`). These abstractions are often applied before the concrete types are stable.
The vision explicitly places types first, then traits (capabilities), and only the
capabilities the domain actually needs. The Haskell ecosystem's direction is toward
maximum generality; the vision's direction is toward minimum sufficient abstraction.

### What Transfers to a Rust-Based Doctrine

**Direct transfers:**
- ADTs / sum types (Rust's `enum` with fields).
- Exhaustive pattern matching (`match` in Rust; the compiler enforces it).
- "Parse, don't validate" — the doctrine transfers word-for-word; `TryFrom` is the
  Rust spelling of the parse step.
- Newtype pattern — wrapping a primitive in a named type to prevent misuse; Rust's
  tuple structs are the equivalent.
- Named intermediate types per pipeline stage — the Elm compiler pattern transfers
  directly. Make `Src`, `Canonical`, `Optimized` distinct named types, not
  parameterized variants.
- Typeclass laws as capability contracts — the concept transfers; Rust's trait system
  does not enforce laws but the design discipline does.

**Does not transfer:**
- Lazy evaluation — not wanted. The vision requires "assembled into a coherent whole"
  meaning evaluated, not thunked.
- Monad transformer stacks — Rust's `?` and `Result` are the correct equivalent for
  fallible conversion chains; stacks add complexity the vision does not need.
- The Handle pattern — explicitly forbidden by the vision.
- Extension-heavy type-level programming (`TypeFamilies`, `DataKinds`) — Rust has
  const generics and associated types, but the vision does not push toward type-level
  programming; it pushes toward clear named types at value level.

### Fitness Verdict

Haskell's culture is the closest typed-FP tradition to the vision: types-first design,
"parse, don't validate," exhaustive matching, and ADTs as ontology are genuine overlaps.
The Elm compiler and Dhall are the strongest real-world demonstrations that the
architecture is achievable.

The gap is the memory model. Rust's ownership system — move semantics, `From`/`TryFrom`
as a protocol, `Drop` on inputs after conversion — enforces the conversion spine as a
structural property, not a discipline. Haskell can demonstrate the pattern but cannot
enforce it. Laziness makes stage boundaries evaluation-invisible. GC makes input
consumption inexpressible.

The most accurate characterization: Haskell discovered the type-theoretic ideas the
vision rests on. Rust is the language that enforces them.

## Summary Table

| Exemplar           | Vision Match | Strongest Property             | Key Gap |
|--------------------|--------------|-------------------------------|---------|
| Elm compiler       | Strong       | All four parts, type-enforced | No From/TryFrom protocol; GC |
| Dhall              | Strong (partial) | Phase-indexed type parameter | Monad stack in resolver; shared type |
| Pandoc             | Partial      | Universal intermediate type   | Parts 2 and 3 collapsed; large driver |
| GHC                | Partial      | Named IRs (Core/STG/Cmm)      | HscEnv service record; Trees That Grow shares type |
| XMonad             | Partial      | One-line main; value-config   | Reactive domain; inapplicable anatomy |
| Parse-don't-validate | Doctrine   | Names Part 1→2 transition exactly | N/A — conceptual contribution |
