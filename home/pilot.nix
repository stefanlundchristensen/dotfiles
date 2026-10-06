{ pkgs, ... }:
{
  # Replace only in a separately reviewed disposable-account enrollment change.
  home.username = "pilot";
  home.homeDirectory = "/Users/pilot";
  home.stateVersion = "26.05";

  home.packages = [ pkgs.zsh pkgs.git pkgs.jq pkgs.ripgrep pkgs.neovim ];

  # User-level Nix client config; does not select or manage the Nix installation.
  xdg.configFile."nix/nix.conf".text = "experimental-features = nix-command flakes\n";

  # No standard shell/Git file takeover or session-variable/PATH declarations.
  xdg.enable = true;
  xdg.configFile."dotfiles-pilot/zsh/.zshrc".source = ../files/zsh/.zshrc;
  xdg.configFile."dotfiles-pilot/git/config".source = ../files/gitconfig;
}
