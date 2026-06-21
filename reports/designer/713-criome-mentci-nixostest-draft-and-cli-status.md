# 713 — criome+mentci nixosTest draft + CLI all-paths status

The two phase-2 follow-ons the psyche greenlit: the end-to-end **criome+mentci
nixosTest** (drafted below, ready for operator to complete + run on Prometheus)
and the **all-paths-CLI** work (Spirit `isia`), which is mostly already in
operator's working copy.

## What this proves (and the honest scope)

The nixosTest lifts the existing in-process proof
`mentci/tests/criome_bridge.rs::mentci_closed_verdict_approves_criome_escalation_over_meta_socket`
from threads to **two systemd services on one guest**: criome (flipped to
ClientApproval over its meta socket at runtime) parks an authorization; mentci
(holding the MetaCriome leg = criome's 0600 meta socket, same system user)
surfaces it as a `CriomeEscalation(slot)` pending question with
`criome_access = ReadWrite`; the test answers it; mentci routes the verdict to
criome by slot; criome records the grant. That is the whole daemon-routing loop,
VM-proven.

**Scope caveat — this is more than "wire the flake packages."** The draft is
complete and grounded, but the workflow found real operator work before it runs
(detailed in §3): mentci has **no flake at all** yet, the observe→answer
**witness bin doesn't exist**, and the 142 template has a pre-existing
**encoder bin-name mismatch** (`criome.nix` calls `criome-encode-configuration`;
only `criome-write-configuration` exists). I cannot `nix build`-verify here, so
this is a designer draft operator completes + runs.

## CLI all-paths status (Spirit isia)

Operator's mentci working copy **already lands the answer atoms** —
`ClientAnswerCommand` with `answer:approve|reject|defer:<question-id>`, a
`ClientReplyRender`, the dispatch, and the happy-path test — so the verdict path
is CLI-reachable and rendered. The remaining gap to fully realize `isia` (every
path first-class + every reply readable) is small and is operator's (their active
repo, uncommitted in flight):

- **Render the generic path too.** The inline-NOTA / `.nota` / binary fallback
  in `ClientCommand::run_with_writer` still emits a raw binary reply frame; route
  it through `ClientReplyRender` so `mentci "(PushUpdate (...))"` prints
  `reply (UpdateAccepted ...)` like the atoms do. (Factor the socket exchange
  onto `FrameCodec::exchange` so observe/answer/generic share one render path.)
- **Two cheap write atoms** for the single-token paths: `retract:<token>`
  (`RetractInterfaceObservation`) and `propose:<id>:<text>`
  (`ProposeEditedAnswer`). `PresentQuestion`/`PushUpdate` carry rich payloads, so
  they stay on the inline-NOTA edge — which now renders readably, so they're
  first-class.
- **A read-only rejection test** — answer against a no-write-bridge daemon and
  assert the readable `reply (Rejection ...)`.

The full per-line CLI spec (exact diffs, the `FrameCodec::exchange` refactor, the
atom roster table, the tests) is in the workflow output; this is the summary for
the handoff. No designer edit to mentci — it's operator's in-flight surface.

## criome+mentci nixosTest

This recycles `criome-nixos-module-142` (the criome.nix systemd module + criome-node.nix runNixOSTest skeleton). It keeps `criome.nix` unchanged (it boots criome in the default `Quorum` mode and binds both a working and a meta socket), adds a sibling `mentci.nix`, and flips criome to `ClientApproval` at runtime over the meta socket from the testScript. Both daemons run under the **same `criome` system user**, so the criome meta socket's `0600` boundary is a real OS boundary that the mentci daemon (same uid) can cross and a third party cannot.

Grounded facts that shape the design (all verified in source, not assumed):

