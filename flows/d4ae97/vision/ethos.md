# Ethos

## Don't double-wrap types: if a job is a flow ID, say flow ID

Context: his comment on «Flow spawning», on its Library root (Role.[ Voice Job ], Job wrapping a FlowId), 2026-10-06T14:59.

> Well first of all I still don't see the meta flow. If a job is a flow ID, then why are we even using the word "job"? Just use "flow ID". Why are you going to wrap a new type with another new type? Don't double-wrap types. That's silly.

-- psyche, typed, book comment.

## Ethos is central, very central

Context: said to this seat on 2026-10-06, turning to the datom expansion and an ethos psyche distillation.

> Keep in mind ethos: ethos is central, it's very central

-- psyche, STT.

## The datom file expansion and the ethos syntax changes are implemented in ethos, ahead of the three-repo curriculum deploy

Context: same message, 2026-10-06; on Astra implementing the three-repository, skill-based curriculum deploy.

> I want to get Astra going maybe on a new flow after all this, on implementing the three-repo skill-based curriculum deploy. I guess we would need the datom file expansion and also all of the things that I've been talking about modifying ethos syntax to be implemented in ethos.

-- psyche, STT.

## Types are declared inline up to a decent level of recursion; repeating type names to declare them apart is noise

Context: his comment on «Ethos, distilled», proposal 5 (Everything is a type), 2026-10-06T15:52.

> There's some good here but remember I was saying that until we reach the third level of recursion I would rather see the types defined inline. Here there would only be one entry where each field of the struct would have the definition of these types inline, which would avoid repetition, right? That's the whole point: the terseness, unless the type is reused somewhere else.
>
> Even if Ethos must support declaring types inline that are used elsewhere, it could be confusing visually to find where a type's been defined but that's okay. I would rather the types be defined inline up until a decent level of recursion. I don't want to have to repeat the type names just so that they're declared independently. I think that's silly. And it creates a whole bunch of repetition, which creates a whole bunch of cognitive load.

-- psyche, typed, book comment.

## Inline declaration is mandatory unless the type is too deep; an algorithm decides

Context: his comment on «Ethos, distilled», proposal 6 (Inline types), 2026-10-06T15:53.

> Well like I said earlier, even if a type is declared inline in one place, it can still be declared at the top. We don't have to and in fact just because of the extra repetition that creates, I would want to make the inline declaration mandatory unless that particular type is so deep that it itself requires too much recursion to be declared inline. We have to explain some kind of algorithm to determine whether or not a type should be declared inline.

-- psyche, typed, book comment.

## A one-position type is called a new type

Context: his comment on «Ethos, distilled», proposal 7 (One position), which said "There is no struct of one position. A type that holds one other type is written as its name, a dot, and …", 2026-10-06T15:55.

> No it's not. It's named `a.` and that's a type. It's a new type, which is explained syntactically elsewhere. We're not going to talk like little kindergarten. We're engineers here. We're going to call things what they are and that's a new type.

-- psyche, typed, book comment.

## Line breaking: a recursive block that would run too far right opens its first element on a new line, indented; vectors wrap at a width, aligned with the first item

Context: his comment on «Ethos, distilled», proposal 8 (Vertical), on its example `launch {` with `voice` on the same line, 2026-10-06T15:58.

> This is a good beginning but I'd like to further develop the logic that we use to determine where the new lines are and things. If the recursive block is going to expand to the right too much, then instead of, like in the example, you have `launch {` and then you put `voice` on the same line, instead of that I would put `voice` on a new line, indented right, so that you get more space to the right that way.
>
> This is fine the way you had it in your example because `voice.aspect.layer` was not so long. Actually it's wrong because `aspect` is declared elsewhere and we're saying we can have three levels of recursion. `aspect` should have been declared in line, which means `voice` should have been on a new line, and then you would add more than enough room to declare `aspect` and `layer` in line. `layer` can have its variance wrap around.
>
> Like when we have a vector, we can do this: we can have more than one item per line but at a certain length it wraps around and lines up with the first item and then continues like that. We can have a certain number per line but only up to a certain width.

-- psyche, typed, book comment.

## Review the specification of the operation type
Context: comment on "Composed" (with open and spawn), section 4 of «Flow and Message» 2nd edition.

> What's this section about, with `composed`, `open`, and `spawn`? What is that? I'd like to get to review the specification of the operation type ethos.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.

## Show the Ethos, not the Rust it generates
Context: comment on "enum" in the Names section.

> Well if you're showing, don't show me code generated from Ethos unless we're working on Ethos and how it generates Rust. Just show me the Ethos. That's the whole point of having Ethos. If you show me the Rust that Ethos makes, then we lose all of the benefits of even having Ethos. It's like having winter boots and going outside in the snow barefoot. Use your winter boots.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

## Newtypes, not type aliases
Context: comment on `pub type FlowId = String;`.

