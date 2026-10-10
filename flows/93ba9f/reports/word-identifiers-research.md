# Word identifiers: replacing short hex hashes with PascalCase word series

Research for Psyche Opus 93ba9f, 2026-09-26. This report covers three things: prior art, token counts measured locally, and a design recommendation. BIP39 is the baseline to beat. The living added three questions: whether anyone has designed word identifiers for LLMs, how dense a list of single-token words can get, and how to avoid homophones.

The measurements come from these tokenizers, run locally:

- **tiktoken `o200k_base`**, used by GPT-4o through GPT-5.
- **tiktoken `cl100k_base`**, used by GPT-4.
- **`Xenova/claude-tokenizer`** (called **claude2** below). This is the public Claude-2-era tokenizer. The tokenizer behind current Claude models is not public. No Anthropic API key was available, so Anthropic's `count_tokens` endpoint was not called.

So every Claude figure below is a proxy and must be checked before the list is frozen.

## 1. Prior art

| Scheme | List size | Bits/word | Reversible | Design constraints | Checksum |
|---|---|---|---|---|---|
| BIP39 | 2048 | 11 | yes | First 4 letters unique. Avoids look-alike and sound-alike pairs (woman/women, build/built) | 4 bits per 128 bits of entropy |
| PGP word list (Juola & Zimmermann) | 2×256 | 8 | yes | Even byte positions use 2-syllable words, odd positions 3-syllable words. Words were chosen by genetic search to be far apart in phoneme space. The parity alternation catches a dropped or swapped word | implicit (parity) |
| Proquint (Wilkerson) | 16 consonants × 4 vowels, CVCVC | 16 bits per 5-letter syllable | yes | Pronounceable and spellable, but the words have no meaning | none |
| Diceware / EFF long list | 7776 | 12.9 | not an encoding (words are drawn at random) | The EFF list uses familiar, concrete words and excludes profanity, homophones and proper names. No word is a prefix of another | none |
| EFF short list 1 | 1296 | 10.3 | random draw | Short, memorable words | none |
| EFF short list 2 | 1296 | 10.3 | random draw | Unique 3-letter prefix. Every pair of words is at edit distance ≥3 | none |
| Mnemonicode (Tirosh) | 1626 | 10.67 (32 bits in 3 words) | yes | Unique 5-letter prefix, no homonyms, designed to be read out over the phone | none |
| RFC 1751 / S/KEY | 2048 | 11 | yes | Words of 1–4 letters | 2 parity bits per 64 bits |
| Bytewords (Blockchain Commons) | 256 | 8 | yes | Every word has 4 letters. The first and last letter together are unique, so a 2-letter short form works | CRC32 |
| Monero legacy seed | 1626 | 10.67 | yes | Unique 3-letter prefix | the 25th word is a CRC |
| niceware | 65536 | 16 | yes | none | none |
| what3words | ~40k (English) | ~15.3 | yes, but the algorithm is proprietary | Homophones removed "where possible" | none |
| Urbit @p | 256 prefixes + 256 suffixes (3-letter syllables) | 8 per syllable | yes, but deliberately scrambled | Pronounceable, meaningless | none |
| humanhash | 256 | 8 | **lossy**: the digest is compressed to 4 words | Made for display only | none |
| Docker names, Heroku/Haikunator, Petname, Gfycat | adjective + noun lists | about 15 bits in total | **no**: names are random, not derived from bits | Style only | none |

What the prior art teaches:

- Reversible schemes use a list size that is a power of two. The alternative is a mixed-radix split like Mnemonicode's 1626³ ≈ 2³².
- Robust lists enforce three things: a unique prefix, a minimum edit distance, and no homophones.
- Only the PGP list and Mnemonicode were designed for being read aloud.
- Only BIP39, RFC 1751, Bytewords and Monero carry a checksum.
- The Docker/Heroku-style names are not candidates here, because they are not reversible.

### Word identifiers designed for LLMs

Found: two small projects from 2025–26, and neither has been peer-reviewed.

- **id-token-nicer** (github.com/thejens/id-token-nicer):
  - Lists of 2048 to 32768 words.
  - Each word is a single token in cl100k, o200k, Gemma and Llama 3.
  - It includes 4–15 check bits.
  - It measures no error rates.
