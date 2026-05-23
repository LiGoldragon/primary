*Kind: Design · Topic: sema-upgrade-and-version-handover-current-state · Date: 2026-05-24*

# 315 — Sema-upgrade and version-handover current state

*Re-contextualised consolidation of `/270` (original sema-upgrade
triad design, 2026-05-21) and `/273` (post-operator/151 synthesis,
2026-05-21). Re-shaped against current ARCH landings + spirit
records to 365 + the canonical vocabulary (Persona-as-orchestrator,
main/next, no `current/`, no `engine manager`). Stands as the source
for bead `primary-ib5n` (canonical sema-upgrade + nota-schema
architecture merge).*

## §1 What's already in permanent docs

The version-handover stack is the load-bearing path to the first
real cutover (Spirit v0.1.0 → v0.1.1). Substance has migrated to
per-repo ARCH files via designer/289 (now retired in this sweep —
substance lives in the per-repo ARCH commits below):

| Repo | ARCH content | Commit |
|---|---|---|
| `version-projection` | Full trait + policy taxonomy + 32-byte `ContractVersion` + Migration index | `b5adda0c` |
| `signal-version-handover` | Operation table + sequence diagram + wire vocabulary + 7 testable Constraints | `eb80f588` |
| `sema-engine` | `CommitSequence — durable high-water mark for handover` section | `8a740ac1` |
| `sema-upgrade` | Two-role TL;DR (protocol witness + sandbox host) + Possible features | `5dd65bc3` |
| `persona-spirit` | Explicit `Active / HandoverMode / PrivateUpgradeOnly` state diagram | `f1e2223b` |
| `persona` | §1.6.7 Persona-as-upgrade-orchestrator + §1.5 Spirit-per-engine | various |

Foundation crates landed (operator/158, /160, /161). End-to-end
sandbox migration proven against persona-spirit (217-record
migration through smart handover). The canonical visual reference
is `reports/designer/287-version-handover-component-explained.md`;
the canonical spec is
`reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`.

## §2 What still warrants design work

The bead `primary-ib5n` carries four merge slices. Three of them
have permanent homes already (per §1); one is genuinely-open.

### §2.1 The sema-upgrade-daemon triad — under consideration

The original `/270` design proposed a full triad component:
`sema-upgrade-daemon` runtime + `signal-sema-upgrade` working
contract + `owner-signal-sema-upgrade` policy contract + `upgrade`
CLI. Persona currently owns the orchestration of version handover
(spirit records 208/209/210 — Persona drives via owner sockets);
the `sema-upgrade-daemon` does not exist on disk.

Open question (carries forward from /270 §9 question 5; restated
against current state): does `sema-upgrade-daemon` ever emerge as a
separate triad, or does Persona absorb the orchestration role
permanently? Two coherent shapes:

- **Persona-absorbs.** Persona's §1.6.7 already drives handover;
  schema-catalogue and approval policy could live in Persona's
  policy substrate. No new daemon. Drawback: Persona's scope
  widens beyond engine supervision into schema policy.
- **Separate daemon.** A `sema-upgrade-daemon` owns the schema
  catalogue, approval policy, throttle, quarantine, and migration
  history. Persona delegates handover orchestration to it via
  signal calls. Drawback: third daemon in the upgrade path
  (Persona + sema-upgrade-daemon + component), wire latency.

The current `sema-upgrade` crate's ARCH names this open question
explicitly in its Possible-features. **Designer lean: persona-absorbs
until a second component's cutover demonstrates a scope problem.**

### §2.2 Owner-signal-version-handover contract

Bead `primary-7kge` (P1) carries the contract crate. ARCH stubs in
both `version-projection/ARCHITECTURE.md` and
`signal-version-handover/ARCHITECTURE.md` name
`owner-signal-version-handover` as Possible-features. The contract
shape (ForceFlip / Rollback / Quarantine per spirit record 214) is
settled; only the crate skeleton remains.

### §2.3 Mirror payload typed shape

Three ARCH files (version-projection, signal-version-handover,
sema-upgrade) name "Mirror payload typed shape" as a coordinated
Possible-features entry. Today the Mirror frame carries bytes plus
`RecordKind`; alternative is a typed enum forcing
`version-projection` to import every signal-X crate.

Per spirit record 274 (Maximum certainty): Mirror payload stays raw
bytes in a separate container — the typed-enum alternative is
rejected because of the cross-crate dependency cost. **The
Possible-features entries in all three ARCH files can retire to a
single sentence stating "Mirror payload is raw bytes in its own
container per signal-version-handover §X."**

### §2.4 Recursive bootstrap

