# Evidence receipt — 2026-09-26

Origin: returned bounded subflow observations and persisted-source recovery; main did not independently inspect infrastructure.

## Network

prometheus_network observed Ouranos enp0s31f6 192.168.1.5/default and DHCP lease for Prometheus 10.44.0.148. Ouranos SSH probes to Zeus 192.168.18.95 and zeus.goldragon.criome timed out. Its final strict SSH probe to prometheus.goldragon.criome timed out before session. No current Prometheus-side state or Prometheus-to-Zeus route witnessed. Historical bus-role implementation: 946bcbd501f14050c04d6025bc879a4e72fc0122; inclusion in current main and deployment unverified.

Network worker artifact: reports/prometheus-network-diagnosis.md.

## Build receipt recovery

zeus_green_receipts recovered current CriomOS main d04257a8efcc73842970dadd782a19300c48f84d, Home fed500843629c828a91fa0e06b9946b69c167898, Lojix 3fc95f0cf4eaf14ff62898c4783ebbc670fdf96b. No current green receipt located for any of:

- nixosConfigurations.target.config.system.build.toplevel
- homeConfigurations.li.activationPackage
- homeConfigurations.bird.activationPackage

Zeus Horizon input SHA256: 46ab9e13f090e5ae7972d04cb655beb2132cc09bf57dea1ea72e903a0ce4c648, reported materialization 2026-09-26 15:55:56 CST. Presence and suitable projection do not prove evaluation/build success.

Deployment 35 Evaluate success was for bootstrap dfb2c89c, not a build receipt. Historical accepted set: CriomOS 35fc6e9896d012bf6f54a9916bd8e725af3fcea0, Home a61b02d0cf69de757bdf8b5fa0f336f78f5054ee, deployment 54 TestActivation and 55 ActivateNow plus embedded li/bird Home service success. Historical only.

Sources recovered by worker: flows/b860be/receipts/lojix-35-37-2026-09-26.md; flows/da88cf/reports/wave3-checks.md; flows/01a030b7/witnesses/lojixDeployments.md; flows/01a030b7/witnesses/embeddedHomeSynchronization.md.

## TLS ownership

Recovered wave3-checks error: stale Ouranos materialization omitted TailnetController fields. Current inspected materialization contains tlsCertificateReference=headscaleTlsCertificate and tlsKeyReference=headscaleTlsKey. No fresh evaluation performed. Recorded rematerialization owner: Field Sol b7da5d under b860be ruling. Current availability/acceptance not witnessed. No current-line three-build owner or source-level TLS repair owner located.

## Transfer implementation boundary

zeus_transfer observed active Ouranos service package lojix-8.1.0, PID 63865, started 2026-09-26 17:17:39. Package identity alone does not prove exact source parity. Inspected 3fc95f0 non-daemon-host branch copies derivations, builds with --store on target, ignores supplied builder, roots target result and checks target path-info. No Zeus execution receipt for that branch. Older daemon-local branch passes --builders and activation copy may use --substitute-on-destination. Generated Prometheus cache intent is not live Zeus configuration, selected transfer, or route proof.

## Publication boundary

Worker reports Primary jj working copy 29239f1b, conflicted parent ba5b13fd, conflict resolution represented in working copy and unrelated concurrent files present. No commit/push performed: scoped publication requires separate authorized shared-tree conflict/isolation work. No infrastructure change, activation or deployment performed by these dispatches.

## 2026-09-26 — Corrected Home generation and reusable Flow 0.17.4

Origin: directly returned build-worker witness; no main-seat binary invocation. One corrected complete-host local build, 2 jobs / 2 cores, retained terminal COMMAND_EXIT_CODE="0" at22:20:38. Log: /var/tmp/flow-0174-home-validation-6fe957/gate4-complete-host-li-activation-package.log.

Immutable source tuple: CriomOS d04257a8efcc73842970dadd782a19300c48f84d; Home daf026f1e02bcd092f0ecc43b81207c96c6ec1b3; Flow bc464e5e1b94fcc179af73111f43b69db1f69fc5, locked NAR sha256-ZIuxiKiA/Y5RytWDIrr5hGq+q2P5i2+qgqFTlgwtQug=; complete-host four input tree manifests unchanged after build.

Generation /nix/store/8fx6k2w4q69z61dq3qiqp1rna7g8admb-home-manager-generation; registered deriver /nix/store/gcvkqyrblrxv8wkk9q8771rmy5wky1yi-home-manager-generation.drv.

Flow output /nix/store/7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4 verified valid; deriver /nix/store/vfv1g24y22h9iqj285d328kziwqy6b7c-flow-0.17.4.drv. bin/flow-nexus exists0555,size5738008, SHA25641c089c92a4ddfe38b60a496e08bc2840c4776a026ce034c7a8562a8bc3cc4cc; not invoked. Generation's next Flow unit references that executable.

Static stable Message unit byte-equal live managed unit SHA25672349688a2844c6610ce4eb5f5b3e967dd3c47a96a0cc0e2e93181388e4dc5ac. Stable Flow base unit remains0.14.0; current external override selects0.12.2. Candidate has no flow-nexus.service.d/override.conf, so no declarative preservation proof of external drop-in; activation-time survival remains unwitnessed. No activation, runtime launch, service operation or store migration. Prior fullcheckexit124 remains non-green. Reservation7880 retained. Direct useful package-provenance delivery toFable8904b1 andField9ac67c delegated; actual receipt grades pending.
