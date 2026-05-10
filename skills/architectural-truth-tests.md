# Skill — architectural truth tests

*Tests that prove the architecture is followed, not just
that the behavior succeeds. The agent that writes the code
doesn't remember what they wrote yesterday — these tests are
what catches "looks aligned but secretly reimplemented the
component next door."*

---

## What this skill is for

Apply this skill when an architecture constraint says
*"component A uses component B to do C"* and you're writing
tests for C.

Behavior tests prove C succeeds. Architectural-truth tests
prove **B was the path** — not a local shortcut that
produces the same output. Without architectural-truth tests,
an agent (or a future agent without yesterday's memory) can
ship code that satisfies behavior while routing around the
intended component, and no test fires.

The discipline name comes from `reports/operator/69-architectural-truth-tests.md`,
which proposed the rule for the persona-messaging stack. This
skill lifts it to the workspace level because it applies to
every architectural assertion — wire contracts, storage
layers, actor protocols, deploy chains.

---

## The principle

> Write tests that prove the architecture, not only the
> behavior. If a rule says "component A uses component B to
> do C", the tests must make bypassing B fail even when C's
> visible output still succeeds.

> Treat architecture as a contract with **observable
> witnesses**: dependency graph, type identity, actor
> messages, storage table identity, wire format, state
> transitions, negative compile/runtime cases.

> Prefer weird tests over trusting implementation prose.
> Agents can write code that looks aligned while secretly
> reimplementing the component next door. A correct test
> forces the intended path to be the only passing path.

> Every architectural constraint gets at least one witness
> test: one **positive** test proving the intended
> component is used, and one **negative** test proving the
> tempting shortcut fails.

## Constraints first

The `Constraints` section of a component `ARCHITECTURE.md`
is the seed list for these tests. Write each constraint as a
short direct sentence in plain language; then name at least
one test after that sentence.

| Constraint | Test name |
|---|---|
| `mind` CLI accepts exactly one NOTA record | `mind_cli_accepts_exactly_one_nota_record` |
| `mind` CLI sends Signal frames to the daemon | `mind_cli_cannot_reply_without_daemon_signal_frame` |
| queries never send write intents | `query_path_cannot_touch_sema_writer` |
| daemon owns `mind.redb` | `mind_redb_cannot_be_opened_by_cli` |
| contract crates contain no runtime actors | `contract_crate_cannot_spawn_actor_runtime` |

A constraint that does not suggest a witness is not precise
enough yet. Rewrite it until it names the component, the
operation, and the boundary that must not be bypassed.

---

## The shape

```mermaid
flowchart LR
    rule["architecture constraint:<br/>A uses B to do C"]
    witness["observable witness:<br/>something B leaves behind<br/>that a bypass cannot counterfeit"]
    positive["positive test:<br/>C succeeds AND witness present"]
    negative["negative test:<br/>local shortcut compiled-out<br/>or runtime-rejected"]

    rule --> witness
    witness --> positive
    witness --> negative
```

The hardest step is naming the **witness** — the artifact
that B necessarily produces and a bypass necessarily
doesn't. Witnesses are the load-bearing design move; the
tests are mechanical once the witness is named.

---

## Witness catalogue

Witnesses, by category:

| Witness | Catches |
|---|---|
| `cargo metadata` dependency assertions | wrong repo reached across a boundary (e.g. router pulls persona-wezterm directly) |
| `compile-fail` tests (`trybuild` or similar) | local duplicate types, string shortcuts, missing trait contracts |
| Fake actor handles | direct method calls disguised as actor code |
| Typed event traces (recorder actor) | wrong ordering of effects (e.g. push-before-commit) |
| Actor topology manifest | missing actors, collapsed phases, unsupervised children |
| Actor trace pattern | request bypasses a required actor plane |
| Forbidden actor-edge trace | query writes, CLI opens database, domain actor bypasses store actor |
| redb fixture files (golden) | schema/version lies; missing table writes |
| rkyv byte fixtures (golden) | incompatible wire or disk encoding |
| Nix-chained derivations (next §) | runtime memory faking what should be filesystem |
| Process-tree witnesses (`/proc/<pid>/maps`, `lsof`) | claimed-open files that aren't open |
| Length-prefixed-frame parser on the wire | text/JSON snuck into a Signal channel |
| Schema-version golden | undocumented schema drift |
| Legacy-surface absence witness | lock-file / BEADS reinvestment sneaking into new components |
| Network namespace test | hidden cross-machine calls |

---

## Actor trace first, artifacts later

For actor-system ordering constraints, start with the mailbox path.
An actor trace is the first witness: it proves the required actors saw
the message and records the happens-before relation that a direct call
or shortcut would skip.

Do not wait for durable storage to exist before testing an ordering
claim. If the current component has only in-memory state, write the
actor-trace witness now. For example, `router_cannot_emit_delivery_before_commit`
records the matching commit event before any delivery event in the
trace stream; the test fails if delivery appears first.

When the durable substrate lands, add the stronger stateful or
Nix-chained artifact witness on top. The later artifact test proves
the redb/table write happened before delivery across process or
derivation boundaries; it does not replace the actor trace, which
still proves the intended mailbox path was used.

---

## Nix-chained tests — the strongest witness

When a rule says *"this writes to the database"*, the
strongest witness is to **separate the write from the read
across two Nix derivations**. The first derivation runs the
code-under-test and **emits the database file as its
output**. The second derivation **reads the file with the
authoritative reader** and asserts content. Nothing in-process
can fake the chain: if the database wasn't actually
written, the second derivation has nothing to read.

```mermaid
flowchart LR
    src["source under test"] --> derivA
    derivA["derivA — run write code<br/>output: state.redb"] -->|state.redb| derivB
    derivB["derivB — read state.redb<br/>with authoritative reader<br/>assert expected content"] --> result["✓ or ✗"]
```

Why Nix specifically:

- **Pure environment.** No carry-over from the host's home
  directory, no `tmpfs` collusion between writer and reader.
  The writer's output is the *only* path between them.
- **Reproducible.** The chain runs the same way on every
  machine; the chain *is* the test, not a flaky integration
  script.
- **Witness output is content-addressed.** `state.redb`
  becomes a `/nix/store/<hash>-state.redb`; the hash
  changes if any byte of the database changes. Drift
  surfaces as a hash mismatch, not a flaky equality
  comparison in some test runner.
- **Reader can't be the writer's mock.** The reader
  derivation depends only on the file artifact — not on
  the writer's source — so the reader can't be tricked
  into accepting the writer's in-memory state.

Worked sketch in a flake:

```nix
{
  outputs = { self, nixpkgs, crane, fenix, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        # ... toolchain + craneLib ...
      in {
        checks = {
          # Step A: run the write code, output the redb file.
          message-stack-write = pkgs.runCommand "message-stack-write.redb" {
            buildInputs = [ self.packages.${system}.message-cli
                            self.packages.${system}.persona-router-daemon ];
          } ''
            export STATE_DIR=$out
            mkdir -p $STATE_DIR
            persona-router-daemon $STATE_DIR/router.sock &
            ROUTER_PID=$!
            sleep 1
            message designer "stack test message" \
              --socket $STATE_DIR/router.sock
            sleep 1
            kill $ROUTER_PID
            test -f $STATE_DIR/persona.redb
          '';

          # Step B: read the redb file with the authoritative
          # reader; assert the message landed.
          message-stack-read = pkgs.runCommand "message-stack-read" {
            buildInputs = [ self.packages.${system}.persona-sema-reader ];
          } ''
            persona-sema-reader \
              --db ${self.checks.${system}.message-stack-write}/persona.redb \
              --table messages \
              --expect "stack test message"
            touch $out
          '';
        };
      });
}
```

The chain forces:
- The writer **must actually create the file** (or step A
  fails).
- The reader **must actually find the message in the typed
  table** (or step B fails).
- The reader is a **separate binary** that depends only on
  the file artifact (so it can't share the writer's memory).

If the agent who wrote the router shortcuts persona-sema and
keeps state in memory, step A produces an empty file and
step B fails. The test names the failure as
`message-stack-read` failing on the witness file from
`message-stack-write`.

---

## Examples (from the persona messaging stack)

| Constraint | Architectural-truth test |
|---|---|
| Component-owned Sema tables store Signal contract types | Insert and read a Signal contract record through the owning component's typed Sema table; no local duplicate type can satisfy the table's value type. |
| Router commits before delivery | Use a fake store actor + fake harness actor; assert the router emits `CommitMessage` *before* any `DeliverToHarness`. |
| Router does not own terminal bytes | `cargo metadata` test fails if `persona-router/Cargo.toml` depends on `persona-wezterm`. |
| Signal is the component wire | Integration test sends a length-prefixed `signal_core::Frame`; NOTA strings on the component socket are rejected. |
| No private durable queue | Restart router after queued message; message survives only if committed through the router-owned Sema table, not if held in memory. (Nix-chained: writer derivation queues + crashes; reader derivation opens the redb and looks for the message.) |
| Sema schema guard is real | Existing redb file with no schema version hard-fails on `open_with_schema`; fresh file writes the version; mismatched version hard-fails. |
| Guard facts are pushed | Fake system actor sends focus/prompt facts; router retries only on pushed observation, never on a timer. (Witness: `tokio-test`'s clock-pause shows zero retries during paused time.) |
| Prompt guard blocks injection | Nonempty prompt fact → `DeliveryBlocked(PromptOccupied)` and **zero** terminal-input frames. |
| Focus guard blocks injection | Focused target → `DeliveryBlocked(HumanOwnsFocus)` and **zero** terminal-input frames. |
| Actor model is real | Router test communicates through actor handles/mailboxes only; direct method calls aren't part of the public API (compile-fail test against the bypass attempt). |
| Actor density is real | Runtime topology contains the named phase actors from the architecture manifest; a request trace must pass through each required actor in order. |
| Actor handler does not block | Failure-injection actor holds an IO/command/clock plane; domain actor mailbox remains responsive while that plane waits. |
| Actor nouns carry data | Static or compile-time witness rejects public empty actor marker types; adapter ZSTs are private framework glue only. |

---

## Rule of thumb — the test name pattern

If the rule is *"X must go through Y"*, write a test named:

```text
x_cannot_happen_without_y
```

Then ensure `Y` leaves a typed witness that a bypass cannot
counterfeit. The test asserts: do the action, then check
the witness exists.

Examples:

- `message_cannot_persist_without_component_owned_sema`
- `router_cannot_deliver_without_commit`
- `injection_cannot_happen_without_focus_observation`
- `claim_cannot_commit_without_conflict_actor`
- `query_cannot_touch_sema_writer`
- `handler_cannot_block_mailbox`
- `claim_normalizer_cannot_be_empty_marker`

When the body needs to teach structure, put the body on a
fixture method. The `#[test]` wrapper only calls the fixture.

---

## Actor-density tests

When an architecture says a component is actor-based, behavior
tests are not enough. The tests must prove that the expected actor
planes exist and were used.

```mermaid
flowchart LR
    manifest["ActorManifest"] --> runtime["running actor tree"]
    runtime --> dump["topology dump"]
    dump --> topology_test["topology test"]

    request["typed request"] --> trace["ActorTrace"]
    trace --> pattern["required actor sequence"]
    pattern --> trace_test["trace-pattern test"]
```

Use these witnesses:

| Rule | Witness |
|---|---|
| Actor exists | topology dump contains the actor path |
| Actor is supervised | topology dump shows the expected parent |
| Request used actor | trace contains actor received/replied events |
| Query stayed read-only | trace contains read actors and excludes writer actors |
| Mutation used store actor | trace contains writer, event append, and commit actors |
| Handler did not block | while one plane actor waits, sibling request actor still replies |
| No hidden shared lock | static scan rejects `Arc<Mutex<...>>` ownership between actors |
| Actor noun carries qualities | compile-time or static witness rejects public empty actor structs |

The failure mode to catch is "one actor with helper methods." If
the architecture names `ClaimNormalizeActor` and
`ClaimConflictActor`, a single `ClaimActor` with private helper
methods is not equivalent. The topology and trace tests should fail
that implementation.

---

## When to use which witness

| Rule shape | Use |
|---|---|
| "Component A depends on B" | `cargo metadata` test |
| "Type X is the wire form" | rkyv byte fixture or compile-fail on alternative types |
| "Effects happen in order" | typed event trace via recorder actor |
| "State is durable across restarts" | nix-chained writer/reader derivations |
| "Inputs are pushed, not polled" | `tokio-test` clock pause + assert zero work |
| "Schema version is checked" | golden redb fixtures (one matching, one mismatched) |
| "Component A doesn't directly call C" | compile-fail test on the direct call + cargo metadata exclusion |
| "Actor X holds state Y" | snapshot the actor's `State` struct after stimulus |
| "Every logical plane is an actor" | topology manifest + runtime topology dump |
| "Request went through actor X" | ordered actor trace pattern |
| "Actor handler does not block" | responsiveness test with blocked plane actor and live sibling actor |

---

## What this skill is NOT

- **Not a replacement for behavior tests.** Architectural
  witnesses + behavior tests are complementary; you need
  both. A test that proves the architecture but never asserts
  the user-facing outcome misses obvious bugs.
- **Not over-engineering for one-off scripts.** A short
  shell script doesn't need a witness; the witness budget
  is for the parts of the system the architecture rules
  govern.
- **Not silver-bullet anti-fraud.** A determined adversary
  can defeat any test. The witnesses make it *substantially
  harder* to ship architecture-violating code without
  catching it in review.

---

## Companion skills

This pairs with:
- `skills/contract-repo.md` §"Examples-first round-trip
  discipline" — the architectural-truth pattern for wire
  contracts (text + typed + round-trip = three layers of
  witness).
- `skills/rust-discipline.md` §"Tests live in separate
  files" — where the tests go.
- `skills/push-not-pull.md` — the `tokio-test`-clock-pause
  pattern for proving no-polling.
- `skills/nix-discipline.md` §"`nix flake check` is the
  canonical pre-commit runner" — the chained-derivation
  pattern lives in nix.

---

## See also

- `~/primary/reports/operator/69-architectural-truth-tests.md`
  — the originating proposal; the examples table here is
  lifted from there.
- `~/primary/skills/rust-discipline.md` §"Actors" — fake
  actor handles + sync-façade-on-State pattern.
- `~/primary/skills/actor-systems.md` — actor-density,
  blocking-handler, topology, and trace rules.
- `~/primary/repos/lore/rust/testing.md` — `CARGO_BIN_EXE_*`
  for two-process integration tests.
- `~/primary/repos/lore/nix/integration-tests.md` — chained
  derivation patterns.
