# Prometheus-absence hotfix inventory

Observed 2026-09-25; read-only. This distinguishes a live override from build-command flags and generated configuration.

| Item | Owner/provenance | Introduced or last witnessed change | Current effect | Declarative source? | Revert or declare boundary |
|---|---|---|---|---|---|
| Flow user-unit override | Field deployment lineage (activation receipts) | 2026-09-25 20:52:09 -0600 | **Active:** user Flow service executes local Flow 0.12.2. Generated base unit still selects 0.6.0. | No; user drop-in is imperative. | Field deployment owner coordinates rollback to a retained verified override/profile, or OS/Flow owner lands a declarative package/unit selection. |
| Local Flow builds, 0.10.5 through 0.12.2 | e51411 then 38de5b / Field deployment receipts | 0.12.2 activation at 2026-09-25 20:52:09 -0600 | Builder-disabled/cache-only and some max-jobs flags were command-scoped. Retained closures are not themselves live; the 0.12.2 closure is live only through the override above. | No invocation policy source witnessed. | Deployment/OS owner decides whether to declare a supported build policy; do not treat old closures as an active configuration. |
| User Nix configuration | Unknown pre-existing owner | 2026-09-12 05:41:22 -0600 | Persistent for user Nix invocations: job/builder/timeout/cache preferences differ from system defaults. | No authored declarative source witnessed. | Unknown configuration owner, with OS owner for any declarative replacement. Do not expose or copy credentials embedded in this file. |
| System Nix configuration and builder list | Operating-system generation | 2026-09-24 18:43:06 -0600 | Generated system defaults include a Prometheus remote builder; daemon-side defaults differ from user configuration. | Yes: generated system configuration. | Operating-system owner declares or reverts it; not a Field hotfix. |
| Lojix generated Ouranos inputs | Lojix materialization/producer owner | Complete-host observed Sep 12; user-environment observed Sep 24 | Present generated runtime inputs. Older materialization is implicated in the missing-hardware evaluation mismatch; presence does not prove a current coherent activation request. | Generated products, not the authoring source. | Current producer/materialization-closure owner must publish a coherent fresh request and evaluate it; do not remove or overwrite live inputs. |
| Local Flow/Nix wrapper | — | — | No relevant executable wrapper was found in the targeted user wrapper directories. | — | No action. |

## Operational boundary (relayed policy)

Fable da88cf’s current night-operations directive supersedes the earlier fallback rule: do not run Nix builds/checks or cargo/bb/clojure substitutes on Ouranos, even after remote failure; report the exact remote error to Fable. Do not use local builder-disabling or increased-job flags. Fable owns Headscale/Tailscale repair and tonight integration; Field performs no mutation without that owner’s exact repair slice.

## Sources

- User unit effective state and drop-in: `systemctl --user show/cat flow-nexus.service`; active service read at 2026-09-25 20:52:09 CST.
- Build and activation provenance: `flows/e51411/log.md`; `flows/38de5b/receipts/flow-0.10.7.md`, `flow-0.12.1-store.md`, and `flow-0.12.2-codex-endpoint.md`; `flows/b7da5d/receipts/flow-0107-live-activation.md`, `flow-0121-live-activation.md`, and `flow-0122-live-activation.md`.
- Configuration and timestamps: `/home/li/.config/nix/nix.conf`, `/etc/nix/nix.conf`, and `/etc/nix/machines` (content summarized without credentials).
- Generated-input presence: targeted metadata beneath `/var/lib/lojix/generated-inputs/goldragon/ouranos`.

## Evidence gaps

The author of the persistent user Nix configuration, its intended declarative source, and a current coherent Ouranos Lojix proposal/transport/selector/pin were not witnessed. No live change, build, restart, or activation was performed.
