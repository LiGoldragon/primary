# ProtosEngine Overnight Morning Report — 2026-08-02

This is the single morning report required by
[`handoffs/codex-overnight-2026-08-01.md`](/home/li/primary/handoffs/codex-overnight-2026-08-01.md).
It reports published component work separately from integration into each
repository's `main` and from integration into the ProtosEngine root.
Branch and bead state was last revalidated at 2026-08-02 07:18 CEST.

## 1. Built work and test results

**Current state.** `primary-36y` is closed, `primary-pjm` is blocked,
`primary-zjo` is closed, and umbrella tuple-remediation bead `primary-wgd` is
open. All feature heads named below are published at their remote bookmarks
except the unchanged `language-engine-witness` lane, whose local feature
bookmark still equals repository `main`. None of the feature heads is an
ancestor of its repository's current `main`; the work is published for review
and integration, not landed on component mains. ProtosEngine `main` remains at
`99d26f14da9c6437f5a3e1589f3b2f0bcaaa02dc`.

| Surface | Published feature head | Repository `main` | Result |
| --- | --- | --- | --- |
| ScopeOf target, `signal-domain` | `ScopeOfTraitTarget20260802` at `fbc400bf5ed5e4c4d27ef4e76cb48fa4e5d53658`, version 0.2.0 | `1890f33174f3637b2d605b9c79e584e127580d13` | Seven contract traits and the handwritten Domain/Scope reference implementation; A1-A18 are visible at their sites. |
| Slice 1 root integration, `protos-engine` | `ProtosOvernightIntegration20260802` at `d54e271f0d098061146435a6f6e13f93a828e9d7`; the Slice 1 integration commit is its parent `a3dc7fa3930e1dd98fdf6629dc42149399a7adb6` | `99d26f14da9c6437f5a3e1589f3b2f0bcaaa02dc` | Pins only the ScopeOf `signal-domain` head and adds the cross-repository fixture witness. The current head additionally places the requested capsule supersession banner in the compiled design. This is the only overnight component slice integrated into a ProtosEngine feature root. |
| Types-only Ethos and its tuple cleanup, `core-ethos` | `TypesOnlyEthos20260802` at `7bb9c5a0a31851641998b26f14326515ca64a7e8`, version 0.23.0; the Slice 2 root itself entered at `78c9530782652af40493b1a0ca22397782560bf7` | `736460fdafbd65d6500fe15e6ae8844b42a39e7c` | One types-only root through the common codec, neutral API names, then archive-witnessed named-field remediation. Published, not integrated into the language witness or ProtosEngine. |
| Tuple-clean Logos producer, `core-logos` | `TupleNamedFields20260802` at `1bb284325d3026a695130967215373fa266629d5`, version 0.20.0 | `9a61e2ac1bf8a8c1163794d695902115a05a4007` | Registered WholeLogos carriers use named fields with retained archive evidence. |
| Tuple-clean Rust projection, `rust-logos` | `TupleNamedFields20260802` at `aa75cf6afdd457bb256ceb955ca78cca54d0e484`, version 0.20.0 | `f46167cbb35d25d86ddbc197653c6560ded8e077` | Dependency-only coherent repin to the tuple-clean Logos producer. |
| Types-only, tuple-clean, ScopeOf pre-gate stack, `core-nomos` | `TypesOnlyEthos20260802` at `ee90fd7159ffb5ac711e0d888a5e658436352440`, version 0.31.0 | `58fd8036bffcb3cff6e27af4db25690764ecc768` | Contains the types-only Ethos repin, archive-witnessed named fields, the coherent current producer train, and Slice 3's non-recursive ScopeOf plan. |
| Current Nomos signal, `signal-nomos` | `TypesOnlyEthos20260802` at `d5b102c339612e68e357a34792b016af3af5254f`, version 0.6.0 | `1af71a9d0625a6404f81cd6fe8b6393ac0c9040f` | Dependency-only repin to the coherent current Nomos train; its d47 compatibility dependency remains separate. |
| Current Nomos engine, `nomos-engine` | `TypesOnlyEthos20260802` at `7f56a5bd93f29a7b4a2fafe73ce9ce72ae75edd9`, version 0.6.0 | `e4230f62b55fcf8543477a26d272862a63aa1fc3` | Coherent repin plus archive-witnessed conversion of the three registered forged carriers. |
| Language integration witness | No new published feature head; local `TypesOnlyEthos20260802` still names `edbf506f2befd2ee756ecdf22e28fd09e53017e7`, the same commit as `main` | `edbf506f2befd2ee756ecdf22e28fd09e53017e7` | Slice 2, Slice 3, and the tuple-clean train have not crossed this integration boundary. |

