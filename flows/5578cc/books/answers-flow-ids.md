<!-- to-the-living:start -->
Presentation.{ «Your answers on Flow ids in words, and what follows» }

# Your answers on Flow ids in words, and what follows

You commented on «Flow ids in words, and seats launched by Flow». Here is each comment and what follows from it.

## The words

> This looks perfect. That's exactly the user interface I was looking for.

Three words joined in camelCase, like `abandonAbilityAble`, are the id's form.

> This should go into a library that all components can reuse, so maybe some kind of Ethos core library or Ethos standard or something. This might mean needing to develop the way ethos is put together, like manifest, registry, index: where do dependencies, libraries, etc., come from? Let's get Fable to ask me some questions about that and then with the answers he can start on a new flow and design something.

Fable asked you those questions in «Questions on the Ethos library». The word-id code goes into that shared library once its shape is decided.

## Which bits become words

> Well it seems to me that the first 33 bits of the actual ID we were using from the harness's ID is what we're using and then converting it into words because then we can go back. Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words. Is there anything that doesn't work with that in practice?

**It works.** Words turn back into the same 33 bits, and a tool finds the transcripts whose session id holds those bits.

Two details:
- **Codex.** A Codex session id begins with a timestamp, so its bits are taken from its random end. Today's six-character ids already do this, and that was confirmed today.
- **Two flows sharing 33 bits.** This is very unlikely (about one in 160 after ten thousand flows). Flow checks at launch and adds a fourth word if it ever happens.

The unmerged word converter turns a fingerprint into words, which cannot be turned back. It will be changed to write the id's own bits.

## The title and the registries

> Like I said to some other Flow or in the comment, I want it to be: now the model is replaced by the layer so this would be psyche secondary and then the ID is replaced. Well it's still the ID but it's a word ID.

> There are two registries:
> - The true registry with the actual IDs
> - Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice, the current flow for that voice
>
> The syntax would be `psyche.primary` because it only has one. It's like a single-field data-carrying variant, right? We don't need the struct braces. It's kind of like a data-carrying variant that holds a variant essentially.

**The pane title.** It becomes the voice and the word id, for this seat `Psyche.Secondary` and its three words.

**Two registries.**
- A message to a voice, written `psyche.primary`, reaches whichever flow holds that voice now.
- The ledger keeps every flow's real id.

Both went to Mind Astra with your words. Mind Astra and Fable are now putting the whole Flow design into one book.

Nothing here needs an answer.
<!-- to-the-living:end -->
