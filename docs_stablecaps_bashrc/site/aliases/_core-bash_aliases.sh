cite about-alias
about-alias 'Core BASH Aliases'

function check_alias_clashes() {
	about 'Check alias clashes'
	group 'aliases'
	example '$ check_alias_clashes'

	# alias lists defined aliases and sed extracts their name.
	# The while loop runs type -ta on each of them and awk
	# prints the lines that both contain alias and file.
	alias | sed 's/^[^ ]* *\|=.*$//g' | while read a; do
	printf "%20.20s : %s\n" $a "$(type -ta $a | tr '\n' ' ')"
	done | awk -F: '$2 ~ /file/'
}

alias mkdir='mkdir -p'

function mkcd() {
	about 'Make a folder and go into it'
	group 'aliases'
	param '1: Name of the directory to create & enter'
	example 'mkcd my_new_dir'

    mkdir -p $1; cd $1
}


# ls commands

# switch to use exa instead of ls if available on system
if command -v exa >/dev/null; then
    alias ls='${HOME}/stablecaps_bashrc/internal/internal_exa_wrapper.sh'
else
    alias ls='/bin/ls -ah --color=always'
fi

#alias ls='ls -ah --color=always' # ls always has --color switched on & shows all files
alias qs='/bin/ls' # fast ls with no options (many files in a directory)
alias la='ls -Alh' # show hidden files
alias lao='ls -ld .?*' # show ONLY hidden files
alias lx='ls -lXBh' # sort by extension
alias lk='ls -lSrh' # sort by size
alias lc='ls -lcrh' # sort by change time
alias lu='ls -lurh' # sort by access time
alias lr='ls -lRh' # recursive ls
alias lt='ls -ltrh' # sort by date
alias lm='ls -alh | less' # pipe through 'less'
alias lw='ls -xAh' # wide listing format
alias ll='ls -lth' # long listing format
alias labc='ls -lap' #alphabetical sort
alias lf="ls -l | egrep -v '^d'" # files only
alias ldir="ls -l | egrep '^d'" # directories only

# exa - uncomment if it is installed on the system
# https://github.com/sharkdp/vivid # to generate LS_COLORS
# https://github.com/trapd00r/LS_COLORS
#ayu
alias ex='exa -a --group --color=automatic --classify'
alias exl='exa -al --group --links --grid --color=automatic --classify'


# function exlt() {
# 	about 'Exa long with tree view with option to limit the number of levels'
# 	group 'aliases'
# 	param 'number of levels'
# 	example '$ exlt'
# 	example '$ exlt 2'

# 	local num_levels=$1
# 	if [ num_levels == "" ]; then
# 		exa -al --group --links --grid --tree --color=automatic --classify --level
# 	else
# 		exa -al --group --links --grid --tree --color=automatic --classify --level $num_levels
# 	fi
# }

# exa --ignore-glob="*case*"
# exa --ignore-glob="Open*|rot??.sh|*case*"
# exa --sort=ext



# cd commands
alias cd..='cd ..'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias bashrc='cd ${HOME}/stablecaps_bashrc; ll' # Switch to stablecaps_bashrc directory in home and ls

# Goes up a specified number of directories  (i.e. up 4)
function up() {
	about 'Go up N directories in the file path'
	group 'aliases'
	param '1: Integer corresponding to number of directories to go up.'
	example '$ up 3'

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

# other commands
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

alias edbash='gedit ~/.bashrc ~/stablecaps_bashrc/internal/*.sh &'
alias F5='source ~/.bashrc'


## df -
alias df='df -x "squashfs"' # Stop showing mounted snap in file system
alias dfraw='df' # raw df with all options disabled


### bat
alias bat='bat --paging=never --theme "Monokai Extended --plain"'
alias batx='bat --paging=always --theme "Monokai Extended"'
alias bata='bat --show-all'

alias bathelp='bat --plain --language=help'
help() {
	about 'Uses bat to colorize help text messages'
	group 'aliases'
	param 'Name of program whose help text we wish to pipe to bat'
	example '$ help mv'
	example '$ help git commit'
    "$@" --help 2>&1 | bathelp
}