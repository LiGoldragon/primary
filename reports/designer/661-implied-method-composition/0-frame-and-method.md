# 661/0 — Frame and method: implied-method composition as the code-is-data body model

## The question the psyche asked

> *"Are there a bunch of patterns that are identifiable as things that we write a lot
> that are easily deductible from the schema data? … standard patterns that we can
> standardize and have implemented by default. Then we can use these as building blocks
> to create other methods that reference these methods inside our data language … as long
> as these methods only reference to these basic built-in sort of implied methods that are
> already producible by virtue being an object in our system, you can build upon by
> composing them … addressed by their object type. So let's build up on that and fully use
> the spec we made with this schema language extension."*

The insight: each schema shape *implies* a standard method vocabulary derivable from the
shape alone, and a code-is-data method body can be built by **composing calls to those
implied primitives, addressed by object type**. The generatable-body set is then the
**closure under composition** over the implied vocabulary — not a fixed list. This resolves
the open piece `d3r2` had flagged ("the named mechanical-body family beyond
payload-projection"), and was Clarified into `d3r2` before this work began.

## Method

A background workflow of 13 agents, four phases, grounded in real code throughout:

| Phase | Agents | What |
|---|---|---|
| Survey | 5 catalog + 2 census | Enumerate the implied primitives per shape (struct/enum/newtype/expanded-frame/codec), grounded in what the emitter *already* produces; and census the *real* component code (spirit, triad-runtime, signal-spirit) for how much hand-wiring is composition-of-primitives vs genuine business logic. |
| Design | 1 | The `Expression` extension (the composition node), the closure rule + resolution, the boundary argument. |
| Verify | 4 skeptics | Each tries to **refute** a core claim: not-an-expression-compiler, deterministic resolution, meaningful deletion, correctness/termination. Default-refuted-if-uncertain. |
| Prototype | 1 builder | Extend the interpreter, generate one real composed method, prove it green; assert-reject out-of-scope with a typed error. |

The adversarial phase is the load-bearing part of the method: it caught a real over-claim in
the design (see `4`) and pinned exactly where the closure holds versus leaks. The thesis
**survives** — but in a sharper, more honest form than the design first proposed.

## The files in this meta-report

- `1-primitive-catalog.md` — the implied-primitive vocabulary per shape, and the
  ground-truth finding about what the emitter actually emits today.
- `2-deletability-census.md` — the numbers: how much real hand-wiring is composition (→ data)
  vs business logic (→ hand-written), with the honest caveats.
- `3-composition-design.md` — the `Expression` extension, the closure rule, and the central
  refinement the adversaries forced: the **two vocabularies**.
- `4-prototype-and-adversarial-verification.md` — the green prototype (byte-identical
  generated Rust + a firing typed boundary) and the four refutation verdicts.
- `5-synthesis.md` — the through-line: what is proven, what is refined, the landing slices,
  and the line that stays hand-written.

## One-line verdict

The thesis is real and proven green on real code — composing shape-implied primitives deletes
a recurring, copy-pasted tax that scales with component count — **but** the clean closure is
the *pure-schema-primitive* fragment; the std-method "leaf" vocabulary it also needs is a
small curated allowlist with an arbitrary boundary, not a structural closure, and must be
presented as such.
