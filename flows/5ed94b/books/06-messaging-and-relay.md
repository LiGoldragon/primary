Presentation.{ «Messaging and relay» }

How seats talk to each other: what a message is, who sends it and to whom, by what name, what it carries and never carries, how his words travel, and what happens when a seat is replaced. A seat is one long-lived post, an aspect at a layer, held by one flow at a time. A datom is our small structured text form.

## 1. What he wants

### A message is a datom, and it arrives as one

A message comes in as a datom, straight into the receiving prompt.

> it sends the prompt in as a Datom-formatted object. That's how the message is composed, how it comes in, and it's recognized that way.

-- 17 September 2026

> I want to get rid of this pasted content ID XML tag around the messages. Get rid of it. ... I think the Datom syntax is more than enough.

-- 24 September 2026

A datom has variants, not tags. The head of the message is its kind, and the kind carries all its data.

> Datom doesn't have tags, has variants.

-- 26 September 2026

> Actually the head is where we put not only priority. Maybe sometimes the priority is implied but this is where the message type is. We can make any number of kinds. ... It's a new type and it carries all the data.

-- book comment, 26 September 2026

Kinds he named include an order, a question, a request for an audit, and a field or psyche report.

> Simple is better:
> - A simple message, a simple psyche
> - A full message that can have many fields, one of which is a vector of psyches that are essentially the support for that message

-- 26 September 2026

### What a message never carries

No hashes, no timestamps, no message id, no repeated or empty fields, nothing the reader does not need.

> You really fucked up. You sent them giant hashes.

> And a bunch of timestamps and all a bunch of fucking useless garbage

-- 3 October 2026

> We shouldn't get the message ID. We're going to develop a different kind of interface to get message history.

-- 26 September 2026

> I see "machine machine." There's a lot of repetition. ... We don't need this huge timestamp.

-- 25 September 2026

There is no size limit.

> Let's just not limit ourselves on message size

-- 26 September 2026

### Seats are addressed by name, not by number

> I would prefer the seats talk to each other by their seat names.

-- typed, 2 October 2026

The sender is known from where the call came from, not declared.

> The message has to be able to figure out who the sender is programmatically eventually from the process that called

-- 26 September 2026

Proposed: the sender's name is filled in by the messaging program; the seat writes only the body.

### Nobody is disturbed by messages that are not theirs

> we shouldn't send these broad messages to everybody, especially for testing. ... don't wake flows unnecessarily.

-- 21 September 2026

A relayed word keeps its addressee. A seat that receives a copy is a witness, not the one spoken to.

> if I say "restart yourself to a flow," I'm talking to that flow, not to all agents. Don't start taking all my messages literally.

-- 17 September 2026

New vision reaches a seat whose topic it touches, with its next messages, not as a fresh wake.

> it should be routed to that flow. The next time that it receives messages anyway, right? We don't necessarily push every time

-- 3 October 2026

### Who may message whom: guidance, not law

> Primary can talk to other primaries and one secondary, with a good reason, can talk or one voice, with a good enough reason, can send a message up. Sol cannot talk to Fable. He has to go through Opus or through Astra. ... It's not a hard rule; it's guidance. Of course there may be an exception but it should be rare.

-- book comment, 3 October 2026

> It should be rare for Field to talk to Psyche, right? Very rare and actually almost never.

-- 28 September 2026

### How his words travel

His words travel whole: context first, then his exact words.

> it's verbatim "psyche" with context. I guess first is the context and then the verbatim.

-- 25 September 2026

They arrive in the receiving seat's prompt, not by that seat reading files.

> what I said has to come in through your middle stratum. You have to use a tool that you might have to refine now to get the message extracted and sent to you in the user prompt.

-- 15 September 2026

The tool finds his words in the transcript from a few characters at each end. The seat never retypes them.

> get the last user prompt, search for that match in the transcript, and send it as a message. It would be way more efficient.

-- 13 September 2026

A message that rests on his words carries them.

> every time somebody sends a message, they need the Psyche verbatim that authorized it.

-- 20 September 2026

His words are told apart from machine messages by form: his are plain, machine messages are datoms.

> the agents will know that it's me because of how the message is formatted. It won't be datom-formatted.

-- 18 September 2026

### How a message is delivered

Delivery differs for each harness (the program that runs a model), and there are degrees of interruption.

> * the hard abrupt
> * the middle hard abrupt
> * the really soft, like waiting until he's done, basically

-- 17 September 2026

