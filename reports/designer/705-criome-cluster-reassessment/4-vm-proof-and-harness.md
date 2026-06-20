# 705-4 — VM-Proof + Test Harness State

Sub-report 4 of the 705 criome-cluster reassessment. Read-only audit of
`CriomOS-test-cluster` and the criome triad at `origin/main`.

## Headline

The criome VM tests are NOT on `CriomOS-test-cluster` main — they live only on the
unmerged branch `origin/criome-cluster-test`. Two checks exist there
(`criome-cluster-1of1`, `criome-cluster-auto-approve`), both green per their commit
logs. The full ClientApproval park/approve runtime AND wire contract are already on
criome / signal-criome / meta-signal-criome main, so the smallest next VM test
(ClientApproval park->approve->Authorized) is writable today — the one and only
blocker is a missing witness binary (`criome-client-approval-witness-test`); criome
main ships no client/witness binary that drives the meta park surface.

## State correction (premise mismatch)

The mission briefing assumed the criome harness is on test-cluster main. It is not.

- `git -C CriomOS-test-cluster ls-tree origin/main` has NO `lib/mkCriomeClusterTest.nix`
  and the flake exports NO `criome-*` check. Main's checks are horizon/CriomOS VM
  pickup, `lojix-deploy-smoke`, spirit-upgrade, and horizon-projection contract checks.
- The criome harness is entirely on `origin/criome-cluster-test` (7 commits ahead of
  main, tip `003bd2c`), which is unmerged. `lib/mkCriomeClusterTest.nix` and the two
  checks exist there only.
- The mission's file:line references therefore resolve against
  `origin/criome-cluster-test`, not main. All evidence below cites that branch for the
  harness and `origin/main` for the criome triad.

## (a) Which checks exist today

Both on `CriomOS-test-cluster origin/criome-cluster-test:flake.nix`, gated to
`x86_64-linux`:

- `criome-cluster-1of1` (flake.nix:333-339) — boots a real NixOS guest running the real
  `criome-daemon` as a systemd service, runs `criome-cluster-witness-test` against the
  working socket. Proves the 1-of-1 quorum gate with real blst BLS over a real Unix
  socket: authorized head accepted, threshold-short rejected. Members `[ "alpha" ]`.
- `criome-cluster-auto-approve` (flake.nix:346-353) — same guest; witness
  `criome-auto-approve-witness-test` reconfigures the daemon to `AutoApprove` over the
  META socket (`Configure(AutoApprove) -> Configured`, witness src lines 72-85 on the
  auto-approve criome branch), then an evidence-less `EvaluateAuthorization` over the
  working socket returns `Authorized`. Exercises the meta socket + runtime
  reconfiguration + the AutoApprove verdict mode together.

Commit logs (`003bd2c`, `115131f`) state both run green in a NixOS VM. There is NO
ClientApproval / park VM test of any kind, on any branch.

## (b) The mkCriomeClusterTest generator + prior audit fixes

Generator at `origin/criome-cluster-test:lib/mkCriomeClusterTest.nix`.

- Params (lines 28-36): `name` (default `criome-cluster-1of1`), `cluster` (default
  `fieldlab`), `members` (default `[ "alpha" ]`), `witness` (default
  `criome-cluster-witness-test`). Note the mission listed a `witness` param — correct —
  but there is no separate `members`/`witness` confusion: the four params are exactly
  `name, cluster, members, witness`.
- It builds one guest node from `inputs.criome.packages.${system}.cluster-witness`
  (line 38), wires a systemd `criome.service` whose `ExecStartPre` runs
  `criome-write-configuration` to encode the typed rkyv startup arg and whose `ExecStart`
  runs `criome-daemon <rkyv>` (lines 71-72) — the proven `mirror.nix` daemon shape, no
  flags, daemon never parses NOTA.
- testScript (lines 84-94): `wait_for_unit("criome.service")`, then
  `wait_for_file(socket)` and `wait_for_file(socket.meta)` (so the generator already
  asserts the meta socket is bound), then runs the witness with `CRIOME_SOCKET=` set.
- B7 honesty docstring (lines 18-22): explicitly scopes the test — the minimal guest
  runs criome as ROOT, proving gate-verdict logic + the meta socket in a real VM, NOT
  per-Unix-user isolation (needs a dedicated non-root service user + a denied-other-user
  assertion) and NOT the full CriomOS substrate.
