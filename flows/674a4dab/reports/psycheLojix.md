# Psyche acquisition: the deployment plane

What the living psyche wanted for Lojix, its Nexus, deployments, deployment
selection, producer/consumer immutable sources, Home Manager generations,
the hosts Ouranos/Zeus/Bird, transports/builders/selectors, host key material,
and how the OS and Home get deployed.

Organized by the psyche's own framing, oldest first within each subject.
Speech-to-text corrections noted in square brackets beside the quote.

---

## Lojix ownership and system placement

### "it should only be in OS"

> I had an agent tell me lojix was in OS and home, which creates conflicts.
> it should only be in OS, and the broken lojix is probably really bad since
> agents have been trying to fix it for months. if I say "what exactly is
> wrong with it" I must admit I wont really trust you to know. sorry, but
> months of bad results destroys trust

-- psyche, typed, 2026-08-13T15:40+02:00. Session `019ffafe-d8dd-7421-ad2e-58fc98ee5240`, line 409.

Agent context: The agent had been asked about the state of Lojix and CriomOS
deployment. The psyche learned from a prior agent that Lojix was present in
both OS and Home configurations and ruled it should be OS-only.

*Inference: The ruling is structural -- Lojix belongs in the operating system,
not the user environment. This is the psyche locating deployment infrastructure
in the system layer, which aligns with the later ruling that deployment
configuration goes in CriomOS, not CriomOS-home. The remark about months of
bad results and destroyed trust establishes the emotional context: the psyche
was frustrated with prolonged agent failures around Lojix and wanted clean
ownership.*

### "I dont care about any past lojix database"

> I dont care about any past lojix database. how do we get a clean working
> lojix service running?

-- psyche, typed, 2026-08-13T23:32+02:00. Session `019ffafe-d8dd-7421-ad2e-58fc98ee5240`, line 573.

Agent context: The agent had been discussing schema version mismatches
between the installed daemon (0.11.0, schema v2) and the store (schema v4).

*Inference: The psyche values a working service over data preservation. The
past database is disposable; getting current and functional is what matters.
This is consistent with the spirit's "backward compatibility is never a design
variable" -- carry the current forward, do not preserve legacy state.*

### "the system has to be redeployed with only the newer Lojix daemon"

> the system has to be redeployed with only the newer Lojix daemon, nothing
> else. And then we can use Lojix to deploy the upgrade. That should have been
> done already.

-- psyche, recorded in `psyche-raw/Vision/lojixOwnership.md` at
2026-08-14T09:06+02:00. The transcript source for this quote was not located
in the Aug 14 session files; the psyche-raw record is the available provenance.

Agent context: The installed daemon (0.11.0) could not read the existing store
(schema v4), blocking Lojix bootstrap from generating fresh inputs.

*Inference: The psyche establishes a deploy-first order: get the correct Lojix
daemon running on the system before using Lojix to perform upgrades. "That
should have been done already" expresses frustration that agents had not taken
this obvious step. The psyche sees Lojix as the tool for deployment -- you
cannot deploy with a broken tool, so fix the tool first.*

---

## Setup-independent interfaces and CLI invariant

### "I don't want setup-specific scripts in general repos"

> I don't want setup-specific scripts in general repos. Everything must be
> setup-independent with simple clear interfaces that agents can easily adapt
> to their needs.

-- psyche, recorded in `psyche-raw/Vision/setupIndependentInterfaces.md` at
2026-08-14. The record identifies the context as an `ouranos-activate.sh`
script in LojixOsOnlyActivation that bundled setup-specific deployment logic.

*Inference: Deployment interfaces must be generic. Agents should not rely on
host-specific wrapper scripts. The interface itself must be clean enough that
agents adapt to it, not the other way around.*

### "The interface is lojix and meta-lojix CLI only"

> Seems like letting agents "fix" it ended up abandoning my vision. The
> interface is lojix and meta-lojix CLI only.

-- psyche, recorded in `psyche-raw/Vision/setupIndependentInterfaces.md` at
2026-08-14.

Agent context: An agent had created `ouranos-activate.sh` as a workaround that
bypassed the designed CLI interface.

*Inference: The psyche explicitly names lojix and meta-lojix as the only
deployment interfaces. Agent-created wrapper scripts are a violation of the
design, not a fix. This is a structural ruling: all deployment goes through the
typed CLI contract.*

