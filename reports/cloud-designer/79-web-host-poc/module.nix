# CriomOS web-host POC module: serve an immutable, build-time-rendered static
# site over hardened nginx. The production form keys these options off the
# typed `horizon.node.services` `WebHost` payload (one `HostedSite` -> one
# virtualHost) and turns on ACME TLS; this POC takes the site package and
# domain directly so it can be demonstrated without cluster data or DNS.
{
  config,
  lib,
  ...
}:
let
  cfg = config.services.criomosWebHostPoc;
in
{
  options.services.criomosWebHostPoc = {
    enable = lib.mkEnableOption "CriomOS web-host POC static serving";

    site = lib.mkOption {
      type = lib.types.package;
      description = ''
        The build-time-rendered immutable static site to serve — the
        `packages.site` derivation (Zola output). Serving a `/nix/store`
        path means the live host runs no renderer.
      '';
    };

    domain = lib.mkOption {
      type = lib.types.str;
      default = "localhost";
      description = ''
        The served hostname. In production this is the ACME-managed TLS name
        carried by the site's `ServedDomain`.
      '';
    };
  };

  config = lib.mkIf cfg.enable {
    services.nginx = {
      enable = true;
      recommendedOptimisation = true;
      recommendedGzipSettings = true;
      recommendedTlsSettings = true;
      # No server-version banner on a public edge.
      serverTokens = false;

      virtualHosts.${cfg.domain} = {
        root = cfg.site;
        # Production adds:
        #   enableACME = true;   # Let's Encrypt via security.acme
        #   forceSSL = true;     # redirect 80 -> 443, HSTS
        # The POC serves plain HTTP on localhost so it needs no real domain
        # or DNS; the Cloudflare token (verified working for zone/DNS reads)
        # is the production DNS + ACME DNS-01 path.
      };
    };

    # A public web edge opens only HTTP/HTTPS.
    networking.firewall.allowedTCPPorts = [
      80
      443
    ];
  };
}
