# 104 — Domain taxonomy naming audit: redundant ancestry and over-structuring in the Spirit `Domain` enum

*The psyche caught an agent tagging intent with
`(Technology (Software (Engineering SoftwareArchitecture)))` and named two
faults: `SoftwareArchitecture` repeats the `Software` grandparent
(→ `Architecture`), and the `Engineering` middle layer "is only needed if there
are other kinds of software architecture." This audits the whole closed `Domain`
taxonomy (`signal-spirit/schema/domain.schema`) for that class of fault. Method:
an 11-builder adversarial workflow (9 subtree passes + a structural pass + a
cross-domain-duplicate pass), each batch skeptically verified against a
term-of-art guard, then synthesised here. 87 findings confirmed, 5 rejected as
false positives.*

## The two rules, and why a third and fourth came along

The psyche's catch is two distinct rules, both already load-bearing intent:

1. **No redundant ancestry** — the founding naming rule ([the `-next` suffix is
   "vestigial ancestry and should be dropped"] Spirit `4ups` Decision; [the
   no-ancestry naming rule] Spirit `7118`; the foundational `naming.nota`). The
   full domain path is in scope at every record, so a leaf needs only the words
   the path does not already supply.
2. **A discriminator (middle) layer earns its place only if it disambiguates** —
   the psyche's "we only need Engineering if there are other kinds of software
   architecture." A middle node that is a pure pass-through (its children would
   read fine one level up, no collision) is ceremony.

Auditing for these surfaced two corollaries already in `skills/naming.md`:

3. **Repeated category words across siblings are a schema smell** — when a word
   recurs across sibling leaves (and matches the parent), it wants to become a
   *layer*, not live in every name (`UnitTesting`, `IntegrationTesting`, … all
   carry `Testing`).
4. **Term-of-art guard** (the false-positive check) — some compounds are fixed
   nouns where stripping the ancestor word yields a non-noun. `OperatingSystems`
   → `Operating` is broken; `MachineLearning`, `DataStructures`, `TypeTheory`
   are atomic. The guard is what keeps the audit from mutilating real names.

## The result in one line

The fault is **systemic and confined to one place**: the 23 non-Technology
domains and `Technology>Hardware` audited essentially clean; **every confirmed
rename lives in the `Technology>Software` subtree**, where the `Software*`,
`Data*`, `Programming*`, and `*Testing` prefixes recur. That the audit returned
"clean" for 23 of 24 top-level domains, and that the guard *rejected* five
tempting strips, is the evidence it found the real signal rather than
pattern-matching every compound word.

### The guard firing correctly (the 5 rejections + the major keeps)

These were proposed and **rejected** — they are *not* to be renamed:

| Kept whole | Why the strip is wrong |
|---|---|
| `DomainSpecificLanguages` | `DomainSpecific` is an adjective; DSL is the term of art. After the parent rename to `Programming` it no longer repeats any ancestor. |
| `BuildSystem` | "build system" is the atomic noun (Make, Bazel); bare `Build` reads weaker. |
| `ContinuousIntegration` / `ContinuousDelivery` | CI/CD are atomic; bare `Integration` collides with `Quality` testing, bare `Delivery` loses CD. |
| `*Management` flat (Package/Dependency/Artifact/Configuration) | the head noun alone (`Configuration`, `Package`) means a *thing*; `-Management` means the *practice*. |
| `DistributedTracing` / `AuditLogging` | `DistributedTracing` → `Distributed` collides head-on with the sibling **layer** `Software>Distributed`. |

Plus the Rule-4 keeps the builders never even proposed stripping:
`OperatingSystems`, `FileSystems`, `EmbeddedSystems`, `RealTimeSystems`,
`TypeTheory`, `DataStructures`, `GraphAlgorithms`, `MachineLearning`,
`DeepLearning`, `NeuralNetworks`, `ApplicationProgrammingInterfaces`,
`CloudComputing`/`EdgeComputing`, `Handicraft`, `Workplace`.

## Confirmed renames (mechanical — land regardless of the structural calls)

**Redundant-ancestry strips, High confidence:**

