# Pilot review and recovery

## Present authorization and ownership

This pilot remains **repository configuration and non-activating validation
only**. The target is native Apple Silicon (`aarch64-darwin`). Existing Nix 2.35.2
was used on macOS 26.6.2 to generate the lock, evaluate and build both outputs.
That demonstrates build availability, not complete OS/activation support; Intel
and Linux remain untested. No installation, activation, host PATH/login-shell
change, service action or Homebrew command was performed by this validation.

The default pilot is **standalone Home Manager**, not nix-darwin activation.
`pilot` and `/Users/pilot` are fictitious disposable-account parameters, not
collected account/host identifiers. Do not activate this output on the working
account. Enrolling a real disposable account requires a separate reviewed change
to those two parameters. There is deliberately no impure home-config import,
identity autodetection, installer, bootstrap script or automatic file adoption.
Do not put secrets into that change; private machine parameters must not be
published. A later real-account enrollment must decide a private parameter path
explicitly rather than introducing one silently here.

| Surface | Pilot owner / scope |
| --- | --- |
| Git, Zsh, jq, ripgrep, Neovim | Five Nix packages in the standalone HM user profile, only after approved activation; Neovim remains unconfigured |
| `~/.config/dotfiles-pilot/zsh/.zshrc` | One authored immutable file; used only with explicit `ZDOTDIR` |
| `~/.config/dotfiles-pilot/git/config` | One authored immutable file; selected only with per-process `GIT_CONFIG_GLOBAL` |
| `~/.config/nix/nix.conf` | One authored user-level Nix client config with `nix-command` and `flakes`; effective only after approved activation |
| HM profile/generation, session-vars, cache/state markers and font marker | Upstream HM machinery, not just the three authored files; inspect the entire built closure before approval |
| `~/.zshrc`, `.zprofile`, `.zshenv`, `.gitconfig`, `.config/git/config` | Unmanaged and untouched; no source/include of their contents |
| Homebrew and GUI/mac-specific apps | Existing owner retained; no cask/formula shortlist or adoption in this pilot |
| Volta/Node 22.22.2, Pi, Herdr/Firstmate, credentials and services | Entirely out of scope; no packages, links, imports or lifecycle commands |

HM activation installs a user profile; that is **not** a read-only operation.
Depending on already-configured profile sourcing, later shells may see its
packages. No global PATH edits are declared here, and no activation is authorized.
The shell file does not source HM session variables, write history, load live rc
files, install plugins or change login shell. Git behavior has no identity,
credential helper or include. Explicitly selecting it replaces the process's
global Git configuration: use local test repositories, not authenticated network
operations or real work requiring private global identity/helper settings.

Neovim is added only as `pkgs.neovim` in the Home Manager user profile. No Neovim
configuration, plugin framework, aliases, editor choice, or default-editor override
is declared. The pilot declares `nix-command` and `flakes` in the user's
`~/.config/nix/nix.conf` through the existing Home Manager XDG file surface. This
avoids selecting a Nix package or changing daemon ownership or nix-darwin settings.
The file takes effect only after Home Manager activation; it cannot bootstrap the
flake evaluation or activation that creates it. Before first use, pass the features
explicitly to Nix, before the subcommand, for example:

```sh
nix --extra-experimental-features 'nix-command flakes' flake metadata --no-update-lock-file
```

Use the same global option for each initial Nix flake/build command. When calling
a standalone `home-manager` executable directly, provide the equivalent setting
for that process and its Nix children, for example
`NIX_CONFIG='experimental-features = nix-command flakes' home-manager ...`.
These are bootstrap instructions only; no activation is authorized here. Do not
assume the HM-declared setting is effective until an independently approved
activation has completed.

`darwinConfigurations.staged` is a separate **build/review-only future seam**.
Homebrew is disabled; its lists are empty, cleanup is `none`, auto-update and
upgrade are false. Nix daemon ownership is external (`nix.enable = false`), not
an installer choice. There are no selected defaults, users, HM integration or
custom services. This does NOT make nix-darwin activation inert: upstream writes
system files and has its own activation effects. Never switch this staged output
as part of the pilot. Later system/Brew adoption and HM integration need separate
approval; never run integrated and standalone HM against the same files.

