# 274 - Forge skeleton reconciliation (existing crates vs. `/271`'s family plan)

*Designer reconciliation, 2026-05-21. Closes the substantive gap
`/272` §4e named in `/271`: the family-design sketch was filed
without naming the existing `forge` and `signal-forge` skeletons in
the LiGoldragon org. New substance; `/271` does not need a v2.*

## 1. The gap

`/271` sketched a forge family — `forge-core` /
`forge-nix-builder` / per-component forges / eventual
`workspace-content-store` — as the workspace's emerging
build-system layer that eventually replaces Nix. The sketch is
substantively sound, but it filed two false absences:

- The `forge` crate already exists in the org
  (`/git/github.com/LiGoldragon/forge`) as a skeleton-as-design
  daemon. Latest commit `8c1ef63` (2026-04-29).
- The `signal-forge` crate already exists in the org
  (`/git/github.com/LiGoldragon/signal-forge`) as a layered
  contract atop `signal-frame`. Latest commit `87882b6`
  (2026-05-20, three-layer-model alignment).

Both crates predate the schema-migration and forge design thread
(now spanning intent record 21, /263, /270, /271, /273) by weeks. The
gap is not corrective of `/271`'s direction — the family plan is
still right — it is corrective of `/271`'s naming surface. The
existing crates are load-bearing context the sketch missed.

## 2. What the existing skeletons are

### 2a. `forge` (the daemon)

`Cargo.toml` description verbatim:

> `forge — the executor daemon. Receives effect-bearing signal
> verbs over UDS from criome; links prism; runs nix; writes into
> arca.`

`ARCHITECTURE.md` role framing (verbatim):

> The forge daemon — the executor. Takes plan records from
> criome (via signal verbs over UDS), links `prism` to emit
> Rust source, runs nix, writes artifacts into `arca`, reports
> outcomes back.

The pipeline: criome (planner) → forge (executor) → nix
subprocesses → `~/.arca/_staging/` → arca-daemon → canonical
`~/.arca/<store>/<blake3>/`.

Actor tree (from `src/lib.rs` + `src/actors/`): NixRunner (spawns
nix), StoreWriter (RPATH rewrite + deterministic timestamps,
writes to arca staging), ArcaDepositor (presents criome-signed
capability token to arca-daemon via signal-arca's Deposit),
FileMaterialiser (projects arca entries into a working dir).

README status banner is explicit about non-overlap with current
lojix deploy work:

> **Not the lojix deploy daemon.** GitHub redirects
> `LiGoldragon/lojix` → `LiGoldragon/forge` because this repo was
> renamed. … forge is a separate concern.

Status: skeleton-as-design; all actor bodies are `todo!()`. Lands
when criome scaffolds and is ready to forward effect-bearing
signal verbs.

### 2b. `signal-forge` (the wire contract)

`Cargo.toml` description verbatim:

> `signal-forge — layered protocol crate atop signal. Carries the
> criome ↔ forge wire (Build, Deploy, store-entry operations)
> using signal's Frame, handshake, and auth. Skeleton-as-design.`

`ARCHITECTURE.md` §1 channel boundary: criome produces requests,
forge consumes them and replies. §2 contract operations: `Build`
(BuildRequest payload carrying records + criome-signed capability
token), `Deploy` (DeployRequest for nixos-rebuild), and a deferred
`StoreEntry*` family (likely migrates to `signal-arca` when that
crate lands). All `Mutate`-classified at the Sema layer.

The contract is already three-layer-aligned (commit `87882b6`,
2026-05-20): layer-1 wire verbs are contract-local; layer-2
ForgeCommand enum lives in the forge daemon; layer-3 Sema
classification is projection-only.

§7 framing of why-layered (verbatim opening):

> **Audience-scoped compile-time isolation.** The criome ↔ forge
> leg has a narrow audience — criome (sender), forge (receiver),
> lojix-cli (transitional sender of deploy verbs).

### 2c. The pre-thread framing

The existing skeletons describe forge as **the criome-stack
executor**: a daemon that runs effects (nix builds, deploys, arca
deposits) that criome cannot perform directly. The wire contract
carries effect-bearing verbs on one specific authority leg.

This is the "executor of cross-cutting effects for the
sema-ecosystem" framing — not the "workspace's build-system
family" framing of `/271`. The existing forge is a single daemon,
not a family. It wraps Nix, but only as one of several effects.

## 3. Where the existing skeletons fit in `/271`'s family map

`/271` §2 declared the family shape:

```
forge-core/               contract standardisation point
forge-nix-builder/        first concrete forge — wraps Nix
forge-<component>/        per-component forges
workspace-content-store/  eventual; replaces Nix's store + substitution
```

### 3a. `forge` (existing) vs `forge-nix-builder` (`/271`)

The existing `forge` daemon is the closest match to `/271`'s
`forge-nix-builder`. Both are concrete (not abstractions), both
wrap Nix straight up. But they are not identical:

- `/271`'s `forge-nix-builder` is "the first concrete forge — the
  persona-system layer above Nix" — generic, owns
  `Build(BuildPlan)`-style operations.
- Existing `forge` is "the criome-stack executor" — bound to
  criome as authority root, includes deploy (`nixos-rebuild`)
  and arca deposit alongside build.

`/271`'s map does not have a slot that includes deploy and arca
deposit. Those are real effects the existing forge already owns.

### 3b. `signal-forge` (existing) vs `forge-core` (`/271`)

`/271` §6 frames `forge-core` as "the standardisation point for
the family" — typed contract types (`BuildPlan` / `BuildResult` /
`ContentAddress` / `BuildHost` / `Substitution`), probably a
pure-library leg.

