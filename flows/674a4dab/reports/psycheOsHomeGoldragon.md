# Psyche acquisition: CriomOS / CriomOS-home / Goldragon / manifests

What the living psyche actually wanted for the operating-system, user-environment, and node-identity plane of the CriomOS stack.

---

## The mess and the recovery imperative

### 2026-08-08 — "right now everything is a fucking mess"

> So we were having problems. Well, there's a few things, and one of which is right now everything is a fucking mess. So don't trust anything. Don't assume anything. Be careful where you step. So, OK, so CryomOS [CriomOS], we have multiple hosts. Everybody's like on different versions because I've mostly been just updating my own laptop and neglecting everybody else because I'm afraid to like break other people's computers. ... So Zeus, another host where my partner works, is having problems. And we've been having a lot of problem with VS Codium or VS Code, whatever we want to call it, in respect with the cloud and the codex extensions. Very problematic. ... So, you know, I have great ambitions, but I have limited means and I'm a bit messy. So things just sort of get like gotten really messy with a lot of ambition stuck and that I get a little tiny bottleneck. And it's just like the ambition is trying to come through too fast and it's like coming out the other side broken or half broken.

STT corrections: "CryomOS" -> CriomOS; "Uranus" -> Ouranos (noted by the psyche themselves: "I should say Odanos, but I think the speech-to-text has a hard time hearing that").

-- psyche, dictated. Transcript: `rollout-2026-08-08T13-28-29-019fe121-b1ea-7350-922b-826d0ce83a37.jsonl`, L9.

Agent context: opening monologue of the steward session that began the recovery arc. The psyche describes hosts on different versions, CriomOS/CriomOS-home falling out of sync, ancient versions being redeployed inexplicably, and agents unable to fix things for months.

My reading: the psyche is frustrated not merely with individual bugs but with structural drift -- hosts diverging, the OS and Home falling out of sync, agent work not converging. The bottleneck description ("ambition trying to come through too fast") suggests the psyche sees the architectural complexity as the chokepoint, not a lack of effort.

### 2026-08-08 (same message) — hosts out of sync, ancient versions redeployed

> And like the user environment is using the wrong version of something that it doesn't match the version on KareemOS [CriomOS] or vice versa. And that cloud and codecs [Claude and Codex] are up to date. I've been having a lot of problems with like ancient versions being redeployed for I don't know what fucking reason.

STT corrections: "KareemOS" -> CriomOS; "cloud and codecs" -> Claude and Codex.

-- psyche, dictated. Same transcript, L9.

Agent context: continuation of the opening. This specifically identifies the OS/Home version mismatch as a witnessed recurring problem.

My reading: the synchronization failure between CriomOS and CriomOS-home is the most viscerally felt problem. The psyche cannot explain why it happens, which points to a structural cause.

---

## Lojix: system ownership, not home

### 2026-08-13 — "it should only be in OS"

> I had an agent tell me lojix was in OS and home, which creates conflicts. it should only be in OS, and the broken lojix is probably really bad since agents have been trying to fix it for months. if I say "what exactly is wrong with it" I must admit I wont really trust you to know. sorry, but months of bad results destroys trust

-- psyche, typed. Transcript: `rollout-2026-08-13T14-00-33-019ffafe-d8dd-7421-ad2e-58fc98ee5240.jsonl`, L409.

Agent context: the psyche had discovered Lojix was declared in both CriomOS and CriomOS-home configurations, causing conflicts. Agent confirmed and recorded the ruling "it should only be in OS".

My reading: Lojix belongs to the system layer. The dual presence is identified as a source of conflicts. The trust damage is notable -- "months of bad results destroys trust" -- suggesting this is part of the broader pattern of agents failing to maintain the stack correctly.

### 2026-08-13 — "I dont care about any past lojix database"

> I dont care about any past lojix database. how do we get a clean working lojix service running?

-- psyche, typed. Transcript: same file, L573.

