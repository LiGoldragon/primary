# CriomOS canonical materialized target witness

Method: immutable evaluation of
`git+file:///git/github.com/LiGoldragon/CriomOS?rev=93049a6e3eb7f66a23484402c96d835caa233b99`
with the existing materialized inputs:

```text
--override-input system /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/system
--override-input horizon /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/horizon
--override-input deployment /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/deployment
--override-input secrets /var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/secrets
```

Observed: `nix eval` of `nixosConfigurations.target.config.system.build.toplevel.drvPath` exited successfully. The evaluated target has users `bird` and `li`; the materialized deployment shape has `includeHome = true`.

Observed from one target summary evaluation: `li`'s `programs.emacs.package` and `services.emacs.package` have the same Emacs PGTK 30.2 output identity; `home.file.".emacs.d/init.el".source` is the generated `criomos-emacs-init-el` artifact; `systemd.user.services.chroma-daemon.Service.ExecStart` points to the Chroma daemon; Chroma is present in `home.packages`; and the Emacs package closure includes `emacs-chroma-theme`.

Observed from source: CriomOS `flake.nix:154-162` consumes the projected Horizon/system/deployment inputs; `:228-252` constructs the sole `nixosConfigurations.target` with Home Manager when `includeHome` is true; `modules/nixos/userHomes.nix:29-50` filters local users, passes the global package set, and imports `inputs.criomos-home.homeModules.default`; `flake.nix:254-267` makes the embedded Home activation package canonical and exposes independent Home output only for comparison.

Boundary: this proves evaluated target composition and closure identity, not a built or activated target. No Nix build, Lojix owner request, deployment, or activation was run by this witness.

Method: ordinary read-only Lojix query:

```text
lojix 'Query.ByNode.(goldragon zeus None)'
```

Observed: the durable node history listed deployments 28 (`Host.Evaluate`) and 29 (`Host.Realize`) using source `d04f6dafce19b7b4f093c35716739f36d75973ba`, both succeeded; deployment 30 (`Host.TestActivation`) using the same source failed at `CopyClosure` with `BuilderUnreachable`. No deployment record listed source `93049a6e3eb7f66a23484402c96d835caa233b99`.
