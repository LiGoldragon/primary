# Origins of the CriomOS Stack

Dated timeline of founding moments, with verbatim psyche words,
transcript or commit provenance, agent context clearly marked, and
inference marked as such.

---

## CriomOS--dev (the original CriomOS)

### ~2020-03-12 — first commit

No psyche quote survives from this era. The commit message style is
the living's own hand, not agent-generated:

> `(rootRebase unnecessaryHistory)`

— commit b263eeb8, /home/li/git-archive/CriomOS--dev

Agent context: CriomOS--dev is the original CriomOS repository, active
from at least 2020 through early 2026. Its readme calls CriomOS "part of
the larger Sema achievement" and "a correct runtime platform for the
Criome using linux ... an evolved version of NixOS." The cluster in this
era was named "maisiliym" and the deploy tool was `criomos-deploy`.

**Inference:** The original CriomOS, its name, and its NixOS-based
nature predate all surviving transcripts. The psyche wrote this
repository directly.

---

## CriomOS-v2 (intermediate rewrite, archived)

### 2026-03-20 — first commit

> `(("schema", "CriomOS-v2"), ("add", "jail infrastructure — WireGuard
> namespace via flake input override, NordVPN setup docs"),
> ("evolution", "fresh rewrite — composable Nix infrastructure replacing
> monolithic NixOS builder"))`

— commit ebfad652, /home/li/git-archive/CriomOS-v2

Its README says:

> CriomOS v2 — Standard runtime substrate for Criome components. Pure
> Nix infrastructure. Configuration arrives as a JSON input override —
> from samskara, from the command line, or from any source.

Agent context: CriomOS-v2 is a short-lived intermediate rewrite (only 4
commits) that replaced the monolithic builder with composable Nix
infrastructure using flake input overrides. It was itself superseded by
the current CriomOS within a month.

**Inference:** The commit message style (structured tuples) is the
agent-era format. CriomOS-v2 was likely agent-created as a rewrite
proposal, but the evolution note "fresh rewrite — composable Nix
infrastructure replacing monolithic NixOS builder" reflects the
direction the psyche was driving.

**Unknown:** No verbatim psyche quote survives for why CriomOS-v2 was
started or why it was abandoned in favor of the current CriomOS.

---

## horizon-rs (Horizon)

### 2025-03-08 — first commit

> `init`

— commit f45c70a4, /git/github.com/LiGoldragon/horizon-rs

The commit is authored by `li` with timezone +0100.

### 2025-04-23 — renamed to horizon-rs

> `rename(horizon-rs)`

— commit a62fd92d, /git/github.com/LiGoldragon/horizon-rs

Agent context: The current ARCHITECTURE.md describes horizon-rs as "The
horizon projection library. Rust types and source files for nixos
modules; consumed by Lojix's deploy projection path." Its design
document (docs/DESIGN.md) says: "horizon-rs takes a cluster proposal
(the goldragon dotos) and a viewpoint (cluster, node), and produces an
enriched horizon." The principle is "Semantic axis — WHAT, never HOW":
horizon expresses only what the psyche-as-cluster-owner wants, as simple
typed facts; Nix consumes the facts downstream.

An archived companion, `horizon-cli`, was created 2025-04-25 at
/home/li/git-archive/horizon-cli (commit e84b8a22).

**Inference:** horizon-rs was created by the living in March 2025 as a
Rust library to express cluster configuration as typed data rather than
ad-hoc Nix. It predates all surviving agent sessions. The early commits
(init, add rust-toolchain.toml, implement basic workspace) are terse
human-style messages, not agent-generated.

**Unknown:** No verbatim psyche quote survives from the founding. The
"WHAT, never HOW" principle in the current ARCHITECTURE.md was likely
written or refined by agents, though it reflects the psyche's long-held
direction.

---

## goldragon (cluster data)

### 2022-09-20 — first commit

> `(init)`

