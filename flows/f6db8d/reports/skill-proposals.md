# Skill proposals — the authored Curriculum skills

Flow f6db8d, skill-review subflow. Written under the living's standing order
that skill edits need the living's approval: **nothing here was applied**. No
skill, manifest, or generated tree was edited; no commit, no lock, no build.

Authored sources reviewed: `/git/github.com/LiGoldragon/Curriculum/skills/*.md`
(46 files), `roles.datom`, and the repository's own `AGENTS.md`,
`ARCHITECTURE.md`. Generated trees (`.claude/`, `.agents/`, `.codex/`, `.pi/`)
were read only to confirm what is deployed; the `.claude/skills` set matches the
46 authored sources exactly (witnessed by `diff` of the two listings).

Each proposal gives the skill, the exact current text, the exact proposed text,
and the ground. Proposals are ordered by the recency of the vision that grounds
them, newest first; the tail — grounded in `skill-designing` rather than in a
dated record — comes last.

Claims are marked **witnessed** (this flow ran it and saw the output), **read**
(this flow read the source and cites it), or **relayed** (a subflow of this
review found it; this flow did not re-verify). Unless marked otherwise, a quoted
line was read by this flow in the file cited.

---

## 1. `main-flow` — how a subflow is launched, and what a cross-harness launch carries

Ground, `flows/162eb3/vision/subflows.md`, four entries, 2026-09-10 and
2026-09-12, psyche typed, none of them carried by any skill (relayed: a grep of
all 46 skills for `sandbox`, `dangerously-skip`, `danger-full-access`,
`ask-for-approval` returns zero hits):

> Okay, we need better training on how to launch subflows. Codex doesn't need another Codex to run ChatGPT models, and vice versa.

> 1. yes, its still a subflow

> 2. no sandbox. all permissions. codex with "--sandbox danger-full-access --ask-for-approval=never" and claude with "--dangerously-skip-permissions" - but some of our wrappers might already add those flags. double check the status on that

> 3. Well, if harness is launched as a main flow, the only way it would start using subflows is if it's loaded with the main flow skill. It's possible to do that, although I'm not sure I want to go down that route. Maybe we should also add into the main flow edit that you're suggesting that, when a different harness is invoked, it shouldn't be invoked with the main flow training, but with the subflow training rather, right?

The living's "double check the status on that" is answered here, **witnessed**:

- `claude` and `codex` on this machine are Nix wrapper scripts
  (`/nix/store/…-claude-code-2.1.263/bin/claude`,
  `/nix/store/…-codex-0.153.4/bin/codex`). Both only prepend to `PATH`; the
  claude wrapper additionally exports `DISABLE_AUTOUPDATER`,
  `DISABLE_NON_ESSENTIAL_MODEL_CALLS` and `DISABLE_INSTALLATION_CHECKS`.
  **Neither wrapper passes a sandbox or permission flag.**
- `/home/li/.codex/config.toml` line 1 `approval_policy = "never"` and line 8
  `sandbox_mode = "danger-full-access"`: a `codex` launch on this machine
  already inherits both, so the flags are redundant there but harmless.
- No `defaultMode`/`bypassPermissions` key exists in `/home/li/.claude/settings.json`
  or `/home/li/primary/.claude/settings.json`, so `--dangerously-skip-permissions`
  **must** be passed explicitly for a `claude -p` subflow.

### 1a. Current text (`skills/main-flow.md`, line 7)

```
Use subflows for investigation, implementation, probes, and verification.
```

### Proposed text

```
Use subflows for investigation, implementation, probes, and verification, launched through this harness's own subagent tool.
```

Preserves the line's list; adds the launch mechanism the 2026-09-10 entry asked
for. It removes nothing.

### 1b. Current text (`skills/main-flow.md`, lines 25-27)

```
Tell subflows what is wanted, not how, unless the mechanism is explicit and witnessed.
A flow is liable for its subflows: what a subflow did, the flow did; asked how, it says it did it through a subflow.
Before the first flow artifact, run `flow-id claude --flows-root ABSOLUTE_DIRECTORY --parent-session "$CLAUDE_CODE_SESSION_ID"`.
```

### Proposed text

```
Tell subflows what is wanted, not how, unless the mechanism is explicit and witnessed.
A flow is liable for its subflows: what a subflow did, the flow did; asked how, it says it did it through a subflow.
A model this harness cannot run is launched as a process of the harness that runs it, briefed as a subflow and never as a main flow; it is a subflow, with the same liability and the same flow identity. Launch it with no sandbox and every permission — `claude -p --dangerously-skip-permissions`, `codex exec --sandbox danger-full-access --ask-for-approval=never` — except where the installed wrapper or that harness's own configuration already supplies them.
Before the first flow artifact, run `flow-id claude --flows-root ABSOLUTE_DIRECTORY --parent-session "$CLAUDE_CODE_SESSION_ID"`.
```

Preserves both existing lines; inserts one line carrying all three 2026-09-12
rulings. It is one line rather than three because the three answers are one
situation: launching a model this harness cannot run.

### 1c. What is deliberately **not** proposed

No line is proposed for `skills/subflow.md`. Ground,
`flows/162eb3/vision/subflows.md`, 2026-09-12, answering a proposal to put a
cross-harness sentence there:

> Well, there's one problem: the main flow should not be available for agents to load by themselves, so that it can only be typed into the prompt. Make sure that that's the case and that the way it's done works for both harnesses. If that's the case, then telling the subflow that something is like the main flow is useless.

