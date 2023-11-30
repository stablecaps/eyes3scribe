
GIT Completions
===============


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/completions/git_completion.sh)***
## Function Index


```python
01 - __git_find_repo_path
02 - __gitdir
03 - __git
04 - __git_dequote
05 - __git_reassemble_comp_words_by_ref
06 - __gitcomp_direct
07 - __gitcompappend
08 - __gitcompadd
09 - __gitcomp
10 - __gitcomp_builtin
11 - __gitcomp_nl_append
12 - __gitcomp_nl
13 - __gitcomp_file_direct
14 - __gitcomp_file
15 - __git_ls_files_helper
16 - __git_index_files
17 - __git_complete_index_file
18 - __git_heads
19 - __git_tags
20 - __git_refs
21 - __git_complete_refs
22 - __git_refs2
23 - __git_complete_fetch_refspecs
24 - __git_refs_remotes
25 - __git_remotes
26 - __git_is_configured_remote
27 - __git_list_merge_strategies
28 - __git_compute_merge_strategies
29 - __git_complete_revlist_file
30 - __git_complete_file
31 - __git_complete_revlist
32 - __git_complete_remote_or_refspec
33 - __git_complete_strategy
34 - __git_compute_all_commands
35 - __git_get_config_variables
36 - __git_pretty_aliases
37 - __git_aliased_command
38 - __git_find_on_cmdline
39 - __git_get_option_value
40 - __git_has_doubledash
41 - __git_count_arguments
42 - _git_am
43 - _git_apply
44 - _git_add
45 - _git_archive
46 - _git_bisect
47 - _git_branch
48 - _git_bundle
49 - _git_checkout
50 - _git_cherry_pick
51 - _git_clean
52 - _git_clone
53 - _git_commit
54 - _git_describe
55 - _git_diff
56 - _git_difftool
57 - _git_fetch
58 - _git_format_patch
59 - _git_fsck
60 - _git_gitk
61 - __git_match_ctag
62 - __git_complete_symbol
63 - _git_grep
64 - _git_help
65 - _git_init
66 - _git_ls_files
67 - _git_ls_remote
68 - _git_log
69 - _git_merge
70 - _git_mergetool
71 - _git_merge_base
72 - _git_mv
73 - _git_notes
74 - _git_pull
75 - __git_complete_force_with_lease
76 - _git_push
77 - _git_range_diff
78 - _git_rebase
79 - _git_reflog
80 - _git_send_email
81 - _git_stage
82 - _git_status
83 - __git_config_get_set_variables
84 - __git_compute_config_vars
85 - _git_config
86 - _git_remote
87 - _git_replace
88 - _git_rerere
89 - _git_reset
90 - _git_revert
91 - _git_rm
92 - _git_shortlog
93 - _git_show
94 - _git_show_branch
95 - _git_stash
96 - _git_submodule
97 - _git_svn
98 - _git_tag
99 - _git_whatchanged
100 - _git_worktree
101 - __git_complete_common
102 - __git_support_parseopt_helper
103 - __git_complete_command
104 - __git_main
105 - __gitk_main
106 - __git_func_wrap
107 - __git_complete
108 - _git
109 - _gitk
```

******
### >> __git_find_repo_path():


```bash
function __git_find_repo_path() {
	if [ -n "$__git_repo_path" ]; then
		return
	fi

	if [ -n "${__git_C_args-}" ]; then
		__git_repo_path="$(git "${__git_C_args[@]}" \
			${__git_dir:+--git-dir="$__git_dir"} \
			rev-parse --absolute-git-dir 2>/dev/null)"
	elif [ -n "${__git_dir-}" ]; then
		test -d "$__git_dir" &&
		__git_repo_path="$__git_dir"
	elif [ -n "${GIT_DIR-}" ]; then
		test -d "${GIT_DIR-}" &&
		__git_repo_path="$GIT_DIR"
	elif [ -d .git ]; then
		__git_repo_path=.git
	else
		__git_repo_path="$(git rev-parse --git-dir 2>/dev/null)"
	fi
}

```




******
### >> __gitdir():


```bash
function __gitdir() {
	if [ -z "${1-}" ]; then
		__git_find_repo_path || return 1
		echo "$__git_repo_path"
	elif [ -d "$1/.git" ]; then
		echo "$1/.git"
	else
		echo "$1"
	fi
}

```
##### Function Calls:


```bash
└─ __gitdir
   └─ __git_find_repo_path
```




******
### >> __git():


```bash
function __git() {
	git ${__git_C_args:+"${__git_C_args[@]}"} \
		${__git_dir:+--git-dir="$__git_dir"} "$@" 2>/dev/null
}

```




******
### >> __git_dequote():


```bash
function __git_dequote() {
	local rest="$1" len ch

	dequoted_word=""

	while test -n "$rest"; do
		len=${#dequoted_word}
		dequoted_word="$dequoted_word${rest%%[\\\'\"]*}"
		rest="${rest:$((${#dequoted_word}-$len))}"

		case "${rest:0:1}" in
		\\)
			ch="${rest:1:1}"
			case "$ch" in
			$'\n')
				;;
			*)
				dequoted_word="$dequoted_word$ch"
				;;
			esac
			rest="${rest:2}"
			;;
		\')
			rest="${rest:1}"
			len=${#dequoted_word}
			dequoted_word="$dequoted_word${rest%%\'*}"
			rest="${rest:$((${#dequoted_word}-$len+1))}"
			;;
		\")
			rest="${rest:1}"
			while test -n "$rest" ; do
				len=${#dequoted_word}
				dequoted_word="$dequoted_word${rest%%[\\\"]*}"
				rest="${rest:$((${#dequoted_word}-$len))}"
				case "${rest:0:1}" in
				\\)
					ch="${rest:1:1}"
					case "$ch" in
					\"|\\|\$|\`)
						dequoted_word="$dequoted_word$ch"
						;;
					$'\n')
						;;
					*)
						dequoted_word="$dequoted_word\\$ch"
						;;
					esac
					rest="${rest:2}"
					;;
				\")
					rest="${rest:1}"
					break
					;;
				esac
			done
			;;
		esac
	done
}

```




******
### >> __git_reassemble_comp_words_by_ref():


```bash
function __git_reassemble_comp_words_by_ref() {
	local exclude i j first
	exclude="${1//[^$COMP_WORDBREAKS]}"
	cword_=$COMP_CWORD
	if [ -z "$exclude" ]; then
		words_=("${COMP_WORDS[@]}")
		return
	fi
	for ((i=0, j=0; i < ${#COMP_WORDS[@]}; i++, j++)); do
		first=t
		while
			[ $i -gt 0 ] &&
			[ -n "${COMP_WORDS[$i]}" ] &&
			[ "${COMP_WORDS[$i]//[^$exclude]}" = "${COMP_WORDS[$i]}" ]
		do
			if [ $j -ge 2 ] && [ -n "$first" ]; then
				((j--))
			fi
			first=
			words_[$j]=${words_[j]}${COMP_WORDS[i]}
			if [ $i = $COMP_CWORD ]; then
				cword_=$j
			fi
			if (($i < ${#COMP_WORDS[@]} - 1)); then
				((i++))
			else
				return
			fi
		done
		words_[$j]=${words_[j]}${COMP_WORDS[i]}
		if [ $i = $COMP_CWORD ]; then
			cword_=$j
		fi
	done
}

if ! type _get_comp_words_by_ref >/dev/null 2>&1; then

```




******
### >> __gitcomp_direct():


```bash
function  __gitcomp_direct() {
	local IFS=$'\n'

	COMPREPLY=($1)
}

```




******
### >> __gitcompappend():


```bash
function __gitcompappend() {
	local x i=${#COMPREPLY[@]}
	for x in $1; do
		if [[ "$x" == "$3"* ]]; then
			COMPREPLY[i++]="$2$x$4"
		fi
	done
}

```




******
### >> __gitcompadd():


```bash
function __gitcompadd() {
	COMPREPLY=()
	__gitcompappend "$@"
}

```
##### Function Calls:


```bash
└─ __gitcompadd
   └─ __gitcompappend
```




******
### >> __gitcomp():


```bash
function __gitcomp() {
	local cur_="${3-$cur}"

	case "$cur_" in
	--*=)
		;;
	--no-*)
		local c i=0 IFS=$' \t\n'
		for c in $1; do
			if [[ $c == "--" ]]; then
				continue
			fi
			c="$c${4-}"
			if [[ $c == "$cur_"* ]]; then
				case $c in
				--*=*|*.) ;;
				*) c="$c " ;;
				esac
				COMPREPLY[i++]="${2-}$c"
			fi
		done
		;;
	*)
		local c i=0 IFS=$' \t\n'
		for c in $1; do
			if [[ $c == "--" ]]; then
				c="--no-...${4-}"
				if [[ $c == "$cur_"* ]]; then
					COMPREPLY[i++]="${2-}$c "
				fi
				break
			fi
			c="$c${4-}"
			if [[ $c == "$cur_"* ]]; then
				case $c in
				--*=*|*.) ;;
				*) c="$c " ;;
				esac
				COMPREPLY[i++]="${2-}$c"
			fi
		done
		;;
	esac
}

if [[ -n ${ZSH_VERSION-} ]]; then
	unset $(set |sed -ne 's/^\(__gitcomp_builtin_[a-zA-Z0-9_][a-zA-Z0-9_]*\)=.*/\1/p') 2>/dev/null
else
	unset $(compgen -v __gitcomp_builtin_)
fi

```




******
### >> __gitcomp_builtin():


```bash
function __gitcomp_builtin() {
	local cmd="$1"
	local incl="$2"
	local excl="$3"

	local var=__gitcomp_builtin_"${cmd/-/_}"
	local options
	eval "options=\$$var"

	if [ -z "$options" ]; then
		options=" $incl $(__git ${cmd/_/ } --git-completion-helper) "
		for i in $excl; do
			options="${options/ $i / }"
		done
		eval "$var=\"$options\""
	fi

	__gitcomp "$options"
}

```
##### Function Calls:


```bash
└─ __gitcomp_builtin
   ├─ __git
   ├─ __gitcomp
   └─ _git
```




******
### >> __gitcomp_nl_append():


```bash
function __gitcomp_nl_append() {
	local IFS=$'\n'
	__gitcompappend "$1" "${2-}" "${3-$cur}" "${4- }"
}

```
##### Function Calls:


```bash
└─ __gitcomp_nl_append
   └─ __gitcompappend
```




******
### >> __gitcomp_nl():


