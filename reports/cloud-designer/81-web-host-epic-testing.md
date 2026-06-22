# Web-host epic — testing developed on a stable branch

cloud-designer, 2026-06-22. Per the psyche: "work on a stable epic
worktree-branch on this. develop the testing side as well (you can look at
the work system-designer/operator has been doing)." This is the testing
increment, built in the operator/system-designer idiom, with one real bug
found and fixed along the way.

## The stable epic branch

`cloud-designer-web-host-epic` (CriomOS, worktree
`~/wt/github.com/LiGoldragon/CriomOS/cloud-designer-web-host-epic`, pushed),
based off the operator's `pi-operator-web-host-testing` so it inherits — and
does not fork — their module. The operator had already built:

- `modules/nixos/web-host.nix` — the real service-gated module: reads the
  `WebHost` payload off `horizon.node.services`, renders each site's
  `flake-input:<name>` source at build time with Zola into an immutable
  artifact, serves it through hardened nginx + ACME. It resolves the source
  model I had left open: sources are pinned flake inputs (reproducible,
  pure); a non-flake source is refused.
- `checks/web-host-policy/` — an eval-level check asserting the produced
  nginx/ACME config and the rendered artifact's content.

My job was the testing side, so I built on that rather than re-deriving it.

## What I developed (two testing styles, mirroring their patterns)

The workspace has two established test idioms: **eval-level `*-policy`
checks** (host-independent, like `mirror-role-policy`) and **VM-level
`runNixOSTest`** (like `lib/mkVmTest`). I added one of each for the web host.

- **`checks/web-host-serve` — the live VM proof.** A `runNixOSTest` (mkVmTest
  idiom) that boots a node carrying the `WebHost` service, brings up nginx,
  and curls the served site — proving the rendered markdown is actually
  *served* over HTTP, the integration the eval check can't reach. It also
  asserts the renderer (`zola`) is **absent from the running system** —
  proof of the build-time-render security model (nothing dynamic on the
  edge). Serves plain HTTP in the hermetic VM (ACME can't reach Let's
  Encrypt); production TLS is asserted by `web-host-policy`.
- **`checks/web-host-render-policy` — extended eval coverage.** What
  `web-host-policy` doesn't cover: multi-site projection (two sites → two
  vhosts), the per-site hardening headers on every vhost, and the two
  contract guards the module enforces by *throwing* — a non-flake-input
  source and an unsupported renderer — as `tryEval` regression tests. These
  pin the module's reproducibility-and-safety boundary.

Both wired into `flake.nix` checks.

## The bug the testing caught (and fixed)

Per the surface-bad-design principle (Spirit `t5qr`), developing the live
test surfaced a real defect in the shared fixture:

**The `web-host-policy` fixture had `config.toml` + `content/_index.md` but
no `templates/` directory.** Zola, finding no template, emits its "couldn't
find a template to render" *placeholder* page — the markdown never reaches
the output. So `web-host-policy`, which asserts the fixture text is in
`index.html`, was **failing to build** (red on the operator's branch right
now). Reproduced locally: the rendered `index.html` was Zola's welcome
placeholder, not the content.

Fix: added `checks/web-host-policy/site/templates/index.html` (a minimal
section template). After it, the render produces the real content and
`web-host-policy` builds green. This is on the epic branch and resolves the
operator's currently-red check — they should pull it onto their branch.

## Test status (run on the configured prometheus builder)

| Check | Kind | Status |
|---|---|---|
| `web-host-policy` (operator's) | eval | **green** — after the fixture fix |
| `web-host-render-policy` (mine) | eval | **green** — multi-site, headers, both contract guards |
| `web-host-serve` (mine) | VM (QEMU) | **driver type-checks green**; QEMU run gated on a `nixos-test`-capable host |

Build invocation (the operator's documented incantation, reports/pi-operator/13):
`nix build .#checks.x86_64-linux.<check> --override-input system path:/tmp/criomos-system-x86_64 --override-input horizon path:/tmp/criomos-horizon-minimal`.

## Second finding — the VM-testing host lacks the `nixos-test` feature

Running `web-host-serve` (and any `runNixOSTest`) needs a Nix builder
advertising the `nixos-test` supported feature. The configured prometheus
builder advertises `[big-parallel, kvm]` but **not `nixos-test`**, so the VM
run reports "Failed to find a machine for remote build! required features:
[kvm, nixos-test]." The QEMU boundary (Spirit `qnf8`) was respected
throughout — I never ran QEMU on this workstation (`--max-jobs 0`). To run
these VM checks, the VM-testing host's builder config needs `nixos-test` in
`supportedFeatures` — a system-designer/system-operator config item, flagged
for them.

## Where this sits

- horizon-rs `NodeService::WebHost` type: on main (`4a0e29f`).
- CriomOS module + tests: this epic branch (operator's module + my testing +
  the fixture fix).
- Remaining to land the live service: a goldragon `datom.nota` site for doris
  (goldragon locked, system-designer), the horizon-rs repin so the projection
  carries `WebHost`, and provisioning doris. The `nixos-test` builder feature
  is the gate on running the VM check in CI.

Bead `primary-unig` tracks the epic.
