{
  description = "primary workspace generated skill surfaces";

  inputs = {
    dotos = {
      url = "github:LiGoldragon/dotos/e19699933dabd09842c4423d15a704ce3d48b493";
      flake = false;
    };
    dotos-config = {
      url = "github:LiGoldragon/dotos-config/4fbf66d82c645d113ed7c3448c05218d1c8d7095";
      flake = false;
    };
    dotos-text-query = {
      url = "github:LiGoldragon/dotos-text-query/acf6b4b935443602f0bf575adfb22e974c5dde53";
      flake = false;
    };
    tree-sitter-dotos = {
      url = "github:LiGoldragon/tree-sitter-dotos/a00d147463e0ba620e17e186803217e86487bce2";
      flake = false;
    };
    curriculum-deploy = {
      url = "github:LiGoldragon/curriculum-deploy/dc7f70edce08";
      inputs.curriculum.follows = "curriculum";
    };
    curriculum = {
      url = "github:LiGoldragon/Curriculum/d63563f908d7a84a02a3b0d50ef53c98b6b6fd5c";
      flake = false;
    };
    nixpkgs.follows = "curriculum-deploy/nixpkgs";
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      curriculum,
      ...
    }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
      messagingCodecFor = system:
        let pkgs = import nixpkgs { inherit system; };
        in pkgs.rustPlatform.buildRustPackage {
          pname = "messaging-codec";
          version = "0.1.0";
          src = ./tools/messaging-codec;
          cargoLock.lockFile = ./tools/messaging-codec/Cargo.lock;
        };
      messagingRuntimeFor = system:
        let
          pkgs = import nixpkgs { inherit system; };
          messagingCodec = messagingCodecFor system;
          runtimePath = pkgs.lib.makeBinPath [ pkgs.bash pkgs.coreutils pkgs.python3 pkgs.util-linux ];
        in pkgs.runCommand "primary-messaging-runtime" {
          nativeBuildInputs = [ pkgs.makeWrapper ];
        } ''
          mkdir -p "$out/bin" "$out/libexec"
          cp ${./tools/msg} "$out/libexec/msg"
          cp ${./tools/msg-psyche-poc} "$out/libexec/msg-psyche-poc"
          cp ${./tools/messenger} "$out/libexec/messenger"
          cp ${./tools/messaging.py} "$out/libexec/messaging.py"
          cp ${./tools/field-watcher} "$out/libexec/field-watcher"
          chmod u+x "$out/libexec/msg" "$out/libexec/msg-psyche-poc" "$out/libexec/messenger" "$out/libexec/messaging.py" "$out/libexec/field-watcher"
          patchShebangs "$out/libexec/msg" "$out/libexec/msg-psyche-poc" "$out/libexec/messenger" "$out/libexec/messaging.py" "$out/libexec/field-watcher"
          makeWrapper "$out/libexec/msg-psyche-poc" "$out/bin/msg-psyche-poc" \
            --set MESSAGING_CODEC ${messagingCodec}/bin/messaging-codec \
            --prefix PATH : ${runtimePath}
          makeWrapper "$out/libexec/messenger" "$out/bin/messenger-runtime" \
            --set MESSAGING_CODEC ${messagingCodec}/bin/messaging-codec \
            --prefix PATH : ${runtimePath}
        '';
    in
    {
      packages = forAllSystems (system: {
        messaging-runtime = messagingRuntimeFor system;
        default = messagingRuntimeFor system;
      });

      apps = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          runtime = inputs."curriculum-deploy".packages.${system}.default;
          wrappedRuntime =
            appName: description:
            let
              script = pkgs.writeShellApplication {
                name = appName;
                text = ''
                  if [ "$#" -ne 1 ]; then
                    echo "usage: ${appName} 'Operation.{ data-root workspace-root }'" >&2
                    exit 2
                  fi
                  exec "${runtime}/bin/curriculum-deploy" "$1"
                '';
              };
            in
            {
              type = "app";
              program = "${script}/bin/${appName}";
              meta.description = description;
            };

          generateSkills = wrappedRuntime "generate-skills" "Run one typed Curriculum deployment request";
          checkSkills = wrappedRuntime "check-skills" "Run one typed Curriculum deployment check request";
          messagingRuntime = messagingRuntimeFor system;
        in
        {
          generate-skills = generateSkills;
          check-skills = checkSkills;
          msg-psyche-poc = {
            type = "app";
            program = "${messagingRuntime}/bin/msg-psyche-poc";
            meta.description = "Run the controlled unauthenticated Mentci POC ingress bridge";
          };
          messenger-runtime = {
            type = "app";
            program = "${messagingRuntime}/bin/messenger-runtime";
            meta.description = "Run the durable typed messaging runtime";
          };
          default = generateSkills;
        });

      checks = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          runtime = inputs."curriculum-deploy".packages.${system}.default;
          messagingCodec = messagingCodecFor system;
          messagingSource = builtins.path {
            path = ./.;
            name = "primary-messaging-source";
            filter = path: type: true;
          };

          generatedSkillsCurrent = pkgs.runCommand "primary-generated-skills-current" { } ''
            ${runtime}/bin/curriculum-deploy \
              "Check.{ ${curriculum} ${self} }"
            touch "$out"
          '';
          promptRelayFixtures = pkgs.runCommand "primary-prompt-relay-fixtures" {
            nativeBuildInputs = [ pkgs.nodejs ];
          } ''
            node ${self}/tools/prompt-relay.test.mjs
            touch "$out"
          '';
          componentEvidenceFixtures = pkgs.runCommand "primary-component-evidence-fixtures" {
            nativeBuildInputs = [ pkgs.nodejs ];
          } ''
            node ${self}/tools/component-evidence.test.mjs
            touch "$out"
          '';
          thirdSeatFixtures = pkgs.runCommand "primary-third-seat-fixtures" {
            nativeBuildInputs = [ pkgs.nodejs ];
          } ''
            node ${self}/tools/third-seat/provider-run.test.mjs
            node ${self}/tools/third-seat/offline-adapter.test.mjs
            touch "$out"
          '';
          fanOutFixtures = pkgs.runCommand "primary-fan-out-fixtures" {
            nativeBuildInputs = [ pkgs.nodejs ];
          } ''
            node ${self}/tools/fan-out.test.mjs
            touch "$out"
          '';
          messagingFixtures = pkgs.runCommand "primary-messaging-fixtures" {
            nativeBuildInputs = [ pkgs.python3 messagingCodec pkgs.util-linux ];
          } ''
            cp -R ${messagingSource} "$TMPDIR/source"
            chmod -R u+rwX "$TMPDIR/source"
            cp ${./tools/msg} "$TMPDIR/source/tools/msg"
            cp ${./tools/messenger} "$TMPDIR/source/tools/messenger"
            patchShebangs "$TMPDIR/source/tools/msg" "$TMPDIR/source/tools/msg-psyche-poc" "$TMPDIR/source/tools/messenger" "$TMPDIR/source/tools/field-watcher"
            MESSAGING_CODEC=${messagingCodec}/bin/messaging-codec \
              python "$TMPDIR/source/tools/test_messaging.py"
            touch "$out"
          '';
        in
        {
          generated-skills-current = generatedSkillsCurrent;
          prompt-relay-fixtures = promptRelayFixtures;
          component-evidence-fixtures = componentEvidenceFixtures;
          third-seat-fixtures = thirdSeatFixtures;
          fan-out-fixtures = fanOutFixtures;
          messaging-fixtures = messagingFixtures;
          default = generatedSkillsCurrent;
        });
    };
}