```bash
function __gitcomp_nl() {
	COMPREPLY=()
	__gitcomp_nl_append "$@"
}

```
##### Function Calls:


```bash
└─ __gitcomp_nl
   └─ __gitcomp_nl_append
      └─ __gitcompappend
```




******
### >> __gitcomp_file_direct():


```bash
function __gitcomp_file_direct() {
	local IFS=$'\n'

	COMPREPLY=($1)

	compopt -o filenames +o nospace 2>/dev/null ||
	compgen -f /non-existing-dir/ >/dev/null ||
	true
}

```




******
### >> __gitcomp_file():


```bash
function __gitcomp_file() {
	local IFS=$'\n'

	__gitcompadd "$1" "${2-}" "${3-$cur}" ""

	compopt -o filenames +o nospace 2>/dev/null ||
	compgen -f /non-existing-dir/ >/dev/null ||
	true
}

```
##### Function Calls:


```bash
└─ __gitcomp_file
   └─ __gitcompadd
      └─ __gitcompappend
```




******
### >> __git_ls_files_helper():


```bash
function __git_ls_files_helper() {
	if [ "$2" == "--committable" ]; then
		__git -C "$1" -c core.quotePath=false diff-index \
			--name-only --relative HEAD -- "${3//\\/\\\\}*"
	else
		__git -C "$1" -c core.quotePath=false ls-files \
			--exclude-standard $2 -- "${3//\\/\\\\}*"
	fi
}

```
##### Function Calls:


```bash
└─ __git_ls_files_helper
   ├─ __git
   └─ _git
```




******
### >> __git_index_files():


```bash
function __git_index_files() {
	local root="$2" match="$3"

	__git_ls_files_helper "$root" "$1" "$match" |
	awk -F / -v pfx="${2//\\/\\\\}" '{
		paths[$1] = 1
	}
	END {
		for (p in paths) {
			if (substr(p, 1, 1) != "\"") {
				print pfx p
				continue
			}

			p = dequote(p)
			if (p == "")
				continue

			if (p in paths)
				continue
			else
				print pfx p
		}
	}
	function dequote(p,    bs_idx, out, esc, esc_idx, dec) {
		p = substr(p, 2)

		while ((bs_idx = index(p, "\\")) != 0) {
			out = out substr(p, 1, bs_idx - 1)
			esc = substr(p, bs_idx + 1, 1)
			p = substr(p, bs_idx + 2)

			if ((esc_idx = index("abtvfr\"\\", esc)) != 0) {
				out = out substr("\a\b\t\v\f\r\"\\",
						 esc_idx, 1)
			} else if (esc == "n") {
				return ""
			} else {
				dec = esc             * 64 + \
				      substr(p, 1, 1) * 8  + \
				      substr(p, 2, 1)
				out = out sprintf("%c", dec)
				p = substr(p, 3)
			}
		}
		if (substr(p, length(p), 1) == "\"")
			out = out substr(p, 1, length(p) - 1)
		else
			out = out p

		return out
	}'
}

```
##### Function Calls:


```bash
└─ __git_index_files
   └─ __git_ls_files_helper
      ├─ __git
      └─ _git
```




******
### >> __git_complete_index_file():


```bash
function __git_complete_index_file() {
	local dequoted_word pfx="" cur_

	__git_dequote "$cur"

	case "$dequoted_word" in
	?*/*)
		pfx="${dequoted_word%/*}/"
		cur_="${dequoted_word##*/}"
		;;
	*)
		cur_="$dequoted_word"
	esac

	__gitcomp_file_direct "$(__git_index_files "$1" "$pfx" "$cur_")"
}

```
##### Function Calls:


```bash
└─ __git_complete_index_file
   ├─ __git_dequote
   ├─ __gitcomp_file_direct
   └─ __git_index_files
      └─ __git_ls_files_helper
```




******
### >> __git_heads():


```bash
function __git_heads() {
	local pfx="${1-}" cur_="${2-}" sfx="${3-}"

	__git for-each-ref --format="${pfx//\%/%%}%(refname:strip=2)$sfx" \
			"refs/heads/$cur_*" "refs/heads/$cur_*/**"
}

```
##### Function Calls:


```bash
└─ __git_heads
   ├─ __git
   └─ _git
```




******
### >> __git_tags():


```bash
function __git_tags() {
	local pfx="${1-}" cur_="${2-}" sfx="${3-}"

	__git for-each-ref --format="${pfx//\%/%%}%(refname:strip=2)$sfx" \
			"refs/tags/$cur_*" "refs/tags/$cur_*/**"
}

```
##### Function Calls:


```bash
└─ __git_tags
   ├─ __git
   └─ _git
```




******
### >> __git_refs():


```bash
function __git_refs() {
	local i hash dir track="${2-}"
	local list_refs_from=path remote="${1-}"
	local format refs
	local pfx="${3-}" cur_="${4-$cur}" sfx="${5-}"
	local match="${4-}"
	local fer_pfx="${pfx//\%/%%}" # "escape" for-each-ref format specifiers

	__git_find_repo_path
	dir="$__git_repo_path"

	if [ -z "$remote" ]; then
		if [ -z "$dir" ]; then
			return
		fi
	else
		if __git_is_configured_remote "$remote"; then
			list_refs_from=remote
		elif [ -d "$remote/.git" ]; then
			dir="$remote/.git"
		elif [ -d "$remote" ]; then
			dir="$remote"
		else
			list_refs_from=url
		fi
	fi

	if [ "$list_refs_from" = path ]; then
		if [[ "$cur_" == ^* ]]; then
			pfx="$pfx^"
			fer_pfx="$fer_pfx^"
			cur_=${cur_#^}
			match=${match#^}
		fi
		case "$cur_" in
		refs|refs/*)
			format="refname"
			refs=("$match*" "$match*/**")
			track=""
			;;
		*)
			for i in HEAD FETCH_HEAD ORIG_HEAD MERGE_HEAD REBASE_HEAD; do
				case "$i" in
				$match*)
					if [ -e "$dir/$i" ]; then
						echo "$pfx$i$sfx"
					fi
					;;
				esac
			done
			format="refname:strip=2"
			refs=("refs/tags/$match*" "refs/tags/$match*/**"
				"refs/heads/$match*" "refs/heads/$match*/**"
				"refs/remotes/$match*" "refs/remotes/$match*/**")
			;;
		esac
		__git_dir="$dir" __git for-each-ref --format="$fer_pfx%($format)$sfx" \
			"${refs[@]}"
		if [ -n "$track" ]; then
			__git for-each-ref --format="$fer_pfx%(refname:strip=3)$sfx" \
				--sort="refname:strip=3" \
				"refs/remotes/*/$match*" "refs/remotes/*/$match*/**" | \
			uniq -u
		fi
		return
	fi
	case "$cur_" in
	refs|refs/*)
		__git ls-remote "$remote" "$match*" | \
		while read -r hash i; do
			case "$i" in
			*^{}) ;;
			*) echo "$pfx$i$sfx" ;;
			esac
		done
		;;
	*)
		if [ "$list_refs_from" = remote ]; then
			case "HEAD" in
			$match*)	echo "${pfx}HEAD$sfx" ;;
			esac
			__git for-each-ref --format="$fer_pfx%(refname:strip=3)$sfx" \
				"refs/remotes/$remote/$match*" \
				"refs/remotes/$remote/$match*/**"
		else
			local query_symref
			case "HEAD" in
			$match*)	query_symref="HEAD" ;;
			esac
			__git ls-remote "$remote" $query_symref \
				"refs/tags/$match*" "refs/heads/$match*" \
				"refs/remotes/$match*" |
			while read -r hash i; do
				case "$i" in
				*^{})	;;
				refs/*)	echo "$pfx${i#refs/*/}$sfx" ;;
				*)	echo "$pfx$i$sfx" ;;  # symbolic refs
				esac
			done
		fi
		;;
	esac
}

```
##### Function Calls:


```bash
└─ __git_refs
   ├─ __git
   ├─ __git_is_configured_remote
   |  └─ __git_remotes
   └─ _git
```




******
### >> __git_complete_refs():


```bash
function __git_complete_refs() {
	local remote track pfx cur_="$cur" sfx=" "

	while test $# != 0; do
		case "$1" in
		--remote=*)	remote="${1##--remote=}" ;;
		--track)	track="yes" ;;
		--pfx=*)	pfx="${1##--pfx=}" ;;
		--cur=*)	cur_="${1##--cur=}" ;;
		--sfx=*)	sfx="${1##--sfx=}" ;;
		*)		return 1 ;;
		esac
		shift
	done

	__gitcomp_direct "$(__git_refs "$remote" "$track" "$pfx" "$cur_" "$sfx")"
}

```
##### Function Calls:


```bash
└─ __git_complete_refs
   ├─ __gitcomp_direct
   └─ __git_refs
      ├─ __git
      ├─ __git_is_configured_remote
      └─ _git
```




******
### >> __git_refs2():


```bash
function __git_refs2() {
	local i
	for i in $(__git_refs "$1"); do
		echo "$i:$i"
	done
}

```
##### Function Calls:


```bash
└─ __git_refs2
   └─ __git_refs
      ├─ __git
      ├─ __git_is_configured_remote
      └─ _git
```




******
### >> __git_complete_fetch_refspecs():


```bash
function __git_complete_fetch_refspecs() {
	local i remote="$1" pfx="${2-}" cur_="${3-$cur}" sfx="${4- }"

	__gitcomp_direct "$(
		for i in $(__git_refs "$remote" "" "" "$cur_") ; do
			echo "$pfx$i:$i$sfx"
		done
		)"
}

```
##### Function Calls:


```bash
└─ __git_complete_fetch_refspecs
   ├─ __gitcomp_direct
   └─ __git_refs
      ├─ __git
      ├─ __git_is_configured_remote
      └─ _git
```




******
### >> __git_refs_remotes():


```bash
function __git_refs_remotes() {
	local i hash
	__git ls-remote "$1" 'refs/heads/*' | \
	while read -r hash i; do
		echo "$i:refs/remotes/$1/${i#refs/heads/}"
	done
}

```
##### Function Calls:


```bash
└─ __git_refs_remotes
   ├─ __git
   └─ _git
```




******
### >> __git_remotes():


```bash
function __git_remotes() {
	__git_find_repo_path
	test -d "$__git_repo_path/remotes" && ls -1 "$__git_repo_path/remotes"
	__git remote
}

```
##### Function Calls:


```bash
└─ __git_remotes
   ├─ __git
   └─ _git
```




******
### >> __git_is_configured_remote():


