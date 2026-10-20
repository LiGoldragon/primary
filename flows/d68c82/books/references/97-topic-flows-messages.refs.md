# References: Topic flows, a design Fable, and messages from files

## The living's words

- flows/d68c82/vision/flow.md, "Specialized Opus topic flows, consulting a fresh Fable for design" (typed): use specialized Opus flows for specialized topics; refresh your flow because you are quite old; keep track of these specialized Opus topics; once in a while they can consult a fresh clean Fable used only for designing; once they have everything together that Fable needs to create a design, they send it all to Fable. Proposals 1 and 2.
- flows/d68c82/vision/messenger.md, "A message can insert files instead of re-typing them" (typed): a way for the messenger to insert files instead of the model outputting all those tokens; message types creating a vector of messages, each with its type defined in the call, which can use a file instead of being typed; reuse content from files. Proposals 4 and 5.
- flows/d68c82/vision/flow.md, "A main flow is a manager, not a doer" (2026-10-16): the neighbouring statement behind proposal 1; the subflow should send the message it holds rather than the main flow retyping it.
- flows/d68c82/vision/flow.md, "The simplified flow has no regular tool" and "A simplified flow" (book comments, 2026-10-19): a simplified flow has no regular tool; its response is its message. Proposal 2 relies on it.
- flows/d68c82/vision/messenger.md, "A message means something" (2026-10-16): background to sending only messages that carry meaning.

## Current modules, as psyche-context has them (6c8e266)

- vision/flow.md: line "A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message." (Starting flows); paragraph "A topic never dies; it goes idle ..." (What it does).
- vision/model-roles.md, Claude side: "Sonnet launches Sonnet and Haiku. Opus launches Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow ever launches a Fable subflow." The conflict with proposal 2.
- vision/subflows.md: only the long-term line that actual flows replace the harness subagent tool; says nothing on topic flows.
- vision/messaging.md is the only messenger vision module found; it holds the datom message, priority, delivery, witness, "only messages that act" and the six-character hash. Nothing on a body from a file.
- vision/book.md: the form this book follows.
- No vision module names a topic flow or a design Fable; no module tracks which topic flows exist.

## How hm-send works today (messenger-clj working tree, uncommitted edits; read, not run)

- Forms: send TARGET BODY; send TARGET --stdin; send TARGET --psyche CONTEXT (VERBATIM|--stdin); send TARGET --psyches --stdin. Option --psyches requires --stdin; --psyche and --psyches are exclusive. README example: printf '%s' '[["context" "whole verbatim"]]' | FLOW_ID=<self> bin/messenger-clj send TARGET --psyches --stdin. hm-send is a link to the same launcher.
- Types (src/data_readers.clj, malli in core.clj): #msg ["origin" "text"]; #psyche ["origin" "context" "verbatim"]; #psyches a vector of #psyche triples; the --psyches input is an EDN vector of [context verbatim] pairs, read as plain EDN without tags.
- Body is read by slurp of stdin or the positional argument. No --file option; unknown flags are refused. A file can be sent today as hm-send TARGET --stdin < file.
- Limits: no character cap; the only limit in code is a Herdr request of 1 MiB (RelayOverflow, message held). Fields reject control characters other than newline and tab, and reject a field that is itself a complete #msg, #psyche or #psyches form.
- Sender is the FLOW_ID environment variable; target is a flow id or one quoted "Aspect Topic Layer" string.
- signal-message is the Rust Nexus contract and is not the hm-send path.
- The `--messages` flag, the `[:msg ...]` and `[:psyche ...]` entries and the `{:file ...}` body in the book's example are proposed; none exists.

## The earlier book

- 85-lean-flow.md: the earlier simplified-flow (lean flow) book, with the alternatives group and an inquiry module whose open question named the supervising flow at which layer and model, citing the model-roles line "no flow ever launches a Fable or an Astra subflow". The simplified flow has since landed in vision/flow.md; this book closes the Fable part of that question as alternatives.

## Origin of the numbering

The brief named four proposals; the consult of a fresh Fable and the change to the model-roles line are two files, so they are proposals 2 and 3 here and the messenger and inquiry follow as 4 and 5.
