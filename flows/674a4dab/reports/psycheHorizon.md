# Psyche acquisition: the data / schema plane

What the living psyche wanted for `horizon-rs` (Horizon),
`criomos-horizon-config`, and how node/host/user data, capabilities,
and configuration are meant to be expressed, stored, and consumed by
CriomOS, CriomOS-home, Goldragon, and Lojix.

---

## Horizon is minimal: WHAT, never HOW

The oldest and most consistently repeated principle.

### "Horizon should be elegant and minimal"

> Horizon and the cluster-data it carries should be elegant and minimal:
> express only **what** the psyche (as cluster user) wants the cluster to
> do, never **how** and never decision-making. Horizon emits simple typed
> facts that Nix consumes; Nix composes those facts into the more complex
> decisions, so complexity stays out of Horizon.

— psyche, captured in Spirit record `7ggswqdxqqz97za6o7w` (Principle,
High), Designer session on 2026-06-04; reported in
`reports/PreResetCorpus-2026-06-07/reports/cloud-designer/23-horizon-lojix-rewrite-audit-2026-06-04/1-intent-agglomerated-subject.md:22–29`.

Agent context: the pre-reset design audit distilled this as the apex
Horizon principle, traced to an earlier 2026-05-20 Maximum-certainty
legacy Principle in `intent/horizon.nota:15-20`: cluster data must not
embed operational constants — ports, derived addresses, well-known
constants live in the *consumer*, not Horizon. A corollary rule stated
"prefer beautiful Horizon over beautiful Nix — ugliness goes in Nix."

**My reading:** this is the governing intent for the entire plane.
Horizon is a data pass-through, not a decision engine. Every derived
boolean, every computed domain name, every policy choice that currently
lives in `horizon-rs` is there on sufferance — tolerated as a "hack
for now," not as the terminal design. The psyche's intent is that Nix
(the consumer) should compose facts into decisions, and Horizon should
carry only the declared cluster facts.

### "Horizon stays a hack for now"

> Horizon is a hack for now, and that's fine. Logix is the more
> traditional component.

— psyche, captured in Spirit record `1bok2bxvu3beswif9mv` (Clarification,
High), Designer session on 2026-06-04; reported in the same audit,
`1-intent-agglomerated-subject.md:59–82`.

Agent context: this resolved a long-open question about whether Horizon
should become a full triad component (Signal/Nexus/SEMA runtime).
The answer was no: Horizon stays the simple projection surface; Lojix
carries the full triad-engine + schema-based-component port.

**My reading:** the psyche accepted Horizon's current "hack" shape but
only because the terminal design is even simpler. The "hack" label is
permission to simplify further, not permission to add machinery.

---

## No cluster-specific data in CriomOS

### "Everything should come from the Horizon"

> I don't want any node or cluster-specific data in those repositories.
> Everything should come from the Horizon.

-- psyche, dictated, 2026-05-10 (ts 1778582678);
`~/.codex/history.jsonl` line 2193.

Agent context: the psyche was directing a survey of CriomOS and
CriomOS-home for hardwired cluster-specific values. The psyche
exempted implementation catalogs (LLM models) that do not vary
per cluster but flagged WiFi passwords as belonging in the secrets
infrastructure (ClaviFaber), not Nix source.

### "move node name gates into Horizon for sure"

> move node name gates into Horizon for sure. You know, no name
> equals Oranos [STT: Ouranos], no name equal [STT: equals]
> Prometheus. This should not be in the code [...] what we're
> trying to figure out by this node names equals Uranus [STT:
> Ouranos] is something completely different than what the host
> name is. It's more like what's its role [...] is there an AI
> node in the cluster? If yes, then we have an AI provider

-- psyche, dictated, 2026-05-10 (ts 1778585249);
`~/.codex/history.jsonl` line 2201.

Agent context: the psyche identified `node.name == "ouranos"` and
`node.name == "prometheus"` patterns in CriomOS Nix source as slop
introduced by an agent. The correct question is about the node's role
(e.g., "is there an AI node?"), not its name. The psyche directed that
this wisdom be encoded in skill files and architecture documents.

**My reading:** this is a foundational ruling: CriomOS is
network-neutral and must never key off node names. What looks like
a node-name check is actually a role query, and roles are expressed as
typed Horizon facts (NodeService variants). Node names are used only
for hostnames and identity, never for control flow.

---

## Cluster data is "a bunch of dials"

### "the cluster data should be a bunch of dials to turn shit on and off"

> the cluster data should be a bunch of dials to turn shit on and off,
> with host name, and stuff like disks and hardware info. all the
> complicated stuff is in the horizon reduction and criomos

-- psyche, typed, 2026-05-18 (ts 1779144353);
`~/.codex/history.jsonl` line 2859.

### "variants first"

> and by dials to turn shit on and off, I mean *variants first* -
> self-describing stuff like [NixBuilder NixCache PersonaDevelopment
> SomeOtherOptionalNodeFeature ...] - along with the majore [STT:
> major] node variant, etc

-- psyche, typed, 2026-05-18 (ts 1779144452);
`~/.codex/history.jsonl` line 2861.

