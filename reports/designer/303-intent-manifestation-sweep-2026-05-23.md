# 303 — Intent manifestation sweep — 2026-05-23

*Kind: Synthesis · Topic: intent manifestation pass coordinated with second-designer · 2026-05-23*

*Dispatched as the manifestation half of a coordinated designer
subagent pair (audit half ran in parallel). Manifests psyche intent
that had firm direction but no durable home yet, after subtracting
the work already landed by second-designer's `/159` meta-directory
(intents 270-276 + manifestation context for 244/251/252/255/256)
and `/160` (intent 280 — drop persona- prefix). Also subtracts
the work landed by prime designer's `/297-/302` (signal-persona-auth
rename, Help operations, agent identity, signal_cli! elegant macro,
operator audit).*

## §1 Frame

Spirit holds records 1-299 with the recent push falling 217-299.
The candidate set for this sweep was the records the dispatch
prompt named as confirmed-not-yet-manifested by second-designer:
244, 245, 246, 247, 248, 251, 252, 254, 255, 256, 257, 258, 259,
271, 272, 273, 274, 276. Subtracting:

- **Already in `signal-frame/ARCHITECTURE.md` §5** via
  second-designer/159/1 (jj change `2313c5ed`): records 244, 251,
  271, 272, 273 — three-tier sizing + 64-bit verb-namespace.
- **Already in `signal-version-handover/ARCHITECTURE.md`** via
  second-designer/159/3 (jj change `0cdcc1a7`) and
  `sema-engine/ARCHITECTURE.md` (jj change `e36c47b8`): record 274 —
  Mirror payload raw container.
- **Already a workspace skill** (`skills/nota-comments.md`, jj
  change `f93f5893`) via second-designer/159/4: record 276 —
  NOTA-as-comments.
- **Already in `persona/ARCHITECTURE.md`**: records 245/246/252 —
  Design D lossless cutover (§1.6.7), record 248 — primary-a5hu
  decomposition is bead-shaped (not ARCH), record 257 — Spirit
  v0.1.0 Path A is in the v0.1.0 retrofit narrative (lines 472-483),
  record 258 — selector-flip-aware routing is in §1.6.7 "Selector
  flips are just steady-state route changes", record 260 —
  Spirit-per-engine in §1.5 "Spirit-per-engine" subsection.
- **Already in `skills/component-triad.md`** via
  second-designer/159/2 (jj change `xrysrwxl`): record 270 —
  component binary naming convention.
- **Already in `signal-persona-origin/ARCHITECTURE.md` §1 owned
  surface (lines 56-63)**: record 261 — `EngineIdentifier` /
  `RouteIdentifier` / `ChannelIdentifier` rename rationale.
- **Already in design report `/298`**: record 263 — Help operations
  (but the workspace-cross-cutting discipline did not have a
  permanent home yet — see §2 below).
- **Already in design report `/300`-`/301`**: records 265, 266, 267
  — CLI macro caller injection + elegant signal_cli!.

That left a specific set of intent records still without a durable
guidance-file home, all carrying decided substance suitable for
manifestation without further psyche turn:

- **254** — designer pattern-based-decision authority
- **255** — designer high-ratification-probability authority
- **256** — audits feed bead filing
- **247** — gap-closure-vs-migration framing
- **259** — `ComponentName` → `ComponentPrincipal` /
  `ComponentInstanceName` planned split
- **229** — closing duplicate beads must preserve information
  from both
- **263** — Help operations as workspace-cross-cutting discipline
  (the design exists in `/298`, but `skills/component-triad.md`
  was missing the rule)

## §2 Per-intent manifestation log

