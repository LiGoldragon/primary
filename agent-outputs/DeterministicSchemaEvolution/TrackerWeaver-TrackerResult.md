# Tracker Result: Deterministic SEMA Schema Evolution

## Task and scope

Tracker-weaver was asked to mutate tracker state only as needed for the first vertical slice toward deterministic SEMA schema evolution. No code was implemented.

## Evidence and commands consulted

Read local instructions:
- `AGENTS.md`

Tracker inspection to avoid duplicates:
- `bd --help | sed -n '1,120p'`
- `bd show primary-g0u6 primary-la7q primary-wehu primary-x5ba primary-7kpe primary-l3h5.1 primary-l3h5.2 primary-l3h5.3 primary-l3h5.4 primary-l3h5.5 primary-l3h5.6 primary-5cxj primary-602y primary-0jjz primary-1jql primary-ekxx primary-x3ci primary-tfdj primary-l9iz primary-cklr primary-zfxx`
- `bd search "upgrade-as-SEMA" --json`
- `bd search "schema-daemon" --json`
- `bd search "deterministic schema" --json`
- `bd search "schema evolution" --json`
- `bd search "schema diff" --json`
- `bd list --status open --type epic --json`
- `bd search "UpgradeRule" --json`
- `bd search "upgrade rule" --json`
- `bd search "family hash" --json`
- `bd list --status open --json | jq -r '.[] | select((.title+.description) | test("upgrade|evolution|diff|SEMA|schema"; "i")) | [.id,.issue_type,.status,.priority,.title] | @tsv' | head -100`

Tracker mutations:
- `bd create "Deterministic SEMA schema evolution" -t epic -p 1 -l schema,sema,upgrade,evolution,deterministic --description ... --acceptance ... --json`
- `bd show primary-xi6z`
- `bd create "Build schema diff awareness tool for old/new SEMA schemas" -t task -p 1 --parent primary-xi6z -l schema,sema,upgrade,diff,first-slice --description ... --acceptance ... --json`
- `bd show primary-xi6z.1 && bd children primary-xi6z`
- `bd show primary-xi6z`

No lock retry was needed.

## Beads changed

### `primary-xi6z` — OPEN epic

Title: `Deterministic SEMA schema evolution`

Purpose: parent epic for deriving deterministic, recreatable component upgrade flows from old/new SEMA schemas via core/schema/SEMA machinery, not agent judgment or per-component hand-implemented upgrade flows.

Status after mutation: `open`, priority `P1`, type `epic`.

Dependency graph:
- Parent of `primary-xi6z.1`.

### `primary-xi6z.1` — OPEN first implementation bead

Title: `Build schema diff awareness tool for old/new SEMA schemas`

Status after mutation: `open`, priority `P1`, type `task`.

Parent/dependency graph:
- Parent: `primary-xi6z`.
- No other blockers/dependencies were added.

Acceptance criteria captured:
- deterministic old/new SEMA schema diff report;
- detects added/removed/likely-renamed families;
- detects added/removed/likely-renamed fields;
- detects type changes;
- detects key/storage identity changes;
- detects family hash changes;
- classifies each change as `auto-safe`, `needs explicit upgrade rule`, or `unsupported`;
- explains schema facts behind classifications;
- includes tests/fixtures covering all detection/classification categories;
- is read-only: no live store mutation, daemon state mutation, selector flip, or silent compatibility shim;
- avoids mirror-as-noun framing.

## Beads left open

- `primary-xi6z` remains open as the parent epic.
- `primary-xi6z.1` remains open for implementation.

## Implementer handoff

Pick up `primary-xi6z.1`. Build the first slice as a read-only schema diff awareness tool/library entry point over old/new SEMA schema inputs. Keep output deterministic and stable. Do not mutate redb stores, component daemon state, or deployment selectors. Anchor to schema-emitted Signal/Nexus/SEMA and current `sema`/`signal-sema`/`sema-engine` direction; do not revive retired persona-spirit handover or direct mirror-daemon migration paths. Treat mirroring only as a verb if it appears at all.

## Blockers

None.