— commit 7da4ce47, /git/github.com/LiGoldragon/goldragon

### 2023-10-04 — added readme

> `(added readme)`

— commit 77a20fca

### 2026-04-23 — reseeded as production cluster data

> `(("data", "scaffold"), ("replace", "wipe experimental phonetic
> schema; reseed with current production maisiliym datom + standard
> NodeProposal flake output"), ("evolution", "goldragon becomes the
> source of truth for the LiGoldragon kriom; old experimental rename
> is abandoned"))`

— commit 87d19826

Agent context: goldragon was originally created in 2022 as an
experimental repository (possibly for phonetic schema experiments). In
April 2026 it was reseeded to become the production cluster proposal —
the source of truth for every node, user, and trust relation in the
LiGoldragon kriom. Its current ARCHITECTURE.md says: "goldragon is a
data repository only. It owns the cluster proposal — the single source
of truth for every node, user, and trust relation in the LiGoldragon
kriom."

**Inference:** The original 2022 `goldragon` repo predates agent
sessions. It was repurposed on 2026-04-23 during the canonical CriomOS
rewrite. The 2022 creation was the living's own work; the 2026 reseed
was agent-executed but aligned with the rewrite plan.

**Unknown:** No verbatim psyche quote survives for the original creation
or the 2026 repurposing decision.

---

## CriomOS and CriomOS-home (the split)

### 2026-04-23 — both repos created simultaneously

CriomOS first commit:

> `(("nix", "scaffold"), ("add", "CriomOS canonical rewrite with
> blueprint + NixOS modules + data/config + criomos-deploy +
> brightness-ctl + llama-cpp-prometheus copies from criomos-archive"),
> ("evolution", "canonical rewrite with horizon-rs as schema owner and
> CriomOS-home as home profile; network-neutral, no hosts/
> enumeration"))`

— commit eff6eea6, /git/github.com/LiGoldragon/CriomOS

CriomOS-home first commit:

> `(("nix", "scaffold"), ("add", "CriomOS-home standalone blueprint
> flake with home modules copied from criomos-archive nix/homeModule"),
> ("evolution", "split home profile into its own repo so CriomOS stays
> network-neutral and home can be consumed standalone via
> home-manager"))`

— commit 87863634, /git/github.com/LiGoldragon/CriomOS-home

The CriomOS-home README at first commit says:

> Split out from legacy CriomOS so that:
> 1. `CriomOS` stays network-neutral and free of desktop-shell inputs
>    (niri, noctalia, stylix, emacs sources, vscodium extensions).
> 2. Non-CriomOS NixOS hosts can consume the same home profile via
>    `home-manager switch --flake
>    github:LiGoldragon/CriomOS-home#<user>@<host>` once standalone
>    wiring lands.

Agent context: Both repos were created on the same day (2026-04-23) as
a "canonical rewrite" replacing the monolithic criomos-archive (the
renamed CriomOS--dev). The split separated system-level NixOS
configuration (CriomOS) from per-user home-manager configuration
(CriomOS-home). CriomOS was made "network-neutral by construction" — it
does not enumerate hosts; the horizon (external typed data) carries
host identity.

The psyche later spoke about the CriomOS/CriomOS-home relationship:

### 2026-08-24 — moving the source of commonality into a new criomos-core repo

> Then find all the commonality between the OS and home repos, then make
> a proposal on moving the source of it all in a new criomos-core repo
> which would export them as exported namespaces for criomos and
> criomos-home to use

— psyche, 2026-08-24T01:17:47+02:00, flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md

### 2026-08-25 — core is more accurate than lib

> I think core is more accurate than lib, yes, so superseding is the
> right perspective.

— psyche, 2026-08-25T14:03:52+02:00, same file