## Pins and honest validation boundary

GitHub's official 26.05-family release refs were queried read-only on 2026-10-05.
[`flake.nix`](../flake.nix) owns the exact input revisions and follows edges;
review them there rather than maintaining a second pin inventory here.

Both module inputs follow the one Nixpkgs input. Revisions are exact, not moving
branches. [`flake.lock`](../flake.lock) was generated by installed Nix from those
unchanged revisions, with real NAR hashes and both follows edges. Metadata and
build commands used `--no-update-lock-file`. The lock enables repeatable input
resolution; this is not proof of a cold rebuild, bit-for-bit determinism or future
binary-cache availability. Do not copy another repository's lock or fabricate
hashes.

The state versions in [`home/pilot.nix`](../home/pilot.nix) and
[`darwin/staged.nix`](../darwin/staged.nix) are initial compatibility values,
not automatic update counters. For future updates, change exact input
revisions deliberately, generate/review the lock on an approved Nix-enabled test
machine, inspect release notes, build and test before activation. Do not update
inputs during activation. Brew cask payloads/vendor app updates are not Nix-pinned.

## Source checks (no Nix required, no host changes)

From this checkout:

```sh
python3 -m unittest discover -s tests -v
actionlint .github/workflows/checks.yml  # optional existing tool; do not install it here
git diff --check
```

Tests use existing Git/Zsh consumers, a fake HOME, suppressed system/global Git
configuration and repository-local disposable state. They validate the Git
configuration's semantic key set, unset identity/helper/includes, initial branch,
local identity override, Zsh syntax and interactive settings, unchanged child PATH
and absence of writes to the fake home. No private home configuration is read.
Zsh necessarily reads the system `zshenv`; `-d` skips later global rc files, and
explicit `ZDOTDIR` avoids the user's rc files. Test environments are not exports
into the working session. A lock regression test checks the JSON lock graph,
repository identities, exact revision format, original/locked revision agreement,
follows edges and SHA-256 format; it does not verify agreement with `flake.nix`
or fetched NAR contents. Declaration agreement is covered by the recorded Nix
metadata validation below. CI runs these checks on a macOS runner, with no Nix installer.
These source checks do **not** evaluate Nix or prove HM/nix-darwin options, package
availability, generated closures, collision handling or rollback.

## Recorded non-activating validation (2026-10-05)

The original source-only pilot had no installed Nix. This follow-up used the
already-installed `/nix/var/nix/profiles/default/bin/nix` (version 2.35.2) on
`arm64`, macOS 26.6.2. No Nix installation or runtime reconfiguration was needed.
The account remains fictitious; no account enrollment or configuration fixes were
needed for evaluation/build.

Exact commands from this checkout (the local `NIX` variable selects the binary;
it does not change PATH):

```sh
NIX=/nix/var/nix/profiles/default/bin/nix
"$NIX" --version
"$NIX" --extra-experimental-features 'nix-command flakes' flake lock
# Stage the generated lock/new test so Git flakes include them.
git add flake.lock tests/test_lock.py
"$NIX" --extra-experimental-features 'nix-command flakes' flake metadata --no-update-lock-file --json
"$NIX" --extra-experimental-features 'nix-command flakes' flake check --no-build --no-update-lock-file
"$NIX" --extra-experimental-features 'nix-command flakes' eval --no-update-lock-file --raw \
  .#homeConfigurations.pilot.activationPackage.drvPath
"$NIX" --extra-experimental-features 'nix-command flakes' eval --no-update-lock-file --raw \
  .#darwinConfigurations.staged.system.drvPath
"$NIX" --extra-experimental-features 'nix-command flakes' build --no-update-lock-file --no-link --print-out-paths \
  .#homeConfigurations.pilot.activationPackage
"$NIX" --extra-experimental-features 'nix-command flakes' build --no-update-lock-file --no-link --print-out-paths \
  .#darwinConfigurations.staged.system
"$NIX" --extra-experimental-features 'nix-command flakes' build --no-update-lock-file --no-link --print-out-paths \
  .#checks.aarch64-darwin.pilot-config
python3 -m unittest discover -s tests -v
actionlint .github/workflows/checks.yml
git diff --check
```

