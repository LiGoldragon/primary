# 7 — Bare `Path` type in NOTA

**Lane:** second-designer-assistant
**Date:** 2026-05-18 (initial); 2026-05-19 (spec + migration follow-up)
**Status:** implemented + tested in nota-codec (§9); spec section landed in
`repos/nota/README.md`; `skills/skills.nota` migrated to bare paths (§11)
**Audience:** designer (language-design authority), operator (`nota-codec` + `nota-derive` implementor)

---

## TL;DR

Filepaths in NOTA today require quotes (`"skills/operator.md"`) because
the bare-ident alphabet is `[A-Za-z0-9_-]` and filepaths carry `/` and
`.`. Proposal: introduce a typed `Path` shape whose decode-time alphabet
is widened to `[A-Za-z0-9_\-./]` (start: letter, `_`, `.`, or `/`), so
schema positions expecting a `Path` accept bare forms like
`skills/operator.md`, `./foo`, `/etc/hosts`. String positions stay strict
and reject the wider tokens with a "use quotes or `Path`" error.

This is consistent with existing NOTA discipline:
**position-determined-by-type-context** already governs bare-int
acceptance for `#[serde(transparent)]` newtypes (`Slot`, `Revision`); it
already governs bare-ident-as-String. `Path` extends the pattern with a
small alphabet change — not a new syntax category.

Reuse over invention: this is **not** a new delimiter pair, not a new
sigil, not a new string form. It is one typed shape that widens the
bare-token alphabet in schema-typed positions and tightens the decode
error in non-Path positions.

---

## 1. Problem

The workspace's only `.nota` file (`skills/skills.nota`) quotes every
path:

```nota
(Role operator "skills/operator.md" apex "...")
(Role designer "skills/designer.md" apex "...")
(Architecture component-triad "skills/component-triad.md" apex "...")
```

The quoted forms are syntactic noise: each `/` and `.` is the reason the
quotes are there, and a reader who knows the NOTA byte set has to
mentally strip the quotes to see the path. The recent canonical-NOTA
rewrite (designer commit `36bc77ad`, `skills/nota-design.md`) made
every other field denser — typed wrapper carries the category, named
enums replace integer codes, comments only explain the schema. The
quoted paths are now the file's last avoidable token-waste. Future NOTA
configs that carry many paths — `orchestrate/roles.nota`, deployment
manifests, component-graph files — would compound this.

The bare-ident byte set is defined canonically in
`repos/nota-codec/src/ident.rs:40-46`:

```rust
fn is_start(self) -> bool {
    self.byte.is_ascii_alphabetic() || self.byte == b'_'
}
fn is_continue(self) -> bool {
    self.byte.is_ascii_alphanumeric() || self.byte == b'_' || self.byte == b'-'
}
```

Filepath characters absent from this set:

| Char | Use in paths | Could-it-be-added? |
|---|---|---|
| `/` | path separator | yes — no current lexer collision |
| `.` | extension, dot-files, `.` / `..` | yes — float lexer dispatches on leading digit, so `nota.codec` is unambiguous as long as start is non-digit |
| `~` | home expansion | **no** — reserved as nexus mutability sigil (`repos/nota/README.md:299`) |
| `:` | Windows drive / ADS | **no** — NOTA's own nested-name separator (`Char:Upper:A`) |
| `\` | Windows path | no — quoted form covers; workspace is Linux-shaped |
| space | paths-with-spaces | no — never; quotes always |

## 2. Design

### 2.1 Bare-`Path` alphabet

```
start byte:    [A-Za-z_./]      ;; ASCII letter, underscore, dot, slash
continue byte: [A-Za-z0-9_\-./] ;; alphanumerics, underscore, hyphen, dot, slash
```

Excluded characters retain their current meaning (`~` reserved for nexus
sigil; `:` for nested-name; `\` for quoted form; space / sigil / bracket
/ quote / `#` / `;;` end the token or are syntax).

### 2.2 Leading digit

