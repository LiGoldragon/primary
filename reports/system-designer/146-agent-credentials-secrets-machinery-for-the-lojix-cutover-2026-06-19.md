# 146 — Agent credentials & secrets machinery: the Linux + hardware option space, mapped to the lojix cutover

*The psyche asked: "we need to find the best ways with Linux for agents to have
their own credentials and manage secrets... what machinery should we use? what's
well thought out, maybe modern even? what's useful in the hardware, what's not —
especially across my different hardware: new AMD, new Intel, older Intel, older
ARM." This grounds the answer in the live code (what the lojix daemon actually
needs), surveys the Linux software machinery and the hardware story per platform,
and recommends a layered scheme. It sits directly under two decisions recorded this
session: [the lojix daemon becomes the production deploy path; legacy lojix-cli
retires] (Spirit bsg1) and [lojix integrates with criome-based authentication;
criome is the auth/credential authority, layered over the per-host hardware/OS root
of trust] (Spirit h03z). Source: four grounded readers (daemon credential needs,
Linux secrets landscape, hardware key management, ecosystem patterns), synthesized.*

## BLUF

The modern, well-thought-out way to give a Linux daemon its own credentials is a
two-layer composition: **sops-nix (or agenix) as the declarative, recoverable,
multi-host at-rest layer**, and **systemd encrypted credentials
(`LoadCredentialEncrypted`) as the per-unit runtime delivery layer**, with the
credential key **sealed to a TPM 2.0** on hosts that have a usable one. This is
purpose-built for headless operation: PID 1 decrypts at unit start with no login, no
agent, and no human, and the plaintext lives only as a `0400` file in a per-unit RAM
tmpfs that never touches the Nix store. The hardware story is uneven and must be
planned for: TPM 2.0 (AMD fTPM / Intel PTT) covers your new AMD and new Intel by
default, older Intel often needs a discrete TPM module or falls back to the software
host-key path, and older ARM is the weakest tier (usually no usable TPM at all) — so
a **YubiKey-class FIDO2/PIV token is the one uniform hardware root** that is
identical across all four machine classes and survives reinstalls. The recommended
scheme layers these under **criome** (the per-Unix-user custody daemon already in
this codebase) as the eventual identity authority — which is exactly your `h03z`
decision — but for the lojix cutover you do **not** need that vision finished: a
TPM-sealed systemd credential plus an agenix-delivered deploy key gets the daemon
unattended now.

## What the lojix daemon actually needs credentials for

The lojix deploy daemon today reads **no secrets itself**. Its binary takes only the
rkyv startup archive (socket paths, state dir) and every authenticated `nix`/`ssh`
subprocess inherits the bare process environment with no injection (`NixCommand::run()`
at `schema_runtime.rs:3939-3956` is `Command::new(...).args(...).output()` — no
`.env`, no `NIX_CONFIG`, no access-tokens anywhere in the file). That design is clean,
but it means **all credentials are currently smuggled in through the inheriting
environment**, and the systemd unit hard-wires that environment to the human
operator's logged-in session. Concretely:

| Credential | Current source | Why it blocks unattended |
|---|---|---|
| **SSH private key** authorized as `root` on every target node | Borrowed from operator's GPG-agent SSH socket: the unit sets `SSH_AUTH_SOCK=/run/user/<operatorUid>/gnupg/S.gpg-agent.ssh` and runs `User=li` | The socket exists **only while operator `li` is logged in** and gpg-agent is unlocked. No login → no socket → every `nix copy`/activation `ssh` fails under `-o BatchMode=yes`. The single biggest cutover blocker. |
| **GitHub API token** for authenticated flake fetch | **Absent today** — relies on ambient `nix.conf`/`netrc`; the unauthenticated path that hit GitHub's 60-req/hour anon limit | Planned via gopass→`NIX_CONFIG` access-tokens through the unbuilt `nix-auth` crate (Spirit `2qhw`, the flake-auth Decision; bead `primary-srmq`, the open P1) — but gopass is operator-keyed, so it re-introduces a human-unlock dependency unless backed by a headless backend. |
| **Binary-cache substituter URL + public key** (non-secret) | Carried on the deploy wire payload as `ExtraSubstituter{url, public_key}` | Not a secret — no unattended problem. Open question only: *where resolution lives* (Spirit `lc28`, a low-certainty "for-now" decision, wants the daemon to resolve from bare node names via horizon-read; unimplemented). |
| **Cache signing private key** | **Deliberately not held by lojix** — relies on `require-sigs` + `--substitute-on-destination`; targets pull already-signed paths | No blocker; the agent scheme leaves signing out. A cluster/CI concern. |
| **Target SSH host public keys** for verification | None consumed — the host-key check (`check_key_material` at `schema_runtime.rs:2713-2720`) is a **stub returning zero mismatches**; trust rests on the inherited `known_hosts` | Not a start-blocker, but a real gap: the daemon does not actually verify target host keys yet. |

