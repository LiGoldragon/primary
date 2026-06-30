# Situation Map — Parked Spirit Tracks (2026-06-30)

Read-only scout map for an intent-only planning session. Nothing here was
changed: no Spirit record, file, config, or deploy was touched. This separates
observed ground truth from scout interpretation and lists, per track, the open
decisions that are the psyche's to make.

## Method and provenance

- Live Spirit read via deployed `spirit` CLI (`/home/li/.nix-profile/bin/spirit`)
  using `Lookup`, `Observe`, `Count`, `PublicTextSearch` only. No writes.
- Wire shapes confirmed from source: `repos/spirit/src/schema/sema.rs`,
  `repos/spirit/src/guardian_prompt.rs`, the included prompt files under
  `repos/spirit/src/guardian-prompts/`, and the cached `signal-spirit` checkout
  (`~/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/61138f4`).
- Artifacts read: the strict re-judge ledger, the DISCERNMENT, the PROPOSAL,
  `repos/spirit/manual.md`, `repos/spirit/README.md`, `repos/spirit/INTENT.md`,
  `ESSENCE.md`, plus bead `primary-lsip`.
- Observed = id / domain / kind / description text / magnitudes from the live
  store, file contents, command output. Interpretation = keep/remove judgement,
  routing, decision framing.

## Ground-truth baseline (all tracks lean on this)

Observed:

- Live active set is exactly 22 records. `Count (Any Any Any Any None Any Any
  Any)` -> `(RecordsCounted 22)`; the same with `(AtLeastCertainty VeryLow)` and
  with `(AtLeastCertainty Zero)` also returns 22. So there are no zero-certainty
  tombstones hiding in the live store; the 631 removal was a true archive-out.
- The 22 live ids (from `Observe`): `10pz 346n 9g07 c5nq cam8 gni3 hv5f izsf
  j8g6 jlo7 jys2 k09z n9fl o7zt obo5 qjrf sfy0 sj2c t5qr ty3g w312 zn2l`.