| Record | Title | Target file (section) | Edit summary |
|---|---|---|---|
| 254 | Designer pattern-based decisions | `skills/designer.md` §"Designer authority — Pattern-based decisions" | New §, names the rule, cites worked examples 260/261, says decisions are captured via Spirit record + reversible if psyche disagrees |
| 255 | Designer high-ratification-probability recommendations | `skills/designer.md` §"Designer authority — High-ratification-probability recommendations" | New §, names the four standing leans (lossless / no-downtime / cheaper-simpler / mechanical renames) and the "Where the authority stops" carve-outs (competing-without-lean per 229; proposed-not-decided per Medium-certainty) |
| 247 | Gap-closure-vs-migration framing | `skills/designer.md` §"Designer authority — Gap-closure framing" | New §, names that migration work IS gap-closure-relevant; earlier gap-closure-as-separate-lens framing is relaxed; both kinds fold into the designer-feeds-operator pipeline |
| 256 | Audits feed bead filing | `skills/designer.md` §"Audits feed into bead filing" | New §, names the two natural directions: bringing code into constraint (witnesses for ARCH constraints) + end-to-end sandboxed engine testing; pairs with auditor role (intent 234) |
| 229 | Closing duplicate beads preserves information | `skills/beads.md` §"Duplicate — preserve information from both" | New § inside "When to close a bead", placed between "Superseded" and "Reformulated as a discipline"; names that competing design ideas in particular must not be collapsed |
| 263 | Help operations as discipline | `skills/component-triad.md` §"Help operations — discovery through NOTA, not through flags" | New §, placed after "The single argument rule"; names the two ops `(Help Main)` and `(Help (Verb <name>))`, why-forbidding-flags forces them, and the auto-injection-via-`signal_channel!` direction |
| 259 | `ComponentName` → `ComponentPrincipal` / `ComponentInstanceName` | `signal-persona-origin/ARCHITECTURE.md` §1 owned surface | Updated the `ComponentName` bullet to name the pending rename: `ComponentName` → `ComponentPrincipal` (closed enum, identity surfaces) in this crate; parallel open-newtype form `ComponentInstanceName` in `signal-persona`; bundled with the `EngineIdentifier` rename (records 277/278) |

Total: 5 workspace skill/`AGENTS` surface edits + 1 per-repo ARCH
edit + 1 substantive subsection added to an existing skill.

## §3 Skipped (with reason)

Records considered but not manifested in this sweep, with the
reason each:

