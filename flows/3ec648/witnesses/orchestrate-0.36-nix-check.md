# orchestrate 0.36 nix flake check
Method: scratch clone at b56f2644600f, transient user unit orch036-check (MemoryMax 16G, RuntimeMax 120m), `nix flake check -L`, built on prometheus; waited on unit end. Result: all checks passed (exit 0), x86_64-linux only.
Checks: build carried-store clippy configuration-authority datom-free-nexus doc fmt live-nexus meta-client ordinary-client ordinary-lock-contract peer-authority relocation socket-claim stopping test test-doc.
Landing: main d80a617f7e03 -> b56f2644600f fast-forward, pushed; Lock 11498 held then released.
