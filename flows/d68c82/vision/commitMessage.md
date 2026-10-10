# Commit message

## Commit messages written in datom, specified in ethos as variants

Context: comment on «Sources in the commit message», ruling 1, approving the commit-message rule.

> We could also improve the format so that it essentially fits a datom, which would mean creating an ethos specification, but we wouldn't need to make an implementation that uses it yet. It would just be the ethos that shows. You can use a type, `type ethos`. It just starts with `type` and it defines a single type and you can define everything inline, like these quick type definitions, where you can use the inline import syntax.
>
> ... We won't need to backport the new syntax to the [commits]. We can do that later. We can improve the syntax so that it's eventually compatible with Datom message. We could even define a specification and ethos for different variants of commit messages so our commit messages would start to be written in a Datom syntax with different variants.
>
> I guess you could use vectors when there's more than one type of thing in a commit. It would be good to support that just in case we can't force the commit to be split up or something but we would encourage only one variant per commit message.

-- psyche, STT. Transcription corrected: "commands" → "commits".

## A distillation's sources as a variant: topic and flow id pairs

Context: comment on the same book, at the example commit-message list for vision-distillation.

> So you can see how you could easily turn this into a variant with a struct in Elm [sic] syntax, right? Your variant would be `vision distillation` and then it would just be a vector of a name to flow ID.
>
> I mean topic and Flow ID.

-- psyche, STT.