All commands exited **0**. Metadata retained the three accepted revisions and
two Nixpkgs follows edges. `flake check --no-build` passed, but does not deeply
validate the custom HM/darwin outputs; the explicit drvPath evaluations and
successful builds above are the evidence for those outputs:

| Output | Evaluated derivation / realized output |
| --- | --- |
| Home Manager | `/nix/store/bzy1cmw68w0f8f3snzb1v01ybv7j1fql-home-manager-generation.drv` / `/nix/store/lc29fhhzxxh82r9r122cf6d6zmd8z0wz-home-manager-generation` |
| Staged nix-darwin | `/nix/store/m20lnyxbvbfcihs2wk5zn2k6rpzcba74-darwin-system-26.05.c3e90c8.drv` / `/nix/store/vd7z8x2gqvx7bhs1ksdvjhkp5q03nz5p-darwin-system-26.05.c3e90c8` |

The HM and darwin builds reused valid existing store outputs, not a clean-room
recompilation. The consumer-check derivation built locally; all five tests passed
both locally and with the Nix-provided Python/Git/Zsh. Dirty-tree warnings were
expected for the staged lock/test/docs. Existing `actionlint` and whitespace checks
passed. CI remains a separate publishing gate, not evidence of activation.

### Read-only closure review

The returned HM output's `activate`, `home-files`, `home-path` and
`home-path/etc/profile.d/hm-session-vars.sh` were inspected, never executed or
sourced. In this 2026-10-05 snapshot, the two authored config files matched with
`cmp`. `home-files` also
contains upstream `.cache/.keep`, `.local/state/.keep` and
`Library/Fonts/.home-manager-fonts-version`; activation includes app/font directory
setup and LaunchAgents setup (the built LaunchAgents directory is empty). Session
variables include XDG paths and TERMINFO_DIRS. Therefore a later adoption review
must not assume HM owns only two links or has no other activation effects.

Absolute `home-path/bin/{git,zsh,jq,rg} --version` commands exited 0: Git 2.54.0,
Zsh 5.9.1, jq 1.8.2, ripgrep 15.1.0. These are store-binary version checks, not
proof of an installed user profile or jq/rg fixture acceptance.

The staged system's generated `activate` and `Library` tree were inspected only.
Even with Homebrew disabled and `nix.enable = false`, upstream activation manages
system shell files, app/font directories, SSH host keys, `/run/current-system`
and `org.nixos.activate-system` launchd machinery. It is **not inert**.

No `activate`, switch, dry-run activation script, service command, Homebrew command,
installer or `sudo` was run. Builds may download/write store artifacts but do not
apply either configuration; `--no-link` also avoids a result link. Keep secrets,
private config and the vault outside this checkout and the Nix store. Before later
adoption, review generated artifacts again from the then-approved source/lock;
store paths here are evidence, not durable backups or approval to activate.

### Neovim follow-up build (2026-10-06)

The follow-up used the same already-installed Nix 2.35.2 binary. The flake check
asserts that Neovim is in the Home Manager package set and runs the Python tests.
The generated XDG Nix client config was inspected as recorded below; the check
does not semantically assert its effective experimental-feature set. Commands:

```sh
NIX=/nix/var/nix/profiles/default/bin/nix
"$NIX" --extra-experimental-features 'nix-command flakes' eval --no-update-lock-file --raw \
  .#checks.aarch64-darwin.pilot-config.drvPath
"$NIX" --extra-experimental-features 'nix-command flakes' eval --no-update-lock-file --raw \
  .#homeConfigurations.pilot.activationPackage.drvPath
"$NIX" --extra-experimental-features 'nix-command flakes' flake check --no-build --no-update-lock-file
"$NIX" --extra-experimental-features 'nix-command flakes' build --no-update-lock-file --no-link --print-out-paths \
  .#homeConfigurations.pilot.activationPackage
"$NIX" --extra-experimental-features 'nix-command flakes' build --no-update-lock-file --no-link --print-out-paths \
  .#checks.aarch64-darwin.pilot-config
python3 -m unittest discover -s tests -v
actionlint .github/workflows/checks.yml
git diff --check
```

