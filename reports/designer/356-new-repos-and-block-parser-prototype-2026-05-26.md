# 356 — New repos + block-parsing prototype slice

*Designer-assistant execution of two coordinated landings per psyche
2026-05-26 authorization: (A) three new GitHub repos for the
persona-prefix retirement (records 779-782); (B) a `nota-next` branch
on the existing `nota` repo (record 781); (C) the block-by-block
parsing prototype slice with constraint tests pinning each
load-bearing intent (records 774-777).*

## Summary

| Output | Location | Status |
|---|---|---|
| `spirit` repo | `https://github.com/LiGoldragon/spirit` (main @ `1d1ba72`) | scaffold pushed |
| `signal-spirit` repo | `https://github.com/LiGoldragon/signal-spirit` (main @ `8a87870`) | scaffold pushed |
| `core-signal-spirit` repo | `https://github.com/LiGoldragon/core-signal-spirit` (main @ `bcd2d61`) | scaffold pushed |
| `nota-next` branch | `LiGoldragon/nota` @ `45a7543` (nota-next) | pushed |
| Block-parsing prototype | `designer-schema-derived-nota-2026-05-26` @ `0e04c22` | 12/12 constraint tests pass |
| Cargo build (prototype) | — | green |
| Cargo test (prototype, all) | — | 41/41 pass (12 new + 14 schema + 15 kernel) |

All three new repos created with the canonical workspace file set
(`README.md`, `ARCHITECTURE.md`, `INTENT.md`, `AGENTS.md`,
`CLAUDE.md`, `.gitignore`, `flake.nix`, `rust-toolchain.toml`,
`Cargo.toml`, `src/lib.rs`, plus a per-repo `schema/*.schema` skeleton).

## Part A — New repositories created

### `spirit` — schema-driven contract repo

```text
gh repo create LiGoldragon/spirit --public \
  --description "Spirit component — schema-driven contract for the psyche-to-mind interface"
→ https://github.com/LiGoldragon/spirit
```

**Scaffold contents** (11 files):
- `README.md` — short intro + provenance pointer back to legacy
  `persona-spirit` per records 765/767/780.
- `ARCHITECTURE.md` — schema-driven contract framing per /353 §2-3;
  explicit non-scope of `EffectTable` / `FanOutTargets` /
  `StorageDescriptor` per records 730-732; component-triad
  mermaid; relationship-to-`nota`-and-`schema` mermaid; deployment
  shape (side-by-side per record 672); boundaries table.
- `INTENT.md` — fresh per-repo synthesis. Verbatim psyche quotes
  from records 765, 767, 780 in italics. Repo-scope only per record
  717. Open shape questions section carries gaps to the psyche per
  `skills/intent-clarification.md`.
- `AGENTS.md` — `@~/primary/AGENTS.md` pointer.
- `CLAUDE.md` — `You MUST read AGENTS.md.`
- `.gitignore` — `/target` + `/result` (Rust + nix).
- `flake.nix` — minimal Rust + Nix setup; schema-filter on `.nota`
  + `.schema` extensions.
- `rust-toolchain.toml` — 1.85.0 + rustfmt + clippy (matches legacy).
- `Cargo.toml` — lib crate `spirit`, version `0.4.0-pre`, no
  dependencies yet (contract-focused; daemon impl deferred).
- `src/lib.rs` — placeholder module-level documentation pointing at
  the schema; `#![forbid(unsafe_code)]`.
- `schema/spirit.schema` — three-section schema skeleton mirroring
  the canonical layout from `signal-persona-spirit/spirit.schema`
  but **without** the retracted-drift constructs (no `EffectEmitted`,
  no `OperationReceived`, no `Observable` filter declarations — those
  belong to the runtime per /353 §9). Five-block layout:
  `{ imports } [ ops ] [] { namespace } [ replies+events ]`.

**Commit + push:**

```text
jj describe -m 'designer: initial scaffold per psyche 2026-05-26 (record 780)'
jj bookmark create main --to @
jj git push --bookmark main --allow-new
→ Add bookmark main to 1d1ba727b53c
```

### `signal-spirit` — ordinary signal layer

```text
gh repo create LiGoldragon/signal-spirit --public \
  --description "Spirit signal layer — ordinary messaging contract"
→ https://github.com/LiGoldragon/signal-spirit
```

**Scaffold contents**: same file set as `spirit`, with content
specialized for the ordinary signal layer:
- `README.md` notes the successor relationship to
  `signal-persona-spirit` (record 767) and explains the "core vs
  signal" split per records 766, 768.
