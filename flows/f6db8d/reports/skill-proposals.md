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
| `` Its single request is the curly positional product `ConfigurationWriteRequest` `` | `` Its single request is the `ConfigurationWriteRequest` struct `` |

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
| `` Two roots: `Library` and `Signal`. `` | `Vision/ethos.md` "Roots": "Library, Signal, Sema." Read in ethos-zero `src/lib.rs:141-162`: `pub enum Root { Library, Signal, Sema }` |
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
## 7. `orchestrate` — curly quotes are not the string delimiter

Ground: `Vision/protos.md` "Delimiters" (2026-09-09) — "The curly quotes are not
delimiters" — and `Vision/datom.md` "Strings" (2026-09-11):

> The delimited form: guillemets, which keep the doubleness of the double quote, cannot be mistyped for it, and point, so the ends are visible at any size.

### Current text (`skills/orchestrate.md`)

```
A reason containing a space or a delimiter is written in Datom curly quotes, “like this”; ASCII double quotes are not Datom string delimiters. A copyable multi-word reason example is:

    orchestrate 'Lock.{ OrchestrateDocs 444e5e [ /absolute/path/to/file ] “Clarify Lock fields” }'
```

### Proposed text

```
A reason containing a space or a delimiter is written in guillemets. A copyable multi-word reason example is:

    orchestrate 'Lock.{ OrchestrateDocs 444e5e [ /absolute/path/to/file ] «Clarify Lock fields» }'
```

Preserves the rule and the copyable example. Removes the trailing guard: naming
the one delimiter positively settles what ASCII double quotes are not, and
`skill-designing` states "needing a guard against a predictable wrong shape
means the instruction is incomplete and must be redesigned."

**Witness before landing.** Whether the installed `orchestrate` accepts
guillemets was not tested by this flow: every `Lock` request changes state, and
the brief's autonomy does not extend to taking locks for a documentation probe.
The `lojix` probe in §3 shows the datom client stack reads guillemets, which is
evidence but not a witness of this binary.

---

## 8. `psyche-grasp` — Dotos, and the wrong comment glyph

Ground: `Vision/datom.md` "Repository" (2026-09-11) — "no Dotos file remains" —
and "Syntax" — "A single semicolon opens a comment."

### Current text (`skills/psyche-grasp.md`, line 12)

```
Mark form — Ethos/Dotos: `;; psyche-grasp: <level> (YYYY-MM-DD)`
```

### Proposed text

```
Mark form — ethos and datom: `; psyche-grasp: <level> (YYYY-MM-DD)`
```

Changes the dead dialect name to the live one and the doubled semicolon to the
one the dialects actually read. A `;;` mark is not wrong — the second semicolon
is comment content — but it teaches a Lisp habit the notation does not have.

---

## 9. `nexus` — what `Vision/nexus.md` says that the skill does not

Ground: `Vision/nexus.md`, rewritten 2026-09-11 (commits `c05f02b58`,
`648c176c5`). The skill is faithful on sockets, contracts, repositories,
subscription, and polling. Four statements standing in Vision reach no skill.

### 9a. Current text (`skills/nexus.md`, opening lines)

```
A Nexus is the long-running whole with at least two sockets, a default CLI client per socket, and the signal contracts it is compiled with. Its long-running executable is <nexus>-nexus; call it a Nexus, never a daemon. The decision-making engine inside it is Nexus Core. A Nexus is a vertex in the graph of nexuses.
```

### Proposed text

```
A Nexus is the long-running whole with at least two sockets, a default CLI client per socket, and the signal contracts it is compiled with; call it a Nexus, never a daemon. A Nexus is like a daemon, said only so that a machine which thinks in daemons understands what a Nexus is. Every component built from now on is a Nexus, and what was built in another shape is rewritten as one. The decision-making engine inside it is Nexus Core. A Nexus is a vertex in the graph of nexuses.
```

Ground for the added second sentence, `Vision/nexus.md` (the 2026-09-11 edit):

> A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is.

Ground for the added third sentence, `Vision/nexus.md` "Why everything is a
Nexus": "Everything built from now on is a Nexus, and what was built in another
shape is rewritten as one." The skill never states it, and it is the statement
that decides what shape a new component takes.

Removes `Its long-running executable is <nexus>-nexus;` from this line: the same
fact is stated eight lines later in the section that owns it — "`<nexus>` is the
repo holding the Nexus and its logic; its long-running executable is
`<nexus>-nexus`". `skill-designing`: "Each piece of meaning has one home."

### 9b. Missing: the router and the shared signal repository

No current text; this is an addition. Ground, `Vision/nexus.md` "Routing":

> Signals cross the network through a router. The router tells signal types apart by an enum that wraps the objects, held in the signal repository, which every component depends on. That repository also holds what every signal needs in common — the handshake payload among it.

### Proposed text, appended to the `## How nexuses fit together` section

```
Signals cross the network through a router, which tells signal types apart by an enum wrapping the objects. That enum lives in the shared signal repository, which every component depends on and which also holds what every signal needs in common, the handshake payload among it.
```

### 9c. Missing: first configuration

No current text. Ground, `Vision/nexus.md` "First configuration":

> A Nexus keeps a standard metadata tree. In it a type records whether the meta Configure was ever done; that record is reversed only on the meta socket, and while it is unset Configure is accessible on the ordinary socket.

### Proposed text, replacing the skill's configuration paragraph's last sentence

Current:

```
A Nexus starts with no arguments. Its executable owns default configuration. It opens its default Sema location: a new store persists those defaults and a populated store resumes them. The same Configure type accepts changed values over the meta socket.
```

Proposed:

```
A Nexus starts with no arguments. Its executable owns default configuration. It opens its default Sema location: a new store persists those defaults and a populated store resumes them. The same Configure type accepts changed values over the meta socket. A standard metadata tree records whether Configure was ever done; while that record is unset Configure is reachable on the ordinary socket, and only the meta socket reverses it. That tree also holds the Nexus's own socket paths and those of every edge it connects to.
```

This is the bootstrap hole an implementer hits first — a Nexus whose meta socket
path is itself configuration — and no skill answers it.

### 9d. Missing: actors

No current text. Ground, `Vision/nexus.md` "Actors": "The engine inside a Nexus
is driven by Kameo actors. The standards of their use are still to be designed.
Arc-Mutex is permitted."

### Proposed text, appended to `## The running Nexus`

```
The engine inside a Nexus is driven by Kameo actors; their standards of use are undesigned, and Arc-Mutex is permitted.
```

### 9e. Flagged, not proposed

`skills/nexus.md` states:

```
Each Nexus owns its own sema database — its typed durable store,
reached only through the sema-engine library, in a `.sema` file. There
is no central storage Nexus.
```

