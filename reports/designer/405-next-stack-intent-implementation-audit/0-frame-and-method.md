# 405/0 — Frame and method: next-stack intent↔implementation audit

*Kind: Meta-report frame · Topics: schema, nota, spirit-next, nexus, sema, signal, audit, intent · 2026-05-28*

*Per psyche prompt 2026-05-28: "audit the next stack (nota/schema/spirit)
for gaps between implementation and intent. do a lot of intent
amalgamation first, and audit the implementation of course." This is the
orchestrator frame of a meta-report directory; §1 is the amalgamated
intent (the audit yardstick), §2 the method, §3 the pinned commits and
dispatch plan. Each sub-agent audit lands as a numbered file beside this
one; the synthesis is the highest-numbered file.*

## 0. What "the next stack" is

Five operator-owned `main` repos form the schema-derived stack, bottom
to top:

| Layer | Repo | Role (per `protocols/active-repositories.md`) |
|---|---|---|
| 0 — raw text | `nota-next` | Raw structural block parsing, source spans, `qualifies_as_*` methods only. No schema semantics. |
| 1 — schema lang | `schema-next` | Position-aware schema macros; lowers `.schema` → ordered macro-free `Asschema`. |
| 2 — Rust emit | `schema-rust-next` | Consumes `Asschema`; emits Rust source text. |
| 3 — pilot | `spirit-next` | Running pilot: `schema/lib.schema` lowered + emitted, then driven by a real NOTA CLI and rkyv Unix-socket daemon. |
| wire | `signal-frame` | Signal wire substrate: typed frames, channel macro, schema concept. |

The audit yardstick is the psyche intent in §1, NOT the repos' own
`INTENT.md`/`ARCHITECTURE.md` (those are agent-synthesised claims —
themselves auditable for drift from psyche intent).

## 1. Amalgamated intent (the yardstick)

Synthesised from Spirit records 700-1008 (queried live 2026-05-28) and
workspace `INTENT.md`. Grouped by the stack concern each constrains.
Record numbers are the Spirit identifiers; quotes are psyche wording.

### 1.1 The schema IS the architecture; schema at the heart

- **Schema is the canonical truth source** (record 1000, Maximum).
  Schema-emitted Rust types are the canonical type for *every type that
  appears in the system*; everything hand-written is a method on those
  nouns or a trait impl those nouns implement. *No hand-written enum
  stubs at system boundaries, no hand-written observer state, no
  hand-written ValidationError or DatabaseMarker shims.*
- **Schema defines data types only** (records 713-715). Effects,
  fan-out, effect tables are runtime dispatch, not authored schema.
- **The schema is one recursive struct down to scalars** (Pattern E:
  894, 932, 933, 940). A `.schema` document is a typed struct read
  positionally; nested struct/enum definitions are macros at known
  positions; macros bottom out in scalar leaves. The macro engine is
  shared substrate for all three schema types.

### 1.2 Three schema types, three runtime planes (Pattern B)

- **Three schema types** (record 964, Maximum): SIGNAL (wire), NEXUS
  (execution/IO/UI), SEMA (durable state). Each has its own engine with
  its own traits, but all three share *"running code based on input
  message and returning output message with populated data."* The ROOT
  TYPE of a schema is the message surface.
- **Each schema type is its own LANGUAGE with the SAME 4-position shape**
  (record 982, High): **Imports / Input / Output / Namespace**, and the
  SAME import/export mechanism via single-colon namespace path
  (`signal-frame:Frame`, `schema:spirit:Entry`). The planes differ in
  what fits each position, not in the structural skeleton. *Operator's
  report 219 does not yet carry this clarification* — the record names
  this gap explicitly.
- **Executor renamed to Nexus** (record 964 refining 371).
- **Nexus is the execution layer** (record 965, Maximum): internal IO,
  external calls (cloud→Cloudflare CLI), AND all UI panels (Mencie).
  Supersedes 880's scope-restriction; Nexus is now PART OF the
  schema-derived stack.

### 1.3 Nexus is the mail keeper; the runtime flow (Pattern A + B)

- **Nexus is the mail keeper** (records 966, 970, Maximum). *"When Nexus
  has the mail, the mail is in the BEING-PROCESSED state; Nexus IS the
  runtime representation that a mail is being processed."*
- **Three execution centers** (record 967): Signal (communication),
  Nexus (execution + in-flight mail + translator), SEMA (durable state).
- **The complete flow** (record 970):

```text
Signal IN -> Nexus accepts mail (BEING-PROCESSED) -> Nexus translates to
SEMA query -> SEMA runs, produces state change + reply -> Nexus receives
SEMA reply -> Nexus translates to Signal response (with logging) -> Signal OUT
```

- **Nexus translates both directions** (record 968): Signal→SEMA in,
  SEMA→Signal out, emitting lifecycle/logging events.
- **Async lives at the data-type level** (Pattern A: 935, 960, 961,
  962, 963). Universal mail mechanism; message identity + sent-state are
  typed data in the protocol, not ambient bookkeeping. Message-sent is an
  event surface (`on_sent`) hooks/UI/routers react to. *Push, not poll.*
- **Pattern A push = sending a typed object to its next logical place**
  (records 989, 990, Maximum). The Signal actor validates an incoming
  message, performs Signal-layer checks, then PUSHES the object onward
  to Nexus. The `on_sent`-style hook fires at the Signal→Nexus handoff.

### 1.4 SEMA = database work