```bash
function __git_is_configured_remote() {
	local remote
	for remote in $(__git_remotes); do
		if [ "$remote" = "$1" ]; then
			return 0
		fi
	done
	return 1
}

```
##### Function Calls:


```bash
└─ __git_is_configured_remote
   └─ __git_remotes
      ├─ __git
      └─ _git
```




******
### >> __git_list_merge_strategies():


```bash
function __git_list_merge_strategies() {
	LANG=C LC_ALL=C git merge -s help 2>&1 |
	sed -n -e '/[Aa]vailable strategies are: /,/^$/{
		s/\.$//
		s/.*://
		s/^[ 	]*//
		s/[ 	]*$//
		p
	}'
}

__git_merge_strategies=

```




******
### >> __git_compute_merge_strategies():


```bash
function __git_compute_merge_strategies() {
	test -n "$__git_merge_strategies" ||
	__git_merge_strategies=$(__git_list_merge_strategies)
}

```
##### Function Calls:


```bash
└─ __git_compute_merge_strategies
   └─ __git_list_merge_strategies
```




******
### >> __git_complete_revlist_file():


```bash
function __git_complete_revlist_file()  {
	local dequoted_word pfx ls ref cur_="$cur"
	case "$cur_" in
	*..?*:*)
		return
		;;
	?*:*)
		ref="${cur_%%:*}"
		cur_="${cur_#*:}"

		__git_dequote "$cur_"

		case "$dequoted_word" in
		?*/*)
			pfx="${dequoted_word%/*}"
			cur_="${dequoted_word##*/}"
			ls="$ref:$pfx"
			pfx="$pfx/"
			;;
		*)
			cur_="$dequoted_word"
			ls="$ref"
			;;
		esac

		case "$COMP_WORDBREAKS" in
		*:*) : great ;;
		*)   pfx="$ref:$pfx" ;;
		esac

		__gitcomp_file "$(__git ls-tree "$ls" \
				| sed 's/^.*	//
				       s/$//')" \
			"$pfx" "$cur_"
		;;
	*...*)
		pfx="${cur_%...*}..."
		cur_="${cur_#*...}"
		__git_complete_refs --pfx="$pfx" --cur="$cur_"
		;;
	*..*)
		pfx="${cur_%..*}.."
		cur_="${cur_#*..}"
		__git_complete_refs --pfx="$pfx" --cur="$cur_"
		;;
	*)
		__git_complete_refs
		;;
	esac
}

```
##### Function Calls:


```bash
└─ __git_complete_revlist_file
   ├─ __git
   ├─ __git_dequote
   ├─ __gitcomp_file
   |  └─ __gitcompadd
   ├─ __git_complete_refs
   |  ├─ __gitcomp_direct
   |  └─ __git_refs
   └─ _git
```




******
### >> __git_complete_file():


```bash
function __git_complete_file() {
	__git_complete_revlist_file
}

```




******
### >> __git_complete_revlist():


```bash
function __git_complete_revlist() {
	__git_complete_revlist_file
}

```




******
### >> __git_complete_remote_or_refspec():


```bash
function __git_complete_remote_or_refspec() {
	local cur_="$cur" cmd="${words[1]}"
	local i c=2 remote="" pfx="" lhs=1 no_complete_refspec=0
	if [ "$cmd" = "remote" ]; then
		((c++))
	fi
	while [ $c -lt $cword ]; do
		i="${words[c]}"
		case "$i" in
		--mirror) [ "$cmd" = "push" ] && no_complete_refspec=1 ;;
		-d|--delete) [ "$cmd" = "push" ] && lhs=0 ;;
		--all)
			case "$cmd" in
			push) no_complete_refspec=1 ;;
			fetch)
				return
				;;
			*) ;;
			esac
			;;
		--multiple) no_complete_refspec=1; break ;;
		-*) ;;
		*) remote="$i"; break ;;
		esac
		((c++))
	done
	if [ -z "$remote" ]; then
		__gitcomp_nl "$(__git_remotes)"
		return
	fi
	if [ $no_complete_refspec = 1 ]; then
		return
	fi
	[ "$remote" = "." ] && remote=
	case "$cur_" in
	*:*)
		case "$COMP_WORDBREAKS" in
		*:*) : great ;;
		*)   pfx="${cur_%%:*}:" ;;
		esac
		cur_="${cur_#*:}"
		lhs=0
		;;
	+*)
		pfx="+"
		cur_="${cur_#+}"
		;;
	esac
	case "$cmd" in
	fetch)
		if [ $lhs = 1 ]; then
			__git_complete_fetch_refspecs "$remote" "$pfx" "$cur_"
		else
			__git_complete_refs --pfx="$pfx" --cur="$cur_"
		fi
		;;
	pull|remote)
		if [ $lhs = 1 ]; then
			__git_complete_refs --remote="$remote" --pfx="$pfx" --cur="$cur_"
		else
			__git_complete_refs --pfx="$pfx" --cur="$cur_"
		fi
		;;
	push)
		if [ $lhs = 1 ]; then
			__git_complete_refs --pfx="$pfx" --cur="$cur_"
		else
			__git_complete_refs --remote="$remote" --pfx="$pfx" --cur="$cur_"
		fi
		;;
	esac
}

```
##### Function Calls:


```bash
└─ __git_complete_remote_or_refspec
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   ├─ __git_complete_refs
   |  ├─ __gitcomp_direct
   |  └─ __git_refs
   ├─ __git_complete_fetch_refspecs
   |  ├─ __gitcomp_direct
   |  └─ __git_refs
   └─ __git_remotes
      ├─ __git
      └─ _git
```




******
### >> __git_complete_strategy():


```bash
function __git_complete_strategy() {
	__git_compute_merge_strategies
	case "$prev" in
	-s|--strategy)
		__gitcomp "$__git_merge_strategies"
		return 0
	esac
	case "$cur" in
	--strategy=*)
		__gitcomp "$__git_merge_strategies" "" "${cur##--strategy=}"
		return 0
		;;
	esac
	return 1
}

__git_all_commands=

```
##### Function Calls:


```bash
└─ __git_complete_strategy
   └─ __gitcomp
```




******
### >> __git_compute_all_commands():


```bash
function __git_compute_all_commands() {
	test -n "$__git_all_commands" ||
	__git_all_commands=$(git --list-cmds=main,others,alias,nohelpers)
}

```




******
### >> __git_get_config_variables():


```bash
function __git_get_config_variables() {
	local section="$1" i IFS=$'\n'
	for i in $(__git config --name-only --get-regexp "^$section\..*"); do
		echo "${i#$section.}"
	done
}

```
##### Function Calls:


```bash
└─ __git_get_config_variables
   ├─ __git
   └─ _git
```




******
### >> __git_pretty_aliases():


```bash
function __git_pretty_aliases() {
	__git_get_config_variables "pretty"
}

```
##### Function Calls:


```bash
└─ __git_pretty_aliases
   └─ __git_get_config_variables
      ├─ __git
      └─ _git
```




******
### >> __git_aliased_command():


```bash
function __git_aliased_command() {
	local word cmdline=$(__git config --get "alias.$1")
	for word in $cmdline; do
		case "$word" in
		\!gitk|gitk)
			echo "gitk"
			return
			;;
		\!*)	: shell command alias ;;
		-*)	: option ;;
		*=*)	: setting env ;;
		git)	: git itself ;;
		\(\))   : skip parens of shell function definition ;;
		{)	: skip start of shell helper function ;;
		:)	: skip null command ;;
		\'*)	: skip opening quote after sh -c ;;
		*)
			echo "$word"
			return
		esac
	done
}

```
##### Function Calls:


```bash
└─ __git_aliased_command
   ├─ __git
   └─ _git
```




******
### >> __git_find_on_cmdline():


```bash
function __git_find_on_cmdline() {
	local word subcommand c=1
	while [ $c -lt $cword ]; do
		word="${words[c]}"
		for subcommand in $1; do
			if [ "$subcommand" = "$word" ]; then
				echo "$subcommand"
				return
			fi
		done
		((c++))
	done
}

```




******
### >> __git_get_option_value():


```bash
function __git_get_option_value() {
	local c short_opt long_opt val
	local result= values config_key word

	short_opt="$1"
	long_opt="$2"
	values="$3"
	config_key="$4"

	((c = $cword - 1))
	while [ $c -ge 0 ]; do
		word="${words[c]}"
		for val in $values; do
			if [ "$short_opt$val" = "$word" ] ||
			   [ "$long_opt$val"  = "$word" ]; then
				result="$val"
				break 2
			fi
		done
		((c--))
	done

	if [ -n "$config_key" ] && [ -z "$result" ]; then
		result="$(__git config "$config_key")"
	fi

	echo "$result"
}

```
##### Function Calls:


```bash
└─ __git_get_option_value
   ├─ __git
   └─ _git
```




******
### >> __git_has_doubledash():


```bash
function __git_has_doubledash() {
	local c=1
	while [ $c -lt $cword ]; do
		if [ "--" = "${words[c]}" ]; then
			return 0
		fi
		((c++))
	done
	return 1
}

```




******
### >> __git_count_arguments():


```bash
function __git_count_arguments() {
	local word i c=0

	for ((i=1; i < ${#words[@]}; i++)); do
		word="${words[i]}"

		case "$word" in
			--)
				((c = 0))
				;;
			"$1")
				((c = 0))
				;;
			?*)
				((c++))
				;;
		esac
	done

	printf "%d" $c
}

__git_whitespacelist="nowarn warn error error-all fix"
__git_am_inprogress_options="--skip --continue --resolved --abort --quit --show-current-patch"

```




******
### >> _git_am():


```bash
function _git_am() {
	__git_find_repo_path
	if [ -d "$__git_repo_path"/rebase-apply ]; then
		__gitcomp "$__git_am_inprogress_options"
		return
	fi
	case "$cur" in
	--whitespace=*)
		__gitcomp "$__git_whitespacelist" "" "${cur##--whitespace=}"
		return
		;;
	--*)
		__gitcomp_builtin am "" \
			"$__git_am_inprogress_options"
		return
	esac
}

```
##### Function Calls:


```bash
└─ _git_am
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_apply():


```bash
function _git_apply() {
	case "$cur" in
	--whitespace=*)
		__gitcomp "$__git_whitespacelist" "" "${cur##--whitespace=}"
		return
		;;
	--*)
		__gitcomp_builtin apply
		return
	esac
}

```
##### Function Calls:


```bash
└─ _git_apply
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_add():


