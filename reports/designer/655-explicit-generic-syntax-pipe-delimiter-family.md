# 655 — Explicit generic syntax: the pipe-delimiter family (design review)

A consolidation of the design thread that ran out of the generics/traits review (`654`).
The psyche drove three corrections and landed a clean direction; this is "review all this"
in one place. Companion: `654` (what generates vs what's hand-wired). Intent: `3742`
(recorded), `j9du`, `549v`, `4itr`, `7c71`; new decisions below are **candidate intent,
held for the psyche's confirmation** (and the Spirit edit-path is currently blocked — see
end).

## The defect, in two parts (both verified in source)

**1. A generic is identified by guessing, not by a marker.** `(Foo A B)` is byte-for-byte
the same form whether it is a generic *declaration head* introducing binders `A`,`B`
(read by `DeclarationHead::from_block`, `schema.rs:1382-1416`) or a generic *application*
applying `Foo` to `A`,`B` (`TypeReference::Application`, `schema.rs:1431-1463`). The only
thing telling them apart is **which slot** it sits in (key vs value of a namespace map,
`source.rs:511`). The form never says "I am a parameterized type."

The psyche's sharpening: name resolution at a *use* site is **not** the problem — resolving
`(Work …)` against an explicit declaration is deterministic lookup, exactly how `(Vector X)`
is known. `Vector` is known because it is **built into the language**; `Work` is yours, so
it is known **only because you declare it**. The defect is purely that the *declaration*
doesn't announce its kind.

**2. Binders scope the body through a side-channel, not structure.** Today a declaration is
a `key value` pair — `(Work A B)` (key, carrying the binders) and the body (value) are
**two separate objects**. The body can only see `A` and `B` because a semantic pass
(`identity.rs` closure walk) quietly threads the binders from key into value. Structurally
the binders are out of scope in the body; a side-channel papers over it. The psyche's words:
*"the second object is outside the first, so A and B are out of scope."*

Per Spirit `3742` (Principle, High): [A type's kind must be explicitly marked in the
syntax, never inferred from position or guessed. A parameterized type must be declared as
such by an explicit signal — a delimiter, a wrapping structural variant, or a reserved
keyword head as the built-ins Vector/Map/Optional already are.]

## The fix: the kind is the delimiter, and generics get `(| … |)`

The kind of a value is **already** announced by the delimiter that wraps it:

| Value form | Kind |
|---|---|
| `Name { … }` | struct |
| `Name [ … ]` | enum |
| `Name <ref>` | newtype |
| **`Name (\| … \|)`** | **generic** (new) |

The bracket *is* the kind — no keyword to read, the same move `{}`/`[]` already make. This
is the psyche's idea: use the pipe-parenthesis delimiter, written pipes-**inside** `(| |)`
to mirror the existing `[| |]` string form (not my earlier `|( )|` with pipes outside).

And it is not an invention — it is exactly the slot the notation reserved. The pipe-bracket
family is a closed set of three (Spirit `j9du`):

```
  [| … |]   pipe-text         → bracket-safe / multiline STRINGS      (already used)
  (| … |)   pipe-parenthesis  → GENERICS                              (this decision)
  {| … |}   pipe-brace        → the next construct we need to define  (reserved; see §below)
```

`j9du`: *"the pipe-parenthesis and pipe-brace delimiters … are reserved as extension points
for extended NOTA languages such as schema to define their own constructs."* Assigning
`(| |)` to generics is precisely that.