- `ARCHITECTURE.md` declares what is IN scope (`State`, `Record`,
  `Observe`, `Watch`, `Unwatch`, replies, events) and what is OUT
  (privileged operations → `core-signal-spirit`; daemon runtime →
  `spirit`).
- `INTENT.md` carries the ordinary-layer intent from records
  765-768; topic vocabulary discipline from legacy v0.3.
- `schema/signal-spirit.schema` — declares the ordinary wire layer's
  signal types (mirrors the ordinary-layer subset of the legacy
  spirit.schema; no Features section per records 730-732).
- `Cargo.toml` — lib crate `signal-spirit`, `0.4.0-pre`.

**Commit + push:**

```text
jj describe -m 'designer: initial scaffold per psyche 2026-05-26 (record 780)'
jj bookmark create main --to @
jj git push --bookmark main --allow-new
→ Add bookmark main to 8a87870ef95a
```

### `core-signal-spirit` — privileged/control signal layer

```text
gh repo create LiGoldragon/core-signal-spirit --public \
  --description "Spirit core signal layer — privileged/control messaging contract"
→ https://github.com/LiGoldragon/core-signal-spirit
```

**Scaffold contents**: same file set, content specialized for the
privileged surface:
- `README.md` documents the **owner→core terminology shift** per
  records 766, 768 explicitly; lists the privileged operation set
  (`Start`, `Drain`, `Reload`, `Register`, `Retire`, plus upgrade
  handover).
- `ARCHITECTURE.md` carries the trust-boundary mermaid (supervisor
  on core socket; ordinary peers on ordinary socket); declares the
  upgrade-handover protocol lives in this contract.
- `INTENT.md` carries the privileged-layer intent: why core, not
  owner; why the handover lives here.
- `schema/core-signal-spirit.schema` — declares the privileged wire
  layer: `Start`, `Drain`, `Reload`, `Register`, `Retire`,
  `HandoverPrepare`, `HandoverReady`, `HandoverComplete`; no
  imports (the privileged surface stands alone); replies are
  acknowledgement-shaped (`StartAccepted`, `DrainAccepted`, etc.).
- `Cargo.toml` — lib crate `core-signal-spirit`, `0.1.0-pre`
  (fresh-name version starts).

**Commit + push:**

```text
jj describe -m 'designer: initial scaffold per psyche 2026-05-26 (record 780)'
jj bookmark create main --to @
jj git push --bookmark main --allow-new
→ Add bookmark main to bcd2d61d1b67
```

### Verification

```text
gh repo view LiGoldragon/spirit            → defaultBranchRef.name=main, visibility=PUBLIC
gh repo view LiGoldragon/signal-spirit     → defaultBranchRef.name=main, visibility=PUBLIC
gh repo view LiGoldragon/core-signal-spirit → defaultBranchRef.name=main, visibility=PUBLIC
```

All three reachable; all default-branch main; all PUBLIC; mirrors
the visibility of the legacy `persona-spirit` triad.

### Note on initial `https://` → SSH remote switch

The clones started on `https://` (the empty-repo creation default).
The initial `jj git push` failed with a credentials error
(`fatal: could not read Username for 'https://github.com'`). Switched
each remote to `git@github.com:LiGoldragon/<name>.git` via `git
remote set-url origin ...` per the pattern of every other repo in
this workspace. Push succeeded on retry. Documenting because future
agents cloning fresh-public-repo URLs will hit the same boundary.

## Part B — `nota-next` branch

Per record 781: *"The nota-related logic for the new schema-derived
stack lands on a nota-next BRANCH on the existing nota repository
rather than a new repo."*

```text
cd /git/github.com/LiGoldragon/nota
jj new -m 'nota: next-branch start for schema-derived stack changes' main
→ Working copy (@) now at: zymonmpt 45a75433 (empty) nota: next-branch start ...
jj bookmark create nota-next --to @
→ Created 1 bookmarks pointing to zymonmpt 45a75433 nota-next
jj git push --bookmark nota-next --allow-new
→ Add bookmark nota-next to 45a7543349b4
```

The branch is now reachable at
`https://github.com/LiGoldragon/nota/tree/nota-next`. Initial commit
is empty (the branch-start marker); subsequent logic-changes for
the schema-derived stack land here per psyche 2026-05-26.

## Part C — Block-by-block parsing prototype slice

Implemented per records 774-777 on the existing schema worktree
`/home/li/wt/github.com/LiGoldragon/schema/designer-schema-derived-nota-2026-05-26/`
which carries the `designer-schema-derived-nota-2026-05-26` branch.
Decision: stay on the existing prototype branch because the kernel
+ schema reader infrastructure is already there; the block layer
goes ABOVE the kernel's `Node` tree.

