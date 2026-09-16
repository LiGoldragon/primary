# Daemon dispatch record — ready only

This records the supported shape for the successor dispatch when the living
explicitly says **Claude**. It is not an instruction to launch now.

The observed prior dispatch used daemon mode `prompt` with these launch fields:

```text
--name primary-claude-pending
--remote-control primary-claude-pending
--model fable
--append-system-prompt-file <package>/system-prompt.md
-- <package>/user-prompt.md contents
```

The daemon, rather than a direct foreground command, is the supported route.
It must mint and record the session id, roster entry, bridge state, cgroup, and
launch receipt. Do not supply or claim a fixed successor identity before that
receipt. The direct CLI help observed on 2026-09-16 supports `--bg`, `--name`,
`--remote-control`, `--model`, and `--append-system-prompt-file`; the retained
launch record is the filesystem receipt that the daemon accepted this shape for
the 840e42 launch.

After an authorized dispatch, verify before declaring success:

1. daemon session id and roster entry;
2. remote-control bridge and per-flow scope/cgroup;
3. both prompt hashes against `manifest.json`;
4. successor's claimed identity and its depth-one reading of 840e42;
5. a real paired-report route to Codex `cf7879`.

No dispatch has occurred while preparing this record.
