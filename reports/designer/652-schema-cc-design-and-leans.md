# 652 — schema-cc: the compiler-compiler design, the leans I took, the questions I answered

The psyche directed: *"create a schema-cc on a feature branch and you can throw even
more of the definition into data which generates the compiler"* — then stepped out
with *"go with your leans … keep [the questions] for the report with your explanations
on the leans you implemented."* This report is that: every design decision I made
autonomously, the alternative I rejected, and why; plus the questions I'd have asked,
with the answers I chose. Intent: Spirit `vpbx` (schema-cc exists; generate the
compiler from data), `549v` (the reference precedence is the generative source),
`v0n6` (route hand-parsing through typed nodes), `9rjq` (compiler is build-time;
binaries carry only rkyv contracts), `7c71` (a language is data). Created:
`/git/github.com/LiGoldragon/schema-cc` on bookmark `next/schema-cc`.

## What schema-cc is

The schema **compiler-compiler**: the compiler's own definition kept as typed data
that **generates** the compiler, bottoming out in the nota-next seed. Three tiers:

```
SEED        nota-next      block parser + the one derive   — frozen, context-free
DEFINITION  schema-cc      ReferenceGrammar, built-in heads, shape vocab, emission   — typed data
COMPILER    schema-next /  resolution, lowering, Rust emission                       — generated
            schema-rust-next
```

It targets the exact fragility the `651` analysis flagged: the parenthesis-reference
dispatch precedence is hand-written match-arm order, pinned only by tests, and the one
place that escaped "a language is data" — a human, an LLM, and the resolver can each
read it differently. schema-cc makes the precedence one declared artifact and
generates the resolver from it.

## The leans I implemented (and what I rejected)

| # | Decision | Chose | Rejected |
|---|---|---|---|
| 1 | Generate vs interpret | **Generate** the resolver Rust | A runtime grammar-interpreter |
| 2 | v0 scope | **`ReferenceGrammar` only, standalone** | Datafy everything at once |
| 3 | Type generality | **Reference-specific, shaped to generalize** | A fully-general meta-grammar now |
| 4 | One grammar vs per-context | **One precedence + a registry hook** | Per-context precedence grammars |
| 5 | DAG position | **Upstream of schema-next** | schema-cc depending on schema-next |
| 6 | Validation | **`ValidatedReferenceGrammar` typestate via `TryFrom`** | Validate-at-generate / no newtype |
| 7 | Lifecycle | **Build-time generator, never a runtime dep** | A shipped grammar + interpreter |

**1 — Generate, don't interpret.** The whole stack is `declared data → emitted Rust`;
nota-next's own `StructuralDerive` already emits decode arms in order from `#[shape]`
annotations. An interpreted `ReferenceGrammar` would be a *second*, inconsistent
mechanism, and would drag a grammar-walker toward the runtime — against `9rjq`.
Reference resolution runs only at schema-compile time, so the generated resolver is
pure compiler code that never ships. (This is the answer to the psyche's own question
"are you using it to generate the compiler code?" — yes.)

**2 — v0 is `ReferenceGrammar` only, standalone.** I prove the *pattern* (precedence
data → generated resolver + the validator) without touching schema-next. Rationale:
the riskiest unknown is "does declared precedence generate a correct, well-formed
resolver" — prove that cheaply first; re-wiring schema-next to *consume* the generated
resolver is a larger, destabilising step better done deliberately (and is operator
integration territory). Datafying the built-in head table, the shape vocabulary, and
the emission rules all at once would be a big unproven surface; I roadmap them instead.

**3 — Reference-specific first, but shaped to generalize.** `ReferenceGrammar` is an
ordered list of recognizers ending in a catch-all — which *is* the general shape of
"specificity-ordered dispatch." I did not pre-build a general `Grammar<Form>`: the
concrete case teaches the abstraction, and over-abstracting before one case works is
how meta-layers calcify wrong. The generalization falls out later if a second dispatch
wants it.

**4 — One precedence grammar + a registry hook.** The precedence *among form kinds*
(built-in → declared-macro → application) is universal; only the macro *set* varies by
context, and that variation is the registry (runtime state) reached through the
`DeclaredMacro` entry. So one declared precedence covers everything, and per-context
behavior is the registry, not a different grammar. I found no evidence a context needs
a *different precedence*; if one ever does, the grammar is already a value and can be
parameterized then.

