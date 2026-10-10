# Context modules

## The whole context modules concept, at the intent level
Context: his comments on the second edition of the Flow book; the book left out context modules.

> A few things: the whole context modules concept has been completely omitted in the book, which is troubling. It means that the machine is almost completely missing my design. It seems that that part of my design has completely gone undervalued and underappreciated. It's extremely important because we have to put this at the top level, at the intent level.
>
> We have to create a system whereby complex actions can be accomplished by a machine with minimal effort, with minimal amounts of output tokens. This means that as much of the context as possible has to be modularized so that we can call a 100,000-token context with 100 or 200 tokens by just naming the modules. With a dependency system maybe only 7 modules are mentioned but 37 of them are loaded because of a dependency chain. There's going to be a whole system developed around that.
>
> It's a very major, huge, massive, super important part of the design. The fact that the whole book missed it is extremely troubling to me so I'm quite vexed at this.

-- psyche, STT, 2026-10-07.

## The brief is small; 95% of the context comes from modules
Context: comment on the launch/refresh/end figure, section 3 «Launch, refresh, end».

> Well now I just realized you never even specified the whole context module aspect of things. Obviously there's going to be a placement for that prompt, that brief, which is essentially the first task of that flow. Yes there is a brief although probably 95%+ of the context that we feed it will come from modules. The brief should be actually fairly small, like a small paragraph at most. We want to be able to start a flow with minimal cost to the calling model, which means that we need 100:1 or 1,000:1 leverage in terms of token output cost to the calling model versus the amount of context that's going to go into that flow.

-- psyche, comment on «Flow and Message» 2nd edition (https://claude.ai/artifact/Tpf6nJzyu5jpkRpogQLFb5), 2026-10-07.
