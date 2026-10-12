# Why the Flow Nexus is not in use

Assembled 2026-10-12 by a read-only subflow of 9519a1. Each item is
marked **witnessed** (observed by this subflow: a command run, code
read, git history read), **claim** (written in a flow log or report;
not re-observed here), or **inference** (this subflow's own reading).

## What is true today

- **Witnessed.** `flow-nexus.service` runs
  `/nix/store/j689l77…-flow-0.14.0/bin/flow-nexus`, active since
  2026-10-08 11:17. `flow-nexus-next.service` runs Flow 0.17.4 from
  the same time. `message-nexus-next.service` runs Message 0.17.0.
  `message-daemon.service` (Message 0.14.0) is failed,
  `start-limit-hit`. Sockets exist at `/run/user/1001/flow/` and
  `/run/user/1001/flow-next/`.
- **Witnessed.** `~/.local/bin/flow` resolves to Flow 0.23.0, a client
  nine minor versions past the stable service it would talk to.
- **Witnessed.** `~/.local/state/flow/flow.sema` is 311 KB, last
  written 2026-10-08 11:17, when the services last started.
- **Witnessed.** Flow source: `origin/main` is 962ad12 (2026-10-10),
  version 0.25.0. The last feature commit, ac6ab64, is from 2026-10-03.
  The first commit, ec3941a, is from 2026-09-17. signal-flow
  `origin/main` 068f0ea (2026-10-09, "SignalFlow11");
  meta-signal-flow 88f3759 (2026-10-09, "Meta 15"); Message
  `origin/main` 6fa4d0c (2026-10-03, 0.19.1).
- **Witnessed.** Seats launch without the Flow Nexus.
  `tools/claude-main-flow-launch.mjs:165` and
  `tools/codex-main-flow-launch.mjs:88` call `flow-id` (from the
  `harness-0.6.1` package, not from Flow), then `herdr` for tab, pane
  and agent, then `hm-register` (messenger-clj 0.3.0). Neither script
  calls `flow`, `flow-meta`, or either Flow socket. The messenger-clj
  source does not reference a Flow socket either. messenger-clj's
  first commit is from 2026-09-25.

So every part of launching and reaching flows in use today (ids,
panes, titles, routes, delivery) runs through flow-id, Herdr and
messenger-clj. The Flow Nexus runs, but nothing on the live path
depends on it.

## Candidate causes

### 1. The target was redesigned while the build was chasing it

- **Witnessed.** Between 2026-09-25 and 2026-10-03, Flow went from
  0.7.0 (812053c) to 0.24.0 (4ad596d), seventeen minor releases in
  nine days. Over the same span signal-flow went to 10.0.0 and
  meta-signal-flow to 14.0.0, and each breaking bump forced a Message
  repin (message 64ea9eb, ce3eb6c).
- **Witnessed.** The buildable design on Primary `origin/main`,
  `flows/f5a6e9/reports/flow-buildable-design.md`, has 34 commits
  from 2026-10-09 to 2026-10-10 (f7a7ad374 … 2d0a119bc). Its section 3
  says that the Library, Memory, both Signals, Bind, Lock, Deliver,
  Configure, Wake, Refresh, End and the module registry are all
  "To build (none in production)". It also says that "the new Flow
  reads nothing of the old store and migrates nothing" (5c3f280ee,
  b7618271b). The deployed line is therefore not an early stage of
  the target. It is a predecessor that the target replaces.
