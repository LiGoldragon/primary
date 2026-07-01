# Independent Audit — Intent Fidelity + Good Design (capstone quality gate)

Second, independent auditor pass over the coverage-gap / repos-deprecation
session work, applying the beauty gate (`design-quality`), `cam8` (target the
ideal pattern), `10pz` (replaceable-not-additive), `repo-intent`,
`intent-manifestation`, `nota-design`, `naming`, `architecture-editor`, and
`privacy`. Builds on — does not redo — the prior correctness/secret pass
(`Auditor-SecretLeakAndCoverage.md`). READ-ONLY: no audited surface was edited.
Intent grounded via read-only Spirit `Lookup` / `PublicTextSearch` only.

## Deep-audited vs sampled (no silent truncation)

- **Deep-audited (full read + analysis):** `protocols/repos-manifest.nota`; the 4
  authored `ARCHITECTURE.md` — `signal-standard`, `substack-cli`, `goldragon`
  (main), `CriomOS-test-cluster` (branch `intent-curator/architecture-md`); the
  `repos/` deprecation edits in primary `ARCHITECTURE.md` (§0.5/§1/§3/§4/§5) and
  `orchestrate/AGENTS.md`; the retirement end-state (3 deprecated repos).
- **Sampled folds (8, across families):** `signal-lojix`, `meta-signal-spirit`,
  `mirror`, `repository-ledger`, `domain-criome`, `BookOfGoldragon` (privacy
  gate), `clavifaber`, `signal-sema`. Plus two out-of-scope cross-checks
  (`harness`, `horizon-rs` — correctly NOT folded this session).
- **Corpus-wide greps (not sampled — exhaustive):** `ESSENCE.md` references and
  dumped operating-process lines across every `/git/.../LiGoldragon/*/ARCHITECTURE.md`;
  manifest record count / balance / on-disk coverage cross-check.
- **NOT exhaustively verified:** the remaining ~32 folds' full Direction prose
  (sampled only); per-record `origin/main` state for every repo (the prior audit
  owns coverage completeness); whether every unresolvable Spirit citation is
  archived vs deleted (characterized, not traced record-by-record).

## Executive verdict

**Overall: PASS-WITH-FIXES.** The intent work is faithful — every authored and
sampled-folded Direction traces to real psyche-authored source, with no
fabrication or invented direction found. The manifest is close to the ideal NOTA
shape. The fixable items are staleness/coherence seams and two design
refinements; none is a correctness or privacy failure.

Per dimension:

1. **Intent fidelity — PASS.** Citations in the authored files verbatim-match the
   source `INTENT.md` (verified for `signal-standard` eeeo/t312 and
   `CriomOS-test-cluster` dqg3/aipc/7let/vcin/xxgp); `substack-cli` traces to its
   `AGENTS.md` + `lore/rust/style.md`; `goldragon` to handover facts. No overreach
   or synthesis-as-intent. One matter-in-direction slip (F2) and a systemic
   provenance-verifiability wrinkle (F6).
2. **Design quality — PASS-WITH-FIXES.** Manifest has the ideal spine (positional
   records, named-variant status enum, facts separated from status — not
   flag-soup). Residual non-ideal: `Content`-status conflates kind with lifecycle,
   and `Fork` is double-encoded as both a family and a flag (F5). Sampled folds
   mostly read as coherent direction (`clavifaber`, `mirror`, `signal-lojix`,
   `signal-sema` exemplary); `domain-criome` carries a dumped line (F2).
3. **Conventions — PASS.** NOTA positional/bare-atom/named-variant correct;
   naming is full-English throughout; `architecture-editor` constraints-as-test-seeds
   are strong. Minor: `signal-sema` cites transient artifacts (F7); manifest
   symmetry/flag-naming (F5b). Section-heading variance not re-litigated (prior
   ruling stands).
4. **Coherence of end-state — PASS-WITH-FIXES.** Manifest (120 records, full
   on-disk coverage, 3 deprecated confirmed gone) + deprecation + folds are
   largely coherent. Residual seams: 14 dangling `ESSENCE.md` references (F1),
   `persona-spirit` missing from the authoritative manifest (F3), the orchestrate
   scan still keyed off `active-repositories.md` (F4). `CriomOS-test-cluster`
   doctrine-home `None` is expected (authored on branch, pending merge) and
   tracked.
5. **Privacy — PASS.** Prior secret-leak PASS holds. `BookOfGoldragon`'s privacy
   gate folded as mechanism-only; two private repos appear name+status+`[IsPrivate]`
   only; `goldragon` secrets are mechanism/handle only. One LOW topology-specificity
   nuance (F8).

