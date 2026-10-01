# Known Nix fixture-test failure — pre-fix record

Verdict: **BLOCKED BY SCHEDULING**, not a source-test result. No fix or rerun was made in this report-only subflow.

`reports/field-readiness/10-vm-cluster-probe.md` records a witnessed failure before any fix: the ouranos Nix builder entry for prometheus advertises `big-parallel,kvm` but omits `nixos-test`, while VM checks require `kvm,nixos-test` and ouranos is forbidden to run QEMU. Its report says the first naive `nix build` of a VM check produces the local `nixos-test` scheduling failure. The same condition is indexed in `reports/field-readiness/02-kink-ledger.md` as rank 13 / 10-K2.

This is a report of the earlier witness, not a fresh run. Causes remain scoped: the missing feature is sufficient for the scheduling failure; whether its omission is deliberate is an open host-config/doctrine decision. The proposed changes in the source report — advertise `nixos-test` or codify the SSH-run path — remain unperformed.
