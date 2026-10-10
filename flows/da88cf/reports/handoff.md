# Handoff — da88cf (Psyche Fable) to its successor

Compact state as of log entry 147 (~00:45 host time, 2026-09-26). Host clocks are the reference; relay times run ~40 min ahead of them. Everything below is drawn from `log.md` unless it names another file.

## 1. Objective tonight

Lead tonight's integration wave. Land the night's fixes declaratively on the repository mains, deploy them to ouranos and then to Prometheus through Lojix, repair the tailnet from cluster data, make the daisy chain (ouranos → Prometheus → zeus over USB/LAN) work without hotfixes and test it, and publish a night report as a visual artifact by 06:30. The living's constraints:
- **Prometheus-only builds.** Remote builders are the default. Local fallback is allowed only after a witnessed remote failure, and every fallback is reported to da88cf with the remote error. It is never routine, and ouranos stays quiet. See `vision/prometheus.md` (the sections "Move all the building to Prometheus" through "Prioritize Nix builds for everything").
- **No hotfixes.** Everything is declared from cluster data and deployed properly (`vision/daisyChain.md`, `vision/clusterData.md`).
- **jj only** in Primary and in the repositories. Raw git is not used.
- **Maximize Opus until 07:07.** At ~00:40, 9% of the weekly usage remained against an 8% floor, and it resets at 07:07. Keep starting waves until the usage is spent or 06:30 arrives. Refresh through Flow Start near 60% context and do not slow down (log 146).
- **Artifact by 06:30.** Its source is `reports/night-2026-09-25.md`.
- **Garbage collecting.** A low-power subflow keeps Prometheus's disk clean (`vision/garbageCollecting.md`).
- The living's words are quoted only in `vision/`, never inline here.

## 2. Seats and ownership

| Seat | Role | Owns tonight |
|---|---|---|
| e167d8 | Psyche Opus, successor of 88475f | Receives the per-wave reports. Owns the Flow 0.13.0 and message 0.14.0 finals. |
| 88475f | Psyche Opus, crossover-only | Relays the living's words. Ran the Prometheus GC and the exact-24 messenger-row retirement and its psyche recovery (evidence is in its witnesses). |
| b7da5d | Field Sol | Host and Flow activations, Lojix deploys (ouranos, then Prometheus), secret minting (root ssh works; sudo does not), and the deploy-window cleanup. |
| 504461 | Field Astra | Review only. Its Home user-environment activation was stood down. It diagnosed deployment 29 (no single cause) and reviewed the retirement. |
| e71dab | Field Luna | Orphan-process cleanup (done), the transcript audit, and the retirement review (final grade B). It mutates no messenger rows. |
| 00f95a | Mind | messenger-clj owner. Put the Home pins on main 5f14f9da and ruled on m1 and m6. |
| a676b3 | Mind Sol (field-clj) | Integrated the field-clj consumer pin (CriomOS d193bafc, Home 478b4ea0). |
| f5a74e | Mind | Topology/roles report and the codex-next unit trace. |
| 38de5b | predecessor, crossover-only | Handed over the wave state. Its wave report and addenda are the earlier record. |
| 5f38bc | (branch owner) | Accepted the disposal of its branches. The OpenCode content is kept under `retained/opencode-home-5f38bc`. |

## 3. Decisions taken under delegated judgment

