# Zeus psyche acquisition

This is an acquisition of the written psyche for the requested explanation. It does not verify the live Zeus host and does not authorize an update.

## Current request

The latest direct user request says:

> I want to update host zeus in my cluster. see if you can explain what that looks like first.

Provenance: canonical transcript `/home/li/.codex/sessions/2026/08/22/rollout-2026-08-22T23-00-27-01a02b46-5e97-7632-8db5-780391553085.jsonl`, physical lines 9–10, timestamp `2026-08-22T21:02:46.852Z` (`23:02:46.852+02:00`), session `01a02b46-5e97-7632-8db5-780391553085`.

## What the written psyche settles

The older Zeus recovery request establishes the desired outcome and the initial caution: the host is a partner's workstation, the OS and user environment must be brought into sync, and the target should reach the latest version. Its exact warning is: “Don't trust anything. Don't assume anything. Be careful where you step.” It also says, “So then once we got all that lined up, we need to redeploy Zeus on the latest version.” Provenance: canonical transcript session `019fe121`, physical line 9, timestamp `2026-08-08T11:37:36.634Z`; preserved in `flows/019fe121/vision/hostEnvironmentRecovery.md`.

The later recovery ruling narrows the permitted repair shape: “dont do hot fixes” and “use the nix user env only, or OS redeploy.” Provenance: canonical transcript session `01a01a93`, physical lines 1878 and 1894, timestamps `2026-08-19T18:42:58.998Z` and `2026-08-19T18:43:15.438Z`; preserved in `flows/01a01a93/vision/hostEnvironmentRecovery.md`.

The deployment interface is settled at the vision level: “The interface is lojix and meta-lojix CLI only.” The psyche also says, “CLIs cannot accept any other type of argument than the typed input object.” Provenance: `psyche-raw/Vision/setupIndependentInterfaces.md`, entries dated `2026-08-14`.

The host-specific workaround must not become the design: “nothing to do with bird, this is a criomos-home fix, universal. nothing in this should hardwire bird or zeus anywhere.” Provenance: `flows/019fe641/vision/hostEnvironmentRecovery.md`, timestamp `2026-08-09T13:00:32.409Z`.

The Lojix ownership/order record says: “it should only be in OS”; “I dont care about any past lojix database”; and “the system has to be redeployed with only the newer Lojix daemon, nothing else. And then we can use Lojix to deploy the upgrade.” Provenance: `psyche-raw/Vision/lojixOwnership.md`, timestamps `2026-08-13T15:40:20+02:00`, `2026-08-13T23:32:19+02:00`, and `2026-08-14T09:06+02:00`.

There is a later authority ruling: “If I say deploy just deploy it.” Provenance: canonical transcript session `01a01a93`, physical line 2213, timestamp `2026-08-19T21:03:41.822Z`; preserved in `flows/01a01a93/vision/hostEnvironmentRecovery.md`.

## Tensions and unknowns to return

1. The current request explicitly asks for an explanation first. The later “If I say deploy just deploy it” ruling removes a repeated transport-confirmation question from a direct deploy instruction, but it does not turn this explanation request into an instruction to mutate Zeus. Deployment remains pending.

2. The 2026-08-08 record tolerates a “hacky way” and mentions root SSH/manual user-environment reload, while the 2026-08-19 record rules out hot fixes and names only the Nix user environment or an OS redeploy. The later ruling should govern; whether a manual reload is still needed after a lawful declarative deployment is an implementation fact to verify, not a psyche ruling.

3. The 2026-08-08 transcript contains speech-to-text uncertainty around host names (“Uranus”, “Odanos”, and other variants) and project names (“KareemOS”, “CREAMOS”). The psyche explicitly says to use cluster data for the name. The authoritative Zeus node identity, selected system/home configurations, and transport must therefore be read from current cluster/manifests before constructing a request.

4. The psyche says deployment uses `lojix` and `meta-lojix` and typed NOTA/DOTOS input, but these records do not settle the exact current request shape, transport fields, deployment target selector, or observation/completion proof for Zeus.

5. “Make sure [OS] and [Home] are in sync” is an outcome, not proof that both should be deployed in one request. The current target surface—OS, user environment, or both—and their lawful order remain to be established from current code and cluster state.

6. “That should be set using cluster data in criomos-home” settles the source of setup-sensitive values such as the SSH keygrip, but does not by itself prove the current cluster data is coherent. Current data needs a read-only witness.

7. The 2026-08-08 request says Lojix “might not work properly,” and the 2026-08-13 record requires the newer Lojix daemon before using Lojix for the upgrade. Whether Zeus currently has a compatible daemon and store is a live-state question, not settled by the psyche records.

8. The broad 2026-08-08 request included VS Code/Codex/Cloud extension repair and writable JSON surgery. The current request only names a host update and asks for an explanation. Do not silently widen this update to extension surgery without a new explicit request.

## Sources

- Canonical current request: `/home/li/.codex/sessions/2026/08/22/rollout-2026-08-22T23-00-27-01a02b46-5e97-7632-8db5-780391553085.jsonl`, physical lines 9–10, session `01a02b46-5e97-7632-8db5-780391553085`.
- Canonical Zeus recovery request: `/home/li/.codex/sessions/2026/08/08/rollout-2026-08-08T13-28-29-019fe121-b1ea-7350-922b-826d0ce83a37.jsonl`, physical lines 9–10, session `019fe121-b1ea-7350-922b-826d0ce83a37`.
- Canonical no-hot-fix and deployment-surface rulings: `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T17-11-18-01a01a93-a27d-7e73-944a-4501e67ce65d.jsonl`, physical lines 1878–1879 and 1894–1895; direct-deploy ruling at line 2213.
- Raw psyche records: `psyche-raw/Vision/lojixOwnership.md`, `psyche-raw/Vision/setupIndependentInterfaces.md`.
- Prior flow psyche records: `flows/019fe121/vision/hostEnvironmentRecovery.md`, `flows/019fe641/vision/hostEnvironmentRecovery.md`, `flows/01a01a93/vision/hostEnvironmentRecovery.md`.
- This flow's verbatim acquisition: `flows/01a02b46/vision/zeusUpdate.md`.