- The criome daemon **always binds two sockets**: a working socket and a meta socket. `criome/src/daemon.rs` `CriomeDaemon::from_configuration` derives the meta path from the working socket when the config omits it — `default_meta_socket_path` returns `…/criome.sock.meta`. Both are bound at `0600` by `bind_private_socket` (`std::fs::set_permissions(socket, Permissions::from_mode(0o600))`). So criome.nix needs no change to expose a meta socket: it sits at `/run/criome/criome.sock.meta`.
- criome's default authorization mode is `Quorum` (`signal-criome/src/lib.rs` `CriomeDaemonConfiguration::new` sets `authorization_mode: AuthorizationMode::Quorum`). The runtime flip to `ClientApproval` goes over the **meta** socket as `meta_signal_criome::Input::Configure(CriomeDaemonConfiguration…with_authorization_mode(ClientApproval))` — exactly what `criome-client-approval-witness-test` and `mentci-criome-pickup-witness-test` already do.
- The mentci daemon (`mentci/src/bin/mentci-daemon.rs`) is one-argument binary-startup: `DaemonCommand::from_environment().run()`, whose `startup_path` rejects anything but exactly one path arg (`Error::StartupArgumentCount`) and rejects `.nota` extensions (`Error::StartupNotaRejected`). It reads a single rkyv `Configure(MentciDaemonConfiguration)` frame via `ConfigurationFile::configuration` → `MetaInput::decode_signal_frame`. Same discipline as criome-daemon.
- The mentci daemon takes its `MetaCriome` `ComponentSocket` = criome's **meta** socket. From that it builds a `CriomeApprovalBridge` (`mentci/src/daemon.rs`, `criome_meta_socket_path().ok().map(CriomeApprovalBridge::new)`). On `ObserveInterfaceState`, the daemon pulls criome's parked list through the bridge (`parked_authorizations_for_request`) and surfaces each parked slot as an `ApprovalQuestion` whose `proposal.source` is `ApprovalSource::CriomeEscalation(slot)`. On `AnswerQuestion`, the produced `CriomeVerdict` is pushed back to criome's meta socket via `CriomeApprovalBridge::submit_criome_verdict` → `SubmitAuthorizationApproval`. So **answering through the mentci daemon is what records the grant on criome** — no separate meta-CLI for the answer step.
- The end-to-end shape is exactly `mentci/tests/criome_bridge.rs::mentci_closed_verdict_approves_criome_escalation_over_meta_socket`, lifted from in-process threads to two systemd services on one guest.

### 1. `mentci.nix` (sibling of `criome.nix`, place at `nix/modules/mentci.nix`)

This mirrors `criome.nix`'s structure beat-for-beat: a single positional-NOTA daemon configuration, an `ExecStartPre` that seals it to rkyv, and an `ExecStart` of `mentci-daemon <config.rkyv>` with exactly one argument and no flags. The daemon package carries no nota-text; the encoder package does.

One real divergence to call out (operator gap, section 3): criome.nix's encoder invocation passes a single inline-NOTA artifact record, but the criome encoder bin that actually exists — `criome-write-configuration` — takes three **positional path arguments** (`<socket> <store> <output>`), and the mentci encoder `mentci-write-configuration` likewise takes `<socket> <criome-meta-socket> <output>`. So mentci.nix below carries the same inline-NOTA shape criome.nix uses (the intended deploy contract), and section 3 records the positional-arg encoder the operator wires until the encoders accept the NOTA artifact.