**Worktree removal (Part A): DONE.** `lojix-primary-5rzf-7` README verified
byte-identical to `lojix` `main@origin` (content already on main via sibling
`658ecd2a`), no code changes; `jj workspace forget` from canonical `lojix`, dir
removed, canonical `lojix` intact (clean, `src/` present, sibling workspaces
preserved); disposition noted on bead `primary-pg6f`.

## Findings (severity-ranked)

### CRITICAL — none.

### HIGH — none newly found.

Carried (not mine to re-adjudicate): prior-audit **H1** (cloud `INTENT.md` still
on `origin/main`; direction substance landed, only the deletion is stranded) is
tracked as `primary-omis` (cloud-maintainer owns `cloud` main, pending merge).

### MEDIUM

**F1 — 14 `ARCHITECTURE.md` files carry dangling `~/primary/ESSENCE.md`
references after ESSENCE.md was eliminated this campaign.** Files: `signal-lojix`
(a this-session fold — ref is inside its Direction "Scope" blockquote at :34 and
its invariant at :194), `lojix`, `mind`, `sema`, `persona`, `lore`, `CriomOS`,
`signal`, `criome`, `arca`, `nexus`, `forge`, `signal-forge`, `signal-mind`. The
ESSENCE content moved into primary `ARCHITECTURE.md` §0.5 "Workspace vision and
intent" (the "Today and eventually" subsection at :102, plus "Backward
compatibility…" and "Push, not poll"). Every reference now points a public repo
guidance surface at a file that no longer exists — the substance is correct, the
pointer is dead. *Fix:* repoint each `~/primary/ESSENCE.md §"…"` to
`~/primary/ARCHITECTURE.md §"Workspace vision and intent"` (matching subsection).
Mechanical; verifiable by a follow-up grep returning zero `ESSENCE` hits.

**F2 — `domain-criome` Direction ends with a dumped operating/process rule.**
"Operator integrates designer `next` work into `main` by rebasing,
cherry-picking, re-implementing, or merging when the code is good enough" is
process/operating matter, not durable repo direction. Per `architecture-editor` /
`intent-manifestation` it belongs in `domain-criome/AGENTS.md`, not the
ARCHITECTURE Direction section. Only `domain-criome` matched the exact pattern
corpus-wide, but the fix-dispatch should sweep folds for other operating-rule
dumps. *Fix:* move the line to `AGENTS.md`; leave Direction as pure direction.

**F3 — `persona-spirit` is a live required input but absent from the authoritative
manifest (internal inconsistency between two this-session artifacts).** The
authored `CriomOS-test-cluster/ARCHITECTURE.md` explicitly resolves the proposal's
"dangling `persona-spirit`" question by declaring it "a live, required input, not a
legacy leftover" that supplies the v0.1.0/v0.1.1 Spirit daemons for the upgrade
test. `gh` confirms `LiGoldragon/persona-spirit` exists and is **unarchived**
(last push 2026-06-08). Yet `protocols/repos-manifest.nota` — which claims to be
the authoritative inventory of LiGoldragon repos — omits it entirely. When
`CriomOS-test-cluster` (`primary-6obv.4`/`primary-2f7j`) merges to main, a
main-tracked repo will depend on an input the inventory does not list. *Fix:* add
`persona-spirit` to the manifest. Its "frozen but required historical-version
source" nature also exposes F5's status-enum gap (no clean slot for it).

**F4 — `orchestrate/AGENTS.md` repo-hygiene scan still keyed off
`active-repositories.md`, not the now-authoritative manifest.** Line 314 "Scans
the repositories named by `protocols/active-repositories.md`; it does not crawl
the filesystem." The deprecation reconciliation updated primary `ARCHITECTURE.md`
§3/§4 to make `repos-manifest.nota` the single source of truth and demote
`active-repositories.md` to a curated *attention map* (a subset). A hygiene scan
scoped to the attention-map subset reintroduces exactly the partial-coverage
failure mode the manifest was built to eliminate. *Fix:* point the scan at the
manifest's `status = Active` set (or state explicitly that this scan is
intentionally scoped to the curated attention set).

**F5 — Manifest design: two special cases that the ideal would dissolve
(`cam8`/`design-quality`).** The manifest is *close* to ideal and is NOT
flag-soup (facts are correctly a separate positional field from status). Two
residual seams:

