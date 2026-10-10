# Item 27 — word identifier separators

Proposal and actual tiktoken 0.12.0 measurements; no identifier implementation. Claude is unmeasured and the production Codex tokenizer mapping remains unwitnessed. Ten original item20 three-word samples are reused. No earlier four-word sample existed; seed10 supplies ten new four-word samples per list, uniformly sampled without replacement, reused across every rendering. Original Diceware retains digits/punctuation; camel/Pascal are presentation experiments on those entries, not proof of a legal alphabet.

Full sample strings, per-sample counts and means: [measurement JSON](../witnesses/item27-measurements.json).

## Mean tokens

Each cell is bare / preceded by one space. Capacity is33/44bits for three/four BIP39-list words and38.774/51.699bits for original Diceware. These are alphabet capacities, not wallet mnemonic payloads.

| List | Words | Form | cl100k bare / leading | o200k bare / leading |
|---|---:|---|---:|---:|
| BIP39 | 3 | space | 3.60 / 3.20 | 3.60 / 3.00 |
| BIP39 | 3 | hyphen | 5.10 / 4.70 | 5.20 / 4.60 |
| BIP39 | 3 | underscore | 4.70 / 4.30 | 4.90 / 4.30 |
| BIP39 | 3 | joined | 4.40 / 3.90 | 4.20 / 3.60 |
| BIP39 | 3 | camel | 4.40 / 4.00 | 4.50 / 3.90 |
| BIP39 | 3 | pascal | 4.50 / 4.40 | 4.50 / 4.30 |
| BIP39 | 3 | slash | 5.50 / 5.10 | 5.50 / 4.90 |
| BIP39 | 3 | colon | 5.90 / 5.50 | 6.00 / 5.40 |
| BIP39 | 3 | period | 5.00 / 4.60 | 5.00 / 4.40 |
| BIP39 | 4 | space | 4.50 / 4.20 | 4.30 / 4.00 |
| BIP39 | 4 | hyphen | 6.50 / 6.20 | 6.50 / 6.20 |
| BIP39 | 4 | underscore | 6.30 / 6.00 | 6.50 / 6.20 |
| BIP39 | 4 | joined | 5.50 / 5.30 | 5.50 / 5.40 |
| BIP39 | 4 | camel | 5.70 / 5.40 | 5.70 / 5.40 |
| BIP39 | 4 | pascal | 5.80 / 5.60 | 5.60 / 5.60 |
| BIP39 | 4 | slash | 7.30 / 7.00 | 7.30 / 7.00 |
| BIP39 | 4 | colon | 7.80 / 7.50 | 7.90 / 7.60 |
| BIP39 | 4 | period | 6.70 / 6.40 | 6.70 / 6.40 |

| Diceware | 3 | space | 5.20 / 5.10 | 4.80 / 4.50 |
| Diceware | 3 | hyphen | 6.00 / 5.90 | 6.00 / 5.70 |
| Diceware | 3 | underscore | 6.00 / 5.90 | 6.00 / 5.70 |
| Diceware | 3 | joined | 4.90 / 4.90 | 4.60 / 4.40 |
| Diceware | 3 | camel | 5.30 / 5.20 | 5.20 / 4.90 |
| Diceware | 3 | pascal | 5.30 / 5.10 | 5.20 / 5.00 |
| Diceware | 3 | slash | 6.00 / 5.90 | 6.10 / 5.80 |
| Diceware | 3 | colon | 6.70 / 6.60 | 6.80 / 6.50 |
| Diceware | 3 | period | 6.00 / 5.90 | 5.90 / 5.60 |
| Diceware | 4 | space | 6.40 / 6.50 | 6.50 / 6.30 |
| Diceware | 4 | hyphen | 7.90 / 8.00 | 7.90 / 7.70 |
| Diceware | 4 | underscore | 7.90 / 8.00 | 7.90 / 7.70 |
| Diceware | 4 | joined | 6.80 / 6.90 | 6.30 / 6.30 |
| Diceware | 4 | camel | 7.10 / 7.20 | 7.00 / 6.80 |
| Diceware | 4 | pascal | 7.20 / 6.70 | 7.10 / 6.70 |
| Diceware | 4 | slash | 8.10 / 8.20 | 8.10 / 7.90 |
| Diceware | 4 | colon | 9.10 / 9.20 | 9.10 / 8.90 |
| Diceware | 4 | period | 7.90 / 8.00 | 7.90 / 7.70 |

## Ranked by tokens per bit

Lower is cheaper. Ties remain ties; these are small-sample ranks, not guarantees.