```nix
# mentci.nix — the NixOS module that runs the mentci daemon as a systemd
# service from a PRE-ENCODED binary rkyv startup, honoring the one-rkyv-arg /
# no-flags daemon discipline. Sibling of criome.nix.
#
# Same shape as criome.nix: the module authors the daemon's typed configuration
# as a single positional NOTA record, an `ExecStartPre` step seals that NOTA
# into the rkyv artifact the daemon consumes, and `ExecStart` launches
# `mentci-daemon <config.rkyv>` with exactly one argument and no flags. The
# daemon itself never parses NOTA (its package is built without nota-text); it
# reads a single rkyv `Configure(MentciDaemonConfiguration)` frame.
#
# THE NOTA -> rkyv ENCODE IS A DEPLOY STEP, NOT A FLAG. `mentci-daemon` accepts
# only the pre-generated rkyv configuration file as its one argument and rejects
# inline NOTA and `.nota` paths (StartupNotaRejected / StartupArgumentCount). So
# the typed `MentciDaemonConfiguration` — the Mentci working socket, the criome
# MetaCriome socket, the persona identity, the notification clients — is encoded
# here, in `ExecStartPre`, by the one-argument `mentci-encode-configuration`
# deploy encoder (which lives in the nota-text encoder package, not the daemon
# one).
#
# SAME-USER META BOUNDARY. mentci must reach criome's PRIVATE meta socket
# (0600, owned by the criome daemon). To make that boundary a real OS boundary
# rather than a hole, mentci runs under the SAME `criome` system user. The meta
# socket admits the local user-owned approval client (mentci) and nobody else.
#
# SELF-RESUME ON RESTART. mentci's interface state is in-process today; the
# durable surface it answers FOR is criome's SEMA store. The ExecStartPre
# re-encode of the (deterministic) configuration is idempotent.

{
  config,
  lib,
  pkgs,
  ...
}:

let
  cfg = config.services.mentci;

  runtimeDir = "/run/mentci";
  socketPath = "${runtimeDir}/${cfg.socketName}";
  configRkyv = "${runtimeDir}/mentci-config.rkyv";

  # The single typed `MentciDaemonConfiguration` record, positional NOTA: the
  # component-socket vector (each `ComponentSocket` is `(kind socket)` with the
  # socket a `StandardSocket` Unix payload), then the `PersonaIdentity`
  # `(name component-kind key-label)`, then the notification-client vector — in
  # declared order, no type-name head, mirroring criome.nix's body-only record.
  # The encoder wraps it in a `MentciConfigurationArtifact` carrying the output
  # path and seals it to rkyv.
  #
  # criome_meta_socket is the MetaCriome leg: criome.nix binds its working
  # socket at /run/criome/criome.sock and the daemon derives the meta socket as
  # <socket>.meta, so this points at /run/criome/criome.sock.meta.
  configurationNota =
    "(MentciConfigurationArtifact "
    + "("
    + "[(Mentci (Unix ${socketPath})) (MetaCriome (Unix ${cfg.criomeMetaSocketPath}))] "
    + "(${cfg.personaName} Persona ${cfg.personaKeyLabel}) "
    + "[StatusBar Popup]"
    + ") "
    + "${configRkyv})";

  encodeConfigurationScript = pkgs.writeShellScript "mentci-encode-configuration" ''
    set -eu
    ${cfg.encoderPackage}/bin/mentci-encode-configuration ${lib.escapeShellArg configurationNota}
  '';
in
{
  options.services.mentci = {
    enable = lib.mkEnableOption "the mentci human-approval daemon";

    daemonPackage = lib.mkOption {
      type = lib.types.package;
      description = "Package providing the `mentci-daemon` binary (built without nota-text).";
    };

    encoderPackage = lib.mkOption {
      type = lib.types.package;
      description = ''
        Package providing the deploy encoder `mentci-encode-configuration`
        (built with the nota-text feature). The daemon package must NOT carry
        nota-text; this one does the typed NOTA -> rkyv encode at deploy time.
      '';
    };

    socketName = lib.mkOption {
      type = lib.types.str;
      default = "mentci.sock";
      description = ''
        The Mentci working Unix socket file name under ${runtimeDir}. The daemon
        binds this socket at 0600 itself; egui / CLI clients point at it.
      '';
    };

    criomeMetaSocketPath = lib.mkOption {
      type = lib.types.str;
      default = "/run/criome/criome.sock.meta";
      description = ''
        The criome PRIVATE meta socket (the MetaCriome leg). criome binds its
        working socket at /run/criome/criome.sock and derives the meta socket as
        <socket>.meta. mentci uses this to list parked authorizations and submit
        approvals. Reachable only because mentci runs under the same criome user.
      '';
    };

    personaName = lib.mkOption {
      type = lib.types.str;
      default = "psyche";
      description = "The persona this mentci instance answers as (PersonaName). A bare NOTA atom.";
    };

    personaKeyLabel = lib.mkOption {
      type = lib.types.str;
      default = "home-verdict";
      description = "The persona key label (PersonaKeyLabel). A bare NOTA atom.";
    };

    user = lib.mkOption {
      type = lib.types.str;
      default = "criome";
      description = ''
        The system user mentci runs as. MUST equal the criome service user so
        mentci can open criome's 0600 meta socket — that shared uid IS the
        approval-authority boundary.
      '';
    };
  };

  config = lib.mkIf cfg.enable {
    systemd.services.mentci = {
      description = "mentci human-approval daemon";
      wantedBy = [ "multi-user.target" ];
      # mentci needs criome's meta socket to exist before it binds its bridge.
      after = [ "criome.service" ];
      requires = [ "criome.service" ];
      serviceConfig = {
        Type = "simple";
        Restart = "on-failure";
        User = cfg.user;
        RuntimeDirectory = "mentci";
        ExecStartPre = [ encodeConfigurationScript ];
        ExecStart = "${cfg.daemonPackage}/bin/mentci-daemon ${configRkyv}";
      };
    };
  };
}
```