**Inference:** The CriomOS / CriomOS-home split on 2026-04-23 was
agent-executed as part of a wholesale rewrite. The rationale (network
neutrality, separation of desktop concerns) appears in the first commit
messages, not in a surviving psyche quote. The rewrite was planned — the
CriomOS README at first commit references `proposals/CRIOMOS-NEXT.md`
in the criomos-archive repo, though that file does not survive in the
archive's current state.

**Unknown:** No verbatim psyche quote survives ordering the 2026-04-23
split itself. The direction is consistent with the psyche's later
"every concept should have its repo" principle, but the specific
decision to split home from system is not traceable to a psyche ask.

---

## CriomOS-lib

### 2026-04-25 — extracted from CriomOS

> `(init): CriomOS-lib — shared helpers (importJSON, mkJsonMerge) +
> data (largeAI/llm.json) extracted from CriomOS/lib + CriomOS/data;
> consumed by both CriomOS and CriomOS-home as a flake input to remove
> the duplicate criomos-lib specialArg setup in each consumer`

— commit 68cd5445, /git/github.com/LiGoldragon/CriomOS-lib

Agent context: CriomOS-lib was extracted two days after the
CriomOS/CriomOS-home split to deduplicate shared helpers that both
repos needed. The commit message explains the engineering rationale:
both CriomOS and CriomOS-home had duplicate `criomos-lib specialArg`
setups.

**Inference:** This extraction traces to an agent's engineering
judgment, not to a verbatim psyche ask. The psyche later (2026-08-25)
ruled that "core is more accurate than lib" and that a `criomos-core`
repo should supersede CriomOS-lib.

**Unknown:** No psyche quote ordering the CriomOS-lib extraction
survives. It may have been a psyche directive given in a session that
left no transcript, or an agent's own initiative.

---

## CriomOS-pkgs

### 2026-04-27 — extracted from CriomOS

> `(init): CriomOS-pkgs — extracted from CriomOS/pkgs-flake/ to its
> own repo so CriomOS source edits don't invalidate the pkgs eval cache
> (path:./subdir keys eval cache on root flake's narHash per Tweag
> eval-cache blog — empirically observed: 0.07s cached → 0.60s after a
> README touch)`

— commit 50d8627a, /git/github.com/LiGoldragon/CriomOS-pkgs

Agent context: CriomOS-pkgs was extracted for a purely technical
reason: Nix's eval cache keys on the root flake's narHash, so any
source edit to CriomOS (even a README touch) invalidated the package
overlay cache. Splitting pkgs into its own repo kept the expensive
overlay evaluation cached across unrelated CriomOS edits.

**Inference:** This is clearly agent-initiated for eval-cache
performance. The commit message cites the "Tweag eval-cache blog" and
empirical measurements — agent reasoning, not psyche direction.

**Unknown:** No psyche quote. The living may have approved this in a
session that left no transcript, but the engineering detail in the
commit body strongly suggests agent initiative.

---

## criomos-horizon-config

### 2026-05-17 — created

> `criomos-horizon-config: add pan-horizon configuration`

— commit 1218566e, /git/github.com/LiGoldragon/criomos-horizon-config

Its ARCHITECTURE.md says:

> This repository exists so pan-horizon identity and temporary network
> facts live in their own repo rather than being smuggled onto the
> cluster-authoring surface. It authors the horizon-wide constants
> (operator identity, DNS suffixes, LAN address pool, reserved
> subdomain labels) that are NOT per-cluster — the values previously
> inlined in `goldragon/datom.nota`.

Agent context: criomos-horizon-config separates horizon-wide constants
(operator identity, DNS, LAN pool) from cluster-specific data
(goldragon). The ARCHITECTURE.md says the boundary is sharp: "a value
belongs here only if another cluster owner would author it differently,
horizon-rs cannot derive it, and it is not a CriomOS implementation
choice."

**Inference:** This separation traces to an agent's architectural
judgment during the horizon-rs deployment period. The commit message
style is agent-generated.

**Unknown:** No psyche quote ordering this separation survives.

