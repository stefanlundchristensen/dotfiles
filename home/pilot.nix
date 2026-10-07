{ pkgs, ... }:
{
  # Replace only in a separately reviewed disposable-account enrollment change.
  home.username = "pilot";
  home.homeDirectory = "/Users/pilot";
  home.stateVersion = "26.05";

  home.packages = [
    pkgs.zsh
    pkgs.git
    pkgs.jq
    pkgs.ripgrep
    pkgs.neovim
    pkgs.nerd-fonts.hack
  ];
  fonts.fontconfig.enable = true;

  # User-level Nix client config; does not select or manage the Nix installation.
  xdg.configFile."nix/nix.conf".text = "experimental-features = nix-command flakes\n";

  # No standard shell/Git file takeover or session-variable/PATH declarations.
  xdg.enable = true;
  xdg.configFile."dotfiles-pilot/zsh/.zshrc".source = ../files/zsh/.zshrc;
  xdg.configFile."dotfiles-pilot/git/config".source = ../files/gitconfig;

  # App configs are sourced from this repo; activation remains a separate gate.
  xdg.configFile."nvim".source = ../home/.config/nvim;
  xdg.configFile."herdr/config.toml".source = ../home/.config/herdr/config.toml;
  xdg.configFile."wezterm/wezterm.lua".source = ../home/.config/wezterm/wezterm.lua;
}
