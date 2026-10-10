# Dependency survey — what the deployed estate runs on, and what it is behind

Read-only subflow of main flow f6db8d. Brief: survey only; nothing upgraded,
nothing committed, no lock touched. Everything below marked **witnessed** was
read or run by this flow on this machine at 2026-09-11; **relayed** means it
comes from another flow's report or another agent's account and was not
re-observed here. Comparisons against upstream are **offline only**: no network
was used, so "behind upstream" is established either from the crates.io index
cache (`~/.cargo/registry/index/index.crates.io-1949cf8c6b5b557f/.cache`,
freshest entry 2026-09-11 14:18 — witnessed) or from another local checkout that
already pins a newer revision of the same input. Where neither exists, the
distance is stated as **unknown**.

---

## 0. What "in use" means here

Witnessed. The deployed set was taken from three places and then confirmed
against the running machine:

- `/git/github.com/LiGoldragon/CriomOS/flake.lock` — 23 root inputs.
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock` — 78 root inputs.
- `/home/li/primary/flows/857335/reports/release-registry.json` — 10 releases.

Confirmed running, witnessed via `systemctl --user`/`systemctl` and
`show -p ExecStart`:

| unit | resident store path version |
|---|---|
| `agent-daemon` | agent-daemon-service (version not in path) |
| `aggregator-daemon` | aggregator **0.3.1** |
| `chroma-daemon` | chroma **0.5.0** |
| `listener` | listener-daemon (version not in path) |
| `message-daemon` | message **0.11.1** |
| `orchestrate-nexus` | orchestrate **0.30.0** |
| `spirit-daemon`, `spirit-judge` | spirit daemon/judge services |
| `lojix-daemon` (system) | lojix-daemon-service |
| `repository-ledger` (system) | repository-ledger **0.2.0** |

`criome`, `router` and `mirror` are packaged and pinned but **not running** —
witnessed: neither appears in the running unit list. (`mirror` being
hard-disabled is relayed from `reports/periphery-audit.md`
§4; this flow did not re-read `CriomOS/modules/nixos/mirror.nix`.)

A caution on the local checkouts: `/git/github.com/LiGoldragon/CriomOS-home`'s
working tree is **7 commits behind its own `origin/main`** (witnessed,
`git rev-list --count HEAD..origin/main`). Its committed-at-origin lock is the
authority for what is deployed; where the two differ this report uses
`origin/main`. `/git/github.com/LiGoldragon/nixpkgs` is a **broken local clone**
(`fatal: your current branch appears to be broken`, witnessed) and could not be
used for any comparison.

---

## 1. Cargo projects

`cargo-outdated` is **not installed** (witnessed: `which cargo-outdated` empty,
`cargo outdated --version` → "no such command"). Every version comparison below
is therefore Cargo.lock versus the local crates.io sparse-index cache, read
directly from the `.cache` files — witnessed, by a script this flow wrote
(`scratchpad/idx.py`, `scratchpad/sweep.py`). Yanked versions and pre-releases
are excluded; "latest" means newest non-yanked stable in the cache.

### 1.1 Edition and MSRV — uniform, and that is the good news

Witnessed, every Cargo.toml read: **edition 2024 everywhere**, without
exception, across all 30 manifests sampled. Declared `rust-version`:

- 1.85 — protos, datom-codec
- 1.88 — repository-ledger, nexus (`1.88.0`), kameo fork (`1.88.0`)
- 1.89 — everything else (ethos-zero, lojix, signal-lojix, meta-signal-lojix,
  orchestrate, curriculum-deploy, chroma, message, aggregator, agent, listener,
  harness, mirror, spirit, router, criome, clavifaber, mentci, claude-answers,
  terminal-cell, signal-terminal)
- absent — brightness-ctl, hexis, substack-cli, horizon-rs (no workspace MSRV)

No repository declares an MSRV newer than 1.89, and no repository is blocked by
the toolchain. The MSRV floor is uniform enough that a single bump would move
the whole estate together if one were ever wanted.

### 1.2 The three Rust versions actually in play

Witnessed, and this is a real finding: there are **three different Rust
toolchains** on this machine, none of them equal.

1. **Interactive Rust** — `rustc 1.96.0 (ac68faa20 2026-05-25)`, resolving to
   `/nix/store/33jgdx2kaiiyfkk9f9wv6l1lyb3hj8c5-rust-minimal-1.96.0/bin/rustc`
   via `home-manager-path`. Supplied by `rust-overlay`, locked 2026-08-13.
2. **nixpkgs Rust** — `1.97.1` in the deployed fork revision. Witnessed by
   evaluating the fork through CriomOS-pkgs offline:
   `cargo = "1.97.1"`.
3. **The toolchain our crates are actually built with under Nix** — fenix
   `complete` (nightly), pinned through `rust-build`. Witnessed,
   `rust-build/lib/default.nix:111-123`: "The cluster Rust toolchain is the
   newest nightly (psyche intent: new language features, not stable). It is
   pinned durably via fenix's flake lock — bump fenix here to advance Rust
   cluster-wide". `rust-build/flake.lock` pins `nix-community/fenix`
   **6914a98b78, 2026-06-19** — witnessed.

Offline evidence that (3) is behind: `/git/github.com/LiGoldragon/nexus`'s own
`flake.lock` already pins fenix **5cc16a9f2a, 2026-09-09** — witnessed, by
scanning every `flake.lock` under `/git/github.com/LiGoldragon/` for the newest
locked revision of each shared input. So the cluster nightly is **~12 weeks**
behind a revision that is already on this disk. Nothing in the estate declares
a nightly feature requirement that this flow found, so the distance is cost, not
breakage — but it is unwitnessed whether any crate compiles clean on the newer
nightly.

### 1.3 The core stack is current; the periphery is a month stale

Witnessed. Repositories whose Cargo.lock has **no watched crate behind**:
ethos-zero, signal-lojix, meta-signal-lojix, horizon-rs, claude-answers,
signal-terminal, brightness-ctl, nexus (rkyv only), curriculum-deploy.

rkyv, tokio and serde are at the cache's newest stable (**rkyv 0.8.18,
tokio 1.53.1, serde 1.0.229**) in: ethos-zero, lojix, signal-lojix,
meta-signal-lojix, horizon-rs, orchestrate, criome, mentci, chroma,
curriculum-deploy, claude-answers, signal-terminal, nexus. That is the realized
stack, and it is in good shape.

Behind by a patch generation across the board — rkyv 0.8.16/0.8.17, tokio
1.52.3, serde 1.0.228, thiserror 2.0.18, bytecheck 0.8.2, rancor 0.1.1/0.1.2,
blake3 1.8.5, indexmap 2.14.0, futures 0.3.32, libc 0.2.186 — in: **message,
aggregator, agent, listener, harness, mirror, spirit, router,
repository-ledger, clavifaber, terminal-cell**. These are exactly the
repositories whose locks were last regenerated around 2026-08-13. This is one
`cargo update` per repo, no semver crossing.

### 1.4 The crates that are genuinely behind

**kameo — the single largest shared gap.** Witnessed:

- We run a **fork**, `/git/github.com/LiGoldragon/kameo`, at version **0.20.0**,
  last commit `3486e4f` 2026-08-13 ("docs: mark Protos estate status"),
  `rust-version = "1.88.0"`, upstream declared as `tqwewe/kameo`.
- Latest on crates.io in the local index: **0.22.2** — two minor versions ahead.
- Consumers pin the fork by **mutable branch**: `kameo = { git =
  "https://github.com/LiGoldragon/kameo.git", branch = "main" }` in chroma,
  criome, introspect, clavifaber, harness, persona (witnessed, grep over all
  manifests). lojix alone takes it from crates.io as `kameo = "0.20"`.
- Every kameo consumer in the estate therefore resolves to 0.20.0: chroma,
  message, agent, listener, harness, mirror, spirit, router, criome,
  repository-ledger, clavifaber, mentci, terminal-cell, lojix.

What the fork changes relative to upstream 0.20.0 was **not established** — the
fork's history was not diffed against upstream here, and there is no upstream
remote in the local clone to diff against offline. That is the principal unknown
blocking a kameo bump, and it should be settled before any attempt.

**chroma's redb and notify are a major version out of line with everything
else.** Witnessed: chroma's lock carries `redb 2.6.3` and `notify 5.2.0`, while
latest are **redb 4.2.0** and **notify 8.2.0**, and every other redb consumer in
the estate (lojix, orchestrate, mirror, spirit, router, criome, mentci,
repository-ledger, message) is already on **4.1.0**. chroma is a *running
daemon* with its own on-disk state; a redb 2 → 4 jump is a storage-format
question, not a dependency bump.

**`nix` (the crate) is stranded at 0.25.1** in mentci and terminal-cell —
six minor versions behind **0.31.3**; lojix and listener are on 0.29.0, two
behind. Witnessed.

**`rand`** — clavifaber and lojix on **0.8.x**, protos/datom-codec/agent/
listener/substack-cli on 0.9.x, latest **0.10.2**. The 0.8 → 0.9 boundary was
already a breaking API change upstream; 0.8 → 0.10 is two.

**`uuid`** — 1.23.x in message, aggregator, agent, listener, harness, mirror,
spirit, router, clavifaber; 1.24.0 in criome, mentci, repository-ledger; latest
**1.26.1**.

**`syn 3.0.5` exists** and most locks still resolve syn 2.0.11x transitively.
Witnessed that listener and criome and mentci already carry syn 3.0.x alongside
— so the estate is mid-transition, driven by upstream proc-macro crates rather
than by us. No repository in the deployed set declares `syn` as a direct
dependency that this flow found; treating this as a *transitive* bump that
follows from `cargo update` is the safe reading, and it is an inference, not a
witness.

**Other single bumps**: `ed25519-dalek 2.2.0 → 3.0.0` (clavifaber, major);
`sha2 0.10.9 → 0.11.0` (lojix, clavifaber); `reqwest 0.12.28 → 0.13.5` and
`base64 0.22.1 → 0.23.1` (agent, listener, spirit, substack-cli);
`crossterm 0.28.1 → 0.29.0` (mentci, terminal-cell); `toml 0.8.23 → 0.9.8` and
`dashmap 6.1.0 → 6.2.1` (hexis); `hyper 1.9.0 → 1.11.1` and `tokio 1.51.0 →
1.53.1` (substack-cli, the most neglected lock in the deployed set).

---

## 2. Flakes — inputs, locked dates, layering

### 2.1 The layered structure, as the nix-input-upgrade skill describes it

Witnessed, from `CriomOS/flake.nix` and `CriomOS-pkgs/flake.nix`:

```
LiGoldragon/nixpkgs (fork, ref=main)
        │
        ├── CriomOS-pkgs ─────── eval-cache boundary. Its only output is
        │     (+ overlays)       `pkgs`, keyed on (nixpkgs.narHash,
        │                        system.narHash, overlay content) so CriomOS
        │                        source edits do not invalidate it.
        │                        MUST be committed and pushed before consumers
        │                        relock.
        │
        ├── rust-build ───────── the one toolchain authority. Every LiGoldragon
        │     (fenix nightly)    crate input declaring `rust-build` is forced
        │                        onto it by `follows` (only clavifaber does).
        │
        ├── CriomOS-lib ──────── shared constants/helpers, cross-consumed.
        │
        └── CriomOS ──────────── the OS root. Follows CriomOS-home for `pkgs`
              │                  (`legacyPackages.${system}`), and forces
              │                  criomos-home's nixpkgs / home-manager /
              │                  criomos-lib / rust-overlay / horizon / system /
              │                  pkgs / orchestrate / spirit to its own.
              └── CriomOS-home ─ the home profile, its own repo and own inputs.
