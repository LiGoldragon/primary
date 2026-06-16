# 53 — Proposal: vmtest auto-pickup + standard fallback + the NOTA-CLI client

For psyche confirmation BEFORE building. Synthesizes the three groundings
(autopickup, node↔vmhost model, nota-cli-client). The five open decisions
needing a yes/no are collected in §6.

## 0. The one-paragraph shape

Stop hand-listing checks: the flake iterates the Pod-on-a-VmHost set the
projection already names and generates one check per node, so **declaring
a node IS getting a test**. A node with no custom entry gets a **standard
fallback** test (boot + sshd + role-basic invariants, derived from its
projected `behavesAs` facets); a node in a small **custom registry**
(today's desktop and home anchors) overrides with its bespoke script. The
vmhost is **not** a runtime override — it stays fixed per guest via
`super_node`; "test certain nodes on certain vmhost" means *selecting the
(hostNode, guest) pairings the cluster data declares*, with `hostNode` the
free seam that already exists. Prometheus becomes a selectable vmhost by a
**data-only** edit (append one `VmHost` service line) plus a guest pinned
to it — host-untouched, never deployed. A new thin **`vmtest`** CLI takes
exactly one NOTA `Test` request (one-argument standard) and dispatches to
the hermetic `runNixOSTest` checks and/or the report-51 live run.

## 1. Auto-pickup suite (the directive's "automatically pick up the nodes configured")

### 1.1 The mechanism — a flake-level iteration, generator untouched

Replace the four literal call sites (`flake.nix:115-234`) with a generated
attrset. `mkVmTest` itself does not change; its `hostedPodNamesOf`
(lib/mkVmTest.nix:132-142) already encodes the exact pickup predicate.

1. **Read the host projection once.** `hostHorizon = readHorizon hostNode`
   — the same `fromJSON (readFile fixtures/horizon/<node>.json)` the
   generator uses.
2. **Enumerate the hosted Pod set.** Fold `hostHorizon.exNodes` on
   `machine.species == "Pod" && machine.superNode == hostNode`. For atlas:
   `[base-home dune edge-desktop mercury]`, sorted, zero authoring.
3. **Generate one check per node.**
   `lib.genAttrs hostedNodes (vmNode: mkVmTest { cluster; hostNode; vmNode;
   testScript = <resolved>; ... })`, check name `vm-<vmNode>` (the named
   anchors keep their invariant-named keys — see §1.3).
4. **Capacity/subnet safety comes free.** `assertModel`
   (mkVmTest.nix:294-306) already fails at eval if the hosted set exceeds
   `VmHost.maximumGuests` or overflows `guestSubnet` — auto-generation
   cannot silently over-subscribe.

**The immediate payoff: dune.** dune is an Edge Pod-on-atlas
(fieldlab.nota:80-83) with **no check today** — exactly the gap auto-pickup
closes. The moment iteration runs, dune auto-gains the Edge standard
fallback (§1.2). That single new green check is the visible proof the
mechanism works.

### 1.2 The standard-test fallback (the directive's "fallback to … the standard test")

The fallback is the default `testScript` a node gets when no custom entry
exists. It is **derived from the node's projected `behavesAs` facets**, so
a newly-declared node of any role gets a meaningful default with no
authoring. A small **facet → fragment** table in the flake's `lib`,
concatenated for the facets the node's projection has set:

| layer | gate | asserts | distilled from |
|---|---|---|---|
| universal base | every node | `wait_for_unit("sshd.service")` + `is-active sshd` | today's `test-vm-guest-boots-sshd` |
| desktop | `behavesAs.edge` | `dbus.service`, `greetd.service` up | `edge-desktop-boots-greeter` |
| router | `behavesAs.router` | `hostapd` + `kea-dhcp4-server` active; `ip_forward=1` | report-50 §4.2 T3 |
| large-ai | `behavesAs.largeAi` | `<node>-llama-router.service` present + wanted | report-50 §4.2 T4 |
| home | `includeHomeResolved` | `home-manager-<user>.service` active | `base-home-activates` |

A lean `testVm` (mercury) gets just boot+sshd — its current behavior,
preserved. An Edge node (dune) gets boot+sshd+dbus+greetd. The home layer
keys off `mkVmTest`'s already-computed `includeHomeResolved`
(`!guestIsTestVm` by default, mkVmTest.nix:291-292), so the standard test
agrees with the home profile the generator actually built. **No router /
large-ai Pod exists in fieldlab today**; those rows are ready for one.

### 1.3 Custom tests coexist via a per-node registry that overrides

A `customTests` attrset keyed by node name, holding only nodes that need a
bespoke test. Per-node resolution:
`customTests.${vmNode} or { testScript = standardTestFor (behavesAs); }`.

```nix
customTests = {
  edge-desktop = { testScript = ''<the greetd/niri/keyring assertions>''; };
  base-home    = { includeHome = true; testScript = ''<the ~/.config/git/config assertions>''; };
  # mercury, dune: absent -> standard fallback
};
```

The existing `edge-desktop-boots-greeter` and `base-home-activates`
anchors MOVE here verbatim (keeping their invariant-named check keys and
their rich assertions; the override entry can carry any `mkVmTest` knob —
`includeHome`, `substrate`, `extraGuestModules`). mercury and dune fall
through to the standard fallback. This is the single coexistence seam:
declaring a node gets a standard test; adding a registry entry replaces it
with a richer one. One-concept-per-test (Spirit `[xxgp]`) is preserved —
anchors stay named, hand-authored, single-concept.

### 1.4 The deploy smoke stays one explicit call

`lojix-deploy-smoke` (`mkDeployTest`, C6) is deploy-MACHINERY, proven
exactly once (INTENT.md; report-50 §3.2). It is **NOT** in the per-node
iteration — it stays one explicit call site for one representative node
(mercury), outside the `mkVmTest` loop.

## 2. The node↔vmhost model (runtime parameter, or fixed?)

**Recommendation: the vmhost is FIXED per guest via `super_node`, not a
runtime override. "Selection" = pairing `hostNode` with a guest whose
`super_node` matches — not mutating `super_node` per run.**

The host edge lives in one field of the guest's `Pod` substrate:
`super_node` (the 5th `Pod` field; mercury = `(Some atlas)`,
fieldlab.nota:108). It is validated at projection
(`validate_pod_super_node`, horizon-rs node.rs:608-626 →
`Error::MissingSuperNode`) and the generator *asserts* the host actually
hosts the guest (mkVmTest.nix:301). A runtime override that re-points
`super_node = chosenHost` after projection would bypass both invariants
and desync the guest's projected `exNodes`/arch from the host it runs on.
The C1 invariant exists precisely to keep the graph total; overriding it
defeats it.

So `hostNode` is the free generator seam (mkVmTest.nix:188) — it is the
single line that retargets atlas → prometheus. To test the *same logical
node on two hosts*, declare **two sibling guests sharing a profile**, one
per host (e.g. `mercury-on-atlas`, `mercury-on-prometheus`), each a
validated graph edge. The C5 relaxation already lets any Pod-on-VmHost
node be a `vmNode` (any role), so the sibling need not be a lean TestVm.

### 2.1 Where the test-VM nodes are declared (keeping goldragon clean)

Two options. The grounding splits them; this is the **single biggest open
decision** (§6, Decision B):

- **Option A — declare VmHost + guests directly in `goldragon/datom.nota`.**
  The *truest* reading of the directive's "declared in goldragon." Cost:
  new plumbing — a second `--cluster goldragon` projection path in
  `projections-match-*`, committed `fixtures/horizon/prometheus.json` +
  guest fixtures, and `readHorizon`/`fixtureSystem` parameterized by
  cluster (today they assume the single fieldlab set). It is purely
  *additive* plumbing, NOT a model change, and it puts production cluster
  data as the source of truth.
- **Option B — a test-surface proposal that NAMES Prometheus as the host.**
  Declares a `prometheus` host node + its guests in the test surface the
  generator already projects (like fieldlab). Production goldragon stays
  free of any test capability; minimal plumbing (reuses the
  `--cluster fieldlab`-style machinery). Tension: the directive says
  "declared in goldragon" — B declares it in a test surface that *names*
  Prometheus, not in goldragon literally.

**Recommendation: A is the right target because the psyche said "declared
in goldragon" explicitly** — production cluster data as the source of
truth, with the host-untouched run guaranteeing no production effect. B is
the faster interim if the psyche accepts "a test surface that names the
real Prometheus node" as honoring the intent. Both drive the *identical*
host-untouched live run; the only difference is where the data lives and
the projection plumbing. This is the one decision that gates the
implementation order.

### 2.2 Both atlas and prometheus selectable

Once each carries a `VmHost` service in its projected data, the host is
selected purely by the `hostNode` arg + a guest whose `super_node`
matches:
- atlas: already selectable (`hostNode = "atlas"` + mercury/edge-desktop/
  base-home/dune).
- prometheus: selectable once §3 lands (`hostNode = "prometheus"` + ≥1
  guest with `super_node = prometheus`). No generator code changes —
  `hostNode` is the designed seam.

## 3. Prometheus as a vmhost (data only, host-untouched)

Append to Prometheus's goldragon service vector (currently
`[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`, verified at the
bottom of its `datom.nota` declaration) the line atlas already carries
(fieldlab.nota:29):

