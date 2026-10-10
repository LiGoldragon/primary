# Transformer Prior Art Survey

**Absorbed-superseded.** The `ProtosEngineDesign-2026-07-29.md` compilation
carries the ranked design lessons compactly (section 11). This document
remains the detailed survey with per-system analysis, mechanism mapping, and
failure-mode documentation; the compilation references it as the live
prior-art record.

Date: 2026-07-29. Currency of claims: web-verified July 2026 unless marked otherwise.

Purpose: survey existing systems whose mechanisms overlap the ultra-transformer
programming system — the Nomos engine that compiles authored transformer source
into a typed engine converting Ethos typed data into generated Logos typed data —
so the design can steal proven ideas and avoid documented failure modes. This is
analysis, not implementation.

## The Lens

Every system below is judged against the same constraints:

- Programs exist as typed encoded data ("true form"); text is only a projection.
- Identity is integer encodedID chains, never spellings.
- Transformation is strictly string-free: placeholders are typed positions
  keying what goes where, including positional insertion into specific vector
  slots, with recursive transformer invocation.
- The engine loads the complete Ethos and Logos type universes into its runtime.
- Transformers may depend on the entire input payload (cross-declaration,
  compiler-grade analysis, on the model of rustc's wide-spectrum analyses
  before codegen).
- Long term: correctness verification at or beyond rustc's level; Logos
  compiling to assembly through LLVM; Rust as the current substrate, treated
  as an assembly language.

No surveyed system satisfies all of these. Each satisfies one or two well, and
the compromises they made under the remaining constraints are the most valuable
data in this report.

## 1. MLIR — dialects, DRR, PDL/PDLL

**What it is.** LLVM's extensible compiler framework. All IR lives in
"dialects" — pluggable, typed operation universes — and compilation is
progressive lowering between dialect levels. It is the industry's largest
running experiment in multi-level typed transformation, the industrial analog
of Ethos-to-Logos lowering.

**Mechanism mapping.** A dialect declares operations in ODS/TableGen: typed
operands, typed results, typed attributes, traits, and a verifier per op. Types
are uniqued immutable objects interned in the context — compared by pointer,
never re-parsed. Three pattern systems sit on top. DRR (TableGen declarative
rewrites) maps a source DAG to a result DAG with named typed bindings,
generating C++ patterns at build time; it is single-root, weak on variadics and
regions, and widely disliked. PDLL is the important precedent: an authored
pattern language whose pipeline is exactly the Nomos shape — PDLL text is
compiled into the PDL dialect (patterns represented as typed IR themselves),
lowered to an interpreter dialect, and executed as bytecode by a generic engine
at runtime. Patterns bind typed values and construct replacement ops as typed
entities with operands slotted by position; no string splicing exists in the
rewrite semantics. Bytecode was reported around 10x smaller than equivalent
compiled C++ and lets users supply patterns without recompiling the compiler.
The dialect conversion framework does multi-level lowering: a conversion target
declares per-op legality, patterns fire until everything is legal, and type
converters supply typed materializations bridging old and new types
mid-conversion (a 1:N type-conversion revamp landed 2024–2025).

**What Nomos should steal.** The dialect idea itself — a registered, verified,
typed operation universe per level, with lowering as the only path between
levels. Legality targets: "conversion is done when every construct is legal for
the target universe" is a clean, checkable termination condition for a
transformation run. Patterns-as-typed-data: PDL proves transformation logic can
itself be typed IR, which is what an encoded Nomos transformer is.

**Where it compromises.** Operation and attribute identity is interned name
strings ("arith.addi") — spelling-based at the registry level, mitigated by
C++ TypeID but never eliminated. Textual round-tripping is culturally central.
And the sociology matters: verified July 2026, PDLL is alive but stagnant —
in-tree, documented, not deprecated, still receiving fixes, but feature
development largely stalled after its champion stepped back around 2023; a 2024
RFC to add basic arithmetic expressions shows how incomplete it remains. The
overwhelming majority of production patterns are hand-written C++, and
community momentum went to the transform dialect (orchestration-as-IR) instead.
Debugging bytecode-interpreted patterns is opaque; there is no overlap or
exhaustiveness checking; the greedy pattern driver gives phase-ordering
nondeterminism; native C++ constraint and rewrite escape hatches reintroduce
opacity.

