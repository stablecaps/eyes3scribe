
Docker aliases
==============


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_stablecaps_bashrc/docs/aliases/docker_aliases.sh)***
## Function Index


```python
01 - dkln
02 - dkclean
03 - dktop
04 - dkstats
05 - dke
06 - dkrun
07 - dkexe
08 - dkstate
09 - dksb
10 - mongo
11 - redis
12 - dkp
13 - dkpnc
14 - dkpl
```

******
### >> dkln():


>***about***: Gets docker logs from running container


>***group***: docker


>***param***: container-id or name


>***example***: `dkln 1411494fa3db`


```bash
function dkln() {

    docker logs -f $(docker ps | grep $1 | awk '{print $1}')
}

```




******
### >> dkclean():


>***about***: Remove all exited containers and dangling volumes


>***group***: docker


>***example***: `dkclean`


```bash
function dkclean() {

    docker rm $(docker ps --all -q -f status=exited)
    docker volume rm $(docker volume ls -qf dangling=true)
}

```




******
### >> dktop():


>***about***: Docker Top - Formatted


>***group***: docker


>***example***: `dktop`


```bash
function dktop() {

    docker stats --format "table {{.Container}}\t{{.Name}}\t{{.CPUPerc}}  {{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"
}

```




******
### >> dkstats():


>***about***: Docker stats - All or named container


>***group***: docker


>***param***: optional: container-id or name


>***example***: `dkstats`


>***example***: `dkstats a2234c1bc7ea`


```bash
function dkstats() {

    if [ $# -eq 0 ]
        then docker stats --no-stream;
        else docker stats --no-stream | grep $1;
    fi
}

```




******
### >> dke():


>***about***: Docker exec into container to get /bin/sh prompt


>***group***: docker


>***param***: container-id or name


>***example***: `dke a2234c1bc7ea`


```bash
function dke() {

    docker exec -it $1 /bin/sh
}

```




******
### >> dkrun():


>***about***: Docker run into image to get /bin/sh prompt


>***group***: docker


>***param***: image-id or image repository


>***example***: `dkrun nginx`


>***example***: `dkrun 992e3b7be046`


```bash
function dkrun() {

    docker run -it $1 /bin/sh
}

```




******
### >> dkexe():


>***about***: Docker exec to run arbitary command on running container.


>***group***: docker


>***param***: 1. container-id or name


>***param***: 2. arbitary nix command


>***example***: `dkexe 992e3b7be046 ls /workspace/`


```bash
function dkexe() {

    docker exec -it $1 $2
}

```




******
### >> dkstate():


>***about***: Read docker state of running container via docker inspect


>***group***: docker


>***param***: container-id or name


>***example***: `dkstate a2234c1bc7ea`


```bash
function dkstate() {

    docker inspect $1 | jq .[0].State
}

```




******
### >> dksb():


```bash
function dksb() {
    docker service scale $1=0
    sleep 2
    docker service scale $1=$2
}

```




******
### >> mongo():


```bash
function mongo() {
    mongoLabel=$(docker ps | grep mongo | awk '{print $NF}')
    docker exec -it $mongoLabel mongo "$@"
}

```




******
### >> redis():


```bash
function redis() {
    redisLabel=$(docker ps | grep redis | awk '{print $NF}')
    docker exec -it $redisLabel redis-cli
}

```




******
### >> dkp():


>***about***: Build & push npm container package with $NPM_TOKEN as build arg. Requires package.json


>***group***: docker


>***param***: container name


>***example***: `dkp mynpm-conatiner`


```bash
function dkp() {

    if [ ! -f .dockerignore ]; then
        echo "Warning, .dockerignore file is missing."
        read -p "Proceed anyway?"
    fi

    if [ ! -f package.json ]; then
        echo "Warning, package.json file is missing."
        read -p "Are you in the right directory?"
    fi

    VERSION=$(cat package.json | jq .version | sed 's/\"//g')
    NAME=$(cat package.json | jq .name | sed 's/\"//g')
    LABEL="$1/$NAME:$VERSION"

    docker build --build-arg NPM_TOKEN=${NPM_TOKEN} -t $LABEL .

    read -p "Press enter to publish"
    docker push $LABEL
}

```




