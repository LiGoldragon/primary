# Witness — claude-desktop asar unpacking and self-contained local-binary override

Method: fresh clone of `ssh://git@github.com/LiGoldragon/CriomOS-home` at
`654144d`, edited, built through the configured remote builder
(`ssh-ng://nix-ssh@prometheus.goldragon.criome`), and asserted against the
built store output. No Zeus access, no deploy. Evaluation used a local
`system` stub flake (`{ outputs = _: { system = "x86_64-linux"; }; }`) because
CriomOS-home refuses to evaluate without an OS-supplied `system` input;
`--impure` with `NIXPKGS_ALLOW_UNFREE=1` is needed only because an unrelated
blueprint check in the same attrset pulls `unrar`.

Pushed CriomOS-home revision: `ceeaaf4272ea` (`ceeaaf4`), parent
`1ae5da8` ("Remove the Claude Remote Control server", the concurrent subflow).

## Build

    $ nix build --impure --no-write-lock-file --override-input system "path:$W/sys-x86" \
        --print-out-paths --no-link .#packages.x86_64-linux.claude-desktop
    building '/nix/store/j9x05g4qd1sjjahqnpwz9gmvp53xbqzp-claude-desktop-1.46388.2.drv'
      on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
    /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2

## Proof 1 — the built app.asar keeps its native modules unpacked

    $ node checks/desktop-app-support/claude-desktop-asar-contract.cjs \
        /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/lib/claude-desktop/resources/app.asar
    claude-desktop-asar: 3 unpacked entries verified in /nix/store/ynk1b2pn8vq2blsmmi3rmjsx1dd2qn5g-claude-desktop-1.46388.2/lib/claude-desktop/resources/app.asar
    claude-desktop-asar: unpacked node_modules/@ant/claude-native/claude-native-binding.node
    claude-desktop-asar: unpacked node_modules/node-pty/prebuilds/linux-x64/pty.node
    claude-desktop-asar: unpacked resources/github-mcp/github-mcp-server

Header entry for `pty.node` in the built archive (no `offset`; `unpacked: true`):

    {"size":75976,"unpacked":true,"integrity":{"algorithm":"SHA256","hash":"123792d8f22f36d519b21dfb6f4b716f9b18b9e579085ea2840d0773d88d35fd","blockSize":4194304,"blocks":["123792d8f22f36d519b21dfb6f4b716f9b18b9e579085ea2840d0773d88d35fd"]}}

Real file on disk:

    $ ls -l .../app.asar.unpacked/node_modules/node-pty/prebuilds/linux-x64/pty.node
    -r--r--r-- 13 root root 84799 Jan  1  1970 .../pty.node

The on-disk size (84799) exceeds the header size (75976) because `formatelf`
patchelfs the `.node` after packing. Upstream's own archive records the same
75976 for the same SHA-256, so the recorded metadata is upstream's; Electron
reads unpacked entries from the real path, not from the header size.

Negative control — the defective repack (`asar pack` with no `--unpack`)
against the same tree:

    $ asar pack $W/built-app $W/neg/app.asar
    $ node checks/desktop-app-support/claude-desktop-asar-contract.cjs $W/neg/app.asar
    Error: app.asar header marks nothing unpacked: .../neg/app.asar
    rc=1

## Proof 2 — the patched initLocalBinary resolves the real declared binary

Method extracted verbatim from the built `app.asar`
(`.vite/build/index.chunk-DrnJEXHK.js`) and executed:

    async initLocalBinary(e){let executable=!1;try{const nodeFs=require("node:fs");try{nodeFs.accessSync(e,nodeFs.constants.X_OK),executable=!0}catch{executable=!1}}catch(internal){throw Error(`[CCD] LOCAL OVERRIDE: internal error resolving declared binary at ${e}: ${internal&&internal.stack||internal}`)}if(!executable)throw Error(`[CCD] LOCAL OVERRIDE: declared binary unavailable at ${e}`);this.localBinaryPath=e;try{console.warn(`[CCD] LOCAL OVERRIDE: Using local binary at ${e}`)}catch{}}

    [CCD] LOCAL OVERRIDE: Using local binary at /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude
    RESOLVED localBinaryPath = /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude
    ABSENT PATH THROWS: [CCD] LOCAL OVERRIDE: declared binary unavailable at /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude-absent
    INTERNAL ERROR PATH: [CCD] LOCAL OVERRIDE: internal error resolving declared binary at /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude: TypeError: require unavailable

The third line is the discrimination the old injection lacked: an internal
failure can no longer masquerade as a missing binary.

The same three assertions run inside `patch-runtime.mjs` during the build, so
any future bundle drift breaks the build rather than the running app.

## Checks

    $ nix build -L --impure --no-write-lock-file --override-input system "path:$W/sys-x86" \
        --no-link --print-out-paths \
        .#checks.x86_64-linux.claude-desktop-declared-cli \
        .#checks.x86_64-linux.desktop-app-support
    /nix/store/4baapzl3dadjj551ynmydlf04hcn692q-claude-desktop-declared-cli-contract
    /nix/store/58jjjmnzldpn6c7njwji09v6kzycambv-desktop-app-support-contract

Log excerpts:

    claude-desktop-declared-cli: valid override
    claude-desktop-asar: 3 unpacked entries verified in /build/claude-desktop-valid/lib/claude-desktop/resources/app.asar
    ... LOCAL OVERRIDE: Using local binary at /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude
    claude-desktop-declared-cli: missing override
    claude-desktop-asar: 3 unpacked entries verified in /build/claude-desktop-missing/lib/claude-desktop/resources/app.asar
    claude-desktop-runtime: actual manager loaded
    claude-desktop-declared-cli: passed

Re-run after rebasing onto `1ae5da8` and pushing `ceeaaf4`: same two store
paths, rc=0.

## Third defect found while proving

`claude-desktop-declared-cli` was already red on 1.46388.2 before either fix,
which is why defect 2 reached Zeus. `claude-desktop-runtime-contract.cjs`
located the manager binding with `source.lastIndexOf(",", classStart) + 1`,
assuming the bundler emits `,NAME=class{`. 1.46388.2 emits `var POn=class{`,
so the binding read back as

    unexpected Claude Code manager binding: code:SDn(r)}}function MOn(e){return!1}...POn

It now reads the identifier characters immediately left of the assignment.

## Not done

No version surface exists in CriomOS-home and the packaged `version`
(1.46388.2) is upstream's and unchanged, so no version bump applies. The
CriomOS pin of CriomOS-home was not advanced.
