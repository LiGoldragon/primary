# Ethos — raw vision heard by 081064

## 2026-10-10 — the registry, its anatomy and population

Context: comment on «Sources and the registry», proposal 2 (a lowercase source names a registry entry); relayed by 23824a.

> Yes this is good and now we need to define the anatomy of that registry and use the same atomically updatable approach. The registry can be populated from multiple sources using the datom files that can be in the repositories that essentially wrap all of the data in that particular repository and can be updated by whoever updates that repo. It can then be loaded along with other repositories to create a full registry.
>
> In Ethos do we have an Ethos Nexus or is Ethos Zero a non-Nexus? We need to migrate the Ethos Nexus version so that we can do this. In Ethos I want to specify the three aspects:
> - the signal
> - the memory
> - the operation
>
> For one or another we can do Ethos now so that would go with the Ethos flow, the eco psyche flow [sic] design to design the ethos of all three parts of the Ethos Nexus. This will be used to put together a registry and it'll just keep it. Every time we update some Ethos source, add one, or edit its name or something, we need to change the registry.

-- psyche, STT, 2026-10-10, relayed by 23824a.

## 2026-10-10 — a shared sources library for ethos and curriculum

Context: same book, section "What the hash covers"; relayed by 23824a.

> We can create a shared library between them, which is about sources, and it can even have objects for memory to store a registry of sources. That way the skill doesn't have a registry for each skill that doesn't need to be updated because it refers by name to the source. Only the source content addressing registry needs to be updated.

-- psyche, STT, 2026-10-10, relayed by 23824a.

## 2026-10-10 — uncapitalized names in Protos languages: the prototype name

Context: same book, section "What the key reaches: names"; relayed by 23824a.

> In Protos languages like datom and [Ethos] for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants. If there's a string position in datom and it starts with a capital, that's okay because we have a different type that's kind of like a string but it has to be checked whenever we create a new one. This is the Prototypic name or whatever, the prototype name, which is an uncapitalized identifier. It's going to have to be composed of words so we need to put together some kind of fancy check. Well not that fancy, I guess.

-- psyche, STT, 2026-10-10, relayed by 23824a. Transcription corrected by the relay: "[Ethos]".

## 2026-10-10 — the inline import, D1

Context: comment on «The inline import, third edition», D1 (the vision statement for `Topic.custom:Name`); relayed by 23824a.

> Yes this is good.

-- psyche, STT, 2026-10-10, relayed by 23824a.

## 2026-10-10 — the inline import is not blocking

Context: spoken to the core Secondary 445410, on the inline import; relayed by 23824a.

> The inline import, we don't have to worry too much about it for now. It's just a nice thing that I thought about and let's not block on it right now.

-- psyche, STT, 2026-10-10, relayed by 23824a.

## 2026-10-10 — a Nexus called sources

Context: comment on «Sources and the registry», heading «What the registry must say», anchored on «One registry type, serving both the libraries named by a source and the vision and knowledge files keyed by subaspect…» (question 2, option a); relayed by 23824a.

> This is actually really interesting. We could just make a registry or sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. We have different registries in fact. Eventually when we cut off Git, we don't need to keep the Git equivalence registry because it's different and some sources don't necessarily need to have it, right?
>
> We can have different types of backend fetchers. Basically we have this concept: we can get it from Git or we can get it from a local path on a certain host and we have the hash, right? Even the local path on the host is not dangerous. We would use a technique similar to Nix in that we wouldn't, obviously, include the Git subdirectory in the data, right? It would be the snapshot of that revision that we hash, kind of like how Nix does.

-- psyche, STT, 2026-10-10, relayed by 23824a.

## 2026-10-10 — one source nexus for all components

Context: same book and heading, anchored on «Two registry types: one for libraries, one for vision and knowledge files.» (question 2, option b); relayed by 23824a.

> There's some mix-up here: vision and knowledge. I guess you mean skills or context modules for the curriculum.
>
> Like I said in my other comment, we can have a source. Essentially we're adapting to the language. If I say, "Go get a source," then eventually you'll automatically know that I mean: use the source nexus and send it a source request and then you'll get a source. It's called the source nexus so let's get that designed too.
>
> I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect.

-- psyche, STT, 2026-10-10, relayed by 23824a.

## 2026-10-10 — provenance correction

Each of the seven entries above dated 2026-10-10 and marked "STT" is typed: they are the living's comments on the published book «Sources and the registry» and «The inline import, third edition», recorded typed by d68c82, which relayed them. The relay envelopes carried no input mode; "STT" was an assumption. Read every provenance line above as `-- psyche, typed, 2026-10-10, relayed by 23824a.`

