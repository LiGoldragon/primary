# Ethos

## An Ethos Nexus whose signal, memory and operation are specified in ethos

Context: comment on «Sources and the registry», proposal 2, 15:22.

> In Ethos do we have an Ethos Nexus or is Ethos Zero a non-Nexus? We need to migrate the Ethos Nexus version so that we can do this. In Ethos I want to specify the three aspects:
> - the signal
> - the memory
> - the operation
>
> For one or another we can do Ethos now so that would go with the Ethos flow, the eco psyche flow [sic] design to design the ethos of all three parts of the Ethos Nexus.

-- psyche, STT.

## All traits and all types in Ethos
Context: the living ordering the Flow topic to re-aggregate Ethos, Nexus and Flow, 2026-10-11.
"I want to see traits also because all of the behavior, basically all of the traits. Here's what we need to do: we need to define all of the traits and all of the types in Ethos. Let's give this a shot on Flow."
-- psyche, STT.

## 2026-10-14 — Lean calls answer in a datom dialect of changes

Context: spoken to the Psyche Flow Secondary after the low-usage order; relayed.

> And I want research into the best Fable fallback. Probably it's going to be in the open source camp in the sense that we need it. I would like to have something to lean on to use less Fable, whether it's by using it as a front before Fable to make sure that the communication is always relevant.
>
> Basically we have this Opus. We need these light calls that have almost no training, no system prompt pre-training (or not pre-training but pre-prompt, like the harness-injected stuff). We really don't need any of the tools and stuff. We just have our own specialized datom-based dialect.
>
> The response just comes in as datom, with the variant and then the payload, which is probably a struct. We should have more than one field. There's always something useful, like the meta part of the payload, right? It could even be its own struct so that it's visually sort of like, "Here's the meta." You can even divide it like that so that cognitively you're telling the system how to design, right? You add meta here.
>
> In datom it's cheap because it's just an additional pair of braces. There's your inner struct, which is the metadata of your whatever, your simple last response, which is just text. It's like the default. Well it's not the default. I guess even the most basic responses can't even be just a single string payload because it would be a proposal, which would have a path at least. A single proposal is the basic fallback default, right, or multiple proposals and then you have a vector of them. They're each about something, the most basic of which is a path and then a diff, which can basically just take a variant, right, where you just have a plain edition, targeted edition, or whatever.
>
> Let's develop a really cool language to talk about changes. Also just for now, basic: between certain paragraphs or in a certain section because Markdown is its own structured data, we can map Markdown into a certain datom-based language of variants. You could even get an output of Flow to sort of draft that into a book and then get an Astra.
>
> All you have to do is basically collaborate with [Mind] Secondary and then we use Astra in this designer mode with secondary in its own aspect, maximizing the efficiency of each call. We make sure that the context doesn't grow beyond 128,000 tokens at the time of the call, right? If it's 127 then we can still use it especially if it's on the same topic.
>
> If it's not on the same topic, if it's a wildly varying topic, that's why we want lean calls: it's cheap to just start another one because it really doesn't even need tool calls. It can just talk to secondary to ask it what it would like to know. All the tool calls are really just talking to the secondary and the secondary then handles ...

-- psyche, STT. Transcription corrected: "mine secondary" → "[Mind] Secondary". Last sentence unfinished.

## A hand-maintained vector of types imported from Rust

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Chronos», Proposal 2, on Latitude.Decimal.

> Maybe there is a fraction library or even an angle library that has more properly developed types for this. Let's just maintain a hand-maintained, specified vector for a list of types that we sort of import directly from Rust into Ethos, so that the Ethos-to-Rust compiler can use that to know what to link to. We can even eventually have proper programmatic feedback on the code, so it would know where these types are coming from, like built-ins, basically.

-- psyche, STT.

## Comments on «The Ethos vision, 3rd edition», 2026-10-16

> "I've commented on the Ethos vision and it probably needs to be two books out of that, one of which is an Ethos syntax modification proposal. The other being the same thing being redone, adjusted for my comments obviously"

Context: on "Chronos is the example project built with them: the golden example from which Flow is implemented properly, then the other nexuses."

> "The first part is good. The second part is only good after you change it to make it explicitly short-term, in the sense that this truth might change. Maybe there's a particular term for this. Maybe the golden example is not going to stay Chronos and Flow forever and eventually even saying that we're doing this to develop Flow will become obsolete. So we need to mark anything that could at some point become stale."

Context: on "A type ethos opens with type and defines a single type."

> "I guess this would be the only payload that doesn't have a brace after its variant. It would just be inline dotted. It would say `type.` and then it would be the name of the type and then it's its specification."

Context: on "A datom is never shown without its Ethos specification."

