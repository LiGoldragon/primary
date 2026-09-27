
# Power-failure recovery state, 2026-09-26 local

The living directed recovery of at least nine remotely accessible flows, fresh context, prior-work handoff, the newer Flow Nexus, and a reply from every seat. This main flow is Mind Sol 56ae53, hosted in Herdr default. Direct living words are preserved in log.md and vision records.

Nine distinct seats have native Herdr sessions and observed replies: Mind Sol 56ae53, Mind Astra 6fe957, Mind Luna 139366; Field Astra 22e12b, Field Sol 9ac67c, Field Luna 184bd8; Psyche Fable 8904b1, Opus dc53b4, Sonnet 38f337. The independently landed evidence roster is flows/56ae53/receipts/roster.md. Incomplete predecessor Field Luna 19ff9f remains unbound and untouched.

Operational distinctions: all nine have live Herdr agents. Astra's imported Flow 0.12.2 row is Pending/RegisteredUnconfirmed by design, although a prior delegated Message task was Presented and answered in its native pane. Fable, Opus, and Sonnet are foreground Claude sessions: Flow rows are Active with Herdr available and Message delivery/replies, while Claude daemon-owned endpoints are Unavailable because the old daemon roster/control socket cannot adopt these foreground processes. Do not fabricate confirmation or daemon ownership.

Flow-next 0.17.1 and Message-next 0.17.0 ran side by side in a test activation. A valid Fable Start was rejected before reservation because Claude first-line composition was 1,125 UTF-16 units against a fixed 800 limit. The source already has durable NativeLaunchIntent and PromptDeliveryIntent; a Terra worker is preparing a safe cap repair. The host test switch failed at tailnet enrollment because tailscaled kept stale CA trust; a scoped restart restored tailscaled. A declarative CA restart-trigger source was pushed and evaluated, but permanent host deployment is blocked because Prometheus is offline on both tailnet and Yggdrasil, so the required remote-only Nix build failed. The living has been asked to check Prometheus power/network. Lojix test deployment #50 remains an ambiguous Copying row and must not be retried.

Herdr default remote attach through Ouranos SSH/Tailscale is verified from the host namespace, not independently from the living's laptop. Exact laptop command and limits are in flows/56ae53/receipts/remote-access.md. Preserve all predecessor sessions and launched seats while resolving remaining infrastructure work.

## Release and access update, 2026-09-26 local

The roster receipt landed on Primary main at 3298f960; this summary's first version landed at 3d5a4517. A profile-only Nix reconciliation aligned Home Manager profile/current-home/new-home at rooted generation 1033 without restarting services. Flow-next 0.17.1 and Message-next 0.17.0 remain enabled and active as user services; they start after user login (linger is disabled), not before login. Existing stable Flow/Message and all nine Herdr sessions retained their processes.

Flow 0.17.3 Claude pasted-prompt startup repair passed independent review and the full workspace test suite. Flow main and tag flow-0.17.3 both point to immutable Git commit 0b512ee0b6681b1925fee7b6435aa7c2eac26bfb, remotely read back. Home staging branch home/flow-0173-stage-56ae53 at b7030941b6a043b1229c02c351907940c40b598e pins that source; Nix eval and flake check --no-build passed. Home main and the host were not changed to 0.17.3.

Prometheus remains offline/unreachable from Ouranos over both Yggdrasil and Tailnet. SSH, Nix cache HTTP, nix store ping, and ICMP timed out; tailnet marks the peer offline. The required remote-only build cannot run, so no Flow 0.17.3 Home activation or new host Lojix cycle is authorized yet. Physical power or entire-network status requires the living's check. Independent laptop remote attach is likewise unverified; instructions and same-host SSH proof are in the remote-access receipt.

Do not claim all Flow endpoints Available: Astra's imported row is Pending by Flow 0.12.2 design; the foreground Psyche Claude endpoints are Unavailable without daemon-owned roster/control sockets. Herdr and Message interactions were observed for the nine seats. Do not fabricate endpoint or registry confirmation. All nine seats and incomplete predecessor 19ff9f remain preserved.
