# Release package mutation analysis

The fixed release archive has one `opencode` member, 167,639,168 bytes. The first Nix package installed a 167,640,032-byte result. Its build log records RPATH shrinking, `strip -S -p`, and `autoPatchelfHook` setting an ELF interpreter; its ELF program-header count changed from nine to ten and its `.bun` section moved by 4096 bytes. The reported `1.3.14` is therefore not usable as evidence about upstream release labeling while that package path is in use.

`release-package.nix` now stores the archive member under `libexec` with `dontStrip` and `dontPatchELF`, then runs it through `buildFHSEnv`. This avoids the NixOS host loader stub while preserving the embedded Bun payload as archived. It is a packaging correction awaiting separate evaluation, remote-only build, and version evidence; it makes no claim about the upstream asset or source-tag correspondence.