- **SEMA means database work — specifically WRITING to the durable state
  file** (records 1007, 1008, High). Today's substrate is redb; the file
  extension should become `.sema` so the name states the role. *An
  in-memory `Store` can prototype the `SemaInput`/`SemaOutput` language,
  but it is not a full SEMA proof until the operation writes the durable
  database artifact.* Rename lands when durable storage is implemented
  (bead `primary-q2au`, currently `Mutex<Vec>` in-memory).

### 1.5 Single-writer + REST-shaped wire (Pattern D)

- **REST-shaped wire** (record 951, High): schema-emitted Operation enums
  on the Signal plane are REST-shaped typed resource operations, not RPC
  calls. SEMA owns durable state per kind; single-owner mirrors REST's
  canonical-state semantics.

### 1.6 Naming, methods, NOTA discipline (Patterns C, F + overrides)

- **Methods on schema-generated types** (Pattern C: 712, 882, 881, 942,
  945, 947, 953, 954). Schema-emitted types are nouns; Rust attaches
  verbs as methods on data-bearing types or trait impls. No free
  functions (except `cfg(test)` + `fn main`). No ZST namespace holders.
- **Mirror naming** (Pattern F: 902, 909, 952). `spirit-next:signal:Frame`
  ↔ `spirit_next::signal::Frame`. Single colon → double colon; kebab →
  snake; PascalCase unchanged. Emitted Rust lives at `src/schema/<mod>.rs`.
- **Schema authoring shape** (records 874, 876, 877, 886, 887). Root
  object name omitted (reader knows the root); nested objects name
  themselves. Enum = `(QualifiedName (variants...))`; struct =
  `[fields]`; newtype-struct = `[singlefield]`. Schema needs a
  schema-authored SELF-DESCRIPTION (`root.schema`) that lowers through
  the engine; possibly a minimal built-in `core.schema` first.
- **Macros are plain NOTA records dispatched by position+shape** (record
  880), via the schema-next MacroRegistry — NOT sigils. Reserved sigils
  `~ @ ! ? * =` live at the NOTA layer; the schema stack does not consume
  them.
- **NOTA strings come EXCLUSIVELY from bracket forms** — `[text]`,
  `[|text|]`, bare camelCase/kebab at String positions. Never quotation
  marks. Brace `{}` is ALWAYS a key/value map; namespace at position 3 is
  pair-style `Name TypeDefinition`, not `(Name TypeDefinition)`.

### 1.7 Tests must PROVE, not pretend

- **Tests prove not pretend** (record 1006, Maximum). In-process
  synthetic state is LESSER PROOF than tests that build real binaries via
  Nix and launch them. Canonical shape: schema files in real project
  paths drive Nix code-gen; spirit CLI + daemon built by Nix; tests
  launch the binaries; CLI sends real rkyv signal frames over a real Unix
  socket; the Nexus executor at the center receives/processes/returns
  (it has its OWN typed input/output); SEMA durable state; reply comes
  back end-to-end; EVERY component driven off the schema.
- **Tests use schema-emitted types through schema-type traits** (records
  998, 999, 1000). A Signal→Nexus→SEMA test asserts against generated
  objects (`MailLedgerEvent`, `NexusInput`/`NexusOutput`,
  `SemaInput`/`SemaOutput`); ad-hoc test-only enums are not a valid
  substitute. SEMA engine operations take SEMA schema input, emit SEMA
  schema output.

## 2. Method

One sub-agent per repo (5), dispatched in parallel in background. Each:

1. Reads the relevant §1 intent slice (quoted into its brief), the repo's
   own `INTENT.md` / `ARCHITECTURE.md` / `AGENTS.md`, and the code at the
   pinned commit.
2. Classifies each applicable intent item as **MET** / **PARTIAL** /
   **MISSING** / **DIVERGENT** (implementation contradicts intent) /
   **AHEAD** (implementation has something intent hasn't yet named).
3. Cites `path:line` evidence for every classification — no
   classification without code evidence.
4. Writes exactly one report file in this directory; edits no repo code
   (read-only audit); dispatches no sub-sub-agents.

The audit targets operator-owned `main` (the canonical implementation).
Where a designer worktree prototype has already proven something main
lacks, the agent notes it as context, not as the audited surface.

## 3. Pinned commits and dispatch plan

All commits captured 2026-05-28; the audit is reproducible against them.

| File | Repo | Pinned `main` commit |
|---|---|---|
| `1-nota-next.md` | `nota-next` | `fa14c7fb027c6c552a4ba29c3eddc61b2b5b6cfb` |
| `2-schema-next.md` | `schema-next` | `e0681f2fb038734ef3a00878749ce2870d7c1d51` |
| `3-schema-rust-next.md` | `schema-rust-next` | `68559f86311bffb341e7cf1b3663e5ef0c123403` |
| `4-spirit-next.md` | `spirit-next` | `6938dd6af1aa69d7102f9a40799c3de4e39bae55` |
| `5-signal-frame.md` | `signal-frame` | `d61ebf25997c47c997c0dce1d576f870e3e8383c` |
| `6-overview.md` | (synthesis) | — |

Convergence note already visible at frame time: `spirit-next` main
`6938dd6` is *"spirit: add nix-built binary integration tests"* and
`schema-rust-next` main `68559f8` is *"emission: emit schema-plane engine
traits"* — operator main appears to have independently moved toward the
record-1006 (Nix binaries) and record-964/982 (three-plane traits)
intent. The audit measures how far that convergence actually reaches.
