# 50 · intent capture — cluster-data-generated VM testing (pending Spirit)

## Status: Spirit write blocked (store layout migration needed)

The Spirit daemon (0.13.0) READS fine but REJECTS WRITES:

> engine storage layout 3 does not match this build's layout 5; the store was
> written under an older engine layout and must be rebuilt through checkpoint
> import or versioned replay; run `spirit-migrate-store` to fold this store
> forward

The intent store was written under an older sema-engine layout (3); the current
build expects layout 5. Until it is folded forward (`spirit-migrate-store` — a
spirit-daemon / maintainer-scope maintenance op), no records can be written.
This file is the durable record until then (per `skills/intent-log.md`: "If
Spirit is unavailable when a record is required, surface that as a blocker in
chat and in the relevant report").

## The intent to record (when Spirit is healthy)

**Principle** — Certainty `Medium`, Importance `Minimum`, Privacy `Zero`;
domains: `(Technology (Software (Quality Testing)))`,
`(Technology (Software (Systems Virtualization)))`; referents:
`vm-testing horizon CriomOS`:

> [VM testing must be cluster-data-generated and generic rather than
> cluster-specific or hand-written: the test-VM host node carries an explicit
> role, and the VM-test config and runner are generated in nix from the VM host
> cluster data plus the vm-node config, giving a predictable interface — the
> substrate for a suite of easy-to-read tests over complex OS and home-profile
> configurations.]

Testimony (verbatim psyche words):
- "using cluster-data-generated code, not cluster specific to me"
- "node hosting it needs a role, interface must be predictable and/or use a
  generated config"
- "use it to create a suite of easy-to-read tests for a bunch of complex os and
  home-profile testing"

Reasoning: directive opening a new design cycle now that the lojix daemon is
live; evolves the existing bespoke per-node CriomOS vm-testing feature toward a
generic cluster-data-generated interface — the host carries an explicit role and
the VM-test config is nix-generated from the host cluster data plus the vm-node
config, as the substrate for a readable OS/home-profile test suite. A durable
architecture principle distinct from the existing per-node-option records.

## Relates to existing Spirit records

- `cncj` (Decision High) — the CriomOS VM-testing node feature's per-node
  gpu-passthrough option (VFIO; the gamma visual test), disabled on Prometheus.
- `ggvg` (Decision Low) — the VM-testing node reachable via
  `vm-testing.<cluster>.criome`.
- the `2630`-era vm-testing-node line these extend.

The new Principle generalises that per-node feature; it does not contradict
`cncj`/`ggvg` (which stay as concrete options under the generalised interface).

## Also still pending capture (report 47)

The integrated-test-VM decision from report 47 (real KVM microVM substrate, v1
host-triggered lifecycle, declared in horizon with a host) was likewise never
written to Spirit (the daemon was flaky then). Capture it together with the
above once the store is migrated.

## Follow-up

- **Maintainer**: run `spirit-migrate-store` to fold the intent store forward
  (layout 3 → 5) so intent capture works again across the workspace. Then record
  the Principle above + the report-47 integrated-test-VM decision.