Agent context: the psyche ruled that preserving the existing Lojix database is not a recovery requirement. A fresh working state is preferred over backward compatibility.

My reading: consistent with Spirit -- backward compatibility is never a design variable.

### 2026-08-14 — deploy Lojix first, then use it to deploy the upgrade

> the system has to be redeployed with only the newer Lojix daemon, nothing else. And then we can use Lojix to deploy the upgrade. That should have been done already.

-- psyche, typed or dictated. Recorded in `psyche-raw/Vision/setupIndependentInterfaces.md`. (Transcript source at `2026-08-14T09:06+02:00`; exact session file not located in this search round.)

Agent context: the installed daemon (0.11.0, schema v2) could not read the store (schema v4). The psyche ruled the deployment order: first redeploy CriomOS with only the current Lojix daemon, then use Lojix itself for further upgrades.

My reading: the psyche expects the deployment tool to be the authority for upgrades. The frustration ("That should have been done already") indicates this was obvious to the psyche but agents failed to see it.

---

## Home equivalence: embedded and independent Home must be identical

### 2026-08-23 — "there should be no difference between the embedded and independent home"

> there should be no difference between the embedded and independent home. the part which is shared ought to be directly from lojix-emitted horizon output, or from a shared nix machinery which uses the said horizon as input only. embedded home should be only the absolute minimum nix code necessary to embed a home logic which is otherwise completly [completely] identical. Do you understand what I mean?

-- psyche, typed. Transcript: `rollout-2026-08-22T23-06-14-01a02b4b-ab46-7921-8e47-928b294470be.jsonl`, L880.

Agent context: the agent had presented a visual showing how embedded Home (inside CriomOS NixOS evaluation) and independent Home diverge because embedded Home inherits NixOS context (locale, Stylix, osConfig). The psyche's ruling eliminates that divergence.

My reading: this is a foundational architectural ruling. The Home logic is one thing; the NixOS embedding is a thin wrapper. Shared inputs come from Horizon, not from the surrounding OS evaluation. This directly explains the OS/Home sync problems -- the current system violates this invariant.

### 2026-08-23 — "whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon"

> whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon (that could be a standalone repo for deriving some data in nix from the horizon data coming out of lojix)

-- psyche, typed. Transcript: same file, L905.

Agent context: the psyche located every Home value currently inherited from the OS in either Lojix-emitted Horizon or a potential `extended-horizon` derivation layer. The psyche framed `extended-horizon` tentatively ("that could be a standalone repo").

My reading: the source-of-truth boundary. Home may consume Horizon directly or through a deterministic derivation layer, but never from the surrounding OS evaluation. The extended-horizon concept is permissive (could be), not a mandate for a specific repository yet.

### 2026-08-23 — challenge: "you mean that repo already existed?"

> (quoting agent: "Yes. extended-horizon is not another authority; it is a deterministic derivation layer over Horizon.") you mean that repo already existed?

-- psyche, typed. Transcript: same file, L932.

Agent context: the psyche caught the agent writing as if `extended-horizon` were an existing, settled thing. The agent corrected: no such repository existed.

My reading: the psyche is vigilant about agents presenting proposals as facts. The extended-horizon concept exists in the psyche's vision, but no repository or implementation has been authorized.

---

## Common ground between OS and Home: criomos-core

### 2026-08-23 — "abstract the common ground between OS and home to a separate repo"

> to me, this looks like a need to abstract the common ground between OS and home to a separate repo, and using that repo as the source for anything that is shared between them. indirection is bad design

-- psyche, typed. Transcript: `rollout-2026-08-23T23-58-34-01a030a1-f055-7273-822a-0a4f94f6f8f8.jsonl`, L605.

Agent context: the agent had proposed that CriomOS-home export a construction record for CriomOS to consume. The psyche rejected this as indirection: the shared ground belongs in its own repository, consumed directly by both.

