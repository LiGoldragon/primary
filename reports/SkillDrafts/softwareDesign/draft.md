# software-design

The anatomy of a well-designed object-and-capabilities-oriented machine is being created.

## The map

The first act of design is the world model: an ontology, an anatomy, an object-and-capabilities-oriented layout of what is being created. Code comes after the map is approved. A checklist that catches bad code means the failure already happened upstream, when code was written without the map.

The map is of the world, not the process. It contains what exists, what each thing contains, and what each thing can do. Steps are walks across the map, never things on it. A service is a step dressed as a thing. Where a proposed type names a process rather than a thing that exists, the process is a walk across existing things and the service type does not belong on the map.

The map's destination form is the Ethos interface file. Ethos is not yet runnable, so the model writes the Ethos it cannot run. The map is written even when its target language cannot execute it.

## Types first

Design begins with the types. The types are the things that exist. Enumerate them, understand what each one is and what it carries, before asking what any of them can do.

> "we need to think very carefully of what the types are. First, really, because the traits are something that the types implement. We don't look for traits and then think of types for that."

A type is a thing with identity: it can be named, it can be distinguished from other things, it carries contents. Every logical aspect of the domain that has identity becomes a type. Turn every logical aspect into a type.

## Contents before behavior

List what each type contains before asking what it does. Containment is structure, not behavior. A table has legs; it does not leg. Fields are the anatomy of a type. The anatomy comes before the capabilities.

When two things always appear together, they are the contents of a third thing. When a thing built from two inputs has no name yet, consider whether the pair is itself a nameable thing.

## Capabilities

A trait is a capability a type has. Traits are what types implement. Every method call in the code lives under a trait, because traits are the comprehension surface: the layer where concepts become visible and implementations are constrained to think within them.

A capability is placed on the thing that contains its subject. The thing that carries the name is the thing that is resolvable. The thing that holds the text is the thing that is realizable. The receiver of a trait method is the thing the capability is about.

Action traits take the infinitive verb: Walk, Write, Read, Resolve. A type implementing Walk is capable of walking. A type implementing Resolve is capable of being resolved.

### The costume-trait fingerprint

A trait method that must be handed its own subject as a parameter is a regular function wearing a trait. If the type needs a name handed in to resolve the import, it is not resolvable; the type that already carries the name is. Strip the trait wrapper: if nothing is lost and a free function serves equally well, the trait adds no capability.

Honest boundary: parameters that narrow or direct an operation the receiver already owns are legitimate. A query range, a callback, an event payload do not disqualify a trait method. The diagnostic applies when the parameter is infrastructure the receiver cannot provide, not when it selects among things the receiver already contains.

Creation is exempt: the created thing does not exist yet, so it cannot be the receiver.

### Direction pairs

A direction pair never sits on one type. The textual type carries Realize; the real type carries Textualize. Any type implementing both directions has the wrong implementation. You do not textualize the text, and you do not realize the realized data. If you cannot find two different types, the implementation is wrong.

### Fragmentation

One type implementing many single-function traits is probably one trait not yet seen. The problem is not that a trait has one implementor, but that many of those traits should be one. Fragmentation is failure: placeholder traits for every function create no sensible ontology.

## The spine is conversions

The program's high-level shape is a chain of conversions. From when infallible, TryFrom when not. Never Into. From is preferred because creation is demand-driven: things are created from other things. Nobody harvests a material and then asks what it can become. Everything is demand-driven, end-result first.

Multi-input creation is TryFrom on a tuple. When something is built from a registry and an assembly file, it is `TryFrom<(Registry, AssemblyFile)>`. With tuple-encoded inputs, multi-input creation is just TryFrom; there is nothing else to make.

Conversions consume their inputs by value. No references held into inputs, no clones up the chain. Memory doubles only at clone. The created thing must not hold references into its inputs, so the inputs can be properly dropped.

## Names

A name tells the truth at the moment the thing exists. A thing that still needs writing has not been generated; it is assembled. Call it AssembledRust, not GeneratedRust, until writing has happened. The name describes what the value is when it exists, not what will happen to it later.

## Main

Main is a few lines tying the specification together. The schema is stated as objects: a fully compliant data tree that can yield the entire program. The code between types is conversions: get the end result, TryFrom the most high-level type, break each type down into what it is made from.

> "most programs create the schema in the code instead of creating the schema and then just tying it up with a few lines. If you read between the lines, you would see the schema."

The schema is not between the lines. It is the types themselves, and main is the few lines that tie them together.

## Deeper levels

High-level reads as TryFrom and new types. Deeper levels carry specific behavior beyond conversions. The more specific traits appear when delving into the internal life of a type: how an import reference walks the world to find its referent, how a block scanner advances through text.

The depth is unlimited, but the principle is the same at every level: capabilities belong on the types they are about, steps are walks across existing things, and the anatomy is enumerated before the behavior.

## Illustration: Import Resolution

The import-resolution world map demonstrates the protocol applied to a concrete domain.

### The things

**Registry** -- an index of all the sources: name-to-source associations. It has entries; it does not resolve.

**AssemblyFile** -- the recipe: everything needed to define one build, no more than one possible output. It has settings; it does not assemble.

**ResolvedAssembly** -- the assembled source, the world the resolution walk crosses. Made from its two inputs: `TryFrom<(Registry, AssemblyFile)>`, consuming both by value.

**Source** -- the unit a registry name points at. Contains a tree of files, with a distinguished default file (lib.es).

**File** -- one source file, one Rust module. Contains type declarations and import references. No namespace inside a file.

**ImportReference** -- what exists where an import is written. Contains a source name (for external pulls), a file path, and the type names it imports. It already carries every name it is about.

### Contents, then capabilities

Every thing listed above is drawn with its contents first:

```
ResolvedAssembly            TryFrom<(Registry, AssemblyFile)>
 +-- from: AssemblyFile     (the recipe)
 +-- from: Registry         (index of sources)
     +-- has: SourceName -> Source
                              +-- has: File tree
                                        +-- has: type declarations
                                        +-- has: ImportReferences
                                                  contains: SourceName, FilePath, TypeNames
                                                  Resolve  <- the one capability on this map
```

Only ImportReference has a capability on this map: Resolve. It is placed there because the import reference contains its own subject. The registry, the source, the file -- all are containers. They have things; they do not do.

### The walk

Resolution is a walk across the map, not a thing on it:

Its SourceName, through the Registry's associations, to a Source; its FilePath through the Source's tree to a File; its TypeNames among the File's declarations to the referents. The walk errors at the first missing edge.

### What dissolved

The rejected design had Resolving on the manifest, FileYielding on the source, ReferenceResolving on the import reference with the manifest handed in. All three were the process view leaking into the ontology: containment drawn as behavior, with the subject handed as a parameter.

On the map, no Resolver type exists. The walk crosses other things' contents, and the world it moves through has its name: the ResolvedAssembly. The environment problem -- may the lookup table be an argument? -- was an artifact of the service framing.
