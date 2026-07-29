# Lojix, Bird VSCodium, and Li Home-owner recovery — 2026-07-29

## Scope and evidentiary standard

This is the durable incident synopsis requested after the deployment and recovery work. It separates witnessed facts from inferences and does not reproduce secrets or content-addressed Nix paths. Timestamps and revisions are those observed during the work; absent a retained command transcript, a stated causal link is an inference rather than a claim of proof.

The psyche's rulings were: preserve the ordinary, Nix-owned command path; preserve direct Claude Code and Codex CLI use; do not signal Niri or perform a full system switch for a Home repair; deploy only authoritative generated inputs; do not allow a stale or manual profile/overlay to become the owner; retain the existing Li VSCodium GUI if possible; and carry recovery to a verified owner state rather than treating a successful build as completion.

Ownership boundaries adopted in the work:

- CriomOS-home owns Home packages, files, VSCodium lifecycle behavior, and Home Manager service declarations.
- CriomOS owns the integration and pins an exact CriomOS-home revision before deployment.
- Lojix owns materializing target inputs and deployment orchestration; it was inspected and reconciled, not bypassed as a source of truth.
- Nix profiles own normal executable resolution. Per-user overlays and unmanaged executable identities are not alternate owners.
- Agent Intercom owns its named operational tools (`coi`, `cci`, MCP and fleet utilities), not ordinary `codex` or `claude` commands.

## Chronology, failures, and corrections

1. The initial Bird VSCodium/agent recovery exposed a lifecycle script that called `cmp` from the Coreutils path. `cmp` is supplied by Diffutils. The current owner source was corrected to substitute and retain the Diffutils closure. The focused lifecycle check passed and the repaired generation was deployed.
2. Earlier validation was too shallow: it accepted an underlying binary or absolute package path while the actual interactive shell could resolve a different profile entry or wrapper. The recovery subsequently used ordinary interactive/login zsh `type`, `whence`, PATH, profile-chain, target, and controlled invocation evidence.
3. A read-like dead-path inspection (`nix-store --gc --print-dead`) pruned stale automatic GC roots. That was a control failure because root-pruning had not been authorized at that point. It did not remove store paths; later deep GC was explicitly authorized.
4. A broad cleanup instinct was rejected after the fact: Bird overlays were inventoried and only verified obsolete ownership was removed. There was no blanket Bird overlay cleanup.
5. Deep cleanup then ran under explicit authority. It retained system generation 60, Bird Home Manager generation 30, Bird profile generation 200, Li Home Manager generation 28, and Li profile generation 264, plus explicit Bird lifecycle roots for Claude 2.1.220 and OpenAI ChatGPT 26.5721.30844. The collection removed 26,338 paths and released about 51.2 GiB. Post-GC free space was 74,204,823,552 bytes (85%); inode availability was 28,790,218. These are witnessed figures, not an estimate.
6. Bird was rebuilt from the current source and checked after GC. Ordinary commands were Nix-owned, Claude was 2.1.220, Codex was 0.146.0, the VSCodium registry/extension witness was pinned and immutable, and no overlay remained. A fresh GUI was healthy (observed PID 175510 at the time); Agent Intercom was inactive/not found on Bird, as expected for that owner profile.
7. Li's first exact Home evaluation against Ouranos inputs recursed. Trace identified an eager use of `pkgs.stdenv.hostPlatform.system` in the Agent Intercom graphical guard during Home module merge. A first replacement with `builtins.currentSystem` was incorrect in this pure evaluator. The durable fix was an explicit `homeSystem` special argument in standalone Home construction and in CriomOS's NixOS Home integration.
8. The exact Li candidate then revealed hidden package ownership collisions: direct Codex versus Agent Intercom's `bin/codex`, then direct Codex's `bin/codex-raw` versus Intercom's alias. The final Home module publishes a filtered Intercom runtime with `codex`, `codex-raw`, `claude`, and `claude-raw` aliases removed. Direct pinned CLI packages supply normal commands and raw recovery commands. This also removed the third-party wrapper's misleading `$HOME/.local/bin/codex` executable identity by exposing the Nix-owned raw binary as normal `codex`.
9. CriomOS was advanced and locked repeatedly while the repair converged. The final deployed owner build was from CriomOS `46373e0e43d2eee28e4f6e58f1cb44abb367dfc9`, pinning CriomOS-home `44c2995c9d551a3e3b028dff9d347863d792c40c`. Earlier intermediate pins are historical only and must not be deployed.
10. The exact Li activation package built successfully against authoritative Ouranos generated user-environment `system` and `horizon` inputs. It was applied through Li's Home Manager profile only, without a system switch and without signalling Niri.

