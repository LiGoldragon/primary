# Remaining portable Datom consumers

`primary-xqj.7` migrated the three missed portable consumers from retired
`datomic`/Dotos to `datom-codec` `41a3c073d5c5cdcb3ebb1a5c842e8c068145fdb2`,
Protos `2d999f17`, and Ethos-zero `bcf728bbe4521e663f4773d3c1fd4ebb643df32e`.
Each repository is now on its tested producer main:

| Repository | Main revision | Public boundary |
| --- | --- | --- |
| relative-age-display | `99d184541ed8b71daeafd44f025cdaafe7ecef82` | Typed `HumanReadableTime` parse/render |
| Chroma | `c9c11a5b5724bc28e402a48615c2f0d1a7b40813` | Generated typed Datom CLI request/reply, unchanged rkyv daemon frame |
| Chronos | `a5cf51f440a722c60963a5f1a0ea95bb3251ddb0` | Generated plus range-checked typed Datom CLI request/reply, unchanged rkyv UDS frame |

Chroma and Chronos regenerated their authored Ethos projections and retain
manual numeric/domain validation where a generated scalar would not express
the range invariant. Both have a breaking public text-codec version bump
(Chroma 0.4.0; Chronos 0.3.0) and migration notes. Relative-age-display is
0.5.0.

Durable-layout audit was source-only; no live state was opened. Chroma's redb
tables archive only unchanged runtime records: theme mode/revision, warmth and
brightness primitives, and raw latitude/longitude. They contain no generated
or Protos value. Chronos has a redb dependency and future-store comments but
no `Database`, `TableDefinition`, or read/write operation in its source.
Relative-age-display has neither rkyv nor durable storage. The text codec
migration therefore does not create a demonstrated stored-archive upgrade.

No deployment or runtime mutation occurred.