The condition holds (**read**): `skills/main-flow.md` frontmatter carries
`user-only: true`, and `skills/skill-designing.md` states what that deploys to
in each harness. So the `subflow` skill gains nothing.

---

## 2. `psyche-interraction` — a comment does not wake the flow; Send to Claude does

Ground, `flows/fe34eb/vision/reports.md`, 2026-09-12, psyche typed (relayed;
this flow did not open the file):

> You shouldn't have been notified every time I post a comment. There are only two ways of posting a comment: 1. Just put the comment 2. Send to Claude. You should only get triggered when I click Send to Claude. … I didn't want you to respond every time I commented. I wanted to make all my comments and then tell you I commented with another sort of overall thing I wanted to say

No skill carries it (relayed: a grep of `psyche-interraction.md`,
`flow-evidence.md`, `main-flow.md`, `correction.md`, `behavior.md` for
`comment`, `Send to Claude`, `trigger` returns nothing on this subject).

### Current text (`skills/psyche-interraction.md`, line 85)

```
While any subflow is out, the reply to the psyche is a holding comment of one or two lines, or the answer to a direct question from what is already witnessed. Never a presentation, a proposal, or a question while a subflow is out.
```

### Proposed text

```
While any subflow is out, the reply to the psyche is a holding comment of one or two lines, or the answer to a direct question from what is already witnessed. Never a presentation, a proposal, or a question while a subflow is out.
A comment on a page the living is reviewing is not a summons. The living comments freely and then says, in one message, that the commenting is done; act on the whole set then, not on each comment as it lands.
```

Preserves the existing line; adds the uncarried ruling beside it because the
existing line governs *what* the reply is while a subflow is out, and the new
line governs *when* a reply is owed at all — different ground, so it does not
replace.

**Open**: this flow did not verify the mechanism by which a comment currently
reaches a session, and the line above is written to hold whatever that mechanism
is. If the harness itself can be configured to wake only on Send to Claude, that
is the better fix and the line is unnecessary — that question is for the living.

---

## 3. `lojix` — the skill teaches a notation the installed binary rejects

Ground: `Vision/datom.md`, "Repository", edited 2026-09-11 (commit `d21ae637e`,
"Land the datom migration scope approved in flow fe34eb") specifically to name
Lojix:

> Everything moves to Datom: all of the stack, Horizon, Lojix, everything;
> no Dotos file remains.

And, decisively, **witnessed on this machine**: the installed
`/run/current-system/sw/bin/lojix` already speaks datom, and rejects the form
the skill teaches.

```
$ lojix 'Query.ByNode.{ alpha node-1 None }'
Queried.{ [] [] { 1 1 } }

$ lojix 'Query.ByNode.(alpha node-1 None)'
(CliRejected [Datom request did not decode: Corporate(Locus { path: [1, 1], extent: Extent(13, 32) }, Shape(Struct, Meaning))])

$ lojix 'Query.ByEventLog.{ 0 1 }'
DeploymentEventsQueried.{ [] [] { 1 1 } }
```

Method: three read-only `Query` requests against the running ordinary socket,
run from `/tmp`, nothing written, no state-changing or subscription request
attempted. The parenthesised form fails because parentheses are Meaning in
datom, exactly as `Vision/datom.md` states — the error names `Shape(Struct,
Meaning)`.

So the skill's `## Dotos syntax` section and **every** request and reply example
in the file is not merely behind Vision: an agent following `lojix.md` writes a
request that the binary refuses. This is the one proposal in this report whose
absence causes a failure today.

### 3a. Current text (`skills/lojix.md`, the `## Dotos syntax` section)

~~~~
## Dotos syntax

Each public client accepts exactly one inline Dotos object. It rejects files, signal files, flags, subcommands, zero arguments, and extra arguments.

Inline decoding requires the client build's `dotos-text` feature. Missing Dotos support is a client-build defect, not permission to pass a file or flag.

A request root is one object.

A variant is `Head.Payload`, with the period glued to both sides. Unit variants are bare.

Lojix products are positional and parenthesized:

```text
Variant.(field0 field1 field2)
```

Vectors use square brackets:

```text
[field0 field1]
```

`None` is bare. `Some` carries one glued payload:

```text
Some.Value
```

A period is structural and right-associative. When a string is expected, a dotted bare value is reconstructed as one string. Use current Dotos curly text for a string that cannot be bare:

```text
“alpha beta”
```

Never name fields or copy the braces from an Ethos type declaration into a socket-client request. The generated Lojix product readers require parentheses.
~~~~

### Proposed text

~~~~
## Request syntax

Each public client accepts exactly one inline datom value and rejects files, flags, subcommands, zero arguments, and extra arguments. A request root is one value.

A struct is brace-enclosed and positional, a vector is bracket-enclosed, a variant is a head with the period glued to both sides, and a variant carrying nothing is bare. `None` is bare and `Some` carries one glued payload. A string with a space or a delimiter is written in guillemets.

```text
Variant.{ field0 field1 field2 }
[ field0 field1 ]
Some.Value
«alpha beta»
```

Never name a field in a request; the position carries the data.
~~~~

Preserves every operative rule: one inline value, no flags, no files, no field
names, right-associative heads. Removes the `dotos-text` feature sentence — a
claim about one client's build that the skill cannot witness, and that
`behavior` would require to be relayed as a claim. Removes the parenthesised
product, the curly-quoted string, and the sentence requiring parentheses,
because the binary refuses all three. It states the datom rules rather than
pointing at the `datom` skill, because those three lines are what an agent
constructing a request needs in hand; the rest of datom stays where it lives.

