# 05 — Workload decision: native NixOS, `WorkloadSubstrate` removed

Date: 2026-05-12
Role: system-assistant
Resolves: open question from
  `reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md`
  §"Decisions still owed" (Ghost workload native vs OCI)
Rule landed: `skills/nix-discipline.md` §"Services are NixOS modules,
  not OCI workloads"

## Resolution

The Ghost workload — and every contained-node workload — is a
native NixOS service module. **Nix through and through.** OCI /
Docker / Compose are not peer choices; they are transitional debt
requiring an explicit sunset bead and typed cluster records before
they can land at all.

Because there is no longer an axis to choose along, the
`WorkloadSubstrate` enum proposed in plan 04 §P1.1 is dropped from
the horizon vocabulary entirely:

```rust
// REMOVED — do not add.
pub enum WorkloadSubstrate {
    NativeNixosService,
    OciContainer,
    SystemdService,
}
```

`ContainmentSubstrate` stays as plan 04 specified
(`NixosContainer | MicroVm`) — that names *how the node exists*,
which is a real axis. The workload running inside a contained node
is just Nix, like everything else on a CriomOS host.

### What changes in the plan

- **P1 (horizon vocabulary).** No `workload.rs` module. No
  `WorkloadSubstrate` field on `ContainedPlacement`. `placement.rs`
  stays as plan 04 specified.
- **P6 (Ghost).** The "native vs OCI" decision matrix in plan 04
  §P6.3 is moot. Ghost is a `Publication` node placed in a
  `NixosContainer`, and the workload inside that container is a
  CriomOS-owned `services/ghost.nix` module packaging Ghost from
  upstream sources. Plan 04 §P6.2 "Workload A" is the path.
- **Effort revision.** Plan 04 §P6.2 estimated the native path at
  ~1 week. That estimate stands. The ~2-day OCI bridge option no
  longer exists.

### What this implies for upstream-only-OCI services

When a service ships only as a Docker image, the CriomOS path is
to package the underlying binary natively. The Nix-shaped path
exists for every mainstream stack:

| Upstream language | Nix-native path |
|---|---|
| Node.js | `mkYarnPackage` / pnpm overlay |
| Python | `uv2nix` / `pyproject-nix` consuming a committed `uv.lock` |
| Rust | crane / naersk |
| Go | `buildGoModule` |
| static binaries | `pkgs.stdenv.mkDerivation` |

The packaging cost is real, paid once per service, and not
distributed across image tag bumps forever.

## Where the rule lives

The durable rule is in `skills/nix-discipline.md` §"Services are
NixOS modules, not OCI workloads" (workspace skill, agent-agnostic
home). The skill is required reading for every role; per
`skills/system-assistant.md` it is in the system-assistant /
system-specialist reading list. No per-repo `AGENTS.md` edit is
needed today; if a specific repo grows a service-shape exception
the AGENTS.md is the right place to record it.

## Status

The architecture is complete. Plan 04 + this report = the
implementation specification. Implementation is gated only on
the system-specialist's currently-held lock on
`/git/github.com/LiGoldragon/{horizon-rs,goldragon,CriomOS}`
(`align-tailnet-gating-with-designer-139-node-services`). When
the lock releases or narrows to file scope, P1 (new files
`horizon-rs/lib/src/{placement,capability,secret}.rs`) is the
natural first claim.

## Sources

- `reports/system-assistant/04-dedicated-cloud-host-plan-second-revision.md`
- `reports/designer-assistant/27-response-to-revised-dedicated-cloud-host-plan.md`
- `skills/nix-discipline.md` (updated this round)
- User direction this conversation: "native nixos service of course
  … we use nix through and through".