My reading: the psyche identifies the dependency direction as the core problem. OS reaching shared values through Home is indirect. Both should point to a common source. The statement "indirection is bad design" reads as a general principle, but its scope has not been explicitly graduated to Intent.

### 2026-08-23 — "no thats not it, I was discussing an extended-horizon or horizon-extended repo"

> no thats not it, I was discussing an extended-horizon or horizon-extended repo

-- psyche, typed. Transcript: same file, L839.

Agent context: when the agent tried to connect the common-ground ruling to Protos/Orca analogues, the psyche corrected: the earlier discussion was specifically about an extended-horizon repository, from flow 01a02b4b.

My reading: the psyche has a specific thread in mind -- the deterministic Horizon-derivation layer -- and distinguishes it from the broader pattern of shared substrates.

### 2026-08-24 — "find all the commonality ... in a new criomos-core repo"

> Then find all the commonality between the OS and home repos, then make a proposal on moving the source of it all in a new criomos-core repo which would export them as exported namespaces for criomos and criomos-home to use

-- psyche, typed. Transcript: `rollout-2026-08-24T01-15-43-01a030e8-91d9-7361-9682-2fdd078f0ad6.jsonl`, L9.

Agent context: continuation of the common-ground ruling. The psyche named the repository: criomos-core.

My reading: the psyche has converged on a specific name and structure. The repository exports namespaces that both consumers use directly. This is a concrete realization directive.

### 2026-08-25 — "core is more accurate than lib, superseding is the right perspective"

> I think core is more accurate than lib, yes, so superseding is the right perspective.

-- psyche, typed. Transcript: same session as 01a030e8, L540.

Agent context: the agent had proposed that criomos-core supersede CriomOS-lib rather than coexist with it. The psyche approved.

My reading: criomos-core replaces CriomOS-lib entirely. No parallel compatibility path -- consistent with Spirit.

---

## Node identity, goldragon, and the AgentIntercomGraphical debacle

### 2026-08-25 — "I would like medium graphical nodes to have codex and claude desktop apps"

> I would like medium graphical nodes to have codex and claude desktop apps installed. If we use a third party flake for them, let's make sure we have a procedure to audit it, making sure the right sources are installed the right way on every update

-- psyche, typed. Transcript: `rollout-2026-08-24T13-37-15-01a0338f-760f-7622-9f2b-bbc83115c95b.jsonl`, L369.

Agent context: after investigating what was installed on Ouranos and Zeus, the psyche ruled that desktop apps belong on medium graphical nodes with a per-update audit procedure.

### 2026-08-25 — "just medium size" and reconstruct the graphical role

> 1. no, just medium size, and there used to be a node role that meant it had graphical aspects enabled. Find out how things are now. Lets see a visual on node configurations and the gates that use them in criomos.

-- psyche, typed. Transcript: same file, L674.

Agent context: the psyche corrected the agent's interpretation and asked for a reconstruction of how the graphical node role works. The existing `size.medium` gate is cumulative (Medium, Large, Max all satisfy it).

My reading: the psyche wants desktop apps gated by size (cumulative medium) plus graphical capability. The graphical capability was historically "Edge" -- the psyche knows there used to be a graphical role and wants it reconstructed.

### 2026-08-28 — "AgentIntercomGraphical is a total misnomer"

> AgentIntercomGraphical is a total misnomer and is now involved in a bunch of things it has nothing to do with (AgentIntercom is one thing, Graphical is another; and a duplication since we already have the Edge node concept)

-- psyche, typed. Transcript: `rollout-2026-08-28T15-54-20-01a048a6-68f8-74f1-b56e-d6c9fe4aef4b.jsonl`, L64.

Agent context: flow 01a04881 had found that Bird on Zeus lacked desktop apps because Zeus has no `AgentIntercomGraphical` capability. This flow continued: the psyche identified the flag as fundamentally wrong.