### "CLIs cannot accept any other type of argument than the typed input object"

> An agent broke the invariant. Get rid of the flag and expose the option
> through nota/dotos. Remove any and all flags from lojix, replace them all.
> CLIs cannot accept any other type of argument than the typed input object. I
> feel like I keep repeating myself.

-- psyche, recorded in `psyche-raw/Vision/setupIndependentInterfaces.md` at
2026-08-14.

Agent context: The agent had been passing `--override-input horizon <path>` as
a CLI flag instead of through the typed Dotos input object.

*Inference: Every CLI in the system accepts exactly one typed input object. No
flags, no subcommands, no extra arguments. "I feel like I keep repeating
myself" signals this is a recurring frustration -- agents keep introducing
flags and the psyche keeps having to correct them. This is an invariant, not
a preference.*

---

## Universal cluster fixes, nothing hardwired

### "this is a criomos-home fix, universal"

> nothing to do with bird, this is a criomos-home fix, universal. nothing in
> this should hardwire bird or zeus anywhere

-- psyche, typed, 2026-08-09T13:00+02:00. Session
`019fe641-5399-7fc3-8559-bda58cfbc632`, line 760.

Agent context: The agent had framed a host-environment recovery fix as
Bird-specific.

*Inference: Fixes must be universal, not host- or user-specific. The
declarative source is the single point of truth; hardwiring a particular node
name in a fix is structurally wrong. This aligns with the later ruling against
hardwired deployment variables.*

### "sshcontrol keygrip comes from cluster data"

> That should be set using cluster data in criomos-home.

-- psyche, typed, 2026-08-16. Recorded in
`psyche-raw/Vision/setupIndependentInterfaces.md`.

Agent context: The GPG keygrip in `~/.gnupg/sshcontrol` was missing from
the new Home Manager generation.

*Inference: Identity material derives from cluster/Horizon data, not from
manual management or hardcoded values.*

---

## Deployment authority: no hot fixes, no unnecessary confirmation

### "dont do hot fixes"

> dont do hot fixes

-- psyche, typed, 2026-08-19T20:42+02:00. Session
`01a01a93-a27d-7e73-944a-4501e67ce65d`, line 1878.

### "use the nix user env only, or OS redeploy"

> use the nix user env only, or OS redeploy

-- psyche, typed, 2026-08-19T20:43+02:00. Session
`01a01a93-a27d-7e73-944a-4501e67ce65d`, line 1894.

Agent context: Normal Codex and Claude had resolved to broken Agent Intercom
wrappers after a deployment. The psyche ruled the authorized recovery surfaces.

*Inference: The only legitimate mutation paths are the Nix user environment
activation (Home Manager) or a full OS redeploy (Lojix CompleteHost). Direct
runtime patching is forbidden. Changes reach production through the
declarative source, period.*

### "If I say deploy just deploy it"

> well lets talk later where it should be recorded but dont ask again. If I
> say deploy just deploy it

-- psyche, typed, 2026-08-19T21:03+02:00. Session
`01a01a93-a27d-7e73-944a-4501e67ce65d`, line 2213.

Agent context: The agent had held a CompleteHost activation for reconfirmation
of its root transport.

*Inference: When the psyche says deploy, agents should not re-ask for
confirmation. The deployment authority is the psyche's word. Agents should not
add unnecessary safety gates on top of a direct order. The psyche defers the
discussion of where to permanently record this default.*

---

## Zeus update: transport, boot, and breaking changes

### "explain what it looks like first"

> I want to update host zeus in my cluster. see if you can explain what that
> looks like first.

-- psyche, typed, 2026-08-22. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 9.

*Inference: The psyche wants comprehension before action. Explain the update
path, then execute.*

### "prefer the direct ethernet route"

> zeus should resolve now but prefer 192.168.18.95 for now, which is a direct
> ethernet route, will be much transfer [STT: "faster"] to transfer the nix
> paths

-- psyche, typed, 2026-08-22. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 234.

### "after the nix paths are moved zeus.goldragon.criome is fine"

> after the nix paths are moved zeus.goldragon.criome is fine for
> activation/etc

-- psyche, typed, 2026-08-22. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 254.

