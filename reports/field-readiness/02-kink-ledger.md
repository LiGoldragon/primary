# Field Readiness — 02: Ranked Kink Ledger (2026-07-02)

Synthesis of the four Phase 1-2 recon reports (10-13, this directory) for the
sustained Fable 5 integration-testing session, especially VM-cluster operation
on prometheus. Parent framing: `reports/persona-system-audit/00-README.md`.
Every claim below is attributed to its source report; this synthesis did no
firsthand recon. Ranking = blast radius on a sustained multi-agent session ×
likelihood of being hit. Beads were opened this session for every
`bead-for-Fable5` entry; cheap-fix items are listed as the fix-list for the
next phase, not beaded.

## HEADLINE VERDICT

The field is READY-WITH-KINKS. Everything load-bearing was witnessed working:
prometheus boots real KVM VM clusters and passed a two-VM engine test GREEN in
~100s (report 10), every core component builds warm in 6-110s through the
remote builder (report 11), the minimal runnable whole comes up and exchanges
real origin-stamped mail (report 12), and every constant-use tool answers in
milliseconds (report 13). But four kinks sit directly in the sustained
session's path: the whole-engine gate (persona-dev-stack + the nix-built
8-component topology checks) is dead at instantiation on a stale fenix pin;
mixed-vintage binaries and cross-repo contract lock drift fail silently at the
wire with a misleading symptom — it was the first thing the run-recon hit;
the entire build/cache/VM/deploy field hangs on prometheus alone; and no
continuous-testing entry point exists, so regressions accumulate silently.
Rank 1-2 should be fixed before the session starts; rank 3-4 early in it; the
rest are pre-emptable with the cheap-fix list below.

## RANKED KINK TABLE

Classification: BEAD = bead-for-Fable5 (id given); CHEAP = cheap-fix-now (see
fix-list). Rank annotation is blast × likelihood on the sustained session.