### "give me a vector of variants, not this meaningless series of booleans"

> ok, all this "true none true" is fine from some stuff, but it's so
> lacking in information. I want to see Variants! give me a vector of
> variants, not this meaningless series of booleans and options! the
> horizon is so fucking ugly!

-- psyche, typed, 2026-05-18 (ts 1779144227);
`~/.codex/history.jsonl` line 2856.

Agent context: the psyche was reviewing the pre-redesign cluster
proposal source and found sequences of `True None True` unreadable.
The immediate preceding entry (ts 1779143826) shows the specific
trigger: seeing `(NodeServices Client (Server 8443 "tailnet.goldragon.
criome") (Workstation (RepositoryReceiveRole true))))` and reacting
"wtf is this? all it needs is a single variable to know this node is
for personaDevelopment."

**My reading:** the psyche's vision for the cluster proposal's shape
is clear: a node carries a species (its major variant), hardware
facts, and a vector of self-describing NodeService variants. Each
variant names the capability and can carry inline data. The current
`goldragon/datom.dotos` has realized this shape -- the services vector
`[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]` is the enacted
vision. The "complicated stuff" -- policy, port numbers, domain
composition -- belongs in Horizon's projection logic or in CriomOS.

---

## Pan-horizon vs. cluster boundary

### "there shouldnt be criome and criome.net in cluster data"

> there shouldnt be criome and criome.net in cluster data - those are
> horizon constants

-- psyche, typed, 2026-05-17 (ts 1778999875);
`~/.codex/history.jsonl` line 2705.

### "everything in the report you made doesnt belong in cluster data"

> everything in the report you made *doesnt* belong in cluster data.
> it either goes in horizon and or criomos. the vpn configuration is
> in criomos, and the cluster data only selects providers, a vector
> of variants (provider names) that carry the data of their config
> (favored server location, etc)

-- psyche, typed, 2026-05-17 (ts 1779000726);
`~/.codex/history.jsonl` line 2709.

### "put the pan-horizon config in a new criomos-horizon-config repo"

> start working on the lean-horizon, but rebase it all on
> horizon-regengineering [STT: re-engineering] all its sibling branches
> [...] put the pan-horizon config in a new criomos-horizon-config repo.
> work all the way until the new lojix and new horizon are able to build
> all the components of criomos

-- psyche, typed, 2026-05-17 (ts 1779002394);
`~/.codex/history.jsonl` line 2714.

Agent context: the psyche had just reviewed an agent report identifying
domain names, subnet CIDRs, and DHCP pool data in the cluster proposal.
The psyche ruled: these are pan-horizon constants, not cluster data.
The cluster selects providers as a vector of variants; the horizon and
CriomOS own constants and implementation.

**My reading:** this is the origin story of `criomos-horizon-config`.
The boundary is sharp: cluster data (goldragon) carries per-cluster
declarations -- node hardware, species, services. Pan-horizon config
(criomos-horizon-config) carries identity and temporary network facts
that are not per-cluster but would differ between independent horizon
operators. CriomOS owns implementation and well-known constants.
`horizon-rs` derives projected views from both. The psyche's ruling
makes the three-input architecture explicit.

---

## Horizon should be "just the reducer"

> some of the stuff that we moved out of CriomOS into the Horizon can
> really even go back into CriomOS because we don't need to introduce
> all of this code into the Horizon. Horizon should mostly be just the
> reducer. [...] We don't need to put everything into Horizon, especially
> really dumb stuff [...] We're just inflating the Rust code

-- psyche, dictated, 2026-05-17 (ts 1779012989, within a longer
response at `~/.codex/history.jsonl` line 2727).

Agent context: this was part of a long dictation answering the
lean-horizon design questions. The psyche was responding to the
question of whether reserved subdomains should be configurable and
where domain composition logic belongs.

**My reading:** a direct qualification of the "WHAT, never HOW" rule.
Horizon should be a minimal reducer: take cluster data + pan-horizon
config, validate, project, emit. Domain composition like
`git.<cluster>.criome` can live in CriomOS as a simple string concat.
The psyche explicitly does not want `horizon-rs` to grow into a large
Rust codebase handling concerns that are naturally expressed in Nix.

---

## Per-user horizon settings

### "per-user horizon setting"

> we need a per-user horizon setting to disable the fast-repeat keyboard
> tweak

-- psyche, typed, 2026-05-04 (ts 1775387512987);
`~/.claude/history.jsonl` line 3238.

### "implement preferredEditor in horizon-rs"

> remove the unfinished textsize and implement preferredEditor (with
> default to emacs) in horizon-rs. another agent is working on
> criomos-home

-- psyche, typed, 2026-05-07 (ts 1778310860625);
`~/.claude/history.jsonl` line 5306.

### "display density"

> text size isnt what I wanted to represent anyway. what does DPI stand
> for? Im talking about the density of the UI in applications. and if
> its framed as a preference, then None is default

-- psyche, typed, 2026-05-07 (ts 1778158263406);
`~/.claude/history.jsonl` line 5085.

Agent context: the psyche wanted per-user preferences in the Horizon
user model for editor choice and UI density. Both have been at least
partially implemented in the `User` struct of `horizon-rs`.