**Verdict: high.** Closest whole-architecture precedent, and the clearest
warning: a declarative pattern language dies when authors can defect to the
host language for anything it cannot express.

## 2. JetBrains MPS — projectional editing and the generator

**What it is.** A language workbench where programs are stored as ASTs and
every editor view is a projection; text is never the source of truth. Every
node has a unique ID and references are node-ID pointers, not name lookups.
Actively maintained: releases 2025.1 through 2025.3 (May–Dec 2025), bugfix
wave July 2026, 2026.1 EAP underway.

**Mechanism mapping.** The generator is the closest existing analog of the
typed-skeleton-with-placeholders design. Templates are written *in the target
language*: a template is a legal target-language AST fragment, so it is
structurally checked against the target metamodel while authored — the target
language's editor, constraints, and type system apply to the template itself.
Macros annotate template nodes as typed positions: node macros (COPY_SRC, LOOP,
IF, SWITCH, CALL, MAP_SRC, INSERT, WEAVE) control filling, iteration, and
branching; property macros compute attribute values; reference macros compute
reference targets. Recursion is implicit and pervasive: whenever the generator
copies an input node to output, it looks for an applicable reduction rule and
applies it, iterating over transient models in micro-steps until no rules fire —
recursive transformer invocation, working in production for two decades.
Cross-linking of generated nodes is identity-based: mapping labels record
(input node → generated node) pairs, and a reference macro asks the generation
context for "the output node generated from input N under label L". Because
targets are node IDs, links survive subsequent transformation stages.
Generation plans give explicit multi-stage pipelines with inspectable
checkpoint models (substantially reworked in 2025.3).

**What Nomos should steal.** Templates authored as legal target-universe
fragments, so skeleton well-formedness is checked at authoring time. The
mapping-label mechanism — this is the exact answer to "how does a generated
reference point at another generated node": by input-identity plus label, never
by name. Transient models saved per stage as the debugging surface.

**Where it compromises.** Well-typedness of the *generated* model is not
guaranteed: macro-computed values and cross-rule interactions fail only at
generation time, and the mbeddr lessons-learned literature (Voelter et al.,
SoSyM) reports generators becoming complex and error-prone, with mbeddr
needing roughly 2,300 tests to hold the line. String escape hatches exist:
dynamic references resolved by name and scope (docs explicitly warn against
them), "generate unique name" facilities, and the final stage is TextGen —
the pipeline bottoms out in strings because the target is ordinary compilers.
Generator debugging is trace archaeology; performance and model-migration
burden are documented, ongoing costs.

**Verdict: high.** The closest production analog; copy the label-based
identity plumbing and recursive reduction, reject the name-resolved dynamic
references, the name-generation utilities, and generation-time-only failure.

## 3. Typed staging — Scala 3 quotes/splices, Typed Template Haskell, MetaOCaml

**What it is.** Multi-stage programming: programs construct typed program
fragments and compose them, with the type system guaranteeing the generated
program is well-typed *before* the generator ever runs.

**Mechanism mapping.** The quote/splice boundary is a typed hole, not a string
interpolation site. `Expr[T]` (Scala 3), `Code T` (BER MetaOCaml), typed
quotes (GHC) all mean: a value representing a code fragment whose eventual
type is T, and a splice is only legal where a term of that type is expected.
A type mismatch in a template is a generator-compile-time error — precisely
the Nomos property that a placeholder is a typed position keying what fits
there. Phase consistency rules prevent a stage-n binding from leaking into the
wrong stage; cross-stage persistence lifts *values* (through typed lifting
instances or references to top-level definitions), never spellings. Scala 3
quoted patterns add the analysis half: `case '{ ($x: Int) + 1 }` pattern-matches
on typed code and binds `x: Expr[Int]` — typed destructuring of programs.

**What Nomos should steal.** The core semantics: transformer skeletons whose
holes carry Logos types, checked when the transformer is compiled, before any
Ethos payload exists. Typed code patterns for the input side. Persistence-as-
reference for anything crossing the stage boundary.

