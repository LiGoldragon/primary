# firmware divergence — OsOnly firmware-field divergence

cloud-designer, 2026-06-11. Grounded run for report 40. Area: OsOnly firmware-field build divergence (report 38 critique B) — confirmed

## Method

Read all four cited source/consumer sites at HEAD: lojix-cli/src/build.rs:51-101 (DeploymentShape, single field include_home; HEAD fc2ff02, branch HEAD), lojix/triad-port/src/schema_runtime.rs:1611-1638 (DeploymentInput, two fields; HEAD 7d66d2e), CriomOS/flake.nix:80-86 and modules/nixos/metal/default.nix:35-36,307 and checks/metal-firmware-policy/default.nix:1-87 (HEAD df05927). Confirmed lojix-cli has zero references to includeAllFirmware/include_all_firmware (grep over lojix-cli/src returned exit 1, no matches). Confirmed nexus.schema:59 MaterializationShape [FullOs OsOnly (Home ...)] is the daemon analog of lojix-cli SystemKind. Then ran a real, non-mutating `nix eval` (nix 2.34.6) against the read-only /git CriomOS checkout, instantiating modules/nixos/metal/default.nix with a base bareMetal node under all four deployment inputs and reading hardware.enableAllFirmware. Eval completed (exit 0). The CriomOS worktree under ~/wt was on a branch lacking the check file, so I used the read-only main checkout with --no-write-lock-file (eval only, no build, no mutation).

## Findings

### ✅ confirmed — lojix-cli's DeploymentShape emits ONLY includeHome — it has no firmware field at all (struct DeploymentShape { include_home: bool }), and OsOnly emits includeHome=false.

- **Evidence:** lojix-cli/src/build.rs:57-71 `pub struct DeploymentShape { include_home: bool }` with home_enabled()/home_disabled(); build.rs:85-91 flake_text emits literally `{ deployment = { includeHome = true|false; }; }` and nothing else; build.rs:94-100 OsOnly => home_disabled(). grep includeAllFirmware|include_all_firmware over lojix-cli/src => exit 1 (no matches).
- **Cutover implication:** The parity bar (Stack A) never writes the firmware field. CriomOS's fallback `includeAllFirmware = deployment.includeAllFirmware or includeHome` (metal/default.nix:36) therefore derives firmware FROM includeHome: OsOnly => false.

### ✅ confirmed — The new daemon's DeploymentInput emits includeHome AND includeAllFirmware, and for OsOnly it sets include_all_firmware: true (diverging from lojix-cli's false-by-derivation).

- **Evidence:** lojix/triad-port/src/schema_runtime.rs:1612-1638 `struct DeploymentInput { include_home, include_all_firmware }`; from_shape: FullOs => {include_home:true, include_all_firmware:true} (1621-1624); OsOnly => {include_home:false, include_all_firmware:true} (1625-1628); flake_text formats `deployment = { includeHome = {}; includeAllFirmware = {}; }` (1633-1637). Daemon OsOnly thus writes includeAllFirmware=true.
- **Cutover implication:** On an OsOnly deploy the daemon explicitly forces enableAllFirmware on, overriding the includeHome-derived default that lojix-cli relies on. The two stacks produce different deployment inputs for the same operation.

### ✅ confirmed — CriomOS consumes includeAllFirmware via `enableAllFirmware = deployment.includeAllFirmware or includeHome`, so the two inputs FLIP hardware.enableAllFirmware for an OsOnly node.

- **Evidence:** metal/default.nix:35-36 `includeHome = deployment.includeHome or true; includeAllFirmware = deployment.includeAllFirmware or includeHome;` and :307 `hardware.enableAllFirmware = includeAllFirmware;`. Live `nix eval` (exit 0): `{"daemon_OsOnly":true,"lojixCli_OsOnly":false}` for inputs daemon={includeHome=false;includeAllFirmware=true} vs lojixCli={includeHome=false}. Full four-input run: lojixCli_FullOs=true, lojixCli_OsOnly=false, daemon_OsOnly=true, daemon_FullOs=true.
- **Cutover implication:** Confirmed real eval-level flip on the exact field the metal-firmware-policy check guards. FullOs is identical across stacks (both true); the divergence is OsOnly-only.