```
[(TailnetClient) (NixBuilder (Some 6)) (NixCache) (VmHost [169.254.100.0/22] Available (Some 4))]
```

- `guest_subnet` `[169.254.100.0/22]` — **link-local**, never routed,
  no overlap with Prometheus's routed space (`5hir5bnz`-inert); the same
  CIDR atlas uses and `test-vm-host.nix` slices per-guest taps from.
- `kvm` `Available` — Prometheus has `/dev/kvm` (report 48 preflight);
  required so C2's `mkIf (hasGuests && kvmAvailable)` fires.
- `maximum_guests` `(Some 4)` — a ceiling asserted-not-exceeded at eval,
  not a reservation.

Adding a `NodeService` does **not** change Prometheus's species
(`LargeAiRouter` stays) and is **inert until a deploy — and the plan never
deploys** (report 51 §2): the live run materializes the C2/C3-generated
runner + tap inside `unshare -rn`, host netns byte-identical. Plus ≥1 guest
with `super_node = prometheus` (placement per Decision B). The client must
hard-refuse the system-config-deploy modality on Prometheus — the live
router is never `nixos-rebuild`'d, only host-untouched.

## 4. The NOTA-CLI client script (`vmtest`)

### 4.1 Shape: a thin NOTA-speaking CLI, NOT a triad daemon

