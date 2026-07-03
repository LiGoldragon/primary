# Handover — Whole-Engine Testing Readiness & the Synchronizer (2026-07-03)

Focus-scoped freshness aid for a session continuing the whole-engine
testing/operation work. Read `reports/field-readiness/02-kink-ledger.md` (its
2026-07-03 closeout delta first), then this.

## Focus

Bring the whole persona/criome engine to the point of continual assembly
testing and entering operation — get the field ready for a sustained session
that fits every component together and tests them together, especially by
running VM clusters on the high-capacity host. Find and clear the kinks that
would stall that session mid-flow.

## Settled psyche direction

- Continually test the complete assembly and enter operation of the whole
  engine; prepare the field so a sustained fitting-and-testing session is not
  blocked by broken tooling. VM-cluster testing on the high-capacity host is the
  main event.
- `prometheus` is the sole builder, permanently, and that is correct — no other
  host is suitable and no second/backup builder is wanted. Single-host
  concentration is an accepted condition, not a defect.
- Builds run on the remote builder only; no local builds.
- Mechanical cross-repo version propagation belongs in a tool, not repeated by
  hand. Hence the `synchronizer` (universal, now public and proven live).

## Confirmed facts (current state)

Field readiness — verdict READY-WITH-KINKS (ledger `02-kink-ledger.md` + its
2026-07-03 closeout delta; recon evidence `10`–`13`; label `field-readiness`):

- prometheus VM host, tooling field, whole-engine build, and the minimal
  runnable whole are all witnessed working (unchanged from the recon; see
  ledger). 22 `NotBuiltYet`/stub operations are enumerated in `12`. No
  continuous-testing entry point exists yet (bead `primary-vp6d`, P1).

Whole-engine gate:

- The fenix-pin instantiation death is FIXED (persona main `bbb7f070`; bead
  `primary-j5j2` closed).
- The runtime wire skew is RESOLVED at signal-frame 0.3.0: signal-frame,
  signal-router, signal-harness, message, and router all verified GREEN on
  prometheus; router-daemon builds and passes its wire checks (the
  `Caller.identity` concern is gone). persona's flake inputs were normalized
  `git+ssh`→`github:` (persona main `ac629103`, landed) and the criome config
  updated (goldragon main `e8b658fa`).
- The gate's SOLE remaining blocker is the `nota-next`→`nota` crate-rename
  migration — bead `primary-ekvt` (P1). `primary-w46v` stays OPEN and now
  depends on `ekvt`; nothing landed to component mains; 6 `synchronizer` staging
  branches remain unmerged.

Synchronizer:

- Universality refactor DONE and independently audited PASS (zero project data,
  fully config-driven). PUBLIC remote `github.com/LiGoldragon/synchronizer`
  created, main pushed. First live run proved it end-to-end and exposed one tool
  bug — the transitive-lock fallback passed a repo/table key where the producer
  package name was needed — FIXED at synchronizer main `8eec5a46` with a
  regression test.
- Criome config externalized to `goldragon/synchronizer.nota` (7 components:
  signal-frame, signal-router, signal-harness, introspect, persona, router,
  message).
- Flagged gap (low severity, sidestepped for w46v by the persona flake-input
  normalization): the tool can't repoint `git+ssh`/`type:git` flake inputs
  (`github:` only).

Host / OS field:

- nixos-test builder capability landed declaratively + proven (CriomOS
  `f8eb6ff7`; kvm-capable builders now also advertise nixos-test); live ouranos
  System Switch DEFERRED to a watched window.
- GitHub-free `nix copy` inner loop VERIFIED working + sanctioned
  (CriomOS-test-cluster README `e57cc8d2`).
- ssh `HostName` fold-in landed declaratively (CriomOS-home `3738e2f2`); Home
  Activate DEFERRED.
- orchestrate daemon had died with no supervisor → restored (pid 58903
  running); systemd `--user` supervisor unit landed (CriomOS-home `faf8c230`,
  pinned to the running rev); live cutover DEFERRED (kill 58903 first),
  unplanned-activation race flagged.
- Jun30–Jul1 demo runtime removed; the 13G `/tmp/…142204` set (9 registered jj
  workspaces with uncommitted work intersecting the criome-authorization lane)
  DEFERRED to its owner.

