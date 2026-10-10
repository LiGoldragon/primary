# Terminal cell

## 2026-09-14 — A Herder backend for now; Terminal Cell as an experimental library; reconsider the forked actor library

Context: comment on the gap "terminal-cell and forge have no psyche statement". Contains questions the flow is to answer: what Herder is here, whether abduco is better, which actor library was forked (Cameo as written), and what changed upstream.

> Well, for now, it might be smarter to use Herder. Maybe the terminal component is our language and /Nexus, right? When you create a Nexus, you basically create a language with a certain logic that is going to be the terminal component, and so you use a terminal-based language to port to Herder.
>
> We can have a Herder backend for now and an experimental Terminal Cell library. Terminal Cell is maybe more of a library for creating a super efficient kind of abduco. Is Abduco better? We want to be able to inject messages, and it has its own process actor, I guess. Do we want to create our own process actor library that calls Reactor? No, what is the latest actor library that we're using that we forked? Let's look at the current seed in the actor library scene.
>
> Maybe there's a new prodigy and what has changed because we forked Cameo. Now we need to reconsider what in our fork is maybe unnecessary from changes on master and our main, and if we should report some of it or rethink what we've done before according to the new code.

-- psyche, typed, artifact comment.
