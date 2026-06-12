---
role: cloud-designer
session: 41-lojix-production-refresh
report: 8-spirit-topic-sweep
topic: Durable psyche intent bearing on finalizing lojix for production
date: 2026-06-12
method: spirit Observe + LookupStash + direct Lookup against deployed spirit 0.9.5
---

# Spirit topic sweep — lojix production finalization

## Method and provenance

All records pulled from the deployed `spirit` binary
(`~/.nix-profile/bin/spirit`, `(VersionReported (0.9.5 ...))`). Grammar
confirmed against `/home/li/primary/skills/spirit-cli.md` (the eight-field
`Query`; `Observe` stashes non-empty results and returns
`(RecordsStashed (<handle> <count> <marker>))`; retrieve with
`(LookupStash <handle>)`).

Per-term `Observe (Any Any (ContainsText <term>) Any None (Exact Zero)
(AtLeastCertainty Minimum) Any)` counts (handle, count):

| term | handle | count | term | handle | count |
|---|---|---|---|---|---|
| lojix | 1 | 18 | meta | 9 | 47 |
| daemon | 2 | 117 | parity | 10 | 2 |
| production | 3 | 49 | BootOnce | 11 | 1 |
| cutover | 4 | 11 | SSH | 12 | 6 |
| deploy | 5 | 44 | secrets | 13 | 3 |
| schema | 6 | 445 | horizon | 14 | 16 |
| CLI | 7 | 71 | sema-engine | 15 | 7 |
| socket | 8 | 28 | durable | 16 | 40 |
| substituter | 17 | 1 | | | |

Direct prior-session lookups: `0xqp`, `oh9l`, `lc28`, `o5rz`, `7m2d` all
resolved with `(RecordFound ...)`; `gdgv` returned `(Error [record not
found])`.

Each record below is `id` + Kind + gloss; certainty/importance noted when
load-bearing. Identifiers are the short codes the daemon returned.

## Theme: lojix charter, parity, cutover

- `tvbn` Decision (High cert, **VeryHigh imp**) — the Horizon+lojix
  rewrite charter. Horizon is an accepted hack-for-now projection surface,
  NOT a full triad component. lojix is the traditional component getting
  the full triad-engine + schema-based port and the runtime triad. Goal:
  finish the lean rewrite to cutover and **retire the dual deploy stacks**
  (end the Stack A production + Stack B next parallel-maintenance burden);
  reach parity then switch over per-node; port high-confidence production
  CriomOS changes into the next stack along the way.
- `v5d4` Constraint (Medium) — passing sandbox testing is a **precondition
  for the lean-stack cutover to main deployment**.
- `nhwv` Clarification (High) — the raw/pretty Horizon split applies ONLY
  to the new lojix+horizon-next stack; production Stack A Horizon stays
  as-is until retired at cutover.
- `bb83` Clarification (Medium) — cross-daemon cutover can be atomic by
  protocol.
- `7m2d` Correction (High) — lojix deployment is NOT the problem to avoid;
  the safety issue is local resource pressure during build/eval, so
  operator work should keep using lojix while making the workload safe.
- `57hq` Decision (High) — `cluster-operator` is a specialized lane for
  live system maintenance and production lojix operations.

## Theme: CLI / socket / client model

- `8bwo` Decision (**VeryHigh cert, High imp**) — every component exposes
  its two contracts as **two thin CLI clients**: the working client named
  after the component, the meta client prefixed `meta-`. One extracted
  pattern across all components. `spirit` and `meta-spirit` are the first
  instance. (lojix gets `lojix` + `meta-lojix`.)
- `7sx6` Correction (**Maximum cert, VeryHigh imp**) — every component has
  **exactly two contracts and no more**: `signal-<component>` (ordinary
  working) and `meta-signal-<component>` (meta policy). No third contract,
  no owner-signal split, no engine-management split.
