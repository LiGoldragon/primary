# Blast Radius — the Stale-Parser Cohort

The headline is narrower and cleaner than the brief feared: across every
active nota-codec-dependent repository, **chroma is the only live
production component that hand-rolls a NOTA parser against the REMOVED
`Token::Str` / quoted-string lexer API.** Its `src/config.rs` (742 lines)
preprocesses NOTA bracket strings INTO quoted strings, feeds them to
`nota_codec::Lexer`, and reads them back as `Token::Str` — the exact
mechanism that nota-codec `f761421` ("reject quoted string delimiters",
2026-05-25) deleted. Two other direct `Token::Str` users exist but neither
is live production: `signal-frame-mockup-stable-caller-id-1` is a
throwaway MOCKUP checkout, and the bespoke-lexer crates `corec` / `askicc`
parse a *different* language (`.core` / `.synth`/`.aski`), do not depend on
nota-codec at all, and are outside this entanglement. The much larger set
of ~65 repos that merely *pin an old nota-codec rev* are NOT the breaking
cohort: the great majority go through the correct `NotaDecode` / `Decoder`
high-level API and need only a `cargo update`, not a rewrite. signal-frame
itself — directly on the porting chain — is in this safe category.

## The dividing line: rev f761421

nota-codec's breaking change is a single commit. Verified against the live
`/git/github.com/LiGoldragon/nota-codec` history:

- `f761421` "nota-codec: reject quoted string delimiters" (2026-05-25
  23:09) removed `Token::Str(String)` from the `Token` enum and the entire
  quoted-string lexer (inline/multiline `"`-delimited reading), and added
  `Error::QuoteStringDelimiter`. The current lexer rejects a leading `"`
  outright: `b'"' => Err(Error::QuoteStringDelimiter { offset: self.pos })`.
- The HEAD the porting chain wants is `24e7823` (current `main`), which is
  `f761421` plus an intent-contract commit.
- Every rev BEFORE `f761421` still carries `Token::Str(String)` and the
  quoted-string reader. Verified `d00fbf5`, `538555e`, `30693c4` all
  contain `Str(String)` in `src/lexer.rs`.

So a repo BREAKS on the forward move only if it touches `Token::Str`, the
quoted-string lexer path, or any other API removed in `f761421` —
regardless of which old rev it pins. A repo that only pins an old rev but
uses `Decoder` / `NotaDecode` is forward-compatible and needs a lock bump,
not surgery.

## Cohort A — genuinely breaks on the forward move (uses removed API)

### chroma (the seed) — effort: LARGE

What it parses: Chroma's `config.nota` (theme/warmth/brightness schedule
configuration) for the `chroma` CLI and the supervised `chroma-daemon`.
`src/config.rs` line 17 imports `use nota_codec::{Lexer, Token};` and runs
a complete hand-rolled recursive-descent parser over the token stream:
`ConfigDocument::parse` → `parse_node` → `parse_record`, plus ~24 free
`parse_*` functions (`parse_theme_axis`, `parse_warmth_schedule`,
`parse_brightness_axis`, `parse_trigger`, `parse_ramp_duration`, …).

Why it is on old nota-codec: `Cargo.lock` pins
`538555e895529e2884b7d37d20c66aadc2a49c08` (pre-`f761421`). It cannot move
forward because two distinct removed surfaces are load-bearing:

1. `Token::Str` consumption. The token walk explicitly matches it, e.g. in
   `reject_removed_or_non_nota_inputs`:

   ```rust
   Token::Ident(value) | Token::Str(value) => {
       if matches!(value.as_str(), "ApplyCommand" | "ApplyTargets" | ...
   ```
   and in the parser core: `Token::Str(value) => Ok(ConfigNode::Str(value))`
   and `Some(Token::Str(head)) => head`.

2. A NOTA-bracket-to-quoted-string preprocessor that is itself the
   anti-pattern. `config()` runs
   `ConfigDocument::parse(&config_text_with_bracket_strings_as_quoted(self.text)?)`.
   That free function (line 119) walks raw bytes, reads `[...]` and `[|...|]`
   bracket strings via `read_config_bracket_string` /
   `read_config_block_string`, and re-emits them through
   `push_quoted_string` — turning the canonical NOTA bracket form INTO
   quotation-mark strings precisely so the OLD quoted-string lexer can
   re-read them. On current nota-codec the emitted `"` is rejected by
   `Error::QuoteStringDelimiter`, so the whole pipeline fails to even lex.

What breaks when nota-codec moves forward: compile error (no `Token::Str`
variant) AND, even if patched to compile, a runtime lex failure on the
self-injected quotes. Both the CLI config read and the daemon's
`config_async` path go through this code.

Migration need: This is a from-scratch rewrite of `config.rs`, not a
patch. The right shape already exists in the workspace: `nota-config`
(`source.rs` / `configuration.rs`) decodes via `nota_codec::Decoder::new`
+ `NotaDecode` with zero hand-rolling — that is the template. chroma's
`Config` / `ThemeAxis` / `WarmthSchedule` / `BrightnessSchedule` types
should derive `NotaDecode` (or be decoded through `nota-config`'s
`ConfigurationRecord` trait), deleting the entire 742-line file:
preprocessor, recursive-descent walk, and all ~24 free `parse_*` functions.
This simultaneously fixes three discipline violations — hand-rolled parser
(`skills/rust/parsers.md`), bracket-strings-emitted-as-quotes (root NOTA
discipline), and free-functions-not-methods (`skills/rust/methods.md`). It
is LARGE because the config schema is rich (nested schedules, palettes,
adapters, ghostty templates, solar offsets) and every node type needs a
deriving struct/enum with correct positional NOTA layout, plus the removed-
architecture rejection (`ApplyCommand` etc.) re-expressed as unknown-variant
errors rather than a token scan.