- **id-agent** (github.com/vostride/id-agent):
  - A 4096-word list, each word one o200k token.
  - A 96-bit ID costs about 14 tokens, against about 23 for a UUID.
  - It has no accuracy data.
  - A Hacker News thread about it (news.ycombinator.com/item?id=48191852) raised three objections:
    - Stripping the hyphens from a UUID already cuts it from 26 to 18 tokens.
    - Meaningful words may prime the model toward their meaning.
    - Words widen the injection surface.

  The same thread reports anecdotes of Sonnet 3.5 transposing hex digit pairs.

Neither project enforces homophone or phonetic distance, and neither uses PascalCase. Both separate words with spaces or hyphens.

**Evidence that LLMs mis-copy IDs:**

- **BAML** (boundaryml.com/blog/uuid-swap) ran the only A/B test found.
  - Setup: Claude Haiku, 200 items over 100 class IDs.
  - UUIDs: 29 and 68 errors in two runs.
  - Integers: 7 and 5 errors.
  - UUIDs remapped to integers: 5 and 6 errors.
  - Opus 4: 80% correct with UUIDs, 100% with integers.

  It compares UUIDs with integers, **not with words**.
- **Anthropic's "Writing tools for agents"** (anthropic.com/engineering/writing-tools-for-agents) says that replacing UUIDs with meaningful language, or even with a 0-indexed ID, "significantly improves Claude's precision in retrieval tasks by reducing hallucinations". It gives no numbers.
- **arXiv 2607.16072** reports frontier models failing to copy long binary or repetitive strings exactly. It blames the model copying by matching local context. Hex and UUIDs were not tested directly.

**Not found:** any controlled study of words versus hex for LLM copy accuracy, and any list designed for both speech-to-text and tokenizers. That combination is still open.

## 2. Measured token counts

**Method.**

- For each bit length, 2000 random values.
- Each ID is counted as it appears mid-sentence, with a leading space (`' ' + id`).
- Word IDs are PascalCase with no separator. The first word carries the most significant bits.
- The word count is ceil(bits / bits-per-word), so the words carry at least as many bits as the hex.
- Cells show the mean token count, with the maximum in parentheses.

| Bits (hex chars) | Form | Example | o200k | cl100k | claude2 |
|---|---|---|---|---|---|
| 24 (6) | hex | `b65c1c` | 4.34 (7) | 4.34 (7) | 3.85 (6) |
| 24 | proquint | `jubis-bafuk` | 4.82 | 5.25 | 5.72 |
| 24 | BIP39, 3 words | `LogicSunnyAble` | 3.79 (8) | 4.20 (8) | 4.98 (9) |
| 24 | 4096-word list (by frequency, not token-selected), 2 words | `CartelRetro` | 3.54 (6) | 3.75 (7) | 4.06 (7) |
| 24 | **list A**: 1024 words, single-token in o200k and cl100k, 3 words | `ThanksRealityCould` | **3.00 (3)** | 3.25 | 3.56 |
| 24 | **list B**: 512 words, single-token in all 3 tokenizers, 3 words | `FatherRepeatFound` | **3.00 (3)** | **3.00 (3)** | **3.00 (4)** |
| 32 (8) | hex | `da65f4b9` | 5.47 (9) | 5.46 (9) | 5.02 (8) |
| 32 | BIP39, 3 words | `NowOakHoney` | 3.93 | 4.25 | 4.62 |
| 32 | list A, 4 words | | 4.00 | 4.48 | 4.93 |
| 32 | list B, 4 words | | 4.00 | 4.00 | 4.00 |
| 48 (12) | hex | | 7.79 (12) | 7.77 | 7.36 |
| 48 | BIP39, 5 words | | 6.81 | 7.32 | 8.14 |
| 48 | list A, 5 words | | 5.00 | 5.81 | 6.51 |
| 64 (16) | hex | | 10.03 (16) | 10.00 | 9.67 |
| 64 | BIP39, 6 words | | 8.05 | 8.78 | 9.34 |
| 64 | list A, 7 words | | 7.00 | 8.15 | 9.00 |
| 64 | list B, 8 words | | 8.00 | 8.00 | 8.00 |
| 128 (32) | hex | | 19.10 (26) | 19.04 | 18.94 |
| 128 | BIP39, 12 words | | 16.24 | 17.73 | 18.77 |
| 128 | list A, 13 words | | 13.00 | 15.64 | 17.30 |

**Bits per token.**

| Form | Bits per token |
|---|---|
| Hex | 5.5 at 6 chars, rising to 6.7 at 32 chars |
| BIP39 | 5.7–8.1, depending on tokenizer and bit length |
| Single-token lists | exactly their bits per word: 9 or 10. In principle 12 for a 4096-word list, but the next paragraph explains why a PascalCase 4096 list is out of reach |

