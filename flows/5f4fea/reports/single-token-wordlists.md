# Item 26 — identifier density per token

Proposal, not an identifier-library change. Corrected item20 original per-list measurements and capacities are in [word-hash-libraries.md](word-hash-libraries.md). The previous aggregate confused HumanHash with BIP39, merged PGP's alternating alphabets, and changed the measured sample; its numbers are withdrawn. Original samples now remain in the corrected [measurement artifact](../witnesses/item20-token-measurements.json).

## Existing lists ranked by bits per token

Ten three-word IDs, spaces, no initial space. tiktoken0.12.0; Claude unmeasured. Higher is denser.

| cl100k ranking | Bits/token | o200k ranking | Bits/token |
|---|---:|---|---:|
| BIP39 | 9.167 | BIP39 | 9.167 |
| Mnemonicode | 7.805 | EFF short | 8.617 |
| EFF short | 7.755 | Original Diceware | 8.078 |
| Original Diceware / EFF long | 7.457 | Mnemonicode | 8.000 |
| Proquint | 6.761 | EFF long | 7.755 |
| Niceware | 6.575 | Proquint | 7.619 |
| S/KEY | 5.690 | Niceware | 6.575 |
| HumanHash | 5.106 | S/KEY | 5.893 |
| PGP alternating | 4.615 | HumanHash | 5.333 |
| — | — | PGP alternating | 4.706 |

**BIP39 wins the measured existing-list sample.** More bits per dictionary word did not imply more bits per model token.

## One-token intersection

Read helper measured the union of lowercase ASCII alphabetic words from BIP39, EFF long/short and Niceware:66,773 distinct words. With exactly one leading space, cl100k recognizes12,757 as one token; o200k14,182. The intersection is12,268, exceeding8,192 (13bits), below16,384 (14bits). This is a bounded source-list intersection, not the densest possible English dictionary. Filtering vocabulary tokens alone would not establish English words or speech quality.

Intersection SHA256: `eb908041ba67a5ea3d2746bc47c54f0a3fd5bdb8dcbe135e636545258b473572`.

Proposed pinned alphabet: byte-sort the intersection lexicographically and take the first8,192 entries. Subset SHA256: `735e872149d7324c3e6f8212101bc892c39851b7ecba4e82d90ec47c4d5144ff`. Reproduction must pin each source list, its license, tokenizer version and encoding files, filter `[a-z]+`, exact leading-space criterion, UTF-8 ordering and newline format. An immutable version identifies the list; changing any word creates a new version. Do not infer redistribution permission from availability in a cache. This is a proposed algorithm; no production alphabet was installed.

## Actual ten-sample measurement

Seed10, ten three-word and ten four-word IDs from that subset, preserved in [sample artifact](../witnesses/item26-random-samples.json). The samples use selection without replacement; the proposed full encoding may allow repeated words. Raw namespace capacities below refer to the latter.

| Tokenizer | 3 words bare / leading | 4 words bare / leading |
|---|---:|---:|
| cl100k | 3.6 / 3.0 | 4.6 / 4.0 |
| o200k | 3.5 / 3.0 | 4.6 / 4.0 |

Three words carry39bits, four52bits. With the measured leading-space form, each carries13bits/token. Bare first words cost extra on average; do not promise one token per word without its leading space. Some source-list entries are awkward, uncommon or unsuitable for dictation; lexical selection is a reproducible baseline, not a readability-optimized design.

## Existing LLM-friendly projects

Bounded offline search of7,224 cache files under pip, npm index-v5 and Cargo registry index used `single.token`, `llm`, `token.word`, `wordlist`, `humanhash`, `niceware`, `diceware`, `mnemonicode`, `proquint`, `tokenizer`. It found tokenizer-package metadata (@anthropic-ai/tokenizer0.0.4, gpt-tokenizer3.4.0, llama3-tokenizer-js1.2.0, llama-tokenizer-js1.2.2), but no cached project identifying a single-token English identifier wordlist. No global absence claim; no package installed. Claude counts remain unmeasured because no authorized secret-path counter was used.

## Recommendation

Use BIP39's pinned alphabet when compatibility and speech outweigh the extra bits. EFF/original Diceware provide more bits per word, but lost in this token-density sample. The13-bit intersection is the denser measured experimental choice, pending speech/readability and license review. For local/private names, three39-bit words can be collision-checked and retried. Four52-bit words are a cluster candidate only after setting population and collision budget; at one million independently issued names their approximate accidental collision risk is0.000111. A public canonical identity should retain its full cryptographic identifier and separate authentication; short words are display/lookup references. None of these widths is a living ruling.
