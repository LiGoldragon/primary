# Scout — Missed-Repos Discovery (repos-manifest / coverage-gap)

## Task and scope

Read-only discovery. The prior per-repo doctrine campaign folded `INTENT.md`
into `ARCHITECTURE.md` across 62 covered repos but missed the rest (root cause:
stale `repos/` symlinks). For EACH missed repo, capture the facts a human needs
to decide **keep-and-fold vs deprecate/retire**: remote liveness, activity
recency, doctrine-file state, INTENT substance, and fold target. No edits, no
commits. Observation is separated from interpretation; deprecation candidacy is
labeled interpretation.

## Commands consulted

- `ls -la /git/github.com/LiGoldragon/` (real repo home).
- `.git`-presence loop → `/tmp/gitrepos.txt` (116); symlink-target loop over
  `/home/li/primary/repos/*` → `/tmp/covered.txt` (62);
  `comm -23` → `/tmp/missed.txt` (54). Partition reproduced exactly.
- `gh auth status` (logged in as `LiGoldragon`, GH_TOKEN, repo+delete_repo scope).
- `gh api --paginate 'user/repos?affiliation=owner&per_page=100'` → liveness
  (`archived`, `fork`, `private`, `pushed_at`) for all 230 owned repos, joined
  onto the 54 missed by name. This is the remote check the prior handover flagged
  as NEVER verified.
- Per-repo filesystem test for `INTENT.md` / `ARCHITECTURE.md` / `AGENTS.md` /
  `README.md` / `Cargo.toml` / `flake.nix`; `jj log -r '@-'` last-commit date.
- `wc -c`/`wc -l` on every missed `INTENT.md` (empty/boilerplate detector);
  full read of the 7 smallest and both no-target repos to judge substance.
- Prior map: `agent-outputs/PerRepoDoctrineCoverageGap/Scout-SituationalMap.md`.

## Reconciliation of handover numbers (observed, exact)

| Metric | Handover (approx) | Observed (exact) |
|---|---|---|
| Missed repos | ~54 | **54** |
| Missed still carrying `INTENT.md` | ~43 | **43** |
| Missed with `ARCHITECTURE.md` (fold target present) | (implied 42) | **42** |
| Missed with `INTENT.md` but NO `ARCHITECTURE.md` (no-fold-target) | 2 named | **2** (exactly the two named) |
| Missed with neither `INTENT` nor `ARCH` | 11 | **11** |

The handover's "54 missed / 43 still have INTENT" reconciles exactly. 116 = 62
covered + 54 missed. Of the 54: 43 carry INTENT.md; of those 43, 41 also have an
ARCHITECTURE.md fold target and 2 do not (`CriomOS-test-cluster`,
`signal-standard`). The other 11 missed repos have no INTENT.md at all
(already doctrine-clean on this axis) and are not part of the fold backlog.

## Remote-liveness headline (the previously-unverified axis)

**All 54 missed repos have a LIVE GitHub remote under
`github.com/LiGoldragon/<name>`. NONE are archived. NONE are missing.** Three are
forks; two are private. So on remote grounds there are **zero dead-remote
deprecation candidates** — every missed repo is a real, present, owner-owned
remote. Recency likewise shows active ownership: 52 of 54 pushed in June 2026;
the two oldest are `AnaSeahawk-website` (2025-12-01) and the AI-notes pair
(2026-05-18).

- **Forks** (`fork=true`): `AnaSeahawk-website`, `kameo`, `whisrs`.
- **Private** (`private=true`): `meta-signal-mentci-client`, `signal-mentci-client`.
  (Both carry `INTENT.md` — keep private substance out of public surfaces when folding.)

## INTENT-substance judgment (observation + interpretation)

Observation: every one of the 43 `INTENT.md` files is real synthesized
direction, NOT an empty or boilerplate stub. Smallest is `meta-signal-lojix`
(639 bytes / 14 lines) and even it states a concrete owner-only mutation
vocabulary and scope boundary. There is **no empty-stub tier** — nothing here is
"delete instead of fold" material on substance grounds. All 43 have real
direction worth folding.

## Per-repo table (54 missed)

