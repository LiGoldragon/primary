# 6 — the staged production cutover plan

cloud-designer, 2026-06-11. Synthesis of the five grounded runs in this directory
(workflow `lojix-cutover-plan`) plus reports 38 (readiness) and 39 (the Stack-A
baseline). The highest-numbered file IS the synthesis. Every claim below is
grounded in a real build/eval this session unless marked otherwise.

## Where it stands, in one paragraph

The new lojix daemon's **build/eval spine is real and works end-to-end today** —
proven, not asserted: both binaries build, all 11 non-ignored tests pass, and all
**7 real-nix `--ignored` tests pass**, including a live `lojix-daemon` process
binding two sockets and round-tripping a client deploy request to `Deployed`, a
real `nix build` to a realized closure, and concurrent service (a 472µs query
answered while a deploy ran). So Stack B is a working runtime, not a stub. But it
**cannot deploy a real node**: the activate reject-guard is confirmed live and the
activate/copy effect bodies behind it are broken (unset `$CLOSURE`, no
`switch-to-configuration`, no signed copy, bare node name as ssh host). On top of
that the cutover is gated by four classes of work — (1) **hygiene** that the green
build hides (a 404'd `nota-codec.git` and a `triad-runtime` rename that red-build
any cold clone or `cargo update`; a daemon that parses NOTA at startup; no
SO_PEERCRED), (2) **build-correctness parity** (an OsOnly firmware-field flip
confirmed at eval level; the unmaterialized `secrets` input), (3) **the entire
operational surface that doesn't exist** (no Nix package, no systemd module, no
request-builder — and the thin client refuses inline NOTA, so it isn't
hand-drivable), and (4) **activation + durable state**. The good news the
grounding surfaced: **CriomOS is already orchestrator-agnostic** (it consumes the
four override inputs, not a lojix input), **only CriomOS-home pins lojix-cli and
only for the binary** (no eval-time coupling), and **zeus is a clean secret-free
first target that evaluates today**. So a first, narrow cutover is reachable
without solving every gate at once.

## Constraints that must hold before go-live (regardless of node)

These gate the privileged surface independent of which node ships first:

1. **Rkyv-only daemon startup.** The daemon currently parses inline NOTA / `.nota`
   from argv (`lojix-daemon.rs:17`, shown live: `lojix-daemon '(not valid nota
   %%%)'` → NOTA decode error). The hard override forbids daemons parsing NOTA.
   Restrict the entry to the `RkyvFile` variant; the bootstrap tool encodes the
   typed config to binary outside the daemon.
2. **Resolvable, explicitly-pinned engine deps.** `nota-codec.git` **404s** on the
   remote (`git ls-remote` → "Repository not found"); the build survives only on
   this machine's warm cargo cache. And `triad-runtime` HEAD renamed **every**
   `Actor*` symbol lojix imports → `Async*` and `DaemonConfiguration` →
   `BindingSurface` with no compat alias. A cold clone or `cargo update`
   red-builds. Pin every engine dep to an explicit rev (or a flake-level pin),
   resolve the dead `nota-codec` repo, and do the rename sweep as one coordinated
   bump. **No deploy host other than this warm workstation can build the lock
   today.**
3. **Signed-path copy + domain-resolved ssh host.** `copy_closure` omits
   `--substitute-on-destination` and targets a bare `node_name`; production needs
   `nix copy --substitute-on-destination --to ssh-ng://root@<node>.<cluster>.criome`
   or the target rejects unsigned paths under `require-sigs`.
4. **SO_PEERCRED on the owner socket.** Authority rests on socket file-mode alone
   (the daemon's own comment: "no peer-credential check yet — audit R3"). Add a
   uid/gid assertion before the owner socket carries real Deploy/Pin/Retire
   authority.
5. **Cutover discipline.** Both stacks run in parallel; switch one consumer / one
   node at a time; lojix-cli retires only when **every** consumer is covered.
6. **Substituter resolution lives in exactly one stack at a time.** lojix-cli
   resolved node-name → Yggdrasil URL+key horizon-side; the Stack-B wire carries
   substituters **pre-resolved**, with no owner for the resolution. Decide the
   owner (§ open decisions) before the first migration, and don't half-wire it.

## Watch-fors — production behaviors that silently diverge if missed

Five of the eight subtle Stack-A behaviors are **not handled** and will diverge
the moment the relevant path is enabled:

- **BootOnce rollback** — lojix-cli's headless-safe design (a PID-1
  `systemd-run --collect --wait` transient unit, `OLD` read from `bootctl status`
  *Current Entry*, reboot-1-lands-NEW/reboot-2-returns-OLD). The daemon has only
  enum routing, none of the mechanism. **Do not cut any node to BootOnce until
  ported and tested against a real bootloader.**
