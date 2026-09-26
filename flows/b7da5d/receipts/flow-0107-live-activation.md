# Flow 0.10.7 reversible local activation

- Canonical source: `8df890ba1bc34a9bd575e75ab4796b4e0dc7b0fd`.
- The local no-builder build closure was independently checked: both `flow` and `flow-nexus` answered `0.10.7`.
- Pre-switch unit: active Flow 0.10.5, zero restarts, profile priority 4, and a user-unit override selecting the 0.10.5 closure. Its exact override is retained beside this receipt.
- Local profile priority 4 now selects the 0.10.7 closure. The override was atomically replaced, the user manager reloaded, and the service restarted. Rollback is bounded to restoring the retained override, re-adding the retained 0.10.5 closure at priority 4, reloading, and restarting.
- Post-switch: active/running, zero restarts, effective `ExecStart` selects 0.10.7, and both profile binaries answer 0.10.7.
- `List.{}` answered after restart. No prompt was sent. The focused existing bound Codex target `5f38bc` resolved `Available` with an endpoint state `Ready` and a live Flow route; this replaced the pre-switch parked/unavailable result.
- The journal has one non-fatal startup warning that legacy ambiguous launch attempts are unreadable from the persisted Sema table. The service remained active, with no restart, and ordinary List/Resolve calls succeeded.