Open question (carries from /270 §9 question 3): if sema-upgrade's
own contracts evolve, who upgrades sema-upgrade? Two coherent shapes:

- **Self-dogfood once.** sema-upgrade migrates itself via its own
  protocol the first time its contracts change.
- **Hand-written boot path** until sema-upgrade's contracts
  stabilise; dogfood after.

**Designer lean: hand-written until stable.** The state machine
contract is in `sema-upgrade/src/handover.rs`; the first contract
revision will hand-write the migration path; after the third stable
release, dogfood the protocol.

## §3 Type-family split — already absorbed

The /273 refinement (two type-families: public-signal historical
types live in `signal-<component>` + `owner-signal-<component>`;
private-storage historical wrappers like `StoredRecord` /
`StampedEntry` live in `<component>` runtime crate) is implicit in
the deployed code and operator/158's frozen-v1 layout. Schema
visibility annotation in /263's language (`(public)` / `(private)`)
is named in `nota/ARCHITECTURE.md` Possible-features (open question
for the schema-language design layer).

## §4 Commit-sequence — already absorbed

The /273 commit-sequence high-water-mark proposal landed end-to-end
in `sema-engine/ARCHITECTURE.md` §"CommitSequence — durable
high-water mark for handover" + `Engine::current_commit_sequence`
API + `replay_from_sequence`. Per-database scope (operator/158
implementation matches /273 §6b "per-database" lean).

## §5 The 0.01 file-substrate migration — superseded

The original /270 §4 pilot framed legacy `intent/*.nota` as a "0.01
schema" sema-upgrade would translate to current Spirit. This framing
is superseded by spirit records 167/168 (Maximum certainty:
*"Why are you logging in the files? We are not using the files
anymore, we are using Spirit"*) and the workspace AGENTS.md
substrate-cutover rule. The legacy files are read-only historical;
no migration tool ports them automatically. The first cutover
exercises sema-upgrade against deployed Spirit v0.1.0 records (the
217-record migration in `spirit-smart-handover-sandbox`), not
against the legacy files.

## §6 Open psyche question carried forward

**Spirit-cutover sequencing.** Persona must land before Spirit
cutover (record 209); `primary-a5hu` (Persona epic) blocks
`primary-x3ci` (Spirit cutover). The work-in-flight observability
question — does Persona own progress reporting during a multi-step
sema-upgrade migration, or does sema-upgrade emit Tap events that
Persona forwards? — remains unsettled. The current `sema-upgrade`
ARCH is silent; the universal Tap/Untap mandate would push the
events toward sema-upgrade emitting + Persona observing.

## §7 What this report supersedes

- `reports/designer/270-sema-upgrade-component-design.md` —
  original triad design; substance migrated to per-repo ARCH and
  this report's §2.1 (daemon-shape open question).
- `reports/designer/273-schema-migration-synthesis-post-operator-151.md`
  — type-family split (§3 above, already absorbed); commit-sequence
  (§4 above, already absorbed); Shape A vs Shape B chosen Shape A
  (foundation landed).

## §8 What carries forward

Bead `primary-ib5n` (P2) — canonical sema-upgrade + nota-schema-
language architecture merge — references this report as the source
of substance. The merge slice now reads:

1. nota-schema-language → `nota/ARCHITECTURE.md` (per /263 +
   /279; both still independent; not consolidated here).
2. sema-upgrade orchestrator shape → see §2.1 of this report;
   open question whether daemon emerges separately.
3. Owner-signal-version-handover → `primary-7kge` (P1).
4. Mirror payload + commit-sequence + type-family → already
   absorbed (§§3–4).

## See also

- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`
  — canonical spec (protected).
- `reports/designer/287-version-handover-component-explained.md`
  — canonical visual reference (protected).
- `reports/designer/263-schema-specification-language-design.md`
  — schema-language design (independent).
- `reports/designer/279-nota-schema-language-and-version-hash.md`
  — content-addressable schema-version hash (independent).
- `version-projection/ARCHITECTURE.md`,
  `signal-version-handover/ARCHITECTURE.md`,
  `sema-engine/ARCHITECTURE.md`, `sema-upgrade/ARCHITECTURE.md`,
  `persona-spirit/ARCHITECTURE.md`, `persona/ARCHITECTURE.md` —
  per-repo permanent homes.
- Spirit records 177–214 (sema-upgrade design arc), 207 (commit-
  sequence pre-cutover), 208–210 (Persona drives handover), 214
  (owner-signal-version-handover), 274 (Mirror payload raw bytes).
- Bead `primary-ib5n` (P2 architecture merge), `primary-7kge` (P1
  owner-signal contract), `primary-x3ci` (Spirit cutover),
  `primary-a5hu` (Persona epic — blocker).