**Where it compromises.** Scala 3's reflection API escape hatch builds raw
trees with far weaker guarantees, and real macros routinely drop into it. In
Haskell the untyped quote API still dominates the ecosystem as of 2026, and
even typed quotes are type-correct but not fully scope-correct. MetaOCaml
exposes the deepest lesson: scope extrusion — with effects, a code value
containing a bound variable can escape its binder's scope, producing
ill-scoped output despite well-typed staging. Typed environment classifiers
fixed this on paper but were too cumbersome; BER MetaOCaml (N153, May 2025,
actively maintained) instead runs a dynamic scope-extrusion check with good
diagnostics, plus sanctioned let-insertion. Note what scope extrusion *is*:
a name-identity bug. With encodedID references and explicit binder ownership,
extrusion degenerates into a detectable dangling-reference error rather than a
silent capture hazard.

**Verdict: high.** The direct ancestor of the typed-placeholder discipline;
steal `Expr[T]` semantics, design out scope extrusion via ID-based binding.

## 4. Racket — syntax-parse and hygiene

**What it is.** The most mature textual macro system. Macros are functions
from syntax objects to syntax objects, where a syntax object is a datum plus
lexical context (scope sets) plus source location — structured values, never
strings.

**Mechanism mapping.** syntax-parse is the gold standard for declarative
validation and destructuring of structured input: patterns with annotated
variables (`x:id`, `e:expr`), reusable syntax classes carrying side conditions
and named attributes, ellipsis-depth checking, and automatically generated
high-quality error messages with source locations. Hygiene (sets of scopes,
Flatt, POPL 2016) solves one precise problem: identifiers introduced by a
transformer must neither capture nor be captured by user identifiers, even
when both are spelled the same.

**What Nomos should steal.** The syntax-class idea — reusable, named,
predicate-carrying input patterns that produce structured attribute bindings
and excellent errors — maps directly onto typed Ethos destructuring. And the
negative lesson, the strongest single argument in the literature for encodedID
identity: hygiene is machinery for recovering referential identity from
spellings. Scope sets exist because an identifier in macro output is a string
that must be re-resolved. If every reference is a direct node-ID edge to its
binder, accidental capture is unrepresentable and the entire apparatus
evaporates.

**Where it compromises / what survives the ID model.** Racket is inherently
spelling-based; that is the point of studying it. Three problems survive even
under encodedIDs and must be designed deliberately: (a) intentional capture —
Racket's `datum->syntax` deliberately re-attaches user context (e.g. an
anaphoric `this`); Nomos needs an explicit, typed "bind into caller's
namespace" operation rather than pretending the need does not exist;
(b) transformers that synthesize new binders plus references to them must mint
fresh IDs and thread them — safe by construction with IDs, but the transformer
language needs first-class fresh-binder values; (c) generated references to
not-yet-generated declarations (forward/recursive links) need a resolution
step or promise-IDs.

**Verdict: medium-high.** Its central mechanism is obsolete under Nomos's
identity model — which is itself the finding — but syntax-parse's
destructuring-and-errors discipline should be stolen wholesale.

## 5. Strategic term rewriting — Stratego/XT + Spoofax, Rascal MPL, TXL

**What it is.** The rewriting school: transformation as sets of small rewrite
rules plus explicit strategies controlling where and when rules apply.

**Mechanism mapping.** Stratego's lasting contribution is the separation of
rules (pure, local pattern-to-pattern) from strategies: combinators for
sequencing and choice, generic traversals (topdown, bottomup, innermost), and
congruences for per-constructor traversal. Dynamic rules — rules created at
runtime that close over context, scoped and undoable — are its answer to
context-sensitive transformation. Rascal is a statically typed metaprogramming
language whose `visit` statement gives strategy-annotated typed traversal with
case arms: typed patterns plus built-in strategic traversal, the closest
existing thing to a typed engine core. TXL writes rules as concrete-syntax
patterns parsed against the grammar, so patterns are grammatically well-formed
by construction.

**What Nomos should steal.** Rule/strategy separation: transformation logic
and traversal schedule as orthogonal, composable, *typed* values. Rascal
demonstrates typed strategic traversal is achievable. Dynamic rules gesture at
what whole-payload-dependent transformers need, though attribute grammars
(section 10) do it more safely.

