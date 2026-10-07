{
  description = "Configuration-only Apple Silicon shell/Git pilot";

  inputs = {
    # Exact commits from the matching 26.05 release branches; see docs/pilot.md.
    nixpkgs.url = "github:NixOS/nixpkgs/6ca6757e08e5dec9110859c969a6a2718ceb44a0";
    home-manager.url = "github:nix-community/home-manager/db7d5e2332710f5abb088f6b5de927d7f9511b35";
    home-manager.inputs.nixpkgs.follows = "nixpkgs";
    nix-darwin.url = "github:nix-darwin/nix-darwin/c3e90c89649b07d1a96e4b9dd6cd0d6e44b91a74";
    nix-darwin.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, home-manager, nix-darwin }:
    let
      system = "aarch64-darwin";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      # A fictitious disposable account, NOT the working account. Build/review only.
      homeConfigurations.pilot = home-manager.lib.homeManagerConfiguration {
        inherit pkgs;
        modules = [ ./home/pilot.nix ];
      };

      # Optional future system adoption: not part of standalone pilot activation.
      darwinConfigurations.staged = nix-darwin.lib.darwinSystem {
        modules = [ ./darwin/staged.nix ];
      };

      checks.${system}.pilot-config =
        assert builtins.elem pkgs.neovim self.homeConfigurations.pilot.config.home.packages;
        pkgs.runCommand "pilot-config-checks" {
          nativeBuildInputs = [ pkgs.python3 pkgs.git pkgs.zsh ];
        } ''
          cp -R ${self} ./source
          chmod -R u+w ./source
          cd source
          python3 -m unittest discover -s tests -v
          touch "$out"
        '';
    };
}
