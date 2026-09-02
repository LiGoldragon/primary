# Remaining `codex_app` producer trace

Observed 2026-09-02 from the deployed ChatGPT Desktop process and its active
ASAR, then compared with the authored Home package and the records for flows
`01a05e53` and `01a05d17`. This is a read-only trace. No implementation,
configuration, deployment, or persistent owner state was changed.

## Conclusion

The `async function JE` name in the earlier generation is the minified name of
the App Tools resolver producer (`Pge` in the active 26.831.21537 package).
The current patch makes that function return an empty list, but it does not
remove all ways to put a `mcp_servers.codex_app` value into a thread request.

The strongest remaining source candidates are two independent helpers in the
active `/.vite/build/src-B8dS-jjl.js` bundle:

* `cj` unconditionally spreads its caller's config and then adds
  `mcp_servers.codex_app: {enabled: false, command: ""}` before calling
  `startThread`.
* `h0` does the same before calling `forkThread` or its fresh-thread
  `startThread` fallback.

Both objects are invalid for Codex 0.152.1: the empty command is not a usable
stdio transport, and there is no HTTP `url`. This is enough to explain why a
successful Desktop bootstrap can still fail at configuration loading for a
new thread. It also explains why the `JE`/`Pge` no-op did not correct the
living's observed payload.

The exact final producer for the normal Composer request is not proven by the
ASAR alone. The `cj` callers are ambient-suggestion paths and the `h0` callers
are generic generated-response/title-reconsideration paths. The active bundle
also exposes generic MCP configuration bridges that can write this key if a
caller supplies `key: "codex_app"`. The runtime log does not include the
merged request body, so these must remain candidates until a captured
`thread/start` request or an instrumented bridge identifies the normal
Composer caller.

## Ownership and active package

The authored-to-deployed path is:

1. `owned-agents/chatgpt/hashes.json` selects the signed ChatGPT Desktop
   26.831.21537 package.
2. `owned-agents/chatgpt/unwrapped.nix:134-157` unpacks it, installs the
   canonical Codex executable as `resources/codex`, and invokes
   `owned-agents/chatgpt/patch-asar.py` on `resources/app.asar`.
3. `owned-agents/chatgpt/default.nix:28-35` wraps the resulting executable,
   selecting local-daemon mode while unsetting the CLI and private App Tools
   override variables.
4. The running main process (PID 1675402 at observation time) resolves to the
   26.831.21537 package. Its ASAR contains exactly one
   `getConfigOverrides:()=>[]` marker and one `async function Pge(){return[]}`
   marker.

This makes `patch-asar.py` the authored owner of the current App Tools change;
there is no separate checked-in source for the minified Desktop bundle. The
current patch has four patterns (`patch-asar.py:9-64`), and none targets the
`src` helpers `cj` or `h0`, nor the `_T` fallback.

The persistent Codex owner is separately declared by the Home profile and is
currently `codex app-server --remote-control --listen unix://` under
`codex-remote-control.service`, running Codex 0.152.1. The Desktop process is
therefore crossing the intended persistent-owner boundary; this trace found
no second owner. The desired user behavior in
`flows/01a05d17/vision/fullAccessPermission.md:3-6` is a Desktop-created
Codex session with full access, not a private malformed App Tools transport.

## Exact active-ASAR inventory

The ASAR header was parsed read-only, then each JavaScript file was searched
for exact `mcp_servers.codex_app` and function-name references. Offsets below
are content offsets within the named minified file.

| Location | Evidence | Classification |
| --- | --- | --- |
| `/.vite/build/main-7MZ5kTIG.js:1014921` | `Mge` validates `mcpServers.codex_app` with a `command` string and optional `env`. | Schema only; no object is created here. |
| `/.vite/build/main-7MZ5kTIG.js:1015019` | `Nge = ...("codex-app-tools-mcp")`; `async function Pge(){return[]}`. | Patched resolver producer. Its static function-name search has no call reference in the active main bundle. |
| `/.vite/build/main-7MZ5kTIG.js:1016362` | `_T(e)` returns the serialized string `mcp_servers.codex_app={command="",enabled=false}`. | Invalid fallback remains in the bundle. `_T(` has no call reference in the active main bundle, so execution is not proven. |
| `/.vite/build/src-B8dS-jjl.js:525911` | `cj` builds `config:{...c,"mcp_servers.codex_app":{enabled:!1,command:``},model_reasoning_effort:r}` and passes it to `d.startThread`. | Direct executable producer. |
| `/.vite/build/src-B8dS-jjl.js:527817` | `Lne` calls `cj` for `ambient_suggestion_safety`; this is one call site. | Direct call site for `cj`. |
| `/.vite/build/src-B8dS-jjl.js:533972` | The ambient-suggestions worker calls `cj` for generated suggestions. | Direct call site for `cj`. |
| `/.vite/build/src-B8dS-jjl.js:1208620` | `h0` builds `v={...s,"mcp_servers.codex_app":{enabled:!1,command:``},model_reasoning_effort:r}` and passes it to `forkThread` or `startThread`. | Direct executable producer. |
| `/.vite/build/src-B8dS-jjl.js:1210010` | `g0` calls `h0` for a generated response. | Direct call site for `h0`. |
| `/.vite/build/src-B8dS-jjl.js:1506843` | `$9`, reached by `ide`, calls `h0` for `thread_title_reconsideration`. | Direct call site for `h0`. |
| `/.vite/build/src-B8dS-jjl.js:390569` | `Ux` and `Wx` name the `codex_app` namespace and its `enabled_tools` setting. | Namespace/setting metadata, not a transport object producer. |
| `/webview/assets/app-initial-8b9dbc7eb80a.js:2087358` | `ADt` filters tools in a `codex_app` namespace. | Tool filtering, not a transport object producer. |

