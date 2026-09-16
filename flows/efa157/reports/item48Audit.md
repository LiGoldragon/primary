# Audit of Codex cf7879's item 48 overnight proofs — 2026-09-16

Read-only Fable audit subflow of flow efa157. "Witnessed" = this auditor ran it; "claim" = Codex's
report. Branch `origin/proposal/prometheus-service-provider-poc`, head `9dd0e63` (15 commits over
main, +1245 lines, contained by no other branch; main unchanged since 2026-09-12).

## Verdict

**Works (witnessed).** The enabled configuration now evaluates `system.build.toplevel`. The two
NixOS Prosody assertions the earlier audit hit are gone because the module sets
`services.prosody.xmppComplianceSuite = false` — the compliance suite is declined, MUC is *not*
configured (`muc = []`). Both the sops-path form and the self-signed form evaluate; the policy
check itself forces `toplevel.drvPath` for the sops form only. The TLS shell script is real
behavior: a 3072-bit RSA self-signed cert, 30 days, `subjectAltName=DNS:<xmpp>,DNS:<forgejo>`, mode
0640, idempotent on a valid existing pair, refusing invalid domains and half-written pairs.
`certificatePath = null` is no longer an assertion failure: it is the default and selects the
generated pair plus a `prometheus-service-tls.service` oneshot ordered `before`/`requiredBy` prosody
and forgejo. The OMEMO 2 round trip is real: `twomemo` 2.1.0 / `omemo` 2.1.0, two in-memory session
managers, encrypt→decrypt of `b"fixture-encrypted-message"` under `urn:xmpp:omemo:2`, plus a tamper
case flipping one ciphertext byte and requiring `omemo.DecryptionFailed`; the branch's build log
shows it built on `ssh-ng://nix-ssh@prometheus.goldragon.criome`. The
Notify CLI is **not** a hand-written subset: `signal-message` `parse_one` runs
`Potential::<Notify>::from(text).actualize(&Budget{…})` — the shared `datom-codec` reader — and adds
only bare-JID and length validation (4096-byte input, 1024-byte body) on top. A review runner now
exists as a script with a genuine behavior check (pass / fail / SIGTERM-interrupt / rejected-source).

**Claimed only.** Every green run. `nix flake check` is unreachable offline by design: the new checks
sit under `projectChecks.${system}` where `system = inputs.system.system`, a throwing lojix stub.
Codex's remote-builder passes are taken as infrastructure ground per the testing skill — but below.

**Stale / disconfirmed.**
1. **The claimed Notify pass does not cover the branch head.** Publication `c2d0e99` tested source
   `9b55087`. Three commits land *after* it and change the check materially: `6e8dbc6` replaced the
   Python parser with the Rust `notify-datom` CLI and added the `signal-message` input; `caa3dc3`
   ("Use positional Notify Datom test fixture") and `9dd0e63` ("Use opaque string Notify Datom
   fixture") each rewrote the fixture's invocation spelling. No report records a run of any of the
   three — two consecutive spelling-only commits with no recorded run is the signature of untested
   iteration. The head's `notify-datom` invocations are unwitnessed.
2. **Reports 0051 and 0054 state the wrong accepted spelling.** Both say `Notify.{ «bare-jid» «body» }`.
   `Notify` is `Notify.{NotifyRecipient NotifyBody}` in `ethos/signal.ethos` — a *struct*, not a root
   variant — so at root it textualizes positionally as `{ bob@example.org «body» }`, exactly what
   `caa3dc3` corrected the fixture to. Their guillemet requirement is wrong too: the head fixture
   passes a bare recipient. The prose was not updated when the code was.
3. **The 30-day certificate is a scheduled outage, not a rotation.** `prometheus-service-tls.sh`
   runs `openssl x509 -checkend 0` and on an expired cert prints "invalid or expired existing TLS
   certificate" and exits 1 — it never regenerates. The unit is `requiredBy` prosody and forgejo, so
   31 days after first activation both fail to start. Nothing tests this.
4. **No firewall ports.** No `networking.firewall`/`openFirewall`/port anywhere in the module, and
   neither the nixpkgs prosody nor forgejo module opens any: nothing outside the host reaches it.
5. **`actions.ENABLED = true` with no registered runner.** Forgejo Actions is switched on by
   `reviewRunner.enable`, but no `services.gitea-actions-runner`, token, or registration exists;
   queued jobs would sit forever. The `prometheus-nix-review` unit is a separate manual oneshot
   rebuilding *one fixture at one hard-coded revision* (`7ee7841`, pinned by a single-value
   `types.enum`, already 8 commits behind head). It reviews nothing proposed; it is a self-rebuild.
6. **`NotifyValidatedOffline.{}` is not a contract type** — nowhere in `signal.ethos`, just a
   `println!` literal; errors are free prose on stderr rather than a datomized `Error`.
7. **Nothing consumes the CLI.** `packages/prometheus-notify-proof.nix` re-exports `notify-datom`
   (blueprint auto-discovers `packages/`) and the check runs it; no module, service, or other repo
   calls it. `signal-message` `87278034` lives on `proposal/notify-datom-adapter` only — unmerged;
   `src/notify.rs` does not exist on its main.
8. **No path connects OMEMO to Prosody.** The round trip is a pure library call on two synthetic
   in-memory identities (`InMemoryStorage`, upstream `tests/session_manager_impl.py`). No account,
   JID registration, stanza serialization, PEP device-list/bundle publication, socket, bot, or trust
   policy. `packages/prometheus-notify-proof.py` is a 47-line Protocol plus `deliver_encrypted`,
   which encrypts, decrypts and compares bytes — the name "deliver" delivers nothing.
9. **"Offline" is qualified.** Both OMEMO checks `fetchurl` the `python-omemo` test helpers from
   `codeload.github.com` (fixed-output — hermetic, not network-free on a cold store). Prosody's
   `mam`, `carbons`, `smacks` are on by nixpkgs default, not by this module (witnessed: all `true`).
10. **sops is still prose.** No `sops.secrets.*` declaration anywhere — only a doc-comment on the two
    path options, and no secret owner/group, so prosody and forgejo may not be able to read them.

## (5) Behavior tests or change-detectors

No change-detector in the testing-skill sense — nothing compares source text. But the policy check is
still mostly **tautological wiring**: ~30 assertions read back an option value the check itself set
two screens earlier (domain in, domain out). Three parts are real behavior: the forced
`enabledToplevel` (runs the whole module system and its assertions — the fix for the earlier
finding), the `hasFailedAssertion` cases, and the TLS fixture, which runs openssl. The runner, OMEMO
and Notify checks are behavior tests. Gaps: nothing forces the *self-signed* form's toplevel (I did;
it evaluates), and no VM test starts the unit, so activation on a real host is untested — the fixture
stubs `chown` with a script that only asserts its arguments.

