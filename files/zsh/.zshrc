# Selected only by an explicit ZDOTDIR in a disposable, non-login shell.
# No PATH edits, startup installers, live rc sourcing, aliases or persisted history.
setopt INTERACTIVE_COMMENTS HIST_IGNORE_DUPS
unsetopt SHARE_HISTORY
# Zsh clamps HISTSIZE to a minimum of one; SAVEHIST disables persistence.
HISTSIZE=1
SAVEHIST=0
PROMPT='[pilot] %~ %# '