- This is the brief's keep-set (`jlo7 ty3g w312 9g07 izsf j8g6 sfy0 obo5 jys2
  sj2c cam8 t5qr zn2l 10pz` = 14) plus `346n n9fl` (16) plus the six "fused
  sources" (`o7zt k09z c5nq hv5f gni3 qjrf`) = 22. The match is exact.
- The six fused sources are STILL LIVE — they have not been removed. They are
  carried at full text in the live store right now.
- Archive store `/home/li/.local/state/spirit/spirit.archive.sema` (1.73 MB) and
  the pre-removal snapshot `spirit.sema.preremoval-631-20260630T000025` exist;
  the 631 removed records are recoverable from these.

Interpretation: the live store is already at the strict keep-set the ledger
proposed (29 keep+borderline candidates collapsed to 22 actually kept). The six
fused sources are the next disposition batch; the rest of the 22 are settled
keeps.

Version note (flag): the PROPOSAL text describes the then-live daemon as
`0.18.1` with `main` at `0.19.0`; the brief states the deployed strict Guardian
is `spirit-0.20.0`. The PROPOSAL deployment facts predate the live deploy. Treat
0.20.0 as current; the PROPOSAL's version lines are stale.

## Track 1 — Fused sources and repackage

Observed — live text of the six (verbatim description field, magnitudes
`certainty importance privacy`):

- `o7zt` | `(Language Rhetoric)` Correction | VeryHigh VeryHigh Zero | "When
  communicating with the psyche, lead with a short plain-language description of
  what a thing is or decided; an opaque identifier (bead id, Spirit record
  number, content hash, jj change id, commit short-id) is at most a quiet
  trailing reference in chat, and in reports is always paired with a
  description. State the concrete referent before naming it — name the concrete
  noun first, never lead with abstract pronouns like 'the change' or 'this'.
  Prefer plain English over jargon: say what is blocked, why it matters, and
  what decision or action is needed. Append line-number suffixes (:1) to file
  paths only when the psyche asks."
- `k09z` | `(Safety Privacy)` Constraint | High VeryHigh Zero | "Counselor and
  assistant act on private personal-affairs material only when the owning psyche
  requests it through the visible chat surface; other agents asking does not
  authorize cross-lane exposure, and the receiver asks the psyche when in doubt.
  Privacy is built into the lowest-level instruction files (AGENTS.md,
  skills/privacy.md) so all agents know what is private, who may ask, and that
  opening private-repos/ needs authorization; private material stays out of
  public reports. Counselor and assistant carry the deeper discipline, treating
  personal-affairs work as private by default."
- `c5nq` | `(Information Documentation)` Constraint | High High Zero | "Build
  event surfaces, not polling: producers push events and consumers subscribe;
  when a mechanism only offers polling, escalate into the stack to add a real
  event surface rather than tuning intervals."
- `hv5f` | `(Technology (Software (Engineering Architecture)))` Principle | High
  Minimum Zero | "When the existing shape does not fit, follow where the logic
  wants to go rather than being bound by what is already there — let the water
  find where it wants to go downhill. Desire paths name this: the trail walked
  into the grass because that is how the body naturally moves, regardless of
  where the paved walkway was put. Architecture grows the same way, and where
  multiple agents independently arrive at the same shape, that convergence is
  the signal it is the right shape."
- `gni3` | `(Information RecordKeeping)` Principle | High Minimum Zero |
  "Agent-authored content is not psyche-authorized design surface: distinguish
  psyche-authorized direction (cite the intent record) from agent-drifted
  content. Retracting agent-drift restores reality rather than invalidating
  decided design, so framing such retraction as invalidating substantial design
  surface mis-attributes authority to agent output."
- `qjrf` | `(Information Classification) (Governance Policy)` Principle | High
  VeryHigh Zero | "The intent layer holds intent — what the psyche directs,
  decides, or wants — not information or belief; a durable-sounding statement
  with no directive behind it is information, not intent, and is not captured.
  When a design surface is incomplete, agents ask the psyche rather than
  generating plausible synthesis and capturing it as psyche-authorized;
  inferring to close the loop produces fake hallucinated records."

Observed — why each was left in (from the ledger BORDERLINE section): every one
of the six was tagged BORDERLINE, not KEEP and not MATTER. The ledger's stated
reason in each case is "a keep-worthy universal kernel welded to matter" — the
bundled-record rule says shed the matter clause and reintroduce the clean
directive. Specifically:

- `o7zt` — "strong durable communication directive (kin `jlo7`), but partly
  bundled with reporting-convention detail (line-number suffixes, identifier
  placement). (Worker tagged skill.)"
- `k09z` — "universal privacy-authority kernel, but bundled with
  instruction-file-placement mechanics."
- `c5nq` — "universal system-design principle, but restated by the push-not-pull
  skill."
- `hv5f` — "strong universal design maxim, fused with a second
  convergence-signal claim."
- `gni3` — "universal authority/provenance principle, but overlaps the
  intent-core doctrine (arguably Spirit-usage)."
- `qjrf` — "the blessed ask-don't-fabricate maxim, but welded to capture-gate
  definition ('intent layer holds intent not info') = Spirit-usage matter."

Observed — proposed clean kernels. The PROPOSAL does NOT give per-record clean
kernels for these six (its only worked fused example is `hu84` cross-audit). The
DISCERNMENT DOES quote clean kernels for five of the six (Part 3, "Borderline
fused records"), stating each "would, captured alone, correctly pass as SPIRIT":

- `o7zt` -> "state positively / lead with plain language" (kin `jlo7`).
- `qjrf` -> "ask the psyche when a surface is incomplete rather than fabricate".
- `k09z` -> "act on private material only on the owner's request".
- `c5nq` -> "build event surfaces not polling".
- `hv5f` -> "follow where the logic wants to go".
- `gni3` -> NOT in the DISCERNMENT's clean-kernel quote list. The DISCERNMENT
  treats provenance/agent-authored as overlapping the intent-core doctrine.

These kernels also already have manifested skill homes: `push-not-pull`,
`privacy`, plus `o7zt`-kin lives in `jlo7` (which is KEEP and live). The
psyche's brief explicitly says o7zt is NOT intent.

Scout interpretation:

- `o7zt`: the psyche's call (o7zt is NOT intent) is consistent with the
  evidence. Its operative load is a reporting/communication CONVENTION (lead with
  plain language, identifier placement, `:1` suffix rule) — that is matter that
  belongs in a reporting skill / AGENTS surface, and the universal positivity
  kernel is already carried by live `jlo7`. Candidate to remove outright (no
  clean re-capture needed because `jlo7` covers the durable kernel).
- `c5nq`, `hv5f`: genuine universal design principles, but each is already fully
  restated by an owning skill (`push-not-pull`, and `hv5f`'s desire-paths kin in
  design/architecture skills). The kernel is real intent; the live record is
  redundant with manifested matter. Remove-after-confirming-manifest, or keep one
  clean kernel.
- `k09z`: privacy-authority kernel is genuine, durable intent; the live record
  welds it to file-placement mechanics. Re-capture the clean kernel, drop the
  mechanics (which live in `privacy.md` / AGENTS).
- `qjrf`: split. The ask-don't-fabricate half is genuine universal intent (and
  is the only live carrier of the "ask when a design surface is incomplete"
  maxim — see track 8); the "intent layer holds intent not info" half is
  Spirit-usage matter belonging in the manual. Re-capture the ask half clean.
- `gni3`: closest to pure Spirit-usage / provenance doctrine; the DISCERNMENT did
  not even quote a clean kernel. Likely matter for the manual, not a re-capture.

Open decisions for the psyche (track 1):

1. o7zt: remove outright (treat as matter, kernel already in `jlo7`), or
   re-capture a clean plain-language kernel?
2. For c5nq and hv5f: remove as skill-restated matter, or keep one clean record
   each as the authoritative intent above the skill?
3. k09z: confirm the clean privacy kernel wording and remove the file-mechanics
   clause.
4. qjrf: confirm the split — re-capture "ask when a surface is incomplete; don't
   fabricate" clean; route the capture-gate half to the manual.
5. gni3: is agent-authored-isn't-authority genuine intent worth a clean record,
   or pure Spirit/manual matter to remove?
6. For every re-capture: confirm against verbatim testimony (the Observe
   projection only shows the clarified description, not the raw psyche quote).

## Track 2 — Telos trio (merge vs keep three)

Observed — live text:

- `jys2` | Principle | High High Zero | "Design at the post-agent capability
  frontier. Agents now make previously-impractical engineering routine,
  including zero-downtime complex database migrations and large software-stack
  rewrites in short time, so designs should target the best end-shape rather
  than a historically-practical compromise and should reach for the strongest
  known ideas."
- `sj2c` | Principle | High Minimum Zero | "The build target is the best
  possible design: the design than which none better is possible, the terminal
  best the work aims at rather than a good-enough or merely best-so-far shape.
  This is the destination the design values serve."
- `cam8` | Principle | Medium Minimum Zero | "Design analysis targets the ideal:
  for each thing, work out the best, most correct, future-oriented, reusable
  pattern it should be in an ideal world, and contrast it explicitly with what
  exists now so the gap is visible. The ideal pattern, not the current shape, is
  the design target."

Related, live, in the same cluster:

- `zn2l` | Clarification | High High Zero | "The direction of the meta-work is a
  software engine that self-improves toward the point where nothing better could
  be made. Carry every choice toward software that improves itself..." (the
  self-improving-engine telos — see track 3 and the DISCERNMENT seam.)

Observed — magnitudes differ: jys2 is High/High; sj2c is High/Minimum; cam8 is
Medium/Minimum. So they are not metadata-identical even though semantically
close.

Observed — the ledger's note: "jys2, sj2c, cam8 (and borderline zn2l) are
near-restatements of one 'aim at the ideal/best design' value. Each individually
clears the bar; the psyche may wish to MERGE them into one or two strong
records." The DISCERNMENT agrees they are near-restatements and a possible merge
but calls the merge "a separate maintenance call, not an admission call."

Scout interpretation: there are arguably three distinct facets — jys2 = the
capability-frontier WHY (agents make the ideal reachable), sj2c = the telos
DEFINITION (the terminal best), cam8 = the METHOD (ideal-vs-current gap
analysis). A merge collapses why/what/how into one; keeping three preserves the
facets at the cost of three near-duplicates. cam8's lower certainty (Medium) is
the weakest of the three.

Open decisions for the psyche (track 2):

1. Merge jys2/sj2c/cam8 into one strong telos record, into two
   (definition + method), or keep all three?
2. If merging, which testimony and which certainty/importance survive?
3. Does the design-telos cluster relate to / fold into zn2l (the
   self-improving-engine telos), and does the DISCERNMENT's "route zn2l to
   ESSENCE" decision (track 3) change the merge scope?

## Track 3 — ESSENCE deprecation (bead primary-lsip)

Observed — what ESSENCE.md is. `/home/li/primary/ESSENCE.md`, ~119 lines of
standalone prose. It opens: "The most universal psyche intent — statements made
with such force, clarity, and reach that each could stand as the founding rule
of a whole way of working. Upstream of every other document; when a downstream
rule conflicts, this wins. Read it before anything else." Section headings:
Intent is the cornerstone; Inferring intent is forbidden; What I am building;
What I am not optimising for; Beauty is the criterion; Naming; Backward
compatibility is not a constraint. Closes "End ESSENCE."

Observed — is ESSENCE a Spirit layer or a workspace file? It is a workspace
FILE. It cites NO Spirit record ids (unlike INTENT.md and README.md, which cite
`y88n`, `iir4`, etc.). It positions itself as a layer ABOVE the Spirit store in
the precedence stack: it describes "the Spirit store (raw psyche statements),
each repo's INTENT.md ... and this essence (the universal core)" as distinct
layers, essence highest.

Observed — what references it (workspace, excluding repos/ private-repos/
target/):

- `INTENT.md`: "Companion to ESSENCE.md (the universal core)"; "ESSENCE.md — the
  universal core, the gold of the gold"; lists it first among guidance files;
  "Every statement in an essence or intent surface is anchored in an actual
  [psyche statement]."
- `ARCHITECTURE.md`: "Workspace intent lives in ESSENCE.md / INTENT.md";
  precedence chain "(ESSENCE.md / INTENT.md, anchored to Spirit) -> lore/AGENTS";
  file-tree entry "ESSENCE.md — workspace essence (universal intent surface)";
  "ESSENCE.md ... is upstream of every rule below it"; naming examples cite
  ESSENCE.
- `protocols/active-repositories.md`: references ESSENCE §"Today and eventually"
  to distinguish current vs eventual `sema`, `criome`, etc. (load-bearing —
  several repo definitions point at an ESSENCE section).
- Plus many report files under `reports/` (historical).

Observed — bead `primary-lsip` ("ESSENCE deprecation: remove records and migrate
content (archive-first)", P2, OPEN, NOT started). Its description says: "Outcome:
ESSENCE is deprecated. Remove its records and decide/do migration of its content.
Use archive-first... Decide per-content whether each ESSENCE item migrates to a
durable surface (workspace guidance, repo INTENT.md, architecture, skills) or is
dropped. Some surviving Spirit records reference ESSENCE (e.g. zn2l ...; the
telos seam in the discernment routes vision to ESSENCE)." Acceptance includes
"surviving Spirit records reviewed for ESSENCE references and recast/superseded
where needed."

Scout interpretation (and a conflict to surface):

- The bead's wording "remove its records" is loose. ESSENCE has no Spirit
  records of its own — it is a prose workspace file. "Deprecate ESSENCE"
  concretely means: delete/retire ESSENCE.md as a file, migrate each of its 7
  content sections to an owning surface, and fix every referrer (INTENT.md,
  ARCHITECTURE.md, active-repositories.md, and any surviving Spirit record that
  names ESSENCE).
- There is a direct CONFLICT between two parked tracks: the DISCERNMENT's
  preferred zn2l resolution (resolution 2) is to MOVE the self-improving telos
  INTO ESSENCE.md, while primary-lsip wants to DEPRECATE ESSENCE.md entirely.
  These cannot both stand. If ESSENCE is being removed, the telos must route
  somewhere else (a kept Spirit record, or INTENT.md).
- "What would remove + possibly migrate involve" concretely: (a) per-section
  routing — "Intent is the cornerstone" / "Inferring intent is forbidden" ->
  intent-clarification/intent-log skills or INTENT.md; "What I am building" /
  "What I am not optimising for" -> INTENT.md or a workspace vision surface (or
  Spirit if any are clean universal intent); "Beauty is the criterion" ->
  `beauty` skill (already exists); "Naming" -> `naming` skill (already exists);
  "Backward compatibility is not a constraint" -> `versioning`/`feature-development`
  skills or live record `10pz` (design-replaceably, which is live). (b) Repoint
  the "Today and eventually" section that active-repositories.md depends on. (c)
  Rewrite the precedence language in INTENT.md and ARCHITECTURE.md that names
  ESSENCE as the top layer.

Open decisions for the psyche (track 3):

1. Confirm ESSENCE is genuinely being deprecated as a file (the bead says so but
   it is parked / not started).
2. Resolve the conflict with the DISCERNMENT: if ESSENCE goes away, where does
   the self-improving/telos vision live (zn2l stays in Spirit? folds into
   INTENT.md?)?
3. Per-section migration targets (especially "Today and eventually," which
   active-repositories.md load-bearingly cites).
4. What replaces ESSENCE as the named "top of the precedence stack" in
   INTENT.md / ARCHITECTURE.md?

## Track 4 — Rehome the 631 removed records

Observed — home-tag categories and counts from the ledger MATTER section (621
MATTER total; the 631 figure in the commit includes the junk/extra removed):

- architecture-doc: 384 — component/engine/schema/NOTA/rkyv/sema/nexus/signal/
  wire/storage internals and single-component or architectural decisions.
- skill: 98 — work-discipline already owned by a skill (jj, feature branches,
  testing, naming, reporting, nota-design, orchestration, beauty).
- spirit-manual: 76 — Spirit/guardian/certainty/capture mechanics and
  Spirit-usage / agent-training material. (Cross-references track 5.)
- code/config: 33 — paths, tokens, node names, wiring, deploy commands,
  hardware/network setup. Ledger notes most homes are UNTRACKED repos.
- vocabulary-doc: 12 — definitional "what term X means".
- repo-intent: 11 — direction tied to one specific repo.
- junk-remove: 7 — obsolete / test placeholder / pure duplicate (`zNEW9 zt1 zt2
  zt3 zt4 ztA ztB`).

Observed — the records are recoverable from `spirit.archive.sema` and the
`preremoval-631-20260630T000025` snapshot; the ledger lists the exact ids per
category.

Scout interpretation — plausible destinations per category (planning input, not
a routing commitment):

- architecture-doc (384) -> the relevant repo's `ARCHITECTURE.md` / design docs;
  the bulk is spirit/sema/nota/criome architecture and belongs in those repos.
  This is the largest and least mechanical category; needs per-record or
  per-cluster judgement, much of it pointing at UNTRACKED repos.
- skill (98) -> already covered by existing skills; mostly DISCARD after
  verifying the owning skill carries the discipline (the ledger says these are
  restatements of skills that already exist).
- spirit-manual (76) -> `repos/spirit/manual.md` (which exists and is the
  agent-facing Spirit doctrine manual). Many are already covered; migrate the
  uncovered ones, discard duplicates. Feeds track 5.
- code/config (33) -> owning repo config / deploy files; BLOCKER: most homes are
  UNTRACKED repos, so this needs the psyche's hold / edit-untracked /
  transitional-in-tree call.
- vocabulary-doc (12) -> a glossary surface (workspace docs or per-repo).
- repo-intent (11) -> the named repo's `INTENT.md`.
- junk-remove (7) -> DISCARD (already archived; no migration).

Open decisions for the psyche (track 4):

1. Is rehoming even wanted for all categories, or is "archived = safe, discard
   the rest" acceptable for skill/junk (the largest mechanical wins)?
2. The code/config (33) untracked-repo blocker: hold-and-edit untracked,
   transitional in-tree staging, or skip?
3. Routing granularity for architecture-doc (384): per-record vs per-cluster vs
   bulk-by-repo?
4. Sequencing: which category first (skill/junk discard is the cheapest;
   spirit-manual feeds track 5)?

## Track 5 — Spirit usage manual (psyche wants to use Spirit himself)

Direct answer: NO human-facing Spirit usage manual exists. There is an
AGENT-facing manual and a developer-facing README, but nothing written for a
non-agent psyche to record/query intent.

Observed — what exists:

- `repos/spirit/manual.md` — AGENT/system doctrine manual. Opens "Spirit is the
  intent layer... This manual explains what Spirit holds, how a statement
  becomes a record, how the guardian gate decides admission, how certainty and
  importance are set, how records age out, and the everyday CLI conventions." It
  is written to "the agent," "the submitting agent," "the operator lane (Codex)."
  8 sections (What Spirit Is; Intent Not Information; The Capture Flow; The
  Guardian Gate; Certainty and Importance; Record Lifecycle; Querying and
  Observing; CLI Basics). It teaches the MODEL of capture/query but its only
  literal CLI invocation is the bare-selector `spirit Version`; it shows no full
  `(Record ...)` / `(Observe ...)` command strings.
- `repos/spirit/README.md` — developer/operator README. It DOES carry real
  copy-pasteable command examples: a full `spirit "(Record (...))"`, three
  `spirit "(Observe (...))"` variants, `spirit "(PublicTextSearch [...])"`,
  `spirit Version`; plus the Query selector vocabulary (DomainMatch
  Partial/Full, optional kind `(Some Decision)`/`None`, certainty-floor
  convention). It assumes NOTA/schema fluency and daemon-startup knowledge.
- The `spirit-cli` SKILL (`.claude/skills/spirit-cli/SKILL.md`) — agent-facing.
  Documents: the CLI takes exactly one argument (inline NOTA starting with `(`,
  or a NOTA file path); the `Record` request = Entry + Justification; the 7
  positional Entry fields (domain vector, kind, description, certainty,
  importance, privacy, referents); the 8 magnitude rungs; capture discipline;
  Observe/Lookup/Count/maintenance ops. It is concise and assumes the reader is
  an agent.

Observed — the deployed CLI's actual operation surface (verified live):

- `(Lookup <id>)` -> `(RecordFound (<id> (<entry>)))`; bare id works, bypasses
  filters. Confirmed.
- `(Observe (<8-field Query>))` -> `(RecordsObserved [...])`. Query is 8
  positional fields: domain_match, keyword_match, text_match, referent_selection,
  selected_kind (Option<Kind>, so `None`/`(Some Kind)`), privacy_selection,
  certainty_selection, importance_selection. Each selection has an `Any` default;
  e.g. all-records = `(Any Any Any Any None Any Any Any)`. Confirmed.
- `(Count (<Query>))` -> `(RecordsCounted N)`. Confirmed (returned 22).
- `(PublicTextSearch <text>)` -> `(RecordsObserved [...])` or `(Error [no
  matching record])`. Confirmed.
- `(Record (<Entry> <Justification>))` -> Recorded receipt (capture side, not
  exercised here — read-only).
- `Version` bare selector exists. NOTE: `(Help)` exists in the signal-spirit
  source (`help.rs`, `HelpRequest`) but the deployed CLI REJECTS it: `spirit
  "(Help)"` -> "invalid NOTA input: unknown Input variant Help". So Help is not
  wired into the deployed Input enum / the deployed build predates it. (Flag.)

Observed — cross-reference to track 4: 76 removed records are tagged
"spirit-manual" (Spirit/guardian/certainty/capture mechanics, Spirit-usage,
agent-training material). These are the raw material a manual would absorb; they
were archived out of Spirit precisely because they were Spirit-usage matter, not
intent. The agent-facing `manual.md` already exists as their natural home.

Scout interpretation — the gap. A psyche-usable manual would need: (1) plain
"what Spirit is for you" framing (not "the submitting agent"); (2) a recording
walkthrough with the literal `spirit "(Record (...))"` shape and what each of
the 7 fields means in human terms; (3) a querying walkthrough (Lookup by id,
Observe with the common selectors, PublicTextSearch) with literal commands; (4)
how the Guardian may reject and what to do; (5) the magnitude vocabulary in
human terms. The README has the literal syntax; the manual has the model; the
skill has the discipline — but none is assembled for a non-agent human, and the
README assumes NOTA fluency. The 76 spirit-manual archived records plus
`manual.md` are the content reservoir; the work is assembly + audience-shift, not
discovery.

Open decisions for the psyche (track 5):

1. Build a dedicated human-facing manual, or extend `manual.md` / README with a
   "for the psyche" section?
2. Where does it live — `repos/spirit/`, workspace docs, or a top-level file the
   psyche reaches easily?
3. Should the 76 archived spirit-manual records be mined into it (track 4
   dependency), or is `manual.md` + README enough source?
4. Is the missing `(Help)` operation worth wiring into the deployed CLI as part
   of human usability?

## Track 6 — certainty vs importance (parked design Q)

Observed — definitions, from the authoritative Guardian source
(`repos/spirit/src/guardian-prompts/burden-ladder.md` and `checklist.md`, and
`repos/spirit/src/guardian_prompt.rs`) and `INTENT.md`:

- CERTAINTY is the BURDEN OF PROOF. "The advocate PROPOSES a burden by claiming
  a Certainty rung." A direct psyche declaration naming the rung supports it;
  otherwise the verbatim testimony must clear the rung on the words' MODAL
  STRENGTH, read off the quote, never the agent's prose. The ladder is ordinal:
  hedged (maybe/could/might) clears only Minimum/VeryLow/Low; a stated
  preference/should clears Medium; a flat commitment clears High; unhedged
  founding language (never/always/non-negotiable/"put this in essence") clears
  VeryHigh/Maximum (rare). Over-claim -> reject `Overstated`. This is Gate 9
  ("the signature gate"). Modality-off-the-quote is structurally enforced
  (records `so3b`, `woku`: the guardian never edits a magnitude itself).
- IMPORTANCE is a SEPARATE AXIS judged from its OWN evidence. A direct psyche
  declaration supports the rung; otherwise use recurrence, architectural
  centrality, blast radius, keeps-coming-up, or blocks-other-work. "High
  importance NEVER raises the certainty burden, and confident tone is NEVER
  evidence of importance." Minimum/Low/Medium importance are ordinary defaults
  needing no justification; only ELEVATED (High/VeryHigh/Maximum) must be backed,
  else reject `ImportanceUnsupported`. Canonical illustration: "A tentative idea
  the psyche keeps returning to is genuinely VeryLow certainty AND High
  importance — admit it at exactly that."
- INTENT.md confirms the storage separation: "Entry stores them separately.
  Certainty names confidence/currentness: Zero nominates a record for removal
  while direct Lookup remains possible. Importance names importance/repetition
  and drives retrieval order/filtering. Importance must not be overloaded onto
  certainty."

Observed — how each is USED:

- Certainty: (a) Guardian admission gate (Overstated); (b) lifecycle — Zero
  certainty = removal nomination / GC candidate while Lookup still works (the
  zero-cert GC of 739 records, commit 8048683e, used exactly this); (c) query
  floor — `certainty_selection` filters Observe/Count (the active set is
  cert >= VeryLow; the ledger dumped at AtLeastCertainty VeryLow).
- Importance: (a) Guardian gate (ImportanceUnsupported on elevated rungs); (b)
  retrieval order / filtering via `importance_selection`; (c) the Duplicate
  remand bumps the canonical record's importance (BumpImportance op).
- There are distinct wire ops for each: `ChangeCertainty`/`CertaintyChange` and
  `BumpImportance`/`ImportanceBump`. The 8-magnitude rung set is shared.

Observed — DISCERNMENT and PROPOSAL both treat certainty-vs-importance as
explicitly OUT OF SCOPE / psyche-parked. Neither recommends a change.

Scout interpretation — what dropping "certainty" (keeping only "importance")
would affect:

- It collapses two orthogonal axes the system currently relies on: the
  burden-of-proof gate (Overstated) loses its anchor; the canonical example
  "VeryLow certainty AND High importance" becomes inexpressible (a tentative idea
  the psyche keeps returning to could no longer be admitted honestly low).
- Lifecycle breaks: Zero-certainty = removal nomination is the whole soft-delete
  / GC mechanism. Without certainty there is no "nominate for removal but keep
  Lookup" state; removal becomes binary.
- The query certainty-floor convention disappears (the "show me removal
  candidates" / "active set only" filter).
- The `ChangeCertainty` op and the Overstated rejection reason become dead.
- Net: importance alone cannot carry confidence/currentness; merging them
  re-introduces exactly the "importance overloaded onto certainty" failure
  INTENT.md warns against. This is a substantial schema + Guardian + lifecycle
  change, not a cosmetic field drop.

Open decisions for the psyche (track 6): observation-only per the brief; the
parked question is whether the two-axis model is worth its complexity, knowing
that dropping certainty removes the burden-of-proof gate, the soft-delete/GC
state, and the certainty query floor.

## Track 7 — Appeals architecture and whole-cleanup audit

Observed:

- Appeals: NOTHING is built. The string "appeal" appears only in the DISCERNMENT
  report (forward design language). No spirit source, no skill, no bead, no
  config mentions an appeals mechanism. Confirmed by `rg` across the workspace
  (excluding target/private-repos/agent-outputs) and across `repos/spirit/src/`.
- Whole-cleanup audit: there is no dedicated bead or artifact for a "whole
  cleanup audit" found by name. The strict re-judge ledger is the closest
  existing audit (it judged all 650 once). Related live beads exist for Spirit
  sweeps: `primary-ptvb.3` (cut spirit-cli to capture-side reference),
  `primary-ptvb.9`/`.10` (retire vocabulary across record clusters),
  `primary-nlx5` epic (activate dormant guardian signals).

Scout interpretation (light touch, flagged design/future):

- Appeals = forward design only. Conceptually it would be a path to re-submit a
  Guardian-rejected record with added testimony/warrant, or to contest a
  rejection — but it is purely a future design surface, not parked work with
  ground truth to map.
- A whole-cleanup audit would plausibly cover: the 22 live keeps re-verified
  against the final strict bar; the six fused-source dispositions (track 1); the
  631 archive rehoming completeness (track 4); ESSENCE references (track 3); and
  consistency between manifested skills and surviving intent. It is a scoping /
  planning artifact, not built.

Open decisions for the psyche (track 7):

1. Is appeals worth designing now, or kept as future?
2. What is the intended scope/owner of a whole-cleanup audit — and is the
   re-judge ledger already enough?

## Track 8 — Two uncaptured intents

Direct answers (verified by live `PublicTextSearch` and `Lookup`):

- "A design is good design only once the psyche has acknowledged it" — NOT in
  live Spirit. `PublicTextSearch acknowledged`, `acknowledge`, `acknowledges`,
  `blessed` all return `(Error [no matching record])`. Searches for `good
  design` and `design surface` return only the existing design-cluster records
  (sj2c, jys2, cam8, izsf, gni3, 10pz, t5qr, obo5, qjrf) — none of which asserts
  the psyche-acknowledgment gate. This intent is uncaptured.
- "Ask the psyche when a design surface is incomplete" — partially present, NOT
  as a clean record. `PublicTextSearch incomplete` returns ONLY `qjrf`, where
  the maxim is welded to the capture-gate matter (see track 1). So the maxim
  exists in Spirit only inside the fused `qjrf` record; there is no standalone
  clean record for it. If qjrf is split (track 1), the clean half would become
  this record.

Scout interpretation: both are candidate captures. The acknowledgment intent is
fully uncaptured and is also a recurring theme in the artifacts (the DISCERNMENT
and ESSENCE both turn on "psyche-authorized / psyche acknowledges" — that the
design is the psyche's to bless). The incomplete-surface intent is half-captured
inside qjrf and is the cleaner of the two to extract.

Open decisions for the psyche (track 8):

1. Capture "a design is good design only once the psyche has acknowledged it" as
   a clean Spirit record? (Confirm testimony.)
2. Capture "ask the psyche when a design surface is incomplete" clean — and is
   this the qjrf split (track 1) or a separate fresh record?

## Key unknowns and blockers

- Verbatim testimony is not in the Observe/Lookup projection — only the
  clarified description shows. Every re-capture / split / merge decision (tracks
  1, 2, 8) must be confirmed against the raw psyche quote at execution time. The
  scout could not see the testimony from the read surface.
- Version drift: the PROPOSAL's deployment facts cite live 0.18.1 / main 0.19.0;
  the brief states deployed 0.20.0. The exact prompt build now live (which
  checklist/burden-ladder text is compiled into 0.20.0) was not re-verified
  against the running daemon — only the repo source was read. Whether the live
  0.20.0 carries the PROPOSAL's strict-bar prose or the DISCERNMENT's
  one-principle framing is unconfirmed from the read surface.
- ESSENCE deprecation (track 3) directly conflicts with the DISCERNMENT's
  preferred zn2l resolution (route telos INTO ESSENCE). One must give; this is a
  psyche decision, not a fact to resolve.
- The 631 archive rehoming (track 4) has an untracked-repo blocker for the
  code/config and much of the architecture-doc category: their homes are repos
  under `repos/` (untracked) or `private-repos/` (off-limits without
  authorization). Routing those needs a psyche hold/edit-untracked call.
- The bead `primary-lsip` says "remove its records" for ESSENCE, but ESSENCE has
  no Spirit records; this is loose wording that should be reconciled with the
  fact that ESSENCE is a prose file.
- `(Help)` is in signal-spirit source but rejected by the deployed CLI — whether
  this is intended or a deploy lag is unknown.
- The full per-record id lists for each track-4 category live in the ledger;
  this map did not re-verify each id against the archive store contents.

## Consolidated open decisions for the psyche (planning seed)

Track 1 — Fused sources: (1) o7zt remove-outright vs re-capture clean; (2) c5nq
/ hv5f remove-as-skill-restated vs keep one clean kernel; (3) k09z clean privacy
kernel wording; (4) qjrf split confirmation; (5) gni3 keep vs manual-matter;
(6) confirm all re-captures against testimony.

Track 2 — Telos trio: (1) merge jys2/sj2c/cam8 into one, two, or keep three;
(2) which testimony/certainty survives a merge; (3) relation to zn2l and the
ESSENCE-routing decision.

Track 3 — ESSENCE: (1) confirm deprecation; (2) resolve the zn2l-into-ESSENCE vs
deprecate-ESSENCE conflict; (3) per-section migration targets (esp. "Today and
eventually"); (4) what becomes the named top of the precedence stack.

Track 4 — Rehome 631: (1) rehome-vs-discard policy per category; (2)
untracked-repo blocker call for code/config; (3) routing granularity for the 384
architecture-doc; (4) sequencing.

Track 5 — Human manual: (1) dedicated manual vs extend manual.md/README; (2)
where it lives; (3) mine the 76 archived spirit-manual records; (4) wire `(Help)`
for human usability?

Track 6 — certainty vs importance: observation-only; the parked question is
whether to keep the two-axis model knowing dropping certainty removes the
burden-of-proof gate, the soft-delete/GC state, and the certainty query floor.

Track 7 — Appeals / cleanup audit: (1) design appeals now or keep future; (2)
scope/owner of a whole-cleanup audit (is the re-judge ledger enough?).

Track 8 — Uncaptured intents: (1) capture the
psyche-acknowledgment-gate intent? (2) capture "ask when a design surface is
incomplete" clean (as the qjrf split or fresh)?