- **Witnessed.** flow-test was rewritten to this design on 2026-10-10
  (30 commits, latest 01c29c9 "written to Flow's design at Primary
  9bffed2f4"). Its README scenarios test Configure.Nexus, Lock and
  Deliver, which no deployed or `main` Flow implements. Whether those
  checks are red now was not run here; that they cannot pass against
  0.25.0 is an **inference**.
- **Claim.** `flows/445410/log.md:427` (2026-10-10): the new-design
  Flow branch "reaches compilation: 29 flow-nexus and 2 flow-meta
  errors", and Message is down to 3 errors. Lines 430 and 432 say the
  design's Aspect/FlowAspect shape was still changing that same day.
- **Witnessed.** The new-design work sits on unmerged branches
  (`origin/field/storepath-flow-…`, `origin/field/signal-aspect-store-…`,
  `origin/field/message-memory-operation-…`, all dated 2026-10-10).

### 2. The deployment path kept failing, and the deployed version moves without explanation

- **Claim.** Prometheus builder and cache were unreachable on several
  days: `flows/836818/log.md:50,54` (09-22/23),
  `flows/b7da5d/log.md:100` (09-25, tailnet logged out),
  `flows/e167d8/log.md:20`. Builds were barred from Ouranos at the
  same time (e167d8:20).
- **Claim.** CriomOS-home had no Flow flake input or service wiring,
  so a pin-only bump could not install Flow (`flows/b7da5d/log.md:94`,
  2026-09-25).
- **Claim.** An unmanaged drop-in `flow-nexus.service.d/override.conf`
  held stable Flow at 0.12.2 while Home declared 0.14.0. The
  0.12.2→0.14.0 step was gated on copied-store proofs, a countdown
  rollback and the living's override ruling
  (`flows/9ac67c/summary-flow-upgrade.md`, lines 17–33 and 84,
  2026-09-26 to 09-28).
- **Claim.** On 2026-10-03, Home deployment 79 failed at activation,
  and 81 failed on a messenger link guard
  (`flows/42265e/log.md:494`, `flows/5578cc/log.md`). Deployments 80,
  82 and 83 succeeded, and stable and Next Flow were both reported at
  0.23.0 (`flows/41fa34/log.md:206`, `flows/42265e/log.md:504`).
- **Witnessed / unknown cause.** Today stable runs 0.14.0 and Next
  runs 0.17.4. That contradicts the 10-03 claim of 0.23.0 on both.
  `flows/4ddfe1/log.md:8` (2026-10-07) already records 0.14.0. This
  subflow found no log entry explaining the change. Possible causes:
  a later Home generation that pins the older units, a rollback toward
  generation 1039, or a wrong 10-03 witness. None of these was checked.

### 3. Flow cannot ship without Message, and Message is part of the same open question

- **Claim.** Flow 0.19.0 could not deploy because Message 0.17.1
  pinned signal-flow 7 and could not read its frames
  (`flows/f1c841/log.md:22`, 2026-10-03). Message's UPGRADES says to
  rebuild Message and Flow together (f1c841:28).
- **Witnessed.** The design's section 4 leaves Message's needs N3
  (Lock and Deliver on which socket) and N8 (queueing an awake flow)
  open. It also says the living's answer on «What the new Message does
  with the old store» "decides Flow and Message together".
- **Witnessed.** The old Message daemon unit is failed. The Next
  Message runs 0.17.0, two minors behind Message `main` (0.19.1).

### 4. The live launch path works and the Flow launch path never passed a real launch

- **Claim.** On 2026-09-25 the living said the messenger should be
  used now (`flows/38de5b/log.md:91`). messenger-clj starts that day.
  Field's blocker was that Codex flow-id needs the session id before
  the first prompt (38de5b:83).
- **Claim.** Flow's first private Start on 2026-10-03 was refused
  because a 54-column pane wrapped its marker. The combined retry
  launched Claude, but Herdr showed no session and the binding was
  refused with the reason discarded (`flows/5578cc/log.md`, entries
  after deployment 80).
- **Claim.** `flows/4ddfe1/log.md:8` (2026-10-07): "Flow Start/Replace
  remains unqualified." `flows/6aa08d/log.md:44`: the Codex launcher
  is "the only candidate avoiding Flow Nexus". The Primary launchers
  received work through 2026-10-10 (897984f36, 899d194af).
- **Inference.** Because the parallel route works, the cost of not
  adopting Flow is never felt on the live path, so cutover never
  becomes a blocker for anyone.

### 5. Rulings wait on the living, one book at a time

- **Witnessed.** Design section 4 lists pending rulings from books 1,
  3, 10, 11, 14, 15, 17 and 18. Its header says "nothing here is
  landed in a skill". Only «Speech across aspects» is recorded as
  approved (psyche-skills 850fd27, 2026-10-09).
- **Claim.** Review goes "one proposal at a time: a book … then a
  pause" (`flows/445410/log.md:15`). `flows/9fed42/log.md:12`: "seven
  Flow books before the living, none ruled". Several books went to
  second and third editions before any ruling (9fed42:18, 28, 32).
- **Claim.** Today, 2026-10-12, the living approved proposal 1 of the
  third edition and asked for further identifier-name shots
  (`flows/875960/log.md`, tail).
- **Inference.** The design is current best only. Its builders build
  against unratified shapes, which feeds cause 1.

### 6. Ownership moved often, and some owners were absent

- **Claim.** Deploy ownership of Flow 0.7–0.10 passed between Field
  Sol, Field Astra and Psyche several times in one day
  (`flows/b7da5d/log.md:13,66,74,80,122`, 2026-09-24/25).
- **Claim.** A task sent to f5a74e "was never acted on"
  (`flows/38de5b/log.md:94`). A stale lock by e798f3 held flow-nexus
  files (38de5b:12). Flow 0.17.3's rollout had "no owner"
  (`flows/8904b1/log.md:121-122,184`). A dead flow's lock (31147a)
  blocked the Home gate (8904b1:121).
- **Claim.** Production adoption was withheld on purpose until
  2026-10-03 ("no production adoption", `flows/5578cc/log.md:20,41`),
  when the living ordered the deployment himself (5578cc:81). On the
  same day he said: "I feel like there's a problem with things
  actually happening as I ask them."

### 7. Gates and proofs ahead of each step

- **Claim.** Each activation required copied-store hashes, a timed
  rollback, a quiet window, live Start witnesses and named acceptance
  (`flows/9ac67c/summary-flow-upgrade.md:26-28,50`). The living
  called "a class of checks" "bullshit" on 2026-10-03
  (`flows/5578cc/log.md`, vision/checks.md).
- **Inference.** Gates sized for a breaking change were applied to
  every step, which slowed each release from reaching the host.

## Not established

- Why stable went from the reported 0.23.0 (10-03) to 0.14.0
  (10-07/08).
- Whether the 10-10 new-design branches compile now, and whether
  flow-test passes against any build. Nothing was built or run here.
- What the living has ruled on books 10–18 outside the logs read.
- The installed `flow` 0.23.0 client rejected the bare word `List` at
  its own parse ("expected Query"). The correct request form was not
  tried, so no answer from either Nexus was observed.

## Sources

Read in this order: `systemctl --user` unit state and ExecStart;
`readlink` of `flow`, `flow-id`, `flow-next`, `hm-send`;
`~/.local/state/flow/`; git logs of flow, signal-flow,
meta-signal-flow, message and flow-test under
`/git/github.com/LiGoldragon/` (local HEAD and `origin/main`);
`git show origin/main:flows/f5a6e9/reports/flow-buildable-design.md`
in `/home/li/primary`; `tools/*-main-flow-launch.mjs`; the
messenger-clj README; `flows/{f5a6e9,38de5b,445410,836818,9fed42,
e167d8,b7da5d,6aa08d,ebbe30,0c85a3,3ec648,f1c841,5578cc,184bd8,
8904b1,6997eb,4ddfe1,41fa34,42265e,28d847,875960}/log.md`;
`flows/9ac67c/summary-flow-upgrade.md`;
`flows/836818/vision/flowNexus.md`; `flows/f5a6e9/handover.md`.
Provenance receipt: unavailable; no receipt handoff exists for this
thread.
