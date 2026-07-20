---
name: pi-extension-updates
description: 'Pi extension updates rules.'
---

# Pi internals

- Treat installed Pi files as read-only evidence.
- Change Pi through its declarative source and deployment owner.
- Do not use internals to bypass role boundaries.

## Pi extension updates

- Reconcile each local extension change with upstream evidence.
- Change the source and declarative package owner, not installed output.
- Push a producer before updating its consumer pin.
- Verify the activated revision.
