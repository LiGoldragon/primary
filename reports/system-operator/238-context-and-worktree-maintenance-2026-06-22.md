# Context and worktree maintenance

System-operator maintenance pass on 2026-06-22 after the lojix contained deploy/test synthesis work.

## Scope

This pass refreshed:

- workspace intent and psyche-facing rules;
- orchestration state;
- primary `jj` state;
- system-operator POC worktrees from the lojix contained wave-0 work;
- canonical live lojix/CriomOS/goldragon/clavifaber checkouts;
- all visible `~/wt/github.com/LiGoldragon/*/*` jj worktrees for dirty-state awareness;
- reports touching the lojix contained deploy/test arc.

No Spirit capture: the psyche asked for maintenance and a best insight/question, not a new durable rule.

## Clean state confirmed

Primary is clean:

- `/home/li/primary`: no working-copy changes, `main` at `62af9cc1` when checked.

System-operator lane is idle:

- `orchestrate/system-operator.lock`: idle.

The four system-operator contained-test POC worktrees are clean:

- `/home/li/wt/github.com/LiGoldragon/schema-rust-next/system-operator-contained-test-poc`
- `/home/li/wt/github.com/LiGoldragon/lojix/system-operator-contained-test-poc`
- `/home/li/wt/github.com/LiGoldragon/signal-lojix/system-operator-contained-test-poc`
- `/home/li/wt/github.com/LiGoldragon/meta-signal-lojix/system-operator-contained-test-poc`

The relevant canonical `/git` checkouts are also clean:

- `/git/github.com/LiGoldragon/lojix`
- `/git/github.com/LiGoldragon/signal-lojix`
- `/git/github.com/LiGoldragon/meta-signal-lojix`
- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/goldragon`
- `/git/github.com/LiGoldragon/clavifaber`

## Active coordination state

System-designer still claims the live system integration slice:

- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/clavifaber`
- `/git/github.com/LiGoldragon/goldragon`
- `/git/github.com/LiGoldragon/lojix`
- `/git/github.com/LiGoldragon/meta-signal-lojix`
- `/git/github.com/LiGoldragon/signal-lojix`

That means downstream operator convergence on the lojix contained contract should either wait for that lane to release or use separate worktrees and explicit coordination.

Other active lanes:

- `cloud-operator`: `/git/github.com/LiGoldragon/CriomOS-test-cluster`
- `schema-operator`: schema-help correction across `schema-next`, `signal-spirit`, `spirit`
- `cloud-maintainer`: `/git/github.com/LiGoldragon/cloud`
- `designer`: `mentci-lib` re-found work

## Dirty worktrees found

The broad `~/wt` pass found these uncommitted worktrees. I did not touch them; they appear to be peer or older feature work:

| Worktree | Dirty paths summary |
|---|---|
| `CriomOS/enable-vm-hosting-prometheus` | `modules/nixos/test-vm-host.nix` |
| `CriomOS/prometheus-vm-host` | VM-testing/check cleanup and `flake.nix` / `criomos.nix` edits |
| `criome/attested-moment-majority-guard-139` | `src/language.rs`, `tests/language.rs` |
| `criome/criome-client-approval-witness` | witness binaries and `Cargo.toml` |
| `goldragon/prometheus-vm-host` | `datom.nota` |
| `meta-signal-spirit/structural-forms-integration` | schema/toolchain pins |
| `schema-next/help-codec` | `src/source.rs` |
| `schema-rust-next/structural-forms-integration` | many fixture/schema migration files |
| `signal-criome/signal-criome-peers` | schema and generated code |
| `signal-introspect/trace-introspect-slice` | contract and tests |
| `signal-spirit/help-codec` | help implementation/tests |
| `signal-spirit/structural-forms-integration` | schema/toolchain pins |
| `spirit/structural-forms-integration` | nexus/sema schema/toolchain pins |

Two entries reported `No working copy`:

- `meta-signal-criome/criome-meta-authz`
- `signal-criome/criome-meta-authz`

Those are not system-operator dirt, but they are worth later cleanup if the owning lane considers those worktrees abandoned.

## Context maintenance finding

The report stack now has two overlapping visual syntheses:

- operator report 237: `reports/system-operator/237-lojix-contained-deploy-test-visual-synthesis-2026-06-21.md`
- designer report 161: `reports/system-designer/161-state-of-lojix-unified-deploy-test-visual-reassessment-2026-06-21.md`

Designer report 161 is the stronger canonical wide-angle map. It incorporates the operator wave-0 proof, the same verb grammar, the authoring layer, intent records, wave plan, and explicit answers to operator report 236's open questions. Operator report 237 remains useful as an operator-lane snapshot and proof/debt framing, but new readers should treat designer 161 as the current visual design synthesis.

The one material design difference is `RunContainedCluster` placement:

- operator 237 leaned helper/client first, then promote if repeated use proves it;
- designer 161 recommends public `signal-lojix` root, daemon-orchestrated, because a networked cluster test needs members co-live before the gate runs.

After re-reading the cluster authoring context, designer's position is stronger. The co-live requirement is not just ergonomic; it changes ownership. A client helper can emit per-node triples, but it cannot naturally own the cluster-wide liveness window, release-all semantics, and failure cleanup as one durable operation. That belongs in the daemon contract once the lower roots are honest.

## Best insight

The next integration cut should stop treating `RunContainedCluster` as a convenience layer. It is a lifecycle coordinator. If it remains a thin client helper, it will either duplicate daemon state logic or fail the first time one member deploys, another member fails verification, and release must be coordinated across the whole cluster. The right layering is:

1. first fix the lower ordinary contract (`DeployContained / VerifyContained / Release / Query`, authoritative `source`, SEMA/Nexus paths);
2. then add `RunContainedCluster` as a public ordinary root that lowers inside lojix and persists one cluster-run record linked to per-node contained runs.

This preserves the typed public interface and gives the daemon one place to guarantee co-live setup, teardown, restart reconciliation, and queryable cluster-level history.

## Best question

Should we explicitly mark operator report 237 as superseded-by or companion-to designer report 161, so future agents do not treat two visual maps as competing canon?

My recommendation: add a short banner to report 237 saying designer 161 is the canonical wide-angle design synthesis, while report 237 is retained as the operator proof/debt snapshot. That is documentation maintenance, not design churn.
