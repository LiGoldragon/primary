Presentation.{ «Ethos, written from the type» Proposal }

# Ethos, written from the type

Created by Fable 5.2; a Sonnet reader gathered the belief lines and the state of the code.

### Proposal 1: Ethos is read and written · psyche-belief › vision/ethos.md

::: comment
Today four programs keep their ethos file as stored text and print it for help; ethos-zero reads Ethos into typed values and prints those back, but no Rust type can say what its own declaration is. This proposal adds that one capability and makes help the type's own answer. The names Describable, Protosizable and the chain are tentative.

The Ethos; Library is Ethos describing itself, as the Spacing section holds it:

The Rust generated from it, and the chain that prints a specification:
:::

::: shown
psyche-belief › vision/ethos.md
A datom object's basic CLI help emits the Ethos that describes its
anatomy. The wanted mechanism extends this: point at any object —
CLI now, Mentci later — and its Ethos prints, self-describing and
self-evident. The schema syntax serves two audiences: it trains
agents to use things properly, and it shows where the design is
lacking.
:::

+ Ethos is read and written by one walk in two directions: an ethos file read is a Library value, and a Library value prints as that file. The value is the specification; the text is one projection of it, and the datom of the same value is another.

+ Every declared type yields its own declaration. Ethos Zero emits Describable with the type, as it emits the datom traits and under the same feature, so it is compiled in only where text is spoken. Help is a type asked for its Library, and the Library printed; a program stores no ethos text.

```ethos
+ Library
+ [ :ethos:Library                                ; imports: the specification as a value
+   :protos:[ Protos Protosizable Textualizable ] ]
+ []                                              ; types
+ [ Describable.[ describe:[ Library ] ] ]        ; traits: no self; the type answers, with every type it names
+ [ Library.[ Protosizable ] ]                    ; associations: a Library becomes protos, in the ethos print
```

```rust
+ pub trait Describable { fn describe() -> Library; }
+ impl Describable for Lock {                      // generated with the type
+     fn describe() -> Library { /* Lock's declaration, then LockId's and LockName's */ }
+ }
+ let text = Lock::describe().protosize().textualize();   // type, Library, protos, text: each step its own type
```

```mermaid
+ flowchart TB
+     t["a type"] -- "describes itself as" --> l["a Library value"]
+     f["an ethos file"] -- "is read into" --> l
+     l -- "prints as" --> f
+     l -- "travels as" --> s["signal"]
```

### Proposal 2: The translator answers for its types · psyche-belief › vision/nexus-v1.md

::: comment
The translator is already the one place compiled with the text side of the Signal's types, so it answers a request for a specification itself and the Nexus stays lean. A CLI given no datom prints the whole; Describe narrows it to one name. Describe lives on the text side only and never reaches the wire. Tentative: whether Describe is wanted at all beside the whole print.
:::

::: shown
psyche-belief › vision/nexus-v1.md
The Nexus decodes signal and nothing else. The translator is the process in front of it that speaks text: a datom typed at the CLI comes in through it, and every emission goes out through it. Every translator carries the Caller, from the connection's peer credentials, in `Call.{ Caller Input }`.
:::

+ The translator answers what its Nexus's types are: asked for a specification, it describes the type and prints the Ethos, and the Nexus is not asked. A CLI given no datom receives the Ethos of its Input and Output.

```ethos
+ Library
+ [ :ethos:[ Library Name ] ]                     ; imports
+ [ Describe.Name                                 ; types: text only, answered by the translator
+   Described.Library ]                           ;   printed as Ethos
+ []                                              ; traits
+ []                                              ; associations
```

```datom
+ ; flow-nexus 'Describe.Send'
+ Send.SendRequest
+ SendRequest.{ Address SendableMessage }
+ Address.{ Aspect Topic Model }
```

### Proposal 3: Ethos is a Nexus · psyche-belief › vision/long-ethos.md, a new file

::: comment
A new module, for the horizon past the translator answering alone: one Nexus holds every specification, and a specification is asked for and carried in signal like any other value.
:::

+ ---
+ description: Ethos as it is to be past the compromised phase: a Nexus that holds every specification.
+ ---

+ Ethos is a Nexus. Its Memory holds every specification as a Library value; a Nexus, a translator or a CLI asks it in signal what a type is and receives the Library, and the asker's translator prints it.

```ethos
+ Signal
+ [ :ethos:[ Library Name ] ]                     ; imports
+ [ Describe.Name ]                               ; inputs: what is this type
+ [ Described.Library                             ; outputs: its specification, as a value
+   Unknown.Name ]
+ []                                              ; types
```
