# 58 · Cloud Hetzner — what's unimplemented, and the land-on-main workflow (2026-06-18)

Psyche: *"look at everything that hasn't been implemented and then create a
workflow to actually implement it and land it e2e tested on main branches."*
Landing on main is psyche-directed here, overriding the usual
designer-branch/operator-integrates split (Spirit `150a`, `6ks1`).

## 1 · Survey — everything not yet on main

| Item | State | Gating |
|---|---|---|
| Phase 1 provider (create/observe/destroy) | built + green on `hetzner-compute` branches, **not on main** | — landable now |
| Destroy via the wire | apply path handles `Destroy`, but `PrepareHostPlan` only builds `Create` — unreachable | — landable now (additive op) |
| cloud `INTENT.md` compute capability | not manifested | — landable now |
| Deferred-effect / actor seam | designed (spec §6), not built | needs a spec+build pass |
| Billing-hour reuse pool + reaper (`6ks1`) | principle captured, not built | needs the deferred seam + a spec pass |
| Install hop (nixos-anywhere) | not built | **fork:** install-hop owner |
| horizon cloud-node model + provisioning ledger | not built | **fork:** chicken-and-egg / spec-identity split |
| Default architecture | undecided | **fork:** ARM vs x86 |
| Real "create a VM" e2e | not run | **live:** Hetzner account + token |

## 2 · What THIS workflow lands on main, e2e tested

The implementable-and-not-blocked set — integrated to all three mains with
the hermetic e2e green:

1. **Phase 1 integration** — `signal-cloud` + `meta-signal-cloud` + `cloud`
   `hetzner-compute` → their mains. The `[patch]`/`links` collision dissolves
   once both contracts are on main (both consumers point at signal-cloud@main).
2. **Destroy via the wire** — an additive `PrepareHostDestruction` meta op
   (`HostDestruction { provider, host_name }`) that builds a `Destroy` host
   plan, so the full create→approve→apply→destroy lifecycle is expressible and
   owner-approved. No `HostPlan` refactor (the create-only fields stay empty on
   a destroy plan, which apply ignores — a clean action-enum refactor is a noted
   follow-up).
3. **Full-lifecycle hermetic e2e** — `RegisterAccount → PrepareHostPlan(Create)
   → Approve → Apply → Observe(present) → PrepareHostDestruction → Approve →
   Apply → Observe(gone)` through the real Store handlers with a mock `Api`.
4. **cloud `INTENT.md`** — manifests the on-demand compute-provisioning
   capability and the billing-hour reuse-pool principle.

Integration order (each a fast-forward; all branches are one commit ahead of
main): land signal-cloud main → land meta-signal-cloud main → cloud (repin
meta dep to `branch=main`, drop the `[patch]`, `cargo update`, build green +
e2e) → land cloud main → verify every main builds + tests green.

## 3 · Explicitly NOT in this workflow — and the unblock for each

The "e2e tested on main" bar forbids landing what can't be soundly built or
verified yet:

- **Reuse pool + deferred-effect seam** — implementable hermetically but not
  yet at impl-spec depth, and the reaper rides the async seam. **Next build:**
  I'll do the spec+build pass (like Phase 1's) and land it on main after this.
- **Install hop + horizon model + ARM/x86** — genuinely fork-gated; building
  blind would land unverifiable architecture on main. **Unblock:** your three
  decisions (report 56 §7; my leans: cloud-owns-install, register-after,
  ARM/CAX11).
- **Live "create a real VM" e2e** — **unblock:** a Hetzner account + token at
  gopass `hetzner/api-token`. Until then the e2e is hermetic (mock `Api`).

This keeps main's tested-bar honest: everything landable-and-verifiable lands
now; the rest is staged with a concrete unblock, not guessed onto main.

## 4 · Landed (2026-06-18) — verified

All three mains landed green and independently re-verified from canonical
checkouts:

- **signal-cloud** `main` = `1466d949` — read-only compute-host wire vocabulary.
- **meta-signal-cloud** `main` = `f541bc65` — Phase 1 + the `PrepareHostDestruction`
  Destroy-on-wire op (additive; `DesiredHostState`/`HostPlan` unchanged).
- **cloud** `main` = `337c53d0` — Phase 1 integration + Destroy-on-wire handler +
  the full-lifecycle hermetic e2e + `INTENT.md`. `[patch]` removed; both sibling
  deps at `branch=main` resolving one `signal-cloud` (the `links` collision is
  gone). Independent rebuild: green; **9/9 hetzner tests pass**, including
  `full_host_lifecycle_runs_through_the_store_handlers`
  (register → create → observe-present → destroy → observe-gone).

### Heads-up — `schema-rust-next` drift (latent, not a landing defect)

The latest `schema-rust-next` (`bb4dfe29`) / `schema-next` (`b3be7d0f`) retired a
struct-field syntax that `signal-cloud@1466d949` and `signal-domain-criome`
sources still use, so a *broad* `cargo update` makes their build scripts panic
(`RetiredStructFieldSyntax`). The landed `Cargo.lock`s pin the working tooling
(`schema-rust-next 733b76d3`), so **committed builds are green** — but future
dependency bumps must stay surgical (`cargo update -p <crate>`, keep
`schema-rust-next`/`schema-next` pinned) until `signal-cloud` /
`signal-domain-criome` migrate off the retired syntax. That migration is a
separate maintenance item, not part of this work.
