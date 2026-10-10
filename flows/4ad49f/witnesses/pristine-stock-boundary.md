# Pristine ChatGPT stock boundary witness

Method: read-only source inspection of the CriomOS-home checkout, read-only
inspection of the pinned OpenAI Debian archive already present under `/tmp`,
signature-key and archive-member inspection, extraction of the vendor data
tree into a temporary directory, read-only inspection of the vendor ASAR, and
byte comparison with the known root-pinned Nix output. No product source,
installed file, service, process, user state, configuration, cache,
credential, conversation, or deployment state was changed. No Nix build was
run.

## Observations

### Source revisions and selection

- CriomOS-home `main` was `0b0a9683` (`Preserve unreviewed ChatGPT sanitizer candidate as evidence`) when inspected. Its working copy had an unrelated concurrent modification to `checks/desktop-app-support/default.nix`; the authored `owned-agents/chatgpt/patch-asar.py` contained eight patch patterns, including the later `cj`, `h0`, serialized-fallback, and request-sanitizer candidates.
- CriomOS itself is pinned to CriomOS-home revision `90a12633cc60148b62bc47fd44957e6165727094`, not the newer Home `main`. The pinned `90a` patch file contains only four patterns: `SKIP_PROCESS_REPORT`, `COPY_PLUGINS_WRITABLE`, `SHARED_APP_SERVER`, and `NO_APP_TOOLS_CONFIG_OVERRIDE`. The active known Nix output inspected below is therefore evidence for the deployed/root-pinned four-pattern package, while the additional `main` patterns are source candidates, not deployed proof.
- The Home package source (`owned-agents/chatgpt/unwrapped.nix:134-170`) unpacks `usr/lib/chatgpt`, copies the vendor application tree, removes `resources/codex`, installs a symlink to the canonical Nix Codex package, runs `patch-asar.py`, wraps the GUI, and adds Qt RPATHs. The outer package (`owned-agents/chatgpt/default.nix:28-36`) adds launch flags, sets `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1`, and unsets four CLI/private-channel variables.

### Pinned archive versus the mutable current URL

- `owned-agents/chatgpt/hashes.json` pins x86_64 version `26.831.21537` to SRI `sha256-XBVu8qLgKRWW0HuuhmDvTwt0jfO6+Rv8ko97XjxhCxE=`. The local `/tmp/tmp.5h42ovBoNs/chatgpt.deb` is version `26.831.21537`, 410,146,862 bytes, and has SHA-256 `5c156ef2a2e0291596d07bae8660ef4f0b748df3baf91bfc928f7b5e3c610b11`, exactly the SRI digest.
- The archive has an `_gpgorigin` OpenPGP signature packet whose issuer fingerprint is `3BFA0E4AE8B8CC16A2D9BA684A3B4A566C4660E4`, the same fingerprint in `openai-archive-key.asc`; the package control member identifies OpenAI `chatgpt` version `26.831.21537`.
- The currently fetched signed `dists/stable/InRelease` is a good signature from that key, but its current `Packages` record has advanced to version `26.901.20858` and SHA-256 `42a6477f22f4136d62321eda7b4697a79da1eb66d61dcb85ab0420860a1a5223`. Therefore the fixed-output 26.831 archive and its pinned hash must be kept distinct from the mutable repository index now served at the same repository URL. The current index does not prove the historical 26.831 package record.

### Vendor application resource tree

The extracted vendor tree is rooted at `usr/lib/chatgpt` and contains:

```text
ChatGPT                         Electron GUI executable
codex-launcher                  shell launcher; execs ChatGPT
resources/
  app.asar                      292,435,829 bytes; 8,935 ASAR files
  app.asar.unpacked/
  codex                         255,505,120-byte executable
  codex-code-mode-host          69,316,672-byte executable
  rg                            5,408,904-byte executable
  cua_node/
  plugins/openai-bundled/
  skills/skills/
  default_app/
  native/
  artifact-template-picker/
  accessibility/
  busy-bar.asar, native data, metadata, and icons
```

