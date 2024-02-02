# CHANGELOG



## v0.1.1 (2024-02-02)

### Ci

* ci(publish): change push branch to make debugging semver easier 7 ([`2fd09c4`](https://github.com/stablecaps/eyes3scribe/commit/2fd09c4b0ce7dc3d8f6d188958ac5c623e9286d5))

* ci(publish): change push branch to make debugging semver easier 6 ([`3746851`](https://github.com/stablecaps/eyes3scribe/commit/3746851a399f8d1e8ee9d3cb31b5c1a049522b05))

* ci(publish): change push branch to make debugging semver easier 5 ([`7e5fad2`](https://github.com/stablecaps/eyes3scribe/commit/7e5fad2023e23f3d2aeeb0025896f2014fb10d51))

* ci(publish): change push branch to make debugging semver easier 4 ([`e66b126`](https://github.com/stablecaps/eyes3scribe/commit/e66b1265ec15a3fbdc22d7da658f10764bc6c0c5))

* ci(publish): change push branch to make debugging semver easier 3 ([`df51210`](https://github.com/stablecaps/eyes3scribe/commit/df51210e30219b47a2a96ce6b1b683c27dbdce43))

* ci(publish): change push branch to make debugging semver easier 2 ([`20be519`](https://github.com/stablecaps/eyes3scribe/commit/20be519438697b51ff78411577e6e8f3300ff1f3))

* ci(publish): change push branch to make debugging semver easier ([`09d0add`](https://github.com/stablecaps/eyes3scribe/commit/09d0addd1625521e5a387c60222799451374ec32))

* ci: rm general build pipeline (#66)

* ci: rm general build pipeline

* ci: fix pr template wording to be less annoying ([`26a8aa3`](https://github.com/stablecaps/eyes3scribe/commit/26a8aa329d6a79ddb5c5fac6f2cc47a91793360e))

### Fix

* fix(toml): trying to publish to pypi 2 ([`5e60176`](https://github.com/stablecaps/eyes3scribe/commit/5e60176177b6f1ddcca2f6a7dcd627729546f286))

* fix(toml): trying to publish to pypi ([`262fa75`](https://github.com/stablecaps/eyes3scribe/commit/262fa7536d21da8181a0fe88c3c8f8fa5ecf354f))

* fix: classifiers ([`a123c45`](https://github.com/stablecaps/eyes3scribe/commit/a123c451465a7cdfaed2f870945f9c5f59260e17))

* fix: empty push 3 ([`a7384cd`](https://github.com/stablecaps/eyes3scribe/commit/a7384cd57e75bebc3d46ef827b559a91beecbbfc))

* fix: empty push 2 (#68) ([`98e629b`](https://github.com/stablecaps/eyes3scribe/commit/98e629b227d90b1b7e93374d165269fd09de22b6))

* fix: empty push (#67) ([`8551b1d`](https://github.com/stablecaps/eyes3scribe/commit/8551b1d95e2b5c96949d2acf55fb23c3f106d79f))

### Unknown

* 0.1.1 ([`c34033e`](https://github.com/stablecaps/eyes3scribe/commit/c34033ee89e35bd637eec89b518f55c7696a57f6))


## v0.1.0 (2024-02-01)

### Ci

* ci: add .deepsource.toml ([`1f96d32`](https://github.com/stablecaps/eyes3scribe/commit/1f96d32fc12cea24eeaaa8c5de62d67f089abd3e))

### Feature

* feat: add things from cookiecutter 3 ([`6baae97`](https://github.com/stablecaps/eyes3scribe/commit/6baae97fe82c5ef25110ebd338ca66c359745f9b))

* feat: add things from cookiecutter 2 ([`10ee2ce`](https://github.com/stablecaps/eyes3scribe/commit/10ee2ce66fb8223dd419373fdd91ade4f8b2761c))

* feat: some changes i forgot about ([`0a5250f`](https://github.com/stablecaps/eyes3scribe/commit/0a5250fd65827e057e69451f3444026ea4ea8de1))

### Fix

* fix(ci): test stage in publish gh-action ([`478643e`](https://github.com/stablecaps/eyes3scribe/commit/478643e19bddd7d58b6bd9c1b55359603420a1c4))

* fix: adjust makefile &amp; gh-actions ([`54d733c`](https://github.com/stablecaps/eyes3scribe/commit/54d733c131ca67828cf6a07ea205cbf6c744b5f6))

* fix: sort makefile ([`a55f79e`](https://github.com/stablecaps/eyes3scribe/commit/a55f79ee1b07e6e436be80269c43baa5efef776f))

* fix: Readme &amp; mode repo settings launcher ([`f528edf`](https://github.com/stablecaps/eyes3scribe/commit/f528edf136f73661c43abf2c25fa1c5454a43dcb))

### Refactor

* refactor: remove unused imports

An object has been imported but is not used anywhere in the file.
It should either be used or the import should be removed. ([`33ea748`](https://github.com/stablecaps/eyes3scribe/commit/33ea748779b6b99f1653803a20dbe9962ac0e3d4))

* refactor: fix dangerous default argument

Do not use a mutable like `list` or `dictionary` as a default value to an argument. Python’s default arguments are evaluated once when the function is defined. Using a mutable default argument and mutating it will mutate that object for all future calls to the function as well. ([`ac393f3`](https://github.com/stablecaps/eyes3scribe/commit/ac393f3fd3da9abdacc451753dbc9e5f47b94456))

* refactor: use identity check for comparison to a singleton

Comparisons to the singleton objects, like `True`, `False`, and `None`, should be done with identity, not equality. Use `is` or `is not`. ([`bf1658d`](https://github.com/stablecaps/eyes3scribe/commit/bf1658d204b14961ad517cf0d1fd34771ee20e64))

* refactor: remove blank lines after docstring

There shouldn&#39;t be any blank lines after the function docstring.
Remove the blank lines to fix this issue. ([`a355152`](https://github.com/stablecaps/eyes3scribe/commit/a3551523dabee446dbe0fb7af3fd0e86309a68a5))

### Style

* style: format code with Black and isort

This commit fixes the style issues introduced in 33ea748 according to the output
from Black and isort.

Details: https://github.com/stablecaps/bash-auto-doc/pull/8 ([`c1c0fa0`](https://github.com/stablecaps/eyes3scribe/commit/c1c0fa0b8897ebe1acef0bde214ca759d65a1457))

* style: format code with Black and isort

This commit fixes the style issues introduced in cf892d4 according to the output
from Black and isort.

Details: None ([`236a786`](https://github.com/stablecaps/eyes3scribe/commit/236a786ac889cb6bd08c66a06f41b63c139fe194))

* style: format code with Black and isort

This commit fixes the style issues introduced in bf1658d according to the output
from Black and isort.

Details: https://github.com/stablecaps/bash-auto-documatix/pull/3 ([`5abb678`](https://github.com/stablecaps/eyes3scribe/commit/5abb678d311100767b258f6d4ef20534d5abeb83))

* style: format code with Black and isort

This commit fixes the style issues introduced in 517c15e according to the output
from Black and isort.

Details: None ([`0ae7ee7`](https://github.com/stablecaps/eyes3scribe/commit/0ae7ee7009b34eaba2b1549f1ea891e3ad9bf209))

### Unknown

* add conventional commit check ([`522e080`](https://github.com/stablecaps/eyes3scribe/commit/522e0802ca1c62d725c185f07cd2b8171e2d18ba))

* tidy up ([`8c400b9`](https://github.com/stablecaps/eyes3scribe/commit/8c400b98eaf058672b88eee10b863e9a5264ffb1))

* Feature/get this to alpha (#15)

* got this broadly operational
* links in md files now point to correct place
* some loose ends tied up
* refactoring

* feat: sync helpohelpo to avoid issues

* feat: sync helpohelpo to avoid issues -2 now synched

* wip

* got relative toclinks mostly working

* refactor: autofix issues in 10 files

Resolved issues in the following files with DeepSource Autofix:
1. eyes3scribe/gen_handwritten_docs.py
2. eyes3scribe/gen_pynavbar_dict.py
3. eyes3scribe/helpo/hdatetime.py
4. eyes3scribe/helpo/old/hfile.py
5. eyes3scribe/helpo/old/hstrops.py
6. eyes3scribe/helpo/old/hsubprocess.py
7. eyes3scribe/models/filepath_datahandler.py
8. eyes3scribe/models/rst2md_datahandler.py
9. eyes3scribe/setup_docs_project.py
10. launcher.py

* style: format code with Black and isort

This commit fixes the style issues introduced in 44ec7a8 according to the output
from Black and isort.

Details: https://github.com/stablecaps/eyes3scribe/pull/15

* refactor: autofix issues in 1 file

Resolved issues in eyes3scribe/helpo/old/hfile.py with DeepSource Autofix

---------

Co-authored-by: deepsource-autofix[bot] &lt;62050782+deepsource-autofix[bot]@users.noreply.github.com&gt; ([`6ed31ef`](https://github.com/stablecaps/eyes3scribe/commit/6ed31efd60c394758278314f389efe8e8dd669e5))

* Merge pull request #14 from stablecaps/feature/refactor-code-structure-part2

feat: some changes i forgot about ([`029c6d6`](https://github.com/stablecaps/eyes3scribe/commit/029c6d659f7563fc27307ec83ea5429742b67a06))

* Merge pull request #13 from stablecaps/feature/refactor-code-structure

Feature/refactor code structure ([`78929e5`](https://github.com/stablecaps/eyes3scribe/commit/78929e5c7551dc03aa3286e7888986b143f4f5bd))

* tidy scrap code ([`7ace7fd`](https://github.com/stablecaps/eyes3scribe/commit/7ace7fd15eef6e5998081f50d2eb11536f06e533))

* fix some pr comments 2 ([`cfa7c62`](https://github.com/stablecaps/eyes3scribe/commit/cfa7c62b6dabb2f0e740bc3c2c3f69d6276a1a55))

* fix some pr comments ([`cc395e4`](https://github.com/stablecaps/eyes3scribe/commit/cc395e4fe764456de90edd72de684407d79bf212))

* rm uneccesary imports ([`400480f`](https://github.com/stablecaps/eyes3scribe/commit/400480f8ee52e9ed118e73f8bdf08d2b2354b446))

* uncouple rst 2 mod modules ([`4e2f7cc`](https://github.com/stablecaps/eyes3scribe/commit/4e2f7cca3650b5d42547c692623f1d1b0d8bfc8a))

* update eyes3scribe name in src ([`d0d9d0c`](https://github.com/stablecaps/eyes3scribe/commit/d0d9d0caea0c4e8140aeac748d984f56b296650f))

* More structural changes ([`2515285`](https://github.com/stablecaps/eyes3scribe/commit/25152859e2e43894486394f6de91a46c6da6a052))

* rename repo ([`2770d0f`](https://github.com/stablecaps/eyes3scribe/commit/2770d0fc08eb9939d963f6e3b1b5ed313e9475b2))

* deconvolute rst2 md via pipeline 1 ([`161868d`](https://github.com/stablecaps/eyes3scribe/commit/161868d35ebaddf9cb59caaa6714f5467efdbe91))

* horrorshow navbar restructure 5 ([`cd1a975`](https://github.com/stablecaps/eyes3scribe/commit/cd1a9755511baaea4f782bc91975221223935c62))

* horrorshow navbar restructure 4 ([`72dbfc8`](https://github.com/stablecaps/eyes3scribe/commit/72dbfc8c805508693af545d883153195c2ad877e))

* horrorshow navbar restructure 3 ([`3eb23d8`](https://github.com/stablecaps/eyes3scribe/commit/3eb23d88bb32393c3624887da23901e91e70f942))

* horrorshow navbar restructure 2 ([`e6dc0f6`](https://github.com/stablecaps/eyes3scribe/commit/e6dc0f64c797eed50bdabb26307616488cf21053))

* horrorshow navbar restructure 1 ([`ced0f45`](https://github.com/stablecaps/eyes3scribe/commit/ced0f4539213d2e7e26594e2a4a9d75668d2144f))

* wip ([`c854c32`](https://github.com/stablecaps/eyes3scribe/commit/c854c32c3e5d91bc207aed21c4cf5c46f7f805d3))

* refactor some funmc names and functionalise some code ([`69ef8a3`](https://github.com/stablecaps/eyes3scribe/commit/69ef8a3b158a3c5250bb0056b58f9e44c468b095))

* split setup intoi new class SetupDocsProject 2 ([`165288e`](https://github.com/stablecaps/eyes3scribe/commit/165288e7b737b76184e7aaf5e69b16ad69439670))

* split setup intoi new class SetupDocsProject ([`4af2537`](https://github.com/stablecaps/eyes3scribe/commit/4af25370072d30dc9a299930e47ba2d9fdc62f0a))

* add create emerge dependency graph script &amp; config ([`9e43c87`](https://github.com/stablecaps/eyes3scribe/commit/9e43c871f7bc1ce9dbad91cdc1da1296ad277437))

* move config to a seperate module &amp; use dotmap for dot notation 4 ([`b5144e3`](https://github.com/stablecaps/eyes3scribe/commit/b5144e3e2600c993dbfffd0ffdd51cc8965137bc))

* move config to a seperate module &amp; use dotmap for dot notation 3 ([`85f3392`](https://github.com/stablecaps/eyes3scribe/commit/85f33925a6707d421bed08e372ce6c9f2eebccfa))

* move config to a seperate module &amp; use dotmap for dot notation 2 ([`20d4724`](https://github.com/stablecaps/eyes3scribe/commit/20d472443f8ce763b933d6f42468eb74f534ebe1))

* move config to a seperate module &amp; use dotmap for dot notatiojn ([`db96662`](https://github.com/stablecaps/eyes3scribe/commit/db9666223a09f26cc389eaae94bad8d901a901df))

* Merge pull request #12 from stablecaps/bugfix/fix-remaining-broken-links

Bugfix/fix remaining broken links ([`ebc6ae4`](https://github.com/stablecaps/eyes3scribe/commit/ebc6ae41f1f08acd01ffe00d47c416d489385c97))

* getting messy paths fixed 2 ([`82e89d2`](https://github.com/stablecaps/eyes3scribe/commit/82e89d249c3f412ffa269e02a20852a33245a5f4))

* Merge pull request #11 from stablecaps/codesee-arch-diagram-workflow-1704340277760

Install the CodeSee workflow. ([`2420a55`](https://github.com/stablecaps/eyes3scribe/commit/2420a551015ce7768b075d930c36d0a1cd75ef3f))

* Install the CodeSee workflow. Learn more at https://docs.codesee.io ([`a3c3a8a`](https://github.com/stablecaps/eyes3scribe/commit/a3c3a8a4d03ccf7af0e88b02931260b05a74fb04))

* getting messy paths fixed 1 ([`b478b4f`](https://github.com/stablecaps/eyes3scribe/commit/b478b4f4746946a99c427347189daf3877e3dbe2))

* Merge pull request #10 from stablecaps/feature/process-rst-image-blocks

Feature/process rst image blocks ([`0db664e`](https://github.com/stablecaps/eyes3scribe/commit/0db664e5541ec6030096393938b5a0c48ba6f487))

* get rst2md conversion of hosted image sorted 3 ([`183cc68`](https://github.com/stablecaps/eyes3scribe/commit/183cc6805125a57e996bdeb68eec987087592ed6))

* get rst2md conversion of hosted image sorted 2 ([`2fd3e8f`](https://github.com/stablecaps/eyes3scribe/commit/2fd3e8fc884d08e1346e9515563b77f81d3df098))

* get rst2md conversion of hosted image sorted 1 ([`75f0185`](https://github.com/stablecaps/eyes3scribe/commit/75f0185bb77fe20357743e8209d427e1634475f9))

* refactor triple colon class after some tipple ([`4f31d86`](https://github.com/stablecaps/eyes3scribe/commit/4f31d861c95f556f4687b20c574e1626f35ae3b0))

* admonitions part 2 - baic implementation sorted ([`ff57e45`](https://github.com/stablecaps/eyes3scribe/commit/ff57e45ab0d27e563b27ab6c19511528fdbf0c5e))

* get hanging hwdocs files in mkdocs.yaml 1 ([`2805c12`](https://github.com/stablecaps/eyes3scribe/commit/2805c121da3e0a475c7ad093f10dd1e627ebaa48))

* admonitions part 1 ([`cb1f30b`](https://github.com/stablecaps/eyes3scribe/commit/cb1f30b0b23e9181ce5a575ed81dc7600d0c5d93))

* switch back to rst2myst ([`bf08dbc`](https://github.com/stablecaps/eyes3scribe/commit/bf08dbc620058b8b6929ae2d53704640bb772d39))

* switch from rst2myst to pandoc 1 ([`ba60641`](https://github.com/stablecaps/eyes3scribe/commit/ba60641c21b8c71be0f6766a171170f5d7c57964))

* switch to pandoc from rst2myst ([`763d920`](https://github.com/stablecaps/eyes3scribe/commit/763d9201523c0a1a0da73814ebe246f8a41784fb))

* got anchor links to section headings mostly working (i think) ([`c0c2d4e`](https://github.com/stablecaps/eyes3scribe/commit/c0c2d4e62bbdea88bbbdde63a00da90f31117bc3))

* Merge pull request #8 from stablecaps/deepsource-autofix-933dc139

refactor: remove unused imports ([`a8c26be`](https://github.com/stablecaps/eyes3scribe/commit/a8c26beeefc5da3132b7a85d1d479555a65a493a))

* generalise &amp; tidy up 1 ([`0bf1ba2`](https://github.com/stablecaps/eyes3scribe/commit/0bf1ba22f818ce44a591dae84137e8f9daad13fb))

* anchor links wip 3 ([`fda1fda`](https://github.com/stablecaps/eyes3scribe/commit/fda1fda2d52888af0a82cae0453a78a415b239e2))

* anchor links wip 2 ([`e926a86`](https://github.com/stablecaps/eyes3scribe/commit/e926a86c4a2e768456a26a3f682176f845b2da6b))

* anchor links wip 1 ([`f93f2ec`](https://github.com/stablecaps/eyes3scribe/commit/f93f2ec62b9a28e15b361b87b47a25a99566f2d5))

* get module MdToc2YamlProcessor to process hwdocs sorted in principal 4 ([`409e382`](https://github.com/stablecaps/eyes3scribe/commit/409e382d976da4531d7393f8d5765d06192cf645))

* get module MdToc2YamlProcessor to process hwdocs sorted in principal 3 ([`c04d08a`](https://github.com/stablecaps/eyes3scribe/commit/c04d08aed88e8bc600e9850a6a72046edcaddf25))

* get module MdToc2YamlProcessor to process hwdocs sorted in principal 2 ([`725e6f1`](https://github.com/stablecaps/eyes3scribe/commit/725e6f1636cfdbafd8f9171357a9f1c50a10bc57))

* get module MdToc2YamlProcessor to process hwdocs sorted in principal ([`54f6187`](https://github.com/stablecaps/eyes3scribe/commit/54f6187262145309e29a0fdf1ad4fc2c85def8f2))

* incorporate rst to md file converter - still need to sort out paths - very messy ([`3e1ceac`](https://github.com/stablecaps/eyes3scribe/commit/3e1ceac10a0e6f1a9aa4f2072e9bb88aabe4f62a))

* make progress on replacing rst --&gt; md {ref} links 3 - WIP ([`0eed812`](https://github.com/stablecaps/eyes3scribe/commit/0eed81257ecfc2d4049e81a3e657ad66e63c84f5))

* make progress on replacing rst --&gt; md {ref} links 2 ([`2557ebd`](https://github.com/stablecaps/eyes3scribe/commit/2557ebdcb4616a86ba0e9e9059ecaf74fa77a81b))

* update images/callgraph.png ([`ac4835b`](https://github.com/stablecaps/eyes3scribe/commit/ac4835bec6809e9e7154f76c921e9564a94ace25))

* update readme 3 ([`6525ca4`](https://github.com/stablecaps/eyes3scribe/commit/6525ca4b6f7d6a5b675ecd580e5dac8648102c3c))

* update readme 2 ([`488b57d`](https://github.com/stablecaps/eyes3scribe/commit/488b57d76cf5e97c04e27433f0bf8198171c0149))

* update readme ([`84b3fd9`](https://github.com/stablecaps/eyes3scribe/commit/84b3fd99c77a642a90005da9d1a577c3d2f1bd81))

* make progress on replaing rst --&gt; md {ref} links 1 ([`ace0643`](https://github.com/stablecaps/eyes3scribe/commit/ace064391495457a082fc6ced02d648d2fe733f1))

* make progress on replaing rst --&gt; md TOC 2 ([`ba708a7`](https://github.com/stablecaps/eyes3scribe/commit/ba708a719316a346e85603e4b8b23661babb048e))

* make progress on replaing rst --&gt; md TOC 1 ([`4b28908`](https://github.com/stablecaps/eyes3scribe/commit/4b28908e3d6e51cb70c2b6e15b77891a6557c883))

* work more on hwdocs &amp; start moving towards recraeting hwdocs in their own dir. Also refactoring for a better tomorrow.. ([`8b67a1f`](https://github.com/stablecaps/eyes3scribe/commit/8b67a1f6cf0e1f7e9bf772b8397dc85b9a878c58))

* update images/callgraph.png ([`f4317bb`](https://github.com/stablecaps/eyes3scribe/commit/f4317bbd252c966f7f1beb013d138e293fe76349))

* implement convert rst files 2md &amp; get gwdocs roughly added to nav ([`ec5438a`](https://github.com/stablecaps/eyes3scribe/commit/ec5438a21af76ddfd98104be68f6d53586e37c69))

* refactoring ([`fbf81d3`](https://github.com/stablecaps/eyes3scribe/commit/fbf81d3f72eefd3d189af3a359829c1154bf149f))

* use dataclass to better pass function data from srcfiles around ([`beb29a4`](https://github.com/stablecaps/eyes3scribe/commit/beb29a4e8b4805e35799b954cc1ef65a454ac28c))

* use dataclass to better pass paths around 2 ([`d74e1f5`](https://github.com/stablecaps/eyes3scribe/commit/d74e1f52cb1b40ec5a9f97c28cfbb0cf8318a0e1))

* use dataclass to better pass paths around 1 ([`07622f3`](https://github.com/stablecaps/eyes3scribe/commit/07622f3a5266777e8e1814bebffae9eb4bab7e2d))

* Fix function parameter formatting, fix orphan quote issue, capitalise title first letter and update docs. hwdocs still broken ([`bf47e6c`](https://github.com/stablecaps/eyes3scribe/commit/bf47e6c768adac48ec9bf7df6a7175fd332fe69f))

* broken wip getting hw docs working ([`501698f`](https://github.com/stablecaps/eyes3scribe/commit/501698f9abd17ccffd2a0d8d7b5fbe9a67207465))

* linting &amp; regen images/callgraph.png ([`a6b91e1`](https://github.com/stablecaps/eyes3scribe/commit/a6b91e16f7cf8bade0768bfdf6c85ec1d6c3e8cf))

* Refactor a shed load of things, and Update bash_it_site.yaml ([`e600bcf`](https://github.com/stablecaps/eyes3scribe/commit/e600bcfd451c45e128ffb6fd936b88fecd91f1ff))

* Update project tasks, refactor gen mkdocs &amp;  abs/rel file path functions ([`ac04a1f`](https://github.com/stablecaps/eyes3scribe/commit/ac04a1f3a4e05535bbd7d5146428d3bf9c2f4c94))

* Add ability to nest code documentation under nav_codedocs_as_ref_or_main in nav bar ([`b4a2c3d`](https://github.com/stablecaps/eyes3scribe/commit/b4a2c3ddefef27f61c32bf030c3110bffbcb07d7))

* Refactor function dependency processing, muck up with it&#39;s tests and add check config ([`57989ce`](https://github.com/stablecaps/eyes3scribe/commit/57989ceecd4494a304a70343b5a0f7296bd5d7ef))

* Update pyproject.toml and README.md files ([`91c2e3a`](https://github.com/stablecaps/eyes3scribe/commit/91c2e3a59ea52c38848918232c3ca8ef6ed0685f))

* sort out function_dependecy_processor (mostly) ([`30e102b`](https://github.com/stablecaps/eyes3scribe/commit/30e102b78bf2eb9f620f73b79a7c1b60f9671c1f))

* add pre-commit hooks 2 &amp; fix tests ([`6efae85`](https://github.com/stablecaps/eyes3scribe/commit/6efae8530b88487c6c50eb40797adc991fdad1c0))

* add pre-commit hooks 1 ([`791d3c3`](https://github.com/stablecaps/eyes3scribe/commit/791d3c392ea523c33b7f21b15d21ee49d4bb9248))

* sort out alphabetical listing of sidebar ([`38d6eb4`](https://github.com/stablecaps/eyes3scribe/commit/38d6eb4e4d32a350948309f4c9b89fa61bc0ec46))

* sort out undef for functions &amp; aliases with no data ([`7d912c3`](https://github.com/stablecaps/eyes3scribe/commit/7d912c370d085a5bf55b1992a97ac48a88b59aa5))

* fix function output ([`7dbea72`](https://github.com/stablecaps/eyes3scribe/commit/7dbea72cd7335145d0ead30a9d4e0690d7ef7d0a))

* refactor names, update things to do and ebable better mkdocs yaml config intergration ([`db237d8`](https://github.com/stablecaps/eyes3scribe/commit/db237d8ddbcb938b9f78d8f8a2866d22fa763dde))

* add poetry &amp; add some docstrings ([`d8dc48a`](https://github.com/stablecaps/eyes3scribe/commit/d8dc48a02235d22f76bb897af0176ea6fa5ab429))

* broken badges to work on laters ([`4b535a7`](https://github.com/stablecaps/eyes3scribe/commit/4b535a7b700d0046ea96d9fcfc5e1d49cc6dddbf))

* add some deepsoure badges ([`8988dae`](https://github.com/stablecaps/eyes3scribe/commit/8988daeed4a4f24b52e762279a5415a53b1d266f))

* seetup deep source coverage analysin in GHA 3 ([`2c0ec4c`](https://github.com/stablecaps/eyes3scribe/commit/2c0ec4c890b2352a709a210ae0efeca40cf21c85))

* seetup deep source coverage analysin in GHA 2 ([`942cc68`](https://github.com/stablecaps/eyes3scribe/commit/942cc682665bdc5660e5662c0144b7f8b50f4bb7))

* seetup deep source coverage analysin in GHA ([`8e89c5d`](https://github.com/stablecaps/eyes3scribe/commit/8e89c5dedbd817a5988436e61334d5d13cd2b4e8))

* make test matrix less insane ([`00c31b9`](https://github.com/stablecaps/eyes3scribe/commit/00c31b995f68a3d80f1ee05ea0c3872c28357c47))

* Create test-python-app.yml ([`3f1f73e`](https://github.com/stablecaps/eyes3scribe/commit/3f1f73e3a09787b324f4e206dec2eaf4efb352b9))

* more test &amp; ci changes ([`f47858e`](https://github.com/stablecaps/eyes3scribe/commit/f47858e8ba11208b3a24f3498ef7d1aa55313902))

* linting &amp; docs ([`66c540a`](https://github.com/stablecaps/eyes3scribe/commit/66c540a318e210630ead56bb4dd2500b52dbed59))

* rename app &amp; restructure folder names ([`203405c`](https://github.com/stablecaps/eyes3scribe/commit/203405c135c9e88e8af47bff4702e5c1d4bf7f80))

* add dependencies to poetry ([`31673fd`](https://github.com/stablecaps/eyes3scribe/commit/31673fda822e6a478712fd5d1cd336747c47762b))

* add poetry, update documenation &amp; readd __init__.py ([`8d904c9`](https://github.com/stablecaps/eyes3scribe/commit/8d904c9bb5ee2993c579825f23708eeab3318eba))

* add basic documenation 6 ([`073d8ab`](https://github.com/stablecaps/eyes3scribe/commit/073d8abc7ce2dab486051d1b422bea921bed5d73))

* add basic documenation 5 gpocb ([`2135102`](https://github.com/stablecaps/eyes3scribe/commit/2135102e2305c4791ab0ef5b292fba28a8361636))

* add basic documenation 4 ([`a42155e`](https://github.com/stablecaps/eyes3scribe/commit/a42155e8e5bbc69ff76be997d84b324a01a295c3))

* add basic documenation 3 ([`1373452`](https://github.com/stablecaps/eyes3scribe/commit/1373452610085448a513ca9f908857f0caf0a1f0))

* add basic documenation 2 ([`183c010`](https://github.com/stablecaps/eyes3scribe/commit/183c0101a3354f4fded842e824909bd190eaab2c))

* add basic documenation ([`8a78214`](https://github.com/stablecaps/eyes3scribe/commit/8a782147cc169fa1c9d7f28674a54306eca88158))

* Merge branch &#39;master&#39; of github.com:stablecaps/bash-auto-documatix ([`9a97b34`](https://github.com/stablecaps/eyes3scribe/commit/9a97b3491525df80b11e70e2af14b822ee8a5a4d))

* more stuff ([`2278918`](https://github.com/stablecaps/eyes3scribe/commit/2278918b5cd7a5b35077737bbbec6b6d877034fe))

* Merge pull request #6 from stablecaps/deepsource-transform-847d7f6f

style: format code with Black and isort ([`2027228`](https://github.com/stablecaps/eyes3scribe/commit/20272287302b5cc4839fa9f8b5ab39b21878a9d7))

* stuff after a bottle of wine ([`865e076`](https://github.com/stablecaps/eyes3scribe/commit/865e07661a787c584255f894e99b40f08aea1647))

* fix writing to md file &amp; add a debug mode ([`f2a2ad0`](https://github.com/stablecaps/eyes3scribe/commit/f2a2ad0d29f4375a1fac526b8e665178f88ca063))

* fix glob patterns --&gt; sidebar menu enrtries &amp; add ability to build &amp; serve mkdocs locally ([`69c848e`](https://github.com/stablecaps/eyes3scribe/commit/69c848eaac70ef04636755eb0c45aad1e71ab18b))

* add bash-it config to generalise program 2 ([`b224cd5`](https://github.com/stablecaps/eyes3scribe/commit/b224cd53e3dc696b2db6371648e2ad5c80cfeb98))

* add bash-it config to generalise program ([`f9190e0`](https://github.com/stablecaps/eyes3scribe/commit/f9190e01b97fbf7afd4341c1a0440409fe2dbf81))

* disable deepsource test coverage for now ([`cf892d4`](https://github.com/stablecaps/eyes3scribe/commit/cf892d4aea549315f989190aa6d92d62f087f87a))

* Merge pull request #4 from stablecaps/deepsource-autofix-dc72e6a9

refactor: fix dangerous default argument ([`007b222`](https://github.com/stablecaps/eyes3scribe/commit/007b2229c739e3a2719c40c692b987c994d93153))

* Merge branch &#39;master&#39; into deepsource-autofix-dc72e6a9 ([`4b07c61`](https://github.com/stablecaps/eyes3scribe/commit/4b07c619ba28b0a4a2290d6dca0eb05e0196d3ba))

* update deepsource checks ([`6cf7113`](https://github.com/stablecaps/eyes3scribe/commit/6cf7113463e25a48996a6bed8ffd7293b21960d4))

* Merge pull request #3 from stablecaps/deepsource-autofix-32b6015b

refactor: use identity check for comparison to a singleton ([`cce5fce`](https://github.com/stablecaps/eyes3scribe/commit/cce5fce0b063407bea0aa0636306e7680fbd5efd))

* Merge pull request #2 from stablecaps/deepsource-autofix-bc9b13c9

refactor: remove blank lines after docstring ([`b9d95ff`](https://github.com/stablecaps/eyes3scribe/commit/b9d95ff84bfa80303db0bdebd79e411dd77ab292))

* Merge pull request #1 from stablecaps/deepsource-transform-a3bbb371

style: format code with Black and isort ([`1337af4`](https://github.com/stablecaps/eyes3scribe/commit/1337af4d6e66b5a8e7d692a4f8ea02f034a8e408))

* more linting 3 ([`781ab2c`](https://github.com/stablecaps/eyes3scribe/commit/781ab2cd6bda96a4988c45e053ede86deb6954b2))

* Merge branch &#39;master&#39; of github.com:stablecaps/bash-auto-documatix ([`517c15e`](https://github.com/stablecaps/eyes3scribe/commit/517c15e05ac71865896496f02f28cf6cf558d618))

* more linting 2 ([`5a622e4`](https://github.com/stablecaps/eyes3scribe/commit/5a622e4be5384dabfd72676434a7ed2162157da0))

* more linting ([`9594b15`](https://github.com/stablecaps/eyes3scribe/commit/9594b15e3e30eed6e7e26692743cc30ecc739fab))

* more linting ([`fab9de4`](https://github.com/stablecaps/eyes3scribe/commit/fab9de4c4045326ad40fa1607e8c75574df6b6d3))

* linting and adding some tests ([`7827ded`](https://github.com/stablecaps/eyes3scribe/commit/7827ded1b06be9ec1b0879f3bbff5d9eba19ec2b))

* more refactoring and added tests ([`981dfcd`](https://github.com/stablecaps/eyes3scribe/commit/981dfcddb94471008da1966aa73538d762735957))

* lint, refactor &amp; fix doc &amp; html location ([`8870326`](https://github.com/stablecaps/eyes3scribe/commit/8870326e05bdb78070126c2106aa484d2464590a))

* rm old dirs ([`4ab23f6`](https://github.com/stablecaps/eyes3scribe/commit/4ab23f6385d5c65d8d2fc2c28e2df6bc28af4a7e))

* remove test files from repo ([`83fa71d`](https://github.com/stablecaps/eyes3scribe/commit/83fa71dc9a5a8dc2b72788b2761108558bd95943))

* whole load of stuff ([`322e332`](https://github.com/stablecaps/eyes3scribe/commit/322e332659139d553ad01a9d8fa80a5f58383321))

* Add github-repo-stats workflow ([`1a42f04`](https://github.com/stablecaps/eyes3scribe/commit/1a42f04774045a544a28536c0d5583fb35422ccf))

* start replacing bash scripts to run python 3 ([`7a2715d`](https://github.com/stablecaps/eyes3scribe/commit/7a2715d9d6eb00464435d8c7a6b1f9d15bf9c275))

* start replacing bash scripts to run python 2 ([`8ce18c3`](https://github.com/stablecaps/eyes3scribe/commit/8ce18c32c7cf91ae50515eaa795723c74e5dd795))

* start replacing bash scripts to run python 1 ([`8b8e27c`](https://github.com/stablecaps/eyes3scribe/commit/8b8e27c6e39048da8579202e8c6ae80861c16dc6))

* some sensible module restructuring 2 ([`5e60700`](https://github.com/stablecaps/eyes3scribe/commit/5e60700a13b4d66d22bd14e1d89fc88c91532801))

* some sensible module restructuring ([`a2e3ab5`](https://github.com/stablecaps/eyes3scribe/commit/a2e3ab5d2f5de9579f0ac3313800753621d5ac70))

* code from years ago in a horrible state - cleaning 1 ([`65b5454`](https://github.com/stablecaps/eyes3scribe/commit/65b5454f1a4b5da6f96d2026b992e0d2526a3682))

* Add README.md ([`bb8658f`](https://github.com/stablecaps/eyes3scribe/commit/bb8658febfa7b9099a6c539995134f6a6f283d01))