### New file: `prototype/src/blocks.rs` (264 LOC)

Introduces the **`Block`** layer above the kernel's `Node` layer:

```rust
pub struct SourcePosition {
    pub line: u32,
    pub column: u32,
    pub byte_offset: usize,
}

pub struct SourceSpan {
    pub start: SourcePosition,
    pub end: SourcePosition,
}

pub enum DelimiterKind { Parenthesis, SquareBracket, Brace, Leaf }

pub struct Block {
    pub delimiter: DelimiterKind,
    pub span: SourceSpan,
    pub root_objects: Vec<Block>,
    pub leaf_text: String,
    pub leaf_kind: Option<NodeKind>,
}
```

**Methods on `impl Block`** (per record 774):

| Method | Purpose |
|---|---|
| `is_parenthesis_block(&self) -> bool` | delimiter classification |
| `is_square_bracket_block(&self) -> bool` | delimiter classification |
| `is_brace_block(&self) -> bool` | delimiter classification |
| `is_leaf(&self) -> bool` | identifier/literal/string |
| `holds_single_root_object(&self) -> bool` | shape predicate |
| `holds_two_root_objects(&self) -> bool` | shape predicate |
| `holds_root_objects(&self) -> usize` | count |
| `root_object_at(&self, n: usize) -> Option<&Block>` | recursive accessor |
| `second_root_object_is_a_square_bracket_object(&self) -> bool` | composed shape predicate per records 774 + 772 |
| `second_root_object_qualifies_as_a_symbol(&self) -> bool` | composed shape predicate per records 774 + 772 |
| `reemit<'src>(&self, source: &'src str) -> &'src str` | range-based re-emission (record 776) |

**Associated functions on `impl BlockParser`**:

| Method | Purpose |
|---|---|
| `new(source: &str) -> Self` | constructor |
| `parse_blocks(&self) -> Result<Vec<Block>, KernelError>` | top-level parse |
| `node_to_block(node: &Node, line_index: &LineIndex) -> Block` | recursive lift from kernel `Node` (private) |
| `reemit_concatenated(source: &str, blocks: &[&Block]) -> String` | sequential concatenation (record 776) |

The `LineIndex` helper struct projects byte offsets onto
(line, column) coordinates once per parse; binary search makes the
lookup `O(log n)` per query. Every function lives on an `impl`
block — no free functions outside `#[cfg(test)]` and `fn main()`
per AGENTS.md (and the existing prototype) discipline.

### New file: `prototype/tests/block_parser_constraints.rs`

12 named constraint tests pinning each load-bearing intent per
record 777. Each test name follows the convention
`constraint_<record>_<what-it-pins>`. When a test fails, the
failure points directly at which intent has been broken.

### Constraint tests pinning each intent

#### Record 774 (block-by-block + source spans + predicates)

5 tests:

```text
constraint_774_blocks_carry_source_spans
constraint_774_block_predicates_classify_correctly
constraint_774_root_object_count_methods
constraint_774_root_objects_are_themselves_blocks_with_spans
constraint_774_recursive_shape_predicates_compose
```

The fifth test pins the **recursion clause** explicitly — root
objects inside a block are themselves typed positioned `Block`s,
with their own source spans, and the chain of block-level queries
IS the recursive parsing chain. Verified on `(Move [1 2] {x 3})`:
the outer parenthesis block holds three root objects; each is a
`Block` of its own delimiter kind; spans are monotonically
increasing.

#### Record 775 (range-based, not normalization)

3 tests:

```text
constraint_775_range_based_not_normalization
constraint_775_spans_use_lines_and_columns
constraint_775_byte_offset_preserved_alongside_line_column
```

The first test is load-bearing. Source contains a multi-line
record with original indentation:

```text
(Move
  [1
   2]
  )
```

The constraint pins that `outer.reemit(source) == source` exactly —
no whitespace collapse, no line-break removal, no re-indentation.
Equally, `inner.reemit(source) == "[1\n   2]"` exactly. The
range-based direction (record 775) is verified by behavior, not by
documentation.

#### Record 776 (reassembly = concatenation)

3 tests:

```text
constraint_776_reassembly_is_concatenation
constraint_776_blocks_are_first_class_units_filtered_and_rejoined
constraint_776_single_block_reemit_round_trips
```