*Inference: The psyche establishes a split transport: use the high-bandwidth
direct Ethernet route for the heavy Nix store closure transfer, and the
regular (Yggdrasil/DNS) route for activation and light traffic. Transport is
chosen by the operation's needs, not by a single hardwired value.*

### "what timeout? I never approved any timeout"

> what timeout? I never approved any timeout

-- psyche, typed, 2026-08-23T12:18+02:00. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 1270.

> get rid of that timeout and resume your goal

-- psyche, typed, 2026-08-23. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 1287.

Agent context: An agent had introduced a wall-clock timeout on Lojix
deployment. The psyche discovered it and ordered its removal.

*Inference: Agents must not introduce unapproved constraints on Lojix
operations. A timeout is a design decision that requires psyche approval.
The psyche's pattern is clear: agents keep adding unauthorized safety
mechanisms (flags, timeouts, confirmation gates) and the psyche keeps removing
them.*

### "breaking upgrade documentation must go in the repository"

> whenever a breaking upgrade like that takes place, the documentation on how
> to deploy the break must go in the repository as well, in a canonical place,
> and it must be corrected if it turns out to fail or partially fail in
> practice. we need a skill proposal for this.

-- psyche, typed, 2026-08-23. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 2648.

> your skill is too complicated.

-- psyche, typed, 2026-08-23. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 2790.

> great, approved. land the skill

-- psyche, typed, 2026-08-23. Session
`01a02b46-5e97-7632-8db5-780391553085`, line 2819.

Agent context: After a complex-init failure during Zeus activation, the psyche
required breaking-upgrade documentation. The first skill proposal was rejected
as too complicated. The final approved skill is three rules:
document how to deploy in `UPGRADES.md`, land it with the breaking change,
correct it if deployment fails.

*Inference: The psyche wants the minimal effective documentation practice.
Complexity in process (like in code) is a defect. The skill went from too
complex to three sentences, which is the psyche's characteristic move:
eliminate machinery until only the essential contract remains.*

---

## SSH restoration and the deployment 49 incident

### "something broke my ssh access to all my hosts"

> something broke my ssh access to all my hosts, including localhost. this is
> a very big problem and must be fixed. something similar happenend [sic] a
> few days ago, you can maybe start with this lead. But it might be
> completly [sic] different.

-- psyche, typed, 2026-08-23. Session
`01a02fe5-ee5a-7a31-92bc-f500f2dc7712`, line 9.

### "why did an agent deploy the wrong home environment?"

> why did an agent deploy the wrong home environment?

-- psyche, typed, 2026-08-24. Session
`01a02fe5-ee5a-7a31-92bc-f500f2dc7712`, line 616.

### "We need better skill training"

> why did it deploy zeus on ouranos? We need better skill training

-- psyche, typed, 2026-08-24. Session
`01a02fe5-ee5a-7a31-92bc-f500f2dc7712`, line 926.

Agent context: Investigation revealed that Lojix deployment 49 had requested
the logical user environment for Zeus while routing activation through
Ouranos. The agent constructed a mismatched pair using shared variables that
encoded `DeploymentNode: zeus` alongside Ouranos transport values.

*Inference: The psyche identifies the root cause as training, not
infrastructure. The deployment variables were confusing agents; the fix is
better skill training, not more hardwiring.*

### "rely on good training instead of trying to hardwire"

> it doesnt matter why. those variables are confusing. we should rely on good
> training instead of trying to hardwire which node all situations should use,
> which is obviously wrong

-- psyche, typed, 2026-08-24. Session
`01a02fe5-ee5a-7a31-92bc-f500f2dc7712`, line 1173.

### "remove those hard wired deployment variables"

> remove those hard wired deployment variables and propose skill training that
> explains how the cluster works, what the nodes are, how to verify which node
> one is working on or building or deploying on/for, etc etc

-- psyche, typed, 2026-08-24. Session
`01a02fe5-ee5a-7a31-92bc-f500f2dc7712`, line 1231.

### "way too complex. start with ultra minimal"

> way too complex. start with ultra minimal

-- psyche, typed, 2026-08-25. Session
`01a02fe5-ee5a-7a31-92bc-f500f2dc7712`, line 1489.

