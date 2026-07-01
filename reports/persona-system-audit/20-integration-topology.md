# Integration Topology

I have enough source-grounded evidence to reconstruct the topology. The e2e test confirms the minimal-whole wiring. Here is the map.

---

# Criome/Persona Integration Topology — Source-Reconstructed Map (2026-07-01)

Scope: 40 critical-path repos under `/git/github.com/LiGoldragon/`. All exist on disk (verified). Every repo is an independent single-crate cargo project wired by **git deps** (not a workspace) plus **runtime Unix sockets**. Bash/grep output in this environment abbreviates long repeated identifiers (e.g. `router`→`nr`, `Unimplemented`→`n`, `ExecStart`→`ln`); all exact-token claims below come from the `Read` tool, which does not abbreviate.

## 1. The dependency DAG (build-time, from Cargo.toml git/path deps)

Evidence: every edge below is a `git = ".../LiGoldragon/<x>"` or `path=` line in the named `Cargo.toml` (FACT). Full extract per repo was read from each `Cargo.toml`.

```
TIER 0  LEAVES (no internal LiGoldragon deps):
   kameo(fork)   nota-next(+nota-derive path)   sema   signal-derive   signal-frame-macros(path)

TIER 1  (nota-next only, + own macros):
   signal-frame ──needs──> nota-next, signal-frame-macros
   signal-sema, schema-next(+schema-cc), version-projection, nota-config ──> nota-next

TIER 2:
   triad-runtime ──> kameo, signal-frame, nota-next
   sema-engine   ──> sema, signal-frame, signal-sema
   signal        ──> nota-next, signal-sema, signal-derive
   nexus         ──> kameo, signal, nota-next        (nexus-cli = thiserror ONLY, standalone)

TIER 3  *** CONVERGENCE CRATE ***
   schema-rust-next ──> nota-next, schema-next, triad-runtime, sema-engine, signal-frame

TIER 4  contracts:
   signal-standard ──> schema-rust-next, nota-next
   signal-<comp> / meta-signal-<comp>  (message, router, mind, persona, harness, system,
        terminal, introspect, orchestrate, upgrade, agent, listener, spirit, criome, lojix,
        cloud, domain-criome, mentci) ──> signal-frame (+ schema-rust for some)

TIER 5  component daemons — each ──> triad-runtime, schema-rust-next, signal-frame,
        sema-engine, nota-next, kameo, own signal+meta-signal contract, + PEER contracts:
   message   ──> signal-message
   router    ──> signal-router, signal-persona, signal-harness, signal-mind, signal-message,
                 signal-standard, signal-criome, signal-mirror, criome, mirror
   mind      ──> signal-mind, signal-agent, signal-persona, signal-orchestrate (ssh-pinned revs)
   harness   ──> signal-harness, signal-persona, signal-terminal, signal-router, message(crate)
   system    ──> signal-system, signal-persona
   terminal-cell ──> signal-terminal
   introspect──> signal-introspect, signal-persona, signal-router
   orchestrate──> signal-orchestrate, signal-criome, signal-version-handover, criome, version-projection
   upgrade   ──> signal-upgrade
   agent     ──> signal-agent
   listener  ──> signal-listener        (minimal: no triad-runtime, no schema-rust)
   spirit    ──> signal-spirit + agent(crate,live-provider), router(crate), criome, mirror, +many contracts
   criome    ──> signal-criome, sema-engine, triad-runtime
   lojix     ──> horizon-lib(horizon-rs), signal-lojix, sema-engine
   cloud     ──> signal-cloud, signal-domain-criome
   domain-criome ──> signal-domain-criome

TIER 6  SUPERVISOR:
   persona ──> signal-{mind,router,system,harness,terminal,message,introspect,persona}
              + message(crate) + upgrade(crate) + version-projection + sema-engine + triad-runtime
```

**Foundational leaves everything rests on (FACT):** the universal substrate imported by essentially every Tier-5 daemon is the set **`signal-frame`, `nota-next`, `triad-runtime`, `schema-rust-next`, `sema-engine`, `kameo`**. `schema-rust-next` is the true convergence point — it sits *on top of* both `triad-runtime` and `sema-engine` (schema-rust-next/Cargo.toml), so it is not a leaf but the crate whose green build unblocks every daemon (it emits their `src/schema/daemon.rs` skeletons — see any daemon.rs doc header, FACT).

