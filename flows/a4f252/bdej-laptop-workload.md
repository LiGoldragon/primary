# bdej — Ouranos workload and Prometheus offload

2026-11-18, local CST (UTC−06). Field upkeep a4f252. This is an observation report, not a Flow repair or a new test admission.

## Established restart cause

At **18:42:03**, the kernel killed Flow daemon **3574620** for **cgroup-local out-of-memory**, not a demonstrated whole-host shortage. Its user unit `flow-nexus-0550.service` had `MemoryMax=3G`, `MemorySwapMax=0`, `Restart=on-failure`, `RestartSec=100ms`. The kernel records usage/limit **3145728kB**, `CONSTRAINT_MEMCG`, and the daemon's anonymous RSS **3042580kB**. Systemd records `oom-kill`, SIGKILL, a **3G peak**, and automatic restart counter **1**. New main PID **2476438** started 18:42:03; service became ready 18:42:04.

ExecStart is `/nix/store/6bkg7sg7z5g80wdhqnz3swzg48xxrpha-flow-workspace-0.59.3/bin/flow-nexus-daemon main`. The old unit description still says 0.55.0; that label is not the running package version. Source binding in `flows/696380/0593-deploy-receipt.md`: Flow **5130439938767547a5bd3935b1649508a7da7e8e**.

The previous invocation consumed **1h 8min 51.349s CPU over 15h 43min 20.028s**. That unit accounting includes its cgroup, not a pure daemon-only profile. Kernel task records show the main daemon itself held most of the memory at OOM; the reason it accumulated that memory remains unknown.

## CPU: observation, source reading, unknown cause

At about18:48, `ps` reported the new daemon at **26.7% lifetime CPU over398s**. This is an elapsed-lifetime average, not an event-free idle measurement. Later unit properties showed CPUUsageNSec148891800000, MemoryCurrent1483776000, MemoryPeak1559236608 and225 cgroup tasks; cgroup tasks are not all threads of the main process.

The retained18:42:03–18:51:00 journal contains **190 admitted messages** and **227 ArchiveUnconfigured warnings**. Thus the measured period had substantial actual input; it does not establish “nothing happens.” An individual thread snapshot mostly found blocking futex/socket/pipe waits; that single cut does not explain accumulated CPU.

Exact-source `crates/flow-nexus/src/reminding.rs:175–206` blocks on reminder-store announcements or the next due time. Each reminder pass also attempts archive retirement; lines233–240 emit the observed warning when archive configuration is absent and closed generations remain. This explains the warning's meaning, **not the CPU or memory-growth cause**. An event churn, expensive store processing, and a repeatedly due reminder are possibilities requiring distinguishing evidence; none is established here. No profiler was attached, and no daemon/configuration/state change was made. Existing owner Mind flowNexus Sol was asked for any already-held exact-source explanation, with its urgent driver correction retaining priority.

## Today's work: evidenced kinds and placement

This inventory distinguishes executed work from proposed commands and local clients from their remote children. It is not a complete process-accounting history: no retained host-wide exec accounting was established. Missing journal entries do not prove an operation never ran.

