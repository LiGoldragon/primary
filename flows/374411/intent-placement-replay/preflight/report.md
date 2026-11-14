# Intent-placement replay preflight

## Observation

The retained `configuration-before.datom` parses as `Configuration` with 19 fields. Its Metaflows field is structurally identical to `metaflows-before.datom`. The payload parses as exactly one `Configure.Metaflows` request.

The baseline and payload each contain 38 declarations in the same address order. All non-module declaration fields are structurally identical. Eleven Field declarations are unchanged. Exactly 27 Psyche/Mind declarations change: each gains one `intent:configuration` system module; `Mind herdrNexus Sol` additionally moves its single `intent:scratch` module from user modules to system modules while preserving the order of all other module entries. `changes.json` names exactly those same 27 addresses in order.

Evidence: `verify_payload.py`, `result.json`, and `sha256.txt` in this directory. This is a parser/structural comparison rather than a text-normalization heuristic.

## Held operation

No owner client was invoked and no configuration was changed. The replay remains held until the validated pinned owner route and exact command contract arrive. A fresh Configuration read and full-family preservation comparison are required immediately before the single authorized replay.
