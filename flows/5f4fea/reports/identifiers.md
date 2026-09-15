# Identifier Types Proposal

Status: proposal only. No Datom primitive, Ethos library, flow-id command, Orchestrate record, or runtime encoding is changed.

## Living direction

The living's complete current statement is recorded in [flows/692df8/vision/identifiers.md](/home/li/primary/flows/692df8/vision/identifiers.md). It asks for readable alphanumeric or sayable symbols or words, identifier types rather than strings, three security contexts, and a protocol owned by Signal while Sema stores typed binary Signal.

The three contexts are local/private, cluster, and public. They affect collision cost, retryability, and adversarial control. An identifier is not a secret and does not authenticate itself.

## Evidence and limits

The inspected Protos source at `/home/li/wt/github.com/LiGoldragon/protos/e2-default-bodies-01a04a30/src/lib.rs` has `ContentHash(u64)` (line 16), `Symbol(String)`, `Separator` with period, exclamation, and colon, and `BareExpectation` with `Symbol`/`String`. `Symbol` conversion (lines 251–270) requires a complete bare symbol. Its private `ContentHash` implementation (lines 944–959) is a standard-library FNV1a-like `u64` hash and is not cryptographic. This is existing source evidence, not a chosen identifier primitive.

Datom legality is position-sensitive. A legal object identifier symbol excludes colon, dot, and other delimiters under the proposed object grammar; a datom bare string can permit colon, so these are distinct policies. No arbitrary-Unicode or all-scalar claim is made. UTF-8 bytes, code points, display cost, and model-token cost are separate measures. The identifier policy settles only model-token cost as its optimization objective; it does not substitute bytes or characters for token counts.

## Candidate identifier library

The following is one complete sweet-form `Library` candidate. The imports are explicitly future imports: these modules and primitives do not currently exist in the inspected Protos source. Widths are candidate choices, not living rulings.

```text
Library
[ signal-standard:[ Identifier36 Identifier64 Hash256 ] ]
[ FlowId.{ Identifier64 }
  ClusterId.{ Identifier36 }
  ProvenanceId.{ Hash256 }
  SourceEventIdentifier.{ Hash256 }
  CompactReference.{ Identifier36 } ]
[]
[]
```

The nominal wrappers prevent identity-bearing values from being aliases to `String`. `signal-standard` and its three primitives are future and absent. Their required contract is a fixed logical width, canonical encoding and decoding, collision scope, and an independent binary value distinct from any surfaced digest. `FlowId` and `ClusterId` widths are illustrative scenario choices; `ProvenanceId`, `SourceEventIdentifier`, and the compact reference representation remain candidate design points. There is no `Vector<Integer>` bytes field or runtime bit-width disguise here. The proposed library has not been implemented or imported, and no claim is made that this candidate generator compiles today.

The existing Ethos parser can parse an external import path syntactically, but the corresponding Rust library and identifier definitions are absent. No generated code or import is claimed.

## Context sizing examples

These are illustrative assumptions for choosing a width, not limits or policy. For a namespace with `N` active values and acceptable accidental collision-pair risk `p`, the expected collision pairs are `N(N-1)/2^(b+1)` and the small-risk approximation is `N(N-1)/2^(b+1)`. The exact birthday probability is `1 - product(k=0..N-1)(1-k/2^b)`; width should be selected as `ceil(log2(N(N-1)/(2p)))` only within the small-risk approximation.

| Context | Illustrative N | Candidate space | Approx. collision-pair risk |
| --- | ---: | ---: | ---: |
| Local/private | 1,000 | 36 bits | 7.27e-6 |
| Cluster | 1,000,000 | 64 bits | 2.71e-8 |
| Public | 1,000,000,000 | 128 bits | 1.47e-21 |

There are no living `N` limits. A public namespace of `10^12` would still be about `1.47e-15` expected pairs at 128 bits. Content hashes targeting roughly 128-bit generic collision resistance call for 256 cryptographic bits, while the identifier's human-readable encoding and authenticity mechanism remain separate decisions.

Readable alphabets can be compared after the repertoire is settled: base32 carries 5 bits per symbol, base36 about 5.17, base62 about 5.95, and base64 6. A 2,048-word list carries 11 bits per word and a 7,776-word list about 12.925. These are entropy figures, not token counts. Exact Claude/Codex token costs remain unmeasured.

## Message report dependency

The provisional Message candidate imports `Hash256`, `SourceEventIdentifier`, and `CompactReference` from this proposed library instead of declaring identifier aliases as `String`. `SourcePath`, `SourceTime`, `SourceFormat`, and `RawPromptText` remain strings because they are paths, timestamps, format labels, and textual content.

The existing relay witness's SHA-256 hex value is legacy display evidence:

```text
d19f5a5d4f9636ee577592ca646d26b445160f80e227a3e4bee8a8385ccc55d0
```

It is not presented as the proposed UTF-8-base encoding. The compact `d19f5a` form remains a scoped legacy illustration pending the library's alphabet, width, normalization, and resolution rules. The source event's canonical 949 UTF-8-byte text and SHA-256 are already witnessed in [relay-extraction.md](/home/li/primary/flows/5f4fea/witnesses/relay-extraction.md).

## Flow and bookkeeping vocabulary

For later Orchestrate design, the proposed vocabulary is `Claim.FlowClaim` and `Flow.{ ClusterId Harness FlowId Option<FlowId> }`; it contains no `Seat`. This is a proposal only. The current flow-id tool and existing records are not changed.

## Open choices and measurement gap

- exact Signal-owned hash primitive and its Datom representation;
- legal alphabet, normalization, and word-list policy;
- width, padding, and partial-symbol rules for each context;
- whether wrappers carry domain and generation data;
- authenticity and collision-retry protocol;
- supported Claude/Codex tokenizer method and exact model mapping.

No default Python tokenizer libraries or local Claude/OpenAI tokenizer mapping was found in readiness research. Exact model-token measurements therefore remain pending; byte or character counts must not be reported as token counts.

## Sources

- `/home/li/primary/flows/692df8/vision/identifiers.md`
- `/home/li/primary/Vision/datom.md`
- `/home/li/wt/github.com/LiGoldragon/protos/e2-default-bodies-01a04a30/src/lib.rs`
- `/home/li/primary/flows/5f4fea/witnesses/relay-extraction.md`
- `/home/li/primary/flows/5f4fea/reports/message-ethos.md`
