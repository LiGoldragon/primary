# Ethos implementations: a design for bodies on kinds (Opus)

Subflow of e51411, 2026-09-25, answering the living's ask of that day (flows/e51411/vision/ethos.md).

**In short.** The whole extension needs no new glyph and no new keyword. It adds one structure: in the association section, a kind that carries a brace holds that type's bodies for the kind. A body is a *datom of the yield type with holes*: construction is written as datom, and a call is a lowercase head that carries its arguments, the same way a query variant carries its payload. Variable names are gone. A value is named by its type, as a field already is, and Pāṇini's *anuvṛtti* (carry-over) decides what an unwritten name refers to. The worked Orchestrate ledger comes to **44 lines and 509 tokens**. The Rust it replaces is **226 lines and 1681 tokens**. That is 3.3× smaller, but the glyph share is unchanged at about 60% (details below). **Witness:** today's protos reader already accepts the whole example. ethos-zero 10.0.0 fails it only at the conceptual layer, at the first body (`Conceptual.{ [ 3 0 1 0 ] Expected.Reference }`). **Verdict:** the syntax costs almost nothing, and the risk is in the scope rules. Build a resolve-only prototype now, after the audit's generator fixes. Do not start Rust emission yet.

## 1. The extension, in rules

Everything below is protos as it stands: heads, the three separators, `{ } [ ] < >`, bare runs, and `« »`.

```
Association    := Type.[ (Kind | Implementation)… ]         ; a bare Kind stays today's compile-time assertion
Implementation := Kind.{ Body… }                            ; simple kind: one body per capability, in the kind's order
                | Kind.{ [ Type… ] [ Constant… ] { Body… } } ; complex kind: associated types, constants, bodies
Body           := [ Step… ]                                 ; each step's value is bound under its type; the last step is the yield
Step           := Expression | Self.{ Expression… }         ; the second form rebinds Self, and is allowed only under a `!` capability
Expression     := Name(.Name)*                              ; a value in scope, then projections by field type: Lock.LockName
                | capability[.Arguments]                    ; a call: the receiver alone, or { receiver input… }
                | Variant[.Expression]                      ; a construction; an omitted payload is filled
                | Type.{ … } | { … } | [ … ] | bare | «…»   ; datom literals, read by position as datom is
                | [Name.][ Arm… ]                           ; a match on Name, or, with no head, on the previous step
Arm            := Variant.Expression | Expression           ; the payload is bound by its type; a last unheaded arm is the general rule
```

Case already separates the three things a head can be. A **lowercase head is a capability** (kinds already write `summarize`, `push`). A **capitalized head is a variant or a value**, and the expected type decides which: a head that names a variant of the expected type constructs, and otherwise it names a bound value. This is the datom rule, "what a structure means is said by the position it sits in", carried into code.

Four rules give the semantics. They are the whole of the "no noise" machinery.