### 3b. Every remaining example in the file must be converted

Relayed inventory (a review subflow enumerated these; this flow re-read the file
and confirms each string appears in it). Left column exact current text, right
column the datom form:

| current | datom |
|---|---|
| `lojix 'Query.ByNode.(alpha node-1 None)'` | `lojix 'Query.ByNode.{ alpha node-1 None }'` |
| `lojix 'WatchDeployments.(None None None)'` | `lojix 'WatchDeployments.{ None None None }'` |
| `lojix 'WatchCacheRetention.(None None)'` | `lojix 'WatchCacheRetention.{ None None }'` |
| `Watching.(subscription-token commit-sequence)` | `Watching.{ subscription-token commit-sequence }` |
| `meta-lojix 'Pin.(alpha node-1 42 keep)'` | `meta-lojix 'Pin.{ alpha node-1 42 keep }'` |
| `DeployAccepted.(13 (263 263))` | `DeployAccepted.{ 13 { 263 263 } }` |
| `Some.Failed.(Activate ActivationFailed)` | `Some.Failed.{ Activate ActivationFailed }` |
| `ConfigurationWriteRequest.{/run/…/ordinary.sock 432 … /tmp/startup.rkyv}` | the same, with the canonical space inside each brace |
| `(ConfigurationWritten [path])` | `ConfigurationWritten.[ path ]` |
| `lojix-inspect-store '(InspectStore /tmp/lojix.sema)'` | `lojix-inspect-store 'InspectStore.{ /tmp/lojix.sema }'` |
| `lojix-reset-store '(ResetStore)'` | `lojix-reset-store 'ResetStore'` |
| `(LojixStoreReset path=path schema=4 removed_sidecars=count)` | `LojixStoreReset.{ path 4 count }` |
| `(LojixStoreAlreadyCurrent path=path schema=4)` | `LojixStoreAlreadyCurrent.{ path 4 }` |
| `(BootstrapTerminal.Succeeded)` / `(BootstrapTerminal.Failed)` | `BootstrapTerminal.Succeeded` / `BootstrapTerminal.Failed` |
| `(BootstrapRejected [...])` | `BootstrapRejected.[ … ]` |
| `Its single request is the curly positional product \`ConfigurationWriteRequest\`` | `Its single request is the \`ConfigurationWriteRequest\` struct` |

`path=path schema=4 removed_sidecars=count` is doubly wrong: named fields are
what `Vision/datom.md` forbids — "All naming and self-description live in the
type; the text carries only the data."

**Only the three `Query` forms above were witnessed.** The rest are converted
mechanically by the same rule and must each be witnessed against the binary
before the skill is edited — several are state-changing and this flow did not
run them. The right order is: witness each form, then edit once.

### 3c. `daemon` throughout, and the socket names

Relayed: `daemon` appears 8 times in `lojix.md` (this flow confirmed the count),
including `` `lojix-daemon` owns durable state and two authority-tiered
sockets. ``, `Stop the daemon before reset.`, and `` `lojix-bootstrap` is a
separate daemon-free ingress. ``

Ground, `Vision/nexus.md`, "A Nexus is the whole", rewritten 2026-09-11:

> A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not.

The `nexus` skill already carries "call it a Nexus, never a daemon", so the
`lojix` skill contradicts a skill, not only Vision.

**Proposed**: `daemon` → `Nexus` throughout, and `lojix-daemon` → `lojix-nexus`.

**Blocked on a fact this flow does not have**: whether the installed executable
is named `lojix-daemon` or `lojix-nexus`. The skill must name the executable
that exists; `behavior` forbids asserting otherwise. Witness the binary name
before this edit.

A second relayed proposal — `owner socket` → `meta socket`, `owner contract` →
`meta contract`, `## Owner requests` → `## Meta requests`, on the ground that
`Vision/nexus.md` and the `nexus` skill both say **meta socket** — is **not**
carried forward here. The CLI is already named `meta-lojix`, so the vocabulary
is half-converted, but `LOJIX_OWNER_SOCKET` is an environment variable name the
skill cannot rename on its own. Rename the variable and the prose together, or
neither.

---

## 4. `ethos` — the skill describes the abandoned design

Ground: `Vision/ethos.md`, last edited 2026-09-11; `Vision/sema.md` 2026-09-09;
`Vision/signal.md` 2026-09-10; and the substrate audit at
`flows/f6db8d/reports/substrate-audit.md` §5, whose drift table this flow
re-read against both the authored skill and the current Vision.

The authored source `/git/github.com/LiGoldragon/Curriculum/skills/ethos.md` was
last touched **2026-09-04** (read: file mtime). Every line of it is replaced.
The claims that are not merely reworded but **wrong** are listed first, with the
exact current wording:

