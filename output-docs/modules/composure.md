
Composure module by Erichs: light-hearted functions for intuitive shell programming
===================================================================================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/modules/composure.sh)***
## Function Index


```python
01 - _bootstrap_composure
02 - _get_composure_dir
03 - _get_author_name
04 - _composure_keywords
05 - _letterpress
06 - _determine_printf_cmd
07 - _longest_function_name_length
08 - _temp_filename_for
09 - _prompt
10 - _add_composure_file
11 - _transcribe
12 - _typeset_functions
13 - _typeset_functions_about
14 - _shell
15 - _generate_metadata_functions
16 - _list_composure_files
17 - _load_composed_functions
18 - _strip_trailing_whitespace
19 - _strip_semicolons
20 - cite
21 - draft
22 - glossary
23 - metafor
24 - reference(){
25 - revise
26 - write
```

******
### >> _bootstrap_composure():


```bash
function _bootstrap_composure() {
    _generate_metadata_functions
    _load_composed_functions
    _determine_printf_cmd
}

```




******
### >> _get_composure_dir():


```bash
function _get_composure_dir() {
    if [ -n "$XDG_DATA_HOME" ]; then
	echo "$XDG_DATA_HOME/composure"
    else
	echo "$HOME/.local/composure"
    fi
}

```




******
### >> _get_author_name():


```bash
function _get_author_name() {
    typeset name localname
    localname="$(git --git-dir "$(_get_composure_dir)/.git" config --get user.name)"
    for name in "$GIT_AUTHOR_NAME" "$localname"; do
	if [ -n "$name" ]; then
	    echo "$name"
	    break
	fi
    done
}

```
##### Function Calls:


```bash
└─ _get_author_name
   └─ _get_composure_dir
```




******
### >> _composure_keywords():


```bash
function _composure_keywords() {
    echo "about author example group param version"
}

```




******
### >> _letterpress():


```bash
function _letterpress() {
    typeset rightcol="$1" leftcol="${2:- }" leftwidth="${3:-20}"

    if [ -z "$rightcol" ]; then
	return
    fi

    $_printf_cmd "%-*s%s\n" "$leftwidth" "$leftcol" "$rightcol"
}

```




******
### >> _determine_printf_cmd():


```bash
function _determine_printf_cmd() {
    if [ -z "$_printf_cmd" ]; then
	_printf_cmd=printf
	[ -x "$(which gprintf 2>/dev/null)" ] && _printf_cmd=gprintf
	export _printf_cmd
    fi
}

```




******
### >> _longest_function_name_length():


```bash
function _longest_function_name_length() {
    echo "$1" | awk 'BEGIN{ maxlength=0 }
    {
    for(i=1;i<=NF;i++)
	if (length($i)>maxlength)
	{
	maxlength=length($i)
	}
    }
    END{ print maxlength}'
}

```




******
### >> _temp_filename_for():


```bash
function _temp_filename_for() {
    typeset file=$(mktemp "/tmp/$1.XXXX")
    command rm "$file" 2>/dev/null     # ensure file is unlinked prior to use
    echo "$file"
}

```




******
### >> _prompt():


```bash
function _prompt() {
    typeset prompt="$1"
    typeset result
    case "$(_shell)" in
	bash)
	    read -r -e -p "$prompt" result;;
	*)
	    echo -n "$prompt" >&2; read -r result;;
    esac
    echo "$result"
}

```
##### Function Calls:


```bash
└─ _prompt
   └─ _shell
```




******
### >> _add_composure_file():


```bash
function _add_composure_file() {
    typeset func="$1"
    typeset file="$2"
    typeset operation="$3"
    typeset comment="${4:-}"
    typeset composure_dir=$(_get_composure_dir)

    (
	if ! cd "$composure_dir"; then
	    printf "%s\n" "Oops! Can't find $composure_dir!"
	    return
	fi
	if git rev-parse 2>/dev/null; then
	    if [ ! -f "$file" ]; then
		printf "%s\n" "Oops! Couldn't find $file to version it for you..."
		return
	    fi
	    cp "$file" "$composure_dir/$func.inc"
	    git add --all .
	    if [ -z "$comment" ]; then
		comment="$(_prompt 'Git Comment: ')"
	    fi
	    git commit -m "$operation $func: $comment"
	fi
    )
}

```
##### Function Calls:


