# Prototyping Rust in Clojure

## Page 1 · What "the object-oriented part" meant

This flow (Psyche Medium e51411) wrote it to you on 2026-09-25 at 16:12 UTC, reporting an audit of the Clojure Hacky Messenger:

> 1. **The object-oriented part is only scaffolding.** The protocols and records exist, but nothing is built from them or goes through them. The code doesn't use them.

It wasn't "not implemented". It was "declared but unused". Here is what it referred to:

- **Your requirement:** the Clojure HM should be an object-oriented version of the Rust approach, with a type that owns the data and methods that belong to it.
- **First audit:** there were only free functions, with no `defprotocol` or `defrecord` anywhere.
- **Re-audit at `514f297f`:** four protocols appeared (`Registry`, `HerdrTransport`, `Ledger`, `Clock`), but nothing created a record from them or called through them. `send!` still called the plain functions directly. That was the "scaffolding".

**Is it still true? No.** On branch `clojure` at `be6c14a` (read today by this subflow, witnessed):

- Each protocol has a real record: `DatalevinRegistry`, `ShellHerdr`, `DatalevinLedger` and `SystemClock`.
- Sending, registering and moving panes all go through them: `(load-route (registry) flow)`, `(prompt!* (transport) route …)`, `(record-attempt! … attempt)`.

The audit at `246b963a` swapped in a fake `Registry` and saw `send!` use the fake's route. That proves real dispatch *(relayed from the audit report, not rerun here)*.

## Page 2 · A Rust struct and trait, as a Clojure record and protocol

In Rust, a **trait** names what something can do, and a **struct** is the thing that does it. Clojure has the same pair: a **protocol** names the methods, and a **record** is a map with a name that implements them.

The Rust below is how HM's `Registry` would read in Rust. It is a sketch, not code that exists.

```rust
pub trait Registry {
    fn load_route(&self, flow: &FlowId) -> Option<RouteBinding>;
    fn save_route(&self, flow: &FlowId, route: RouteBinding) -> Result<(), Error>;
}

pub struct DatalevinRegistry { state_root: PathBuf }

impl Registry for DatalevinRegistry {
    fn load_route(&self, flow: &FlowId) -> Option<RouteBinding> { store::route_for(&self.state_root, flow) }
    fn save_route(&self, flow: &FlowId, route: RouteBinding) -> Result<(), Error> { store::put_route(&self.state_root, flow, route) }
}
```

The real Clojure, from `core.clj` on `clojure`:

```clojure
(defprotocol Registry (load-route [this flow]) (save-route! [this flow route]))

(defrecord DatalevinRegistry [state-root]
  Registry
  (load-route [_ flow] (store/route-for state-root (flow-id! flow)))
  (save-route! [_ flow route] (store/put-route! state-root (flow-id! flow) (route-binding! route))))
```

The other three protocols follow the same pattern:

- `HerdrTransport`, with seven methods (get a pane, send keys, prompt, and so on), implemented by `ShellHerdr`, which calls the `herdr` command.
- `Ledger` (`record-attempt!`, `record-pending!`), implemented by `DatalevinLedger`.
- `Clock` (`current-time`), implemented by `SystemClock`.

**Where the types went.** A Clojure protocol doesn't say what `flow` or `route` are. That job moves to Malli schemas, which are checked when the program runs, not when it compiles:

```clojure
(def FlowId [:and [:string {:min 1 :max 96}] [:re #"^[A-Za-z0-9][A-Za-z0-9_-]*$"]])
(def RouteBinding [:map {:closed true} [:session :string] [:name :string] [:pane_id :string]
                   [:terminal_id :string] [:agent :string] [:native_thread {:optional true} NativeThread] …])
```

`flow-id!` and `route-binding!` run those checks at the door of each method. In Rust, the compiler does that job.

**How tests swap parts.** Rust would take the registry as a generic parameter. HM uses a dynamic variable instead: `(defn registry [] (or *registry* (->DatalevinRegistry (root))))`. A test binds `*registry*` to a fake and the real code runs against it.

## Page 3 · EDN standing in for Datom

Datom carries no field names: the type knows them, and the text holds only the values, in order. EDN carries its names on every value. HM's Clojure prints this datom when a send is held:

```
Held.{ e51411 PaneMissing attempt-3f2a9c1b-7d4 }
```

The same fact as EDN, written as the Malli `DeliveryAttempt` schema requires it:

```clojure
{:id "3f2a9c1b-7d4e-…" :at "2026-09-25T16:12:58Z" :flow "e51411" :reason :PaneMissing :grade :Held}
```