| Path | Current | → | Records tagged |
|---|---|---|---|
| `…Engineering` | `SoftwareArchitecture` | `Architecture` | **93** |
| `…Engineering` | `SoftwareEngineeringManagement` | `Management` (drops *both* ancestors) | 10 |
| `…Engineering` | `SoftwareDevelopmentProcess` | `DevelopmentProcess` | 24 |
| `…Engineering` | `SoftwareDesign` | `Design` | 22 |
| `…Engineering` | `SoftwareMaintenance` | `Maintenance` | 6 |
| `…Engineering` | `RequirementsEngineering` | `Requirements` | 4 |
| `…Data` | `DataModeling` | `Modeling` | **104** |
| `…Data` | `DataFormats` | `Formats` | 37 |
| `…Data` | `DataMigration` | `Migration` | 17 |
| `…Data` | `DataValidation` | `Validation` | 9 |
| `…Data` | `DataPipelines` | `Pipelines` | 0 |
| `…Languages` (layer → `Programming`) | `ProgrammingLanguages` | `Languages` | 1 |
| `…Languages` (layer → `Programming`) | `ProgrammingParadigms` | `Paradigms` | 1 |

**Medium / Low (term-of-art tension noted):**
`AutomataTheory`→`Automata` (0 recs); `DatabaseSystems`→`Databases` (2 — and
the `Data` inside `Database` is *atomic*, not stripped); `SystemsProgramming`→
`Programming` (5; "systems programming" is canonical — Low); `KernelDevelopment`
→`Kernel` (0); `NetworkProtocols`→`Protocols` (0); `DistributedSystems`→
`Systems` (2 — but see judgment call #5); `ModelTraining`→`Training` (1),
`ModelInference`→`Inference` (4). `ApplicationSecurity`/`NetworkSecurity` **kept
whole** (bare heads thin/colliding).

## The corrected `Technology>Software` subtree

High/Medium renames applied; term-of-art leaves untouched; the three structural
sub-layers shown in their proposed shape (each is a judgment call below).

```
      (Software [
        (Programming [Languages Paradigms TypeSystems Compilation Interpretation Parsing LexicalAnalysis Grammars CodeGeneration Metaprogramming Macros DomainSpecificLanguages RuntimeEnvironments GarbageCollection MemoryManagement ForeignFunctionInterfaces])
        (Theory [Algorithms DataStructures ComputationalComplexity Automata FormalLanguages GraphAlgorithms TypeTheory ProgramSemantics FormalMethods FormalVerification ModelChecking StaticAnalysis NumericalComputing Cryptanalysis])
        (Systems [OperatingSystems Programming Concurrency Parallelism Asynchrony Synchronization Scheduling FileSystems Virtualization Containerization EmbeddedSystems RealTimeSystems Firmware ResourceManagement Kernel DeviceDrivers])
        (Distributed [Systems Networking Protocols ProtocolDesign Consensus Replication MessageQueuing EventDrivenArchitecture ServiceMesh LoadBalancing RemoteProcedureCall InterprocessCommunication Routing FaultTolerance Sharding])
        (Data [Databases QueryProcessing Indexing Transactions Caching Storage Persistence Serialization Formats Compression Encoding Modeling Pipelines StreamProcessing BatchProcessing SchemaEvolution Migration Validation])
        (Intelligence [MachineLearning DeepLearning NeuralNetworks NaturalLanguageProcessing ComputerVision ReinforcementLearning Training Inference FeatureEngineering PromptEngineering RetrievalAugmentedGeneration AgentSystems InformationRetrieval Search Ranking RecommendationSystems KnowledgeRepresentation AutomatedReasoning])
        (Security [Cryptography Authentication Authorization AccessControl AdmissionControl SecretsManagement ThreatModeling VulnerabilityManagement PenetrationTesting ApplicationSecurity NetworkSecurity Sandboxing Hardening Privacy IntrusionDetection ReverseEngineering InputSanitization])
        (Quality [
          (Testing [Unit Integration EndToEnd PropertyBased Load Automation Fuzzing Mocking Coverage])
          Debugging Profiling Benchmarking PerformanceOptimization CodeReview Refactoring Linting Formatting TechnicalDebt])
        (Operations [ContinuousIntegration ContinuousDelivery BuildSystem ReleaseEngineering
          (Management [Dependency Package Artifact Configuration])
          Deployment Provisioning InfrastructureAsCode Orchestration AutoScaling CapacityPlanning SiteReliability IncidentResponse DisasterRecovery RateLimiting])
        (Observability [Logging Monitoring Alerting Tracing DistributedTracing Metrics Telemetry ErrorHandling AuditLogging])
        (Surfaces [
          (Development [Web Frontend Backend Mobile Game])
          UserInterface InteractionDesign Rendering ComputerGraphics Animation Layout Styling StateManagement Accessibility Usability Internationalization Localization Visualization SyntaxHighlighting CommandLineInterfaces])
        (Engineering [Architecture Design DesignPatterns DomainDrivenDesign ApplicationProgrammingInterfaces Microservices Serverless CloudComputing EdgeComputing Scalability Reliability Maintainability Portability Interoperability Modularity Abstraction Requirements Documentation VersionControl DevelopmentProcess Maintenance Management])
      ])
```

## Structural judgment calls — these are the psyche's, not mechanical

The renames above land regardless. These six change the *shape* of the tree:

1. **Does `Engineering` earn its place, or flatten into `Software`?** (the
   central question, and the literal one the psyche raised.) Recommendation:
   **keep** — flattening 22 children next to `Languages`/`Systems` orphans them
   with no grouping, and `Design` would collide with the `Surfaces` design
   items. But it holds leaves arguably belonging elsewhere (`CloudComputing`/
   `EdgeComputing`→Operations/Distributed; `VersionControl`→Operations;
   `Documentation`→Information). The six ancestry strips inside it are
   unconditional either way.
2. **Introduce `Quality > Testing`?** (recommend **yes** — the cleanest Rule-3
   case.) Standalone `Testing` becomes the layer; `Unit`/`Integration`/`EndToEnd`/
   `PropertyBased`/`Load`/`Automation` read correctly; `Fuzzing`+`Mocking`
   (techniques) and `Coverage` move under it. Alternative: de-prefix flat under
   `Quality`, losing the grouping.
3. **Introduce `Operations > Management`?** (**contested** — the audit split.)
   One reviewer confirmed the 4-wide sub-layer; another rejected it ("too diffuse
   — artifact and configuration management are distinct concerns; bare heads name
   the object not the practice"). Your tie-break.
4. **Introduce `Surfaces > Development`?** (weaker than Testing.) `Web/Frontend/
   Backend` = where code runs; `Mobile/Game` = platform/genre — less cohesive.
   **Hard constraint:** if *not* adopted, keep the compounds whole — never
   half-strip, because bare `Mobile` is an adjective and bare `Game` collides
   with `Leisure>Games`.
5. **`DistributedSystems`: rename to `Systems`, or remove the leaf?** Parent
   `Distributed` already names the family; one reviewer says rename to `Systems`,
   another says drop the leaf as pure redundancy. (Only 2 records tagged.)
6. **Security by surface?** If you want `ApplicationSecurity`/`NetworkSecurity`
   restructured, the sub-layer must be named by the *discriminator* (e.g.
   `Surface [Application Network …]`) — **never** a `Security` layer nested under
   `Security` (that is itself the ancestry violation). Default: keep both whole.

## Cross-domain duplicates

- **Verified existing `Equivalence` bridges (keep):** `Hardware>Networking` ≡
  `Software>Distributed>Networking`; `Information>Database` ≡
  `Software>Data>DatabaseSystems`. The second's right-hand path becomes
  `…Data Databases` under the rename and **must be edited in lockstep**.
- **`Networking` is the one real structural twin** (under both Hardware and
  Distributed) — already handled by the bridge; leave as-is unless you want them
  disambiguated (physical/link-layer vs protocol cluster).
- **Three proposed new bridges REJECTED as over-bridging** (`Equivalence` asserts
  *identity*, not relatedness): `Safety>Privacy` vs `Security>Privacy` (a right
  vs a property), `Information>Documentation` vs `Engineering>Documentation`
  (general vs specialization), `Information>Retrieval` vs
  `Intelligence>InformationRetrieval` (act vs research subfield). Same-word
  leaves in disjoint domains are legitimate homonyms, not violations.
- **Boundary-placement calls for you (not renames):** `Craft` mixes hand trades
  with industrial/technical leaves (`Electronics`, `Manufacturing`,
  `Engineering`, `Invention`) that sit near `Technology>Hardware`; `Home>Realty`
  vs `Home>Property` are near-synonyms.

## Migration consequence — the load-bearing risk

The `Domain` enum is **closed and stored inline** in every record:
`signal.schema:217` `Entry { Domains * … }`, `:101` `Domains (Vec Domain)`,
persisted via rkyv (daemon self-resumes from SEMA state). Renaming a closed-enum
leaf changes the variant identity in **both** the NOTA encoding and the rkyv
archived layout — old records won't deserialize and old NOTA won't parse. Per the
no-backward-compat hard override this clean break is the correct posture; but the
intent store is **precious data** ([recorded intent is precious, closely guarded
data] Spirit `i59i`), so the rewrite must be faithful.

**Measured blast radius (live store, 1248 active records):** concentrated in the
`Software` subtree. The renamed leaves I measured carry, conservatively:

- Engineering renames: 93 + 24 + 22 + 10 + 6 + 4 = **~159 records**
- Data renames: 104 + 37 + 17 + 9 + 2 = **~169 records**
- Testing re-parenting: 11 + 10 + … = **~21 records**
- scattered (SystemsProgramming 5, ModelInference 4, DistributedSystems 2,
  Programming layer, …) = ~15

`DataModeling` (104) and `SoftwareArchitecture` (93) are the two heaviest single
renames — **~197 records between them**. (Records may carry multiple domains, so
these overlap; the union is a large fraction of the 1248.) Untouched: every
record tagged only with non-Technology domains.

**Required migration:** a faithful `From`-chain domain rewrite — for each
affected record, map its `Domains` vector old-path → new-path before re-archiving
(`(Technology Software Engineering SoftwareArchitecture)` →
`(… Architecture)`; `(… Quality UnitTesting)` → `(… Quality Testing Unit)`).
Same pattern as the v8→v9 fold. The map should be generated mechanically from the
rename table so no record is missed; the **depth-changing** moves (the Testing/
Management/Development re-parenting) are the highest-risk because the path length
changes, not just the leaf name. Edit the line-53 `Equivalence` entry in the same
change.

## Skill files teach the bad name — they ship in the same change

Both psyche-facing intent skills (required reading for psyche-facing lanes, so
stale examples propagate into every capture) hardcode the bad example:

- `skills/spirit-cli.md:125`, `:145` — prose + the canonical `Record` example.
- `skills/intent-log.md:176`, `:299` — domain examples.

All four `(… Engineering SoftwareArchitecture)` → `(… Engineering Architecture)`.
Also `intent-log.md:298` `(… Quality Testing)` becomes a *layer* if the Testing
sub-layer lands — reword to a leaf, e.g. `(… Quality (Testing Unit))`. The
guardian prompt `spirit/src/guardian-prompts/record-shape.md` and the generated
`signal-spirit/src/schema/domain.rs` (+ `lib.rs`) regenerate from the schema.

## Consumers to migrate in lockstep

`signal-spirit/schema/domain.schema` (source) → `signal-spirit/src/schema/domain.rs`
(generated) + `lib.rs`; `spirit/src/production_migration.rs` (the migration code
itself); `spirit/tests/process_boundary.rs`, `tests/operator_271_closed_claims.rs`;
`spirit/src/guardian-prompts/record-shape.md`; the two skills above; the live SEMA
store (the `From`-chain).

## Spirit gate

The redundant-ancestry rule is already firmly captured (`4ups`, `7118`,
`naming.nota`) — no re-capture. The genuinely *new* arrow in the psyche's message
is the sharper criterion **a taxonomy middle-layer earns its place only if it
actually disambiguates** — a reusable refinement of the ancestry rule. Held for
the psyche's confirmation rather than auto-recorded (the prompt framed it as a
within-task aside; over-capture corrupts the layer). Recommendation: capture it
as a `Clarification` refining naming, certainty `High`, importance `Minimum`,
referents `[naming]`.

## Hand-offs

This audit is **design** — the rename + the `From`-chain migration + the schema/
generated-Rust/skill edits are **operator** work (one branch, since the schema,
the migration, the tests, and the skills move together). The three structural
sub-layer decisions (#2–#4), the `Engineering` keep-vs-flatten (#1), the
`DistributedSystems` choice (#5), and the security restructure (#6) are **psyche
decisions** that gate the operator branch.
