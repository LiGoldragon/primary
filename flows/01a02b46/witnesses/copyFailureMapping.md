# Copy failure mapping

Method: code read `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs` at lines 3689–3724, 4385–4398, 5200–5224, and 5920–6021; probe `journalctl --no-pager -o short-precise -u lojix-daemon.service --since '2026-08-23 00:00:00' --until '2026-08-23 01:01:00'`; query `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon zeus None)'`; and run `lojix-inspect-store '(InspectStore /var/lib/lojix/lojix.sema)'`.

The source constructs the copy as:

```text
nix copy --substitute-on-destination --to <requested-store-uri> <closure-path>
```

`NixCommand::run` captures stdout and stderr. A non-zero command returns a detail containing the complete argument vector, exit status, and trimmed stderr. A timeout returns a detail naming the timeout and process-group termination. `run_copy_closure` wraps either detail in `EffectFailure.string`.

`fail_pipeline` logs only `failure.effect_stage`, maps every `CopyClosure` failure to `BuilderUnreachable`, and terminalizes the deployment with only the stage and mapped reason. It does not log, persist, or expose `failure.string`. Therefore the exact `nix copy` exit status and stderr cannot be recovered from the active daemon's durable deployment record or its journal after the fact.

The service journal retained only:

```text
Aug 23 00:13:26.001872 ... lojix deploy pipeline reached a terminal state
Aug 23 01:00:27.674188 ... lojix deploy pipeline effect failed at CopyClosure
Aug 23 01:00:27.681950 ... lojix deploy pipeline reached a terminal state
```

The node query returned deployment 30 as `Failed.(CopyClosure BuilderUnreachable)` alongside successful deployments 28 and 29. The read-only store inspector could not acquire the running redb lock (`Database already open. Cannot acquire lock.`); this is an inspection-lock limitation, not evidence of store corruption. No full store verification was run.

The source mapping is a witness for loss of diagnostic detail, not a witness for the underlying copy cause.

