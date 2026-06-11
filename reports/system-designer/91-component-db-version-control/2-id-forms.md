## Identifier audit: beads vs Spirit short codes

### 1. Bead identifier format (verified)

Source: `/home/li/primary/.beads/metadata.json`, `/home/li/primary/.beads/config.yaml`, and 549 distinct real IDs sampled from `/home/li/primary/.beads/interactions.jsonl`.

- Shape: `<repo-prefix>-<code>`, e.g. `primary-hj63`. The prefix is the project id; `metadata.json` declares `"dolt_database": "primary"` and every one of the 639 interaction rows uses prefix `primary` (no other prefix appears). `config.yaml` documents the prefix is set at `bd init` (auto-detected from directory name; example `myproject-1`).
- Backend: embedded Dolt — `metadata.json` = `{"database":"dolt","backend":"dolt","dolt_mode":"embedded","dolt_database":"primary"}`. Matches the embedded Dolt dir at `.beads/embeddeddolt/`. Beads is the upstream `steveyegge/beads` tool (`.beads/README.md`), not a workspace component.
- Code alphabet: lowercase base36 `[0-9a-z]`. The full character set observed across all codes is exactly `0123456789abcdefghijklmnopqrstuvwxyz` (plus `.` only as a sub-issue separator).
- Code length: variable, **3 to 8 characters** observed (distribution: 3→190, 4→339, 5→21, 6→71, 7→12, 8→6). Real 3-char codes exist: `primary-03q`, `primary-0cd`, `primary-0ey`, `primary-1ha`, `primary-2y5`. So beads has **no 4-char minimum** — it goes down to 3.
- Sub-issues: a `.N` suffix denotes child issues, e.g. `primary-0m1u.1` … `primary-0m1u.12`, `primary-2y5.1` … `.9`. This is an extra disambiguator beads has that Spirit lacks.
- Derivation: the upstream beads scheme is a per-repo opaque short code (not a global counter, not content-addressed in any way the workspace controls); from the workspace's side it is simply an opaque per-repo token. It is not sequential integers (codes like `hj63`, `2xzv`, `ffew` are non-monotonic).

### 2. Spirit short-code format (verified from source)

Source: `/git/github.com/LiGoldragon/spirit/src/store.rs` (the `RecordIdentifierMint` + `RecordIdentifierCodeRange` impls), constants at `store.rs:43-46`, and `RecordIdentifier` `Deref<str>`/`Display` at `engine.rs:1001-1013`. Confirmed by `skills/spirit-cli.md:107-110`.

- Type: `RecordIdentifier` is a transparent newtype over `String` (it `Deref`s to `str` and `Display`s its payload; `store.rs` stores `record_identifier: String` in `StoredRecord`).
- Alphabet: **lowercase base36 `[0-9a-z]`** — `RECORD_IDENTIFIER_CODE_RADIX = 36` (`store.rs:45`); `digit_character` maps `0..=9` to `'0'+d` and `10..=35` to `'a'+d-10` (`store.rs:992-998`). Identical alphabet to beads.
- Length: **4-char minimum, 7-char maximum** — `RECORD_IDENTIFIER_MINIMUM_CODE_LENGTH = 4`, `RECORD_IDENTIFIER_MAXIMUM_CODE_LENGTH = 7` (`store.rs:43-44`). The mint walks `4..=7`, taking the shortest length that has a free code.
- Minting: random, then collision-checked. `random_identifier` pulls 8 random bytes via `getrandom::fill`, mods into the code-length range, and base36-encodes (`store.rs:964-970`). It retries up to `RANDOM_IDENTIFIER_ATTEMPTS_PER_LENGTH = 128` random draws per length, falling back to `first_available_identifier` (linear scan) before widening to the next length (`store.rs:925-947`). So: **random lowercase base36, shortest collision-free, 4-char minimum** — exactly as the skill states.
- Scope: **per-store, not global.** `next_record_identifier` builds the mint from `RecordIdentifierMint::from_records(&self.records()?)` (`store.rs:848-849`) — the used-set is the records of that one `.sema` store. Collision-freedom holds only within a single Spirit database (the live store at `~/.local/state/spirit/`). It carries **no repo/store prefix**: the reply is a bare code, `(RecordAccepted abcd)` (`skills/spirit-cli.md:107`), and `Lookup abcd` takes a bare code.

### 3. Namespace comparison

| Property | Bead | Spirit record |
|---|---|---|
| Carrier shape | `primary-<code>` (prefix mandatory) | bare `<code>` (no prefix) |
| Alphabet | lowercase base36 `[0-9a-z]` | lowercase base36 `[0-9a-z]` — **identical** |
| Length range | 3–8 chars | 4–7 chars |
| Sub-token | `.N` sub-issue suffix | none |
| Minting | upstream beads / embedded Dolt, per-repo opaque | random, collision-checked per `.sema` store |
| Uniqueness scope | per beads repo (`primary`) | per Spirit `.sema` store |

Same alphabet, overlapping length band (4–7 chars is common to both). A **bare 4-to-7-char base36 token is ambiguous**: `2xzv` could be the bead `primary-2xzv` written without its prefix, or a Spirit record id. The only reliable structural signal is the bead prefix `primary-`; strip it and the two namespaces are indistinguishable by form alone. Neither is content-derived, so you cannot recompute and check. Note the live workspace data already contains real collisions in the bare-code space (the bead code set and the Spirit code set both range over the same `[0-9a-z]{4..7}` strings independently), so confusion is a live risk, not theoretical.

The existing AGENTS.md hard override already covers the human-facing remedy: *"Opaque identifiers in chat carry an inline description. A bead UID, content hash, jj change id, or commit short-id gets a short prose gloss on first mention."* This rule names beads explicitly but does not yet name Spirit record ids, and does not address the bead-vs-Spirit ambiguity specifically.

### 4. Recommended disambiguation convention (minimal)

No code change — purely a writing rule, layered on the existing gloss override:

1. **Beads always carry the full prefix in chat and reports**: write `primary-hj63`, never the bare `hj63`. AGENTS.md already forbids the bare bead UID; the prefix is what distinguishes a bead from a Spirit code, so dropping it is the one move that creates the ambiguity. (This already matches `skills/spirit-cli.md` and bead convention; just make "never bare" explicit for beads.)
2. **Spirit record codes are written bare but always tagged with the word "Spirit"** on first mention, e.g. "Spirit record `4ups`" — the word is what carries the namespace, since the code has no prefix of its own. Their `Lookup`/`Remove`/`RecordAccepted` wire form is bare by contract, so do not invent a prefix.
3. **Both keep the AGENTS.md inline gloss** ("bead `primary-hj63` (the README rewrite)"; "Spirit record `4ups` (the no-backward-compat principle)"). The gloss already disambiguates by content even when the form coincides.
4. Optional one-line addition to the AGENTS.md "opaque identifiers" override: add Spirit record codes to its enumeration and state the rule — bead = prefixed `primary-…`, Spirit = bare code introduced by the word "Spirit". This closes the one gap where the override names beads but not Spirit.

Net: the two systems are not the same hash space and there is no on-disk collision (different stores, different uniqueness scopes). The risk is entirely in chat/report references where a bead's prefix is dropped, collapsing it onto the bare base36 Spirit code form. The prefix-always / word-tag-always / gloss-always trio resolves it with no schema or tooling change.