The two `src` object literals are the material correction target. They are
independent of `Pge`: no caller of either helper invokes `Pge`, and the helper
config objects are built locally from their arguments. A no-op at the resolver
hook cannot remove an object literal that is later added by a different
function.

## Configuration writers, merges, and bridges

The active bundle has several paths that must be distinguished from the two
hard-coded producers:

* In `main-7MZ5kTIG.js:145715-146109`, the local CUA synchronization function
  (`ds`) sends `config/batchWrite` with a dynamic
  `mcp_servers.${n.oc}` edit. The neighboring `cua_repl` schema, plugin file
  update, and `node_repl` read path identify this as the CUA/Node-REPL
  synchronizer, not a literal `codex_app` writer in the current package. Its
  dynamic shape is still a bridge in principle, so its key must be verified
  if the imported identifier ever changes.
* In `main-7MZ5kTIG.js:3005432`, Desktop initializes its settings store with a
  `batchWriteConfigValues` callback that forwards caller-supplied edits to
  `config/batchWrite`. This callback is generic and can carry any key supplied
  by the webview; it does not itself name `codex_app`.
* In `app-initial-8b9dbc7eb80a.js:3981190`, `_nr` accepts `{filePath,key,value}`
  and sends `config/batchWrite` with
  `keyPath: mcp_servers.${key}`, `value`, and `mergeStrategy: replace`. A
  caller passing `key: "codex_app"` can create or replace the invalid entry.
  The function's static name search found only its definition, so a current
  caller was not established.
* In `app-initial-8b9dbc7eb80a.js:3981784`, `ynr` forwards an arbitrary key
  as `mcp_servers.${key}.enabled` through `config/value/write` with `upsert`.
  It can create or mutate a partial `codex_app` entry when called with that
  key, but no current call site with that argument is visible in the bundle.
* The generic config writer near
  `app-initial-8b9dbc7eb80a.js:3987597` accepts an arbitrary `keyPath` and
  chooses `replace` or `upsert`. It is another capability boundary, not
  evidence of a hard-coded producer.
* The `config/mcpServer/reload` request near
  `app-initial-8b9dbc7eb80a.js:3976850` only asks the owner to reload MCP
  servers. It does not create the object.
* The main thread request interceptor (`main-7MZ5kTIG.js:65184-66493`) only
  strips the reserved `mcp_servers.artifact_session` subtree from
  `thread/start`, `thread/resume`, and `thread/fork` when its viewer path is
  active. It does not strip `mcp_servers.codex_app`, so it cannot protect the
  current request boundary from this key.

The important negative result is that the active main bundle contains no
hard-coded `config/batchWrite` edit with literal `mcp_servers.codex_app`.
The earlier flow's direct `config/batchWrite` attribution therefore remains
valid evidence for its then-active generation, but is not by itself a proof
of the current main bundle's `ds` path. The current source has two new direct
producers in `src`, plus generic bridges; the final Composer caller remains
unidentified.

## Runtime and cached-state boundary

Flow `01a05e53` records the original failure as an app-server configuration
load rejection before both `thread/start` and `thread/resume`, with no
`mcp_servers.codex_app` section in the ordinary static config. The available
live diagnosis records the same boundary: Desktop bootstraps and reaches its
local app-server connection, then Composer's `thread/start` receives
`-32600` with `invalid transport in mcp_servers.codex_app`.

The current static state does not identify a durable malformed object:

* `/home/li/.codex/config.toml` has MCP sections but no
  `[mcp_servers.codex_app]` section.
* `/home/li/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/codex-app-tools/desktop-mcp.json`
  is a valid definition containing a command and arguments. Its existence
  proves only that the valid plugin material is cached; it does not prove that
  a thread request used it.
* `/home/li/.config/Codex` is the Electron user-data/cache boundary. Earlier
  flow auditing found no durable malformed `codex_app` entry in the Desktop
  atom state or inspected session metadata. The current process and owner
  were not modified during this trace.