- cl100k_base, BIP39, 3 words, bare: space 0.109, camel 0.133, joined 0.133, pascal 0.136, underscore 0.142, period 0.152, hyphen 0.155, slash 0.167, colon 0.179.
- cl100k_base, BIP39, 3 words, leading: space 0.097, joined 0.118, camel 0.121, underscore 0.130, pascal 0.133, period 0.139, hyphen 0.142, slash 0.155, colon 0.167.
- cl100k_base, BIP39, 4 words, bare: space 0.102, joined 0.125, camel 0.130, pascal 0.132, underscore 0.143, hyphen 0.148, period 0.152, slash 0.166, colon 0.177.
- cl100k_base, BIP39, 4 words, leading: space 0.095, joined 0.120, camel 0.123, pascal 0.127, underscore 0.136, hyphen 0.141, period 0.145, slash 0.159, colon 0.170.
- cl100k_base, Diceware, 3 words, bare: joined 0.126, space 0.134, camel 0.137, pascal 0.137, hyphen 0.155, period 0.155, slash 0.155, underscore 0.155, colon 0.173.
- cl100k_base, Diceware, 3 words, leading: joined 0.126, pascal 0.132, space 0.132, camel 0.134, hyphen 0.152, period 0.152, slash 0.152, underscore 0.152, colon 0.170.
- cl100k_base, Diceware, 4 words, bare: space 0.124, joined 0.132, camel 0.137, pascal 0.139, hyphen 0.153, period 0.153, underscore 0.153, slash 0.157, colon 0.176.
- cl100k_base, Diceware, 4 words, leading: space 0.126, pascal 0.130, joined 0.133, camel 0.139, hyphen 0.155, period 0.155, underscore 0.155, slash 0.159, colon 0.178.
- o200k_base, BIP39, 3 words, bare: space 0.109, joined 0.127, camel 0.136, pascal 0.136, underscore 0.148, period 0.152, hyphen 0.158, slash 0.167, colon 0.182.
- o200k_base, BIP39, 3 words, leading: space 0.091, joined 0.109, camel 0.118, pascal 0.130, underscore 0.130, period 0.133, hyphen 0.139, slash 0.148, colon 0.164.
- o200k_base, BIP39, 4 words, bare: space 0.098, joined 0.125, pascal 0.127, camel 0.130, hyphen 0.148, underscore 0.148, period 0.152, slash 0.166, colon 0.180.
- o200k_base, BIP39, 4 words, leading: space 0.091, camel 0.123, joined 0.123, pascal 0.127, hyphen 0.141, underscore 0.141, period 0.145, slash 0.159, colon 0.173.
- o200k_base, Diceware, 3 words, bare: joined 0.119, space 0.124, camel 0.134, pascal 0.134, period 0.152, hyphen 0.155, underscore 0.155, slash 0.157, colon 0.175.
- o200k_base, Diceware, 3 words, leading: joined 0.113, space 0.116, camel 0.126, pascal 0.129, period 0.144, hyphen 0.147, underscore 0.147, slash 0.150, colon 0.168.
- o200k_base, Diceware, 4 words, bare: joined 0.122, space 0.126, camel 0.135, pascal 0.137, hyphen 0.153, period 0.153, underscore 0.153, slash 0.157, colon 0.176.
- o200k_base, Diceware, 4 words, leading: joined 0.122, space 0.122, pascal 0.130, camel 0.132, hyphen 0.149, period 0.149, underscore 0.149, slash 0.153, colon 0.172.

## Recommendation, pending the living

Keep space-separated words as the token-cost reference. A camelCase candidate is visually recognizable without punctuation and usually cheaper than hyphens, but its capitalization costs tokens compared with spaces in these samples. Joined lowercase loses explicit word boundaries, so speech and exact reverse parsing need a fixed dictionary/decoder or a delimiter. PascalCase also risks looking like an Ethos type. I recommend testing camelCase as the visible short-name presentation, while retaining typed binary identity and explicit full-query resolution; choose no production separator until its Datom String representation and speech round-trip are agreed.

A private short reference can detect and retry collisions; a cluster reference needs a defined population and collision budget; a public identifier must retain sufficient underlying bits and independent authenticity. Changing separators adds no entropy. Fixed-width words joined by case need normalization rules; changing capitalization must never silently create a second identity.

## Datom grammar witness

The native datom skill was received before this analysis. Exact source evidence, `.agents/skills/datom/SKILL.md:17` and `:19` (generated evidence, not edited):

> A brace structure is a struct, a bracket structure is a vector, and a head in front of a structure is a variant carrying it. In datom a head is always a variant, so it is capitalized. A symbol alone, in a position expecting an enum, is a variant carrying nothing; a variant's name is written as the head every time, one carrying nothing included. Guillemets are the string delimiter and parentheses are reserved for Meaning. A datom is not preceded by a Datom root. What a structure means — struct, vector, string, integer, variant — is said by the position it sits in, never by the structure alone.

> A string has two forms: bare, a run with no space and no delimiter glyph, which may be a whole sentence written without spaces in any casing; and guillemets, where every glyph is content until the closing guillemet, which is escaped with a backslash where it is content. Because the position already knows it holds a string, a bare run may carry characters that are syntax elsewhere, the colon among them. An integer is bare ASCII decimal, no leading plus and no leading zero except `0` itself. A decimal is finite and point-mandatory. Today a parenthesized text lands as a plain String, with the Meaning type marked in code.

Capitalized heads name variants in enum positions; a camelCase string is not an enum head simply because it names an object. The expected type determines the position. Spaces require the guillemet String form. Under the stated String rule, hyphen, underscore, slash, colon and period are candidate characters inside a bare String; colon is explicitly supported by the wording. Braces, brackets, guillemets and Meaning parentheses have structural roles. This is the skill's grammar rule, not a newly executed parser round-trip test of all nine forms. The object identifier's production alphabet remains unruled; rendering experiments do not silently change it.
