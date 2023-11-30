
sshagent helper functions
=========================


***(in /home/bsgt/stablecaps_bashrc/modules/ssh-agent_module.sh)***
## Function Index


```python
01 - _get_sshagent_pid_from_env_file
02 - _get_process_status_field
03 - _is_item_in_list
04 - _is_proc_alive_at_pid
05 - _ensure_valid_sshagent_env
06 - _ensure_sshagent_dead
07 - sshlist
08 - sshagent
```

******
### >> _get_sshagent_pid_from_env_file():


```bash
function _get_sshagent_pid_from_env_file() {

  local env_file="${1}"
  [[ -r "${env_file}" ]] || {
    echo "";
    return
  }
  tail -1 "${env_file}" \
  | cut -d' ' -f4 \
  | cut -d';' -f1
}

```




******
### >> _get_process_status_field():


```bash
function _get_process_status_field() {

  local \
    pid \
    status_file \
    field
  pid="${1}"
  field="${2}"
  status_file="/proc/${pid}/status"
  if ! ([[ -d "${status_file%/*}" ]] \
    && [[ -r "${status_file}" ]]); then
    echo ""; return;
  fi
  grep "${field}:" "${status_file}" \
  | cut -d':' -f2 \
  | sed -e 's/[[:space:]]\+//g' \
  | cut -d'(' -f1
}

```




******
### >> _is_item_in_list():


```bash
function _is_item_in_list() {
  local item
  for item in "${@:1}"; do
    if [[ "${item}" == "${1}" ]]; then
      return 1
    fi
  done
  return 0
}

```




******
### >> _is_proc_alive_at_pid():


```bash
function _is_proc_alive_at_pid() {

  local \
    pid \
    expected_name \
    actual_name \
    actual_state
  pid="${1?}"
  expected_name="ssh-agent"
  actual_name=$(_get_process_status_field "${pid}" "Name")
  [[ "${expected_name}" == "${actual_name}" ]] || return 1
  actual_state=$(_get_process_status_field "${pid}" "State")
  if _is_item_in_list "${actual_state}" "X" "T" "Z"; then
    return 1
  fi
  return 0
}

```
##### Function Calls:


```bash
└─ _is_proc_alive_at_pid
   ├─ _get_process_status_field
   └─ _is_item_in_list
```




******
### >> _ensure_valid_sshagent_env():


```bash
function _ensure_valid_sshagent_env() {

  local \
    agent_pid \
    tmp_res

  mkdir -p "${HOME}/.ssh"
  type restorecon &> /dev/null
  tmp_res="$?"

  if [[ "${tmp_res}" -eq 0 ]]; then
    restorecon -rv "${HOME}/.ssh"
  fi

  if ! [[ -r "${SSH_AGENT_ENV}" ]]; then
    ssh-agent > "${SSH_AGENT_ENV}"
    return
  fi

  agent_pid=$(_get_sshagent_pid_from_env_file "${SSH_AGENT_ENV}")
  if [[ -z "${agent_pid}" ]]; then
    ssh-agent > "${SSH_AGENT_ENV}"
    return
  fi

  if _is_proc_alive_at_pid "${agent_pid}"; then
    return
  fi

  ssh-agent > "${SSH_AGENT_ENV}"
  return
}

```
##### Function Calls:


```bash
└─ _ensure_valid_sshagent_env
   ├─ _get_sshagent_pid_from_env_file
   └─ _is_proc_alive_at_pid
      ├─ _get_process_status_field
      └─ _is_item_in_list
```




******
### >> _ensure_sshagent_dead():


```bash
function _ensure_sshagent_dead() {
  [[ -r "${SSH_AGENT_ENV}" ]] \
  || return ## no agent file - no problems

  agent_pid=$(
    _get_sshagent_pid_from_env_file \
    "${SSH_AGENT_ENV}"
  )

  [[ -n "${agent_pid}" ]] \
  || return # no pid - no problem

  _is_proc_alive_at_pid "${agent_pid}" \
  || return # process is not alive - no problem

  echo -e -n "Killing ssh-agent (pid:${agent_pid}) ... "
  kill -9 "${agent_pid}" && echo "DONE" || echo "FAILED"
  rm -f "${SSH_AGENT_ENV}"
}

```
##### Function Calls:


```bash
└─ _ensure_sshagent_dead
   ├─ _get_sshagent_pid_from_env_file
   └─ _is_proc_alive_at_pid
      ├─ _get_process_status_field
      └─ _is_item_in_list
```




******
### >> sshlist():


>***about***: list hosts defined in ssh config


>***group***: ssh


>***example***: `sshlist`


```bash
function sshlist() {

  awk '$1 ~ /Host$/ {for (i=2; i<=NF; i++) print $i}' ~/.ssh/config
}

```




******
### >> sshagent():


>***about***: ensures ssh-agent is up and running


>***param***: 1: on|off


>***group***: ssh


>***example***: `$ sshagent on`


```bash
function sshagent() {

  [[ -z "${SSH_AGENT_ENV}" ]] \
  && export SSH_AGENT_ENV="${HOME}/.ssh/agent_env.${HOSTNAME}"

  case "${1}" in
    on) _ensure_valid_sshagent_env;
      source "${SSH_AGENT_ENV}" > /dev/null;
      ;;
    off) _ensure_sshagent_dead
      ;;
    *)
      ;;
  esac
}

sshagent on

```