| exact current text in `skills/ethos.md` | what Vision and the released ethos-zero say |
|---|---|
| `Two roots: \`Library\` and \`Signal\`.` | `Vision/ethos.md` "Roots": "Library, Signal, Sema." Read in ethos-zero `src/lib.rs:141-162`: `pub enum Root { Library, Signal, Sema }` |
| `Library.{ 0 1 0 }` and `Signal.{ 1 0 0 }` | `Vision/ethos.md`: "An ethos file carries no version; datom has no versions. What is versioned is versioned in a manifest of some kind, never in the file." |
| `pub struct Record(pub protos::Text, pub Scores);` and `pub struct Lock(pub LockId, pub LockName, pub FlowId, pub LockPaths, pub LockReason);` | `Vision/ethos.md`: "A declaration turns into the Rust type with **named fields**". Read: ethos-zero `tests/generated/record-types.rs` emits `pub struct Record { pub string: String, pub integer: i64 }` |
| `` `Name.« K V »` is a map alias `` and `Roles.« Text Integer »` / `pub type Roles = BTreeMap<protos::Text, protos::Integer>;` | `Vision/protos.md`: "The key-value map, which the guillemets once delimited, is dropped entirely from protos and its dialects." `Vision/datom.md` "Map": "So datom has no map." |
| associated constants in `` « UPPER_CASE Type » `` | `Vision/ethos.md`: "associated constants in a bracket — upper case, each the name, a dot, and its type". Read: ethos-zero `src/conception.rs:459-475` |
| `Intrinsic names known without import: Text, Integer, …` and every `protos::Text` in the generated Rust | `Vision/protos.md`: "The text type is `String`." `Vision/ethos.md` lists `String`, not `Text`. Read: ethos-zero emits `String` and `i64` |
| `` Every ethos-declared type gets `impl datomic::Datomic` generated from its anatomy. `` | `Vision/ethos.md`: "Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates". Read: `tests/generated/record-types.rs` line 3 |
| the Signal example's `; requests` section label and `pub enum Request` / `pub enum Reply` | `Vision/signal.md`: "A Signal declares queries and responses; input and output are too low-level for it." Read: ethos-zero emits `pub enum Query` / `pub enum Response` |
| (absent) | `Vision/ethos.md`: a Signal's derives are gated — `#[cfg_attr(feature = "datom", derive(…))]` — "so a Nexus can use its contract without a text codec". The skill never mentions it |

### Proposed text — the whole file

~~~~
---
description: Writing or reading an ethos file, or generating Rust from one.
dependencies: [protos, datom]
---

Ethos is the schema language: it specifies the types, datom fills them with data, and ethos-zero generates the Rust. In ethos there are no generics, only kinds. Any repetition in ethos syntax is an implementation failure.

## Roots and file shape

Three roots: Library, Signal, Sema. Signal gives a Nexus its main types and Sema its database types. An ethos file carries no version; what is versioned is versioned in a manifest.

The unit is File: one file, one Rust module, no namespace inside it. A file is written in the sweet form — the root's head, then the sections as siblings, the outer braces omitted — and is converted mechanically to the canonical braced form before it is read as ethos. A Library's sections in order are imports, types, kinds, associations; a Signal's are imports, queries, responses, types; a Sema's are imports, record types. In the Signal and Sema roots the associations of the query, response and record types are implied and never written.

```
Library                                   ; the sweet form, as a file is written
[ protos:String ]                         ; imports
[ Record.{ String Integer } ]             ; types
[]                                        ; kinds
[]                                        ; associations

Library.{ [ protos:String ] [ Record.{ String Integer } ] [] [] }   ; the canonical form the reader sees
```
```rust
#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
pub struct Record { pub string: String, pub integer: i64 }
```

## Declarations

`Name.Type` is an alias, `Name.{ … }` a struct, `Name.[ … ]` an enum. A field is named after its type in snake case; a constructed type type-first, `string_vector`, `lock_option`; a repeated type as first and second. A variant either names a type already defined, which is then the data it carries, or declares its payload in place — a vector, a struct or an enum, each a full type whose derived name carries `_Data`, recursively.

```
Signal
[]                                                   ; imports
[ Lock.LockRequest  Release.LockId ]                 ; queries
[ Locked.Lock  LockRejected.LockRejection ]          ; responses
[ LockId.Integer                                     ; types
  LockName.String
  LockPath.String
  LockRequest.{ LockName Vector<LockPath> }
  Lock.{ LockId LockName }
  LockRejection.[ DuplicateName.Lock                 ;   a variant naming a defined type carries that type
                  PathOverlap.{ Lock Lock } ] ]      ;   a variant declaring its payload inline
```
```rust
pub type LockId = i64;
pub type LockName = String;
pub type LockPath = String;
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Compositional))]
pub struct LockRequest { pub lock_name: LockName, pub lock_path_vector: std::vec::Vec<LockPath> }
// … Lock and PathOverlap_Data likewise
pub struct PathOverlap_Data { pub first_lock: Lock, pub second_lock: Lock }
pub enum LockRejection { DuplicateName(Lock), PathOverlap(PathOverlap_Data) }
pub enum Query    { Lock(LockRequest), Release(LockId) }
pub enum Response { Locked(Lock), LockRejected(LockRejection) }
```

Ethos Zero emits the datom kinds on every struct and enum it generates; an alias bears them through the type it names and carries no derive. A Signal's types gate them behind a `datom` feature that the CLI and client enable and the Nexus does not, so the Nexus compiles its contract without datom-codec. No tuple in the code we design; where a standard trait or a dependency requires one it is allowed at that contact point only.

## Imports and intrinsics

An import names a source and a type: `protos:String`, or `protos:[ String Integer ]`. Intrinsic names known without import: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self. The generated code carries no `use` statements; each imported name is written fully qualified.

## Kinds

Kind is the word for the bearer of capabilities: something that can run is a runner, Runnable is its kind, run is its capability. Kinds are qualifier-named — Runnable, Textualizable, Embodied; Run is not a kind. A kind's identity is its name and its constraints, written as one head, and a constraint is a kind, never a type; angle brackets hold the constraints.