Net: an agent-owned scheme must deliver **two live secrets** non-interactively — a
dedicated deploy SSH key and a GitHub token — plus the two non-secret trust inputs.
Honest caveat: the `nix-auth` crate does not exist yet, bead `primary-srmq` cites a
design report not present at its path, and the original rate-limit incident report is
gone — so the crate's API is corroborated by Spirit prose, not a readable doc.

## The Linux software machinery (what's out there, ranked)

| Mechanism | What it gives | Unattended / headless | NixOS fit | Verdict |
|---|---|---|---|---|
| **systemd credentials** (`LoadCredential[Encrypted]`, credstore) | Per-unit secret decrypted by PID 1 into a `0400` RAM-tmpfs file (`$CREDENTIALS_DIRECTORY`), gone when the unit stops | **Excellent — purpose-built.** No session, agent, or presence; never world-readable or in the store | **First-class** native option; encrypted ciphertext can ship in the store | **The runtime delivery baseline.** Tightest blast radius of any option. |
| **TPM 2.0 sealing** (`systemd-creds --with-key=tpm2`, PCR policy; clevis+tang for network-bound) | Machine-bound key — only this physical machine (optionally only in a trusted boot state) unseals, no passphrase | **Best-in-class for unattended.** Auto-unseal at boot, optional tamper-binding | **Good.** Friction: PCR-bound ciphertext is host-and-boot-specific | **Bind the credstore key** where a TPM exists. Caveat: PCR brittleness — keep a recovery secret. |
| **sops-nix** | Declarative at-rest secrets in-repo (age / SSH-host-key / KMS) → `/run/secrets` at activation, no human | **Excellent** — decryption key is the host ed25519 key, on disk at boot | **Native, excellent — and already adopted in CriomOS** | **The at-rest source-of-truth.** De-facto NixOS standard. Pair into `LoadCredential` for tightest exposure. |
| **agenix / ragenix** | Lighter pure-age: one encrypted file per secret, SSH/age pubkey recipients | **Excellent** — same host-key model | **Native, minimal module** | **The simpler at-rest option.** Lighter fit for a single deploy key. |
| **FIDO2 / PKCS#11 / PIV tokens** (YubiKey, `age-plugin-yubikey`, `systemd-cryptenroll --fido2`) | Presence-gated secret bound to a physical token | **Deliberately the opposite of unattended** — needs a human touch | Supported (pcscd, age plugins) but orthogonal | **Operator-present ceremonies only** — gate the root recipient, authorize/seal/rotate. The uniform portable hardware root. |
| **Kernel keyring** (`keyctl`) | In-kernel volatile RAM secret storage | **A building block, not a solution** — RAM-only, no at-rest store | Available, rarely surfaced | **Complement, not baseline.** |
| **D-Bus Secret Service / gnome-keyring** | Freedesktop secret API over the login keyring | **Poor — avoid for daemons.** Login-scoped; a system daemon has nothing to unlock it | Fine for desktop, wrong for daemons | **Legacy / ill-fit for headless.** |
| **gopass / pass (GPG)** | Password store as GPG files in git, via gpg-agent + pinentry | **Poor for services** — needs a cached passphrase / pinentry | Fine as a human tool | **Keep as your personal vault; never a service source.** |
| **SPIFFE/SPIRE + Vault** | Short-lived workload identities, dynamic secrets, mTLS fabric | **Excellent at scale** — but bootstrap still needs the simpler roots above | Packaged but heavyweight (a server to run/unseal/back up) | **Overkill for a personal cluster.** A deliberate future upgrade, not now. |

