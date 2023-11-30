cite about-module
about-module 'Base module'


function ips() {
    about 'display all ip addresses for this host'
    group 'base'

    if command -v ifconfig &>/dev/null
    then
        ifconfig | awk '/inet /{ gsub(/addr:/, ""); print $2 }'
    elif command -v ip &>/dev/null
    then
        ip addr | grep -oP 'inet \K[\d.]+'
    else
        echo "You don't have ifconfig or ip command installed!"
    fi
}

function down4me() {
    about 'checks whether a website is down for you, or everybody'
    group 'base'
    param '1: website url'
    example '$ down4me http://www.google.com'

    curl -Ls "http://downforeveryoneorjustme.com/$1" | sed '/just you/!d;s/<[^>]*>//g'
}

function myip() {
    about 'displays your ip address, as seen by the Internet'
    group 'base'

    list=("http://myip.dnsomatic.com/" "http://checkip.dyndns.com/" "http://checkip.dyndns.org/")
    for url in ${list[*]}
    do
        res=$(curl -s "${url}")
        if [ $? -eq 0 ];then
            break;
        fi
    done
    res=$(echo "$res" | grep -Eo '[0-9\.]+')
    echo -e "Your public IP is: ${echo_bold_green} $res ${echo_normal}"
}

function pickfrom() {
    about 'picks random line from file'
    group 'base'
    param '1: filename'
    example '$ pickfrom /usr/share/dict/words'

    local file=$1
    [ -z "$file" ] && reference $FUNCNAME && return
    length=$(cat $file | wc -l)
    n=$(expr $RANDOM \* $length \/ 32768 + 1)
    head -n $n $file | tail -1
}

function passgen() {
    about 'generates random password from dictionary words'
    group 'base'
    param 'optional integer length'
    param 'if unset, defaults to 4'
    example '$ passgen'
    example '$ passgen 6'

    local i pass length=${1:-4}
    pass=$(echo $(for i in $(eval echo "{1..$length}"); do pickfrom /usr/share/dict/words; done))
    echo "With spaces (easier to memorize): $pass"
    echo "Without (use this as the password): $(echo $pass | tr -d ' ')"
}

function mkcd() {
    about 'make one or more directories and cd into the last one'
    group 'base'
    param 'one or more directories to create'
    example '$ mkcd foo'
    example '$ mkcd /tmp/img/photos/large'
    example '$ mkcd foo foo1 foo2 fooN'
    example '$ mkcd /tmp/img/photos/large /tmp/img/photos/self /tmp/img/photos/Beijing'

    mkdir -p -- "$@" && eval cd -- "\"\$$#\""
}

function lsgrep() {
    about 'search through directory contents with grep'
    group 'base'

    ls | grep "$*"
}

function usage() {
    about 'disk usage per directory, in Mac OS X and Linux'
    group 'base'
    param '1: directory name'

    if [ $(uname) = "Darwin" ]; then
        if [ -n "$1" ]; then
            du -hd 1 "$1"
        else
            du -hd 1
        fi

    elif [ $(uname) = "Linux" ]; then
        if [ -n "$1" ]; then
            du -h --max-depth=1 "$1"
        else
            du -h --max-depth=1
        fi
    fi
}

function comex() {
    about 'checks for existence of a command'
    group 'base'
    param '1: command to check'
    example '$ comex ls'

    type "$1"  #&> /dev/null ;
}


function default-file-dir-perms-set() {
    about 'Recursively set directories to 0755 & files under `pwd` to 0644 octal perms'
    group 'base'
    example 'default-file-dir-perms-set'

    find . -type d -print0 | xargs -r -0 chmod 0755
    find . -type f -print0 | xargs -r -0 chmod 0644
}

function buf() {
    about 'back up file with timestamp'
    group 'base'
    param 'filename'
    example 'buf $filename'

    local filename=$1
    local filetime=$(date +%Y%m%d_%H%M%S)
    cp -a "${filename}" "${filename}_${filetime}"
}

function del() {
    about 'move files to hidden folder in tmp, that gets cleared on each reboot'
    group 'base'
    param 'file or folder to be deleted'
    example 'del $filename'
    example 'del $foldername'

    mkdir -p /tmp/.trash && mv "$@" /tmp/.trash;
}

function rm-except() {
    about 'Remove all files/directories except for one file'
    group 'base'
    param 'file or folder to be deleted'
    example 'rm-except $filename'
    example 'rm-except $foldername'

    local keep_file=$1

    find . ! -name "$keep_file" -type f -exec rm -f {} +
}