## Lojix incident and transport state

Lojix had a broader operational history in this incident: schema migration/corruption handling, a fresh-store path, marker-gating, a deadlocked transport condition, and lost job history. The durable conclusion is not that history was recovered: it was not. Fresh-store and marker-gate actions allowed current work to proceed, but provenance for lost/deadlocked jobs cannot be reconstructed from this audit alone.

At closure, `lojix-daemon.service` on Ouranos was enabled and active. Its observed pre-start configuration write succeeded and the daemon had been running since 15:16:32 CEST. This proves the daemon was live at inspection time; it does not prove that all historical jobs, transports, or schema records were preserved.

Permanent risk: Lojix needs durable job provenance, explicit timeout ownership, and a resumable transport protocol. A marker alone should never be treated as proof of completed deployment semantics. Recovery state must distinguish fresh initialization, successfully migrated state, failed/abandoned job state, and idempotent resume state.

## Li owner final state and caveats

The official npm stable channel was queried: `@openai/codex` `latest` was 0.146.0; 0.147.0 was alpha. No speculative Codex upgrade was made.

Post-activation interactive/login zsh verified:

- `codex`, `claude`, and `codium` first resolve through `~/.nix-profile/bin`; the state-profile entry is the compatibility second hit.
- Codex is 0.146.0 and `codex --sandbox danger-full-access --ask-for-approval never --help` succeeds without invoking an Intercom socket or unmanaged user executable identity.
- Claude Code is 2.1.220.
- Codium reports 1.112.01907 and no longer emits the missing-`cmp` warning.
- Existing Li VSCodium PID 66741 survived activation.
- The final candidate had one direct provider each for Codex and Claude, and no profile overlay was introduced.

Activation did have an important gate exception. Static inspection found only Home Manager's user-daemon reload, but actual `reloadSystemd` started declared units: `agent-intercom-codex-bridge`, `codex-remote-control`, `criomos-ui-priority`, `spirit-daemon`, and `spirit-judge`. Therefore a claim of "zero unit actions" would be false. `agent-intercom-codex-bridge` and `codex-remote-control` were active after activation. `spirit-judge.service` was already degraded/failed before the activation and remained failed. This is the active residual operational risk.

The Home activation emitted a removable-profile message while creating the new Home Manager profile generation. That is expected profile-set behavior, not a user-file removal. The activation completed successfully. The report does not claim zero profile transition effects; it claims no full system switch and no observed VSCodium process loss.

## Bird, Zeus, and recovery evidence

Bird's owner source series included commits `4901de965e32` (recover missing VSCodium state), `6387d78494d6` (converge current declared link), `f3dba006dcc9` (Diffutils lifecycle correction), and `a08e4dda3c74` (an intermediate invalid `currentSystem` attempt superseded by later source). The direct Home bypass used only for diagnosis/build was not adopted as the owner deployment path; final owner behavior remained source/pin driven.

Bird ended with a healthy GUI, required extensions/registry witness, direct CLIs, and no unwanted Intercom service. There were no active GC/copy/import operations after the cleanup checks.

Zeus reboot and disk evidence were captured during the wider recovery. This report preserves the ruling, not a new assertion of unrecorded metrics: do not roll Zeus back merely to recreate old state. The deep generation deletion/GC was deliberate and separately authorized; recovery now depends on declared sources and retained roots, not rollback of Zeus.

Archived backups and discarded stores must be treated as forensic inputs, not deployment owners. Some historical stores were intentionally collected; lost Lojix history is not recoverable merely because a surviving closure exists.

## Design decisions that now govern future work

