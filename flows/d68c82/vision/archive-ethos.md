## 2026-10-14 — Ethos and datom translated to Clojure and EDN

Context: spoken to the Psyche Core Tertiary after commenting on «Short-term prototypes: Clojure now?»; relayed.

> I've commented on the Clojure prototypes and I want to design a standard way to translate an ethos specification to essentially a Clojure type, I guess, that can be represented in EDN instead of datom. For both Clojure and EDN let's work out a context module for this: how we translate an ethos and datom syntax into Clojure and EDN.

-- psyche, STT.

## 2026-10-14 — The Clojure translation, fleshed out

Context: after reading «The shared Clojure translation pattern».

> I read the shared Clojure translation, or whatever it's called, and it's all good. It can all land in the proposal.
>
> Now I want it much more fleshed out. Even the graph, the flow graph, should be in the vision. I want even more actual examples. I want to see some example code that's been... and then I want the mind to document it to create a knowledge skill that I'll review in terms of how this actually works in practice after testing it.

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.

## A datom is shown with its Ethos specification

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the line { read minimal «One known question, one line back.» }.

> This syntax is wrong because these should be variants so they should be capitalized and never show a [datom] without its ethos specification, which can just use the prefix `type`, right? We can create an inline syntax for an ethos object and an example of it, or more than one example of it.

-- psyche, STT. Transcription corrected: "datum" → "datom".

## White square brackets as sugar; layers; traits as capabilities

Relayed by Psyche Core Tertiary, 2026-10-16; the living's comment on «Battery drain in sleep», Proposal 1.

> I actually want long-term marked ethos. I also want a review that I want to add: the different kind of square bracket. There's another pair. I think it's called a white square bracket. I want to use that as sugar in ethos, as a special syntax at the right layer of interpretation, because we have different layers.
>
> I want to review all the layers and all the changes that we've made on ethos, and which layer they're at. I also want to review the concept of traits and how we need to design traits so that we can implement a state where all the traits in the program have to be declared in ethos. Also, all of the implementations have to use one of those traits, so that we can then see the behavior part of everything in terms of the signature and what everything is called: the anatomy of how we think of every feature.
>
> Every feature is a [capability], a capability, which is borne by a certain trait, and we need to learn how to name traits. We need to put together the best understanding of the ontology of giving trait names to things and how we want to do it: describe it as a capability, as a feature that a certain type of object has.

-- psyche, STT. Transcription corrected: "capa" → "capability".

## Traits in Ethos: long term

Context: on the Flow seat's finding that ethos-zero generates no traits and Flow holds 209 hand-written traits, 2026-10-16.

> "Yeah well, of course we can't meet all of our long-term ethos goals in the short term. That's why we have short term and long term. Long term we want all the [traits] in ethos and short term we just do without."

-- psyche, STT. Transcription corrected: "trades" → "traits".

## Ethos and Nexus are infrastructure; Chronos is the example

Context: comments on «The Ethos vision, 2nd edition», 2026-10-16T19:03–19:04.

> "Yeah let's use this flowchart in the short-term section in Nexus."

-- psyche, typed. (On the opening figure: Ethos specifies Nexus; Chronos is built as a Nexus; Nexus guides Flow; Flow then guides other nexuses.)

> "I can see already that the machine [who] made this totally misunderstood what I meant. Ethos and Nexus are not golden examples. They're basic infrastructure. They're not examples. They're like the kind of wood we use to build our houses. There's a deep misunderstanding here and this whole book has to be redone."

-- psyche, typed. Transcription corrected: "hood" → "who".

## An extendable enum marked by uncapitalized user entries

Context: the living, same message as the always-on Flow core.

> I also want to talk about this special syntax for a sort of extendable enum concept, which is differentiated by the user-made entries being uncapitalized. It's like a mixed symbol that tells you: if it's the uncapitalized kind then it's the user-made variant with a string, which is the word made in topic style: words only, uncapitalized camel case identifier.

-- psyche, STT.

## Sema is the meaning language; the database is Memory

> "Here Sema is used incorrectly. Sema now means the meaning language, the subdialect of it. It's like a specialized language to a semantic language essentially. The database is called Memory now. Let's make sure we get a pass on Opus and a pass on Sol, both checking to see if they can find all the places where Sema is used incorrectly and changed for Memory."

Context: comment on «Ethos categories and sugar», Roots section, 2026-10-18 17:25.
-- psyche, STT.

## One Ethos file holds one main object

Context: the living withdraws his recent notion that a single Ethos file could contain several main objects.

> I want to come back on a suggestion, a notion I had made recently, where I was saying that a single ethos file could contain multiple ethos main objects. I want to roll back that notion because it would create complications with how things work in the registry and how things are addressed. Then you would have multiple objects occupying one name.

-- psyche, typed.

## A specification groups its items by variant

