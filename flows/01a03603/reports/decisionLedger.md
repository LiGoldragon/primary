# Ethos-monolith POC decision report

## Result

The POC is complete. Ethos-monolith emits usable Rust wire modules from Ethos; two Orchestrate contract crates commit those projections; and Orchestrate 0.22.0 uses them in a live, durable, two-socket Nexus. This report records the decisions made during realization and why. The AI-generated task charter is direction, not psyche-origin material.

## Decisions

### Provenance and execution

1. **Keep the realization prompt outside Vision.** The living corrected its provenance: it was AI-generated. The incorrectly created Vision file was deleted, and only the cited existing psyche records were treated as psyche authority.
2. **Split work at repository boundaries.** Ethos emission, ordinary/meta contracts, and the Nexus runtime/proof were delegated separately so product edits did not overlap and the generated API remained an explicit dependency.
3. **Continue when edit coordination was unavailable.** The brace-form requests parsed, but the deployed coordination sockets were absent. Claims are advisory, so every subflow recorded the failed transport probe and continued with disjoint ownership.

### Ethos-monolith

4. **Put the complete Signal binding in Ethos.** The Interface dialect gained `Channel.{Name ContractId WireRevision}`. Channel identity and binding are public interface facts; leaving them in handwritten consumer Rust would make the generated interface incomplete.
5. **Generate the usable wire module, not declarations alone.** Signal projections include the wire marker and binding, structural rkyv/Datom support, `signal_channel!`, request/frame aliases, operations, and a closed reply. This was necessary for the live daemon to use generated Rust as its actual contract.
6. **Require a channel only for `signal.ethos`.** `nexus.ethos` and `sema.ethos` may be exact empty Interface documents and emit plain empty modules. They are canonical source/module positions without invented runtime vocabulary.
7. **Support the syntax demanded by the proving contracts.** The POC emits nominal String/Integer types, structs, closed enums, nested data variants, and `Vector<T>` of local types. Imports, interactions, unconstrained generic parameters, and streaming runtime declarations remain explicit errors rather than guessed or silently dropped output.
8. **Make text headed only at the concrete contact point.** `PathLock.{name [/path] (description)}` keeps its outer type head, while embedded nominal fields and vector elements use their underlying data form. The outer schema already fixes their types; repeating inner heads was redundant and contradicted the witnessed carrier and Ethos non-repetition.
9. **Flatten one-field record carriers under their own head.** `PathLockRegistered.{name ...}` and `Configured.{store ...}` use one brace body rather than doubled braces. Their reply type is the contact point; the wrapped record's head/body must not leak through as extra syntax.
10. **Project Rust field names as snake_case.** Ethos names remain authored as witnessed, while generated Rust follows Rust naming rules. The choice was forced and regression-tested by downstream Clippy.
11. **Make formatting a required generation phase.** Rust 2024 `rustfmt` runs before projection installation, and failure is explicit. Committed generated files must pass the consumer's unchanged format gate.
12. **Keep unsupported or incomplete generation atomic.** All three Ethos sources are realized before any projection is installed; invalid source fails before output installation. A component cannot be left with a partly refreshed interface.

### Generated contract repositories

13. **Preserve contract identity and advance the actual prior wire revisions.** Ordinary remains ContractId 1 and moves wire 3→4; meta remains ContractId 2 and moves wire 2→3. The cited path-lock branch, not stale main, was the carrier being extended.
14. **Use `Register(PathLock)`, not a textual `Reserve` wrapper.** `PathLock.{...}` is the ruled concrete Datom input; the CLI wraps it in the generated `Register` operation internally. The generated envelope enum is not the user's text boundary.
15. **Make release the smallest paired carrier.** `PathLockRelease.{name}` yields `PathLockReleased.{name}` or a closed `UnknownActiveName` refusal. A held lock's name is sufficient to select the durable row; sessions, owners, and lane vocabulary were not reintroduced.
16. **Make `Configure` the concrete meta carrier.** It contains only store, ordinary-socket, and meta-socket paths and yields `Configured` or closed `StorePathImmutable`/`InvalidConfiguration` refusals. Workspace roots, repository refresh, and other privileged vocabulary were unnecessary for this POC.
17. **Commit generated Rust and enforce freshness without writing source.** Each build copies Ethos inputs to `$OUT_DIR`, generates there, and byte-compares all three results with committed `src/generated` modules. This keeps ordinary tooling functional and works in read-only vendored/Nix sources while still rejecting stale projections.
18. **Patch-bump the packaging repair.** The wire-bearing releases are signal 0.16.0 and meta 0.10.0; changing their package build behavior produced immutable-source-safe 0.16.1 and 0.10.1. The wire revisions did not change because the wire bytes did not.