A simple kind opens with a bracket after the dot, holding its capabilities. The receiver after a capability's head names who is called: `.` takes self, `!` takes mutable self, `:` takes no self. A capability with inputs is a headed brace: inputs in a bracket, yield in a bracket holding one type. A complex kind opens with a brace holding four brackets: superkinds, associated types with their constraints, associated constants — upper case, each the name, a dot, its type — and capabilities.

```
Library
[ std:Serializable ]                                          ; imports
[ SinkError.[ Closed Full ] ]                                 ; types
[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; kinds
             create:[ Self ] ]
  Streamable.{ [ Fillable ]
               [ Item<Serializable> ]
               [ CAPACITY.Integer ]
               [ next![ Option<Item> ] ] }
  Processable<[Clonable Sendable] Serializable>.[] ]
[ SinkError.[ Fillable ] ]                                    ; associations
```
```rust
pub trait Fillable {
    fn push(&mut self, input: String) -> Result<i64, SinkError>;
    fn create() -> Self;
}
pub trait Streamable: Fillable {
    type Item: Serializable;
    const CAPACITY: i64;
    fn next(&mut self) -> Option<Self::Item>;
}
pub trait Processable<A: Clone + Send, B: Serialize> {}
// An association is a compile-time assertion; the interaction body is hand-written.
const _: () = {
    fn assert_sink_error_fillable<T: Fillable>() {}
    let _ = assert_sink_error_fillable::<SinkError>;
};
```

## Spacing and generation

Ethos follows the canonical protos print: a space inside every bracket and brace at both ends when non-empty. Generated Rust is committed and held fresh by a test.

```sh
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
# -> Generated.[ /abs/out/orchestrate.rs ]
```

A datom object's basic CLI help emits the ethos that describes its anatomy: point at the object and its ethos prints.
~~~~

What the replacement preserves: the file-roots section, type declarations, kind
syntax, associations, imports and intrinsics, generation by request to
`ethos-zero`, and the non-repetition rule. What it changes: every item in the
table above. What it adds: the third root and its section list, the sweet-form
conversion, the `_Data` naming of inline payloads, the snake-case field-naming
rule, the `datom` feature gate, the fully-qualified-name rule, and the no-tuple
rule — each of them a statement standing in `Vision/ethos.md` that no skill
carried.

Following `flows/564f55/vision/designPractice.md`, 2026-09-08 — "The code they
don't know is Ethos and datom, what this Ethos should turn into in Rust, and how
to use datom in Rust" — every ethos form is shown beside the Rust it generates,
and no example shows anything a model already knows.

**Two things in the replacement are Vision, not witnessed behaviour**, and an
agent following them will hit the substrate audit's defects: a Signal declaring
a type named `Query` generates invalid Rust silently (audit §4.2(a)), and a Sema
root cannot declare a record type named `Record` (audit §4.2(b)) although
`Vision/sema.md` names that section "record types". The skill states the design;
these are code defects to fix, not skill text to weaken.

---

## 5. `datom` — the skill describes the abandoned design

Ground: `Vision/datom.md`, last edited 2026-09-11; `Vision/protos.md`
2026-09-09; substrate audit §5.

The authored source was last touched 2026-09-04. The wrong claims, exact current
wording first:

| exact current text in `skills/datom.md` | what Vision and the released datom-codec say |
|---|---|
| `Map — guillemets, key and value by position:` with `« home { … }  work { … } »` | `Vision/datom.md` "Map": "So datom has no map. … What a map would hold is a struct when its keys are fixed, and a vector of structs when they are not." |
| `String — bare when it contains no space and no delimiter; curly-quoted otherwise.` and every `“…”` in the examples | `Vision/datom.md` "Strings": "The delimited form: guillemets". `Vision/protos.md`: "The curly quotes are not delimiters." |
| `implementing Datomic` (frontmatter description) and `## Datomic in Rust` | `Vision/datom.md` "Name": "Datomic names the conceptual layer abstractly; it is not a term of the code." |
| the whole `Corporal` / `Fault` / `incorporate` / `Embodied` trait block | Read: `datom-codec/src/lib.rs` exports `Composable, Compositional, Datomizable`; no `Corporal`, `Fault`, `incorporate` or `Embodied` exists in protos or datom-codec |
| `fn textualize(&self) -> protos::Text;` | Read: `protos/src/core.rs:93` `pub trait Textualizable { fn textualize(&self) -> String; }` |
| `Potential::<Lock>::from(text); potential.actualize()?` | `Vision/datom.md`: the potential "owns the budget": `Potential::<Query>::from(text).actualize(budget)?` |
| `Boolean:` with `True  False` | `Vision/datom.md` names no Boolean form; `Vision/ethos.md` lists Boolean as an intrinsic type. Dropped from the replacement as unsourced |
| `Every ethos-declared type gets its `Datomic` generated.` | `Vision/ethos.md`: "Ethos Zero emits `Datomizable` and `Compositional`". Moved to the ethos skill, which owns generation |

### Proposed text — the whole file

~~~~
---
description: Constructing, reading or interpreting datom text, or giving a Rust type its datom kinds.
dependencies: [protos]
---

Datom is the pure-data dialect on the protos substrate: data, strictly typed, super dense, no field names. Its whole work is carrying data between text and typed form. Schema-driven and positional: the reader walks the expected type, writing is the exact reverse projection. All naming lives in the type; the text carries only the data. The library is datom-codec.

