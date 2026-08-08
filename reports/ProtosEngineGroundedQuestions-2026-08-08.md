# The Engine From the Ground Up — Carrying the Open Questions

2026-08-08 — Designer, for the psyche.

**What this is.** Each section teaches one area of the engine *as actually
built* — assuming no knowledge of the code, marking which names are yours
and which are agent coinage — and ends with the question that lives there.
Nothing here requires reading any other document. Where I don't know
something, I say so.

---

## 1. The whole machine in one pass

What exists today is a pipeline that turns a small text file into Rust
code inside a library, plus daemons that use those libraries to talk to
each other.

1. **An author writes an interface file** in Ethos syntax (a real one is
   ten lines; see §2).
2. **The parser** (crate `core-ethos`) reads it into typed structure.
3. **The naming authority** (crate `sema-translator`) mints every declared
   thing a permanent random hidden name — an `EncodedName`. This is your
   three-layer naming vision in the flesh: the text name is presentation,
   the hidden name is identity, renaming in text breaks nothing.
4. **Lowering** (crate `core-nomos`) turns the parsed declarations into
   `WholeLogos` — a fully explicit typed description of a program:
   "a struct with these fields", "an enum with these variants", "this
   type implements the Input trait". This step is where Nomos-the-language
   will eventually live; today it is a fixed Rust function — the
   temporary hack you sanctioned until self-hosting.
5. **The Rust emitter** (crate `rust-logos`) prints that description as
   Rust source text — direct printing driven by the hidden names, none of
   the Rust ecosystem's macro machinery.
6. The printed Rust is committed inside a **contract crate** — a library
   that a daemon and its clients both depend on, so both sides agree on
   every message type. `signal-spirit` is "the contract for talking to
   Spirit"; `meta-signal-spirit` is the contract for Spirit's
   configuration plane.

Per component, three authored files describe three worlds (your file-kind
ruling): the **Interface** (everything that can be said to and by the
component), **Nexus** (the behavior contracts — traits — its daemon
implements), and **Sema** (what it stores: record types and tables).

The overnight round genuinely moved Spirit's two contract crates onto this
pipeline: their generated code is produced by steps 2–5 and committed with
a freshness hash. That holds. What I overstated — and the codex audit
caught — is the wider vertical: Nix-level checks, several test layers, the
Nexus/Sema files, and the daemon itself are not green. §7 shows exactly
what is and is not proven.

---

## 2. The observer, and what `Tap` / `Untap` actually are

Spirit is your decision-record daemon. The **observer** is the feature
where a client says: *let me watch what Spirit is doing* — every operation
it performs, every effect — streamed live as it happens.

An Interface body has five sections, in fixed order — your
sections-confer-traits ruling means *where* a type sits **is** its role:

| Section | Meaning |
|---|---|
| Input | messages a client may send |
| Output | messages the component may answer |
| Refusal | the ways it can refuse |
| Stream | what it can push continuously |
| Declarations | shared types with no role |

Here is the actual blessed fixture file, line by line. Every name in it
was coined by agents during the night round — the metaphor is tapping a
phone line:

```
Interface.{1 0 0}                        ;; header: kind Interface, version 1.0.0
[signal/domain.[ObserverFilter ObservationEvent]]   ;; imports from shared vocabulary
{
  [Tap.ObserverFilter                    ;; INPUT: "start watching, filtered like this"
   Untap.ObservationTapToken]            ;; INPUT: "stop the watch with this token"
  [ObservationTapped.ObservationTapToken ;; OUTPUT: "watch is on — here is its token"
   ObservationUntapped.ObservationTapToken] ;; OUTPUT: "watch stopped"
  [UnknownObservationTap.ObservationTapToken] ;; REFUSAL: "no such watch"
  [Observation.ObservationEvent]         ;; STREAM: pushed events, element type
  []                                     ;; DECLARATIONS: empty
}
```

So the built-in lifecycle is: client sends `Tap` with a filter → Spirit
answers `ObservationTapped` carrying an `ObservationTapToken` (a numbered
receipt identifying this watch) → `Observation` events flow → client sends
`Untap` quoting the token → `ObservationUntapped`.

The pushed event type, in the shared vocabulary (also agent-drafted):

```
ObservationEvent.[OperationObserved.OperationKind      ;; "an operation happened, of this kind"
                  EffectObserved.EffectKind            ;; "an effect happened, of this kind"
                  ObservationLagged.DiscardedOperationCount ;; "you fell behind; N events dropped"
                  ObservationEnded.ObservationEndReason]    ;; "the stream is over, because…"
```

On 2026-08-07 22:10Z you said: **"the fixture is blessed, and / for
imports."** I treat that as blessing the *syntax shape* — five sections,
the header triple, slash imports, element-type-only stream section. The
names and the lifecycle semantics inside are agent coinage, fully yours to
rename or reject.

**Why there was an open question at all:** the pre-redesign interface had
`Observe.Query` — a one-shot "give me records matching this query". When
the stream arrived, I held open whether `Observe` should *also* mean
"start streaming". But the blessed fixture carries its own complete
start/stop. Codex reads the question as dissolved: `Observe` stays a
one-shot query; `Tap`/`Untap` own the stream.