*Inference: The corrective cycle mirrors the breaking-upgrades pattern:
(1) remove the wrong mechanism (hardwired variables), (2) propose the right
mechanism (training), (3) reject the first proposal as too complex, (4) approve
the ultra-minimal version. The final approved training is three sentences:
the logical node selects what is built; the activation destination selects
which machine changes; proceed only when they are verified as the same node.*

---

## Zeus update resume and embedded Home

### "use its ethernet LAN ip address for nix paths"

> Then resume the zeus update. use its ethernet LAN ip address 192.168.18.95
> if you need to move nix paths to it (yggdrassil [sic: Yggdrasil] is over
> wifi and will be very slow and heavy, but it's fine for activation and other
> non-heavy transfers usage)

-- psyche, typed, 2026-08-24. Session
`01a030b7-83db-72c1-a965-d4256df34349`, line 9.

### "it's missing the latest claude/codex update"

> its missing the latest claude/codex update. get it sorted out, see why it
> didnt make it, deploy it properly, and report back after it all explaining
> why it didnt get those updates

-- psyche, typed, 2026-08-24. Session
`01a030b7-83db-72c1-a965-d4256df34349`, line 282.

Agent context: Zeus had successfully reached generation 64 on OS, but its
embedded Home had a stale lock pinning an older CriomOS-home revision with
Codex 0.148.0 instead of 0.149.1.

