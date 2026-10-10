# Handover bead acquisition

## Psyche ruling — 2026-08-01

There was no agent text answered.

A workspace handover bead holds the actual handover content. It is a transfer
envelope, not the durable goal and not a proxy for implementation completion.

The receiving session acquires the handover by reading and claiming it,
verifying the existing goal beads and creating any missing goals it decides are
needed in their owning repositories, then closing the handover bead with the
acquisition evidence. The handover is closed at transfer, while each goal bead
remains open until its own outcome is proven.

Goal beads may predate the handover. They live in other repositories when those
repositories own the work. Cross-repository goal identities are named in the
handover because Beads dependencies do not cross databases.