Leading digit still dispatches to `read_number` (preserves
first-token-decidability on the lexer's number-vs-ident split). A path
like `01-intro.md` still needs quotes — leading-digit filenames are the
narrow remaining exception. This keeps `3.14`, `0xFF`, `1_000_000`
unambiguous.

### 2.3 Lexer change

Single permissive scan: when the lexer's current `read_ident` enters,
extend `is_start` and `is_continue` to include `.` and `/`. Tokens
produced widen from `Ident(String)` whose content is `[A-Za-z0-9_-]+` to
`Ident(String)` whose content matches §2.1's alphabet.

The lexer **does not** branch by schema. The token classification stays
one-token-decidable. The acceptance rules differ at *decode* time, not
*lex* time.

### 2.4 Decode rules per schema position

| Schema position | Accepts bare ident with chars outside `[A-Za-z0-9_-]`? | Error if rejected |
|---|---|---|
| `String` | **no** | "bare-ident-string content `skills/operator.md` contains `/`; quote it as `\"skills/operator.md\"` or use a `Path`-typed field" |
| Record-head `(Foo ...)` | **no** — PascalCase rule still enforced | unchanged |
| Field name in schema | **no** — camelCase still enforced | unchanged |
| `true` / `false` / `None` | **no** — reserved | unchanged |
| Bare-int for `#[transparent]` newtype | unchanged | unchanged |
| **`Path` newtype** | **yes** | n/a |

A `Path` value in a quoted form still works — `(Skill operator
"skills/operator.md" ...)` decodes the same as bare. Quoted is the
fallback for content that has spaces, leading digits, `~`, `:`, or other
disallowed chars.

### 2.5 Encoder rules

When encoding a `Path`:

- If content matches §2.1 alphabet *and* doesn't start with a digit *and*
  isn't one of `true`/`false`/`None`: **emit bare** (canonical form).
- Otherwise: emit quoted (`" "` inline; `""" """` if it contains `"` or
  a newline).

Same canonical-emit-when-eligible discipline as bare-ident-strings (per
README §"Bare-identifier strings": "canonical form emits bare when
eligible").

### 2.6 Schema-side surface

Two viable shapes; recommendation is **(a)**.

**(a) Typed newtype, derive-driven.** `Path` is a newtype in `nota-codec`
(or a small adjacent crate) that derives a `NotaPath` impl. Field-site
usage:

```rust
struct Skill {
    name: String,
    path: Path,         // <-- bare-Path decoding gated by this type
    kind: SkillKind,
    tier: u8,
    description: String,
}
```

Pro: "verb belongs to noun" — Path is a type, surfaced in the schema.
Pro: same discipline as `Slot`, `Revision`, `Blake3` — small typed shapes
with their own bare/wrapped decoding.
Con: forces schema edits at consumer sites where `String` was the
default.

**(b) Attribute.** `#[nota(path)] path: String` flags the field. Pro:
no new type. Con: the verb-encoding-in-attribute pattern is the kind of
thing `skills/language-design.md` §"Delimiters earn their place" warns
against — the typed shape is the right home for the rule.

Pick **(a)**. The attribute path encodes a type-of-string distinction in
an attribute when the workspace already has the typed-newtype mechanism
that surfaces it in the schema.

### 2.7 `nota` spec text

The spec gets a new short section after §"Bare-identifier strings",
parallel to §"Newtype structs". Drafted:

> **`Path` bare form.** When a schema position expects the typed shape
> `Path`, a bare token may use the extended alphabet `[A-Za-z_./]`
> (start) / `[A-Za-z0-9_\-./]` (continue), e.g. `skills/operator.md`,
> `./config`, `/etc/hosts`. The quoted form (`"..."`) remains available
> for content that has spaces, a leading digit, or any character outside
> the extended alphabet. Canonical encoding emits the bare form when
> eligible.
>
> `Path` content does not use NOTA's nested-name separator `:` and does
> not use the nexus sigil `~`. Both characters force quoted form.

---

## 3. Why this is in keeping with NOTA's discipline

| Instinct (`skills/language-design.md`) | This proposal |
|---|---|
| 0. NOTA is the only text syntax | unchanged — same syntax, wider bare alphabet in a typed position |
| 1. Delimiter-first | unchanged — `(`, `[`, `"`, `#`, `;;` still dispatch first |
| 2. No keywords beyond truth values | unchanged — Path is a typed record, not a keyword |
| 3. Position defines meaning | **exactly the same pattern** — schema-position determines what bare tokens mean (already true for bare-int in `transparent` newtypes, bare-ident in `String` positions) |
| 4. PascalCase head / camelCase field | unchanged — Path content appears in value position only |
| 6. Every value is structured | **advances** the discipline — `Path` is a typed newtype, not a `String` field |
| 7. Newlines not significant | unchanged |
| 11. The parser stays small | one alphabet change in the lexer, one decoder method in the codec — not a new rule class |
| 18. Delimiters earn their place | **passes the test** — no new delimiter; the existing quoted form was the workaround, the bare form is the ergonomic upgrade for a load-bearing case |

The closest precedent in NOTA today is **§"Newtype structs"** in the
spec (`repos/nota/README.md:221-259`): `#[serde(transparent)]` lets a
newtype of a primitive accept the bare primitive at its schema position
(`(Edge 100 101 Flow)` instead of `(Edge (Slot 100) (Slot 101) Flow)`).
`Path` is the same pattern for a wider alphabet: a typed wrapper whose
schema position relaxes the lexer's wrapping requirement.

---

## 4. Implementation surface

| Crate | Change | Estimated effort |
|---|---|---|
| `nota` (spec) | Add §"Path bare form" after bare-ident-strings; update §Identifiers + §Literals tables | small |
| `nota-codec` | Loosen `IdentByte::is_start` / `is_continue` to include `.` and `/`; add `Path(String)` newtype + `NotaEncode` / `NotaDecode`; add decode-time rejection of widened tokens in `String` positions with helpful error | medium |
| `nota-derive` | Add `NotaPath` derive or wire `Path` into existing derives | small |
| `skills/skills.nota` | Replace `"skills/operator.md"` etc. with bare form; update schema to use `Path` | trivial follow-up |
| Round-trip tests | New cases: each bare-Path alphabet char; rejection in `String` position; canonical-emit-bare-when-eligible | small |

The codec change is the load-bearing piece. The spec change pins the
contract. The derive change is mechanical. The schema migration is the
gain.

---

## 5. Open questions

### 5.1 Should leading `/` be allowed bare?

Absolute paths (`/etc/hosts`, `/nix/store/...`) start with `/`. The spec
section is cleaner if `/` is a valid start byte; consumers who pass
relative paths only never write `/` at start anyway. Recommend: **yes**.

### 5.2 Should leading `.` be allowed bare?

`./foo`, `../bar`, `.config`, `.envrc`. Same answer as `/`: cleaner spec
if yes; consumers who never use dot-relative paths don't see it.
Recommend: **yes**.

### 5.3 Path bare form starting with hyphen?

A path like `-rf` (a malformed argument hiding as a path) — currently the
lexer dispatches `-` to `read_number` and would fail. Should bare-Path
start include `-`? **No** — `-` as start collides with negative-int
lexing. Quoted form covers the edge case.

### 5.4 `:` for Windows drives (e.g. `C:\foo`)?

NOTA's nested-name `:` is at the syntax level; the parser sees it as
`Token::Colon`. If `:` were added to bare-Path, a bare `C:\foo` would
need the lexer to know "this is a Path position." That re-introduces
schema-driven lexing — rejected. Windows drives go through quoted form;
acceptable cost given the workspace targets Linux.

### 5.5 Should this be a family — `Path` + `Url` + ...?

`https://example.com/foo` has the same problem (`:`, `/`, `.`).
`mailto:user@example.com` adds `@` (nexus sigil — same problem as `~`).
URLs are a strictly harder problem because `:` and `@` are unavoidable.
Recommendation: ship `Path` alone first; defer `Url` to a separate
report. The bare-`Url` design either needs schema-driven lexing (NO) or
accepts that URLs always quote (acceptable). A `Url` newtype that always
emits quoted is still a worthwhile structuring even without bare form.

### 5.6 Migration concerns for existing `.nota` files

Only `skills/skills.nota` is affected today. The change is
**backwards-compatible** at decode: quoted strings still decode as
`Path`. Encoder canonicalisation changes (emits bare when eligible) ripple
to any round-trip-equality tests of canonical output. Plan: ship codec
change first with encoder still emitting quoted (matches current
"aspirational bare-emit" note in spec §"Bare-identifier strings"
implementation note); enable bare-emit in a follow-up commit alongside
the spec update.

---

## 6. Consequences

### What gets easier

- `.nota` config files carrying paths read like prose:
  `(Role operator skills/operator.md apex "...")` — every quoted path
  string in `skills/skills.nota` drops to bare.
- Future deployment manifests (`/etc/nixos/configuration.nix`,
  `repos/horizon-rs/flake.nix`) carry as bare tokens.
- `orchestrate/roles.nota` (when the `.list` → `.nota` migration lands —
  `orchestrate/roles.list` references this) carries
  per-lane report subdirectories (`reports/designer/`) bare.

### What gets a sharper error

A bare token like `nota.codec` in a `String` position today is a
lex-time `Error::UnexpectedChar` at the `.`. After this change it's a
*token* that decodes successfully in a `Path` position and **fails with
a helpful "use quotes or `Path`" error in a `String` position**. The
error moves from lex-time confusion to decode-time clarity — net
improvement.

### What stays the same

- Round-tripping: every existing quoted `String` content decodes
  identically. Existing `.nota` files don't break.
- First-token-decidability: leading byte still picks the token class
  (numbers, delimiters, strings, idents).
- The closed sigil and delimiter budget: no new delimiters, no new
  sigils.
- The PascalCase-head rule: unaffected — Path lives in value positions.

---

## 7. What designer needs to decide

1. **Adopt the `Path` newtype approach (§2.6 option a) over an
   attribute (option b)?** Recommendation: yes — typed shape over
   attribute-encoded type-distinction. **Status:** implemented as
   the typed-newtype path; see §9.
2. **Approve the bare alphabet (§2.1) including leading `/` and `.`?**
   Recommendation: yes (§5.1, §5.2). **Status:** implemented; see §9.
3. **Defer `Url` to a separate report (§5.5)?** Recommendation: yes.
   **Status:** deferred; no `Url` type added in this pass.
4. **Land in two commits — codec accepts wider tokens first, encoder
   canonicalises to bare second (§5.6)?** Recommendation: yes.
   **Status:** shipped in a single commit (lexer + decoder + encoder
   + `Path` newtype + tests). The split was a precaution against
   round-trip regressions; the test suite (§9.2) verified the joint
   change held end-to-end. Designer can override and split in
   follow-up if preferred.

After designer approval of the **spec text** (§2.7): the codec is
already implemented; what remains is (a) landing the spec section in
`repos/nota/README.md`, (b) optional `NotaPath` derive in `nota-derive`,
(c) the cosmetic migration of `skills/skills.nota` to drop quoted
paths. None of (a)/(b)/(c) blocks consumers from adopting `Path`
today.

---

## 9. Implementation evidence

**Codec shipped 2026-05-18.** Repository
`LiGoldragon/nota-codec`, branch `main`, commit `97c1f496`
("add Path type with relaxed bare-token alphabet at schema position").
Workspace claim taken under `second-designer-assistant` per user
direction to implement; claim released after push.

### 9.1 Files changed

| File | Change |
|---|---|
| `src/ident.rs` | added `PathByte` predicate (wide alphabet: `[A-Za-z_./]` start, `[A-Za-z0-9_\-./]` continue); added `Ident::is_bare_path` (used at decode/encode validation time). `IdentByte` + `Ident::is_bare_string` stay strict — the encoder still quotes path-shaped String content. |
| `src/lexer.rs` | bare-ident scanning switched from `IdentByte` to `PathByte` (start dispatch + continuation slurp). The lexer now produces a single `Token::Ident("skills/operator.md")` for path-shaped input; first-token-decidability preserved because leading digit still dispatches to `read_number`. |
| `src/decoder.rs` | `read_string` validates the bare-ident token content against `Ident::is_bare_string` (strict) and rejects path-shaped tokens with the new typed error below. New `read_path` accepts `Token::Str` or any `Token::Ident` whose content matches `Ident::is_bare_path`. |
| `src/encoder.rs` | new `write_path` mirrors `write_string` but uses the wide bare alphabet for bare-eligibility; falls back to inline-quoted form otherwise. `write_string` is unchanged — `String` field encoding still uses strict bare. |
| `src/error.rs` | new variant `Error::PathShapedTokenInStringPosition { content: String }` with a help-text message naming both remedies (quote the content, or use a `Path`-typed field). |
| `src/path.rs` | new module: `pub struct Path(String)` with `new`/`as_str`/`into_string`, `From<String>`/`From<&str>`/`From<Path> for String`/`AsRef<str>`, and the `NotaEncode` + `NotaDecode` impls delegating to `write_path` / `read_path`. |
| `src/lib.rs` | re-exports `pub use path::Path`. |
| `tests/path_round_trip.rs` | 25 tests covering bare-Path encode, bare-Path decode, quoted-form decode, round-trip via canonical text, quoted fallback for content with spaces / leading digit / reserved literal `None`, String-position rejection with the typed error, regression guards for strict bare-ident-as-String acceptance and reserved nexus-sigil rejection, lexer single-token production for path-shaped input, and a record schema position carrying `Path` (`(Skill operator skills/operator.md "…")`). |

### 9.2 Test surface

`cargo test` — **111/111 pass** across 11 binaries:

| Suite | Count | Result |
|---|---|---|
| `path_round_trip` (new) | 25 | pass |
| `horizon_rs_feedback_fixes` (existing bare-ident-as-String + multiline) | 16 | pass |
| `production_primitives` (existing primitives + containers) | 25 | pass |
| `lexer_tokens` (existing reserved-sigil rejection) | 3 | pass |
| `nota_record_round_trip`, `nota_enum_round_trip`, `nota_sum_round_trip`, `nota_transparent_round_trip`, `nota_try_transparent_round_trip`, `option_vec_struct_variant` | 42 | pass |

`nix flake check` — built from clean derivation on the remote builder;
**all checks passed**. The Nix surface confirms the cargo result and
satisfies `skills/testing.md` ("all tests live in Nix").

### 9.3 Verified behaviors

- `Path::from("skills/operator.md").encode(...)` → `skills/operator.md`
- `Path::from("/etc/hosts").encode(...)` → `/etc/hosts`
- `Path::from("./foo").encode(...)` → `./foo`
- `Path::from("../bar").encode(...)` → `../bar`
- `Path::from("README").encode(...)` → `README`
- `Path::from("with space").encode(...)` → `"with space"` (quoted fallback)
- `Path::from("01-intro.md").encode(...)` → `"01-intro.md"` (leading-digit quoted fallback)
- `Path::from("None").encode(...)` → `"None"` (reserved literal quoted fallback)
- `String::decode("skills/operator.md")` → `Error::PathShapedTokenInStringPosition { content: "skills/operator.md" }`
- `String::decode("foo")` → `Ok("foo")` (strict bare-ident-as-String still works)
- `String::decode("\"skills/operator.md\"")` → `Ok("skills/operator.md")` (quoted-form still works in String position)
- Record with `path: Path` field: `(Skill operator skills/operator.md "…")` round-trips
- Reserved nexus sigils (`~`, `@`, `?`, `*`) still rejected at the lexer

### 9.4 What did not land in this pass

- `repos/nota/README.md` — the §"Path bare form" spec text drafted
  in §2.7 of this report is the change designer needs to land. The
  codec ships ahead of the spec doc; the test suite is the
  falsifiable proof of the behavior.
- `nota-derive` — no `NotaPath` derive. `Path` works through manual
  impls; a derive is nice-to-have if/when the type appears with
  variants or as part of a bigger derive family. Not blocking.
- `skills/skills.nota` migration — the workspace canonical example
  (designer's commit `36bc77ad`, currently on the
  `push-ukwtxmxn-lanefix` branch) still quotes every path. The
  migration is cosmetic, backwards-compatible at decode, and trivial
  once designer's commit lands on main. Deferred to a follow-up
  (`Role operator skills/operator.md apex "…"` saves one quote pair
  per row — 40+ rows in the file).

### 9.5 Bead state

No new bead created. Designer-scope follow-up work is the spec text
in `repos/nota/README.md`; the codec implementation is closed.
If designer wants to formalise the spec-text + derive + migration as
a discrete tracking item, this report names the scope; bead is small
enough that opening one is a discretion call.

---

## 10. Follow-up 2026-05-19 — spec landed + workspace migration

Per user direction the same day as initial implementation:

### 10.1 Spec text landed in nota README

Repository `LiGoldragon/nota`, branch `main`, commit `a0617b99`
("spec: bare Path form section — typed Path widens the bare alphabet
to [A-Za-z_./]/[A-Za-z0-9_-./]"). New section `## Bare \`Path\` form`
placed after `### A clarification on bracketed bare idents`, before
the unrelated `## Path syntax` (which describes NOTA's nested-name
`:` separator — distinct concept; not renamed in this pass).

Section content matches §2.7's draft and the implemented behavior:
the two-row alphabet table (strict bare-string vs bare-`Path`); a
schema-level example using the canonical `(Skill <name> <Path>
<tier> "<description>")` shape; the "content that always quotes"
table covering spaces, leading digit, `~`, `:`, `\`, and reserved
literals; the canonical-form bare-emit-when-eligible note.

### 10.2 `skills/skills.nota` migrated to bare paths

Workspace `primary`, branch `main`, commit `9c018120`
("skills.nota: migrate path strings to bare per nota Path
typed-position rule (was quoted)"). Every quoted path string in
the typed-skill-index — `"skills/operator.md"`,
`"skills/component-triad.md"`, etc., ~40 rows — dropped to its
bare form. Descriptions stay quoted (they contain spaces and
punctuation).

The schema-comment header was kept stripped (designer's commit
`c5f80951` removed it earlier the same day as self-evident); the
file is data-only now, which is consistent with `skills/nota-design.md`
Rule 2 ("data lives in records, not in comments"). Any future
schema documentation lives in `skills/nota-design.md` rather than
as inline comments in the data file.

### 10.3 Still deferred

- `nota-derive` `NotaPath` derive — see follow-up analysis: useful
  if/when the workspace introduces multiple type-distinguished path
  newtypes (`RepoPath`, `CratePath`, etc.). Today there is one
  `Path` shape and the manual impl in `src/path.rs` covers it.
  Lift the manual impl into a `NotaPath` derive (in `nota-derive`
  alongside `NotaTransparent`) when the second consumer lands.

## 11. See also

- `repos/nota/README.md` §"Bare-identifier strings" — the existing
  bare-string carve-out this extends.
- `repos/nota/README.md` §"Newtype structs" — the canonical precedent
  for "schema-position determines what bare token means".
- `repos/nota-codec/src/ident.rs` — the byte-set definition that
  changes.
- `repos/nota-codec/src/lexer.rs:130-137` — the lexer entry-point for
  bare idents that the alphabet change widens.
- `skills/language-design.md` §3 "Position defines meaning", §11 "The
  parser stays small", §18 "Delimiters earn their place" — the design
  instincts this proposal aligns with.
- `skills/nota-design.md` — canonical NOTA design rules (designer commit
  `36bc77ad`, 2026-05-18). This proposal is the next density gain after
  the wrapping-type / data-not-comments / named-enums rules; quoted
  paths are the residue.
- `skills/skills.nota` — the file that benefits first.
- `repos/nota-codec/src/path.rs` (commit `97c1f496`) — the `Path` newtype
  shipped to nota-codec main.
- `repos/nota-codec/tests/path_round_trip.rs` (commit `97c1f496`) — the
  25-test falsifiable spec for bare-Path behavior.
- `reports/second-designer-assistant/6-roles-as-config-owner-socket-mutable-2026-05-17.md` —
  the prior lane report; mentions the eventual `orchestrate/roles.nota`
  shape that would also benefit.