- B8 loud rejection (lines 49-53): `members` length != 1 `throw`s with a message naming
  Stage A vs unbuilt Stage B, instead of silently `builtins.head`-truncating the tail.

## (c) What a ClientApproval park/approval VM test needs

The flow (submit -> criome parks -> client lists parked over meta -> approves by slot ->
original submission resolves Authorized) is FULLY SUPPORTED by the runtime and the wire
contract on all three repo mains. Evidence:

- Wire contract `meta-signal-criome origin/main:schema/lib.schema` already carries the
  client-approval meta surface: requests `ObserveParkedAuthorizations` (line 21) and
  `SubmitAuthorizationApproval(AuthorizationApproval{ request_slot, decision:
  Approve|Reject|Defer })` (lines 22, 44-52); replies `ParkedAuthorizationSnapshot`
  (line 24) and `AuthorizationApprovalRecorded` (line 25).
- signal-criome `origin/main:schema/lib.schema` carries `AuthorizationMode [Quorum
  AutoApprove ClientApproval]` (line 84), the park snapshot/observation types (lines
  471-489), and `AuthorizationRequestSlot` (line 71).
- criome `origin/main:src/actors/root.rs` implements all of it: working-socket dispatch
  for `ObserveParkedAuthorizations` (line 224) and the `ClientApproval` -> park branch in
  `evaluate_authorization` (lines 331-333, calling `park_authorization` line 348);
  meta-socket dispatch for `ObserveParkedAuthorizations` (line 293) and
  `SubmitAuthorizationApproval` (line 298); `apply_authorization_approval` (line 423)
  publishes the Authorized object update and sets status Granted on Approve (lines
  443-466). `park_authorization` returns `AuthorizationPending` carrying the
  `request_slot` + an `AuthorizationObservationToken` (root.rs:355-361) — so the
  submitter learns its slot.
- The client API exists in `criome origin/main:src/transport.rs`: `CriomeClient.send`
  (line 227) and `CriomeMetaClient.send` (line 248) cover every message above. The
  auto-approve witness already demonstrates the exact `CriomeMetaClient` +
  `CriomeClient` pattern a park witness would copy.
- Default boot mode is `Quorum` (`criome origin/main:src/lib.rs:142`,
  `src/daemon.rs:44`), so the witness must `Configure(ClientApproval)` over meta first
  (exactly as the auto-approve witness configures AutoApprove), OR the generator's
  `criome-write-configuration` would need a mode argument (it currently hardcodes the
  default — `src/bin/criome-write-configuration.rs:38` calls
  `CriomeDaemonConfiguration::new` with no mode).

WHAT IS MISSING: a witness/client BINARY. criome main ships exactly three bins —
`criome-daemon`, `criome-cluster-witness-test`, `criome-write-configuration`
(`Cargo.toml` lines 19-31). The `criome-auto-approve-witness-test` bin exists ONLY on
the `criome-auto-approve` branch. NO park/ClientApproval witness exists on any branch.
So a ClientApproval VM test needs a new `criome-client-approval-witness-test` bin
(behind the existing `cluster-witness` feature) that: Configures ClientApproval over
meta; submits an `EvaluateAuthorization` over working (expects `AuthorizationPending`,
captures the slot); `ObserveParkedAuthorizations` over meta (expects one parked entry at
that slot); `SubmitAuthorizationApproval(slot, Approve)` over meta (expects
`AuthorizationApprovalRecorded`); then re-reads via working-socket `ObserveAuthorization`
(root.rs:219) to confirm the verdict resolved to Authorized/Granted. With that bin in
the `cluster-witness` package, the test is one more `mkCriomeClusterTest` call with
`witness = "criome-client-approval-witness-test"` — no generator change.

## (d) Repointing the criome input from the auto-approve branch to main

Current pin: `CriomOS-test-cluster origin/criome-cluster-test:flake.nix:49` —
`criome.url = "github:LiGoldragon/criome/criome-auto-approve"`.

The `criome-auto-approve` branch has exactly ONE commit not on criome main
(`e80e206`: auto-approve verdict mode + meta Configure + the
`criome-auto-approve-witness-test` bin). Its runtime half is fully subsumed by main —
criome main's `root.rs`/`daemon.rs` carry the AutoApprove short-circuit (root.rs:325),
the meta `Configure` applying `authorization_mode` (root.rs:290, 308), and then the
entire ClientApproval/park surface ON TOP (root.rs grew 303 lines vs the branch). So the
ONLY thing main lacks from the branch is the `criome-auto-approve-witness-test` BINARY
(`src/bin/criome-auto-approve-witness-test.rs`, present on the branch, absent on main).