### ✅ confirmed — The metal-firmware-policy check itself encodes the lojix-cli truth table and would reject the daemon's OsOnly input as a policy violation.

- **Evidence:** checks/metal-firmware-policy/default.nix:80-83 asserts: default{includeHome=true}=>true; homeOff{includeHome=false}=>false; explicitFirmware{includeHome=false;includeAllFirmware=true}=>true; explicitSynthetic{includeHome=true;includeAllFirmware=false}=>false. The daemon's OsOnly input is exactly the `explicitFirmwareConfiguration` row (=>true), i.e. the check documents that {includeHome=false;includeAllFirmware=true} is a DIFFERENT closure from plain home-off.
- **Cutover implication:** The closure difference is not incidental — CriomOS has a dedicated check distinguishing home-off (firmware off) from explicit-firmware-on. The daemon silently selects the explicit-firmware-on branch for every OsOnly deploy.

### ✅ confirmed — This is a real NixOS closure difference (not a no-op label change) that must be reconciled before any OsOnly node migrates from Stack A to Stack B.

- **Evidence:** hardware.enableAllFirmware in NixOS pulls in the broad linux-firmware set; metal/default.nix:304-309 comment: `Broad firmware remains enabled for normal deployments, while synthetic/home-off builds can opt out and rely on model-specific firmware below` (firmware = modelSpecificFirmware at :309). With enableAllFirmware=true the OsOnly closure gains the entire all-firmware package; with false it carries only modelSpecificFirmware. Different store paths => different system closure => different switch-to-configuration result.
- **Cutover implication:** An OsOnly node migrated to the daemon would build/activate a closure that includes all-firmware where lojix-cli built it firmware-lean. Running both stacks in parallel (cutover discipline) would show divergent closures for the SAME node, defeating parity verification. CORRECT FIX: the daemon's OsOnly arm must emit include_all_firmware: false (matching lojix-cli's includeHome-derived default), i.e. DeploymentInput::from_shape OsOnly => {include_home:false, include_all_firmware:false}. Equivalently, since CriomOS already derives firmware from includeHome when the field is absent, the daemon could omit the field for OsOnly entirely; emitting it as true is the bug.

## Notes

- Likely OsOnly migration candidates per datom.nota grounding: tiger & zeus (EdgeTesting/Edge, no router, no LLM) are the secret-free, OsOnly-plausible nodes where this flip would first bite. balboa=Center and prometheus=LargeAiRouter are FullOs-shaped (firmware identical across stacks), so they do not surface this divergence.
- FullOs is byte-identical across stacks for this field: lojix-cli FullOs emits includeHome=true (=> enableAllFirmware true via the `or` fallback), daemon FullOs emits includeHome=true+includeAllFirmware=true (=> true). The divergence is strictly the OsOnly path.
- The field set the daemon SHOULD emit, to match the parity bar: FullOs => {includeHome=true, includeAllFirmware=true} (already correct), OsOnly => {includeHome=false, includeAllFirmware=false}. The single wrong line is schema_runtime.rs:1627 `include_all_firmware: true` inside the OsOnly arm.
- Report 38's claim B is fully confirmed at both source level and eval level. The earlier note that lojix-cli is stateless does not apply here — this is a genuine deployment-input parity gap, not net-new charter.
- Eval was non-mutating: `nix eval --no-write-lock-file --impure --json` against the read-only /git/github.com/LiGoldragon/CriomOS checkout (rev df05927); no build, no store mutation, no code-repo main touched. nix version 2.34.6.
- The CriomOS worktree at ~/wt/github.com/LiGoldragon/CriomOS exists but is on a branch where checks/metal-firmware-policy/default.nix is absent; I instantiated the metal module directly from the main read-only checkout instead, replicating configurationFor from the policy check verbatim.
