# Item 20 — word and hash library research

Status: research witness and comparison. No identifier implementation or library dependency is selected. Measurements use an existing Nix Python 3.14 environment with `tiktoken 0.12.0` (seed 10, `cl100k_base` and `o200k_base`). The reproducible JSON artifact is `../witnesses/item20-token-measurements.json`.

## Word-list sources and raw capacity

Raw capacity is `log2(list size)` under uniform selection. It is separate from valid checksummed payload capacity, readability, normalization, spelling or phonetic error policy, separators, and list version.

| Source/list | Observed size | Raw capacity | Source and license boundary |
|---|---:|---:|---|
| Bitcoin BIP-0039 English | 2048 | 11 bits/word | [BIP-0039](https://github.com/bitcoin/bips/tree/173f386dfb8b4f1c4b16d69190a753802802ac4d/bip-0039); [Rust bip39 2.2.2](https://docs.rs/bip39/2.2.2/bip39/) records the embedded list as CC0 |
| EFF long Diceware | 7776 | 12.9248 bits/word | [EFF wordlist page](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases); preserve its data terms when redistributing |
| EFF short Diceware | 1296 | 10.3399 bits/word | Same EFF source and terms |
| Original Diceware | 7776 | 12.9248 bits/word | [Reinhold Diceware source](http://world.std.com/~reinhold/diceware.html); source license needs verification before redistribution |
| S/KEY RFC 1760 | 2048 | 11 bits/word | [RFC 1760](https://www.rfc-editor.org/rfc/rfc1760); OTP vocabulary, not a general identifier checksum |
| PGP biometric | 510 extracted; source describes two 256-word lists | 8.9944 observed bits/word; 8 bits/list target | [Archived PGPfone appendix](https://web.archive.org/web/20100326141145/http://web.mit.edu/network/pgpfone/manual/index.html#PGP000062); local source records GFDL attribution uncertainty and MIT PGPfone code |
| Niceware/SIL-derived | 65536 | 16 bits/word | Local source header identifies SIL-derived English words and Yahoo End-to-End; [project source](https://github.com/yahoo/end-to-end), MIT code notice; upstream data terms require verification |
| Mnemonicode v0.7 ordinary list | 1626 (7 reserved entries excluded) | 10.6671 bits/word | [Source at pinned commit](https://github.com/singpolyma/mnemonicode/tree/315aed6f1272cf2afa2eb1e1ed4a8879a49e5a6c); source carries MIT license and declares wordlist v0.7 |
| HumanHash BIP39 projection | 2048-word BIP39 alphabet | 11 bits/word alphabet; 8-bit digest input per displayed word in the reviewed XOR-style projection | [HumanHash source](https://github.com/deepgram/humanhash/tree/a957845d0df71a60f1e0387d15bc36c0fc7b4620); code is public domain/Unlicense and the embedded BIP39 list is separately attributed |
| Proquint CVCVC | 65536 possible 16-bit quints | 16 bits/quint | [Proquint source](https://github.com/dsw/proquint/tree/af91d5bb77c182504a1cda5bdb11b2d3a5edb96a); 16 consonant and 4 vowel choices; source `License.txt` governs |

BIP39's 11-bit index is not 11 independent application bits in every valid mnemonic because checksum bits and fixed sentence lengths apply. A BIP39 alphabet may be a candidate for readable object references, but a three-word object reference is not thereby a BIP39 wallet mnemonic.

## Measured tokenizer sample

The artifact contains ten three-word samples for every table row, with counts for space, hyphen, and no separator under both observed encodings. The counts are actual `tiktoken 0.12.0` results, not byte proxies. The exact production Codex model-to-encoding mapping remains unwitnessed and Claude's tokenizer remains unmeasured. The samples compare separator/list behavior; they are not an equal-entropy benchmark. The tokenizer source is [OpenAI tiktoken tag 0.12.0](https://github.com/openai/tiktoken/tree/97e49cbadd500b5cc9dbb51a486f0b42e6701bee), [MIT licensed](https://github.com/openai/tiktoken/blob/97e49cbadd500b5cc9dbb51a486f0b42e6701bee/LICENSE).

## Hash and identifier comparison

- SHA-256 or another cryptographic content hash provides a digest and collision resistance. Keep it as an independent binary/content value; a hex projection is not a readable name.
- Nano ID 6.0.1 provides cryptographically random URL-safe identifiers and custom alphabets ([source](https://github.com/ai/nanoid/tree/03cdf5295dccf0d47415fee0e6427578fdb34e64), [MIT license](https://github.com/ai/nanoid/blob/03cdf5295dccf0d47415fee0e6427578fdb34e64/LICENSE)). It is an ID generator, not a wordlist or content checksum.
- Hashids is a reversible number-to-symbol presentation scheme ([official organization](https://github.com/hashids)). It is not a cryptographic hash or arbitrary-content collision resistance.
- HumanHash is a lossy XOR-style recognition projection. Its words improve recognition while the full digest remains authoritative; it does not authenticate or reversibly identify content.
- Proquint encodes 16-bit groups into pronounceable CVCVC forms. It has no finite dictionary licensing issue, but pronunciation and delimiter rules remain part of the wire contract.

## Recommendation and collision contexts

Choose a nominal typed binary identifier first, then a readable projection with a pinned list and separator. Do not alias a readable word name to a digest, and do not claim that a short projection authenticates its source. A three-word local reference can be collision-checked and expanded to a full query; it is not a universal primary ID. Public authentication retains the strong full hash.

These are illustrative sizing scenarios, not living rulings. For `N` issued identifiers and `b` uniform random bits, expected collision pairs are `N(N-1)/2^(b+1)`; the small-risk approximation is not an exact probability. Choose `b` using `ceil(log2(N(N-1)/(2p)))`, then account for adversarial control, retryability, and collision detection.

| Context | Population | Candidate space | Approximate accidental risk | Rule |
|---|---:|---:|---:|---|
| Local controlled | 1,000 | 36-bit readable projection | 7.27e-6 | Detect and retry; issuer controls namespace |
| Cluster | 1,000,000 | 64 bits | 2.71e-8 | Detect centrally or use disjoint issuer namespace |
| Public | 1,000,000,000 | 128 bits | 1.47e-21 | Cryptographic randomness plus separate authenticity; content hashes can use 256 bits |

The identifier is not a secret and does not authenticate an object by itself. At `10^12` public identifiers, 128 bits gives approximately `1.47e-15` accidental collision risk; this illustrates why population and threat model remain explicit.