The psyche said "client script," and the triad standard agrees: this thing
holds **no durable single-writer state** — it parses one NOTA request,
shells out to `nix build`/`runNixOSTest` or `ssh + systemd-run --user`, and
exits. It is the same carve-out as `horizon-cli` ("a test CLI … is
convenience, not a triad", component-triad.md). Building a daemon here
would invent state where there is none.

- **Binary name: `vmtest`** — the verb the human types; lives in
  CriomOS-test-cluster beside `scripts/run-on-prometheus`. NOT
  `<component>-cli`, NOT a daemon, no `vmtest-daemon`.
- **One argument, no flags** (component-triad.md "The one argument rule"):
  one inline NOTA `Test` string (shell **double**-quoted) or a path to a
  `.nota` file. Mode/host/node-selection/substrate are all typed FIELDS in
  the record, never flags.
- **It is a CLIENT of the lojix CLIs** in live/deploy modes — it shells to
  `meta-lojix`/`lojix` exactly as `mkDeployTest`'s testScript does,
  inheriting their env-var socket convention
  (`LOJIX_OWNER_SOCKET`/`LOJIX_ORDINARY_SOCKET`; env vars are a NOTA host,
  not flags).
- **NOTA is parsed by a typed decoder, never hand-rolled in shell**
  (no-hand-rolled-parsers rule). Recommended: a **tiny `TestRequest`
  decoder** (a small typed front-half) whose back-half shells to
  `nix`/`ssh`/`meta-lojix`. The `Test` schema lives in
  CriomOS-test-cluster (test-surface vocabulary, not a wire contract any
  daemon speaks).

### 4.2 The `Test` request shape (positional, full-English, no tail-omission)

The "standard-test fallback" cannot be a defaulted/missing field
(nota-design.md:263 forbids tail-omission). So it is a **distinct shorter
variant**, not an under-filled struct. The CLI argument is a `Test` enum
with two variants:

```
;; full form — explicit nodes + mode
(Run fieldlab atlas (Nodes [mercury]) Hermetic)

;; standard-test fallback — cluster + host only; the decoder EXPANDS
;; this to (all hosted Pods, Hermetic)
(Standard fieldlab atlas)
```

Schema (positional struct bodies; the file/CLI position supplies the root
`Test`, so the CLI sees `(Run …)` / `(Standard …)` directly):

```schema
[(Run RunRequest) (Standard StandardRequest)]
{
  RunRequest      { ClusterName HostNode NodeSelection TestMode }
  StandardRequest { ClusterName HostNode }
  NodeSelection   [(Nodes [NodeName]) All]
  TestMode        [Hermetic Live Both]
  ClusterName     String
  HostNode        NodeName
  NodeName        String
}
```

- **`ClusterName`** — bare atom (`fieldlab`, or `goldragon` under
  Decision-B-A). The cluster the projections come from.
- **`HostNode`** — bare atom naming the vmhost (`atlas`, `prometheus`) —
  the directive's "certain vmhost." Read exactly as `mkVmTest`'s
  `hostNode`.
- **`NodeSelection`** — the "certain nodes" axis: `(Nodes [<name> …])` for
  an explicit list, or bare `All` (a unit variant) to sweep every
  Pod-on-`HostNode` guest (the `hostedPodNamesOf` set).
- **`TestMode`** — three variants (a real interface):
  - `Hermetic` — the auto-generated `runNixOSTest` check(s); zero host
    effect; the everyday default.
  - `Live` — the report-51 host-untouched on-demand cycle on the real
    `HostNode`; touches the vmhost (user-level only).
  - `Both` — `Hermetic` as the cheap gate, then `Live`.

`StandardRequest { ClusterName HostNode }` *structurally means* "all
hosted nodes, hermetic" — the fallback is a real variant whose meaning the
decoder expands, never a silently-defaulted field. (All identifiers are
full English words per AGENTS.md; records positional, no `(key value)`.)

### 4.3 Dispatch

The decoder turns the one NOTA argument into the `Test` enum; the script
dispatches and prints a NOTA reply (e.g.
`(TestRun (Results [(Passed mercury) (Failed edge-desktop)]))` or a typed
rejection `(TestRejected (HostDeclaresNoVmHost atlas))`).

- **Node expansion.** `(Standard c h)` and `(Run c h All _)` expand to the
  host's hosted Pod set (read `fixtures/horizon/<h>.json`, the
  `hostedPodNamesOf` filter). `(Run c h (Nodes […]) _)` uses the listed
  names, asserting each is a Pod on `h`.