| Kind | Evidence / actual placement | Prometheus route and disposition |
|---|---|---|
| Native integration matrix / private service bootstrap | **Local Ouranos execution established.** Eight failed proposal2 units, plus one pre-unit refusal, are retained in `flows/2e9c12/order0601-native-evidence.md` and Core's reset-custody receipt. Early cuts failed before native turns; later cuts did launch real private native sessions. The full matrix did not pass. | This is host-bound integration, not just CPU tests: private paths, unit/cgroup custody, endpoint/process identity, production before/after captures and installed harness bindings are in its contract. Moving its compile/synthetic preparation is straightforward; moving the actual native matrix needs a new builder-bound manifest/identity/custody admission. No active attempt was moved or replayed. |
| Driver synthetic tests / CLI codec checks | Mind core5sic reports bounded subsecond local synthetics, distinct from the native matrix. The Field report also retains finite local pinned-CLI no-socket decoding. These are local work but not established as today's sustained heavy load. | Push the immutable driver revision or copy unpublished source once to builder scratch; run the same suite there and return its log. No currently running synthetic job was found to migrate. No duplicate suite was started. |
| Rust cargo/clippy/tests and whole gates | Mind core5sic identifies known Flow clippy/tests/whole gates as **Prometheus**, not laptop work. Deployment receipt independently records one Prometheus whole Home gate08:43:08–08:44:33Z,98 EVAL+98 BUILD success. The immutable codec compile attempt was also remote and stopped at disabled cargo before compilation. | Already remote. Keep immutable revision/toolchain/input identity and reuse derivations. Do not infer local compilation from local SSH/client output. No active cargo process was found in the current process cut. |
| Nix evaluation | No actual local heavy `nix eval` established by the records inspected so far. The retired m6il packet was preparation only and never executed here. Predecessor reports stage original Ouranos inputs for the builder; that is not evidence of a local evaluator. No matching current evaluator process was found. | Pure pinned evaluation goes to Prometheus via SSH; whole-system evaluation goes through Lojix. Preserve exact staged input identities and remote accessibility. Host-local generated paths cannot simply be substituted. Existing builder configuration is `ssh-ng://nix-ssh@prometheus.goldragon.criome`. Further owner inventory requested. |
| Zoekt indexing | **Already offloaded.** Installed script `/nix/store/n8vqvkjfl23d79gb3fl5yxc2yflnz9im-zoekt-index-offload/bin/zoekt-index-offload` sets indexing_host=prometheus and executes the snapshot indexer there over SSH, then rsyncs shards back. Today's local journal has shard-completion lines relayed by this local offload client; those lines do not prove local indexing CPU. Its drain process has2s lifetime CPU over6+days. | Existing event-driven queue sends snapshots/indexing to Prometheus. Local git snapshot creation, transport and shard installation remain local. No migration needed or duplicate indexer started. |
| Harness/client/background context work | Current local snapshot shows Claude sessions, week-old Codex app-server, Herdr and eight bb codex-context-watch processes. Each watcher has roughly2.5min lifetime CPU over4.5h. These are distinct from cargo/eval/build. | Moving whole harnesses or watchers reading local transcripts requires locality/event/endpoint design. No service was moved, killed or restarted. This report does not ascribe their resource use to a specific defect. |

**Plain moves made:** no active misplaced cargo/eval/indexing job was identified to move safely; indexing and known heavy source gates are already remote. No workload was rerun merely to obtain offload evidence. Native integration and production harness relocation require design/admission and were left intact.

## Failed-unit cleanup completed

Field core Resultag19 explicitly confirmed copied evidence and authorized reset-failed **only** for the eight exact names in `/tmp/proposal2-reset-custody-2e9e53.l5j2rk46/receipt.md`. I read that receipt and ran one literal-name `systemctl --user reset-failed` for:

- proposal2-2e9c12-c7d52c2ffd.service
- proposal2-2e9c12-final-e25b813d52.service
- proposal2-2e9c12-fresh-74bba46ea2.service
- proposal2-2e9c12-review600-fafe213686.service
- proposal2-09456769.service
- proposal2-2b0256fb.service
- proposal2-321fbbbd.service
- proposal2-42bb5c51.service

Command exited **0**. Afterwards only unrelated `context-skills.service` remained failed. No stop/start/restart, evidence removal, account action or test retry occurred. Resetting unit failure state does not change the retained failed test outcomes.

## Evidence and remaining work

Raw observation directory: `/tmp/bdej-upkeep-a4f252.SnAO6cXk/`: `kernel-oom.log`, `flow-restart.log`, `flow-post-restart.log`, `flow-unit.txt`, `flow-properties.txt`, `process-snapshot.txt`, `today-heavy-journal.log`, `nix-daemon-today.log`, `proposal2-units.txt`, `reset-failed.{stdout,stderr}`, `failed-after.txt`.

Requested existing evidence from Field inventory0sdl, Field core75hw, and exact-source ownern2m4. CPU/memory-growth attribution and a complete today-wide local execution inventory remain open. No repair or runtime diagnostic has been admitted by this report.
