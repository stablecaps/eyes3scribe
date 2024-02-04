# Milestones


## Things to do still
2. **CI/CD**
    1.  add create callgen or emerge to pre-commit hook
    2.  figure out branching strategy
    3.  link build status to badge
    4.  link test status to badge
    5.  do a proper release with new branch strategy
    6.  get github milestones setup
    7.  get github project & linked issues set up
    8.  automate project linking to prs release notes, etc
    ~~9. autogenerate template python repo (cookie-cutter)~~
    10. finish badges
    11. create repo avatar image

3. **Documentation**
    1. finish generating docstrings
    2. feed test data into docstrings (run tests on docstrings to check vailidity?)
    ~~3. add contributing.md~~
    4. create GHA to auto generate BASH documentation for users
    5. amend readme to take into account poetry & also list instructions for standalone binary


5. **Bug Fixes and Improvements**
    1. fix paths so it works with windows - use Pathlib
    ~~2. move undefined md pages to undef category~~
    ~~3. fix orphan single quote on value for about, param, etc~~
    4. Add features to jump to github code file from website
    5. List function calls across files?
    6. List function references across files?
    ~~7. Organise sidebar entries alphabetically~~
    ~~8. Check input config file for errors~~
    7. Finish manually written RST docs (broken links)
    ~~8. optionally put code generated stuff into a "reference" section~~
    ~~10. Capitalise title first letter~~
    12. embed hyperlinks in function index (currently a code block)
    13. think about putting function names in navbar? too messy?
    14. implement [gpt4docstrings](https://github.com/MichaelisTrofficus/gpt4docstrings)
    15. Use custom datasources and display in ui

6. **Mkdocs**
    1. fix mkdocs search
    ~~2. fix input yaml so it works better with arbitrary mkdocs yaml~~
    ~~3. allow arbitrary mkdocs themes to be used~~

8. module: bash auto-docs
    1. setup standalone app & test user execute experience
    2. integrate helpohelpo library
    3. write tests using better data sources
    4. test code against websites other than bash-it
    5. generate demo sites
    6. Add facility to auto-publish and update hosted github pages
    7. correct "(in ./docs_bash-it/docs/docshw/plugins/available/osx.plugin.bash)" to point at relative repo src file, not temp
    8. Get ref code working

9. module: python auto-docs
    1. Investigate best method for python documentation. pdoc, pydoc, etc. perhaps all sensible?
    2. write module with option to auto generate python code
    3. investigate using mkdocstrings
    4. investigate using subsets of callgraph for viz
    5. create GHA to auto generate python documentation for eyes2scribe repo3.
