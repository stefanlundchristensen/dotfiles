# dotfiles
Reproducible macOS setup with a staged Nix and Homebrew configuration

## Configuration-only pilot

A small Apple Silicon (`aarch64-darwin`) preparation: standalone Home Manager
provides Zsh, Git, jq, ripgrep and Neovim plus isolated Zsh/Git configuration
and user-level Nix feature flags. `darwinConfigurations.staged` records the later
nix-darwin/Homebrew seam; Homebrew is disabled and existing GUI/mac-specific
software stays with its owner.

**Nothing here installs or activates Nix or dotfiles.** No live shell/Git takeover,
Node/Volta/Pi changes, Herdr/Firstmate lifecycle, secrets, services or cleanup.
`pilot` is a fictitious disposable account, not the working Mac's account.

```sh
python3 -m unittest discover -s tests -v
```

See [pilot review, ownership, build evidence and rollback](docs/pilot.md) for
the locked-input validation results, remaining acceptance gates and approval
boundaries. Do not merge until explicit approval.
