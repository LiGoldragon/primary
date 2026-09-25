# Audit pack: Flow, Messenger, Field and their -clj versions (for Fable 38de5b)

Collected 2026-09-25 by an e51411 subflow on ouranos. **W** means witnessed here (command or file read). **C** means another flow's claim, not re-checked. Each task below is sized for one Opus subagent.

## 1. Flow (Rust nexus)

**The living's words.**
- "It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed." (2026-09-25, e51411 vision/launch.md)
- "A flow's ID is claimed for it by code as it starts" / "This could easily be done by code." (2026-09-24, vision/launch.md)
- "Anything that's not clear about all of the nexuses and specifically flow and message not getting working" (2026-09-25, vision/nexus.md)
- "I'm introducing the notion of specialized flows so there's a specialty type. That's a different kind of call, basically, than the regular flow call." (2026-09-25, vision/flowAspect.md)

**What exists.**
- Canonical main is 812053c "Release Flow 0.7.0". Workspace version 0.7.0. **W**
- Live: `flow-nexus.service` is active and runs `/nix/store/99rq…-flow-0.6.0/bin/flow-nexus`, started 13:52 CST. `~/.nix-profile/bin/flow` is also 0.6.0. The unit file comes from home-manager. **W**
- `flow --version` fails with `invalid Flow query … expected "Query", found "--version"`. No crate handles a `--version` flag (grep finds none); the client takes only one inline Query datom. **W**
- Flow pins `signal-flow` at `ab70332`. That revision exists only on the branch `origin/flow/system-prompt-bundle-00f95a`. `signal-flow` main (968ae3b) has only Start, Restart and ResolveRecipient, with no Send, Stop or List. **W**
- `crates/flow-nexus/src/store.rs:370-380` has a store-level Query handler that answers Send, Stop and List with `PersistenceRefused`. The real handlers are in `lib.rs:~470`. **W**
- The Home consumer (e6f60a1) and CriomOS consumer (58b4c6b) for 0.7.0 exist only on branches. 504461 has no activation, List or Start receipt. **C** (b7da5d, 504461 log)
- The Prometheus builder is unreachable: `ssh prometheus` times out on port 22. **W**
- Specialized Start exists only as a proposal (38de5b reports/specialties-distillation.md; f5a74e "outside Malli"). **W**

**Tasks.**
- **F1. Merge the signal-flow branch into main.** Fast-forward or merge `flow/system-prompt-bundle-00f95a` (ab70332) into signal-flow main. Then repin Flow to a main revision. Verify: `git -C signal-flow merge-base --is-ancestor ab70332 origin/main`, and `cargo build` of flow passes.
- **F2. Add a version answer to the Flow CLI.** In `crates/flow/src/main.rs`, handle `--version` (print `CARGO_PKG_VERSION`) before datom parsing, and do the same for `flow-nexus`. Release this as 0.7.1 so the Field's "verify --version 0.7.0" gate becomes checkable. Verify: `flow --version` prints `0.7.x`.
- **F3. Deploy 0.7.x on ouranos.** Owner is 504461 (the Field). Integrate the Home and CriomOS consumer branches onto main with 0.7.x. Build (the builder blocker is F4). Activate, restart `flow-nexus`, then witness the store path, one List and one disposable Start.
- **F4. Restore the Prometheus builder, or rule on a local build.** Diagnose why ouranos cannot reach Prometheus (Yggdrasil over the cable, per the e51411 log). The alternative is to ask the living whether a local build is allowed. The nix-workflow skill forbids a local fallback. Verify: `ssh prometheus true` succeeds and `nix build --builders …` succeeds.
- **F5. Remove the legacy refusals.** Delete or make unreachable the `store.rs` handler that refuses Send, Stop and List, or cover it with a test proving the live path never uses it. Verify: `cargo test`, plus a grep showing only one Query dispatch.
- **F6. Draft the Start anatomy with shorthands.** Write an ethos draft for one central Start (the thirteen-field profile), named shorthands (for example StartPsyche.{ Model }), and StartSpecialized.{ Profile Specialty Origin }. The source is specialties-distillation.md §2 and §5. This is design work for the living's review, not code.