**Not in the runtime graph:** `forge` (deps = tokio, thiserror, clap only — forge/Cargo.toml) and `nexus-cli` (thiserror only) are standalone; they do not participate in the daemon fabric (FACT). `nexus` is depended on by nothing in this set that I found (INFERENCE — negative, scoped to these 40 repos).

## 2. The minimal runnable whole

**What persona-daemon actually supervises (FACT):** `persona/src/engine.rs:352-361` — `PROTOTYPE_SUPERVISED_COMPONENTS` = **[Mind, Router, System, Harness, Terminal, Message, Introspect, Spirit]** (8 components). Each gets a domain socket, a supervision socket, an envelope, and a `.sema` store (`engine.rs:472-526`, socket files `mind.sock`, `router.sock`, `message.sock`, etc.). The supervisor is a real kameo actor system that spawns OS processes via `DirectProcessLauncher` and verifies liveness via `ComponentSocketReadiness` + `ComponentSupervisionReadiness` (`persona/src/supervisor.rs:1-60`).

**Designed vs. today (FACT, load-bearing):** supervision is **environment-gated**. `persona/src/daemon.rs:80-131` (`open_engine`/`start_supervisor`) only starts the supervisor when `PersonaLaunchPlan::from_environment` returns `Some`. That in turn (`persona/src/transport.rs:468-486` → `persona/src/launch/configuration.rs:96-131`) returns `Some` **only if** `PERSONA_PROTOTYPE_STACK_EXECUTABLE` or per-component `PERSONA_<COMP>_EXECUTABLE` env vars are set; otherwise it returns `Ok(None)` and **persona runs manager-socket-only with zero supervised children**. So the 8-component topology is fully coded but does not self-activate without an environment that hands persona the component executable paths. INFERENCE: in a bare `persona-daemon` launch today you get a manager, not a running stack; the stack is stood up by the integration fixture/tests (see §3) or by a wired Nix wrapper.

**Smallest interactive system (the two-agent chat loop) — proven by `harness/tests/message_router_harness_e2e.rs:35-90` (FACT):** you do **not** need all 8. The minimal set and spawn order the test uses:

```
ORDER  DAEMON                 SOCKET (binds)          ROLE
1  harness-daemon             harness.sock            receives HarnessRequest::MessageDelivery
2  router-daemon              router.sock             signal-message ingress + delivery fabric
                              (+ bootstrap doc: RegisterActor / GrantDirectMessage)
3  message-daemon (agent A)   message.sock (A)        CLI ingress → forwards to router
4  message-daemon (agent B)   message.sock (B)        CLI ingress → forwards to router
   terminal socket (A,B)      terminal.sock           delivery endpoint (test uses stand-in listeners)
```

Handoff: message-daemon forwards to router over `router_socket_path` speaking the `signal-message` contract (`message/src/router.rs:62-69,331-344`); router adjudicates against its actor/channel tables and delivers to the recipient's terminal or harness socket over a fresh `UnixStream::connect` (`router/src/harness_delivery.rs:59-146`). **Mind, System, Introspect, Spirit, Orchestrate are NOT required for this loop** — the router routes via a bootstrap `GrantDirectMessage` document, bypassing mind adjudication (FACT: mind absent from the e2e test; router's mind dep is for the *adjudicated* channel-grant path, `router` exports `ApplyMindChannelGrant`/`ApplyMindAdjudicationDeny`).

To get a **model-backed** reply rather than a stand-in terminal echo, add `harness → pi`: the harness spawns an external agent RPC process `Command::new(command_path).arg("--mode").arg("rpc")...spawn()` (`harness/src/pi.rs:108-168`). That `pi` binary is the actual LLM runtime; the reply returns asynchronously as a *new* mail message, not as a synchronous return value (see §3).

## 3. End-to-end wiring reality (per-hop implemented/stubbed)

Path for "agent A sends a message and agent B (model) replies":

