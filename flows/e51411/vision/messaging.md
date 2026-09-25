# Messaging

## Flows may bypass a failing send and prompt each other's panes directly: communication with fallback

Context: this seat had declined to type straight into Field Astra 5f38bc's pane, because the checked send could not reach it and the messaging rule forbade falling back to another channel.

> That's okay. You're all allowed to bypass failing messages and send each other straight into your panes. I just want you guys to be able to communicate with fallback.

-- living, input mode not established, 2026-09-24, to Psyche Medium e51411. This is a newer word than the "no fallback to another channel" rule in testing-message-route. The skill line is owed.

## The easiest way to send is the basic skill; remove contradictory instructions

> Can we figure out the easiest way to send messages and just skill properly, remove contradictory instructions, and make sure this is a basic skill?

-- living, input mode not established, 2026-09-24 20:25:32, to Field Astra 5f38bc; not logged by that seat; recovered verbatim from its transcript by d8df70's logging audit (flows/d8df70/reports/psyche-logging-audit.md).

## The pasted-content wrapper on messages must go, and be explained

> I can see the new Fable and I can see these messages getting the pasted content ID/XML tags. I want that gone. I want it explained to me what's going on there. Communicate with mind and maybe [field] to find out what it's about. Get different points of view.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411. Transcription corrected: "feel" → "field" (inference).

## The Clojure HM makes machine messages real EDN, actually processed; the living's input stays apart because it is not EDN

> the proof of concept, and pure [Clojure] is what I'm talking about. We can get a fully actually real concept on the ground instead of just making the agents pretend that they're talking through datom but it's not processed. And then we still get the differentiation from real Psyche input messages, which are not in EDN syntax.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411. Transcription corrected: "closure" → "Clojure".

## Our own system prompt explains the message syntax, with a section for the psyche's verbatim words; speech-to-text is corrected before it travels, and in logs, with the correction marked

> Well it's not completely false. We need to write our own version so we need to replace that system prompt to explain that the message syntax will have a section for verbatim psyche words, which should also be corrected, by the way, in the right skill. We shouldn't pass around verbatim speech to text that has not been corrected for speech-to-text errors because then it's going to create a huge hell.
>
> Even when they're logged, the psyche should be corrected and we just put the correction in. I don't know, what's canonically done: do we put square brackets around the part that was corrected for clarity? Then we would train.
>
> I guess it's a bit of a problem that Claude automatically wraps this with the pasted content thing but maybe there's a way around that. If we remove those instructions and replace them, it's not a big deal because it doesn't then have those instructions although it probably has been trained on them.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411, after Mind reported that a Codex base-instruction replacement is inherited by subflows.

## Maximize the message itself: it has more value, a higher stratum, than a pointer

> Anyway you can give me your 5 cents and send the whole thing as a package with all the data that you can gather to Fable. I guess you're going to write some report and then give him a nice message explaining: maximize the message that you send because it has more value or a higher strata. Contact Fable and ask him for his input on this.

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411.

## The registry becomes Datalevin: the relational database with Datomic-like syntax

> Well obviously, the registry would become this Datomic, the database we picked again: the Datomic open source. Like a relational database with datomic-like syntax

-- living, input mode not established, 2026-09-25, to Psyche Medium e51411, after the Clojure HackyMessenger passed its tester. Reading note, inference: "the database we picked" is Datalevin, the living's own earlier database, now used through the Babashka pod.

## A message is really just a message

> I think that there are too many fields. This timestamp is fucking huge. It's taking so much fucking room and most of the message you got is just gibberish. Let's cut this. Write the fuck down [sic]. A message is really just a message. What is this machine relay? Is that like a key-value map? You're using that to kind of emulate the variant?

-- psyche, STT, 2026-09-25, to e51411. "Write the fuck down" kept [sic]; read as "cut it down".

## The psyche reaches flows through the messenger

> I want you to use a subagent to refurnish your context in the middle stratum so that you get the psyche verbatim from recent logs that concern anything that you're touching. ... Use an Opus subagent to recompose and send you messages so that the psyche reaches you in the middle stratum and let's start using this new messenger.

-- psyche, STT, 2026-09-25, to e51411.

## No repeated or empty fields in a message

> I see "machine machine." There's a lot of repetition. There's really no point to that. Just "1: machine" would be enough and we don't need to repeat this other "machine." We don't need this huge timestamp. I don't even know why we are doing the timestamp. I don't know what this "unknown" is but I see a lot of "unknown" and I don't think it's really useful. There's a vector of Flow IDs. Are these the recipients? What's the last string? It's always empty.

-- psyche, STT, 2026-09-25, to e51411.

Correction to "A message is really just a message": the living said the words were "Let's cut this [right] the fuck down." -- psyche, STT, 2026-09-25, to e51411. Transcription corrected: "Let's cut this. Write" → "Let's cut this [right]".

## The sender's aspect and model come from the database

> It knows which pane the call came from so we can use the database to know the aspect and the model.

-- psyche, STT, 2026-09-25, to e51411.

## Messenger, not Message

> You know the way you just made a change and then committed it in one command? Why don't you just make a cool [Clojure] tool called Field so we can emulate the Hacky Messenger, the Hacky Field? It's actually Hacky Message, right, because it's message, or is it Messenger? I don't even know. I guess Messenger because a message is another thing that we talk about a lot so it's Messenger. Even the nexus should be called Messenger.

-- psyche, STT, 2026-09-25, to e51411. Transcription corrected: "closure" → "Clojure".