**5 — schema-cc is upstream of schema-next.** Dependency order `nota-next → schema-cc
→ schema-next → schema-rust-next`. schema-cc must not depend on schema-next because it
*generates into* it; the reverse edge would be a cycle. schema-cc depends only on
nota-next (to decode the definition) + `quote`/`proc-macro2`/`prettyplease` (to emit).

**6 — Validation is a real typestate.** `ValidatedReferenceGrammar` (newtype via
`TryFrom<ReferenceGrammar>`) carries an invariant the borrow checker cannot express:
the generator may run *only* on a grammar whose catch-all is unique and last, with no
built-in/macro head collision. This is exactly nota-next's
`StructuralVariantSet::validate_no_silent_conflicts` — the conflict check the
context-free derive already has — **lifted to the context-aware declared grammar**.
It closes the silent-shadowing failure mode `651` flagged (register a macro named
`Vector` → today the built-in silently wins; here the validator rejects it).

**7 — Build-time only.** schema-cc generates compiler code and never links into a
runtime binary, reinforcing `9rjq`. "Generate not interpret" is what makes this true.

## The questions I would have asked — and my answers

- **The exact NOTA surface for the grammar.** I chose
  `(ReferenceGrammar (Builtin Vector 1) … DeclaredMacro Application)` — headed forms
  for built-ins (head + arity), bare keyword markers for the two catch-alls. The one
  awkward case is `(Bytes N)` whose "arity" is a fixed-bytes atom, not a type argument;
  I model it explicitly rather than forcing it into the type-arity slot. **Confirm the
  surface; it is cheap to change while it is one prototype.**
- **Should `ReferenceGrammar` itself eventually be a schema** (a self-describing
  meta-schema), or stay a Rust type that derives `StructuralMacroNode`? For v0 it is a
  Rust type with the derive (so it decodes NOTA, no hand-rolled parser). Making the
  grammar's *own* shape a schema is the deeper self-hosting fixpoint — worthwhile, but
  it is a separate question I deferred. **My lean: do the fixpoint later, once a second
  definition (the shape vocabulary) is also datafied and the meta-schema has two
  clients to justify it.**
- **What migrates next.** Roadmap below. **My lean on order: built-in head table →
  shape vocabulary → emission rules**, each as a separate slice with its own validator,
  because each is progressively more entangled with schema-rust-next.
- **When to re-wire schema-next to consume the generated resolver.** That is the step
  that makes this real rather than a proof. **My lean: do it as a deliberate
  operator-style integration after v0 is reviewed — generate the resolver, diff it
  against the current hand-written `from_parenthesis_objects`, prove semantic
  equivalence (the identity-hash test suite is the witness), then swap.**

## Bootstrap soundness (no cycle)

A `ReferenceGrammar` value is written in NOTA using only shapes the **seed** decodes
directly (headed forms + keyword atoms — no registry-aware resolution needed to parse
the grammar *itself*). So: seed decodes the grammar → grammar generates the
registry-aware resolver → resolver handles every user reference. The compiler
generates part of itself, but the part it needs to *read its own definition* is below
it in the seed. Standard self-hosting layering.

## Roadmap (after v0)

1. **v0 (this branch):** `ReferenceGrammar` decode + validate + generate the resolver,
   standalone, green. (Prototype outcome below.)
2. **Re-wire:** schema-next consumes the generated resolver; prove identity-hash
   equivalence to the hand-written dispatch; delete `from_parenthesis_objects`.
3. **Built-in head table as data:** the `ReferenceHead`/`classify` set becomes part of
   the grammar (closes the `classify`-drift failure mode — single source).
4. **Shape vocabulary as data:** the 7-shape recognizer set expressed in schema-cc.
5. **Emission rules as data:** the schema-rust-next lowering/emission templates.
6. **Meta-schema fixpoint:** express schema-cc's own definitions as a schema.

## Prototype outcome — green, the thesis proven

Branch `next/schema-cc`, prototype change `79ad0fc3` (8 files, 843 lines). **15 tests
pass** (grammar 4, validate 6, generate 5) and `clippy --all-targets -- -D warnings`
is clean — independently re-verified, not just agent-reported.