| Record | Title | Reason for skipping |
|---|---|---|
| 217 | Port stale components to current foundations | Work-instruction; bead-shaped, not guidance-shaped |
| 218 | Long answers MUST go in reports | Already in AGENTS.md §"Reports go in files; chat is for the user" |
| 219 | Find implementable beads | Work-instruction |
| 220 | 3-7 chat items policy | Already in AGENTS.md §"Chat normal-response policy" |
| 221 | /287 substance distributes to per-repo ARCH | Bead-shaped follow-up, not a guidance-file rule |
| 222 | Encode 3-7 chat policy in AGENTS.md | Already done |
| 223-227 | Persona-Pi work direction | Bead-shaped; covered in active-repositories.md |
| 228 | Operator continues until no clear work remains | Work-instruction |
| 230 | Second-operator pivots from orchestrate-executor | Work-instruction |
| 231 | Sub-agent meta-report directory pattern | Already in AGENTS.md §"Meta-report directories" |
| 232 | Chat 3-7 items balanced across three categories | Already in AGENTS.md §"Chat normal-response policy" |
| 233 | Intent-and-design engine | Already in ESSENCE.md §"Intent and design — the engine's dance" and INTENT.md §"The engine is intent and design" |
| 234 | Auditor as third role | Already in AGENTS.md §"Possible additional role" and INTENT.md §"Possible additional role" |
| 235 | DeepSeek as auditor model | Already in AGENTS.md §"Possible additional role" and INTENT.md §"Possible additional role" |
| 236 | Third-designer report 20 relevant | Work-instruction |
| 237 | jj headless / no editor | Already in AGENTS.md §"Reach for the right tool, not raw git" + `skills/jj.md` |
| 238-239 | Persona is a permissioned system daemon | Already in `persona/ARCHITECTURE.md` §"Persona" |
| 240 | Persona uses systemd template units | Already in `persona/ARCHITECTURE.md` §1.6.7 and §"Component unit control" |
| 241 | Refresh reports and intent before selecting next work | Work-instruction |
| 242 | NOTA bracket-string migration | Gated on "after bracket-string support is well tested" — brainstorm-in-flight per `skills/intent-manifestation.md` §"When to skip"; awaits land of bracket-string parser |
| 243 | Visuals MUST be mermaid | Already in AGENTS.md §"Hard overrides" + `skills/reporting.md` |
| 244, 251, 271, 272, 273 | Three-tier signal sizing + 64-bit verb-namespace | Landed by second-designer/159/1 in `signal-frame/ARCHITECTURE.md` §5 |
| 245, 246, 252 | Lossless cutover routing Design D | Already in `persona/ARCHITECTURE.md` §1.6.7 |
| 248 | primary-a5hu decomposition | Bead-shaped |
| 249 | Vocabulary sweep | Already filed as `skills/workspace-vocabulary.md` |
| 250 | Library research beads | Bead-shaped |
| 253 | Second-operator may pick up any ready bead | Work-instruction |
| 257 | Spirit v0.1.0 Path A | Already in `persona/ARCHITECTURE.md` lines 472-483 v0.1.0 retrofit narrative |
| 258 | Selector-flip-aware routing | Already in `persona/ARCHITECTURE.md` §1.6.7 ("Selector flips are just steady-state route changes") |
| 260 | Spirit-per-engine | Already in `persona/ARCHITECTURE.md` §1.5 §"Spirit-per-engine" subsection |
| 261 | Identifier rename | Already in `signal-persona-origin/ARCHITECTURE.md` §1 owned surface |
| 262 | "auth" is forbidden abbreviation | Captured by the rename to `signal-persona-origin` (records 264, 297, 264 ratified) |
| 264 | signal-persona-auth → signal-persona-origin | Rename is in flight per `/297`; `protocols/active-repositories.md` already lists `signal-persona-origin` |
| 265, 266, 267 | CLI macro caller injection + elegant signal_cli! | Designs in `/300`-`/301`; operator beads filed per record 267; awaiting implementation before durable ARCH home — discipline tracking via the design reports until first implementation lands then arch-manifests |
| 268, 269, 277, 278 | Rename-pass bead bundling | Operator-side coordination; not guidance-shaped |
| 270 | Component binary naming | Landed by second-designer/159/2 in `skills/component-triad.md` |
| 274 | Mirror payload raw container | Landed by second-designer/159/3 in `signal-version-handover/ARCHITECTURE.md` |
| 275 | persona-mind agent-error events | Design phase per second-designer/159/5; bead `primary-x0qm` filed; ARCH-manifest awaits persona-mind production deployment |
| 276 | NOTA-as-comments | Landed by second-designer/159/4 as `skills/nota-comments.md` |
| 279 | Lane identifiers use exact role-name | Already in `skills/role-lanes.md` |
| 280 | Drop persona- prefix from supervised components | Manifestation is the coordinated rename pass per second-designer/160; per-file edits await operator/system-specialist pickup; not a guidance-file rule but a workspace mechanical change |
| 281-299 | Cloud / domain-criome direction, meta-signal rename, etc. | New-component design + Medium-certainty rename direction; already captured in `protocols/active-repositories.md` Adjacent Active Work table; meta-signal rename is proposed-not-decided per record 299 |

## §4 Cross-cutting observations

### §4.1 Designer authority discipline now has a single home

Records 254, 255, 256, 247 all spoke to **what the designer may
decide without a fresh psyche turn, what the designer holds back
on, and how audits feed forward**. These previously lived only in
the Spirit log; agents working in the designer lane could not
easily pick up the discipline without re-reading the relevant
records each session. The new `skills/designer.md` §"Designer
authority — when to act without explicit psyche approval" + §"Audits
feed into bead filing" sections gather them.

The grouping turns out cleanly: pattern-based + high-ratification
+ the explicit gap-closure framing form one connected discipline
of "designer forward motion"; audits feed the operator pipeline as
the natural output of that motion. Both subsections cite the
Spirit records they manifest so future agents can trace back.

### §4.2 Auditor / designer / operator loop is shaping up

Three sections across this sweep + second-designer's manifestation
landed pieces of the auditor → designer → operator loop:

- **AGENTS.md + INTENT.md** carry the auditor as proposed-not-
  decided (records 234/235; DeepSeek named, automation desired).
- **`skills/designer.md` §"Audits feed into bead filing"** (new
  this sweep) names the natural output of an audit: operator beads
  for constraint witnesses + integration coverage.
