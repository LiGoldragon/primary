# Live code tools — Stage 2 decision packet

2026-11-16, researchTools b06fc3. Source-only proposal; Stage 2 remains unallocated. Open task l0mm. This packet builds on `flows/09fa53/proposals/runtime-clearance.md` and the completed inventory `flows/12b000/runtime-inventory.md`.

## Observations

- On Ouranos and Prometheus, the exposed rust-analyzer, cargo and rustc are unconditional exit-126 wrappers. An analyzer version invocation would encounter that same guard. lspmux is absent. No compatible retained artifact was identified; none was searched for broadly.
- The known historical Nix source is CriomOS `ab62d218610f35af6279ed3590224dee83645011`, `packages/repository-analysis/default.nix`. Reading that exact file shows an offline vendor derivation, toolchain and `pkgs.rust-analyzer-unwrapped`; it executes a batch SCIP index, not a live language server. No evaluation, executable probe or build was performed here.
- That expression supplies an observational compiler wrapper and explicitly invokes the underlying toolchain. Its Rust guard permits a print/version argument and rejects several output arguments; it is not a complete compiler argument grammar or universal containment. The historical expression is evidence of packaging structure, not authorization to reproduce its execution outside the derivation.
- Its source pin covers the old corpus, not the approved Flow a044e39 and Lojix 5d75a403 corpora. An existing batch output, even if retained, would not establish a live-server executable closure or current offline metadata.
- The living's recorded instruction is manual analyzer startup only: `vision-raw/why-is-rust-analyzer-running.md`. Nothing in this proposal changes that.

## Options requiring a ruling

1. **Reviewed temporary Nix runtime package.** Packaging owner supplies a published derivation exposing the analyzer, matching toolchain/Rust sources, offline dependencies for each exact corpus, selected multiplexer if retained, and ranked map. Field approves its precise manual entry point and guard policy before a build/start. No profile or service installation. Existing guards remain in place.
2. **Explicit bounded runtime exception.** If the intended live server needs observational compiler/Cargo execution outside the normal guarded route, the approving owner names exactly which packaged executables and invocation classes are permitted, on Prometheus, for this trial. This is a policy decision, not a guessed absolute executable path. No exception currently exists.
3. **Cargo-free project description, conditional alternative.** A reviewed explicit rust-project.json could avoid Cargo metadata at server startup. Its complete crate graph, cfgs, dependency sources and sysroot must be supplied and checked by the source/packaging owner. It still needs an approved analyzer executable, and omitted generated/procedural information remains a coverage limitation. This option has not been validated and has no executable packet yet.

Option 1 is the proposed direction. Option 2 is needed only if its reviewed runtime actually requires an exception. Option 3 is an alternative design to judge before implementation, not an automatic fallback. No option is presently launch-ready.

## Evidence the owners must return

Packaging owner: exact published revision and Nix selector; artifact store identity or permission to build; analyzer/toolchain versions established from declared inputs; exact offline corpus/dependency identities; supported initialization settings; compiler/Cargo invocation policy and its enforcement scope; ranked-map selector. Supply existing artifacts first where they actually meet these identities. Do not infer an artifact path from package names.

Field: assigned awake actor and runtime window; exact allocated roots, socket, transport, start/query/stop command boundary; resource/time limits; registered process and mount cleanup ownership. Allocation and command review follow packaging/policy evidence. No guessed mktemp result or PID belongs in an approval packet.

Flow owner: fresh distinct declarations after roots and tool boundaries freeze; explicitly reviewed modules, leave-outs and records; per-session provider/model/effort receipts; one pair at a time capacity. The observed old Luna mapping is historical evidence only.

## Acceptance and next event

After these replies make the paths and policy real, researchTools returns the exact Stage 2 command packet to Field/Core for approval. It must demonstrate definition, implementations, hover and workspace symbols against the frozen questions before answerers start. Shared-server identity, coverage omissions, guarded execution evidence and cleanup are operational acceptance results, not assumptions.

Until then: zero live starts, zero mounts, zero runtime allocations and zero paired outcomes. The interim report remains `flows/72fb9a/research/live-code-tools.md`; l0mm remains open. Read-only source packet refinement can proceed; runtime work waits for explicit owner replies.