**The proof.** A `ReferenceGrammar` written in NOTA —
`(ReferenceGrammar (Builtin Vector 1) (Builtin Optional 1) (Builtin ScopeOf 1)
(Builtin Map 2) (Builtin Bytes Atom) DeclaredMacro Application)` — decodes through the
seed, validates, and **generates** this resolver (golden-pinned):

```rust
pub fn resolve(&self, block: &::nota_next::Block) -> Result<Resolution, ResolveError> {
    let head = block.root_object_at(0).and_then(::nota_next::Block::demote_to_string);
    let object_count = block.holds_root_objects();
    if head == Some("Vector")  && object_count == 2 { return Ok(Resolution::Builtin); }
    if head == Some("Optional") && object_count == 2 { return Ok(Resolution::Builtin); }
    if head == Some("ScopeOf")  && object_count == 2 { return Ok(Resolution::Builtin); }
    if head == Some("Map")     && object_count == 3 { return Ok(Resolution::Builtin); }
    if head == Some("Bytes")   && object_count == 2 { return Ok(Resolution::Builtin); }
    const RESERVED_BUILTIN_HEADS: &[&str] = &["Vector","Optional","ScopeOf","Map","Bytes"];
    if let Some(head) = head && RESERVED_BUILTIN_HEADS.contains(&head) {
        return Err(ResolveError::WrongBuiltinArity);   // reserved head, wrong arity — no fall-through
    }
    if Self::is_declared_macro(head) { return Ok(Resolution::DeclaredMacro); }
    Ok(Resolution::Application)                          // catch-all, last
}
```

The built-in arms are in the grammar's **declared order**, the reserved-head guard is
**derived from the built-in set** (closing the `classify`-drift failure mode — single
source), and the declared-macro→application tail is last. **Reorder the NOTA grammar
and the emitted arms reorder with it** — that is the whole point: the precedence is now
data, readable once, generated, not hidden in match-arm order.

**How it was built (verified against the discipline):**
- `nota-next` stayed on `main` — its enum shape vocabulary sufficed; no need for the
  `next/structural-forms` struct/named-field derive. Shapes: `ReferenceGrammar` →
  `#[shape(head = "ReferenceGrammar", body)]`; `Builtin` →
  `#[shape(head = "Builtin", arity = 3)]`; the two markers → `#[shape(keyword = "…")]`.
- `BuiltinHead`/`BuiltinArity` carry **hand-written `StructuralMacroNode` impls** (the
  legitimate manual trait path nota-next's own tests use for leaf newtypes a derive
  shape can't express — a bare integer atom is neither PascalCase nor headed).
  `BuiltinArity` is a typed sum `Atom | Count(ArgumentCount)`, so the `(Bytes Atom)`
  case is a first-class arm, never a sentinel number — the dimensional principle in
  miniature.
- Discipline holds: generate is `From<&ValidatedReferenceGrammar>`, validate is
  `TryFrom<ReferenceGrammar>`, even the per-arm emitters (`BuiltinFormEmit`,
  `ReservedHeadGuard`) are data-bearing nouns carrying what they emit — no free
  functions, no ZST holders; one `thiserror` `Error`; decode via the seed (no
  hand-rolled parser); tests in `tests/`.

**v0 stubs (intended, per the boundary):** the emitted resolver's `is_declared_macro`
is a `todo!()` registry hook and `Resolution`/`ResolveError` are placeholder enums; the
resolver is asserted as tokens (`syn::parse2` validity + substring-order + golden), not
compiled against schema-next's real types. No dependency on or change to schema-next.

**Two small findings:** (1) a `DeclaredMacroAfterApplication` validator variant was
dropped as unreachable — `ApplicationNotLast` already covers any marker trailing the
catch-all (a test documents it). (2) The harness-produced genesis had `target/` tracked
and no `.gitignore`; that was cleaned and `/target` ignored (genesis was local-only,
unpushed). The genesis `Cargo.toml` still declares `rkyv`, unused by this prototype —
left as-is.

**Status:** local on `next/schema-cc`, not pushed; GitHub-remote creation left for the
psyche/operator (a new public repo is an outward call). Next per the roadmap: re-wire
schema-next to consume the generated resolver, proven equivalent by the identity-hash
suite.
