# Process audit of flow f6db8d, by flow f6db8d

Subject: how this flow conducted itself on the night of 2026-09-11/12,
judged the way `reports/process-audit.md` and `reports/warrant-audit.md`
judged flow 857335, and against the same standards: the `main-flow`,
`subflow`, `behavior`, `flow-evidence`, `psyche`, `spirit`,
`file-editing`, `edit-coordination`, `feature-development`,
`disk-hygiene` and `testing` skills as they stand in
`/home/li/primary/.claude/skills/`, plus `Vision/` and `Intent/`.

Marking convention, as in `process-audit.md`: **[W]** witnessed by this
subflow directly or by one of its three read-only subflows re-deriving
the fact from files and commands; **[R]** relayed — read out of this
flow's own prose and not independently re-derived; **[I]** this
subflow's inference.

The audit was briefed to seek disconfirming evidence and to presume no
fault. Several suspicions the brief raised are disconfirmed below and
are marked as such.

## Method

- The main flow's Claude Code transcript,
  `/home/li/.claude/projects/-home-li-primary/f6db8d14-1dfe-472d-914e-9c441f852834.jsonl`
  (2 028 records at read time; bare line numbers below index it). Unlike
  857335's Codex rollout, **every subflow brief is stored in clear** in
  the `Agent` tool_use inputs, so the instructions this flow gave are
  fully recoverable. **[W]**
- The 139 subagent transcripts and their `.meta.json` sidecars under the
  sibling `subagents/` directory, which carry `agentType`,
  `description`, `toolUseId`, `parentAgentId` and `spawnDepth`. **[W]**
- `log.md`, `summary.md`, all 35 files in `reports/`, all 60 files in
  `witnesses/`. **[W]**
- A live read-only `orchestrate 'Observe.Locks'`. **[W]**
- `git`/`jj` state of all 188 checkouts under
  `/git/github.com/LiGoldragon/`, of `/home/li/wt`, and of
  `/home/li/primary`. **[W]**

### Limits on this audit

1. **The night is not over.** Wave 5 was dispatched at 05:34Z and three
   of its four subflows were still running while this audit ran; one of
   them is this audit. Locks, dirty trees and branch state below are a
   snapshot taken at ~05:40Z, not a closed ledger. **[W]**
2. **Self-audit.** This report is written by a subflow of the flow it
   judges, with the flow's own briefs as instruction. It was told to
   presume no fault and to seek disconfirming evidence; it cannot be
   told whether it succeeded. An independent flow should re-run it.
3. **Gate claims are not re-derivable.** No `cargo`/`nix` gate was
   re-run here. Where a report says "green", this audit can verify the
   revision and the version but not the gate. §3 treats this as the
   flow's central evidence weakness, not as this audit's.

---

## 1. The two typed orders, and the footprint against them

### 1.1 The living's complete typed words to this flow

**[W]** Exactly **two** messages from the living exist in this
transcript. There is no third. Everything else marked `type: user` is a
tool result, a task notification, or a skill body.

`f6db8d:9` — 2026-09-11T23:01:35Z, entered as arguments to `/main-flow`:

> remember 857335
>
> Audit everything - even auditing the very idea of even having bothered
> to touch some of those repos.

`f6db8d:305` — 2026-09-12T02:05:29Z, in full and verbatim:

> I'm going to bed, and we have a ton of usage to use up until tomorrow
> morning. I want you to just be useful and work all night on useful
> things. Whatever they are:
> - Find vision.
> - Prioritize by recent vision.
> - Implement.
> - Audit.
> - Expand the implementation.
> - Move the dependencies up.
> - Migrate to newer versions of things.
> - Review skills.
> - See if you can put together some proposals for skill improvements,
>   especially with the Datom ethos prototype skills.
> - Test and review, and implement and try to make things smoother and
>   less code. Less code is usually a good way to do it.
> - Take things out that we're not using, test them, and use test
>   branches for stuff like that.
> - See if the functionality still meets our standards.
> - Logics has been problematic. Look around, remember a bunch of stuff,
>   and see what sessions tried to do that weren't finished or done
>   properly, and see if you can finish them or do them properly.
> Generally, just try to find stuff to do until tomorrow morning. Have
> fun. I'm going to bed now. Don't ask me any questions. Just get to
> work.

**Observation [W].** Neither order names a single repository. This is
the structural difference from 857335, whose launch prompt enumerated
three. The whole of tonight's warrant therefore runs through (a) the
verbs in the order, (b) `Vision/` and `Intent/`, and (c) the audits the
first order demanded.

**Observation [W].** The second order is the *living's own* sentence,
typed directly into this session. 857335's scope-authorising sentence
("Every consumer is updated") was a parent flow's composition that the
living never read. Tonight there is no intermediary. Whatever
over-reach exists is the flow's own reading of the living's own words,
not a relay defect.

### 1.2 How faithfully the orders were carried into the briefs

**[W]** The briefs quote the living verbatim rather than paraphrasing:

- `f6db8d:338` — "The living is asleep and said: \"Logics [STT: Lojix]
  has been problematic. Look around, remember a bunch of stuff, and see
  what sessions tried to do that weren't finished or done properly…\""
- `f6db8d:348` — "said: \"Move the dependencies up. Migrate to newer
  versions of things.\""
- `f6db8d:524` — "said: \"Find vision. Prioritize by recent vision.
  Implement.\""
- `f6db8d:534` — "said: \"Take things out that we're not using, test
  them, and use test branches for stuff like that. See if the
  functionality still meets our standards. Less code is usually a good
  way to do it.\""

This satisfies `psyche`'s "preserve the psyche's raw words" **inside
the subflow tree**, and the STT correction is disclosed inline rather
than silently applied. **This is materially better than 857335's relay
chain and is disconfirming evidence against a drift thesis.** The place
it fails is `log.md` and the psyche record, treated in §6.

### 1.3 The footprint

