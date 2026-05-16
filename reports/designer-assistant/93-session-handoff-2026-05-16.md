# 93 — Session handoff, 2026-05-16

*Designer-assistant session capped at the Claude 5h-window; substance
handed to system-specialist (Codex). This report
names what landed, what was queued but never fired, the per-subagent
follow-ups that surfaced after report 92 closed, and the suggested
order of operations for the next role.*

## TL;DR

Stage-1 (7 audit/research reports, 77–83) and stage-2 (4 implementation
subagents A–D, reports 84–87) landed and pushed; 16 commits across 5
repos plus 5 reports on primary `main`. Stage-3 was prepared but not
fired (subagents E for nspawn reinstatement and F for rich `Contained`
schema additions) — their briefs are preserved in §3 of this report and
in `92-cloud-host-arc-system-specialist-handoff.md` §3. Three discrete
follow-ups surfaced from stage-2 (§4): `llm.nix` resolveSecret
refactor, three pre-existing horizon-rs test failures, and an
orphan-sweep continuation in CriomOS-home. Decisions on the cloud-host
open questions are settled in 92 §1.

---

## §1 — What landed this session

### Stage-1 — research + gap audits (reports 77, 79–83)

| Report | Title | Findings |
|---|---|---|
| 77 | Nix container hosting prior art research | systemd-nspawn is CriomOS's existing substrate (dropped on branch — regression); microvm-cloud-hypervisor recommended as second substrate for Publication; OCI + extra-container rejected. 5 recommendations. |
| 78 | Cloud-host implementation roadmap | 10-step cutover. Rich `Contained { host, user, substrate, resources, network, state, trust, userNamespacePolicy }`; closed `Substrate ::= NixosContainer \| MicrovmCloudHypervisor`; host-set/contained-set/cloud-host-set module split. |
| 79 | CriomOS network gap audit | 25 gaps; top: wireguard.nix latent crash, wifi-eap SSID literal slips source-constraints, ClusterSecretBinding arc unfinished. |
| 80 | CriomOS metal/hardware gap audit | 15 gaps; **thermal regression** as Finding 1 (today's overheating cause); stringly-typed model dispatch; metal/default.nix concern-mixing (`primary-gfc0`). |
| 81 | CriomOS services/orchestration gap audit | 28 gaps; horizon-rs System serde bug; nspawn.nix deletion regression; AiProvider.api_key unconsumed in llm.nix. |
| 82 | CriomOS-home gap audit | 30 gaps; `arch == "x86-64"` typo installs i7z on zero nodes; `dunst.enable = !size.min` inside `mkIf size.min`; Emacs theme reads stale darkman path. |
| 83 | horizon-rs ↔ consumer alignment audit | 21 alignment findings; zero JSON RT tests on `view::*` records is the major systemic finding. |

### Stage-2 — implementation subagents (reports 84–87)

All four landed. Cumulative diff: 16 commits across horizon-rs, goldragon, CriomOS, CriomOS-test-cluster, CriomOS-home — all on `horizon-re-engineering` — plus 5 reports committed to primary `main`.

| Subagent | Report | Lane | Result |
|---|---|---|---|
| A | 84 | horizon-rs Rust | System per-variant serde rename + JSON RT (6 tests); KnownModel +3 variants + ComputerIs flags; goldragon datom rewrites (balboa `rock64`→`Rock64`, prometheus `"GMKtec EVO-X2"`→`GmktecEvoX2`); view JSON RT seed (17 tests, every `view::*` record kind). 29 new tests; 4 commits. |
| B | 85 | CriomOS Nix | Thermal regression cherry-pick (overheating fix); wireguard.nix latent crash fix (`inherit` scope + `pubKey` field name); wifi-eap.nix SSID literal lift + source-constraints widened; AiProvider.apiKey wired via sops. 5 commits. |
| C | 86 | horizon-rs + CriomOS | `view::Cluster.secret_bindings: BTreeMap<SecretName, SecretBackend>` projected with duplicate-name loud-fail; new `resolveSecret` helper in `modules/nixos/secrets.nix`; `nordvpn.nix` and `router/default.nix` refactored to dispatch through it. 3 commits. |
| D | 87 | CriomOS-home Nix | `i7z` gates on `chipIsIntel` (typo fix); dead `dunst` block deleted; Emacs theme reads `chroma/current-mode` (verified against `chroma/src/theme.rs:443`); 5 orphan modules deleted (waybar/hyprland/sway/swayConf + med/element); `wasistlos` stub deleted; Quickshell stale-widget note added to dictation.nix. 6 commits. |

### Primary `main`

- Report renumbering: parallel-agent's 84/85 critique → 90/91 (substance preserved, cross-citation updated).
- 92 cloud-host arc system-specialist hand-off (§1 decisions, §4 work order).
- 84, 85, 86, 87 stage-2 subagent reports committed via two `main` pushes.

---

## §2 — Standing decisions (carry forward from 92 §1)

User-authorised on 2026-05-16. The cloud-host open questions are settled:

| Topic | Decision |
|---|---|
| Q1 substrate per-variant fields | Empty struct variants — `Substrate ::= NixosContainer {} \| MicrovmCloudHypervisor {}`. |
| Q2 Ghost packaging in cloud-host arc | Out of scope; independent track. |
| Q3 cloud-host species | New `NodeSpecies::CloudHost` (not a derived flag). |
| Q4 trust→flags lowering location | Per-substrate wrappers; `contained.nix` carries the policy helper. |
| Cross-realm session-lock | Collapse to system-only `loginctl lock-sessions`. |
| Tailnet TLS server material | Extend `TlsTrustPolicy` to carry server cert + key. |
| Tailscale-protocol constants | New `TailscaleConstants` Nix attribute (NOT inside `TailnetConfig`). |
| nspawn.nix deletion | Regression — reinstate. |
| Orphans / dead code | Delete freely; git history holds the path. |
| Emacs theme darkman→chroma | Subagent D took the file-poll path against chroma; push-subscription is the noted follow-up. |
| lojix-cli sopsFiles template | No change on main (legacy); kebab-case template lives on horizon-re-engineering already. |

---

## §3 — Stage-3 prepared but not fired

Two subagents were briefed but the 5h-window capped the session before they fired. **Both can be picked up cleanly by the next role** — the briefs below are the full work specs; no design questions remain.

### §3.1 Subagent E — nspawn.nix reinstatement (cutover step 1)

**Lane**: CriomOS Nix.
**Branch**: `horizon-re-engineering` worktree at `/home/li/wt/github.com/LiGoldragon/CriomOS/horizon-re-engineering/`.
**Report number to claim**: 94 (in whatever lane's `reports/<role>/` directory the implementer chooses; e.g. `reports/system-specialist/N`).

Scope:

- Cherry-pick `modules/nixos/nspawn.nix` from `main` at `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nspawn.nix` — the `criomos-nspawn` wrapper gated on `size.large && behavesAs.center`.
- Verify any role-policy check at `checks/nspawn-role-policy/` exists on main and reinstate if missing on branch.
- Apply the resolveSecret follow-up subagent C flagged: `modules/nixos/llm.nix` (which postdates the audit and got AiProvider.apiKey wiring in B's commit) still calls sops directly — refactor to call `resolveSecret { name = provider.apiKey.name; }` from C's helper. One-commit change, same pattern as the nordvpn + router refactors C landed.
- Resource posture: `nix-instantiate --parse` only; no nix build/eval.
- jj flow: one commit per logical change (nspawn reinstatement, llm.nix refactor), `jj bookmark set horizon-re-engineering -r @-`, `jj git push --bookmark horizon-re-engineering`.

### §3.2 Subagent F — rich `Contained` schema additions (cutover steps 2–3)

**Lane**: horizon-rs Rust (Operator's surface; designer-assistant CAN land falsifiable-spec tests per `skills/designer.md`).
**Branch**: `horizon-re-engineering` worktree at `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-re-engineering/`.
**Report number to claim**: 95 (or operator-assistant lane).

Scope (per the decided cloud-host design):

- New types in `lib/src/proposal/placement.rs` (or new sub-modules):
  - `Substrate ::= NixosContainer {} | MicrovmCloudHypervisor {}` (empty struct variants per Q1; `NotaSum` derive).
  - `Resources { cores: u32, ram_gb: u32 }` (NotaRecord).
  - `ContainedNetwork { local_address: VirtualIp, host_address: VirtualIp }` (NotaRecord; new `VirtualIp` typed newtype or alias).
  - `ContainedState { persistent_paths: Vec<PersistentPath> }` (NotaRecord; new `PersistentPath` newtype).
  - `UserNamespacePolicy ::= PrivateUsersPick | PrivateUsersIdentity | PrivateUsersOff` (NotaEnum, closed sum).
- Extend `NodePlacement::Contained` with `substrate, resources, network, state, trust: Magnitude, user_namespace_policy: UserNamespacePolicy`. **Tail-position** the new fields for positional NotaRecord stability with existing datoms (per system-assistant/15 §"positional Nota-record stability").
- Goldragon datom: no update needed if defaults are valid; otherwise add explicit defaults (e.g., `(Contained atlas aria NixosContainer (Resources 2 2) (ContainedNetwork "10.42.0.10" "10.42.0.1") (ContainedState []) Medium PrivateUsersPick)`).
- Fieldlab `dune` node: same shape (it's currently `(Contained atlas aria)`).
- View-side: extend `view::ProjectedNodeView` in `lib/src/view/projected_node.rs` to carry the same rich fields (so consumers see the substrate/resources/network/state/trust/userNamespacePolicy without re-deriving).
- New `NodeSpecies::CloudHost` variant in `lib/src/species.rs` (per Q3) + projection support (`TypeIs.cloud_host` flag in `view::TypeIs`).
- Extend `TlsTrustPolicy` in `lib/src/proposal/services.rs` with `server_certificate: Option<PublicCertificate>` and `server_private_key: Option<SecretReference>` per the Tailnet-TLS decision.
- JSON RT tests for every new record and the extended NodePlacement, in `lib/tests/` (one file per record group per the seed pattern A landed).
- Tests: `cargo test --jobs 1 -- --test-threads=1`. Resource posture: avoid heavy compile.
- jj flow: one commit per logical group (Substrate sum + sub-records; NodePlacement extension; view::ProjectedNodeView extension; NodeSpecies::CloudHost; TlsTrustPolicy extension; JSON RT tests). Per-commit push.

### §3.3 Sequencing

E and F can run in parallel — different repos, no working-copy overlap.

---

## §4 — Follow-ups surfaced by stage-2 subagents (post-92)

| # | Source | Follow-up | Severity |
|---|---|---|---|
| F1 | C, A | Three pre-existing horizon-rs test failures: `node_proposal_size_zero_decodes_via_renamed_variant`, `metal_arch_unresolvable_when_no_arch_set`, `nordvpn_profile_decodes_from_nota_record`. Predate today's work; assertion-substring drift. Worth fixing soon to unblock CI green. | medium |
| F2 | A | Sweep CriomOS modules for raw `rock64` / `"GMKtec EVO-X2"` string matches that now silently miss (the variants are PascalCase). | medium |
| F3 | A | Add `ARCH.md` (horizon-rs) commitment naming the dashed-tuple wire shape for `system` (so future agents don't re-introduce PascalCase). | low |
| F4 | A | JSON RT tests for proposal-side closed sub-enums (audit 83 asked for view-side first; proposal-side parity is the next layer). | low |
| F5 | C | `modules/nixos/llm.nix` (post-audit) bypasses the binding the same way nordvpn did — same one-commit fix. **Folded into §3.1 Subagent E's scope.** | medium |
| F6 | D | Likely additional orphans in CriomOS-home: `fzf*.nix`, `zed_*` files. Sweep + delete. | low |
| F7 | D | `# freecad # broken` comment-out — clean delete (same pattern as wasistlos). | low |
| F8 | D | `AIPackages` → `aiPackages` rename for naming consistency. | low |
| F9 | D | Profile-ladder concern split (`primary-gfc0`) for CriomOS-home: `min/med/max` conflates `user.size` with `behavesAs.edge`. | medium |

---

## §5 — System-specialist work order (carries forward from 92 §4)

After stage-3 (subagents E, F) lands, the cloud-host arc still requires substantial system-specialist work. Numbered in cutover order:

1. **§4.1 Host-set / contained-set / cloud-host-set module split** (cloud-host cutover step 6, the largest single change). Acceptance: byte-identical `toplevel.drvPath` for every existing node-type per fixture, plus fresh closures for `CloudHost` and `Publication`.
2. **§4.2 Native Ghost packaging** (cutover step 8). `pkgs.ghost` in nixpkgs is a name collision (research/77). CriomOS-owned derivation + `modules/nixos/services/ghost.nix`.
3. **§4.3 Full `MicrovmCloudHypervisor` substrate** (cutover step 9). microvm.nix flake input; per-node `microvm@<name>.service`; cloud-hypervisor + virtiofs `/nix/store` share.
4. **§4.4 Goldragon's first Publication node** (cutover step 10). Depends on 2 and 3.

Also pending from stage-1 audits and not in any subagent's scope (carry from 92 §4.5):

- **Concern split of `modules/nixos/metal/default.nix`** (bd `primary-gfc0`).
- **`KnownModel` stringly-typed model dispatch refactor in `metal/default.nix`** (audit 80 finding 2; depends on A's KnownModel landing — done).
- **`disks/preinstalled.nix` typed-enum re-encoding** (audit 80 finding 5).
- **`Editor` / `AiProtocol` / `TextSize` stringly-typed dispatch** in Nix consumers (audit 83 closed §17 unfinished).
- **`unused-inputs` check** (bd `primary-k9kj`).
- **Lojix daemon implementation** (bd `primary-sff`; replacement for lojix-cli per closed §1+§15).

Plus the §4 follow-ups F1, F2, F3, F4, F6, F7, F8, F9 above.

---

## §6 — Suggested order of operations

For the next role picking this up:

1. **Read** `92-cloud-host-arc-system-specialist-handoff.md` (decisions + earlier work order) and this report (where things stand).
2. **Fire subagent E** (§3.1) — small, well-scoped, unblocks everything else. Includes the F5 llm.nix follow-up.
3. **Fire subagent F** (§3.2) in parallel — also small-ish, in horizon-rs. The schema additions are prerequisite for any contained-node work.
4. **Fix F1** (three pre-existing test failures in horizon-rs) — needed for CI-green. Likely one focused subagent.
5. **Apply F2** (sweep CriomOS for now-mis-matching model strings).
6. **Start §5 item 1** — the host-set module split. This is the biggest piece of work; budget multiple sessions.
7. The remaining §5 items can land in any order based on operator priority.

---

## §7 — Operational state at handoff

- **Branches**: `horizon-re-engineering` on horizon-rs, goldragon, CriomOS, CriomOS-test-cluster, CriomOS-home — all advanced and pushed to origin.
- **Primary `main`**: tip carries the renumbered parallel-agent reports (90, 91), cloud-host hand-off (92), four stage-2 subagent reports (84–87), and this report (93).
- **Goldragon datom**: `KnownModel` strings updated (`rock64`→`Rock64`, `"GMKtec EVO-X2"`→`GmktecEvoX2`). No other production changes.
- **Resource posture**: no nix builds run this session; thermal load minimal. Stage-3 subagents inherit the same `--jobs 1` / `nix-instantiate --parse` posture.
- **Working copy on primary**: contains other agents' uncommitted edits (designer/181–200 series, ESSENCE.md, .claude/scheduled_tasks.lock, etc.) — left untouched per the lane discipline. The next role inherits this state; use `jj split` to commit only their scope.

---

## See also

- `~/primary/reports/designer-assistant/77-…md` through `92-…md` — full session output.
- `~/primary/reports/system-assistant/15-handover-2026-05-15.md` — schema-arc handover this session builds on.
- `~/primary/skills/designer.md`, `skills/system-specialist.md` — role contracts.
