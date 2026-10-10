# Receipt: stale Orchestrate lock release, 2026-09-25/26

Source claim: 88475f's `flows/88475f/witnesses/24-stale-reap-2026-09-25.md` — 24 stale messenger-clj
routes retired; 8 Orchestrate locks left untouched, held by 5 of the retired IDs.

Protocol followed: `stale-lock` skill. For each lock: `orchestrate 'Observe.Locks'` record, holder
liveness re-check (`hm-send` to holder, `hm-list`, no live process/pane per witness), successor-claim
grep of `flows/*/log.md`, uncommitted-work check under the lock's paths, then
`orchestrate 'Release.<id>'`.

## Holder liveness re-check (this session)

- `FLOW_ID=da88cf hm-list` — none of eb7bae, 6db4fe, 2c61af, 6fb948, c88918 appear (no live rows).
- `FLOW_ID=da88cf hm-send <id> "stale-lock check"` for each of the 5 holders — all five returned
  `messenger-clj: Retired: <id> by /home/li/primary/flows/88475f/witnesses/24-stale-reap-2026-09-25.md`.
  This is a stronger signal than the skill's baseline "Held" case: the route itself no longer exists,
  so no live pane can ever answer it.
- Cross-checked against the witness table: all five (eb7bae, 6db4fe, 2c61af, 6fb948, c88918) are
  listed among the 24 with pane state "pane gone" or "exists, no agent", none a current seat, none
  matching a live process in the witness's `ps aux` scan.

## Successor-claim grep (flows/*/log.md, last two days of commits)

Grepped each holder ID across all `flows/*/log.md` and read context in the recently-touched logs
(88475f, b7da5d, 504461, 38de5b, da88cf, 752e0f, e51411, 00f95a, 5f38bc, d8df70, 836818). Found one
role-succession statement — `flows/b7da5d/log.md:3`: "GPT-6 Sol, Medium. Successor of Field Medium
9ddcbc and eb7bae; both ended and will not be resumed." — which confirms eb7bae's end rather than
claiming its locked paths. Also grepped each lock's specific path fragment
(agent-intercom-cleanup, materialization-20260924, field-world-6db4fe, Curriculum/roles.datom,
flow-message.md, vm-testing, mentci-web, refresh-round-20260922, reap-flow) across all logs: no
live flow claims ownership or successorship of any of these specific paths/work items.

## Uncommitted-work check under lock paths

- `field-medium-eb7bae-agent-intercom-cleanup` (git worktree): clean.
- `flows/eb7bae/materialization-20260924`: not its own git root; no changes under this path in
  primary's dirty set.
- `field-world-6db4fe` (git worktree): clean.
- `Curriculum/roles.datom`: clean.
- `Curriculum/skills/flow-message.md`: path does not exist.
- `/var/lib/microvms/vm-testing`: path does not exist.
- `mentci-web/mind-medium-mentci-web-2c61af`: not a git repository (plain workspace dir).
- `flows/03e825/refresh-round-20260922`: not its own git root; no changes under this path in
  primary's dirty set.
- `tools/reap-flow`, `tools/reap-flow.test.py`: tracked in primary, no uncommitted changes.

No uncommitted work found under any lock path. Nothing committed (none needed; task also said not
to commit this receipt work).

## Locks released

| id   | name                                    | holder | paths                                                                 | reason                                                                                     | reply |
|------|-----------------------------------------|--------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-------|
| 4964 | AgentIntercomCleanupDeclarativeEb7bae   | eb7bae | field-medium-eb7bae-agent-intercom-cleanup/modules/home/profiles/min/agent-intercom.nix; .../checks/agent-intercom/default.nix | Declare packaged Agent Intercom cleanup timer and prove obsolete mutable path absent | Released |
| 4928 | PrometheusFreshMaterialization          | eb7bae | flows/eb7bae/materialization-20260924                                   | Fresh pinned Lojix materialization and immutable deployment evidence                         | Released |
| 4285 | FieldWorldPresentation6db4fe            | 6db4fe | field-world-6db4fe/flows/6db4fe/reports/state-of-field-20260921         | Measured Field presentation, data and printable deck                                        | Released |
| 3825 | FlowMessageCurriculumAuthored           | 6db4fe | Curriculum/roles.datom; Curriculum/skills/flow-message.md               | Own FlowMessage operational skill and authored role composition data pending final API      | Released |
| 4373 | PrometheusVmTesting6db4fe               | 6db4fe | /var/lib/microvms/vm-testing                                            | Own only Prometheus existing vm-testing guest process lifecycle for bounded Flow Message VM experiment | Released |
| 4416 | MindMediumMentciWeb2c61af               | 2c61af | mentci-web/mind-medium-mentci-web-2c61af                                | mentci-web-stage-two-isolated-workspace                                                     | Released |
| 4639 | FieldHighRefreshController              | 6fb948 | flows/03e825/refresh-round-20260922                                     | Accepted successor controller reservation after explicit 03e825 release                     | Released |
| 4739 | ReapFlowEvidenceGates                   | c88918 | tools/reap-flow; tools/reap-flow.test.py                                | Require per-flow native Herdr continuity evidence before archival                            | Released |

