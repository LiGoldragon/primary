---
title: 65/3 — The nota-codec entanglement, conceptual root and everything related
role: system-designer
variant: Psyche
date: 2026-06-04
topics: [nota-codec, bracket-strings, hand-rolled-parsers, sema-engine, redb, schema-stack, two-deploy-stacks, stale-pin, chroma]
description: |
  Angle 3 of the nota-codec entanglement meta-investigation. Explains WHY the
  collision exists at the conceptual level: the bracket-only-strings discipline
  forced Token::Str out of nota-codec, and a component (chroma) that hand-rolled
  its own NOTA pre-lexer expecting quoted strings is now the carrier of the debt.
  Connects the entanglement to the sema-engine boundary cleanup (report 63), the
  redb-2 stale cohort, the schema stack, and the two-deploy-stacks. Identifies
  the latent instances of the same stale-pin + bespoke-parser shape that will
  surface the same way.
---

# 65/3 — The nota-codec entanglement, conceptual root and everything related

The collision the psyche hit is not a packaging accident — it is one
discipline (NOTA strings come EXCLUSIVELY from bracket forms) cutting through
the dependency graph and severing a component that never honored it. When
`f761421` ("nota-codec: reject quoted string delimiters") removed `Token::Str`
and made the lexer error on `"`, every consumer that *parsed through the codec
lexer expecting a quoted-string token* lost its ground. chroma is the seed
because chroma did the one thing the no-hand-rolled-parsers rule forbids: it
wrote a 742-line bespoke NOTA pre-lexer (`src/config.rs`) that converts
bracket strings *back into* quoted strings and re-feeds them through
`nota_codec::Lexer`, then reads `Token::Str`. The quote-removal discipline and
the parser discipline are the same rule from two ends, and chroma violates
both. Cargo unifies `nota-codec` to one version per build graph, so the moment
chroma sits in the same graph as the current schema/signal/sema chain, the old
`Token::Str` consumer and the new shape-layer consumer cannot coexist —
chroma's lock pin to old `538555e` is the only thing keeping it compiling. The
same shape (stale pin masking a bespoke parser or a removed-API consumer) is
the *generic* form of every stale-cohort problem in this workspace: the
redb-2 cohort in report 63, the schema-stack drift, and the two-deploy-stacks
split are all instances of "a component pinned itself to an old contract and
hand-built what the contract now provides."

## 1. The nota-codec timeline, verified rev-by-rev

I read the actual `nota-codec` history and the source at each named rev. The
seven relevant commits, oldest to newest (verbatim `git log` subjects):

- `538555e` 2026-05-21 — `nota-codec support bracket strings`. Has
  `Token::Str(String)` (lexer.rs:39) and reads `"` directly
  (`b'"' => Ok(Some(self.read_string()?))`). **chroma and sema-engine pin
  this.**
- `a7aa75b` 2026-05-25 — `expand structural shape helpers for schema macros`.
  Introduces `NotaRecordShape` and `NotaMapEntry` (the structural value-shape
  layer the schema macros consume). Still has `Token::Str`.
- `d00fbf5` 2026-05-25 — has BOTH the shape layer (`NotaRecordShape` /
  `NotaMapEntry`) AND `Token::Str`, but the quote path is now explicitly
  renamed: `b'"' => self.read_legacy_quote_string()`. **schema, signal-frame,
  and signal-sema pin this — the bridge rev.**
- `f761421` 2026-05-25 23:09 — `reject quoted string delimiters`. **Removes
  `Token::Str` entirely**; the lexer now returns `Error::QuoteStringDelimiter`
  on `"`. **spirit, persona-spirit, repository-ledger, lojix-cli pin this.**
- `24e7823` (current `main`) — `synthesize intent contract`. No `Str` variant;
  `b'"' => Err(Error::QuoteStringDelimiter { offset: self.pos })` (lexer.rs:162).

The load-bearing fact: the shape layer (`NotaRecordShape` / `NotaMapEntry`)
and the quote rejection both land at or before the current main. There is **no
rev that has the new shape layer without also being past, or at, the point
where `Token::Str` is on its way out** — `d00fbf5` is the last rev with both,
and it already marks the quote path "legacy." Anything the current schema chain
needs (`a7aa75b`+) is downstream of where the migration started; the current
main is downstream of the removal. So a graph that needs *both* the shape layer
*and* `Token::Str` has no single rev to unify on. That is the entanglement,
stated as a version-lattice fact rather than a packaging inconvenience.

