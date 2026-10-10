
## Reload sessions when idle through hooks

Context: relayed by Psyche Opus 7328f4 on 2026-09-30 from the living's comments on Psyche Fable's book “What Waits on You”; this bears on the flow-state design.

> "we want to avoid polling, which means we're going to make this hook-based. ... sessions can be reloaded in the new harness one at a time as they go idle."

-- psyche, STT.

## Full page comment recovered

Context: exact fuller quote recovered from flows/7328f4/vision/hooks.md, page comment 2026-09-30T18:47; it supersedes the abbreviated relay above without erasing it. The originating record marked “tab update” [sic].

> "Yeah obviously, the seats are not going to be cut off … Essentially we want to avoid polling, which means we're going to make this hook-based. When an order comes in, this will be controlled by Flow obviously. When that order comes in, we need to upgrade the harness. Then sessions can be reloaded in the new harness one at a time as they go idle. As soon as the session goes idle, the hook kicks in. It gets locked for the next order tab update [sic], which essentially locks it from getting sync messages, right? It would wait until it stops because the restart will happen and then the message will just come through. This will tie into how context size will essentially start triggering the unwind. Then we'll have a whole way of passing the right transcript, either passing it over or selecting what transcript to pass depending on what the next flow will specialize in."

-- psyche, STT.

## Provenance correction

The entry headed “Full page comment recovered” above reproduces the longer preserved excerpt in flows/7328f4/vision/hooks.md. Its ellipsis is an omission in that source; this flow has not independently recovered the omitted words or read the live page.

## Flow state without polling

Context: relayed by Psyche Opus 7328f4 on 2026-09-30; speech-to-text corrections supplied in brackets.

> "I've reset Codex and we need to also start working on the hook/[Herdr] functionality for getting the state of what's happening in a flow as cheaply as possible, with no polling. We really wanted to [de-emphasize] polling and if we do poll it would be a really long period and it'll be for something really important."