## A datom is a form at a path

```rust
pub struct Datom { pub path: Path, pub form: Form }
pub enum Form { Struct(Vec<Datom>), Vector(Vec<Datom>), Variant(Symbol, Box<Datom>), Bare(String), String(String), Meaning(Opaque) }
```

## Syntax

A brace structure is a struct, a bracket structure is a vector, and a head in front of a structure is a variant carrying it. In datom a head is always a variant, so it is capitalized. A symbol alone, in a position expecting an enum, is a variant carrying nothing; a variant's name is written as the head every time, one carrying nothing included. Guillemets are the string delimiter and parentheses are reserved for Meaning. A datom is not preceded by a Datom root. What a structure means — struct, vector, string, integer, variant — is said by the position it sits in, never by the structure alone.

A string has two forms: bare, a run with no space and no delimiter glyph, which may be a whole sentence written without spaces in any casing; and guillemets, where every glyph is content until the closing guillemet, which is escaped with a backslash where it is content. Because the position already knows it holds a string, a bare run may carry characters that are syntax elsewhere, the colon among them. An integer is bare ASCII decimal, no leading plus and no leading zero except `0` itself. A decimal is finite and point-mandatory. Today a parenthesized text lands as a plain String, with the Meaning type marked in code.

There is no map. What a map would hold is a struct when its keys are fixed, and a vector of structs when they are not.

```
; datom, in a position expecting Person: a struct of name String, born Integer, address Address, roles Vector<Role>.
{ Ada 1990 { «12 Rue de la Paix» Paris 75002 } [ Author Reviewer.{ 2024 17 } ] }

; Reply: an enum of Accepted.{ id Integer  at String }, Refused.{ reason String  code Integer }, Pending
Accepted.{ 42 2026-09-03T17:46:20 }          ; the timestamp has no space and no delimiter, so it is bare
Refused.{ «no such file: { } is content» 2 } ; delimited: the string has spaces and braces; inside the guillemets they are content
Pending                                      ; a variant carrying nothing

[ 0 42 -42 ]                                 ; a vector of Integer
Observed.Locks.[]                            ; the Observed variant, its Locks variant, the empty vector
[ Some.42 None ]   Ok.{ Ada 1990 }   Err.«no such lock»   ; Vector, Option and Result read as ordinary variants
```

## The datom composes; the type states its positions

The descent into a composition is the datom's act, written once. What only the type can supply, its positions in order, is stated by the type through the derive, so arity, budget and locus live in one place and no type repeats them.

```rust
pub trait Composable { fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>; }
pub trait Compositional: Sized {
    const ARITY: Integer;
    fn from_positions(positions: Positions<'_>, budget: &mut Budget) -> Result<Self, Error>;
    fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error> {      // provided; the descent, written once
        budget.spend(&datom.path)?;
        Self::from_positions(datom.positions("Struct")?, budget)
    }
}
pub trait Datomizable { type Output; fn datomize(&self, at: Path) -> Self::Output; }
```

## Any Rust type

Any Rust type bears the two kinds through datom-codec's derive, with no attributes, because datom is structural all the way down: field order is position order, a field's type is the position's type, a bare variant carries nothing, a single-field variant carries its type's own form, a multi-field variant carries an inline struct. Hand-written impls are reserved to the intrinsics.

```rust
#[derive(datom_codec::Datomizable, datom_codec::Compositional)]
pub struct Locus { pub path: Path, pub extent: Extent }

impl Compositional for Locus {                              // generated
    const ARITY: Integer = 2;
    fn from_positions(mut p: Positions<'_>, budget: &mut Budget) -> Result<Self, Error> {
        Ok(Locus { path: p.position(budget)?, extent: p.position(budget)? })
    }
}
impl Datomizable for Locus {                                // generated: each child placed as the tree is built
    type Output = Datom;
    fn datomize(&self, at: Path) -> Datom {
        Datom { form: Form::Struct(vec![self.path.datomize(at.child(0)), self.extent.datomize(at.child(1))]), path: at }
    }
}
```

## From text and back

```rust
let query: Query = Potential::<Query>::from(text).actualize(budget)?;
let out = response.datomize(Path::root()).protosize().textualize();
```

## Errors

An error names the layer that raised it and the path of the datom where it arose; the extent is the protos node at that path. An error is itself datomizable.

```
[ 1 x ]                                  ; read as Vector<Integer>
Corporate.{ [ 1 ] Value.x }              ; at path 1, the bare string x is not an integer
```

## The interface shape

A program's configuration surface is the datom's shape itself: a data enum at the root whose variants are the main operations, a variant's data carrying what follows. Output is an enum, always. A datom-speaking CLI takes exactly one inline datom value and no flags; datom passes inline at a CLI boundary, never as a datom file.

```sh
orchestrate 'Lock.{ MyLock 6329f1 [ /abs/path ] «why I hold it» }'
# -> Locked.{ 442 MyLock 6329f1 [ /abs/path ] «why I hold it» }
```

A written datom gives every position; omittable fields are not yet.
~~~~

What the replacement preserves: the opening statement of what datom is, the
positional rule, the text forms for struct, vector, variant, string and integer,
and the one-inline-value CLI rule. What it changes: every item in the table.
What it adds: the `Datom`/`Form` types, the `Composable`/`Compositional` pair
and the derive as the living has ruled them, the container forms, the error
form, and the interface-shape rule — all standing statements of
`Vision/datom.md` that no skill carried.