Legend: REMOTE = GitHub remote state (all EXIST/live; A=archived none; fork/priv
noted); PUSHED = remote `pushed_at`; LAST = local `@-` commit date; INT/ARCH =
`INTENT.md`/`ARCHITECTURE.md` present; FOLD-TGT = ARCHITECTURE.md (or code home)
to fold into; INTENT gist for the 43.

### Fold backlog — carry INTENT.md, HAVE an ARCHITECTURE.md target (41)

| Repo | REMOTE | PUSHED | LAST | ARCH | FOLD-TGT | INTENT gist / real direction? |
|---|---|---|---|---|---|---|
| agent | live | 2026-06-23 | 2026-06-23 | yes | ARCH | agent-triad daemon runtime — YES |
| BookOfGoldragon | live | 2026-06-16 | 2026-06-16 | yes | ARCH | public first-person practice notes; explicit privacy gate — YES |
| clavifaber | live | 2026-06-20 | 2026-06-20 | yes | ARCH | CriomOS host key-material provisioning tool; NOTA request/response — YES |
| cloud | live | 2026-06-20 | 2026-06-19 | yes | ARCH | provider execution daemon (Hetzner first); plan/policy state — YES |
| criomos-horizon-config | live | 2026-06-05 | 2026-06-05 | yes | ARCH | pan-horizon config source for CriomOS — YES |
| domain-criome | live | 2026-06-19 | 2026-06-19 | yes | ARCH | domain meaning + provider-neutral projection — YES |
| lojix | live | 2026-06-30 | 2026-06-30 | yes | ARCH | long-lived deploy daemon stack — YES |
| mentci | live | 2026-06-29 | 2026-06-27 | yes | ARCH | programmable approval-surface daemon — YES |
| meta-signal-agent | live | 2026-06-23 | 2026-06-23 | yes | ARCH | owner-only meta policy contract for agent — YES |
| meta-signal-cloud | live | 2026-06-19 | 2026-06-19 | yes | ARCH | meta policy contract: provider accounts/plans/apply — YES |
| meta-signal-domain-criome | live | 2026-06-17 | 2026-06-17 | yes | ARCH | meta policy contract for domain-criome — YES |
| meta-signal-lojix | live | 2026-06-22 | 2026-06-17 | yes | ARCH | owner-only deploy-mutation vocabulary — YES |
| meta-signal-mentci | live | 2026-06-26 | 2026-06-26 | yes | ARCH | meta Configure contract for Mentci daemon — YES |
| meta-signal-mentci-client (PRIVATE) | live | 2026-06-27 | 2026-06-27 | yes | ARCH | meta policy/authority for a Mentci client — YES |
| meta-signal-mind | live | 2026-06-18 | 2026-06-18 | yes | ARCH | meta signal contract for PersonaMind policy — YES |
| meta-signal-mirror | live | 2026-06-29 | 2026-06-29 | yes | ARCH | meta policy wire contract of mirror triad — YES |
| meta-signal-orchestrate | live | 2026-06-26 | 2026-06-23 | yes | ARCH | MetaSignal contract for privileged orchestrate — YES |
| meta-signal-persona | live | 2026-06-17 | 2026-06-17 | yes | ARCH | meta policy contract for privileged persona ops — YES |
| meta-signal-repository-ledger | live | 2026-06-19 | 2026-06-19 | yes | ARCH | meta authority contract for repository-ledger — YES |
| meta-signal-router | live | 2026-06-30 | 2026-06-30 | yes | ARCH | meta contract for PersonaRouter channel policy — YES |
| meta-signal-spirit | live | 2026-06-30 | 2026-06-30 | yes | ARCH | privileged Spirit lifecycle/config contract — YES |
| meta-signal-terminal | live | 2026-06-19 | 2026-06-19 | yes | ARCH | meta contract for terminal session lifecycle — YES |
| meta-signal-version-handover | live | 2026-06-17 | 2026-06-17 | yes | ARCH | meta authority for component version handover — YES |
| mirror | live | 2026-06-29 | 2026-06-29 | yes | ARCH | daemon of the mirror triad — YES |
| nota-config | live | 2026-06-19 | 2026-06-19 | yes | ARCH | typed config input library every component uses — YES |
| persona-pi | live | 2026-06-27 | 2026-06-27 | yes | ARCH | Nix-packaged Pi harness; no-manual-approval automation — YES |
| repository-ledger | live | 2026-06-20 | 2026-06-20 | yes | ARCH | records repository changes after push — YES |
| rust-build | live | 2026-06-19 | 2026-06-19 | yes | ARCH | shared Nix build-policy flake for Rust repos — YES |
| signal-cloud | live | 2026-06-19 | 2026-06-19 | yes | ARCH | ordinary peer-callable wire contract for cloud — YES |
| signal-domain-criome | live | 2026-06-17 | 2026-06-17 | yes | ARCH | ordinary Signal contract for domain-criome — YES |
| signal-frame | live | 2026-06-27 | 2026-06-27 | yes | ARCH | wire kernel: frame envelope, rkyv archives — YES |
| signal-lojix | live | 2026-06-23 | 2026-06-17 | yes | ARCH | typed Signal contract for lojix orchestrator — YES |
| signal-mentci | live | 2026-06-26 | 2026-06-27 | yes | ARCH | wire contract for Mentci programmable UI — YES |
| signal-mentci-client (PRIVATE) | live | 2026-06-27 | 2026-06-27 | yes | ARCH | schema-generated client contract crate — YES |
| signal-mirror | live | 2026-06-23 | 2026-06-23 | yes | ARCH | ordinary wire contract of mirror triad — YES |
| signal-repository-ledger | live | 2026-06-19 | 2026-06-19 | yes | ARCH | ordinary Signal contract for repository events — YES |
| signal-sema | live | 2026-06-23 | 2026-06-23 | yes | ARCH | universal Sema classification vocabulary — YES |
| signal-spirit | live | 2026-06-27 | 2026-06-23 | yes | ARCH | ordinary Signal contract for Spirit surface — YES |
| signal-version-handover | live | 2026-06-17 | 2026-06-17 | yes | ARCH | private daemon-to-daemon upgrade contract — YES |
| triad-runtime | live | 2026-06-19 | 2026-06-19 | yes | ARCH | shared runtime library for schema-derived components — YES |
| version-projection | live | 2026-06-23 | 2026-06-23 | yes | ARCH | library projecting values between adjacent versions — YES |

