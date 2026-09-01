# ChatGPT Desktop startup realization

The flow is continuing the ChatGPT Desktop startup defect reported by the psyche: the Electron application cannot locate the Codex CLI binary and asks for `CODEX_CLI_PATH` or `bin/codex` in its resources.

The psyche identified flow `01a05487` as the relevant memory anchor.

Remembered: `01a05487` — depth 1. It landed and remotely built the ChatGPT package/source repair, but explicitly left activation and a signed-in live GUI smoke unclaimed; its continuing constraint was not to disturb the live Codex service while remote access was required.

Remembered: `01a05487` — depth 2. Its last response claimed that Option 2 “uses ChatGPT Desktop’s native shared-daemon transport,” while explicitly saying no live activation or authenticated GUI session was attempted. The present signed-in startup disconfirms the first claim: current ChatGPT `26.825.51511` resolves no CLI, records `hostId=local` and `transport=stdio`, and fails before initialization even though the managed Codex service and socket are healthy.

Settled diagnosis: the wrapper sets local-daemon mode while unsetting `CODEX_CLI_PATH`, the package omits every recognized `codex` resource, and the ASAR requires an executable candidate before it can enter the shared-daemon path. The static contract was inverted: it asserted the candidate's absence and therefore passed over the real startup defect. Current ASAR control flow requires `resources/codex` for a `codex app-server daemon version` preflight, then selects shared WebSocket transport only while `CODEX_CLI_PATH` stays blank; setting that variable would select stdio.

Landed repair: CriomOS-home `b04edb442f52` (`Restore ChatGPT shared-daemon resolver candidate`) adds `resources/codex` backed by the managed package while keeping override variables blank. Before the patch, the focused remote contract failed on the missing candidate. After it, the focused desktop contract and behavioral `codex-remote-control-vm` service/socket/restart gate passed remotely. The attempted daemon RPC in the pure desktop sandbox was removed as a test-design correction because that socket belongs to the VM/service boundary. The commit is pushed, the worktree is clean, and Locks 458/459 were released.

Landed consumer: CriomOS `69a946b1d0e522d6ad04162a497992641c87bcfb` pins the pushed producer exactly; only `flake.nix` and `flake.lock` changed, the immutable remote flake resolves the producer revision/hash, the commit is pushed, the worktree is clean, and Lock 460 was released.

Correction approved: authored Curriculum Lojix says a deployment proposal must be a `.dotos` file, but pinned Lojix `34a8e9c2` requires the basename `proposal.datom`, parses `Text<ClusterProposal>`, and the canonical cluster source is `goldragon/proposal.datom`; the stale sentence stopped the non-activating Realize route. The psyche approved the exact replacement with `proposal.datom`; authored edit, regeneration, and fresh-flow test are in progress.

Lojix correction landed: Curriculum `b71104d1` changes only the approved proposal filename; primary `2b896f24` regenerates only the Lojix outputs; generation/check returned `Generated.{37 27}` / `Checked.{37 27}`. A fresh flow selected the canonical `proposal.datom` and constructed the correct Ouranos request.

Realized and activated: Lojix deployments 123 (`Realize`) and 124 (`ActivateNow`) both completed `Succeeded` for CriomOS `69a946b1d0e522d6ad04162a497992641c87bcfb` on `goldragon/ouranos/li`. The active profile contains the repaired ChatGPT package. The persistent Codex owner remained PID 4013983 with the same start time/socket and existing clients through activation.

Startup witnessed: fresh ChatGPT PID 837740 opened a Niri window, emitted no missing-binary error, completed its app-server initialize handshake with `transportKind=websocket`, and reached connected state through the sole pre-existing persistent Codex owner; no second app-server owner appeared. The psyche visually confirmed “chatgpt works now.”

Open correction proposal: authored Orchestrate still shows `Release.{<lock-id>}` although the live/schema-tested scalar form is `Release.<lock-id>`. A read-only audit accidentally reached the live wrapper and released completed lock 461; no lock remains. Exact skill edit awaits psyche approval.
