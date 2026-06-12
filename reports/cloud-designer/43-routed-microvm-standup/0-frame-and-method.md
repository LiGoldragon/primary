# 43 · Routed microVM standup — frame and method

## Psyche decision (2026-06-12)

> [you can setup the full routed microvm. go all the way] (Spirit `se72`,
> Decision High)

Resolves the end-to-end test-target fork in favour of the **full routed
microVM** — a microVM with its own Criome domain and a reachable IP (the
`vm-testing` module: microvm.nix + tap + projected `networking.hosts`),
currently designed and CI-tested on CriomOS `next` but deployed to no node —
over the systemd-nspawn shortcut. Scoped to the lojix cutover validation, so
it coexists with `btc0` (operator e2e may still use nspawn) rather than
superseding it.

## Correction (2026-06-12) — the host is NOT reconfigured

The psyche clarified (Spirit `7let`): the e2e is harmless because lojix
deploys a full OS **into a throwaway KVM-hosted VM** — a broken deploy kills
only the VM, never the host. It does **not** require reconfiguring the host to
declaratively run a microVM. So this report's recon framing — the `vm-testing`
NixOS host-module (microvm.nix + tap + projected `networking.hosts`), which is
what raised the `5hir5bnz` host-risk and the zeus-vs-Prometheus debate — is
**superseded**. The real plan: run a transient qemu/KVM VM on **Prometheus**
(verified live: bare-metal, AMD-V `svm`, `/dev/kvm`, 32 cores, 124 GiB free;
qemu run via `nix`, no host config change) and have lojix deploy a full OS
into it. Prometheus's production config and networking stay untouched, so the
host-risk class is gone. The host-reconfiguring standup steps below no longer
apply; the rest (lojix-cli BootOnce mechanics, horizon/Yggdrasil reachability,
the deploy-into-target shape) remains useful.

## Why ground first

Standing this up means deploying a CriomOS config to a **live host** and
changing networking. Constraint `5hir5bnz` is explicit: **do not break
Prometheus networking** (Prometheus may be a router — highest-risk node for a
networking change). So this meta-report grounds a *safe* standup plan —
chosen host, deploy path with rollback, networking/IP mechanics, risk surface
— **before any change touches a live host**. All reconnaissance is
READ-ONLY: agents may `ssh` a candidate host to *inspect* state, but must run
no command that mutates it.

## Method

Read-only reconnaissance fan-out, each dimension writing its own numbered
file, then a synthesis standup plan (host choice, ordered steps, rollback,
risks, prerequisites). Runs in parallel with the lojix daemon-code track
(report 42 S0/S2–S4); the microVM standup is the prerequisite for S5's live
deploy.

Dimensions:

1. the `vm-testing` module on CriomOS `next` — how it works, what it needs
2. candidate host state (Prometheus + other reachable nodes) — role, KVM,
   networking, current generation (read-only ssh)
3. deploy path + rollback — how a CriomOS config reaches the host safely
   (BootOnce / router boot-once safety), how to roll back
4. networking + domain + IP — how the microVM gets a reachable Criome domain
   viewable from ouranos
5. risk history — `5hir5bnz`, `xv9v`, `kx32`, `1lex`, cluster/system-operator
   reports, the microVM design + CI history
6. synthesis — the safe standup plan