```bash
└─ _add_composure_file
   ├─ _get_composure_dir
   └─ _prompt
      └─ _shell
```




******
### >> _transcribe():


```bash
function _transcribe() {
    typeset func="$1"
    typeset file="$2"
    typeset operation="$3"
    typeset comment="${4:-}"
    typeset composure_dir=$(_get_composure_dir)

    if git --version >/dev/null 2>&1; then
	if [ -d "$composure_dir" ]; then
	    _add_composure_file "$func" "$file" "$operation" "$comment"
	else
	    if [ "$USE_COMPOSURE_REPO" = "0" ]; then
		return    # if you say so...
	    fi
	    printf "%s\n" "I see you don't have a $composure_dir repo..."
	    typeset input=''
	    typeset valid=0
	    while [ $valid != 1 ]; do
		printf "\n%s" 'would you like to create one? y/n: '
		read -r input
		case $input in
		    y|yes|Y|Yes|YES)
			(
			    echo 'creating git repository for your functions...'
			    mkdir -p "$composure_dir" || return 1
			    cd "$composure_dir" || return 1
			    git init
			    echo "composure stores your function definitions here" > README.txt
			    git add README.txt
			    git commit -m 'initial commit'
			)
			_transcribe "$func" "$file" "$operation" "$comment"
			valid=1
			;;
		    n|no|N|No|NO)
			printf "%s\n" "ok. add 'export USE_COMPOSURE_REPO=0' to your startup script to disable this message."
			valid=1
		    ;;
		    *)
			printf "%s\n" "sorry, didn't get that..."
		    ;;
		esac
	    done
	 fi
    fi
}

```
##### Function Calls:


```bash
└─ _transcribe
   ├─ _get_composure_dir
   └─ _add_composure_file
      ├─ _get_composure_dir
      └─ _prompt
```




******
### >> _typeset_functions():


```bash
function _typeset_functions() {

    case "$(_shell)" in
	sh|bash)
	    typeset -F | awk '{print $3}'
	    ;;
	*)
	    typeset +f | sed 's/().*$//'
	    ;;
    esac
}

```
##### Function Calls:


```bash
└─ _typeset_functions
   └─ _shell
```




******
### >> _typeset_functions_about():


```bash
function _typeset_functions_about() {
    typeset f
    for f in $(_typeset_functions); do
	typeset -f -- "$f" | grep -qE "^about[[:space:]]|[[:space:]]about[[:space:]]" && echo -- "$f"
    done
}

```
##### Function Calls:


```bash
└─ _typeset_functions_about
   └─ _typeset_functions
      └─ _shell
```




******
### >> _shell():


```bash
function _shell() {
    typeset this=$(ps -o comm -p $$ | tail -1 | awk '{print $NF}' | sed 's/^-*//')
    echo "${this##*/}"    # e.g. /bin/bash => bash
}

```




******
### >> _generate_metadata_functions():


```bash
function _generate_metadata_functions() {
    typeset f
    for f in $(_composure_keywords)
    do
	eval "$f() { :; }"
    done
}

```
##### Function Calls:


```bash
└─ _generate_metadata_functions
   └─ _composure_keywords
```




******
### >> _list_composure_files():


```bash
function _list_composure_files() {
    typeset composure_dir="$(_get_composure_dir)"
    [ -d "$composure_dir" ] && find "$composure_dir" -maxdepth 1 -name '*.inc'
}

```
##### Function Calls:


```bash
└─ _list_composure_files
   └─ _get_composure_dir
```




******
### >> _load_composed_functions():


```bash
function _load_composed_functions() {

    if [ "$LOAD_COMPOSED_FUNCTIONS" = "0" ]; then
	return    # if you say so...
    fi

    typeset inc
    for inc in $(_list_composure_files); do
	. "$inc"
    done
}

```
##### Function Calls:


```bash
└─ _load_composed_functions
   └─ _list_composure_files
      └─ _get_composure_dir
```




******
### >> _strip_trailing_whitespace():


```bash
function _strip_trailing_whitespace() {
    sed -e 's/ \+$//'
}

```




******
### >> _strip_semicolons():


```bash
function _strip_semicolons() {
    sed -e 's/;$//'
}

```




******
### >> cite():


