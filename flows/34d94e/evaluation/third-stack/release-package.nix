{ pkgs }:
pkgs.stdenvNoCC.mkDerivation {
  pname = "opencode";
  version = "1.17.13";
  src = pkgs.fetchurl {
    url = "https://github.com/anomalyco/opencode/releases/download/v1.17.13/opencode-linux-x64.tar.gz";
    sha256 = "157afa289d1a8d9372de0ce19ac726119b937a1f6b201808d46f06e4e59bb348";
  };
  nativeBuildInputs = [ pkgs.autoPatchelfHook ];
  buildInputs = [ pkgs.stdenv.cc.cc.lib ];
  unpackPhase = "tar -xzf $src";
  installPhase = ''
    runHook preInstall
    install -Dm755 opencode "$out/bin/opencode"
    runHook postInstall
  '';
}
