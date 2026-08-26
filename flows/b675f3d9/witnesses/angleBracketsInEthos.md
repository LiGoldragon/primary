# Angle-bracket `<>` syntax in Ethos

## Findings — psyche's verbatim words

### 1. `<>` for generics (2026-08-04)

> we could use .() for transformers, and <> for generics

— psyche, 2026-08-04T09:42:51Z, typed.
Source: transcript 6b31eff3-6477-4ee4-baed-cb491ebadd48.jsonl line 159.
Status: SUPERSEDED for transformers (`.()` → `.[ / .{` per a5587095:133, 2026-08-11);
the `<>` for generics half was not explicitly retracted at that time.

> and I want the Result<Vector<Sortable> Error> syntax for generics, since its
> more token efficient than using a dot, and recycles rust cognition

— psyche, 2026-08-04T09:42:51Z, typed (same turn).
Source: transcript 6b31eff3 line 159.
Status: UNRECORDED in Vision (ac1e9ec8/reports/datomSyntaxTranscripts.md:218).

### 2. Generic struct/enum syntax sketch (2026-08-04)

> ```ethos
> Sorted.{Vector<Ordered>}
> Range.{<Ordered> <Ordered>}
> Status.[Pending Ready.<Numeric>]
> ```
> are Vector, Option, Map really generics though? Im not talking about how
> rust sees it, but how we decide to see it. Or do we want to call those
> things generics? or something else?

— psyche, 2026-08-04T12:41:31Z, typed.
Source: transcript 6b31eff3 line 420 (datomSyntaxTranscripts.md:225, UNRECORDED).

### 3. Generic parameters are traits (2026-08-01)

> youre right; and the answer is the mandatory trait! so T would be a trait!
> and multiple trait in the declaration would just adjust the emitted rust -
> remember for us rust is assembly

— psyche, 2026-08-01, typed (psyche vision session).
Source: psyche-raw/Vision/genericParametersAreTraits.md lines 11–13.

### 4. Datom does not do generics; generics belong to Ethos (2026-08-11)

> datom doesnt do generics, it only carries data, like json (but strictly
> typed of course)

— psyche, 2026-08-11T17:35+02:00, dictated.
Source: psyche-raw/Vision/archive-datomSyntax.md lines 6–7 (flow 012fbf07).
Agent note (not psyche's words): generics belong to Ethos; Datom is the data
carrier. The 2026-08-04 rulings predate the Datom/Ethos split; each ruled
construct needs its language assigned.

### 5. In Ethos, generics and traits are essentially the same (2026-08-26)

> it's a trait because in ethos, generics and traits are essentially the same
> thing. If you understand what I'm saying or you're welcome to push back on
> that also.

— psyche, 2026-08-26, dictated.
Source: flows/f426777b/vision/nexusTraits.md lines 22–25.

### 6. The triggering quote: `Processable<[Clonable Sendable] Serializable>` (2026-08-26)

> I prefer
>
> Processable<[Clonable Sendable]  Serializable>
>
> what did I say about the <> syntax in ethos?

— psyche, 2026-08-26T15:33:06Z, typed.
Source: transcript b675f3d9 line 298;
flows/b675f3d9/vision/kinds.md lines 31–35.

### 7. ethos-monolith ARCHITECTURE.md (not psyche's words; cites usage)

`Vector<PathLockPath>` appears in the fixture; ARCHITECTURE.md line 46 notes
`Vector<T>` is the supported collection reference — no ruling quoted, agent-
authored note only.
Source: /git/github.com/LiGoldragon/ethos-monolith/ARCHITECTURE.md lines 35, 46–47.

---

## Method

- Method: probe `grep -rn "angle\|chevron\|bracket\|generic\|<T>\|<>" Vision/ psyche-raw/ flows/*/vision/`
- Method: probe `grep -rn "angle\|chevron\|<>" flows/*/log.md flows/*/reports/*.md`
- Method: probe `cat flows/ac1e9ec8/reports/datomSyntaxTranscripts.md` (section "Generics and angle brackets")
- Method: probe `python3` json parse of transcripts 6b31eff3 (lines 157, 159, 420) and b675f3d9 (line 298)
- Method: code read `/git/github.com/LiGoldragon/ethos-monolith/ARCHITECTURE.md`

---

## Summary

The psyche has said three things about `<>` in Ethos, across 2026-08 sessions.
On 2026-08-01 the ruling was that generic type parameters are traits — `T`
would be a trait. On 2026-08-04 (flow 6b31eff3) the psyche proposed `<>` as
the delimiter for generics in Ethos (with `.()` for transformers) and sketched
`Result<Vector<Sortable> Error>` as the preferred syntax, recycling Rust
cognition; that transformer half was superseded on 2026-08-11 but the `<>`
for generics was not retracted. On 2026-08-11 the psyche clarified that Datom
does not do generics at all — generics belong to Ethos. On 2026-08-26 (flow
f426777b) the psyche said generics and traits are essentially the same thing
in Ethos. On 2026-08-26 (flow b675f3d9, line 298) the psyche wrote
`Processable<[Clonable Sendable] Serializable>` — using `<>` to hold
kind-constraints — and then asked "what did I say about the <> syntax in
ethos?", indicating they recalled a prior ruling but could not retrieve it.
No recorded ruling explicitly closes or supersedes the 2026-08-04 `<>` for
generics decision; the 2026-08-04 sketch was flagged UNRECORDED in the
ac1e9ec8 distillation.
