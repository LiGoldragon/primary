# Repository classification: vocabulary, prior art, local conventions, names

Subflow of Psyche Fable 6997eb, 2026-10-01. Subject: the living's
repository-classification Nexus (`flows/6997eb/vision/repositoryClassification.md`).

Evidence marks: **witnessed** = I read it myself on disk in this run (file,
command output); **claim** = a web page or paper says so; I did not verify
behaviour. Every web row below is a claim. Hashes are six characters.

## 1. Vocabulary

### 1a. Lifecycle and maturity (what stage a thing is in)

| Term(s) | Meaning | Who uses it |
|---|---|---|
| Proposal, Incubation (podling), Graduation, Retirement | Stages of entry into a foundation; incubating = "not yet fully endorsed", explicitly *not* a statement of code stability | Apache Incubator (claim) |
| Attic | End-of-life holding place: preserved, overseen, "not authorized to actively develop and release" | Apache Attic (claim) |
| Sandbox, Incubating, Graduated, Archived | Four maturity levels tied to adoption ("Crossing the Chasm"), promotion judged on adoption, contributor diversity, best-practice badge | CNCF (claim) |
| experimental, production, deprecated | Component `spec.lifecycle`; free-form, these three are the common values | Backstage catalog (claim) |
| Concept, WIP, Suspended, Abandoned, Active, Inactive, Unsupported, Moved | Eight repo statuses on two axes: *reached stable/usable?* × *is work continuing / intended?*; Moved carries a new URL | repostatus.org (claim) |
| actively-developed, passively-maintained, as-is, experimental, looking-for-maintainer, deprecated, none | Maintainer *intent* (not observed activity); crates.io no longer displays it | Cargo `[badges] maintenance` (claim) |
| 1 Planning, 2 Pre-Alpha, 3 Alpha, 4 Beta, 5 Production/Stable, 6 Mature, 7 Inactive | Ordered development-status scale, one of nine classifier facets | PyPI trove classifiers (claim) |
| Experiment, Beta, Limited Availability, Generally Available | Feature support stages; experiment "could be removed at any time" | GitLab (claim) |
| alpha, beta, stable (v1alpha1, v2beta3, v1) | API stability encoded in the version name; beta has a bounded lifetime before deprecation | Kubernetes (claim) |
| stable / unstable + feature gate, deprecated | Per-item stability attribute; unstable items require an opt-in gate | Rust compiler (claim) |
| 0.y.z: "Anything MAY change at any time" | Version number as a breakage signal; major bump = breaking | SemVer (claim) |
| Adopt, Trial, Assess, Caution (was Hold) | Recommendation rings for technologies, in four quadrants | Thoughtworks Tech Radar (claim) |
| archived (read-only) | Repository frozen; only fork/star possible | GitHub (claim) |
| RFA, O (orphaned), ITA, RFH, ITP, RFP | Ownership-transition states of a package | Debian WNPP (claim) |
| broken, insecure, knownVulnerabilities, maintainerless | Per-package state flags that gate evaluation/installation | nixpkgs `meta` (claim) |
| Active, (Deprecated <disposition>) | Repo lifecycle, orthogonal to kind | our `protocols/repos-manifest.dotos` (witnessed) |
| active component / frozen reference / legacy-wired / out of scope | Repo status inside each repo's AGENTS.md | our "Protos estate status" sections (witnessed) |

### 1b. Kind and type (what a thing is)

