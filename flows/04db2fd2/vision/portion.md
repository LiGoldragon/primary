# Portion

## "Portion" as universal term for field / variant / element; open vs closed portions

> instead of saying field, right, because the concept is universal. Like, it doesn't matter if we're talking about a vector and a list of variants in an enum, fields in a struct, or other things, every object, so to speak, is a portion. So like, one of the variant in the list of the enum's variants is a portion. And every field in a struct is a portion.

-- psyche, STT.

## Open and closed portions: bare string is open, delimited string is closed; an opened struct has its outer delimiters implied

> if we say that this is an opened struct, meaning it doesn't have its outer delimiters, its outer delimiters are implied. Right, so we have a closed and an opened version, essentially, of pretty much anything. Let's take, for example, the bare string. Right, so in a position where we expect a string, we don't know necessarily beforehand if that... Block, I guess, if we could call it, or that portion, if that portion is open or closed. Meaning a bare string is essentially an open portion. It doesn't have the limiters. It's just pure payload. Whereas the limited string is a closed portion. Or, yeah, portion, I think, is good.

-- psyche, STT.

## Suggestions asked for portion and for span

> represent everything again. what is your suggestion por portion? span?

-- psyche, typed.

## Portion is probably an enum; Headed as a variant that is a type; the ethos-types block; recursive-parsing-dependency concern; Span vs Extent

> I think a Portion is an enum, but im not sure. would it be wrong for Headed to be a type (a variant of Portion)? Then we would have a bunch of qualifiers. Headed carries a struct;
>
> ``` ethos-types
> Portion.[ Headed Delimited Bare ... ]
>
> ;; We once discussed an ethos syntax whereby the data of a data-variant is derived automatically when a variant is also another type in-scope
> ;; like I demonstrate here with Headed. It avoids the clumsyness of doing Headed.HeadedData. The name of the contained type would be derived deterministically
> ;; in a way that is very unlikely to create conflict. maybe something like DataOfHeadedVariant, or maybe something even more sophisticated which I cant even picture right now
> ;; which would deal with absolute naming (module included); Protos_Portion_Headed_VariantData (I dont know what rust's position is on using _ (whatever that character is called))
> Headed.{
>   Name.Symbol ;; Symbol is a specific type of qualified string
>   Separator.[ Period Exclamation Colon]
>   Portion ;; body - not sure if it needs to be aliased - Body.Portion - Ideally we dont even need to do that. but you can push back so we can think about this out loud
>           ;; problem; this introduces a recursive-parsing-dependency problem. So my design is either deeply flawed or I havent thought of a very clever trick.
>   Span ;; Or Extent. I think Span sounds pretty awful
> ```

-- psyche, typed.

## "We don't want to imply the box, that would hide too much."; Portions as single-variant enum vs Vector<Portion> syntax; "it should be Bare.Symbol"; Extent once on portion is better; enclosed vs unenclosed, opaque a different concern

> We don't want to imply the box, that would hide too much.
>
> Portions would be an enum with a single data variant (Portion). Did you mean Vector<Portion> ? Is that not the syntax for vectors?
>
> And it should be Bare.Symbol

> Extent once on portion is better.
>
> its not enclosed vs opaque. its enclosed vs something like "unenclosed" - opaque is a different concern

-- psyche, typed.

## Portions exist inside portions; the box is not objected to

> Headed lost its Portion member?

> problem is portions exist inside portions

> I didnt say anything against the box

-- psyche, typed.

## opaque is opaque; no containing portion

> opaque is opaque; no containing portion.

-- psyche, typed.

## A non-opaque enclosed portion holds a vector of possible inner portions

> an enclosed portion has an unknown number (vector) of possible inner portions

> non-opaque enclosed*

-- psyche, typed.