1. **Scope (anuvṛtti).** Values in scope are Self, the inputs, each step's result, loop elements and arm payloads. Each is named by its type. A struct in scope also *carries* its fields, each named by its type. To resolve a name, a direct value beats a carried field, and a nearer value beats a farther one. A tie is refused, and the author must then qualify (`Self.LockName`, `Lock.LockName`). This is Pāṇini 1.4.2, *vipratiṣedhe paraṃ kāryam*: in a conflict, the later rule prevails.
2. **Fill.** A construction or call whose positions are not written is filled from scope, one unique value per position. So `Locked` alone means `Locked.Lock` with the Lock at hand, and `admit` alone means `admit.{ LockRequest Lock }`. A struct type named where no value of it is bound is built from scope (Haskell's `Lock{..}`). The canonical print omits every filling that would resolve the same way, so there is one written form, as with protos canonical spacing.
3. **Exit (typed rejection).** Suppose a step yields `Err.E`. If the capability's yield is `Result<_ E>`, the step leaves with that Err. If the yield is an enum with a variant carrying `E` (unique, because variants are named by type), it leaves as that variant. Otherwise `Ok.X` binds X. This is Rust's `?` without the glyph. `Response` carries `LockRejected.LockRejection`, so a refusal anywhere in `lock` exits as `LockRejected`.
4. **Effect.** Only a `!` capability changes Self, and it does so by a `Self.{ … }` step. That step constructs a whole new Self; nothing is mutated in place. Everything else is pure. The runtime owns I/O: it persists Self after a changing `!`, and it calls `announce` then (see the example). Other I/O comes in as imported kinds implemented in Rust through the existing `Ethos.Rust` escape.

Two more positions exist, and only intrinsics use them. The second position of `each`/`find`/`any`/`drop` is a *body position*, evaluated once per element with the element bound by its type. The key position of `sort` is a bracket of such bodies. The intrinsic capabilities used below are `equal not require either any find drop each include empty repeat sort append split join concatenate begin increment`. `require.{ Boolean Rejection }` yields `Ok.True` or `Err.Rejection`. `repeat` yields the first repeated element as an Option. `either` is `any` over a literal vector of Booleans.

## 2. The worked example: the Orchestrate lock logic, wholly in ethos

The contract is `signal_orchestrate`, with `LockPaths.Vector<LockPath>` as in `ethos-zero/fixtures/orchestrate.ethos`. The example needs one contract change, which the design pushes rather than just allows. The Rust turns bad user paths into `StoreError`, an infrastructure error. Here they become typed refusals: `LockRejection.[ DuplicateName.Lock PathOverlap.LockOverlap RelativePath.LockPath ParentComponent.LockPath RepeatedPath.LockPath EmptyPaths ]`.

```
Library
[ signal_orchestrate:[ LockId LockPath LockPaths LockRequest Lock LockOverlap
                       LockRejection ReleaseRejection Query Response
                       ObserveSelection Observation ]
  nexus:Answering ]
[ Locks.Vector<Lock>
  Ledger.{ Locks LockId } ]                                   ; the held locks, and the next LockId
[ Normalizable.[ normalize.[ Result<Self LockRejection> ] ]
  Nestable.[ nest.{ [ LockPath ] [ Boolean ] }
             contain.{ [ LockPath ] [ Boolean ] }
             meet.{ [ LockPaths ] [ Boolean ] } ]
  Admitting.[ admit.{ [ Lock ] [ Result<Lock LockRejection> ] } ]
  Lockable.[ lock!{ [ LockRequest ] [ Response ] }
             release!{ [ LockId ] [ Response ] }
             observe.{ [ ObserveSelection ] [ Observation ] } ] ]
[ LockPath.[ Normalizable.{ [ require.{ begin.{ Self / } RelativePath }
                              drop.{ split.{ Self / } include.{ [ «» «.» ] String } }
                              require.{ not.include.{ Vector<String> «..» } ParentComponent }
                              Ok.concatenate.[ / join.{ Vector<String> / } ] ] }
             Nestable.{ [ either.[ contain.{ Self LockPath } contain.{ LockPath Self } ] ]
                        [ either.[ equal.{ Self / } equal.{ Self LockPath } begin.{ LockPath concatenate.[ Self / ] } ] ]
                        [ any.{ LockPaths nest.{ Self LockPath } } ] } ]
  LockRequest.[ Normalizable.{ [ require.{ not.empty EmptyPaths }
                                 each.{ LockPaths normalize.LockPath }
                                 repeat
                                 [ Some.Err.RepeatedPath
                                   None.Ok.Self.{ LockName FlowId Vector<LockPath> LockReason } ] ] }
                Admitting.{ [ require.{ not.equal.{ Self.LockName Lock.LockName } DuplicateName }
                              find.{ Self.LockPaths meet.{ LockPath Lock.LockPaths } }
                              [ Some.Err.PathOverlap  None.Ok ] ] } ]
  Ledger.[ Lockable.{ [ normalize
                        each.{ Locks admit }
                        Lock
                        Self.{ sort.{ append [ LockName LockId ] } increment.Self.LockId }
                        Locked ]
                      [ find.{ Locks equal.{ LockId Lock.LockId } }
                        Self.{ drop.{ Locks equal.{ LockId Lock.LockId } } Self.LockId }
                        Option<Lock>.[ Some.Released  None.ReleaseRejected.UnknownLockId ] ]
                      [ Locks ] }
           Answering.{ [ Query Response Observation ]
                       []
                       { [ Self.{ [] 1 } ]
                         [ Query.[ Lock.lock  Release.release  Observe.Observed.observe ] ]
                         [ observe.{ Self Locks } ] } } ] ]
```

How to read `lock`, one step at a time:

- `normalize`: the only Normalizable value in scope is the input LockRequest. It is rebound normalized, or a refusal exits as `LockRejected`.
- `each.{ Locks admit }`: each held Lock is admitted beside the request. The first refusal exits (Rule 3).
- `Lock`: no Lock is bound yet, so a Lock is built from scope. LockId comes from the Ledger; the other fields come from the request.
- `Self.{ … }`: Self is rebuilt with the Lock appended and sorted by name, then id, and with the id incremented.
- `Locked`: the reply is filled with that Lock.

The other bodies:

- `admit`: require the names differ, else DuplicateName (this Lock); find a requested path meeting the held paths; Some refuses with PathOverlap built from that LockPath and this Lock; None is Ok (this Lock).
- The `Answering` kind comes from the nexus library and has three capabilities. `start:` builds the first Ledger, `{ [] 1 }`. `answer!` dispatches Query. `announce` is what the runtime broadcasts to open Observe exchanges after any answer that changed Self. That reproduces the Rust `matches!(Locked | Released)`, because rejections exit before Self is rebuilt.

### The current Rust, beside it (excerpt)

The full comparison text is 226 lines: `ordinary.rs` 15–40, `store/transition.rs` 20–111, `store/normalize.rs` 12–133, and `core.rs` 130–158 (orchestrate 9070cbb). The central piece:

```rust
impl Locks for OrchestrateStore {
    fn lock(&mut self, request: LockRequest) -> Result<OrdinaryResponse, StoreError> {
        let request = NormalizedLockRequest::from_request(request)?;
        for holder in self.current_locks()? {
            if request.duplicates_name_of(&holder) {
                return Ok(OrdinaryResponse::LockRejected(LockRejection::DuplicateName(holder)));
            }
            if let Some(path) = request.overlapping_path_of(&holder) {
                return Ok(OrdinaryResponse::LockRejected(LockRejection::PathOverlap(
                    LockOverlap { lock_path: path, lock: holder })));
            }
        }
        // … allocator read with invariant check, checked_add, into_lock, atomic sema commit: 11 more lines
        Ok(OrdinaryResponse::Locked(lock))
    }
}
```

### Count

Comments are stripped. A token is an identifier, a guillemet string, or a single glyph.

| | lines | non-space chars | tokens | word tokens | glyph tokens | keyword-like words |
|---|---|---|---|---|---|---|
| Rust (the 4 excerpts) | 226 | 5657 | 1681 | 678 | 1003 | 251 |
| ethos (above, types + kinds + bodies) | 44 | 1642 | 509 | 200 | 309 | 35 |

The ethos glyphs are `.` 87, `[ ]` 52 pairs, `{ }` 47 pairs, `< >` 7 pairs, bare `/` 6 (content), and `!` 2. The Rust's top glyphs are `( )` 142 pairs, `:` 126, `.` 110, `{ }` 61 pairs, `,` 61, `&` 44 and `;` 41.

**Honest reading of the count.** The ethos is 3.3× smaller in tokens and 3.4× smaller in characters. Keyword-like words fall from 251 to 35. The glyph share stays where it was: 61% for ethos against 60% for Rust. The saving comes from removing words (let, fn, self, return, names, restated types), not glyphs. Every meaning costs a delimiter pair or a `.`.

The scope is not equal either way, and it favours ethos by about 10%. The Rust carries sema-engine plumbing (22 lines: allocator invariant, record keys, retraction), which the ethos hands to the runtime. In the other direction, the ethos adds four rejection variants to the contract, not counted.

## 3. Prior art: what was taken, what was left

- **EDN / Lisp.** Taken: code is data, a body is a datom with holes, and construction is the literal. Left: names as variables, and prefix application everywhere.
- **Forth / Joy.** Taken: a one-deep stack, since a headless match reads the previous step; and point-free steps bound by their yield type. Left: stack shuffling.
- **APL.** Taken: no loop syntax, just collection capabilities with an implicit element. Left: the glyph vocabulary, because we do not shorten words.
- **Haskell.** Taken: equations as arms; record wildcards, as Fill; `Either` with `?`, as Exit; Elm-style effects returned to a runtime, as `announce`. Left: named binders and type-class parameters (ethos has kinds, not generics).
- **Prolog / Datalog.** Taken: clause order as priority; unification by *type*, not variable. Left: backtracking.
- **Pāṇini.** Taken: *anuvṛtti*, where a term stated once carries into the rules after it (Rule 1); 1.4.2, where the later rule prevails in a conflict; *utsarga/apavāda*, where the specific rule comes first and the general rule last (the `require` steps and the unheaded last arm);. Left: the *it*-markers and pratyāhāras, which buy economy by shortening words, which is exactly what the living forbids.

## 4. Where it strains

1. **Everything is read by type.** `Locks` is a value in one place and a variant in another. `Lock` is a Query variant, a type, and a built value. `A.B` is either a projection or a construction. It resolves, but only with the types in view. A reader, human or model, needs the tool to print the *resolved* form. That form would be the natural "point at it and its ethos prints" help for code.
2. **Fill makes data flow invisible.** Suppose a second LockId-typed field is added to Ledger. The step `Lock`, built by Fill, then becomes a refusal because of the tie, which is safe. But a new binding at a nearer level would win silently. This is the audit's row-16 hazard, meaning changing at a distance, generalized to code.
3. **Two values of one type.** These cannot be filled, and within one level they cannot even be named apart. The design pushes toward decomposing into capabilities (`meet` exists so that `nest` sees Self against LockPath) and toward domain aliases (Width, Height), which the audit's item 7 wants anyway. Arithmetic-heavy code will feel this most.
4. **Bodies are positional in an implementation.** The capability name is not repeated, which is consistent with datom structs but hard to scan in a large kind.
5. **Intrinsics are a standard library to design.** There are 18 here, and their names are not all verbs (`each any either empty equal not`). The body position is intrinsic-only: a user capability taking a body needs a kind for "a body yielding X", which ethos cannot yet say.
6. **Exit is `?` with no mark.** Control flow is visible only through the yield types.
7. **Effects.** Self-rebuild plus runtime persistence writes the whole Self, where sema-engine commits one record. Ledger would need to *be* Sema record types for the runtime to diff. Files, time, network and spawning are not designed; they stay Rust behind imported kinds.
8. **Aliases.** Implementing Nestable on `LockPath` implements it on every `String` in Rust. Ethos needs aliases to be nominal (newtypes), which runs into the single-field-struct ban.
9. **Semantic drift from the Rust.** Path errors become typed rejections, not `StoreError`. `increment` overflow at 2^63 traps where Rust answers `LockIdExhausted`. `observe` ignores its one-variant selection, where Rust matches it. Admission scans the ledger kept sorted, which is the same order Rust uses.

**Unresolved:** default bodies in kind declarations; folds with an accumulator; numeric and string-formatting expressions; how a complex kind binds associated types when the names differ (positional, as above, but untested); recursion limits; async; and `Configure`, which this example omits (the fixture has no Configure).

## 5. The manifest root

A manifest is a fourth root. Its sections are *data*: a datom of a `Manifest` type that ethos-zero declares in its own ethos. It is where the version lives, since no ethos file carries one, and it is what resolves import sources, which today are unchecked Rust paths (audit row 1).

```
Manifest
orchestrate-nexus                                             ; name
0.9.0                                                         ; version: the only place one is written
[ ledger.ethos ]                                              ; files, one module each
[ { signal_orchestrate 0.8.1 github:LiGoldragon/signal-orchestrate }
  { nexus 3.2.0 github:LiGoldragon/nexus } ]                  ; dependencies: import source, version, origin
Nexus.Ledger                                                  ; product: its Signal is Answering's Query, bound in the implementation
```

The type behind it is `Manifest.{ Name Version Vector<FilePath> Vector<Dependency> Product }`, with `Dependency.{ SourceName Version Origin }` and `Product.[ Library Nexus.Type Command.Type ]`. A dependency's published ethos is its anatomy, so `signal_orchestrate:[ LockId … ]` is checked against it. Generation emits Cargo.toml and the flake inputs.

## 6. A parse-only prototype, and the verdict

**Parse is already done.** The protos reader accepts the whole example: `lock!{`, `Option<Lock>.[`, `not.equal.{`, bare `/` and `«..»` all parse. So a parse-only prototype proves little. The distinctions that matter (call, construction, value, match, fill) are all made by type, after parsing.

The useful prototype is **resolve-only**:

- (a) Declare the body AST in `ethos-zero.ethos` itself, about 15 types: Implementation, Body, Step, Expression with its 6 variants, Arm, and Resolution.
- (b) Extend conception so that an association entry may be `Kind.{ … }`.
- (c) Write a resolver: scope levels, the direct/carried/nearer rule, Fill, Exit, `!` checking, and an intrinsic table. It should print the fully expanded form of each body, and refuse ties.
- (d) Fixtures: this ledger, plus negative cases for a tie, an unfilled position, `Self.{}` under `.`, and an unknown capability.

That is roughly 800–1200 lines of Rust and no emission. Emission to Rust comes later and is the bulk, the nomos/logos work: step typing, value semantics (clones first), and runtime generation for `Answering`.

**Verdict: worth doing now only in that resolve-only form, and only after the audit's generator bugs are fixed** (duplicate `_Data`, the `Composing`/`Compositional` drift, and the empty Library sections). The reasons:

- The syntax is free: no new glyph, and protos already reads it.
- The real risk is whether the scope and fill rules stay comprehensible, especially to agents, who will write most of it. Only a resolver printing expanded forms over 3–4 real components can test that: this ledger, a CLI, a datom transform, and a Sema-backed store.
- If the expanded forms read as obvious, emission is justified. If agents keep tripping on Fill, fall back to written arguments. That keeps everything else and costs about 15% more tokens.

## Sources

- Skills (loaded through the Skill tool): ethos, datom, protos.
- `/home/li/primary/Vision/ethos.md`, `/home/li/primary/Vision/datom.md`
- `/home/li/primary/flows/e51411/vision/ethos.md` (living, 2026-09-25, both entries)
- `/home/li/primary/flows/752e0f/vision/ethosNextGeneration.md` (nomos/logos)
- `/home/li/primary/flows/e51411/reports/ethos-audit.md`
- `/git/github.com/LiGoldragon/ethos-zero`: 4bf73ca; `fixtures/orchestrate.ethos`, `ethos-zero.ethos`; binary `target/debug/ethos-zero`, run on the example.
- `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/{ordinary.rs,core.rs,store/transition.rs,store/normalize.rs,store/mod.rs}` (9070cbb)
- READMEs of core-logos, core-nomos, rust-logos (type lowering only, no bodies).
- Count: Python tokenizer, comments stripped, regex `«[^»]*»|[A-Za-z0-9_]+|\S`.