**My reading:** the Horizon user model is not only about key material
and identity -- it also carries user preferences that CriomOS-home
consumes to configure the user's environment (editor, UI density,
keyboard tweaks). The per-user size field (Zero/Min/Medium/Large/Max)
already governs which Home packages are installed; the psyche wants
richer per-user preferences alongside it.

---

## The federation vision

> I would like people to be able to host their own meta-clusters. So
> maybe they want to use a different domain name than .creome.net [STT:
> .criome.net] because they register their own sort of federated
> network. So this is how they'll be able to use Logix [STT: Lojix] to
> [deploy their own]

-- psyche, dictated, 2026-05-17 (ts 1779012989, within the same
longer response, `~/.codex/history.jsonl` line 2727).

Agent context: this was answering the question "should Lojix daemon
require the pan-horizon config path in typed configuration?" The
psyche confirmed yes: Lojix needs both the pan-horizon config and
the cluster data to create the horizon. The pan-horizon config is
what allows independent operators to federate with different domain
names.

**My reading:** the three-input architecture (goldragon cluster data +
criomos-horizon-config pan-horizon config + horizon-rs projection) is
explicitly motivated by federation. Different operators author
different cluster data and different pan-horizon config; the same
horizon-rs projection engine serves all of them. This is the deepest
"why" behind `criomos-horizon-config` as a separate repository.

---

## Implementation catalogs belong in CriomOS, not Horizon

> the gguf model catalog belongs in criomos; they're *system
> derivations*!

-- psyche, typed, 2026-05-17 (ts 1779010184393);
`~/.claude/history.jsonl` line 6289.

Agent context: the lean-horizon design audit asked where AI model
files should be materialized. The psyche ruled they are system
derivations -- Nix packages -- and belong in CriomOS, not in Horizon.

**My reading:** Horizon carries the declaration that a node has a
certain role (e.g., LargeAiRouter). CriomOS owns the implementation
catalogs (which models, which packages, which ports). This is another
instance of the WHAT/HOW separation applied to data.

---

## Horizon data types: no input/output duplication

> Horizon data types should not repeat themselves across inputs and
> outputs: where the input type can also serve as the output type,
> reuse it rather than defining parallel in/out types. Fewer, reused
> types keep the model small.

— psyche, captured in Spirit record `10v4744869xt5spwnam` (Principle,
High), Designer session on 2026-06-04; reported in
`1-intent-agglomerated-subject.md:43–57`.

Agent context: `horizon-rs` currently has separate `*Proposal` input
structs and `Node`/`Horizon`/`Cluster` enriched output structs. The
lean rewrite on `horizon-leaner-shape` has already collapsed some
derived fields but the split remains.

**My reading:** a direct structural criticism of the current codebase.
The psyche wanted fewer types, not more — the in/out split is a cost,
not a feature. This aligns with "minimal" above.

---

## Cluster data must be typed end-to-end, source-first

> Cluster-data features must be typed end-to-end, and the correct
> order is typed-source-first.

— psyche, captured in Spirit record `431pfi7l1akuu22b01b` (Correction,
High), 2026-06-04; reported in `1-intent-agglomerated-subject.md:94–113`.

Agent context: this arose from a concrete failure. The VmTesting feature
was modeled as a string in Nix, not as a typed `NodeService` variant in
`horizon-rs`. The psyche ruled the canonical pipeline:

1. Extend the `horizon-rs` model with a real typed `NodeService` enum
   variant carrying `NotaEncode`/`NotaDecode`.
2. Author the fact in `goldragon`'s `datom.nota` (STT correction: was
   `datom.dotos` in the original reports; the proposal source has since
   migrated to datom).
3. Project it typed through `horizon-rs`.
4. Consume the typed value in CriomOS.

Explicitly forbidden: string keys at schema positions, defensive
or-empty-list defaults, and synthetic-fixture-fed checks.

**My reading:** "typed end-to-end, source-first" is the strongest
engineering directive. No feature should be expressed as a string when
it could be a typed variant. This governs how new capabilities enter
the system.

---

## Variants over booleans

> Express a fact as a data-carrying variant where inline tuning is part
> of the dial, not a boolean flag.

— psyche, from `intent/horizon.nota:1-13`, refreshed in the 2026-06-04
audit `1-intent-agglomerated-subject.md:45–47`.

Agent context: the `horizon-leaner-shape` rewrite already removed
several `is_*` boolean fields. The principle is that a NodeService
carries a variant (e.g., `NixBuilder { maximum_jobs: Option<u32> }`)
rather than a bare `is_remote_nix_builder: bool` with separate data.

**My reading:** this is a specific application of "typed end-to-end" to
the type design. It is consistent across every Horizon discussion I found.

---

## AgentIntercom capabilities are opt-in, not implicit

### "it should be behind a feature flag in horizon"

> also, her codex is broken: [error output] what is going on? Can we
> disable this intercom stuff by disabling a feature on zeus? it should
> be behind [STT correction: "behind"] a feature flag in horizon

— psyche, typed, 2026-07-28;
`~/.codex/sessions/2026/07/28/rollout-…-019fa893-…-.jsonl` line 1194.

