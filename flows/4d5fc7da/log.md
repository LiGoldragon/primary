# Flow 4d5fc7da

Design: remember flow 674a4dab (the CriomOS / Lojix / Horizon stack audit)
in depth and bring forward the Lojix redesign it left pending — the
"Deploy request, redesigned" proposal and the three questions awaiting the
psyche's rulings.

## State

Remembering in progress: 674a4dab log, consolidated report, Lojix psyche
acquisition and audit read in the main flow; transcript tail (last model
response, the psyche's last words on Deploy.Host) delegated to a subflow.

## Remembering (in progress)

Read in the main flow: 674a4dab log; reports/criomosStackAudit.md in full
(the seven-plane end-shape, §3 Lojix findings, §5 slices, §7 three questions,
the Deploy.Host appendix and "Deploy request, redesigned"); psycheLojix.md
(partly); e8c4cc61 log and vision/ethosFileAnatomy.md; Vision/nexus.md,
ethos.md, ethosMonolith.md, orchestrate.md, highLevelView.md.
Subflows out: 674a4dab transcript tail (last model response, psyche's last
words on Deploy.Host); current state of the Lojix/Horizon/CriomOS repos at
origin/main since 2026-08-28; all raw psyche on Lojix, deployment and nexus
shape across flows, with a Vision/lojix.md distillation draft.

Where 674a4dab left the Lojix redesign: proposal
`Deploy.Host.{ NodeName Action Option<Revision> Option<Route> }` and
`Deploy.UserEnvironment.{ NodeName UserName Action Option<Revision> }`, every
other field of today's 13 read from the daemon configuration or Horizon; open
for the psyche: (1) the real set and names of actions; (2) route as a
per-deployment choice or a Lojix rule. Question 3 (how much Lojix: keep or cut
the durable store, watch contracts, outbox, transition machinery) unruled.
Lojix distillation proposal (§6) never approved.

## Current state (witnessed via subflow, 2026-08-29; probes: git fetch / rev-parse / log, systemctl, ls /run/lojix)

lojix origin/main still 33b8b6b (no commit since the audit); ByDeployment
`false` at schema_runtime.rs:4187 and the CheckHostKeyMaterial stub both
still there; signal-lojix f614ae1 and meta-signal-lojix 8e0dbe1 unchanged —
Deploy.Host is still the 13-field HostDeployment, and UserEnvironmentDeployment
carries the same 13 minus HostComposition plus UserName. No criomos-core
anywhere under /git. Moved since the audit: goldragon (ClusterProposal →
proposal.datomic, SynchronizerConfig → synchronizer.datomic, 2026-08-29
morning), horizon-rs (ClusterProposal on Datomic 0.5.0; "package Horizon Ethos
map"), CriomOS 16 commits ahead of the working copy, CriomOS-home 12 (Datomic
Chroma config, Orchestrate WireContract 0.26, canonical Home package set).
Working copies: lojix 1 behind, goldragon 3, horizon-rs 3, CriomOS 16,
CriomOS-home 12; the rest at origin/main.
Daemon: lojix-daemon.service running lojix-0.19.2 since 2026-08-23, sockets
/run/lojix/ordinary.sock and owner.sock present; journal shows worker-thread
panics (WireShapeError, src/adapters.rs:539) on 2026-08-28 and 2026-08-29,
process not restarted since 08-23. Cause of the panics unknown.

Remembered: 674a4dab — depth 2 (log, all of criomosStackAudit.md, the
Lojix audit and acquisition, the transcript's tail via subflow: last model
response at line 1058 read). Most relevant: the psyche's only words on the
redesign were "what does the Deploy.Host payload lok like?" (L907) and
"redesign that without any repitition" (L950); the proposal shown at L973 is
the four-field Deploy.Host; the last response left pending "the names of the
deploy actions, route as a per-deployment choice or a Lojix rule, and the
three questions in the report" — none answered. The psyche also corrected
the skill: vision/ holds psyche only, rulings are instructions (L1006).

Remembered (via subflow, psyche gathering): 019ffafe, 01a01bac, 01a02b46,
01a02b4b, 01a02fe5, 01a030b7, 01a03d6e, 01a03eda, 01a048a6, 55d18f4f,
e06e4c07, f426777b, fd301d9a, db97561c, e8c4cc61 — depth 1 (vision files
and logs). Most relevant to Lojix: OS-only; "The interface is lojix and
meta-lojix CLI only"; "CLIs cannot accept any other type of argument than the
typed input object"; "dont do hot fixes" / "use the nix user env only, or OS
redeploy"; LAN for nix paths, domain for activation; "the ipv4 address is
extremely temporal and should not be relied upon"; ".dotos is now considered
stale"; every Nexus keeps its state in Sema, "the nexus and sema ethos arent
designed yet"; "Nexus should be the universal Nexus library ... ethos-zero is
where the daemon should be". No psyche word exists on: the deploy action set,
route as choice or rule, keeping or cutting Lojix's store/watch/outbox
machinery, the Deploy.UserEnvironment shape.

## State (2026-08-29, after remembering)

Brought forward to the psyche: the Lojix anatomy in the redesign (one Nexus,
OS-only, meta socket carries Deploy, ordinary carries Observe; configuration,
Horizon, pipeline, Sema) and three asks: (1) the action set and names —
proposed Activate | Boot | Realize; (2) route as a Lojix rule (heavy copy over
LAN when reachable, activation over the domain) — recommended, versus a
per-deployment Option<Route>; (3) Lojix's Sema anatomy: keep deployment
records, live set, configuration; delete container-lifecycle, watch
contracts, outbox, transition intents, Direct mode, CheckHostKeyMaterial, the
duplicate type family. Distillation proposal for Vision/lojix.md shown
(psyche's words only) — awaiting approval.

## Open

- Naming inconsistency in distilled Vision: Vision/nexus.md says the meta CLI
  is "component-meta"; Vision/orchestrate.md says "meta-orchestrate"; the
  psyche's Lojix words say "meta-lojix". Not raised yet.
- How Lojix finds a node's LAN route without a temporal IPv4 — unknown; a
  LAN domain name from the pan-horizon config is the candidate.
- Questions 1 (criomos-core) and 2 (Horizon's line) of 674a4dab still stand.
- Daemon worker-thread panics (WireShapeError) — cause unknown, not examined.

2026-08-29 — psyche (typed): "looks reasonable" on the brought-forward
redesign, the three asks and the distillation proposal — read as agreement
in direction, not as rulings on the action set, the route rule, the Sema
anatomy, or approval of Vision/lojix.md; explicit word asked for each.
Constraint logged (vision/datom.md): datom has no omittable fields yet — the
request must be written in full; proposed `Source.[ Main  Revision.<rev> ]`
in place of `Option<Revision>`.
Instruction/state: "we still have to get ethos-zero fixed, as it was messed
up last night by a long codex flow" — ethos-zero's repair precedes any
realization of the Lojix ethos files. Known from e8c4cc61's log (claim, not
witnessed here): the Codex flow 01a04a30 ran overnight, invented a
Schema.{0 1 0} Rust-transcript dialect; the corrective prompt
codexCorrection.md (db97561c) was told "Implement it" but never landed.
Light check of ethos-zero's current state dispatched.

ethos-zero state (witnessed via subflow, probes: git fetch/log, grep,
orchestrate 'Observe.Locks', pgrep): ethos-zero origin/main b922afba
(07:19Z), protos bfde3b87 (03:04Z), datomic b670c72d (03:09Z) — all from the
overnight Codex flow, nothing after 11:30Z; the correction in
flows/db97561c/reports/codexCorrection.md (sections: Standing, direction
chain, Library file, Nexus shape, slices, references) has not landed
anywhere. `Schema` present in ethos-zero.ethos, src/lib.rs,
tests/file_contract.rs (not read). No `nexus` repository exists. Locks 135/136
of 01a04a30 gone; only 333 (01a04e75, listener) and 19 (01a0433a) held. No
ethos-zero process running. Working copies of ethos-zero, protos, datomic
behind origin/main. Repair not dispatched from this flow — the psyche's call.
