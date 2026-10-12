---
description: A flow runs an hm-* command, reads its output, or changes messenger-clj.
dependencies: [vision-messaging]
---

The `hm-*` shorthands are provided by the standalone messenger-clj repository under `Repository root`, on its default branch. Use `hm-send` for flow-to-flow messages, never a shell script, paste, or another intercom.

`FLOW_ID=<self> hm-send TARGET BODY` sends one complete machine body as `#msg [sender machine-prose]`. Use `--stdin` in place of `BODY` for a large or multiline body. `FLOW_ID=<self> hm-send TARGET --psyche CONTEXT VERBATIM` sends the living's words, context first, as one `#psyche [sender context whole-verbatim]`; `--psyche CONTEXT --stdin` reads the verbatim from standard input. `FLOW_ID=<self> hm-send TARGET --psyches --stdin` reads one EDN vector of `[context verbatim]` pairs and sends them as one `#psyches` envelope. Pass message fields, never a prebuilt envelope. `hm-send-abrupt` takes the same arguments and interrupts the target's active turn first. TARGET is the recipient's six-character flow id.

The living's words travel only as psyche, never quoted, paraphrased or summarized inside a `#msg` body. A message that rests on his words sends two messages: the psyche, then the flow's own `#msg`. Write the recipient-facing body only.

Work goes straight to the flow that acts on it next. A flow that finishes a package hands it directly to the flow that turns it into the deliverable, such as a Tertiary book subflow that publishes it. The ordering flow hears only about a blocker, a needed ruling, or the finished deliverable when it asked for that.

Before sending, establish that the recipient holds the work and is live. Before relying on a Codex delivery, establish its supported authenticated binding and Presented receipt.

The typed reply is what hm-send itself prints; a flow never waits on or watches the target for an answer. Report the printed receipt as it is. `Transported` is Herdr's acceptance for the checked binding. `Presented` includes the observed reaction of the target. `Held` means nothing was typed and the whole body is pending until an explicit supported delivery action; its printed reason names the refusal. `RepairRequired` means the recorded candidates must be judged and the route repaired with `hm-repair`. `Uncertain` means the envelope may have arrived: inspect the target and never retry blindly. A refused or undelivered send is reported to the sending flow and its route is mended.

Registration validates one exact live Herdr identity and stores its native binding immediately; send readiness is checked separately.

`FLOW_ID=<self> hm-retire FLOW` takes only the flow id: it reads the route and live Herdr identity itself, writes the evidence file, and prints its path. A refusal prints `RetireRefused.{ FLOW Reason }` and changes nothing.