## Cohort B — direct Token::Str users that are NOT live production

### signal-frame-mockup-stable-caller-id-1 — effort: N/A (throwaway)

`macros/src/schema_reader.rs` imports `use nota_codec::{Decoder, Token};`
and matches `Some(Token::Ident(_)) | Some(Token::Str(_))` (line 772). It
pins `30693c4` (2026-05-20, pre-`f761421`). But the repo's top commit is
`077a76c "MOCKUP: stable durable Caller ID for upgrade-time session
resumption"` — it is an explicitly-labelled mockup checkout, not the
active signal-frame. No migration owed; it dies with the mockup. It is
worth noting only because it reveals the historical schema-reader-macro
pattern that once walked tokens with `Token::Str`.

### corec — effort: N/A for THIS entanglement (separate language)

`src/main.rs` / `src/primitive.rs` use `crate::lex::Lexer` — corec's OWN
78-line bespoke tokenizer (`src/lex.rs`, `enum Token { Ident(String), … }`)
plus `src/parse.rs` (194 LoC). corec is the `.core` → Rust compiler
("core compiler: .aski → Rust with rkyv derives") and does NOT depend on
nota-codec. It is a hand-rolled-parser cohort member by the *spirit* of
`skills/rust/parsers.md`, but it is outside the nota-codec rev collision.
Its own CLAUDE.md already marks it STALE. Flagged for the no-hand-rolled-
parsers audit, not for this porting unblock.

### askicc — effort: N/A for THIS entanglement (separate language)

`src/synth_lex.rs` / `src/synth_parse.rs` use `crate::synth_token::{SynthToken,
SynthSpanned}` — again a fully bespoke lexer for the `.synth` bootstrap
compiler ("all 5 DSLs in one dsls.rkyv"), no nota-codec dependency. Same
classification as corec: a hand-rolled-parser-rule concern, not part of the
nota-codec entanglement.

## Cohort C — pin old rev but use the high-level API (safe; just bump the lock)

This is the large majority and the most important honesty correction to the
brief's worst-case framing. ~65 repos depend on nota-codec; most pin a
pre-`f761421` rev (`538555e`, `c366e3c`, `d00fbf5`, `ae6187e`, `139217d`,
`2618adb`). But pinning old is a LATENT concern, not a break, when the
consumer uses `Decoder` / `NotaDecode` rather than the removed lexer
surface. The signal contract repos and the storage/engine chain are in
this category.

Spot-checked representative on the porting chain:

- **signal-frame** (pins `d00fbf5`): `src/request.rs` and
  `src/command_line.rs` use `Decoder::new` + `NotaDecode` and only
  reference structural tokens like `Token::LBracket` — there is NO
  `Token::Str`, no `into_quoted`, no `read_string`, no quoted-string
  handling anywhere in `src`/`macros`. signal-frame is forward-compatible;
  it needs a `cargo update -p nota-codec`, not a rewrite. This matters
  because signal-frame sits on the exact porting path
  (sema-engine → signal-sema → signal-frame → schema-rust → schema).

- **nota-config** (pins `538555e`): the *correct template* — `source.rs`
  decodes via `nota_codec::Decoder::new` + `NotaDecode`, no hand-rolling.
  Forward-compatible.

The remaining signal-* / owner-signal-* / sema / sema-engine / schema /
mind / router / terminal / introspect / message / persona repos pin old
revs but follow the same derive/decoder pattern as signal-frame and
nota-config; none surfaced in the `Token::Str` / direct-`Lexer` scan. They
are bump-the-lock work, sequenced by the dependency graph, not parser
rewrites. (Each should still be confirmed individually at port time, but
the source scan found no removed-API usage in any of them.)

## Why Cargo collapses this into one collision

Cargo unifies all `git+...nota-codec.git?branch=main` references in a single
build graph to ONE resolved rev. So the moment any workspace member that
shares a build/lock graph with chroma advances nota-codec to `f761421`+ to
satisfy the schema chain, chroma's `Token::Str` references stop compiling.
chroma only builds today because its own `Cargo.lock` independently pins
`538555e`. The collision is therefore real but its true blast radius for
*rewrite* work is a single component: chroma. Everything else is either a
lock bump (Cohort C) or out of scope (Cohort B).

## Summary table of the cohort

| Component | nota-codec rev | Touches removed API? | Class | Effort |
|---|---|---|---|---|
| chroma | `538555e` (old) | YES — `Token::Str` + quote-preprocessor | A: breaks | LARGE |
| signal-frame-mockup-stable-caller-id-1 | `30693c4` (old) | YES — `Token::Str` | B: throwaway mockup | N/A |
| corec | none (own lexer) | n/a (own `Token`) | B: separate language | N/A here |
| askicc | none (own lexer) | n/a (own `SynthToken`) | B: separate language | N/A here |
| signal-frame | `d00fbf5` (old) | NO — `Decoder`/`NotaDecode` | C: bump lock | SMALL |
| nota-config | `538555e` (old) | NO — `Decoder`/`NotaDecode` | C: template | SMALL |
| ~63 other signal/sema/schema/runtime repos | various old | NO (none found in scan) | C: bump lock | SMALL each |
