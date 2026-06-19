# 703-9 — schema-next single lowering engine: the context

The walk-through behind the `schema-next` `main` landing (`4b7e830a`). The
psyche asked to "explain with context," then "implement it … on main." This
file is the explanation; the landing is recorded in `8-decisions-and-implementation.md`.

## The two lowering "engines"

schema-next had two paths from a `.schema` document to a typed `Schema`:

- **The typed-source path** (`source.rs`, `SchemaSource::to_schema`) — parses
  the document structurally and lowers it directly. **This is the only path
  production uses** (`module.rs:199`).
- **The macro/document path** (`engine.rs`, `lower_source` /
  `lower_document_with_resolver`) — ran the **MacroRegistry** first (expanding
  registered macros), then lowered. Reachable only from tests in production
  terms.

## Why collapsing them was the goal (the `schema-1` bug)

The two were hand-mirrored — the code said they "must stay in lockstep" — and
had already drifted: the macro path had no nested-namespace case (it lowered a
colon-keyed brace as a *struct*) and rejected trailing relations, while the
source path handled both. Because production only ran the source path, the macro
path was a **test-only shadow carrying a latent divergence**: the same schema
text could mean two different things by entry point. The collapse makes the
macro/document entry point *delegate* to the source path (reparse into a
`SchemaSource`, lower once) — one semantics, the drift cannot recur.

## What the collapse surfaced (and why 3 tests went red)

The two paths were **not** pure duplicates. The macro/document path carried the
**macro-dispatch layer** — the schema-next MacroRegistry that expands registered
macros: both the builtin structural macros (`RootInput`/`RootOutput`/
`RootNamespace`/`KeyValueDeclaration`) and user-declared `TypeReference` macros
like `(SchemaMacro Bag TypeReference (Bag $Type) (Reference (Vector $Type)))`
that expand `(Bag Topic)` → `Vector<Topic>` with `$`-capture substitution. The
source path resolves types via `SourceTypeResolver`, which **never consults the
registry**. So collapsing onto the source path silently dropped expansion:
`(Bag Topic)` stayed an unexpanded `Application`, the capture-binding didn't
fire, and 3 `design_examples` tests went red — they guard the user-extensible
macro capability, not incidental plumbing.

## Why it was not a regression to paper over

Macro dispatch is governed intent, and high-certainty:

> Per Spirit `c2dc` (Decision High): [the NOTA decoder is extended by a registry
> of registered macros dispatched as an ordered list, first match wins, with
> conflict detection at registry-construction time; the captured blocks are
> interpreted by a consumer, Schema being one].
>
> Per Spirit `5mxn`: [schema macros are plain NOTA records dispatched by
> position+shape in schema-next MacroRegistry].

The builtin structural macros are largely redundant with the source path's
direct parsing (so normal schemas still lower), but the **user macros are a
genuine capability only the registry provides**.

## The resolution — intent-aligned

`c2dc` is explicit about the shape: the registry **expands**, a **consumer
interprets**. Expansion was never meant to be a rival *lowering engine* — it is
a **front-end pass** that feeds the single lowering path. So the correct
architecture is:

```mermaid
flowchart LR
    P["parse<br/>nota-next Document::parse"] --> X["MACRO-REGISTRY<br/>pre-expansion pass<br/>src/expansion.rs (NEW)"]
    X --> F["SchemaSource::from_document<br/>(rkyv archive, already expanded)"]
    F --> L["source.to_schema<br/>(the SOLE lowering semantics)"]
    classDef new fill:#1f3a1f,stroke:#50a050,color:#d0f0d0
    class X new
```

The collapse did the second arrow right and just omitted the expansion pass. The
fix re-homed dispatch as a pre-pass over the parsed `Document` **before**
`SchemaSource::from_document` builds the rkyv archive — so the archive carries
only built-in heads and the source path stays the sole lowering semantics. The
pass (`MacroExpansionPass`): records every structural root-macro firing and
`$`-capture binding into `MacroContext` (so the structural macros register as
fired), and rewrites user `TypeReference` invocations through the registered
macro's own capture/substitution before re-emitting NOTA and re-parsing. The
alternative — threading `&MacroRegistry` through `SourceTypeResolver` at resolve
time — changes the lowering core signature and fights the rkyv archive shape, so
it was not chosen.

## Outcome

Full suite green (0 failures, independently verified, no fake-green; the 3
`design_examples` macro tests and both-paths parity tests pass). Squashed to one
green commit (`4b7e830a`) and landed on schema-next `main` per psyche direction.
The single-lowering-engine `schema-1` divergence is closed **and** macro
dispatch (`c2dc`/`5mxn`) is preserved as the front-end pass it was always meant
to be.
