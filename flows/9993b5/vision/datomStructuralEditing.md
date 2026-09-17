# Datom structural editing

## We are going to create this language to edit through our own CLI, the right tool; oh my god, it just works with Datom, and it is a super efficient way of editing, a really really smart way of editing; what is the smartest way of editing text? if you are just going to append, that is easy, and there is an append already spec'd out, but what else is there? depends on the object type; if it is a Datom object, we can almost just structurally edit it based on the structure — you can add an item to a vector, or change the type of something, maybe even with a new structure; crazy, right?

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the shared-workspace and auto-commit-on-write visions (sharedWorkspace.md, autoCommitOnWrite.md, same date). Names the shape of the "right tool" for editing files that is not string-replace and not line-diff: a datom-native structural editor exposed as a CLI, whose edit operations are themselves datom values so they compose and reason. Pairs with the auto-commit-on-write vision: each structural edit is one CLI invocation, one file write, one commit. The rhetorical question at the end ("crazy, right?") invites this flow's engagement with the design — answered in the reply, not treated as a decision. Related to the datom vision generally (positional, typed, no field names; kinds carried by types) and to the ethos vision (structure is what the reader walks). Logged by the main flow before acting.

> We're going to create this language to edit through our own CLI, the right tool. Oh my god, it just works with Datom, and it's a super efficient way of editing, a really, really smart way of editing.
>
> What's the smartest way of editing text? If you're just going to append, that's easy, right? There's an append already spec'd out, but what else is there? Depends on the object type, right? If it's a Datom object, we can almost just structurally edit it based on the structure. You can add an item to a vector, or change the type of something, maybe even with a new structure. Crazy, right?

-- psyche, typed.
