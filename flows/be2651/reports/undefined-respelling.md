# Ondyfaind respelled Undefined (ruling 6grp)

## Heads
- `undefined-be2651` on horizon-rs, from origin/main e723ce1: **87e9d58** (pushed, not merged).
- `ethos28-be2651`, from 825a7f0: **182f530** (pushed). Lojix still pins 825a7f0; lojix untouched.

## What changed (each head, one commit)
`lib/ethos/horizon.ethos:67`, `lib/src/generated/horizon.rs` (variant), `lib/src/projection/names.rs:102` (variant and projected string "Undefined"), `lib/tests/archive_roundtrip.rs:9`, `lib/tests/contract.rs:18`. The generated file is a one-token change; build.rs asserts the ethos-zero output equals the file and passed, so it matches regeneration. On ethos28 also `lib/tests/fixtures/definition-0.17.1.datom` (the text fixture, 4 occurrences); the rkyv fixture is untouched and still passes, confirming the archive is by position. MotherBoard is not reshaped.

## Gates
Both ran in the foreground on prometheus with nix-fast-build, exit 0: logs in the scratchpad, `gate-87e9d58.log` and `gate-182f530.log` (…/scratchpad/ of this session; the exit file is `gate-exits.log`). horizon-test built at 0.17.1 and 0.18.0.

## Consumers of the text form or projected name, at origin/main
Search: zoekt returned nothing for the term; rg over /git/github.com/LiGoldragon (all repos), /git/worktrees, ~/primary, ~/private-repos and other home trees.

| Where | Finding | Read by live system? |
|---|---|---|
| horizon-rs main | the 5 files above only; cli and checks have none | built into lojix 0.10.6 via horizon-lib 0.17.1 as the old spelling |
| goldragon `cluster-definition.datom` (the live cluster definition) | no Ondyfaind; every Machine has MotherBoard `None` (e.g. `Some.ThinkPadT14Gen5Intel None Some.12 Some.32 None`) | yes, but carries no text to change |
| lojix (checks/horizon/cluster-definition.datom, tests/fixtures, flake fixture, tests/common/mod.rs, tools/tests/common/mod.rs) | no Ondyfaind; fixtures use `mother_board_option: None` | n/a |
| lojix-test `fixtures/qualification-driver.rs:13,15` | `mother_board_option:None` only | no |
| CriomOS, CriomOS-home `fixtures/horizon-projection.json:27` | `"motherboard": null`; no string consumer | no |
| CriomOS-test-cluster `fixtures/horizon/*.json` | `"motherBoard": null` throughout | no |
| horizon-rs worktrees (codec-7a0079, capability-9228ed, wireless-d76b4c) and ~/private-repos horizon checkouts | stale copies of the same 5 files | no |
| flow reports (2987ba phonetic-*, be2651 lojix-steps-5) | prose mentions | no |

Nothing outside horizon-rs holds the text "Ondyfaind", and no live data uses MotherBoard Some. (Caveat: the local /git/.../lojix and horizon-rs clones are not current; I grepped their origin/main refs after fetch, which also had none, but I did not inspect lojix's in-flight branch.)

## Landing order
Because no cluster definition or fixture outside horizon-rs spells the variant, nothing outside horizon-rs needs editing, and live parsers (horizon-lib 0.17.1) keep reading the unchanged definition either way.
1. Land the ethos28 line (182f530) as the horizon-lib 0.18.0 base, with lojix repinning to it after the other worker's branch settles (lojix pins 825a7f0, so it moves to 182f530).
2. Rebase/merge `undefined-be2651` onto main only if the 0.18.0 line is not taken first; otherwise it is superseded by 182f530.
3. Deploy lojix with the new horizon-lib. Since goldragon's definition holds MotherBoard None, no text change is needed in goldragon at any step.
4. Any future cluster definition that sets MotherBoard must write `Undefined` only after the lojix carrying the new horizon-lib is live on ouranos and zeus.
