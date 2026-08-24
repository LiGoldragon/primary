# Realization decision ledger

This ledger records implementation choices made where the acquired psyche was silent or where competing evidence had to be reconciled. It does not promote the AI-generated realization charter into Vision.

## Decisions

### Keep the realization prompt outside psyche records

The prompt is task direction, not a statement originating from the living psyche. An initially created Vision entry was deleted after the living corrected its provenance. Existing cited Vision and raw records remain the only psyche authority used by the work.

### Divide realization by repository boundary

The compiler/emitter, wire contracts, and Nexus runtime/proof are separate delegated slices. This keeps product edits non-overlapping while allowing the generated contract API to be the explicit dependency between them.

### Keep the executable name `meta-orchestrate`

The component-specific restoration record explicitly orders that name and rejects an alias. It is more specific than the generic `<component>-meta` convention, and the task charter expressly allowed integration evidence to decide the name.

### Put complete wire binding in Ethos

The Interface dialect will gain the minimum explicit channel declaration carrying channel identity, `ContractId`, and `WireRevision`. Ethos-monolith will emit the marker, binding, structural codecs, frame/channel declaration, operations, and closed reply type. A consumer-owned handwritten binding was rejected because these are public interface facts and would leave Ethos short of being the source of the usable wire contract.

### Preserve contract identity and advance the real prior revisions

Existing `ContractId` values remain stable. Wire revisions advance because both contracts change. The source drafts must reconcile against the path-lock carrier branches (`signal-orchestrate` wire 3 and `meta-signal-orchestrate` wire 2), rather than stale main, before choosing the new revisions.

### Treat codec derives as Interface generator policy

Structural archive, rkyv serialization/deserialization, Datom text codec, comparison, clone, and debug support are emitted consistently for Interface data rather than repeated on every Ethos type. The dialect remains responsible for ontology and binding; deterministic Rust mechanics remain the emitter's responsibility.

### Represent daemon startup Signal in argv with base64url

The daemon's single argument is URL-safe unpadded base64 around one framed meta `Configure` value. Arbitrary rkyv bytes cannot be represented directly in an OS argument because of NUL bytes. The wrapper exists only at the OS process boundary: it is decoded and validated immediately and never becomes a socket protocol.

### Reject unsupported Ethos explicitly

The generator must either emit the syntax used by the proving contracts or return a specific generation error. It must never silently drop or guess unsupported constructs. Support is being added demand-first for channel declarations and `Vector<T>` because the proving interfaces require them.

## Sources

- `Vision/ethos.md`, `Vision/ethosMonolith.md`, and `Vision/datom.md` — distilled Ethos/Datom direction.
- `flows/aa4c7747/vision/` and `flows/2b34fafa/vision/` — current Interface syntax, interaction, tuple, source-file, import, and namespace ground.
- `flows/01a02a34/reports/pathLockEpic.md` — prior carrier identities and wire revisions.
- `flows/01a02fd5/vision/metaOrchestrate.md` and `reports/metaOrchestrateRestoration.md` — executable name and interface restoration boundary.
- `flows/01a03603/witnesses/ethosEmitter.md`, `orchestrateInterfaces.md`, and `orchestrateNexus.md` — implementation witnesses when complete.
