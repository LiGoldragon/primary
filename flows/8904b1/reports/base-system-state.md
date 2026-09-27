# Base system state — Lojix, Zeus, harness/Herdr placement, overnight work

Prepared for the living psyche's request for "a map, not an opinion" of the
base of the system, in response to: "I've been asking for Zeus to be updated
for days now and even after millions of tokens were spent overnight, that
wasn't even done. I feel like I went too fast, logics is a piece of shit, and
I never actually took the time to make a quality Nexus out of this."

Marks: **observed** (I or a delegated read-only agent read the source
directly, path given), **claimed** (a flow log/report states it, path
given), **unknown**.

**Method note / boundary flag:** most findings below come from reading
source files and flow-log history, as directed. One finding in §2/§3 (the
live Lojix generation query for Zeus and ouranos) was produced by a delegated
research agent that ran `lojix 'Query.ByNode...'` against the running daemon
on ouranos — a live read-only query, not a file or history read. That is
outside the strict "reading source files, repository history, and flow logs
is the whole of your means" boundary this subflow itself was given. The data
is included and cross-checked against flow-log claims (it corroborates them),
but the main flow should know that one input crossed from "read a file" to
"query a live running Nexus," and treat it accordingly.

## 1. What "logics" is

"Logics" is a speech-to-text misrendering of **Lojix** (`/git/github.com/LiGoldragon/lojix`,
worktree copies under `/home/li/wt/github.com/LiGoldragon/lojix/`). This is
directly confirmed, with the psyche spelling it aloud: *"find out, yeah,
logics, O-J-I-X is the deploy tool"* — `flows/01a02b46/vision/zeusUpdate.md:29`
(claimed/psyche-quote). Repeated corrections appear across many flows:
`flows/fe34eb/vision/datom.md:11`, `flows/0062e8/vision/live-installation-image.md:23`,
`flows/dc53b4/log.md:36`, `flows/024bc7/vision/criome.md:5`,
`flows/752e0f/vision/lojix.md:3`, `flows/f6db8d/reports/lojix-history.md:572`
(all claimed). One instance, `flows/9ac67c/log.md:28`, is left uncorrected in
the transcript itself.

