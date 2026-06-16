# Operator Implementation Handoff — cluster-data-generated VM-testing system

Audience: cloud-operator (CO). This is the single operator-actionable handoff to **merge the built `horizon-test-vm` feature branches AND implement the remaining (gated/dependent) work**: Unit 3 (scoped image-exchange emission), the live path (turning `LiveNotYetEnabled` into the real host-untouched cycle), the Prometheus wiring (goldragon `VmHost` data edit + test-VM nodes + `TestDefaults` config), and the multi-host Test-validation activation.

All shas, file paths, line numbers, flake pins, and commands below were verified against the actual repos under `/git/github.com/LiGoldragon/` and worktrees under `/home/li/wt/github.com/LiGoldragon/` as of 2026-06-16. Where a claim was empirically pinned (e.g. projecting real `goldragon/datom.nota` through a freshly-built `horizon-cli`), it is flagged VERIFIED.

## 1. Overview — what this system is, and the vision

The cluster-data-generated VM-testing system makes **declaring a node in cluster data equivalent to getting a test of that node**, dispatched through the lojix daemon to a durable verdict. The pieces (C1–C6 in report 50):

- **C1 — the host role.** A cluster node can declare `NodeService::VmHost` (in horizon cluster data), making it a host that runs on-demand test VMs. The projection emits the host's tap subnet, KVM availability, and a guest ceiling.
- **C2 — the host substrate.** CriomOS `test-vm-host.nix` reads the projected `VmHost` data and stands up the microVM host plumbing (additive tap, networkd match, `microvm.vms`) only when the host actually hosts guests and KVM is available.
- **C3 — the guest substrate.** CriomOS `test-substrate.nix` is the named lean test-guest profile (writable store, `require-sigs=false`, NSS, serial, label) — the substrate both the hermetic check and the live guest boot.
- **C4/C5 — the generators + suite.** `mkVmTest`/`mkDeployTest` generate per-node checks; the §1 **auto-pickup suite** generates one `vm-<node>` check per declared hosted node (declaring a node IS getting a test), with a standard role-derived fallback unless the node is in `customTests`.
- **C6 — the deploy smoke.** `lojix-deploy-smoke` runs the real production deploy path under a hermetic 2-node `runNixOSTest` — proven GREEN.
- **The lojix Test op (Units 2a+2b).** The lojix triad gained a `Test` operation: `(Check mercury)` nix-builds the node's hermetic check and writes a durable `Passed`/`Failed`, queryable via `(ByTestRun …)`, dispatched through a decoupled `TestJobs` actor that survives client disconnect. LIVE is honestly rejected at submit with `LiveNotYetEnabled` (no faked pass).
- **Unit 1 — multi-host.** A node can be hosted on a **set** of hosts (`super_node` ∪ `super_nodes`); the projection emits the **scoped** `image_exchange_pub_keys` = the signing keys of exactly that host-set, so only the declared co-hosts can `nix-copy` the guest image between each other.
- **Unit 3 — scoped emission (remaining).** CriomOS emits those scoped keys as `extra-trusted-public-keys` from the node's host-set.
- **The live path (remaining, gated).** On-demand hosting on **Prometheus**: a host-untouched user-namespace bring-up → real deploy into the guest → real assert → teardown, behind explicit psyche authorization, never touching the live router's system config (the gemma hazard).

The end-state vision: a psyche declares a `TestVm` node (and optionally a multi-host set) in cluster data; the auto-pickup suite gives it a hermetic check for free; `lojix (Test (Check <node>))` runs it to a durable verdict through the daemon; and for nodes that need a real machine, the live path brings the VM up on a real `VmHost` (Prometheus), deploys the production closure into it, asserts it booted, and tears it down — host byte-identical before and after.

## 2. Current state (verified per-repo)

### 2.1 Per-repo state table

All SHAs verified via `git ls-remote` / `git -C … rev-parse` against the actual remotes (2026-06-16). The lojix triad is already on its mains; the three `horizon-test-vm` branches are unmerged and operator-ready (387 cleanup already applied — see §3.4).