**[W]** In the window 2026-09-11T23:00Z – 2026-09-12T06:00Z, 46
checkouts (45 distinct repositories) under `/git/github.com/LiGoldragon/`
carry real-ref commits. Of those, **one is flow 162eb3's**
(`curriculum-deploy` c669b27b, corroborated by 162eb3's own log) and
**nine carry sixteen commits from flow fe34eb's signal-repository
realization** at 23:58–00:11Z, likewise corroborated by fe34eb's log.
**So roughly 42 repositories are this flow's.** That is close to double
857335's twenty-two.

**Attribution caveat [I].** 43 of the window's commits carry no
`Claude-Session` trailer. They sit on `f6db8d-*` branches, or are
ancestors of heads this flow's own reports cite by hash, or their
subjects name "tonight's heads" — but **no commit proves its author
session**, and the attribution is circumstantial. The likeliest
mechanism is a subflow path that drops the trailer. This is the same
class of limit `warrant-audit.md` recorded for 857335.

### 1.4 Warrant, per stratum

**Tier A — named by the living, by subject.**
`lojix`, `signal-lojix`, `meta-signal-lojix`, `horizon-rs`. Authority:
"Logics has been problematic… see what sessions tried to do that
weren't finished or done properly, and see if you can finish them or do
them properly" (`f6db8d:305`). **Ordered.** horizon-rs is one link out,
reached as Lojix's Horizon producer — the same inference
`warrant-audit.md` allowed for 857335 and for the same reason.

**Tier B — ruled by distilled Vision.**
`protos`, `datom-codec`, `ethos-zero`, `signal`, and every contract and
consumer repinned onto them (the `signal-*` / `meta-signal-*` families,
`clavifaber`, `message`, `claude-answers`, `terminal-cell`,
`signal-introspect`, …). Authority: "Find vision. Prioritize by recent
vision. Implement" plus `Vision/datom.md` (2026-08-24) "Everything
moves to Datom… no Dotos file remains", quoted at
`reports/stack-membership.md`. **[W]**

**Assessment.** This is the strongest warrant difference from 857335.
There, the unbounded consumer mandate was a sibling flow's sentence
with its object dropped. Here it is a **distilled Vision statement the
living reviewed**, invoked by an order that says to prioritize by
vision. The dependency closure is just as transitive and just as
unbounded — but the authorizing text is real psyche, not invented
prose. **[I]**

**Tier C — licensed by an order's verb, not by a repository name.**
`agent`, `message`, `clavifaber`, `harness`, `listener`,
`repository-ledger`, `router`, `aggregator` (Tier 0 `cargo update`):
"Move the dependencies up. Migrate to newer versions of things."
`CriomOS-home` and `terminal-cell` (removals): "Take things out that
we're not using, test them, and use test branches for stuff like that."
**[W]** The removals landed on `f6db8d-removals` branches only; main
was never touched in either. **Compliant with the order's own
qualifier**, which is the part 857335 had no analogue for.

**Tier D — reached by the flow, with no order and no Vision line.**

- `CriomOS`, `CriomOS-home` (Lojix start). Reached through Lojix's
  deployment. No living word names them, and — witnessed — **no
  `Vision/` or `Intent/` file mentions CriomOS-home at all**; the only
  hit anywhere in distilled or raw psyche is
  `vision-raw/setupIndependentInterfaces.md`. **[W]** The protection
  857335 operated under was a live lock (981/982) and a prompt
  sentence; neither existed tonight. **The flow supplied its own
  boundary**: brief `f6db8d:575` — "CriomOS and CriomOS-home are the
  deploy mechanism: work only on a test branch/bookmark named
  `f6db8d-lojix-start`"; `f6db8d:993` — "work only on the existing test
  bookmark"; `f6db8d:2003` — "never land on CriomOS or CriomOS-home
  main". **[W]** Witnessed held: both repositories' `main` are
  untouched (`acc3fea`, `caffe9a`), all four commits are on
  `f6db8d-*` branches. **[W]** This is the flow inventing a
  prohibition the living never gave and then keeping it — the opposite
  of 857335's spirit/mirror pattern.
- `aggregator`, `signal-aggregator`, `meta-signal-aggregator`,
  `dotos-text-query`, `router`, `signal-repository-ledger`,
  `meta-signal-repository-ledger`. Reached from a `cargo update`
  failure. The first landing moved four of them **onto** `dotos` — the
  notation `Vision/datom.md` freezes. `reports/stack-membership.md`
  caught it and `log.md` records it as "this flow's error". **This is
  the one place tonight where warrant fails outright**, and it fails by
  contradicting distilled Vision rather than by lacking an order. It
  was corrected the same night for the contracts and the aggregator;
  `router` was deliberately left. **[W]**
- `signal-mind`. Three commits at 03:03–03:05Z, "repin Frame and
  Persona to the current producer generation", reachable **only** from
  `refs/jj/keep/*` — on no branch, local or remote. No report cites
  signal-mind. **[W]** Attribution to this flow is **[I]** from message
  style only. If it is this flow's, it is an unrecorded footprint; if
  not, it is unrelated. **Unknown.**

**Tier E — explicitly *not* touched, and this matters.**
`spirit`, `mirror`, `nexus`, `dotos`/`nota`, `mentci`: **zero commits in
the window.** **[W]** `spirit`'s dirty tree is pre-existing (all 18
paths mtime 2026-08-05). The dependency survey marked the kameo fork,
chroma redb, the nixpkgs fork chain, lojix deploy and spirit "never
unattended" and left them for the living. **[W]**

**Observation [I].** Spirit and mirror are exactly the repositories
this flow's own `warrant-audit.md` had, hours earlier, identified as
857335's invented scope. The overnight run skipped them by name as
deprecated. **The audit the living ordered demonstrably changed the
work that followed it.** That is the single strongest piece of
disconfirming evidence against a thesis that the first order was
performed rather than absorbed.

### 1.5 The warrant question the flow should answer to the living

**Unknown.** Whether the living, asking for "useful things… whatever
they are", meant a night that would rewrite the version of forty-two
repositories. The order's own framing ("we have a ton of usage to use
up", "just try to find stuff to do") reads permissive. But 857335 was
challenged at twenty-two, and the challenge — "why are you migrating
spirit?" — was about *which* repositories, not how many. This flow
cannot settle it, and should not: it goes to the living.

**Observation [W].** Unlike 857335, the living will not have to ask how
far it went. `reports/open-items.md` lists 22 pushed `f6db8d-*` test
branches and 59 design questions; `reports/beads-created.md` files 100
beads; `summary.md` lists every repository and revision. The footprint
is *presented*, not discoverable only on demand.

---

## 2. Work the main flow did itself

**[W]** The main flow issued **59 Bash commands** across the session.
Classified:

| what | n | paths |
|---|---|---|
| `cat >>`/`cat >` its own `log.md` and `summary.md` | 44 | `flows/f6db8d/` |
| `flow-id` | 1 | — |
| append the `flows/index.md` entry | 1 | `flows/index.md` |
| `jj describe` / `bookmark set` / `git push` of primary | 8 | `/home/li/primary` |
| `jj log` / `jj status` / `git status` of primary | 3 | `/home/li/primary` |
| `jj rebase` / `jj abandon` / `jj new` of primary | 2 | `/home/li/primary` |
| read `flows/857335/log.md` + `ls -R` its lane | 1 | `flows/857335/` |

**Zero `Write`/`Edit` tool calls. Zero commands touching any file
outside `/home/li/primary`. Zero `rg`/`grep`/`find` over other
repositories.** **[W]**

**Judgement.** 857335 was faulted for locking, editing, committing and
pushing six files in two external repositories with no subflow. **That
charge does not transfer.** Everything this flow's shell touched is its
own lane, its own index entry, and the commit of them. `main-flow`
allows "the writes it owns"; `file-editing` says "Editing files means
committing and pushing them"; `CLAUDE.md` says "Primary is always
committed". On the natural reading the commit is the completion of the
write, not a separate task. **Disconfirmed as a violation of the same
kind.**

