# Desktop to persistent Codex removal audit

## Outcome

The originating `cf0ed9` thread requested a stock rollback, then superseded that working instruction with a request to stop all child flows and summarize. Its final model response says the rollback did not happen, Desktop remained customized, ordinary new-chat still failed, and the last attempted sanitizer remained dirty, non-green, uncommitted, and undeployed. A fresh repository and installed-state witness now independently confirms that the deployed Desktop remains customized and the wider candidate remains dirty and undeployed.

The provisional clean removal boundary is not the entire persistent Codex topology. The persistent owner and terminal/phone routing existed independently of Desktop. If the destination is stock Desktop behavior while retaining those capabilities, the removal set is Desktop-specific transport forcing and application-bundle mutation, followed by an immutable consumer update and deployment. Removing the persistent owner is a separate product decision.

This report is an inventory only. It changes no product source, declarative system source, deployment, service, process, configuration, cache, database, or conversation.

## Psyche boundary

Earlier Vision said:

> I dont want to start a nexus for this; we just need the server running for codex and claude, and the desktop apps using it locally.

The current flow records the later statement:

> I am no longer interested in heavily modifying those applications to achieve better functionality.

Flow `cf0ed9` also records:

> The defect is on openai for lacking the feature I want

The later statements strongly direct this flow away from continuing a brittle succession of private-bundle patches. They do not by themselves say whether the independent persistent Codex owner should be removed, and this investigation does not authorize the rollback.

## Current state witnessed

The currently selected system source pins user-environment revision `90a12633cc60148b62bc47fd44957e6165727094`. Its active generation contains ChatGPT `26.831.21537`, Codex `0.152.1`, the local-daemon wrapper variables, the shared `resources/codex` link, the patched `getConfigOverrides`, and remaining private `codex_app` producer/fallback material.

The user-environment working copy is dirty beyond that selected revision: it modifies `owned-agents/chatgpt/patch-asar.py` and `checks/desktop-app-support/default.nix` and contains an untracked Python bytecode artifact. Those wider removal/sanitization changes are not selected or deployed.

The persistent service is active and listening. ChatGPT itself was not running during the snapshot, so the witness does not claim a current Desktop connection, new-chat failure, or resumed-thread result. No legacy TCP server, custom ChatGPT user service, or second ChatGPT-owned app-server was present.

## Implementations and attempts

### Historical predecessors already deleted

The source history contains three earlier lineages that are no longer current removal work:

- Commit `ed338a1ab2aa` introduced an Agent Intercom shared-app-server patch, `sharedAppServerSocket`, a `programs.codexDesktopLinux` configuration, and an `agent-intercom-codex-bridge` so Intercom could attach to a Desktop-owned server. Rebase/maintenance commits kept that patch alive temporarily. Commit `2fb9f089fafb` deleted the patch and service branch.
- Commit `f05a3639de72` moved the graphical path to the unofficial `codex-desktop-linux` module, enabled Computer Use/Mobile Control, configured a shared Unix socket, and declared a bridge service. Commit `2fb9f089fafb` also removed that input, module, and bridge.
- The first official ChatGPT package in `2fb9f089fafb` used a `symlinkJoin` wrapper setting `CODEX_CLI_PATH` to managed Codex; a follow-up added the Wayland argument. The direct CLI wrapper was superseded by the current local-daemon plus `resources/codex` design.

Classification: already absent or superseded. Preserve as history; do not search for or recreate these deleted files during rollback.

### 1. Persistent Codex owner

The user environment declares a per-user `codex-remote-control.service` running the canonical Codex package as a long-running app server on its private control socket, rooted in the primary workspace. Daemon-backed terminal sessions and phone Remote Control use it independently of ChatGPT Desktop.

Classification: independent foundation. Retain unless the living separately abandons persistent terminal/phone Remote Control.

### 2. Packaged CLI gate and bare app-server proxy

An early Desktop attempt changed the packaged Codex gate so ChatGPT's bare `resources/codex app-server` launch would proxy to the persistent owner's Unix socket. It landed in user-environment commit `799f8fd2d549241c323f84f6ff80fe9255a76615`.

The real Desktop invocation included feature, analytics, and dynamic `codex_app` arguments. A bare proxy would discard those per-launch values and Electron's App Tools callback path. Later commits removed stale gate consumers and moved away from this design.

Classification: failed historical approach; verify it is absent from current source, but do not recreate or widen it.

### 3. Forced native local-daemon wrapper

The ChatGPT wrapper was changed to set the private local-daemon selection variable while clearing CLI- and App-Tools-related override variables. This tells Desktop to prefer the persistent local owner rather than its private stdio Codex child.