Two removals are deliberate:

- `With no argument, a CLI prints its contract's ethos.` is deleted here and
  kept in the `ethos` skill only. Ground, `skill-designing`: "Each piece of
  meaning has one home: write it once, in the field that owns it." Self-description
  is `Vision/ethos.md`'s statement ("A datom object's basic CLI help emits the
  Ethos that describes its anatomy"), so ethos owns it.
- `Decimal — finite, point-mandatory` is kept (it is in `Vision/datom.md`'s
  syntax paragraph) but `Boolean: True False` is dropped: no current Vision
  statement gives datom a Boolean text form, and `behavior` forbids asserting
  what has no origin.

**Two things to put to the living before this lands.** Both are places where the
code and `Vision/datom.md` disagree, and the proposed text follows the code
because an agent must write Rust that compiles:

1. `Vision/datom.md` writes `fn from_positions(p: Positions<'_>) -> Result<Self, Error>`;
   the released crate writes `fn from_positions(positions: Positions<'_>, budget: &mut Budget) -> Result<Self, Error>`
   (read, `datom-codec/src/core.rs:129-136` at `HEAD`). The proposal uses the
   crate's signature.
2. **The datom-codec working tree is dirty and is removing this very design.**
   Witnessed: `git status --short` in `/git/github.com/LiGoldragon/datom-codec`
   reports ` M src/composition.rs` and ` M src/core.rs`, and the uncommitted
   `src/core.rs` reduces the trait to

   ```rust
   pub trait Compositional: Sized {
       fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error>;
   }
   ```

   — `ARITY` and `from_positions` deleted, while `src/composition.rs` still
   carries `const ARITY` in its impls, so the tree does not currently compile as
   it stands. Committed `HEAD` (`99a9e8c`, version 0.25.7) and the audited
   release (`f2cc068`, 0.25.6) both keep `ARITY` and `from_positions`, and
   `Vision/datom.md` states them. This flow does not know whose change this is
   or whether it is sanctioned; it is reported as an observation. If it lands,
   this proposal's Rust block and `Vision/datom.md`'s own snippet both go stale
   the same day.

---

## 6. `protos` — the skill describes the abandoned design

Ground: `Vision/protos.md`, last edited 2026-09-09; `Intent/context.md`;
`Intent/conversion.md`; substrate audit §2.1 and §5.

The authored source was last touched 2026-09-04. The wrong claims:

| exact current text in `skills/protos.md` | what Vision and the released protos crate say |
|---|---|
| `Six delimiter pairs, four structural and two opaque:` | `Vision/protos.md` "Delimiters": "Five pairs." Read: `protos/src/core.rs:14-24` — `Enclosure { Braced, Bracketed, Angled }`, `Boundary { Guillemets, Parentheses }` |
| `` `« »` | Guillemets (U+00AB/U+00BB) | map: key value key value by position `` | `Vision/protos.md`: "`« »` opaque, every glyph content"; "The key-value map, which the guillemets once delimited, is dropped entirely from protos and its dialects." |
| `` `“ ”` | Curly quotes (U+201C/U+201D) | opaque string: every glyph inside is content until the closing quote; no escapes `` | `Vision/protos.md`: "The curly quotes are not delimiters." Read: no curly quote appears anywhere in the protos source |
| `` `( )` | Parentheses | opaque, read by balance with backslash escapes `` | `Vision/protos.md`: "`( )` reserved for meaning, its type unspecified, read by balance as opaque until it is." |
| the whole `## Layers` table: `Text`, `Protoform`, `Concept`, `Corporal`; `protos::Text`, `Delineation`, `Structural::delineate`, `Conceptual<C>::conceive`, `Printing::print`, `Datomic::incorporate` | `Vision/protos.md` "Layers": "the textual layer; the protosic layer, whose root type is the `Protos` enum; the conceptual layer …; and the compositional layer". Read: `protos/src/lib.rs` exports `Boundary, BoundedProtosizable, Canonicalizable, Enclosure, Error, Extent, Problem, Protos, Protosizable, ReaderBudget, Separator, Symbol, Textualizable` — and nothing else |
| the whole `## Kinds` table: `Structural`, `Conceptual<C>`, `Actualizable<T>`, `Printing`, `Corporal<C>`, `Embodied` | `Vision/protos.md` "Kinds are borne by the type converted and named for the layer it becomes", whose table is `Protosizable`, `Textualizable`, `Datomizable`, `Composable`, `Compositional`. None of the six named kinds exists in the crate |
| `may fault` / `cannot fault` / `MissingBody fault` / `MissingHead fault` throughout | `Vision/protos.md`: "The word is error, not fault, through the chain." Read: `protos/src/core.rs:51-66` — `pub struct Error { extent, problem }`, `pub enum Problem { … }` |
| `` `« k v k v »` — one space inside at both ends `` | `Vision/protos.md` "Canonical print": a space inside the delimiters "except inside the guillemets, where every glyph is content and a space would be load-bearing" |
| (absent) | `Vision/protos.md`: the extent on every node, the budget on the reader, the composition carrying no position — `Intent/context.md`'s rule made concrete, and the crate's actual shape |
| (absent) | `Vision/protos.md`: the backslash escape for a closing guillemet inside a string, "so the ascent never refuses" |

### Proposed text — the whole file

~~~~
---
description: Reading or writing any protos dialect, or touching the protos crate.
dependencies: []
---