## 2. flow-clj

**The living's words.**
- "It's like a flow [Clojure], simple and easier to implement than the rest. Simple flow with, again, the EDN input, typed input." (2026-09-25, flowAspect.md)
- "Astra should implement that on both sides." (same)
- "It's just CLJ … flow-CLJ … a simple standalone CLI … let's use the power of Nix there." (2026-09-25, flowAspect.md)

**What exists.**
- Mind's contract is flows/f5a74e/reports/clojure-flow-input.md. It defines `#start [aspect exact-model effort power goal skills origin]`, `#stop [flow-id]`, `#list []` and `#send [flow-id body]`. No-data variants are keywords and data-bearing variants are tags. There is no transport. **W**
- No `flow-clj` repository exists under /git/github.com/LiGoldragon. **W** The work was relayed to 504461 as its third step, after the 0.7 deploy and two test flows. **C**

**Tasks.**
- **C1. Build flow-clj.** Create `LiGoldragon/flow-clj` with a Malli-closed reader for the four forms, and wire it to Herdr, or to the Flow socket if it is live. The living said the Field implements it (Astra), so place this under 504461 or a fresh Field Astra. Verify: tests reject a wrong arity, an unknown tag and a display name used as a model; `#list []` returns the live bindings; one `#start` produces a registered pane.

## 3. messenger-clj

**The living's words.**
- "A message is really just a message." / "Let's cut this [right] the fuck down." (2026-09-25, vision/messaging.md)
- "It knows which pane the call came from so we can use the database to know the aspect and the model." (2026-09-25, messaging.md)
- "There should be three hashtags there, right? … Let's look at that also closely with Fable" (2026-09-25, notion/message.md)
- "maximize the message that you send because it has more value or a higher strata." (2026-09-25, messaging.md)
- "the registry would become this Datomic … Like a relational database with datomic-like syntax" (2026-09-25, messaging.md)
- "Even the nexus should be called Messenger." (2026-09-25, messaging.md)
- "We can get a fully actually real concept … instead of just making the agents pretend that they're talking through datom but it's not processed." (2026-09-25, messaging.md)

**What exists.**
- Canonical main is d4f2d08. The installed binary is `~/.local/libexec/messenger-clj` → `/nix/store/q5r1…-messenger-clj-0.1.0`. `hm-*` are wrappers that call `bb` with a bundled `dist/messenger-clj.clj`. The Datalevin pod is 0.8.25. State is under `~/.local/state/messenger-clj/typed-datalevin`. **W**
- The pane line is `#msg ["<sender>" "<text>"]`. The sender comes from the `FLOW_ID` environment variable, so it is self-asserted (core.clj:614). The registry schema has no aspect or model attribute. **W**
- The cap is `relay`, core.clj:108, at 800 characters on one line. A body with more than 3 lines, more than 800 characters, or a pasted-content marker is written to `flows/<sender>/messages/<stamp>-<recipient>-<uuid>.md`. The pane then gets only "Message too long for a pane; read <path> in full." These files are not committed (38de5b log line 54). **W**
- There are two Malli schema sets. core.clj:18-29 defines FlowId (regex), NativeThread, RouteBinding (`:state` optional) and others. typed_store.clj:20-55 defines Route (`:state` required, `:flow :string`, no regex) and others. They overlap and have drifted. **W**
- There is a `Ledger` protocol and `DatalevinLedger`, but no CLI subcommand reads an attempt back. The commands are send, send-abrupt, list, register, deregister, rebind, move, retire and heartbeat-state. An "Uncertain.{ flow attempt-… }" result cannot be looked up. **W**
- `check.nix` only runs `--help` and tests that `hm-send` is executable. The Clojure tests (36 tests / 276 assertions, per a C claim) are not a flake check. `dist/` is a 5630-line uberscript with no generation task; its core namespace matches src today. `hm.py`, `supervisor.py` and the Python tests are still in the repo. **W**
- messenger-clj is not in the CriomOS-home flake; it was installed imperatively. The old Rust `message-daemon` 0.12.0 is still active as a user unit. **W**
- `field-luna-heartbeat.service` is masked (a /dev/null symlink made 13:13). The CriomOS-home module runs `tools/field-luna-heartbeat.mjs` from the `prompt-relay-source` pin 9d144e3. Primary commit fabbba0d "Read Field Luna heartbeat state from typed HM" is source-ready but not pinned. **W**