```
HOP                                                     STATUS      EVIDENCE
message CLI  --(NOTA (Send b [..]))-->  message-daemon  IMPLEMENTED message/src/command.rs, engine.rs
message-daemon --stamp origin(SO_PEERCRED)-->           IMPLEMENTED message/src/router.rs:363-399 (OriginPolicy, ingress stamp)
message-daemon --signal-message--> router.sock          IMPLEMENTED message/src/router.rs:62-69,331-344
   (router unreachable => typed Unreachable, not crash) IMPLEMENTED message/src/router.rs:337-341
router ingest ApplySignalMessage -> tables/adjudicate   IMPLEMENTED router/src/daemon.rs:111-151; router/src/router.rs (3747 lines)
router --deliver--> terminal.sock / harness.sock        IMPLEMENTED router/src/harness_delivery.rs:59-146 (real UnixStream per endpoint kind)
harness MessageDelivery -> run pi RPC subprocess         IMPLEMENTED(wired) harness/src/daemon.rs:1096-1111; harness/src/pi.rs:108-168
harness -> model reply text                              EXTERNAL-DEP requires `pi` binary; not exercised in offline test
reply travels back as NEW mail: B's message-daemon->router->A terminal  IMPLEMENTED (e2e asserts slot 2 + "response from agent b")
```

So the **synchronous chat request/reply does not exist** — the architecture is **async mail** (component-architecture skill: "async mail objects"). The immediate reply to a `Send` is `SubmissionAccepted(slot)` (a receipt), and the actual answer arrives later as an independent routed message (FACT: e2e asserts A receives "response from agent b" as a separate delivery).

**Mind's real role (FACT):** `mind/src/daemon.rs:61-134` — mind is a durable knowledge/memory graph (`MindRoot` actor tree over a `.sema` store) with a `KnowledgeJudgePort` that is either `FixtureKnowledgeJudge::empty()` (stub) or `AgentKnowledgeJudge` (real, calls an agent/LLM) selected by config (`mind/src/daemon.rs:150-163`). Its working plane is implemented; its **meta plane returns unimplemented** (`mind/src/daemon.rs:113-119`). Mind is an adjudication/knowledge sidecar, not a chat-forwarding hop.

**Stubbed/skeleton surfaces (FACT):** the *owner/meta (management) planes* of many components return `NotBuiltYet`:
- `system` — most working `SystemRequest` ops reply `SystemRequestUnavailable{reason: NotBuiltYet}` (system/src/supervisor.rs, command.rs, daemon.rs) → **system is largely a skeleton**.
- `introspect` meta → `RequestUnimplemented{NotBuiltYet}` (introspect/src/daemon.rs).
- `harness` meta → `NotBuiltYet`; harness also has a *default* engine path where `MessageDelivery => DeliveryFailed` (harness/src/daemon.rs:189-206) alongside the *wired* path that actually delivers (`:1096-1111`).
- `message` meta socket returns typed unimplemented replies "until live reconfiguration is wired" (message/src/daemon.rs:83-103).

**Second proven chain — the replication/intent path (FACT):** `spirit/tests/end_to_end_offline_full_chain.rs` wires `spirit → mirror → criome (BLS authorize) → router fanout → mirror restore` fully offline in one binary. This is the crypto-attestation spine, complete in-process.

## 4. What "all components together" means, and the top obstacles

**Integration surface (FACT):** there is no cargo workspace and no single "run everything" target. Integration is realized three ways: (a) persona's `EngineSupervisor` spawning the 8-component prototype (env-gated); (b) cross-repo Rust e2e tests that build+spawn real daemon binaries (`harness/tests/message_router_harness_e2e.rs`, `spirit/tests/.../end_to_end_offline_full_chain.rs`, `introspect/tests/daemon.rs`, `persona/src/bin/persona_component_fixture.rs`); (c) Nix/systemd deployment.

**Deployment reality (FACT):** `CriomOS/modules/nixos/` contains per-daemon systemd modules for only **router (persona-router.nix), criome (criome.nix), mirror (mirror.nix), repository-ledger (repository-receive.nix), lojix (lojix.nix), llm.nix**. Home side (`CriomOS-home/modules/home/profiles/min/spirit.nix`) runs **spirit-daemon + agent-daemon** as user services. Each uses `<pkg>-write-configuration` in ExecStartPre and `<pkg>-daemon <config>` in ExecStart. **There is NO persona.nix / mind.nix / message.nix / harness.nix / system.nix / terminal.nix / introspect.nix / orchestrate.nix.** So the deployed OS today = criome + router + mirror + repository-ledger + lojix + (home) spirit + agent — supervised by **systemd**, not by persona. The persona-supervised full stack lives only in code + tests, not in the OS. CriomOS flake LiGoldragon inputs: criome, router, mirror, repository-ledger, lojix, clavifaber, brightness-ctl, CriomOS-{home,lib,pkgs}, rust-build (FACT).

