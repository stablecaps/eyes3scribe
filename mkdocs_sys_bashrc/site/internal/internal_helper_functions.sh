cite about-internal
about-internal 'Internal bash helper functions'

function check_new_bashrc_vers() {
    about 'checks whether stablecaps_bashrc is up-to-date'
    group 'internal'
    example 'check_new_bashrc_vers'

    git --git-dir=${HOME}/stablecaps_bashrc/.git fetch --quiet
    # check relation of our local .bashrc to remote basshrc at https://github.com/stablecaps/stablecaps_bashrc
    BASHRC_CURR_BRANCH=$(git --git-dir=${HOME}/stablecaps_bashrc/.git rev-parse --abbrev-ref HEAD)
    BASHRC_COMMIT_DETAILS=$(git --git-dir=${HOME}/stablecaps_bashrc/.git rev-list --left-right \
                            --count origin/master..."${BASHRC_CURR_BRANCH}")
    BC_BEHIND=$(echo "$BASHRC_COMMIT_DETAILS" | awk '{print $1}' | sed 's/^[ \t]*//;s/[ \t]*$//')
    BC_AHEAD=$(echo "$BASHRC_COMMIT_DETAILS" | awk '{print $2}' | sed 's/^[ \t]*//;s/[ \t]*$//')

    echo -e "\n${PureCHATREU}Your bashrc is ${PureBRed}${BC_BEHIND} ${PureCHATREU}commits behind origin/master and ${PureBBlue}${BC_AHEAD} ${PureCHATREU}commits ahead\n${NOCOL}"
}