Classification: Desktop-specific shared-owner wiring. Remove for stock Desktop behavior.

### 4. Managed `resources/codex` resolver candidate

The package derivation injects the canonical managed Codex executable at ChatGPT's `resources/codex` path. This was added in commit `b04edb442f52` because the local-daemon branch still performs `codex app-server daemon version` before selecting WebSocket. Without the candidate, Desktop failed before initialization.

Classification: introduced to make the shared-owner selection path pass its preflight. For strict stock behavior, restore the upstream package's resource tree. If the upstream Linux package independently requires a companion executable even for its stock private-core path, that packaging requirement must be re-established from upstream rather than assumed.

### 5. ASAR startup-override rewrite

The package runs `patch-asar.py` over the shipped Electron `app.asar`. One rewrite makes `getConfigOverrides` return an empty list so Desktop's native local-daemon branch is reachable. This landed as part of the ordinary-client implementation in commit `64d4784969e8f82cd9b4a732e8c27e8a5e90929c`.

Classification: direct mutation of private Desktop internals. Remove for stock Desktop behavior.

### 6. ASAR App Tools producer suppression

A later rewrite makes the minified `codex-app-tools-mcp` producer return no edits. It was introduced in commit `51676f4eed1c2356faef799ebe8f0d12b933384c` after Desktop kept injecting malformed `mcp_servers.codex_app` configuration independently of `getConfigOverrides`.

One version of this rewrite introduced an extra closing brace and made the updated Desktop fail with `Unexpected token '}'`; a later correction repaired the JavaScript syntax. Successful initialize afterward did not prove new-chat or resume behavior.

Classification: direct mutation of private Desktop internals. Remove for stock Desktop behavior.

### 7. Other `codex_app` producers and sanitizers

The `cf0ed9` ASAR trace directly found the patched `Pge`/earlier `JE` resolver, a dormant-looking `_T` serialized empty-command fallback, direct `cj` and `h0` helpers adding an empty-command `mcp_servers.codex_app` object, and generic `_nr`/`ynr` MCP bridges. It did not prove `_T` was called or that `cj`/`h0` supplied the normal Composer request. A later diagnosis reports a local-thread branch emitting only `mcp_servers.codex_app.enabled_tools`; with the base producer suppressed, that partial table has neither `command` nor `url`. The normal Composer producer remains uncaptured.

The originating thread's last response reported a wider sanitizer in `patch-asar.py` with a corresponding desktop-support check, a non-zero focused check, and no commit or deployment. The fresh working-tree witness confirms those two dirty files and the accidental Python bytecode artifact, while the active source pin excludes them.

Classification: an undeployed, uncommitted working-tree candidate, not active product state or approved design. Preserve it as found evidence until an authorized rollback snapshots and removes it; do not finish it.

### 8. Custom package checks

The user environment added checks for the wrapper variables, resolver candidate, ASAR markers, persistent-owner unit/socket contract, and disposable app-server start/resume behavior. The checks exercised and reported passing package shapes and bare Codex behavior but did not exercise Desktop Composer's actual generated configuration, allowing green builds while the reported real new-chat path remained broken.

Classification: tests encoding the Desktop-specific shared-owner contract must be removed or replaced with stock-package integrity and ordinary launch checks when the contract is rolled back. Independent persistent-owner tests remain relevant if that service is retained.

### 9. Immutable consumer pins and deployments

The system consumes an immutable revision of the user environment. Every landed Desktop attempt required a consumer revision update and declarative deployment. These pins are not hacks themselves; after rollback they must point to the new stock-behavior user-environment revision. Directly changing installed or running files would be lost on rebuild.

A separate fresh Lojix `Query.ByNode` followed by `Query.ByDeployment.(144)` witnessed user-environment deployment 144 as the current completed, succeeded activation at system revision `d6c69fb46a6114a2ea472c9fb89ce8925b81f942`. The installed/source witness independently resolves that system revision to user-environment pin `90a12633cc60` and the customized package described above.

Classification: update as a deployment consequence; do not delete the declarative ownership boundary.

### 10. Stale architectural and upgrade prose

The user environment's upgrade prose still describes the deleted bare-app-server gate/proxy topology. The system's architecture prose still says the Desktop module owns `CODEX_CLI_PATH` and its own app server, while the selected package clears that variable and uses a direct candidate.

Classification: stale documentation, not runtime code. Update it in the rollback so it describes the selected stock/private-core boundary and the separately retained persistent owner.

## Items not established as rollback targets