| Term(s) | Meaning | Who uses it |
|---|---|---|
| Kind: Component, API, Resource, System, Domain, Group, User, Location, Template | Nine entity kinds; Component has free `spec.type` (service, website, library) | Backstage (claim) |
| projectType application / library; tags `type:*`, `scope:*` + depConstraints | Tags are free strings; constraints say which tagged projects may depend on which | Nx (claim) |
| tags (manual, exclusive, no-remote…), visibility, testonly, deprecation | Per-target attributes; testonly forbids production deps on test code; deprecation warns dependants | Bazel (claim) |
| tags + `--tag` filter; 170+ target types | Free strings for filtering targets | Pants (claim) |
| Primary Package Purpose: APPLICATION, FRAMEWORK, LIBRARY, CONTAINER, OPERATING-SYSTEM, DEVICE, FIRMWARE, SOURCE, ARCHIVE, FILE, INSTALL, OTHER; Valid Until Date | Closed enum of package purpose; support end date | SPDX 2.3 (claim) |
| categories (closed slug list, max 5), keywords (free, max 5) | Two-tier: controlled vocabulary + free tags | Cargo / crates.io (claim) |
| packages, apps, devShells, checks, nixosModules, nixosConfigurations, overlays, templates, … | What a flake *exports*, by output attribute; flake schemas define how outputs are shown | Nix flakes; DeterminateSystems flake-schemas (claim) |
| Development Status, Environment, Framework, Intended Audience, License, Natural Language, Operating System, Programming Language, Topic | Nine orthogonal facets | PyPI (claim) |
| Entity + Aspects (Ownership, Tags, Glossary Terms, Status, SubTypes) + Relationships; versioned vs timeseries aspects | Entity typed by URN; facts attached as independent aspects; observations as timeseries | DataHub (claim) |
| custom properties: string, single select, multi select, boolean | Org-defined typed metadata per repo, used to target rulesets | GitHub (claim) |
| Kind: Code, Content, Data; Family; flags IsFork, IsPrivate, BuildTimeConsumed; doctrine-home | Our existing classification | `protocols/repos-manifest.dotos` (witnessed) |

### 1c. Observed state signals (measured, not declared)

| Term | Meaning | Who uses it |
|---|---|---|
| Contributor Absence Factor (formerly bus factor) | Smallest number of contributors making 50% of contributions | CHAOSS (claim) |
| Truck factor | Minimal number of developers whose leaving incapacitates the project; estimated from commit history | Avelino et al., ICPC 2016 (claim) |
| Time to First Response, Change Request Closure Ratio, Release Frequency | With absence factor, the CHAOSS "Starter Project Health" model | CHAOSS (claim) |
| Libyears | Cumulative age of dependencies behind their current releases | CHAOSS (claim) |
| Maintained | Top score = ≥1 commit/week over 90 days; projects <90 days not assessed; archived = lowest | OpenSSF Scorecard (claim) |
| Level of maintenance activity | Data-driven score of whether a GitHub project is maintained | Coelho, Valente et al., IST 2020 (claim) |
| Repository stability / Composite Stability Index | Capacity to return to equilibrium after disturbance; commits, issues, PRs, engagement | Destefanis et al., arXiv 2504.00542, conceptual (claim) |
| Productivity, Robustness, Niche Creation | Three pillars of *ecosystem* (not project) health | Jansen 2014, OSEHO (claim) |

