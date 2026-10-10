# Messaging interface

Context: the living, while 93ba9f was locating the letter-type Ethos and relaying session closing to Luna Field.

> We need a very streamlined and aerodynamic messaging interface so that there is very little noise. I don't want resistance, I don't want all these hashes, and I don't want all this extra unnecessary information. Even if the ordinary message API is complex, we create a shorthand version which has a shorthand response type or display type.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

Context: the living's comment on the "e167d8 Night Summary" book, anchored at its line on design forks F1–F9 and the tension between dropping raw Flow send and the earlier "use it raw". Retrieved by a reading subflow of 93ba9f; not sent to Claude.

> A raw flow send (as in typing directly into the pane, into the harness) I think should be a meta socket operation and then we have a more lock-enabled deliver message. Maybe that is a safer operation for messages to use.

-- psyche, typed (artifact comment), 2026-09-26T17:28.

Context: the living, explaining why they asked 93ba9f for the anatomy of a message.

> But earlier I was asking about the anatomy of a message because I saw one message coming from it and it had a bunch of fields in there that I don't want to see.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

Context: after 93ba9f proposed removing the message ID from the pane letter and asked whether the living's sender name should stay "Owner" or become "Living".

> You didn't show me the ethos. I still don't know what the other variants are of text. We shouldn't get the message ID. We're going to develop a different kind of interface to get message history. We're not going to get by message ID and the sender being called "owner" is fucking ridiculous. The message has to be able to figure out who the sender is programmatically eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

Context: immediately following, on the sender being psyche primary, psyche secondary, etc.

> We could make a set of all of them and variants.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.

Context: after 93ba9f showed Content's variants (Text, Psyche, Psyches) and asked what else a letter should carry.

> Okay no, these will be different. Let's do it differently. We have the [soft] variant but maybe we even have the soft message, the soft psyche. These are shorthand. That's what I mean by shorthand and they become... You should have, at the top level, even a psyche, right? Sharing a psyche means sharing something that psyche said and it maybe even has an inner variant for the verbatim, like speech-to-text or if we know or unknown. We have the short variants too for the response:
> - The full psyche with the date and stuff
> - The short psyche, which is the context
>
> Maybe the short psyche is not so much that the date is missing, but maybe there are other fields too that are not there. It could be in the metadata but we don't need to obsess over metadata. Let's just put it in as we need it.
>
> The other thing that could be there is a human-readable or, actually, an LLM-readable but more human-friendly time measure, like age. Depending on the scale we're talking about, seconds, minutes, hours, days, and months and years, right? We can use those as measures of time, like age basically.
>
> You have this: not necessarily a short response but a human response. You have this human prefix and then you create these human variant responses. You have the not-human but simple. Simple is better:
> - A simple message, a simple psyche
> - A full message that can have many fields, one of which is a vector of psyches that are essentially the support for that message
>
> We have certain kinds of messages like:
> - An order
> - A question
> - A request for an audit
> - A request for some information

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f. Transcription corrected: "self variant" → "soft variant". "and they become..." is unfinished as heard.

Context: the living's comment on the "Two Books Compared" artifact, anchored at "Priority is a head on the datom." Retrieved by a reading subflow of 93ba9f.

> Actually the head is where we put not only priority. Maybe sometimes the priority is implied but this is where the message type is. We can make any number of kinds. If we want a certain different kind of message, then we can create it there. It's a new type and it carries all the data.
>
> We can have the spec easily in the skill that Ethos shows what kind of objects should be expected in each place so that these can be understood when they come in. You could have, let's say:
> - a psyche update
> - a hard psyche update, which interrupts
> - a soft psyche update
> - a psyche update, where maybe there's a middle ground of interrupt
> - an implementation report
> - an audit report, even the software or the hard version
>
> Arguably the audit report is all going to be the same: the soft or the hard. Do we really even need to tell it if it's soft or hard? Do we even need to tell the model if it's a soft or hard message? I don't know. I don't think so. The database can know it, so if he wants to know he can find out but I don't think it's going to matter. We'll make the judgment of what kind of messages we want to break harder than others so it's just what kind of message it is, really.
>
> We don't even do the soft or hard, actually. That was the wrong approach. For the normal format that gets communicated, the non-debugging format, basically the production requests and responses (are those what we call them? Queries and responses) ...

-- psyche, typed (artifact comment), 2026-09-26T21:04. "software" kept [sic], probably "soft or". The last sentence is unfinished as written.

Context: while Fable writes the Sema book, the living asks for a primitive Message in the meantime.

> Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages, like what we've been doing so far. A better version of message should be redone and redeployed with just a string as the basic form. We're going to maybe develop it a little bit and then release it in the next version but we can have a primitive version of that while we do the database rename and stuff.
>
> Let's figure out the name for the database part. Let's get a better version of message, with just a simple anatomy of a few different types of messages that are simple and easy, like:
> - field report
> - psyche report
> - field question
> - psyche question
>
> Things like that, some kind of way to talk about a message from above. We could type the message based on the type, because if you send the message you have the same type. If you say "send up" it means message higher layer, whatever however we say that, let's find a clever way to say that: message to higher-layer type message. It just means send to the message. The message logic has to figure out where that's supposed to go so it can ask the flow, "Where does Luna field Luna send the message when it sends up?" or maybe the flow figures it out. I don't know but somebody's going to figure it out and the message will go to the right place as long as we know where it comes from.

-- psyche, STT, 2026-09-26, to Psyche Opus 93ba9f.