```

Four inputs are **deliberate stubs overridden per deploy by lojix** —
`system` (`path:./stubs/no-system`), `horizon` (`path:./stubs/no-horizon`),
`deployment`, `secrets` (CriomOS only). Witnessed: evaluating
`CriomOS-home#legacyPackages.x86_64-linux.<anything>` throws "The OS-owned
deployment path must provide the target system and projected horizon by
overriding this input" — the stubs are load-bearing and evaluation without
lojix is intentionally impossible.

Contract pins the skill warns about: **`spirit` is pinned by `follows` in
both directions** — CriomOS pins `spirit` to an immutable rev and CriomOS-home
takes `spirit.follows = spirit` from CriomOS. Same for `orchestrate`. So
advancing either requires editing CriomOS, not CriomOS-home.

### 2.2 CriomOS root inputs (23), locked dates

Witnessed, parsed from `flake.lock`:

| input | source | locked | date | pin style |
|---|---|---|---|---|
| nixpkgs | LiGoldragon/nixpkgs | `0e251e24a4f2` | 2026-08-12 | `ref=main` |
| pkgs | LiGoldragon/CriomOS-pkgs | `c64ea0eddea6` | 2026-08-13 | mutable |
| home-manager | nix-community | `c554d3441f72` | 2026-08-13 | mutable |
| rust-overlay | oxalica | `892c035d7c2f` | 2026-08-13 | mutable |
| sops-nix | Mic92 | `a8627b21b910` | 2026-08-13 | mutable |
| rust-build | LiGoldragon | `1bcdafd45909` | 2026-08-12 | mutable |
| criomos-lib | LiGoldragon | `6e3bcb0808b7` | 2026-08-12 | mutable |
| criomos-home | LiGoldragon | `caffe9a17cc5` | 2026-09-11 | rev `9548d7d353dd` requested |
| lojix | LiGoldragon | `23f09f28accc` | 2026-09-11 | **immutable rev** |
| orchestrate | LiGoldragon | `5f016531e765` | 2026-09-05 | **immutable rev** |
| spirit | LiGoldragon | `008d8ca0e4a3` | 2026-08-12 | **immutable rev** |
| brightness-ctl | LiGoldragon | `5274f9937a8b` | 2026-08-12 | mutable |
| clavifaber | LiGoldragon | `d0488014bf93` | 2026-08-12 | mutable |
| criome | LiGoldragon | `2f4dded85697` | 2026-08-12 | mutable |
| mirror | LiGoldragon | `c9708ed639f2` | 2026-08-12 | mutable |
| router | LiGoldragon | `f60d4e33d0d0` | 2026-08-12 | mutable |
| repository-ledger | LiGoldragon | `0580eff46139` | 2026-08-12 | mutable |
| microvm | astro | `71beea0076cd` | 2026-08-09 | mutable |
| blueprint | numtide | `56131e8628f1` | **2026-04-15** | mutable |
| system, horizon, deployment, secrets | path stubs | — | — | overridden |