```bash
function _git_add() {
	case "$cur" in
	--*)
		__gitcomp_builtin add
		return
	esac

	local complete_opt="--others --modified --directory --no-empty-directory"
	if test -n "$(__git_find_on_cmdline "-u --update")"
	then
		complete_opt="--modified"
	fi
	__git_complete_index_file "$complete_opt"
}

```
##### Function Calls:


```bash
└─ _git_add
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_complete_index_file
   |  ├─ __git_dequote
   |  ├─ __gitcomp_file_direct
   |  └─ __git_index_files
   └─ __git_find_on_cmdline
```




******
### >> _git_archive():


```bash
function  _git_archive() {
	case "$cur" in
	--format=*)
		__gitcomp "$(git archive --list)" "" "${cur##--format=}"
		return
		;;
	--remote=*)
		__gitcomp_nl "$(__git_remotes)" "" "${cur##--remote=}"
		return
		;;
	--*)
		__gitcomp "
			--format= --list --verbose
			--prefix= --remote= --exec= --output
			"
		return
		;;
	esac
	__git_complete_file
}

```
##### Function Calls:


```bash
└─ _git_archive
   ├─ __gitcomp
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   └─ __git_remotes
      ├─ __git
      └─ _git
```




******
### >> _git_bisect():


```bash
function  _git_bisect() {
	__git_has_doubledash && return

	local subcommands="start bad good skip reset visualize replay log run"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"
	if [ -z "$subcommand" ]; then
		__git_find_repo_path
		if [ -f "$__git_repo_path"/BISECT_START ]; then
			__gitcomp "$subcommands"
		else
			__gitcomp "replay start"
		fi
		return
	fi

	case "$subcommand" in
	bad|good|reset|skip|start)
		__git_complete_refs
		;;
	*)
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_bisect
   ├─ __gitcomp
   ├─ __git_find_on_cmdline
   └─ __git_has_doubledash
```




******
### >> _git_branch():


```bash
function _git_branch() {
	local i c=1 only_local_ref="n" has_r="n"

	while [ $c -lt $cword ]; do
		i="${words[c]}"
		case "$i" in
		-d|--delete|-m|--move)	only_local_ref="y" ;;
		-r|--remotes)		has_r="y" ;;
		esac
		((c++))
	done

	case "$cur" in
	--set-upstream-to=*)
		__git_complete_refs --cur="${cur##--set-upstream-to=}"
		;;
	--*)
		__gitcomp_builtin branch
		;;
	*)
		if [ $only_local_ref = "y" -a $has_r = "n" ]; then
			__gitcomp_direct "$(__git_heads "" "$cur" " ")"
		else
			__git_complete_refs
		fi
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_branch
   ├─ __gitcomp_direct
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_heads
   |  ├─ __git
   |  └─ _git
   └─ __git_complete_refs
      ├─ __gitcomp_direct
      └─ __git_refs
```




******
### >> _git_bundle():


```bash
function _git_bundle() {
	local cmd="${words[2]}"
	case "$cword" in
	2)
		__gitcomp "create list-heads verify unbundle"
		;;
	3)
		;;
	*)
		case "$cmd" in
			create)
				__git_complete_revlist
			;;
		esac
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_bundle
   └─ __gitcomp
```




******
### >> _git_checkout():


```bash
function _git_checkout() {
	__git_has_doubledash && return

	case "$cur" in
	--conflict=*)
		__gitcomp "diff3 merge" "" "${cur##--conflict=}"
		;;
	--*)
		__gitcomp_builtin checkout
		;;
	*)
		local flags="--track --no-track --no-guess" track_opt="--track"
		if [ "$GIT_COMPLETION_CHECKOUT_NO_GUESS" = "1" ] ||
		   [ -n "$(__git_find_on_cmdline "$flags")" ]; then
			track_opt=''
		fi
		__git_complete_refs $track_opt
		;;
	esac
}

__git_cherry_pick_inprogress_options="--continue --quit --abort"

```
##### Function Calls:


```bash
└─ _git_checkout
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_complete_refs
   |  ├─ __gitcomp_direct
   |  └─ __git_refs
   ├─ __git_find_on_cmdline
   └─ __git_has_doubledash
```




******
### >> _git_cherry_pick():


```bash
function _git_cherry_pick() {
	__git_find_repo_path
	if [ -f "$__git_repo_path"/CHERRY_PICK_HEAD ]; then
		__gitcomp "$__git_cherry_pick_inprogress_options"
		return
	fi
	case "$cur" in
	--*)
		__gitcomp_builtin cherry-pick "" \
			"$__git_cherry_pick_inprogress_options"
		;;
	*)
		__git_complete_refs
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_cherry_pick
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_clean():


```bash
function _git_clean() {
	case "$cur" in
	--*)
		__gitcomp_builtin clean
		return
		;;
	esac

	__git_complete_index_file "--others --directory"
}

```
##### Function Calls:


```bash
└─ _git_clean
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_complete_index_file
      ├─ __git_dequote
      ├─ __gitcomp_file_direct
      └─ __git_index_files
```




******
### >> _git_clone():


```bash
function _git_clone() {
	case "$cur" in
	--*)
		__gitcomp_builtin clone
		return
		;;
	esac
}

__git_untracked_file_modes="all no normal"

```
##### Function Calls:


```bash
└─ _git_clone
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_commit():


```bash
function _git_commit() {
	case "$prev" in
	-c|-C)
		__git_complete_refs
		return
		;;
	esac

	case "$cur" in
	--cleanup=*)
		__gitcomp "default scissors strip verbatim whitespace
			" "" "${cur##--cleanup=}"
		return
		;;
	--reuse-message=*|--reedit-message=*|\
	--fixup=*|--squash=*)
		__git_complete_refs --cur="${cur#*=}"
		return
		;;
	--untracked-files=*)
		__gitcomp "$__git_untracked_file_modes" "" "${cur##--untracked-files=}"
		return
		;;
	--*)
		__gitcomp_builtin commit
		return
	esac

	if __git rev-parse --verify --quiet HEAD >/dev/null; then
		__git_complete_index_file "--committable"
	else
		__git_complete_index_file "--cached"
	fi
}

```
##### Function Calls:


```bash
└─ _git_commit
   ├─ __git
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_complete_index_file
   |  ├─ __git_dequote
   |  ├─ __gitcomp_file_direct
   |  └─ __git_index_files
   ├─ __git_complete_refs
   |  ├─ __gitcomp_direct
   |  └─ __git_refs
   └─ _git
```




******
### >> _git_describe():


```bash
function _git_describe() {
	case "$cur" in
	--*)
		__gitcomp_builtin describe
		return
	esac
	__git_complete_refs
}

__git_diff_algorithms="myers minimal patience histogram"

__git_diff_submodule_formats="diff log short"

__git_diff_common_options="--stat --numstat --shortstat --summary
			--patch-with-stat --name-only --name-status --color
			--no-color --color-words --no-renames --check
			--full-index --binary --abbrev --diff-filter=
			--find-copies-harder --ignore-cr-at-eol
			--text --ignore-space-at-eol --ignore-space-change
			--ignore-all-space --ignore-blank-lines --exit-code
			--quiet --ext-diff --no-ext-diff
			--no-prefix --src-prefix= --dst-prefix=
			--inter-hunk-context=
			--patience --histogram --minimal
			--raw --word-diff --word-diff-regex=
			--dirstat --dirstat= --dirstat-by-file
			--dirstat-by-file= --cumulative
			--diff-algorithm=
			--submodule --submodule= --ignore-submodules
"

```
##### Function Calls:


```bash
└─ _git_describe
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_diff():


```bash
function _git_diff() {
	__git_has_doubledash && return

	case "$cur" in
	--diff-algorithm=*)
		__gitcomp "$__git_diff_algorithms" "" "${cur##--diff-algorithm=}"
		return
		;;
	--submodule=*)
		__gitcomp "$__git_diff_submodule_formats" "" "${cur##--submodule=}"
		return
		;;
	--*)
		__gitcomp "--cached --staged --pickaxe-all --pickaxe-regex
			--base --ours --theirs --no-index
			$__git_diff_common_options
			"
		return
		;;
	esac
	__git_complete_revlist_file
}

__git_mergetools_common="diffuse diffmerge ecmerge emerge kdiff3 meld opendiff
			tkdiff vimdiff gvimdiff xxdiff araxis p4merge bc codecompare
"

```
##### Function Calls:


```bash
└─ _git_diff
   ├─ __gitcomp
   └─ __git_has_doubledash
```




******
### >> _git_difftool():


```bash
function _git_difftool() {
	__git_has_doubledash && return

	case "$cur" in
	--tool=*)
		__gitcomp "$__git_mergetools_common kompare" "" "${cur##--tool=}"
		return
		;;
	--*)
		__gitcomp_builtin difftool "$__git_diff_common_options
					--base --cached --ours --theirs
					--pickaxe-all --pickaxe-regex
					--relative --staged
					"
		return
		;;
	esac
	__git_complete_revlist_file
}

__git_fetch_recurse_submodules="yes on-demand no"

```
##### Function Calls:


```bash
└─ _git_difftool
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_has_doubledash
```




******
### >> _git_fetch():


```bash
function _git_fetch() {
	case "$cur" in
	--recurse-submodules=*)
		__gitcomp "$__git_fetch_recurse_submodules" "" "${cur##--recurse-submodules=}"
		return
		;;
	--*)
		__gitcomp_builtin fetch
		return
		;;
	esac
	__git_complete_remote_or_refspec
}

__git_format_patch_extra_options="
	--full-index --not --all --no-prefix --src-prefix=
	--dst-prefix= --notes
"

```
##### Function Calls:


```bash
└─ _git_fetch
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_format_patch():


```bash
function _git_format_patch() {
	case "$cur" in
	--thread=*)
		__gitcomp "
			deep shallow
			" "" "${cur##--thread=}"
		return
		;;
	--*)
		__gitcomp_builtin format-patch "$__git_format_patch_extra_options"
		return
		;;
	esac
	__git_complete_revlist
}

```
##### Function Calls:


```bash
└─ _git_format_patch
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_fsck():


```bash
function _git_fsck() {
	case "$cur" in
	--*)
		__gitcomp_builtin fsck
		return
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_fsck
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_gitk():


```bash
function _git_gitk() {
	_gitk
}

```




******
### >> __git_match_ctag():


```bash
function __git_match_ctag() {
	awk -v pfx="${3-}" -v sfx="${4-}" "
		/^${1//\//\\/}/ { print pfx \$1 sfx }
		" "$2"
}

```




******
### >> __git_complete_symbol():


