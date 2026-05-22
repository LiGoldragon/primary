# 260 — Schema migration discipline for persona daemons

*The problem the psyche surfaced 2026-05-21: a persona daemon and
its persistent database evolve together when the signal contract
or storage schema changes, and the workspace has no pattern for
the coherent migration. This report sketches the dimensions and
four candidate approaches, then asks the load-bearing questions
before any approach is picked.*

## Problem

A persona daemon is a binary plus a redb database. The binary
declares the wire vocabulary through its `signal-<component>` crate
(the working contract) and the storage layout through `redb` table
definitions plus the rkyv-encoded payloads it stores. When either
shape changes, **both the new binary and the existing on-disk data
have to end up in a consistent state**.

Concrete trigger: the operator may currently be reshaping
`signal-persona-spirit` (the spirit pilot is the live test). When
the rebuild lands and CriomOS-home updates its spirit pin, the new
`persona-spirit-daemon` will face an existing
`~/.local/state/persona-spirit/persona-spirit.redb` whose records
were written by the prior daemon. If the rkyv layout for `Entry`
changed, naïve deserialisation fails. Spirit has real captured
intent in it now — drop-and-rebuild is no longer free.

Same shape applies for every persona triad: `mind`, `orchestrate`,
`router`, eventually `introspect`, `terminal`, `message`. Spirit
just hits it first because it shipped first.

## Two axes of change

The word "schema" actually hides two distinct surfaces. Most
contract edits touch one; many touch both.

**Wire contract** — the `Operation`, `Reply`, `Event`,
`SubscriptionToken` types in `signal-<component>`. Affects clients
when they call the new operations; affects the daemon as it
deserialises requests. Backwards-incompatible wire changes cause
clients on the old protocol to error out (`RequestUnimplemented`,
parse failure, kind-not-found). No on-disk artefact.

**Storage schema** — the redb tables the daemon owns plus the rkyv
layout of the payloads it stores. Affects existing on-disk data
when the daemon's types no longer match what was written. rkyv's
zero-copy layout depends on the exact Rust types, so even small
changes (adding a field, reordering, changing an `Option<X>` to a
typed sum) break read-back.

A typed-record change in the working contract (e.g., adding a
field to `Entry`) usually crosses both axes — the wire shape
changes AND the storage shape changes, because the daemon stores
what it receives.

## Lifecycle of a contract edit (today)

What actually happens when the operator modifies `signal-persona-spirit`:

1. Operator commits to `signal-persona-spirit` main.
2. Operator bumps the persona-spirit Cargo dep to the new rev,
   commits.
3. CriomOS-home's flake.lock points to the new persona-spirit
   commit (manual `nix flake update` or a similar refresh).
4. CriomOS rebuilds; new `spirit` and `persona-spirit-daemon`
   land in the user profile.
5. User-service unit restarts the daemon, **pointing it at the
   existing redb file written by the prior daemon**.
6. The new daemon attempts to open the redb tables, dispatch
   requests, deserialise stored records. If the schema changed,
   step 6 is where the failure modes live.

Steps 1–4 are mechanical. Step 5 is automatic (systemd-style
restart). Step 6 is unprotected — there's no migration anywhere.

## Candidate approaches

Four shapes. Listed from cheapest to most general. Not exhaustive.

### Approach A — drop and rebuild

When the contract changes, the deployment process deletes the redb
file before the new daemon starts. The daemon comes up against an
empty database.

- **What it costs**: every captured intent record. Today that's
  ~20+ psyche statements; the count is rising fast.
- **What it gains**: zero migration code. The daemon needs no
  knowledge of prior schemas.
- **When it fits**: pure prototype phase where data is
  intentionally throwaway. The workspace was here until psyche
  started using Spirit yesterday. **Not viable from here on**.

### Approach B — offline migration tool

A separate one-shot binary (a sibling `spirit-migrate` or a
`Migrate` subcommand on the daemon) reads the old database with
both old and new type definitions linked, transforms records into
the new layout, writes a new database, and replaces the old. The
daemon then opens the new database normally.

- **What it costs**: the migrator must link both versions of the
  types. Either the old types are kept in a versioned module
  (`schema_v3`, `schema_v4`, …) or the migrator is a sibling
  crate pinned to the *old* `signal-persona-spirit` rev that
  reads then re-emits in the new format.
- **What it gains**: clean separation — the daemon only knows the
  current schema; migration is a one-shot transformation outside
  the hot path. Composable: each contract version ships a
  migrator from N-1 to N.
- **When it fits**: deliberate contract bumps where downtime is
  acceptable and the team accepts a migrator-per-schema-bump
  discipline.

### Approach C — versioned records in storage

Every stored record carries a schema-version tag. The daemon
dispatches read-side on the tag — if the record is at a prior
version, it migrates on read into the current shape, optionally
writing the upgraded form back. Writes always go in the current
shape.

- **What it costs**: the daemon links all historical type
  definitions (or has explicit migration steps `read_v3 → v4 →
  v5`). Storage carries a small per-record tag.
- **What it gains**: zero-downtime upgrades. No external
  migrator. Mixed-version reads work indefinitely.
- **When it fits**: production-grade evolution after the contract
  shape stabilises and the historical lineage is worth preserving
  in code.

### Approach D — daemon handover via wire-encoded state

Old daemon serialises its full state to a stable wire form (NOTA
text or a simple versioned binary). New daemon reads that form on
boot. The actual on-disk redb is rebuilt from the handover dump.

- **What it costs**: requires defining a stable handover format
  separate from both the wire contract and the storage schema —
  a third surface to maintain.