Relayed: "sema-engine library" and the `.sema` file extension appear in no
Vision file (`Vision/sema.md` says only that Sema is "the database engine of a
Nexus, authored in Ethos so the stored types are visible"). This flow did not
witness the crate name. Either witness it or drop the clause; `behavior` does
not let a skill assert an unsourced implementation name.

The `nexus` skill's `## Traits first` and `## No free functions` sections carry
`Intent/mandatoryTraits.md` — "Every method call in our Rust code lives under a
trait" — which is Intent, above Vision, and applies to **all** our Rust, not
only to a Nexus. Placing it in `nexus` means an agent writing Rust in protos,
datom-codec or ethos-zero never reads it. The substrate audit §2.3 witnessed the
consequence: of the three substrate repositories only ethos-zero runs the
no-free-function and no-inherent-method checks. **Proposal**: the rule needs a
home that loads for any Rust work. This flow does not propose the wording,
because creating a new skill is a larger decision than a line edit and the
living should choose between a new `rust` skill, a line in `spirit`, and an
entry-file line.

---
## 10. `psyche-distillation` — example code is for what the models do not know

Ground: `flows/564f55/vision/designPractice.md`, 2026-09-08, psyche by STT. The
file's first entry is already carried; its second is not:

> Okay, now let's look at a thorough vision distillation with example code, but I don't need example code for stuff like how to define a dependency in a Cargo configuration file. That's ridiculous. This is the kind of stuff that the models already know. Just saying that the crate is called datom-codec is enough for them to understand how to do this.
>
> The code they don't know is Ethos and datom, what this Ethos should turn into in Rust, and how to use datom in Rust.

Relayed and confirmed by this flow: `psyche-distillation.md` carries the first
half of the ruling and not the qualification.

### Current text (`skills/psyche-distillation.md`, line 26)

```
A statement about code carries the code: a distilled statement on a syntax, a type, a kind, or a wire form shows example code, because machines think in code and the next machine to read it must understand.
```

### Proposed text

```
A statement about code carries the code: a distilled statement on a syntax, a type, a kind, or a wire form shows example code. Show the code the models do not have — ethos, datom, the Rust an ethos declaration becomes, the use of datom in Rust — and not what any model already knows, a dependency line among it.
```

Replaces rather than accompanies, per `skill-designing`: "A new line replaces
the line it resembles, never stands alongside it." It also drops the trailing
"because machines think in code and the next machine to read it must
understand": it justifies rather than directs, and
`flows/fe34eb/vision/designPractice.md`, 2026-09-12, records the living calling
that phrase "pretty but not very useful on its own" (relayed; this flow did not
open the file).

---

## 11. `testing` — the absurd test

Ground: `flows/8e9e77/vision/tests.md`, 2026-09-08, psyche typed (relayed):

> Also, there are a lot of tests that I call useless tests. They're absurd tests. The machine will say 1 + 1 = 2, and then it'll make a test that says: - Make sure the first element of 1 + 1 is 1. - Make sure the second element of 1 + 1 is 1. - Make sure the answer of 1 + 1 is 2. Right? It's fucking absurd.

### Current text (`skills/testing.md`)

```
A test runs the machinery and observes what it does. A test that searches or compares source text is a change-detector: it fails on any edit and catches no behavior — never write one. Text may be asserted only where the text is itself the product, as generated output against its authored source.
```

### Proposed text

```
A test runs the machinery and observes what it does. A test that searches or compares source text is a change-detector: it fails on any edit and catches no behavior — never write one. Text may be asserted only where the text is itself the product, as generated output against its authored source.
One fact is one test. Asserting a fact's inputs back, or the same fact a second way, adds no coverage; a test earns its place by being able to fail alone.
```

Adds beside the existing line rather than replacing it: the existing line
governs *what a test looks at*, the new one *how many tests one fact gets*.

---

## 12. `psyche-acquisition` — establishing age

Ground: `flows/8e9e77/vision/flow-retrieval.md`, 2026-09-08 (relayed):

> Also, we might have to train the flow retriever to better understand how to use git commits to establish how old something is. Maybe we even need to develop a tool to do that better.

### Current text (`skills/psyche-acquisition.md`, line 7)

```
The psyche's typed words live in transcripts before any log; search them too.
```

### Proposed text

```
The psyche's typed words live in transcripts before any log; search them too.
Establish how old a record is from its commit, not from a date written in it.
```

The softest proposal in this report: the living said "we might have to", which
is a direction rather than a ruling, and the second half — "maybe we even need
to develop a tool" — is a notion. The line is worth writing because this flow
hit the failure directly: `flows/162eb3/vision/subflows.md` carries entries
headed `2026-09-12` while `git log` dates the file `2026-09-11`, and only the
commit settles which records are newer.

---

## 13. `main-flow`, `design`, `psyche-distillation` — three Vision rulings no skill carries

Ground for all three: `Vision/`, 2026-08-27. Relayed; this flow re-read each
Vision line quoted.

| skill | exact current text | proposed text | ground |
|---|---|---|---|
| `main-flow.md` | `` When the living says `remember <flow-id>`, read that flow's psyche records, log, reports, and last model response, then lightly re-witness the current touched state. `` | `` When the living says `remember <flow-id>`, read that flow's psyche records, log, reports, and last model response, reaching its transcript directly when those are not enough, then lightly re-witness the current touched state. `` | `Vision/remembering.md`: "a flow remembers it at a depth fit to the question, reaching the transcript directly when the logs are not enough." |
| `design.md` | `Show the psyche the high-level view routinely.` | `Show the psyche the high-level view routinely; a high-level view takes room and breaks everything down in-line.` | `Vision/highLevelView.md`, "A view takes room": "A high-level view takes room and breaks everything down in-line." |
| `psyche-distillation.md` | `A proposal names, for every statement, the Vision topic it lands in; a statement in the wrong topic cannot be approved.` | `A proposal names, for every statement, the Vision topic it lands in; a statement under the wrong topic is corrected by a distillation edit of its own.` | `Vision/distillation.md`: "a statement under the wrong topic is corrected by a distillation edit of its own." The skill's "cannot be approved" is stricter than the Vision it carries. |
| `psyche-distillation.md` | (absent) | `A distilled statement carries no useless negative.` and `A distilled statement never says it is the psyche's.` | `Vision/distillation.md`, "No useless negatives" and "A statement never attributes itself to the psyche": "Vision is the psyche's; a distilled statement never says so of itself." |

---

## 14. The entry-file gap: `CLAUDE.md` carries the skill-loading rule and `AGENTS.md` does not

Read by this flow: `/home/li/primary/CLAUDE.md`, `/home/li/primary/AGENTS.md`.
Relayed and confirmed: `/home/li/primary/.codex/` and `/home/li/primary/.pi/`
hold only `agents/` role definitions — there is no separate Codex or Pi entry
file, so Codex reads `/home/li/primary/AGENTS.md` itself.

Exactly one rule is in `CLAUDE.md` and not in `AGENTS.md`. Current `CLAUDE.md`,
`## Skills`, second paragraph:

```
Load a skill only through the skill interface: the Skill tool. A skill
file opened with cat, Read, or any other tool lands in the bottom
stratum and carries no authority. The bypass-mode preference for Bash
covers ordinary files, never skill loading.
```

`AGENTS.md`'s `## Skills` section holds only the generated-tree paragraph and
goes straight to `## Variables`.

This is the gap that matters most in this section: every Codex session in this
repository runs without the rule, and Codex's own `## Codex Instruction
Overrides` section already presumes the `$skill-name` mechanism exists without
ever saying it is the only way to load a skill. `context-strata` states the
consequence: "The bottom stratum is what the flow fetches or says itself: tool
results, files it opens, subflow reports, its own output. It carries no
authority." A Codex agent that `cat`s a skill believes it loaded one.

### Proposed insertion into `AGENTS.md`, after the first `## Skills` paragraph

```
Load a skill only through the skill interface: the `$skill-name` injection. A
skill file opened with cat, Read, or any other tool lands in the bottom stratum
and carries no authority. A bypass or full-access permission setting covers
ordinary files, never skill loading.
```

The two entry files name different interfaces because the interface is
different; the rule is one rule. If the entry files are generated from a single
flat source, the interface clause takes the conditional form `skill-designing`
specifies — `{% if claude %}` / `{% if codex %}` / `{% if pi %}` — and the rest
stays literal. Whether they are generated, this flow does not know: neither
`CLAUDE.md` nor `AGENTS.md` is under Curriculum, and Curriculum's `AGENTS.md`
says the repository owns "only `skills/*.md`, `roles.datom`, and repository
documentation."

### 14a. In `AGENTS.md` and not in `CLAUDE.md`: a temporary section that contradicts the generated roles

Current `AGENTS.md`:

```
## Temporary subagent model constraint

- Subagents must never use or inherit Sol.
- `fork_turns="all"` inherits the root model and prevents role/model overrides, so it must not be used when the root model is Sol.
- Spawn ordinary or exploration subagents with the configured Luna/xhigh default or explorer role, using `fork_turns="none"` or a bounded positive fork.
- Terra may be used only for actual implementation when explicitly appropriate and authorized by existing instruction.
- If a non-Sol model cannot be guaranteed, do not spawn the subagent.
```

**Proposed**: move the whole section, unchanged in substance, to
`/home/li/primary/NON_IDEAL_AGENTS.md` with its proper fix named. Ground,
`documentation-placement`: "Put temporary workarounds and their proper fix in
`NON_IDEAL_AGENTS.md`. Favor it over AGENTS.md when uncertain whether an
instruction is permanent." The section calls itself Temporary.

**And it is live-contradicted** (relayed): `roles.datom` assigns `gpt-5.6-sol`
to the demanding depths, and the generated `/home/li/primary/.codex/agents/`
files — `worker.toml`, `write-demanding.toml`, `read-demanding.toml` — carry
`model = "gpt-5.6-sol"`, which the AGENTS.md section forbids. One of the two is
wrong and only the living can say which. Until then an agent reading both is
given contradictory instructions with no way to resolve them.

Two further notes: the section uses `- ` bullets, which Curriculum's `AGENTS.md`
forbids in skills and which no other section of this file uses; and `Sol`,
`Luna`, `Terra` are values that differ between setups, which `behavior` requires
to be skill variables — "Anything that differs between setups — a path, a
repository, a host — must be a skill variable."

### 14b. Both entry files duplicate the `psyche` skill

Both carry, identically:

```
Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `Vision/`, `vision-raw/`, and `flows/*/vision/` before assuming.
```

The second sentence restates `psyche.md`'s "Any agent can search psyche logs for
answers. If a topic is raised that the psyche may have spoken on, check before
assuming" and names the paths `psyche.md`'s own "Where psyche lives" lists.
**Proposed**: both entry files keep only `` Load the `psyche` skill. `` Ground,
`documentation-placement`: "An AGENTS.md carries only what stops a failure or
states a convention an agent cannot derive."

Counter-argument the living should weigh before accepting: the entry file is
middle stratum and always present, while the skill is loaded only when the flow
loads it. If the search rule must reach a flow that never loads `psyche`, the
entry file is its only home and the duplication is deliberate. This flow does
not know which was intended.

---

## 15. `roles.datom` — the manifest is written in curly quotes

Witnessed: `/git/github.com/LiGoldragon/Curriculum/roles.datom` is one line;
`grep -o '“' | wc -l` counts **14** opening curly quotes, so 14 delimited
strings. It uses no guillemet map and depends on no retired delimiter; the curly
quote is the only stale element. Excerpt, verbatim:

```
{ general-instructions “The brief is your authority. Decide what it settles; return what it does not.” }
{ “claude-opus-4-6[1m]” Claude [ Low Medium High Xhigh ] }
{ write “” Unrestricted }
```

### Proposed

Every `“…”` becomes `«…»`. Ground, `Vision/protos.md` "Delimiters": "`« »`
opaque, every glyph content … The curly quotes are not delimiters."

Two details: `«claude-opus-4-6[1m]»` is right and must stay delimited, because
its brackets are content — `Vision/datom.md`: "A guillemet string is opaque:
every glyph inside it is content until the closing guillemet." And `“”`, the
empty string, becomes `«»`; no current Vision statement gives an empty-string
example, so witness that the codec accepts `«»` in a String position before
landing this.

**Blocked**: this flow does not know which reader consumes `roles.datom`. If it
is still read by a Dotos-era reader, converting the file breaks the deployment
that generates every skill tree. Witness the reader first.

---
## 16. Less text — deletions where another line already holds the ground

Ground for the whole section: `skill-designing` — "Write skills with brutal
minimalism"; "Each piece of meaning has one home: write it once, in the field
that owns it"; "A new line replaces the line it resembles, never stands
alongside it"; and its `## Cut these` list.

These were found by a review subflow reading all 43 non-substrate skills;
**relayed**, except those marked ✓, which this flow re-read in the file cited.
Every one is a deletion or a shortening — none adds text. `DELETE` means the
quoted text goes and nothing replaces it.

### 16a. One line, two skills

| skill | exact current text | proposed | ground |
|---|---|---|---|
| `main-flow.md` ✓ | `` Pass `FLOW_ID` and `FLOW_DIRECTORY` unchanged to every nested subflow brief. `` | DELETE | `` Byte-identical line in `subflow.md`, and `main-flow.md` already says `Put `$subflow`, `FLOW_ID`, and `FLOW_DIRECTORY` in every subflow brief.` `` |
| `main-flow.md` | `` Use `flow-evidence` only for a main-flow-delegated artifact or one a named tool or flow will consume. `` | DELETE | It restates `flow-evidence`'s own description, and `subflow.md` holds the acting form: "Create a report or witness only when the main flow delegates it or a named tool or flow will consume it." |
| `main-flow.md` | `Give concurrent evidence writers distinct paths, or use edit coordination before they share one.` | DELETE | `flow-evidence.md`: "Use a main-flow-reserved unique path, or acquire edit coordination before sharing a path." |
| `flow-evidence.md` | `Write no log or index entry.` | DELETE | `subflow.md`: "Do not create a lane, index entry, or log."; `main-flow.md`: "The main flow creates the flow directory, its index entry, and a rare high-level log." |
| `prompt-crafting.md` | `A prompt states decisions and asks for an outcome; the receiving flow determines the mechanism.` | DELETE | `main-flow.md`: "Tell subflows what is wanted, not how, unless the mechanism is explicit and witnessed." — which is the better form, naming the exception. |
| `repository-lifecycle.md` | `Commit and push edited work.` | DELETE | `file-editing.md`: "Commit and push every change your work produces in every affected repository, including generated output." |
| `main-feature-integration.md` | `Land portable producers before consumers.` | DELETE | Three other homes: `nix-input-upgrade.md` ("Update bottom-up: eval-cache boundary repos … must be committed and pushed before their consumers update their locks"), `lojix.md` ("Push producer revisions before pushing the consumer revision that pins them"), `repository-lifecycle.md` ("Keep portable dependencies on pushed public refs."). One rule, four homes: keep `nix-workflow`'s and delete the rest. |
| `psyche.md` ✓ | `The purpose of AI is to extend a psyche. ` (the leading sentence of its first paragraph) | DELETE that sentence; the paragraph begins `A psyche is, as far as words allow, …` | `spirit.md` line 6 is the identical sentence, and `spirit` loads on "Every agent task." |
| `psyche.md` | `Any agent can search psyche logs for answers. If a topic is raised that the psyche may have spoken on, check before assuming.` | DELETE | `psyche-acquisition.md`: "Whenever a new topic is raised or touched upon, reacquire for that topic." (See §14b: the entry files hold it too. Exactly one of the three keeps it.) |
| `claude-harness.md` | `Tool results and the machine's own output are bottom stratum.` | DELETE | `context-strata.md`, its declared dependency, holds it for every harness; and it scopes the split — "Which text a given harness places in which stratum … are that harness's skill's to carry". The generic bottom stratum is not harness-specific. |
| `codex-harness.md` | `Tool results and the machine's own output are bottom stratum.` | DELETE | Same. |
| `claude-harness.md` | `Claude Code has three strata. ` | DELETE the sentence; the paragraph begins `CLAUDE.md and the other entry files are delivered…` | `context-strata.md`: "A thinking machine's context has three strata". |
| `beads.md` | `Persistent credential import is allowed when that supported contract requires it and the task authorizes credential setup.` | DELETE | `secrets.md`, a declared dependency: "Persistent import is allowed when the consumer's supported contract requires it and the task authorizes credential setup." |
| `beads.md` | `` Use `secrets` for PAT and JWK delivery. `` | DELETE | `skill-designing`: "Agents connect surfaces that use the same term. Do not add a line telling them where to look." `secrets` is already a declared dependency. |
| `beads.md` | `When Dolt needs a missing JWK credential, import it through Dolt's supported stdin contract.` | DELETE | `secrets.md`: "Verify the consumer's official stdin or file-descriptor interface first." |
| `agent-harness-packaging.md` | `Put durable packages and configuration in the declarative source that owns that environment.` | DELETE | `nix-workflow.md`, its declared dependency: "Any part of an environment already owned by Nix, CriomOS, or CriomOS-home is fixed, updated, and maintained through that owning declarative source." |
| `agent-harness-packaging.md` | `Do not run an upstream integration installer that mutates a configuration Nix owns; express the intended configuration in its declarative owner.` | DELETE | Same `nix-workflow` line, plus `operating-system.md`: "A change made directly to running system state is lost at the next rebuild." |
| `operating-system.md` | `` Use `lojix` and `meta-lojix` for deployment and observation; their exact typed contract and terminal verification are defined by the `lojix` instructions. `` | `` Use `lojix` and `meta-lojix` for deployment and observation. `` | `skill-designing`: "Do not add a line telling them where to look." `lojix` is already a declared dependency. |
| `lojix.md` | the whole `## Placement` section | DELETE | `operating-system.md` holds both halves; and its second paragraph ("setup-specific wrapper scripts are not an alternative interface") is a pure guard — `skill-designing`: "needing a guard against a predictable wrong shape means the instruction is incomplete." |
| `psyche-interraction.md` | `Get approval before every skill edit.` | DELETE | Curriculum `AGENTS.md` line 1: "Get explicit psyche approval before changing a skill or role." |
| `psyche-interraction.md` | `` A statement enters `Vision/` only as a distillation the living has explicitly approved. Intent and spirit enter only on the living's explicit word. Never edit the spirit skill without explicit psyche approval of exact wording. `` | `Never edit the spirit skill without explicit psyche approval of exact wording.` | The first two sentences are in `psyche-distillation.md`. The third is kept: "exact wording" is more than Curriculum's `AGENTS.md` says. |
| `psyche.md` | `` - `Vision/<topic>.md` — distilled vision: self-standing statements, each reviewed by the living before it stands.` and `- `Intent/<topic>.md` — distilled intent: entered only on the living's explicit word. `` | keep the paths, drop the approval conditions | The conditions are in `psyche-distillation.md` **and** `psyche-interraction.md`. Three homes; keep `psyche-distillation`'s. |
| `psyche-acquisition.md` | `Preserve exact meaning — do not summarize or distill. Use verbatim quotes.` | `Use verbatim quotes.` | `psyche.md`, its declared dependency: "Preserve the psyche's raw words." |
| `design.md` | `While the psyche is designing, the proposal lives in the conversation; no file is written until the psyche approves a landing.` | DELETE | `main-flow.md`, its declared dependency: "A proposal lives in the conversation, revised there, until the psyche approves a landing." |
| `design.md` | `When it does, dispatch a subflow to gather all records on that subject, then compose a distillation proposal in the conversation for the psyche's approval.` | DELETE | `psyche-distillation.md`: "A distillation is composed only in the main flow. A subflow only gathers records that could qualify as candidates for distilling together." |
| `documentation-placement.md` | `Document a repository's own structure inside that repository.` | DELETE | Two lines above, same skill: "Put system shape, invariants, and accepted direction in `ARCHITECTURE.md`." |
| `edit-coordination.md` | `` Edit only after receiving `Locked`. On `LockRejected` or a client failure, report the failure and do not edit. `` | `` Edit only after receiving `Locked`; report a `LockRejected` or client failure. `` | `orchestrate.md`, its declared dependency: "Treat a client failure as a failed operation." The "do not edit" is the guard "only after receiving `Locked`" already excludes. |

### 16b. Lines that explain, restate the name, or an agent would follow untold

| skill | exact current text | proposed | ground (`skill-designing` `## Cut these`) |
|---|---|---|---|
| `spirit.md` ✓ | `Target the best end-shape, not the historically practical compromise.` | DELETE | Five lines up, same skill: "The build target is the design than which none better is possible, the terminal best the work aims at rather than a good-enough or merely best-so-far shape." Flagged, not pressed: spirit is philosophy and needs the living's word on exact wording. |
| `spirit.md` | `When more correctness is introduced into an engine, a design, an architecture, the gain in correctness more than makes up for the added machinery; and as the system expands, that correctness layer makes the expansion simpler and more natural.` | move to a `spirit-rationale` | "A line that explains or justifies a rule instead of directing an action." Same caveat: spirit is the living's. |
| `psyche.md` | `Never treat a psyche log as ground truth. It is an approximation of a living thing you cannot touch.` | DELETE | Three sentences earlier, same skill: "It is tentative and fallible." |
| `psyche.md` | `Sometimes the living psyche is confused, or lacks perspective. A log entry can faithfully record a confused moment. ` | DELETE those two sentences; the directive that follows stands alone | "A line that explains or justifies a rule instead of directing an action." |
| `psyche.md` | `Every rephrasing compounds the drift. ` | DELETE | Same rule; "Preserve the psyche's raw words." is the directive. |
| `psyche-interraction.md` | `Psyche not logged in the moment is psyche at risk of drift.` | DELETE | Same rule; the directives around it are "Log psyche as it is spoken." and "Do not batch — each statement is one write." |
| `psyche-interraction.md` | `Never attribute a position to the psyche that the psyche has not either said verbatim or reviewed as a proposed wording.` | DELETE | Restates the paragraph above it: "Never paraphrase the psyche into a log entry without the psyche reviewing the proposed wording." |
| `psyche-distillation.md` | `Distillation re-articulates psyche records into self-standing statements. ` | DELETE | "A line that restates the skill or role name", and "Nothing in a description appears in the skill." |
| `psyche-distillation.md` | `A proposal re-articulates; it never quotes. A distilled statement stands on its own words.` | `A proposal re-articulates; it never quotes.` | "A new line replaces the line it resembles." |
| `psyche-grasp.md` | `Documentation lives in the code — external documentation falls stale.` | DELETE | `documentation-placement.md`: "Put non-obvious local rationale in code comments." |
| `psyche-grasp.md` | `Psyche-grasp measures the psyche's understanding OF the code. Code-seniority measures alignment WITH the psyche; these are distinct.` | DELETE here; add both definitions to `vocabulary.md` | "A line that restates the skill or role name", and `vocabulary`'s description is "One of our own terms is used, or a term is being defined." |
| `psyche-grasp.md` | `Term "psyche-grasp" is provisional — TO BE REVIEWED by the psyche.` | DELETE | Not a directive. `documentation-placement.md`: "Put temporary workarounds and their proper fix in `NON_IDEAL_AGENTS.md`." |
| `design.md` | `Design fleshes out the anatomy of the psyche's vision.` | DELETE | Restates the name and the description. |
| `realization.md` | `Realization brings design into reality and proves it there.` | DELETE | Same. |
| `subflow.md` | `Do the delegated work and return its final response.` | DELETE | "A line an agent would follow untold." |
| `main-flow.md` | `Keep your context's signal-to-noise ratio high — delegate work to subflows rather than flooding context with tool calls and results.` | DELETE | "A line pairing a goal with a mechanism. The reader cannot tell which one binds." The mechanism is the two lines around it. |
| `main-flow.md` | `Never stop waiting for subflows when the living asks a question.` | DELETE | Same skill already holds "Never block on subflows."; the psyche-facing case is `psyche-interraction.md`'s holding-comment line. |
| `file-editing.md` | `` `jj commit` snapshots the working copy. After it, `@-` is that commit. `jj bookmark set main -r @-` advances main to it. Then push. `` | DELETE | "A line that explains or justifies a rule instead of directing an action." The commands above it are the directive. |
| `file-editing.md` | `` Every `jj` command that takes a description uses `-m`. Never open an editor. Never use raw `git`. `` | `` Every `jj` command that takes a description uses `-m`. Never use raw `git`. `` | "Never open an editor" is the shape `-m` already excludes. |
| `file-editing.md` | `A source file is written in pieces of a few hundred lines; a module that would exceed that is split.` | move out of `file-editing` | This skill's field is landing edits; file size is not that field. Its home is wherever the mandatory-traits rule lands (§9e). |
| `feature-development.md` | `Do not share a claimed checkout.` | DELETE | Guard restating "Use the assigned branch or isolated worktree for feature work." |
| `disk-hygiene.md` | `Delete only authorized, understood data.` | DELETE | "A line true of any competent agent." |
| `agent-harness-packaging.md` | `Obtain current release, packaging, installation, and integration facts from authoritative upstream sources before choosing or changing an integration.` | DELETE | Same. |
| `agent-harness-packaging.md` | `Treat an external harness manager as distinct from the Claude or Codex harnesses it coordinates.` | DELETE | Restates the description. |
| `agent-harness-packaging.md` | `Evaluation is not package proof: build the artifact and behavior-smoke every claimed CLI, GUI, and headless surface.` | `Build the artifact and behavior-smoke every claimed CLI, GUI, and headless surface.` | `nix-workflow.md`: "Run Nix evaluations and builds independently." |
| `nix-workflow.md` | `Run Nix builds only through configured remote builders; never build locally.` | `Run Nix builds only through configured remote builders.` | The guard is the shape "only" already excludes. |
| `nix-workflow.md` | `Keep local overrides transient.` | DELETE | "A line whose meaning a competent reader must guess." |
| `documentation-placement.md` | `Create it when needed and absent.` | DELETE | "A line an agent would follow untold." |
| `documentation-placement.md` | `When auditing or reviewing, check it for stale or inappropriate entries and report them promptly.` | drop `promptly` | Brutal minimalism. |
| `prompt-crafting.md` | `Include only the references needed to resume.` + `A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.` | `A prompt carries only what the receiving flow would not otherwise have.` | Three statements of one rule. |
| `repository-lifecycle.md` | `Close out only after relevant validation exists.` | DELETE | "A line naming the desired end state without teaching the move, the test, or the case." `testing.md` owns proof. |
| `repository-lifecycle.md` | `Preserve peer changes and report remaining blockers.` | `Report remaining blockers.` | "Preserve peer changes" is `edit-coordination`'s whole field. |

### 16c. `skill-designing` against its own rules

| exact current text | proposed | ground |
|---|---|---|
| `Present a proposed edit as exact replacement text or a diff; describing what should be written is not a proposal.` | `Present a proposed edit as exact replacement text or a diff.` | Its own: "needing a guard against a predictable wrong shape means the instruction is incomplete and must be redesigned." |
| `State unusual, impactful instructions once and directly.` | DELETE | Covered by "Each piece of meaning has one home" and "Unusual lines carry the behavior change." |
| `Flag anything noisy, unclear, unsafe, or misplaced. Explain what each proposed change preserves, changes, or removes.` | split onto two lines | Curriculum `AGENTS.md`: "one directive per line as plain prose." |
| `Open with the situation itself. A shared formula carries nothing.` | `Open with the situation itself.` | Its own Cut rule on explanation. |
| `A line pairing a goal with a mechanism. The reader cannot tell which one binds.` | `A line pairing a goal with a mechanism.` | Same. |
| `Minimal is the requirement. Imperative is often the shortest form of it, not the only one.` | DELETE | Restates "Write skills with brutal minimalism." |
| `Removal is better than addition, when the expected behavior is the desired behavior.` | DELETE | Same, plus the whole `## Cut these` list. |
| `Write each rule as a plain sentence. Do not shape a line for memorability.` | `Write each rule as a plain sentence.` | Its own guard rule. |
| `Name the incident or the choice. If you can name neither, do not write the rule.` | DELETE | Restates the line immediately above it. |
| heading `## Skill types` | `## Types` | Curriculum `AGENTS.md`: "A skill carries no heading naming the skill or containing the word 'skill'." |

### 16d. Headings and bullets against Curriculum's own `AGENTS.md`

Curriculum `AGENTS.md`: "A skill carries no heading naming the skill or
containing the word 'skill'." and "No `- ` hyphen-space bullet prefixes; one
directive per line as plain prose."

| skill | current | proposed |
|---|---|---|
| `nexus.md` | `## The Nexus`, `## The running Nexus` | `## Repositories and binaries`, `## What it holds` |
| `psyche.md` | `## Where psyche lives` | `## Where it lives` |
| `psyche.md` | two `- ` bulleted lists (the four levels, and the homes) | plain prose lines, no `- `, no `**` |
| `nix-input-upgrade.md` | the three `- Historical: / - Reconciliation: / - Live:` lines | three plain prose lines |

---
## 17. Descriptions

`skill-designing`: "Nothing in a description appears in the skill. The
description is the situation before loading; the skill is what to do after."
"Repeat neither the skill's name nor the word 'skill'." "No two descriptions may
match the same situation." Relayed.

| skill | current description | proposed | ground |
|---|---|---|---|
| `file-editing.md` | `Editing files means committing and pushing them.` | `A file has been changed and the work is not yet in its repository.` | It is a statement, not a trigger, and its words appear in the body. |
| `psyche.md` | `What agents are reading when they read psyche.` | `A record of what the living has expressed must be read, weighed, or placed.` | Repeats the name twice; states a topic, not a situation; and collides with `psyche-acquisition`'s. |
| `psyche-acquisition.md` | `Reacquiring what the psyche has expressed.` | (reword after `psyche.md`'s, so the two no longer match one situation) | "No two descriptions may match the same situation": both currently match "find what the psyche said about X". |
| `psyche-grasp.md` | `A code site needs marking with how deeply the psyche has seen and understood it.` | (reword) | Repeats the name and paraphrases "grasp". |
| `nexus.md` | `A long-running Nexus with privileged and ordinary sockets, CLI clients, and binary signal contracts is being designed, built, or changed.` | `A long-running component must be designed, built, or changed, and everything it exposes to its peers must be settled.` | All four listed terms appear in the skill. |
| `claude-harness.md`, `codex-harness.md`, `psyche-distillation.md`, `design.md`, `realization.md` | (see §16b for the body lines) | leave the descriptions, delete the body lines that echo them | "Nothing in a description appears in the skill" is satisfied by cutting from the body, which is also the shorter fix. |

**Not proposed**: `lojix`, `orchestrate`, `beads` and `nexus` carry their proper
noun in the description. For a product-named skill the proper noun *is* the word
the task uses, so the descriptions are right and the rule is what is incomplete.
**Proposed instead**: add to `skill-designing`, after "Repeat neither the skill's
name nor the word 'skill'.":

```
A proper noun the task itself uses is the exception; name it.
```

---

## 18. Contradictions between skills — for the living, not for an editor

Each of these is a conflict no agent can resolve from the corpus. None is
proposed as an edit.

**`vocabulary` against a third of the corpus.** `vocabulary.md` holds: "Use
machine, not AI; use flow, not agent, except when reproducing an external name
or quotation." Violated by `spirit.md` ("The purpose of AI is to extend a
psyche", "An agent is a machine; it does not misbehave"), `psyche.md` ("Agents
never access the living psyche"), `skill-designing.md` ("A line true of any
competent agent"), `documentation-placement.md`, `beads.md`,
`edit-coordination.md`, `agent-harness-packaging.md`, and the entry files.
Either the rule is binding and about fifteen files change, or it is aspirational
and should say what it exempts. Note that `spirit`'s first line is itself the
psyche's own wording, so the rule as written condemns the highest-authority text
in the corpus — which is the strongest evidence that the rule, not the text, is
what needs the living's attention.

**`documentation-placement` against `skill-designing`.**
`documentation-placement.md`: "A skill points to the document holding domain
facts instead of restating them." `skill-designing`: "Agents connect surfaces
that use the same term. Do not add a line telling them where to look." Opposite
instructions for the same line. §16a applied `skill-designing`'s form to the
`operating-system` and `beads` pointers, which presumes it wins; if
`documentation-placement` wins instead, those four deletions are wrong.

**`testing` against `behavior`.** `testing.md`: "Infrastructure reports are
ground: a build reported green is green, wherever it ran." `behavior.md`: "A
claim must be relayed as a claim; a thing is verified only by a witness." If the
carve-out is deliberate, one sentence in `testing.md` naming it as the exception
settles it; if not, one of the two lines is wrong.

**"Lane" is undefined.** `main-flow.md`'s description says "owns their shared
flow lane"; `subflow.md` says "Do not create a lane, index entry, or log";
`main-flow.md`'s body says "its claimed lane as `FLOW_DIRECTORY`".
`vocabulary.md` defines "Flow directory" and never "lane". Either add
`Lane: the flow directory a main flow claims.` to `vocabulary.md`, or replace
every "lane" with "flow directory". The second is shorter and this flow would
take it.

**`Curriculum/ARCHITECTURE.md` is stale.** Witnessed: it says "Its canonical
surface is 38 described skill sources and one complete Datom role record";
`ls skills/*.md` counts **46**. Not a skill, so not proposed as skill text, but
it is the document a maintainer reads first.

---

## 19. What this review did not do

It did not read the `.pi` deployment, the deepseek harness, or `beads`'
DoltHub contract against a running system. It did not witness any `orchestrate`
or `meta-lojix` request, because every one of them changes state. It did not
open `flows/fe34eb/vision/reports.md` or `flows/8e9e77/vision/*` directly: §2,
§11 and §12 rest on a review subflow's reading, marked relayed, and their quotes
should be re-read against the files before the lines land. It formed no view on
whether the `datom-codec` working-tree change described in §5 is sanctioned.

## Sources

- Authored skills: `/git/github.com/LiGoldragon/Curriculum/skills/*.md` (46
  files), `roles.datom`, `AGENTS.md`, `ARCHITECTURE.md`.
- Psyche: `/home/li/primary/Vision/{protos,datom,ethos,sema,signal,nexus,distillation,remembering,highLevelView}.md`;
  `/home/li/primary/Intent/{anatomy,context,conversion,data,mandatoryTraits,protosParsing}.md`;
  `/home/li/primary/flows/162eb3/vision/subflows.md`;
  `/home/li/primary/flows/564f55/vision/designPractice.md`;
  and, relayed, `flows/fe34eb/vision/reports.md`, `flows/8e9e77/vision/{tests,flow-retrieval}.md`.
- Vision dating: `git log -1 --format=%as` per file, and commits `d21ae637e`,
  `648c176c5`, `c05f02b58` (2026-09-11).
- Prior evidence: `/home/li/primary/flows/f6db8d/reports/substrate-audit.md`,
  §2.1, §2.3, §4, §5.
- Released code read at its working tree: `/git/github.com/LiGoldragon/protos`
  (HEAD `b543678`, 0.29.1), `/git/github.com/LiGoldragon/datom-codec` (HEAD
  `99a9e8c`, 0.25.7, **working tree dirty**, and the audited release `f2cc068`,
  0.25.6, read through `git show`), `/git/github.com/LiGoldragon/ethos-zero`
  (HEAD `4695ee0`, 6.1.6, including `tests/generated/*.rs` and `fixtures/*.ethos`).
- Witnessed on this machine: three read-only `lojix` requests against the
  running ordinary socket; the `claude` and `codex` Nix wrapper scripts;
  `/home/li/.codex/config.toml`; the absence of a permission default in
  `/home/li/.claude/settings.json` and `/home/li/primary/.claude/settings.json`;
  `diff` of `Curriculum/skills` against `/home/li/primary/.claude/skills`;
  `git status --short` in `/git/github.com/LiGoldragon/datom-codec`.
- Entry files: `/home/li/primary/CLAUDE.md`, `/home/li/primary/AGENTS.md`,
  and the listings of `/home/li/primary/.codex/`, `/home/li/primary/.pi/`,
  `/home/li/primary/.agents/`.

---

## Addendum — corrections surfaced after this report was written

Written by a later f6db8d subflow (thread `f6db8d14-1dfe-472d-914e-9c441f852834`),
2026-09-11 night, reading every `flows/f6db8d/reports/*.md` written after this
file. Same rule as above: nothing here was applied, no skill or manifest was
edited. Claims are marked **witnessed** (this subflow ran it), **witnessed
(prior)** (an earlier subflow ran it and named the command/output, re-read
here), or **relayed** (a report asserts it without a quoted command; named).

**Already covered above, not repeated**: the `lojix` skill's parenthesised
product syntax and its rejection (§3a-b, ground `lojix-history.md` and the
witnessed CLI probe); the `## Dotos syntax` heading, the "Dotos curly text"
string rule, and the general `daemon` → `Nexus` sweep including
`lojix-write-configuration`'s prose (§3a, §3c); the `orchestrate` and `datom`
skills' curly-quote string delimiter and the `roles.datom` manifest's curly
quotes (§5, §7, §15); the `ethos` skill's Signal query enum named `Request`
where the generator emits `Query` (§4, line 330 of this file, ground
`ethos-zero-fix.md`).

### A1. `lojix` — the owner CLI is `lojix-meta`, not `meta-lojix`

Ground: `Vision/nexus.md` "The CLIs" — "The meta CLI is named
component-meta." — and `flows/f6db8d/reports/lojix-history.md`'s eight-count
table, row 2: "`meta-lojix` (`:10`, `:189`, `:408`) | the binary is
`lojix-meta`; `Vision/nexus.md:49` says \"component-meta\"" (relayed there
from the workspace's own `[[bin]]` declarations, confirmed in
`flows/f6db8d/reports/lojix-criomos.md` §1.1: "the pinned revision's
workspace declares `[[bin]] lojix-nexus` … `lojix`, `lojix-meta`").

Current text (`skills/lojix.md:10`):

> Use `meta-lojix` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.

Proposed text:

> Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.

Current text (`skills/lojix.md:189`, inside the request example — already
flagged for parenthesised → braces in §3b's table, whose right column keeps
the wrong binary name):

> `meta-lojix 'Pin.(alpha node-1 42 keep)'`

Proposed text (supersedes §3b's row for this line):

> `lojix-meta 'Pin.{ alpha node-1 42 keep }'`

Current text (`skills/lojix.md:408`):

> The supported deployment and observation interface is `lojix` and `meta-lojix`; setup-specific wrapper scripts are not an alternative interface.

Proposed text:

> The supported deployment and observation interface is `lojix` and `lojix-meta`; setup-specific wrapper scripts are not an alternative interface.

Not proposed here: renaming `LOJIX_OWNER_SOCKET` or "owner socket"/"owner
contract" to "meta" — §3c already declined that on the ground that the
environment variable name is a fact the skill cannot rename unilaterally.

### A2. `lojix` — `Deploy.Host` and `Deploy.UserEnvironment` are missing `SecretsInput`

Ground, **witnessed** by this subflow reading
`/git/github.com/LiGoldragon/meta-signal-lojix/ethos/signal.ethos:30-31`:

> `HostDeployment.{ ClusterName NodeName HostComposition ProposalSource SecretsInput FlakeReference DeploymentTransport DeploymentInputMode DeploymentOutputSelector ActivationBackend HostDeployAction SourceRevisionPolicy Option<NixBuilderSpec> Vector<ExtraSubstituter> }`
> `UserEnvironmentDeployment.{ ClusterName NodeName UserName ProposalSource SecretsInput FlakeReference DeploymentTransport DeploymentInputMode DeploymentOutputSelector ActivationBackend UserEnvironmentAction SourceRevisionPolicy Option<NixBuilderSpec> Vector<ExtraSubstituter> }`

14 fields each, `SecretsInput` fourth. `flows/f6db8d/reports/lojix-history.md`
names the same gap for `Deploy.Host`: "`Deploy.Host` has 13 fields
(`:203-216`) | `meta-signal-lojix/ethos/signal.ethos:30` has **14** —
`SecretsInput` after `ProposalSource`". This subflow additionally confirms
`Deploy.UserEnvironment` has the identical gap, which no prior report named.

Current text (`skills/lojix.md:124-136`):

> `Deploy.Host` has, in order:
>
> 1. cluster name
> 2. node name
> 3. host composition
> 4. proposal source
> 5. flake reference
> 6. deployment transport
> 7. deployment input mode
> 8. deployment output selector
> 9. activation backend
> 10. host deploy action
> 11. source revision policy
> 12. optional Nix builder
> 13. extra substituters

Proposed text:

> `Deploy.Host` has, in order:
>
> 1. cluster name
> 2. node name
> 3. host composition
> 4. proposal source
> 5. secrets input
> 6. flake reference
> 7. deployment transport
> 8. deployment input mode
> 9. deployment output selector
> 10. activation backend
> 11. host deploy action
> 12. source revision policy
> 13. optional Nix builder
> 14. extra substituters

Current text (`skills/lojix.md:139-152`):

> `Deploy.UserEnvironment` has, in order:
>
> 1. cluster name
> 2. node name
> 3. user name
> 4. proposal source
> 5. flake reference
> 6. deployment transport
> 7. deployment input mode
> 8. deployment output selector
> 9. activation backend
> 10. user-environment action
> 11. source revision policy
> 12. optional Nix builder
> 13. extra substituters

Proposed text:

> `Deploy.UserEnvironment` has, in order:
>
> 1. cluster name
> 2. node name
> 3. user name
> 4. proposal source
> 5. secrets input
> 6. flake reference
> 7. deployment transport
> 8. deployment input mode
> 9. deployment output selector
> 10. activation backend
> 11. user-environment action
> 12. source revision policy
> 13. optional Nix builder
> 14. extra substituters

### A3. `lojix` — the store schema is v5, not v4

Ground, `flows/f6db8d/reports/lojix-history.md` table: "\"The daemon accepts
schema v4 and refuses earlier schemas\" (`:337`) | deployed inspector reports
`expected=5`; v4 is refused" — and the same report's witnessed store
inventory: "`/var/lib/lojix/lojix-v5.sema`, 180 KiB, created at daemon start"
against "prior store `/var/lib/lojix/lojix.sema`, 8.8 MiB, schema **v4**,
last written 2026-09-09 16:56", the v4 file now refused.

Current text (`skills/lojix.md:343`):

> The daemon accepts schema v4 and refuses earlier schemas. Reset removes and recreates recognized v2/v3 stores as v4. An existing v4 store is left intact.

Proposed text:

> The daemon accepts schema v5 and refuses earlier schemas. Reset removes and recreates recognized v2/v3/v4 stores as v5. An existing v5 store is left intact.

(This line also names "the daemon"; §3c's general `daemon` → `Nexus` sweep
already covers that word, blocked on the same executable-name witness.)

### A4. `lojix` — `CheckHostKeyMaterial` no longer exists

Ground, `flows/f6db8d/reports/lojix-work.md` §W8, **witnessed** (that
subflow's own change): "`check_key_material`. Removed, with the whole
`CheckHostKeyMaterial` vocabulary, from `signal-lojix` and from `lojix`," with
the reasoning that the verb was a stub always returning an empty mismatch
vector — "a security check that always answers 'no mismatch' is worse than no
check" — and the flow's own note: "Owed: the `lojix` skill documents
`CheckHostKeyMaterial` under 'Ordinary requests'. The skill is now wrong. …
this is not edited here — it is an addition to W2's proposal." This addendum
is that addition.

Current text (`skills/lojix.md:7`):

> Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, `Unwatch`, and `CheckHostKeyMaterial`.

Proposed text:

> Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.

Current text (`skills/lojix.md:115-119`):

> `CheckHostKeyMaterial` has, in order:
>
> 1. cluster name
> 2. node name
> 3. proposal source

Proposed text: delete the block entirely — the verb has no wire type to describe.

### A5. `lojix` — the proposal file must be named `horizon-definition.datom`

Ground, `flows/f6db8d/reports/lojix-criomos.md` §3.4, **witnessed**: "the
bootstrap validator requires the file to be named `horizon-definition.datom`
(`src/bootstrap.rs:2166-2169`,
`safe_existing_regular_file(&input.proposal_source.0, "horizon-definition.datom")`).
A request naming `proposal.datom` is refused with a redacted
`(BootstrapRejected [InvalidRequest])` that says nothing about the name."

Current text (`skills/lojix.md:275`):

> A deployment proposal must be an existing absolute regular non-symlink `proposal.datom` file.

Proposed text:

> A deployment proposal must be an existing absolute regular non-symlink `horizon-definition.datom` file.

### A6. `orchestrate` — `Observe` is a subscription now, and the skill tells agents to re-poll

Ground, `Vision/nexus.md` "Observation by subscription" — "State is observed
by subscription: the subscriber receives the state on open, then each change
as it happens." — and "Polling is forbidden" — "Polling is forbidden; a
correct system goes quiet when nothing changes." Against this,
`flows/f6db8d/reports/orchestrate-review.md` §1.6, **witnessed** (that
subflow ran `live_nexus::observe_delivers_the_state_on_open_and_every_later_
change` against a real `orchestrate-nexus` binary and a real socket, reading
the opening `Observed`, then an unprompted `Observed` after a `Lock`, then
another after a `Release`): "That is Vision's subscription… But
`Vision/nexus.md` forbids polling on the grounds that *a correct system goes
quiet when nothing changes*, and no consumer of Orchestrate goes quiet. Both
CLIs read exactly one frame and exit; **the `orchestrate` skill tells every
agent to re-ask `Observe.Locks`**." Confirmed still open in
`flows/f6db8d/reports/orchestrate-followup.md`: "The subscription reaches no
consumer (D-5). Both CLIs read one frame and exit, and the `orchestrate`
skill tells every agent to re-ask `Observe.Locks` — the polling shape Vision
forbids."

Current text (`skills/orchestrate.md`):

> Observe current Locks:
>
>     orchestrate 'Observe.Locks'
>
> `Observed` carries one complete point-in-time Lock snapshot. It is not a subscription.

Proposed text:

> Observe current Locks:
>
>     orchestrate 'Observe.Locks'
>
> `Observed` carries the complete Lock set on open, then again after every Lock or Release — the connection itself is the subscription, with no token and no `Unwatch`. The current `orchestrate` CLI reads one `Observed` frame and exits; it does not yet hold the connection open to receive the later ones, so re-issuing `Observe.Locks` is today's only way to see a change, not the designed one.

This keeps the honest limit (re-issuing is still the only thing that works
today) while removing the false "it is not a subscription" and no longer
teaching the polling shape Vision forbids as if it were the design.

### A7. `nexus` — the semver rule has no line forbidding what already happened to it

Ground, `flows/f6db8d/reports/orchestrate-review.md` D-1, **witnessed**:
"`signal-orchestrate` went 2.0.0 → 3.0.0 → 3.0.1 with **no wire change at
all**: `git diff 7408fb6 c783b727 -- src/generated/ ethos/` is comment-only
plus dependency repins… Both were set to 3.0.x to match `signal`'s number.
The `nexus` skill says *\"the crate's semver is the wire's semver, and
consumers pin it\"*; mirroring a dependency's number breaks that." Confirmed
in `flows/f6db8d/reports/orchestrate-followup.md` §4 (verified independently,
not merely relayed): "`git diff 7408fb6 c783b72 -- src/` in
`signal-orchestrate` is **empty**… 3.0.x was chosen to mirror `signal`'s
number — which the `nexus` skill's \"the crate's semver is the wire's
semver\" forbids." Also named in `flows/f6db8d/reports/runtime-audit.md:668`.

This is not a case of the skill describing an abandoned design — the rule is
still the intended one — but the skill states it with no line ruling out the
one way it has now actually been broken twice, in the same release, by the
flow that wrote both this skill's dependency and its own contract.

Current text (`skills/nexus.md`):

> The signal wire vocabulary is versioned by its contract crate: the crate's semver is the wire's semver, and consumers pin it.

Proposed text:

> The signal wire vocabulary is versioned by its contract crate: the crate's semver is the wire's semver, and consumers pin it. A contract crate's version reflects only its own wire text; it is never raised to match another crate's version.

### A8. `testing` — do not stop a scratch instance by a pattern a production instance also matches

Ground, `flows/f6db8d/reports/orchestrate-review.md`, disclosed at the top of
the file, **witnessed (self-reported by the subflow that caused it)**: "this
review took the live Orchestrate Nexus down for 21 seconds. A `pkill -f`
written to stop the scratch 0.30.0 instance matched the live systemd user
service as well, because both run the same `/nix/store` path… This was my
error and a breach of the brief's 'no running-service changes'."

No current text — this is an addition; the `testing` skill states several
isolation rules ("Tests share no mutable state") but none about stopping a
process by name/path pattern rather than by the PID a test itself started.

Proposed text, appended to `skills/testing.md`:

> Stop a process a test started by the PID that test holds, never by a process-name or path pattern — a scratch and a production instance of the same build share that pattern.

### A9. `file-editing` — clone from the real remote, and verify a push against it

Ground, `flows/f6db8d/reports/consumer-sweep.md`, **witnessed** (the subflow
that found and corrected it): "The first dispatched attempts at
`signal-orchestrate` and `claude-answers` each cloned with `git clone
--shared /git/github.com/LiGoldragon/<repo> ...`, which repoints the clone's
`origin` remote at the local checkout path rather than GitHub; both attempts
ran a full gate green, committed, 'pushed', and reported success, but the
push had only moved the local checkout's own `main` branch ref — GitHub's
real `main` had not moved."

And `flows/f6db8d/reports/push-verification.md` D1-D3, **witnessed**: the
`repository-ledger` and `signal-repository-ledger` checkouts' `origin` remote
is `gitolite@localhost:<repo>`, a local mirror, with GitHub reachable only
under a differently-named remote (`github`); two reports had called the
gitolite mirror's ref "the pushed authority" and named GitHub's actual head a
"local-only divergent commit" — inverted. D2 names the same class of failure
again with a different cause: a branch reported "pushed, left in place"
exists only on the gitolite mirror, not on GitHub.

No current text — this is an addition to `file-editing`'s landing sequence,
which currently only names `jj git push --bookmark main` and stops.

Proposed text, appended to `skills/file-editing.md`:

> Clone a working copy from its real remote URL, never from another local checkout (`git clone --shared <local-path>` repoints `origin` at that checkout, and a push there never reaches the real remote). Before reporting a push landed, confirm the pushed revision against the real remote directly — `git ls-remote <real-remote-url>` — not merely against the checkout's configured `origin`, which some checkouts point at a mirror (gitolite, or another local clone) distinct from it.

### A10. `subflow` — release every lock before reporting the work finished

Ground, `flows/f6db8d/reports/push-verification.md` D5, **witnessed**: "three
f6db8d locks are still held with their work reported finished. 1111
`LojixNexusHardening`… and 1112 `HorizonRsNoFreeFunctions`… are live, yet
`lojix-work.md` reports all four of its repositories released and verified
at GitHub… `lojix-work.md` never mentions acquiring or releasing any lock…
Two locks appear to be leaked by a finished subflow, and they blocked two
consumer sweeps for the rest of the night."

The `subflow` skill already states the parallel rule for Beads ("For
completed work, close its Beads with evidence and report their status when
returning") but has no equivalent for Orchestrate Locks, and this incident
shows the gap is not hypothetical: it cost two later subflows their sweep
coverage of two repositories for a night.

Current text (`skills/subflow.md`):

> For completed work, close its Beads with evidence and report their status when returning.

Proposed text (new line immediately after it):

> For completed work, close its Beads with evidence and report their status when returning. Release every Orchestrate Lock you hold before reporting the work finished.

---

Skills touched by this addendum: `lojix` (five new items: A1-A5), `orchestrate`
(A6), `nexus` (A7), `testing` (A8), `file-editing` (A9), `subflow` (A10).

New proposals in this addendum: **10**.

---

## Addendum 2 — the `lojix` skill against the 6.0.0 decomposition, the CriomOS bootstrap witness, and the honesty release

Written by a subflow of flow f6db8d (thread
`f6db8d14-1dfe-472d-914e-9c441f852834`), 2026-09-12, reading
`flows/f6db8d/reports/lojix-anatomy.md` §8, `flows/f6db8d/reports/
criomos-hardware.md`, and `flows/f6db8d/reports/lojix-honesty.md`. Same rule as
above: nothing here was applied, no skill or manifest was edited. The authored
source read throughout is `/git/github.com/LiGoldragon/Curriculum/skills/
lojix.md` at `987a1e37d1c7f747b48a47a1806bd4a817cc4b84`, the repository's `HEAD`
at the time of writing — **witnessed** directly by this subflow (`git rev-parse
HEAD`, then `cat -n skills/lojix.md`), not relayed from an earlier report. Line
numbers below are from that file at that revision.

**Already covered above, not repeated as new proposals**: A1's `lojix-meta`
rename and A5's `horizon-definition.datom` naming, both landed (§B7 below only
adds independent confirmation of the binary names).

### B1. `lojix` — the `CheckHostKeyMaterial` row: A4 is applied, this is a closure, not a new proposal

Ground: `flows/f6db8d/reports/lojix-honesty.md` §8 — "The `lojix` skill
documents `CheckHostKeyMaterial`, removed in W8. The skill is wrong and skill
edits need the living's approval; this remains an addition to W2's proposal,
unchanged by this flow." And `flows/f6db8d/reports/lojix-anatomy.md` §8 —
"The `lojix` skill's `CheckHostKeyMaterial` row is still wrong… this is an
addition to W2's proposal, not an edit."

Both reports carry the item forward as still open at the time each was
written. **Witnessed** by this subflow against the current authored source:
`grep -n CheckHostKeyMaterial skills/lojix.md` at `987a1e37` returns nothing,
and the "## Ordinary requests" section names only `Query`, `WatchDeployments`,
`WatchCacheRetention`, and `Unwatch`.

Current text (`skills/lojix.md:8`):

> Use `lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.

Proposed text: unchanged. This addendum's own A4 (above) already proposed
exactly this removal, and `git log --oneline -- skills/lojix.md` shows it was
applied in commit `2ef2b538f7efa9b7da4b98b98b1e9cb73c6f2fdf` ("Apply the
approved skill proposals from flow f6db8d"), an ancestor of `987a1e37`. Both
reports' open item is closed by that commit; no further edit is proposed here.

### B2. `lojix` — no section names the traits a Rust consumer must import

Ground: `flows/f6db8d/reports/lojix-anatomy.md` §8 — "the skill does not name
the traits a Rust consumer must import" — and §3's two decomposition tables,
e.g. `LojixRecord` ("Where this family lives, what it is called, how it
registers"), `DurableStore` ("Where the store is, how far its write counter
has run, every row of one family"), `TransitionJournal` ("Exactly-once
delivery of a durable transition"), `RuntimeCore` ("How an engine is made,
what it sits on, how an action runs to a reply"), `DeployDriving` ("Driving
one deployment from handle to terminal record").

**Witnessed** by this subflow: `grep -n trait skills/lojix.md` at `987a1e37`
returns nothing; the file describes only the socket wire and the CLI clients.

Current text: none — no such section exists in `skills/lojix.md`.

Proposed text, a new section inserted before `## Placement` (currently at
`skills/lojix.md:379`):

> ## Rust library surface
>
> Since `lojix` 6.0.0, every public method on the store and the schema engine lives on a trait, never on an inherent `impl Store` or `impl SchemaRuntime` block. Import the trait that names the question being asked, not the type:
>
> - `LojixRecord` — a record type's table, family, and schema hash
> - `DurableStore` — the store's identity, write counter, and `records::<R>()`
> - `NexusPersistable` — the Nexus's durable configuration
> - `TransitionJournal` — exactly-once delivery of a durable transition
> - `DeploymentLedger` / `GenerationLedger` / `TestRunLedger` — durable deployment, generation, and test-run state
> - `RuntimeCore` — constructing the engine and driving one action to a reply
> - `DeployDriving` / `TestDriving` — driving one deployment or test run to its terminal
> - `NexusReadiness` — the readiness announcement (below)
>
> No method above is reachable through an inherent method any more.

This list is this subflow's own synthesis of `lojix-anatomy.md` §3's tables
(this subflow's inference, not a psyche ruling and not exhaustive of all
sixteen traits landed there) — offered as a starting proposal for the living
to accept, cut, or expand, not as settled wording.

### B3. `lojix` — the readiness announcement a supervisor waits on

Ground: `flows/f6db8d/reports/lojix-anatomy.md` §6b — "`src/daemon.rs` gains
`pub trait NexusReadiness` on `NexusConfiguration`, with `const READY =
"(LojixNexusReady"` and `announce_readiness`, and `run_daemon` calls it once…
writing `(LojixNexusReady /run/lojix/ordinary.sock /run/lojix/meta.sock)` to
standard output and flushing… Two things end the wait and neither is a clock:
the announcement, or standard output closing."

**Witnessed** by this subflow: the current `## Startup configuration` section
(`skills/lojix.md:258-296`) describes only `lojix-write-configuration`, the
datom-to-startup boundary; it says nothing about what the Nexus itself prints
once running, and no other section does either.

Current text: none — no `## Readiness` section exists.

Proposed text, a new section inserted after `## Startup configuration`
(currently ending `skills/lojix.md:296`) and before `## Store inspection and
reset` (currently at `skills/lojix.md:298`):

> ## Readiness
>
> `lojix-nexus` announces readiness on standard output once both sockets are bound and started:
>
> ```text
> (LojixNexusReady /run/lojix/ordinary.sock /run/lojix/meta.sock)
> ```
>
> A supervisor waits on this line, or on standard output closing — which is what a Nexus that dies before readiness does — never on a clock. The announcement never reaches a socket; the wire stays pure signal.

### B4. `lojix` — a bootstrap parent directory must be mode `0700`, or the refusal names nothing

Ground: `flows/f6db8d/reports/criomos-hardware.md` §4.1 — "**The journal
parent, the gc root's parent and the evidence path's parent must be mode
`0700` and owned by the caller.** Witnessed, `src/bootstrap.rs` at the pinned
revision: `private_existing_directory` → `private_directory_metadata`, which
refuses unless `metadata.mode() & 0o777 == PRIVATE_DIRECTORY_MODE` where
`PRIVATE_DIRECTORY_MODE = 0o700`. A default-umask `0755` directory is refused
with a bare `(BootstrapRejected [InvalidRequest])` that says nothing about
permissions. **The `lojix` skill does not mention this**, and it is the
single most likely reason an agent's first bootstrap request fails."

Current text (`skills/lojix.md:338-344`):

> `BuildOnly` carries:
>
> 1. direct immutable build request
> 2. optional builder
> 3. journal parent
> 4. GC root
> 5. terminal-evidence path

Proposed text: insert one paragraph after this list (the combined text,
folded together with B5's restructuring of item 1, is given whole in B5 to
avoid two overlapping edits to the same lines):

> The journal parent, the GC root's parent, and the terminal-evidence path's parent must each already exist, be owned by the caller, and be mode `0700`. A parent left at the default umask (`0755`) is refused with a bare `BootstrapRejected.[ InvalidRequest ]` that names no permission problem — `chmod 700` each parent before submitting the request.

### B5. `lojix` — `BuildOnly`'s build request is a `BootstrapInput`, `Direct` or `Horizon`, not one shape

Ground: `flows/f6db8d/reports/criomos-hardware.md` §4.1 — "The skill says
`BuildOnly` carries \"a direct immutable build request\". It carries a
`BootstrapInput`, which is `Direct.{ flake system selector }` **or**
`Horizon.{ proposal cluster node shape secrets flake system selector }`. The
complete-system build is the `Horizon` arm; the skill describes only the
first and does not say the second exists." Field order for `Horizon`
confirmed against the same report's §4.2 witnessed accepted request:
`BuildOnly.{Horizon.{<dir>/horizon-definition.datom alpha atlas CompleteHost
NoSecrets github:…/8fcfbfec… x86_64-linux
nixosConfigurations.target.config.system.build.toplevel} NixBuilder.«…»
<dir>/journal <dir>/gcroot <dir>/evidence.datom}` — proposal, cluster, node,
host composition (shape), secrets, flake, system, selector, in that order.

Current text (`skills/lojix.md:338-350`):

> `BuildOnly` carries:
>
> 1. direct immutable build request
> 2. optional builder
> 3. journal parent
> 4. GC root
> 5. terminal-evidence path
>
> The direct immutable build request carries:
>
> 1. immutable flake
> 2. Nix system
> 3. output selector

Proposed text (supersedes the block above and folds in B4's addition):

> `BuildOnly` carries:
>
> 1. a `BootstrapInput`
> 2. optional builder
> 3. journal parent
> 4. GC root
> 5. terminal-evidence path
>
> The journal parent, the GC root's parent, and the terminal-evidence path's parent must each already exist, be owned by the caller, and be mode `0700`. A parent left at the default umask (`0755`) is refused with a bare `BootstrapRejected.[ InvalidRequest ]` that names no permission problem — `chmod 700` each parent before submitting the request.
>
> A `BootstrapInput` is `Direct` or `Horizon`.
>
> `Direct` carries:
>
> 1. immutable flake
> 2. Nix system
> 3. output selector
>
> `Horizon` carries:
>
> 1. proposal source
> 2. cluster name
> 3. node name
> 4. host composition
> 5. secrets input
> 6. immutable flake
> 7. Nix system
> 8. output selector

### B6. `lojix` — `DeployRefused` and `ClosureCopyFailed` are missing from the wire vocabulary the skill teaches

Ground: `flows/f6db8d/reports/lojix-honesty.md` §2.2 — "`DeployRefused.{
DeployRefusalReason DatabaseMarker }` with `DeployRefusalReason.[
ContinuationBudgetExhausted NoCorrelatedDeployment DurableWriteFailed ]`" is
the answer for three states that name no deployment, taken "rather than
reusing `DeployRejected`, because reusing it requires inventing a
`DeploymentRecord` for a deployment that does not exist." And §4 — "`nexus::
EffectStage::CopyClosure` mapped to `BuilderUnreachable`… `signal-lojix`'s
`DeploymentTerminalReason` gains `ClosureCopyFailed`… `BuilderUnreachable` is
no longer produced anywhere in lojix."

Current text (`skills/lojix.md:205`):

> Owner reply families are `DeployAccepted`, `DeployRejected`, `DeployTerminal`, `Pinned`, `PinRejected`, `Unpinned`, `UnpinRejected`, `Retired`, `RetireRejected`, `Tested`, and `TestRejected`.

Proposed text:

> Owner reply families are `DeployAccepted`, `DeployRejected`, `DeployRefused`, `DeployTerminal`, `Pinned`, `PinRejected`, `Unpinned`, `UnpinRejected`, `Retired`, `RetireRejected`, `Tested`, and `TestRejected`.

Current text (`skills/lojix.md:218`, immediately after the `DeployAccepted`
example):

> `DeployAccepted` is admission only. It does not prove evaluation, build, copy, activation, or completion.

Proposed text, one paragraph added after it:

> `DeployRefused` carries a `DeployRefusalReason` (`ContinuationBudgetExhausted`, `NoCorrelatedDeployment`, or `DurableWriteFailed`) and a state marker read best-effort. Unlike `DeployRejected`, it names no deployment, because for these three reasons none exists to name.

Current text (`skills/lojix.md:222`):

> A deployment terminal is bare `Succeeded`, `Rejected` carrying a terminal reason, or `Failed` carrying failure stage and terminal reason.

Proposed text:

> A deployment terminal is bare `Succeeded`, `Rejected` carrying a terminal reason, or `Failed` carrying failure stage and terminal reason — for example `Failed.{ CopyClosure ClosureCopyFailed }`, when the copy to the target store itself fails. `BuilderUnreachable` is not produced by a copy failure; it names an unreachable build target, not a copy target.

### B7. `lojix` — the binary names `lojix-nexus` and `lojix-meta`: already correct, three more independent witnesses

Ground: `flows/f6db8d/reports/lojix-anatomy.md:351`, a build failure quoted
verbatim — "lojix-nexus never announced readiness on first start";
`flows/f6db8d/reports/lojix-honesty.md` §7 — "under the feature set the `-p
lojix-nexus` build uses"; `flows/f6db8d/reports/criomos-hardware.md`'s brief
line — "no `lojix-meta` request, no running service touched."

This addendum's own §3c (above) called the executable's real name "a fact
this flow does not have" and left the `daemon` → `Nexus` sweep "blocked" on
it; A1 (above) already supplied that fact from `lojix-criomos.md` §1.1's
`[[bin]]` declarations and was applied. These three reports are three further,
independent sightings of the same two names, in running output and build
arguments rather than in source, so this closes the question rather than
reopening it.

**Witnessed** by this subflow against the current authored source: both names
are already correct in `skills/lojix.md` at `987a1e37`.

Current text (`skills/lojix.md:6`):

> `lojix-nexus` owns durable state and two authority-tiered sockets. The ordinary contract is `signal-lojix`; the owner contract is `meta-signal-lojix`.

Current text (`skills/lojix.md:10`):

> Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. The owner contract is not optional.

Proposed text: unchanged in both cases. No edit is proposed.

---

Skills touched by this addendum: `lojix` only (B1-B7, of which B1 and B7 are
closures of already-applied proposals, not new text; B4 and B5 are one
combined edit; B2, B3, and B6 are new sections or additions).

New proposals in this addendum: **5**.