> Isn't that a type alias? We want new types not type aliases. Let's look at what this is in practice on the Rust side and what the differences are. From memory I don't think I want type aliases. I'm pretty sure I want... I think they're called the single tuple new types or just new type for short. I think the properties of those are more interesting than these type aliases, which I think don't really offer much in terms of correctness but you're welcome to correct me.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

## Traits are load-bearing abstractions
Context: comments on "ReportsThroughCli", "PreparesClaudePane", and the one-method Nexus trait.

> On a similar note here, maybe something like executable instead of reports through CLI. I feel like the machine is just inventing a whole bunch of silly traits that are not really load-bearing, as in it's offering the right abstraction. The [trait] is a cognitive help so if it's just these silly big verb-containing phrases, it seems like it's just sort of making [traits] up for the sake of filling the requirement that everything must be done under a [trait].

> That doesn't really qualify as a trait and it's probably too narrow. There's probably a bunch of other capabilities that we could agglomerate under an appropriately named trait, like a Claude host trait. I guess we can use either a qualifier or a name for traits.

> A trait that only has one function is suspicious and a trait that's only implemented by one type is doubly suspicious. Just throwing that out there. I think we need to design traits more carefully and types. This is why we created ethos.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06. Transcription corrected: "trade" → "trait" (his own correction, "Trait not trade.").

## The running Nexus as operation, actor or process; all types in Ethos
Context: comment on "RunningNexus", «Start: what self is».

> This is an interesting concept and I think it belongs in operation ethos as the main operation. Maybe "operation" is the right term. Maybe it's "actor" or maybe there's something in between: "process."
>
> Showing me types in Rust is kind of silly. Like I said, we have Ethos. Is that because we have a problem with it? Is it because we don't support mutexes in Ethos, so the machine feels obligated to define that type in Rust directly? I feel like we should maybe possibly make all of the types in Ethos but maybe there are limitations and problems with that. Or maybe it's not realistic. You're invited to push back on that but also to consider it seriously.

-- psyche, comment on «The code» 1st edition (https://claude.ai/artifact/WKNo47drHA8VWSruvMUFDT), 2026-10-06.

## A Nexus's types live in its three roots or in named libraries
Context: comment on `Settings`, among the types Curriculum defines in Rust.

> Yeah that's what I'm saying. When we write a nexus, essentially all of the types, because we have three layers, are going to be in one of the three layers or in the library. The libraries can be named. They can have subnames, right? Kind of like Rust: if you create a file, I guess, called foo.bar.ethos or whatever (what is our file suffix for Ethos anyway?), .ethos is great because LLM is thinking word anyway.
>
> I don't know where I was going but yeah this is a shit show. I'm realizing now that I'm actually looking at the code with you and this is what we need to do, right? Let's fix this. Let's rewrite this as a whole vision that would be better. Even if I don't agree with all of it maybe you can just apply my correction and then we'll write the vision. That's it: write the vision and it's all around the ethos code.

-- psyche, comment on «Curriculum's ethos, and every Nexus's three roots» (https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU), 2026-10-07.

## Variants are ordered by seniority, the first most senior
> I guess we should represent it in the order, so whenever you have a variant in ethos you need to position the variants hierarchically. There's an implied hierarchy: the first one is most senior. That's going to be the case with spirit being first and, in the field, compensation is above trial, right? It's tested, trial, and field work.

-- psyche, STT, 2026-10-07.

## Traits are written in ethos
> We can have other kinds of checks to make sure that all implementations are done under a [trait] but that's very mechanical. The model is just code around it and writing really dumb traits. We have to teach people how to design traits, which is why we have to look at the traits, which is why all the traits should not now [sic] have to be written in the ethos. We can mechanically make sure there's no trait.

-- psyche, STT, 2026-10-07. Transcription corrected: "trade" → "trait".

## No trait outside the ethos-generated code (correction of the entry above)
> I was saying we can mechanically make sure there's no trait in the non-ethos-generated part of the code and my speech detect got me off.

-- psyche, typed, 2026-10-07. Corrects the [sic] in "Traits are written in ethos": every trait is written in ethos; a mechanical check finds none in hand-written code.

## Ethos redesigned to his syntax; patterns wanted and disallowed
> I want to redesign the ethos and flow. ... Actually probably changing ethos to better conform with my expectations of the syntax and what kind of patterns I want to see and what kind of patterns I don't want to see and even disallow

-- psyche, STT, 2026-10-08.

## Ethos is designed with the datom payload's cost in mind
> Basically the guiding principle in designing the ethos and the datom payload is also keeping in mind what the datom payload looks like, considering that the datom will probably be more expensive because machines will have to output them. It's funny because System 1 models actually make that cheaper, which is interesting.

-- psyche, STT, 2026-10-08.

## Jev and the System 1 models speak a subset of Ethos
> Also I want to marry Jev System 1 and its siblings, the System 1 models, to probably a subset of the Ethos specification so it could talk to an Ethos contract. Like I said it's only a subset because it doesn't have all the types yet. Let's get that also going, where we're designing in another flow.

-- psyche, STT, 2026-10-08.