My reading: three distinct concepts are conflated in one flag: (1) AgentIntercom (the agent communication layer), (2) Graphical (generic desktop/input prerequisites), and (3) Edge (the node concept that already means "graphical desktop node"). The psyche sees this as slop that must be decomposed.

### 2026-08-28 — "seems it doesnt even anything to do with agent-intercom even"

> seems it doesnt even anything to do with agent-intercom even

STT note: likely "seems it doesn't even have anything to do with agent-intercom even".

-- psyche, typed. Transcript: same file, L87.

Agent context: the agent confirmed the stronger hypothesis -- the gate's actual responsibilities are graphical prerequisites and desktop apps, not AgentIntercom behavior.

My reading: the psyche's working hypothesis was confirmed by the code: the flag is an Edge-node concern wearing an unrelated name.

### 2026-08-28 — "we were gating agent-intercom before because it would modify codex and claude"

> we were gating agent-intercom before because it would modify codex and claude, but now I only want different executables (different names) to be wrapped with the agent-intercom wrapped codex and claude, so we dont need a gate at all. so differentiate what is gated by this now totally inappropriate flag, which must be removed, so we can gate what needs to be gated with the right variables

-- psyche, typed. Transcript: same file, L141.

Agent context: the psyche explained why the gate was originally created (AgentIntercom modified the canonical Codex/Claude executables), why it no longer applies (now only alternate-name wrappers are wanted), and what must happen (remove the flag, separate what it gates, gate by the right variables).

My reading: the original gate conflated the presence of AgentIntercom wrappers with the presence of a graphical desktop. Now that wrappers use separate names and do not replace canonical executables, AgentIntercom needs no gate. Desktop apps follow Edge plus cumulative Medium.

### 2026-08-28 — "We don't need to gate agent intercom, it should be on any node that has Claude/codex"

> We don't need to gate agent intercom, it should be on any node that has Claude/codex

-- psyche, typed. Transcript: same file, L803.

Agent context: the psyche restated the AgentIntercom boundary: it follows the presence of canonical Claude/Codex packages, not a node service, not Edge, not architecture, not size.

My reading: AgentIntercom is orthogonal to both the graphical/Edge question and the size question. It is simply present wherever Claude and Codex are present.

### 2026-08-28 — "Why is x86 a gate for the apps?" / "Remove the x86 gate"

> Why is x86 a gate for the apps?

> Remove the x86 gate, and get all the work merged or ready do merge on main everywhere

-- psyche, typed. Transcript: same file, L803 and L845.

Agent context: the Home module had a shared x86 assertion that gated desktop apps. The psyche identified this as unjustified.

My reading: architecture should not be a conceptual gate for desktop apps. Each package's actual build support decides whether it exists. The x86 gate was carried forward from an earlier assumption without re-verification.

### 2026-08-28 — implement, merge, deploy

> Great. Implement and merge on main then deploy ouranos and zeus

-- psyche, typed. Transcript: same file, L274.

Agent context: the psyche approved the agent's restructuring proposal and authorized implementation across all repositories, main integration, and deployment to both Ouranos and Zeus.

---

## Setup-independent interfaces and no setup-specific scripts

### 2026-08-14 — "I don't want setup-specific scripts in general repos"

> I don't want setup-specific scripts in general repos. Everything must be setup-independent with simple clear interfaces that agents can easily adapt to their needs.

-- psyche, typed. Recorded in `psyche-raw/Vision/setupIndependentInterfaces.md`.

Agent context: `ouranos-activate.sh` in `LojixOsOnlyActivation` bundled setup-specific deployment logic. The psyche rules this pattern out.

My reading: deployment interfaces must work for any setup, not just Ouranos. This is part of the broader principle that the system should not require host-specific knowledge.

### 2026-08-14 — "the interface is lojix and meta-lojix CLI only"

> Seems like letting agents "fix" it ended up abandoning my vision. The interface is lojix and meta-lojix CLI only.