### 2.3 CriomOS-home root inputs (78) — the stale ones

Witnessed. 40-odd of the 78 are `file:` npm tarball pins for the Pi extension
set and agent-intercom; those are version-locked by URL and move only when the
URL changes. Of the rest, the ones whose lock date is materially old:

| input | locked | date | age at 2026-09-11 |
|---|---|---|---|
| **niri-flake** | `e84276a7f2d1` | **2025-07-19** | **~14 months** |
| ↳ niri-stable (transitive) | `8ba57fcf25d2` | 2025-05-25 | ~15.5 months |
| ↳ niri-unstable (transitive) | `fefc0bc0a715` | 2025-07-18 | ~14 months |
| **annas-mcp** | `5a2b9c50e87d` | 2026-02-22 | ~6.5 months (tag `v0.0.5`) |
| **google-workspace-cli** | `a3768d0e82ad` | 2026-03-31 | ~5.5 months |
| **blueprint** | `56131e8628f1` | 2026-04-15 | ~5 months |
| pyproject-build-systems | `90fde00db368` | 2026-08-03 | ~5.5 weeks |
| crane | `2c71e194474d` | 2026-08-03 | ~5.5 weeks |
| pi-src | `53fa77ccd8a2` (v0.84.1) | 2026-08-06 | ~5 weeks |
| primary-generated-src | `fd049d9030a7` | 2026-08-22 | ~3 weeks |
| stylix | `1e6ccadeda17` | 2026-08-12 | ~4 weeks |
| everything else non-pinned | — | 2026-08-12/13 | ~4 weeks |