The shape: **modern/well-thought-out = systemd-creds + TPM2 (runtime) over
sops-nix/agenix (at-rest)**; **legacy or ill-fit for headless = gnome-keyring and
gopass-for-services**; **enterprise-overkill = SPIFFE/Vault**. Don't conflate the
layers — sops-nix/agenix authors and versions the ciphertext, systemd credentials
delivers it per-unit, the TPM binds the key to the machine. Picking only one leaves
a gap (sops-nix without `LoadCredential` over-exposes to `/run/secrets`; TPM-only
loses recoverability).

## The hardware story across your machines

| Hardware class | Hardware root | What's useful | What's NOT useful |
|---|---|---|---|
| **New AMD** | **fTPM** in the Platform Security Processor | Seal the daemon key to the TPM (`systemd-cryptenroll`/`systemd-creds --with-key=tpm2`); auto-unseal unattended at boot | **SEV / SEV-SNP** — protects VM memory from an untrusted hypervisor; gives no host-local key-at-rest sealing. Overkill. (The old AMD fTPM stutter bug was fixed in AGESA 1.2.0.7+, 2022.) |
| **New Intel** | **PTT** (Platform Trust Technology), fTPM in the CSME | Same: enable in firmware, seal the key, unattended unseal | **SGX** deprecated/removed on client (11th-gen+); **TDX** is Xeon-only confidential-VM. Neither is for a host key at rest. |
| **Older Intel** | **Often none** — pre-Skylake / low-end may lack PTT | (a) Fit a **discrete TPM** if the board has an SPI/LPC header (stronger boundary, not wiped by a CPU BIOS update); (b) else the **software age host-key path** (sops-nix via the host ed25519 key) — exactly what this workspace does today | Don't assume "just seal to the TPM" works — it frequently can't. |
| **Older ARM** | **Usually none / weakest** — TrustZone+OP-TEE fTPM is board-specific and provisioning-heavy | The **software age key** fallback + full-disk encryption + the portable token as the real hardware factor | Don't chase OP-TEE fTPM for one SSH key on hobbyist SBCs — high effort, low payoff. |

Two blunt cross-cutting truths. First, **the portable FIDO2/PIV token is the only
uniform hardware root** — identical on AMD, Intel, and ARM, surviving OS reinstall
and motherboard swap because the secret lives on the token. Use it as the
operator-presence factor and, where TPMs are absent, as a portable age recipient.
Second, **no open PC/ARM stack matches Apple's Secure Enclave + Keychain
integration**: there is no unified, OS-managed secure element with seamless UX. TPM2
is a separate device with manual enrollment, PCR-policy management, and
recovery-secret discipline. And the standing caveat for every TPM tier: **fTPM trust
roots in closed vendor firmware** (AMD PSP, Intel CSME) and sealed state can be
**wiped by a BIOS update, "Clear TPM", firmware reset, or hardware swap** — so a TPM
must never be the sole copy of an unrecoverable key. Always keep an independent
recovery secret (which is exactly what the sops-nix/agenix at-rest layer provides).

## What this ecosystem already does, and the criome question

Two adopted secret layers, one daemon-identity-key custody pattern in code:

- **sops-nix** is the only adopted cluster/system machinery — a flake input + NixOS
  module decrypting via the host SSH ed25519 key converted to age (`secrets.nix`,
  used in `router/default.nix` and `llm.nix` for Wi-Fi passwords and the local-LLM
  token). **No agenix, ragenix, tpm2, clevis, or systemd `LoadCredential` is adopted
  anywhere** — those appear only as enumerated-but-unused options in one CriomOS
  review report. Adopting systemd credentials or TPM sealing is genuinely greenfield.
- **gopass** is the established user-session store, fetched fresh at exec time via
  wrappers; agents are forbidden from ever seeing the value (Spirit `7gq6`/`y94z`,
  the never-show-a-secret rule; `cjrl`, the gopass-for-session /
  sops-nix-for-cluster split).
