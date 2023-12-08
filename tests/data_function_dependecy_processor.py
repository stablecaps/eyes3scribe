triple_var2_input = """# This is a comment
This is not a comment
This is still not a comment

i left a blank line above which will not show up"""

triple_var2_expected = """This is not a comment
This is still not a comment
i left a blank line above which will not show up"""

#############################
func_name_list_data1 = [
    "_sdkman_complete",
    "_sdkman_candidate_local_versions",
    "_sdkman_candidate_all_versions",
    "__sdkman_cleanup_local_versions",
]
func_text_dict_data1 = {
    "_sdkman_complete": 'function _sdkman_complete() {\n\tlocal CANDIDATES\n\tlocal CANDIDATE_VERSIONS\n\tlocal SDKMAN_CANDIDATES_CSV="${SDKMAN_CANDIDATES_CSV:-}"\n\n\tCOMPREPLY=()\n\n\tif [ "$COMP_CWORD" -eq 1 ]; then\n\t\tmapfile -t COMPREPLY < <(compgen -W "install uninstall rm list ls use default home env current upgrade ug version broadcast help offline selfupdate update flush" -- "${COMP_WORDS[COMP_CWORD]}")\n\telif [ "$COMP_CWORD" -eq 2 ]; then\n\t\tcase "${COMP_WORDS[COMP_CWORD - 1]}" in\n\t\t\t"install" | "i" | "uninstall" | "rm" | "list" | "ls" | "use" | "u" | "default" | "d" | "home" | "h" | "current" | "c" | "upgrade" | "ug")\n\t\t\t\tCANDIDATES="${SDKMAN_CANDIDATES_CSV//,/${IFS:0:1}}"\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "$CANDIDATES" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t"env")\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "init" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t"offline")\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "enable disable" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t"selfupdate")\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "force" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t"flush")\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "archives tmp broadcast version" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t*) ;;\n\n\t\tesac\n\telif [ "$COMP_CWORD" -eq 3 ]; then\n\t\tcase "${COMP_WORDS[COMP_CWORD - 2]}" in\n\t\t\t"uninstall" | "rm" | "use" | "u" | "default" | "d" | "home" | "h")\n\t\t\t\t_sdkman_candidate_local_versions "${COMP_WORDS[COMP_CWORD - 1]}"\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "$CANDIDATE_VERSIONS" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t"install" | "i")\n\t\t\t\t_sdkman_candidate_all_versions "${COMP_WORDS[COMP_CWORD - 1]}"\n\t\t\t\tmapfile -t COMPREPLY < <(compgen -W "$CANDIDATE_VERSIONS" -- "${COMP_WORDS[COMP_CWORD]}")\n\t\t\t\t;;\n\t\t\t*) ;;\n\n\t\tesac\n\tfi\n\n\treturn 0\n}\n',
    "_sdkman_candidate_local_versions": 'function _sdkman_candidate_local_versions() {\n\n\tCANDIDATE_VERSIONS=$(__sdkman_cleanup_local_versions "$1")\n\n}\n',
    "_sdkman_candidate_all_versions": 'function _sdkman_candidate_all_versions() {\n\n\tcandidate="$1"\n\tCANDIDATE_LOCAL_VERSIONS=$(__sdkman_cleanup_local_versions "$candidate")\n\tif [[ "${SDKMAN_OFFLINE_MODE:-false}" == "true" ]]; then\n\t\tCANDIDATE_VERSIONS=$CANDIDATE_LOCAL_VERSIONS\n\telse\n\t\t# sdkman has a specific output format for Java candidate since\n\t\t# there are multiple vendors and builds.\n\t\tif [ "$candidate" = "java" ]; then\n\t\t\tCANDIDATE_ONLINE_VERSIONS="$(__sdkman_list_versions "$candidate" | grep " " | grep "\\." | cut -c 62-)"\n\t\telse\n\t\t\tCANDIDATE_ONLINE_VERSIONS="$(__sdkman_list_versions "$candidate" | grep " " | grep "\\." | cut -c 6-)"\n\t\tfi\n\t\t# the last grep is used to filter out sdkman flags, such as:\n\t\t# "+" - local version\n\t\t# "*" - installed\n\t\t# ">" - currently in use\n\t\tCANDIDATE_VERSIONS="$(echo "$CANDIDATE_ONLINE_VERSIONS $CANDIDATE_LOCAL_VERSIONS" | tr \' \' \'\\n\' | grep -v -e \'^[[:space:]|\\*|\\>|\\+]*$\' | sort -u) "\n\tfi\n\n}\n',
    "__sdkman_cleanup_local_versions": "function __sdkman_cleanup_local_versions() {\n\n\t__sdkman_build_version_csv \"$1\" | tr ',' ' '\n\n}\n\ncomplete -F _sdkman_complete sdk\n",
}

