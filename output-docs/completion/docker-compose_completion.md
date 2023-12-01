
docker-compose Completions
==========================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/completions/docker-compose_completion.sh)***
## Function Index


```python
01 - __docker_compose_q
02 - __docker_compose_to_alternatives
03 - __docker_compose_to_extglob
04 - __docker_compose_has_option
05 - __docker_compose_map_key_of_current_option
06 - __docker_compose_nospace
07 - __docker_compose_services
08 - __docker_compose_complete_services
09 - __docker_compose_complete_running_services
10 - _docker_compose_build
11 - _docker_compose_bundle
12 - _docker_compose_config
13 - _docker_compose_create
14 - _docker_compose_docker_compose
15 - _docker_compose_down
16 - _docker_compose_events
17 - _docker_compose_exec
18 - _docker_compose_help
19 - _docker_compose_images
20 - _docker_compose_kill
21 - _docker_compose_logs
22 - _docker_compose_pause
23 - _docker_compose_port
24 - _docker_compose_ps
25 - _docker_compose_pull
26 - _docker_compose_push
27 - _docker_compose_restart
28 - _docker_compose_rm
29 - _docker_compose_run
30 - _docker_compose_scale
31 - _docker_compose_start
32 - _docker_compose_stop
33 - _docker_compose_top
34 - _docker_compose_unpause
35 - _docker_compose_up
36 - _docker_compose_version
37 - _docker_compose
```

******
### >> __docker_compose_q():


```bash
function __docker_compose_q() {
	docker-compose 2>/dev/null "${top_level_options[@]}" "$@"
}

```




******
### >> __docker_compose_to_alternatives():


```bash
function __docker_compose_to_alternatives() {
	local parts=( $1 )
	local IFS='|'
	echo "${parts[*]}"
}

```




******
### >> __docker_compose_to_extglob():


```bash
function __docker_compose_to_extglob() {
	local extglob=$( __docker_compose_to_alternatives "$1" )
	echo "@($extglob)"
}

```
##### Function Calls:


```bash
└─ __docker_compose_to_extglob
   └─ __docker_compose_to_alternatives
```




******
### >> __docker_compose_has_option():


```bash
function __docker_compose_has_option() {
	local pattern="$1"
	for (( i=2; i < $cword; ++i)); do
		if [[ ${words[$i]} =~ ^($pattern)$ ]] ; then
			return 0
		fi
	done
	return 1
}

```




******
### >> __docker_compose_map_key_of_current_option():


```bash
function __docker_compose_map_key_of_current_option() {
        local glob="$1"

        local key glob_pos
        if [ "$cur" = "=" ] ; then        # key= case
                key="$prev"
                glob_pos=$((cword - 2))
        elif [[ $cur == *=* ]] ; then     # key=value case (OSX)
                key=${cur%=*}
                glob_pos=$((cword - 1))
        elif [ "$prev" = "=" ] ; then
                key=${words[$cword - 2]}  # key=value case
                glob_pos=$((cword - 3))
        else
                return
        fi

        [ "${words[$glob_pos]}" = "=" ] && ((glob_pos--))  # --option=key=value syntax

        [[ ${words[$glob_pos]} == @($glob) ]] && echo "$key"
}

```




******
### >> __docker_compose_nospace():


```bash
function __docker_compose_nospace() {
	type compopt &>/dev/null && compopt -o nospace
}

```




******
### >> __docker_compose_services():


```bash
function __docker_compose_services() {
	__docker_compose_q ps --services "$@"
}

```
##### Function Calls:


```bash
└─ __docker_compose_services
   └─ __docker_compose_q
```




******
### >> __docker_compose_complete_services():


```bash
function __docker_compose_complete_services() {
	COMPREPLY=( $(compgen -W "$(__docker_compose_services "$@")" -- "$cur") )
}

```
##### Function Calls:


```bash
└─ __docker_compose_complete_services
   └─ __docker_compose_services
      └─ __docker_compose_q
```




******
### >> __docker_compose_complete_running_services():


```bash
function __docker_compose_complete_running_services() {
	local names=$(__docker_compose_services --filter status=running)
	COMPREPLY=( $(compgen -W "$names" -- "$cur") )
}

```
##### Function Calls:


```bash
└─ __docker_compose_complete_running_services
   └─ __docker_compose_services
      └─ __docker_compose_q
```




******
### >> _docker_compose_build():


```bash
function _docker_compose_build() {
	case "$prev" in
		--build-arg)
			COMPREPLY=( $( compgen -e -- "$cur" ) )
			__docker_compose_nospace
			return
			;;
		--memory|-m)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--build-arg --compress --force-rm --help --memory -m --no-cache --no-rm --pull --parallel -q --quiet" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services --filter source=build
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_build
   └─ __docker_compose_complete_services
      └─ __docker_compose_services
```




******
### >> _docker_compose_bundle():


```bash
function _docker_compose_bundle() {
	case "$prev" in
		--output|-o)
			_filedir
			return
			;;
	esac

	COMPREPLY=( $( compgen -W "--push-images --help --output -o" -- "$cur" ) )
}

```