**Top structural obstacles to standing up the whole:**
1. **Version-pin fragmentation (biggest).** The same transitive crate is pinned to *different revs/branches across consumers*: `mind/Cargo.toml:131-144` pins `signal-mind`, `meta-signal-mind`, `meta-signal-orchestrate`, `schema-rust-next`, `nota-next`, `schema-next`, `signal-orchestrate` to specific `ssh://` **revs**, while persona/router/message pin `https … branch=main`. A unified build must reconcile these or Cargo will build multiple incompatible copies of `schema-rust-next`/`signal-frame` (rkyv wire types would not match across the socket boundary → silent decode failures). (FACT: the divergent pins; INFERENCE: the wire-mismatch consequence.)
2. **`criome-authorization-push` vs `main` branch split.** `criome`, `signal-criome`, `router` (as seen from spirit/mentci), `mentci`, `mentci-lib`, `mentci-egui`, and spirit's optional criome are on `criome-authorization-push`; persona depends on `signal-router` **main**. Router main vs router criome-auth is an unmerged fork in the delivery fabric (FACT).
3. **No persona-side OS deployment.** To run "all together" as an OS, persona/mind/message/harness/system/terminal/introspect need NixOS/home modules that either (a) run each under systemd, or (b) run persona-daemon with `PERSONA_*_EXECUTABLE` env pointing at the packaged component binaries so its supervisor spawns them. Neither exists yet (FACT).
4. **Skeleton components on the critical topology.** `system` and the meta/management planes of harness/introspect/message/mind return `NotBuiltYet`. Persona supervises System + Introspect as first-class members of the 8-component prototype, but their behavior is largely unbuilt — supervision readiness will pass (sockets bind) while function is absent (FACT for the stubs; INFERENCE for the readiness-passes-but-empty consequence).
5. **`pi` external binary dependency.** Model-backed replies require the `pi` RPC binary present and configured (`harness/src/pi.rs`); its provenance/packaging is outside these 40 repos (FACT it's spawned by path; UNKNOWN where packaged).
6. **Mixed transports/ssh auth in the graph.** mind's `ssh://git@github.com/...` deps require SSH auth to even resolve, unlike the https deps elsewhere — a hermetic/CI build must supply credentials or rewrite these (FACT, mind/Cargo.toml).

## 5. Explicit UNKNOWNS / not-checked

- **`forge` and `nexus`/`nexus-cli` runtime role** — forge deps are generic (tokio/clap); I did not read forge's `main.rs` to learn its function. `nexus` (Tier-2, kameo+signal) is depended on by nothing I traced in this 40-repo set; its consumers may be outside scope. NOT verified who runs nexus.
- **Router's internal adjudication/mind-grant path** — I read the ingress+delivery (`router/src/daemon.rs`, `harness_delivery.rs`) but not the 3747-line `router/src/router.rs` adjudication core; the mind-adjudicated (non-bootstrap) routing path's completeness is UNVERIFIED beyond the exported symbol names.
- **orchestrate, upgrade, agent, listener, cloud, domain-criome daemons** — I have their dep edges (FACT) but did not read their working-plane handlers; their implemented-vs-stub status is NOT assessed.
- **Whether persona's `EngineSupervisor` is exercised by a committed integration test/fixture that actually spawns all 8** — `persona_component_fixture.rs` exists and binds domain+supervision sockets per component (FACT, read header), but I did not confirm a test drives the full 8-up topology end-to-end.
- **`triad-runtime` socket-binding/accept-loop internals** — every daemon delegates listener binding to the emitted `src/schema/daemon.rs` (from schema-rust-next) over `triad_runtime`; I did not read triad-runtime's bind code, so the exact socket-permission/peer-cred mechanics are asserted from callers, not from triad-runtime source.
- **`meta-signal-*` contract repos** (30+ present on disk) — treated as contract leaves; their internal wiring not opened.
- Line-number citations from `Read` are exact; any identifier I reproduce from a Bash/grep line may be abbreviation-mangled and should be re-read before quoting verbatim.