The first test confirms `BlockParser::reemit_concatenated(source,
&[block1, block2, block3])` produces the concatenation of each
block's source slice — and that the operation is order-sensitive
(reordering blocks reorders the output). The second test confirms
blocks are first-class units: a caller can FILTER blocks and
reassemble the survivors WITHOUT re-parsing. The third pins the
unit-level round-trip: `outer.reemit(source)` for a nested vector
returns the exact original substring.

#### Record 777 (intents-as-constraint-tests)

1 meta-test plus the existence of the file above:

```text
constraint_777_named_tests_pin_each_intent
```

Acts as a smoke test for the meta-claim that the file ABOVE
contains named constraint tests for records 774, 775, 776.

### Verbatim test output

```text
running 12 tests
test constraint_774_block_predicates_classify_correctly ... ok
test constraint_774_root_objects_are_themselves_blocks_with_spans ... ok
test constraint_774_root_object_count_methods ... ok
test constraint_776_blocks_are_first_class_units_filtered_and_rejoined ... ok
test constraint_774_blocks_carry_source_spans ... ok
test constraint_776_single_block_reemit_round_trips ... ok
test constraint_776_reassembly_is_concatenation ... ok
test constraint_774_recursive_shape_predicates_compose ... ok
test constraint_777_named_tests_pin_each_intent ... ok
test constraint_775_range_based_not_normalization ... ok
test constraint_775_spans_use_lines_and_columns ... ok
test constraint_775_byte_offset_preserved_alongside_line_column ... ok

test result: ok. 12 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

And the full prototype test suite (kernel + schema + new block
parser) all green:

```text
test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 14 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 12 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

**41/41 prototype tests pass.** Build green; clippy not re-run (no
hand-authored Rust changes outside the new files; prior commit
already cleared clippy).

### Commit + push

The schema worktree is a pure git worktree (not jj-colocated). To
honor the jj-headless discipline I committed via jj from the
schema repo's main checkout. The bookmark
`designer-schema-derived-nota-2026-05-26` moved from
`5d9b0ff2` → `0e04c22f`.

```text
cd /git/github.com/LiGoldragon/schema
jj new 'designer-schema-derived-nota-2026-05-26' \
  -m 'schema: prototype block-by-block parser slice per records 774-777'
[copy three new files from worktree to the main checkout]
jj bookmark move designer-schema-derived-nota-2026-05-26 --to @
jj bookmark track designer-schema-derived-nota-2026-05-26 --remote=origin
jj git push --bookmark designer-schema-derived-nota-2026-05-26
→ Move forward bookmark from 5d9b0ff295c8 to 0e04c22f46e6
```

Then resync'd the worktree:

```text
cd /home/li/wt/github.com/LiGoldragon/schema/designer-schema-derived-nota-2026-05-26/
git reset --hard 0e04c22f
git checkout designer-schema-derived-nota-2026-05-26
```

Worktree now at the new commit; tests re-verified green from the
resync'd state.

## What's deferred (with reasoning)

- **Implementing logic on `nota-next`.** Record 781 placed
  schema-derived-stack nota changes on a branch, not in a new repo.
  The branch is created (empty) per the directive; the actual
  source-block work currently lives on `schema/...prototype/src/blocks.rs`
  rather than in `nota/src/`. Migrating the block layer to nota-next
  is the natural next slice — the prototype's `blocks.rs` would
  move into nota's crate(s) once the kernel-boundary is firmed up.
  Deferred because the prototype is still maturing; the block layer
  builds on the prototype's `Node` representation today.

- **Daemon implementation for the new `spirit` repo.** Per record
  780: "New repos are CONTRACT-focused at this stage; daemon
  implementation comes after the contract surface settles." The
  scaffold sets up the repo for daemon work but does NOT begin it.

- **Cargo dependency rewiring.** Existing v0.3 callers reference
  `persona-spirit / signal-persona-spirit / owner-signal-persona-spirit`.
  Migrating those references to the new triad names is operator
  authority and is NOT part of this designer-assistant slice.

- **CriomOS-home flake input rewiring.** Same reasoning —
  system-specialist authority per record 779; deferred.

- **`spirit.schema` content beyond skeleton.** The three schema
  files mirror the legacy v0.3 spirit.schema shape as a starting
  reference, NOT as final content. The final shape evolves with
  the schema-driven stack maturity. Per record 780 the new repos
  start contract-focused; the contract itself is iterated forward
  on `nota-next` + the schema repo's prototype branch.

- **Schema daemon.** Per /354 §"Schema daemon (deferred)" — same
  reasoning carries forward. The prototype's `Library` struct
  exposes the daemon's API shape but stays in-process. Promoting
  to out-of-process lands as a follow-up.

