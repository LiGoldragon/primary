{
  description = "primary workspace generated skill surfaces";

  inputs = {
    skills.url = "github:LiGoldragon/skills";
    nixpkgs.follows = "skills/nixpkgs";
  };

  outputs =
    {
      self,
      nixpkgs,
      skills,
    }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      apps = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          skillApps = skills.apps.${system};
          generatorAppNames = builtins.filter (nixpkgs.lib.hasPrefix "generate-") (builtins.attrNames skillApps);

          runSkillApp =
            appName:
            let
              script = pkgs.writeShellApplication {
                name = appName;
                text = ''
                  if [ "$#" -gt 1 ]; then
                    echo "usage: ${appName} [workspace-root]" >&2
                    exit 2
                  fi

                  workspace_root="''${1:-$PWD}"
                  exec "${skillApps.${appName}.program}" "$workspace_root"
                '';
              };
            in
            {
              type = "app";
              program = "${script}/bin/${appName}";
              meta.description = "Run ${appName} through the locked skills flake";
            };

          generateSkills =
            let
              script = pkgs.writeShellApplication {
                name = "generate-skills";
                text = ''
                  if [ "$#" -gt 1 ]; then
                    echo "usage: generate-skills [workspace-root]" >&2
                    exit 2
                  fi

                  workspace_root="''${1:-$PWD}"
                  ${nixpkgs.lib.concatMapStringsSep "\n" (appName: ''
                    "${skillApps.${appName}.program}" "$workspace_root"
                  '') generatorAppNames}
                '';
              };
            in
            {
              type = "app";
              program = "${script}/bin/generate-skills";
              meta.description = "Regenerate every configured skill output into the workspace root";
            };
        in
        (nixpkgs.lib.genAttrs generatorAppNames runSkillApp)
        // {
          generate-skills = generateSkills;
          default = generateSkills;
        }
      );

      checks = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          skillApps = skills.apps.${system};
          checkAppNames = builtins.filter (nixpkgs.lib.hasPrefix "check-") (builtins.attrNames skillApps);

          generatedSkillsCurrent = pkgs.runCommand "primary-generated-skills-current" { } ''
            ${nixpkgs.lib.concatMapStringsSep "\n" (appName: ''
              "${skillApps.${appName}.program}" ${self}
            '') checkAppNames}
            touch "$out"
          '';
        in
        {
          generated-skills-current = generatedSkillsCurrent;
          default = generatedSkillsCurrent;
        }
      );
    };
}
