# Ethos implementations — Fable's independent design

Psyche High 38de5b, 2026-09-25. Written without sight of the parallel design. The living's words this design answers: "make the syntax perfect and super minimal (so that there's no repetition, nothing out of place, and no noise), it's all just pure description of a program, as compact as it can be, basically, and not in word size. We don't shorten words. The compactness is in the very low noise amount." (flows/e51411/vision/ethos.md, last entry.)

## 1. Where implementations live

Ethos already has the place. An association today says that a type bears a kind: `SinkError.[ Fillable ]`, a compile-time assertion whose body is hand-written. The design adds no section and no root: **an association that carries bodies is an implementation.** `Store.[ Lockable.{ … } ]` is Store bearing Lockable with the bodies of Lockable's capabilities inside the braces, one body per capability, in the kind's declared order. An association without bodies stays what it is. Every function is a capability of a kind, so there are no free functions: a function with no receiver is a `:` capability, and a type bears it.

## 2. The grammar, in one family of rules

Ethos declares with `Name.Type`, `Name.{ … }`, `Name.[ … ]`: a name, a dot, what it stands for. Bodies use the same shape and nothing else.

1. **Binding.** `name.expression` — the name stands for the expression. A lowercase head is a binding; an uppercase head is a type or variant. This one rule is also the parameter list of a capability body and the parameter of a closure: `push.[ input  body ]` names the input `input`; `find.[ held.held.lock_name.equals.[ name ] ]` passes a closure whose parameter is `held`.
2. **Construction.** `Head.{ … }`, `Head.[ … ]`, `Head.expression`, or a bare variant — exactly the datom of the value being built. `Lock.{ self.lock_id request.lock_name }` builds a Lock; `Err.DuplicateName.held` builds a Result.
3. **Call.** `expression.capability.[ arguments ]` — the receiver, its capability, the arguments in a bracket, positional, empty when none. `self.lock_vector.push.[ lock ]`. A capability's receiver mark (`.` `!` `:`) is in the kind; the body does not repeat it.
4. **Match.** `expression.[ arms ]` — a bracket after an expression of enum type is a match. An arm is `Variant.binding.expression` when the variant carries data, `Variant.expression` when it does not. Every variant appears once; the checker refuses a missing arm.
5. **Sequence.** `[ steps ]` — steps in order, each a binding, the last one bare: it is the yield.

Nothing else: no keywords, no operators, no parentheses (reserved to Meaning), no field names, no type annotations in bodies — every position's type is known from the kind's signature and the declared types, so the reader walks the type as datom does. What a bracket means — vector, arguments, arms, steps — is said by the position it sits in, exactly the datom rule.

Intrinsic capabilities (`equals`, `any`, `find`, `push`, `remove`, `increment`, `clone`, `prefix_of`, `or`) are capabilities of kinds the intrinsics bear, declared once in a `protos` library and imported like any kind; nothing is built into the body grammar.

## 3. The manifest

An ethos file carries no version. The manifest is a datom in a Manifest type, one per repository:

```
Library
[]
[ Manifest.{ Name Version Vector<File> Vector<Dependency> }
  Name.String  Version.String  File.String  Dependency.{ Name Version } ]
[]
[]
```
```
{ orchestrate 3.1.0 [ signal.ethos library.ethos ] [ { protos 2.0.0 } { std 1.0.0 } ] }
```

Generation reads the manifest, resolves each dependency's kinds and types, and emits one Rust crate: the types as today, the kinds as traits, and each implementation as an `impl Kind for Type` whose bodies are generated. `ethos-zero 'Generate.{ /abs/manifest.ethos /abs/out }'`.

## 4. Worked example: Orchestrate Lock, Release, Observe

```
Library
[ protos:[ Equatable Searchable Growable Countable ] ]        ; imports: kinds the intrinsics bear
[ LockId.Integer  LockName.String  LockPath.String  FlowId.String  Reason.String
  LockRequest.{ LockName FlowId Vector<LockPath> Reason }
  Lock.{ LockId LockName FlowId Vector<LockPath> Reason }
  LockRejection.[ DuplicateName.Lock  PathOverlap.{ Lock LockRequest } ]
  ReleaseRejection.[ UnknownLock.LockId ]
  Store.{ LockId Vector<Lock> } ]                              ; next id, held locks
[ Lockable.[ lock!{ [ LockRequest ] [ Result<Lock LockRejection> ] }
             release!{ [ LockId ] [ Result<Lock ReleaseRejection> ] }
             observe.[ Vector<Lock> ] ]
  Overlapping.[ overlaps.{ [ Vector<LockPath> ] [ Boolean ] } ] ]
[ Lock.[ Overlapping.{
    overlaps.[ lock_path_vector
               self.lock_path_vector.any.[ mine  lock_path_vector.any.[ theirs  mine.prefix_of.[ theirs ].or.[ theirs.prefix_of.[ mine ] ] ] ] ] } ]
  Store.[ Lockable.{
    lock.[ request
           self.lock_vector.find.[ held  held.lock_name.equals.[ request.lock_name ] ]
             .[ Some.held.Err.DuplicateName.held
                None.self.lock_vector.find.[ held  held.overlaps.[ request.lock_path_vector ] ]
                  .[ Some.held.Err.PathOverlap.{ held request }
                     None.[ lock.Lock.{ self.lock_id request.lock_name request.flow_id request.lock_path_vector request.reason }
                            self.lock_id.increment.[]
                            self.lock_vector.push.[ lock ]
                            Ok.lock ] ] ] ]
    release.[ lock_id
              self.lock_vector.remove.[ held  held.lock_id.equals.[ lock_id ] ]
                .[ Some.lock.Ok.lock
                   None.Err.UnknownLock.lock_id ] ]
    observe.self.lock_vector.clone.[] } ] ]
```

