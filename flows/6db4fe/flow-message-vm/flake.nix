{
  description = "Disposable Flow and Message candidate VM experiment";

  inputs = {
    flow.url = "github:LiGoldragon/flow/1b57de018a821e73d5cc31662ad107cb38d65736";
    message.url = "github:LiGoldragon/message/580021b936914b2a0585db1b99cc21a5595d0224";
    nixpkgs.follows = "flow/nixpkgs";
  };

  outputs = { self, flow, message, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      flowPackage = flow.packages.${system}.default;
      messagePackage = message.packages.${system}.default;
      configuration = pkgs.writeShellScript "flow-message-vm-configure" ''
        set -eu
        mkdir -p /var/lib/flow-message-vm /run/flow-message-vm
        ${messagePackage}/bin/message-write-configuration \
          "{(/run/flow-message-vm/message.sock 384 /run/flow-message-vm/owner.sock 384 /run/flow-message-vm/router.sock [] UnixUser.0) /var/lib/flow-message-vm/message.sema vm /var/lib/flow-message-vm/message.rkyv}"
      '';
    in {
      checks.${system}.candidate-vm = pkgs.testers.runNixOSTest {
        name = "flow-message-candidate-raw-vm";
        nodes.machine = { ... }: {
          virtualisation.memorySize = 2048;
          environment.systemPackages = [ flowPackage messagePackage ];
          systemd.tmpfiles.rules = [
            "d /run/user/1001 0700 root root -"
            "d /home/li/.local/state/flow 0700 root root -"
            "d /run/flow-message-vm 0700 root root -"
          ];
          systemd.services.flow-candidate = {
            wantedBy = [ "multi-user.target" ];
            after = [ "systemd-tmpfiles-setup.service" ];
            serviceConfig.ExecStart = "${flowPackage}/bin/flow-nexus";
          };
          systemd.services.message-candidate = {
            wantedBy = [ "multi-user.target" ];
            after = [ "systemd-tmpfiles-setup.service" ];
            serviceConfig = {
              ExecStartPre = configuration;
              ExecStart = "${messagePackage}/bin/message-nexus /var/lib/flow-message-vm/message.rkyv";
            };
          };
        };
        testScript = ''
          machine.start()
          machine.wait_for_unit("flow-candidate.service")
          machine.wait_for_unit("message-candidate.service")
          machine.wait_for_file("/run/user/1001/flow/flow.sock")
          machine.wait_for_file("/run/flow-message-vm/message.sock")

          flow = machine.succeed("FLOW_SOCKET=/run/user/1001/flow/flow.sock ${flowPackage}/bin/flow 'ResolveRecipient.vm-missing'")
          assert "RecipientResolutionRejected" in flow and "UnknownFlow" in flow, flow

          message = machine.succeed("MESSAGE_SOCKET=/run/flow-message-vm/message.sock ${messagePackage}/bin/message 'QueryDeliveryReceipts.{vm-event [ vm-recipient ]}'")
          assert "Missing" in message and "vm-recipient" in message, message
        '';
      };
    };
}
