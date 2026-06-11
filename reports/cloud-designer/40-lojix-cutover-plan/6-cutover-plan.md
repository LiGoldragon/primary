# 6 — the staged production cutover plan

cloud-designer, 2026-06-11. Synthesis of the five grounded runs in this directory
(workflow `lojix-cutover-plan`) plus reports 38 (readiness) and 39 (the Stack-A
baseline). The highest-numbered file IS the synthesis. Every claim below is
grounded in a real build/eval this session unless marked otherwise.

> **Update (2026-06-11):** the redundant `triad-port/` subdir was flattened to the
> repo root across all three triad repos (Spirit `gdgv`; lojix `13192bce`,
> signal-lojix `b31cd980`, meta-signal-lojix `317b7fab`). Read every
> `triad-port/src/…` / `triad-port/…` path below as the repo-root path (`src/…`).

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
only for the binary** (no eval-time coupling), and **zeus is the simplest node to
validate the runtime on first** (it evaluates today — no router/LLM/swap). So the
runtime can be proven on a real node early, but the recorded charter is
**port-first** (`fe2j`): complete the port onto the designed components, reaching
parity, before cutting any node over (see §Spirit grounding).

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
6. **Substituter resolution in the daemon** (decided `lc28`, provisional). The
   daemon gains horizon-read for substituters; the wire reverts to bare node names
   (drop the pre-resolved `{url, public_key}` from signal/meta-signal-lojix). The
   resolving code is marked *must be replaced by better design* — a for-now shape.
7. **Sandbox testing passes** (`v5d4`) — a recorded precondition for the lean-stack
   cutover to main deployment.

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
first real cutover; stages 4–6 widen it. **Per decision `oh9l` (durable-first), the
durable-state work (Stage 5) is sequenced ahead of the first cutover** — pre-cutover
baseline, built on sema-engine (`munq`/`tj99`).

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
- **(Required — production uses secrets.)** Add a `Secrets` MaterializationShape
  mirroring lojix-cli's `artifact.rs` (existence-gated on
  `<proposal>/secrets/router-wifi-sae-passwords.sops`, the 3 fixed filenames) and
  inject `--override-input secrets`. Baseline work, not a deferral — prometheus is a
  production node that cannot evaluate without it, so lojix-cli cannot retire until
  it lands.
- (CriomOS-side, optional, widens the first wave) Fix the `swapDevices.sizeMebibytes`
  → `.size` mismatch in `disks/preinstalled.nix:40` that blocks tiger/ouranos eval
  (a Stack-A bug, independent of lojix).
- **Exit:** `CriomOS/checks/metal-firmware-policy` passes for daemon-emitted inputs;
  prometheus evaluates once Secrets lands; the Stack-B build of a node produces a
  closure identical to the Stack-A build.

### Stage 2 — The missing operational surface
- Write a Nix package (`flake.nix`/`default.nix`) for the daemon + thin client —
  **none exists**.
- Write a NixOS module / systemd unit running `lojix-daemon` (rkyv config), cluster-
  operator-owned, one instance per deploy host.
- Write the **request-builder/encoder** (the new `lojix-run`): writes a
  `DeployRequest` signal frame to disk for the thin client to send (the client refuses
  inline NOTA). Per `lc28` it does **not** resolve substituters — it names nodes.
- **Substituter resolution moves into the daemon** (`lc28`, provisional): the daemon
  gains horizon-read, the wire reverts to bare node names, and the resolving code is
  tagged *must be replaced by better design*. Needs a `signal-lojix`/`meta-signal-lojix`
  contract change (drop the pre-resolved `{url, public_key}`).
- **Exit:** an operator can drive a System Eval/Build of a real node through the
  daemon, end to end.

### Stage 3 — First cutover (simplest node, build parity, parallel)
- Stand up the Stack-B daemon **alongside** Stack A (both live).
- Swap CriomOS-home's home-profile package set toward the new client + request-
  builder (keeping lojix-cli installed during the parallel run).
- **First target: `zeus`** (Edge; no router, no LLM, empty swap) — chosen because it
  is the *simplest* node (evaluates clean today), **not** to dodge secrets (Secrets
  ships in Stage 1 regardless). Mode: System Eval/Build or Home Build.
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

### Stage 5 — Durable state — DECIDED: build before Stage 3 (`oh9l`)
- Land the **sema-engine** backing + startup self-resume; make `Retire` actually
  reclaim (it currently only pops an in-memory Vec); wire keep-roots-gated GC (the
  `nix-store --gc` path is dead code today); write real gcroot symlinks.
- **Exit:** the daemon survives restart with its live-set/GC-roots/event-log intact.
- **Sequencing:** decided **durable-first** (`oh9l`) — lands before the first cutover
  (Stage 3) as pre-cutover baseline, not an after-the-fact follow-on; the psyche judges
  it small. Per `munq`/`tj99`, build it in the shared/generated layer (sema-engine + the
  schema-rust-next emitter), not a lojix fork. (Listed last only to keep the
  stage-numbering stable; it is sequenced early.)