>***about***: creates one or more meta keywords for use in your functions


>***param***: one or more keywords


>***example***: `$ cite url username`


>***example***: `$ url http://somewhere.com`


>***example***: `$ username alice`


>***group***: composure


```bash
function cite() {




    if [ -z "$1" ]; then
	printf '%s\n' 'missing parameter(s)'
	reference cite
	return
    fi

    typeset keyword
    for keyword in "$@"; do
	eval "$keyword() { :; }"
    done
}

```




******
### >> draft():


>***about***: wraps command from history into a new function, default is last command


>***param***: 1: name to give function


>***param***: 2: optional history line number


>***example***: `$ ls`


>***example***: `$ draft list`


>***example***: `$ draft newfunc 1120    # wraps command at history line 1120 in newfunc()`


>***group***: composure


about


param


example`


group


```bash
function draft() {

    typeset func=$1
    typeset num=$2

    if [ -z "$func" ]; then
	printf '%s\n' 'missing parameter(s)'
	reference draft
	return
    fi

    if type -a "$func" 2>/dev/null | grep -q 'is.*alias'; then
	printf '%s\n' "sorry, $(type -a "$func"). please choose another name."
	return
    fi

    typeset cmd
    if [ -z "$num" ]; then
	typeset lines=$(fc -ln -1 | grep -q draft && echo 2 || echo 1)
	cmd=$(fc -ln -$lines | head -1 | sed 's/^[[:blank:]]*//')
    else
	cmd=$(eval "history | grep '^[[:blank:]]*$num' | head -1" | sed 's/^[[:blank:][:digit:]]*//')
    fi
    eval "function $func {
    author '$(_get_author_name)'
    $cmd;
}"
    typeset file=$(_temp_filename_for draft)
    typeset -f "$func" | _strip_trailing_whitespace | _strip_semicolons > "$file"
    _transcribe "$func" "$file" Draft "Initial draft"
    command rm "$file" 2>/dev/null
    revise "$func"
}

```
##### Function Calls:


```bash
└─ draft
   ├─ _get_author_name
   |  └─ _get_composure_dir
   ├─ _temp_filename_for
   ├─ _transcribe
   |  ├─ _get_composure_dir
   |  └─ _add_composure_file
   ├─ _strip_trailing_whitespace
   ├─ _strip_semicolons
   └─ revise
      ├─ _get_composure_dir
      ├─ _temp_filename_for
      └─ _transcribe
```




******
### >> glossary():


>***about***: displays help summary for all functions, or summary for a group of functions


>***param***: 1: optional, group name


>***example***: `$ glossary`


>***example***: `$ glossary misc`


>***group***: composure


```bash
function glossary() {

    typeset targetgroup=${1:-}
    typeset functionlist="$(_typeset_functions_about)"
    typeset maxwidth=$(_longest_function_name_length "$functionlist" | awk '{print $1 + 5}')

    for func in $(echo $functionlist); do

	if [ "X${targetgroup}X" != "XX" ]; then
	    typeset group="$(typeset -f -- $func | metafor group)"
	    if [ "$group" != "$targetgroup" ]; then
		continue    # skip non-matching groups, if specified
	    fi
	fi
	typeset about="$(typeset -f -- $func | metafor about)"
	typeset aboutline=
	echo "$about" | fmt | while read -r aboutline; do
	    _letterpress "$aboutline" "$func" "$maxwidth"
	    func=" " # only display function name once
	done
    done
}

```
##### Function Calls:


```bash
└─ glossary
   ├─ _letterpress
   ├─ _longest_function_name_length
   ├─ _typeset_functions_about
   |  └─ _typeset_functions
   └─ metafor
      └─ glossary
```




******
### >> metafor():


>***about***: prints function metadata associated with keyword


>***param***: 1: meta keyword


>***example***: `typeset -f glossary | metafor example`


>***group***: composure


```bash
function metafor() {

    typeset keyword=$1

    if [ -z "$keyword" ]; then
	printf '%s\n' 'missing parameter(s)'
	reference metafor
	return
    fi


    sed -n "/$keyword / s/['\";]*\$//;s/^[ 	]*$keyword ['\"]*\([^([].*\)*\$/\1/p"
}