- Before every CriomOS deployment, update and lock the CriomOS-home input to current CriomOS-home main, then build/deploy only that pinned revision. This exact rule was added to CriomOS `AGENTS.md`.
- Horizon capabilities remain opt-in. Agent Intercom graphical behavior must be driven by declared capability plus an explicitly supplied target platform, never eager module-time package evaluation.
- VSCodium lifecycle ownership belongs in declared Home source. Hexis structured transforms/configuration must be treated as activation-owned behavior and tested at the real command path, not by inspecting only underlying binaries.
- Agent Intercom operational utilities are distinct from normal CLI ownership. Do not reintroduce `codex`/`claude` aliases into the Home package union.
- A Home activation service-action gate must inspect the generated activation's effective systemd behavior, not merely grep for start/stop commands. Declared `WantedBy` services can be started by reload processing.
- No rollback is authorized on Zeus merely to recover pre-GC generations. New recovery must remain reproducible from pushed, pinned configuration and explicitly retained roots.

## Current non-mutating verification

These commands are evidence-oriented and do not deploy or mutate state:

```sh
runuser --login --command 'zsh -ilc "type -a codex claude codium; codex --version; claude --version; codium --version"' li
kill -0 66741
systemctl --machine=li@.host --user is-active agent-intercom-codex-bridge.service codex-remote-control.service spirit-judge.service
systemctl is-active lojix-daemon
```

Expected current evidence is direct Nix-owned command resolution, Codex 0.146.0, Claude 2.1.220, Codium 1.112.01907 without the `cmp` warning, live PID 66741 (unless the user has since closed/restarted it), active Intercom bridge/remote-control, failed Spirit Judge, and active Lojix daemon. Process IDs are inherently transient.

## Residual risks requiring attention

1. `spirit-judge.service` remains failed; its cause and restart policy require a separate, evidence-led incident.
2. Home Manager's reload can start declared services. Future narrow activations need an explicit expected-unit set and a pre/post check.
3. Lojix's prior schema/transport corruption and lost job history leave an audit/provenance gap until resumable, timeout-bounded jobs are implemented.
4. The upstream Codex Nix package may change its wrapper behavior in a future pin. Keep the direct-identity assertion in the focused Home check.

## 2026-07-29 bounded Lojix transport repair

### Completed, witnessed work

Lojix `0.11.0` was pushed through commits `250c1e38`, `d0f7e83e`, and `15e25e0`. Its deploy pipeline now evaluates and builds the exact immutable output locally, copies that output to the target, then uses the existing root-mediated target-user profile and activation path. It never evaluates a deploy flake through an SSH Nix store. Every Nix, SSH, and activation effect now has a configured wall-clock bound; the production default is 2700 seconds. The runner starts a session process group, terminates it on expiry, escalates if necessary, waits for it, and reports a durable terminal rejection.

Focused Rust tests cover the local eval/build, exact copy/profile/activation order, copy and activation failures, and a hung descendant process. The full Lojix Rust suite, its Nix sandbox test, and the CriomOS daemon-configuration round-trip check passed. The latter also corrected a stale assertion that expected shell quotes absent from the generated static migration script. No deployment-job schema or provenance migration was added: existing terminal failure persistence and source-revision records remain, while proposal-source snapshot and content provenance remain a known gap.

CriomOS `0683d00e` pins Lojix `15e25e0`. It writes the bounded-effect value into the daemon startup archive and includes `setsid` in the service path. The exact pushed Ouranos system, built with all four authoritative generated full-OS inputs, completed successfully; its NAR hash was `sha256-EPd6ER6/HVdUW2xbPd9EwdXDlnkRud/1+k1JwCjhReU=`. The persistent system profile was set and switched through `root@localhost`. Afterwards, `lojix-daemon.service` was active and enabled, both sockets existed, its deployed unit carried Lojix `0.11.0`, and an ordinary `ByNode` query succeeded.

### Owner and Bird gates

