# 658 — A reactive component end to end: minimal schema → the beautiful generated code (operator spec)

The psyche's ask: *show all the code — the minimal schema, and the complete "most beautiful"
Rust emitted from it — as the implementation target operators build toward.* No aliases: the
schema holds the convenience (declare once, bind per component); the generated Rust is the
explicit, fully-expanded "assembly" form. This report is the spec; a test implementation aims
at it next. Builds on the verified expansion prototype (`656`), the concrete-not-generic
principle (`657`), the explicit-kind principle (`3742`), and `zjmc` (declare once, bind per
component).

## 1. The data-node model — kind is on the form (Spirit `3742`)

Every distinct *data node* is marked by its delimiter; you never resolve a name to learn what
kind of node you're looking at. The base delimiters carry the non-generic kinds; the two
reserved pipe delimiters (`j9du`) carry generics:

| Schema form | Data node | Generated Rust |
|---|---|---|
| `Name [ (A) (B) ]` | enum declaration | `pub enum Name { A(A), B(B) }` |
| `Name { F G }` | struct declaration | `pub struct Name { pub f: F, pub g: G }` |
| `Name Type` | newtype declaration | `pub struct Name(Type)` + accessors + `From` |
| `Type` / `(Vector T)` | type reference / application | `Type` / `Vec<T>` |
| **`Name (\| [P…] <body> \|)`** | **generic declaration** | `pub enum/struct Name<P…> { … }` *(emitted only where genuinely polymorphic; for a component root it is **expanded**, §3)* |
| **`{\| Head Arg… \|}`** *(candidate)* | **generic application / use** | the bound type |

The **declare** delimiter `(| … |)` wraps `[params]` then a **body whose own delimiter says
enum (`[…]`) or struct (`{…}`)** — the same enum/struct distinction used everywhere, now
*inside* the generic wrapper. That is the "outer delimiter = generic declaration, inner
delimiter = enum/struct" you described.

**Two open forks to settle before operators start** (both about the *use* row and the second
pipe delimiter):

- **Does generic *use* need its own `{| … |}` delimiter, or is the existing application
  `(Head Arg…)` enough?** Per `3742` you settled earlier that *use-site name resolution is
  legitimate, not guessing* — `(Work …)` resolving against an explicitly-`(| |)`-declared
  `Work` is exactly how `(Vector T)` is known. By that principle the **use form needs no new
  delimiter** (`(Head Arg…)` suffices), which keeps `{| … |}` free. The alternative — a
  distinct `{| Head Arg… |}` use form — is *more* explicit (the application self-identifies as
  *generic* without resolving the head) but consumes the second delimiter. **My lean: keep
  `(Head Arg…)` for use** (consistent with the settled principle), unless you want maximal
  explicitness.
- **Therefore `{| … |}`'s owner.** If use stays `(Head Arg…)`, `{| … |}` is **free for
  traits/impls** (the earlier intent). If use takes `{| … |}`, **both** pipe delimiters are
  generics and **traits/impls need a different mechanism** (a reserved keyword head like
  `(Trait …)` / `(Impl …)`, since the pipe space is exhausted). This is the consequence to
  decide.

## 2. No aliases — the generated Rust is the explicit expansion

The genericity is a *schema-authoring* convenience. It does **not** persist as a generic type
in a component's output (`657`): a component root is **expanded** to a concrete enum, not
left as `type Input = Work<…>`. The generic `Work`/`Action` exist as real types in exactly
one place — hand-written polymorphic runtime code in `triad-runtime` (the runner). Everything
a component emits is concrete.

## 3. The complete worked example

### 3a. The universal frame — declared once, shared by every component

```
;; reaction.schema
Work (| [Event WriteDone ReadDone EffectDone]
  [(SignalArrived Event) (SemaWriteCompleted WriteDone) (SemaReadCompleted ReadDone) (EffectCompleted EffectDone)] |)

Action (| [Reply Write Read Effect Continuation]
  [(ReplyToSignal Reply) (CommandSemaWrite Write) (CommandSemaRead Read) (CommandEffect Effect) (Continue Continuation)] |)
```

### 3b. A component's *entire* schema (spirit's nexus, minimal slice)

```
{ Work reaction:reaction:Work
  Action reaction:reaction:Action }

;; the two roots: bind the frame (shown in the application-use form; see §1 fork)
Input  (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)
Output (Action SignalOutput SemaWriteSet SemaReadInput EffectCommand (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome))

;; payload declarations — one of each kind
SemaWriteSet [(Record) (Remove)]          ;; enum of single-payload legs
Record       Entry                         ;; newtype
StashRequest { Records DatabaseMarker }    ;; struct (field name = type, ov30)
```

That is the whole authored surface for the reaction core. No leg is re-spelled; the frame
shape lives once in `reaction.schema`.

### 3c. The complete *beautiful* generated Rust

Every type, fully expanded and concrete. The shared derive stack on each type is
`#[cfg_attr(feature = "nota-text", derive(NotaDecode, NotaEncode))]` +
`#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]`
(elided below for brevity, but on every item).

