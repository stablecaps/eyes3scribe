
Internal PS prompt related git functions
========================================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_stablecaps_bashrc/docs/internal/internal_git_functions.sh)***
## Function Index


```python
01 - _parse_git
02 - _parse_git_minimal
03 - _find_git_branch
04 - _get_git_commid
05 - _find_git_dirty
06 - _git_com_diff
07 - _format_git_stats
```

******
### >> _parse_git():


>***about***: Formats prompt: Calls functions to find various git attribiutes. See call graph.


>***group***: internal


>***example***: `_parse_git()`


```bash
function _parse_git() {

    git_str=$(_find_git_branch)
    if [[ ! -z "$git_str" ]]; then
        git_str="${BARCOL}──${TXTCOL}[$(_git_com_diff)${git_str}$(_find_git_dirty)"

        git_str="${git_str}$(_format_git_stats)"

        git_str="${git_str}${TXTCOL}]"


        echo $git_str
    else
        echo ""
    fi
}

```
##### Function Calls:


```bash
└─ _parse_git
   ├─ _find_git_branch
   ├─ _find_git_dirty
   ├─ _git_com_diff
   └─ _format_git_stats
```




******
### >> _parse_git_minimal():


>***about***: Formats prompt: Alternative option to _parse_git().


>***group***: internal


>***example***: `_parse_git_minimal()`


```bash
function _parse_git_minimal() {

    git_str=$(_find_git_branch)
    if [[ ! -z "$git_str" ]]; then
        git_str="${BARCOL}─${TXTCOL}(${git_str}$(_find_git_dirty)"

        git_str="${git_str}${TXTCOL})"


        echo $git_str
    else
        echo ""
    fi
}

```
##### Function Calls:


```bash
└─ _parse_git_minimal
   ├─ _find_git_branch
   └─ _find_git_dirty
```




******
### >> _find_git_branch():


>***about***: Print git branch if in a repo


>***group***: internal


>***example***: `_find_git_branch()`


```bash
function _find_git_branch() {

    local branch=$(git rev-parse --abbrev-ref HEAD 2> /dev/null)
    if [[ ! -z "$branch" ]]; then
        if [[ "$branch" == "HEAD" ]]; then
            branch_fmt="${RED}!detached"
        else
            branch_fmt="${TXTCOL}${branch}"
        fi
        git_branch="${branch_fmt}"
    else
        git_branch=""
    fi
    echo $git_branch
}

```




******
### >> _get_git_commid():


>***about***: Print current and previous commit id


>***group***: internal


>***example***: `_get_git_commid()`


```bash
function _get_git_commid() {

    curr_commitid=$(git rev-parse --short HEAD 2> /dev/null)
    prev_commitid=$(git rev-list --max-count=2 --abbrev-commit HEAD  | tail -1)
    echo "${BARCOL}──${TXTCOL}[c~${curr_commitid}]${BARCOL}──${TXTCOL}[p~${prev_commitid}]"
}

```




******
### >> _find_git_dirty():


>***about***: Mark with a dirty yellow star* if there are uncommitted/unstaged entities in git


>***group***: internal


>***example***: `_find_git_dirty()`


```bash
function _find_git_dirty() {

    gdirtstr=$(git status 2> /dev/null | tail -n1 | sed 's/,//' | awk '{print $1, $2, $3}')
    if [[ ${gdirtstr} == "nothing to commit" ]]
        then
        dirty_state=""
    elif [[ ${gdirtstr} == "" ]]
        then
        dirty_state=""
    else
        dirty_state='\[\033[01;38;5;221m\]*'
    fi
    echo $dirty_state
}

```




******
### >> _git_com_diff():


>***about***: Calculate how far git branch is relative to origin. (Probably imperfect)


>***group***: internal


>***example***: `_git_com_diff()`


```bash
function _git_com_diff() {

    gbranchrel=$(git status 2> /dev/null | grep "Your branch is")
    gup=$(echo $gbranchrel 2> /dev/null | grep ahead)
    gdown=$(echo $gbranchrel 2> /dev/null | grep behind)
    grelN=$(echo $gbranchrel | sed -nr 's/.*by ([0-9]+) commit?[a-z]./\1/p')

    gupdown=""
    if [[ $gup != "" ]]; then
        gupdown="${grelN}↑"
    fi

    if [[ $gdown != "" ]]; then
        gupdown="${grelN}↓"
    fi
    echo $gupdown
}

```




******
### >> _format_git_stats():


>***about***: Calcualte git stats & print out numbers to PS prompt indicating files taht are (u)ntracked, (a)dded, (m)odified, (am) & (d)deleted


>***group***: internal


>***example***: `_format_git_stats()`


```bash
function _format_git_stats() {

    gporcelain=$(git status --porcelain 2> /dev/null)
    untrN=$(echo $gporcelain | tr ' ' '\n' | grep -w '??' | wc -l) # untracked
    addN=$(echo $gporcelain | tr ' ' '\n' | grep -w '^A' | wc -l)  # added
    modN=$(echo $gporcelain | tr ' ' '\n' | grep -w '^M' | wc -l)  # modified
    commN=$(echo $gporcelain | tr ' ' '\n' | grep -w '^AM' | wc -l)  # added & modified?
    delN=$(echo $gporcelain | tr ' ' '\n' | grep -w '^D' | wc -l)  # deleted


    gitlegend=""
    gitstats_str=""
    if [[ $untrN != "0" ]]; then
        gitlegend="${gitlegend}${TEAL}u"
        gitstats_str="${gitstats_str}${TEAL}${untrN}"
    fi

    if [[ $addN != "0" ]]; then
        gitlegend="${gitlegend}${LBLUE}a"
        gitstats_str="${gitstats_str}${LBLUE}${addN}"
    fi

    if [[ $modN != "0" ]]; then
        gitlegend="${gitlegend}${MAGENTA}m"
        gitstats_str="${gitstats_str}${MAGENTA}${modN}"
    fi

    if [[ $commN != "0" ]]; then
        gitlegend="${gitlegend}${HIGreen}c"
        gitstats_str="${gitstats_str}${HIGreen}${commN}"
    fi

    if [[ $delN != "0" ]]; then
        gitlegend="${gitlegend}${RED}d"
        gitstats_str="${gitstats_str}${RED}${delN}"
    fi

    gitlegend="${gitlegend}${SLATE}: "


    if [[ $gitstats_str == "" ]]; then
        joined_gitstats=""
    else
        joined_gitstats=" ${gitlegend}${gitstats_str}"
    fi
    echo "${gupdown}${TXTCOL}${gbranchstr}${dirty_state}${joined_gitstats}"
}

```


