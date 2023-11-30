
Base module
===========


***(in /home/bsgt/stablecaps_bashrc/modules/base_module.sh)***
## Function Index


```python
01 - ips
02 - down4me
03 - myip
04 - pickfrom
05 - passgen
06 - mkcd
07 - lsgrep
08 - usage
09 - comex
10 - default-file-dir-perms-set
11 - buf
12 - del
13 - rm-except
14 - gedit
15 - nomacs
16 - Ngedit
17 - terminator
18 - grepo
19 - grepoall
20 - del_file_by_patt
21 - venv_create
22 - venv_activate
```

******
### >> ips():


>***about***: display all ip addresses for this host


>***group***: base


```bash
function ips() {

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

```




******
### >> down4me():


>***about***: checks whether a website is down for you, or everybody


>***group***: base


>***param***: 1: website url


>***example***: `$ down4me http://www.google.com`


```bash
function down4me() {

    curl -Ls "http://downforeveryoneorjustme.com/$1" | sed '/just you/!d;s/<[^>]*>//g'
}

```




******
### >> myip():


>***about***: displays your ip address, as seen by the Internet


>***group***: base


```bash
function myip() {

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

```




******
### >> pickfrom():


>***about***: picks random line from file


>***group***: base


>***param***: 1: filename


>***example***: `$ pickfrom /usr/share/dict/words`


```bash
function pickfrom() {

    local file=$1
    [ -z "$file" ] && reference $FUNCNAME && return
    length=$(cat $file | wc -l)
    n=$(expr $RANDOM \* $length \/ 32768 + 1)
    head -n $n $file | tail -1
}

```




******
### >> passgen():


>***about***: generates random password from dictionary words


>***group***: base


>***param***: optional integer length


>***param***: if unset, defaults to 4


>***example***: `$ passgen`


>***example***: `$ passgen 6`


```bash
function passgen() {

    local i pass length=${1:-4}
    pass=$(echo $(for i in $(eval echo "{1..$length}"); do pickfrom /usr/share/dict/words; done))
    echo "With spaces (easier to memorize): $pass"
    echo "Without (use this as the password): $(echo $pass | tr -d ' ')"
}

```
##### Function Calls:


```bash
└─ passgen
   └─ pickfrom
```




******
### >> mkcd():


>***about***: make one or more directories and cd into the last one


>***group***: base


>***param***: one or more directories to create


>***example***: `$ mkcd foo`


>***example***: `$ mkcd /tmp/img/photos/large`


>***example***: `$ mkcd foo foo1 foo2 fooN`


>***example***: `$ mkcd /tmp/img/photos/large /tmp/img/photos/self /tmp/img/photos/Beijing`


```bash
function mkcd() {

    mkdir -p -- "$@" && eval cd -- "\"\$$#\""
}

```




******
### >> lsgrep():


>***about***: search through directory contents with grep


>***group***: base


```bash
function lsgrep() {

    ls | grep "$*"
}

```




******
### >> usage():


>***about***: disk usage per directory, in Mac OS X and Linux


>***group***: base


>***param***: 1: directory name


```bash
function usage() {

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

```




******
### >> comex():


>***about***: checks for existence of a command


>***group***: base


>***param***: 1: command to check


>***example***: `$ comex ls`


```bash
function comex() {

    type "$1"  #&> /dev/null ;
}

```




******
### >> default-file-dir-perms-set():


>***about***: Recursively set directories to 0755 & files under `pwd` to 0644 octal perms


>***group***: base


>***example***: `default-file-dir-perms-set`


```bash
function default-file-dir-perms-set() {

    find . -type d -print0 | xargs -r -0 chmod 0755
    find . -type f -print0 | xargs -r -0 chmod 0644
}

```




******
### >> buf():


>***about***: back up file with timestamp


>***group***: base


>***param***: filename


>***example***: `buf $filename`


```bash
function buf() {

    local filename=$1
    local filetime=$(date +%Y%m%d_%H%M%S)
    cp -a "${filename}" "${filename}_${filetime}"
}

```