```rust
// === roots: expanded from the frame application (binder→argument substitution) ===
pub enum Input {
    SignalArrived(SignalInput),
    SemaWriteCompleted(SemaWriteOutput),
    SemaReadCompleted(SemaReadOutput),
    EffectCompleted(EffectOutcome),
}
impl Input {
    pub fn signal_arrived(payload: SignalInput) -> Self { Self::SignalArrived(payload) }
    pub fn sema_write_completed(payload: SemaWriteOutput) -> Self { Self::SemaWriteCompleted(payload) }
    pub fn sema_read_completed(payload: SemaReadOutput) -> Self { Self::SemaReadCompleted(payload) }
    pub fn effect_completed(payload: EffectOutcome) -> Self { Self::EffectCompleted(payload) }
}
impl From<SignalInput> for Input { fn from(p: SignalInput) -> Self { Self::SignalArrived(p) } }
// …one From per distinct-payload leg…

pub enum Output {
    ReplyToSignal(SignalOutput),
    CommandSemaWrite(SemaWriteSet),
    CommandSemaRead(SemaReadInput),
    CommandEffect(EffectCommand),
    Continue(Input),                  // the (Work …) Continuation arg → the sibling expanded root
}
impl Output { /* reply_to_signal/command_sema_write/command_sema_read/command_effect/r#continue */ }
impl From<SignalOutput> for Output { /* … */ }   // …one per distinct-payload leg, incl. From<Input> for Output

// === enum of single-payload legs ===
pub enum SemaWriteSet { Record(Record), Remove(Remove) }
impl SemaWriteSet {
    pub fn record(payload: Record) -> Self { Self::Record(payload) }
    pub fn remove(payload: Remove) -> Self { Self::Remove(payload) }
}
impl From<Record> for SemaWriteSet { /* … */ }
impl From<Remove> for SemaWriteSet { /* … */ }

// === newtype ===
pub struct Record(Entry);
impl Record {
    pub fn new(payload: Entry) -> Self { Self(payload) }
    pub fn payload(&self) -> &Entry { &self.0 }
    pub fn into_payload(self) -> Entry { self.0 }
}
impl From<Entry> for Record { fn from(payload: Entry) -> Self { Self::new(payload) } }

// === struct (field name = snake_case of the type, ov30) ===
pub struct StashRequest { pub records: Records, pub database_marker: DatabaseMarker }
impl StashRequest {
    pub fn new(records: Records, database_marker: DatabaseMarker) -> Self { Self { records, database_marker } }
    pub fn records(&self) -> &Records { &self.records }
    pub fn database_marker(&self) -> &DatabaseMarker { &self.database_marker }
}
```

### 3d. What "beautiful" fixes versus today

Today the emitter double-wraps the frame legs: it emits a **per-leg newtype**
`pub struct SignalArrived(SignalInput);` *and then* `NexusWork::SignalArrived(SignalArrived)`
— two layers, and a hand-spelled `NexusWork`/`NexusAction` re-authored in the schema. The
beautiful version **flattens** to `Input::SignalArrived(SignalInput)` directly (one layer, the
real payload), and the enum is **expanded from the frame**, not re-authored. Same wire bytes
(the wrapper was incidental); less code; the schema shrinks to the binding lines.

## 4. The code generation (what operators implement)

The expansion engine is **already prototyped and tested green** (`656`,
`schema-next`/`schema-rust-next` `reaction-expand` worktrees): an applied root lowers, by
positional binder→argument substitution, into a concrete `RustEnum` that flows through the
existing concrete-enum emitters (constructors / `From` / accessors / wire derives), because an
expanded enum has empty parameters so the parameterized-decl suppression guards don't fire.
The remaining surface work:

1. **`(| … |)` declare arm** — handle a declaration *value* that is a `(| [params] body |)`
   pipe-paren block (the value-lowering path in `source.rs` namespace-entry handling — *not*
   the head; the name is the namespace key). `child[0]` = the `[params]` vector → the
   declaration's parameters; `child[1]` = the body, whose delimiter (`[…]`/`{…}`) selects
   enum/struct. Params and body live together inside the `(| |)` so the binders scope the body
   structurally (`655`). Lowers to the same parameterized `Declaration` the bare-paren
   `(Name P…)` head form produces, so everything downstream (expansion) is unchanged.
2. **Generic *use* form** — per the §1 fork: either keep `(Head Arg…)` (no work) or add the
   `{| … |}` use delimiter + lower it to a `TypeReference::Application`.
3. **Expansion at applied-root lowering** — land the prototype (`656`): promote `FrameExpansion`
   to a library method, carry the frame's params+variants across the import boundary
   (`ResolvedImport`), expand applied roots into concrete `root_enums`.
4. **Flatten the per-leg newtype layer** — bind legs to the real payload directly.

## 5. Decisions needed before/at implementation

- **The two §1 forks:** does generic-use take `{| … |}` (then traits need a keyword head), or
  stay `(Head Arg…)` (then `{| … |}` is traits)? My lean: use stays `(Head Arg…)`, `{| … |}`
  is traits — consistent with the settled "use-site name resolution is fine" principle.
- **Confirm the newtype flattening** (§3d) as the intended beautiful form.
- The Spirit-record cleanup for the pipe-delimiter assignments remains blocked on the daemon
  v9/v10 store fix (per `655`); the design here is what those records will encode once the
  store is fixed.
