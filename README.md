# Eyes3Scribe

<div align="center">


[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eyes3scribe)]
[![Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/stablecaps/eyes3scribe/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/stablecaps/eyes3scribe/releases)
[![License](https://img.shields.io/github/license/stablecaps/eyes3scribe)](https://github.com/stablecaps/eyes3scribe/blob/master/LICENSE)
[![DeepSource](https://app.deepsource.com/gh/stablecaps/eyes3scribe.svg/?label=active+issues&show_trend=true&token=JveipNb_ClaKjk0YBBKrG-32)](https://app.deepsource.com/gh/stablecaps/eyes3scribe/)
[![DeepSource](https://app.deepsource.com/gh/stablecaps/eyes3scribe.svg/?label=resolved+issues&show_trend=true&token=JveipNb_ClaKjk0YBBKrG-32)](https://app.deepsource.com/gh/stablecaps/eyes3scribe/)
![Coverage Report](assets/images/coverage.svg)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/stablecaps/eyes3scribe/total)
[![Test eyes3scribe](https://github.com/stablecaps/eyes3scribe/actions/workflows/test-python-app.yml/badge.svg)](https://github.com/stablecaps/eyes3scribe/actions/workflows/test-python-app.yml)
[![repo-stats](https://github.com/stablecaps/eyes3scribe/actions/workflows/github-repo-stats.yml/badge.svg)](https://github.com/stablecaps/eyes3scribe/actions/workflows/github-repo-stats.yml)
[![Stable Version]](https://img.shields.io/pypi/v/eyes3scribe?label=stable)]
[![Build status](https://github.com/stablecaps/eyes3scribe/workflows/build/badge.svg?branch=master&event=push)](https://github.com/stablecaps/eyes3scribe/actions?query=workflow%3Abuild)


Automatically creates HTML documentation files for BASH/Shell source code using markdown & python mkdocs

</div>

# This is still a WIP!!!

## Overview
This project is a Python application that uses pip for package management. The main entry point for the application is gen_mkdocs_site.py.

**Features:**

0. Uses mkdocs to create websites with any mkdocs theme
1. Auto-generates BASH shell script documentation from src code that are marked with composure annotations.
2. Create alias tables from shell code
3. Preserves handwritten documentation (TBD)
4. Converts existing RST docs --> Markdown docs (TBD)
5. Auto-generates Python documentation from source code (TBD)


### Prerequisites
* Python 3.x
* poetry/pip

## Installation

```
git clone <repository_url>
cd <project_directory>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
# Run program to create mkdocs documentation site and serve it locally.
python gen_mkdocs_site.py --site-confname config/bash_it_site.yaml ---build-serve

# Show help
python gen_mkdocs_site.py --help
```
### Program options
1. `--site_confname` (str): The name of the site configuration.
2. `--build_serve` (bool): Whether to build and serve the local MkDocs site.
3. `--check_singlefile` (str): The path of a single shell source file to debug.
4. `--debug` (bool, optional): If True, debug information will be printed. Defaults to False.



## Program structure

**Auto-Documatix Callgraph:**
__(made with [PyDeps](https://github.com/thebjorn/pydeps?tab=readme-ov-file#usage))__
![PyDeps](images/launcher.svg)

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the Apache 2.0 License - see the LICENSE.md file for details.

## Things to do still
1. **Setup and Configuration**
    1. use poetry to setup package & standalone app
    2. ~~set up python test coverage (link with deep source)~~
    ~~3. set up pre-commit hooks~~
    4. add create callgen to pre-commit hook
    5. ~~protect master branch~~
    6. package for pip

2. **Documentation**
    1. finish generating docstrings
    2. feed test data into docstrings (run tests on docstrings to check vailidity?)
    3. add contributing.md
    4. create GHA to auto generate BASH documentation for users

3. **Testing**
    1. finish tests using better data sources

4. **Project Management**
    1. write scripts to autogenerate template python repo (cookie-cutter) & https://github.com/cjolowicz/cookiecutter-hypermodern-python?tab=readme-ov-file
    2. add badges
    3. create repo avatar image
    4. setup relewase pipeline

5. **Bug Fixes and Improvements**
    1. fix paths so it works with windows - use Pathlib
    ~~2. move undefined md pages to undef category~~
    ~~3. fix orphan single quote on value for about, param, etc~~
    4. Add features to jump to github code file from website
    5. List function calls across files?
    6. List function references across files?
    ~~7. Organise sidebar entries alphabetically~~
    ~~8. Check input config file for errors~~
    7. Process manually written docs
    ~~8. optionally put code generated stuff into a "reference" section~~
    9. Add facility to auto-publish and update hosted github pages
    ~~10. Capitalise title first letter~~
    11. correct "(in ./docs_bash-it/docs/docshw/plugins/available/osx.plugin.bash)" to point at relative repo src file, not temp
    12. embed hyperlinks in function index (currently a code block)
    13. think about putting function names in navbar? too messy?
    14. implement [gpt4docstrings](https://github.com/MichaelisTrofficus/gpt4docstrings)


6. **Mkdocs**
    1. fix mkdocs search
    ~~2. fix input yaml so it works better with arbitrary mkdocs yaml~~
    ~~3. allow arbitrary mkdocs themes to be used~~

1. **create python documentation website:**
    1. investigate using mkdocstrings
    2. investigate using subsets of callgraph for viz
    3. create GHA to auto generate python documentation for eyes2scribe repo

8. **Miscellaneous**
    1. amend readme to take into account poetry & also list instructions for standalone binary
    ~~2. rename site to eyes3scribe~~

## Not so Random info links

### Python call graphs
1. [Generating and using a Callgraph, in Python](https://cerfacs.fr/coop/pycallgraph)
2. [Quick & Simple Call Graphs in Python](https://medium.com/parkbee/quick-simple-call-graphs-in-python-eaa583d0e1b2)
    [pyan](https://github.com/Technologicat/pyan)
3. [Build a Call graph in python including modules and functions?](https://stackoverflow.com/questions/13963321/build-a-call-graph-in-python-including-modules-and-functions)
4. [What is a Call Graph? And How to Generate them Automatically](https://www.freecodecamp.org/news/how-to-automate-call-graph-creation/)
5. [Crabviz: a call graph generator for various programming languages](https://www.reddit.com/r/rust/comments/142is0h/crabviz_a_call_graph_generator_for_various/)
6. [**Insane**: Callgraphs with Ghidra, Pyhidra, and Jpype](https://clearbluejar.github.io/posts/callgraphs-with-ghidra-pyhidra-and-jpype/)


### Dependency analysis v2

1. https://github.com/glato/emerge
2. https://github.com/thebjorn/pydeps
3. https://www.python.org/success-stories/building-a-dependency-graph-of-our-python-codebase/


## Very first steps

### Initialize your code

1. Initialize `git` inside your repo:

```bash
cd eyes3scribe && git init
```

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

4. Run the codestyle:

```bash
make codestyle
```

5. Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/stablecaps/eyes3scribe.git
git push -u origin main
```

### Set up bots

- Set up [Dependabot](https://docs.github.com/en/github/administering-a-repository/enabling-and-disabling-version-updates#enabling-github-dependabot-version-updates) to ensure you have the latest dependencies.
- Set up [Stale bot](https://github.com/apps/stale) for automatic issue closing.

### Poetry

Want to know more about Poetry? Check [its documentation](https://python-poetry.org/docs/).

<details>
<summary>Details about Poetry</summary>
<p>

Poetry's [commands](https://python-poetry.org/docs/cli/#commands) are very intuitive and easy to learn, like:

- `poetry add numpy@latest`
- `poetry run pytest`
- `poetry publish --build`

etc
</p>
</details>

### Building and releasing your package

Building a new version of the application contains steps:

- Bump the version of your package `poetry version <version>`. You can pass the new version explicitly, or a rule such as `major`, `minor`, or `patch`. For more details, refer to the [Semantic Versions](https://semver.org/) standard.
- Make a commit to `GitHub`.
- Create a `GitHub release`.
- And... publish 🙂 `poetry publish --build`



## Installation

```bash
pip install -U eyes3scribe
```

or install with `Poetry`

```bash
poetry add eyes3scribe
```

Then you can run

```bash
eyes3scribe --help
```

or with `Poetry`:

```bash
poetry run eyes3scribe --help
```

### Makefile usage

[`Makefile`](https://github.com/stablecaps/eyes3scribe/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

</p>
</details>

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/stablecaps/eyes3scribe/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/stablecaps/eyes3scribe/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/stablecaps/eyes3scribe/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/stablecaps/eyes3scribe)](https://github.com/stablecaps/eyes3scribe/blob/master/LICENSE)

This project is licensed under the terms of the `Apache Software License 2.0` license. See [LICENSE](https://github.com/stablecaps/eyes3scribe/blob/master/LICENSE) for more details.

## 📃 Citation

```bibtex
@misc{eyes3scribe,
  author = {Stablecaps},
  title = {Automatically creates HTML documentation files for BASH/Shell source code using markdown & python mkdocs},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/stablecaps/eyes3scribe}}
}
```

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/stablecaps/stablecaps-pycookiecutter-template)

This project was generated with [`python-package-template`](https://github.com/stablecaps/stablecaps-pycookiecutter-template)
