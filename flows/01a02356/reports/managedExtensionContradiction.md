# VSCodium managed-extension contradiction

The witnessed pre-repair state split across owners and representations:

```text
Home/stable ─────────────── Claude 2.1.235
desired versioned link ─── absent
manifest ────────────────── 2.1.223 → old store output named 2.1.220
                               └─ package identifies 2.1.223
existing versioned link ─── 2.1.223 → a different output
GC root ─────────────────── retains the manifest target
```

The durable repair is owner-authenticated Nix reconciliation. Its focused
lifecycle check exited 0, including a three-version fixture, repeat/idempotence,
and preservation of unmanaged registry/settings. A bounded local fallback
completed the Home closure build after Prometheus cache and remote-builder SSH
timeouts. Nix-built activation-refresh succeeded and live state converged to
Claude 2.1.235. `codium --version` exited 0 with `1.126.04524`; normal
real-profile GUI launch exited 0 (PID 451570, parent user-manager PID 2305);
`codium --status` exited 0. The registry reports Claude 2.1.235 and ChatGPT
26.5814.41407.

The temporary isolated no-extension recovery window remains live by choice at
`/tmp/criomos-codium-recovery.6UDf73Xe`, alongside the normal GUI, to avoid
closing user-visible work. The backup is at
`/home/li/.local/state/criomos/vscodium-claude/recovery-20260821T101900Z`.

The exact historical event that created the contradiction remains unknown.

## Sources

- `sessions/realization/2026-08-21T100106.md` (legacy session record; claims
  carried into this report)
- `flows/01a02356/log.md` (this flow's summary)
- `flows/01a02356` (migration path and report)