The surrounding text changes hex costs: at 24 bits, bare hex costs 3.72 tokens and backticked hex (`` `b65c1c` ``) costs 5.72.

**Density ceiling.** The binding constraint is PascalCase itself. The measured counts:

| Count | Words |
|---|---|
| Dictionary words (CMUdict ∩ 50k frequency list, 3–10 letters) that are one token as `' word'`, in both o200k and cl100k | 14,523 |
| Same, as `' Word'` | 8,598 |
| Same, as `Word` with no leading space, which is how every word after the first appears in PascalCase | 3,802 |
| Single-token in both `Word` and `' Word'`, per tokenizer set | o200k 5,038; o200k+cl100k 3,565; all three 2,541 |

**Pruning funnel.** This applies the quality filters to the PascalCase single-token pool:

| Filter step | o200k only | o200k+cl100k | all 3 |
|---|---|---|---|
| Single-token dictionary words | 5038 | 3565 | 2541 |
| minus names and profanity | 4805 | 3426 | 2441 |
| minus exact homophones (CMUdict) | 3843 | 2733 | 1884 |
| plus spelling edit distance ≥2 | 2490 | 1892 | 1318 |
| plus phoneme edit distance ≥2 | **2119** | **1618** | **1152** |
| Content-word variant (Brysbaert: noun/adjective/verb, ≥95% known), same filters | 1298 | 1024 | 781 |
| plus unique 4-letter prefix (BIP39 style) | 1047 | 848 | 672 |

Conclusion on density:

- A PascalCase list of words that are each one token, and also survive the homophone and confusability filters, tops out at about **1024 (10 bits)** across OpenAI tokenizers. That already includes the content-word filter.
- Across all three tokenizers the ceiling is about **512 to 1024 (9–10 bits)**.
- A 2048 list is possible only for o200k alone, or with dictionary words that are not content words.
- **No PascalCase 4096 list is possible** under these filters.
- A lowercase, space-separated form gets much further: **4718 content words** (o200k+cl100k) survive all the homophone, spelling and phoneme filters. So 12 bits per token is reachable only if the words are separated by spaces.
- Separators cost tokens. At 3 words on o200k:

  | Form | Tokens |
  |---|---|
  | PascalCase | 3.00 |
  | space-separated | 3.00 |
  | underscore | 3.77 |
  | hyphen | 3.97 |

**BIP39 against a token-selected list:**

- Only about 1,089 of the 2048 BIP39 words are single tokens in both `Word` forms in o200k and cl100k.
- BIP39 averages 1.17 (o200k), 1.21 (cl100k) and 1.43 (claude2) tokens per word.
- The per-ID token count varies with each ID: a 24-bit BIP39 ID can cost up to 8 tokens.
- A token-selected list costs a fixed k tokens for k words.

In short, BIP39 is beaten on tokens at every length, but by about one token or less at 24–32 bits. The bigger gain is that the cost becomes predictable.

**LLM copy risk.** Everything in this block is my own inference except the BAML and Anthropic results already cited. The BAML result shows opaque IDs mis-copy far more than simple ones. The failure differs by form:

- **Hex** fails by substituting or transposing characters inside a token that is not a word. The result is a well-formed string, so nothing flags it.
- **Words** fail by substituting a plausible word: a synonym (River→Stream), a plural or tense change, or a word pulled in from nearby prose. The model also may "mean" the words and mix them into the surrounding text.

Two cheap checks cover the word case:

- Decoding against the list rejects any word not on it.
- Check bits reject a substitution that lands on another list word.

Removing plurals, inflections and near synonyms from the list lowers the plausible-substitution rate further. The spelling edit distance ≥2 filter already removes plural pairs such as `cat`/`cats`. Synonym pruning was not done.

## 3. Recommendation

**The list.**

- Exactly **1024 words (10 bits per word)**.
- Each word is a single token as both `Word` and `' Word'` in o200k and cl100k, and in the Claude tokenizer as well once `count_tokens` confirms it.
- Filters, all applied in this research:
  - 3–8 letters, ASCII.
  - Content words (noun, adjective or verb) known to ≥95% of raters.
  - Not a first name, no profanity.
  - No CMUdict homophone anywhere in common English.
  - Spelling edit distance ≥2 and phoneme edit distance ≥2 from every other list word.
