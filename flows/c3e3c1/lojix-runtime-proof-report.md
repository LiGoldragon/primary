# Lojix executable-switch proof and exact producer pair

## Result

The proof is complete on two isolated pushed candidate branches. Production source, main, Home, hosts, boot and live Lojix state were untouched.

| Role | Branch | Immutable revision | Tree | Lojix producer |
|---|---|---|---|---|
| B, accepted producer | `flow-c3e3c1-lojix-runtime-proof` | `2abc8e21dd249a9d2ab4aaf1d9c012b4dba0c628` | `e3bd10c4cbf3f0f5eceb057d505bcc4eaad4c4f7` | `da0ad8ad363efe6751efe7e8f01f974bdd10cf06` |
| A, old producer | `flow-c3e3c1-lojix-runtime-proof-old321` | `d7957edc0b71a19faa20b4dfb714432df2d57833` | `fe17684f690da0d0eb6e7d653a2d9cb740fbe7e2` | `321682e0b0d6aafd255c703a444019bddc56e150` |

Both remote refs resolve to the revisions above. A is a child of B solely so their exact delta is one lock-node edit. These are review candidates, not main or materialized host revisions.

## Changed files and invariants

B has parent `20f72cd9fbd61fc70800ac42d013d8df6539ce1e` and changes only `checks/lojix-command-boundary/default.nix`. The binary diff SHA-256 is `3c3b38f665cda1418bd81af4d0fcc0f61bf74ecea53ef4c6da56ed9c5886c1ee`. It turns the focused check into an isolated NixOS VM proof; every production module remains byte-identical to accepted `20f72cd`.

A has parent B and changes only `flake.lock`. The binary pair diff SHA-256 is `ac9fe1ee46c0dff898f438a8542d117b98bf41399abb017a78e3bb0de0105b0f`. The entire parsed lock is equal after removing `nodes.lojix.locked`. The exact locked-node delta is:

| Field | A, old | B, accepted |
|---|---|---|
| `lastModified` | `1794274919` | `1794511691` |
| `narHash` | `sha256-MiG6vSPaUwnUhyawxvQdj3RkAhNF8yqVYQy3FXmlB+k=` | `sha256-N383sKXykHCZoMBp0dDYql1+BvPmaaKEJAADfpmygjk=` |
| `rev` | `321682e0b0d6aafd255c703a444019bddc56e150` | `da0ad8ad363efe6751efe7e8f01f974bdd10cf06` |

The node's `owner`, `repo`, `type`, inputs and original URL are invariant. Every other lock node is invariant. In particular, both revisions retain CriomOS-home `0b430341a594f1b1ee31e986c4dbd0d537e6ffe7` and nixpkgs `9d3b8db48266c17be0b5f9c6360c3ecfbac3d1f5`.

The pair's command-boundary test is byte-identical, SHA-256 `624bafac9520d51e8c617798441a1e532772d0c646410f8dd7e8c7daae8c16fb`. `flake.nix` is byte-identical, SHA-256 `8a8de7b9a96e5c5a1d68819201dffb60a9f68cba3f5124cefc1f52153083aed2`. The production Lojix module is byte-identical, SHA-256 `f38646cdee9c1416b4828b1bead705c8bc6c2c5d5086c49c1d88664f610da41f`.

The two producer revisions export the same five package roles consumed by `lojix-persona-development.nix`: `lojix-nexus`, `lojix`, `lojix-meta`, `offline-tools` and `lojix-bootstrap`. Their producer `flake.nix` and `Cargo.toml` are identical; their own delta is confined to `src/schema_runtime.rs` and `tests/failure_evidence.rs`.

## Real PATH and `/etc` switching proof

The VM fixture uses the production Lojix module with synthetic five-role generation A. A NixOS specialisation selects synthetic five-role generation B. The service is kept out of the fixture's boot target so the synthetic daemon has one behavior: direct launcher identity output.

The VM test:

1. resolves all eight names from the active PATH at `/run/current-system/sw/bin/<name>`;
2. executes every PATH name and requires `a:<name>`;
3. records the real `/etc/lojix/commands` link and all eight resolved target links;
4. activates the declarative B specialisation with its `switch-to-configuration test`;
5. requires the real `/etc` directory link and every target to change, then executes all eight PATH names and requires `b:<name>`;
6. activates the saved A system closure, requires the directory link and every target to equal their original A values, and executes all eight PATH names as A again; and
7. observes `lojix` and `lojix-meta` together at every stage.