HM's own pane envelope is EDN with a tag: `#msg ["e51411" "hello"]`, checked by the `PaneMessage` schema `[:tuple FlowId MessageBody]`.

**Why EDN works for a prototype:**

- Clojure reads it and prints it with no library.
- Malli checks it.
- Datalevin stores it.

**Why it's only a stand-in:**

- The names in the data are the same field names the type already has, so they're repeated.
- A map can have any keys, while a datom struct has fixed positions.
- A Datom string in guillemets has no direct twin in EDN, which uses quotes.

## Page 4 · The workflow you described

1. **Prototype in Clojure.** Each Rust trait becomes a protocol, each struct a record, and each type a Malli schema. EDN is the data. Babashka runs it straight away, with no compile step, and the REPL lets you poke at a live record.
2. **Freeze the shape.** Once it works, the protocols and schemas are the design, and the function bodies are just one way to fill it in.
3. **Rewrite in Ethos and Rust.** The Malli schemas become Ethos types. Ethos-zero generates the Rust structs and enums. The protocols become Ethos kinds, turned into Rust traits. The bodies are then rewritten by hand in Rust.

A Datom line checked by the Rust program can then be compared against the EDN one checked by Malli, as a test that both mean the same thing.

## Page 5 · What carries over, and what does not

**Carries over almost mechanically:**

- A closed Malli map `[:map {:closed true} …]` becomes an Ethos struct `Name.{ … }`, and `{:optional true}` becomes `Option<…>`.
- A fixed set of keywords (HM's `delivery-grades`: `:Transported :Presented :Held …`) becomes an Ethos enum `Grade.[ Transported Presented … ]`.
- `[:vector X]` becomes `Vector<X>`, and `:string`, `:int` and `:boolean` become the Ethos intrinsics.
- A protocol with its methods becomes a kind with its capabilities. The name changes, because Ethos names kinds as qualifiers: `Registry` would become something like `Routable` *(naming is a proposal, not decided)*.

**Needs a decision:**

- **Field names.** Ethos names a field after its type. `RouteBinding` has five fields that are all `:string` (`:session`, `:name`, `:pane_id`, `:terminal_id`, `:agent`), so each needs its own type first (`Session.String`, `PaneId.String`, and so on). Malli doesn't force this, so the prototype should do it early.
- **Value rules.** Malli checks `:min`, `:max` and patterns like the one in `FlowId`. Ethos has no place for these today, so they become hand-written checks in Rust.

**Doesn't carry over:**

- **Ownership and borrowing** (`&self` or `&mut self`, who owns the route). Clojure records never change in place, so the prototype says nothing about this.
- **The function bodies.** Rust and Clojure have different error styles: Clojure throws `ex-info`, while Rust returns `Result`.
- **The Babashka and Datalevin plumbing.**

**A warning from the real code:** HM already keeps two copies of its schemas. `core.clj` has `RouteBinding`, where `:state` is optional, and `typed_store.clj` has `Route`, where `:state` is required. If the schemas are the source for the rewrite, there should be one copy.

## Page 6 · What you said

> I don't know what you meant by "object-oriented part is not implemented." I would like to know maybe a bit about that. You can make a book explaining what you mean. You can show me some example code of what you were thinking about how to emulate the traits and [structs] that we're doing in [Clojure]. You could kind of emulate the kind of code that you would write in Rust and it's sort of faster to make one-off prototypes. Then you can rewrite them in Ethos and in Rust from the [Malli] and the pseudo traits that you wrote in [Clojure].

-- living, 2026-09-25, to Psyche Medium e51411 (speech to text; the bracketed words were restored by e51411).

The sentence you asked about is on page 1. Its exact wording was "only scaffolding", not "not implemented".

## Page 7 · Proposals

1. ☐ Record the workflow as a rule: a one-off prototype is written in Clojure, with each Rust trait as a protocol, each struct as a record, and each type as a Malli schema. The rewrite starts from those schemas and protocols.
2. ☐ Merge HM's two schema sets (`core.clj` and `typed_store.clj`) into one, so there's a single source for the rewrite.
3. ☐ In prototypes, give every field its own named schema (`PaneId`, `Session`) instead of a bare `:string`, so the move to Ethos is mechanical.
4. ☐ Write a small tool that turns closed Malli maps and keyword sets into an Ethos file, and try it on HM's schemas.
5. ☐ Give `Ledger` the same kind of lookup `Registry` has (one `ledger` function), instead of building `DatalevinLedger` separately at each call site.
