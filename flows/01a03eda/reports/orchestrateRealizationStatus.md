# Orchestrate realization status

The approved Orchestrate contract is partially realized. The two former syntax blockers are now ruled: Datom Integer uses canonical bare decimal syntax, and the observation selection is `Observe.Locks`.

## Landed producers

- Protos `1e089017531985e11bda46814cab1bb7601d23f2`, v0.7.0: headless guillemet blocks.
- Datom `064829e2aef30854e8fb91c4a55f0bdde8a98a0b`, v0.4.0: typed roots, guillemet maps, and curly-quoted plain Strings.
- signal-frame `000d86684d91ab6b38dd0bce7a5d8bae6db7b147`, v0.4.0: Dotos-only duplicate payload-head restriction removed; repeated reply payload types proven at the binary frame layer.
- ethos-monolith `7c6299aacef54cd9d3b03177af33d61ba4fcecf5`, v0.5.1, then `22cde50c7a6494538902d51317accaafe55c47da`, v0.5.2: Protos alignment, Datom structural generation, and Operation root projection.
- Protos `3b190f9fc2c2a074ceeb6ababfea89e3dd504996`, v0.8.0, and Datom `4e13442be314ebfdf7bbd32d095c88a084bde42e`, v0.5.0: dotted-bare headed units, strict canonical `i64`, and generic `DatomHeadedUnit`.
- ethos-monolith `5fd6aa4c5cf24aff65e5b99406aa773b9cdc2640`, v0.5.3: generic headed-unit operation projection.
- signal-orchestrate `6fc8c5b7f1880b73461a4ffa863a3f8952245c0a`, v0.17.0: approved Interface 0.2.0 / channel 1/5 contract, exact `Observe.Locks`, canonical Integer behavior, and clean rejection of the legacy ordinary interface.

## Preserved pending work

Signal-orchestrate is complete, green, pushed, and handed to the Nexus lane.

Orchestrate has a red ordinary-contract fixture and implemented trait/store work for atomic acquisition, durable non-reused IDs, complete replies, typed conflicts, canonical current snapshot, legacy-row refusal, and a read-only zero-argument upgrade preflight. It remains uncommitted until the Signal producer exists.

The formerly generated `Observe.{Locks.{Current}}` is superseded. The living ruled the request spelling `Observe.Locks`; future categories are sibling selections such as `Observe.ExpiredLocks`.

## Deployment chain

After the Integer surface is ruled and realized:

1. Land and gate signal-orchestrate.
2. Pin it in Orchestrate; finish CLI Datom fixtures, store/restart/legacy tests, and land Orchestrate.
3. Run the read-only legacy-store preflight and require zero active legacy rows before activation.
4. Update the four authored Curriculum skills, then regenerate Primary's consumer trees.
5. Update and gate CriomOS-home's live service-path fixture and immutable Orchestrate pin.
6. Update CriomOS's Home/Orchestrate pins and stale ownership assertion.
7. Deploy the immutable Home revision to `goldragon/ouranos/li` through Lojix, observe terminal success through the node ledger, and witness Lock, Observe, Release-by-ID, and empty Observe against the live Nexus.

## Sources

- Flow `01a03eda` psyche and design records.
- Realization subflows `realize_string_delimiters`, `implement_signal_contract`, `implement_orchestrate_nexus`, and `prepare_orchestrate_deployment`.
- Pushed producer revisions listed above.