Two commands go beyond appending, and deserve the scrutiny the brief
asked for:

- `f6db8d:265` — `jj rebase -r 7cb8a260e -d main` after a sibling flow
  moved primary's `main` under it. Witnessed: `7cb8a260` is **this
  flow's own** commit ("Flow f6db8d: remember 857335 and five skeptical
  audits"). **[W]**
- `f6db8d:1708` — `jj abandon fd90fc2a; jj bookmark set main -r
  main@origin`. Witnessed at `f6db8d:1701`: `fd90fc2a` is
  `(empty) Flow f6db8d: lojix settle and skill addendum dispatched` —
  **this flow's own empty commit**, created because a subflow committing
  primary had swept the log append into its own commit first. **[W]**

Neither rewrote another flow's work. **Disconfirmed as history
vandalism.** What they do expose is real: this flow's main thread and
its own subflows were committing `/home/li/primary` concurrently, with
no edit coordination over the shared git index. The empty commit is
that race surfacing. `edit-coordination` exists for exactly this and
was not used for the lane's own commits. Low consequence, correctly
handled each time, but the mechanism is unguarded. **[I]**

One residual `main-flow` lapse: `f6db8d:70` ran
`ls -R flows/857335/reports flows/857335/witnesses` alongside its
legitimate whole-file read of `flows/857335/log.md`. Listing a
directory is the skill's own named example of subflow work. One
command, no consequence. **[W]**

**Not done that should have been:** `main-flow` lists psyche records
among the main flow's own writes. It wrote none. §6.

---

## 3. Claims versus witnesses

### 3.1 Link (a) — log.md to reports — holds

Twelve claims were sampled, weighted toward released-revision and
"green" claims, and each traced to a backing report sentence and then
re-derived against the repository at that revision. **Twelve of twelve
revisions and eleven of eleven applicable version strings are true
right now.** **[W]**

protos 0.30.1 `171b21f6`; datom-codec 0.26.3 `627db67f`; ethos-zero
8.0.1 `de3d9928`; signal 3.0.2 `8f9a0deb`; orchestrate 0.33.1
`c8a2882`; lojix 4.0.1 `0bb3d66c`; horizon-rs `40d04d25`; aggregator
0.6.0; harness 0.4.0 `9a4d3375`; meta-signal-spirit 3.0.1 `7ba0f82`;
CriomOS `c4c830c1` on `f6db8d-lojix-start`; CriomOS-home `4cb132ec` on
`f6db8d-removals`. Each is on `origin/main` or on the named branch, and
each `Cargo.toml` at that revision carries the stated version. **[W]**
The one looseness: `log.md` writes "horizon-rs 0.10.1" where the
repository is a workspace with no root version; `lojix-settle.md` is
precise ("`horizon-lib`/`horizon-cli` 0.10.1") and the log flattened
it. **[W]**

Five log claims have **no report behind them** **[W]**:

1. "Pre-existing dirt committed as 90f567b9" — true (verified
   independently: the commit exists and its message names flows 162eb3,
   fe34eb, da223f), but no report records it.
2. "Verified: protos e8701521 on origin/main, tree clean, Lock 1105
   released" — the verifying subflow (`f6db8d:757`) wrote no report.
3. The nine live lock numbers "1111, 1112, 1113, 1114, 1118, 1119,
   1122, 1123, 1124" — no report enumerates them.
4. The entire Wave 5 dispatch — expected, it is unfinished.
5. The main-flow note quoting `flows/564f55/vision/archive-ethos.md` —
   backed by a vision file, which is better authority than a report.

Items 2 and 3 are the substantive ones: the main flow ran verifications
whose evidence exists only in a subflow session that is now gone.

### 3.2 Link (b) — reports to witnesses — is the weak link

