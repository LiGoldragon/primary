# 8 · Deploy network incident — root cause + prevention (2026-05-28)

The Gemma deploy to prometheus knocked prometheus off the network and
required a blind hard reboot. The psyche asked for the root cause so it
can't recur. This report is that analysis.

## Timeline

1. `lojix` deploy of CriomOS main → prometheus, action `Switch`
   (live activation), `builder = prometheus`. Build succeeded (Gemma
   weights + mmproj + new system gen all built on prometheus).
2. Activation began: `stopping the following units: dnsmasq.service,
   hostapd.service, prometheus-llama-router.service`.
3. The ssh connection died: `Timeout, server not responding`. The
   deploy exited rc=1 — activation never completed.
4. prometheus was unreachable (ping 100% loss). No out-of-band access,
   so recovery was a blind hard reboot.
5. The reboot booted the **old** generation (the failed switch never
   committed the new gen as boot default), so the router came back and
   the deploy did **not** apply. No data loss; pre-deploy state.

## Root cause (definitive)

The live `Switch` activation **restarted prometheus's wifi access point
(hostapd)** — and prometheus is the LAN router we administer it
*through* — so the wifi dropped mid-activation, the ssh died, and the
switch was interrupted before it could restart the services.

Evidence:

- The deploy log explicitly stops hostapd + dnsmasq + llama-router.
- The deploy's actual new gen (`imiggsb678kn…`) vs the running gen
  (`4l0g3573…`) differs in exactly one networking-relevant way:
  hostapd's `ExecStartPre` script path changed
  (`xywkzw48… → nxmz1dbz…`) and `router-wifi-sae-passwords.sops`
  entered the closure. So hostapd's config changed → switch restarted
  it.
- That change traces to recent CriomOS `main` router work (commits
  *"align router wifi projection names"*, *"tolerate derived router
  wifi names"*) plus sops-sourced wifi password wiring — **not** the
  LLM/Gemma changes, which never touch networking.

**Correction of an earlier mis-step:** a first closure-diff suggested
"dnsmasq removed / router=false". That diff was run against the wrong
same-named store path. The horizon lojix actually projected has
`behavesAs.router = true`, and the real gen keeps dnsmasq + hostapd. So
it was a service **restart** (config changed), not a removal.

## Why it was self-inflicting

prometheus is both the AI node and the cluster router (hostapd AP +
dnsmasq DHCP/DNS). We reach and administer it over the network it
serves. Any live activation that restarts hostapd/dnsmasq severs our
own connection — and if the switch is interrupted mid-restart, the
services don't come back until a reboot.

## The compounding exposure — no out-of-band access

There is no console / serial / IPMI access to prometheus. So when the
network dropped, the only option was a blind hard reboot. It happened
to recover (the failed switch left the old gen as boot default). Had
the switch committed the new gen first, or had the new gen's wifi
config been broken, the reboot would have booted into a broken router
config and left prometheus **unrecoverable** without physical access.
This is the most dangerous part of the incident.

## Prevention

1. **Deploy the router node with `Boot`, not `Switch`.** `Boot` sets
   the new gen as boot default without live-restarting units; the
   reboot starts hostapd/dnsmasq fresh — no mid-activation wifi drop.
2. **Establish out-of-band/console access to prometheus before any
   router deploy.** This is the real gap; without it a bad activation
   is unrecoverable.
3. **Verify the new gen's router/wifi config (SSID, interface, SAE
   password) before rebooting into it.** The recent "derived router
   wifi names" work is explicitly fragile ("tolerate…"); confirm it is
   correct for prometheus first.
4. **System-operator owns the router-wifi projection** (horizon-rs, the
   router module, the datom). They should confirm those recent
   router-wifi changes are correct for prometheus before it is
   redeployed — this is the change that triggered the hostapd restart.
5. Optional guard: a deploy preflight that refuses to live-restart
   hostapd/dnsmasq on the host the deployer is connected through.

## Separate, still-unexplained: the first hard shutdown

Earlier (first deploy attempt) prometheus hard-rebooted mid-**download**
— before activation, so unrelated to the router restart. A hard power
loss leaves no logs; likely power/thermal/hardware. Flagged as a
distinct unknown; if it recurs, suspect hardware.

## Status + the blocked Gemma deploy

prometheus is healthy on the old generation (router + old models
serving). The Gemma build is cached on prometheus, so a retry won't
re-download. But the Gemma deploy is **blocked** until there is a safe
router-deploy path: out-of-band access + `Boot` + a verified router-wifi
config + system-operator's sign-off on the router-wifi projection.
Retrying via `Switch` — or even `Boot` into an unverified router config
— risks another lockout.

## Anchors

- Cached horizon: `~/.cache/lojix/horizon/goldragon/prometheus/horizon.json` (`router: true`).
- Gens: old `4l0g3573…`, deploy's new `imiggsb678kn…` (diff: hostapd
  pre-start + router-wifi sops).
- Intent: spirit 1105 (constraint — deploys must not knock out
  prometheus's network).
