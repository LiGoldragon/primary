# Scout Situational Map — Per-Repo Doctrine Campaign Coverage Gap

## Task and scope

Read-only investigation. A per-repo doctrine campaign (eliminate `INTENT.md` →
fold into `ARCHITECTURE.md`; rehome archived records) ran only over the repos
**symlinked under `/home/li/primary/repos/`**. But `/git/github.com/LiGoldragon/`
holds more repos than are symlinked there. Goal: enumerate every repo under
`/git/github.com/LiGoldragon/`, diff against campaign coverage, and report the
true gap with per-repo `INTENT.md` / `ARCHITECTURE.md` status.

No edits made. All facts below are backed by the commands quoted.

## Commands consulted

- `ls -la /git/github.com/LiGoldragon/` and `ls -la /home/li/primary/repos/`
- `.git`-presence loop over `/git/github.com/LiGoldragon/*/` → `/tmp/gitrepos.txt` (116)
- symlink-target resolution loop over `repos/*` → `/tmp/covered.txt` (62)
- `comm -23 /tmp/gitrepos.txt /tmp/covered.txt` → `/tmp/missed.txt` (54)
- per-missed-repo presence test for `INTENT.md` / `ARCHITECTURE.md` / `AGENTS.md`
- per-missed-repo `jj status` (clean/dirty) and `jj log -r '@-'` (last commit date + subject)
- cloud family `jj log`/`jj status` detail
- `spirit` query: skipped — not load-bearing for the file-presence facts requested; see Unknowns.

## Headline reconciliation (observed)

| Metric | Count |
|---|---|
| Repos under `/git/github.com/LiGoldragon/` with `.git` | **116** |
| Covered by campaign (symlink-into-`/git` targets in `repos/`) | **62** |
| **Missed (in `/git`, NOT symlinked under `repos/`)** | **54** |
| Missed repos still carrying `INTENT.md` (doctrine says eliminate) | **43** |
| Missed repos with `ARCHITECTURE.md` | 42 |
| Missed repos with neither `INTENT.md` (already doctrine-clean) | 11 |

Sanity confirmed: `comm -13` shows every covered symlink target is a real `/git`
repo (covered ⊆ gitrepos), so the 62/54 split is exact and non-overlapping.
All 116 `.git` entries are real repos; `116 = 62 + 54`.

### The true coverage gap (one statement)

**The campaign touched 62 of 116 LiGoldragon repos (53%). It missed 54 repos
(47%), and 43 of those 54 still carry an `INTENT.md` that doctrine wants
eliminated/folded into `ARCHITECTURE.md`.** The miss is not noise: it includes
the entire `cloud` surface, the entire `domain-criome` surface, large families
of `meta-signal-*` and `signal-*` contract repos, and several daemon repos
(`agent`, `mirror`, `lojix`, `mentci`).

## Why these were missed (interpretation, mechanism observed)

`repos/` is the campaign's input surface. Its LiGoldragon entries are **symlinks
that point into `/git/github.com/LiGoldragon/`** (e.g. `repos/arca ->
/git/github.com/LiGoldragon/arca`). The campaign processed only what `repos/`
exposed. Any `/git` repo with **no corresponding symlink in `repos/`** was never
seen. That is the 54.

Two coverage subtleties worth flagging to downstream (observed, not assumed):

- `repos/skills` is itself a **full jj repo** (real dir, has `.jj/repo` dir, on
  `main`), and `repos/skills-primary-ascl-doctrine` is a jj **workspace**
  pointing at `../../skills/.jj/repo`. So the canonical skills checkout lives in
  `repos/`, NOT via a symlink into `/git/.../skills`. Therefore
  `/git/.../skills` shows up in the missed list (no symlink), even though skills
  is clearly actively maintained. `/git/.../skills` has **no `INTENT.md`** (has
  `ARCHITECTURE.md`), so it is already doctrine-clean regardless.
- `repos/spirit-guardian-config` is a jj workspace pointing into
  `/git/.../spirit/.jj/repo`, and `repos/spirit` is a normal symlink to
  `/git/.../spirit`, so **`spirit` IS covered** (not in the missed set).