Agent context: Bird's Codex on Zeus was replaced by the Agent Intercom
wrapper, which waited for a socket that did not exist. The psyche
expected Horizon feature flags to control whether intercom was active.

### "then *that* is wrong. I never asked for this"

> \> Horizon currently hard-requires AgentIntercomLocal on every trusted
> node
>
> then \*that\* is wrong. I never asked for this, so this implementation
> is wrong

— psyche, typed, 2026-07-28; same transcript, line 1271.

Agent context: the agent reported that Horizon hard-required
AgentIntercomLocal on every trusted node. The psyche rejected this
categorically.

**My reading:** the psyche was clear that trust and AgentIntercom are
independent axes. A node being trusted does not mean it has or wants
AgentIntercom. This is a direct statement about Horizon's capability
model: capabilities are opt-in per node, never implied by other
properties.

### "this agentintercomgraphical is slop"

> this agentintercomgraphical is slop.

— psyche, typed, 2026-08-28;
`~/.codex/sessions/2026/08/28/rollout-…-01a04881-…-.jsonl` line 218.
`flows/01a04881/vision/agentIntercomGraphical.md`.

### "AgentIntercomGraphical is a total misnomer"

> AgentIntercomGraphical is a total misnomer and is now involved in a
> bunch of things it has nothing to do with (AgentIntercom is one thing,
> Graphical is another; and a duplication since we already have the Edge
> node concept)

— psyche, typed, 2026-08-28;
`~/.codex/sessions/2026/08/28/rollout-…-01a048a6-…-.jsonl` line 64.
`flows/01a048a6/vision/agentIntercomGraphical.md`.

### "we dont need a gate at all"

> we were gating agent-intercom before because it would modify codex and
> claude, but now I only want different executables (different names) to
> be wrapped with the agent-intercom wrapped codex and claude, so we
> dont need a gate at all. so differentiate what is gated by this now
> totally inappropriate flag, which must be removed, so we can gate what
> needs to be gated with the right variables

— psyche, typed, 2026-08-28; same transcript, line 141.
`flows/01a048a6/vision/agentIntercomGraphical.md`.

### "We dont need to gate agent intercom"

> We don't need to gate agent intercom, it should be on any node that
> has Claude/codex

— psyche, typed, 2026-08-28; same transcript, line 803.
`flows/01a048a6/vision/agentIntercomGraphical.md`.

Agent context: the psyche was shown that AgentIntercomGraphical gated
generic graphical prerequisites (AT-SPI, uinput, WLR portals), desktop
apps, and agent-specific GUIs — none of which are about AgentIntercom.
Edge already owns the general graphical substrate. The flag was deleted
and its consumers were re-gated by what they actually need.

**My reading:** the psyche wants Horizon capabilities to name exactly
what they mean, one concept per flag, no compound flags. AgentIntercom
follows Claude/Codex presence — it is not a node capability in the
Horizon sense at all. Graphical requirements belong under Edge.
This episode is a concrete instance of "WHAT, never HOW" applied
to the capability model.

---

## Horizon is the sole source of setup-specific facts

### "there should be no difference between embedded and independent home"

> there should be no difference between the embedded and independent
> home. the part which is shared ought to be directly from lojix-emitted
> horizon output, or from a shared nix machinery which uses the said
> horizon as input only. embedded home should be only the absolute
> minimum nix code necessary to embed a home logic which is otherwise
> completly [STT/typing as-is] identical. Do you understand what I mean?

— psyche, typed, 2026-08-23;
`~/.codex/sessions/2026/08/22/rollout-…-01a02b4b-…-.jsonl` line 880.
`flows/01a02b4b/vision/homeEquivalence.md`.

### "whatever in home is currently originating in the OS must originate from the horizon"

> whatever in home is currently originating in the OS must originate
> from the horizon or the extended-horizon (that could be a standalone
> repo for deriving some data in nix from the horizon data coming out
> of lojix)

— psyche, typed, 2026-08-23; same transcript, line 905.
`flows/01a02b4b/vision/homeEquivalence.md`.

Agent context: the embedded Home (inside NixOS) and the independent Home
(standalone Home Manager) were producing different activations because the
embedded path inherited NixOS context (locale, Stylix, osConfig). The
psyche ruled the only allowed input: Horizon and whatever is
deterministically derived from Horizon.

### "you mean that repo already existed?"

> \> Yes. extended-horizon is not another authority; it is a deterministic
> derivation layer over Horizon.
>
> you mean that repo already existed?

— psyche, typed, 2026-08-23; same transcript, line 932.

Agent context: the agent had spoken too definitively about
`extended-horizon`. The psyche caught the false confidence. No
`extended-horizon` repository existed or was authorized.
`flows/01a030a1/reports/extendedHorizonReacquisition.md` records the
correction.

**My reading:** the psyche established Horizon as the single source of
truth for all setup-specific facts that Home consumes. Extended-horizon
is a possible deterministic derivation layer, not a separate authority.
The agent's diagrams showing the data flow were not approved as Intent;
the psyche's own words are narrower than the agent's proposal. The
psyche wants the contract but has not yet ruled the repository anatomy
or the interface shape.