> "Well we should say a new [datom] or a [datom] proposal. Obviously if we're using a common [datom] that's in production, then its specification will be in a knowledge module.
>
> Also I want Ethos, Opus, and Fable involved in redesigning. I want to get rid of the exception and change the exception from an actual syntax change that makes everything complicated to a formatting change that makes it simple.
>
> For the variant of an Ethos specification, as we had it before, in a `where` we would remove the outer braces of the struct of that variant of that file. Now I want the braces to be there explicitly and the variant to just be the variant, then the `.`, then the `{}`, but we'll make that on its own line. We won't indent the first inner object unless there's more than one variant and one iso variant. I don't know if we'll allow vectors of variants or whatnot.
>
> This would simplify the code a lot. We would just always expect a traditional datom payload for the Ethos specification, with each different variant having a different shape."

Context: on the type-ethos code example ("CommitMessage").

> "Actually looking at this now, I even want to modify the spec of Ethos. In that other proposal we'd also make it so that when there's a dotted form, there can be a space after it. That way we can split it up onto multiple lines.
>
> Instead of the brace opening on the same line as the dot, we can make a new line and then open the brace. Or if there are several dotted variants in a row, we can make an indent, a new line, an indent, and then the next name, and then another dot. We could even make a new line there again.
>
> That way we don't force things to expand to the right. In this type definition it could be `type.new indent` and then the type, which could be more aesthetic or better to read. I think it would be easier to quickly get the visual impression from that formatting."
>
> "Oh and this is very important: in this code `Type` should be capitalized because it's a variant. All these variants need to be capitalized. This is obligatory. It should be because it's interpreted by the ethos that only uses capitalized symbols for variants."

-- psyche, typed (input mode not shown). Transcription corrected: "datum" → "datom".

## Comments on «The Ethos syntax», 2026-10-16, 22:16–22:30

Context: spoken to the Psyche core Tertiary after commenting.

> "I commented on the ethos syntax and there's a lot of garbage. The code is fucking garbage so I want all the books redone because obviously the ethos is going to be wrong everywhere.
>
> Also we need to get serious about ethos traits because I really don't see any of them and it's like you don't want your programs to do anything. If there are no declared traits for these types, these types can't fucking do shit. It means you want a system that does nothing. If you show me another thing that has no [trait], you're showing me a system that doesn't do anything.
>
> Get Fable involved, stop being so retarded, and make systems that actually do things."

Context: Proposal 1, "braces open on their own line, under the variant; the first section sits on the brace's line".

> "No not quite. The braces don't open on their own line. It's just usually canonical to make a new line because, actually, you don't have to open the brace on a new line. I didn't say that. I said that it should be possible in the syntax to do that but that the new line really doesn't need to be for the brace.
>
> It's just that we do it on a non-indented new line, generally in files, because we don't need the indentation. We don't want too much indentation and the first variant is really just giving us the type of that file unless we do start supporting a vector, in which case it's still going to have a variant.
>
> It's not an invariant like you said it is. It's just usually good form but it's not necessary."
>
> "And no you would not put the brace and the first section on the same line. That's the whole point of why you make a new line after the brace actually. But if it's just a single type then there are no breaks because it's just one thing."

Context: Proposal 1's Library example, indented under the brace.

> "See here, you did it all wrong. You did make an indentation when I said... My whole point was the only thing I wanted to say. You missed my entire point, which is: no indentation for that first struct. Do you understand what I'm saying? I don't know why I'm asking you because you're not going to respond like that. Yeah that's what I'm trying to say."

Context: Proposal 2, "A space and a line break may follow the dot".

> "Not a space and a new line, just any kind of space or new line, any amount of space. The dot doesn't care if what comes after is right next to it or if there's a space, a new line, a tab, or any number of spaces."
>
> (On its Observed.Locks example:) "Yeah this example is good."

Context: Proposal 3, the type ethos with a one-variant CommitMessage enum, and "A type ethos may carry one or more examples of its datom."

> "This is invalid. We cannot have an enum with only one variant and I don't understand. I don't think your last paragraph is good. When you say a type ethos may carry one or more examples of its [datom], I don't know what you mean by that. There's no logic there. There's no foundation for what you're saying.
>
> I think you're confused because I said, "If you show me a new [datom], you can show me the type." Now you think that that means... I don't know, you're just fucking hallucinating bullshit. Do you understand what I'm saying?
>
> This is bullshit: you think that you're forcing the jigsaw puzzle pieces together. You're smashing them all. You're just breaking them all by trying to fit shit together that has absolutely nothing to do with what you're trying to explain. You're explaining the vision and then... I'm really tired of this kind of behavior where you just put bullshit together. You just try and fit everything together that doesn't fit together."

Context: Proposal 4, "Every variant is capitalized, a root's variant and `Type` included".

> "You don't need to say "type included." Why the fuck do you say "type included"? That just looks stupid. Stop talking like a retard."
>
> (On its examples:) "Your examples suck 'cause they're wrong. Anything that's wrong, anything that is not canonically written, or just a piece of it is just garbage. Absolutely fucking confusing fucking garbage. Do not confuse everybody with your bad, incorrect, shitty examples."