Non-repo note: `/git/github.com/LiGoldragon/lojix-primary-5rzf-7` is the one
top-level dir **without `.git`** — it is a **jj workspace of `lojix`** (has
`.jj`, `.jj/repo` contents reference the lojix store). Correctly excluded from
the 116 repo count; it is a transient working copy, not an independent repo.
(It does contain an `INTENT.md`, but that is lojix's, reached separately.)

## The MISSED set — 54 repos with doctrine status

Legend: INTENT = `INTENT.md` present (YES = doctrine still wants it eliminated);
ARCH = `ARCHITECTURE.md` present; all working copies were **clean** at scout time
(`jj status` = "no changes"); LAST = `@-` commit date (active-ownership signal).

### Missed repos that STILL carry INTENT.md (43 — the elimination backlog)

| Repo | ARCH | LAST commit | Purpose (first ARCHITECTURE line) |
|---|---|---|---|
| agent | yes | 2026-06-23 | daemon of the agent triad (`agent` runtime, `signal-agent`) |
| BookOfGoldragon | yes | 2026-06-16 | public first-person practice notes / autobiographical fragments |
| clavifaber | yes | 2026-06-20 | host-key-material aggregator and certificate signer |
| **cloud** | yes | 2026-06-19 | provider API daemon for Criome systems; first target DigitalOcean |
| criomos-horizon-config | yes | 2026-06-05 | pan-horizon configuration source for CriomOS |
| CriomOS-test-cluster | **no** | 2026-06-29 | independent fixture cluster for CriomOS/Horizon regression tests |
| **domain-criome** | yes | 2026-06-19 | Criome-domain registry and projection daemon |
| lojix | yes | 2026-06-30 | new deploy stack: one crate shipping a long-lived deploy daemon |
| mentci | yes | 2026-06-27 | component daemon hosting the programmable approval surface |
| meta-signal-agent | yes | 2026-06-23 | owner-only meta policy Signal contract for `agent` |
| **meta-signal-cloud** | yes | 2026-06-19 | meta policy Signal contract for the `cloud` component |
| meta-signal-domain-criome | yes | 2026-06-17 | meta policy Signal contract for `domain-criome` |
| meta-signal-lojix | yes | 2026-06-17 | owner-only policy signal contract for `lojix` |
| meta-signal-mentci | yes | 2026-06-26 | owner/meta configuration contract for Mentci |
| meta-signal-mentci-client | yes | 2026-06-27 | meta policy/authority contract for a Mentci client |
| meta-signal-mind | yes | 2026-06-18 | meta signal contract for PersonaMind policy/configuration |
| meta-signal-mirror | yes | 2026-06-29 | meta policy wire contract of the mirror triad |
| meta-signal-orchestrate | yes | 2026-06-23 | MetaSignal contract for privileged `orchestrate` role |
| meta-signal-persona | yes | 2026-06-17 | meta policy Signal contract for privileged persona ops |
| meta-signal-repository-ledger | yes | 2026-06-19 | meta-signal authority contract for repository-ledger |
| meta-signal-router | yes | 2026-06-30 | meta-signal Signal contract for PersonaRouter channel policy |
| meta-signal-spirit | yes | 2026-06-30 | MetaSignal contract for privileged Spirit lifecycle/policy |
| meta-signal-terminal | yes | 2026-06-19 | meta Signal contract for privileged terminal session lifecycle |
| meta-signal-version-handover | yes | 2026-06-17 | meta authority surface for component version handover |
| mirror | yes | 2026-06-29 | daemon of the mirror triad |
| nota-config | yes | 2026-06-19 | typed configuration input library every component uses |
| persona-pi | yes | 2026-06-27 | Nix-packaged Pi harness for the Persona agent |
| repository-ledger | yes | 2026-06-20 | records repository changes after push |
| rust-build | yes | 2026-06-19 | exports a per-system library at `lib.${system}` |
| **signal-cloud** | yes | 2026-06-19 | ordinary Signal contract for the `cloud` component |
| signal-domain-criome | yes | 2026-06-17 | ordinary Signal contract for `domain-criome` |
| signal-frame | yes | 2026-06-27 | the wire kernel: frame envelope, length-prefixed rkyv archives |
| signal-lojix | yes | 2026-06-17 | typed Signal contract for the lojix deploy orchestrator |
| signal-mentci | yes | 2026-06-27 | wire contract for Mentci's programmable UI |
| signal-mentci-client | yes | 2026-06-27 | schema-generated client contract crate |
| signal-mirror | yes | 2026-06-23 | ordinary working wire contract of the mirror triad |
| signal-repository-ledger | yes | 2026-06-19 | ordinary Signal contract for repository events |
| signal-sema | yes | 2026-06-23 | owns the universal Sema classification vocabulary |
| signal-spirit | yes | 2026-06-23 | ordinary Signal contract for the psyche-facing Spirit surface |
| signal-standard | **no** | 2026-06-23 | shared cross-component standards for the primary workspace |
| signal-version-handover | yes | 2026-06-17 | private upgrade contract carrying daemon-to-daemon handover |
| triad-runtime | yes | 2026-06-19 | shared runtime library for schema-derived components |
| version-projection | yes | 2026-06-23 | library for projecting values between adjacent versions |

Two of the 43 have an `INTENT.md` but **no `ARCHITECTURE.md`**
(`CriomOS-test-cluster`, `signal-standard`) — for these, folding the INTENT into
an ARCHITECTURE means there is no existing ARCHITECTURE.md target yet; downstream
must create one or place the direction in a code stub.

### Missed repos with NO INTENT.md (11 — already doctrine-clean on this axis)

| Repo | ARCH | LAST commit | Purpose source |
|---|---|---|---|
| AnaSeahawk-website | no | 2025-12-01 | (Hugo `_index.md` site; least active) |
| ArtificialIntelligence | no | 2026-05-18 | AI notes README |
| BookOfLuna | no | 2026-05-18 | Luna AI intent notes |
| brightness-ctl | no (README) | 2026-06-20 | laptop backlight control daemon |
| caraka-samhita | no (README) | 2026-06-05 | study/translation/philology working repo |
| kameo | no (README) | 2026-06-19 | vendored Kameo actor-runtime fork (lifecycle fork) |
| kibord | no | 2026-05-30 | keyboard/keymap repo (ergodone keymap) |
| qmkBinaries | no | 2026-05-30 | QMK firmware binaries (minidox refresh) |
| skills | yes | 2026-06-30 | generator source for workspace skill/role surfaces |
| WebPublish | no | 2026-05-30 | web publishing (aski source) |
| whisrs | no (README) | 2026-05-03 | Linux voice-to-text dictation tool in Rust |

These 11 need no INTENT.md elimination; `skills` already has `ARCHITECTURE.md`.

## Cloud surface — explicit confirmation (the deferred-record candidate homes)

All four named candidate homes are **live, clean, actively-owned repos**, each
carrying an `INTENT.md` (still to eliminate) AND an `ARCHITECTURE.md`. All sit on
`main` with an empty working copy (`jj status` = no changes):

| Repo | INTENT.md | ARCHITECTURE.md | `@-` (main) commit |
|---|---|---|---|
| `cloud` | present | present | `cloud: harden DigitalOcean live test path` (2026-06-19) |
| `signal-cloud` | present | present | `signal-cloud: add DigitalOcean Provider variant` (2026-06-19) |
| `meta-signal-cloud` | present | present | `meta-signal-cloud: add DigitalOcean Provider variant` (2026-06-19) |
| `domain-criome` | present | present | `use Kameo lifecycle fork` (2026-06-19) |

So the deferred "cloud-component config" records have real, current homes — but
those homes were **entirely outside the campaign's coverage**, which is exactly
why the deferral had nowhere to land.

## Other obviously-missed families (observed)

The miss is family-structured, not scattered. Whole contract families were
skipped because none of their members are symlinked in `repos/`:

- **cloud family:** `cloud`, `signal-cloud`, `meta-signal-cloud` — all missed.
- **domain-criome family:** `domain-criome`, `signal-domain-criome`,
  `meta-signal-domain-criome` — all missed.
- **mentci family:** `mentci`, `signal-mentci`, `signal-mentci-client`,
  `meta-signal-mentci`, `meta-signal-mentci-client` — all missed.
- **mirror family:** `mirror`, `signal-mirror`, `meta-signal-mirror` — all missed.
- **lojix family:** `lojix`, `signal-lojix`, `meta-signal-lojix` — all missed.
- **repository-ledger family:** `repository-ledger`, `signal-repository-ledger`,
  `meta-signal-repository-ledger` — all missed.
- **agent family:** `agent`, `meta-signal-agent` missed (note `signal-agent` IS
  covered via symlink — so this family is split).
- **persona/mind/orchestrate/router/terminal/version-handover meta tier:**
  `meta-signal-persona`, `meta-signal-mind`, `meta-signal-orchestrate`,
  `meta-signal-router`, `meta-signal-terminal`, `meta-signal-version-handover`,
  `signal-version-handover`, `signal-spirit`, `signal-sema`, `signal-frame`,
  `signal-standard` — all missed, while their `signal-*` siblings (e.g.
  `signal-persona`, `signal-mind`, `signal-router`, `signal-terminal`,
  `signal-spirit` covered? — `signal-spirit` is MISSED) are inconsistently
  covered. **The `meta-signal-*` tier is almost entirely missed:** of the
  meta-signal repos in `/git`, only `meta-signal-criome`, `meta-signal-harness`,
  `meta-signal-introspect`, `meta-signal-message`, `meta-signal-system`,
  `meta-signal-upgrade` are symlinked/covered; the other ~16 are missed.

Interpretation: `repos/` was seeded for an earlier, smaller component set and
never re-synced as the contract families (`meta-signal-*`, the cloud and
domain-criome surfaces, `signal-frame`/`signal-standard`/`signal-sema`) were
added. The campaign inherited that stale surface.

## Working-state and ownership (observed)

- **All 54 missed repos are clean** (`jj status` = "no changes" for every one).
  No dirty trees to worry about; this is a pure doctrine-coverage gap, not a
  work-in-progress hazard.
- **Active ownership is strong:** 43 of 54 have `@-` commits in **June 2026**;
  the cloud/domain/mentci/mirror/meta-signal families are all current.
  Least-recently-touched: `AnaSeahawk-website` (2025-12-01), `whisrs`
  (2026-05-03), `ArtificialIntelligence`/`BookOfLuna` (2026-05-18). None look
  abandoned; all sit on a named `main` bookmark.

## Likely relevant files for the follow-up campaign run

- Input surface to re-sync: `/home/li/primary/repos/` (symlink set).
- 43 `INTENT.md` files to eliminate live at
  `/git/github.com/LiGoldragon/<repo>/INTENT.md` for each repo in the
  "still carry INTENT.md" table above.
- 42 corresponding `/git/github.com/LiGoldragon/<repo>/ARCHITECTURE.md` fold
  targets; 2 repos (`CriomOS-test-cluster`, `signal-standard`) lack an
  ARCHITECTURE.md target.
- `cloud`, `signal-cloud`, `meta-signal-cloud`, `domain-criome` —
  `ARCHITECTURE.md` present in each; candidate homes for the deferred
  cloud-component config records.

## Blockers and unknowns (named)

- **Not verified:** whether each missed repo's GitHub remote is live/owned — I
  read only local `jj` state (last commit + branch), not remote existence. Local
  evidence (recent dated commits on `main`) strongly implies live ownership but
  is not a remote check.
- **Not verified:** the exact archived-record-rehoming half of the campaign
  ("rehome archived records"). I checked only `INTENT.md`/`ARCHITECTURE.md`
  presence, not whether each missed repo contains archived records still needing
  rehoming. That requires a separate scan if it is in scope.
- **Spirit query not run.** The brief asked for file-presence facts, which are
  fully answered from the filesystem. Whether the deferred "cloud-component
  config" records are formally tracked in Spirit (and where they should land) is
  intent-grounding I did not query; flag for the orchestrator if record-rehoming
  decisions depend on it.
- **Coverage definition assumption:** I treated "campaign coverage" = the set of
  LiGoldragon repos reachable as symlink targets under `repos/`. If the campaign
  actually iterated a different list (e.g. a hardcoded manifest), the true
  missed set could differ. The brief states the campaign "processed only the
  repos symlinked under repos/", so this assumption matches the stated mechanism,
  but I did not see the campaign's own iteration code.
- `repos/skills` being a real checkout rather than a symlink means `skills` shows
  as "missed" by the symlink definition even though it is the actively maintained
  skills repo; it has no `INTENT.md` so it needs no elimination either way — but
  downstream should not be confused by its appearance in the missed list.
