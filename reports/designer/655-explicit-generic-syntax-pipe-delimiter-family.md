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
- The exact inner shape `Name (| [params] <body> |)` — confirm.
- What `{| |}` is for (traits/impls is the lead candidate).

**Candidate intent to record on the psyche's go (Record works; edit-path is blocked):**
1. **Decision** — A type's kind is announced by its value delimiter; generics use the
   reserved pipe-parenthesis `(| … |)` (Spirit `j9du`'s extension point), mirroring the
   `[| … |]` string form. Realizes `j9du` and `3742`.
2. **Principle** — Binders scope their body by structure: a parameterized declaration nests
   its body inside the binding form so the parameters are in scope without any semantic
   side-channel. Retires the current key/value binder-threading.
3. **Decision** (when chosen) — `{| … |}` (pipe-brace) is assigned to [the next construct].

**Spirit edit-path blocker:** refining `3742`'s wording (it still reads "plus name
resolution") needs `Clarify`, which the deployed daemon rejected with
`sema: file written with v9, this build expects v10`. `Record`/`Lookup`/`Observe` work;
only the in-place edit path hit the store-version skew. Flagged for system-maintainer /
operator; new `Record`s can still land, so the candidate intents above are recordable, but
`3742` cannot be reworded until the daemon store is fixed.
