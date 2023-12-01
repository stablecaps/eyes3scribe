
Scrap functions
===============


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/internal/_unused_scrap_functions.sh)***
## Function Index


```python
01 - FUNCpromptCommand
```

******
### >> FUNCpromptCommand():


```bash
function FUNCpromptCommand () {
    sudo -n uptime 2>/dev/null 1>/dev/null
  local bSudoOn=`if(($?==0));then echo true; else echo false; fi`

    history -a; # append to history at each command issued!!!
    local width=`tput cols`;
    local half=$((width/2))
    local dt="[EndAt:`date +"%Y/%m/%d-%H:%M:%S.%N"`]";
  if $bSudoOn; then dt="!!!SUDO!!!$dt"; fi
    local sizeDtHalf=$((${#dt}/2))
    echo
    output=`printf "%*s%*s" $((half+sizeDtHalf)) "$dt" $((half-sizeDtHalf)) "" |sed 's" "="g';`

    local colorLightRed="\e[1;31m"
  local colorNoColor="\e[0m"
    if $bSudoOn; then
        echo -e "${colorLightRed}${output}${colorNoColor}"
    else
        echo -e "${output}"
    fi
}

```


