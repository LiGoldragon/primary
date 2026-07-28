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
            appName: mode: description:
            let
              script = pkgs.writeShellApplication {
                name = appName;
                text = ''
                  if [ "$#" -gt 1 ]; then
                    echo "usage: ${appName} [nota-payload]" >&2
                    exit 2
                  fi

                  if [ "$#" -eq 1 ]; then
                    exec "${skillApps.${appName}.program}" "$1"
                  fi

                  exec "${skillApps.${appName}.program}" "(Generate (${skills} $PWD manifests/active-outputs.nota ${mode}))"
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
            "${skillApps."check-skills".program}" "(Generate (${skills} ${self} manifests/active-outputs.nota Check))"
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
