Presentation.{ «Identifiers and names» }

# Part 1. What he wants

## Why words at all

Words exist to be cheaper, for the machine and for him. An id written in words is meant to be used: read, spoken and passed around, not kept in a back room.

> "If the whole point of using words is because it's cheaper for LLMs and for humans, then the whole point is for LLMs and humans to use it. Isn't that obvious?"

-- typed, 2026-10-03

The cost being saved is the machine's reading cost, and words are also easier to say and to think with.

> "The only cost we're worried about is the LLM token cost. ... They're more easily communicable in a speech-to-text context, and even cognitive. We think better in terms of words."

-- typed, 2026-09-15

## What an id is

An id is a number of its own type, not text. Text is only how the number is printed.

> "Why are we saying that the ID is a string? It seems to me that we could maybe create an ethos library for this, but those are real types, like a SHA-256. Yes, in a way, it's a string when you print it, but it's not a string per se."

-- typed, 2026-09-15

Inside a Nexus the id stays a number. Turning it into letters or words, and back, happens when it is written out or read in, at the edge.

> "The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits. In the deserialization, we can have special implementations, maybe, so that a certain kind of thing is deserialized with a certain kind of algorithm that creates an alphanumeric hash from a string, from a hash which is an integer or whatever."

-- spoken, 2026-10-03

Proposed: the Nexus keeps records under the number, and only the command-line side carries the printed forms.

## How a word id is made

A word id takes the first 33 bits of the id the harness gives a session and writes them as words. Because it can be turned back into those bits, a tool can go from the words to the right transcript.

> "Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words."

-- typed, 2026-10-03

The words are joined in camelCase, with the first word in small letters, so an id never looks like a type name, which starts with a capital. A real example is abandonAbilityAble.

> "They're all capitalized, and then camel case could be easily recognized as probably a hash or an idea of some sort. That could be a good idea. You get the visual differentiation, and that's how it's written. If the LLM can tokenize that efficiently, then it's golden."

-- typed, 2026-09-15

Proposed: three words from a list of 2,048 words give exactly 33 bits, eleven bits per word.

He accepts that two sessions may sometimes share the same words. When that happens, the tool returns every match and he is told.

> "If 33 bits, for me, I think it is enough entropy. If there is a clash then the model can easily figure out, "Okay here are two matches," and that would be worth bringing up to the psyche: "Oh we've had a collision," and then see what we do."

-- typed, 2026-10-03

## The library

Word ids come from one shared library, not from something built only for flows. It works for a hash of any size, so the same code gives a 33-bit id, a shorter one or a longer one, and any id type can ask for its words.

> "No the word ID library that I want is not implemented specifically for Flow ID. It's generic so we can use it for any hashes of any size. ... Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?"

-- typed, 2026-10-03

Every tool can read and write the words.

> "There's a converter that can use this in field and all our tools would support it, so that it has an implementation for how to turn this name ID, this word ID, or this phrase ID basically into the hash. That will give us the link that we need, like the Codex transcript."

-- spoken, 2026-09-26

Proposed: the library offers four operations for each size: to words, from words, to the short letter form, and from the short letter form. Reading the words back can fail in two ways: the text is not a valid id, or more than one id matches.

## What a title is

A session's title is three things: its aspect, its layer, and its word id. The layer takes the place where the model name used to be.

> "I want it to be: now the model is replaced by the layer so this would be psyche secondary and then the ID is replaced. Well it's still the ID but it's a word ID."

-- typed, 2026-10-03

A title is written in the same notation as the data, and that notation is meant to spread everywhere.

> "That's what the titles will be everywhere. I wanted to see we are going to permeate the world with ethos and Datom syntax."

-- typed, 2026-09-25

A title holds no state. Whether a seat is current belongs in Flow's records, not in a window title.

> "Using header pane titles for storing data is like you should just use a registry for that, somewhere where you want to say whether it's current or it's not. That's what Flow's database should be."

-- typed, 2026-09-24

## Session names

A session is named by aspect and layer, with the aspect first.

> "I [also] want the session names to be by aspect and layer only: primary or psyche primary, the aspect first."

-- typed, 2026-10-03

The name is the same everywhere he sees it: in the pane, on the remote, and in the list.

> "Can we fix the [Herdr] pane and all of the names disagreeing so that the name is the same everywhere in the session?"

-- spoken, 2026-09-26

## What a name is for: addressing

Seats are reached by their lasting name, which carries over when one session hands over to the next. The flow id belongs to the ledger and the archive, and to finding a transcript.

> "I'd like flows to be addressable by their continuous name, not the flow itself. ... so that we don't need to use these flow IDs anymore. They're just for accounting or for the ledger, the archive side of things, and for knowing where to search if the transcript is needed, etc."

-- typed, 2026-10-02