Synthesis (my reading, not a source's): the field keeps three things
apart that the living's words mix together. **Kind** (what it is),
**declared lifecycle** (what its owner intends: experimental, stable,
deprecated) and **observed state** (what the history shows: activity,
churn, breakage). "Very active", "high development speed" and "quickly
breaking" are observed state; nobody serious asks the owner to type them
in. Cargo's maintenance badge died partly because a declared state rots;
Scorecard and CHAOSS compute it. repostatus.org is the cleanest declared
vocabulary because it is two axes (usable yet? / work continuing?).

## 2. Prior-art systems

| System | Kinds | Lifecycle | Relations | State signals | Leaves out |
|---|---|---|---|---|---|
| Backstage software catalog | 9 closed kinds; free `spec.type` per kind | free `spec.lifecycle`, conventionally experimental/production/deprecated | partOf/hasPart (Component→System→Domain), dependsOn, providesApi/consumesApi, ownedBy | none built in; plugins and "scorecards" (commercial Soundcheck, Cortex, OpsLevel) add them | measured activity; types are free strings, so no type checking; entities are YAML hand-written per repo |
| DataHub (and OpenMetadata-style data catalogs) | typed entities with URN keys; SubTypes aspect | Status aspect (soft delete), deprecation aspect | named, bidirectional relationships declared in schema | timeseries aspects (usage, profiles) kept apart from versioned aspects | software build graph; repository semantics |
| GitHub | repo; custom properties (typed: string, single/multi select, bool); topics | archived (read-only) | forks, dependency graph; CODEOWNERS (last match wins) for path ownership | Insights; Scorecard as external app | any hierarchy of kinds; lifecycle beyond archived |
| Google monorepo (Piper, OWNERS, Blaze/Bazel) | BUILD targets with rule kinds; visibility and testonly | `deprecation` attribute on targets | dependency graph enforced by visibility | OWNERS route review per directory | repo-level classification: one repo, so classification is per directory/target |
| Nx / Bazel / Pants | project/target types + free tags | none first-class (Bazel `deprecation`) | dependency graph; Nx depConstraints between tag classes | affected-by-change computation | lifecycle and health |
| Nix (flakes, nixpkgs meta) | flake output attributes say what a repo exports; flake schemas | `meta.broken`, `insecure`, `knownVulnerabilities` | flake inputs = dependency graph; lock file pins | Hydra build status per platform | intent, ownership hierarchy beyond `maintainers`/`teams` |
| repostatus.org | none | 8 declared statuses on two axes | `Moved` points elsewhere | none | everything but status |
| CHAOSS / Scorecard | none | none (Scorecard: archived) | none | computed health metrics and models | kind, intent |

"Boq": only an anonymous Hacker News comment ties it to Google's deployment
automation (claim, weak); I found no primary source and treat it as
unknown. "OpenDataHub-style catalogs" I read as metadata catalogs of the
DataHub/OpenMetadata kind; if a specific project was meant, it is not
covered here.

Most worth modeling on: Backstage (kind/type/lifecycle split, System and
Domain grouping, ownership and API-provision relations), DataHub (typed
entities with independent aspects; declared facts versioned, observations
timeseries), and Scorecard/CHAOSS (state computed from history, never typed
in). Nix flake outputs are the natural *subtype detector* for our repos:
what a repo exports is readable without asking anyone.

## 3. Local conventions and existing psyche

### 3a. Workspace roots (witnessed, `ls /home/li`)

`/home/li/primary`, plus seat workspaces `/home/li/core`, `secondary`,
`tertiary`, `quaternary` (each holding AGENTS.md, CLAUDE.md, SKILL_VARIABLES.md,
flake.nix, flows/, skills/); worktree roots `/home/li/worktrees` and
`/home/li/wt`. Repository root (SKILL_VARIABLES.md): `/git`, host/owner/name
layout (`/git/github.com/LiGoldragon/<name>`, 213 entries). `primary/repos` is
a symlink to that directory.

### 3b. Existing classification already on disk (witnessed)

- `protocols/repos-manifest.dotos` (last change 792a08, 2026-09-14), declared
  "Authoritative inventory of LiGoldragon repos". One record per repo:
  `(Repo <name> <remote> (Family <f>) <kind> <lifecycle> <doctrine-home> [flags])`.
  Kind ∈ Code | Content | Data; lifecycle ∈ Active | (Deprecated
  <disposition>); flags IsFork, IsPrivate, BuildTimeConsumed; Families:
  Signal 41, Tooling 35, MetaSignal 25, Content 20, Persona 19, Dotos 11,
  Criome 9, CriomOS 7, Schema 6, Sema 4, Lojix 4, Mentci 3, and five of 1.
  188 records; **8 name repos absent on disk, and 33 on-disk repos are
  unlisted** (among them datom, flow, signal-flow, meta-signal-flow,
  psyche-skills, mind-skills, field-skills, *-logs, persona-test,
  primary-next). It has drifted: a hand-kept index, as the field predicts.
- `protocols/active-repositories.md`: prose sections "Current Core Stack",
  "Inactive / Archived Components", "Adjacent Active Work", "Replacement
  Stack", "Current Truth Pins".
- `protocols/component-evidence.generated.json`: generated check of the
  manifest against disk (`missing-locally` status).
- "Protos estate status" sections in 165 repos' AGENTS.md: fields Stack
  (correct-new destination 96, incorrect-new 33, not applicable 32, legacy 3),
  Status (active component; active component contract; frozen reference 33;
  legacy production/reference; adoption unresolved), Role (content, upstream
  fork, general tooling, operating-system source, …). A second, unsynchronised
  classification living inside the repos.
- `repository-ledger` (+ `signal-` and `meta-signal-repository-ledger`): an
  existing Nexus-shaped component recording Gitolite push events, commits and
  file changes in sema; meta operations `Register`, `Retire`,
  `SetSpoolDirectory`, `SetMirror`; queries for recent repositories, changed
  files, commit-message search. It already holds the raw history from which
  activity and churn could be computed. Last commit 096179, 2026-09-12; its
  own AGENTS.md says it is legacy-wired (triad daemon, schema-rust).

### 3c. Repo kinds by naming convention (witnessed from names and skills)

- Nexus repo `<n>` with `signal-<n>` and `meta-signal-<n>` wire type repos
  (nexus skill; Vision/nexus.md "A component has three repositories").
- `<repo>-test`: Nix sandbox test repo (persona-test; compensation-nix skill).
- Skill/data repos: psyche-skills, mind-skills, field-skills; psyche-logs,
  mind-logs, field-logs; Curriculum (skill sources).
- Standards repository (`standards`), workspace repos (primary-next,
  secondary, tertiary, quaternary, core), OS/config (CriomOS*,
  criomos-horizon-config), `-engine` libraries (sema-engine, ethos-engine,
  logos-engine, nomos-engine), `-config` repos (mind-judge-config,
  spirit-judge-config), `-derive`/`-codec` libraries, `tree-sitter-*`
  grammars, forks (kameo, nixpkgs, pi-subagents-nicobailon), content/books
  (BookOfGoldragon, TheBookOfSol, caraka-samhita).

### 3d. What the psyche has already said (verbatim, with provenance)

The opening of this subject:

> The way repositories are indexed: right now they're not. Obviously we haven't done that: the way that all of the repositories are classified by type, the way they're marked as sort of very active or [not] very active, or maybe not very active but in high development speed or quickly breaking or something.

-- psyche, STT, 2026-10-01, `flows/6997eb/vision/repositoryClassification.md`.

Component anatomy (a repo kind rule):

> A component has three repositories: its main repository, holding all
> its code, and two signal repositories — one for the ordinary
> socket's contract, one for the meta socket's. Shared kinds go into
> reusable libraries, which are encouraged.

-- `Vision/nexus.md`, §Repositories. Source quote: "so ethos can have all the code, minus the two signal repos, and so on (3 repos per component). other than reusable libraries of course" -- psyche, typed, 2026-08-11, `flows/012fbf07/vision/archive-threeStacks.md`.

Test repos as a kind made by suffix:

> which we could also have for any other repo. We would just add the test suffix and then create a new repo.

-- psyche, STT, 2026-09-26, `flows/e167d8/vision/testRepos.md`.

Data repos with expected structure; stable vs unstable marking:

> That's going to be in its own dedicated repository, which has an expected structure of the psyche. You're going to have another repo for the mind and another repo for mind data. Psyche data, mind data, and then we're going to have the field now, so field data.
>
> These are three repos. The primary workspace is a template, the basic infrastructure that you don't necessarily touch very often, which expects to find other repositories mounted there. [...] It's going to have different levels of setup, some of which are stable and some are not. We can mark them unstable or testing.

-- psyche, artifact comment, 2026-09-18, `flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md`.

A repo's state named by the psyche:

> persona-spirit? that is an abandonned repo.

-- psyche, 2026-08-21, `vision-raw/spiritComponentAndFile.md`.

On naming (the criterion a candidate must meet):

> people wont remember dotos, eidos or rhetos. it just wont stick at
> all

-- psyche, typed, 2026-08-10, `flows/c6b71b4c/vision/archive-threeStacks.md`.

Searches of `Vision/`, `vision-raw/`, `flows/*/vision/` for catalog,
registry, repository type/kind/index/classification found nothing else on
the subject; "workspace" hits concern seat workspaces, not repo
classification.

### 3e. What the local conventions imply

The kind axis already exists and is mostly derivable from names and files:
the nexus triad, `-test`, `-skills`/`-logs`, `-engine`, `-config`,
`tree-sitter-`, forks. The manifest already separates kind from lifecycle
from flags, the separation the field converged on. Two hand-kept indexes
(manifest, estate-status sections) disagree with disk and with each other;
repository-ledger already sees every push. A Nexus that derives kind from
structure, takes lifecycle by meta-socket declaration, and computes state
from the ledger's history would absorb all three. Whether it is a new Nexus
or repository-ledger grown is open; the nexus skill's splitting rule cuts
both ways.

## 4. Candidate names

Style: one-word nouns, the stickiness test above. Checked against the 213
names in `/git/github.com/*/`: none collide.

| Name | Reasoning |
|---|---|
| Census | Counts and classifies the whole population on a schedule; plain, sticky, already used by the psyche for "a periodic system census". |
| Taxon | The unit of a taxonomy: type, subtype, rank; short and Greek-rooted like protos/ethos. |
| Genus | Kind with species beneath it, exactly "types and subtypes"; widely known word. |
| Atlas | A map of everything, the "top-down structural organization" the living named. |
| Estate | Already the local word ("Protos estate status" in 165 repos); the whole holding, surveyed. |
| Canon | The recognized body and its standing; pairs with the standards repository, though it leans to authority over state. |
| Kosmos | Greek "ordered whole"; matches the top-down ambition, less plain than Census. |
| Cadastre | The official register of an estate's parcels and their status; precise, but may fail stickiness. |

Ledger is taken (repository-ledger); Eidos was already rejected by the psyche
as unmemorable.

## Sources

Web (all claims):
- Backstage descriptor format: https://backstage.io/docs/features/software-catalog/descriptor-format
- Backstage system model: https://backstage.io/docs/features/software-catalog/system-model
- repostatus.org: https://www.repostatus.org/
- Cargo manifest (badges, categories, keywords): https://doc.rust-lang.org/cargo/reference/manifest.html
- CNCF maturity levels: https://www.cncf.io/project-metrics/
- Apache Incubator policy: https://incubator.apache.org/policy/incubation.html
- Apache Attic: https://attic.apache.org/
- PyPI classifiers: https://pypi.org/classifiers/
- GitLab development stages: https://docs.gitlab.com/policy/development_stages_support/
- Kubernetes API versioning: https://kubernetes.io/docs/reference/using-api/#api-versioning
- Rust stability attributes: https://rustc-dev-guide.rust-lang.org/stability.html
- SemVer: https://semver.org/
- Thoughtworks Radar FAQ: https://www.thoughtworks.com/radar/faq
- GitHub archiving: https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories
- GitHub CODEOWNERS: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub custom properties: https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization
- Debian WNPP: https://www.debian.org/devel/wnpp/
- nixpkgs meta attributes: https://nixos.org/manual/nixpkgs/stable/#chap-meta
- nix flake check outputs: https://nix.dev/manual/nix/2.28/command-ref/new-cli/nix3-flake-check
- flake-schemas: https://github.com/DeterminateSystems/flake-schemas
- Nx module boundaries: https://nx.dev/docs/features/enforce-module-boundaries
- Bazel common attributes: https://bazel.build/reference/be/common-definitions
- Pants tags: https://www.pantsbuild.org/stable/reference/targets/python_source
- SPDX 2.3 package information: https://spdx.github.io/spdx-spec/v2.3/package-information/
- DataHub metadata model: https://docs.datahub.com/docs/metadata-modeling/metadata-model
- OpenSSF Scorecard checks: https://github.com/ossf/scorecard/blob/main/docs/checks.md
- CHAOSS Contributor Absence Factor: https://chaoss.community/kb/metric-bus-factor/
- CHAOSS Starter Project Health: https://chaoss.community/kb/metrics-model-starter-project-health/
- CHAOSS Libyears: https://chaoss.community/kb/metric-libyears/
- Avelino et al., "A Novel Approach for Estimating Truck Factors", ICPC 2016, arXiv:1604.06766
- Coelho, Valente, Milen, Silva, "Is this GitHub project maintained?", Information and Software Technology 122, 2020
- Destefanis et al., "Introducing Repository Stability", https://arxiv.org/abs/2504.00542
- Jansen, "Measuring the health of open source software ecosystems", 2014 (via search summaries)
- Potvin, Levenberg, "Why Google Stores Billions of Lines of Code in a Single Repository", CACM 2016: https://cacm.acm.org/research/why-google-stores-billions-of-lines-of-code-in-a-single-repository/
- Boq: Hacker News comment only, https://news.ycombinator.com/item?id=40823142 (weak)

Local (witnessed):
- /home/li/primary/flows/6997eb/vision/repositoryClassification.md
- /home/li/primary/protocols/repos-manifest.dotos, active-repositories.md, component-evidence.generated.json
- /home/li/primary/Vision/nexus.md
- /home/li/primary/flows/012fbf07/vision/archive-threeStacks.md
- /home/li/primary/flows/e167d8/vision/testRepos.md
- /home/li/primary/flows/b05237/vision/operational-threeDataReposAndPrimaryNext.md
- /home/li/primary/vision-raw/spiritComponentAndFile.md
- /home/li/primary/flows/c6b71b4c/vision/archive-threeStacks.md
- /git/github.com/LiGoldragon/repository-ledger (README.md, ARCHITECTURE.md, AGENTS.md), meta-signal-repository-ledger/ethos/signal.ethos
- "Protos estate status" sections: grep over /git/github.com/LiGoldragon/*/AGENTS.md
- Directory listings of /home/li, /git/github.com/LiGoldragon
