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
    tree-sitter-dotos = {
      url = "github:LiGoldragon/tree-sitter-dotos/a00d147463e0ba620e17e186803217e86487bce2";
      flake = false;
    };
    curriculum-deploy = {
      url = "github:LiGoldragon/curriculum-deploy/f0174020675ff148bd7a8ebff31aef225464e8d0";
      inputs.curriculum.follows = "curriculum";
    };
    curriculum = {
      url = "github:LiGoldragon/Curriculum/9fe559994c56708f3852740e9f8114cf30ce691b";
      flake = false;
    };
    nixpkgs.follows = "curriculum-deploy/nixpkgs";
  };

  outputs =
    inputs@{
      self,
      nixpkgs,
      curriculum,
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
      apps = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          runtime = inputs."curriculum-deploy".packages.${system}.default;

          wrappedRuntime =
            appName: description:
            let
              script = pkgs.writeShellApplication {
                name = appName;
                text = ''
                  if [ "$#" -ne 1 ]; then
                    echo "usage: ${appName} 'CurriculumRequest.{Operation.{data-root workspace-root}}'" >&2
                    exit 2
                  fi
                  exec "${runtime}/bin/curriculum-deploy" "$1"
                '';
              };
            in
            {
              type = "app";
              program = "${script}/bin/${appName}";
              meta.description = description;
            };

          generateSkills = wrappedRuntime "generate-skills" "Run one typed Curriculum deployment request";
          checkSkills = wrappedRuntime "check-skills" "Run one typed Curriculum deployment check request";
        in
        {
          generate-skills = generateSkills;
          check-skills = checkSkills;
          default = generateSkills;
        });

      checks = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          runtime = inputs."curriculum-deploy".packages.${system}.default;

          generatedSkillsCurrent = pkgs.runCommand "primary-generated-skills-current" { } ''
            ${runtime}/bin/curriculum-deploy \
              "CurriculumRequest.{Check.{${curriculum} ${self}}}"
            touch "$out"
          '';
        in
        {
          generated-skills-current = generatedSkillsCurrent;
          default = generatedSkillsCurrent;
        });
    };
}
