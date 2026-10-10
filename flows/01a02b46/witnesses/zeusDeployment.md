# Zeus deployment stages

Method: probe `meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS?rev=d04f6dafce19b7b4f093c35716739f36d75973ba (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 <action> RequireImmutable Some.@/etc/nix/machines [])'` and ordinary `lojix 'Query.ByNode.(goldragon zeus None)'` on 2026-08-23.

The authorized field set was used verbatim for every action: `goldragon/zeus`,
`CompleteHost`, the absolute regular proposal source, pinned source revision,
Horizon, the supplied selector, `NixosSystemdBootV1`, remote builder
`Some.@/etc/nix/machines`, and no extra substituters. The transfer URI was
`ssh-ng://root@192.168.18.95`; the activation destination was
`root@zeus.goldragon.criome`.

- Evaluate was admitted as deployment 28 at `(626 626)` and reached
  `Completed Some.(641 641) Some.Succeeded`.
- Realize was admitted as deployment 29 at `(646 646)` and reached
  `Completed Some.(662 662) Some.Succeeded`.
- TestActivation was admitted as deployment 30 at `(667 667)`. Its closure
  copy process used `nix copy --substitute-on-destination --to
  ssh-ng://root@192.168.18.95` and its SSH transfer counter rose to at least
  1,932,511,150 bytes. Lojix then recorded terminal
  `Failed Some.(683 683) Some.Failed.(CopyClosure BuilderUnreachable)`; the
  node query marker was `(687 687)`.

No `ActivateNow`, `SetBootProfile`, reboot, runtime mutation, or
`Deploy.UserEnvironment` request was submitted after the failed test.

## Target baseline and post-failure witness

Method: probe `ssh -o BatchMode=yes -o StrictHostKeyChecking=yes root@zeus.goldragon.criome` with `readlink`, `nixos-rebuild list-generations`, `bootctl status`, `systemctl`, `journalctl`, and `df` on 2026-08-23.

Before TestActivation, Zeus's persistent system profile, `/run/current-system`,
and `/run/booted-system` all resolved to
`6mjh02yv45nh0r0nr7gyd9rakrv79xdv-nixos-system-zeus-26.05.20260422.0726a0e`.
`nixos-rebuild list-generations` reported generation 63 current; systemd-boot
reported current and default entry `nixos-generation-63.conf`; `systemctl
--failed` was empty; `sshd.service` was active. `mpd.service` was absent and
D-Bus was running with pre-existing duplicate service-name messages. Bird and
li Home Manager profile links resolved respectively to
`z013ab5cszmn7v8m212f7dfg91kn7ckk-home-manager-generation` and
`l6wizcwajdc9qfyc16ahlqspgvsrp039-home-manager-generation`.

After deployment 30 failed, the same three system links and the current/default
boot entry remained at generation 63; the candidate
`jz6mg0qlm3w3h2h5jxwldccncjgcz22j-nixos-system-zeus-26.11.20260813.0e251e2`
store path was absent; SSH remained active; `systemctl --failed` remained empty;
and no activation journal lines were returned. The pre-existing MPD and D-Bus
observations were unchanged. `/nix` free space was 66,240,798,720 bytes after
the failed copy, versus 79,294,595,072 bytes in the pre-test baseline. This is
a material partial-copy footprint; its exact Nix-store disposition is not
established by these observations.