*Inference: The psyche expects the full stack to be current after an update.
A successful OS activation that embeds a stale Home is not a successful
update. The psyche wants the root cause understood ("see why it didnt make
it") alongside the fix.*

---

## Embedded and independent Home equivalence

### "there should be no difference between the embedded and independent home"

> there should be no difference between the embedded and independent home. the
> part which is shared ought to be directly from lojix-emitted horizon output,
> or from a shared nix machinery which uses the said horizon as input only.
> embedded home should be only the absolute minimum nix code necessary to embed
> a home logic which is otherwise completly [sic] identical. Do you understand
> what I mean?

-- psyche, typed, 2026-08-23T15:44+02:00. Recorded in
`flows/01a02b4b/vision/homeEquivalence.md`.

### "whatever in home is currently originating in the OS must originate from the horizon"

> whatever in home is currently originating in the OS must originate from the
> horizon or the extended-horizon (that could be a standalone repo for deriving
> some data in nix from the horizon data coming out of lojix)

-- psyche, typed, 2026-08-23T17:14+02:00. Recorded in
`flows/01a02b4b/vision/homeEquivalence.md`.

*Inference: The psyche establishes the Horizon (Lojix-emitted typed data) as
the single source of truth for both OS-embedded and independent Home
evaluation. The OS is not the source of Home values; the Horizon is. An
"extended-horizon" repository could derive additional Nix data from the raw
Horizon, but the OS evaluation itself does not own Home configuration. The
embedded Home wrapper is a thin embedding shim, not a separate configuration
surface.*

---

## Common ground between OS and Home: criomos-core

### "abstract the common ground to a separate repo"

> to me, this looks like a need to abstract the common ground between OS and
> home to a separate repo, and using that repo as the source for anything that
> is shared between them. indirection is bad design

-- psyche, typed, 2026-08-24T00:58+02:00. Recorded in
`flows/01a030a1/vision/commonGround.md`.

### "find all the commonality and propose moving it to criomos-core"

> Then find all the commonality between the OS and home repos, then make a
> proposal on moving the source of it all in a new criomos-core repo which
> would export them as exported namespaces for criomos and criomos-home to use

-- psyche, typed, 2026-08-24T01:17+02:00. Recorded in
`flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`.

### "core is more accurate than lib"

> I think core is more accurate than lib, yes, so superseding is the right
> perspective.

-- psyche, typed, 2026-08-25T14:03+02:00. Recorded in
`flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`.

Agent context: The proposal asked whether criomos-core should coexist with
CriomOS-lib or supersede it.

*Inference: The psyche locates shared OS/Home ground in a neutral third
repository (criomos-core) rather than having one consumer indirectly expose
code to the other. "Indirection is bad design" -- the shared ground should be
directly referenced by both consumers, not passed through. CriomOS-lib is
superseded, not extended.*

---

## AgentIntercomGraphical: slop and the correct gates

### "this agentintercomgraphical is slop"

> this agentintercomgraphical is slop. what does it actually gate?

-- psyche, typed, 2026-08-28. Session
`01a04881-741f-7591-ba44-6ed77dca4b7b`, line 218.

### "AgentIntercomGraphical is a total misnomer"

> AgentIntercomGraphical is a total misnomer and is now involved in a bunch of
> things it has nothing to do with (AgentIntercom is one thing, Graphical is
> another; and a duplication since we already have the Edge node concept)

-- psyche, typed, 2026-08-28. Session
`01a048a6-68f8-74f1-b56e-d6c9fe4aef4b`, line 64.

### "we dont need a gate at all"

> we were gating agent-intercom before because it would modify codex and
> claude, but now I only want different executables (different names) to be
> wrapped with the agent-intercom wrapped codex and claude, so we dont need a
> gate at all. so differentiate what is gated by this now totally inappropriate
> flag, which must be removed, so we can gate what needs to be gated with the
> right variables

-- psyche, typed, 2026-08-28. Session
`01a048a6-68f8-74f1-b56e-d6c9fe4aef4b`, line 141.

### "We don't need to gate agent intercom"

> We don't need to gate agent intercom, it should be on any node that has
> Claude/codex

-- psyche, typed, 2026-08-28. Session
`01a048a6-68f8-74f1-b56e-d6c9fe4aef4b`, line 803.

### "Why is x86 a gate for the apps?"

> Why is x86 a gate for the apps?

-- psyche, typed, 2026-08-28. Session
`01a048a6-68f8-74f1-b56e-d6c9fe4aef4b`, line 803.

*Inference: The psyche identified that "AgentIntercomGraphical" was a composite
gate that bundled unrelated concerns: agent intercom, generic graphical
facilities, and desktop applications. The correct decomposition is:
(1) Agent intercom follows Claude/Codex presence -- no gate needed.
(2) Graphical facilities belong to the Edge node concept.
(3) Desktop apps require Edge plus cumulative Medium size, with unjustified
architecture gates (x86) removed.
The composite flag must be deleted and each gated concern re-derived from
what it actually depends on.*

---

## Medium graphical nodes: desktop apps for Bird

### "I would like medium graphical nodes to have codex and claude desktop apps"

> I would like medium graphical nodes to have codex and claude desktop apps
> installed.

-- psyche, typed, 2026-08-25T00:38+02:00. Recorded in
`flows/01a0338f/vision/mediumGraphicalNodes.md`.

### "just medium size"

> no, just medium size, and there used to be a node role that meant it had
> graphical aspects enabled. Find out how things are now.

-- psyche, typed, 2026-08-25T12:30+02:00. Recorded in
`flows/01a0338f/vision/mediumGraphicalNodes.md`.

### "tui and desktop versions line up"

> and we should have a way that ensures the tui and desktop versions line up
> (do they share some code?).

-- psyche, typed, 2026-08-25T00:38+02:00. Recorded in
`flows/01a0338f/vision/tuiAndDesktopVersions.md`.

*Inference: The psyche wants Claude and Codex desktop applications available
on medium-sized graphical nodes (which would include Zeus/Bird). TUI and
desktop versions must be synchronized. This is the desired end-state that
the AgentIntercomGraphical slop was blocking.*

---

## Identifying the cause of agentic failure

### "youre so short sighted"

> youre so short sighted. we are addressing skills here. youre putting out
> fires while ignoring the pyromaniac with a flamethrower; youll be putting
> out fires and wasting my time forever. you still havent found the cause of
> anything. which means theres a deeper failure; you dont understand how to
> identify the cause of agentic failure

-- psyche, typed, 2026-08-28. Session
`01a04881-741f-7591-ba44-6ed77dca4b7b`, line 387.

*Inference: The psyche sees the deployment-plane failures (wrong node
deployed, slop gates, broken wrappers) as symptoms of a deeper failure in
how agents are trained. Fixing individual broken outputs without finding the
governing cause in the skills is wasted time. The psyche frames this as a
skill-design problem, not a code problem.*

---

## Simplicity and minimal machinery

### "all we need to do is get the codex derivation from the same place"

> all we need to do is get the codex derivation from the same place. declared
> once, used everywhere. youre overcomplicating this to the extreme

-- psyche, typed, 2026-08-25T14:22+02:00. Recorded in
`flows/01a038be/vision/codexDerivation.md`.

### "we dont allow installing software statefully"

> which shouldnt even show up: we dont allow installing software statefully

-- psyche, typed, 2026-08-25T17:54+02:00. Recorded in
`flows/01a038be/vision/installingSoftwareStatefully.md`.

### "I would rather keep the flake very minimal; an entry point"

> I would rather keep the flake very minimal; an entry point

-- psyche, typed, 2026-08-19T12:42+02:00. Recorded in
`psyche-raw/Vision/minimalFlake.md`.

*Inference: The psyche consistently cuts toward minimal machinery. One source
for each derivation, no stateful installation, minimal flakes. Agents keep
expanding solutions beyond what is needed and the psyche keeps cutting back.*

---

## The initial state of deployment: "everything is a fucking mess"

### "right now everything is a fucking mess"

> So we were having problems. Well, there's a few things, and one of which is
> right now everything is a fucking mess. So don't trust anything. Don't
> assume anything. Be careful where you step.

-- psyche, dictated, 2026-08-08T11:37+02:00. Session
`019fe121-b1ea-7350-922b-826d0ce83a37`, line 9.

### "make sure KareemOS and KareemOS Home are in sync"
[STT: "KareemOS" = CriomOS]

> So with all this said, see if you can reliably get the latest version. Like
> make sure KareemOS and KareemOS Home are in sync that they don't have like
> we've been having this problem with them falling out of sync.

-- psyche, dictated, 2026-08-08T11:37+02:00. Session
`019fe121-b1ea-7350-922b-826d0ce83a37`, line 9.

### "we need to fix Zeus's VS code so that my friend can keep working"

> But, yeah, we need to fix Zeus's VS code so that my friend can keep working
> because her time is valuable and her creativity is valuable.

-- psyche, dictated, 2026-08-08T11:37+02:00. Session
`019fe121-b1ea-7350-922b-826d0ce83a37`, line 9.

### "If we have to use a hacky way to do it"

> If we have to use a hacky way to do it, then we're going to have to use a
> hacky way to do it. We have root access on all my hosts.

-- psyche, dictated, 2026-08-08T11:37+02:00. Session
`019fe121-b1ea-7350-922b-826d0ce83a37`, line 9.

### "logics [Lojix] is the deploy tool, but it might not work properly"

> And find out, yeah, logics, O-J-I-X [STT: spelling of Lojix] is the deploy
> tool, but it might not work properly.

-- psyche, dictated, 2026-08-08T11:37+02:00. Session
`019fe121-b1ea-7350-922b-826d0ce83a37`, line 9.

### "a full CREAMOS redeploy should change the user environment"
[STT: "CREAMOS" = CriomOS]

> I mean, I guess if you do a full CREAMOS redeploy on Zeus, it should change
> the user environment, but you might have to reload the user environment
> manually, which means SSH root into the host and then change to the user and
> reload.

-- psyche, dictated, 2026-08-08T11:37+02:00. Session
`019fe121-b1ea-7350-922b-826d0ce83a37`, line 9.

*Inference: The opening session establishes the psyche's framing of the whole
deployment plane: multiple hosts on different versions, CriomOS and
CriomOS-home falling out of sync, Lojix as the intended deploy tool that may
not work, root access as a practical fallback, and the pragmatic willingness
to use hacky methods when the correct ones are broken. The psyche explicitly
values Bird's productivity and wants the fix to reach her.*

---

## Nixpkgs update cadence

### "Update on the first commit exactly after the new moon"

> Update on the first commit exactly after the new moon every lunation.

-- psyche, typed, 2026-08-17. Recorded in
`psyche-raw/Vision/setupIndependentInterfaces.md`.

*Inference: The nixpkgs pin follows a lunar cycle. This is a concrete,
unconventional cadence choice that reveals the psyche's preference for a
natural rhythm rather than an arbitrary version schedule.*

---

## Lojix skill: placement reversal

### First ruled against, then for

> We wont use a skill called lojix; thats nonsensical. Thats what
> operating-system is for.

-- psyche, typed, 2026-08-19T22:20+02:00. Session
`01a01bac-91d6-7161-80c3-6f9ca38c7cf5`, line 9.

> we should create a lojix skill that properly documents it, and reference it
> in operating-system

-- psyche, typed, 2026-08-20T11:20+02:00. Session
`01a01bac-91d6-7161-80c3-6f9ca38c7cf5`, line 271.

> it must explain the syntax. dotos/datom is strict

-- psyche, typed, 2026-08-20T11:49+02:00. Session
`01a01bac-91d6-7161-80c3-6f9ca38c7cf5`, line 310.

*Inference: The psyche initially resisted a standalone Lojix skill, seeing it
as belonging in operating-system. Within 13 hours the psyche reversed: Lojix
does deserve its own skill, and operating-system references it. The skill
must explain the strict Dotos/Datom syntax. The reversal is genuine -- the
psyche reconsidered overnight and gave the corrected direction. The later
entry supersedes.*

---

## Orchestrate deployment and the deployment plane's naming

### "everything is going to be a nexus"

> what is "legacy nexus"?

> everything is going to be a nexus. so are you going to call everything the
> same thing? if you want to talk about orchestrate, say orchestrate. why are
> you saying nexus?

-- psyche, typed, 2026-08-26. Session
`01a03fe9-426c-7653-a3f2-ffee7e4653dd`, lines 416 and 427.

*Inference: The psyche insists on using the correct specific name
(Orchestrate) rather than the generic category name (Nexus). Every component
is a Nexus, so calling Orchestrate "the Nexus" is useless. Name the specific
thing.*

---

## Deployment preflight block: missing deployment selection

The 01a048a6 flow log records: "No authoritative `manifests/*.dotos` selection
supplies the required explicit store/SSH transport, builder, selector, and
input mode for Ouranos and Zeus."

The `manifests/` directory exists but is empty.

The AGENTS.md instructs: "Identity and deployment selection are only
`manifests/*.dotos`."

*Observation: No psyche quote on deployment selection was found in the
searched transcripts. The `manifests/*.dotos` pattern is referenced in
AGENTS.md as the canonical deployment-selection location, but no manifest has
been created yet. This blocks deployment of the corrected AgentIntercom work.
Whether the psyche has spoken on the exact shape of deployment selection
manifests remains unknown from this search.*

---

## Tensions and unresolved points

1. **Deploy-first order vs. declarative purity.** The psyche says "redeploy
   with only the newer Lojix daemon, nothing else" and also "no hot fixes,
   use the nix user env only, or OS redeploy." If the current Lojix is
   broken, you cannot use Lojix to fix Lojix. The psyche acknowledged this
   ("If we have to use a hacky way to do it") but the permanent resolution
   is unclear -- bootstrap is an authorized exception, but its boundaries
   are not formally recorded as a psyche ruling.

2. **Home equivalence is declared but not yet realized.** The psyche ruled
   that embedded and independent Home must be identical, fed from Horizon.
   But the current architecture still has the OS evaluation providing some
   Home values. The extended-horizon standalone repository is proposed but
   does not exist.

3. **criomos-core is approved but not created.** The supersession of
   CriomOS-lib by criomos-core was approved, but no repository exists yet.
   The Horizon service failure boundary remains unresolved.

4. **Deployment selection manifests are empty.** The `manifests/*.dotos`
   pattern is declared in AGENTS.md as the canonical location for deployment
   selection, but the directory is empty, blocking deployment of current
   work.

5. **Skill training vs. the recurring pattern.** The psyche keeps finding
   that agents add unauthorized mechanisms (flags, timeouts, hardwired
   variables, wrapper scripts, extra gates). Each time the psyche removes
   them and asks for better training. But the training corrections have
   been narrow (three sentences on node/activation matching). Whether the
   deeper structural cause that the psyche identified ("you dont understand
   how to identify the cause of agentic failure") has been addressed remains
   open.

---

## Sources

### Codex transcripts (searched directly)

- `/home/li/.codex/sessions/2026/08/08/rollout-2026-08-08T13-28-29-019fe121-b1ea-7350-922b-826d0ce83a37.jsonl` (session 019fe121)
- `/home/li/.codex/sessions/2026/08/09/rollout-2026-08-09T13-21-08-019fe641-5399-7fc3-8559-bda58cfbc632.jsonl` (session 019fe641)
- `/home/li/.codex/sessions/2026/08/13/rollout-2026-08-13T14-00-33-019ffafe-d8dd-7421-ad2e-58fc98ee5240.jsonl` (session 019ffafe)
- `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T17-11-18-01a01a93-a27d-7e73-944a-4501e67ce65d.jsonl` (session 01a01a93)
- `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T22-18-09-01a01bac-91d6-7161-80c3-6f9ca38c7cf5.jsonl` (session 01a01bac)
- `/home/li/.codex/sessions/2026/08/22/rollout-2026-08-22T23-00-27-01a02b46-5e97-7632-8db5-780391553085.jsonl` (session 01a02b46)
- `/home/li/.codex/sessions/2026/08/23/rollout-2026-08-23T20-33-13-01a02fe5-ee5a-7a31-92bc-f500f2dc7712.jsonl` (session 01a02fe5)
- `/home/li/.codex/sessions/2026/08/24/rollout-2026-08-24T00-22-08-01a030b7-83db-72c1-a965-d4256df34349.jsonl` (session 01a030b7)
- `/home/li/.codex/sessions/2026/08/24/rollout-2026-08-24T10-31-14-01a032e5-2852-72c0-a184-c88c82dd4490.jsonl` (session 01a032e5)
- `/home/li/.codex/sessions/2026/08/26/rollout-2026-08-26T23-10-46-01a03fe9-426c-7653-a3f2-ffee7e4653dd.jsonl` (session 01a03fe9)
- `/home/li/.codex/sessions/2026/08/28/rollout-2026-08-28T15-13-58-01a04881-741f-7591-ba44-6ed77dca4b7b.jsonl` (session 01a04881)
- `/home/li/.codex/sessions/2026/08/28/rollout-2026-08-28T15-54-20-01a048a6-68f8-74f1-b56e-d6c9fe4aef4b.jsonl` (session 01a048a6)

### Psyche-raw records

- `psyche-raw/Vision/lojixOwnership.md`
- `psyche-raw/Vision/setupIndependentInterfaces.md`
- `psyche-raw/Vision/host-environment-recovery.md`
- `psyche-raw/Vision/minimalFlake.md`

### Flow vision files

- `flows/01a02b46/vision/zeusUpdate.md`
- `flows/01a030b7/vision/zeusUpdate.md`
- `flows/01a030a1/vision/commonGround.md`
- `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`
- `flows/01a02b4b/vision/homeEquivalence.md`
- `flows/01a02fe5/vision/skillTraining.md`
- `flows/01a04881/vision/cause.md`
- `flows/01a04881/vision/agentIntercomGraphical.md`
- `flows/01a04881/vision/repeatingLikeThis.md`
- `flows/01a04881/vision/subflows.md`
- `flows/01a048a6/vision/agentIntercomGraphical.md`
- `flows/01a01bac/vision/skillDesigning.md`
- `flows/01a0338f/vision/mediumGraphicalNodes.md`
- `flows/01a0338f/vision/tuiAndDesktopVersions.md`
- `flows/01a038be/vision/installingSoftwareStatefully.md`
- `flows/01a038be/vision/codexDerivation.md`
- `flows/019fe121/vision/hostEnvironmentRecovery.md`
- `flows/019fe121/vision/nonIdealAgents.md`
- `flows/019fe641/vision/hostEnvironmentRecovery.md`
- `flows/01a03d6e/vision/orchestrateDeployment.md`
- `flows/01a03d6e/vision/orchestrateSkill.md`

### Flow logs

- `flows/01a02fe5/log.md`
- `flows/01a02b46/log.md`
- `flows/01a030b7/log.md`
- `flows/01a032e5/log.md`
- `flows/01a03fe9/log.md`
- `flows/01a04881/log.md`
- `flows/01a048a6/log.md`
- `flows/01a01bac/log.md`
- `flows/01a030e8/log.md`
- `flows/d098fa2d/log.md`
- `flows/491750ff/log.md`

### Witnesses

- `flows/01a04881/witnesses/zeusDeploymentAndDesktopGate.md`
- `flows/01a032e5/reports/criomosB8xDeployment.md`

### Skills (agent instructions, not the psyche's words)

- `.claude/skills/lojix/SKILL.md`
- `.claude/skills/operating-system/SKILL.md`
- `.claude/skills/breaking-upgrades/SKILL.md`
