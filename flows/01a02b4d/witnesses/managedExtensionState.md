# VSCodium managed-extension state

Method: probe `for p in /home/li/.vscode-oss/extensions/anthropic.claude-code /home/li/.vscode-oss/extensions/anthropic.claude-code-2.1.235-linux-x64 /home/li/.local/state/criomos/vscodium-claude/gcroots/anthropic.claude-code-2.1.235-linux-x64 /home/li/.local/state/criomos/vscodium-claude/manifest /home/li/.local/state/criomos/vscodium-claude/extensions-immutable.registry.json; do ls -ld --time-style=full-iso "$p"; readlink "$p"; realpath "$p"; stat -c 'type=%F mode=%A size=%s mtime=%y inode=%i' "$p"; done`.

Method: probe `jq -c '{name,publisher,version,engines,extensionKind}' /home/li/.vscode-oss/extensions/anthropic.claude-code/package.json`.

Method: probe a registry loop over the explicit normal-state registry `/home/li/.local/state/criomos/vscodium-claude/extensions-immutable.registry.json` and archived recovery registry `/home/li/.local/state/criomos/vscodium-claude/recovery-20260821T101900Z/extensions-immutable.registry.json`, using `jq 'length'` and selecting the records for `anthropic.claude-code`, `openai.chatgpt`, and `visualjj.visualjj`.

Method: probe `stat -c 'size=%s mtime=%y mode=%A' /tmp/criomos-codium-recovery.6UDf73Xe/extensions/extensions.json`; a `jq` conditional array summary on that file; `ls -ld --time-style=full-iso /tmp/criomos-codium-recovery.6UDf73Xe`; and `find /tmp/criomos-codium-recovery.6UDf73Xe -maxdepth 2 -printf '%y %p -> %l\n' | sort | head -200`.

Method: probe `command -v codium`; `realpath "$(command -v codium)"`; `timeout 20s codium --version`; `timeout 20s codium --status`; and `timeout 20s codium --list-extensions --show-versions`.

Method: probe `ps -eo pid=,ppid=,user=,stat=,etime=,args= | awk '$6 ~ /\/codium$/ && $0 !~ /--type=/ {print}'`.

Method: probe a direct bounded `/proc/[0-9]*/cmdline` scan that read each process's first argv and matched Codium commands and `/tmp/criomos-codium-recovery.6UDf73Xe`; result `NO_MATCHING_RECOVERY_CODIUM_PROCESS`.

Method: probe `readlink -e /home/li/.nix-profile/bin/codium`; `sed -n '1,220p' /nix/store/khz4kl4md42vlk7rmhb81m4hm52swdvl-vscodium-casual-managed/bin/codium`.

The probe was anchored at `2026-08-22T23:13:56+02:00` (Europe/Madrid). The observations below are the probe results; no further Codium command was run for this record.

## Observations

- The desired link `/home/li/.vscode-oss/extensions/anthropic.claude-code` and the versioned link `/home/li/.vscode-oss/extensions/anthropic.claude-code-2.1.235-linux-x64` both resolve to the Nix store package for Claude Code 2.1.235.
- The managed-extension manifest and the Claude GC-root link target that same 2.1.235 package. The installed package metadata reports Claude Code version 2.1.235.
- The immutable registry contains 9 entries. Its relevant entries include `anthropic.claude-code` at 2.1.235 and `openai.chatgpt` at 26.5814.41407. The registry content was unchanged by the later wrapper invocation.
- `codium --version` exited 0 and reported `1.126.04524`. `codium --status` exited 0 with no output. `codium --list-extensions --show-versions` listed the current extension versions.
- Around local `23:17:04`, the wrapper execution associated with the list-extensions probe refreshed lifecycle, lock, GC-root, and manifest mtimes. Their content remained unchanged. This is a temporal observation, not proof that the list command caused the refresh.
- The normal GUI Codium process remains PID `451570`, under user-manager PID `2305`.
- The bounded process scan found no process matching the recovery path: `NO_MATCHING_RECOVERY_CODIUM_PROCESS`.
- `/tmp/criomos-codium-recovery.6UDf73Xe` still exists. Its `extensions/extensions.json` contains an empty array (`[]`), and its Session Storage/`LOCK` state is stale. No recovery cleanup was performed.
- The archived recovery records retain the earlier contradictory state described by flow `01a02356`; they are historical records, not the current managed-extension targets.

## Unknowns

- The historical event that produced the earlier contradiction remains unknown.
- Runtime extension-host activity was not proven by these observations.
- The timestamp refresh has no established causal explanation beyond its temporal association with the wrapper invocation.
- Whether the retained recovery directory is safe or authorized to remove remains unresolved; this flow performed no cleanup.
