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

## 2026-10-14 — Ethos and datom translated to Clojure and EDN

Context: spoken to the Psyche Core Tertiary after commenting on «Short-term prototypes: Clojure now?»; relayed.

> I've commented on the Clojure prototypes and I want to design a standard way to translate an ethos specification to essentially a Clojure type, I guess, that can be represented in EDN instead of datom. For both Clojure and EDN let's work out a context module for this: how we translate an ethos and datom syntax into Clojure and EDN.

-- psyche, STT.

## 2026-10-14 — Ethos/datom-to-Clojure prototyping, a Mind Clojure topic

Context: same speech to the Tertiary.

> I want to move away. Let's get Mind Astra on a fresh flow to work with Mind primary and secondary on a fresh flow or maybe on a new topic on Clojure. Let's get the design down first: land some minimum vision on how we want to do this ethos/datom-to-Clojure prototyping. Then we'll get a minimal proposal for all of the short-term tools that we need. Then we'll get a specific Mind primary and secondary topic, a Clojure topic that will focus on writing, maintaining Clojure prototypes, or migrating any kind of script or needs into Clojure.

-- psyche, STT. ("Mind Astra" kept as heard: read as a Mind flow on the Astra model.)

## 2026-10-14 — The Clojure translation, fleshed out

Context: after reading «The shared Clojure translation pattern».

> I read the shared Clojure translation, or whatever it's called, and it's all good. It can all land in the proposal.
>
> Now I want it much more fleshed out. Even the graph, the flow graph, should be in the vision. I want even more actual examples. I want to see some example code that's been... and then I want the mind to document it to create a knowledge skill that I'll review in terms of how this actually works in practice after testing it.

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.

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

## A datom is shown with its Ethos specification

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the line { read minimal «One known question, one line back.» }.

> This syntax is wrong because these should be variants so they should be capitalized and never show a [datom] without its ethos specification, which can just use the prefix `type`, right? We can create an inline syntax for an ethos object and an example of it, or more than one example of it.

-- psyche, STT. Transcription corrected: "datum" → "datom".
