# 53 — vmtest auto-pickup + the NOTA-CLI client: frame and method

## The psyche directive (verbatim)

> "the config should be wired to automatically pick up the nodes
> configured, with fallback to be test-run for the standard test, so we
> can have a script to test certain nodes on certain vmhost - we should
> make that 'client script' use nota cli standard."

Plus the framing fact: Prometheus's real goldragon service line is
`[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]` — **no VmHost**. The
psyche wants Prometheus to *be* a vmhost (declared in goldragon, run
host-untouched, never deployed to the live router — the gemma finding,
report 51 §2).

## What this report is

A concrete PROPOSAL for psyche confirmation, BEFORE building. Reports 50
(general VM-testing interface) and 51 (Prometheus live host) decided the
C1–C6 substrate; this report sits on top of it and decides four things
the directive newly asks for:

1. **Auto-pickup** — the flake stops hand-listing checks and iterates the
   declared test-VM nodes, generating one check per node. Declaring a node
   = getting a test.
2. **Standard-test fallback** — a node with no custom test gets a default
   boot+sshd+role-basic test script, derived from its projected
   `behavesAs` facets. A custom test (the desktop / home anchors)
   overrides via a per-node registry.
3. **The node↔vmhost model** — is the vmhost a runtime parameter, or fixed
   in the node's declaration? Where do the test-VM nodes live so the
   production goldragon model stays clean? How are atlas AND prometheus
   both selectable hosts?
4. **The NOTA-CLI client script** — a thin `vmtest` CLI taking exactly one
   NOTA `Test` request (one-argument component-triad standard), dispatching
   to the hermetic `runNixOSTest` checks and/or the report-51 live
   host-untouched run. Plus the Prometheus VmHost data edit.

## Method

Three parallel grounding sub-agents, each reading the live branches and
the prior reports:

- **autopickup** — the flake-level iteration mechanism, the standard
  fallback shape, the custom-override registry, against the existing
  `mkVmTest`/`mkDeployTest` helpers on `horizon-test-vm`.
- **node-vmhost-model** — the `super_node` binding, runtime-vs-fixed host
  selection, declaration-placement (goldragon-A vs test-surface-B), the
  Prometheus VmHost datum.
- **nota-cli-client** — the `TestRequest` NOTA shape (positional,
  full-English, no-tail-omission), the client-script dispatch to the
  hermetic and live backends, the one-argument-rule conformance, binary
  name.

All three landed complete grounding with exact file:line citations. The
synthesis (this directory's `4-proposal.md`) reconciles them into one
buildable plan with a single confirmation gate.

## The load-bearing constraints inherited (not re-litigated here)

- **The generator needs no change.** `mkVmTest`'s `hostedPodNamesOf`
  (lib/mkVmTest.nix:132-142) already IS the auto-pickup predicate, and
  `assertModel` (:294-306) already gives free capacity/subnet safety.
  Auto-pickup is purely a flake-level change.
- **One concept per test** (INTENT.md non-negotiable; Spirit `[xxgp]`):
  the named anchors (desktop greeter, home activation) stay hand-authored
  single-concept checks; standard fallbacks are node-named and assert one
  facet-derived invariant set.
- **The deploy smoke is proven once** (`mkDeployTest`, C6): it is
  deploy-MACHINERY, NOT auto-generated per node — one explicit call site.
- **Hermetic ≠ live.** Hermetic (`runNixOSTest`, direct kernel boot)
  proves role/profile CONTENT and touches no real host; live (report 51
  §3) proves deploy MACHINERY + real-substrate fidelity on the actual
  vmhost, user-level only. `-M microvm` and `runNixOSTest`'s PCI backdoor
  cannot compose (report 52 §3), so the two paths cannot collapse.
- **No tail-omission in NOTA** (nota-design.md:263): "fallback" cannot be
  a defaulted/missing field — it must be a distinct shorter request
  variant.
- **One NOTA argument, no flags** (component-triad.md "The one argument
  rule"): the mode/host/node-selection are typed fields inside the
  record, never CLI flags.
- **Prometheus is host-untouched** (report 51 §2): the live run
  materializes inside `unshare -rn`; the live router is NEVER
  system-deployed. The client must hard-refuse the system-deploy modality
  on Prometheus.

## Key source files (all absolute)

- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/horizon-test-vm/flake.nix:115-234` — the four hand-listed checks to replace with iteration.
- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/horizon-test-vm/lib/mkVmTest.nix:132-142,285-306` — `hostedPodNamesOf` (the auto-pickup predicate), `includeHomeResolved`, `assertModel`. No change needed.
- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/horizon-test-vm/lib/mkDeployTest.nix:111-115` — the C6 deploy smoke; keep ONE explicit call site.
- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/horizon-test-vm/clusters/fieldlab.nota:29,80-158` — atlas VmHost (:29) + the four Pod-on-atlas guests.
- `/home/li/wt/github.com/LiGoldragon/CriomOS-test-cluster/horizon-test-vm/scripts/run-on-prometheus` — the existing client script (emits descriptive NOTA but invokes raw nix flags); the NOTA-CLI-standard target.
- `/git/github.com/LiGoldragon/goldragon/datom.nota` — Prometheus production declaration; its service line ends `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`, no VmHost.
- `/home/li/primary/skills/component-triad.md` (one-argument rule), `/home/li/primary/skills/nota-design.md:261-263` (no tail-omission).
- `/home/li/primary/reports/cloud-designer/50-general-vm-testing-interface/`, `/home/li/primary/reports/cloud-designer/51-prometheus-live-vm-host/`, `/home/li/primary/reports/cloud-designer/52-lojix-and-vm-testing-synthesis.md`.