- **F5a — `Content` status conflates repo *kind* with *lifecycle*.** The status
  axis mixes "kept, code" (`Active`) and "kept, asset" (`Content`) with "retired"
  (`Deprecated`). "Kept vs retired" is lifecycle; "code vs asset/data" is kind.
  The ideal separates them: all kept repos are `Active`; asset-ness is a kind
  fact (already partly carried by `Family Content` and the `DataRepo` flag —
  e.g. `criomos-horizon-config` is `Content` status but `Family CriomOS`, showing
  the two axes are already decoupled in practice). Contrast with current: the
  coverage semantic "edge-silence is expected here" would then attach to the kind,
  not a bespoke status value.
- **F5b — `Fork` is double-encoded.** `kameo` carries BOTH `(Family Fork)` and
  `[IsFork]`, while `whisrs`/`AnaSeahawk-website` are `[IsFork]` inside their real
  families. `Fork`-as-family is a catch-all bucket for a fork "with no other
  cluster home"; the ideal drops the `Fork` family (put `kameo` in `Tooling`) and
  lets `[IsFork]` be the single orthogonal fact. Minor twins: `(Family X)` is
  always wrapped even though it is payload-less, whereas payload-less status /
  doctrine-home values are bare atoms (`Active`, `Architecture`, `None`) — an
  asymmetry; and flag naming mixes predicate-style (`IsFork`, `IsPrivate`) with
  bare tags (`BuildTimeConsumed`, `DataRepo`).

  *Caveat:* the manifest shape was psyche-approved at the review gate (proposal
  §5.2; `primary-6obv.2` closed). Per `repo-intent`, only the psyche overrides
  accepted shape — so F5 is surfaced as the ideal-vs-current contrast `cam8`
  requires, NOT a defect to fix unilaterally. Route as a psyche design question.

### LOW / informational

**F6 — Systemic dangling Spirit citations across folds.** Every design-record ID
cited in the audited surfaces is unresolvable via live `Lookup`: `eeeo`, `t312`
(signal-standard); `dqg3`, `aipc`, `7let`, `vcin`, `xxgp` (CriomOS-test-cluster);
`0yx5`, `rj9y`, `29pb`, `x0ja` (mirror) — while `cam8`/`10pz`/`qjrf` resolve fine,
so the daemon works. This is **NOT fabrication**: the citations verbatim-match the
psyche-authored source `INTENT.md` (verified), and only `7let` even appears in the
`/tmp` archive dump. It is consistent with the session's archive-rehoming, which
moved record substance into `ARCHITECTURE.md` and left the source records
archived/removed. The residual is that `repo-intent`'s "keep direction traceable
to the statements" is only half-met: a reader cannot re-verify the citation
against Spirit. *Disposition (psyche/doctrine call, not a mechanical fix):* either
accept Spirit IDs as historical-provenance breadcrumbs and document that folded
ARCHITECTUREs may cite archived IDs, or re-home / drop unresolvable IDs. Prefer
the former — the direction is genuinely psyche-backed.

