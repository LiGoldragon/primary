<!-- to-the-living:start -->
Presentation.{ «Flow's Tests» }

# Flow's Tests

## psyche-context › spirit/core.md

````markdown
The purpose of a thinking machine is to extend a psyche.

A well-behaving machine is well aligned with the psyche of which it is an extension.

Beauty is the symptom of good engineering or good art or work well done.

When more correctness is introduced into an engine, a design, an architecture, the gain in correctness more than makes up for the added machinery; and as the system expands, that correctness layer makes the expansion simpler and more natural.

Start with the smallest shape that works. Add machinery only where the
requested behavior needs it.

Backward compatibility is never a design variable. Do not preserve an older shape for compatibility's sake; if the current system is not designed to do what we want, it is replaced — every consumer updated — never extended with a parallel compatibility path.

The build target is the design than which none better is possible, the terminal best the work aims at rather than a good-enough or merely best-so-far shape. This is the destination the design values serve.

A machine does not misbehave. Its output is a function of its context and prompt — when an output looks wrong, determine the lacking or incorrect context which produced it.

Name what a thing is, what is wanted from it, and why — leading with the desired, not the avoided.

A module named kind:name reads as its kind before the colon and its name after it: vision:book is the module book, of the kind vision.

Target the best end-shape, not the historically practical compromise.

Never pretend to know what you don't know; admit you don't know.

Keep observations, hypotheses, and unknowns separate. Keep unknown causes unknown.

Seek disconfirming evidence. Do not seed audits with suspected conclusions.

Weigh evidence by origin, not repetition.
````

### Proposal 1: psyche-context › spirit/core.md

**Comment** 433 tests passed while both of today's real failures went through untouched. The fakes stood in for the tools and agreed with the code, not with the tools.

```
+--------------------------------------------+
| 433 tests passing                          |
+--------------------------------------------+
        | run against
        v
+--------------------------------------------+
| scripted fakes of Herdr, Claude, Codex     |
+--------------------------------------------+
        | stand in for
        v
+--------------------------------------------+
| real Herdr, Claude, Codex                  |
+--------------------------------------------+
   | broke live in              | witnessed by
   v                            v
+-------------------+   +--------------------+
| 2 failures,       |   | 6 ignored tests,   |
| all tests passed  |   | never run          |
+-------------------+   +--------------------+
```

  Weigh evidence by origin, not repetition.
+
+ Evidence that a thing works is its behaviour witnessed on the live system; a count of passing tests is not evidence, and a test that restates its own fake or the code it checks witnesses nothing.
+
+ A fake carries the real tool's recorded behaviour, or it is not used.

Ruling: land, amend, or reject.

### Proposal 2: flow › flake.nix

**Comment** The 151 `exactTest` checks re-run tests that `default` (`cargoTest --workspace`) already runs; two run one test under two names. With none left the helper and its export go too. `…` stands for the lines of the block not shown: 22 in the helper, 302 in the entries (lines 194-495).

```nix
-   exactTest =
-     package: testName:
-     craneLib.mkCargoDerivation (
-       …
-     );
    in
    {
      inherit
        pkgs
        toolchain
        craneLib
        commonArgs
        cargoArtifacts
-       exactTest
        lawSource
        ;
```

```nix
        clippy = context.craneLib.cargoClippy (
          …
        );
-       flow-v5-flow-row-upgrades-to-derived-origin
-         = context.exactTest "flow-nexus" "…";
-       … (150 more)
      }
```

Ruling: land, amend, or reject.

### Proposal 3: flow › crates/flow-nexus/src/herdr/launch.rs

**Comment** The Herdr fake, as the real Herdr 0.8.2 behaves. `agent start` returns only once the agent is idle (src/cli/agent.rs:548-610). `pane report-metadata` prints nothing on success (src/cli.rs:748-760). Open: the fake agent turns idle when its TUI attaches; the marker file written there is the amend point.

```rust
  *"agent start"*) …;
+   until [ -f '{agent_idle}' ]; do
+     sleep 0.05;
+   done;
    printf '%s\n' '{{"result":{{"agent":…}}}}' ;;
  *"pane report-metadata w7:p1 "*) …;
-   printf '%s\n' '{{"result":{{}}}}' ;;
+   ;;
```

Ruling: land, amend, or reject.

### Proposal 4: flow › crates/flow-nexus/src/herdr/launch.rs

**Comment** Flow parsed the empty reply of `report-metadata` as JSON, which is what refused the pane label live. `run_status` already exists beside `run_json` and reads success from the exit status alone. Both calls change (lines 1556 and 1608).

```rust
-       self.run_json(&[
+       self.run_status(&[
            "--session".into(),
            pane.herdr_session_name.clone(),
            "pane".into(),
            "report-metadata".into(),
```

Ruling: land, amend, or reject.

### Proposal 5: flow › crates/flow-nexus/src

**Comment** Removed whole, each with its `#[test]`: the two tests that assert the broken Codex order (their flake checks went with Proposal 2), and the tautological ones, which restate a fake, a constant or the code they call.

```rust
- codex.rs:2389
-   a_codex_thread_is_opened_lean_and_given_its_first_turn_before_attach
- herdr/launch.rs:3826
-   a_codex_first_turn_given_before_the_tui_attached_is_observed
- codex.rs:2303
-   fake_proxy_names_the_bound_thread_and_reads_the_name_back
- codex.rs:2062
-   adapter_uses_the_configured_wrapper_without_path_resolution
- lib.rs:1877
-   running_nexus_parses_actual_working_interactive_snapshot
- lean.rs:225
-   claude_leave_outs_become_its_flags_environment_and_settings
- lean.rs:263
-   codex_leave_outs_become_its_config_overrides
- main.rs:381
-   version_answers_the_cargo_package_version
```

Ruling: land, amend, or reject.

### Proposal 6: flow › deployment/live-witness.sh, a new file

**Comment** After each deploy, on the host, against real Herdr, Claude and Codex. Open: a script needs a verb that starts a flow and prints its Herdr session, pane and workspace; `Start` is a typed Signal request with no plain command, so `FLOW_WITNESS_START` names whatever verb the living rules.

```sh
+ #!/bin/sh
+ set -eu
+ for harness in claude codex; do
+   set -- $("$FLOW_WITNESS_START" "$harness")
+   session=$1 pane=$2 workspace=$3
+   herdr --session "$session" pane get "$pane"
+   herdr --session "$session" \
+     workspace get "$workspace"
+   herdr --session "$session" \
+     pane read "$pane"
+   "$FLOW_WITNESS_END" "$session" "$pane"
+ done
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
