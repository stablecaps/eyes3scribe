
common git abbreviations
========================


***(in /media/bsgt/jogi1/XX_local_PSYNC_linux2/XXX_CONTRACTING/stablecaps/0000_STABLECAPS_GITREPOS/bash-auto-documatix/mkdocs_stablecaps_bashrc/docs/aliases/git_aliases.sh)***
## Aliases


| **Alias Name** | **Code** | **Notes** |
| ------------- | ------------- | ------------- |
| **gdiffh** | `git diff HEAD` | 
| **gpllo** | `git pull origin` | 
| **gpllocb** | `git pull origin $(git rev-parse --abbrev-ref HEAD)'` |  git pull origin current branch
| **gp** | `git push` | 
| **gpo** | `git push origin` | 
| **gpocb** | `git push origin $(git rev-parse --abbrev-ref HEAD)'` |  git push origin current branch
| **gcl** | `git clone` | 
| **ga** | `git add` | 
| **grm** | `git rm` | 
| **gap** | `git add -p` | 
| **gall** | `git add -A` | 
| **gf** | `git fetch --all --prune` | 
| **gft** | `git fetch --all --prune --tags` | 
| **gfv** | `git fetch --all --prune --verbose` | 
| **gftv** | `git fetch --all --prune --tags --verbose` | 
| **gus** | `git reset HEAD` | 
| **gpristine** | `git reset --hard && git clean -dfx` | 
| **gclean** | `git clean -fd` | 
| **gm** | `git merge` | 
| **gmv** | `git mv` | 
| **g** | `git` | 
| **get** | `git` | 
| **gs** | `git status` | 
| **gss** | `git status -s` | 
| **gsu** | `git submodule update --init --recursive` | 
| **gl** | `git pull` | 
| **glum** | `git pull upstream master` | 
| **gpr** | `git pull --rebase` | 
| **gpp** | `git pull && git push` | 
| **gup** | `git fetch && git rebase` | 
| **gp** | `git push` | 
| **gpo** | `git push origin` | 
| **gpu** | `git push --set-upstream` | 
| **gpuo** | `git push --set-upstream origin` | 
| **gpuoc** | `git push --set-upstream origin $(git symbolic-ref --short HEAD)` | 
| **gpom** | `git push origin master` | 
| **gr** | `git remote` | 
| **grv** | `git remote -v` | 
| **gra** | `git remote add` | 
| **gd** | `git diff` | 
| **gds** | `git diff --staged` | 
| **gdv** | `git diff -w "$@" | vim -R -` | 
| **gc** | `git commit -v` | 
| **gca** | `git commit -v -a` | 
| **gcm** | `git commit -v -m` | 
| **gcam** | `git commit -v -am` | 
| **gci** | `git commit --interactive` | 
| **gb** | `git branch` | 
| **gba** | `git branch -a` | 
| **gbt** | `git branch --track` | 
| **gbm** | `git branch -m` | 
| **gbd** | `git branch -d` | 
| **gbD** | `git branch -D` | 
| **gcount** | `git shortlog -sn` | 
| **gcp** | `git cherry-pick` | 
| **gcpx** | `git cherry-pick -x` | 
| **gco** | `git checkout` | 
| **gcom** | `git checkout master` | 
| **gcb** | `git checkout -b` | 
| **gcob** | `git checkout -b` | 
| **gct** | `git checkout --track` | 
| **gcpd** | `git checkout master; git pull; git branch -D` | 
| **gexport** | `git archive --format zip --output` | 
| **gdel** | `git branch -D` | 
| **gmu** | `git fetch origin -v; git fetch upstream -v; git merge upstream/master` | 
| **gll** | `git log --graph --pretty=oneline --abbrev-commit` | 
| **gg** | `git log --graph --pretty=format:'%C(bold)%h%Creset%C(magenta)%d%Creset %s %C(yellow)<%an> %C(cyan)(%cr)%Creset' --abbrev-commit --date=relative` | 
| **ggs** | `gg --stat` | 
| **gsl** | `git shortlog -sn` | 
| **gwc** | `git whatchanged` | 
| **gt** | `git tag` | 
| **gta** | `git tag -a` | 
| **gtd** | `git tag -d` | 
| **gtl** | `git tag -l` | 
| **gpatch** | `git format-patch -1` | 
| **gnew** | `git log HEAD@{1}..HEAD@{0}` | 
| **gcaa** | `git commit -a --amend -C HEAD` | 
| **ggui** | `git gui` | 
| **gcsam** | `git commit -S -am` | 
| **gst** | `git stash` | 
| **gstb** | `git stash branch` | 
| **gstd** | `git stash drop` | 
| **gstl** | `git stash list` | 
| **gstp** | `git stash pop` | 
| **ght** | `cd "$(git rev-parse --show-toplevel)"` | 
| **gu** | `git ls-files . --exclude-standard --others "$(git rev-parse --show-toplevel)"` | 
