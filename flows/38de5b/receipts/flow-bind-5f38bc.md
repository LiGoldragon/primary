# Flow bind of 5f38bc with its role — 38de5b, 2026-09-25

An Opus subflow of 38de5b did this. It ran against Flow 0.12.1 (`/nix/store/42xmmsnnsjr6pq7q8jj7p0mx9mqxf3cw-flow-0.12.1`, flow `fe709c7`, the `flow-nexus` unit active since 20:37:59). Nothing was Started, Stopped, Sent or Replaced.

## Outcome

**Refused: `DuplicateFlowId`. 5f38bc still has no role.** The request had no effect on the store. At 0.12.1 the Nexus's `MetaBindExisting` arm (`crates/flow-nexus/src/lib.rs` about 350–363) runs `ResolveRecipient` on every binding first. A flow that is already known (`RecipientResolved` or `FlowUnavailable`) is refused as `DuplicateFlowId` before `register_existing_flow` is reached. The store-level role path that `flow-0.12.1-store.md` "Not settled" relied on therefore cannot be reached through this query for a flow that is already stored. In any case `register_existing_flow` also returns `ConflictingBinding` for a node that is not `Pending` (`store.rs` 1534), and the node the arm would build is always Pending. Adding a role to the stored, Active 5f38bc needs a Nexus change or a meta verb that the pinned contract does not have.

## The three facts, checked read-only before sending (none contradicts the ruling)

1. **Aspect: Field.** `flows/5f38bc/log.md`:
   - Its header says the client "resumed the accepted native Field Astra session".
   - The launcher-receipt section it restates gives title `Field Astra 5f38bc` and Herdr agent `field-astra-5f38bc`.
   - The log does not say "High" in words. High comes from the tier: Astra is High in the witnessed receipt `5f38bc/mind-astra-native/receipts/mind-astra.json` (`canonicalRole.power High`, model gpt-6-astra, effort medium, the same effort as 5f38bc's rollout).
2. **Pane.** `herdr agent list` shows `field-astra-5f38bc` on wQ:pN / wQ:tM / `term_65c3ff14cafb070`, with terminal title `Field Astra 5f38bc | primary` and status done.
3. **Model: gpt-6-astra.** The rollout `/home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T13-48-34-01a0d4f6-6bc6-7530-94d6-1515f38bcb84.jsonl` has `"model":"gpt-6-astra"` 485 times and no other model, with `"effort":"medium"`. The live argv (`herdr pane process-info --pane wQ:pN`) also has `-m gpt-6-astra`.

## Live identity

- **Container:** herdr pid 3219203, uid 1001, start token 61814493. This is the `ss -xlp` listener on `messaging-build/herdr.sock`. The owner is 38de5b.
- **Process:** codex pid 2012036, uid 1001. `/proc/2012036/stat` field 22 is 121098091. The cwd is `/home/li/primary`. The argv is `codex resume --remote unix:///home/li/.codex-next/app-server-control/app-server-control.sock -m gpt-6-astra ... 01a0d4f6-6bc6-7530-94d6-1515f38bcb84`.
- These were checked again just before sending, and they were unchanged.

## Validation

meta-signal-flow `fbfe8970247d57e9299e496e89d1845df991c73d` (6.0.4) is the revision flow `fe709c7` pins in Cargo.toml and Cargo.lock. Its `MetaBindExisting` / `FlowBinding` shape is the same as at 29ec97d. In a scratch clone, `cargo test --features datom` ran a one-off test (`bind_5f38bc_datom_is_a_meta_query ... ok`). The text actualizes as `Query::MetaBindExisting` with one binding, `FlowBinding { flow_id: "5f38bc", flow_aspect: Field, power_level: High, model_name: "gpt-6-astra", harness_kind: Codex, ... }`, and it round-trips byte-identical.

## Datom sent (`flow-meta '<datom>'`)
```
MetaBindExisting.{ { messaging-build /home/li/.config/herdr/sessions/messaging-build/herdr.sock { 3219203 1001 61814493 } 38de5b } [ { 5f38bc Field High gpt-6-astra Codex 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 wQ wQ:pN wQ:tM term_65c3ff14cafb070 field-astra-5f38bc { 2012036 1001 121098091 } /home/li/primary } ] }
```

## Reply (verbatim, exit 0)
```
BoundExisting.{ { messaging-build /home/li/.config/herdr/sessions/messaging-build/herdr.sock { 3219203 1001 61814493 } 38de5b } [ Refused.{ 5f38bc DuplicateFlowId } ] }
```

## `flow 'List.{}'`: the 5f38bc row (verbatim)
```
{ 5f38bc 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 Codex Available.{ /home/li/.codex-next/app-server-control/app-server-control.sock Ready } Available.{ messaging-build field-astra-5f38bc wQ:pN term_65c3ff14cafb070 } { 5f38bc 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 unavailable } Active }
```
`flow 'ResolveRecipient.5f38bc'` gave the same content before the send: Active, with its Codex endpoint and Herdr route both Available. Rows in the List have no role position, so this shows the binding did not change. It does not show the role. The role can only be read through `ResolveCaller` from 5f38bc's own pane, which this subflow cannot reach. Following `flow-0.12.1-store.md`, that query is expected to still give `CallerUnknown`.

## Sources
- `LiGoldragon/flow` fe709c7: `crates/flow-nexus/src/lib.rs` (the `MetaBindExisting` arm), `crates/flow-nexus/src/store.rs` (`register_existing_flow`)
- `LiGoldragon/meta-signal-flow` fbfe897: `ethos/signal.ethos`
- `flows/5f38bc/log.md`, `flows/38de5b/reports/route-manifest.md` row 5f38bc, `receipts/flow-bind-live.md`, `receipts/flow-0.12.1-store.md`