## 2. Why the discipline forced `Token::Str` out

`skills/nota-design.md` §"Strings come EXCLUSIVELY from bracket forms" and the
AGENTS.md hard override are unambiguous: brackets ARE the string form;
quotation marks do NOT form string types; the encoder structurally cannot emit
a `"` (the skill notes `write_string` has three branches — bare identifier,
`[|...|]` block, `[...]` inline — and no fourth quote branch). Legacy quoted
input was accepted as **migration only** and removal was **authorised once all
emitters migrate**. `f761421` is that authorised removal executed: the lexer
stopped accepting `"` at all.

This is a *correct* and intended move. The point of the discipline is
embedding-safety — a NOTA expression with no `"` embeds escape-free inside any
double-quote host (JSON, Rust, Nix, shell, env vars, DB columns). Keeping a
quoted-string lexer path indefinitely would have left the format permanently
ambiguous about whether `"` is content or delimiter, defeating the property.
So the debt is not in nota-codec — nota-codec did the right thing. The debt is
in every downstream that *modeled NOTA strings as quoted strings* and now finds
the substrate has moved out from under it.

## 3. chroma is the seed because it hand-rolled the parser

chroma's `src/config.rs` (742 lines) is the textbook violation of
`skills/rust/parsers.md` ("If a format has a name, there's a parser library.
Use it… NotaDecode/derive is the intended surface"). NOTA has a name and a
library — `nota-codec` with `#[derive(NotaDecode, NotaEncode)]`. chroma instead
hand-built a parser in two layers:

**Layer 1 — a bespoke pre-lexer that un-does the discipline.**
`config_text_with_bracket_strings_as_quoted` (config.rs:119) walks the bytes by
hand and rewrites every bracket string into a quoted string:

```rust
b'[' if bytes.get(offset + 1) == Some(&b'|') => {
    offset += 2;
    let value = read_config_block_string(text, &mut offset)?;
    push_quoted_string(&mut output, &value);   // emits "..."
}
b'[' => {
    offset += 1;
    let value = read_config_bracket_string(text, &mut offset)?;
    push_quoted_string(&mut output, &value);   // emits "..."
}
```

`push_quoted_string` (config.rs:255) literally builds `"..."` with escape
cascades — the exact shape the discipline forbids and the encoder structurally
cannot emit. chroma re-introduces quotes as an internal intermediate
representation so that its layer-2 parser can read them back.

**Layer 2 — feeding the rewritten text through the codec lexer and reading the
removed token.** `reject_removed_or_non_nota_inputs` (config.rs:96) and
`ConfigDocument::parse` (config.rs:380) both do
`Lexer::new(&text)` / `lexer.next_token()` and then match on `Token::Str`:

```rust
Token::Ident(value) | Token::Str(value) => { ... }   // config.rs:101
```

`Token::Str` no longer exists at `f761421`+. This line is a hard compile error
against current nota-codec. chroma compiles today **only** because its
`Cargo.lock` pins `538555e` (verified: `...?branch=main#538555e...`), where
`Token::Str` still exists. The lock pin is the load-bearing fiction.

**The double violation.** chroma breaks the discipline twice: it *emits*
quotation marks (push_quoted_string) and it *parses through a hand-rolled
lexer* (config_text_with_bracket_strings + direct Lexer/Token use). The correct
shape is one `#[derive(NotaDecode)]` on the config structs — the derive reads
bracket strings natively, no pre-lexer, no quote IR, no `Token::Str`. The
~600 lines of bespoke parsing in config.rs would mostly delete. The bespoke
parser is not just stylistically wrong; it is the *mechanism* by which the
quote-removal discipline turns into a build break.

## 4. Why hand-rolled parsers are the anti-pattern (and the intended surface)

`skills/rust/parsers.md` makes the rule absolute: hand-rolled string slicing
for a named format is forbidden; the library owns the parse. The skill's stated
failure mode is exactly chroma's situation — a hand-rolled parser "gets
re-debugged forever as the external tool's output evolves." Here the "external
tool" is nota-codec itself: when the format's string rule changed, the library
consumers tracked it for free, but chroma's hand-rolled copy froze at the old
contract and now blocks the version unification.

The intended surface is `#[derive(NotaDecode, NotaEncode)]`. `nota-design.md`
§"When to hand-write the codec instead of deriving" carves out the *only*
legitimate reason to hand-write a codec impl: a newtype around `String` whose
content is always a symbol-shaped name, where the derive emits noisier-than-
canonical NOTA. That carve-out is a hand-written `NotaEncode`/`NotaDecode`
*impl on a type* that still delegates to `NotaString`/`NotaBlock` — it is NOT a
license to write a byte-walking pre-lexer. chroma is nowhere near that carve-
out; it is the forbidden case.

A weaker version of the same anti-pattern lives in **nexus** and **signal-core**
(both old-pin): they hand-write `NotaDecode` impls that dispatch on raw tokens
(`nexus/src/parser.rs` matches `Token::LParen`; `signal-core/src/request.rs`
and `pattern.rs` match `Token::LBracket` / `Token::LParen`). These are
hand-rolled-parser-shaped — they reach into `Decoder`/`Token` instead of
composing derives — but I verified they only touch *structural* tokens
(`LParen`, `LBracket`) that survive the f761421 removal. They are version-
compatible debt: a lockfile bump fixes them. chroma is the strong form: it
touches the *removed* `Token::Str`, so a lockfile bump breaks it. The
distinction matters for remediation order (§7).

## 5. This is the same problem as the sema-engine boundary cleanup (report 63)

Report 63 found two cohorts split along a redb-2-vs-redb-4 fault line: the core
Persona stack + production Spirit go through sema-engine (redb 4); a second
cohort (new spirit, schema-next, chroma, orchestrator) bypasses sema-engine
with raw redb (redb 2.x). I verified chroma is redb `2.6.3` and sema-engine is
redb `4.1.0`. chroma sits in the bypass cohort in report 63 AND the stale-pin
cohort here — **it is the same component failing the same way on two different
contracts at once.**

The deep identity: both findings are "a component pinned itself to an old
contract and hand-built what the contract now provides."

- **Storage contract (report 63):** chroma/new-spirit hand-rolled raw redb
  (`Database::open`, `begin_write`, a hand-rolled `COMMIT_SEQUENCE_KEY`)
  instead of going through sema-engine. The kernel *provides* the transaction
  surface; they reimplemented it.
- **Parse contract (this report):** chroma hand-rolled a NOTA lexer +
  quoted-string IR instead of going through `NotaDecode`. The codec *provides*
  the parse surface; chroma reimplemented it.

Both are the no-hand-rolled-X discipline (parsers.md for parsing, Spirit 2563
for storage) being enforced at the substrate level, and both surface as a
version collision because the hand-rolled copy froze at an old API generation.
The remediation is identical in shape: **delete the hand-rolled layer, adopt
the provided surface** (derive for parse, sema-engine for storage). That single
move resolves chroma on both axes — it removes the `Token::Str` dependency
(unblocking the nota-codec bump) and removes the raw-redb dependency
(unblocking the redb-4/sema-engine adoption).

Note also: **sema-engine itself still pins old `538555e`** (verified). So the
chain the psyche wants — sema-engine → signal-sema → signal-frame →
schema-rust → schema — currently has sema-engine on the OLD codec and the
signal/schema legs on the bridge `d00fbf5`. Pulling sema-engine forward to the
current main (which the boundary-adoption work will require anyway) and bumping
the schema legs past the bridge is **one unification event**, not two. The
sema-engine boundary cutover and the nota-codec bump are the same migration.

## 6. Connection to the schema stack and the two-deploy-stacks

**Schema stack.** There are two distinct schema/nota lineages and they must not
be conflated. The `nota-codec` family (this report's chain: schema, schema-rust,
signal-frame, signal-sema, sema-engine) is separate from the `nota-next` /
`schema-next` / `schema-rust-next` family (schema-next depends on `nota-next`,
not `nota-codec`). The current-stack porting the psyche is doing pulls the
*nota-codec* family forward. The shape layer (`NotaRecordShape`,
`NotaMapEntry`) the schema macros need lives in nota-codec at `a7aa75b`+, which
is precisely the window where `Token::Str` started being marked legacy and then
removed. So "port to current schema stack" structurally *cannot* coexist with
"keep a `Token::Str` consumer in the graph." The schema stack's forward motion
and chroma's quoted-string parser are mutually exclusive by construction — the
schema stack is the forcing function.

**Two-deploy-stacks.** The two-deploy-stacks discipline (INTENT.md) is the
*intended* containment for exactly this: the production stack and the
next/forward stack are deliberately separated so a forward-moving contract
doesn't break a still-deployed component. The entanglement is what happens when
a component is neither cleanly in the old stack nor ported to the new one — it
straddles, held together by a stale lock pin. chroma is straddling: it consumes
nota-codec (a forward-moving contract) but at a frozen rev, while the rest of
its intended neighborhood moves. The two-deploy-stacks model says the fix is to
*place* chroma decisively: either it stays on the old stack (and the old stack
keeps its old nota-codec — fine, as long as it never shares a graph with the
new chain) or it ports to current (and adopts the derive). The entanglement is
the symptom of an un-made placement decision. The redb-2 cohort in report 63 is
the same straddle on the storage axis.

## 7. Other latent instances of the same shape (stale-pin + bespoke-parser)

I surveyed all ~26 repos that pin old `538555e` for direct use of the codec's
parse API. The latent instances, by severity:

**Strong form — removed-API consumer behind a stale pin (will break on bump):**

- **chroma** — the only one. `Token::Str` + 742-line bespoke pre-lexer +
  quote IR. This is the seed; everything above is about it.

**Weak form — hand-rolled token dispatch, version-compatible (bump-survivable
but still parser-discipline debt):**

- **nexus** (`src/parser.rs`) — hand-written `NotaDecode` matching
  `Token::LParen`. Survives the bump (structural token), but it is a
  hand-rolled parser where a derive belongs.
- **signal-core** (`src/request.rs`, `src/pattern.rs`) — hand-written decode
  matching `Token::LBracket` / `Token::LParen`. Same: survives, but is the
  anti-pattern. signal-core is a *foundational* dependency of the whole signal
  family, so this debt is high-leverage — if signal-core's hand-rolled decode
  ever reaches for a removed token in a future codec change, the entire signal
  cohort breaks at once.

**Latent-only — stale pin, no source-level codec-parse coupling (lockfile bump
suffices):** the remaining ~23 old-pin repos (owner-signal-*, signal-*,
message, system, terminal-cell, chronos, clavifaber, nota-config,
version-projection, sema-engine, etc.) use nota-codec only through derives or
error types (`nota_codec::Error::UnknownVariant`, `nota_codec::Result`) or not
in source at all. These are pure stale-pin: a `cargo update` to current main
fixes them with no code change. They are latent in the sense that they all
share the same single nota-codec graph constraint — the day any of them must
co-build with chroma's old pin, Cargo cannot satisfy both.

**The generalized smell to watch for going forward:** any component that (a)
pins a git dependency to a specific old rev rather than tracking, AND (b)
reaches into that dependency's *internal parse/token/transaction primitives*
rather than its high-level typed surface (derive, engine handle). The
combination is the signature. The redb-2 raw-redb consumers in report 63 are
the storage-axis members of the same set; the `Token::Str` / hand-rolled-Token
consumers here are the parse-axis members. A standing check — grep every repo
for direct use of a dependency's low-level primitives (`Lexer`, `Token`,
`Decoder`, `Database::open`, `begin_write`) — would surface this class
mechanically, which is the auditor-role kind of work AGENTS.md flags as a
candidate.

