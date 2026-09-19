{
  description = "Isolated localhost Unity/Mentci/Persona POC build";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    crane.url = "github:ipetkov/crane";
    fenix = {
      url = "github:nix-community/fenix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    signal-mentci-source = {
      url = "path:/home/li/primary/repos/signal-mentci";
      flake = false;
    };
    unity-web-source = {
      url = "path:/home/li/primary/flows/0ab019/unity-web-draft";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, flake-utils, fenix, crane, signal-mentci-source, unity-web-source }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        toolchain = fenix.packages.${system}.complete.withComponents [ "cargo" "rustc" "rustfmt" ];
        wasmToolchain = fenix.packages.${system}.combine [
          toolchain
          fenix.packages.${system}.targets.wasm32-unknown-unknown.latest.rust-std
        ];
        source = pkgs.runCommand "unity-local-poc-source" { } ''
          mkdir -p $out/third-party
          cp -r ${self}/. $out/
          cp -r ${signal-mentci-source} $out/third-party/signal-mentci
          chmod -R u+w $out
          substituteInPlace $out/Cargo.toml \
            --replace-fail '../../../repos/signal-mentci' 'third-party/signal-mentci'
        '';
        manifestFilter = path: type:
          type == "directory" || builtins.baseNameOf path == "Cargo.toml"
          || builtins.baseNameOf path == "Cargo.lock";
        manifestSource = builtins.path {
          path = ./.;
          name = "unity-local-poc-manifests";
          filter = manifestFilter;
        };
        signalManifestSource = builtins.path {
          path = signal-mentci-source;
          name = "signal-mentci-manifests";
          filter = manifestFilter;
        };
        manifestClosureSource = pkgs.runCommand "unity-local-poc-manifest-closure-source" { } ''
          mkdir -p $out/third-party
          cp -r ${manifestSource}/. $out/
          cp -r ${signalManifestSource}/. $out/third-party/signal-mentci
          chmod -R u+w $out
          substituteInPlace $out/Cargo.toml \
            --replace-fail '../../../repos/signal-mentci' 'third-party/signal-mentci'
        '';
        cargoClosure = pkgs.runCommand "unity-local-poc-cargo-closure" {
          nativeBuildInputs = [ toolchain ];
          outputHashMode = "recursive";
          outputHashAlgo = "sha256";
          outputHash = "sha256-cfefMv6cVwx5++gayAzT0DwD83ArXg36HjZkJjQboBA=";
        } ''
          cp -r ${manifestClosureSource} work
          chmod -R u+w work
          export CARGO_HOME=$TMPDIR/cargo-home
          mkdir -p "$CARGO_HOME"
          cd work
          mkdir -p $out
          cp Cargo.lock $out/Cargo.lock
          cargo vendor --locked --versioned-dirs vendor > $out/config.toml
          cp -r vendor $out/vendor
        '';
        sourceWithVendor = pkgs.runCommand "unity-local-poc-source-with-vendor" { } ''
          cp -r ${source} $out
          chmod -R u+w $out
          ln -s ${cargoClosure}/vendor $out/vendor
        '';
        signalProjection = pkgs.runCommand "unity-poc-signal-mentci-projection" {
          nativeBuildInputs = [ toolchain pkgs.stdenv.cc ];
        } ''
          cp -r ${sourceWithVendor} work
          chmod -R u+w work
          export CARGO_HOME=$TMPDIR/cargo-home
          export SIGNAL_PROJECTION_OUT=$out/signal.rs
          mkdir -p "$CARGO_HOME" $out
          cd work
          mkdir -p .cargo
          cp ${cargoClosure}/config.toml .cargo/config.toml
          substituteInPlace third-party/signal-mentci/build.rs \
            --replace-fail 'assert_eq!(' 'std::fs::write(std::env::var_os("SIGNAL_PROJECTION_OUT").expect("projection path"), &generated).expect("projection write"); assert_eq!('
          cargo build --offline --locked -p browser-signal-codec || test -s $out/signal.rs
          test -s $out/signal.rs
        '';
        rustPlatform = pkgs.makeRustPlatform { cargo = toolchain; rustc = toolchain; };
        wasmBindgenRelease = pkgs.fetchurl {
          url = "https://github.com/rustwasm/wasm-bindgen/releases/download/0.2.127/wasm-bindgen-0.2.127-x86_64-unknown-linux-musl.tar.gz";
          hash = "sha256-YdSn3IWs+g0jVMzAuDYZKMflKnRtF/KOuqeV7T3BYUo=";
        };
        browserCodecWasm = pkgs.runCommand "unity-poc-browser-signal-codec-wasm" {
          nativeBuildInputs = [ wasmToolchain pkgs.stdenv.cc ];
        } ''
          cp -r ${sourceWithVendor} work
          chmod -R u+w work
          export CARGO_HOME=$TMPDIR/cargo-home
          mkdir -p "$CARGO_HOME"
          cd work
          mkdir -p .cargo
          cp ${cargoClosure}/config.toml .cargo/config.toml
          cargo build --offline --locked --release \
            --target wasm32-unknown-unknown -p browser-signal-codec
          mkdir bindgen
          tar -xzf ${wasmBindgenRelease} -C bindgen --strip-components=1
          mkdir -p $out/browser-signal-codec/pkg
          bindgen/wasm-bindgen --target web \
            --out-dir $out/browser-signal-codec/pkg \
            target/wasm32-unknown-unknown/release/browser_signal_codec.wasm
        '';
        assets = pkgs.runCommand "unity-poc-assets" { } ''
          mkdir -p $out/unity-web-draft
          cp ${unity-web-source}/index.html $out/unity-web-draft/index.html
          cp ${unity-web-source}/app.js $out/unity-web-draft/app.js
          cp ${unity-web-source}/unity.css $out/unity-web-draft/unity.css
          mkdir -p $out/unity-local-poc/browser-signal-codec
          cp -r ${browserCodecWasm}/browser-signal-codec/pkg \
            $out/unity-local-poc/browser-signal-codec/pkg
        '';
      in {
        packages.cargoClosure = cargoClosure;
        packages.signalProjection = signalProjection;
        packages.browserCodecWasm = browserCodecWasm;
        packages.assets = assets;
        packages.default = rustPlatform.buildRustPackage {
          pname = "unity-local-poc";
          version = "0.1.0";
          src = sourceWithVendor;
          cargoLock.lockFile = "${cargoClosure}/Cargo.lock";
          cargoVendorDir = "vendor";
          preBuild = ''
            mkdir -p .cargo
            cp ${cargoClosure}/config.toml .cargo/config.toml
          '';
          cargoBuildFlags = [ "--workspace" ];
          cargoTestFlags = [ "--workspace" ];
        };
      });
}
