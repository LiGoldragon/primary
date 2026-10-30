## Ethos is central, very central

Context: said to this seat on 2026-10-06, turning to the datom expansion and an ethos psyche distillation.

> Keep in mind ethos: ethos is central, it's very central

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
