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
    curriculum = {
      url = "github:LiGoldragon/Curriculum/d7bb1375338cb9da30d29f1f7f5182b4766fea26";
      flake = false;
    };
    psyche-context = {
      url = "github:LiGoldragon/psyche-context/53f68b69c3f9a7628e804dcd69cb47cd5db9bb33";
      flake = false;
    };
    mind-context = {
      url = "github:LiGoldragon/mind-context/e3fcd4f36d4f75e8c546e5e9596f5a48a5d8592b";
      flake = false;
    };
    field-context = {
      url = "github:LiGoldragon/field-context/95121c6727052941f7e5f0c1125f8118d737e561";
      flake = false;
    };
    flow = {
      url = "github:LiGoldragon/flow/ac6ab64193f3c4a43009db5a343284977bd33ea7";
      flake = false;
    };
    nixpkgs.url = "github:NixOS/nixpkgs/2d1e72b652ee13fd1297641ce735e06416d22827";
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
      messagingCodecFor =
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.rustPlatform.buildRustPackage {
          pname = "messaging-codec";
          version = "0.1.0";
          src = ./tools/messaging-codec;
          cargoLock.lockFile = ./tools/messaging-codec/Cargo.lock;
        };
      messagingRuntimeFor =
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          messagingCodec = messagingCodecFor system;
          runtimePath = pkgs.lib.makeBinPath [
            pkgs.bash
            pkgs.coreutils
            pkgs.python3
            pkgs.util-linux
          ];
        in
        pkgs.runCommand "primary-messaging-runtime"
          {
            nativeBuildInputs = [ pkgs.makeWrapper ];
          }
          ''
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
      curriculumRuntimeFor =
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.rustPlatform.buildRustPackage {
          pname = "curriculum";
          version = "0.1.0";
          src = curriculum;
          cargoLock = {
            lockFile = "${curriculum}/Cargo.lock";
            outputHashes = {
              "datom-codec-0.32.2" = "sha256-5yoo6p3mS/du8ajWob4y0SiIZvdh2enVyxnriSy8rjo=";
              "ethos-zero-16.0.0" = "sha256-DInSt3pdZSvrDN9zTxmCPVMvaXFILX+ulEYx3FlNxeY=";
              "nexus-0.5.0" = "sha256-ztAbsHMvobXgbkvvi4SG4EwtAqIoMBLvO2LTyI2pGDA=";
              "protos-0.32.2" = "sha256-Sf0CeqeUnfNkPAjz/a5CbJK4Kx1eM+429zll3qtV1VA=";
            };
          };
          cargoBuildFlags = [
            "--features"
            "datom"
            "--bins"
          ];
          cargoInstallFlags = [
            "--path"
            "."
            "--features"
            "datom"
            "--bins"
          ];
          cargoTestFlags = [
            "--all-targets"
            "--features"
            "datom"
          ];
          doCheck = true;
        };
    in
    {
      packages = forAllSystems (system: {
        messaging-runtime = messagingRuntimeFor system;
        curriculum = curriculumRuntimeFor system;
        default = messagingRuntimeFor system;
      });

      apps = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          runtime = curriculumRuntimeFor system;
          messagingRuntime = messagingRuntimeFor system;
        in
        {
          curriculum = {
            type = "app";
            program = "${runtime}/bin/curriculum";
            meta.description = "Send one typed Curriculum request to its Nexus";
          };
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
          default = { type = "app"; program = "${runtime}/bin/curriculum"; };
        }
      );

      checks = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          runtime = curriculumRuntimeFor system;
          messagingCodec = messagingCodecFor system;
          messagingSource = builtins.path {
            path = ./.;
            name = "primary-messaging-source";
            filter = path: type: true;
          };

          contextCompositionCurrent =
            pkgs.runCommand "primary-context-composition-current"
              {
                nativeBuildInputs = [ pkgs.coreutils ];
              }
              ''
                set -eu
                workspace="$TMPDIR/workspace"
                runtime_root="$TMPDIR/runtime"
            mkdir -p "$workspace" "$runtime_root/curriculum"
                cp -R ${self}/. "$workspace/"
                chmod -R u+rwX "$workspace"
                export XDG_RUNTIME_DIR="$runtime_root"
                export CURRICULUM_PSYCHES_REPOSITORY_DIR="${inputs."psyche-context"}"
                export CURRICULUM_CONTEXT_LAYOUT=2
                export CURRICULUM_PSYCHES_REVISION="${inputs."psyche-context".rev}"
                export CURRICULUM_MIND_CONTEXT_DIR="${inputs."mind-context"}"
                export CURRICULUM_MIND_REVISION="${inputs."mind-context".rev}"
                export CURRICULUM_FIELD_CONTEXT_DIR="${inputs."field-context"}"
                export CURRICULUM_FIELD_REVISION="${inputs."field-context".rev}"
                export CURRICULUM_ROLES_FILE="${curriculum}/roles.datom"
                ${runtime}/bin/curriculum-nexus > "$TMPDIR/curriculum-nexus.log" 2>&1 &
                nexus_pid=$!
                trap 'kill "$nexus_pid" 2>/dev/null || true; wait "$nexus_pid" 2>/dev/null || true' EXIT
                socket="$runtime_root/curriculum/curriculum.sock"
                attempts=0
                while [ ! -S "$socket" ]; do
                  if [ "$attempts" -ge 100 ]; then
                    cat "$TMPDIR/curriculum-nexus.log" >&2
                    exit 1
                  fi
                  attempts=$((attempts + 1))
                  sleep 0.1
                done
                query=$(${pkgs.babashka}/bin/bb -e '(require (quote [clojure.edn :as edn]) (quote [clojure.string :as str])) (let [m (:modules (edn/read-string (slurp (first *command-line-args*))))] (println (str "ComposeStartup.{ { Psyche core Secondary } Claude [ " (str/join " " (map name (:system m))) " ] [ " (str/join " " (map name (:user m))) " ] }")))' ${self}/config/main-flow/psyche.edn)
                ${runtime}/bin/curriculum "$query" > "$TMPDIR/composed.datom"
                grep -q '^StartupComposed' "$TMPDIR/composed.datom"
                ${runtime}/bin/curriculum 'ComposeRole.{ illustrator ClaudeAgent }' > "$TMPDIR/role.datom"
                grep -q '^RoleComposed' "$TMPDIR/role.datom"
                touch "$out"
              '';
          bookPhoneCode = pkgs.runCommand "primary-book-phone-code" {
            nativeBuildInputs = [ pkgs.nodejs pkgs.chromium pkgs.coreutils ];
          } ''
            export CHROMIUM="${pkgs.chromium}/bin/chromium"
            export FONTCONFIG_FILE="${pkgs.makeFontsConf { fontDirectories = [ pkgs.dejavu_fonts ]; }}"
            timeout 100s node ${self}/tools/book-phone-code.test.mjs ${self}/tools/book-code.html > "$out"
          '';
          bookPublicationFixtures = pkgs.runCommand "primary-book-publication-fixtures" {
            nativeBuildInputs = [ pkgs.nodejs ];
          } ''
            node ${self}/tools/book-check.test.mjs
            node ${self}/tools/book-fetch.test.mjs
            touch "$out"
          '';
          promptRelayFixtures =
            pkgs.runCommand "primary-prompt-relay-fixtures"
              {
                nativeBuildInputs = [ pkgs.nodejs ];
              }
              ''
                node ${self}/tools/prompt-relay.test.mjs
                touch "$out"
              '';
          componentEvidenceFixtures =
            pkgs.runCommand "primary-component-evidence-fixtures"
              {
                nativeBuildInputs = [ pkgs.nodejs ];
              }
              ''
                node ${self}/tools/component-evidence.test.mjs
                touch "$out"
              '';
          canonicalTitleFixtures =
            pkgs.runCommand "primary-canonical-title-fixtures"
              {
                nativeBuildInputs = [ pkgs.nodejs ];
              }
              ''
                node ${self}/tools/canonical-title-alignment.test.mjs
                touch "$out"
              '';
          claudeNativeSeatFixtures =
            pkgs.runCommand "primary-claude-native-seat-fixtures"
              {
                nativeBuildInputs = [ pkgs.python3 pkgs.nodejs ];
              }
              ''
                node ${self}/tools/main-flow-mode/spirit-system-prompt.test.mjs
                python3 ${self}/tools/claude-native-seat-refresh.test.py
                touch "$out"
              '';
          thirdSeatFixtures =
            pkgs.runCommand "primary-third-seat-fixtures"
              {
                nativeBuildInputs = [ pkgs.nodejs ];
              }
              ''
                node ${self}/tools/third-seat/provider-run.test.mjs
                node ${self}/tools/third-seat/offline-adapter.test.mjs
                touch "$out"
              '';
          fanOutFixtures =
            pkgs.runCommand "primary-fan-out-fixtures"
              {
                nativeBuildInputs = [ pkgs.nodejs ];
              }
              ''
                node ${self}/tools/fan-out.test.mjs
                touch "$out"
              '';
          messagingFixtures =
            pkgs.runCommand "primary-messaging-fixtures"
              {
                nativeBuildInputs = [
                  pkgs.python3
                  messagingCodec
                  pkgs.util-linux
                ];
              }
              ''
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
          direct-start-adapter = pkgs.runCommand "primary-direct-start-adapter" { nativeBuildInputs = [ pkgs.nodejs ]; } ''
            node --test ${self}/tools/claude-main-flow-launch.test.mjs ${self}/tools/codex-main-flow-launch.test.mjs ${self}/tools/flow-start-adapter.test.mjs > "$out"
          '';
          context-composition-current = contextCompositionCurrent;
          book-publication-fixtures = bookPublicationFixtures;
          book-phone-code = bookPhoneCode;
          prompt-relay-fixtures = promptRelayFixtures;
          component-evidence-fixtures = componentEvidenceFixtures;
          canonical-title-fixtures = canonicalTitleFixtures;
          native-seat-fixtures = claudeNativeSeatFixtures;
          third-seat-fixtures = thirdSeatFixtures;
          fan-out-fixtures = fanOutFixtures;
          messaging-fixtures = messagingFixtures;
          default = contextCompositionCurrent;
        }
      );
    };
}
