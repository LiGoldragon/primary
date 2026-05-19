# Production Horizon Circle-Back

## Active Reports

- `reports/system-specialist/146-production-horizon-service-variant-rework-2026-05-19.md`
- `reports/system-specialist/145-persona-gitolite-server-production-shape-2026-05-19.md`

## Stale Report

- `reports/system-specialist/144-repository-receive-production-slice-2026-05-18.md`

Report 144 is now historical. It still describes the old
`Workstation (RepositoryReceiveRole true)` shape and the old
`NodeServices Client (Server 8443 "tailnet.goldragon.criome") ...`
record. The corrected production truth is in reports 145 and 146.

## Current State

Production is now on the service-variant Horizon shape:

- cluster data selects semantic variants;
- cluster data does not author tailnet ports or domains;
- Headscale port lives in `CriomOS-lib` as
  `constants.network.headscale.port`;
- `PersonaDevelopment [(GitoliteServer)]` gates the production
  Gitolite receive module;
- the stack was deployed to `ouranos` through `FullOs Switch` pinned
  to `CriomOS` `fcf6f09a`.

## Main Topic

The next real topic is not "fix Horizon shape" anymore. That is done
for the production slice.

The next topic is deciding where to continue from the Gitolite receive
slice:

- system-specialist can keep hardening the CriomOS packaging and live
  system behavior;
- operator should probably own the Rust triad implementation for the
  repository ledger daemon and signal contract.

## Best Questions

1. Should report 144 be deleted now that reports 145 and 146 supersede
   its production shape?
2. Should system-specialist create a BEADS item for operator to build
   the `repository-ledger` / `signal-repository-ledger` triad, or is
   that already covered by existing Persona work?
3. Do you want a live end-to-end Gitolite push test next, or should we
   wait until a real repository-ledger daemon exists?
