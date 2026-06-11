# Lojix / Horizon / CriomOS — Situation Analysis

*system-designer · 2026-06-11 · light survey of the deploy stack: what the
repos are, which does what, how they fit together.*

> **Correction (same session, follow-up to a psyche challenge):** the clean
> two-stack A/B framing below is substantially wrong, and the tell was
> exactly what the psyche caught — *the arc is named after horizon, yet
> horizon-rs has no fork.* See **§Correction: the rewrite never forked
> horizon** before trusting the A/B table. Short version: the horizon half
> of the rewrite already shipped on `main` and is **in production**; only
> the *lojix daemon* still lives on a parallel fork.

## TL;DR

These repos are **the CriomOS deploy stack** — the machinery that turns a
human-authored cluster description into a built, activated NixOS host. The
defining fact is that **two versions of this stack coexist**:

- **Stack A (production today).** A single monolithic CLI — `lojix-cli` —
  links `horizon-rs` in-process, projects a cluster proposal, writes a few
  override flake inputs, and runs `nix` against `CriomOS`. No daemon, no
  wire contract. This is what runs on every node. **Production fixes go
  here.**
- **Stack B (lean rewrite, smoke-built, not deployed).** The deploy logic
  becomes a long-lived `lojix-daemon` + a thin `lojix` CLI client, talking
  over a typed Signal wire (`signal-lojix` / `meta-signal-lojix`), with the
  pan-horizon constants split into their own `criomos-horizon-config` repo.
  Built end-to-end on `zeus` through `prometheus`, but **cut over to no
  node**. **Rewrite edits go here** (`horizon-leaner-shape` branch).

`horizon-rs` and the `CriomOS*` family are **shared** — the same OS layer
and the same projection library serve both stacks. Only the *driver* (CLI
monolith vs daemon+thin-client) and the *config split* differ between A
and B.

The one thing not to do: fold one stack into the other piecemeal. The
schemas have diverged; cutover is a coordinated multi-repo merge after the
rewrite reaches parity.

## Correction: the rewrite never forked horizon — it shipped on main

The psyche's instinct was right: *"the whole thing started as a horizon-rs
rewrite, so something went really wrong if horizon doesn't have a fork."*
Horizon-rs has no fork. There is no `horizon-leaner-shape` branch for it —
local or origin. But the diagnosis is not "the rewrite was lost." It is
that **the arc decomposed into two independently-shipping streams, and only
one of them is the parallel stack.** The forensic trail:

| Arc repo | `horizon-leaner-shape` fork? | Where its rewrite went | In production now? |
|---|---|---|---|
| **horizon-rs** | **No** (main only, local+origin) | `main` — NodeServices, service-variant projection, nota-next codec migration | **Yes** — prod builds horizon-rs `48df4bd` (the nota-next codec) |
| **lojix-cli** | **No** (main only) | `main` — `fc2ff02` *"migrate lojix-cli to nota-next"* | **Yes** — CriomOS lock pins `fc2ff02` |
| **goldragon** | **No** (main only) | `main` — pan-horizon constants still inline in `datom.nota` | **Yes** |
| **CriomOS / -home** | **No** (`next` = operator integ., no leaner-shape) | `main`/`next` | **Yes** |
| **CriomOS-lib** | **No** (main only) | `main` | **Yes** |
| **lojix** (daemon) | **Yes** — `~/wt/.../lojix/horizon-leaner-shape` (+ `horizon-re-engineering`) | the fork | **No** — smoke-built |
| **signal-lojix** | **Yes** — worktree | the fork | **No** |
| **meta-signal-lojix** | net-new on `main` | `main` (new repo) | **No** — only the daemon consumes it |
| **criomos-horizon-config** | net-new on `main` | `main` (new repo) | **No** — horizon-rs main doesn't reference it; constants still inline in goldragon |