```bash
function __git_complete_symbol() {
	local tags=tags pfx="" cur_="${cur-}" sfx=" "

	while test $# != 0; do
		case "$1" in
		--tags=*)	tags="${1##--tags=}" ;;
		--pfx=*)	pfx="${1##--pfx=}" ;;
		--cur=*)	cur_="${1##--cur=}" ;;
		--sfx=*)	sfx="${1##--sfx=}" ;;
		*)		return 1 ;;
		esac
		shift
	done

	if test -r "$tags"; then
		__gitcomp_direct "$(__git_match_ctag "$cur_" "$tags" "$pfx" "$sfx")"
	fi
}

```
##### Function Calls:


```bash
└─ __git_complete_symbol
   ├─ __gitcomp_direct
   └─ __git_match_ctag
```




******
### >> _git_grep():


```bash
function _git_grep() {
	__git_has_doubledash && return

	case "$cur" in
	--*)
		__gitcomp_builtin grep
		return
		;;
	esac

	case "$cword,$prev" in
	2,*|*,-*)
		__git_complete_symbol && return
		;;
	esac

	__git_complete_refs
}

```
##### Function Calls:


```bash
└─ _git_grep
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_has_doubledash
   └─ __git_complete_symbol
      ├─ __gitcomp_direct
      └─ __git_match_ctag
```




******
### >> _git_help():


```bash
function _git_help() {
	case "$cur" in
	--*)
		__gitcomp_builtin help
		return
		;;
	esac
	if test -n "$GIT_TESTING_ALL_COMMAND_LIST"
	then
		__gitcomp "$GIT_TESTING_ALL_COMMAND_LIST $(git --list-cmds=alias,list-guide) gitk"
	else
		__gitcomp "$(git --list-cmds=main,nohelpers,alias,list-guide) gitk"
	fi
}

```
##### Function Calls:


```bash
└─ _git_help
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_init():


```bash
function _git_init() {
	case "$cur" in
	--shared=*)
		__gitcomp "
			false true umask group all world everybody
			" "" "${cur##--shared=}"
		return
		;;
	--*)
		__gitcomp_builtin init
		return
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_init
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_ls_files():


```bash
function _git_ls_files() {
	case "$cur" in
	--*)
		__gitcomp_builtin ls-files
		return
		;;
	esac

	__git_complete_index_file "--cached"
}

```
##### Function Calls:


```bash
└─ _git_ls_files
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_complete_index_file
      ├─ __git_dequote
      ├─ __gitcomp_file_direct
      └─ __git_index_files
```




******
### >> _git_ls_remote():


```bash
function _git_ls_remote() {
	case "$cur" in
	--*)
		__gitcomp_builtin ls-remote
		return
		;;
	esac
	__gitcomp_nl "$(__git_remotes)"
}

_git_ls_tree() {
	case "$cur" in
	--*)
		__gitcomp_builtin ls-tree
		return
		;;
	esac

	__git_complete_file
}

__git_log_common_options="
	--not --all
	--branches --tags --remotes
	--first-parent --merges --no-merges
	--max-count=
	--max-age= --since= --after=
	--min-age= --until= --before=
	--min-parents= --max-parents=
	--no-min-parents --no-max-parents
"
__git_log_gitk_options="
	--dense --sparse --full-history
	--simplify-merges --simplify-by-decoration
	--left-right --notes --no-notes
"
__git_log_shortlog_options="
	--author= --committer= --grep=
	--all-match --invert-grep
"

__git_log_pretty_formats="oneline short medium full fuller email raw format:"
__git_log_date_formats="relative iso8601 rfc2822 short local default raw"

```
##### Function Calls:


```bash
└─ _git_ls_remote
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   └─ __git_remotes
      ├─ __git
      └─ _git
```




******
### >> _git_log():


```bash
function _git_log() {
	__git_has_doubledash && return
	__git_find_repo_path

	local merge=""
	if [ -f "$__git_repo_path/MERGE_HEAD" ]; then
		merge="--merge"
	fi
	case "$prev,$cur" in
	-L,:*:*)
		return	# fall back to Bash filename completion
		;;
	-L,:*)
		__git_complete_symbol --cur="${cur#:}" --sfx=":"
		return
		;;
	-G,*|-S,*)
		__git_complete_symbol
		return
		;;
	esac
	case "$cur" in
	--pretty=*|--format=*)
		__gitcomp "$__git_log_pretty_formats $(__git_pretty_aliases)
			" "" "${cur#*=}"
		return
		;;
	--date=*)
		__gitcomp "$__git_log_date_formats" "" "${cur##--date=}"
		return
		;;
	--decorate=*)
		__gitcomp "full short no" "" "${cur##--decorate=}"
		return
		;;
	--diff-algorithm=*)
		__gitcomp "$__git_diff_algorithms" "" "${cur##--diff-algorithm=}"
		return
		;;
	--submodule=*)
		__gitcomp "$__git_diff_submodule_formats" "" "${cur##--submodule=}"
		return
		;;
	--*)
		__gitcomp "
			$__git_log_common_options
			$__git_log_shortlog_options
			$__git_log_gitk_options
			--root --topo-order --date-order --reverse
			--follow --full-diff
			--abbrev-commit --abbrev=
			--relative-date --date=
			--pretty= --format= --oneline
			--show-signature
			--cherry-mark
			--cherry-pick
			--graph
			--decorate --decorate=
			--walk-reflogs
			--parents --children
			$merge
			$__git_diff_common_options
			--pickaxe-all --pickaxe-regex
			"
		return
		;;
	-L:*:*)
		return	# fall back to Bash filename completion
		;;
	-L:*)
		__git_complete_symbol --cur="${cur#-L:}" --sfx=":"
		return
		;;
	-G*)
		__git_complete_symbol --pfx="-G" --cur="${cur#-G}"
		return
		;;
	-S*)
		__git_complete_symbol --pfx="-S" --cur="${cur#-S}"
		return
		;;
	esac
	__git_complete_revlist
}

```
##### Function Calls:


```bash
└─ _git_log
   ├─ __gitcomp
   ├─ __git_pretty_aliases
   |  └─ __git_get_config_variables
   ├─ __git_has_doubledash
   └─ __git_complete_symbol
      ├─ __gitcomp_direct
      └─ __git_match_ctag
```




******
### >> _git_merge():


```bash
function _git_merge() {
	__git_complete_strategy && return

	case "$cur" in
	--*)
		__gitcomp_builtin merge
		return
	esac
	__git_complete_refs
}

```
##### Function Calls:


```bash
└─ _git_merge
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_complete_strategy
      └─ __gitcomp
```




******
### >> _git_mergetool():


```bash
function _git_mergetool() {
	case "$cur" in
	--tool=*)
		__gitcomp "$__git_mergetools_common tortoisemerge" "" "${cur##--tool=}"
		return
		;;
	--*)
		__gitcomp "--tool= --prompt --no-prompt --gui --no-gui"
		return
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_mergetool
   └─ __gitcomp
```




******
### >> _git_merge_base():


```bash
function _git_merge_base() {
	case "$cur" in
	--*)
		__gitcomp_builtin merge-base
		return
		;;
	esac
	__git_complete_refs
}

```
##### Function Calls:


```bash
└─ _git_merge_base
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_mv():


```bash
function _git_mv() {
	case "$cur" in
	--*)
		__gitcomp_builtin mv
		return
		;;
	esac

	if [ $(__git_count_arguments "mv") -gt 0 ]; then
		__git_complete_index_file "--cached --others --directory"
	else
		__git_complete_index_file "--cached"
	fi
}

```
##### Function Calls:


```bash
└─ _git_mv
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_complete_index_file
   |  ├─ __git_dequote
   |  ├─ __gitcomp_file_direct
   |  └─ __git_index_files
   └─ __git_count_arguments
```




******
### >> _git_notes():


```bash
function _git_notes() {
	local subcommands='add append copy edit get-ref list merge prune remove show'
	local subcommand="$(__git_find_on_cmdline "$subcommands")"

	case "$subcommand,$cur" in
	,--*)
		__gitcomp_builtin notes
		;;
	,*)
		case "$prev" in
		--ref)
			__git_complete_refs
			;;
		*)
			__gitcomp "$subcommands --ref"
			;;
		esac
		;;
	*,--reuse-message=*|*,--reedit-message=*)
		__git_complete_refs --cur="${cur#*=}"
		;;
	*,--*)
		__gitcomp_builtin notes_$subcommand
		;;
	prune,*|get-ref,*)
		;;
	*)
		case "$prev" in
		-m|-F)
			;;
		*)
			__git_complete_refs
			;;
		esac
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_notes
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_complete_refs
   |  ├─ __gitcomp_direct
   |  └─ __git_refs
   └─ __git_find_on_cmdline
```




******
### >> _git_pull():


```bash
function _git_pull() {
	__git_complete_strategy && return

	case "$cur" in
	--recurse-submodules=*)
		__gitcomp "$__git_fetch_recurse_submodules" "" "${cur##--recurse-submodules=}"
		return
		;;
	--*)
		__gitcomp_builtin pull

		return
		;;
	esac
	__git_complete_remote_or_refspec
}

__git_push_recurse_submodules="check on-demand only"

```
##### Function Calls:


```bash
└─ _git_pull
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_complete_strategy
      └─ __gitcomp
```




******
### >> __git_complete_force_with_lease():


```bash
function __git_complete_force_with_lease() {
	local cur_=$1

	case "$cur_" in
	--*=)
		;;
	*:*)
		__git_complete_refs --cur="${cur_#*:}"
		;;
	*)
		__git_complete_refs --cur="$cur_"
		;;
	esac
}

```
##### Function Calls:


```bash
└─ __git_complete_force_with_lease
   └─ __git_complete_refs
      ├─ __gitcomp_direct
      └─ __git_refs
```




******
### >> _git_push():


```bash
function _git_push() {
	case "$prev" in
	--repo)
		__gitcomp_nl "$(__git_remotes)"
		return
		;;
	--recurse-submodules)
		__gitcomp "$__git_push_recurse_submodules"
		return
		;;
	esac
	case "$cur" in
	--repo=*)
		__gitcomp_nl "$(__git_remotes)" "" "${cur##--repo=}"
		return
		;;
	--recurse-submodules=*)
		__gitcomp "$__git_push_recurse_submodules" "" "${cur##--recurse-submodules=}"
		return
		;;
	--force-with-lease=*)
		__git_complete_force_with_lease "${cur##--force-with-lease=}"
		return
		;;
	--*)
		__gitcomp_builtin push
		return
		;;
	esac
	__git_complete_remote_or_refspec
}