His reviewed vision says how: on Codex a hard interrupt is one Escape; on Claude it is two Escapes, the prompt, then Enter. Middle reaches Claude at its next tool step. Soft waits until the receiver finishes.

Flow, the program that runs flows, is the only writer into a seat's terminal. It locks it, types the message, unlocks it, and says whether it worked.

> It would just ask to send a message to a certain Flow, and then the Flow would say successful or not, basically.

-- 21 September 2026

> A raw flow send (as in typing directly into the pane, into the harness) I think should be a meta socket operation and then we have a more lock-enabled deliver message.

-- book comment, 26 September 2026

An interrupt witness is not a delivery witness. His reviewed vision separates four observations: the interrupt, the text placed, the text submitted, and the receiver taking it in. None stands for another, and a submission is never a read receipt.

Writing in your own transcript is not replying.

> when you write a comment in your transcript, you're not replying to another agent, right?

-- typed, 28 September 2026

### Registration

> We need to take out the requirement for the flow to not be busy to be able to register and we don't want it to require any kind of probe or testing message. ... It's just kind of like fake correctness

-- typed, about 29 September 2026

> If there's no registry or if the registry says "in transition" or something, then the message can sort of be held

-- 23 September 2026

### On refresh and replacement

A replaced seat is never woken by a message.

> The old one's still open and I bet if somebody tries to message people, they'll wake the old flow up. That's really bad.

-- typed, 29 September 2026

Replies go to the successor, which knows what its predecessor sent.

> if the message does go out to its destination, then the reply will go to the new flow. The new flow also knows what the message was that was sent to another flow by its ancestor.

-- book comment, 19 September 2026

If a message cannot be delivered, it goes up one power, then down.

> If a message can't be delivered, then we try a higher power. ... The message returned for the caller will say what happened

-- book comment, 24 September 2026

### Signal

> Signal is our messaging layer, and the CLI's role is to transform text into Signal.

-- 8 August 2026

Proposed: seats read and write datom text; the programs carry it between them as Signal.

## 2. What exists today

Witnessed. The messenger, version 0.2.8, is the route every seat uses. It sends, interrupts, registers, repairs, retires and lists, and its skill tells seats to address by six-character code, not name. A machine message goes as a tagged note holding sender and text, and his words go in a second tagged form with sender, context and words. Each send takes a file lock and types into the terminal itself, never through Flow or the Message Nexus (a message ledger, version 0.19, that nobody uses). Flow's deliver command runs, and no skill points to it. One report counts 444 receipts in 39 logs, much of it lock notices, landings and releases. Two seats share one seat name. The relay tool he described exists but is not installed, and seats retype his words.

Supposed: names cannot be addresses yet, and seat messages do not travel as Signal.

## 3. Questions

**1. Which name is the address?** Say one seat messages another.

> It would be like Psyche Fable, Mind Astra, Mind Sol, Psyche Opus, etc.

-- 2 October 2026

> Actually no, it's not psyche Astra. It's psyche primary, psyche secondary, mind primary, mind secondary

-- 2 October 2026

Answer 1 for seat and model ("Psyche Fable"). Answer 2 for aspect and layer ("Psyche Primary"). Today two seats can hold the same seat-and-model name.

**2. Who receives his words?** Say you speak and a decision follows.

> can you pass all of the psyche messages along to everyone and stay aware of how many flows there are?

-- 17 September 2026

> I'd like, for a solution, for you to stop being disturbed so much by messages that absolutely have nothing to do with you and are costing us money (a lot of money in terms of the fact that it's polluting your context and then degrading our design, destroying our machine).

-- typed, 3 October 2026

Answer 1 for everyone, 2 for the seat's own cluster, or 3 for only seats whose topic they touch.

**3. Who writes the relay of his words?** Say you speak and a seat must pass your words on.

> We shouldn't ask the model to rewrite the whole thing because it's already been said and it's right there in the transcript.

-- 15 September 2026

> We actually use the intelligence, the thinking there, to create the message.

-- 15 September 2026

Answer yes if the tool carries your exact words and a small model writes only the context line.

**4. Is urgency part of the message?** Say a seat must tell another to stop at once.

> There should probably be two or three types

-- 17 September 2026

> We don't even do the soft or hard, actually. That was the wrong approach.

-- 26 September 2026

Answer 1 for a separate head with three degrees, which his reviewed vision still keeps. Answer 2 for each kind of message carrying its own urgency, as his 26 September comment says.