- `vudl` Decision (High) — **lojix two-contract authority split**: Deploy,
  Pin, Unpin, Retire are owner-only policy → `meta-signal-lojix`; Query,
  the WatchDeployments/WatchCacheRetention subscriptions, and Unwatch are
  peer-callable → `signal-lojix`. A deploy mutates the live cluster and can
  break the router, so it is the strongest case for the owner socket.
  Until cutover carry `meta-signal-lojix` as a **local path-dependency
  package inside the lojix tree** (mirroring the cloud stopgap); create the
  standalone repo at cutover.
- `9v7h` Decision (High) — owner/meta socket uses `triad-runtime`
  `ConnectionContext` SO_PEERCRED, **rejecting on uid mismatch and failing
  closed** for Deploy/Pin/Unpin/Retire; defense-in-depth on top of the
  socket file-mode guard.
- `3chp` Decision (High) — the policy/control socket is the **meta socket**
  (not owner socket).
- `hnpo`/`0fs6`/`rtrf` Corrections (VeryHigh) — `MetaSignal` is canonical;
  `OwnerSignal` deprecated. From-scratch policy contracts are born
  `meta-signal-*`.
- `lw73`/`q33b` (Medium/High) — keep separate ordinary + owner sockets for
  now, permissions enforced by filesystem socket access in local trusted
  dev; permission-in-signal-variant deferred until needed.
- `l96d` Decision / `s5dz` Decision (Medium) — parallel daemon versions
  need **versioned sockets** and version-suffixed CLI binaries; a shim
  resolves bare names to the current default version.
- CLI-is-thin-client principles (from CLI stash): "CLIs are thin Signal
  clients"; the daemon binary compiles with **no NOTA at all** (NOTA is a
  thin-CLI text-edge concern, gated behind a `nota-text` cargo feature);
  "There should be no NOTA between components." `kg2z` Correction (High):
  Spirit CLI uses **inline NOTA strings by default**, temp-file paths only
  for binary signal-encoded files or shell-metacharacter-heavy NOTA.
- `dn3c` Constraint (High) — public-traffic routing during cutover must be
  **lossless AND client-transparent** (one stable socket, no client
  discovery); rules out CLI-discovery designs.
- `n2te` Correction / `ns7t` Decision (Medium) — client-side discovery
  (Design C) rejected; first lossless-cutover prototype is
  Persona-orchestrated FD handoff via SCM_RIGHTS (Design D), same socket
  model dev and prod, Persona off the byte path after handoff. `iq11`:
  drain-with-mirror accepted as the no-downtime upgrade protocol
  (acked == durable, atomic socket handoff).

## Theme: daemon config / bootstrap / schema syntax

- `ur16` Decision (**VeryHigh cert, Maximum imp**) — daemon bootstrap
  model. Single startup argument is a **pre-generated signal-encoded (rkyv)
  Configure message — NOT NOTA**. Bootstrap depends on no manager. Daemon
  opens the store in the Configure: virgin/empty → apply as first config;
  populated → **self-resume** from persisted store. Same Configure type
  accepted live over the meta socket; bootstrap-config and runtime-config
  are one vocabulary.
- `t803` Clarification (High) — the baseline meta operation of every
  `meta-signal-*` contract is `Configure`; component-specific privileged
  actions build on top.
- `q3q7`/`cgd8` (Medium) — the daemon configuration *type* lives in the
  ordinary `signal-<component>` contract (imported for binary startup
  decode); the meta `Configure` op wraps that same type; configuration
  verbs live in the meta contract. Don't duplicate the config struct in the
  daemon.
- `l6zw` Correction (High) — a contract carries ONLY wire messaging
  vocabulary (Signal Input/Output roots, record types, codec). Nexus and
  SEMA are daemon-internal and must NOT appear in any contract schema.
- `vfjw` Clarification (**VeryHigh cert, High imp**) — NOTA strings come
  EXCLUSIVELY from bracket forms (`[text]`, `[|text|]`); quotation marks do
  NOT form strings. **Legacy lojix-cli double-quote acceptance is
  non-canonical and slated for removal.** (Directly names lojix-cli.)
