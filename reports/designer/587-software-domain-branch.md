# Spirit — the deep `Software` domain branch (three-tier)

The expansion of the software branch, per psyche intent: domain granularity tracks
intent density (`0zi7`), the tree is variable-depth with a third tier where dense
(`4wt3`), and `nota`/`signal`/`sema`/`spirit` are **referents, not domains**. A new
top-level `Software` area, `Software(Cluster(Leaf))` — 12 clusters, ~202 universal
subjects. Grounded in SWEBOK v4 + ACM CCS 2012 + GitHub/SO folksonomy. Run
`wf_b31eaa4a-937` (one synth agent dropped on a socket error; the merge compensated).

## Structure: a dedicated `Software` area, three tiers

`Software` becomes a **new top-level area** (24 → 25 areas, sibling to `Craft`,
`Knowledge`, `Technology`, `Information`), and `Craft` is cleaned back to pure physical
craft (its software leaves — `Programming`, `Architecture`, `Schema`, `Infrastructure`,
`Versioning`, `Testing`, `Tooling` — evicted into `Software`). Inside `Software` only,
a third tier: `Software(Languages(Parsing))`, `Software(Security(AdmissionControl))`.

Why a dedicated area, not expand-`Craft` or third-tier-under-`Craft`: `Craft` already
mixes code with carpentry/metalworking/sewing; bolting ~200 software leaves on makes
one branch 10× its siblings and forces a reader past `Sewing` to reach `Compilation`.
`0zi7` is the warrant to *break software out* as its own deep branch, not to swell a
catch-all. The third tier is **contained to `Software`** — life-areas stay two-tier —
so it's the variable-depth tree of `4wt3`, not a uniform complication.

**Mechanically free:** `DomainMatch` matches at `Domain` granularity, and
`Software(Languages(Parsing))` is one `Domain` value like any other — nothing
downstream (query, filter, match) sees a third level; it only lives inside the
`Software` variant's payload type. And growing an enum is trivial (`uuh7`), so the tree
keeps deepening wherever density appears.

## The tree — 12 clusters, ~202 subjects

- **Languages (16)** — ProgrammingLanguages · ProgrammingParadigms · TypeSystems · Compilation · Interpretation · Parsing · LexicalAnalysis · Grammars · CodeGeneration · Metaprogramming · Macros · DomainSpecificLanguages · RuntimeEnvironments · GarbageCollection · MemoryManagement · ForeignFunctionInterfaces
- **Theory (14)** — Algorithms · DataStructures · ComputationalComplexity · AutomataTheory · FormalLanguages · GraphAlgorithms · TypeTheory · ProgramSemantics · FormalMethods · FormalVerification · ModelChecking · StaticAnalysis · NumericalComputing · Cryptanalysis
- **Systems (16)** — OperatingSystems · SystemsProgramming · Concurrency · Parallelism · Asynchrony · Synchronization · Scheduling · FileSystems · Virtualization · Containerization · EmbeddedSystems · RealTimeSystems · Firmware · ResourceManagement · KernelDevelopment · DeviceDrivers
- **Distributed (15)** — DistributedSystems · Networking · NetworkProtocols · ProtocolDesign · Consensus · Replication · MessageQueuing · EventDrivenArchitecture · ServiceMesh · LoadBalancing · RemoteProcedureCall · InterprocessCommunication · Routing · FaultTolerance · Sharding
- **Data (18)** — DatabaseSystems · QueryProcessing · Indexing · Transactions · Caching · Storage · Persistence · Serialization · DataFormats · Compression · Encoding · DataModeling · DataPipelines · StreamProcessing · BatchProcessing · SchemaEvolution · DataMigration · DataValidation
- **Intelligence (18)** — MachineLearning · DeepLearning · NeuralNetworks · NaturalLanguageProcessing · ComputerVision · ReinforcementLearning · ModelTraining · ModelInference · FeatureEngineering · PromptEngineering · RetrievalAugmentedGeneration · AgentSystems · InformationRetrieval · Search · Ranking · RecommendationSystems · KnowledgeRepresentation · AutomatedReasoning
- **Security (17)** — Cryptography · Authentication · Authorization · AccessControl · AdmissionControl · SecretsManagement · ThreatModeling · VulnerabilityManagement · PenetrationTesting · ApplicationSecurity · NetworkSecurity · Sandboxing · Hardening · Privacy · IntrusionDetection · ReverseEngineering · InputSanitization
- **Quality (19)** — Testing · UnitTesting · IntegrationTesting · EndToEndTesting · PropertyBasedTesting · Fuzzing · TestAutomation · Mocking · CodeCoverage · Debugging · Profiling · Benchmarking · PerformanceOptimization · LoadTesting · CodeReview · Refactoring · Linting · Formatting · TechnicalDebt
- **Operations (18)** — ContinuousIntegration · ContinuousDelivery · BuildSystem · ReleaseEngineering · DependencyManagement · PackageManagement · ArtifactManagement · Deployment · Provisioning · InfrastructureAsCode · Orchestration · ConfigurationManagement · AutoScaling · CapacityPlanning · SiteReliability · IncidentResponse · DisasterRecovery · RateLimiting
- **Observability (9)** — Logging · Monitoring · Alerting · Tracing · DistributedTracing · Metrics · Telemetry · ErrorHandling · AuditLogging
- **Surfaces (20)** — WebDevelopment · FrontendDevelopment · BackendDevelopment · UserInterface · InteractionDesign · Rendering · ComputerGraphics · Animation · Layout · Styling · StateManagement · Accessibility · Usability · Internationalization · Localization · MobileDevelopment · GameDevelopment · Visualization · SyntaxHighlighting · CommandLineInterfaces
- **Engineering (22)** — SoftwareArchitecture · SoftwareDesign · DesignPatterns · DomainDrivenDesign · ApplicationProgrammingInterfaces · Microservices · Serverless · CloudComputing · EdgeComputing · Scalability · Reliability · Maintainability · Portability · Interoperability · Modularity · Abstraction · RequirementsEngineering · Documentation · VersionControl · SoftwareDevelopmentProcess · SoftwareMaintenance · SoftwareEngineeringManagement

