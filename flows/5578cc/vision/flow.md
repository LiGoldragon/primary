# Flow

## Speech climbs one layer at a time, and the Primary layer is spoken to least

Context: comment on the proposed vision-flow line "Speech climbs one layer at a time, never skipping a layer, and the Primary layer is spoken to least. Design belongs to Mind's Primary."

> This is good. Except for the last sentence, I don't understand that. That feels half-hallucinated from a particular situation. I think what it's trying to say is not the right thing and not in the right scale but the beginning is good. Maybe we want to put in the layers there.

-- psyche, typed, 2026-10-03T15:43, book comment.

## Session names are aspect and layer only, aspect first

Context: typed in chat to Psyche Opus 5578cc, after the layer decisions.

> I [also] want the session names to be by aspect and layer only: primary or psyche primary, the aspect first.

-- psyche, typed, 2026-10-03. Typing corrected: "so" → "also".

## The session title: aspect, layer, and the word id

Context: comment on «Flow ids in words, and seats launched by Flow», at the current title `Psyche.{ Opus 5578cc }` (this seat).

> Like I said to some other Flow or in the comment, I want it to be: now the model is replaced by the layer so this would be psyche secondary and then the ID is replaced. Well it's still the ID but it's a word ID.

-- psyche, typed, 2026-10-03T15:55, book comment.

## Two registries: the true one with the ids, and the voices

Context: comment on «Flow ids in words, and seats launched by Flow», at "Psyche Primary" under "The path I propose".

> There are two registries:
> - The true registry with the actual IDs
> - Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice, the current flow for that voice
>
> The syntax would be `psyche.primary` because it only has one. It's like a single-field data-carrying variant, right? We don't need the struct braces. It's kind of like a data-carrying variant that holds a variant essentially.

-- psyche, typed, 2026-10-03T15:58, book comment.

## Speech between voices is guidance, not a hard rule

Context: comment on «May Field speak to Psyche?» (the pointer version), at its title.

> Primary can talk to other primaries and one secondary, with a good reason, can talk or one voice, with a good enough reason, can send a message up. Sol cannot talk to Fable. He has to go through Opus or through Astra. He can't talk through another voice. He can talk to Astra and then Astra might convey some of what he said to Fable but we can't. It's not a hard rule; it's guidance. Of course there may be an exception but it should be rare.

-- psyche, typed, 2026-10-03T15:11, book comment. Already carried into Astra's design through 9fb0ad's relay.

## Deterministic work is done by code, never by the model

Context: comment on «How Flow launches a flow and builds its prompt», at "Flow picks the session id and claims the flow id before the harness exists (Claude). Codex gets its id after it starts." First comment in the thread (a question): "Why is this different from Claude Codex? Are you saying we can give Claude the hash we want to use for its session ID and not Codex?"

> In any case there's no reason for us to make the model check the flow ID. It should get it in its prompt because, if anything, we can start a session without launching its first prompt and we can get its session ID before it even starts. We don't have to pay for the LLM to do all of the work that a deterministic cheap program can do. Let's make this so we need something developed into intent: that we intend to do anything that is deterministic into code, to save the context, cost, and noise that making an LLM do it would incur.

-- psyche, typed, 2026-10-03T16:17, book comment. Asks for an Intent statement; wording to be proposed for his approval.

## The system prompt is built from modules, with an anatomy in ethos

Context: comment on the same book, at "System prompt." (Flow replaces Claude's system prompt with one caller-supplied file).

> Well that obviously won't do. We need way more configuration for the system prompt so that we'll have modules and then there are going to be different types. There could even be an overlap between what we call skills now and what these modules are that can go in the system prompt.
>
> The one thing I would really like to know is if it's possible that there's a part of the system prompt that doesn't get passed down to the subagents of that harness. I would like to be able to program the main flow a certain way but not its subagents in its system prompt.
>
> We need to break that down into modules. We can't just make this one thing. That's absurd. The system prompt is huge. It has several, many, many different parts that have many different subparts. We need to draw up the anatomy of this in ethos by studying all kinds of system prompts and splitting them up into:
> - what this is
> - is this behavior?
> - is this personality?
> - is this operational safety?
> - what each line even falls under in terms of what kind of training/guidance it is a part of

-- psyche, typed, 2026-10-03T16:20, book comment. Contains a question (a part of the system prompt not passed to subagents), to be found out.
