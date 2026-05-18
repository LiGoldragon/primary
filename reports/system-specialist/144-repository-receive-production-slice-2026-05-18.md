# Repository Receive Production Slice

Date: 2026-05-18  
Role: system-specialist  
Source plan: `reports/designer-assistant/121-post-push-repository-ledger-and-ad-hoc-git-server-2026-05-18.md`

## What Landed

This pass implemented the production CriomOS side of the local repository
receive plan.

Commits pushed:

- `horizon-rs` `036b175c` — `NodeServices.personaDevelopment` with
  `Workstation { repositoryReceive }`, plus decode/projection witnesses.
- `goldragon` `cc1fa9ad` — enables the role only on `ouranos`; all other
  nodes keep `None`.
- `lojix-cli` `b398cbac` — repins `horizon-lib` so production deploy tooling
  can parse the new service role.
- `CriomOS-home` `36e7b43f` — repins `lojix-cli` in the user profile lock.
- `CriomOS` `433a77f2` — adds the gated Gitolite receive service and hook
  spool module.
- `CriomOS` `7b6ff9b6` — repins `CriomOS-home` so full OS builds see the new
  user-profile lock.

## Production Shape

The cluster fact is now a typed Horizon role, not a node-name predicate:

```nota
(NodeServices
  Client
  (Server 8443 "tailnet.goldragon.criome")
  (Workstation (RepositoryReceiveRole true)))
```

CriomOS reads the projected JSON at
`horizon.node.services.personaDevelopment.Workstation.repositoryReceive`.
If that role is present, CriomOS enables NixOS `services.gitolite` with:

- `dataDir = "/var/lib/gitolite"`;
- initial `adminPubkey` from `horizon.node.adminSshPubKeys`;
- one common `post-receive` hook;
- durable spool directory at `/var/lib/repository-ledger/spool`.

The hook fails open. It writes a NOTA-shaped
`RepositoryReceiveHookNotification` containing repository name, gitolite user,
receive timestamp, daemon-socket-presence bit, and Git's standard
`old new ref` rows. The hook does not trust itself as ledger truth; the future
daemon must read the canonical bare repository before committing ledger rows.

GitHub mirroring is intentionally absent from this slice.

## Validation

Passed:

- `horizon-rs`: `CARGO_BUILD_JOBS=2 cargo test -p horizon-lib`
- `lojix-cli`: `CARGO_BUILD_JOBS=2 cargo test`
- CriomOS direct Nix witness:
  `repository-receive-role-policy`
- Projected `goldragon/ouranos` with `horizon-cli` and confirmed
  `services.gitolite.enable == true` under full CriomOS module evaluation.
- Projected `goldragon/prometheus` and confirmed
  `services.gitolite.enable == false`.
- `nixfmt --check` on the touched CriomOS Nix files.

Known test caveat:

- `horizon-rs` has pre-existing `cargo fmt --check` failures across untouched
  files. I formatted only files touched by this slice.
- `nix build .#checks.x86_64-linux.repository-receive-role-policy` through the
  CriomOS flake output still requires overriding the default `system` and
  `horizon` stub inputs, and the broader flake check set can force those
  stubs. I built the check directly through `pkgs.callPackage` and also did a
  real module evaluation with projected Horizon input.

## Pre-Existing Dirty Repair

`goldragon/datom.nota` had a pre-existing uncommitted edit adding country and
SSID fields to `RouterInterfaces`. Production `horizon-rs/main` has no such
fields, so that dirty edit made the cluster proposal unparsable. It also
conflicted with the earlier decision that router SSID is derived by Horizon
from the cluster, not authored in cluster data. I removed those extra fields
while adding the repository receive role.

## What Is Not Done

The remaining report-121 work is no longer just "production CriomOS":

- create the `repository-ledger` triad repo;
- create `signal-repository-ledger`;
- decide whether `permission-signal-repository-ledger` exists in the first
  implementation or waits for a real delegated operator;
- create `owner-signal-repository-ledger`;
- implement the daemon's sema-engine tables;
- implement owner registration of repositories;
- implement normal recent-push queries;
- connect the Gitolite hook to the daemon once the daemon exists;
- replay the spool on daemon startup;
- import refs and commit metadata from the canonical bare repository.

The production OS can now host Gitolite and preserve receive notifications in
a durable spool. The actual ledger component is the next boundary.

## Best Question

Should system-specialist continue into the new triad component repos, or should
operator own `repository-ledger` / `signal-repository-ledger` implementation
while system-specialist keeps only the CriomOS packaging and deployment
surface?

My lean: operator owns the Rust triad implementation; system-specialist owns the
NixOS module, Gitolite integration, local deployment, and later service
packaging once the component exists.