- `3naf` Correction (High) — NOTA encoders should not over-bracket
  bare-safe atoms; bare atoms valid inside typed positions/vectors.
- `tj99` Decision (Medium) — evolve the `schema-rust-next` daemon emitter
  (+`triad-runtime`) to host lojix's load-bearing daemon properties so
  concurrent daemons adopt the GENERATED daemon: BoundedWorkers, fresh
  per-request engine over a shared store, two-wire-contract single-Nexus
  working tier with the meta tier as a typed engine path, per-request
  frame-size/read-timeout hardening. **lojix hand-written daemon is the
  reference implementation feeding back into the emitter.**
- `2tfa`/`brgo` Decisions (Medium) — `signal-lojix` carries
  WatchDeployments + WatchCacheRetention streaming subscriptions from day
  one; lojix is the first component to prove schema-derived
  streaming-subscription emission; if the generator can't emit streams yet
  that work lands on the lojix port path. Full schema-derived streaming is
  the chosen direction (teach schema-next + schema-rust-next + add push to
  triad-runtime); handshake+poll suffices until then and **does not block
  cutover**.

## Theme: durable state / sema-engine

- `oh9l` Decision (High) — **durable-first**: for the lojix cutover build
  the durable DB backing now as baseline (daemon live-generation-set,
  GC-roots, event-log state persisted on sema-engine with self-resume on
  restart) rather than a first cutover on in-memory state. Psyche judges
  the durable DB small and straightforward.
- `up9q` Decision (High) — a lojix deploy/build **survives client
  disconnect**: owned by a job actor that owns the external process and
  persists job state, reporting status later. Cancellation declared
  per-operation in schema; durable deploys survive disconnect by default;
  speculative queries/builds may opt into kill-on-drop; **no blanket
  kill-on-drop on effect processes**.
- `2alg` Decision (High) — the lojix deploy daemon **MUST serve multiple
  connections concurrently and must not block** during a deploy nix build.
  In-flight deploy state is PER-REQUEST (per connection), not a shared
  slot; the durable Store is the only shared concurrency point, locked
  briefly per sema op; long nix effects hold no global lock; bounded by a
  connection permit cap. (`k6w1` Principle: this bounded thread-per-conn
  worker primitive belongs in shared `triad-runtime`, reused per daemon.)
- `fosp` Correction (**VeryHigh**) — sema-engine is the **exclusive**
  database interface; no daemon may make direct redb calls. A daemon
  opening redb directly is wrong even as a pilot.
- `e440` Decision (High) — SEMA engine is a single-writer actor; reads run
  in parallel (redb MVCC); single-writer invariant is writes-only.
- `3d5z` Constraint (**VeryHigh cert, VeryHigh imp**) — strict triad engine
  separation: SEMA owns all durable-state code, Nexus all decision-making,
  Signal all communication; the daemon contains no DB/decision/comms code
  outside its engine.
- `29pb` Constraint (High) — component Sema databases must be backed up to
  a server atomically; state loss unacceptable; pursue native
  version-controlled component DBs.

## Theme: deploy mechanics, substituters, secrets, safety

- `lc28` Decision (**Low cert** — provisional) — substituter resolution
  (node-name → Yggdrasil cache URL + public key) **moves into the daemon**:
  daemon gains horizon-read for substituters; wire reverts to carrying bare
  node names. Explicitly "for-now, must be replaced by better design."
- `2qhw` Decision (Medium) — lojix-daemon takes scope expansion for
  **GitHub-authenticated Nix flake input resolution**: a small Rust library
  lojix-daemon calls, fetching the GitHub API key from gopass and injecting
  it (likely NIX_CONFIG access-tokens); resolves the rate-limit
  stale-activation incident as a deploy-path problem owned by lojix.
