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

### 1.1 2026-07-28/29 — the legacy reports, before flows existed

`/home/li/primary/reports/*-2026-07-2[89].md`, relayed.

The living's framing, dictated 2026-08-08 (`019fe121-…:9`):

> right now everything is a fucking mess. So don't trust anything. Don't assume anything. Be careful where you step.

**What was blocked on a word.** `core-operations-audit-2026-07-28.md:57` found
`lojix-daemon.service` in an auto-restart loop — *"It rejects
/var/lib/lojix/lojix.sema: store schema v1, daemon expects v2. At observation it
had restarted 591 times."* But `recovery-map-2026-07-28.md:78` gated every
repair on item **O4**: *"Resolve the term `Logics` before assigning its repair…
Exact-name evidence is absent."* The identity was confirmed later that day by a
Claude session and finally by the living himself on 2026-09-11 (*"yes it was
lojix"*).

**Finished:** the v1→v2 migration turned out to need **zero mutation** — the fix
was already committed and wired as the first `ExecStartPre`
(`lojix-v1-v2-migration-proposal-2026-07-28.md:11-17,118`); six static gates
passed (`lojix-v1-v2-validation-2026-07-28.md:35-42`); the CriomOS closure built
offline with the correct unit ordering
(`lojix-criomos-closure-validation-2026-07-28.md:5-19,74-84`).

**Left, and still true in kind today** —
`lojix-bird-vscodium-recovery-2026-07-29.md:32,36`:

> The durable conclusion is not that history was recovered: it was not. … Lojix needs durable job provenance, explicit timeout ownership, and a resumable transport protocol. A marker alone should never be treated as proof of completed deployment semantics.

Two things that report started are still open:

- **The 2700-second wall-clock bound was introduced here** (`:98`), as part of
  the bounded-transport repair. The living repudiated it 25 days later:
  *"what timeout? I never approved any timeout."*
- **The Zeus signing/trust boundary** (`:110-114`): Zeus refuses closures
  unsigned by a key it trusts; neither Zeus nor Ouranos has `secret-key-files`;
  Prometheus signs as a name Zeus does not trust. *"A psyche decision is
  required before adding or changing any signing/trust capability."* **Never
  ruled.** It is still the most likely latent cause of CopyClosure failures to
  Zeus.

**`SignalLayerDivergenceAudit-2026-08-08.md`** (opened on the living's words
*"It's kind of been really ad hoc. I feel like all the demons like use a
different approach"*) classified Lojix as its own family (`:38-42`): *"Family D
— lojix hybrid … hybrid concurrency (kameo for jobs, tokio tasks per request)
and an 'owner' socket in place of the standard meta pattern."* Its
recommendation, *"D normalizes its owner socket and concurrency"*, was never
done: today the Nexus's default owner socket is `meta.sock` while the client env
var is still `LOJIX_OWNER_SOCKET`, and the concurrency split is exactly as
described (§4.5).

**What did stick from this period:** the OS-only ownership ruling, enforced by
`CriomOS/checks/lojix-ownership/default.nix`; and the removal of
`ouranos-activate.sh` and `--override-input` flags — the no-flags invariant now
holds in code.

### 1.2 2026-08-22 — flows/01a01bac — the Lojix skill, and a split brain

The living first ruled against a Lojix skill (2026-08-19T22:20), reversed within
13 hours, then approved: *"looks good enough. deploy it"*
(`flows/01a01bac/vision/skillDesigning.md:10,21,31,43`).

**Finished:** the skill landed (Curriculum `bb700c50`, CriomOS `d04f6daf`), with
a real witness — UserEnvironment deployment **27** terminal `Succeeded`,
confirmed by a direct target-profile probe
(`flows/01a01bac/witnesses/userEnvironmentDeployment.md:3-13`).

**Left wrong, and both are still wrong:**

- *"A fresh ordinary `Query.ByDeployment.16` instead fails client decoding…
  **The unknown remains unknown**"* (`reports/lojixRealization.md:78-81`). The
  cause is now known — `schema_runtime.rs:4404` returns `false` — and still
  unfixed.
- **A split brain** (`reports/lojixRealization.md:68-76`): CompleteHost
  deployment **16** — *"Lojix terminal bookkeeping recorded activation failure,
  while the target system profile and `/run/current-system` advanced to the same
  live closure."* The same pattern recurred at deployments 34 and 37 (01a02b46)
  and again at 7dc7cc's pre-deployment check (*"Something advanced the system
  outside Lojix"*). No reconciliation operation exists.

The skill itself has not been touched since 2026-09-03 and is now false on eight
counts (§4.2).

### 1.3 2026-08-22/23 — flows/01a02b46 — the timeout, and Lojix failing to upgrade itself

Three attempts, each instructive.

**(a) Zeus CompleteHost failed at exactly 2699.66 seconds.**
`reports/copyClosureDiagnosis.md:3` measured it against a 2700-second bound, and
`:5` names the deeper defect:

> The word `BuilderUnreachable` is an error-mapping artifact here… it does not persist the captured string. No exact `nix copy` exit code or stderr is retained in the daemon journal or deployment record.

That is the first recorded statement of the defect in §4.3. It is 20 days old.

**(b) The timeout removed.** Provenance search found *"no exact living-psyche
approval for a 2700-second timeout"* anywhere (`reports/lojixEffectTimeout.md`).
**Finished:** lojix **0.18.0** `edbb53aa` removed it from the archive, writer and
effect execution; CriomOS `a4322cd1` followed.
**Left:** *"Whole-CriomOS evaluation and realization are deliberately deferred,
not passed: they require four exact Lojix-materialized inputs"*
(`reports/lojixTimeoutRemovalImplementation.md:54-61`) — the same four-input gate
that still blocks 33a4d4's complete-system BuildOnly today.

**(c) Lojix upgrading itself — the recurring wound.** The first attempt stopped
because *"two unrelated nonterminal CompleteHost `ActivateNow` records, **IDs 5
and 7, both at `Copying`**"* blocked the precondition, and
`reports/ouranosStaleDeployments.md:19-21`:

> **There is no typed deployment cancellation/retirement operation.** `Retire` is a generation GC-root operation and is not a safe way to resolve these records.

Still true in the contract today. The second and third attempts crossed the
system to generations 164 and 165 but Lojix recorded
`Failed.(Activate ActivationFailed)` both times, leaving
*"the live/durable and boot-default projections divergent; no retry or recovery
was submitted."*

### 1.4 2026-08-23/25 — flows/01a02fe5 — deployment 49

The incident that cost the living SSH access to every host, and produced the
only guardrail the system has.

`reports/wrongHomeDeployment.md:5-12`:

> Deployment 49 named `goldragon zeus li` as its logical node and user, while its copy and activation transport was `ssh-ng://li@ouranos` / `li@ouranos`. Lojix keeps logical node and transport independent.

and `:36-38`:

> This request shape had **no invariant** requiring a user-environment activation transporting to Ouranos to also evaluate the Ouranos logical node. The mismatch was consequently valid to the engine and reached successful activation.

**Finished:** recovery (deployment 52); all twelve static `Deployment*` variables
removed; and the minimal rule landed in the authored skill (Curriculum
`8a773baa`), with a behavioral witness — the pre-change skill called the mixed
request ready, the installed skill stopped it.

**Left, explicitly:** `reports/lojixDeploymentTrainingGap.md:50-56` — *"Current
Lojix validates route shape and login authority but **does not validate
logical-node/endpoint identity**… A typed engine guardrail is a separate design
decision."* **That guardrail still does not exist.** The only thing standing
between the system and a repeat of deployment 49 is three sentences of prose in
a skill that is now false on eight other counts.

Note the living's own reading, and a later flow's caution
(`flows/674a4dab/log.md:50-52`): *"way too complex. start with ultra minimal"*
was said of a skill-training text, **not of Lojix itself**.

### 1.5 2026-08-24 — flows/01a030a1, 01a030e8 — two repositories the living approved that do not exist

- **criomos-core.** The living, 2026-08-24T01:17 and 2026-08-25T14:03
  (`flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md:5,11`):
  *"make a proposal on moving the source of it all in a new criomos-core repo"*
  / *"I think core is more accurate than lib, yes, so superseding is the right
  perspective."* The proposal landed
  (`flows/01a030e8/reports/criomosCoreProposal.md`) and named the only strong
  duplication: Horizon service-variant interpretation.
  **Witnessed by me, 2026-09-11: `/git/github.com/LiGoldragon/criomos-core` does
  not exist; `CriomOS-lib` still does.** Open since 2026-08-25.
- **extended-horizon.** The living, 2026-08-23
  (`flows/01a02b4b/vision/homeEquivalence.md:15`): *"whatever in home is
  currently originating in the OS must originate from the horizon or the
  extended-horizon (that could be a standalone repo…)"*, and when an agent
  asserted it existed, *"you mean that repo already existed?"* The flow had to
  retract (`reports/extendedHorizonReacquisition.md:29-33,94`): *"I have not
  verified an existing `extended-horizon` repository, and none has been created
  or authorized here."*
  **Witnessed by me: no such repository exists.** Four questions about its shape
  remain unruled (`:124-131`).

Also from 01a030a1, psyche verbatim
(`flows/01a030a1/vision/commonGround.md:5`, 2026-08-24T00:58):

> to me, this looks like a need to abstract the common ground between OS and home to a separate repo, and using that repo as the source for anything that is shared between them. indirection is bad design

### 1.6 2026-08-28 — flows/01a048a6 and 674a4dab — the audit that named the defects

01a048a6 integrated the AgentIntercom cleanup across five repositories
(horizon-rs `c70915eb`, lojix `33b8b6b7`, CriomOS `45e83fbc`, CriomOS-home
`1274c581`, goldragon `5bc563bf`) and then **could not deploy any of it**
(`log.md:28-31`):

> No authoritative `manifests/*.dotos` selection supplies the required explicit store/SSH transport, builder, selector, and input mode for Ouranos and Zeus. … `Query.ByDeployment` fails at the frame boundary, and `CheckHostKeyMaterial` is a stub returning empty material.

674a4dab then found that block was a **conflation** (`log.md:146-152`):
*"`manifests/*.dotos` in CLAUDE.md is the Curriculum skill-deployment manifest…
**Lojix has no manifest concept**."* Its corrected framing is the real question:
**the per-node 13-field `Deploy.Host` typed request "exists nowhere durable:
each deployment's typed input is composed by an agent in the moment"**
(`criomosStackAudit.md:108`). That is the true ancestor of deployment 49, and it
is still true — with 14 fields now.

Its archaeology is the most useful thing anyone has written about why Lojix is
the way it is (`flows/674a4dab/log.md:88-94`):

> Lojix's whole internal architecture was built by agents in June 2026 **with no surviving psyche transcript**; the +11.5k-line spike (2026-08-04, durable deploy transitions) and the flow/model type split (2026-08-06) were **autonomous agent decisions (sessions with zero psyche messages)**; horizon-rs's 54-field Node and nine species were **authored by the living on 2026-04-23**.

**Finished, and still the best document on Lojix:**
`flows/674a4dab/reports/auditLojix.md` and `criomosStackAudit.md`, with three
questions put to the living and **never answered**
(`criomosStackAudit.md:273-293`): what criomos-core is exactly; where Horizon's
line is; how much Lojix, and where a deployment request lives.

**All of §4.9's items were named here.** Nothing in Lojix or Horizon was changed
by this flow.

### 1.7 2026-08-29 — flows/4d5fc7da — the redesign that was never ruled

Goal (the living, typed): *"remember 674a4dab in depth and bring forward the
lojix redesign"*.

**Finished:** the redesign was carried to the living —
`Deploy.Host.{ NodeName Action Option<Revision> Option<Route> }`, everything
else read from configuration or Horizon; plus a Sema-anatomy cut list and a
`Vision/lojix.md` distillation proposal (`flows/4d5fc7da/log.md:78-89`).

**Left unfinished — this is the largest abandoned thread in the whole history:**

> 2026-08-29 — psyche (typed): "looks reasonable" on the brought-forward redesign, the three asks and the distillation proposal — read as agreement in direction, not as rulings on the action set, the route rule, the Sema anatomy, or approval of Vision/lojix.md; explicit word asked for each.
> — `flows/4d5fc7da/log.md:98-101`

Nothing was ever ruled. **There is still no `Vision/lojix.md` and no
`Vision/horizon.md`** (witnessed). Every subsequent flow therefore worked from
scattered raw records. And the Deploy request went the other way: 542442 added a
fourteenth field rather than cutting to four.

The flow also found the redesign **cannot be written** as drafted. Psyche,
typed, `flows/4d5fc7da/vision/archive-datom.md:9`:

> just remember datom doesnt support omittable fields yet.

So `Deploy.Host.{ Node Action Option<Revision> Option<Route> }` has no textual
form; the flow proposed `Source.[ Main Revision.<rev> ]` instead. **Unruled.**

What it witnessed that day and what is still open (`log.md:35-52, 91-99`):

- lojix origin/main had not moved since the audit; `ByDeployment` and the
  `CheckHostKeyMaterial` stub both still there — **true again today, 13 days
  later**.
- *"Daemon: lojix-daemon.service running lojix-0.19.2 since 2026-08-23 …
  journal shows **worker-thread panics (WireShapeError, src/adapters.rs:539)**
  on 2026-08-28 and 2026-08-29 … **Cause of the panics unknown.**"* Never
  examined. The store those panics ran against is now discarded, so the evidence
  is gone.
- *"Naming inconsistency in distilled Vision: Vision/nexus.md says the meta CLI
  is "component-meta"; Vision/orchestrate.md says "meta-orchestrate"; the
  psyche's Lojix words say "meta-lojix". **Not raised yet.**"* Still not raised;
  and 857335 resolved it unilaterally by shipping `lojix-meta`.
- *"**How Lojix finds a node's LAN route without a temporal IPv4 — unknown.**"*
  This is the living's *"duct tape and haywire"* question of 2026-09-04,
  unanswered on both ends.

The work then stopped on the living's word (`log.md:108-109`): *"we still have
to get ethos-zero fixed, as it was messed up last night by a long codex flow."*
The Lojix redesign was never resumed.

### 1.8 2026-08-30 .. 09-04 — flows/01a052bb, 01a0539e, 01a05833, 5a3ee4, 966be8

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

### 1.9 2026-09-05/06 — flows/0062e8 and 542442 — the Datom renovation

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

### 1.10 2026-09-06 — flows/db267d — the rollback

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

### 1.11 2026-09-10 — flows/857335 — Lojix becomes a Nexus

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

### 1.12 2026-09-11 — flows/fe34eb and 33a4d4

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

### 2.1 On Horizon — verbatim, oldest first

Lojix's only data input. Gathered by flow 674a4dab from Spirit records and the
pre-flow `history.jsonl`; relayed from `flows/674a4dab/reports/psycheHorizon.md`
with its citations.

**2026-05-10**, `history.jsonl:2193` (dictated), `psycheHorizon.md:65-66`
> I don't want any node or cluster-specific data in those repositories. Everything should come from the Horizon.

**2026-05-17**, `history.jsonl:2705`, `psycheHorizon.md:158-159`
> there shouldnt be criome and criome.net in cluster data - those are horizon constants

**2026-05-17**, `history.jsonl:2714`, `psycheHorizon.md:177-181`
> …put the pan-horizon config in a new criomos-horizon-config repo. work all the way until the new lojix and new horizon are able to build all the components of criomos

**2026-05-17**, `history.jsonl:2727` (dictated), `psycheHorizon.md:205-209`
> Horizon should mostly be just the reducer. […] We don't need to put everything into Horizon, especially really dumb stuff […] We're just inflating the Rust code

**2026-05-18**, `history.jsonl:2856`, `psycheHorizon.md:127-129`
> ok, all this "true none true" is fine from some stuff, but it's so lacking in information. I want to see Variants! give me a vector of variants, not this meaningless series of booleans and options! the horizon is so fucking ugly!

**2026-05-18**, `history.jsonl:2859`, `psycheHorizon.md:108-110`
> the cluster data should be a bunch of dials to turn shit on and off, with host name, and stuff like disks and hardware info. all the complicated stuff is in the horizon reduction and criomos

**2026-06-04**, Spirit record `7ggswqdxqqz97za6o7w`, `psycheHorizon.md:16-20`
> Horizon and the cluster-data it carries should be elegant and minimal: express only **what** the psyche (as cluster user) wants the cluster to do, never **how** and never decision-making.

**2026-06-04**, Spirit record `1bok2bxvu3beswif9mv`, `psycheHorizon.md:43-44`
> Horizon is a hack for now, and that's fine. Logix is the more traditional component.

**2026-07-28**, `019fa893:1271`, `psycheHorizon.md:402-406`, answering *"Horizon
currently hard-requires AgentIntercomLocal on every trusted node"*
> then *that* is wrong. I never asked for this, so this implementation is wrong

**2026-08-01**, `019fbf4a:3801`, `psycheHorizon.md:576-577`
> make sure nothing no host names or anything like that is hardwired into lojix

**2026-08-28**, `01a04881:218`, `psycheHorizon.md:422`
> this agentintercomgraphical is slop.

**2026-09-05**, `flows/0062e8/vision/horizon.md:5,13,19` — psyche, STT
> The horizon would get a separate general definition for nodes that all clusters could call on. That would allow them to access these generic hosts for live ISO and maybe even potentially other usage, like cloud deployment images and things like that.

> Well, this CriomOS Horizon settings repo is a perfect place to specify a new generic node setting, which will contain all of our generic node definitions along with their names, and then we'll implement the functionality that these nodes use, gated by node type.

> I think there is such a thing as a node type because some things are just mutually exclusive, like a live ISO node is not an installed node. If anything, the node type should only be this very high-level, mutually exclusive kind of variant separation.

**2026-09-05**, `flows/542442/vision/node.md:5,11` — psyche, STT
> I want it modified a bit so that the node variant, we'll call it that instead of maybe the node species.

> I think generic nodes are better. It's not that they're shared; they're just generic, right? Let's go with that.

**What Horizon owes, still.** The 2026-05-18 complaint — *"a vector of variants,
not this meaningless series of booleans"* — was answered in part: 542442
decomposed `NodeSpecies` into role facets and 0062e8's generic-node design was
implemented (goldragon's flake now composes `horizon-configuration.datom` from
`criomos-horizon-config` at `74a4ad35f7a7`; **witnessed by me** at
`goldragon:flake.nix:12-14,31-37`). Not answered: `psycheHorizon.md` records
nine unresolved points, including the species/services → roles merge *"settled
2026-05-21, still unimplemented"*, and how far Horizon should simplify —
*"the psyche has not drawn the line."*

### 2.2 Distilled vision that governs Lojix but does not name it

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

### 2.3 What the living has never spoken on

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

### 4.2 The `lojix` skill is false on eight counts — decisive

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

### 4.7 Two structural absences the living approved and nobody built

- **`criomos-core` does not exist.** The living approved it on 2026-08-25
  (*"I think core is more accurate than lib, yes, so superseding is the right
  perspective"*), with a landed proposal naming exactly what moves. Witnessed:
  `/git/github.com/LiGoldragon/criomos-core` is absent; `CriomOS-lib` is still
  present. Open 17 days. Its one strong justification — Horizon service-variant
  interpretation duplicated between OS and Home — is the same class of defect as
  §4.4.
- **`extended-horizon` does not exist.** The living asked for it on 2026-08-23
  as the home of everything Home currently inherits from the OS. Witnessed:
  absent. Its shape was never ruled (four open questions at
  `flows/01a030a1/reports/extendedHorizonReacquisition.md:124-131`), and the
  home-equivalence ruling it serves is therefore unrealized.

### 4.8 No way to end a stuck deployment, and no way to reconcile a split brain

Two operations the contract does not have, each of which has already cost a
flow:

- **Cancellation.** `flows/01a02b46/reports/ouranosStaleDeployments.md:19-21`:
  *"**There is no typed deployment cancellation/retirement operation.** `Retire`
  is a generation GC-root operation and is not a safe way to resolve these
  records."* Two deployments (5 and 7) sat nonterminal at `Copying` and blocked
  a self-upgrade precondition. **Witnessed by me: the meta contract at
  `meta-signal-lojix/ethos/signal.ethos:6-12` still has no cancel verb.** The
  stuck rows are gone only because the v5 cutover discarded the store.
- **Reconciliation.** Lojix has recorded `Failed.(Activate ActivationFailed)`
  while the target actually switched, at deployments **16** (01a01bac), **34**
  and **37** (01a02b46); and 7dc7cc found the reverse — *"Something advanced the
  system outside Lojix"* (`flows/7dc7cc/log.md:60-65`). There is no operation to
  re-derive Lojix's live-set from a target's real profile. Today this matters
  more than ever: the v5 store believes nothing is current anywhere (§3).

### 4.9 Smaller, certain items

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
- `goldragon/synchronizer.datomic` still carries the `.datomic` suffix the
  living corrected on 2026-09-05 (*"it's datom, not datomic"*); the composed
  output is named `.datom`.
- The local checkout `/git/github.com/LiGoldragon/criomos-horizon-config` is at
  `e222d3a` and still holds `horizon.dotos`; `origin/main` is at `74a4ad3` and
  holds `horizon-configuration.datom`. Any agent reading the checkout reads a
  retired file. (The same stale-checkout condition 674a4dab found across five
  repositories on 2026-08-28 and warned about: *"wave-1 maps and the first Nix
  audit read stale code."*)

---

## 5. Ranked work items

Ranked by: does it unblock deployment at all; then by how much of the living's
stated frustration it removes; then by whether the vision that grounds it is
distilled or raw. Each names the vision, the repository, the files, and the
witness that would close it.

**W1 — Make CriomOS start the Lojix it pins.** *Nothing else can be deployed
until this is true.*
Vision: `Vision/nexus.md:76-81` ("A Nexus starts with no arguments … it looks
for its Sema database at the default location"); the living, 2026-08-14 — *"the
system has to be redeployed with only the newer Lojix daemon, nothing else."*
Repo: `CriomOS`. Files: `modules/nixos/lojix.nix:26-27,185-207,224-229`
(ExecStart, the `lojix-write-configuration` ExecStartPre, the unit name
`lojix-daemon`, the reset unit), `modules/nixos/lojix-persona-development.nix:41-56`
(`storePath`, `startupArchivePath`), `checks/lojix-daemon-config-roundtrip/default.nix`
(rewrite around `ExecStart`, drop the paren-form grep). Decide where the module
lives: `lojix/flake.nix` exposes no `nixosModules`, which is why it drifted.
Witness: a CriomOS evaluation showing
`systemd.services.<unit>.serviceConfig.ExecStart == "${package}/bin/lojix-nexus"`
with no argument, plus a NixOS VM test that starts it and completes one ordinary
`Query` — lojix already has the second half at
`lojix/flake.nix:255-310`, so borrow it.

**W2 — Correct the `lojix` skill against the shipped binary.** *This is the
mechanical cause of "Lojix has been problematic": every documented command is
rejected.*
Vision: `Vision/datom.md:66-79,87,274-284` (guillemet strings, brace structs,
parentheses reserved for Meaning); `Vision/datom.md:239` ("no Dotos file
remains"); `Vision/nexus.md:5,49` (never "daemon"; the meta CLI is
`component-meta`); the living, 2026-08-20 — *"it must explain the syntax.
dotos/datom is strict"*, and 2026-08-16 — *"it should train agents on how to use
lojix properly."*
Repo: `Curriculum`. File: `skills/lojix.md` (all of §4.2's eight rows), then
regenerate `.agents/`, `.claude/`, `.codex/`, `.pi/`. Start from the replacement
text 542442 already wrote at
`flows/542442/reports/lojix-implementation.md:113-161`; it predates the Nexus
rename, so `lojix-daemon`/`meta-lojix` still need correcting in it.
**Skill edits require the living's explicit approval after proposal** — land it
as a proposal in `flows/f6db8d/reports/`, not as an edit.
Witness: every command form in the proposed text executed against the running
Nexus and its exact reply pasted beside it — the form the skill already uses
("Exact witnessed form").

**W3 — Carry actionable failure evidence into the durable record.**
Vision: the living, 2026-09-04 — *"we might want to modify Logics itself in
order to support this explicitly, because otherwise it feels like we're doing
duct tape and haywire here"*; `Vision/signal.md` — errors are vocabulary.
Open bead **`primary-cod`** (P1) already carries the design and the acceptance
criteria; use them rather than inventing new ones.
Repo: `lojix` (+ `meta-signal-lojix` if the reason enum gains variants).
Files: `src/schema_runtime.rs:3864-3888` (`fail_pipeline` — the stage-to-reason
collapse), the `EffectFailure` type in `src/runtime_flow.rs`, the
`DeploymentRecord`/event-log writers in `src/lib.rs`, and
`meta-signal-lojix/ethos/signal.ethos:36,39,52` if
`DeployRejectionReason` should distinguish eval from build.
Witness: bead `primary-cod`'s own criteria — a failing UserEnvironment
activation whose durable record names the failed command and exit status,
retrievable by `Query.ByDeployment`, with a red-green test and `UPGRADES.md`
explaining partial-failure reconciliation.

**W4 — Repair the Horizon-projection / consumer mismatch, and stop fixtures from
hiding it.**
Vision: the living, 2026-08-23 — *"whatever in home is currently originating in
the OS must originate from the horizon"*; 2026-06-04 — Horizon expresses *"only
**what** … never **how**"*.
Repos: `CriomOS-home`, and `horizon-rs` if the field should be named otherwise.
Files: `CriomOS-home/modules/home/profiles/min/default.nix:240`
(`node.machine.arch` → `node.machine.architecture`);
`CriomOS-home/checks/ai-agent-launch-orchestration/default.nix:25` and
`checks/yt-dlp/default.nix:47` (fixtures must come from the real projection, not
be hand-written); producer at `horizon-rs/lib/src/model.rs:97-105` and
`lib/src/projection.rs:657,677`. Sweep for the same class: 33a4d4 named CPU
vendor, board class and lid-switch policy as fields legacy CriomOS metal code
reads and current Horizon does not project
(`flows/33a4d4/log.md:25`).
Witness: a complete-system BuildOnly that terminalizes
`BootstrapTerminal.Succeeded` — the exact thing 33a4d4 could not produce.

**W5 — Re-establish what Lojix knows about the cluster.**
Vision: the living, 2026-08-13 — *"I dont care about any past lojix database.
how do we get a clean working lojix service running?"* — the history is
disposable, **a working service is not**.
Repo: `lojix`. The v5 store is empty by design, so `Query.ByNode` answers
nothing about any node, and `Pin`/`Retire`/rollback have no ground. Either an
operation that re-derives the live-set from a target's real system profile, or
an accepted first deployment per node that re-seeds it. This is the same gap as
§4.8's reconciliation.
Witness: `lojix 'Query.ByNode.{goldragon ouranos None}'` returning a generation
whose store path equals `readlink -f /run/current-system` on that node.

**W6 — Give the deploy request a durable home, or a typed guardrail.**
Vision: the living, 2026-08-24 — *"why did it deploy zeus on ouranos? We need
better skill training"* and *"those variables are confusing"*;
674a4dab's corrected framing — the 14-field request *"exists nowhere durable:
each deployment's typed input is composed by an agent in the moment."*
Repo: `lojix` (+ wherever the authored request lives — the living has not said,
and `manifests/*.dotos` was a conflation). Files:
`NON_MANAGEMENT_AGENTS.md:12` is currently false and must change either way;
`lojix/src/schema_runtime.rs` submit path for the guardrail
`flows/01a02fe5/reports/lojixDeploymentTrainingGap.md:50-56` explicitly deferred.
**Blocked on the living**: 674a4dab's question 3 and 4d5fc7da's three asks were
never answered, and the four-field redesign cannot be written until Datom has
omittable fields. Minimum unblocked step: the typed engine guardrail rejecting a
request whose logical node and activation destination disagree — that needs no
ruling, only the decision to enforce in code what the skill enforces in prose.
Witness: a red-green test submitting deployment 49's exact shape and getting a
typed rejection.

**W7 — Make observation an observation, or remove the contract.**
Vision: `Vision/nexus.md:117-125` — *"State is observed by subscription … Polling
is forbidden; a correct system goes quiet when nothing changes."* Distilled, and
Lojix violates it while advertising conformance.
Repo: `lojix`, `signal-lojix`. Files: `src/schema_runtime.rs:2689-2717`
(`open_subscription`, `close_subscription`), `src/daemon.rs:421-445`
(`serve_ordinary`'s one-shot transport), `src/lib.rs:2256-2260` (the counter),
`signal-lojix/ethos/signal.ethos:8,11,18,84`, `ARCHITECTURE.md:69-70` (a false
claim). The `deployment-outbox` and `pending-transition-intent` tables exist to
serve this and have no consumer either way.
**Note the honest option:** the living has never asked for `WatchDeployments`
(§2.3). Under the spirit's "backward compatibility is never a design variable",
deleting the whole subscription vocabulary and its two tables is as faithful as
implementing it — and is the *"less code"* the living asked for. Put both to
him; do not choose silently.
Witness: either a test where a watcher receives state on open and one event per
change without re-querying; or the contract, the tables and the outbox gone and
every gate still green.

**W8 — Two one-line truths.** `src/schema_runtime.rs:4404`
(`ByDeployment(_) => false`) makes a documented query always return nothing;
`src/schema_runtime.rs:4493-4500` (`check_key_material`) is a stub on the public
ordinary contract. Named by the 674a4dab audit on 2026-08-28 as a one-line fix
and a remove-or-implement. Repo: `lojix` (+ `signal-lojix` if
`CheckHostKeyMaterial` is removed). Witness: a test that deploys, then
`Query.ByDeployment` returns that deployment's generation; and either a real
host-key report or the verb absent from the contract.

**W9 — Enforce the laws where they are not enforced.**
Vision: the nexus skill — *"`fn main()` is the only production free function"*,
*"A zero-sized type with behavior is a namespace pretending to be a thing"*;
the living, 2026-09-12 — *"try to make things smoother and less code."*
Repos: `lojix` (114 violations), `horizon-rs` (45). Files: copy
`signal-lojix/checks/no-free-functions.sh` and `checks/no-inherent-methods.sh`
into both flakes, then work the list down —
`src/bootstrap.rs` (65 sites) and `horizon-rs/lib/src/projection.rs` (45) are
the whole job; the 19 identity-shim ZSTs at `src/schema_runtime.rs:101-147,175-235`
and the triplicated `canonical_nix_store_root`/`credential_like` are the clearest
missing types. Do it on a test branch, as the living asked.
Witness: the two checks green in both flakes.

**W10 — Housekeeping with real consequences.** Pin `sema-engine` and
`triad-runtime` by rev like every other dependency (`lojix/Cargo.toml:41,44`);
resolve the two incompatible `kameo` crates (`Cargo.lock:659,674`); delete or
rewrite `lojix/tests/actor_native_runtime.rs`, which greps source text and which
fe34eb already said *"should be replaced or deleted"* — the living forbade
source-searching tests (`flows/01a01bac/vision/testTravesties.md:9`); prune the
26 stale lojix bookmarks and the 542442 branches once their fate is ruled;
refresh the stale `criomos-horizon-config` checkout. Witness: `cargo tree`
showing one kameo; the forbidden test gone; `jj bookmark list` matching the
work actually in flight.

**W11 — Ask the living the questions that have been waiting.** Not work on
Lojix, but the gate on W6 and W7 and on `criomos-core`/`extended-horizon`
(§4.7). The unanswered set: 674a4dab's three questions
(`criomosStackAudit.md:273-293`); 4d5fc7da's three asks (action set, route as
rule or choice, Sema anatomy); whether `Vision/lojix.md` and `Vision/horizon.md`
should be distilled at all — Lojix is the most-discussed component in the corpus
and has no distilled vision; and the Zeus signing/trust boundary open since
2026-07-29. He said *"Don't ask me any questions"* tonight, so these are a
morning list, not a blocker on W1–W5 and W8–W10.

---

## 6. Unknowns

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
11. **The cause of the 2026-08-28/29 `WireShapeError` worker-thread panics**
    (`src/adapters.rs:539`) on the then-running 0.19.2. Never examined; the
    store they ran against has since been discarded, so the evidence is gone.
12. **Whether the Zeus signing/trust boundary still blocks anything.** Open and
    unruled since 2026-07-29; several later CopyClosure failures to Zeus were
    attributed to routing instead, and no flow re-tested the signature gate.
13. **What should happen to the three 542442 branches.** The living ruled the
    epic goes on a branch and `main` rolls back; he did not say whether the
    branches are to be merged later, re-derived, or abandoned. Part of the
    renovation has since reached `main` by other routes (horizon-rs now emits
    the new schema), so the branches are no longer a coherent unit.

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

Also read at origin: `/git/github.com/LiGoldragon/{goldragon,criomos-horizon-config}`
(`flake.nix`, tree listings), `/home/li/primary/reports/*-2026-07-2[89].md`,
`reports/SignalLayerDivergenceAudit-2026-08-08.md`,
`flows/{01a01bac,01a02b46,01a02fe5,01a030a1,01a030e8,01a048a6,01a04a30,01a02f74}/`
logs, reports, witnesses and vision.

Method: four read-only subflows of this thread carried the four-repository
inventory (including the `WatchDeployments` and Kameo traces and the
free-function counts), the live-service inspection, the late-flow chronology
(2026-08-30 → 09-11) and the early-flow chronology (2026-07-28 → 08-29). Their
findings are relayed where they are theirs; §4.1, §4.2, §4.4, §4.7, §4.8 and
every re-check of an older audit's finding against today's working tree are my
own reading.