---

## The common ground belongs in a separate source repo

### "abstract the common ground between OS and home to a separate repo"

> to me, this looks like a need to abstract the common ground between
> OS and home to a separate repo, and using that repo as the source for
> anything that is shared between them. indirection is bad design

— psyche, typed, 2026-08-24;
`~/.codex/sessions/2026/08/23/rollout-…-01a030a1-…-.jsonl` line 605.
`flows/01a030a1/vision/commonGround.md`.

### "core is more accurate than lib"

> I think core is more accurate than lib, yes, so superseding is the
> right perspective.

— psyche, typed, 2026-08-25;
`~/.codex/sessions/2026/08/24/rollout-…-01a030e8-…-.jsonl` line 540.
`flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`.

### "horizon service? wtf?"

> horizon service? wtf?

— psyche, typed, 2026-08-25; same transcript, line 621.

Agent context: the agent had referred to a "malformed horizon service."
The psyche rejected the term. The agent corrected itself: there is no
"Horizon service" component; only entries in `node.services` field of
Horizon's emitted data.

**My reading:** `criomos-core` supersedes `CriomOS-lib` as the
dependency-free shared Nix interpretation layer. Its only authority is
pure interpretation of already-emitted Horizon values and static
authored data. It does not author Horizon, and it has no flake inputs.
Horizon and criomos-horizon-config retain schema and fact authority.
The psyche is clear that indirection (Home obtaining shared values
through the OS, or vice versa) is bad design.

---

## Nothing hardwired: all site-specific data through typed input

### "make sure nothing no host names or anything like that is hardwired into lojix"

> make sure nothing no host names or anything like that is hardwired
> into lojix

— psyche, typed, 2026-08-01;
`~/.codex/sessions/2026/08/01/rollout-…-019fbf4a-…-.jsonl` line 3801.

### "CLIs cannot accept any argument other than the typed input object"

> An agent broke the invariant. Get rid of the flag and expose the
> option through nota/dotos. Remove any and all flags from lojix,
> replace them all. CLIs cannot accept any other type of argument than
> the typed input object. I feel like I keep repeating myself.

— psyche, typed, 2026-08-14;
`psyche-raw/Vision/setupIndependentInterfaces.md`, lines 14–16.

Agent context: `--override-input horizon <path>` was a command-line
flag. The psyche ruled that all CLI input goes through the typed
DOTOS/NOTA/Datom object — no flags on any component CLI.

### "those variables are confusing"

> it doesnt matter why. those variables are confusing. we should rely
> on good training instead of trying to hardwire which node all
> situations should use, which is obviously wrong

— psyche, typed, 2026-08-23;
`~/.codex/sessions/2026/08/23/rollout-…-01a02fe5-…-.jsonl` line 1173.

### "remove those hard wired deployment variables"

> remove those hard wired deployment variables and propose skill
> training that explains how the cluster works, what the nodes are, how
> to verify which node one is working on or building or deploying
> on/for, etc etc

— psyche, typed, 2026-08-23; same transcript, line 1231.

**My reading:** the psyche consistently objects to hardwired site-specific
values. Configuration enters through typed data objects only (Horizon
for cluster facts, Datom for CLI input). Agent training, not hardwired
variables, teaches agents what the cluster looks like.

---

## Lojix owns deployment; Lojix is OS-only

### "it should only be in OS"

> it should only be in OS

— psyche, typed, 2026-08-13;
`psyche-raw/Vision/lojixOwnership.md`, line 9.

Agent context: after learning that Lojix appeared in both OS and Home
configurations.

### "the interface is lojix and meta-lojix CLI only"

> Seems like letting agents "fix" it ended up abandoning my vision. The
> interface is lojix and meta-lojix CLI only.

— psyche, typed, 2026-08-14;
`psyche-raw/Vision/setupIndependentInterfaces.md`, lines 8–9.

Agent context: an agent had created `ouranos-activate.sh` as a
deployment workaround. The psyche ruled all deployment goes through the
Lojix CLI, not parallel scripts.

### "I dont care about any past lojix database"

> I dont care about any past lojix database.

— psyche, typed, 2026-08-13T23:32:19+02:00;
`psyche-raw/Vision/lojixOwnership.md`, line 17.

Agent context: the psyche removed preservation of the existing Lojix
database as a recovery requirement while asking for a clean working
Lojix service.

### "the system has to be redeployed with only the newer Lojix daemon"

> the system has to be redeployed with only the newer Lojix daemon,
> nothing else. And then we can use Lojix to deploy the upgrade. That
> should have been done already.

— psyche, typed, 2026-08-14T09:06+02:00;
`psyche-raw/Vision/lojixOwnership.md`, line 26.

Agent context: the installed daemon (0.11.0, schema v2) could not read
its store (schema v4, written by 0.17.x), blocking deployment. The
psyche ruled the ordering: redeploy with the newer daemon first, then
use it to deploy upgrades.

