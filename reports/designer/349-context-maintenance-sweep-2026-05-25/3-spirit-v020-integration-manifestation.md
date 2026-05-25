# 3 — Spirit v0.2.0 integration manifestation

*Subagent C — coupled context-maintenance + intent-manifestation
sweep dispatched 2026-05-25. Manifests the Spirit v0.2.0 deployment
findings (operator's /187, designer's /347) and the relevant intent
records (672-678) into permanent docs.*

## What was found

### The intent surface — records 672-678

Walked the live intent layer at records 670-706 (the slice that
drove the v0.2.0 cutover decision). The Spirit-deployment cluster:

| Record | Topic | Kind | Substance |
|---|---|---|---|
| 672 | workspace | Clarification | Next/main/previous vocabulary — *authors always write from the point of view of next; main is the imported baseline; previous is the prior reference retained for handover*. Applies broadly; the v0.2.0 deployment is one instance. |
| 673 | spirit | Decision | Spirit next entries carry one clarified description and no verbatim field. |
| 674 | spirit | Decision | Spirit record acknowledgements stay terse — `(RecordAccepted N)`, no echo. |
| 675 | spirit | Decision | Spirit timestamp is daemon-stamped. |
| 676 | spirit | Decision | Spirit topics are user-creatable single strings. |
| 678 | spirit | Principle | Agents clarify psyche wording into the Spirit description (the agent's job, not the daemon's). |
| 691 | spirit | Constraint | Intent capture should become denser and less verbose — durable records preserve clarified intent without large verbatim blocks. |
| 699 | spirit | Decision | Migrate live Spirit to v0.2 now. |
| 700 | spirit | Correction | Spirit CLI calls wrap the whole NOTA argument in shell double quotes (NOTA has no `"` inside; the shell double quote is the clean outer boundary). |

These cohere as one tight discipline cluster: the v0.2.0 wire shape
strips verbatim/context, the daemon stamps time, replies stay
terse, topics are free strings, and the agent does the clarifying
work upstream of the record. Records 672 + the deployment-slot
mechanism in /187 are the same discipline projected onto two
surfaces (codebase + deployment naming).

### The deployment state — /187

Operator deployed Spirit v0.2.0 as a Home Manager side-by-side
service on `ouranos`:

- `persona-spirit` tag `v0.2.0` → `ba1956d23217`
- New CriomOS-home flake input `persona-spirit-v0-2-0`
- New service `persona-spirit-daemon-v0.2.0.service` — active
- New wrapper `spirit-v0.2.0` in the user profile
- Segregated state under `~/.local/state/persona-spirit/v0.2.0/`
- Unsuffixed `spirit` still resolves to v0.1.0 (production unchanged)
- Profile shows the slot pattern: `spirit` / `spirit-v0.1.0` /
  `spirit-v0.1.1` / `spirit-v0.2.0` / `spirit-next` (the next slot
  reserved, currently missing)

The daemon's `ExecStart` is the canonical 9-field configuration
witness: three sockets (ordinary/owner/upgrade), one redb database
path, one magnitude limit (`384`), four trailing `None`-slot
extension points.

Live wire usage verified: `(RecordAccepted 1)` on Record, expected
subsets on Observe with topic/kind filters, terse replies
throughout, bracket strings on every CLI call.

### The integration audit — /347

The designer's /347 layered context onto the deployment:

- The schema-driven feature branch `designer-schema-full-stack-spirit-2026-05-25`
  at `e0378b8d` is a **sibling fork** of v0.2.0, not parent-child.
  Common ancestor `f2c1538aad00`. Operator integration of the
  schema-driven branch will rebase / merge onto the v0.2.0 baseline.
- The schema-driven branch's dual-emission compatibility approach
  (legacy `signal_persona_spirit::Operation` stays at the root;
  schema-driven types land under `::spirit::*`) was designed
  precisely for this integration scenario — both surfaces survive
  simultaneously.
- The 9-field daemon configuration shape is a schema-emission
  opportunity (future operator slice; not blocking).
- The `spirit-next` slot is the natural deployment surface for the
  schema-driven branch as an unreleased preview before v0.3.0
  tagging.

The substance of /347 is mostly **deployment integration analysis**
— how the operator's /187 deployment substrate interacts with the
designer's schema-driven branch. Mature enough to migrate; the
discipline pieces have landed in skills + INTENT, and the operator
action items are tracked through the upgrade-chain beads, not by
keeping the report.

## Migration map — record → destination