Context: Proposal 5 (Type is no exception) and Proposal 6 (whitespace after a separator).

> "This section is good."
>
> "This is good."

Context: Proposal 7, a canonical print that breaks after the dot, two spaces per link.

> "No I don't want to make this canonical. Your example is garbage because it's mixing things which cannot be mixed together. Stop making any kind of code that could not work in practice. These are wrong.
>
> We have to stop completely, absolutely: never, ever, ever make an example that is not real code, ever, ever fucking again. Never, ever, ever.
> - Golden fucking rule
> - Top of the list
> - Full book on this topic
>
> Stop giving me bad code ever, never, ever, ever, ever, ever. I want to see bad code ever, ever"

Context: Proposal 8, a new datom shown with its specification; a production datom's specification in a knowledge module; the example Reply.[ Accepted.Integer Pending ].

> "There's a lot of bullshit here. This specification may or may not be in a knowledge module. It depends if it's implemented so why are you saying that? You don't seem to understand the principles that you should understand before you start explaining this to me. Let's go back to those principles.
>
> Your example is bullshit because every ethos needs a variant and your ethos has no variant so it's fucking garbage, just like most of the code in here. You have to stop writing ethos like it's like you're writing it without caring. It's like you don't care. It's like you're just making shit, slop, shit, garbage, filth. Stop giving me fucking filth, you filthy bastard."

-- psyche, typed (input mode not shown). Transcription corrected: "trade" → "trait"; "datum" → "datom".

## Comment on the Role/Subagent Ethos in «Today, as psyche, 2nd edition», 2026-10-17T16:41

> "This is really inefficient. It's way better if you separate the specification: you create a vector in the category instead of repeating the category for every entry.
>
> "First" is a bit confusing: "First" what? You did some incorrect ethos there. I don't know if that actually compiles because, where you have `brief`, `compose`, `name`, and `roles`, these are all lowercase. You should make it clear where the ethos code ends, although it does make it clear, which is funny because of the syntax. I want `library.` and then `{` on the same line. We create the new line after `library`.
>
> There's a bunch of things that are weird about this ethos. I'm happy that Flow works. Let's make it work better but let's fix ethos while we fix Flow.
>
> I also want to talk about the new syntax for declaring a vector. Not that it matters but visually it could help if we use the white. In the same way, when we declare a struct, we could use the white braces. Anyway I'd like a whole book on that ethos side of things, obviously run by the ethos topic stack."

-- psyche (input mode not shown).

## Every file is a vector of variants; signal, memory and operation carry traits

> Since we have variants now to open ethos, I think that we can just consider every file as a vector variant. You can have a library, a signal, a memory, and an operation, in the same file if you want. It's just about file management but we need traits. We need traits on essentially all of the different portions: signal, memory, and operation. You need traits to do things.

-- psyche, STT.

## A set is a set

Context: comment on the grouping example whose first line is `Model.String`.

> Yeah this is good except in the example I would use `models` (which should be a set and not a string because it is a set). Just change that and then you can use this example.

-- psyche, book comment, 2026-10-19T17:49, input mode not shown.

## Example code is complete

Context: comment on the Datom example opening `Definition.{` in proposed vision/flow-definition.md.

> I don't see the enum where the definition variant is defined and I don't understand what the other variants would be so you're going to have to explain that to me. Don't make incomplete code. This is a failure. You failed to make complete code. You've shown me a variant that is not defined as an enum. Total failure, complete redo.

-- psyche, book comment, 2026-10-19T17:51, input mode not shown.

## A custom variant with a string, and a trait for its own datomization

Context: comment on «Ethos: the open enum», proposal 2, the example marking Topic open with a trait Extensible.

> I think one of the easiest ways to do this is to use a custom variant in the enum that takes a string. Then we have a trait, probably something like `unusually represented` or something like that. I don't know. Maybe you can make some suggestions for names. That trait, if it's implemented, is called in the datomization and dedatomization step for that object so that it has custom logic for serializing and deserializing it.
>
> Let's take a deep look at that and a dedicated book on the subject and then let's cover the different usages, like hash based on words.

-- psyche, book comment, 2026-10-19T18:01, input mode not shown.

## No ASCII-only concern

Context: comment on proposal 4, ASCII spellings of the white delimiters.

> I don't understand this section. I don't care about ASCII only. I'm not living in 1971.

-- psyche, book comment, 2026-10-19T18:09, input mode not shown.

## Models are a set (repeated)

Context: comment on «Flow ethos», proposal 3, the grouping example with `Models.Vector<Model>`.

> I just commented earlier today that the models are a set and not a string so why are you coming back to me with this fucking bullshit?

-- psyche, book comment, 2026-10-19T18:37, input mode not shown.
