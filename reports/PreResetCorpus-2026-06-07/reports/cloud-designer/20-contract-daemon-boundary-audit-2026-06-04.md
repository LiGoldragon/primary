# Contract ↔ daemon boundary — audit verdict and correction

*cloud-designer, 2026-06-04. A four-angle audit (canon, macro, reference,
prototype) triggered by the psyche catching that the cloud-port prototype
embedded Nexus/SEMA in the contract schemas. **All four angles converge,
all high-confidence.** On `cloud-designer/next`; not on `main`.*

## Verdict — the psyche is right on every count

**A component contract is wire-only.** The contract schema
(`signal-<component>` / `meta-signal-<component>`) carries only the Signal
messaging vocabulary — Input/Output roots, their record types, and the
wire codec. Nexus and SEMA are daemon-internal runtime planes and must not
appear in a contract. A client sends and receives only Signal messages; it
never sends a Nexus or a SEMA object.

The canon says it outright (`component-triad.md`):

> [The contract crates carry no runtime, no actors, no tokio — they declare
> typed wire vocabulary and generated method surfaces, and nothing else.]

and the runtime triad lives elsewhere:

> [Inside the `<component>` daemon, three layers organise the logic … the
> THREE EXECUTION CENTERS of the daemon.]

So the read-SEMA question from the prototype was malformed at the root: a
contract has no SEMA engine *at all* — the daemon does.

## Why it happened (my error) — and why it's workspace-wide

I briefed the prototype by modeling the contract schemas on `spirit`. But
`spirit` is an **all-in-one single-repo pilot that deliberately defers the
split** — its own ARCHITECTURE.md admits it:

> [The repo-triad split (spirit, signal-spirit, owner-signal-spirit) is not
> represented in this pilot repo.]

The canon was clear; I followed an incomplete reference. And it isn't just
cloud: **no correct schema-derived contract/daemon-split exemplar exists
yet.** `signal-upgrade` carries the *same* error (its `lib.schema` has
Nexus/SEMA). `signal-spirit` is wire-only but isn't wired to the spirit
daemon. So this audit surfaces a workspace-wide gap, not a cloud-only slip.

## The macro reality (schema-rust-next)

Good news and a gap:

- **A wire-only contract already works today.** A schema declaring only
  Input/Output + records (no Nexus/SEMA roots) emits **no engine traits**
  — `SignalEngine` itself is gated on `NexusWork`/`NexusAction` being
  present, and `NexusEngine`/`SemaEngine` on their own roots. So stripping
  Nexus/SEMA from the two contract schemas fixes them now, with no macro
  change. (It still emits the rkyv/short-header wire codec + mail
  envelopes — which is exactly a contract's job.)
- **The gap:** a *daemon* schema cannot **import** a contract's Input/Output
  as its own Signal roots — Input/Output are mandatory struct positions in
  `Asschema`, not namespace entries, and the import mechanism only
  re-aliases namespace types. So today a daemon schema must **re-declare**
  the wire roots locally, which defeats the split. The required
  enhancement: let a daemon schema import (or a contract `export`) the
  Input/Output roots. (Optional secondary: flags to suppress mail/upgrade
  infrastructure for a leaner contract.)

## The correct three-way layout

- **`signal-cloud.schema`** (wire-only): `Input [Observe Validate]`,
  `Output [Observed Validated RequestUnsupported RequestRejected]`, the
  record types, codec. **No Nexus/SEMA.**
- **`meta-signal-cloud.schema`** (wire-only): `Input [RegisterAccount …
  RetireAccount]`, `Output [AccountRegistered … RequestRejected]`, records.
  **No Nexus/SEMA.**
- **The daemon's plane schemas** (in the `cloud` repo — **separate files,
  not one**): per settled intent (Spirit 2604, 2601, 2598), the daemon
  carries `cloud/schema/nexus.schema` and `cloud/schema/sema.schema` as
  distinct per-plane schema files inside the one daemon crate (NOT per-plane
  crates, NOT one all-in-one daemon schema). Each imports the wire
  contracts' Signal Input/Output; the generator emits **per plane** — the
  Nexus schema emits the Nexus engine, the Sema schema emits the Sema
  engine. This requires `schema-next` to read multiple plane-schemas per
  crate (2604) and to import a contract's wire roots. The
  provider-IO-as-`CommandEffect` shape and the in-memory `Store` are correct
  — they belong in the daemon's `nexus.schema`/`sema.schema` + impls, not in
  the contracts and not in a single daemon schema.

The prototype's *engine logic* (the decide loops, the effect handler) is
sound and stays — it only needs to move from the contract repos' schemas
into the cloud daemon schema, and the contracts need Nexus/SEMA stripped.

## What's fixable now vs what needs operator infra

| Step | Owner | Blocked? |
|---|---|---|
| Strip Nexus/SEMA from the two contract schemas → pure wire | cloud-designer (now) | No — works today |
| Author `cloud.schema` declaring Nexus/SEMA + the engines | cloud-designer | Needs root-import to import contract Input/Output (else re-declare as stopgap) |
| Cross-crate **root import** in schema-next/schema-rust-next | **operator** (owns those repos) | This is the real enhancement |
| Clean up `signal-upgrade`'s same error | operator/system-designer | Separate slice |

## Settled by recent intent (Spirit 2597, 2598, 2601, 2604, 2605)

The shape is decided — these records (which postdate and sharpen 2593/2595)
settle it: a triad component is **three+ schemas**. The wire contract
(`signal-*` / `meta-signal-*`) stays wire-only. The daemon carries
**separate per-plane schema files** — `cloud/schema/nexus.schema` and
`cloud/schema/sema.schema` — inside the one daemon crate (NOT per-plane
crates, NOT one all-in-one daemon schema). Each imports the contract's
Signal Input/Output; the generator emits per-plane (2598). The separate
`signal-*` / `meta-signal-*` repos exist for rebuild-churn isolation and
security-edit visibility (2605, 2602).

So the sequencing question is moot — the architecture is settled. What
remains is **operator work on `schema-next`/`schema-rust-next`**: read
multiple plane-schemas per crate (2604) and import the wire contract's
Input/Output roots into the plane schemas. Until those land, the cloud
daemon cannot be authored as separate plane schemas that build. The cloud
prototype must be re-done to the three-schema shape: contracts stripped to
wire-only (works today), daemon re-authored as `nexus.schema` +
`sema.schema` once the `schema-next` enhancements are in. Every contract
repo needs the same wire-only audit (2594).

## Branch locators

- `primary` → `cloud-designer/next` — reports 18, 19, 20 + the next-workflow skill edits.
- `cloud` / `signal-cloud` / `owner-signal-cloud` → `next` — the prototype (contracts to be corrected to wire-only; engine logic moves to a `cloud.schema`).
