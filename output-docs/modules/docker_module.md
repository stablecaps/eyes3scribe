
Helpers to more easily work with Docker
=======================================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_sys_bashrc/docs/modules/docker_module.sh)***
## Function Index


```python
01 - docker-remove-most-recent-container
02 - docker-remove-most-recent-image
03 - docker-remove-stale-assets
04 - docker-enter
05 - docker-remove-images
06 - docker-image-dependencies
07 - docker-runtime-environment
08 - docker-archive-content
```

******
### >> docker-remove-most-recent-container():


>***about***: attempt to remove the most recent container from docker ps -a


>***group***: docker


```bash
function docker-remove-most-recent-container() {
    docker ps -ql | xargs docker rm
}

```




******
### >> docker-remove-most-recent-image():


>***about***: attempt to remove the most recent image from docker images


>***group***: docker


```bash
function docker-remove-most-recent-image() {
    docker images -q | head -1 | xargs docker rmi
}

```




******
### >> docker-remove-stale-assets():


>***about***: attempt to remove exited containers and dangling images


>***group***: docker


```bash
function docker-remove-stale-assets() {
    docker ps --filter status=exited -q | xargs docker rm --volumes
    docker images --filter dangling=true -q | xargs docker rmi
}

```




******
### >> docker-enter():


>***about***: enter the specified docker container using bash


>***group***: docker


>***param***: 1: Name of the container to enter


>***example***: `docker-enter oracle-xe`


```bash
function docker-enter() {

    docker exec -it "$@" /bin/bash;
}

```




******
### >> docker-remove-images():


>***about***: attempt to remove images with supplied tags or all if no tags are supplied


>***group***: docker


```bash
function docker-remove-images() {
    if [ -z "$1" ]; then
        docker rmi $(docker images -q)
    else
        DOCKER_IMAGES=""
        for IMAGE_ID in $@; do DOCKER_IMAGES="$DOCKER_IMAGES\|$IMAGE_ID"; done
        ID_ARRAY=($(docker images | grep "${DOCKER_IMAGES:2}" | awk {'print $3'}))
        docker rmi $(echo ${ID_ARRAY[@]} | tr ' ' '\n' | sort -u | tr '\n' ' ')
 fi
}

```




******
### >> docker-image-dependencies():


>***about***: attempt to create a Graphiz image of the supplied image ID dependencies


>***group***: docker


```bash
function docker-image-dependencies() {
    if hash dot 2>/dev/null; then
        OUT=$(mktemp -t docker-viz-XXXX.png)
        docker images -viz | dot -Tpng > $OUT
        case $OSTYPE in
            linux*)
                xdg-open $OUT
                ;;
            darwin*)
                open $OUT
                ;;
        esac
    else
        >&2 echo "Can't show dependencies; Graphiz is not installed"
    fi
}

```




******
### >> docker-runtime-environment():


>***about***: attempt to list the environmental variables of the supplied image ID


>***group***: docker


```bash
function docker-runtime-environment() {
    docker run "$@" env
}

```




******
### >> docker-archive-content():


>***about***: show the content of the provided Docker image archive


>***group***: docker


>***param***: 1: image archive name


>***example***: `docker-archive-content images.tar.gz`


```bash
function docker-archive-content() {

    if [ -n "$1" ]; then
        tar -xzOf $1 manifest.json | jq '[.[] | .RepoTags] | add'
    fi
}

```


