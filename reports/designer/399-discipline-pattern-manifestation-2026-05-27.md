# 399 — Discipline pattern manifestation

*Kind: Manifestation · Topics: intent, patterns, workspace, skills, repos · 2026-05-27*

*Per psyche record 988 (Maximum, 2026-05-27) — "Manifest the recurring
architecture patterns across active worktrees, primary skills, and
workspace intent: async mail flow, mail-system actor objects, object-
oriented Rust methods on schema-generated types, and related repeated
implementation disciplines should be durable instructions rather than
only report-local notes." Companion to /398 (completeness audit) and
/395 + /396 (Signal/Nexus/SEMA triad manifestation).*

## 1. Patterns identified

Six repeating patterns drawn from intent records 700-988. Each is a
discipline-shaped statement (not a one-off decision) that surfaces in
multiple records and shapes multiple repos. The names are the
**pattern names** — used in the workspace from now on.

### Pattern A — Async lives at the data-type level (push, hookable, mail-based)

**Anchoring records:** 935 (Communicate trait + signal-frame + mail
state manager + database marker), 962 (mail mechanism is a push
system), 963 (Signal protocol + universal mail mechanism + hookable
events + method-on-message-sent), 970 (Nexus is the mail keeper).

**Synthesis.** Async correlation, message lifecycle, and observer
notification are CARRIED BY THE TYPED MESSAGE OBJECTS themselves, not
imposed externally by polling or by hidden state machinery. Messages
on the Signal protocol move through a universal MAIL MECHANISM with
hookable lifecycle events (`on_sent`, etc.); the mail manager pushes
events; observers attach methods on typed mail-event objects. The
consequence binds every component: same mail substrate, same lifecycle
hooks, same database-marker propagation.

### Pattern B — Three execution centers (Signal + Nexus + SEMA)

**Anchoring records:** 371 (runtime triad framing; Executor renamed in
964), 964 (three schema types ↔ three runtime planes), 970 (Nexus is
the mail keeper; three execution centers; consolidated flow), 981
(Nexus and SEMA each have first-class languages), 982 (each of the
three schema types is its own LANGUAGE with the SAME 4-position
structural shape).

**Synthesis.** Every persona daemon's runtime decomposes into three
execution centers — Signal (wire/communication), Nexus (execution +
mail keeper + Signal-to-SEMA translator), SEMA (durable single-writer
state). Each has its OWN schema language with the same 4-position
shape (Imports / Input / Output / Namespace) and the SAME import-export
mechanism via colon-path namespaces. All three engines share the
pattern *"running code based on input message and returning output
message with populated data."*

### Pattern C — Methods on schema-generated data types (Rust nouns from schema)

**Anchoring records:** 712 (every Rust function is a method on a
non-ZST; sole exemptions cfg-test and fn main), 882 (clarifies and
strengthens the rule; no methods on ZST namespace holders), 942
(prefer logic-on-objects: behaviour lives on schema-created data
types), 945 (schema-created base enums define the reaction and
action types), 947 (Rust uses schema-created types as the nouns of
the system), 953 (schema-created base enums define reaction/action;
execution matches variants), 954 (schema types are the Rust nouns
for actor behavior).

**Synthesis.** Schema-emitted types are the nouns; hand-written Rust
attaches verbs to them as methods on the data-bearing type or as
trait impls. No free functions. No ZST namespace holders. No parallel
hand-rolled mirrors of generated types. When the runtime gains a
behaviour (encode/decode, upgrade, mail-event hook, actor reaction),
the behaviour lives as a method on the schema-emitted noun, not on a
helper-function library beside it.

### Pattern D — Single-writer authority + REST-shaped wire

