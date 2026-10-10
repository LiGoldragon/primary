# ChatGPT Desktop new-chat code and deployment path

## Conclusion

The source repair for the `codex_app` transport defect is already present in
the current Home source and in the newest activated Home generation. The
currently running ChatGPT process is older than that generation, however. It
started before generation 992 was linked and still runs the prior ASAR that
contains the `codex-app-tools-mcp` producer. The immediate correction supported
by the witnesses is therefore to close and reopen ChatGPT; no implementation or
configuration edit is indicated yet.

This separates two boundaries that were easy to conflate:

1. The persistent Codex owner is healthy and is not the source of the failure.
2. An already-running Electron process does not change executable or ASAR when
   Home Manager changes the profile link.

## Authored ownership

The canonical implementation is in the `CriomOS-home` repository, currently
`main` at `097a9bdef8507e86c7b504037ab2cdd1b70b168e`. That revision is a
descendant of the flow `01a05e53` repair commit
`51676f4eed1c2356faef799ebe8f0d12b933384c`.

| Boundary | Authored source and responsibility |
| --- | --- |
| Binary identity | `owned-agents/chatgpt/hashes.json` pins the official Linux ChatGPT package; the current package version is 26.825.51511. |
| ChatGPT derivation | `owned-agents/chatgpt/unwrapped.nix:139-157` unpacks the `.deb`, copies its application tree, links the canonical Codex executable at `resources/codex`, and invokes `patch-asar.py` on the shipped `app.asar`. |
| Desktop wrapper | `owned-agents/chatgpt/default.nix:25-37` creates the user-facing `chatgpt` wrapper, enables `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1`, clears CLI-forcing variables, and clears `CODEX_APP_TOOLS_PIPE_PATH`. |
| ASAR transport patch | `owned-agents/chatgpt/patch-asar.py:36-43` replaces the startup `getConfigOverrides` call with an empty list, allowing the local-daemon branch. Lines 45-64 replace the separate App Tools configuration producer with `async function <name>(){return[]}`. |
| Canonical package edge | `lib/owned-agent-packages.nix:1-17` constructs ChatGPT with the same `codexPackage` used by the other Home consumers. |
| Profile package selection | `modules/home/profiles/min/agent-intercom.nix:20-28` constructs the ChatGPT package from `config.criomos.corePackages.codex`; lines 171-189 expose it only for projected Edge + cumulative Medium and install its desktop entry/MIME default. |
| Persistent owner | `modules/home/profiles/min/agent-intercom.nix:153-169` owns `codex-remote-control.service`, running the canonical Codex executable as `app-server --remote-control --listen unix://`, rooted at the user's `primary` workspace, with a private service umask and restart policy. |

The source patch is not an alternate transport implementation. It makes the
Desktop application an ordinary local-daemon client and suppresses the private
Electron App Tools configuration that was incompatible with Codex 0.151.0.

## Generated and deployed ownership

CriomOS is the consumer and deployment boundary:

- `CriomOS/flake.nix:35-49` pins `CriomOS-home` at
  `097a9bdef8507e86c7b504037ab2cdd1b70b168e`; the same immutable revision is
  recorded in `CriomOS/flake.lock:939-951`.
- `CriomOS/modules/nixos/userHomes.nix:33-49` imports
  `inputs.criomos-home.homeModules.default`, passes the consumer's package set,
  and materializes only users projected on the target node.
- Home's `flake.nix` exposes the owned ChatGPT package in the Linux package set
  (`ownedPackagesForSystem`) and exposes `desktop-app-support`,
  `codex-remote-control`, and `codex-remote-control-vm` in the check graph.
- The deployment service/profile, not the ChatGPT package, owns activation.
  Home Manager links the new generation and starts/reloads declared user units;
  it does not replace an already-running Electron process.

Read-only live inspection on `ouranos` found:

- `codex-remote-control.service` is active, with Codex 0.151.0, the expected
  `app-server --remote-control --listen unix://` command, and
  `WorkingDirectory=/home/li/primary`.
- The current Home generation is `home-manager-992-link`, updated at
  12:14:21. Its `home-files` desktop entry resolves to the ChatGPT 26.825.51511
  package whose ASAR contains both `getConfigOverrides:()=>[]` and
  `async function JE(){return[]}`.
- The running ChatGPT main process (PID 1440540) started at 12:04:49, before
  generation 992, and its executable belongs to the older generation-991
  package. Its ASAR contains `getConfigOverrides:()=>[]` but not the no-op JE
  marker; it still contains the original `codex-app-tools-mcp` producer and
  `mcp_servers.codex_app` strings.

The generation comparison is a witness of process staleness, not a claim that
the current source failed to build. The process must be restarted to load the
new executable tree.

## Runtime boundary and failure mechanism

The relevant code is inside the packaged Electron ASAR. Byte-level inspection
of the running old package found:

- The local connection constructor first calls `getConfigOverrides`, resolves
  the packaged Codex candidate, and runs `codex app-server daemon version`.
  With an empty override list, local-daemon mode, no CLI-forcing variables, and
  a successful preflight it selects a WebSocket connection to the user's local
  app-server-control socket. Otherwise it falls back to a private stdio
  process.