- `6x2k` Principle (**VeryHigh cert, High imp**) — use the github remote
  url form for flake/repo references; commit and push first, then build
  from the remote. **Never build or deploy from a local path checkout** —
  non-reproducible bad form. Local path/override-input only for throwaway
  iteration.
- `88eq` Decision (High imp) — component upgrade protocol via Nix-flake
  versions: each flake captures running-production (pinned), local-dev, and
  named variants as inputs; tests run through Nix (commit-first).
- `vcin` Constraint (High imp) — positive grep checks are NOT proof of live
  architecture; a deploy check must compile/execute/round-trip; grep only
  as a narrow negative guard.
- `my4g` Decision (High) — Persona uses systemd template units for
  component daemon management in prod from day one (UnitController trait;
  systemd-D-Bus backend prod, direct-fork backend tests/sandbox).
- `xv9v` Constraint (High) — **BootOnce**: Prometheus/router deploys use
  the safe BootOnce path rather than Switch until console/out-of-band
  access and sign-off are in place.
- `kx32` Constraint (High) — deploying to the router node (prometheus,
  running hostapd/dnsmasq) must not knock out its network; prefer
  boot-mode activation over live switch; prefer out-of-band/console.
- `1lex`/`gnfx` Constraints (High/Medium) — disruptive live switch and
  large prefetch operations run as **durable systemd transient units** so
  they survive SSH/Wi-Fi drop.
- `nfic` Clarification (Medium) — maintainer has root SSH on cluster hosts
  but cannot SSH as Bird on Zeus; Zeus Bird home-profile redeploy uses a
  root/maintainer path.
- `7gq6` Constraint (**Maximum**) / `cjrl` Principle (VeryHigh) — secrets:
  an agent must never see a secret value (no echo/print/log/argv); pipe
  source to sink, verify by length+exit code. Secrets land in the most
  secure store (gopass user-session, SOPS-nix cluster); move ciphertext to
  ciphertext.

## Theme: branch / main policy for the rewrite repos

- `o5rz` Clarification (High) — the new-stack rewrite repos (lojix,
  signal-lojix, meta-signal-lojix triad-port and peers), which are NOT the
  production deploy logic (production is **lojix-cli and the current
  stack**), are pushed **directly to main, no next/feature-branch
  ceremony**. The designer-next/operator-main split (intents 515, 2561)
  governs only PRODUCTION code repos. Untracked working trees with no
  git/jj are unacceptable; rewrite work must live in version control and be
  pushed.
- `nzf3` Decision (Medium) — operator may work directly on main of new
  concept-prototype repos without the designer-feature-branch /
  operator-rebase ceremony; exception applies only to fresh repos with no
  production history.
- `vqtd` Principle (High) — major architectural breaks get a new
  `-next`/`-v2` repo rather than a branch; rename to the canonical short
  name after the break stabilizes.

## Theme: standing process intent

- `0xqp` Principle (High) — running a Spirit Observe is standard routine
  practice; observe recent records proactively to let recorded intent guide
  the work, not only when intent is unclear.
- `9huv` Principle (High) — agents must track the **deployed** version's
  interface, not current source; find the pinned commit via the CriomOS
  Home flake input and Nix metadata.

## Open questions / unsettled (low/medium certainty, explicitly flagged)

- `lc28` substituter-in-daemon is **Low certainty, explicitly "must be
  replaced by better design"** — provisional, not the final shape.
- `brgo` carries an open question: whether the existing signal-frame
  streaming substrate was deliberate scaffolding or leftover (changes the
  streaming effort estimate). Real push not yet landed; poll bridges until
  then.
- `2qhw` GitHub-auth library form is Medium certainty (a small Rust lib
  lojix-daemon calls).
- `s5dz` versioned-socket / version-suffix shim mechanism is Medium
  ("see-if-it-makes-sense"), exact shim TBD (system-specialist territory).
- `gdgv` (cited in the prior session) does **not resolve** — `(Error
  [record not found])`; either removed or mis-cited.
