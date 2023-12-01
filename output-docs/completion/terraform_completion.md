
Terraform completions
=====================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/completions/terraform_completion.sh)***
## Function Index


```python
01 - _terraform
```

******
### >> _terraform():


```bash
function _terraform() {
	local cur prev words cword opts
	_get_comp_words_by_ref -n : cur prev words cword
	COMPREPLY=()
	opts=""

	if [[ ${cword} -eq 1 ]] ; then

		opts="$(terraform --help | grep -E '^\s\s\s\s\S' | awk '{print $1}')"
		opts="${opts} --help --version"

	elif [[ ${cword} -gt 1 ]] ; then

		if [[ ${cword} -eq 2 && ${prev} == '--help' ]] ; then

			opts="$(terraform --help | grep -E '^\s\s\s\s\S' | awk '{print $1}')"

		elif [[ ${words[1]} != "--help" && ${words[1]} != "--version" && ${words[1]} != "version" ]] ; then

			opts="$(terraform --help "${words[1]}" | grep -E '^\s+-' | awk '{print $1}' | awk -F '=' '{ if ($0 ~ /=/) {print $1"="} else {print $1} }')"
			opts="${opts} $(terraform --help "${words[1]}" | grep -E '^\s\s\s\s\S' | awk '{print $1}')"
			opts="${opts} --help"

		fi
	fi

	COMPREPLY=( $(compgen -W "${opts}" -- "${cur}") )

	if [[ ${#COMPREPLY[*]} -eq 1 ]] ; then
		if [[ ${COMPREPLY[0]} == *= ]] ; then
			compopt -o nospace
		fi
	fi
	return 0
}

complete -F _terraform terraform

```


