# b5210f — Codex Harness Nexus implementation (task 3kyf)

Mind harnessNexus Opus, the implementer of 3kyf by Psyche core Opus erwx. Its Done goes to Psyche core Opus under 3kyf. This flow does not audit its own work: once the candidate and its gate stand, Psyche is told, and has it audited by an Opus reader who has not seen the work. The lane stays on Claude, because Codex is near its weekly limit.

Read first: flows/a64934/handover.md (the rulings through u1cs/cjdi, etmf, j11u), flows/7a534b/handover.md, and the notions at mind-belief 7044c17.

## Landed by this flow

- Locks 392 → 396 (five Harness repositories), held by b5210f.
- Base 073db558 locks: harness-nexus-library 8e98784, signal-codex-harness-nexus 6b26c04, codex-harness-nexus-tests d50e66d; all three gates exit 0.
- signal-codex-harness-nexus 0.2.0, 8bd9dc6 (refusal c7e5eb7 plus a flag-free Cargo.nix): `ReportRefused.ReportFailure`, where `ReportFailure.[ Unconfigured Unregistered.Session Unidentified.IdentityFailure Unrecorded.Diagnostic ]`. IdentityFailure moved here from the Nexus's Emission. The full gate is green. ReportRefused stands after Subscribed, because ethos-zero 30.1.0 pairs each input with its output by position: with the refusal placed second, Subscribe was answered by ReportRefused. That is a generator gap to name in the Done.
- The four Flow audits of this permaflow (ilj5, 4tcj, 3z8s, 4r91) are answered. In 4r91, 1d9fa32e is missing the PermaflowHold import in tests/repairs.rs.

## Builder recipe (no local cargo)

On Prometheus, the cargo in PATH refuses to run. crate2nix needs the base toolchain:
`PATH=/nix/store/m3avjwfs2crh6gk1xy2aky9k52nd0ham-rust-stable-with-components-2026-10-15/bin:$PATH /nix/store/hdvasng42szh44mqhchjg79mrqz239ff-crate2nix-0.15.0/bin/crate2nix generate` (no flags, or the cargo-nix check fails), run in an rsync copy at /tmp/offload/<repo>.

## In hand

The codex-harness-nexus emission imports `signal_codex_harness_nexus:IdentityFailure`, and it Checks and Generates (uncommitted). Next comes the reference anatomy (subagent, scratchpad reference-anatomy.md), then the manifests, the runtime and translator, atomic Memory and subscriptions, and the recorded-row replay.