All 8 released; each `orchestrate 'Release.<id>'` call returned `Released.{...}` with the full lock
record echoed back. No locks were kept back. No transcript touched. No paths committed by this
receipt.

## 2026-09-26: 753e69's four remaining locks (horizon-rs USB-gateway line)

Holder `753e69` (Field Sol/Medium): not in `hm-list` (absent, not STALE-listed); `hm-send 753e69` returned typed `Retired: 753e69 by /home/li/primary/flows/753e69/reports/self-refresh-transfer-2026-09-23.md` (self-refresh to successor `eb7bae` on 2026-09-23, also absent from `hm-list` and reported stale elsewhere, flows/38de5b/log.md:219). Pane `wQ:pA` labeled "Field Medium 753e69" exists but shows `agent_status:"unknown"`, no live agent binding — the same inert legacy endpoint (`messaging-build/wQ:pA/term_65c0046ddcf0a54`) the retirement report names as vacated. No live flow claims succession on these lock paths: `grep -r 753e69 flows/*/log.md` across the last 3 days finds only retirement/gap notices (e.g. da88cf log 09-25/09-26, 38de5b log, 836818 log), none claiming the paths. Main flow (da88cf) has ruled the horizon-rs `b45d6ad` line abandoned.

Checked out both lock paths with `jj status`: `lojix/horizon-contract-repin-8565e8` and `signal-lojix/usb-gateway-753e69` both report "The working copy has no changes" — nothing unlanded to preserve beyond the abandoned line already ruled on.

Released via `Observe.Locks` then `Release.<id>`, all `753e69`:
- 4051 `SignalLojixHorizon37416Migration` — signal-lojix/usb-gateway-753e69 Cargo.toml/lock, ethos/signal.ethos, generated/signal.rs, tests/generated_contract.rs
- 4062 `LojixUsbGatewaySignalCompatibility` — lojix/horizon-contract-repin-8565e8/clients/ordinary/Cargo.toml
- 4070 `SignalLojixHorizonWireDto` — signal-lojix/usb-gateway-753e69 horizon_wire.rs, lib.rs, tests/horizon_wire_contract.rs
- 4164 `SignalLojixHorizonWireArchiveFix` — signal-lojix/usb-gateway-753e69/src/horizon_wire_types.rs

All returned typed `Released.{...}` replies. No locks kept; 753e69 now holds none.

## Flow 542442 — 24 Orchestrate locks — 2026-09-26

Holder liveness: 542442 absent from `hm-list` (not bound; no STALE row either — never/no-longer registered). `FLOW_ID=da88cf hm-send 542442 ...` returned `Held.{ 542442 RepairRequired ... candidates=[] }` — no live route. No matching process (`ps aux`) and no pane. Corroborated by flows/836818/log.md:94 ("542442 (Goldragon usbIpv4Gateway) has no live route and a held attempt") and da88cf/log.md:152 ("542442 not live but holding ~25 locks"). No live flow claims succession on these paths: flows/542442/log.md tail (through the 07:21:49 UTC 2026-09-06 checkpoint) names no successor and records no terminal/retirement state; grep of flows/*/log.md in the last 3 days for "542442" turns up only observational mentions (da88cf, 836818, 38de5b logging the gap/dispatch), none claiming ownership of these 24 paths. (38de5b/log.md:219-223 shows a prior, disjoint stale-lock release of locks 853/854/855 for the same flow — separate lock IDs, already closed.)

Uncommitted work found (not touched): `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/generic-nodes-fixtures-542442` has an untracked addition `result` (jj status: `A result`, empty diff — looks like a Nix build-result symlink, not content). All other eleven checked worktrees report "The working copy has no changes." The two `/home/li/primary/flows/542442/{reports,witnesses}/...` paths (locks 914, 940) are clean in primary.

Released (all 24, by ID): 937, 911, 925, 850, 902, 905, 898, 856, 910, 846, 900, 907, 890, 903, 851, 914, 847, 844, 845, 940, 870, 869, 908, 868. Each returned a typed `Released.{...}` reply matching its Lock record.

Kept: none.