**Tasks.**
- **M1. Read the sender's aspect and model from the registry, keyed by pane.** Add `:route/aspect` (psyche|mind|field) and `:route/model` enums to the typed_store schema. Fill them at `register`, from the launcher receipt or Flow. At send time, resolve the caller from its Herdr pane (for example `HERDR_PANE_ID` or a Herdr query) instead of trusting `FLOW_ID`. Refuse the send if the pane is unregistered. Verify: a test with a fake pane shows that a spoofed `FLOW_ID` is rejected.
- **M2. Emit the three-tag envelope once it is ruled.** The living's shape is still open. The candidate is `#msg #psyche #fable ["38de5b" "text"]` (f5a74e §Message tag chains). Fable rules first, then implement `data_readers` and the round-trip test. Keep `#msg [id text]` readable during the transition. Verify: an EDN round trip, and one line under the cap.
- **M3. Maximize the pane message before overflow.** Following "maximize the message", the overflow line should carry as much of the body as fits under 800 characters (collapsed, cut at a word boundary) plus the path, not only a pointer. Either commit the overflow file itself or write it outside the tracked tree. Verify: a 2 KB body gives an 800-character pane line that starts with the body text, and `jj st` in primary stays clean.
- **M4. Keep one Malli schema set.** Move the schemas into `messenger-clj.schema`. Make core and typed_store both require it. Reconcile `:state` (optional or required) and use the FlowId regex everywhere. Verify: the legacy import and all tests still pass, and a grep finds each schema defined only once.
- **M5. Add a ledger lookup.** Add `messenger-clj attempt <id-prefix>` (and optionally `attempts <flow>`) that reads DatalevinLedger and prints the grade, reason, binding and time. Name it in the Uncertain message. Verify: after a fake send, `attempt` returns the recorded row.
- **M6. Make the build honest.** Generate `dist/` in the Nix build (`bb uberscript`), or add a check that regenerates it and compares. Put the Clojure tests into `checks` (or leave that to clj-build, X1). Remove `hm.py`, `supervisor.py` and the Python tests now that the cutover is done. Verify: `nix flake check` runs the Clojure tests.
- **M7. Declare the messenger in Home.** Add messenger-clj as a CriomOS-home input and package in place of the imperative libexec install. Coordinate with 5f38bc and 504461, who hold the consumer boundary. Decide whether to retire the Rust `message-daemon` (ask the living). Verify: after activation, `readlink -f $(which hm-send)` points into the Home generation.
- **M8. Unmask the heartbeat declaratively.** Repin `prompt-relay-source` in CriomOS-home to include fabbba0d. Activate, remove the manual /dev/null mask, and witness one timer run reading typed HM state. Blocked by Home activation (F4).

## 4. field-clj

**The living's words.**
- "Why don't you just make a cool [Clojure] tool called Field … You were just doing 'make a change and then JJ commit' in one go. You could make a cool [Clojure] call that takes a simple EDN input." (2026-09-25, messaging.md)
- "compile it for deployment … use the power of Nix … reuse your libraries for how you package your nexuses. Create some Nix libraries with Fable." (2026-09-25, messaging.md)

