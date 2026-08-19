# Nexus Prior Art: Sockets, Contracts, Binary Wire Formats, and Capability Privilege

Research commissioned 2026-08-19. All claims attributed; inferences flagged explicitly.

---

## 1. Separating a Privileged Control Interface from the Ordinary Service Interface

### 1.1 SDN: Control Plane vs Data Plane

In Software-Defined Networking (SDN), the control plane (deciding where traffic goes) is separated from the data plane (actually forwarding packets). OpenFlow is the southbound protocol: the controller sends instructions over a secure channel (TLS over TCP) to switches. The controller "programs the network"; network devices forward based on flow tables installed by the controller. No switch exposes raw control operations to ordinary traffic. Source: [MDPI SDN/OpenFlow survey, 2014](https://www.mdpi.com/1999-5903/6/2/302); [GeeksforGeeks SDN](https://www.geeksforgeeks.org/computer-networks/software-defined-networking/).

What is separated: forwarding decisions (control) from packet handling (data). Privilege is established by the channel itself — only the controller may write to the flow table.

### 1.2 Envoy Proxy Admin Interface

Envoy exposes two surfaces: the main proxy ports (data plane, one per listener) and an administration interface on a separate address (typically TCP :9901 or a Unix socket). The admin interface exposes destructive operations: `/quitquitquit` shuts the proxy down; `/clusters`, `/config_dump`, and `/stats` expose internal state. Envoy's own documentation describes these as operations requiring access control separate from the data path. The Istio community filed an issue to move the admin interface to a Unix domain socket precisely because binding it to 0.0.0.0 over TCP exposes it to any container in the same network namespace. Sources: [Envoy admin docs](https://www.envoyproxy.io/docs/envoy/latest/operations/admin); [Istio issue #19684](https://github.com/istio/istio/issues/19684); [Envoy misconfigurations article](https://medium.com/@smgtknn/envoy-proxy-misconfigurations-you-can-easily-fall-into-7b2effc6e076).

What can go wrong when the two are merged: any client that can reach the main proxy port can also reach `/quitquitquit`.

### 1.3 Docker: One Socket, One Privilege Level — A Cautionary Shape

Docker exposes a single Unix socket `/var/run/docker.sock` owned root:docker, mode 0660. Any process in the docker group can ask the daemon to do anything the daemon can do — which is everything root can do. There is no fine-grained separation inside the socket: the ordinary user interface and the privileged management surface are the same surface. Membership in the docker group is effectively root. Source: [Netdata docker socket security](https://www.netdata.cloud/guides/docker/docker-socket-security/); [Docker daemon docs](https://docs.docker.com/reference/cli/dockerd/); [kkloudtarus Docker architecture](https://kkloudtarus.net/en/blog/docker-architecture-client-daemon-containerd-and-runc).

Inference: Docker's design is the canonical case of what happens when privileged and ordinary surfaces are merged. The Nexus two-socket design avoids this by construction.

### 1.4 Plan 9: ctl Files as a Control Surface Alongside Data Files

In Plan 9, resources are presented as file hierarchies. Devices expose both data files (e.g., `/dev/eia0` for serial data) and control files (`/dev/eia0ctl`). Writing to the ctl file configures the device ("b1200" sets 1200 baud). The Plan 9 network stack uses a ctl file per conversation: writing "connect address!port" to a ctl file initiates an outgoing connection. The data file is for payload; the ctl file is for control. Sources: [Plan 9 network doc](https://9p.io/sys/doc/net/net.html); [Plan 9 system doc](https://plan9.io/sys/doc/9.html). Note: Plan 9's ctl files use ASCII strings — this is the opposite of the Nexus binary-only principle but the structural separation of control from data is the same idea.

### 1.5 D-Bus: System Bus vs Session Bus

D-Bus distinguishes the system bus (used by privileged, system-wide services) from per-user session buses (used by user-scoped services). Access control is enforced by XML policy files: the system bus policy grants specific operations only to specific Unix users or groups. A process on the session bus cannot access another user's session bus or cross into the system bus without the appropriate policy grant. Source: [D-Bus specification](https://dbus.freedesktop.org/doc/dbus-specification.html); [D-Bus explained](https://everything.explained.today/D-Bus/).

What this separates: user-scope operations from system-scope (privileged) operations. Privilege is established by the bus the caller connects to plus the kernel-enforced identity of the calling process.

### 1.6 systemd: Private Control Socket Alongside D-Bus

systemd (PID 1) exposes most of its management API over D-Bus. It also maintains a private socket at `/run/systemd/private`. This socket is used by systemctl in specific conditions: before D-Bus is available (early boot), and for certain internal operations. The general API is D-Bus; the private socket is the privileged back channel. Source: [systemd/systemd CONTROL_GROUP_INTERFACE docs](https://github.com/systemd/systemd/blob/main/docs/CONTROL_GROUP_INTERFACE.md); [systemd narkive thread](https://systemd-devel.freedesktop.narkive.com/3T7mdzJv/question-about-systemctl-and-its-related-commands).

### 1.7 SO_PEERCRED: Kernel-Enforced Identity on Unix Sockets

On Linux, a process reading from a Unix domain socket can call `getsockopt(SO_PEERCRED)` to obtain the pid, uid, and gid of the connected peer as recorded by the kernel at connect time. These values cannot be spoofed. MySQL's `auth_socket` plugin and PostgreSQL's peer authentication use this mechanism to grant access based on OS identity rather than a password. This is one technique for establishing privilege on a single socket without a second socket: the daemon inspects who is on the other end and grants or denies operations based on that identity. Source: [Linux unix(7) man page](https://man7.org/linux/man-pages/man7/unix.7.html); [MySQL socket auth](https://dev.mysql.com/doc/mysql-security-excerpt/8.0/en/socket-pluggable-authentication.html); [PostgreSQL SO_PEERCRED patch](https://www.postgresql.org/message-id/20100718155101.11E297541D5%40cvs.postgresql.org).

### 1.8 Erlang: System Messages vs Ordinary Messages

In OTP, system messages (used by the sys module to suspend, resume, or get state from a process) are a distinct message class, structurally separate from the ordinary messages a process handles. A process implementing `gen_server`, `gen_statem`, etc. has its handle_call/handle_info callbacks for user messages and a separate system message path handled by the OTP behaviour's receive loop before user messages are dispatched. The separation is enforced by convention and library design, not by a socket or OS primitive. Source: [Erlang OTP documentation](https://www.erlang.org/doc/apps/erts/erlang.html).

---

## 2. Binary Typed Wire Contracts Compiled Into Each Party

### 2.1 Protocol Buffers (protobuf)

Google's protobuf defines a schema in `.proto` files. Both producer and consumer compile the schema into language-specific code; the wire format carries field numbers (not names) and type tags, relying on the shared compiled schema for full interpretation. Schema evolution rules: fields can be added (new field numbers), but removing or reusing a field number breaks compatibility. The schema is not transported on the wire. Source: [protobuf evolution guide](https://oneuptime.com/blog/post/2026-01-24-protocol-buffer-evolution/view).

### 2.2 Cap'n Proto

Cap'n Proto was designed by Kenton Varda (former protobuf maintainer). Key properties:
- Zero-copy: the wire bytes are the in-memory representation; no parse step.
- Schema compiled into each party; not transported on the wire.
- Evolution rules: new fields and enumerants may be added as long as each new member's ordinal is larger than all previous ones; members may be reordered in source as long as ordinals are preserved. Renaming does not break ABI.
- The wire format carries enough information to recursively copy a message without knowing its schema (unlike FlatBuffers or SBE).
- Cap'n Proto also has an RPC layer (CapTP) derived from E's network protocol (see section 4). The RPC layer is capability-based.
- "Closed vocabulary" on the wire: if a receiver encounters an unknown field ordinal it ignores it; if it encounters an unknown union discriminant it treats it as "unknown". Forward-compatibility is built into the format.

Sources: [Cap'n Proto introduction](https://capnproto.org/); [Cap'n Proto schema language](https://capnproto.org/language.html); [Cap'n Proto vs FlatBuffers vs SBE comparison](https://capnproto.org/news/2014-06-17-capnproto-flatbuffers-sbe.html); [Cap'n Proto Wikipedia](https://en.wikipedia.org/wiki/Cap%27n_Proto).

### 2.3 FlatBuffers

Google's FlatBuffers is also a zero-copy binary format with schema. Unlike Cap'n Proto, it does not store type information sufficient to copy a message without its schema. Evolution rule: fields may be added (using table fields, not structs), but cannot be removed — only deprecated. Field order must be preserved. Source: [FlatBuffers schema overview](https://new.halfrost.com/flatbuffers_schema/); [binary formats comparison](https://medium.com/@shekhar.manna83/binary-serialization-formats-e2703f053010).

### 2.4 Simple Binary Encoding (SBE)

SBE targets ultra-low latency financial systems. It does not carry any type information on the wire; interpretation is entirely schema-dependent. The schema is compiled into codecs on both sides. SBE does not allow copying without the schema. Source: [Cap'n Proto vs FlatBuffers vs SBE](https://capnproto.org/news/2014-06-17-capnproto-flatbuffers-sbe.html).

### 2.5 Fuchsia FIDL

FIDL (Fuchsia Interface Definition Language) is Fuchsia's IPC schema system. FIDL is "primarily concerned with defining ABI concerns." The wire format is what constitutes the ABI; the FIDL source and generated bindings are the API but not the ABI. Protocols compiled into each party. Evolution affordances: methods may be added and removed; flexible unions allow old clients to ignore new variants; renaming types does not break ABI. Source: [FIDL overview](https://fuchsia.dev/fuchsia-src/concepts/fidl/overview); [FIDL ABI/API compat guide](https://fuchsia.dev/fuchsia-src/development/languages/fidl/guides/compatibility).

FIDL is also the mechanism through which Fuchsia's capability-based handles pass between components — the protocol defines what handles are passed and what authority they carry (see section 4).

### 2.6 rkyv

rkyv is a Rust zero-copy serialization library. The archived (serialized) form is directly usable as a Rust value without any parse step. Endianness is configurable via cargo features (`archive_le`, `archive_be`) for portability. It does not have a full schema system and is not designed for schema migration. Source: [rkyv crate](https://docs.rs/rkyv); [rkyv GitHub](https://github.com/rkyv/rkyv).

The psyche's stated format is portable rkyv (endianness fixed, settings consistent); Cap'n Proto was identified as the cross-platform zero-copy alternative (termed "universal signal" in design session 6863ef19, deferred pending Rust-to-capnp-schema tooling).

### 2.7 Erlang External Term Format (ETF)

Erlang encodes all inter-node messages (across distribution) using the external term format: a self-describing binary encoding of Erlang terms. Both sides know the format because both run BEAM. The format is typed (integer, atom, binary, list, tuple, etc.) and carries enough information to decode without out-of-band schema. Unlike the schema-compiled formats above, ETF is a universal term encoding, not a specific schema per service. Source: [Erlang ETF docs](https://www.erlang.org/doc/apps/erts/erl_ext_dist.html).

### 2.8 ASN.1 / DER

ASN.1 is one of the oldest binary schema systems (1984, X.208/X.680). DER (Distinguished Encoding Rules) is the strict canonical binary encoding used in X.509 certificates, TLS, and PKCS. The schema is compiled into each party. ASN.1 is the deepest ancestor of the "schema compiled into parties, binary wire" pattern. Source: standard references; context only.

### 2.9 Consumer-Driven Contracts (Pact)

Pact is the dominant consumer-driven contract testing framework. The consumer publishes a contract describing what it needs (specific fields, specific types) from the provider; the provider verifies it can satisfy the contract. This is not a wire format but a contract discipline: each consumer relationship has its own explicit contract, and the provider is validated against the union of all consumer contracts. Source: [Pact docs](https://docs.pact.io/); [totalshiftleft API contract testing](https://totalshiftleft.ai/blog/what-is-api-contract-testing).

Inference: the Nexus concept that "a Nexus speaks only the contracts it is compiled with" maps structurally onto compiled-schema binary formats (protobuf, FIDL, Cap'n Proto), where each party has exactly the contracts it was compiled with and nothing else can pass through the wire. The consumer-driven contract testing ecosystem formalizes the discipline of explicit, enumerated relationships between parties — closer to the social/process side of the same idea.

---

## 3. The Thin CLI as the Only Text Boundary

### 3.1 Docker: CLI Translates to REST, Daemon Never Sees Text Commands

The docker CLI translates user text commands into REST API calls (JSON over the Unix socket or TCP). The daemon (dockerd) handles only structured API calls; it never parses the human-readable text the user types. Source: [Docker client-server architecture](https://oneuptime.com/blog/post/2026-02-08-how-to-understand-the-docker-client-server-architecture/view); [inside Docker architecture](https://dev.to/srinivasamcjf/inside-docker-the-complete-architecture-explained-from-cli-to-kernel-4mf1).

Note: Docker's daemon-side format is JSON (text), not binary. The boundary is at the CLI, but the daemon still handles a text format, not a binary one.

### 3.2 Plan 9: File Servers Never Parse Human Text; Shells Do

In Plan 9, file servers (daemons) speak 9P, a binary message protocol. The shell (rc) and userland tools assemble 9P messages; the file server never sees or produces human-readable text. Text rendering is entirely the responsibility of the tool layer. The file server's job is 9P operations: Tattach, Twalk, Tread, Twrite, etc. Source: [9P protocol (Wikipedia)](https://en.wikipedia.org/wiki/9P_(protocol)); [The ubiquitous file server in Plan 9](https://www.researchgate.net/publication/228745747_The_ubiquitous_file_server_in_plan_9).

Qualification: Plan 9's ctl files (section 1.4) use ASCII strings as their payload, which is the exception to this — the data path is binary 9P but the control payload is ASCII. This is an internal inconsistency in Plan 9's design, not an endorsement of text in the daemon.

### 3.3 systemd: systemctl as the Text Layer Over a Binary/D-Bus Daemon

PID 1 never parses human-readable text. systemctl serializes commands into D-Bus method calls; PID 1 handles D-Bus messages. The text output the user sees from `systemctl status` is produced by systemctl, not by PID 1. PID 1 returns structured data; systemctl renders it. Source: [systemctl and unit management (DeepWiki)](https://deepwiki.com/systemd/systemd/9.1-systemctl-and-unit-management).

### 3.4 Fuchsia: ffx as the Text Boundary Over FIDL

ffx is Fuchsia's unified developer CLI. It communicates with an ffx daemon via FIDL over a Zircon channel (or an overnet emulation of one on the host). The daemon handles FIDL-typed messages; ffx handles argument parsing and human-readable output. FIDL is binary-typed; the text boundary is at ffx. Source: [The ffx tool](https://fuchsia.dev/fuchsia-src/development/tools/ffx/overview); [ffx CLI architecture](https://fuchsia.dev/fuchsia-src/development/tools/ffx/architecture/cli); [Zircon handles](https://fuchsia.dev/fuchsia-src/concepts/kernel/handles).

### 3.5 LSP: A Counter-Example That Chose Text Throughout

The Language Server Protocol (LSP), designed by Microsoft to decouple language intelligence from editors, chose JSON-RPC as its wire format — a text-based protocol over stdio or a socket. The language server daemon parses JSON. This is a deliberate choice to maximize interoperability across language runtimes (a TypeScript editor, a Python server, a Java server all speak the same JSON-RPC). The cost is that every party must parse and render text on every message. Source: [LSP specification](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/); [LSP overview](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/).

Inference: LSP made text universal because it valued breadth of interoperability over binary efficiency. The Nexus design makes the opposite trade — pure binary in the daemon, text only at the CLI — because the daemon's simplicity and correctness are valued over runtime polyglotism.

---

## 4. The Object-Capability View of Sockets and Privilege

### 4.1 The Object-Capability Model

The object-capability model holds that a reference to an object is simultaneously authorization to use that object. Possession of the reference is the only credential; there is no ambient authority. "In a pure capability-based system, there's no such thing as 'I'm root, give me access to everything.' You have specific capabilities for specific resources." Sources: [Capability-based security (HandWiki)](https://handwiki.org/wiki/Capability-based_security); [ocap security article (Medium)](https://medium.com/@sohail_saifii/the-capability-based-security-model-that-makes-privilege-escalation-impossible-8231d679b972).

### 4.2 E Language and CapTP

E is a capability-safe language developed by Mark Miller and others at Electric Communities in the 1990s. E's CapTP (Capability Transport Protocol) defines how capabilities (object references granting authority) are conveyed across a network boundary in an unforgeable way. References are passed explicitly; no caller can gain access to a resource without first being given a reference by a party that already holds one. Source: [awesome-ocap (GitHub)](https://github.com/dckc/awesome-ocap); [Hacker News Cap'n Proto / E lineage](https://news.ycombinator.com/item?id=9484643).

### 4.3 Cap'n Proto RPC: CapTP Implemented

Cap'n Proto's RPC layer is explicitly derived from E's CapTP. Kenton Varda confirmed this directly: "Cap'n Proto's RPC layer is based on E's CapTP protocol." Features inherited: three-way introductions (a server can introduce a client to a third party by giving it a capability), promise pipelining (chaining operations before earlier ones complete), and SturdyRefs (persistent capabilities). Access to a resource is impossible without possession of the capability; capabilities are unforgeable tokens conveyed over Cap'n Proto channels. Source: [Hacker News thread](https://news.ycombinator.com/item?id=9484643); [Cap'n Proto introduction](https://capnproto.org/); [Cap'n Proto groups.google](https://groups.google.com/g/friam/c/0HFPWRMPkkY).

### 4.4 seL4: Formally Verified Capability Kernel

seL4 is a formally verified microkernel. Its security model is capability-based: every kernel object (thread, address space, IPC endpoint, device frame) is accessed through a capability stored in a capability derivation tree. The kernel enforces: (a) you cannot access an object without a valid capability; (b) capabilities cannot be forged; (c) authority confinement — there is a formal proof of an upper bound on how authority can propagate. Source: [seL4 verified protection model](https://trustworthy.systems/publications/nicta_full_text/1474.pdf); [seL4 capabilities tutorial](https://github.com/sel4/sel4-tutorials/blob/master/tutorials/capabilities/capabilities.md).

### 4.5 Fuchsia / Zircon Handles

In Fuchsia, every kernel object (channel, socket, VMO, process, thread, eventpair, etc.) is accessed through a handle — an unforgeable integer token held in a process's handle table. Handles are transferred between processes only through explicit passing over channels; there is no global namespace for kernel objects. A process with no handle to a channel has no way to access it. The FIDL layer defines what handles are passed in a protocol call and what rights they carry. Source: [Zircon fundamentals](https://fuchsia.dev/fuchsia-src/get-started/learn/intro/zircon); [Zircon handles](https://fuchsia.dev/fuchsia-src/concepts/kernel/handles); [Understanding Fuchsia Security (arxiv)](https://arxiv.org/pdf/2108.04183).

### 4.6 The Meta-Socket as a Capability

Inference (flagged as inference): in the capability-security framing, a socket is itself a capability: possession of a file descriptor to a socket is authorization to use it. A process cannot access a Unix socket it has not been given (or been allowed to open by filesystem permissions). The Nexus two-socket design — where the meta-socket is the privileged surface — maps onto the object-capability model naturally: the meta-socket descriptor is the capability that grants privileged operations. A client that holds only the regular socket descriptor cannot escalate to privileged operations because it literally does not possess the meta-socket capability. This is structurally analogous to seL4's capability table and Fuchsia's handle table: authority is precisely what you hold, nothing more.

---

## Summary of Convergence Points

| Nexus property | Closest prior art |
|---|---|
| Two sockets: regular and meta | Envoy data vs admin; D-Bus session vs system; systemd D-Bus vs private socket |
| Meta-socket grants privileged configuration | Plan 9 ctl files; SO_PEERCRED authenticated sockets |
| Pure binary, no text in the daemon | Plan 9 9P; Fuchsia ffx + FIDL; systemd D-Bus |
| Contracts compiled into each party, not transported on wire | Cap'n Proto, protobuf, FlatBuffers, FIDL |
| Schema evolution via ordinal rules | Cap'n Proto (ordinal rule); FIDL (flexible union); protobuf (field numbers) |
| Two contracts per Nexus (one per socket) | FIDL per-endpoint protocol definitions |
| Only CLI textalizes | Plan 9 rc; ffx; systemctl |
| Socket as capability (meta-socket = authority) | Fuchsia handles; seL4 capabilities; Cap'n Proto CapTP / E |

---

## What the Prior Art Does Not Quite Do

Noted without inference about the Nexus design:

- No prior system found that issues two typed binary sockets per daemon with distinct compiled contracts per socket as an architectural invariant for all components. The separation exists in individual systems (Envoy, systemd) but is not a universal compositional primitive.
- Consumer-driven contract testing (Pact) formalizes the "each relationship has its own contract" idea for service testing but does not compile contracts into binaries; it works at the test/verification layer.
- rkyv has no schema language or schema evolution mechanism; the psyche has noted this limitation (session 6863ef19: portability requires explicit endian settings) and identified Cap'n Proto as the migration path when cross-runtime support is needed.

---

*Research agent: sonnet-4.6, session e06e4c07. Sources cited inline. All inferences explicitly marked.*
