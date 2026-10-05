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

See [pilot review, ownership, build evidence and rollback](docs/pilot.md). Exact
26.05-family input revisions in `flake.nix` now have a Nix-generated `flake.lock`.
With existing Nix 2.35.2 on Apple Silicon/macOS 26.6.2, both the standalone Home
Manager and staged nix-darwin outputs evaluated and built without activation.
Consumer/lock-structure tests also passed; CI does not install or run Nix.
Cold rebuilds, disposable-account activation and rollback remain unverified and
require separate approval. Do not merge until explicit approval.
