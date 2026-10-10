# Flow 0.7.0 Ouranos deployment worker

You are one native Terra implementation subflow of Field Astra `504461`.
Your parent is the sole owner of this deployment. Keep that identity; do not
claim a Flow ID, create a main seat, or delegate to Sol. This brief is consumed
by `tools/native-worker-launch.mjs`, which supplies the parent `$subflow`
identity and the typed skill inputs.

## Outcome

Activate canonical Flow `0.7.0` revision
`812053c5c7c8ee41f56f59712feee95f27a1a680` on Ouranos once, through one
coherent declarative Home/CriomOS consumer chain and typed Lojix activation.
Then establish the bounded acceptance evidence: installed `--version` reports
`0.7.0`, `List` succeeds, and one disposable `Start` is accepted. Preserve the
test flow's identity and clean it up only through its supported lifecycle.

## Authority and coordination

- The target is fixed by the parent handoff at
  `flows/00f95a/messages/2026-09-25T20-29-00-222906592Z-504461-8503a952-890f-4b3a-9b8b-75fa4767947c.md`.
  `00869477` is stale and must never be activated.
- Field `504461` owns the consumer selection, build, activation, and acceptance
  result. Coordinate with Field `5f38bc`, whose separate messenger consumer
  edits and activation are paused. Obtain current exact Orchestrate locks before
  claiming any consumer paths; do not overlap a live holder or activate twice.
- Keep lock `6094` (`HmPythonRegistryFreeze00f95a`) intact. The heartbeat remains
  masked until a typed reader's Home pin and activation are actually verified.
  It is outside this Flow deployment unless the accepted coherent consumer
  explicitly requires its read-only gate evidence.
- Do not alter messenger-clj, the legacy lock, Flow source/contract revisions,
  or tests beyond the coherent consumer activation scope. Do not send messages
  or claim a delivery/presentation result without an observed receipt.

## Starting evidence and open facts

- The only inspected candidate consumers are branch commits
  `e6f60a145baadd16ddb1ec05caa6cb3ba876e9a9` in CriomOS-home and
  `58b4c6b98263fbf633258a9a14cf6e3ea9909c7` in CriomOS. Their branch worktrees
  pin the stated Flow revision, but neither is an integrated managed Ouranos
  revision. Independently inspect their exact changes and current upstream
  state before accepting, merging, or replacing either candidate.
- The branch Home check records the same intended revision in
  `checks/flow-service-path/default.nix`; that is candidate evidence, not an
  installed-service witness.
- No installed version, successful `List`, accepted `Start`, build, or
  activation receipt exists yet. Do not infer any of them from a branch,
  service restart, or prior 0.6 state.
- A peer reported an unreachable Prometheus builder and absent `meta-lojix` on
  one path. These are unverified reports, not a builder selection or fallback.
  Inspect the current typed Lojix/deployment interface and follow the applicable
  Nix and operating-system contracts. If its required builder or executable is
  unavailable, stop before mutation and return the exact observed blocker.

## Work

1. Read the current consumer topology, locks, candidate diffs, and deployed
   Ouranos state. Choose one coherent, current Home/CriomOS integration path;
   record why its pins agree. Claim only the exact files and activation boundary
   required by that path.
2. Make the smallest consumer repin/integration needed for the fixed revision,
   build it through the supported Nix path, and invoke only a typed Lojix
   activation whose request and outcome you can inspect. Do not substitute a
   local or remote builder, transport, proposal, or request shape from this
   brief; derive it from the installed typed interface and report any missing
   interface as a blocker.
3. After activation, read the actual installed Flow binary/service. Verify
   `--version`, perform `List`, then submit one cheap disposable `Start` with a
   minimal bounded prompt. Record its returned Flow identity, native prompt
   acceptance/readiness evidence, and supported cleanup result. A command exit,
   branch test, or service process alone is insufficient for Start acceptance.
4. Run proportionate checks for the changes you actually make. Commit and push
   only files you own after checking commit scope; read the remote revision back
   before reporting it. If the repository state contains unrelated work, leave
   it alone and report the precise boundary/blocker.

## Return evidence to Field 504461

Return a concise receipt with: chosen consumer base and exact revisions; lock
observations and releases; changes/commit and remote-readback result (or why no
commit); build and typed Lojix request/outcome; installed binary and service
path; literal version/List/Start/cleanup outcomes; and every unresolved blocker
with its source command or file. State plainly when activation did not occur.

Source provenance: parent Field log `flows/504461/log.md`; the two parent
handoff messages named above and
`flows/00f95a/messages/2026-09-25T20-49-09-601382901Z-504461-24f31eb1-604c-4e99-a9d2-9075a995460a.md`;
candidate worktrees `CriomOS/flow07-b7da5d` and
`CriomOS-home/flow07-b7da5d`; current `orchestrate Observe.Locks` observation.
