
Internal theme related functions
================================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/internal/internal_colour_functions.sh)***
## Function Index


```python
01 - _check_integer
02 - _check_theme_range
03 - colsw
04 - colsw_path
05 - col_set_prompt_style
06 - csp1
07 - csp2
08 - csp3
09 - col_cp_root
10 - col_ssh
11 - _virtualenv_info
12 - _virtualenv_min_info
13 - _ssh_info
14 - _aws_info
15 - _pwdtail
```

******
### >> _check_integer():


>***about***: Check if argument is an integer


>***group***: internal


>***param***: A putative integer


>***example***: `_check_integer 42`


```bash
function _check_integer() {

    local MYINT="$1"
    local REX=^[0-9]*$
    if [[ "$MYINT" =~ $REX ]]; then
        echo "$MYINT"
    else
        echo 0
    fi
}

```




******
### >> _check_theme_range():


>***about***: Check if argument is an integer between 0 --> N


>***group***: internal


>***param***: 1. A test integer


>***param***: 2. Ma=x number in range


>***example***: `_check_theme_range 56 1003`


```bash
function _check_theme_range() {

    local MYINT="$1"
    local MAX_LEN="$2"
    if [ "$MYINT" -ge 0 -a "$MYINT" -lt "$MAX_LEN" ]; then
        echo "$MYINT"
    else
        echo 0
    fi
}

```




******
### >> colsw():


>***about***: Switch PS1 prompt theme color scheme usining a integer, N. There is a upper limit to N


>***group***: internal


>***param***: 1. A integer corresponding to a theme color scheme. See internal_colour_defs.sh


>***example***: `colsw 42`


```bash
function colsw() {


    local NEWCOL_IDX=${1}

    local NEWCOL_IDX=$(_check_integer "${NEWCOL_IDX}")

    local NEWCOL_IDX=$(_check_theme_range "${NEWCOL_IDX}" "$BARCOL_ARR_LEN")

    cp ${HOME}/stablecaps_bashrc/theme_settings.sh ${HOME}/stablecaps_bashrc/theme_settings_BACKUP.sh
    local CURRCOL_IDX=$(grep "SET_THEME_VAR=" ${HOME}/stablecaps_bashrc/theme_settings.sh | grep -v sed | tr '=' ' ' | awk '{print $2}')

    local CURRPATH_IDX=$(grep "SET_PATHCOL_VAR=" ${HOME}/stablecaps_bashrc/theme_settings.sh | grep -v sed | tr '=' ' ' | awk '{print $2}' | sed 's/\"//g')


    SET_THEME_VAR="${SET_THEME_VAR:=0}"
    SET_BARCOL="${SET_BARCOL:=\[\033[38;5;202m\]}"
    SET_TXTCOL="${SET_TXTCOL:=\[\033[38;5;221m\]}"
    SET_PATHCOL_VAR="${SET_PATHCOL_VAR:=1}"
    SET_PATHCOL="${SET_PATHCOL:=\[\033[0;37m\]}"
cat << BACON > ${HOME}/stablecaps_bashrc/theme_settings.sh




SET_THEME_VAR="${NEWCOL_IDX}"
SET_BARCOL="${BARCOL_ARR[${NEWCOL_IDX}]}"
SET_TXTCOL="${TXTCOL_ARR[${NEWCOL_IDX}]}"
SET_PATHCOL_VAR="${CURRPATH_IDX}"
SET_PATHCOL="${PATH_COLS_ARR[${CURRPATH_IDX}]}"

BACON

    PRINTCOLVAR="ON"
    if [ $PRINTCOLVAR = "ON" ]; then
        PATHCOL_NAME=${PATH_COLS_ARR[${CURRPATH_IDX}]}
        BARCOL_NAME=${BARCOL_ARR[${THEME_VAR}]}
        TXTCOL_NAME=${TXTCOL_ARR[${THEME_VAR}]}
        echo "BARCOL = ${BARCOL_NAME}"
        echo "TXTCOL = ${TXTCOL_NAME}"
        echo "PATHCOL = ${PATHCOL_NAME}"
    fi

    source ${HOME}/stablecaps_bashrc/_bashrc
}

```
##### Function Calls:


```bash
└─ colsw
   ├─ _check_integer
   └─ _check_theme_range
```




******
### >> colsw_path():


>***about***: Fine Tune PS1 prompt theme $PATH_COL_VAR val color scheme usinng a integer, N. There is a upper limit to N


>***group***: internal


>***param***: 1. A integer corresponding to a theme color scheme. See internal_colour_defs.sh


>***example***: `colscolsw_path 2`


```bash
function colsw_path() {

    local NEWPATH_IDX=${1}

    NEWPATH_IDX=$(_check_integer "${NEWPATH_IDX}")

    NEWPATH_IDX=$(_check_theme_range "${NEWPATH_IDX}" "$PATHCOLS_ARR_LEN")

    cp ${HOME}/stablecaps_bashrc/theme_settings.sh ${HOME}/stablecaps_bashrc/theme_settings_BACKUP.sh

    local NEWPATH_COL="${PATH_COLS_ARR[${NEWPATH_IDX}]}"

    sed -i "/^SET_PATHCOL/d" ${HOME}/stablecaps_bashrc/theme_settings.sh

cat << CHEESE >> ${HOME}/stablecaps_bashrc/theme_settings.sh
SET_PATHCOL_VAR="${NEWPATH_IDX}"
SET_PATHCOL="${NEWPATH_COL}"
CHEESE
    echo "No of Themes: $BARCOL_ARR_LEN"
    source ${HOME}/stablecaps_bashrc/_bashrc
}

```
##### Function Calls:


