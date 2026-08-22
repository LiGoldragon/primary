# "That's what enumerators are"

## 2026-08-07T18:47:12.105Z — "That's what enumerators are"

> The main objects that I've been emphasizing, because we're talking
> about creating an interface, is the root input objects and perhaps
> even a lot of the root output objects should be enumerators because
> if you're trying to create a language, an input and output language,
> you want to create like branches. That's what enumerators are.
> They're like, here's a category and here's all the different
> subcategories and then these usually carry data, each of them. And
> if it's an elaborate language, then you have more enums down that
> and that creates a nice interface for input and output. You can look
> at the spirit that, you know, the production spirit, which used the
> old schema language, might give you an idea.

— psyche, 2026-08-07T18:47:12.105Z (Designer session d63804f2)

Context (agent-authored, separate from the quote): this entry is the
root input/output enumerator ruling from the 2026-08-07 observer-interface
review. The same prompt also discussed stream and newtype concerns;
those belong to their topic logs. The production Spirit reference is
kept here because it directly identifies the old schema-language
interface as the model for this branching form. Source evidence: the
Designer transcript record for user message d061c084-0359-43db-b5d5-93d8e5527a52.

## 2026-08-22 — no derive for cli config: datom creates configuration options by its very shape; a data enum at the root (main operation) with options in its data

Design session `bc05da32`, typed (captured 2026-08-22), answering the
Designer's proposed datom-config derive crate for the program input
and the argv-derive family (clap derive, argh) it was modeled on:

> there is no production lexer yet, its still in development.

> and I dont think we need a derive on a datom type for what we want.
> its simpler than that; datom creates configuration options by its
> very shape, as the ethos interface shows; a data enum at the root
> (main operation) with options in its data

Context (agent-authored, separate from the psyche's words): the
datom-config derive idea is dead. The program's configuration
surface is the datom's shape as the ethos interface declares it —
the root data enum's variants are the main operations, each
variant's data its options; nothing generates a UI because the
shape already is one. Extends the 2026-08-07 root-enumerator ruling
above. The first line answers the Designer's "realize it through
the project's datom parser": the parser is still in development —
the design is written ahead of what can run, per
worldModelBeforeCode.md 2026-08-21.
