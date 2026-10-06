<!-- to-the-living:start -->
Presentation.{ «Ethos, distilled», second edition }

## What changed
Your comments on the first edition (2026-10-06, 15:4x to 15:58) are answered here.
Proposals 1 and 4 are landed. Proposals 2 and 3 now show the bad form, then the good. Proposals 5 and 6 are rewritten on your words. Proposal 7 is called a new type. Proposal 8 now carries your line breaking.
Every ethos block below is a whole root with comments. A good example obeys every proposal in this book. A bad example breaks only the rule it shows.
Accept a proposal whole or refuse it. A ruling is a choice for you to make.
Landed in Vision/ethos.md: 1, "Ethos is central" (What Ethos is), and 4, "Terseness is in the low amount of noise, never in shortened words" (Non-repetition). Their sources are appended to Vision/sources/ethos.md.

## Proposals

### 2. Non-repetition: a type is never wrapped twice
Proposed, appended to Non-repetition:
> A type is never wrapped in a second new type: where a thing is a FlowId, it is written FlowId. No type is invented to say what a variant carries.

The real case is the Flow Library root in «Flow spawning». A job is a flow, so `Job.FlowId` wraps the new type FlowId in a second new type. Only Originator changes; Role's Job carries nothing, so it wraps nothing.

Bad:
```
Library                                  ; Flow's shared types, as «Flow spawning» wrote them
[]                                       ; imports: none
[ FlowId.Integer                         ; types: FlowId, used in Flow and in Originator
  Voice.{ Aspect.[ Psyche Mind Field ]   ;   Voice, used in Role and in Originator
          Layer.[ Primary Secondary
                  Tertiary Quaternary ] }
  Flow.{ FlowId                          ;   a flow: its id and what it runs as
         Role.[ Voice Job ] }            ;   a voice, or a job, which carries nothing
  Originator.[ Voice                     ;   who sent a message: a voice,
               Job.FlowId ] ]            ;   or Job, a second new type around FlowId
[]                                       ; kinds: none
[]                                       ; associations: none
```
Good:
```
Library                                  ; Flow's shared types
[]                                       ; imports: none
[ FlowId.Integer                         ; types: FlowId, used in Flow and in Originator
  Voice.{ Aspect.[ Psyche Mind Field ]   ;   Voice, used in Role and in Originator
          Layer.[ Primary Secondary
                  Tertiary Quaternary ] }
  Flow.{ FlowId                          ;   a flow: its id and what it runs as
         Role.[ Voice Job ] }            ;   a voice, or a job, which carries nothing
  Originator.[ Voice                     ;   who sent a message: a voice,
               FlowId ] ]                ;   or a flow, written FlowId; the variant carries FlowId itself
[]                                       ; kinds: none
[]                                       ; associations: none
```
Your words:
> If a job is a flow ID, then why are we even using the word "job"? Just use "flow ID". Why are you going to wrap a new type with another new type? Don't double-wrap types. That's silly.
-- d4ae97 ethos, 2026-10-06
> I don't want this repetition of types, like where we invent another type to say what's inside a variant.
-- 91ea9f ethos, 2026-10-02

### 3. Non-repetition: an enum whose every variant carries the same type is a struct
Proposed, appended to Non-repetition:
> An enum whose every variant carries the same type repeats that type in each variant; it is written as a struct of the two.

Bad:
```
Library                                  ; the shared types of Flow
[]                                       ; imports: none
[ Voice.[ Psyche.Layer                   ; types: Voice, an enum whose every variant
          Mind.Layer                     ;   carries Layer, so Layer is written
          Field.Layer ]                  ;   three times
  Layer.[ Primary Secondary
          Tertiary Quaternary ] ]
[]                                       ; kinds: none
[]                                       ; associations: none
```
Good:
```
Library                                     ; the shared types of Flow
[]                                          ; imports: none
[ Voice.{ Aspect.[ Psyche Mind Field ]      ; types: Voice, a struct of its aspect and its layer;
          Layer.[ Primary Secondary         ;   Layer is written once, inline,
                  Tertiary Quaternary ] } ] ;   since it is used only here
[]                                          ; kinds: none
[]                                          ; associations: none
```
Your words:
> I think we're going to abandon this idea that we wouldn't have an enum where each data-carrying variant carries the same type, because it creates this repetition that you can see now: `[psyche].layer`, `[mind].layer`, `.layer` is being repeated. I think rather the voice is a struct that contains the aspect and the layer
-- aa887c ethos and bad807 ethos, 2026-10-04
> This is good but you should also show the bad example and then the good example so that you make your point clear in code.
-- d4ae97 books, 2026-10-06