Before the system switch, both Li and Bird resolved direct Codex `0.146.0` and Claude `2.1.220`; Codium reported `1.112.01907`, with `anthropic.claude-code@2.1.220` and `openai.chatgpt@26.5721.30844`. Neither account had the checked user overlay directory. Bird's Intercom units were inactive. After the switch, Li retained those package and VSIX versions and no overlay. Li's previously active Intercom units were then inactive and no longer installed. The authoritative generated Ouranos Horizon contains no Agent Intercom capability; that is consistent with the absence, but the observation alone does not establish the full causal mechanism.

The configured Zeus endpoint was initially reachable for the read-only Bird gate, then became unreachable before the required smoke. Authoritative DNS resolution and the local Yggdrasil route were correct while TCP port 22 and verbose SSH timed out during connection establishment. Prometheus was reachable over the same local Yggdrasil fabric but also could not reach Zeus over ICMP or TCP port 22. The authoritative Horizon has no Zeus LAN/link-local address, WireGuard identity, or ProxyJump endpoint, so no identity-safe alternate route was used. The cause of that outage is unknown.

When TCP and identity-safe SSH later recovered, Bird again passed the command, VSIX, overlay, and inactive-Intercom pre-gates. Exactly one current-environment `ActivateNow` request was admitted. Its durable phase observation reached `Building`; its copy then failed at the target signature gate. The daemon emitted a terminal `DeployRejected` result for `CopyClosure`: the target refused a copied closure lacking a signature by a trusted key. No second request was sent. The ordinary event-log query still displayed `Building` as its last phase event after that rejection, so that query alone must not be treated as proof of a terminal success or failure.

Post-rejection read-only checks found the Bird profile still resolving to its existing generation, and the direct command/extension/overlay and inactive-Intercom gates remained unchanged. The daemon was active and enabled. The copy failed before profile replacement or activation; that ordering is evidence against an activation, but the report does not claim an unavailable before/after profile digest comparison.

Read-only declarative and runtime Nix inspection established a specific, unresolved signing boundary. Zeus requires signatures and currently trusts the key name `zeus.goldragon.criome`; Zeus and Ouranos have no configured `secret-key-files`. Their configured cache is `nix.prometheus.goldragon.criome`. Prometheus's active cache signs as `prometheus.goldragon.criome`, which Zeus does not trust, and its root Nix configuration likewise declares no `secret-key-files`. No declared root signing helper for the Zeus-trusted key was found. No key bytes were read, no trust or signature requirement was changed, and no unsigned-copy bypass was used. A psyche decision is required before adding or changing any signing/trust capability; without it, the one-shot smoke cannot reach `Current`.

## 2026-07-30 capture-bridge removal and system redeploy

Psyche authority covered disruptive declarative removal and redeployment on
both hosts. CriomOS-home `653ade70` removes the Home-only capture-card
virtual-camera module, its user service and bridge package, its aggregate
import, and its prior positive check. Its focused absence check evaluates and
builds representative large-edge and ordinary profile fixtures with no bridge
unit or package; it also checks that the retired module and check roots are not
present. CriomOS `3938a923` pins that exact Home revision in both `flake.nix`
and `flake.lock`.

Exact pushed full-OS closures were built from that CriomOS revision using the
authoritative owner-generated inputs: Ouranos's local full-OS set and Zeus's
authoritative full-OS set held by the owner on Ouranos. Before activation,
each closure contained Claude 2.1.220, Codex 0.146.0, the pinned OpenAI VSIX
26.5721.30844, and VSCodium; neither contained the retired bridge or an
undeclared Intercom bridge/remote-control unit. Both persistent system
profiles were set to their exact closures and switched declaratively. On each
host, the current and persistent system references matched the activated
closure afterwards.

Read-only production verification found the retired unit not found in the
system manager or in each already-running relevant user manager. It found no
FFmpeg process using either former bridge video device, and no bridge package,
script, or reference in the active system or Home Manager generations. No
v4l2loopback device was present on either host; no device was removed. Ordinary
Li and Bird login shells resolved `codium`, `claude`, and `codex` to Nix-owned
executables; both accounts reported the required Claude and Codex versions and
the expected Claude Code and OpenAI ChatGPT extensions. The prior user-local
Codium overlay was absent on both accounts. These are observed deployment
facts; they do not establish a cause for the earlier capture process.
