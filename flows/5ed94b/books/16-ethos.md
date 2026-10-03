Presentation.{ «Ethos» }

# Part 1. What he wants

## What Ethos is

Ethos is the language the system's types and kinds are written in. It is still being designed.

> "Well definitely, ethos is being designed, one of those things."

-- typed, 2026-10-02

It exists because every older language is noisy, and none of them keeps the whole program correct once you add a higher layer of abstraction on top.

> "These two are noisy, or, in other words, they don't allow for the creation of a higher layer of abstraction which still contains the correctness of the whole."

-- spoken, 2026-09-08

Reading the Ethos is how he understands the system. The kinds become Rust traits, the types are declared in Ethos, and the hand-written code is mostly the bodies.

> "That allows me to understand the anatomy and the ontology of the system using ethos syntax, which is a lot more clear."

-- typed, 2026-09-13

Every language machines invent to talk to each other is written in Ethos.

> "all of the machine-to-machine language that is invented as you go is ethos."

-- said, 2026-09-20

## The roots

A Nexus is described from three sides: what it says, what it does, and what it remembers.

> "Yeah the memory is good. That's what it is I guess: signal, operation, and memory."

-- typed, 2026-10-02

Anything that has an effect gets its own operation type.

> "Anything that can have an effect is going to have a corresponding operation, which is going to be the type that we have to use."

-- typed, 2026-10-02

A fourth root, Library, holds what the others share.

> "You have the library, which combines them, and signal, which is more specialized."

-- typed, 2026-09-19

When a stored type changes, the edit to its Ethos is also the operation that moves the old data into the new shape.

> "That operation is going to be the very edit, the very update operation that this particular data type needs to change into its new memory format."

-- typed, 2026-10-02

## Everything is a type

There are no loose values and no key-value maps. Every value has a type.

> "Ultimately everything becomes a type because everything is a variant of a set."

-- typed, 2026-09-26

> "We don't have key-value in Ethos anymore. Everything is a type."

-- typed, 2026-10-02

You design the types first. The kinds follow from what the types can do.

> "the traits are something that the types implement. We don't look for traits and then think of types for that."

-- spoken, 2026-08-13

## How a type is written

If a variant has the same name as a type that already exists, it carries that type, and nothing more needs to be written.

> "The rule of ethos is that if there's another type called psyche with the same name, that's what data that variant carries. You don't need to write psyche type."

-- spoken, 2026-09-30

A variant can also declare what it carries right where it stands, and Ethos makes up the name of that new type.

> "The submit variant has, for data, a struct and its name will just be derived deterministically by ethos."

-- spoken, 2026-09-30

A type used in only one place is declared inline, where it is used.

> "I would also like to make it so that unless a type is used in more than one place, it should be declared inline."

-- typed, 2026-10-02

Struct fields have no names in Ethos. Rust names them after their types.

> "Ethos should create a struct with actually named fields, but the field names don't show up in Ethos. They show up in Rust, deterministically."

-- typed, 2026-09-08

A type that wraps exactly one other type is a newtype, never a struct with one field.

> "I think we should possibly even refuse single-field struct types and ethos, and instruct against them even in Rust, because those should be new types."

-- typed, 2026-09-08

## Kinds and capabilities

A kind is something a type is able to do. Its name is a quality, like Launchable, not a verb like Launch.

> "1. qualifier. Write isnt a kind. we say kind now, not trait."

-- typed, 2026-08-26

> "I think we went more towards the qualifier `launchable`. I think that makes more sense because that then cognitively translates as a kind."

-- typed, 2026-10-02

A capability is one function that a kind has.

> "capability will refer to the actual functions a kind has (Runnable would be the Kind, run would be a capability)"

-- typed, 2026-08-26

The thing that has the capability is the thing being called. A method that must be handed its own subject from outside is not a capability.

> "your trait methods are just regular functions pretending to be traits. if the type needs a 'name' to resove the import, then it's not resolvable."

-- typed, 2026-08-20