Context: said while asking for the flow-definition book.

> We don't have a vector of things where each one gives its variant. We have a vector of a certain variant and then a vector of another variant, kind of like how we have these ethos types. The first vector in a signal file is a bunch of queries and then the second vector is a bunch of responses. We agglomerate them by their variant.
>
> Let's get some wording in with some examples on how to do a good ethos specification, how a not-so-good ethos specification would look in comparison, and why: because we save repetition. Essentially we want the Datom syntax to result in something as succinct and dense, with as high a signal-to-noise ratio as possible.

-- psyche, typed.

## An open enum, and the camel ID

Context: comment on «Flow's vision», the metaflow paragraph whose default topic is core.

> I also, in regards to this, want to talk about a special representation of `datom`. We have these objects that have an unconventional representation, like the word-based hashes. I want to create these special enums that can be either one of the variants, or a special variant is implied when the object itself does not qualify as a variant (meaning it's not capitalized). When it's uncapitalized it means it's another one of its variants and then we would create this special definition in ethos: it would be a special object, like an open enum basically.
>
> If a payload is given with an uncapitalized identifier, I think I could have a temporary name for it called a camel ID. The camel ID is a word-based camel case identifier and we would need some kind of check eventually, long term, to make sure that it is a word-based camel case identifier. It would be represented without the variant so it's essentially like this extensible variant.
>
> In the topic we could have an actual set: a set of variants for the roles/topics, whatever we want to call that, that are constant, like `core` and maybe some others. This would allow the users or the machine to extend and essentially create topics as it needs to. This would be the same mechanism that we would develop to have some things represented differently, like a word-based hash for some hashes and any such kind of things. Let's get a whole book on that and a review of Ethos architecture, how this could be done, and what layer. Let's do a multiple-book series on Ethos, reviewing Ethos and modifying Ethos.

-- psyche, book comment, 2026-10-19T17:33, input mode not shown.

## Imports start with a colon and can be inline

> I also want to maybe modify the syntax for imports to actually start with a colon so that it could be done inline. If you wanted to import just an object inline where you declare a type, you would have the type name. Or if it's just being used in a field, you could just directly have the import, which would start with a colon and then an uncapitalized name (meaning addressing its namespace in the registry), and then so on, like another colon and another colon, until we get to the type. The same syntax would be used in the import section for consistency.

-- psyche, book comment, 2026-10-19T17:33, input mode not shown.

## White braces define a struct; white square brackets define a vector

> Also I think I want to use the white braces for struct definition. That way we can easily distinguish visually between a struct definition and a struct declaration. I also want to use the white square brackets to define a vector instead of using the word `vector` because it's so common.

-- psyche, book comment, 2026-10-19T17:33, input mode not shown.

## The colon replaces the dot for an inline import

Context: comment on «Ethos: imports and definition brackets», proposal 1, the code "Topic.:custom:Name".

> No there would be no dot. It would just be a colon so it's `topic:cost` and `:name`. The colon replaces the dot. That's how you know it's one or the other. If you mix them both you're going to make this whole thing way more confusing.

-- psyche, book comment, 2026-10-19T18:05, input mode not shown.

## Implicit imports depend on the Ethos object type

Context: comment on proposal 1, the intrinsic names known without import.

> The types that are implicitly imported will depend on the ethos type. We need to define these ethos types and what imports they have by default. I guess instead of "library" (or "library" is just "standard library"), later on if we want long term, we can define new objects like "non-standard library." Maybe try and do a "non-standard runtime object" later on but that's long term and it's just a notion.

> So yeah maybe there are more words that are known than just `string`. For example we have `vector`, `result`, and `option`. If we're going to start listing the implicit imports, or the builtins, or the standard builtins, then we should make sure they're all there.

-- psyche, book comments, 2026-10-19T18:03–18:04, input mode not shown.

## An enum declaration is a vector of its variants

Context: comment on proposal 3, the sentence "Where types are defined a plain bracket is an enum, never a vector."

> Well this is kind of not really correct because a variant enum declaration has a vector of variants. In a way it is a vector: it's a vector of the variants of that enum, which is why we're using the same delimiters that vectors use (because technically it is a vector).

-- psyche, book comment, 2026-10-19T18:07, input mode not shown.

## The variant as a field, not a header

Context: comments on «Flow's vision», 2nd ed., proposal 31, the Memory example `Flow.{ FlowId Address State.[ Running Ended ] Vector<Event> }`.

> Yeah this is all good but now I need a refresh on the spec of the different Etho subjects because you've changed a number of fields and I need to know what's going on.

> You've also changed the format back to the variant being one of the fields instead of the header, which I guess is okay. I think it's okay to keep that form now because it's more elegant. It's just less noise so let's stick with this format actually.

-- psyche, book comments, 2026-10-19T18:34–18:35, input mode not shown.
