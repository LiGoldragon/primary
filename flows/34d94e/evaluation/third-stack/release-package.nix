{ pkgs }:
let
  release = pkgs.stdenvNoCC.mkDerivation {
    pname = "opencode-release-member";
    version = "1.17.13";
    src = pkgs.fetchurl {
      url = "https://github.com/anomalyco/opencode/releases/download/v1.17.13/opencode-linux-x64.tar.gz";
      sha256 = "157afa289d1a8d9372de0ce19ac726119b937a1f6b201808d46f06e4e59bb348";
    };
    dontStrip = true;
    dontPatchELF = true;
    unpackPhase = "tar -xzf $src";
    installPhase = ''install -Dm755 opencode "$out/libexec/opencode"'';
  };
in
pkgs.buildFHSEnv {
  name = "opencode";
  targetPkgs = pkgs: [ pkgs.glibc pkgs.stdenv.cc.cc.lib ];
  runScript = "${release}/libexec/opencode";
}