Two patterns quoted directly from `criome.nix` that this mirrors:

- The `ExecStartPre` encoder wrapper: criome.nix wraps the encoder in `pkgs.writeShellScript "criome-encode-configuration"` with `set -eu` and `${cfg.encoderPackage}/bin/criome-encode-configuration ${lib.escapeShellArg configurationNota}`; mentci.nix is byte-for-byte the same shape with `mentci-` names.
- The one-arg `ExecStart`: criome.nix is `ExecStart = "${cfg.daemonPackage}/bin/criome-daemon ${configRkyv}"`; mentci.nix is `…/mentci-daemon ${configRkyv}`. Single positional rkyv path, no flags — the discipline the criome-node test asserts via `/proc/$PID/cmdline`.

### 2. The combined runNixOSTest (place at `nix/tests/criome-mentci-node.nix`)

One guest imports both modules. criome boots in default `Quorum` mode (criome.nix unchanged) and the testScript flips it to `ClientApproval` over the meta socket using the existing `mentci-criome-pickup-witness-test` driver (it does Configure(ClientApproval)+park, env-driven by `CRIOME_SOCKET`/`CRIOME_META_SOCKET`/`CRIOME_STORE`). Then mentci observes, answers, and we assert criome recorded the grant.

```nix
# criome-mentci-node.nix — a single-node nixosTest that boots BOTH the criome
# daemon and the mentci daemon from the deploy path (typed NOTA -> rkyv in
# ExecStartPre, then `<daemon> <config.rkyv>` with one argument), runs them
# under the SAME criome user so the 0600 meta socket is a real boundary, and
# proves the full ClientApproval escalation loop across the two services:
#
#   (1) Both daemons come up; criome binds its 0600 working + meta sockets and
#       mentci binds its 0600 working socket.
#   (2) criome is flipped to ClientApproval over its META socket at runtime
#       (keeps criome.nix unchanged — it ships the Quorum default).
#   (3) A criome authorization is PARKED over the WORKING socket
#       (EvaluateAuthorization -> AuthorizationPending, a parked slot).
#   (4) mentci ObserveInterfaceState(PendingQuestions) surfaces that parked slot
#       as a pending ApprovalQuestion whose source is
#       ApprovalSource::CriomeEscalation(slot) and whose criome_access is
#       ReadWrite.
#   (5) mentci AnswerQuestion(ApproveSuggestedAnswer) makes the mentci daemon
#       push SubmitAuthorizationApproval(Approve) back over criome's meta socket.
#   (6) criome records the grant: ObserveAuthorization(slot) -> Granted.
#
# Needs /dev/kvm to actually boot; the driver builds and evaluates everywhere.

{
  pkgs,
  criomeDaemonPackage, # criome `default` package: criome-daemon (no nota-text)
  criomeEncoderPackage, # criome `text` package: criome / criome-encode-configuration
  criomeWitnessPackage, # criome witness: mentci-criome-pickup-witness-test + criome-client-approval-witness-test
  mentciDaemonPackage, # mentci daemon (no nota-text)
  mentciEncoderPackage, # mentci `text`: mentci-encode-configuration
  mentciAnswerPackage, # mentci witness: observe + AnswerQuestion driver (see section 3)
  criomeModule,
  mentciModule,
}:

pkgs.testers.runNixOSTest {
  name = "criome-mentci-node";

  nodes.machine =
    { ... }:
    {
      imports = [
        criomeModule
        mentciModule
      ];

      services.criome = {
        enable = true;
        daemonPackage = criomeDaemonPackage;
        encoderPackage = criomeEncoderPackage;
        # criome.nix ships AuthorizationMode::Quorum (the daemon default); we do
        # NOT change criome.nix — the flip to ClientApproval is a runtime meta
        # Configure below.
      };

      services.mentci = {
        enable = true;
        daemonPackage = mentciDaemonPackage;
        encoderPackage = mentciEncoderPackage;
        # Same user as criome so mentci can open criome's 0600 meta socket.
        user = "criome";
        # criome.nix binds /run/criome/criome.sock; the daemon derives the meta
        # socket as <socket>.meta.
        criomeMetaSocketPath = "/run/criome/criome.sock.meta";
      };

      # Both daemons share the criome system user; the criome module already
      # provisions it implicitly via its service. Make it explicit and let mentci
      # ride on it. (If criome.nix does not yet declare a DynamicUser/User, the
      # operator adds `users.users.criome` here — see section 3.)
      systemd.services.mentci.serviceConfig.User = "criome";
    };

  testScript = ''
    start_all()

    # (1) Both daemons come up via the deploy path: each ran its NOTA -> rkyv
    #     ExecStartPre, then `<daemon> <config.rkyv>` with one argument.
    machine.wait_for_unit("criome.service")
    machine.wait_for_unit("mentci.service")

    # criome bound its 0600 working + meta sockets; mentci bound its 0600
    # working socket.
    machine.wait_until_succeeds("test -S /run/criome/criome.sock")
    machine.wait_until_succeeds("test -S /run/criome/criome.sock.meta")
    machine.wait_until_succeeds("test -S /run/mentci/mentci.sock")
    for sock in [
        "/run/criome/criome.sock",
        "/run/criome/criome.sock.meta",
        "/run/mentci/mentci.sock",
    ]:
        mode = machine.succeed(f"stat -c '%a' {sock}").strip()
        assert mode == "600", f"{sock} must be 0600, got {mode}"

    # Deploy discipline: each daemon's argv is exactly one rkyv path, no flags.
    for unit, want in [
        ("criome.service", "/run/criome/criome-config.rkyv"),
        ("mentci.service", "/run/mentci/mentci-config.rkyv"),
    ]:
        argv = machine.succeed(
            f"tr '\\0' '\\n' < /proc/$(systemctl show -p MainPID --value {unit})/cmdline"
        ).strip().split("\n")
        print(unit, "argv:", argv)
        assert argv[-1] == want, f"{unit} last arg must be {want}, got {argv!r}"
        assert not any(a.startswith("--") for a in argv), f"{unit} no flags, got {argv!r}"

    # The same uid owns all three sockets — that shared identity IS the approval
    # boundary mentci crosses and a third party cannot.
    criome_uid = machine.succeed(
        "stat -c '%u' /run/criome/criome.sock.meta"
    ).strip()
    mentci_uid = machine.succeed(
        "stat -c '%u' /run/mentci/mentci.sock"
    ).strip()
    assert criome_uid == mentci_uid, (
        f"mentci must run as criome's uid to cross the 0600 meta boundary, "
        f"criome={criome_uid} mentci={mentci_uid}"
    )

    # (2)+(3) Flip criome to ClientApproval over its META socket and PARK one
    #     authorization over the WORKING socket. The existing
    #     `mentci-criome-pickup-witness-test` does exactly this: meta
    #     Configure(ClientApproval) -> Configured, then working
    #     EvaluateAuthorization -> AuthorizationPending (parked). It is run as
    #     the criome user so it can open the 0600 meta socket, and it prints the
    #     parked slot.
    park = machine.succeed(
        "CRIOME_SOCKET=/run/criome/criome.sock "
        "CRIOME_META_SOCKET=/run/criome/criome.sock.meta "
        "CRIOME_STORE=/var/lib/criome/criome.sema "
        "runuser -u criome -- "
        "${criomeWitnessPackage}/bin/mentci-criome-pickup-witness-test 2>&1"
    )
    print("pickup witness:", park)
    assert "parked" in park, f"criome must park the request, got: {park}"
    parked_slot = park.strip().splitlines()[-1].split("parked", 1)[1].strip()
    print("parked criome slot:", parked_slot)

    # (4)+(5)+(6) Drive mentci: ObserveInterfaceState(PendingQuestions) must
    #     surface the parked slot as a CriomeEscalation question with
    #     criome_access ReadWrite, then AnswerQuestion(ApproveSuggestedAnswer)
    #     makes the mentci daemon push SubmitAuthorizationApproval(Approve) back
    #     over criome's meta socket, recording the grant. The
    #     `mentci-criome-answer-witness-test` (section 3) is the binary driver;
    #     run as the criome user (it speaks the mentci working socket only).
    answered = machine.succeed(
        "MENTCI_SOCKET=/run/mentci/mentci.sock "
        f"EXPECT_CRIOME_SLOT={parked_slot} "
        "runuser -u criome -- "
        "${mentciAnswerPackage}/bin/mentci-criome-answer-witness-test 2>&1"
    )
    print("answer witness:", answered)
    # The witness asserts internally; surface its proofs in the test log.
    assert "OBSERVED CriomeEscalation" in answered, answered
    assert "criome_access=ReadWrite" in answered, answered
    assert "VERDICT ACCEPTED" in answered, answered

    # (6) Independently confirm criome itself records the grant over its WORKING
    #     socket: ObserveAuthorization(slot) -> Granted. The
    #     criome-client-approval-witness-test library path is reused via the
    #     `criome` CLI for a direct read; if no read-only CLI sub-binary is
    #     wired, this is the `mentci-criome-answer-witness-test`'s final proof.
    granted = machine.succeed(
        "CRIOME_SOCKET=/run/criome/criome.sock "
        f"EXPECT_GRANTED_SLOT={parked_slot} "
        "runuser -u criome -- "
        "${criomeWitnessPackage}/bin/criome-observe-authorization-witness-test 2>&1"
    )
    print("grant proof:", granted)
    assert "Granted" in granted, f"criome must record the grant, got: {granted}"

    print(
        "criome+mentci node GREEN: two deploy-encoded daemons (one rkyv arg, no "
        "flags) under one user; criome flipped to ClientApproval and parked a "
        "slot; mentci observed it as a CriomeEscalation ReadWrite question and "
        "answered it; criome recorded the grant."
    )
  '';
}
```