This also defuses the one real objection to a delimiter ("you'd have to know it means
generic"): you already have to know `[| |]` means string, and that is fine. `(| |)` =
generic is the identical deal, and consistent with it.

## Concrete shape — and it fixes scope for free

Because the params and the body live **inside the one `(| … |)`**, the binders scope the
body by structure — no side-channel:

```
;; BEFORE — kind implicit, binders threaded across a key/value split
Work (Work A B)               ;; key carries binders ...
     [ (SignalArrived A) (Completed B) ]   ;; ... value (body) is a separate object: A,B out of scope

;; AFTER — kind explicit (the (| |) delimiter), binders scope the body structurally
Work (| [A B]
       [ (SignalArrived A) (Completed B) ] |)   ;; A,B are IN scope: body is inside the (| |)
```

Proposed shape: **`Name (| [params] <body> |)`** — the `(| |)` says "generic," `[params]`
is the binder list, `<body>` is an ordinary struct/enum body that can see the binders. A
generic enum and a generic struct differ only by the inner body delimiter (`[ ]` vs `{ }`):

```
Sema (| [Root]
       { origin_route.OriginRoute root.Root } |)   ;; generic STRUCT over Root

Work (| [Event WriteDone ReadDone EffectDone]
       [ (SignalArrived Event) (SemaWriteCompleted WriteDone)
         (SemaReadCompleted ReadDone) (EffectCompleted EffectDone) ] |)   ;; generic ENUM
```

Use sites stay bare and resolve by name — `(Work SignalInput SemaWriteOutput …)` — exactly
as `(Vector X)` does, because `Work`'s `(| |)` declaration has made it a *known* generic.

## It already parses — this is schema-level work only

Verified directly in nota-next (correcting an earlier claim that it needs seed-parser
support): the parser **already** produces these blocks. `Delimiter`/`MacroDelimiter` carry
`PipeParenthesis` and `PipeBrace` (`macros.rs:42-47`, `parser.rs:115`, `parser.rs:125`);
`[| |]` is `Block::PipeText`. So `(| … |)` and `{| … |}` already parse into structured
`Block::Delimited` values with their own delimiter tag — they simply carry **no schema
meaning** yet. The work is:

1. **nota-next derive** — let a `#[shape(…)]` recognize the `PipeParenthesis` delimiter, so
   a generic node decodes from `(| … |)` the way headed forms decode from `( … )`.
2. **schema-next** — make the declaration reader treat a `(| [params] body |)` value as a
   parameterized declaration whose binders scope the body **structurally** (retiring the
   key/value side-channel threading in the closure walk), and arity-check uses as today.
3. **schema-cc** — the generic construct's shape joins the compiler-definition-as-data
   (`vpbx`), not a hand-written arm.

No change to the seed parser; the delimiters are already there.

## The delimiter-space map, and `{| … |}`

The full closed delimiter set, with this decision applied:

| Delimiter | Holds | Meaning |
|---|---|---|
| `( … )` | objects | application / headed form / record |
| `[ … ]` | objects | enum body, vector, parameter list |
| `{ … }` | objects | struct body, namespace, map |
| `[\| … \|]` | text | bracket-safe / multiline string |
| `(\| … \|)` | objects | **generic** |
| `{\| … \|}` | objects | **reserved — the next construct** |

`{| … |}` is the last reserved slot. The natural candidate, given `654`, is **traits /
impls as data** — the other major construct the schema still cannot express (every trait
and impl today is a proc-macro derive, a hardcoded `quote!` template, or hand-written; see
`654`). If `{| |}` becomes the trait/impl construct, the two reserved pipe-delimiters end up
carrying exactly the two capabilities `654` identified as missing: generics (`(| |)`) and
traits/impls (`{| |}`). Open for the psyche to assign.

## Settled / open / candidate intent

**Settled (psyche-driven this session):**
- Name resolution at use sites is legitimate, not guessing; the defect is the declaration.
- The kind must be explicit on the declaration form (`3742`, recorded).
- Generics use the `(| |)` pipe-parenthesis delimiter, pipes inside, mirroring `[| |]`.
- Binders scope the body by structure (body nested inside `(| |)`), retiring the
  key/value side-channel.

**Open:**
- What `{| |}` is for — **still unassigned**. The psyche confirmed the generic shape but
  did not pick the pipe-brace slot; traits/impls remains the lead candidate (`654`).

**Intent captured** (the psyche confirmed the design):
1. **Decision — recorded `hh3z`**: [A type's kind is announced by the delimiter that wraps
   its value (brace → struct, square-bracket → enum); generics use the reserved
   pipe-parenthesis `(| … |)`, pipes inside, mirroring the pipe-text string delimiter; a
   generic declaration is `Name (| [params] body |)`.] Realizes `j9du`'s reserved extension
   point and `3742`.
2. **Binders-scope-by-structure — no standalone record.** The guardian rejected a separate
   principle as `Compound` with `3742`/`hh3z`, correctly: `hh3z` already encodes it — the
   body is *nested inside* the `(| … |)` form, so the binders scope it structurally, and the
   closure-walk key/value side-channel is retired as a consequence. Rationale lives in
   §"Concrete shape." (Right call: a refinement rides or edits an existing record, it does
   not bolt on a near-duplicate.)
3. **`{| … |}`** — held open, see above.

**Spirit edit-path blocker:** refining `3742`'s wording (it still reads "plus name
resolution") needs the `Clarify` operation — which *edits the record's description in
place* (`store/mod.rs:931`), the correct way to clarify (never a new `Clarification` record
beside it). The deployed daemon rejected it with `sema: file written with v9, this build
expects v10`; `Record`/`Lookup`/`Observe` work, only the in-place edit path hit the
store-version skew. Flagged for system-maintainer / operator; `3742` cannot be reworded
until the daemon store is fixed.

## STOP at the manifestation gate — the pipe delimiters had a prior assignment

Manifesting into the repos' `INTENT.md` was halted: a broader Spirit query (`ContainsText
pipe`) surfaced a cluster of **prior records that already assign the pipe delimiters — to
struct/enum *declarations*, not generics/traits.** This is the contradiction the guardian
caught when it rejected `{| |}`=traits. The initial review leaned on `j9du`
("reserved, no assigned meaning") and did not search the full pipe-delimiter history; this
is that gap, caught at the right gate (before overwriting).

| Record | Kind / certainty | What it says about the pipe delimiters |
|---|---|---|
| `td1d` | Decision / Low | **pipe-brace declares a struct** (first item names the type, rest fields); **pipe-paren declares an enum** (first item names the type, rest variants) |
| `010y` | Clarification / Low | pipe forms may become built-in declaration delimiters — brace-pipe struct, pipe-paren enum |
| `1rci` | Clarification / Medium | pipe-brace is a one-off named struct wrapper (first object names the struct type, rest is the field body) |
| `7m84` | Decision / Medium | authored schema declarations should use pipe-family forms for struct and enum |
| `f743` | Decision / Medium | schema declarations live in pipe-family forms for struct, enum, newtype |
| `nbvg` | Clarification / Low | pipe-declaration struct/enum forms allow nested shapes |
| `own9` | **Correction / High** | the **legacy pipe declaration forms are transitional and being replaced by the positional form** (`{…}` struct bodies, `[…]` enum/variant lists) — per psyche 2026-06-06 |
| `j9du` | Principle / Low | pipe-paren / pipe-brace "carry no assigned meaning, reserved as extension points" |
| `3qjw` | Decision / Medium | pipe-text `[\| … \|]` = multiline string (no conflict — consistent with our use) |
| `hh3z` | Decision (this session) | pipe-paren `(\| … \|)` = **generics** — contradicts `td1d`'s pipe-paren=enum |

**The reconciling fact is `own9` (High):** it already *vacated* the pipe-struct/enum
declaration forms in favor of the positional `{…}`/`[…]` forms the schema uses today. So
the pipe delimiters are, by `own9`, freed — which is exactly why reassigning them to
generics/traits is *coherent*. But the older `td1d`/`010y`/`1rci`/`7m84`/`f743`/`nbvg`
records were never formally retired, so they still sit in Spirit contradicting the new
assignment (and `nota-next/INTENT.md` lines 24-27 still carry the stale "pipe = enum-like /
struct-like declarations" text). `j9du` ("no assigned meaning") is itself already in tension
with `td1d` — the store was internally inconsistent before this session.

### Decision (made): overwrite the deprecated design

The psyche confirmed: *"we are overwriting that old deprecated design."* The freed pipe
delimiters are reassigned to generics (`(| |)`, `hh3z`) and traits/impls (`{| |}`),
**superseding** the legacy pipe-struct/enum intent (`td1d` and the cluster
`010y`/`1rci`/`7m84`/`f743`/`nbvg`) — which `own9` (High) already started by moving
struct/enum to the positional `{}`/`[]` forms. `j9du`'s "no assigned meaning" likewise
yields to the new assignment. So the only live work is mechanical cleanup of the stale
records, not a design question.

### Blocker chain (all gated on the daemon store fix)

Resolving this needs `Supersede`/`Retire`/`Clarify` on the stale records, re-recording
`{| |}`=traits once the contradictors are gone, and rewording `3742` — **all of which use
the Spirit edit/supersede path the daemon currently rejects** (`v9` vs `v10` store skew).
So the cleanup cannot land until system-maintainer fixes the spirit daemon store.
Meanwhile `hh3z` ((| |)=generics) is recorded but formally contested by the un-retired
`td1d`; it should be reconciled in the same supersession pass.

**Manifestation:** the `INTENT.md` text manifestation proceeds (the psyche authorized the
overwrite) — removing `nota-next`'s stale "pipe = enum-like / struct-like declarations"
text and stating the new direction (generics `(| |)`, traits/impls `{| |}`, struct/enum via
positional `{}`/`[]`). The **Spirit-record cleanup** (superseding the `td1d` cluster,
recording `{| |}`=traits, rewording `3742`, reconciling `j9du`) is **pending the daemon
store fix**: `Supersede`/`Retire`/`Clarify` all use the rejected v9/v10 edit path, and
`{| |}`=traits cannot be recorded until its contradictors are retired. The `INTENT.md`
manifestation notes this so the file and the (temporarily un-reconciled) Spirit store don't
read as a silent contradiction. Sequence to finish once the daemon is fixed:
system-maintainer fixes the store → supersede the `td1d` cluster + reconcile `hh3z`/`j9du` →
record `{| |}`=traits → reword `3742`.