**Tests that passed.**

- The ScopeOf target passed the focused Domain contract suite, 10/10; the
  three dependency-boundary tests; documentation tests; formatting; full
  all-target/all-feature Clippy; its focused Nix test derivation; and full
  `nix flake check`. The ProtosEngine Slice 1 feature root passed flake
  evaluation, the focused `scope-of-target-witness`, full `nix flake check
  --print-build-logs`, and `nix run .#check-all`. The witness byte-compared the
  pinned `signal-domain/schema/domain.schema` and
  `language-engine-witness/tests/fixtures/spirit-domain.ethos`; both had SHA-256
  `f671462eee55f82ead6feaece69b91e1c7a8bbccf13cd9e94a4a0a6c12d65b15`.
  Those gates were recorded at integration commit `a3dc7fa393...`. The current
  `d54e271f0d09...` head changes only the compiled design document by adding a
  capsule supersession banner; no separate build rerun is recorded for that
  documentation-only descendant.
- The original types-only producer commit passed 23/23 all-target tests,
  including 10/10 `whole_ethos` tests, plus formatting, warning-denied Clippy
  and rustdoc, focused Nix test, and full Nix flake check. Its current published
  head passes 24/24 all-target tests and all eight Nix checks after the
  registered tuple cleanup.
- The six-repository current producer chain was independently checked at
  `core-ethos` `7bb9c5a0...`, `core-logos` `1bb28432...`, `rust-logos`
  `aa75cf6a...`, `core-nomos` `6470efc1...`, `signal-nomos` `d5b102c3...`, and
  `nomos-engine` `7f56a5bd...`. Focused archive and golden suites passed;
  locked all-target counts were respectively 24, 40, 15, 98 with one
  intentional generator ignore, 8, and 17 with one intentional generator
  ignore. Formatting, warning-denied Clippy and rustdoc, flake checks, and
  explicit Nix build/test/doc/fmt/clippy gates passed in all six repositories.
- Slice 3 advanced `core-nomos` from the audited producer head to
  `ee90fd7159ffb5ac711e0d888a5e658436352440`. Its focused ScopeOf and boundary
  suites passed 9/9; the full crate passed 107 active all-target tests with one
  pre-existing ignored freezer witness; formatting, warning-denied Clippy and
  rustdoc, flake evaluation, full `nix flake check`, and the five explicit Nix
  build/test/doc/fmt/clippy derivations passed.

**Failures, corrections, and incomplete integrations.**

- A reversible Slice 2 consumer experiment removed the five inferable empty
  positions from `signal-domain/schema/domain.schema`, leaving the populated
  types block byte-identical. Its actual generator failed in `build.rs` with
  `Schema(ExpectedRootObjectCount { expected: "6 root slots (imports input
  output types generics impls)", found: 1 })`. The file was restored exactly;
  the restored baseline passed 10/10 focused tests and full flake check. No
  failed experiment was committed or pushed.
- Slice 3's first Nix run failed because a test tried to include
  `NON_IDEAL_AGENTS.md`, which the filtered crate source intentionally omits.
  The test was corrected to inspect the production boundary without requiring
  that documentation in the package source; the complete Nix gate then passed.
- An intermediate `core-nomos` dependency shape at `326ffd818d...` introduced
  simultaneous core-logos 0.19 and 0.20 type universes. The published
  correction `4453dfd9b16e699b9050c9fb7cd28096d8bda7a5` removed that alias and
  restored one coherent 0.19 universe. The later coherent train moved the
  entire consumer chain to core-logos 0.20. The intermediate dual-universe
  claim is superseded and must not be treated as the current result.
- `language-engine-witness` was not repinned, and the ProtosEngine feature root
  still pins the pre-overnight `core-ethos`, `core-logos`, `rust-logos`,
  `core-nomos`, `signal-nomos`, and `nomos-engine` revisions. Therefore Slice 2,
  Slice 3, and the tuple-clean producer train are not yet integrated even
  though their component bookmarks are published and green.

## 2. Complete assumption register with sites