| # | Kink | Merged from | Blast × likelihood | Class | Bead / cheap | Evidence |
|---|------|-------------|--------------------|-------|--------------|----------|
| 1 | Rust toolchain pin rot: persona's stale fenix rust-stable FOD kills the whole-engine gate now; 18/28 repos carry their own aging pin (harness next) | 11-K1 + 11-K2 | total (primary loop target dead at instantiation) × certain (witnessed twice; latent per-repo) | BEAD | primary-j5j2 (bump, P1); primary-95fm (convergence, P2) | 11: dry-run hash mismatch on channel-rust-stable.toml.drv for persona-dev-stack + nix-built-topology check; persona/flake.nix:85, fenix lock 2026-05-05; pin grep across 28 flakes |
| 2 | Build-vintage wire skew: mixed-vintage binaries + cross-repo contract lock drift (signal-router 277bd153 vs 289c7de4, signal-harness 959b62bd vs 0727beb7) fail silently at the frame with a misleading typed symptom | 12-K1 + 12-K2 + 11-K9 (audit 20 obstacle 1) | whole fabric, misleading diagnosis × high (hit on the recon's first bring-up attempt; contracts append wire fields, e.g. d212ea8) | BEAD + CHEAP | primary-mddx (fingerprint, P2); primary-w46v (lock-sync sweep, P2); cheap: preflight rebuild script + rev-pin diff check script | 12: rkyv decode failure surfacing as "router socket unreachable", fail→rebuild→pass on identical sources; lock diffs measured |
| 3 | prometheus is a quadruple SPOF: only remote builder, only project binary cache, only kvm/nixos-test host, and the lojix deploy-experiment target; local fallback is max-jobs=1/cores=2 | 11-K3 + 13-K5 (+10 context) | every build loop on every machine × moderate (deploy experiments to prometheus are exactly the session's business) | BEAD + CHEAP | primary-oeng (second builder/substituter, P1); cheap habit: dry-run heavy builds first | 11/13: /etc/nix/machines single line; cache = same host; nix.conf; audit 24 deploy state |
| 4 | No continuous-testing entry point: no CI, no timers; testing is entirely pull-based and the harness e2e skips by default | 13-K8 (+ audit 23 §4) | regressions accumulate silently — the session's whole purpose × certain (structural) | BEAD | primary-vp6d (P1); related keystone: primary-iy51.12 | 13: workflows glob (only kameo/whisrs), systemctl list-timers, cluster flake grep |
| 5 | Channel adjudication is bootstrap-only: mind answers NotInPrototypeScope, router parks unknowns in an unwired pull-only outbox; grants exist only via the bootstrap rkyv | 12-K3 + 12-stubs 1-2 (+ audit 22) | every topology must be pre-declared; no runtime channel changes × certain beyond the pre-granted pair | BEAD + CHEAP interim | primary-5k4o (P2); cheap: exhaustive bootstrap grants for the planned actor set | 12: mind/src/actors/dispatch.rs:143-145; router_write_bootstrap.rs:102-108 doc comment; bring-up worked only because grants were pre-declared |
| 6 | Persona readiness never leaves Starting under fixture launch: all 8 components Running, readiness stuck | 12-K4 | Ready-gated sessions wait forever; supervision green unusable as health gate × high for fixture scaffolding | BEAD (diagnosis) | primary-6yur (P2) | 12: witnessed EngineStatusReport (0 Starting ...) after ~10s; cause not established |
| 7 | Declared persistent VM guest is network-dark and un-enterable: guest config emits hostname+stateVersion only; IPv4 /32 route hardcoded onto IPv6 nodeIp; no sshd | 10-K1 + 10-K6 | the whole persistent-reachable-test-VM surface (boot-only today) × certain (witnessed); runNixOSTest path unaffected and GREEN | BEAD (existing) | primary-dw95 (P1, evidence note added this session); shaped by open decision (e) | 10: boot to Multi-User <25s; 100% ping loss, 0-packet tcpdump, route 5::/32 dev vmt0; test-vm-host.nix read |
| 8 | Harness is un-configurable outside cargo tests (no harness-write-configuration binary) and the chat-loop components have no deploy modules | 12-K6 (+ audit 24) | no scriptable/deployable bring-up of the interactive loop × certain when deploying | BEAD | primary-zi99 (P2) | 12: harness Cargo.toml [[bin]] list read; all other fabric components have writers |
| 9 | Model-backed reply leg unwitnessed: pi RPC receipt is prompt acceptance only; no LLM server running; no committed real-daemon full-loop test | 12-K7 | the demo goal (agent B replies) — last leg of the minimal whole × certain until built | BEAD | primary-uhul (P2) | 12: pi_rpc_live ok (0.72s); process/port scan negative |
| 10 | Spirit field-truth skew: dirty 8-file checkout on criome-authorization-push; deployed daemon (2d uptime) likely pre-v11; doctrine cites dead record ids (vcin) | 11-K7 + 13-K3 | most active engine component builds from unpushed state; source-read wire shapes vs lagging daemon = mid-flow rejections × medium-certain | BEAD | primary-sos8 (P2); deploy decision already tracked: primary-6kst / primary-yluj; archive-id set: primary-6obv.13; disposition = open decision (b) | 11: git status read-only; 13: daemon etime, checkout head, Lookup vcin → not found |
| 11 | Spirit skill-vs-deployed drift: (Count) rejected as unknown variant; single-word bracket text rejected as non-canonical | 13-K2 | retry loops + misread-as-blocker for every fresh agent × high (bit the recon twice on first attempts) | BEAD | primary-qnaa (P2, skill-editor scope) | 13: both error outputs witnessed, 3ms each |
| 12 | mind vendors 8 ssh:// git deps with plain crane: cache-miss vendoring needs interactive SSH auth; hides while fully cached | 11-K4 | first mind source edit hits it; fails hermetic/CI/fresh contexts × high if mind is touched | BEAD | primary-sech (P3) | 11: grep counts in mind Cargo.toml/Cargo.lock; bare craneLib, no [patch] |
| 13 | VM checks cannot be remote-scheduled from ouranos: builder line lacks nixos-test; ouranos forbidden to fire QEMU | 10-K2 | every VM test needs an ssh wrap; confusing scheduling failure on first naive nix build × certain first attempt | BEAD (decision-gated) | primary-vcqx (P3, blocked-on-psyche); open decision (a) | 10: cat /etc/nix/machines; run-criome-auth-on-prometheus script doctrine |
| 14 | NotBuiltYet stub surface: no daemon live-reconfigurable over meta; system + upgrade near-total skeletons behind healthy sockets; 22 path-cited operation stubs | 12 §NOTBUILTYET | bounds what the session can test (typed, not silent); readiness passes while function is absent × certain structural | BEAD | primary-afh8 (P3); adjudication portion carried by primary-5k4o | 12: 22 entries, all source-verified this session (appendix below) |
| 15 | SUN_LEN: unix socket paths >~104 bytes fail bind; the session scratchpad path is already too deep | 12-K5 | confusing first-contact failure for every daemon on deep roots × certain on generated deep paths | CHEAP | fix-list 4 (short-run-root convention); triad-runtime dirfd lift deferred unless the convention proves insufficient | 12: exact bind error witnessed on router and message |
| 16 | bd cold-start compaction stall (18.2s) + embedded-dolt single-writer lock under concurrent agents | 13-K1 | ~20s stall misread as hang; outright failure on lock collision × high (once per cold DB; medium for lock) | CHEAP | fix-list 6 (pre-warm, sequential use, retry-on-lock) | 13: time bd stats 18.220s with conjoin logs; bd ready 0.806s after |
| 17 | primary main push contention between concurrent agents + 20+ stale bookmarks and 3 stale workspaces | 13-K4 | push-rejected mid-flow halts by design × medium-high in a multi-agent session | CHEAP | fix-list 7 (small-unit push cadence, escape hatch, litter cleanup) | 13: op log push 3 min before probe; bookmark/workspace listings |
| 18 | forge Nix-invisible (devShells only) and mentci flakeless: sweeps silently skip them; "all repos build" vacuous | 11-K6 | gates lie about the build-authorization component × certain structural, low immediate blast | BEAD + CHEAP | primary-0q0k (forge, P3); cheap: mentci README note | 11: nix flake show forge; mentci ls |
| 19 | Malformed CriomOS flake registry on hosts: entries lack owner/repo; every flake op warns; all registry aliases dead | 10-K3 | noise on every nix call + alias-dependent tooling broken × certain every invocation, low blast | BEAD | primary-ij68 (P3, bug) | 10: warning witnessed; registry file head read |
| 20 | CriomOS bare eval throws by design (no-system stub); the working --override-input recipe is undocumented | 11-K5 | minutes lost per naive attempt; OS misread as unbuildable × certain for fresh workers | CHEAP | fix-list 8 (document the witnessed recipe) | 11: throw witnessed; override eval 47s/26 drvs witnessed |
| 21 | Missing built binaries: terminal-cell, system, introspect, upgrade have no target dir — real 8-component topology cannot start | 12-K8 | blocks the real-daemon topology until built × certain, trivially fixed | CHEAP | fix-list 5 (cargo build; terminal-cell is the real one) | 12: target-dir scan |
| 22 | Orphan demo daemons from Jun 30-Jul 1 squatting /tmp sandboxes (criome, mentci, introspect; one binary's target dir gone); tmpfiles reaps in 10d | 12-K9 + 13-K7 | socket/state collisions + confusing ps for the next session × low-medium | CHEAP (owner-confirmed) | fix-list 13; open decision (c) | 12: ps scan; 13: pgrep/ss/tmpfiles rule |
| 23 | Spirit write path depends on a live LLM provider + API key via the guardian | 13-K6 | Record blocked mid-session on provider outage/key expiry × low-medium | CHEAP | fix-list 11 (session-start guardian/provider probe) | 13: provider.rs/nexus.rs source-read; write path not exercised |
| 24 | Full flake check on wide repos is a loop-killer (router ~44 / mind ~60 / persona ~120 checks); whole-engine sweeps only survive as dry-run-first + background + logs-on-disk | 11-K8 + 11-K10 | tens of minutes per naive iteration; worker context death × high without the practice | CHEAP | fix-list 10 (narrow-check-first; sweep method) | 11: check counts; report-25 stall analysis |
| 25 | Push-first VM iteration loop: prometheus only sees pushed github: refs; GitHub becomes a hard inner-loop dependency | 10-K5 | latency + forced commit granularity × constant but tolerable | ACCEPT / watch | open decision (d); bead only if latency bites | 10: reproduce-script requirement; witnessed mechanics |
| 26 | microvm -l inventory is blind on CriomOS hosts (assumes /etc/nixos flake) | 10-K4 | naive inventory reports "no VMs" × certain when used, trivial | CHEAP | fix-list 12 (doc line: systemctl + /var/lib/microvms) | 10: microvm -l empty vs ls /var/lib/microvms |

## CHEAP-FIX-NOW LIST (fix-list for the next phase — not beaded)

1. Bring-up preflight script: `cargo build` in every participating repo before
   spawning any daemon (12-K1a; interim guard until primary-mddx lands).
2. Contract rev-pin diff check script across repo Cargo.locks — the diff was
   one awk line during recon (12-K2; companion to primary-w46v).
3. Interim adjudication mitigation: generate bootstrap grants exhaustively for
   the planned actor set before router start (12-K3; until primary-5k4o).
4. Short-run-root convention for daemon sandboxes (e.g. `/tmp/<lane>/`) to stay
   under SUN_LEN; never nest sockets under the session scratchpad (12-K5).
5. `cargo build` terminal-cell (real code, needed for real PTY delivery);
   system/introspect optionally (status-only skeletons) (12-K8).
6. bd pre-warm (`bd stats`) at session start; keep bd usage sequential;
   retry-on-lock (13-K1).
7. Small-unit commit-and-push cadence on primary main; on push-reject follow
   the version-control escape hatch; clean the 20+ stale `operator/report-*`
   bookmarks and 3 stale jj workspaces (13-K4).
8. Document the witnessed CriomOS whole-OS eval recipe (`--override-input`
   with lojix generated-inputs) in CriomOS agent docs (11-K5).
9. mentci README note: deliberately flakeless, packaged via
   CriomOS-home#mentci (11-K6b).
10. Loop practice: build the one check that proves the edit
    (`nix build .#checks.x86_64-linux.<check>`); full `nix flake check` only
    pre-commit; whole-engine sweeps as dry-run-first + background builds +
    logs-on-disk (11-K8, 11-K10).
11. Session-start guardian/LLM-provider liveness probe before relying on
    Spirit Record (13-K6).
12. Operating doctrine line: VM inventory on CriomOS hosts is
    `systemctl` + `/var/lib/microvms`, not `microvm -l` (10-K4).
13. Orphan demo daemon cleanup (kill tmux session
    `criome-mentci-spirit-demo-20260701-150210`, inventory + remove /tmp
    sandboxes) — pending open decision (c) (12-K9, 13-K7).
14. Habit: `nix build --dry-run` before heavy builds to see the miss surface
    and spot prometheus degradation early (13-K5 cheap half).

## OPEN DECISIONS FOR THE PSYCHE (recorded, not resolved)

(a) Should the prometheus builder line on ouranos gain `nixos-test` so VM
checks schedule transparently via plain `nix build`, or is its absence
deliberate doctrine keeping heavy KVM runs an explicit ssh-run act?
Tradeoff: frictionless VM iteration vs deliberate, visible scheduling of
heavyweight tests. (10-K2; gates primary-vcqx.)

(b) Commit or discard the 8-file dirty spirit checkout on
`criome-authorization-push`? Tradeoff: preserving in-flight authorization work
vs restoring build-from-committed-truth for the engine's most active
component. (11-K7; gates part of primary-sos8.)

(c) May the leftover demo daemons and /tmp sandboxes from the Jun 30-Jul 1
demos be killed and removed, or do they hold state worth keeping? Tradeoff:
field hygiene for the next session vs losing demo state. (12-K9, 13-K7; gates
fix-list 13.)

(d) Accept GitHub as a hard availability dependency of the VM-test inner loop
(push-first doctrine), or sanction a `nix copy` derivation-shipping path to
prometheus? Tradeoff: pushed-refs doctrine purity vs inner-loop latency and
availability. (10-K5.)

(e) Complete the declared persistent-guest surface (guest network + sshd per
primary-dw95), or retire it in favor of runNixOSTest-only VM operation?
Tradeoff: a persistent, enterable test VM vs maintaining a second, heavyweight
VM path that requires cluster-facts changes and host redeploys per guest.
(10-K1, 10-K6; shapes primary-dw95.)

## APPENDIX — THE 22-ENTRY NOTBUILTYET SURFACE

The full enumerated, path-cited stub surface (working plane: mind
adjudication/channel-list, system near-total skeleton, harness non-delivery
ops, upgrade near-total skeleton, router/message scope guards, persona
manager rejections; meta plane: live reconfiguration dead fabric-wide) lives
in `reports/field-readiness/12-run-and-assembly.md` § "NOTBUILTYET / STUB
SURFACE". Tracker carrier: primary-afh8 (triage/build-out), with the
adjudication hole carried separately by primary-5k4o. Sessions must probe
operations, not socket liveness: supervision readiness passes while function
is absent.
