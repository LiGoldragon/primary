# 707-4 — Synthesis: findings, build plan, decisions

Three parallel design/audit agents (sub-reports 1-3), all non-destructive. The
results are unusually clean and B+C converged on a single design.

## Stream A — mentci integration (sub-report 1)

The reassuring part: the **mentci daemon triad is real** (mentci daemon + thin
CLI, signal-mentci with 6 requests + a `MentciEvent` stream, meta-signal-mentci),
and the **criome client-approval chain works end-to-end** over the meta socket by
slot — exactly the `t00s`/`p43g` model (criome parks; mentci lists+decides by
`AuthorizationRequestSlot`; the daemon folds parked criome requests into its
pending-question queue).

The keystone problem: **mentci-lib is orphaned and stale, contradicting `7x5z`.**
`7x5z` says mentci-lib is the shared state-machine library reused by the daemon
*and* clients. In reality the daemon uses its own `state.rs` on signal-mentci,
mentci-egui uses its own `daemon_client.rs` on signal-mentci, and **mentci-lib
depends on neither** — it carries a generic graph-signal skeleton, a non-existent
`DaemonRole::Criome/Nexus` handshake, and a *duplicate* hand-rolled copy of the
approval vocabulary. The shared leg is a divergent skeleton on a contract the
daemon abandoned. Everything else (a readable unified CLI/GUI surface) hangs off
fixing this.

Also: **mentci-egui is view-only** — one `ObserveInterfaceState` on a button
press, NOTA-rendered, no live subscription, meta mode is a placeholder, it renders
only the Mentci socket, and it *cannot answer a question*. The `gc0n`
EscalateToPsyche approval UI does not exist yet. And the **VM-test foundation
already exists**: `criome-nixos-module-142` carries `criome.nix` (systemd module,
NOTA→rkyv ExecStartPre, one-arg daemon) + `criome-node.nix` (a `runNixOSTest`) —
the template to extend into a multi-daemon guest driven through mentci on Prometheus.

The plan (design-validated): re-found mentci-lib on the live contracts as the one
shared observability+control model (one `ObservationModel` keyed by component
socket, one NOTA renderer, the closed-decision→criome mapping); a CLI read+answer
atom roster that prints the same renderer (so CLI output is grep-assertable in a
testScript and reads identically to the GUI); mentci-egui gains the live
subscription + per-component panes + the **approval card** (which *is* the inert
`gc0n` psyche-escalation surface made real); two daemon enablers (bind the meta
socket; continuous criome park subscription); collapse the now-unblocked
signal-standard cross-imports; and a criome+mentci `runNixOSTest` on Prometheus.

## Stream B — worktree audit (sub-report 2)

44 worktrees / 23 repos: ~9 **merged** (safe to dismantle), ~16 **archive**
(pushed/captured, unmerged or superseded), 2 **recycle**, ~16 **keep-active**
(the live criome E1 trees, the cloud-designer cloud-node wave, system-designer's
prometheus work), plus 2 empty leftover parent dirs (`nota-next/`, `upgrade/`).

**4 worktrees hold unique UNPUSHED work — must not be lost:**
- `schema-rust-next/reaction-expand` (`8b147fac`, `a1582dfd`) — **no bookmark, not
  on any remote, no owning lane** → most at risk.
- `schema-rust-next/structural-forms-integration` (`a0138ce1`) — bookmark diverged
  (ahead 5 / behind 5), so the work isn't tracked by it.
- `CriomOS/prometheus-vm-host` (`92b5d6f6`), `goldragon/prometheus-vm-host`
  (`b9d1ddca`) — system-designer's, unpushed (overlap the pushed
  `enable-vm-hosting-prometheus` superset).

The durable record (this report, committed) protects them: the GC contract refuses
any row with `pushed=Unpushed`. No tree is touched in this wave.

## Stream C — worktree registry (sub-report 3)

The decisive finding: **`tools/orchestrate` is already the typed
`persona-orchestrate` component** (the shim execs `orchestrate-cli`, a compat
surface over a long-lived daemon with a redb/sema-engine store + `*.lock`/
`roles.list` *projections*). So the `w190`/`tz5j` "migration" concern is moot —
the registry should be **daemon-owned typed state from day one**, with the CLI as
its argv front door. `StoredRepository` (a `repositories` table scanning `/git`,
projected over the meta socket) is the exact precedent; `verify_jj.rs` already
computes pushed/ancestor-of-main/age, so the audit signals come free.

**B+C convergence: the GC manifest IS the registry projection** —
`orchestrate/worktrees.nota` (the daemon's typed-NOTA projection of a `worktrees`
table), beside the `.lock` projections. One artifact, not two. Stream B's audit
becomes the first bulk population (register/update/archive/recycle calls), and a
`~/wt` scan keeps it live. Build: `Worktree`/`WorktreeStatus`/`PushedState` types
in signal-orchestrate (`Observe(Worktrees)`) + meta-signal-orchestrate
(Register/Update/Refresh orders), a `worktrees` redb table (schema-version bump), a
`WorktreeRegistry` scanner, and the `orchestrate worktree …` verb group (list→
ordinary socket, mutations→meta). Register-at-creation goes into
`skills/feature-development.md` / `skills/jj.md` / `orchestrate/AGENTS.md`.

## Build plan (the wave 2, sequenced)

1. **Worktree registry** (orchestrate triad + CLI) — unblocked, non-destructive;
   prototype on branches (signal-orchestrate / meta-signal-orchestrate / orchestrate)
   + the orchestrate-cli verbs; seed from B's audit; generate `worktrees.nota`.
2. **mentci re-founding** — re-found mentci-lib on the live contracts, then the CLI
   read+answer roster, then the criome+mentci `runNixOSTest` on Prometheus
   (recycle `criome-nixos-module-142`; fresh worktrees for mentci/mentci-egui/
   mentci-lib — none exist today, that work bypassed the worktree protocol).
3. **mentci-egui** — live subscription + per-component panes + the approval card.
4. **GC pass** (destructive, gated) — only after the must-not-lose work is
   pushed/captured; re-verify live per the GC contract; dismantle merged/archived
   trees + remove the empty parent dirs.

## Decisions needed

1. **mentci-lib direction** — re-found it on the live signal-mentci/criome
   contracts (recommended; the daemon+egui already use those, mentci-lib is the
   outlier per `7x5z`), or have the daemon/egui adopt the existing mentci-lib
   graph-signal model? One of the three must move.
2. **Registry build** — proceed with the daemon-owned typed registry across the
   orchestrate triad (recommended; matches the actual architecture + `eh5a`), now
   and in parallel with the mentci work?
3. **Must-not-lose** — the 2 unowned `schema-rust-next` unpushed trees: push them
   to preserve now, or record-protected + route to their owner (recommended; not
   designer's work to rewrite, and the diverged bookmark is delicate)?
