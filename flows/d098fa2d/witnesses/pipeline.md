Subject: Exact current Lojix host deployment pipeline.

Method: code read /git/github.com/LiGoldragon/Curriculum/skills/lojix.md

The owner-only operation is `meta-lojix Deploy.Host`. Its positional fields are cluster, node, host composition, proposal source, flake reference, transport, input mode, output selector, activation backend, host action, source revision policy, optional builder, and extra substituters. `CompleteHost` uses the root transport pair; `Horizon` materializes projection inputs. `RequireImmutable` requires an exact source revision. `DeployAccepted` is admission only; ordinary `Query.ByDeployment` or `Query.ByEventLog` must continue until a terminal record.

Method: code read /git/github.com/LiGoldragon/lojix/src/schema_runtime.rs

The durable pipeline resolves flake auth, optionally materializes Horizon, evaluates, realizes/builds, copies the closure to the explicit transport, activates according to the selected host action/backend, and records the generation. The copy uses `nix copy --substitute-on-destination --to <request nix_store_uri>`. `NixosSystemdBootV1` host activation maps `SetBootProfile` to boot, `ActivateNow` to live switch, `TestActivation` to test, and `ScheduleBootOnce` to a target-owned transient boot-once unit.

Method: code read /git/github.com/LiGoldragon/lojix/tests/build_smoke.rs

The current parser witness uses the shape `Deploy.Host.(fixture-cluster fixture-node BaseHost /dev/null github:fixture-owner/fixture-flake (ssh-ng://fixture-copy.invalid fixture-login@fixture-activate.invalid) Direct (checks.fixture-a) NixosSystemdBootV1 ActivateNow ResolveAndRecord None [])`, confirming parentheses and positional order without supplying a production Zeus request.