The authoritative starting register is the
[`ScopeOf Salvageability Assessment`](/home/li/primary/reports/ScopeOfSalvageabilityAssessment-2026-08-01.md).
The implementation scan found exactly its A1-A18 labels in the ScopeOf target,
the three `primary-pjm` labels in the types-only producer, and the eleven
`primary-zjo` labels in the pre-gate transformer. A19 remained an assessment
assumption and was then made concrete as `primary-pjm-A1`. No additional
`[assumption]` label exists in the changed implementation surfaces. Trait
exception notes, archive-layout equivalence, exact pin selections, and test
expectations are not silently counted as assumptions: they are respectively
auditable standard exceptions, proved observations, published integration
facts, and witnesses.

**ScopeOf assessment A1-A19.**

| Assumption | Exact provisional choice | Site |
| --- | --- | --- |
| A1, contract decomposition and names | `ScopeOf`, scope containment, overlap, filtering, and scope-domain matching are distinct contracts with the implemented provisional method names. | Assessment; [`signal-domain/src/scope.rs`](/home/li/wt/github.com/LiGoldragon/signal-domain/ScopeOfTraitTarget20260802/src/scope.rs) lines 3-41. |
| A2, trait ownership | The first witness's local Domain/Scope owner also owns the seven traits; there is no claim that `signal-domain` or `core-nomos` is the permanent universal owner. | Assessment; `signal-domain/src/scope.rs` line 4. |
| A3, coherent relation operands | Scope-to-scope relations compare members of the same contracted Scope family; cross-family relations wait for a named conversion contract. | Assessment; `signal-domain/src/scope.rs` line 17. |
| A4, total structural projection | The first Domain-to-Scope projection is total and structure-preserving, including Domain `All` to Scope `All`. | `signal-domain/src/scope.rs` line 44; [`tests/domain_contract.rs`](/home/li/wt/github.com/LiGoldragon/signal-domain/ScopeOfTraitTarget20260802/tests/domain_contract.rs) lines 64-79. |
| A5, root `All` attached to all four relations | Root Scope `All` contains, overlaps, filters, and scope-domain-matches every relevant value. | `signal-domain/src/scope.rs` lines 51, 67, 76, and 89; relation matrix tests. |
| A6, containment against root `All` | A non-`All` scope does not contain or directionally filter root Scope `All`. | `signal-domain/src/scope.rs` lines 52 and 77; containment and filtering tests. |
| A7, containment reflexivity | Every materialized scope contains itself; overlap and filtering inherit the corresponding true cell. | `signal-domain/src/scope.rs` line 53; containment, overlap, and filtering tests. |
| A8, ancestor containment | An ancestor scope contains a strict descendant. | `signal-domain/src/scope.rs` line 54; containment, overlap, and filtering tests. |
| A9, reverse containment | A strict descendant does not contain or filter its ancestor. | `signal-domain/src/scope.rs` line 55; containment and filtering tests. |
| A10, unrelated containment | Unrelated siblings do not contain, overlap, or filter one another. | `signal-domain/src/scope.rs` line 56; all three scope-relation tests. |
| A11, overlap symmetry | Scope overlap is symmetric and true exactly when either operand contains the other. | `signal-domain/src/scope.rs` line 68; overlap matrix test. |
| A12, filtering direction | `matches_scope(filter, candidate)` follows directional containment but remains a distinct contract. | `signal-domain/src/scope.rs` line 77; filtering matrix test. |
| A13, exact scope-domain match | A scope matches a domain at the same structural location. | `signal-domain/src/scope.rs` line 90; scope-domain matrix test. |
| A14, ancestor scope-domain match | An ancestor scope matches a strict descendant domain. | `signal-domain/src/scope.rs` line 91; scope-domain matrix test. |
| A15, reverse scope-domain match | A strict descendant scope does not match an ancestor domain. | `signal-domain/src/scope.rs` line 92; scope-domain matrix test. |
| A16, unrelated scope-domain match | A scope does not match a domain on an unrelated branch. | `signal-domain/src/scope.rs` line 93; scope-domain matrix test. |
| A17, domain-side `All` | Every materialized scope matches Domain `All`; this preserves historical behavior but is not psyche-ruled. | `signal-domain/src/scope.rs` line 84; scope-domain matrix test lines 220-252. |
| A18, nested `All` | If representable, a nested Scope `All` covers its local subtree rather than the entire root tree; whether nested `All` should exist remains open. | `signal-domain/src/scope.rs` lines 57 and 94; projection, containment, and scope-domain tests. |
| A19, minimal Ethos witness root | The first six-slot replacement is a types-only root through the same structural machinery; its record shape and delimiters were initially open. | Assessment only; concretized by `primary-pjm-A1` below. |

