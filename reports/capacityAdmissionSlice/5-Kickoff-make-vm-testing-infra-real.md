# Kickoff: Make the VM-Testing Infra Real

Seed context for a fresh session. Boot from `skills/skills.nota` as usual; this
file is the only carry-over read. Keep it small — pull detail from the locators
below on demand, do not inline them.

## Psyche intent (durable — stated by the human this session)

Downstream drive (NOT this session's target, the motivation behind it) —
VM-host capacity admission:

- A `VmHost` declares how much it can hold (RAM / disk / cores, host-total); the
  system refuses to place guests that together exceed it.
- Enforcement is RUNTIME ONLY. Static / author-time is the wrong model because
  VMs stop and start and test clusters deploy ad-hoc.
- Mechanism is phase-2 lojix: all inter-system action flows through each
  component's own lojix daemon; the local daemon is authoritative for local
  state; a request goes daemon -> router -> daemon; this needs criome auth
  propagated so criome runs on every component.
- Finish line is the full stack: criome auth everywhere -> daemon mesh -> the
  capacity check on top.
- Method: a working vertical slice first (thin, end-to-end, per
  `skills/bead-weaver.md` traceable-bullet), then real features.
- The slice must span two or more REAL hosts. Loopback is not a valid proof.
- VM tests run on a host DESIGNATED for VM testing, never the orchestrator's own
  host.

THIS SESSION'S TARGET: make the vm-testing infrastructure real first — a
trustworthy multi-host VM test that actually witnesses boot and activation, runs
on a designated host, and cannot pass hollow. Everything above waits on it.

## Why now (adversarially checked last session — but re-verify, trust nothing here)

The existing 2-node test `.#checks.x86_64-linux.lojix-deploy-smoke`
(`CriomOS-test-cluster/lib/mkDeployTest.nix`) is NOT a solid baseline:

- Proves only eval -> closure-copy -> profile-generation-set. It does NOT
  witness boot or activation: `installBootLoader` is a no-op, `bootctl` is a
  no-op shim, it deploys `Boot` not `Switch`, and the production closure
  (clavifaber) is stubbed `exit 0`.
- Satisfiable by a CACHE HIT: the check output is already in the store, so a
  plain `nix build` boots zero VMs and still prints GREEN. Only `--rebuild`
  forces a real boot.
- Ran on the WRONG host: `INTENT.md:89-93` restricts these checks to a
  designated VM-testing host and explicitly rejects "it has KVM so I ran it";
  last session ran them on ouranos, the orchestrator laptop. Designated VmHost
  appears to be prometheus.

## Open blocker for the psyche

The authoritative designated-VM-test-host list lives in the goldragon
cluster-facts repo, which is **public** (`github:LiGoldragon/goldragon`) and not
authorization-gated — read it directly. Only the SOPS-encrypted secret values it
references are protected, not the data or the host designation, so no psyche
authorization is needed to open it. The host name is therefore readable now.
[Corrected: an earlier draft of this report miscalled goldragon a "private …
off-limits" repo; that was wrong — the repo is public.]

## Locators (detail on demand)

- `reports/capacityAdmissionSlice/4-Audit-adversarial-reaudit-deploy-smoke-green.md`
  — adversarial teardown of the GREEN; the load-bearing read.
- `reports/capacityAdmissionSlice/2-Audit-vmtest-harness-two-node-substrate-feasibility.md`
  — where the harness actually lives and what is vapor.
- `reports/capacityAdmissionSlice/1-Design-capacity-admission-vertical-slice.md`
  — the slice design (downstream).
- `reports/lojixPhase2SubstrateStatus/1-lojix-phase2-substrate-status.md`
  — criome auth and inter-daemon routing are both net-new in code.
- `reports/vmhostCapacityGrounding/1-*` and `2-*` — capacity data foundation and
  ledger design (downstream).

## Discipline (already in auto-memory)

Verify, don't trust: brief workers for DISPROOF, not verdicts; refute every
load-bearing claim with an independent pass; a thing named X is not X until its
behavior says so. The old "roles / locks" orchestration framing in older reports
is DEAD — ignore it. Open option, not yet done: encode this rule into the
intent-led-orchestration skill.
