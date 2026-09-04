# Independent audit — Wispr/Noctalia recovery

This account distinguishes this flow's direct, read-only observations from
historical subflow statements. A statement labelled **claim** was not repeated
as a fresh test or deployment by this audit.

## Audit 1 — immutable source chain

I read the checked-out producer, Home, and OS sources and their revision
metadata. The product revision consumed by the recovery is
`5e6156aa235fa17d6a3e34d1c97ad1d3f6999b9a` (Wispr Flow Linux); Home is exactly
`8021ae5d4428343624920330098641f772c9eece`; OS is exactly
`840ed01d1c73bb373fd694a49cca9d3007014f8b`. Home's `flake.nix` pins the
product revision, and OS's `flake.nix` pins the Home revision. A fresh
`jj git fetch` of the provider reported no later remote-main revision at the
time of this audit; if a later Beads-only descendant is published, it is not
the product revision pinned by these consumer commits.

The producer's changed test/verification surface includes
`tests/signed-payload-patches.bats`, `tests/verify-patches.bats`, and
`scripts/verify-patches.sh`; its commit subject is “Suppress Linux dictation
status-window recovery.” **Claim (the implementation subflow, preserved by
the main-flow log):** its executable test run had 41 failures before the fix,
then all 44 passed, and an independent immutable-remote check passed. This
audit did not rerun the historical red/green run, so it does not upgrade that
claim into a new witness.

## Audit 2 — deployment ledger and build boundary

Direct ordinary-socket queries show deployment 188 as
`UserEnvironment.Realize`, revision `840ed01d…`, terminal `Succeeded`, and
189 as `UserEnvironment.ActivateNow`, the same immutable revision, terminal
`Succeeded`. `Query.ByNode.(goldragon ouranos None)` identifies 189 as the
current live user-environment generation and records
`/nix/store/4idm37b4awlkk1yj3w6j61cn3a0hinih-home-manager-generation`.

The event-log re-query for positions 661–676 returns deployments 184–187:
their event positions are 661–675 and their terminal completed rows are
Succeeded. The accompanying `(4,7xx–4,8xx)` pairs are state markers, not
event-log positions. This corrects the prior ambiguity: positions 661–676
are distinct from the 4,8xx state markers; no event-history defect was
witnessed by this query.

**Claim (deployment/implementation subflows, preserved by the main-flow
log):** the final target and Home activation outputs built on the configured
remote builder. **Claim:** official OS check attributes were blocked before
their derivations by the unrelated eager MS2130 policy, while those target
and Home outputs built. The current OS source independently shows that the
MS2130 check asserts a selected-kernel review before its derivation body;
this audit did not rerun the historical remote builds.

## Audit 3 — live status consumer and window state

Read-only process, socket, configuration, and Niri queries show the running
Wispr executable from `wispr-flow-1.6.774+criomos.5`; both status and control
sockets are present mode 0600. A status-socket snapshot was `state: "idle"`
and `hands_free: false`. The Noctalia-owned process tree contains a continuing
consumer of the Wispr status socket, and `plugins.json` enables
`wispr-status`. Niri reports one `Wispr Flow` window, non-floating, and no
window whose title is `Status`.

No recording or hands-free verification was invoked by this audit. Those
controls therefore remain unverified.

## Sources

- `flows/4e296a/log.md` — originating main-flow account for the historical
  provider test, remote-build, deployment, and recovery statements; where
  those observations originate in an implementation/deployment subflow, this
  audit retains them as claims rather than re-witnessing them.
- Provider worktree
  `/home/li/wt/github.com/LiGoldragon/wispr-flow-linux/wispr-recovery-4e296a`:
  `jj log`, `jj git fetch`, revision `5e6156aa…`,
  `tests/verify-patches.bats`, `scripts/verify-patches.sh`.
- Home worktree
  `/home/li/wt/github.com/LiGoldragon/CriomOS-home/wispr-recovery-4e296a`:
  `flake.nix`, revision `8021ae5d…`.
- OS worktree `/home/li/wt/github.com/LiGoldragon/CriomOS/wispr-recovery-4e296a`:
  `flake.nix`, `checks/ms2130-uvc-aspect-quirk/default.nix`, revision
  `840ed01d…`.
- Typed ordinary records: `lojix 'Query.ByDeployment.(188)'`,
  `lojix 'Query.ByDeployment.(189)'`,
  `lojix 'Query.ByEventLog.(661 676)'`, and
  `lojix 'Query.ByNode.(goldragon ouranos None)'`.
- Live read-only observations: `ps`, `pstree`, `stat` on the two Wispr
  sockets, a one-snapshot `socat` status read, Noctalia `plugins.json`, and
  `niri msg -j windows`.