- The official ChatGPT package version pin, unpacking derivation, desktop entry, MIME association, and unrelated Wayland integration are packaging concerns, not evidence of persistent-server wiring.
- Canonical Codex package ownership and version alignment are shared by terminal and service consumers; they need not be removed to restore stock Desktop behavior.
- Agent Intercom's current MCP entry/package and the independent VSCodium ChatGPT/Codex sidebar are separate consumers. The inspected source contains no shared app-server socket option in current Agent Intercom.
- Full-access defaults are a separate session-permission preference, not the cause of `mcp_servers.codex_app` transport failure.
- The current ASAR patcher also carries `SKIP_PROCESS_REPORT` and `COPY_PLUGINS_WRITABLE` mutations. They are not persistent-Codex wiring. A strict unmodified-ASAR destination would remove them too; retaining either for an unrelated Linux packaging need requires a separate decision and test rather than silently keeping the general patch step.
- No retained evidence finds a durable malformed `codex_app` entry in ordinary Codex configuration, Desktop atom state, inspected session metadata, the persistent database, or the valid bundled plugin manifest. No data migration or conversation deletion is indicated.
- The retained evidence reports no Nexus implementation for this Desktop path and reports no cross-vendor broker or transparent multi-generation migration among the inspected surfaces.

## Provisional removal set

For stock ChatGPT Desktop behavior while retaining persistent Codex for terminal/phone use:

1. Snapshot the pre-existing dirty user-environment work as required by repository policy, then remove the uncommitted sanitizer, its partial check changes, and the accidental bytecode artifact.
2. Stop invoking the ASAR patch and remove every shared-owner/App-Tools rewrite it carries.
3. Remove wrapper variables that force local-daemon mode or suppress the stock CLI/App Tools route.
4. Restore the upstream ChatGPT resource tree; retain a Codex companion only if current upstream packaging itself requires one for stock operation.
5. Remove or rewrite Desktop-specific assertions so they test the stock artifact and launch path rather than the abandoned bridge.
6. Correct the stale user-environment upgrade prose and system architecture prose at the same semantic boundary.
7. Keep the persistent owner, terminal wrapper, Agent Intercom, editor sidebar, and their independent tests unless the living explicitly removes those capabilities too.
8. Update the system's immutable user-environment input and deploy only through Lojix after a separate authorized realization round.

## Why the attempts accumulated

The following is analysis from the records and witnesses, conditional on a stock-Desktop destination. They support several contributing causes rather than one singular explanation:

- ChatGPT Desktop exposed a private local-daemon path, while the inspected work found no stable supported contract for attaching all of its per-thread behavior to the external persistent owner.
- The implementation targeted minified private bundle details whose function names and call paths changed between Desktop releases.
- Early tests checked resolver markers, initialize handshakes, and bare app-server calls, but not the Composer-generated `thread/start` and `thread/resume` payloads.
- Successive patches suppressed one producer at a time; another branch could still create a partial invalid `codex_app` table.
- Home activation changed the profile but not an already-running Electron process, creating a separate stale-process failure during diagnosis.

The exact normal-Composer producer was not captured in the retained request logs. If the living explicitly selects stock Desktop rather than another private-bundle patch, resolving that unknown is not required to remove the private integration; it would still matter to any attempt to preserve it.

## Sources

- [Remembered cf0ed9 account](/home/li/primary/flows/ea1e56/reports/remembered-cf0ed9.md:1)
- [Current source and revision inventory](/home/li/primary/flows/ea1e56/reports/source-inventory.md:1)
- [Fresh current-state witness](/home/li/primary/flows/ea1e56/witnesses/current-desktop-codex-state.md:1)
- [cf0ed9 producer trace](/home/li/primary/flows/cf0ed9/reports/remaining-codex-app-producer.md:1)
- [cf0ed9 code and deployment path](/home/li/primary/flows/cf0ed9/reports/code-and-deployment-path.md:1)
- [Later focused diagnosis](/home/li/primary/flows/d30eb1/log.md:1)
- [Ordinary-client decision and implementation history](/home/li/primary/flows/01a05487/log.md:1)
- [Desktop resolver-candidate repair history](/home/li/primary/flows/01a05c80/log.md:1)
- [Dynamic App Tools producer repair history](/home/li/primary/flows/01a05e53/log.md:1)
- [Earlier persistent-owner and proxy history](/home/li/primary/flows/01a047d2/log.md:1)
- [Earlier persistent-owner Vision](/home/li/primary/flows/01a047d2/vision/remoteControl.md:1)
- [Current flow Vision](/home/li/primary/flows/ea1e56/vision/desktopCodexIntegration.md:1)