-- psyche, typed. Recorded in `psyche-raw/Vision/setupIndependentInterfaces.md`.

Agent context: `ouranos-activate.sh` was an agent-created workaround bypassing the designed CLI interface.

My reading: agents created workarounds that departed from the psyche's vision. The deployment interface is the typed CLI, not scripts. This carries over to the broader principle: CLIs take typed input objects, no flags.

### 2026-08-14 — "CLIs cannot accept any argument other than the typed input object"

> An agent broke the invariant. Get rid of the flag and expose the option through nota/dotos. Remove any and all flags from lojix, replace them all. CLIs cannot accept any other type of argument than the typed input object. I feel like I keep repeating myself.

-- psyche, typed. Recorded in `psyche-raw/Vision/setupIndependentInterfaces.md`.

Agent context: `--override-input horizon <path>` was being passed as a flag. The psyche ruled all input goes through the typed object.

My reading: this is an invariant that agents keep violating. The frustration ("I feel like I keep repeating myself") is diagnostic -- the context or skills were not preventing this.

---

## Repository ownership principles

### 2026-08-23 — "an orca repo is smarter than cramming more stuff in the home repo"

> I think an orca repo is smarter than cramming more stuff in the home repo

-- psyche, typed. Recorded in `flows/01a02f23/vision/orca.md`. Transcript: flow 01a02f23, `2026-08-23T18:15:03+02:00`.

Agent context: the ownership boundary for Nix packaging of StablyAI Orca was being decided.

My reading: the psyche prefers concept-scoped repositories over cramming things into existing large repositories. This aligns with "every concept should really have its repo" (psyche-raw/Vision/everyConceptShouldHaveItsRepo.md, 2026-08-09).

### 2026-08-10 — "we should use main for everything"

> we should use main for everything

-- psyche, typed. Recorded in `psyche-raw/Vision/mainForEverything.md`.

Agent context: said during Lojix recovery after finding a dependency pinned to a non-main branch.

My reading: no long-lived feature branches; everything goes through main. Consistent with the Spirit principle on backward compatibility.

---

## Flake and user environment structure

### 2026-08-19 — "keep the flake very minimal; an entry point"

> I would rather keep the flake very minimal; an entry point

> how to structure the code so customizing packages is done in a central place and is easy for agents to perform.

-- psyche, typed. Recorded in `psyche-raw/Vision/minimalFlake.md`. Transcript: `rollout-2026-08-19T12-36-31-01a01998-1214-7172-b75d-6f2d79f4bcef.jsonl`, L9.

Agent context: while requesting a faster-moving yt-dlp source in the Nix user environment, the psyche ruled the intended project shape.

My reading: the flake is a thin entry point. Package customization should be centralized and agent-friendly, not scattered.

### 2026-08-16 — sshcontrol keygrip comes from cluster data

> That should be set using cluster data in criomos-home.

-- psyche, typed. Recorded in `psyche-raw/Vision/setupIndependentInterfaces.md`.

Agent context: the GPG keygrip in `~/.gnupg/sshcontrol` was missing from the new Home Manager generation. The psyche ruled it should come from the Horizon/cluster data.

My reading: another instance of the principle that Home values should derive from Horizon data, not be hardcoded or manually managed.

### 2026-08-17 — nixpkgs update on the first commit after the new moon

> Update on the first commit exactly after the new moon every lunation.

-- psyche, dictated. Recorded in `psyche-raw/Vision/setupIndependentInterfaces.md`.

Agent context: the nixpkgs pin update cadence follows the lunar cycle.

My reading: a distinctive cadence that is specific to the psyche's preferences. It ensures regular updates without being arbitrary.

---

## The remote-control server: one server for everything

### 2026-08-27 — "one server for everything ... both for Claude and codex"

> Keep working on the one server for everything solutions, both for Claude and codex

-- psyche, typed. Recorded in `flows/01a047d2/vision/remoteControl.md`.

### 2026-08-27 — "the code server should be rooted in primary"

