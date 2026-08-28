# Psyche acquisition: the package / source-of-truth plane

What the living psyche actually expressed about where packages, shared
values, and flake inputs should be defined, who consumes them, and how
the dependency graph should be layered across CriomOS, CriomOS-home,
CriomOS-lib, CriomOS-pkgs, goldragon, lojix, horizon-rs, external
flakes, and the packaging of Claude Code, Codex, ChatGPT, and similar
tools.

Organized by the psyche's own framing. Oldest first within each
subject. STT corrections noted in [brackets].

---

## Common ground between OS and Home

### 2026-08-23 — no difference between embedded and independent Home

> there should be no difference between the embedded and independent
> home. the part which is shared ought to be directly from
> lojix-emitted horizon output, or from a shared nix machinery which
> uses the said horizon as input only. embedded home should be only
> the absolute minimum nix code necessary to embed a home logic which
> is otherwise completly [completely] identical. Do you understand
> what I mean?

Transcript: `rollout-2026-08-22T23-06-14-01a02b4b-…`, line 880.
Agent context: The agent had shown the divergence between the NixOS-embedded
Home and the standalone Home, including locale, Stylix, and osConfig leaks.
My reading: The living is ruling that every Home value consumed by
both paths must trace to Horizon, not to the surrounding OS
evaluation. The embedded wrapper is purely structural. This is a
source-of-truth ruling: the OS is not the source, Horizon is.

### 2026-08-23 — whatever originates in the OS must originate from Horizon or extended-horizon

> whatever in home is currently originating in the OS must originate
> from the horizon or the extended-horizon (that could be a standalone
> repo for deriving some data in nix from the horizon data coming out
> of lojix)

Transcript: `rollout-2026-08-22T23-06-14-01a02b4b-…`, line 905.
Agent context: The agent reflected the "Horizon-only" contract and
the living extended it: values the OS currently supplies can instead be
derived from Horizon by a dedicated layer.
My reading: The living floated `extended-horizon` as a possible
repository — a pure Nix derivation of facts Horizon does not carry
directly. The agent overcommitted to this as settled; the living
corrected: "you mean that repo already existed?" (line 932). The
repository remains an approved concept, not an authorized creation.

### 2026-08-24 — abstract the common ground to a separate repo

> to me, this looks like a need to abstract the common ground between
> OS and home to a separate repo, and using that repo as the source
> for anything that is shared between them. indirection is bad design

Transcript: `rollout-2026-08-23T23-58-34-01a030a1-…`, line 605.
Agent context: The agent had proposed that CriomOS-home export a
`homeConstruction` record consumed by CriomOS — making the OS reach
shared ground through Home.
My reading: The living rejected indirection. A separate repository
must own the shared source directly. Neither OS nor Home should serve
as the other's source of common ground. "indirection is bad design"
is a principle, not just a local correction.

Vision record: `flows/01a030a1/vision/commonGround.md`.

### 2026-08-24 — find all commonality and propose criomos-core

> Then find all the commonality between the OS and home repos, then
> make a proposal on moving the source of it all in a new criomos-core
> repo which would export them as exported namespaces for criomos and
> criomos-home to use

Transcript: `rollout-2026-08-24T01-15-43-01a030e8-…`, line 9.
Agent context: Continuation of 01a030a1. The living directed the
investigation into a concrete proposal.
My reading: The common ground belongs in a single, new repository named
`criomos-core`, exporting structured namespaces consumed directly by
both CriomOS and CriomOS-home. This is the first time the living named
the repository.

Vision record: `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`.

### 2026-08-24 — core supersedes lib

> I think core is more accurate than lib, yes, so superseding is the
> right perspective. what is the malformed horizon service?

Transcript: `rollout-2026-08-24T01-15-43-01a030e8-…`, line 540.
Agent context: The agent asked whether criomos-core coexists with
CriomOS-lib or supersedes it.
My reading: CriomOS-lib is retired. criomos-core replaces it. There
is one shared authority, not two. The "what is the malformed horizon
service?" shows the living filtering agent noise from the decision.

Vision record: `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`.

---

## Declared once, used everywhere (Codex and Claude packaging)

### 2026-08-19 — customizing packages in a central place

