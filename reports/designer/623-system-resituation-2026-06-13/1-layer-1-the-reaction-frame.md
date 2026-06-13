# Layer 1 — the system we're touching: the reaction frame

Top-down, plain language. The goal is the *shape*, not the implementation.

## What we have

About fourteen small programs — `spirit`, `agent`, `router`, `terminal`, and so
on. Each is a **daemon**: it runs continuously, things arrive, it reacts, it
replies. And every one of them has the **same loop** at its heart:

> something **arrives** → the component **decides** what to do (write to its
> database, read from its database, perform some external effect, or reply) →
> that may produce the next arrival → loop.

## What the reaction frame is

The reaction frame is just the **types for that loop**:

- `Work` = "the kinds of things that can arrive / have happened" — a signal
  arrived, a database write finished, a database read finished, an effect
  finished.
- `Action` = "the choices the component can make in response" — reply, command a
  write, command a read, command an effect, or continue.

Arrive → choose an action → loop. **That shape is identical in all fourteen
components.** Only the specific payloads differ (spirit's signal type vs router's
signal type).

## The problem (the psyche's "design failure")

Each of the fourteen components carried its **own hand-written copy** of these
`Work` / `Action` types, even though the shape is the same everywhere. Fourteen
copies of one idea. That is the "re-authoring the universal frame per component"
the psyche flagged — recorded as Spirit `zjmc`: *the reaction-frame types are
workspace-universal and must be declared once and applied per component, never
hand-re-authored in each component schema.*

## What we're building

Declare that frame **once, with holes in it**, and let each component fill the
holes with its own payloads — exactly like `Vec<T>`:

> You define "list of T" once and write `Vec<i32>`, `Vec<String>`. You do **not**
> write a separate list type for every element type.

So: one generic `Work` / `Action`, **applied** per component —
`Work<spirit's-signal, spirit's-write, …>`.

## Why it took so much machinery

The components' types are **not hand-written — they're generated** from small
schema files (a component declares its shape in a schema; a generator turns it
into Rust). So "declare the frame once and apply it per component" meant the
**schema language itself had to learn generics**: how to write a type with holes,
and how to fill them. It couldn't before. That is what all the steps were —
teaching the schema language to say "here is a type with parameters" and "here is
that type with the parameters filled in," then making the generated Rust actually
be a generic that compiles. (Proven; reports 621–622.)

## Re-situating the thing that lost you: `Absent`

`Absent` is a **detail inside this, not the core**. Some components don't use all
the arrival-kinds — the `harness` only ever gets "a signal arrived," never "a
database read finished." So when such a component fills the holes, it needs
*something* to put in the holes it never uses. `Absent` is just the typed word
for "nothing real arrives on this leg, for me." The long explanation was about
*how perfectly* to express "this leg is unused" — a corner of the building, not
the building.

## The one-paragraph version

Fourteen daemons share one arrive-decide-loop; its types (`Work` / `Action`) were
copy-pasted fourteen times; we're collapsing them to a single generic frame
applied per component like `Vec<T>`; and because the types are generated from
schemas, the real work was teaching the schema generator to express generics.

## The next layers inward (when the psyche is ready)

- **Layer 2:** how a component actually *is* — what "schema → generated Rust"
  means, what a daemon / signal / sema / nexus really are, the machinery this
  frame lives in.
- **Layer 3:** the foundation — NOTA (the notation it's all written in), the
  structural-macro decode model, and how the psyche's recorded intent drives the
  whole pipeline.
