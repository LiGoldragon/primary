# 703 — System-Operator Brief: kameo fleet + first-cluster hosts

Designer-lane synthesis for the **system-operator** lane. Two parts, each
with a firm lean (the psyche delegated these "with your leans"). Frame
each as *proceeding with X unless the psyche redirects*.

Both parts were re-verified against the on-disk `/git/github.com/LiGoldragon`
checkouts on 2026-06-19. Part 1's verified state **differs from the 702
framing** in an important way (the divergent repo is `lojix`, not
spirit/mirror) — the correction is in §1.1, and it makes the fix sharper,
not larger.

## Part 1 — kameo fleet: one runtime, witness-first

### 1.1 Verified state (corrected)

The 702 framing said *"criome/router/mentci use the LiGoldragon fork;
spirit/mirror default to stock 0.20.0 via triad-runtime; spirit's lock
carries both."* On-disk verification overturns the spirit/mirror half:

**Every triad/runtime repo except one resolves to the fork.** Across all
`Cargo.lock` files under `/git/github.com/LiGoldragon`, there is exactly
**one** distinct git kameo source — the LiGoldragon fork at
`f491b45d7dcb55e5837eddde3d5d7ca8ceaa9f01` (52 lock references, the rev
the prompt names). spirit, mirror, criome, router, triad-runtime, cloud,
mind, persona, harness, message, terminal, and the rest all pin
`git = "github.com/LiGoldragon/kameo.git", branch = "main"`, and
`branch = "main"` currently resolves to that fork rev. `kameo` itself is
version `0.20.0` on the fork (the fork is a patch series *on top of* the
0.20.0 tree, not a version bump): tip `f491b45` *"fix lifecycle fork after
upstream rebase"*.

**spirit and mirror are clean.** Neither pins kameo directly; both reach
it transitively through `triad-runtime` (`spirit` → `triad-runtime`
`branch = "main"`; `mirror` → `triad-runtime` `branch = "main"`).
triad-runtime `0.6.1`'s own `Cargo.toml` pins the fork, and spirit's
`Cargo.lock` resolves kameo + kameo_macros to the fork f491b45 with **one**
source line each — it does **not** carry two kameo entries. The
"spirit's lock carries both" observation does not reproduce against the
current tree (it may have been true mid-transition during operator-431 and
has since converged).

**The real split-brain is `lojix`.** Exactly one repo pins stock kameo:

| | pin in `Cargo.toml` | resolves to |
|---|---|---|
| `lojix` | `kameo = "0.20"` | **stock** `registry+…crates.io` 0.20.0 |
| all 24 others | `git = …LiGoldragon/kameo.git, branch = main` | fork `f491b45` |

The mechanism is the subtle part, and it is a genuine correctness hazard,
not a cosmetic pin difference. `lojix` depends on **both**
`kameo = "0.20"` (registry) **and** `triad-runtime` (`branch = "main"`,
whose own tree pins the fork). Cargo's version-unification picks one
`kameo` for the build graph: because the direct `kameo = "0.20"` registry
dep is semver-compatible with the fork's `0.20.0`, the **registry source
wins**, and triad-runtime's `"kameo"` dependency edge is unified onto
stock. The proof is in `lojix/Cargo.lock`: it contains **zero** references
to `f491b45` — its only `kameo`/`kameo_macros` entries are
`registry+…crates.io`, even though triad-runtime `0.6.1`
(`f46f66e`) sits right there in the same lock depending on `"kameo"`.
So `lojix` (and its `triad-runtime` actors) compile against stock kameo
while everyone else compiles against the fork.

This matters operationally because **lojix is a deployed daemon**:
`lojix-daemon` is the new deploy-orchestrator daemon, smoke-deployed to
`zeus` (system-operator report 220), with `[[bin]]` targets
`lojix-daemon`, `lojix`, `meta-lojix`, `lojix-write-configuration` and a
repo-local `flake.nix` (the 220 "no repo-local flake" caveat is now
resolved). lojix's lifecycle/shutdown semantics are exactly what the fork
patches change (the fork tip is literally *"fix lifecycle fork after
upstream rebase"*, and the prior commits gate weak-shutdown helpers, split
the lifecycle-control mailbox, and publish terminal lifecycle outcomes).
A deploy daemon running a *different* actor-lifecycle implementation from
the rest of the fleet is precisely the kind of latent divergence the fork
exists to remove.

