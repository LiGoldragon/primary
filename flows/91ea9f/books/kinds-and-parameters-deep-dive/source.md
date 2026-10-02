`Presentation.{ «Kinds and parameters, the deep dive» }`

<!-- Revised for publication on the coordinator's two binding changes: the Profile/Profiled examples are dropped in favour of Fillable, Processable and Streamable; every point is framed through today's start of Mind Astra. Original source: source-original.md. -->

## 0. Today, as the system

Today Opus asked Flow to start Mind Astra. Follow that one event and every kind in this book shows up doing a job.

1. The voice «Mind Astra» bears **Launchable**. Flow's Process calls `start!` on it. A pane opens, Codex launches, the first turn is sent, and the result is the flow dea0ba.
2. A harness hook reports `TurnFinished`. The flow dea0ba bears **Reportable**.
3. The messenger asks `Resolve.«Mind Astra»`. The name bears **Resolvable** and answers with the binding.
4. The messenger asks `Observe.«Mind Astra»`. The name bears **Observable** and hands back a stream. That stream is a **Streamable** whose Item is Binding. The messenger's route list is another Streamable, whose Item is a route. Same kind, two Items: that is what a parameter is, in the running system.
5. When the successor binds, Current changes: that is Memorable's `change!`.

At every step one thing calls and another thing bears the kind. The caller never becomes the bearer.

Where we talk past each other is the word *parameter*. In Rust it names three different things that look alike on the page; in ethos you have one word, kind, that must cover them. This book lays the two vocabularies side by side, shows what the compiler does with each, and then shows the one mistake I made and the one rule that prevents it.

## 1. The vocabulary, side by side

| Your word | Rust's word | What it is |
|---|---|---|
| kind | trait | a named set of capabilities a thing can have |
| capability | trait method | one verb of the kind |
| the thing that bears the kind | `Self` | the type the kind is implemented on |
| interaction | `impl Kind for Type` | the declaration that a type bears a kind |
| parameter of a kind | generic parameter *or* associated type | a slot in the kind, filled with a type later |
| constraint | trait bound (`T: Kind`) | "whatever fills this slot must bear that kind" |
| superkind | supertrait | a kind every bearer must also bear |
| `.` `!` `:` | `&self` `&mut self` no receiver | who the capability acts on |

Two of these are the whole disagreement: *Self* and *parameter*.

## 2. What the compiler does with Self

A trait is a contract with a hole in it: `Self`. Writing the contract names no type; implementing it fills the hole.

```ethos
Launchable.[ start![ Result<Flow StartRefused> ] ]
```
```rust
trait Launchable {                         // Self is the hole
    fn start(&mut self) -> Result<Flow, StartRefused>;
}
impl Launchable for Voice { … }            // the hole is filled with Voice
```

`start` takes nothing but the voice: a voice already is what it needs to start. What a voice needs beyond itself, if anything, is yours to answer.

Then every call `voice.start()` is resolved at compile time: the compiler knows the type is `Voice`, finds `impl Launchable for Voice`, and emits a direct call. No table, no lookup at run time. This is monomorphization: one concrete function per concrete type. (The other route, `dyn Launchable`, builds a small table of function pointers and looks up at run time; we never need it here.)

The point for the model: **the capability belongs to the bearer.** "The voice is launchable" is exactly `impl Launchable for Voice`, and `start` acts on *that voice* through `self`. My error wrote `impl Launchable for Process` and passed the voice as an argument — legal, but it says the Process is the launchable thing. The compiler accepted it because the compiler accepts any filling of the hole; only the model can be wrong.

## 3. What "parameter" means, three ways

The story already showed all three. When a capability needs a type beyond Self, there are three places that type can come from. They look alike and mean different things. Each has a name among your own kinds.

**A. Fillable: the kind fixes the type.**

```ethos
Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] }
           create:[ Self ] ]
```
```rust
trait Fillable {
    fn push(&mut self, input: String) -> Result<i64, SinkError>;
    fn create() -> Self where Self: Sized;
}
```

Every filler takes exactly `String`. Nobody chooses; the type is written into the kind. This is what you called "too specific."

**B. Processable: each use fills the slots.**

```ethos
Processable<[Clonable Sendable] Serializable>.[]
```
```rust
trait Processable<A: Clone + Send, B: Serialize> {}
```

`A` and `B` are slots in the head. Wherever `Processable<…>` is named, in an impl or a bound, they are filled: A with any type that bears Clonable and Sendable, B with any type that bears Serializable. The compiler makes one copy per distinct filling. This is your 1 August line: "T would be a trait."

**C. Streamable: the bearer chooses, once.**

```ethos
Streamable.{ [ Fillable ]
             [ Item<Serializable> ]
             [ CAPACITY.Integer ]
             [ next![ Option<Item> ] ] }
```
```rust
trait Streamable: Fillable {
    type Item: Serialize;
    const CAPACITY: i64;
    fn next(&mut self) -> Option<Self::Item>;
}
impl Streamable for BindingStream { type Item = Binding; … }
impl Streamable for RouteList     { type Item = Route;   … }
```

Each stream says once, when it takes the kind on, what its Item is. The stream that Observe handed back says Binding; the messenger's route list says Route. Whoever calls `next!` does not choose; they get what the stream declared. The compiler resolves `Self::Item` the moment it knows `Self`. (The two type names are illustrative.)

**How to tell them apart in one sentence each.** A: the kind fixes the type. B: each use fills the slots. C: the bearer picks the type, per implementation. B and C are both "a kind as input" in your sense: the capability never names a concrete type, only a slot constrained by a kind.

**Which one when.** When the type is part of *what the bearer is*, like a stream's Item, C: the bearer owns it. When it varies *per use* and the bearer does not care which, B: the user owns it. A is a smell: it means a kind not yet named.

## 4. The one rule, and what the generator must change

The rule, in your terms: *a capability speaks only in Self, the kind's own parameters, and other kinds; a concrete type in an input is a kind not yet named.*

What it changes in ethos-zero: today a kind written in an input position is rejected with a role error, and inputs must be concrete types. Under the rule, a kind name in an input position is accepted and means: the matching parameter in the head's angle brackets (form B), or the matching associated type in the body (form C), and a bare concrete type there is flagged. The generated Rust is exactly the B and C above; nothing new is needed from the compiler.

Written vertically, hanging, as you said — the closer ends the last line:

```ethos
Operation
[ flow:[ Name Flow StartRefused Event Reported Binding ] ]
[ Launchable.[ start![ Result<Flow StartRefused> ]
               succeed![ Succeeding ] ]
  Reportable.[ report!{ [ Event ] [ Reported ] } ]
  Resolvable.[ resolve.[ Option<Binding> ] ]
  Observable.[ observe![ Subscription ] ] ]
[ Name.[ Launchable Resolvable Observable ]
  Flow.[ Reportable ] ]
```

`Reportable` still takes `Event`, a concrete type. Under the rule that is the smell: either Event becomes an associated type the flow chooses (`Event<Eventful>`), or `report!` takes `Eventful` and any event may be reported. I have left it as the worked example of the choice you make in point 3.

## Rulings
1. The rule in point 4, as the knowledge line on kinds.
2. The generator change: kind names in inputs resolve to parameters; concrete types there are flagged.
3. For `Reportable`: bearer-chosen event (C) or caller-chosen (B)?
4. The hanging layout shown here — open on the line, items down the page under the first, closers on the last content line — as the ethos print form.