******
### >> del():


>***about***: move files to hidden folder in tmp, that gets cleared on each reboot


>***group***: base


>***param***: file or folder to be deleted


>***example***: `del $filename`


>***example***: `del $foldername`


```bash
function del() {

    mkdir -p /tmp/.trash && mv "$@" /tmp/.trash;
}

```




******
### >> rm-except():


>***about***: Remove all files/directories except for one file


>***group***: base


>***param***: file or folder to be deleted


>***example***: `rm-except $filename`


>***example***: `rm-except $foldername`


```bash
function rm-except() {

    local keep_file=$1

    find . ! -name "$keep_file" -type f -exec rm -f {} +
}

```




******
### >> gedit():


>***about***: Opens non-blocking program from terminal


>***group***: base


>***example***: `gedit $filename`


```bash
function gedit() {

    command gedit "$@" &>/dev/null &
}

```




******
### >> nomacs():


>***about***: Opens non-blocking program from terminal


>***group***: base


>***example***: `nomacs $filename`


```bash
function nomacs() {

    command nomacs "$@" &>/dev/null &
}

```




******
### >> Ngedit():


>***about***: Opens non-blocking program from terminal


>***group***: base


>***example***: `Ngedit $filename`


```bash
function Ngedit() {

    command gedit --new-window "$@" &>/dev/null &
}

```
##### Function Calls:


```bash
└─ Ngedit
   └─ gedit
```




******
### >> terminator():


>***about***: Opens non-blocking program from terminal


>***group***: base


>***example***: `terminator $filename`


```bash
function terminator() {

    command terminator --geometry=945x1200+0+0 "$@" &>/dev/null &
}

```




******
### >> grepo():


>***about***: Find all files "*" recursively from current directory and grep within each file for a pattern


>***group***: base


>***param***: Pattern to grep for


>***example***: `grepo $PATERN`


>***example***: `grepo import`


```bash
function grepo() {
    find ./ -not -path "*/\.*" -not -path "*venv/*" -not -path "*node_modules/*" -name "*" -exec grep --color=auto -Isi "$1" {}  \;
}

```




******
### >> grepoall():


>***about***: Find all files "*" recursively from current directory and grep within each file for a pattern


>***group***: base


>***param***: 1. Pattern to grep for


>***param***: 2. File type to find in double quotes


>***example***: `grepoall $PATERN`


>***example***: `grepoall import`


>***example***: `grepoall $PATERN $FILE_PATTERN`


>***example***: `grepoall import "*.py"`


```bash
function grepoall() {

    TXT_PATTERN="$1"
    if [[ $# -eq 2 ]]; then
        FILE_SEARCH="$2"
    else
        FILE_SEARCH="*"
    fi

    find ./ -not -path "*/\.*" -not -path "*venv/*" -not -path "*node_modules/*" -iname "${FILE_SEARCH}" -exec grep --color=auto -Isin "$TXT_PATTERN" {} /dev/null \;
}

```




******
### >> del_file_by_patt():


>***about***: Delete all files matching a pattern


>***group***: base


>***param***: 1. Delete pattern


>***example***: `del_file_by_patt $DEL_PATERN`


>***example***: `del_file_by_patt "*.css"`


```bash
function del_file_by_patt() {

    file_ext="$1"
    find . -name "$file_ext" -exec rm -fv {} \;
}

```




******
### >> venv_create():


>***about***: Create & activte a python virtual environment. Works with Python3


>***group***: base


>***param***: python version findable on path. Test with $(which)


>***example***: `venv_create python3.6`


```bash
function venv_create() {

    if [[ $# -ge 1 ]]; then
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

```




******
### >> venv_activate():


>***about***: Activte an existing python virtual environment


>***group***: base


>***param***: python version findable on path. Test with $(which)


>***example***: `venv_activate`


```bash
function venv_activate() {

    source venv/bin/activate
}

```