**Where it compromises.** Classic Stratego rewrites untyped terms — nothing
guarantees a rule preserves well-formedness or even arity; failures are silent
strategy failure or malformed trees downstream. Stratego 2 (around 2020) added
a *gradual* type system, but it is opt-in and generic traversals needed special
typing rules; Spoofax remains academically alive (2.5.23, April 2025; Spoofax 3
in development) but never industrially dominant. Rascal is the sharper warning:
the analysis side is fully typed trees, and then code generation is done with
string templates — interpolated strings with loops and conditionals. The match
side is typed and the guarantee is lost at the emit side, exactly the failure
mode Nomos forbids. Rascal is active (0.41.x, Dec 2025). TXL is text in, text
out, identity by spelling, types only as grammar nonterminals — the purest
text-centric pole of the design space and a complete anti-model.

**Verdict: medium.** Steal the rule/strategy separation and the typed visit;
keep Rascal's emit-side collapse and Stratego's untyped terms as the two named
failure modes Nomos exists to eliminate.

## 6. Cranelift ISLE

**What it is.** A typed s-expression term-rewriting DSL inside Cranelift
(Wasmtime), used for instruction lowering and, since the 2022 e-graph work,
mid-end optimization rewrites. Authored rule source is compiled at build time
into Rust decision trees. This is the production system whose pipeline most
directly parallels "compile Nomos transformer source to Rust."

**Mechanism mapping.** ISLE declares types mirrored to Rust enums and terms
with fully typed signatures. Terms have constructors (build a value) and
extractors (a term run in reverse, for matching); rules are typed
left-hand-side pattern to typed right-hand-side expression, with integer
priorities for disambiguation. The ISLE compiler merges all rules into a match
trie and emits native Rust — no interpretation, no strings in rule semantics;
symbols compile down to Rust type identity. A static overlap checker flags
same-priority overlapping rules. External constructors and extractors bind to
Rust trait methods on a context object; that is where side effects and any
cross-instruction context live.

**What Nomos should steal.** The compilation story wholesale: authored typed
rules become generated Rust, which is fast, debuggable with ordinary tooling,
and statically checkable as a whole rule set (overlap today, exhaustiveness
plausibly). Above all, the verification path: Crocus (ASPLOS 2024) annotates
ISLE terms with SMT bit-vector specifications and verified aarch64 integer
lowering rules, reproducing a severity-9.9 CVE and finding two new bugs;
Arrival (OOPSLA, Oct 2025) scales this by checking rules against ARM's
authoritative machine-readable ISA semantics, and the verifier lives in-tree.
Small, total, typed rules are the unit that makes per-rule SMT verification
tractable — this is the most credible existing path toward the "rustc-grade
correctness for a rule language" ambition.

**Where it compromises.** Multi-result values are awkward; there is no general
iteration or recursion beyond what terms encode; rules see one instruction
tree, not the whole function, so whole-payload context arrives only through
external Rust constructors — and every external constructor is opaque to the
overlap checker and a hole in verification coverage that must be manually
specified.

**Verdict: high.** The best precedent for the transformer-compilation slice,
and its sharpest lesson: verification coverage is bounded by how much logic
leaks into escape hatches.

## 7. rustc query system and Salsa

**What it is.** rustc organizes compilation as demand-driven pure queries over
inputs with automatic dependency tracking. Salsa is the reusable Rust library
implementing the same model; rust-analyzer is built on it. This is the
architectural pattern for cross-declaration transformer dependencies.

**Mechanism mapping.** Query results are hashed to 128-bit stable
fingerprints. The red-green algorithm walks a node's recorded dependencies
from the previous session: if a dependency re-executed but produced an
unchanged fingerprint, dependents stay green — early cutoff, so a whole-payload
analysis that changed but produced the same answer does not cascade. Stable
identity across runs is bridged by DefPathHash lookup tables at cache load.
New Salsa (very active: 0.26.0 Feb 2026 through 0.28.1 Jul 2026) adds tracked
functions, tracked structs — derived entities whose identity is *minted by the
creating query* as stable integer IDs across revisions — interning,
accumulators, durability tiers that skip revalidation of rarely-changing
inputs, cancellation, and fixpoint cycle support. rust-analyzer completed its
port to new Salsa in March 2025; initial regressions were severe (roughly 4x
on cache-priming time and memory) and were then largely clawed back through
1H 2025–2026, with fine-grained cancellation landing February 2026.

