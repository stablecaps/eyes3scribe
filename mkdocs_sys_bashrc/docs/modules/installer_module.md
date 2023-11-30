
Install additional packages
===========================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/modules/installer_module.sh)***
## Function Index


```python
01 - get-latest-gh-release
02 - install-usr-local
03 - install-sys-bashrc-deps
```

******
### >> get-latest-gh-release():


>***about***: Download & extract the latest package release from gihub releases page to /tmp. Use install-usr-local() to install correct file


>***group***: installers


>***param***: 1: package name. This is used to search an internal dictionary for github connection details


>***example***: `get-latest-gh-release ccat`


```bash
function get-latest-gh-release() {

    local PACKAGE_NAME=$1
    local GITHUB_USER=$(echo "${GH_INSTALL_LIB[${PACKAGE_NAME}]}" | cut -d, -f1)
    local GITHUB_REPO=$(echo "${GH_INSTALL_LIB[${PACKAGE_NAME}]}" | cut -d, -f2)

    if ! command -v jq &> /dev/null; then
        echo -e "please install stablecaps_bashrc dependencies using the command: \ninstall-sys-bashrc-deps"
        return 42
    fi

    local LNX_AMD64_RELEASE_URL=$(wget -q -nv -O- "https://api.github.com/repos/$GITHUB_USER/$GITHUB_REPO/releases/latest" 2>/dev/null |  jq -r '.assets[] | select(.browser_download_url | contains("linux-amd64")) | .browser_download_url')

    local REL_FILE=$(basename $LNX_AMD64_RELEASE_URL)
    echo "Release file is: $REL_FILE"

	wget -q -nv -O "/tmp/${REL_FILE}" $LNX_AMD64_RELEASE_URL
	if [ ! -f "/tmp/${REL_FILE}" ]; then
		echo -e "\n~~~~~~~~~~~~~~~\nDidn't download $PACKAGE_NAME from url:$LNX_AMD64_RELEASE_URL properly.  Where is /tmp/${REL_FILE}?"
        return 42
	fi

    echo "Now extracting $REL_FILE to /tmp"
    cd /tmp
    extract $REL_FILE
}

```




******
### >> install-usr-local():


>***about***: Move program to /usr/local/bin


>***group***: installers


>***param***: 1: Program file to move to /usr/local/bin. This function makes it executable


>***example***: `install-usr-local ${SOME_PROG}`


```bash
function install-usr-local() {

    MYPROG=$1

	sudo mv -fv $MYPROG /usr/local/bin
	sudo chmod -v +x /usr/local/bin/$(basename $MYPROG)
}

```




******
### >> install-sys-bashrc-deps():


>***about***: Install stablecaps_bashrc dependencies


>***group***: installers


>***example***: `install-sys-bashrc-deps`


```bash
function install-sys-bashrc-deps() {
    sudo apt install jq
}

```


