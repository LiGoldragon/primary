# CriomOS web-host POC — build-time markdown render, served static

cloud-designer, 2026-06-21. Per the psyche's "go with your leans and make a
POC." A runnable proof of the website-hosting architecture from report 78,
built on my recommended defaults. Artifacts live beside this file
(`flake.nix`, `site/`, `module.nix`, `flake.lock`).

## What the psyche asked, and the leans I took

"I need a website hoster… the most reliable and secure way… users configure
a source… multiple variants… markdown default… the 3 best tools." Report 78
recommended; the psyche said go with my leans. So this POC commits to:

- **Renderer default: Zola** — single Rust binary, no plugin system, in
  nixpkgs, stack-aligned. (`SiteRenderer::MarkdownStatic` maps to it.)
- **Source model: build-time render** — the renderer runs at Nix build time
  in the sandbox; the live node serves static files only.
- **Config: cluster-authored** — the production form reads the typed
  `horizon.node.services` `WebHost` payload; the POC takes the site package
  + domain directly so it runs with no cluster data or DNS.

## What it proves (and the transcript)

The whole point — **render at build time, serve static at runtime** — proven
without a VM or a droplet:

1. **Build-time render → immutable artifact.** `nix build` runs Zola in the
   sandbox and freezes the output into `/nix/store`:

   ```
   $ nix build "path:$PWD#site"
   building '…-criomos-web-host-poc-site-0.1.0.drv' on prometheus…
   → /nix/store/l2lmhkajinb81sdliyn51vdbnzyrrmzm-criomos-web-host-poc-site-0.1.0
   $ ls -la <out>
   dr-xr-xr-x root root  index.html  404.html  robots.txt  sitemap.xml   # read-only, root-owned
   ```

2. **Markdown became HTML.** The source `**rendered from markdown**` rendered
   to real HTML — the render genuinely happened, not a passthrough:

   ```
   $ grep '<h1>' <out>/index.html
       <h1>Hello from CriomOS</h1>
       <p>This page was <strong>rendered from markdown</strong> by Zola at Nix build time…
   ```

3. **Static serving works.** Serving the store path over HTTP answers 200
   with the rendered page:

   ```
   $ curl -fsS -o /dev/null -w 'status=%{http_code} bytes=%{size_download}\n' http://127.0.0.1:8731/
   status=200 bytes=662
   ```

The `nix build` used the pinned `nixpkgs` (`flake.lock`, 2026-06-16) and
Zola 0.22.1 from the binary cache — reproducible, no ambient toolchain.

## Why this is the reliable + secure shape

The served artifact is read-only in `/nix/store` and contains only static
files. **No renderer, app server, or database runs at request time** — the
class of web-host RCE bugs cannot exist because nothing dynamic is exposed.
Same source → same store hash → same site; a redeploy is a generation
switch, rollback is instant. This is exactly why doris's **low trust** fits:
a public static edge holds no secrets and is floored out of trusted cluster
operations if breached.

## The deployable form (code, ready to land)

- **`module.nix`** — `services.criomosWebHostPoc`: hardened nginx
  (`serverTokens = false`, recommended TLS/gzip/optimisation) serving the
  site package, firewall opened only on 80/443. Production turns on
  `enableACME` + `forceSSL`; DNS and ACME DNS-01 go through the Cloudflare
  token (verified working for zone/DNS reads by pi-operator, report 12).
- **`flake.nix` `checks.serve`** — a nixosTest that boots the module and
  curls the page. It is QEMU-backed, so it runs on a VM-testing host
  (Spirit `qnf8`); `nix flake check` there is the VM-level proof. Not run
  here (this is not a VM-testing host) — the build+serve+curl above is the
  host-independent proof.

## How it maps to the typed model (already landed)

The horizon-rs `NodeService::WebHost { sites: Vec<HostedSite> }` (branch
`cloud-designer-web-host`) is the cluster-data half: each `HostedSite
{ domain, source, renderer }` becomes one nginx virtualHost serving one
build-time-rendered `packages.site`. `ServedDomain` → the ACME TLS name,
`SiteSource` → the pinned source the derivation builds, `SiteRenderer` →
which generator the module invokes (Zola for `MarkdownStatic`).

## What's left to land the real thing (lock-blocked)

The production integration touches repos system-designer currently holds, so
it is sequenced, not done:

1. Merge `cloud-designer-web-host` → horizon-rs main (operator; bead
   `primary-n98t`).
2. Add the real CriomOS module reading the `WebHost` payload (this POC's
   `module.nix` generalized over `horizon.node.services`) — **CriomOS
   locked** (system-designer fix-it-all).
3. Author doris's `WebHost` service + land the doris declaration in goldragon
   `datom.nota` — **goldragon locked** (system-designer VmHost/TestVm).
4. Provision doris and deploy (the `zeqq` defer condition is met — the host
   is doris's role).

The POC de-risks all four: the pipeline is proven, the module shape is
written, and the only remaining work is wiring it to the cluster data and the
real droplet once the locks free.
