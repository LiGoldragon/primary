# ethos

## Listing only types uses the types type

Context: Comment by the living on the book "Anatomy Correction" (Psyche Fable c64ee3), on the block "Ethos file 2 of 2 · Library root". Read by this flow from the page on 2026-09-30.

> If you're only listing types then you can use the `types` type. We should make sure that that's in the code, in the spec, and in the vision anyway.

-- psyche, typed (page comment, 2026-09-30T16:59).

## Too much indirection; a variant carries the type of its own name; the struct follows the variant

Context: Comment by the living on the same book, on "Ethos file 1 of 2 · Signal root".

> This is something that goes deeper but the ethos syntax here is not what I envision still and I didn't address it before. Now I see that it's a bigger problem. We also want to work on other things and try to fix it. I feel like I've been fixing for days.
>
> On the syntax we don't want to do something like there's too much indirection. I already said, for example, if you have a skill type and one of the variants is psyche, that psyche object: the rule of ethos is that if there's another type called psyche with the same name, that's what data that variant carries. You don't need to write psyche type.
>
> We don't really need something like the collection because submit is too short. Using just an indirection to put a simple struct there, I think, is bad form. I think we can just have the definition of that struct be what comes right after the submit. The submit variant has, for data, a struct and its name will just be derived deterministically by ethos. I think that, for a variant, you can have a variant and a struct name be the same thing so I don't even think that's a problem.
>
> When we say stuff like skill name, I think it should just be name. Maybe not. Maybe that's appropriate. I haven't read everything. I don't know what deployed is. I'm trying to see where deployed actually happens. Oh vector deployed. Okay yeah, that's fair. The rest is all good.
>
> Like I said don't use psyche type. Just type psyche. I mean I'm not telling you to change. Obviously that's [the vision] so I want all of [the vision] to be edited to take that into account. Let's put a package together for this and give it to Fable on a new flow to help design this properly so he can send sub-agents to look at the current state and make his design proposition. Astra makes his and then we'll combine them. Fable and Astra Mind will agree after they've done their own design proposal on what it should actually look like.  And then Mindester [sic] will implement it on a fresh flow.

-- psyche, STT (page comment, 2026-09-30T17:10). Transcription corrected: "division" → "the vision" (twice). "Mindester" kept as heard.
