# Datom syntax

## 2026-08-26 — a map in an expected position carries no Map head

The flow's view showed a map as `Map.[ k.v k.(v) … ]`. The correction:

> If a position expects a map, the data will be [ k.v ... ], no Map.

— psyche, 2026-08-26 (Design session ac1e9ec8), typed.

Asked in the same message, not ruled:

> Is there a scenario in which a Head. isnt a variant?

## 2026-08-26 — considering positional key/values in a map

> Im considering making key/values resolve by position in a map
>
> [ key value second-key second-value ... ]
>
> that looks cleaner and makes the Head. always a variant; lower
> cognitive cost

— psyche, 2026-08-26 (Design session ac1e9ec8), typed. Under
consideration, not ruled.

## 2026-08-26 — or a dedicated delimiter for maps

> or we could use one of the unused delimiters for maps, making them
> easy to spot visually

— psyche, 2026-08-26 (Design session ac1e9ec8), typed. Under
consideration, not ruled.
