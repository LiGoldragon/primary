# Flow id alignment: words against hex, base32, base64 (measured 2026-10-07)

Wordlist: BIP-39 English from the `bip39-2.2.2` crate in the cargo registry; 2048 words, sha256 `2f5eed53…24dbda` (the canonical list). Arithmetic in Python; the globs were run against real transcript paths.

Worked ids, from markers in `flows/`:
- Claude `d4ae97`: `identity=d4ae97d46b854301b07e53ccc192d782` (uuid v4), at `~/.claude/projects/-home-li-primary/d4ae97d4-6b85-4301-b07e-53ccc192d782.jsonl`.
- Codex `0062e8`: `identity=01a0712d8284766098fe22a0062e8636` (uuid v7), cut at hex index 23 → `0062e8636`, at `~/.codex/archived_sessions/rollout-2026-09-05T12-46-43-01a0712d-8284-7660-98fe-22a0062e8636.jsonl`.

## 1. Bit boundaries
Where word boundaries (11, 22, 33, 44 bits) fall, counted in characters:

| encoding | bits/char | word 1 | word 2 | word 3 | word 4 | first shared boundary (LCM) |
|---|---|---|---|---|---|---|
| hex | 4 | 2.75 | 5.5 | 8.25 | **11** | 44 bits = 4 words = 11 hex |
| base32 (RFC 4648 / Crockford) | 5 | 2.2 | 4.4 | 6.6 | 8.8 | 55 bits = 5 words = 11 chars |
| base64url | 6 | 1.83 | 3.67 | 5.5 | 7.33 | 66 bits = 6 words = 11 chars |

No word boundary lands on a character until 4 words (hex), 5 (base32) or 6 (base64url). Three words (33 bits) never align: 8¼ hex, 6⅗ base32, 5½ base64.

## 2. Renderings and transcript lookup
The bit field is taken from the front of the hex (Claude) or from hex index 23 (Codex). A partial last character is zero-padded.

| bits | Claude d4ae97 | Codex 0062e8 |
|---|---|---|
| 24 hex | `d4ae97` | `0062e8` |
| 24 words (3 words, 9 bits padding) | `startInputScale` | `aboutBlanketAbandon` |
| 24 b32 RFC / Crockford | `2sxjo` / `tjq9e` | `abroq` / `01heg` |
| 33 hex (8¼) | `d4ae97d4` + 1 bit (`0`) | `0062e863` + 1 bit (`0`) |
| 33 words | `startInputVital` | `aboutBlanketBoat` |
| 33 b32 RFC / Crockford | `2sxjpva` / `tjq9fn0` | `abroqyy` / `01hegrr` |
| 44 hex | `d4ae97d46b8` | **not available**: only 36 bits remain after index 23 |
| 44 words | `startInputVitalStrike` | — |
| 44 b32 RFC / Crockford | `2sxjpvdlq` / `tjq9fn3bg` | — |

Globs from words to transcript. The words are decoded to bits, the whole hex characters are written out, and a partial character becomes a range.
- Claude 24: `~/.claude/projects/*/d4ae97*.jsonl`
- Claude 33: `~/.claude/projects/*/d4ae97d4-[0-7]*.jsonl`. The 9th hex sits after the first hyphen, and its top bit is 0, so the range is `[0-7]`; with top bit 1 it would be `[89a-f]`. Ran it: 1 hit, the right file.
- Claude 44: `~/.claude/projects/*/d4ae97d4-6b8*.jsonl` (exact, with no range).
- Codex 24: `~/.codex/{sessions,archived_sessions}/**/rollout-*-????????-????-????-????-???0062e8*.jsonl`
- Codex 33: `…/rollout-*-????????-????-????-????-???0062e8[0-7]??.jsonl`. Ran it: 1 hit, in `archived_sessions`, not `sessions`.
- As a regex for Codex 33: `-[0-9a-f]{3}0062e8[0-7][0-9a-f]{2}\.jsonl$` (index 23 = the 4th character of the last uuid group).

Codex limit: index 23 leaves 9 hex = 36 bits, so at most 3 words. In a uuid v7, hex 17–31 holds 60 random bits. Starting at index 20 (the start of the last group) would leave 48 bits, which allows 4 words and a whole-group prefix.

## 3. Collisions (birthday bound, arithmetic)
Witnessed today: 275 `.*.flow-id` markers (the brief said 267). Of these, 274 have 6-character aliases and one has 7 (`836818c`). That 7-character alias stretched because it clashed with a legacy directory, `flows/836818`, which has no marker; it was not a clash between two markers.

| bits | 50% clash at | P(any clash) at 275 ids |
|---|---|---|
| 24 | ~4,800 ids | 0.22% |
| 33 | ~109,000 | 4.4e-6 |
| 36 | ~309,000 | 5.5e-7 |
| 44 | ~4,940,000 | 2.1e-9 |

The existing grow-by-one-character rule already handles the rare clash at any length.

## 4. Proposed converter (not built)
Lives in `repos/harness`, next to `flow_id.rs`, as subcommands of the `flow-id` binary. It shares the marker reader and `HarnessKind`, and adds the `bip39` crate's English list.
```
flow-id words  <alias|hex|session-id> [--bits 33|44]  -> startInputVital
flow-id hex    <words>                                -> d4ae97d4 + range [0-7]
flow-id session <alias|words>                         -> full session id (from the marker's identity=)
flow-id transcript <alias|words|session-id>           -> transcript path(s); Claude prefix, Codex offset-23 substring;
                                                         searches sessions/ and archived_sessions/
```
The marker already stores the full identity, so `session` and `transcript` need no glob when a marker exists. Globs are only the fallback when there is no marker.

## Recommendation
33 bits, three words, as designed. It has a 50% clash point near 109k ids, and it fits Codex's 36 available bits at offset 23. It never aligns with any character encoding, so the converter must treat words as bits, not as a re-spelling of characters. If a byte-aligned form is wanted, 44 bits (4 words = 11 hex) is the only clean point. For Codex that needs the cut moved from index 23 to index 20 or earlier.