- **`Hermetic`.** For each node, build the corresponding pre-declared
  check: `nix build .#checks.<system>.vm-test-<cluster>-<node>
  --print-build-logs` (check name `vm-test-${cluster}-${vmNode}`,
  mkVmTest.nix:356). The script stays a pure dispatcher — it selects
  pre-declared checks by name, no nix authoring at runtime. Zero host
  effect.
- **`Live`** (the report-51 §3 cycle, the one mode that touches the host):
  1. `nix build` the generated runner
     (`<hostNode>.config.microvm.vms.<node>.config.config.microvm.declaredRunner`)
     — on a builder, zero host effect.
  2. `ssh <hostNode-fqdn>` + a durable `--user` unit: `unshare -rn`,
     create the additive `vmt<i>` tap **inside** the private netns with the
     C2-computed link-local `/32` sliced from `VmHost.guestSubnet`, run
     `declaredRunner` under `nsenter`.
  3. Start the fixed lojix daemon (`lojix-write-configuration → rkyv →
     lojix-daemon`, sockets 660/600) as a `--user` unit inside the netns,
     submit the deploy:
     `meta-lojix '(Deploy (System (<cluster> <node> FullOs /dev/null
     path:<src> Boot None [] (Some <buildAttribute>))))'`.
  4. Assert: `lojix '(Query (ByNode (<cluster> <node> None)))'` and check
     the durable terminal record.
  5. `systemctl --user stop` — tap + route vanish with the namespace; host
     netns byte-identical (`5hir5bnz`).
- **`Both`.** Hermetic across the selection; only if all pass, `Live`.
- **Gates.** `Live`/`Both` on `HostNode == prometheus` is gated behind
  explicit psyche authorization (report 51 §5). The script refuses
  `Live`/`Both` on a host whose projection has no `VmHost` service, with a
  typed rejection.

### 4.4 Why hermetic ≠ live cannot collapse (kept distinct)

