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
      url = "github:LiGoldragon/Curriculum/7dfa6a81b2e7bd174ce924824497bf39f82c744b";
      flake = false;
    };
    # Pinned to each context repo main head; CriomOS-home follows this cohort.
    psyche-belief = {
      url = "github:LiGoldragon/psyche-belief/8717e76a6582aff93ae074698b5571193c2ede2a";
      flake = false;
    };
    mind-belief = {
      url = "github:LiGoldragon/mind-belief/1850d49feebbb60a61c992c49dc6aee8aef82d8f";
      flake = false;
    };
    field-belief = {
      url = "github:LiGoldragon/field-belief/d7b2cdcaadcff35fcb1e9de34e95bd6a54e750e6";
      flake = false;
    };
    flow = {
      url = "github:LiGoldragon/flow/f111805de99494addb7cb3c3f668723373cfa123";
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
        curriculum = curriculumRuntimeFor system;
        default = curriculumRuntimeFor system;
      });

      apps = forAllSystems (
        system:
        let
          runtime = curriculumRuntimeFor system;
        in
        {
          curriculum = {
            type = "app";
            program = "${runtime}/bin/curriculum";
            meta.description = "Send one typed Curriculum request to its Nexus";
          };
          default = { type = "app"; program = "${runtime}/bin/curriculum"; };
        }
      );
    };
}