******
### >> dkpnc():


>***about***: Build (without cache) & push npm container with $NPM_TOKEN as build arg. Requires package.json


>***group***: docker


>***param***: container name


>***example***: `dkpnc mynpm-conatiner`


```bash
function dkpnc() {

    if [ ! -f .dockerignore ]; then
        echo "Warning, .dockerignore file is missing."
        read -p "Proceed anyway?"
    fi

    if [ ! -f package.json ]; then
        echo "Warning, package.json file is missing."
        read -p "Are you in the right directory?"
    fi

    VERSION=$(cat package.json | jq .version | sed 's/\"//g')
    NAME=$(cat package.json | jq .name | sed 's/\"//g')
    LABEL="$1/$NAME:$VERSION"

    docker build --build-arg NPM_TOKEN=${NPM_TOKEN} --no-cache=true -t $LABEL .
    read -p "Press enter to publish"
    docker push $LABEL
}

```




******
### >> dkpl():


>***about***: Build (without cache) & push npm container (with latest tag) and with $NPM_TOKEN as build arg. Requires package.json


>***group***: docker


>***param***: container name


>***example***: `dkpl mynpm-conatiner`


```bash
function dkpl() {

    if [ ! -f .dockerignore ]; then
        echo "Warning, .dockerignore file is missing."
        read -p "Proceed anyway?"
    fi

    if [ ! -f package.json ]; then
        echo "Warning, package.json file is missing."
        read -p "Are you in the right directory?"
    fi

    VERSION=$(cat package.json | jq .version | sed 's/\"//g')
    NAME=$(cat package.json | jq .name | sed 's/\"//g')
    LATEST="$1/$NAME:latest"

    docker build --build-arg NPM_TOKEN=${NPM_TOKEN} --no-cache=true -t $LATEST .
    read -p "Press enter to publish"
    docker push $LATEST
}

```



## Aliases


| **Alias Name** | **Code** | **Notes** |
| ------------- | ------------- | ------------- |
| **dk** | `docker` | 
| **dklc** | `docker ps -l' ` |  List last Docker container
| **dklcid** | `docker ps -l -q' ` |  List last Docker container ID
| **dklcip** | `docker inspect -f "{{.NetworkSettings.IPAddress}}" $(docker ps -l -q)' ` |  Get IP of last Docker container
| **dkps** | `docker ps' ` |  List running Docker containers
| **dkpsa** | `docker ps -a' ` |  List all Docker containers
| **dki** | `docker images' ` |  List Docker images
| **dkrmac** | `docker rm $(docker ps -a -q)' ` |  Delete all Docker containers
| **dkelc** | `docker exec -it $(dklcid) bash --login'` |  Enter last container (works with Docker 1.3 and above)
| **dkrmflast** | `docker rm -f $(dklcid)` | 
| **dkbash** | `dkelc` | 
| **dkex** | `docker exec -it '` |  Useful to run any commands into container without leaving host
| **dkri** | `docker run --rm -i ` | 
| **dkrit** | `docker run --rm -it ` | 
| **dkip** | `docker image prune -a -f` | 
| **dkvp** | `docker volume prune -f` | 
| **dksp** | `docker system prune -a -f` | 
| **dkpruneall** | `docker system prune -a -f --all --volumes` | 
| **dm** | `docker-machine` | 
| **dmx** | `docker-machine ssh` | 
| **dks** | `docker service` | 
| **dkrm** | `docker rm` | 
| **dkl** | `docker logs` | 
| **dklf** | `docker logs -f` | 
| **dkflush** | `docker rm $(docker ps --no-trunc -aq)` | 
| **dkflush2** | `docker rmi $(docker images --filter "dangling=true" -q --no-trunc)` | 
| **dkt** | `docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"` | 
| **dkps** | `docker ps` | 
