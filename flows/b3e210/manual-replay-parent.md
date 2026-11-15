# Explicit Flow bootstrap replay — removal parent

Task 53zh / Order g5hd; Psyche gh91 approves the existing configured-place binding. This is source/gate evidence, not publication or deployment.

## Immutable source and custody

- Base Home main: `2af9265d37a10e20289db6826bfcef86c861bf74`.
- Candidate: `adeb3e53749bc0b211761c35b52525196f7e859a`.
- Local branch: `nixcriomos-b3e210-manual-replay`.
- Worktree root is retained in `/tmp/b3e210-workspace`; the Home checkout is its `home` child.
- No branch or main publication occurred. Mind flowNexus Sol owns separate s60o forward pins; Core independently reviews this candidate. Field alone activates an approved exact packet.

## Source behavior

`modules/home/profiles/min/flow-nexus-place.nix` no longer defines `flow-configure-0550` or its WantedBy relationship. The configureUnit option has no other tracked consumer on the selected base and was removed. The entire authored Flow Nexus unit block is byte-identical to its base, independently compared before commit; no Flow input or other dependency pin changed.

Home installs `flow-replay-0.55.0`, explicitly bound to the configured named place via the existing placeConfiguration. It accepts no arguments, preserves query order, replaces the existing runtime token, and exits on failed transport or a non-Configured reply. It does not start the Nexus or create a target place. The existing place-file materialization remains unchanged. No startup unit or Home activation hook invokes replay.

For the main version's existing configuration, ten queries are replayed: Nexus, Models, Thresholds, SendServers, HarnessHook, Metaflows, HarnessFlags, Investigation, DefaultMinutes, HandoverPolicies. Seven are retained authored datom source files; Nexus, SendServers and HarnessHook are generated definitions. They are not ten authored datom files. Other version configurations preserve existing optional HarnessHook applicability.

Owner declaration links remain source material. Changing/linking them no longer automatically submits their contents to Flow Memory. An explicit replay still replaces the configured families, so it remains an owner decision rather than a routine activation step.

## Gates

Full `checks.x86_64-linux` remote gate: **exit 0; 98 successful check entries**, including the new `flow-manual-replay` contract. Receipt directory: `/tmp/b3e210-replay-gate/`; `gate.log` retains immutable source archive, actual generated remote invocation and results; `gate.exit` records 0.

The gate used nix-fast-build on Prometheus, no-download, one evaluation worker and 16384 MiB evaluation limit. It reused the existing generated system projection at `/tmp/offload/1541ef-generated-inputs/system`, hash-bound by `/tmp/flow-4aa030-home-awake/system.hash`. No target projection was invented.

The new test checks the authored Flow unit exactly, absence of the effective configure unit, installed helper, ten exact family/order submissions, refusal stopping at the third family, argument rejection and required runtime environment. It uses a fake flow-meta, not production Memory or a live replay. Earlier failed runs are retained: one shortened-revision syntax error and three fixture mismatches against Home Manager-normalized unit attributes; the final test compares the authored unit independently of that normalization.

## Integration and activation scope

This exact reviewed/gated removal parent is proposed as the predecessor of the separate minimal Energy pin. Energy source `ca043ebc25bf9ca429b7639df752e71011c7be97` has also had its `packages.x86_64-linux.default` realized remotely, exit 0 (`/tmp/b3e210-energy-gate/package.log`, `package.exit`), independently of survey's 123-test source gate. No Energy Home pin has yet been changed.

An approved deployment must remove the obsolete configuration unit without invoking replay or restarting Flow. Core/Field must compare the effective unit set and coordinate any retained runtime masks. No Memory rollback, active-flow retarget, ujg2/ke1s adoption or producer upgrade belongs to this candidate. Field owns its serialized cleanup and later Energy transition; neither has been executed here.