- **`reports/second-designer/159/5`** (Spirit record 275) sketches
  persona-mind's AgentError typed events as the substrate the
  auditor will read.

The loop is not yet closed (auditor doesn't exist; persona-mind
isn't producing AgentError events yet), but the design surface
spans three guidance files now plus one bead (`primary-x0qm`).

### §4.3 Help operations and Caller — same pattern, different macros

Records 263 (Help) and 265/266 (Caller via signal_cli!) are both
**workspace-cross-cutting capabilities auto-injected at the macro
layer**, applied to every component contract or every CLI binary
respectively. Records 263 lands in `skills/component-triad.md` as a
discipline rule (this sweep); 265/266 live in `/300`-`/301`
awaiting implementation before they crystallize as `skills/`
discipline. Once both ship, a follow-up sweep should crystallize
the larger pattern — "macros auto-inject universal cross-component
capabilities; per-component declarations carry only the
component-specific verbs" — as either a new skill or an addition to
`skills/component-triad.md` §"Compile-time module index" or its
neighbor.

### §4.4 Where the persona- prefix rename intersects this sweep

The coordinated rename per second-designer/160 (intent 280)
re-targets `persona-spirit` → `spirit`, `persona-mind` → `mind`,
etc., across 24 repos. The edits this sweep made cite current
(pre-rename) names: `signal-persona-origin`, `persona-spirit`,
`persona-orchestrate`. Post-rename these citations need a sweep,
landed naturally by the Phase-5 ARCH+skill+workspace refresh from
`/160` §4. No special action this sweep — the rename touches a
larger surface than this sweep's edits and the cascade is already
planned.

### §4.5 What this sweep did not touch — operator beads

Several manifestations carry implied operator follow-ups:

- Record 263 (Help operations) implies an operator bead for the
  `signal_channel!` macro extension that emits the Help arm. The
  design exists in `/298`; per record 267, an operator bead chain
  is already filed for the related signal_cli! work. Help is a
  parallel macro extension that may bundle with that work or file
  its own bead. Open follow-on (not for this sweep).
- Record 259 (ComponentName rename) implies an operator bead for
  the source-level rename. Per Spirit records 277/278, this is
  bundled with the `signal-persona-auth → signal-persona-origin`
  crate rename. Existing bead `primary-7ru6` carries the
  Identifier rename; bundling per record 277. No new bead from
  this sweep.

The manifestations name the discipline; the implementation beads
exist or will exist in the operator filing pass triggered by
records 267/277/278.

## §5 See also

Within this directory and the sibling second-designer directory:
- `reports/second-designer/159-intent-manifestation/` — the parallel
  meta-directory that landed intents 244, 251, 270-276 + manifestation
  context for 245/246/252/255/256
- `reports/second-designer/160-persona-prefix-removal-coordinated-rename-2026-05-23.md` — intent 280's rename map

Workspace files edited this sweep:
- `skills/designer.md` — added §"Designer authority" + §"Audits feed
  into bead filing"
- `skills/beads.md` — added §"Duplicate — preserve information from
  both" inside "When to close a bead"
- `skills/component-triad.md` — added §"Help operations — discovery
  through NOTA, not through flags" after §"The single argument rule"
- `signal-persona-origin/ARCHITECTURE.md` — extended `ComponentName`
  bullet in §1 owned surface with the pending rename note

Spirit records this sweep manifests:
- 247 (workspace, Decision, gap-closure-vs-migration)
- 254 (workspace, Principle, pattern-based decisions)
- 255 (workspace, Principle, high-ratification-probability)
- 256 (workspace, Decision, audits feed bead filing)
- 229 (beads, Principle, duplicate-bead information preservation)
- 259 (signal, Decision, ComponentName → ComponentPrincipal split)
- 263 (component-shape, Decision, Help operations universal)

Prime designer adjacent reports:
- `reports/designer/297-design-signal-persona-auth-rename.md`
- `reports/designer/298-design-help-operations-in-components.md`
- `reports/designer/299-design-origin-process-and-agent-identity.md`
- `reports/designer/300-design-cli-macro-caller-context-injection.md`
- `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md`
- `reports/designer/302-audit-recent-operator-work-2026-05-23.md`