---

## Lojix (the living dictates "Logix")

### Pre-history: samskara-lojix-contract (2026-03-16)

> `init: Datalog schema contract between Samskara and Lojix agents`

— commit 04df860b, /home/li/git-archive/samskara-lojix-contract

Agent context: The name "Lojix" appears as early as March 2026 in the
Samskara ecosystem, as a Datalog-based contract between the Samskara
knowledge base and "Lojix agents." A `lojix-macros` crate was split out
on 2026-03-24 (commit a4bfe2f2 in /home/li/git-archive/lojix-macros).
This early "Lojix" was a different system — a Datalog/CozoDB-based
agent framework, not the current deploy daemon.

### 2026-05-13 — lojix repo created (as lojix-daemon)

> `skeleton: docs-only (ARCHITECTURE, AGENTS, skills.md stub)`

— commit 67fd4544, /git/github.com/LiGoldragon/lojix

The initial ARCHITECTURE.md says:

> `lojix-daemon` is the long-lived owner of cluster deploy state. It
> receives typed deploy requests over a Unix socket (`signal-lojix`
> records), executes the build/copy/activate pipeline, observes the
> resulting cluster state, and maintains the durable substrate needed
> for cache retention and container lifecycle visibility.

> Today's `lojix-cli` is one-shot: each invocation projects horizon,
> builds, copies, activates, exits. After cutover, `lojix-cli` becomes
> a thin client; this daemon owns persistent state.

### 2026-05-14 — renamed to lojix

> `docs: rename to lojix; one-crate two-binary shape; sema-engine +
> signal-core defaults`

— commit eca194fc

### 2026-06-05 — INTENT.md added

The INTENT.md says:

> `lojix` is the new deploy stack: one crate shipping a long-lived
> deploy orchestrator daemon (`lojix-daemon`) plus a thin CLI client
> (`lojix`) that speaks the daemon over a Unix socket. It is the
> cluster-operator-owned authority for "what generation is running on
> every node right now," GC-roots retention, and the deploy event log.
> It replaces the implementation surface of the monolithic `lojix-cli`.

— commit c830eebe, /git/github.com/LiGoldragon/lojix

Agent context: The current lojix repo was created as a docs-only
skeleton on 2026-05-13, initially named "lojix-daemon", and renamed to
plain "lojix" the next day. It replaced the earlier one-shot
`criomos-deploy` / `lojix-cli` tool with a long-lived daemon.

The psyche's later words about lojix treat it as established:

> We wont use a skill called lojix; thats nonsensical. Thats what
> operating-system is for.

— psyche, 2026-08-19T22:20:16+02:00, flows/01a01bac/vision/skillDesigning.md

> we should create a lojix skill that properly documents it, and
> reference it in operating-system

— psyche, 2026-08-20T11:20:38+02:00, same file (superseding the
previous ruling)

> it must explain the syntax. dotos/datom is strict

— psyche, 2026-08-20T11:49:18+02:00, same file

**Inference:** The name "Lojix" was reused from the earlier
Samskara/Datalog ecosystem for the new deploy daemon. The current
lojix's creation appears to trace to the system-assistant design report
cited in its first ARCHITECTURE.md
(`~/primary/reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md
§P5`), which is an agent-authored plan. That report does not survive in
the current file tree.

**Unknown:** No verbatim psyche quote survives ordering the creation of
the lojix deploy daemon itself. The name "Lojix" / "Logix" predates the
current repo. No surviving transcript records the psyche's original
coinage of the name or its intended meaning.

---

## dotos (the NOTA/Dotos structural reader)

### Lineage: NOTA → nota-codec → nota-next → dotos

The data notation's line of descent:

- **NOTA** — the original name. `nota-codec` created 2026-04-27
  (commit b72dbfa7 in /home/li/git-archive/nota-codec).
