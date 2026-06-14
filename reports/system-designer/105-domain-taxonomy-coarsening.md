# 105 — Coarsening the Domain taxonomy: broad-field curation over the over-specified Software subtree

*The psyche: "the domain became over specified, some of those domains look more
like referents." This is the deeper cut beneath report 104's naming audit — 104
fixed names assuming every leaf stays; this questions whether the leaves should
exist. The psyche chose the fix: keep the 12 Software sub-domains as branches,
keep only a curated set of genuinely-broad-field leaves under each, cut the rest
down to referents/keywords. Method: a 13-curator adversarial workflow (one
skeptic per sub-domain, biased toward cut), grounded in a full live-store usage
census. Result: **42 leaves kept from 211 — 80% pruned.***

## The principle (what "looks like a referent" actually means)

The Spirit intent system has three retrieval layers, and the closed `Domain`
enum is only the first:

- **Domains** — the *closed* taxonomy: broad routing buckets.
- **Referents** — the *open*, auto-registering layer of named particulars
  (`spirit`, `rkyv`, `DeepSeek`, a host, a bead).
- **Keywords** — *free text* in the description, queried by `KeywordMatch` /
  `ContainsText`: narrow concepts.

The `Technology>Software` subtree over-built the *closed* layer into ~200 fine
leaves doing the open layers' job. Sharpening the psyche's wording: most of these
aren't proper-noun particulars, so strictly they're keyword-bound **concepts**,
not referents — but the diagnosis is identical: **they don't belong in the closed
routing enum.** The census proves it: **113 of 211 leaves (54%) have zero
records**; the traffic piles onto a handful of broad subjects.

This honors existing intent — [split only when query results prove noisy]
(`skills/intent-log.md`): start lean, promote a leaf back on evidence. The
keyword layer loses nothing (still fully queryable), so cutting is cheap and
reversible; over-keeping perpetuates the over-specification.

## The curated Technology subtree

42 kept leaves, ancestry-stripped names (per 104), term-of-art compounds whole.
`Languages` renamed to `Programming` (104). Each sub-domain is now **terminal-able**
(a record may tag just the sub-domain) and **branchable** (or tag a curated leaf).

```
(Technology
  (Hardware [Networking])
  (Software
    (Programming   [TypeSystems Compilation Parsing Grammars CodeGeneration Metaprogramming Macros DomainSpecificLanguages])
    (Theory)                          ;; terminal-only: zero kept leaves
    (Systems       [SystemsProgramming Concurrency])
    (Distributed   [ProtocolDesign EventDrivenArchitecture])
    (Data          [Persistence Serialization Formats Modeling SchemaEvolution Migration])
    (Intelligence  [AgentSystems])
    (Security      [Cryptography Authentication Authorization SecretsManagement Privacy])
    (Quality       [Testing])
    (Operations    [BuildSystem ReleaseEngineering DependencyManagement Deployment ConfigurationManagement])
    (Observability [Tracing])
    (Surfaces      [Visualization CommandLineInterfaces])
    (Engineering   [Architecture Design ApplicationProgrammingInterfaces Documentation VersionControl DevelopmentProcess Management Modularity])))
```

Per-sub-domain tally: Programming 8, Engineering 8, Data 6, Security 5,
Operations 5, Systems 2, Distributed 2, Surfaces 2, Hardware 1, Intelligence 1,
Quality 1, Observability 1, **Theory 0**.

## How this resolves report 104

104's leaf-level work is largely *subsumed*, not contradicted:
- **Most of 104's 87 renames evaporate** — you don't rename `DataPipelines`→
  `Pipelines` when the leaf is cut. Only the **42 survivors** carry the ancestry
  strip, which this curation already applied (`SoftwareArchitecture`→`Architecture`,
  `DataModeling`→`Modeling`, `DataFormats`→`Formats`, `SoftwareDevelopmentProcess`→
  `DevelopmentProcess`, `SoftwareEngineeringManagement`→`Management`).
- **104 structural call #1 (flatten `Engineering`?) → resolved: keep.** It earns
  its place as a sub-domain with 8 curated leaves.
