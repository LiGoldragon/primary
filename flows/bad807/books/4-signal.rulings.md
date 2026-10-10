# «Signal»: rulings

1. What a Signal's two sections are called.
   (a) Queries and responses: 2026-09-09, 564f55, "it's a query and a response"; 2026-09-26, b7ba00, asked again as "Queries and responses".
   (b) Requests and replies, or requests and responses: 2026-09-10, fe34eb, "signal defines the requests and the replies"; 2026-09-13, 024bc7, "the requests and the responses".
2. What input and output name.
   (a) Too low-level for signal, good names for the computing inside the core: 2026-09-09, 564f55.
   (b) No part: the middle part is operation, whose sections ethos-zero 16.0.0 reads as operations and outcomes, marked "not yet the living's word": 2026-10-04, 5ed94b, his three-part words.
3. What the privileged socket is called.
   (a) Meta socket: 2026-08-26, 01a03d6e, and "fairly reasonable for now" on 2026-10-03, edf227.
   (b) Owner socket: in no record of his; in code since 2026-06-05 (Lojix `LOJIX_OWNER_SOCKET`) and 2026-09-26 (Message 0.15.0, `message-owner.sock`).
4. Whether the wire protocol is decided.
   (a) Decided as built: the length-prefixed rkyv frame and the digest greeting, in `signal` since 2026-09-12 (`e1a8302`).
   (b) To be decided: `Vision/signal.md` "Protocol", landed 2026-09-09; 2026-08-08, 55d18f4f, "we need to flesh that out better too".
5. Whether any Nexus touches datom.
   (a) Never: 2026-09-09, 564f55, the Nexus "is not going to do the textualization at all".
   (b) A Nexus that hands a datom into a prompt must make the text: 2026-10-03, 5578cc (a notion), "how does Nexus send datom to places"; `flow-nexus` does so today.

## Summary

1. `Vision/signal.md` "Query and response": queries are verbs, responses their past tense, refusals name themselves; example adds a forms section.
2. `Vision/signal.md` new "Simple and extended forms": one datum, two containers; the extended adds the flow id.
3. `Vision/signal.md` "Meta signal" becomes "Sockets": one contract per socket, configuration only over the meta socket, local only.
4. `Vision/signal.md` "Protocol" becomes "The frame": four-byte length, rkyv root, digest greeting, exchange ids.
5. `Vision/signal.md` "Text and signal": datom kinds compiled out of the Nexus; the Nexus a package apart from its CLIs.
6. `Vision/signal.md` new "The caller": the CLI carries the calling process; no flow says who it is.
7. `ethos-zero/README.md` "File variants": the Signal root gains a forms section generating `Form<T>`.
8. `signal-harness/ethos/signal.ethos` queries: noun heads become verbs; 9.0.0.
9. `message` configuration and meta CLI: `message-owner.sock` becomes `message-meta.sock`.
10. `Curriculum/skills/vision-nexus.md` line 12: the Signal sentence names the frame, greeting, exchanges and the two forms.