Type/atom names used, all confirmed in source:
- `meta_signal_criome::Input::Configure`, `ObserveParkedAuthorizations`, `SubmitAuthorizationApproval`; `AuthorizationApproval { request_slot, decision: AuthorizationApprovalDecision::Approve }`; `Output::AuthorizationApprovalRecorded` / `ParkedAuthorizationSnapshot` / `Configured`.
- `signal_criome::AuthorizationMode::ClientApproval`, `AuthorizationRequestSlot`, `CriomeReply::AuthorizationPending`, `AuthorizationStatus::Granted`, `ObserveAuthorization`.
- `signal_mentci::ApprovalSource::CriomeEscalation(AuthorizationRequestSlot)`, `MentciRequest::ObserveInterfaceState(InterfaceStateObservation{ interest: InterfaceInterest::PendingQuestions })`, `MentciRequest::AnswerQuestion(ApprovalVerdict{ decision: ApprovalDecision::ApproveSuggestedAnswer })`, `criome_access: CriomeAccess::ReadWrite`, `MentciReply::VerdictAccepted`.

### 3. Flake-package gaps operator wires

The criome packages already exist in the 142 flake; the mentci side and two test-driver bins are net-new. Operator wires these:

| Package arg in the test | Source | Status |
|---|---|---|
| `criomeDaemonPackage` | criome flake `packages.default` (no nota-text, ships `criome-daemon`) | exists in 142 flake |
| `criomeEncoderPackage` | criome flake `packages.text` (nota-text, ships `criome` CLI) | exists, but ships `criome-write-configuration`, NOT `criome-encode-configuration` — see gap (a) |
| `criomeWitnessPackage` | criome flake — a witness package built with `--features cluster-witness --bins`, shipping `mentci-criome-pickup-witness-test`, `criome-client-approval-witness-test`, and a new `criome-observe-authorization-witness-test` | the `cluster-witness` package exists in criome's own flake (`packages.cluster-witness`); the 142 worktree flake does NOT yet export a witness package — operator adds one |
| `mentciDaemonPackage` | mentci flake `packages.default` (no nota-text, ships `mentci-daemon`) | gap (b): **mentci has no flake.nix at all** |
| `mentciEncoderPackage` | mentci flake `packages.text` (nota-text, ships `mentci-encode-configuration`) | gap (b) + gap (c) |
| `mentciAnswerPackage` | mentci flake — a witness package shipping `mentci-criome-answer-witness-test` | gap (d): that binary does not exist yet |

