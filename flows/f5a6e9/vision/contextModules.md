# Context modules

## The Nexus uses a registry keyed by subaspect and topic, storing each module's containing source with its hash and relative path; the registry payloads live on the meta signal; the vision files live at psyche-skills/vision/<topic>.md

Context: his comment on «The golden ethos», third edition, 2026-10-09 20:07, on the line naming psyche-skills/skills/vision-ethos.md; relayed by Psyche Fable d5df1d (Ethos), who asks that the registry and file-location parts reach the Flow topic. The inline-import syntax in it is the Ethos topic's.

> should be psyche-skills/vision/ethos.md
>
> tell astra to adjust all the files and the code. the file location shouldnt matter from the nexus' pov; it must use a registry which uses the `{ Subaspect.[Vision Knowledge ...] Topic:Name }` to store the location of each, using the containing source with hash (blake3 I believe is what we use?) and relative path of each. those payloads live on the meta signal (to modify those registries). curriculum can have the capacity to get/check the hash when the query come in, according to the operation (write or read).
>
> Notice I used a new syntax there that I also want to bring into the table of ethos design. I want to talk about how this will be implemented, but I also have more ideas for more ethos improvements.
>
> This is another form where a type can be declared, and it means that we're doing an inline import. If it starts with a capital letter, then it means it's pulling directly from the core built-ins. `name` would be one of the built-ins in the core of the language, which would be declared in the core library. We need a whole registry for all this: all of the manifests for where all the different libraries live.
>
> Otherwise, if it starts with a small letter, then that means it's pulling in from the registry name. This sort of depends on the isos environment that's loaded, right? There's going to be a registry for those as well.
>
> This is a rather big improvement or change in Etho, so I want to make sure it's done well with a full Opus and Fable topic flow on that. I need to know where we are with starting the new topic flows. Do they exist? Oh wow, they do. Bravo! Oh my god, let's... I'm going to go, and I guess you'll pass all of the relevant stuff to the metaflow that is taking care of ethos and flow and nexus, whatever, whenever their topic is right. I'm going to alternate between you guys. Wow, this is brilliant. Oh my god, let's get to work.

-- psyche, typed, book comment, relayed by d5df1d.
