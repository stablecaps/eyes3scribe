
Core BASH Aliases
=================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/aliases/_core-bash_aliases.sh)***
## Function Index


```python
01 - check_alias_clashes
02 - mkcd
03 - up
```

******
### >> check_alias_clashes():


>***about***: Check alias clashes


>***group***: aliases


>***example***: `$ check_alias_clashes`


```bash
function check_alias_clashes() {

	alias | sed 's/^[^ ]* *\|=.*$//g' | while read a; do
	printf "%20.20s : %s\n" $a "$(type -ta $a | tr '\n' ' ')"
	done | awk -F: '$2 ~ /file/'
}

```
##### Function Calls:


```bash
└─ check_alias_clashes
   └─ up
```




******
### >> mkcd():


>***about***: Make a folder and go into it


>***group***: aliases


>***param***: 1: Name of the directory to create & enter


>***example***: `mkcd my_new_dir`


# 	>***about***: Exa long with tree view with option to limit the number of levels


# 	>***group***: aliases


# 	>***param***: number of levels


```bash
function mkcd() {

    mkdir -p $1; cd $1
}



if command -v exa >/dev/null; then
    alias ls='${HOME}/stablecaps_bashrc/internal/internal_exa_wrapper.sh'
else
    alias ls='/bin/ls -ah --color=always'
fi

```
##### Function Calls:


```bash
└─ mkcd
   └─ up
```




******
### >> up():


>***about***: Go up N directories in the file path


>***group***: aliases


>***param***: 1: Integer corresponding to number of directories to go up.


>***example***: `$ up 3`


>***about***: Uses bat to colorize help text messages


>***group***: aliases


>***param***: Name of program whose help text we wish to pipe to bat


>***example***: `$ help mv`


>***example***: `$ help git commit`


```bash
function up() {

	local d=""
	limit=$1
	for ((i=1 ; i <= limit ; i++))
		do
			d=$d/..
		done
	d=$(echo $d | sed 's/^\///')
	if [ -z "$d" ]; then
		d=..
	fi
	cd $d
}







help() {
    "$@" --help 2>&1 | bathelp
}

```



## Aliases


| **Alias Name** | **Code** | **Notes** |
| ------------- | ------------- | ------------- |
| **mkdir** | `mkdir -p` | 
| **qs** | `/bin/ls'` |  fast ls with no options (many files in a directory)
| **la** | `ls -Alh'` |  show hidden files
| **lao** | `ls -ld .?*'` |  show ONLY hidden files
| **lx** | `ls -lXBh'` |  sort by extension
| **lk** | `ls -lSrh'` |  sort by size
| **lc** | `ls -lcrh'` |  sort by change time
| **lu** | `ls -lurh'` |  sort by access time
| **lr** | `ls -lRh'` |  recursive ls
| **lt** | `ls -ltrh'` |  sort by date
| **lm** | `ls -alh | less'` |  pipe through 'less'
| **lw** | `ls -xAh'` |  wide listing format
| **ll** | `ls -lth'` |  long listing format
| **labc** | `ls -lap'` | alphabetical sort
| **lf** | `ls -l | egrep -v '^d'"` |  files only
| **ldir** | `ls -l | egrep '^d'"` |  directories only
| **ex** | `exa -a --group --color=automatic --classify` | 
| **exl** | `exa -al --group --links --grid --color=automatic --classify` | 
| **cd..** | `cd ..` | 
| **..** | `cd ..` | 
| **...** | `cd ../..` | 
| **....** | `cd ../../..` | 
| **.....** | `cd ../../../..` | 
| **bashrc** | `cd ${HOME}/stablecaps_bashrc; ll'` |  Switch to stablecaps_bashrc directory in home and ls
| **grep** | `grep --color=auto` | 
| **egrep** | `egrep --color=auto` | 
| **fgrep** | `fgrep --color=auto` | 
| **edbash** | `gedit ~/.bashrc ~/stablecaps_bashrc/internal/*.sh &` | 
| **F5** | `source ~/.bashrc` | 
| **df** | `df -x "squashfs"'` |  Stop showing mounted snap in file system
| **dfraw** | `df'` |  raw df with all options disabled
| **bat** | `bat --paging=never --theme "Monokai Extended --plain"` | 
| **batx** | `bat --paging=always --theme "Monokai Extended"` | 
| **bata** | `bat --show-all` | 
| **bathelp** | `bat --plain --language=help` | 