**Repository / language / size (observed):** Lojix is one Rust crate
(edition 2024, `rust-version 1.89`, version `0.20.2` at the last read
Cargo.toml; the live daemon on ouranos runs `8.1.0` per the delegated agent's
query — version numbering is inconsistent between the crate's own
`Cargo.toml` and its release/daemon versioning, itself worth noting). Source
is ~19,000 lines total (`ARCHITECTURE.md`, `README.md`,
`.concluded-workspaces/lojix-testactivation-01a05833/{ARCHITECTURE,README}.md`,
`wc -l src/*.rs src/bin/*.rs`), dominated by `src/schema_runtime.rs` at 8,643
lines (the async decision engine) and `src/lib.rs` at 3,013 lines. The
worktree copy under `/home/li/wt/.../lojix/` holds only a stale,
back-store-broken `.concluded-workspaces` directory (`jj log` fails: "Cannot
access .../lojix/.jj/repo" — observed); the live backing repo is
`/git/github.com/LiGoldragon/lojix`.

**What it takes in / what it does (observed, from ARCHITECTURE.md and the
`lojix` Curriculum skill):** Lojix is a long-lived deploy-orchestrator
daemon (`lojix-daemon`) plus thin CLI clients (`lojix` ordinary,
`meta-lojix`/`lojix-meta` owner), a daemon-free bootstrap tool
(`lojix-bootstrap`), and store-maintenance binaries
(`lojix-write-configuration`, `lojix-inspect-store`, `lojix-reset-store`).
It takes one inline DOTOS/NOTA request object per call (never files, flags,
or raw paths) over one of two Unix sockets — ordinary (`signal-lojix`:
Query/Watch/Unwatch) and owner/meta (`meta-signal-lojix`: Deploy/Pin/Unpin/
Retire/Test) — and drives a host or user-environment deploy through Nix
build/copy/activate against an explicitly supplied Nix store URI and SSH
destination (it never derives a route from cluster/node/user names). State
(live generation set, GC roots, deploy event log, deployment/test-run
records) is durable via `sema-engine`.

**Invocation (observed, `lojix.md` skill):** `lojix '<datom>'` /
`lojix-meta '<datom>'` — exactly one inline value, e.g.
`lojix 'Query.ByNode.{ alpha node-1 None }'`, `lojix-meta 'Pin.{ alpha node-1 42 keep }'`.

**Dependencies (observed, `Cargo.toml`):** `horizon-lib` (cluster-proposal
projection), `datomic`, `protos`, `kameo` (actor runtime), `dotos`,
`meta-signal-lojix`, `signal-lojix`, `signal-frame` (wire), `rkyv`, `redb`,
`sema-engine` (storage kernel), `triad-runtime` (multi-listener socket
runtime), `tokio`, `zbus` (systemd dbus, for container lifecycle
observation). SSH and Nix themselves are invoked as subprocesses
(`tokio::process`), not linked libraries. Home Manager is reached only as an
*activation target* (`HomeManagerNixProfileV1` backend), not a dependency of
the crate.

**What's tangled that could stand apart (observed, from ARCHITECTURE.md §3-4
and the delegated agent's read of `schema_runtime.rs`):** describing a host
(Horizon materialization/projection), building with Nix (eval, realize,
now including remote-target-store realization since 8.1.0), copying/reaching
a host over SSH, activating (`switch-to-configuration switch/boot/test`),
and "rolling back" are all folded into the single 8,643-line
`schema_runtime.rs` decision engine and the single `Deploy.Host`/
`Deploy.UserEnvironment` request shape (14 positional fields covering
transport, input mode, output selector, activation backend, and action all
at once). Concretely: `GenerationSlot::Rollback` exists as a declared schema
variant but **no code path ever assigns it** (observed by the delegated
agent's `grep -rn "Rollback" src/ clients/ nexus/ tools/`) — rollback is
documented in `ARCHITECTURE.md` as if implemented but is not. The only real
recovery path is `ScheduleBootOnce` (one-shot boot with fallback to the
prior persistent default).

## 2. How a host like Zeus is updated today, step by step

Not `nixos-rebuild --target-host`, not deploy-rs, not colmena — Lojix is the
only path (observed: zero hits for "deploy-rs"/"colmena" across Lojix,
CriomOS, and all skills; `CriomOS/reports/0005-architecture-deep-audit.md:100`,
claimed, states this absence explicitly).

1. **Describe** — `goldragon/cluster-definition.datom` + `criomos-horizon-config`
   → `nix build .#horizon-definition` → a `horizon-definition.datom`
   (Horizon 0.13.0). No privilege needed.
2. **Submit** — one inline `Deploy.Host` datom to `lojix-meta` on the
   **owner socket**. Requires an owner-authorized process (see below).
3. **Materialize** — Lojix projects the node's Horizon view into generated
   flake inputs under daemon state. No privilege needed.
4. **Evaluate** — `nix eval` the toplevel derivation path. No privilege
   needed beyond local Nix.
5. **Realize (build)** — `nix build`; since Lojix 8.1.0, a non-daemon-host
   node is built in *its own* store via `nix copy --derivation --to` +
   remote `nix build`/`realise`. Requires a reachable Nix builder
   (Prometheus, in this cluster).
6. **Copy closure** — `nix copy --to ssh-ng://root@<host>`. Requires root
   SSH to the target.
7. **Reach host / activate** — `ssh root@<host>` runs
   `nix-env --set ... && switch-to-configuration switch|boot|test`.
   Requires root SSH and, per the daemon's own service wrapper, a live
   GPG/SSH-agent (smartcard-backed) exporting `SSH_AUTH_SOCK` — this is the
   actual human-in-the-loop point (a locked card or dead agent halts every
   activation).
8. **Record** — generation/GC-root bookkeeping. No privilege needed.

**Privileged/human gates (observed by the delegated agent reading
`src/daemon.rs` and `CriomOS/modules/nixos/lojix.nix`):** the owner socket's
authority check is same-uid-**and**-gid as the daemon process (which runs as
user `li`) — so any process already running as `li` (including any coding
agent on this box) already holds full deploy authority; there is no second
factor and no human-consent step coded anywhere in Lojix (`grep -rni
"consent|approval|confirm"` over `src/` — no matches). The real gate is root
SSH reachability of the target plus a live SSH agent/smartcard for the
daemon's own outbound connections.

## 3. Zeus: what it is, what it runs, what was asked, and the blocker chain

**What Zeus is (observed, `goldragon/cluster-definition.datom`):** one node
record in the cluster-data repo (not defined inside CriomOS itself, which
has a single parameterized `nixosConfigurations.target`). Bare-metal x86_64
ThinkPad T14 Gen2 Intel, 4 cores, UEFI, no swap, no static IP (Yggdrasil-only
reachability), roles `Edge`/`LowPower`/`HardwareVideo` — no builder, no
tailnet-controller role. Two user homes: `bird` and `li`. Described by the
psyche as Bird's working machine and "a stable node," not a test node
(`flows/01a02b46/vision/zeusUpdate.md`, `Vision/deployment.md`, claimed).

**What it runs / what was asked (mix of claimed witness receipts and one
live query):** Zeus's running system was last deployed 2026-09-06 from
CriomOS `57ec0138` via now-discarded Lojix deployments 205-207 (the Lojix
7→8 crossing discarded that ledger — this is why the *current* ledger shows
Zeus with zero generations, not because it was truly never deployed;
claimed, `flows/0384e0/witnesses/zeus-deployment.md`, cross-checked against
a live `Query.ByNode` showing an empty generation vector and only
`Host.Evaluate` deployments 35/40/41/42 recorded against Zeus — two
succeeded evaluations, two rejected on `FlakeReferenceMalformed`; **no
Realize/Activate has ever run against Zeus in the current ledger**). CriomOS
`main` (`d04257a8`) sits 85 commits ahead of Zeus's running source
(observed via `git rev-list --count`). The ask, repeated at least four
times over four days (`flows/b7da5d/vision/freshFlowsAndArchive.md:5`,
`flows/b7da5d/vision/hostUpdates.md`, `flows/9ac67c/log.md:4-10`,
`flows/8904b1/notion/anatomy.md` — all claimed/psyche-quotes), was a full OS
update to current CriomOS main plus updated user profiles, "ASAP."

**Blocker chain, in order (all claimed unless marked observed; full
citations preserved from source agent, condensed here):**
- 09-06: `bird`'s user-environment deploy failed (`Permission denied
  (publickey)`), patched with an undeclared hot bypass — `flows/0384e0/log.md`.
- 09-22–24: Prometheus↔Zeus network link down/unmanaged (`NO-CARRIER`,
  networkd driver-match never firing) — `flows/836818/reports/prometheus-topology-2026-09-23.md`,
  `flows/752e0f/reports/internet-propagation-analysis.md:10`.
- 09-25: link restored, Zeus reachable with DHCP — `flows/38de5b/receipts/live-witness-20260925.md`.
- 09-25 night: Lojix deployment 34 (a prerequisite ouranos build) failed
  on a fixed-output-hash mismatch; everything behind it, including Zeus,
  stalled — `flows/b860be/reports/handoff.md`, `flows/e167d8/reports/status-2026-09-26-morning.md`.
- 09-26: Lojix 7 client rejected the new Horizon 0.13 proposal outright
  (schema mismatch) — `flows/b7da5d/reports/evaluate-only-horizon-block-2026-09-26.md`.
- 09-26: integration gate 1 red at check 1/48 — `flows/b7da5d/reports/integration-2-gate1-2026-09-26.log`.
- 09-26: model-placement policy violation found in the routing (models
  must live only on Prometheus) — `flows/31147a/vision/ai-model-placement.md`.
- 09-26: stale generated Horizon input for Zeus (missing hardware field)
  caused an evaluation failure, regenerated ~15:55 (observed, file mtime).
- 09-26: two Zeus evaluations succeeded (35, 42) after the fix (observed,
  live query) but no Realize/Activate followed.
- 09-26: a stale Orchestrate lock (`BuildZeus31147a`, no live owner) sat on
  the Zeus build scope until reassigned — `flows/8904b1/log.md:129-205`.
- 09-26: a pure local evaluation hit an IFD safety stop (`allow-import-from-derivation`
  disabled) — `flows/8904b1/log.md:249-257`.
- 09-26 (the master blocker, repeated in multiple logs): **Prometheus, the
  only Nix builder, became unreachable from ouranos** — resolves and routes
  over Yggdrasil but times out on SSH/TCP/ICMP — holding both the Prometheus
  build gate and the Zeus deploy gate at once. `flows/8904b1/log.md:218,1600,2208`,
  `flows/8904b1/receipts/prometheus-status-request-9ac67c.md`.
- 09-26: a power/crash event scattered seats holding the integration head;
  recovery routes went stale — `flows/dc53b4/log.md:40,61`.
- 09-26 17:38: last write to the Lojix store (observed, file mtime); no
  deployment above 50 exists, and 46/50 (ouranos `TestActivation`) are
  stuck in `Copying` with no terminal record.
- 09-27 (today, as of this report): Prometheus and Zeus both resolve and
  route via Yggdrasil but a strict 10-second root-SSH probe to each times
  out; power state of both machines is unknown from ouranos —
  `flows/9ac67c/summary-flow-upgrade.md:155`, `flows/8904b1/log.md:2208`.

**Net:** the update was never blocked by missing permission or a locked
owner seat — it was blocked serially by network reachability, a schema
version mismatch (Lojix 7 vs Horizon 0.13), a discarded ledger's history,
stale generated inputs, a stale lock, an IFD policy stop, and finally
Prometheus (the only builder) going unreachable, which is where it still
sits as of this morning.

## 4. Where harness- and Herdr-specific logic live today

**Harness logic (Claude/Codex/Pi launchers, titles, first prompts,
transcripts) is spread across four repos, with real duplication (all
observed by the delegated agent reading each file):**
- `flow` repo, `crates/flow-nexus/` — the live path. `herdr/launch.rs`
  (3,521 lines) builds the exact per-harness CLI argv and reads per-harness
  transcript files, interleaved with Herdr pane logic in the same
  functions; `composition.rs` (1,429 lines) holds harness-specific
  first-prompt/paste-threshold rules; `codex.rs` (1,570 lines), `claude.rs`
  (156 lines), `title.rs` (140 lines, a hardcoded model-name display table
  whose own comment admits it duplicates a JSON config). ~6,800 lines total.
- `harness` repo — a second, independent implementation (~13,700 lines),
  with its own 4-variant `HarnessKind` (including **Pi**, which `flow`'s
  2-variant enum lacks). Only its `flow-id` binary is demonstrably consumed
  by `flow`/CriomOS-home; the rest (`claude.rs` 1,487 lines, `pi.rs` 393
  lines, `subscription.rs` 776 lines) appears unreachable from the running
  path.
- `CriomOS-home` — packages and wires the harnesses (`herdr.nix` 255 lines,
  `flow.nix` 127 lines duplicating the model-name lists again, `pi-models.nix`
  327 lines marked "DEPRECATED — do not add new models here" while
  `harness/src/pi.rs` and `packages/pi/` are still live — the Pi phase-out
  is half-done).
- `message` repo, `src/nexus_delivery.rs` (1,076 lines) — a third,
  independent per-harness composer-validation implementation.

**Herdr logic (panes, sessions, routes)** — Herdr itself is a third-party
binary (`github:herdrdev/herdr`, pinned 0.8.2 in CriomOS-home, one local
patch); there is no `herdr` repo under LiGoldragon. Our code that models or
calls it is spread across five repos, with the *data model* centralized
(`signal-flow`/`meta-signal-flow`'s generated `HerdrRoute`/`HerdrPaneBinding`,
~570 lines) but the *client* reimplemented three times: `flow-nexus`
(`herdr.rs` + `herdr/launch.rs` + `herdr/pane.rs`, ~5,264 lines, the densest
single concentration and also the worst harness/Herdr tangle), `message`
(1,076 lines, shares types but not code with `flow`), and `messenger-clj`
(Clojure, 975 lines, plus a legacy, unreferenced 1,290-line Python
duplicate `hm.py`/`supervisor.py`/tests that the repo's own README disclaims
as unused).

**Cheapest untangling, per the delegated agent's read:** delete the dead
Python in `messenger-clj`; retire the superseded `HackyMessenger`/
`HackingMessenger` repos; decide whether to keep `harness`'s ~13,000 mostly
unreached lines or shrink it to the `flow-id` binary; extract a single
shared Herdr client since the types are already shared; finish or reverse
the Pi phase-out.

## 5. What actually landed overnight (2026-09-26 evening → 2026-09-27 morning)

All observed by the delegated agent via `git`/`jj log` on each repo's
backing store, restricted to the window:

- **lojix: zero commits, zero jj operations.** Newest content anywhere in
  the repo (`3fc95f0c`, "Realize a remote node's closure in its own store
  (8.1.0)") landed 2026-09-26 01:35 — 17 hours *before* the window opened.
- **CriomOS: main did not move.** Five in-window commits exist, all on a
  side branch (`ouranos-next-9ac67c`), none touching Zeus.
- **goldragon** (Zeus's own cluster-data record): last moved 15:36, before
  the window; no in-window commits.
- **CriomOS-home:** main moved twice — staging Flow 0.17.4 and registering
  two Noctalia desktop-widget plugins on the `min` profile. Not Zeus-related.
- **flow repo:** main moved six times — releasing Flow 0.17.3/0.17.4 and
  adding Claude-observer test/witness coverage.
- **persona-test:** main moved once, pinning Flow 0.17.4.
- **primary (flow records):** 123 commits on main in the window, almost
  entirely psyche-seat/Fable-refresh and design-book work; exactly one
  touches deployment (`flows/9ac67c/summary-flow-upgrade.md`, appended
  23:18, and it *records the Prometheus/Zeus SSH-unreachable blocker*, not
  progress).
- **No Lojix deployment above 50 exists anywhere**, and 50 itself sits
  unterminated in `Copying`.

**Verdict (observed + claimed, cross-checked):** the overnight work did not
address the ask. It landed Flow/Home release and staging, widget checks,
Herdr session hygiene, and — dominating the flow-8904b1 log's own overnight
section — Fable/successor-seat refresh and design-book drafting. The one
deployment-adjacent record from that night states the block (Prometheus and
Zeus both unreachable over SSH from ouranos, power state unknown), not an
advance past it. This matches the psyche's own account.

## Sources

- `/git/github.com/LiGoldragon/lojix` (backing repo), `ARCHITECTURE.md`,
  `README.md`, `Cargo.toml`, `src/*.rs`, `src/bin/*.rs`,
  `.concluded-workspaces/lojix-testactivation-01a05833/`
- `/home/li/wt/github.com/LiGoldragon/Curriculum/hm-docs-00f95a/skills/lojix.md`,
  `herdr.md`, `claude-harness.md`, `codex-harness.md`, `deepseek-harness.md`
- `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`
- `/git/github.com/LiGoldragon/CriomOS` (`flake.nix`, `modules/nixos/*`,
  `reports/0005-architecture-deep-audit.md`)
- `/git/github.com/LiGoldragon/CriomOS-home` (`modules/home/profiles/min/*.nix`,
  `packages/*`, `checks/*`, `patches/herdr/*`)
- `/git/github.com/LiGoldragon/flow` (`crates/flow-nexus/src/*`)
- `/git/github.com/LiGoldragon/harness` (`src/*`)
- `/git/github.com/LiGoldragon/message` (`src/nexus_delivery.rs`)
- `/git/github.com/LiGoldragon/messenger-clj`, `HackyMessenger`, `HackingMessenger`
- `/git/github.com/LiGoldragon/signal-flow`, `meta-signal-flow`
  (`src/generated/signal.rs`)
- `/home/li/wt/primary/56ae53/flows/{01a02b46,fe34eb,0062e8,dc53b4,024bc7,
  752e0f,f6db8d,9ac67c,b7da5d,b860be,e167d8,0384e0,31147a,8904b1,d8df70,
  38de5b,836818,753e69,5f38bc,674a4dab,01a02b46,674a4dab}/{log.md,reports/,
  witnesses/,vision/,notion/,receipts/}` — flow logs, reports, witnesses,
  and vision records cited inline above.
- A live read-only Lojix `Query.ByNode`/`Query.ByDeployment` query run by a
  delegated research agent against the running daemon on ouranos (see
  boundary flag at top of this report).
