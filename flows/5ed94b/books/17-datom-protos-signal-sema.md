Presentation.{ «Datom, Protos, Signal and Sema» }

How data is written as text, how it is read, how it travels between running programs, and how it is stored. A Nexus is one of our long-running programs; each has a small command beside it that people and agents type into. A seat is one running agent session.

## Part 1. What he wants

### Everything is data

There is one plane. Code, types, rules and settings are all data, and the notation shows it.

> "everything is data. ... Code is data. a type is declared with code, so a type is data. a trait is data. an impl is data. *everything* is data, but protolanguages make it more obvious."

-- 1 September

### Datom: data, typed, with no names in it

Datom is our text form for data. It carries only data, never the rules of a language.

> "you've mixed up datom with ethos. datom is data"

-- 26 August

He holds it high.

> "dont be so apologetic. Datom is the most advanced textual data format in the world."

-- 26 August

A datom has no field names. The type already knows what each position is, so the text carries only the values, in order.

> "Maybe you think that Datom has named fields, but it doesn't. The object is just the payload. There are no names for the objects in Datom. The spec is known: there are no named fields. Isn't that clear in the skills? Don't you have those skills?"

-- 20 September

A capitalized word in front of a structure is a variant, one choice out of a set. It is never a tag or a label.

> "And I don't know what you mean by tag. Datom doesn't have tags, has variants."

-- 26 September

A string with no space in it needs no quotes and is written bare. Anything else goes inside « and ».

> "only if it's a bare (undelimited because it doesnt need delimiters) string"

-- 10 September

A datom is a form at a path: each piece knows where it sits in the whole, and what shape it has. Proposed: this stands in his reviewed vision, but I found no words of his own saying it.

One datom as he would write it, read against a person type: name, birth year, address, roles.

```
{ Ada 1990 { «12 Rue de la Paix» Paris 75002 } [ Author Reviewer.{ 2024 17 } ] }
```

Braces make a struct, brackets make a list, and `Reviewer.{ 2024 17 }` is the Reviewer variant carrying two numbers. Nothing in the text says "name" or "year"; the type says it.

Everything we run moves to Datom.

> "All of the stack, the horizon, logics, everything is going to move to the new datom ..."

-- 11 September ("logics" is Lojix, by his word the next day)

### Protos: the shape every dialect shares

Protos is not a language of its own. It is the shared style of all our languages: the brackets, the heads, the nesting,. Its code is the part every reader shares, and opening a bracket switches what the reader expects until it closes.

> "This is important and is the part of the code which can be shared between all parsers (should be in protos; protos is the name we give to the style which all our dialects share; hence why the final fully-decomposed engine with 3 daemons is the protos engine, with datom sort of sitting besides it, as it is only for pure, typed data)"

-- 11 August

Datom is one of those dialects. It is only kept out of the engine that will turn Ethos into Rust.

> "because datom doesnt take part in the multi pass engine which ethos->nomos->logos->rust is slated to become. but youre right; beside sounds like its not a protos dialect. it *is* a protos dialect, but not part of the future ethos/nomos/logos rust-generation engine"

-- 14 August

Protos sees shape only. It does not know what a struct or a list is.

> "Protos is only about structure. It has nothing to do with `struct` and `vector`, and it only understands form, so it's only a very abstract structure, like the syntactic structure. It wouldn't know what anything is."

-- 3 September

Text is read down through several layers, one pass per layer: raw text, then shape, then meaning, then the finished value in memory.

> "basically what we're doing is a multi-pass process. We're not interested in doing everything in a single pass, because it creates a whole bunch of, I don't know, corner-cutting bad design."

-- late August

### Signal: requests and responses between programs

Signal is the binary form our programs exchange. Each side already knows every type, so nothing on the wire describes itself.

> "signal: portable rkyv + whatever protocol we decide to standardize (talked about before but just mark as TBD for now)"

-- 10 September

A Signal definition declares requests and responses, and its root is a set of variants.

> "... when you describe a signal ethos file, you're describing the requests and the responses. ...
>
> The root type of each definition is an enum. The structs represent an enum, and each thing can come in as an object."

-- 13 September

A request and a response are never the same type.

> "Something right off the bat, in your interface file, there's no way that input is the same type as the output or that anything is the same type as anything else. Because then why do we have different fields? Because they're different things."

-- 14 August

Every Nexus also has a second, settings channel, and it is never optional.

> "I'm looking at your draft and I would like to say that the metasignal is not optional because otherwise there's no way to configure the daemon."

-- 9 August

Responses are small by default. Long identifiers are cut short, fields nobody needs stay in the store, and a separate, explicit call returns the full form.

> "Your spec is good for the messages, but we need a small response. We need an efficient system, like a summary style or minimal style. You could have this minimal provenance response, which has a truncated hash in place of a hash. These hashes are too expensive.
>
> ... If there are fields that aren't necessarily needed, they can just live in the database and be queryable. The flow can query for them, and then we don't need to include all of those fields in these minimal response types. You would have an explicit type of call to get the full explicit response type.
>
> You can have these shorthand types that are usually default, and then you have the more explicit longer name. Let's make this a design standard in the skill for specifying signal."

-- 15 September

On 3 October he called the default a "simple form" of the same data, not a short one; his words are in question 4.

A Nexus learns who called it from the calling process itself, never from what the caller claims.

> "We have two standard signal handshakes. One checks the origin process of the call for the message to know where the message came from. We should put that in the signal."

-- 18 September

### A Nexus sends datom without knowing datom

