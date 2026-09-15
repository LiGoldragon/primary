# Item 20 — word and hash library research

**Correction, 2026-09-15:** The earlier aggregate and mean table used the wrong HumanHash alphabet and PGP union capacity and did not preserve the original measured samples. Those claims are withdrawn. The replacement artifact preserves the original per-list measurements; the corrected table below reports each tokenizer separately. Prior 1/2/4-word token projections are withdrawn, not measurements.

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
| PGP biometric | 256 words per alternating even/odd position | 8 bits/word; parity is not extra entropy | [Archived PGPfone appendix](https://web.archive.org/web/20100326141145/http://web.mit.edu/network/pgpfone/manual/index.html#PGP000062); local source records GFDL attribution uncertainty and MIT PGPfone code |
| Niceware | 65536 | 16 bits/word | [Niceware source](https://github.com/diracdeltas/niceware), MIT; the earlier additional SIL provenance claim is withdrawn |
| Mnemonicode v0.7 ordinary list | 1626 (7 reserved entries excluded) | 10.6671 bits/word | [Source at pinned commit](https://github.com/singpolyma/mnemonicode/tree/315aed6f1272cf2afa2eb1e1ed4a8879a49e5a6c); source carries MIT license and declares wordlist v0.7 |
| HumanHash measured default list | 256 | 8 bits/word; lossy digest projection | Original per-list witness `measurements-human-proquint.json`; the prior BIP39 projection did not describe this measured list |
| Proquint CVCVC | 65536 possible 16-bit quints | 16 bits/quint | [Proquint source](https://github.com/dsw/proquint/tree/af91d5bb77c182504a1cda5bdb11b2d3a5edb96a); 16 consonant and 4 vowel choices; source `License.txt` governs |

BIP39's 11-bit index is not 11 independent application bits in every valid mnemonic because checksum bits and fixed sentence lengths apply. A BIP39 alphabet may be a candidate for readable object references, but a three-word object reference is not thereby a BIP39 wallet mnemonic.

## Measured tokenizer sample

The primary measured sample is ten deterministic three-word triples for every table row. The 1–4 planning columns below are capacity and separator projections; they must not be read as a four-word production benchmark. Counts are actual `tiktoken 0.12.0` results, not byte proxies. The exact production Codex model-to-encoding mapping remains unwitnessed and Claude's tokenizer remains unmeasured. The samples compare separator/list behavior; they are not an equal-entropy benchmark. The tokenizer source is [OpenAI tiktoken tag 0.12.0](https://github.com/openai/tiktoken/tree/97e49cbadd500b5cc9dbb51a486f0b42e6701bee), [MIT licensed](https://github.com/openai/tiktoken/blob/97e49cbadd500b5cc9dbb51a486f0b42e6701bee/LICENSE).

## Hash and identifier comparison

- SHA-256 or another cryptographic content hash provides a digest and collision resistance. Keep it as an independent binary/content value; a hex projection is not a readable name.
- Nano ID 6.0.1 provides cryptographically random URL-safe identifiers and custom alphabets ([source](https://github.com/ai/nanoid/tree/03cdf5295dccf0d47415fee0e6427578fdb34e64), [MIT license](https://github.com/ai/nanoid/blob/03cdf5295dccf0d47415fee0e6427578fdb34e64/LICENSE)). It is an ID generator, not a wordlist or content checksum.
- Hashids is a reversible number-to-symbol presentation scheme ([official organization](https://github.com/hashids)). It is not a cryptographic hash or arbitrary-content collision resistance.
- HumanHash is a lossy XOR-style recognition projection. Its words improve recognition while the full digest remains authoritative; it does not authenticate or reversibly identify content.
- Proquint encodes 16-bit groups into pronounceable CVCVC forms. It has no finite dictionary licensing issue, but pronunciation and delimiter rules remain part of the wire contract.

## Conditional recommendation and collision contexts

If the priority is model-token cost plus a mature readable alphabet, the measured matrix favors the 2048-word BIP39 English alphabet in this comparison. Use it only as a pinned object-reference alphabet with a legal separator and explicit list version; do not call a three or four word reference a valid BIP39 wallet mnemonic. Use three words only for a local, collision-checked short reference that expands to a full query. Under the illustrative `N <= 1000`, `p <= 2.84e-8` budget, four 11-bit words provide 44 raw bits. Under `N <= 1e6`, `p <= 3.31e-12`, seven such words provide 77 raw bits. These are recommendations, not facts or living width rulings. If phonetic separation outweighs token cost, prefer the PGP or Diceware family only after its list terms and pronunciation policy are pinned. For a public canonical identifier, retain the full 256-bit digest; if a word encoding is needed, a valid 24-word BIP39 mnemonic carries 256 entropy bits plus checksum bits, and authentication remains separate. Do not alias a readable word name to a digest or claim that a short projection authenticates its source.

These are illustrative sizing scenarios, not living rulings. For `N` issued identifiers and `b` uniform random bits, expected collision pairs are `N(N-1)/2^(b+1)`; the small-risk approximation is not an exact probability. Choose `b` using `ceil(log2(N(N-1)/(2p)))`, then account for adversarial control, retryability, and collision detection.

| Context | Population | Candidate space | Approximate accidental risk | Rule |
|---|---:|---:|---:|---|
| Local controlled | 1,000 | 36-bit readable projection | 7.27e-6 | Detect and retry; issuer controls namespace |
| Cluster | 1,000,000 | 64 bits | 2.71e-8 | Detect centrally or use disjoint issuer namespace |
| Public | 1,000,000,000 | 128 bits | 1.47e-21 | Cryptographic randomness plus separate authenticity; content hashes can use 256 bits |

The identifier is not a secret and does not authenticate an object by itself. At `10^12` public identifiers, 128 bits gives approximately `1.47e-15` accidental collision risk; this illustrates why population and threat model remain explicit.

## Corrected capacity and mean token counts

Capacities are raw vocabulary capacity; counts are ten actual three-word, space-separated IDs without an initial space, seed10. Mnemonicode triples encode32 payload bits, versus32.001 raw vocabulary bits; BIP39 three/four words are not valid wallet mnemonics. Six/eight hex characters carry24/32bits; six base32 characters carry30bits.

| List | Bits/word | 1 word | 2 words | 3 words | 4 words | cl100k mean | o200k mean | cl bits/token | o bits/token |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BIP39 | 11.000 | 11.000 | 22.000 | 33.000 | 44.000 | 3.60 | 3.60 | 9.167 | 9.167 |
| eff-long | 12.925 | 12.925 | 25.850 | 38.774 | 51.699 | 5.20 | 5.00 | 7.457 | 7.755 |
| eff-short | 10.340 | 10.340 | 20.680 | 31.020 | 41.359 | 4.00 | 3.60 | 7.755 | 8.617 |
| SKEY-RFC1760 | 11.000 | 11.000 | 22.000 | 33.000 | 44.000 | 5.80 | 5.60 | 5.690 | 5.893 |
| Niceware-65536 | 16.000 | 16.000 | 32.000 | 48.000 | 64.000 | 7.30 | 7.30 | 6.575 | 6.575 |
| Mnemonicode | 10.667 | 10.667 | 21.334 | 32.001 | 42.668 | 4.10 | 4.00 | 7.805 | 8.000 |
| Diceware-original | 12.925 | 12.925 | 25.850 | 38.774 | 51.699 | 5.20 | 4.80 | 7.457 | 8.078 |
| humanhash | 8.000 | 8.000 | 16.000 | 24.000 | 32.000 | 4.70 | 4.50 | 5.106 | 5.333 |
| proquint | 16.000 | 16.000 | 32.000 | 48.000 | 64.000 | 7.10 | 6.30 | 6.761 | 7.619 |
| PGP-alternating | 8.000 | 8.000 | 16.000 | 24.000 | 32.000 | 5.20 | 5.10 | 4.615 | 4.706 |