Read `lock`: the parameter is `request`; find a held lock of the same name — if Some, refuse DuplicateName with it; if None, find a held lock whose paths overlap the request's — if Some, refuse PathOverlap with both; if None, a sequence: bind `lock` to the new Lock, increment the next id, push, yield Ok.lock.

The Rust ethos-zero would emit beside it:

```rust
impl Overlapping for Lock {
    fn overlaps(&self, lock_path_vector: std::vec::Vec<LockPath>) -> bool {
        self.lock_path_vector.iter().any(|mine|
            lock_path_vector.iter().any(|theirs| mine.prefix_of(theirs) || theirs.prefix_of(mine)))
    }
}
impl Lockable for Store {
    fn lock(&mut self, request: LockRequest) -> std::result::Result<Lock, LockRejection> {
        match self.lock_vector.iter().find(|held| held.lock_name == request.lock_name) {
            Some(held) => Err(LockRejection::DuplicateName(held.clone())),
            None => match self.lock_vector.iter().find(|held| held.overlaps(request.lock_path_vector.clone())) {
                Some(held) => Err(LockRejection::PathOverlap(PathOverlap_Data { lock: held.clone(), lock_request: request })),
                None => {
                    let lock = Lock { lock_id: self.lock_id, lock_name: request.lock_name, flow_id: request.flow_id,
                                      lock_path_vector: request.lock_path_vector, reason: request.reason };
                    self.lock_id += 1;
                    self.lock_vector.push(lock.clone());
                    Ok(lock)
                }
            },
        }
    }
    fn release(&mut self, lock_id: LockId) -> std::result::Result<Lock, ReleaseRejection> {
        match self.lock_vector.iter().position(|held| held.lock_id == lock_id).map(|i| self.lock_vector.remove(i)) {
            Some(lock) => Ok(lock),
            None => Err(ReleaseRejection::UnknownLock(lock_id)),
        }
    }
    fn observe(&self) -> std::vec::Vec<Lock> { self.lock_vector.clone() }
}
```

The Signal side is unchanged: `Lock.LockRequest`, `Release.LockId`, `Observe.ObserveSelection` queries route to these capabilities; the Nexus handler is `store.lock.[ request ].[ Ok.lock.Locked.lock  Err.rejection.LockRejected.rejection ]`, itself a body.

## 5. Where it strains

1. **Ownership is invisible.** Ethos describes a program without borrowing, moving or cloning; the generator must choose. The rule that keeps the description pure: values are moved when consumed once, cloned when a later step still names them, borrowed for `.` receivers. The Rust above shows the `.clone()` calls the rule inserts. This is the real cost, and it is the generator's, not the author's.
2. **Bracket by position.** One bracket is a vector, call arguments, match arms or a sequence, said only by the type of the position. A reader with the types reads fluently; a reader without them cannot. This is already datom's bargain; bodies extend it to control flow.
3. **No early return.** Refusals nest as match arms. A `?`-shaped rule (yield the Err arm at once) would flatten `lock` to one level, at the price of a sixth rule. Not added here; the nesting is honest and the checker enforces exhaustive arms.
4. **Closures take one parameter.** `held  body` is one name. A two-parameter closure is a struct of names, `{ a b }  body`, which is the same rule read as a struct; no case needs it in Orchestrate.
5. **Intrinsic kinds are a library to write.** Every `equals`, `find`, `push` is a declared capability of a kind an intrinsic bears; the `protos` library that declares them is a prerequisite and the place where naming discipline is won or lost.

Not a strain: iteration, IO and time. They are capabilities of kinds borne by the runtime's types, declared like everything else; bodies call them.

## 6. Worth doing now?

Yes, for one bounded slice, and not for everything. The slice: the pure store transitions of the Nexuses — Orchestrate's locks, Flow's registry states, Message's ledger — where the types already carry most of the meaning and the bodies are match-and-construct. There the description is shorter than the Rust and every line is meaning. Not now: the harness adapters, sockets, files and processes, where the intrinsic-kind library would have to be large before the first body compiles. Prerequisites in flight tonight: unique derived names and source-located errors in ethos-zero (fixes 5 and 7) — an error in a body needs a line and column. Sequence: land those; write the `protos` kinds for Vector, Option, Result, Integer, String; generate Orchestrate's store from this file and diff it against the hand-written crate; only then decide the `?` rule.

## Sources

- flows/e51411/vision/ethos.md — the living, 2026-09-25, last entry (quoted above).
- The ethos skill: roots, sections, kinds, receivers, associations; the datom skill: positional reading, a head is a variant.
- Vision/flowNexus.md, Vision/nexus.md; signal-orchestrate's contract for the Lock/Release/Observe shapes.
- Agent coinages in this document: "an association that carries bodies is an implementation"; the five body rules; Manifest as a Library type; the ownership rule for generation.
