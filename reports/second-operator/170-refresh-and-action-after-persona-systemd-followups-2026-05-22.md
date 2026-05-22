# 170 - Refresh and Action After Persona Systemd Followups

Report kind: refresh
Topic: Persona handover, systemd followups, bead reconciliation
Date: 2026-05-22
Lane: second-operator

## Inputs Absorbed

Intent refresh included records 217 through 241, with emphasis on:

- 217: port stale components to the current executor / signal / NOTA foundations.
- 218 and 220: keep large analysis in reports; chat carries only the main items and questions.
- 228: keep Persona handover work moving until no clear work remains.
- 230: second-operator pivots from orchestrate migration to reviewing Persona smart-handover work for possible parallel slices.
- 238 through 240: Persona is a permissioned system daemon and uses systemd template units from day one for production component management.
- 241: refresh reports and intent before selecting next work.

Reports absorbed or refreshed against:

- `reports/designer/287-version-handover-component-explained.md`
- `reports/designer/288-actionable-beads-2026-05-22.md`
- `reports/designer/289-arch-distribution-from-287-2026-05-22.md`
- `reports/designer/290-persona-arch-diff-suggestions-2026-05-22.md`
- `reports/designer/291-persona-systemd-units-for-daemon-management.md`
- `reports/operator/158-version-handover-foundation-implementation-2026-05-22.md`
- `reports/operator/159-persona-engine-upgrade-foundation-2026-05-22.md`
- `reports/operator/160-spirit-smart-handover-sandbox-test-2026-05-22.md`
- `reports/operator/161-spirit-private-handover-socket-2026-05-22.md`
- `reports/operator/162-persona-owner-version-handover-authority.md`
- `reports/operator/163-persona-systemd-component-management-position.md`
- `reports/second-designer/152-persona-engine-architecture-overview/9-overview.md`
- `reports/second-designer/153-refresh-after-prime-systemd-followups-2026-05-22.md`

## Actions Taken

Closed bead `primary-chpq` (Spirit default wrapper dual-writes during version migration) as superseded. Later intent and the current design replace CLI-owned dual-write with Persona-driven smart handover over private version-handover sockets. Remaining cutover work is tracked by `primary-x3ci` and `primary-wvdl`.

Commented on bead `primary-qk04` (multi-version persona-spirit daemon coexistence in CriomOS-home). The coexistence shape is still present: both v0.1.0 and v0.1.1 user services are active, versioned state directories and sockets exist, and wrappers exist. I did not close it because `spirit-v0.1.1` is not current with the latest v0.1.0 intent records; that freshness/cutover issue belongs under `primary-x3ci` or a system-specialist verification pass, not under the now-superseded dual-write wrapper idea.

Verified the workspace working copy has no `jj` changes after the bead updates.

## Current Situation

The main operator lane holds the active Persona lock for `primary-a5hu` (Persona engine systemd unit management slice) over `/git/github.com/LiGoldragon/persona` and `/home/li/primary`. I avoided Persona code edits from second-operator to avoid colliding with that work.

The operator has advanced Persona handover beyond the earlier report baseline. Bead comments now show Persona and Spirit have real private upgrade socket witnesses, mirror payload application for `StampedEntry`, copied-store handover, public-write freeze after readiness, failure recovery back to Active, next-marker parity checks, and prepared-attempt audit logging. The remaining handover gap is narrower: automatic next-daemon launch / copy / retry / live replay, production v0.1.0 protocol-aware retrofit / tag / deploy, and production active-selector routing.

The newest systemd decision is settled at the architectural level: Persona is the privileged system daemon; production component daemons run under systemd template units named like `persona-component@<component>:<version>.service`; Persona uses a `UnitController` trait with a systemd D-Bus backend in production and direct / fake backends in tests and sandboxes.

## Questions Still Worth Asking

1. Public traffic routing during cutover remains the biggest design question. Persona owns the active-version table and systemd owns production process identity, but clients still need a concrete route to the active daemon. Should this be a Persona-owned routing socket, stable systemd socket activation, or CLI query to Persona followed by direct connection?

2. Spirit v0.1.0 production retrofit looks like the correct path, but it is still worth confirming before work starts: should we rebuild, tag, and deploy a protocol-aware v0.1.0 maintenance build with the same database schema, rather than accepting any staged first-cutover shortcut?

3. `EffectEmitted` convention remains open. The strongest rule candidate is: authority-tier / cross-cutting contracts default to `SemaObservation`, while component-local domain contracts may use typed `Effect`. This needs psyche ratification before agents propagate it into the remaining observable blocks.

4. `signal-persona` crate shape is still unresolved before Track B cleanup. Should `Engine` and `EngineManagement` remain two channels in one `signal-persona` crate, or should `EngineManagement` split into its own contract repo before the Axis 2 rename cascades further?

## Next Implementation Options

If the main operator keeps the Persona lock, the least-colliding second-operator implementation path is one of the ready non-Persona migration beads, such as `primary-0bls` (migrate criome triad to current foundation) or `primary-9up1` (migrate lojix triad to current foundation). If Persona work is handed to this lane, the clean slice is not broad design: it is the production routing / replay piece under `primary-wvdl` and `primary-x3ci`, after coordinating the lock.
