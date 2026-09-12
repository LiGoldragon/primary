# Recent vision, against the code — a ranked backlog

Flow f6db8d, read-only subflow. Brief: read every Vision, Intent, flow
`vision/` and flow `notion/` entry dated 2026-09-05 or later, judge each
against the code it concerns, and rank what is unrealized.

Scope read: 124 dated lines across `Vision/`, `Intent/`, `vision-raw/`,
`flows/*/vision/`, `flows/*/notion/`. `Intent/` has no entry dated
2026-09-05 or later. `vision-raw/` has no entry of its own in the window —
its only hits are landing banners written by flow fe34eb on 2026-09-10.

### A gap in the method, found late and corrected

**A date sweep does not find all recent vision.** Witnessed by this flow:
of 472 files under `flows/*/vision/` and `flows/*/notion/`, **186 carry no
`## 2026-…` date heading at all** — they head their entries with the subject
instead. A grep for the date window silently skips every one of them.

Twenty-two such files were committed on or after 2026-09-05. Reaching them
by `git log --diff-filter=A` instead of by heading recovered them, and one
of them **overturned a finding this report had already written** — see item
13, where a record with no date heading supersedes a dated one and makes the
"defect" this flow had identified into correct code.

Part E lists the undated recent vision. The dates there are first-commit
dates, which is weaker ground than a heading: a commit date bounds when a
record was written, not when the psyche spoke. Where this matters below it
says so. This is the same problem the psyche named at
`/home/li/primary/flows/8e9e77/vision/flow-retrieval.md:5` — establishing
how old something is — reached from the other side.

**Provenance.** Every psyche quote below is **relayed**: this flow read the
file, but the utterance was heard and recorded by another flow (fe34eb,
162eb3, 564f55, e996e8, 58a86d, 8e9e77, 1a6ca4, 542442). Every code claim
is marked **witnessed** (this flow or a named subflow of it read the cited
line or ran the cited command) or **relayed** (carried from an earlier
report). Where a judgement is this flow's inference rather than an
observation, it says so.

**Tonight's releases, as given in the brief and confirmed here:**
ethos-zero 7.0.0 at `c8a68369` (witnessed: clean tree, `Cargo.toml:3`);
datom-codec 0.26.0 at `196d0e29` (witnessed: clean tree, `Cargo.toml:3`);
protos 0.30.0 **not released** — see item 1.

---

## Part A — the ranked backlog

Ranked by the date of the newest vision statement each item answers, then
by how much of it is unrealized.

### 1. Land the protos writer fix — it exists only in a dirty detached worktree

**Vision (2026-09-09, relayed)**, `/home/li/primary/flows/564f55/vision/archive-datom.md:111`:

> the escape is a backslash

**Realization: partially realized; the completing change is uncommitted.**

Witnessed by this flow: `/git/github.com/LiGoldragon/protos` is at
`b543678cfc8609529cea7174eb4af8a64daa54ad` on a **detached HEAD** with ten
modified/added files (`Cargo.toml` now reads `version = "0.30.0"`,
`src/core.rs`, new `src/traversing.rs`, four test files). Nothing is
committed. `/home/li/primary/flows/f6db8d/reports/protos-fix.md` records
"After: **0.30.0** at `REVISION_PENDING`" and `GATE_OUTPUT_PENDING`.

Witnessed: Orchestrate Lock **1105 `ProtosStringRoundTrip`**, held by
f6db8d over the whole repository, is still open (`orchestrate
'Observe.Locks'`, run by this flow).