- **EFI reconcile** on Boot/Switch (`bootctl set-default` + clear one-shot) —
  `switch-to-configuration` writes `loader.conf` but not the EFI
  `LoaderEntryDefault`; without reconcile a stale prior one-shot can hijack the
  next boot.
- **Signed-path copy** (above; cross-listed).
- **Secrets flow** — existence-gated, filename-hardcoded (3 `.sops` files); breaks
  *eval* for router/LLM nodes (below).
- **Home-activation local fast-path** — skip ssh when the dispatcher already is
  the user on the node (the path that activated your home generation).

Two are fine: **content-addressed `path:?narHash`** materialization is faithful
for the three inputs it writes; the **Yggdrasil-preferred substituter URL** moved
upstream of the daemon (whoever builds the request must select it). And one is a
**trap**: do **not** add a wall-clock timeout on eval/build — lojix-cli runs cold
builds for hours by design; adding a cap *breaks* parity. The only kill/timeout to
add is **cancel-kill on the privileged activate ssh**, not on cold builds.

## The staged plan

Stages 0–2 are activation-independent and can proceed in parallel; stage 3 is the
first real cutover; stages 4–6 widen it. Stage 5 (durable state) is sequencing-
flexible — see open decision 2.

### Stage 0 — Hygiene (unblocks a cold/CI build and the privileged surface)
- Pin engine deps to explicit revs; resolve the `nota-codec.git` 404 (fork/rehost
  or migrate off it); land the `triad-runtime` `Actor*`→`Async*` /
  `DaemonConfiguration`→`BindingSurface` rename sweep + regen artifacts as one bump.
- Restrict daemon startup to `RkyvFile`-only; add a bootstrap encoder.
- Add SO_PEERCRED on the owner socket.
- **Exit:** a from-cold-clone `cargo build` is green on a machine that isn't this
  one; the daemon rejects inline NOTA; the owner socket checks peer creds.

### Stage 1 — Build-correctness parity
- Fix the OsOnly firmware field: `DeploymentInput::from_shape` OsOnly arm must emit
  `include_all_firmware: false` (the one wrong line, `schema_runtime.rs:1627`).
  Confirmed eval-level flip: `{daemon_OsOnly:true, lojixCli_OsOnly:false}`.
- (Defer-able if first cutover is secret-free) Add a `Secrets` MaterializationShape
  mirroring lojix-cli's `artifact.rs` (existence-gated on
  `<proposal>/secrets/router-wifi-sae-passwords.sops`, the 3 fixed filenames) and
  inject `--override-input secrets`.
- (CriomOS-side, optional, widens the first wave) Fix the `swapDevices.sizeMebibytes`
  → `.size` mismatch in `disks/preinstalled.nix:40` that blocks tiger/ouranos eval
  (a Stack-A bug, independent of lojix).
- **Exit:** `CriomOS/checks/metal-firmware-policy` passes for daemon-emitted inputs;
  prometheus evaluates (if Secrets landed); the Stack-B build of a node produces a
  closure identical to the Stack-A build.

### Stage 2 — The missing operational surface
- Write a Nix package (`flake.nix`/`default.nix`) for the daemon + thin client —
  **none exists**.
- Write a NixOS module / systemd unit running `lojix-daemon` (rkyv config), cluster-
  operator-owned, one instance per deploy host.
- Write the **request-builder/encoder** (the new `lojix-run`): resolves substituters
  (node-name → Yggdrasil URL+key) and writes a `DeployRequest` signal frame to disk
  for the thin client to send (the client refuses inline NOTA).
- **Exit:** an operator can drive a System Eval/Build of a real node through the
  daemon, end to end.

### Stage 3 — First cutover (secret-free, build-only, parallel)
- Stand up the Stack-B daemon **alongside** Stack A (both live).
- Swap CriomOS-home's home-profile package set toward the new client + request-
  builder (keeping lojix-cli installed during the parallel run).