> **Question 1.** Should watching Spirit work exactly as the fixture says —
> `Tap` with a filter to start, token receipt, pushed `Observation`
> events, `Untap` to stop — with the one-shot `Observe` query remaining a
> separate, unrelated verb? Or do you want a different anatomy or
> different names?

> **Question 1b.** `ObservationTapToken` (the numbered receipt) currently
> exists nowhere: the fixture uses it but neither imports nor declares it —
> verified: the blessed file cannot pass the reader once anything actually
> reads it. Should it be declared inside the Interface's Declarations
> section (as `ObservationTapToken.Integer`), or owned by the shared
> `signal/domain` vocabulary and imported?

---

## 3. The vocabulary types with no bodies

Four types in the event enum above are named but have **no defined
variants** — nobody has said what they contain:

- `OperationKind` — what kinds of operation can be observed. For Spirit
  the natural candidates are its own verbs (recording, querying, …).
- `EffectKind` — what kinds of effect.
- `ObservationEndReason` — why a stream ended. Evidence so far supports
  only one real case: daemon shutdown.
- `ObserverFilter` — what a client can filter a watch by. Proposed
  minimal body: `ObserverFilter.[All OperationsOnly EffectsOnly]`.
  (`DiscardedOperationCount` is just a count — `Integer` newtype.)