All commands exited **0**; all five Python tests passed. The activation package
built as `/nix/store/4g3hjbl45h6c7s2rmxfp7cmkhgpajal2-home-manager-generation`;
its generated `home-files/.config/nix/nix.conf` contained exactly
`experimental-features = nix-command flakes`, and its profile contained executable
Neovim 0.12.4. The flake check derivation also built successfully. These were
non-activating evaluation/build and read-only output checks: the generated
`activate` script was not run, no user profile was switched, and no nix-darwin
output or daemon configuration was changed. Dependency paths were fetched into the
Nix store; this was not a cold rebuild.

## Future activation gate — separate explicit approval required

Only on the named disposable account/spare Mac, after successful lock/evaluation/
build review and verified recoverable backup. Check every reviewed generated
`home-files` target for collisions, including upstream markers; do not inspect or
adopt unrelated home files. Stop on a collision:
no `force`, backup-overwrite, automated move/removal or shell-file replacement.
Preserve existing packages and at least two known-good HM generations/closures;
no automatic garbage collection, Brew cleanup/zap or service adoption.

Record the source commit, lock, Nix implementation/version and previous generation
path. The examples below assume a separately reviewed `result-pilot` link to that
approved HM output; this validation created no such link.
With that approval only, `./result-pilot/activate` applies the reviewed HM
closure. This does not activate the staged nix-darwin output. Launch a separate
non-login test shell with `ZDOTDIR="$HOME/.config/dotfiles-pilot/zsh"
./result-pilot/home-path/bin/zsh -d`. No parent-session PATH or login-shell change
is needed. Use absolute `home-path/bin/{git,jq,rg}` paths for provenance checks;
select the authored Git file per test process with
`GIT_CONFIG_GLOBAL="$HOME/.config/dotfiles-pilot/git/config"`.

Acceptance evidence still needed: installed-profile package provenance, jq/rg
fixture behavior, activation twice with unchanged files/executables, zero
unrelated installs/upgrades/removals/restarts/login prompts,
unmanaged file collision refusal, and timed rollback on that disposable account.
None of these host acceptance tests is claimed by the source-consumer checks.

## Future rollback gate — not tested here

Exit the test shell/unset only its process-local selectors to return to unmanaged
shell/Git behavior; this alone does not remove the HM profile or linked files.
If a previous generation exists, inspect the recorded generation path and execute
its `activate` script on the same approved disposable account. Home Manager's
manual also documents `home-manager generations` and `home-manager switch
--rollback`; use the exact pinned HM tool if opting for that interface, not a
moving bootstrap branch. Recheck managed file contents, profile executable
provenance and unchanged unrelated software; target recovery within 15 minutes.

A first activation has no previous HM generation. Before it, document how to
relinquish the reviewed generated links/profile and restore any explicitly backed-up target
files under separate approval. Do not guess a destructive uninstall command.
Retain the previous source revision, lock and closures: Git alone cannot recreate
unavailable binaries. Rollback does not restore mutable data, OS updates, GUI app
state, credentials or installer changes. Nix-darwin/system rollback and Nix
uninstallation are separate, unapproved operations; follow the selected owner's
reviewed recovery documentation, never generic deletion of `/nix`.

## Sources consulted (read-only)

- [Home Manager 26.05 manual](https://home-manager.dev/manual/26.05/index.xhtml): standalone/integrated configurations, stateVersion, builds, collisions and rollback.
- [nix-darwin README](https://github.com/nix-darwin/nix-darwin/blob/master/README.md): Apple Silicon output and Nix implementation ownership.
- [nix-darwin Homebrew module](https://github.com/nix-darwin/nix-darwin/blob/nix-darwin-26.05/modules/homebrew.nix): activation boundary and explicit no-cleanup/no-update policy.
- [Nix flake lock manual](https://nix.dev/manual/nix/2.35/command-ref/new-cli/nix3-flake-lock): lock generation, hashes and no-update behavior.
- [kunchenguid/dotfiles at 9a4a638](https://github.com/kunchenguid/dotfiles/tree/9a4a6387d0dd6f4bf9b8a5a732b406916bbbf95d): small flake/module split and follows pattern only. No cleanup/zap, force, installer, app defaults, live agent resources or bootstrap behavior copied.