- **What it gains**: handover format absorbs schema drift; old
  and new daemons coordinate without sharing types.
- **When it fits**: long-running daemons across major schema
  redesigns where neither offline migration nor versioned records
  feels right. Probably not the right first move.

## Where the schema-in-NOTA proposal connects

The psyche's parallel design thread on **defining signal schemas
in NOTA** (intent record 12, `intent/signal.nota` 2026-05-21)
intersects this report directly. If signal schemas become NOTA
artefacts that generate Rust code, then:

- A schema bump is a diff between two NOTA schema files.
- The migrator (approach B) or version-dispatch table (approach C)
  could itself be generated from the diff.
- The stored data format (rkyv layout) becomes a function of the
  NOTA schema version, making cross-version reads tractable
  without hand-written type registries.

That thread is queued behind this one per psyche on 2026-05-21.
The recommendation below stays approach-agnostic so it composes
with whichever schema-source-of-truth shape lands.

## Selected approach — C, in-process versioned reads

**Decision 2026-05-21** (psyche selection, `intent/component-shape.nota`
record 21): the migration mechanism for persona daemons is
**Approach C — in-process versioned reads**. Zero downtime per
schema bump; the daemon dispatches read-side on a per-record
schema-version tag and migrates older records on read into the
current shape, optionally writing back the upgraded form. Trade-offs
explicitly accepted: the daemon links every prior schema version's
type definitions, and read paths fork by version (squashable later
through explicit version-collapse work).

A first concrete slice for spirit (subject to follow-up design):

1. The `signal-persona-spirit` crate exports a `SCHEMA_VERSION`
   constant and stamps each record's stored payload with that
   version on write — a leading `u32` (or a `SchemaVersion(u32)`
   newtype) prefix on the rkyv payload, or an explicit
   `version: SchemaVersion` field on the record types.
2. The daemon's read path peeks the version tag, dispatches to the
   prior-version deserialiser when needed, runs a
   `migrate_v<N-1>_to_v<N>` step to lift into the current shape,
   and (per write-back policy) writes the upgraded record before
   serving it.
3. Prior-version type definitions live in a versioned module tree
   inside `signal-persona-spirit` (`schema_v3::Entry`,
   `schema_v4::Entry`, …) — or, if the module tree gets large, in
   a sibling `signal-persona-spirit-history` crate.
4. Schema bumps land as: (a) a `signal-persona-spirit` PR that
   adds the new version, freezes the old as `schema_v<N-1>`, and
   provides the migration function; (b) a `persona-spirit` PR
   that updates the daemon to call the migration step.

The exact shape of every numbered item above is design follow-up,
not settled by today's selection.

This selection composes with the schema-in-NOTA proposal directly:
the historical-version modules become NOTA artefacts under that
direction, and the migration step becomes a function of the diff
between two NOTA schemas.

## Open questions

Post-selection. The downtime question is answered (zero downtime
via Approach C). Three follow-up decisions remain.

1. **Schema version surface within Approach C.** The selection
   wording says *per-record*: every stored record carries a
   version tag. That settles record-instance versioning. Still
   open: does the version number range over the whole component
   (one counter per daemon, bumped whenever any record type
   changes) or per record type (Entry has its own version,
   Subscription has its own, etc.)? Per-component reads cleaner
   and is the workspace's component-shape lens; per-record-type
   matches the actual change locality. Designer lean:
   per-component.

2. **Where the historical type modules live.** Approach C requires
   the daemon to link every prior schema version's types so the
   read path can deserialise old payloads. Two homes:
   (a) inside the `signal-<component>` crate as a `schema_v<N>`
   module tree — keeps the historical types near the current
   contract, but the crate grows with every bump; or (b) a
   sibling `signal-<component>-history` crate that re-exports
   each prior version as its own submodule — decouples the
   current contract from history, at the cost of a sibling repo
   per triad. Designer lean: (a) until the module tree becomes
   load-bearing on the current contract's read path.

3. **Owner-channel symmetry.** Spirit's `owner-signal-persona-spirit`
   contract carries policies, identities, and configuration —
   data with different recovery characteristics from the working
   channel's record stream. Does the owner contract get the same
   versioned-reads treatment, or do owner schemas migrate
   differently (e.g., always re-bootstrapped from
   `bootstrap-policy.nota` and treated as transient)?  Probably
   needs a dedicated follow-up report.

## Next slice if this lands

Once the psyche picks a direction:

- Specify the schema-version stamping mechanism in
  `signal-persona-spirit` (operator work).
- Specify the migrator binary's NOTA argument shape and exit
  contract (designer report follow-up).
- Pilot the migrator for spirit's next planned schema change —
  which will likely arrive soon given the operator activity.
- Generalise the pattern into a `skills/schema-migration.md`
  skill once the shape proves out.

This report retires when either:
- A successor design report supersedes it, OR
- The first migrator ships and the discipline becomes a skill.

## References

- `intent/component-shape.nota` 2026-05-21 record 10 — psyche
  surfaces the schema-migration concern as a real workspace-wide
  problem.
- `intent/signal.nota` 2026-05-21 record 12 — the schema-in-NOTA
  proposal that intersects this work.
- `intent/spirit.nota` 2026-05-21 record 7 — the deployed-version
  tracking principle that turned into this report's trigger.
- `skills/spirit-cli.md` — for how to find the deployed wire
  shape from the criome-os pinning.
- Spirit's pinned contracts as of 2026-05-21: persona-spirit
  `694452a`, signal-persona-spirit `b89731f`. The next contract
  bump beyond these is the first real migration trigger.