- **First target: `zeus`** (Edge; no router, no LLM, empty swap) — confirmed to
  evaluate clean to a full drvPath with no secrets. Mode: System Eval/Build or Home
  Build (no activation needed).
- **Parity gate:** the Stack-B-built closure for zeus must be store-path-identical
  to the Stack-A-built closure.
- **Exit:** zeus builds via Stack B == Stack A, through the real daemon + client +
  request-builder.

### Stage 4 — Activation (lift the guard)
- Implement target-safe copy/activate: domain-resolved `root@<node>.<cluster>.criome`,
  real interpolated closure path, `--substitute-on-destination`,
  `switch-to-configuration`, EFI reconcile, the full BootOnce transient-unit
  rollback, the Home local fast-path; add cancel-kill on the activate ssh.
- Lift the reject-guard.
- **Exit:** a real activating deploy on zeus (Test → Boot → Switch) works against a
  real bootloader, and BootOnce rollback is verified (reboot-2 returns to OLD).

### Stage 5 — Durable state (the daemon's net-new charter)
- Land the redb/sema-engine backing + startup self-resume; make `Retire` actually
  reclaim (it currently only pops an in-memory Vec); wire keep-roots-gated GC (the
  `nix-store --gc` path is dead code today); write real gcroot symlinks.
- **Exit:** the daemon survives restart with its live-set/GC-roots/event-log intact.
- **Sequencing:** this blocks the *charter*, not minimal lojix-cli parity (lojix-cli
  is stateless). Per open decision 2, it may land before Stage 3 (durability-first)
  or after a small in-memory first cutover.

### Stage 6 — Widen and retire
- Add the swap fix → tiger/ouranos; add Secrets → prometheus (router WPA3 + LLM).
- Migrate the second consumer; switch one node at a time.
- When both consumers are covered and every node deploys via Stack B, retire
  lojix-cli (move it to "Retired" in `active-repositories.md`).

## Recommended first cutover

**`zeus`, System Eval/Build (or Home Build), Stack B running in parallel with Stack
A** — after Stage 0 (hygiene) + the Stage 1 firmware fix + Stage 2 (packaging +
request-builder). It needs **no** secrets, **no** activation, and **no** swap fix,
yet exercises the entire Stack-B path — daemon, two sockets, request-builder,
substituter resolution, input materialization, eval/build — against a real node,
with a hard parity check (closure must equal Stack A's). It is the smallest move
that proves the runtime in production without touching the deepest blockers
(activate, durable state, secrets).

## Open decisions — the psyche's to settle

1. **Parity-bar scope for the first cutover.** Is a secret-free, build-only cutover
   (zeus) an acceptable first step, or must full activate+secrets parity land
   before *any* node moves? (Report 26 open Q1; never enumerated.)
2. **In-memory vs durable-first.** May the first cutover run on in-memory state
   against a small node set (Stage 5 after Stage 3), or must persistence land first?
   (Report 26 open Q2 / record `v5d4`; explicitly undecided.) Governs the whole
   stage order.
3. **Where substituter resolution lives.** Either (a) the daemon gains horizon read
   for substituters (it already projects horizon for the overrides) and the wire
   reverts to node names, or (b) the request-builder hand-resolves before encoding.
   The wire currently bakes in (b).
4. **A fresh live Spirit Observe** to confirm no newer record green-lights cutover
   or redefines the bar — this plan's intent is grounded in INTENT.md + report-cited
   records, not a live dump (the deployed spirit-daemon schema was reported out of
   sync, so a live read couldn't be made).

## Two corrections this grounding makes to report 38

- The secrets gate fires via a **NixOS assertion** (`router/default.nix:89-97`),
  not only the let-binding throw at `:36` report 38 cited — the assertion is
  stricter and surfaces both the primary and backup Wi-Fi secrets. A parity test
  should assert against the assertion message.
- A **new, independent CriomOS bug** surfaced: `swapDevices.sizeMebibytes` (horizon)
  vs `.size` (nixpkgs) in `disks/preinstalled.nix:40` blocks eval of any node with a
  swap entry (tiger, ouranos) — unrelated to lojix, but it narrows the secret-free
  first wave to zeus until fixed.