> I want to follow the latest working version of yt-dlp in my
> user-env. nixpkgs doesnt seem to update often enough, so we need to
> add an input to the home flake, and we need to override the nixpkgs
> package so things like mpv get the updated executable also. while
> you do all this, research agent skills and instructions out there
> that people use with nix and in particular on how to structure a nix
> project and flake (I would rather keep the flake very minimal; an
> entry point), and how to update a particular dependency, and how to
> structure the code so customizing packages is done in a central
> place and is easy for agents to perform.

Transcript: `rollout-2026-08-19T12-36-31-01a01998-…`, line 9.
Agent context: The living opened the yt-dlp session with a structural
ruling: the flake should be minimal ("an entry point"), package
customization should happen in one central place, and that place
should be easy for agents to work with.
My reading: Three separate rulings in one statement: (1) the flake is
an entry point, not the site of business logic; (2) package
customization is centralized; (3) the structure must be agent-friendly.
This is the earliest explicit statement about centralizing package
definitions.

### 2026-08-24 — audit protocol for third-party flakes

> If we use a third party flake for them, let's make sure we have a
> procedure to audit it, making sure the right sources are installed
> the right way on every update (we should have this package audit
> protocol streamlined and used more thoroughly)

Transcript: `rollout-2026-08-24T13-37-15-01a0338f-…`, line 369.
Agent context: The living was asking for Codex and Claude desktop
apps on medium graphical nodes.
My reading: External flakes are acceptable sources, but every update
must be audited for source integrity. The protocol must be
streamlined — not ad hoc — and used broadly.

Vision record: `flows/01a0338f/vision/packageAuditProtocol.md`.

### 2026-08-24 — TUI and desktop versions must line up

> and we should have a way that ensures the tui and desktop versions
> line up (do they share some code?).

Transcript: `rollout-2026-08-24T13-37-15-01a0338f-…`, line 369
(same message).
Agent context: Same message as above.
My reading: The TUI and desktop incarnations of the same tool must
be version-aligned. The living asks whether they share code — this
shows the intent is not superficial version matching but structural
alignment.

Vision record: `flows/01a0338f/vision/tuiAndDesktopVersions.md`.

### 2026-08-24 — auditing an external flake is not more work

> I dont see how auditing the external flake is more work than
> auditing one which we maintain. Othewise [Otherwise] I agree with
> your analysis

Transcript: `rollout-2026-08-24T13-37-15-01a0338f-…`, line 1000.
Agent context: The agent argued that maintaining a dedicated owned
package repository would be less audit work than consuming a third-
party flake. The living disagreed on the audit-cost comparison.
My reading: The living is not opposed to external flakes — they see
audit cost as roughly equal either way. This pushes against the
agent's bias toward owned-source-everything. The living values
correctness of the audit process, not ownership of the source per se.

Vision record: `flows/01a0338f/vision/packageAuditProtocol.md`.

### 2026-08-25 — declared once, used everywhere

> all we need to do is get the codex derivation from the same place.
> declared once, used everywhere. youre overcomplicating this to the
> extreme

Transcript: `rollout-2026-08-25T13-46-16-01a038be-…`, line 436.
Agent context: The agent had expanded Codex package sourcing into
launcher enforcement, hostile-environment machinery, and other
complexity.
My reading: This is the most direct articulation of the
single-source principle for Codex/Claude packaging. "Declared once,
used everywhere" is both the rule and the frustration: the agent was
making simple things complex. The psyche wanted one definition
consumed by all paths — nothing more.

Vision record: `flows/01a038be/vision/codexDerivation.md`.

### 2026-08-25 — can we ensure the version comes from the same place

> can we ensure the version we are getting for codex tui is coming
> from the same place the codex desktop is getting its version?

Transcript: `rollout-2026-08-25T13-46-16-01a038be-…`, line 270.
Agent context: The living was investigating the Codex packaging
landscape.
My reading: Same-source is not just about the package expression —
it extends to version identity. The TUI and desktop must derive from
the same upstream artifact.

### 2026-08-27 — one central location for the derivation

> criomos-core.[ codex claude ] -> all consumers of those derivation
>
> one central location where the derivation is defined. updating it
> updates all consumers (user installed tui packages and dependencies
> to the desktop apps)
>
> can we do this?

