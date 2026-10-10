{
  description = "Flow Nexus contract candidate: ethos files, Check, acceptance tests";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-build = {
      url = "github:LiGoldragon/rust-build";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    ethos-zero = {
      url = "github:LiGoldragon/ethos-zero/b2fa8b0e6bd273f0b590444d19e72083a3c865e9";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
      inputs.rust-build.follows = "rust-build";
    };
  };

  outputs = { self, nixpkgs, flake-utils, rust-build, ethos-zero }:
    flake-utils.lib.eachSystem [ "x86_64-linux" ] (system:
      let
        pkgs = import nixpkgs { inherit system; };
        rust = rust-build.lib.${system}.fromPkgs pkgs;
        inherit (rust) craneLib;
        ethos = ethos-zero.packages.${system}.default;
        ethosFilter = path: type:
          type == "regular" && pkgs.lib.hasSuffix ".ethos" path;
        src = rust.cleanSource {
          root = ./.;
          extraFilters = [ ethosFilter ];
        };
        # Check every contract file; print each line as
        # ethos-zero prints it. Always succeeds: the
        # report is the product.
        checkReport = pkgs.runCommand "flow-ethos-check-report" { } ''
          mkdir -p $out
          for f in ${./ethos}/*.ethos; do
            ${ethos}/bin/ethos-zero "Check.$f" >> $out/check.txt 2>&1 || true
          done
          cat $out/check.txt
        '';
        # Generate the contract and the two test
        # stand-ins into src/generated before cargo runs.
        generate = ''
          mkdir -p src/generated
          for f in ethos/*.ethos tests/fixtures/*.ethos; do
            ${ethos}/bin/ethos-zero "Generate.{ $PWD/$f $PWD/src/generated }" || true
          done
        '';
        common = { inherit src; strictDeps = true; };
        cargoArtifacts = craneLib.buildDepsOnly common;
        test = features: craneLib.cargoTest (common // {
          inherit cargoArtifacts;
          pname = "flow-ethos-candidate-test${if features == "" then "" else "-" + features}";
          preBuild = generate;
          cargoTestExtraArgs =
            (if features == "" then "" else "--features ${features} ")
            + "--no-fail-fast -- --nocapture";
        });
      in {
        packages.check-report = checkReport;
        checks = {
          ethos-check = pkgs.runCommand "flow-ethos-check" { } ''
            cat ${checkReport}/check.txt
            if grep -q '^Rejected' ${checkReport}/check.txt; then exit 1; fi
            touch $out
          '';
          test = test "";
          test-datom = test "datom";
        };
      });
}
