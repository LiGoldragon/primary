# Word check for the judged identifier type — research, 2026-10-12

Delegated web research with scratchpad measurements (subflow of 875960); measurements are the subflow's, not re-run by this seat.

## Splitting camelCase
| crate | API | binary | notes |
|---|---|---|---|
| heck 0.5.0 | snake case then split on `_`; acronym runs kept | ~11 KB | dormant, stable |
| convert_case 0.12.0 | `split(&str, &[Boundary])` | ~36 KB + unicode-segmentation ~100 KB | active |
| Inflector 0.11.4 | snake case only | 17 KB | unmaintained since 2019 |

## Word-list membership
| approach | crate | size in binary | lookup | proper nouns | false negatives |
|---|---|---|---|---|---|
| Hunspell en_US stems (47.8k) as fst::Set, include_bytes | fst 0.4.7 | 230 KB + ~50 KB code | ~100 ns, no startup | 10.7k capitalized entries, lowercase only | medium: derived forms, jargon (`criomos`) |
| dwyl words_alpha (370k) as fst | fst | 1.65 MB | same | few | low for English, high for names |
| google-10000 as fst | fst | 39 KB | same | no | high |
| bloom over 47.8k stems | bloomfilter 3.0.2 | 57–86 KB | ~50 ns | as list | plus false positives (wrong direction) |
| hunspell-compatible checker | spellbook 0.4.2 | 552 KB dic + ~200 KB code, startup parse | ~1 µs | yes, with case rules | low; API unstable |
| same | zspell 0.5.5 | similar, no bundled dictionaries | ~1 µs | yes | low; 2024 |

## Listless plausibility (no crate; measured on words_alpha training, 5k Hunspell words vs 5k random)
| model | table | dictionary words rejected | gibberish accepted | project nouns passed (of 30) |
|---|---|---|---|---|
| char bigram, threshold −3.18 | ~3 KB | 6.3% | 5.9% | 23 |
| char trigram, threshold −3.36 | ~20 KB | 4.1% | 4.5% | 26 (fails lojix, nix, jev, tokyo) |
Short components (≤4 letters) dominate both failure columns.

## Recommended shape
split → each component lowercased against a ~230 KB fst of Hunspell stems plus our own proper nouns, with a -s/-ed/-ing/-er strip retry → on a miss, the ~20 KB trigram scorer → only components below the threshold, or short components that missed, go to the System-1 model, the score as certainty. Skip spellbook/zspell (startup parse, unstable API) and bloom (false positives).

Sources: docs.rs/heck, docs.rs/convert_case, github.com/BurntSushi/fst, github.com/jedisct1/rust-bloom-filter, github.com/helix-editor/spellbook, github.com/pluots/zspell, github.com/rrenaud/Gibberish-Detector, github.com/dwyl/english-words, github.com/first20hours/google-10000-english.