The vendor also ships `resources/linux-package-metadata.json` and
`resources/owl-app.ini`, both identifying `26.831.21537`. Running the bundled
`resources/codex --version` with an isolated temporary `CODEX_HOME` reported
`codex-cli 0.152.1`. There is no need for a separate external CLI path merely
to provide the stock candidate.

The pristine ASAR's top-level entries are `.vite`, `native-menu-locales`,
`node_modules`, `package.json`, and `webview`. Static source inside it shows
the vendor resolver searching the packaged resource path, including
`resources/codex` and `app.asar.unpacked/codex`, and then running the selected
executable as `codex app-server daemon version` before considering the local
daemon branch. The connection code starts as `stdio`; it selects WebSocket to
`app-server-control/app-server-control.sock` only when the local-daemon
environment and other no-override conditions hold. Otherwise it starts the
selected bundled CLI through its stdio app-server.

### Exact pristine comparison

The vendor app.asar extracted from the fixed-output archive has:

```text
size  292435829
sha256 9745ec1195897c019533d08e8415ab81a3c4e59e845403fdfea42ce1272fe954
```

The known root-pinned output
`/nix/store/sggmyn0j99xypqala8vaqhhr5ghiq0f8-chatgpt-unwrapped-26.831.21537/lib/chatgpt/resources/app.asar`
has the same size but:

```text
sha256 1f34de646fa2d1b5f8e687a6d52298659053a618f33db5119028f26748dc62eb
cmp --silent vendor.app.asar packaged.app.asar  => exit 1
different bytes 1355
```

The differing bytes form four patch regions (the individual replacement
regions contain unchanged padding bytes): around offsets 3,122,903
(`COPY_PLUGINS_WRITABLE`), 4,039,854 (`NO_APP_TOOLS_CONFIG_OVERRIDE`),
5,604,938 (`SHARED_APP_SERVER`), and 11,010,555 (`SKIP_PROCESS_REPORT`).
The proof of a pristine packaged ASAR is consequently an exact `cmp` against
the ASAR extracted from the pinned archive, or equality of both size and the
vendor SHA-256 above; marker searches alone are insufficient.

The Nix output's `resources/codex` is a 67-byte symlink to
`/nix/store/vp307a51wwncdl5cd7a8mm3d1w1x5qj6-codex-0.152.1/bin/codex`, whereas
the vendor output has the 255,505,120-byte regular executable. The rest of
the copied resource layout is substantially the vendor tree; ordinary Nix
ELF/RPATH and dependency wrapping also changes generated binaries and is a
packaging adaptation, not by itself a persistent-owner crossing.

## Source-derived interpretation

### Stock CLI/Core boundary

OpenAI ships the GUI, its app.asar client, a complete packaged Codex CLI at
`resources/codex`, the code-mode host, and supporting CUA/plugin/skill
resources in one Debian archive. The app requires an executable candidate for
its app-server connection, but the stock archive supplies that candidate.
Stock behavior therefore keeps the Desktop frontend coupled to the
vendor-shipped CLI/Core (normally its own stdio app-server); it does not need
the Home-managed Codex derivation or the persistent `codex-remote-control`
service to satisfy the stock boundary.

### Desktop-to-persistent-owner mutations

These source changes are specifically part of the custom persistent-owner
crossing and are not vendor behavior:

- `CODEX_APP_SERVER_USE_LOCAL_DAEMON=1` forces the vendor local-daemon branch.
- Unsetting `CODEX_CLI_PATH` prevents the vendor stdio-selection override;
  unsetting `CODEX_APP_SERVER_FORCE_CLI` and
  `CODEX_APP_SERVER_CLI_COMMAND` suppresses other CLI/transport forcing; and
  unsetting `CODEX_APP_TOOLS_PIPE_PATH` suppresses the private App Tools pipe.
- Deleting vendor `resources/codex` and replacing it with the canonical Nix
  Codex symlink changes the Desktop/Core owner and version source.
- `SHARED_APP_SERVER` changes the vendor `getConfigOverrides` call to
  `()=>[]`; `NO_APP_TOOLS_CONFIG_OVERRIDE` removes the private App Tools
  resolver producer. The later Home-main candidate additionally strips the
  `cj`/`h0` `mcp_servers.codex_app` objects, the serialized fallback, and
  outgoing thread config. Those later patterns are not in the root-pinned
  90a package and have no deployment proof here.

