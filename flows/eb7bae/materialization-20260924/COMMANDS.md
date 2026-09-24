# Evidence commands

All materializing Nix invocations used the configured Prometheus builder with
local jobs disabled and fallback disabled. The commands below are the exact
successful evidence-producing invocations, with `lane` and `artifact` expanded
only for readability.

```sh
lane=/home/li/primary/flows/eb7bae/materialization-20260924

nix build -L --no-link --print-out-paths --max-jobs 0 \
  --option fallback false \
  'github:LiGoldragon/goldragon/8c4d03de76907f590072c0998b00037330ebcd82#horizon-definition'

artifact=/nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition

nix run -L --max-jobs 0 --option fallback false \
  'github:LiGoldragon/goldragon/8c4d03de76907f590072c0998b00037330ebcd82#horizon-cli' \
  -- --node prometheus \
  <"$artifact/horizon-definition.datom" \
  >"$lane/generated/prometheus.json"

nix run -L --max-jobs 0 --option fallback false \
  'github:LiGoldragon/goldragon/8c4d03de76907f590072c0998b00037330ebcd82#horizon-cli' \
  -- --node ouranos \
  <"$artifact/horizon-definition.datom" \
  >"$lane/generated/ouranos.json"
```

The disconnected Lojix 6.0.0 pre-socket check used the installed client from
`/nix/store/a32y4pgaircllhc8kshqr0cvlip5y76l-lojix-6.0.0/bin/lojix-meta`:

```sh
LOJIX_OWNER_SOCKET="$lane/nonexistent-owner.sock" lojix-meta \
  'Deploy.Host.{ goldragon prometheus BaseHost /nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom NoSecrets github:LiGoldragon/CriomOS/59b3229436d0f101e779c14b7ed4ee0f71507540 { ssh-ng://nix-ssh@prometheus.goldragon.criome nix-ssh@prometheus.goldragon.criome } Horizon { nixosConfigurations.prometheus.config.system.build.toplevel } NixosSystemdBootV1 TestActivation ResolveAndRecord Some.@/etc/nix/machines [] }'
```

It exited 2 with `(CliRejected [Datom request did not decode: proposal source
is not a Horizon definition])`. The deliberately nonexistent socket remained
absent, proving the check stopped before socket exchange.

Schema assertions were derived directly from the generated JSON with `jq`:

```sh
jq '.node.network.routerInterfaces' "$lane/generated/prometheus.json"
jq '{network:.node.network, capabilityKinds:[.node.capabilities[]?.kind]}' \
  "$lane/generated/ouranos.json"
rg -n -i 'usb|routerInterfaces|network' \
  "$lane/generated/prometheus.json" "$lane/generated/ouranos.json"
```

