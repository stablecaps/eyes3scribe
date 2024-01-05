import logging
import os
import sys
from collections import defaultdict
from dataclasses import dataclass

from bashautodoc.helpo import hfile

LOG = logging.getLogger(__name__)


class Config:
    def __new__(cls, site_confname):
        LOG.info("Loading config: %s", site_confname)
        cls.cnf = hfile.load_yaml_file2dotmap(filename=site_confname)
        cls.check_config()

        LOG.info("conf: %s", cls.cnf)
        print(cls.cnf.extra_css)

        cls.set_default_patterns()

        cls.set_paths()

        cls.set_conf_bashautodoc_keys()

        cls.set_func_def_keywords()

        return cls.cnf

    @classmethod
    def check_config(cls):
        """
        Check the configuration for errors.
        """
        LOG.info("Checking config...")

        expected_keys = {
            "project_name": None,
            "site_name": None,
            "site_url": None,
            "site_author": None,
            "repo_url": None,
            "shell_srcdir": None,
            "catnames_src": None,
            "nav_codedocs_as_ref_or_main": ["ref", "main"],
        }

        current_conf_keys = list(cls.cnf.keys())

        for ckey in list(expected_keys.keys()):
            cvalue = cls.cnf.get(ckey)
            if ckey not in current_conf_keys:
                LOG.error(
                    "Error: Missing key <%s> in config file: <%s>\nExiting..",
                    ckey,
                    cls.site_confname,
                )
                sys.exit(42)

            expected_key_value = expected_keys.get(ckey)

            if isinstance(expected_key_value, list):
                if cvalue not in expected_key_value:
                    LOG.error(
                        "Error: Key <%s> in config file: <%s> has unexpected value <%s>\nOptions are: <%s>\nExiting..",
                        ckey,
                        cls.site_confname,
                        cvalue,
                        expected_key_value,
                    )
                    sys.exit(42)

            if cls.cnf.get(ckey) is None:
                LOG.error(
                    "Error: Key <%s> in config file: <%s> has no value\nExiting..",
                    ckey,
                    cls.site_confname,
                )
                sys.exit(42)

    @classmethod
    def set_default_patterns(cls):
        if "shell_glob_patterns" not in cls.cnf:
            cls.cnf.shell_glob_patterns = ["*.sh"]

        if "docs_glob_patterns" not in cls.cnf:
            cls.cnf.docs_glob_patterns = ["*.md"]

        LOG.info("Using shell_glob_patterns: %s", cls.cnf.shell_glob_patterns)
        LOG.info("Using docs_glob_patterns: %s", cls.cnf.docs_glob_patterns)

    @classmethod
    def set_paths(cls):
        ### Set paths
        cls.cnf.program_root_dir = os.path.abspath(".")
        # TODO: allow project_reldir to be initiated anywhere
        project_name = cls.cnf["project_name"]
        cls.cnf.project_absdir = os.path.abspath(project_name)
        cls.cnf.project_reldir = os.path.relpath(project_name)

        cls.cnf.project_docs_dir = f"{cls.cnf.project_reldir}/docs"
        cls.cnf.project_css_dir = f"{cls.cnf.project_docs_dir}/custom_css/"

        cls.cnf.handwritten_docs_outdir = f"./{cls.cnf.project_docs_dir}/docshw"

        cls.cnf.undef_category_dir = f"{cls.cnf.project_docs_dir}/undef"
        cls.cnf.undef_category_dir_hwdocs = f"{cls.cnf.project_docs_dir}/docshw/undef"
        cls.cnf.catnames_src.append("undef")
        cls.cnf.catnames_docs.append("undef")

    @classmethod
    def set_conf_bashautodoc_keys(cls):
        cls.cnf.bashautodoc_keys = [
            "bashautodoc_keys",
            "project_name",
            "program_root_dir",
            "project_reldir",
            "project_absdir",
            "project_docs_dir",
            "project_css_dir",
            "undef_category_dir",
            "undef_category_dir_hwdocs",
            "shell_srcdir",
            "shell_glob_patterns",
            "exclusion_patterns_src",
            "additional_mdfiles",
            "catnames_src",
            "catnames_docs",
            "nav_codedocs_as_ref_or_main",
            "nav_codedocs_name",
            "handwritten_docs_dir",
            "handwritten_docs_outdir",
            "docs_glob_patterns",
            "exclusion_patterns_docs",
            "rst2myst_configfile",
            "func_def_keywords",
        ]

    @classmethod
    def set_func_def_keywords(cls):
        cls.cnf.func_def_keywords = [
            "about",
            "group",
            "param",
            "example",
        ]

    # TODO: change this into a for loop
    @classmethod
    def log_config_info(cls):
        LOG.info("project_name: %s", cls.cnf.project_name)
        LOG.info("program_root_dir: %s", cls.cnf.program_root_dir)
        LOG.info("project_reldir: %s", cls.cnf.project_reldir)
        LOG.info("project_docs_dir: %s", cls.cnf.project_docs_dir)
        LOG.info("project_css_dir: %s", cls.cnf.project_css_dir)
        LOG.info("undef_category_dir: %s", cls.cnf.undef_category_dir)
        LOG.info(
            "undef_category_dir_hwdocs: %s",
            cls.cnf.undef_category_dir_hwdocs,
        )

        LOG.info("handwritten_docs_dir: %s", cls.cnf.handwritten_docs_dir)
        LOG.info("handwritten_docs_outdir: %s", cls.cnf.handwritten_docs_outdir)
        LOG.info("exclusion_patterns_src: %s", cls.exclusion_patterns_src)
        LOG.info("exclusion_patterns_docs: %s", cls.cnf.exclusion_patterns_docs)
