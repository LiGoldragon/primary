# Rust

## Freestanding implementations are forbidden; all implementations must be of a trait

Context: artifact comment on the recap's "pieces, in protos" Rust block, which had `impl Form { … }` (2026-08-31 11:26).

> Two things:
> 1. I'm trying to understand why you're presenting this to me in Rust code. I'm not saying there's no reason. I'm just puzzled, especially because you prefaced this block by saying the piece is in Protos. You mean in Rust.
> 2. You've used an implementation block that is not implementing a trait, and that is forbidden. We forbid freestanding implementations. All implementations must be of a trait.
>
> What's going on here, and why did this happen? What's the goal? Why are we writing Rust that we're not even allowing to be written?

-- psyche, typed (artifact comment).

## Generated Rust uses fully qualified names; Rust as an assembly language, explicit, correct over sweet

Context: artifact comment on a mermaid node reading `Context: Kinds` (2026-08-31 11:22).

> Like I said earlier, I think we could be more explicit about the context. In this case, the context would be `ethos`. We could use the import syntax because I also want to make this clear: when we generate Rust, the generated Rust would just use fully qualified names, so it would be `ethos::kinds` and not just `kinds`. That is because we're using Rust the way we intend to use it, which is more like an assembly language, which is extremely explicit and doesn't leave room for... We're not concerned about making it look sweet. We're concerned about it being correct.
>
> Even in our examples, just to be clear about what we're talking about, it doesn't have to be `ethos::kinds`. In this case, it could just be that the graph itself is titled `ethos` or `ethos declaration` or something like that. Just `ethos` would be enough, I think.

-- psyche, typed (artifact comment).

## Free functions despised; inlined lambdas despised even more

> I really despise free functions, and I despise these inlined lambdas even more. Whenever I see that, to me, that smells of bullshit and ugly design.

-- psyche, STT.