Only the command beside a Nexus turns text into Signal and back. The Nexus itself receives Signal and nothing else.

> "... the Nexus only gets signal. The CLI translates datom into signal, so that has to be clear everywhere in the skill, in the vision. It seems it isn't because you haven't gotten that right."

-- 15 September

The same type library is built twice: with the text conversion for the command, without it for the Nexus.

> "The Nexus component is not going to do the textualization at all. That's only in the CLI and the client. ... When the CLI uses the signal library, it would derive Datomizable and composable, but when the Nexus compiles the same signal library, it would compile it without any of the textualization capability."

-- 9 September

That keeps every Nexus small.

> "But yeah it's really important that we don't put any extra logic for handling deserialization and serialization of text in the Nexus because the Nexus has to stay small. That's the whole point because they keep running ..."

-- 28 September

So a Nexus can hand a datom along, store it and answer with it, while only ever holding typed binary values. A settings file written in datom reaches it through its command, as one more Signal.

> "... like config.datom, right? ... so the Nexus doesn't speak Datom. It would be added into the CLI's dependencies so it's like it's another signal I guess."

-- 24 September (the words "doesn't speak" may be a mishearing)

### What travels, and what never does

Proposed, gathered from all of the above. On the wire between programs: Signal only, binary, typed, with the request or response variant first. In text, at a command or in a message: one datom, values in order. Never on the wire: text, field names, any self-description. Never by default: full long identifiers, or fields the caller did not ask for. Never into a Nexus: the code that reads or writes text.

### Streams

A stream is several separate parts: a start, the events, an end. They are not bundled into one object.

> "When I explained that a stream is several parts, I was disqualifying the object that tries to put all of the components of the stream in one source object. So your whole problem should probably go away. ... That's trying to fit a square block in a triangle hole."

-- 6 August

The stream sits as a section inside the interface, and the start and end requests live among the inputs.

> "a section inside the object"

> "Yes, the initiation and termination live in the input."

-- 7 August

### Sema: the store, and maybe more

Sema is the database engine of a Nexus. Its types are declared in Ethos, so what is stored is visible.

> "Yes, SEMA is the database. ... When we create the SEMA Ethos type for the root type, like we have library and signal, then we're going to be defining database record types. Yes, SEMA is the database engine."

-- 9 September

Thinking aloud later, he pictured Sema as a whole communication; that is question 1.

### Messages are datom

A message between seats is a datom: a variant first, then a struct or a list.

> "Like I was saying, we put it in a Datom object, so it starts with a variant and then a delimiter, which is probably going to be a struct or a vector, right? Depending on the type of messages we want to have and all that, we need to implement the proper nexus that uses specified messages."

-- 18 September

It arrives as a datom in the receiving seat's prompt, straight from the message command.

> "It then returns the string, and when the process returns, it sends the prompt in as a Datom-formatted object. That's how the message is composed, how it comes in, and it's recognized that way."

-- 17 September

No wrapper around it. The datom is enough.

> "I want to get rid of this pasted content ID XML tag around the messages. Get rid of it. It's just annoying. ... I think the Datom syntax is more than enough. ... let's make sure we are not forcing the agents to put information in there that's not necessary."

-- 24 September

His own words are never datom. That is how a seat tells him from a machine.

> "for now, the agents will know that it's me because of how the message is formatted. It won't be datom-formatted."

-- 18 September

Datom is not forced where no program reads it.

> "Yeah we don't need Datom syntax where the program doesn't need it so we're not going to enforce Datom syntax on a messenger that doesn't need it."

-- 27 September

## Part 2. What exists today

Witnessed on 3 October 2026, from the crates and the Nexus knowledge skill.

- The protos and datom crates are both at 0.32.2 on main; Signal's shared crate is at 8.0.0.
- Four kinds of Nexus run and speak Signal: the lock Nexus, two Flow Nexuses, the message Nexus and Lojix. An older message program also still runs. None of them speaks the newest Signal on main yet.
- Seats message each other through a Clojure command that writes into terminal panes directly, with no Nexus.
- Sema exists only as the store engine, 0.18.0 on main. Nothing yet models utterances and acts.
- The message, Flow and lock Signal definitions have no minimal or simple response form, and there is no Signal skill.

## Part 3. Questions

Answer each with its number and "1", "2", "3" or "yes".

1. **What is Sema?** On 9 September you said "SEMA is the database engine." On 26 September, thinking aloud: "I see a struct, right? It's like a complete communication: here's a vector of utterances, here's a vector of acts, and here's a vector of ethos objects, which basically categorize things based on their qualities, their kinds and types, right?" Is Sema the store (1), the communication (2), or both, one name over two things (3)?

2. **A subflow's report to its main flow.** On 19 September: "We're going to program it in the system prompt of all our machine calls, and everything is going to be Datom." On 27 September you said no datom "where the program doesn't need it." When no program reads that report, is it written in datom anyway? Yes or no.

3. **The Curriculum settings file.** On 29 September, as a notion: "Conceptually you would have the datom file there and next to it would be the compiled signal file so that then the Nexus could load it because it's already signal." On 24 September the file went into "the CLI's dependencies." Does the command read the datom file at each call and send Signal (1), or does a compiled Signal file sit beside it for the Nexus to load (2)?

4. **What the default response carries.** On 15 September the default was minimal, "which has a truncated hash in place of a hash." On 3 October: "This would not so much be a short form but a simple form, right? The simplified version is the part that doesn't have the flow ID. It's the same data, just represented differently, like it's cast into a different container, if you will." Does the simple form carry a shortened identifier (1), or no identifier at all (2)?
