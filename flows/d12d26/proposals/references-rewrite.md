Records drawn on by A full rewrite:

flows/9abe63/vision/committing.md (2026-10-30):

> And we won't always be able to rename a component when we rewrite it from scratch so we need a protocol or method to talk about full rewrites. Maybe it's like these full version numbers. Flow version 1 would be a full rewrite of Flow version 0 and the two would not in any way. We can use the same repo but we would start the version 1 branch as a fork from the initial commit on a completely empty repository. We would create a new commit on top of the first one that just deletes all the code. Maybe there's one line in there that's still relevant but that's not my point. My point is that we would start from scratch basically.

flows/d12d26/vision/committing.md (2026-10-30):

> The full rewrite new version concept is not a committing concept. How many hundreds of times a day are we going to do a full rewrite from scratch? You're making the committer understand something that will happen once in a long time.
>
> This is a module that would rarely be loaded and that certainly wouldn't be called committing. We'd be very explicit about the fact that the Git example is an example.
>
> Why is the example using Git and not Jujitsu? Is it because Jujitsu would be unable to do this or do you think I'm wasting my time trying to use Jujitsu? Please don't be sycophantic here and don't give me an ignorant answer based on a context that has done no investigation into the matter.

Jujutsu example: witnessed 2026-10-30, `jj new root()` then `jj bookmark create v1`.