## (6) Items 47 and 48 residue

Still missing from **47**: Yggdrasil binding, ssh, namespaces/orgs (universal primary / persona /
per-person), GitHub mirrors, any `sops.secrets` declaration, a registered Forgejo Actions runner,
any build of the Slint app or the crates, any review of a proposed change, firewall. *Newly present:*
a bounded manual review unit and its behavior check.
Still missing from **48**: accounts for the living and a bot, a chime bot, an XMPP transport of any
kind, device-list/bundle publication, persistent OMEMO storage, trust policy, and any Cloudflare
linkage — `cloud`'s `proposal/cf7879-cloudflare-fixture-nix-check-signed-upstream` adds
`src/messaging_dns.rs` (scoped DNS *plans* from fixtures, refusing out-of-scope records) and a Nix
check, but no live API, no certificate issuance, and CriomOS does not reference `cloud`. *Newly
present:* the self-signed fallback (was the blocking gap) and a datom-codec-backed Notify CLI.

## Before the living can try it

1. Run the branch head's `prometheus-notify-proof` and record it; the claimed pass predates three
untested commits. 2. Correct reports 0051/0054 to the positional spelling. 3. Renew the certificate
before expiry instead of failing on it, or the services die on day 31. 4. Open the ports. 5. Either
register an Actions runner or stop setting `actions.ENABLED`. 6. Declare the sops secrets with
owner/group, or drop the sops branch from the option surface. 7. Add a VM test that boots the enabled
configuration, so activation — not evaluation — is what is proven.

## Files read

`/git/github.com/LiGoldragon/CriomOS` @ `9dd0e63`: `modules/nixos/{prometheus-service-provider.nix,
prometheus-service-tls.sh,prometheus-nix-review-runner.sh,criomos.nix}`, `checks/{prometheus-service-provider-policy,
prometheus-notify-proof,omemo2-encrypted-roundtrip,prometheus-nix-review-runner}/default.nix`,
`packages/prometheus-notify-proof.{nix,py}`, `flake.nix`, `flake.lock`, `AGENTS.md`,
`reports/0048-omemo2-roundtrip-remote-7446b94c.log`, `reports/{0050,0051,0054}-*.md`.
`/git/github.com/LiGoldragon/signal-message` @ `87278034`: `src/notify.rs`, `src/bin/notify-datom.rs`,
`tests/notify_datom.rs`, `src/generated/signal.rs`, `ethos/signal.ethos`, `flake.nix`.
`/git/github.com/LiGoldragon/cloud` @ `9cb9394` (diff stat only). Prior audit:
`/home/li/primary/.claude/worktrees/flow-840e42/flows/840e42/reports/prometheusServicesAudit.md`.

Witness method: `nix-instantiate --eval --strict --json --max-jobs 0` on a local expression that
`getFlake`s the branch revision, rebuilds the policy check's two `lib.nixosSystem` fixtures and
`deepSeq`s both `system.build.toplevel.drvPath` → `{"carbons":true,"complianceSuite":false,
"enabledToplevel":true,"mam":true,"muc":0,"selfSignedToplevel":true,"smacks":true}`.