The structural fork underneath: are `OperationKind`/`EffectKind`
**universal** vocabulary every component shares (one fixed list of
operation kinds for the whole system), or **per-component** (Spirit's
operation kinds are Spirit's verbs; each component has its own)? The
evidence — these live in `signal/domain` today but describe Spirit's
verbs — leans per-component; codex agrees.

> **Question 2.** Per-component or universal? And do the minimal bodies
> above suffice to start — `ObserverFilter.[All OperationsOnly
> EffectsOnly]`, `ObservationEndReason` with daemon shutdown only?

---

## 4. Writing to Spirit: per-verb types vs `Entry`+`Kind`

Spirit stores your records. Two designs for the *write* side exist in the
estate, from different eras:

**Old (per-verb):** four distinct input types, each with its own receipt —
`Proposal` (propose a new record), `Clarification` (attach a
clarification), `Supersession` (this record replaces that one),
`Retirement` (retire one). Rich, but every new verb grows the interface.

**Current (unified):** one write verb whose payload is an `Entry` struct
carrying a `Kind` field — an enum tag saying what kind of record this is
(the old minimal fixture had `Kind.[Decision Principle Correction
Clarification Constraint]`). One verb; kinds are data; adding a kind
doesn't change the interface.

The overnight rescue copied the old per-verb types into the new files
(§5), which is how the two designs came to coexist. Nothing is wired to
generation until this resolves.

The deciding test: does any verb carry structure a kind-tagged `Entry`
cannot express? `Supersession` must name its victim record. **I do not
know** whether the current `Entry` can carry a record reference — that is
exactly what to check against each verb, and I'll bring you the per-verb
anatomy comparison if you want it before ruling.

> **Question 3.** Does `Entry`+`Kind` supersede the per-verb taxonomy?
> If yes, do any of the four verbs carry irreducible anatomy that must
> survive as structure (e.g. supersession's target reference), and how?

---

## 5. The rescued Nexus and Sema files — why they cannot even parse

The file kinds, concretely:

- **Nexus** body: two sections — `[trait declarations] [supporting types]`.
- **Sema** body: two sections — `[record types] [table declarations]`,
  e.g. `records.{StoredRecord RecordIdentifier}` = "a table of
  StoredRecords keyed by RecordIdentifier".

Spirit's Nexus and Sema lived in the condemned old repo. Overnight I
transcribed them into `spirit/schema/nexus.ethos` and `sema.ethos` in
current syntax — and, my own assumption, gave each a **third section** for
wire/decision types that fit neither ruled section. Verified since: the
strict reader accepts *exactly two* sections for these kinds, so both
files are currently unparseable, and nothing reads them — they are
notebooks, not source. (Spirit itself still builds through the *old*
pipeline meanwhile.)

> **Question 4.** Fork: **(a)** treat the transcriptions as notebooks —
> after Questions 1–3 resolve, re-derive proper two-section files, with
> the wire types living where they belong (most likely the Interface's
> Declarations section); or **(b)** rule a third section into the Nexus
> and Sema file kinds, and the reader follows. My proposal is (a); the
> ruling is yours.

> **Question 4b — the countersignature.** The whole file-kind scheme —
> header as `Kind.{Major Minor Patch}`, imports as the second object,
> the section orders above — shipped as *provisional*, explicitly
> awaiting your read; you have ruled pieces of it in passing, never the
> whole. Everything downstream now treats it as law. Countersign it, or
> mark corrections, and it stops being provisional.

---

## 6. What is `Integer`?

Builtins are types that exist without declaration: `String`, `Integer`,
`Boolean`, `Unit`, `Vector`, `Option`, `Map`, `Result`. The emitter maps
them to Rust. Three are uncontroversial (`Boolean`→`bool`, `Unit`→`()`,
`Vector`→`Vec`). For `Integer` I chose signed 64-bit (`i64`) as a tagged
assumption — the old pipeline disagreed with itself (unsigned in one
consumer, signed in another).

Codex's point, which I endorse: the Rust mapping should *follow* the
meaning, not define it. Nothing says yet whether `Integer` is signed,
whether it is bounded, or what overflow means. Note this touches §2: the
observation token is an `Integer` newtype.

> **Question 5.** What is `Integer` — signed? bounded? overflow
> semantics? (The `i64` mapping then falls out, or gets corrected.)

---

## 7. What "done" currently proves — and what it doesn't

The proof layers, plainly:

- **Per-repo tests** (`cargo test`). Discovery: nine repos — including
  core pipeline crates `rust-logos`, `core-nomos`, `sema-translator`,
  `schema-rust`, `structural-codec` — carry a manifest flag
  (`autotests = false`) that silently *unregisters* their test files.
  The files exist on disk and look like coverage; cargo never compiles
  or runs them. My earlier "these tests pass" claims for those crates
  were unsupported.
- **Family check** (`nix flake check`). The whole-family proof. It
  currently **fails** for `signal-spirit`: the Nix packaging filters out
  the very schema file the build needs (so the Nix build can't see it),
  plus four lint errors.
- **Freshness digest.** Generated code embeds a hash of its source text;
  the build refuses if the source drifted. But it binds *only the source
  text* — not which generator version produced the output.
  `meta-signal-spirit` demonstrates the hole live: it pins an emitter
  two commits old, its digest shows green, and its output lacks what the
  current emitter would produce — patched by hand-written code.
- **The blessed fixture** is read by no test at all.

This is the mechanical reason my "all suites green" was wrong: every
green I cited was real but proved less than I presented.

> **Question 6.** Proposed law for the working skill, in one breath:
> *nothing is reported landed unless every on-disk test is registered
> and running, `nix flake check` is green, freshness digests bind the
> generator revision, and every blessed artifact has a consuming test.*
> Approve, amend, or reject — on your word I put it in the skill.

---

## 8. Nomos and the escape algebra

Nomos today is only the hardcoded lowering function from §1. The designed
language: a **transformer** is a named machine that expands one authored
declaration into many generated ones. Its body is a **template** — the
output with holes. The **escapes** are the holes:

- `Realize` — drop one bound value into a position.
- `Splice` — flatten a bound list into a vector.
- `Invoke` — call another transformer (including itself, recursively).
- `InsertAt` — place an item at a *specific position* in a vector; this
  answers your July requirement, verbatim: "a particular spot in a
  vector where a certain item gets inserted".

Illustrative only (spelled in a now-dead syntax era): a `Stream`
transformer could take one declaration and expand it into the token
newtype, the initiation/termination inputs, and the membership
implementations — names synthesized from the stream's name, as you
described on 08-06.

History, precisely: in late July you approved — at delegated-assent
grade, explicitly not conviction — recursion staying one authored
`Invoke` concept (no separate `Fold`) plus `InsertAt` as a fourth
member. A day later you said: **"the po2.19 surface question… is not yet
ruled — do not build recursion surface until it is."** The August
redesign then deleted that implementation entirely. So: direction leaned,
surface unruled, code gone.

> **Question 7.** Not for today's ruling — for scheduling. Nomos-as-a-
> language needs a design campaign with you: its file kind, its package
> carrier, the concrete escape spellings under the current colon syntax,
> and whether the July lean (`Invoke`, `InsertAt`) stands. Shall I
> prepare that campaign as its own sitting, after the Spirit vertical?

---

## 9. Two vision documents claim the same throne

Two consolidations of your Protos vision exist, one day apart:
`reports/deep-vision/protos-engine-renewed-vision-2026-08-06.md` (named
by your standing instruction as the reacquisition authority) and
`design/ProtosEngine/VISION-2026-08-07.md` (newer, carries the 08-07
rulings the older one lacks). Each preserves verbatim of yours the other
dropped. Neither mentions the other.

> **Question 8.** Name the survivor; I fold the loser's unique material
> into it and retire it.

---

## 10. Housekeeping tail (flag, not argument)

- `spirit-ethos` (condemned repo): still alive and buildable; its death
  is scheduled work.
- A stale pre-rename clone of `core-ethos` sits at the old
  `core-schema` path; referenced by nothing; deletable on your word.
- The migrated pipeline reads authored files with the `.schema`
  extension; `.ethos` is unruled convention. Rename or bless.
- 43 of 60 Dotos data files still use pre-ruling syntax; no current
  Dotos spec document exists.
- `OpenedStream` (my rename of the runtime stream handle, to cede
  `Stream` to the universal trait) awaits your yes/no.
- `WholeLogosVisibility` (`Public`/`Private`) survives in the program
  description against your visibility-death ruling; item-level `Private`
  is never produced.

---

*Reading order: Questions 1–3 unblock the working Spirit. 4–6 make its
ground safe. 7–8 open the next campaign.*