- **nota-next** — the replacement implementation begun 2026-05-26 in
  what is now the `dotos` repo (first commit 0f21138d: "bootstrap
  nota-next structural reader").
- **Dotos** — the repo was renamed from nota to dotos on 2026-07-31
  (commit 1facca44: "dotos: rename the NOTA language and API surface").

### 2026-08-08 — the psyche's dissatisfaction with the name

> Signal is our messaging layer, and the CLI's role is to transform
> text into Signal. So we used to call it NOTA, now it's DOTOS. I don't
> even know if I like that new name actually. But yeah, yeah, I don't
> think it's a good name. I don't think it sticks. It's been bothering
> me for days.

— psyche, 2026-08-08T11:45:33.818Z (Designer session 55d18f4f),
/home/li/.claude/projects/-home-li-primary/55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2.jsonl:636

### 2026-08-10 — the "three stacks" and naming crisis

> So currently we have... I've made a mess because I've tried to rename
> everything. I tried to rename Noda to Dothos and now I don't like the
> name Dothos. I still prefer Noda, although... Yeah, Noda is good. But
> I think because Noda, or whatever we call it, is going to be probably
> one of the most important or famous things that I'm making at first,
> I would like the name to be really good. Noda is going to become, or
> whatever we call it, is going to become the next JSON, but bigger
> than JSON.

Speech-to-text corrections beside the quote: "Noda" = NOTA, "Dothos" =
Dotos.

— psyche, 2026-08-10T12:12Z (Designer session 13cfc23f),
flows/13cfc23f/vision/threeStacks.md

The full passage describes three stacks: "The old stack, the incorrect
new stack, and the correct new stack." The old stack uses the old names
(Schema and NOTA). The incorrect new stack has the new names (Dotos,
Ethos, Nomos, Logos, and Protos).

### 2026-08-10 — naming criteria and the Datom coinage

> people wont remember dotos, eidos or rhetos. it just wont stick at
> all

— psyche, 2026-08-10T12:44Z (Designer session c6b71b4c),
flows/c6b71b4c/vision/archive-threeStacks.md

> its data, strictly typed, super dense (no field names). something
> that echoes this

— psyche, 2026-08-10T12:53Z, same file

> what about datom
>
> ok we'll use datom, and we'll get you started with a fresh session to
> look at how we spilt [STT correction: split] those 3 stacks so make
> yourself a restart prompt

— psyche, 2026-08-10T13:53Z, same file

Agent context: After this moment, the NOTA-successor data notation is
named **Datom**. But the `dotos` repository keeps its name for the
structural reader layer — because "dotos" becomes the name for the
low-level text encoding, while "datom" names the typed data dialect on
top of it.

### 2026-08-22 — Dotos is the old syntax; Datom replaces it

> And you're saying dotos, but like that's the old syntax, which is
> being replaced by datum [STT correction: datom], which is, you know,
> has the same concept.

— psyche, 2026-08-22T17:32:33.328Z,
flows/01a02a34/vision/archive-datum.md

### 2026-08-25 — migrate to Datom

> I want to migrate curriculum stack to datom instead of dotos

— psyche, 2026-08-25T11:37:42.226Z,
flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md

### 2026-08-26 — no more Dotos files

> There should be no Dodos [STT correction: Dotos] files anymore.

— psyche, 2026-08-26T10:10:32.842Z,
flows/01a03d6e/vision/dotosFiles.md

**Inference:** The `dotos` repository name came from the NOTA → Dotos
rename on 2026-07-31, which was agent-executed. The psyche never liked
the name "Dotos" — they said it "won't stick" and coined "Datom" to
replace it as the name for the data notation. The `dotos` repo remains
as the low-level structural reader, but the psyche's direction is that
Datom is the forward name.

---

## datom (the data dialect)

### 2026-08-10 — named by the psyche

> what about datom

— psyche, 2026-08-10T13:53Z, flows/c6b71b4c/vision/archive-threeStacks.md

### 2026-08-11 — the psyche rules datom is a renamed dotos, not a new repo

> datom is just a renamed dotos, so there was no need to create a new
> repo. unless I missed something.

— psyche, 2026-08-11T13:53+02:00 (Designer session 012fbf07),
flows/012fbf07/vision/archive-threeStacks.md

### 2026-08-11 — datom does not generate Rust

> datom doesnt generate rust. ethos does. so I dont know what youre
> trying to say there, but its a dangerous line, and should be rooted
> out, wherever you got tha idea

— psyche, 2026-08-11T00:39+02:00, same file

### 2026-08-11 — datom and ethos are different languages sharing a substrate

> no, I dont think so. they share an approach, but are different
> languages. they could have a shared substrate (traits with a shared
> implementation and types)

— psyche, 2026-08-11T14:06+02:00, same file

### 2026-08-11 — datom repo created

> `datom: initial Datom text serialization and deserialization codec`

— commit 3c5c6f26, 2026-08-11T12:18:20+02:00,
/git/github.com/LiGoldragon/datom

Agent context: Despite the psyche ruling that datom should be a renamed
dotos (not a new repo), a separate datom repo was created. The distilled
Vision/datom.md says: "Datom is the psyche's own coinage for the new
data notation, the successor to NOTA and to the rejected name Dotos.
The name was chosen for its energetic power and to echo what the
notation is: data, strictly typed, super dense, no field names."

The distilled vision continues: "Datom carries data only — like JSON,
but strictly typed. Generics belong to Ethos; Datom's whole work is
serialization and deserialization — carrying data between text and typed
form." And: "Everything migrates to Datom. Datom's own line of descent
is NOTA — which also passed through the temporary name Dotos; that old
notation stays behind, frozen, and may be called legacy."

**Observation:** The psyche ruled "datom is just a renamed dotos, so
there was no need to create a new repo" — but a new repo was created
anyway. This may reflect an agent's judgment that the dotos repo
carried too much legacy structure, or a later psyche directive not
captured in the transcripts.

---

## The three stacks and the vision for the engine

### 2026-08-08 — everything is in the daemon

> Everything is in the daemon. So this is my vision from the very
> beginning. ... You have the Ethos daemon, the Nomos daemon. I mean,
> they're just called Ethos, Nomos, and Logos. Those are the name of
> the repositories. They're all daemons. The same architecture as all
> my other components, right? There's the daemon, there's a CLI,
> there's a CLI for the metasocket. Everything is signal messages,
> meaning RKYV binary messages. That's what signal means.

— psyche, 2026-08-08T11:12:45.472Z (Designer session 55d18f4f),
flows/55d18f4f/vision/everythingIsInTheDaemon.md

### 2026-08-08 — recovery and the component shape

> im too angre [STT correction: angry] to read all this right now. do
> a major recovery effort right now. I want the repos to be called
> ethos nomos and logos
>
> they will each have a signal-XXX and meta-signal-XXX repo, which will
> hold the ethos describing the types of the messaging layer, which we
> call signal, and always have.
>
> we can still have a core-XXX repo for each, if you think that wise or
> useful, otherwise all the logic can live in the main repo.

— psyche, 2026-08-08T11:21:29.377Z,
flows/55d18f4f/vision/majorRecoveryEffort.md

### 2026-08-11 — three repos per component

> I dont know if we need a core-* repo. I dont see much point. so
> ethos can have all the code, minus the two signal repos, and so on
> (3 repos per component). other than reusable libraries of course,
> which we want to encourage for shared traits especially.

— psyche, 2026-08-11T00:39+02:00,
flows/012fbf07/vision/archive-threeStacks.md

---

## Summary of traceable psyche founding asks

| Component | Psyche ask? | Evidence |
|---|---|---|
| CriomOS--dev | Yes — the living wrote this directly | Commit style, 2020 origin |
| horizon-rs | Yes — the living created this directly | Human-style commits, Mar 2025 |
| goldragon | Yes — the living created this directly | 2022 origin |
| CriomOS (canonical) | Unknown — agent-executed rewrite | No psyche quote for the decision |
| CriomOS-home | Unknown — agent-executed split | No psyche quote for the split |
| CriomOS-lib | No traceable psyche ask | Agent-initiated extraction |
| CriomOS-pkgs | No traceable psyche ask | Agent-initiated for eval cache |
| criomos-horizon-config | No traceable psyche ask | Agent-initiated separation |
| lojix | Unknown — agent-planned | Name predates the deploy daemon |
| dotos | Agent-renamed from NOTA | Psyche disliked the name |
| datom | Yes — psyche coined the name | "what about datom" (2026-08-10) |

---

## Sources

### Git repositories (first commits)

- `/git/github.com/LiGoldragon/horizon-rs` — f45c70a4, 2025-03-08
- `/git/github.com/LiGoldragon/lojix` — 67fd4544, 2026-05-13
- `/git/github.com/LiGoldragon/goldragon` — 7da4ce47, 2022-09-20
- `/git/github.com/LiGoldragon/criomos-horizon-config` — 1218566e, 2026-05-17
- `/git/github.com/LiGoldragon/CriomOS-lib` — 68cd5445, 2026-04-25
- `/git/github.com/LiGoldragon/CriomOS-pkgs` — 50d8627a, 2026-04-27
- `/git/github.com/LiGoldragon/dotos` — 0f21138d, 2026-05-26
- `/git/github.com/LiGoldragon/datom` — 3c5c6f26, 2026-08-11
- `/git/github.com/LiGoldragon/CriomOS` — eff6eea6, 2026-04-23
- `/git/github.com/LiGoldragon/CriomOS-home` — 87863634, 2026-04-23

### Archived repositories

- `/home/li/git-archive/CriomOS--dev` — b263eeb8, 2020-03-12
- `/home/li/git-archive/CriomOS-v2` — ebfad652, 2026-03-20
- `/home/li/git-archive/horizon-cli` — e84b8a22, 2025-04-25
- `/home/li/git-archive/nota-codec` — b72dbfa7, 2026-04-27
- `/home/li/git-archive/samskara-lojix-contract` — 04df860b, 2026-03-16
- `/home/li/git-archive/lojix-macros` — a4bfe2f2, 2026-03-24
- `/home/li/git-archive/github.com/LiGoldragon/criomos-archive` — b263eeb8, 2020-03-12

### Psyche vision records

- `flows/13cfc23f/vision/threeStacks.md` — three stacks discussion
- `flows/c6b71b4c/vision/archive-threeStacks.md` — Datom naming
- `flows/012fbf07/vision/archive-threeStacks.md` — repo anatomy, datom vs ethos
- `flows/55d18f4f/vision/everythingIsInTheDaemon.md` — daemon architecture vision
- `flows/55d18f4f/vision/majorRecoveryEffort.md` — component shape
- `flows/55d18f4f/vision/signalIsOurMessagingLayer.md` — Signal and NOTA/DOTOS naming
- `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md` — criomos-core
- `flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md` — migration to Datom
- `flows/01a03d6e/vision/dotosFiles.md` — no more Dotos files
- `flows/01a01bac/vision/skillDesigning.md` — lojix skill
- `flows/01a02a34/vision/archive-datum.md` — datom replaces dotos
- `Vision/datom.md` — distilled Datom vision

### Claude transcripts

- `~/.claude/projects/-home-li-primary/55d18f4f-ea0b-43d8-88ae-f8f4bd3027d2.jsonl` — Designer session 55d18f4f (2026-08-08)

### Other

- `protocols/repos-manifest.dotos` — authoritative repo inventory
- CriomOS first-commit README referencing `proposals/CRIOMOS-NEXT.md` (not found in current archive state)