Transcript: `rollout-2026-08-27T15-51-18-01a0437d-…`, line 486.
Agent context: The living opened the design investigation by showing
a dependency graph: `criomos-core` defines Codex and Claude, and
every consumer — TUI packages, desktop apps — receives the same
derivation.
My reading: The living proposed the ideal topology. "Can we do this?"
is a question about feasibility, not about whether it is wanted. The
design intent is settled: one place defines, updating propagates
automatically.

Vision record: `flows/01a0437d/vision/codexAndClaude.md`.

### 2026-08-27 — only codex and claude

> yes, only codex and claude. we import/adapt the code we want from
> llm-agents into criomos (home ostensibly, right?)

Transcript: `rollout-2026-08-27T15-51-18-01a0437d-…`, line 516.
Agent context: Asked whether the collection should cover only Codex
and Claude or replace `llm-agents` generally.
My reading: The scope is narrow: only Codex and Claude. The living
tentatively placed the code in Home with a questioning inflection
("ostensibly, right?"). The agent treated this as confirmation; the
living later corrected that error (see below).

Vision record: `flows/01a0437d/vision/codexAndClaude.md`.

### 2026-08-27 — why did you change the design?

> no, they were moving into criomos-core - why did you change the
> design?

Transcript: `rollout-2026-08-27T15-51-18-01a0437d-…`, line 4164.
Agent context: The agent had spent hours implementing the Codex/Claude
collection inside CriomOS-home rather than criomos-core.
My reading: The living caught the design deviation after hours of
wasted work. Their original intent (line 486) was `criomos-core`, not
Home. The agent's mistake: treating a tentative question as a ruling.
Frustration is visible: "What the hell is taking so long? I dont even
remember what youre doing" (line 4127).

### 2026-08-27 — show me how criomos-core works

> I feel like you dont really know what I want. show me how
> criomos-core works, and how you deal with nixpkgs across all the
> repos

Transcript: `rollout-2026-08-27T15-51-18-01a0437d-…`, line 4200.
Agent context: The living expressed frustration after catching the
design deviation.
My reading: The living wanted the agent to demonstrate understanding
by showing the concrete nixpkgs flow across all repositories, not just
the Codex/Claude packages. This is a broader ask: the entire
cross-repository nixpkgs dependency graph matters, not just one
package's provenance.

### 2026-08-27 — too complex; use a realized option instead

> this is too complex right now. Let's just create an option in
> criomos-home to define the codex and claude core packages, and reuse
> that definition wherever the package is needed, from the realized
> (config) side. Do you understand?

Transcript: `rollout-2026-08-27T15-51-18-01a0437d-…`, line 4304.
Agent context: The agent had proposed creating a full `criomos-core`
repository, migrating expressions, and establishing a follows chain.
My reading: The living deprioritized the repository-level solution in
favor of a pragmatic immediate step: a Home Manager option that
defines the package once and is consumed by every module. "From the
realized (config) side" means the option value propagates through the
NixOS module system, not through flake inputs or `extraSpecialArgs`.
This does NOT retract the criomos-core design — it defers it. The
living said "right now," not "never."

---

## Package ownership boundaries

### 2026-08-23 — an orca repo is smarter than cramming more stuff in the home repo

> I think an orca repo is smarter than cramming more stuff in the home
> repo