func_dep_dict_data1_expected = {
    "_sdkman_complete": [
        "_sdkman_candidate_local_versions",
        "_sdkman_candidate_all_versions",
    ],
    "_sdkman_candidate_local_versions": ["__sdkman_cleanup_local_versions"],
    "_sdkman_candidate_all_versions": ["__sdkman_cleanup_local_versions"],
    "__sdkman_cleanup_local_versions": ["_sdkman_complete"],
}


###
func_name_list_data2 = [
    "time-machine-destination",
    "time-machine-list-machines",
    "time-machine-list-all-backups",
    "time-machine-list-old-backups",
    "_tm_startsudo",
    "_tm_stopsudo",
    "time-machine-delete-old-backups",
]
func_text_dict_data2 = {
    "time-machine-destination": 'function time-machine-destination() {\n\tgroup "osx-timemachine"\n\tabout "Shows the OS X Time Machine destination/mount point"\n\n\ttmutil destinationinfo | grep "Mount Point" | sed -e \'s/Mount Point   : \\(.*\\)/\\1/g\'\n}\n',
    "time-machine-list-machines": 'function time-machine-list-machines() {\n\tgroup "osx-timemachine"\n\tabout "Lists the OS X Time Machine machines on the backup volume"\n\n\tlocal tmdest\n\ttmdest="$(time-machine-destination)/Backups.backupdb"\n\n\tfind "$tmdest" -maxdepth 1 -mindepth 1 -type d | grep -v "/\\." | while read -r line; do\n\t\techo "${line##*/}"\n\tdone\n}\n',
    "time-machine-list-all-backups": 'function time-machine-list-all-backups() {\n\tgroup "osx-timemachine"\n\tabout "Shows all of the backups for the specified machine"\n\tparam "1: Machine name (optional)"\n\texample "time-machine-list-all-backups my-laptop"\n\n\t# Use the local hostname if none provided\n\tlocal COMPUTERNAME BACKUP_LOCATION\n\tCOMPUTERNAME=${1:-$(scutil --get ComputerName)}\n\tBACKUP_LOCATION="$(time-machine-destination)/Backups.backupdb/$COMPUTERNAME"\n\n\tfind "$BACKUP_LOCATION" -maxdepth 1 -mindepth 1 -type d | while read -r line; do\n\t\techo "$line"\n\tdone\n}\n',
    "time-machine-list-old-backups": 'function time-machine-list-old-backups() {\n\tgroup "osx-timemachine"\n\tabout "Shows all of the backups for the specified machine, except for the most recent backup"\n\tparam "1: Machine name (optional)"\n\texample "time-machine-list-old-backups my-laptop"\n\n\t# Use the local hostname if none provided\n\tlocal COMPUTERNAME BACKUP_LOCATION\n\tCOMPUTERNAME=${1:-$(scutil --get ComputerName)}\n\tBACKUP_LOCATION="$(time-machine-destination)/Backups.backupdb/$COMPUTERNAME"\n\n\t# List all but the most recent one\n\tfind "$BACKUP_LOCATION" -maxdepth 1 -mindepth 1 -type d -name 2\\* | sed \\$d | while read -r line; do\n\t\techo "$line"\n\tdone\n}\n\n# Taken from here: http://stackoverflow.com/a/30547074/1228454',
    "_tm_startsudo": 'function _tm_startsudo() {\n\tlocal -x SUDO_COMMAND="plugin/osx-timemachine: keep \'sudo\' token alive during long-run \'tmutil\' commands"\n\tsudo "-${SUDO_ASKPASS:+A}v" # validate without running a command, using `ssh-askpass` if available.\n\t(while sudo "-${SUDO_ASKPASS:+A}v"; do\n\t\tsleep 50\n\tdone) &\n\tSUDO_PID="$!"\n\ttrap _tm_stopsudo SIGINT SIGTERM\n}',
    "_tm_stopsudo": 'function _tm_stopsudo() {\n\tkill "$SUDO_PID"\n\ttrap - SIGINT SIGTERM\n\tsudo -k\n}\n',
    "time-machine-delete-old-backups": 'function time-machine-delete-old-backups() {\n\tgroup "osx-timemachine"\n\tabout "Deletes all of the backups for the specified machine, with the exception of the most recent one"\n\tparam "1: Machine name (optional)"\n\texample "time-machine-delete-old-backups my-laptop"\n\n\t# Use the local hostname if none provided\n\tlocal COMPUTERNAME=${1:-$(scutil --get ComputerName)} _old_backup\n\n\t# Ask for sudo credentials only once\n\t_tm_startsudo\n\n\twhile read -r _old_backup; do\n\t\t# Delete the backup\n\t\tsudo tmutil delete "$_old_backup"\n\tdone <<< "$(time-machine-list-old-backups "$COMPUTERNAME")"\n\n\t_tm_stopsudo\n}\n',
}

func_dep_dict_data2_expected = {
    "time-machine-list-machines": ["time-machine-destination"],
    "time-machine-list-all-backups": ["time-machine-destination"],
    "time-machine-list-old-backups": ["time-machine-destination"],
    "_tm_startsudo": ["_tm_stopsudo"],
    "time-machine-delete-old-backups": ["time-machine-list-old-backups"],
}


#############################
