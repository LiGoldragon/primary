# Chroma projection audit

Read-only audit of Chroma and chroma-emacs at the approved revisions against
the accepted resident Emacs projection design. Product repositories, GitHub,
deployment, and runtime state were not changed.

2026-08-23 — Reacquired the accepted Chroma–Emacs design and the parent
realization approval, then resolved the exact origin revisions:
Chroma `d6cea6bcb41fb75d8a268cd46c66120eb694562c` and chroma-emacs
`d432f95db5837e685e32afbf5790060fb15a3703`.

2026-08-23 — Read the server wire, root, persistence, migration, projection,
owner-watcher, client, documentation, and test paths. Both repositories were
clean. Direct Cargo, ERT, private-bus, and flake-evaluation witnesses passed.

2026-08-23 — The wire and active Emacs-removal shape match. The audit found an
unfiltered server owner-loss signal path, stale failed-report validation that
is skipped, and a saturating revision edge at `u64::MAX`. Runtime proof is
incomplete: Chroma's bus test exports a test-only interface rather than the
production `ThemeDbusService`, and the default Chroma Nix check does not force
a private session bus or daemon restart.

2026-08-23 — Handoff report is preserved in `reports/chromaProjectionAudit.md`
with command witnesses in `witnesses/chromaProjectionAudit.md`. No commit or
push was made while implementation subflows remain active.

2026-08-23 — Re-audited corrected Chroma origin
`9248420ef8ccff005aa1a5e0e5d8e5505755269e`. Checked owner filtering, stale
failure bounds, checked revision exhaustion, real `ChromaRoot` plus
`ThemeDbusService` private-bus behavior, second owner, full snapshot, owner
loss, and service re-export. The three prior implementation defects are
corrected and the explicit durable witness passed. The remaining proof gap is
that service restart reuses the same root/state actor rather than recreating a
process and reopening persisted redb; stale-invalid and both same-current
status directions remain reducer-level coverage. Correction details are
appended to the report and witnesses.