A capability's inputs are kinds, never specific types.

> "It should only be another kind because a type is too specific."

-- typed, 2026-10-02

## How Rust is made from it

The generator writes Rust for every type and kind: what goes over the wire, what the engine does, and what the database keeps.

> "just generate the rust code for types and generics/traits to define the wire types (signal), major internal engine operation types (nexus), and database types (sema)."

-- typed, 2026-08-10

Converting values to and from text is built in only where text is actually read or written.

> "That way the Nexus doesn't do the string conversion but the CLI does and eventually the user interface will have all of that conversion-to-string logic compiled in."

-- typed, 2026-09-24

The function bodies are written by hand for now. The generator runs only when asked. A running Ethos Nexus comes later.

> "no, ethos-zero is not a daemon, hence its name. ethos is the repo for the upcoming ethos nexus"

-- typed, 2026-09-10

Proposed: the comments in an Ethos file go into the Rust made from it, so the Rust explains itself too. Question 3 asks this.

## How it looks

Ethos grows downward. Anything that has a layer inside it opens onto new lines, with the inner parts lined up beneath.

> "I want it to be a language that expands vertically."

-- typed, 2026-10-02

A closing bracket ends the last line. It never sits on a line of its own.

> "I don't want the closing delimiter to create a whole new line"

-- typed, 2026-10-02

Every section has a comment, and so does every line that has a layer inside it, saying in plain words what the machine reads there. He wants to see the code with those comments as it is built.

> "Okay, let's do the full implementation with all the comments, in the sake of this new flow with the context module set up."

-- typed, 2026-10-03

## Where the library lives

A component's own Ethos lives in that component's repository.

> "the ethos code can live with the component."

-- typed, 2026-08-11

The shared types go into one core library, which needs a manifest, a registry and an index.

> "This should go into a library that all components can reuse, so maybe some kind of Ethos core library or Ethos standard or something. This might mean needing to develop the way ethos is put together, like manifest, registry, index"

-- typed, 2026-10-03

The first thing to go in it is the word-id library. It works for a hash of any size, and any id type gets its words through a kind.

> "It's generic so we can use it for any hashes of any size. ... Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?"

-- typed, 2026-10-03

## Topics

The subjects, topics and subtopics of the vision become variants in Ethos, inside a Nexus like Mind.

> "We have different subjects, topics, and subtopics and these will even become variants in actual Nexus components like Mind."

-- spoken, 2026-10-03

## Ethos in a book

Ethos is always shown as a whole file, starting with its root. A loose fragment is not Ethos.

> "Whenever ethos is written, this block is not ethos because it's lacking a type so it's invalid."

-- typed, 2026-09-29

Next to it goes a datom example showing it in use.

> "I want to see the ethos and the example datom: examples in use, how it would be used, and what kind of queries and responses we would get."

-- typed, 2026-10-02

He writes it this way himself:

> ```
> Voice.{ Aspect.[ Psyche Mind Field ]
>         Layer.[ Primary
>                 Secondary
>                 Tertiary
>                 Quaternary  }
> ```

-- typed, 2026-10-03

The same voice as a whole, commented file, with one proposed kind. The generator accepts it:

```
Library                                  ; the shared root: names other files may use
[]                                       ; imports: none, every name here is built in
[ Voice.{ Aspect.[ Psyche                ; types: a voice pairs an aspect with a layer;
                   Mind                  ;   the aspect is one of three
                   Field ]
          Layer.[ Primary                ;   the layer is one of four
                  Secondary
                  Tertiary
                  Quaternary ] } ]
[ Launchable.[ launch.[ Self ] ] ]       ; kinds: launch reads the thing itself and gives it back running
[ Voice.[ Launchable ] ]                 ; associations: every voice is launchable
```

## The three stacks

There are three stacks side by side. The old one stays where it is. The quick new one is today's generator, which writes Rust. The correct new one waits, unchanged.

> "the new correct stack is out of scope for now, but it should be clearly marked and not abandnned or otherwise modified with the wrong design while we do the quick-new stack"