**What Nomos should steal.** The whole execution architecture. A transformer
that depends on a cross-declaration analysis should declare that dependence as
a query; tracking plus early cutoff make whole-payload dependence affordable
and incremental instead of a recompile-the-world hazard. Tracked-struct
identity minting is congruent with encodedID chains: derived entities get
stable integer identity from their creating computation. Durability tiers map
naturally onto "the Logos type universe changes rarely; the payload changes
constantly."

**Where it compromises.** rustc's cross-session stable identity, DefPathHash,
is a hash of a *name path* — spellings leak into the identity layer, which is
precisely the Nomos anti-pattern, and encodedIDs would replace it cleanly and
more robustly. The input edge is still text re-parsed each session; spans and
diagnostics live as side channels outside the pure-query discipline. The
rust-analyzer migration shows the identity and caching layers dominate
performance and that retrofitting them is expensive — a reason to build them
in from the start.

**Verdict: high.** Adopt as the execution architecture; replace the
name-derived stable-ID layer with true encodedID identity.

## 8. Unison

**What it is.** A language where a definition is identified by a 512-bit hash
of its term structure with names excluded; names live in a separate namespace
mapping name to hash. The codebase is a typed database managed by UCM, not
text files; text is rendered on demand. Unison 1.0 was announced November 25,
2025, declaring the language, distributed runtime, and workflow stable.

**Mechanism mapping.** This is the closest end-to-end validation of encodedID
identity plus names-as-projection. Rename is a pure metadata operation —
dependents reference the hash, nothing recompiles. The current update workflow
(patch mechanism is gone; verified against 2025 docs): `update` typechecks
dependents against a changed definition and auto-propagates, giving dependents
new hashes in a cascading rehash; when propagation cannot be automatic, UCM
creates a temporary branch, dumps affected definitions into the scratch file,
and `todo` tracks the remaining work. The "same structure, different intent"
problem forced a concession to nominality: structural types (identity by
structure hash) exist, but the *default* is `unique type` — identity by a GUID
minted at declaration time. Pure structural addressing was demoted to opt-in
because most domain types need minted identity.

**What Nomos should steal.** Proof at 1.0 scale that the identity model works:
no builds, perfect incremental caching, trivial rename, dependency-version
conflicts dissolve. The typed codebase-as-database with a manager tool is
exactly the engine-over-encoded-data shape. Most importantly the two hard-won
lessons: minted nominal identity (the GUID/encodedID) is mandatory, not
optional; and ID-chain churn — editing a leaf re-identifies every transitive
dependent — is severe enough that the entire update/todo machinery exists to
manage it. Nomos's encodedID chains will face the same cascade and must treat
the recomputation workflow as a designed surface, not an afterthought.

**Where it compromises.** Pretty-printing and comment/format fidelity — the
projection surface — is a long-standing sore spot; codebase serialization
format churn historically forced migrations. Names still mediate all human
interaction, so the name-to-hash mapping layer carries real UX weight.

**Verdict: high.** The existence proof for the identity model, and the best
map of where it hurts.

## 9. egg / egglog — e-graphs and equality saturation

**What it is.** egg (POPL 2021) is a Rust e-graph library for equality
saturation: rewrites apply non-destructively, equivalent terms share an
e-class, and a cost function extracts the best representative. egglog
(PLDI 2023) unifies Datalog with e-graphs: typed (sorted) functions, rules as
joins over the whole database plus equality assertion, fixpoint execution.
Both remain active (PLDI 2025 tutorial; egglog-python 13.1.0, March 2026;
DialEgg applying egglog to MLIR, 2025).

**Mechanism mapping.** Terms are typed and identity is structural, held by
integer e-class IDs under congruence closure — the closest existing
realization of "identity is integer IDs, never spellings" inside a rewriting
engine. Rewrites bind typed pattern variables and build typed replacement
terms positionally. egglog's Datalog half is genuine whole-payload analysis:
rules join across the entire database, so dataflow-style analyses and
rewriting coexist in one fixpoint.

**What Nomos should steal.** The identity discipline (integer class IDs,
congruence over typed terms) and the whole-database-rules idea. For
verification ambitions: equality saturation gives equivalence-by-construction
*relative to rule soundness* — every output is provably in the input's
equivalence class given the rules — and egglog can emit per-run proof
certificates, i.e. translation validation. Rule soundness itself must still be
proven separately (the Crocus/Arrival job), and eqsat cannot prove properties
outside the rule set.