A voice's name is its aspect and its rank, not its model.

> "Actually no, it's not psyche Astra. It's psyche primary, psyche secondary, mind primary, mind secondary, because we're not going to expose all the models to all of the voices."

-- typed, 2026-10-02

Two lists keep this straight. One holds the real ids. The other holds only the voices and passes a message to whichever session holds that voice now. A voice is written with a dot, like psyche.primary.

> "Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice, the current flow for that voice. The syntax would be `psyche.primary` because it only has one."

-- typed, 2026-10-03

A seat never has to say who it is. The receiving side works out from the calling process which seat sent the request.

> "It can get its origin without the user having to say, "Hey I'm Psyche Fable." It would just know. That's really what I want. I want the user interface for the agent to be really simple and everything just works deterministically."

-- spoken, 2026-09-26

## Where a hash may appear, and where never

Never in what seats send each other.

> "You guys have to stop messaging each other these huge random alphanumeric strings, these huge identifying strings. ... These huge unreadable strings are extremely context-expensive and you're just filling your circuits with disruptive noise."

-- typed, 2026-10-01

> "You really fucked up. You sent them giant hashes."

-- typed, 2026-10-03

Never in a launch prompt and never in anything shown to him.

> "There are these huge hashes, these huge alphanumeric strings, and I don't want these. They're extremely expensive context-wise. They're like entire paragraphs."

-- spoken, 2026-10-01

A hash may be stored in full in the ledger, the archive and the transcript stores, where tools read it and no one has to.

Proposed: the full id is used only for these lookups.

## Six characters for commits and artifacts

Where a printed id is still needed, it is shortened to six characters, with words to follow.

> "We need to develop a way to deal with these, a standard way to write a shortened hash, really 6 characters. ... Let's go situation by situation but I also want to eventually go into the transformation of these random strings into the word-based standard."

-- spoken, 2026-10-01

A commit names the larger piece of work it belongs to, and the change explains itself in that light.

> "The commit message identifies the epic because there are going to be maybe thousands of commits for that epic. They're all called the same, right?"

-- spoken, 2026-09-18

Proposed: commits, published pages and other artifacts carry the six-character form as their name until the word library is in place, then the three words. Commits never carry the full id.

## Book titles

A book's title is plain and short.

> "I like better titles, no convoluted titles like that."

-- spoken, 2026-10-03

# Part 2. What exists today

The flow-id tool hands a new session its id. It takes six characters from the session id the harness gives, makes the flow's folder under that name, and prints the six characters. It has no word form.

The flows index has one line per flow, 271 lines in all. Each line gives a kind, the six-character id and a one-line summary.

The messenger's list names each seat as aspect, model and six characters joined by underscores. It gives the model where he wants the layer, and it has no word id.

Recent commits begin with "Publish", then the six-character id, then a short line describing the change.

No word-id library was found in the Rust sources searched.

# Part 3. Questions

1. **Six characters now, or words first?** Today every seat name carries six characters.

   > "I would like to get the minimum [viable] product up first so if we let go of the word ID for now and then do that in a later version, that's okay."

   -- typed, 2026-10-03

   > "This looks perfect. That's exactly the user interface I was looking for."

   -- typed, 2026-10-03, at abandonAbilityAble

   Answer 1 to ship titles with the six characters now and switch to words later. Answer 2 to build the word library before anything else is renamed.

2. **Where does the library live?**

   > "Let's do the name-based hash thing in the signal library."

   -- typed, 2026-09-15

   > "This should go into a library that all components can reuse, so maybe some kind of Ethos core library or Ethos standard or something."

   -- typed, 2026-10-03

   Answer 1 for an Ethos core library, 2 for Ethos standard, 3 for Signal.

3. **May a seat point to a transcript with six letters?** For example, a seat relays one of your book comments and needs to say which session it came from.

   > "Make a change in a testing skill that's usually loaded to prevent the usage of hashes in most contexts, only using shortened hashes where necessary."

   -- spoken, 2026-09-21

   > "Other than that I would prefer the seats talk to each other by their seat names. ... These would be their names without the flow ID."

   -- typed, 2026-10-02

   Answer yes if six letters, or three words, may appear when a transcript must be found. Answer no if seat names only, with the reader looking the session up itself.

4. **Which word list?** With 2,048 words, 33 bits is exactly three words. A denser list carries more bits per word, so 33 bits no longer fills three words evenly.

   > "Is there a newer one that has more bit density? We can use that. We don't have to be standard."

   -- typed, 2026-09-15

   > "Yeah I think BIP-39 was the one we found to be most efficient but it would be cool to dig to see if somebody did some research on something like this for LLMs. ..."

   -- spoken, 2026-09-26

   Answer yes to keep the 2,048-word wallet list for three words. Answer a number to set the list size you want.