### Fold backlog — carry INTENT.md, NO ARCHITECTURE.md target (2 — no-fold-target)

| Repo | REMOTE | PUSHED | LAST | ARCH | INTENT lines | INTENT gist / real direction? |
|---|---|---|---|---|---|---|
| CriomOS-test-cluster | live | 2026-06-29 | 2026-06-29 | **NO** | 129 | Synthetic `fieldlab` fixture cluster proving CriomOS consumes projected Horizon data, never production facts; owns projection→config test pipeline, static + booted-VM altitudes. Strong real direction — YES. Has `flake.nix`, `checks/`, `lib/`, `README.md` as code home. |
| signal-standard | live | 2026-06-23 | 2026-06-23 | **NO** | 63 | Second non-component shared `signal-` library alongside `signal-frame`; owns cross-component standards: `ComponentKind` (14-variant closed roster), `Differentiator`, `AuthorizedObjectInterest` lattice, `StandardSocket`. Cites Spirit eeeo/t312. Strong real direction — YES. Has `src/`, `schema/`, `Cargo.toml`, `README.md` as code home. |

### No INTENT.md — already doctrine-clean on the fold axis (11)

| Repo | REMOTE | PUSHED | LAST | ARCH | Notes |
|---|---|---|---|---|---|
| AnaSeahawk-website | live, **fork** | 2025-12-01 | 2025-12-01 | no | Hugo site; most dormant of all 54 |
| ArtificialIntelligence | live | 2026-05-18 | 2026-05-18 | no | AI notes README |
| BookOfLuna | live | 2026-05-18 | 2026-05-18 | no | Luna AI intent notes |
| brightness-ctl | live | 2026-06-19 | 2026-06-20 | no | laptop backlight daemon; Cargo+flake+AGENTS |
| caraka-samhita | live | 2026-06-05 | 2026-06-05 | no | study/translation/philology repo |
| kameo | live, **fork** | 2026-06-19 | 2026-06-19 | no | vendored Kameo actor-runtime lifecycle fork |
| kibord | live | 2026-06-11 | 2026-05-30 | no | keyboard/keymap (ergodone) |
| qmkBinaries | live | 2026-05-30 | 2026-05-30 | no | QMK firmware binaries |
| WebPublish | live | 2026-06-11 | 2026-05-30 | no | web publishing (aski source); Cargo+flake |
| whisrs | live, **fork** | 2026-06-11 | 2026-05-03 | no | voice-to-text dictation tool in Rust |
| skills | live | 2026-07-01 | 2026-06-30 | yes | generator source; canonical checkout lives in `repos/skills` (real repo, not symlink), which is why it shows "missed"; NOT a fold candidate — already clean |