It also retains the static stable-launcher, selected-package non-embedding, custom canonical path, invalid path, exact daemon role and exact reset role assertions.

The detailed builder log is `/home/li/primary/flows/c3e3c1/lojix-runtime-proof-builder-b.log`, SHA-256 `28ffa13c003361e7bd0fab439b101dc2922a21359a869933920d59406a7aa64b`. It records both real configuration switches, the 32.77-second completed VM script, and `IMMUTABLE_CHECK_EXIT=0` for B. A's immutable direct import also returned `IMMUTABLE_CHECK_EXIT=0` in `/home/li/primary/flows/c3e3c1/lojix-runtime-proof-builder-a.log`, SHA-256 `11bf9857b9885e433d7303d6d7034570b0f7e799a210cb026ee20126d063f08f`.

The A run reuses the same VM derivation by design: the runtime boundary proof uses synthetic role packages and therefore distinguishes the consumer command boundary from either producer aggregate. Actual old-versus-accepted producer interface and executable coverage is the separate ownership proof below.

## Full ownership failure and independent boundary proof

The complete ownership check and the Home-independent package-boundary proof answer different questions.

The complete check was direct-imported with exact base and candidate inputs. Both full logs exit 1 at the same sole terminal cause, with the same two declaring store paths:

```text
The option `programs.noctalia.enable' in `.../modules/programs/noctalia' is already declared in `.../nix/home-module.nix'.
```

- Immutable base log: `/home/li/primary/flows/c3e3c1/lojix-ownership-full-base.log`, SHA-256 `f4f53557b38129938976644bbec78abd98e82b714a3ef8928687c64b7198e0ae`.
- Candidate log: `/home/li/primary/flows/c3e3c1/lojix-ownership-full-candidate.log`, SHA-256 `6c4dc5647f76a0fe6b3dd4b8fd6427cc03e756f3ff5ac6c283ebf0b991247c1f`.

This establishes the bounded baseline limit; it does not claim the early Home failure exercised later assertions.

The durable independent expression `/home/li/primary/flows/c3e3c1/lojix-ownership-boundary.nix`, SHA-256 `ca10e152a7c76b6ed77e8730dc1516a78f5be12d55cbc7e4e2520f7c30b91ed5`, imports no Home module. Against each immutable pair revision it separately asserts:

- all five configured roles equal the corresponding producer package outputs;
- the daemon unit executes the daemon role's `lojix-nexus`;
- reset executes the offline role's `lojix-reset-store`;
- the ordinary package name remains `lojix`; and
- all eight exact executables exist in their five role packages.

Both immutable revisions pass this check:

- B log: `/home/li/primary/flows/c3e3c1/lojix-ownership-boundary-candidate.log`, SHA-256 `d0914010781b94a906d8d70e4ddf473310d936ac83853b0f8143a21a8b18b931`, `IMMUTABLE_OWNERSHIP_EXIT=0`.
- A log: `/home/li/primary/flows/c3e3c1/lojix-ownership-boundary-a.log`, SHA-256 `fbb4c6ed14fdf80efd8ca320e070407bdcc959d7d679093d0b3247da53a2d311`, `IMMUTABLE_OWNERSHIP_EXIT=0`.

Thus the duplicate Noctalia declaration stays a named full-check baseline gate, while the new Lojix ownership assertions are positively exercised for both producers without a Home repair or override.

## Exact Field A/B materialization request

Astra first reviews and accepts this exact immutable pair:

1. A: `d7957edc0b71a19faa20b4dfb714432df2d57833`;
2. B: `2abc8e21dd249a9d2ab4aaf1d9c012b4dba0c628`.

After that review, Field may realize A and B through Lojix as aggregate materializations, without activating either result. The requested comparison is:

- the system-path closure identity;
- the accounts, D-Bus and polkit identities;
- unit definitions, environments and restart-trigger identities; and
- the expected selected command targets and daemon target for each producer pin.

Field may realize the identical A revision again to show that Lojix reuses the same derivation. This is the aggregate rollback evidence. The isolated VM proof above already establishes the real `/etc/lojix/commands` A-to-B-to-A link switch and executable rollback; no real-host activation or link switch is requested here. Field retains materialization and later runtime authority.

The prior plan and its resolved unknowns are `/home/li/primary/flows/c3e3c1/lojix-runtime-proof-plan.md`. No host evaluation or output was performed.