> Yes, the code server should be rooted in primary.

-- psyche, typed. Recorded in `flows/01a047d2/vision/remoteControl.md`.

### 2026-08-27 — "we just need the server running for codex and claude"

> I dont want to start a nexus for this; we just need the server running for codex and claude, and the desktop apps using it locally.

-- psyche, typed. Recorded in `flows/01a047d2/vision/remoteControl.md`.

Agent context: the agent proposed a Nexus/control-plane interpretation. The psyche rejected it. The server is a simpler thing: it runs for Codex and Claude, desktop apps use it.

My reading: the psyche wants a practical solution for desktop/remote access to agent sessions, not an over-architected Nexus. The server lives in the primary workspace.

---

## The slop and the failure to identify causes

### 2026-08-28 — "this agentintercomgraphical is slop"

> this agentintercomgraphical is slop. what does it actually gate?

-- psyche, typed. Transcript: `rollout-2026-08-28T15-13-58-01a04881-741f-7591-ba44-6ed77dca4b7b.jsonl`, L218.

### 2026-08-28 — "repeating like this is also slop"

> repeating like this is also slop. isolate the cause for this sloppey [sloppy] behavior

-- psyche, typed. Transcript: same file, L248.

Agent context: the agent had logged the psyche's ruling with minimal context, repeating the same sloppy behavior the psyche was complaining about.

### 2026-08-28 — "youre putting out fires while ignoring the pyromaniac with a flamethrower"

> youre so short sighted. we are addressing skills here. youre putting out fires while ignoring the pyromaniac with a flamethrower; youll be putting out fires and wasting my time forever. you still havent found the cause of anything. which means theres a deeper failure; you dont understand how to identify the cause of agentic failure

-- psyche, typed. Transcript: same file, L387.

Agent context: the flow was proposing isolated repairs to individual slop records rather than identifying the systemic cause in the governing skills.

My reading: the psyche sees the AgentIntercomGraphical problem as symptomatic of a deeper failure pattern: agents do not identify root causes. The "pyromaniac" is the skill or context deficiency that produces recurring slop, not any individual output. This is a meta-concern about agentic behavior, not just about the CriomOS stack.

---

## CriomOS should move toward operating without X11

> CriomOS should move toward operating without X11.

-- recorded in `Vision/x11.md`. (Transcript source not located in this search round; the entry predates or stands outside the August flow record.)

My reading: a directional ruling. CriomOS aims for a Wayland-only future. The flow 01a03e3f implemented a ChatGPT native-Wayland override, consistent with this direction.

---

## Tensions and unresolved points

1. **criomos-core vs. extended-horizon**: the psyche named two separate concepts. criomos-core is the general shared-ground repository replacing CriomOS-lib (2026-08-24). extended-horizon is the Horizon-derivation layer where Home values currently originating from the OS would live (2026-08-23). Whether these are the same repository, overlapping, or separate is unresolved. The criomos-core proposal included Horizon service interpretation and data; the extended-horizon concept was specifically about deriving Nix data from Lojix-emitted Horizon. They may converge, but the psyche has not ruled them identical.

2. **Deployment preflight**: flow 01a048a6 reports that no authoritative `manifests/*.dotos` selection supplies the required explicit store/SSH transport, builder, selector, and input mode for Ouranos and Zeus. The psyche approved "implement and merge on main then deploy ouranos and zeus" (L274, 01a048a6) but deployment is blocked by missing Lojix request fields.

3. **Zeus node capabilities**: Zeus is defined in `goldragon/datom.dotos` as `Edge` / `Max` / `Max` with an empty services list `[]`. The psyche approved removing AgentIntercomGraphical and deriving desktop apps from Edge plus cumulative Medium. But Zeus has no services at all in the current datom. Whether this is the intended shape (Zeus as a minimal Edge node without services) or an omission is unresolved. Ouranos has `[(AgentIntercomLocal) (AgentIntercomGraphical) ...]` which is being restructured.

