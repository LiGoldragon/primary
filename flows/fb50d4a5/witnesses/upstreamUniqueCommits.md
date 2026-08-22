# Upstream unique commits

Method: probe `gh api repos/LiGoldragon/kameo/compare/3486e4f63ea4e87123476cfbdefeb12403540306...b4aaee797cc3fd12e8194db406d9d73a6bc021ce --jq '.commits[] | [.sha, .commit.author.date, (.commit.message | split("\\n")[0])] | @tsv'`

The forge returned exactly 49 commits unique to upstream relative to fork head `3486e4f6`; the comparison URL is the authoritative full list. The returned set runs from `fcd846e6c2a3122ca44eb0fb972442d3b540b524` (`chore: fix typos (#342)`) through `b4aaee797cc3fd12e8194db406d9d73a6bc021ce` (`chore(deps): update syn requirement from 2.0.52 to 3.0.2 (#383)`). Notable unique API/architecture commits in that set are:

- `ae17f01270c5d578ebc404749a91792d774da42a`, ActorRef lifecycle deadlock fixes and panic catching (#340).
- `bddbbf015eec2392947778cceed216cb5889c2f6`, preserve pending mailbox messages (#345).
- `78617ddbf1962f5033513d5af8fd86233daa2125`, console actor-system TUI (#343).
- `0750d5a731669f6d473c441afc79fc7835f7a954`, per-actor reply timeout (#354).
- `3e01df19aa6d9424b18322dcaeb44cfce82eb7cc`, supervision drain behavior (#351).
- `4d897f2c5418fd0b297bd3fbfe49f174c382b3d1`, `ctx.pipe` and `ctx.pipe_with` (#360).
- `e8a0bce041af295eb3c013be08b5282fda4d9b7b`, reject new messages after graceful stop (#362).
- `c1c14b95f0efe41c532345438802c19cc9d8d19c`, `on_undelivered` hook (#363).
- `39018860114723a86c705b37c62ae3d3c0511426`, single-Arc ActorRef clone (#365).
- `1c66bf9d16f80cd374283616fdbbebd49a4df61b`, FutureActor (#372).
- `1315c811994d6ded956c4f821438a8e5f63e3556`, tracing span root/linking change (#382).
- `90138758779d2260798c41cfaa47598db84f05b8`, release v0.22.2 (#374).

## Sources

- https://github.com/LiGoldragon/kameo/compare/3486e4f63ea4e87123476cfbdefeb12403540306...b4aaee797cc3fd12e8194db406d9d73a6bc021ce