-- typed, 2026-08-13

In the correct stack, Ethos runs through two further layers, Nomos and Logos, which signal each other all the way down to compiled Rust.

> "They work in series by sending each other signals to create this layer of code from ethos and datom all the way into compiled Rust."

-- typed, 2026-09-24

## The registry's kinds

The context-module registry left out role, and its list was named with a word that Ethos already uses for something more basic.

> "I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic."

-- typed, 2026-10-03

Proposed: the list is named ModuleType, and Role is one of its entries.

## What gets built first

Flow with context modules is built in six steps: Ethos, the registry, role configuration, launch, skill deployment from the manifest, and the first seat. Proposed: Ethos comes first, because everything after it uses its types. He reviews each step while it is being built.

> "Let's look at what's being built while it's being built so I can comment on it."

-- typed, 2026-10-03

## What it never does

Ethos never repeats itself, and never makes up a second type just to say what a variant holds.

> "Think about what I said about how I don't want this repetition of types, like where we invent another type to say what's inside a variant."

-- typed, 2026-10-02

An Ethos file has no version number. Versions go in a manifest.

> "I think I want to drop the version number altogether. datom doesnt have versions. if we version stuff it should be in a manifest of some kind."

-- typed, 2026-09-04

Ethos has no generics, only kinds. Where Rust would have a generic parameter, Ethos names a kind.

> "the answer is the mandatory trait! so T would be a trait!"

-- typed, 2026-08-01

# Part 2. What exists today

The generator is version 16.0.0. It is not on the command path. For this check it was built from its own repository. It reads the four roots, Library, Signal, Operation and Memory, and it refuses the old name for Memory. It accepts a whole file with comments. It refuses a specific type as a capability's input and asks for a kind. Each association becomes a check the compiler makes.

It still accepts a struct with one field. It writes a one-part type like Name, which holds a String, as a plain alias, so Rust treats it as the same type as String. Every comment is dropped: the Rust it writes has none.

No word-id library and no core Ethos library were found.

# Part 3. Questions

1. **Topics: fixed variants, or open names?** Mind would keep each topic as a variant, rebuilt whenever a topic is added.

   > "We can submit a new variant and then it has to be approved and added into the ethos spec and then the whole thing is recompiled."

   -- spoken, 2026-10-03

   > "for engineering reasons we don't create an enum for everything. There are these open-ended variants, which we call names."

   -- typed, 2026-09-26

   Answer yes if every topic is a variant, so Mind is rebuilt for each new one. Answer no if topics are names.

2. **Is Name a type of its own?** Today Rust takes any String where a Name is wanted. A distinct Name needs a one-part wrapper.

   > "A new type generally is like `name.string`, `age.integer`, or whatever we use: `int`."

   -- typed, 2026-09-08

   > "tuple: no tuple in the code we design: if some parts require it (standard traits, dependencies), then we allow it at that contact point only"

   -- typed, 2026-08-24

   Answer yes if Name becomes a type of its own and that one-part wrapper is allowed for it.

3. **Do the comments go into the generated Rust?** For example, "a voice pairs an aspect with a layer" would sit above Voice in the Rust.

   > "I actually would like all of the Ethos code to get way more comments so that I can see what the machine is seeing."

   -- typed, 2026-10-03

   > "make the syntax perfect and super minimal (so that there's no repetition, nothing out of place, and no noise)"

   -- spoken, 2026-09-25

   Answer yes to carry each comment into the Rust.

4. **How deep can a type go inline?** For example, Voice holds Layer at the second level. A fourth level would have to come from a library.

   > "We would have a maximum depth after which we would require the types that are at, I don't know, maybe the third depth to be imported from an external library."

   -- typed, 2026-10-02

   > "We don't have to make it a hard limit. Maybe it's not a hard hard limit"

   -- typed, 2026-10-02

   Answer 1 to have the generator refuse a fourth level, 2 to have it warn, 3 to leave the depth to the writer.
