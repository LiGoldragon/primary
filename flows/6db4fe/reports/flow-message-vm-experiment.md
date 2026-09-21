# Experimental Flow/Message VM gate

Field 6db4fe prepared the isolated `flows/6db4fe/flow-message-vm` NixOS test. Its lock pins Flow `1b57de018a821e73d5cc31662ad107cb38d65736` and Message `580021b936914b2a0585db1b99cc21a5595d0224` as **experimental** inputs. The test definition boots one disposable NixOS guest with both candidate binaries, starts their Nexuses against guest-only stores and sockets, then calls each actual CLI: Flow resolves one missing recipient to a typed refusal, and Message queries one missing recipient receipt. It uses no model login or credential. This is the first raw CLI/Nexus smoke; it does not assert delivered transport, locked mode, authorization, or a production release.

`nix flake lock path:/home/li/primary/flows/6db4fe/flow-message-vm` succeeded. `nix eval --raw 'path:/home/li/primary/flows/6db4fe/flow-message-vm#checks.x86_64-linux.candidate-vm.drvPath'` evaluated to `/nix/store/qki5i7iv2zw6v3lci8p9xzy4cl0kfqas-vm-test-run-flow-message-candidate-raw-vm.drv`. This verifies the pinned test definition evaluates; **the VM was not built or booted**.

The first actual configured-builder candidate check was:

```sh
nix build --no-link --print-out-paths --max-jobs 0 --builders @/etc/nix/machines --option fallback false 'github:LiGoldragon/flow/1b57de018a821e73d5cc31662ad107cb38d65736#checks.x86_64-linux.flow-conflicting-registration-refusal'
```

It reached `ssh-ng://nix-ssh@prometheus.goldragon.criome` and **failed** in derivation `/nix/store/rpmsxfmp0xaa5g12kgxs8az8m80vligc-flow-workspace-test-0.3.0.drv`: Rust E0596 at `crates/flow-nexus/src/store.rs:727` declared `candidate` immutable, while lines 774–778 extend `candidate.retired_registration_ids`. The released Flow candidate therefore cannot currently compile; the VM test must not be run against this graph.

The 9dd rollout owner and Mind Medium graph owner were sent this concrete failure through the established courier, without a status or acknowledgment probe. VM runtime is held until the retained candidate writer fixes the compile error and the release owner publishes one immutable graph with current generated Signal contracts, exact lock inputs and a Field parity fixture. At that point update the two exact pins, refresh the lock, re-evaluate, and run the test with the configured remote builders and `--max-jobs 0 --option fallback false`; retain the guest logs and result. Further single-recipient delivery, locked-mode, lifecycle, and authentication negative cases require separate accepted contract fixtures. Running production services, stores, units, sockets and consumer pins were untouched.
