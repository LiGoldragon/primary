# Flow 0.12.1 reversible local activation

- Canonical source `fe709c7e20efc2dc5f4c7bac5969f3be57c610b4` was fetched from canonical main. A local build with remote builders disabled produced the 0.12.1 closure; both binaries answered 0.12.1.
- Before switch, the user unit was active on the retained 0.10.7 priority-4 profile and override. Its override is retained beside this receipt for rollback.
- The priority-4 profile and override were atomically advanced to 0.12.1, followed by daemon reload and service restart. Post-switch service is active/running with zero restarts and effective 0.12.1 `ExecStart`.
- Startup emitted `LaunchAttemptMigrated` for one `BeforeSystemPromptBundle` legacy row. It did not quarantine a row. `List.{}` returned 13 rows; `88475f` is directly listed `Active`. `5f38bc` remains unchanged and was not assigned a role.
- A guessed `LaunchStatus.88475f` query was rejected as `UnknownLaunchRequest`; it was not treated as a status witness. No Observe, Start, or prompt was sent to a production flow.
- Rollback is bounded to restoring the saved 0.10.7 override and profile closure, daemon reload, then user-service restart.