### Orchestrate Nexus

19. **Replace the lane/workflow runtime wholesale.** The legacy source produced 156 compile errors against the new contract and embodied an unrelated lane/claim/workflow/upgrade domain. The POC retains only the daemon, Sema-owned state, two required sockets, generated contracts, and two thin clients; no compatibility layer or upgrade socket remains.
20. **Keep the executable name `meta-orchestrate` with no alias.** The component-specific restoration record explicitly orders this name and is more specific than the generic `<component>-meta` convention.
21. **Use one base64url startup argument containing a generated Configure frame.** OS argv cannot carry arbitrary rkyv bytes because it forbids NUL. URL-safe unpadded base64 is only an argv envelope; it is decoded and validated immediately and never becomes a socket protocol.
22. **Let the daemon alone own Sema durability.** One Sema store persists the single configuration and normalized active locks through sema-engine. Neither CLI opens storage or implements policy.
23. **Normalize lexically and reject conflicts atomically.** Paths must be absolute; duplicate active names and ancestor/descendant path overlap reject the whole registration while preserving the full holder in typed refusal data. The reserved filesystem paths themselves are never mutated.
24. **Release by active name and permit re-registration.** Release removes the durable active row; an unknown name is a typed refusal. A successful release makes the same name/path available again, as the proving sequence requires.
25. **Do not silently reconfigure a running durable owner.** Repeating the persisted configuration succeeds; changing the store is `StorePathImmutable`, and another incompatible change is `InvalidConfiguration`. The POC does not switch stores or rebind live sockets mid-request.
26. **Keep both CLIs to one concrete Datom positional object.** `orchestrate` accepts `PathLock` or `PathLockRelease`; `meta-orchestrate` accepts `Configure`. Flags and file-shaped inputs are rejected; each client uses only its designated socket and converts text to validated generated Signal frames.
27. **Serialize store dispatch behind the two socket listeners.** Both ordinary and meta requests reach the same daemon-owned state in a defined order. This is the smallest correct concurrency shape for the POC and avoids concurrent mutable Sema access.
28. **Version the replacement as Orchestrate 0.22.0.** The ruled PathLock carrier was already 0.21.0; Release, Configure, the replacement runtime, clients, and durable live proof change public, storage, package, and deployment surfaces.

### Proof and tracking

29. **Use one actual-process scenario as the decisive POC witness.** The test starts `orchestrate-daemon` with a temporary `.sema` store and two sockets, invokes both actual CLIs, and observes register, duplicate-name refusal, path-overlap refusal, release, re-register, and meta Configure. It tests the assembled system rather than a parallel harness.
30. **Require both local gates and a real remote Nix build.** Evaluation alone did not prove immutable-source packaging; the remote `live-nexus` build found the contract build-script defect. Completion waited for patched contract releases and a green remote release test.
31. **Do not invent a Beads store for historical IDs.** The current Orchestrate checkout has no active Beads workspace and repository-wide search found neither cited ID. The POC was completed and evidenced without bootstrapping an unrelated tracking database; the historical records were left unchanged.

## Final revisions

- ethos-monolith `cc3ee3221401bf4edec0e6c9b1c1b2ce35e28ff6`
- signal-orchestrate `d23fb6430eda` — 0.16.1, ContractId 1, WireRevision 4
- meta-signal-orchestrate `ebefb65c7076` — 0.10.1, ContractId 2, WireRevision 3
- orchestrate `09c19ce2af53328748a73dd2d7b5c4288bc33d98` — 0.22.0

## Sources

- `flows/01a03603/witnesses/ethosEmitter.md` and `flows/01a03603/reports/ethosEmitter.md`
- `flows/01a03603/witnesses/orchestrateInterfaces.md` and `flows/01a03603/reports/orchestrateInterfaces.md`
- `flows/01a03603/witnesses/orchestrateNexus.md` and `flows/01a03603/reports/orchestrateNexus.md`
- `Vision/ethos.md`, `Vision/ethosMonolith.md`, and `Vision/datom.md`
- `flows/aa4c7747/vision/` and `flows/2b34fafa/vision/`
- `flows/01a02a34/reports/pathLockEpic.md`
- `flows/01a02fd5/vision/metaOrchestrate.md` and `flows/01a02fd5/reports/metaOrchestrateRestoration.md`
- `flows/e06e4c07/vision/nexus.md`
- `flows/98fbfa47/vision/metaSignalNotOptional.md`
