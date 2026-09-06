# Psyche on Zeus Deployment

Verbatim psyche entries touching Zeus, CriomOS deployment, Lojix, network topology, boot/activation, upgrade sequencing, and deploying to a machine the psyche's partner uses. Entries are ordered oldest-first within each topic. Vision entries are ruling; Notion entries bind nothing until raised.

---

## Topic: Zeus — identity and who uses it

**File:** `flows/01a02b46/vision/zeusUpdate.md`
**Provenance:** 2026-08-08T11:37:36.634Z, session `019fe121-b1ea-7350-922b-826d0ce83a37`, physical line 9, transcript `/home/li/.codex/sessions/2026/08/08/rollout-2026-08-08T13-28-29-019fe121-b1ea-7350-922b-826d0ce83a37.jsonl`
**Level:** Vision (raw)

> So Zeus, another host where my partner works, is having problems.

**File:** `flows/019fe121/vision/hostEnvironmentRecovery.md`
**Provenance:** 2026-08-08T11:37:36.634Z, session `019fe121-b1ea-7350-922b-826d0ce83a37`
**Level:** Vision (raw)

> But, yeah, we need to fix Zeus's VS code so that my friend can keep working because her time is valuable and her creativity is valuable.

> And I need obviously BIRD. BIRD is my partner's username. So BIRDS, VS codes, cloud and codecs extensions need to be fixed. They're broken. There's like glitches on codecs and cloud doesn't even load. So let's make sure that all of this is at the latest version and maybe even rethink the whole way of how these VS code extensions are updated or obtained or deployed or I don't know what.

---

## Topic: What "latest" means and the sync requirement before deploying

**File:** `flows/01a02b46/vision/zeusUpdate.md` (also `flows/019fe121/vision/hostEnvironmentRecovery.md`)
**Provenance:** 2026-08-08T11:37:36.634Z, session `019fe121-b1ea-7350-922b-826d0ce83a37`, physical line 9
**Level:** Vision (raw)

> So with all this said, see if you can reliably get the latest version. Like make sure KareemOS and KareemOS Home are in sync that they don't have like we've been having this problem with them falling out of sync. And like the user environment is using the wrong version of something that it doesn't match the version on KareemOS or vice versa. And that cloud and codecs are up to date.
>
> So then once we got all that lined up, we need to redeploy Zeus on the latest version.

---

## Topic: Nixpkgs pinning — what "latest" nixpkgs means

**File:** `vision-raw/setupIndependentInterfaces.md`
**Provenance:** 2026-08-17, agent-authored context names the source as the current session at the time; no session id recorded in the file
**Level:** Vision (raw, vision-raw; not yet distilled)

> Update on the first commit exactly after the new moon every lunation.

Agent-authored context in the file: nixpkgs pin updates follow the lunar cycle — the first commit on the nixpkgs repo after each new moon becomes the pin for that lunation.

---

## Topic: The deploy method — full OS redeploy; user environment may need manual reload

**File:** `flows/01a02b46/vision/zeusUpdate.md` (also `flows/019fe121/vision/hostEnvironmentRecovery.md`)
**Provenance:** 2026-08-08T11:37:36.634Z, session `019fe121-b1ea-7350-922b-826d0ce83a37`
**Level:** Vision (raw)

> Let's figure out how we're going to redeploy Zeus. If we have to use a hacky way to do it, then we're going to have to use a hacky way to do it. We have root access on all my hosts.

> And find out, yeah, logics, O-J-I-X is the deploy tool, but it might not work properly.

> I mean, I guess if you do a full CREAMOS redeploy on Zeus, it should change the user environment, but you might have to reload the user environment manually, which means SSH root into the host and then change to the user and reload.

Note: "CREAMOS" is the psyche's speech-to-text rendering of CriomOS. "logics, O-J-I-X" is the psyche's STT rendering of Lojix.

---

## Topic: No hot fixes — authorised surfaces only

