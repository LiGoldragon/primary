# Resume capacity assessment

Method: query the realized candidate with `nix path-info --json --json-format 1 --recursive --sigs --no-pretty /nix/store/jz6mg0qlm3w2h2h5jxwldccncjgcz22j-nixos-system-zeus-26.11.20260813.0e251e2`; derive the exact closure-path list and query those paths in one read-only batch through `nix path-info --store ssh-ng://root@192.168.18.95 --stdin --json --json-format 1 --sigs --no-pretty`; read the prior same-flow metadata witness; and read `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs` lines 5209–5223.

The expected candidate is not currently present in its actual local store. The direct query returns:

```text
don't know how to build these paths:
  /nix/store/jz6mg0qlm3w2h2h5jxwldccncjgcz22j-nixos-system-zeus-26.11.20260813.0e251e2
error: path '...' is not valid
```

Because the local root is unavailable, no current closure path list exists to submit to the remote store, and the remote valid-path/missing-path byte and count comparison is not measurable. The attempted batch therefore produced no validity rows; this is a missing-input result, not evidence that Zeus has zero valid candidate dependencies.

Earlier in this flow, while the candidate was present locally, read-only metadata measured 3,579 recursive paths and a human-readable recursive NAR size of 34.5 GiB. That prior coarse witness is not an exact byte total and is not a current-store witness. The failed deployment's parent record separately measured at least 1,932,511,150 transferred bytes and about 13 GiB of target free-space consumption; no path-level relation between those values and valid destination registrations is established.

The local Lojix source documents the copy as idempotent when the closure already exists on the target: it invokes `nix copy --substitute-on-destination --to <target> <closure>`, and Nix can skip destination-valid paths while sending paths that are absent. This semantic statement does not make incomplete or unregistered transfer residue reusable.

No copy, retry, build, hash verification, GC, deletion, signing, activation, or reboot was performed.

