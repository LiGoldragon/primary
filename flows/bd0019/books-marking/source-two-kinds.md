```yaml
title: Two kinds of output
```

## Two kinds of output

1. **Everything a machine says is one of two things.** Either it is addressed to you, in prose, as a presentation, or it is machine output: a result, an error, an unexpected outcome, one condensed line each, no progress, no commentary, no restating of your question. There is no third kind. You said it plainly: "if we keep everything else that the machine says to a more mechanical logging-like behavior, then it'll be obvious when it's actually talking in prose and talking to me." (STT, 1 October)

2. **The living-directed block is wrapped, and the wrapping does not render.** It sits between `<!-- to-the-living:start -->` and `<!-- to-the-living:end -->`, each on a line of its own, Astra's instinct, which you chose over a visible pair: "I don't need to be able to see them in the chat ... If it doesn't render it then there might be an advantage to that. Astra's vision is better." (STT, 1 October) A quoted marker stays inline so no tool mistakes it for a boundary. The markers stay even when metadata is present: "I'm not taking out the markers here." (STT, 1 October)

3. **The block opens with its metadata, and only there.** Just inside the start marker, a fenced block carries what the book needs but must not show, today only the title of the book the block belongs to. Nothing says who sent it, "because we know from which transcript we're getting it from" (STT, 1 October), and nothing says whether the book is new or edited, since the seat cannot know that; Sonnet, which holds the list of what it has published, decides by title and seat. The metadata sits at the beginning and nowhere else.

4. **Not every reply is a block.** A conversational answer carries no markers and no metadata; the wrapping is for a presentation meant to become a book or to change one: "the blocks that are intended to be either turned into a book, updated, or changed in an already existing one." (STT, 1 October) A hook on each harness reads the finished reply, cuts out the wrapped blocks and sends them to Sonnet, so the seat spends no tool call and nothing polls. Eventually the machine output outside the block becomes system logging, "notifying us of errors, unexpected outcomes or results." (STT, 1 October)

## Open

- The metadata block as a fenced `yaml` block, as here, or as dashed front matter.
- Who builds the hook: proposed Field Astra, with Mind Sol witnessing one reply on each harness.