**File:** `flows/01a02b46/vision/zeusUpdate.md` (also `flows/01a01a93/vision/hostEnvironmentRecovery.md`)
**Provenance:** 2026-08-19T18:42:58.998Z and 2026-08-19T18:43:15.438Z, session `01a01a93-a27d-7e73-944a-4501e67ce65d`, physical lines 1878 and 1894
**Level:** Vision (raw)

> dont do hot fixes

> use the nix user env only, or OS redeploy

---

## Topic: Direct deploy authority — do not ask again

**File:** `flows/01a02b46/vision/zeusUpdate.md` (also `flows/01a01a93/vision/hostEnvironmentRecovery.md`)
**Provenance:** 2026-08-19T21:03:41.822Z, session `01a01a93-a27d-7e73-944a-4501e67ce65d`, physical line 2213
**Level:** Vision (raw)

> well lets talk later where it should be recorded but dont ask again. If I say deploy just deploy it

---

## Topic: Lojix ownership — OS only; past database disposable; deploy Lojix first

**File:** `vision-raw/lojixOwnership.md`
**Provenance (entry 1):** 2026-08-13T15:40:20+02:00
**Level:** Vision (raw, vision-raw; not yet distilled)

> it should only be in OS

**Provenance (entry 2):** 2026-08-13T23:32:19+02:00

> I dont care about any past lojix database.

**Provenance (entry 3):** 2026-08-14T09:06+02:00
Agent-authored context in the file: after discovering the installed daemon (0.11.0, schema v2) cannot read the store (schema v4, written by 0.17.x), blocking lojix-bootstrap from generating fresh materialized inputs.

> the system has to be redeployed with only the newer Lojix daemon, nothing else. And then we can use Lojix to deploy the upgrade. That should have been done already.

---

## Topic: Deployment interface — no setup-specific scripts; CLI only

**File:** `vision-raw/setupIndependentInterfaces.md` (also `flows/01a01046/vision/setupIndependentInterfaces.md`)
**Provenance:** 2026-08-14
**Level:** Vision (raw, vision-raw; not yet distilled)

> I don't want setup-specific scripts in general repos. Everything must be setup-independent with simple clear interfaces that agents can easily adapt to their needs.

> Seems like letting agents "fix" it ended up abandoning my vision. The interface is lojix and meta-lojix CLI only.

> An agent broke the invariant. Get rid of the flag and expose the option through nota/dotos. Remove any and all flags from lojix, replace them all. CLIs cannot accept any other type of argument than the typed input object. I feel like I keep repeating myself.

---

## Topic: Cluster data — universal; never hardwire a host name

**File:** `flows/019fe641/vision/hostEnvironmentRecovery.md`
**Provenance:** 2026-08-09T13:00:32.409Z, session `019fe641-5399-7fc3-8559-bda58cfbc632`, physical line 760
**Level:** Vision (raw)

> nothing to do with bird, this is a criomos-home fix, universal. nothing in this should hardwire bird or zeus anywhere

---

## Topic: Cluster data — what it is for; host name inferred from it

**File:** `flows/966be8/vision/clusterData.md`
**Provenance:** 2026-09-03T15:59:07+02:00, typed
**Level:** Vision (raw)

> Your first proposal, "put Zeus' current transfer and activation routes into cluster data," seems to misunderstand what cluster data is. I think what you're trying to suggest, or what needs to happen here, is not what you're suggesting. You're misunderstanding what cluster data is for. Inferring the name of the host from the cluster data is extremely straightforward. That's probably all that's missing: just an explanation of how one is derived from the other.

---

## Topic: Network — Ethernet for Nix-path transfer, hostname for activation

**File:** `flows/01a02b46/vision/zeusUpdate.md`
**Provenance:** 2026-08-22T21:26:43.173Z, session `01a02b46-5e97-7632-8db5-780391553085`, physical line 234
**Level:** Vision (raw)

> zeus should resolve now but prefer 192.168.18.95 for now, which is a direct ethernet route, will be much transfer to transfer the nix paths

**Provenance:** 2026-08-22T21:27:17.954Z, session `01a02b46-5e97-7632-8db5-780391553085`, physical line 254