| Record | Destination edit |
|---|---|
| 672 (next/main/previous) | `skills/spirit-cli.md` §"Deployment slots" — projected onto deployment-naming; persona-spirit `INTENT.md` §"Deployment — next, main, previous side-by-side" |
| 673 (description-only) | `skills/spirit-cli.md` §"Record an intent entry — description-only is the v0.2.0 shape"; persona-spirit `INTENT.md` §"v0.2.0 wire discipline" |
| 674 (terse acks) | `skills/spirit-cli.md` §"Record an intent entry" (reply paragraph); persona-spirit `INTENT.md` §"v0.2.0 wire discipline" |
| 675 (daemon-stamped time) | `skills/spirit-cli.md` §"Record an intent entry" (daemon stamp emphasised); persona-spirit `INTENT.md` §"v0.2.0 wire discipline" |
| 676 (user-creatable topics) | `skills/spirit-cli.md` §"Topics are user-creatable" (new paragraph); persona-spirit `INTENT.md` §"v0.2.0 wire discipline" |
| 678 (agent clarifies wording) | `skills/spirit-cli.md` §"Record an intent entry" (description-clarification paragraph); persona-spirit `INTENT.md` §"v0.2.0 wire discipline" |
| 691 (denser intent capture) | persona-spirit `INTENT.md` §"v0.2.0 wire discipline" (forcing function) |
| 700 (shell double quote wrap) | `skills/spirit-cli.md` §"How to invoke" (existing — strengthened with the no-`"` -inside framing) |
| /187 (9-field daemon config) | `skills/spirit-cli.md` §"The daemon's single-argument configuration" (new); persona-spirit `INTENT.md` §"Daemon configuration — 9-field positional argument" (new) |
| /187 (side-by-side pattern) | `skills/spirit-cli.md` §"Deployment slots"; persona-spirit `INTENT.md` §"Deployment — next, main, previous side-by-side" |
| /347 (sibling-fork topology, schema-driven integration path) | Substance migrated; report retired (see below). Operator-action items track through the upgrade-chain beads, not the report. |

## Edits applied directly

### `/home/li/primary/skills/spirit-cli.md`

Four refinements absorbed:

1. **Header path note** — corrected `~/.local/state/persona-spirit/`
   to `~/.local/state/persona-spirit/<version>/` to reflect the
   versioned-directory side-by-side reality.
2. **New section §"Deployment slots"** — names the
   `spirit` / `spirit-vX.Y.Z` / `spirit-next` pattern explicitly,
   maps to next/main/previous vocabulary, gives the `readlink -f`
   discovery command, and frames cutover as alias change rather
   than destructive replace.
3. **§"How to invoke" strengthened** — explicit "**Wrap the whole
   NOTA expression in shell double quotes**" framing; explained why
   (NOTA bracket strings have no `"` inside, shell double-quote is
   the clean boundary); flagged single-quoting as wrong (loses
   apostrophes).
4. **§"Operations on the ordinary channel" reshaped** — description-
   only record shape now front-and-centre with the agent-clarifies
   discipline (record 678) and the dense-not-verbose forcing
   function (record 691); terse-reply discipline (record 674) named
   in the same paragraph; daemon-stamped time (record 675) framed
   as a deliberate decision; user-creatable single-string topics
   (record 676) added as its own paragraph.
5. **New section §"The daemon's single-argument configuration"** —
   names the 9-field positional shape, the four `None` extension
   slots, the discovery command (`systemctl --user cat …`), and
   the forward-look to schema-emitted configuration once
   schema-driven substrate matures.

### `/git/github.com/LiGoldragon/persona-spirit/INTENT.md`

Three new sections appended before §"See also":

1. **§"Deployment — next, main, previous side-by-side"** — names
   the side-by-side substrate, the segregated-per-version state,
   the next/main/previous vocabulary applied to deployment naming,
   and the cutover-as-alias-change discipline. Names the v0.2.0
   deployment as the empirical validation. Verbatim psyche quote
   from record 699 in italics.
2. **§"v0.2.0 wire discipline — description-only, terse,
   daemon-stamped"** — records 673, 674, 675, 676, 678, 691
   synthesised. Verbatim psyche quotes in italics inline.
3. **§"Daemon configuration — 9-field positional argument"** —
   summarises the 9-field shape, the `None`-slot extension
   pattern, the forward-look to schema-emitted configuration.

§"See also" updated: added cross-reference to
`skills/spirit-cli.md` for the deployed-CLI invocation discipline.

The architecture-section area (top of INTENT.md) was deliberately
left untouched to avoid stepping on Subagent A's schema-driven
architecture additions. All my additions land below the existing
content.

## Proposed shared-file edits

### `INTENT.md` (workspace) — new section

Propose adding the following section after §"Two deploy stacks
coexist" (the existing deployment-discipline section in the
workspace INTENT). This synthesises the v0.2.0 deployment state
for fresh-agent onboarding without duplicating the per-repo detail
that lives in `persona-spirit/INTENT.md`.

