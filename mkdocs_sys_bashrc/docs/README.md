# Stablecaps bashrc

## Premise
Slimmed down sysadmin .bashrc that should hopefully have minimal system dependencies.

## Extended Documentation >> https://stablecaps.github.io/stablecaps_bashrc/

## Installation - Git Clone
```
cd
git clone https://github.com/stablecaps/stablecaps_bashrc.git
mv .bashrc .your_old_bashrc
ln -fs ~/stablecaps_bashrc/_bashrc ~/.bashrc
source ~/.bashrc
```

## Installation - wget & unzip
```sh

sudo apt install wget jq unzip

cd
mv .bashrc .your_old_bashrc
#
RELEASE_VERSION=$(wget -q -nv -O- "https://api.github.com/repos/stablecaps/stablecaps_bashrc/releases/latest" | jq '.tag_name' | sed 's|v||g' | sed 's|"||g')
wget https://github.com/stablecaps/stablecaps_bashrc/archive/refs/tags/v${RELEASE_VERSION}.zip -O stablecaps_bashrc.zip
unzip stablecaps_bashrc.zip
mv stablecaps_bashrc-${RELEASE_VERSION} stablecaps_bashrc
ln -fs ~/stablecaps_bashrc/_bashrc ~/.bashrc
source ~/.bashrc
```