## Synchronizer — settled shape (for pickup)

Purpose: cascade version bumps up the component dependency tree so wire
contracts stay aligned when a low dependency's `main` advances. Rust; NOTA
config in, NOTA report out; manages Cargo pins (format-preserving) and flake
pins (typed `flake.lock`). Topology from the manifests; edges by repository
identity, not Cargo package name. Cascade source: `main` tip for unmoved deps,
the producer's `synchronizer`-branch tip for anything bumped this run; the flake
input's `original` ref is preserved. Action: edit + commit + force-push a
per-repo `synchronizer` staging branch, never `main`. Verify runs the
wire-exercising checks where present else a default build; builder host resolved
from config (CriomOS cluster-datom resolver is one optional plugin). Universality
is done: builder resolution, commit author, branch scheme, verify words, and
forge are all config; the tool carries zero project data. Full law + schema:
`github.com/LiGoldragon/synchronizer/ARCHITECTURE.md`.

## Open questions and live uncertainties

- w46v's last blocker is the `nota-next`→`nota` migration (bead `primary-ekvt`).
  Open psyche decision: TOOL the crate-rename propagation (extend the
  synchronizer or a sibling) vs. hand-migrate the 9 gate-critical repos now —
  per settled direction "mechanical cross-repo propagation belongs in a tool".
- Residual uncertainty: persona's own topology checks have never fully BUILT+RUN
  (run 1 died at git+ssh fetch, runs 2/3 at the broken lock), so a latent
  persona-source incompatibility with signal-frame 0.3.0 is unproven — but
  router (a comparable consumer) passed its wire checks at 0.3.0, so confidence
  is high.
- Persistent-VM guest (decision e): genuine CONFLICT — the guest surface is being
  actively extended (goldragon mirror-alpha/beta TestVms for the spirit/mirror
  front on the same VmHost) while decision (e) asked to retire it. Needs psyche
  adjudication; bead `primary-dw95` updated, not closed.
- Deferred-activation punch list (needs a watched window): ouranos System Switch
  (nixos-test); ssh Home Activate; orchestrate systemd cutover (kill 58903
  first, unplanned-activation race hazard).
- Cheap-fix status: doctrine items and #6/#8/#12 done (skills + CriomOS
  `AGENTS.md`); #1/#2 superseded by the synchronizer; #7 (bookmark/workspace
  litter) deferred to a quiet single-agent window; component-repo hygiene
  (#3/#5/#9/#4-code/#11-code) not done (interim guards / active-front repos, low
  priority).
- Documented synchronizer limitations: a dual `[dependencies]` +
  `[dev-dependencies]` pin of one package is refused loud; `git+ssh`/`type:git`
  flake inputs are not repointed.

## Pointers

- `reports/field-readiness/00-README.md`, `02-kink-ledger.md` (+ closeout
  delta), `10`–`13`.
- Evidence:
  `agent-outputs/W46vGoLive/GeneralCodeImplementer-{Evidence,Run2-Map,Run3-NewLayer}.md`
  + `SyncNotaReport*.nota`;
  `agent-outputs/SynchronizerUniversality/GeneralCodeImplementer-Evidence.md`;
  `agent-outputs/FieldReadiness/OperatingSystemImplementer-{VmFieldPrep,FieldHardening}Evidence.md`.
- `github.com/LiGoldragon/synchronizer/ARCHITECTURE.md` and the repo.
- Beads (label `field-readiness`): `w46v` (OPEN, depends on `ekvt`); `ekvt` (P1,
  nota-next migration); `dw95` (conflict, open); `vcqx` (open, blocked-on-psyche
  dropped); `vp6d`/`95fm`/`mddx` and others open; `wgae`/`oftl` filed this
  session; `j5j2` closed; `oeng` retired (single-host concentration accepted).
- Mains/commits: persona `ac629103`, goldragon `e8b658fa`, synchronizer
  `8eec5a46` (+ public remote), CriomOS `f8eb6ff7`+`4140322e`, CriomOS-home
  `3738e2f2`+`faf8c230`, CriomOS-test-cluster `e57cc8d2`.