**The pin chain that proves production already drank the rewrite:**
`CriomOS` flake.lock → `lojix-cli@fc2ff02` (*"migrate lojix-cli to
nota-next"*) → its `Cargo.lock` → `horizon-rs@48df4bd` (*"migrate proposal
codec to nota-next"*). And `lojix-cli/Cargo.toml` declares
`horizon-lib = { git = ".../horizon-rs" }` with **no rev/branch** — it
floats to horizon-rs `main`.

So the two streams are:

1. **Horizon schema + codec modernization** — the part literally about
   *horizon*. Rolled forward on **`main`** in horizon-rs, lojix-cli, and
   goldragon, and **shipped into production** through the pin chain. No fork,
   because a library doesn't need one — you protect consumers with version
   pins, not branches. **This is correct evolution, and it's done and live.**
2. **The lojix daemon reshape** — monolith CLI → daemon + thin client +
   typed Signal wire. The *only* thing on a parallel fork, in exactly two
   repos (`lojix`, `signal-lojix`), smoke-built, not deployed. This stream
   has nothing to do with horizon schema.

**Consequences for the docs.** `protocols/active-repositories.md` claims
Stack B *"spans the same six repos plus two new ones, all on the
`horizon-leaner-shape` branch in worktrees"* and that Stack A is the
pre-rewrite monolith with *"no daemon, no `lojix` repo, no
`criomos-horizon-config`"* pinning lojix-cli at `4c66b8a6fa55`. Reality:
(a) only two repos forked; the six "shared" repos have no leaner-shape
branch at all; (b) production is **already on nota-next** (`fc2ff02`), not
the pre-rewrite shape; (c) the pin advanced to `fc2ff02`. The branch name
**`horizon-leaner-shape` is a misnomer** — the horizon is already lean and
in prod; the fork is really *lojix-daemon-shape*. The genuinely-unshipped
horizon piece is the **`criomos-horizon-config` constants split**, which
never wired into horizon-rs main (constants still inline in
`goldragon/datom.nota`).

**The open question I won't infer (§For your attention #1 below).** Whether
this is *map-stale-territory-fine* or *territory-breached* depends on psyche
intent I don't have.

## The cast — which repo does what

| Repo | What it is | Stack | Status |
|---|---|---|---|
| **lojix-cli** | Production deploy CLI (monolith). Reads one NOTA request, projects horizon in-process, writes override flakes, runs `nix`. | A | **Deployed.** Pinned into the CriomOS graph. Retires after cutover — does *not* grow into a daemon client. |
| **lojix** | The Stack-B replacement: one crate, two binaries — `lojix-daemon` (long-lived deploy orchestrator) + `lojix` (thin CLI client). | new-in-B | Implemented crate under `triad-port/`, smoke-built. In-memory store; durable backing pending. |
| **signal-lojix** | Working-signal wire contract: deploy + retention + watch verbs the CLI/clients exchange with the daemon. Pure contract crate. | new-in-B | Implemented. rkyv + NOTA round-trip witnessed. |
| **meta-signal-lojix** | Owner-only **meta policy** contract: privileged `Deploy`/`Pin`/`Unpin`/`Retire` over the owner socket. | new-in-B | Builds clean. Wire-only, no behavior. |
| **horizon-rs** | The **projection library**. Owns the `ClusterProposal`/`NodeProposal` schema and projects it to a per-`(cluster,node)` view. Linked in-process. | **shared** | **CANON, active on both stacks.** Two crates: `lib/` + `cli/`. |
| **criomos-horizon-config** | Tiny pan-horizon constants repo (operator identity, DNS suffixes, transitional LAN block). Split out of `goldragon/datom.nota`. | new-in-B | Single 367-byte `horizon.nota`. Complete for its scope. |
| **CriomOS** | The **NixOS OS layer**. Network-neutral `nixosConfigurations.target`; identity enters only as projected flake inputs. Never built directly. | A (shared host) | **Deployed / CANON.** Also the cluster meta-repo. |
| **CriomOS-home** | Home-Manager profile flake (min/med/max). User desktop: Niri, theming, editors, Spirit user service. | A (shared host) | **Deployed / CANON.** Bakes Spirit's rkyv startup archive at build time. |
| **CriomOS-lib** | Dependency-free shared Nix lib (constants, `fetchHfModel`, model catalog). | support | Stable, shrinking by design. No INTENT.md yet. |
| **CriomOS-pkgs** | The `pkgs` axis — does the one expensive `import nixpkgs` with overlays, cached independently. | A infra | Live infra flake. No INTENT.md/ARCHITECTURE.md yet. |
| **CriomOS-emacs** | Emacs distribution as a home-manager module, split out for independent versioning. | support | Scaffold (Phase 0). Legacy `mkEmacs` not yet converted. |

## How it fits together

```mermaid
flowchart TB
  subgraph authored["Authored truth (human writes this)"]
    datom["goldragon/datom.nota<br/>cluster proposal"]
    hcfg["criomos-horizon-config<br/>horizon.nota — pan-horizon constants<br/>(Stack B only)"]
  end

  horizon["horizon-rs<br/><b>projection lib</b><br/>ClusterProposal → per-(cluster,node) view<br/>SHARED, linked in-process"]

  subgraph stackA["Stack A — PRODUCTION (running on every node)"]
    cli["lojix-cli<br/>monolith: project + write flakes + run nix"]
  end

  subgraph stackB["Stack B — LEAN REWRITE (smoke-built, not deployed)"]
    thin["lojix (thin CLI)"]
    daemon["lojix-daemon<br/>live generation set · GC-roots · event log"]
    sig["signal-lojix<br/>(read/watch)"]
    meta["meta-signal-lojix<br/>(owner: deploy/pin/retire)"]
    thin -- "ordinary socket" --> daemon
    thin -. "owner socket" .-> daemon
    sig --- daemon
    meta --- daemon
  end

  subgraph os["CriomOS host platform (SHARED)"]
    criomos["CriomOS<br/>network-neutral nixosConfigurations.target"]
    home["CriomOS-home"]
    pkgs["CriomOS-pkgs"]
    clib["CriomOS-lib"]
    emacs["CriomOS-emacs"]
    criomos --> home & pkgs & clib
    home --> emacs
  end

  datom --> horizon
  hcfg --> horizon
  horizon --> cli
  horizon --> daemon
  cli -- "writes horizon/system/deployment<br/>override inputs, runs nix" --> criomos
  daemon -- "same projection, daemon-driven<br/>(intended future writer)" --> criomos
```

The deploy mechanism, in one breath: **a cluster proposal in NOTA →
projected by `horizon-rs` into a per-node view → that view written as
override flake inputs (`horizon` / `system` / `deployment`) → `nix` builds
`CriomOS.nixosConfigurations.target` → activate.** Stack A does all of
this inside one CLI process; Stack B splits the "write inputs + run nix"
half behind a daemon and puts the request on a typed wire. CriomOS itself
is identical to both — it holds no node names and renders whatever the
projected inputs say.

The four content-addressed input axes into CriomOS — `system`, `pkgs`,
`horizon`, `deployment` — each cache independently in the nix flake-eval
cache, which is why CriomOS can iterate its module tree without re-evaluating
the costly nixpkgs instantiation (`CriomOS-pkgs`'s whole reason to exist).

## Production vs development intent, distilled

- **Production intent is "keep Stack A correct and untouched by the
  rewrite."** `lojix-cli` is the deploy entry point; `horizon-rs` is the
  CANON typed proposal boundary that stops the cluster owner from
  authoring the operating system; `CriomOS`/`-home`/`-pkgs`/`-lib` are the
  live host platform. All explicitly transitional — *built rightly for
  today's Nix stack, not as a draft of the eventual.*
- **Development intent is the triad shape.** The rewrite's thesis: deploy
  is a **component triad** — `lojix` (daemon + its first client, the thin
  CLI) + `signal-lojix` (working signal) + `meta-signal-lojix` (meta
  policy). Push-not-poll observation, authority-tiered sockets (ordinary
  read socket vs owner mutation socket with kernel-vouched peer creds),
  operator-sovereign (the daemon never self-initiates a deploy).
  Notably, **lojix is explicitly *not* a Persona component** — so the
  usual Tap/Untap observable block doesn't apply; observation stays as
  domain-specific `Watch`/`Unwatch`.
- **`horizon-rs` stays a linked-in-process library in both stacks** — the
  daemon is not a "horizon daemon." Its constants split out to
  `criomos-horizon-config` only in Stack B so the daemon takes config as
  binary.

## For your attention

0. **Was production *meant* to be on nota-next already? (intent, please.)**
   Two readings of "no horizon fork," and the code can't tell me which:
   - **(A) Map stale, territory fine.** Horizon-rs is a library; rolling it
     forward on `main` and deliberately bumping the production lojix-cli pin
     to the nota-next migration (`fc2ff02`) was the plan. Only the *daemon*
     needs a parallel stack. → the two-stack doctrine doc is just
     over-described and stale; I correct it, no alarm.
   - **(B) Territory breached.** Production was supposed to stay frozen on
     the pre-rewrite horizon until a coordinated multi-repo cutover, and the
     floating `horizon-lib = { git }` dependency + a pin bump leaked the
     nota-next rewrite into production *ahead* of that cutover. → a real
     process breach, and the unpinned git dep is a latent hazard regardless.

   I lean **(A)** — the production commits are deliberately named migration
   commits (`fc2ff02` *"migrate lojix-cli to nota-next"*), not an accidental
   float — but I won't infer it. Which is it? Either way, the unpinned
   `horizon-lib` git dependency is worth a rev-pin so production can't drift
   to horizon-rs main on the next `cargo update`.

1. **The cutover gate is durable storage + safe activate in the daemon.**
   The `lojix-daemon` runs on an in-memory store behind a shared lock; the
   named next step is durable redb/`sema-engine` backing, and *activating*
   deploys still self-reject until copy/activate is target-safe. Until
   those land, Stack B can build but can't safely deploy — which is exactly
   why it's smoke-built-not-cutover. This is the real blocker, not parity
   of the wire contracts (those are implemented).

2. **A pin-fact in our protocols doc is stale.** `protocols/active-repositories.md`
   (and AGENTS-adjacent context) says *"CriomOS and CriomOS-home flake locks
   pin `lojix-cli` at `4c66b8a6fa55`."* The actual locks now read
   `fc2ff0287f53` — the lock advanced, and `lojix-cli` reaches CriomOS as a
   **transitive** input via `criomos-home`, not a direct `flake.nix`
   declaration. The pin in the doc is a frozen snapshot, not current truth.
   Worth a one-line correction to the protocols doc — flag before I touch it
   since it's an operator/system-operator-adjacent surface.

3. **Three repos have no `INTENT.md`** — `CriomOS-lib`, `CriomOS-pkgs`,
   `CriomOS-emacs`. Per the workspace rule, a missing `INTENT.md` is "the
   first gap to fill." These three are support/infra, so the gap is low-
   stakes, but if we want the intent layer complete across the stack, they
   are the three open slots.

4. **`CriomOS-emacs` is the least-built leg** — Phase 0 scaffold, legacy
   `mkEmacs` not yet converted to a blueprint package, `homeModules.default`
   still an empty aggregate. Tracked by beads `emacs-plb` / `emacs-y55` /
   `home-tl6`. Not on the deploy critical path, but it's the one repo here
   that isn't actually doing its job yet.

## Method

Eleven sub-agents read one repo each (`INTENT.md` → `ARCHITECTURE.md` →
`AGENTS.md`/`README` heads) and returned structured summaries; this report
synthesizes them. Source frame and per-repo returns: workflow
`wf_6561ae56-9f1`. No Spirit capture — the prompt was a task-only order
(produce an analysis), not durable intent.
