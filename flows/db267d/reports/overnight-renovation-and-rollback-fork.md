# The overnight renovation, the arch defect, and the rollback fork

Investigation only. Nothing was changed, built, pushed or deployed.

## Answer in one line

The psyche is right. `8cda3bab` is not a slip — it is renovation code from flow
`542442`, written against a **Horizon projection schema that exists only on an
unmerged `horizon-rs` branch**, landed directly on `CriomOS-home` `main`, and
dragged into production this afternoon by an unrelated repin.

## Observations

### 1. The renovation exists, and `8cda3bab` is part of it

Flow `542442` ("Node variants, external Horizon configuration, and Datom stack
migration") ran through the night of 2026-09-05/06. Its work lives in three
repositories:

| Repository | Renovation lands where |
|---|---|
| `horizon-rs` (the **producer**) | `origin/horizon-datom-node-542442` only — **not on main**. `main` last moved 2026-08-13. |
| `CriomOS` (the OS **consumer**) | `origin/horizon-flake-integration-542442` (15 commits, 09-05 23:19 → 09-06 08:11) and `origin/horizon-module-consumer-fix-542442` — **not on main**. |
| `CriomOS-home` (the Home **consumer**) | **directly on `main`**, commits `b12e3dc` (00:03) through `654144d` (03:35). Only after `654144d` did the flow branch off (`home-horizon-shape-542442`: `978bb65`, `be20529`, `e71729e`). |

The seven `CriomOS-home` `main` commits are:

```
b12e3dc 00:03  Consume Horizon user vectors in Home
4bac7ce 00:22  Read Horizon Home gates from projected capabilities
ad20d95 00:28  Pin corrected Orchestrate migration
8cda3ba 00:54  CriomOS-home: read projected machine architecture
a464fd7 00:56  CriomOS-home: align Horizon test fixtures
0808afc 01:08  CriomOS-home: repair Horizon isolation fixtures
654144d 03:35  CriomOS-home: pin current Chroma Datom producer
```

`8cda3bab` sits in the middle of that run. It is renovation work.

### 2. How it reached production — the exact mechanism

`CriomOS` `main` pinned `criomos-home` as follows:

| CriomOS main commit | time | criomos-home pin |
|---|---|---|
| `57ec0138` | 09-05 23:55 | `08717ef8` — the **last pre-renovation** Home revision |
| `a48f9cb` (Drop Claude Remote Control) | 09-06 16:59 | `1ae5da86` |
| `1a2ce02` | 09-06 17:01 | `ceeaaf4272ea` |
| `37149c31` | 09-06 17:06 | `fde8a2d2` |

`CriomOS` `main` had **no commits at all** between 09-05 23:55 and 09-06 16:59.
Production therefore ran on Home `08717ef8` — clean of the renovation — right up
until this flow's own Claude-Remote-Control repin at 16:59, which advanced the
Home pin past all seven renovation commits in a single step.

This corrects the brief's framing: the arch defect did not break deployments
"from 00:56 onward". It broke the **first** deployment that consumed it, at
16:59 today, because this flow's unrelated repin was the first thing to pull the
overnight Home line into the OS.

### 3. The defect is a schema mismatch, not a typo — and it is not isolated

The producer on `horizon-rs` **main** (`lib/src/machine.rs:12-13`,
`lib/src/species.rs:129-135`) emits, via `#[serde(rename_all = "camelCase")]` on
`Machine` and **no** rename on `enum Arch`:

```
node.machine.arch = "X86_64"
```

The producer on `origin/horizon-datom-node-542442` (`lib/src/projection.rs:135`)
instead declares `pub architecture: String`. And the unmerged `CriomOS` branches
read `machine.architecture` with value `"x86_64"` lowercase.

So `8cda3bab`'s `node.machine.architecture == "x86_64"` is **exactly the new
schema**. It was correct code for a producer that is not deployed.

Three further consumer reads on `CriomOS-home` `main` are against the same
absent schema:

| Site on `CriomOS-home` main | Reads | `horizon-rs` main emits | Effect today |
|---|---|---|---|
| `modules/home/profiles/min/spirit.nix:25` (from `4bac7ce`) | `horizon.node.capabilities or [ ]` | `Node` has **no `capabilities`**; it has `services: Vec<NodeService>` (`lib/src/node.rs:54`) | **Silent live regression.** `isPersonaDevelopment` is now permanently `false` on every node. No error — the `or [ ]` swallows it. |
| `flake.nix` `homeUsers` (from `b12e3dc`) | `map (rawUser: …) horizon.users` — treats `users` as a **vector** | `Horizon.users: BTreeMap<UserName, User>` (`lib/src/horizon.rs:22`) — an **attrset** | `map` over an attrset is a Nix type error. Reachable through the `homeConfigurations` flake output (not the OS module path), so it does not break deploys but does break that output. |
| `lib/horizon-user.nix` (from `b12e3dc`) | `rank.${raw.size}` (string enum), `raw.publicKeys` (list of `{node,ssh,keygrip}`), `raw.hasPublicKey`, `raw.sshPublicKey`, `raw.resolvedTextSize` | `size: AtLeast {min,medium,large,max}` attrset; `pubKeys: BTreeMap`; `hasPubKey`; `sshPubKey`; `textSize` | Entirely new-schema. Same reachability as above. |

**Answer to question 2: it is not an isolated slip.** Four distinct consumer
sites on `main` read the new schema. `8cda3bab` was merely the only one that
failed *loudly*, because a missing attribute on the module path is a hard
evaluation error while the others are guarded by `or` defaults or sit behind a
lazy flake output.

### 4. A residual defect this flow's own fix left behind

`a464fd7` ("align Horizon test fixtures") rewrote two check fixtures from
`horizon.node.machine.arch = "x86-64"` to `horizon.node.machine.architecture =
"x86_64"` — i.e. the overnight flow moved the *fixtures* to match its wrong
consumer rather than checking the producer. This flow's `fde8a2d2` fixed the
consumer but **not** the fixtures. They still read, on `main` today:

- `checks/ai-agent-launch-orchestration/default.nix:25` — `horizon.node.machine.architecture = "x86_64";`
- `checks/yt-dlp/default.nix:47` — `horizon.node.machine.architecture = "x86_64";`

Those fixtures now supply no `machine.arch` at all to a consumer that reads
`machine.arch`. Either those checks fail, or they never reach line 240 — I did
not run them, so I do not know which.

Note also: the *pre-renovation* line was `node.machine.arch == "x86-64"`, which
the producer never matches either (`"X86_64"`). It was wrong before the
renovation too — just harmlessly, silently declining to install `i7z`.
`8cda3bab` converted a silent wrong comparison into a fatal missing attribute.

### 5. `checks/lojix-ownership` — yes, same renovation

Three-way mismatch on `CriomOS` `main`:

| Value | Revision | Set by |
|---|---|---|
| `expectedOrchestrateRevision` (`checks/lojix-ownership/default.nix:11`) | `9585484738ce…` (Orchestrate 0.27.0) | stale since 09-04 |
| root `flake.lock` `orchestrate` | `5f016531e765…` (0.30.0) | `CriomOS 57ec0138`, 09-05 23:55 |
| `criomos-home` `flake.lock` `orchestrate` | `ac8a92666f4a…` | `CriomOS-home ad20d95`, 09-06 00:28 |

Both moves are flow `542442`'s. Its log records them: *"Orchestrate 0.30.0 is on
main at 5f016531e765; owning pins landed in CriomOS-home 08717ef8950e and
CriomOS 57ec0138e28d"* (line 54) and *"The remaining catalog preflight ordering
was corrected at main ac8a92666f4a"* (line 62).

**The complete fix already exists on the unmerged branch.** On
`origin/horizon-flake-integration-542442`, commits `add8a44` ("make Lojix
ownership fixture match projected keys") and `82f6bf5` ("align ownership fixture
Home pin") set `expectedOrchestrateRevision = "ac8a92666f4a…"` and move the root
lock to `ac8a9266` — root, Home and expectation all agree there. Main is broken
solely because the Home half landed and the OS half did not.

### 6. What flow 542442 itself said

Its log's final checkpoint: *"CriomOS de02 and Home e717 remain frozen; no
product source change followed these fixture findings."* Line 73: *"The frozen
CriomOS integration candidate `6d6aa72d…` includes module consumer fixes
`8bbc75d3…`, Home `0808afc5…`, Lojix `d4404aad…`, Orchestrate `ac8a926…`, and
Horizon `05879e7c…`."*

So the flow regarded the Home commits — including `0808afc`, which is on `main`
— as part of a **frozen candidate**, coherent only in combination with the
CriomOS branch, the Horizon branch and the Lojix/Orchestrate pins. It gated the
combination behind branches on the OS side. It did not gate the Home side,
because `CriomOS-home` is consumed by pin and the flow only pinned it into its
own CriomOS *branch*.

I found no statement anywhere that the flow knew a third party would repin
`CriomOS-home` `main` into the OS. I did not reach the `transcript` tool (not on
PATH in this environment), so this rests on the flow log, which is a first-hand
flow record, not on the raw transcripts.

## Hypotheses (labelled as such)

- **H1.** The flow's working model was "Home main is safe to write to, because
  nothing consumes it until a CriomOS commit pins it." That model held for
  seventeen hours and was invalidated by an unrelated repin. I have no direct
  statement of this model; it is inferred from the branch/main split at
  `654144d`.
- **H2.** The remaining new-schema reads (`capabilities`, `horizon.users` as a
  vector, `lib/horizon-user.nix`) are currently masked rather than fixed. I have
  not evaluated `nix flake check` on `CriomOS-home` `main` to confirm which of
  them actually fail.

## Unknowns

- Whether the two stale fixtures (§4) currently fail. Not run.
- Whether `nix flake check` on `CriomOS-home` `main` passes at all.
- Whether any behaviour other than `isPersonaDevelopment` silently changed.
- Whether flow `542442` is still live and would be disrupted by a rollback of
  `CriomOS-home` `main`.

## The fork

Last pre-renovation `CriomOS-home` `main` revision: **`08717ef8950e514c346cbdfbc69143e4369056fb`**
("Pin Orchestrate framed Datom Signals", 09-05 23:55) — the exact revision
`CriomOS 57ec0138` pinned and the last one production ran before today.

### Option A — roll `main` back to `08717ef8` and move the renovation to a branch

What is removed: the seven renovation commits. What must be re-landed on top:
this flow's three fixes.

Separability, checked file-by-file:

- `1ae5da86` (Claude Remote Control removal) — touches
  `checks/claude-remote-control/`, `modules/home/profiles/min/claude-remote-control.nix`,
  `flake.nix`, `modules/home/default.nix`, docs. **Cleanly separable.** Its
  `flake.nix` and `modules/home/default.nix` hunks are in different regions from
  the renovation's.
- `ceeaaf4272ea` (Claude Desktop asar unpack + self-contained local-binary
  override) — `owned-agents/claude-desktop/*`, `checks/claude-desktop-*`.
  **Fully disjoint from the renovation. Cleanly separable.**
- `fde8a2d2` (the arch fix) — **not separable, and not wanted.** Its only hunk
  is `min/default.nix:240`, a line that exists in its current form *because of*
  `8cda3bab`. Rolling back restores `node.machine.arch == "x86-64"`, i.e. the
  pre-renovation silent mismatch. Nothing to re-land; the line reverts to its
  old, harmless-but-wrong state.

Also lost by the rollback: `ad20d95`'s Orchestrate bump to `ac8a9266`, which
returns Home's lock to `5f016531` — matching the root lock. That does **not**
fix `checks/lojix-ownership`, whose expectation (`9585484`) is stale against
both. It reduces the three-way mismatch to a two-way one.

Cost: two cherry-picks (or a revert of the seven commits with the two fixes
preserved), a `CriomOS` repin, and a rebase of `home-horizon-shape-542442` onto
the new `main` so flow `542442` keeps a coherent line.

Risk: low mechanically. The real risk is disrupting flow `542442` if it is still
running against Home `main` ancestry.

Gain: removes the silent `isPersonaDevelopment` regression, the broken
`homeConfigurations` output, the new-schema `lib/horizon-user.nix`, and the
stale fixtures — all at once, and returns `main` to a state that is *known* to
have run in production.

### Option B — keep `main` and fix forward

Cost, the actual list:

1. `min/spirit.nix:25` — restore the `services`-based `isPersonaDevelopment`
   gate (revert `4bac7ce`'s spirit hunk), or the PersonaDevelopment profile
   stays off everywhere.
2. `flake.nix` `homeUsers` / `lib/horizon-user.nix` — revert to
   `mapAttrs mkHomeConfiguration horizon.users`, or delete
   `lib/horizon-user.nix` and the vector mapping.
3. `checks/ai-agent-launch-orchestration` and `checks/yt-dlp` — fixtures back to
   `machine.arch = "X86_64"`.
4. `CriomOS checks/lojix-ownership` — either bring the root lock to `ac8a9266`
   and set `expectedOrchestrateRevision` to it (what branch commits `add8a44` /
   `82f6bf5` already do), or roll Home's lock back.

That is, fixing forward means individually undoing most of what the renovation
put on `main` anyway — plus keeping the `min/default.nix` line at the *correct*
`arch`/`"X86_64"` value, which is Option B's one genuine advantage over a
rollback.

Risk: medium. Each item is a separate decision made under time pressure, and
item 1 is invisible until someone notices PersonaDevelopment is off. The
enumeration above is mine and may be incomplete — §"Unknowns" applies.

### Recommendation

**Option A, with one amendment.** Roll `CriomOS-home` `main` back to
`08717ef8`, replay `1ae5da86` and `ceeaaf4272ea` on top, then — separately and
deliberately — set `min/default.nix:240` to `node.machine.arch == "X86_64"`,
which is correct against the deployed producer and was never correct before.
Move `b12e3dc..654144d` onto `home-horizon-renovation-542442` and rebase
`home-horizon-shape-542442` onto it, so flow `542442` loses nothing.

Reasoning: the renovation is a coherent three-repository change (`horizon-rs`
projection, `CriomOS` modules, `CriomOS-home` modules, plus the Orchestrate and
Lojix pins) that flow `542442` explicitly froze as a *combination*. Two thirds
of that combination are on branches. Landing one third on `main` is what
produced the outage, and it is still producing at least one silent regression
and one broken flake output. Fixing forward would leave the same one-third-
landed shape in place and merely patch its visible edges. The rollback restores
a known-good production line and lets the renovation land whole, once
`horizon-rs` `main` carries the new projection.

The amendment matters because a bare rollback would silently reinstate the
`"x86-64"` mismatch, and this flow now knows the right value.

**This is the psyche's call, not mine.** Both options are mechanically small;
they differ in what state `main` is left describing.

## Sources

- `git log`, `git show`, `git merge-base` in `/git/github.com/LiGoldragon/CriomOS-home`,
  `/git/github.com/LiGoldragon/CriomOS`, `/git/github.com/LiGoldragon/horizon-rs`
  (all read-only, working trees at their current HEADs on 2026-09-06).
- `horizon-rs` `lib/src/machine.rs:12-13`, `lib/src/species.rs:129-135`,
  `lib/src/horizon.rs:16-23`, `lib/src/node.rs:31-76`, `lib/src/magnitude.rs:61-66`,
  `lib/src/user.rs:15-58` (producer, `main`).
- `horizon-rs` `origin/horizon-datom-node-542442:lib/src/projection.rs:135`
  (producer, unmerged renovation branch).
- `CriomOS-home` `modules/home/profiles/min/default.nix:240`,
  `modules/home/profiles/min/spirit.nix:25`, `flake.nix` `homeUsers`,
  `lib/horizon-user.nix`, `checks/ai-agent-launch-orchestration/default.nix:25`,
  `checks/yt-dlp/default.nix:47`.
- `CriomOS` `checks/lojix-ownership/default.nix:7-11,199-200`; `flake.lock`
  `orchestrate` and `criomos-home` nodes at `57ec0138`, `a48f9cb`, `1a2ce02`,
  `37149c31`; `origin/horizon-flake-integration-542442` commits `add8a44`,
  `82f6bf5`, `de02ef1`.
- `/home/li/primary/flows/542442/log.md` lines 54, 62, 73, 253, and final
  checkpoint paragraph — first-hand flow record of flow `542442`, not
  independently verified against its transcripts.
- A delegated read-only subagent performed the CriomOS-side consumer census and
  the unmerged-branch schema comparison; its schema findings on
  `horizon-datom-node-542442` and on `machine.arch` casing were re-checked
  directly against source by me.
- Not established: no Nix evaluation, build, check or deployment was run.
