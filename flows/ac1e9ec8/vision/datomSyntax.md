# Datom syntax

## 2026-08-26 — a map in an expected position carries no Map head

The flow's view showed a map as `Map.[ k.v k.(v) … ]`. The correction:

> If a position expects a map, the data will be [ k.v ... ], no Map.

— psyche, 2026-08-26 (Design session ac1e9ec8), typed.

Asked in the same message, not ruled:

> Is there a scenario in which a Head. isnt a variant?
