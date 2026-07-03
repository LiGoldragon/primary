# Scout — CriomOS Deployment-Agnostic Redesign Proposal

Audit of hard-wired deployment-specific code in the CriomOS OS layer, plus a
proposal (proposal only — not implemented) for decoupling deployment specifics
from CriomOS. Read-only over code. Backing psyche directive (2026-07-03):

> "if that means something was hard-wired to do this in criomos, then it's
> wrong; criomos should be deployment agnostic. better would be to just make it
> a user service. if an agent goes there, he should audit to look for and
> propose a way to redesign any deployment-specific code."

Grounding: `agent-outputs/LojixDeployAuthMap/Scout-SituationalMap.md`.
Tracking bead: `primary-gss3`. Related epic: `primary-om4g` (criome auth core).

## Scope And Boundaries

- Audited: the CriomOS repo at `/git/github.com/LiGoldragon/CriomOS` (the OS
  layer). The deploy tool `lojix` lives in a **separate** repo
  (`/git/github.com/LiGoldragon/lojix`); its source is referenced for context,
  not audited as "CriomOS code."
- Read-only over all code/config. I did **not** edit any `.nix`, run `nix`,
  run `lojix`, or touch the concurrent worker's fix. The other worker owns the
  code/config change (guardian prompt + safe local-activate fix, possibly
  converting lojix to a user service).