**Where it compromises / sobering data.** egglog's surface language names
functions and sorts by string; cost functions and e-class analyses are
arbitrary Rust; extraction with sharing is NP-hard and done heuristically.
Production reality check: Cranelift's aegraph retrospective (April 2026)
reports its default e-graph mid-end does eager rewriting rather than
saturation, measures an average e-class size of 1.13, found that keeping
multiple equivalent forms bought about 0.1% runtime, and nets roughly 2%
speedup for 7–8% compile-time cost. In a production ruleset, the full eqsat
machinery barely pays.

**Verdict: medium.** Adopt the identity model and the certificate idea; treat
full equality saturation as optional machinery the production data says to
defer.

## 10. Attribute grammars — JastAdd and Silver

**What it is.** Declarative specification of analyses over typed trees:
synthesized and inherited attributes propagate results up and context down,
and the evaluator schedules computation. JastAdd built ExtendJ, a full
extensible Java compiler, this way; Silver (U. Minnesota) is the other main
living system.

**Mechanism mapping.** Reference attribute grammars are the key idea: an
attribute's value can be a *direct reference to another AST node*. A use
site's `decl()` attribute evaluates to the declaration node itself — name
resolution, type lookup, and call graphs become declaratively specified graphs
superimposed on the tree. This is encodedID-chain cross-declaration linking,
computed declaratively rather than authored by hand. Circular attributes are
declared fixpoints (bottom value, iterate to convergence) covering dataflow
and recursive inference. Evaluation is demand-driven with memoization: no
phase ordering, the dependency order emerges from what is asked. Silver's
forwarding lets an extension construct answer unknown analyses by forwarding
to its host-language translation.

**What Nomos should steal.** The shape of the analysis layer: whole-payload,
cross-declaration facts expressed as declared attributes that the engine
schedules, caches, and fixpoints — attribute-shaped, not visitor-shaped. This
is the declarative complement to the Salsa execution machinery: RAGs say what
the analyses *are*; queries say how they are computed incrementally.

**Where it compromises.** Debugging is hard because demand order is emergent;
performance tuning means fighting memo tables; and the sore point is
incrementality after tree edits — invalidating cached reference attributes is
genuinely hard, has been a research topic through the 2020s, and is still not
turnkey. Aspect-oriented weaving makes "where is this attribute defined"
nonlocal.

**Verdict: medium-high.** The declarative analog of whole-payload analysis;
adopt reference-valued attributes and demand/fixpoint evaluation, but design
invalidation in from day one rather than inheriting the field's unsolved
problem.

## 11. Brief notices

**Lean 4 metaprogramming.** Two-level design: `Syntax` (concrete, inert trees)
versus `Expr` (fully elaborated, typed kernel terms). Macros are Syntax to
Syntax, but elaborators consume Syntax and produce typed Expr under an
elaboration monad carrying expected-type information, with typed metavariables
as holes filled during elaboration. Parser, macros, elaborators, and tactics
are all user-extensible in Lean itself. The relevant pattern: a clean two-layer
architecture where the typed layer is the real program and surface syntax is
disposable — Nomos's text-as-projection stance, realized inside a proof
assistant.

**Zig comptime.** No separate metalanguage: the same language is partially
evaluated at compile time, and types are first-class comptime values, so
generics and reflection are just functions returning types. Limits: no new
syntax is ever possible, comptime-generated code has no inspectable artifact,
and errors surface only at instantiation. Relevant as proof that staging
within one typed language, with types as data, covers most metaprogramming
without any quoting apparatus — and as a warning about opaque generated code.

**Shen / KLambda.** The entire language — pattern-matching functions, macros,
embedded Prolog, parser generator — compiles to KLambda, a kernel of roughly
46 primitive forms; porting Shen means implementing KLambda. Its sequent-
calculus type system is optional per program region, with typed and untyped
code coexisting. The psyche's own reference for Logos: the lesson is extreme
kernelization — a tiny typed kernel all surface forms reduce to is a strong
architecture for "text is only a projection," though Shen itself is
spelling-based and dynamically bootstrapped.

**GHC rewrite rules.** RULES pragmas are typed equational rewrites (both sides
type-checked) applied by the optimizer during simplification — the basis of
fusion. Semantic correctness of each equation rests entirely on the
programmer, and applicability is fragile: phase-control numbers, inlining
interactions, and slight syntactic mismatches silently disable rules. The
relevant lesson is the cost of *implicit, unscheduled* rule application;
explicit strategies and plans are the antidote.

