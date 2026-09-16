# Claude successor package v5

This is an unlaunched package for the efa157 successor. `system-prompt.md` is
the complete v4 source-body packet, copied as a file so Claude's supported
`--system-prompt-file` replaces the harness base prompt rather than appending
to it. A copied body is evidence of package content, not a native skill-loader
receipt.

`user-prompt.md` is the first bounded order. The launcher is dry-run by
default, uses structured arguments and `/dev/null` stdin, and needs `--launch`
only after the living gives the efa157 launch word. It does not read a
credential, install a service, or start a model in dry-run mode.

The inherited v4 source receipt is retained in `v4-source-manifest.tsv`. New
artifact hashes are in `artifact-sha256sums.txt`; verify with
`sha256sum -c artifact-sha256sums.txt` before any launch. The complete skill
bodies are retained in `system-prompt.md`; this package does not claim native
loader invocation.