**Slice 2 assumptions `primary-pjm-A1` through `primary-pjm-A3`.**

| Assumption | Exact provisional choice | Site |
| --- | --- | --- |
| `primary-pjm-A1`, types-only root shape | The first Ethos file kind is a one-member ordered product whose sole types role delegates to the existing non-empty brace-delimited item list. The expected root identity selects the kind; the author writes no tag and no empty slots. | [`core-ethos/src/whole.rs`](/home/li/wt/github.com/LiGoldragon/core-ethos/TypesOnlyEthos20260802/src/whole.rs) lines 587-618; [`tests/whole_ethos.rs`](/home/li/wt/github.com/LiGoldragon/core-ethos/TypesOnlyEthos20260802/tests/whole_ethos.rs) lines 20-27. |
| `primary-pjm-A2`, decoded-mirror round trip | The exact evaluator-produced structural mirror is retained beside the decoded `WholeEthos` so the same sealed table can render it; this avoids inventing an independently authored reverse projection in the slice. | `core-ethos/src/whole.rs` lines 1250-1264; `tests/whole_ethos.rs` lines 398-410. |
| `primary-pjm-A3`, neutral API naming | The common codec is named `EthosCodec` and related public names are arity-neutral; the slice introduces neither a file-kind enum nor a parallel per-kind parser API. | `core-ethos/src/whole.rs` lines 695-701; `tests/whole_ethos.rs` lines 401-405. |

**Slice 3 assumptions `primary-zjo-A1` through `primary-zjo-A11`.**

| Assumption | Exact provisional choice | Site |
| --- | --- | --- |
| `primary-zjo-A1`, local contract ownership | `core-nomos` locally owns the six pre-gate ScopeOf contracts for declaration content, recognition, resolution, planning, realization, and gate observation. | [`core-nomos/src/scope_of.rs`](/home/li/wt/github.com/LiGoldragon/core-nomos/TypesOnlyEthos20260802/src/scope_of.rs) lines 15-66. |
| `primary-zjo-A2`, exact typed application recognition | A declaration is recognized only as a typed WholeEthos newtype application whose head equals the configured ScopeOf identity; unrelated items return no match without spelling inspection. | `core-nomos/src/scope_of.rs` lines 143-157. |
| `primary-zjo-A3`, malformed matching form refuses | Once the head is the exact ScopeOf identity, a payload that is not one source identity is a typed `SourceOperandNotIdentity` refusal rather than an unrelated item. | `core-nomos/src/scope_of.rs` lines 159-171. |
| `primary-zjo-A4`, one-root-level planning | Planning validates the source's exact identity and prepares only its root enumeration; it does not descend into child domains. | `core-nomos/src/scope_of.rs` lines 216-228. |
| `primary-zjo-A5`, unresolved name dependency | Each planned output variant carries only a promise keyed by the source variant identity. That promise is not treated as a generated visible name or true identity. | `core-nomos/src/scope_of.rs` lines 281-287 and 349-362. |
| `primary-zjo-A6`, admitted one-level payload shapes | Root planning accepts unit variants and exactly one identity-bearing positional child. A different field count or an application child refuses with a typed error. | `core-nomos/src/scope_of.rs` lines 258-278. |
| `primary-zjo-A7`, visibility and source order retained | The plan copies public/private visibility and keeps variants in source order. | `core-nomos/src/scope_of.rs` lines 251-287. |
| `primary-zjo-A8`, source carries root `All` | The source enumeration must contain exactly one configured root `All`; planning neither synthesizes nor silently deduplicates it. | `core-nomos/src/scope_of.rs` lines 230-249. |
| `primary-zjo-A9`, existing WholeLogos mirror target | The stopped realization contract provisionally names the existing `WholeLogosEnumeration` as its return target, although the implementation constructs no value before identity is supplied. | `core-nomos/src/scope_of.rs` lines 54-62 and 297-311. |
| `primary-zjo-A10`, child edge is not traversal | A payload-bearing variant records a typed source-domain dependency and exposes a recursion gate; it does not resolve or traverse the child. | `core-nomos/src/scope_of.rs` lines 268-271 and 363-387. |
| `primary-zjo-A11`, translator-only identity allocation | The transformer never allocates output identities; every planned output stops at a typed generated-identity gate owned by the future translator/operation boundary. | `core-nomos/src/scope_of.rs` lines 282-287, 297-311, and 378-383. |

## 3. Gate encounters