The existing `signal-forge` is NOT the family standardisation
point. It is the criome ↔ forge wire contract — narrow audience,
specific channel, layered atop `signal-frame`. Its §7 frames its
purpose as "audience-scoped compile-time isolation".

Existing `signal-forge` is the wire contract for one specific
authority leg. `/271`'s `forge-core` is the universal vocabulary
the whole family agrees on. Different concerns, different levels.

### 3c. What `/271`'s plan adds the existing skeleton lacks

- A standardisation layer (`forge-core`) where the family agrees
  on what a build *is*, independent of who is asking.
- Per-component forges converging into `forge-core` over time.
- An eventual workspace-owned content-addressed store.
- A trajectory: forge takes over from Nix piece by piece.

### 3d. What the existing skeleton has that `/271` missed

- A concrete authority-root model (criome signs; forge runs;
  arca-daemon takes ownership).
- An actor decomposition for the daemon.
- A capability-token discipline on the criome → forge wire.
- An explicit non-overlap with the lojix deploy daemon.
- Three-layer-model alignment already on the wire contract.

`/271` foreshadowed most of these implicitly (the carve-outs in §4
push signing to the content store, authentication to Criome) but
does not engage with the concrete authority chain the existing
skeletons already declare.

## 4. The reconciliation path

**Recommendation: Path A — reframe the existing skeletons as the
first family members under `/271`'s plan.**

### 4a. Why Path A

The existing skeletons are not pre-thread experimental dross. They
are a coherent, three-layer-aligned sketch of one specific forge
slice — the criome-stack executor — with a clear authority model.
This is exactly the kind of concrete forge `/271` §7 describes as
a per-component forge: a wrapper that carries component-specific
policy on top of a universal vocabulary.

Path B (retire and start fresh) would discard:

- A three-layer wire contract already migrated to current
  discipline.
- An actor decomposition that already correctly carves arca
  ownership out of the build layer (matching `/271`'s carve-out
  philosophy in §4).
- A clear authority-root pattern (criome signs the capability
  token) that `/271` does not yet have an answer for.

The existing skeletons are not orthogonal to `/271`'s vision; they
are an instance of it, with one specific authority root (criome).

### 4b. Reframing under `/271`'s map

| Existing | `/271`'s family slot | Justification |
|---|---|---|
| `forge` (the daemon) | A per-component forge for criome's authority chain. Sibling to other concrete forges that may emerge later. | The daemon is bound to criome as authority root; `/271` says per-component forges exist initially and converge on `forge-core` later. |
| `signal-forge` (wire contract) | The criome ↔ forge wire — one specific authority leg. Layered atop `signal-frame`. | The contract's audience is criome + forge + transitional lojix-cli; that is one authority leg, not the universal vocabulary. |

The crates keep their names. Their existing framing is correct
for their slot.

### 4c. What `/271`'s plan adds on top

