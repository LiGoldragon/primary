# Operator review — cloud-designer general VM testing interface

## Scope

Reviewed cloud-designer's `reports/cloud-designer/50-general-vm-testing-interface/` and the three `horizon-test-vm` feature branches:

- `/git/github.com/LiGoldragon/horizon-rs` `horizon-test-vm` at `fe7182f1`
- `/git/github.com/LiGoldragon/CriomOS` `horizon-test-vm` at `724fae1a`
- `/git/github.com/LiGoldragon/CriomOS-test-cluster` `horizon-test-vm` at `f9910de7`

I did not merge branches, check out worktrees, run live deploys, or rerun the full `runNixOSTest` suite. This is a code/report review against branch snapshots plus recent Spirit reads.

## Recent intent read

Spirit lookups that constrain this review:

- `xxgp` — tests should be one concept, named as the invariant they prove, with a PATTERN comment.
- `dqg3` — unblock test blockers inside the test rather than returning with “cannot test”.
- `l50b` — load-bearing intent should become constraint tests.
- `aipc` — no stubs/placeholders dressed as done and no circular golden tests.
- `oh9l` — Lojix cutover is durable-first on sema-engine before cutover.
- `lc28` — substituter resolution moves into the daemon provisionally and must be marked temporary.
- `cncj` / `ggvg` — prior VM-testing node direction remains concrete precedent, not contradiction.

The new cluster-data-generated VM-testing principle is documented in `reports/cloud-designer/50-general-vm-testing-interface/intent-capture.md` but is still pending Spirit capture because Spirit writes are blocked by the store layout migration.

## Verdict

The branch set is strong and mostly operator-ready. The architecture is implemented in the right layer order: Horizon owns the host capability datum, CriomOS consumes the projection without node-name logic, and the test-cluster owns readable `runNixOSTest` checks over generated CriomOS systems. The work honors the main testing intent better than the earlier live `/tmp` harnesses: the substrate constraints are named, versioned, and entered through flake checks.

I would integrate after a short cleanup pass for the findings below. The cleanup is small relative to the delivered work and should happen before merging the feature branches to their mains so the claimed interface is exact.

## What looks right

- `NodeService::VmHost` is in the correct horizon bucket: variable, cluster-authored, not derivable by CriomOS, and sibling to other capability services rather than a node species.
- `KvmAvailability` and `MaximumGuests` are typed domain values, not booleans or loose integers at the Rust boundary.
- The host-viewpoint test in `horizon-rs/lib/tests/horizon.rs` proves the generator-facing surface: the host projection exposes its own `VmHost` service and the hosted guest relation through `ex_nodes`.
- `CriomOS/modules/nixos/test-vm-host.nix` reads the projected service and emits additive tap networking with a low-numbered by-name networkd match, addressing the earlier broad-ether DHCP capture risk.
- `CriomOS/modules/nixos/test-substrate.nix` centralizes the writable-store, `require-sigs=false`, NSS/root-shell, serial, and label fixes that were previously per-run harness knowledge.
- `CriomOS-test-cluster/INTENT.md` is added on the feature branch and clearly states the repo’s job: synthetic projection-to-config proof with no production facts.
- `mkVmTest` is the right abstraction: author supplies `(cluster, hostNode, vmNode, testScript)`, while guest OS, size, role, address, home toggle, acceleration, and capacity are derived from projection data.
- The suite checks are readable and named by behavior: `edge-desktop-boots-greeter`, `base-home-activates`, and `lojix-deploy-smoke`.

## Findings to fix before merge

### 1. `TapSubnet` accepts IPv6 and too-small CIDRs, while Nix slicing assumes IPv4 host addresses

`horizon-rs/lib/src/address.rs` defines `TapSubnet(IpNet)`, but both `CriomOS/modules/nixos/test-vm-host.nix` and `CriomOS-test-cluster/lib/mkVmTest.nix` split the subnet base on `.` and construct dotted-decimal addresses. An IPv6 `TapSubnet`, or an IPv4 subnet too small for the hosted guest count, passes the Rust type and fails later as confusing Nix behavior or silently slices outside the declared network.

Recommended fix: make `TapSubnet` an IPv4-only domain value, or add Rust validation that rejects non-IPv4 and maybe exposes capacity helpers. At minimum, the Nix generator should assert `guestSubnet` is dotted IPv4 and has enough host slots for `maximumGuests` or the hosted set.

### 2. `mkDeployTest` accepts `hostNode` but does not use it

`CriomOS-test-cluster/lib/mkDeployTest.nix` has `{ cluster, hostNode, vmNode }`, but the reviewed code never reads `hostNode`, never checks the host projection, and never asserts that `vmNode` is hosted by that `VmHost`. That weakens the “cluster data from the VM host and VM-node config” claim specifically for C6.

Recommended fix: either use `hostNode` the same way `mkVmTest` does for model assertions, or remove it from `mkDeployTest` and describe C6 honestly as a deploy-path smoke over a projected target node rather than a host-derived VM-host test. I prefer using it, because the smoke then fails if the target is no longer a Pod on the declared VmHost.

### 3. The deploy smoke reads durable Lojix state but does not assert it

`mkDeployTest.nix` calls the ordinary `lojix Query (ByNode ...)` and prints `final_query`, but it does not assert that the durable record contains the deployed terminal state, node, or closure. The target profile assertion is strong and proves the deploy effect, but the report claim says the daemon’s durable deploy-job record corroborates it. Currently that corroboration is observational only.

Recommended fix: assert a stable part of the generated `Query` reply, preferably a schema-owned status/path shape rather than just a substring. If the text surface is all the test has, assert at least the node and terminal deployed state.

### 4. `test-substrate.nix` comments drifted after the runNixOSTest machine-type finding

The top comment still says the generator composes both `guestModule` and `vmTypeModule`; `mkVmTest` intentionally imports only `guestModule` after discovering that bare `-M microvm` cannot compose with the `runNixOSTest` PCI driver backdoor. The code is sensible; the durable comment should match it so future operators do not reintroduce the broken machine-type override.

Recommended fix: update `test-substrate.nix` prose to say `vmTypeModule` is for live/standalone or future UEFI paths, while `mkVmTest` uses the qemu-vm runner machine type and only applies the guest prebakes.

## Integration guidance

- Merge order should be `horizon-rs` → `CriomOS` → `CriomOS-test-cluster`, because downstream flake pins reference upstream feature branches.
- Keep the feature branch shape; do not flatten it into unrelated Lojix cutover work.
- Before pushing mains, run the branch’s claimed Nix witnesses from a clean checkout/worktree. At minimum: horizon tests/clippy, CriomOS eval checks, and the x86_64 `CriomOS-test-cluster` checks including the three `runNixOSTest` checks if builder capacity permits.
- After merge, capture the pending VM-testing principle in Spirit once the store migration is done; until then `intent-capture.md` is the durable blocker note.