******
### >> _docker_compose_config():


```bash
function _docker_compose_config() {
	case "$prev" in
		--hash)
			if [[ $cur == \\* ]] ; then
				COMPREPLY=( '\*' )
			else
				COMPREPLY=( $(compgen -W "$(__docker_compose_services) \\\* " -- "$cur") )
			fi
			return
			;;
	esac

	COMPREPLY=( $( compgen -W "--hash --help --quiet -q --resolve-image-digests --services --volumes" -- "$cur" ) )
}

```
##### Function Calls:


```bash
└─ _docker_compose_config
   └─ __docker_compose_services
      └─ __docker_compose_q
```




******
### >> _docker_compose_create():


```bash
function _docker_compose_create() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--build --force-recreate --help --no-build --no-recreate" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_docker_compose():


```bash
function _docker_compose_docker_compose() {
	case "$prev" in
		--tlscacert|--tlscert|--tlskey)
			_filedir
			return
			;;
		--file|-f)
			_filedir "y?(a)ml"
			return
			;;
		--log-level)
			COMPREPLY=( $( compgen -W "debug info warning error critical" -- "$cur" ) )
			return
			;;
		--project-directory)
			_filedir -d
			return
			;;
		$(__docker_compose_to_extglob "$daemon_options_with_args") )
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "$daemon_boolean_options $daemon_options_with_args $top_level_options_with_args --help -h --no-ansi --verbose --version -v" -- "$cur" ) )
			;;
		*)
			COMPREPLY=( $( compgen -W "${commands[*]}" -- "$cur" ) )
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_docker_compose
   └─ __docker_compose_to_extglob
      └─ __docker_compose_to_alternatives
```




******
### >> _docker_compose_down():


```bash
function _docker_compose_down() {
	case "$prev" in
		--rmi)
			COMPREPLY=( $( compgen -W "all local" -- "$cur" ) )
			return
			;;
		--timeout|-t)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --rmi --timeout -t --volumes -v --remove-orphans" -- "$cur" ) )
			;;
	esac
}

```




******
### >> _docker_compose_events():


```bash
function _docker_compose_events() {
	case "$prev" in
		--json)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --json" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_exec():


```bash
function _docker_compose_exec() {
	case "$prev" in
		--index|--user|-u|--workdir|-w)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "-d --detach --help --index --privileged -T --user -u --workdir -w" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_running_services
			;;
	esac
}

```




******
### >> _docker_compose_help():


```bash
function _docker_compose_help() {
	COMPREPLY=( $( compgen -W "${commands[*]}" -- "$cur" ) )
}

```




******
### >> _docker_compose_images():


```bash
function _docker_compose_images() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --quiet -q" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_kill():


```bash
function _docker_compose_kill() {
	case "$prev" in
		-s)
			COMPREPLY=( $( compgen -W "SIGHUP SIGINT SIGKILL SIGUSR1 SIGUSR2" -- "$(echo $cur | tr '[:lower:]' '[:upper:]')" ) )
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help -s" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_running_services
			;;
	esac
}

```




******
### >> _docker_compose_logs():


```bash
function _docker_compose_logs() {
	case "$prev" in
		--tail)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--follow -f --help --no-color --tail --timestamps -t" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_pause():


```bash
function _docker_compose_pause() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_running_services
			;;
	esac
}

```




******
### >> _docker_compose_port():


```bash
function _docker_compose_port() {
	case "$prev" in
		--protocol)
			COMPREPLY=( $( compgen -W "tcp udp" -- "$cur" ) )
			return;
			;;
		--index)
			return;
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --index --protocol" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_ps():


```bash
function _docker_compose_ps() {
	local key=$(__docker_compose_map_key_of_current_option '--filter')
	case "$key" in
		source)
			COMPREPLY=( $( compgen -W "build image" -- "${cur##*=}" ) )
			return
			;;
		status)
			COMPREPLY=( $( compgen -W "paused restarting running stopped" -- "${cur##*=}" ) )
			return
			;;
	esac

	case "$prev" in
		--filter)
			COMPREPLY=( $( compgen -W "source status" -S "=" -- "$cur" ) )
			__docker_compose_nospace
			return;
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--all -a --filter --help --quiet -q --services" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_ps
   └─ __docker_compose_map_key_of_current_option
```




******
### >> _docker_compose_pull():


```bash
function _docker_compose_pull() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --ignore-pull-failures --include-deps --no-parallel --quiet -q" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services --filter source=image
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_pull
   └─ __docker_compose_complete_services
      └─ __docker_compose_services
```




******
### >> _docker_compose_push():


```bash
function _docker_compose_push() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --ignore-push-failures" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_restart():


```bash
function _docker_compose_restart() {
	case "$prev" in
		--timeout|-t)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --timeout -t" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_running_services
			;;
	esac
}

```




******
### >> _docker_compose_rm():


```bash
function _docker_compose_rm() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--force -f --help --stop -s -v" -- "$cur" ) )
			;;
		*)
			if __docker_compose_has_option "--stop|-s" ; then
				__docker_compose_complete_services
			else
				__docker_compose_complete_services --filter status=stopped
			fi
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_rm
   ├─ __docker_compose_has_option
   └─ __docker_compose_complete_services
      └─ __docker_compose_services
```