> after the nix paths are moved zeus.goldragon.criome is fine for activation/etc

**File:** `flows/01a030b7/vision/zeusUpdate.md`
**Provenance:** 2026-08-24T00:26:58+02:00, typed in flow `01a030b7`
**Level:** Vision (raw)

> Then resume the zeus update. use its ethernet LAN ip address 192.168.18.95 if you need to move nix paths to it (yggdrassil is over wifi and will be very slow and heavy, but it's fine for activation and other non-heavy transfers usage)

Note: the `01a030b7` entry is later and supersedes on the network routing detail. Both entries agree: Ethernet (192.168.18.95) for Nix-path transfer; Yggdrasil / hostname (zeus.goldragon.criome) for activation and light traffic.

---

## Topic: Boot and activation protocol — approved design

**File:** `flows/01a02b46/vision/zeusUpdate.md`
**Provenance:** 2026-08-23T12:18:00.608Z, session `01a02b46-5e97-7632-8db5-780391553085`, physical lines 2376–2377; the proposal being answered is at physical lines 2370–2372
**Level:** Vision (raw)

Context (recorded in the file): This reply answers the immediately preceding assistant proposal: normal `ActivateNow`/`SetBootProfile` clear both EFI default and one-shot overrides so declarative `loader.conf` is the sole persistent authority; `ScheduleBootOnce` reads the actual hash-named candidate from `loader.conf`, preserves the current boot entry as the persistent fallback, and sets the candidate one-shot; EFI write failure remains terminal; and legacy synthesized `nixos-generation-N.conf` is removed, including bootstrap.

> yes

---

## Topic: Breaking upgrade documentation

**File:** `flows/01a02b46/vision/zeusUpdate.md`
**Provenance:** 2026-08-23T12:46:07.017Z, session `01a02b46-5e97-7632-8db5-780391553085`, physical lines 2648–2649
**Level:** Vision (raw)

> whenever a breaking upgrade like that takes place, the documentation on how to deploy the break must go in the repository as well, in a canonical place, and it must be corrected if it turns out to fail or partially fail in practice. we need a skill proposal for this.

---

## Topic: Hardwired deployment-node variables rejected; training over hardwiring

**File:** `flows/01a02fe5/vision/skillTraining.md`
**Provenance:** 2026-08-24 and 2026-08-25, typed; flow `01a02fe5`
**Level:** Vision (raw)

Context (file): after establishing that an agent constructed a Lojix request whose logical node was Zeus and whose activation transport was Ouranos.

> We need better skill training

> it doesnt matter why. those variables are confusing. we should rely on good training instead of trying to hardwire which node all situations should use, which is obviously wrong

> remove those hard wired deployment variables and propose skill training that explains how the cluster works, what the nodes are, how to verify which node one is working on or building or deploying on/for, etc etc

**Provenance:** 2026-08-25

> way too complex. start with ultra minimal

> ok approved. and we have removed the static deployment variables?

---

## Topic: Deployment selection — IPv4 is temporal; .dotos is stale

**File:** `flows/01a048a6/vision/deploymentSelection.md`
**Provenance:** not timestamped in file; flow `01a048a6`, typed
**Level:** Vision (raw)

> the ipv4 address is extremely temporal and should not be relied upon. what manifest? .dotos is now considered stale, and whatever is using them should migrate to using datom instead

---

## Topic: Trust — all hosts trusted; trust derives from cluster data

**File:** `flows/01a05e53/vision/hostTrust.md`
**Provenance:** typed, flow `01a05e53`
**Level:** Vision (raw)

> It doesnt matter if a remote builder or evaluator is used; we trust all our hosts.

> The part where it says that everything is equally trusted is kind of true, but the trust is in the cluster data. Technically, I'm not sure. Maybe you wanna look into the Creome OS code, but if something is a builder, then I think it has a minimum amount of trust. I don't think we have a problem trusting if we trust something to build and we trust it enough to evaluate. There's no trust issue here if you follow what I'm saying.

---

## Topic: Nix evaluation and build placement

**File:** `flows/01a05e53/vision/nixExecution.md`
**Provenance:** typed, flow `01a05e53`
**Level:** Vision (raw)

> If there are no remote builders, then we have to build locally. That line is not quite correct.

> If we can run evaluations remotely, then we should also.

---

## Topic: No stateful software installation

**File:** `flows/01a038be/vision/installingSoftwareStatefully.md`
**Provenance:** 2026-08-25T17:54:08+02:00; flow `01a038be`
**Level:** Vision (raw)

> which shouldnt even show up: we dont allow installing software statefully

---

## Topic: Old Orchestrate is broken — ditch it

**File:** `flows/01a03d6e/vision/archive-orchestrateDeployment.md`
**Provenance:** 2026-08-26T10:10:32.842Z, session `01a03d6e-5cb8-7b60-b573-7f59413bc18e`, records 300–301
**Level:** Vision (raw; file name `archive-orchestrateDeployment` indicates the ruling is the archival of the old deployment)

> Well, the previous Orchestrate is broken, so I don't care about it.
>
> So we don't care about the old deployment. It's actually just creating problems because agents try to use it and it doesn't even work.
>
> So what I would do is just ditch the old Orchestrate.

---

## What was NOT found

- **Generations and rollback:** The psyche has not stated a position on NixOS generation management (how many to keep, rollback policy, or garbage collection timing) in any Vision, vision-raw, flows/*/vision/, or flows/*/notion/ file found.
- **What "latest CriomOS" resolves to concretely:** The psyche has described the sync requirement (OS and Home at matching commits, cloud and codecs up to date) but has not stated a formal definition of what constitutes the latest CriomOS revision or how to confirm it.
- **Upgrade sequencing beyond Lojix-first:** Beyond the Lojix-first rule (deploy Lojix daemon before using Lojix to deploy the upgrade), the psyche has not stated a multi-step upgrade order for other components.
- **Reboots — timing and consent:** Beyond the approved boot/activation protocol (ScheduleBootOnce, declarative loader.conf, hash-named candidate, one-shot), the psyche has not stated whether an agent may initiate a reboot without per-deployment approval.

---

## Sources

| File | Level | Date range |
|---|---|---|
| `flows/019fe121/vision/hostEnvironmentRecovery.md` | Vision raw | 2026-08-08 |
| `flows/019fe641/vision/hostEnvironmentRecovery.md` | Vision raw | 2026-08-09 |
| `vision-raw/lojixOwnership.md` | Vision raw (vision-raw) | 2026-08-13 – 2026-08-14 |
| `vision-raw/setupIndependentInterfaces.md` | Vision raw (vision-raw) | 2026-08-14 – 2026-08-17 |
| `flows/01a01046/vision/setupIndependentInterfaces.md` | Vision raw | 2026-08-17 |
| `flows/01a01a93/vision/hostEnvironmentRecovery.md` | Vision raw | 2026-08-19 |
| `flows/01a02b46/vision/zeusUpdate.md` | Vision raw | 2026-08-08 to 2026-08-23 |
| `flows/01a02fe5/vision/skillTraining.md` | Vision raw | 2026-08-24 – 2026-08-25 |
| `flows/01a030b7/vision/zeusUpdate.md` | Vision raw | 2026-08-24 |
| `flows/01a03d6e/vision/archive-orchestrateDeployment.md` | Vision raw | 2026-08-26 |
| `flows/01a038be/vision/installingSoftwareStatefully.md` | Vision raw | 2026-08-25 |
| `flows/01a048a6/vision/deploymentSelection.md` | Vision raw | undated |
| `flows/01a05e53/vision/hostTrust.md` | Vision raw | undated |
| `flows/01a05e53/vision/nixExecution.md` | Vision raw | undated |
| `flows/966be8/vision/clusterData.md` | Vision raw | 2026-09-03 |
| `flows/542442/notion/terminology.md` | Notion | undated |
| `flows/542442/notion/pod.md` | Notion | undated |