Hermetic proves role/profile CONTENT (a function of the cluster model,
under `runNixOSTest` direct kernel boot, no real host touched — the
`VmHost` data is still read for KVM/TCG + capacity + endpoint derivation,
but no tap is wired). Live proves deploy MACHINERY + real-substrate
fidelity (report-48/49 cycle on the actual host). `-M microvm` and
`runNixOSTest`'s PCI backdoor cannot compose (report 52 §3): hermetic uses
qemu-vm.nix direct-boot, live uses the real microvm.nix runner. The
`substrate` field selects only the C3 guest-module prebake set in hermetic;
in live it selects the machine type. If a request must carry substrate
explicitly later, add a `Substrate [Microvm Uefi]` field to `RunRequest` —
but the standard fallback keeps it implicit (hermetic → microvm prebakes).

## 5. Implementation order (on ~/wt feature branches; operator integrates)

Designer lanes ship `next`/feature branches under `~/wt/...`; operators own
main + rebase. Order chosen so each step is independently green:

1. **CriomOS-test-cluster — auto-pickup + standard fallback + registry**
   (§1). Pure flake-level change on `horizon-test-vm`; `mkVmTest`
   untouched. Move the two anchors into `customTests`; iterate
   `hostedPodNamesOf atlas`; add the facet→fragment table. **Net new green
   check: dune.** Independently verifiable on atlas alone — no Prometheus
   dependency.
2. **The `vmtest` CLI + `Test` schema** (§4). A tiny typed `TestRequest`
   decoder + dispatch back-half, in CriomOS-test-cluster. `Hermetic` mode
   first (drives step-1 checks by name); `Live`/`Both` wired to the
   report-51 runner. Replaces/supersedes `scripts/run-on-prometheus`'s raw
   role.
3. **Prometheus VmHost data + guest** (§2.1, §3) — **GATED on Decision B
   (A vs test-surface) and the §6 confirmation.** Under A: the
   `goldragon/datom.nota` edit + the `--cluster goldragon` projection
   plumbing + committed `fixtures/horizon/prometheus.json`. Under B: the
   test-surface proposal naming Prometheus. Either way the `hostNode =
   "prometheus"` retarget is then a one-arg `vmtest '(Standard goldragon
   prometheus)'` (or `'(Run … Live)'`).
4. **First live Prometheus run** — only after step 3 lands AND the psyche
   confirms the live-on-Prometheus gate (report 51 §5 step 6). This is the
   single irreversible-ish action; everything before it is host-untouched
   by construction.

Operator integrates each branch to main + rebases; designer does not push
code-repo main.

## 6. Open decisions needing psyche confirmation

| # | Decision | Recommendation | Why it needs you |
|---|---|---|---|
| A | **Auto-pickup + standard fallback + registry** as in §1 — declaring a node = getting a test; mercury/dune fall to standard, anchors move to `customTests`. | Yes, build it. | Confirms the suite stops being hand-listed and dune gains a check by declaration alone. |
| B | **Where the test-VM nodes live: Option A (declare VmHost + guests in `goldragon/datom.nota`) vs Option B (a test-surface proposal naming Prometheus).** | **A** — you said "declared in goldragon"; production data as source of truth, host-untouched run guarantees no production effect. B is the faster interim if a test-surface that *names* Prometheus honors the intent. | The single biggest fork; gates step 3's plumbing. Both drive the identical host-untouched run. |
| C | **vmhost is FIXED via `super_node`, not a runtime override**; "same node, two hosts" = sibling guest declarations. | Yes — runtime override would bypass the validated graph + generator assert. | Confirms the model: "test X on host Y" is a cluster-data pairing, not a per-run mutation. |
| D | **The `Test` NOTA shape** — `[(Run RunRequest) (Standard StandardRequest)]`, `TestMode [Hermetic Live Both]`, fallback as the `Standard` variant (not a defaulted field). Binary named **`vmtest`**, a thin client (not a daemon). | Yes. | Confirms the typed request surface + that "standard test fallback" is the `Standard` variant, and the name. |
| E | **The Prometheus live-run gate** — append `VmHost` (data only, inert, never deployed); the FIRST live run on Prometheus needs explicit per-run authorization; the client hard-refuses any system-deploy modality on the live router. | Yes to the data edit now; live run gated per report 51 §5. | The one host-touching action; explicit go-ahead required before step 4. |

Nothing in steps 1–2 touches Prometheus or production; they are safe to
build on confirmation of A/C/D. Step 3 waits on B; step 4 waits on E.