**The types-only canonical-source bridge blocked Slice 2.** The new
`core-ethos` root proves that a one-position types-only file can use the shared
structural codec with no per-kind parser. The live `signal-domain` generation
path does not consume that root. It goes through pinned `schema-rust` and
`schema-language` code whose `SchemaDocumentLayout` requires exactly six root
positions. Removing only the five inferable empty positions produced the typed
failure reported in section 1. There is no ruled typed bridge from the legacy
six-slot `TrueSchema` source to current `core_ethos::WholeEthos`. Consequently
`primary-pjm` is correctly blocked: the producer exists, but calling Slice 2
integrated would require either making the types-only form canonical and
adapting the upstream generator path, or authorizing a temporary compatibility
bridge and naming which representation is authoritative.

**The language witness and ProtosEngine root did not integrate the new train.**
The language witness lane still equals its old `main`. The ProtosEngine feature
root pins only the new `signal-domain`; it deliberately retains old revisions
for `core-ethos`, `core-logos`, `rust-logos`, `core-nomos`, `signal-nomos`, and
`nomos-engine`. Moving those pins before resolving the canonical-source bridge
would either preserve two contradictory source authorities or require an
unruled conversion. A safe eventual integration must update the normal and
compatibility dependency universes coherently, advance the exact-pin policy and
lock together, run the language witness across its daemon restart boundary,
and only then advance the ProtosEngine root witness.

**Slice 3 stopped at generated-output identity.** Recognition and exact source
resolution work, and one root-level Nomos mirror can be planned. Every output
variant still needs a true identity supplied by the translator/atomic-operation
boundary. The current `ScopeOfVariantNamePromise` records the source variant on
which future identity depends; it does not decide a name, derive an identity,
create a slot, or append to a change log. Concrete realization therefore always
returns `GeneratedOutputIdentityRequired` before constructing a
`WholeLogosEnumeration`. Implementing beyond this point would have violated the
overnight hard stop and the same-true-name law.

**Child relationships reached both the recursion and dependency-DAG gates.** A
one-field payload records a child-domain dependency and exposes a typed
`RecursiveDescent` gate; it never follows the edge. The seated DAG law says
dependencies determine topological evaluation, affected transformations run
exactly once, cycles are typed errors, and fixpoint iteration is forbidden.
What is still missing is the sanctioned representation that turns a child edge
or a dependency on a generated symbol into a graph edge and schedules it. The
existing `RecursiveInvoke` implementation was neither called nor extended and
is not validated by this slice.

**The existing Logos target is too narrow for full ScopeOf realization.** The
handwritten mirror currently targets one `WholeLogosEnumeration`. The worked
ScopeOf target also needs the complete reviewed family of relations, traits,
implementations, conversions, and any functions that embody the ScopeOf
contract. The current Logos vocabulary and output-role model do not yet state
that full family. The slice therefore proves recognition and pre-gate planning,
not the complete Domain-to-Scope transformation.

**Tuple remediation crossed the archive gate but not historical closure.**
Archive-compatibility witnesses were written before converting every registered
archived carrier, including non-empty and recursively meaningful values. At the
current six-repository producer heads, all 27 registered multi-field tuple
declarations are absent: 25 are named-field declarations and the two obsolete
six-slot declarations disappeared with the new root. The misleading
`*Newtype` carriers now have semantic named fields rather than merely renamed
types. This completes only the registered declaration slice.

`primary-wgd` remains open for 52 current explicit tuple-type nodes and other
ad-hoc tuple syntax; the language witness's atomic normal/dev repin; the
ProtosEngine root, pin-policy, and coherence update; and the disposition of
legacy code that still participates in live checks. In particular,
ProtosEngine actively builds four historical inputs:
`sealed-core-nomos` at `ba7abc0b471a0385012b1d8a03cf4942e9da617e`,
`template-core-logos` at `141abe23273273d2e4470ce15b42ccf9bc5c8764`,
`template-rust-logos` at `96eda934a8f3203295f0a08869199441f109c369`, and
`equivalent-core-nomos` at `e1b2febf9f143ab1c84d042d2e9bdd0685303ddc`.
`signal-nomos` also compiles an old d47 `core-nomos` solely as a refusal
witness. The Rust tuple law has no historical-source exception on record, but
deleting or rewriting compatibility witnesses without deciding their authority
could erase evidence. That is a psyche gate, not a mechanical omission.

## 4. Ranked questions for the psyche

