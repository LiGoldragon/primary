# Proposal and book

Created by Fable.

Source for the book metaflow. Markers: [-removed-] is a passage removed, shown highlighted red in ordinary type; [+added+] is a passage added, shown green; [~moved from <module>: ...~] is a passage that enters this module from another, shown blue, naming the module it leaves. Everything unmarked stands as it is. Each section is shown whole, as it would stand.

## psyche-belief › vision/proposal.md — section "A proposal", changed

Why: he reads a proposal as the sections it changes, and its own words are few; the rendering of those changes belongs to the book module, so only what a proposal is made of is said here.

[-A proposal is the prose and the code that describe the system.-]

[+A proposal is the sections of belief it changes, each shown whole as it would stand; a module is shown whole when he asks for it, or when the module is new.+]

[~moved from vision/book.md: A proposal's own words are its title, its subtitles naming the module and the kind of change, and a short comment on why each change is made.~]

A proposal is a proposal into belief modules, and the whole of it is its crystallization: what it removes and what it adds.

A proposal that touches a code component shows the code it changes or adds.

A code block in a proposal stands on its own: it is shown without a path, directory or file name. It carries the code, why it is important, and what its function is.

A proposal is usually drawn as well as written, and always when it has a shape: what it adds, removes and keeps, in one frame.

The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.

The proposal is the center of development: it is the evolution of an idea.

A [-line-][+passage+] removed from a module is shown beside the [-line-][+statement+] that makes it unnecessary; the compensation module is leaned out first, because vision replaces it.

A question between alternative [-lines-][+statements+] shows each alternative as its own proposal, with the exact [-lines-][+statements+] it lands; the living rules land, amend or reject.

Every word of his redoes the proposal it bears on, unless it closes the topic; words that open a topic of their own get a proposal of their own.

A proposal in the chat [+opens with the module's name and+] shows the whole section as it would stand, with the part that changes in bold.

## psyche-belief › vision/book.md — section "What a book shows", changed

Why: the book module keeps only how a change is rendered; what a proposal says of its own leaves for the proposal module; a removed passage is read more easily highlighted than struck; a moved passage is read once, at its destination, instead of being assembled from a red block and a green one.

A book is belief modules in the forms below, each under its repo › path[-; its headings, naming the module and the kind of change, are the only words it has of its own-].

[-A module shown whole, as it stands, situates the landing.-]

A module shown beside another, both as they stand, serves comparison: psyche with knowledge, with compensation.

A [-line-][+passage+] added shows [+highlighted+] in green.

A [-line-][+passage+] removed shows [+highlighted+] in red[+, in ordinary type+].

A [-line-][+passage+] replaced shows its removal and its addition together, and only the changed words are marked.

A new module shows whole in green, under the path it will have.

A module deleted shows whole in red, with a Destroy or Archive mark.

[-A line moved between modules is one proposal headed by both paths: the line in red under the module it leaves, the same line in green under the module it enters.-]

[+A passage moved between modules shows once, highlighted in blue under the module it enters, naming the module it leaves; words changed in the move are marked red and green inside it.+]

A dependency changed shows in the module's front matter: the dependency removed in red, the dependency added in green.

A figure shows as proposed for the module it will live in.

A figure proposed for a module shows under that module's path in green, as an added [-line-][+passage+] does; a figure it replaces shows beside it in red.

## psyche-belief › vision/crystallization.md — section "Crystallization", two statements changed

Why: "from his quoted words alone" pulled the flows toward his sentences verbatim, where he meant the statement to carry his meaning and the record to keep his words.

A crystallized statement stands on its own words. A proposed change to a raw record — correction included — is proposed as a crystallization of its subject.

[-A statement is composed from the living's quoted words alone.-] [+A statement says what he means; his words are its record, kept whole.+] Every term in a crystallized statement is defined. Define the term first, or leave the statement raw.

## psyche-belief › vision/remembering.md — section "A flow is started with a remembering", one variant added

Why: his words this morning: a launch may name a size instead of a depth or a list; Flow walks the predecessors newest first, one at a time, taking each one's open records until the size is filled, and all of them when it never fills; a predecessor in which he said nothing contributes nothing. Landing archives records, so a flow that remembers by size reaches past the crystallized layer into what was left behind, and catching up on crystallization is what shortens the remembering.

A launch names how far back the new flow remembers: the raw vision and notion logs of its predecessors to a depth, [+to a size,+] or of flows named one by one. The remembering is a field of the launch; the belief modules come from the declaration, from main; the brief comes last and carries the task alone. The logs are the record.

[+A remembering by size walks the predecessors newest first, one at a time, and takes each one's open raw records until the size is filled; when the walk reaches the first predecessor before the size fills, it takes everything there was.+]

```
RememberingDepth.Integer
[+RememberingSize.Integer                                   ; tokens+]
Remembering.[ Predecessors.RememberingDepth [+Size.RememberingSize+] Custom.Vector<FlowId> ]
Launch.{ Address Remembering InstructionPrompt }
```

```
flow 'Launch.{ { Psyche core Primary } Predecessors.2 «brief» }'
[+flow 'Launch.{ { Psyche core Primary } Size.40000 «brief» }'+]
flow 'Launch.{ { Psyche core Primary } Custom.[ 36b71b e3c8c1 ] «brief» }'
```