### Generic Linux/Nix adaptations

`SKIP_PROCESS_REPORT` and `COPY_PLUGINS_WRITABLE` have no source-level
relationship to the persistent Codex owner. In the vendor ASAR,
`process.report` is guarded and has an ordinary `{}` fallback when unavailable;
the patch merely forces that fallback. The plugin patch changes a recursive
copy to shell `cp -r` followed by `chmod -R u+w`, addressing mutability of a
copied plugin tree. Neither is a demonstrated GUI launch precondition. The
plugin edit may matter for later plugin mutation in a read-only Nix store, but
that is a separate post-launch behavior and was not proven here. For a truly
vendor-pristine Desktop, both patches should be absent unless a separately
approved Nix/Linux runtime witness justifies retaining one.

### Wayland remains separate

The explicit `--ozone-platform=wayland` argument in the package factory and
profile (`default.nix:29-30`, `modules/home/profiles/min/agent-intercom.nix:26-29`)
is a display-stack choice. It is independent of the Codex owner crossing and
should be preserved or changed only as a separate Wayland decision.

## Claims supported by this witness

1. Upstream 26.831.21537 itself ships `resources/codex`; the stock app does
   not require `CODEX_CLI_PATH` when that bundled candidate is present.
2. The root-pinned Nix package is not ASAR-pristine: exact byte comparison
   fails and identifies the four source patch regions above.
3. The current transport environment, candidate replacement, and ASAR
   transport/App Tools changes are Desktop-to-persistent-owner integration
   hacks. The process-report and writable-plugin changes are generic package
   mutations, not owner-boundary requirements.
4. Returning the Desktop application to vendor behavior means restoring the
   vendor ASAR and regular bundled `resources/codex`, while treating Wayland
   launch flags separately.

## Unknowns and authority returned to caller

- The historical signed `InRelease`/`Packages` record that directly named
  26.831.21537 was not retained by the live repository after it advanced to
  26.901.20858. The pinned archive hash and its `_gpgorigin` issuer packet
  are observed; historical index linkage remains unverified here.
- No live GUI launch or authenticated Desktop request was performed. This
  witness does not claim that stock stdio or the vendor local-daemon branch
  succeeds on this host, nor that the persistent owner should be retained or
  removed.
- Removing ChatGPT-specific owner-crossing mutations does not settle whether
  the independent Codex CLI/TUI, Agent Intercom, or
  `codex-remote-control.service` should remain. That owner-topology decision
  requires explicit authority.
- Whether writable plugin copies are needed for a desired plugin update flow
  is unresolved; it is not established as a launch requirement.
- The newer eight-pattern Home-main sanitizer candidate is source evidence
  only. Its acceptance, deployment, and compatibility consequences require
  explicit approval.

## Sources

- [`CriomOS-home/owned-agents/chatgpt/unwrapped.nix`](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/unwrapped.nix:134)
- [`CriomOS-home/owned-agents/chatgpt/default.nix`](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/default.nix:20)
- [`CriomOS-home/owned-agents/chatgpt/patch-asar.py`](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/patch-asar.py:9)
- [`CriomOS-home/owned-agents/chatgpt/hashes.json`](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/hashes.json:1)
- [`CriomOS-home/owned-agents/chatgpt/update.py`](/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/update.py:20)
- [`CriomOS-home/modules/home/profiles/min/agent-intercom.nix`](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix:14)
- [`CriomOS/flake.nix`](/git/github.com/LiGoldragon/CriomOS/flake.nix:36) and [`CriomOS/flake.lock`](/git/github.com/LiGoldragon/CriomOS/flake.lock:944)
- Fixed-output archive `/tmp/tmp.5h42ovBoNs/chatgpt.deb` and its extracted vendor tree `/tmp/chatgpt-pristine-extract.1972779/usr/lib/chatgpt`
- Prior source inventory and deployment-boundary records: [`source-inventory.md`](/home/li/primary/flows/ea1e56/reports/source-inventory.md) and [`current-desktop-codex-state.md`](/home/li/primary/flows/ea1e56/witnesses/current-desktop-codex-state.md)
