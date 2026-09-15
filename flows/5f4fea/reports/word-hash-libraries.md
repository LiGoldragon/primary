# Item 20 — word and hash library research

Status: research witness and comparison. No identifier implementation or
library dependency is selected by this report. Measurements were made in an
existing Nix Python 3.14 environment with `tiktoken 0.12.0` (seed 10,
`cl100k_base` and `o200k_base`). The reproducible JSON artifact is
`../witnesses/item20-token-measurements.json`.

## Word-list sources and raw capacity

| Source/list | Observed size | Raw capacity | Source and license boundary |
|---|---:|---:|---|
| Bitcoin BIP-0039 English | 2048 | 11 bits/word | [BIP-0039](https://github.com/bitcoin/bips/tree/173f386dfb8b4f1c4b16d69190a753802802ac4d/bip-0039), specification marked MIT; verify the list's redistribution terms separately |
| EFF large Diceware | 7776 | 12.9248 bits/word | [EFF passphrase wordlists](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases); list data and page terms must be preserved when redistributed |
| EFF short Diceware | 1296 | 10.3399 bits/word | Same EFF source; this is lower raw capacity per word |
| S/KEY RFC 1760 list | 2048 | 11 bits/word | [RFC 1760](https://www.rfc-editor.org/rfc/rfc1760); RFC distribution terms apply, and its list is a one-time-password vocabulary rather than a general identifier checksum |
| PGP biometric list | 512 total (two 256-word lists) | 9 bits/word if one combined list | Original list source and license require separate verification before redistribution; local acquisition is retained only as research input |
| Niceware/SIL-derived list | 65536-class source | 16 bits/word if uniformly selected | Local source header identifies SIL-derived English words and Yahoo End-to-End; upstream data and project license must be checked independently |
| Mnemonicode wordlist v0.7 | project-defined | measure from the pinned source | [mnemonicode source](https://github.com/singpolyma/mnemonicode/tree/315aed6f1272cf2afa2eb1e1ed4a8879a49e5a6c); the source carries an MIT license; list capacity is not treated as a security claim here |

Raw capacity is `log2(list size)` and assumes uniform random selection. It is
not the same as valid checksummed payload capacity. BIP-0039, for example,
uses checksum bits and fixed sentence lengths; the 11-bit word index is not
11 independent application data bits in every valid sentence. A readable
word identifier also needs normalization, spelling/phonetic error policy,
separator policy, and an explicit list version.

## Measured tokenizer sample

The artifact contains ten three-word samples for each of BIP39, EFF long, EFF
short, and S/KEY, with counts for space, hyphen, and no separator under both
observed encodings. The counts are actual `tiktoken 0.12.0` results, not byte
length proxies. The exact production Codex model-to-encoding mapping remains
unwitnessed, and Claude's tokenizer remains unmeasured. These samples compare
separator and list behavior; they are not an equal-entropy benchmark.

The tokenizer source is [OpenAI tiktoken tag 0.12.0](https://github.com/openai/tiktoken/tree/97e49cbadd500b5cc9dbb51a486f0b42e6701bee), whose [license is MIT](https://github.com/openai/tiktoken/blob/97e49cbadd500b5cc9dbb51a486f0b42e6701bee/LICENSE). A later model or vocabulary must be measured separately.

## Hash and identifier library comparison

- A cryptographic content hash such as SHA-256 provides a digest and collision
  resistance, but its hex projection is expensive in model tokens and is not
  a readable identifier. Use it as an independent binary/content value, not as
  the human name.
- Nano ID provides cryptographically random URL-safe identifiers and a custom
  alphabet; [its README](https://github.com/ai/nanoid/tree/6.0.1) and
  [MIT license](https://github.com/ai/nanoid/blob/6.0.1/LICENSE) are source
  references. It is an ID generator, not a wordlist or content checksum.
- Hashids is a reversible number-to-symbol presentation scheme; the [official
  organization](https://github.com/hashids) and implementations document
  custom alphabets. It must not be presented as a cryptographic hash or as
  collision resistance for arbitrary content.
- A wordlist wrapper can improve sayability, but it inherits the list's
  capacity, spelling ambiguity, license, and versioning. A checksum or
  authenticated tag remains a separate binary field.

Candidate recommendation remains parametric: choose a nominal typed binary
identifier first, then choose a readable projection with a pinned list and
separator. Do not alias a readable word name to a digest, and do not claim
that a short projection authenticates its source.

## Collision contexts

These are illustrative sizing scenarios, not living rulings. For `N` issued
identifiers and `b` uniform random bits, expected collision pairs are
`N(N-1)/2^(b+1)`; the small-risk approximation is the same quantity, not an
exact probability. Choose `b` using
`ceil(log2(N(N-1)/(2p)))` for an explicit target `p`, then account for
adversarial control, retryability, and collision detection:

| Context | Illustrative population | Candidate space | Approximate accidental risk | Operational rule |
|---|---:|---:|---:|---|
| Local controlled | 1,000 | 36-bit readable projection | 7.27e-6 | Detect and retry; issuer controls the namespace |
| Cluster | 1,000,000 | 64 bits | 2.71e-8 | Detect centrally or use a disjoint issuer namespace |
| Public | 1,000,000,000 | 128 bits | 1.47e-21 | Use cryptographic randomness plus separate authenticity; content hashes can use 256 bits |

The identifier is not a secret and does not authenticate an object by itself.
A public population of 10^12 would have approximately 1.47e-15 accidental
collision risk at 128 bits; this illustrates why population and threat model
must remain explicit rather than becoming a fixed universal width.