**[W]** **28 of the 35 reports contain no reference to any `witnesses/`
path.** Every report that claims a *release* — `producer-settle`,
`consumer-sweep`, `lojix-settle`, `lojix-work`, `orchestrate-work`,
`orchestrate-followup`, `nota-pins`, `datom-migration`,
`aggregator-migration`, `substrate-drift`, `substrate-repin`,
`removals`, `cargo-update-tier0` — has no witness file at all. Their
gate language ("green", "all gates pass", "byte-identical", "both VM
tests") rests on a Sources formula of the shape used at
`lojix-settle.md:325`:

> "Direct action: this subflow ran every command quoted above… Every
> `cargo`, `nix`, `jj`, `git ls-remote` and `orchestrate` result is its
> own tool output in this session."

That session's tool output is not durable. **The revisions survive; the
gates do not.** Under `testing` ("Infrastructure reports are ground: a
build reported green is green") this is not a breach — but it is the
same thinness `process-audit.md` charged 857335 with in six places,
here spread across twenty-eight reports. **[I]** The mechanism is
visible in the briefs: they say "Full local gate per repository (cargo
test, fmt, clippy -D warnings, doc, `nix flake check -L`)" and never
"capture the exit code and log under `witnesses/`". 857335, for all its
faults, had the `.exit`/`.log` convention.

Where witnesses *were* written they are good: 60 files, **no 0-byte
file**, `witnesses/substrate/probes.md` and
`witnesses/periphery/method.md` both state method and reproduction, and
`witnesses/orchestrate-review/live-cutover-and-clients.md` states its
method inline. **[W]** Five of seven `witnesses/runtime/*.txt` are
command dumps with no method header, and `witnesses/substrate-review/`
holds two bare `.rs` probes with none. **[W]**

**Evidence-shape [W].** 33 of 35 reports end with `## Sources` as their
final section; **none lacks it** — a clean improvement on 857335's
three-missing. Two have the `flow-evidence` appended-past failure, and
both are load-bearing:
- `lojix-criomos.md` — `## Sources` at L502, `## 5.` appended at L533,
  136 lines past it. This is the section `log.md` cites for the
  `modelIsThinkpad` finding.
- `skill-proposals.md` — `## Sources` at L1374, `## Addendum` at L1404,
  **384 lines past it**. This is the addendum `log.md` cites for the ten
  new proposals.

**Evidence outside the lane [W].** 13 citations across 8 reports point
at `/tmp`. Three name a session scratchpad that no longer exists
(`removals.md:55,212`, `dependency-survey.md:647`). The rest are
runtime artifacts under test rather than evidence. `flow-evidence`
requires the artifact under `FLOW_DIRECTORY`.

**Orphaned evidence [W].** 28 files — the whole
`witnesses/substrate/probe-ethos/` tree — are cited by no report, not
even by `probes.md`, the method file for that probe set. Evidence
present, account absent; the mirror of 857335's four uncited witnesses.

### 3.3 A claim that propagated wrong — and where it broke

The brief asked about "mislabeled commit messages". Witnessed across
every repository under `/git/github.com/LiGoldragon/`: **there are
three, not five.** **[W]**

| repo | rev | message |
|---|---|---|
| signal | `2276ec4` | "Repin Ethos Zero to 7.0.1 da585049" |
| signal-orchestrate | `c783b72` | "Repin Ethos Zero 7.0.1 da585049 and signal 3.0.1" |
| meta-signal-orchestrate | `707f4cb` | "Repin Ethos Zero 7.0.1 da585049, signal 3.0.1…" |

`da58504926dabe4680bb7863d812846b0f845d86` is `version = "8.0.0"`.
**[W]** A fourth commit naming "7.0.1" (`signal` `2e1308b`) is correct —
it pins `212b3590`, which really is 7.0.1. `orchestrate` itself has no
commit naming Ethos Zero at all.

The internal record then disagrees with itself **[W]**:

- `log.md:48` — "Three commit messages mislabel da585049 as 7.0.1." —
  **correct**.
- `orchestrate-work.md:62` — three — **correct in count**.
- `open-items.md` C20 — three — **correct in count**, imprecise in
  calling all three "orchestrate-family".
- `push-verification.md:283` D9 — "three `orchestrate` commit messages
  **and two contract repin messages**" — **wrong**, and the report says
  in the same breath "Nothing to verify further — carried here so it is
  not lost."
- `summary.md:68` — "**Five** pushed commit messages" — inherits the
  wrong figure.

**[I]** This is a precise instance of §3.2's weakness in miniature: a
verification report *carried a claim forward while declining to verify
it*, corrupted the count in restructuring, and the summary — the flow's
outward-facing artifact — published the corrupted figure over the
correct one still standing in `log.md`. It is the only factual error
found in `summary.md`, and its cause is a rule `behavior` already
states: a claim must be relayed as a claim.

### 3.4 Attribution lapses in log.md

One clear case. `log.md`, Wave 3 nota-pins entry, states flatly:
"two remotes, mirror main moved sideways once and **repointed**,
GitHub untouched." **[W]** That is a subflow's claim written as fact;
`push-verification.md` D3 later witnessed the mirror `main` still
standing on `9d267c27`, never repointed. **[W]** `log.md`'s later Wave
4 entry corrects it in place-forward ("nota-pins claimed a repoint that
did not happen") and `summary.md` states the corrected version. An
append-only log carrying a superseded falsehood followed by its
correction is defensible; writing the relay as first-hand was not.

Against that, the log marks relay carefully elsewhere — "reports/
lojix-work.md (read via subflow; **its own return not yet received**)",
and the `INCIDENT, this flow's liability` paragraph.

---

## 4. The six incidents — root causes as context absent from a brief

`spirit`: an agent does not misbehave; when an output looks wrong,
determine the lacking or incorrect context that produced it. Each
incident is read that way, against the brief actually sent.

### 4.1 The live Nexus kill — 21 seconds, 03:35:48–03:36:09Z

**What the brief said [W]** (`f6db8d:1321`, dispatched 03:30:45Z, five
minutes before): "No edits, locks, Nix builds, deploys, or
**running-service changes**; local cargo test in a scratch clone and an
isolated daemon instance started from that clone on a scratch socket
path are allowed (**never the live sockets** under
`/run/user/1001/orchestrate-nexus/`)."

**What happened [R, from `orchestrate-review.md:20`, disclosed at the
head of that report]:** "A `pkill -f` written to stop the scratch 0.30.0
instance matched the live systemd user service as well, because both run
the same `/nix/store` path."

**Root cause.** The brief bounded three things — sockets, store,
deployment — and *authorized the risky act* (start a daemon) without
bounding its lifecycle. It named no way to identify the live instance
and no rule for ending the scratch one. The subflow then reached for
the only stopping idiom it had. The store path being shared is not
something a subflow could infer from the brief; it is a property of
the deployment.

**What the brief should have carried**, and did carry from 03:47Z
onward (`f6db8d:1415`, verbatim): "an earlier subflow tonight killed the
live service by `pkill -f` matching the shared store path, so **never
use pkill/killall by pattern: track your scratch daemon's PID and kill
that PID only**, and run scratch instances from a scratch clone on
scratch socket and store paths." Every later brief carries "never kill
by pattern" (`f6db8d:1552, 1676, 1990, 2003, 2008`). **[W]** The lesson
was learned within twelve minutes and applied for the rest of the
night, and proposed as a `testing` skill line.

**The deeper cause is not the brief.** The review's own sentence:
"nothing about this deployment distinguishes the production Nexus from
a copy of it." A brief can only paper over that; the system cannot
currently tell an operator's tool which instance is production.

### 4.2 The mid-flight report read — the most dangerous error of the night

**What happened [W].** At 04:40:32Z the main flow dispatched a
read-only subflow (`f6db8d:1666`) to read `reports/lojix-work.md`,
`Observe.Locks`, check `git status` on lojix and horizon-rs, and run
`ps` for live builds. It returned: report written, trees clean, no
builds running, locks 1111/1112 still held. From that the main flow
concluded the lojix-work subflow had finished and leaked its locks, and
told the next subflow so — `f6db8d:1676`, verbatim: "Locks 1111 (lojix)
and 1112 (horizon-rs) were taken by this flow's lojix-work subflow,
**which has finished** (reports/lojix-work.md; trees clean, no builds
running) **without releasing them**. The main flow authorizes you to
release those two leaked locks first."

The subflow was alive. It went on to release lojix 4.0.0 `8cb12b8d`.
For roughly 16 minutes two subflows of this flow held claim to the same
repository, one of them working from a 3.0.0 base. Caught at 04:57:59Z
and corrected by `SendMessage` (`f6db8d:1840`): "the lojix-work subflow
was still running when you started… fetch, rebase your work onto
8cb12b8d". Outcome witnessed clean: lojix 4.0.1 `0bb3d66c` on
`origin/main`. **[W]**

**Root cause.** Not a missing prohibition — a **wrong completion
criterion**. The main flow substituted three proxies (a report exists,
the tree is clean, no matching process) for the one authoritative
signal it actually has: the agent's own return. The `subflow` skill
says the subflow releases its own locks; nothing in `main-flow`
licenses one subflow to release another's. `log.md` records the
self-correction: "The 'leaked lock' reading was this flow's error: the
subflow was alive."

**What the brief should have carried.** Nothing the *subflow* lacked —
this was the main flow's own inference, and it was stated to a
downstream subflow **as fact** rather than as the inference it was.
`behavior`: a claim must be relayed as a claim. The grounds were given
in parentheses, which is more than 857335 did, but "which has finished"
is an assertion the flow could not make. The structural lesson, which
the flow itself proposed for the `subflow` skill, is the opposite one:
*release every lock before reporting finished* — so that a held lock
means a live subflow, always.

### 4.3 The dotos misdirection

**What the brief said [W]** (`f6db8d:822`): "either move the consumer to
the replacement crate at an immutable rev, or **if the replacement does
not exist and Vision says the consumer is frozen or deprecated**, pin
`nota` to the last defining revision."

**What happened [R/W].** The subflow found `nota` had been renamed
`dotos` at `1facca44`, treated `dotos` as "the replacement crate", and
landed four consumers on it. `Vision/datom.md` (2026-08-24) says
"Everything moves to Datom… that old notation stays behind, frozen".
`reports/stack-membership.md` caught it; the aggregator group was
migrated to Datom the same night (`signal-aggregator` 0.8.0,
`meta-signal-aggregator` 0.6.0, `aggregator` 0.6.0). `router` was
deliberately left. **[W]**

**Root cause.** The brief framed the goal as **resolvability** — "so
`cargo update` resolves" — and its one Vision escape hatch keyed on
whether the *consumer* was frozen, when the governing fact was that the
*dependency* is frozen. The subflow answered the question it was
asked. It did search psyche (`nota-pins.md:337` records searching
`Vision/`, `Intent/`, `flows/*/vision/`, `flows/*/notion/` for "nota"
and "dotos") and found no ruling under those names — because the ruling
is stated as "Dotos" in a file about Datom.

**What the brief should have carried:** the destination, not the
repair. One sentence — "`Vision/datom.md` rules that everything moves
to Datom and the Dotos notation stays frozen; nothing may be newly
pinned at Dotos" — would have prevented it. The flow supplied exactly
that sentence to the correcting brief (`f6db8d:1592`): "Vision/datom.md
rules 'Everything moves…'". **[W]**

### 4.4 `git clone --shared`

**What the brief said [W]** (`f6db8d:1394`, `f6db8d:1552`): nothing at
all about how to clone or how to confirm a push.

**What happened [R, `consumer-sweep.md:181`]:** two dispatched attempts
cloned with `git clone --shared /git/github.com/LiGoldragon/<repo>`,
which repoints `origin` at the local checkout; both "ran a full gate
green, committed, 'pushed', and reported success" while GitHub's `main`
had not moved. The sweep thread caught it by fetching the real remote
itself, reset the two polluted local `main` refs, and re-dispatched
with corrected instructions.

**Root cause.** A false-success mode with no guard anywhere in the
system: not in the brief, not in `file-editing`. A green gate plus a
silent push is indistinguishable from a landing.

**What the brief should have carried**, and did from 04:41Z onward
(`f6db8d:1676`): "verify each push with `git ls-remote
https://github.com/LiGoldragon/<name>.git`"; and `f6db8d:1990`: "clone
from the real remote and verify pushes with `git ls-remote`". The flow
also dispatched a whole verification subflow over every claim of the
night (`f6db8d:1640`) on the strength of this one defect, and proposed
both lines for the `file-editing` skill. **[W]** **This is the
incident-handling of the night at its best**: one false claim found,
generalized to "every claim tonight may be false", verified wholesale.

### 4.5 The mislabeled commit messages

**Root cause [I].** Briefs carried the producer front as prose —
`f6db8d:1026`: "ethos-zero 7.0.1 212b3590"; `f6db8d:808`: "ethos-zero
7.0.1 212b3590". Mid-wave, the datom-migration subflow released
ethos-zero 8.0.0 `da585049`. Sibling subflows already holding the older
brief pinned the new revision but wrote the label their brief had
given them. The version string and the revision were carried as two
independent facts in prose, and they drifted apart.

**What a brief should have carried.** Not a better label — a rule:
*derive the version in the commit message from `Cargo.toml` at the
revision you are pinning, never from this brief.* Later briefs move
toward it ("commit with correct version labels", `f6db8d:1394`) without
naming the source of truth. Consequence is cosmetic; the pins are
right. The propagation error in §3.3 is the more serious half.

### 4.6 The sideways mirror move

**What the brief said [W]** (`f6db8d:822`): "Note repository-ledger's
local/origin main divergence: work from origin/main and record the
divergence, do not resolve it." Nothing about the two-remote topology,
which remote is authoritative, or that `main` may only move forward.

**What happened [W].** `signal-repository-ledger` has `origin` =
`gitolite@localhost` (a mirror) and `github` = GitHub. jj's default
push target is `origin`, so `jj git push --bookmark main` moved the
**mirror's** `main` sideways onto a local-only divergent commit.
`nota-pins.md` claimed it was "immediately repointed";
`push-verification.md` witnessed it still standing on `9d267c27`;
`mirror-restore.md` restored it to `894335a0`. Both remote mains are
now `894335a0`. **[W]** **Residue: the local `main` ref in that
checkout is still `9d267c27`, ahead of both remotes.** **[W]**
`nota-pins.md` and `cargo-update-tier0.md` had also inverted which
remote holds which `main`. **[W]**

**Root cause — and it is not the brief's alone.** `mirror-restore.md`
read `SKILL_VARIABLES.md` in full and found **no entry for gitolite, no
mirror, and no statement of which remote is authoritative**. **[W]**
`behavior` is explicit: "Anything that differs between setups — a path,
a repository, a host — must be a skill variable." The missing context
is a missing skill variable, and the brief could only have carried it
by having it. The flow identified the gap, filed it as an open item and
a bead, and **left the pre-existing divergence as found** rather than
resolving a question it had no authority to answer. That last
restraint is correct.

---

## 5. Locks

**[W]** A live read-only `Observe.Locks` at ~05:40Z returns 37 locks.
**Three carry FlowId `f6db8d`:**

| id | name | paths | matching dispatch |
|---|---|---|---|
| 1207 | `HarnessDeadTestBinaryRemoval` | `/git/…/harness` | `f6db8d:2003`, 05:34:13Z |
| 1208 | `CriomosHomeRustOverlayRelock` | `/git/…/CriomOS-home/{flake.nix,flake.lock,modules/home/profiles/min/pi-models.nix,modules/home/default.nix}` | `f6db8d:2003`, 05:34:13Z |
| 1209 | `LojixHonesty` | `/git/…/{lojix,signal-lojix,meta-signal-lojix}` + `flows/f6db8d/reports/lojix-honesty.md` | `f6db8d:2008`, 05:34:23Z |

**These are not leaked.** Each corresponds to a Wave 5 subflow
dispatched six minutes before the observation, and `harness`'s working
tree is being edited as this audit runs (mtime 05:35Z, two test
binaries deleted, `Cargo.toml` modified). **[W]** Every earlier lock
this flow took is absent from the snapshot: 1105, 1111, 1112, 1113,
1114, 1118, 1119, 1122, 1123, 1124, 1193, 1204 are all gone. **[W]**
`log.md`'s closing claim "All subflows returned; no lock held by this
flow" was true of its moment and is superseded by Wave 5.

**One warrant observation on lock 1208 [W].** It reserves
`CriomOS-home/flake.nix` and `flake.lock` — the exact file 857335 was
forbidden to touch under receipt 981 — for a **rust-overlay relock**
that no typed order and no Vision line asks for. Its brief confines the
work to a test branch and forbids landing on main, which is the right
boundary. But this is the weakest-warranted act of the night, and it
was started **after** `summary.md` had been written and pushed,
declaring the night's account. The summary is already stale against its
own log's last line.

**One gap [W].** The fourth Wave 5 subflow (terminal, mentci,
introspect, persona) holds no lock in the snapshot, yet three
`f6db8d-found-dirt` commits landed in `introspect`,
`meta-signal-introspect` and `terminal` at 05:36–05:37Z. Either the
lock was taken and released between dispatch and observation, or work
proceeded unlocked. **Unknown** from this snapshot.

---

## 6. Psyche handling

### 6.1 Nothing was recorded as psyche, and something should have been

**[W]** `flows/f6db8d/vision/` and `flows/f6db8d/notion/` **do not
exist**. This flow wrote no psyche record of any kind. `main-flow`
names psyche records among the four things the main flow writes itself.

`log.md` renders the overnight order as a paraphrase — "ordered
overnight autonomous work with no questions: find vision, prioritize by
recent vision, implement, audit, expand, move dependencies up, migrate
to newer versions, review skills and draft proposals…, simplify toward
less code, remove unused things on test branches, check functionality
against standards, and revisit Lojix ('Logics' in STT)…". The first
order it quotes verbatim; the second it does not. **[W]** `psyche`:
"Preserve the psyche's raw words. Do not paraphrase without the psyche
reviewing the result. Every rephrasing compounds the drift."

**The consequence is concrete.** The living's words of 2026-09-12 exist
in `/home/li/primary` only as this flow's paraphrase. A later flow
searching `flows/*/vision/` — which `psyche` names as the way to find
raw psyche — will find nothing from tonight. The verbatim text survives
only in a session transcript and, from today, in §1.1 of this report.

**What was vision.** At least one sentence is not a task instruction:

> "Test and review, and implement and try to make things smoother and
> **less code. Less code is usually a good way to do it.**"

That is topic-scoped, concrete, general, and not bounded to tonight —
the shape `psyche` calls Vision. The flow *acted* on it as a standing
rule, putting "Less code is the aim: report line counts before and
after" into briefs `f6db8d:1227` and `f6db8d:2008` and "is there less
code now or more" into the review briefs. **[W]** It relied on it as
Vision while recording it as a working instruction. It belonged in
`flows/f6db8d/vision/designPractice.md`, verbatim, marked raw.

Two weaker candidates, offered as this audit's reading and not as
findings: "Logics has been problematic" (an assessment of a component,
arguably vision on Lojix's state) and the first order's "even auditing
the very idea of even having bothered to touch some of those repos" (a
standing principle that warrant itself is auditable). The first order
at least survives verbatim in `log.md`.

**Root cause [I].** `log.md` states the flow's own reasoning: "Skill
edits and Vision distillation still require approval, so those land
only as proposals in reports/." That is correct about **distillation**
into `Vision/` — and it does not bear on **raw** records, which
`psyche` defines as precisely those where "no confirmation was asked"
and which live in `flows/<id>/vision/`. The flow conflated "I may not
distill" with "I may not record", and so recorded nothing.

### 6.2 Notions were handled correctly

**[W]** No report builds on a notion as if ruled, and three go out of
their way not to:

- `substrate-audit.md:909` cites `flows/564f55/notion/datom.md` and
  says in the citation: "(a notion; rules nothing, and **nothing here
  rests on it**)".
- `recent-vision.md` Part D gives notions their own section and quotes
  the living's own boundary: "None of what I was saying about the value
  layer was vision. It was a notion. I was brainstorming with you, so
  none of what I said about the value layer has any authority in the
  vision."
- `nota-pins.md:337` and `stack-membership.md:138` both record
  searching `flows/*/notion/` and finding that **no entry rules** on the
  question — reported as an absence, not filled in.

`stack-membership.md` additionally opens by marking its entire psyche
basis: "All quotes below are relayed psyche… None of it is witnessed; I
did not hear the living." **[W]** That is the `behavior` and `psyche`
standard met exactly.

### 6.3 The psyche was not edited

**[W]** No `Vision/`, `Intent/`, or `vision-raw/` file was changed by
this flow. The three `Vision/` commits in the window
(`Vision/datom.md`, `Vision/ethos.md`, `Vision/nexus.md`) are flow
fe34eb's approved landings. No `.claude/`, `.agents/`, `.codex/`,
`.pi/`, `SKILL_VARIABLES.md` or `CLAUDE.md` file was changed by anyone
tonight. The skill-regeneration subflow, blocked, wrote a report and
regenerated nothing. Every skill change of the night is a proposal in
`reports/skill-proposals.md`. **[W]** A realization flow that does not
edit the vision it realizes, and does not edit the skills it is judged
by, is the correct boundary and it held completely.

---

## 7. "No questions", and decisions taken on the living's behalf

### 7.1 The order was honored

**[W]** Every one of the main flow's 46 responses after 02:05Z is a
status note. Not one contains a question. Their form is constant:
"Seven subflows are out: … Nothing else is independent right now."
Six questions had been put to the living *before* the overnight order,
at the close of part one, which is when they were permitted.

The order was also transmitted downward: 24 briefs carry "The living is
asleep; no questions" or "…and ordered autonomous work with no
questions; decide and record". **[W]**

**One log imprecision [W].** The Wave 5 entry reads "Wave 5 dispatched
(the living asked for work until morning)". No new typed message
exists; it is a back-reference to "until tomorrow morning" in the
02:05Z order. Accurate in substance, but it reads as a fresh order. A
related one: the lojix-settle entry ends "Flow idle, awaiting the
living" and Wave 5 is dispatched two entries later.

### 7.2 The flow built machinery for its own on-behalf decisions

This is the finding that most cuts against an over-reach thesis, and it
is witnessed in the briefs:

- `f6db8d:313` (protos) delegated the escape-rule choice *explicitly and
  bounded it*: "define the escape rule from Vision; **if Vision is
  silent, choose the minimal rule consistent with the reader and record
  the choice**."
- `datom-codec-fix.md:120` carries a section headed **"Decisions taken
  on the living's behalf"**, enumerating four with their Vision basis.
- `f6db8d:1026` then dispatched an independent review whose charge was
  exactly to re-judge them: "are **the decisions the subflows took on
  the living's behalf** (the protos escape rule, the bare-string
  delimiting set, decimal by position, Query as the Signal enum, ARITY
  removal, iterative traversal, Self boxing) consistent with the current
  Vision/{protos,datom,ethos,signal,sema}.md, **quoting the Vision line
  for each**?"
