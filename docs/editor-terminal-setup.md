# Neovim, Herdr and WezTerm setup

## Provenance and scope

The app configuration is adapted from [`kunchenguid/dotfiles` at
`9a4a6387d0dd6f4bf9b8a5a732b406916bbbf95d`](https://github.com/kunchenguid/dotfiles/tree/9a4a6387d0dd6f4bf9b8a5a732b406916bbbf95d), the upstream `main` commit at the time of review (2026-10-07). The read-only snapshot remote was `https://github.com/kunchenguid/dotfiles.git`, and its `main` ref matched that commit. The source files copied are:

- `home/.config/nvim/` (init, Lua modules, plugin specs and `lazy-lock.json`)
- `home/.config/herdr/config.toml`
- `home/.config/wezterm/wezterm.lua`

The upstream `LICENSE` is preserved verbatim at
[`third-party/licenses/kunchenguid-dotfiles-MIT-0.txt`](../third-party/licenses/kunchenguid-dotfiles-MIT-0.txt). It is MIT No Attribution, Copyright 2026 Kun Chen. No other upstream Home Manager, bootstrap, system defaults, Homebrew cleanup, agent/Pi, shell alias, identity, or secret configuration is adopted. The three configuration sets contain no upstream username or absolute home paths, so no path/identity substitution was needed.

This repo adds the existing Neovim package's config mappings and the upstream Hack Nerd Font requirement to the isolated Home Manager pilot. It does not add another Neovim package, and it does not claim package ownership for WezTerm or Herdr. Both commands already resolve on the host (`/opt/homebrew/bin/wezterm` and `~/.local/bin/herdr`); `herdr` is not an attribute in this flake's locked Nixpkgs. The pilot's declarative Hack Nerd Font package and fontconfig option are build configuration only until a separately approved Home Manager activation. Lazy.nvim's upstream lock file records the plugin revisions. On first startup, it seeds a writable lock at `stdpath('state')/lazy/lazy-lock.json` (normally `~/.local/state/nvim/lazy/lazy-lock.json`), so read-only Home Manager config works too. An existing runtime lock is never replaced by the supplied copy; configuration changes do not silently update its pins. Explicit Lazy install/update operations may write that runtime lock. The first ordinary Neovim start will still bootstrap lazy.nvim and may need network access.

The mappings in `home/pilot.nix` describe the intended XDG targets in the fictitious `pilot` profile. They do not enroll the real account. Do not activate `homeConfigurations.pilot` on this Mac, switch nix-darwin, or symlink the host to a disposable worktree.

## Host metadata observed (read-only, 2026-10-07)

Only the named app paths were inspected for metadata; existing config contents were not read.

| Host path | Observed state | Owner / mode / symlink details |
| --- | --- | --- |
| `~/.config/nvim` | Absent | No existing target to back up; Neovim command resolves to `~/.nix-profile/bin/nvim`. |
| `~/.config/herdr` | Existing directory | Ordinary directory, not a symlink; owned by `stefanchristensen:staff`, mode `0755`, with extended-attribute marker. Other entries were not inspected. |
| `~/.config/herdr/config.toml` | Existing regular file, 162 bytes | Not a symlink; owned by `stefanchristensen:staff`, mode `0644`, with extended-attribute marker. Contents were not read. |
| `~/.config/wezterm` | Existing directory | Ordinary directory, not a symlink; owned by `stefanchristensen:staff`, mode `0755`, with extended-attribute marker. Other entries were not inspected. |
| `~/.config/wezterm/wezterm.lua` | Existing regular file, 1,655 bytes | Not a symlink; owned by `stefanchristensen:staff`, mode `0644`, with extended-attribute marker. Contents were not read. |

The executable paths observed were `/Users/stefanchristensen/.nix-profile/bin/nvim`, `/opt/homebrew/bin/wezterm`, and `/Users/stefanchristensen/.local/bin/herdr`. Their package managers/owners were not investigated. No config was backed up or changed by this worker.

## Bounded installation handoff (for MAIN)

Perform only after the branch is reviewed and the repository has been published to a stable, non-disposable checkout. Keep copies of the two colliding files until the new configs have been accepted. Use a private, timestamped backup directory such as `~/.config/dotfiles-backups/editor-terminal-setup/<UTC timestamp>/`, mode `0700`; use a metadata-preserving copy (for example macOS `ditto`) and verify byte equality before changing either target. Do not inspect unrelated config files, copy the entire Herdr/WezTerm directories, or remove/replace either directory.

Then install only these three links from that stable checkout:

1. Create `~/.config/nvim` as a symlink to `<stable-dotfiles-checkout>/home/.config/nvim` (the target is currently absent).
2. Back up `~/.config/herdr/config.toml`, verify the backup, then replace only that file with a symlink to `<stable-dotfiles-checkout>/home/.config/herdr/config.toml`.
3. Back up `~/.config/wezterm/wezterm.lua`, verify the backup, then replace only that file with a symlink to `<stable-dotfiles-checkout>/home/.config/wezterm/wezterm.lua`.

Verify link targets, backup readability/byte equality and ownership/modes; leave every other file in the two existing directories unchanged. Retain the backups and rollback instructions until separately accepted: remove only the newly created links and restore the matching saved files. Do not run a nix-darwin/Home Manager switch, install/reinstall an app package, change login shell or PATH, restart apps/services, or run any Herdr lifecycle command as part of this narrow file step. No app or config installation has yet been performed on the live host by this worker.

## Validation and limits

Validation is deliberately limited to isolated, headless/static checks: Neovim startup and configured plugin/keymap state with temporary XDG directories under ignored `.test-tmp`; WezTerm config parsing with `show-keys`; TOML syntax and expected Herdr keybindings parsed by Python's `tomllib`; and flake evaluation/build checks for the pilot package/config declarations. No Herdr server/session/pane or other lifecycle behavior was invoked. The offline lock regression in `tests/test_nvim_lock.py` runs real Lazy against a local Git plugin and read-only config, checking pinned first installation, writable lock state and unchanged repeated startup. Run it with `NVIM=<nvim-executable> LAZY_NVIM_SOURCE=<lazy.nvim-checkout> python3 -m unittest discover -s tests -p test_nvim_lock.py`. No GUI behavior, real font rendering, live app adoption, target-home collision handling, or Home Manager activation is claimed.