```bash
└─ colsw_path
   ├─ _check_integer
   └─ _check_theme_range
```




******
### >> col_set_prompt_style():


>***about***: Change prompt style between full (3-line), mid (2-line) & default (1-line primitive)


>***group***: internal


>***param***: 1. A integer from 1-3


>***example***: `col_set_prompt_style 1`


```bash
function col_set_prompt_style() {
    local CHOICE="$1"
    if [[ "$CHOICE" =~ (full|mid) ]]; then
        export SET_FULL_PROMPT=$CHOICE
        source ~/.bashrc
    else
        echo "enter 'full' or 'mid'"
    fi
}

```




******
### >> csp1():


>***about***: Change prompt style to full 3-line glory


>***group***: internal


>***example***: `csp1`


```bash
function csp1() {
    col_set_prompt_style full
}

```
##### Function Calls:


```bash
└─ csp1
   └─ col_set_prompt_style
```




******
### >> csp2():


>***about***: Change prompt style to experimental 2-line worrying


>***group***: internal


>***example***: `csp2`


```bash
function csp2() {
    col_set_prompt_style mid
}

```
##### Function Calls:


```bash
└─ csp2
   └─ col_set_prompt_style
```




******
### >> csp3():


>***about***: Change prompt style to a basic 1-line primitive level (default)


>***group***: internal


>***example***: `csp3`


```bash
function csp3() {
    unset SET_FULL_PROMPT
    export SET_FULL_PROMPT=
    source ~/.bashrc
}

```




******
### >> col_cp_root():


>***about***: Copies .bashrc to root home on current machine. Only affects things if full color prompt is set


>***group***: internal


>***example***: `col_cp_root`


```bash
function col_cp_root() {
    sudo mv /root/.bashrc /root/.your_old_bashrc
    sudo cp -rf ${HOME}/stablecaps_bashrc /root/
    sudo ln -s /root/stablecaps_bashrc/_bashrc /root/.bashrc
    sudo su root
    source /root/.bashrc
}

```




******
### >> col_ssh():


>***about***: Copy stablecaps_bashrc PS1 prompt to remote host via rsync


>***group***: internal


>***param***: ${USERNAME}@${HOSTNAME}


>***example***: `col_ssh ubuntu@mywebserver.com`


```bash
function col_ssh() {
    rsync -av ${HOME}/stablecaps_bashrc ${1}:~/
    ssh -A "${1}" 'mv ~/.bashrc ~/.your_old_bashrc; ln -s ${HOME}/stablecaps_bashrc/_bashrc ~/.bashrc'
}

```




******
### >> _virtualenv_info():


>***about***: Get Virtual Env and display in PS prompt (full version)


>***group***: internal


>***example***: `_virtualenv_min_info`


```bash
function _virtualenv_info() {

    local venv=$(_virtualenv_min_info)
    [[ -n "$venv" ]] && echo "${BARCOL}─${TXTCOL}[${HIRed}$venv${TXTCOL}]"
}

```
##### Function Calls:


```bash
└─ _virtualenv_info
   └─ _virtualenv_min_info
```




******
### >> _virtualenv_min_info():


>***about***: Get Virtual Env and display in PS prompt (minimal version)


>***group***: internal


>***example***: `_virtualenv_min_info`


```bash
function _virtualenv_min_info() {

    if [[ -n "$VIRTUAL_ENV" ]]; then
        local venv="${VIRTUAL_ENV##*/}"
    else
        local venv=""
    fi
    [[ -n "$venv" ]] && echo "$venv"
}

```




******
### >> _ssh_info():


>***about***: Display ssh in PS prompt if current seesion is via ssh


>***group***: internal


>***example***: `_ssh_info`


```bash
function _ssh_info() {
    ssh_state=""
    [[ -n "$ssh_state" ]] && echo "${BARCOL}─${TXTCOL}[${HIRed}${ssh_state}${TXTCOL}]"
}

```




******
### >> _aws_info():


>***about***: Display the current AWS profile loaded in PS prompt


>***group***: internal


>***example***: `_aws_info`


```bash
function _aws_info() {
    aws_profile="$(printenv AWS_PROFILE)"
    if [[ -n "${aws_profile}" ]]; then
        set_aws_profile=${aws_profile}
    else
        set_aws_profile=""
    fi
    [[ -n "$set_aws_profile" ]] && echo "${BARCOL}─${TXTCOL}[${HIRed}${set_aws_profile}${TXTCOL}]"
}

```




******
### >> _pwdtail():


>***about***: Display last two directories from `pwd` in PS prompt


>***group***: internal


>***example***: `_pwdtail`


```bash
function _pwdtail() {

    pwd | awk -F/ '{nlast = NF -1;print $nlast"/"$NF}' #TODO: Use for something?
}

```


