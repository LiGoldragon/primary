# cf7879 wake-adapter receipt

Source base: published prompt-relay `6301363eb9b279d9675bd642a3bde1a87193dee5`.

The standalone adapter has no scheduler and defaults to `enabled:false`. It accepts only a strict configuration and trusted per-target eligibility observations: `idle`, at least 90 idle minutes, and open work. Unknown and approval-wait states refuse. Claude calls use the published prompt-relay with explicit `peer-file` provenance; Codex calls use the supported argv-only `codex queue --thread … --message …` interface with the same JSON provenance envelope followed by the unchanged body. Subprocesses use a 10-second timeout and bounded output. Submission acceptance is reported as `unobserved`, never as recipient or turn delivery.

Local and remote validation are appended after execution.

Local validation: `node tools/wake-adapter.test.mjs` passed 5 tests. Final remote validation: `nix build --max-jobs 0 --no-link --option substituters https://cache.nixos.org/ --option connect-timeout 5 '.#checks.x86_64-linux.wake-adapter-fixtures'` completed on Prometheus with exit 0 and returned `primary-wake-adapter-fixtures`.