- I own two written surfaces only, both claimed/exempt: the CriomOS
  `ARCHITECTURE.md` direction (claimed via Orchestrate under the `scout` lane)
  and this proposal doc (report in the active lane's own directory).

## 1 · ARCHITECTURE Direction Recorded

Added a subsection **"Deployment-agnostic OS layer"** to
`/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md` (inserted just before
"### Direction: the LojixOS split"). It states, 100% backed by the psyche
directive above:

- CriomOS is deployment-agnostic; hard-wiring a deployment specific (host, user,
  system-vs-user service, remote auth) into a CriomOS module is a defect.
- This generalizes the pre-existing network-neutral rule (node names as
  projected data, `ARCHITECTURE.md:49-53`, `:200-202`) from node names to every
  deployment fact.
- The deploy orchestrator (Lojix) runs as the operator's **user-level service**,
  not a system service pinned to a fixed user; its unattended identity and
  remote-deploy credentials are a deployment concern owned outside the OS module.
- Test-seed constraints: no operator-username literal, no cluster/node/trust
  deploy-target constant, no credential-socket path constant in a CriomOS
  module; the deploy orchestrator is declared as a user service.

The recorded direction deliberately does **not** retire the existing
`ssh root@<host>` privileged-access statement (`ARCHITECTURE.md:166-171`); that
is flagged below as a psyche decision point.

## 2 · Deployment-Specific Coupling Catalog

All citations are `file:line` in `/git/github.com/LiGoldragon/CriomOS` unless
noted. **Observation** = literal code fact; **Interp** = my reading.

### 2.1 The system-vs-user service choice (the psyche's direct target)

- **Observation:** `modules/nixos/lojix.nix:43` declares
  `systemd.services.lojix-daemon` — a systemd **SYSTEM** service. There is no
  `systemd.user.*` declaration for lojix anywhere in the repo (grep for
  `systemd.user` in `modules/` returns nothing).
- **Observation:** `serviceConfig` drops it to a fixed user:
  `User = operatorUser` (`:60`), `Group = operatorGroup` (`:61`), with
  `WorkingDirectory`/`StateDirectory` under `/var/lib/lojix` (`:62,:65`),
  `wantedBy = [ "multi-user.target" ]` (`:45`).
- **Interp:** this is exactly the "hard-wired to do this in criomos" the psyche
  calls wrong — a system unit impersonating a user. The grounding map's local
  HOME-activate failure (Q2) traces to this: the system daemon runs the user
  activate in an impoverished non-login environment (no `XDG_RUNTIME_DIR`/DBUS
  of its own). A user service dissolves that special case.

### 2.2 Hard-coded operator identity (`li`)

- **Observation:** `modules/nixos/lojix.nix:16` `operatorUser = "li";` and
  `:17` `operatorGroup = "users";` — literal identity constants. Used at:
  `:34-36` (assertion requiring user `li`), `:39`
  (`users.users.${operatorUser}.uid = mkDefault 1001;`), `:56` (SSH socket
  path), `:60` (`User = operatorUser`).
- **Contrast (Observation):** the rest of CriomOS does **not** hard-code the
  user. `modules/nixos/users.nix:16,25` derives the whole user set from
  projected Horizon (`inherit (horizon) node users;` … `name = user.name`).
  `modules/nixos/criome.nix:184,226` takes its service user from a `mkOption`
  (`cfg.user`), not a literal.
- **Interp:** `lojix.nix` is the outlier. Every other identity in CriomOS
  enters as projected data or an option; only lojix bakes `"li"`. This is a
  clean, isolated violation of the repo's own network-neutral rule.

### 2.3 Hard-coded cluster / witness / trust / cluster-source

- **Observation:** `modules/nixos/lojix.nix:26-28` writes the daemon startup
  config with a literal cluster proposal tuple:
  `(goldragon prometheus Hermetic github:LiGoldragon/CriomOS-test-cluster ${stateDirectory}/cluster.nota)`
  — cluster `goldragon`, witness/root node `prometheus`, trust mode `Hermetic`,
  and cluster-proposal source repo `github:LiGoldragon/CriomOS-test-cluster`,
  all as string literals.
- **Observation (partial compliance):** the **node** name in that same tuple is
  rendered from projected config: `${config.networking.hostName}` (`:27`) — this
  part follows the network-neutral pattern.
- **Observation (context):** the node name is *also* the only projected axis;
  `flake.nix:92-113` shows CriomOS already carries the projected-input substrate
  (`system`, `pkgs`, `horizon`, `deployment`, `secrets` stub flakes that lojix
  overrides per deploy). The literals at `lojix.nix:27` bypass that substrate.
- **Interp:** the daemon's bootstrap cluster identity is baked into the OS
  module instead of flowing through the projected-deployment substrate the rest
  of the flake uses. Note the source repo is literally a **test** cluster
  (`CriomOS-test-cluster`) — possibly a latent misconfiguration worth
  confirming, independent of the redesign.

### 2.4 Remote-auth wiring in the OS module

- **Observation:** `modules/nixos/lojix.nix:56`
  `SSH_AUTH_SOCK = "/run/user/${toString operatorUid}/gnupg/S.gpg-agent.ssh";`
  — the OS module injects operator `li`'s gpg-agent SSH socket as the daemon's
  auth credential.
- **Observation (mechanism lives in lojix, not CriomOS):** the actual
  `ssh root@<node>` transport is in the lojix crate, not CriomOS — grounding map
  cites `SshTarget::root_at_node` in `lojix/src/schema_runtime.rs`
  (~3948/3990/1342). CriomOS's coupling is only the credential-path wiring at
  `:56`. The `root@<node>.<cluster>.criome` targeting is documented in
  `modules/nixos/test-substrate.nix:58-60,88,109,155` (comments), consistent.
- **Observation (existing recorded direction):** `ARCHITECTURE.md:166-171`
  already states `ssh root@<host>` with the operator SSH key is "the standing
  privileged-access mechanism across the workspace."
- **Interp:** the OS layer hard-wiring *which* credential the daemon uses (the
  operator's gpg-agent socket) is a deployment specific per the psyche's rule.
  A user service inherits that agent from the session naturally, so the OS
  module would not need to name the socket at all.

### 2.5 Enable gate (compliant — no action needed)

- **Observation:** the service is gated by a projected node-service capability,
  not a hostname: `modules/nixos/lojix.nix:14`
  `lojixEnabled = nodeServices.has services "PersonaDevelopment";` over
  `horizon.node.services` (`:13`), via `modules/nixos/node-services.nix`.
- **Interp:** this part already follows the network-neutral / role-driven
  pattern. Keep it.

### 2.6 `ouranos` is NOT hard-coded in CriomOS Nix modules

- **Observation:** grep for `ouranos` across CriomOS hits only `AGENTS.md`
  (deploy-command examples, `:31-36`), `reports/*`, and comments in
  `criome-node-test.nix:19` / `criome-auth-integrated-test.nix:15` /
  `userHomes.nix:21`. No CriomOS **module** branches on or renders a literal
  `ouranos`.
- **Interp:** the brief's "hard-coded host `ouranos`" is not literally present in
  the OS Nix layer; the node identity flows via `config.networking.hostName`.
  The real hard-wired specifics are user (`li`), cluster/witness/trust/source
  (§2.3), the credential socket (§2.4), and the system-service model (§2.1).

## 3 · Proposed Deployment-Agnostic Redesign (Proposal Only)

Four coupled moves. The intent is: **CriomOS provides the generic substrate to
run a user-level deploy service; the deployment specifics live in projected data
and a deployment/criome concern, not in the OS module.**

### A · Service model: system service → user service

Convert the deploy orchestrator from `systemd.services.lojix-daemon`
(system, dropped to `User=li`) to a **user-level service** owned by the
operator's session. This is the psyche's stated preference and matches lojix's
own accepted invariant (`lojix/ARCHITECTURE.md:223-224`: "cluster-operator-owned,
not per-host … per operator workstation"). Side benefit: it runs the local
home-activate inside a real user session (with `XDG_RUNTIME_DIR`/DBUS/gpg-agent),
which is the grounding map's diagnosed root cause of the local-activate failure —
so this move is both the deployment-agnostic direction and the durable fix for
that bug.

### B · Parameterize identity and bootstrap config from projected data

Any remaining declaration derives user/uid/group and the daemon startup config
(cluster, witness, trust, cluster-source) from **projected Horizon / deployment
inputs**, exactly as `users.nix` and `criome.nix` already do — never from the
`"li"` and `(goldragon prometheus Hermetic github:…CriomOS-test-cluster)`
literals. The bootstrap cluster proposal becomes per-deploy data flowing through
the `flake.nix:92-113` substrate.

### C · Move remote auth out of the OS module

Remove the `SSH_AUTH_SOCK` gpg-agent wiring (`lojix.nix:56`) from the OS layer.
The daemon's remote-deploy identity is custodied per lojix's accepted direction
(`lojix/ARCHITECTURE.md:255-260`: "credentials custodied through criome … rather
than borrowing the operator's logged-in session (GPG/SSH agent)") — the criome
auth core, epic `primary-om4g`. Interim (until om4g lands): a **user** service
inherits the operator's gpg-agent from the session for free, so the OS module
stops naming the socket without needing om4g first.

### D · Deployment as a separate concern (end state)

The clean end state coincides with the already-recorded **LojixOS split**
(`ARCHITECTURE.md:180-192`): CriomOS = generic OS substrate; per-deploy config
(cluster/node/user/trust/source) = Horizon cluster data / the per-deploy config
crate; the deploy orchestrator = a user-level component the operator runs,
parameterized by projected data. CriomOS provides the ability to run a user
service; it does not encode one operator's specific deploy daemon.

## 4 · Top Decision Points For The Psyche

1. **Where does the lojix user service live / how enabled?**
   (a) Home Manager user service in CriomOS-home, gated by a projected
   user/role capability; (b) NixOS `systemd.user.services` in CriomOS, fully
   parameterized from projected data; (c) a standalone deployment component the
   operator installs. Trade-off: (a) most "user concern," (b) keeps declaration
   central, (c) most decoupled but most new scaffolding. **Recommendation: (a)
   or (b); confirm which repo owns the user-service declaration.**

2. **Interim remote auth while `primary-om4g` is unbuilt.** Accept the
   operator-session gpg-agent as the interim credential (OS no longer wires it;
   the session provides it), pending criome custody? Or block the user-service
   move on om4g? **Recommendation: accept the interim — it also unblocks the
   local-activate bug and needs nothing from om4g.**

3. **Fate of `ARCHITECTURE.md:166-171` (`ssh root@<host>` standing mechanism).**
   The new principle says the OS module must not *wire* the credential, but
   166-171 still names root-SSH-with-operator-key as the mechanism. Keep it as
   the interim transport, superseded by criome daemon-to-daemon auth
   (`primary-om4g` / `primary-1e6b`) when built — or retire it now? **I did NOT
   retire it; this needs a psyche call.**

4. **The bootstrap cluster proposal `(goldragon prometheus Hermetic
   CriomOS-test-cluster)`.** Should this become projected deployment data, or
   does the operator's daemon legitimately need one bootstrap cluster identity?
   And is the source pointing at **`CriomOS-test-cluster`** intended, or a stale
   misconfiguration to fix regardless?

5. **Sequencing vs the concurrent worker.** A separate worker may already be
   converting lojix to a user service as the "safe local-activate fix." This
   redesign should **absorb that as step A** of a ratified direction rather than
   a one-off patch, with B/C/D as follow-on. Confirm the fix and this direction
   converge rather than diverge.

## 5 · Checks Run / Not Run

- **Run (read-only):** `rg`/grep over CriomOS for `ouranos`, `systemd.user`,
  `User =`, `operatorUser`, `"li"`, `root@`, `SSH_AUTH_SOCK`, `gpg-agent`; read
  `modules/nixos/lojix.nix`, `node-services.nix`, `criomos.nix`, `users.nix`,
  `criome.nix` (partial), `flake.nix` inputs; read CriomOS + lojix
  `ARCHITECTURE.md`; `jj status`/`jj log` (CriomOS clean on `main`, no
  in-progress edits); `bd show primary-om4g`; `orchestrate (Observe Roles)` (no
  CriomOS claim held; only `cloud-maintainer` holds `cloud`); `spirit` lookups
  (negative — no matching public record for the cited Spirit ids, so treated as
  absence, not failure).
- **Not run:** no `nix eval`/`build`, no `lojix`/`meta-lojix` deploy, no
  `ssh`, no edits to `.nix`/config, no inspection of the concurrent worker's
  transcript. The exact failing activate line remains UNKNOWN per the grounding
  map (out of scope here).

## 6 · Blockers / Unknowns

- **Not a blocker, a coordination note:** CriomOS commits the whole working
  copy via `jj`. If the concurrent worker edits `modules/nixos/lojix.nix` in the
  same checkout, a co-commit risk exists. Mitigation applied: claimed only
  `ARCHITECTURE.md`, verified `jj status` shows only that file before
  committing.
- **Unknown:** whether the `CriomOS-test-cluster` source in `lojix.nix:27` is
  intentional or stale (Decision Point 4).
- **Provisional:** this proposal and the recorded ARCHITECTURE constraints are
  agent synthesis backed by the one psyche statement above plus the pre-existing
  network-neutral rule; the redesign moves (A-D) await psyche approval before
  any implementation. `primary-gss3` tracks that gate.
