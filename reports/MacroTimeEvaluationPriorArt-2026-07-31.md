# Macro-Time Evaluation Prior Art

TENTATIVE research. Grade: [agent-inference] throughout.

# Problem Statement

The psyche raised this thought about transformation-time evaluation for the
protos typed sugar-language stack:

> Transformation-time ("what other languages call macro expansion time")
> evaluation for a typed sugar-language stack -- program-wide configuration
> data objects that escapes/placeholders in transformer templates can
> reference, with derived values ("template conditions or default values: if
> this isn't set, then derive from this and this and this"), possibly
> requiring "our own evaluation runtime."

His two research questions, verbatim:

> "Is this something that the most advanced macro language systems use
> universally? And is there a good use case for this?"

# System Context

The protos family comprises Ethos (authored sugar, a strictly typed textual
language parsed structurally as a pre-known typed struct), Nomos (the
transformation language: templates shaped like output types with a closed
escape algebra of Realize/Splice/Invoke), Logos (assembly-like true form,
projected to Rust), and NOTA (positional data notation).

Standing laws that constrain any recommendation:

- No string manipulation in transformation (all operations are typed,
  positional, encoded-form to encoded-form).
- All data positional and typed on NOTA substrate.
- Identity via integer encodedID chains, never spellings.
- Proc macros (syn/quote) banned in the codebase.
- Everything round-trips textualform/encodedform.
- The escape algebra is closed at three authored members: Realize (unquote one
  bound value), Splice (expand a bound sequence), Invoke (call another
  transformer). The system has deliberate resistance to growing this algebra.
- No expansion-time evaluation, config-object system, or derived-defaults
  mechanism exists in the current design.

Long-horizon vision: whole programs authored in Ethos with near-full Rust
capability on the Logos side.

# Part 1: Is Expansion-Time Evaluation Universal?

[agent-inference] Yes. Every advanced macro system has some form of
expansion-time evaluation. The variation is in how much of the language is
available at expansion time and how the phases are separated. The spectrum runs
from unrestricted towers (Racket) through typed-but-restricted (Zig comptime)
to implicit fixpoint (Nix modules).

## The Full Tower: Racket Phase Levels

Racket organizes computation into numbered phases: phase 0 (runtime), phase 1
(compile-time / macro expansion), phase 2 (compile-compile-time: macros that
define macros), and so on without bound. Each phase is a separate instantiation
of module-level definitions. The same identifier can be bound independently at
different phases.

Phase shifting happens through imports: `(require (for-syntax "a.rkt"))` shifts
bindings from phase 0 in module `a` to phase 1 in the importing module.
`begin-for-syntax` and `define-for-syntax` elevate definitions by +1 phase
within a single module.

Key properties:

- **Full language at every phase.** Phase 1 code can use any bindings imported
  `for-syntax`, including I/O, mutation, and side effects. There is no
  restriction on what computations run at compile time.
- **Strict phase separation.** Different phases cannot communicate except via
  the protocol of macro expansion. A phase-0 binding is invisible at phase 1
  and vice versa. This prevents accidental cross-phase leakage.
- **Separate instantiation.** A module is instantiated separately at each phase
  where it is needed. Each instantiation has its own mutable state. This avoids
  the "tower of interpreters" problem: modules compile once but instantiate at
  whichever phases are needed.
- **No termination guarantee.** Macro expansion can diverge. This is an
  explicit design choice: restricting compile-time code to total functions
  would sacrifice the "full language at every phase" property.

Sources: Racket Guide, General Phase Levels; Racket Reference, Syntax Model.

## Typed Staging Without a Separate Language: Zig Comptime

Zig's `comptime` is the system most analogous to what protos might need: typed
compile-time evaluation that uses the same language as runtime, without a
separate macro sublanguage.

Ordinary Zig code runs during compilation when parameters or expressions are
marked `comptime`. Types are first-class compile-time values: a function
accepting `comptime T: type` is how generics work, collapsing generics, macros,
and conditional compilation into one mechanism.

Key properties:

- **Typed, same-language evaluation.** No separate macro language. The compiler
  evaluates ordinary Zig code at compile time.
- **Hermetic by design.** No I/O, no side effects, no host-architecture
  leakage. Build-time data must come through `build.zig`. This ensures
  reproducible cross-compilation.
- **No dynamic code generation.** No string-to-code injection. Everything
  operates on typed values, not text. (This aligns directly with protos's "no
  string manipulation" law.)
- **Evaluation budget for termination.** The compiler imposes a limit of 1000
  backward branches by default. `@setEvalBranchQuota` raises the limit for
  complex computations. This prevents runaway loops without requiring
  termination proofs.
- **No custom syntax.** No parser extension points. The language surface is
  fixed.

Sources: Zig documentation; Matklad, "Things Zig Comptime Won't Do" (2025).

## Typed Staged Metaprogramming: Template Haskell, MetaOCaml, Scala 3

These three systems represent typed multi-stage programming with explicit
splice/quote constructs.

**Template Haskell.** Untyped splices `$(e)` evaluate an expression of type
`Q Exp` at compile time, producing an AST fragment that is type-checked
post-splice. Typed splices `$$(e)` guarantee the generated code has a known
type. The Q monad provides the metaprogramming environment (name generation,
reification of the type environment). The stage restriction is cross-module: a
function cannot be spliced in the module where it is defined. This is the main
ergonomic pain point.

**MetaOCaml.** Multi-stage programming with brackets `.< e >.` (delay) and
escape `.~e` (splice). The type system tracks stages statically: `int code`
represents an `int` computation deferred to the next stage. The key property is
unconditional type safety: a well-typed MetaOCaml program generates only
well-typed programs, by construction, without post-splice type-checking. Scope
extrusion is detected dynamically (since version N101). This is the strongest
safety guarantee among staging systems.

**Scala 3.** Quotes `'{expr}` produce `Expr[T]`; splices `${expr}` evaluate
them back. Staging levels are tracked: local variables can only be used at
their definition's staging level. Top-level splices are restricted to static
method calls (avoiding the need for a full interpreter at compile time). This
is a pragmatic middle ground between TH's full flexibility and MetaOCaml's
strict safety.

## The Degenerate Case: Rust

[agent-inference] Rust's staging model is the weakest among serious systems,
fragmented across three mechanisms that do not compose:

- **`const fn`**: Typed compile-time evaluation within the compiler (Miri
  interpreter). No heap allocation, no I/O, limited operations.
- **Build scripts (`build.rs`)**: A separate Rust program. Communicates via
  stdout directives and environment variables. Opaque to the compiler.
- **Proc macros**: Token-stream-to-token-stream functions in a separate crate.
  Full Rust execution but operate on untyped token streams before type
  checking.

The three mechanisms do not compose into a coherent staging discipline. This is
a recognized limitation. The protos system has already banned proc macros.

## Fixpoint Configuration: Nix Module System

The Nix module system is the closest existing model to the psyche's
"if this isn't set, derive from this and this and this" pattern. It is a lazy
fixed-point evaluator over typed configuration attributes.

The core primitive is `lib.fix = f: let x = f x; in x;`. A function receives
its own output as input; laziness prevents infinite recursion as long as no
actual circular data dependency exists. `lib.evalModules` extends this:
it collects all module functions, merges their option declarations and
definitions, and passes the final merged `config` attrset back to each module
as its argument.

Key mechanisms:

- **Derived defaults with priorities.** `lib.mkDefault` (priority 1000) and
  `lib.mkOverride` (arbitrary priority integer). Lower numbers win. A module
  can write `config.services.bar.port = lib.mkDefault (config.services.foo.port + 1);`
  -- the default is derived from another option but can be overridden.
- **Conditional definitions.** `lib.mkIf config.services.foo.enable { ... }`
  makes definitions conditional on other configuration values.
- **Lazy cycle resolution.** A can default-depend on B and B on A, as long as
  one is explicitly set. If both remain lazy, Nix hits infinite recursion at
  evaluation time.
- **No static cycle detection.** Nix is Turing-complete; termination is not
  guaranteed. Infinite recursion is a runtime error.
- **Dynamic typing with option types.** `types.int`, `types.listOf`,
  `types.submodule` provide checking but it is dynamic, not static.

## Other Configuration Languages

**Dhall.** Total evaluation (guaranteed termination) via System F-omega. No
general recursion; iteration only through bounded folds. Strong static typing.
Values flow strictly forward through let bindings; no fixpoint/lazy derivation.
Relevant as a safety ceiling but lacks the circular-derivation pattern the
psyche described.

**CUE.** Lattice-based unification: types and values live on the same lattice.
`int & 5` yields `5`. Default values via disjunctions: `port: int | *8080`.
Unification is commutative, associative, idempotent, so order does not matter.
Some cyclic references resolve (`a: b + 1; b: a - 1; b: 1` yields `a=2, b=1`).
Not Turing-complete by design.

**Jsonnet.** Prototype-based OOP with late binding. `self` is re-bound at each
composition, enabling open recursion: `{ basePort: 8080, derivedPort: self.basePort + 1 }`.
When a child overrides `basePort`, `derivedPort` updates automatically. Turing-complete,
lazy, no static types.

**Nickel.** Gradual typing + Nix-style laziness + CUE-inspired record merging.
Records merge with metadata (defaults, priorities, type contracts). Lazy
self-reference within merged records. Turing-complete. Aims to be "Nix but
with types and contracts." The closest config-language analogue to what protos
might want if types and fixpoint derivation must coexist.

## Summary Table

[agent-inference] Positioning each system on axes relevant to protos:

| System | Expansion-time eval? | Typed? | Derived defaults? | Termination guarantee? | Separate language? |
|---|---|---|---|---|---|
| Racket | Full tower (unbounded phases) | Untyped macros | No (imperative) | No | No (same language) |
| Zig | comptime (same language) | Yes | No (manual) | Budget-bounded | No |
| Template Haskell | Typed splices | Yes | No | No | No (same + Q monad) |
| MetaOCaml | Typed staging | Yes (strongest) | No | No | No |
| Scala 3 | Quotes/splices | Yes | No | No | No |
| Rust | const fn / build.rs / proc macros | Partial | No | Partial (const fn) | Yes (build.rs) |
| Nix modules | Lazy fixpoint | Dynamic | Yes (exactly) | No | N/A (config lang) |
| Dhall | Total evaluation | Yes (strong) | Forward-only | Yes (total) | N/A (config lang) |
| CUE | Constraint unification | Yes (lattice) | Via constraints | Yes (not Turing-complete) | N/A (config lang) |
| Jsonnet | Late-bound self | No | Via self-reference | No | N/A (config lang) |
| Nickel | Lazy + contracts | Gradual | Via merge + priorities | No | N/A (config lang) |

[agent-inference] The answer to the first question is unambiguously yes:
expansion-time evaluation is universal in advanced macro systems. Every system
surveyed has it. The variation is in power, typing discipline, and termination
guarantees. No serious macro system operates without some form of compile-time
computation.

# Part 2: Use Cases Mapped to the Psyche's Examples

[agent-inference] The psyche identified three specific needs. Here is how the
surveyed systems address each.

## Program-Wide Configuration Objects Referenced from Templates

This is the "config object" idea: a data structure available at transformation
time that templates can read via some reference mechanism.

- **Nix modules** do exactly this. Every module receives a `config` attrset
  representing the merged state of all configuration. Templates (module
  definitions) reference it freely: `config.services.foo.port`.
- **Zig comptime** achieves this through comptime parameters and
  `@import("build_options")`, where build.zig can set options that are
  available as comptime constants throughout the program.
- **Racket** does this through phase-1 parameters or compile-time state
  shared via `define-for-syntax`.
- **Rust build.rs** does this crudely through `env!("CARGO_CFG_...")` and
  `cfg!(...)` predicates, but these are string-typed and limited.

The strongest use case: when a program has cross-cutting configuration (e.g.,
a database URL used in multiple generated modules, a feature flag that
conditionally includes certain transformations, a naming convention applied
across all generated types), having a typed config object avoids repeating
the same values as explicit parameters to every transformer invocation.

## Derived Values ("if this isn't set, then derive from this and this")

This is the fixpoint/default-derivation pattern.

- **Nix modules** are the canonical example: `mkDefault` with priority,
  conditional derivation via `mkIf`, full fixpoint semantics.
- **Nickel** adds static/gradual types to the same pattern via record merging
  with priority metadata.
- **CUE** handles it through constraint refinement and default markers in
  disjunctions, with the safety property that conflicting defaults are
  rejected rather than silently resolved.
- **Jsonnet** handles it through late-bound `self` references, where derived
  fields automatically update when base fields are overridden.

The strongest use case: when transformation produces many output declarations
whose parameters have logical relationships (e.g., "the HTTP server port
defaults to the base port + 1", "the TLS configuration defaults to enabled if
the deployment target is production", "the serialization format defaults to
the project-wide format unless this module overrides it"). Without derived
defaults, every such relationship must be manually specified at every use site.

## Template Conditions

Conditional inclusion/exclusion of template regions based on config state.

- **Nix** `mkIf`: definitions are conditional on other config values.
- **Zig** `if (comptime condition)`: compile-time branching that eliminates
  dead code.
- **Racket**: macro transformers can inspect compile-time state and
  conditionally produce different expansions.
- **Rust** `cfg!(...)` and `#[cfg(...)]`: the most limited form, restricted
  to predefined configuration predicates.

The strongest use case: when some Nomos templates should produce different
Logos output depending on program-wide state (e.g., "include debug assertions
if the config says debug mode", "generate async variants if the config enables
async", "omit serialization impls if the module is internal-only").

# Part 3: Known Hazards

[agent-inference] Five hazards recur across all surveyed systems.

## Termination

- **Unrestricted systems** (Racket, TH, MetaOCaml, Nix, Jsonnet, Nickel):
  expansion-time evaluation can diverge. Nix and Jsonnet surface infinite
  recursion as runtime errors. Racket and TH surface it as a hung compiler.
- **Budget-bounded** (Zig): a backward-branch counter provides a soft
  guarantee. Compile-time evaluation halts after a configurable number of
  iterations, with a clear error.
- **Total** (Dhall): guaranteed termination via System F-omega. No general
  recursion.
- **Lattice-bounded** (CUE): not Turing-complete; no general recursion or
  lambdas.

For protos: [agent-inference] since the evaluation domain is NOTA config
objects with typed derivation rules (not arbitrary computation), a
budget-bounded or total approach is feasible. The psyche's examples (derived
defaults, conditional inclusion) do not require Turing-completeness.

## Dependency Cycles

- **Lazy systems** (Nix, Jsonnet, Nickel): cycles are tolerated as long as
  no actual circular data dependency exists. Lazy evaluation defers enough
  that A-depends-on-B-depends-on-A resolves if one side is explicitly set.
  True cycles produce runtime errors.
- **Strict systems** (Dhall, Zig, Rust const): cycles are compile-time errors.
  No risk of runtime divergence, but less expressive for configuration
  derivation.
- **CUE**: some cycles resolve through algebraic reasoning; others are errors.

For protos: [agent-inference] the psyche's derived-defaults pattern inherently
involves potential cycles (A defaults from B, B defaults from A). A lazy or
priority-based resolution strategy (like Nix) handles this naturally. A strict
strategy would require the author to explicitly order derivation, which is more
verbose but safer.

## Hygiene and Scoping

- **Racket**: hygienic macros via syntax objects with lexical context. The
  gold standard.
- **MetaOCaml**: lexical scope automatically maintained; variable capture
  impossible by construction. Scope extrusion detected dynamically.
- **Scala 3**: symbolic references; splice scope is validated.
- **Template Haskell**: less hygienic; name capture is possible with untyped
  splices.
- **Config languages**: scoping is simpler (no binding forms beyond let/record
  fields). Nix uses lexical scope within modules; the `config` fixpoint is
  the only cross-module sharing mechanism.

For protos: [agent-inference] the existing encodedID system and typed escape
algebra already provide strong hygiene. Config references would go through a
typed mechanism (like a new prefix) that resolves to encodedIDs, not spellings.
This is inherently hygienic because there are no textual names to capture.

## Staging Discipline (What Phase Can See What)

- **Racket**: strict phase separation enforced by the import system. Phase N
  cannot see phase N-1 bindings except through macro expansion protocol.
- **Zig**: comptime code sees only comptime-available data. Runtime data is
  invisible. Clean separation.
- **Template Haskell**: cross-module restriction enforces that splice code is
  compiled before use. Reification lets compile-time code inspect the type
  environment up to a declaration-group boundary.
- **Nix modules**: no phase separation. Everything is one evaluation phase
  (the fixpoint). This works because Nix is a pure config language with no
  runtime.

For protos: [agent-inference] there is already an implicit phase separation:
Ethos authoring -> Nomos transformation -> Logos output. Config evaluation
would be a new phase that precedes or accompanies Nomos transformation. The
question is whether config evaluation can see transformation-internal state
(it probably should not) and whether templates can see config state (they
must, by definition).

## Determinism and Reproducibility

- **Zig comptime**: deterministic by design (no I/O, no host leakage).
- **Dhall**: deterministic (total, pure).
- **CUE**: deterministic (commutative unification).
- **Nix**: evaluation is pure and deterministic; non-determinism enters only
  through derivation builds (outside the module system).
- **Racket/TH**: compile-time code can perform I/O, making expansion
  potentially non-deterministic.

For protos: [agent-inference] the existing laws (no side effects in
transformation, typed positional data) already ensure determinism. Config
evaluation over NOTA data inherits this property as long as the evaluation
does not introduce I/O or non-deterministic operations.

# Part 4: Candidate Designs for Protos

[agent-inference] Three candidate designs, each consistent with the existing
escape algebra and system laws.

## Candidate A: Config-Object Reference Prefix (Minimal Extension)

Add a single new reference mechanism: a prefix (e.g., `Config.`) that
resolves to a program-wide typed NOTA config object during transformation.

**Mechanism.** A Config NOTA object is declared at program scope in Ethos (or a
dedicated config file). During transformation, Nomos templates can reference
config values at escape positions using a new prefix: `Config.<path>`.
This is not a new escape-algebra member; it is a new binding source for
existing Realize escapes. Templates write `Realize.Config.featureFlag`
where they currently write `Realize.inputBinding`.

**Derived values.** Config fields can have default expressions that reference
other config fields: a simple expression language over NOTA values (arithmetic,
boolean logic, conditionals, field references). Evaluation is strict and
topologically ordered: the config evaluator detects cycles statically and
rejects them.

**Example (notional syntax).**

```
Config {
  basePort 8080
  httpPort (Config.basePort)
  grpcPort (Config.basePort + 1)
  debugMode false
  enableTracing (Config.debugMode)
}
```

A Nomos template:

```
Template ServerConfig -> Logos.StructDecl {
  field port Realize.Config.httpPort
  field tracing Realize.Config.enableTracing
}
```

**Trade-offs.**

- Pro: minimal extension to the escape algebra (new binding source, not new
  escape type). Strict evaluation with static cycle detection is simple to
  implement and reason about.
- Pro: config object is a typed NOTA struct; it fits the existing substrate.
- Con: no lazy/fixpoint derivation. "If this isn't set, derive from that"
  requires explicit defaulting logic in the expression language. The author
  must provide explicit defaults or explicit overrides; there is no priority
  system.
- Con: the expression language is a new evaluation surface. Even a restricted
  one requires design, implementation, and testing.

## Candidate B: Nix-Style Lazy Fixpoint Over NOTA (Full Derivation)

A lazy fixed-point evaluator over typed NOTA config attributes, closely
modeled on Nix's module system but with static types.

**Mechanism.** Multiple config modules contribute typed option declarations
with optional default expressions. The evaluator merges all declarations,
passes the merged result back as input (fixpoint), and lazily evaluates each
field on demand. Priority annotations (e.g., `default`, `override`) resolve
conflicts.

**Derived values.** Config fields reference other fields freely, including
circular references that resolve when one side is explicitly set. Laziness
defers evaluation until a value is demanded.

**Example (notional syntax).**

```
ConfigModule database {
  option host : Text
  option port : Int (default 5432)
  option url : Text (default (
    "postgres://" ++ Config.database.host ++ ":" ++ show Config.database.port
  ))
}

ConfigModule server {
  option port : Int (default (Config.database.port + 1000))
  option debug : Bool (default false)
  option logLevel : Text (default (if Config.server.debug then "trace" else "info"))
}
```

**Trade-offs.**

- Pro: maximum expressiveness for derived defaults. Exactly matches the
  psyche's "if this isn't set, derive from this and this" pattern.
- Pro: proven model (Nix module system serves this purpose for all of NixOS).
- Con: lazy evaluation over typed data is a significant runtime to implement.
  Cycle detection becomes dynamic (runtime errors on true cycles) rather than
  static.
- Con: the string concatenation in the URL example violates the "no string
  manipulation" law. A strict version would need to keep values as typed
  positional data and compose them structurally, not textually.
- Con: debugging lazy fixpoint evaluation is notoriously difficult. Nix's
  error messages for infinite recursion are famously unhelpful.

**Important note.** [agent-inference] The example above uses string
concatenation for illustration. A protos-legal version would need to compose
the URL from typed positional components (host field, port field) that are
assembled at the Logos output boundary, not concatenated during config
evaluation.

## Candidate C: Typed Constraint Derivation (CUE-Inspired)

A constraint-based system where config fields are refined by typed constraints
from multiple sources, with unification resolving the final values.

**Mechanism.** Config fields are declared with type constraints. Multiple
modules can contribute constraints to the same field. The evaluator unifies
all constraints, producing either a unique value or an error (conflicting
constraints). Default values are expressed as constraints with lower priority.

**Derived values.** A field's constraint can reference other fields. The
evaluator topologically orders constraints and evaluates in dependency order.
True cycles are static errors (unlike Candidate B).

**Example (notional syntax).**

```
Config {
  basePort : Int & >=1024 & <=65535
  basePort : default 8080
  httpPort : Int & default Config.basePort
  grpcPort : Int & default (Config.basePort + 1)
  debugMode : Bool & default false
  enableTracing : Bool & default Config.debugMode
}
```

A Nomos template references these the same way as Candidate A:
`Realize.Config.httpPort`.

**Trade-offs.**

- Pro: deterministic (unification is commutative and idempotent). Order of
  constraint declaration does not matter.
- Pro: conflicting constraints produce clear errors rather than silent
  priority resolution.
- Pro: static cycle detection (dependency-ordered evaluation).
- Pro: the constraint language maps naturally to NOTA's typed, positional
  model.
- Con: less expressive than Candidate B for the "if not set, derive" pattern.
  The constraint model does not naturally express priority-based override
  chains the way Nix does.
- Con: the unification/lattice model is conceptually dense and may be
  unfamiliar to Ethos authors.

# Part 5: Ranked Recommendation

[agent-inference] Ranking by fit to protos system laws and the psyche's stated
needs:

**1. Candidate A (Config-Object Reference Prefix)** is the recommended
starting point. It is the minimal extension, requires no new evaluation
paradigm beyond a small expression language over typed NOTA values, fits
the existing escape algebra as a new binding source rather than a new escape
type, and handles the majority of the psyche's examples (program-wide config,
template conditions, simple derived defaults). Static cycle detection and
strict evaluation align with the system's existing determinism guarantees.

**2. Candidate C (Typed Constraint Derivation)** is the recommended direction
if Candidate A proves insufficient. It preserves determinism and static
analysis while adding more expressive derivation through constraint
unification. It is a natural evolution from A: config fields gain constraint
annotations, and the evaluator gains a unification step.

**3. Candidate B (Lazy Fixpoint)** is the most powerful but carries the
highest implementation and debugging cost. It should be considered only if the
program-wide configuration genuinely requires circular derivation chains that
cannot be expressed as forward-flowing constraints. The Nix module system
proves this model works at scale, but Nix pays for it with dynamic typing
and difficult-to-debug infinite recursion.

## The Single Question Whose Answer Most Changes This Ranking

[agent-inference] **Do the psyche's real-world configuration patterns require
circular derivation (A defaults from B, B defaults from A), or do they flow
in one direction (A defaults from B, B defaults from C, with no cycles)?**

If derivation is acyclic (which the psyche's examples so far suggest), then
Candidate A with strict topological evaluation is sufficient and Candidate B's
lazy fixpoint is unnecessary complexity. If real patterns require circular
derivation, then Candidate B or a lazy variant of Candidate C becomes
necessary, and the implementation cost of a lazy evaluator must be accepted.

## Correction (appended 2026-07-31, after independent review)

This report's headline claim — that expansion-time evaluation is universal in
advanced macro systems — overstates the evidence, as identified by an
independent Codex research pass
(reports/protosVisionReacquisition/2-Research-psyche-vision-open-questions-and-proposals.md,
section 9.5). R7RS `syntax-rules` is an advanced hygienic system that performs
pattern/template transcription without arbitrary expansion-time procedure
execution; R6RS separates transcription (`syntax-rules`) from procedural
(`syntax-case`) macros. The corrected, narrower conclusion: many powerful
macro, staging, and configuration systems perform computation before runtime,
but general evaluator execution is not universal, and structural transcription,
typed evaluator execution, and stage transition are three distinct capabilities
— Nomos may need all three, and none entails the others. The per-system
surveys, hazard analysis, and candidate designs in this report are unaffected;
only the universality framing is retracted.