******
### >> _docker_compose_run():


```bash
function _docker_compose_run() {
	case "$prev" in
		-e)
			COMPREPLY=( $( compgen -e -- "$cur" ) )
			__docker_compose_nospace
			return
			;;
		--entrypoint|--label|-l|--name|--user|-u|--volume|-v|--workdir|-w)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--detach -d --entrypoint -e --help --label -l --name --no-deps --publish -p --rm --service-ports -T --use-aliases --user -u --volume -v --workdir -w" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```




******
### >> _docker_compose_scale():


```bash
function _docker_compose_scale() {
	case "$prev" in
		=)
			COMPREPLY=("$cur")
			return
			;;
		--timeout|-t)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --timeout -t" -- "$cur" ) )
			;;
		*)
			COMPREPLY=( $(compgen -S "=" -W "$(__docker_compose_services)" -- "$cur") )
			__docker_compose_nospace
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_scale
   └─ __docker_compose_services
      └─ __docker_compose_q
```




******
### >> _docker_compose_start():


```bash
function _docker_compose_start() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services --filter status=stopped
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_start
   └─ __docker_compose_complete_services
      └─ __docker_compose_services
```




******
### >> _docker_compose_stop():


```bash
function _docker_compose_stop() {
	case "$prev" in
		--timeout|-t)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help --timeout -t" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_running_services
			;;
	esac
}

```




******
### >> _docker_compose_top():


```bash
function _docker_compose_top() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_running_services
			;;
	esac
}

```




******
### >> _docker_compose_unpause():


```bash
function _docker_compose_unpause() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--help" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services --filter status=paused
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_unpause
   └─ __docker_compose_complete_services
      └─ __docker_compose_services
```




******
### >> _docker_compose_up():


```bash
function _docker_compose_up() {
	case "$prev" in
		=)
			COMPREPLY=("$cur")
			return
			;;
		--exit-code-from)
			__docker_compose_complete_services
			return
			;;
		--scale)
			COMPREPLY=( $(compgen -S "=" -W "$(__docker_compose_services)" -- "$cur") )
			__docker_compose_nospace
			return
			;;
		--timeout|-t)
			return
			;;
	esac

	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--abort-on-container-exit --always-recreate-deps --build -d --detach --exit-code-from --force-recreate --help --no-build --no-color --no-deps --no-recreate --no-start --renew-anon-volumes -V --remove-orphans --scale --timeout -t" -- "$cur" ) )
			;;
		*)
			__docker_compose_complete_services
			;;
	esac
}

```
##### Function Calls:


```bash
└─ _docker_compose_up
   └─ __docker_compose_services
      └─ __docker_compose_q
```




******
### >> _docker_compose_version():


```bash
function _docker_compose_version() {
	case "$cur" in
		-*)
			COMPREPLY=( $( compgen -W "--short" -- "$cur" ) )
			;;
	esac
}

```




******
### >> _docker_compose():


```bash
function _docker_compose() {
	local previous_extglob_setting=$(shopt -p extglob)
	shopt -s extglob

	local commands=(
		build
		bundle
		config
		create
		down
		events
		exec
		help
		images
		kill
		logs
		pause
		port
		ps
		pull
		push
		restart
		rm
		run
		scale
		start
		stop
		top
		unpause
		up
		version
	)

	local daemon_boolean_options="
		--skip-hostname-check
		--tls
		--tlsverify
	"
	local daemon_options_with_args="
		--file -f
		--host -H
		--project-directory
		--project-name -p
		--tlscacert
		--tlscert
		--tlskey
	"

	local top_level_options_with_args="
		--log-level
	"

	COMPREPLY=()
	local cur prev words cword
	_get_comp_words_by_ref -n : cur prev words cword

	local command='docker_compose'
	local top_level_options=()
	local counter=1

	while [ $counter -lt $cword ]; do
		case "${words[$counter]}" in
			$(__docker_compose_to_extglob "$daemon_boolean_options") )
				local opt=${words[counter]}
				top_level_options+=($opt)
				;;
			$(__docker_compose_to_extglob "$daemon_options_with_args") )
				local opt=${words[counter]}
				local arg=${words[++counter]}
				top_level_options+=($opt $arg)
				;;
			$(__docker_compose_to_extglob "$top_level_options_with_args") )
				(( counter++ ))
				;;
			-*)
				;;
			*)
				command="${words[$counter]}"
				break
				;;
		esac
		(( counter++ ))
	done

	local completions_func=_docker_compose_${command//-/_}
	declare -F $completions_func >/dev/null && $completions_func

	eval "$previous_extglob_setting"
	return 0
}

eval "$__docker_compose_previous_extglob_setting"
unset __docker_compose_previous_extglob_setting

complete -F _docker_compose docker-compose docker-compose.exe

```
##### Function Calls:


```bash
└─ _docker_compose
   └─ __docker_compose_to_extglob
      └─ __docker_compose_to_alternatives
```


