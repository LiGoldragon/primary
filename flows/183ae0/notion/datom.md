# Datom

## A datom payload from multiple places

> The big question that this just brought up in my mind is designing a way to deal with a datom payload that comes from multiple places. Imagine you have a manifest or a kind of manifest or registry or something like that sitting in the repo where the skills are, and then you have the CLI's actual datom that we pass to it. Because the Nexus doesn't speak datom, we can't just send him the path to a datom file.
>
> There are two complexities here:
> - Call time complexity
> - Background infrastructure complexity
>
> I think maybe there's variance in between but in one version we find a way for datom to be able to use a path in some places instead of the actual payload (so that it can just insert the payload of that datom in that spot). Now that I say it out loud, it doesn't sound so complicated but it does because then there's the problem of how we know what it is. I guess you would have some kind of special reader character. It's a fairly deep modification of the datom language. Not necessarily the worst approach but I don't think it's very pure. Using paths is very setup-dependent so it's not a very good idea for a system that wants to be correct.
>
> The other way is to simply not use it. Conceptually you would have the datom file there and next to it would be the compiled signal file so that then the Nexus could load it because it's already signal.

Context: arose from the anatomy of the Curriculum Nexus taking typed skills from skill repos.

-- psyche, typed.