## Summary Table

| System | Core mechanism for Nomos | Fatal compromise under the lens | Relevance |
|---|---|---|---|
| MLIR / PDLL | Typed op universes; patterns as typed IR; legality-driven lowering | Interned name-string identity; PDLL stagnation via C++ escape hatch | High |
| JetBrains MPS | Templates as legal target ASTs; macros as typed positions; mapping labels; recursive reduction | Generation-time-only typing; dynamic name references; TextGen endpoint | High |
| Scala 3 / TTH / MetaOCaml | Typed holes checked at generator compile time; typed code patterns | Untyped/reflective escape hatches; scope extrusion from name identity | High |
| Racket syntax-parse | Syntax classes: declarative destructuring + errors | Spelling identity; hygiene is the workaround Nomos obsoletes | Medium-high |
| Stratego / Rascal / TXL | Rule/strategy separation; typed strategic visit | Untyped terms (Stratego); string-template emit (Rascal); text-centric (TXL) | Medium |
| Cranelift ISLE | Typed rules compiled to Rust; overlap check; SMT verification per rule | External constructors opaque to checking and verification | High |
| rustc queries / Salsa | Demand-driven whole-payload analysis; red-green cutoff; minted tracked IDs | DefPathHash: identity from name paths | High |
| Unison | Hash identity, names as metadata; typed codebase-database; update workflow | Minted GUIDs required anyway; churn cascade; projection fidelity pain | High |
| egg / egglog | Integer e-class identity; whole-database rules; proof certificates | String-named surface; heuristic extraction; eqsat barely pays in production | Medium |
| JastAdd / Silver | Reference attributes; demand + fixpoint evaluation | Incremental invalidation unsolved; emergent-order debugging | Medium-high |

## Synthesis

### Design lessons for the Nomos transformer engine, ranked

1. **Check transformers against both type universes at transformer-compile
   time.** The staging trio proves placeholders can be typed holes verified
   before any input exists; MPS proves skeletons can be authored as legal
   target-language fragments. A Nomos transformer must be rejected at load
   time if any placeholder's Logos type, vector-slot position, or Ethos
   binding is wrong — never at generation time. MPS's generation-time-only
   failures, and the thousands of tests mbeddr needed to compensate, are the
   cost of skipping this.

2. **Compile transformers to Rust; do not interpret them.** ISLE versus PDLL
   is a controlled experiment run by industry: typed rules compiled to native
   Rust decision trees (fast, debuggable, statically overlap-checked,
   verifiable per rule) thrived; patterns interpreted as bytecode (flexible
   but opaque, undebuggable, escape-hatch-ridden) stagnated. The
   transformer-compilation slice should follow ISLE's shape, including a
   whole-ruleset overlap/exhaustiveness check as a first-class engine feature.