Software alone (~202) is ~40% of the whole vocabulary — which is exactly
density-proportional: most intent here is software, so the software tree is the
deepest. The names are PascalCase variants, full English words, no abbreviations
(`ContinuousIntegration` not `CI`), no tool/product/language names.

## The referent boundary (the correction, made concrete)

The test on every leaf: *would an engineer at another company, on a different product,
recognize this as a subject they also work on?* Yes for all 202 → domains. Everything
below is a **referent** (a camelCase atom in the per-person, guardian-gated registry),
never a domain:

- **The workspace's own named instances** — `nota`, `signal`, `sema`, `nexus`, `spirit`,
  `guardian`, `rkyv`, `componentTriad`, `criomos`. An intent about Spirit's guardian is
  domain `Software(Security(AdmissionControl))` + referent `spirit`.
- **Named languages/runtimes** — Rust, Python, Nix-the-language → subject is
  `Languages(ProgrammingLanguages)`; the name is a referent. No `Rust` leaf.
- **Named tools/libraries/frameworks** — Cargo, Docker, Git, Postgres, React → subject
  is the activity (`PackageManagement`, `Containerization`, `VersionControl`,
  `DatabaseSystems`); the tool is a referent.
- **Named formats/patterns/protocols** — JSON, UML, HTTP, Raft, CQRS → subject is
  `DataFormats`/`DesignPatterns`/`NetworkProtocols`/`Consensus`; the artifact is a referent.

Rule of thumb: *if you can capitalize it as a proper noun and point at one specific
thing in the world, it's a referent; if it names an activity any team anywhere
performs, it's a domain.*

## Stress test — the split holds

Each real intent as domain(universal) + referent(instance):

| Intent | domain | referent |
|---|---|---|
| spirit's guardian decides atomically | `Software(Security(AdmissionControl))` + `Software(Data(Transactions))` | `spirit` |
| NOTA strings are bare atoms | `Software(Languages(Grammars))` | `nota` |
| daemon takes one rkyv startup arg | `Software(Data(Serialization))` + `Software(Engineering(SoftwareArchitecture))` | `spirit`, `rkyv` |
| deploy spirit via nix | `Software(Operations(Deployment))` | `spirit`, `nix` |
| property-test the parser | `Software(Quality(PropertyBasedTesting))` + `Software(Languages(Parsing))` | *(optional)* |
| signal contract is binary-by-default | `Software(Data(DataFormats))` + `Software(Distributed(ProtocolDesign))` | `signal` |

Erase the referent and a universal subject remains; erase the subject and only a bare
name remains that means nothing to an outsider. That asymmetry is the boundary working.

## Decisions for the psyche

1. **Adopt the dedicated `Software` area + three-tier mini-domain?** (Vs forcing
   `Software` into a flat ~202-variant enum, which is unreadable.) My lean: yes — it's
   your `(Software (Cluster Leaf))`.
2. **12 clusters — right granularity?** `Design` was folded into `Engineering` (now 22,
   the biggest cluster). Split `Design` back out (→13)? Or coarser?
3. **Craft eviction scope** — evict the 7 software leaves, keep `Engineering`/`Invention`
   in `Craft` as the universal physical-making sense? (My lean: yes.)
4. **`Knowledge(Computing)` vs `Software(Theory)`** — keep both (science-as-knowledge vs
   theory-applied-in-building), or retire `Knowledge(Computing)`? (My lean: keep both.)
5. **Area name `Software` vs `Computing`?** (My lean: `Software`.)
6. **Overlap ruling** — `Technology(Networking)` vs `Software(Distributed)`,
   `Information(Database)` vs `Software(Data)`, `Technology(Intelligence)` vs
   `Software(Intelligence)`. Proposed boundary: `Technology` = hardware/societal-system
   framing, `Information` = records/library framing, `Software` = build-it framing. Needs
   your ruling so a networking intent files deterministically.
7. **Migration** — existing records tagged `Craft(Programming/…)` re-tag to their
   `Software` cluster (breaking enum change, fine pre-production; operator-owned,
   guardian-aware pass).

Nothing logged from this yet — the tree is a proposal; the durable intent (`0zi7`
density, `4wt3` variable-depth) is already recorded. Bless the structure (or adjust the
open questions) and it becomes the blessed software branch.
