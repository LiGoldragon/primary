# Ethos

## Signal, process, and storage; nexus is overloaded; a better vocabulary for what is memorized

> "Let's also look at ethos more in depth because I want to be able to start designing with it so we can have the signal, the process, and the storage. Maybe we call it the process instead of these convoluted terms. Plus nexus is overloaded because it means the daemon and also the central process actor. I'm not a big fan of storage but something that emphasizes the kinds of things that are memorized, as in a database, but maybe with a better concept vocabulary."

-- psyche, typed, 2026-10-02.

## No repetition of types; inline unless reused; a maximum depth; a dense self-documenting overview

> "Think about what I said about how I don't want this repetition of types, like where we invent another type to say what's inside a variant. I would also like to make it so that unless a type is used in more than one place, it should be declared inline. We would have a maximum depth after which we would require the types that are at, I don't know, maybe the third depth to be imported from an external library. We would have an extremely dense visual overview look when we look at the main, say, signal file: what the queries and responses are, it would be very, very clear. It's kind of like a self-documenting data type specification."

-- psyche, typed, 2026-10-02.

## The actual ethos of the three layers; distill the vision; example syntaxes now

After commenting on the capsule book.

> "Now we need the actual ethos of the three layers if you understand what I'm saying. Otherwise we also need to talk about the ethos, what all of this means, and how we design in three layers: three different specifications:
> - the signal
> - the process
> - the storage
>
> We need to talk about where this will all go in terms of actual code and vision. Let's distill the vision for this and start putting out example syntaxes even if they're not running as-is in the code right now. Using the new way of writing ethos is extremely compact and non-repetitive."

-- psyche, typed, 2026-10-02.

## A book with Astra on the ethos of the three layers: signal, storage, operation

Held in the transcript during the quiet window; written at its end.

> "Yes let's make a book with Astra and with the ethos of all three layers: signal, storage, and operation. I like it. I don't know what yet storage is. Do we have a book on that? I'm going to go look. Anyway I want to talk about that. Do you understand what I'm saying?"

-- psyche, typed, 2026-10-02.

## His comments on «Flow in ethos», 2026-10-02 20:09–20:56

> "Yes they're going to be called voices. That's the right term. Psyche, Fable, and Mind Astra are voices."

> "Actually the word you used, "run," is "flow." That's what a flow is. What you're calling a run is a flow. That's why we're calling the component "flow." It's all about managing all of these flows. I don't understand, up higher in the stack, when you have a start refused and then one of the variants is launching. How does that work? If it's refused how is it launching? That doesn't make sense to me."

> "I don't want these Sonnet comments anymore. Sonnet's place is not in comments so that was an error on my part. Let's remove that instruction wherever it is."

> "Yeah the memory is good. That's what it is I guess: signal, operation, and memory.
>
> When we define its operation we define all of the operation types. What kind of operations have to take place for this to happen? Anything that can have an effect is going to have a corresponding operation, which is going to be the type that we have to use. We're going to have to go through these types to go from signal to operation to memory and back into operation.
>
> If the memory has changed and there is a successful memory edit kind of return operation, that's going to end with a signal, probably sending a response back that the effect has taken place.
>
> I want a whole document on this aspect of how the anatomy is developed in signal (which is the way it talks) and in operation (which is the way it treats these signals or these returns on the memory change).
>
> We're going to have to have, I guess, an implementation on the memory kind. It's going to be a kind that's going to have a standard successful or unsuccessful change implemented on these particular data types. Also each version is possibly going to have an implementation of an upgrade from or an upgrade to. I'm not sure. I guess an upgrade from makes more sense because you're trying to upgrade the past but it could be a symmetrical operation. That's also where I want to tie into how eventually the change in ethos is going to be operational. That operation is going to be the very edit, the very update operation that this particular data type needs to change into its new memory format."

> "We don't have key-value in Ethos anymore. Everything is a type."

> "What the hell is a question 4 here?"

> "Launching, hearing, and resolving are not good names for kinds so I think we went more towards the qualifier `launchable`. I think that makes more sense because that then cognitively translates as a kind."

> "The way this is formatted, I want ethos formatted differently so we need to change the vision. I want it to be a language that expands vertically.
>
> When there's a bunch of stuff and it's going to overflow, the overflow, when it wraps the line in this web UI here, is fucking horrible because it goes back to the same line that it wrapped from, which is really really bad. Even if it made an indent, it wouldn't be good enough because it has to be perfectly lined up, beautifully formatted, a bit like Nix or Python. It looks more like a data structure that expands vertically whenever there's a next layer.
>
> When you're defining inline, like `flow.voices`, then you should go vertically and be liberal in going to the right. If you have a `temps.vector`, then you can make that next bracket there expand vertically too.
>
> Let's redo all of that, all of the book, with the comments applied and this new way of making the language and its structure more obvious. If you go all in one line, the structure is not obvious. That's what I'm trying to say. That's why I was thinking we limit it to three depths and then everything has to be referenced from another library, in which you can expand again three depths.
>
> We don't have to make it a hard limit. Maybe it's not a hard hard limit but it would mean it's more like a user interface approach to programming languages rather than accelerating the cognitive transmission of ideas."

> "I don't understand how there's a specific type as an input for a kind. That shouldn't be, right? It should only be another kind because a type is too specific. Now you're saying, I don't understand: where is it? This doesn't make any sense. The voice is launchable, right, so it uses self. I feel like you've lost it here. You don't understand kinds or what you're showing me. This is something else that you've hallucinated. Or what do you think? What's your pushback on here? Do some actual real-world Rust checks to make sure that nobody is shoving a foot down his mouth, neither you nor me. Let's make things clear here also in the knowledge skill."

-- psyche, typed, 2026-10-02, book comments on «Flow in ethos».

## The closing delimiter does not take its own line

After the redone book laid every closing bracket on its own line.

> "Yeah you misunderstood what I wanted: the ethos formatting. I don't want the closing delimiter to create a whole new line and I don't think you really understood what I meant about the traits and the parameters for it."

-- psyche, typed, 2026-10-02. (The rest of the message — "Let's get into that more in depth ... do some digging to see what I've said about this" — is an instruction, kept here as context only.)
