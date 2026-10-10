# Flow bc3530 — the flow launch protocol, and a report proof over the intended network

Opened 2026-09-09. Claude main flow, own lane claimed with `flow-id claude`.

Source provenance: launched by a parent Claude Code session. The parent session
identity lives only in the gitignored claim marker `flows/.bc3530.flow-id`; no
parent transcript, prompt, or thread identifier is copied into this lane. This
flow is an independent main flow, not a subflow of its source: it holds its own
FLOW_ID and writes only here.

Facts carried: none from a parent transcript. Public starting references only —
`flows/564f55/log.md`, `flows/564f55/reports/codexLaunch.md`,
`flows/219191/log.md`, and the two Plannotator Nix files in CriomOS-home.

## Outcome sought

A reusable, open-source protocol with two distinct relations:

- Delegation — a subflow, same FLOW_ID, same lane.
- Succession — an independent main flow, new FLOW_ID, carrying source provenance.

Privacy and security domain inherit across either relation. Source material moves
as a capability-scoped reference with bounded transcript search, never as full
prompt replay in a public log. The private capability must be enforced by the OS
or runtime and inherited deliberately by a child, covering transcripts, cache,
logs, and temporary routing; same-UID with chmod, and a private Git branch, are
both insufficient.

Alongside it, a generic report proof over the Plannotator report subsystem with
synthetic data, reachable over the intended network, authenticated for private
artifacts, with anonymous access to a private artifact proved denied.

## Opening audit

2026-09-09. Six read-only subflows audited, before any change: the flow system
and its launch conventions, the psyche's rulings, the Plannotator network and
report subsystem, network ingress, OS private-capability mechanisms, and
repository coordination state.

Established by the flow-system audit:

- `flow-id` lives in `/git/github.com/LiGoldragon/harness`. It claims a lane and
  writes `flows/.<alias>.flow-id`, a `key=value` marker holding harness kind,
  session identity, alias, and UUID version. It records no parent, source, or
  launching flow. There is no field for it.
- The marker and its lock are gitignored; the alias-named lane and its authored
  contents are tracked. A private identity and a public record are therefore
  already separated on disk. Provenance belongs on the private side of that line.
- `harness/src/launch.rs` spawns a child harness through `SessionLauncher`, in a
  PTY-owning session directory. Its request carries harness kind, agent identity,
  and initial prompt, and no flow identity or parent. It is not wired to
  `flow-id`. This is the seam where succession is implemented.
- The launch convention today is prose in one lane: `flows/1a6ca4/log.md` records
  launching Codex main flows that then claimed their own lanes. The parent-child
  link survives only as that prose; the children's own logs do not name it.
- `Vision/flowNexus.md` is approved vision: a Nexus sets up and starts a model
  flow, deciding working directory, system prompt, training files, and prompt.
  This protocol extends toward that, and must not become a second one.
- `Vision/sources/<topic>.md` is today the only structured flow provenance in the
  repository: `<originating flow short id> <topic>` per line. Succession
  provenance should read like it.
- `flows/564f55/reports/codexLaunch.md` left open whether a launched flow claims
  its own lane or writes into the parent's. That question is answered here: it
  depends on the relation, and the two relations are now named.

Established by the coordination audit: primary is jj-managed on `main`;
Orchestrate is the live lock nexus and flow 542442 currently holds locks across
CriomOS, CriomOS-home, and orchestrate; bead `primary-y61` is open and blocked on
the phone ingress question this flow takes up.

## Corrections to the opening brief

- `reports/codexLaunch.md` does not exist at the repository root. The file is
  `flows/564f55/reports/codexLaunch.md`.
- `CLAUDE.md` and `NON_MANAGEMENT_AGENTS.md` name `manifests/*.dotos` as the
  identity source. No such directory exists; identity is `Curriculum/roles.datom`.

## What the audits established

2026-09-09. All six landed. The three that changed the design:

Psyche. Privacy was already ruled on, twice in one sitting on 2026-08-03, and
ruled *out* of any record's shape: privacy belongs to a different component in a
different environment, and what survived is the privacy silo, a separate log. A
per-record privacy classification would re-litigate a settled ruling. Source
transport was also already ruled: there is no handoff file, the flow reads its
previous flow, push is inverted to pull, and `Vision/remembering.md` already
bounds that reading by depth. Bounded transcript search therefore exists; it is
called remembering, and this work extends it rather than adding a second
mechanism. The reference itself must stay plain and directly resolvable, so the
capability gates access and never obscures the name. `successor flow` is
already the psyche's own word for a fresh context continuing a prior one.

Two premises in the opening brief have no psyche record: that chmod, same UID,
and a private Git branch are insufficient. That claim exists only in
agent-authored pre-reset doctrine. It is treated here as the living's current
word, not as an established ruling.

The opening brief is not logged as psyche. A ruling holds that machine-generated
or pasted content is never recorded as psyche, and the brief reads as
machine-composed.

Operating system. Live probes, not documentation. A mount namespace does not
hide anything from a same-UID peer: `/proc/<pid>/root` is readable, and `setns`
into a user namespace whose owner UID equals the caller's succeeds. Namespace
privacy is convention, of the same rank as chmod. `PR_SET_DUMPABLE=0` closes
`/proc/<pid>/{root,fd,ns}` and ptrace, but resets on every `execve`. Kernel
keyring possession is the one unforgeable capability present: inherited across
fork and exec, denied to a same-UID process on a different session keyring even
when handed the key id, and undiscoverable by description. Landlock is at ABI 9,
enforcing and inherited, and nothing on this machine uses it. systemd user
credentials fail the rule outright. Today every harness writes transcripts,
caches, and logs under one UID with many directories world-readable, and nothing
distinguishes one flow's material from another's.

Plannotator. There is no Planeter; the name is unbound. The report seam is a
pure `(snapshot) -> HTML` boundary over a versioned document, served through an
injectable store, with public synthetic fixtures under a never-delete promise,
and a public-or-private axis already present. What it lacks is read
authorization: there is no principal anywhere to hang one on. That gap is where
this flow's capability belongs. Remote mode binds `0.0.0.0` with no
authentication, no CORS, and no Host validation, while offering arbitrary file
read through an extension-only path check and file write through upload. It must
stay on loopback and be gated at the transport.

Network. The recorded blocker is real and there is a second one beneath it. The
tailnet has never come up: the client rejects the control server's self-signed
certificate because nothing installs it as a trust anchor. Serve and Funnel are
genuinely unimplemented upstream at the newest release, with no ETA, so no
upgrade helps. But Serve is not required: binding the tailnet interface directly
and relaying loopback sidesteps it. Present and working today are keys-only SSH
with no password path, an active overlay network, and sops-nix with a
file-delivered bearer-token precedent. Absent entirely are any reverse proxy,
any certificate automation, and any HTTP authentication.

## Open, and the living's to decide

- Whether the protocol and the report proof may be published, and where. Every
  public repository in this history was authorized one at a time.
- The access default for a report: public, owner-only, or per-report. Logged as
  an open question three times across earlier flows and never answered.
- Whether to fix the certificate trust anchor in the system source, and whether
  to move to a hosted control plane. The second is what bead `primary-y61` has
  been blocked on since flow 219191.
- The gitlink pointers under `flows/da223f/joint.0jZ7PT` remain dirty. The
  residue was committed and pushed inside both nested repositories, but jj
  ignores gitlinks and cannot record the pointer update, and raw git on primary
  was not authorized.
