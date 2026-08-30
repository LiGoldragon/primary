# Canonical Lojix proposal migration and Wispr activation

Remembered: 01a05209 — depth 1. Wispr packaging and declarative Home/CriomOS integration are complete; producer `9e991e50…`, Home `6201c493…`, and CriomOS `e3c9d714…` carry the Status-window transparency and keyboard-class active-seat `uaccess` repairs. The immutable Ouranos target realized, but Lojix 0.19.2 rejected deployments because its legacy ClusterProposal reader accepts only stale `goldragon/datom.dotos`, while canonical goldragon authority is `proposal.datomic`. No compatible canonical proposal source was deployable, and adding a legacy duplicate was explicitly rejected as backward compatibility.

Ruled work: migrate deployed Lojix to consume canonical `goldragon/proposal.datomic` with no compatibility duplicate; prove and deploy that migration; then activate CriomOS `e3c9d714` and verify the Wispr shortcut and Status-window repairs live. Related bead `CriomOS-home home-y3l` is already closed.

No psyche record: the machine prompt is an execution instruction.

Current state: migration implementation, independent audit, and CriomOS activation/live verification are delegated to active subflows. Flow index registration is pending because `flows/index.md` is held by Lock 19 for flow 01a0433a.