4. **The "indirection is bad design" scope**: the psyche stated this while discussing OS/Home common ground. Whether it is a general principle (Intent) or scoped to this specific dependency direction has not been graduated.

5. **Who maintains the manifests**: `manifests/*.dotos` was identified in AGENTS.md as the source of identity and deployment selection, but no `.dotos` files exist in `primary/manifests/`. The goldragon repository contains the cluster data as `datom.dotos`. The synchronizer in `goldragon/synchronizer.dotos` presumably carries deployment configuration. The relationship between goldragon's datom, the Lojix request shape, and any per-host deployment manifest is not clear from the psyche record.

## Sources

### Transcripts (Codex sessions, all in `/home/li/.codex/sessions/2026/08/`)
- `08/rollout-2026-08-08T13-28-29-019fe121-b1ea-7350-922b-826d0ce83a37.jsonl` (L9) -- "everything is a mess" opening
- `13/rollout-2026-08-13T14-00-33-019ffafe-d8dd-7421-ad2e-58fc98ee5240.jsonl` (L409, L573) -- Lojix OS ownership, database disposal
- `19/rollout-2026-08-19T12-36-31-01a01998-1214-7172-b75d-6f2d79f4bcef.jsonl` (L9) -- flake minimal
- `22/rollout-2026-08-22T23-06-14-01a02b4b-ab46-7921-8e47-928b294470be.jsonl` (L880, L905, L932) -- Home equivalence, extended-horizon
- `23/rollout-2026-08-23T23-58-34-01a030a1-f055-7273-822a-0a4f94f6f8f8.jsonl` (L605, L839) -- common ground, extended-horizon correction
- `24/rollout-2026-08-24T01-15-43-01a030e8-91d9-7361-9682-2fdd078f0ad6.jsonl` (L9, L540) -- criomos-core naming, lib superseding
- `24/rollout-2026-08-24T13-37-15-01a0338f-760f-7622-9f2b-bbc83115c95b.jsonl` (L369, L674) -- medium graphical nodes, desktop apps
- `28/rollout-2026-08-28T15-13-58-01a04881-741f-7591-ba44-6ed77dca4b7b.jsonl` (L218, L248, L387) -- slop, cause identification
- `28/rollout-2026-08-28T15-54-20-01a048a6-68f8-74f1-b56e-d6c9fe4aef4b.jsonl` (L64, L87, L141, L274, L803, L845) -- AgentIntercomGraphical decomposition

### Flow vision and reports
- `flows/01a02b4b/vision/homeEquivalence.md`
- `flows/01a030a1/vision/commonGround.md`
- `flows/01a030a1/reports/commonGroundReacquisition.md`
- `flows/01a030a1/reports/extendedHorizonReacquisition.md`
- `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`
- `flows/01a030e8/reports/criomosCoreProposal.md`
- `flows/01a04881/vision/cause.md`
- `flows/01a04881/vision/agentIntercomGraphical.md`
- `flows/01a04881/vision/repeatingLikeThis.md`
- `flows/01a048a6/vision/agentIntercomGraphical.md`
- `flows/01a048a6/log.md`
- `flows/01a02fd5/vision/interfaces.md`
- `flows/01a02f23/vision/orca.md`
- `flows/01a047d2/vision/remoteControl.md`
- `flows/01a04881/witnesses/zeusDeploymentAndDesktopGate.md`

### Psyche-raw / Vision / Intent
- `psyche-raw/Vision/lojixOwnership.md`
- `psyche-raw/Vision/setupIndependentInterfaces.md`
- `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md`
- `psyche-raw/Vision/minimalFlake.md`
- `psyche-raw/Vision/mainForEverything.md`
- `psyche-raw/Vision/host-environment-recovery.md`
- `Vision/x11.md`

### Node identity data
- `goldragon/datom.dotos` -- cluster proposal with node definitions
