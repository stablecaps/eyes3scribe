
Internal bash helper functions
==============================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/internal/internal_helper_functions.sh)***
## Function Index


```python
01 - check_new_bashrc_vers
```

******
### >> check_new_bashrc_vers():


>***about***: checks whether stablecaps_bashrc is up-to-date


>***group***: internal


>***example***: `check_new_bashrc_vers`


```bash
function check_new_bashrc_vers() {

    git --git-dir=${HOME}/stablecaps_bashrc/.git fetch --quiet
    BASHRC_CURR_BRANCH=$(git --git-dir=${HOME}/stablecaps_bashrc/.git rev-parse --abbrev-ref HEAD)
    BASHRC_COMMIT_DETAILS=$(git --git-dir=${HOME}/stablecaps_bashrc/.git rev-list --left-right \
                            --count origin/master..."${BASHRC_CURR_BRANCH}")
    BC_BEHIND=$(echo "$BASHRC_COMMIT_DETAILS" | awk '{print $1}' | sed 's/^[ \t]*//;s/[ \t]*$//')
    BC_AHEAD=$(echo "$BASHRC_COMMIT_DETAILS" | awk '{print $2}' | sed 's/^[ \t]*//;s/[ \t]*$//')

    echo -e "\n${PureCHATREU}Your bashrc is ${PureBRed}${BC_BEHIND} ${PureCHATREU}commits behind origin/master and ${PureBBlue}${BC_AHEAD} ${PureCHATREU}commits ahead\n${NOCOL}"
}

```