function gedit() {
    about 'Opens non-blocking program from terminal'
    group 'base'
    example 'gedit $filename'

    command gedit "$@" &>/dev/null &
}

function nomacs() {
    about 'Opens non-blocking program from terminal'
    group 'base'
    example 'nomacs $filename'

    command nomacs "$@" &>/dev/null &
}

function Ngedit() {
    about 'Opens non-blocking program from terminal'
    group 'base'
    example 'Ngedit $filename'

    command gedit --new-window "$@" &>/dev/null &
}

function terminator() {
    about 'Opens non-blocking program from terminal'
    group 'base'
    example 'terminator $filename'

    command terminator --geometry=945x1200+0+0 "$@" &>/dev/null &
}

function grepo() {
    about 'Find all files "*" recursively from current directory and grep within each file for a pattern'
    group 'base'
    param 'Pattern to grep for'
    example 'grepo $PATERN'
    example 'grepo import'
    # finds all files in current directory recursively and searches each for grep pattern
    # (case insensitive)
    find ./ -not -path "*/\.*" -not -path "*venv/*" -not -path "*node_modules/*" -name "*" -exec grep --color=auto -Isi "$1" {}  \;
}

function grepoall() {
    about 'Find all files "*" recursively from current directory and grep within each file for a pattern'
    group 'base'
    param '1. Pattern to grep for'
    param '2. File type to find in double quotes'
    example 'grepoall $PATERN'
    example 'grepoall import'
    example 'grepoall $PATERN $FILE_PATTERN'
    example 'grepoall import "*.py"'
    # finds all files in current directory recursively and searches each for grep pattern
    # Shows the file name in which the pattern was found (case insensitive + linenumber)
    # FILE_SEARCH eaxmple "*.py" with quotes or "*" if not supplied

    TXT_PATTERN="$1"
    if [[ $# -eq 2 ]]; then
        FILE_SEARCH="$2"
    else
        FILE_SEARCH="*"
    fi

    find ./ -not -path "*/\.*" -not -path "*venv/*" -not -path "*node_modules/*" -iname "${FILE_SEARCH}" -exec grep --color=auto -Isin "$TXT_PATTERN" {} /dev/null \;
}

function del_file_by_patt() {
    about 'Delete all files matching a pattern'
    group 'base'
    param '1. Delete pattern'
    example 'del_file_by_patt $DEL_PATERN'
    example 'del_file_by_patt "*.css"'

    file_ext="$1"
    find . -name "$file_ext" -exec rm -fv {} \;
}

# TODO: figure out virtualenv for python2
# https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe
function venv_create() {
    about 'Create & activte a python virtual environment. Works with Python3'
    group 'base'
    param 'python version findable on path. Test with $(which)'
    example 'venv_create python3.6'

    if [[ $# -ge 1 ]]; then
        # takes argument like python3.6
        desired_py_version=$1
        pyth_ver=$(which $desired_py_version)
        if [[ -z "${pyth_ver}" ]]; then
            echo "python version $desired_py_version not found"
        else
            $pyth_ver -m venv venv
            source venv/bin/activate
        fi
    else
        echo "supply an arg"
    fi
}

function venv_activate() {
    about 'Activte an existing python virtual environment'
    group 'base'
    param 'python version findable on path. Test with $(which)'
    example 'venv_activate'

    source venv/bin/activate
}

#--------------------------------------------------------------
#  Automatic setting of $DISPLAY (if not set already).
#  This works for me - your mileage may vary. . . .
#  The problem is that different types of terminals give
#+ different answers to 'who am i' (rxvt in particular can be
#+ troublesome) - however this code seems to work in a majority
#+ of cases.
#--------------------------------------------------------------

# function get_xserver ()
# {
#     case $TERM in
#         xterm )
#             XSERVER=$(whoami | awk '{print $NF}' | tr -d ')''(' )
#             # Ane-Pieter Wieringa suggests the following alternative:
#             #  I_AM=$(who am i)
#             #  SERVER=${I_AM#*(}
#             #  SERVER=${SERVER%*)}
#             XSERVER=${XSERVER%%:*}
#             ;;
#             aterm | rxvt)
#             # Find some code that works here. ...
#             ;;
#     esac
# }

# if [ -z ${DISPLAY:=""} ]; then
#     get_xserver
#     if [[ -z ${XSERVER}  || ${XSERVER} == $(hostname) ||
#        ${XSERVER} == "unix" ]]; then
#           DISPLAY=":0.0"          # Display on local host.
#     else
#        DISPLAY=${XSERVER}:0.0     # Display on remote host.
#     fi
# fi

# export DISPLAY