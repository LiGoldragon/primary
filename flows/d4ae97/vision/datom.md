# Datom

## Hashes and flow ids: a stored type and a string representation
Context: said beside his comments on the second edition of the Flow book, about how certain objects convert between their stored form and their Datom form.

> Have on the side: develop this concept (and this is in my comments in the book) of how certain types of objects have a different kind of conversion in the sense that they might be an 8-bit, sorry. I don't know how many bytes 256-bit is but I think it's 8. No, sorry, it's more than that: 8 × 4.
>
> Anyway the number of bytes that it takes for the SHA-256 to fit is going to be the type or we should actually have an actual type. Let's look at what types people use for hashes in actual fast Rust code and that's the type we're going to use to store it.
>
> When it's actually represented in Datom or ingested from Datom, it's going to have some string representation and the flow ID as well, like the words to integer or something. We have some kind of a match concept that we'll implement so that the transcript file can be found using these words programmatically, in code. There's going to be a conversion which probably will end up with a some kind of a match, like a regular expression match or something, a glob on a superset of string, because the 33 bits doesn't actually line up with the alphanumeric cutoff of the Flow IDs representation in the alphanumeric (if you follow what I'm saying). We can be pretty certain at 33 bits that we're not going to have clashes in session IDs. I'm almost entirely certain of that.

-- psyche, STT, 2026-10-07.

## Stored type and datom representation; shorthands; the flow id as three words
Context: comment on "FlowId" in the registry record, section 2 «The registry is Flow's Memory».

> I know I said I want to focus on bringing Flow Nexus to production and this would probably slow things down quite a bit but this is who I am. Perfectionism does slow down a lot of things but here it is.
>
> Certain concepts, I guess you could call them, or certain types in ethos, will have to have a different representation than how they're stored in the runtime. For example the SHA-256 is a good example. I've seen another presentation in which the SHA-256, which is really a 256-bit number, is said to be a string.
>
> Now I understand what the machine is trying to convey in terms of the fact that when we handle this SHA-256 in datom in text form, it's a string. Everything basically is a string. It would kind of be absurd to say that now integers are strings and enums are strings just because they have a string representation. Although, like I said, I do understand the reasoning or the practical reasons behind this, we need some kind of abstraction there. When we go from datom representation into an in-memory type, there's a conversion that happens and this touches the flow ID as well. You could represent certain things differently, not represent them, but they would have different methods.
>
> The shorthand concept ties into this, where you get a certain kind of query or response that is the full-size, fully explicit, advanced expert version that has all the parameters. You have the shortened version that only contains the bits that matter for the particular use case in which these shorthands are being used, namely in the thinking machine context most of the time.
>
> For example messaging doesn't require knowing its flow ID at all. In fact it would be bad practice to try to send to a flow ID because the sender doesn't know if that is the current flow of that voice. I guess you could have a subflow. Research this thoroughly.
>
> Can subflows use subflows themselves? It would be interesting to allow a subflow to use another subflow to populate its context at the middle stratum using the messenger. I don't know because the messenger has this registration process that probably would slow things down. I'm going all over the place now.
>
> The flow ID needs to be represented with this. We decided on three words and I think it's probably wise because in LLM terms it's fairly cheap for the amount of entropy that we get. This three-word camel case format conversion, and the same thing with the [SHA-256], is sort of like some kind of base 32 or whatever it is that they're using, into an actual 256-bit whatever or a vector of bytes. I don't know how these things are represented. I think a vector of bytes is going to be the type that is in memory, whereas when it's back out into datom, it's going to be in this alphanumeric encoding and this concept is probably going to come back and be used in other places as well.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07. Transcription corrected: "shot 256" → "SHA-256".

## A checked bridge between JSON and datom, adaptable to other formats
> And if we make the tool that can translate [JSON] to Datom and vice versa with the actual specified ethos (checking, back-checking whenever it goes in or out, type-checking it through the [rest of the] infrastructure), then we could use Datom with our [Clojure] tools, which would be really cool. And if we design it well it would be really easy to adapt it to other things like [Cap'n Proto]. I'm guessing [Clojure] has [Cap'n Proto]. I think everything does. I think Java has it so [Clojure] automatically can get it. That would be: if we create the right abstraction then we can adapt it to different data formats.

-- psyche, STT, 2026-10-08. Transcription corrected: "JavaScript" → "JSON"; "REST infrastructure" → "rest of the infrastructure"; "Closure" → "Clojure"; "Cap and Proto" → "Cap'n Proto". The first two corrections are inferred from the conversation (the JSON bridge); not confirmed by him.