* `/home/li/.codex/sqlite/codex-dev.db` is persistent app-server state. The
  owner remained active and its state was not changed by this read-only
  inspection. Conversations and the owner are therefore not targets for a
  repair migration.

This evidence supports a request-local or in-memory merge, rather than a
simple stale `[mcp_servers.codex_app]` line in the ordinary user config. It
does not prove whether the normal Composer request got the value from `cj`,
`h0`, a generic bridge, or an unlogged Desktop path.

## Correction and recommended source target

The sentence that led to the earlier incomplete correction was effectively:
“Disabling the separate `codex-app-tools-mcp` generator removes the remaining
`codex_app` producer.” The active package disproves the word “remaining.” The
`Pge` no-op is still useful for preventing the private App Tools resolver and
its transport selection, but it is not a complete config invariant.

The smallest supported source correction for the known direct producers is to
remove the hard-coded `mcp_servers.codex_app` property from both `cj` and
`h0`, leaving the caller config and `model_reasoning_effort` intact. In the
authored package this means adding exact, byte-length-preserving ASAR patch
patterns to `owned-agents/chatgpt/patch-asar.py`, each requiring one match:

```text
cj: config:{...c,"mcp_servers.codex_app":{enabled:!1,command:``},model_reasoning_effort:r}
  -> config:{...c,model_reasoning_effort:r}

h0: {...s,"mcp_servers.codex_app":{enabled:!1,command:``},model_reasoning_effort:r}
  -> {...s,model_reasoning_effort:r}
```

The `_T` fallback should also be neutralized to return no edits (or otherwise
never serialize the empty-command assignment), even though its active bundle
has no static call reference. Finally, the Desktop generic MCP bridges should
reject or omit the reserved `codex_app` key if the product decision is that
Desktop is no longer allowed to create private App Tools. A central sanitizer
at the `thread/start`/`thread/resume` config boundary is the strongest
defense-in-depth option for stale in-memory values, but it should supplement
removing the producers rather than hide an unbounded writer.

No source or deployment edit was made because the delegated brief explicitly
requested read-only tracing before correction.

## Durable behavioral test boundary

The existing `checks/desktop-app-support/default.nix` proves package wiring,
the two current markers, and a disposable bare Codex
`initialize`/`thread/start`/`turn/start`/`thread/resume` sequence
(`default.nix:151-204`). It does not exercise the `cj`/`h0` config merge, the
generic webview writers, or a thread request carrying the malformed object.
Consequently it can pass while the living Desktop still fails.

The durable check should have two behavior layers:

1. Run the complete `patch-asar.py` fixture with both minified `cj` and `h0`
   shapes plus `Pge` and `_T`. Load the resulting fixture with Node and invoke
   each helper against a fake client that records `startThread` and
   `forkThread` parameters. Assert that neither captured config contains
   `mcp_servers.codex_app`, and ask `node --check` to parse the result. This
   catches a patch boundary regression without relying on a string-only
   marker.
2. Send the captured, sanitized configs through a disposable Codex app-server
   in a temporary `CODEX_HOME`, then require successful `thread/start` and
   `thread/resume`. Include a negative control containing
   `{enabled:false,command:""}` and assert the server rejects it with the
   known invalid-transport error; this proves the test is sensitive to the
   bug. Keep the persistent owner and user conversations out of the check.

The final deployment-time acceptance remains GUI-native: after a fresh
ChatGPT process is opened, exercise one new chat and one existing-thread
resume, and capture the outgoing request or sanitized logs. Success requires
both operations to complete through the sole persistent owner with no
`invalid transport` error. At present, no current `thread/resume` runtime
witness is available, so resumed-thread success is unresolved.

## Sources

- [Authored ASAR patch](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/patch-asar.py:36)
- [Authored ChatGPT package build](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/unwrapped.nix:134)
- [Authored ChatGPT wrapper](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/default.nix:28)
- [Current durable package check](/git/github.com/LiGoldragon/CriomOS-home/checks/desktop-app-support/default.nix:151)
- [Original producer and runtime-boundary record](/home/li/primary/flows/01a05e53/log.md:3)
- [Desired full-access Desktop behavior](/home/li/primary/flows/01a05d17/vision/fullAccessPermission.md:3)
- [Sanitized live new-thread failure diagnosis](/home/li/primary/flows/cf0ed9/reports/live-diagnosis.md:7)
- [Current static Codex config](/home/li/.codex/config.toml)
- [Current valid cached App Tools definition](/home/li/.codex/.tmp/bundled-marketplaces/openai-bundled/plugins/codex-app-tools/desktop-mcp.json)
- Active process `/proc/1675402/exe`, package version 26.831.21537, and its internal ASAR files/offsets listed above (read-only extraction on 2026-09-02).