```
##### Function Calls:


```bash
└─ metafor
   └─ glossary
      ├─ _letterpress
      ├─ _longest_function_name_length
      ├─ _typeset_functions_about
      └─ metafor
```




******
### >> reference(){():


>***about***: displays apidoc help for a specific function


>***param***: 1: function name


>***example***: `$ reference revise`


>***group***: composure


```bash
function reference(){

    typeset func=$1
    if [ -z "$func" ]; then
	printf '%s\n' 'missing parameter(s)'
	reference reference
	return
    fi

    typeset line

    typeset about="$(typeset -f "$func" | metafor about)"
    _letterpress "$about" "$func"

    typeset author="$(typeset -f $func | metafor author)"
    if [ -n "$author" ]; then
	_letterpress "$author" 'author:'
    fi

    typeset version="$(typeset -f $func | metafor version)"
    if [ -n "$version" ]; then
	_letterpress "$version" 'version:'
    fi

    if [ -n "$(typeset -f $func | metafor param)" ]; then
	printf "parameters:\n"
	typeset -f $func | metafor param | while read -r line
	do
	    _letterpress "$line"
	done
    fi

    if [ -n "$(typeset -f $func | metafor example)" ]; then
	printf "examples:\n"
	typeset -f $func | metafor example | while read -r line
	do
	    _letterpress "$line"
	done
    fi
}

```
##### Function Calls:


```bash
└─ reference(){
   ├─ _letterpress
   └─ metafor
      └─ glossary
```




******
### >> revise():


>***about***: loads function into editor for revision


>***param***: <optional> -e: revise version stored in ENV


>***param***: 1: name of function


>***example***: `$ revise myfunction`


>***example***: `$ revise -e myfunction`


>***example***: `save a zero-length file to abort revision`


>***group***: composure


```bash
function revise() {

    typeset source='git'
    if [ "$1" = '-e' ]; then
	source='env'
	shift
    fi

    typeset func=$1
    if [ -z "$func" ]; then
	printf '%s\n' 'missing parameter(s)'
	reference revise
	return
    fi

    typeset composure_dir=$(_get_composure_dir)
    typeset temp=$(_temp_filename_for revise)
    if [ "$source" = 'env' ] || [ ! -f "$composure_dir/$func.inc" ]; then
	typeset -f $func > $temp
    else
	cat "$composure_dir/$func.inc" > "$temp"
    fi

    if [ -z "$EDITOR" ]
    then
	typeset EDITOR=vi
    fi

    $EDITOR "$temp"
    if [ -s "$temp" ]; then
	typeset edit='N'

	. "$temp" || edit='Y'

	while [ $edit = 'Y' ]; do
	    echo -n "Re-edit? Y/N: "
	    read -r edit
	    case $edit in
		 y|yes|Y|Yes|YES)
		     edit='Y'
		     $EDITOR "$temp"
		     . "$temp" && edit='N';;
		 *)
		     edit='N';;
	    esac
	done
	_transcribe "$func" "$temp" Revise
    else
	printf '%s\n' 'zero-length file, revision aborted!'
    fi
    command rm "$temp"
}

```
##### Function Calls:


```bash
└─ revise
   ├─ _get_composure_dir
   ├─ _temp_filename_for
   └─ _transcribe
      ├─ _get_composure_dir
      └─ _add_composure_file
```




******
### >> write():


>***about***: writes one or more composed function definitions to stdout


>***param***: one or more function names


>***example***: `$ write finddown foo`


>***example***: `$ write finddown`


>***group***: composure


```bash
function write() {

    if [ -z "$1" ]; then
        printf '%s\n' 'missing parameter(s)'
        reference write
        return
    fi

    echo "#!/usr/bin/env ${SHELL##*/}"

cat <<END
for f in $(_composure_keywords)
do
    eval "\$f() { :; }"
done
unset f
END

    typeset -f cite "$@"

cat <<END
main() {
    echo "edit me to do something useful!"
    exit 0
}
main \$*
END
}

_bootstrap_composure

: <<EOF
License: The MIT License
Copyright © 2012, 2016 Erich Smith
Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
EOF

cite about-module

```
##### Function Calls:


```bash
└─ write
   ├─ _composure_keywords
   └─ cite
```



## Aliases


| **Alias Name** | **Code** | **Notes** |
| ------------- | ------------- | ------------- |
| **cref** | `reference ` | 