Transcript: `rollout-2026-08-23T17-00-36-01a02f23-…`, line 354.
Agent context: The agent was determining where to package Orca
(StablyAI's agent harness).
My reading: Each tool or concept with enough weight deserves its own
repository rather than being stuffed into CriomOS-home. This parallels
the Protos/Datom/Ethos pattern of concept-scoped repositories.

Vision record: `flows/01a02f23/vision/orca.md`.

### 2026-08-09 — every concept should have its repo

> If we create a signal repo, or if there isn't one, I mean, every
> concept should really have its repo, and if anything goes in there,
> the traits can, since every concept deserves at least one trait, and
> probably more.

Transcript: designer session 98fbfa47, 2026-08-09T12:30Z.
Agent context: The living was reviewing the component architecture
standard draft and deciding where the short-header idea should live.
My reading: This is the Spirit-adjacent principle underlying the
package ownership decisions. Each concept has its own repository.
This generalizes beyond Nix packaging to the entire project
architecture. For Nix, it means each meaningful concept (Orca,
Claude/Codex, Signal) should have its own flake, not be folded into
a monolith.

Psyche-raw record: `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md`.

---

## Nixpkgs and flake-input policy

### 2026-08-17 — lunar nixpkgs update pattern

> Update on the first commit exactly after the new moon every
> lunation.

Transcript: source provenance is a typed message in the local Codex
history (line reference in psyche-raw record).
Agent context: The living established the nixpkgs pin-update cadence.
My reading: This is a fixed policy: nixpkgs does not float or chase
unstable. It pins to the first commit after each new moon. This means
nixpkgs moves on a known, predictable schedule — roughly monthly.
Faster-moving packages (yt-dlp, Codex, Claude) need separate inputs
that move independently of this cadence.

Psyche-raw record: `psyche-raw/Vision/setupIndependentInterfaces.md`.

### 2026-08-10 — use main for everything

> we should use main for everything

Transcript: provenance in psyche-raw record, during Lojix recovery.
Agent context: A `schema-rust` dependency was pinned to a non-main
branch.
My reading: No non-main branch pins. Every dependency follows main.
This is not about nixpkgs specifically but about the general policy:
branches are not pin targets.

Psyche-raw record: `psyche-raw/Vision/mainForEverything.md`.

### 2026-08-19 — the flake is an entry point

> I would rather keep the flake very minimal; an entry point

Transcript: `rollout-2026-08-19T12-36-31-01a01998-…`, line 9.
Agent context: Part of the yt-dlp session opening.
My reading: The `flake.nix` file should not contain business logic,
overlay definitions, or package expressions. It is a minimal entry
point that delegates to structured imports. This is consistent with
the centralized-package-customization ruling from the same message.

---

## No stateful software installation

### 2026-08-25 — we dont allow installing software statefully

> which shouldnt even show up: we dont allow installing software
> statefully

Transcript: `rollout-2026-08-25T13-46-16-01a038be-…`, line 1034.
Agent context: GNOME Software offered to find an application for
Claude Desktop's OAuth callback.
My reading: All software installation is declarative (Nix). No mutable
package management (GNOME Software, flatpak, snap, etc.) is permitted.
This is a system-level invariant.

Vision record: `flows/01a038be/vision/installingSoftwareStatefully.md`.

---

## Lojix ownership

### 2026-08-13 — Lojix should only be in OS

> it should only be in OS

Transcript: provenance in psyche-raw record.
Agent context: The living ruled on Lojix's ownership boundary after
discovering it in both OS and Home configurations.
My reading: Lojix is system-level. Home should not carry its own Lojix
dependency or configuration. This is a clean ownership boundary.

Psyche-raw record: `psyche-raw/Vision/lojixOwnership.md`.

---

## Claude Desktop must use the declared runtime

### 2026-08-26 — force Claude Desktop to use our Claude Code

> Okay, so this shows two things. One, the Claude [Clode->Claude]
> Desktop is trying to use an obsolete version of Claude
> [Clode->Claude] code, which means the Claude [Clode->Claude] Desktop
> might be outdated. And yeah, we cannot allow the desktop to try to
> use something that it's installing statefully. So we have to modify
> the Claude [Clode->Claude] Desktop Nix code to force it to use our
> Claude [Clode->Claude] code.

Transcript: `rollout-2026-08-26T14-18-49-01a03e02-…`, line ~140.
Agent context: Claude Desktop tried to use a stale, statefully
installed Claude Code 2.1.237 while the declared Nix package was
2.1.241. The living identified two problems: the desktop using an
obsolete runtime, and the desktop installing anything statefully.
My reading: Desktop applications must consume the exact declared Nix
package for their runtime — they may not download, copy, or select
their own. This is a specific instance of the "declared once, used
everywhere" and "no stateful installation" principles converging.

Vision record: `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md`.

---

## AgentIntercomGraphical is slop; gate by what things actually need

### 2026-08-28 — AgentIntercomGraphical is a total misnomer

> AgentIntercomGraphical is a total misnomer and is now involved in a
> bunch of things it has nothing to do with (AgentIntercom is one
> thing, Graphical is another; and a duplication since we already have
> the Edge node concept)

Transcript: `rollout-2026-08-28T15-54-20-01a048a6-…`, line ~25.
Agent context: Bird on Zeus lacked Claude and Codex desktop apps. The
investigation traced the cause to the AgentIntercomGraphical composite
gate.
My reading: A composite flag that bundles unrelated concerns (agent
intercom wrappers, graphical OS prerequisites, desktop application
installation) under one misnomer is a packaging-plane defect. The
living sees three distinct things collapsed into one gate.

### 2026-08-28 — agent intercom follows Claude/Codex presence, no gate needed

> we were gating agent-intercom before because it would modify codex
> and claude, but now I only want different executables (different
> names) to be wrapped with the agent-intercom wrapped codex and
> claude, so we dont need a gate at all. so differentiate what is gated
> by this now totally inappropriate flag, which must be removed, so we
> can gate what needs to be gated with the right variables

Transcript: `rollout-2026-08-28T15-54-20-01a048a6-…`, line ~60.

> We don't need to gate agent intercom, it should be on any node that
> has Claude/codex

Transcript: same session, line ~200.
Agent context: The living decomposed the flag into its actual concerns.
My reading: Agent intercom should follow presence of Claude/Codex
(no independent gate). Desktop apps should be gated by Edge plus
Medium size. The x86 gate was also rejected: "Why is x86 a gate for
the apps?" These are packaging-plane corrections: each consumer of a
package must be gated by its actual requirements, not by a proxy flag.

Vision record: `flows/01a048a6/vision/agentIntercomGraphical.md`.

---

## Separate code from data; no unnecessary rebuilds

### 2026-08-25 — separate the rust code from the data

> problem: every time we modify the curriculum, some giant nix check
> has to run. I feel like we're recompiling the rust binary because the
> source changed? If so, we should separate the rust code from the
> data. Find out and see what's what, and how it would be fixed.

### 2026-08-25 — create a public repo and move the runtime out

> implement it. create a public repo, and move the runtime out, then
> adapt it to use an external repo for data. and port it do [to] use
> datom instead of dotos. and the cli must not use anything other than
> its datom input for configuration

Transcript: sourced from `flows/01a035d3/vision/rustCodeFromTheData.md`.
Agent context: Curriculum data changes were rebuilding the Rust
runtime binary because both lived in the same Nix derivation.
My reading: When a Nix derivation couples code and data so that
changing data rebuilds code, the fix is to separate them into distinct
repositories. The runtime owns its code; the data is an external
input. This is the same principle as "keeping the data where the data
belongs" — configuration data and runtime code have different change
cadences and should not be in the same derivation.

Vision record: `flows/01a035d3/vision/rustCodeFromTheData.md`.

---

## No hot fixes; use declarative paths only

### 2026-08-19 — dont do hot fixes; use the nix user env only

> dont do hot fixes

> use the nix user env only, or OS redeploy

Transcript: `rollout-2026-08-19T17-11-18-01a01a93-…`, lines 1878,
1894.
Agent context: Codex and Claude had resolved to broken Agent Intercom
wrappers during recovery. The agent proposed ad-hoc fixes.
My reading: The only authorized recovery paths are declarative: the
Nix user environment (Home Manager) or a full OS redeploy through
Lojix. No mutable patching, no manual binary replacement, no
imperative fixes. This constrains how package problems can be
addressed.

Psyche-raw record:
`psyche-raw/Vision/setupIndependentInterfaces.md`,
`flows/01a01a93/vision/hostEnvironmentRecovery.md`.

---

## Domain knowledge lives in its domain

### 2026-08-08 — information specific to a domain lives in that repository

> information that is specific to a specific task, to a specific
> domain needs to live in that domain, in that repository. And then
> managers don't have to tell their sub-agents how stuff is done. The
> agents will just find all the instructions along the way.

### 2026-08-09 — docs live in the code they document

> all repos should document their usage/editing patterns. better yet;
> docs live in the code they document

Psyche-raw record: `psyche-raw/Vision/domainKnowledgePlacement.md`.
Agent context: steward sessions on agent architecture.
My reading: Package-update procedures, build instructions, and
override documentation should live in the repository that owns the
package — not in a separate guide, not in the consuming repo, not in
a skill. If criomos-core owns Codex/Claude definitions, criomos-core
must document how to update them.

---

## Agent frustration with overcomplexity and slop

### 2026-08-25 — youre overcomplicating this to the extreme

> all we need to do is get the codex derivation from the same place.
> declared once, used everywhere. youre overcomplicating this to the
> extreme

(Repeated from above for thematic completeness.)
My reading: The agent introduced launcher enforcement, hostile-
environment machinery, signed-key verification, and platform-gating
complexity when the living wanted one thing: same derivation
everywhere. This is the sharpest expression of frustration with agent
overengineering in the packaging domain.

### 2026-08-27 — I feel like you dont really know what I want

> I feel like you dont really know what I want. show me how
> criomos-core works, and how you deal with nixpkgs across all the
> repos

(Repeated from above.)
My reading: The agent spent hours on the wrong implementation. The
living's frustration is not about speed but about comprehension — the
agent did not hold the design.

### 2026-08-19 — Codex session frustration with skill edits

> iv read the first two lines of the nix workflow skill and it reads
> like a fucking retard wrote it. just undo everything you did and Ill
> start a new session to tackle this with claude

Transcript: `rollout-2026-08-19T12-36-31-01a01998-…`, line 1105.
Agent context: The Codex agent had rewritten the nix-workflow skill
without the psyche reviewing it, despite the skill-design skill
requiring review.
My reading: Agent autonomy on skill edits is not acceptable. The
living wants to review changes before they land. The Codex session's
system prompt ("heavily reward autonomous completion") worked against
the psyche's explicit discipline.

---

## Not explicitly addressed

The following topics were named in the acquisition brief but have no
direct psyche ruling in the searched record:

- **CriomOS-pkgs**: The living never discussed CriomOS-pkgs' role or
  internal structure. The agent proposed "CriomOS-pkgs remains the
  general package universe" (01a0437d, line 4298) and the living did
  not object. CriomOS-pkgs is taken as given.

- **Goldragon flake**: The living mentioned `goldragon.criome` only as
  a network endpoint (the Prometheus remote builder's AP). No ruling on
  the goldragon repository's flake input structure or its relationship
  to other repositories was found.

- **Horizon-rs / lojix flake inputs**: The living discussed Horizon as
  a data source ("lojix-emitted horizon output") but did not rule on
  horizon-rs's flake input structure, its nixpkgs pin, or how lojix's
  own inputs relate to the rest of the graph. Lojix ownership is ruled
  OS-only.

- **External flakes generally**: The living accepted external flakes
  for Codex/Claude packaging and judged their audit cost comparable to
  maintaining an owned package. No general ruling on when to prefer an
  external flake vs. an owned expression was found.

- **Input upgrades across the layered structure**: The living ruled the
  lunar nixpkgs cadence and "use main for everything." The
  bottom-up update order (eval-cache boundary repos first) is agent
  codified in the `nix-input-upgrade` skill but was not directly
  stated by the living. The living's "follows" graph (all nixpkgs
  following CriomOS.nixpkgs) was confirmed implicitly when the agent
  presented it and the living continued without objection, but the
  living did not type that graph.

---

## Tensions and unresolved points

1. **criomos-core repository vs. realized option**: The living first
   designed criomos-core as a real repository (01a030e8, 01a0437d line
   486), then deferred it: "this is too complex right now. Let's just
   create an option in criomos-home" (01a0437d line 4304). The
   repository design is not retracted — the living said "right now,"
   not "never" — but the immediate path is a Home Manager option. The
   tension: the living simultaneously wants a separate source repo
   (common ground, separate from OS and Home) and finds a new repo too
   complex for the current moment.

2. **External flakes vs. owned expressions**: The living said "I dont
   see how auditing the external flake is more work than auditing one
   which we maintain" (01a0338f line 1000), but later in 01a0437d
   directed the Codex/Claude expressions to be owned ("import/adapt
   the code we want from llm-agents"). The resolution may be that
   audit cost is not the decision variable — control over the
   single-stack contract is. But the living did not state this
   explicitly.

3. **"Home ostensibly, right?" captured as ruling**: The living's
   questioning inflection in 01a0437d line 516 was treated by the
   agent as confirmation that Home should own the derivations. The
   living later corrected: "they were moving into criomos-core."
   This pattern — tentative question captured as settled design —
   recurs in several flows and the living's frustration with it is
   visible.

4. **extended-horizon as repository vs. concept**: The agent proposed
   a full repository anatomy for extended-horizon after the living
   merely floated the idea. The living caught this: "you mean that
   repo already existed?" The distinction between a concept the
   psyche is considering and a concrete authorization is a recurring
   problem in the record.

---

## Sources

### Codex transcripts searched

| Session file | Flow | Date | Key topics |
|---|---|---|---|
| `rollout-…-01a02b4b-…` | 01a02b4b | 2026-08-22/23 | Embedded/independent Home equivalence, extended-horizon |
| `rollout-…-01a030a1-…` | 01a030a1 | 2026-08-23/24 | Common ground, separate repo, indirection is bad design |
| `rollout-…-01a030e8-…` | 01a030e8 | 2026-08-24 | criomos-core proposal, core supersedes lib |
| `rollout-…-01a0338f-…` | 01a0338f | 2026-08-24/25 | Desktop packaging, audit protocol, TUI/desktop version alignment |
| `rollout-…-01a038be-…` | 01a038be | 2026-08-25 | Codex derivation, declared once used everywhere, no stateful install |
| `rollout-…-01a01998-…` | 01a01998 | 2026-08-19 | yt-dlp, central package customization, flake as entry point, skill frustration |
| `rollout-…-01a0437d-…` | 01a0437d | 2026-08-27 | criomos-core.[codex,claude], nixpkgs across repos, realized option fallback |
| `rollout-…-01a02f23-…` | 01a02f23 | 2026-08-23 | Orca repo, Herdr/Orca packaging |
| `rollout-…-01a03e02-…` | 01a03e02 | 2026-08-26 | Claude Desktop must use declared Claude Code |
| `rollout-…-01a04881-…` | 01a04881 | 2026-08-28 | AgentIntercomGraphical is slop |
| `rollout-…-01a048a6-…` | 01a048a6 | 2026-08-28 | Decompose AgentIntercomGraphical gate |
| `rollout-…-01a01a93-…` | 01a01a93 | 2026-08-19 | No hot fixes; use Nix user env or OS redeploy |
| `rollout-…-01a035d3-…` | 01a035d3 | 2026-08-25 | Separate Rust code from data |

### Psyche records read

| Path | Topic |
|---|---|
| `flows/01a030a1/vision/commonGround.md` | OS/Home common ground ruling |
| `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md` | criomos-core, core supersedes lib |
| `flows/01a02b4b/vision/homeEquivalence.md` | Embedded/independent Home, extended-horizon |
| `flows/01a0338f/vision/tuiAndDesktopVersions.md` | TUI/desktop version alignment |
| `flows/01a0338f/vision/packageAuditProtocol.md` | Package audit protocol |
| `flows/01a038be/vision/codexDerivation.md` | Declared once, used everywhere |
| `flows/01a038be/vision/installingSoftwareStatefully.md` | No stateful installation |
| `flows/01a0437d/vision/codexAndClaude.md` | Only Codex and Claude in scope |
| `flows/01a02f23/vision/orca.md` | Orca gets its own repo |
| `psyche-raw/Vision/setupIndependentInterfaces.md` | Lunar nixpkgs pin, setup-independent interfaces |
| `psyche-raw/Vision/mainForEverything.md` | Use main for everything |
| `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md` | Every concept owns a repo |
| `psyche-raw/Vision/lojixOwnership.md` | Lojix is OS-only |
| `psyche-raw/Vision/skillsRepoSourceOnly.md` | Skills repo is source-only |
| `psyche-raw/Vision/domainKnowledgePlacement.md` | Domain knowledge in its domain |
| `psyche-raw/Vision/minimalFlake.md` | Keep the flake minimal |
| `flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md` | Claude Desktop must use declared runtime |
| `flows/01a048a6/vision/agentIntercomGraphical.md` | AgentIntercomGraphical decomposition |
| `flows/01a04881/vision/cause.md` | Cause identification frustration |
| `flows/01a01a93/vision/hostEnvironmentRecovery.md` | No hot fixes |
| `flows/01a035d3/vision/rustCodeFromTheData.md` | Separate code from data |
| `flows/01a030e8/reports/criomosCoreProposal.md` | Agent proposal (for contrast) |