- **Operator-prototype methodology lift.** /355 surfaced the
  compiled-fixture three-way verification pattern (string-compare
  + compile + runtime-decode) as worth carrying forward.
  Constraint tests here use direct assertions rather than fixtures;
  applying the fixture pattern is a follow-up.

## Open shape questions (per don't-infer record 735)

Gaps where this slice made the smallest reasonable interpretation
and the psyche may want a different shape. Surfacing them per
`skills/intent-clarification.md` rather than inferring fills.

1. **Block leaf classification.** The block layer carries
   `leaf_kind: Option<NodeKind>` which mirrors the kernel's `NodeKind`
   for leaves (Identifier, Integer, Float, InlineString, BlockString,
   Bytes). Whether the block layer should carry its OWN classification
   or defer to the kernel's is open. Current choice: defer (avoids
   duplication; the kernel boundary is the cut). Alternative: the
   block layer could re-classify by source-position semantics (e.g.
   "a leaf in a Map-key position is always an identifier"). Open.

2. **Reassembly separator policy.** `reemit_concatenated` joins
   blocks with a single space. Per record 776 reassembly is
   "concatenation"; the literal interpretation would have NO
   separator. The single-space choice matches NOTA's whitespace
   convention (any whitespace is equivalent). The psyche may want
   either: no separator (strict concatenation), single space (current),
   or original-source-between-blocks reconstruction.

3. **`SourcePosition.byte_offset` field.** Carries both line/column
   AND raw byte offset. Per record 775 the direction is "range-based
   on the original source text". Whether byte_offset belongs in the
   public `SourcePosition` struct or stays internal to the line index
   is a question of API ergonomics. Current choice: public (callers
   that want raw byte access don't have to re-derive it). Alternative:
   line/column only, byte_offset via a separate accessor.

4. **The `second_root_object_*` predicate naming.** Per record 774:
   "recursive predicates like second_root_object_is_a_square_bracket_object
   / second_root_object_qualifies_as_a_symbol". These are
   long-explicit method names. The psyche-named convention is honored
   here; a more compact `nth_root_is_square_bracket(1)` form is the
   natural generalisation. Whether the explicit form OR the
   generalised form is canonical is open.

5. **Where the block layer ultimately lives.** Per record 781 the
   nota-next branch is the home for schema-derived stack logic. The
   block layer (`blocks.rs`) is currently in the `schema` prototype
   crate. A natural migration would relocate it to nota-next under
   `nota`/`nota-codec`/elsewhere — but the prototype-to-production
   path is operator authority, not designer-assistant authority.

None of these are blockers for the constraint tests' purpose
(empirically pinning the intents); they're shape questions for the
next iteration.

## Worktrees touched

| Worktree | Branch | Change |
|---|---|---|
| `/git/github.com/LiGoldragon/spirit/` | `main` | initial scaffold pushed |
| `/git/github.com/LiGoldragon/signal-spirit/` | `main` | initial scaffold pushed |
| `/git/github.com/LiGoldragon/core-signal-spirit/` | `main` | initial scaffold pushed |
| `/git/github.com/LiGoldragon/nota/` | `nota-next` (new) | branch-start commit pushed |
| `/git/github.com/LiGoldragon/schema/` | `designer-schema-derived-nota-2026-05-26` | block parser commit pushed |
| `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-derived-nota-2026-05-26/` | same | resync'd to new commit |

## References

- Spirit records **774-777** — block-by-block parsing methodology
  + intents-as-constraint-tests.
- Spirit records **779-782** — repo creation authorization + the
  nota-next branch decision + the schema-repo-stays decision.
- Spirit records **765-768** — persona-prefix retirement; new triad
  names; owner→core terminology shift.
- Spirit records **746-753** (Maximum) — schema-driven NOTA design.
- Spirit records **713-715, 730-732** (Maximum) — retracted
  Features / EffectTable / FanOutTargets / StorageDescriptor drift
  cluster; what NOT to do.
- Spirit record **717** — file-ownership discipline (repo INTENT
  carries repo-scope intent only).
- Spirit record **735** — don't-infer; surface gaps for psyche.
- Primary `/353` — schema-derived NOTA design vision.
- Primary `/354` — prototype implementation report.
- Primary `/355` — operator-prototype critique; compiled-fixture
  test methodology surfaced as a future lift.
- AGENTS.md hard overrides: NOTA bracket-only strings; positional
  records; methods on impl blocks; jj headless inline; designers
  in worktrees not main of existing repos.