Therefore repointing the input requires: (1) operator ports
`criome-auto-approve-witness-test.rs` onto criome main behind the `cluster-witness`
feature (add the `[[bin]]` stanza to Cargo.toml, mirroring the branch); (2) change the
test-cluster flake input to `github:LiGoldragon/criome/main` and re-lock; (3) the two
existing checks keep their witness names unchanged. Once landed, the `criome-auto-approve`
branch is fully retireable. (The same port should add the new
`criome-client-approval-witness-test` from part (c) in the same pass, so main carries all
three witness bins.) Note the input comment at lines 42-48 already anticipates this:
"Operator repoints to main once the runtime lands there" — the runtime HAS landed; only
the witness bin port remains.

## (e) Path to extend members beyond 1 (future N-node quorum)

The generator is forward-shaped but the path is blocked at the transport layer.

- `mkCriomeClusterTest.nix:49-53` already `throw`s for `members > 1` and names the gap
  (Stage B multi-node quorum unbuilt). The generator builds exactly one
  `nodes.${member}` (line 82) and runs the witness against that one socket.
- The hard blocker is criome's transport: `criome origin/main:src/transport.rs` is
  `UnixStream`-only — both clients connect via `UnixStream::connect` (lines 233, 254),
  imported `std::os::unix::net::UnixStream` (line 2). There is no TCP/network listener or
  connector anywhere. This is the 701 E1 gap (cross-criome peer transport). Multi-machine
  quorum (701 E3) cannot be VM-proven until E1 lands: peer criome nodes on separate VM
  guests cannot reach each other.
- So the members-beyond-1 path is: (1) criome E1 — add a network transport (a TCP or
  Tailnet listener/connector alongside the Unix sockets) and peer-node addressing; (2)
  E2/E3 — cluster-root admission of peer master keys + the k-of-n quorum gather across
  peers; (3) generator change — emit N `nodes` with inter-node networking
  (`runNixOSTest` gives guests a shared test subnet automatically), seed each daemon's
  config with the peer set + ClusterRoot, drop the `members == 1` throw, and run a
  quorum witness that submits to one node and asserts k peer signatures resolve the
  verdict. `runNixOSTest` is the right substrate (it networks guests), so the harness
  change is mechanical once E1-E3 exist. The cluster-root admission ceremony branch
  (`origin/cluster-root-admission-ceremony`, carries a `criome-cluster-root` bin) is the
  start of E2.

## Smallest next VM test to write, and what blocks it

Smallest next test: `criome-cluster-client-approval` — one `mkCriomeClusterTest` call
with `name = "criome-cluster-client-approval"`, `members = [ "alpha" ]`,
`witness = "criome-client-approval-witness-test"`. It proves the third authorization
mode (the Track A operator just landed) end-to-end in a real VM: meta Configure to
ClientApproval, submit->park, observe-parked, approve-by-slot, resolve Authorized.

The ONLY blocker is the missing witness binary — the runtime and wire contract are
already on all three mains. Operator writes `criome-client-approval-witness-test.rs`
(behind the `cluster-witness` feature, copying the auto-approve witness's client setup),
then the test-cluster flake adds one check on the `criome-cluster-test` branch (or wherever
the criome harness is consolidated). No generator change, no networking, no new
infrastructure. This single test would give the ClientApproval park flow its first VM
proof, which the briefing notes it currently lacks ("cargo test green; no VM proof of the
park flow yet").

A close second, smaller in code but lower value: a per-Unix-user isolation test (the B7
follow-on) — a non-root service user + an assertion that a different unprivileged user is
denied the 0600 socket. That needs only a generator tweak (run as a dedicated user, add a
deny assertion), no new criome code.

## Cross-cutting observation: the criome harness is stranded off main

The harness branch `origin/criome-cluster-test` is 7 commits ahead of test-cluster main
and pins a criome FEATURE BRANCH (`criome-auto-approve`), while criome itself has moved
its runtime to main. The two greens reported in the commit logs are real but live only on
this side-branch; test-cluster main's CI (`nix flake check`) does NOT run them. Until the
branch is rebased and merged (after the witness-bin port in part d), the criome VM proofs
are invisible to anyone checking test-cluster main, and the harness drifts further from
both criome main and test-cluster main's evolving auto-pickup VM suite.