### Stage 6 — Widen and retire
- Add the swap fix → tiger/ouranos; add Secrets → prometheus (router WPA3 + LLM).
- Migrate the second consumer; switch one node at a time.
- When both consumers are covered and every node deploys via Stack B, retire
  lojix-cli (move it to "Retired" in `active-repositories.md`).

## Recommended first cutover

**`zeus`, System Eval/Build (or Home Build), Stack B running in parallel with Stack
A** — after Stage 0 (hygiene) + the Stage 1 build-parity fixes + Stage 2 (packaging +
request-builder). zeus is chosen as the *simplest* node (no router/LLM/swap), and it
exercises the entire Stack-B path — daemon, two sockets, request-builder, substituter
resolution, input materialization, eval/build — against a real node, with a hard
parity check (closure must equal Stack A's). Per the charter (`fe2j` port-first,
`v5d4` sandbox-test gate), treat this as the **pre-cutover validation** that the
ported daemon reaches build parity; the *real* cutover follows once activation and
(per decision 1) durable state are in. Secrets is **not** skipped — it ships in
Stage 1; zeus simply doesn't reference it.

## Spirit grounding (live Observe, 2026-06-11)

A live Spirit Observe (`spirit Version` → v0.8.1; daemon up) grounds this plan's
intent — and corrects one mis-citation. The load-bearing records:

- **`tvbn`** (Decision, VeryHigh) — the rewrite charter: *reach parity then switch
  over per node; port high-confidence production CriomOS changes into the next stack
  immediately where the correct change is clear, then test those builds.*
- **`fe2j`** (Decision, High) — **port-first**: *complete the lojix triad-engine /
  schema-component port BEFORE cutting CriomOS over; Stack A is never retired onto a
  non-triad deployer.*
- **`v5d4`** (Constraint, High) — *passing sandbox testing is a precondition for the
  lean-stack cutover.* (A sandbox-test gate — **not** the in-memory-vs-durable record
  I earlier mis-cited.)
- **`up9q`** (Decision, High) — *a durable deploy is owned by a job actor that
  persists job state and survives client disconnect; cancellation is per-operation in
  schema; **no blanket kill-on-drop** on effect processes.* → deploy-job-state
  persistence is intended, and the activate-ssh control must be **per-operation
  cancellation, not a blanket kill** (refines watch-for #8).
- **`783n`** (Correction) — *lojix must permit local builds; prometheus must build its
  own model-heavy closures locally* (it owns the AI model/closure cache).
- **`2tfa`/`brgo`** (Decisions) — the Watch subscriptions are *from day one, not
  deferred*, via **schema-derived** streaming (teach schema-next / schema-rust-next to
  emit the event frame), *not a lojix hand-wired carve-out*.
- **`munq`/`tj99`** (Constraint/Decision) — *use the designed components fully; when
  one is too incomplete, develop it further rather than bypass*, and host daemon
  properties (concurrency, and by extension durable state / streaming) in the
  **generated** emitter, not hand-written per-component forks.

Net: the plan already aligns with the charter (port-first, parity-then-per-node,
designed-components-fully). Two consequences fold in — the durable-state and
subscription work belongs in the **generated/shared layer** (sema-engine,
triad-runtime, schema-rust-next), not hand-rolled in lojix; and **sandbox-test-passing
(`v5d4`)** joins the must-meet constraints.

## Decisions — all resolved (psyche, 2026-06-11)

- **Secrets is in the parity bar** (production uses it) → mandatory Stage-1 work, not
  an optional deferral. (The earlier "secret-free cutover acceptable?" framing was
  wrong.)
- **A Spirit Observe is standard routine practice**, not a decision to offer —
  principle `0xqp`.
- **Durable-first** (`oh9l`). Build the durable database now, before the real cutover:
  live-generation-set / GC-roots / event-log persisted on **sema-engine** with
  self-resume — not a first cutover on in-memory state. The psyche judges it small
  ("not a big deal"). Stage 5's work is sequenced ahead of Stage 3; the in-memory
  validation idea is dropped.
- **Substituter resolution in the daemon, provisionally** (`lc28`). Option (a): the
  daemon gains horizon-read and the wire reverts to bare node names (drop the
  pre-resolved `{url, public_key}`). A *for-now* choice — the implementing code is
  tagged **"must be replaced by better design."**

No open decisions remain. The next move is execution — Stage 0 hygiene, the durable
sema-engine backing (`oh9l`), and the operational surface (packaging + request-builder)
— per whichever the psyche points at first.

## Two corrections this grounding makes to report 38

- The secrets gate fires via a **NixOS assertion** (`router/default.nix:89-97`),
  not only the let-binding throw at `:36` report 38 cited — the assertion is
  stricter and surfaces both the primary and backup Wi-Fi secrets. A parity test
  should assert against the assertion message.
- A **new, independent CriomOS bug** surfaced: `swapDevices.sizeMebibytes` (horizon)
  vs `.size` (nixpkgs) in `disks/preinstalled.nix:40` blocks eval of any node with a
  swap entry (tiger, ouranos) — unrelated to lojix, but it narrows the secret-free
  first wave to zeus until fixed.