Protos is the style every dialect shares: the context-switching parse, the delimiters, the heads, the recursive structure. It owns the only character reader and the only character writer. It knows form and nothing else: what a structure means — struct, vector, string, integer, variant — is said by the conceptual layer that reads it, never by protos.

## Four layers

Textual, protosic, conceptual, compositional. Going down, the information gains density and strictness; going up, visibility. Each step converts into a wholly different type, and nothing of the previous step is used after it. Implement the descent as multiple passes; a single pass is not an option.

```
; textual: these characters, uninterpreted
{ Ada 1990 }
```
```rust
// protosic: an enclosure of two bare runs, each structure at its extent in the text
Protos::Enclosed(Braced, vec![Protos::Bare("Ada"), Protos::Bare("1990")])
// conceptual, here datomic: a struct of two positions, each datom at its path
Datom { path: [], form: Form::Struct(vec![Datom { path: [0], form: Form::Bare("Ada") }, Datom { path: [1], form: Form::Bare("1990") }]) }
// compositional: the meaning fully absorbed; no position, because the tree is consumed
Person { name: String::from("Ada"), born: 1990 }
```

## Delimiters

Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every glyph content; `( )` reserved for meaning, its type unspecified, read by balance as opaque until it is. The curly quotes are not delimiters. There is no key-value map in protos or in any dialect. A brace enclosure's arity is anatomical; a bracket enclosure's is not.

## Structure

Structure is the word for every unit of the text; its type is the `Protos` enum: headed, enclosed, opaque, or bare. A headed structure is a head, a separator and a body; the separators are period, exclamation and colon; the head is a symbol; heads daisy-chain, separators differing. An enclosed structure stands between its delimiters; a bare structure has none.

## Every layer carries its own context

The extent, where a structure sits in the text, is a fact of the protosic layer, and every `Protos` node carries one. The path, where a datom sits in its tree, is a fact of the datomic layer. The budget, how much reading one act allows, is a fact of the reader and lives on it. The composition carries no position.

## Kinds

A kind is borne by the type converted and named for the layer it becomes. No type bears a kind two layers away; a chain is written in the open where it is used, never folded into a kind on its first type.

| type | kind | becomes |
|---|---|---|
| text | `Protosizable` | protos |
| `Protos` | `Textualizable` | text |
| `Protos` | `Datomizable`, or `Ethosizable` further on | its concept |
| `Datom` | `Protosizable` | protos |
| `Datom` | `Composable` | any compositional type |
| composition | `Datomizable` | datom |
| composition | `Compositional` | states its own positions, so a datom can compose it |

```rust
pub enum Protos {
    Headed { extent: Extent, head: Symbol, constraints: Option<Box<Protos>>, separator: Separator, body: Box<Protos> },
    Enclosed { extent: Extent, enclosure: Enclosure, children: Vec<Protos> },
    Opaque { extent: Extent, boundary: Boundary, content: String },
    Bare { extent: Extent, text: String },
}
pub enum Enclosure { Braced, Bracketed, Angled }
pub enum Boundary  { Guillemets, Parentheses }
pub enum Separator { Period, Exclamation, Colon }
pub struct Extent { pub start: usize, pub end: usize }
pub struct Error  { pub extent: Extent, pub problem: Problem }
pub struct ReaderBudget { pub remaining: usize }

pub trait Protosizable    { type Output; fn protosize(&self) -> Self::Output; }  // String -> Result<Protos, Error>; Datom -> Protos
pub trait Textualizable   { fn textualize(&self) -> String; }
pub trait Canonicalizable { fn canonicalize(&mut self); }

let text = person.datomize(Path::root()).protosize().textualize();
```

## String, escape, error

The text type is `String`. A closing guillemet inside a string is escaped with a backslash, so the ascent never refuses. The word is error, not fault, through the chain.

```
«she said \»no\» and left»
```

## Canonical print

A space inside every delimiter at both ends when non-empty, and never inside the guillemets, where every glyph is content and a space would be load-bearing. `Head.body` with nothing around the separator. A single `;` opens a comment to end of line; comments are not printed.
~~~~

What the replacement preserves: what protos is and does not know, the head and
separator rules, bare runs, comments, and canonical spacing. What it changes:
every item in the table. What it adds: the four-layer chain shown in code, the
per-layer context rule, the kinds table as `Vision/protos.md` states it, the
released `Protos` enum, and the guillemet escape.

One line is a design ruling an agent cannot derive, so it is kept although it
reads as rationale — `Vision/protos.md` "Multi-pass": "Multiple passes are
wanted over a single pass, because a single pass creates corner-cutting bad
design." It appears in the replacement as a bare directive, "Implement the
descent as multiple passes; a single pass is not an option", with the reasoning
left to a `protos-rationale` skill if one is ever wanted
(`skill-designing`: "A skill's reasoning and concepts live in a parallel
<skill>-rationale skill").

**Known trap, deliberately left out.** The substrate audit §2.1 witnessed that
`Vector<Integer>`, unless a separator follows, parses as **two sibling protos
structures**, and §4.4 that ethos-zero repairs this with four adjacency scanners
and cannot reprint `Vector<String>` without inserting a space. Vision sanctions
neither. Putting it in the skill would teach agents to work around a defect; the
audit has already put it to the living as a defect. If the living rules that the
split stands, one line belongs in the protos skill and the ethos skill's spacing
section, and this proposal should be reopened.

---
