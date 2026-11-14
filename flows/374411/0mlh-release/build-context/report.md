# 0mlh immutable Home build context

Prepared only; no evaluation or build ran.

- Consumer: CriomOS `1d3cee5405ad30ad02d50edaf8f70376e7eee930`.
- Home override: `4dbaa059836a1328f567c5ca0db04be6885898f1`.
- Selector: `homeConfigurations.li.activationPackage`.
- Exact deployment-543 `horizon`, `system`, and `secrets` generated directories were each copied once from the local Lojix source to `/tmp/offload/374411-0mlh-generated-inputs/` on canonical Prometheus. The private workspace and each input directory are owned by `li:users`, mode 700. Rsync suppressed file output; secret content was neither read into evidence nor printed.
- Source and builder `nix hash path --type sha256 --sri` results are byte-identical; `source-builder-hash.diff` is empty. They match retained 543 SRIs: horizon `sha256-9n6IJ+TIk7SkREyhSXVz/ZP/hS3iYc+gVdPG5g0rDq8=`, system `sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=`, secrets `sha256-UXfrzp0B+uwSwvYhoW8v9Hg9tTtsJire8YmSf4h8SDQ=`.
- `build-command.sh` is the executable ouranos-side orchestrator. It connects as `li@prometheus.goldragon.criome`, rechecks all three SRIs, and runs the build locally on Prometheus with `--refresh --no-link --print-out-paths` and the four exact overrides. Direct `nix-ssh` interactive SSH was refused; `li` is the verified canonical evaluator and owns the private inputs. Because evaluation/build executes on Prometheus itself, the script does not route back through ouranos `/etc/nix/machines`.
- `bash -n` passed. The installed `nix build --help` confirms `--refresh`, `--no-link`, and `--print-out-paths`.

Final command SHA-256: `7ca035561199c197fea7272a8be355bbc65911efc242d0796d6e7894c48e546b`.
