# 46 · Lojix live end-to-end (S5) — execution-grounding frame

## Goal

The cutover validation (Spirit `se72`/`7let`; psyche authorized proceeding
2026-06-13): stand up a **throwaway qemu/KVM VM on Prometheus** (host config
untouched, run via `nix`) and drive the lojix **daemon** end-to-end into it —
deploy a full OS, proving the real `nix copy` + BootOnce activation land and
that the deploy survives an SSH disconnect. This is the first time the daemon
touches a target.

## Why ground the runbook first

S5 is live, novel, and multi-step, and the existing reports (41 fixture, 43
VM/test-cluster, 45 activation) don't fully pin the *execution* sequence:
- exactly how to build + run a throwaway qemu NixOS VM on Prometheus that is a
  reachable `ssh-ng` deploy target, host config untouched;
- the cluster-proposal / horizon piece — the VM as a node the daemon
  materializes + builds a toplevel for;
- how to run the `lojix-daemon` live (config via `lojix-write-configuration`,
  the two sockets, where it runs) and issue the `meta-lojix` `Deploy`;
- the disconnect-test method + resource bounds + rollback.

This meta-report produces the exact ordered, verified runbook **before any
live action**. All grounding is READ-ONLY plus safe dry-eval (`nix eval` /
`nix flake show` / read-only ssh inspection) — **no VM run, no deploy, no host
mutation**. The live execution follows, by cloud-designer, step by step, each
step verified, with the throwaway VM keeping it harmless to Prometheus.

## Method

Read-only reconnaissance fan-out → a synthesis runbook.

Dimensions:
1. the deploy-target VM — build + run a throwaway qemu NixOS VM on Prometheus,
   reachable for `ssh-ng` (base image + sshd + key + networking)
2. the cluster-proposal / horizon piece — the VM as a node the daemon
   materializes + builds a full-OS toplevel for
3. running the lojix daemon live + the deploy command (config, sockets,
   `meta-lojix` Deploy, the eval→build→copy→activate flow against the VM)
4. the disconnect test + resource/safety/rollback
5. synthesis — the ordered, verified S5 runbook