- Filters to add before freezing:
  - A human review pass. The machine selection still admits `let`, `were` and `kill`, and IT jargon such as `android`.
  - Synonym pruning with WordNet.
  - The 4-letter unique prefix only if it does not push the list below 1024.
- The o200k+cl100k content-word candidate yields exactly 1024 words. On the claude2 proxy only 73% are single tokens (1.19 tokens per word), so the list must be re-derived against the current Claude tokenizer.
- Fallback: list B (512 words, 9 bits) is single-token in all three measured tokenizers.

**Words per ID** (1024 list):

| Use | Bits needed | Words | Bits carried | Spare bits | Tokens (o200k) | Hex it replaces (tokens) |
|---|---|---|---|---|---|---|
| Flow ID | 24 | 3 | 30 | 6 check bits | 3 | 6 hex, 4.3 |
| Flow ID, short form | 20 | 2 | 20 | none | 2 | 5 hex, lossy against the current 24 bits |
| Message / lock ID | 24–30 | 3 | 30 | 0–6 check bits | 3 | 8 hex, 5.5 |
| Commit prefix | 28 (7 hex) | 3 | 30 | 2 check bits | 3 | 7–8 hex, 5.0–5.5 |
| Commit prefix, long | 40 (10 hex) | 4 | 40 | none | 4 | 10 hex, about 6.5 |
| Full SHA-1 | 160 | 16 | 160 | none | 16 | 40 hex, about 24 |

Two words cannot hold a 24-bit flow ID unless each word carries 12 bits. That needs a 4096 list, which as PascalCase costs about 1.65 tokens per word, or 3.54 tokens per ID: worse than three single-token words.

If the living wants two words, the choices are:

- Accept 20-bit flow IDs. By the birthday bound, a collision becomes 50% likely around 1,200 flows.
- Accept about 3.5 tokens with a 4096 list.

**Casing and parsing.**

- The canonical form is PascalCase: ASCII, the first letter of each word uppercase, no separators.
- Most significant bits go in the first word, so a shorter prefix is simply fewer leading words, as with hex prefixes.
- Check bits go in the last word.
- The decoder is case-insensitive. It accepts spaces, hyphens and underscores between words, so speech-to-text output like "logic sunny able" decodes. It rejects any word not on the list.
- A future tolerant mode could snap an unknown word to its nearest list word by phoneme distance.

**Candidate names for the standard:**

- **Wordprint**
- **Mnemonid**
- **Saybits**
- **Tokenword**
- **Hashspeak**

## Sources

- BIP39 list and design notes: https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
- PGP word list: https://en.wikipedia.org/wiki/PGP_word_list, https://philzimmermann.com/docs/PGP_word_list.pdf
- Proquints: https://arxiv.org/html/0901.4016
- EFF wordlists (Bonneau): https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
- Mnemonicode: https://github.com/singpolyma/mnemonicode
- RFC 1751: https://www.rfc-editor.org/rfc/rfc1751.html
- Bytewords: https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-012-bytewords.md
- Monero seed: https://docs.getmonero.org/mnemonics/legacy/
- niceware: https://github.com/diracdeltas/niceware
- humanhash: https://github.com/zacharyvoase/humanhash
- Urbit @p: https://docs.urbit.org/hoon/stdlib/4a
- Docker names: https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go
- what3words: https://support.what3words.com/en/articles/1520578
- Tierney's critique of what3words: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0292491
- id-token-nicer: https://github.com/thejens/id-token-nicer
- id-agent: https://github.com/vostride/id-agent and https://news.ycombinator.com/item?id=48191852
- BAML UUID-swap test: https://boundaryml.com/blog/uuid-swap
- Anthropic, "Writing tools for agents": https://www.anthropic.com/engineering/writing-tools-for-agents
- Exact-copy failures in LLMs: https://arxiv.org/html/2607.16072v1
- Phonetic confusability in speech recognition: https://www.researchgate.net/publication/279295675
- Data and tokenizers used locally:
  - tiktoken (o200k_base, cl100k_base)
  - https://huggingface.co/Xenova/claude-tokenizer
  - BIP39 english.txt and the EFF lists
  - CMUdict (https://github.com/cmusphinx/cmudict)
  - FrequencyWords en_50k (https://github.com/hermitdave/FrequencyWords)
  - Brysbaert concreteness norms (https://github.com/ArtsEngine/concreteness)
  - LDNOOBW profanity list
  - dominictarr/random-name first-names list
- The prior-art and literature sweep was done by a nested research subflow of 93ba9f.