The 2026-08-12/13 cluster is one bulk `nix flake update` and it is the shape of
the whole estate: **the last general input refresh was a month ago**, and
everything pinned by rev since then moved individually.

### 2.4 Which inputs are behind, as known offline

Method, witnessed: for each `github:` input in both locks, compare the locked
rev against the local clone's `origin/main` (`git rev-list --count
<locked>..origin/main`); and separately, scan every `flake.lock` under
`/git/github.com/LiGoldragon/` for the newest locked revision of each shared
input, so that another repository's newer pin is offline proof of movement.

**Behind their own `origin/main` (LiGoldragon inputs), witnessed:**

| input | pinned version → head version | commits behind |
|---|---|---|
| repository-ledger | **0.2.0 → 0.4.1** | 6 |
| chroma *(local tree lock)* | 0.4.0 → 0.5.0 | 8 — **but origin/main's lock is current at 0.5.0**, matching the resident daemon |
| orchestrate | **0.30.0 → 0.31.0** | 3 |
| lojix | **1.0.1 → 2.0.0** | 1 |
| agent | 0.3.0 → 0.3.0 | 2 |
| spirit | 0.27.0 → 0.27.0 (deprecation-marking commit) | 1 |
| mirror | 0.3.0 → 0.3.0 (deprecation-marking commit) | 1 |
| harness | 0.3.4 → 0.3.4 | 1 |
| claude-answers | 0.5.1 → 0.6.0 | 1 |
| agent-intercom-pi-src | — | 6 |
| agent-intercom-claude-src | — | 2 |

Current at their heads, witnessed: brightness-ctl, clavifaber, criome,
criomos-lib, CriomOS-pkgs, router, rust-build, aggregator, chroma-emacs, hexis,
listener, mentci-src, message, orca-ide, pi-session-namer, pi-subagents-src,
substack-cli, wispr-flow-linux, agent-intercom-codex-src, criomos-home.

**Behind, proven by a newer local pin elsewhere (third-party inputs),
witnessed:**

| input | deployed pin | newest pin on this disk | source of the newer pin |
|---|---|---|---|
| NixOS/nixpkgs (upstream of our fork) | fork at 2026-08-12 | `5052d7ccbc` **2026-09-09** | `nexus/flake.lock` |
| nix-community/fenix | `6914a98b78` 2026-06-19 (in rust-build) | `5cc16a9f2a` **2026-09-09** | `nexus/flake.lock` |
| ipetkov/crane | `2c71e19447` 2026-08-03 | `eb35abda9f` **2026-09-03** | `nexus/flake.lock` |
| sodiboo/niri-flake | `e84276a7f2` **2025-07-19** | `6558302716` 2026-04-25 | `CriomOS-test-cluster/flake.lock` |

Distance **unknown offline** (no local checkout, no newer local pin):
`numtide/blueprint`, `Mic92/sops-nix`, `astro/microvm.nix`, `danth/stylix`,
`nix-community/home-manager`, `oxalica/rust-overlay`, `yt-dlp/yt-dlp`,
`earendil-works/pi`, `googleworkspace/cli`, `herdrdev/herdr`,
`LiGoldragon/noctalia`, `LiGoldragon/plannotator`, `LiGoldragon/annas-mcp`,
and the whole `registry.npmjs.org` tarball set.

### 2.5 Two findings the layering makes sharp

**niri-flake does not supply the compositor.** This is precisely the pattern the
nix-input-upgrade skill names ("niri-flake pinned v25.08 while nixpkgs already
carried v26.04"), and here it is real and already resolved in our favour by
accident. Witnessed: the running compositor is `niri 26.04 (Nixpkgs)` at
`/nix/store/6ppik5vw4y28qn7nxaqr3xq1dxgk5w66-niri-26.04`, and the fork revision
in use evaluates `niri.version = "26.04"`. The 14-month-old niri-flake input is
consumed for its **home-manager module** (`programs.niri.settings`,
`niri-flake.homeModules.config`), not for its package. So the risk of that
input is a *module-schema* risk against a 26.04 compositor, not an old
compositor. Whether the 2025-07 module schema still covers everything 26.04
accepts was **not checked**.

**CriomOS-pkgs carries one live local patch.** Witnessed, `CriomOS-pkgs/flake.nix`:
three overlays — `openldap` and `spamassassin` with `doCheck = false`, and a
GTK `fetchpatch` of GNOME/gtk commit `7ff233c7` (MR !10130, GLArea DMA-buffer /
GL-texture ownership leak). The deployed fork evaluates `gtk4 = "4.22.4"`,
which is exactly the version the nix-input-upgrade skill records as *not*
containing that fix; the backport is therefore **live**, not historical, and
must be re-verified against whatever GTK the next nixpkgs bump brings — if it
brings 4.23.3 or later the patch becomes historical and must be dropped, and if
it brings another 4.22.x the patch must be rebased.

---

## 3. Cross-repository pin graph among our own crates

Method, witnessed: every `Cargo.toml` under `/git/github.com/LiGoldragon/` was
parsed for git dependencies whose URL names a LiGoldragon repository; each
`rev = ` pin was measured against that producer's local `origin/main` with
`git rev-list --count`. Reproduced by `scratchpad/pins.py`. Producer head
versions are read from `origin/main:Cargo.toml`.

### 3.1 Producer heads (witnessed)

`protos` 0.29.1 `b543678cfc` · `datom-codec` **0.25.7** `99a9e8c9cb` ·
`ethos-zero` 6.1.6 `4695ee0c1f` · `signal` **2.0.0** `626e407be5` ·
`horizon-rs` `8f4240ef23` · `nexus` 0.1.1 `a84bfa960c` ·
`lojix` **2.0.0** `fab60e584d` · `orchestrate` **0.31.0** `1bc55af185` ·
`signal-lojix` 2.0.0 `662cedb7d9` · `meta-signal-lojix` 3.0.1 `f7f11d410d` ·
`signal-orchestrate` 2.0.0 `7408fb6f5f` · `meta-signal-orchestrate` 2.0.2
`d8e035014a` · `signal-spirit` 2.0.0 `e4ab10624a` · `meta-signal-spirit` 2.0.1
`a4b8cddedd` · `signal-terminal` 1.0.1 `ddbd3237a5` · `signal-introspect` 1.1.0
`910b1e3780` · `signal-mirror` 1.0.0 `e6c565caac` · `meta-signal-mirror` 1.0.0
`bdc76bcdd0` · `signal-message` 1.0.0 `178a5ef755` · `signal-persona` 1.0.0
`740eb20f48`.

The release registry at `flows/857335/reports/release-registry.json` is already
**stale against these heads** — relayed as a file, witnessed as stale: it lists
datom-codec 0.25.6 `f2cc0685` (head is 0.25.7 `99a9e8c9`), lojix 1.0.1
`b8f7a8cc` (head is 2.0.0), and does not list signal at all.

### 3.2 The lojix subtree is the one fully converged group

Witnessed. `lojix`, `signal-lojix`, `meta-signal-lojix` and `horizon-rs` are
**mutually current** on protos `b543678c`, datom-codec `99a9e8c9`, ethos-zero
`4695ee0c`, horizon `8f4240ef`, nexus `a84bfa96`, signal `626e407b`. This is the
only group in the estate where every producer pin is at that producer's head.
`chroma` joins them on the three-crate stack (protos/datom-codec/ethos-zero all
current) — the only deployed *daemon* that does.

### 3.3 datom-codec 0.25.7 — the producer everything is behind

Witnessed. datom-codec's head is `99a9e8c9` (0.25.7). Consumers:

- **current** (6): chroma, horizon-rs, lojix, meta-signal-lojix, signal-lojix,
  and datom-codec's own consumers inside the lojix group.
- **behind 3** (still at `f2cc0685`, 0.25.6 — the registry's "released" rev):
  ethos-zero, curriculum-deploy, orchestrate, mirror, signal, signal-domain,
  signal-introspect, signal-message, signal-mirror, signal-orchestrate,
  signal-persona, signal-spirit, signal-spirit-judge, meta-signal-mirror,
  meta-signal-orchestrate, meta-signal-spirit.
- **behind 6** (at `2dad91af`, 0.25.4): claude-answers, signal-terminal,
  signal-upgrade, meta-signal-terminal, meta-signal-upgrade.

Note the shape: **ethos-zero, a producer, is itself behind datom-codec by 3.**
That is the ordering fact that decides the plan — datom-codec is below
ethos-zero, and ethos-zero is below every signal contract.

protos is the healthiest producer: **21 of 28 consumers are current** at
`b543678c`; only the claude-answers/signal-terminal/signal-upgrade cluster
(behind 7, at `aac95b0d`) lags. ethos-zero: 16 current at `4695ee0c`, 8 behind 4
at `daf00729`.

### 3.4 The 205 mutable pins

Witnessed: `grep -c 'branch = "main"' */Cargo.toml` — **43 repositories carry
205 git dependencies pinned to a mutable branch.** Concentrated in: spirit (21),
harness (12), router (12), repository-ledger (8), aggregator (5), mentci (5),
criome (4), listener (4), chroma (2), clavifaber (2), lojix (2).

These are not "slightly behind" — they have **no version at all**; what they
resolve to depends on when the lock was last regenerated. The flow-857335
periphery audit (relayed, `reports/periphery-audit.md` §6) already records six
of these resolving to symbols and features that no longer exist on the
producers' mains (mentci's `signal-introspect` with `features = ["dotos-text"]`;
persona's and terminal's `signal-terminal` constructor calls). This flow
witnessed the manifest lines themselves — `mentci/Cargo.toml:26` does read
`branch = "main", features = ["dotos-text"]` — but did not re-run a build, so
"these fail to resolve" remains that audit's claim, not this flow's witness.

Two of those mutable pins sit in *deployed, running* code: **chroma's two kameo
pins** and **lojix's `sema-engine` and `triad-runtime` pins**. Everything else
mutable is in the not-running set (spirit, harness, router, mentci, criome,
aggregator, listener, repository-ledger, clavifaber all carry them too — of
which aggregator, listener and repository-ledger *are* running).

### 3.5 Consumers behind the released head — the deployed subset

Witnessed, restricted to what is actually deployed or running:

| consumer | producer | pinned | head | behind |
|---|---|---|---|---|
| orchestrate | datom-codec | `f2cc0685` | `99a9e8c9` | 3 |
| aggregator | signal-frame, signal-aggregator | *mutable* | — | unbounded |
| agent | signal-frame `8aa0bcae`, signal-agent `d9ca91d7`, meta-signal-agent `5104d456` | — | — | 4 / 1 / 1 |
| listener | signal-frame, signal-listener, meta-signal-listener | *mutable* | — | unbounded |
| message | signal-frame `8aa0bcae`, signal-message `dff3fbf3`, meta-signal-message `96099d5f`, signal-harness `c05eacf1` | — | — | 4 / 4 / 1 / 3 |
| repository-ledger | signal-frame, signal-repository-ledger, meta-signal-repository-ledger | *mutable* | — | unbounded |
| spirit | signal-domain `801e1c5b`, signal-spirit `b37fc963`, signal-spirit-judge `4fc339fe`, meta-signal-spirit `009cb6c8` | — | — | **33 / 14 / 3 / 11** |
| chroma | protos, datom-codec, ethos-zero | all head | — | **0** |
| lojix | everything | all head | — | **0** |

`spirit` is the deepest hole in the graph — 33 commits behind `signal-domain`
and 14 behind `signal-spirit` — and it is *running right now* while being marked
deprecated. That tension belongs to the main flow, not to this survey.

---

## 4. Systems

All witnessed on this host at 2026-09-11.

| thing | version | provenance |
|---|---|---|
| NixOS / CriomOS channel | **26.11 "Zokor"**, `26.11.20260813.0e251e2` | `nixos-version`; `/run/current-system` → `nixos-system-ouranos-26.11.20260813.0e251e2` |
| system generation | **181**, linked 2026-09-09 16:56 | `/nix/var/nix/profiles/system` |
| home-manager generation | **1026**, linked 2026-09-11 14:35 | `~/.local/state/nix/profiles/home-manager` |
| nixpkgs revision in use | `0e251e24a4f2` of `LiGoldragon/nixpkgs`, locked 2026-08-12 | both `flake.lock`s; matches the running system's version string |
| nix (daemon/CLI) | **2.35.1** | `nix --version` |
| nix in that nixpkgs | 2.34.8 | offline eval |
| kernel in that nixpkgs | 6.18.44 | offline eval |
| mesa / gtk4 / python3 / nodejs | 26.2.0 / 4.22.4 (+ our MR !10130 patch) / 3.14.7 / 24.19.0 | offline eval |
| **jj** | **0.44.0** | `jj --version`; `/nix/store/ssyd5l9…-jujutsu-0.44.0`, reached through `home-manager-path`; that nixpkgs provides 0.44.0 |
| **git** | **2.55.0** | `git --version`; `/nix/store/8wxs657…-git-2.55.0`, same path |
| **rustc / cargo (interactive)** | **1.96.0** (`ac68faa20`, 2026-05-25) | `/nix/store/33jgdx2…-rust-minimal-1.96.0`, from rust-overlay — **behind the 1.97.1 the same nixpkgs carries** |
| Rust for Nix crate builds | fenix nightly, pinned 2026-06-19 | `rust-build/flake.lock` |
| niri | 26.04, from nixpkgs | `niri --version` → `niri 26.04 (Nixpkgs)` |

Offline evidence on jj: a nixpkgs source tree in the store already carries
**jujutsu 0.45.1** (witnessed, `/nix/store/0gzsbyn4…-source/pkgs/…/package.nix`),
so jj 0.44.0 is one release behind something already on this disk. git's and
nix's distance from upstream is **unknown offline**.

A method correction worth recording: an earlier attempt in this flow to evaluate
the fork through `builtins.fetchTree { owner; repo; rev; narHash }` returned a
**different tree** (`1hb1glk…-source`, `.version` 26.05, jj 0.41.0, rustc
1.95.0) than the flake's own input resolution (`31w94yh…-source`, `.version`
26.11, jj 0.44.0, rustc 1.97.1). The flake-resolved tree is the authority and is
what §4 reports; the fetchTree numbers were discarded. Cause unknown — a
narHash-keyed cache hit on an unrelated tree is one possibility, a mis-specified
fetchTree attribute set another. Anyone repeating this should evaluate through
`builtins.getFlake` on CriomOS-pkgs, not through `fetchTree`.

---

## 5. What is NOT known from here

Kept unknown, deliberately:

- The distance from upstream of blueprint, sops-nix, microvm, stylix,
  home-manager, rust-overlay, pi, herdr, noctalia, plannotator, yt-dlp,
  google-workspace-cli, annas-mcp, and the npm tarball set. No local checkout,
  no newer local pin, no network.
- How far `LiGoldragon/nixpkgs` `main` is behind `NixOS/nixpkgs` `master` in
  commits, and whether the fork carries local commits at all. The local clone is
  broken; the only offline evidence is that nexus pins an upstream revision 4
  weeks newer.
- What our kameo fork changes relative to upstream kameo — the blocking unknown
  for the largest single bump in the estate.
- Whether anything in the estate fails to compile on a 2026-09 nightly, on
  kameo 0.22, or on redb 4 with a redb-2-born chroma store. No build was run.
- Whether the 2025-07 niri-flake home-module schema is still complete against a
  26.04 compositor.
- Whether `primary-generated-src` (pinned 2026-08-22, and `/home/li/primary` is
  **1014 commits ahead** of that pin — witnessed) is actually consumed. It is
  declared at `CriomOS-home/flake.nix:219` with the comment "Generated
  project-role packets used by the harness compatibility check", and a grep of
  `modules/` and `packages/` finds **no reference to it**. Either the consumer is
  named differently, or the input is dead. Unresolved.

---

## 6. Prioritized upgrade plan

Ordering rule throughout: **producers before consumers**, and for Nix,
**eval-cache boundary repos committed and pushed before their consumers
relock** (nix-input-upgrade). "Safe tonight unattended" means: no on-disk format
change, no API surface crossing a semver boundary, a local gate exists, and a
failure leaves only a test branch behind.

### Tier 0 — safe tonight, unattended, on test branches

1. **`cargo update` (lockfile-only, no manifest edit) in the 11 month-stale
   repositories** — message, aggregator, agent, listener, harness, mirror,
   spirit, router, repository-ledger, clavifaber, terminal-cell. Moves rkyv
   0.8.16/17→0.8.18, tokio 1.52.3→1.53.1, serde 1.0.228→1.0.229, thiserror,
   bytecheck, rancor, blake3, indexmap, futures, libc. All patch-level within
   the declared ranges. *Risk: very low.* Gate: each repo's own
   `nix flake check` / `cargo test`. Do these in parallel; they do not interact.
2. **Re-pin the five consumers stuck on datom-codec `2dad91af` (0.25.4) and
   protos `aac95b0d` up to the released `99a9e8c9` / `b543678c`** —
   claude-answers, signal-terminal, signal-upgrade, meta-signal-terminal,
   meta-signal-upgrade. These are pure catch-up to revisions the rest of the
   estate already runs. *Risk: low-moderate* — the generated contract surface
   changed between 0.25.4 and 0.25.7, so a regeneration may be needed; that
   fails loudly at compile time on a test branch.
3. **Bump the interactive Rust to 1.97.1** by relocking `rust-overlay` in
   CriomOS/CriomOS-home. Touches no build of ours (crate builds use fenix).
   *Risk: low.* Gate: home-manager eval.

### Tier 1 — do next, attended, one at a time, in this order

4. **datom-codec 0.25.6 → 0.25.7 across its 16 behind-by-3 consumers**, starting
   with **ethos-zero** (a producer that is itself behind), then the signal
   contracts, then orchestrate/mirror/curriculum-deploy. This is the one place
   where ordering genuinely matters: ethos-zero regenerates the contracts, so a
   contract re-pinned before ethos-zero moves must be re-pinned again.
   *Risk: moderate* — generated code, and the periphery audit (relayed) records
   three different ethos-zero generator versions already producing contracts
   released on the same day, so convergence is the point of the exercise.
5. **fenix in `rust-build`: 2026-06-19 → 2026-09-09** (the revision nexus
   already pins, so it is already on disk and needs no network). This advances
   the cluster nightly for every Nix-built crate at once. *Risk: moderate* —
   a nightly three months newer can break on lints, on trait-solver changes, or
   on a crate that used a nightly feature since renamed. It is a single-input
   edit with an enormous blast radius, so gate it by building the lojix group
   and chroma before pushing rust-build.
6. **repository-ledger 0.2.0 → 0.4.1** in CriomOS. It is *running* two minor
   versions behind its own head. *Risk: moderate* — two minors of a ledger
   daemon, unknown store-format implications; the repository's own changelog was
   not read here.
7. **orchestrate 0.30.0 → 0.31.0** and **lojix 1.0.1 → 2.0.0** in CriomOS.
   lojix 2.0.0 is explicitly breaking — witnessed in the commit body: "Signal<T>,
   Signalizable, ByteViewable, and Restorable come from signal rather than from
   the two contract crates, which no longer define them", with "the wire bytes
   are unchanged". Wire compatibility is *claimed by the producer*, not
   witnessed here. **lojix is the deploy mechanism itself** — a broken lojix
   means no way to deploy the fix. Never unattended.

### Tier 2 — needs a decision before it needs an upgrade

8. **kameo 0.20 → 0.22** across 14 repositories. Blocked on the unknown in §5:
   what our fork changes. Two shapes are possible and the choice is the living's:
   rebase the fork onto upstream 0.22.2, or drop the fork and take kameo from
   crates.io (as lojix already does). Either way the fork's mutable `branch =
   "main"` pins should become immutable revs in the same move. *Risk: high* —
   two minor versions of the actor runtime under every daemon.
9. **chroma redb 2.6.3 → 4.x and notify 5 → 8.** chroma is a running daemon with
   its own store, and redb 2 → 4 is a storage-format question. *Risk: high*, and
   it needs a migration answer, not a `cargo update`. Everything else in the
   estate is already on redb 4.1.0, so chroma is the outlier, not the standard.
10. **nixpkgs fork → a 2026-09 upstream revision**, then CriomOS-pkgs, then
    CriomOS and CriomOS-home. Order is fixed by the eval-cache boundary:
    **fork → CriomOS-pkgs (commit + push) → CriomOS/CriomOS-home relock**.
    Before it: verify the GTK MR !10130 backport against whatever GTK the new
    revision carries (drop if ≥ 4.23.3, rebase otherwise), and re-check the
    openldap and spamassassin `doCheck = false` overlays. Expect home-manager
    option renames to surface only at consumer eval time. *Risk: high, and it is
    the single largest-value bump available* — it carries kernel, mesa, GTK, jj,
    git and the entire desktop.
11. **niri-flake 2025-07 → current.** The compositor is already 26.04 from
    nixpkgs, so this is purely a home-module-schema upgrade. *Risk: moderate*
    — fourteen months of `programs.niri.settings` schema drift, all of it
    surfacing at eval, none of it at runtime.

### Tier 3 — hygiene the survey exposed, not version bumps

12. **The 205 mutable `branch = "main"` pins.** No upgrade plan can be stated
    for a dependency that has no version. Converting them to immutable revs is
    the precondition for ever surveying this estate cheaply again — and the
    periphery audit (relayed) shows some of them are already resolving to
    producers that dropped the symbols they use.
13. **`primary-generated-src`** — 1014 commits stale and, as far as a grep of
    `modules/` and `packages/` shows, unreferenced. Resolve which it is before
    deciding whether to bump it or delete it.
14. **The release registry** (`flows/857335/reports/release-registry.json`) is
    behind the producer heads it names. Anything reading it as the release
    authority is reading a month-old snapshot.

### What must not be done unattended

lojix (it is the deploy path), the nixpkgs fork chain, kameo, chroma's redb,
and anything touching spirit — which is simultaneously running, marked
deprecated, and 33 commits behind its own contract producer.

## Sources

- Witnessed on this host, 2026-09-11: `nixos-version`, `/run/current-system`,
  `/nix/var/nix/profiles/system`, `~/.local/state/nix/profiles/home-manager`,
  `nix --version`, `rustc/cargo --version`, `jj --version`, `git --version`,
  `niri --version`, `systemctl --user list-units`, `systemctl list-units`,
  `systemctl show -p ExecStart`, `readlink -f` on the resolved store paths,
  `nix-store -q --deriver`, `nix derivation show`.
- Witnessed, offline Nix evaluation through `builtins.getFlake` on
  `/git/github.com/LiGoldragon/CriomOS-pkgs`, `--offline --impure`, for
  jujutsu/git/rustc/cargo/niri/gtk4/mesa/linux/nix/python3/nodejs/yt-dlp
  versions and the resolved nixpkgs store path.
- Witnessed, read directly: `flake.nix` and `flake.lock` of CriomOS,
  CriomOS-home (working tree and `origin/main`), CriomOS-pkgs, rust-build;
  `rust-build/lib/default.nix`; every `Cargo.toml` and `Cargo.lock` named above;
  `git log`, `git rev-list --count`, `git show <rev>:Cargo.toml` in each named
  repository under `/git/github.com/LiGoldragon/`.
- Witnessed, crates.io sparse-index cache at
  `~/.cargo/registry/index/index.crates.io-1949cf8c6b5b557f/.cache`, newest
  entry 2026-09-11 14:18, read by scripts this flow wrote:
  `idx.py` (index → latest stable), `sweep.py` (Cargo.lock → behind-ness),
  `pins.py` (manifest git pins → producer distance), under
  `/tmp/claude-1001/-home-li-primary/f6db8d14-1dfe-472d-914e-9c441f852834/scratchpad/`.
- Relayed, not re-observed here: `/home/li/primary/flows/f6db8d/reports/periphery-audit.md`
  (§6 broken branch-pinned consumers; §4 mirror hard-disabled; the three-way
  ethos-zero version split) and `/home/li/primary/flows/857335/reports/release-registry.json`
  (the release set, itself witnessed as stale against producer heads).
- Skills loaded and applied: `subflow`, `spirit`, `behavior`,
  `nix-input-upgrade`, `nix-workflow`, `versioning`, `flow-evidence`, `psyche`.
