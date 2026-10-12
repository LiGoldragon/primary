---
name: vision-model-roles
description: Which model seat thinks, designs, delegates or speaks to the living is decided, or a model is named natively.
dependencies: []
---

## Roles are explained by layer, not by model

Roles are explained by layer, not by model; one skill maps layer to model.

| Layer | Claude (Psyche) | OpenAI (Mind, Field) |
|---|---|---|
| Primary | Fable | Astra |
| Secondary | Opus | Sol |
| Tertiary | Sonnet | Luna |
| Quaternary | Haiku | Luna, low effort |

Every seat runs at medium effort, except the OpenAI Quaternary.

## Delegation ceiling

Each layer has a ceiling on what subflows it may launch. Conservative by
default: prefer the lower layer.

### OpenAI side

Luna launches only Luna. Sol is not
launched lightly; it is getting expensive. Astra launches Sol and Luna — try Luna first. Astra is main-flow only: no flow ever
launches an Astra subflow.

### Claude side

Sonnet launches Sonnet and Haiku. Opus launches
Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
ever launches a Fable subflow.

## One declaration sets the model everywhere

The model is declared once, as typed configuration in Flow, mutated only
through the meta wire. Skill variables carry that value by name into every
skill, launcher and brief. Nothing else holds a model name, so a launcher
never writes one by hand and no flow is born on a seat by accident.

## Native names use aspect, topic and layer

Every native main session is titled `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`.
The layer selects the configured model through the table above, so the
title names the layer, never the model.

Horizontal communication joins aspects at the same layer.
Vertical communication stays within one aspect and normally advances one layer
at a time. If the adjacent layer is absent or unavailable, routing advances to
the next running layer in that direction, so a Tertiary may reach the Primary
when the Secondary is not running. The missing layer is reported as a gap; it
does not make the message disappear.

Aspect, topic, layer, exact model identifier, Flow ID, and native binding
remain separate typed facts. The title grants none of the identity,
authority, availability, or routing those facts establish.

Horizontal routing selects the unique eligible cell in the target aspect at
the sender's layer. Vertical routing selects the nearest eligible
layer in the requested direction within the same aspect. Busy is still
eligible. Missing or unavailable needs fresh lifecycle and route evidence.
Multiple bindings for one cell are an unresolved conflict, never fanout. No
eligible cell yields an explicit undeliverable result. Resolve the binding
immediately before each attempt. A fallback has succeeded only when the exact
recipient accepts it; an ambiguous attempt remains attached to that recipient
and is reconciled instead of being resent to another layer.