### 5. New heading after Non-repetition: Everything is a type
Proposed:
> ## Everything is a type
> There is no key-value in Ethos; everything is a type. A struct's positions are types, and no name is written beside a value. A position's type is declared inline, in the position, unless it is used again; its name is never repeated only to declare it apart.

Bad, the first edition's example:
```
Library                                  ; the shared types of a lock service
[]                                       ; imports: none
[ LockId.Integer                         ; types: LockId and LockName declared apart,
  LockName.String                        ;   then their names repeated in Lock,
  Lock.{ LockId LockName } ]             ;   though Lock is their only use
[]                                       ; kinds: none
[]                                       ; associations: none
```
Good:
```
Library                                  ; the shared types of a lock service
[]                                       ; imports: none
[ Lock.{ LockId.Integer                  ; types: Lock, each position a type declared inline:
         LockName.String } ]             ;   a new type of Integer, a new type of String
[]                                       ; kinds: none
[]                                       ; associations: none
```
Your words:
> We don't have key-value in Ethos anymore. Everything is a type.
-- 91ea9f ethos, 2026-10-02
> Here there would only be one entry where each field of the struct would have the definition of these types inline, which would avoid repetition, right? That's the whole point: the terseness, unless the type is reused somewhere else. ... I don't want to have to repeat the type names just so that they're declared independently. I think that's silly. And it creates a whole bunch of repetition, which creates a whole bunch of cognitive load.
-- d4ae97 ethos, 2026-10-06

### 6. Inline types: inline declaration is mandatory up to a depth
Now:
> A type may be declared where it is used.

Proposed, in its place:
> A type used within another type is declared inline, where it is used; this is mandatory. A type is declared at the top only when it is used again, or when it is too deep to be declared inline. Ethos supports a type declared inline being used elsewhere.

Open: the algorithm that decides inline or top, and the depth that is too deep. You asked for one; it is a design question for the new Fable, whose brief makes ethos central. This book does not invent it.

Bad:
```
Library                                  ; the shared types of Flow
[]                                       ; imports: none
[ FlowId.Integer                         ; types: FlowId, used in Flow and in Report
  State.[ Running Ended ]                ;   State, used only in Flow, declared apart
  Event.[ Started Stopped ]              ;   Event, used only in Report, declared apart
  Flow.{ FlowId State }                  ;   so both names are written twice
  Report.{ FlowId Event } ]
[]                                       ; kinds: none
[]                                       ; associations: none
```
Good:
```
Library                                  ; the shared types of Flow
[]                                       ; imports: none
[ FlowId.Integer                         ; types: FlowId, used in Flow and in Report, at the top
  Flow.{ FlowId                          ;   a flow: its id and its state;
         State.[ Running Ended ] }       ;   State is used only here, so it is inline
  Report.{ FlowId                        ;   a report: which flow, and what happened;
           Event.[ Started Stopped ] } ] ;   Event is used only here, so it is inline
[]                                       ; kinds: none
[]                                       ; associations: none
```
Your words:
> I would rather the types be defined inline up until a decent level of recursion.
-- d4ae97 ethos, 2026-10-06
> even if a type is declared inline in one place, it can still be declared at the top. We don't have to and in fact just because of the extra repetition that creates, I would want to make the inline declaration mandatory unless that particular type is so deep that it itself requires too much recursion to be declared inline. We have to explain some kind of algorithm to determine whether or not a type should be declared inline.
-- d4ae97 ethos, 2026-10-06
> We would have a maximum depth after which we would require the types that are at, I don't know, maybe the third depth to be imported from an external library.
-- 91ea9f ethos, 2026-10-02

### 7. New heading after What a declaration turns into: New type
Proposed:
> ## New type
> A new type is written as its name, a dot, and the type it holds: `LockName.String`. There is no single-field struct.