- **104 structural call #2 (`Quality>Testing` sub-layer?) → dissolved.** `Testing`
  becomes a single terminal-able curated leaf; `Unit`/`Integration`/`EndToEnd`
  become keywords. Simpler than a sub-layer — the over-specification the sub-layer
  was working around is just gone.
- The term-of-art guard from 104 carried through: `TypeSystems`,
  `DomainSpecificLanguages`, `SystemsProgramming`, `EventDrivenArchitecture`,
  `SchemaEvolution`, `ApplicationProgrammingInterfaces`, `CommandLineInterfaces`,
  `ConfigurationManagement` kept whole.

## The enum-shape change (the design is half-built already)

The taxonomy is a **dual enum family** in `signal-spirit/src/schema/domain.rs`
(3801 lines): **39 value enums** (stored in a record's `Domains`) mirrored by
**39 `*Scope` enums** (used in queries). The query side *already* models
"the whole sub-domain": **38 of 39 `*Scope` enums carry an `All` variant**. The
value side has no terminal — which is exactly why a stored record can't stop at
`(Technology Software)`. So "terminal-able sub-domain" is **giving the stored
value the terminal-ability the query side already has**, then pruning each
sub-enum to its curated leaves.

Concrete shape — each sub-domain carries an `Optional` curated-leaf payload (bare
atom = terminal, `(Sub Leaf)` = curated); a fully-cut sub-domain is a unit
variant:

```
enum Technology { Hardware(Option<HardwareLeaf>), Software(SoftwareScope) }

enum SoftwareScope {
    Programming(Option<ProgrammingLeaf>),
    Theory,                                  // pure terminal — no leaf enum
    Systems(Option<SystemsLeaf>),
    Data(Option<DataLeaf>),
    // … one Option<…Leaf> per sub-domain with curated leaves
}
enum ProgrammingLeaf { TypeSystems Compilation Parsing Grammars CodeGeneration Metaprogramming Macros DomainSpecificLanguages }
```

Consequences: each value sub-enum shrinks from ~16 variants to 0–8; `Theory`
emits no leaf enum (the canonical pure-terminal shape); single-leaf sub-domains
(`Quality`/`Intelligence`/`Observability`) keep an `Option`-wrapped one-variant
enum so the terminal case stays expressible. Every edit touches **both** mirror
families, and the `From`-chain migration rewrites stored values across both. The
schema-emit macro emits each leaf enum and its impls into `impl` blocks (method-only
rule).

## Migration consequence

The closed enum is stored inline in all **1248 records** (`Entry.Domains`, rkyv +
NOTA). All 169 cuts go to **keyword** (no leaf is a proper-noun referent). Every
cut leaf with live records folds up to its surviving sub-domain (terminal tag) or
a sibling curated leaf, with the specificity preserved as a description keyword.
The high-usage re-tags (the migration's real work):

| Cut leaf (usage) | Folds to | Keyword |
|---|---|---|
| `Engineering>DesignPatterns` (4) | `Engineering>Design` | design pattern |
| `Data>QueryProcessing` (10) | `Data` (terminal) | query processing |
| `Data>Encoding` (9) | `Data>Serialization` | encoding |
| `Data>DataValidation` (9) | `Data` (terminal) | validation |
| `Distributed>InterprocessCommunication` (9) | `Distributed>ProtocolDesign` | IPC |
| `Quality>IntegrationTesting` (10) | `Quality>Testing` | integration testing |
| `Quality>EndToEndTesting` (7) | `Quality>Testing` | e2e |
| `Security>AdmissionControl` (15) | **re-home** (see below) | admission control |
| `Operations>PackageManagement` (5) | `Operations>DependencyManagement` | packaging |
| `Systems>Virtualization` (6) | `Systems` (terminal) | virtualization |

Zero-usage cuts (113 leaves) have no records to re-tag — pure schema deletion.

**Hard dependency:** cutting `Data>DatabaseSystems` forces editing the
`Information>Database` ≡ `…Data DatabaseSystems` `Equivalence` bridge (104) in the
same change. The `Hardware>Networking` ≡ `Distributed>Networking` bridge survives
(Hardware keeps `Networking`; Distributed cuts it to keyword).

## The decisions that are yours

The curation defaulted to cut and verified each keep; these are the genuine
judgment calls left for you:

**1. `Theory` went pure-terminal (0 leaves).** All 13 leaves are 0-usage and
shadowed by applied siblings (`TypeTheory` by `Programming>TypeSystems` 17;
`FormalLanguages` by `Grammars` 30 + `Parsing` 11). Clean — but confirm you're
fine with `(Technology Software Theory)` carrying no sub-fields.

**2. High-usage but technique-ish keeps** (kept because usage was made decisive;
a stricter "recognized fields only" reading cuts some):
- `Macros` (49), `CodeGeneration` (41), `SchemaEvolution` (44) — the workspace's
  core mechanisms; artifact/activity-shaped, not classical "fields," but
  overwhelmingly routed. `SchemaEvolution` is the keep most exposed to the
  challenge.
- `Migration` (17) overlaps `SchemaEvolution`; `Modularity` (10) is an `-ility`
  identical in kind to the cut `Scalability`/`Maintainability`/`Reliability` —
  kept only on 10× usage. **A uniform `-ility` policy would flip `Modularity` to
  cut.**
- `Management` (10, from `SoftwareEngineeringManagement`), `SecretsManagement`
  (10), `Compilation` (11), `Visualization` (6) — thin-breadth keeps.

**3. Overrides where the skeptic cut a leaf the curator kept — confirm:**
- `AdmissionControl` (15, the highest-usage Security cut) — the count is a
  **semantic collision**: it's daemon/actor *peer-credential admission*, not a
  security discipline. Re-homed to the IPC/actor area as a keyword. Confirm the 15
  records aren't a real Security leaf.
- `InterprocessCommunication` (9) — transport mechanism, folded under
  `ProtocolDesign`; reinstate as `IPC` if transport deserves a bucket distinct
  from contract-shape.
- `NaturalLanguageProcessing` (5), `Virtualization` (6) — cut as
  not-workspace-central; glance at the records before finalizing.

**4. `DependencyManagement` kept but `PackageManagement` cut** — they overlap
heavily in Rust/Nix; keep both, or cut both and route via `BuildSystem`.

## Scope held to Technology

Per your choice (option 2, not "whole taxonomy"), the 23 non-Technology domains
are untouched. If you later want the same grain test on `Health`/`Craft`/etc.,
that's a separate pass.

## Skill / consumer updates (same change)

Carried from 104: `skills/spirit-cli.md` and `skills/intent-log.md` worked
examples (`SoftwareArchitecture`→`Architecture`, and `(Quality Testing)` is now a
terminal-able leaf — reword the example); `spirit/src/guardian-prompts/record-shape.md`;
the generated `domain.rs` (both mirror families) + `lib.rs`; `production_migration.rs`;
the two spirit test files; the `From`-chain over the live store.

## Spirit gate

Two durable arrows have surfaced across this thread, both held for your
green-light rather than auto-recorded (intent is precious; you didn't ask for
capture):

1. *A taxonomy middle-layer / leaf earns its place only if it disambiguates and
   carries routing load* — the discriminator refinement from the first prompt.
2. *The closed `Domain` enum is broad routing; fine specificity belongs to the
   open referent + keyword layers, not to deepening the closed taxonomy* — this
   prompt's principle.

These are one coherent `Principle` (certainty High, importance Minimum, referents
`spirit`/`signal-spirit`). Recommend recording once you confirm; I won't write to
the intent store unprompted.

## Hand-offs

Design (this report + 104) is complete. The schema rewrite — prune both mirror
families, add the `Optional`/terminal shape, regenerate, write the `From`-chain
domain migration, fix the skills + guardian prompt + tests, edit the
`DatabaseSystems` `Equivalence` bridge — is **one operator branch** (it all moves
together). The judgment calls in "The decisions that are yours" gate it.