```
##### Function Calls:


```bash
└─ _git_push
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   ├─ __git_remotes
   |  ├─ __git
   |  └─ _git
   └─ __git_complete_force_with_lease
      └─ __git_complete_refs
```




******
### >> _git_range_diff():


```bash
function _git_range_diff() {
	case "$cur" in
	--*)
		__gitcomp "
			--creation-factor= --no-dual-color
			$__git_diff_common_options
		"
		return
		;;
	esac
	__git_complete_revlist
}

```
##### Function Calls:


```bash
└─ _git_range_diff
   └─ __gitcomp
```




******
### >> _git_rebase():


```bash
function _git_rebase() {
	__git_find_repo_path
	if [ -f "$__git_repo_path"/rebase-merge/interactive ]; then
		__gitcomp "--continue --skip --abort --quit --edit-todo --show-current-patch"
		return
	elif [ -d "$__git_repo_path"/rebase-apply ] || \
	     [ -d "$__git_repo_path"/rebase-merge ]; then
		__gitcomp "--continue --skip --abort --quit --show-current-patch"
		return
	fi
	__git_complete_strategy && return
	case "$cur" in
	--whitespace=*)
		__gitcomp "$__git_whitespacelist" "" "${cur##--whitespace=}"
		return
		;;
	--*)
		__gitcomp "
			--onto --merge --strategy --interactive
			--rebase-merges --preserve-merges --stat --no-stat
			--committer-date-is-author-date --ignore-date
			--ignore-whitespace --whitespace=
			--autosquash --no-autosquash
			--fork-point --no-fork-point
			--autostash --no-autostash
			--verify --no-verify
			--keep-empty --root --force-rebase --no-ff
			--rerere-autoupdate
			--exec
			"

		return
	esac
	__git_complete_refs
}

```
##### Function Calls:


```bash
└─ _git_rebase
   ├─ __gitcomp
   └─ __git_complete_strategy
      └─ __gitcomp
```




******
### >> _git_reflog():


```bash
function _git_reflog() {
	local subcommands="show delete expire"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"

	if [ -z "$subcommand" ]; then
		__gitcomp "$subcommands"
	else
		__git_complete_refs
	fi
}

__git_send_email_confirm_options="always never auto cc compose"
__git_send_email_suppresscc_options="author self cc bodycc sob cccmd body all"

```
##### Function Calls:


```bash
└─ _git_reflog
   ├─ __gitcomp
   └─ __git_find_on_cmdline
```




******
### >> _git_send_email():


```bash
function _git_send_email () {
	case "$prev" in
	--to|--cc|--bcc|--from)
		__gitcomp "$(__git send-email --dump-aliases)"
		return
		;;
	esac

	case "$cur" in
	--confirm=*)
		__gitcomp "
			$__git_send_email_confirm_options
			" "" "${cur##--confirm=}"
		return
		;;
	--suppress-cc=*)
		__gitcomp "
			$__git_send_email_suppresscc_options
			" "" "${cur##--suppress-cc=}"

		return
		;;
	--smtp-encryption=*)
		__gitcomp "ssl tls" "" "${cur##--smtp-encryption=}"
		return
		;;
	--thread=*)
		__gitcomp "
			deep shallow
			" "" "${cur##--thread=}"
		return
		;;
	--to=*|--cc=*|--bcc=*|--from=*)
		__gitcomp "$(__git send-email --dump-aliases)" "" "${cur#--*=}"
		return
		;;
	--*)
		__gitcomp_builtin send-email "--annotate --bcc --cc --cc-cmd --chain-reply-to
			--compose --confirm= --dry-run --envelope-sender
			--from --identity
			--in-reply-to --no-chain-reply-to --no-signed-off-by-cc
			--no-suppress-from --no-thread --quiet --reply-to
			--signed-off-by-cc --smtp-pass --smtp-server
			--smtp-server-port --smtp-encryption= --smtp-user
			--subject --suppress-cc= --suppress-from --thread --to
			--validate --no-validate
			$__git_format_patch_extra_options"
		return
		;;
	esac
	__git_complete_revlist
}

```
##### Function Calls:


```bash
└─ _git_send_email
   ├─ __git
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ _git
```




******
### >> _git_stage():


```bash
function _git_stage() {
	_git_add
}

```




******
### >> _git_status():


```bash
function _git_status() {
	local complete_opt
	local untracked_state

	case "$cur" in
	--ignore-submodules=*)
		__gitcomp "none untracked dirty all" "" "${cur##--ignore-submodules=}"
		return
		;;
	--untracked-files=*)
		__gitcomp "$__git_untracked_file_modes" "" "${cur##--untracked-files=}"
		return
		;;
	--column=*)
		__gitcomp "
			always never auto column row plain dense nodense
			" "" "${cur##--column=}"
		return
		;;
	--*)
		__gitcomp_builtin status
		return
		;;
	esac

	untracked_state="$(__git_get_option_value "-u" "--untracked-files=" \
		"$__git_untracked_file_modes" "status.showUntrackedFiles")"

	case "$untracked_state" in
	no)
		complete_opt=
		;;
	all|normal|*)
		complete_opt="--cached --directory --no-empty-directory --others"

		if [ -n "$(__git_find_on_cmdline "--ignored")" ]; then
			complete_opt="$complete_opt --ignored --exclude=*"
		fi
		;;
	esac

	__git_complete_index_file "$complete_opt"
}

```
##### Function Calls:


```bash
└─ _git_status
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __git_complete_index_file
   |  ├─ __git_dequote
   |  ├─ __gitcomp_file_direct
   |  └─ __git_index_files
   ├─ __git_find_on_cmdline
   └─ __git_get_option_value
      ├─ __git
      └─ _git
```




******
### >> __git_config_get_set_variables():


```bash
function __git_config_get_set_variables() {
	local prevword word config_file= c=$cword
	while [ $c -gt 1 ]; do
		word="${words[c]}"
		case "$word" in
		--system|--global|--local|--file=*)
			config_file="$word"
			break
			;;
		-f|--file)
			config_file="$word $prevword"
			break
			;;
		esac
		prevword=$word
		c=$((--c))
	done

	__git config $config_file --name-only --list
}

__git_config_vars=

```
##### Function Calls:


```bash
└─ __git_config_get_set_variables
   ├─ __git
   └─ _git
```




******
### >> __git_compute_config_vars():


```bash
function __git_compute_config_vars() {
	test -n "$__git_config_vars" ||
	__git_config_vars="$(git help --config-for-completion | sort | uniq)"
}

```




******
### >> _git_config():


```bash
function _git_config() {
	local varname

	if [ "${BASH_VERSINFO[0]:-0}" -ge 4 ]; then
		varname="${prev,,}"
	else
		varname="$(echo "$prev" |tr A-Z a-z)"
	fi

	case "$varname" in
	branch.*.remote|branch.*.pushremote)
		__gitcomp_nl "$(__git_remotes)"
		return
		;;
	branch.*.merge)
		__git_complete_refs
		return
		;;
	branch.*.rebase)
		__gitcomp "false true merges preserve interactive"
		return
		;;
	remote.pushdefault)
		__gitcomp_nl "$(__git_remotes)"
		return
		;;
	remote.*.fetch)
		local remote="${prev#remote.}"
		remote="${remote%.fetch}"
		if [ -z "$cur" ]; then
			__gitcomp_nl "refs/heads/" "" "" ""
			return
		fi
		__gitcomp_nl "$(__git_refs_remotes "$remote")"
		return
		;;
	remote.*.push)
		local remote="${prev#remote.}"
		remote="${remote%.push}"
		__gitcomp_nl "$(__git for-each-ref \
			--format='%(refname):%(refname)' refs/heads)"
		return
		;;
	pull.twohead|pull.octopus)
		__git_compute_merge_strategies
		__gitcomp "$__git_merge_strategies"
		return
		;;
	color.branch|color.diff|color.interactive|\
	color.showbranch|color.status|color.ui)
		__gitcomp "always never auto"
		return
		;;
	color.pager)
		__gitcomp "false true"
		return
		;;
	color.*.*)
		__gitcomp "
			normal black red green yellow blue magenta cyan white
			bold dim ul blink reverse
			"
		return
		;;
	diff.submodule)
		__gitcomp "log short"
		return
		;;
	help.format)
		__gitcomp "man info web html"
		return
		;;
	log.date)
		__gitcomp "$__git_log_date_formats"
		return
		;;
	sendemail.aliasfiletype)
		__gitcomp "mutt mailrc pine elm gnus"
		return
		;;
	sendemail.confirm)
		__gitcomp "$__git_send_email_confirm_options"
		return
		;;
	sendemail.suppresscc)
		__gitcomp "$__git_send_email_suppresscc_options"
		return
		;;
	sendemail.transferencoding)
		__gitcomp "7bit 8bit quoted-printable base64"
		return
		;;
	--get|--get-all|--unset|--unset-all)
		__gitcomp_nl "$(__git_config_get_set_variables)"
		return
		;;
	*.*)
		return
		;;
	esac
	case "$cur" in
	--*)
		__gitcomp_builtin config
		return
		;;
	branch.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "remote pushRemote merge mergeOptions rebase" "$pfx" "$cur_"
		return
		;;
	branch.*)
		local pfx="${cur%.*}." cur_="${cur#*.}"
		__gitcomp_direct "$(__git_heads "$pfx" "$cur_" ".")"
		__gitcomp_nl_append $'autoSetupMerge\nautoSetupRebase\n' "$pfx" "$cur_"
		return
		;;
	guitool.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "
			argPrompt cmd confirm needsFile noConsole noRescan
			prompt revPrompt revUnmerged title
			" "$pfx" "$cur_"
		return
		;;
	difftool.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "cmd path" "$pfx" "$cur_"
		return
		;;
	man.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "cmd path" "$pfx" "$cur_"
		return
		;;
	mergetool.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "cmd path trustExitCode" "$pfx" "$cur_"
		return
		;;
	pager.*)
		local pfx="${cur%.*}." cur_="${cur#*.}"
		__git_compute_all_commands
		__gitcomp_nl "$__git_all_commands" "$pfx" "$cur_"
		return
		;;
	remote.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "
			url proxy fetch push mirror skipDefaultUpdate
			receivepack uploadpack tagOpt pushurl
			" "$pfx" "$cur_"
		return
		;;
	remote.*)
		local pfx="${cur%.*}." cur_="${cur#*.}"
		__gitcomp_nl "$(__git_remotes)" "$pfx" "$cur_" "."
		__gitcomp_nl_append "pushDefault" "$pfx" "$cur_"
		return
		;;
	url.*.*)
		local pfx="${cur%.*}." cur_="${cur##*.}"
		__gitcomp "insteadOf pushInsteadOf" "$pfx" "$cur_"
		return
		;;
	*.*)
		__git_compute_config_vars
		__gitcomp "$__git_config_vars"
		;;
	*)
		__git_compute_config_vars
		__gitcomp "$(echo "$__git_config_vars" | sed 's/\.[^ ]*/./g')"
	esac
}