**My reading:** Lojix is the sole deployment interface; it is OS-owned
infrastructure. Home does not contain Lojix. Deployment goes through
the designed CLI, never through ad-hoc scripts. The psyche views the
Lojix database as transient operational data, not precious — bootstrap
the tool before using it. The frustration ("should have been done
already") suggests agents were spending effort on recovery instead of
the straightforward redeploy-then-upgrade path.

---

## Nix-owned environment must stay Nix-controlled

### "any part of the environment already controlled through nix must remained controlled through nix"

> no. any part of the environment already controlled through nix
> (criomos/home) must remained [STT/typing as-is] controlled (fixed,
> updated, maintained) through nix.

— psyche, typed, 2026-07-28;
`~/.codex/sessions/2026/07/28/rollout-…-019fa893-…-.jsonl` line 1405.

### "only criomos home is allowed"

> only criomos home is allowed. what is this .local bullshit?

— psyche, typed, 2026-07-28; same transcript, line 1384.

Agent context: an agent had placed files under `/home/bird/.local/bin/`
as a hotfix. The psyche rejected any environment mutation outside the
Nix-managed path.

**My reading:** the Nix-managed path (CriomOS for OS, CriomOS-home for
user environment) is the only authority. This means Horizon data that
feeds these consumers must itself be available through the Nix evaluation
(as a flake input), never through runtime file discovery or ad-hoc state.

---

## Separate Rust code from data

### "we should separate the rust code from the data"

> problem: every time we modify the curriculum, some giant nix check
> has to run. I feel like we're recompiling the rust binary because the
> source changed? If so, we should separate the rust code from the data.
> Find out and see what's what, and how it would be fixed.

— psyche, typed, 2026-08-25;
`flows/01a035d3/vision/rustCodeFromTheData.md`, line 7.

### "create a public repo, and move the runtime out"

> implement it. create a public repo, and move the runtime out, then
> adapt it to use an external repo for data. and port it do [STT
> correction: "to"] use datom instead of dotos. and the cli must not
> use anything other than its datom input for configuration, so add the
> variables you need to the config type which is used to read the cli
> datom input.

— psyche, typed, 2026-08-25; same file, line 13.

Agent context: the curriculum stack was a single repo containing Rust
runtime and authored skill data; any data change triggered a Rust
rebuild. The psyche ruled the separation: runtime in its own public
repo, data in the external Curriculum repo, transport via Datom (not
DOTOS), and CLI configuration exclusively through the typed Datom input.

**My reading:** this is a concrete application of the general principle
to the curriculum stack, but the principle is universal: Rust code and
authored data belong in separate repositories; the CLI receives all
configuration through typed input, never through command-line flags or
environment variables. This principle also applies to `horizon-rs` and
`criomos-horizon-config` — the config data and the projection engine
are separate.

---

## Every concept should have its repo

> If we create a signal repo, or if there isn't one, I mean, every
> concept should really have its repo, and if anything goes in there,
> the traits can, since every concept deserves at least one trait, and
> probably more.

— psyche, spoken, 2026-08-09;
`psyche-raw/Vision/everyConceptShouldHaveItsRepo.md`.

**My reading:** this governs the repository topology. `horizon-rs` is
the concept "Horizon" — the cluster projection engine. `criomos-horizon-config`
is the concept "pan-horizon constants." `goldragon` is the concept
"the Goldragon cluster" — where authored cluster facts live. Lojix is
the concept "deployment orchestration." criomos-core is the concept
"shared Nix interpretation." Each concept owns a repository; concepts
should not be conflated into compound repositories.

---

## GPG/SSH keygrip comes from cluster data

> That should be set using cluster data in criomos-home.

— psyche, typed, 2026-08-16;
`psyche-raw/Vision/setupIndependentInterfaces.md`, lines 21–23.

Agent context: the GPG keygrip in `~/.gnupg/sshcontrol` was missing
from a new home-manager generation.

**My reading:** concrete evidence that the psyche expects Horizon to
carry user-level data (SSH/GPG key identities) that Home consumes.
This is consistent with the `User` struct in `horizon-rs` already
carrying `keygrip`, `ssh_pub_keys`, and similar fields.

---

## Tensions and unresolved points

### 1. extended-horizon: concept without settled anatomy

The psyche said "that could be a standalone repo for deriving some data
in nix from the horizon data coming out of lojix" but immediately
challenged the agent's over-definite description. The concept exists
(a deterministic Nix derivation layer over Horizon) but the repository
name, public output shape, and the distinction between mechanics and
policy have not been ruled.

### 2. What exactly Horizon carries vs. what extended-horizon derives

The psyche ruled that Home values currently inherited from the OS must
come from Horizon or extended-horizon. But the boundary between what
Horizon itself emits (Rust-projected cluster facts) and what
extended-horizon derives (Nix-resolved locale, styling, package
choices) is undrawn. The agent proposed an inventory of "leaks" to
move, but the psyche did not approve it.

### 3. criomos-core vs. extended-horizon: overlapping purposes?

`criomos-core` is described as the dependency-free pure Nix
interpretation layer; `extended-horizon` was described as a
deterministic Nix derivation layer over Horizon. These might be the
same thing, or they might be distinct: core interprets emitted values,
extended-horizon derives new values from them. The psyche has not
stated the relationship.

### 4. Horizon service interpreter: where should malformed values fail?

The `criomos-core` proposal asked whether the Nix-side service
interpreter should be strict (reject malformed service values) or
whether `horizon-rs` should reject them before projection. The psyche
ruled that core supersedes lib, but the failure-boundary question
remains open.

### 5. "Hack for now" — how far does simplification go?

The pre-reset audit identified many derived fields that could move to
Nix composition (`BehavesAs`, `is_*` booleans, `criome_domain_name`,
`handle_lid_switch_*`). The lean rewrite removed some. But the psyche
has not explicitly ruled how many derived fields should survive in
`horizon-rs` vs. move to Nix. The principle ("WHAT, never HOW")
suggests most derived fields should move, but the psyche has not
drawn the line.

### 6. Datom is for the text edge, not the wire

The psyche corrected a claim that "everything is datom":

> no, this is false. all our components speak signal, not datom;
> datom is only used at the edge to let text-based systems (LLMs and
> all existing editors) understand signal.

-- psyche, `flows/ac1e9ec8/vision/datomSyntax.md`, lines 108-112.

This limits Datom's role in the data plane: Horizon data is
*authored* in Datom (the text edge), but the internal representation
and wire format are Signal/rkyv, not Datom. This is consistent with
the Horizon DESIGN.md rule "DOTOS in, JSON out" (JSON for Nix
consumption, not for human authoring or wire transport).

### 7. NodeSpecies + NodeService role-merge: settled but unimplemented

The pre-reset audit (2026-06-04, `cloud-designer/23/1-intent-
agglomerated-subject.md:276-299`) identified a settled Maximum/Medium
intent from 2026-05-21 to merge `NodeSpecies` and `NodeService` into
a single `roles: Vec<Role>` field. The audit called this "the single
most consequential finding for an implementer." The psyche has not
re-confirmed or deferred this merge in recent sessions.

**My reading:** if this merge is still intended, it would unify the
two current top-level node axes (species = what the node IS,
services = what features it has) into one vector of role variants.
This would make the cluster proposal even more "dial-like" --
a single vector of self-describing roles per node. But the psyche's
recent sessions have not mentioned it, and the current code keeps
them separate. This is an unresolved open question.

### 8. DOTOS to Datom migration for cluster data

`goldragon/datom.dotos` is the current authored cluster proposal. The
curriculum stack was explicitly migrated from DOTOS to Datom. Whether
`goldragon`'s cluster proposal similarly migrates to Datom, and whether
`criomos-horizon-config` migrates, has not been explicitly ruled for
those consumers, though the general direction is clear:

> we don't need to worry about the old repo. We're just going to move
> forward and migrate everything to datum [Datom].

— psyche, dictated, 2026-08-11T17:35+02:00
(`psyche-raw/Vision/archive-threeStacks.md`); bracketed reading is an
agent transcription repair.

### 9. Deployment manifests: the missing typed authority

Flow 01a048a6's deployment preflight block records that no authoritative
`manifests/*.dotos` selection supplies the required explicit store/SSH
transport, builder, selector, and input mode for Ouranos and Zeus. The
psyche ordered deployment ("Great. Implement and merge on main then
deploy ouranos and zeus" — line 274) and it was blocked by this gap.
This is not a psyche ruling but a structural consequence of the
no-flags invariant: if everything enters through typed input, and the
manifests that carry that input don't exist, deployment cannot proceed.

### 10. The three stacks: frozen legacy vs. new Datom/Ethos

The psyche's framing for the broader data/schema plane (2026-08-10):

> we could just make a sort of like shortcut where it's just like
> schema rest [schema-rust], you know, it's ethos rest [ethos-rust].
> And datum [Datom] is basically just like a different syntax than nota

— psyche, dictated, 2026-08-10T18:49Z (Designer session c6b71b4c);
`psyche-raw/Vision/archive-threeStacks.md`, lines 6–49.

Agent context: the psyche ruled that the incorrect old stack is frozen
in place, new repositories carry simplified ethos-to-Rust emission, and
Datom is the new syntax replacing NOTA/Schema. The old stack's slowness
came from imposing daemon-era architecture on a pipeline that didn't need
it. This is the broader context within which Horizon data sits: all
authored data moves to Datom; the pipeline is authored Datom → Rust
projection → Nix consumption.

---

## Sources

### Codex history

- `~/.codex/history.jsonl` line 2193, ts 1778582678 — "I don't want any node or cluster-specific data in those repositories"
- `~/.codex/history.jsonl` line 2201, ts 1778585249 — "move node name gates into Horizon"
- `~/.codex/history.jsonl` line 2705, ts 1778999875 — criome/criome.net are horizon constants
- `~/.codex/history.jsonl` line 2709, ts 1779000726 — cluster data only selects providers as variant vectors
- `~/.codex/history.jsonl` line 2714, ts 1779002394 — criomos-horizon-config origin
- `~/.codex/history.jsonl` line 2727, ts 1779012989 — federation/meta-cluster vision, "horizon should mostly be just the reducer"
- `~/.codex/history.jsonl` line 2856, ts 1779144227 — "give me variants, not booleans"
- `~/.codex/history.jsonl` line 2859, ts 1779144353 — "bunch of dials to turn shit on and off"
- `~/.codex/history.jsonl` line 2861, ts 1779144452 — "variants first"

### Claude history

- `~/.claude/history.jsonl` line 3238, ts 1775387512987 — per-user horizon setting for keyboard
- `~/.claude/history.jsonl` line 5085, ts 1778158263406 — display density, not text size
- `~/.claude/history.jsonl` line 5306, ts 1778310860625 — implement preferredEditor in horizon-rs
- `~/.claude/history.jsonl` line 5910, ts 1778778699832 — goal: fully tested re-engineered horizon stack
- `~/.claude/history.jsonl` line 6289, ts 1779010184393 — gguf model catalog belongs in CriomOS

### Transcripts (Codex sessions)

- `~/.codex/sessions/2026/07/28/rollout-…-019fa893-…-.jsonl` — lines 1194, 1271, 1384, 1405 (horizon feature flags, intercom incident, Nix-controlled environment)
- `~/.codex/sessions/2026/08/01/rollout-…-019fbf4a-…-.jsonl` — line 3801 (no hardwired hostnames in lojix)
- `~/.codex/sessions/2026/08/22/rollout-…-01a02b4b-…-.jsonl` — lines 880, 905, 932 (home equivalence, extended-horizon, false confidence correction)
- `~/.codex/sessions/2026/08/23/rollout-…-01a02fe5-…-.jsonl` — lines 1173, 1231 (deployment variables)
- `~/.codex/sessions/2026/08/23/rollout-…-01a030a1-…-.jsonl` — lines 605, 839 (common ground, extended-horizon reacquisition)
- `~/.codex/sessions/2026/08/24/rollout-…-01a030e8-…-.jsonl` — lines 9, 540, 621 (criomos-core request, core supersedes lib, horizon service wtf)
- `~/.codex/sessions/2026/08/25/rollout-…-01a035d3-…-.jsonl` — lines 9, 279 (rust/data separation, datom instead of dotos)
- `~/.codex/sessions/2026/08/28/rollout-…-01a04881-…-.jsonl` — lines 218, 387 (slop, cause of agentic failure)
- `~/.codex/sessions/2026/08/28/rollout-…-01a048a6-…-.jsonl` — lines 9, 64, 87, 141, 274, 751, 803, 845 (AgentIntercomGraphical misnomer, gate removal, AgentIntercom follows Claude/Codex, x86 gate)

### Flow vision records

- `flows/01a02b4b/vision/homeEquivalence.md`
- `flows/01a030a1/vision/commonGround.md`
- `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`
- `flows/01a035d3/vision/rustCodeFromTheData.md`
- `flows/01a04881/vision/agentIntercomGraphical.md`
- `flows/01a048a6/vision/agentIntercomGraphical.md`

### Flow reports

- `flows/01a030a1/reports/extendedHorizonReacquisition.md`
- `flows/01a030e8/reports/criomosCoreProposal.md`
- `flows/01a0338f/reports/nodeConfigurationGates.md`

### Psyche-raw records

- `psyche-raw/Vision/setupIndependentInterfaces.md`
- `psyche-raw/Vision/lojixOwnership.md`
- `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md`
- `psyche-raw/Vision/traitsAsCapabilities.md`
- `psyche-raw/Vision/archive-threeStacks.md`
- `psyche-raw/Vision/everythingIsInTheDaemon.md`

### Pre-reset corpus

- `reports/PreResetCorpus-2026-06-07/reports/system-designer/70-cluster-data-feature-horizon-criomos-2026-06-04.md`
- `reports/PreResetCorpus-2026-06-07/reports/cloud-designer/23-horizon-lojix-rewrite-audit-2026-06-04/` (files 0–7)
- `protocols/active-repositories.md`

### Additional flow records

- `flows/01a04881/vision/cause.md` — "my failure isnt identifying the cause"
- `flows/01a04881/vision/repeatingLikeThis.md` — "repeating like this is also slop"
- `flows/01a04881/witnesses/zeusDeploymentAndDesktopGate.md`
- `flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md`
- `flows/01a030eb/witnesses/criomosHomeCommonality.md`
- `flows/01a0338f/witnesses/currentNodeGates.md`
- `flows/01a0338f/reports/nodeConfigurationGates.md`
- `flows/ac1e9ec8/vision/datomSyntax.md` — datom is for the text edge only
- `flows/db97561c/log.md`

### Distilled Vision

- `Vision/highLevelView.md`
- `Vision/nexus.md` (Nexus configuration model)
- `Vision/orchestrate.md`

### Repository source

- `horizon-rs/ARCHITECTURE.md` — typed end-to-end, WHAT never HOW, type-count axis
- `horizon-rs/docs/DESIGN.md` — wire format, schema rules, crate shape
- `criomos-horizon-config/ARCHITECTURE.md` — pan-horizon config boundary
- `goldragon/datom.dotos` — authored cluster proposal
- `d098fa2d/witnesses/declaredSources.md` — deployment pipeline shape
- `d098fa2d/witnesses/pipeline.md` — Lojix materialization steps
