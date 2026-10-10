# CriomOS source revision

## Result

The exact pushed immutable CriomOS candidate representing the current public
`main` is:

```text
github:LiGoldragon/CriomOS/d04f6dafce19b7b4f093c35716739f36d75973ba
```

For the host output established by the earlier Zeus path report, the exact
candidate flake reference is:

```text
github:LiGoldragon/CriomOS/d04f6dafce19b7b4f093c35716739f36d75973ba#nixosConfigurations.target.config.system.build.toplevel
```

At that immutable CriomOS revision, the exact locked producer pins are:

```text
CriomOS-home  1a6e22da155bb75a6362d10623301b13d0c24b34
Lojix        0d968da44bc0be8ed875b8546bebf52c3de53a81
```

Both lock entries are GitHub owner/repository/revision references with fixed
nar hashes. Public forge refs confirm that each pinned producer commit is
present and is the current `main` of its own public, non-archived repository.
The public proposal repository's current `main` is
`be4bf4d63d15f5e591bb5d7bfdf06d9ed019d38c`; its `datom.dotos` file is also
present at that immutable revision.

## Comparison with Zeus

Zeus generation 63 is active and reports NixOS
`26.05.20260422.0726a0e` with nixpkgs revision
`0726a0ecb6d4e08f6adced58726b95db924cef57`. Its exposed version/profile
metadata does not report a CriomOS configuration revision or either dependent
pin. This is compatible with, but does not prove, deployment of the candidate
above. No target-side evidence currently identifies generation 63 with
`d04f…`, `1a6e…`, or `0d968…`.

## Inference and authority boundary

The forge facts establish a public, pushed, immutable, and portable producer
chain suitable for a `RequireImmutable` request. They do not establish that
Zeus generation 63 was built from that chain, that the candidate's output
evaluates successfully for the current proposal, or that its Home Manager
state is synchronized. Selecting this source, output, and any activation
action remains the caller's authority.

No source checkout was fetched or changed. No Nix build/evaluation, proposal
submission, closure copy, deployment, activation, reboot, or secret access was
performed by this subflow.

## Sources

- [forgePins witness](../witnesses/forgePins.md)
- [zeusGeneration63 witness](../witnesses/zeusGeneration63.md)
- [prior Zeus update-path report](../../d098fa2d/reports/zeusUpdatePath.md)
- [prior Zeus live preflight](../../7a9f4c12/reports/zeusDualRoutePreflight.md)
- [Zeus psyche vision](../../01a02b46/vision/zeusUpdate.md)
- `/home/li/primary/SKILL_VARIABLES.md`
- `/home/li/primary/.agents/skills/nix-workflow/SKILL.md`
- `/home/li/primary/.agents/skills/lojix/SKILL.md`
