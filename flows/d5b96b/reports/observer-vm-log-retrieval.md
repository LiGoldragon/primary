# Observer VM log retrieval — bounded read-only result

Evidence cut: existing package evidence only; no rebuild, VM run, probe, host mutation, or service action.

## Existing commands and results

`nix log /nix/store/nphzpdr10zxza6srixf89c2pgr5gnxbn-vm-test-run-usb-downlink-chain.drv` returned: `got build log for '/nix/store/nphzpdr10zxza6srixf89c2pgr5gnxbn-vm-test-run-usb-downlink-chain.drv' from 'http://nix.prometheus.goldragon.criome'`. The command exited 0, but exposed no child VM log lines.

Evidence files show:

- `usb-downlink-observer/exit`: `0`; bootstrap ended `BootstrapTerminal.Succeeded`.
- `usb-downlink-chain/exit`: `2`; bootstrap ended `BootstrapTerminal.Failed`.
- `chain-nix-log.exit`: `0`; `chain-nix-log` says the remote build log was fetched from `http://nix.prometheus.goldragon.criome`.
- Chain request names drv `/nix/store/nphzpdr10zxza6srixf89c2pgr5gnxbn-vm-test-run-usb-downlink-chain.drv`, revision `8d77ff95a795f6f7f413dd08787b59bb94fe785f`.

## Boundary

The observer package/build-only path succeeded at the bootstrap terminal; the USB downlink chain child failed with exit 2. The supported remote Nix log route confirms transport retrieval but provides no child failure line or pass/root artifact. This is a child-VM/build failure plus a log-detail gap, not evidence of a released observer artifact. Mind Sol’s Luna delegate is separately checking the exact derivation/VM logs; this report does not duplicate that diagnosis.

Source evidence directory: `/tmp/lojix-usb-final-8d77ff95a795-dNODU6`.

- `chain-nix-log` SHA-256 `c98f338909e902e7c4517a5b0fc97801d528703f444503b864092f0e4c582ee5`

- `chain-nix-log.exit` SHA-256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`

- `exit` SHA-256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa`

- `exit` SHA-256 `53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3`

- `bootstrap.log` SHA-256 `5ac67006c6a1a9c1c20524c64b5178a13344dfe5d1cf11d5dcd1bd916baf91ae`

- `bootstrap.log` SHA-256 `ca549df8bc9dff56884b7f1f8313d03652acf51d803994d33f4b84dc357caa3a`

## Prometheus remote route attempt

The documented endpoint is `ssh-ng://nix-ssh@prometheus.goldragon.criome`. A direct read-only shell query,
`ssh -o BatchMode=yes -o ConnectTimeout=8 nix-ssh@prometheus.goldragon.criome 'nix log /nix/store/nphzpdr10zxza6srixf89c2pgr5gnxbn-vm-test-run-usb-downlink-chain.drv'`, failed before command execution with `Permission denied (publickey,keyboard-interactive)`.

The supported store query,
`nix log --store ssh-ng://nix-ssh@prometheus.goldragon.criome /nix/store/nphzpdr10zxza6srixf89c2pgr5gnxbn-vm-test-run-usb-downlink-chain.drv`, failed with `operation 'getBuildLogExact' is not supported by store 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`.

Therefore no remote builder log lines were retrieved. The existing evidence does not establish the child failure cause; it establishes only that the remote exact-log retrieval path is unavailable from this seat. No build, rerun, probe, daemon, service, or network action was performed.

## Mind Sol direct-cause relay

Mind Sol ended the remote retrieval request after an authorized local retry found `undefined ouranosUsbMac` in the generated `testScriptWithTypes` at line 206, before VM launch. This is Mind Sol’s direct relay, not a Field runtime witness. Source evidence supplied by Mind Sol: `/tmp/lojix-usb-chain-retry-tlmzjq`. The remote-log gap is therefore no longer needed for the assigned diagnosis. Mind Sol owns the locked correction on a new immutable revision and the later rerun; no deployment occurred.