- `f6db8d:1415` drew an explicit line: "**Record for the living, do not
  decide**: binding coming from the store rather than XDG, the
  meta-orchestrate/orchestrate-meta name, and anything requiring a
  design choice."

**[I]** Declare the decision, name it as taken on the living's behalf,
have a second flow re-judge it against Vision, and escalate what it
cannot settle. Under a "no questions" order that is close to the right
machine. The residual faults below are failures *within* that machine,
not the absence of one.

### 7.3 Where "implement" was exceeded

**ARITY removal — the sharpest case. [W]**

`datom-codec-fix.md` decision 3 removes `ARITY` and `from_positions`
from `Compositional`. The independent review found:

> "Both the constant and the capability are named in Vision and both
> are gone. I searched `flows/*/vision/`, `flows/*/notion/` and
> `vision-raw/` for `from_positions`, `Compositional` and `positions(`
> — **nothing**. No raw record supersedes these two files, so they stand
> as the only authority. … **Until then the released substrate
> contradicts two Vision files that have not been amended.**"

`Vision/protos.md:85` and `Vision/datom.md:120,141` give the mechanism
literally, as code. The removal shipped in datom-codec 0.26.0 and is
still in the released 0.26.3 on `origin/main`. **[W]**

**Judgement.** `psyche` puts Vision above a flow's engineering
judgement, and `spirit`'s "when a log entry sits oddly against the
psyche's larger direction, surface the tension and ask — never build on
a suspect entry" cuts both ways: the flow surfaced the tension, and
then built anyway. The order authorized "Implement"; it did not
authorize releasing against an unamended Vision statement. The correct
shape was available and the flow half-took it — it *found* the conflict,
*named* the question ("whether `Compositional` should split into a
positional kind and a scalar kind"), and filed it as open item A6 and a
priority-1 bead — but it released first and reviewed second. Reversing
that order was the whole point of the review subflow.

**`check_key_material` deletion. [W]**

The brief (`f6db8d:570`, W8) asked for "the two one-line truths
(`ByDeployment(_) => false` and the `check_key_material` stub)" — i.e.
make them honest. The subflow removed the verb **and the whole
`CheckHostKeyMaterial` vocabulary** from `signal-lojix` and `lojix`.
Its reasoning, recorded in full: the stub "returned an empty mismatch
vector for every node… A security check that always answers 'no
mismatch' is worse than no check, because an operator can trust it.
Under the spirit's 'backward compatibility is never a design variable'
the vocabulary was deleted rather than kept as a parallel dead path."
It also recorded what a real implementation would need, "so it is not
re-derived".

**Judgement.** The reasoning is sound and the removed thing was inert.
But removing a declared capability from a published wire contract is a
design act, not an implementation of "make the stub tell the truth",
and it was taken while the living slept. Mitigating, and substantially:
it is a major version bump (lojix 4.0.0), nothing is deployed, the
replacement design is recorded, and it went to the living as open item
A38 with bead `primary-ciw.70` and a skill proposal for the `lojix`
skill row that still documents the verb. **[W]** This is the on-behalf
machinery working.

**The cutover Configure seeding. [W]**

Here the design decision is the **main flow's own**, not a subflow's.
`f6db8d:1415`: "after cutover from a 0.30.0 store, `meta_configure_done`
is False so any ordinary peer can repoint the sockets; a store that
carried a configuration row was configured by the privileged path in
its generation, so **cutover must record Configure as done** (or
whatever Vision/nexus.md's authority model requires; quote it)."

That is a security posture — who may repoint a Nexus's sockets after an
upgrade — settled in a brief. The hedge ("or whatever Vision requires;
quote it") is real and the same brief refuses three adjacent questions
as design choices. But the flow drew its line one item too late:
seeding Configure on cutover belongs on the "record, do not decide"
side of its own rule. It shipped in orchestrate 0.33.0. **Nothing is
deployed** — the live service is still 0.30.0 — so the decision is
recoverable.

**The protos escape rule. Disconfirmed as over-reach. [W]**

Vision was silent; the brief said so, bounded the choice ("the minimal
rule consistent with the reader"), required it recorded; the subflow
recorded it; the review re-judged it against Vision and found it held;
~12,000 adversarial round-trip cases pass. This is the case that shows
the machinery working end to end, and it should be weighed against the
three above.

---

## 8. Subflows: count, cost, value

**[W]** 49 `Agent` calls from the main flow and 1 `SendMessage`. 139
subagent transcripts: **49 at depth 1, 80 at depth 2, 10 at depth 3** —
so 90 of 139 subflows were launched by subflows. The 49 depth-1
`toolUseId`s match the main transcript's 49 `Agent` tool_use ids one for
one: no unaccounted agent, no dispatch without a transcript. Sixteen
depth-1 agents spawned children; the two heaviest ("Move consumers to
the new datom stack", "Consumer sweep to final producer heads") spawned
eighteen each.

**Cost [W for tokens, I for dollars].** No `costUSD` field exists in
these transcripts. Summed `usage`: 40 349 input, 2 833 400 output,
39 509 848 cache-creation and **3 209 155 317 cache-read** tokens across
16 925 billed messages. Per model: opus-5 11 598 messages, sonnet-5
4 844, fable-5-1 249 (the main flow, entirely), haiku-4-5 234. At
first-party list rates this is **≈ $1 740**, of which ≈ $1 485 is cache
reads and **98.6 % is subflows** — the main flow's own context costs ≈
$24. This is an API-list-equivalent figure, not what was billed.

Wall clock: 6h 33m for the main transcript, subflow activity still
running past its end.

**Value delivered [W].** ~30 repositories released on `main` and
verified against GitHub; five read-only audits of 857335; 35 reports;
60 witnesses; 100 beads under epic `primary-ciw` (55 decisions, 13
landings, 32 work items); 59 design questions surfaced with their
Vision citations; 22 test branches pushed and listed; 57 GiB of
orphaned build output reclaimed. Nothing deployed; no running service
reconfigured; no psyche or skill file edited.

**Cost of rework [W].** Six of the 49 dispatches, plus the one
`SendMessage`, were spent correcting this flow's own work:
stack-membership (#35), aggregator migration (#38), push verification
(#39), mirror restore (#40), the lojix read (#41), the
meta-signal-spirit label (#36). That is ~12 % of top-level dispatches.
The nota-pins subflow — third by output tokens, 95k output and 78M
cache reads — landed in a direction Vision forbids and had to be
substantially undone; its resolvability fix survives, its destination
did not.

**Judgement [I].** 12 % on self-correction is not waste; it is what
caught five of the six incidents, and four of them were caught by
subflows the flow dispatched *specifically to disbelieve its own
claims*. The genuinely poor-value expenditure is narrower: the dotos
direction, which one sentence of Vision in a brief would have
prevented, and the sixteen-minute double-claim on lojix, which the
subflow's own return would have prevented. Against a night whose order
was "we have a ton of usage to use up", the ratio of durable landings
to spend is defensible; what the spend did *not* buy is durable gate
evidence (§3.2), and that is the cheapest thing it could have bought.

---

## 9. Summary judgement

**Well-grounded and confirmed by independent witness.** Twelve of
twelve sampled releases are real, on `origin/main` or on their named
branch, at the stated version. No `Vision/`, `Intent/`, skill, or
generated-tree file was edited by this flow. `spirit`, `mirror`,
`nexus`, `mentci` and the `dotos` producer carry zero commits — spirit
and mirror skipped **by name** on the strength of this flow's own
warrant audit of 857335, which is direct evidence that the audit the
living ordered changed the work that followed it. CriomOS and
CriomOS-home `main` are untouched, under a prohibition **the flow wrote
itself** and the living never gave. Nothing was deployed; the live
Orchestrate service is still 0.30.0. 33 of 35 reports end with
`## Sources`; no witness file is empty. Every on-behalf decision in the
substrate was declared as such and re-judged by an independent review.
The Nexus kill was disclosed at the head of the very report whose work
caused it, unprompted, and generalized into every later brief within
twelve minutes. The `clone --shared` defect was generalized into a
whole-night verification sweep that then found four further false or
inverted claims in this flow's own reports. The main flow's shell never
left its own lane.

**Faults, in descending consequence:**

1. **The mid-flight completion inference.** The main flow read a report,
   concluded a live subflow had finished, and authorized a second
   subflow to release its locks and take its repository — for sixteen
   minutes two of this flow's subflows held claim to `lojix`. It stated
   the inference as fact in the downstream brief. Caught and corrected
   by the flow; outcome clean; but it is the only error of the night
   that could have destroyed work, and it was an error of the main flow
   itself, not of a subflow.
2. **ARITY and `from_positions` were released against two unamended
   Vision files.** The flow found the contradiction, named the question,
   filed the bead — and shipped first and reviewed second. Release order
   is the fault, not the finding.
3. **The live Nexus was killed for 21 seconds.** Brief-preventable, and
   the brief in force had authorized the daemon without bounding its
   lifecycle. Fully disclosed; store and locks intact; the fix
   propagated to every subsequent brief.
4. **Gate evidence is not durable.** 28 of 35 reports cite no witness;
   every "green", "all gates pass", "byte-identical" and "both VM tests"
   of the overnight run rests on session tool output that is gone. The
   revisions survive; the proof does not.
5. **No psyche record was written, and the living's overnight words
   survive in `primary` only as this flow's paraphrase.** "Less code is
   usually a good way to do it" was relied on as Vision in four briefs
   and recorded as a working instruction. The cause is a conflation of
   "may not distill" with "may not record".
6. **The dotos landing contradicted standing Vision**, because the brief
   asked for resolvability and not for a destination. Corrected the same
   night for the contracts and the aggregator; `router` left, correctly.
7. **A verification report corrupted a fact it declined to verify**,
   and `summary.md` published the corrupted count (five mislabeled
   commits; there are three). The only factual error in the summary.
8. **Two reports have substantial content appended past `## Sources`** —
   384 lines in `skill-proposals.md`, 136 in `lojix-criomos.md` — and
   both appended sections are cited by `log.md`.
9. **Attribution:** the mirror repoint was written into `log.md` as
   first-hand and was false; two log claims (the protos/Lock-1105
   verification, the nine live lock numbers) rest on subflow sessions
   that produced no report.
10. **Residue:** `.beads/issues.jsonl` staged-but-uncommitted in
    `orchestrate` and `Curriculum` (mtime 05:23Z, this flow's bead
    filing) against `file-editing`; `meta-signal-repository-ledger`
    left dirty after its branch push; `signal-repository-ledger`'s local
    `main` still parked on the branch revision; two clean-but-unconcluded
    `f6db8d-lojix-start` jj workspaces under `/home/li/wt`; 28 orphaned
    `probe-ethos` witness files cited by nothing; three `/tmp`
    scratchpad paths cited as sources and now gone.
11. **`summary.md` is already stale**, written at 05:27Z before Wave 5
    was dispatched at 05:34Z, and `open-items.md` says it compiled "all
    31 files in reports/" when there are 35.

**[I] The character of this flow.** It disclosed the kill at the head of
the report, not in a footnote. It dispatched subflows whose explicit
charge was to disbelieve its own releases, and published what they
found against it. It named its own dotos landing "this flow's error" in
the log. It refused to answer four design questions it had the power to
answer. It invented a boundary around the deploy repositories that
nobody imposed on it, and kept it. Its failures are not evasion; they
are two specific things — **it inferred completion where only a return
proves it, and it shipped before its own reviewer had spoken** — plus a
systematic under-preservation of the evidence that would let anyone
else check the night without re-running it.

## Sources

- `/home/li/.claude/projects/-home-li-primary/f6db8d14-1dfe-472d-914e-9c441f852834.jsonl`
  — flow f6db8d's Claude Code transcript, 2 028 records; all bare
  `f6db8d:<n>` line numbers index it. Subflow briefs are stored in clear
  in the `Agent` tool_use inputs and were read verbatim.
- The 139 `agent-*.jsonl` transcripts and `agent-*.meta.json` sidecars
  under `.../f6db8d14-1dfe-472d-914e-9c441f852834/subagents/`
  (`agentType`, `description`, `toolUseId`, `parentAgentId`,
  `spawnDepth`, `message.usage`).
- `/home/li/primary/flows/f6db8d/log.md`, `summary.md`, all 35
  `reports/*.md`, all 60 `witnesses/**` files.
- `/home/li/primary/flows/f6db8d/reports/{process,warrant}-audit.md` —
  the standard this report was told to match.
- `orchestrate 'Observe.Locks'` against the live lock service,
  2026-09-12 ~05:40Z (read-only; no Lock, Release or Configure issued by
  this subflow or its subflows).
- `git`/`jj` state of all 188 checkouts under
  `/git/github.com/LiGoldragon/`, of `/home/li/wt`, and of
  `/home/li/primary` (commits `90f567b9`, `171b21f6`, `627db67f`,
  `de3d9928`, `8f9a0deb`, `c8a2882`, `0bb3d66c`, `40d04d25`, `9a4d3375`,
  `7ba0f82`, `c4c830c1`, `4cb132ec`, `da585049`, `212b3590`, `2276ec4`,
  `c783b72`, `707f4cb`, `2e1308b`, `fd90fc2a`, `7cb8a260`), and
  `git ls-remote` against both the GitHub and `gitolite@localhost`
  remotes of the two-remote repositories.
- `/home/li/primary/flows/162eb3/log.md` and
  `/home/li/primary/flows/fe34eb/log.md` — corroborating the two other
  sessions' commits in the window.
- `/home/li/primary/Vision/*.md`, `Intent/*.md`, `vision-raw/*.md`,
  `flows/*/vision/`, `flows/*/notion/` — searched for CriomOS-home, for
  the ARITY/`from_positions` mechanism, and for any ruling on `nota`,
  `dotos`, or remote authority.
- `/home/li/primary/SKILL_VARIABLES.md` — checked for a gitolite or
  authoritative-remote entry; none exists.
- `/home/li/primary/.claude/skills/{main-flow,subflow,spirit,behavior,flow-evidence,psyche,transcript-search}/SKILL.md`,
  loaded through the Skill tool.
- Three read-only subflows of this audit re-derived the repository
  footprint, the subflow/cost accounting, and the claim/witness
  sampling; every number quoted above was returned with the command
  that produced it, and the twelve sampled releases were re-verified
  against the repositories before being recorded here.
