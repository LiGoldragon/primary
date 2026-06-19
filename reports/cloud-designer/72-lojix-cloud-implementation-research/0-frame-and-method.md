# 0 · Frame and method — lojix↔cloud implementation research + hanging-bug sweep

cloud-designer, 2026-06-19. Session orchestrator frame.

## The psyche's order

> "research how to implement this properly. fix all the hanging bugs and
> missed polish and get everything lined up first. make sure you read skills
> and spirit before taking action"

"this" = the lojix↔cloud deployment integration designed in report 71 §4
(pre-baked CriomOS `CloudNode` snapshot → activate; two daemons that never
call each other, joined by domain/IP + closure; create→observe→DNS→deploy
handoff). The order has three movements:

1. **Research how to implement it properly** — turn the report-71 design
   (correct at altitude) into an implementation-ready spec grounded in the
   *current* source of lojix, cloud, and CriomOS. Report 71 already has one
   known staleness: it shows `nix copy --to ssh-ng://` for the deploy leg,
   but lojix moved to **build-on-target** (`nix build --eval-store auto
   --store ssh-ng://root@<node>.<cluster>.criome <attr>^*`, system-designer
   report 150, 2026-06-19). Every NOTA leg and node precondition must be
   re-grounded.
2. **Fix all the hanging bugs and missed polish** — sweep the open findings
   from cloud-designer reports 68/69/70/71, verify each against current
   source, fix the designer-lane ones on the `cloud-designer-intent-refresh`
   branch, file precise operator/system-operator beads for the rest.
3. **Get everything lined up first** — consolidate before the implementation
   push: branch coherent, reports current, ARCHITECTURE.md reconciled, the
   spec implementation-ready.

## Spirit gate

The prompt is a **task-only order** — it carries no durable arrow that
survives the task's completion. Gate outcome: **no capture, Observe/refresh**.
The live Spirit store is unreachable (see Blocker), so grounding comes from
the *manifested* intent already in `cloud/INTENT.md` and `lojix/INTENT.md`
(both read this session) carrying the load-bearing records: `hcp8` (DO lead),
`iprx` (system-creds eventual), `ad53` (CloudNode image home), `cjrl`
(sops-at-activation), `h03z` (criome-custodied deploy identity), `6ks1`
(billing-hour reuse pool).

## BLOCKER surfaced this session — Spirit daemon down workspace-wide

`spirit-daemon.service` is `failed (start-limit-hit)` after the Jun 19
22:47 reboot. Root cause: `ExecStartPre=spirit-startup-state` runs
`spirit-migrate-store`, which aborts with **`unrecognized spirit store
schema version: 10`** — the active spirit generation's store-migrator tops
out below the on-disk SEMA store schema version 10 (the store was advanced
by a newer generation than the one systemd loaded after reboot). Six rapid
restarts tripped `StartLimitBurst=5`, so the socket
(`~/.local/state/spirit/spirit.sock`) never appears and every `spirit`
call gets `transport IO error: No such file or directory`. This is a
**deployed-service fault (system-maintainer's lane)** that touches intent-
data integrity — NOT fixed in this session; surfaced to the psyche with a
recommended recovery (roll the active home-manager generation forward to
the v10-capable spirit, or restore from a pre-v10 backup in
`~/.local/state/spirit/`). Intent capture and Observe are down for every
psyche-facing agent until it is fixed.

## Two hanging bugs already verified by hand (workflow seeds)

- **Cloudflare daemon credential never injected.** `cloudflare.rs:53`
  resolves the token by `std::env::var(handle)` where the daemon handle is
  `CLOUDFLARE_DNS_TOKEN`; the flake `cloud-daemon` postInstall wrapper
  (`flake.nix:96-99`) injects only `HCLOUD_TOKEN` and
  `DIGITALOCEAN_ACCESS_TOKEN`. `CF_API_TOKEN` (`cloudflare_cli.rs:18`) is a
  *separate* var set only inside the `flarectl` subprocess wrapper. So if
  the daemon's `EnvironmentCredentialSource` path is load-bearing, the
  Cloudflare capability has no token. Severity/lane pending lane-B
  verification (is the daemon env path used in production, or is flarectl's
  own CF_API_TOKEN the only live path?).
- **cloud `ARCHITECTURE.md` reconciliation open.** The
  `cloud-designer-intent-refresh` branch touches only
  INTENT.md/README.md/flake.nix; `ARCHITECTURE.md` still carries the
  5-actor/no-block prescription that report 68 found contradicted by the
  shipped single-EngineActor synchronous-Store reality, and the dead
  sema-engine pilot is unreconciled.

## Method — research + adversarial-audit workflow, designer applies fixes

Ultracode is on. A parallel workflow does the read-heavy research and the
bug sweep; the orchestrator (designer) applies the designer-lane fixes on
the branch and files beads. Phases:

- **Research (4 lanes, parallel, each writes its numbered report):**
  1. lojix deploy contract — the exact `meta-lojix Deploy` the handoff tool
     issues, build-on-target mechanics, node preconditions, activation
     confirmation. (signal-designer 150, operator 436, lojix source.)
  2. cloud socket contract — the exact NOTA for every handoff leg, the
     create→observe seam, image_name plumbing, and the Cloudflare
     credential-path truth.
  3. CriomOS CloudNode build — the concrete species + provider-snapshot
     build path mirroring TestVm; DO upload vs Hetzner bootstrap mint.
  4. hanging-bug ledger — every open item from 68/69/70/71 + the two
     verified seeds, deduplicated, each with location/severity/current-
     state/fix-shape/lane.
- **Verify:** adversarial refutation of each bug-ledger finding (is it
  really still open?) + completeness critic over the three research lanes
  (what NOTA leg / precondition is unspecified or unverified?).
- **Synthesize:** the implementation-ready handoff-tool + CloudNode spec,
  and the consolidated fix ledger split into designer-now / operator-bead /
  sysop-bead.

Then the designer applies designer-now fixes on
`cloud-designer-intent-refresh`, updates report 71's stale deploy leg, and
folds the bead ledger into `primary-x8by`.
