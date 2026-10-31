# Translator

## 2026-10-31 — The translator: a socket for signal and one for datom; requests wrap the type, the outgoing ones saying where the text goes
Context: the living, in the Psyche core Primary chat a78e9a, opening the design of the translator Nexus.

Let's design the translator. It has, I guess, a socket for signal and a socket for datom so it can go both ways. It has different types of requests that will wrap the type that it has to translate, especially, I think, maybe not coming in but coming out, so that we know if it's going into a file descriptor or if it's composing a particular kind of system call (which begs the question, I guess, which process is going to start that subprocess). Show me how you would design that. Show me some ethos: an example datum coming in and out.