The defect the fix closes, witnessed by the datom-codec subflow: the
guillemet writer escapes only `»` and never a literal `\`, while the reader
treats `\` as an escape — so `a\»b` does not round-trip
(`/git/github.com/LiGoldragon/protos/src/core.rs:537-543` against
`:259-270`). 9.2 % of built guillemet strings failed to read back, and the
failure reached real data through `Datomizable for String`.

**Repository and files:** `/git/github.com/LiGoldragon/protos` —
`Cargo.toml`, `Cargo.lock`, `README.md`, `src/core.rs`, `src/lib.rs`,
`src/traversing.rs`, `tests/{deep,delineation,scale,textualization}.rs`.

**What realizing it takes:** run the gate (`nix flake check -L --option
builders ''`), commit, push to `main`, fill in the two `PENDING` markers in
`protos-fix.md`, release Lock 1105.

**Safe unattended tonight: NO — not by another flow.** Lock 1105 is held.
The work belongs to the sibling subflow that holds it; a second writer
would collide, and a `git checkout` in that repository would destroy the
change. If that subflow has died, the main flow should confirm it before
anyone touches the tree. This is the single highest-value action in the
backlog and also the most easily lost.

---

### 2. Everything moves to the new datom — no consumer has moved

**Vision (2026-09-12, relayed)**, `/home/li/primary/flows/fe34eb/vision/datom.md:11-15`:

> ## 2026-09-12 — "logics" was Lojix: everything moves to the new datom, the stack, Horizon, Lojix, everything
>
> yes it was lojix.

confirming `/home/li/primary/flows/542442/vision/archive-datom.md:10`:

> We're going to migrate the datom codec to the latest version that just was implemented now, so take a look at that too. All of the stack, the horizon, logics, everything is going to move to the new datom, and we're going to start migrating everything that uses datom, which means everything, to the new datom as we go along.

Distilled at `/home/li/primary/Vision/datom.md:238-241`:

> Everything moves to Datom: all of the stack, Horizon, Lojix, everything; no Dotos file remains.

**Realization: unrealized.** This is the newest vision statement in the
whole window and nothing in the estate satisfies it.

Witnessed by this flow (`grep` over `Cargo.toml` under
`/git/github.com/LiGoldragon/`): datom-codec 0.26.0 is `196d0e29`, and
every consumer pins an older revision.

| repository | file:line | pinned datom-codec | = version |
|---|---|---|---|
| lojix | `lojix/Cargo.toml:30` | `99a9e8c9` | 0.25.7 |
| horizon-rs | `horizon-rs/Cargo.toml:14` | `99a9e8c9` | 0.25.7 |
| signal-lojix | `signal-lojix/Cargo.toml:15` | `99a9e8c9` | 0.25.7 |
| meta-signal-lojix | `meta-signal-lojix/Cargo.toml:15` | `99a9e8c9` | 0.25.7 |
| orchestrate | `orchestrate/Cargo.toml:18` | `f2cc0685` | 0.25.6 |
| signal | `signal/Cargo.toml:23` | `f2cc0685` | 0.25.6 |

0.25.7 is the revision the datom-codec fix **reverted** as contradicting
`Vision/datom.md` (relayed:
`/home/li/primary/flows/f6db8d/reports/datom-codec-fix.md`, "The bare
string — Vision rules, 0.25.7 is reversed"). So four of the six consumers
are pinned to a revision the flow has since judged wrong against Vision.

Witnessed: **29 `.dotos` files remain** under
`/git/github.com/LiGoldragon/` outside `target/`, against "no Dotos file
remains" — including `criomos-horizon-config/horizon.dotos`,
`CriomOS-test-cluster/clusters/fieldlab.dotos`,
`signal-sema/magnitude.schema.dotos`, `message/.message/agents.dotos`, and
sixteen `examples/canonical.dotos` under the `signal-*`/`meta-signal-*`
crates. Four repositories are still named for it: `dotos`, `dotos-config`,
`dotos-text-query`, `tree-sitter-dotos`.

**What realizing it takes:** ordered, because the wire text changed twice.
(a) Land protos 0.30.0 (item 1). (b) Repin datom-codec's protos rev and
release. (c) Repin the six consumers above to the new datom-codec and the
new protos together, rebuild each. (d) Separately, convert or retire the 29
`.dotos` files. Each repin is a **breaking** change: 0.26.0 changed the
canonical wire text, so every repin is a minor bump in its consumer and any
stored datom text must be re-read.

**Safe unattended tonight: PARTIALLY.** (a)–(c) for `signal`,
`signal-lojix`, `meta-signal-lojix`, `horizon-rs` and `lojix` are ordinary
library repins with Nix gates and no running service — safe once item 1
lands, and **not before**. `orchestrate` is **not safe**: a live Orchestrate
service is running (this flow queried its socket; flow 857335 recorded PID
2323 untouched and a deployment held behind receipt 981), so an orchestrate
repin edges toward a running-service change and should wait for the living.
`criomos-horizon-config` and `CriomOS-test-cluster` `.dotos` files are
deploy-adjacent and excluded tonight.

---

### 3. The `main-flow` skill must not be loadable by an agent

**Vision (2026-09-12, relayed)**, `/home/li/primary/flows/162eb3/vision/subflows.md:35-39`:

> ## 2026-09-12 — The main-flow skill is only ever typed into the prompt
>
> Well, there's one problem: the main flow should not be available for agents to load by themselves, so that it can only be typed into the prompt. Make sure that that's the case and that the way it's done works for both harnesses. If that's the case, then telling the subflow that something is like the main flow is useless.

**Realization: unrealized on Claude, realized on Codex — and the fix is
already written and pinned. The deployed tree is stale by one regeneration.**

Witnessed directly by this flow, and unusually strong evidence: **this
agent's own available-skills listing contains `main-flow`**, described as
"A user starts the main flow that coordinates subflows and owns their
shared flow lane." A subflow can therefore call it right now. `design` and
`realization`, the other two `user-only` skills, are listed too.

Why: witnessed at `/home/li/primary/.claude/skills/main-flow/SKILL.md:3`,
the deployed frontmatter key is `user-only: true`. **Claude Code does not
recognize that key** — its key is `disable-model-invocation: true`, which
`/home/li/primary/.claude/skills/skill-designing/SKILL.md:53` itself names.
Witnessed: `grep -rn 'disable-model-invocation'` across `.claude`,
`.agents`, `.codex`, `.pi` returns only that one line of prose, never a
frontmatter key.

Codex is fine. Witnessed:
`/home/li/primary/.agents/skills/main-flow/agents/openai.yaml` carries
`policy: allow_implicit_invocation: false`, and only the three `user-only`
skills carry such a manifest.

**And the correction already exists.** Witnessed by this flow:
`/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:247-248` reads

```rust
if self == Self::Claude && directive == "user-only: true" {
    rendered.push_str("disable-model-invocation: true\n");
```

landed in commit `c669b27` (2026-09-11, "Emit disable-model-invocation for
the Claude target instead of user-only"), which is that repository's HEAD —
**and `/home/li/primary/flake.nix:22` already pins exactly
`c669b27b464f652edd1c1f812e6b7fd20b941ab7`.** But `.claude/skills` was last
regenerated on 2026-09-10, one day before. So the authored source needs no
change, the generator needs no change, and the deployed tree is simply
behind.

Witnessed, and this is what makes it safe: `/home/li/primary/flake.nix:26`
pins Curriculum at `a7d2f4f1fc57c2376ae041288d05b55ab7577052`, which equals
the local Curriculum HEAD (`a7d2f4f`). Regenerating therefore applies **only
the generator's frontmatter change** — no unapproved skill content can ride
along.

**What realizing it takes:** `nix run .#check-skills` to see the difference,
then `nix run .#generate-skills` (both defined at
`/home/li/primary/flake.nix:49-81`), then commit the regenerated
`.claude/skills`.

**Covered by `skill-proposals.md`: no, and §1c states the opposite.** That
section concludes "The condition holds" from the *authored* frontmatter plus
`skill-designing`'s description of what it deploys to; it did not check the
deployed tree. The psyche asked specifically to "make sure that that's the
case", and on Claude it is not.

**Safe unattended tonight: YES, with one caveat.** It edits no skill body —
the living's approval reservation is on skill *content*, and this changes
none. It is a regeneration that brings the tree level with an already-pinned
generator. The caveat: it makes `main-flow`, `design` and `realization`
disappear from every Claude flow's skill list, so any flow mid-session that
expected to load one would find it gone. Run `check-skills` first and read
the diff.

**One thing still unknown:** whether Codex's
`allow_implicit_invocation: false` also blocks an agent from *explicitly*
naming `$main-flow`, or only blocks description-matched auto-invocation.
The psyche asked that it "works for both harnesses"; that half is
unanswered.

---

### 4. Cross-harness subflow launching — three rulings, none in a skill

**Vision (2026-09-12 and 2026-09-10, relayed)**,
`/home/li/primary/flows/162eb3/vision/subflows.md`:

Line 15 — > 1. yes, its still a subflow

Line 23 — > 2. no sandbox. all permissions. codex with "--sandbox danger-full-access --ask-for-approval=never" and claude with "--dangerously-skip-permissions" - but some of our wrappers might already add those flags. double check the status on that

Line 31 — > 3. Well, if harness is launched as a main flow, the only way it would start using subflows is if it's loaded with the main flow skill. ... Maybe we should also add into the main flow edit that you're suggesting that, when a different harness is invoked, it shouldn't be invoked with the main flow training, but with the subflow training rather, right?

Line 7 (2026-09-10) — > Okay, we need better training on how to launch subflows. Codex doesn't need another Codex to run ChatGPT models, and vice versa.

**Realization: unrealized in the skills.** The psyche's own factual question
("double check the status on that") is **answered** — relayed from
`/home/li/primary/flows/f6db8d/log.md`, wave 1: "witnessed that neither the
claude nor codex Nix wrapper passes a permission flag, codex config already
sets danger-full-access and approval never, so `--dangerously-skip-permissions`
must be explicit."

**Covered by `skill-proposals.md`: yes** — §1 "`main-flow` — how a subflow is
launched, and what a cross-harness launch carries", with proposed
replacement text at §1a (line 7) and §1b (lines 25-27), and §1c naming what
is deliberately not proposed.

**Safe unattended tonight: NO.** Skill edit; proposal already written.

---

### 5. A report wakes the flow only on Send to Claude

**Vision (2026-09-12, relayed)**, `/home/li/primary/flows/fe34eb/vision/reports.md:7-10`:

> You shouldn't have been notified every time I post a comment. There are only two ways of posting a comment: 1. Just put the comment 2. Send to Claude. You should only get triggered when I click Send to Claude. ... I didn't want you to respond every time I commented. I wanted to make all my comments and then tell you I commented with another sort of overall thing I wanted to say

**Realization: unrealized in the skills.** Witnessed: no skill under
`/home/li/primary/.claude/skills/` mentions comments or Send to Claude
(`grep` over `flow-evidence` and `main-flow` returns nothing).

This flow's inference, flagged as inference: part of this is a harness
setting rather than a skill — the artifact tooling arms comment auto-replies
on publish, and the behaviour the psyche objected to (a reply per comment,
plus an automatic acknowledgement on each thread) comes from that arming,
not from any instruction a flow follows.

**Covered by `skill-proposals.md`: yes** — §2 "`psyche-interraction` — a
comment does not wake the flow; Send to Claude does", proposing replacement
text for `skills/psyche-interraction.md` line 85.

**Safe unattended tonight: NO.** Skill edit plus a harness-configuration
question for the living.

---

### 6. `nexus` is the library that defines the core of a Nexus component

**Vision (2026-09-10, relayed)**, `/home/li/primary/flows/fe34eb/vision/nexus.md:7-11`:

> a nexus is a daemon. every component we will build will be a nexus. so the nexus repo is the library that defines the core of a nexus component, which is a daemon
>
> > "Nexus is the universal library for all nexuses; the daemon lives in Ethos Zero.
>
> this is wrong

Distilled at `/home/li/primary/Vision/nexus.md:13-14`.

**Realization: partially realized.** Witnessed:
`/git/github.com/LiGoldragon/nexus` is a real crate — clean tree, HEAD
`a84bfa9` (2026-09-10), two commits ever — but its entire source is
`src/lib.rs` (10 lines) and `src/configuration.rs` (121 lines, of which
78-121 are tests), holding `ConfigurationState`,
`ConfigurationTransitionError` and the `Configurable` trait. That realizes
exactly one paragraph of Vision (`Vision/nexus.md:83-92`, "First
configuration"). Nothing in it is a daemon: no socket, no listener, no
lifecycle. `/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md:4-5` says so:
"Transport, listener, actor, and runner mechanics remain in runtime
libraries."

Witnessed: the daemon core lives in two other places —
`/git/github.com/LiGoldragon/triad-runtime` 0.7.0 (last substantive commit
`d323f90`, 2026-07-11, predating every Nexus vision record), which supplies
`AsyncMultiListenerDaemon`, `NexusWork`, `NexusAction`; and per-component
copies, e.g. `/git/github.com/LiGoldragon/lojix/src/runtime_flow.rs:417-421`
declares `pub mod nexus { … }` that shadows the crate name locally, so the
`nexus::NexusEngine` throughout `lojix/src/daemon.rs` is lojix's own module.
The crate is reached only as `nexus::Configurable`
(`lojix/src/lib.rs:40`, `:1104,1156,1173,1188`).

Witnessed: `/git/github.com/LiGoldragon/nexus/Cargo.toml:11-15` depends on
`rkyv` and `thiserror` only — not on `signal`, not on `sema`. Whether it
*should* is **not settled by any vision text this flow read**; stated as an
open question, not a defect.

**What realizing it takes:** port the two-socket bind, the frame/serve loop,
the runner continuation loop and the `NexusEngine` kind out of
`triad-runtime` and out of `lojix/src/runtime_flow.rs` into the `nexus`
crate, so a component supplies only its domain engine. A real port across
three repositories, not a rename.

**Safe unattended tonight: NO.** Large design work with an unsettled
dependency question, and lojix has a deployed consumer chain. For the
living.

---

### 7. Merge the signal repositories into `signal`

**Vision (2026-09-10, relayed)**, `/home/li/primary/flows/fe34eb/vision/signal.md:23`:

> Yeah, I think you understand the Signal repository, so we could merge all of that there, but let's not just throw a bunch of code that no one's using in there. Start with the code that was written recently ... Let's make sure that whatever depends on Signal standard is then depending on it, or just archive the old Signal repo and then rename the Signal Standard repo to it. We don't need the old Git history unless you think there's something useful there.

**Realization: mixed — two of four parts realized.**

- **Rename — realized.** Witnessed: `/git/github.com/LiGoldragon/signal`
  commit `626e407be520a7a12f39b1d06c56ec423f3b3d09` (2026-09-11 17:58),
  "Become the shared signal repository", body: "Renamed from
  signal-standard. The crate, library, and Cargo links key are now signal,
  at 2.0.0." `Cargo.toml:2-3`. GitHub redirects the old name.
- **Archive the old repo — realized.** Witnessed: `gh api
  repos/LiGoldragon/signal-legacy` → `archived: true`; the four sections
  judged worth keeping were carried verbatim into
  `/git/github.com/LiGoldragon/signal/DESIGN.md:9-11`.
- **Protocol TBD — realized.** Witnessed in four places, e.g.
  `/git/github.com/LiGoldragon/signal/README.md:29`, `src/lib.rs:9-10`,
  `ARCHITECTURE.md:70`.
- **Merge — partially realized.** Witnessed:
  `/git/github.com/LiGoldragon/signal-frame/Cargo.toml:6` still declares an
  independent 0.4.0 crate (~2,812 lines against `signal`'s 373), with
  **62 `Cargo.toml` dependents**, 28 of them floating on `branch = "main"`.
  What `626e407` lifted was the portable rkyv frame duplicated across the
  six generated contract crates, not signal-frame's envelope, handshake,
  exchange identifiers, async correlation, streams or reply plumbing.
- **Dependents — unrealized for the existing estate.** Witnessed: **14
  `Cargo.toml` files still name `signal-standard`** — `signal-agent:25`,
  `signal-criome:25`, `signal-mentci:23,34`, `signal-mentci-client:22`,
  `signal-mirror:25`, `meta-signal-agent:25`, `meta-signal-mentci:22,32`,
  `meta-signal-mentci-client:22,32`, `meta-signal-mind:25`,
  `meta-signal-mirror:26`, `meta-signal-router:36,47`, `mirror:58`,
  `router:68`, and `spirit:179`. Thirteen work today only because they pin
  pre-rename revisions and GitHub redirects. **One is actively broken**:
  `/git/github.com/LiGoldragon/spirit/Cargo.toml:179` follows `branch =
  "main"` on a package that no longer exists under that name (inference from
  the rename; no build was run).

**What realizing it takes:** for the merge — decide whether signal-frame's
envelope layer *is* the protocol the psyche deferred, then either absorb it
and retire signal-frame (migrating 62 dependents) or write down why the two
layers stay separate. For the dependents — repoint the 13 rev-pinned files
to `https://github.com/LiGoldragon/signal` with the package renamed; this is
a 0.2.x → 2.0.0 migration, not a URL edit.

**Safe unattended tonight: PARTIALLY.** Repointing `router`,
`meta-signal-router`, `signal-agent`, `signal-criome`, `signal-mentci`,
`signal-mentci-client`, `meta-signal-agent`, `meta-signal-mentci`,
`meta-signal-mentci-client`, `meta-signal-mind` is ordinary library work
with no running service. **Excluded by the brief:** `spirit` and `mirror`
(and `signal-mirror`, `meta-signal-mirror` as mirror's contracts) — which
unfortunately includes the one actively broken dependency. The merge
decision itself is for the living.

---

### 8. `ethos` — the repository for the upcoming ethos nexus

**Vision (2026-09-10, relayed)**, `/home/li/primary/flows/fe34eb/vision/ethos.md:7`:

> no, ethos-zero is not a daemon, hence its name. ethos is the repo for the upcoming ethos nexus

**Realization: half realized.**

- "ethos-zero is not a daemon" — **realized.** Witnessed: `grep -rni daemon`
  over `/git/github.com/LiGoldragon/ethos-zero` (`.rs`, `.md`, `.toml`,
  `.ethos`, `.nix`, excluding `target/`) returns **zero hits**.
  `Cargo.toml:8` — "Ethos schema language version zero: reads ethos,
  generates Rust". No `ethos-monolith` repo exists; GitHub redirects the old
  name to `ethos-zero`, matching the 2026-09-10 ruling at
  `flows/fe34eb/vision/ethos.md:15`.
- "ethos is the repo for the upcoming ethos nexus" — **unrealized.**
  Witnessed: `/git/github.com/LiGoldragon/ethos` does not exist locally;
  `gh repo view LiGoldragon/ethos` → "Could not resolve to a Repository".

**What realizing it takes:** create the repository. This flow's inference:
it is downstream of item 6 — an ethos nexus would be the first consumer of a
real `nexus` core, so the core comes first.

**Safe unattended tonight: NO.** Creating a repository for an undesigned
component is a `repository-lifecycle` decision for the living, and the thing
it would hold does not exist yet.

---

### 9. `error`, not `fault` — ethos-zero still carries it in its public API

**Vision (2026-09-09, relayed)**, `/home/li/primary/flows/564f55/vision/archive-datom.md:47`:

> the Text type becomes String, since Text confuses with Textualizable and text is all of the characters; error, not fault

and `archive-protos.md:109`: "error replaces fault".

**Realization: realized in protos and datom-codec; unrealized in ethos-zero.**

Witnessed: protos has `pub struct Error` / `pub enum Problem`
(`/git/github.com/LiGoldragon/protos/src/core.rs:51-64`), no `Fault`
identifier. datom-codec has `Error` with `ErrorLayer`/`ErrorKind`
(`/git/github.com/LiGoldragon/datom-codec/src/core.rs:66-98`), no `Text`
type, no `Fault` type; three prose survivals only
(`src/lib.rs:9`, `README.md:15`, `tests/core.rs:655`).

Witnessed: **ethos-zero still exports the word in its public API** —
`pub trait ConceptualFaulting` at
`/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:530`, `impl
ConceptualFaulting for Error` at `:564`, used at `src/checking.rs:13` and
`src/conception.rs:7`, with the noun through its docs (`src/lib.rs:13,16,19,
21,22,499,515,517,523,525,531`, `src/checking.rs:1,7,8,367,408`,
`src/conception.rs:143`) and locals named `fault` at `src/lib.rs:555,583,585`.

**Repository and files:** `/git/github.com/LiGoldragon/ethos-zero` —
`src/lib.rs`, `src/checking.rs`, `src/conception.rs`.

**What realizing it takes:** rename `ConceptualFaulting`, or fold it into
the existing `Error` construction, and sweep the prose. It is a **public
trait**, so a major bump: 8.0.0.

**Safe unattended tonight: YES.** A contained rename in a clean repository
with a local Nix gate, no running service, no deploy. It does mean a second
major release of ethos-zero hours after 7.0.0 — a `versioning` and
`breaking-upgrades` judgement the main flow should make, since ethos-zero's
one consumer (`orchestrate/Cargo.toml:19`) still pins `4695ee0c`, a release
behind, so nothing downstream is disturbed either way.

---

### 10. Stale protos vocabulary in ethos-zero's documentation

**Vision (2026-09-09, relayed)**,
`/home/li/primary/flows/564f55/vision/archive-protos.md:121` ("its root enum
is protos, not delineation") and `:153` ("the protoform is dropped").

**Realization: realized in protos; unrealized in ethos-zero's docs.**

Witnessed: no `Delineation` or `Protoform` in protos `src/`, `tests/`,
`protos.ethos`, or the working-tree README.

Witnessed: ethos-zero documents protos types that no longer exist —
`/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:11` (`| Text, canonical …
| protos::Delineation |`), `:12` (`| Protoform | protos::Delineation,
protos::Protoform |`), `src/checking.rs:7` ("as the protoform was laid
out"), and `README.md:14,15,20,65` (`Delineation`, `Protoform`,
`Situated<Error>`). These compile because nothing references the types.

Also witnessed: `/git/github.com/LiGoldragon/protos/tests/delineation.rs` is
still named for the retired type, though the pending fix rewrote its body.

**What realizing it takes:** rewrite the ethos-zero module-doc table and the
four README rows against `Protos`, `Extent`, `Error`; rename
`tests/delineation.rs` to `tests/reading.rs` (this is inside item 1's dirty
tree, so it belongs to that commit).

**Safe unattended tonight: YES for ethos-zero** — documentation only, no
API change, patch bump. **NO for the protos rename**, which is inside the
locked tree.

---

### 11. Parentheses are reserved for meaning, not opaque

**Vision (2026-09-08, relayed)**, `/home/li/primary/flows/564f55/vision/archive-protos.md:29`:

> parentheses are not opaque; they are unspecified, treated as opaque until specified

and `:37`: "parentheses are reserved for meaning; the meaning type is what has not been specified".

**Realization: partially realized — the behaviour is right, the vocabulary
contradicts the correction.**

Witnessed: the behaviour matches Vision
(`/home/li/primary/Vision/protos.md:98-100`). Parentheses read by balance
(`/git/github.com/LiGoldragon/protos/src/core.rs:333-337`, `:340-353`);
datom-codec lifts them to a distinct `Form::Meaning(Opaque)`
(`/git/github.com/LiGoldragon/datom-codec/src/core.rs:21`,
`src/composition.rs:52-59`), with the intrinsic `pub struct Meaning(pub
Opaque)` at `src/composition.rs:361` and `Meaning.String` at
`datom-codec.ethos:11`; a Meaning in a String position is refused, not
flattened (`src/composition.rs:738-752`, `:247-255`).

Witnessed: **the vocabulary states the retracted claim.**
`/git/github.com/LiGoldragon/protos/README.md:65` — "Guillemets and
parentheses are opaque: every glyph inside is content" — is exactly what the
psyche corrected. The words *reserved*, *unspecified* and *meaning* appear
nowhere against parentheses in protos `src/`, `protos.ethos`, or the README.

One further note, this flow's inference:
`/home/li/primary/Vision/datom.md` "Meaning" says "today a parenthesized
text lands as a plain String, with the later type marked in code" — the code
has **overshot** that transitional allowance in the direction Vision points,
landing it as its own `Form::Meaning`. That is realization, not divergence,
but the distilled sentence is now behind the code and may want a
distillation edit.

**What realizing it takes:** a documentation and naming pass in protos —
say on `Boundary` in `src/core.rs` and in the README's opaque-regions
section that parentheses are reserved for a meaning type not yet specified
and are read as opaque only provisionally. Whether `Boundary::Parentheses`
should eventually move off `Opaque` is **not settled** and needs the living.

**Safe unattended tonight: NO** — the file is inside item 1's locked dirty
tree. Fold it into that commit or do it after.

---

### 12. Single-field structs are an aberration and should be refused

**Vision (2026-09-08, relayed)**, `/home/li/primary/flows/8e9e77/vision/single-field-structs.md:5`:

> there's another recent flow which you might want to look into, where we talked about single-field structs, which are an aberration and which we need to sort of train against, or possibly even refuse. I think we should possibly even refuse single-field struct types and ethos, and instruct against them even in Rust, because those should be new types.

and `:13-15`:

> This should be a new type and not a struct with just a single element in it. ... a new type should be just the name of the type and then the separator, which is a period, and then the name of the contained type. ... A new type generally is like `name.string`, `age.integer`.

**Realization: unrealized, and it carries a Vision conflict the living must resolve.**

Witnessed, ethos-zero: `Meters.{ Integer }` is **accepted**, generating
`pub struct Meters { pub integer: i64 }` (observed by running the built
binary). The specific complaint the psyche reacted to is answered — it is no
longer a *tuple* struct, because `FieldNaming`
(`/git/github.com/LiGoldragon/ethos-zero/src/generation.rs:434`) always
names fields. But there is no arity-one refusal anywhere: the only
`Problem::arity` sites (`src/checking.rs:518,632-638,701-707`,
`src/conception.rs:103`) are intrinsic-argument and constraint counts.

Witnessed, datom-codec's derive: the struct arm emits `Form::Struct(vec![…])`
with **no arity-1 case**
(`/git/github.com/LiGoldragon/datom-codec/crates/datom-codec-derive/src/lib.rs:189-196`),
while the *enum* arm of the same macro does have the transparent case
(`:140-141`). The asymmetry is in the crate's own fixtures: `struct
NodeData<T>(T)` at `tests/core.rs:920-921`.

Witnessed, and this is the blocker: the form the psyche prescribed, `X.T`,
generates a Rust **alias**, not a newtype — `Name.String` → `pub type Name =
String;`, `/git/github.com/LiGoldragon/protos/generated-contract/protos.rs:7`.
And `/home/li/primary/Vision/ethos.md` explicitly endorses that: "An alias
bears them through the type it names: an alias is not a new type and cannot
carry a derive." **So the psyche said a single-field struct "should be a new
type", and the form named for it produces something Vision itself calls not
a new type.** Meanwhile protos hand-writes the newtype it actually wants —
`pub struct Symbol(pub String);`
(`/git/github.com/LiGoldragon/protos/src/core.rs:27`) — which ethos-zero
cannot express and the generated contract flattens to an alias.

Witnessed: it is load-bearing today. `ReaderBudget.{ Integer }` at
`/git/github.com/LiGoldragon/protos/protos.ethos:16` generates `pub struct
ReaderBudget { pub integer: i64 }` (`generated-contract/protos.rs:74-76`),
and protos's `dependency-ethos` flake check runs ethos-zero over that file —
so refusing one-position products today **breaks protos's own gate**.

Witnessed: this is the **only** item in the 2026-09-08/09 batch with no
distilled counterpart — `grep "single-field"` across `Vision/*.md` hits only
`Vision/datom.md:132`, which is about variants. This flow's inference: that
is the likeliest reason it is also the item with no movement in the code.

**What realizing it takes, in order:** (a) the living settles whether `X.T`
emits `pub type X = T` or a real newtype; (b) a refusal in `Checkable` with a
new `Problem` variant; (c) rewrite `protos.ethos:16` and regenerate the
contract; (d) an arity-1 arm in datom-codec's struct derive mirroring
`:140-141`; (e) major bumps on ethos-zero, protos and datom-codec.

**Safe unattended tonight: NO.** It needs a psyche ruling, it would break a
sibling repository's gate, and it changes canonical wire text in three
repositories at once.

---

### 13. The subagent demanding tier must be Opus 4.6, not Opus 5

**Vision (2026-09-05, relayed)**, `/home/li/primary/flows/58a86d/vision/subagentModel.md:3-7`:

> ## 2026-09-05 — Opus 4.6, not Opus 5
>
> Context: the flow had offered Opus 5 for the demanding and critical subagent tiers, since no Opus 5.1 exists and those tiers are pinned to Opus 4.6.
>
> I dont want opus 5, which is why I use 4.6

**Realization: NOT A DEFECT — superseded three days later. The code is
right and this entry is stale vision.**

This flow first judged it a dated regression and was **wrong**. The
correction is recorded in full because the error is instructive and because
anyone reading the 2026-09-05 entry alone would "fix" `roles.datom`
backwards.

What this flow witnessed and what it wrongly concluded:
`/git/github.com/LiGoldragon/Curriculum/roles.datom` assigns
`{ demanding { claude-opus-5 Some.Medium } … }`, and
`/home/li/primary/.claude/agents/{read,write}-demanding.md:4` carry
`model: 'claude-opus-5'`. `git log -S'claude-opus-5'` shows it entering at
`c5498a2`, **2026-09-08** — three days *after* the ruling. This flow read
that as a regression.

**The superseding record**, witnessed after a subflow surfaced it —
`/home/li/primary/flows/5851f4/vision/psycheFacingModel.md`, first committed
2026-09-08, heading "Opus 4.6 for the interlocutor, Opus 5 for subagents".
Its context paragraph names the very entry above, and the psyche typed:

> Yes, I did say 4.6 is better at understanding me, which means that this doesn't concern the skills, but I'm just explaining it to you so you can maybe log this. If I'm not going to use Fable as the main orchestrator, like you are now with your Fable, then I would use Opus 4.6, but I would still let him use Opus 5 for sub-agents. Now I realize the whole point isn't to avoid Opus 5 per se. It's just to avoid Opus 5 as the interlocutor, because a psyche-facing model 4.6 is better than 5 in Opus.

And `/home/li/primary/flows/5851f4/vision/subagents.md`, same date:

> So now we can take out the critical role on both sides:
> - On the Claude side, we have Haiku, Sonnet, and Opus, all at medium effort: Haiku 4.5, Sonnet 5, and Opus 5.
> - On the codex side, we would also have three roles: Luna, Terra, and Sol

So commit `c5498a2` is not a regression — it **implements** the 2026-09-08
ruling exactly, `claude-opus-5` for demanding and Sol on the Codex side
included. `roles.datom` is correct as it stands.

**What is actually owed here is a distillation, not a code change:**
`/home/li/primary/flows/58a86d/vision/subagentModel.md` and `codexModel.md`
are stale vision that a later record has revised, and nothing marks them so.
A reader arriving at them first is misled — as this flow was.

**The one live contradiction that remains** is the one
`skill-proposals.md` §14a already raises: `/home/li/primary/AGENTS.md` still
carries "Subagents must never use or inherit Sol", grounded in
`flows/358f143a/vision/entryFiles.md` (2026-08-17), while `roles.datom` and
the generated `.codex/agents/{worker,read-demanding,write-demanding}.toml`
assign `gpt-5.6-sol` to every demanding depth. An agent reading both is
given contradictory instructions. §14a proposes relocating the AGENTS.md
section but does not resolve which side is right. **Only the living can.**

Separately, on Astra: witnessed, `/home/li/.codex/config.toml:4` sets
`model = "gpt-6-astra"` and `:11` sets
`default_subagent_model = "gpt-5.6-luna"` — which **realizes** "Astra for the
main flow only". Astra's absence from `roles.datom` is correct, since that
file governs subflow depths only.

**Safe unattended tonight: NO ACTION — do not touch `roles.datom`.** The
distillation that retires the two stale 58a86d entries needs the living's
approval like any Vision edit.

---

### 14. Visuals in a response must be ASCII; otherwise the web report

**Vision (2026-09-05, relayed)**, `/home/li/primary/flows/58a86d/vision/visuals.md:7`:

> You can use visuals if you give me visuals directly in the response. Has to be ASCII. That also should be in a skill. If you want to use visuals, you have to use the web report.

The psyche said outright where it belongs: "That also should be in a skill."

**Realization: unrealized.** Witnessed: no skill under
`/home/li/primary/.claude/skills/` states it; `grep` for `ASCII` hits only
`orchestrate/SKILL.md:14` and `datom/SKILL.md:42`, both about datom syntax.

**Covered by `skill-proposals.md`: NO.** Witnessed: `grep` for
`ASCII|visual` over that report returns only three datom-syntax lines
(512, 789, 803). A second gap in the existing proposals.

**What realizing it takes:** one or two sentences in an authored skill —
`flow-evidence` or `behavior` are the candidates — then regenerate.

**Safe unattended tonight: NO.** Skill edit; proposal only. It is small
enough to write tonight as an addendum.

---

### 15. A dedicated flows repository

**Vision (2026-09-05, relayed)**, `/home/li/primary/flows/e996e8/vision/flows.md:5`, `:13-15`, `:21`:

> I think we need a dedicated repository for the flow IDs so we could just mount it or link it in that position where we're putting them.

> in primary

> Yeah, there's just too much going on in the Flow directories, so using a dedicated repository would make sense, I think.

> Yeah, the whole Flow directory essentially becomes a repository. That's all. There's not really a lot of complexity to it. ... And we need a proper name for it because Flow is already a component that we're drafting, so maybe Flow data or flows plural data. Maybe you have some suggestions there.

**Realization: unrealized.** Witnessed: `/home/li/primary/flows` is a plain
directory, not a symlink and not a gitlink; `git -C /home/li/primary ls-files
flows` returns **1510 tracked files**, all regular blobs. No repository under
`/git/github.com/LiGoldragon/` matches flow/flows/flow-data; `gh api
search/repositories?q=user:LiGoldragon+flows` → `total_count: 0`. No mount or
link configuration exists in CriomOS, CriomOS-home or Curriculum.

The naming question the psyche explicitly opened — "Maybe you have some
suggestions there" — is **unanswered in any file**. That is an owed reply,
not just unbuilt work.

**What realizing it takes:** create the repository, move `flows/` history out
of primary, link it back at `/home/li/primary/flows`.

**Safe unattended tonight: NO.** Moving 1510 tracked files that every flow
and several skills reach by path, while sibling subflows of this very flow
are writing into `flows/f6db8d/`, is the worst possible night for it. And the
name is the psyche's to choose.

---

### 16. A static workspace repository

**Vision (2026-09-05, relayed)**, `/home/li/primary/flows/e996e8/vision/workspace.md:7-10`:

> I also want to make my way to a more static workspace repository, which is mostly just about holding the infrastructure of a workspace, like:
> - the skills
> - the agent's description
> - maybe some other stuff I can't think of right now

**Realization: unrealized as described; Curriculum already covers two of the
three things named.**

Witnessed: `/git/github.com/LiGoldragon/Curriculum/README.md:1-8` — "the
canonical data root for reusable agent instruction sources and role
definitions ... contains no runtime, generator, deployment configuration, or
generated consumer output." It holds `skills/` (38 sources) and
`roles.datom` (the agents' descriptions). It is already static and consumed
externally.

Witnessed: a repository `LiGoldragon/workspace` exists on GitHub (not cloned
locally), created 2026-04-22, last pushed 2026-05-02, holding `flake.nix`,
`lib/`, `checks/`, `docs/`, `workspace.code-workspace`. It predates the
statement by four months. This flow does **not know** whether the psyche had
it in mind.

**What realizing it takes:** a decision this flow cannot make from the
record — whether Curriculum is broadened into the workspace repository, or a
new repository sits beside it consuming Curriculum, or the dormant
`workspace` repository is revived.

**Safe unattended tonight: NO.** It is a question for the living, and the
answer moves skill-generation paths.

---

### 17. The Psyche component

**Vision (2026-09-05, relayed)**, `/home/li/primary/flows/1a6ca4/vision/psyche.md:7`:

> not the psyche log (the psyche log is obviously going in Psyche, which is why Psyche is so important: it gets its own sort of mind-like component).

**Realization: unrealized.** Witnessed:
`/git/github.com/LiGoldragon/psyche` HEAD `14b9c3e` (2026-08-14),
`Cargo.toml` version 0.1.0, description literally "Quick-new Psyche MVP
component scaffold." `src/lib.rs` is **5 lines**; the only test is
`tests/segregation.rs` (31 lines). No binary, no store, no log handling. The
psyche log today is markdown in primary.

The companion statement, `/home/li/primary/flows/1a6ca4/vision/mind.md:7`
("the mind component replaces the files, readmes and indexes ... the memory
of the system is going to go in mind") is **partially realized**: witnessed,
`/git/github.com/LiGoldragon/mind` is real — version 0.8.0, ~21,158 lines,
binaries `mind`/`mind-daemon`/`meta-mind`, a store under
`src/actors/store/`, daemon-persistence and memory tests — but HEAD is
`ee4f34f` (2026-07-31), six weeks stale, and it has plainly replaced nothing
in `/home/li/primary`, which is still full of `reports/`, `handoffs/`,
`verified/` and markdown indexes. `mind` also has **21 uncommitted files**
(witnessed) which nobody has claimed.

**Safe unattended tonight: NO.** Building psyche out along mind's lines is
multi-day component work. The 21 dirty files in `mind` are worth surfacing
to the living separately — this flow does not know whose they are.

---

### 18. A tool that establishes age from git commits

**Vision (2026-09-08, relayed)**, `/home/li/primary/flows/8e9e77/vision/flow-retrieval.md:5`:

> we might have to train the flow retriever to better understand how to use git commits to establish how old something is. Maybe we even need to develop a tool to do that better.

**Realization: unrealized, both halves.** Witnessed: `/home/li/primary/tools/`
holds three scripts (`engine-situation`, `jj-branch-queue`,
`nix-local-stack`); none reads commit dates.
`/git/github.com/LiGoldragon/relative-age-display` (HEAD `6961aac`,
2026-08-13 — four weeks *before* the ask) converts a `Duration` into a typed
`HumanReadableTime`; it never touches git, and grepping every `Cargo.toml`
under `/git/github.com/LiGoldragon/` finds **no consumer at all**.
`/git/github.com/LiGoldragon/transcript` is a single `transcript.py`, no age
handling.

**Covered by `skill-proposals.md`: the training half, yes** — §12
"`psyche-acquisition` — establishing age", proposing replacement text for
line 7. The tool half is not covered.

**What realizing it takes:** something that walks `git log` per path and
feeds durations to `relative-age-display`, which is the presentation end
already built.

**Safe unattended tonight: YES for the tool.** A new small program with no
service, no deploy and no consumer to break — and it would give
`relative-age-display` its first consumer. The skill half is a proposal.

---

### 19. Containers — podman was named, nspawn is what exists

**Vision (2026-09-08, relayed)**, `/home/li/primary/flows/8e9e77/vision/containers.md:5-7`:

> This is why I called it pod. I think Red Hat Linux has a tool called Podman, short for pod manager, I think. I was going more towards container than virtual machine, but we could have both, right?

**Realization: partially realized — the capability exists under a different
tool.** Witnessed: `podman` appears **nowhere** in CriomOS or CriomOS-home
(zero hits over all text files); same for `docker` and `oci`. What exists is
systemd-nspawn: `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nspawn.nix:12-125`
wraps `pkgs.nixos-container` as `criomos-nspawn`; `:167`
`boot.enableContainers = true`; the psyche's own word is already the name of
a role — `modules/nixos/disks/pod.nix` sets `boot.isContainer = true`. The VM
half exists too (`modules/nixos/vm-testing/default.nix:118`,
`test-substrate.nix:171,211`), so "we could have both" is structurally true.

Witnessed on this machine: `systemctl list-units 'container@*'` lists 0
units, `machinectl list` says "No machines", and `criomos-nspawn` is not
present — the module is gated to large center nodes and this is not one.

This flow's inference, flagged: the quote reads as naming podman for the
*origin of the word "pod"*, not as choosing it. nspawn already delivers the
lightweight-container half. Worth asking rather than building.

**Safe unattended tonight: NO.** Adding `virtualisation.podman` touches a
system rebuild and activation — a deploy, excluded by the brief.

---

### 20. Finish removing VSCodium; tie the desktop app to Claude Code

**Vision (2026-09-05, relayed)**, `/home/li/primary/flows/58a86d/vision/vscodium.md:7`:

> let's get rid of vscodium; we now use the claude and chatgpt desktop apps instead. vscodium is obsolete.

**Realization: realized, with residue.** Witnessed:
`/git/github.com/LiGoldragon/CriomOS-home` commit `befd927`, 2026-09-05
11:53 — subject quotes the ruling verbatim — removed `modules/home/vscodium/`;
it is an ancestor of HEAD. On the running machine `codium`/`vscodium`/`code`
are not on PATH while `claude-desktop`, `claude` and `chatgpt` are.

Residue witnessed: the `nix-vscode-extensions` flake input survives at
`CriomOS-pkgs/flake.nix:16-17,20,25` and `CriomOS-home/flake.nix:409,454`;
a dead Stylix `vscode.enable = false;` at
`CriomOS-home/modules/home/base.nix:187`; stale prose in
`CriomOS-home/AGENTS.md:10`, `docs/ROADMAP.md:14`, `README.md:16`,
`UPGRADES.md:140`.

The companion statement, `/home/li/primary/flows/58a86d/vision/claudeDesktop.md:7`
("It should be updated along with the Claude code. I believe it also uses
Claude code internally"), is **partially realized**: the psyche's belief is
confirmed and the internal coupling is fail-closed and check-enforced
(`CriomOS-home/owned-agents/claude-desktop/default.nix:5,190-199,217`;
`checks/claude-desktop-declared-cli/default.nix` boots the app under Xvfb
twice to prove it). What drifts is the Electron app's own pin:
`claude-desktop/hashes.json` is 1.46388.2 (2026-09-05) while
`claude-code/hashes.json` is 2.1.263 (2026-09-07), each with its own
`update.py` and nothing sequencing them.

**Safe unattended tonight: NO for both.** Removing the flake input changes
two lockfiles and requires a closure rebuild and activation — a deploy. The
four prose files could be corrected alone, but doing prose without the input
leaves the inconsistency the prose describes.

---

## Part B — recent vision already realized

Recorded so the main flow does not re-open them. All witnessed.

| Vision | Date | Where it is realized |
|---|---|---|
| "only if it's a bare (undelimited because it doesnt need delimiters) string" — `flows/fe34eb/vision/datom.md:7` | 09-10 | `datom-codec/src/core.rs:19` `Form::Bare`; `:179`; `src/composition.rs:204-209` `BareStringComposing`; `datom-codec.ethos:17` `Bare.String`; `README.md:51`. No competing name survives. |
| The reconciled Nexus first heading — `flows/fe34eb/vision/nexus.md:51` ("yes, good") | 09-11 | `Vision/nexus.md:5`, landed at commit `c05f02b58`. |
| "keep 'the ethos repository is for the ethos nexus' under Zero only" — `flows/fe34eb/vision/ethos.md:19` | 09-11 | `Vision/ethos.md`, Zero heading only. |
| "'trait' is still valid to say, because we still write Rust" — `flows/fe34eb/vision/ethos.md:27` | 09-11 | `Intent/mandatoryTraits.md` stands unamended; no change was owed. |
| ethos-zero is not a daemon; no ethos-monolith | 09-10 | Zero `daemon` hits in the repo; `Cargo.toml:8`; GitHub redirect only. |
| signal renamed from signal-standard; old signal archived; protocol TBD | 09-10 | `signal` `626e407`, `Cargo.toml:2-3`; `signal-legacy` `archived: true`; `signal/README.md:29` and three more. |
| "the situated datom is the rectification of a design flaw" — `flows/564f55/vision/archive-datom.md:131` | 09-09 | Realized in its *rectified* form, which is what the psyche approved ("This is brilliant"): no `Situated` pair, no `Site` type. Path on the datom (`datom-codec/src/core.rs:8-12`), applied recursively (`src/composition.rs:82-88,128`; derive at `crates/datom-codec-derive/src/lib.rs:139-147`), extent a fact of protos (`src/core.rs:99-124`), budget a fact of the reader (`src/core.rs:24-30`). |
| "a derive implements the kind on any Rust type" — `archive-datom.md:39` | 09-09 | `crates/datom-codec-derive/src/lib.rs:16,119`; no attributes read anywhere — structural all the way down; exercised on non-ethos types at `tests/core.rs:920-936`. |
| "the Text type becomes String" — `archive-datom.md:47` | 09-09 | No `Text` type in datom-codec; `Textualizable` only. |
| "enclosed, not closed" — `archive-protos.md:137` | 09-09 | `protos/src/core.rs:36-40`, `:16-20`, `:288`; `protos.ethos:13`. No `Closed` identifier in either repo. |
| "the guillemet ... should delimit strings; the curly quote is no longer a delimiter" — `archive-protos.md:3,21` | 09-08 | `protos/src/core.rs:273-283` (no curly-quote arm), `:22-25`, `:126-136`; witnessed positively at `tests/textualization.rs:191`. |
| "a struct has named fields; Ethos generates the names deterministically" — `archive-ethos.md:19` | 09-08 | `ethos-zero/src/generation.rs:388-403`, `:434-460`; observed output `pub struct Generation { pub first_string: String, pub second_string: String }`. |
| "field naming as proposed; type-first; the sugar-derived name carries an underscore" — `archive-ethos.md:39` | 09-08 | `generation.rs:390-402`; observed `string_vector`, `lock_option`, and `Overlap_Data` beside `pub enum PathOverlap`. |
| "Ethos does not generate implementations" / the retraction — `archive-ethos.md:11,29` | 09-08 | Reconciled as the retraction permits: no `impl` bodies emitted anywhere in `generation.rs`; derives (`:576-588,606-608,624-633`), trait declarations (`:835`) and const assertions (`:863,884`) only. |
| "stop locking your own flow directory" — `flows/e996e8/vision/editCoordination.md:7` | 09-05 | `.claude/skills/edit-coordination/SKILL.md:6`: "A flow's own directory is never locked: only the flow that has its id ever writes there." |
| "the library is called datom codec; datomic is too confusing" — `flows/1a6ca4/vision/archive-datom.md:11` | 09-05 | The crate is `datom-codec`; `Vision/datom.md:244-247` carries the reason. |
| "get rid of vscodium" — `flows/58a86d/vision/vscodium.md:7` | 09-05 | `CriomOS-home` `befd927`, same day. Residue listed at item 20. |

---

## Part C — vision that concerns how flows behave (skills)

**These are proposals only.** The living reserved skill edits for approval
(`flows/f6db8d/log.md`, the night brief). The column says whether
`/home/li/primary/flows/f6db8d/reports/skill-proposals.md` already carries a
proposal for it.

| Vision | Date | Path:line | In `skill-proposals.md`? |
|---|---|---|---|
| A cross-harness invocation is still a subflow | 09-12 | `flows/162eb3/vision/subflows.md:11` | **Yes** — §1 `main-flow`, §1a/§1b |
| No sandbox, all permissions (with the wrapper question) | 09-12 | `.../subflows.md:19` | **Yes** — §1; the wrapper status is witnessed and answered there |
| A different harness is invoked with the subflow training | 09-12 | `.../subflows.md:27` | **Yes** — §1b |
| The main-flow skill is only ever typed into the prompt | 09-12 | `.../subflows.md:35` | **No, and §1c concludes the opposite.** It verified the authored frontmatter, not the deployed tree. Not a skill edit at all — a stale regeneration (item 3) |
| The flow is triggered only on Send to Claude | 09-12 | `flows/fe34eb/vision/reports.md:3` | **Yes** — §2 `psyche-interraction` |
| "machines think in code" is pretty but not very useful on its own | 09-12 | `flows/fe34eb/vision/designPractice.md:3` | **Yes** — bears on §10; it *withdraws* the 09-08 line from becoming Intent |
| Launching subflows in the same harness | 09-10 | `flows/162eb3/vision/subflows.md:3` | **Yes** — §1 |
| Machines think in code; give the machine the code | 09-08 | `flows/564f55/vision/designPractice.md:3` | **Yes** — §10 `psyche-distillation`. Read with the 09-12 entry above, which qualifies it |
| Example code is for what the models don't know, not Cargo files | 09-08 | `.../designPractice.md:11` | **Yes** — §10 |
| Useless tests — the absurd decomposition test | 09-08 | `flows/8e9e77/vision/tests.md:3` | **Yes** — §11 `testing`. Witnessed: the current `testing` skill forbids change-detector tests (`.claude/skills/testing/SKILL.md:11-15`) but does not name the absurd decomposition test |
| Use git commits to establish how old something is | 09-08 | `flows/8e9e77/vision/flow-retrieval.md:3` | **Yes** for the training half — §12; the tool half is item 18 |
| Stop locking your own flow directory | 09-05 | `flows/e996e8/vision/editCoordination.md:3` | Not needed — **already realized** (Part B) |
| Visuals in the response are ASCII; otherwise the web report | 09-05 | `flows/58a86d/vision/visuals.md:3` | **NO** — a gap (item 14) |
| Opus 4.6, not Opus 5 | 09-05 | `flows/58a86d/vision/subagentModel.md:3` | Not needed — **superseded** by `flows/5851f4/vision/psycheFacingModel.md` (item 13). What is owed is a distillation retiring the stale entry |
| Astra for the main flow only; subflows stay Luna and Terra | 09-05 | `flows/58a86d/vision/codexModel.md:3` | Astra half **realized** (`/home/li/.codex/config.toml:4,11`); the Sol half **superseded** by `flows/5851f4/vision/subagents.md`. The live `AGENTS.md`-vs-`roles.datom` Sol contradiction is §14a and needs the living |
| Extend flow logging with a summary on instruction | ~09-08 | `flows/403a1a/vision/flowLogging.md` (undated; see Part E) | **NO** — a gap |

One correction to `skill-proposals.md` §1's evidence, witnessed by a subflow
of this flow: §1 states that neither the claude nor the codex wrapper passes
a permission flag. That is true of `claude` itself
(`/git/github.com/LiGoldragon/CriomOS-home/owned-agents/claude-code/default.nix:52-64`
sets env vars only) but **omits `cci`**, the agent-intercom client, which
does — `/git/github.com/LiGoldragon/CriomOS-home/packages/agent-intercom/default.nix:155-157`
adds `--dangerously-skip-permissions`, re-emitted to the child at
`cci.mjs:250` and asserted by `checks/agent-intercom/default.nix:85`. On the
Codex side the flags are redundant rather than required: `/home/li/.codex/config.toml:1,8`
already sets `approval_policy = "never"` and
`sandbox_mode = "danger-full-access"`, declaratively managed by
`modules/home/profiles/min/codex-permission-defaults.nix`. §1b's proposed
*text* holds either way, since it says "except where the installed wrapper
or that harness's own configuration already supplies them"; only the
evidence paragraph is incomplete.

Two further skill-class findings this flow witnessed, both already in
`skill-proposals.md`, listed because they are consequences of the code
releases rather than of a psyche statement:

- The `protos`, `datom`, `ethos` and `orchestrate` skills teach the
  **superseded** delimiter design — guillemets as a map and curly quotes as
  the string delimiter. Witnessed: `.claude/skills/protos/SKILL.md:16,18`,
  `.claude/skills/datom/SKILL.md:15,23,25,38,67-68`,
  `.claude/skills/ethos/SKILL.md:66,69,88,92`,
  `.claude/skills/orchestrate/SKILL.md:14`. Covered by §§4, 5, 6, 7 with full
  replacement bodies. The ethos-zero release makes the `ethos` skill wrong on
  one more point — it says the Signal query enum is `Request`.
- `roles.datom` is itself written in curly-quote datom (14 delimited
  strings). Covered by §15, which correctly flags it **blocked** until the
  reader that consumes the file is witnessed.

---

## Part D — notions in the window

Notions rule nothing and are listed separately, as the brief directs. Only
two carry a date of 2026-09-05 or later.

**`/home/li/primary/flows/fe34eb/notion/reports.md:3`, 2026-09-11** — "too
many reports and witnesses; Codex logs compulsively; too complicated a
subject for now":

> Well, we can go into that if you want. What you're talking about is cloud only for now, but I do want to bring up also the topic of the fact that I see too many reports. Maybe it's okay, though. I don't know. It feels like a lot of reports sometimes, and a lot of witnesses, especially Codex, will just think that he has to log everything. It's a little bit compulsive. Yeah, too complicated a subject

The recording flow marked it notion because the living framed it as
exploration ("Maybe it's okay, though. I don't know."). This flow notes only
that it bears on tonight's output volume — eleven reports now sit in
`flows/f6db8d/reports/`, this one included — and that the psyche explicitly
declined to settle it.

**`/home/li/primary/flows/564f55/notion/datom.md:3` and `:13`, 2026-09-09** —
the value layer, and "composed and composable for the in-memory value
layer". Superseded as vision by the living's own retraction at
`flows/564f55/vision/datom.md:19-23`:

> None of what I was saying about the value layer was vision. It was a notion. I was brainstorming with you, so none of what I said about the value layer has any authority in the vision.

Nothing in the code should be built on either.

---

## Part E — recent vision with no date heading

Recovered by first-commit date, not by heading, after the gap described at
the top. These were outside the brief's sweep and are **not** ranked into
Part A, because their commit dates bound when they were written rather than
when the psyche spoke. Several plainly deserve ranking once dated properly.

| Path | First committed | Subject, and whether it looks realized |
|---|---|---|
| `flows/5851f4/vision/psycheFacingModel.md` | 09-08 | Opus 4.6 as interlocutor, Opus 5 for subagents. **Realized** — and it supersedes item 13. |
| `flows/5851f4/vision/subagents.md` | 09-08 | Three roles per side, all medium effort; Haiku 4.5 / Sonnet 5 / Opus 5; Luna / Terra / Sol. **Realized** in `roles.datom`. |
| `flows/5851f4/vision/skills.md` | 09-08 | "A skill enters the middle stratum only on Claude … That's not true for Codex." Bears directly on item 3 — the two harnesses gate skills differently, which is exactly why the `user-only` transform is per-target. Not checked against the `context-strata` skill. |
| `flows/5851f4/vision/thinkingPhases.md` | 09-08 | Break the thinking process into phases, each assigned to a different flow: an interpretation layer before the flow that acts. The psyche names the subagent-model incident as the motivating failure — "if there had been a process that processes what I said and creates instructions first … the second flow would have used the right model." **Unrealized**, and large. It is the same ground as `Vision/flowNexus.md` ("A Nexus component decides the system prompt … replacing the harness's subagents with specialized harnesses"). |
| `flows/5851f4/vision/anatomyOfCommunicatingThinkingAndReacting.md` | 09-08 | Research Panini's Sanskrit grammar and what branches from it, to build a rough anatomy of communicating, thinking and reacting. A research dispatch. A repository `Ashtadhyayi` exists under `/git/github.com/LiGoldragon/`; this flow did not open it. |
| `flows/403a1a/vision/flowLogging.md` | 09-08 | Extend the flow logging protocol with a **summary** written by the main flow on the instruction to summarize: chronology of subflows, what each stood for and produced, lessons, unfinished topics, associated beads. **Unrealized** — not in `main-flow` or `beads`. Skill-class; **not** in `skill-proposals.md`. |
| `flows/7dc7cc/vision/redeploying-the-operating-system-after-a-user-is-deployed.md` | 09-07 | "After a user is deployed, we need to redeploy the entire operating system so that, if there's a reboot, the user environment isn't replaced with an older version." Deploy-class; excluded tonight. |
| `flows/0384e0/vision/deployIncludesUserEnvironment.md` | 09-06 | "Whenever I say deploy, I always want [the user's environment] up to date and refreshed." Deploy-class; excluded tonight. Pairs with the row above. |
| `flows/db267d/vision/reminders.md` | 09-06 | "I don't know where we put reminders, but I guess we need a system for that." Openly unsettled; a question, not a ruling. |
| `flows/e71fa5/vision/private-data-separation.md` | 09-10 | "we're just doing everything public for now. We're gonna work towards creating a separation of private data." Directional. Bears on item 15 — moving `flows/` to its own repository is where that separation would first bite. |
| `flows/542442/vision/node.md` | 09-05 | Node *variant*, not node species; generic nodes rather than shared. CriomOS-class; deploy-adjacent. |

Two of these matter enough to say plainly. **`thinkingPhases.md` is the
most consequential unrealized vision this flow saw all night** — it is the
psyche describing the architecture that would have prevented the exact class
of failure that produced this report's own item 13. And
`flows/403a1a/vision/flowLogging.md` is a concrete, small, uncovered skill
proposal.

---

## Part F — two things the living should see that are not vision items

1. **`orchestrate` still pins ethos-zero one release behind.** Witnessed:
   `/git/github.com/LiGoldragon/orchestrate/Cargo.toml:19` pins `4695ee0c`
   (6.1.6), not tonight's `c8a6836` (7.0.0). Also witnessed: **ethos-zero
   carries no git tags at all** (`git tag` empty, `git describe` fails), so
   "released" means a manifest bump at a clean commit and consumers pin by
   revision.

2. **Uncommitted work nobody has claimed.** Witnessed:
   `/git/github.com/LiGoldragon/mind` has 21 modified files at HEAD `ee4f34f`
   (2026-07-31); `/git/github.com/LiGoldragon/signal-forge` has modified
   `ARCHITECTURE.md` and `Cargo.lock` at HEAD `dca42cd` (2026-07-31);
   `/git/github.com/LiGoldragon/Curriculum` has a deleted `result` symlink.
   Separately, `/home/li/primary` itself carries two uncommitted submodule
   deletions under `flows/da223f/joint.0jZ7PT` which flow f6db8d already
   recorded that `jj` would not stage. None of these belongs to this flow and
   none was touched.

---

## Sources

- Psyche read whole by this flow: `/home/li/primary/flows/fe34eb/vision/`
  (`datom.md`, `nexus.md`, `ethos.md`, `signal.md`, `designPractice.md`,
  `reports.md`) and `notion/reports.md`;
  `/home/li/primary/flows/162eb3/vision/subflows.md`;
  `/home/li/primary/flows/564f55/vision/` (`datom.md`, `ethos.md`,
  `designPractice.md`) and `notion/datom.md`;
  `/home/li/primary/flows/e996e8/vision/` (`workspace.md`, `flows.md`,
  `editCoordination.md`); `/home/li/primary/flows/8e9e77/vision/`
  (`tests.md`, `single-field-structs.md`, `flow-retrieval.md`,
  `containers.md`); `/home/li/primary/flows/58a86d/vision/` (all five);
  `/home/li/primary/flows/1a6ca4/vision/` (`psyche.md`, `mind.md`,
  `flow.md`, `personaMetaHarness.md`, `thinkingMachineProcedures.md`);
  `/home/li/primary/flows/542442/vision/archive-datom.md`;
  `/home/li/primary/Vision/` (`datom.md` Repository/Map, `nexus.md`,
  `ethos.md`, `signal.md`, `sema.md`, `flowNexus.md`, `highLevelView.md`,
  `orchestrate.md`); `/home/li/primary/Intent/` (all six — none in the
  window). The date sweep was a single `grep` for `2026-09-0[5-9]` and
  `2026-09-[12][0-9]` across `Vision/`, `Intent/`, `vision-raw/`,
  `flows/*/vision/`, `flows/*/notion/`, yielding 124 lines.
- Relayed from this flow's own earlier reports, not re-derived:
  `/home/li/primary/flows/f6db8d/reports/protos-fix.md`,
  `datom-codec-fix.md`, `ethos-zero-fix.md`,
  `skill-proposals.md` (§§1, 2, 10, 11, 12, 14a, 15 read directly),
  and `/home/li/primary/flows/f6db8d/log.md`.
- Also read whole by this flow, after the date-sweep gap was found:
  `/home/li/primary/flows/5851f4/vision/` (`psycheFacingModel.md`,
  `subagents.md`, `skills.md`, `thinkingPhases.md`,
  `anatomyOfCommunicatingThinkingAndReacting.md`) and the ten other undated
  files listed in Part E.
- Witnessed by this flow directly: the `.dotos` census; the datom-codec pin
  table; `git log -S'claude-opus-5'` and `git log -S'gpt-5.6-sol'` over
  `Curriculum/roles.datom`; `orchestrate 'Observe.Locks'`; the dirty-tree
  and HEAD survey of twelve repositories; `roles.datom` read whole; the
  `user-only` frontmatter survey; the delimiter grep over the generated
  skills;
  `/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:247-248`
  with its `git log`, against `/home/li/primary/flake.nix:22,26` and the
  local Curriculum HEAD — the evidence that item 3 is a stale regeneration
  rather than a missing feature; the count of 472 flow vision/notion files
  against 186 with no date heading, and the `git log --diff-filter=A` sweep
  that recovered Part E; this agent's own available-skills listing, which is
  the evidence that item 3's gap is live.
- Witnessed by read-only subflows of this flow, each of which cited the file
  and line it read and, where stated, ran the command it reports: the signal
  estate survey; the nexus/ethos repository survey; the datom-codec vision
  check; the protos/ethos-zero vision check (including runs of the built
  `ethos-zero` binary on scratch files); the environment and component
  survey. Their findings are carried here as their claims, attributed above
  by the citation each gave.
