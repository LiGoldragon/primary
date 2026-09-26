# Handoff — b860be (Psyche Fable, successor of da88cf), written at wind-down

Written on the living's order relayed at ~02:00 host time, 2026-09-26: model usage at 99%, Claude seats may be stopped cold before the 06:59 reset. Codex seats (Field Sol b7da5d, Mind seats) are not affected and continue under the rulings below. Everything here is drawn from `flows/b860be/log.md` (the ordered record) and the receipts under `flows/b860be/receipts/`; claims are marked as claims.

## 1. State at wind-down

Witnessed by b860be subflows unless marked (claim):

- goldragon main **ddf27e0c**: merge of the mint commit 3e6ecfa9 and the tailnet bookmark e8ce1e42; cluster data carries the tailnet CA, ouranos `UsbDownlink.{ 10.44.0.0/24 }`, five preauth names, Prometheus NixBuilder 8 / Metal 16; five sops files (four to ouranos's age key, Prometheus's preauth to its own); mirrors and vm-testing preauth secrets are declared but NOT minted. `nix flake check` green on Prometheus (receipts `goldragon-check-…`, `goldragon-main-…`).
- field-clj main **a2c278d3**: deps.edn pins clojure 1.12.6, so the deps fixed-output hash `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=` is the same under Home's nixpkgs and field-clj's own; each derivation built twice on Prometheus, deterministic; tests green (receipt `field-clj-deps-hash-…`).
- CriomOS-home bookmark **integration-2-b860be 7dd9e666** (integrator's claim): 8a60835c (flow 0.14.0 9fcd625a + message 0.14.0 930c5169 pins) + wave3-home 182400f0 + heartbeat-gate 9d721984 + field-clj a2c278d3 pin; evaluates green with Lojix's ouranos inputs.
- CriomOS bookmark **integration-2-b860be** (integrator's claim, in progress at wind-down): fd0be3f0 + hotfix-removal d9f808ec + Home pin → 7dd9e666 + wave3-checks a28fadfe + a filter keeping `nixos-*` toplevels out of `checks`; lojix pin stays f090da07 (8.0.0). Both host toplevels evaluated against the goldragon data. Builds on Prometheus NOT yet run. The integrator's own account lands in `flows/b860be/reports/integration-2.md`.
- Lojix on ouranos: deployment 32 Failed (Eval, 3e2cc8be); 33 Evaluate Succeeded (e6a83edc); 34 Realize Failed BuildFailed on the field-clj deps hash — now fixed at the source. Current host generation 4. (b7da5d claims for 33/34.)
- ouranos store: 20 GiB free after collecting a stray /tmp root (9.5 GiB freed); Gemma (48 GiB) pre-seeded from Prometheus and rooted under `/home/li/.local/state/b860be-gcroots/gemma-{1,2,3}`; da88cf's Qwen roots (~71 GiB) still rooted; Lojix audit roots untouched.
- Zeus: in cluster data (ThinkPad T14 Gen2; Edge, LowPower, HardwareVideo); reachable over Yggdrasil, root ssh answers; 188 GiB free; nixos 26.11.20260813 hand-deployed; NO Lojix history. Transports verified by b7da5d (claim): `ssh-ng://root@{ouranos,prometheus,zeus}.goldragon.criome` with matching ssh destinations.
- Prometheus: current = booted, 45 boot entries, Lojix history terminal (b7da5d claim).
- lojix 8.1.0 = 3fc95f0c on lojix main (da88cf claim; 15 checks green incl. a two-machine VM check; builds remote nodes in the target store). Not pinned in step 2 by ruling.
- The night book: `flows/b860be/reports/night-2026-09-25.md` (sections 1–12 da88cf's, section 13 the successor's); a final refresh was dispatched at wind-down; the visual artifact is produced from it.

## 2. Rulings in force (Field Sol may act on these without a new GO)

1. **Builder rule**: Prometheus by default (`--option max-jobs 0`, ssh-ng builder), retain offload lines; local build only after a witnessed remote failure, reported. One build at a time.
2. **Step 2 completion** — exact revisions from the integrator's report (`reports/integration-2.md`): CriomOS `integration-2-b860be` = **416afd41**, CriomOS-home `integration-2-b860be` = **7dd9e666**; both mains fast-forward (e6a83edc → 416afd41, 4a9d85d7 → 7dd9e666). Before any main moves, in order: (i) evaluate and build the 48 CriomOS checks on 416afd41 one at a time on Prometheus, offload lines kept — `agent-intercom-command-ownership` printed an unexplained failure once and must be understood; (ii) run the tailnet-enrollment VM test, then usb-downlink-chain; (iii) build the five focused Home checks and the ouranos Home activation on 7dd9e666 — the first real proof of the field-clj hash fix; (iv) regenerate Lojix's generated secrets input for each host from goldragon ddf27e0c (today it holds four of the nine sops files). Build the CriomOS line on Prometheus; gates are the merged checks (pre-existing failures fixed by wave-3 are expected green; `criome-daemon-config-roundtrip` / criome-deps-0.9.0 is a known pre-existing red and not a gate), the two VM tests (tailnet-enrollment, three-hop UsbDownlink), and both host toplevels realizing. When green: move CriomOS main to the CriomOS bookmark head and CriomOS-home main to 7dd9e666 (jj, `-m`, verify on the real remote with `git ls-remote`). If a gate is red, do not move mains; write the red into `flows/b7da5d/reports/` and stop.
3. **Second ouranos deploy** (from the new CriomOS main, goldragon ddf27e0c, SecretsDirectory): Evaluate → Realize → TestActivation → witness from Prometheus that its default route, DNS and Internet go through ouranos's declared downlink (the hotfix files are removed in the same generation; a rollback would cut Prometheus's uplink) → ActivateNow → cleanup window (Flow drop-in, profile element, user-manager LOJIX_OWNER_SOCKET env, messenger links after PATH confirmation) with the **field-luna-heartbeat masks KEPT** (Home 7dd9e666 gates the unit off; masks come off only once a Home activation carrying that gate is witnessed). Witness Nexus 8 startup (quarantine count).
4. **Prometheus boot-once**: Evaluate → Realize → ScheduleBootOnce with rollback, the three stages chained so no GC falls between; do not run a garbage collection on ouranos during it; watch `df /nix/store` on ouranos. The living's question 15 (confirm the reboot or name a time) stands: if the reboot is judged too disruptive at the hour, leave it scheduled-but-not-rebooted and say so.
5. **Zeus** (the living: "Make sure Zeus is updated."): first Lojix deployment, CompleteHost, explicit transport as verified, Evaluate → Realize → TestActivation → ActivateNow if the test holds; record that no Lojix rollback baseline existed.
6. **After Prometheus lands**: remove da88cf's three Qwen roots on ouranos; then the daisy-chain acceptance test per `flows/da88cf/reports/daisy-chain-test-brief.md`.
7. **Not tonight**: no UserEnvironment Lojix deploy (Home lands through the host deploy); no codex-next unit transition; no flow-data deletion by anyone; no repin of lojix 8.1.0 in step 2 (step 3 or morning); no GC root removal beyond rule 6.
8. **Reports**: Field/Mind reports to b860be if it answers, else to e167d8, else into `flows/b7da5d/reports/`; every gate with its Lojix terminal record.

## 3. Book items and questions for the living (beyond da88cf's twenty)

- Which monitors to keep and where; when the Herdr server handover may happen; where core-checkup's roster comes from (wave-3 Home).
- Codex-next cutover window (f5a74e's unit trace; recovery unit holds 863 tasks).
- Home deploy owner (host deploy vs user-environment deploy) — still the living's.
- Hotfix removal trade-off: rollback after the second ouranos deploy would leave Prometheus without uplink; stale base-chain rules from the unreadable hotfix script persist until reboot or flush.
- Blueprint: host toplevels in `checks` (ruled out at the consumer tonight; Blueprint change if the filter is not enough).
- criome-deps-0.9.0 does not build on Prometheus; criome-daemon-config-roundtrip imports it — needs an owner.
- Other clj-build consumers with `follows` and no clojure pin (messenger-clj) can hit the same deps-hash mismatch.
- lojix 8.1.0 gaps: retire does not remove the target root; Realize terminal lacks the output path; no live proof yet of zero staging on ouranos.
- Mirror and vm-testing tailnet preauth secrets not minted.
- Deviation on record: Mind Sol a676b3 started a local nix build on ouranos without offload evidence, stopped on ask.
- 24-route reap review grade B (e71dab): 24/24 retired by postcheck; strict no-pane acceptance partial for 13 IDs.

## 4. Morning corrections from the living (2026-09-26 ~07:50–07:55, via e167d8)

- "There must never be AI models on any other node than Prometheus, which is why Prometheus can only be built on Prometheus." and "There should be no AI models on [ouranos] ever and we can garbage collect." — e167d8's subflow removes the Gemma and model roots on ouranos and collects; nobody pre-seeds or roots a model on ouranos again; a declared closure that pulls a model onto ouranos is a cluster-data defect.
- Consequence for rule 2: **repin lojix to 3fc95f0c (8.1.0, build-on-target) in CriomOS `integration-2-b860be`** before the gate run, so the ouranos activation brings a Nexus that realizes Prometheus's closure on Prometheus. Rule 7's "no repin of 8.1.0" is withdrawn. Rule 6's Qwen-root removal is done now, not after Prometheus.
- "You can reboot Prometheus whenever you want. I don't have any limitation on rebooting it." — rule 4's reboot is authorized at any time.

## 5. Bootstrap order (ruled ~08:05 on b7da5d's evidence)

The live Nexus on ouranos is Lojix 7 composing Horizon 0.12; it rejects the 0.13 proposal from goldragon ddf27e0c client-side. The step-2 CriomOS tree does not evaluate under 0.12 inputs (tailnet-roles). Therefore Route A, two deploys:

1. **Bootstrap revision** `bootstrap-b860be` on CriomOS: e6a83edc + criomos-home pin 7dd9e666 + lojix pin 3fc95f0c (8.1.0). Mind Astra evaluates it with the existing 0.12 generated inputs, builds the ouranos toplevel and the Home activation on Prometheus (first proof of the field-clj fix), pushes the bookmark. No main move for it.
2. **Bootstrap deploy** (b7da5d): ouranos through Nexus 7 with the 0.12 proposal that deployment 33 accepted, from `bootstrap-b860be` (immutable rev): Evaluate → Realize → TestActivation → ActivateNow; heartbeat masks kept; witness Nexus 8.1.0 startup (quarantine count).
3. **Step 2** as in rule 2 and §4, with 416afd41 rebased to include the same two pins, gated, mains moved, then the second ouranos deploy through Nexus 8.1.0 with goldragon ddf27e0c (rule 3), then Prometheus built on Prometheus (rule 4, reboot authorized), then Zeus (rule 5).

## 6. Piper ruling and the AI-node role (~08:40–08:50)

- The living on Piper: never used it, no problem losing it. Ruling: piper-tts (and with it pysilero-vad's 865 KiB model) leaves CriomOS-home's medium profile as one commit on the Home integration line; nothing else may pull model data into ouranos's toplevel or Home (why-depends witness); the bootstrap bookmark and the step-2 CriomOS line are re-pinned to the new Home head; then ouranos's own toplevel and Home are built on Prometheus; then Field Sol deploys the bootstrap through Nexus 7 with the 0.12 proposal.
- The living (~08:40, partial as relayed by e167d8): the AI node is a role in cluster data, not Prometheus by name ("whichever node plays the role of what we're calling a large AI node"); e167d8 maps that role for an Ethos spec. Until that role exists in data, Prometheus is the node that plays it.
- Rule as applied from the living's words: no model data of any size on a node other than the AI node.
