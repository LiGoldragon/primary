{
  description = "CriomOS web-host POC: build-time markdown render (Zola) -> immutable static site served by nginx";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      # The reliable-and-secure core: the renderer runs HERE, at build time,
      # inside the Nix sandbox. The output is an immutable /nix/store path of
      # plain HTML. No generator, app server, or dynamic code ever runs at
      # request time on the host.
      packages.${system} = {
        site = pkgs.stdenvNoCC.mkDerivation {
          pname = "criomos-web-host-poc-site";
          version = "0.1.0";
          src = ./site;
          nativeBuildInputs = [ pkgs.zola ];
          # Zola renders the markdown content into static HTML and writes it
          # straight to the derivation output.
          buildPhase = ''
            runHook preBuild
            zola build --output-dir "$out"
            runHook postBuild
          '';
          dontInstall = true;
        };
        default = self.packages.${system}.site;
      };

      # The deployable form. In CriomOS this is driven off the typed
      # horizon.node.services WebHost payload (one HostedSite -> one
      # virtualHost); the POC takes the site package + domain directly.
      nixosModules.webHost = import ./module.nix;

      # The VM-level proof. nixosTest is QEMU-backed, so it runs only on a
      # VM-testing host (Spirit qnf8): `nix flake check` there boots the
      # module and curls the rendered page. The build+serve+curl proof in
      # 0-poc.md runs anywhere and needs no VM.
      checks.${system}.serve = pkgs.testers.runNixOSTest {
        name = "web-host-poc-serve";
        nodes.machine =
          { ... }:
          {
            imports = [ self.nixosModules.webHost ];
            services.criomosWebHostPoc = {
              enable = true;
              site = self.packages.${system}.site;
              domain = "localhost";
            };
          };
        testScript = ''
          machine.wait_for_unit("nginx.service")
          machine.wait_for_open_port(80)
          machine.succeed("curl -fsS http://localhost/ | grep 'rendered from markdown'")
        '';
      };
    };
}