- **criome** is the one daemon with real key custody in code: `master_key.rs`
  generates a master BLS keypair on first run from `/dev/urandom`, persists the
  secret to an atomically-created `0600` file (rejecting symlinks / loose perms /
  corrupt files), and **never lets the secret cross a wire boundary**. It is
  architected as the **per-Unix-user** custody + registrar + verifier (trust
  boundary = the OS Unix-user; meta socket `0600` + `SO_PEERCRED` failing closed on
  uid mismatch). It already has `Agent` as a first-class `Identity` and
  `AgentRequest`/`PersonaRequest` in `KeyPurpose`, and **registration is gated by a
  cluster-root signature** (`admission.rs`, five passing tests).

**Position on criome** (and it matches your `h03z` decision): criome should be the
credential/identity **authority** for agent and daemon identity, layered *above* the
OS machinery, not a competitor to it. Recorded intent points squarely there —
`3fm6`/`a4i6` (long-lived agents have cryptographic identity tied to their criome
master public key), `jtmt` (the public key IS the agent identifier), `ermr` (the
cluster-root signature is the registry admission gate), `d6he` (the first production
milestone's object authentication routes through the local criome). criome is the
**only** mechanism that gives daemons real cryptographic identity (sign / verify /
registry / attestation), not just a stored secret blob.

But be precise about exists-versus-prescribed. criome holds **only the public
halves** of others' keys — each principal custodies its own private half. The
admission **gate** exists and is tested, but per commit `c8f2f51f` (the cluster-root
admission correction) the admission-**signing ceremony** — who/what runs the
cluster-root signer and issues admissions — is **operationally undefined**, the real
open gap. And the agent-daemon and spirit-daemon do **not** currently link
`signal-criome` or carry any identity key (empty grep on their `Cargo.toml`);
layering criome custody onto them is net-new wiring, not an extension of a live
integration. So criome is the right authority and is partly built, but it is the
heaviest leg to finish and the newest substrate.

## Recommendation — the layered scheme

A four-layer composition, degrading gracefully per host:

**(a) Runtime delivery, every host — systemd encrypted credentials.** Each daemon
gets its secret via `LoadCredentialEncrypted=` → a `0400` RAM-tmpfs file in
`$CREDENTIALS_DIRECTORY`, never in the store, never world-readable. Composes cleanly
with the daemon-takes-one-binary-startup rule: the deploy/bootstrap tool reads the
decrypted secret, encodes the typed NOTA config to rkyv, and delivers it via the
credential — the daemon never parses NOTA or touches a vault.

**(b) Machine-unattended unlock where a TPM exists (new AMD, new Intel) —
TPM2-sealed credstore.** Upgrade the credstore key to
`systemd-creds --with-key=host+tpm2` (PCR-less, or signed-PCR for boot-state binding
that survives updates). Auto-unseal at boot, no operator. **Always** keep the
recovery secret in (c).

**(c) At-rest source-of-truth, every host (and the fallback for older Intel / ARM) —
sops-nix or agenix.** Secrets encrypted in-repo, each host listed by its
`ssh-to-age` host-key pubkey, decrypted at activation with no human. The recoverable,
version-controlled authoring layer; the TPM credstore is a regenerable cache on top.
On TPM-less hosts, this *is* the unattended path (host ed25519 key → age), hardened
with full-disk encryption. **Decision point:** stay on sops-nix (already adopted,
KMS/structured-file capable) or adopt agenix/ragenix (simpler one-file-per-secret) —
for a single deploy key, agenix is the lighter fit.

**(d) Operator-presence + uniform portable root, every host — FIDO2/PIV token.**
Gates human-in-the-loop actions (authorize a deploy, seal/rotate the daemon key,
recovery) and serves as a portable age recipient where TPMs are absent. The one
hardware root identical across all four machine classes.

**(e) Identity authority, the longer architecture — criome (your `h03z` decision).**
Per-daemon/per-agent identity is minted by reusing criome's custody pattern: each
principal generates its own BLS keypair following the `master_key.rs` discipline
(`0600`, atomic, never leaves the process), registers its public key with the local
per-Unix-user criome gated by cluster-root admission, and escalates to criome for
authorization. The public key is the identity. The work to do: the **cluster-root
admission-signing ceremony** plus **linking `signal-criome` into the agent/spirit/
lojix daemons** — the custody, registry, verify, and admission-gate machinery
already exist and are tested.

**Mapping to the cutover blocker** ("the daemon must run unattended with its own
credentials instead of borrowing the operator's GPG SSH agent"):

- *Daemon SSH credential* → replace `SSH_AUTH_SOCK=.../gnupg/S.gpg-agent.ssh` and
  `User=li` with a dedicated deploy SSH key delivered via **(a)** `LoadCredentialEncrypted`,
  sealed via **(b)** on TPM hosts and via **(c)** agenix on the rest. The service
  runs under its own system identity. The cutover-critical change.
- *GitHub token* → deliver the same way (agenix/sops → `LoadCredential` → injected
  as `NIX_CONFIG` access-tokens per-process, never on disk). The `nix-auth`
  `SecretBackend` trait is the right seam, but its default gopass backend is
  operator-keyed — for unattended you need a **headless backend reading the
  systemd-credential file**, not gopass.
- *Route operators onto meta-lojix* → an orthogonal interface change, not a
  credential change; it does not gate on this scheme.

**Build FIRST for the cutover (days, not the full vision):** a dedicated deploy SSH
key + GitHub token, encrypted with **agenix** (or sops-nix — match the adopted
tool), delivered via **`LoadCredentialEncrypted`** into the lojix unit, the unit
changed to run under its own system identity. On the deploy host (the probe confirms
a usable TPM2 v2 chip, `has-tpm2 yes`, `credential.secret` provisioned), seal the
credstore key to the TPM for boot-survivable unattended unlock. That alone clears the
blocker. **The longer architecture:** the full criome custody/admission scheme
(layer e, your `h03z` direction), the `nix-auth` headless backend, lc28's daemon-side
substituter horizon-read, and making the host-key verification stub real.

## What NOT to do

- **Don't reach for SEV-SNP, SGX, or TDX for key storage.** They protect VM/enclave
  memory from an untrusted host; they give no host-local key-at-rest sealing for a
  bare-metal daemon, add large complexity for zero benefit, and SGX is deprecated on
  client CPUs. The TPM is the tool for sealing a host key.
- **Don't put service secrets behind gnome-keyring/Secret-Service or pinentry-gated
  gopass.** Both assume an interactive login session; a daemon with no logged-in
  user has nothing to unlock them — the exact trap the current lojix unit fell into.
  Keep gopass as the human vault only.
- **Don't hand-roll crypto or a bespoke secret store.** Use systemd credentials,
  sops-nix/agenix, and the TPM stack. For identity, reuse criome's tested
  custody/admission machinery rather than inventing a parallel one.
- **Don't make a TPM the sole copy of a key.** Firmware updates, "Clear TPM", and
  hardware swaps wipe sealed state. The sops-nix/agenix at-rest layer is the
  mandatory recovery copy.
- **Don't block the cutover on the full criome-custody vision.** criome is the right
  long-term authority and intent backs it, but its admission-signing ceremony is
  operationally undefined and the agent/spirit/lojix daemons don't yet link
  `signal-criome`. A TPM-sealed systemd credential plus an agenix-delivered deploy
  key gets the daemon unattended **now**; criome custody is the architecture you grow
  into, not a cutover prerequisite.
- **Don't treat `lc28` or `2qhw` (substituter-resolution and flake-auth "for-now"
  decisions) as final.** Both are low-to-medium certainty; `lc28` explicitly says its
  code must be replaced. Build credential delivery backend-swappable.

**Honesty on thin spots:** the `nix-auth` crate and its design report do not exist
(API known only from bead text); the host-key verification path is a stub; and the
criome cluster-root *signing* ceremony — who actually issues admissions — is
genuinely undesigned. None block the recommended cutover path (a/b/c against the
deploy key), but they are real gaps in the longer criome-authority architecture and
should not be presented as solved.
