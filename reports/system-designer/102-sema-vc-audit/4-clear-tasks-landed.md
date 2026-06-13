# 102/4 — Clear-tasks arc: landed

*On psyche direction ("take all the clear tasks yourself"), the clear (decided,
no-open-question) audit findings were implemented as designer feature branches,
each cargo-green and adversarially reviewed. All five slices landed; the gated
mirror shipper — partial last attempt — landed this time because the
`Arc<Engine>` refactor was scoped across mirror + spirit.*

## Branches (for operator integration, in dependency order)

| Repo | Branch | Head | Ver | Verdict | Content |
|---|---|---|---|---|---|
| sema-engine | `record-key-sum` | `65a6126a` | 0.6.1 | approve | `RecordKey` → closed sum `Domain \| Identifier`; dead `MaterializeIdentifierParse` deleted; **digest bytes preserved** (Identifier hashes the decimal-string form, same tag) so no store chain changes; tamper 11/11 unchanged. **Tip carries the whole engine chain**: single-writer mutex + O(1) head-digest + rebuild-from-log + RecordKey. |
| schema-next | `schema-next-polish` | `976d9f80` | 0.3.0 | approve | `SchemaError` → thiserror with typed nota sources; new `ReferenceHead` type centralizes the 5 copied `TypeReference` head-dispatch sites (fixes the `declarative.rs:2121` drift). |
| mirror | `arc-shipper` | `02ba9d5e` | 0.2.0 | approve-w/notes | `ComponentShipper` → `Arc<Engine>` (shares the component's one engine); `MirrorTailnetClient` → `TailnetClient`. Pins sema-engine to rev `65a6126a` (flagged for the integrator). |
| spirit | `vc-followups` | `339b08f9` | 0.13.0 | approve | v7-referent fix; **v1–v6 readers deleted** + probe rejects `<7`; naming cleanup; `StoreError` names `spirit-migrate-store`; `VersionReport` widened to 3 axes (+ `StoreSchemaHash`); meta **mirror-target on the `Configure` plane**; `Store` → `Arc<Engine>`; **gated shipper (29pb)**; + the guardian `ARCHITECTURE.md` note (`339b08f9`). |

## The single API change

`RecordKey::as_str()` → `to_owned_string()` (the `Identifier` arm carries a
typed `u64`, no borrowable `&str`). One trivial call-site change in spirit's
tests; no production caller used `as_str`. Everything else is API-preserving.

## The shipper landed — gated

`spirit::shipper::MirrorShipper` behind a new **`mirror-shipper` cargo feature,
off by default**. When the meta `ConfigureRequest` sets a `MirrorTarget`, the
spirit engine actor arms the shipper with a clone of the `Store`'s `Arc<Engine>`
and drains the outbox after each durable commit, recording `acknowledge_mirror`.
The 29pb witness passes: *configured → ships → `ServerCommitted` → fresh store
restores identical*; *unset → nothing ships, behavior byte-unchanged*. This is
the durability loop wired end to end as production code (not a test fixture) —
but **OFF until two deploy actions: authenticate the mirror TCP ingress
(`primary-x3l7`), then enable the feature + set a target.** Never enable against
the unauthenticated `0.0.0.0` ingress.

## Integration (operator — `primary-qu28`)

Order: **sema-engine first** (integrate the `record-key-sum` tip = the full
engine chain; the layout 4→5 bump self-heals existing stores on open via
rebuild-from-log — verify on a staging copy of the live store first), then
**mirror + schema-next**, then **spirit** (repins to the integrated engine +
mirror). `vc-followups` transitively pulls all four engine commits, so
sema-engine main must absorb the whole chain before spirit repoints to
`branch=main`.

## Remaining

- **God-impl split** (`x178`) — confirmed by the psyche ("definitely should be
  elegantly split"); decomposition decided (by data-ownership, `Engine` as the
  transaction coordinator, `sema` stays actor-free). In flight as the next
  workflow, stacked on the functional tips.
- **Ingress auth + enable shipper** (`primary-x3l7`) — system-operator; the
  deploy gate for live durability.
- **TypeReference → real structural macro** — needs the nota-next
  derive-vocabulary decision (the centralize part landed).
- **Guardian decision** — resolved: stays separate from the intent log (recorded
  in spirit `ARCHITECTURE.md`).