## Synthesizer sections

### (a) No-fold-target repos (INTENT.md exists, ARCHITECTURE.md absent)

Exactly **two**, matching the handover names — no others found:
`CriomOS-test-cluster`, `signal-standard`. Both carry substantial real direction
(129 / 63 lines) and both have a plausible code home already (flake+checks+lib;
src+schema+Cargo). For these, folding means either creating a new
`ARCHITECTURE.md` or placing direction in a code stub — there is no existing
markdown target to fold into.

### (b) Apparent deprecation / retire candidates (INTERPRETATION)

On the two hard signals in the brief (dead remote; long-dormant + no dependents):
**there are no dead-remote candidates** — all 54 remotes are live and unarchived.
So deprecation candidacy rests only on dormancy, which is weak here. My
interpretation of the softest-signal set (label: interpretation, not fact):

- `AnaSeahawk-website` — a **fork**, dormant since 2025-12-01 (~7 months), no
  doctrine files, personal website. Weakest ownership signal of the 54; most
  plausible retire/leave-as-is candidate. Interpretation only.
- `ArtificialIntelligence`, `BookOfLuna` — dormant since 2026-05-18 (~6 weeks),
  note-only repos, no doctrine files. Low-activity; not obviously dead.
- `qmkBinaries` (2026-05-30) and `kibord` (last commit 2026-05-30) — hardware
  firmware/keymap artifacts; naturally low-churn, not evidence of abandonment.

I did **not** verify dependents/importers for any repo (no cross-repo dependency
scan run), so "no dependents" is unconfirmed for every candidate — treat all
deprecation candidacy as unverified interpretation. Nothing here is a confident
retire recommendation.

### (c) Ambiguous / needs-human-judgment

- `skills` — appears "missed" only because its canonical checkout is
  `repos/skills` (a real jj repo, not a symlink into `/git`). Actively pushed
  today (2026-07-01). Has ARCHITECTURE.md, no INTENT.md — already clean. It is a
  false positive in the "missed" set, NOT a fold or deprecation candidate.
- The 3 forks (`AnaSeahawk-website`, `kameo`, `whisrs`): fork status is a keep/own
  question independent of the fold campaign. `kameo` and `whisrs` are actively
  used (vendored runtime fork; dictation tool) despite being forks.
- 2 private repos (`meta-signal-mentci-client`, `signal-mentci-client`): both are
  live fold-backlog members with ARCH targets; fold normally but keep private
  substance out of public surfaces.

## Blockers, unknowns, follow-ups

- **Dependents/importers not scanned.** No `Cargo.toml`/`flake.nix` reverse-dep
  analysis was run, so "no dependents" (a leg of the deprecation test) is
  unverified for every repo. A dependency scan is the missing input if any
  retire decision must be made.
- **INTENT substance summarized, not deeply audited.** Gists come from the first
  ~25 lines of each file plus full reads of the 7 smallest and both no-target
  repos; all sampled files were genuine direction. I did not read all 43 in full,
  but the size/line audit rules out empty/boilerplate stubs across the set.
- **Local last-commit vs remote pushed_at differ slightly** for a few repos
  (e.g. `cloud` remote 2026-06-20 vs local `@-` 2026-06-19; `lojix` remote
  2026-06-30 vs local 2026-06-30). Both are reported; neither changes any
  keep/deprecate call.
- **Spirit not queried.** Whether specific repos are formally deprecated or
  retired in Spirit intent was not checked; if a retire decision needs
  intent-grounding, query Spirit before acting.
- Coverage-partition assumption inherited from the prior map (coverage = symlink
  targets under `repos/`); reproduced exactly (62/54), consistent with the stated
  stale-symlink mechanism, but the campaign's own iteration code was not read.