```markdown
## Spirit deploys side-by-side; cutover is an alias change

The Spirit substrate ships side-by-side under
`~/.local/state/persona-spirit/<version>/` with one tag-suffixed
wrapper per release (`spirit-vX.Y.Z`), a `spirit-next` slot for
the in-flight authoring branch, and the unsuffixed `spirit`
symlink pointing at the current production target. Each daemon
has its own sockets and its own redb database; versioned daemons
never share files. Cutover from one production version to the
next is an alias change, not a destructive replace — the older
daemon stays installed and reachable through its tag-suffixed
wrapper.

This is the next/main/previous vocabulary applied at the
deployment layer: *what is being authored IS next; the current
published baseline IS main; previous is the prior release
retained for handover.* The v0.2.0 deployment validated the
pattern: production stayed on v0.1.0 while v0.2.0 ran in
parallel for explicit testing through `spirit-v0.2.0`. Full
discipline: `skills/spirit-cli.md` §"Deployment slots".

The current deployed substrate (Spirit 0.2.0) carries one
agent-clarified description per record, a kind, a magnitude, and
a daemon-stamped timestamp; replies are terse
(`(RecordAccepted N)`, no echo); topics are user-creatable
single strings. *"Migrate live Spirit to v0.2 now."* The
schema-driven persona-spirit feature branch
(`designer-schema-full-stack-spirit-2026-05-25`) is a sibling
fork of v0.2.0 awaiting operator integration; the schema-driven
substrate is the candidate to fill `spirit-next` once integrated.
```

The orchestrator should consolidate this with Subagents A and B's
INTENT.md proposals (NOTA discipline, schema-driven architecture)
before applying — they may want neighbour sections.

### `AGENTS.md` (workspace) — no proposed change

The existing AGENTS.md already carries `skills/spirit-cli.md` in
the Required Reading discipline cluster (under §"Capture intent
through Spirit FIRST when a psyche prompt arrives"). The deployment-
slot, description-only, and daemon-stamped disciplines are
appropriately topic-specific — they belong in the skill, not on
every keystroke. No AGENTS.md addition needed.

### `ESSENCE.md` — no proposed change

No record in the 672-700 slice rises to ESSENCE bar.

## Reports retired

### `/347` retired

`reports/designer/347-spirit-v020-schema-driven-integration-2026-05-25.md`
— substance migrated as listed in the migration map above. The
deployment-discipline content lives in `skills/spirit-cli.md` +
`persona-spirit/INTENT.md`; the operator-action items (rebase
schema-driven branch onto v0.2.0; decide path A vs path B for
`spirit-next`; future `spirit-daemon-config.schema`) are tracked
through the upgrade-chain beads rather than the report. The
sibling-fork-topology mermaid is preserved in git history; the
substance — that v0.2.0 and the schema-driven branch are
complementary and need rebase-style integration — is captured in
the persona-spirit INTENT deployment section.

Retire command (jj headless):

```sh
jj describe -m 'retire designer/347 — substance migrated to skills/spirit-cli.md + persona-spirit/INTENT.md + INTENT.md (subagent C of /349)'
```

Then `jj split` or direct file deletion in the same change.

### `/187` retained — cross-role

`reports/operator/187-spirit-v0-2-0-side-by-side-deployment-2026-05-25.md`
is operator-owned. Substance was manifested without retiring the
source; operator owns their report retirement decision per the
cross-role discipline (designer doesn't touch operator/).

## Carry-forward — not blocking but worth surfacing

- The `spirit-next` slot is empty. Per /347 §6, the schema-driven
  feature branch is the candidate fill. Either Path A (release as
  v0.3.0 once integrated) or Path B (use `spirit-next` for an
  unreleased preview) is reasonable; the recommendation in /347
  was Path B for immediate exposure. Operator + system-specialist
  decision; not designer's call.
- The 9-field daemon configuration is hand-authored. Future
  `spirit-daemon-config.schema` would emit it from a schema
  declaration. Tracked in persona-spirit/INTENT.md §"Daemon
  configuration" as the forward-look; not blocking.
- `lojix-cli` still uses quoted-string NOTA per /187 §Notes; record
  690 wants bracket strings universally. Migration debt tracked
  through the heresy-sweep workflow (Subagent B may have surfaced
  this in their NOTA-discipline manifestation).

## References

- `/home/li/primary/skills/spirit-cli.md` — primary destination,
  refined in this pass.
- `/git/github.com/LiGoldragon/persona-spirit/INTENT.md` — per-repo
  destination, deployment sections appended.
- `/home/li/primary/reports/operator/187-spirit-v0-2-0-side-by-side-deployment-2026-05-25.md`
  — cross-role source, retained.
- Spirit records 672, 673, 674, 675, 676, 678, 691, 699, 700 — the
  intent surface manifested into the destinations above.