| Repo | Branch | SHA (remote) | What it carries | Main SHA |
|---|---|---|---|---|
| **horizon-rs** | `origin/horizon-test-vm` | `214e6816` | C1 `NodeService::VmHost` role + `VmHostCapability` (`proposal.rs:128,188`); `TestVm` species; Unit 1 multi-host: `Machine.super_nodes` + `host_set()` (`machine.rs:66,77`), SCOPED `image_exchange_pub_keys` projection (`node.rs:136,558-592`), host-set-existence + `validate_host_set_single_arch` invariants (`node.rs:678`, `horizon.rs:59`). 4 commits over main; +1095 lines; 135/135 tests | `9fae4a36` — **UNTOUCHED** (zero hits for `super_nodes`/`VmHostCapability`/`image_exchange_pub_keys`) |
| **CriomOS** | `origin/horizon-test-vm` | `42bc62b3` | `modules/nixos/test-vm-host.nix` (reads projected VmHost, additive tap, low-numbered networkd match), `test-substrate.nix` (writable-store / `require-sigs=false` / NSS / serial / label substrate + `guestModule`/`vmTypeModule`), `test-vm-guest.nix`, `vm-testing/default.nix` (VmTesting feature, `gpuPassthrough=false`), `checks/vm-testing-prometheus-policy/`; the **05- tap .network prefix fix** (`084b00d` — claim guest tap before broad 10-main-eth DHCP); the **lean-guest gates** (`56ee372` — docs forced off for any test guest, `includeHome` alone decides home). 6 commits; +2055/-880 | `856c79d7` |
| **CriomOS-test-cluster** | `origin/horizon-test-vm` | `46febf36` | `lib/mkVmTest.nix`, `lib/mkDeployTest.nix`, `lib/standardTest.nix` (role-derived fallback), `lib/deploy-flake.nix`; the **§1 auto-pickup suite** in `flake.nix` (one `vm-<node>` check per declared hosted node, standard fallback unless in `customTests`); `clusters/fieldlab.nota` (atlas declares `VmHost [169.254.100.0/22] Available (Some 4)`; mercury + base-home are `TestVm`; edge-desktop is `Edge`); fixtures (atlas/mercury/edge-desktop/base-home/dune JSON). The **C6 lojix-deploy smoke RUNS GREEN** (`f9910de`). 6 commits; +7639/-323 | `4621bdd3` |
| **signal-lojix** | **main** | `cc8bbf32` | Unit 2a shared types: `TestRunIdentifier`, `TestMode [Hermetic Live]`, `HostSelection`, durable `TestRunRecord` + `TestRunListing`, the `(ByTestRun TestRunLookup)` Selection arm + `TestRunsQueried` reply. Schema regenerated, contract tests green | (this IS main) |
| **meta-signal-lojix** | **main** | `1dbecc08` | Unit 2a: `Test` added to operation root `(Deploy Pin Unpin Retire Test)` with `Tested`/`TestRejected`; `TestRequest [(Run TestRun) (Check QuickCheck)]`; `AcceptedTest`; `TestRejectionReason`. Unit 2b fix: `TestRejectionReason::LiveNotYetEnabled`. Schema regenerated, tests green | (this IS main) |
| **lojix** | **main** | `538fdebf` | Unit 2b: REAL hermetic Test-op dispatch. `TestJobs` actor (`daemon.rs:714`, decoupled — survives client disconnect); `(Check mercury)` nix-builds `#checks.x86_64-linux.vm-mercury` → durable `Passed`/`Failed(HermeticCheck)` with real out-path; `(ByTestRun)` query; LIVE rejected `LiveNotYetEnabled` at submit (`schema_runtime.rs:1599`); host-set validation. The live `BringUpTestVm`/`TearDownTestVm` effects + invocations are **BUILT but not run** (`schema_runtime.rs:2894-2926` construct the ssh/systemd-run/unshare/nsenter invocation via `_invocation`, return the gated result without `.run().await`). 2 commits (`bf487a0` stub + `538fdebf` real). `tests/test_op.rs` proves it 3 ways (in-process, real-daemon-socket, both `#[ignore]`'d as they hit the network) | (this IS main) |

### 2.2 Authoritative branch tips (integrate from `origin`, not the local ref)

The worktrees under `~/wt/github.com/LiGoldragon/<repo>/horizon-test-vm/` are `jj` working copies whose `@` commits are byte-identical to `origin/horizon-test-vm` (verified `jj diff --from <tip> --to @` = 0 files for all three). The pushed `origin/horizon-test-vm` tip is authoritative. **The *local* `horizon-test-vm` ref in the `/git/...` checkouts is STALE** (horizon-rs local = `12da6238`, an old pre-VM-testing commit) — **integrate from `origin/horizon-test-vm`, never the local ref.**

| Repo | `origin/horizon-test-vm` (merge this) | `origin/main` | commits ahead |
|---|---|---|---|
| `horizon-rs` | `214e6816` | `9fae4a36` | 4 |
| `CriomOS` | `42bc62b3` | `856c79d7` | 6 |
| `CriomOS-test-cluster` | `46febf36` | `4621bdd3` | 6 |

The lojix triad is ALREADY on main (no merge needed): `lojix 538fdebf`, `signal-lojix cc8bbf32`, `meta-signal-lojix 1dbecc08` — all three verified as ancestors of their `origin/main`.

### 2.3 Reports map (where the deep detail lives)

- **47** (`47-horizon-test-vm-design/`) — original design: the horizon test-VM model, captured psyche intent (durable on-demand VMs, not throwaways), the horizon model / CriomOS derivation / host-lifecycle decomposition. `4-design-proposal.md`.
- **48** (`48-lojix-microvm-live-e2e/`) — the proven host-untouched microVM live e2e: `1-execution-log.md`, `2-synthesis-and-findings.md`. The empirical source for the live-path wiring and its caveats (ssh-config alias, `<drv>^*` bug, single-vs-two-unit shape).
- **49** (`49-lojix-uefi-activation-e2e/`) — the proven UEFI `FullOs` + `BootOnce` activation e2e: `2-synthesis.md`. Userspace-stall caveat for the assert.
- **50** (`50-general-vm-testing-interface/`) — THE general cluster-data-generated VM-testing interface (C1–C6). `4-design-proposal.md` (full proposal); `1-psyche-decisions.md` (resolutions + the 387 cleanup re-review PASS note); `intent-capture.md` (the pending-Spirit principle).
- **51** (`51-prometheus-live-vm-host/`) — Prometheus as the LIVE on-demand VM host; the host-untouched user-namespace bring-up (§3); the gemma finding (never deploy `VmHost` to the live router). `0-frame.md`, `4-plan.md`.
- **52** (`52-lojix-and-vm-testing-synthesis.md`) — cross-session synthesis (single file).
- **53** (`53-vmtest-autopickup-and-client/`) — §1 auto-pickup suite (declaring a node IS getting a test) + the NOTA-CLI client. `4-proposal.md`. DONE.
- **54** (`54-lojix-test-op/`) — the lojix Test op + multi-host model. `1-decisions.md` carries the A–E decisions, the Unit 1/2/3 implementation order, and the **Progress (2026-06-16)** section (the authoritative remaining-work map). `4-proposal.md` is the full proposal.
- **387** (`reports/cloud-operator/387-cloud-designer-vm-testing-review.md`) — operator review. NOTE: reviewed an EARLIER branch snapshot (horizon-rs `fe7182f1`, CriomOS `724fae1a`, test-cluster `f9910de7`); 4 findings raised — **all now fixed on the branch HEADs** (§3.4).
- **43** (`43-routed-microvm-standup/5-risk-history.md:21-45`) — the binding `5hir5bnz`/`kx32`/`xv9v`/`1lex` router-safety constraint text (the gemma hazard).

## 3. Integration plan (step by step)

### 3.1 Merge ORDER and WHY: `horizon-rs` → `CriomOS` → `CriomOS-test-cluster`

Mandated by report 387 §"Integration guidance" and the flake-pin dependency direction. **Integrate as a set** — test-cluster `89f93ba` explicitly re-locks `horizon 8fb25be9 / criomos 42bc62b3` in `flake.lock`, and fieldlab fixtures depend on the horizon `VmHost` projection + CriomOS emission.

1. **`horizon-rs` first.** The model root — `NodeService::VmHost`, `Machine.{disk_gb,location,super_nodes}`, `host_set()`, the scoped `image_exchange_pub_keys` projection, the extended C1 host-set-existence + single-arch invariants. The 4 commits on top of main:
   - `59862dd` (TestVm species + `disk_gb`/`location` + golden test)
   - `44415db` (= content of `fe7182f1`: C1 `NodeService::VmHost` + Pod super-node invariant)
   - `8fb25be` (operator cleanup finding 1: `TapSubnet` IPv4-only + capacity helpers)
   - `214e6816` (Unit 1 multi-host `super_nodes` + scoped image-exchange keys)
   
   Self-contained — **no cross-repo flake pin to bump.**

2. **`CriomOS` second.** Reads the projected `VmHost` data (C2 `test-vm-host.nix`) and ships the named C3 `test-substrate.nix` profile. **Key fact: CriomOS does NOT pin horizon-rs** — it stubs horizon via `horizon.url = "path:./stubs/no-horizon"` (`flake.nix:69`). So **no horizon pin to bump in CriomOS**; the horizon→CriomOS coupling is exercised only at the test-cluster layer. The 6 commits: `c193127`, `9543da2`, `28ad489`, `084b00d`, `56ee372`, plus `42bc62b3` (cleanup finding 4: test-substrate prose corrected).

3. **`CriomOS-test-cluster` last.** The only repo whose `flake.lock` pins the upstreams (`horizon`, `criomos`, `lojix`) — its `runNixOSTest`/projection checks consume both upstream branches through those pins. The 6 commits: `9f74700`, `3add32a`, `b454a1c`, `f9910de` (C6 smoke), `89f93ba` (cleanup findings 1-3), `46febf3` (auto-pickup suite, report 53 §1).

### 3.2 Cross-repo FLAKE PINS to bump as each lands

Only **CriomOS-test-cluster** carries cross-repo pins. Its declared inputs (`flake.nix:7,18,28`) point at branches:
- `horizon.url = github:LiGoldragon/horizon-rs/horizon-test-vm`
- `criomos.url = github:LiGoldragon/CriomOS/horizon-test-vm`
- `lojix.url   = github:LiGoldragon/lojix/main`

Its current `flake.lock` (on the branch) pins:
- `horizon` (node `horizon_2`) → **`8fb25be9`** (the cleanup-finding-1 commit, NOT the branch tip `214e6816`)
- `criomos` → **`42bc62b3`** (= CriomOS branch tip; correct)
- `lojix` → **`9d4eae3b`** on `main` (NOT current lojix main `538fdebf`)

**Two stale pins the operator must handle when landing test-cluster:**

1. **`horizon` is pinned at `8fb25be9`, BEHIND the horizon branch tip `214e6816` by exactly one commit** — the Unit 1 multi-host work (`super_nodes` + `host_set` + scoped `image_exchange_pub_keys` + host-set/single-arch invariants) is NOT in the locked rev. The cleanup commit `89f93ba` deliberately re-locked horizon to `8fb25be9`. After merging horizon-rs to main, change `horizon.url` to `github:LiGoldragon/horizon-rs/main` (or the new main SHA) and run `nix flake lock --update-input horizon` so the test-cluster builds against the merged horizon main carrying Unit 1. Single-host fixtures project byte-identically (verified: branch `fieldlab.nota` Pod records omit the `super_nodes` tail and the horizon golden tests pass 135/135), so re-locking to the merged main is non-breaking for existing checks.

2. **`lojix` is pinned at `9d4eae3b`, behind lojix main `538fdebf` by 2 commits** (`bf487a0` Test op 2a, `538fdeb` Test op 2b). The C6 smoke (`mkDeployTest.nix`) uses only lojix's `Deploy` op + ordinary `Query` (verified — it does not call the Test op), so `9d4eae3b` is functionally sufficient for the smoke. But re-locking `lojix.url` to current `main`/`538fdebf` is correct and harmless, and keeps the deployed FIXED lojix daemon current.

After repointing both `url`s to `main`, run `nix flake lock` once in the test-cluster checkout to regenerate `flake.lock` against the merged mains, then run the gates in §3.3.

### 3.3 Per-repo GATES (run from a clean checkout/worktree before pushing each main)

Report 387 §"Integration guidance": "run the branch's claimed Nix witnesses from a clean checkout before pushing mains."

- **horizon-rs.** Rust gates: `cargo build`, `cargo test` (branch claims 135/135; the flake check is `cargoTest`, `flake.nix:56-59` — `nix build .#checks.<system>.default` runs the suite), `cargo clippy`. The golden test in `lib/tests/horizon.rs` exercises the host-viewpoint projection + the multi-host `super_nodes` path (fixtures at lines 38, 448, 646-651). The invariant to confirm stays green: single-host byte-identical projection (`project_single_host_node_is_unchanged_by_empty_super_nodes`).
- **CriomOS.** Eval checks via `nix flake check` (x86_64). Relevant policy checks: `vm-testing-prometheus-policy`, `nspawn-role-policy`, `metal-firmware-policy`, `router-wifi-horizon-policy`, plus the standard set (`flake.nix:99-117`). These are static-eval, cheap.
- **CriomOS-test-cluster.** `nix flake check` including the heavier `runNixOSTest` checks. The auto-pickup suite generates one `vm-<node>` check per declared Pod-on-atlas (`flake.nix:201`, `genAttrs`): **`vm-base-home`** (custom home anchor), **`vm-dune`** (standard Edge fallback — the net-new green check report 53 §1.1 highlights), **`vm-edge-desktop`** (custom desktop anchor), **`vm-mercury`** (standard lean TestVm fallback). Plus explicit checks: **`lojix-deploy-smoke`** (C6, claimed GREEN at `f9910de`), **`projections-match-fieldlab`** (`flake.nix:206` — re-projects `fixtures/horizon/*.json` from `clusters/fieldlab.nota` via `horizon-cli --cluster fieldlab` and `cmp`s; **fails if the horizon pin's projection output drifts from committed fixtures**), `pod-missing-super-node-rejected`, `spirit-nspawn-can-build`, and `source-constraints` (see §3.5 caveat 2). The four `runNixOSTest` VM checks + the smoke are builder-capacity-heavy; report 387 says run them "if builder capacity permits."

**Critical gate interaction:** after re-locking horizon to merged-main, **re-run `projections-match-fieldlab`** — if the new horizon's projection emits any field the committed `fixtures/horizon/*.json` lack (e.g. a new `imageExchangePubKeys` array, or `superNodes`), this check fails and the fixtures must be regenerated with `horizon-cli` from the new horizon. Confirm the fixtures already carry the Unit-1 output before pushing. (Note: `imageExchangePubKeys` is `#[serde(skip_serializing_if = "Option::is_none")]` and `superNodes` is an empty default for the single-host fieldlab guests, so the projected JSON should be byte-identical — but verify, don't assume.)

### 3.4 Operator-review-387 cleanup status: DONE — all 4 findings fixed + re-reviewed PASS

Per `reports/cloud-designer/50-general-vm-testing-interface/1-psyche-decisions.md` §"Operator review 387 — cleanup DONE, re-review PASS (2026-06-16)" and report 52 §"Operator review (387)". The reviewer drove each assert to prove it fires. Mapping to actual commits:

- **F1 — TapSubnet IPv4 + capacity** → horizon-rs **`8fb25be`**: `TapSubnet`→`Ipv4Net` (IPv6 rejected into `InvalidTapSubnet`), `usable_host_count`/`can_host` helpers, and a Nix `assertModel` subnet-capacity check (a `/30` with >2 guests aborts eval).
- **F2 — `mkDeployTest` uses `hostNode`** → CriomOS-test-cluster **`89f93ba`**: `mkDeployTest` now reads + asserts `hostNode` declares VmHost and `vmNode` is a Pod with `superNode==hostNode`.
- **F3 — deploy smoke asserts durable state** → same commit **`89f93ba`**: the durable lojix `Query` is now asserted (node + slot + closure). The slot asserted is **`Current`** — verified correct: `activation_commit()` hardcodes `GenerationSlot::Current` in the durable record; an earlier relay of "BootPending" was an implement-agent mis-description. `lojix-deploy-smoke` re-ran GREEN.
- **F4 — test-substrate prose** → CriomOS **`42bc62b3`**: `test-substrate.nix` comment corrected to say `vmTypeModule` is NOT composed on the hermetic path (`mkVmTest` imports only `guestModule`).

The branch HEADs in §2.1 are post-cleanup, so 387's "integrate after cleanup" verdict is satisfied. **The operator does not need to do any cleanup of the VM-testing branches — they are clean.**

### 3.5 KNOWN CAVEATS the operator must handle

1. **Strict-positional NOTA requires the new `Machine` tail fields; goldragon records are stale-arity.** The `Machine` struct (horizon-rs `lib/src/machine.rs` on `214e6816`) is now **12 fields**: `species, arch, cores, model, mother_board, super_node, super_user, chip_gen, ram_gb, disk_gb, location, super_nodes`. NOTA is strict-positional (`#[serde(default)]` covers JSON only). The branch's `fieldlab.nota` records carry the tail through `location` (and omit the trailing empty `super_nodes` Vec, which the decoder tolerates as an empty default — confirmed by 135/135 passing). But `repos/goldragon/datom.nota` records are SHORTER — they stop at `ram_gb`, missing `disk_gb`, `location`, `super_nodes`. This does NOT bite the merge itself: **goldragon is not projected by any current check** (only `--cluster fieldlab` is wired). It bites the Prometheus wiring (§4.3) — the operator must extend ALL goldragon `Machine` records with the 3-field tail before goldragon is projected. VERIFIED empirically (§4.3.1).

2. **Pre-existing `source-constraints` RED — NOT introduced by these branches.** The test-cluster `source-constraints` check (`checks/source-constraints.nix`) scans all CriomOS `modules/nixos/*.nix` for forbidden host-fact tokens (`goldragon`, `prometheus`, `zeus`, etc.). `CriomOS/modules/nixos/llm.nix:158` has the comment `# this host's age key in goldragon/secrets`, containing the literal `goldragon` — tripping the check RED. Verified pre-existing: the comment is on CriomOS main (introduced by `699c7a6`, pre-branch), the `horizon-test-vm` branch did not touch `llm.nix`, and `source-constraints.nix` is pre-existing. The cloud-designer cleanup explicitly flagged this out-of-scope. **The operator should NOT treat this RED as a blocker for the VM-testing merge, and should fix it separately** (e.g. reword `llm.nix:158` to drop the literal `goldragon` token).

## 4. Remaining implementation (concrete specs)

### 4.1 Unit 3 — CriomOS emits the SCOPED image-exchange keys

**Summary.** Unit 1 projects a per-guest field `imageExchangePubKeys` = the Nix signing-key lines of exactly the hosts in that guest's declared host-set (`{super_node} ∪ super_nodes`), proven strictly tighter than the cluster-wide pool. Unit 3 makes a CriomOS **host** emit, per its `extra-trusted-public-keys`, the signing keys of the hosts it co-hosts a guest with — and ONLY those — so the declared hosts (and only they) can `nix-copy` a guest's image between each other.

**The Unit-1 projection contract Unit 3 consumes (verified):**
- **Field shape** — `node.rs:124-136`: `pub image_exchange_pub_keys: Option<Vec<NixPubKeyLine>>`. `Node` is `#[serde(rename_all = "camelCase")]` (`node.rs:28`), so the JSON key is **`imageExchangePubKeys`**. Each element is a `NixPubKeyLine` = `<criomeDomainName>:<base64key>` (`pub_key.rs:179-180`), the exact line format `nix.settings.trusted-public-keys` expects.
- **Derivation** — `fill_viewpoint` at `node.rs:558-564`: `self.machine.host_set().iter().filter_map(|h| all_nodes.get(h)).filter_map(|host_node| host_node.nix_pub_key_line.clone()).collect()`. So it is the host-set's signing keys, in host-set order (primary first), skipping any host with no signing key.
- **`host_set()`** — `machine.rs:77-85`: `super_node` first, then `super_nodes`, deduped (`superNode`, `superNodes` in JSON).
- **Scope proof** — `lib/tests/horizon.rs:666-744`: a guest hosted on `ouranos`+`prometheus` gets exactly those two keys; `apollo` (a keyed Center in the cluster-wide pool but NOT a co-host) is provably absent.

**THE CRITICAL CONSTRAINT — `imageExchangePubKeys` is NOT on exNodes.** `Horizon::project` (`horizon.rs:119-153`) calls `fill_viewpoint` on the **viewpoint node only** (`:143`), then drops the viewpoint to form `ex_nodes` (`:146-151`). The `ex_nodes` entries are un-filled base `Node`s — their `image_exchange_pub_keys` stays `None` and, being `#[serde(skip_serializing_if = "Option::is_none")]` (`node.rs:135`), is OMITTED from the projected JSON for every exNode. **So `horizon.exNodes.<guest>.imageExchangePubKeys` does not exist** — a host module reading it gets `null`/missing.

**Recommended route: 3-Host (no horizon change).** The host RECOMPUTES the co-host trust set itself in `test-vm-host.nix`, from data present on exNodes: for each co-hosted guest, take `guest.machine.superNode` ∪ `guest.machine.superNodes`, drop `thisNode`, resolve each to a cluster node's `nixPubKeyLine`, union+dedup. This is the exact host-side mirror of the guest-side `fill_viewpoint` fold. All inputs ARE available: exNodes carry `machine.superNode`/`machine.superNodes` and each cluster node's `nixPubKeyLine` is on its base projection (`node.rs:98`). Recommend 3-Host: it needs only the already-built Unit-1 fields, lands entirely within CriomOS, and keeps the projection from re-touching. (The alternative, 3-Horizon, adds a viewpoint-only `hostImageExchangePubKeys` field — a horizon-rs change that must land first; only take it if the psyche wants the host-side relation typed for queryability.)

**Per-host aggregation rule (precise):** `hostKeys(H) = ⋃ over guests G where H ∈ hostSet(G) of { nixPubKeyLine(P) : P ∈ hostSet(G), P ≠ H }`. Self-key excluded; union+dedup across all co-hosted guests; single-host guests contribute nothing (a host that only primarily-hosts single-host guests emits an empty `extra-trusted-public-keys`, correctly a no-op).

**The single substantive design decision inside Unit 3 — aggregation precision.** `test-vm-host.nix`'s `hostedTestVms` filter today is `superNode == thisNode` (only guests this node PRIMARILY hosts). For a multi-host guest whose primary is a peer but whose `superNodes` includes `thisNode` (this node is an ADDITIONAL host), the current filter misses it, so this node would not pick up that guest's co-host keys. To honor "the declared hosts AND ONLY THEY can exchange," the trust computation should scan guests where `thisNode ∈ host_set(guest)` (primary OR additional) — a broader predicate than the microvm-emission predicate. **Recommended: option (a)** — compute `imageExchangePubKeys` from a separate `coHostedTestVms = filter (g: elem thisNode (hostSet g)) (attrValues exNodes)` predicate, decoupled from `hostedTestVms` (which stays `superNode == thisNode` for the `microvm.vms` emission, since only the primary host runs the VM). This is the correct image-exchange boundary and is what makes the multi-host case actually work.

**Which module emits it, and how.** Module: `modules/nixos/test-vm-host.nix` (CriomOS, `origin/horizon-test-vm` `42bc62b3`). It already gates on `kvmAvailable`/`hasGuests` and computes the co-hosting set. The current `mkIf (hasGuests && kvmAvailable) { … }` body gains one attribute:

```nix
nix.settings.extra-trusted-public-keys = imageExchangePubKeys;
```

Use `extra-trusted-public-keys` (additive) NOT `trusted-public-keys` (which `modules/nixos/nix/client.nix:72` already sets to the cluster-wide `trustedBuildPubKeys`). Additive emission is the whole point: it grants the co-host keys ON TOP OF the host's normal config without disturbing the cluster-wide pool, and it is the same key `lojix` injects per-deploy (`lojix/src/schema_runtime.rs:3891-3917`, `extra-trusted-public-keys` as a transient `--option`). Unit 3 is the config-baked counterpart of that transient injection.

Aggregation expression (3-Host, sketch — operator owns final Nix):

```nix
let
  inherit (lib) unique findFirst;
  inherit (builtins) filter map attrValues concatMap elem;
  allNodes = [ horizon.node ] ++ attrValues exNodes;
  pubKeyOf = name:
    let n = findFirst (m: m.name == name) null allNodes;
    in if n == null then null else (n.nixPubKeyLine or null);
  hostSetOf = g:
    (lib.optional (g.machine.superNode != null) g.machine.superNode)
    ++ (g.machine.superNodes or []);
  coHostedTestVms = filter (g: (g.behavesAs.testVm or false) && elem thisNode (hostSetOf g))
                      (attrValues exNodes);
  coHostNames = concatMap (g: filter (n: n != thisNode) (hostSetOf g)) coHostedTestVms;
  imageExchangePubKeys = unique (filter (k: k != null) (map pubKeyOf coHostNames));
in …
```

**The gate (eval/assert — mirror `checks/nix-role-policy/default.nix:65-118`).** Add a CriomOS eval check (no VM boot): build a `nixosSystem` with a hand-authored `horizon` carrying a host that co-hosts a multi-host guest with one peer (peer keyed), plus a third keyed cluster node that is NOT a co-host, then assert against `config.nix.settings.extra-trusted-public-keys`:
- **lands**: the peer co-host's `nixPubKeyLine` IS in `extra-trusted-public-keys`.
- **scoped, not cluster-wide**: the non-co-host third node's key is ABSENT (the direct analogue of the horizon `apollo`-absent test at `horizon.rs:724-743`).
- **additive, not replacing**: `trusted-public-keys` (the cluster-wide pool from `client.nix`) is untouched and still carries the full pool.
- **single-host no-op**: a host that co-hosts no multi-host guest emits empty `extra-trusted-public-keys`.

Follow the check's `pkgs.runCommand … test ${lib.escapeShellArg …}` assertion style; name the check by its invariant, e.g. `image-exchange-keys-scoped-to-co-hosts`, one concept, PATTERN comment. Note: the only declared VmHost today is `atlas`/fieldlab, and all three test guests are single-host on atlas (no `superNodes`), so the test cluster does NOT yet exercise multi-host image-exchange — Unit 3's gate must be this synthetic-horizon CriomOS eval check, not a fieldlab projection assertion. (A multi-host fieldlab guest could be added later as a pure cluster-data addition.)

**Ordering.** Unit 3 (3-Host route) depends only on Unit 1 being on horizon main — the host recomputes from `machine.superNodes` + `nixPubKeyLine`, both already projected onto exNodes. No new horizon dependency beyond the merge. CriomOS-side; lands as a designer branch off the merged CriomOS main.

### 4.2 The live path — `LiveNotYetEnabled` → the report-51 host-untouched cycle

Verified against lojix main `538fdebf`. **The honest baseline today:** a Live `TestRequest` is rejected at submit; the brackets are BUILT but never run live.

- **Submit-time gate** — `resolve_and_validate` (`schema_runtime.rs:1595-1600`) returns `Err(TestRejectionReason::LiveNotYetEnabled)` whenever any resolved run is `TestMode::Live`. This is the single thing the operator must remove.
- **`drive_submitted_test`** (`:1366-1394`) constructs the first Live effect `BringUpTestVm(bring_up_command(ClosurePath::new(String::new())))` — an **empty runner closure** (`:1382-1386`).
- **`bring_up_command`** (`:324-332`) hardcodes `guest_ip: String::new()` and takes `runner` from the caller (currently empty). **`tear_down_command`** (`:336-342`) is complete.
- **`LiveTestVm`** (`:565-651`) is the real invocation builder: `bring_up_invocation` (`:614-624`) emits `systemd-run --user --unit=lojix-test-vm-<node> --collect --service-type=notify unshare -rn /bin/sh -c <body>`; `bring_up_body` (`:630-640`) does `ip tuntap add dev vmt0 mode tap; ip addr add 169.254.100.1/32 dev vmt0; ip link set vmt0 up; ip route add {guest_ip} dev vmt0; exec {runner}`. **The host endpoint `169.254.100.1/32` is hardcoded**, and `guest_ip`/`runner` are empty strings.
- **`run_bring_up_test_vm`** (`:2894-2909`) and **`run_tear_down_test_vm`** (`:2915-2926`) construct the invocation into `let _invocation = …` and **discard it** — returning `TestVmBroughtUp`/`TestVmTornDown` without ever `.run().await`-ing.
- **`decide_test_effect_completion`** (`:1738-1791`): the `TestVmBroughtUp` arm (`:1755-1765`) records the container `Started`, sets stage `BroughtUp` then immediately `Asserted`, and jumps **straight to `TearDownTestVm`** — no deploy, no assert in between. The `TestVmTornDown` arm (`:1766-1782`) records `Stopped` and writes terminal **`Failed(FailureStage::Assert)` — never Passed** (the honesty belt).

**Key positive findings (no schema work needed for the result surface):**
- The durable phase ladder already exists: `TestRunPhase [Submitted BringingUp Deploying Asserting TearingDown Completed Failed]` (`signal-lojix/src/schema/lib.rs:342-350`) and `FailureStage [BringUp Deploy Assert TearDown HermeticCheck]` (`:373-379`). The live path only needs to *use* `Deploying`/`Asserting`/`TearingDown` — unused today.
- `ContainerState [Starting Started Stopping Stopped]` exists (`lojix/src/schema/sema.rs:179-183`); only `Started`/`Stopped` recorded today. `record_container_transition` (`:2541+`) is the working driver.
- The guest IP **is projectable**: the projected `Node` carries `node_ip: Option<NodeIp>` (`horizon-rs/lib/src/node.rs:37`), and `mercury` declares `(Some [10.77.0.7/24])` (the exact IP reports 48/49 used).
- The whole deploy effect chain (`ResolveFlakeAuth → MaterializeHorizon → NixEval → NixBuild → CopyClosure → ActivateGeneration`) and `SshTarget::root_at_node` already target a node by its `<node>.<cluster>.criome` domain with **zero VM special-casing**.

**The ordered change-list (spec points 1–7):**

1. **(spec 1) Build the node's generated microVM runner + the guest IP from its projection — the largest missing piece.** Today the daemon has NO code deriving a runner closure or a guest IP. The model to mirror is `CriomOS-test-cluster/lib/mkVmTest.nix` (horizon-test-vm), which does exactly this in Nix.
   - **1a. Guest IP** — projection-read, not a placeholder. The daemon already projects clusters in `HorizonMaterialization::run_inner` (`:2957-2966`). The live path projects the guest node the same way and reads `node_ip` (strip the `/24` prefix → bare `10.77.0.7`). Fold this into `ResolvedTestRun` (add `guest_ip` + `runner` fields, populated when the Live pipeline opens) rather than leaving `bring_up_command`'s `guest_ip: String::new()`.
   - **1b. Host tap endpoint** — currently hardcoded `169.254.100.1/32` in `bring_up_body` (`:633`). Report 51 §2 and `mkVmTest.nix:170-184` (`hostTapAddressOf`: `base(guestSubnet) + guestIndex + 1`) derive it from the host's `VmHost.guest_subnet` sliced by the guest's sorted index. Derive it from the host projection; for the **first single-guest Prometheus run** the static `169.254.100.1` is correct (index 0 → base+1), so it can ship hardcoded-for-mercury-first and be generalized — flag it.
   - **1c. The runner closure** — the launch script is the Nix attribute `<host>.config.microvm.vms.<guest>.config.config.microvm.declaredRunner` (report 51 §2, report 48 log line 31). It must be realized by a `nix build` whose out-path becomes `BringUpTestVmCommand.runner` (`runner: ClosurePath`, `nexus.rs:252`). Preferred shape: a new `NixBuild`-flavored effect emitted as the Live pipeline's *first* effect (before `BringUpTestVm`), capturing the out-path onto the cursor, then passed into `bring_up_command`. Reuse the `NixCommand::build_check`-style `nix build <flake>#…declaredRunner --print-out-paths` (`:3851-3861`). **Mind the `<drv>^*` bug** (`:3879-3889`, `output_installable`): a bare `.drv` prints the `.drv`, so the runner build must print the realised script. Today `drive_submitted_test` (`:1382-1386`) passes an empty `ClosurePath` — that line must change to thread the built runner path.

2. **(spec 2) `BringUpTestVm` runs the real invocation.** Change `run_bring_up_test_vm` (`:2894-2909`) and `run_tear_down_test_vm` (`:2915-2926`) from constructing-and-discarding to actually running:

   ```rust
   // run_bring_up_test_vm: replace `let _invocation = …;` with:
   match bring_up.bring_up_invocation().run().await {
       Ok(_) => EffectResult::TestVmBroughtUp(TestVmBroughtUp { … }),
       Err(detail) => Self::effect_failed(EffectStage::BringUpTestVm, detail),
   }
   ```

   `NixCommand::run` (`:3939+`) already spawns and maps non-zero exit to `Err(detail)`. The `EffectStage::BringUpTestVm`/`TearDownTestVm` failure mapping already exists (`test_failure_stage`, `:1859-1870` → `FailureStage::BringUp`/`TearDown`). This is the host-untouched user-namespace path: `ssh root@<host-fqdn>` → `systemd-run --user` → `unshare -rn` → tap inside the private netns → `exec` the runner. **No sudo, no `switch-to-configuration` on the host, host netns byte-identical.**

3. **(spec 3) The deploy chain into the VM.** Between `BroughtUp` and teardown, run the **existing deploy effects** targeting the *guest* node. Today `active_deploy` and `active_test` are **separate cursors** (`SchemaRuntime:44,51`) and there is **no test→deploy bridge** — this must be built. In the `TestVmBroughtUp` arm of `decide_test_effect_completion` (`:1755-1765`), instead of jumping straight to teardown:
   1. Set phase `Deploying` (durable row via `record_at`/`record_test_run`).
   2. Construct a `DeployPipeline` for `(System (<cluster> <guest> FullOs … Boot/BootOnce …))`. Report 51 §3 step 3 specifies `Boot`; reports 48/49 proved `FullOs` + `BootOnce` end-to-end on the UEFI substrate. Use `DeployPipeline::from_submission` (`:840+`) with the guest as `node_name`, so `SshTarget::root_at_node(cluster, guest)` (`:3266-3274`) targets `root@<guest>.<cluster>.criome`. The deploy chain then runs `ResolveFlakeAuth → MaterializeHorizon → NixEval → NixBuild(<drv>^*) → CopyClosure(--substitute-on-destination) → ActivateGeneration` autonomously (`decide_effect_completion`, `:1903-1947`).
   3. Thread that deploy pipeline to terminal through `drive_to_terminal` (`:1401-1422`), then resume the test pipeline at the assert step.

   **Guest reachability caveat (load-bearing, from reports 48/49):** the deploy's `nix copy`/`ssh` reach the guest at its tap IP only because the runner host had a `~/.ssh/config` alias `<guest>.<cluster>.criome → 10.77.0.7` and `NIX_SSHOPTS=-F ~/.ssh/config` (report 48 log lines 93-96, 202-203), and the daemon ran *inside* the namespace. The current `SshTarget::remote_invocation` (`:3303-3313`) emits plain `ssh -o BatchMode=yes` with no `-F` — so either (a) the host's `~/.ssh/config` must carry the guest alias, or (b) the daemon must inject `NIX_SSHOPTS`/`-F`. **This wiring is NOT in the daemon today** and must be added or arranged on the host as a live-run prerequisite. Flag prominently.

4. **(spec 4) A REAL assert → a REAL outcome.** Replace the unconditional `Failed(Assert)` (`:1776-1781`). Report 51 §3 step 4: query the daemon's durable terminal deploy-job record and check the guest booted the lojix-deployed closure (the generation-activation check):
   - **Generation-activation check (recommended first):** the deploy chain into the guest records `GenerationActivated`; the assert confirms the activate effect succeeded (the deploy pipeline reached `ActivatedRecorded`/`finish_deploy_pipeline` without `EffectFailed`). A successful deploy-into-guest → `TestOutcome::Passed`, closure = the deployed out-path; a failed deploy → `Failed(Deploy)`.
   - **OR** run the node's auto-pickup `vm-<node>` check script (report 53 §1) over ssh into the guest.
   
   The outcome must be **earned**: `Passed` only if the deploy-into-guest activated and the assert held; otherwise `Failed(Deploy)`/`Failed(Assert)` with the real stage. The honesty belt at `:1766-1782` (never `Passed` without an assertion) stays — it just stops being the *only* path.

5. **(spec 5) `TearDownTestVm` + the ContainerLifecycle records.** Teardown works once `run_tear_down_test_vm` actually runs the invocation (§2): `systemctl --user stop lojix-test-vm-<node> || true` (`:644-650`) — the tap + route vanish with the namespace, host netns byte-identical. **ContainerLifecycle records:** today only `Started`/`Stopped` recorded (`record_container`, `:1823-1825`); the full ladder `Starting → Started → Stopping → Stopped` exists (`sema.rs:179-183`). Record `Starting` before bring-up and `Stopping` before teardown to give the report-47 §2 `ContainerLifecycleRecord` table its complete driver. Container name is `vm-<node>` (`container_transition`, `:414-421`).

6. **(spec 6) The schema change — removing `LiveNotYetEnabled` is a schema edit.** It is a generated variant: `meta-signal-lojix/schema/lib.schema:160` (`TestRejectionReason [… NoTestDefaults LiveNotYetEnabled SubstrateUnavailable InternalError]`) → regenerated into `meta-signal-lojix/src/schema/lib.rs:402`. Per the no-backward-compat override, drop the variant from the `.schema` source, regenerate the codec, remove the `:155-158` comment block, the lojix `:1595-1600` guard, and the `:402` enum arm. Everything else (phases, outcomes, failure stages, effects, container states) is already in the wire contract — **no other schema additions needed.**

7. **(spec 7) The gates stay load-bearing.** Hermetic stays the proven CI path, untouched — `runNixOSTest` with zero host effect, the everyday default (`decide_test_effect_completion` HermeticCheck arm, `:1745-1754`). The first live run is PSYCHE-GATED (§5).

**Ordered operator change-list for the live path:**
1. meta-signal-lojix schema: delete `LiveNotYetEnabled` from `schema/lib.schema:160` + comment `:155-158`; regenerate (→ removes `src/schema/lib.rs:402`).
2. lojix `:1595-1600`: delete the `LiveNotYetEnabled` guard in `resolve_and_validate`.
3. lojix `ResolvedTestRun` (`:278-343`): add `guest_ip`/`runner` (+ host-tap endpoint), populated from the projection; fix `bring_up_command:330` `guest_ip: String::new()`.
4. lojix new runner-build effect (or reuse `NixBuild`) emitting `nix build <flake>#…declaredRunner` realised output (mind `<drv>^*`), captured onto the cursor; thread into `drive_submitted_test:1382-1386`.
5. lojix `run_bring_up_test_vm:2894-2909` / `run_tear_down_test_vm:2915-2926`: replace `let _invocation = …` with `.run().await` + error mapping.
6. lojix `decide_test_effect_completion` `TestVmBroughtUp` arm `:1755-1765`: insert `Deploying` phase + guest-targeted `DeployPipeline` driven via `drive_to_terminal`, then a real assert (`Asserting` phase) → real `TestOutcome`. Replace the unconditional `Failed(Assert)` at `:1776-1781`.
7. lojix container ladder: record `Starting`/`Stopping` around the effects.
8. Host prerequisite (not daemon code): the guest ssh-config alias + `NIX_SSHOPTS -F` reachability, and the daemon running inside the namespace.
9. **Do NOT run live** until the §5 gates clear and the psyche authorizes.

**Residual risks / unproven assumptions (flag in handoff):**
- Building `…declaredRunner` straight from the **production projection** is unproven — reports 48/49 used a hand-built standalone `mercury.nix` to dodge atlas's GGUF/clavifaber build breaks. The daemon building it from goldragon/Prometheus projection depends on Unit 3 + the goldragon `VmHost` edit landing. Real residual risk, not a copy-paste.
- Single-unit `lojix-test-vm-<node>` bring-up shape differs from the proven two-unit (`mercury-ns` + `mercury-vm`) shape — verify on first live run.
- Guest-reachability ssh wiring is **absent from the daemon** today.
- mercury's userspace does not fully come up on generic q35 (report 49: gen-2 kernel boots from the one-shot, but userspace stalls) — a CriomOS lean-profile gap (Unit B), not a lojix defect, but it caps what a live "assert the node works" can claim until Unit B lands.

### 4.3 The Prometheus wiring (goldragon data edit + test-VM nodes + TestDefaults config)

#### 4.3.1 The goldragon `VmHost` edit (DATA ONLY) — VERIFIED

State: `goldragon/datom.nota` HEAD `71a4666`. Prometheus is a production `LargeAiRouter`, `Metal` GMKtec EVO-X2 (8 cores / 128 GiB), services `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]` — **no `VmHost`**.

**The arity-tail prerequisite — VERIFIED, load-bearing, must be done first.** The current goldragon `Machine` records hold **9** root objects; the horizon-test-vm `Machine` type expects **12**. Running the freshly-built CLI against the unmodified file:

```
$ horizon-cli --cluster goldragon --node prometheus < datom.nota
error: parse cluster proposal: expected Machine to hold 12 root objects, found 9
```

The parser parses **every** node's Machine before projecting any viewpoint, so **all 5 Machine records** (`balboa`, `ouranos`, `prometheus`, `tiger`, `zeus`) must gain the 3-field positional tail or the whole proposal fails. The field order (verified `machine.rs:14-67` on `214e6816`): `species, arch, cores, model, mother_board, super_node, super_user, chip_gen, ram_gb, disk_gb, location, super_nodes`. The current records stop at `ram_gb`. The three missing tail fields are `disk_gb: Option<u32>`, `location: Option<Location>`, `super_nodes: Vec<NodeName>`. For every existing Metal node the correct tail is **`None None []`**. Patched all 5 records with `None None []` and confirmed clean projection (exit 0, full JSON horizon emitted). E.g. prometheus:

```
(Metal (Some X86_64) 8 (Some [GMKtec EVO-X2]) None None None None (Some 128) None None [])
```

(For real placement data the operator may optionally fill `(Some home-lab)` for `location`; `None None []` is the minimal parsing fix.)

**The VmHost service append — VERIFIED.** Append `(VmHost [169.254.100.0/22] Available (Some 4))` to Prometheus's services vector:

```
[(TailnetClient) (NixBuilder (Some 6)) (NixCache) (VmHost [169.254.100.0/22] Available (Some 4))]
```

Confirmed it projects correctly (after the arity fix), emitting:

```json
"VmHost": { "guestSubnet": "169.254.100.0/22", "kvm": "Available", "maximumGuests": 4 }
```

Field semantics (verified `proposal.rs:128-181`):
- **`guest_subnet: TapSubnet`** — bracket-delimited because of the `/`: `[169.254.100.0/22]`. `TapSubnet` is an `Ipv4Net` newtype; link-local, never routed — `5hir5bnz`-inert (the C2 host endpoint is a `/32` link-local sliced from it; Prometheus's routed IP is never touched). **This `/22` link-local CIDR is the value report 51 §1a proposes and the psyche's to confirm.**
- **`kvm: KvmAvailability`** = `Available` (bare atom). Must be `Available` so C2's `mkIf (hasGuests && kvmAvailable)` fires and selects KVM over TCG. Report 48 preflight confirmed `/dev/kvm` present (mode 666) on Prometheus.
- **`maximum_guests: Option<MaximumGuests>`** = `(Some 4)` — a ceiling asserted-not-exceeded at eval, not a reservation.

`VmHost` is a `NodeService` sibling to `NixBuilder`/`NixCache`; adding it does NOT change Prometheus's species (`LargeAiRouter` stays) and changes no running system until a deploy — and there is no deploy.

**THE HARD DATA-ONLY / NO-DEPLOY GATE.** This edit is **DATA ONLY. It must never be deployed to the live router via `lojix Deploy … switch`.** The hazard is the gemma incident, verbatim at `43-routed-microvm-standup/5-risk-history.md:21-45`:
- `kx32` (Constraint, High): a live switch on the router restarts `hostapd`/`dnsmasq`/`networkd`/`kea` and drops the SSH/Wi-Fi connection — "which is what broke during the gemma deploy" — and "there is none [out-of-band/console access] today."
- `xv9v`: use BootOnce, never live Switch, until console access + sign-off exist.
- `1lex`: any risky activation runs as a detached durable systemd unit, never the foreground SSH session.

So `switch-to-configuration` on the router is forbidden. The edit records the capability in cluster data; the live materialization (§4.2) is host-untouched user-namespace only.

**Commit convention (goldragon).** Per `goldragon/AGENTS.md`: jujutsu only, push immediately, Mentci three-tuple format: `(("CommitType", "data"), ("Action", "declare Prometheus VmHost test-VM-host capability + C1 Machine tail"), ("Verdict", "..."))`. Keep new atoms bare where eligible (HEAD `71a4666` "canonicalize bare cluster strings").

#### 4.3.2 Declaring the test-VM node(s) hosted on Prometheus

The psyche pointed at **goldragon** (Option A in report 51 §6 — production cluster as source of truth). Declare ≥1 `TestVm` Pod guest in `goldragon/datom.nota` with `super_node = prometheus`, mirroring fieldlab's `mercury` (`CriomOS-test-cluster/clusters/fieldlab.nota:105-129` on `origin/horizon-test-vm`). The `Pod` substrate field carries `(Some prometheus)` in the `super_node` slot; that is the predicate C2 reads (`n.machine.superNode == thisNode && n.behavesAs.testVm`) to host the guest. A `TestVm` species ⇒ `behaves_as.test_vm` (lean: sshd + writable disk, home/doc weight suppressed). The guest's own Machine record also needs the 12-field arity (its tail provides `disk_gb`, optional `location`, and `super_nodes` — `super_nodes` non-empty only if the guest is multi-hosted). Report 51 §1b gives the guest record template (Pod substrate, Qwerty/Uefi IO, guest ssh keys, link-local guest IP, `[(TailnetClient)]` services). The exact guest IP/keys are the psyche's to fill.

**Cross-cluster plumbing consequence (report 51 §4, independent of the live-run gate).** Because Prometheus is now goldragon-native as a host, the CriomOS-test-cluster generators must learn to project `--cluster goldragon` for the Prometheus host node:
- a `--cluster goldragon` projection path beside the existing fieldlab one in `projections-match-*`,
- committed `fixtures/horizon/prometheus.json` + guest fixtures (generated by `horizon-cli --cluster goldragon --node <n>`),
- `fixtureSystem`/`readHorizon` parameterized by cluster (today they assume the single fieldlab fixture set),
- retarget `hostNode = "prometheus"` in the `mkVmTest`/`mkDeployTest` calls (`flake.nix:131,161,207,215`).

This is the heavier wiring work; run hermetic C4/C5/C6 green (never touches Prometheus).

#### 4.3.3 The lojix `TestDefaults` config for Prometheus — exact NOTA, VERIFIED

The config is binary-only (rkyv startup file), authored as typed NOTA through `lojix-write-configuration` and encoded before the daemon sees it — never a flag, never a runtime `Configure`. `TestDefaults` (`lojix/src/lib.rs:197-204`): `{ cluster, default_vm_host, default_mode: TestMode, test_flake, proposal_source }`, the 6th field of `DaemonConfiguration` (`src/lib.rs:166-178`).

The `lojix-write-configuration` request schema is `ConfigurationWriteRequest` (`src/bin/lojix-write-configuration.rs:27-48`): a positional record of `ordinary_socket_path, ordinary_socket_mode, owner_socket_path, owner_socket_mode, state_directory_path, test_defaults, output_path`, where `test_defaults` is the positional 5-tuple `(cluster default_vm_host default_mode test_flake proposal_source)`. Exact wire form (verified `tests/write_configuration.rs:15`):

```
lojix-write-configuration "(ConfigurationWriteRequest (/run/lojix/ordinary.sock 432 /run/lojix/owner.sock 384 /var/lib/lojix (goldragon prometheus Hermetic github:LiGoldragon/CriomOS-test-cluster /var/lib/lojix/cluster.nota) {}))"
```

For the Prometheus deployment the `test_defaults` tuple is **`(goldragon prometheus Hermetic <test_flake> <proposal_source>)`**:
- `cluster = goldragon` — so `(Check mercury)` defaults the cluster (decision D).
- `default_vm_host = prometheus` — the host a `DefaultHost` request resolves to.
- `default_mode = Hermetic` — the everyday safe default; `Live` is the gated path.
- `test_flake` — the flake whose `#checks.<system>.vm-<cluster>-<node>` auto-pickup check the hermetic dispatch builds, and whose generated runner the live path brings up. For the proof this is `github:LiGoldragon/CriomOS-test-cluster`; once §4.3.2 lands goldragon-native this is the flake exposing the goldragon-projected checks.
- `proposal_source` — the cluster-proposal NOTA file path the daemon projects to validate `(OnHost h)` against the declared host-set and to resolve `All`. **This must point at the goldragon `datom.nota`** (e.g. `/var/lib/lojix/cluster.nota`, a deployed copy) so host-set validation actually runs; empty disables validation (`src/lib.rs:192-196`, and `resolve_and_validate:1608` only validates when `projection()` is `Some`).

The two socket modes are decimal: `432` = octal 660 (owner+group rw), `384` = octal 600 (owner-only) — matching the 660/600 owner/ordinary split.

### 4.4 The multi-host Test-validation activation — exact one-line widening point

Report 54's "structured one-line change already in place" is **confirmed and located**: `lojix/src/schema_runtime.rs:486-497`, method `Machine::host_set_of` (the single reader behind `validate_host_for_node` at `:467-480`). Today, because lojix pins horizon-lib **main** (which lacks `super_nodes`), it reads only the primary:

```rust
// schema_runtime.rs:486-497 (lojix main 538fdeb) — the widening point
fn host_set_of(&self, node: &ordinary::NodeName) -> Option<Vec<String>> {
    let name = HorizonNodeName::try_new(node.payload().clone()).ok()?;
    let proposal = self.proposal.nodes.get(&name)?;
    Some(
        proposal.machine.super_node.as_ref()
            .map(|primary| vec![primary.as_str().to_string()])
            .unwrap_or_default(),
    )
}
```

The doc comment (`:482-485`) names the follow-on: "The additive `super_nodes` join is the Unit-1-on-main follow-on; today the pinned horizon-lib carries only `super_node`." **The activation is: (1) integrate `horizon-test-vm` → horizon-rs main; (2) bump lojix's horizon-lib pin to that main; (3) widen this method to `proposal.machine.host_set()`** (which exists at `machine.rs:77-89`, returning `{super_node} ∪ super_nodes` deduped, primary first). That single substitution turns `validate_host_for_node` and the `(OnHost h)` picker into the full declared-host-set check. The companion `hosted_pod_nodes` sweep (`:503-510`, used by `All`) already filters on `super_node.is_some()` and is unaffected.

**lojix `Cargo.toml:35` pins `horizon-lib = { ..., branch = "main" }`** — this is the cross-unit dependency. Multi-host Test validation stays inert until horizon-rs `horizon-test-vm` merges to horizon-rs main and the pin picks it up. The hermetic Test path works today regardless because the sandboxed check owns its own VM and needs no real host projection.

## 5. Gates, dependencies, and safety

### 5.1 The cross-unit dependency graph

- **lojix pins horizon `branch = main` (`Cargo.toml:35`); Unit 1 multi-host is on the horizon branch.** Merging horizon-rs `horizon-test-vm` → main is the prerequisite for: the multi-host Test validation (§4.4, the `host_set_of` widening), the auto-pickup suite's projection drift gate, and Unit 3's recompute (which needs `machine.superNodes` + `nixPubKeyLine` on exNodes). After horizon merges, re-lock lojix's horizon pin to merged-main.
- **The three `horizon-test-vm` branches are interdependent** — test-cluster `89f93ba` re-locks `horizon 8fb25be9 / criomos 42bc62b3`, and fieldlab fixtures depend on the horizon `VmHost` projection + CriomOS emission. Integrate as a set, updating `flake.lock` pins to the merged main shas.
- **Unit 3** (3-Host route) depends only on Unit 1 on horizon main; lands within CriomOS.
- **The live path** is independent of Unit 3 for *code*, but the *first live Prometheus run* depends on Unit 3 (the guest must trust the unsigned locally-built closure — today faked by `require-sigs=false` in the test substrate), the goldragon `VmHost` edit, and the projection-built runner being proven.

### 5.2 The psyche-gated first live Prometheus run

The code can land with `LiveNotYetEnabled` removed and the pipeline wired, but **the first live Prometheus cycle does not run until explicit psyche authorization** (report 51 §5 step 6; report 54 decisions item 4). The three gate conditions to confirm (report 51 §6):
1. Run modality is host-untouched user-namespace, never a system-config switch (while Prometheus has no out-of-band access).
2. The chosen `guest_subnet` (link-local `169.254.100.0/22` proposed — non-routed, `5hir5bnz`-inert).
3. Explicit psyche authorization to perform the user-level live run on Prometheus.

**The safety envelope (report 51 §5, binding).** On the live run the daemon's live path **DOES**: log in as `li` (uid 1001), start `--user` systemd units, create a tap inside a private user network namespace, open world-writable `/dev/kvm`, append one line to `li`'s own `~/.ssh/config`. It **DOES NOT**: use sudo or root; run `switch-to-configuration`; create a new system generation; touch host networkd / `hostapd` / `kea` / `dnsmasq` / `br-lan`; add any route or interface to the host netns; change anything that survives `systemctl --user stop` + namespace teardown. Host netns is byte-identical before/after (proven reports 48/49). A hard refusal is carried in code intent (report 54 §5.2): on a `VmHost` that is also a live router, LIVE runs **only** the host-untouched user-namespace path — never `switch-to-configuration` on the router. The system-config deploy modality is **off the table** until Prometheus has real out-of-band/console access, which `5hir5bnz`/`kx32` states does not exist today.

### 5.3 The verification gates (what must be green at each stage)

- Pre-merge, per repo, from clean checkouts: §3.3 (horizon-rs `cargo test`/`clippy`; CriomOS `nix flake check`; test-cluster `nix flake check` incl. the four `vm-<node>` checks, `lojix-deploy-smoke`, `projections-match-fieldlab` after re-lock).
- Post-merge: re-run `projections-match-fieldlab` against merged-horizon-main; regenerate fixtures if any new field appears.
- Unit 3: the synthetic-horizon CriomOS eval check (`image-exchange-keys-scoped-to-co-hosts`) — lands/scoped/additive/no-op assertions.
- Prometheus wiring: project goldragon clean through `horizon-cli --cluster goldragon` (arity tail + VmHost); the `--cluster goldragon` `projections-match-*` path green; hermetic C4/C5/C6 green with `hostNode = "prometheus"`.
- Live path: hermetic stays green (untouched); the live cycle only after the §5.2 psyche gate.

## 6. Operator integration order (the full dependency-ordered plan)

Steps 1–7 touch nothing on Prometheus (model edits, schema, builds, hermetic checks). Only the final live run touches Prometheus, user-level only, behind the §5.2 gate.

1. **Merge the three `horizon-test-vm` branches → their mains** in order `horizon-rs` (`214e6816`) → `CriomOS` (`42bc62b3`) → `CriomOS-test-cluster` (`46febf36`), integrating from `origin/horizon-test-vm` (not the stale local ref), bumping test-cluster's `horizon`/`lojix` `flake.lock` pins to the merged mains (§3.2), running the §3.3 gates from clean checkouts before pushing each main. Operator owns the rebase (designers ship `next`/feature; operators own main + integration). Fix the pre-existing `source-constraints` RED separately (§3.5 caveat 2).
2. **Bump lojix's horizon-lib pin** (`Cargo.toml:35`) off `branch = main` to the new merged main, then **widen `host_set_of` → `proposal.machine.host_set()`** (§4.4, `schema_runtime.rs:486-497`) — lights up multi-host Test validation.
3. **goldragon data edit** (§4.3.1): C1 arity tail on all 5 Machine records (`None None []`) + the prometheus `VmHost` service + the `TestVm` guest (§4.3.2) — verified to project cleanly. Mentci three-tuple commit, jj only, push immediately. **DATA ONLY — never deployed.**
4. **Cross-cluster generator plumbing** (§4.3.2 / report 51 §4): `--cluster goldragon` projection path + committed goldragon fixtures + `hostNode = "prometheus"` retarget; run hermetic C4/C5/C6 green (never touches Prometheus).
5. **Unit 3 — CriomOS** (§4.1): emit the scoped `image_exchange_pub_keys` as `extra-trusted-public-keys` from the node's host-set (3-Host route, designer branch off merged CriomOS main) + the synthetic-horizon eval gate.
6. **Author the `TestDefaults` rkyv config** for Prometheus via `lojix-write-configuration` (§4.3.3), deploy the daemon with it + a copy of goldragon's `datom.nota` at `proposal_source`.
7. **Implement the live deploy+assert chain** (§4.2) — turns `LiveNotYetEnabled` into the report-51 host-untouched cycle (schema drop → guard removal → projection-read runner/IP → `.run().await` → guest-targeted `DeployPipeline` → real assert → real outcome → container ladder).
8. **GATED:** first live Prometheus run — only after the three §5.2 confirmations from the psyche.

## 7. Key file/line index for the operator

- `lojix/Cargo.toml:35` — `horizon-lib = { ..., branch = "main" }` (the cross-unit pin to bump).
- `lojix/src/schema_runtime.rs` (main `538fdeb`): `:486-497` (`host_set_of` — §4.4 widening), `:467-480` (`validate_host_for_node`), `:1595-1600` (`LiveNotYetEnabled` gate), `:1366-1394` (`drive_submitted_test`), `:1382-1386` (empty runner closure to thread), `:324-342` (`bring_up_command`/`tear_down_command`), `:565-651` (`LiveTestVm` invocation builder), `:614-624` (`bring_up_invocation`), `:630-640` (`bring_up_body`, hardcoded `169.254.100.1/32`), `:2894-2909`/`:2915-2926` (`run_*_test_vm` construct-and-discard), `:1738-1791` (`decide_test_effect_completion`), `:1755-1765` (`TestVmBroughtUp` arm), `:1766-1782` (`TestVmTornDown` arm / honesty belt), `:1859-1870` (`test_failure_stage`), `:840+` (`DeployPipeline::from_submission`), `:1401-1422` (`drive_to_terminal`), `:1903-1947` (`decide_effect_completion`), `:3266-3274` (`SshTarget::root_at_node`), `:3303-3313` (`SshTarget::remote_invocation`), `:3851-3861` (`NixCommand::build_check`), `:3879-3889` (`output_installable`/`<drv>^*`), `:3891-3917` (`extra-trusted-public-keys` per-deploy precedent), `:3939+` (`NixCommand::run`), `:2957-2966` (`HorizonMaterialization::run_inner` projection).
- `lojix/src/lib.rs:166-204` (`DaemonConfiguration` + `TestDefaults`), `src/bin/lojix-write-configuration.rs:27-48` (config request schema), `tests/write_configuration.rs:15` (exact NOTA template), `src/schema/sema.rs:179-183` (`ContainerState`), `src/schema/nexus.rs:248-296,371-372,554-558` (BringUp/TearDown effect commands, built-not-driven), `nexus.rs:252` (`runner: ClosurePath`).
- `signal-lojix/src/schema/lib.rs:342-350` (`TestRunPhase`), `:373-379` (`FailureStage`), `+schema/lib.schema`.
- `meta-signal-lojix/src/schema/lib.rs:396-405` (incl. `:402` `LiveNotYetEnabled` arm), `schema/lib.schema:155-166` (incl. `:160` variant + `:155-158` comment to drop).
- `horizon-rs … lib/src/machine.rs:14-67` (Machine 12-field order), `:77-89` (`host_set()`) — `origin/horizon-test-vm` `214e6816`.
- `horizon-rs … lib/src/node.rs:28` (camelCase), `:37` (`node_ip`), `:98` (`nix_pub_key_line`), `:124-136` (`image_exchange_pub_keys`), `:501` (None default), `:558-592` (`fill_viewpoint`).
- `horizon-rs … lib/src/horizon.rs:119-153` (viewpoint-only fill / exNodes omission).
- `horizon-rs … lib/src/proposal.rs:128-181` (`NodeService::VmHost`, `KvmAvailability`, `MaximumGuests`), `lib/src/address.rs` (`TapSubnet`).
- `horizon-rs … lib/tests/horizon.rs:666-744` (scope proof), `:754-` (single-host byte-identical).
- `CriomOS … modules/nixos/test-vm-host.nix` (Unit 3 emission module, `42bc62b3`), `modules/nixos/nix/client.nix:72` (cluster-wide `trusted-public-keys`, untouched), `checks/nix-role-policy/default.nix:65-118` (gate pattern to mirror), `modules/nixos/llm.nix:158` (pre-existing `source-constraints` RED).
- `CriomOS-test-cluster … flake.nix:7,18,28` (cross-repo inputs), `:131,161,207,215` (`hostNode`/`mkVmTest`/`mkDeployTest` calls to retarget), `:201` (`genAttrs` auto-pickup), `:206` (`projections-match-fieldlab`); `lib/mkVmTest.nix:170-184` (`hostTapAddressOf`, runner/guest-IP derivation model); `clusters/fieldlab.nota:29` (atlas VmHost), `:105-129` (mercury guest template).
- `goldragon/datom.nota` (HEAD `71a4666`) — prometheus services vector; all 5 Machine records need the `None None []` tail.
- Verification artifacts (not committed, under `/tmp`): `goldragon-all-fixed.nota`, `goldragon-vmhost.nota`. Built CLI: `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-test-vm/target/debug/horizon-cli`.
- Reports: `reports/cloud-designer/{47,48,49,50,51,52,53,54}-*`, `reports/cloud-operator/387-cloud-designer-vm-testing-review.md`, `reports/cloud-designer/43-routed-microvm-standup/5-risk-history.md:21-45`.
