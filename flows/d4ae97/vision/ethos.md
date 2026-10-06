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