Bad:
```
Library                                  ; the shared types of a lock service
[]                                       ; imports: none
[ LockName.{ String } ]                  ; types: a single-field struct
[]                                       ; kinds: none
[]                                       ; associations: none
```
Good:
```
Library                                  ; the shared types of a lock service
[]                                       ; imports: none
[ LockName.String ]                      ; types: LockName, a new type of String
[]                                       ; kinds: none
[]                                       ; associations: none
```
Your words:
> It's a new type, which is explained syntactically elsewhere. We're not going to talk like little kindergarten. We're engineers here. We're going to call things what they are and that's a new type.
-- d4ae97 ethos, 2026-10-06
What a new type turns into in Rust is ruling 2.

### 8. New heading after Spacing: Vertical
Proposed:
> ## Vertical
> Ethos expands vertically wherever there is a next layer: the structure opens on its line and its elements hang beneath the first, aligned, and going right is free. The closing delimiter ends the last element's line; it never takes a line of its own. If a recursive block would expand too far right, its first element goes on a new line, indented right, for more space to the right. A vector may hold more than one item per line, up to a width; past it, it wraps and lines up with the first item.

Open: the full algorithm for where the new lines go, and the width, are left to the design.

Bad, the first edition's example: Aspect and Layer declared apart, so Voice stayed short and on Launch's line:
```
Signal                                   ; what Flow says
[]                                       ; imports: none
[ Launch.{ Voice.{ Aspect Layer }        ; queries: Voice's types declared apart
           Brief.String } ]
[ Launched Refused ]                     ; responses
[ Aspect.[ Psyche Mind Field ]           ; types: each used only in Launch
  Layer.[ Primary Secondary Tertiary Quaternary ] ]
```
Good:
```
Signal                                      ; what Flow says
[]                                          ; imports: none
[ Launch.{                                  ; queries: Launch would run far right,
    Voice.{ Aspect.[ Psyche Mind Field ]    ;   so Voice opens a new line, indented;
            Layer.[ Primary Secondary       ;   Aspect and Layer inline; Layer's variants
                    Tertiary Quaternary ] } ;   wrap, aligned with the first
    Brief.String } ]                        ;   Brief, a new type of String
[ Launched Refused ]                        ; responses
[]                                          ; types: none
```
Your words:
> If the recursive block is going to expand to the right too much, then instead of, like in the example, you have `launch {` and then you put `voice` on the same line, instead of that I would put `voice` on a new line, indented right, so that you get more space to the right that way. ... `aspect` should have been declared in line ... `layer` can have its variance wrap around.
> Like when we have a vector, we can do this: we can have more than one item per line but at a certain length it wraps around and lines up with the first item and then continues like that. We can have a certain number per line but only up to a certain width.
-- d4ae97 ethos, 2026-10-06

### 9. New heading after Declaration: File: Written whole, and commented
Proposed:
> ## Written whole, and commented
> Ethos is always written whole: inside its root, every section in place, so what each type is for is known. Types lifted out of their root are not ethos. Ethos carries many comments, so whoever reads it sees what the machine reads.

```
Library                                  ; the root: what follows is a library
[]                                       ; imports: none
[ FlowId.Integer ]                       ; types: a flow's id, a new type of Integer
[]                                       ; kinds: none
[]                                       ; associations: none
```
Your words:
> You can't just throw uncontextualized ethos code around. It doesn't mean anything.
-- d4ae97 books, 2026-10-05
> I actually would like all of the Ethos code to get way more comments so that I can see what the machine is seeing.
-- edf227 ethosComments, 2026-10-03

### 10. Declaration: File: the edit is the migration
Now:
> An ethos file carries no version; datom has no versions. What is versioned is versioned in a manifest of some kind, never in the file.

Proposed, appended:
> A change to an ethos file is an operation, and that same operation is the migration that carries the stored data into its new format.

Your words:
> the change in ethos is going to be operational. That operation is going to be the very edit, the very update operation that this particular data type needs to change into its new memory format.
-- 91ea9f ethos, 2026-10-02

### 11. New heading after Associations: The memory kind
Proposed:
> ## The memory kind
> Every record type of Memory bears a kind whose change is standard: it succeeds or it fails.

```
Memory                                   ; what Flow remembers
[ flow:FlowId ]                          ; imports from the Library
[ Flow.{ FlowId                          ; record types: Flow bears the memory kind,
         State.[ Running Ended ] } ]     ;   so a change to it either succeeds or fails
```
Your words:
> It's going to be a kind that's going to have a standard successful or unsuccessful change implemented on these particular data types.
-- 91ea9f ethos, 2026-10-02
Whether Memory is a root of its own is ruling 1; the upgrade between versions is ruling 4.