Concrete gaps:

(a) **Encoder bin-name mismatch in the recycled template.** `criome.nix` invokes `${cfg.encoderPackage}/bin/criome-encode-configuration`, and the 142 flake comment says `text` "carries … `criome-encode-configuration`," but the only encoder bin in `criome/Cargo.toml` is `criome-write-configuration` (`src/bin/criome-write-configuration.rs`). No bin named `criome-encode-configuration` is produced anywhere. Operator either renames the criome `[[bin]]` to `criome-encode-configuration` or fixes criome.nix to call `criome-write-configuration`. `mentci.nix` above inherits the same intended name `mentci-encode-configuration`; mentci's real bin is `mentci-write-configuration`, so the same rename/alias applies.

(b) **mentci has no Nix at all.** There is no `mentci/flake.nix` and no `mentci/nix/` module dir. Operator adds a mentci flake (crane, same shape as criome's) exporting `packages.default` (the daemon, no nota-text), `packages.text` (the encoder, `--features nota-text`), and a witness package, plus `nixosModules.mentci = import ./nix/modules/mentci.nix`. mentci's deps are all git-branch crates (`criome`, `signal-criome`, `meta-signal-criome`, `meta-signal-mentci`, `mentci-lib`, `signal-mentci`, `signal-frame`, `kameo`), so the flake needs those inputs or a vendored lock.

(c) **The encoders take positional path args, not the inline-NOTA artifact.** `mentci-write-configuration` reads `<socket-path> <criome-meta-socket> <output-rkyv>` from argv and hardcodes the persona identity (`psyche` / `Persona` / `home-verdict`) and notification clients (`StatusBar`, `Popup`); `criome-write-configuration` reads `<socket> <store> <output>`. So either (i) the operator implements the `mentci-encode-configuration` / `criome-encode-configuration` NOTA-artifact path the modules call (an encoder that parses the single `MentciConfigurationArtifact` / `CriomeConfigurationArtifact` NOTA record into config + output path), or (ii) until then, the modules' `ExecStartPre` calls the positional bin instead. The positional fallback for mentci.nix is a one-line swap:
```nix
encodeConfigurationScript = pkgs.writeShellScript "mentci-encode-configuration" ''
  set -eu
  ${cfg.encoderPackage}/bin/mentci-write-configuration \
    ${lib.escapeShellArg socketPath} \
    ${lib.escapeShellArg cfg.criomeMetaSocketPath} \
    ${lib.escapeShellArg configRkyv}
'';
```
This is fully functional today (it already encodes the `MetaCriome` leg pointed at criome's meta socket); the inline-NOTA artifact form is the eventual contract that matches criome.nix's stated pattern.

(d) **No mentci-side binary driver for observe+answer against a running daemon.** The observe→answer flow is proven in-process in `mentci/tests/criome_bridge.rs::mentci_closed_verdict_approves_criome_escalation_over_meta_socket`, and the criome half has a process-boundary driver (`mentci-criome-pickup-witness-test`), but there is no env-driven binary that talks to a *running* `mentci-daemon` over its working socket to `ObserveInterfaceState` then `AnswerQuestion`. Operator adds `mentci/src/bin/mentci-criome-answer-witness-test.rs` (behind a `witness` feature, like criome's `cluster-witness`): read `MENTCI_SOCKET` + `EXPECT_CRIOME_SLOT`, send `ObserveInterfaceState(PendingQuestions)`, assert one `ApprovalQuestion` whose `proposal.source` is `CriomeEscalation(slot)` and whose `criome_access` is `ReadWrite`, send `AnswerQuestion(ApproveSuggestedAnswer)`, assert `VerdictAccepted`, printing `OBSERVED CriomeEscalation`, `criome_access=ReadWrite`, `VERDICT ACCEPTED`. It can reuse `mentci-egui`'s `DaemonClient` (`observe_interface_state_typed` + `send_request_typed`), or talk raw frames as `criome_bridge.rs`'s `send_mentci` helper does. The grant-confirmation bin `criome-observe-authorization-witness-test` is the same idea on criome's working socket (it already exists as logic inside `criome-client-approval-witness-test::assert_status`; factor it into a standalone bin or fold the grant assertion into the answer witness).

(e) **System user.** criome.nix as shipped uses systemd `StateDirectory`/`RuntimeDirectory` without an explicit `User=` (it runs as root, and `StateDirectoryMode=0700` is root-owned). For the same-user meta boundary to be meaningful and for `runuser -u criome` to work, the operator gives criome.nix a `User = "criome"` (with `users.users.criome`/`users.groups.criome`, or a `DynamicUser` that both services share — note `DynamicUser` allocates per-unit uids and would defeat the shared-uid requirement, so a static `criome` user is the right choice here). mentci.nix already exposes `services.mentci.user` defaulting to `criome`.

### 4. Where to place it

Repo / worktree: the criome NixOS-module repo that houses `criome.nix`:

`/home/li/wt/github.com/LiGoldragon/criome/criome-nixos-module-142/` (the `criome-nixos-module-142` worktree of `github.com/LiGoldragon/criome`).

- `mentci.nix` → `/home/li/wt/github.com/LiGoldragon/criome/criome-nixos-module-142/nix/modules/mentci.nix` (sibling of the existing `nix/modules/criome.nix`).
- combined test → `/home/li/wt/github.com/LiGoldragon/criome/criome-nixos-module-142/nix/tests/criome-mentci-node.nix` (sibling of `nix/tests/criome-node.nix`).
- flake wiring (in that worktree's `flake.nix`): add `nixosModules.mentci = import ./nix/modules/mentci.nix;` next to the existing `nixosModules.criome` (line 203), and add a `checks.<system>.criome-mentci-node = import ./nix/tests/criome-mentci-node.nix { … }` block next to `criome-node` (lines 194–199), passing the packages from section 3.

Caveat for the operator: this module-and-test set lives in the criome NixOS-module repo but depends on **mentci** packages that do not exist yet (gap b). The cleanest landing is for the operator to first stand up the mentci flake (daemon, encoder, witness, `nixosModules.mentci`), then either (i) export `mentci.nix` from the mentci flake and have the 142 flake consume it as an input, or (ii) keep both modules co-located in the 142 worktree (as written above) and add the mentci repo as a flake input solely for its packages. Option (i) is the more honest home for `mentci.nix` long-term (a module belongs with its daemon); the prompt asked for the sibling-of-criome.nix placement, which is option (ii) and is correct for a designer prototype the operator runs on Prometheus.
