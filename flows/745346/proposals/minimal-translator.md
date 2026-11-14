Presentation.{ «The minimal translator» Proposal }

# The minimal translator

Created by Fable 5.2. Sonnet gathered what the vision says and what the code holds.

### Proposal 1: A translator is its emission bodies and nothing else · psyche-belief › vision/translator/0.md

::: comment
Why: each Nexus rewrites the same translator plumbing by hand today.
:::

+ ---
+ description: The translator of a Nexus, what of it is shared, what is generated and what is written by hand, is being designed or judged.
+ dependencies: [vision:nexus:1, vision:ethos:0]
+ ---

+ # The minimal translator

+ A Nexus gains a translator by declaring its Emission in Ethos and writing one body for each emission: the words of that one call. Everything else a translator does is the same for every Nexus, and is written once.

```mermaid
+ flowchart TB
+     e["the Nexus's Ethos: Signal and Emission"] -- "generates" --> g["its types, and the dispatch of each emission to its body"]
+     l["the translator library"] -- "gives, written once" --> s["the sockets, the text, the caller, the serving"]
+     h["the implementer"] -- "writes by hand" --> b["one body for each emission: the words of the call"]
+     g -- "together are" --> t["the Nexus's translator"]
+     s -- "together are" --> t
+     b -- "together are" --> t
```

+ ## What is written once

+ The translator library holds everything that does not differ between Nexuses: making the sockets in the Nexus's place, reading one datom from a connection, taking the caller from the connection's credentials, turning the text into signal and the reply into text, and receiving each emission from the Nexus and returning its outcome. A translator names its Nexus's types and takes all of it as the default.

```ethos
+ Library                                           ; in the translator library; tentative in its names
+ [ signal:[ Signalizable Restorable ]              ; imports: what crosses to the Nexus
+   datom:[ Datomizable Composing ]                 ;   what is read from and written as text
+   nexus:[ Place ] ]                               ;   where a Nexus's sockets and memory are
+ [ Served.[ Stopped                                ; types: how serving ended
+            PlaceUnusable.Place ] ]
+ [ Emittable.{ []                                  ; traits: an emission; one external call
+               [ Outcome<Signalizable> ]           ;   what the translator observed of it
+               []
+               [ emit.[ Outcome ] ] }              ;   the body, written by hand: the words of the call
+   Translating.{ []                                ; a Nexus's translator, named by its types
+                 [ Input<[Composing Signalizable]>        ;   what the ordinary CLI may say
+                   Output<[Restorable Datomizable]>
+                   MetaInput<[Composing Signalizable]>    ;   what the meta CLI may say
+                   MetaOutput<[Restorable Datomizable]>
+                   Emission<[Restorable Emittable]> ]     ;   every emission of the Nexus, as one enum
+                 []
+                 [ serve:{ [ Place ] [ Served ] } ] } ]   ;   the whole translator; its body is the library's
+ []                                                ; associations
```

+ ## What is generated

+ The Emission root generates each emission's type, the enum of them all, and that enum's own emit, which hands each emission to its body. Ethos Zero knows the Emission root as it knows the other four.

```rust
+ // generated from the Source Nexus's Emission, with its types
+ pub enum Emission { Resolve(Resolve), Fetch(Fetch) }
+ impl Emittable for Emission {
+     type Outcome = Outcome;
+     fn emit(&self) -> Outcome {
+         match self {
+             Emission::Resolve(resolve) => resolve.emit(),
+             Emission::Fetch(fetch) => fetch.emit(),
+         }
+     }
+ }
```

+ ## What is written by hand

+ The bodies, and the naming of the types. This is the whole translator of the Source Nexus:

```rust
+ impl Emittable for Resolve {                      // which revision a reference stands at
+     type Outcome = Outcome;
+     fn emit(&self) -> Outcome { Git::remote_revision(&self.repository, &self.reference) }
+ }
+ impl Emittable for Fetch {                        // one revision's content, through Nix
+     type Outcome = Outcome;
+     fn emit(&self) -> Outcome { Nix::fetch(&self.repository, &self.revision) }
+ }
+ struct SourceTranslator;
+ impl Translating for SourceTranslator {
+     type Input = signal::Input;
+     type Output = signal::Output;
+     type MetaInput = meta_signal::Input;
+     type MetaOutput = meta_signal::Output;
+     type Emission = emission::Emission;
+ }
+ fn main() { SourceTranslator::serve(Place::from_argument()); }
```

+ ## One CLI for every Nexus

+ A CLI holds no type, so there is one CLI program. It is installed under each Nexus's name and its meta name, and the name it is called by says which configuration it reads and which translator socket it writes to.

```sh
+ source 'Read.{ psyche-belief «modules.datom» }'      # the one CLI, called by this name
+ source-meta 'Moved.psyche-belief'                   # the same program, the meta socket
```

+ ## Started with the Nexus

+ A translator is started with the same one datom as its Nexus, its place, and makes its sockets there: the text socket, the meta text socket and the emission socket. The Nexus connects to the emission socket and sends each emission on it.

## Questions

1. The Source Nexus is the first Nexus built this way, then the Belief Nexus. The translators that exist, Energy's among them, move to it as each is next touched. Is that the order?
2. Is the translator a module of its own, as here, or a section of the Nexus, version 1, vision?
