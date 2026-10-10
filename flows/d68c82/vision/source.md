# Source

## A nexus called Source

Context: said after commenting on the «Sources and the registry» book in «Open books»; the concepts themselves are in his comments there.

> I did advance some concepts on how we can get sources from a particular nexus called Source that we would design.

-- psyche, STT, 2026-10-10.

## The registry: its anatomy, populated from datom files in each repository

Context: comment on «Sources and the registry», proposal 2 (a lowercase source names a registry entry), 15:22.

> Yes this is good and now we need to define the anatomy of that registry and use the same atomically updatable approach. The registry can be populated from multiple sources using the datom files that can be in the repositories that essentially wrap all of the data in that particular repository and can be updated by whoever updates that repo. It can then be loaded along with other repositories to create a full registry.
> ... This will be used to put together a registry and it'll just keep it. Every time we update some Ethos source, add one, or edit its name or something, we need to change the registry.

-- psyche, typed.

## The hash verifies the files; a smart store comes later

Context: same thread, 15:22.

> Also we could use the content hashes maybe. Maybe we need this hash-based storage. I think I had a thing called Logic Store but we could just move it to something more straightforward like a file store, an archive, or a file archive or something. It would be a nexus where we can put these hash-addressed files. Actually never mind all this. The hash is there for us so that we can verify that the files are the right files when we use them. That's all.

> For now we can just check the files. Later on we can have a store dedicated for this that will be smart enough to know what to store and what not to store, and how or where to get it (if it has to just use a Git backend to fetch a particular request) so that we don't double-store if we're already storing it in Git (like some kind of smart system). This is not the first lane. This is not the priority lane.

-- psyche, typed.

## The hash covers the whole repository; one shared sources library for ethos and curriculum

Context: «Sources and the registry», proposal 3, "What the hash covers", 15:27.

> Since we're going to use repos, we're going to hash the whole thing. It's got lights like Nix [sic], right? When the source changes, the source changes. That's why we don't put non-Rust things in the Rust repo, because if we want to change any of it, then Nix has to recompile.
>
> Since the skills are in repos, if we're talking about curriculum, we should have a list of sources. ... It's the same concept for curriculum.
>
> We can create a shared library between them, which is about sources, and it can even have objects for memory to store a registry of sources. That way the skill doesn't have a registry for each skill that doesn't need to be updated because it refers by name to the source. Only the source content addressing registry needs to be updated.

-- psyche, typed.

## A Source nexus: Git at a revision, own Blake3 hashes, several registries, backend fetchers

Context: «Sources and the registry», proposal 3, "How many", 15:30.

> This is actually really interesting. We could just make a registry [of] sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. We have different registries in fact. Eventually when we cut off Git, we don't need to keep the Git equivalence registry because it's different and some sources don't necessarily need to have it, right?
>
> We can have different types of backend fetchers. Basically we have this concept: we can get it from Git or we can get it from a local path on a certain host and we have the hash, right? Even the local path on the host is not dangerous. We would use a technique similar to Nix in that we wouldn't, obviously, include the Git subdirectory in the data, right? It would be the snapshot of that revision that we hash, kind of like how Nix does.

-- psyche, typed. Transcription corrected: "registry or sources" → "registry of sources".

## One Source nexus for all components; "get a source" means a source request to it

Context: «Sources and the registry», proposal 3, "How many", choice b, 15:31.

> There's some mix-up here: vision and knowledge. I guess you mean skills or context modules for the curriculum.
>
> ... we can have a source. Essentially we're adapting to the language. If I say, "Go get a source," then eventually you'll automatically know that I mean: use the source nexus and send it a source request and then you'll get a source. It's called the source nexus ...
>
> I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect.

-- psyche, typed.
