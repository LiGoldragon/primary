# Fresh-Session Handover — Persistent Spirit Mirror (corrected architecture reset)

## North star (the corrected vision — from the psyche, just now)

Mirroring is **not** a service and **not** a new component. It is **how Spirit
itself operates**, riding the **sema-engine's built-in mirroring capability**.
Hold this as the fresh session's orienting truth; earlier work drifted off it and
the psyche reset the lane.

The intended data flow for one change:

1. A **Spirit record** is created on one host.
2. The **router** carries it across the network to the *other host's* router.
3. That peer router hands it to the **right component**.
4. **Criome authenticates** it on arrival.
5. It becomes a **Spirit record** on the peer.

Use **only the components that already exist — spirit, criome, router** — extended
as needed. **No other components**: no bolt-on daemons, no separate "mirror"
component or daemon.

The larger aim, beyond backup: every instance of each component (spirit first,
others later) across all nodes **converges to the same state**. Open Spirit on any
machine and it is the same; changes propagate (eventually bidirectionally). Treat
this as durable psyche intent worth capturing properly, not a throwaway remark.

## Mandate for this session (state this to the psyche up front)

- This is a **questionnaire-first orchestration lane**. Interview the psyche
  heavily with focused questions — **one focus per turn** — to draw out the full
  vision and resolve the unknowns **before any implementation**. Sequence:
  alignment gate first, then method gate, then implement. The psyche asked for this
  reset precisely because implementation ran ahead of the vision.
- **Plain language only, no jargon.** The psyche reads only the final answer of each
  turn, not the agent chatter. Prior sessions lost him in identifiers, revision
  hashes, and protocol terms. Translate everything to plain terms; surface only
  decisions and blockers.

## Settled, reusable facts (confirmed on the metal)

- **Two standing VMs on `prometheus`**: `mirror-alpha` (node A, address `5::7`) and
  `mirror-beta` (node B, address `5::8`). They are first-class SSH goldragon-cluster
  nodes (loginable, keys-only), right-sized to **2 cores / 4 GiB RAM / 8 GiB disk**,
  authored in the **public** `goldragon` cluster data.
- **Reboot-persistent.** prometheus runs system-profile **generation 51**, promoted
  to the bootloader default by hand (`nix-env --set` + `switch-to-configuration
  boot`), so the guests, guest networking, firewall, SSH, and right-sizing survive a
  reboot. Landed revs behind gen 51: **CriomOS main `3aa4780971e4`**, **goldragon
  main `2fe644be`**. (Note: lojix's own deployment records still show older gens
  because gen 51 was promoted by hand, not via a lojix Switch — live truth is gen 51.)
- **The two guests reach each other on the metal.** Guest-originated A→B ping and TCP
  over the `vmt` tap succeeded (`5::7` ↔ `5::8`), plus host↔guest both ways. The
  guest-networking fix (`/128` host routes + `fe80::1` gateway + `vmt*` firewall
  rules) is live and verified.
- **Criome Stage-A (1-of-1) BLS-identity authentication works.** Each node runs its
  own criome with its own master key and identity; a head is authorized deterministically
  with no human in the loop. Stage-B multi-node quorum is unbuilt and **not needed**
  here.
- **The sema-engine's content-addressed mirroring lands data intact.** A live A→B
  proof advanced node A's Spirit head and the identical head digest
  (`38b6de6a…feecf53`) appeared on node B, verified at append time. This is the
  mechanism the north star names.
- **`spirit --features mirror-shipper` compiles clean on prometheus** — no fenix-FOD
  build problem. It lives on the pushed spirit feature bookmark
  **`mirror-shipper-daemon-output`** @ `aff00c988634` (spirit main `d20982c4`,
  untouched); it adds a `mirror-shipper-daemon` build output.
- **Productionization note:** a guest firewall must open **port 7474** on the tap for
  a receiver (currently opened only on `tailscale0`; the guests talk over `vmt`).

## What to DISCARD / reconsider (make this explicit to the psyche)

- The live proof used a **direct spirit → mirror-shipper → mirror-daemon** path with
  a **separate `mirror` component**, and the **router was not in the path**. Per the
  corrected vision this is **not** the intended architecture. Do not anchor on it.
- The prior planning conclusion (see WeavePlan "B1 resolution") treated that direct
  mirror-component path as *the* slice and **deferred** the router-mediated path. The
  corrected vision **flips this**: the **router-mediated** path is the intended one,
  and it is currently **net-new** work — today the router fans out *typed references*,
  not record bodies, and no standing router daemon carries a body host-to-host.
- **Cleanup item:** ad-hoc proof daemons (criome, spirit-shipper on A; mirror on B)
  and a live 7474 firewall rule are left running on the guests. They are fully
  reversible: restarting the `microvm@mirror-alpha` / `microvm@mirror-beta` units
  returns each guest to clean gen 51.
- The production-data copy (read-only seed of live Spirit from ouranos) was
  intentionally deferred; not part of the corrected architecture question.

## Open questions the questionnaire must resolve (seeds — expand as you read)

- How does Spirit's sema-engine mirror stream feed **into the router**, and how does
  the peer router route an arriving record to the **right component**, then into
  **Criome auth**, then into a Spirit record? (This is the net-new router work.)
- Is sema-engine mirroring the **sole** mechanism, with **no mirror component at all**?
- Where does **Criome auth** sit in the arrival path, and what is the intended
  per-request auth posture? (Today's tap/tailnet-ACL + AutoApprove trust is only a
  stopgap; the psyche's strict prior stance was authenticate-ingress-then-ship.)
- **Bidirectional / multi-master convergence and conflict model** — two hosts editing
  the same state while disconnected, then reconciling.
- **Which components beyond spirit**, and how general must the one mechanism be (must
  it serve every component's sema-engine, not just Spirit's)?
- How is "open Spirit on the other machine and see the same live state" realized
  natively — applying an arrived record into the **running** Spirit, not just landing
  bytes in a store?
- **Deployment as native node config** (no new components), reboot-survivable; and
  **sequencing**: one-directional first vs straight to bidirectional; spirit-first vs
  all components.

## Evidence pointers (all under `agent-outputs/PersistentSpiritMirror/`)

- `Scout-SituationalMap.md` — ground-truth map of the components, the horizon/cluster
  data path, the criome auth flow, and the "router fans references, not bodies" limit.
- `TrackerWeaver-WeavePlan.md` — prior bead graph (epic `primary-1e6b`) and the now-
  **superseded** direct-mirror-path conclusion; read for the router-path notes
  (`primary-1e6b.8`) which are closest to the corrected vision.
- `OperatingSystemImplementer-MirrorStandUpFindings.md` — productionization gap
  analysis: no production spirit/criome node modules, the `mirror-shipper` feature
  gap, the mirror→spirit hop is not autonomous, and the horizon data carries no
  mirror-role atom.
- `OperatingSystemImplementer-LiveMirrorProof.md` — the live A→B proof, the identical
  head digest, the 7474 firewall discovery, and the exact reversible teardown.
- `OperatingSystemImplementer-LandAndBuildEvidence.md` — the full VM stand-up / deploy
  history: guest-networking fix, home-inclusion fix, right-sizing, and the gen-51
  promotion. (Its final one-line "Revs now" is stale; trust gen 51 =
  CriomOS `3aa4780971e4` + goldragon `2fe644be`.)

## Constraints carried

- No `/nix/store` filesystem search. On primary, work on `main` with `jj`; no raw
  `git`. NOTA records are positional. Keep private/secret material out of public
  surfaces (goldragon is public; digests and node addresses above are safe).
- Do **not** implement in this lane until the alignment and method gates pass.
