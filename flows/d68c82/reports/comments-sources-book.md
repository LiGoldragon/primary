# Comments on "Sources in the commit message"

## Thread 93ad5a4d-2c0a-4d9e-922b-3d121029c2e5

**Anchored section:** remove the existing lists › text "vision-distillation b675f3d9 visionImpu…"

**Anchored element:** `<code> vision-distillation b675f3d9 visionImpurities acbb6006 distillation b675f3d9 distillation ac1e9ec8 distillationNegatives`

**Timestamp:** 2026-10-10T18:57

**Comment:**

So you can see how you could easily turn this into a variant with a struct in Elm syntax, right? Your variant would be `vision distillation` and then it would just be a vector of a name to flow ID.

I mean topic and Flow ID.

---

## Thread d691198d-94ad-489a-b56c-5fecec6c2848

**Anchored section:** the rule, in operation-psyche-distillation › text "Every distillation refers to the raw ps…"

**Anchored element:** `<p> Every distillation refers to the raw psyche it was distilled from, in the message of the commit that lands it and never …`

**Timestamp:** 2026-10-10T18:56

**Comment:**

Yeah this is good. We could also improve the format so that it essentially fits a datom, which would mean creating an ethos specification, but we wouldn't need to make an implementation that uses it yet. It would just be the ethos that shows. You can use a type, `type ethos`. It just starts with `type` and it defines a single type and you can define everything inline, like these quick type definitions, where you can use the inline import syntax.

You can land this now and then let's do another landing. We won't need to backport the new syntax to the commands. We can do that later. We can improve the syntax so that it's eventually compatible with Datom message. We could even define a specification and ethos for different variants of commit messages so our commit messages would start to be written in a Datom syntax with different variants.

I guess you could use vectors when there's more than one type of thing in a commit. It would be good to support that just in case we can't force the commit to be split up or something but we would encourage only one variant per commit message.