**F7 — `signal-sema` Direction cites transient artifacts.** It references
`reports/designer/246-v4-bundled-fix-deep-design-with-examples.md` and
`intent/component-shape.nota` as backing, against `architecture-editor` ("do not
reference transient artifacts from architecture; move the fact in and drop the
dependency"). The Layer-1/2/3 substance is already inlined, so the citations can
simply be dropped.

**F8 — `goldragon` ARCHITECTURE production-topology specificity (privacy nuance,
not a leak).** The example "Prometheus's primary router Wi-Fi and its independent
backup Wi-Fi" states a concrete production-network topology fact on a public repo
surface. No secret value is present (the prior secret-leak PASS holds), but the
architecture does not need node-level dual-Wi-Fi specificity — generalize to
"router interface records that carry production access facts."

**F9 — Two tracker follow-ups are partially stale (disposition otherwise right).**
`primary-6obv.10` ("doctrine-home None→ARCHITECTURE for CriomOS-test-cluster +
signal-standard") is already satisfied for `signal-standard` — the live manifest
records it `Architecture` (as it also now does for `goldragon` and `substack-cli`,
resolving prior-audit M1). Only `CriomOS-test-cluster` remains `None`, correctly
gated on the `primary-6obv.4`/`primary-2f7j` merge. `primary-6obv.12` ("stale
persona-pi example at primary `ARCHITECTURE.md:273`") also appears already
resolved — :273 now reads `persona-codex`/`persona-gemini`/`persona-claude`, no
`persona-pi`. *Fix:* trim 6obv.10 to CriomOS-test-cluster only; verify/close
6obv.12.

## Per-dimension detail

**Intent fidelity (PASS).** Provenance verified at the source: `signal-standard`'s
removed INTENT cited `eeeo`×2/`t312`×2 → carried verbatim; `CriomOS-test-cluster`'s
still-on-main INTENT cites `dqg3`×2/`aipc`/`7let`/`vcin`/`xxgp` and its commit
message names "Spirit 7let, vcin" → carried faithfully; `substack-cli`
constraints ("methods on types not free functions", "domain newtypes", "one type
per concept, PostFull the one accepted sibling", "manual thiserror, never anyhow")
are a tighter synthesis of its `AGENTS.md` + `lore/rust/style.md`; `goldragon`
(data-only, cluster-proposal source of truth, schema owned by horizon-rs) matches
the handover's `t5vj`/cloud-node-data facts. Architecture *shape* decisions
(signal-standard's 14-variant/5-zone `ComponentKind` partition; CriomOS-test-cluster's
auto-pickup generator) are legitimate agent-authored architecture, and are the
kind of ideal-pattern design `cam8` wants — "declaring a test-VM node IS getting a
test" dissolves per-node special cases into the normal case. No invented psyche
direction found.

**Design quality (PASS-WITH-FIXES).** Beauty-gate strengths: the manifest's
named-variant status enum with in-variant disposition avoids bool-soup; folds like
`clavifaber` ("adding a capability means adding a typed request/response/method —
not flags or loose helper logic") and `signal-sema` (payloadless class vocabulary,
"the vocabulary is the schema") describe genuinely ideal shapes; `10pz` is honored
throughout (lojix-cli/signal-executor "retired", signal-standard's "no-backward-compat
override, both consumers rebuild at once", primary §0.7 "wrapping an old path is
not migration"). Weaknesses are F5 (status/kind conflation, fork double-encoding)
and F2 (one dumped process line).

**Conventions (PASS).** NOTA: positional, bare atoms for canonical strings,
named variants, optional flags as a trailing vector — all per `nota-design`;
parses balanced (249/249 parens, 123/123 brackets). Naming: full English across
manifest and prose. `architecture-editor`: constraints written as test seeds
(signal-standard "add no operation roots…", CriomOS-test-cluster "No production
facts / No hand-stubbed horizon", clavifaber mode-0600 rules) — exemplary. Minor
deviations F7 (transient-artifact citation) and F5b (symmetry/flag naming).

**Coherence (PASS-WITH-FIXES).** Manifest = 120 records (106 Active / 11 Content /
3 Deprecated); every on-disk LiGoldragon repo is covered (comm cross-check empty);
the 3 deprecated (`persona-pi`, `WebPublish`, `AnaSeahawk-website`) are confirmed
gone from disk; `repos/` correctly retired-as-index with residual-checkout
migration deferred (`primary-6obv.9`, psyche-gated). Seams: F1 (ESSENCE refs), F3
(persona-spirit gap), F4 (orchestrate scan). Tracked follow-ups
(6obv.9/.10/.11/.12, omis, 2f7j, t5vj.3) are the right disposition; they should
absorb F1/F3/F4 (currently untracked).

**Privacy (PASS).** `BookOfGoldragon` fold carries only the privacy *mechanism*
("personal material enters only by explicit psyche authorization"; "sensitive
personal material stays out unless the psyche explicitly makes it public") — no
personal substance. The two private repos appear as name + `Active` +
`Architecture` + `[IsPrivate]` only. `goldragon` describes `secrets/` naming
convention and "router SAE passwords … stay out of any public surface" as
mechanism, no value. One LOW nuance (F8).

## Recommended fix dispatch (I did not edit; audit kept independent)

1. Mechanical, safe now: F1 (repoint 14 ESSENCE refs), F2 (move domain-criome
   process line to AGENTS.md), F7 (drop signal-sema artifact citations), F9 (trim
   6obv.10, close 6obv.12). Verify F1 with a zero-hit `ESSENCE` grep.
2. Coherence: F3 (add persona-spirit to manifest), F4 (repoint orchestrate scan or
   document its scope) — small edits, want a confirming glance.
3. Psyche design question (do not fix unilaterally): F5 (manifest status/kind +
   fork encoding), F6 disposition (Spirit-citation traceability policy).
4. F8: generalize the goldragon topology example (author/owner call).

## What could not be verified

- The ~32 unsampled folds' full Direction prose (8 sampled; corpus-wide greps
  caught the systemic ESSENCE and operator-process patterns, but a per-fold
  altitude read was not done).
- Whether each unresolvable Spirit ID is archived vs deleted (characterized as
  "not in live daemon, consistent with archive-rehoming"; not traced per record).
- Per-repo `origin/main` residual-INTENT state (prior audit owns coverage; its H1
  is tracked as `primary-omis`).
