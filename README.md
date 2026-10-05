# dotfiles
Reproducible macOS setup with a staged Nix and Homebrew configuration

## Configuration-only pilot

A small Apple Silicon (`aarch64-darwin`) preparation: standalone Home Manager
provides Zsh, Git, jq and ripgrep plus two explicitly selected, isolated config
files. `darwinConfigurations.staged` records the later nix-darwin/Homebrew seam;
Homebrew is disabled and existing GUI/mac-specific software stays with its owner.

**Nothing here installs or activates Nix or dotfiles.** No live shell/Git takeover,
Node/Volta/Pi changes, Herdr/Firstmate lifecycle, secrets, services or cleanup.
`pilot` is a fictitious disposable account, not the working Mac's account.

```sh
python3 -m unittest discover -s tests -v
```

See [pilot review, ownership, build gates and rollback](docs/pilot.md). Exact
26.05-family input revisions are pinned in `flake.nix`, but **no lockfile or Nix
evaluation/build is claimed**: Nix is unavailable here. Consumer tests and CI
validate authored Git/Zsh behavior only. Installation, lock generation, disposable
host testing and any activation require separate approval. Do not merge until
explicit approval.