**Anchoring records:** 949 (execution uses current state and
permission/owner messages; preserve single-owner so mutation cannot
race across writers), 951 (REST-shaped wire architecture; single-
owner mirrors REST's stateless-server-with-canonical-state).

**Synthesis.** SEMA owns the durable state for each resource kind;
mutations route through that one owner. Schema-emitted Operation
enums on the Signal plane are REST-shaped typed resource operations,
not RPC method calls. The single-owner property at SEMA mirrors
REST's canonical-state semantics — distributed semantics with one
canonical owner per kind, no shared-write races, all observation
via push-subscription not poll. Combined with pattern A: writers are
single; observers are many; communication is push-via-mail-events.

### Pattern E — Schema is one recursive struct down to scalars

**Anchoring records:** 933 (schema file IS conceptually a struct
with positional fields; 4-position document is a struct), 940 (one
recursive shape: root-layer struct with macro-expanded fields all
the way down to scalar leaves), 894 (brace IS a key/value map;
namespace is structurally a dynamic enum stored as key/value pair),
932 (macros are sugar syntax in the schema layer; brace-enum
expands to canonical paren-list).

**Synthesis.** A `.schema` document is a typed struct read
positionally; nested struct and enum definitions are macros applied
at known positions; macros bottom out in scalar leaves (booleans,
integers, strings, vectors, typed-string newtypes). The recursion
is one shape — the macro engine is shared substrate for all three
schema types (Signal, Nexus, SEMA), each of which is its own
language (record 982) but uses the same structural skeleton.

### Pattern F — Mirror naming: schema namespace mirrors Rust modules

**Anchoring records:** 902 (single-colon namespace separator;
crate-name:module-name:TypeName mirrors Rust crate-then-module-
then-type), 909 (emitted Rust to src/schema for visibility), 952
(naming MIRRORS — colon→double colon; kebab→snake; PascalCase
unchanged).

**Synthesis.** A schema position named `spirit-next:signal:Frame`
maps mechanically to the Rust type `spirit_next::signal::Frame`.
The identifier IS the same in both views; only the case-rules and
separator differ. Agents grep across either surface and reach the
matching point in the other. The schema and the emitted Rust are
two views of one identity — either view is a sufficient entry
point for navigation.

(Patterns G — schema upgrade traits (record 950) and H — continuous
intent manifestation (record 944) were considered but excluded:
record 944 already manifested broadly in /398; record 950 is a
single-record direction, not yet a repeating pattern across
multiple records.)

## 2. Workspace INTENT.md additions

| File | Commit | Change ID | What added |
|---|---|---|---|
| `INTENT.md` + `skills/component-triad.md` + `skills/rust/methods.md` + `skills/actor-systems.md` | (see below) | (see below) | New §"Recurring architectural patterns" in workspace INTENT.md naming all six patterns + cross-refs to anchoring records; "Recurring pattern" pointer in three skills. |

The workspace INTENT.md section names each pattern, gives the 2-4
sentence synthesis from §1 above, and cross-refs to the existing
detailed sections in INTENT.md and the relevant skills. The new
section sits AFTER §"The wire architecture is REST-shaped" and
BEFORE §"Concept designer is the entry for new concepts" because
it's a structural-pattern claim about the schema-driven stack.

## 3. Skills additions

| Skill | What added |
|---|---|
| `skills/component-triad.md` | Pattern names in §"Runtime triad" — references the workspace INTENT.md §"Recurring architectural patterns" so the pattern terms are searchable from the triad skill. |
| `skills/rust/methods.md` | §"Recurring pattern — schema-generated objects as method surface" header restated as Pattern C. |
| `skills/actor-systems.md` | §"Recurring patterns this skill realizes" cross-ref to patterns B, C, and the push-not-pull surface. |

These additions are LIGHT-TOUCH — no skill content rewriting. The
goal is the pattern-name visibility; the discipline content was
already correct.

## 4. Per-repo branches updated

Each pattern that affects multiple repos got a §"Recurring patterns
realized in this repo" naming section added to the relevant
per-repo INTENT.md on the existing
`designer-intent-manifestation-2026-05-27` branches.

| Repo | Patterns named |
|---|---|
| `signal-frame` | A, B, D (already covers individual records; now names the patterns) |
| `spirit-next` | A, B, C, D, E, F |
| `spirit` | A, B, C, D |
| `schema-next` | B, C, E, F |
| `schema-rust-next` | B, C, F |
| `signal-spirit` | A, B, D, F |
| `core-signal-spirit` | A, B, D, F |
| `nota-next` | E, F |
| `cloud` | A, B, C |

Each per-repo addition uses the **same pattern letters and same
short synthesis** as the workspace INTENT.md so the repo-scope
sections and the workspace section read as one cross-referenced
discipline.

## 5. ESSENCE.md proposals (not executed)

**Proposal C — Async lives at the data-type level (Pattern A).**

Combined with the three-execution-centers proposal already on the
table from /398 (Proposal A for record 964), Pattern A could be
considered for ESSENCE-tier promotion. The reasoning: Pattern A
binds every component's wire protocol, observer mechanism, and
state-evolution proof to the same substrate; it's a foundational
architectural commitment, not a topic-specific discipline. But the
records anchoring it (935, 962, 963, 970) are High and Maximum
certainty across the cluster — promotion would be in the same arc
as the three-execution-centers promotion if the psyche elects to
move that one.

**Recommendation.** Hold Pattern A for psyche consideration
ALONGSIDE Proposal A from /398. Promote both together or neither —
they're the same architectural commitment seen at different scales.

No other ESSENCE-tier promotion proposed in this report.

## 6. Remaining gaps + open questions

1. **Mencie repo still does not exist.** Pattern B (specifically the
   UI panel = nexus schema clause) cannot land per-repo until the
   Mencie crate scaffold exists. Forward-only carry from /398.

2. **Pattern G (schema upgrade traits, record 950) is single-record.**
   Not promoted to pattern status here. If upgrade-trait records
   accumulate, revisit in a future manifestation pass.

3. **Pattern boundaries between A and B may simplify.** Pattern A
   (async + mail) and Pattern B (three execution centers) overlap
   significantly — Nexus is the mail keeper (per 970), and the mail
   keeper is the realization of the async surface. Future iterations
   may merge them into one pattern; for now keeping the names
   distinct because A is the substrate (data-type-level async) and B
   is the architecture (three execution centers).

4. **Pattern naming convention.** This report names patterns
   A through F. If patterns become a stable workspace vocabulary, a
   future skill (`skills/patterns.md`?) could enumerate them with
   explicit labels and a topic-index. Not built today; carry forward
   if the pattern-naming becomes load-bearing.
</content>
</invoke>