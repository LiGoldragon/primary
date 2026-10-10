# Nexus Prior Art: Independently-Compiled, Independently-Restartable Communicating Units

Research date: 2026-08-19. Scope: prior art only. No design proposals.
Sources cited inline. "Inferred" marks conclusions not directly stated in sources.

---

## 1. Systems of Independently-Compiled, Independently-Restartable, Upgradeable Units

### Erlang/OTP

**Unit swapped:** the BEAM module (a compiled `.beam` file for one module). The VM can hold two versions of a module simultaneously — old and new — and migrates processes lazily.

**How state survives the swap:** `gen_server`, `gen_statem`, and similar OTP behaviours expose a `code_change/3` callback. All processes running the old module are suspended before the swap, `code_change` is called on each to transform the old state record into the new shape, then all processes resume together. The appup/relup system encodes these transformation instructions explicitly; the author must write migration logic that understands the old record layout.

**Guarantees:** zero-downtime for the running node if the migration succeeds. No coordination across nodes is automatic — each node upgrades independently. If `code_change` raises, the process crashes and its supervisor may restart it with initial state, losing live state.

**Mechanism:** `.appup` files per application describe upgrade and downgrade steps; `systools:make_relup` composes them into a single `.relup` script of low-level VM instructions. The `release_handler` executes this script live.

