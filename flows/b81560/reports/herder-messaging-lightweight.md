# Herder messaging — lightweight report

Flow b81560, 2026-09-19. Synthesized from Mind Astra 0ab019 (components),
Psyche Fable c8d79f (design), Psyche b81560 (coordination).

## What we see

Every message today is text pushed into a pane by a client that looked the
pane up itself. Three separate systems do this: Hacky Messenger (hm-send),
the bash central messenger (tools/msg, dead — its pane w4:p3 is gone), and
raw herdr agent prompt. None of them know who is alive. A refresh starts a
successor and leaves the ancestor registered and addressable, so messages
wake the dead and waste power.

Meanwhile, the actual infrastructure is running and empty: Message Nexus
(0.12, two sockets, persisted receipts) and Flow Nexus (two sockets, flow
resolution) are both live but have zero registered flows. The capability
exists — registration, delivery, receipts — nobody uses it.

## The target shape

**Flow owns Herder.** Flow is the only client of Herder. The living does
not create panes or name them; the living opens Herder to look and to type.
Flow starts sessions, lays out workspaces, names panes, and closes them.

**Messages go through Message Nexus, which resolves through Flow Nexus.**
No client ever looks up a pane. A flow sends `Submit.{ To Priority Body }`
to Message; Message asks Flow for the live binding; Flow delivers through
its own `Prompt` operation. Dead panes are never in the table.

**Named routing with succession.** Two kinds of name: Seat (PsycheHigh,
MindMedium, FieldLow — outlives every flow) and FlowId (born at start,
dead at end — never passes on). A model name like PsycheFable is an alias
of a seat. When the model changes, the alias rebinds; nothing routed by
seat changes. Messages to a refreshing seat are held until it binds.

**The living's words enter as PsycheInput** through Unity → Mentci →
Persona → Message, with the Ingress stamped so every flow knows it is
hearing the living.

## Questions to the living

1. Is the seat set (high/medium/low/ultra-low per component) the wire
   naming, or do you want model tier names (Fable/Astra/Sol/Terra/Luna)
   as seats with the component as prefix?
2. Does PsycheFable retire when Fable leaves the high seat, or follow
   Fable to whatever seat it fills?
3. Should Flow's Prompt be the only writer into a pane from day one
   (even while Flow's implementation is a shell calling herdr agent
   prompt), or does Hacky Messenger keep writing until Flow's Herder
   client exists?

## Sources

- Mind Astra 0ab019: live CLI/process/socket receipts, source inspection
  of message 0.12 and flow-nexus
- Psyche Fable c8d79f: flows/c8d79f/herder-messaging-target-shape.md
- Mind Sol effa1b: initial infrastructure probe
