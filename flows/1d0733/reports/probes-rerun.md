# Probes rerun: ethos-zero c2653d

## Build

Command: `nix run "github:LiGoldragon/ethos-zero/c2653d"`

Host: prometheus

## Results

| Probe | Status |
|-------|--------|
| golden.ethos | MATCH |
| fnmem.ethos | MATCH |
| s2.ethos | MATCH |
| m2.ethos | MATCH |

**Summary:** 4 matches, 0 mismatches.

All probes from the audit (flows/d5df1d) run successfully against the binary built at c2653d. Each generated Rust file matches the expected observations.
