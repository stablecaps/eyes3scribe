import logging

from eyes3scribe.helpo import hcollections, hfile

LOG = logging.getLogger(__name__)


class SetupDocsProject:
    def __init__(self, cnf, check_singlefile):
        self.cnf = cnf
        self.check_singlefile = check_singlefile

    def copy_starting_files(self):
        """
        Set up the docs project by copying shell source files and custom CSS
        to the project directory.
        """
        hfile.rmdir_if_exists(target=self.cnf.project_docs_dir)
        hfile.mkdir_if_notexists(target=self.cnf.project_docs_dir)

        ### make undefined category directory
        hfile.mkdir_if_notexists(target=self.cnf.undef_category_dir)
        hfile.mkdir_if_notexists(target=self.cnf.undef_category_dir_hwdocs)

        print(self.cnf.shell_srcdir, self.cnf.project_docs_dir)
        hfile.copy_dir(
            source=self.cnf.shell_srcdir,
            target=self.cnf.project_docs_dir,
            symlinks=True,
            dirs_exist_ok=True,
        )
        hfile.copy_dir(
            source="custom_assets/custom_css",
            target=self.cnf.project_css_dir,
        )

        # TODO: sort this out later
        LOG.info("Copying additional markdown files")
        # for mdsrc, mddest in self.classmethod"additional_mdfiles").items():
        #     hfile.copy_file(source=mdsrc, target=f"{self.cnf.project_docs_dir}/{mddest}")

        if self.cnf.handwritten_docs_indir:
            hfile.copy_dir(
                source=self.cnf.handwritten_docs_indir,
                target=self.cnf.handwritten_docs_outdir,
            )

    def process_handwritten_docs(self):
        LOG.info("Processing handwritten doc files")
        hwdocs_rpaths = hfile.multiglob_dir_search(
            search_path=self.cnf.handwritten_docs_outdir,
            glob_patt_list=self.cnf.docs_glob_patterns,
        )
        LOG.debug("hwdocs_rpaths: %s", hwdocs_rpaths)

        # TODO: move exclusion_patterns_src into class init
        strict_exclusion_patterns_docs = [
            patt for patt in self.cnf.exclusion_patterns_docs
        ]
        LOG.debug("strict_exclusion_patterns_docs: %s", strict_exclusion_patterns_docs)

        # clean_hwdocs_rpaths = hfile.filter_paths_excluding_patterns(
        #     path_list=hwdocs_rpaths,
        #     exclusion_patterns_src=strict_exclusion_patterns_docs,
        # )

        clean_hwdocs_rpaths = hcollections.clean_list_via_rm_patts(
            input_list=hwdocs_rpaths, rm_patts=hwdocs_rpaths
        )
        LOG.debug("clean_hwdocs_rpaths: %s", clean_hwdocs_rpaths)
        # sys.exit(42)

        # self.mkdocs_add_srcdocs_to_nav(self, catname_2mdfile_dict)

        return clean_hwdocs_rpaths

    def process_shell_source_files(self):
        src_absolute_path_list = hfile.multiglob_dir_search(
            search_path=self.cnf.project_docs_dir,
            glob_patt_list=self.cnf.shell_glob_patterns,
        )

        LOG.debug("src_absolute_path_list: %s", src_absolute_path_list)

        # TODO: move exclusion_patterns_src into class init
        strict_exclusion_patterns_src = [
            f"/{patt}/" for patt in self.cnf.exclusion_patterns_src
        ]
        LOG.debug("strict_exclusion_patterns_src: %s", strict_exclusion_patterns_src)

        srcfiles_rpath = hfile.replace_substr_in_paths(
            input_paths=src_absolute_path_list,
            replace_path=self.cnf.program_root_dir,
        )
        LOG.info("srcfiles_rpath: %s", srcfiles_rpath)

        # clean_srcfiles_rpaths = hfile.filter_paths_excluding_patterns(
        #     path_list=srcfiles_rpath,
        #     exclusion_patterns_src=strict_exclusion_patterns_src,
        # )
        clean_srcfiles_rpaths = hcollections.clean_list_via_rm_patts(
            input_list=srcfiles_rpath, rm_patts=strict_exclusion_patterns_src
        )
        LOG.debug("clean_srcfiles_rpaths: %s", clean_srcfiles_rpaths)

        return clean_srcfiles_rpaths

    def main(self):
        self.copy_starting_files()

        clean_hwdocs_rpaths = None
        if self.cnf.handwritten_docs_indir:
            clean_hwdocs_rpaths = self.process_handwritten_docs()

        LOG.info("Processing shell source files")
        clean_srcfiles_rpaths = None
        if self.check_singlefile is None:
            clean_srcfiles_rpaths = self.process_shell_source_files()
        else:
            LOG.warning("Checking single file")
            clean_srcfiles_rpaths = [self.check_singlefile]

        return {
            "clean_hwdocs_rpaths": clean_hwdocs_rpaths,
            "clean_srcfiles_rpaths": clean_srcfiles_rpaths,
        }

    # def somethingelse(self):
    #     if self.cnf.handwritten_docs_indir:
    #         LOG.info("Processing handwritten doc files")
    #         hwdocs_rpaths = hfile.multiglob_dir_search(
    #             search_path=self.cnf.handwritten_docs_outdir,
    #             glob_patt_list=self.cnf.docs_glob_patterns,
    #         )
    #         LOG.debug("hwdocs_rpaths: %s", hwdocs_rpaths)

    #         # TODO: move exclusion_patterns_src into class init
    #         strict_exclusion_patterns_docs = [
    #             patt for patt in self.cnf.exclusion_patterns_docs
    #         ]
    #         LOG.debug(
    #             "strict_exclusion_patterns_docs: %s", strict_exclusion_patterns_docs
    #         )

    #         clean_hwdocs_rpaths = hfile.filter_paths_excluding_patterns(
    #             path_list=hwdocs_rpaths,
    #             exclusion_patterns_src=strict_exclusion_patterns_docs,
    #         )
    #         LOG.debug("clean_hwdocs_rpaths: %s", clean_hwdocs_rpaths)
    #         # sys.exit(42)

    #         # self.mkdocs_add_srcdocs_to_nav(self, catname_2mdfile_dict)

    #     LOG.info("Processing shell source files")
    #     if self.check_singlefile is None:
    #         src_absolute_path_list = hfile.multiglob_dir_search(
    #             search_path=self.cnf.project_docs_dir,
    #             glob_patt_list=self.cnf.shell_glob_patterns,
    #         )
    #     else:
    #         LOG.warning("Checking single file")
    #         src_absolute_path_list = [self.check_singlefile]

    #     LOG.debug("src_absolute_path_list: %s", src_absolute_path_list)

    #     # TODO: move exclusion_patterns_src into class init
    #     strict_exclusion_patterns_src = [
    #         f"/{patt}/" for patt in self.cnf.exclusion_patterns_src
    #     ]
    #     LOG.debug("strict_exclusion_patterns_src: %s", strict_exclusion_patterns_src)

    #     srcfiles_rpath = hfile.replace_substr_in_paths(
    #         input_paths=src_absolute_path_list,
    #         replace_path=self.cnf.program_root_dir,
    #     )
    #     LOG.info("srcfiles_rpath: %s", srcfiles_rpath)

    #     clean_srcfiles_rpaths = hfile.filter_paths_excluding_patterns(
    #         path_list=srcfiles_rpath,
    #         exclusion_patterns_src=strict_exclusion_patterns_src,
    #     )
    #     LOG.debug("clean_srcfiles_rpaths: %s", clean_srcfiles_rpaths)
