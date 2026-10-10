# Fork pack: message-flow.ethos at 04a895

Draft: `flows/73ada7/reports/message-flow/message-flow.ethos` read via `git show 04a895:`. Records read from the raw files under `/home/li/primary/flows/`.

## Fork 1: the Message body/psyche payload, string or Meaning

### Records

1. `flows/b7ba00/vision/messaging.md:101`, section "A primitive Message now: a few simple types with a string; ..." (line 97). Date 2026-09-26. Context line (99): "while Fable writes the Sema book, the living asks for a primitive Message in the meantime."
   > Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages, like what we've been doing so far. A better version of message should be redone and redeployed with just a string as the basic form. We're going to maybe develop it a little bit and then release it in the next version but we can have a primitive version of that while we do the database rename and stuff.

   Provenance line (111): `-- psyche, STT, 2026-09-26, relayed by 93ba9f.`
   The same words are also at `flows/93ba9f/vision/messagingInterface.md:75`.

2. `flows/b7ba00/vision/meaningLanguage.md:157`, section "Sema's first version: one or two layers of variants with a string payload ..." (line 155). Date 2026-09-26.
   > The first version of sema could be that it just has one or two layers of variants, possibly with one variant and then another variant inside and the payload at the end being a string. That way we get a sort of strongly typed string, if you will.  And this then becomes the basis for how agents start to communicate with the message component.

   Provenance line (159): `-- psyche, typed (artifact comment), 2026-09-26, relayed by 93ba9f.`
   The same words are also at `flows/93ba9f/vision/meaningLanguage.md:29`.

3. `flows/8475a9/vision/datom.md:29`, section "No datom in any Nexus; string handling in a Nexus is forbidden" (line 25). Date 2026-10-05. Context line (27): "his comment on the drawing's box «Nexus: no Expander, so @ is Forbidden». Relayed by 8f0f57."
   > Well the Nexus has no datom so expand [it]. It doesn't even have datom. There should be no datom in any Nexus. It's going to be forbidden for string handling to be in the Nexus.

   Provenance line (31): `-- psyche, STT, book comment, 2026-10-05.`

### Draft lines at stake (04a895)

```
16:  Psyche.{ Context.{ Meaning }                 ;   something the living said, and where
17:           Verbatim.{ Meaning } }
18:  Body.{ Meaning                               ;   what a message says,
19:         Vector<Psyche> }                      ;     with the psyche that supports it
20:  Message.[ Order.Body                         ;   the head is the message's kind
21:            Question.Body
22:            Report.Body
23:            AuditRequest.Body
24:            InformationRequest.Body
25:            Psyche ] ]
```

## Fork 2: datom rendering in the Flow Nexus

### Records

1. `flows/1b8ac0/vision/messaging.md:31`, section "FlowLock does not degrade to Raw: ..." (line 23). Date 2026-09-21 (locator `1b8ac00b:1872, 2026-09-21T21:49:14.522Z`). Context line (25): "spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21, correcting PsycheHigh's framing of the living's earlier idea as a "fallback" and answering Mind's conflict ... Input mode STT."
   > It locks the message for the session to send the message, then it sends the message, then it removes the lock. The messaging will send a request to Flow to send the message, and Flow will say, "Yes, that window is locked." I guess Flow would even be the part that sends the text, so message wouldn't need to make this a two-part thing. It would just ask to send a message to a certain Flow, and then the Flow would say successful or not, basically.

   Provenance lines (33-34): `-- psyche, STT.` / `Locator: 1b8ac00b:1872, 2026-09-21T21:49:14.522Z.`
   The preceding paragraph (line 29) of the same record: "It's just a shorthand for a certain configured type of messaging request, or a request to send this text into a particular harness. ..."

2. The phrase "the message body is a datom that lands in the recipient's prompt": NOT FOUND in any raw record of the living under `flows/*/vision/` or `flows/*/notion/`. It occurs only as machine text: the skill copy (`flows/38de5b/reports/message-in-flow.md:60`, `flows/752e0f/psyche-block/recent.md:1238`, `flows/aa887c/scripts/splits/80-messaging/psyche-messaging.md:5`) and a machine mosaic (`flows/108ab0/vision/operational-designMosaic.md:16`, "The message body IS a datom that lands directly in the recipient's prompt as a datom-formatted object. No JSON envelope."; the file's line 3 says verbatim quotes live in the individual entries).

3. `flows/8475a9/vision/datom.md:29`, as in Fork 1 record 3 (2026-10-05; provenance `-- psyche, STT, book comment, 2026-10-05.` at line 31).

4. `flows/26c50c/vision/ethos.md:18`, section "Kinds and compiled conversion boundaries — 2026-09-24" (line 14). Date 2026-09-24.
   > Yeah I meant kinds not traits. If I say traits I mean kinds. They're kind of the same thing but we say kind because I think it's actually more accurate.
   >
   > I want you to design that aspect of everything, or look at the design of it, and look at how enforced the ethos code is. Look at how we make sure that it's the code that runs, that it is compiled in, and that it does what it's supposed to be doing. It makes the code able to lower and lower (and vice versa) from a datom string or from string syntax into a Rust value, or not, depending on whether it has that option turned on during compilation. That way the Nexus doesn't do the string conversion but the CLI does and eventually the user interface will have all of that conversion-to-string logic compiled in.

   Provenance line (20): `-- living, typed directly in this flow.`

### Draft lines at stake (04a895)

```
71: Signal                                         ; what Flow says to Message, on Flow's ordinary socket
75:   Deliver.{ Lock                               ;   write the message into the locked metaflow's flow
76:             Sender
77:             Message } ]
87: Operation                                      ; what Flow does for Message
91:   Write.{ FlowId                               ;   write the message into the current flow
92:           Sender
93:           Message }
```

(The Message type at lines 16-25 is quoted under Fork 1.)