- The separate `codex-app-tools-mcp` function (`async function JE` in this
  package) reads the bundled `desktop-mcp.json`, constructs a
  `mcp_servers.codex_app=...` configuration string, or emits the disabled
  fallback `mcp_servers.codex_app={command="",enabled=false}`.
- The Desktop startup/configuration path later sends edits through
  `config/batchWrite`. The flow `01a05e53` directly established that this
  producer runs independently of `getConfigOverrides`; therefore patching only
  the resolver does not suppress the producer.
- Codex 0.151.0 rejects the resulting runtime `codex_app` object because it has
  neither a valid `command` transport nor a valid `url` transport. The rejection
  occurs during configuration loading, before both `thread/start` for a new
  chat and `thread/resume` for an existing chat.

The durable source repair addresses both halves: `getConfigOverrides:()=>[]`
selects the shared owner, and `async function JE(){return[]}` prevents the
invalid dynamic `codex_app` edit. The old running process has only the first
half, which explains why it can appear connected while new-chat creation still
fails.

## Durable tests and their boundaries

The repository exposes these checks through Home's Nix `checks` output:

1. `checks/desktop-app-support/default.nix:124-150` checks the profile's
   ChatGPT executable, desktop entry, MIME handler, wrapper environment,
   packaged `resources/codex` candidate, and both ASAR patch markers. Lines
   152-191 then start a disposable Codex app-server over stdio and exercise
   `initialize`, `thread/start`, `turn/start`, and `thread/resume`.
2. `checks/codex-remote-control/default.nix:93-158` checks the projected Home
   service shape, canonical working directories, TUI routing to `unix://`, and
   rejection of lifecycle or alternate-socket invocations.
3. `checks/codex-remote-control-vm/default.nix:44-85` is the runtime VM
   witness. It starts the user service, checks the private socket mode, runs an
   initialize probe, restarts the service, and initializes again after restart.
4. `CriomOS/checks/lojix-ownership/default.nix:120-226` checks the consumer's
   generated Codex/Claude service ownership and `/home/li/primary` working
   directory shape.

The existing checks prove the package artifact, the owner service, and Codex's
protocol independently. They do not launch the actual ChatGPT Electron
process, do not drive its dynamic `config/batchWrite` path, and do not prove
that a running process has reloaded a newly activated package. In particular,
the direct app-server loop in `desktop-app-support` uses a disposable
`CODEX_HOME` and stdio; it is not a connection to the persistent owner.

That is a test-boundary gap, not evidence that another implementation change is
needed now. The first live witness after reopening should cover one new chat and
one resumed chat in the newly started process, while observing that the owner
service remains the sole app-server process.

## Best correction supported by present evidence

The source and generated package are already corrected. Close/reopen ChatGPT so
the process uses generation 992. Then witness both a new chat and a resumed
thread. If the reopened process still emits `mcp_servers.codex_app`, capture
its new executable path and ASAR markers before changing source; that would
indicate a deployment/profile selection defect rather than a missing patch.

Do not widen the Codex transport matcher or reintroduce a proxy. Flow
`01a047d2` established that the Desktop build's dynamic App Tools path cannot
be preserved by a simple bare `app-server` proxy, and flow `01a05e53` settled
that no durable `codex_app` state migration is needed. The smallest supported
correction is therefore process replacement followed by the live witness.

## Sources

- `flows/01a05e53/log.md`: diagnosis of the invalid runtime `codex_app`, its
  independent `config/batchWrite` producer, commit `51676f4...`, and the fact
  that deployment/activation had not yet been witnessed in that flow.
- `flows/01a05d17/vision/fullAccessPermission.md`: the psyche's request that
  a new ChatGPT Desktop Codex session use the desired full-access permission.
- `flows/01a05487/log.md`: settled ordinary-client topology, package update,
  check coverage, and the boundary between package repair and activation/live
  GUI proof.
- `flows/01a047d2/log.md`: the earlier Desktop gate/proxy investigation and
  the warning that preserving Desktop's dynamic App Tools requires more than
  a bare app-server proxy.
- `CriomOS-home/owned-agents/chatgpt/default.nix`.
- `CriomOS-home/owned-agents/chatgpt/unwrapped.nix`.
- `CriomOS-home/owned-agents/chatgpt/patch-asar.py`.
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix`.
- `CriomOS-home/checks/desktop-app-support/default.nix`.
- `CriomOS-home/checks/codex-remote-control/default.nix`.
- `CriomOS-home/checks/codex-remote-control-vm/default.nix`.
- `CriomOS/flake.nix`, `CriomOS/flake.lock`,
  `CriomOS/modules/nixos/userHomes.nix`, and
  `CriomOS/checks/lojix-ownership/default.nix`.
- Read-only live witnesses on `ouranos`: `systemctl --user show`, `ps`, profile
  symlink inspection, and byte-marker inspection of the running and current
  ChatGPT ASARs on 2026-09-02. These witnesses are observations, while the
  correction recommendation above is an inference from them.