## 8. The conceptual root in one statement

The entanglement exists because a discipline (bracket-only strings → no
`Token::Str`) propagated through a typed library's API, and a component that had
hand-rolled a copy of that library's job (chroma's NOTA pre-lexer) could not
ride the propagation — it froze at the old API behind a lock pin. The fix is
not version juggling; it is removing the hand-rolled layer so the component
consumes the typed surface and tracks the contract automatically. That is
exactly the same fix report 63 prescribes for the storage axis (delete raw
redb, adopt sema-engine). Parsing and storage are two faces of one rule: **do
not hand-build what a typed boundary provides; if you do, you inherit the debt
of every contract change forever, and one day a discipline lands that your
frozen copy cannot follow.**

## See also

- `reports/system-designer/63-sema-engine-boundary-conformance-audit-2026-06-04.md` — the storage-axis twin of this finding; chroma in the bypass cohort.
- `reports/designer/501-strict-engine-separation-audit-2026-06-04/4-overview.md` — the runner-makes-it-structural concept; same "delete the hand-written host" logic.
- `skills/nota-design.md` §"Strings come EXCLUSIVELY from bracket forms" — the discipline that removed `Token::Str`.
- `skills/rust/parsers.md` — no-hand-rolled-parsers; NotaDecode/derive is the intended surface.
- `/git/github.com/LiGoldragon/chroma/src/config.rs` — the seed: `Token::Str` at :101, the bespoke pre-lexer at :119-268.
- `/git/github.com/LiGoldragon/nota-codec/src/lexer.rs` — current main: no `Str`, `b'"' => Err(QuoteStringDelimiter)` at :162.
