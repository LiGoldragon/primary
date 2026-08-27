# Codex working directory failure

The living reports that Codex works from `~/` regardless of where it is started and requests an immediate repair followed by the proven cause. The living then identified `--remote` as the apparent trigger and ruled that it must preserve the caller's directory; a fallback may be `~/primary` but must not be hardwired into OS or home code. The ordinary launcher must also default to `--sandbox danger-full-access --ask-for-approval=never`.

Open: establish a direct witness of the failure, repair the responsible configuration or code, and test launch behavior from more than one directory.
