# CriomOS website-hosting service — design + the two cloud-node features

Session: cloud-designer, 2026-06-20. Answers three psyche asks: (1) what
the two open cloud-node branches are and whether to land them, (2) a
reliable + secure CriomOS website-hosting service design with the three
best markdown renderers compared, (3) the standing surface-bad-design
principle.

Intent captured this session:
- Spirit `878r` (Decision, Low): [CriomOS provides a website-hosting node
  service so the psyche can host websites: a user configures a source to
  be rendered and served from a node, the service supports multiple
  renderer variants, and the standard default for now is a markdown-based
  static site in the Jekyll mould. The psyche requires the implementation
  be the most reliable and secure way to do it. This is the first
  concrete role doris, the low-trust DigitalOcean cloud node, can fill.]
- Spirit `t5qr` (Principle, Medium): [When debugging or rewriting a part
  of the system, actively evaluate the design of the parts being touched
  and surface any flaw or improvement opportunity to the psyche as you
  find it.]

## Part 1 — the two cloud-node features, and my advice

Both are pushed designer feature branches awaiting an operator main-merge
(designers don't own code-repo main). Both: **land them.**

### Feature A — `cloud-designer-cloud-node-data` (goldragon)

Declares **doris** as a DigitalOcean `CloudNode` in the goldragon cluster
data, across four commits: declare the node, fix its root filesystem to
`/dev/disk/by-label/nixos` (the live-deploy boot fix), set it **low trust
(`Min`)**, and mark it **unprovisioned** with a clearly-labelled
placeholder host key.

**Advise: FOR, and now on the critical path.** Every piece is settled and
proven: the root-device fix is confirmed live on real DigitalOcean
(`deploy=criomos-confirmed`, report 76); the low-trust decision is
psyche-captured (Spirit `5pf6`); the defer-provisioning is psyche-captured
(Spirit `zeqq`). It is clean, tested, and — as of the website-host ask —
doris finally has a role, so landing its declaration is the prerequisite
for the hosting work below.

### Feature B — `cloud-designer-cloud-node-species` (horizon-rs)

Deletes the dead `TypeIs` one-hot struct and derives the `BehavesAs`
facets directly from `NodeSpecies`. 64 tests green; projected JSON drops
`typeIs`, keeps `behavesAs`.

**Advise: FOR.** Pure accretion removal — `TypeIs` was a one-hot mirror of
information already in `NodeSpecies`, with no live consumers (report 77).
Removing it is the surface-bad-design principle (`t5qr`) in action:
behaviour is unchanged (the facets derive identically), the model gets
leaner, and the tests prove it. Low-risk; land it.

Both are independent (data vs. type model) and both block on the same
thing: an operator main-merge. Bead **`primary-n98t` (cloud-node landings)**
tracks the handoff; the website-host bead **`primary-unig`** depends on it.

## Part 2 — the website-hosting service

### What CriomOS already gives us (so we build with the grain)

CriomOS already has the exact mechanism this needs:

- **Typed `NodeService` enum** (`horizon-rs/lib/src/proposal.rs:123`):
  cluster-authored per-node capabilities, projected typed onto each node —
  `TailnetClient`, `NixBuilder { maximum_jobs }`, `NixCache`,
  `PersonaDevelopment { capabilities }`, `VmHost { guest_subnet, kvm,
  maximum_guests }`. Each variant carries its own cluster-authored payload.
- **`node-services.nix`** (`CriomOS/modules/nixos/node-services.nix`): the
  Nix gate. NixOS modules read `horizon.node.services` and switch config on
  the presence (`has`) and payload (`payload`) of a named service.

So the entire integration pattern is: **add one typed `NodeService`
variant + one NixOS module that reads its payload.** This is precisely how
`VmHost` works today.

### The shape: `NodeService::WebHost { sites }`

A new typed variant carrying the per-site configuration:

```
WebHost { sites: Vec<HostedSite> }

HostedSite {
  domain:   Domain,        // the served hostname (ACME-managed TLS)
  source:   SiteSource,    // a pinned flake / git ref the user points at
  renderer: SiteRenderer,  // which generator renders it
}

enum SiteRenderer {        // "define them that way" — typed variants, not string keys
  MarkdownStatic,          // the standard default → Zola (see below)
  // future: Hugo, RawHtml passthrough, …
}
```

The renderer is a **typed enum**, answering the psyche's "I guess we could
even define them that way" — the variants are typed values consistent with
the workspace's typed-domain-values discipline, not string keys. The
default variant `MarkdownStatic` is the Jekyll-style markdown site.

### The security + reliability core: render at build time, serve static at runtime

This is the single most important design decision and the answer to "the
most reliable and secure way":

**The renderer runs at deploy time inside the Nix sandbox and produces an
immutable `/nix/store` artifact of plain HTML. The live node runs only a
static file server. No generator process, no app server, no dynamic code
is ever exposed to the internet.**

Why this is the secure + reliable path:

- **No runtime execution surface.** The public-facing node serves static
  files through hardened nginx only. There is no renderer, interpreter, or
  database listening — the class of bugs that compromises web hosts
  (template injection, deserialization, app-server RCE) does not exist
  because nothing dynamic runs at request time.
- **Reproducible + instantly rollback-able.** Same source → same store
  hash → same site. Each deploy is a full NixOS generation; rollback is a
  generation switch, not a restore.
- **Updates are a re-pin.** The user updates the site by re-pinning the
  source ref and rebuilding; the node switches to the new generation (or
  `BootOnce` for the cautious path, mirroring the `VmHost` discipline).
- **Minimal secrets.** A public static site needs no cluster secrets on
  doris. The only sensitive material is the ACME/TLS private key, scoped to
  the node and rotatable.

### Why doris's LOW trust is exactly right for this role

A public web host is the textbook low-trust node: it terminates TLS for
untrusted public traffic and is the most-exposed surface in the cluster.
Effective node trust is `min(NodeProposal.trust, ClusterTrust.nodes[n],
ClusterTrust.cluster)`. doris at `Min` means that even if the edge is
compromised, it is already floored out of every trusted cluster operation
— not a dispatcher, not fully trusted, holding no cluster secrets. **The
role and the trust level align perfectly** — this retroactively justifies
the low-trust decision (`5pf6`): doris's role *is* the public edge.

### The serving + TLS layer

- **nginx** via `services.nginx` `virtualHosts`, serving the immutable
  store path. NixOS already runs nginx hardened (systemd sandboxing,
  `ProtectSystem`, dropped privileges). Recommended for the proven path.
- **TLS** via `security.acme` (Let's Encrypt, automatic renewal), HSTS,
  no server tokens.
- **Caddy** is the simpler alternative (automatic HTTPS built in, smaller
  config), but nginx is the more battle-tested NixOS default. I recommend
  nginx; Caddy is a reasonable simplification if config ergonomics win.

### The three best markdown renderers

The psyche's "a-la-jekyll" names the *style* (markdown content + templates
→ HTML), not Jekyll the tool — actual Jekyll (Ruby) is the slowest with
the heaviest dependency and is not a contender. The three modern best-in-
class for that style:

| Renderer | Lang | Surface | Ecosystem | Stack fit |
|---|---|---|---|---|
| **Zola** | Rust | Single binary, **no plugin system** (minimal surface) | Smaller theme set | **Best** — Rust-aligned with the whole workspace, in nixpkgs |
| **Hugo** | Go | Single binary, large feature surface | **Largest** themes + community | Good — in nixpkgs, fastest at scale |
| **Eleventy (11ty)** | JS/Node | Flexible, minimal abstraction | Broad templating | Weaker — Node + npm build-time dependency tree |

All three emit zero-JS static HTML by default (strong security baseline)
and are markdown-first. Because we render at build time, the runtime
security is identical across them — the differentiator is **build-time
complexity and dependency surface**, where the single-binary Rust/Go tools
beat the Node option.

**Recommended default: Zola.** A single self-contained Rust binary, *no
plugin system* (deliberately minimal complexity and attack surface),
packaged in nixpkgs, fast, markdown-first, Jekyll-style. It is the closest
fit to "most reliable and secure" and is coherent with the workspace's
all-Rust discipline (easy to vendor, audit, and reason about).
**Alternative: Hugo**, if theme ecosystem and community matter more than a
minimal surface. Eleventy only if its flexibility is specifically needed —
its Node/npm build dependency is a real supply-chain consideration even
though the runtime stays static.

## Part 3 — the four real decisions (yours to make)

1. **Default renderer.** I recommend **Zola** (single Rust binary, no
   plugins, stack-aligned) over Hugo (bigger ecosystem) and Eleventy
   (more flexible, heavier Node deps). Confirm Zola, or prefer Hugo?
2. **Source model.** I recommend **build-time render** (source is a pinned
   flake/git ref, Nix builds the site immutably, the node serves static
   only). The alternative — the node pulls + renders at runtime so users
   update without a redeploy — is more convenient but reintroduces a live
   execution surface on a low-trust public node, which I advise against.
   Confirm build-time-only?
3. **"users can configure" — who, and how?** (a) cluster-authored only
   (the psyche edits `datom.nota`, like every other service) — simplest,
   most secure, and fine while the psyche is the only user; or (b) a
   user-facing per-site config surface the node reads — more literally
   "users configure" but more surface. I'd ship (a) first. Confirm?
4. **Does this provision doris now?** The web host *is* the role doris was
   waiting for, so the defer condition (`zeqq`, "until we have a role for
   it") is arguably met. Provision doris now (mint its real host key,
   stand up the standing droplet) to carry the host, or design the service
   first and provision when it's ready to deploy?

## Part 4 — recommended build order

1. Land features A + B (operator main-merges) — doris declared, node model
   clean. **Status: B (TypeIs deletion) merged to horizon-rs main
   (`bd1cc2c1`); A (doris declaration) blocked on system-designer's
   goldragon lock.**
2. Add `NodeService::WebHost { sites }` + `SiteRenderer` to horizon-rs
   (designer branch) with NOTA round-trip + projection tests. **Status:
   DONE — branch `cloud-designer-web-host` off the post-merge main. Typed
   `HostedSite { domain, source, renderer }`, `ServedDomain`/`SiteSource`
   newtypes, `SiteRenderer` closed enum (`MarkdownStatic` default);
   accessors `NodeService::hosted_sites` + `Node::web_host_sites` mirroring
   `VmHost`; round-trip + projection tests; fmt/test/clippy `-D warnings`
   green. Embodies the recommended defaults; the open decisions below gate
   the NixOS module, not this type.**
3. Add the CriomOS NixOS module that reads the `WebHost` payload: a
   build-time render derivation (Zola) per `HostedSite` → an immutable
   site artifact, served by hardened nginx + ACME TLS.
4. Author doris's `WebHost` service in goldragon `datom.nota` (one site,
   the default markdown variant).
5. Provision doris (decision 4) and deploy; verify the site serves over
   TLS, then sweep or keep per the standing-droplet decision.
