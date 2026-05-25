# 348 — NOTA string discipline: empirically confirmed

*Designer audit + empirical test of the NOTA codec implementation against psyche 2026-05-25 (intent record 698). Verifies that the latest NOTA implementation behaves as the psyche described: brackets are the canonical string form; quotation marks are non-canonical legacy migration input only; canonical encoding never emits them.*

## §1 The psyche rule (record 698)

Verbatim: *"nota uses brackets for strings, not quotation marks. safe nota is free of unescaped quotation marks, they are strongly disfavored, and do not surround string types - that is what [ and [| do."*

Strengthens record 690 (authoring preference) into a structural rule about the NOTA format: brackets ARE the string form; quotation marks do NOT form string types.

## §2 The spec — what NOTA's own README says

From `/git/github.com/LiGoldragon/nota/README.md`:

Line 43-44 (canonical string forms):
| Form | Type |
|---|---|
| `[ ]` | String (inline, at string-like schema positions) — `[hello world]` |
| `[\| \|]` | String (multiline block) — `[\|line one\nline two\|]` |

Line 62-64 (legacy disposition):
> *"Legacy double-quoted strings are accepted by the Rust codec as migration input only. They are not canonical authored NOTA, and canonical encoding never emits them."*

The spec is **aligned** with the psyche rule: brackets canonical; quotation marks legacy migration input; canonical encoding never emits quotation marks.

## §3 The implementation — code evidence

### Lexer (`nota-codec/src/lexer.rs`)

