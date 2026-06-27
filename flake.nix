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

          wrappedSkillApp =
            appName: description:
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
              meta.description = description;
            };

          generateSkills = wrappedSkillApp "generate-skills" "Regenerate configured skill outputs into the workspace root";
          checkSkills = wrappedSkillApp "check-skills" "Check generated skill outputs in the workspace root without writing";
        in
        {
          generate-skills = generateSkills;
          check-skills = checkSkills;
          default = generateSkills;
        }
      );

      checks = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          skillApps = skills.apps.${system};

          generatedSkillsCurrent = pkgs.runCommand "primary-generated-skills-current" { } ''
            "${skillApps."check-skills".program}" ${self}
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