3. **EncodedID identity dissolves hygiene — but three operations must be
   designed in its place.** Racket's scope sets and MetaOCaml's
   scope-extrusion checks are compensating machinery for spelling-based
   identity; with node-ID references, accidental capture is unrepresentable.
   What remains and must be explicit, typed API: fresh-binder minting
   (gensym-by-construction), intentional capture ("bind into the caller's
   namespace" as a deliberate operation), and forward references to
   not-yet-generated nodes (promise-IDs or a resolution step).

4. **Cross-link generated output by mapping labels, never by name.** MPS's
   (input node, label) → generated node mechanism is the production answer to
   "how does one generated declaration reference another": identity flows from
   input identity through the transformation, so links survive later stages.
   This composes with lesson 3 and is the concrete device that keeps the
   emit side string-free.

5. **Make whole-payload analysis demand-driven queries with minted identity.**
   Reference attribute grammars give the declarative shape (cross-declaration
   facts as attributes whose values are node references, fixpoints for
   circular analyses); Salsa gives the execution engine (dependency tracking,
   red-green early cutoff, durability tiers, tracked structs minting stable
   integer IDs for derived entities). Replace rustc's name-path-derived
   DefPathHash layer with encodedIDs — Nomos's identity model is strictly
   stronger here. Design cache invalidation on day one; it is the attribute-
   grammar field's unsolved problem and the expensive part of rust-analyzer's
   Salsa migration.

6. **Separate rules from scheduling, and make the schedule explicit and
   typed.** Stratego's strategies, MPS's generation plans, and MLIR's
   conversion targets all say the same thing from different directions; GHC's
   silently-inapplicable RULES and MLIR's greedy-driver nondeterminism show
   the failure mode. A transformation run should have an inspectable plan and
   a checkable termination condition — MLIR's "every construct legal for the
   target universe" legality model is the cleanest one to steal.

7. **Design the ID-churn workflow before it is needed.** Unison at 1.0 scale
   shows that with chained identity, editing a leaf re-identifies every
   transitive dependent, and that managing this cascade (update, todo,
   propagation, scratch surfaces) is a core workflow, not an edge case. Also
   from Unison: minted nominal identity is mandatory — pure structural
   identity was demoted to opt-in because domain types need declared intent.

8. **Treat every escape hatch as a verification hole — budget for
   completeness instead.** The recurring correctness leak across the whole
   survey: PDLL's native C++ constraints, ISLE's external constructors,
   MPS's dynamic references and TextGen, Scala's reflection API, Rascal's
   string templates. Verification coverage always equals rule-language
   coverage. Nomos's strict no-strings stance is only meaningful if the
   transformer language is expressive enough that authors never need a hatch;
   where a hatch is unavoidable, it must carry a machine-checkable
   specification (Crocus's move) or it silently caps the correctness
   ambition.

### Failure modes to design against

- **Emit-side collapse.** Typed matching with string emission (Rascal, untyped
  Template Haskell, MPS TextGen). The output side must construct typed Logos
  nodes positionally, with no textual endpoint inside the engine.
- **Spelling leakage into identity.** MLIR's interned op names, rustc's
  DefPathHash, MPS's dynamic references, egglog's string-named sorts. Any
  name-keyed lookup inside the engine reintroduces the entire class of
  problems hygiene exists to patch.
- **Declarative-language defection.** If the transformer language cannot
  express what authors need, they defect to the substrate and the language
  dies (PDLL, DRR). Expressiveness gaps are existential, not cosmetic.
- **Generation-time-only failure.** Errors surfacing only when a payload runs
  through the transformer (MPS, Zig instantiation errors) push correctness
  onto test suites.
- **Implicit scheduling.** Fixpoint-until-quiet drivers and phase-numbered
  rules produce nondeterminism and silent inapplicability (MLIR greedy
  driver, GHC RULES).
- **Debugging opacity.** Declarative engines fail socially when authors
  cannot see why a rule did or did not fire (PDL bytecode, attribute demand
  order, comptime). Inspectable intermediate stages (MPS transient models)
  and rule-firing traces are required engine features, not tooling luxuries.
- **Retrofitted incrementality.** Both the attribute-grammar literature and
  rust-analyzer's migration show invalidation and identity layers dominate
  cost when added late.

### Deep-study recommendations before the transformer-compilation slice

1. **Cranelift ISLE, including its verification stack (Crocus, Arrival) and
   its in-tree verifier.** The same slice Nomos is about to design — authored
   typed rules compiled to Rust — exists here in production with static
   overlap checking and per-rule SMT verification against authoritative
   semantics. Study the term/constructor/extractor typing, the match-trie
   compilation, priority semantics, and exactly where external constructors
   punch holes in the guarantees.

2. **The JetBrains MPS generator.** The only production system whose
   templates are typed target-language skeletons with typed placeholder
   macros, identity-based reference resolution via mapping labels, recursive
   reduction, and staged plans with inspectable intermediates. Study the
   macro taxonomy, the mapping-label/genContext resolution protocol, and the
   documented failure modes (generation-time typing gaps, migration burden)
   as the checklist of what to do at compile time instead.

3. **New Salsa (with rust-analyzer as the case study).** The execution
   architecture for whole-payload transformer dependencies: tracked
   functions and structs, minted stable IDs for derived entities, red-green
   early cutoff, durability, cancellation, fixpoints — plus a documented,
   recent, expensive migration showing which parts dominate performance.

MLIR's dialect-conversion framework (legality targets, type converters) is the
strong runner-up: worth a focused read when the multi-level Ethos-to-Logos
pipeline itself is designed, rather than for the transformer-compilation slice.