**Deployed graph is unwitnessed.** No Nix evaluation has been run to
report the resolved kameo rev per built daemon. The lock-file evidence
above is the source-tree truth; what is *actually deployed* on
prometheus/zeus is inferred from those locks, not proven by a witness.
That gap is exactly what Step 1 closes.

### 1.2 The lean — witness first, then everyone onto the fork f491b45

**Recommendation:** proceed witness-first.

1. Run a Nix fleet witness that reports the resolved kameo rev per built
   daemon — turn the inferred graph into a proven one **before** changing
   any pin.
2. Then unify: make `lojix` consume the fork (drop the stock
   `kameo = "0.20"`), so the whole fleet builds the single fork rev.
3. Add a hard CI gate so a second kameo source can never re-enter.

Rationale for the order: the lock evidence is strong but the *deployed*
artifacts on prometheus/zeus are unproven. Bumping pins before witnessing
risks "fixing" a graph we never measured and masking a second divergence
we did not know about. Witness, then change, then re-witness to prove the
change took.

Rationale for the destination (fork, not stock): the fork is not optional
polish. It carries router's and lojix's actor-lifecycle/shutdown
corrections, intent record `zk6y` ("schema-emitted engines are kameo
actors") and `96mi`/`ilxh` (only real kameo actors get actor naming)
make actor density a standing requirement, and 24 of 25 repos already
build the fork. Unifying *down* to stock would regress the lifecycle
fixes across two dozen repos to spare one. Unify *up*.

### 1.3 Step 1 — the Nix fleet witness (no `/nix/store` filesystem search)

Hard rule (`AGENTS.md`): no `/nix/store` filesystem search. Resolve the
rev through evaluation / metadata / a derivation that exposes it, never by
grepping the store.

Three layers, cheapest first:

**(a) Source-of-truth witness — `Cargo.lock` per daemon, via `nix eval`.**
The lock pins the rev; that is the build input. Expose, per daemon repo,
the kameo source line as a flake-readable value so `nix eval` reports it
without building:

```
# In each daemon flake (lojix shown; mirror/spirit/criome/router analogous):
#   packages.<system>.kameo-rev = a derivation (or eval-time value) that
#   reads ./Cargo.lock and extracts the kameo source rev.
nix eval --raw .#kameo-rev          # -> f491b45… expected; lojix -> registry (the bug)
```

Implement the extractor as a tiny derivation that `grep`s the *checked-in*
`Cargo.lock` (an input file, not the store): `runCommand` over
`./Cargo.lock` selecting the `name = "kameo"` source line. This is
`nix eval`/derivation-exposed, store-search-free, and works offline.

**(b) Built-artifact witness — `nix path-info` / dependency closure.** For
the daemons that are actually built and deployed (`lojix-daemon`, and the
triad daemons once they ship), prove the *built* closure references the
fork, not just the lock. Build the daemon derivation and read its inputs
via `nix path-info --json .#daemon-binary` / `nix-store --query
--references` on the **derivation path** — derivation/eval introspection,
never a store filesystem walk.

**(c) Fleet roll-up — one derivation, `flake show` discoverability.**
Add a `checks.kameo-fleet-witness` (or a `packages.fleet-kameo-report`)
that aggregates each daemon's `kameo-rev` into a single report and
`assert`s they are all the one fork rev. `nix flake show` surfaces it;
`nix flake check` runs it.

Witness output to capture in the system-operator report: for each daemon
repo, `{ repo, lock-rev, expected = fork f491b45, status }`. Expected
pre-fix result: every repo `OK` **except `lojix` = `registry (stock)`**.

### 1.4 Step 2 — pin unification (the one-repo change)

The fix is one repo, because the divergence is one repo.

- **`lojix/Cargo.toml`:** drop `kameo = "0.20"`. lojix already depends on
  `triad-runtime` (`branch = "main"`), which transitively provides the
  fork kameo; lojix's direct kameo usage should come through
  triad-runtime, or, if lojix genuinely needs a direct kameo dep, pin it
  to the fork: `kameo = { git = "…/kameo.git", branch = "main" }` (matching
  every sibling). Either way the registry source disappears from the build
  graph.
- **Re-lock:** `cargo update -p kameo` (or regenerate the lock) so
  `lojix/Cargo.lock`'s kameo/kameo_macros entries become the fork
  `f491b45`, with **zero** `registry+…crates.io` kameo lines remaining.
- **Re-witness:** rerun §1.3(a)/(c). lojix must flip `registry` → `OK`.
- **Build + test:** `nix flake check` on lojix (its flake already has
  `build`, `daemon-binary`, `test`, `clippy`, `fmt`, and the
  NOTA-startup-rejection check). The fork's changed lifecycle/shutdown
  surface is the risk zone — if lojix's daemon lifecycle tests or the
  `daemon_binary_socket_roundtrip_eval` smoke regress under the fork, that
  is a *real* finding to report, not something to paper over. Report
  PartialGreen with the exact failing test and cargo output rather than
  faking green.

**Optional hardening (worth doing while in here):** the active-repositories
truth-pin notes that `branch = "main"` floats. Once the fleet is unified,
consider pinning kameo to the explicit rev (`rev = "f491b45d…"`) fleet-wide
instead of `branch = "main"`, so a fork push cannot silently re-fan the
fleet onto an unwitnessed rev. This is a separate, larger change (touches
all 24 repos) — flag it, do not block the lojix fix on it. The CI gate
(§1.5) is the cheaper guarantee.

### 1.5 Step 3 — the hard CI gate

Make a second kameo source structurally impossible to re-introduce:

- **Per-daemon flake gate:** the `checks.kameo-rev` extractor from §1.3(a)
  becomes a *check*, not just a value — it `assert`s the lock's kameo
  source is the fork and fails `nix flake check` otherwise. lojix's flake
  already has a `checks` set; add the assertion there and to each triad
  daemon flake as they gain one.
- **Fleet gate:** `checks.kameo-fleet-witness` (§1.3c) is the single
  cross-repo gate — it fails if *any* enumerated daemon's resolved kameo
  is not the one fork rev. Wire it into whatever runs `nix flake check`
  in CI for the deploy stack.
- **Lint the toml, not just the lock:** a grep-gate that fails if any
  workspace `Cargo.toml` declares `kameo = "<version>"` (registry form)
  instead of the git fork form catches the divergence at the *source*
  before it reaches a lock. Cheap belt-and-suspenders.

### 1.6 Production relevance (per Spirit `xhwa` + `9s52`) — does this block deploy?

**No — but it constrains it.** Spirit record `xhwa` (the
production-deploy decision, High certainty) is explicit: the near-term
production milestone is the **1-of-1 local** authorization case —
*spirit* asks its **co-resident local criome** daemon to authorize the
content-addressed head; a single local signature suffices to gate
propagation; *"quorum authorization and the multi-machine cluster from
`jk1w` are the subsequent step, not a prerequisite."* So deploy does **not**
block on the multi-machine cluster (Part 2).

But the same record co-locates spirit + a local criome daemon on one host,
and the propagation chain is spirit → criome → router → mirror. **All
four co-reside and must agree on the actor runtime.** Per the verified
state, those four already resolve to the fork (spirit/mirror via
triad-runtime, criome/router directly) — so the near-term 1-of-1 deploy is
**already coherent** on the kameo runtime. The kameo work is therefore
*not* a blocker for the 1-of-1 spirit+criome production deploy; it is a
blocker for cleanly bringing **lojix** (the deploy orchestrator itself)
and the eventual cluster onto a single witnessed runtime. Sequence
accordingly: the witness + lojix unification can proceed in parallel with,
and need not gate, the 1-of-1 deploy — but lojix should be unified before
it is relied on to orchestrate that deploy, so the deploy tool and the
daemons it deploys share one actor runtime.

`9s52` (criome is per-Unix-user; Low certainty) bears on *which* criome
co-resides: the "co-resident local criome" in `xhwa` is the user's **home
criome** under li's Unix user, peering with a host-scoped **system
criome** for host facts — not a shared multi-user daemon. The runtime
coherence requirement applies to whichever criome instance spirit talks
to locally; both home and system criome are fork-resolved today.

## Part 2 — first-cluster hosts (for the eventual `jk1w` cluster)

Scope: this is the **multi-machine cluster** (Spirit `jk1w` — a running
multi-machine criome cluster, near-term goal, the *subsequent* step after
the 1-of-1 deploy). It is **not** the near-term 1-of-1 production deploy
of Part 1 / `xhwa`. A 2-of-3 quorum needs three hosts.

### 2.1 Verified host inventory

Source: `goldragon/datom.nota` (the production cluster proposal — header:
*"production cluster proposal for the LiGoldragon kriom… Production data
for every node"*; consumed by `horizon-rs` via `horizon-cli`). Five
**system nodes** (criome-capable hosts) and two **user nodes**. Decoded
per the `horizon-rs ClusterProposal` schema (Class, then size/criome
tier, then `Metal`, etc.):

| Host | Class | Hardware | IPv6 / tailnet | Roles / notes |
|---|---|---|---|---|
| **prometheus** | `LargeAiRouter` (Max/Max) | GMKtec EVO-X2 x86_64, 8-core, **128 GB** | tailnet `5::5/128`, has Wi-Fi router config (primary + backup SSID) | The AI router; named `prometheus.goldragon.criome`. `NixBuilder(6)` + `NixCache`. The fleet's heaviest box + the router. |
| **ouranos** | `EdgeTesting` (Large/Max) | ThinkPad T14 Gen5 Intel x86_64, 12-core, 32 GB | tailnet `5::3/128`, full tailnet identity + DERP coords | li's primary dev/laptop. `TailnetController` + `TailnetClient` + `NixBuilder` + `PersonaDevelopment[GitoliteServer]`. The tailnet controller and gitolite host. |
| **zeus** | `Edge` (Max/Max) | ThinkPad T14 Gen2 Intel x86_64, 4-core, 12 GB | tailnet identity present, no `5::x` reserved addr | The lojix-daemon smoke-deploy target (report 220). General edge node. |
| **tiger** | `EdgeTesting` (Max/Max) | ThinkPad E15 Gen2 Intel x86_64, 4-core, 12 GB | tailnet `5::4/128` | Edge testing node, `NixBuilder`. Has a secondary data disk. |
| **balboa** | `Center` (Zero/Min) | rock64 **Arm64**, 4-core, SD-card root | no IPv6/tailnet reserved addr, criome tier **Min** | Smallest node (SD-booted ARM SBC), lowest criome tier. Not a cluster-quorum candidate. |

User nodes (not cluster hosts): **bird** (Multimedia) and **li**
(Unlimited, the operator persona). These are persona/user records, not
criome quorum nodes.

So: `zeus` is the ThinkPad T14 Gen2 edge node and the existing lojix
deploy target; the additional hosts the prompt asked me to find are
`balboa` (ARM SBC), `ouranos` (the T14 Gen5 dev box + tailnet controller +
gitolite), and `tiger` (the E15 edge-testing node). `prometheus` is the
big AI-router box.

Caveat: `goldragon/datom.nota` is a **proposal** ("cluster proposal",
"has not been cut over to any node" per active-repositories §deploy-stack).
It is the authoritative *intended* inventory, not a witness that all five
are currently up and reachable. The system-operator should confirm
liveness (tailnet reachability, current generation) before committing
the three.

### 2.2 home/system criome split (per Spirit `9s52`)

The prompt asks whether the first cluster is *three hosts* or a
*home/system-criome split*. Spirit `9s52` (Constraint) settles the
**axis**, though at Low certainty: criome is **per-Unix-user**. Each user
runs their own **home criome** with their own key custody; there is **no
single shared system criome multiple users connect to**. The privileged
**system criome** tier (from `9qm8`) is for **host-scoped system services
under a service user** — a user's home criome *peers* with it for
host-level facts; it is not a multi-user shared daemon.

These are **orthogonal axes, not alternatives:**

- The **home/system split** is a *per-host* split: on each host there can
  be a system-criome (host-scoped, service user) and li's home-criome
  (user-scoped, li's custody) peering with it. This is the local trust
  boundary, present on a single host too.
- The **three-host cluster** is the *quorum membership* axis: which
  criome **principals' nodes** form the 2-of-3 quorum.

`p3td` reconciles them under one primitive: *"Each principal runs more
than one node and asks its own quorum… a self-quorum across one's own
nodes is a reliability mechanism."* So the first cluster's purpose is a
**self-quorum of li's own nodes** — li runs criome on three hosts and the
2-of-3 makes li's attestations and timestamps credible against
single-node compromise — **and** on each host the home/system split is the
per-host trust boundary. The right framing for the brief: *three hosts*
**carrying** li's home-criome quorum, with each host also running its
host-scoped system-criome that the home-criome peers with. It is not
either/or.

### 2.3 The lean — proceed with prometheus + ouranos + zeus as the first 2-of-3

**Recommendation:** form the first 2-of-3 cluster from
**prometheus**, **ouranos**, **zeus**, unless the psyche redirects.

Rationale, in priority order:

1. **prometheus** — mandatory anchor. 128 GB, the `NixCache` + `NixBuilder`,
   the AI router, the always-on infra box, and the only host the prompt
   named explicitly (`prometheus.goldragon.criome`). It is the natural
   "more available, more powerful" quorum member that should almost always
   be reachable — the right host to weight a self-quorum toward.
2. **ouranos** — the `TailnetController` and `GitoliteServer`, 32 GB,
   12-core, li's primary dev box with a full reserved tailnet identity
   (`5::3/128` + DERP coords). It is the host with the richest networking
   identity and the one that already controls the tailnet the quorum
   signs over. Highest-availability laptop in the fleet.
3. **zeus** — the existing **lojix-daemon deploy target** (report 220), so
   the deploy path to it is already exercised; it has a full tailnet
   identity and is an `Edge` (Max/Max) node. Choosing zeus means the first
   cluster member after the two infra anchors is the one host we have
   already pushed a daemon to.

Why these over the alternatives:

- **tiger over zeus?** tiger (`5::4/128`, E15 Gen2, also Max/Max) is a
  strong fourth and an equally valid third. I lean zeus because the deploy
  path to zeus is already proven (220) — fewer unknowns for the *first*
  cluster bring-up. Hold tiger as the immediate 3→4 / hot-spare expansion
  and the obvious member if zeus proves flaky.
- **balboa excluded.** ARM SD-card SBC at criome tier **Min**,
  Zero/Min sizing, no reserved tailnet addr — not a quorum-grade node.
  Keep it as a `Center`-class leaf, not a quorum member.
- **Why three of the five, not all five for the first bring-up?** `jk1w`
  wants a *running* multi-machine cluster soon; 2-of-3 is the smallest
  real quorum that tolerates one node down (matching `p3td`'s
  reliability-via-self-quorum intent). Start with the three most-available,
  best-understood hosts; expand to 5 (adding tiger then balboa-as-leaf or
  a 2-of-5/3-of-5) once the 2-of-3 is witnessed healthy.

**Proceeding with prometheus + ouranos + zeus (2-of-3) unless the psyche
redirects** — with tiger as the designated first expansion node. Each host
runs li's home-criome (quorum member) alongside its host-scoped
system-criome per `9s52`; the three-node quorum is a self-quorum of li's
own nodes per `p3td`, not a cross-principal trust set yet.

### 2.4 Sequencing note tying Part 1 and Part 2

`jk1w` is explicit that the **single-host causal loop is the prerequisite
foundation** and the cross-machine enablers follow. So the order is:
(1) the 1-of-1 spirit+local-criome production deploy (`xhwa`, Part 1 §1.6,
already kameo-coherent); (2) the lojix unification + fleet witness (Part 1)
so the deploy orchestrator and the daemons share one runtime; (3) the
2-of-3 cluster bring-up on prometheus/ouranos/zeus (Part 2). Part 2 should
not start before the fleet is witnessed on one runtime — you cannot cluster
a fleet running two actor runtimes, and the witness is what proves it is
one.

## Quick reference — what to do

| # | Action | Owner | Blocks |
|---|---|---|---|
| 1 | Build the Nix kameo-rev witness (eval/derivation, no store search): per-daemon `kameo-rev` + fleet roll-up | system-operator | nothing — do first |
| 2 | Run the witness; capture `{repo, lock-rev, status}`; expect all `OK` except `lojix = registry` | system-operator | the fix |
| 3 | `lojix/Cargo.toml`: drop `kameo = "0.20"`, take the fork via triad-runtime (or direct git pin); re-lock | system-operator | re-witness |
| 4 | `nix flake check` lojix on the fork; report any lifecycle/shutdown regression honestly (PartialGreen, exact test) | system-operator | gate |
| 5 | Add the per-daemon + fleet CI gate (assert single fork rev) + a toml-lint against registry kameo | system-operator | — |
| 6 | Confirm prometheus/ouranos/zeus liveness; bring up the 2-of-3 self-quorum (each host: home-criome member + system-criome peer); tiger = first expansion | system-operator | after fleet witnessed |

Open question for the psyche (Part 2): `9s52` is **Low** certainty. Confirm
the home-criome (li's user) + system-criome (service user) per-host split
is the intended deployment shape before standing up three hosts each
running two criome instances, vs. a simpler one-criome-per-host first cut.
The lean above assumes the split per `9s52`/`p3td`; a one-criome-per-host
first cut is a reasonable simpler start if the psyche prefers it.