### 12. Kind: the word names nothing else
Now:
> Kind is the word for the bearer of capabilities

Proposed, appended to Kind:
> The word is kept for that; no type is named Kind.

Your words:
> I don't like `kind` because it collides with our use for `kind`, which is more basic.
-- 5578cc ethos, 2026-10-03

## Rulings
Unchanged from the first edition, except where noted.

### 1. Roots: Sema or Memory
Vision/ethos.md, Roots: "Library, Signal, Sema. ... Sema's are record types, the rest to be decided."
One side: "When we create the SEMA Ethos type for the root type ... we're going to be defining database record types." (564f55 sema, 2026-09-09)
Other side: "Yeah the memory is good. That's what it is I guess: signal, operation, and memory." (91ea9f ethos, 2026-10-02), landed in Vision/nexus.md on 2026-10-04.

(a) Memory is the root once named Sema. Roots becomes:
> Library, Signal, Operation, Memory. No version in a file. Signal declares what a Nexus says, its sections queries and responses; Operation what it does, one operation type for every effect; Memory what it remembers, its record types; Library what they share.

(b) Sema stays the root of record types; Memory names the Nexus's part only. Roots becomes:
> Library, Signal, Operation, Sema. No version in a file. Signal declares what a Nexus says, its sections queries and responses; Operation what it does, one operation type for every effect; Sema what it remembers, its record types; Library what they share.

Under (a), Vision/sema.md's "its root, Sema" needs a proposal of its own later.

### 2. What a new type turns into in Rust
Vision/ethos.md, landed 2026-09-09: "An alias bears them through the type it names: an alias is not a new type and cannot carry a derive."
Your words: "This should be a new type and not a struct with just a single element in it." (8e9e77, 2026-09-08)
Noted: on 2026-10-06 you called `LockName.String` a new type (proposal 7). That reads as (b); the choice stays yours.

(a) `LockName.String` stays an alias:
```rust
pub type LockName = String;
```
(b) `LockName.String` is a Rust newtype, bearing both kinds:
```rust
#[derive(Datomizable, Compositional)]
pub struct LockName(String);
```

### 3. A capability's inputs: types, or only kinds and Self
Vision/ethos.md, Kind syntax, has push take a String. Reduced here so the block obeys proposal 6:
```
Library                                  ; a sink
[]                                       ; imports: none
[]                                       ; types: none
[ Fillable.[ push!{ [ String ]           ; kinds: push takes a String, a concrete type,
                    [ Integer ] } ] ]    ;   and yields an Integer
[]                                       ; associations: none
```
Your words: "I don't understand how there's a specific type as an input for a kind. ... It should only be another kind because a type is too specific. ... The voice is launchable, right, so it uses self." (91ea9f ethos, 2026-10-02)
You asked for real Rust checks with this; none is reported yet.
(a) A capability speaks only in Self, the kind's own parameters and other kinds.
(b) A concrete type may stand as an input, as now.
(c) Wait for the Rust checks.

### 4. A memory format's upgrade: from, or both ways
Your words: "I guess an upgrade from makes more sense because you're trying to upgrade the past but it could be a symmetrical operation." (91ea9f ethos, 2026-10-02)
(a) Each version carries the upgrade from the previous format.
(b) Each version carries an upgrade both ways.
(c) Not yet.

### 5. The Types root
Your words: "the types plural would be a vector of public types" (b05237, 2026-09-19); "If you're only listing types then you can use the `types` type." (7328f4, 2026-09-30)
Vision/ethos.md: "Every root's first section is its imports; its own sections follow."
(a) Types opens with imports, like every root:
```
Types                                    ; only types are listed
[]                                       ; imports: none
[ LockId.Integer                         ; types: two new types
  LockName.String ]
```
(b) Types has one section, the vector of types, and no imports:
```
Types                                    ; only types are listed
[ LockId.Integer                         ; types: two new types
  LockName.String ]
```
## Not proposed
Unchanged: book orders (situational); "ethos isn't about strings" (ruled bad vision); nomos and logos; Ethos Delta; an ethos core library and word ids (waiting on Fable); simple and extended forms, identifiers (Signal and Datom topics); an escape delimiter for ethos inside datom (your open question).

## Discarded on landing
- Roots: "the rest to be decided" (ruling 1 replaces it).
- Inline types: "may" (proposal 6 replaces it).
<!-- to-the-living:end -->
