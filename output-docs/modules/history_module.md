
History functions
=================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_stablecaps_bashrc/docs/modules/history_module.sh)***
## Function Index


```python
01 - hist_nlines
02 - grep_history
03 - _chop_first_column
04 - _add_line_numbers
05 - _top_ten
06 - _unique_history
07 - ghf
08 - histdel
09 - histdeln
```

******
### >> hist_nlines():


>***about***: Get last N entries from bash history. N default is 100 lines


>***group***: history


>***param***: 1: An integer corresponding to the number of history lines to tail


>***example***: `$ hist_nlines 200`


```bash
function hist_nlines() {

    if [ $# -eq 0 ]; then num_lines=100; else num_lines=$1; fi

    history | tail -n $num_lines;
}

```




******
### >> grep_history():


>***about***: Grep bash history


>***group***: history


>***example***: `$ grep_history ls`


```bash
function grep_history() {

    history | grep "$1" ;
}

```




******
### >> _chop_first_column():


```bash
function _chop_first_column() { awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' ; }

```




******
### >> _add_line_numbers():


```bash
function _add_line_numbers() { awk '{print NR " " $0}' ; }

```




******
### >> _top_ten():


```bash
function _top_ten() { sort | uniq -c | sort -r | head -n 10 ; }

```




******
### >> _unique_history():


```bash
function _unique_history() { _chop_first_column | _top_ten | _chop_first_column | _add_line_numbers ; }

```
##### Function Calls:


```bash
└─ _unique_history
   ├─ _chop_first_column
   ├─ _add_line_numbers
   └─ _top_ten
```




******
### >> ghf():


>***about***: Grep bash history Function


>***group***: history


>***param***: 1: With no args supplied, ghf returns the top 10 most used commands


>***param***: 2: With 1 search strings ghf returns top 10 uses for that term


>***param***: 3: With 2 search strings ghf executes a further search filter to the top10


>***example***: `$ grep_history mkdir`


```bash
function ghf() {

    if [ $# -eq 0 ]; then hist_nlines | _unique_history; fi
    if [ $# -eq 1 ]; then grep_history "$1" | _unique_history; fi
    if [ $# -eq 2 ]; then
        $(grep_history "$1" | _unique_history | grep ^$2 | _chop_first_column)
    fi
}

```
##### Function Calls:


```bash
└─ ghf
   ├─ hist_nlines
   ├─ grep_history
   └─ _unique_history
      ├─ _chop_first_column
      ├─ _add_line_numbers
      └─ _top_ten
```




******
### >> histdel():


>***about***: Delete lines of history between N -> N+n. Excluding histdel iteself.


>***group***: history


>***param***: 1: starting line to delete


>***param***: 2: ending line to delete


>***example***: `$ histdel 1000 1033`


```bash
function histdel() {

    for h in $(seq $1 $2 | tac); do
        history -d $h
    done
    history -d $(history 1 | awk '{print $1}')
}

```




******
### >> histdeln():


>***about***: Delete last N lines of history including histdeln


>***group***: history


>***param***: 1: Number of lines to delete


>***example***: `$ histdeln 10`


```bash
function histdeln() {

    n=$(history 1 | awk '{print $1}')

    histdel $(( $n - $1 )) $(( $n - 1 ))
}

```
##### Function Calls:


```bash
└─ histdeln
   └─ histdel
```



## Aliases


| **Alias Name** | **Code** | **Notes** |
| ------------- | ------------- | ------------- |
| **hist** | `history'` |  shows all history
| **gh** | `history | grep '` |  grep all history