Sources: [Erlang release_handler docs](https://www.erlang.org/doc/man/release_handler.html), [Erlang Release Handling guide](https://www.erlang.org/doc/system/release_handling.html), [AppSignal hot code reloading guide](https://blog.appsignal.com/2021/07/27/a-guide-to-hot-code-reloading-in-elixir.html), [eighty-twenty.org hot reloading without OTP release](https://eighty-twenty.org/2024/10/02/hot-reloading-in-erlang)

### MINIX 3 Reincarnation Server

**Unit swapped:** userspace OS services (drivers, servers). The microkernel itself cannot be live-updated; neither can user applications. Only the usermode components that sit between the microkernel and applications are in scope.

**How state survives:** the Reincarnation Server (RS) brings the service to a quiescence state — exploiting the message-based architecture so no in-flight messages are interrupted — then applies the update. State migration details are service-specific; MINIX 3 does not provide a generic state-serialization mechanism equivalent to Erlang's `code_change`.

**Guarantees:** if a driver crashes independently of an upgrade, RS detects the failure and restarts the driver without touching the rest of the system. MINIX 3 can survive driver crashes that would panic a monolithic kernel.

Sources: [MINIX 3 Live Update wiki](https://wiki.minix3.org/doku.php?id=developersguide:liveupdate), [microkernel.info](https://www.microkernel.info/)

### seL4

seL4 is a formally verified capability-based microkernel. It provides strong isolation between user-level components; upgrading a component means restarting that capability domain. seL4 itself provides the isolation primitive; the upgrade orchestration is the user-level system's responsibility. No built-in hot-patching. QNX follows a similar microkernel pattern with resource managers in userspace that can be restarted independently.

Source: [Trustworthy Systems seL4 project](https://trustworthy.systems/projects/seL4/)

### Plan 9 from Bell Labs

**Unit swapped:** services exposed as file-system namespaces via the 9P protocol. Services can be replaced transparently because programs access them through per-process namespace names fixed by convention — replacing the service behind the name is invisible to the consumer.

**How state survives:** no built-in mechanism. The protocol is stateless at the 9P level for most operations; reconnection is the recovery model.

**Guarantees:** structural composability — any replacement service that speaks 9P and presents the same namespace can substitute transparently. The guarantee is interface compatibility, not state continuity.

Sources: [Plan 9 Wikipedia](https://en.wikipedia.org/wiki/Plan_9_from_Bell_Labs), [Plan 9 Bell Labs paper on ResearchGate](https://www.researchgate.net/publication/2859328_Plan_9_from_Bell_Labs)

### OSGi (Open Services Gateway Initiative)

**Unit swapped:** a Java bundle (a JAR with explicit import/export metadata). Bundles can be installed, started, stopped, updated, and uninstalled without restarting the JVM. Apache Karaf is the canonical runtime container.

**How state survives:** no standard mechanism. Bundle stop/start loses in-memory state unless the bundle persists it externally before stopping. OSGi provides lifecycle hooks (BundleActivator) for cleanup and initialization but does not snapshot object graphs.

**Guarantees:** classloader isolation between bundles; dependency resolution enforced at install time; version ranges in imports let multiple versions coexist.

Sources: [OSGi Core 8 spec](https://docs.osgi.org/specification/osgi.core/8.0.0/framework.introduction.html), [Red Hat Fuse OSGi intro](https://docs.redhat.com/en/documentation/red_hat_fuse/7.5/html/deploying_into_apache_karaf/esbosgiintro)

### COM / DCOM

**Unit swapped:** a COM server (an in-process DLL or out-of-process EXE). Versioning uses interface GUIDs — a new interface is a new GUID, coexisting with the old. `IUnknown::QueryInterface` lets clients probe which interfaces an object implements at runtime.

**How state survives:** object identity is per-interface; replacing the DLL on disk and restarting the process loses all state. DCOM adds cross-process and cross-machine remoting, using the same binary vtable contract.

**Guarantees:** binary interface stability (adding new interfaces does not break old clients) but no live migration of running object state.

Sources: [COM Technical Overview, UMD](https://www.cs.umd.edu/~pugh/com/), [Binary Component Model paper](https://doi.org/10.3390/a19080619)

### Microservices

**Unit swapped:** an independently deployed service process (or container). Upgrade by deploying a new instance, shifting traffic, draining the old one (rolling deploy, blue-green, canary).

**How state survives:** external to the process — database, event log, distributed cache. The process itself is stateless or reconstructs state from the store.

**Guarantees:** depends on the infrastructure; no language-level guarantee. The distribution tax (network latency, versioned API contracts, partial failure, observability overhead) is significant: infrastructure costs run approximately 2.5–4x higher than a modular monolith at comparable scale; distributed system coordination consumes 30–50% of engineering capacity once service counts grow.

Sources: [Martin Fowler: Microservice Trade-Offs](https://martinfowler.com/articles/microservice-trade-offs.html), [HLD Handbook: Monolith vs Microservices](https://hld.handbook.academy/curriculum/architecture-patterns/monolith-vs-microservices/), [Medium: The Microservices Tax](https://medium.com/@Iyanudavid/the-microservices-tax-ff6c6a60ba99)

### Actor Systems (Akka / Apache Pekko)

**Unit swapped:** individual actors or actor subtrees. Supervisor strategies restart crashed actors. Cluster Sharding and Persistence (event sourcing) are used to reconstruct state after restarts from a durable event log.

**How state survives:** event sourcing via Akka Persistence replays events to rebuild actor state after a restart. Without persistence, state is lost.

**Guarantees:** isolation between actors; failure does not propagate past supervisor boundaries by default.

Sources: [Akka actor model guide](https://doc.akka.io/libraries/guide/concepts/akka-actor.html), [Apache Pekko actors](https://pekko.apache.org/docs/pekko/current/typed/actors.html)

### Google Fuchsia Components

**Unit swapped:** a component (a sandboxed unit with explicit capability declarations). The Component Framework brokers capability routing between components. Swapping an implementation means providing a new component that exports the same FIDL protocol.

**How state survives:** persistent storage is a capability routed explicitly; it survives component restarts because it is external to the component binary. Component state in RAM is lost on stop.

**Guarantees:** capability routing is typed (FIDL IDL enforces interface shape at build time). The framework resolves which component satisfies a given capability at runtime; implementations are interchangeable if they present the same interface.

Sources: [Fuchsia software model](https://fuchsia.dev/fuchsia-src/concepts/software_model), [Fuchsia component introduction](https://fuchsia.dev/fuchsia-src/concepts/components/v2/introduction), [Fuchsia capabilities](https://fuchsia.dev/fuchsia-src/concepts/components/v2/capabilities)

### Unison (Content-Addressed Code)

**Unit swapped:** a function, identified by the SHA3-512 hash of its syntax tree plus its dependencies' hashes. Names are aliases for hashes; renaming does not change identity.

**How state survives:** deployed services are immutable and addressed by hash. Upgrading means deploying a new hash and switching a name alias to point to it. Rollback is switching the alias back.

**Guarantees:** dependency pinning is exact — you depend on a specific hash, not a version range. Missing dependencies are deployed on the fly.

Sources: [Unison big idea docs](https://www.unison-lang.org/docs/the-big-idea/), [Unison 1.0 production release](https://byteiota.com/unison-1-0-content-addressed-code-hits-production/), [SoftwareMill: code as hashes](https://softwaremill.com/trying-out-unison-part-1-code-as-hashes/)

### Smalltalk and Lisp Images

**Unit swapped:** the image — a snapshot of the live heap. Any definition in the image can be redefined while the system runs. The running system is the development environment; there is no separate compilation step visible to the programmer.

**How state survives:** the image contains all objects. Redefining a class or function takes effect immediately for new message sends; existing objects are instances of the old class until the class is updated or they are migrated explicitly. Smalltalk's `become:` can atomically swap object identity.

**Guarantees:** no process boundary; everything is in one address space. The image saves the full heap. There is no separate deployment unit smaller than the image.

Sources: [Live multi-language development environments, arXiv 1803.10200](https://arxiv.org/pdf/1803.10200), [LispForum: image-based development](https://www.lispforum.com/viewtopic.php?t=785)

### Linux Live Kernel Patching (ksplice, kpatch, kgraft, livepatch)

**Unit swapped:** individual kernel functions. The patch replaces a function pointer at runtime by redirecting calls through a trampolined jump table.

**How state survives:** function-level only; kernel data structures are not migrated. The consistency model: livepatch (the upstream Linux mechanism) uses a hybrid approach — per-task consistency from kgraft (lazy migration, each task switches to patched code at its next safe point: syscall entry/exit or schedule point) combined with kpatch's stack-trace check. Transition typically completes within seconds.

**Guarantees:** security and bugfix patches without reboot. Struct layout changes are not supported; only function body replacements. Kpatch originated at Red Hat (2014); kgraft at SUSE; livepatch merged both approaches into the kernel.

Sources: [Linux kernel livepatch docs](https://www.kernel.org/doc/html/latest/livepatch/livepatch.html), [Red Hat: What is Linux kernel live patching](https://www.redhat.com/en/topics/linux/what-is-linux-kernel-live-patching), [LWN: update on live kernel patching](https://lwn.net/Articles/734765/)

### WebAssembly Component Model

**Unit swapped:** a Wasm component — a binary with explicit import/export interfaces described in WIT (WebAssembly Interface Types). WASI 0.2 (released 2024) standardized the Component Model.

**How state survives:** component state in linear memory is lost on unload. Persistent state must be externalized. wasmCloud's tooling ("wash" CLI) aims at hot-reload for development, but production hot-swap of stateful components is not standardized.

**Guarantees:** interface typing enforced at link time across language boundaries. Components are composable if their WIT signatures match. The Component Model is the closest existing standardized binary-typed interface contract for independently-compiled units.

Sources: [NGINX Unit: Wasm Component Model Part 1](https://docs.nginx.com/nginx-unit/news/2024/wasm-component-model-part-1/), [wasmCloud interfaces overview](https://wasmcloud.com/docs/overview/interfaces/), [WebAssembly 2026 status, Java Code Geeks](https://www.javacodegeeks.com/2026/04/webassembly-in-2026-where-it-has-landed-what-wasi-0-2-changes-and-why-java-and-kotlin-developers-should-pay-attention-now.html)

---

## 2. The Claim That No Compiler Allows Selectively Changing One Part of an Executable

The claim: "there isn't even a compiler out there that allows for selectively changing one part of an executable, it's always just completely recompiled."

The actual state of the art:

**Rust — cargo incremental compilation.** `cargo` has supported incremental compilation since Rust 1.24 (2018). It recompiles only changed crates and their dependents, not the whole graph. Within a crate, incremental compilation recompiles only changed functions' MIR. However, the output is still a single linked binary; the linker re-links the full binary. You cannot hot-patch the running process. The incremental step reduces rebuild time (often to seconds for a leaf crate change), but does not change the monolithic executable model.

**Rust — hot-lib-reloader.** Uses dynamic linking (`crate-type = ["dylib"]`) to extract logic into a `.so`/`.dylib`. The host binary watches the file on disk; when the dynamic library is recompiled and relinked, the host `dlopen`s the new version. This is selective reloading of a dynamic library, not of a function within a monolithic binary. Constraint: only the extracted crate changes; the host binary must be restarted if host code changes. Struct layout changes break the running process.

**Rust — Subsecond / Dioxus 0.7 hotpatch.** Subsecond (2025) intercepts the Rust linking phase, diffs assembly between compiles, and patches the running process by redirecting calls through a jump table. This is binary hot-patching of a running Rust process. Limitations: does not support struct layout changes (the generated code assumes a fixed layout); only tracks the "tip" (leaf) crate — changes to dependencies are not picked up. This is the closest existing Rust mechanism to selective in-executable function replacement, but it is development-mode tooling, not a production mechanism, and it operates at the "tip crate" granularity.

**JVM — HotSwap.** Standard JVM JVMTI-based HotSwap allows reloading a class's method bodies while the JVM is running. Constraint: only method bodies can change; adding or removing methods, fields, or changing signatures requires a full restart (or DCE VM extensions).

**JVM — JRebel.** JRebel extends HotSwap to allow adding and removing methods, fields, and constructors. It preserves object identity and in-heap state. Constraint: it operates on JVM bytecode with a reflective class model; it does not apply to ahead-of-time compiled native binaries.

**JVM — DCEVM + HotswapAgent.** A patched JVM that allows unrestricted class redefinition (including added fields, changed hierarchies). Still JVM-specific.

**Erlang/BEAM.** As described above, the BEAM VM natively runs two versions of a module simultaneously. This is a VM-level feature, not a compiler feature; the compiler always produces a full `.beam` module file. The VM manages the two-version window.

**Lisp / Smalltalk.** Image-based systems redefine individual functions or methods at runtime. The "compiler" produces new bytecode or native code for the new definition; the image-based runtime grafts it in. This is selective change of a running program, but the unit is the entire image, not a separably deployed binary.

**Conclusion (inferred from sources).** The strong form of the claim — that no compiler allows selectively changing one part of an executable — is approximately accurate for production, statically-linked, ahead-of-time compiled native binaries. Incremental compilation reduces recompilation work but still re-links a full binary. Hot-patching mechanisms exist (Subsecond, live kernel patching), but they are function-body-only, cannot change data layouts, are not production-grade for all cases, and require explicit design investment. Dynamic-library segmentation (hot-lib-reloader) is the practical Rust approach, and it is structurally equivalent to the Nexus model: each dynamic unit is compiled and linked independently and loaded at runtime. The Nexus design — separate daemon processes — is a coarser-grained version of the same idea with process isolation instead of shared-process dynamic loading.

Sources: [hot-lib-reloader GitHub](https://github.com/rksm/hot-lib-reloader-rs), [Robert Krahn: Hot Reloading Rust](https://robert.kra.hn/posts/hot-reloading-rust/), [Subsecond crate docs](https://docs.rs/subsecond/latest/subsecond/), [Dioxus 0.7 hotpatch PR](https://github.com/DioxusLabs/dioxus/pull/3797), [Subsecond on Hacker News](https://news.ycombinator.com/item?id=44369642), [JRebel Java HotSwap guide](https://www.jrebel.com/blog/java-hotswap-guide), [DCEVM + HotswapAgent, Sentia blog](https://sentiatechblog.com/using-dcevm-hotswap-agent-in-java-development/)

---

## 3. The "Meta-Kernel That Can Selectively Be Upgraded" — Closest Existing Things

**Erlang VM as meta-kernel.** The BEAM VM is the closest existing thing to this vision in production software: it is a runtime that manages independently-loaded code modules, can run two versions of a module simultaneously, brokers messages between processes, restarts failed processes, and upgrades live. The BEAM itself cannot be hot-patched (upgrading the VM requires a restart), but everything above the VM can be. Inferred: the BEAM is the VM-as-kernel pattern; the Nexus meta-kernel vision extends this to a native execution model.

**Microkernel + userspace servers.** MINIX 3 demonstrates that an OS kernel's drivers and servers can be independently restarted and live-updated. The kernel itself cannot be live-patched. The pattern: the kernel provides IPC and isolation; all meaningful logic lives in userspace servers that can be independently managed.

**Linux livepatch.** Closest to selective executable patching in a production native kernel: individual kernel functions are replaced without reboot. Data structure changes are out of scope. This is the limit of the art for native code hot-patching today.

**Unison codebase manager.** Treats the entire codebase as a content-addressed store. "Upgrading" a function means introducing a new hash and propagating it; old and new coexist in the store. No execution model change required. The "meta-layer" is the codebase manager itself.

**Nix/NixOS system generations.** Each `nixos-rebuild switch` creates an atomic generation: the new system is fully prepared before activation, activation is atomic, and rollback reverts to the previous generation via the bootloader. This is generation-level (whole system) atomicity, not per-service function-level hot-swap. Inferred: this is the closest production-grade example of "selectively upgradeable system components" at the service granularity on NixOS — systemd units are started/stopped around package upgrades, but there is no in-process state migration.

**WebAssembly Component Model.** The WIT interface system provides the typed contract layer for independently-compiled units. The component model is the closest existing standardized binary interface contract for native-adjacent compiled code. Hot-swap of components is an active area (wasmCloud, Spin/Fermyon) but not production-standardized for stateful components.

**Dynamic linking at OS level.** `dlopen`/`dlclose` on POSIX systems, or Windows DLL replacement, is the traditional mechanism: replace a shared library file on disk, unload the old version, load the new one. The OS process is the meta-kernel; the dynamic linker is the loader. This is the mechanism underlying hot-lib-reloader and similar tools.

Sources: as cited above.

---

## 4. Literature on Trade-Offs of This Architecture Shape

**Distribution tax.** Crossing a process boundary introduces: serialization and deserialization cost (even for binary protocols, as opposed to direct memory access); network/IPC latency on every call; the need to version the protocol explicitly (interface drift); observability infrastructure (tracing, correlation IDs) to reconstruct what a stack trace gives for free in a monolith. The literature (Martin Fowler, 2015; HLD Handbook) calls this the "microservices tax." Infrastructure cost difference: approximately 2.5–4x vs. modular monolith at comparable feature scope.

**Versioned contracts between units.** The literature recommends: version contracts aggressively and delete old versions on a fixed deprecation schedule (six months cited as a working policy). Interface drift — schemas and API contracts evolving continuously — becomes a permanent maintenance burden without a non-negotiable retirement policy. Binary typed protocols (as in the Nexus design) reduce drift compared to text protocols because the schema is compiler-enforced, but they do not eliminate the versioning problem — they move it from runtime negotiation to compile-time contract agreement.

**Partial failure.** When a unit is unreachable, callers must decide: retry, circuit-break, return stale data, or surface error. The CAP theorem (Brewer 2000) formalizes the trade-off: a distributed system cannot simultaneously guarantee consistency, availability, and partition tolerance. Erlang's supervision trees are the literature's most worked-out answer to partial failure in this shape of system: every process is supervised; the supervisor's restart strategy (one_for_one, one_for_all, rest_for_one) encodes the failure domain.

**Observability.** In a monolith, a stack trace spans the full call graph. Across process boundaries, a distributed trace must be assembled from spans emitted by each process; this requires instrumentation at every boundary. The literature (OpenTelemetry specification, distributed tracing literature) treats this as a solved but non-trivial infrastructure cost.

**How the best systems pay the tax.** Erlang/OTP: binary message passing (BERT format), supervisor trees, `code_change` state migration, appup/relup tooling. The total cost is paid upfront in tooling and protocol design; the runtime cost is low. Fuchsia: FIDL as the typed IPC IDL, capability routing as the service discovery mechanism, explicit capability declarations as the versioned contract. WebAssembly Component Model: WIT as the IDL, component composition at build time, runtime as the broker. NixOS: atomic generations eliminate partial-upgrade states; the cost is paid in build and activation time.

Sources: [Martin Fowler: Microservice Trade-Offs](https://martinfowler.com/articles/microservice-trade-offs.html), [byteiota: Microservices Tax 2026](https://byteiota.com/microservices-tax-42-ditch-architecture-in-2026/), [Cerbos: Handling failures in microservice architectures](https://www.cerbos.dev/blog/handling-failures-in-microservice-architectures), [developers.dev: API versioning in microservices](https://www.developers.dev/tech-talk/api-versioning-strategies-in-a-microservices-architecture-a-decision-framework-for-tech-leads.html)
