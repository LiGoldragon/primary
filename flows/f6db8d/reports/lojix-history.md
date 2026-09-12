# Lojix — what every flow tried, what the living asked for, and what is still owed

Read-only remembering, 2026-09-11/12, by subflow thread
`f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d. Nothing was written
outside this file. Repositories were read with `git show`/`grep` without
checkout; the live service was read with `systemctl`, `journalctl`, `ls`,
`strings`, `lojix-inspect-store` (documented read-only) and two ordinary
`Query` calls. No `meta-lojix`, no `Deploy`/`Pin`/`Retire`/`Test`, no reset.

Throughout: **witnessed** = this flow or a read-only subflow of it opened the
file or ran the command; **relayed** = another flow's log or report says so and
is named. Observations, hypotheses and unknowns are kept apart.

The living's standing order for this work (`~/.claude/projects/-home-li-primary/f6db8d14-1dfe-472d-914e-9c441f852834.jsonl:305`, 2026-09-12T02:05:29Z, typed):

> Logics has been problematic. Look around, remember a bunch of stuff, and see what sessions tried to do that weren't finished or done properly, and see if you can finish them or do them properly.

---

## 0. The three sentences that matter

1. **Nothing built for Lojix since 2026-09-05 has ever run.** The live service
   on Ouranos is `lojix-0.21.1`, built 2026-09-09. Everything after it —
   0.21.1 → 1.0.0 → 1.0.1 → 2.0.0, the whole Nexus port — exists only as source
   and Nix checks. Witnessed §3.
2. **The next deployment cannot start the service.** CriomOS pins lojix
   `23f09f28` (1.0.1), whose workspace produces no `lojix-daemon` binary and
   whose Nexus refuses any argument; `CriomOS/modules/nixos/lojix.nix:27` still
   builds `ExecStart=${package}/bin/lojix-daemon ${startupArchivePath}`.
   Witnessed §4.1.
3. **The one defect every flow named, nobody fixed.** Lojix collapses each
   pipeline stage failure into a generic reason and discards the captured
   stderr. It has cost at least six flows their diagnosis. Witnessed §4.3,
   open bead `primary-cod`.

---

## 1. Chronology — what each flow tried, finished, and left

Dates are the first commit in the flow's lane unless stated.

### 1.1 Before flows — 2026-07-24 .. 2026-08-21

Relayed from `/home/li/primary/reports/` (legacy, pre-flow) and from
`flows/674a4dab/reports/psycheLojix.md`.

The living's framing of the period, dictated 2026-08-08 (`019fe121-…:9`):

> right now everything is a fucking mess. So don't trust anything. Don't assume anything. Be careful where you step.

> And find out, yeah, logics, O-J-I-X is the deploy tool, but it might not work properly.

What was attempted and what stuck:

- **v1→v2 store migration and closure validation** —
  `reports/lojix-v1-v2-migration-proposal-2026-07-28.md`,
  `lojix-v1-v2-validation-2026-07-28.md`,
  `lojix-criomos-closure-validation-2026-07-28.md`. Superseded: the store went
  v2 → v3 → v4 → v5 afterwards, and the living later ruled the history
  disposable.
- **Ownership split resolved.** The living ruled 2026-08-13 that Lojix is
  OS-only; `CriomOS/checks/lojix-ownership/default.nix` now enforces it and
  CriomOS-home has no lojix reference. **Finished and still holding** (witnessed
  by me: the check file exists and asserts four absences).
- **A deployed daemon far behind its source.** The daemon was 0.11.0 (schema
  v2) against a v4 store on 2026-08-14. The living: *"the system has to be
  redeployed with only the newer Lojix daemon, nothing else."* Done at the time
  — **and the identical condition has returned today** (§3).
- **Flag creep and wrapper scripts.** An agent wrote `ouranos-activate.sh` and
  passed `--override-input horizon <path>`. Both removed; the no-flags invariant
  now holds in code (`src/lib.rs` rejects `-`-prefixed arguments; witnessed by
  the 674a4dab audit at §2.11, re-checked by me at `clients/*/src`).

### 1.2 2026-08-22 — flows/01a01bac — the Lojix skill

Goal: pick up where 01a01a93 left off on root-deployment guidance.

The living first ruled against a Lojix skill (2026-08-19T22:20), then reversed
within 13 hours (2026-08-20T11:20), then approved the text
(`flows/01a01bac/vision/skillDesigning.md:10,21,31,43`).

- **Finished:** the authored `lojix` skill landed at
  `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md`.
- **Left wrong:** it has not been touched since `8483e20` (2026-09-03) and is
  now false in five independent ways (§4.2). This is the single highest-leverage
  unfinished item, because every agent that deploys reads it.

### 1.3 2026-08-22 .. 08-24 — flows/01a02b46, 01a02fe5, 01a030a1, 01a030e8

Zeus update, then the SSH outage and the "deployment 49" incident.

- **Finished:** an unapproved wall-clock timeout was found and removed
  (`reports/lojixTimeoutRemovalImplementation.md`) after *"what timeout? I never
  approved any timeout"*; the `breaking-upgrades` skill landed; the static
  deployment variables were deleted and replaced with three sentences of
  cluster training (`flows/01a02fe5/vision/skillTraining.md`).
- **Left open:** the living's diagnosis — *"youre so short sighted … you dont
  understand how to identify the cause of agentic failure"* — was answered with
  a narrow training edit, not a structural change. §5 item 9.

### 1.4 2026-08-28 — flows/674a4dab — the audit that named the defects

Goal (the living, STT, `674a4dab-…:9`): audit CriomOS, "Logix" and Horizon for
"bad designs and flaws … quackery, sloppiness, hallucinations".

**Finished, and still the best document on Lojix:**
`flows/674a4dab/reports/auditLojix.md` (findings 2.1–2.13, an end-shape, a
six-step vertical-slice migration, seven unknowns) and `psycheLojix.md` (861
lines of dated verbatim psyche).

**Named there, still unfixed today (all re-witnessed by me in the working tree,
2026-09-11):**

| audit finding | today |
|---|---|
| `Query.ByDeployment` hard-coded `false` at `schema_runtime.rs:4187` | still `false`, moved to `src/schema_runtime.rs:4404` |
| `CheckHostKeyMaterial` returns `string_vector: Vec::new()` | unchanged at `src/schema_runtime.rs:4493-4500` |
| `manifests/*.dotos` empty — no deployment selection exists | `/home/li/primary/manifests/` **does not exist**, while `NON_MANAGEMENT_AGENTS.md:12` still says "Identity and deployment selection are only `manifests/*.dotos`" |
| 11 types duplicated between `runtime_flow.rs` and `runtime_model.rs`; `DeploymentPhase`/`DeploymentLifecycle` identical | unchanged |
| 13-field `Deploy.Host` | now **14** fields — `SecretsInput` was added by 542442 |

### 1.5 2026-08-29 — flows/4d5fc7da — the redesign that was never ruled

Goal (the living, typed): *"remember 674a4dab in depth and bring forward the
lojix redesign"*.

**Finished:** the redesign was carried to the living —
`Deploy.Host.{ NodeName Action Option<Revision> Option<Route> }`, everything
else read from configuration or Horizon; plus a Sema-anatomy cut list and a
`Vision/lojix.md` distillation proposal (`flows/4d5fc7da/log.md:78-89`).

**Left unfinished — this is the largest abandoned thread in the whole history:**

> 2026-08-29 — psyche (typed): "looks reasonable" on the brought-forward redesign, the three asks and the distillation proposal — read as agreement in direction, not as rulings on the action set, the route rule, the Sema anatomy, or approval of Vision/lojix.md; explicit word asked for each.
> — `flows/4d5fc7da/log.md:98-101`

Nothing was ever ruled. **There is still no `Vision/lojix.md`** (witnessed: `ls
/home/li/primary/Vision/` has no lojix entry). Every subsequent flow therefore
worked from scattered raw records. And the Deploy request went the other way:
542442 added a fifteenth concern rather than cutting to four.

### 1.6 2026-08-30 .. 09-04 — flows/01a052bb, 01a0539e, 01a05833, 5a3ee4, 966be8

Five point-releases, each repairing a real defect found in production:

| release | commit | what it repaired | flow |
|---|---|---|---|
| 0.20.0 | `76400200` | canonical `proposal.datom` admission, legacy `datom.dotos` removed | 01a052bb |
| 0.20.1 | `8bb4b0a1` | `ByDeployment`/`ByGeneration` product/scalar adapter mismatch | 01a05833 |
| 0.20.2 | `34a8e9c2` | same-host `TestActivation` killed the daemon from its own cgroup | 01a05833 |
| 0.20.3 | `d3c0ac90` | `ClosureCopy` now copies as root, so user-scoped transports work | 5a3ee4 |

**Done properly:** each shipped with a red-green witness (0.20.2's real NixOS VM
went red on 0.20.1 and green on 0.20.2; 92/92 library tests).

**Done badly / left open:**

- **Lojix killed its own control plane.** Deployment 109's TestActivation
  stopped `lojix-daemon.service` with `KillMode=control-group` and recorded no
  terminal state; recovery required the living to approve `systemctl start`
  by hand (`flows/01a05833/log.md:22-30`). 0.20.2 fixed *that* path. The general
  problem — **Lojix upgrading the host it runs on** — was never given a design.
  33a4d4 located the supported route (daemon-free bootstrap with
  `BootOnce`/`LocalBootstrapV1`) but did not take it.
- **Two deployments burned on a misleading reason code.** 5a3ee4's 158 and 162
  failed at CopyClosure reported as `BuilderUnreachable`; the real cause was
  `No route to host` on a stale LAN IP. `flows/5a3ee4/log.md:25` names the exact
  line. Not fixed.
- **966be8 landed the derivation rule into the skill** (`<node>.<cluster>.<internal
  suffix>`) after the living's correction — that part **is** finished and still
  correct in the skill.

### 1.7 2026-09-05/06 — flows/0062e8 and 542442 — the Datom renovation

0062e8 was pure design and produced the Horizon vision (§2). 542442 then built
it, on the living's mandate:

> We're going to migrate the datom codec to the latest version that just was implemented now … All of the stack, the horizon, logics, everything is going to move to the new datom
> — `flows/542442/vision/archive-datom.md:10`, psyche, STT

**Finished:** Horizon 0.6.0 (`05879e7c`) as a `HorizonConfiguration` +
`ClusterDefinition` → `horizon-definition.datom` composer; Lojix 0.21.0
(`7e29c37f`) consuming one root artifact, Datom/Signal ingress, explicit
`SecretsInput`, store v4→v5 with a red-green refusal test; a real secrets
symlink hole closed (`0d95061a`); a contract-ID collision found and fixed.

**Left unfinished or wrong — the most consequential set in this history:**

- **Never activated.** *"The implementation still excludes live activation,
  reboot, live-store migration, reboot or authored-skill change"*
  (`flows/542442/log.md:67,141,255`).
- **Abandoned mid-gate with locks held.** The last line of its log
  (`:277`): *"Attached remote C6 session 1132 is active, with no terminal result
  at this checkpoint."* Five days later its lock 851 was still blocking flow
  162eb3 (`flows/162eb3/log.md:11`).
- **The epic landed asymmetrically.** The CriomOS-home half went to `main`; the
  `horizon-rs` and CriomOS halves stayed on branches. db267d's repin pulled the
  Home half into production and every user-environment deployment died at Eval.
  The analysis is `flows/db267d/reports/overnight-renovation-and-rollback-fork.md`.
- **The skill edit was written and never applied.** The full replacement text
  sits at `flows/542442/reports/lojix-implementation.md:113-161` under its own
  admission (`:106-109`): *"No authored skill source or generated skill evidence
  was edited. The current generated `lojix` skill still says `## Dotos syntax`,
  gives parenthesized product examples … and says the daemon accepts schema
  v4."* **Witnessed by me: all four statements are still true today.**

### 1.8 2026-09-06 — flows/db267d — the rollback

The living's ruling, quoted at `flows/db267d/log.md:200-202`:

> Put all the changes that belong to this giant epic work onto a branch and roll back `main` to before that.

**Finished:** CriomOS-home `main` rolled to `ed958211`, the epic preserved on
`home-datom-renovation-from-main-542442`; bird's Claude Desktop fixed;
deployments 222–225 Succeeded.

**Left open:** `checks/lojix-ownership` deliberately red; bird's SSH key still
undeclared so her Lojix ledger and live state disagree; and the flow's own
verdict on the defect that cost it both dead ends
(`flows/db267d/log.md:149-154`): *"Lojix discarding activation-stage stderr
behind a single `ActivationFailed` code."*

### 1.9 2026-09-10 — flows/857335 — Lojix becomes a Nexus

**Finished, and genuinely well done:** five workspace packages
(`lojix-nexus`, `lojix`, `lojix-meta`, offline tools, bootstrap); durable
`ConfigurationState` with exact meta-Configure transitions — the realized form
of `Vision/nexus.md`'s "First configuration"; copy-only historical-store
migration that never opens the source for write; Horizon 0.8.0 emitting final
generated types across a data-only wire. Released lojix 1.0.1 `b8f7a8cc`,
horizon 0.8.0 `e4871220`, nexus 0.1.1.

Its own witness states the break plainly
(`flows/857335/witnesses/lojix-horizon-boundary.md:36`):

> There are no `lojix-daemon` or `meta-lojix` executable aliases.

**Left unfinished:**

- **Never deployed.** `reports/shutdown-runtime.md:3-6`: *"No production service
  was stopped, restarted, reconfigured, or deployed."* And nothing downstream —
  CriomOS's module, the skill, the env-var names — was updated to the new names.
- **Its own gap audit overstated the closure.** `reports/nexus-gap-audit.md:8-10`
  calls the Nexus-shape gaps closed. Flow f6db8d's `runtime-audit.md` §9 found
  three of five closures hold, one holds in part (Kameo), one holds with a
  caveat, and two unmentioned invariants are unmet (subscriptions,
  traits/free-functions).
- **Both skeptical audits were SIGINT-killed before any verdict** — the gate
  857335 itself set was never passed.

### 1.10 2026-09-11 — flows/fe34eb and 33a4d4

- **fe34eb** unified the frame into a `signal` crate and bumped lojix to
  **2.0.0** (`fab60e5`), with a real witness (the Nexus started and exchanged
  typed signals over both real Unix sockets). It also flagged a test it did not
  fix (`reports/signal-realization.md:205-210`): `lojix/tests/actor_native_runtime.rs`
  is a change-detector that greps `src/daemon.rs` for string literals — *"The
  testing discipline forbids such a test … It should be replaced or deleted."*
  **Witnessed by me: still present.**
- **33a4d4** pushed Horizon 0.9 (`49746ba3`), Datom 0.25.7, CriomOS `acc3feab`,
  and passed Lojix `23f09f28` remote tests — then stopped:
  *"Complete-system BuildOnly did not pass … The final complete-system source
  has no successful BuildOnly witness; component checks do not substitute for
  it"* (`flows/33a4d4/log.md:24,26`). Its blocking finding is that current
  Horizon no longer projects CPU vendor, board class, or lid-switch policy that
  legacy CriomOS metal code consumes. **I found a second, unreported instance of
  the same class** (§4.4).

---

## 2. The living's vision on Lojix — verbatim, oldest first

Sources are the raw session transcripts (`~/.codex/sessions/**`,
`~/.claude/projects/-home-li-primary/*.jsonl`) and the curated psyche records.
Claude transcripts begin 2026-08-09, Codex 2026-07-24; anything earlier survives
only in `vision-raw/`. STT renders Lojix as "logics"; the living corrected it
himself on 2026-09-05 and confirmed the referent on 2026-09-11.

**2026-07-25**, `~/.codex/sessions/2026/07/24/rollout-2026-07-24T23-36-15-019f960e-….jsonl:289`
> Yes. Can you deploy using an adhoc way? we have root aceess on all hosts.
>
> Then let's look at why lojix is failing to deploy properly.

**2026-07-28**, `…/2026/07/27/rollout-…-019fa340-….jsonl:1114`
> I'm not interested in backporting, I want to move forward. So, you're going to do a context handle that focuses on fixing the latest version of Lojix, deploying it, and then finally fixing Birds vs Codium.

**2026-07-28**, `…/2026/07/28/rollout-…-019fa893-….jsonl:9`
> So apparently the previous agent had trouble. We want to deploy a fix on another host in our cluster, and he's saying our deployment tool Logix needs to be fixed. So I don't want a backport. I don't want like an old version fixed. I want a new version fixed. So that means if the old version is deployed, we have to deploy the new version after testing it, or just deploy it and then test it in production because whatever, you're the only one using it. And it has to work anyway, so it's tested by using it.

**2026-07-28**, `…/2026/07/28/rollout-…-019fa847-….jsonl:9`
> I need Mind, I need Orchestrate, I need Logics to work properly, and they're always broken.

**2026-07-29**, `…-019fa893-….jsonl:1490`
> > After that, the remaining blocker is updating Ouranos's Lojix daemon
>
> wtf, agent have been talking about this for weeks. its like nobody actually does it. are you all fucking retarded and useless?

**2026-08-04**, `…/2026/08/01/rollout-…-019fbf4a-….jsonl:3801`
> make sure nothing no host names or anything like that is hardwired into lojix

**2026-08-06**, `…/2026/08/05/rollout-…-019fd35b-….jsonl:156`
> > CriomOS currently disables the Lojix daemon instead of upgrading it
>
> wtf is that about?

**2026-08-08**, `…/2026/08/08/rollout-…-019fe121-….jsonl:9` (dictated)
> And find out, yeah, logics, O-J-I-X is the deploy tool, but it might not work properly.

**2026-08-09**, `…/2026/08/09/rollout-…-019fe7eb-….jsonl:286`
> how the fuck does lojix end up running so far behind? something isnt right. this keeps fucking happening

**2026-08-10**, `…-019fe7eb-….jsonl:396`
> you can use a new lojix database if its easier

**2026-08-10**, `vision-raw/mainForEverything.md:8` (said during Lojix recovery, on a dependency pinned to a non-main branch)
> we should use main for everything

**2026-08-13**, `…/2026/08/13/rollout-…-019ffafe-….jsonl:409`
> I had an agent tell me lojix was in OS and home, which creates conflicts. it should only be in OS, and the broken lojix is probably really bad since agents have been trying to fix it for months. if I say "what exactly is wrong with it" I must admit I wont really trust you to know. sorry, but months of bad results destroys trust

**2026-08-13**, `…-019ffafe-….jsonl:573`
> I dont care about any past lojix database. how do we get a clean working lojix service running?

**2026-08-14**, `~/.claude/projects/-home-li-primary/5fa00ba7-….jsonl:2183`
> Yeah, Lojix is in the wrong version, so that means the system has to be redeployed with only the newer Lojix daemon, nothing else. And then we can use Lojix to deploy the upgrade. That should have been done already. I don't know why it wasn't done.

**2026-08-14**, `~/.claude/projects/-home-li-primary/d076fe3a-….jsonl:153`
> everything is designed to be consumed through lojix, including criomos

**2026-08-14**, `…d076fe3a….jsonl:162`
> seems like letting agents "fix" it ended up abandonning my vision.
>
> the interface is lojix and meta-lojix cli only

**2026-08-14**, `…d076fe3a….jsonl:344`
> an agent broke the invariant. get rid of the flag and expose the option through nota/dotos. remove any and all flags from lojix, replace them all.
>
> We need this invariant in the rust component skill. clis cannot accept any other type of argument than the typed inpud object. I feel like I keep repeating myself

**2026-08-14**, `vision-raw/setupIndependentInterfaces.md:3`
> I don't want setup-specific scripts in general repos. Everything must be setup-independent with simple clear interfaces that agents can easily adapt to their needs.

**2026-08-16**, `…d076fe3a….jsonl:779`
> skills should be deployed by their mere presence. but calling it lojix is bad. tell some random agent "lojix" see if he knows what thats for. and yes it should train agents on how to use lojix properly

**2026-08-17**, `…/2026/08/17/rollout-…-01a01046-….jsonl:1165`
> can you hot-start the deployment? then we can look at the lojix problem
>
> 2. I want to dedicate a session to this, otherwise itll probably be done badly

**2026-08-19**, `…/2026/08/19/rollout-…-01a01a93-….jsonl:1878, 1894`
> dont do hot fixes

> use the nix user env only, or OS redeploy

**2026-08-19**, `…-01a01a93-….jsonl:2213`
> well lets talk later where it should be recorded but dont ask again. If I say deploy just deploy it

**2026-08-19 → 08-20**, `flows/01a01bac/vision/skillDesigning.md:10,21,31,43` — the reversal
> We wont use a skill called lojix; thats nonsensical. Thats what operating-system is for.

> we should create a lojix skill that properly documents it, and reference it in operating-system

> it must explain the syntax. dotos/datom is strict

> looks good enough. deploy it

**2026-08-22**, `…-01a02b46-….jsonl:234, 254`
> zeus should resolve now but prefer 192.168.18.95 for now, which is a direct ethernet route, will be much transfer [faster] to transfer the nix paths

> after the nix paths are moved zeus.goldragon.criome is fine for activation/etc

**2026-08-23**, `…-01a02b46-….jsonl:1270, 1287`
> what timeout? I never approved any timeout

> get rid of that timeout and resume your goal

**2026-08-23**, `…-01a02b46-….jsonl:2648`
> whenever a breaking upgrade like that takes place, the documentation on how to deploy the break must go in the repository as well, in a canonical place, and it must be corrected if it turns out to fail or partially fail in practice. we need a skill proposal for this.

**2026-08-23**, `flows/01a02b4b/vision/homeEquivalence.md:5,15`
> there should be no difference between the embedded and independent home. the part which is shared ought to be directly from lojix-emitted horizon output, or from a shared nix machinery which uses the said horizon as input only.

> whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon (that could be a standalone repo for deriving some data in nix from the horizon data coming out of lojix)

**2026-08-24**, `…-01a02fe5-….jsonl:1173, 1231`
> it doesnt matter why. those variables are confusing. we should rely on good training instead of trying to hardwire which node all situations should use, which is obviously wrong

> remove those hard wired deployment variables and propose skill training that explains how the cluster works, what the nodes are, how to verify which node one is working on or building or deploying on/for, etc etc

**2026-08-25**, `…-01a02fe5-….jsonl:1489`
> way too complex. start with ultra minimal

**2026-08-26**, `…/2026/08/26/rollout-…-01a03d6e-….jsonl:300` — the Nexus ruling that governs Lojix
> we should make an invariant that the demons are not called demons but Nexus. So it should be Orchestrate Nexus, and all Nexuses should be like that.

**2026-08-26**, `…-01a03d6e-….jsonl:683`
> only problem is the bootstrap binary. There should be no bootstrap binary. So, in terms of configuring the Nexus, obviously, well it's going to have default configuration. … it can just have a constant in the executable with a default configuration. And because it has a default, well first it should try to get its state from the default location for its SEMA database. … So then there's no need for a bootstrap executable.

**2026-08-28**, `…-01a04881-….jsonl:387`
> youre so short sighted. we are addressing skills here. youre putting out fires while ignoring the pyromaniac with a flamethrower; youll be putting out fires and wasting my time forever. you still havent found the cause of anything. which means theres a deeper failure; you dont understand how to identify the cause of agentic failure

**2026-08-30**, `…/2026/08/30/rollout-…-01a052bb-….jsonl:334`
> explain to me what exactly is the lojix problem

**2026-09-04**, `~/.claude/projects/-home-li-primary/fd99506c-….jsonl:467` — build it into Lojix, not around it
> I think what you're suggesting means that we might want to modify Logics itself in order to support this explicitly, because otherwise it feels like we're doing duct tape and haywire here. So why don't you investigate how logic actually functions, what you're trying to achieve, and what that would look like if we added the logic and the right anatomy for it in Logics itself?

**2026-09-04**, `…/2026/09/04/rollout-…-01a06da9-….jsonl:9, 642`
> find out what the lojix problem is, so we can finish the mission

> did you get someone to investigate lojix itself?

**2026-09-05**, `flows/0062e8/vision/live-installation-image.md:25` (STT "logics" corrected by the living)
> I'm not sure where the additional node would come from, but I don't want to hardcode this into Lojix or anything. It would come in as an external additional input to Lojix that defines the default nodes for any cluster, so that it's maybe just merged, and then we would add this node type.

**2026-09-05**, `…/2026/09/05/rollout-…-01a0712d-….jsonl:71`
> and its lojix, not logics, stt error

**2026-09-05**, `…-01a0712d-….jsonl:732` — on Horizon
> Horizon has been left for poorly guided agents to do with it as they please. In all likelihood, it has been ravaged a little bit, so maybe we get some nice, clear, fresh vision into that.

**2026-09-05**, `…/2026/09/05/rollout-…-01a07275-….jsonl:9`
> All of the stack, the horizon, logics, everything is going to move to the new datom, and we're going to start migrating everything that uses datom, which means everything, to the new datom as we go along.

> maybe go and remember some other flows where we dealt with logics, because we're probably going to have to fix logics. It's been quite broken also for a while.

**2026-09-06**, `~/.claude/projects/-home-li-primary/0384e018-….jsonl:10` and `flows/0384e0/vision/deployIncludesUserEnvironment.md:7`
> Well, I want the user's environment to be up to date and refreshed. Whenever I say deploy, I always want that.

**2026-09-06**, `~/.claude/projects/-home-li-primary/7dc7cc87-….jsonl:6`
> After a user is deployed, we need to redeploy the entire operating system so that, if there's a reboot, the user environment isn't replaced with an older version.

**2026-09-06**, `flows/db267d/log.md:200-202`
> Put all the changes that belong to this giant epic work onto a branch and roll back `main` to before that.

**2026-09-09**, `~/.claude/projects/-home-li-primary/564f55c4-….jsonl:1062`
> The Nexus component is not going to do the textualization at all. That's only in the CLI and the client.

**2026-09-10**, `~/.claude/projects/-home-li-primary/fe34eb91-….jsonl:145, 176`
> a nexus is a daemon. every component we will build will be a nexus. so the nexus repo is the library that defines the core of a nexus component, which is a daemon

> The word Nexus is our word for the style of component that speaks signal and uses a similar database.

**2026-09-11**, `~/.claude/projects/-home-li-primary/fe34eb91-….jsonl:538` — the referent confirmed
> yes it was lojix. implement what is ruled. make your proposals.

**2026-09-12**, `~/.claude/projects/-home-li-primary/f6db8d14-….jsonl:305` — most recent
> Logics has been problematic. Look around, remember a bunch of stuff, and see what sessions tried to do that weren't finished or done properly, and see if you can finish them or do them properly.

### 2.1 Distilled vision that governs Lojix but does not name it

- `Vision/nexus.md:35-39` two sockets, meta privileged; `:41-49` one CLI per
  socket, **"The meta CLI is named component-meta"**; `:76-92` zero-argument
  start, defaults in the executable, Sema at the default location, Configure on
  the meta socket; `:107-110` "The engine inside a Nexus is driven by Kameo
  actors"; `:117-125` **"State is observed by subscription … Polling is
  forbidden; a correct system goes quiet when nothing changes."**
- `Vision/datom.md:66-79` guillemets are the string delimiter; `:87,103`
  **braces are the struct delimiter**; `:274-284` parentheses are reserved for
  Meaning; `:239-241` "Everything moves to Datom: all of the stack, Horizon,
  Lojix, everything; no Dotos file remains."
- `Vision/signal.md:35-38` "The meta signal is never optional."
- The spirit: "Backward compatibility is never a design variable."

### 2.2 What the living has never spoken on

No typed message in the available corpus (Codex from 2026-07-24, Claude from
2026-08-09) uses `WatchDeployments`, `subscribe`, `subscription`, or mentions
free functions or actors in connection with Lojix. The subscription vocabulary
is agent-authored; it is governed only indirectly, by `Vision/nexus.md`'s
"Observation by subscription" and "Polling is forbidden". Likewise no ruling
exists on the deploy action set, on route as a per-deployment choice versus a
Lojix rule, on the Sema table anatomy, or on the shape of a deployment manifest.

---

## 3. The live service — witnessed 2026-09-11

| | |
|---|---|
| unit | `lojix-daemon.service`, system scope, **active (running) since 2026-09-10 13:29:53**, `NRestarts=0` |
| binary | `/nix/store/628yi3nrywgfl425nmdd1f8bi8hhb4kq-lojix-0.21.1/bin/lojix-daemon`, registered 2026-09-09 16:42 |
| ExecStartPre | `lojix-write-configuration 'ConfigurationWriteRequest.{…}'` |
| sockets | `/run/lojix/ordinary.sock` `0660`, `/run/lojix/owner.sock` `0600` — both live |
| store | `/var/lib/lojix/lojix-v5.sema`, **180 KiB, created at daemon start** |
| prior store | `/var/lib/lojix/lojix.sema`, 8.8 MiB, schema **v4**, last written 2026-09-09 16:56 |
| source tree | lojix **2.0.0** at `fab60e5`, pushed to `origin/main` |
| CriomOS pin | lojix `23f09f28` = **1.0.1** |

Read-only queries answered and returned nothing:

```
$ lojix 'Query.ByNode.{goldragon ouranos None}'
Queried.{ [] [] { 1 1 } }
$ lojix 'Query.ByEventLog.{0 5}'
DeploymentEventsQueried.{ [] [] { 1 1 } }
```

The v4 store it no longer reads holds 100 live-set rows, 98 GC roots, 895
event-log rows and 245 deployment records (`lojix-inspect-store` on the retained
path; its `deploy-job` table fails to decode). The cutover to an empty v5 store
was deliberate and documented (`lojix/UPGRADES.md`, "0.21.0 — Durable-store
cutover") and the living authorized the loss (*"I dont care about any past lojix
database"*, *"you can use a new lojix database if its easier"*).

**The consequence is not documented anywhere:** Lojix now believes no generation
is current on any node. Pin labels, retirement, GC-root tracking and rollback
history all start from zero, and `Query.ByNode` cannot tell an operator what is
live. Since 2026-09-10 13:29 the daemon has emitted no log line and used 17 ms
of CPU over 30 hours.

**The living's 2026-08-09 complaint is exactly true again today:** *"how the
fuck does lojix end up running so far behind? something isnt right. this keeps
fucking happening."* The running binary is three minor versions and one major
version behind its own source, and one version behind what CriomOS pins.

---

## 4. What is broken right now — witnessed in the working trees

### 4.1 The next CriomOS deployment cannot start Lojix — decisive

`/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix:27`:

```nix
daemonCommand = "${cfg.package}/bin/lojix-daemon ${cfg.startupArchivePath}";
```

`CriomOS/flake.nix:96` pins `lojix/23f09f28accc…`. At that revision:

- `git ls-tree -r 23f09f28 | grep bin/` returns **nothing**; the root `Cargo.toml`
  declares no `[[bin]]`. The only Nexus binary is `lojix-nexus`
  (`nexus/Cargo.toml:9`), and `packages.default` is a `symlinkJoin` of
  `lojix-nexus`, `lojix`, `lojix-meta`, offline tools and bootstrap. **There is
  no `lojix-daemon` and no `meta-lojix` in the closure.**
- `nexus/src/main.rs:19-21` returns `Error::UnexpectedNexusArguments` if any
  argument is present, and lojix's own flake carries a check named
  `lojix-nexus-startup-rejects-arguments` proving it. The module passes one.
- The Nexus self-configures from Sema (`src/daemon.rs:181-194`); the startup
  archive the module writes is accepted only by `lojix-migrate-configuration`.

Two further landmines behind the first:

- `NexusConfiguration::built_in()` (`src/lib.rs:363-376`) defaults the store to
  `/var/lib/lojix/lojix.sema` — **the retained schema-v4 file**, which the Nexus
  refuses. The v5 store the live service uses is named only in the archive the
  Nexus will not read.
- the default owner socket is `meta.sock`, not `owner.sock`, while the client
  env var is still `LOJIX_OWNER_SOCKET` (`clients/meta/src/lib.rs:11`).

**Why no gate caught it:** `CriomOS/checks/lojix-daemon-config-roundtrip/default.nix`
asserts the `ExecStartPre` string and never touches `ExecStart`; its round-trip
step greps for `'(ConfigurationWritten ['` — the parenthesized form the deployed
binary already replaced with `ConfigurationWritten.{ … }`. Lojix's own VM test
uses `ExecStart = "${package}/bin/lojix-nexus"` with no argument, so lojix is
green while its only consumer is wrong.

### 4.2 The `lojix` skill is false on five counts — decisive

Authored source `/git/github.com/LiGoldragon/Curriculum/skills/lojix.md`, last
changed `8483e20` on 2026-09-03, generated to
`/home/li/primary/.claude/skills/lojix/SKILL.md`. Every agent that deploys reads
this.

| skill says | reality |
|---|---|
| `lojix-daemon` (`:6`, `:285`) | the binary is `lojix-nexus`; `Vision/nexus.md:5` forbids calling it a daemon |
| `meta-lojix` (`:10`, `:189`, `:408`) | the binary is `lojix-meta`; `Vision/nexus.md:49` says "component-meta" |
| "`## Dotos syntax`", "one inline Dotos object", "`dotos-text` feature" | `Vision/datom.md:239` — "no Dotos file remains" |
| products in **parentheses**: `Query.ByNode.(alpha node-1 None)` | witnessed rejected by the deployed binary: `(CliRejected [Datom request did not decode: … Shape(Struct, Meaning)])`. The working form is `Query.ByNode.{goldragon ouranos None}`. `Vision/datom.md:274` reserves parentheses for Meaning |
| "current Dotos curly text" for strings (`:42`) | `Vision/datom.md:66` — guillemets `«»` are the string delimiter; curly is superseded (also found independently by flow 33a4d4) |
| "The daemon accepts schema v4 and refuses earlier schemas" (`:337`) | deployed inspector reports `expected=5`; v4 is refused |
| `Deploy.Host` has 13 fields (`:203-216`) | `meta-signal-lojix/ethos/signal.ethos:30` has **14** — `SecretsInput` after `ProposalSource` |
| `lojix-inspect-store '(InspectStore /tmp/lojix.sema)'` (`:376`) | rejected; the working form is `InspectStore.{<path>}` |

542442 wrote the replacement text and left it unapplied
(`flows/542442/reports/lojix-implementation.md:113-161`).

This is, in my reading, the mechanical answer to *"Lojix has been
problematic"*: the instructions an agent is given produce a rejection on every
documented command, and the agent then improvises.

### 4.3 Failure reasons are collapsed and stderr is discarded — decisive

`lojix/src/schema_runtime.rs:3864-3888` — `fail_pipeline` prints the stage name
to stderr and maps:

```rust
nexus::EffectStage::Eval  => meta::DeployRejectionReason::FlakeReferenceMalformed,
nexus::EffectStage::Build => meta::DeployRejectionReason::FlakeReferenceMalformed,
nexus::EffectStage::CopyClosure => meta::DeployRejectionReason::BuilderUnreachable,
nexus::EffectStage::Activate    => meta::DeployRejectionReason::ActivationFailed,
```

The `EffectFailure` carries the child process's captured stderr; it is never
persisted. Consequences named by six separate flows:

- 5a3ee4 deployments 158 and 162: `BuilderUnreachable` for `No route to host`
  on a stale IP — Prometheus was never unreachable (`flows/5a3ee4/log.md:25`).
- 58a86d deployment 190: `ActivationFailed` for a VSCodium extension hook,
  recovered only by hand (`flows/58a86d/log.md:32`).
- 4a8046: deliberately cancelled builds terminalized as
  `Build/FlakeReferenceMalformed`, "not evidence of malformed source"
  (`log.md:64`).
- 0384e0 212/213, db267d 214/215, 542442's C6 gate — all the same.

Open bead **`primary-cod`** (P1, created 2026-09-05) already carries the design
and acceptance criteria. It has never been worked.

### 4.4 Horizon's projection and CriomOS-home's consumer disagree — high confidence

This is the db267d defect, inverted, and nobody has reported it.

- `horizon-rs/lib/src/model.rs:95-99` — `#[serde(rename_all = "camelCase")] pub
  struct Machine { pub kind: String, pub architecture: String, … }`, populated at
  `lib/src/projection.rs:657, 677`. horizon-rs `main` = `8f4240ef` = the exact
  revision `lojix/Cargo.toml:29` pins.
- `CriomOS-home` `origin/main` (`caffe9a1`, the revision `CriomOS/flake.lock`
  pins) `modules/home/profiles/min/default.nix:240`:
  `++ (optionals (node.machine.arch == "X86_64") [ i7z ]);`

`node` is the projected Horizon node (`horizon` is a module argument; the
`horizon` flake input is a `throw` stub overridden by Lojix at deploy time).
The projection emits `architecture`; the consumer asks for `arch`. Nix has no
`or` here, so this should be `attribute 'arch' missing` at evaluation.

Its two Nix checks hide it: `CriomOS-home/checks/ai-agent-launch-orchestration/default.nix:25`
and `checks/yt-dlp/default.nix:47` hand-write `horizon.node.machine.arch = "X86_64"`
into their fixtures. They are green against a shape the producer no longer emits.

This is the same class as 33a4d4's blocking finding (Horizon no longer projects
CPU vendor, board class, or lid-switch policy) and a plausible contributor to
*"Complete-system BuildOnly did not pass"*. **Unknown:** whether any layer
between Lojix's materialized `horizon` flake and this module renames the key; I
found none, but I did not run an evaluation.

### 4.5 Observation is not observation — decisive, and against distilled Vision

`Vision/nexus.md:117-125`: *"State is observed by subscription: the subscriber
receives the state on open, then each change as it happens. Polling is
forbidden; a correct system goes quiet when nothing changes."*

What the code does (traced by a read-only subflow, quoted from source):

- `src/schema_runtime.rs:2689-2691` binds the watch filter to `_` and discards
  it; `WatchDeployments` and `WatchCacheRetention` are handled identically.
- `open_subscription` (`:2696-2710`) allocates a token from
  `self.subscription_sequence.fetch_add(1, SeqCst) + 1` (`src/lib.rs:2256-2260`)
  and returns one reply. The token is inserted into nothing. `rg
  'next_subscription_token'` has exactly two hits: the definition and this call.
- `close_subscription` (`:2712-2717`) echoes the caller's token back and cannot
  fail, so `SubscriptionTokenUnknown` and `SubscriptionAlreadyClosed` are
  unreachable; `OrdinaryEgress::UnwatchRejected` is never constructed anywhere.
- `serve_ordinary` (`src/daemon.rs:421-445`) reads one body, writes one frame,
  returns; the connection is dropped. There is no loop.
- An exhaustive search for `broadcast`, `mpsc`, `watch::`, `Sender`,
  `subscriber` across the repository returns **zero** hits.

So a `WatchDeployments` peer receives an integer and an EOF. The only way to
follow changes is to re-issue `Query.ByEventLog` — which is the forbidden
polling shape, and which the skill itself instructs (`:222-225`).
`ARCHITECTURE.md:69-70` claims the CLI "streams subscription events". It does
not.

The machinery built to serve these contracts — the `deployment-outbox` and
`pending-transition-intent` tables — has no consumer.

### 4.6 The no-free-functions law is enforced only where it is free

| repo | production free functions (non-`main`) | `checks/no-free-functions.sh` |
|---|---|---|
| `signal-lojix` | 0 | present |
| `meta-signal-lojix` | 0 | present |
| `horizon-rs` | **45** (all but three in `lib/src/projection.rs`) | **absent** |
| `lojix` | **114** (65 of them in `src/bootstrap.rs`) | **absent** |

`canonical_nix_store_root` and `credential_like` each exist three times
(`src/lib.rs:637,681`; `src/adapters.rs:762,780`; `src/schema_runtime.rs:54,73`).
`src/schema_runtime.rs:101-147, 175-235` define 19 zero-sized types whose only
method is `pub fn new(p: P) -> P { p }`, with `#[allow(clippy::new_ret_no_self)]`
at `:94` and `:150` silencing the lint that catches exactly this. horizon-rs has
**three** impl/trait functions in the entire repository.

The nexus skill: *"`fn main()` is the only production free function … A
zero-sized type with behavior is a namespace pretending to be a thing."*

### 4.7 Smaller, certain items

- `schema_runtime.rs:4404` — `ordinary::Selection::ByDeployment(_) => false`.
  `Query.ByDeployment` still returns an empty generation vector. Named by the
  674a4dab audit as a one-line fix; 14 days old.
- `schema_runtime.rs:4493-4500` — `check_key_material` always returns
  `string_vector: Vec::new()`. A stub on the public ordinary contract.
- `/home/li/primary/manifests/` **does not exist**, while
  `NON_MANAGEMENT_AGENTS.md:12` declares it the only source of deployment
  selection. Every deployment is therefore hand-assembled from a 14-field
  request — the exact condition that produced deployment 49 (Zeus's environment
  activated through Ouranos's transport).
- `lojix/Cargo.toml:41,44` — `sema-engine` and `triad-runtime` are
  `branch = "main"` while every other git dependency pins an exact rev.
- `Cargo.lock:659,674` — **two incompatible `kameo` crates**: crates.io `0.20.0`
  for lojix, and `git+…LiGoldragon/kameo.git?rev=f491b45d` for `triad-runtime`.
  Their `Actor`/`ActorRef` types are not interchangeable.
- `lojix/tests/actor_native_runtime.rs` reads `src/daemon.rs` as a string and
  asserts on literals. fe34eb updated two markers to make it pass and wrote
  *"It should be replaced or deleted."*
- 15 production `unreachable!()` sites in `schema_runtime.rs`/`lib.rs`, several
  of which panic the Nexus on a store-write error
  (e.g. `:3903 "could not persist correlated deployment failure: {error}"`).
- 26 stale jj bookmarks in lojix (most from 2026-07-16/17), 7 in signal-lojix,
  4 in meta-signal-lojix, 1 in horizon-rs; four divergent; three
  deleted-on-remote still local. Eight description-less or empty commits sit in
  lojix's own `main` ancestry.
- 542442's three-repository epic is still unmerged on
  `horizon-datom-node-542442`, `horizon-flake-integration-542442` and
  `home-datom-renovation-from-main-542442`, and its lock 851 was still blocking
  flow 162eb3 on 2026-09-11.

---

## 5. Unknowns

1. **Whether §4.4 actually fails an evaluation.** I read both sides but ran no
   `nix eval`. A renaming layer between Lojix's materialized horizon and the
   Home module would disconfirm it.
2. **What is in the live `lojix-v5.sema`.** The daemon holds an exclusive lock;
   I did not stop it. The socket says it is empty.
3. **Why the daemon has logged nothing since 2026-09-10 13:29.** Consistent with
   an empty store and no deployments, but not distinguishable from a regression
   without exercising it.
4. **Whether the 245 orphaned v4 deployment records were meant to be migrated.**
   `UPGRADES.md` documents retaining the v4 file for inspection; nothing says
   whether the live-set was to be re-established, and `Query.ByNode` now answers
   nothing about any node.
5. **Whether `DeploymentInputMode::Direct`, the container-lifecycle mirror, and
   the test-run tables have any producer or consumer** — open since the 674a4dab
   audit's unknowns 2, 3 and 5.
6. **Whether the ~112/114 free-function count is exact.** Two independent counts
   (857335's and mine) agree within two; each named site is cited, the totals are
   approximate.
7. **Whether the living wants the 542442 Deploy.Host redesign at all.** He said
   *"looks reasonable"* and nothing since; the request has grown from 13 fields
   to 14 in the interval.
8. **What the living meant by *"calling it lojix is bad"*** (2026-08-16). He kept
   the name and approved the skill five days later, but never said the naming
   objection was withdrawn.
9. **Whether the CriomOS lojix module or lojix's own flake should own the NixOS
   module.** lojix's flake exposes no `nixosModules`; CriomOS carries it and has
   drifted. No ruling exists.
10. **Whether `checks/lojix-ownership`'s deliberate red (db267d) has been
    cleared.** I did not evaluate it.

---

## Sources

Psyche, verbatim:
`~/.codex/sessions/2026/{07,08,09}/**/rollout-*.jsonl` (lines cited inline);
`~/.claude/projects/-home-li-primary/{5fa00ba7,d076fe3a,fd99506c,0384e018,7dc7cc87,564f55c4,fe34eb91,f6db8d14}*.jsonl`
(lines cited inline);
`vision-raw/{lojixOwnership,setupIndependentInterfaces,mainForEverything}.md`;
`flows/{01a01a93,01a01bac,01a02b46,01a02b4b,01a02fe5,0062e8,542442,fe34eb}/vision/*.md`.

Distilled vision: `Vision/{nexus,signal,datom,orchestrate,highLevelView}.md`;
the `spirit`, `nexus`, `lojix`, `behavior`, `psyche`, `flow-evidence`,
`transcript-search`, `subflow` skills.

Flow logs and reports read in full or in the cited sections:
`flows/674a4dab/reports/{auditLojix,psycheLojix}.md`;
`flows/4d5fc7da/log.md`; `flows/542442/{log.md,reports/lojix-implementation.md}`;
`flows/01a05833/log.md`; `flows/5a3ee4/log.md`; `flows/58a86d/log.md`;
`flows/966be8/log.md`; `flows/0384e0/log.md`;
`flows/db267d/{log.md,reports/overnight-renovation-and-rollback-fork.md}`;
`flows/7dc7cc/log.md`; `flows/857335/{reports/nexus-gap-audit.md,reports/shutdown-runtime.md,witnesses/lojix-horizon-boundary.md}`;
`flows/fe34eb/{log.md,reports/signal-realization.md,vision/datom.md}`;
`flows/33a4d4/log.md`; `flows/162eb3/log.md`;
`flows/f6db8d/reports/{runtime-audit.md,process-audit.md}`;
`flows/01a052bb/log.md`, `flows/01a0539e/log.md`, `flows/4a8046/log.md`,
`flows/6329f1/log.md`, `flows/01a06da9/log.md`, `flows/ea1e56/log.md`,
`flows/4ad49f/log.md`, `flows/cf0ed9/log.md`, `flows/4647d2/log.md`.

Repositories, read without checkout at the revisions named:
`/git/github.com/LiGoldragon/{lojix,horizon-rs,signal-lojix,meta-signal-lojix,CriomOS,CriomOS-home,Curriculum}`.

Live system, read-only: `systemctl`, `systemctl cat`, `journalctl`,
`ls -la /run/lojix /var/lib/lojix`, `strings /run/lojix/startup.rkyv`,
`nix path-info --json`, `lojix-inspect-store 'InspectStore.{…}'`,
`lojix 'Query.ByNode.{goldragon ouranos None}'`,
`lojix 'Query.ByEventLog.{0 5}'`. Beads: `bd show primary-cod`.

Method: three read-only subflows of this thread carried the repository
inventory, the live-service inspection, and the late-flow chronology; their
findings are marked where they are theirs. The early-flow chronology subflow had
not returned when this report was written; §1.1–§1.4 rest on my own reading of
`flows/674a4dab/reports/` and the transcripts, not on it.
