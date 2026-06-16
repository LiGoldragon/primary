# 659/3 — The end-to-end goal and the concrete use case

## The original problem

The psyche's ask (`654`): *"review the improved nota/schema syntax and how it can represent
the generics/traits we wanted it to represent so it could generate the code we actually need
for the components, and avoid hand-wiring all of it with newtypes."* Two halves: the schema
must **represent** generics and traits, and from that representation the compiler must
**generate** the component code — eliminating hand-wiring.

The `654` review found: generics-of-*types* already emit true generic Rust, but generic
*impls* and *traits* don't generate at all — and a stack of hand-wiring exists precisely
because the schema couldn't express those shapes.

## The concrete use case — the reaction frame (`zjmc`)

`zjmc` (Principle, High): [the Signal/Nexus/SEMA reaction-frame types Work, Action, and the
canonical five-variant action set are workspace-universal and must be declared once and
applied/bound per component, never hand-re-authored in each component schema; re-authoring
universal types per component is a design failure].

Concretely: the universal **Work** (4-leg: SignalArrived / SemaWriteCompleted /
SemaReadCompleted / EffectCompleted) and **Action** (5-leg: ReplyToSignal / CommandSemaWrite
/ CommandSemaRead / CommandEffect / Continue) are declared **once** (the hand-written generic
in `triad-runtime/src/reaction.rs`, proven to compile + round-trip rkyv and NOTA over
multi-parameter generics, task #408), as the `hh3z` form `Work (| [Event WriteDone ReadDone
EffectDone] [(SignalArrived Event) …] |)`. Each component **binds** it in two import lines +
two application lines. That binding *generates* spirit's `NexusWork`/`NexusAction`
(`spirit/src/schema/nexus.rs:188,198`, expanded `Input`/`Output` at `:504,:514`) instead of
the ~2577-line hand-spelled `nexus.rs` re-authoring them per component.

## The verified prototype (`656`)

The expansion codegen works end-to-end, independently re-verified (designer worktrees
`reaction-expand`, schema-next `rtxlqtkptunw` + schema-rust-next `ulnvylmyypuw`, not pushed):

- The decisive call — **expansion**, not generic-alias: an applied root expands by positional
  binder→argument substitution into a concrete `RustEnum` with empty params, flowing through
  the existing constructor/`From`/accessor/wire emitters (suppression guards don't fire on
  empty params) — zero new machinery.
- Implemented: schema-next `RootApplication::expand_with` (promoted `FrameExpansion`),
  `Schema::expand_application_root` (+ `reaim_sibling_application` for the nested Continuation),
  `ResolvedImport` carrying params+variants (from the already-loaded-then-discarded module
  schema); schema-rust-next applied-roots branch → concrete `RustEnum`.
- Verified: regenerated fixture shows `pub enum Input { SignalArrived(SignalInput), … }` /
  `pub enum Output { …, Continue(Input) }` leg-for-leg with auto constructors + `From` (incl.
  `From<Input> for Output`), newtype wrapper flattened; `cargo test --test
  spirit_frame_application` 5/5; full suites green (18 + 88 binaries), no regression.
- Caveat for landing: `ResolvedImport` gaining `Vec<EnumVariant>` needed `#[rkyv(omit_bounds)]`
  + bound attrs and shifted content hashes (expected, no-byte-stability).

## The hand-wiring inventory to eliminate (`654`, cross-checked in source)

Ranked by the capability that removes each:

1. **`plane.rs` cross-plane `From` bridges** — 8 impls (6 over `OriginRoute`, 2 over
   `Engine*Failure`), existing only because the same logical types are **triplicated**.
2. **The triplicated types** — `OriginRoute` declared 3× (`engine.rs:26`, `sema.rs:1388`,
   `nexus.rs:2423`), `EngineStart/StopFailure` 2× each. Declare-once-universal removes both
   the dupes and the bridges (frame-application + universal-type emit; proven leg-for-leg,
   only emitter wiring missing).
3. **`NexusWork`/`NexusAction` re-authored per component** + the redundant per-leg newtype
   wrappers — removed by frame expansion (done in the `656` prototype).
4. **schema-cc's own newtypes** — the irony the psyche pointed at: the compiler-of-the-compiler
   is itself hand-wired. `BuiltinHead`/`BuiltinArity` carry ~112 lines of hand-written
   `StructuralMacroNode` impls because the derive's 7-shape vocabulary lacks leaf shapes and
   supports enums only. Removed by leaf shapes in the derive.
5. **Suppressed parameterized-decl `From`/constructor/accessor impls**
   (`schema-rust-next lib.rs:5099-5106,5149-5156`) — suppressed because the emitter can't
   synthesize an `impl<P..> Type<P..>` header. Removed by generic impl-header threading (the
   genuinely-NEW codegen behind "bounds").
6. **`RuntimeRoleTraitImpl` hardcoded trait paths + push-lists, the `NexusEngineTraitTokens`
   template, the verbatim `AcceptPrevious` impl string, 12× hand `impl Deref`** — removed by
   the single-payload `Deref` directive (lowest-cost first proof), the `ImplDeclaration`
   section + marker impls (honest cost: the role→trait binding is currently structural
   inference in `nexus_runner_shape`, must be made explicit not merely relocated), and trait
   declarations as data.

**The boundary that is NOT debt** (`5hjv`): handwritten Rust implements *behavior* on
generated nouns — the Nexus decision plane, store, guardian, signal-query matchers stay
hand-written. The candidate Principle caps generated bodies at marker + a fixed named
mechanical family; arbitrary expression bodies are never data.

## The e2e goal chain

1. **Represent** every construct a component needs — struct / enum / newtype (positional
   `{}`/`[]`, `own9`), generics (`(| … |)`, `hh3z`), traits/impls (`{| … |}`, `bpyu`) — so the
   two reserved pipe points carry exactly the two capabilities `654` found missing.
2. **Make kind explicit** on the declaration (`3742`), binders scoping the body structurally;
   use sites stay bare and resolve by name as built-ins do — a concrete owned interface, not a
   persisted generic alias (`657`).
3. **Generate** the component Rust from the declared data (`4itr`/`7c71`/`vpbx`): declare
   universal frames once, bind per component (`zjmc`); expansion gives each component a
   concrete owned interface with normal impls for zero new machinery (`656`/`657`/`658`),
   build-time only (`9rjq`).
4. **Collapse** the triplication and delete the hand-wired bridges/templates — a two-line
   binding for ~4,200 lines of hand-spelled Rust — keeping only genuine behavior hand-written
   on generated nouns (`5hjv`).