```
##### Function Calls:


```bash
└─ _git_config
   ├─ __git
   ├─ __gitcomp_direct
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __gitcomp_nl_append
   |  └─ __gitcompappend
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   ├─ __git_heads
   |  ├─ __git
   |  └─ _git
   ├─ __git_refs_remotes
   |  ├─ __git
   |  └─ _git
   ├─ __git_remotes
   |  ├─ __git
   |  └─ _git
   ├─ __git_config_get_set_variables
   |  ├─ __git
   |  └─ _git
   └─ _git
```




******
### >> _git_remote():


```bash
function _git_remote() {
	local subcommands="
		add rename remove set-head set-branches
		get-url set-url show prune update
		"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"
	if [ -z "$subcommand" ]; then
		case "$cur" in
		--*)
			__gitcomp_builtin remote
			;;
		*)
			__gitcomp "$subcommands"
			;;
		esac
		return
	fi

	case "$subcommand,$cur" in
	add,--*)
		__gitcomp_builtin remote_add
		;;
	add,*)
		;;
	set-head,--*)
		__gitcomp_builtin remote_set-head
		;;
	set-branches,--*)
		__gitcomp_builtin remote_set-branches
		;;
	set-head,*|set-branches,*)
		__git_complete_remote_or_refspec
		;;
	update,--*)
		__gitcomp_builtin remote_update
		;;
	update,*)
		__gitcomp "$(__git_remotes) $(__git_get_config_variables "remotes")"
		;;
	set-url,--*)
		__gitcomp_builtin remote_set-url
		;;
	get-url,--*)
		__gitcomp_builtin remote_get-url
		;;
	prune,--*)
		__gitcomp_builtin remote_prune
		;;
	*)
		__gitcomp_nl "$(__git_remotes)"
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_remote
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   ├─ __git_remotes
   |  ├─ __git
   |  └─ _git
   ├─ __git_get_config_variables
   |  ├─ __git
   |  └─ _git
   └─ __git_find_on_cmdline
```




******
### >> _git_replace():


```bash
function _git_replace() {
	case "$cur" in
	--*)
		__gitcomp_builtin replace
		return
		;;
	esac
	__git_complete_refs
}

```
##### Function Calls:


```bash
└─ _git_replace
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_rerere():


```bash
function _git_rerere() {
	local subcommands="clear forget diff remaining status gc"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"
	if test -z "$subcommand"
	then
		__gitcomp "$subcommands"
		return
	fi
}

```
##### Function Calls:


```bash
└─ _git_rerere
   ├─ __gitcomp
   └─ __git_find_on_cmdline
```




******
### >> _git_reset():


```bash
function _git_reset() {
	__git_has_doubledash && return

	case "$cur" in
	--*)
		__gitcomp_builtin reset
		return
		;;
	esac
	__git_complete_refs
}

__git_revert_inprogress_options="--continue --quit --abort"

```
##### Function Calls:


```bash
└─ _git_reset
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_has_doubledash
```




******
### >> _git_revert():


```bash
function _git_revert() {
	__git_find_repo_path
	if [ -f "$__git_repo_path"/REVERT_HEAD ]; then
		__gitcomp "$__git_revert_inprogress_options"
		return
	fi
	case "$cur" in
	--*)
		__gitcomp_builtin revert "" \
			"$__git_revert_inprogress_options"
		return
		;;
	esac
	__git_complete_refs
}

```
##### Function Calls:


```bash
└─ _git_revert
   ├─ __gitcomp
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_rm():


```bash
function _git_rm() {
	case "$cur" in
	--*)
		__gitcomp_builtin rm
		return
		;;
	esac

	__git_complete_index_file "--cached"
}

```
##### Function Calls:


```bash
└─ _git_rm
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_complete_index_file
      ├─ __git_dequote
      ├─ __gitcomp_file_direct
      └─ __git_index_files
```




******
### >> _git_shortlog():


```bash
function _git_shortlog() {
	__git_has_doubledash && return

	case "$cur" in
	--*)
		__gitcomp "
			$__git_log_common_options
			$__git_log_shortlog_options
			--numbered --summary --email
			"
		return
		;;
	esac
	__git_complete_revlist
}

```
##### Function Calls:


```bash
└─ _git_shortlog
   ├─ __gitcomp
   └─ __git_has_doubledash
```




******
### >> _git_show():


```bash
function _git_show() {
	__git_has_doubledash && return

	case "$cur" in
	--pretty=*|--format=*)
		__gitcomp "$__git_log_pretty_formats $(__git_pretty_aliases)
			" "" "${cur#*=}"
		return
		;;
	--diff-algorithm=*)
		__gitcomp "$__git_diff_algorithms" "" "${cur##--diff-algorithm=}"
		return
		;;
	--submodule=*)
		__gitcomp "$__git_diff_submodule_formats" "" "${cur##--submodule=}"
		return
		;;
	--*)
		__gitcomp "--pretty= --format= --abbrev-commit --oneline
			--show-signature
			$__git_diff_common_options
			"
		return
		;;
	esac
	__git_complete_revlist_file
}

```
##### Function Calls:


```bash
└─ _git_show
   ├─ __gitcomp
   ├─ __git_pretty_aliases
   |  └─ __git_get_config_variables
   └─ __git_has_doubledash
```




******
### >> _git_show_branch():


```bash
function _git_show_branch() {
	case "$cur" in
	--*)
		__gitcomp_builtin show-branch
		return
		;;
	esac
	__git_complete_revlist
}

```
##### Function Calls:


```bash
└─ _git_show_branch
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> _git_stash():


```bash
function _git_stash() {
	local save_opts='--all --keep-index --no-keep-index --quiet --patch --include-untracked'
	local subcommands='push list show apply clear drop pop create branch'
	local subcommand="$(__git_find_on_cmdline "$subcommands save")"
	if [ -n "$(__git_find_on_cmdline "-p")" ]; then
		subcommand="push"
	fi
	if [ -z "$subcommand" ]; then
		case "$cur" in
		--*)
			__gitcomp "$save_opts"
			;;
		sa*)
			if [ -z "$(__git_find_on_cmdline "$save_opts")" ]; then
				__gitcomp "save"
			fi
			;;
		*)
			if [ -z "$(__git_find_on_cmdline "$save_opts")" ]; then
				__gitcomp "$subcommands"
			fi
			;;
		esac
	else
		case "$subcommand,$cur" in
		push,--*)
			__gitcomp "$save_opts --message"
			;;
		save,--*)
			__gitcomp "$save_opts"
			;;
		apply,--*|pop,--*)
			__gitcomp "--index --quiet"
			;;
		drop,--*)
			__gitcomp "--quiet"
			;;
		list,--*)
			__gitcomp "--name-status --oneline --patch-with-stat"
			;;
		show,--*|branch,--*)
			;;
		branch,*)
			if [ $cword -eq 3 ]; then
				__git_complete_refs
			else
				__gitcomp_nl "$(__git stash list \
						| sed -n -e 's/:.*//p')"
			fi
			;;
		show,*|apply,*|drop,*|pop,*)
			__gitcomp_nl "$(__git stash list \
					| sed -n -e 's/:.*//p')"
			;;
		*)
			;;
		esac
	fi
}

```
##### Function Calls:


```bash
└─ _git_stash
   ├─ __git
   ├─ __gitcomp
   ├─ __gitcomp_nl
   |  └─ __gitcomp_nl_append
   ├─ __git_find_on_cmdline
   └─ _git
```




******
### >> _git_submodule():


```bash
function _git_submodule() {
	__git_has_doubledash && return

	local subcommands="add status init deinit update summary foreach sync"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"
	if [ -z "$subcommand" ]; then
		case "$cur" in
		--*)
			__gitcomp "--quiet"
			;;
		*)
			__gitcomp "$subcommands"
			;;
		esac
		return
	fi

	case "$subcommand,$cur" in
	add,--*)
		__gitcomp "--branch --force --name --reference --depth"
		;;
	status,--*)
		__gitcomp "--cached --recursive"
		;;
	deinit,--*)
		__gitcomp "--force --all"
		;;
	update,--*)
		__gitcomp "
			--init --remote --no-fetch
			--recommend-shallow --no-recommend-shallow
			--force --rebase --merge --reference --depth --recursive --jobs
		"
		;;
	summary,--*)
		__gitcomp "--cached --files --summary-limit"
		;;
	foreach,--*|sync,--*)
		__gitcomp "--recursive"
		;;
	*)
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_submodule
   ├─ __gitcomp
   ├─ __git_find_on_cmdline
   └─ __git_has_doubledash
```




******
### >> _git_svn():


```bash
function _git_svn() {
	local subcommands="
		init fetch clone rebase dcommit log find-rev
		set-tree commit-diff info create-ignore propget
		proplist show-ignore show-externals branch tag blame
		migrate mkdirs reset gc
		"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"
	if [ -z "$subcommand" ]; then
		__gitcomp "$subcommands"
	else
		local remote_opts="--username= --config-dir= --no-auth-cache"
		local fc_opts="
			--follow-parent --authors-file= --repack=
			--no-metadata --use-svm-props --use-svnsync-props
			--log-window-size= --no-checkout --quiet
			--repack-flags --use-log-author --localtime
			--add-author-from
			--ignore-paths= --include-paths= $remote_opts
			"
		local init_opts="
			--template= --shared= --trunk= --tags=
			--branches= --stdlayout --minimize-url
			--no-metadata --use-svm-props --use-svnsync-props
			--rewrite-root= --prefix= $remote_opts
			"
		local cmt_opts="
			--edit --rmdir --find-copies-harder --copy-similarity=
			"

		case "$subcommand,$cur" in
		fetch,--*)
			__gitcomp "--revision= --fetch-all $fc_opts"
			;;
		clone,--*)
			__gitcomp "--revision= $fc_opts $init_opts"
			;;
		init,--*)
			__gitcomp "$init_opts"
			;;
		dcommit,--*)
			__gitcomp "
				--merge --strategy= --verbose --dry-run
				--fetch-all --no-rebase --commit-url
				--revision --interactive $cmt_opts $fc_opts
				"
			;;
		set-tree,--*)
			__gitcomp "--stdin $cmt_opts $fc_opts"
			;;
		create-ignore,--*|propget,--*|proplist,--*|show-ignore,--*|\
		show-externals,--*|mkdirs,--*)
			__gitcomp "--revision="
			;;
		log,--*)
			__gitcomp "
				--limit= --revision= --verbose --incremental
				--oneline --show-commit --non-recursive
				--authors-file= --color
				"
			;;
		rebase,--*)
			__gitcomp "
				--merge --verbose --strategy= --local
				--fetch-all --dry-run $fc_opts
				"
			;;
		commit-diff,--*)
			__gitcomp "--message= --file= --revision= $cmt_opts"
			;;
		info,--*)
			__gitcomp "--url"
			;;
		branch,--*)
			__gitcomp "--dry-run --message --tag"
			;;
		tag,--*)
			__gitcomp "--dry-run --message"
			;;
		blame,--*)
			__gitcomp "--git-format"
			;;
		migrate,--*)
			__gitcomp "
				--config-dir= --ignore-paths= --minimize
				--no-auth-cache --username=
				"
			;;
		reset,--*)
			__gitcomp "--revision= --parent"
			;;
		*)
			;;
		esac
	fi
}

```
##### Function Calls:


