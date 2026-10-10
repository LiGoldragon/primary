# ClaviFaber current-Datom migration

ClaviFaber `main@origin` is `2203f677d3448d99269d66386d35683cd10a05ef`.
It replaces the direct legacy Dotos dependency and text boundary with
`datom-codec` `41a3c073d5c5cdcb3ebb1a5c842e8c068145fdb2`, Protos
`2d999f173334`, and generated Rust from `ethos/clavifaber.ethos` using
Ethos-zero `bcf728bbe4521e663f4773d3c1fd4ebb643df32e`.

The CLI accepts one generated `ClaviFaberRequest` Datom and prints one
generated `ClaviFaberResponse` Datom. The six variants retain their prior
operations and idempotency rules. The public result is now the direct
generated `PublicKeyPublication` Datom at `publication.datom`, atomically
written at mode 0644. It is an explicit public-file cutover:
`publication.dotos` is neither read as the new file nor rewritten. No
rkyv/redb record exists in this producer; the only durable boundary audited is
this public text file.

Consumers decode that file directly with
`datom_codec::Potential::<clavifaber::generated::clavifaber::PublicKeyPublication>::from(text)`
followed by `actualize(IncorporationBudget::try_from(16_384)?)`. The producer
does not expose a compatibility reader CLI or an envelope around the record.

The consumer handoff is deliberately split. Horizon holds the CriomOS
`complex.nix` request/publication-reader change and pin; its staged consumer
was pending this immutable producer ref when this record was written. C6 is
external's fixture and remains pending the combined OS consumer revision. This
producer record does not claim either consumer gate.

The final source change is forward-only `2203…`: it adds a decoder-only test
for the six literal current-Datom operator examples. `2203…` has the 28-test
local formatter/clippy receipt and the attached remote Nix-check receipt. The
two packaged isolated apps ran at `8ed3…`, the immediately preceding
writer/package source. `2203…` changes only `tests/request_surface.rs`; this
record does not infer packaged-derivation identity from that source fact. The
paired witness records the revision-scoped receipts separately.

The repository skill at
`/home/li/wt/github.com/LiGoldragon/clavifaber-datom-542442/skills.md` is an
authored instruction source. It remains unmodified. The separate review-only
[skill review](clavifaber-skill-review.md) and
[patch](clavifaber-skill-review.patch) record its source hash and proposed
current-Datom wording for later approval.
