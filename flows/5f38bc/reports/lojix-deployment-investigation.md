# Lojix deployment investigation — 2026-09-24

## Scope

This report records the observed Lojix activation attempts and the present deployment boundary for Ouranos. It distinguishes socket/contract failures from Nix build placement and source-integration work. It contains no secret values or secret-file contents.

## Observed evidence

| Time / source | Observation | Meaning |
| --- | --- | --- |
| 2026-09-24 15:54:35 -06:00, user journal for PID 3260879 | lojix-nexus[owner]: structural wire conversion failed: Error { inner: Failure } | The live daemon rejected a structural wire conversion at that time. |
| /proc/3260879/exe | /nix/store/0hkvzd8x4k24bd1irgr20im9cj3yk4kn-lojix-6.0.0/bin/lojix-nexus | The listening daemon is Lojix 6.0. |
| ss -xlp | PID 3260879 owns both /run/lojix/ordinary.sock and /run/lojix/meta.sock | Both live sockets belong to that single daemon; no second controller was started. |
| Matched-client terminal receipt | /nix/store/7fclgzyw2y0pl5fwdp2a61xwyvi7020b-lojix-7.0.0/bin/lojix-meta exited 2 with (CliRejected [signal frame error: Signal frame I/O failed: failed to fill whole buffer]) | No Lojix job was accepted and no deployment ID exists. |
| Nix derivation metadata | client derivation is v8d2q3iv...-lojix-7.0.0.drv; live wrapper derivation is xn706di...-lojix-6.0.0.drv | The attempted client and daemon have different major package versions. This supports, but does not prove, a wire-compatibility cause. |
| Current source | CriomOS/modules/nixos/lojix.nix:28-31 forms the daemon command from the pinned package; checks/lojix-nexus-start/default.nix:39-50 requires both sockets and invokes a matching package client. | The source contract expects daemon and clients to be supplied by one package generation. |
| Current source | CriomOS/flake.nix:295-302 projects homeConfigurations.<user>.activationPackage from nixosConfigurations.target.config.home-manager.users. | The required Home output is the embedded target projection, not a standalone CriomOS-home generation. |
| Current guidance | CriomOS/docs/GUIDELINES.md:266-283 names nixosConfigurations.target as the public system surface and lojix-bootstrap with one BootstrapRun as the maintained bootstrap interface. UPGRADES.md:102,160 rejects standalone Home activation. | A direct profile mutation or arbitrary home-manager switch is not an evidenced fallback. |
| Bootstrap preparation | nix build --no-link --print-out-paths .#lojix-bootstrap produced /nix/store/l5rygv4zraxa2ag4jb40n6wpppyps1wz-lojix-bootstrap. | The compatible bootstrap executable is built locally. No BootstrapRun was issued. |
| Nix configuration | nix show-config reports builders = @/etc/nix/machines, max-jobs = 0; /etc/nix/machines selects ssh-ng://nix-ssh@prometheus.goldragon.criome. | Ordinary Nix evaluation dispatches builds to Prometheus. This is distinct from Lojix coordinator and target behavior. |
| Earlier Flow 0.5 build receipt | Nix reported building Flow derivations on ssh-ng://nix-ssh@prometheus.goldragon.criome, then copied the final output back. | This proves physical remote Nix builder execution on Prometheus for that closure, not that Lojix deployments build there. |

## Separate failures

- An early request used /run/lojix/owner.sock, which did not exist. That is a wrong-socket failure, not evidence against /run/lojix/meta.sock.
- An early nix run invocation expected /bin/lojix; the package exports lojix-meta. That is an executable-selection failure.
- The previous c4 Horizon decoder could not represent OpenCodeTesting. The later compatible a67 source was reported to parse the unchanged EB artifact and preserve the Horizon user-environment shape; this report does not independently re-run that producer test.
- Historical daemon journal entries at 14:40:40 -06:00 show a Lojix build pipeline attempting large model-file downloads from Prometheus and ending terminally after cache timeouts/partial transfers. They are evidence of a prior Lojix pipeline, not evidence that an activation job is currently accepted or that all Lojix builds occur on Ouranos.

## Causal assessment

| Claim | Status |
| --- | --- |
| The attempted 7.0 client reached the live meta socket. | Observed from its signal-frame EOF, together with socket/daemon inspection. |
| The live daemon rejected structural wire conversion. | Observed in its journal. |
| The 7.0 client versus 6.0 daemon major-version difference caused the EOF. | Hypothesis supported by the facts above; no replay against a matched live daemon has been run. |
| A Lojix activation job exists. | False for the recorded matched attempt: no job ID or acceptance receipt exists. |
| The exact full request argv/body is available. | Unknown/unavailable: it was not retained in a run file. Canonical request text must not be relabeled as an observed argv. |
| Lojix only builds on Ouranos. | Unverified. Current Nix dispatcher demonstrably builds ordinary closures on Prometheus; the historical Lojix journal shows a pipeline on Ouranos fetching from Prometheus. These are different layers. |
| Generation 54 is a successful Lojix generation without ledger state. | Relayed claim only; no local generation-54/ledger receipt was located in this bounded inspection. |

## Next supported crossing

Wait for Mind's final marker-capable Flow publication before any consumer pin or activation. Then use a coherent source revision that includes the embedded target Home projection, compatible Horizon-capable Lojix package, and declarative Claude bypass source. The maintained bootstrap executable is available, but no exact, source-proven BootstrapRun payload for the intended user-environment crossing has yet been retained. Do not synthesize one from older request forms, mutate the Home profile directly, or start another Lojix controller. Any next deployment command must retain its literal argv, stdout/stderr, exit status, and resulting job ID before an activation claim.