```bash
└─ _git_svn
   ├─ __gitcomp
   └─ __git_find_on_cmdline
```




******
### >> _git_tag():


```bash
function _git_tag() {
	local i c=1 f=0
	while [ $c -lt $cword ]; do
		i="${words[c]}"
		case "$i" in
		-d|--delete|-v|--verify)
			__gitcomp_direct "$(__git_tags "" "$cur" " ")"
			return
			;;
		-f)
			f=1
			;;
		esac
		((c++))
	done

	case "$prev" in
	-m|-F)
		;;
	-*|tag)
		if [ $f = 1 ]; then
			__gitcomp_direct "$(__git_tags "" "$cur" " ")"
		fi
		;;
	*)
		__git_complete_refs
		;;
	esac

	case "$cur" in
	--*)
		__gitcomp_builtin tag
		;;
	esac
}

```
##### Function Calls:


```bash
└─ _git_tag
   ├─ __gitcomp_direct
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_tags
      ├─ __git
      └─ _git
```




******
### >> _git_whatchanged():


```bash
function _git_whatchanged() {
	_git_log
}

```




******
### >> _git_worktree():


```bash
function _git_worktree() {
	local subcommands="add list lock move prune remove unlock"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"
	if [ -z "$subcommand" ]; then
		__gitcomp "$subcommands"
	else
		case "$subcommand,$cur" in
		add,--*)
			__gitcomp_builtin worktree_add
			;;
		list,--*)
			__gitcomp_builtin worktree_list
			;;
		lock,--*)
			__gitcomp_builtin worktree_lock
			;;
		prune,--*)
			__gitcomp_builtin worktree_prune
			;;
		remove,--*)
			__gitcomp "--force"
			;;
		*)
			;;
		esac
	fi
}

```
##### Function Calls:


```bash
└─ _git_worktree
   ├─ __gitcomp
   ├─ __gitcomp_builtin
   |  ├─ __git
   |  ├─ __gitcomp
   |  └─ _git
   └─ __git_find_on_cmdline
```




******
### >> __git_complete_common():


```bash
function __git_complete_common() {
	local command="$1"

	case "$cur" in
	--*)
		__gitcomp_builtin "$command"
		;;
	esac
}

__git_cmds_with_parseopt_helper=

```
##### Function Calls:


```bash
└─ __git_complete_common
   └─ __gitcomp_builtin
      ├─ __git
      ├─ __gitcomp
      └─ _git
```




******
### >> __git_support_parseopt_helper():


```bash
function __git_support_parseopt_helper() {
	test -n "$__git_cmds_with_parseopt_helper" ||
		__git_cmds_with_parseopt_helper="$(__git --list-cmds=parseopt)"

	case " $__git_cmds_with_parseopt_helper " in
	*" $1 "*)
		return 0
		;;
	*)
		return 1
		;;
	esac
}

```
##### Function Calls:


```bash
└─ __git_support_parseopt_helper
   ├─ __git
   └─ _git
```




******
### >> __git_complete_command():


```bash
function __git_complete_command() {
	local command="$1"
	local completion_func="_git_${command//-/_}"
	if ! declare -f $completion_func >/dev/null 2>/dev/null &&
		declare -f _completion_loader >/dev/null 2>/dev/null
	then
		_completion_loader "git-$command"
	fi
	if declare -f $completion_func >/dev/null 2>/dev/null
	then
		$completion_func
		return 0
	elif __git_support_parseopt_helper "$command"
	then
		__git_complete_common "$command"
		return 0
	else
		return 1
	fi
}

```
##### Function Calls:


```bash
└─ __git_complete_command
   ├─ __git_complete_common
   |  └─ __gitcomp_builtin
   └─ __git_support_parseopt_helper
      ├─ __git
      └─ _git
```




******
### >> __git_main():


```bash
function __git_main() {
	local i c=1 command __git_dir __git_repo_path
	local __git_C_args C_args_count=0

	while [ $c -lt $cword ]; do
		i="${words[c]}"
		case "$i" in
		--git-dir=*) __git_dir="${i#--git-dir=}" ;;
		--git-dir)   ((c++)) ; __git_dir="${words[c]}" ;;
		--bare)      __git_dir="." ;;
		--help) command="help"; break ;;
		-c|--work-tree|--namespace) ((c++)) ;;
		-C)	__git_C_args[C_args_count++]=-C
			((c++))
			__git_C_args[C_args_count++]="${words[c]}"
			;;
		-*) ;;
		*) command="$i"; break ;;
		esac
		((c++))
	done

	if [ -z "$command" ]; then
		case "$prev" in
		--git-dir|-C|--work-tree)
			return
			;;
		-c|--namespace)
			return
			;;
		esac
		case "$cur" in
		--*)   __gitcomp "
			--paginate
			--no-pager
			--git-dir=
			--bare
			--version
			--exec-path
			--exec-path=
			--html-path
			--man-path
			--info-path
			--work-tree=
			--namespace=
			--no-replace-objects
			--help
			"
			;;
		*)
			if test -n "$GIT_TESTING_PORCELAIN_COMMAND_LIST"
			then
				__gitcomp "$GIT_TESTING_PORCELAIN_COMMAND_LIST"
			else
				__gitcomp "$(git --list-cmds=list-mainporcelain,others,nohelpers,alias,list-complete,config)"
			fi
			;;
		esac
		return
	fi

	__git_complete_command "$command" && return

	local expansion=$(__git_aliased_command "$command")
	if [ -n "$expansion" ]; then
		words[1]=$expansion
		__git_complete_command "$expansion"
	fi
}

```
##### Function Calls:


```bash
└─ __git_main
   ├─ __gitcomp
   ├─ __git_aliased_command
   |  ├─ __git
   |  └─ _git
   └─ __git_complete_command
      ├─ __git_complete_common
      └─ __git_support_parseopt_helper
```




******
### >> __gitk_main():


```bash
function __gitk_main() {
	__git_has_doubledash && return

	local __git_repo_path
	__git_find_repo_path

	local merge=""
	if [ -f "$__git_repo_path/MERGE_HEAD" ]; then
		merge="--merge"
	fi
	case "$cur" in
	--*)
		__gitcomp "
			$__git_log_common_options
			$__git_log_gitk_options
			$merge
			"
		return
		;;
	esac
	__git_complete_revlist
}

if [[ -n ${ZSH_VERSION-} ]] &&
   [[ -z ${GIT_SOURCING_ZSH_COMPLETION-} ]]; then
	echo "WARNING: this script is deprecated, please see git-completion.zsh" 1>&2

	autoload -U +X compinit && compinit

	__gitcomp ()
	{
		emulate -L zsh

		local cur_="${3-$cur}"

		case "$cur_" in
		--*=)
			;;
		*)
			local c IFS=$' \t\n'
			local -a array
			for c in ${=1}; do
				c="$c${4-}"
				case $c in
				--*=*|*.) ;;
				*) c="$c " ;;
				esac
				array[${#array[@]}+1]="$c"
			done
			compset -P '*[=:]'
			compadd -Q -S '' -p "${2-}" -a -- array && _ret=0
			;;
		esac
	}

	__gitcomp_direct() {
		emulate -L zsh

		local IFS=$'\n'
		compset -P '*[=:]'
		compadd -Q -- ${=1} && _ret=0
	}

	__gitcomp_nl() {
		emulate -L zsh

		local IFS=$'\n'
		compset -P '*[=:]'
		compadd -Q -S "${4- }" -p "${2-}" -- ${=1} && _ret=0
	}

	__gitcomp_file_direct() {
		emulate -L zsh

		local IFS=$'\n'
		compset -P '*[=:]'
		compadd -f -- ${=1} && _ret=0
	}

	__gitcomp_file() {
		emulate -L zsh

		local IFS=$'\n'
		compset -P '*[=:]'
		compadd -p "${2-}" -f -- ${=1} && _ret=0
	}

	_git() {
		local _ret=1 cur cword prev
		cur=${words[CURRENT]}
		prev=${words[CURRENT-1]}
		let cword=CURRENT-1
		emulate ksh -c __${service}_main
		let _ret && _default && _ret=0
		return _ret
	}

	compdef _git git gitk
	return
fi

```
##### Function Calls:


```bash
└─ __gitk_main
   ├─ __gitcomp
   ├─ __git_has_doubledash
   └─ _git
```




******
### >> __git_func_wrap():


```bash
function __git_func_wrap() {
	local cur words cword prev
	_get_comp_words_by_ref -n =: cur words cword prev
	$1
}

```




******
### >> __git_complete():


```bash
function __git_complete() {
	local wrapper="__git_wrap${2}"
	eval "$wrapper () { __git_func_wrap $2 ; }"
	complete -o bashdefault -o default -o nospace -F $wrapper $1 2>/dev/null \
		|| complete -o default -o nospace -F $wrapper $1
}

```
##### Function Calls:


```bash
└─ __git_complete
   └─ __git_func_wrap
```




******
### >> _git():


```bash
function _git () {
	__git_wrap__git_main
}

```




******
### >> _gitk():


```bash
function _gitk () {
	__git_wrap__gitk_main
}

__git_complete git __git_main
__git_complete gitk __gitk_main

if [ Cygwin = "$(uname -o 2>/dev/null)" ]; then
__git_complete git.exe __git_main
fi

```
##### Function Calls:


```bash
└─ _gitk
   └─ __git_complete
      └─ __git_func_wrap
```


