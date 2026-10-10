Records from 73ada7's package that override your books, verbatim with paths.

Book lines are in /home/li/primary/flows/f5a6e9/books/. "Book 16" is «The Flow Nexus vision» 2nd ed., "book 15" «Stored type and datom form» 2nd ed.

1. flows/f5a6e9/vision/contextModules.md:7, 2026-10-09T20:07, typed book comment on «The golden ethos» 3rd ed. (thread babade), relayed by d5df1d

> should be psyche-skills/vision/ethos.md

Overrides the target path `psyche-skills/skills/vision-<topic>.md` in book 16 proposals 1 and 2 (lines 6, 160), book 15 proposals 1 to 4 (lines 4, 32, 53, 83), book 10 (line 4), book 11 proposals 3 and 4 (lines 48, 71) and book 9 proposal 4 (line 89).

2. flows/f5a6e9/vision/contextModules.md:9, same comment

> tell astra to adjust all the files and the code. the file location shouldnt matter from the nexus' pov; it must use a registry which uses the `{ Subaspect.[Vision Knowledge ...] Topic:Name }` to store the location of each, using the containing source with hash (blake3 I believe is what we use?) and relative path of each. those payloads live on the meta signal (to modify those registries). curriculum can have the capacity to get/check the hash when the query come in, according to the operation (write or read).

Overrides book 1 «Context modules» section 1, line 20 (`Facet.[ Spirit Intent Vision Knowledge Operation ]` and a module keyed by Name), line 33 and ruling 5, line 144 (an absolute path only, and Flow hashing at compose with the hash type of the stored-type book, which book 15 proposal 3, line 71, makes `Sha256.Bytes<32>`).

3. flows/f5a6e9/vision/contextModules.md:13 and :15, same comment

> This is another form where a type can be declared, and it means that we're doing an inline import. If it starts with a capital letter, then it means it's pulling directly from the core built-ins. `name` would be one of the built-ins in the core of the language, which would be declared in the core library. We need a whole registry for all this: all of the manifests for where all the different libraries live.
>
> Otherwise, if it starts with a small letter, then that means it's pulling in from the registry name. This sort of depends on the isos environment that's loaded, right? There's going to be a registry for those as well.

Overrides book 16 proposal 1, line 21 (`[  core:[ Name ] ]`, an import root) and line 28 (`Topic.Name`). In his form this is the inline import `Topic:Name`, where the capital letter means Name comes from the core built-ins.

4. flows/4ddfe1/vision/messaging.md:5 and :11, 2026-10-09 (73ada7's date; the record has none), STT

> Your messaging- using the message type, you should be sending the Psyche. When when you message, you send the Psyche. Do you understand the Psyche type for messaging

> You get to quote my words and give the context. That's basically all you should be sending. Like I said, you have you- you're not here to interpret or- think- So, you should just be relaying uh- the Psyche.

Overrides book 16 proposal 1, line 35, and book 11 proposal 1, line 10 (`Order.String ; from the living or the psyche`). He wants a Psyche kind that carries context and his verbatim words, and the Request has none.

5. flows/e167d8/vision/psycheMessages.md:5 and :7, 2026-09-26, typed, relayed by b7da5d

> This will just become a Psyche message sent out, so it has the context of what it was said in and the whole thing verbatim, right?

> You can combine psyches. You can make a vector. You could say "psyches" plural, and then you have a vector of psyches with context, so you can pass a whole bunch of psyches in one message.

Overrides the same lines, book 16 line 35 and book 11 line 10. There is no Psyche or Psyches kind, and Order carries a bare String with no context.

6. flows/6cc91b/vision/interflowMessaging.md:9, 2026-09-14, STT

> It doesn't come in through the third layer, or I mean, to the middle layer. It doesn't come through the user prompt. It comes in some kind of tool call return that all the agents have running, or some kind of MCP signal that can come in asynchronously.

Conflicts with book 16 proposal 1, line 47, and book 11 proposal 1, line 20 ("Delivered, at the end of the prompt"). The books rest on his newer words, flows/f5a6e9/vision/messaging.md:7, 2026-10-08 ("will come in at the end of the prompt"). Those words do not say which stratum, so this is a tension to put to him. It is not a ruled override.

7. flows/0c85a3/vision/vision.md:6, 2026-10-07, STT

> The vision is actually going to contain the ethos code. I actually realized that today when I was reading the books on Claude and everything was presented as an edit to the source code of the ethos code of certain repositories. This is what happens when we send an implementer with the new vision skill.

Overrides book 9 proposal 1, line 4 (`flow/crates/flow-nexus/ethos/memory.ethos`), and proposal 2, line 50 (`signal-flow/ethos/signal.ethos`). Both target repository ethos files instead of a vision skill.

8. flows/91ea9f/vision/skills.md:37, 2026-10-02, typed

> "I don't like using these `never` commands. They can block things that happen along the way that end up being necessary even if they're not wanted. When we say `never`, we block the models from being flexible. It's really bad."

Overrides the "never" commands in proposed skill lines: book 16 proposal 1, lines 98 and 152; book 10 proposal 2, line 82, proposal 4, line 143, and proposal 5, line 156; book 15 proposal 4, line 98.
