
## Correctness by layers; control through the meta socket

2026-10-25, to Psyche core Secondary 36ac89. Context: answering the book "A restriction nobody designed" (flows/63a06a/books/flow-inband-control), whose case is that Flow 0.39 refreshes a session only from inside its own turn.

> the correctness of the system that we're going to create is not going to be baked into a giant monolith. It's going to be done by layers. The control mechanism for who can restart a flow and stuff like that is going to be controlled by who can access the socket, the meta socket.
>
> Right now it's like a full permission system. Even the dumbest model in the world could use my credentials that it has access to to destroy my life. It's fully unsecured. There's no security in the system right now. I'm just trusting that machines aren't delirious enough to push the [nuke] button randomly and that they would even be smart enough to question a message that ordered them to do it.
>
> All of these attempts to try and [bake in] the security, with really bad architecture like this, are a misunderstanding of what I'm trying to build.

Transcription corrected: "new" → "nuke"; "break into" → "bake in".
