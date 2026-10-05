# Pilot review and recovery

## Present authorization and ownership

This PR is **repository configuration only**. The target is native Apple Silicon
(`aarch64-darwin`); the sanitized baseline reports macOS 26.6.2. Support for that
exact OS, Intel and Linux has not been demonstrated. Nix is absent here: no
installation, Nix evaluation/build, activation, host PATH/login-shell change,
service action or Homebrew command was performed.

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
| Git, Zsh, jq, ripgrep | Four Nix packages in the standalone HM user profile, only after approved activation |
| `~/.config/dotfiles-pilot/zsh/.zshrc` | One authored immutable file; used only with explicit `ZDOTDIR` |
| `~/.config/dotfiles-pilot/git/config` | One authored immutable file; selected only with per-process `GIT_CONFIG_GLOBAL` |
| HM profile/generation and session-vars artifacts | HM's normal activation machinery; inspect the built closure before approval |
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
branches. **There is no `flake.lock`**: Nix was not available to compute/verify NAR
hashes or resolve the complete input graph. This is revision-pinned preparation,
not a fully verified lock or proven reproducible build. Do not copy another
repository's lock, fabricate hashes, or claim evaluated package versions.

The state versions in [`home/pilot.nix`](../home/pilot.nix) and
[`darwin/staged.nix`](../darwin/staged.nix) are initial compatibility values,
not automatic update counters. For future updates, change exact input
revisions deliberately, generate/review the lock on an approved Nix-enabled test
machine, inspect release notes, build and test before activation. Do not update
inputs during activation. Brew cask payloads/vendor app updates are not Nix-pinned.

## Review now (no Nix, no host changes)

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
into the working session. CI runs these checks on a macOS runner, with no Nix
installer. These checks do **not** parse/evaluate Nix or prove HM/nix-darwin options,
package availability, generated closures, collision handling or rollback.

### Recorded local validation (2026-10-05)

- Four consumer tests passed with the existing Git and Zsh executables.
- Existing `actionlint` accepted `.github/workflows/checks.yml`.
- `git diff --check` passed.
- `nix` and `nix-instantiate` were unavailable; Nix syntax/evaluation, lock hash
  verification, builds and all activation/rollback acceptance tests remain unverified.
- No host installation or configuration changes were made. CI results are a
  separate delivery gate, not evidence of Nix acceptance.

## Future build/review gate — not executed here

Requires an approved Nix implementation already installed on an approved disposable
Apple Silicon test machine. Installer/version/integrity/daemon approval is a
separate decision. No `sudo`, installer URL, activation one-liner or force flag
is supplied by this repository. Keep secrets, private config and the vault outside
this checkout: even private Git and local Nix-store copies are not secret stores.

After reviewing account parameters and staging the intended source files (Git
flakes include tracked files), compute the real lock and commit it in a separate
reviewed change. Then run non-activating validation there:

```sh
nix --extra-experimental-features 'nix-command flakes' flake lock
# Review every revision, follows edge and NAR hash before continuing.
nix --extra-experimental-features 'nix-command flakes' flake check --no-build --no-update-lock-file
nix --extra-experimental-features 'nix-command flakes' build --no-update-lock-file \
  .#homeConfigurations.pilot.activationPackage --out-link result-pilot
nix --extra-experimental-features 'nix-command flakes' build --no-update-lock-file \
  .#checks.aarch64-darwin.pilot-config --no-link
# Optional staged-system BUILD ONLY, independently reviewed:
nix --extra-experimental-features 'nix-command flakes' build --no-update-lock-file \
  .#darwinConfigurations.staged.system --out-link result-staged
```

Inspect `result-pilot/activate`, `result-pilot/home-files`, `result-pilot/home-path`
and generated profile/session files; review the system closure independently.
Building downloads/writes Nix-store artifacts but does not activate configuration.
Resolve any invalid options/packages here before seeking adoption approval.

## Future activation gate — separate explicit approval required

Only on the named disposable account/spare Mac, after successful lock/evaluation/
build review and verified recoverable backup. Check both exact target paths for
collisions; do not inspect or adopt unrelated home files. Stop on a collision:
no `force`, backup-overwrite, automated move/removal or shell-file replacement.
Preserve existing packages and at least two known-good HM generations/closures;
no automatic garbage collection, Brew cleanup/zap or service adoption.

Record the source commit, lock, Nix implementation/version and previous generation
path. With that approval only, `./result-pilot/activate` applies the reviewed HM
closure. This does not activate the staged nix-darwin output. Launch a separate
non-login test shell with `ZDOTDIR="$HOME/.config/dotfiles-pilot/zsh"
./result-pilot/home-path/bin/zsh -d`. No parent-session PATH or login-shell change
is needed. Use absolute `home-path/bin/{git,jq,rg}` paths for provenance checks;
select the authored Git file per test process with
`GIT_CONFIG_GLOBAL="$HOME/.config/dotfiles-pilot/git/config"`.

Acceptance evidence still needed: package versions/provenance, jq/rg fixture
behavior, successful build on macOS 26.6.2, activation twice with unchanged files/
executables, zero unrelated installs/upgrades/removals/restarts/login prompts,
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
relinquish the two exact links/profile and restore any explicitly backed-up target
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
