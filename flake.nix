{
  description = "primary workspace generated skill surfaces";

  inputs = {
    dotos = {
      url = "github:LiGoldragon/dotos/e19699933dabd09842c4423d15a704ce3d48b493";
      flake = false;
    };
    dotos-config = {
      url = "github:LiGoldragon/dotos-config/4fbf66d82c645d113ed7c3448c05218d1c8d7095";
      flake = false;
    };
    dotos-text-query = {
      url = "github:LiGoldragon/dotos-text-query/acf6b4b935443602f0bf575adfb22e974c5dde53";
      flake = false;
    };
    skills.url = "github:LiGoldragon/Curriculum";
    tree-sitter-dotos = {
      url = "github:LiGoldragon/tree-sitter-dotos/a00d147463e0ba620e17e186803217e86487bce2";
      flake = false;
    };
    nixpkgs.follows = "skills/nixpkgs";
  };

  outputs =
    {
      self,
      nixpkgs,
      skills,
      ...
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
            appName: mode: description:
            let
              script = pkgs.writeShellApplication {
                name = appName;
                text = ''
                  if [ "$#" -gt 1 ]; then
                    echo "usage: ${appName} [dotos-payload]" >&2
                    exit 2
                  fi

                  if [ "$#" -eq 1 ]; then
                    exec "${skillApps.${appName}.program}" "$1"
                  fi

                  exec "${skillApps.${appName}.program}" "Generate.{${skills} $PWD manifests/active-outputs.dotos ${mode}}"
                '';
              };
            in
            {
              type = "app";
              program = "${script}/bin/${appName}";
              meta.description = description;
            };

          generateSkills = wrappedSkillApp "generate-skills" "Write" "Regenerate configured skill outputs into the workspace root";
          checkSkills = wrappedSkillApp "check-skills" "Check" "Check generated skill outputs in the workspace root without writing";
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
            SKILLS_WORKSPACE_ROOT="${self}" \
              "${skillApps."check-skills".program}" "Generate.{${skills} ${self} manifests/active-outputs.dotos Check}"
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