**What exists.**
- Canonical main is 212cf38 "Allow unrelated dirty paths in scoped commits"; before it is 1997f64. The form is `field-clj 'commit ["msg" ["path"]]'`. It validates with Malli, requires each named path to be dirty, commits exactly those, checks `jj diff -r @- --name-only`, pushes main and runs `git ls-remote`. **W**
- The path rule drifted from its brief. flows/00f95a/launches/field-clj-brief.md step 2 says "Refuse if any other path is present"; 212cf38 relaxed that to "Unrelated dirty paths do not block". In shared primary only the relaxed rule is usable. The living has not ruled on it. **W**
- The package is a wrapper that runs `clojure -Sdeps '{…malli 0.18.0…}'` at run time, so it resolves Maven at first run and is not hermetic. The flake check runs `clojure -M:test` inside the sandbox, which likely fails without network (not built here). **W** (source)
- It is pinned in CriomOS-home main (flake.nix:64, profiles/med/cli-tools.nix:51, lock 212cf38) but not on PATH (`which field-clj` finds nothing). Activation is blocked by the builder. **W**

**Tasks.**
- **D1. Ratify the path rule.** Rule: exactly the named paths, other dirty paths allowed, and a refusal when a named path is clean or when `@-` differs from the named set. Update the brief, the README and the file-editing or compensation skill source. Add tests for a clean named path and for an `@-` mismatch.
- **D2. Package hermetically.** Pre-fetch the deps (clj-nix / deps-lock, or a `bb` uberscript as messenger-clj does). Make the check run offline. Verify: `nix build` and `nix flake check` pass with `--option substituters ''` and no network.
- **D3. Activate and witness.** After F4, activate CriomOS-home and run `field-clj 'commit …'` on a scratch repo. Witness the success EDN and the remote revision.

## 5. Cross-cutting

- **X1. Build clj-build, a shared Nix library.** The living's words: "Create some Nix libraries with Fable." Neither the repo nor the library exists; only `rust-build` does. Build `mkCljCli`, `mkCljUberjar` and `mkCljChecks` (shape in specialties-distillation.md §Nix library). Move messenger-clj and field-clj onto it. flow-clj is its third consumer. Verify: both tools build from the library with their tests as checks.
- **X2. Specialized flows.** The living's words: "Every variant of the aspect has its own variants of specialized roles in that aspect." (flowAspect.md). There is no code yet. After F6 and the living's acceptance, add StartSpecialized to signal-flow and flow-clj. The first specialty is Monitor, triggered by a final response or a message, never by polling. Luna at light effort.
- **Notions, not tasks:** a single datom call tool with a unified namespace (notion/message.md); Flow-started subflows with their own system prompt (notion/stack.md); the V2 test network (notion/v2.md).

## Sources

- flows/e51411/vision/{messaging,launch,nexus,flowAspect,stack}.md; flows/e51411/notion/{message,stack,v2}.md; flows/e51411/log.md
- flows/38de5b/reports/specialties-distillation.md, update-2026-09-25.md; flows/38de5b/log.md (lines 22-122)
- flows/f5a74e/reports/clojure-flow-input.md; flows/504461/log.md; flows/00f95a/launches/field-clj-brief.md; flows/00f95a/messages/2026-09-25T20-29-00-222906592Z-504461-*.md
- Vision/flowNexus.md, Vision/messaging.md
- /git/github.com/LiGoldragon/flow (origin/main 812053c; Cargo.toml:17; crates/flow/src/main.rs; crates/flow-nexus/src/{store.rs:370-395,lib.rs:470-485})
- /git/github.com/LiGoldragon/signal-flow (origin/main 968ae3b; ab70332 on flow/system-prompt-bundle-00f95a)
- /git/github.com/LiGoldragon/messenger-clj origin/main d4f2d08 (src/messenger_clj/{core,typed_store,main}.clj, flake.nix, check.nix, dist/)
- /git/github.com/LiGoldragon/field-clj origin/main 212cf38 (README.md, flake.nix, src/field_clj/core.clj)
- /git/github.com/LiGoldragon/CriomOS-home origin/main (flake.nix:20,63-65; modules/home/profiles/min/field-luna-heartbeat.nix; profiles/med/cli-tools.nix:51)
- Live on ouranos: `systemctl --user status flow-nexus`, `flow --version`, `readlink -f ~/.nix-profile/bin/flow`, `which hm-send`/`field-clj`, `systemctl --user cat field-luna-heartbeat.service`, `message-daemon.service`, `ssh prometheus true`
