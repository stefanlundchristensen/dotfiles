{ pkgs, ... }:
{
  # Replace only in a separately reviewed disposable-account enrollment change.
  home.username = "pilot";
  home.homeDirectory = "/Users/pilot";
  home.stateVersion = "26.05";

  home.packages = [ pkgs.zsh pkgs.git pkgs.jq pkgs.ripgrep ];

  # No standard shell/Git file takeover or session-variable/PATH declarations.
  xdg.enable = true;
  xdg.configFile."dotfiles-pilot/zsh/.zshrc".source = ../files/zsh/.zshrc;
  xdg.configFile."dotfiles-pilot/git/config".source = ../files/gitconfig;
}