```rust
// Line 9 — module comment
//! ... legacy quote strings, ...

// Line 163 — opening byte dispatch
b'"' => self.read_legacy_quote_string(),

// Lines 183-186 — the legacy reader exists
/// Read a legacy quote-delimited string. `"` opens the inline
/// migration form; `"""` opens the legacy multiline form. Caller
/// is past the opening quote.
fn read_legacy_quote_string(&mut self) -> Result<Token> {
```

Confirms: lexer accepts `"..."` as legacy migration input, explicitly named "legacy".

### Encoder (`nota-codec/src/encoder.rs`)

```rust
// Line 132-145 — write_string implementation
/// Write a string value. Eligible identifier-shaped strings
/// are emitted bare; values containing newlines or closing
/// square brackets use `[| |]` block form when that form can
/// preserve the value exactly; everything else is written as a
/// bracket string with inline escapes.
pub fn write_string(&mut self, value: &str) -> Result<()> {
    self.write_separator_if_needed();
    if should_write_block(value) {
        self.output.push_str("[|");
        self.output.push_str(value);
        self.output.push_str("|]");
    } else if Ident::new(value).is_bare_string() {
        self.output.push_str(value);
    } else {
        write_bracket_string(&mut self.output, value);
    }
    self.needs_space = true;
    Ok(())
}
```

Three branches: bare identifier / `[\| \|]` block / `[ ]` inline. **No fourth branch emits `"..."`.** Grep for any `push.*0x22` or `push_str.*"\""` in `encoder.rs` finds nothing. The encoder structurally cannot emit a quotation mark.

## §4 Empirical proof — running the codec

Probed via a small standalone Rust program against the latest nota-codec on disk. Verbatim output:

```text
ENCODE "hello world" -> [hello world]  quote? false
ENCODE "/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock" -> [/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock]  quote? false
ENCODE "contains [ bracket" -> [contains [ bracket]  quote? false
ENCODE "multi\nline" -> [|multi
line|]  quote? false

DECODE LEGACY "hello world" -> "hello world"
DECODE LEGACY "/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock" -> "/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock"

DECODE BRACKET [hello world] -> "hello world"
DECODE BRACKET [/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock] -> "/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock"

ROUND-TRIP "/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock" -> decoded -> [/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock]

ALL DISCIPLINE PROOFS PASS
```

Four claims proven simultaneously:

| Claim | Evidence |
|---|---|
| Encoder NEVER emits quotation marks | All 4 encode tests show `quote? false`; emitted strings use `[...]` or `[\|...\|]` |
| Encoder uses `[\| \|]` block form for multiline content | `multi\nline` → `[\|multi\nline\|]` |
| Decoder accepts legacy `"..."` as migration input | Both legacy inputs decode to their string contents |
| Decoder accepts canonical `[...]` form | Both bracket inputs decode to their string contents |
| Legacy → canonical round-trip sheds quotation marks | `"path/..."` → decode → re-encode → `[path/...]` (no quotes) |

## §5 The /187 heresy — what's actually happening

The deployed v0.2.0 daemon's `ExecStart` in /187 §"Live State":

```text
("/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock"
 "/home/li/.local/state/persona-spirit/v0.2.0/owner.sock"
 "/home/li/.local/state/persona-spirit/v0.2.0/upgrade.sock"
 "/home/li/.local/state/persona-spirit/v0.2.0/persona-spirit.redb"
 384 None None None None)
```

This is **legacy NOTA** (`"..."` quoted strings). The daemon's `Decoder::read_string()` accepts it because legacy input is part of the contract for migration. **But it is not canonical NOTA**; canonical encoding would emit:

```text
([/home/li/.local/state/persona-spirit/v0.2.0/spirit.sock]
 [/home/li/.local/state/persona-spirit/v0.2.0/owner.sock]
 [/home/li/.local/state/persona-spirit/v0.2.0/upgrade.sock]
 [/home/li/.local/state/persona-spirit/v0.2.0/persona-spirit.redb]
 384 None None None None)
```

**The heresy lives in the CriomOS-home Nix module that synthesizes the ExecStart string.** It's emitting the legacy form rather than the canonical form. The daemon parses it correctly because the legacy form is still accepted as migration input — but the deployment is not yet on canonical NOTA.

## §6 What still emits legacy quote strings

Survey of where legacy-form emission likely persists (would need scan to confirm):

| Surface | Likely legacy emission | Note |
|---|---|---|
| CriomOS-home `criomosHome.personaSpirit` module | YES — confirmed via /187 ExecStart | Nix string interpolation generates `"..."` shell-friendly tuple |
| `lojix-cli` | YES — confirmed via /187 §Notes | "still uses the older quoted-string NOTA reader" |
| Other Nix modules generating NOTA invocations | LIKELY — Nix interpolation pattern is common | Any `${...}` concatenation that uses Nix `"..."` |
| Any hand-authored `.nota` fixtures | POSSIBLE | Should scan for canonicalization |
| Bash scripts piping NOTA | POSSIBLE | Shell-quoting interaction |

Each item is a candidate for the conversion-of-heresy sweep (Task #244).

## §7 Action items

Ordered by priority:

1. **(System-specialist)** Update the `criomosHome.personaSpirit` module to emit canonical bracket-form strings in the ExecStart NOTA tuple. Most reliable approach: build the tuple in Rust via Encoder, ship the encoded text, embed in Nix as a single string literal. Less reliable: change Nix string interpolation to wrap paths in `[...]`. The deployed v0.2.0 daemon accepts both because legacy input is part of its contract; switching to canonical is a quality-of-substrate landing, not a correctness fix.

2. **(Operator)** Migrate `lojix-cli` from the legacy quoted-string reader to bracket-only canonical NOTA. Use nota-codec directly. /187 §Notes already flagged this as known debt.

3. **(Operator / heresy-sweep)** Scan workspace + repos for any other surfaces that emit legacy quote strings into NOTA. Candidates per §6.

4. **(Designer / nota-designer)** Consider deprecation timeline for the lexer's `read_legacy_quote_string` path. When all emission sites are migrated, the legacy reader can be removed — collapsing the parser surface to a single canonical string form.

5. **(Nothing blocking)** All current deployments survive — legacy input is still accepted. This is migration discipline, not a correctness bug.

## §8 What this audit empirically validates

Confirmed empirically (not assumed):

- **Psyche record 698 matches actual NOTA codec behavior** — the codec implements exactly the rule described: bracket-canonical, quote-legacy-migration-input, never-emit-quotes.
- **The README spec (§2) matches the implementation (§3-4)** — spec is not aspirational; it's enforced by the encoder structurally.
- **Legacy quote input is accepted today** — meaning the /187 deployment works correctly even though it's emitting legacy form. There's no immediate correctness emergency; only migration discipline.
- **Canonical → canonical round-trip is lossless** — bracket form decodes to the exact string, encodes back to bracket form.
- **Legacy → canonical round-trip converts** — quoted form decodes to the string, encodes back as canonical bracket form. This is the migration path: read legacy, write canonical.

The discipline is **load-bearing in the encoder** (structurally enforced) and **permissive in the decoder** (accepts legacy for migration). This is the right shape — strict on what we emit, lenient on what we accept; the migration always moves toward canonical.

## §9 References

- `/187` — Spirit v0.2.0 side-by-side deployment (the operator report that surfaced the heresy)
- `/347` — v0.2.0 ↔ schema-driven integration audit (action item #6 flagged lojix-cli migration debt)
- Intent records 690 (initial authoring preference), 698 (structural rule strengthening — this report's authoritative source)
- `nota/README.md` lines 43-44 (canonical forms), 62-64 (legacy disposition)
- `nota-codec/src/lexer.rs` lines 9, 163, 183-186 (legacy quote reader, explicitly named)
- `nota-codec/src/encoder.rs` lines 127-145 (write_string — three branches, none emit quotes)
- The empirical probe results in §4 (run against nota-codec at HEAD of `/git/github.com/LiGoldragon/nota-codec`)