| New (per `/271`) | Relative to existing |
|---|---|
| `forge-core` | NEW crate. Pure-library standardisation point. The existing `signal-forge`'s `Build` payload eventually carries `forge-core::BuildPlan` instead of an inline records-list. |
| `forge-nix-builder` | NEW crate, OR the existing `forge` daemon refactors its NixRunner actor out as an embeddable nix-builder library. Cleanest path: NEW crate that existing `forge` depends on; existing forge becomes thin policy ("criome authority + arca deposit on top of forge-nix-builder"). |
| Other per-component forges | NEW crates, as other authority chains emerge (e.g. a forge bound to persona-orchestrate rather than criome). |
| `workspace-content-store` | NEW crate (eventual). For now arca-daemon and `~/.arca/` cover the role. |

### 4d. What does NOT change

`signal-forge`'s three-layer alignment; the criome → forge
capability-token mechanism; the arca staging → arca-daemon deposit
pattern; the existing forge's actor decomposition; either crate's
name.

## 5. Implications for `/271`

**`/271` does not need a v2.** Its direction stands. This report
extends `/271` rather than corrects it. The gap was the missing
inventory of existing crates, not a flaw in the family plan.

- `/271` §2's family map is unchanged in shape — only its
  population gets clarified.
- `/271` §3 (eternal Nix abstractions) is undisturbed.
- `/271` §4 (carve-outs) is undisturbed; the existing skeletons
  already match this discipline.
- `/271` §5 (forge-nix-builder) is the place this report
  sharpens: the first concrete forge is plausibly the existing
  `forge` daemon with `forge-nix-builder` extracted as a library.
- `/271` §9 question one ("is forge-core a triad or
  pure-library?") becomes easier to answer once the existing
  `signal-forge`'s pattern is named as a per-leg contract —
  `forge-core` likely carries no daemon, just typed vocabulary.

A pointer from `/271` to `/274` is the only cross-link needed; no
text in `/271` is wrong.

## 6. Open psyche questions

1. **Does the existing `forge` daemon stay as the criome-stack
   executor, with `forge-nix-builder` extracted as a library?**
   Or does the existing daemon become the new `forge-nix-builder`,
   with criome policy moving to a thin wrapper above it? Both are
   coherent. Recommend the first (less rename churn).

2. **Does the `Deploy` verb stay in `signal-forge`, or migrate
   out?** `/271` does not name deploy as a forge concern. The
   existing `signal-forge` carries `Deploy` alongside `Build`. If
   forge owns build but not deploy, `Deploy` migrates to
   `signal-lojix` or a sibling. The existing skeleton's framing
   reads broader than `/271`'s.

3. **Is `forge-core` actually needed as a separate crate, or does
   the existing `signal-forge` evolve to carry the standardisation
   vocabulary directly?** Path A leans toward a NEW `forge-core`
   pure-library; `signal-forge` then carries
   `forge-core::BuildPlan` as the `Build` payload. But if there is
   ever only one concrete forge, the indirection is overhead.

4. **Does the workspace-owned content-addressed store (`/271` §8)
   consume or replace the existing arca-daemon / `~/.arca/`?** The
   arca pattern already implements content-addressing via blake3
   and staging-then-deposit. If that store IS the workspace's
   content-addressed store eventually, `/271` §8 lands
   incrementally inside arca-daemon rather than as a new crate.

5. **Should intent records for the forge family land on disk
   before further design work?** `/271` flagged record-locations
   for the forge decision and content-addressed-store decision as
   `recent` but unresolved on disk; `workspace.nota` (inspected
   end-to-end) does not carry them. The dispatch to write `/274`
   referenced "record 74 — forge family decision; record 75 —
   content-addressed-store decision" but those records are not in
   `workspace.nota`. Either the numbering is forward-looking or
   the records have not been committed. Future designer work has
   a substrate gap to close before drafting `forge-core`'s
   contract.

## See also

- `reports/designer/271-forge-component-family-design.md` — the
  exploratory family sketch this report extends.
- `/git/github.com/LiGoldragon/forge/ARCHITECTURE.md` — existing daemon's framing.
- `/git/github.com/LiGoldragon/signal-forge/ARCHITECTURE.md` — existing wire contract.
- `skills/component-triad.md` — the universal shape both
  existing crates already follow.
- `skills/contract-repo.md` §"The layered pattern" —
  `signal-forge` exemplifies this; `forge-core` would formalise
  it across legs.