The living's "best judgment" delegation is recorded in `vision/clusterData.md`.
- **Builder policy.** The refinement governs over the earlier absolute relay: Prometheus by default, local fallback only after a witnessed failure, and each fallback reported (log 30).
- **Tailnet CA design.** A cluster CA is declared in cluster data and installed on every node: ECDSA P-256, name-constrained. The controller stays on ouranos. Enrollment is an argv-free oneshot that reads a sops preauth key (one reusable key per host), with its login URL derived from cluster data. Membership is unchanged. Force-reauth of ouranos is allowed. Field mints the secrets as root and pipes them into sops, and no agent sees them. The pipe is plain, with no jq (logs 36, 134).
- **horizon-rs.** The base is ee8d6f8 (0.12.0). b45d6ad (753e69's 0.5.1 line) is abandoned and MacAddress is discarded. A single 0.13.0 bump (a3ddaf86) bundles the tailnet references, the required router `country`, and UsbDownlink. horizon-rs main was moved sideways onto it, and the signal mains were reset under the same ruling (logs 78, 95, 113).
- **UsbDownlink by bus role** with an IPv4 CIDR ("no matter how we plug"). The MAC-address chain is discarded (log 50).
- **Route A for the Nexus.** Two deploys and no hand switch. lojix 8.0.0 carries a startup quarantine for undecodable rows (log 95).
- **Model list.** Gemma 4 26B is restored beside qwen3.5-122b on CriomOS-lib. The choice of "latest" Qwen and Laguna go to the living (log 41).
- **Discards.** The ruled branches were deleted with proofs. The 16 stale jj workspaces were forgotten. Twelve stale Orchestrate locks were released: 8 from retired flows and 4 from 753e69. flow07-ouranos-b7da5d was proven pin-only and deleted (logs 81–106).
- **Builder capacity.** goldragon gets NixBuilder.Some.8 for Prometheus, corrected Metal cores (16), and ouranos off the builder list. Decoupling build_cores is a horizon-rs follow-up for the book (log 119).
- **Home via host deploy.** Home reaches ouranos through the CriomOS host deploy, as one activation owned by b7da5d. "Which path owns Home" stays with the living (log 61).
- **Flow 0.13.0 deferred.** It is not in the first Home activation. It joins integration step 2 with message 0.14.0 when the finals are green (log 98).
- **Prometheus boot-once timing rule.** One boot-once deploy after step 2. If step 2 is not on main by ~03:30 host time, deploy step 1's CriomOS revision (3e2cc8be, or e6a83edc with lojix 8) so the morning finds the two-model catalogue and the USB fix declared (logs 45, 128).
- **Retirement ruling.** 88475f's subflow is the sole executor of exactly 24 named stale rows. Exclusions hold, and flow-data deletion is authorized for nobody tonight. The gate is distill → archive → delete (logs 68–72, 79).
- **Pre-existing check failures are not gates.** The gates are specific checks plus both host toplevels (log 67).

## 4. Repository mains and bookmarks

| Repository | main | Live bookmarks |
|---|---|---|
| CriomOS | **e6a83edc** (3e2cc8be + lojix 8.0.0 pin). 3e2cc8be = USB tip + lojix a67f5773 + Home 4a9d85d7 + criomos-lib 6db67c3b | `wifi-country-da88cf` 71ab4707 (742f03d mergeable now; 71ab470 needs 0.13.0 data), `criomos-fixes-da88cf` 66aad7c9, `usb-downlink-da88cf` 946bcbd5, tailnet bookmark 216b4035, step-2 integration bookmark (in progress), `wave3-checks-da88cf` (in progress) |
| CriomOS-home | **4a9d85d7** (5f14f9da pins + diverged line merged) | `home-fixes-da88cf` 98255d10 (codex-next handoff, owned checks to gates/, niri spawn, Herdr module fixes), `retained/opencode-home-5f38bc`, `wave3-home-da88cf` (in progress), step-2 Home integration bookmark |
| CriomOS-lib | **6db67c3b** (gemma + qwen3.5-122b) | `models-da88cf` = main |
| horizon-rs | **a3ddaf86** (0.13.0) | tailnet bookmark = a3ddaf86 |
| goldragon | main carries the rotated opencodeServerPassword (Prometheus + ouranos recipients) | tailnet bookmark a3fdb232 (repin to 0.13.0, five preauth names, ouranos TLS refs + CA None + UsbDownlink 10.44.0.0/24, Prometheus MX + NixBuilder 8 + Metal 16). goldragon/secrets gets the minted secrets and the CA from b7da5d |
| lojix | **f090da07** (8.0.0, on the tolerance commit 1c9b43ac) | `lojix-store-tolerance-da88cf` 1c9b43ac |
| signal-lojix | **cd164896** (6.0.0) | none |
| meta-signal-lojix | **c0f883c5** (7.0.0) | none |
| flow / message | via e167d8: Flow 0.13.0 on flow main (signal-flow 6.1.0, meta-signal-flow 8.0.1). message 0.14.0 is on a branch repinned to signal-flow 6.1.0, and its revisions will move once more | Home keeps message 8aa6d7b4 until step 2 |
| messenger-clj | main includes the m6 port | m1/m6 bookmarks deleted |

## 5. Active dispatches

- **Step-2 integrator (Opus).** Builds a CriomOS integration bookmark (wifi → criomos-fixes → usb-downlink → tailnet), rebased onto e6a83edc and pinning lojix f090da07. It also builds a Home integration bookmark from `home-fixes-da88cf` 98255d10. It evaluates both hosts against goldragon a3fdb232 composed with horizon 0.13.0, and runs the merged checks and the two VM tests one at a time. **Returns:** bookmark revisions, check and VM results, and readiness for the main moves. It moves no mains until the secrets land.
- **Field b7da5d, ouranos deploy.** Deploys from CriomOS e6a83edc with a SecretsDirectory: Evaluate → Realize (a new derivation is expected) → TestActivation with witnesses → ActivateNow → window cleanup. The cleanup covers the Flow drop-in, the profile element, the heartbeat masks, the user-manager LOJIX_OWNER_SOCKET env, and the messenger links after PATH confirmation. The Qwen roots stay. **Returns:** deployment id, derivation, activation witnesses, Nexus 8 witnesses (quarantine count, configuration row).
- **Field b7da5d, minting.** Tailnet secrets for GO MINT: CA, TLS, and five preauth keys into goldragon/secrets, and the CA recorded on the goldragon bookmark. **Returns:** commit revisions and key names only.
- **Wave 3 Home (Opus, low build priority).** On `wave3-home-da88cf`: a feature-gated field-monitoring Home module and a declared herdr-server user service, both default off. **Returns:** bookmark revision and check results.
- **Wave 3 checks (Opus).** On `wave3-checks-da88cf`: fixes for resolver-role-policy and router-non-router-lazy, aiming at a green check set. **Returns:** bookmark revision and check results.
- **GC watcher.** **Returned.** The 00:00 sweep ran; details are in `receipts/gc-2026-09-26.md`. The 348e7b closure is gone and the six protected paths are present. ouranos is at 93%.
- **e167d8's finals.** Flow 0.13.0 and message 0.14.0 revisions once the Prometheus checks are green. They feed step 2 as the second Home activation, or become the first item of the morning.
- **Wave-2 interim to e167d8 and a status ask to b7da5d** were dispatched (log 121).

## 6. Blockers and unknowns

- The ouranos activation is not yet witnessed. Deployment 32 failed because its request carried NoSecrets. The resubmission from e6a83edc is pending.
- Step 2 cannot reach main until the tailnet secrets are minted and on goldragon/secrets and goldragon a3fdb232 is merged.
- There are six Prometheus builder slots, and contention from our own ~20 build hooks caused the night's slowness. Run builds one at a time and in priority order.
- headscale preauthkey output parsing is settled as a plain secret pipe. Per-host age recipients other than ouranos are unverified.
- The goldragon record for ouranos's UsbDownlink is included in a3fdb232 and must be confirmed in step 2's evaluation.
- Prometheus runs hand-switched generation 55, which Lojix does not know. Deploying anything older than 3e2cc8be would regress it.
- A Lojix deploy stages the whole closure through ouranos's store, which has ~66 GiB free at 93%. Gemma (48 GiB) must be copied over ssh first (the timing plan is with b7da5d).
- Prometheus's restore-on-AC-loss setting can only be checked at the box.
- The deployment-29 (Home user-environment) cause is unknown. There are two candidate windows.
- Flow 0.13.0 + message 0.14.0 finals are not yet green.
- Lock collision: flow 542442's lock 907 touches a check that the tailnet branch deletes.
- Deviations on record: a local cargo build of a scratch redb repair tool (repin train), and a Realize submitted without a separate Evaluate (deployment 32).

## 7. Next actions, in order

1. **ouranos activation witnesses.** Take b7da5d's report for the e6a83edc deploy: derivation, TestActivation, ActivateNow, Nexus 8 startup (quarantine counts), and the cleanup window. Then unroot nothing yet; the Qwen roots stay until Prometheus lands.
2. **Step-2 main merge.** When the minting commits land: merge goldragon a3fdb232 with the CA onto goldragon main, then take the step-2 integrator's CriomOS and Home integration bookmarks onto main after green checks and the two VM tests (tailnet-enrollment, three-hop UsbDownlink). Fold in Flow 0.13.0 + message 0.14.0 if e167d8's finals are green. Then deploy ouranos a second time (Route A: lojix and data, Home second activation) and tailnet-enroll ouranos.
3. **Prometheus boot-once.** Evaluate → Realize → ScheduleBootOnce with rollback, from step 2's main. If step 2 is not on main by ~03:30 host time, use step 1's revision. Copy Gemma first. Then check tailnet enrollment on Prometheus and unroot the three Qwen shards on ouranos.
4. **Daisy-chain test.** Launch the tester subflow with `reports/daisy-chain-test-brief.md`: forced wired interface on zeus, per-hop evidence, AP country and log level, and hotfix-absence negatives (NetworkManager share, firewall drop-in).
5. **Wave-2 report** to e167d8, with revisions, deploy witnesses, and the test grade.
6. **Morning book fill.** Resolve the PENDING markers in `reports/night-2026-09-25.md` and fold in the wave-3 results and GC receipt. Book items: realize-on-target design; build_cores decoupling; Blueprint/aggregate; OpenCode in Home; primary/flow submodule at 0.9.0; deletion gate; deployment 29.
7. **Visual artifact by 06:30.** Run the `visual-report-from-md` skill on `reports/night-2026-09-25.md`.

In between, keep new Opus waves going from the wave-2 plan's remaining rows until usage is spent, and refresh near 60% context.

## 8. Questions for the living

Copied from `reports/night-2026-09-25.md` §11.

1. **Which Qwen?** Keep 3.5-122B (largest, current), or switch to 3.6-35B-A3B, or Qwen3.8-27B from the proposal branch? Gemma 26B is restored beside it. Add Laguna S now (68 GiB; license to confirm)?
2. **Phone and Wi-Fi.** Does your phone connect to goldragon.criome with WPA3 (SAE)? If it fails, may an agent watch the access-point log while you retry?
3. **Laptop on Wi-Fi.** Should ouranos rejoin goldragon.criome automatically, reversing the 09-24 "Wi-Fi A" that an agent made?
4. **Power.** Will you set "Restore on AC power loss" to On in Prometheus's firmware, so it comes back by itself after a power cut?
5. **GitHub token.** May we treat the token in ouranos's Nix settings as exposed? You rotate it, and the new one goes into an encrypted secret. The old line stays until then, because private repos need it.
6. **Who installs Home.** Should Home come with the system deploy, or through its own Lojix "user environment" deploy? Today three mechanisms claim three different versions.
7. **Where Headscale lives.** Keep the tailnet controller on the laptop, which roams and sleeps, or move it to Prometheus, which is always on?
8. **Who is in the tailnet.** You said "those are the trusted nodes based on the trust value there in the cluster". Should membership follow trust? For example, tiger and zeus are trust Max but not tailnet members, while mirror-alpha and mirror-beta are members with no trust entry.
9. **Tailscale Inc.** Stop Tailscale sending logs to Tailscale Inc.? Keep using Tailscale's public relay servers? On 09-10, Headscale refused to start 29 times because it could not reach them from behind a hotel-style portal.
10. **Herdr restart.** When may we restart the Herdr server under its declared unit? It closes every open pane once.
11. **Codex-next cutover.** When is a quiet window to move Codex-next sessions from the hand-started copy to the declared server? It ends the attached sessions.
12. **Monitors.** Keep or drop core-checkup, field-census, field-checkup-shadow, field-luna-research, and the cloud-maintainer-chrome DigitalOcean script?
13. **Backup Wi-Fi radio.** Plug the ASUS dongle back into Prometheus in place of the SanDisk stick? Or declare the dongle's new port name?
14. **Daisy chain NAT.** Prometheus is both the house Wi-Fi router, with its own address sharing, and a downstream of ouranos. Accept three address-sharing layers in series as a named nested setup, or should one owner do it?
15. **Prometheus reboot.** da88cf read "get all the fixes deployed to it" as allowing one scheduled boot-once reboot of Prometheus with rollback. The reboot briefly drops your Wi-Fi, zeus and the builder. Confirm, or name a time.
16. **OpenCode in Home.** Your earlier request for OpenCode in Home is kept as open work, not done tonight. Still wanted?
17. **Unfinished words.** "Also on the message and flow development, which you'll get started on when you refresh ..." What did you want started?
18. **"lambda daisy chain".** Was "lambda" a mis-transcription? Of what?
19. **Model listing.** Is it acceptable that Prometheus's model list answers on the network without the API key?
20. **Speech-to-text.** Are the speech-to-text models you mentioned on 09-13 for Prometheus still wanted? None are declared.

## 9. Where exact values live

All paths are under `flows/da88cf/` unless noted.

**Vision (the living's words)**
- `vision/prometheus.md`
- `vision/clusterData.md`
- `vision/daisyChain.md` (includes the recovered e51411 statements)
- `vision/garbageCollecting.md`

**Log**
- `log.md`

**Reports**
- `blueprint-check-fix.md`: why the Blueprint aggregate check fails, with the exact Home/CriomOS diffs.
- `builder-capacity.md`: Prometheus cores/memory and the NixBuilder value proposal.
- `daisy-chain-plan.md`: daisy-chain design and branch verdicts (bus role, MAC chain discarded).
- `daisy-chain-test-brief.md`: acceptance-test brief for the tester subflow.
- `headscale-repair.md`: tailnet diagnosis and the CA design.
- `home-fixes.md`: first Home-fixes writer (codex-next, Lojix socket, registry fix).
- `integration-1.md`: integration step 1 (CriomOS-lib, Home and CriomOS main moves, the lojix stall).
- `inventory-branches.md`: targeted branch inventory of the deploy-path repositories.
- `inventory-system.md`: temporary system state on the reachable nodes.
- `jj-workspaces.md`: audit of the stale jj workspaces.
- `local-models-status.md`: served-model status and the living's model words, for the book.
- `lojix-secrets-input.md`: why deployment 32 had an empty secrets input (NoSecrets request).
- `lojix-store-tolerance.md`: the lojix 8.0.0 quarantine of undecodable rows.
- `night-2026-09-25.md`: night-report source for the 06:30 artifact, with the questions in §11.
- `opencode-secret.md`: trace of the OpenCode testing assertion and its secret.
- `prometheus-deploy-risk.md`: how Lojix stages closures through ouranos, and the model-file placement.
- `prometheus-pending.md`: Prometheus gen-55 provenance and the deploy form (boot-once).
- `prometheus-return.md`: the power-loss account and the first remote-build witness.
- `psyche-recovery.md`: d8df70/e51411 transcript recovery and the proposals.
- `repin-train-run.md`: repin train results (signal-lojix 6, meta 7, lojix 8, store gate).
- `repin-train.md`: the repin train map and the store risk.
- `step2-fixes.md`: the codex-next handoff, registry and lojix-ownership fixes.
- `tailnet-repair-slice.md`: Field slice for minting and deploying the tailnet.
- `usb-downlink-impl.md`: the UsbDownlink consumer and its test plan.
- `wave2-plan.md`: the 56-row disposition plan (wave-3 candidates come from here).
- `wifi-password-path.md`: where the Wi-Fi password lives and how to retrieve it (key names only).
- `wifi-power.md`: the 3 dBm display defect, MX country evidence, and the AP log level.
- `wifi-prometheus.md`: the Wi-Fi/Prometheus picture from cluster data and the live network.

**Receipts**
- `receipts/gc-2026-09-26.md`
- `receipts/gcroot-messenger-clj.md`
- `receipts/stale-root-348e7b.md`
- `receipts/branches-deleted.md`
- `receipts/workspaces-forgotten.md`
- `receipts/stale-locks-released.md`
- `receipts/registry-pin-removed.md`
- `receipts/broadcast-prometheus-only.md`
- `receipts/messages.md`

**Elsewhere**
- `flows/f5a74e/reports/codex-next-unit.md`
- 88475f's witnesses (retirement, recovery, GC)
- 38de5b's wave report
