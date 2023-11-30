#!/bin/bash

PROJECT_NAME="mkdocs_sys_bashrc"
SITE_NAME="Sys Bashrc"
SITE_URL="https://meatware.github.io/sys_bashrc"
SITE_AUTHOR="giri"
REPO_URL="https://github.com/meatware/sys_bashrc.git"
MD_SRC_DIR="gbm-docs"
mkdocs new $PROJECT_NAME

# TODO: sort out index.md (copy from REAME.md)
mkdir -p ./${MD_SRC_DIR}/
cp /home/bsgt/sys_bashrc/README.md ./${MD_SRC_DIR}/index.md


###################################################################
mkdir -p ${PROJECT_NAME}/docs/

cp -rf custom_assets/custom_css ${PROJECT_NAME}/docs/
#cp -rf custom_assets/custom_css ${PROJECT_NAME}/docs/
cp -rf ${MD_SRC_DIR}/* ${PROJECT_NAME}/docs/

###########################
cd $PROJECT_NAME/

cat<<EOF > mkdocs.yml
site_name: $SITE_NAME
site_url: $SITE_URL
repo_url: $REPO_URL
site_author: $SITE_AUTHOR
nav:
    - Home: index.md
EOF

###########################
cd docs
all_md_files=$(find . -name "*.md")
cd -


echo $all_md_files

##############################################
#for mymd in $all_md_files; do
for category_name in "aliases" "completion" "modules" "internal" ; do
cat<<BACON >> mkdocs.yml
    - ${category_name}:
BACON

    grouped_categ_info=$(echo "$all_md_files" | grep "$category_name" | sed 's|.md||g' | tr "/" " ")
    grouped_categ_pages=$(echo "$all_md_files" | grep "$category_name")

    for page_path in $grouped_categ_pages; do
    echo "z $page_path"
        page_name=$(echo "$page_path" | grep "$category_name" | sed 's|.md||g' | tr "/" " " | awk '{print $3}')
        echo "mymd: $page_name $page_path"
        #exit 1

cat<<CHEESE >> mkdocs.yml
        - ${page_name}: $page_path
CHEESE
        #exit 1
    done #
done


###########################
cat<<EOF3 >> mkdocs.yml
theme:
    name: windmill-dark
    navigation_depth: 5
    highlightjs: true
    hljs_languages:
        - bash
        - python
# markdown_extensions:
#   - codehilite:
#       guess_lang: false
#       use_pygments: true
#       noclasses: true
#       pygments_style: monokai
#   - toc:
#       toc_depth: 7

extra_css:
    - custom_css/extra.css
EOF3

###########################
mkdocs build

cd -
###################################################################