1. **Which source representation is canonical for the new types-only Ethos
   file kind?** The published producer reads a single brace-delimited types
   position through the common structural codec. The current Domain generator
   reads a legacy six-position schema source and rejects the one-position form
   before code generation. If the types-only Ethos form is canonical, the next
   work must adapt the `schema-language`/`schema-rust` generation boundary and
   then repin consumers. If the old schema source remains canonical for now,
   Slice 2 needs explicit authority for a temporary typed bridge, including
   which side owns meaning and whether the bridge may exist only at the
   compatibility boundary. Without this ruling, `primary-pjm` cannot honestly
   integrate.

2. **How does the translator assign stable true identity to each output of a
   transformation?** ScopeOf can produce a root and many variants, and later
   transformations can depend on those generated symbols. The current plan
   knows the authored target identity and each source variant identity but stops
   before inventing an output identity. Please rule what information forms an
   output's identity, when the translator allocates or resolves it, how repeated
   evaluation recognizes the same true thing, and how that act participates in
   the engine's atomic operation and change log. This answer unlocks concrete
   Logos realization without granting the transformer naming authority.

3. **How should a transformer express variable-depth child work under the DAG
   law?** A ScopeOf source variant can refer to a child Domain, which can refer
   to another. The present slice records the child edge and stops. Please rule
   whether the generic dependency graph itself expands that chain as separately
   keyed transformation nodes, or whether there is a sanctioned recursion
   contract inside one transformation. The answer must say how dependencies on
   generated symbols enter the graph, how topological once-only evaluation is
   preserved, and what typed refusal represents a cycle. No fixpoint option is
   being proposed.

4. **What complete typed Logos family must ScopeOf emit?** The current stopped
   mirror can describe one output enumeration, while the reference target also
   exposes projection, containment, overlap, filtering, and scope-domain
   matching behavior. Please name which traits, implementations, conversions,
   inherent functions, or other Logos objects are part of the required result,
   and which are merely temporary reference conveniences. This determines the
   output-role vocabulary and prevents the enumeration carrier from becoming a
   ScopeOf-specific shortcut.

5. **Which of the ScopeOf target assumptions A1-A18 should become law, and
   which should change?** The implementation currently separates seven traits;
   keeps their ownership local; permits only same-family relations; makes
   projection total; gives root `All` whole-tree behavior across all four
   relations; makes containment and filtering directional; makes overlap the
   symmetric union of containment; lets every scope match Domain `All`; and
   treats a representable nested `All` as local to its subtree. The root Scope
   `All` meaning itself is already ruled. The open choices needing confirmation
   are the API decomposition and owner, reflexivity and operand direction,
   Domain-side `All`, and whether nested `All` exists and is local. These choices
   are already executable at the published reference head, so accepting or
   correcting them now avoids building the transformer against an accidental
   truth table.

6. **Are the three types-only producer assumptions acceptable as the bootstrap
   form?** The provisional root is exactly one inferred types position selected
   by expected root identity; the runtime retains the evaluator's structural
   mirror to render through the same table; and the public API uses neutral
   `EthosCodec` naming without a file-kind enum. Please confirm whether the
   retained mirror is the right bootstrap reverse path or should be replaced by
   another typed derivation, and whether expected identity alone is sufficient
   to select the file kind. This is separate from deciding which downstream
   source is canonical.

7. **Does the no-tuples Rust law require tuple-free historical and refusal
   witnesses that are still compiled, or may frozen compatibility sources be an
   explicit exception?** The current producer declarations are clean and their
   old archive bytes remain proven. Absolute closure is blocked by four
   historical ProtosEngine inputs, the d47 old-reader refusal dependency, and
   remaining generated/ad-hoc tuple types. If compiled history must obey current
   source law, those witnesses need replacement or forward-porting while their
   evidence is preserved. If frozen historical source may retain tuples, please
   define that exception narrowly: whether it applies only to immutable
   compatibility revisions, whether they may remain active build inputs, and
   what proof must prevent their types from leaking into the current universe.

8. **After the rulings above, should integration land as one coherent train or
   as separately reviewed main landings followed by an atomic root repin?** The
   component bookmarks are published and green, but no component `main`
   contains them and the language witness and ProtosEngine root remain old. A
   single train minimizes mixed type universes; separate landings make each
   semantic change easier to review but temporarily leave published mains that
   cannot yet compose. The integration must in either case update the language
   witness's normal and compatibility pins together, prove daemon restart and
   refusal behavior, then update the ProtosEngine exact-pin policy and lock in
   one root commit.
