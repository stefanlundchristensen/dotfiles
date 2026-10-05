{ ... }:
{
  nixpkgs.hostPlatform = "aarch64-darwin";
  system.stateVersion = 6;

  # Leave the installer/runtime owner undecided and external to nix-darwin.
  nix.enable = false;

  # Retain existing Homebrew, GUI apps and vendor updaters. No adoption yet.
  homebrew = {
    enable = false;
    brews = [ ];
    casks = [ ];
    taps = [ ];
    onActivation = {
      cleanup = "none";
      autoUpdate = false;
      upgrade = false;
    };
  };
  # No Home Manager integration, defaults, users, login shell or custom services.
  # Even this staged output's upstream activation changes system files: DO NOT APPLY.
}
